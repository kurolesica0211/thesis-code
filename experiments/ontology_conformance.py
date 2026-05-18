from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from statistics import mean
from pathlib import Path

import jpype
import jpype.imports
from rdflib import Graph
from tqdm import tqdm

RUN_DIR_PATTERN = re.compile(r"^\d+_\d+$")
DEFAULT_JAR_CLASSPATH = "experiments/java_libs/*"
DEFAULT_TBOX_PATH = "custom_family_bench/family_TBOX.ttl"
OWL_NOISE_SUBSTRINGS = (
    "OWLDataFactoryImpl.getInstance() WARNING: you should not use the implementation directly; this static method is here for backwards compatibility only",
)


class _FilteredStream(io.TextIOBase):
    def __init__(self, stream: io.TextIOBase, blocked_substrings: tuple[str, ...]) -> None:
        self._stream = stream
        self._blocked_substrings = blocked_substrings

    def write(self, text: str) -> int:
        if any(substring in text for substring in self._blocked_substrings):
            return len(text)
        return self._stream.write(text)

    def flush(self) -> None:
        self._stream.flush()

    def isatty(self) -> bool:
        return self._stream.isatty()


def suppress_known_java_warnings() -> None:
    sys.stdout = _FilteredStream(sys.stdout, OWL_NOISE_SUBSTRINGS)
    sys.stderr = _FilteredStream(sys.stderr, OWL_NOISE_SUBSTRINGS)


def ensure_jvm(classpath: str) -> None:
    if not jpype.isJVMStarted():
        jpype.startJVM(
            "-Dorg.slf4j.simpleLogger.defaultLogLevel=error",
            classpath=[classpath],
        )


def suppress_java_stderr() -> None:
    # Some OWLAPI/Pellet warnings are emitted by Java directly to System.err.
    # Redirecting Java std streams at JVM level avoids terminal clutter.
    System = jpype.JClass("java.lang.System")
    PrintStream = jpype.JClass("java.io.PrintStream")
    OutputStream = jpype.JClass("java.io.OutputStream")
    null_stream = PrintStream(OutputStream.nullOutputStream())
    System.setErr(null_stream)
    System.setOut(null_stream)


def discover_run_dirs(results_dir: Path) -> list[Path]:
    return sorted(
        [
            p
            for p in results_dir.iterdir()
            if p.is_dir() and RUN_DIR_PATTERN.match(p.name)
        ],
        key=lambda p: (int(p.name.split("_")[0]), int(p.name.split("_")[1])),
    )


def load_rdf(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path)
    return graph


def compute_avai(ontology, explanations):
    axiom_count: dict[str, int] = {}
    for axiom in ontology.getAxioms():
        axiom_count[str(axiom.toString())] = 1

    for expl in explanations:
        for axiom in expl.getAxioms():
            key = str(axiom.toString())
            axiom_count[key] = axiom_count.get(key, 0) + 1

    return sum(axiom_count.values()) / (len(axiom_count.keys()) + 1)


def compute_metrics(ontology, explanations):
    smis = explanations.size()
    avai = compute_avai(ontology, explanations)

    return {
        "smis": int(smis),
        "avai": float(avai),
    }


def compute_run_metrics(
    delta_graph_path: Path,
    tbox_graph: Graph,
    reasoner_factory,
    entailment_limit: int,
    timeout: int,
) -> dict[str, float]:
    from org.semanticweb.owlapi.apibinding import OWLManager
    from org.semanticweb.owlapi.io import StringDocumentSource
    from org.semanticweb.owl.explanation.impl.blackbox.checker import (
        InconsistentOntologyExplanationGeneratorFactory,
    )

    import time
    start_t = time.time()
    if globals().get("DEBUG"):
        print(f"[DEBUG] {delta_graph_path.name}: loading RDF...")
    abox_graph = load_rdf(delta_graph_path)
    ontology_rdf = abox_graph + tbox_graph

    if globals().get("DEBUG"):
        print(f"[DEBUG] {delta_graph_path.name}: serializing + loading into OWL (elapsed {time.time()-start_t:.3f}s)")

    string_source = StringDocumentSource(ontology_rdf.serialize(format="ttl"))
    manager = OWLManager.createOWLOntologyManager()
    ontology = manager.loadOntologyFromOntologyDocument(string_source)

    data_factory = manager.getOWLDataFactory()
    entailment = data_factory.getOWLSubClassOfAxiom(
        data_factory.getOWLThing(), data_factory.getOWLNothing()
    )

    if globals().get("DEBUG"):
        t1 = time.time()
        print(f"[DEBUG] {delta_graph_path.name}: creating explanation generator (elapsed {t1-start_t:.3f}s)")

    inc_expl_fac = InconsistentOntologyExplanationGeneratorFactory(reasoner_factory, timeout)
    generator = inc_expl_fac.createExplanationGenerator(ontology)

    if globals().get("DEBUG"):
        print(f"[DEBUG] {delta_graph_path.name}: requesting explanations (limit={entailment_limit})")
        t2 = time.time()
    explanations = generator.getExplanations(entailment, entailment_limit)
    
    if globals().get("DEBUG"):
        t3 = time.time()
        print(f"[DEBUG] {delta_graph_path.name}: got explanations (elapsed {t3-start_t:.3f}s) count={explanations.size()}")

    metrics = compute_metrics(ontology, explanations)

    return metrics


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "avg": float(mean(values)),
        "min": float(min(values)),
        "max": float(max(values)),
    }


def write_plots(output_dir: Path, per_run_metrics: list[dict[str, object]]) -> list[str]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return []

    plot_paths: list[str] = []
    metric_names = ["smis", "avai"]
    for metric_name in metric_names:
        values = [float(m[metric_name]) for m in per_run_metrics]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(values, bins=min(20, max(5, int(len(values) ** 0.5))), edgecolor="black")
        ax.set_title(f"Distribution of {metric_name.upper()}")
        ax.set_xlabel(metric_name)
        ax.set_ylabel("Count")
        fig.tight_layout()
        plot_file = output_dir / f"{metric_name}_distribution.png"
        fig.savefig(plot_file, dpi=150)
        plt.close(fig)
        plot_paths.append(str(plot_file))

    return plot_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute ontology conformance metrics over run folders with names like i_i. "
            "Each run must contain delta_graph.ttl."
        )
    )
    parser.add_argument(
        "results_dir",
        type=Path,
        help="Directory containing run folders named like 0_0, 1_1, ...",
    )
    parser.add_argument(
        "--tbox",
        type=Path,
        default=Path(DEFAULT_TBOX_PATH),
        help="Path to TBOX ttl file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output files. Defaults to <results_dir>/ontology_conformance_metrics.",
    )
    parser.add_argument(
        "--jar-classpath",
        type=str,
        default=DEFAULT_JAR_CLASSPATH,
        help="Classpath for OWLAPI/Pellet jars (supports wildcard).",
    )
    parser.add_argument(
        "--explanation-limit",
        type=int,
        default=5000,
        help="Maximum number of explanations per ontology.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1000,
        help="Reasoner timeout parameter for explanation generator factory.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug timing logs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    suppress_known_java_warnings()

    results_dir = args.results_dir
    if not results_dir.exists() or not results_dir.is_dir():
        raise FileNotFoundError(f"Invalid results directory: {results_dir}")

    if not args.tbox.exists():
        raise FileNotFoundError(f"TBOX file not found: {args.tbox}")

    output_dir = args.output_dir or (results_dir / "ontology_conformance_metrics")
    output_dir.mkdir(parents=True, exist_ok=True)

    ensure_jvm(args.jar_classpath)
    suppress_java_stderr()
    from com.clarkparsia.pellet.owlapiv3 import PelletReasonerFactory
    from org.semanticweb.owlapi.apibinding import OWLManager

    # enable debug globally
    globals()["DEBUG"] = bool(args.debug)

    reasoner_factory = PelletReasonerFactory.getInstance()
    tbox_graph = load_rdf(args.tbox)
    run_dirs = discover_run_dirs(results_dir)

    if not run_dirs:
        raise ValueError(f"No run folders matching i_i pattern found in {results_dir}")

    per_run_metrics: list[dict[str, object]] = []
    failed_runs: list[dict[str, str]] = []

    for run_dir in tqdm(run_dirs, desc="Computing ontology metrics", unit="run"):
        delta_graph = run_dir / "delta_graph.ttl"
        if not delta_graph.exists():
            failed_runs.append({"run": run_dir.name, "error": "missing delta_graph.ttl"})
            continue

        try:
            metrics = compute_run_metrics(
                delta_graph,
                tbox_graph,
                reasoner_factory,
                entailment_limit=args.explanation_limit,
                timeout=args.timeout,
            )
            metrics["run"] = run_dir.name
            per_run_metrics.append(metrics)
        except Exception as exc:
            failed_runs.append({"run": run_dir.name, "error": str(exc)})

    if not per_run_metrics:
        raise RuntimeError("No run metrics could be computed. Check failed_runs in output JSON.")

    smis_values = [m["smis"] for m in per_run_metrics]
    avai_values = [m["avai"] for m in per_run_metrics]

    summary = {
        "num_runs_discovered": len(run_dirs),
        "num_runs_processed": len(per_run_metrics),
        "num_runs_failed": len(failed_runs),
        "smis": summarize(smis_values),
        "avai": summarize(avai_values),
        "failed_runs": failed_runs,
    }

    csv_path = output_dir / "per_run_metrics.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run", "smis", "avai"])
        writer.writeheader()
        writer.writerows(per_run_metrics)

    summary_path = output_dir / "summary.json"
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2)

    plot_paths = write_plots(output_dir, per_run_metrics)

    print(f"Processed {len(per_run_metrics)} runs (failed: {len(failed_runs)}).")
    print(f"Per-run metrics: {csv_path}")
    print(f"Summary: {summary_path}")
    if plot_paths:
        print("Plots:")
        for plot in plot_paths:
            print(f"- {plot}")
    else:
        print("Plots skipped (matplotlib not installed).")


if __name__ == "__main__":
    main()