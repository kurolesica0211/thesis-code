import json
import re
from typing import List, Dict, Optional, Literal, Tuple
from litellm import completion
from models.data_models import (
    TaskEntry, BatchExtractionResult,
    EntryExtractionResult, Triple, TripleSchema
)
from extractors.prompt_engine import PromptEngine
from extractors.response_schema import (
    build_batch_response,
    build_correction_response,
    BatchResponse,
)

NUM_RETRIES = 3  # passed as num_retries to litellm; it handles backoff internally

# Matches an RDF/Turtle namespace prefix like "rel:", "ns:", "dbo:" but NOT "http://"
_NS_PREFIX_RE = re.compile(r'^[A-Za-z][A-Za-z0-9]*:(?!//)') 

# Matches the entry_N__ prefix added during data graph construction
_ENTRY_PREFIX_RE = re.compile(r'^(?:entry_\d+__)+')

def _strip_ns(s: str) -> str:
    """Strip a namespace prefix from an RDF prefixed name (e.g. 'rel:location' → 'location')."""
    return _NS_PREFIX_RE.sub("", s)

def _strip_entry_prefix(s: str) -> str:
    """Strip entry_N__ prefix from entity names (e.g. 'entry_1__Radbot' → 'Radbot')."""
    return _ENTRY_PREFIX_RE.sub("", s)

def _normalize_entity_name(s: str) -> str:
    """Normalize entity names by removing namespace + any entry key prefixes."""
    normalized = _strip_ns(s)
    if normalized.startswith("ex_"):
        normalized = normalized[3:]
    return _strip_entry_prefix(normalized)


def _log_round_conforms(log_file: str, round_num: int) -> None:
    """Log when all triples conform in a SHACL round."""
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[ROUND {round_num}] All triples conform ✓\n")


def _log_round_header(log_file: str, round_num: int, violation_count: int, entry_count: int) -> None:
    """Log the header for a new SHACL correction round."""
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"ROUND {round_num} — Corrections Applied\n")
            f.write(f"{'='*80}\n")
            f.write(f"Violations found: {violation_count} in {entry_count} entries\n\n")


def _log_triple_correction(
    log_file: str,
    triple_idx: int,
    orig_triple: Optional[Triple],
    orig_schema: Optional[TripleSchema],
    corrected_triple: Optional[Triple],
    corrected_schema: Optional[TripleSchema],
    violations: List[any]
) -> None:
    """Log a single triple's before/after correction with violations."""
    if not log_file:
        return
    
    with open(log_file, "a", encoding="utf-8") as f:
        if triple_idx >= 0:
            f.write(f"\nTriple {triple_idx + 1}:\n")
        else:
            f.write(f"\nTriple NEW (triple_idx=-1):\n")

        if orig_triple is not None:
            f.write(f"  ORIGINAL: ({orig_triple.subject}, {orig_triple.relation}, {orig_triple.object})\n")
        if orig_schema is not None:
            f.write(f"  ORIGINAL TYPES: ({orig_schema.subject}, {orig_schema.object})\n")
        
        if violations:
            f.write(f"\n  VIOLATIONS:\n")
            for v in violations:
                f.write(f"    [{v.constraint}] {v.message}\n")
        
        if corrected_triple:
            f.write(f"\n  CORRECTED: ({corrected_triple.subject}, {corrected_triple.relation}, {corrected_triple.object})\n")
        if corrected_schema is not None:
            f.write(f"  CORRECTED TYPES: ({corrected_schema.subject}, {corrected_schema.object})\n")


def _log_entry_header(log_file: str, entry_id: str) -> None:
    """Log the header for an entry's corrections."""
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'-'*80}\n")
            f.write(f"Entry: {entry_id}\n")
            f.write(f"{'-'*80}\n")


def _log_correction_error(log_file: str, round_num: int, error_type: str, error_msg: str) -> None:
    """Log when a correction call fails."""
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[ROUND {round_num}] Correction call failed: {error_type}: {error_msg}\n")


def _log_unmapped_violations(log_file: str, violations: List[any]) -> None:
    """Log violations that are not tied to a concrete non-negative triple index."""
    if not log_file or not violations:
        return
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\nUNMAPPED VIOLATIONS (triple_idx < 0):\n")
        for v in violations:
            f.write(f"  [{v.constraint}] {v.message}\n")


def _parse_entry_data(data: dict) -> EntryExtractionResult:
    """Parse a single entry's dict into an EntryExtractionResult."""
    triples_data = data.get("triples", [])
    schemas_data = data.get("schemas", [])

    if not isinstance(triples_data, list):
        triples_data = []
    if not isinstance(schemas_data, list):
        schemas_data = []

    triples = []
    for t in triples_data:
        if isinstance(t, dict):
            if "subject" in t and "relation" in t and "object" in t:
                triples.append(Triple(
                    subject=_normalize_entity_name(str(t["subject"])),
                    relation=_strip_ns(str(t["relation"])),
                    object=_normalize_entity_name(str(t["object"])),
                ))
            elif "sub" in t and "rel" in t and "obj" in t:
                triples.append(Triple(subject=_normalize_entity_name(str(t["sub"])),
                                      relation=_strip_ns(str(t["rel"])),
                                      object=_normalize_entity_name(str(t["obj"]))))

    schemas = []
    for s in schemas_data:
        if isinstance(s, dict) and "subject" in s and "object" in s:
            schemas.append(TripleSchema(
                subject=_normalize_entity_name(str(s["subject"])),
                object=_normalize_entity_name(str(s["object"])),
            ))

    return EntryExtractionResult(triples=triples, schemas=schemas)


def _parse_correction_entry_data(
    data: dict,
) -> Tuple[Dict[int, Tuple[Triple, Optional[TripleSchema]]], List[Tuple[Triple, Optional[TripleSchema]]]]:
    """
    Parse correction entry data.

    Returns:
      - indexed_updates: mapping for non-negative triple_idx updates
      - additions: list of triples/schemas for triple_idx == -1 (can be multiple)
    """
    triples_data = data.get("triples", [])
    schemas_data = data.get("schemas", [])

    if not isinstance(triples_data, list):
        triples_data = []
    if not isinstance(schemas_data, list):
        schemas_data = []

    indexed_updates: Dict[int, Tuple[Triple, Optional[TripleSchema]]] = {}
    additions: List[Tuple[Triple, Optional[TripleSchema]]] = []

    for pos, t in enumerate(triples_data):
        if not isinstance(t, dict):
            continue
        triple_idx = t.get("triple_idx")
        if not isinstance(triple_idx, int):
            continue

        if "subject" in t and "relation" in t and "object" in t:
            triple = Triple(
                subject=_normalize_entity_name(str(t["subject"])),
                relation=_strip_ns(str(t["relation"])),
                object=_normalize_entity_name(str(t["object"])),
            )
        elif "sub" in t and "rel" in t and "obj" in t:
            triple = Triple(
                subject=_normalize_entity_name(str(t["sub"])),
                relation=_strip_ns(str(t["rel"])),
                object=_normalize_entity_name(str(t["obj"])),
            )
        else:
            continue

        schema_obj: Optional[TripleSchema] = None
        if pos < len(schemas_data):
            s = schemas_data[pos]
            if isinstance(s, dict) and "subject" in s and "object" in s:
                schema_obj = TripleSchema(
                    subject=_normalize_entity_name(str(s["subject"])),
                    object=_normalize_entity_name(str(s["object"])),
                )

        if triple_idx == -1:
            additions.append((triple, schema_obj))
        elif triple_idx >= 0:
            indexed_updates[triple_idx] = (triple, schema_obj)

    return indexed_updates, additions


def _validate_response_payload(response_model, payload: dict) -> dict:
    """Validate a raw response payload against the expected dynamic schema."""
    validated = response_model.model_validate(payload)
    return validated.model_dump()


class Extractor:
    def __init__(self, model_name: str, prompt_engine: PromptEngine):
        self.model_name = model_name
        self.prompt_engine = prompt_engine

    def extract_batch_rdf(self, entries: List[TaskEntry],
                          rdf_ontology_text: str,
                          schema_def=None) -> BatchExtractionResult:
        """Batched extraction using an RDF ontology pasted into the prompt.
        When schema_def is provided, relation and entity-type fields are
        constrained to the allowed labels via Literal enums."""
        prompt = self.prompt_engine.build_rdf_batch_prompt(entries, rdf_ontology_text)
        ResponseModel = (
            build_batch_response(schema_def, expected_entries=len(entries))
            if schema_def
            else BatchResponse
        )

        try:
            response = completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format=ResponseModel,
                temperature=0.0,
                num_retries=NUM_RETRIES,
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            data = _validate_response_payload(ResponseModel, data)
            results: Dict[str, EntryExtractionResult] = {}
            for i, entry_data in enumerate(data.get("entries", []), 1):
                key = f"entry_{i}"
                if not isinstance(entry_data, dict):
                    entry_data = {}
                results[key] = _parse_entry_data(entry_data)

            return BatchExtractionResult(results=results)

        except Exception as e:
            print(f"[Extractor] RDF batch failed ({len(entries)} entries): "
                  f"{type(e).__name__}: {e}")
            return BatchExtractionResult(
                results={f"entry_{i}": EntryExtractionResult()
                         for i in range(1, len(entries) + 1)}
            )

    # ── SHACL validation loop ────────────────────────────────────────────

    def extract_batch_rdf_with_shacl(
        self,
        entries: List[TaskEntry],
        rdf_ontology_text: str,
        shacl_shapes_ttl: str,
        correction_template_path: str = "prompts/correction_rdf.md",
        max_rounds: int = 1,
        schema_def=None,
        shacl_log_file: str = None,
        ontology_format: Literal["turtle", "xml"] = "turtle",
    ) -> BatchExtractionResult:
        """
        RDF extraction with iterative SHACL validation & correction.

        1. Initial extraction via extract_batch_rdf().
        2. Validate predicted triples against the ontology's domain/range.
        3. If violations exist, build a correction prompt for the violated
           entries and re-extract. Merge corrected entries back.
        4. Repeat up to *max_rounds* correction passes.
        """
        from validators.shacl_validator import (
            validate_batch, format_violations_for_prompt
        )

        # Step 1 — initial extraction
        batch_result = self.extract_batch_rdf(entries, rdf_ontology_text, schema_def=schema_def)
        
        for round_num in range(1, max_rounds + 1):
            # Step 2 — SHACL validation
            report, shapes_graph, _, _ = validate_batch(
                batch_result.results, rdf_ontology_text, shacl_shapes_ttl, ontology_format=ontology_format
            )
            if report.conforms:
                print(f"  [SHACL] round {round_num}: all triples conform ✓")
                _log_round_conforms(shacl_log_file, round_num)
                break
            
            violations_by_entry = report.group_violations_by_entry()
            violated_indices = report.entries_with_violations()
            
            print(f"  [SHACL] round {round_num}: {len(report.violations)} violations "
                  f"in {len(violated_indices)} entries — sending correction prompt")

            # Step 3 — build correction prompt
            violations_text = format_violations_for_prompt(
                violations_by_entry, entries, batch_result.results, shapes_graph
            )
            prompt = PromptEngine.build_correction_prompt(
                correction_template_path, rdf_ontology_text, violations_text
            )

            with open(f"results/shacl_round_{round_num}_prompt.md", "w", encoding="utf-8") as f:
                f.write(prompt)

            violated_indices_sorted = sorted(violated_indices)
            allowed_indices_by_entry = []
            max_new_triples_by_entry = []
            for entry_idx in violated_indices_sorted:
                entry_violations = violations_by_entry.get(entry_idx, [])
                allowed_indices = sorted({
                    v.triple_idx for v in entry_violations
                })
                max_new = sum(1 for v in entry_violations if v.triple_idx == -1)
                allowed_indices_by_entry.append(allowed_indices)
                max_new_triples_by_entry.append(max_new)

            # Step 4 — call LLM with correction prompt
            ResponseModel = build_correction_response(
                schema_def,
                allowed_indices_by_entry=allowed_indices_by_entry,
                max_new_triples_by_entry=max_new_triples_by_entry,
                constrain_triple_count=True
            )
            corrected_data = None
            try:
                response = completion(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=ResponseModel,
                    temperature=0.0,
                    num_retries=NUM_RETRIES,
                )
                corrected_data = json.loads(response.choices[0].message.content)
                corrected_data = _validate_response_payload(ResponseModel, corrected_data)
            except Exception as e:
                print(f"  [SHACL] correction call failed: {type(e).__name__}: {e}")
                _log_correction_error(shacl_log_file, round_num, type(e).__name__, str(e))
                break
            
            with open(f"results/shacl_round_{round_num}_correction_response.json", "w", encoding="utf-8") as f:
                json.dump(corrected_data, f, ensure_ascii=False, indent=2)
            
            # Step 5 — merge corrections back
            corrected_entries = corrected_data.get("entries", {})
            _log_round_header(shacl_log_file, round_num, len(report.violations), len(violated_indices))

            for local_i, entry_idx in enumerate(violated_indices_sorted):
                key = f"entry_{entry_idx + 1}"
                correction_key = f"entry_{local_i + 1}"
                entry_violations = violations_by_entry.get(entry_idx, [])
                unmapped_violations = [v for v in entry_violations if v.triple_idx < 0]

                _log_entry_header(shacl_log_file, entries[entry_idx].entry_id)
                _log_unmapped_violations(shacl_log_file, unmapped_violations)

                if isinstance(corrected_entries, dict):
                    raw = corrected_entries.get(correction_key)
                else:
                    raw = None

                if not isinstance(raw, dict):
                    continue
                indexed_updates, additions = _parse_correction_entry_data(raw)
                # Determine which non-negative triple indices were violated in this entry
                violated_t_indices = sorted({
                    v.triple_idx for v in entry_violations
                    if v.triple_idx >= 0
                })
                orig = batch_result.results[key]
                new_triples = list(orig.triples)
                new_schemas = list(orig.schemas)

                for t_idx in violated_t_indices:
                    orig_triple = orig.triples[t_idx] if t_idx > -1 and t_idx < len(orig.triples) else None
                    orig_schema = orig.schemas[t_idx] if t_idx > -1 and t_idx < len(orig.schemas) else None
                    corrected_pair = indexed_updates.get(t_idx)
                    corrected_triple = corrected_pair[0] if corrected_pair else None
                    corrected_schema = corrected_pair[1] if corrected_pair else None
                    
                    # Log this specific triple correction
                    violations_for_triple = [
                        v for v in entry_violations
                        if v.triple_idx == t_idx
                    ]
                    _log_triple_correction(
                        shacl_log_file,
                        t_idx,
                        orig_triple,
                        orig_schema,
                        corrected_triple,
                        corrected_schema,
                        violations_for_triple,
                    )
                    
                    # Apply the correction
                    if corrected_triple is not None and corrected_schema is not None:
                        if t_idx > -1 and t_idx < len(new_triples) and t_idx < len(new_schemas):
                            new_triples[t_idx] = corrected_triple
                            new_schemas[t_idx] = corrected_schema
                        else:
                            print(f"  [SHACL] warning: invalid triple index {t_idx} in corrections for entry_{entry_idx + 1}")
                    else:
                        print(f"  [SHACL] warning: missing corrected triple/schema for triple index {t_idx} in entry_{entry_idx + 1}")

                # Apply additions (triple_idx == -1) — can be multiple per entry.
                for added_triple, added_schema in additions:
                    _log_triple_correction(
                        shacl_log_file,
                        -1,
                        None,
                        None,
                        added_triple,
                        added_schema,
                        [],
                    )
                    if added_schema is not None:
                        new_triples.append(added_triple)
                        new_schemas.append(added_schema)
                    else:
                        print(f"  [SHACL] warning: skipping added triple without schema in entry_{entry_idx + 1}")
                    
                batch_result.results[key] = EntryExtractionResult(
                    triples=new_triples, schemas=new_schemas
                )

        return batch_result
