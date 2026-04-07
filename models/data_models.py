from __future__ import annotations

from pydantic import BaseModel, model_validator, ConfigDict
from typing import List, TypedDict, Annotated, Any
from rdflib import Graph, URIRef
from pydantic import BaseModel
from operator import add


class RelationDef(BaseModel):
    relation: str
    valid_subjects: List[str]
    valid_objects: List[str]


class Schema(BaseModel):
    entities: List[str]
    relations: List[RelationDef]


class TaskEntry(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    entry_id: str
    input_text: str
    gold_triples_graph: Graph | None = None
    ontology_graph: Graph
    shacl_graph: Graph
    schema_def: Schema
    data_graph: Graph | None = None
    

class DataEntry(BaseModel):
    """``gold_triples_filepaths`` should follow in the order corresponding to ``text_filepaths``"""
    entry_id: str
    text_filepaths: List[str]
    gold_triples_filepaths: List[str | None]
    ontology_filepath: str
    shacl_filepath: str
    data_graph_path: str | None = None
    
    @model_validator(mode="before")
    @classmethod
    def set_dynamic_defaults(cls, data: Any):
        if isinstance(data, dict):
            if data.get("gold_triples_filepaths") is None:
                text_paths = data.get("text_filepaths") or []
                data["gold_triples_filepaths"] = [None] * len(text_paths)
                return data
    
    @model_validator(mode="after")
    def check_lengths(self) -> DataEntry:
        if self.gold_triples_filepaths is not None:
            if len(self.gold_triples_filepaths) != len(self.text_filepaths):
                raise ValueError("The nubmer of provided files with gold triples" + 
                                f"and files with text don't match at {self.entry_id}")
        return self


class Violation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
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
    

class ViolationTranslation(BaseModel):
    explanation: str
    instruction: str
    

class TaskState(TypedDict, total=False):
    messages: Annotated[list, add]
    iterations: int
    data_graph: Graph
    shacl_tool_call_id: str
    finish_tool_call_id: str
    to_end: bool
    task_manifest: dict
    violation_report: ValidationReport
    
    
class TaskContext(TypedDict):
    llm: Any
    entry_id: str
    input_text: str
    ontology_graph: Graph
    shacl_graph: Graph
    tracing_path: str
    config: dict
    artifacts_dir: str
    

class _ToolRuntime(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    state: TaskState
    context: TaskContext
    tool_call_id: str