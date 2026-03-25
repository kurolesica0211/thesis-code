import sys
from dotenv import load_dotenv
from loaders.oskgc_loader import OSKGCLoader
from loaders.custom_family_bench_loader import CustomFamilyBenchLoader
from extractors.prompt_engine import PromptEngine
from extractors.extractor import Extractor
from runner import ExtractionRunner


def main():
    load_dotenv()

    # Configuration
    data_dir      = "OSKGC/data"
    split         = "dev"
    #model_name    = "gemini/gemini-3.1-flash-lite-preview"
    model_name = "gemini/gemini-flash-lite-latest"

    # SHACL validation loop
    shacl_validation = True
    shacl_max_rounds = 1
    shacl_log_enabled = True  # Set to True to enable SHACL correction logging

    template_path      = "prompts/zero_shot_rdf.md"
    #oskgc_ontology_dir   = "OSKGC/ontologies/rdf"
    #oskgc_shapes_dir   = "OSKGC/ontologies/shacl_shapes"
    family_ontology = "custom_family_bench/family_TBOX.owl"
    family_shapes   = "custom_family_bench/family_TBOX_shacl_opened.ttl"
    habsburgs_text   = "custom_family_bench/habsburgs.txt"
    tag                = "rdf_shacl" if shacl_validation else "rdf"
    custom_tag = "habsburgs"

    safe_model = model_name.replace("/", "_").replace(":", "_")
    run_dir    = f"results/{custom_tag}_{tag}_{safe_model}"

    # Optional: pass specific categories on the command line
    #   python main.py 1_Airport 2_Politician 3_Company
    categories = sys.argv[1:] if len(sys.argv) > 1 else None

    #loader        = OSKGCLoader(data_dir=data_dir, ontology_dir=rdf_ontology_dir, split=split)
    loader = CustomFamilyBenchLoader(
        input_text_file=habsburgs_text,
        ontology_file=family_ontology,
        shacl_file=family_shapes
    )
    prompt_engine = PromptEngine(template_path=template_path)
    extractor     = Extractor(model_name=model_name, prompt_engine=prompt_engine)

    runner = ExtractionRunner(
        loader=loader,
        extractor=extractor,
        run_dir=run_dir,
        categories=categories,
        rdf_ontology=family_ontology,
        shacl_validation=shacl_validation,
        shacl_max_rounds=shacl_max_rounds,
        shacl_shapes=family_shapes,
        shacl_log_enabled=shacl_log_enabled,
    )
    runner.run()


if __name__ == "__main__":
    main()
