from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

from ontology_conformance import (
    DEFAULT_JAR_CLASSPATH,
    DEFAULT_TBOX_PATH,
    compute_explanations,
    discover_run_dirs,
    ensure_jvm,
    load_rdf,
    suppress_java_stderr,
    suppress_known_java_warnings,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print the most succinct justification for each inconsistent ABox in a run directory."
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


def explanation_sort_key(explanation) -> tuple[int, int, tuple[str, ...]]:
    axioms = [str(axiom.toString()) for axiom in explanation.getAxioms()]
    return (
        len(axioms),
        sum(len(axiom) for axiom in axioms),
        tuple(sorted(axioms)),
    )


def pick_most_succinct_explanation(explanations):
    return min(explanations, key=explanation_sort_key)


def format_explanation(explanation) -> str:
    axioms = [str(axiom.toString()) for axiom in explanation.getAxioms()]
    return "\n".join(f"- {axiom}" for axiom in axioms)


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

    globals()["DEBUG"] = bool(args.debug)

    reasoner_factory = PelletReasonerFactory.getInstance()
    tbox_graph = load_rdf(args.tbox)
    run_dirs = discover_run_dirs(results_dir)

    if not run_dirs:
        raise ValueError(f"No run folders matching i_i pattern found in {results_dir}")

    for run_dir in tqdm(run_dirs, desc="Finding inconsistent ABoxes", unit="run"):
        delta_graph = run_dir / "delta_graph.ttl"
        if not delta_graph.exists():
            continue

        ontology, explanations = compute_explanations(
            delta_graph,
            tbox_graph,
            reasoner_factory,
            explanation_limit=args.explanation_limit,
            timeout=args.timeout,
        )
        del ontology

        if explanations.size() == 0:
            continue

        succinct_explanation = pick_most_succinct_explanation(explanations)
        print(run_dir.name)
        print(format_explanation(succinct_explanation))
        print()


if __name__ == "__main__":
    main()