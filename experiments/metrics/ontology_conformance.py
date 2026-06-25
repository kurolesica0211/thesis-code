from __future__ import annotations

import argparse
import io
import re
import sys
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


def compute_explanations(
    delta_graph_path: Path,
    tbox_graph: Graph,
    reasoner_factory,
    explanation_limit: int,
    timeout: int,
):
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
        print(
            f"[DEBUG] {delta_graph_path.name}: serializing + loading into OWL "
            f"(elapsed {time.time() - start_t:.3f}s)"
        )

    # Turtle serialization can emit prefixed names that OWLAPI's Turtle parser
    # does not accept for some percent-encoded IRIs; RDF/XML avoids that path.
    string_source = StringDocumentSource(ontology_rdf.serialize(format="xml"))
    manager = OWLManager.createOWLOntologyManager()
    ontology = manager.loadOntologyFromOntologyDocument(string_source)

    data_factory = manager.getOWLDataFactory()
    entailment = data_factory.getOWLSubClassOfAxiom(
        data_factory.getOWLThing(), data_factory.getOWLNothing()
    )

    if globals().get("DEBUG"):
        t1 = time.time()
        print(
            f"[DEBUG] {delta_graph_path.name}: creating explanation generator "
            f"(elapsed {t1 - start_t:.3f}s)"
        )

    inc_expl_fac = InconsistentOntologyExplanationGeneratorFactory(
        reasoner_factory,
        timeout,
    )
    generator = inc_expl_fac.createExplanationGenerator(ontology)

    if globals().get("DEBUG"):
        print(
            f"[DEBUG] {delta_graph_path.name}: requesting explanations "
            f"(limit={explanation_limit})"
        )
    explanations = generator.getExplanations(entailment, explanation_limit)

    if globals().get("DEBUG"):
        t3 = time.time()
        print(
            f"[DEBUG] {delta_graph_path.name}: got explanations "
            f"(elapsed {t3 - start_t:.3f}s) count={explanations.size()}"
        )

    return ontology, explanations


def compute_run_metrics(
    delta_graph_path: Path,
    tbox_graph: Graph,
    reasoner_factory,
    entailment_limit: int,
    timeout: int,
) -> bool:
    _, explanations = compute_explanations(
        delta_graph_path,
        tbox_graph,
        reasoner_factory,
        explanation_limit=entailment_limit,
        timeout=timeout,
    )

    return explanations.size() > 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "List the inconsistent ABoxes in run folders with names like i_i. "
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
        "--jar-classpath",
        type=str,
        default=DEFAULT_JAR_CLASSPATH,
        help="Classpath for OWLAPI/Pellet jars (supports wildcard).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1000,
        help="Reasoner timeout parameter for explanation generator factory.",
    )
    parser.add_argument(
        "--explanation-limit",
        type=int,
        default=1,
        help="Maximum number of explanations to request when checking consistency.",
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

    ensure_jvm(args.jar_classpath)
    suppress_java_stderr()
    from com.clarkparsia.pellet.owlapiv3 import PelletReasonerFactory

    # enable debug globally
    globals()["DEBUG"] = bool(args.debug)

    reasoner_factory = PelletReasonerFactory.getInstance()
    tbox_graph = load_rdf(args.tbox)

    run_dirs = discover_run_dirs(results_dir)

    if not run_dirs:
        raise ValueError(f"No run folders matching i_i pattern found in {results_dir}")

    inconsistent_runs: list[str] = []

    for run_dir in tqdm(run_dirs, desc="Checking ABox consistency", unit="run"):
        delta_graph = run_dir / "delta_graph.ttl"
        if not delta_graph.exists():
            continue

        try:
            is_inconsistent = compute_run_metrics(
                delta_graph,
                tbox_graph,
                reasoner_factory,
                entailment_limit=args.explanation_limit,
                timeout=args.timeout,
            )
            if is_inconsistent:
                inconsistent_runs.append(run_dir.name)
        except Exception as exc:
            print(f"Skipped {run_dir.name}: {exc}", file=sys.stderr)

    print("Inconsistent ABoxes:")
    for run_name in inconsistent_runs:
        print(f"- {run_name}")
    print(f"Count: {len(inconsistent_runs)}")


if __name__ == "__main__":
    main()