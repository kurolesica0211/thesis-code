import os
from typing import List, Dict, Set, Tuple
from collections import defaultdict
from collections.abc import Generator
from rdflib import BNode, Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from models.data_models import TaskEntry, Schema, RelationDef, DataEntry
    

class Loader:
    """
    Base loader for all datasets.
    
    Expects:
    - Text file(s) containing natural language descriptions
    - Files with ontolog(y/ies)
    - SHACL shapes files
    """

    def __init__(
        self,
        input_entries: List[DataEntry]
    ):
        """
        Args:
            input_entries: a list of DataEntry dictionaries, each representing a set of paths to text files under one ontology
        """
        self.input_entries: List[DataEntry] = input_entries

    def load(self) -> Generator[TaskEntry, None, None]:
        for entry in self.input_entries:
            schema, ont_graph = Loader._load_ontology(entry.ontology_filepath)
            shacl_graph       = Loader._load_graph(entry.shacl_filepath)
            data_graph        = Loader._load_data_graph(entry.data_graph_path, ont_graph.namespaces())
            
            for text_path, gt_path in zip(entry.text_filepaths, entry.gold_triples_filepaths):
                text = Loader._load_input_text(text_path)
                gt_graph = Loader._load_gold_triples(gt_path) if gt_path is not None else None
                
                task_entry = TaskEntry(
                    entry_id=entry.entry_id,
                    input_text=text,
                    gold_triples_graph=gt_graph,
                    ontology_graph=ont_graph,
                    shacl_graph=shacl_graph,
                    schema_def=schema,
                    data_graph=data_graph
                )
            
                yield task_entry
    
    def get_total(self) -> int:
        """Get total number of task entries"""
        return sum([len(entry.text_filepaths) for entry in self.input_entries])
    
    @staticmethod
    def _load_input_text(path: str) -> str:
        with open(path, "r") as f:
            text = f.read()
        return text
    
    @staticmethod
    def _load_gold_triples(path: str) -> Graph:
        #TODO: implement when new datasets come
        pass
    
    @staticmethod
    def _load_graph(path: str) -> Graph:
        graph = Graph()
        graph.parse(path)
        return graph
    
    @staticmethod
    def _load_data_graph(path: str | None, namespaces: Generator[Tuple[str, URIRef], None, None]) -> Graph:
        """Load a data graph, if not None, else create an empty graph with the ontology's namespaces."""
        if path is not None:
            return Loader._load_graph(path)
        else:
            graph = Graph()
            for prefix, namespace in namespaces:
                graph.bind(prefix, namespace)
            graph.bind("data", URIRef("http://example.org/data/"))
            return graph
            

    @staticmethod
    def _load_ontology(path: str) -> Tuple[Schema, Graph]:
        """Parse an ontology, and extract schema (entities and relations)."""
        graph = Graph()
        graph.parse(path)

        def _to_label(node) -> str | None:
            """Convert RDF node to compact label, skipping blank nodes."""
            if isinstance(node, BNode):
                return None
            return node.n3(graph.namespace_manager)

        entities = set()

        # Extract all classes with their labels
        for cls_uri in graph.subjects(RDF.type, OWL.Class):
            cls_label = _to_label(cls_uri)
            if cls_label is None:
                continue
            entities.add(cls_label)

        # Build class hierarchy for transitive closure
        hierarchy = defaultdict(list)
        for subclass_uri, superclass_uri in graph.subject_objects(RDFS.subClassOf):
            subclass = _to_label(subclass_uri)
            superclass = _to_label(superclass_uri)
            if subclass is None or superclass is None:
                continue
            hierarchy[superclass].append(subclass)
            entities.add(subclass)
            entities.add(superclass)

        def get_all_subclasses(cls: str) -> Set[str]:
            """Get all subclasses (including the class itself) via transitive closure."""
            subclasses = set([cls])
            stack = [cls]
            while stack:
                current = stack.pop()
                for child in hierarchy.get(current, []):
                    if child not in subclasses:
                        subclasses.add(child)
                        stack.append(child)
            return subclasses

        # Extract all object and datatype properties
        relations = []
        prop_nodes = set(graph.subjects(RDF.type, OWL.ObjectProperty))
        prop_nodes.update(graph.subjects(RDF.type, OWL.DatatypeProperty))

        for prop_uri in sorted(prop_nodes, key=str):
            rel_label = prop_uri.n3(graph.namespace_manager)

            # Get domain and range
            domains = {
                label
                for domain in graph.objects(prop_uri, RDFS.domain)
                for label in [_to_label(domain)]
                if label is not None
            }
            ranges = {
                label
                for range_ in graph.objects(prop_uri, RDFS.range)
                for label in [_to_label(range_)]
                if label is not None
            }

            entities.update(domains)
            entities.update(ranges)

            # Compute transitive closure for valid subjects and objects
            valid_subjects = set()
            for domain in domains:
                valid_subjects.update(get_all_subclasses(domain))

            valid_objects = set()
            for range_ in ranges:
                valid_objects.update(get_all_subclasses(range_))

            relations.append(RelationDef(
                relation=rel_label,
                valid_subjects=sorted(valid_subjects),
                valid_objects=sorted(valid_objects)
            ))

        return Schema(
            entities=sorted(list(entities)),
            relations=relations
        ), graph
