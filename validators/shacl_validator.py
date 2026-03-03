"""
SHACL‑based validation of predicted KG triples against an OWL ontology.

Workflow
--------
1.  Parse the category's OWL/TTL ontology with rdflib.
2.  Generate SHACL shapes from domain/range declarations.
3.  Convert the LLM's predicted triples + entity‑type schemas into an
    instance RDF data graph.
4.  Run pyshacl and collect per‑entry violations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SH, XSD

from models.data_models import EntryExtractionResult, Triple, TripleSchema


# ── Namespace helpers ─────────────────────────────────────────────────────────

# Instance data will live under this namespace.
EX = Namespace("http://example.org/data/")

# Maps an rdfs:label string to the full URI seen in the ontology.
_LABEL_RE = re.compile(r'^[A-Za-z][A-Za-z0-9]*:(?!//)')


def _label_of(uri: URIRef) -> str:
    """Extract the local name / fragment from a URI."""
    s = str(uri)
    return s.rsplit("#", 1)[-1].rsplit("/", 1)[-1]


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class Violation:
    """A single SHACL violation mapped back to an entry + triple index."""
    entry_idx: int
    triple_idx: int
    focus_node: str
    property_path: Optional[str]
    constraint: str
    message: str


@dataclass
class ValidationReport:
    """Aggregated validation output for a whole batch."""
    conforms: bool
    violations: List[Violation] = field(default_factory=list)

    def entries_with_violations(self) -> List[int]:
        """Return sorted unique entry indices that have violations."""
        return sorted({v.entry_idx for v in self.violations})


# ── OWL → SHACL shape generator ──────────────────────────────────────────────

class ShaclShapeGenerator:
    """
    Reads an OWL/TTL ontology and produces SHACL NodeShapes that enforce
    domain/range type checking for every declared property.
    """

    def __init__(self, ontology_ttl: str):
        self.ont = Graph()
        self.ont.parse(data=ontology_ttl, format="turtle")
        # Build label→URI map for classes
        self._class_uris: Dict[str, URIRef] = {}
        for cls_uri in self.ont.subjects(RDF.type, OWL.Class):
            for label in self.ont.objects(cls_uri, RDFS.label):
                self._class_uris[str(label)] = URIRef(cls_uri)
        # Also include subclass hierarchy
        self._subclass_map: Dict[URIRef, set] = {}
        for sub, _, sup in self.ont.triples((None, RDFS.subClassOf, None)):
            self._subclass_map.setdefault(URIRef(sup), set()).add(URIRef(sub))

    def class_uri(self, label: str) -> Optional[URIRef]:
        """Resolve a class label to its full URI."""
        return self._class_uris.get(label)

    def all_subclasses(self, cls_uri: URIRef) -> set:
        """Transitively collect all subclasses of cls_uri (including itself)."""
        result = {cls_uri}
        queue = [cls_uri]
        while queue:
            cur = queue.pop()
            for child in self._subclass_map.get(cur, set()):
                if child not in result:
                    result.add(child)
                    queue.append(child)
        return result

    def generate_shapes(self) -> Graph:
        """
        Return a SHACL shapes graph.

        For each owl:ObjectProperty with domain D and range R we create a
        PropertyShape that requires sh:class R on nodes of type D.

        For each owl:DatatypeProperty with domain D and range R we create
        a PropertyShape with sh:datatype R on nodes of type D.
        """
        sg = Graph()
        sg.bind("sh", SH)
        sg.bind("ex", EX)

        # Collect all properties
        props = set()
        for p in self.ont.subjects(RDF.type, OWL.ObjectProperty):
            props.add(("object", URIRef(p)))
        for p in self.ont.subjects(RDF.type, OWL.DatatypeProperty):
            props.add(("datatype", URIRef(p)))

        # Group by domain class → list of property shapes
        domain_shapes: Dict[URIRef, List[Tuple[str, URIRef, URIRef]]] = {}
        for kind, prop_uri in props:
            domains = list(self.ont.objects(prop_uri, RDFS.domain))
            ranges = list(self.ont.objects(prop_uri, RDFS.range))
            if not domains or not ranges:
                continue
            for d in domains:
                for r in ranges:
                    domain_shapes.setdefault(URIRef(d), []).append(
                        (kind, URIRef(prop_uri), URIRef(r)))

        # Create one NodeShape per domain class
        for domain_cls, prop_list in domain_shapes.items():
            label = _label_of(domain_cls)
            shape_uri = URIRef(f"http://example.org/shapes/{label}Shape")
            sg.add((shape_uri, RDF.type, SH.NodeShape))
            # Target all instances of this class and its subclasses
            for cls in self.all_subclasses(domain_cls):
                sg.add((shape_uri, SH.targetClass, cls))

            for kind, prop_uri, range_uri in prop_list:
                ps = BNode()
                sg.add((shape_uri, SH.property, ps))
                sg.add((ps, SH.path, prop_uri))
                if kind == "object":
                    sg.add((ps, SH["class"], range_uri))
                else:
                    sg.add((ps, SH.datatype, range_uri))
                # Properties are optional (no minCount), so we only validate
                # type correctness when the property is present.
                sg.add((ps, SH.severity, SH.Violation))

        return sg


# ── Build instance data graph ─────────────────────────────────────────────────

def _safe_uri(name: str) -> URIRef:
    """Convert an entity name string into a safe URI."""
    safe = re.sub(r'[^A-Za-z0-9_\-.]', '_', name)
    return EX[safe]


def build_data_graph(
    entries: Dict[str, EntryExtractionResult],
    shape_gen: ShaclShapeGenerator,
) -> Tuple[Graph, Dict[URIRef, Tuple[int, int]]]:
    """
    Build an rdflib Graph of instance data from predicted triples + schemas.

    Returns:
        (data_graph, uri_map) where uri_map maps each triple's property‑usage
        URI to (entry_idx, triple_idx) so violations can be traced back.
    """
    g = Graph()
    g.bind("ex", EX)

    # We also need the ontology's property URIs – build a label→URI map
    prop_uris: Dict[str, URIRef] = {}
    for kind in (OWL.ObjectProperty, OWL.DatatypeProperty):
        for p in shape_gen.ont.subjects(RDF.type, kind):
            for lbl in shape_gen.ont.objects(p, RDFS.label):
                prop_uris[str(lbl)] = URIRef(p)

    triple_map: Dict[URIRef, Tuple[int, int]] = {}

    for entry_key, result in entries.items():
        entry_idx = int(entry_key.split("_")[1]) - 1  # entry_1 → 0

        for t_idx, (triple, schema) in enumerate(
            zip(result.triples, result.schemas)
        ):
            subj_uri = _safe_uri(triple.subject)
            obj_uri = _safe_uri(triple.object)

            # Add rdf:type for subject and object from schemas
            subj_cls = shape_gen.class_uri(schema.subject)
            obj_cls = shape_gen.class_uri(schema.object)

            if subj_cls:
                g.add((subj_uri, RDF.type, subj_cls))
            if obj_cls:
                g.add((obj_uri, RDF.type, obj_cls))

            # Add the property triple
            rel_uri = prop_uris.get(triple.relation)
            if rel_uri:
                # Check if this is a datatype property
                is_datatype = (rel_uri, RDF.type, OWL.DatatypeProperty) in shape_gen.ont
                if is_datatype:
                    # Determine the expected datatype from the ontology
                    ranges = list(shape_gen.ont.objects(rel_uri, RDFS.range))
                    dt = ranges[0] if ranges else XSD.string
                    g.add((subj_uri, rel_uri, Literal(triple.object, datatype=dt)))
                else:
                    g.add((subj_uri, rel_uri, obj_uri))

                # Store mapping so we can trace violations back
                # Use a unique blank‑node‑style key
                marker = URIRef(f"http://example.org/marker/e{entry_idx}_t{t_idx}")
                triple_map[marker] = (entry_idx, t_idx)
            # If relation not in ontology, skip (won't trigger SHACL since
            # there's no shape for it).

    return g, triple_map


# ── Run validation ────────────────────────────────────────────────────────────

def validate_batch(
    entries: Dict[str, EntryExtractionResult],
    ontology_ttl: str,
) -> ValidationReport:
    """
    Validate a batch of predicted triples against the category's OWL ontology.

    Steps:
      1. Generate SHACL shapes from the ontology.
      2. Build an instance data graph from predictions + schemas.
      3. Run pyshacl.
      4. Parse the results graph and map violations back to entry/triple indices.
    """
    from pyshacl import validate as py_validate

    shape_gen = ShaclShapeGenerator(ontology_ttl)
    shapes_graph = shape_gen.generate_shapes()
    data_graph, triple_map = build_data_graph(entries, shape_gen)

    if len(data_graph) == 0:
        return ValidationReport(conforms=True)

    conforms, results_graph, results_text = py_validate(
        data_graph,
        shacl_graph=shapes_graph,
        ont_graph=shape_gen.ont,
        inference="rdfs",
        abort_on_first=False,
    )

    violations: List[Violation] = []

    if not conforms:
        # Parse the results graph for violation details
        for result_node in results_graph.subjects(RDF.type, SH.ValidationResult):
            severity = results_graph.value(result_node, SH.resultSeverity)
            if severity and str(severity) != str(SH.Violation):
                continue

            focus = results_graph.value(result_node, SH.focusNode)
            path = results_graph.value(result_node, SH.resultPath)
            source = results_graph.value(result_node, SH.sourceConstraintComponent)
            value = results_graph.value(result_node, SH.value)
            messages = list(results_graph.objects(result_node, SH.resultMessage))

            # Map focus node back to entry/triple
            # The focus node is the subject URI — find which entries used it
            focus_str = _label_of(focus) if focus else "?"
            path_str = _label_of(path) if path else None
            constraint_str = _label_of(source) if source else "unknown"
            msg = str(messages[0]) if messages else f"{constraint_str} on {path_str}"

            # Find the entry + triple that produced this focus+path combo
            matched = False
            for entry_key, result in entries.items():
                entry_idx = int(entry_key.split("_")[1]) - 1
                for t_idx, triple in enumerate(result.triples):
                    subj_safe = re.sub(r'[^A-Za-z0-9_\-.]', '_', triple.subject)
                    if focus and subj_safe == _label_of(focus):
                        # Check if the path matches this triple's relation
                        if path_str and triple.relation == path_str:
                            violations.append(Violation(
                                entry_idx=entry_idx,
                                triple_idx=t_idx,
                                focus_node=focus_str,
                                property_path=path_str,
                                constraint=constraint_str,
                                message=msg,
                            ))
                            matched = True
                            break
                if matched:
                    break

            if not matched and focus:
                # Couldn't map precisely — attribute to first entry with this subject
                violations.append(Violation(
                    entry_idx=-1,
                    triple_idx=-1,
                    focus_node=focus_str,
                    property_path=path_str,
                    constraint=constraint_str,
                    message=msg,
                ))

    return ValidationReport(conforms=conforms, violations=violations)


# ── Format violations for the correction prompt ──────────────────────────────

def format_violations_for_prompt(
    entries_with_violations: Dict[int, List[Violation]],
    original_entries: list,
    original_results: Dict[str, EntryExtractionResult],
) -> str:
    """
    Build a human‑readable summary of SHACL violations keyed by entry,
    showing the original text, the LLM's previous triples, and what
    went wrong — ready to paste into a correction prompt.
    """
    parts = []
    for entry_idx in sorted(entries_with_violations):
        vs = entries_with_violations[entry_idx]
        entry = original_entries[entry_idx]
        key = f"entry_{entry_idx + 1}"
        prev = original_results.get(key)

        part = f"### entry_{entry_idx + 1}\n"
        part += f"Text: {entry.input_text}\n"
        part += "Your previous extraction:\n"
        if prev:
            for i, (t, s) in enumerate(zip(prev.triples, prev.schemas)):
                part += f"  triple {i+1}: ({t.subject}, {t.relation}, {t.object})  types: ({s.subject}, {s.object})\n"
        part += "SHACL violations found:\n"
        for v in vs:
            part += f"  - {v.message}\n"
        parts.append(part)

    return "\n".join(parts)
