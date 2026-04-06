import argparse
from dotenv import load_dotenv

from configs.run_config import RunConfig
from runner import run

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM KG extraction with SHACL verification")
    parser.add_argument("--config", default="configs/run_config.yaml", help="Path to YAML run config")
    return parser.parse_args()

def main():
    load_dotenv()
    args = parse_args()
    config = RunConfig.from_yaml(args.config)
    
    run(config)


if __name__ == "__main__":
    main()
