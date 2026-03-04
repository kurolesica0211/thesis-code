import json
import re
import time
from typing import List, Dict
from litellm import completion
from models.data_models import (
    TaskEntry, BatchExtractionResult,
    EntryExtractionResult, Triple, TripleSchema
)
from extractors.prompt_engine import PromptEngine
from extractors.response_schema import build_batch_response, BatchResponse

MAX_RETRIES   = 2
RETRY_DELAY_S = 10

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

    def extract_batch(self, entries: List[TaskEntry], schema) -> BatchExtractionResult:
        """Send a single batched request for all entries (same category/schema).
        Retries once on transient 503 / ServiceUnavailable errors."""
        prompt = self.prompt_engine.build_batch_prompt(entries, schema)
        ResponseModel = build_batch_response(schema)

        last_err = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = completion(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=ResponseModel,
                    temperature=0.0,
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
                last_err = e
                is_transient = "503" in str(e) or "ServiceUnavailable" in type(e).__name__
                if is_transient and attempt < MAX_RETRIES:
                    print(f"  [retry {attempt}/{MAX_RETRIES}] 503 — waiting {RETRY_DELAY_S}s ...")
                    time.sleep(RETRY_DELAY_S)
                    continue
                break

        print(f"[Extractor] batch failed ({len(entries)} entries): "
              f"{type(last_err).__name__}: {last_err}")
        return BatchExtractionResult(
            results={f"entry_{i}": EntryExtractionResult()
                     for i in range(1, len(entries) + 1)}
        )

    def extract_batch_rdf(self, entries: List[TaskEntry],
                          rdf_ontology_text: str,
                          schema_def=None) -> BatchExtractionResult:
        """Batched extraction using an RDF ontology pasted into the prompt.
        When schema_def is provided, relation and entity-type fields are
        constrained to the allowed labels via Literal enums."""
        prompt = self.prompt_engine.build_rdf_batch_prompt(entries, rdf_ontology_text)
        ResponseModel = build_batch_response(schema_def) if schema_def else BatchResponse

        last_err = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = completion(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=ResponseModel,
                    temperature=0.0,
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
                last_err = e
                is_transient = "503" in str(e) or "ServiceUnavailable" in type(e).__name__
                if is_transient and attempt < MAX_RETRIES:
                    print(f"  [retry {attempt}/{MAX_RETRIES}] 503 — waiting {RETRY_DELAY_S}s ...")
                    time.sleep(RETRY_DELAY_S)
                    continue
                break

        print(f"[Extractor] RDF batch failed ({len(entries)} entries): "
              f"{type(last_err).__name__}: {last_err}")
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
            validate_batch, format_violations_for_prompt,
        )

        # Step 1 — initial extraction
        batch_result = self.extract_batch_rdf(entries, rdf_ontology_text, schema_def=schema_def)

        for round_num in range(1, max_rounds + 1):
            # Step 2 — SHACL validation
            report = validate_batch(batch_result.results, rdf_ontology_text, shacl_shapes_ttl)
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
            last_err = None
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    response = completion(
                        model=self.model_name,
                        messages=[{"role": "user", "content": prompt}],
                        response_format=ResponseModel,
                        temperature=0.0,
                    )
                    corrected_data = json.loads(
                        response.choices[0].message.content
                    )
                    break
                except Exception as e:
                    last_err = e
                    is_transient = "503" in str(e) or "ServiceUnavailable" in type(e).__name__
                    if is_transient and attempt < MAX_RETRIES:
                        print(f"  [retry {attempt}/{MAX_RETRIES}] 503 — waiting {RETRY_DELAY_S}s ...")
                        time.sleep(RETRY_DELAY_S)
                        continue
                    break

            if corrected_data is None:
                print(f"  [SHACL] correction call failed: {last_err}")
                break

            # Step 5 — merge corrections back
            corrected_entries = corrected_data.get("entries", [])
            for local_i, entry_idx in enumerate(sorted(violated_indices)):
                key = f"entry_{entry_idx + 1}"
                if local_i < len(corrected_entries):
                    raw = corrected_entries[local_i]
                    if isinstance(raw, dict):
                        batch_result.results[key] = _parse_entry_data(raw)

        return batch_result
