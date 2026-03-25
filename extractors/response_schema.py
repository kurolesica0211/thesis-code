"""
Pydantic response schema for constrained decoding of a category batch.

The static base classes define the shape. build_batch_response(schema_def)
produces a per-category subclass where relation and entity-type fields are
constrained to the exact allowed values via Literal enums, so the model
cannot hallucinate unknown relations or entity types.
"""
from typing import Annotated, List, Literal, Optional, Type
from pydantic import BaseModel, Field, create_model


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

def build_batch_response(schema_def, expected_entries: Optional[int] = None) -> Type[BaseModel]:
    """
    Return a BatchResponse-shaped Pydantic model whose relation field is
    restricted to the allowed values in schema_def.
    If expected_entries is set, enforce an exact number of items in `entries`.
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
    entries_type = List[ConstrainedEntry]
    if expected_entries is not None:
        entries_type = Annotated[
            List[ConstrainedEntry],
            Field(min_length=expected_entries, max_length=expected_entries),
        ]

    return create_model(
        "BatchResponse",
        entries=(entries_type, ...),
    )


def build_correction_response(
    schema_def,
    allowed_indices_by_entry: List[List[int]],
    max_new_triples_by_entry: Optional[List[int]] = None,
    constrain_vocab: bool = False,
    constrain_triple_count: bool = False,
) -> Type[BaseModel]:
    """
    Build a correction-response model with strict per-entry constraints.

    - Number of entries is fixed to len(allowed_indices_by_entry)
    - Can constrain per-entry triple count (optional)
    - Each triple must include `triple_idx`, constrained to allowed indices for that entry
    - Can cap the number of new triples (`triple_idx = -1`) per entry

    Note: uses object fields entry_1..entry_n (instead of heterogeneous list items)
    for compatibility with providers that do not support tuple-array schemas.
    """
    if constrain_vocab and schema_def is not None:
        entity_type = Literal[tuple(schema_def.entities)]  # type: ignore[valid-type]
        relation_type = Literal[tuple(r.relation for r in schema_def.relations)]  # type: ignore[valid-type]
    else:
        entity_type = str
        relation_type = str

    if max_new_triples_by_entry is None:
        max_new_triples_by_entry = [0] * len(allowed_indices_by_entry)
    if len(max_new_triples_by_entry) != len(allowed_indices_by_entry):
        raise ValueError("max_new_triples_by_entry must match allowed_indices_by_entry length")

    entry_fields = {}
    for entry_i, allowed_indices in enumerate(allowed_indices_by_entry, 1):
        max_new_for_entry = max(0, int(max_new_triples_by_entry[entry_i - 1]))
        unique_allowed = sorted(set(allowed_indices))
        required_updates_count = len([idx for idx in unique_allowed if idx >= 0])
        allows_additions = -1 in unique_allowed

        triple_count = len(unique_allowed)
        if triple_count == 0:
            index_type = int
        else:
            index_type = Literal[tuple(unique_allowed)]  # type: ignore[valid-type]

        CorrectionTriple = create_model(
            f"CorrectionTripleOut_{entry_i}",
            triple_idx=(index_type, ...),
            subject=(str, ...),
            relation=(relation_type, ...),
            object=(str, ...),
        )
        CorrectionTypes = create_model(
            f"CorrectionTypesOut_{entry_i}",
            subject=(entity_type, ...),
            object=(entity_type, ...),
        )

        if constrain_triple_count:
            if allows_additions:
                triples_type = Annotated[
                    List[CorrectionTriple],
                    Field(
                        min_length=required_updates_count,
                        max_length=required_updates_count + max_new_for_entry,
                    ),
                ]
                schemas_type = Annotated[
                    List[CorrectionTypes],
                    Field(
                        min_length=required_updates_count,
                        max_length=required_updates_count + max_new_for_entry,
                    ),
                ]
            else:
                triples_type = Annotated[
                    List[CorrectionTriple],
                    Field(min_length=required_updates_count, max_length=required_updates_count),
                ]
                schemas_type = Annotated[
                    List[CorrectionTypes],
                    Field(min_length=required_updates_count, max_length=required_updates_count),
                ]
        else:
            triples_type = List[CorrectionTriple]
            schemas_type = List[CorrectionTypes]

        CorrectionEntry = create_model(
            f"CorrectionEntryResult_{entry_i}",
            triples=(triples_type, ...),
            schemas=(schemas_type, ...),
        )

        entry_fields[f"entry_{entry_i}"] = (CorrectionEntry, ...)

    EntriesModel = create_model("CorrectionEntries", **entry_fields)

    return create_model(
        "CorrectionBatchResponse",
        entries=(EntriesModel, ...),
    )
