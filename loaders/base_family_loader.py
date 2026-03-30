import os

from loaders.loader import Loader, DataEntry


def get_loader():
    dir = "custom_family_bench"
    input_text = "habsburgs.txt"
    ontology = "family_TBOX.owl"
    shacl = "family_TBOX_shacl_closed.ttl"
    
    data_entry = DataEntry(
        entry_id="habsburgs",
        text_filepaths=[os.path.join(dir, input_text)],
        gold_triples_filepaths=None,
        ontology_filepath=os.path.join(dir, ontology),
        shacl_filepath=os.path.join(dir, shacl),
        data_graph_path=None
    )
    
    loader = Loader([data_entry])
    
    return loader