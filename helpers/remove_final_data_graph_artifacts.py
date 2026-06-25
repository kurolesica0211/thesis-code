#!/usr/bin/env python3
"""Remove duplicated final_data_graph artifacts from main results folders.

By default, this script scans these roots recursively:
- results/royalty_gemini_with_shacl
- results/royalty_gemini_without_shacl

It removes files named:
- final_data_graph.ttl
- final_data_graph*_inferred*.ttl (matched via final_data_graph*.ttl)

Usage:
    python helpers/remove_final_data_graph_artifacts.py
    python helpers/remove_final_data_graph_artifacts.py --dry-run
    python helpers/remove_final_data_graph_artifacts.py --roots results/foo results/bar
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable


DEFAULT_ROOTS = [
    Path("results/royalty_gemini_with_shacl"),
    Path("results/royalty_gemini_without_shacl"),
]
TARGET_GLOB = "final_data_graph*.ttl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove final_data_graph artifacts recursively from result folders."
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        type=Path,
        default=DEFAULT_ROOTS,
        help=(
            "Root folders to scan recursively. "
            "Defaults to results/royalty_gemini_with_shacl and results/royalty_gemini_without_shacl."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be removed without deleting them.",
    )
    return parser.parse_args()


def collect_targets(roots: Iterable[Path]) -> tuple[list[Path], list[Path]]:
    existing_roots: list[Path] = []
    missing_roots: list[Path] = []
    for root in roots:
        if root.exists() and root.is_dir():
            existing_roots.append(root)
        else:
            missing_roots.append(root)

    targets: list[Path] = []
    for root in existing_roots:
        for candidate in root.rglob(TARGET_GLOB):
            if candidate.is_file():
                targets.append(candidate)

    # Deduplicate and keep deterministic ordering.
    targets = sorted(set(targets))
    return targets, missing_roots


def main() -> None:
    args = parse_args()
    targets, missing_roots = collect_targets(args.roots)

    if missing_roots:
        print("Warning: some root directories do not exist and were skipped:")
        for root in missing_roots:
            print(f"- {root}")
        print()

    if not targets:
        print("No matching files found.")
        return

    if args.dry_run:
        print(f"Dry run: {len(targets)} file(s) would be removed:")
        for path in targets:
            print(f"- {path}")
        return

    removed = 0
    failed = 0
    for path in targets:
        try:
            path.unlink()
            removed += 1
            print(f"Removed: {path}")
        except OSError as exc:
            failed += 1
            print(f"Failed to remove {path}: {exc}", file=sys.stderr)

    print()
    print(f"Removed: {removed}")
    print(f"Failed: {failed}")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
