import json
import re
import time
from typing import List, Dict
from litellm import completion
from models.data_models import (
    TaskEntry, BatchExtractionResult,
    EntryExtractionResult, Triple
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

    if not isinstance(triples_data, list):
        triples_data = []

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

    return EntryExtractionResult(triples=triples)


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
                          rdf_ontology_text: str) -> BatchExtractionResult:
        """Batched extraction using an RDF ontology pasted into the prompt.
        Uses the static BatchResponse schema (no enum constraints)."""
        prompt = self.prompt_engine.build_rdf_batch_prompt(entries, rdf_ontology_text)
        ResponseModel = BatchResponse

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
