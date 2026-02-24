"""
Test litellm API connectivity using a real category batch and the actual prompt template.
Run with:  python test_api.py
Override model:     python test_api.py gemini/gemini-1.5-pro
Override category:  python test_api.py gemini/gemini-2.0-flash 1_City
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
from extractors.response_schema import build_batch_response

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
MODEL    = sys.argv[1] if len(sys.argv) > 1 else "gemini/gemini-3-flash-preview"
CATEGORY = sys.argv[2] if len(sys.argv) > 2 else None   # None = use first category
# ─────────────────────────────────────────────────────────────────────────────

# Load data grouped by category
loader = OSKGCLoader(data_dir="OSKGC/data", ontology_dir="OSKGC/ontologies", split="test")
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
engine = PromptEngine(template_path="prompts/zero_shot_basic.md")
prompt = engine.build_batch_prompt(batch.entries, batch.schema_def)

# ── Call API ──────────────────────────────────────────────────────────────────
log = {
    "timestamp": datetime.now().isoformat(),
    "model": MODEL,
    "category": batch.category,
    "num_entries": len(batch.entries),
    "schema": {
        "entities": batch.schema_def.entities,
        "relations": [r.model_dump() for r in batch.schema_def.relations],
    },
    "prompt": prompt,
}

start = time.time()
try:
    response = completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format=build_batch_response(batch.schema_def),
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
        pred = entries_out[i] if i < len(entries_out) else {}
        log["entries"].append({
            "entry_id":    entry.entry_id,
            "input_text":  entry.input_text,
            "gold_triples": [t.model_dump() for t in entry.gold_triples],
            "pred_triples": pred.get("triples", []),
            "pred_schemas": pred.get("schemas", []),
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
out_path   = f"results/test_api_{safe_model}_{safe_cat}.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(log, f, indent=2, ensure_ascii=False)

print(f"{'✓' if log['status'] == 'success' else '✗'} {log['status']} — written to {out_path}")
if log["status"] == "error":
    raise RuntimeError(log["error"])