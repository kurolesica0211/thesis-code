"""Materialize the inferred closure of an RDF/Turtle knowledge graph.

The script loads an input Turtle graph with Owlready2, runs Pellet reasoning,
and serializes the materialized graph back to Turtle.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import tempfile
import sys
from contextlib import contextmanager
from pathlib import Path

import jpype
from owlready2 import World, sync_reasoner_pellet
from rdflib import BNode, Graph, Literal, OWL, RDF, RDFS, URIRef

try:
	from tqdm import tqdm
except ImportError:  # pragma: no cover - depends on local environment
	def tqdm(iterable, **kwargs):
		return iterable

if __package__ is None or __package__ == "":
	sys.path.append(str(Path(__file__).resolve().parents[1]))

from experiments.metrics.ontology_conformance import (
	DEFAULT_JAR_CLASSPATH,
	compute_explanations,
	ensure_jvm,
	load_rdf,
	suppress_java_stderr,
	suppress_known_java_warnings,
)

DEFAULT_TBOX_PATH = Path("custom_family_bench/family_TBOX.ttl")
DEFAULT_EXPLANATION_LIMIT = 50
DEFAULT_REASONER_TIMEOUT = 1000


def prepare_tbox_graph(tbox_path: Path) -> Graph:
	"""Load a TBox and remove declarations Owlready2 cannot materialize safely."""
	graph = Graph().parse(tbox_path, format="turtle")
	filtered = Graph()

	for subject, predicate, obj in graph:
		if predicate == RDF.type and obj in {
			OWL.AnnotationProperty,
			OWL.DatatypeProperty,
			OWL.Ontology,
			RDFS.Datatype,
		}:
			continue
		filtered.add((subject, predicate, obj))

	return filtered


def collect_data_subjects(input_path: Path) -> set[URIRef | BNode]:
	"""Collect the resource subjects that define the input ABox."""
	graph = Graph().parse(input_path, format="turtle")
	return {subject for subject in graph.subjects() if isinstance(subject, (URIRef, BNode))}



def strip_owl_imports(graph: Graph) -> Graph:
	"""Return a copy of the graph without owl:imports triples."""
	cleaned = Graph()
	bind_graph_namespaces(cleaned, graph)
	for triple in graph:
		if triple[1] == OWL.imports:
			continue
		cleaned.add(triple)
	return cleaned


def explanation_sort_key(explanation) -> tuple[int, int, tuple[str, ...]]:
	axioms = [str(axiom.toString()) for axiom in explanation.getAxioms()]
	return (
		len(axioms),
		sum(len(axiom) for axiom in axioms),
		tuple(sorted(axioms)),
	)


def pick_shortest_explanation(explanations):
	return min(explanations, key=explanation_sort_key)


def _iri_term(java_iri) -> URIRef:
	return URIRef(str(java_iri))


def axiom_to_triples(axiom) -> set[tuple[object, object, object]]:
	"""Convert a Java OWL axiom into the rdflib triples it represents."""
	kind = str(axiom.getAxiomType().getName())
	triples: set[tuple[object, object, object]] = set()

	try:
		if kind == "ClassAssertion":
			individual = axiom.getIndividual().asOWLNamedIndividual()
			class_expression = axiom.getClassExpression().asOWLClass()
			triples.add((_iri_term(individual.getIRI()), RDF.type, _iri_term(class_expression.getIRI())))
		elif kind == "ObjectPropertyAssertion":
			subject = axiom.getSubject().asOWLNamedIndividual()
			obj = axiom.getObject().asOWLNamedIndividual()
			prop = axiom.getProperty().getNamedProperty()
			triples.add((_iri_term(subject.getIRI()), _iri_term(prop.getIRI()), _iri_term(obj.getIRI())))
		elif kind == "DataPropertyAssertion":
			subject = axiom.getSubject().asOWLNamedIndividual()
			prop = axiom.getProperty().getNamedProperty()
			literal = axiom.getObject()
			lang = str(literal.getLang()) if hasattr(literal, "getLang") and str(literal.getLang()) else None
			datatype = literal.getDatatype()
			if datatype is not None:
				rdflib_literal = Literal(str(literal.getLiteral()), datatype=_iri_term(datatype.getIRI()))
			elif lang:
				rdflib_literal = Literal(str(literal.getLiteral()), lang=lang)
			else:
				rdflib_literal = Literal(str(literal.getLiteral()))
			triples.add((_iri_term(subject.getIRI()), _iri_term(prop.getIRI()), rdflib_literal))
		elif kind in {"SameIndividual", "DifferentIndividuals"}:
			individuals = [individual.asOWLNamedIndividual() for individual in axiom.getIndividualsAsList()]
			predicate = OWL.sameAs if kind == "SameIndividual" else OWL.differentFrom
			for index, left in enumerate(individuals):
				for right in individuals[index + 1 :]:
					triples.add((_iri_term(left.getIRI()), predicate, _iri_term(right.getIRI())))
	except Exception:
		return set()

	return triples


def axiom_is_abox(axiom, graph: Graph) -> bool:
	return any(triple in graph for triple in axiom_to_triples(axiom))


def explanation_abox_axioms(explanation, abox_axiom_strings: set[str]) -> list[object]:
	return [
		axiom
		for axiom in explanation.getAxioms()
		if str(axiom.toString()) in abox_axiom_strings
	]


def remove_axiom_triples(graph: Graph, axiom) -> Graph:
	triples_to_remove = axiom_to_triples(axiom)
	if not triples_to_remove:
		return graph

	reduced_graph = Graph()
	bind_graph_namespaces(reduced_graph, graph)
	for triple in graph:
		if triple not in triples_to_remove:
			reduced_graph.add(triple)
	return reduced_graph


def graph_fingerprint(graph: Graph) -> tuple[str, ...]:
	return tuple(sorted(str(triple) for triple in graph))


@contextmanager
def temporary_turtle_file(graph: Graph):
	with tempfile.NamedTemporaryFile(suffix=".ttl", mode="w", encoding="utf-8", delete=False) as temp_file:
		temp_file.write(graph.serialize(format="turtle"))
		temp_path = Path(temp_file.name)
	try:
		yield temp_path
	finally:
		temp_path.unlink(missing_ok=True)


def bind_graph_namespaces(target: Graph, *sources: Graph) -> None:
	seen: set[tuple[str, str]] = set()
	for source in sources:
		for prefix, namespace in source.namespaces():
			key = (str(prefix), str(namespace))
			if key in seen:
				continue
			seen.add(key)
			target.bind(prefix, namespace)


def materialize_graph_from_graph(
	input_graph: Graph,
	tbox_path: Path,
	*,
	keep_reasoner_output: bool = False,
) -> Graph:
	"""Materialize a consistent graph by reusing the file-based Owlready2 path."""
	with temporary_turtle_file(input_graph) as input_path:
		with tempfile.NamedTemporaryFile(suffix=".ttl", delete=False) as temp_output:
			output_path = Path(temp_output.name)
		try:
			materialize_closure(
				input_path,
				tbox_path,
				output_path,
				keep_reasoner_output=keep_reasoner_output,
			)
			result_graph = Graph().parse(output_path, format="turtle")
			bind_graph_namespaces(result_graph, input_graph, prepare_tbox_graph(tbox_path))
			return result_graph
		finally:
			output_path.unlink(missing_ok=True)


def brave_closure(
	input_graph: Graph,
	tbox_graph: Graph,
	tbox_path: Path,
	reasoner_factory,
	abox_axiom_strings: set[str],
	explanation_limit: int,
	timeout: int,
	keep_reasoner_output: bool = False,
	visited: set[tuple[str, ...]] | None = None,
) -> Graph:
	"""Compute the brave-semantics closure by branching over the shortest explanation."""
	if visited is None:
		visited = set()
	fingerprint = graph_fingerprint(input_graph)
	if fingerprint in visited:
		return Graph()
	visited.add(fingerprint)

	with temporary_turtle_file(input_graph) as temp_input_path:
		_, explanations = compute_explanations(
			temp_input_path,
			tbox_graph,
			reasoner_factory,
			explanation_limit=explanation_limit,
			timeout=timeout,
		)

	if explanations.size() == 0:
		return materialize_graph_from_graph(
			input_graph,
			tbox_path,
			keep_reasoner_output=keep_reasoner_output,
		)

	shortest_explanation = pick_shortest_explanation(explanations)
	abox_axioms = explanation_abox_axioms(shortest_explanation, abox_axiom_strings)
	if not abox_axioms:
		return materialize_graph_from_graph(
			input_graph,
			tbox_path,
			keep_reasoner_output=keep_reasoner_output,
		)

	closure_union = Graph()
	bind_graph_namespaces(closure_union, input_graph, tbox_graph)
	for axiom in abox_axioms:
		reduced_graph = remove_axiom_triples(input_graph, axiom)
		if graph_fingerprint(reduced_graph) == fingerprint:
			continue
		branch_closure = brave_closure(
			reduced_graph,
			tbox_graph,
			tbox_path,
			reasoner_factory,
			abox_axiom_strings,
			explanation_limit=explanation_limit,
			timeout=timeout,
			keep_reasoner_output=keep_reasoner_output,
			visited=visited,
		)
		closure_union += branch_closure

	return strip_owl_imports(closure_union)


def default_output_path(input_path: Path) -> Path:
	"""Return the default sibling output path for the inferred graph."""
	suffix = input_path.suffix or ".ttl"
	if suffix.lower() != ".ttl":
		suffix = ".ttl"
	return input_path.with_name(f"{input_path.stem}_inferred{suffix}")


def collect_input_paths(input_path: Path) -> list[Path]:
	"""Collect input TTL files from a file path or recursively from a directory."""
	if input_path.is_file():
		return [input_path]

	paths = sorted(
		[
			path
			for path in input_path.rglob("*.ttl")
			if path.is_file() and not path.name.endswith("_inferred.ttl")
		]
	)
	if not paths:
		raise FileNotFoundError(f"No .ttl files found under directory: {input_path}")
	return paths


def resolve_output_path(source_path: Path, root_input: Path, output_arg: Path | None) -> Path:
	"""Resolve output path for single-file and directory batch modes."""
	if root_input.is_file():
		if output_arg is None:
			return default_output_path(source_path)
		if output_arg.exists() and output_arg.is_dir():
			return output_arg / default_output_path(source_path).name
		return output_arg

	if output_arg is None:
		return default_output_path(source_path)

	relative_source = source_path.relative_to(root_input)
	return output_arg / relative_source.parent / default_output_path(source_path).name


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Materialize inferential closure of a Turtle knowledge graph using Owlready2, "
			"with brave semantics for inconsistent ontologies."
		)
	)
	parser.add_argument(
		"input",
		type=Path,
		help="Path to an input Turtle file or directory containing Turtle files.",
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=None,
		help=(
			"Output path. For a single input file, this is the output file path. "
			"For directory input, this must be an output directory. "
			"If omitted, each inferred file is written next to its source as "
			"<input_stem>_inferred.ttl."
		),
	)
	parser.add_argument(
		"--tbox",
		type=Path,
		default=DEFAULT_TBOX_PATH,
		help=(
			"Path to the separate TBox Turtle file. Defaults to "
			f"{DEFAULT_TBOX_PATH}"
		),
	)
	parser.add_argument(
		"--keep-reasoner-output",
		action="store_true",
		help="Show Owlready2/Pellet output instead of suppressing it.",
	)
	parser.add_argument(
		"--explanation-limit",
		type=int,
		default=DEFAULT_EXPLANATION_LIMIT,
		help="Maximum number of explanations to request when checking inconsistency.",
	)
	parser.add_argument(
		"--timeout",
		type=int,
		default=DEFAULT_REASONER_TIMEOUT,
		help="Timeout passed to the explanation generator factory.",
	)
	parser.add_argument(
		"--jar-classpath",
		type=str,
		default=DEFAULT_JAR_CLASSPATH,
		help="Classpath for OWLAPI/Pellet jars (supports wildcard).",
	)
	return parser.parse_args()


def load_ontology(world: World, ontology_path: Path, *, graph: Graph | None = None) -> object:
	"""Load a Turtle file into a fresh Owlready2 world."""
	ontology_iri = ontology_path.resolve().as_uri()
	ontology = world.get_ontology(ontology_iri)

	try:
		turtle_graph = graph or Graph().parse(ontology_path, format="turtle")
		with tempfile.NamedTemporaryFile(suffix=".rdf", mode="w+b") as temp_file:
			rdfxml_text = turtle_graph.serialize(format="xml")
			temp_file.write(rdfxml_text.encode("utf-8") if isinstance(rdfxml_text, str) else rdfxml_text)
			temp_file.flush()
			temp_file.seek(0)
			ontology.load(fileobj=temp_file, format="rdfxml")
	except Exception as exc:
		raise RuntimeError(f"Failed to load Turtle graph from {ontology_path}") from exc

	return ontology


def load_ontologies(input_path: Path, tbox_path: Path) -> tuple[World, object, object]:
	"""Load the data graph and TBox into a fresh Owlready2 world."""
	world = World()
	data_ontology = load_ontology(world, input_path)
	tbox_ontology = load_ontology(world, tbox_path, graph=prepare_tbox_graph(tbox_path))
	return world, data_ontology, tbox_ontology


def materialize_closure(
	input_path: Path,
	tbox_path: Path,
	output_path: Path,
	keep_reasoner_output: bool = False,
) -> None:
	"""Run inference on the input graph and write the materialized graph."""
	if not tbox_path.exists():
		raise FileNotFoundError(f"TBox graph not found: {tbox_path}")

	input_graph = Graph().parse(input_path, format="turtle")
	input_graph = strip_owl_imports(input_graph)
	data_subjects = collect_data_subjects(input_path)
	world, data_ontology, tbox_ontology = load_ontologies(input_path, tbox_path)

	reasoner_context = contextlib.nullcontext()
	if not keep_reasoner_output:
		reasoner_context = contextlib.ExitStack()
		reasoner_context.enter_context(contextlib.redirect_stdout(io.StringIO()))
		reasoner_context.enter_context(contextlib.redirect_stderr(io.StringIO()))

	with reasoner_context:
		try:
			sync_reasoner_pellet(
				[data_ontology, tbox_ontology],
				infer_property_values=True,
				infer_data_property_values=True,
			)
		except TypeError:
			# Older Owlready2 releases may not accept infer_data_property_values.
			sync_reasoner_pellet(
				[data_ontology, tbox_ontology],
				infer_property_values=True,
			)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_graph = Graph()
	bind_graph_namespaces(output_graph, input_graph, prepare_tbox_graph(tbox_path))
	for triple in world.as_rdflib_graph():
		subject = triple[0]
		if isinstance(subject, (URIRef, BNode)) and subject in data_subjects:
			output_graph.add(triple)
	output_graph = strip_owl_imports(output_graph)
	output_graph.serialize(destination=str(output_path), format="turtle")


def main() -> None:
	args = parse_args()
	suppress_known_java_warnings()

	root_input = args.input
	if not root_input.exists():
		raise FileNotFoundError(f"Input path not found: {root_input}")
	if not args.tbox.exists():
		raise FileNotFoundError(f"TBox graph not found: {args.tbox}")
	if root_input.is_dir() and args.output is not None and args.output.suffix.lower() == ".ttl":
		raise ValueError("When input is a directory, --output must be a directory path, not a .ttl file.")

	input_paths = collect_input_paths(root_input)

	tbox_graph = load_rdf(args.tbox)

	ensure_jvm(args.jar_classpath)
	suppress_java_stderr()
	reasoner_factory = jpype.JClass("com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory").getInstance()

	processed = 0
	failed = 0
	progress_iter = tqdm(input_paths, desc="Inferring closures", unit="file")
	progress_write = tqdm.write if hasattr(tqdm, "write") else print

	for input_path in progress_iter:
		try:
			input_graph = load_rdf(input_path)
			input_graph = strip_owl_imports(input_graph)

			with temporary_turtle_file(input_graph) as temp_input_path:
				ontology, explanations = compute_explanations(
					temp_input_path,
					tbox_graph,
					reasoner_factory,
					explanation_limit=args.explanation_limit,
					timeout=args.timeout,
				)
			abox_axiom_strings = {str(ax.toString()) for ax in ontology.getABoxAxioms(True)}

			if explanations.size() == 0:
				result_graph = materialize_graph_from_graph(
					input_graph,
					args.tbox,
					keep_reasoner_output=args.keep_reasoner_output,
				)
			else:
				result_graph = brave_closure(
					input_graph,
					tbox_graph,
					args.tbox,
					reasoner_factory,
					abox_axiom_strings,
					explanation_limit=args.explanation_limit,
					timeout=args.timeout,
					keep_reasoner_output=args.keep_reasoner_output,
				)

			bind_graph_namespaces(result_graph, input_graph, tbox_graph)
			output_path = resolve_output_path(input_path, root_input, args.output)
			output_path.parent.mkdir(parents=True, exist_ok=True)
			result_graph = strip_owl_imports(result_graph)
			result_graph.serialize(destination=str(output_path), format="turtle")
			processed += 1
			progress_write(f"Wrote inferred graph to {output_path}")
		except Exception as exc:
			failed += 1
			progress_write(f"Failed for {input_path}: {exc}")

	if failed > 0:
		raise RuntimeError(f"Inference completed with failures: {processed} succeeded, {failed} failed.")

	if len(input_paths) > 1:
		print(f"Finished batch inference: {processed} file(s) processed.")


if __name__ == "__main__":
	main()
