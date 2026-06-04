from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Iterable, Dict, Set

from rdflib import Graph, URIRef, BNode, Literal, RDF


def load_graph(path: Path, fmt: str | None = None) -> Graph:
    g = Graph()
    if fmt:
        g.parse(str(path), format=fmt)
    else:
        # let rdflib guess format from file extension
        g.parse(str(path))
    return g


def connected_components_rdf(
    graph: Graph,
    ignore_rdf_types: set | None = None,
    ignore_predicates: set | None = None,
) -> list[Set[str]]:
    """Compute connected components of an RDF graph considering only resource nodes.

    ignore_rdf_types: optional set of URIRefs; triples of the form (s, rdf:type, o)
    where o is in this set will be ignored.
    ignore_predicates: optional set of predicates to skip entirely.
    """

    # Nodes are URIRef or BNode from subjects and objects (ignore Literals as nodes)
    adj: Dict[str, Set[str]] = {}
    if ignore_rdf_types is None:
        ignore_rdf_types = set()
    if ignore_predicates is None:
        ignore_predicates = set()

    def ensure_node(n):
        # Skip namespace-root URIs like 'http://example.com/data#' or 'http://example.com/'
        if isinstance(n, URIRef):
            s = str(n)
            if s.endswith("#") or s.endswith("/"):
                return None
        key = str(n)
        if key not in adj:
            adj[key] = set()
        return key

    for s, p, o in graph:
        if p in ignore_predicates:
            continue

        # Optionally ignore rdf:type triples for certain objects
        if p == RDF.type and o in ignore_rdf_types:
            continue

        if isinstance(s, (URIRef, BNode)):
            s_key = ensure_node(s)
        else:
            s_key = None

        if isinstance(o, (URIRef, BNode)):
            o_key = ensure_node(o)
        else:
            o_key = None

        # add undirected edge when both ends are resources
        if s_key is not None and o_key is not None:
            adj[s_key].add(o_key)
            adj[o_key].add(s_key)

    # BFS/DFS to collect components
    seen: Set[str] = set()
    components: list[Set[str]] = []

    for node in adj:
        if node in seen:
            continue
        comp: Set[str] = set()
        q = deque([node])
        seen.add(node)
        while q:
            cur = q.popleft()
            comp.add(cur)
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        components.append(comp)

    return components


def summarize_components(comps: Iterable[Set[str]]) -> dict:
    comps = list(comps)
    sizes = sorted((len(c) for c in comps), reverse=True)
    return {
        "num_fragments": len(sizes),
        "sizes": sizes,
        "num_isolated_nodes": sum(1 for s in sizes if s == 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Count unconnected fragments (connected components) in an RDF graph")
    parser.add_argument("graph", nargs="?", help="Path to RDF file (ttl, rdf, nt, json-ld, etc.). If omitted and --example given, runs the internal example.")
    parser.add_argument("--format", "-f", help="RDF format to pass to rdflib (e.g. turtle, xml, ntriples, json-ld)")
    parser.add_argument("--print-sizes", action="store_true", help="Print component sizes")
    parser.add_argument("--example", action="store_true", help="Run a small built-in example instead of parsing a file")
    args = parser.parse_args()

    if args.example:
        # Build a tiny in-memory graph to test the algorithm
        g = Graph()
        ttl = """
        @prefix ex: <http://example.org/> .
        ex:a ex:knows ex:b .
        ex:b ex:knows ex:c .
        ex:d ex:relatedTo ex:e .
        ex:i ex:knows ex:j .
        ex:g ex:label "hello" .
        ex:h ex:age 30 .
        """
        g.parse(data=ttl, format="turtle")
    else:
        if not args.graph:
            parser.error("either provide a graph path or use --example")
        path = Path(args.graph)
        if not path.exists():
            parser.error(f"file not found: {path}")
        g = load_graph(path, args.format)

    comps = connected_components_rdf(g)
    summary = summarize_components(comps)

    print("Unconnected fragments (connected components) summary")
    print("-" * 48)
    print(f"Total fragments: {summary['num_fragments']}")
    print(f"Isolated nodes (size==1): {summary['num_isolated_nodes']}")
    if args.print_sizes:
        print(f"Component sizes (desc): {summary['sizes']}")


if __name__ == "__main__":
    main()
