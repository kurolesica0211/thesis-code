"""
SHACL‑based validation of predicted KG triples against an OWL ontology.

Workflow
--------
1.  Parse the category's OWL/TTL ontology with rdflib.
2.  Load pre‑generated SHACL shapes from a TTL file.
3.  Convert the LLM's predicted triples + entity‑type schemas into an
    instance RDF data graph.
4.  Run pyshacl and collect per‑entry violations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SH, XSD

from models.data_models import EntryExtractionResult


# ── Namespace helpers ─────────────────────────────────────────────────────────

# Instance data will live under this namespace.
EX = Namespace("http://example.org/data/")


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


# ── Ontology index (class / property URI lookups) ─────────────────────────────

class OntologyIndex:
    """
    Reads an OWL/TTL ontology and builds lookup maps for class and property
    URIs so that the data‑graph builder can resolve LLM‑produced labels to
    the correct ontology URIs.
    """

    def __init__(self, ontology_ttl: str):
        self.ont = Graph()
        self.ont.parse(data=ontology_ttl, format="turtle")
        # Build label→URI map for classes
        self._class_uris: Dict[str, URIRef] = {}
        for cls_uri in self.ont.subjects(RDF.type, OWL.Class):
            for label in self.ont.objects(cls_uri, RDFS.label):
                self._class_uris[str(label)] = URIRef(cls_uri)
            # Also index by URI local name (fragment / last path segment)
            # so that types like "فلم" (from http://dbpedia.org/ontology/فلم)
            # resolve even when the label is "Film".
            local = _label_of(URIRef(cls_uri))
            if local not in self._class_uris:
                self._class_uris[local] = URIRef(cls_uri)
            # And index by the full URI string itself
            self._class_uris[str(cls_uri)] = URIRef(cls_uri)

        # Build label→URI map for object/datatype properties
        self._prop_uris: Dict[str, URIRef] = {}
        for kind in (OWL.ObjectProperty, OWL.DatatypeProperty):
            for p in self.ont.subjects(RDF.type, kind):
                for lbl in self.ont.objects(p, RDFS.label):
                    self._prop_uris[str(lbl)] = URIRef(p)

    def class_uri(self, label: str) -> Optional[URIRef]:
        """Resolve a class label to its full URI."""
        return self._class_uris.get(label)

    def prop_uri(self, label: str) -> Optional[URIRef]:
        """Resolve a property label to its full URI."""
        return self._prop_uris.get(label)


# ── Build instance data graph ─────────────────────────────────────────────────

def _inject_superclasses(
    g: Graph, ont: Graph, subject: URIRef, cls: URIRef
) -> None:
    """Add all ancestor classes of cls (from the ontology) as rdf:type of subject."""
    for parent in ont.transitive_objects(cls, RDFS.subClassOf):
        if parent != cls:
            g.add((subject, RDF.type, parent))


def _safe_uri(name: str, entry_key: str = "") -> URIRef:
    """Convert an entity name string into a safe URI, scoped by entry_key."""
    safe = re.sub(r'[^A-Za-z0-9_\-.]', '_', name)
    if entry_key:
        safe = f"{entry_key}__{safe}"
    return EX[safe]


def build_data_graph(
    entries: Dict[str, EntryExtractionResult],
    ont_idx: OntologyIndex,
) -> Tuple[Graph, Dict[Tuple[URIRef, URIRef], List[Tuple[int, int]]]]:
    """
    Build an rdflib Graph of instance data from predicted triples + schemas.

    Returns:
        (data_graph, triple_map) where triple_map maps (subj_uri, rel_uri)
        to a list of (entry_idx, triple_idx) pairs.  The list handles the
        case where two triples in different entries share the same sanitised
        subject name and relation.
    """
    g = Graph()
    g.bind("ex", EX)

    # (subj_uri, rel_uri) → [(entry_idx, triple_idx), ...]
    triple_map: Dict[Tuple[URIRef, URIRef], List[Tuple[int, int]]] = {}

    for entry_key, result in entries.items():
        entry_idx = int(entry_key.split("_")[1]) - 1  # entry_1 → 0
        for t_idx, (triple, schema) in enumerate(
            zip(result.triples, result.schemas)
        ):
            subj_uri = _safe_uri(triple.subject, entry_key)

            # Always type the subject — it's an entity instance.
            subj_cls = ont_idx.class_uri(schema.subject) or EX[re.sub(r'[^A-Za-z0-9_]', '_', schema.subject)]
            g.add((subj_uri, RDF.type, subj_cls))
            _inject_superclasses(g, ont_idx.ont, subj_uri, subj_cls)

            # Resolve the property first to decide how to handle the object.
            rel_uri = ont_idx.prop_uri(triple.relation) or EX[re.sub(r'[^A-Za-z0-9_]', '_', triple.relation)]
            is_datatype = (rel_uri, RDF.type, OWL.DatatypeProperty) in ont_idx.ont

            if is_datatype:
                # Object is a literal value — no rdf:type needed.
                ranges = list(ont_idx.ont.objects(rel_uri, RDFS.range))
                dt = ranges[0] if ranges else XSD.string
                g.add((subj_uri, rel_uri, Literal(triple.object, datatype=dt)))
            else:
                # Object is an entity instance — type it.
                obj_uri = _safe_uri(triple.object, entry_key)
                obj_cls = ont_idx.class_uri(schema.object) or EX[re.sub(r'[^A-Za-z0-9_]', '_', schema.object)]
                g.add((obj_uri, RDF.type, obj_cls))
                _inject_superclasses(g, ont_idx.ont, obj_uri, obj_cls)
                g.add((subj_uri, rel_uri, obj_uri))

            triple_map.setdefault((subj_uri, rel_uri), []).append((entry_idx, t_idx))

    return g, triple_map


# ── Run validation ────────────────────────────────────────────────────────────

def validate_batch(
    entries: Dict[str, EntryExtractionResult],
    ontology_ttl: str,
    shacl_shapes_ttl: str,
) -> Tuple[ValidationReport, str, List[dict]]:
    """
    Validate a batch of predicted triples against the category's OWL ontology
    using pre‑generated SHACL shapes.

    Steps:
      1. Load pre‑generated SHACL shapes.
      2. Build an instance data graph from predictions + schemas.
      3. Run pyshacl.
      4. Parse the results graph and map violations back to entry/triple indices.
    """
    from pyshacl import validate as py_validate

    ont_idx = OntologyIndex(ontology_ttl)

    shapes_graph = Graph()
    shapes_graph.parse(data=shacl_shapes_ttl, format="turtle")

    data_graph, triple_map = build_data_graph(entries, ont_idx)

    if len(data_graph) == 0:
        return ValidationReport(conforms=True), "", []

    conforms, results_graph, results_text = py_validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="none",
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
            messages = list(results_graph.objects(result_node, SH.resultMessage))

            focus_str = _label_of(focus) if focus else "?"
            path_str = _label_of(path) if path else None
            constraint_str = _label_of(source) if source else "unknown"
            msg = str(messages[0]) if messages else f"{constraint_str} on {path_str}"

            # Direct lookup — (subj_uri, rel_uri) were recorded at graph-build time.
            # A key may map to multiple triples if the same entity name / relation
            # appears across different entries in the batch.
            matches = triple_map.get((focus, path), []) if (focus and path) else []
            if matches:
                for entry_idx, t_idx in matches:
                    violations.append(Violation(
                        entry_idx=entry_idx,
                        triple_idx=t_idx,
                        focus_node=focus_str,
                        property_path=path_str,
                        constraint=constraint_str,
                        message=msg,
                    ))
            else:
                # Violation on a node with no matching property triple
                # (e.g. sh:closed firing on an unexpected property).
                violations.append(Violation(
                    entry_idx=-1,
                    triple_idx=-1,
                    focus_node=focus_str,
                    property_path=path_str,
                    constraint=constraint_str,
                    message=msg,
                ))

    ttl = data_graph.serialize(format="turtle")
    tm_entries = [
        {"subj": str(k[0]), "prop": str(k[1]), "indices": v}
        for k, v in triple_map.items()
    ]
    return ValidationReport(conforms=conforms, violations=violations), ttl, tm_entries


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
        part += "Violated triples:\n"
        if prev:
            # Group violation messages by triple index
            by_triple: Dict[int, List[str]] = {}
            for v in vs:
                by_triple.setdefault(v.triple_idx, []).append(v.message)
            for t_idx, msgs in sorted(by_triple.items()):
                if 0 <= t_idx < len(prev.triples):
                    t = prev.triples[t_idx]
                    s = prev.schemas[t_idx]
                    part += f"  triple {t_idx + 1}: ({t.subject}, {t.relation}, {t.object})  types: ({s.subject}, {s.object})\n"
                    for m in msgs:
                        part += f"    violation: {m}\n"
        parts.append(part)

    return "\n".join(parts)
