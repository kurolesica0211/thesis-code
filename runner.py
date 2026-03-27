import os
import time
import json
from datetime import datetime, timezone
from typing import List, Optional
from tqdm import tqdm
from loaders.base_loader import BaseLoader
from extractors.extractor import Extractor
from orchestration import build_shacl_batch_graph
from orchestration.tracing import append_trace
from evaluator.evaluator import Evaluator
from models.data_models import EntryExtractionResult

# Seconds to wait between API calls to avoid rate-limit errors.
RATELIMIT_DELAY = 4.0


class ExtractionRunner:
    """Runs extraction only (no evaluation).

    Output layout::

        {run_dir}/
            results.json
            shacl_corrections.log (if shacl_log_enabled=True)
    """

    def __init__(self, loader: BaseLoader, extractor: Extractor,
                 run_dir: str, delay: float = RATELIMIT_DELAY,
                 categories: Optional[List[str]] = None,
                 rdf_ontology: Optional[str] = None,
                 shacl_validation: bool = False,
                 shacl_max_rounds: int = 1,
                 shacl_shapes: Optional[str] = None,
                 shacl_log_enabled: bool = False,
                 prompt_caching_enabled: bool = True,
                 correction_template_path: str = "prompts/two_step_correction/correction.md",
                 violation_translation_template_path: str = "prompts/two_step_correction/violation_translation.md",
                 run_config: Optional[dict] = None):
        self.loader           = loader
        self.extractor        = extractor
        self.run_dir          = run_dir
        self.delay            = delay
        self.categories       = categories
        self.rdf_ontology = rdf_ontology
        self.shacl_validation = shacl_validation
        self.shacl_max_rounds = shacl_max_rounds
        self.shacl_shapes = shacl_shapes
        self.shacl_log_enabled = shacl_log_enabled
        self.prompt_caching_enabled = prompt_caching_enabled
        self.shacl_log_path   = os.path.join(run_dir, "shacl_corrections.log") if shacl_log_enabled else None
        self.shacl_graph = build_shacl_batch_graph(extractor) if shacl_validation else None
        self.correction_template_path = correction_template_path
        self.violation_translation_template_path = violation_translation_template_path
        self.run_config = run_config or {}

        self.artifacts_dir = os.path.join(run_dir, "artifacts")
        self.batch_artifacts_dir = os.path.join(self.artifacts_dir, "batches")
        self.manifests_dir = os.path.join(run_dir, "manifests")
        self.trace_path = os.path.join(run_dir, "run_events.jsonl")
        self.metrics_path = os.path.join(run_dir, "metrics_summary.json")
        self.run_manifest_path = os.path.join(self.manifests_dir, "run_manifest.json")

    def run(self):
        print("Loading data by category...")
        all_batches = self.loader.load_by_category()

        if self.categories:
            batches = [b for b in all_batches if b.category in self.categories]
            if not batches:
                available = [b.category for b in all_batches]
                raise ValueError(f"None of {self.categories} found. "
                                 f"Available: {available}")
            print(f"Filtered to {len(batches)} categories: {self.categories}")
        else:
            batches = all_batches

        total_entries = sum(len(b.entries) for b in batches)
        print(f"Will process {total_entries} entries across {len(batches)} batches.")

        os.makedirs(self.run_dir, exist_ok=True)
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.batch_artifacts_dir, exist_ok=True)
        os.makedirs(self.manifests_dir, exist_ok=True)

        failed_batches: List[str] = []
        all_records: List[dict] = []
        all_metrics: List[dict] = []
        evaluator = Evaluator()

        run_manifest = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "run_dir": self.run_dir,
            "config": self.run_config,
            "batches": [],
            "failed_batches": [],
        }
        append_trace(self.trace_path, "run.start", {
            "run_dir": self.run_dir,
            "shacl_validation": self.shacl_validation,
            "total_batches": len(batches),
            "total_entries": total_entries,
        })
        
        # Initialize SHACL log file if enabled
        if self.shacl_log_enabled:
            with open(self.shacl_log_path, "w", encoding="utf-8") as f:
                f.write("="*80 + "\n")
                f.write("SHACL Validation & Correction Log\n")
                f.write("="*80 + "\n\n")

        for batch_idx, batch in enumerate(tqdm(batches, desc="Categories")):
            append_trace(self.trace_path, "batch.start", {
                "batch_idx": batch_idx,
                "category": batch.category,
                "entries": len(batch.entries),
            })

            rdf_path = self.resolve_ontology(batch.category)
            with open(rdf_path, "r", encoding="utf-8") as rf:
                rdf_text = rf.read()

            batch_artifact_dir = os.path.join(
                self.batch_artifacts_dir,
                f"{batch_idx + 1:03d}_{batch.category.replace('/', '_')}"
            )
            os.makedirs(batch_artifact_dir, exist_ok=True)

            if self.shacl_validation:
                shacl_path = self.resolve_shacl(batch.category)
                with open(shacl_path, "r", encoding="utf-8") as sf:
                    shacl_text = sf.read()
                
                ontology_format = self.get_ontology_format(rdf_path)

                graph_state = self.shacl_graph.invoke(
                    {
                        "batch": batch,
                        "rdf_ontology_text": rdf_text,
                        "shacl_shapes_ttl": shacl_text,
                        "ontology_format": ontology_format,
                        "max_rounds": self.shacl_max_rounds,
                        "current_round": 1,
                        "correction_template_path": self.correction_template_path,
                        "violation_translation_template_path": self.violation_translation_template_path,
                        "prompt_caching_enabled": self.prompt_caching_enabled,
                        "shacl_log_file": self.shacl_log_path if self.shacl_log_enabled else None,
                        "trace_path": self.trace_path,
                        "artifact_dir": batch_artifact_dir,
                    }
                )
                batch_result = graph_state["batch_result"]
                done_reason = graph_state.get("done_reason", "unknown")
                
            else:
                batch_result = self.extractor.extract_batch_rdf(
                    batch.entries, rdf_text,
                    schema_def=batch.schema_def)
                done_reason = "no_shacl"

            all_empty = all(
                len(v.triples) == 0 for v in batch_result.results.values())
            if all_empty:
                failed_batches.append(batch.category)

            # ── Collect records ────────────────────────────────────────────
            for i, entry in enumerate(batch.entries, 1):
                key = f"entry_{i}"
                ext = batch_result.results.get(key)
                ext = ext if ext is not None else EntryExtractionResult()
                ev = evaluator.evaluate(entry, ext)
                all_records.append({
                    "entry_id":     entry.entry_id,
                    "input_text":   entry.input_text,
                    "gold_triples": [t.model_dump() for t in entry.gold_triples],
                    "pred_triples": [t.model_dump() for t in ext.triples],
                    "pred_schemas": [s.model_dump() for s in ext.schemas],
                    "precision": ev.precision,
                    "recall": ev.recall,
                    "f1": ev.f1,
                })
                all_metrics.append({
                    "entry_id": entry.entry_id,
                    "category": batch.category,
                    "precision": ev.precision,
                    "recall": ev.recall,
                    "f1": ev.f1,
                })

            batch_manifest = {
                "batch_idx": batch_idx,
                "category": batch.category,
                "entry_count": len(batch.entries),
                "done_reason": done_reason,
                "all_empty": all_empty,
                "artifact_dir": batch_artifact_dir,
                "rdf_path": rdf_path,
                "shacl_path": shacl_path if self.shacl_validation else None,
            }
            batch_manifest_path = os.path.join(
                self.manifests_dir,
                f"batch_{batch_idx + 1:03d}_{batch.category.replace('/', '_')}.json"
            )
            with open(batch_manifest_path, "w", encoding="utf-8") as f:
                json.dump(batch_manifest, f, ensure_ascii=False, indent=2)
            run_manifest["batches"].append(batch_manifest_path)

            append_trace(self.trace_path, "batch.end", {
                "batch_idx": batch_idx,
                "category": batch.category,
                "done_reason": done_reason,
                "all_empty": all_empty,
            })

            if self.delay > 0 and batch_idx < len(batches) - 1:
                time.sleep(self.delay)

        # ── Write single results file ─────────────────────────────────────
        results_path = os.path.join(self.run_dir, "results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(all_records, f, ensure_ascii=False, indent=2)

        metric_count = len(all_metrics)
        avg_precision = sum(m["precision"] for m in all_metrics) / metric_count if metric_count else 0.0
        avg_recall = sum(m["recall"] for m in all_metrics) / metric_count if metric_count else 0.0
        avg_f1 = sum(m["f1"] for m in all_metrics) / metric_count if metric_count else 0.0

        metrics_summary = {
            "entry_count": metric_count,
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1": avg_f1,
            "entries": all_metrics,
        }
        with open(self.metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics_summary, f, ensure_ascii=False, indent=2)

        run_manifest["failed_batches"] = failed_batches
        run_manifest["metrics_summary"] = self.metrics_path
        run_manifest["results"] = results_path
        run_manifest["trace"] = self.trace_path
        run_manifest["completed_at"] = datetime.now(timezone.utc).isoformat()
        with open(self.run_manifest_path, "w", encoding="utf-8") as f:
            json.dump(run_manifest, f, ensure_ascii=False, indent=2)

        append_trace(self.trace_path, "run.end", {
            "results": results_path,
            "failed_batches": len(failed_batches),
            "metrics": {
                "avg_precision": avg_precision,
                "avg_recall": avg_recall,
                "avg_f1": avg_f1,
            }
        })

        print(f"\nExtraction complete. Results saved to {results_path}")
        print(f"Run manifest saved to {self.run_manifest_path}")
        if failed_batches:
            print(f"WARNING: {len(failed_batches)} batches returned no triples: "
                  f"{failed_batches}")

    def resolve_ontology(self, category: str = None):
        if os.path.isfile(self.rdf_ontology):
            rdf_path = self.rdf_ontology
        elif os.path.isdir(self.rdf_ontology):
            rdf_path = os.path.join(self.rdf_ontology, f"{category}.ttl")
            if os.path.isfile(rdf_path) != True:
                rdf_path = os.path.join(self.rdf_ontology, f"{category}.owl")
                if os.path.isfile(rdf_path) != True:
                    raise FileNotFoundError(f"No RDF ontology file found for category '{category}' in {self.rdf_ontology}")
        return rdf_path
                
    def resolve_shacl(self, category: str = None):
        if os.path.isfile(self.shacl_shapes):
            shacl_path = self.shacl_shapes
        elif os.path.isdir(self.shacl_shapes):
            shacl_path = os.path.join(self.shacl_shapes, f"{category}_shacl.ttl")
            if os.path.isfile(shacl_path) != True:
                raise FileNotFoundError(f"No SHACL shapes file found for category '{category}' in {self.shacl_shapes}")
        return shacl_path
    
    def get_ontology_format(self, filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".ttl":
            return "turtle"
        elif ext == ".owl":
            return "xml"
        else:
            raise ValueError(f"Unsupported ontology file extension: {ext}")