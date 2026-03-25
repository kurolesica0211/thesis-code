import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Set
from collections import defaultdict, OrderedDict
from rdflib import Graph
from rdflib.namespace import OWL, RDF, RDFS, XSD
from models.data_models import TaskEntry, Triple, Schema, RelationDef, CategoryBatch
from loaders.base_loader import BaseLoader

class OSKGCLoader(BaseLoader):
    def __init__(self, data_dir: str, ontology_dir: str, split: str = "test"):
        self.data_dir = os.path.join(data_dir, split)
        self.ontology_dir = ontology_dir
        self.ontologies = {}
        self._load_ontologies()

    def _load_ontologies(self):
        rdf_dir = self.ontology_dir
        nested_rdf_dir = os.path.join(self.ontology_dir, "rdf")
        sibling_rdf_dir = os.path.join(os.path.dirname(self.ontology_dir), "rdf")

        if os.path.isdir(nested_rdf_dir):
            rdf_dir = nested_rdf_dir
        elif os.path.isdir(sibling_rdf_dir):
            rdf_dir = sibling_rdf_dir

        datatype_map = {
            str(XSD.decimal): "number",
            str(XSD.integer): "number",
            str(XSD.float): "number",
            str(XSD.double): "number",
            str(XSD.gYear): "Year",
        }

        def local_name(uri: str) -> str:
            return uri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]

        for filename in sorted(os.listdir(rdf_dir)):
            if not filename.endswith(".ttl"):
                continue

            filepath = os.path.join(rdf_dir, filename)
            graph = Graph()
            graph.parse(filepath, format="turtle")

            category = os.path.splitext(filename)[0]
            ontology_subject = next(graph.subjects(RDF.type, OWL.Ontology), None)
            if ontology_subject is not None:
                ontology_label = next(graph.objects(ontology_subject, RDFS.label), None)
                if ontology_label is not None:
                    category = str(ontology_label)

            class_labels: Dict[str, str] = {}
            entities = set()
            for cls_uri in graph.subjects(RDF.type, OWL.Class):
                label_obj = next(graph.objects(cls_uri, RDFS.label), None)
                cls_label = str(label_obj) if label_obj is not None else local_name(str(cls_uri))
                class_labels[str(cls_uri)] = cls_label
                entities.add(cls_label)

            def node_to_label(node) -> str:
                node_str = str(node)
                if node_str in class_labels:
                    return class_labels[node_str]
                if node_str in datatype_map:
                    return datatype_map[node_str]
                return local_name(node_str)

            hierarchy = defaultdict(list)
            for subclass_uri, superclass_uri in graph.subject_objects(RDFS.subClassOf):
                subclass = node_to_label(subclass_uri)
                superclass = node_to_label(superclass_uri)
                hierarchy[superclass].append(subclass)
                entities.add(subclass)
                entities.add(superclass)

            def get_all_subclasses(cls: str) -> Set[str]:
                subclasses = set([cls])
                stack = [cls]
                while stack:
                    current = stack.pop()
                    for child in hierarchy.get(current, []):
                        if child not in subclasses:
                            subclasses.add(child)
                            stack.append(child)
                return subclasses

            relations = []
            prop_nodes = set(graph.subjects(RDF.type, OWL.ObjectProperty))
            prop_nodes.update(graph.subjects(RDF.type, OWL.DatatypeProperty))

            for prop_uri in sorted(prop_nodes, key=str):
                rel_label = next(graph.objects(prop_uri, RDFS.label), None)
                rel_id = str(rel_label) if rel_label is not None else local_name(str(prop_uri))

                domains = {node_to_label(domain) for domain in graph.objects(prop_uri, RDFS.domain)}
                ranges = {node_to_label(range_) for range_ in graph.objects(prop_uri, RDFS.range)}

                entities.update(domains)
                entities.update(ranges)

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

            self.ontologies[category] = Schema(
                entities=sorted(list(entities)),
                relations=relations
            )

    def load(self) -> List[TaskEntry]:
        entries = []
        for filename in sorted(os.listdir(self.data_dir)):
            if not filename.endswith(".xml"):
                continue
            
            filepath = os.path.join(self.data_dir, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            for entry_elem in root.findall(".//entry"):
                entry_id = entry_elem.get("id")
                category = entry_elem.get("category")
                
                text_elem = entry_elem.find("text")
                text = text_elem.text if text_elem is not None else ""
                
                gold_triples = []
                triples_elem = entry_elem.find("triples")
                if triples_elem is not None:
                    for triple_elem in triples_elem.findall("triple"):
                        sub = triple_elem.find("sub").text
                        rel = triple_elem.find("rel").text
                        obj = triple_elem.find("obj").text
                        gold_triples.append(Triple(subject=sub, relation=rel, object=obj))
                
                schema_def = self.ontologies.get(category, Schema(entities=[], relations=[]))
                
                entries.append(TaskEntry(
                    entry_id=entry_id,
                    input_text=text,
                    gold_triples=gold_triples,
                    schema_def=schema_def
                ))
                
        return entries

    def load_by_category(self) -> List[CategoryBatch]:
        """Load all entries and group them into CategoryBatch objects."""
        all_entries = self.load()
        
        grouped: Dict[str, List[TaskEntry]] = OrderedDict()
        for entry in all_entries:
            cat = entry.entry_id.rsplit("_", 2)[0]  # e.g. "1_Airport" from "1_Airport_test_1"
            grouped.setdefault(cat, []).append(entry)
        
        batches = []
        for cat, entries in grouped.items():
            schema = self.ontologies.get(cat, Schema(entities=[], relations=[]))
            batches.append(CategoryBatch(category=cat, schema_def=schema, entries=entries))
        
        return batches
