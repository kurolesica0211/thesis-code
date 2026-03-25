import os
from typing import List, Dict, Set, Optional
from collections import defaultdict
from rdflib import Graph
from rdflib.namespace import OWL, RDF, RDFS
from models.data_models import TaskEntry, Schema, RelationDef, CategoryBatch
from loaders.base_loader import BaseLoader


class CustomFamilyBenchLoader(BaseLoader):
    """
    Loader for the custom_family_bench dataset.
    
    Expects:
    - Text file(s) containing natural language descriptions
    - OWL ontology file defining classes and relations
    - SHACL shapes file (for reference, not used in loading)
    
    Creates TaskEntry objects with:
    - input_text from the full text file content
    - gold_triples = [] (no gold standard)
    - schema_def extracted from OWL ontology
    """

    def __init__(
        self,
        input_text_file: str,
        ontology_file: str,
        shacl_file: str = None,
    ):
        """
        Args:
            data_dir: Directory containing text files (e.g., 'custom_family_bench')
            ontology_file: OWL ontology file path (e.g., 'custom_family_bench/family_TBOX.owl')
            shacl_file: SHACL shapes file path (optional, for reference)
            input_text_file: Optional explicit text file path to load as input
        """
        self.ontology_file = ontology_file
        self.shacl_file = shacl_file
        self.input_text_file = input_text_file
        self.schema_def = None
        self._load_ontology()

    def _load_ontology(self):
        """Parse OWL ontology and extract schema (entities and relations)."""
        graph = Graph()
        graph.parse(self.ontology_file, format="xml")

        class_labels: Dict[str, str] = {}
        entities = set()

        # Extract all classes with their labels
        for cls_uri in graph.subjects(RDF.type, OWL.Class):
            label_obj = next(graph.objects(cls_uri, RDFS.label), None)
            cls_label = str(label_obj) if label_obj is not None else self._local_name(str(cls_uri))
            class_labels[str(cls_uri)] = cls_label
            entities.add(cls_label)

        def node_to_label(node) -> str:
            """Convert a node URI to its label."""
            node_str = str(node)
            if node_str in class_labels:
                return class_labels[node_str]
            return self._local_name(node_str)

        # Build class hierarchy for transitive closure
        hierarchy = defaultdict(list)
        for subclass_uri, superclass_uri in graph.subject_objects(RDFS.subClassOf):
            subclass = node_to_label(subclass_uri)
            superclass = node_to_label(superclass_uri)
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
            rel_label = next(graph.objects(prop_uri, RDFS.label), None)
            rel_id = str(rel_label) if rel_label is not None else self._local_name(str(prop_uri))

            # Get domain and range
            domains = {node_to_label(domain) for domain in graph.objects(prop_uri, RDFS.domain)}
            ranges = {node_to_label(range_) for range_ in graph.objects(prop_uri, RDFS.range)}

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
                relation=rel_id,
                valid_subjects=sorted(valid_subjects),
                valid_objects=sorted(valid_objects)
            ))

        self.schema_def = Schema(
            entities=sorted(list(entities)),
            relations=relations
        )

    def _local_name(self, uri: str) -> str:
        """Extract local name from URI."""
        return uri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]

    def load(self) -> List[TaskEntry]:
        """Load text entries from text files in data_dir."""
        entries = []
        entry_counter = 0

        filepath = self.input_text_file

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

            # Treat the entire file content as a single entry
            content = content.strip()

            if content:
                entry_id = f"family_{entry_counter}"
                entries.append(TaskEntry(
                    entry_id=entry_id,
                    input_text=content,
                    gold_triples=[],  # No gold triples provided
                    schema_def=self.schema_def
                ))
                entry_counter += 1

        return entries

    def load_by_category(self) -> List[CategoryBatch]:
        """
        Load all entries and group into a single category.
        
        Since this dataset doesn't have multiple categories, all entries
        are grouped under a single "family" category.
        """
        entries = self.load()

        # Single category for this dataset
        category_batch = CategoryBatch(
            category="family",
            schema_def=self.schema_def,
            entries=entries
        )

        return [category_batch]
