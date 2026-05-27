#!/usr/bin/env python3
"""Group SHACL violations by source constraint component.

The script scans a run directory for per-task ``artifacts/graphs.json`` files,
extracts validation graphs, and counts all SHACL violations by
``sh:sourceConstraintComponent``.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Counter as CounterType, Dict, Iterable

from rdflib import Graph, Namespace


SOURCE_CONSTRAINT_PATTERN = re.compile(r"sh:sourceConstraintComponent\s+sh:([A-Za-z0-9_]+)")
SH = Namespace("http://www.w3.org/ns/shacl#")


def _iter_graph_records(run_path: Path) -> Iterable[Dict[str, object]]:
	for graphs_path in sorted(run_path.rglob("artifacts/graphs.json")):
		try:
			records = json.loads(graphs_path.read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError):
			continue

		if not isinstance(records, list):
			continue

		for record in records:
			if isinstance(record, dict):
				yield record


def collect_source_constraint_component_counts(run_directory: str) -> CounterType[str]:
	run_path = Path(run_directory)
	if not run_path.exists():
		raise FileNotFoundError(f"Run directory not found: {run_directory}")

	counts: CounterType[str] = Counter()
	for record in _iter_graph_records(run_path):
		if record.get("graph_type") != "validation_graph":
			continue

		graph_text = record.get("graph")
		if not isinstance(graph_text, str):
			continue

		for component_name in SOURCE_CONSTRAINT_PATTERN.findall(graph_text):
			counts[component_name] += 1

	return counts


def collect_class_constraint_messages(run_directory: str) -> CounterType[str]:
	run_path = Path(run_directory)
	if not run_path.exists():
		raise FileNotFoundError(f"Run directory not found: {run_directory}")

	message_counts: CounterType[str] = Counter()
	for record in _iter_graph_records(run_path):
		if record.get("graph_type") != "validation_graph":
			continue

		graph_text = record.get("graph")
		if not isinstance(graph_text, str):
			continue

		graph = Graph()
		try:
			graph.parse(data=graph_text, format="turtle")
		except Exception:
			continue

		for result_node in graph.subjects(SH.sourceConstraintComponent, SH.ClassConstraintComponent):
			message = graph.value(result_node, SH.resultMessage)
			if message is None:
				continue
			message_counts[str(message)] += 1

	return message_counts


def collect_non_class_constraint_messages(run_directory: str) -> CounterType[str]:
	run_path = Path(run_directory)
	if not run_path.exists():
		raise FileNotFoundError(f"Run directory not found: {run_directory}")

	message_counts: CounterType[str] = Counter()
	for record in _iter_graph_records(run_path):
		if record.get("graph_type") != "validation_graph":
			continue

		graph_text = record.get("graph")
		if not isinstance(graph_text, str):
			continue

		graph = Graph()
		try:
			graph.parse(data=graph_text, format="turtle")
		except Exception:
			continue

		for result_node in graph.subjects(SH.resultSeverity, SH.Violation):
			component = graph.value(result_node, SH.sourceConstraintComponent)
			if component == SH.ClassConstraintComponent:
				continue

			message = graph.value(result_node, SH.resultMessage)
			if message is None:
				continue
			message_counts[str(message)] += 1

	return message_counts


def reorganize_non_class_violations(message_counts: CounterType[str]) -> CounterType[str]:
	"""Reorganize non-class constraint messages for cleaner grouping.
	
	- Merges all "is closed" violations into a single label.
	- Groups "more than ... values on" violations by the property name.
	- Keeps other violations as-is.
	"""
	reorganized: CounterType[str] = Counter()
	
	closed_count = 0
	more_than_pattern = re.compile(r"More than .* values on .+->(:[\w]+)")
	
	for message, count in message_counts.items():
		if "is closed" in message.lower():
			closed_count += count
		else:
			match = more_than_pattern.search(message)
			if match:
				property_name = match.group(1)
				label = f"More than 1 values on {property_name}"
				reorganized[label] += count
			else:
				reorganized[message] += count
	
	if closed_count > 0:
		reorganized["Node is closed"] = closed_count
	
	return reorganized


def collect_non_class_violations_by_task(run_directory: str) -> dict[str, set[str]]:
	"""Collect non-class constraint violations grouped by message type and their source tasks.
	
	Returns a dict mapping message strings to sets of task names where that message occurs.
	"""
	violations_by_message: dict[str, set[str]] = {}
	run_path = Path(run_directory)
	
	for graphs_path in sorted(run_path.rglob("artifacts/graphs.json")):
		# Extract task name from path like: .../task_name/artifacts/graphs.json
		task_name = graphs_path.parent.parent.name
		
		try:
			records = json.loads(graphs_path.read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError):
			continue
		
		if not isinstance(records, list):
			continue
		
		for record in records:
			if not isinstance(record, dict):
				continue
			
			if record.get("graph_type") != "validation_graph":
				continue
			
			graph_text = record.get("graph")
			if not isinstance(graph_text, str):
				continue
			
			# Parse the TTL string into an RDF graph
			try:
				graph = Graph()
				graph.parse(data=graph_text, format="turtle")
			except Exception:
				continue
			
			# Get all violation subjects that are not ClassConstraintComponent
			for result_node in graph.subjects(SH.resultSeverity, SH.Violation):
				component = graph.value(result_node, SH.sourceConstraintComponent)
				
				# Skip ClassConstraintComponent violations
				if component == SH.ClassConstraintComponent:
					continue
				
				message = graph.value(result_node, SH.resultMessage)
				if message:
					message_str = str(message)
					if message_str not in violations_by_message:
						violations_by_message[message_str] = set()
					violations_by_message[message_str].add(task_name)
	
	return violations_by_message


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Group SHACL violations by sourceConstraintComponent for a KG construction run."
	)
	parser.add_argument("run_directory", help="Path to the run directory")
	args = parser.parse_args()

	counts = collect_source_constraint_component_counts(args.run_directory)
	if not counts:
		print("No SHACL violations found.")
		return

	for component_name, count in counts.most_common():
		print(f"{component_name}: {count}")


if __name__ == "__main__":
	main()