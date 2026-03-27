import sys
from pathlib import Path
import json
import re
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph, RDF, Namespace, URIRef
from litellm import completion
from pydantic import BaseModel

EX = Namespace("http://example.org/data/")

def _label_of(uri: URIRef) -> str:
    """Extract the local name / fragment from a URI."""
    s = str(uri)
    return s.rsplit("#", 1)[-1].rsplit("/", 1)[-1]

def serialize_shape(graph: Graph, shape_uri: URIRef) -> str:
    mini_graph = graph.cbd(shape_uri)
    for prefix, namespace in graph.namespaces():
        mini_graph.bind(prefix, namespace)
    serialized_cleaned = re.sub(r'@prefix.*\n|@base.*\n', '', mini_graph.serialize(format="ttl")).strip()
    return serialized_cleaned

graph = Graph()
graph.parse("experiments/data_graph.ttl", format="ttl")

with open("experiments/validation_report.json", "r", encoding="utf-8") as f:
    report = json.load(f)
    
shacl_shapes = Graph()
shacl_shapes.parse("custom_family_bench/family_TBOX_shacl_closed.ttl", format="ttl")
    
with open("custom_family_bench/family_TBOX.owl", "r", encoding="utf-8") as f:
    ontology = Graph()
    ontology.parse(f, format="xml")

print(
    serialize_shape(ontology, URIRef("http://www.example.com/genealogy.owl#hasPartner"))
)