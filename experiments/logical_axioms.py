from __future__ import annotations

import argparse
import io
import sys
from collections import defaultdict
from pathlib import Path

try:
	import jpype
	import jpype.imports
except ImportError as exc:  # pragma: no cover - depends on local environment
	raise RuntimeError(
		"This script requires JPype1. Install the project dependencies before running it."
	) from exc

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
	System = jpype.JClass("java.lang.System")
	PrintStream = jpype.JClass("java.io.PrintStream")
	OutputStream = jpype.JClass("java.io.OutputStream")
	null_stream = PrintStream(OutputStream.nullOutputStream())
	System.setErr(null_stream)
	System.setOut(null_stream)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Load family_TBOX.ttl through OWL API and list its distinct logical axioms."
		)
	)
	parser.add_argument(
		"--tbox",
		type=Path,
		default=Path(DEFAULT_TBOX_PATH),
		help="Path to the TBOX ttl file.",
	)
	parser.add_argument(
		"--jar-classpath",
		type=str,
		default=DEFAULT_JAR_CLASSPATH,
		help="Classpath for OWLAPI/Pellet jars (supports wildcard).",
	)
	return parser.parse_args()


def load_ontology(tbox_path: Path):
	from org.semanticweb.owlapi.apibinding import OWLManager

	manager = OWLManager.createOWLOntologyManager()
	java_file = jpype.JClass("java.io.File")(str(tbox_path.resolve()))
	return manager.loadOntologyFromOntologyDocument(java_file)


def group_logical_axioms(ontology) -> dict[str, list[str]]:
	grouped_axioms: dict[str, list[str]] = defaultdict(list)
	for axiom in ontology.getLogicalAxioms():
		axiom_type = str(axiom.getAxiomType().getName())
		grouped_axioms[axiom_type].append(str(axiom.toString()))

	return {
		axiom_type: sorted(axioms)
		for axiom_type, axioms in sorted(grouped_axioms.items())
	}


def main() -> None:
	args = parse_args()
	suppress_known_java_warnings()

	if not args.tbox.exists():
		raise FileNotFoundError(f"TBOX file not found: {args.tbox}")

	ensure_jvm(args.jar_classpath)
	suppress_java_stderr()

	ontology = load_ontology(args.tbox)
	grouped_axioms = group_logical_axioms(ontology)
	total_axioms = sum(len(axioms) for axioms in grouped_axioms.values())

	print(f"Distinct logical axiom types: {len(grouped_axioms)}")
	print(f"Distinct logical axioms: {total_axioms}")
	for axiom_type, axioms in grouped_axioms.items():
		print(f"\n{axiom_type}: {len(axioms)}")
		for index, axiom in enumerate(axioms, start=1):
			print(f"  {index}. {axiom}")


if __name__ == "__main__":
	main()
