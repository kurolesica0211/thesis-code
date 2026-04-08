"""Inject missing SHACL node shapes for ontology classes.

Given an ontology and a SHACL shapes graph, this script finds ontology classes
that do not yet have a corresponding ``sh:NodeShape`` and creates minimal shapes
for them.

Minimal shape created:
- ``rdf:type sh:NodeShape``
- optional ``rdf:type rdfs:Class``
- optional ``sh:closed true``
- optional ``sh:ignoredProperties ( rdf:type )``

This is useful for classes that are present in the ontology but have no explicit
property constraints in SHACL (for example, ``fhkb:Sex`` in the family ontology).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Set

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS, SH


def parse_graph(path: Path, fmt: Optional[str] = None) -> Graph:
	graph = Graph()
	graph.parse(path.as_posix(), format=fmt)
	return graph


def ontology_classes(ontology: Graph) -> Set[URIRef]:
	classes: Set[URIRef] = set()

	for cls in ontology.subjects(RDF.type, OWL.Class):
		if isinstance(cls, URIRef):
			classes.add(cls)

	# Include classes that are only referenced via subclass axioms.
	for cls, _, _ in ontology.triples((None, RDFS.subClassOf, None)):
		if isinstance(cls, URIRef):
			classes.add(cls)

	# Include classes referenced in union/intersection descriptions.
	for _, _, expr in ontology.triples((None, OWL.unionOf, None)):
		if isinstance(expr, (URIRef, BNode)):
			try:
				for member in Collection(ontology, expr):
					if isinstance(member, URIRef):
						classes.add(member)
			except Exception:
				pass

	for _, _, expr in ontology.triples((None, OWL.intersectionOf, None)):
		if isinstance(expr, (URIRef, BNode)):
			try:
				for member in Collection(ontology, expr):
					if isinstance(member, URIRef):
						classes.add(member)
			except Exception:
				pass

	return classes


def existing_node_shapes(shapes: Graph) -> Set[URIRef]:
	nodes: Set[URIRef] = set()
	for subject in shapes.subjects(RDF.type, SH.NodeShape):
		if isinstance(subject, URIRef):
			nodes.add(subject)
	return nodes


def add_minimal_shape(
	shapes: Graph,
	cls: URIRef,
	include_class_type: bool,
	closed: bool,
	ignore_rdf_type: bool,
) -> None:
	shapes.add((cls, RDF.type, SH.NodeShape))

	if include_class_type:
		shapes.add((cls, RDF.type, RDFS.Class))

	if closed:
		shapes.add((cls, SH.closed, Literal(True)))

	if ignore_rdf_type:
		ignored_list = BNode()
		Collection(shapes, ignored_list, [RDF.type])
		shapes.add((cls, SH.ignoredProperties, ignored_list))


def inject_missing_shapes(
	ontology: Graph,
	shapes: Graph,
	include_class_type: bool,
	closed: bool,
	ignore_rdf_type: bool,
) -> tuple[Graph, list[URIRef]]:
	ont_classes = ontology_classes(ontology)
	node_shapes = existing_node_shapes(shapes)

	missing = sorted(ont_classes - node_shapes, key=str)
	for cls in missing:
		add_minimal_shape(shapes, cls, include_class_type, closed, ignore_rdf_type)

	return shapes, missing


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Inject SHACL NodeShapes for ontology classes missing in a shapes graph."
	)
	parser.add_argument("--ontology", required=True, help="Path to ontology file.")
	parser.add_argument("--shapes", required=True, help="Path to SHACL shapes file.")
	parser.add_argument("--output", required=True, help="Output file path.")
	parser.add_argument(
		"--ontology-format",
		default=None,
		help="Optional rdflib format for ontology (xml, turtle, ttl, etc.).",
	)
	parser.add_argument(
		"--shapes-format",
		default=None,
		help="Optional rdflib format for shapes (turtle, trig, nt, etc.).",
	)
	parser.add_argument(
		"--output-format",
		default="turtle",
		help="Output serialization format (default: turtle).",
	)
	parser.add_argument(
		"--no-class-type",
		action="store_true",
		help="Do not add rdf:type rdfs:Class to newly created shapes.",
	)
	parser.add_argument(
		"--open-shapes",
		action="store_true",
		help="Do not add sh:closed true to newly created shapes.",
	)
	parser.add_argument(
		"--dont-ignore-rdf-type",
		action="store_true",
		help="Do not add sh:ignoredProperties (rdf:type) to newly created shapes.",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	ontology_path = Path(args.ontology)
	shapes_path = Path(args.shapes)
	output_path = Path(args.output)

	ontology = parse_graph(ontology_path, args.ontology_format)
	shapes = parse_graph(shapes_path, args.shapes_format)

	updated, missing = inject_missing_shapes(
		ontology=ontology,
		shapes=shapes,
		include_class_type=not args.no_class_type,
		closed=not args.open_shapes,
		ignore_rdf_type=not args.dont_ignore_rdf_type,
	)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	updated.serialize(destination=output_path.as_posix(), format=args.output_format)

	print(f"Added {len(missing)} missing NodeShape(s).")
	if missing:
		print("Created shapes for:")
		for cls in missing:
			print(f"- {cls}")


if __name__ == "__main__":
	main()
