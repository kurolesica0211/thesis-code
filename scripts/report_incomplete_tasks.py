#!/usr/bin/env python3
"""Report tasks in a results folder that did not complete successfully.

By default this inspects results/royalty_gemini_flash_lite, compares the
scheduled task IDs in trace.jsonl with the task manifests on disk, and reports
any task that is missing its manifest, missing its result artifact, or did not
finish with the expected done_reason.

Usage:
    python scripts/report_incomplete_tasks.py [run_directory]

Example:
    python scripts/report_incomplete_tasks.py results/royalty_gemini_flash_lite
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Tuple


DEFAULT_RUN_DIR = Path("results/royalty_gemini_flash_lite")
EXPECTED_DONE_REASON = "llm_finished"


def _task_sort_key(task_id: str) -> Tuple[int, str]:
    prefix = task_id.split("_", 1)[0]
    try:
        return (int(prefix), task_id)
    except ValueError:
        return (sys.maxsize, task_id)


def _load_trace_entry_ids(run_path: Path) -> List[str]:
    trace_path = run_path / "trace.jsonl"
    if not trace_path.exists():
        return []

    entry_ids: List[str] = []
    with trace_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            if payload.get("event") == "run.entry.start":
                entry_id = payload.get("payload", {}).get("entry_idx")
                if entry_id:
                    entry_ids.append(str(entry_id))

    return entry_ids


def _resolve_result_path(run_path: Path, result_value: str) -> Path:
    result_path = Path(result_value)
    if result_path.is_absolute():
        return result_path

    candidates = [Path.cwd(), run_path] + list(run_path.parents)
    for base_path in candidates:
        candidate = base_path / result_path
        if candidate.exists():
            return candidate

    return Path.cwd() / result_path


def _inspect_task(run_path: Path, task_id: str) -> Tuple[bool, str]:
    task_dir = run_path / task_id
    manifest_path = task_dir / "task_manifest.json"

    if not manifest_path.exists():
        return False, "missing task_manifest.json"

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, f"invalid task_manifest.json: {exc.msg}"

    done_reason = manifest.get("done_reason")
    if done_reason != EXPECTED_DONE_REASON:
        return False, f"done_reason={done_reason!r}"

    result_value = manifest.get("results")
    if not result_value:
        return False, "missing results path in task_manifest.json"

    result_path = _resolve_result_path(run_path, str(result_value))
    if not result_path.exists():
        return False, f"missing result artifact: {result_value}"

    return True, ""


def report_incomplete_tasks(run_dir: str) -> Tuple[int, List[Tuple[str, str]], int]:
    run_path = Path(run_dir)
    if not run_path.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    entry_ids = _load_trace_entry_ids(run_path)
    if not entry_ids:
        entry_ids = [task_dir.name for task_dir in run_path.iterdir() if task_dir.is_dir() and (task_dir / "task_manifest.json").exists()]

    unique_entry_ids = sorted(set(entry_ids), key=_task_sort_key)
    incomplete: List[Tuple[str, str]] = []
    for task_id in unique_entry_ids:
        completed, reason = _inspect_task(run_path, task_id)
        if not completed:
            incomplete.append((task_id, reason))

    completed_count = len(unique_entry_ids) - len(incomplete)
    return len(unique_entry_ids), incomplete, completed_count


def main() -> None:
    run_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RUN_DIR

    try:
        total_tasks, incomplete_tasks, completed_tasks = report_incomplete_tasks(str(run_dir))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Run directory: {run_dir}")
    print(f"Total tasks found: {total_tasks}")
    print(f"Completed successfully: {completed_tasks}")
    print(f"Not completed successfully: {len(incomplete_tasks)}")

    if incomplete_tasks:
        print()
        for task_id, reason in incomplete_tasks:
            print(f"{task_id}: {reason}")
    else:
        print("\nAll tasks completed successfully.")


if __name__ == "__main__":
    main()