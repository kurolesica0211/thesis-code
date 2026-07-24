"""Materialize the inferred closure of an RDF/Turtle knowledge graph.

The script loads an input Turtle graph with Owlready2, runs Pellet reasoning,
and serializes the materialized graph back to Turtle.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import multiprocessing
import queue
import tempfile
import sys
import time
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
DEFAULT_REASONER_TIMEOUT = 30000  # ms; passed to OWLAPI's explanation generator factory
DEFAULT_FILE_TIMEOUT = 300


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


def _axiom_triples_present(axiom, graph: Graph) -> bool:
	"""Whether every triple contributed by axiom is still present in graph."""
	triples = axiom_to_triples(axiom)
	if not triples:
		return True
	return all(triple in graph for triple in triples)


def explanation_still_valid(explanation, abox_axiom_strings: set[str], graph: Graph) -> bool:
	"""Whether a previously found explanation still holds against the current (reduced) graph.

	An explanation is a minimal justification: removing any one of its ABox
	axioms breaks that specific derivation. So it remains valid exactly as
	long as none of its ABox axioms have been removed yet, letting a
	still-valid explanation from an ancestor node be reused directly instead
	of re-invoking the reasoner to rediscover the same independent
	inconsistency in every sibling branch.
	"""
	return all(
		_axiom_triples_present(axiom, graph)
		for axiom in explanation_abox_axioms(explanation, abox_axiom_strings)
	)


_FAMILY_NS = "http://example.com/family_TBOX.ttl#"
_HAS_FATHER = URIRef(_FAMILY_NS + "hasFather")
_HAS_MOTHER = URIRef(_FAMILY_NS + "hasMother")
_HAS_PARENT = URIRef(_FAMILY_NS + "hasParent")
_HAS_CHILD = URIRef(_FAMILY_NS + "hasChild")
_MAN_CLASS = URIRef(_FAMILY_NS + "Man")
_WOMAN_CLASS = URIRef(_FAMILY_NS + "Woman")


def _axiom_triple(axiom) -> tuple | None:
	"""Return the single triple an axiom contributes, or None if it maps to zero or several."""
	triples = axiom_to_triples(axiom)
	if len(triples) != 1:
		return None
	return next(iter(triples))


def _is_sex_mismatch_axiom(axiom, graph: Graph) -> bool:
	"""hasFather pointing at a :Woman, or hasMother pointing at a :Man: always wrong."""
	triple = _axiom_triple(axiom)
	if triple is None:
		return False
	_, predicate, obj = triple
	if predicate == _HAS_FATHER:
		return (obj, RDF.type, _WOMAN_CLASS) in graph
	if predicate == _HAS_MOTHER:
		return (obj, RDF.type, _MAN_CLASS) in graph
	return False


def _parents_of(graph: Graph, person) -> set:
	parents = set()
	for pred in (_HAS_FATHER, _HAS_MOTHER, _HAS_PARENT):
		for _, _, parent in graph.triples((person, pred, None)):
			parents.add(parent)
	return parents


def _is_grandparent_duplicate_axiom(axiom, graph: Graph) -> bool:
	"""hasChild(G, C) where G is also a parent of some P who separately claims hasChild(P, C)."""
	triple = _axiom_triple(axiom)
	if triple is None:
		return False
	grandparent, predicate, child = triple
	if predicate != _HAS_CHILD:
		return False
	for parent, _, _ in graph.triples((None, _HAS_CHILD, child)):
		if parent == grandparent:
			continue
		if grandparent in _parents_of(graph, parent):
			return True
	return False


def _branch_pattern_priority(axiom, graph: Graph) -> int:
	"""Lower sorts first: axioms matching a known royalty-dataset error shape before others."""
	if _is_sex_mismatch_axiom(axiom, graph):
		return 0
	if _is_grandparent_duplicate_axiom(axiom, graph):
		return 1
	return 2


def _branch_sort_key(axiom, graph: Graph, other_axiom_string_sets: list[set[str]]) -> tuple[int, int]:
	"""Order branches to try likely-genuine fixes first, breaking ties by hitting-set coverage.

	Reordering never changes correctness (every branch is still explored, the
	union is identical) - it only changes how soon a consistent leaf is
	found, which is what lets subset pruning start cutting off dominated
	branches. Coverage prefers axioms shared by the most other currently
	known explanations (a standard greedy hitting-set heuristic), which
	helps even on files whose error shape doesn't match the patterns above.
	"""
	axiom_key = str(axiom.toString())
	pattern_priority = _branch_pattern_priority(axiom, graph)
	coverage = sum(1 for axiom_strings in other_axiom_string_sets if axiom_key in axiom_strings)
	return (pattern_priority, -coverage)


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
	progress=None,
	depth: int = 0,
	known_explanations: list | None = None,
	removed_so_far: frozenset[str] = frozenset(),
	found_repairs: list[frozenset[str]] | None = None,
) -> Graph:
	"""Compute the brave-semantics closure by branching over the shortest explanation.

	Each call to the reasoner returns up to `explanation_limit` distinct
	justifications, not just one. `known_explanations` carries forward the
	ones a prior call already found but didn't act on (from this same node or
	an ancestor) that are unrelated to the axiom just removed to get here. If
	one of them is still fully intact (none of its ABox axioms removed on
	this path), it's reused directly instead of re-invoking the reasoner to
	rediscover the same independent inconsistency in every sibling branch.

	`found_repairs` records the removed-axiom-set of every consistent leaf
	found anywhere in the search so far (shared across the whole tree, like
	`visited`). Removing axioms only shrinks what's entailed, so a branch
	whose `removed_so_far` is already a superset of some found repair can
	only produce a closure that repair's leaf already subsumes; such
	branches are pruned outright (Reiter hitting-set-tree subset pruning).

	`progress`, if given, is called as `progress(**info)` at each notable step
	(state entered, branch decision, branch started, leaf resolved) so a caller
	can report liveness during what can otherwise be a long, silent recursion.
	"""
	if visited is None:
		visited = set()
	if known_explanations is None:
		known_explanations = []
	if found_repairs is None:
		found_repairs = []

	if any(repair <= removed_so_far for repair in found_repairs):
		if progress is not None:
			progress(depth=depth, explored=len(visited), stage="pruned-dominated")
		return Graph()

	fingerprint = graph_fingerprint(input_graph)
	if fingerprint in visited:
		return Graph()
	visited.add(fingerprint)

	if progress is not None:
		progress(depth=depth, explored=len(visited), stage="checking-consistency")

	still_valid = [
		explanation
		for explanation in known_explanations
		if explanation_still_valid(explanation, abox_axiom_strings, input_graph)
	]

	if still_valid:
		candidates = still_valid
		source = "cache"
	else:
		with temporary_turtle_file(input_graph) as temp_input_path:
			_, explanations = compute_explanations(
				temp_input_path,
				tbox_graph,
				reasoner_factory,
				explanation_limit=explanation_limit,
				timeout=timeout,
			)

		if explanations.size() == 0:
			if progress is not None:
				progress(depth=depth, explored=len(visited), stage="leaf-consistent")
			found_repairs.append(removed_so_far)
			return materialize_graph_from_graph(
				input_graph,
				tbox_path,
				keep_reasoner_output=keep_reasoner_output,
			)

		candidates = list(explanations)
		source = "reasoner"

	shortest_explanation = pick_shortest_explanation(candidates)
	remaining_known = [explanation for explanation in candidates if explanation is not shortest_explanation]
	abox_axioms = explanation_abox_axioms(shortest_explanation, abox_axiom_strings)
	if not abox_axioms:
		if progress is not None:
			progress(depth=depth, explored=len(visited), stage="leaf-no-abox-axioms")
		return materialize_graph_from_graph(
			input_graph,
			tbox_path,
			keep_reasoner_output=keep_reasoner_output,
		)

	other_axiom_string_sets = [
		{str(axiom.toString()) for axiom in explanation_abox_axioms(explanation, abox_axiom_strings)}
		for explanation in remaining_known
	]
	abox_axioms = sorted(
		abox_axioms,
		key=lambda axiom: _branch_sort_key(axiom, input_graph, other_axiom_string_sets),
	)

	if progress is not None:
		progress(
			depth=depth,
			explored=len(visited),
			stage="branching",
			branch_total=len(abox_axioms),
			source=source,
		)

	closure_union = Graph()
	bind_graph_namespaces(closure_union, input_graph, tbox_graph)
	for branch_index, axiom in enumerate(abox_axioms, start=1):
		reduced_graph = remove_axiom_triples(input_graph, axiom)
		if graph_fingerprint(reduced_graph) == fingerprint:
			continue
		if progress is not None:
			progress(
				depth=depth,
				explored=len(visited),
				stage="branch-start",
				branch_index=branch_index,
				branch_total=len(abox_axioms),
			)
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
			progress=progress,
			depth=depth + 1,
			known_explanations=remaining_known,
			removed_so_far=removed_so_far | {str(axiom.toString())},
			found_repairs=found_repairs,
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
		"inputs",
		type=Path,
		nargs="+",
		help=(
			"Path(s) to one or more input Turtle files or directories (e.g. results "
			"folders) containing Turtle files. Multiple directories may be given."
		),
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=None,
		help=(
			"Output path. For a single input file, this is the output file path. "
			"For directory input(s), this must be an output directory. "
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
		"--file-timeout",
		type=int,
		default=DEFAULT_FILE_TIMEOUT,
		help=(
			"Maximum wall-clock seconds to spend inferring a single file before "
			f"it is skipped and reported as timed out. Defaults to {DEFAULT_FILE_TIMEOUT}."
		),
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


def _infer_one_file(
	input_path: Path,
	output_path: Path,
	tbox_path: Path,
	tbox_graph: Graph,
	reasoner_factory,
	explanation_limit: int,
	reasoner_timeout: int,
	keep_reasoner_output: bool,
	result_queue: "multiprocessing.Queue",
) -> None:
	"""Run the full inference pipeline for one file, reporting progress via the queue."""
	input_graph = load_rdf(input_path)
	input_graph = strip_owl_imports(input_graph)

	with temporary_turtle_file(input_graph) as temp_input_path:
		ontology, explanations = compute_explanations(
			temp_input_path,
			tbox_graph,
			reasoner_factory,
			explanation_limit=explanation_limit,
			timeout=reasoner_timeout,
		)
	abox_axiom_strings = {str(ax.toString()) for ax in ontology.getABoxAxioms(True)}
	is_inconsistent = explanations.size() > 0
	result_queue.put({"kind": "consistency", "inconsistent": is_inconsistent})

	if not is_inconsistent:
		result_graph = materialize_graph_from_graph(
			input_graph,
			tbox_path,
			keep_reasoner_output=keep_reasoner_output,
		)
	else:
		def _report_progress(**info) -> None:
			result_queue.put({"kind": "progress", **info})

		result_graph = brave_closure(
			input_graph,
			tbox_graph,
			tbox_path,
			reasoner_factory,
			abox_axiom_strings,
			explanation_limit=explanation_limit,
			timeout=reasoner_timeout,
			keep_reasoner_output=keep_reasoner_output,
			progress=_report_progress,
			known_explanations=list(explanations),
		)

	bind_graph_namespaces(result_graph, input_graph, tbox_graph)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	result_graph = strip_owl_imports(result_graph)
	result_graph.serialize(destination=str(output_path), format="turtle")


def _worker_loop(
	task_queue: "multiprocessing.Queue",
	result_queue: "multiprocessing.Queue",
	tbox_path: Path,
	jar_classpath: str,
	explanation_limit: int,
	reasoner_timeout: int,
	keep_reasoner_output: bool,
) -> None:
	"""Process files from task_queue until poisoned with None.

	Runs in its own process so a file that hangs the reasoner can be killed
	from outside without losing the rest of the batch.
	"""
	suppress_known_java_warnings()
	ensure_jvm(jar_classpath)
	suppress_java_stderr()
	reasoner_factory = jpype.JClass("com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory").getInstance()
	tbox_graph = load_rdf(tbox_path)

	while True:
		task = task_queue.get()
		if task is None:
			return
		input_path, output_path = task
		try:
			_infer_one_file(
				input_path,
				output_path,
				tbox_path,
				tbox_graph,
				reasoner_factory,
				explanation_limit,
				reasoner_timeout,
				keep_reasoner_output,
				result_queue,
			)
			result_queue.put({"kind": "done", "ok": True})
		except Exception as exc:
			result_queue.put({"kind": "done", "ok": False, "error": str(exc)})


def _spawn_worker(
	tbox_path: Path,
	jar_classpath: str,
	explanation_limit: int,
	reasoner_timeout: int,
	keep_reasoner_output: bool,
):
	"""Start a fresh worker process with its own JVM and task/result queues."""
	ctx = multiprocessing.get_context("spawn")
	task_queue = ctx.Queue()
	result_queue = ctx.Queue()
	process = ctx.Process(
		target=_worker_loop,
		args=(task_queue, result_queue, tbox_path, jar_classpath, explanation_limit, reasoner_timeout, keep_reasoner_output),
		daemon=True,
	)
	process.start()
	return process, task_queue, result_queue


def _branch_bar_description(message: dict) -> str:
	stage = message.get("stage")
	depth = message.get("depth", 0)
	if stage == "branching":
		tag = " [cached]" if message.get("source") == "cache" else ""
		return f"Exploring inconsistency (depth {depth}, {message['branch_total']} branch(es)){tag}"
	if stage == "branch-start":
		return f"Exploring inconsistency (depth {depth}, branch {message['branch_index']}/{message['branch_total']})"
	if stage in ("leaf-consistent", "leaf-no-abox-axioms"):
		return f"Exploring inconsistency (depth {depth}, resolving leaf)"
	if stage == "pruned-dominated":
		return f"Exploring inconsistency (depth {depth}, pruning dominated branch)"
	return f"Exploring inconsistency (depth {depth})"


def _await_result(result_queue: "multiprocessing.Queue", deadline: float) -> dict:
	"""Drain status messages for the in-flight file until it finishes or the deadline passes.

	Progress messages from a brave_closure branching search drive a single
	nested tqdm bar (states explored so far) instead of individual print
	lines, so the outer per-file progress bar stays visible and uncluttered.
	"""
	inconsistent = None
	branch_bar = None
	try:
		while True:
			remaining = deadline - time.monotonic()
			if remaining <= 0:
				return {"kind": "timeout", "inconsistent": inconsistent}
			try:
				message = result_queue.get(timeout=remaining)
			except queue.Empty:
				return {"kind": "timeout", "inconsistent": inconsistent}
			if message["kind"] == "consistency":
				inconsistent = message["inconsistent"]
				continue
			if message["kind"] == "progress":
				if branch_bar is None:
					branch_bar = tqdm(
						desc="Exploring inconsistency",
						unit="state",
						position=1,
						leave=False,
					)
				branch_bar.set_description_str(_branch_bar_description(message))
				branch_bar.n = message.get("explored", branch_bar.n)
				branch_bar.refresh()
				continue
			message["inconsistent"] = inconsistent
			return message
	finally:
		if branch_bar is not None:
			branch_bar.close()


def _terminate_worker(process) -> None:
	process.terminate()
	process.join(5)
	if process.is_alive():
		process.kill()
		process.join()


def main() -> None:
	args = parse_args()
	suppress_known_java_warnings()

	root_inputs = args.inputs
	for root_input in root_inputs:
		if not root_input.exists():
			raise FileNotFoundError(f"Input path not found: {root_input}")
	if not args.tbox.exists():
		raise FileNotFoundError(f"TBox graph not found: {args.tbox}")

	multiple_roots = len(root_inputs) > 1
	any_dir_input = any(root_input.is_dir() for root_input in root_inputs)
	if args.output is not None and args.output.suffix.lower() == ".ttl" and (multiple_roots or any_dir_input):
		raise ValueError(
			"When input includes a directory or multiple inputs, --output must be a directory path, not a .ttl file."
		)

	file_entries: list[tuple[Path, Path]] = []
	for root_input in root_inputs:
		for input_path in collect_input_paths(root_input):
			file_entries.append((root_input, input_path))

	progress_write = tqdm.write if hasattr(tqdm, "write") else print

	pending_entries = []
	for root_input, input_path in file_entries:
		if default_output_path(input_path).exists():
			progress_write(f"Skipping {input_path}: inferred sibling already exists.")
			continue
		pending_entries.append((root_input, input_path))

	if not pending_entries:
		print("Nothing to do: all input files already have an inferred sibling.")
		return

	processed = 0
	failed = 0
	inconsistent_count = 0
	timed_out_files: list[Path] = []
	timed_out_inconsistent_count = 0

	process, task_queue, result_queue = _spawn_worker(
		args.tbox, args.jar_classpath, args.explanation_limit, args.timeout, args.keep_reasoner_output
	)
	progress_iter = tqdm(pending_entries, desc="Inferring closures", unit="file", position=0)

	try:
		for root_input, input_path in progress_iter:
			display_path = str(input_path.relative_to(root_input)) if root_input.is_dir() else input_path.name
			progress_iter.set_postfix_str(display_path, refresh=True)
			output_path = resolve_output_path(input_path, root_input, args.output)
			task_queue.put((input_path, output_path))
			deadline = time.monotonic() + args.file_timeout
			outcome = _await_result(result_queue, deadline)

			if outcome["kind"] == "timeout":
				timed_out_files.append(input_path)
				if outcome["inconsistent"]:
					inconsistent_count += 1
					timed_out_inconsistent_count += 1
				progress_write(f"Timed out after {args.file_timeout}s: {input_path}")
				_terminate_worker(process)
				process, task_queue, result_queue = _spawn_worker(
					args.tbox, args.jar_classpath, args.explanation_limit, args.timeout, args.keep_reasoner_output
				)
				continue

			if outcome["inconsistent"]:
				inconsistent_count += 1

			if outcome["ok"]:
				processed += 1
				progress_write(f"Wrote inferred graph to {output_path}")
			else:
				failed += 1
				progress_write(f"Failed for {input_path}: {outcome['error']}")

		task_queue.put(None)
		process.join(5)
	finally:
		if process.is_alive():
			_terminate_worker(process)

	if timed_out_files:
		share = (timed_out_inconsistent_count / inconsistent_count) if inconsistent_count else 0.0
		print(
			f"Timed out on {len(timed_out_files)} file(s) after {args.file_timeout}s "
			f"({share:.1%} of the {inconsistent_count} inconsistent graph(s) encountered):"
		)
		for path in timed_out_files:
			print(f"  - {path}")

	if multiple_roots:
		print(
			f"Finished batch inference across {len(root_inputs)} folder(s): "
			f"{processed} succeeded, {failed} failed, {len(timed_out_files)} timed out."
		)
	elif len(pending_entries) > 1:
		print(f"Finished batch inference: {processed} file(s) processed.")

	if failed > 0:
		raise RuntimeError(f"Inference completed with failures: {processed} succeeded, {failed} failed.")


if __name__ == "__main__":
	main()
