"""Loader for the SHACL-backed repair experiment.

Reads `experiments/shacl_repair/sample_manifest.json` (produced by
`experiments/shacl_repair/sample_documents.py`) and builds one `DataEntry`
per sampled document, seeded with that document's own raw `delta_graph.ttl`
from its original baseline run via `data_graph_path`, so the pipeline
continues editing the existing graph instead of starting from empty.

Hard-coded for this one experiment: the sample picks themselves come from
the manifest, but the ontology/shapes paths and manifest location are fixed.

Entries that already have a `task_manifest.json` in the output run directory
are skipped, so a crashed/partial run (e.g. from a transient API error) can
be resumed by just rerunning the same config.
"""

import json
from pathlib import Path

from loaders.loader import Loader, DataEntry

MANIFEST_PATH = Path("experiments/shacl_repair/sample_manifest.json")
BENCH_DIR = Path("custom_family_bench")
ONTOLOGY_PATH = str(BENCH_DIR / "family_TBOX.ttl")
SHACL_PATH = str(BENCH_DIR / "family_shacl_final.ttl")
TEXTS_DIR = BENCH_DIR / "royalty" / "denoised_texts_fuzzy_match"
RUN_DIR = Path("results/shacl_repair_experiment")


def get_loader():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    data_entries = []
    for sample in manifest["samples"]:
        entry_id = sample["entry_id"]
        if (RUN_DIR / entry_id / "task_manifest.json").exists():
            continue

        text_path = str(TEXTS_DIR / f"{sample['qid']}.txt")
        data_entries.append(DataEntry(
            entry_id=entry_id,
            text_filepaths=[text_path],
            ontology_filepath=ONTOLOGY_PATH,
            shacl_filepath=SHACL_PATH,
            data_graph_path=sample["seed_data_graph_path"],
        ))

    return Loader(data_entries)
