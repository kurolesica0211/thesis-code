import re
from urllib.parse import quote
from enum import Enum
from rdflib import Graph, RDF, URIRef, BNode, XSD, Literal
import logging, traceback

from helpers import strip_ns, strip_uri


def _sanitize_local_name(local_name: str) -> str:
    """Normalize and escape a URI local name so it is safe to concatenate."""
    cleaned = str(local_name).strip().strip("<>")
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = cleaned.replace(":", "_").replace("/", "_").replace("#", "_")
    cleaned = cleaned.strip("._")

    if not cleaned:
        raise ValueError(f"Invalid local name: {local_name!r}")

    return quote(cleaned, safe="-._~%")


def create_safe_uri(graph: Graph, prefix: str, local_name: str) -> URIRef:
    nm = graph.namespace_manager
    
    base_uri = nm.store.namespace(prefix)
    
    if base_uri is None:
        raise ValueError(f"Prefix '{prefix}' is not defined in the graph headers.")

    safe_local_name = _sanitize_local_name(local_name)
    return URIRef(f"{base_uri}{safe_local_name}")


def assign_class(data_graph: Graph, subject: str, type: str) -> Graph:
    """Adds a triple ``(subject, RDF.type, type)`` to the graph.\n
    Assumes ``data`` namespace exists in the graph.\n
    Assumes that the type is of format ``namespace:local_name``."""
    
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    class_uri = create_safe_uri(data_graph, *type.split(":"))
    
    updated_graph = data_graph.add((subj_uri, RDF.type, class_uri))
    
    return updated_graph


def unassign_class(data_graph: Graph, subject: str, type: str) -> Graph:
    """Removes a triple ``(subject, RDF.type, type)`` from the graph.\n
    Assumes ``data`` namespace exists in the graph.\n
    Assumes that the type is of format ``namespace:local_name``."""
    
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    class_uri = create_safe_uri(data_graph, *type.split(":"))
    
    updated_graph = data_graph.remove((subj_uri, RDF.type, class_uri))
    
    return updated_graph


def add_triple(data_graph: Graph, subject: str, relation: str, object: str) -> Graph:
    """Adds a triple ``(subject, relation, object) to the ``data_graph``.\n
    Assumes the graph has ``data`` namespace defined.\n
    Assumes the ``relation`` is of ``namespace:local_name`` format."""
    
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    object = strip_ns(strip_uri(object))
    #TODO: account for literals here
    obj_uri = create_safe_uri(data_graph, "data", object)
    rel_uri = create_safe_uri(data_graph, *relation.split(":"))
    
    updated_graph = data_graph.add((subj_uri, rel_uri, obj_uri))
    
    return updated_graph


def remove_triple(data_graph: Graph, subject: str, relation: str, object: str) -> Graph:
    """Removes a triple ``(subject, relation, object) to the ``data_graph``.\n
    Assumes the graph has ``data`` namespace defined.\n
    Assumes the ``relation`` is of ``namespace:local_name`` format."""
    
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    object = strip_ns(strip_uri(object))
    obj_uri = create_safe_uri(data_graph, "data", object)
    rel_uri = create_safe_uri(data_graph, *relation.split(":"))
    
    updated_graph = data_graph.remove((subj_uri, rel_uri, obj_uri))
    
    return updated_graph


def check_ents_typed(data_graph: Graph) -> list[URIRef]:
    all_nodes = set(s for s in data_graph.subjects() if isinstance(s, (URIRef, BNode)))
    all_nodes.update(o for o in data_graph.objects() if isinstance(o, (URIRef, BNode)))
    typed_nodes = set(data_graph.subjects(predicate=RDF.type))
    classes = set(data_graph.objects(predicate=RDF.type))
    classless_nodes = all_nodes - typed_nodes - classes
    return classless_nodes


def extract_classes(data_graph: Graph, uri: URIRef) -> list[URIRef]:
    cls_uris = data_graph.objects(uri, RDF.type)
    return list(cls_uris)


literals = {name: getattr(XSD, name) for (name, _) in vars(XSD)["__annotations__"].items() if re.match("[a-z][a-zA-Z]*", name)}
GraphLiterals = Enum("GraphLiterals", literals)

class RdfLibExceptionCapture(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.WARNING)
        self.last_exception_line = None
        self.last_record_message = None

    def emit(self, record):
        # First line logged by rdflib (without traceback)
        self.last_record_message = record.getMessage()

        # Actual exception attached by logger.exception(...)
        if record.exc_info:
            exc_type, exc, _ = record.exc_info
            self.last_exception_line = traceback.format_exception_only(exc_type, exc)[-1].strip()

def make_literal_and_extract_error(value: str, datatype) -> tuple[Literal, str]:
    logger = logging.getLogger("rdflib.term")
    capture = RdfLibExceptionCapture()

    old_level = logger.level
    old_propagate = logger.propagate
    logger.setLevel(logging.WARNING)
    logger.propagate = False
    logger.addHandler(capture)

    try:
        lit = Literal(value, datatype=datatype)
    finally:
        logger.removeHandler(capture)
        logger.setLevel(old_level)
        logger.propagate = old_propagate

    # Example: "ValueError: day is out of range for month"
    return lit, capture.last_exception_line


def add_literal(
    data_graph: Graph,
    subject: str,
    relation: str,
    lit_value: str,
    lit_type: str
) -> tuple[bool, Graph, str]:
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    rel_uri = create_safe_uri(data_graph, *relation.split(":"))
    lit_uri = create_safe_uri(data_graph, *lit_type.split(":"))
    lit, err_msg = make_literal_and_extract_error(lit_value, lit_uri)
    
    parsed = getattr(lit, "ill_typed", False) == False
    if parsed == False:
        return parsed, data_graph, err_msg
    
    updated_graph = data_graph.add((subj_uri, rel_uri, lit))
    
    return parsed, updated_graph, ""

def remove_literal(
    data_graph: Graph,
    subject: str,
    relation: str,
    lit_value: str,
    lit_type: str
) -> tuple[bool, Graph, str]:
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    rel_uri = create_safe_uri(data_graph, *relation.split(":"))
    lit_uri = create_safe_uri(data_graph, *lit_type.split(":"))
    lit, err_msg = make_literal_and_extract_error(lit_value, lit_uri)
    
    parsed = getattr(lit, "ill_typed", False) == False
    if parsed == False:
        return parsed, data_graph, err_msg
    
    updated_graph = data_graph.remove((subj_uri, rel_uri, lit))
    
    return parsed, updated_graph, ""