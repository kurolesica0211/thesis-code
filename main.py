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
    ontology_dir  = "OSKGC/ontologies"
    split         = "dev"
    model_name    = "gemini/gemini-3-flash-preview"

    # Ontology mode: "json" (structured schema) or "rdf" (copy-paste .ttl)
    ontology_mode = "rdf"

    if ontology_mode == "rdf":
        template_path    = "prompts/zero_shot_rdf.md"
        rdf_ontology_dir = "OSKGC/ontologies/rdf"
        tag              = "rdf_1"
    else:
        template_path    = "prompts/zero_shot_basic.md"
        rdf_ontology_dir = None
        tag              = "json_1"

    safe_model  = model_name.replace("/", "_").replace(":", "_")
    output_file = f"results/results_{safe_model}_{tag}.jsonl"

    # Optional: pass specific categories on the command line
    #   python main.py 1_Airport 2_Politician 3_Company
    categories = sys.argv[1:] if len(sys.argv) > 1 else None

    loader        = OSKGCLoader(data_dir=data_dir, ontology_dir=ontology_dir, split=split)
    prompt_engine = PromptEngine(template_path=template_path)
    extractor     = Extractor(model_name=model_name, prompt_engine=prompt_engine)

    runner = ExtractionRunner(
        loader=loader,
        extractor=extractor,
        output_file=output_file,
        categories=categories,
        ontology_mode=ontology_mode,
        rdf_ontology_dir=rdf_ontology_dir,
    )
    runner.run()


if __name__ == "__main__":
    main()
