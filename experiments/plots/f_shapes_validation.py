#!/usr/bin/env python3
"""Validate delta graphs against the F1-F5 shape families.

For every `*_without_shacl*` run directory, and for every document's delta
graph (``delta_graph_inferred.ttl`` by default, or ``delta_graph.ttl`` via
``--data-graph-filename``), this runs SHACL validation separately against
each of the five ``custom_family_bench/shapes_F{1..5}_*.ttl`` shape families,
using ``core.shacl_functions.pyshacl_validate`` (the same validation helper
used elsewhere in this repo). One JSON report per run is written, keyed by
document index and then by shape family, so it's possible to see which
shape families fired violations for which documents, and how persistently
across repeated runs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from rdflib import Graph

from core.shacl_functions import pyshacl_validate


RUN_NAMES = [
	"royalty_gemini_without_shacl",
	"royalty_gemini_without_shacl_1",
	"royalty_gemini_without_shacl_2",
	"royalty_gemini_without_shacl_3",
	"royalty_gemini_without_shacl_4",
]

SHAPE_FAMILIES = {
	"F1_typing": "shapes_F1_typing.ttl",
	"F2_cardinality": "shapes_F2_cardinality.ttl",
	"F3_class_disjointness": "shapes_F3_class_disjointness.ttl",
	"F4_property_disjointness": "shapes_F4_property_disjointness.ttl",
	"F5_closed_shapes": "shapes_F5_closed_shapes.ttl",
}

DOC_DIR_PATTERN = re.compile(r"^(\d+)_\1$")


def discover_documents(run_dir: Path) -> list[tuple[int, Path]]:
	docs = []
	for child in run_dir.iterdir():
		if not child.is_dir():
			continue
		match = DOC_DIR_PATTERN.match(child.name)
		if not match:
			continue
		docs.append((int(match.group(1)), child))
	return sorted(docs, key=lambda item: item[0])


def load_shape_graphs(bench_dir: Path) -> dict[str, Graph]:
	graphs = {}
	for key, filename in SHAPE_FAMILIES.items():
		graphs[key] = Graph().parse(str(bench_dir / filename))
	return graphs


def validate_document(data_graph: Graph, shapes_graph: Graph) -> dict:
	empty_ont_graph = Graph()
	conforms, report, _ = pyshacl_validate(data_graph, empty_ont_graph, shapes_graph)
	violations = report.violations or []
	return {
		"conforms": conforms,
		"violation_count": len(violations),
		"violations": [v.model_dump(mode="json") for v in violations],
	}


def run_validation(
	results_root: Path,
	bench_dir: Path,
	output_dir: Path,
	data_graph_filename: str = "delta_graph_inferred.ttl",
) -> None:
	output_dir.mkdir(parents=True, exist_ok=True)
	shape_graphs = load_shape_graphs(bench_dir)

	start = time.time()
	total_validations = 0

	for run_name in RUN_NAMES:
		run_dir = results_root / run_name
		if not run_dir.exists():
			print(f"[skip] run directory not found: {run_dir}", flush=True)
			continue

		docs = discover_documents(run_dir)
		print(f"[{run_name}] {len(docs)} documents", flush=True)

		run_report: dict[str, dict] = {}
		for doc_index, doc_dir in docs:
			data_path = doc_dir / data_graph_filename
			doc_key = str(doc_index)

			if not data_path.exists():
				print(f"  [warn] missing {data_graph_filename}: {doc_dir.name}", flush=True)
				run_report[doc_key] = {
					key: {"conforms": None, "violation_count": None, "violations": []}
					for key in SHAPE_FAMILIES
				}
				continue

			data_graph = Graph().parse(str(data_path))

			doc_result = {}
			for shape_key, shapes_graph in shape_graphs.items():
				doc_result[shape_key] = validate_document(data_graph, shapes_graph)
				total_validations += 1
			run_report[doc_key] = doc_result

			if doc_index % 50 == 0:
				elapsed = time.time() - start
				print(
					f"  [{run_name}] doc {doc_index}/{len(docs) - 1} done "
					f"({total_validations} validations so far, {elapsed:.1f}s elapsed)",
					flush=True,
				)

		report_path = output_dir / f"{run_name}.json"
		with report_path.open("w", encoding="utf-8") as f:
			json.dump(run_report, f, indent=2)
		print(f"[{run_name}] wrote {report_path}", flush=True)

	elapsed = time.time() - start
	print(f"Done. {total_validations} validations in {elapsed:.1f}s", flush=True)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--results-root", default=str(WORKSPACE_ROOT / "results"))
	parser.add_argument("--bench-dir", default=str(WORKSPACE_ROOT / "custom_family_bench"))
	parser.add_argument(
		"--output-dir",
		default=str(WORKSPACE_ROOT / "helpers" / "validation_reports" / "f_shapes_without_shacl"),
	)
	parser.add_argument(
		"--data-graph-filename",
		default="delta_graph_inferred.ttl",
		help="Which per-document delta graph file to validate (e.g. delta_graph.ttl for the pre-inference graph).",
	)
	args = parser.parse_args()

	run_validation(
		Path(args.results_root),
		Path(args.bench_dir),
		Path(args.output_dir),
		data_graph_filename=args.data_graph_filename,
	)


if __name__ == "__main__":
	main()
