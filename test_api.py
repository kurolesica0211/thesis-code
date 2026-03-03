"""
Test litellm API connectivity using a real category batch and the actual prompt template.
Run with:  python test_api.py
Override model:     python test_api.py gemini/gemini-1.5-pro
Override category:  python test_api.py gemini/gemini-2.0-flash 1_City
Override mode:      python test_api.py gemini/gemini-3-flash-preview 1_City rdf
Enable SHACL:       python test_api.py gemini/gemini-3-flash-preview 1_City rdf shacl
"""
import os
import sys
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from litellm import completion

from loaders.oskgc_loader import OSKGCLoader
from extractors.prompt_engine import PromptEngine
from extractors.response_schema import build_batch_response, BatchResponse
from extractors.extractor import _parse_entry_data, Extractor

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
MODEL    = sys.argv[1] if len(sys.argv) > 1 else "gemini/gemini-3-flash-preview"
CATEGORY = sys.argv[2] if len(sys.argv) > 2 else None   # None = use first category
MODE     = sys.argv[3] if len(sys.argv) > 3 else "rdf"  # "rdf" or "json"
SHACL    = (sys.argv[4].lower() == "shacl") if len(sys.argv) > 4 else False

# ── Config ────────────────────────────────────────────────────────────────────
MODEL    = sys.argv[1] if len(sys.argv) > 1 else "gemini/gemini-3-flash-preview"
CATEGORY = sys.argv[2] if len(sys.argv) > 2 else None   # None = use first category
MODE     = sys.argv[3] if len(sys.argv) > 3 else "rdf"  # "rdf" or "json"

RDF_ONTOLOGY_DIR = "OSKGC/ontologies/rdf"
# ─────────────────────────────────────────────────────────────────────────────

# Load data grouped by category
loader = OSKGCLoader(data_dir="OSKGC/data", ontology_dir="OSKGC/ontologies", split="dev")
batches = loader.load_by_category()

if CATEGORY:
    matching = [b for b in batches if b.category == CATEGORY]
    if not matching:
        raise ValueError(f"Category '{CATEGORY}' not found. Available: "
                         f"{[b.category for b in batches]}")
    batch = matching[0]
else:
    batch = batches[0]

# Build the batched prompt
if MODE == "rdf":
    rdf_path = os.path.join(RDF_ONTOLOGY_DIR, f"{batch.category}.ttl")
    with open(rdf_path, "r", encoding="utf-8") as f:
        rdf_text = f.read()
    engine = PromptEngine(template_path="prompts/zero_shot_rdf.md")
    prompt = engine.build_rdf_batch_prompt(batch.entries, rdf_text)
    ResponseModel = BatchResponse
    schema_log = {"rdf_file": rdf_path}
else:
    engine = PromptEngine(template_path="prompts/zero_shot_basic.md")
    prompt = engine.build_batch_prompt(batch.entries, batch.schema_def)
    ResponseModel = build_batch_response(batch.schema_def)
    schema_log = {
        "entities": batch.schema_def.entities,
        "relations": [r.model_dump() for r in batch.schema_def.relations],
    }

# ── Call API ──────────────────────────────────────────────────────────────────
log = {
    "timestamp": datetime.now().isoformat(),
    "model": MODEL,
    "mode": MODE,
    "shacl": SHACL,
    "category": batch.category,
    "num_entries": len(batch.entries),
    "schema": schema_log,
    "prompt": prompt,
}

start = time.time()
try:
    if SHACL and MODE == "rdf":
        # Use the full Extractor SHACL loop
        engine_obj = PromptEngine(template_path="prompts/zero_shot_rdf.md")
        ext = Extractor(model_name=MODEL, prompt_engine=engine_obj)
        batch_result = ext.extract_batch_rdf_with_shacl(
            batch.entries, rdf_text, max_rounds=1,
        )
        elapsed = time.time() - start
        log["elapsed_seconds"] = round(elapsed, 3)
        log["entries"] = []
        for i, entry in enumerate(batch.entries):
            key = f"entry_{i + 1}"
            parsed_entry = batch_result.results.get(key)
            if parsed_entry is None:
                from models.data_models import EntryExtractionResult
                parsed_entry = EntryExtractionResult()
            log["entries"].append({
                "entry_id":     entry.entry_id,
                "input_text":   entry.input_text,
                "gold_triples": [t.model_dump() for t in entry.gold_triples],
                "pred_triples": [t.model_dump() for t in parsed_entry.triples],
                "pred_schemas": [s.model_dump() for s in parsed_entry.schemas],
            })
        log["status"] = "success"
    else:
        response = completion(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format=ResponseModel,
            temperature=0.0,
        )
        elapsed = time.time() - start

        content = response.choices[0].message.content
        usage   = response.usage
        parsed  = json.loads(content)
        entries_out = parsed.get("entries", [])

        log["elapsed_seconds"] = round(elapsed, 3)
        log["raw_response"] = parsed
        log["token_usage"] = {
            "prompt":     usage.prompt_tokens,
            "completion": usage.completion_tokens,
            "total":      usage.total_tokens,
        }
        log["entries"] = []
        for i, entry in enumerate(batch.entries):
            raw = entries_out[i] if i < len(entries_out) else {}
            parsed_entry = _parse_entry_data(raw if isinstance(raw, dict) else {})
            log["entries"].append({
                "entry_id":     entry.entry_id,
                "input_text":   entry.input_text,
                "gold_triples": [t.model_dump() for t in entry.gold_triples],
                "pred_triples": [t.model_dump() for t in parsed_entry.triples],
                "pred_schemas": [s.model_dump() for s in parsed_entry.schemas],
            })
        log["status"] = "success"

except Exception as e:
    elapsed = time.time() - start
    log["elapsed_seconds"] = round(elapsed, 3)
    log["status"] = "error"
    log["error"] = str(e)

# ── Write log file ────────────────────────────────────────────────────────────
os.makedirs("results", exist_ok=True)
safe_model = MODEL.replace("/", "_").replace(":", "_")
safe_cat   = (CATEGORY or batch.category).replace("/", "_")
suffix     = f"_{MODE}_shacl" if SHACL else f"_{MODE}"
out_path   = f"results/test_api_{safe_model}_{safe_cat}{suffix}.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print(f"{'✓' if log['status'] == 'success' else '✗'} {log['status']} — written to {out_path}")
if log["status"] == "error":
    raise RuntimeError(log["error"])