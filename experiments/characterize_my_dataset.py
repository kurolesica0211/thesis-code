from __future__ import annotations

import re
from pathlib import Path
from statistics import mean

from rdflib import OWL, RDF, Graph, URIRef

try:
    from experiments.precision_recall import deduplicate_by_synonymy, get_predicate_name
except ModuleNotFoundError:
    # Allows running this file directly via: python experiments/characterize_my_dataset.py
    from precision_recall import deduplicate_by_synonymy, get_predicate_name


PERSON_CLASS_LOCAL_NAMES = {"Person", "Man", "Woman", "Ancestor"}


def _count_sentences(text: str) -> int:
    normalized = re.sub(r"\s+", " ", text.strip())
    if not normalized:
        return 0
    parts = [part.strip() for part in re.findall(r"[^.!?]+(?:[.!?]+(?=\s|$)|$)", normalized) if part.strip()]
    return len(parts)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _collect_text_lengths(text_dir: Path) -> dict[str, int]:
    lengths: dict[str, int] = {}
    for path in sorted(text_dir.glob("*.txt")):
        lengths[path.stem] = _count_sentences(path.read_text(encoding="utf-8"))
    return lengths


def _collect_ttl_paths(ground_truth_dir: Path) -> dict[str, Path]:
    return {path.stem: path for path in sorted(ground_truth_dir.glob("*.ttl"))}


def _uri_local_name(uri: URIRef) -> str:
    text = str(uri)
    if "#" in text:
        return text.rsplit("#", 1)[-1]
    return text.rsplit("/", 1)[-1]


def _person_class_uris_from_tbox(tbox_graph: Graph) -> set[URIRef]:
    class_uris: set[URIRef] = set()
    for subj in tbox_graph.subjects(RDF.type, OWL.Class):
        if isinstance(subj, URIRef) and _uri_local_name(subj) in PERSON_CLASS_LOCAL_NAMES:
            class_uris.add(subj)
    return class_uris


def _count_tbox_classes(tbox_graph: Graph) -> int:
    return len(
        {
            subj
            for subj in tbox_graph.subjects(RDF.type, OWL.Class)
            if isinstance(subj, URIRef)
        }
    )


def _count_tbox_object_properties(tbox_graph: Graph) -> int:
    return len(
        {
            subj
            for subj in tbox_graph.subjects(RDF.type, OWL.ObjectProperty)
            if isinstance(subj, URIRef)
        }
    )


def _people_in_graph(graph: Graph, person_class_uris: set[URIRef]) -> set[URIRef]:
    return {
        subj
        for subj in graph.subjects(RDF.type, None)
        if isinstance(subj, URIRef) and (subj, RDF.type, None) in graph and any((subj, RDF.type, cls) in graph for cls in person_class_uris)
    }


def _count_people_relation_triples(graph: Graph, person_class_uris: set[URIRef]) -> int:
    people = _people_in_graph(graph, person_class_uris)
    triples: set[tuple[str, str, str]] = set()
    for subj, pred, obj in graph:
        if pred == RDF.type:
            continue
        if not isinstance(subj, URIRef) or not isinstance(obj, URIRef):
            continue
        if subj in people and obj in people:
            triples.add(
                (
                    _uri_local_name(subj),
                    get_predicate_name(pred),
                    _uri_local_name(obj),
                )
            )

    # Count only semantically distinct relations using the same closure rules
    # as experiments/precision_recall.py.
    return len(deduplicate_by_synonymy(triples))


def characterize_dataset(tbox_path: Path, ground_truth_dir: Path, text_dir: Path) -> dict[str, float | int]:
    tbox_graph = Graph()
    tbox_graph.parse(tbox_path, format="turtle")

    text_lengths = _collect_text_lengths(text_dir)
    ttl_paths = _collect_ttl_paths(ground_truth_dir)

    common_ids = sorted(set(text_lengths) & set(ttl_paths))
    if not common_ids:
        raise ValueError("No matching .ttl/.txt pairs found by filename stem.")

    person_class_uris = _person_class_uris_from_tbox(tbox_graph)
    if not person_class_uris:
        raise ValueError("Could not find person-related classes (Person/Man/Woman/Ancestor) in the TBox.")

    triples_per_text: list[int] = []
    for item_id in common_ids:
        graph = Graph()
        graph.parse(ttl_paths[item_id], format="turtle")
        triples_per_text.append(_count_people_relation_triples(graph, person_class_uris))

    return {
        "num_tbox_classes": _count_tbox_classes(tbox_graph),
        "num_tbox_object_properties": _count_tbox_object_properties(tbox_graph),
        "num_paired_samples": len(common_ids),
        "avg_sentences_per_text": mean(text_lengths[item_id] for item_id in common_ids),
        "avg_people_relation_triples_per_text": mean(triples_per_text),
    }


def main() -> None:
    root = _repo_root()
    tbox_path = root / "custom_family_bench" / "family_TBOX.ttl"
    ground_truth_dir = root / "custom_family_bench" / "royalty" / "ground_truths"
    text_dir = root / "custom_family_bench" / "royalty" / "denoised_texts_fuzzy_match"

    metrics = characterize_dataset(tbox_path, ground_truth_dir, text_dir)

    print("Dataset Characterization")
    print("=" * 24)
    print(f"TBox classes: {metrics['num_tbox_classes']}")
    print(f"TBox object properties: {metrics['num_tbox_object_properties']}")
    print(f"Paired text/KG samples: {metrics['num_paired_samples']}")
    print(f"Average sentences per input example: {metrics['avg_sentences_per_text']:.2f}")
    print(
        "Average semantically distinct people-to-people triples per text: "
        f"{metrics['avg_people_relation_triples_per_text']:.2f}"
    )


if __name__ == "__main__":
    main()
