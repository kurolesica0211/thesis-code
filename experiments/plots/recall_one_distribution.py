#!/usr/bin/env python3
"""Aggregate subruns with recall == 1 and plot distribution by ground-truth count.

Usage:
  python experiments/plots/recall_one_distribution.py \
    --run-a results/royalty_gemini_with_shacl \
    --run-b results/royalty_gemini_without_shacl \
    --output-pdf results/recall_one_distribution.pdf
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt


def _find_metrics(run_dir: Path) -> Path:
    # Prefer top-level metrics.json, fall back to first found.
    candidate = run_dir / "metrics.json"
    if candidate.exists():
        return candidate
    found = list(run_dir.rglob("metrics.json"))
    if found:
        return found[0]
    raise FileNotFoundError(f"No metrics.json found in {run_dir}")


def _load_subruns(metrics_path: Path) -> List[Dict]:
    data = json.loads(metrics_path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.get("subrun_metrics") or data.get("subruns") or [])
    if isinstance(data, list) and data:
        first = data[0]
        return list(first.get("subrun_metrics") or first.get("subruns") or [])
    return []


def aggregate_recall_one(run_a: Path, run_b: Path) -> Tuple[Dict[int, int], int]:
    """Return mapping ground_truth_count -> number of recall==1 subruns and total matched."""
    metrics_a = _find_metrics(run_a)
    metrics_b = _find_metrics(run_b)

    subruns = _load_subruns(metrics_a) + _load_subruns(metrics_b)
    counts: Dict[int, int] = {}
    matched = 0
    for rec in subruns:
        try:
            recall = float(rec.get("recall", 0.0))
        except Exception:
            continue
        if recall == 1.0:
            matched += 1
            gt = int(float(rec.get("ground_truth") or 0))
            counts[gt] = counts.get(gt, 0) + 1

    return counts, matched


def plot_bar(counts: Dict[int, int], output_pdf: Path) -> Path:
    if not counts:
        raise ValueError("No recall==1 subruns found to plot.")

    xs = sorted(counts.keys())
    ys = [counts[x] for x in xs]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=160)
    ax.bar(xs, ys, color="#2ca02c", alpha=0.85)
    ax.set_xlabel("Ground-truth triple count", fontsize=20)
    ax.set_ylabel("Number of subruns with recall = 1", fontsize=20)
    ax.tick_params(axis="both", labelsize=20)
    ax.set_ylim(0, max(ys) * 1.1)
    fig.tight_layout()
    out = output_pdf.with_suffix(".pdf")
    fig.savefig(out, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Aggregate recall==1 subruns and plot distribution by ground-truth count")
    p.add_argument("--run-a", type=Path, required=True, help="First results run folder (contains metrics.json)")
    p.add_argument("--run-b", type=Path, required=True, help="Second results run folder (contains metrics.json)")
    p.add_argument("--output-pdf", type=Path, help="Output PDF path for bar chart (defaults to <run_a>_vs_<run_b>_recall1.pdf)")
    p.add_argument("--output-json", type=Path, help="Optional JSON summary path")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_a = args.run_a
    run_b = args.run_b
    if not run_a.exists() or not run_b.exists():
        raise FileNotFoundError("One of the run folders does not exist")

    counts, matched = aggregate_recall_one(run_a, run_b)
    if not args.output_pdf:
        default_name = f"{run_a.name}_vs_{run_b.name}_recall1"
        output_pdf = Path("results") / f"{default_name}.pdf"
    else:
        output_pdf = args.output_pdf

    if counts:
        saved = plot_bar(counts, output_pdf)
        print(f"Saved bar chart to: {saved}")
    else:
        print("No recall==1 subruns found across the two runs.")

    summary = {
        "run_a": str(run_a),
        "run_b": str(run_b),
        "matched_recall_1_subruns": matched,
        "distribution": {str(k): v for k, v in sorted(counts.items())},
    }
    print(json.dumps(summary, indent=2))
    if args.output_json:
        args.output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Wrote JSON summary to: {args.output_json}")


if __name__ == "__main__":
    main()
