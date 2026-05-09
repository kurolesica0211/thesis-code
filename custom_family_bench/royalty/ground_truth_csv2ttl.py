#!/usr/bin/env python3
"""Convert royalty family CSV rows into gold TTL triples.

This script intentionally emits only two ontology predicates:
- :hasParent
- :hasSex
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef


MALE_WIKIDATA = "http://www.wikidata.org/entity/Q6581097"
FEMALE_WIKIDATA = "http://www.wikidata.org/entity/Q6581072"

ONTOLOGY_PREFIX = "http://example.com/family_TBOX.ttl#"
DATA_PREFIX = "http://example.com/data#"
WIKIDATA_PREFIX = "http://www.wikidata.org/entity/"
DATA_URI = URIRef(DATA_PREFIX)
TBOX_URI = URIRef("http://example.com/family_TBOX.ttl#")

ONT_NS = Namespace(ONTOLOGY_PREFIX)
DATA_NS = Namespace(DATA_PREFIX)
WDT_NS = Namespace(WIKIDATA_PREFIX)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert royalty family CSV to TTL gold triples."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("custom_family_bench/royalty/ground_truth.csv"),
        help="Path to source CSV (default: custom_family_bench/royalty/ground_truth.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("custom_family_bench/royalty/ground_truth.ttl"),
        help="Path to output TTL (default: custom_family_bench/royalty/ground_truth.ttl)",
    )
    return parser.parse_args()


def proper_label(label: str) -> str:
    return label.strip("\"").replace(" ", "_").replace("|", "-").replace(",", "-").replace(".", "").replace("(?)", "").strip("_").replace("’", "").replace("'", "")


def gender_to_ontology_value(gender_uri: str) -> str | None:
    normalized = gender_uri.strip().lower()
    if gender_uri == MALE_WIKIDATA or normalized == "male":
        return "Male"
    if gender_uri == FEMALE_WIKIDATA or normalized == "female":
        return "Female"
    return None


def convert_csv_to_ttl(input_path: Path, output_path: Path) -> None:
    graph = Graph()
    graph.bind("", ONTOLOGY_PREFIX)
    graph.bind("data", DATA_PREFIX)
    graph.bind("wdt", WIKIDATA_PREFIX)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)

    # Declare the test ontology and import the TBOX
    graph.add((DATA_URI, RDF.type, OWL.Ontology))
    graph.add((DATA_URI, OWL.imports, TBOX_URI))

    # Create sex individuals
    male_individual = DATA_NS.male
    female_individual = DATA_NS.female
    graph.add((male_individual, RDF.type, ONT_NS.Male))
    graph.add((female_individual, RDF.type, ONT_NS.Female))
    graph.add((DATA_NS.wdtLink, RDF.type, OWL.AnnotationProperty))

    def row_value(row: dict[str, str], *keys: str) -> str:
        for key in keys:
            value = (row.get(key) or "").strip()
            if value:
                return value
        return ""

    with input_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required_columns = {"item", "parent", "genderLabel", "itemLabel", "parentLabel"}
        missing = required_columns.difference(reader.fieldnames or [])
        if missing:
            missing_cols = ", ".join(sorted(missing))
            raise ValueError(f"Missing required CSV columns: {missing_cols}")

        for row in reader:
            item = URIRef(row_value(row, "item"))
            item_label_text = row_value(row, "itemLabel")
            itemLabel = DATA_NS[f"{proper_label(item_label_text)}"]
            
            ext = list(graph.objects(itemLabel, DATA_NS.wdtLink))
            if len(ext) > 0 and item not in ext:
                itemLabel += f"_{len(ext)}"
            
            parent = URIRef(row_value(row, "parent", "ancestor"))
            parent_label_text = row_value(row, "parentLabel", "ancestorLabel")
            ancestorLabel = DATA_NS[f"{proper_label(parent_label_text)}"]
            
            ext_a = list(graph.objects(ancestorLabel, DATA_NS.wdtLink))
            if len(ext_a) > 0 and parent not in ext_a:
                ancestorLabel += f"_{len(ext_a)}"
            
            gender = row_value(row, "genderLabel", "gender")

            if item and parent:
                graph.add((itemLabel, ONT_NS.hasParent, ancestorLabel))
                graph.add((itemLabel, DATA_NS.wdtLink, item))
                graph.add((ancestorLabel, DATA_NS.wdtLink, parent))
                graph.add((itemLabel, RDFS.label, Literal(item_label_text)))
                graph.add((ancestorLabel, RDFS.label, Literal(parent_label_text)))
                graph.add((itemLabel, RDF.type, ONT_NS.Person))
                graph.add((ancestorLabel, RDF.type, ONT_NS.Person))

            sex_name = gender_to_ontology_value(gender)
            if sex_name == "Male":
                sex_value = male_individual
            elif sex_name == "Female":
                sex_value = female_individual
            else:
                sex_value = None
            if item and sex_value:
                graph.add((itemLabel, ONT_NS.hasSex, sex_value))
    
    graph.serialize(output_path, "turtle")


def main() -> None:
    args = parse_args()
    convert_csv_to_ttl(args.input, args.output)
    print(f"Wrote TTL to {args.output}")


if __name__ == "__main__":
    main()
