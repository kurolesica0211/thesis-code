import os
from typing import List
from models.data_models import Schema, TaskEntry

class PromptEngine:
    def __init__(self, template_path: str):
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found at {template_path}")
        with open(template_path, "r", encoding="utf-8") as f:
            self.template = f.read()

    def build_batch_prompt(self, entries: List[TaskEntry], schema: Schema) -> str:
        """Build a single prompt for a batch of entries sharing the same schema."""
        entities_str = ", ".join(schema.entities)
        
        relations_list = []
        for rel in schema.relations:
            rel_str = f"- {rel.relation} (Valid Subjects: {', '.join(rel.valid_subjects)}, Valid Objects: {', '.join(rel.valid_objects)})"
            relations_list.append(rel_str)
        relations_str = "\n".join(relations_list)
        
        texts_list = []
        for i, entry in enumerate(entries, 1):
            texts_list.append(f"entry_{i}: {entry.input_text}")
        input_texts_str = "\n".join(texts_list)
        
        return self.template.format(
            entities=entities_str,
            relations=relations_str,
            input_texts=input_texts_str
        )

    def build_rdf_batch_prompt(self, entries: List[TaskEntry], rdf_ontology_text: str) -> str:
        """Build a prompt for a batch of entries using an RDF ontology pasted into the template."""
        texts_list = []
        for i, entry in enumerate(entries, 1):
            texts_list.append(f"entry_{i}: {entry.input_text}")
        input_texts_str = "\n".join(texts_list)

        return self.template.format(
            ontology_rdf=rdf_ontology_text,
            input_texts=input_texts_str
        )

    @staticmethod
    def build_correction_prompt(
        template_path: str,
        rdf_ontology_text: str,
        violations_text: str,
    ) -> str:
        """Build a correction prompt from the correction template."""
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.format(
            ontology_rdf=rdf_ontology_text,
            violations=violations_text,
        )
        
    @staticmethod
    def build_violation_translation_prompt(
        template_path: str,
        violation_text: str,
    ) -> str:
        """Build a violation translation prompt from the violation translation template."""
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.format(
            violations=violation_text,
        )
