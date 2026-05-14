#!/usr/bin/env python3
"""Match extracted delta graph entities to ground-truth royalty entities.

For each task folder inside a results run directory, this script:
- pairs the folder with the corresponding text file by sorted index,
- finds the main ground-truth entity for that text via ground_truth.csv,
- collects the main entity's one-hop and two-hop non-metadata neighborhood,
- filters those candidates to entities that are linked from the CSV,
- matches extracted entity local names to those candidate labels using a
  SentenceTransformer model,
- writes a JSON map into the task folder, and
- writes a global debug JSON file under scripts/ with unmatched entities last.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from sentence_transformers import SentenceTransformer, util


DEFAULT_RESULTS_ROOT = Path("results")
DEFAULT_TEXT_DIR = Path("custom_family_bench/royalty/denoised_texts_llama")
DEFAULT_CSV = Path("custom_family_bench/royalty/ground_truth.csv")
DEFAULT_GRAPH = Path("custom_family_bench/royalty/ground_truth_inferred.ttl")
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_THRESHOLD = 0.7
DEFAULT_FOLDER_OUTPUT = "entity_match_map.json"
DEFAULT_GLOBAL_OUTPUT = Path("scripts/royalty_entity_match_debug.json")

DATA = Namespace("http://example.com/data#")
ONTOLOGY = Namespace("http://example.com/family_TBOX.ttl#")
METADATA_PREDICATES = {RDF.type, DATA.wdtLink, RDFS.label, ONTOLOGY.hasSex}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Match extracted delta graph entities to ground-truth royalty entities."
    )
    parser.add_argument(
        "--results-root",
        type=Path,
        default=DEFAULT_RESULTS_ROOT,
        help="Root results directory containing run subdirectories.",
    )
    parser.add_argument(
        "--run-directory",
        dest="run_directories",
        action="append",
        type=Path,
        help=(
            "Optional run directory to process. Can be passed multiple times. "
            "If omitted, all run directories under --results-root are processed."
        ),
    )
    parser.add_argument(
        "--text-dir",
        type=Path,
        default=DEFAULT_TEXT_DIR,
        help="Directory containing the sorted denoised text files.",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="Royalty ground-truth CSV file.",
    )
    parser.add_argument(
        "--ground-truth-graph",
        type=Path,
        default=DEFAULT_GRAPH,
        help="Full dataset-level ground-truth KG in Turtle format.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="Cosine similarity threshold for a valid match.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="SentenceTransformer model name used for matching.",
    )
    parser.add_argument(
        "--folder-output-name",
        default=DEFAULT_FOLDER_OUTPUT,
        help="JSON filename written into each task folder.",
    )
    parser.add_argument(
        "--global-output",
        type=Path,
        default=DEFAULT_GLOBAL_OUTPUT,
        help="Global JSON debug output path.",
    )
    return parser.parse_args()


def sort_key(path: Path) -> tuple[int, str]:
    prefix = path.name.split("_", 1)[0]
    try:
        return (int(prefix), path.name)
    except ValueError:
        return (sys.maxsize, path.name)


def local_name(value: str) -> str:
    if "#" in value:
        return value.rsplit("#", 1)[-1]
    if "/" in value:
        return value.rsplit("/", 1)[-1]
    return value


def semantic_form(value: str) -> str:
    text = unquote(value)
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = text.replace("_", " ").replace("-", " ")
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def article_key(article_url: str) -> str:
    return semantic_form(urlsplit(article_url).path.rsplit("/", 1)[-1])


def filename_key(file_path: Path) -> str:
    return semantic_form(file_path.stem)


def qid_from_uri(uri: URIRef | None) -> str | None:
    if uri is None:
        return None
    value = str(uri)
    if "/" in value:
        return value.rsplit("/", 1)[-1]
    return value or None


def load_csv_index(csv_path: Path) -> tuple[dict[str, dict[str, str]], dict[str, str], set[str]]:
    article_to_row: dict[str, dict[str, str]] = {}
    label_by_qid: dict[str, str] = {}
    qids_in_csv: set[str] = set()

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"item", "parent", "itemLabel", "parentLabel", "article"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")

        for row in reader:
            row_article = article_key(row.get("article", ""))
            if row_article and row_article not in article_to_row:
                article_to_row[row_article] = row

            item_value = (row.get("item") or "").strip()
            parent_value = (row.get("parent") or "").strip()
            item_qid = qid_from_uri(URIRef(item_value)) if item_value else None
            parent_qid = qid_from_uri(URIRef(parent_value)) if parent_value else None

            item_label = (row.get("itemLabel") or "").strip()
            parent_label = (row.get("parentLabel") or "").strip()

            if item_qid:
                qids_in_csv.add(item_qid)
                if item_label and item_qid not in label_by_qid:
                    label_by_qid[item_qid] = item_label
            if parent_qid:
                qids_in_csv.add(parent_qid)
                if parent_label and parent_qid not in label_by_qid:
                    label_by_qid[parent_qid] = parent_label

    return article_to_row, label_by_qid, qids_in_csv


def load_ground_truth(graph_path: Path, csv_label_by_qid: dict[str, str], qids_in_csv: set[str]) -> tuple[Graph, dict[str, URIRef], dict[str, str]]:
    graph = Graph()
    graph.parse(graph_path.as_posix(), format="turtle")

    entity_by_qid: dict[str, URIRef] = {}
    label_by_qid: dict[str, str] = {}

    for subject in graph.subjects(DATA.wdtLink, None):
        if not isinstance(subject, URIRef):
            continue
        qid = qid_from_uri(graph.value(subject, DATA.wdtLink))
        if not qid or qid not in qids_in_csv:
            continue

        entity_by_qid[qid] = subject
        label = graph.value(subject, RDFS.label)
        if label is not None:
            label_by_qid[qid] = str(label)
        elif qid in csv_label_by_qid:
            label_by_qid[qid] = csv_label_by_qid[qid]

    for qid, label in csv_label_by_qid.items():
        label_by_qid.setdefault(qid, label)

    return graph, entity_by_qid, label_by_qid


def discover_run_directories(results_root: Path) -> list[Path]:
    run_directories: list[Path] = []
    if not results_root.exists():
        raise FileNotFoundError(f"Results root not found: {results_root}")

    for child in sorted(results_root.iterdir()):
        if not child.is_dir():
            continue
        has_delta_graph = any(
            grandchild.is_dir() and (grandchild / "delta_graph.ttl").exists()
            for grandchild in child.iterdir()
        )
        if has_delta_graph:
            run_directories.append(child)
    return run_directories


def collect_extracted_entities(graph: Graph) -> list[URIRef]:
    entities: set[URIRef] = set()
    for subject, predicate, obj in graph:
        if predicate not in METADATA_PREDICATES and isinstance(subject, URIRef):
            entities.add(subject)
        if predicate not in METADATA_PREDICATES and isinstance(obj, URIRef):
            entities.add(obj)
    return sorted(entities, key=str)


def is_person_entity(entity_uri: URIRef | str, graph: Graph) -> bool:
    """Check if an entity has a person-like type (Person, Man, Woman, Ancestor)."""
    entity_ref = URIRef(entity_uri) if isinstance(entity_uri, str) else entity_uri
    person_types = {
        ONTOLOGY.Person,
        ONTOLOGY.Man,
        ONTOLOGY.Woman,
        ONTOLOGY.Ancestor,
    }
    for entity_type in graph.objects(entity_ref, RDF.type):
        if entity_type in person_types:
            return True
    return False


def collect_candidate_entities(graph: Graph, start_entity: URIRef, max_depth: int = 2) -> dict[str, int]:
    candidates: dict[str, int] = {str(start_entity): 0}
    frontier: set[URIRef] = {start_entity}
    visited: set[URIRef] = {start_entity}

    for depth in range(1, max_depth + 1):
        next_frontier: set[URIRef] = set()
        for node in frontier:
            for _, predicate, obj in graph.triples((node, None, None)):
                if predicate in METADATA_PREDICATES or not isinstance(obj, URIRef):
                    continue
                if obj in visited:
                    continue
                visited.add(obj)
                next_frontier.add(obj)
                candidates[str(obj)] = depth
        frontier = next_frontier

    return candidates


def match_entities(
    extracted_entities: list[URIRef],
    candidate_entities: dict[str, int],
    graph: Graph,
    label_by_qid: dict[str, str],
    model: SentenceTransformer,
    threshold: float,
) -> tuple[list[dict[str, Any]], int]:
    candidate_rows: list[dict[str, Any]] = []
    candidate_texts: list[str] = []

    for candidate_uri, depth in candidate_entities.items():
        qid = qid_from_uri(graph.value(URIRef(candidate_uri), DATA.wdtLink))
        if not qid:
            continue

        label = label_by_qid.get(qid)
        if not label:
            label_obj = graph.value(URIRef(candidate_uri), RDFS.label)
            label = str(label_obj) if label_obj is not None else local_name(candidate_uri)

        candidate_rows.append(
            {
                "uri": candidate_uri,
                "qid": qid,
                "label": label,
                "embedding_text": semantic_form(label),
                "distance": depth,
            }
        )
        candidate_texts.append(semantic_form(label))

    if not candidate_rows:
        debug_rows = []
        for extracted in extracted_entities:
            debug_rows.append(
                {
                    "extracted_uri": str(extracted),
                    "extracted_local_name": local_name(str(extracted)),
                    "embedding_text": semantic_form(local_name(str(extracted))),
                    "matched": False,
                    "score": None,
                    "ground_truth_uri": None,
                    "ground_truth_qid": None,
                    "ground_truth_label": None,
                    "ground_truth_distance": None,
                    "best_candidate_label": None,
                    "best_candidate_qid": None,
                    "best_candidate_score": None,
                }
            )
        return debug_rows, 0

    extracted_rows: list[dict[str, Any]] = []
    extracted_texts = [semantic_form(local_name(str(entity))) for entity in extracted_entities]

    extracted_embeddings = model.encode(
        extracted_texts,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    candidate_embeddings = model.encode(
        candidate_texts,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    similarity_matrix = util.cos_sim(extracted_embeddings, candidate_embeddings)

    matched_count = 0
    for index, extracted in enumerate(extracted_entities):
        scores = similarity_matrix[index].cpu().tolist()
        best_index = max(range(len(scores)), key=scores.__getitem__)
        best_score = float(scores[best_index])
        best_candidate = candidate_rows[best_index]

        if best_score >= threshold:
            matched_count += 1
            matched = True
            ground_truth_uri = best_candidate["uri"]
            ground_truth_qid = best_candidate["qid"]
            ground_truth_label = best_candidate["label"]
            ground_truth_distance = best_candidate["distance"]
        else:
            matched = False
            ground_truth_uri = None
            ground_truth_qid = None
            ground_truth_label = None
            ground_truth_distance = None

        extracted_rows.append(
            {
                "extracted_uri": str(extracted),
                "extracted_local_name": local_name(str(extracted)),
                "embedding_text": extracted_texts[index],
                "matched": matched,
                "score": best_score if matched else None,
                "ground_truth_uri": ground_truth_uri,
                "ground_truth_qid": ground_truth_qid,
                "ground_truth_label": ground_truth_label,
                "ground_truth_distance": ground_truth_distance,
                "best_candidate_label": best_candidate["label"],
                "best_candidate_qid": best_candidate["qid"],
                "best_candidate_score": best_score,
            }
        )

    extracted_rows.sort(
        key=lambda row: (
            0 if row["matched"] else 1,
            -(row["score"] or 0.0),
            row["extracted_local_name"],
        )
    )
    return extracted_rows, matched_count


def build_folder_payload(
    run_directory: Path,
    task_directory: Path,
    text_file: Path,
    csv_row: dict[str, str],
    ground_truth_graph: Graph,
    entity_by_qid: dict[str, URIRef],
    label_by_qid: dict[str, str],
    model: SentenceTransformer,
    threshold: float,
) -> tuple[dict[str, Any], int]:
    delta_graph_path = task_directory / "delta_graph.ttl"
    if not delta_graph_path.exists():
        raise FileNotFoundError(f"Missing delta_graph.ttl: {delta_graph_path}")

    delta_graph = Graph()
    delta_graph.parse(delta_graph_path.as_posix(), format="turtle")

    article = csv_row.get("article", "")
    article_label = csv_row.get("itemLabel", "")
    item_value = (csv_row.get("item") or "").strip()
    item_qid = qid_from_uri(URIRef(item_value)) if item_value else None
    if not item_qid or item_qid not in entity_by_qid:
        raise KeyError(f"Could not find ground-truth entity for {text_file.name} ({item_qid or 'missing QID'})")

    main_entity = entity_by_qid[item_qid]
    main_label = label_by_qid.get(item_qid) or article_label or local_name(str(main_entity))

    candidate_entities = collect_candidate_entities(ground_truth_graph, main_entity, max_depth=2)
    candidate_entities = {
        uri: depth
        for uri, depth in candidate_entities.items()
        if (qid := qid_from_uri(ground_truth_graph.value(URIRef(uri), DATA.wdtLink))) 
        and qid in label_by_qid
        and is_person_entity(uri, ground_truth_graph)
    }

    extracted_entities = collect_extracted_entities(delta_graph)
    extracted_entities = [e for e in extracted_entities if is_person_entity(e, delta_graph)]
    matched_entities, matched_count = match_entities(
        extracted_entities,
        candidate_entities,
        ground_truth_graph,
        label_by_qid,
        model,
        threshold,
    )

    candidate_payload = []
    for candidate_uri, depth in sorted(candidate_entities.items(), key=lambda item: (item[1], item[0])):
        qid = qid_from_uri(ground_truth_graph.value(URIRef(candidate_uri), DATA.wdtLink))
        if not qid:
            continue
        candidate_payload.append(
            {
                "uri": candidate_uri,
                "qid": qid,
                "label": label_by_qid.get(qid),
                "distance": depth,
            }
        )

    payload = {
        "run_directory": run_directory.as_posix(),
        "task_directory": task_directory.as_posix(),
        "text_file": text_file.name,
        "text_key": filename_key(text_file),
        "article": article,
        "article_key": article_key(article) if article else None,
        "main_entity": {
            "uri": str(main_entity),
            "qid": item_qid,
            "label": main_label,
        },
        "candidate_entities": candidate_payload,
        "entities": matched_entities,
        "summary": {
            "entities_total": len(extracted_entities),
            "entities_matched": matched_count,
            "entities_unmatched": len(extracted_entities) - matched_count,
        },
    }
    return payload, matched_count


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()

    text_files = sorted(args.text_dir.glob("*.txt"))
    if not text_files:
        raise FileNotFoundError(f"No text files found in {args.text_dir}")

    article_to_row, csv_label_by_qid, qids_in_csv = load_csv_index(args.csv)
    ground_truth_graph, entity_by_qid, label_by_qid = load_ground_truth(
        args.ground_truth_graph,
        csv_label_by_qid,
        qids_in_csv,
    )

    run_directories = args.run_directories or discover_run_directories(args.results_root)
    if not run_directories:
        raise FileNotFoundError(
            f"No run directories found under {args.results_root}. Use --run-directory to target one explicitly."
        )

    model = SentenceTransformer(args.model)

    all_rows: list[dict[str, Any]] = []
    total_matched = 0
    total_entities = 0

    for run_directory in sorted(run_directories):
        task_directories = sorted(
            [task_dir for task_dir in run_directory.iterdir() if task_dir.is_dir() and (task_dir / "delta_graph.ttl").exists()],
            key=sort_key,
        )

        if len(task_directories) != len(text_files):
            print(
                f"Warning: {run_directory} has {len(task_directories)} task folders but {len(text_files)} text files.",
                file=sys.stderr,
            )

        for index, task_directory in enumerate(task_directories):
            if index >= len(text_files):
                print(
                    f"Warning: skipping {task_directory} because there is no matching text file index {index}.",
                    file=sys.stderr,
                )
                continue

            text_file = text_files[index]
            article_row = article_to_row.get(filename_key(text_file))
            if article_row is None:
                print(f"Warning: no CSV row found for {text_file.name}", file=sys.stderr)
                continue

            payload, matched_count = build_folder_payload(
                run_directory=run_directory,
                task_directory=task_directory,
                text_file=text_file,
                csv_row=article_row,
                ground_truth_graph=ground_truth_graph,
                entity_by_qid=entity_by_qid,
                label_by_qid=label_by_qid,
                model=model,
                threshold=args.threshold,
            )

            total_matched += matched_count
            total_entities += payload["summary"]["entities_total"]
            write_json(task_directory / args.folder_output_name, payload)

            for entity_row in payload["entities"]:
                debug_row = dict(entity_row)
                debug_row.update(
                    {
                        "run_directory": run_directory.as_posix(),
                        "task_directory": task_directory.as_posix(),
                        "text_file": text_file.name,
                        "article": article_row.get("article", ""),
                        "main_entity_qid": payload["main_entity"]["qid"],
                        "main_entity_label": payload["main_entity"]["label"],
                    }
                )
                all_rows.append(debug_row)

    all_rows.sort(
        key=lambda row: -(row.get("best_candidate_score") or 0.0)
    )

    global_payload = {
        "results_root": args.results_root.as_posix(),
        "text_dir": args.text_dir.as_posix(),
        "csv": args.csv.as_posix(),
        "ground_truth_graph": args.ground_truth_graph.as_posix(),
        "threshold": args.threshold,
        "model": args.model,
        "total_entities": total_entities,
        "total_matched": total_matched,
        "total_unmatched": total_entities - total_matched,
        "entities": all_rows,
    }
    write_json(args.global_output, global_payload)

    print(f"Wrote global entity map to {args.global_output}")
    print(f"Successfully mapped entities: {total_matched}")
    print(f"Total entities processed: {total_entities}")


if __name__ == "__main__":
    main()