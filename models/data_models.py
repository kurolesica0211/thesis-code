from __future__ import annotations

from pydantic import BaseModel, model_validator
from typing import List
from rdflib import Graph, URIRef

class Triple(BaseModel):
    subject: str
    relation: str
    object: str

class TripleSchema(BaseModel):
    """Entity types the model assigned to the subject and object of a triple."""
    subject: str
    object: str

class RelationDef(BaseModel):
    relation: str
    valid_subjects: List[str]
    valid_objects: List[str]

class Schema(BaseModel):
    entities: List[str]
    relations: List[RelationDef]

class TaskEntry(BaseModel):
    entry_id: str
    input_text: str
    gold_triples_graph: Graph | None = None
    ontology_graph: Graph
    shacl_graph: Graph
    schema_def: Schema
    data_graph: Graph | None = None
    

class DataEntry(BaseModel):
    """
    A typed dict representing a set of paths to text files under one ontology. \n
    ``entry_id`` is used to identify individual entries later. \n
    ``gold_triples_filepaths`` positionally corresponds to ``text_filepaths``.
    """
    entry_id: str
    text_filepaths: List[str]
    gold_triples_filepaths: List[str] | None = None
    ontology_filepath: str
    shacl_filepath: str
    data_graph_path: str | None = None
    
    @model_validator(mode="after")
    def check_lengths(self) -> DataEntry:
        if self.gold_triples_filepaths is not None:
            if len(self.gold_triples_filepaths) != len(self.text_filepaths):
                raise ValueError("The nubmer of provided files with gold triples" + 
                                f"and files with text don't match at {self.entry_id}")


class Violation(BaseModel):
    severity: str | None = None
    focus: URIRef | None = None
    path: URIRef | None = None
    value: URIRef | None = None
    constraint: str | None = None
    source_shape: URIRef | None = None
    message: str | None = None
    llm_explanation: str | None = None
    llm_instruction: str | None = None
    

class ValidationReport(BaseModel):
    conforms: bool
    violations: list[Violation] | None = None