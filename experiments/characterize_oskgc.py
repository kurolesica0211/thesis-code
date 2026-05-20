from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from rdflib import Graph, OWL, RDF, URIRef


@dataclass(frozen=True)
class OskgcEntry:
	text: str
	triple_count: int


def _repo_root() -> Path:
	return Path(__file__).resolve().parent.parent


def _dataset_root() -> Path:
	return _repo_root() / "experiments" / "OSKGC"


def _data_dirs() -> list[Path]:
	root = _dataset_root() / "HeraclesWang OSKGC master benchmark-data"
	return [root / "dev", root / "train", root / "test"]


def _ontology_dir() -> Path:
	return _dataset_root() / "HeraclesWang OSKGC master benchmark-ontology_rdf"


def _count_classes(graph: Graph) -> int:
	return len({subj for subj in graph.subjects(RDF.type, OWL.Class) if isinstance(subj, URIRef)})


def _count_object_properties(graph: Graph) -> int:
	return len({subj for subj in graph.subjects(RDF.type, OWL.ObjectProperty) if isinstance(subj, URIRef)})


def _iter_xml_entries(xml_path: Path) -> list[OskgcEntry]:
	tree = ET.parse(xml_path)
	root = tree.getroot()
	entries: list[OskgcEntry] = []
	for entry in root.findall(".//entry"):
		text_node = entry.find("text")
		triples_node = entry.find("triples")
		text = text_node.text.strip() if text_node is not None and text_node.text else ""
		triple_count = len(triples_node.findall("triple")) if triples_node is not None else 0
		entries.append(OskgcEntry(text=text, triple_count=triple_count))
	return entries


def _collect_entries(data_dirs: list[Path]) -> list[OskgcEntry]:
	entries: list[OskgcEntry] = []
	for data_dir in data_dirs:
		for xml_path in sorted(data_dir.glob("*.xml")):
			entries.extend(_iter_xml_entries(xml_path))
	return entries


def _collect_tbox_counts(ontology_dir: Path) -> tuple[int, int, int]:
	class_total = 0
	object_property_total = 0
	file_count = 0
	for ttl_path in sorted(ontology_dir.glob("*.ttl")):
		graph = Graph()
		graph.parse(ttl_path, format="turtle")
		class_total += _count_classes(graph)
		object_property_total += _count_object_properties(graph)
		file_count += 1
	return class_total, object_property_total, file_count


def characterize_oskgc() -> dict[str, float | int | str]:
	data_dirs = _data_dirs()
	ontology_dir = _ontology_dir()
	entries = _collect_entries(data_dirs)
	if not entries:
		raise ValueError("No XML entries found in the OSKGC data directories.")

	class_total, object_property_total, ontology_file_count = _collect_tbox_counts(ontology_dir)
	if ontology_file_count == 0:
		raise ValueError("No ontology TTL files found in the OSKGC ontology directory.")

	return {
		"num_ontology_files": ontology_file_count,
		"num_tbox_classes": class_total,
		"num_tbox_object_properties": object_property_total,
		"num_entries": len(entries),
		"avg_text_size_chars": mean(len(entry.text) for entry in entries),
		"avg_triples_per_text": mean(entry.triple_count for entry in entries),
		"dataset_structure": (
			"Each split (dev/train/test) contains many category-specific XML files named like "
			"1_Astronaut.xml. Each XML file contains a <benchmark> with <entries>; every <entry> has "
			"an id, a category, one natural-language <text>, a gold <triples> block, and a <schemas> "
			"block that describes the expected schema pattern. The ontology side mirrors these categories "
			"with one TTL file per category, and the script treats all TTL files together as one aggregated TBox."
		),
	}


def main() -> None:
	metrics = characterize_oskgc()

	print("OSKGC Dataset Characterization")
	print("=" * 31)
	print("What I understood about the structure:")
	print(metrics["dataset_structure"])
	print()
	print(f"Ontology files: {metrics['num_ontology_files']}")
	print(f"TBox classes across all ontologies: {metrics['num_tbox_classes']}")
	print(f"TBox object properties across all ontologies: {metrics['num_tbox_object_properties']}")
	print(f"Total benchmark entries: {metrics['num_entries']}")
	print(f"Average text size (chars): {metrics['avg_text_size_chars']:.2f}")
	print(f"Average triples per text: {metrics['avg_triples_per_text']:.2f}")


if __name__ == "__main__":
	main()
