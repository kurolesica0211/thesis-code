from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from rdflib import Graph, URIRef
from sentence_transformers import SentenceTransformer, util
import numpy as np


def parse_args() -> object:
    parser = ArgumentParser(description="Measure coverage between two RDF graphs using entity-name embeddings.")
    parser.add_argument("source_graph", help="Path to the graph whose coverage will be measured.")
    parser.add_argument("target_graph", help="Path to the graph used as the coverage reference.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="Cosine similarity threshold for considering two entity names a match.",
    )
    parser.add_argument(
        "--model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="SentenceTransformer model name to use for entity matching.",
    )
    return parser.parse_args()


def local_name(value: str) -> str:
    if "#" in value:
        return value.rsplit("#", 1)[-1]
    if "/" in value:
        return value.rsplit("/", 1)[-1]
    return value


def load_subject_names(graph_path: str) -> list[str]:
    graph = Graph()
    graph.parse(graph_path)
    return sorted(
        {
            local_name(str(subject))
            for subject in graph.subjects()
            if isinstance(subject, URIRef)
        }
    )


def match_coverage(source_names: list[str], target_names: list[str], model: SentenceTransformer, threshold: float) -> tuple[int, int, float, list[tuple[str, str, float]]]:
    if not source_names:
        return 0, 0, 0.0, []
    if not target_names:
        return 0, len(source_names), 0.0, []

    source_embeddings = model.encode(source_names, convert_to_tensor=True, normalize_embeddings=True)
    target_embeddings = model.encode(target_names, convert_to_tensor=True, normalize_embeddings=True)
    similarity_matrix = util.cos_sim(source_embeddings, target_embeddings)

    covered = 0
    matches: list[tuple[str, str, float]] = []
    for source_index, source_name in enumerate(source_names):
        scores = similarity_matrix[source_index].cpu().numpy()
        indices = np.where(scores >= threshold)[0]
        passing_scores = scores[indices]
        sort_order = np.argsort(passing_scores)[::-1]
        sorted_scores = passing_scores[sort_order]
        sorted_indices = indices[sort_order]
        
        for idx, best_score in zip(sorted_indices, sorted_scores):
            target = target_names[int(idx)]
            if any(match[1] == target for match in matches):
                continue
            else:
                score = float(best_score)
                covered += 1
                matches.append((source_name, target, score))
                break

    return covered, len(source_names) - covered, covered / len(source_names), matches


def print_report(label: str, source_names: list[str], target_names: list[str], model: SentenceTransformer, threshold: float) -> None:
    covered, uncovered, fraction, matches = match_coverage(source_names, target_names, model, threshold)
    print(f"{label}:")
    print(f"  unique source entities: {len(source_names)}")
    print(f"  unique target entities: {len(target_names)}")
    print(f"  matched entities: {covered}")
    print(f"  unmatched entities: {uncovered}")
    print(f"  coverage fraction: {fraction:.4f}")
    print(f"  threshold: {threshold:.2f}")
    if matches:
        print("  matches:")
        for source_name, target_name, score in matches:
            print(f"    {source_name} -> {target_name} ({score:.4f})")


def main() -> None:
    args = parse_args()
    source_path = Path(args.source_graph)
    target_path = Path(args.target_graph)

    source_names = load_subject_names(str(source_path))
    target_names = load_subject_names(str(target_path))
    model = SentenceTransformer(args.model)

    print_report(
        f"Coverage of {source_path.name} by {target_path.name}",
        source_names,
        target_names,
        model,
        args.threshold,
    )


if __name__ == "__main__":
    main()
