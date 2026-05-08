#!/usr/bin/env python3
"""Merge per-task delta graphs into a single graph for a run directory.

By default this scans results/royalty_gemini_flash_lite, loads each task
folder's delta_graph.ttl, merges them into one graph, and writes the result to
merged_graph.ttl in the run directory.

Usage:
    python scripts/merge_delta_graphs.py [run_directory] [--output merged_graph.ttl]

Example:
    python scripts/merge_delta_graphs.py results/royalty_gemini_flash_lite
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

from rdflib import Graph


DEFAULT_RUN_DIR = Path("results/royalty_gemini_flash_lite")
DEFAULT_OUTPUT_NAME = "merged_graph.ttl"


def _task_sort_key(task_dir: Path) -> Tuple[int, str]:
    prefix = task_dir.name.split("_", 1)[0]
    try:
        return (int(prefix), task_dir.name)
    except ValueError:
        return (sys.maxsize, task_dir.name)


def _load_delta_graph(task_dir: Path) -> Graph | None:
    delta_graph_path = task_dir / "delta_graph.ttl"
    if not delta_graph_path.exists():
        print(f"Warning: delta_graph.ttl not found at {delta_graph_path}", file=sys.stderr)
        return None

    graph = Graph()
    graph.parse(delta_graph_path.as_posix(), format="turtle")
    return graph


def merge_delta_graphs(run_dir: str, output_name: str = DEFAULT_OUTPUT_NAME) -> Tuple[Path, int, int]:
    run_path = Path(run_dir)
    if not run_path.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    task_dirs = sorted(
        [task_dir for task_dir in run_path.iterdir() if task_dir.is_dir()],
        key=_task_sort_key,
    )

    merged_graph: Graph | None = None
    namespace_source: Graph | None = None
    loaded_graphs = 0
    skipped_graphs = 0

    for task_dir in task_dirs:
        delta_graph = _load_delta_graph(task_dir)
        if delta_graph is None:
            skipped_graphs += 1
            continue

        if merged_graph is None:
            merged_graph = delta_graph
            namespace_source = delta_graph
        else:
            merged_graph = merged_graph + delta_graph
        loaded_graphs += 1

    if merged_graph is None:
        merged_graph = Graph()

    merged_graph_path = run_path / output_name
    if namespace_source is not None:
        merged_graph.namespace_manager = namespace_source.namespace_manager
    merged_graph.serialize(format="turtle", destination=merged_graph_path.as_posix())

    return merged_graph_path, loaded_graphs, skipped_graphs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge delta_graph.ttl files from each task folder into one graph."
    )
    parser.add_argument(
        "run_directory",
        nargs="?",
        default=str(DEFAULT_RUN_DIR),
        help="Path to the run directory",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_NAME,
        help=f"Output file name inside the run directory (default: {DEFAULT_OUTPUT_NAME})",
    )
    args = parser.parse_args()

    try:
        merged_graph_path, loaded_graphs, skipped_graphs = merge_delta_graphs(args.run_directory, args.output)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote merged graph to {merged_graph_path}")
    print(f"Loaded delta graphs: {loaded_graphs}")
    if skipped_graphs:
        print(f"Skipped task folders without delta_graph.ttl: {skipped_graphs}")


if __name__ == "__main__":
    main()