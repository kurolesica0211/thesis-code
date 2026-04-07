import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph, URIRef

graph = Graph()
graph.add((URIRef("http://example.com/AAA"), URIRef("http://example.com/bbb"), URIRef("http://example.com/CCC")))

graph.add((URIRef("http://example.com/AAA"), URIRef("http://example.com/bbb"), URIRef("http://example.com/CCC")))

print(graph.serialize(format="turtle"))