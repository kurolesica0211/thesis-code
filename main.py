"""Entry point for the LLM-based Knowledge Graph extraction pipeline.

This module parses CLI args, loads the run configuration, and dispatches
either the synchronous or asynchronous runner depending on the config.
"""

import argparse
import asyncio
from dotenv import load_dotenv

from configs.run_config import RunConfig
from runner import run
from async_runner import run_async


def parse_args() -> argparse.Namespace:
    """Parse command-line args.

    By default points to an example run config.
    """
    parser = argparse.ArgumentParser(description="LLM KG extraction with SHACL verification")
    parser.add_argument("--config", default="configs/run_config.yaml", help="Path to YAML run config")
    #parser.add_argument("--config", default="configs/example_run_config.yaml", help="Path to YAML run config")
    return parser.parse_args()


def main():
    """Load environment, configuration and start the chosen runner.

    - Loads environment variables from a `.env` file (if present).
    - Reads config via `RunConfig.from_yaml`.
    - Calls `run_async` when `runtime.async_mode` is true, else `run`.
    """
    load_dotenv()
    args = parse_args()
    config = RunConfig.from_yaml(args.config)
    
    if config.runtime.async_mode:
        # Run in async mode
        asyncio.run(run_async(config))
    else:
        # Run in sync mode
        run(config)


if __name__ == "__main__":
    main()
