from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit

import spacy
from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.term import Node
from spacy.matcher import Matcher


ONTOLOGY_PREFIX = "http://example.com/family_TBOX.ttl#"
DATA_PREFIX = "http://example.com/data#"
WIKIDATA_PREFIX = "http://www.wikidata.org/entity/"

ONT_NS = Namespace(ONTOLOGY_PREFIX)
DATA_NS = Namespace(DATA_PREFIX)
WDT_NS = Namespace(WIKIDATA_PREFIX)

METADATA_PREDICATES = {
    RDF.type,
    RDFS.label,
    DATA_NS.wdtLink,
    ONT_NS.alsoKnownAs,
    ONT_NS.hasSex,
    DATA_NS.posIndices,
}


@dataclass(frozen=True)
class TextRow:
    text_file: Path
    article_url: str
    item_qid: str
    item_label: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create denoised royalty texts and per-text ground-truth Turtle files by "
            "fuzzy-matching entity mentions sentence by sentence."
        )
    )
    parser.add_argument(
        "--texts-dir",
        type=Path,
        default=Path("custom_family_bench/royalty/texts"),
        help="Directory containing the source Wikipedia texts.",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("custom_family_bench/royalty/ground_truth.csv"),
        help="Royalty ground-truth CSV used to map texts to main entities.",
    )
    parser.add_argument(
        "--graph",
        type=Path,
        default=Path("custom_family_bench/royalty/ground_truth_inferred.ttl"),
        help="Ground-truth Turtle graph with labels, aliases, and relations.",
    )
    parser.add_argument(
        "--denoised-output-dir",
        type=Path,
        default=Path("custom_family_bench/royalty/denoised_texts_fuzzy_match"),
        help="Directory where filtered text files will be written.",
    )
    parser.add_argument(
        "--ground-truth-output-dir",
        type=Path,
        default=Path("custom_family_bench/royalty/ground_truths"),
        help="Directory where per-text Turtle files will be written.",
    )
    parser.add_argument(
        "--spacy-model",
        default="en_core_web_sm",
        help="spaCy model used for sentence segmentation and fuzzy matching.",
    )
    return parser.parse_args()


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


def normalize_key(value: str) -> str:
    text = unquote(value)
    text = text.removesuffix(".txt")
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def article_key(article_url: str) -> str:
    return normalize_key(urlsplit(article_url).path.rsplit("/", 1)[-1])


def filename_key(file_path: Path) -> str:
    return normalize_key(file_path.stem)


def qid_from_uri(value: Node | None) -> str | None:
    if value is None:
        return None
    text = str(value)
    if "/" in text:
        return text.rsplit("/", 1)[-1]
    if "#" in text:
        return text.rsplit("#", 1)[-1]
    return text or None


def load_text_rows(csv_path: Path, texts_dir: Path) -> list[TextRow]:
    rows_by_article: dict[str, dict[str, str]] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"item", "itemLabel", "article"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")

        for row in reader:
            article = (row.get("article") or "").strip()
            item = (row.get("item") or "").strip()
            if not article or not item:
                continue
            rows_by_article.setdefault(article_key(article), row)

    text_rows: list[TextRow] = []
    for text_file in sorted(texts_dir.glob("*.txt")):
        text_row = rows_by_article.get(filename_key(text_file))
        if text_row is None:
            continue
        item_uri = (text_row.get("item") or "").strip()
        item_qid = qid_from_uri(URIRef(item_uri)) if item_uri else None
        if not item_qid:
            continue
        text_rows.append(
            TextRow(
                text_file=text_file,
                article_url=(text_row.get("article") or "").strip(),
                item_qid=item_qid,
                item_label=(text_row.get("itemLabel") or "").strip(),
            )
        )
    return text_rows


def load_ground_truth_graph(graph_path: Path) -> tuple[Graph, dict[str, URIRef]]:
    graph = Graph()
    graph.parse(graph_path.as_posix(), format="turtle")

    entity_by_qid: dict[str, URIRef] = {}
    for subject in graph.subjects(DATA_NS.wdtLink, None):
        if not isinstance(subject, URIRef):
            continue
        qid = qid_from_uri(graph.value(subject, DATA_NS.wdtLink))
        if qid:
            entity_by_qid[qid] = subject

    return graph, entity_by_qid


def entity_labels(graph: Graph, entity: URIRef, fallback_label: str | None = None) -> list[str]:
    labels: list[str] = []
    seen: set[str] = set()

    for predicate in (RDFS.label, ONT_NS.alsoKnownAs):
        for value in graph.objects(entity, predicate):
            if not isinstance(value, Literal):
                continue
            label = str(value).strip()
            if label and label not in seen:
                seen.add(label)
                labels.append(label)

    if fallback_label and fallback_label not in seen:
        labels.append(fallback_label)
    return labels


def primary_label(graph: Graph, entity: URIRef, fallback_label: str | None = None) -> str | None:
    label = graph.value(entity, RDFS.label)
    if label is not None:
        text = str(label).strip()
        if text:
            return text
    if fallback_label:
        text = fallback_label.strip()
        if text:
            return text
    return None


def build_candidate_closure(graph: Graph, start_entity: URIRef, max_depth: int = 2) -> set[URIRef]:
    candidates: set[URIRef] = {start_entity}
    frontier: set[URIRef] = {start_entity}
    visited: set[URIRef] = {start_entity}

    for _depth in range(max_depth):
        next_frontier: set[URIRef] = set()
        for node in frontier:
            for subject, predicate, obj in graph.triples((node, None, None)):
                if predicate in METADATA_PREDICATES:
                    continue
                if isinstance(obj, URIRef) and obj not in visited:
                    visited.add(obj)
                    candidates.add(obj)
                    next_frontier.add(obj)

            for subject, predicate, obj in graph.triples((None, None, node)):
                if predicate in METADATA_PREDICATES:
                    continue
                if isinstance(subject, URIRef) and subject not in visited:
                    visited.add(subject)
                    candidates.add(subject)
                    next_frontier.add(subject)
        frontier = next_frontier

    return candidates


def word_tokens(label: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", label)
    return re.findall(r"[\w]+", normalized, flags=re.UNICODE)


def build_matcher(
    nlp: spacy.language.Language,
    graph: Graph,
    candidate_entities: set[URIRef],
    fallback_labels: dict[URIRef, str],
) -> tuple[Matcher, dict[str, set[URIRef]]]:
    matcher = Matcher(nlp.vocab)
    label_to_entities: dict[str, set[URIRef]] = defaultdict(set)

    for entity in sorted(candidate_entities, key=str):
        qid = qid_from_uri(graph.value(entity, DATA_NS.wdtLink))
        if not qid:
            continue

        labels = entity_labels(graph, entity, fallback_labels.get(entity))
        for label in labels:
            # Tokenize the label with spaCy to ensure consistent tokenization
            label_doc = nlp.make_doc(label)
            tokens = [tok.text for tok in label_doc if tok.text.strip()]
            if not tokens:
                continue
            key = normalize_key(label)
            label_to_entities[key].add(entity)
            pattern = [
                {"LOWER": {"FUZZY2": tok.lower()} if len(tok) >= 4 else tok.lower()} for tok in tokens
            ]
            matcher.add(key, [pattern])

    return matcher, label_to_entities


def collect_mentions_for_sentence(
    sentence_doc: spacy.tokens.Doc,
    matcher: Matcher,
    label_to_entities: dict[str, set[URIRef]],
) -> tuple[set[URIRef], list[tuple[URIRef, int, int]]]:
    def is_valid_span(span_text: str) -> bool:
        return len(span_text.strip()) >= 3

    mentioned_entities: set[URIRef] = set()
    mentions: list[tuple[URIRef, int, int]] = []
    seen_spans: set[tuple[URIRef, int, int]] = set()

    for match_id, start, end in matcher(sentence_doc):
        label_key = sentence_doc.vocab.strings[match_id]
        entities = label_to_entities.get(label_key)
        if not entities:
            continue

        span = sentence_doc[start:end]
        if not is_valid_span(span.text):
            continue
        text_start = span.start_char
        text_end = span.end_char

        for entity in entities:
            dedupe_key = (entity, text_start, text_end)
            if dedupe_key in seen_spans:
                continue
            seen_spans.add(dedupe_key)
            mentioned_entities.add(entity)
            mentions.append((entity, text_start, text_end))

    return mentioned_entities, mentions


def mask_spans(text: str, spans: list[tuple[int, int]]) -> str:
    if not spans:
        return text

    masked = list(text)
    for start, end in spans:
        for index in range(max(0, start), min(len(masked), end)):
            if not masked[index].isspace():
                masked[index] = " "
    return "".join(masked)


def collect_token_mentions_for_sentence(
    sentence_text: str,
    candidate_entities: set[URIRef],
    fuzzy_entities_in_sentence: set[URIRef],
    graph: Graph,
    fallback_labels: dict[URIRef, str],
    excluded_spans: list[tuple[int, int]],
    nlp: spacy.language.Language,
) -> tuple[set[URIRef], list[tuple[URIRef, int, int]]]:
    function_words = {
        "a",
        "an",
        "the",
        "and",
        "of",
        "in",
        "on",
        "at",
        "to",
        "his",
        "her",
        "st.",
        "st",
        "for",
        "from",
        "by",
        "with",
        "de",
        "du",
        "da",
        "del",
        "des",
        "di",
        "do",
        "der",
        "den",
        "van",
        "von",
        "la",
        "le",
        "les",
        "en",
        "y"
    }

    # Roman numeral detection (valid up to 3999)
    ROMAN_RE = re.compile(r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", re.IGNORECASE)

    def is_roman_numeral(tok: str) -> bool:
        if not tok:
            return False
        return bool(ROMAN_RE.fullmatch(tok.strip()))

    # Ordinal detection (1st, 2nd, 3rd, 4th, etc.)
    ORDINAL_RE = re.compile(r"^\d+(st|nd|rd|th)$", re.IGNORECASE)

    def is_ordinal(tok: str) -> bool:
        if not tok:
            return False
        return bool(ORDINAL_RE.fullmatch(tok.strip()))

    token_to_entities: dict[str, set[URIRef]] = defaultdict(set)
    for entity in sorted(candidate_entities, key=str):
        if entity in fuzzy_entities_in_sentence:
            continue

        label = primary_label(graph, entity, fallback_labels.get(entity))
        if not label:
            continue

        # Tokenize with spaCy to match the same tokenization as the sentence
        label_doc = nlp.make_doc(label)
        for tok in label_doc:
            token_text = tok.text.strip()
            if not token_text:
                continue
            low = token_text.lower()
            if low in function_words:
                continue
            if is_roman_numeral(token_text):
                continue
            if is_ordinal(low):
                continue
            token_to_entities[token_text].add(entity)

    if not token_to_entities:
        return set(), []

    residual_text = mask_spans(sentence_text, excluded_spans)
    residual_doc = nlp.make_doc(residual_text)
    matcher = Matcher(nlp.vocab)

    for token in sorted(token_to_entities):
            matcher.add(token, [[{"LOWER": token.lower()}]])

    mentioned_entities: set[URIRef] = set()
    mentions: list[tuple[URIRef, int, int]] = []
    seen_spans: set[tuple[URIRef, int, int]] = set()

    for match_id, start, end in matcher(residual_doc):
        token = residual_doc.vocab.strings[match_id]
        entities = token_to_entities.get(token)
        if not entities:
            continue

        span = residual_doc[start:end]
        if len(span.text.strip()) <= 2:
            continue
        text_start = span.start_char
        text_end = span.end_char
        if any(text_start < span_end and text_end > span_start for span_start, span_end in excluded_spans):
            continue

        for entity in entities:
            dedupe_key = (entity, text_start, text_end)
            if dedupe_key in seen_spans:
                continue
            seen_spans.add(dedupe_key)
            mentioned_entities.add(entity)
            mentions.append((entity, text_start, text_end))

    return mentioned_entities, mentions


def create_output_graph(
    source_graph: Graph,
    selected_entities: set[URIRef],
    mentions_full: dict[URIRef, set[str]],
    mentions_part: dict[URIRef, set[str]],
) -> Graph:
    output = Graph()
    output.bind("", ONTOLOGY_PREFIX)
    output.bind("data", DATA_PREFIX)
    output.bind("wdt", WIKIDATA_PREFIX)
    output.bind("owl", OWL)
    output.bind("rdf", RDF)
    output.bind("rdfs", RDFS)

    data_uri = URIRef(DATA_PREFIX)
    ontology_uri = URIRef(ONTOLOGY_PREFIX)
    output.add((data_uri, RDF.type, OWL.Ontology))
    output.add((data_uri, OWL.imports, ontology_uri))
    output.add((DATA_NS.wdtLink, RDF.type, OWL.AnnotationProperty))
    output.add((DATA_NS.posIndicesFull, RDF.type, OWL.AnnotationProperty))
    output.add((DATA_NS.posIndicesPart, RDF.type, OWL.AnnotationProperty))

    for entity in sorted(selected_entities, key=str):
        for predicate in METADATA_PREDICATES:
            for obj in source_graph.objects(entity, predicate):
                output.add((entity, predicate, obj))

        for pos_index in sorted(mentions_full.get(entity, set())):
            output.add((entity, DATA_NS.posIndicesFull, Literal(pos_index)))

        for pos_index in sorted(mentions_part.get(entity, set())):
            output.add((entity, DATA_NS.posIndicesPart, Literal(pos_index)))

    for subject, predicate, obj in source_graph:
        if predicate in METADATA_PREDICATES:
            continue
        if subject in selected_entities and obj in selected_entities:
            output.add((subject, predicate, obj))

    return output


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Normalize Unicode and replace non-breaking spaces with regular spaces
    try:
        import unicodedata

        text = unicodedata.normalize("NFKC", text)
    except Exception:
        pass
    text = text.replace("\u00A0", " ")
    return text


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_graph(path: Path, graph: Graph) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=path.as_posix(), format="turtle")


def process_text_row(
    text_row: TextRow,
    graph: Graph,
    entity_by_qid: dict[str, URIRef],
    nlp: spacy.language.Language,
    denoised_output_dir: Path,
    ground_truth_output_dir: Path,
) -> tuple[Path, Path, int, int, int]:
    main_entity = entity_by_qid.get(text_row.item_qid)
    if main_entity is None:
        raise KeyError(f"Could not find ground-truth entity for {text_row.text_file.name} ({text_row.item_qid})")

    candidate_entities = {
        entity
        for entity in build_candidate_closure(graph, main_entity, max_depth=2)
        if graph.value(entity, DATA_NS.wdtLink) is not None
    }

    fallback_labels = {main_entity: text_row.item_label}
    matcher, label_to_entities = build_matcher(nlp, graph, candidate_entities, fallback_labels)

    full_text = read_text(text_row.text_file)
    doc = nlp(full_text)

    kept_sentence_records: list[
        tuple[str, list[tuple[URIRef, int, int]], list[tuple[URIRef, int, int]]]
    ] = []
    mentions_full: dict[URIRef, set[str]] = defaultdict(set)
    mentions_part: dict[URIRef, set[str]] = defaultdict(set)
    selected_entities: set[URIRef] = set()
    text_fuzzy_entities: set[URIRef] = set()

    sentence_fuzzy_results: list[tuple[str, set[URIRef], list[tuple[URIRef, int, int]]]] = []

    total_original_sentence_count = 0
    for sentence in doc.sents:
        total_original_sentence_count += 1
        sentence_text = sentence.text.strip()
        if not sentence_text:
            continue

        sentence_doc = nlp.make_doc(sentence_text)
        sentence_mentions, spans = collect_mentions_for_sentence(
            sentence_doc=sentence_doc,
            matcher=matcher,
            label_to_entities=label_to_entities,
        )

        sentence_fuzzy_results.append((sentence_text, sentence_mentions, spans))
        text_fuzzy_entities.update(sentence_mentions)

    first_sentence_text = sentence_fuzzy_results[0][0] if sentence_fuzzy_results else None

    # Map each entity to the index of the first sentence where it was fully (fuzzily) matched
    first_fuzzy_sentence_idx: dict[URIRef, int] = {}
    for idx, (_s_text, s_mentions, _s_spans) in enumerate(sentence_fuzzy_results):
        for ent in s_mentions:
            if ent not in first_fuzzy_sentence_idx:
                first_fuzzy_sentence_idx[ent] = idx

    for sentence_idx, (sentence_text, sentence_mentions, spans) in enumerate(sentence_fuzzy_results):
        # Only allow fallback candidates that were fully matched earlier (first match index < current sentence index)
        candidate_entities_for_fallback = {
            e for e in text_fuzzy_entities if first_fuzzy_sentence_idx.get(e, float("inf")) < sentence_idx
        }

        fallback_mentions, fallback_spans = collect_token_mentions_for_sentence(
            sentence_text=sentence_text,
            candidate_entities=candidate_entities_for_fallback,
            fuzzy_entities_in_sentence=sentence_mentions,
            graph=graph,
            fallback_labels=fallback_labels,
            excluded_spans=[(start, end) for _, start, end in spans],
            nlp=nlp,
        )

        sentence_entities = sentence_mentions | fallback_mentions

        if not sentence_entities:
            continue

        kept_sentence_records.append((sentence_text, spans, fallback_spans))
        selected_entities.update(sentence_entities)
    if first_sentence_text and (not kept_sentence_records or kept_sentence_records[0][0] != first_sentence_text):
        kept_sentence_records.insert(0, (first_sentence_text, [], []))

    output_offset = 0
    for index, (sentence_text, fuzzy_spans, fallback_spans) in enumerate(kept_sentence_records):
        sentence_start = output_offset
        sentence_end = sentence_start + len(sentence_text)
        if index < len(kept_sentence_records) - 1:
            output_offset = sentence_end + 1
        else:
            output_offset = sentence_end

        for entity, start, end in fuzzy_spans:
            mentions_full[entity].add(f"{sentence_start + start}:{sentence_start + end}")

        for entity, start, end in fallback_spans:
            mentions_part[entity].add(f"{sentence_start + start}:{sentence_start + end}")

    if selected_entities and main_entity not in selected_entities:
        selected_entities.add(main_entity)

    output_text = "\n".join(sentence_text for sentence_text, _, _ in kept_sentence_records)
    output_text_path = denoised_output_dir / f"{text_row.item_qid}.txt"
    write_text(output_text_path, output_text + ("\n" if output_text else ""))

    output_graph = create_output_graph(graph, selected_entities, mentions_full, mentions_part)
    output_graph_path = ground_truth_output_dir / f"{text_row.item_qid}.ttl"
    write_graph(output_graph_path, output_graph)

    return output_text_path, output_graph_path, len(kept_sentence_records), len(selected_entities), total_original_sentence_count


def main() -> None:
    args = parse_args()
    nlp = load_spacy_pipeline(args.spacy_model)
    graph, entity_by_qid = load_ground_truth_graph(args.graph)
    text_rows = load_text_rows(args.csv, args.texts_dir)

    if not text_rows:
        raise SystemExit(f"No text files in {args.texts_dir} could be matched to rows in {args.csv}")

    total_sentences = 0
    total_entities = 0
    total_original_sentences = 0

    for text_row in text_rows:
        _, _, kept_sentence_count, selected_entity_count, original_sentence_count = process_text_row(
            text_row=text_row,
            graph=graph,
            entity_by_qid=entity_by_qid,
            nlp=nlp,
            denoised_output_dir=args.denoised_output_dir,
            ground_truth_output_dir=args.ground_truth_output_dir,
        )
        total_sentences += kept_sentence_count
        total_entities += selected_entity_count
        total_original_sentences += original_sentence_count
        print(
            f"Processed {text_row.text_file.name} -> {text_row.item_qid} "
            f"({kept_sentence_count} kept sentences out of {original_sentence_count}, {selected_entity_count} entities)"
        )

    print(
        f"Completed {len(text_rows)} texts with {total_sentences} kept sentences out of {total_original_sentences} and {total_entities} selected entities."
    )


if __name__ == "__main__":
    main()