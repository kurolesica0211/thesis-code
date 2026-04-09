import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph
from core.data_graph_functions import add_literal, remove_literal

graph = Graph()
graph = graph.parse("experiments/data_graph.ttl")

parsed, graph, msg = add_literal(graph, "RandomSubject", "fhkb:hasBirthYear", "1090", "xsd:integer")
print(parsed)
print(msg)
print(graph.serialize(format="turtle"))