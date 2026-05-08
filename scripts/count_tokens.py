#!/usr/bin/env python3
"""
Count total input and output tokens across all tasks in a run directory.

Usage:
    python scripts/count_tokens.py <run_directory> [--per-task]

Example:
    python scripts/count_tokens.py results/habsburgs_gemini-flash-lite-latest
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Tuple


def count_tokens_in_run(run_dir: str) -> Tuple[int, int, Dict]:
    """
    Count total input and output tokens across all tasks in a run directory.
    
    Args:
        run_dir: Path to the run directory
        
    Returns:
        Tuple of (total_input_tokens, total_output_tokens, detailed_breakdown)
    """
    run_path = Path(run_dir)
    
    if not run_path.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    total_input_tokens = 0
    total_output_tokens = 0
    breakdown = {}

    task_dirs = sorted(
        [task_dir for task_dir in run_path.iterdir() if task_dir.is_dir()],
        key=lambda path: path.name,
    )

    for task_dir in task_dirs:
        task_manifest_full_path = task_dir / "task_manifest.json"
        if not task_manifest_full_path.exists():
            print(f"Warning: task_manifest.json not found at {task_manifest_full_path}", file=sys.stderr)
            continue

        with open(task_manifest_full_path, "r", encoding="utf-8") as f:
            task_manifest = json.load(f)

        entry_id = task_manifest.get("entry_id", "unknown")
        artifacts_dir = task_manifest.get("artifacts_dir")
        
        if not artifacts_dir:
            print(f"Warning: artifacts_dir not found in {task_manifest_full_path}", file=sys.stderr)
            continue

        usage_metadata_path = Path(artifacts_dir)
        if not usage_metadata_path.is_absolute():
            usage_metadata_path = Path.cwd() / usage_metadata_path
        usage_metadata_path = usage_metadata_path / "usage_metadata.json"
        
        if not usage_metadata_path.exists():
            print(f"Warning: usage_metadata.json not found at {usage_metadata_path}", file=sys.stderr)
            continue
        
        with open(usage_metadata_path, "r", encoding="utf-8") as f:
            usage_metadata = json.load(f)
        
        entry_input_tokens = 0
        entry_output_tokens = 0
        
        # Process translation metadata
        for trans_entry in usage_metadata.get("translation", []):
            metadata = trans_entry.get("metadata", {})
            entry_input_tokens += metadata.get("input_tokens", 0)
            entry_output_tokens += metadata.get("output_tokens", 0)
        
        # Process final metadata (list of metadata from all messages)
        for final_entry in usage_metadata.get("final", []):
            metadata_list = final_entry.get("metadata", [])
            for metadata in metadata_list:
                entry_input_tokens += metadata.get("input_tokens", 0)
                entry_output_tokens += metadata.get("output_tokens", 0)
        
        total_input_tokens += entry_input_tokens
        total_output_tokens += entry_output_tokens
        
        breakdown[entry_id] = {
            "input_tokens": entry_input_tokens,
            "output_tokens": entry_output_tokens,
            "total_tokens": entry_input_tokens + entry_output_tokens,
        }
    
    return total_input_tokens, total_output_tokens, breakdown


def main():
    parser = argparse.ArgumentParser(
        description="Count total input and output tokens across all tasks in a run directory."
    )
    parser.add_argument("run_directory", help="Path to the run directory")
    parser.add_argument(
        "--per-task",
        action="store_true",
        help="Print the per-task token breakdown",
    )
    args = parser.parse_args()

    run_dir = args.run_directory
    
    try:
        input_tokens, output_tokens, breakdown = count_tokens_in_run(run_dir)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n=== Token Count Summary for {run_dir} ===\n")
    print(f"Total Input Tokens:  {input_tokens:,}")
    print(f"Total Output Tokens: {output_tokens:,}")
    print(f"Total Tokens:        {input_tokens + output_tokens:,}\n")
    
    if args.per_task and breakdown:
        print("=== Per-Task Breakdown ===\n")
        for entry_id in sorted(breakdown.keys()):
            stats = breakdown[entry_id]
            print(f"{entry_id}:")
            print(f"  Input:  {stats['input_tokens']:,}")
            print(f"  Output: {stats['output_tokens']:,}")
            print(f"  Total:  {stats['total_tokens']:,}")
    
    print()


if __name__ == "__main__":
    main()
