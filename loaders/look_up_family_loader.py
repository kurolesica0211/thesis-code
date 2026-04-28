import json
from pathlib import Path
from rdflib import Graph

from loaders.loader import Loader, DataEntry


def get_loader():
    bench_dir = Path("custom_family_bench")
    ontology = str(bench_dir.joinpath("family_TBOX.ttl"))
    shacl = str(bench_dir.joinpath("family_shacl_final.ttl"))
    texts_dir = bench_dir.joinpath("british_royalty_texts")
    last_run_dir = "british_royalty_gemini_flash_lite_0"
    
    results_dir = Path("results")
    look_up_manifest = results_dir.joinpath(
        last_run_dir,
        "run_manifest.json"
    )
    if look_up_manifest.exists():
        with open(look_up_manifest, "r") as f:
            json_manifest = json.load(f)
            task_manifests = json_manifest["task_manifests"]
        processed_ids = set([str(Path(p).parent).split("/")[-1] for p in task_manifests])
        data_graph_path = str(Path(task_manifests[-1]).parent.joinpath("final_data_graph.ttl"))
    else:
        processed_ids = set([])
        data_graph_path = None
        
    ids = set([str(path).split("/")[-1].strip(".txt") for path in texts_dir.iterdir()])
    final_ids = ids - processed_ids
    
    data_entries = []
    for task_id in final_ids:
        entry = DataEntry(
            entry_id=task_id,
            text_filepaths=[str(texts_dir) + "/" + task_id + ".txt"],
            ontology_filepath=ontology,
            shacl_filepath=shacl,
            data_graph_path=data_graph_path
        )
        data_entries.append(entry)
    
    loader = Loader(data_entries)
    return loader