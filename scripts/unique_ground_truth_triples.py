from pathlib import Path

from rdflib import Graph


root = Path('/Users/momssun/thesis-code/custom_family_bench/royalty/ground_truths')
combined = set()

for ttl_file in sorted(root.glob('*.ttl')):
    graph = Graph()
    graph.parse(ttl_file)
    combined.update(graph)

print(len(combined))
