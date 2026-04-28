import os

from loaders.loader import Loader, DataEntry


def get_loader():
    dir = "custom_family_bench"
    input_text = "Queen_Victoria.txt"
    ontology = "family_TBOX.ttl"
    shacl = "family_shacl_final.ttl"
    
    data_entry = DataEntry(
        entry_id="royal_family",
        text_filepaths=[os.path.join(dir, input_text)],
        ontology_filepath=os.path.join(dir, ontology),
        shacl_filepath=os.path.join(dir, shacl)
    )
    
    loader = Loader([data_entry])
    
    return loader