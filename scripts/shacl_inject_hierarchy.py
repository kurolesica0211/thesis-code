"""Inject ontology hierarchy into SHACL node shapes.

This script enriches closed SHACL node shapes by:
1) adding subproperties of already allowed properties,
2) adding properties inherited from superclass shapes,
3) ensuring inherited properties also include their subproperties.

For newly added properties, missing property-shape definitions are created from:
- existing SHACL property-shape templates (if any), otherwise
- ontology axioms (range, functional, and class restrictions).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional, Set, Tuple

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS, SH, XSD


@dataclass(frozen=True)
class ConstraintTemplate:
	range_class: Optional[URIRef] = None
	min_count: Optional[int] = None
	max_count: Optional[int] = None


def local_name(uri: URIRef) -> str:
	text = str(uri)
	if "#" in text:
		return text.rsplit("#", 1)[1]
	if "/" in text:
		return text.rsplit("/", 1)[1]
	return text


def literal_to_int(value: Literal) -> Optional[int]:
	try:
		return int(str(value))
	except (TypeError, ValueError):
		return None


def parse_graph(path: Path, fmt: Optional[str] = None) -> Graph:
	graph = Graph()
	graph.parse(path.as_posix(), format=fmt)
	return graph


def list_members(graph: Graph, node: URIRef | BNode) -> Iterable[URIRef | BNode]:
	try:
		yield from Collection(graph, node)
	except Exception:
		return


def build_subproperty_maps(ontology: Graph) -> Tuple[Dict[URIRef, Set[URIRef]], Dict[URIRef, Set[URIRef]]]:
	direct_children: Dict[URIRef, Set[URIRef]] = {}
	direct_parents: Dict[URIRef, Set[URIRef]] = {}
	for child, _, parent in ontology.triples((None, RDFS.subPropertyOf, None)):
		if not isinstance(child, URIRef) or not isinstance(parent, URIRef):
			continue
		direct_children.setdefault(parent, set()).add(child)
		direct_parents.setdefault(child, set()).add(parent)

	descendants: Dict[URIRef, Set[URIRef]] = {}
	ancestors: Dict[URIRef, Set[URIRef]] = {}

	all_props = set(direct_children) | set(direct_parents)
	for prop in all_props:
		stack = list(direct_children.get(prop, set()))
		seen: Set[URIRef] = set()
		while stack:
			item = stack.pop()
			if item in seen:
				continue
			seen.add(item)
			stack.extend(direct_children.get(item, set()))
		descendants[prop] = seen

		stack = list(direct_parents.get(prop, set()))
		seen = set()
		while stack:
			item = stack.pop()
			if item in seen:
				continue
			seen.add(item)
			stack.extend(direct_parents.get(item, set()))
		ancestors[prop] = seen

	return descendants, ancestors


def build_class_hierarchy(ontology: Graph, shapes: Graph, shape_nodes: Set[URIRef]) -> Dict[URIRef, Set[URIRef]]:
	direct_supers: Dict[URIRef, Set[URIRef]] = {}
	for graph in (ontology, shapes):
		for cls, _, sup in graph.triples((None, RDFS.subClassOf, None)):
			if not isinstance(cls, URIRef) or not isinstance(sup, URIRef):
				continue
			direct_supers.setdefault(cls, set()).add(sup)

	# Derive common subclass links from equivalentClass expressions.
	for cls, _, eq in ontology.triples((None, OWL.equivalentClass, None)):
		if not isinstance(cls, URIRef):
			continue

		if isinstance(eq, URIRef):
			direct_supers.setdefault(cls, set()).add(eq)
			direct_supers.setdefault(eq, set()).add(cls)
			continue

		if not isinstance(eq, BNode):
			continue

		inter = ontology.value(eq, OWL.intersectionOf)
		if isinstance(inter, (URIRef, BNode)):
			for member in list_members(ontology, inter):
				if isinstance(member, URIRef):
					direct_supers.setdefault(cls, set()).add(member)

		union = ontology.value(eq, OWL.unionOf)
		if isinstance(union, (URIRef, BNode)):
			for member in list_members(ontology, union):
				if isinstance(member, URIRef):
					direct_supers.setdefault(member, set()).add(cls)

	supers: Dict[URIRef, Set[URIRef]] = {}
	for cls in shape_nodes:
		stack = list(direct_supers.get(cls, set()))
		seen: Set[URIRef] = set()
		while stack:
			item = stack.pop()
			if item in seen:
				continue
			seen.add(item)
			stack.extend(direct_supers.get(item, set()))
		supers[cls] = seen
	return supers


def shape_property_maps(shapes: Graph, shape_nodes: Set[URIRef]) -> Tuple[Dict[URIRef, Set[URIRef]], Dict[URIRef, URIRef], Dict[URIRef, ConstraintTemplate]]:
	shape_to_paths: Dict[URIRef, Set[URIRef]] = {shape: set() for shape in shape_nodes}
	path_to_shape_template: Dict[URIRef, URIRef] = {}
	path_to_constraints: Dict[URIRef, ConstraintTemplate] = {}

	for shape in shape_nodes:
		for _, _, prop_shape in shapes.triples((shape, SH.property, None)):
			if not isinstance(prop_shape, URIRef):
				continue
			path = shapes.value(prop_shape, SH.path)
			if not isinstance(path, URIRef):
				continue
			shape_to_paths[shape].add(path)
			path_to_shape_template.setdefault(path, prop_shape)

			range_class = shapes.value(prop_shape, SH['class'])
			min_count_lit = shapes.value(prop_shape, SH.minCount)
			max_count_lit = shapes.value(prop_shape, SH.maxCount)

			min_count = literal_to_int(min_count_lit) if isinstance(min_count_lit, Literal) else None
			max_count = literal_to_int(max_count_lit) if isinstance(max_count_lit, Literal) else None
			range_uri = range_class if isinstance(range_class, URIRef) else None

			existing = path_to_constraints.get(path, ConstraintTemplate())
			merged = ConstraintTemplate(
				range_class=existing.range_class or range_uri,
				min_count=existing.min_count if existing.min_count is not None else min_count,
				max_count=existing.max_count if existing.max_count is not None else max_count,
			)
			path_to_constraints[path] = merged

	return shape_to_paths, path_to_shape_template, path_to_constraints


def restrictions_for_class_and_property(ontology: Graph, cls: URIRef, prop: URIRef) -> ConstraintTemplate:
	min_count: Optional[int] = None
	max_count: Optional[int] = None
	range_class: Optional[URIRef] = None

	candidates = [
		restriction
		for _, _, restriction in ontology.triples((cls, RDFS.subClassOf, None))
	]

	# Also scan equivalentClass intersections for inline restrictions.
	for _, _, eq in ontology.triples((cls, OWL.equivalentClass, None)):
		if isinstance(eq, (BNode, URIRef)):
			inter = ontology.value(eq, OWL.intersectionOf)
			if isinstance(inter, (BNode, URIRef)):
				candidates.extend(list_members(ontology, inter))

	for restriction in candidates:
		if not isinstance(restriction, (BNode, URIRef)):
			continue
		on_property = ontology.value(restriction, OWL.onProperty)
		if on_property != prop:
			continue

		some_values = ontology.value(restriction, OWL.someValuesFrom)
		all_values = ontology.value(restriction, OWL.allValuesFrom)
		if isinstance(some_values, URIRef):
			range_class = range_class or some_values
			min_count = 1 if min_count is None else max(min_count, 1)
		if isinstance(all_values, URIRef):
			range_class = range_class or all_values

		min_q = ontology.value(restriction, OWL.minQualifiedCardinality)
		max_q = ontology.value(restriction, OWL.maxQualifiedCardinality)
		exact_q = ontology.value(restriction, OWL.qualifiedCardinality)
		min_c = ontology.value(restriction, OWL.minCardinality)
		max_c = ontology.value(restriction, OWL.maxCardinality)
		exact_c = ontology.value(restriction, OWL.cardinality)

		for lit in (min_q, min_c):
			if isinstance(lit, Literal):
				value = literal_to_int(lit)
				if value is not None:
					min_count = value if min_count is None else max(min_count, value)

		for lit in (max_q, max_c):
			if isinstance(lit, Literal):
				value = literal_to_int(lit)
				if value is not None:
					max_count = value if max_count is None else min(max_count, value)

		for lit in (exact_q, exact_c):
			if isinstance(lit, Literal):
				value = literal_to_int(lit)
				if value is not None:
					min_count = value if min_count is None else max(min_count, value)
					max_count = value if max_count is None else min(max_count, value)

		on_class = ontology.value(restriction, OWL.onClass)
		if isinstance(on_class, URIRef):
			range_class = range_class or on_class

	return ConstraintTemplate(range_class=range_class, min_count=min_count, max_count=max_count)


def constraints_from_ontology(
	ontology: Graph,
	cls: URIRef,
	prop: URIRef,
	class_supers: Dict[URIRef, Set[URIRef]],
	superprops: Dict[URIRef, Set[URIRef]],
) -> ConstraintTemplate:
	# Collect from property itself and all its super-properties.
	prop_candidates = {prop} | superprops.get(prop, set())
	range_class: Optional[URIRef] = None
	max_count: Optional[int] = None

	for candidate in prop_candidates:
		range_candidate = ontology.value(candidate, RDFS.range)
		if isinstance(range_candidate, URIRef):
			if range_candidate not in {RDFS.Literal, XSD.string}:
				range_class = range_class or range_candidate
		if (candidate, RDF.type, OWL.FunctionalProperty) in ontology:
			max_count = 1 if max_count is None else min(max_count, 1)

	# Collect class restrictions from class and its superclasses.
	classes_to_check = {cls} | class_supers.get(cls, set())
	min_count: Optional[int] = None
	for c in classes_to_check:
		class_constraints = restrictions_for_class_and_property(ontology, c, prop)
		if class_constraints.range_class and not range_class:
			range_class = class_constraints.range_class
		if class_constraints.min_count is not None:
			min_count = class_constraints.min_count if min_count is None else max(min_count, class_constraints.min_count)
		if class_constraints.max_count is not None:
			max_count = class_constraints.max_count if max_count is None else min(max_count, class_constraints.max_count)

	return ConstraintTemplate(range_class=range_class, min_count=min_count, max_count=max_count)


def merged_constraints(*templates: ConstraintTemplate) -> ConstraintTemplate:
	range_class: Optional[URIRef] = None
	min_count: Optional[int] = None
	max_count: Optional[int] = None

	for tpl in templates:
		if tpl.range_class and not range_class:
			range_class = tpl.range_class
		if tpl.min_count is not None:
			min_count = tpl.min_count if min_count is None else max(min_count, tpl.min_count)
		if tpl.max_count is not None:
			max_count = tpl.max_count if max_count is None else min(max_count, tpl.max_count)

	return ConstraintTemplate(range_class=range_class, min_count=min_count, max_count=max_count)


def unique_property_shape_uri(graph: Graph, shape_uri: URIRef, prop: URIRef) -> URIRef:
	base = URIRef(f"{str(shape_uri)}-{local_name(prop)}")
	if (base, None, None) not in graph and (None, None, base) not in graph:
		return base
	idx = 1
	while True:
		candidate = URIRef(f"{str(base)}_{idx}")
		if (candidate, None, None) not in graph and (None, None, candidate) not in graph:
			return candidate
		idx += 1


def ensure_property_shape(
	shapes: Graph,
	shape_uri: URIRef,
	prop: URIRef,
	path_to_template_shape: Dict[URIRef, URIRef],
	path_to_constraints: Dict[URIRef, ConstraintTemplate],
	ontology: Graph,
	class_supers: Dict[URIRef, Set[URIRef]],
	superprops: Dict[URIRef, Set[URIRef]],
) -> URIRef:
	if prop in path_to_template_shape:
		return path_to_template_shape[prop]

	shape_node = unique_property_shape_uri(shapes, shape_uri, prop)
	shapes.add((shape_node, RDF.type, SH.PropertyShape))
	shapes.add((shape_node, SH.path, prop))

	shacl_template = path_to_constraints.get(prop, ConstraintTemplate())
	ontology_template = constraints_from_ontology(ontology, shape_uri, prop, class_supers, superprops)
	final = merged_constraints(shacl_template, ontology_template)

	if final.range_class:
		shapes.add((shape_node, SH['class'], final.range_class))
	if final.min_count is not None:
		shapes.add((shape_node, SH.minCount, Literal(final.min_count)))
	if final.max_count is not None:
		shapes.add((shape_node, SH.maxCount, Literal(final.max_count)))

	path_to_template_shape[prop] = shape_node
	path_to_constraints[prop] = final
	return shape_node


def shape_nodes(shapes: Graph) -> Set[URIRef]:
	nodes: Set[URIRef] = set()
	for subject in shapes.subjects(RDF.type, SH.NodeShape):
		if isinstance(subject, URIRef):
			nodes.add(subject)
	return nodes


def compute_property_closure(
	base_shape_props: Dict[URIRef, Set[URIRef]],
	class_supers: Dict[URIRef, Set[URIRef]],
	subproperties: Dict[URIRef, Set[URIRef]],
) -> Dict[URIRef, Set[URIRef]]:
	current = {shape: set(props) for shape, props in base_shape_props.items()}

	changed = True
	while changed:
		changed = False
		for shape, props in list(current.items()):
			expanded = set(props)

			for prop in list(expanded):
				expanded.update(subproperties.get(prop, set()))

			for sup in class_supers.get(shape, set()):
				expanded.update(current.get(sup, set()))

			if expanded != props:
				current[shape] = expanded
				changed = True

	return current


def inject_hierarchy(shapes: Graph, ontology: Graph) -> Graph:
	node_shapes = shape_nodes(shapes)
	base_shape_props, path_to_template_shape, path_to_constraints = shape_property_maps(shapes, node_shapes)
	subproperties, superprops = build_subproperty_maps(ontology)
	class_supers = build_class_hierarchy(ontology, shapes, node_shapes)

	closure = compute_property_closure(base_shape_props, class_supers, subproperties)

	for shape in node_shapes:
		existing_prop_shapes = {
			pshape
			for _, _, pshape in shapes.triples((shape, SH.property, None))
			if isinstance(pshape, URIRef)
		}
		existing_paths = {
			path
			for pshape in existing_prop_shapes
			for path in [shapes.value(pshape, SH.path)]
			if isinstance(path, URIRef)
		}

		for prop in sorted(closure.get(shape, set()), key=str):
			if prop in existing_paths:
				continue
			pshape = ensure_property_shape(
				shapes,
				shape,
				prop,
				path_to_template_shape,
				path_to_constraints,
				ontology,
				class_supers,
				superprops,
			)
			shapes.add((shape, SH.property, pshape))

	return shapes


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Inject ontology class/property hierarchy into SHACL node shapes."
	)
	parser.add_argument("--ontology", required=True, help="Path to ontology file (e.g., OWL/RDF/XML, Turtle).")
	parser.add_argument("--shapes", required=True, help="Path to SHACL shapes file.")
	parser.add_argument("--output", required=True, help="Output path for enriched SHACL shapes file.")
	parser.add_argument(
		"--ontology-format",
		default=None,
		help="Optional rdflib format for ontology parsing (xml, turtle, ttl, etc.).",
	)
	parser.add_argument(
		"--shapes-format",
		default=None,
		help="Optional rdflib format for shapes parsing (turtle, trig, nt, etc.).",
	)
	parser.add_argument(
		"--output-format",
		default="turtle",
		help="Output serialization format for shapes (default: turtle).",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	ontology_path = Path(args.ontology)
	shapes_path = Path(args.shapes)
	output_path = Path(args.output)

	ontology = parse_graph(ontology_path, args.ontology_format)
	shapes = parse_graph(shapes_path, args.shapes_format)
	enriched = inject_hierarchy(shapes, ontology)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	enriched.serialize(destination=output_path.as_posix(), format=args.output_format)


if __name__ == "__main__":
	main()
