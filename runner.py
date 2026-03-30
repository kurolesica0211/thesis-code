import os
import time
import json
from datetime import datetime, timezone
from typing import List, Optional
from tqdm import tqdm

from loaders.loader import Loader
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

    def __init__(self, loader: Loader, extractor: Extractor,
                 run_dir: str, delay: float = RATELIMIT_DELAY,
                 max_iterations: int = 10,
                 shacl_log_enabled: bool = False,
                 prompt_caching_enabled: bool = True,
                 run_config: Optional[dict] = None):
        self.loader                 = loader
        self.extractor              = extractor
        self.run_dir                = run_dir
        self.delay                  = delay
        self.max_iterations         = max_iterations
        self.shacl_log_enabled      = shacl_log_enabled
        self.prompt_caching_enabled = prompt_caching_enabled
        self.shacl_log_path         = os.path.join(run_dir, "shacl_corrections.log") if shacl_log_enabled else None
        self.shacl_graph            = build_shacl_batch_graph(extractor)
        self.run_config             = run_config or {}

        self.artifacts_dir = os.path.join(run_dir, "artifacts")
        self.task_artifacts_dir = os.path.join(self.artifacts_dir, "task_entries")
        self.manifests_dir = os.path.join(run_dir, "manifests")
        self.trace_path = os.path.join(run_dir, "run_events.jsonl")
        self.metrics_path = os.path.join(run_dir, "metrics_summary.json")
        self.run_manifest_path = os.path.join(self.manifests_dir, "run_manifest.json")

    def run(self):
        print("Starting up...")

        os.makedirs(self.run_dir, exist_ok=True)
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.task_artifacts_dir, exist_ok=True)
        os.makedirs(self.manifests_dir, exist_ok=True)

        failed_batches: List[str] = []
        all_records: List[dict] = []

        total_entries = self.loader.get_total()
        print(f"Will process {total_entries} of task entries.")

        run_manifest = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "run_dir": self.run_dir,
            "config": self.run_config,
            "entries": [],
            "failed_entries": [],
        }
        append_trace(self.trace_path, "run.start", {
            "run_dir": self.run_dir,
            "total_entries": total_entries
        })

        for entry_idx, entry in enumerate(tqdm(self.loader.load(), total=total_entries, desc="Task Entries")):
            append_trace(self.trace_path, "task_entry.start", {
                "entry_idx": entry_idx,
                "data_entry_id": entry.entry_id,
                "text_files": len(entry.text_filepaths),
            })

            task_artifact_dir = os.path.join(
                self.task_artifacts_dir,
                f"{entry_idx + 1:03d}_{entry.entry_id.replace('/', '_')}"
            )
            os.makedirs(task_artifact_dir, exist_ok=True)

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