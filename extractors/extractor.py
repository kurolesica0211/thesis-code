import json
import time
from typing import List, Dict
from litellm import completion
from models.data_models import (
    TaskEntry, BatchExtractionResult,
    EntryExtractionResult, Triple, TripleSchema
)
from extractors.prompt_engine import PromptEngine
from extractors.response_schema import build_batch_response

MAX_RETRIES   = 2
RETRY_DELAY_S = 10


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
                triples.append(Triple(**{k: str(v) for k, v in t.items()
                                         if k in ("subject", "relation", "object")}))
            elif "sub" in t and "rel" in t and "obj" in t:
                triples.append(Triple(subject=str(t["sub"]),
                                      relation=str(t["rel"]),
                                      object=str(t["obj"])))

    schemas = []
    for s in schemas_data:
        if isinstance(s, dict) and "subject" in s and "object" in s:
            schemas.append(TripleSchema(subject=str(s["subject"]),
                                        object=str(s["object"])))

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
