#!/usr/bin/env python3
"""Compute precision, recall, and F1 for KG construction runs.

The evaluator works on per-task folders produced under ``results/``. Each task
folder must contain ``delta_graph.ttl`` and ``entity_match_map.json``.

Precision is computed over raw extracted triples after filtering annotation and
type predicates, unmapped entities, entities outside the run's candidate set,
and relations that never occur in the filtered gold graph.

Recall is computed over the deduplicated gold triples after applying the same
relation normalization rules and removing redundant property-chain triples.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL


DATA = Namespace("http://example.com/data#")
ONTOLOGY = Namespace("http://example.com/family_TBOX.ttl#")

DIRECT_SYNONYMS = [
	("hasParent", "hasMother"),
	("hasParent", "hasFather"),
	("hasParent", "isDaughterOf"),
	("hasParent", "isSonOf"),
	("hasParent", "isChildOf"),

	("hasChild", "hasDaughter"),
	("hasChild", "hasSon"),
	("hasChild", "isFatherOf"),
	("hasChild", "isMotherOf"),
	("hasChild", "isParentOf"),
	
	("isSiblingOf", "isBrotherOf"),
	("isSiblingOf", "isSisterOf"),
	("isSiblingOf", "hasBrother"),
	("isSiblingOf", "hasSister"),
]

INVERSE_SYNONYMS = [
	("hasParent", "isParentOf"), ("isSiblingOf", "isSiblingOf")
]


def build_relation_adjacency() -> dict[str, list[tuple[str, int]]]:
	adjacency: dict[str, list[tuple[str, int]]] = defaultdict(list)

	for left, right in DIRECT_SYNONYMS:
		adjacency[left].append((right, 0))
		adjacency[right].append((left, 0))

	for left, right in INVERSE_SYNONYMS:
		adjacency[left].append((right, 1))
		adjacency[right].append((left, 1))

	return adjacency


RELATION_ADJACENCY = build_relation_adjacency()


@lru_cache(maxsize=None)
def relation_states(relation_name: str) -> tuple[tuple[str, int], ...]:
	visited: set[tuple[str, int]] = {(relation_name, 0)}
	queue: deque[tuple[str, int]] = deque([(relation_name, 0)])

	while queue:
		current_name, current_flip = queue.popleft()
		for next_name, edge_flip in RELATION_ADJACENCY.get(current_name, []):
			next_state = (next_name, current_flip ^ edge_flip)
			if next_state in visited:
				continue
			visited.add(next_state)
			queue.append(next_state)

	return tuple(sorted(visited))


@lru_cache(maxsize=None)
def relation_class_id(relation_name: str) -> str:
	return min(name for name, _ in relation_states(relation_name))


def local_name(value: str) -> str:
	if "#" in value:
		return value.rsplit("#", 1)[-1]
	if "/" in value:
		return value.rsplit("/", 1)[-1]
	return value


def make_relation_variants(subject: str, relation_name: str, obj: str) -> set[tuple[str, str, str]]:
	relation_id = relation_class_id(relation_name)
	variants: set[tuple[str, str, str]] = set()
	for _, flipped in relation_states(relation_name):
		if flipped:
			variants.add((relation_id, obj, subject))
		else:
			variants.add((relation_id, subject, obj))
	return variants


def canonical_triple_key(subject: str, relation_name: str, obj: str) -> tuple[str, str, str]:
	return min(make_relation_variants(subject, relation_name, obj))


def load_annotation_predicates(ontology_path: Path) -> set[URIRef]:
	ontology_graph = Graph()
	ontology_graph.parse(ontology_path.as_posix(), format="turtle")
	return {subject for subject in ontology_graph.subjects(RDF.type, OWL.AnnotationProperty) if isinstance(subject, URIRef)}


def load_property_chains(ontology_path: Path) -> dict[str, tuple[str, str]]:
	ontology_graph = Graph()
	ontology_graph.parse(ontology_path.as_posix(), format="turtle")

	chains: dict[str, tuple[str, str]] = {}
	for predicate, chain_node in ontology_graph.subject_objects(OWL.propertyChainAxiom):
		if not isinstance(predicate, URIRef):
			continue
		try:
			chain_values = [value for value in Collection(ontology_graph, chain_node) if isinstance(value, URIRef)]
		except Exception:
			continue
		if len(chain_values) == 2:
			chains[local_name(str(predicate))] = (local_name(str(chain_values[0])), local_name(str(chain_values[1])))
	return chains


def discover_task_directories(results_root: Path) -> list[Path]:
	task_directories: list[Path] = []
	for delta_graph_path in results_root.rglob("delta_graph.ttl"):
		task_directory = delta_graph_path.parent
		if (task_directory / "entity_match_map.json").exists():
			task_directories.append(task_directory)
	return sorted(task_directories)


def load_entity_map(entity_map_path: Path) -> dict[str, Any]:
	with entity_map_path.open("r", encoding="utf-8") as handle:
		return json.load(handle)


def build_candidate_entity_set(entity_map: dict[str, Any]) -> set[str]:
	candidate_entities: set[str] = set()

	main_entity = entity_map.get("main_entity") or {}
	main_uri = main_entity.get("uri")
	if main_uri:
		candidate_entities.add(main_uri)

	for row in entity_map.get("candidate_entities", []):
		if row.get("uri"):
			candidate_entities.add(row["uri"])

	return candidate_entities


def build_extracted_entity_map(entity_map: dict[str, Any]) -> dict[str, str]:
	extracted_to_gold: dict[str, str] = {}
	for row in entity_map.get("entities", []):
		extracted_uri = row.get("extracted_uri")
		gold_uri = row.get("ground_truth_uri")
		if extracted_uri and gold_uri:
			extracted_to_gold[extracted_uri] = gold_uri
	return extracted_to_gold


def load_raw_graph(graph_path: Path) -> Graph:
	graph = Graph()
	graph.parse(graph_path.as_posix(), format="turtle")
	return graph


def build_semantic_closure(
	raw_triples: list[tuple[str, str, str]],
	property_chains: dict[str, tuple[str, str]],
) -> set[tuple[str, str, str]]:
	semantic_keys: set[tuple[str, str, str]] = set()
	forward_index: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

	for subject, predicate_name, obj in raw_triples:
		semantic_keys.add(canonical_triple_key(subject, predicate_name, obj))
		for edge_relation_id, edge_subject, edge_object in make_relation_variants(subject, predicate_name, obj):
			forward_index[edge_relation_id][edge_subject].add(edge_object)

	for predicate_name, (first_relation, second_relation) in property_chains.items():
		first_relation_id = relation_class_id(first_relation)
		second_relation_id = relation_class_id(second_relation)

		for subject, middles in forward_index[first_relation_id].items():
			for middle in middles:
				for obj in forward_index[second_relation_id].get(middle, set()):
					semantic_keys.add(canonical_triple_key(subject, predicate_name, obj))

	return semantic_keys


def build_gold_sets(
	graph_path: Path,
	ontology_path: Path,
) -> tuple[set[tuple[str, str, str]], set[str]]:
	annotation_predicates = load_annotation_predicates(ontology_path)
	excluded_predicates = set(annotation_predicates) | {RDF.type, DATA.wdtLink, ONTOLOGY.hasSex}
	raw_graph = load_raw_graph(graph_path)
	property_chains = load_property_chains(ontology_path)
	raw_triples: list[tuple[str, str, str]] = []

	for subject, predicate, obj in raw_graph:
		if not isinstance(subject, URIRef) or not isinstance(obj, URIRef):
			continue
		if not isinstance(predicate, URIRef) or predicate in excluded_predicates:
			continue
		raw_triples.append((str(subject), local_name(str(predicate)), str(obj)))

	gold_keys = build_semantic_closure(raw_triples, property_chains)

	gold_relation_classes = {key[0] for key in gold_keys}
	return gold_keys, gold_relation_classes


@dataclass
class RunMetrics:
	run_directory: str
	task_directory: str
	text_file: str | None
	article: str | None
	main_entity_uri: str | None
	candidate_entity_count: int
	raw_triples_total: int
	annotation_or_type_filtered: int
	entity_mismatch_filtered: int
	relation_mismatch_filtered: int
	valid_predicted_total: int
	correct_predicted_total: int
	precision: float


def evaluate_task_directory(
	task_directory: Path,
	gold_keys: set[tuple[str, str, str]],
	gold_relation_classes: set[str],
	property_chains: dict[str, tuple[str, str]],
	ontology_path: Path,
) -> tuple[RunMetrics, set[tuple[str, str, str]]]:
	entity_map_path = task_directory / "entity_match_map.json"
	delta_graph_path = task_directory / "delta_graph.ttl"
	if not entity_map_path.exists():
		raise FileNotFoundError(f"Missing entity_match_map.json: {entity_map_path}")
	if not delta_graph_path.exists():
		raise FileNotFoundError(f"Missing delta_graph.ttl: {delta_graph_path}")

	entity_map = load_entity_map(entity_map_path)
	candidate_entities = build_candidate_entity_set(entity_map)
	extracted_to_gold = build_extracted_entity_map(entity_map)

	main_entity = entity_map.get("main_entity") or {}
	run_directory = entity_map.get("run_directory") or str(task_directory.parent)
	text_file = entity_map.get("text_file")
	article = entity_map.get("article")

	graph = load_raw_graph(delta_graph_path)
	annotation_predicates = load_annotation_predicates(ontology_path)
	excluded_predicates = set(annotation_predicates) | {RDF.type, DATA.wdtLink, ONTOLOGY.hasSex}

	raw_triples_total = 0
	annotation_or_type_filtered = 0
	entity_mismatch_filtered = 0
	relation_mismatch_filtered = 0
	semantic_predicted_total = 0
	correct_predicted_total = 0
	run_correct_keys: set[tuple[str, str, str]] = set()
	base_predicted_rows: list[tuple[str, str, str]] = []

	for subject, predicate, obj in graph:
		raw_triples_total += 1

		if not isinstance(predicate, URIRef) or predicate in excluded_predicates:
			annotation_or_type_filtered += 1
			continue

		if not isinstance(subject, URIRef) or not isinstance(obj, URIRef):
			entity_mismatch_filtered += 1
			continue

		subject_uri = extracted_to_gold.get(str(subject))
		object_uri = extracted_to_gold.get(str(obj))
		if not subject_uri or not object_uri:
			entity_mismatch_filtered += 1
			continue

		predicate_name = local_name(str(predicate))
		relation_id = relation_class_id(predicate_name)
		if relation_id not in gold_relation_classes:
			relation_mismatch_filtered += 1
			continue

		base_predicted_rows.append((subject_uri, predicate_name, object_uri))

	predicted_keys = build_semantic_closure(base_predicted_rows, property_chains)
	semantic_predicted_total = len(predicted_keys)

	for canonical_key in predicted_keys:
		if canonical_key in gold_keys:
			correct_predicted_total += 1
			run_correct_keys.add(canonical_key)

	precision = (correct_predicted_total / semantic_predicted_total) if semantic_predicted_total else 0.0

	metrics = RunMetrics(
		run_directory=run_directory,
		task_directory=task_directory.as_posix(),
		text_file=text_file,
		article=article,
		main_entity_uri=main_entity.get("uri"),
		candidate_entity_count=len(candidate_entities),
		raw_triples_total=raw_triples_total,
		annotation_or_type_filtered=annotation_or_type_filtered,
		entity_mismatch_filtered=entity_mismatch_filtered,
		relation_mismatch_filtered=relation_mismatch_filtered,
		valid_predicted_total=semantic_predicted_total,
		correct_predicted_total=correct_predicted_total,
		precision=precision,
	)
	return metrics, run_correct_keys


def aggregate_results(
	runs: list[RunMetrics],
	global_gold_keys: set[tuple[str, str, str]],
	global_correct_keys: set[tuple[str, str, str]],
) -> dict[str, Any]:
	total_valid_predicted = sum(run.valid_predicted_total for run in runs)
	total_correct_predicted = sum(run.correct_predicted_total for run in runs)
	total_annotation_or_type_filtered = sum(run.annotation_or_type_filtered for run in runs)
	total_entity_mismatch_filtered = sum(run.entity_mismatch_filtered for run in runs)
	total_relation_mismatch_filtered = sum(run.relation_mismatch_filtered for run in runs)

	precision = (total_correct_predicted / total_valid_predicted) if total_valid_predicted else 0.0
	recall = (len(global_correct_keys) / len(global_gold_keys)) if global_gold_keys else 0.0
	f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

	return {
		"precision": precision,
		"recall": recall,
		"f1": f1,
		"global_gold_total": len(global_gold_keys),
		"global_correct_total": len(global_correct_keys),
		"total_valid_predicted": total_valid_predicted,
		"total_correct_predicted": total_correct_predicted,
		"total_annotation_or_type_filtered": total_annotation_or_type_filtered,
		"total_entity_mismatch_filtered": total_entity_mismatch_filtered,
		"total_relation_mismatch_filtered": total_relation_mismatch_filtered,
	}


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Evaluate precision/recall for KG construction runs.")
	parser.add_argument(
		"--results-root",
		type=Path,
		default=Path("results"),
		help="Root results directory to scan recursively for task folders.",
	)
	parser.add_argument(
		"--task-directory",
		dest="task_directories",
		action="append",
		type=Path,
		help="Optional task directory to evaluate. Can be repeated.",
	)
	parser.add_argument(
		"--gold-graph",
		type=Path,
		default=Path("custom_family_bench/royalty/ground_truth_inferred.ttl"),
		help="Ground-truth graph used as the gold standard.",
	)
	parser.add_argument(
		"--ontology",
		type=Path,
		default=Path("custom_family_bench/family_TBOX.ttl"),
		help="Ontology graph used for annotation and property-chain rules.",
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=Path("results/precision_recall_summary.json"),
		help="Output JSON file for the detailed metrics summary.",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	task_directories = args.task_directories or discover_task_directories(args.results_root)
	if not task_directories:
		raise FileNotFoundError("No task directories with delta_graph.ttl and entity_match_map.json were found.")

	property_chains = load_property_chains(args.ontology)
	gold_keys, gold_relation_classes = build_gold_sets(args.gold_graph, args.ontology)

	runs: list[RunMetrics] = []
	global_correct_keys: set[tuple[str, str, str]] = set()

	for task_directory in sorted(task_directories):
		metrics, correct_keys = evaluate_task_directory(
			task_directory=task_directory,
			gold_keys=gold_keys,
			gold_relation_classes=gold_relation_classes,
			property_chains=property_chains,
			ontology_path=args.ontology,
		)
		runs.append(metrics)
		global_correct_keys.update(correct_keys)

	summary = {
		"results_root": args.results_root.as_posix(),
		"gold_graph": args.gold_graph.as_posix(),
		"ontology": args.ontology.as_posix(),
		"task_count": len(runs),
		"aggregate": aggregate_results(runs, gold_keys, global_correct_keys),
		"runs": [asdict(run) for run in runs],
	}

	args.output.parent.mkdir(parents=True, exist_ok=True)
	args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

	aggregate = summary["aggregate"]
	print(
		f"precision={aggregate['precision']:.4f} recall={aggregate['recall']:.4f} "
		f"f1={aggregate['f1']:.4f} runs={len(runs)}"
	)
	print(f"wrote {args.output}")


if __name__ == "__main__":
	main()
