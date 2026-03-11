import os
import time
import json
from typing import List, Optional
from tqdm import tqdm
from loaders.oskgc_loader import OSKGCLoader
from extractors.extractor import Extractor
from models.data_models import CategoryBatch

# Seconds to wait between API calls to avoid rate-limit errors.
RATELIMIT_DELAY = 4.0


class ExtractionRunner:
    """Runs extraction only (no evaluation).

    Output layout::

        {run_dir}/
            results.json
    """

    def __init__(self, loader: OSKGCLoader, extractor: Extractor,
                 run_dir: str, delay: float = RATELIMIT_DELAY,
                 categories: Optional[List[str]] = None,
                 ontology_mode: str = "json",
                 rdf_ontology_dir: Optional[str] = None,
                 shacl_validation: bool = False,
                 shacl_max_rounds: int = 1,
                 shacl_shapes_dir: Optional[str] = None):
        self.loader           = loader
        self.extractor        = extractor
        self.run_dir          = run_dir
        self.delay            = delay
        self.categories       = categories
        self.rdf_ontology_dir = rdf_ontology_dir
        self.shacl_validation = shacl_validation
        self.shacl_max_rounds = shacl_max_rounds
        self.shacl_shapes_dir = shacl_shapes_dir

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
        failed_batches: List[str] = []
        all_records: List[dict] = []

        for batch_idx, batch in enumerate(tqdm(batches, desc="Categories")):

            rdf_path = os.path.join(self.rdf_ontology_dir, f"{batch.category}.ttl")
            with open(rdf_path, "r", encoding="utf-8") as rf:
                rdf_text = rf.read()

            if self.shacl_validation:
                shacl_path = os.path.join(
                    self.shacl_shapes_dir, f"{batch.category}_shacl.ttl")
                with open(shacl_path, "r", encoding="utf-8") as sf:
                    shacl_text = sf.read()
                batch_result = self.extractor.extract_batch_rdf_with_shacl(
                    batch.entries, rdf_text, shacl_text,
                    max_rounds=self.shacl_max_rounds,
                    schema_def=batch.schema_def,
                )
            else:
                batch_result = self.extractor.extract_batch_rdf(
                    batch.entries, rdf_text,
                    schema_def=batch.schema_def)

            all_empty = all(
                len(v.triples) == 0 for v in batch_result.results.values())
            if all_empty:
                failed_batches.append(batch.category)

            # ── Collect records ────────────────────────────────────────────
            for i, entry in enumerate(batch.entries, 1):
                key = f"entry_{i}"
                ext = batch_result.results.get(key)
                all_records.append({
                    "entry_id":     entry.entry_id,
                    "input_text":   entry.input_text,
                    "gold_triples": [t.model_dump() for t in entry.gold_triples],
                    "pred_triples": [t.model_dump() for t in ext.triples] if ext else [],
                    "pred_schemas": [s.model_dump() for s in ext.schemas] if ext else [],
                })

            if self.delay > 0 and batch_idx < len(batches) - 1:
                time.sleep(self.delay)

        # ── Write single results file ─────────────────────────────────────
        results_path = os.path.join(self.run_dir, "results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(all_records, f, ensure_ascii=False, indent=2)

        print(f"\nExtraction complete. Results saved to {results_path}")
        if failed_batches:
            print(f"WARNING: {len(failed_batches)} batches returned no triples: "
                  f"{failed_batches}")
