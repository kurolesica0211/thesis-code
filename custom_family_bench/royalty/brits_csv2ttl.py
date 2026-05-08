#!/usr/bin/env python3
"""Convert British family CSV rows into gold TTL triples.

This script intentionally emits only two ontology predicates:
- :hasParent
- :hasSex
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from rdflib import Graph, Namespace, URIRef


MALE_WIKIDATA = "http://www.wikidata.org/entity/Q6581097"
FEMALE_WIKIDATA = "http://www.wikidata.org/entity/Q6581072"

ONTOLOGY_PREFIX = "http://example.com/family_TBOX.ttl#"
DATA_PREFIX = "http://example.com/data#"
WIKIDATA_PREFIX = "http://www.wikidata.org/entity/"

ONT_NS = Namespace(ONTOLOGY_PREFIX)
DATA_NS = Namespace(DATA_PREFIX)
WDT_NS = Namespace(WIKIDATA_PREFIX)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert British family CSV to TTL gold triples."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("custom_family_bench/british_family_gold.csv"),
        help="Path to source CSV (default: custom_family_bench/british_family_gold.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("custom_family_bench/british_family_gold.ttl"),
        help="Path to output TTL (default: custom_family_bench/british_family_gold.ttl)",
    )
    return parser.parse_args()


def proper_label(label: str) -> str:
    return label.strip("\"").replace(" ", "_").replace("|", "-").replace(",", "-").replace(".", "").replace("(?)", "").strip("_")


def gender_to_ontology_value(gender_uri: str) -> str | None:
    if gender_uri == MALE_WIKIDATA:
        return "Male"
    if gender_uri == FEMALE_WIKIDATA:
        return "Female"
    return None


def convert_csv_to_ttl(input_path: Path, output_path: Path) -> None:
    graph = Graph()
    graph.bind("", ONTOLOGY_PREFIX)
    graph.bind("data", DATA_PREFIX)
    graph.bind("wdt", WIKIDATA_PREFIX)

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required_columns = {"item", "ancestor", "gender"}
        missing = required_columns.difference(reader.fieldnames or [])
        if missing:
            missing_cols = ", ".join(sorted(missing))
            raise ValueError(f"Missing required CSV columns: {missing_cols}")

        for row in reader:
            item = URIRef((row.get("item") or "").strip())
            itemLabel = DATA_NS[f"{proper_label((row.get("itemLabel") or "").strip())}"]
            
            ext = list(graph.objects(itemLabel, DATA_NS.wdtLink))
            if len(ext) > 0 and item not in ext:
                itemLabel += f"_{len(ext)}"
            
            ancestor = URIRef((row.get("ancestor") or "").strip())
            ancestorLabel = DATA_NS[f"{proper_label((row.get("ancestorLabel") or "").strip())}"]
            
            ext_a = list(graph.objects(ancestorLabel, DATA_NS.wdtLink))
            if len(ext_a) > 0 and ancestor not in ext_a:
                ancestorLabel += f"_{len(ext_a)}"
            
            gender = (row.get("gender") or "").strip()

            if item in WDT_NS and ancestor in WDT_NS:
                graph.add((itemLabel, ONT_NS.hasParent, ancestorLabel))
                graph.add((itemLabel, DATA_NS.wdtLink, item))
                graph.add((ancestorLabel, DATA_NS.wdtLink, ancestor))

            sex_value = ONT_NS[f"{gender_to_ontology_value(gender)}"]
            if item and sex_value:
                graph.add((itemLabel, ONT_NS.hasSex, sex_value))
    
    graph.serialize(output_path, "turtle")


def main() -> None:
    args = parse_args()
    convert_csv_to_ttl(args.input, args.output)
    print(f"Wrote TTL to {args.output}")


if __name__ == "__main__":
    main()
