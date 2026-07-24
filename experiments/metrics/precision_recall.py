"""
Calculate precision and recall metrics for knowledge graph construction pipeline.

This script:
1. Matches extracted triples (from delta_graph.ttl) to ground truth triples
2. Filters out metadata triples
3. Keeps only extracted triples whose relation exists in ground truth
4. Keeps only extracted triples whose entities map to ground truth entities,
   while allowing class entities
4. Reports micro and macro metrics
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from rdflib import Graph, URIRef
import csv
from urllib.parse import unquote

# Metadata properties to filter out
METADATA_PROPERTIES = {
    "alsoKnownAs",
    "formerlyKnownAs",
    "hasBirthYear",
    "hasDeathYear",
    "hasMarriageYear",
    "knownAs",
    "hasSex",
    "wdtLink",
    "posIndicesFull",
    "posIndicesPart",
    "imports",
    "label"
}


def load_ground_truth_csv(csv_path: str) -> Dict[str, str]:
    """Load ground_truth.csv and map article URLs to q-ids.
    
    Returns dict mapping decoded filename to q-id.
    """
    article_to_qid = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            article_url = row['article']
            qid = row['item'].split('/')[-1]  # Extract Q-id from wikidata URL
            # Extract filename from article URL (last part after last /)
            filename = article_url.split('/')[-1]
            # Store both URL-encoded and decoded versions for matching
            article_to_qid[filename] = qid
            article_to_qid[unquote(filename)] = qid
    return article_to_qid


def get_sorted_texts(text_dir: str) -> List[Tuple[int, str]]:
    """Get sorted list of text files with their indices.
    
    Returns list of (index, filename) tuples.
    Note: Files are URL-encoded in the directory.
    """
    texts = sorted([f for f in os.listdir(text_dir) if f.endswith('.txt')])
    return [(i, f) for i, f in enumerate(texts)]


def get_qid_from_fuzzy_match(fuzzy_match_file: str) -> Optional[str]:
    """Extract Q-id from fuzzy_entity_match_map.json.
    
    Returns the main entity's Q-id if available.
    """
    try:
        with open(fuzzy_match_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            main_entity = data.get('main_entity', {})
            return main_entity.get('qid')
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_entity_mapping(fuzzy_match_file: str) -> Dict[str, str]:
    """Load fuzzy_entity_match_map.json and create URI mapping.

    Returns a mapping from extracted URIs to ground truth URIs for matched entities.
    """
    mapping = {}
    try:
        with open(fuzzy_match_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entity in data.get('entities', []):
                if entity.get('matched'):
                    extracted_uri = entity.get('extracted_uri')
                    ground_truth_uri = entity.get('ground_truth_uri')
                    if extracted_uri and ground_truth_uri:
                        mapping[extracted_uri] = ground_truth_uri
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return mapping


def get_class_entities(triples: Set[Tuple[str, str, str]]) -> Set[str]:
    """Extract known class names from rdf:type triples."""
    class_entities = set()
    for subject, predicate, obj in triples:
        if predicate == 'type':
            class_entities.add(obj)

    # Ignore OWL/RDFS infrastructure terms that are not user-level entities.
    class_entities.difference_update({
        'Ontology',
        'AnnotationProperty',
        'Class',
        'Thing',
        'Nothing',
        'NamedIndividual',
    })
    return class_entities


def normalize_uri(uri: str) -> str:
    """Extract local name from URI."""
    if '#' in uri:
        return uri.split('#')[-1]
    elif '/' in uri:
        return uri.split('/')[-1]
    return uri


def get_predicate_name(predicate: URIRef) -> str:
    """Extract predicate name from URIRef."""
    s = str(predicate)
    if '#' in s:
        return s.split('#')[-1]
    return s.split('/')[-1]


def is_metadata_property(predicate: URIRef) -> bool:
    """Check if predicate is a metadata property."""
    pred_name = get_predicate_name(predicate)
    return pred_name in METADATA_PROPERTIES


def load_and_normalize_graph(graph_path: str, entity_mapping: Optional[Dict[str, str]] = None) -> Set[Tuple[str, str, str]]:
    """Load a TTL graph and normalize URIs.
    
    Returns set of (subject, predicate, object) tuples as strings.
    """
    triples = set()
    try:
        g = Graph()
        g.parse(graph_path, format='turtle')
        
        for s, p, o in g.triples((None, None, None)):
            # Convert URIs to strings
            s_str = str(s)
            p_str = str(p)
            o_str = str(o)

            if entity_mapping:
                if s_str in entity_mapping:
                    s_str = entity_mapping[s_str]
                if o_str in entity_mapping:
                    o_str = entity_mapping[o_str]
            
            # Normalize to local names for comparison
            s_local = normalize_uri(s_str)
            o_local = normalize_uri(o_str)
            p_local = get_predicate_name(p)
            
            triples.add((s_local, p_local, o_local))
    except Exception as e:
        print(f"Error loading graph {graph_path}: {e}")
    
    return triples


def filter_triples(triples: Set[Tuple[str, str, str]]) -> Set[Tuple[str, str, str]]:
    """Filter out invalid triples.
    
    Removes:
    1. Triples with metadata predicates
    """
    filtered = set()
    for s, p, o in triples:
        if p in METADATA_PROPERTIES:
            continue
        
        filtered.add((s, p, o))
    
    return filtered


def filter_extracted_triples(
    extracted_triples: Set[Tuple[str, str, str]],
    ground_truth_triples: Set[Tuple[str, str, str]],
    entity_mapping: Dict[str, str],
) -> Set[Tuple[str, str, str]]:
    """Filter extracted triples to those comparable against ground truth."""
    allowed_predicates = {predicate for _, predicate, _ in ground_truth_triples}
    mapped_entities = {normalize_uri(uri) for uri in entity_mapping.values()}
    class_entities = get_class_entities(ground_truth_triples)

    filtered = set()
    for subject, predicate, obj in extracted_triples:
        if predicate in METADATA_PROPERTIES:
            continue

        if predicate not in allowed_predicates:
            continue

        subject_allowed = subject in mapped_entities or subject in class_entities
        object_allowed = obj in mapped_entities or obj in class_entities

        if subject_allowed and object_allowed:
            filtered.add((subject, predicate, obj))

    return filtered


def filter_ground_truth_triples(
    ground_truth_triples: Set[Tuple[str, str, str]],
    extracted_triples: Set[Tuple[str, str, str]],
    entity_mapping: Dict[str, str],
) -> Set[Tuple[str, str, str]]:
    """Filter ground-truth triples to the same comparable slice as extracted triples."""
    allowed_predicates = {predicate for _, predicate, _ in extracted_triples}
    mapped_entities = {normalize_uri(uri) for uri in entity_mapping.values()}
    class_entities = get_class_entities(ground_truth_triples)

    filtered = set()
    for subject, predicate, obj in ground_truth_triples:
        if predicate in METADATA_PROPERTIES:
            continue

        if predicate not in allowed_predicates:
            continue

        subject_allowed = subject in mapped_entities or subject in class_entities
        object_allowed = obj in mapped_entities or obj in class_entities

        if subject_allowed and object_allowed:
            filtered.add((subject, predicate, obj))

    return filtered


def calculate_metrics(extracted_triples: Set[Tuple[str, str, str]],
                    ground_truth_triples: Set[Tuple[str, str, str]]) -> Dict[str, float]:
    """Calculate precision, recall, and F1 score."""
    correct = len(extracted_triples & ground_truth_triples)
    total_extracted = len(extracted_triples)
    total_ground_truth = len(ground_truth_triples)
    
    precision = correct / total_extracted if total_extracted > 0 else 0.0
    recall = correct / total_ground_truth if total_ground_truth > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'correct': correct,
        'extracted': total_extracted,
        'ground_truth': total_ground_truth,
    }


def _subrun_sort_key(name: str):
    """Sort numerically by the leading "N_" index when present, else alphabetically."""
    prefix = name.split('_')[0]
    try:
        return (0, int(prefix))
    except ValueError:
        return (1, name)


def process_run(run_path: str, ground_truths_dir: str, data_graph_filename: str = "delta_graph_inferred.ttl") -> Tuple[Dict, List[Dict]]:
    """Process a single run and calculate metrics for all subruns."""

    run_name = os.path.basename(run_path)
    subrun_metrics = []
    all_precision = []
    all_recall = []
    all_f1 = []

    # Get all subrun directories
    subrun_dirs = [d for d in os.listdir(run_path)
                if os.path.isdir(os.path.join(run_path, d)) and '_' in d and
                d != "ontology_conformance_metrics"]

    for subrun_dir in sorted(subrun_dirs, key=_subrun_sort_key):
        try:
            subrun_path = os.path.join(run_path, subrun_dir)

            # Load file paths
            delta_graph_file = os.path.join(subrun_path, data_graph_filename)
            # Get Q-id from fuzzy match file
            fuzzy_match_file = os.path.join(subrun_path, "fuzzy_entity_match_map.json")
            qid = get_qid_from_fuzzy_match(fuzzy_match_file)
            if not qid:
                print(f"Warning: Could not extract Q-id from {fuzzy_match_file}")
                continue
            
            # Load ground truth
            ground_truth_file = os.path.join(ground_truths_dir, f"{qid}_inferred.ttl")
            if not os.path.exists(ground_truth_file):
                print(f"Warning: Ground truth file not found: {ground_truth_file}")
                continue
            
            if not os.path.exists(delta_graph_file):
                print(f"Warning: {data_graph_filename} not found in {subrun_path}")
                continue
            
            # Load graphs
            entity_mapping = get_entity_mapping(fuzzy_match_file)

            extracted_triples = load_and_normalize_graph(delta_graph_file, entity_mapping)
            ground_truth_triples = load_and_normalize_graph(ground_truth_file)
            
            # Filter triples down to comparable triples only
            extracted_filtered = filter_extracted_triples(
                extracted_triples,
                ground_truth_triples,
                entity_mapping,
            )
            ground_truth_filtered = filter_ground_truth_triples(
                ground_truth_triples,
                extracted_filtered,
                entity_mapping,
            )
            
            
            # Calculate metrics
            metrics = calculate_metrics(extracted_filtered, ground_truth_filtered)
            
            metrics['subrun'] = subrun_dir
            metrics['qid'] = qid
            
            subrun_metrics.append(metrics)
            
            all_precision.append(metrics['precision'])
            all_recall.append(metrics['recall'])
            all_f1.append(metrics['f1'])
            
        except Exception as e:
            print(f"Error processing subrun {subrun_dir}: {e}")
            import traceback
            traceback.print_exc()
    
    # Calculate micro and macro metrics
    total_correct = sum(m['correct'] for m in subrun_metrics)
    total_extracted = sum(m['extracted'] for m in subrun_metrics)
    total_ground_truth = sum(m['ground_truth'] for m in subrun_metrics)
    
    micro_precision = total_correct / total_extracted if total_extracted > 0 else 0.0
    micro_recall = total_correct / total_ground_truth if total_ground_truth > 0 else 0.0
    micro_f1 = 2 * (micro_precision * micro_recall) / (micro_precision + micro_recall) \
        if (micro_precision + micro_recall) > 0 else 0.0
    
    macro_precision = sum(all_precision) / len(all_precision) if all_precision else 0.0
    macro_recall = sum(all_recall) / len(all_recall) if all_recall else 0.0
    macro_f1 = sum(all_f1) / len(all_f1) if all_f1 else 0.0
    
    aggregated = {
        'run': run_name,
        'num_subruns': len(subrun_metrics),
        'micro': {
            'precision': micro_precision,
            'recall': micro_recall,
            'f1': micro_f1,
            'total_correct': total_correct,
            'total_extracted': total_extracted,
            'total_ground_truth': total_ground_truth,
        },
        'macro': {
            'precision': macro_precision,
            'recall': macro_recall,
            'f1': macro_f1,
        }
    }
    
    return aggregated, subrun_metrics

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate precision, recall and F1 metrics of a pipeline run."
    )
    parser.add_argument(
        "--results-root",
        type=Path,
        help="Root results directory containing run subdirectories.",
    )
    parser.add_argument(
        "--data-graph-filename",
        default="delta_graph_inferred.ttl",
        help="Which per-subrun inferred graph file to score (e.g. final_data_graph_inferred.ttl).",
    )
    parser.add_argument(
        "--output-filename",
        default="metrics.json",
        help="Filename to write the resulting metrics to, inside the run directory.",
    )

    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_args()
    run_dir = args.results_root

    ground_truths_dir = Path("custom_family_bench") / "royalty" / "ground_truths"

    if not os.path.isdir(run_dir):
        raise Exception("The provided run directory isn't a directory...")

    final_metrics = {}
    aggregated, subrun_metrics = process_run(str(run_dir), str(ground_truths_dir), args.data_graph_filename)
    final_metrics["aggregated"] = aggregated
    final_metrics["subrun_metrics"] = subrun_metrics
    
    print(f"  Micro - Precision: {aggregated['micro']['precision']:.4f}, "
            f"Recall: {aggregated['micro']['recall']:.4f}, "
            f"F1: {aggregated['micro']['f1']:.4f}")
    print(f"  Macro - Precision: {aggregated['macro']['precision']:.4f}, "
            f"Recall: {aggregated['macro']['recall']:.4f}, "
            f"F1: {aggregated['macro']['f1']:.4f}")
    
    # Output results
    output_file = run_dir / args.output_filename
    print(f"\nWriting results to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_metrics, f, indent=2)

if __name__ == "__main__":
    main()

