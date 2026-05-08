from __future__ import annotations

from rdflib import Graph, URIRef

def strip_ns(qid: str) -> str:
    return qid.split("#")[-1].split("/")[-1]

input_path = "custom_family_bench/british_family_gold.ttl"
graph = Graph()
graph.parse(input_path)
qids_uri = graph.objects(None, URIRef("http://example.com/data#wdtLink"), True)
qids = [strip_ns(str(uri)) for uri in qids_uri]
query = f"""SELECT ?person ?personLabel ?article WHERE {{
  VALUES ?person {{ {" wd:".join(qids)} }}
  ?article schema:about ?person .
  ?article schema:isPartOf <https://en.wikipedia.org/> .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}"""
with open("custom_family_bench/query.txt", "w") as f:
    f.write(query)

print(len(qids))