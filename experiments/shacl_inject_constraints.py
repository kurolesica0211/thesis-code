"""Inject and propagate ontology-driven constraints into SHACL shapes.

Assumes that constraints domain, range, and propertyDisjointWith, are propagated through the onotology correctly.

It performs the following transformations:
1) Inject annotation properties using reusable generic PropertyShapes.
2) Inject minimal missing NodeShapes for ontology classes.
3) Propagate allowed properties across non-disjoint NodeShapes.
4) Transfer class disjointness into esh:disjointWith constraints.
5) Add generic superclass inference TripleRules.
6) Transfer property disjointness using sh:disjoint and enrich with
   equivalent/sub-properties.
7) Mark irreflexive properties with esh:isIrreflexive true.
8) Mark asymmetric properties with esh:isAsymmetric true.
9) Remove all sh:minCount triples.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS, SH, XSD

ESH = Namespace("http://example.org/esh#")


def parse_graph(path: Path, fmt: Optional[str] = None) -> Graph:
    graph = Graph()
    graph.parse(path.as_posix(), format=fmt)
    return graph


def local_name(term: URIRef) -> str:
    text = str(term)
    if "#" in text:
        return text.rsplit("#", 1)[-1]
    return text.rsplit("/", 1)[-1]


def cut_local_name(term: URIRef) -> str:
    name = local_name(term)
    uri = str(term).replace(name, '')
    return uri


def stable_iri(base: Namespace, prefix: str, term: URIRef) -> URIRef:
    raw = local_name(term)
    cleaned = "".join(ch if (ch.isalnum() or ch == "_") else "_" for ch in raw)
    return base[f"{prefix}_{cleaned}"]


def ontology_classes(ontology: Graph) -> Set[URIRef]:
    classes: Set[URIRef] = set()
    for cls in ontology.subjects(RDF.type, OWL.Class):
        if isinstance(cls, URIRef):
            classes.add(cls)
    for cls in ontology.subjects(RDF.type, RDFS.Class):
        if isinstance(cls, URIRef):
            classes.add(cls)
    for cls, _, parent in ontology.triples((None, RDFS.subClassOf, None)):
        if isinstance(cls, URIRef):
            classes.add(cls)
        if isinstance(parent, URIRef):
            classes.add(parent)
    return classes


def annotation_properties(ontology: Graph) -> Set[URIRef]:
    props: Set[URIRef] = set()
    for prop in ontology.subjects(RDF.type, OWL.AnnotationProperty):
        if isinstance(prop, URIRef):
            props.add(prop)
    return props


def node_shapes(shapes: Graph) -> Set[URIRef]:
    return {
        node
        for node in shapes.subjects(RDF.type, SH.NodeShape)
        if isinstance(node, URIRef)
    }


def shape_to_classes(shape: URIRef, shapes: Graph, ont_classes: Set[URIRef]) -> Set[URIRef]:
    classes = {
        cls
        for cls in shapes.objects(shape, SH.targetClass)
        if isinstance(cls, URIRef)
    }
    if not classes and shape in ont_classes:
        classes.add(shape)
    return classes


def property_shapes_of_node(shapes: Graph, node_shape: URIRef) -> Set[URIRef | BNode]:
    return {
        pshape
        for pshape in shapes.objects(node_shape, SH.property)
        if isinstance(pshape, (URIRef, BNode))
    }


def property_shape_path(shapes: Graph, pshape: URIRef | BNode) -> Optional[URIRef]:
    for path in shapes.objects(pshape, SH.path):
        if isinstance(path, URIRef):
            return path
    return None


def existing_paths_in_node(shapes: Graph, node_shape: URIRef) -> Set[URIRef]:
    paths: Set[URIRef] = set()
    for pshape in property_shapes_of_node(shapes, node_shape):
        path = property_shape_path(shapes, pshape)
        if path is not None:
            paths.add(path)
    return paths


def all_property_shapes(shapes: Graph) -> Set[URIRef | BNode]:
    return {
        s
        for s in shapes.subjects(RDF.type, SH.PropertyShape)
        if isinstance(s, (URIRef, BNode))
    }


def ensure_minimal_missing_shapes(
    ontology: Graph,
    shapes: Graph,
) -> list[URIRef]:
    ont_classes = ontology_classes(ontology)
    shaped_classes: Set[URIRef] = set()
    for shape in node_shapes(shapes):
        shaped_classes.update(shape_to_classes(shape, shapes, ont_classes))

    missing = sorted(ont_classes - shaped_classes, key=str)
    for cls in missing:
        shapes.add((cls, RDF.type, SH.NodeShape))
        shapes.add((cls, RDF.type, RDFS.Class))
        shapes.add((cls, SH.closed, Literal(True)))
        ignored = BNode()
        Collection(shapes, ignored, [RDF.type])
        shapes.add((cls, SH.ignoredProperties, ignored))
    return missing


def ensure_annotation_property_shapes(ontology: Graph, shapes: Graph) -> int:
    props = sorted(annotation_properties(ontology), key=str)
    nodes = sorted(node_shapes(shapes), key=str)
    added_links = 0

    # Reuse existing PropertyShape for a path when present.
    path_to_shapes: Dict[URIRef, Set[URIRef | BNode]] = {}
    for pshape in all_property_shapes(shapes):
        path = property_shape_path(shapes, pshape)
        if path is not None:
            path_to_shapes.setdefault(path, set()).add(pshape)

    for prop in props:
        if prop in path_to_shapes and path_to_shapes[prop]:
            reusable = next(iter(path_to_shapes[prop]))
        else:
            reusable_uri = URIRef(f"{cut_local_name(prop)}AnnotationProperty_{local_name(prop)}")
            shapes.add((reusable_uri, RDF.type, SH.PropertyShape))
            shapes.add((reusable_uri, SH.path, prop))
            path_to_shapes.setdefault(prop, set()).add(reusable_uri)
            reusable = reusable_uri

        for node in nodes:
            if (node, SH.property, reusable) not in shapes:
                if prop not in existing_paths_in_node(shapes, node):
                    shapes.add((node, SH.property, reusable))
                    added_links += 1

    return added_links


def direct_subclass_edges(ontology: Graph) -> Set[Tuple[URIRef, URIRef]]:
    """Collect direct subclass edges with lightweight OWL class-expression support.

    Supported inferences:
    - explicit rdfs:subClassOf
    - named owl:equivalentClass (both directions)
    - C owl:equivalentClass [ owl:intersectionOf (... named classes ...) ] => C sub each member
    - C owl:equivalentClass [ owl:unionOf (... named classes ...) ] => each member sub C
    """

    edges: Set[Tuple[URIRef, URIRef]] = set()

    for child, _, parent in ontology.triples((None, RDFS.subClassOf, None)):
        if isinstance(child, URIRef) and isinstance(parent, URIRef):
            edges.add((child, parent))

    def parse_equivalent_expression(named_cls: URIRef, expr: URIRef | BNode) -> None:
        for _, _, list_node in ontology.triples((expr, OWL.intersectionOf, None)):
            if isinstance(list_node, (URIRef, BNode)):
                try:
                    for member in Collection(ontology, list_node):
                        if isinstance(member, URIRef):
                            edges.add((named_cls, member))
                except Exception:
                    pass

        for _, _, list_node in ontology.triples((expr, OWL.unionOf, None)):
            if isinstance(list_node, (URIRef, BNode)):
                try:
                    for member in Collection(ontology, list_node):
                        if isinstance(member, URIRef):
                            edges.add((member, named_cls))
                except Exception:
                    pass

    for left, _, right in ontology.triples((None, OWL.equivalentClass, None)):
        if isinstance(left, URIRef) and isinstance(right, URIRef):
            edges.add((left, right))
            edges.add((right, left))

        if isinstance(left, URIRef) and isinstance(right, (URIRef, BNode)):
            parse_equivalent_expression(left, right)
        if isinstance(right, URIRef) and isinstance(left, (URIRef, BNode)):
            parse_equivalent_expression(right, left)

    return edges


def transitive_superclasses(ontology: Graph, classes: Set[URIRef]) -> Dict[URIRef, Set[URIRef]]:
    direct: Dict[URIRef, Set[URIRef]] = {cls: set() for cls in classes}
    for child, parent in direct_subclass_edges(ontology):
        direct.setdefault(child, set()).add(parent)
        direct.setdefault(parent, set())

    closure: Dict[URIRef, Set[URIRef]] = {cls: set() for cls in direct}
    for cls in direct:
        stack = list(direct.get(cls, set()))
        seen: Set[URIRef] = set()
        while stack:
            sup = stack.pop()
            if sup in seen:
                continue
            seen.add(sup)
            closure.setdefault(cls, set()).add(sup)
            stack.extend(direct.get(sup, set()))
    return closure


def direct_disjoint_map(ontology: Graph) -> Dict[URIRef, Set[URIRef]]:
    disjoint: Dict[URIRef, Set[URIRef]] = {}

    for left, _, right in ontology.triples((None, OWL.disjointWith, None)):
        if isinstance(left, URIRef) and isinstance(right, URIRef):
            disjoint.setdefault(left, set()).add(right)
            disjoint.setdefault(right, set()).add(left)

    for disjoint_set in ontology.subjects(RDF.type, OWL.AllDisjointClasses):
        members_node = ontology.value(disjoint_set, OWL.members)
        if members_node is None:
            members_node = ontology.value(disjoint_set, OWL.distinctMembers)
        if isinstance(members_node, (URIRef, BNode)):
            try:
                members = [m for m in Collection(ontology, members_node) if isinstance(m, URIRef)]
                for i, first in enumerate(members):
                    for second in members[i + 1 :]:
                        disjoint.setdefault(first, set()).add(second)
                        disjoint.setdefault(second, set()).add(first)
            except Exception:
                pass

    return disjoint


def disjoint_class_pairs(ontology: Graph, classes: Set[URIRef]) -> Set[Tuple[URIRef, URIRef]]:
    pairs: Set[Tuple[URIRef, URIRef]] = set()

    for left, _, right in ontology.triples((None, OWL.disjointWith, None)):
        if isinstance(left, URIRef) and isinstance(right, URIRef):
            pairs.add((left, right))
            pairs.add((right, left))

    for disjoint_set in ontology.subjects(RDF.type, OWL.AllDisjointClasses):
        members_node = ontology.value(disjoint_set, OWL.members)
        if members_node is None:
            members_node = ontology.value(disjoint_set, OWL.distinctMembers)
        if isinstance(members_node, (URIRef, BNode)):
            try:
                members = [m for m in Collection(ontology, members_node) if isinstance(m, URIRef)]
                for i, first in enumerate(members):
                    for second in members[i + 1 :]:
                        pairs.add((first, second))
                        pairs.add((second, first))
            except Exception:
                pass

    super_to_subs: Dict[URIRef, Set[URIRef]] = {cls: {cls} for cls in classes}
    for sub, supers in transitive_superclasses(ontology, classes).items():
        for sup in supers:
            super_to_subs.setdefault(sup, {sup}).add(sub)
        super_to_subs.setdefault(sub, {sub})

    expanded: Set[Tuple[URIRef, URIRef]] = set()
    for left, right in pairs:
        left_subs = super_to_subs.get(left, {left})
        right_subs = super_to_subs.get(right, {right})
        for l in left_subs:
            for r in right_subs:
                if l != r:
                    expanded.add((l, r))
    return expanded


def shapes_are_disjoint(
    shape_a: URIRef,
    shape_b: URIRef,
    shape_classes: Dict[URIRef, Set[URIRef]],
    disjoint_pairs: Set[Tuple[URIRef, URIRef]],
) -> bool:
    for class_a in shape_classes.get(shape_a, set()):
        for class_b in shape_classes.get(shape_b, set()):
            if (class_a, class_b) in disjoint_pairs or (class_b, class_a) in disjoint_pairs:
                return True
    return False


def propagate_properties_across_non_disjoint_nodes(ontology: Graph, shapes: Graph) -> int:
    nodes = sorted(node_shapes(shapes), key=str)
    ont_classes = ontology_classes(ontology)
    shape_classes = {node: shape_to_classes(node, shapes, ont_classes) for node in nodes}
    all_classes = ont_classes | set().union(*shape_classes.values())

    # Superclass closure for each class (includes inferred edges from selected
    # owl:equivalentClass intersection/union patterns).
    supers = transitive_superclasses(ontology, all_classes)

    # Descendant closure (class -> all transitive subclasses including itself).
    descendants: Dict[URIRef, Set[URIRef]] = {cls: {cls} for cls in all_classes}
    for child, ancestors in supers.items():
        descendants.setdefault(child, {child})
        for ancestor in ancestors:
            descendants.setdefault(ancestor, {ancestor}).add(child)

    # Direct disjoint relations as asserted in the ontology.
    direct_disjoint = direct_disjoint_map(ontology)

    # Snapshot source properties to avoid cascade propagation via intermediate
    # non-disjoint nodes (which can otherwise reintroduce disjoint-source paths).
    source_properties: Dict[URIRef, Set[URIRef | BNode]] = {
        node: set(property_shapes_of_node(shapes, node)) for node in nodes
    }

    added = 0
    for dst in nodes:
        dst_classes = shape_classes.get(dst, set())

        # For each target class C, collect:
        # - all superclasses of C (and C itself)
        # - classes disjoint with any of those
        # - subclasses of those disjoint classes
        forbidden: Set[URIRef] = set()
        for cls in dst_classes:
            for ancestor in {cls} | supers.get(cls, set()):
                for disjoint_cls in direct_disjoint.get(ancestor, set()):
                    forbidden.add(disjoint_cls)
                    forbidden.update(descendants.get(disjoint_cls, {disjoint_cls}))

        for src in nodes:
            if src == dst:
                continue

            # Skip all source shapes whose class-set intersects the forbidden set.
            src_classes = shape_classes.get(src, set())
            if src_classes and (src_classes & forbidden):
                continue

            for pshape in source_properties.get(src, set()):
                if (dst, SH.property, pshape) not in shapes:
                    shapes.add((dst, SH.property, pshape))
                    added += 1
    return added


def ensure_disjoint_with_component(shapes: Graph) -> None:
    comp = ESH.DisjointWithConstraintComponent
    param = ESH.DisjointWithParameter
    validator = ESH.DisjointWithNodeValidator

    shapes.add((comp, RDF.type, SH.ConstraintComponent))
    shapes.add((comp, SH.parameter, param))
    shapes.add((param, RDF.type, SH.Parameter))
    shapes.add((param, SH.path, ESH.disjointWith))
    shapes.add((param, SH.nodeKind, SH.IRI))
    shapes.add((param, SH.name, Literal("disjoint with class")))
    shapes.add(
        (
            param,
            SH.description,
            Literal("Ensures the focus node is not an instance of the specified class."),
        )
    )

    shapes.add((comp, SH.nodeValidator, validator))
    shapes.add((validator, RDF.type, SH.SPARQLSelectValidator))
    shapes.add(
        (
            validator,
            SH.message,
            Literal("Class disjointness violation."),
        )
    )
    shapes.add(
        (
            validator,
            SH.select,
            Literal(
                f"""
SELECT $this ?disjointClass
WHERE {{
    $currentShape <{ESH.disjointWith}> ?disjointClass .
    $this a ?disjointClass .
}}
""",
            ),
        )
    )


def transfer_class_disjointness(ontology: Graph, shapes: Graph) -> int:
    ensure_disjoint_with_component(shapes)
    nodes = sorted(node_shapes(shapes), key=str)
    classes = ontology_classes(ontology)
    shape_classes = {node: shape_to_classes(node, shapes, classes) for node in nodes}
    disjoint_pairs = disjoint_class_pairs(ontology, classes | set().union(*shape_classes.values()))

    added = 0
    for node in nodes:
        for cls in shape_classes.get(node, set()):
            for left, right in disjoint_pairs:
                if left == cls and (node, ESH.disjointWith, right) not in shapes:
                    shapes.add((node, ESH.disjointWith, right))
                    added += 1
    return added


def ensure_inference_rule(shapes: Graph, superclass: URIRef) -> URIRef:
    rule = stable_iri(ESH, "InferTypeRule", superclass)
    shapes.add((rule, RDF.type, SH.TripleRule))
    shapes.add((rule, SH.subject, SH.this))
    shapes.add((rule, SH.predicate, RDF.type))
    shapes.add((rule, SH.object, superclass))
    return rule


def add_superclass_inference_rules(ontology: Graph, shapes: Graph) -> int:
    nodes = sorted(node_shapes(shapes), key=str)
    classes = ontology_classes(ontology)
    shape_classes = {node: shape_to_classes(node, shapes, classes) for node in nodes}
    supers = transitive_superclasses(ontology, classes | set().union(*shape_classes.values()))

    added = 0
    for node in nodes:
        for cls in shape_classes.get(node, set()):
            for superclass in sorted(supers.get(cls, set()), key=str):
                if superclass == cls:
                    continue
                rule = ensure_inference_rule(shapes, superclass)
                if (node, SH.rule, rule) not in shapes:
                    shapes.add((node, SH.rule, rule))
                    added += 1
    return added


def equivalent_property_closure(ontology: Graph) -> Dict[URIRef, Set[URIRef]]:
    neighbors: Dict[URIRef, Set[URIRef]] = {}
    for left, _, right in ontology.triples((None, OWL.equivalentProperty, None)):
        if isinstance(left, URIRef) and isinstance(right, URIRef):
            neighbors.setdefault(left, set()).add(right)
            neighbors.setdefault(right, set()).add(left)

    closure: Dict[URIRef, Set[URIRef]] = {}
    for prop in list(neighbors):
        stack = [prop]
        seen: Set[URIRef] = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(neighbors.get(cur, set()))
        closure[prop] = seen
    return closure


def transitive_subproperties(ontology: Graph) -> Dict[URIRef, Set[URIRef]]:
    # Map super-property -> transitive set of sub-properties.
    children: Dict[URIRef, Set[URIRef]] = {}
    for sub, _, sup in ontology.triples((None, RDFS.subPropertyOf, None)):
        if isinstance(sub, URIRef) and isinstance(sup, URIRef):
            children.setdefault(sup, set()).add(sub)
            children.setdefault(sub, set())

    closure: Dict[URIRef, Set[URIRef]] = {prop: set() for prop in children}
    for sup in children:
        stack = list(children.get(sup, set()))
        seen: Set[URIRef] = set()
        while stack:
            child = stack.pop()
            if child in seen:
                continue
            seen.add(child)
            closure.setdefault(sup, set()).add(child)
            stack.extend(children.get(child, set()))
    return closure


def property_disjoint_pairs(ontology: Graph) -> Dict[URIRef, Set[URIRef]]:
    disj: Dict[URIRef, Set[URIRef]] = {}

    def add_pair(a: URIRef, b: URIRef) -> None:
        disj.setdefault(a, set()).add(b)
        disj.setdefault(b, set()).add(a)

    for left, _, right in ontology.triples((None, OWL.propertyDisjointWith, None)):
        if not isinstance(left, URIRef):
            continue

        if isinstance(right, URIRef):
            add_pair(left, right)
            continue

        if isinstance(right, (URIRef, BNode)):
            try:
                for member in Collection(ontology, right):
                    if isinstance(member, URIRef):
                        add_pair(left, member)
            except Exception:
                pass

    return disj


def enrich_property_disjointness(ontology: Graph, shapes: Graph) -> int:
    disj = property_disjoint_pairs(ontology)
    eq = equivalent_property_closure(ontology)
    sub = transitive_subproperties(ontology)

    def expand(target: URIRef) -> Set[URIRef]:
        expanded = set(eq.get(target, {target}))
        expanded.add(target)
        result: Set[URIRef] = set()
        for prop in expanded:
            result.add(prop)
            result.update(sub.get(prop, set()))
        return result

    added = 0
    for pshape in all_property_shapes(shapes):
        path = property_shape_path(shapes, pshape)
        if path is None:
            continue

        targets: Set[URIRef] = set()
        for disjoint_prop in disj.get(path, set()):
            targets.update(expand(disjoint_prop))

        for target in sorted(targets, key=str):
            if target == path:
                continue
            if (pshape, SH.disjoint, target) not in shapes:
                shapes.add((pshape, SH.disjoint, target))
                added += 1
    return added


def ensure_irreflexive_component(shapes: Graph) -> None:
    comp = ESH.IrreflexiveConstraintComponent
    param = ESH.IrreflexiveParameter
    validator = ESH.IrreflexivePropertyValidator

    shapes.add((comp, RDF.type, SH.ConstraintComponent))
    shapes.add((comp, SH.parameter, param))
    shapes.add((param, RDF.type, SH.Parameter))
    shapes.add((param, SH.path, ESH.isIrreflexive))
    shapes.add((param, SH.datatype, XSD.boolean))
    shapes.add((param, SH.name, Literal("is irreflexive")))
    shapes.add(
        (
            param,
            SH.description,
            Literal("When true, ensures a node does not point to itself via this property."),
        )
    )
    shapes.add((comp, SH.propertyValidator, validator))
    shapes.add((validator, RDF.type, SH.SPARQLSelectValidator))
    shapes.add(
        (
            validator,
            SH.message,
            Literal("Irreflexive violation: Node {$this} points to itself."),
        )
    )
    shapes.add(
        (
            validator,
            SH.select,
            Literal(
                """
SELECT $this ?value
WHERE {
    $this $PATH ?value .
    FILTER ($isIrreflexive = true && $this = ?value)
}
""",
            ),
        )
    )


def ensure_asymmetric_component(shapes: Graph) -> None:
    comp = ESH.AsymmetricConstraintComponent
    param = ESH.AsymmetricParameter
    validator = ESH.AsymmetricPropertyValidator

    shapes.add((comp, RDF.type, SH.ConstraintComponent))
    shapes.add((comp, SH.parameter, param))
    shapes.add((param, RDF.type, SH.Parameter))
    shapes.add((param, SH.path, ESH.isAsymmetric))
    shapes.add((param, SH.datatype, XSD.boolean))
    shapes.add((param, SH.name, Literal("is asymmetric")))
    shapes.add(
        (
            param,
            SH.description,
            Literal(
                "When true, ensures that if A points to B, B does not point back to A."
            ),
        )
    )
    shapes.add((comp, SH.propertyValidator, validator))
    shapes.add((validator, RDF.type, SH.SPARQLSelectValidator))
    shapes.add(
        (
            validator,
            SH.message,
            Literal("Asymmetric violation: Node {$this} and another node point to each other."),
        )
    )
    shapes.add(
        (
            validator,
            SH.select,
            Literal(
                """
SELECT $this ?value
WHERE {
    FILTER ($isAsymmetric = true)
    $this $PATH ?value .
    ?value $PATH $this .
}
""",
            ),
        )
    )


def mark_irreflexive_and_asymmetric_properties(ontology: Graph, shapes: Graph) -> Tuple[int, int]:
    ensure_irreflexive_component(shapes)
    ensure_asymmetric_component(shapes)

    irreflexive = {
        prop
        for prop in ontology.subjects(RDF.type, OWL.IrreflexiveProperty)
        if isinstance(prop, URIRef)
    }
    asymmetric = {
        prop
        for prop in ontology.subjects(RDF.type, OWL.AsymmetricProperty)
        if isinstance(prop, URIRef)
    }

    irref_added = 0
    asym_added = 0
    for pshape in all_property_shapes(shapes):
        path = property_shape_path(shapes, pshape)
        if path is None:
            continue
        if path in irreflexive and (pshape, ESH.isIrreflexive, Literal(True)) not in shapes:
            shapes.add((pshape, ESH.isIrreflexive, Literal(True)))
            irref_added += 1
        if path in asymmetric and (pshape, ESH.isAsymmetric, Literal(True)) not in shapes:
            shapes.add((pshape, ESH.isAsymmetric, Literal(True)))
            asym_added += 1

    return irref_added, asym_added


def remove_min_count(shapes: Graph) -> int:
    triples = list(shapes.triples((None, SH.minCount, None)))
    for triple in triples:
        shapes.remove(triple)
    return len(triples)


def add_multi_domain_subject_shapes(ontology: Graph, shapes: Graph) -> int:
    """Create SHACL NodeShapes for properties with conjunctive URI domains.

    For each property P that has multiple rdfs:domain class IRIs, create a
    shape that targets sh:targetSubjectsOf P and adds one sh:class per domain
    class. In SHACL, multiple sh:class constraints on a NodeShape are combined
    with logical AND.

    Blank-node domain expressions are ignored by design.
    """

    property_domains: Dict[URIRef, Set[URIRef]] = {}
    for prop, _, domain in ontology.triples((None, RDFS.domain, None)):
        if isinstance(prop, URIRef) and isinstance(domain, URIRef):
            property_domains.setdefault(prop, set()).add(domain)

    added = 0
    for prop, domains in sorted(property_domains.items(), key=lambda item: str(item[0])):
        if len(domains) < 2:
            continue

        shape_uri = stable_iri(ESH, "DomainConjunctionShape", prop)

        if (shape_uri, RDF.type, SH.NodeShape) not in shapes:
            shapes.add((shape_uri, RDF.type, SH.NodeShape))
            added += 1

        if (shape_uri, SH.targetSubjectsOf, prop) not in shapes:
            shapes.add((shape_uri, SH.targetSubjectsOf, prop))
            added += 1

        class_predicate = SH["class"]
        for domain_cls in sorted(domains, key=str):
            if (shape_uri, class_predicate, domain_cls) not in shapes:
                shapes.add((shape_uri, class_predicate, domain_cls))
                added += 1

        class_list = ", ".join(local_name(c) for c in sorted(domains, key=str))
        message = Literal(
            f"Any subject of {local_name(prop)} must be all of: {class_list}."
        )
        if (shape_uri, SH.message, message) not in shapes:
            shapes.add((shape_uri, SH.message, message))
            added += 1

    return added


def apply_all(ontology: Graph, shapes: Graph) -> Dict[str, int]:
    shapes.bind("esh", ESH)

    missing = ensure_minimal_missing_shapes(ontology, shapes)
    annotation_links = ensure_annotation_property_shapes(ontology, shapes)
    propagated = propagate_properties_across_non_disjoint_nodes(ontology, shapes)
    class_disjoint = transfer_class_disjointness(ontology, shapes)
    inferred_rules = add_superclass_inference_rules(ontology, shapes)
    prop_disjoint = enrich_property_disjointness(ontology, shapes)
    irref_added, asym_added = mark_irreflexive_and_asymmetric_properties(ontology, shapes)
    multi_domain_shape_terms = add_multi_domain_subject_shapes(ontology, shapes)
    removed_min_count = remove_min_count(shapes)

    return {
        "missing_shapes_added": len(missing),
        "annotation_links_added": annotation_links,
        "propagated_property_links_added": propagated,
        "class_disjoint_constraints_added": class_disjoint,
        "superclass_inference_rules_linked": inferred_rules,
        "property_disjoint_constraints_added": prop_disjoint,
        "irreflexive_flags_added": irref_added,
        "asymmetric_flags_added": asym_added,
        "multi_domain_subject_shape_terms_added": multi_domain_shape_terms,
        "min_count_removed": removed_min_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inject ontology-driven constraints into a SHACL shapes graph."
    )
    parser.add_argument("--ontology", required=True, help="Path to ontology file.")
    parser.add_argument("--shapes", required=True, help="Path to SHACL shapes file.")
    parser.add_argument("--output", required=True, help="Output path for updated SHACL.")
    parser.add_argument(
        "--ontology-format",
        default=None,
        help="Optional rdflib parser format for ontology.",
    )
    parser.add_argument(
        "--shapes-format",
        default=None,
        help="Optional rdflib parser format for shapes.",
    )
    parser.add_argument(
        "--output-format",
        default="turtle",
        help="Serialization format for output (default: turtle).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    ontology_path = Path(args.ontology)
    shapes_path = Path(args.shapes)
    output_path = Path(args.output)

    ontology = parse_graph(ontology_path, args.ontology_format)
    shapes = parse_graph(shapes_path, args.shapes_format)

    stats = apply_all(ontology, shapes)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shapes.serialize(destination=output_path.as_posix(), format=args.output_format)

    print("Constraint injection complete.")
    for key, value in stats.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()