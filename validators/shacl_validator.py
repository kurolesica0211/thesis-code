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
_NS_PREFIX_RE = re.compile(r'^[A-Za-z][A-Za-z0-9]*:(?!//)')
_ENTRY_PREFIX_RE = re.compile(r'^(?:entry_\d+__)+')


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
    value_node: Optional[str]
    constraint: str
    source_shape: Optional[URIRef]
    message: str


@dataclass
class ValidationReport:
    """Aggregated validation output for a whole batch."""
    conforms: bool
    violations: List[Violation] = field(default_factory=list)

    def entries_with_violations(self) -> List[int]:
        """Return sorted unique entry indices that have violations."""
        return sorted({v.entry_idx for v in self.violations})
    
    def group_violations_by_entry(self) -> Dict[int, List[Violation]]:
        """Group violations by entry index."""
        by_entry: Dict[int, List[Violation]] = {}
        for v in self.violations:
            by_entry.setdefault(v.entry_idx, []).append(v)
        return by_entry


# ── Ontology index (class / property URI lookups) ─────────────────────────────

class OntologyIndex:
    """
    Reads an OWL/TTL ontology and builds lookup maps for class and property
    URIs so that the data‑graph builder can resolve LLM‑produced labels to
    the correct ontology URIs.
    """

    def __init__(self, ontology: str, ontology_format: Literal["turtle", "xml"] = "turtle"):
        self.ont = Graph()
        self.ont.parse(data=ontology, format=ontology_format)
        # Build label→URI map for classes
        self._class_uris: Dict[str, URIRef] = {}
        for cls_uri in self.ont.subjects(RDF.type, OWL.Class):
            for label in self.ont.objects(cls_uri, RDFS.label):
                self._class_uris[str(label)] = URIRef(cls_uri)
            # Also index by URI local name (fragment / last path segment)
            local = _label_of(URIRef(cls_uri))
            if local not in self._class_uris:
                self._class_uris[local] = URIRef(cls_uri)
            # And index by the full URI string itself
            self._class_uris[str(cls_uri)] = URIRef(cls_uri)

        # Build label→URI map for object/datatype properties
        self._prop_uris: Dict[str, URIRef] = {}
        for kind in (OWL.ObjectProperty, OWL.DatatypeProperty):
            for p in self.ont.subjects(RDF.type, kind):
                prop_uri = URIRef(p)
                for lbl in self.ont.objects(p, RDFS.label):
                    self._prop_uris[str(lbl)] = prop_uri
                local = _label_of(prop_uri)
                if local not in self._prop_uris:
                    self._prop_uris[local] = prop_uri
                self._prop_uris[str(prop_uri)] = prop_uri

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
        if parent != cls and isinstance(parent, URIRef):
            g.add((subject, RDF.type, parent))


def _resolve_class_uri(ont_idx: OntologyIndex, raw_label: str) -> URIRef:
    """Resolve class URI from possibly noisy LLM label; fallback to DomainEntity."""
    token = _NS_PREFIX_RE.sub("", str(raw_label))
    token = _ENTRY_PREFIX_RE.sub("", token)
    cls_uri = ont_idx.class_uri(token)
    if cls_uri is not None:
        return cls_uri

    domain_entity = ont_idx.class_uri("DomainEntity")
    if domain_entity is not None:
        return domain_entity

    return EX["DomainEntity"]


def _resolve_prop_uri(ont_idx: OntologyIndex, raw_label: str) -> URIRef:
    """Resolve property URI from possibly noisy LLM label; fallback to EX namespace."""
    token = _NS_PREFIX_RE.sub("", str(raw_label))
    if token.startswith("ex_"):
        token = token[3:]
    token = _ENTRY_PREFIX_RE.sub("", token)

    prop_uri = ont_idx.prop_uri(token) or ont_idx.prop_uri(str(raw_label))
    if prop_uri is not None:
        return prop_uri

    return EX[re.sub(r'[^A-Za-z0-9_]', '_', token)]


def _safe_uri(name: str, entry_key: str = "") -> URIRef:
    """Convert an entity name string into a safe URI, scoped by entry_key."""
    normalized = _NS_PREFIX_RE.sub("", str(name))
    if normalized.startswith("ex_"):
        normalized = normalized[3:]
    normalized = _ENTRY_PREFIX_RE.sub("", normalized)

    safe = re.sub(r'[^A-Za-z0-9_\-.]', '_', normalized)
    if entry_key:
        safe = f"{entry_key}__{safe}"
    return EX[safe]

def _key_of(label: str) -> int:
    return int(label.split("__")[0].split("_")[1]) - 1  # entry_1__Entity → 0


def build_data_graph(
    entries: Dict[str, EntryExtractionResult],
    ont_idx: OntologyIndex,
) -> Tuple[Graph, Dict[Tuple[URIRef, URIRef, object], List[Tuple[int, int]]]]:
    """
    Build an rdflib Graph of instance data from predicted triples + schemas.

    Returns:
        (data_graph, triple_map) where triple_map maps (subj_uri, rel_uri, obj_value)
        to a list of (entry_idx, triple_idx) pairs.  The list handles the
        case where two triples in different entries share the same sanitised
        subject name and relation.
    """
    g = Graph()
    g.bind("ex", EX)

    # (subj_uri, rel_uri, obj_value) → [(entry_idx, triple_idx), ...]
    triple_map: Dict[Tuple[URIRef, URIRef, object], List[Tuple[int, int]]] = {}

    for entry_key, result in entries.items():
        entry_idx = int(entry_key.split("_")[1]) - 1  # entry_1 → 0
        for t_idx, (triple, schema) in enumerate(
            zip(result.triples, result.schemas)
        ):
            subj_uri = _safe_uri(triple.subject, entry_key)

            # Always type the subject — it's an entity instance.
            subj_cls = _resolve_class_uri(ont_idx, schema.subject)
            g.add((subj_uri, RDF.type, subj_cls))
            _inject_superclasses(g, ont_idx.ont, subj_uri, subj_cls)

            # Resolve the property first to decide how to handle the object.
            rel_uri = _resolve_prop_uri(ont_idx, triple.relation)
            is_datatype = (rel_uri, RDF.type, OWL.DatatypeProperty) in ont_idx.ont

            if is_datatype:
                # Object is a literal value — no rdf:type needed.
                ranges = list(ont_idx.ont.objects(rel_uri, RDFS.range))
                dt = ranges[0] if ranges else XSD.string
                obj_value = Literal(triple.object, datatype=dt)
                g.add((subj_uri, rel_uri, obj_value))
            else:
                # Object is an entity instance — type it.
                obj_uri = _safe_uri(triple.object, entry_key)
                obj_cls = _resolve_class_uri(ont_idx, schema.object)
                g.add((obj_uri, RDF.type, obj_cls))
                _inject_superclasses(g, ont_idx.ont, obj_uri, obj_cls)
                g.add((subj_uri, rel_uri, obj_uri))
                obj_value = obj_uri

            triple_map.setdefault((subj_uri, rel_uri, obj_value), []).append((entry_idx, t_idx))

    return g, triple_map


# ── Run validation ────────────────────────────────────────────────────────────

def validate_batch(
    entries: Dict[str, EntryExtractionResult],
    ontology: str,
    shacl_shapes_ttl: str,
    ontology_format: Literal["turtle", "xml"] = "turtle",
) -> Tuple[ValidationReport, Graph, str, List[dict]]:
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

    ont_idx = OntologyIndex(ontology, ontology_format)

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
            value = results_graph.value(result_node, SH.value)
            source = results_graph.value(result_node, SH.sourceConstraintComponent)
            source_shape = results_graph.value(result_node, SH.sourceShape)
            if "http" not in str(source_shape):
                source_shape = None
            messages = list(results_graph.objects(result_node, SH.resultMessage))

            focus_str = _label_of(focus) if focus else "?"
            value_str = _label_of(value) if value is not None else None
            entry_idx = _key_of(focus_str) if focus else -1
            path_str = _label_of(path) if path else None
            constraint_str = _label_of(source) if source else "unknown"
            msg = str(messages[0]) if messages else f"{constraint_str} on {path_str}"

            matches = (
                triple_map.get((focus, path, value), [])
                if (focus and path and value is not None)
                else []
            )
            if matches:
                for _, t_idx in matches:
                    violations.append(Violation(
                        entry_idx=entry_idx,
                        triple_idx=t_idx,
                        focus_node=focus_str,
                        property_path=path_str,
                        value_node=value_str,
                        constraint=constraint_str,
                        source_shape=source_shape if source_shape else None,
                        message=msg,
                    ))
            else:
                # Violation on a node with no matching property triple
                # (e.g. sh:closed firing on an unexpected property).
                violations.append(Violation(
                    entry_idx=entry_idx,
                    triple_idx=-1,
                    focus_node=focus_str,
                    property_path=path_str,
                    value_node=value_str,
                    constraint=constraint_str,
                    source_shape=source_shape if source_shape else None,
                    message=msg,
                ))

    ttl = data_graph.serialize(format="turtle")
    tm_entries = [
        {"subj": str(k[0]), "prop": str(k[1]), "obj": str(k[2]), "indices": v}
        for k, v in triple_map.items()
    ]
    return ValidationReport(conforms=conforms, violations=violations), shapes_graph, ttl, tm_entries


# ── Format violations for the correction prompt ──────────────────────────────

def serialize_shape(graph: Graph, shape_uri: URIRef) -> str:
    mini_graph = graph.cbd(shape_uri)
    serialized_cleaned = re.sub(r'@prefix.*\n|@base.*\n', '', mini_graph.serialize(format="turtle")).strip()
    return serialized_cleaned

def format_violations_for_prompt(
    violations_by_entry: Dict[int, List[Violation]],
    original_entries: list,
    original_results: Dict[str, EntryExtractionResult],
    shapes_graph: Graph,
) -> str:
    """
    Build a human‑readable summary of SHACL violations keyed by entry,
    showing the original text, the LLM's previous triples, and what
    went wrong — ready to paste into a correction prompt.
    """
    parts = []
    
    for entry_idx in sorted(violations_by_entry):
        vs = violations_by_entry[entry_idx]
        entry = original_entries[entry_idx]
        key = f"entry_{entry_idx + 1}"
        prev = original_results.get(key)

        part = f"### entry_{entry_idx + 1}\n"
        part += f"Text: {entry.input_text}\n"
        part += "Violations summary:\n"
        part += f"- Total violations: {len(vs)}\n"
        part += "- Expected correction items: roughly one triple per violation item below (you may satisfy multiple items with one triple only if it is explicitly valid to do so).\n"
        part += "Correction items:\n"
        if prev:
            # Group violation objects by triple index
            by_triple: Dict[int, List[Violation]] = {}
            for v in vs:
                by_triple.setdefault(v.triple_idx, []).append(v)

            item_counter = 1
                
            for t_idx, grouped_violations in sorted(by_triple.items()):
                if t_idx < len(prev.triples):
                    if t_idx > -1:
                        t = prev.triples[t_idx]
                        s = prev.schemas[t_idx]
                        part += f"\nTarget triple index {t_idx} (existing triple to edit):\n"
                        part += f"- Current triple: ({t.subject}, {t.relation}, {t.object})\n"
                        part += f"- Current schema types: ({s.subject}, {s.object})\n"
                    else:
                        part += "\nTarget triple index -1 (no matching existing triple):\n"
                        part += "- You likely need to ADD new triple(s).\n"

                    for v in grouped_violations:
                        part += f"\n  [{item_counter}] Correction item\n"
                        part += f"  - focus node: {v.focus_node}\n"
                        part += f"  - property path: {v.property_path or 'unknown'}\n"
                        part += f"  - value: {v.value_node if v.value_node is not None else 'N/A (missing value violation)'}\n"
                        part += f"  - constraint: {v.constraint}\n"
                        part += f"  - violation: {v.message}\n"
                        if v.source_shape:
                            shape_ttl = serialize_shape(shapes_graph, v.source_shape)
                            part += f"  - source shape:\n\n    {shape_ttl}\n\n"
                        item_counter += 1
                else:
                    raise ValueError(f"Unexpected triple index {t_idx} in violation for entry_{entry_idx + 1}")
        parts.append(part)

    return "\n".join(parts)
