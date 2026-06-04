from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import mean


OBJECT_PROPERTY_EXCLUDED_RANGES = {
	"string",
	"number",
	"integer",
	"float",
	"double",
	"decimal",
	"date",
	"Date",
	"year",
	"Year",
	"boolean",
	"Boolean",
	"time",
	"Time",
	"gYear",
	"gMonth",
	"gDay",
	"anyURI",
	"uri",
	"URL",
	"duration",
	"literal",
	"Literal",
}


def _count_sentences(text: str) -> int:
	normalized = re.sub(r"\s+", " ", text.strip())
	if not normalized:
		return 0
	parts = [part.strip() for part in re.findall(r"[^.!?]+(?:[.!?]+(?=\s|$)|$)", normalized) if part.strip()]
	return len(parts)


def _repo_root() -> Path:
	return Path(__file__).resolve().parent.parent.parent


def _dataset_root() -> Path:
	return _repo_root() / "experiments" / "text2kg"


def _ground_truth_dirs() -> list[Path]:
	root = _dataset_root()
	return [
		root / "cenguix Text2KGBench main data-dbpedia_webnlg_ground_truth",
		root / "cenguix Text2KGBench main data-wikidata_tekgen_ground_truth",
	]


def _ontology_dirs() -> list[Path]:
	root = _dataset_root()
	return [
		root / "cenguix Text2KGBench main data-dbpedia_webnlg_ontologies",
		root / "cenguix Text2KGBench main data-wikidata_tekgen_ontologies",
	]


def _iter_jsonl_entries(jsonl_path: Path) -> list[dict]:
	entries: list[dict] = []
	with jsonl_path.open("r", encoding="utf-8") as handle:
		for line in handle:
			line = line.strip()
			if line:
				entries.append(json.loads(line))
	return entries


def _collect_entries(ground_truth_dirs: list[Path]) -> list[dict]:
	entries: list[dict] = []
	for ground_truth_dir in ground_truth_dirs:
		for jsonl_path in sorted(ground_truth_dir.glob("*.jsonl")):
			entries.extend(_iter_jsonl_entries(jsonl_path))
	return entries


def _count_concepts(ontology: dict) -> int:
	return len(ontology.get("concepts", []))


def _count_object_properties(ontology: dict) -> int:
	count = 0
	for relation in ontology.get("relations", []):
		range_name = str(relation.get("range", "")).strip()
		if range_name not in OBJECT_PROPERTY_EXCLUDED_RANGES:
			count += 1
	return count


def _collect_tbox_counts(ontology_dirs: list[Path]) -> tuple[int, int, int]:
	class_total = 0
	object_property_total = 0
	file_count = 0
	for ontology_dir in ontology_dirs:
		for json_path in sorted(ontology_dir.glob("*.json")):
			ontology = json.loads(json_path.read_text(encoding="utf-8"))
			class_total += _count_concepts(ontology)
			object_property_total += _count_object_properties(ontology)
			file_count += 1
	return class_total, object_property_total, file_count


def characterize_text2kg() -> dict[str, float | int | str]:
	ground_truth_dirs = _ground_truth_dirs()
	ontology_dirs = _ontology_dirs()
	entries = _collect_entries(ground_truth_dirs)
	if not entries:
		raise ValueError("No JSONL entries found in the Text2KGBench ground-truth directories.")

	class_total, object_property_total, ontology_file_count = _collect_tbox_counts(ontology_dirs)
	if ontology_file_count == 0:
		raise ValueError("No ontology JSON files found in the Text2KGBench ontology directories.")

	total_triples = sum(len(entry.get("triples", [])) for entry in entries)

	return {
		"num_ontology_files": ontology_file_count,
		"num_tbox_classes": class_total,
		"num_tbox_object_properties": object_property_total,
		"num_entries": len(entries),
		"total_triples": total_triples,
		"avg_sentences_per_text": mean(_count_sentences(entry.get("sent", "")) for entry in entries),
		"avg_triples_per_text": mean(len(entry.get("triples", [])) for entry in entries),
		"dataset_structure": (
			"The dataset is split into two benchmark families: DBpedia/WebNLG and Wikidata/TekGen. "
			"Each family has a ground-truth directory with one JSONL file per ontology slice. Every JSONL "
			"line is a standalone example with an id, a sentence in sent, and a triples array containing "
			"gold subject-relation-object tuples. The ontology side has one JSON file per slice, with concepts "
			"and relations arrays. For counting purposes, all ontology JSON files are treated as one aggregated TBox."
		),
	}


def main() -> None:
	metrics = characterize_text2kg()

	print("Text2KGBench Dataset Characterization")
	print("=" * 38)
	print("What I understood about the structure:")
	print(metrics["dataset_structure"])
	print()
	print(f"Ontology files: {metrics['num_ontology_files']}")
	print(f"TBox classes across all ontologies: {metrics['num_tbox_classes']}")
	print(f"TBox object properties across all ontologies: {metrics['num_tbox_object_properties']}")
	print(f"Total benchmark entries: {metrics['num_entries']}")
	print(f"Total triples in dataset: {metrics['total_triples']}")
	print(f"Average sentences per input example: {metrics['avg_sentences_per_text']:.2f}")
	print(f"Average triples per text: {metrics['avg_triples_per_text']:.2f}")


if __name__ == "__main__":
	main()
