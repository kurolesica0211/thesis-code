from loaders.loader import Loader, DataEntry


def get_loader():
    bench_dir = "custom_family_bench"
    entry = DataEntry(
        entry_id="Prince_Bernhard_of_Lippe-Biesterfeld",
        text_filepaths=[f"{bench_dir}/royalty/denoised_texts_fuzzy_match/Q57304.txt"],
        ontology_filepath=f"{bench_dir}/family_TBOX.ttl",
        shacl_filepath=f"{bench_dir}/family_shacl_final.ttl",
    )
    return Loader([entry])
