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
    """Runs extraction only (no evaluation). Results are saved as JSONL."""

    def __init__(self, loader: OSKGCLoader, extractor: Extractor,
                 output_file: str, delay: float = RATELIMIT_DELAY,
                 categories: Optional[List[str]] = None,
                 ontology_mode: str = "json",
                 rdf_ontology_dir: Optional[str] = None,
                 shacl_validation: bool = False,
                 shacl_max_rounds: int = 1):
        self.loader      = loader
        self.extractor   = extractor
        self.output_file  = output_file
        self.delay       = delay
        self.categories  = categories   # None → process all
        self.ontology_mode = ontology_mode  # "json" or "rdf"
        self.rdf_ontology_dir = rdf_ontology_dir  # e.g. "OSKGC/ontologies/rdf"
        self.shacl_validation = shacl_validation
        self.shacl_max_rounds = shacl_max_rounds

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

        os.makedirs(os.path.dirname(self.output_file) or ".", exist_ok=True)
        failed_batches: List[str] = []

        # Append mode so we can add to an existing file.
        with open(self.output_file, "a", encoding="utf-8") as f:
            for batch_idx, batch in enumerate(tqdm(batches, desc="Categories")):
                if self.ontology_mode == "rdf":
                    rdf_path = os.path.join(
                        self.rdf_ontology_dir, f"{batch.category}.ttl")
                    with open(rdf_path, "r", encoding="utf-8") as rf:
                        rdf_text = rf.read()
                    if self.shacl_validation:
                        batch_result = self.extractor.extract_batch_rdf_with_shacl(
                            batch.entries, rdf_text,
                            max_rounds=self.shacl_max_rounds,
                        )
                    else:
                        batch_result = self.extractor.extract_batch_rdf(
                            batch.entries, rdf_text)
                else:
                    batch_result = self.extractor.extract_batch(
                        batch.entries, batch.schema_def)

                all_empty = all(
                    len(v.triples) == 0 for v in batch_result.results.values())
                if all_empty:
                    failed_batches.append(batch.category)

                for i, entry in enumerate(batch.entries, 1):
                    key = f"entry_{i}"
                    ext = batch_result.results.get(key)
                    record = {
                        "entry_id":     entry.entry_id,
                        "input_text":   entry.input_text,
                        "gold_triples": [t.model_dump() for t in entry.gold_triples],
                        "pred_triples": [t.model_dump() for t in ext.triples] if ext else [],
                        "pred_schemas": [s.model_dump() for s in ext.schemas] if ext else [],
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    f.flush()

                if self.delay > 0 and batch_idx < len(batches) - 1:
                    time.sleep(self.delay)

        print(f"\nExtraction complete. Results saved to {self.output_file}")
        if failed_batches:
            print(f"WARNING: {len(failed_batches)} batches returned no triples: "
                  f"{failed_batches}")
