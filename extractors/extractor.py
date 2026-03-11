import json
import re
from typing import List, Dict
from litellm import completion
from models.data_models import (
    TaskEntry, BatchExtractionResult,
    EntryExtractionResult, Triple, TripleSchema
)
from extractors.prompt_engine import PromptEngine
from extractors.response_schema import build_batch_response, BatchResponse

NUM_RETRIES = 3  # passed as num_retries to litellm; it handles backoff internally

# Matches an RDF/Turtle namespace prefix like "rel:", "ns:", "dbo:" but NOT "http://"
_NS_PREFIX_RE = re.compile(r'^[A-Za-z][A-Za-z0-9]*:(?!//)') 

def _strip_ns(s: str) -> str:
    """Strip a namespace prefix from an RDF prefixed name (e.g. 'rel:location' → 'location')."""
    return _NS_PREFIX_RE.sub("", s)


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
                    subject=str(t["subject"]),
                    relation=_strip_ns(str(t["relation"])),
                    object=str(t["object"]),
                ))
            elif "sub" in t and "rel" in t and "obj" in t:
                triples.append(Triple(subject=str(t["sub"]),
                                      relation=_strip_ns(str(t["rel"])),
                                      object=str(t["obj"])))

    schemas = []
    for s in schemas_data:
        if isinstance(s, dict) and "subject" in s and "object" in s:
            schemas.append(TripleSchema(
                subject=_strip_ns(str(s["subject"])),
                object=_strip_ns(str(s["object"])),
            ))

    return EntryExtractionResult(triples=triples, schemas=schemas)


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
        ResponseModel = build_batch_response(schema_def) if schema_def else BatchResponse

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
            report, _, _ = validate_batch(
                batch_result.results, rdf_ontology_text, shacl_shapes_ttl
            )
            if report.conforms:
                print(f"  [SHACL] round {round_num}: all triples conform ✓")
                break

            violated_indices = report.entries_with_violations()
            # Group violations by entry index
            violations_by_entry: Dict[int, list] = {}
            for v in report.violations:
                violations_by_entry.setdefault(v.entry_idx, []).append(v)

            print(f"  [SHACL] round {round_num}: {len(report.violations)} violations "
                  f"in {len(violated_indices)} entries — sending correction prompt")

            # Step 3 — build correction prompt
            violations_text = format_violations_for_prompt(
                violations_by_entry, entries, batch_result.results,
            )
            prompt = PromptEngine.build_correction_prompt(
                correction_template_path, rdf_ontology_text, violations_text,
            )

            # Step 4 — call LLM with correction prompt
            ResponseModel = build_batch_response(schema_def) if schema_def else BatchResponse
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
            except Exception as e:
                print(f"  [SHACL] correction call failed: {type(e).__name__}: {e}")
                break

            # Step 5 — merge corrections back (only the violated triples)
            corrected_entries = corrected_data.get("entries", [])
            for local_i, entry_idx in enumerate(sorted(violated_indices)):
                key = f"entry_{entry_idx + 1}"
                if local_i >= len(corrected_entries):
                    continue
                raw = corrected_entries[local_i]
                if not isinstance(raw, dict):
                    continue
                corrected = _parse_entry_data(raw)
                # Determine which triple indices were violated in this entry
                violated_t_indices = sorted({
                    v.triple_idx for v in violations_by_entry.get(entry_idx, [])
                    if v.triple_idx >= 0
                })
                orig = batch_result.results[key]
                new_triples = list(orig.triples)
                new_schemas = list(orig.schemas)
                for j, t_idx in enumerate(violated_t_indices):
                    if j < len(corrected.triples) and t_idx < len(new_triples):
                        new_triples[t_idx] = corrected.triples[j]
                    if j < len(corrected.schemas) and t_idx < len(new_schemas):
                        new_schemas[t_idx] = corrected.schemas[j]
                batch_result.results[key] = EntryExtractionResult(
                    triples=new_triples, schemas=new_schemas
                )

        return batch_result
