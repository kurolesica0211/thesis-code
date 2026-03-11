import sys
from dotenv import load_dotenv
from loaders.oskgc_loader import OSKGCLoader
from extractors.prompt_engine import PromptEngine
from extractors.extractor import Extractor
from runner import ExtractionRunner


def main():
    load_dotenv()

    # Configuration
    data_dir      = "OSKGC/data"
    json_ontology_dir  = "OSKGC/ontologies/json"
    split         = "dev"
    model_name    = "gemini/gemini-3.1-flash-lite-preview"

    # SHACL validation loop (RDF mode only)
    shacl_validation = True
    shacl_max_rounds = 1

    template_path      = "prompts/zero_shot_rdf.md"
    rdf_ontology_dir   = "OSKGC/ontologies/rdf"
    shacl_shapes_dir   = "OSKGC/ontologies/shacl_shapes"
    tag                = "rdf_shacl_1" if shacl_validation else "rdf_1"

    safe_model = model_name.replace("/", "_").replace(":", "_")
    run_dir    = f"results/{safe_model}_{tag}"

    # Optional: pass specific categories on the command line
    #   python main.py 1_Airport 2_Politician 3_Company
    categories = sys.argv[1:] if len(sys.argv) > 1 else None

    loader        = OSKGCLoader(data_dir=data_dir, ontology_dir=json_ontology_dir, split=split)
    prompt_engine = PromptEngine(template_path=template_path)
    extractor     = Extractor(model_name=model_name, prompt_engine=prompt_engine)

    runner = ExtractionRunner(
        loader=loader,
        extractor=extractor,
        run_dir=run_dir,
        categories=categories,
        rdf_ontology_dir=rdf_ontology_dir,
        shacl_validation=shacl_validation,
        shacl_max_rounds=shacl_max_rounds,
        shacl_shapes_dir=shacl_shapes_dir,
    )
    runner.run()


if __name__ == "__main__":
    main()
