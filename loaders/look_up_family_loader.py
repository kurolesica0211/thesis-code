import json
from pathlib import Path

from loaders.loader import Loader, DataEntry


def get_loader():
    bench_dir = Path("custom_family_bench")
    ontology = str(bench_dir.joinpath("family_TBOX.ttl"))
    shacl = str(bench_dir.joinpath("family_shacl_final.ttl"))
    texts_dir = bench_dir.joinpath("royalty/denoised_texts")
    last_run_dir = "AAA"
    
    results_dir = Path("results")
    look_up_manifest = results_dir.joinpath(
        last_run_dir,
        "run_manifest.json"
    )
    if look_up_manifest.exists():
        with open(look_up_manifest, "r", encoding="utf-8") as f:
            json_manifest = json.load(f)
            task_manifests = json_manifest["task_manifests"]
        processed_ids = set([str(Path(p).parent).split("/")[-1] for p in task_manifests])
        data_graph_path = str(Path(task_manifests[-1]).parent.joinpath("final_data_graph.ttl"))
    else:
        processed_ids = set([])
        data_graph_path = None
        
    ids = set([
        str(path).split("/")[-1].removesuffix(".txt")
        for path in texts_dir.iterdir()
        if not str(path).split("/")[-1].startswith(".")
    ])
    final_ids = sorted(ids - processed_ids)
    
    data_entries = []
    text_filepaths = [str(texts_dir) + "/" + task_id + ".txt" for task_id in final_ids]
    
    '''step = 1
    for i in range(0, len(text_filepaths), step):
        entry = DataEntry(
            entry_id=f"{i}_{i+step-1}",
            text_filepaths=text_filepaths[i:i+step],
            ontology_filepath=ontology,
            shacl_filepath=shacl,
            data_graph_path=data_graph_path
        )
        data_entries.append(entry)'''
        
    # FAILURES
    li = [229]
    text_filepaths = [text_filepaths[l] for l in li]
    for i, id in enumerate(li):
        entry = DataEntry(
            entry_id=f"{id}_{id}",
            text_filepaths=[text_filepaths[i]],
            ontology_filepath=ontology,
            shacl_filepath=shacl,
            data_graph_path=data_graph_path
        )
        data_entries.append(entry)
    
    loader = Loader(data_entries)
    return loader