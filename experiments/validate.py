import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph
from core.shacl_functions import pyshacl_validate

graph = Graph()
graph = graph.parse("experiments/data_graph.ttl")

ont_graph = Graph()
ont_graph = ont_graph.parse("custom_family_bench/family_TBOX.ttl")

shacl_graph = Graph()
shacl_graph = shacl_graph.parse("custom_family_bench/family_shacl_final.ttl")

conforms, report = pyshacl_validate(graph, ont_graph, shacl_graph)

print(report.model_dump())