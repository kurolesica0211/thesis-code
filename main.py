import argparse
import os
from dotenv import load_dotenv
from loaders.oskgc_loader import OSKGCLoader
from loaders.custom_family_bench_loader import CustomFamilyBenchLoader
from extractors.prompt_engine import PromptEngine
from extractors.extractor import Extractor
from runner import ExtractionRunner
from configs.run_config import RunConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM KG extraction with SHACL verification")
    parser.add_argument("--config", default="configs/run_config.yaml", help="Path to YAML run config")
    parser.add_argument("--model-name", help="Override model name")
    parser.add_argument("--categories", nargs="*", help="Optional category filters")
    parser.add_argument("--dataset", choices=["custom_family_bench", "oskgc"], help="Override dataset source")
    parser.add_argument("--disable-shacl", action="store_true", help="Disable SHACL validation loop")
    parser.add_argument("--shacl-max-rounds", type=int, help="Override SHACL correction rounds")
    parser.add_argument("--run-dir", help="Override full output run directory")
    return parser.parse_args()


def _build_loader(config: RunConfig):
    if config.dataset.source == "custom_family_bench":
        ds = config.dataset.custom_family_bench
        loader = CustomFamilyBenchLoader(
            input_text_file=ds.input_text_file,
            ontology_file=ds.ontology_file,
            shacl_file=ds.shacl_file,
        )
        rdf_ontology = ds.ontology_file
        shacl_shapes = ds.shacl_file
        custom_tag = config.output.custom_tag or "family"
    else:
        ds = config.dataset.oskgc
        loader = OSKGCLoader(
            data_dir=ds.data_dir,
            ontology_dir=ds.ontology_dir,
            split=ds.split,
        )
        rdf_ontology = ds.ontology_dir
        shacl_shapes = ds.shacl_shapes_dir
        custom_tag = f"oskgc_{ds.split}"

    return loader, rdf_ontology, shacl_shapes, custom_tag


def _compute_run_dir(config: RunConfig, custom_tag: str) -> str:
    if config.output.run_dir:
        return config.output.run_dir
    tag = "rdf_shacl" if config.shacl.enabled else "rdf"
    safe_model = config.model.name.replace("/", "_").replace(":", "_")
    return os.path.join(config.output.base_dir, f"{custom_tag}_{tag}_{safe_model}")


def main():
    load_dotenv()
    args = parse_args()
    config = RunConfig.from_yaml(args.config)

    if args.model_name:
        config.model.name = args.model_name
    if args.categories is not None:
        config.categories = args.categories
    if args.dataset:
        config.dataset.source = args.dataset
    if args.disable_shacl:
        config.shacl.enabled = False
    if args.shacl_max_rounds is not None:
        config.shacl.max_rounds = args.shacl_max_rounds
    if args.run_dir:
        config.output.run_dir = args.run_dir

    loader, rdf_ontology, shacl_shapes, custom_tag = _build_loader(config)
    run_dir = _compute_run_dir(config, custom_tag)

    prompt_engine = PromptEngine(template_path=config.prompts.extraction_template)
    extractor = Extractor(model_name=config.model.name, prompt_engine=prompt_engine)

    runner = ExtractionRunner(
        loader=loader,
        extractor=extractor,
        run_dir=run_dir,
        delay=config.runtime.delay_seconds,
        categories=config.categories or None,
        rdf_ontology=rdf_ontology,
        shacl_validation=config.shacl.enabled,
        shacl_max_rounds=config.shacl.max_rounds,
        shacl_shapes=shacl_shapes,
        shacl_log_enabled=config.shacl.log_enabled,
        prompt_caching_enabled=config.shacl.prompt_caching_enabled,
        correction_template_path=config.prompts.correction_template,
        violation_translation_template_path=config.prompts.violation_translation_template,
        run_config=config.model_dump(),
    )
    runner.run()


if __name__ == "__main__":
    main()
