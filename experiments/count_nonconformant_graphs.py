from __future__ import annotations

import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import re

from rdflib import Graph

from core.shacl_functions import pyshacl_validate


RUN_DIR_PATTERN = re.compile(r"^\d+_\d+$")
DEFAULT_RESULTS_DIR = Path("results/royalty_gemini_without_shacl")
DEFAULT_SHAPES_PATH = Path("custom_family_bench/family_shacl_final.ttl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count how many delta_graph.ttl files are non-conformant against a SHACL shapes graph."
    )
    parser.add_argument(
        "results_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_RESULTS_DIR,
        help="Directory containing numbered run folders like 0_0, 1_1, ...",
    )
    parser.add_argument(
        "--shapes",
        type=Path,
        default=DEFAULT_SHAPES_PATH,
        help="Path to the SHACL shapes graph.",
    )
    return parser.parse_args()


def discover_run_dirs(results_dir: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in results_dir.iterdir()
            if path.is_dir() and RUN_DIR_PATTERN.match(path.name)
        ],
        key=lambda path: (int(path.name.split("_")[0]), int(path.name.split("_")[1])),
    )


def load_graph(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path)
    return graph


def is_conformant(data_graph: Graph, shapes_graph: Graph) -> bool:
    conforms, _, _ = pyshacl_validate(data_graph, None, shapes_graph)
    return bool(conforms)


def main() -> None:
    args = parse_args()

    results_dir = args.results_dir
    if not results_dir.exists() or not results_dir.is_dir():
        raise FileNotFoundError(f"Invalid results directory: {results_dir}")

    shapes_path = args.shapes
    if not shapes_path.exists():
        raise FileNotFoundError(f"SHACL shapes file not found: {shapes_path}")

    shapes_graph = load_graph(shapes_path)
    run_dirs = discover_run_dirs(results_dir)

    if not run_dirs:
        raise ValueError(f"No run folders matching i_i pattern found in {results_dir}")

    non_conformant_count = 0
    validated_count = 0

    for run_dir in run_dirs:
        delta_graph_path = run_dir / "delta_graph.ttl"
        if not delta_graph_path.exists():
            continue

        validated_count += 1
        data_graph = load_graph(delta_graph_path)
        if not is_conformant(data_graph, shapes_graph):
            non_conformant_count += 1

    print(non_conformant_count)


if __name__ == "__main__":
    main()