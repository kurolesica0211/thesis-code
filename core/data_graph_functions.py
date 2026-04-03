from rdflib import Graph, RDF, URIRef

from helpers import strip_ns, strip_uri


def create_safe_uri(graph: Graph, prefix: str, local_name: str) -> URIRef:
    nm = graph.namespace_manager
    
    base_uri = nm.store.namespace(prefix)
    
    if base_uri is None:
        raise ValueError(f"Prefix '{prefix}' is not defined in the graph headers.")
    
    return URIRef(f"{base_uri}{local_name}")


def add_class(data_graph: Graph, subject: str, type: str) -> Graph:
    """Adds a triple ``(subject, RDF.type, type)`` to the graph.\n
    Assumes ``data`` namespace exists in the graph.\n
    Assumes that the type is of format ``namespace:local_name``."""
    
    subject = strip_ns(strip_uri(subject))
    subj_uri = create_safe_uri(data_graph, "data", subject)
    class_uri = create_safe_uri(data_graph, *type.split(":"))
    
    updated_graph = data_graph.add((subj_uri, RDF.type, class_uri))
    
    return updated_graph


def remove_class(data_graph: Graph, subject: str, type: str) -> Graph:
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


def extract_classes(data_graph: Graph, uri: URIRef) -> list[URIRef]:
    cls_uris = data_graph.objects(uri, RDF.type)
    return list(cls_uris)