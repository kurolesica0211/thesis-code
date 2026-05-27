"""Fuzzy-match extracted delta-graph entities to ground-truth royalty entities.

This script mirrors the JSON layout produced by ``semantic_entity_match.py`` but
uses URI local-name normalization instead of full-text sentence similarity.

For each run directory, task folders are paired with the sorted text files by
index. For the current legacy runs the text filenames come from article slugs in
``ground_truth.csv``; for future runs the script first accepts QID-based text
filenames directly, which keeps the mapping easy to swap later.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import spacy
from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from spacy.matcher import Matcher


DEFAULT_RESULTS_ROOT = Path("results")
DEFAULT_TEXT_DIR = Path("custom_family_bench/royalty/denoised_texts_fuzzy_match")
DEFAULT_CSV = Path("experiments/dataset_creation/ground_truth.csv")
DEFAULT_GROUND_TRUTH_DIR = Path("custom_family_bench/royalty/ground_truths")
DEFAULT_THRESHOLD = 0.74
SPLIT_PART_MIN_SCORE = 0.5
DEFAULT_FOLDER_OUTPUT = "fuzzy_entity_match_map.json"
DEFAULT_GLOBAL_OUTPUT = Path("experiments/metrics/royalty_fuzzy_entity_match_debug.json")

DATA = Namespace("http://example.com/data#")
ONTOLOGY = Namespace("http://example.com/family_TBOX.ttl#")
METADATA_PREDICATES = {RDF.type, DATA.wdtLink, RDFS.label, ONTOLOGY.hasSex, ONTOLOGY.alsoKnownAs, DATA.posIndicesFull, DATA.posIndicesPart}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Match extracted delta graph entities to ground-truth royalty entities using fuzzy URI-name matching."
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
        help="Royalty ground-truth CSV file used for legacy article-slug mapping.",
    )
    parser.add_argument(
        "--ground-truth-dir",
        type=Path,
        default=DEFAULT_GROUND_TRUTH_DIR,
        help="Directory containing per-QID ground-truth Turtle files.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="Similarity threshold for accepting a fuzzy match.",
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


def desanitize_uri_local_name(value: str) -> str:
    """Turn a URI local part into a fuzzy-matchable text form.

    This intentionally mirrors the inverse of the URI sanitization used when
    constructing graph terms: percent-decoding, underscore/hyphen splitting,
    camel-case splitting, and whitespace normalization.
    """

    text = unquote(value)
    text = text.replace("_", " ")
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def semantic_form(value: str) -> str:
    return desanitize_uri_local_name(value)


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
    if "#" in value:
        return value.rsplit("#", 1)[-1]
    return value or None


def load_csv_index(csv_path: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    article_to_row: dict[str, dict[str, str]] = {}
    qid_to_row: dict[str, dict[str, str]] = {}

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"item", "itemLabel", "article"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")

        for row in reader:
            article = (row.get("article") or "").strip()
            item_value = (row.get("item") or "").strip()
            item_qid = qid_from_uri(URIRef(item_value)) if item_value else None

            if article:
                article_to_row.setdefault(article_key(article), row)
            if item_qid:
                qid_to_row.setdefault(item_qid, row)

    return article_to_row, qid_to_row


def discover_run_directories(results_root: Path) -> list[Path]:
    if not results_root.exists():
        raise FileNotFoundError(f"Results root not found: {results_root}")

    run_directories: list[Path] = []
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


def resolve_text_row(
    text_file: Path,
    article_to_row: dict[str, dict[str, str]],
) -> dict[str, str] | None:
    """Resolve the CSV row for a text file.

    Future runs can switch to QID-named files by keeping only the direct-QID
    branch below. For the current legacy runs, filenames still match article
    slugs from the CSV.
    """

    stem = filename_key(text_file)
    if re.fullmatch(r"Q\d+", text_file.stem):
        return {"item": f"http://www.wikidata.org/entity/{text_file.stem}", "article": "", "itemLabel": text_file.stem}
    return article_to_row.get(stem)


def load_ground_truth_graph(ground_truth_dir: Path, qid: str) -> Graph:
    graph_path = ground_truth_dir / f"{qid}.ttl"
    if not graph_path.exists():
        return None

    graph = Graph()
    graph.parse(graph_path.as_posix(), format="turtle")
    return graph


def load_entity_index(graph: Graph) -> tuple[dict[str, URIRef], dict[str, str]]:
    entity_by_qid: dict[str, URIRef] = {}
    label_by_qid: dict[str, str] = {}

    for subject in graph.subjects(DATA.wdtLink, None):
        if not isinstance(subject, URIRef):
            continue
        qid = qid_from_uri(graph.value(subject, DATA.wdtLink))
        if not qid:
            continue

        entity_by_qid[qid] = subject
        label = graph.value(subject, RDFS.label)
        if label is not None:
            label_text = str(label).strip()
            if label_text:
                label_by_qid[qid] = label_text

    return entity_by_qid, label_by_qid


def is_person_entity(entity_uri: URIRef | str, graph: Graph) -> bool:
    entity_ref = URIRef(entity_uri) if isinstance(entity_uri, str) else entity_uri
    person_types = {ONTOLOGY.Person, ONTOLOGY.Man, ONTOLOGY.Woman, ONTOLOGY.Ancestor}
    for entity_type in graph.objects(entity_ref, RDF.type):
        if entity_type in person_types:
            return True
    return False


def entity_gender(entity_uri: URIRef | str, graph: Graph) -> str | None:
    entity_ref = URIRef(entity_uri) if isinstance(entity_uri, str) else entity_uri
    types = set(graph.objects(entity_ref, RDF.type))
    if ONTOLOGY.Man in types:
        return "male"
    if ONTOLOGY.Woman in types:
        return "female"
    return None


def gender_compatible(extracted_gender: str | None, candidate_gender: str | None) -> bool:
    # If either side is unknown/person-only, keep name comparison enabled.
    if extracted_gender is None or candidate_gender is None:
        return True
    return extracted_gender == candidate_gender


def collect_extracted_entities(graph: Graph) -> list[URIRef]:
    entities: set[URIRef] = set()
    for subject, predicate, obj in graph:
        if predicate not in METADATA_PREDICATES and isinstance(subject, URIRef):
            entities.add(subject)
        if predicate not in METADATA_PREDICATES and isinstance(obj, URIRef):
            entities.add(obj)
    return sorted(entities, key=str)


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

            for subj, predicate, _ in graph.triples((None, None, node)):
                if predicate in METADATA_PREDICATES or not isinstance(subj, URIRef):
                    continue
                if subj in visited:
                    continue
                visited.add(subj)
                next_frontier.add(subj)
                candidates[str(subj)] = depth
            frontier = next_frontier

    return candidates


def tokenize_match_text(nlp: spacy.language.Language, text: str) -> list[str]:
    doc = nlp.make_doc(text)
    return [tok.text for tok in doc if tok.text.strip()]


def collect_candidate_patterns(candidate_ref: URIRef, graph: Graph) -> list[str]:
    patterns: list[str] = []
    seen: set[str] = set()

    # Always keep URI-local fallback as a pattern.
    local_pattern = semantic_form(local_name(str(candidate_ref)))
    if local_pattern:
        key = local_pattern.lower()
        if key not in seen:
            seen.add(key)
            patterns.append(local_pattern)

    for label_node in graph.objects(candidate_ref, RDFS.label):
        label_pattern = str(label_node).strip()
        if not label_pattern:
            continue
        key = label_pattern.lower()
        if key in seen:
            continue
        seen.add(key)
        patterns.append(label_pattern)

    for alias_node in graph.objects(candidate_ref, ONTOLOGY.alsoKnownAs):
        alias_pattern = str(alias_node).strip()
        if not alias_pattern:
            continue
        key = alias_pattern.lower()
        if key in seen:
            continue
        seen.add(key)
        patterns.append(alias_pattern)

    return patterns


def build_matcher(
    nlp: spacy.language.Language,
    graph: Graph,
    candidate_entities: dict[str, int],
    label_by_qid: dict[str, str],
) -> tuple[Matcher, dict[str, list[dict[str, Any]]]]:
    matcher = Matcher(nlp.vocab)
    rows_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for candidate_uri, depth in sorted(candidate_entities.items(), key=lambda item: (item[1], item[0])):
        candidate_ref = URIRef(candidate_uri)
        qid = qid_from_uri(graph.value(candidate_ref, DATA.wdtLink))
        if not qid:
            continue
        if not is_person_entity(candidate_ref, graph):
            continue

        graph_label = graph.value(candidate_ref, RDFS.label)
        label = label_by_qid.get(qid)
        if not label and graph_label is not None:
            label = str(graph_label).strip()
        if not label:
            label = local_name(candidate_uri)

        candidate_gender = entity_gender(candidate_ref, graph)

        for match_text in collect_candidate_patterns(candidate_ref, graph):
            tokens = tokenize_match_text(nlp, match_text)
            if not tokens:
                continue

            pattern = []
            for token in tokens:
                if len(token) >= 8:
                    pattern.append({"LOWER": {"FUZZY4": token.lower()}})
                elif len(token) >= 4:
                    pattern.append({"LOWER": {"FUZZY2": token.lower()}})
                else:
                    pattern.append({"LOWER": token.lower()})
            
            matcher.add(match_text, [pattern])
            rows_by_key[match_text].append(
                {
                    "uri": candidate_uri,
                    "qid": qid,
                    "label": label,
                    "match_text": match_text,
                    "distance": depth,
                    "gender": candidate_gender,
                }
            )

    return matcher, rows_by_key


def split_on_keyword(text: str, keyword: str) -> tuple[str, str, bool]:
    parts = re.split(rf"\b{re.escape(keyword)}\b", text, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) < 2:
        return text.strip(), "", False
    before = parts[0].strip()
    after = parts[1].strip()
    return before, after, True


def split_two_words(text: str) -> tuple[str, str, bool]:
    tokens = [token for token in text.strip().split() if token]
    if len(tokens) != 2:
        return text.strip(), "", False
    return tokens[0], tokens[1], True


def pair_similarity(left: str, right: str) -> float:
    left_norm = left.lower().strip()
    right_norm = right.lower().strip()
    if not left_norm and not right_norm:
        return 1.0
    if not left_norm or not right_norm:
        return 0.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def split_parts_pass_threshold(scores: list[float], min_score: float = SPLIT_PART_MIN_SCORE) -> bool:
    return all(score >= min_score for score in scores)


noble_titles = [
    "Emperor", "Empress", "King", "Queen", "Prince", "Princess", "Archduke", 
    "Archduchess", "Grand Duke", "Grand Duchess", "Duke", "Duchess", 
    "Marquess", "Marquis", "Marchioness", "Earl", "Count", "Countess", 
    "Viscount", "Viscountess", "Baron", "Baroness", "Baronet", "Baronetess", 
    "Lord", "Lady", "Sir", "Dame", "Chevalier", "Esquire", "Esq", "Laird", 
    "Don", "Doña", "Infante", "Infanta", "Dauphin", "Dauphine", "Vicomte", 
    "Vicomtesse", "Margrave", "Margravine", "Landgrave", "Landgravine", 
    "Elector", "Electress", "Honourable", "Hon", "Right Honourable", 
    "Rt Hon", "Dowager", "Majesty", "Royal Highness", "Serene Highness"
]


def split_title_prefix(text: str) -> tuple[str, str, bool]:
    for title in sorted(noble_titles, key=len, reverse=True):
        pattern = rf"^\s*{re.escape(title)}\b\s+(.*)$"
        match = re.match(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        rest = match.group(1).strip()
        if not rest:
            return text.strip(), "", False
        return title, rest, True
    return text.strip(), "", False


def split_on_keyword_in_text(text: str, keyword: str) -> tuple[str, str, bool]:
    before, after, has_keyword = split_on_keyword(text, keyword)
    if not has_keyword:
        return text.strip(), "", False
    if not before or not after:
        return text.strip(), "", False
    return before, after, True


def score_candidate_name(extracted_text: str, candidate_text: str) -> float:
    """Return final score with optional balanced split scoring.

    Priority:
    1) title + of/von/de on both names -> average(title, before, after)
    2) title on both names -> average(title, rest)
    3) both contain standalone 'of' -> average(before, after)
    4) both contain standalone 'von' -> average(before, after)
    5) both contain standalone 'de' -> average(before, after)
    6) both are exactly two-word names -> average(first, second)
    7) fallback to whole-string similarity
    """

    full_score = pair_similarity(extracted_text, candidate_text)

    ext_title, ext_rest, ext_has_title = split_title_prefix(extracted_text)
    cand_title, cand_rest, cand_has_title = split_title_prefix(candidate_text)

    for keyword in ("of", "von", "de"):
        if ext_has_title and cand_has_title:
            ext_before, ext_after, ext_has_keyword = split_on_keyword_in_text(ext_rest, keyword)
            cand_before, cand_after, cand_has_keyword = split_on_keyword_in_text(cand_rest, keyword)
            if ext_has_keyword and cand_has_keyword:
                title_score = pair_similarity(ext_title, cand_title)
                before_score = pair_similarity(ext_before, cand_before)
                after_score = pair_similarity(ext_after, cand_after)
                if not split_parts_pass_threshold([title_score, before_score, after_score]):
                    return 0.0
                return (title_score + before_score + after_score) / 3.0

    if ext_has_title and cand_has_title:
        title_score = pair_similarity(ext_title, cand_title)
        rest_score = pair_similarity(ext_rest, cand_rest)
        if not split_parts_pass_threshold([title_score, rest_score]):
            return 0.0
        return (title_score + rest_score) / 2.0

    ext_before, ext_after, ext_has_of = split_on_keyword(extracted_text, "of")
    cand_before, cand_after, cand_has_of = split_on_keyword(candidate_text, "of")
    if ext_has_of and cand_has_of:
        before_score = pair_similarity(ext_before, cand_before)
        after_score = pair_similarity(ext_after, cand_after)
        if not split_parts_pass_threshold([before_score, after_score]):
            return 0.0
        return (before_score + after_score) / 2.0

    ext_before, ext_after, ext_has_von = split_on_keyword(extracted_text, "von")
    cand_before, cand_after, cand_has_von = split_on_keyword(candidate_text, "von")
    if ext_has_von and cand_has_von:
        before_score = pair_similarity(ext_before, cand_before)
        after_score = pair_similarity(ext_after, cand_after)
        if not split_parts_pass_threshold([before_score, after_score]):
            return 0.0
        return (before_score + after_score) / 2.0

    ext_before, ext_after, ext_has_de = split_on_keyword(extracted_text, "de")
    cand_before, cand_after, cand_has_de = split_on_keyword(candidate_text, "de")
    if ext_has_de and cand_has_de:
        before_score = pair_similarity(ext_before, cand_before)
        after_score = pair_similarity(ext_after, cand_after)
        if not split_parts_pass_threshold([before_score, after_score]):
            return 0.0
        return (before_score + after_score) / 2.0

    ext_first, ext_second, ext_two_words = split_two_words(extracted_text)
    cand_first, cand_second, cand_two_words = split_two_words(candidate_text)
    if ext_two_words and cand_two_words:
        first_score = pair_similarity(ext_first, cand_first)
        second_score = pair_similarity(ext_second, cand_second)
        if not split_parts_pass_threshold([first_score, second_score]):
            return 0.0
        return (first_score + second_score) / 2.0

    return full_score

def match_candidates(
    extracted_entities: list[URIRef],
    matcher: Matcher,
    candidate_rows: dict[str, list[dict[str, Any]]],
    extracted_graph: Graph,
    nlp: spacy.language.Language,
    threshold: float,
) -> tuple[list[dict[str, Any]], int]:
    if not extracted_entities:
        return [], 0

    extracted_rows: list[dict[str, Any]] = []
    matched_count = 0
    used_candidate_uris: set[str] = set()

    for extracted in extracted_entities:
        extracted_uri = str(extracted)
        extracted_local_name = local_name(extracted_uri)
        extracted_text = semantic_form(extracted_local_name)
        extracted_doc = nlp.make_doc(extracted_text)
        extracted_gender = entity_gender(extracted, extracted_graph)

        best_row: dict[str, Any] | None = None
        best_score = -1.0
        
        for match_id, _start, _end in matcher(extracted_doc):
            match_key = extracted_doc.vocab.strings[match_id]
            rows = candidate_rows.get(match_key)
            if not rows:
                continue

            for row in rows:
                if row["uri"] in used_candidate_uris:
                    continue
                candidate_gender = row.get("gender")
                if not gender_compatible(extracted_gender, candidate_gender):
                    continue
                candidate_text = row["match_text"]
                score = score_candidate_name(extracted_text, candidate_text)
                if score > best_score:
                    best_score = score
                    best_row = row

        hard_match = best_row is not None and best_score >= 0.5

        if not hard_match:
            for rows in candidate_rows.values():
                for row in rows:
                    if row["uri"] in used_candidate_uris:
                        continue
                    candidate_gender = row.get("gender")
                    if not gender_compatible(extracted_gender, candidate_gender):
                        continue
                    candidate_text = row["match_text"]
                    score = score_candidate_name(extracted_text, candidate_text)
                    if score > best_score:
                        best_score = score
                        best_row = row

        soft_match = best_row is not None and best_score >= threshold

        matched = hard_match or soft_match
        
        if "Marriage" in extracted_text or "marriage" in extracted_text:
            best_score = 0
            matched = False

        if matched and best_row is not None:
            used_candidate_uris.add(best_row["uri"])
            
        if matched:
            matched_count += 1

        extracted_rows.append(
            {
                "extracted_uri": extracted_uri,
                "extracted_local_name": extracted_local_name,
                "embedding_text": extracted_text,
                "extracted_gender": extracted_gender,
                "matched": matched,
                "score": best_score if matched else None,
                "ground_truth_uri": best_row["uri"] if matched and best_row else None,
                "ground_truth_qid": best_row["qid"] if matched and best_row else None,
                "ground_truth_label": best_row["label"] if matched and best_row else None,
                "ground_truth_distance": best_row["distance"] if matched and best_row else None,
                "ground_truth_gender": best_row["gender"] if matched and best_row else None,
                "best_candidate_match_text": best_row["match_text"] if best_row else None,
                "best_candidate_label": best_row["label"] if best_row else None,
                "best_candidate_qid": best_row["qid"] if best_row else None,
                "best_candidate_gender": best_row["gender"] if best_row else None,
                "best_candidate_score": best_score if best_row else None,
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
    nlp: spacy.language.Language,
    threshold: float,
) -> tuple[dict[str, Any], int]:
    delta_graph_path = task_directory / "delta_graph.ttl"
    if not delta_graph_path.exists():
        raise FileNotFoundError(f"Missing delta_graph.ttl: {delta_graph_path}")

    delta_graph = Graph()
    delta_graph.parse(delta_graph_path.as_posix(), format="turtle")

    article = (csv_row.get("article") or "").strip()
    article_label = (csv_row.get("itemLabel") or "").strip()
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
    extracted_entities = [entity for entity in extracted_entities if is_person_entity(entity, delta_graph)]

    matcher, candidate_rows = build_matcher(nlp, ground_truth_graph, candidate_entities, label_by_qid)
    matched_entities, matched_count = match_candidates(
        extracted_entities=extracted_entities,
        matcher=matcher,
        candidate_rows=candidate_rows,
        extracted_graph=delta_graph,
        nlp=nlp,
        threshold=threshold,
    )

    candidate_payload: list[dict[str, Any]] = []
    for candidate_uri, depth in sorted(candidate_entities.items(), key=lambda item: (item[1], item[0])):
        candidate_ref = URIRef(candidate_uri)
        qid = qid_from_uri(ground_truth_graph.value(candidate_ref, DATA.wdtLink))
        if not qid:
            continue
        candidate_payload.append(
            {
                "uri": candidate_uri,
                "qid": qid,
                "label": label_by_qid.get(qid) or local_name(candidate_uri),
                "distance": depth,
                "gender": entity_gender(candidate_ref, ground_truth_graph),
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


def load_spacy_pipeline(model_name: str) -> spacy.language.Language:
    try:
        nlp = spacy.load(model_name)
    except OSError as exc:
        raise SystemExit(
            f"spaCy model '{model_name}' is not installed. Install it before running this script."
        ) from exc

    if not nlp.has_pipe("parser") and not nlp.has_pipe("sentencizer"):
        nlp.add_pipe("sentencizer")
    return nlp


def main() -> None:
    args = parse_args()

    text_files = sorted(args.text_dir.glob("*.txt"))
    if not text_files:
        raise FileNotFoundError(f"No text files found in {args.text_dir}")

    article_to_row, qid_to_row = load_csv_index(args.csv)

    run_directories = args.run_directories or discover_run_directories(args.results_root)
    if not run_directories:
        raise FileNotFoundError(
            f"No run directories found under {args.results_root}. Use --run-directory to target one explicitly."
        )

    nlp = load_spacy_pipeline("en_core_web_sm")

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
            csv_row = resolve_text_row(text_file, article_to_row)
            if csv_row is None:
                print(f"Warning: no CSV row found for {text_file.name}", file=sys.stderr)
                continue

            item_qid = qid_from_uri(URIRef((csv_row.get("item") or "").strip()))
            if not item_qid:
                print(f"Warning: no QID found for {text_file.name}", file=sys.stderr)
                continue

            if item_qid in qid_to_row:
                csv_row = qid_to_row[item_qid]

            ground_truth_graph = load_ground_truth_graph(args.ground_truth_dir, item_qid)
            if not ground_truth_graph:
                continue
            entity_by_qid, label_by_qid = load_entity_index(ground_truth_graph)
            
            payload, matched_count = build_folder_payload(
                run_directory=run_directory,
                task_directory=task_directory,
                text_file=text_file,
                csv_row=csv_row,
                ground_truth_graph=ground_truth_graph,
                entity_by_qid=entity_by_qid,
                label_by_qid=label_by_qid,
                nlp=nlp,
                threshold=args.threshold,
            )

            total_matched += matched_count
            total_entities += payload["summary"]["entities_total"]
            write_json(task_directory / args.folder_output_name, payload)

            all_rows.extend(payload["entities"])

    all_rows.sort(
        key=lambda row: (
            0 if row.get("matched") else 1,
            -(row.get("best_candidate_score") or 0.0),
            row.get("extracted_local_name") or "",
        )
    )

    global_payload = {
        "results_root": args.results_root.as_posix(),
        "text_dir": args.text_dir.as_posix(),
        "csv": args.csv.as_posix(),
        "ground_truth_dir": args.ground_truth_dir.as_posix(),
        "threshold": args.threshold,
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
