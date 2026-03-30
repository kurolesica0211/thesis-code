import argparse
import os
from dotenv import load_dotenv
from loaders.base_family_loader import get_loader
from runner import ExtractionRunner
from configs.run_config import RunConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM KG extraction with SHACL verification")
    parser.add_argument("--config", default="configs/run_config.yaml", help="Path to YAML run config")
    return parser.parse_args()


def _build_loader(config: RunConfig):
    if config.dataset.source == "custom_family_bench":
        ds = config.dataset.custom_family_bench
        loader = get_loader()
        custom_tag = config.output.custom_tag or "family"

    return loader, custom_tag


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

    loader, custom_tag = _build_loader(config)
    run_dir = _compute_run_dir(config, custom_tag)

    runner = ExtractionRunner(
        loader=loader,
        run_dir=run_dir,
        delay=config.runtime.delay_seconds,
        max_iterations=config.runtime.max_iterations,
        shacl_log_enabled=config.shacl.log_enabled,
        prompt_caching_enabled=config.shacl.prompt_caching_enabled,
        run_config=config.model_dump(),
    )
    runner.run()


if __name__ == "__main__":
    main()
