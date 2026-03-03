"""
Pydantic response schema for constrained decoding of a category batch.

The static base classes define the shape. build_batch_response(schema_def)
produces a per-category subclass where relation and entity-type fields are
constrained to the exact allowed values via Literal enums, so the model
cannot hallucinate unknown relations or entity types.
"""
from typing import List, Literal, Type
from pydantic import BaseModel, create_model


# ── Static base classes (shape only) ─────────────────────────────────────────

class TripleOut(BaseModel):
    subject:  str
    relation: str
    object:   str


class TypesOut(BaseModel):
    """Entity types for the subject and object of one triple (same index)."""
    subject: str
    object:  str


class EntryResult(BaseModel):
    triples: List[TripleOut]
    schemas: List[TypesOut]


class BatchResponse(BaseModel):
    """Top-level response: one EntryResult per input sentence, in order."""
    entries: List[EntryResult]


# ── Per-category constrained model ───────────────────────────────────────────

def build_batch_response(schema_def) -> Type[BaseModel]:
    """
    Return a BatchResponse-shaped Pydantic model whose relation field is
    restricted to the allowed values in schema_def.
    Subject/object string values remain free-form str.
    """
    entity_enum   = Literal[tuple(schema_def.entities)]  # type: ignore[valid-type]
    relation_enum = Literal[tuple(r.relation for r in schema_def.relations)]  # type: ignore[valid-type]

    ConstrainedTriple = create_model(
        "TripleOut",
        subject=(str, ...),
        relation=(relation_enum, ...),
        object=(str, ...),
    )
    ConstrainedTypes = create_model(
        "TypesOut",
        subject=(entity_enum, ...),
        object=(entity_enum, ...),
    )
    ConstrainedEntry = create_model(
        "EntryResult",
        triples=(List[ConstrainedTriple], ...),
        schemas=(List[ConstrainedTypes], ...),
    )
    return create_model(
        "BatchResponse",
        entries=(List[ConstrainedEntry], ...),
    )
