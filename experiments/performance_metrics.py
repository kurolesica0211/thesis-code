#!/usr/bin/env python3
"""Calculate performance metrics for a knowledge graph construction run.

The script inspects a run folder that contains task subdirectories with
``task_manifest.json`` files, per-task ``artifacts/usage_metadata.json`` files,
and a run-level ``trace.jsonl`` file. It reports statistics for:

- task processing time, derived from ``run.entry.start`` and ``run.entry.finish``
  events in the trace
- token usage, derived from the task-level usage metadata files

Usage:
	python experiments/performance_metrics.py <run_directory>

Example:
	python experiments/performance_metrics.py results/royalty_gemini_without_shacl
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class TaskMetrics:
	task_id: str
	processing_seconds: Optional[float]
	translation_input_tokens: Optional[int]
	translation_output_tokens: Optional[int]
	final_first_input_tokens: Optional[int]
	final_additional_input_tokens: Optional[int]
	final_input_tokens: Optional[int]
	final_output_tokens: Optional[int]
	iterations: Optional[int]

	@property
	def translation_total_tokens(self) -> Optional[int]:
		if self.translation_input_tokens is None or self.translation_output_tokens is None:
			return None
		return self.translation_input_tokens + self.translation_output_tokens

	@property
	def final_total_tokens(self) -> Optional[int]:
		if self.final_input_tokens is None or self.final_output_tokens is None:
			return None
		return self.final_input_tokens + self.final_output_tokens

	@property
	def final_first_total_tokens(self) -> Optional[int]:
		if self.final_first_input_tokens is None or self.final_output_tokens is None:
			return None
		return self.final_first_input_tokens + self.final_output_tokens

	@property
	def total_tokens(self) -> Optional[int]:
		translation_total = self.translation_total_tokens
		final_total = self.final_total_tokens
		if translation_total is None or final_total is None:
			return None
		return translation_total + final_total


def _task_sort_key(task_id: str) -> Tuple[int, str]:
	prefix = task_id.split("_", 1)[0]
	try:
		return int(prefix), task_id
	except ValueError:
		return sys.maxsize, task_id


def _resolve_relative_path(base_path: Path, value: str) -> Path:
	path_value = Path(value)
	if path_value.is_absolute():
		return path_value

	candidate_bases = [Path.cwd(), base_path] + list(base_path.parents)
	for candidate_base in candidate_bases:
		candidate = candidate_base / path_value
		if candidate.exists():
			return candidate

	return Path.cwd() / path_value


def _parse_timestamp(value: str) -> datetime:
	return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _load_trace_durations(run_path: Path) -> Dict[str, float]:
	trace_path = run_path / "trace.jsonl"
	if not trace_path.exists():
		return {}

	start_times: Dict[str, datetime] = {}
	finish_times: Dict[str, datetime] = {}

	with trace_path.open("r", encoding="utf-8") as handle:
		for line in handle:
			if not line.strip():
				continue

			record = json.loads(line)
			event = record.get("event")
			payload = record.get("payload", {})
			task_id = payload.get("entry_idx") or payload.get("entry_id")
			timestamp = record.get("ts")

			if not task_id or not timestamp:
				continue

			if event == "run.entry.start":
				start_times[str(task_id)] = _parse_timestamp(timestamp)
			elif event == "run.entry.finish":
				finish_times[str(task_id)] = _parse_timestamp(timestamp)

	durations: Dict[str, float] = {}
	for task_id, start_time in start_times.items():
		finish_time = finish_times.get(task_id)
		if finish_time is None:
			continue
		durations[task_id] = (finish_time - start_time).total_seconds()

	return durations


def _load_usage_metadata(task_dir: Path, run_path: Path) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int], Optional[int], Optional[int], Optional[int]]:
	manifest_path = task_dir / "task_manifest.json"
	if not manifest_path.exists():
		return None, None, None, None, None, None, None

	try:
		manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	except json.JSONDecodeError:
		return None, None, None, None, None, None, None

	artifacts_dir_value = manifest.get("artifacts_dir")
	if not artifacts_dir_value:
		return None, None, None, None, None, None, None

	artifacts_dir = _resolve_relative_path(run_path, str(artifacts_dir_value))
	usage_path = artifacts_dir / "usage_metadata.json"
	if not usage_path.exists():
		return None, None, None, None, None, None, None

	usage_metadata = json.loads(usage_path.read_text(encoding="utf-8"))
	iterations = manifest.get("iterations")

	translation_input_tokens = 0
	translation_output_tokens = 0
	final_input_tokens = 0
	final_output_tokens = 0
	final_additional_input_tokens = 0
	final_entries = usage_metadata.get("final", [])
	first_final_entry = final_entries[0] if final_entries else None
	first_final_metadata = first_final_entry.get("metadata", []) if first_final_entry else []
	first_final_input_tokens = int(first_final_metadata[0].get("input_tokens", 0) or 0) if first_final_metadata else 0

	for translation_entry in usage_metadata.get("translation", []):
		metadata = translation_entry.get("metadata", {})
		translation_input_tokens += int(metadata.get("input_tokens", 0) or 0)
		translation_output_tokens += int(metadata.get("output_tokens", 0) or 0)

	for final_entry in final_entries:
		for metadata in final_entry.get("metadata", []):
			input_tokens = int(metadata.get("input_tokens", 0) or 0)
			final_input_tokens += input_tokens
			final_output_tokens += int(metadata.get("output_tokens", 0) or 0)
			# Additional input tokens are measured against the first final prompt.
			final_additional_input_tokens += max(input_tokens - first_final_input_tokens, 0)

	final_first_input_tokens = first_final_input_tokens

	return (
		translation_input_tokens,
		translation_output_tokens,
		final_first_input_tokens,
		final_additional_input_tokens,
		final_input_tokens,
		final_output_tokens,
		int(iterations) if iterations is not None else None,
	)


def _collect_task_metrics(run_dir: str) -> List[TaskMetrics]:
	run_path = Path(run_dir)
	if not run_path.exists():
		raise FileNotFoundError(f"Run directory not found: {run_dir}")

	durations = _load_trace_durations(run_path)
	task_dirs = sorted(
		[task_dir for task_dir in run_path.iterdir() if task_dir.is_dir()],
		key=lambda path: _task_sort_key(path.name),
	)

	task_metrics: List[TaskMetrics] = []
	for task_dir in task_dirs:
		(
			translation_input_tokens,
			translation_output_tokens,
			final_first_input_tokens,
			final_additional_input_tokens,
			final_input_tokens,
			final_output_tokens,
			iterations,
		) = _load_usage_metadata(task_dir, run_path)
		task_metrics.append(
			TaskMetrics(
				task_id=task_dir.name,
				processing_seconds=durations.get(task_dir.name),
				translation_input_tokens=translation_input_tokens,
				translation_output_tokens=translation_output_tokens,
				final_first_input_tokens=final_first_input_tokens,
				final_additional_input_tokens=final_additional_input_tokens,
				final_input_tokens=final_input_tokens,
				final_output_tokens=final_output_tokens,
				iterations=iterations,
			)
		)

	return task_metrics


def _mean(values: List[float]) -> float:
	return statistics.fmean(values) if values else 0.0


def _median(values: List[float]) -> float:
	return statistics.median(values) if values else 0.0


def _stdev(values: List[float]) -> float:
	return statistics.stdev(values) if len(values) > 1 else 0.0


def _percentile(values: List[float], percentile: float) -> float:
	if not values:
		return 0.0

	if percentile <= 0:
		return min(values)
	if percentile >= 100:
		return max(values)

	ordered = sorted(values)
	rank = (len(ordered) - 1) * (percentile / 100.0)
	lower_index = math.floor(rank)
	upper_index = math.ceil(rank)
	lower_value = ordered[lower_index]
	upper_value = ordered[upper_index]
	if lower_index == upper_index:
		return lower_value
	return lower_value + (upper_value - lower_value) * (rank - lower_index)


def _format_seconds(value: float) -> str:
	if value < 60:
		return f"{value:.2f}s"

	minutes, seconds = divmod(value, 60.0)
	if minutes < 60:
		return f"{int(minutes)}m {seconds:.2f}s"

	hours, minutes = divmod(minutes, 60.0)
	return f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"


def _format_int(value: int) -> str:
	return f"{value:,}"


def _print_stat_block(title: str, values: List[float], unit: str) -> None:
	print(title)
	if not values:
		print("  No data found.")
		return

	total = sum(values)
	print(f"  Count:  {len(values):,}")
	if unit == "seconds":
		print(f"  Total:  {_format_seconds(total)}")
		print(f"  Min:    {_format_seconds(min(values))}")
		print(f"  Max:    {_format_seconds(max(values))}")
		print(f"  Mean:   {_format_seconds(_mean(values))}")
		print(f"  Median: {_format_seconds(_median(values))}")
		print(f"  Stddev: {_format_seconds(_stdev(values))}")
		print(f"  P95:    {_format_seconds(_percentile(values, 95.0))}")
	else:
		int_values = [int(value) for value in values]
		print(f"  Total:  {_format_int(int(round(total)))}")
		print(f"  Min:    {_format_int(min(int_values))}")
		print(f"  Max:    {_format_int(max(int_values))}")
		print(f"  Mean:   {_format_int(int(round(_mean(values))))}")
		print(f"  Median: {_format_int(int(round(_median(values))))}")
		print(f"  Stddev: {_format_int(int(round(_stdev(values))))}")
		print(f"  P95:    {_format_int(int(round(_percentile(values, 95.0))))}")


def _print_summary(run_dir: str, task_metrics: List[TaskMetrics], per_task: bool) -> None:
	processing_values = [metric.processing_seconds for metric in task_metrics if metric.processing_seconds is not None]
	translation_input_values = [metric.translation_input_tokens for metric in task_metrics if metric.translation_input_tokens is not None]
	translation_output_values = [metric.translation_output_tokens for metric in task_metrics if metric.translation_output_tokens is not None]
	translation_total_values = [metric.translation_total_tokens for metric in task_metrics if metric.translation_total_tokens is not None]
	final_first_input_values = [metric.final_first_input_tokens for metric in task_metrics if metric.final_first_input_tokens is not None]
	final_additional_input_values = [metric.final_additional_input_tokens for metric in task_metrics if metric.final_additional_input_tokens is not None]
	final_input_values = [metric.final_input_tokens for metric in task_metrics if metric.final_input_tokens is not None]
	final_output_values = [metric.final_output_tokens for metric in task_metrics if metric.final_output_tokens is not None]
	final_total_values = [metric.final_total_tokens for metric in task_metrics if metric.final_total_tokens is not None]
	iteration_values = [metric.iterations for metric in task_metrics if metric.iterations is not None]
	total_token_values = [metric.total_tokens for metric in task_metrics if metric.total_tokens is not None]

	print(f"Run directory: {run_dir}")
	print(f"Tasks discovered: {len(task_metrics):,}")
	print(f"Tasks with timing data: {len(processing_values):,}")
	print(f"Tasks with token data:  {len(total_token_values):,}")
	print()

	_print_stat_block("Processing time statistics", processing_values, "seconds")
	print()

	print("Token usage totals")
	if translation_total_values:
		print(f"  Translation tokens: {_format_int(int(sum(translation_total_values)))}")
		print(f"    Input tokens:     {_format_int(int(sum(translation_input_values)))}")
		print(f"    Output tokens:    {_format_int(int(sum(translation_output_values)))}")
	else:
		print("  Translation tokens: no data")

	if final_total_values:
		print(f"  Final tokens:       {_format_int(int(sum(final_total_values)))}")
		print(f"    First input:      {_format_int(int(sum(final_first_input_values)))}")
		print(f"    Additional input: {_format_int(int(sum(final_additional_input_values)))}")
		print(f"    Total input:      {_format_int(int(sum(final_input_values)))}")
		print(f"    Output tokens:    {_format_int(int(sum(final_output_values)))}")
	else:
		print("  Final tokens:       no data")

	if iteration_values:
		print(f"  Median iterations: {_median([float(value) for value in iteration_values]):.2f}")
	else:
		print("  Average iterations: no data")

	if total_token_values:
		print(f"  All tokens:         {_format_int(int(sum(total_token_values)))}")
	else:
		print("  All tokens:         no data")

	print()
	_print_stat_block("Translation token statistics per task", [float(value) for value in translation_total_values], "tokens")
	print()
	_print_stat_block("Final token statistics per task", [float(value) for value in final_total_values], "tokens")
	print()
	_print_stat_block("Final first-input token statistics per task", [float(value) for value in final_first_input_values], "tokens")
	print()
	_print_stat_block("Final additional-input token statistics per task", [float(value) for value in final_additional_input_values], "tokens")
	print()
	_print_stat_block("Iteration statistics per task", [float(value) for value in iteration_values], "iterations")

	if per_task:
		print()
		print("Per-task breakdown")
		for metric in sorted(task_metrics, key=lambda item: _task_sort_key(item.task_id)):
			time_text = _format_seconds(metric.processing_seconds) if metric.processing_seconds is not None else "n/a"
			translation_input_text = _format_int(metric.translation_input_tokens) if metric.translation_input_tokens is not None else "n/a"
			translation_output_text = _format_int(metric.translation_output_tokens) if metric.translation_output_tokens is not None else "n/a"
			translation_total_text = _format_int(metric.translation_total_tokens) if metric.translation_total_tokens is not None else "n/a"
			final_first_input_text = _format_int(metric.final_first_input_tokens) if metric.final_first_input_tokens is not None else "n/a"
			final_additional_input_text = _format_int(metric.final_additional_input_tokens) if metric.final_additional_input_tokens is not None else "n/a"
			final_input_text = _format_int(metric.final_input_tokens) if metric.final_input_tokens is not None else "n/a"
			final_output_text = _format_int(metric.final_output_tokens) if metric.final_output_tokens is not None else "n/a"
			final_total_text = _format_int(metric.final_total_tokens) if metric.final_total_tokens is not None else "n/a"
			iteration_text = _format_int(metric.iterations) if metric.iterations is not None else "n/a"
			total_text = _format_int(metric.total_tokens) if metric.total_tokens is not None else "n/a"
			print(
				f"  {metric.task_id}: time={time_text}, "
				f"translation(input={translation_input_text}, output={translation_output_text}, total={translation_total_text}), "
				f"final(first_input={final_first_input_text}, additional_input={final_additional_input_text}, input={final_input_text}, output={final_output_text}, total={final_total_text}), "
				f"iterations={iteration_text}, "
				f"all={total_text}"
			)


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Calculate processing-time and token-usage statistics for a KG construction run."
	)
	parser.add_argument("run_directory", help="Path to the run directory")
	parser.add_argument(
		"--per-task",
		action="store_true",
		help="Print a per-task breakdown in addition to the summary statistics.",
	)
	args = parser.parse_args()

	try:
		task_metrics = _collect_task_metrics(args.run_directory)
	except (FileNotFoundError, json.JSONDecodeError) as exc:
		print(f"Error: {exc}", file=sys.stderr)
		sys.exit(1)

	_print_summary(args.run_directory, task_metrics, args.per_task)


if __name__ == "__main__":
	main()
