import sys
from pathlib import Path
from argparse import ArgumentParser
from argparse import Namespace
from contextlib import redirect_stdout, redirect_stderr
from contextlib import contextmanager
import logging
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph
from core.shacl_functions import pyshacl_validate
import pyshacl.entrypoints as pyshacl_entrypoints
from pyshacl import validate as py_validate

from core.shacl_functions import parse_results_graph
from models.data_models import ValidationReport


def parse_args() -> Namespace:
	parser = ArgumentParser()
	parser.add_argument(
		"--ontology",
		required=True
	)
	parser.add_argument(
		"--shapes",
		required=True
	)
	parser.add_argument(
		"--data-graph",
		required=True
	)
	parser.add_argument(
		"--debug-log",
		default="-",
		help="File path to write pyshacl debug output.",
	)
	parser.add_argument(
		"--bypass-merge",
		default=False,
		type=bool,
		help="Whether to bypass the data graph + shacl shapes merge"
	)
	return parser.parse_args()


@contextmanager
def attach_debug_file_handlers(debug_file):
	logger_names = ["pyshacl", "pyshacl-validate"]
	handler = logging.StreamHandler(debug_file)
	handler.setLevel(logging.DEBUG)
	handler.setFormatter(logging.Formatter("%(message)s"))
	original_pyshacl_stderr = pyshacl_entrypoints.stderr

	configured_loggers = []
	for logger_name in logger_names:
		logger = logging.getLogger(logger_name)
		configured_loggers.append((logger, logger.level))
		logger.setLevel(logging.DEBUG)
		logger.addHandler(handler)

	# pyshacl's default logger writes to pyshacl.entrypoints.stderr.
	pyshacl_entrypoints.stderr = debug_file

	try:
		yield
	finally:
		for logger, prev_level in configured_loggers:
			logger.removeHandler(handler)
			logger.setLevel(prev_level)
		pyshacl_entrypoints.stderr = original_pyshacl_stderr
		handler.flush()

args = parse_args()

graph = Graph()
graph = graph.parse(args.data_graph)

ont_graph = Graph()
ont_graph = ont_graph.parse(args.ontology)

shacl_graph = Graph()
shacl_graph = shacl_graph.parse(args.shapes)

if args.debug_log == "-":
    if args.bypass_merge == False:
        conforms, report, _ = pyshacl_validate(graph, ont_graph, shacl_graph)
    else:
        conforms, results_graph, _ = py_validate(
			data_graph=graph,
			shacl_graph=shacl_graph,
			#ont_graph=ont_graph,
			advanced=True,
			abort_on_first=False,
			debug=False
		)
        
        report = ValidationReport(conforms=conforms)
        
        if not conforms:
            report.violations = parse_results_graph(results_graph)
else:
	debug_log_path = Path(args.debug_log)
	debug_log_path.parent.mkdir(parents=True, exist_ok=True)
	with debug_log_path.open("w", encoding="utf-8") as debug_file:
		# Capture both plain stream output and logger output from pyshacl.
		with attach_debug_file_handlers(debug_file):
			with redirect_stdout(debug_file), redirect_stderr(debug_file):
					if args.bypass_merge == False:
						conforms, report, _ = pyshacl_validate(graph, ont_graph, shacl_graph, True)
					else:
						conforms, results_graph, _ = py_validate(
							data_graph=graph,
							shacl_graph=shacl_graph,
							#ont_graph=ont_graph,
							advanced=True,
							abort_on_first=False,
							debug=True
						)
						
						report = ValidationReport(conforms=conforms)
						
						if not conforms:
							report.violations = parse_results_graph(results_graph)

print(report.model_dump())