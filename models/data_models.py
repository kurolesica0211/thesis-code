from pydantic import BaseModel
from typing import List, Dict, Optional

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
    gold_triples: List[Triple]
    schema_def: Schema

class CategoryBatch(BaseModel):
    """A batch of entries sharing the same category (and therefore the same schema)."""
    category: str
    schema_def: Schema
    entries: List[TaskEntry]

class EntryExtractionResult(BaseModel):
    """Extraction result for a single entry inside a batch response."""
    triples: List[Triple] = []
    schemas: List[TripleSchema] = []

class BatchExtractionResult(BaseModel):
    """Full batch response keyed by entry label (entry_1, entry_2, …)."""
    results: Dict[str, EntryExtractionResult] = {}
