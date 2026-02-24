import os
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Set
from collections import defaultdict, OrderedDict
from models.data_models import TaskEntry, Triple, Schema, RelationDef, CategoryBatch
from loaders.base_loader import BaseLoader

class OSKGCLoader(BaseLoader):
    def __init__(self, data_dir: str, ontology_dir: str, split: str = "test"):
        self.data_dir = os.path.join(data_dir, split)
        self.ontology_dir = ontology_dir
        self.ontologies = {}
        self._load_ontologies()

    def _load_ontologies(self):
        for filename in os.listdir(self.ontology_dir):
            if not filename.endswith(".json"):
                continue
            
            filepath = os.path.join(self.ontology_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            category = data["id"]
            
            # Parse hierarchy
            hierarchy = defaultdict(list)
            if "hierarchy" in data:
                for item in data["hierarchy"]:
                    if item["id"] == "IsA":
                        subclass = item["domain"]
                        superclass = item["range"]
                        hierarchy[superclass].append(subclass)
            
            # Transitive closure of subclasses
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

            # All entities
            entities = set()
            if "entity type" in data:
                for item in data["entity type"]:
                    entities.add(item["id"])
            
            # All relations
            relations = []
            if "relation" in data:
                for item in data["relation"]:
                    rel_id = item["id"]
                    domain = item.get("domain", "")
                    range_ = item.get("range", "")
                    
                    valid_subjects = list(get_all_subclasses(domain)) if domain else []
                    valid_objects = list(get_all_subclasses(range_)) if range_ else []
                    
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
