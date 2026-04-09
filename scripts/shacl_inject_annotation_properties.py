"""Inject missing ontology annotation properties into SHACL node shapes.

This script scans an ontology for annotation properties and a SHACL shapes graph
for already-mentioned property paths. Any annotation property that is not
mentioned anywhere in the SHACL shapes graph is added to every NodeShape as a
minimal property shape.

The intent is to keep closed shapes permissive for annotation metadata without
adding unnecessary value constraints.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Set

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, SH


def parse_graph(path: Path, fmt: Optional[str] = None) -> Graph:
    graph = Graph()
    graph.parse(path.as_posix(), format=fmt)
    return graph


def ontology_annotation_properties(ontology: Graph) -> Set[URIRef]:
    annotation_properties: Set[URIRef] = set()

    for prop in ontology.subjects(RDF.type, OWL.AnnotationProperty):
        if isinstance(prop, URIRef):
            annotation_properties.add(prop)

    # Some ontologies may only declare annotation properties by using the
    # `owl:AnnotationProperty` term in Turtle prefixes or through equivalent
    # naming conventions; keep the scan focused on explicit ontology axioms.
    return annotation_properties


def mentioned_paths(shapes: Graph) -> Set[URIRef]:
    paths: Set[URIRef] = set()
    for path in shapes.objects(predicate=SH.path):
        if isinstance(path, URIRef):
            paths.add(path)
    return paths


def node_shapes(shapes: Graph) -> Set[URIRef]:
    nodes: Set[URIRef] = set()
    for subject in shapes.subjects(RDF.type, SH.NodeShape):
        if isinstance(subject, URIRef):
            nodes.add(subject)
    return nodes


def unique_property_shape_uri(graph: Graph, shape_uri: URIRef, prop: URIRef) -> URIRef:
    prop_text = str(prop)
    local = prop_text.rsplit("#", 1)[-1] if "#" in prop_text else prop_text.rsplit("/", 1)[-1]
    base = URIRef(f"{str(shape_uri)}-{local}")
    if (base, None, None) not in graph and (None, None, base) not in graph:
        return base

    index = 1
    while True:
        candidate = URIRef(f"{str(base)}_{index}")
        if (candidate, None, None) not in graph and (None, None, candidate) not in graph:
            return candidate
        index += 1


def add_annotation_property_shape(shapes: Graph, shape_uri: URIRef, prop: URIRef) -> URIRef:
    prop_shape = unique_property_shape_uri(shapes, shape_uri, prop)
    shapes.add((prop_shape, RDF.type, SH.PropertyShape))
    shapes.add((prop_shape, SH.path, prop))
    shapes.add((shape_uri, SH.property, prop_shape))
    return prop_shape


def inject_annotation_properties(ontology: Graph, shapes: Graph) -> tuple[Graph, dict[URIRef, list[URIRef]]]:
    annotation_properties = ontology_annotation_properties(ontology)
    existing_paths = mentioned_paths(shapes)
    shapes_to_update = node_shapes(shapes)

    missing = sorted(annotation_properties - existing_paths, key=str)
    added: dict[URIRef, list[URIRef]] = {shape: [] for shape in shapes_to_update}

    for shape in sorted(shapes_to_update, key=str):
        for prop in missing:
            add_annotation_property_shape(shapes, shape, prop)
            added[shape].append(prop)

    return shapes, added


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inject ontology annotation properties into every SHACL NodeShape when missing globally."
    )
    parser.add_argument("--ontology", required=True, help="Path to the ontology file.")
    parser.add_argument("--shapes", required=True, help="Path to the input SHACL shapes file.")
    parser.add_argument("--output", required=True, help="Path to write the updated SHACL shapes file.")
    parser.add_argument(
        "--ontology-format",
        default=None,
        help="Optional rdflib format for the ontology (xml, turtle, ttl, etc.).",
    )
    parser.add_argument(
        "--shapes-format",
        default=None,
        help="Optional rdflib format for the SHACL shapes (turtle, trig, nt, etc.).",
    )
    parser.add_argument(
        "--output-format",
        default="turtle",
        help="Serialization format for the output file (default: turtle).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    ontology_path = Path(args.ontology)
    shapes_path = Path(args.shapes)
    output_path = Path(args.output)

    ontology = parse_graph(ontology_path, args.ontology_format)
    shapes = parse_graph(shapes_path, args.shapes_format)

    updated, added = inject_annotation_properties(ontology, shapes)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    updated.serialize(destination=output_path.as_posix(), format=args.output_format)

    total_added = sum(len(props) for props in added.values())
    print(f"Added {total_added} annotation property shape(s) across {len(added)} NodeShape(s).")


if __name__ == "__main__":
    main()