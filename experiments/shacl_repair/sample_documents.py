#!/usr/bin/env python3
"""Sample documents for the SHACL-backed repair experiment.

From each of the 5 `royalty_gemini_without_shacl(_1..4)` baseline runs, samples
a roughly even share of logically-inconsistent documents (raw `delta_graph.ttl`,
via Pellet OWL-DL consistency checking) and an equal-sized "usual" control
group of documents that were NOT flagged inconsistent. Both pools are
restricted to documents that have a scored entry in that run's `metrics.json`,
so every sampled document has a reliable "before" precision/recall/f1 to
compare against after the repair run.

Writes `sample_manifest.json` next to this script: one record per sampled
document, with a repair-run entry_id, its source run/subrun/qid, category
(inconsistent/usual), the path to the raw delta graph to seed the repair run
with, and its pre-repair metrics.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from rdflib import Graph
from core.shacl_functions import pyshacl_validate

RUN_TAGS = {
	"royalty_gemini_without_shacl": "base",
	"royalty_gemini_without_shacl_1": "r1",
	"royalty_gemini_without_shacl_2": "r2",
	"royalty_gemini_without_shacl_3": "r3",
	"royalty_gemini_without_shacl_4": "r4",
}

RANDOM_SEED = 42
INCONSISTENT_TARGET = 100
USUAL_PER_RUN = 10


def load_ontology_conformance():
	sys.path.insert(0, str(WORKSPACE_ROOT / "experiments" / "metrics"))
	import ontology_conformance as oc
	return oc


def find_inconsistent_subruns(oc, run_dir: Path, reasoner_factory, tbox_graph: Graph) -> list[str]:
	inconsistent = []
	for doc_dir in oc.discover_run_dirs(run_dir):
		delta_graph = doc_dir / "delta_graph.ttl"
		if not delta_graph.exists():
			continue
		try:
			is_inconsistent = oc.compute_run_metrics(
				delta_graph, tbox_graph, reasoner_factory, entailment_limit=1, timeout=1000
			)
		except Exception as exc:
			print(f"  [warn] {doc_dir.name}: consistency check failed: {exc}")
			continue
		if is_inconsistent:
			inconsistent.append(doc_dir.name)
	return inconsistent


def build_pools(run_name: str, results_root: Path, inconsistent_subruns: list[str]) -> tuple[list[dict], list[dict]]:
	run_dir = results_root / run_name
	metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
	by_subrun = {e["subrun"]: e for e in metrics["subrun_metrics"]}

	all_subruns = {
		p.name for p in run_dir.iterdir()
		if p.is_dir() and "_" in p.name and p.name.split("_")[0].isdigit()
	}

	inconsistent_set = set(inconsistent_subruns)
	inconsistent_scored = sorted(inconsistent_set & by_subrun.keys())
	usual_scored = sorted((all_subruns - inconsistent_set) & by_subrun.keys())

	inconsistent_pool = [by_subrun[s] for s in inconsistent_scored]
	usual_pool = [by_subrun[s] for s in usual_scored]
	return inconsistent_pool, usual_pool


def main() -> None:
	results_root = WORKSPACE_ROOT / "results"
	oc = load_ontology_conformance()

	oc.suppress_known_java_warnings()
	oc.ensure_jvm(oc.DEFAULT_JAR_CLASSPATH)
	oc.suppress_java_stderr()
	from com.clarkparsia.pellet.owlapiv3 import PelletReasonerFactory
	reasoner_factory = PelletReasonerFactory.getInstance()
	tbox_graph = oc.load_rdf(WORKSPACE_ROOT / oc.DEFAULT_TBOX_PATH)

	inconsistent_pools: dict[str, list[dict]] = {}
	usual_pools: dict[str, list[dict]] = {}

	for run_name in RUN_TAGS:
		run_dir = results_root / run_name
		print(f"[{run_name}] checking raw-graph consistency...", flush=True)
		inconsistent_subruns = find_inconsistent_subruns(oc, run_dir, reasoner_factory, tbox_graph)
		inconsistent_pool, usual_pool = build_pools(run_name, results_root, inconsistent_subruns)
		inconsistent_pools[run_name] = inconsistent_pool
		usual_pools[run_name] = usual_pool
		print(
			f"[{run_name}] inconsistent+scored={len(inconsistent_pool)}  usual+scored={len(usual_pool)}",
			flush=True,
		)

	# Pick the smallest per-run quota (<=25, in steps of 1) that pushes the
	# total inconsistent sample as close to INCONSISTENT_TARGET as possible,
	# using every available document in runs that fall short of the quota.
	best_quota, best_total = None, -1
	for quota in range(1, 30):
		total = sum(min(len(pool), quota) for pool in inconsistent_pools.values())
		if abs(total - INCONSISTENT_TARGET) < abs(best_total - INCONSISTENT_TARGET):
			best_quota, best_total = quota, total
	print(f"\nChosen per-run inconsistent quota: {best_quota} (total {best_total})")

	rng = random.Random(RANDOM_SEED)
	sample_records: list[dict] = []

	for run_name, tag in RUN_TAGS.items():
		pool = inconsistent_pools[run_name][:]
		rng.shuffle(pool)
		picked = pool[:best_quota]
		for e in picked:
			sample_records.append({
				"entry_id": f"{tag}-{e['subrun']}",
				"category": "inconsistent",
				"source_run": run_name,
				"source_subrun": e["subrun"],
				"qid": e["qid"],
				"seed_data_graph_path": f"results/{run_name}/{e['subrun']}/delta_graph.ttl",
				"before_metrics": {
					"precision": e["precision"],
					"recall": e["recall"],
					"f1": e["f1"],
					"correct": e["correct"],
					"extracted": e["extracted"],
					"ground_truth": e["ground_truth"],
				},
			})

	for run_name, tag in RUN_TAGS.items():
		pool = usual_pools[run_name][:]
		rng.shuffle(pool)
		picked = pool[:USUAL_PER_RUN]
		for e in picked:
			sample_records.append({
				"entry_id": f"{tag}-{e['subrun']}",
				"category": "usual",
				"source_run": run_name,
				"source_subrun": e["subrun"],
				"qid": e["qid"],
				"seed_data_graph_path": f"results/{run_name}/{e['subrun']}/delta_graph.ttl",
				"before_metrics": {
					"precision": e["precision"],
					"recall": e["recall"],
					"f1": e["f1"],
					"correct": e["correct"],
					"extracted": e["extracted"],
					"ground_truth": e["ground_truth"],
				},
			})

	entry_ids = [r["entry_id"] for r in sample_records]
	assert len(entry_ids) == len(set(entry_ids)), "duplicate entry_id in sample"

	n_inconsistent = sum(1 for r in sample_records if r["category"] == "inconsistent")
	n_usual = sum(1 for r in sample_records if r["category"] == "usual")
	print(f"\nSampled {n_inconsistent} inconsistent + {n_usual} usual = {len(sample_records)} total")

	manifest = {
		"random_seed": RANDOM_SEED,
		"inconsistent_quota_per_run": best_quota,
		"usual_per_run": USUAL_PER_RUN,
		"n_inconsistent": n_inconsistent,
		"n_usual": n_usual,
		"samples": sample_records,
	}
	out_path = Path(__file__).parent / "sample_manifest.json"
	with out_path.open("w", encoding="utf-8") as f:
		json.dump(manifest, f, indent=2)
	print(f"Wrote {out_path}")


if __name__ == "__main__":
	main()
