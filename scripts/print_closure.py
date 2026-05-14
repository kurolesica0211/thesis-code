#!/usr/bin/env python3
"""Print two-hop candidate closure and labels for a given QID from the ground-truth graph.

Usage:
  python scripts/print_closure.py --qid Q2825469

Defaults to: custom_family_bench/royalty/ground_truth_inferred.ttl
"""
from __future__ import annotations

import argparse
from pathlib import Path
from rdflib import Graph, Namespace, RDFS, URIRef
from rdflib.term import Node
from generate_fuzzy_denoised_pairs import build_candidate_closure

DATA_PREFIX = "http://example.com/data#"
ONTOLOGY_PREFIX = "http://example.com/family_TBOX.ttl#"
WIKIDATA_PREFIX = "http://www.wikidata.org/entity/"

DATA_NS = Namespace(DATA_PREFIX)
ONT_NS = Namespace(ONTOLOGY_PREFIX)
WDT_NS = Namespace(WIKIDATA_PREFIX)


def qid_from_uri(value: Node | None) -> str | None:
    if value is None:
        return None
    text = str(value)
    if "/" in text:
        return text.rsplit("/", 1)[-1]
    if "#" in text:
        return text.rsplit("#", 1)[-1]
    return text or None


def main() -> None:
    parser = argparse.ArgumentParser(description="Print candidate closure and labels for a QID")
    parser.add_argument("--qid", required=True, help="Wikidata QID (e.g. Q2825469)")
    parser.add_argument(
        "--graph",
        type=Path,
        default=Path("custom_family_bench/royalty/ground_truth_inferred.ttl"),
        help="Path to ground-truth TTL",
    )
    parser.add_argument("--depth", type=int, default=2, help="Max depth for closure (default 2)")
    args = parser.parse_args()

    g = Graph()
    g.parse(args.graph.as_posix(), format="turtle")

    # Find subject for given qid
    subject = None
    for s in g.subjects(DATA_NS.wdtLink, None):
        if not isinstance(s, URIRef):
            continue
        if qid_from_uri(g.value(s, DATA_NS.wdtLink)) == args.qid:
            subject = s
            break

    if subject is None:
        raise SystemExit(f"QID {args.qid} not found in graph {args.graph}")

    closure = build_candidate_closure(g, subject, max_depth=args.depth)

    # Print results in readable format
    print(f"Candidate closure for {args.qid} (size={len(closure)}), depth={args.depth}:\n")
    for ent in sorted(closure, key=lambda u: str(u)):
        qid = qid_from_uri(g.value(ent, DATA_NS.wdtLink)) or "(no qid)"
        labels = [str(o) for o in g.objects(ent, RDFS.label)]
        aliases = [str(o) for o in g.objects(ent, ONT_NS.alsoKnownAs)]
        print(f"- {qid} <{ent}>")
        if labels:
            for l in labels:
                print(f"    {l}")
        if aliases:
            for a in aliases:
                print(f"    {a}")
        print()


if __name__ == "__main__":
    main()
