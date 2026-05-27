"""
Calculate precision and recall metrics for knowledge graph construction pipeline.

This script:
1. Matches extracted triples (from delta_graph.ttl) to ground truth triples
2. Filters out invalid triples based on entity matching and predicate types
3. Calculates semantic precision/recall using synonym relations
4. Reports micro and macro metrics
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque
from rdflib import Graph, URIRef, Namespace
import csv
import sys
from urllib.parse import unquote

# Synonym relations from precision_recall.py
DIRECT_SYNONYMS = [
    ("hasParent", "hasMother"),
    ("hasParent", "hasFather"),
    ("hasParent", "isDaughterOf"),
    ("hasParent", "isSonOf"),
    ("hasParent", "isChildOf"),
    ("hasChild", "hasDaughter"),
    ("hasChild", "hasSon"),
    ("hasChild", "isFatherOf"),
    ("hasChild", "isMotherOf"),
    ("hasChild", "isParentOf"),
    ("isSiblingOf", "isBrotherOf"),
    ("isSiblingOf", "isSisterOf"),
    ("isSiblingOf", "hasBrother"),
    ("isSiblingOf", "hasSister"),
]

INVERSE_SYNONYMS = [
    ("hasParent", "isParentOf"),
    ("isSiblingOf", "isSiblingOf"),
]

# Metadata properties to filter out
METADATA_PROPERTIES = {
    "alsoKnownAs",
    "formerlyKnownAs",
    "hasBirthYear",
    "hasDeathYear",
    "hasMarriageYear",
    "knownAs",
    "type",  # RDF.type
    "hasSex",
    "wdtLink",
    "posIndicesFull",
    "posIndicesPart",
    "imports",
    "label"
}

# Derived relations to filter out
FILTERED_RELATIONS = {
    "hasAncestor",
    "hasRelation",
    "isBloodrelationOf",
    "hasFemalePartner",
    "hasMalePartner"
}


def compute_synonym_closure() -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Compute transitive closure of synonym relations.
    
    Closure rules:
    - Direct ∘ Direct = Direct (if A~dB and B~dC then A~dC)
    - Inverse ∘ Inverse = Direct (if A~iB and B~iC then A~dC)
    - Direct ∘ Inverse = Inverse (if A~dB and B~iC then A~iC)
    - Inverse ∘ Direct = Inverse (if A~iB and B~dC then A~iC)
    
    Returns:
        Tuple of:
        - direct_synonyms: Dict[str, Set[str]] - all pairs that are directly synonymous
        - inverse_synonyms: Dict[str, Set[str]] - all pairs that are inversely synonymous
    """
    # Build graph of relations with labeled edges
    edges = defaultdict(list)  # edges[A] = [(B, 'direct'), (C, 'inverse'), ...]
    all_relations = set()
    
    # Add initial direct synonymies
    for rel1, rel2 in DIRECT_SYNONYMS:
        edges[rel1].append((rel2, 'direct'))
        edges[rel2].append((rel1, 'direct'))
        all_relations.add(rel1)
        all_relations.add(rel2)
    
    # Add initial inverse synonymies
    for rel1, rel2 in INVERSE_SYNONYMS:
        edges[rel1].append((rel2, 'inverse'))
        edges[rel2].append((rel1, 'inverse'))
        all_relations.add(rel1)
        all_relations.add(rel2)
    
    # Compute transitive closure using BFS from each starting relation
    direct_synonyms = defaultdict(set)
    inverse_synonyms = defaultdict(set)
    for start_rel in all_relations:
        # BFS over (relation, parity) states so we do not lose inverse reachability.
        visited_states = {(start_rel, 'direct')}
        queue = deque([(start_rel, 'direct')])  # Start with 'direct' to self (identity)
        reachable_parities = defaultdict(set)
        
        while queue:
            current_rel, current_type = queue.popleft()
            reachable_parities[current_rel].add(current_type)
            
            # Explore all neighbors
            for next_rel, edge_type in edges[current_rel]:
                # Compose relation types using the closure rules
                if current_type == 'direct':
                    # d ∘ d = d,  d ∘ i = i
                    new_type = edge_type
                else:  # current_type == 'inverse'
                    # i ∘ d = i,  i ∘ i = d
                    new_type = 'direct' if edge_type == 'inverse' else 'inverse'
                
                next_state = (next_rel, new_type)
                if next_state not in visited_states:
                    visited_states.add(next_state)
                    queue.append(next_state)
        
        # Store computed relations (excluding self-loops)
        for rel, parities in reachable_parities.items():
            if rel == start_rel:
                if 'inverse' in parities:
                    inverse_synonyms[start_rel].add(start_rel)
                continue

            if 'direct' in parities:
                direct_synonyms[start_rel].add(rel)
            if 'inverse' in parities:
                inverse_synonyms[start_rel].add(rel)
    
    return dict(direct_synonyms), dict(inverse_synonyms)


# Compute synonym closure at module initialization
_DIRECT_SYN_CLOSURE, _INVERSE_SYN_CLOSURE = compute_synonym_closure()


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
    
    Returns dict mapping extracted URIs to ground truth URIs.
    """
    mapping = {}
    try:
        with open(fuzzy_match_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entity in data.get('entities', []):
                if entity['matched']:
                    extracted_uri = entity['extracted_uri']
                    # Map to ground truth URI
                    ground_truth_uri = entity['ground_truth_uri']
                    if ground_truth_uri:
                        mapping[extracted_uri] = ground_truth_uri
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return mapping


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
    return pred_name in METADATA_PROPERTIES or str(predicate).endswith('type')


def should_filter_relation(predicate: URIRef) -> bool:
    """Check if relation should be filtered out."""
    pred_name = get_predicate_name(predicate)
    return pred_name in FILTERED_RELATIONS


def get_equivalent_triples(subject: str, predicate: str, obj: str) -> Set[Tuple[str, str, str]]:
    """Get all semantically equivalent forms of a triple.
    
    Uses transitive closure of synonym relations to handle:
    1. Direct synonyms: (s, p1, o) == (s, p2, o) where p1 and p2 are directly synonymous
    2. Inverse synonyms: (s, p1, o) == (o, p2, s) where p1 and p2 are inversely synonymous
    
    All transitively inferred relations are included through the closure sets.
    """
    equivalent = {(subject, predicate, obj)}
    
    # Add all directly synonymous predicates
    for syn_pred in _DIRECT_SYN_CLOSURE.get(predicate, set()):
        equivalent.add((subject, syn_pred, obj))
    
    # Add all inversely synonymous predicates (with subject/object swapped)
    for inv_pred in _INVERSE_SYN_CLOSURE.get(predicate, set()):
        equivalent.add((obj, inv_pred, subject))
    
    return equivalent


def load_and_normalize_graph(graph_path: str, entity_mapping: Dict[str, str]) -> Set[Tuple[str, str, str]]:
    """Load a TTL graph and normalize URIs using entity mapping.
    
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
            
            # Map extracted URIs to ground truth URIs if they exist
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


def filter_triples(triples: Set[Tuple[str, str, str]], 
                valid_entities: Optional[Set[str]] = None) -> Set[Tuple[str, str, str]]:
    """Filter out invalid triples.
    
    Removes:
    1. Triples with unmatched entities (if valid_entities provided)
    2. Triples with metadata predicates
    3. Triples with filtered relations
    """
    filtered = set()
    for s, p, o in triples:
        # Check entity matching if provided
        if valid_entities and (s not in valid_entities or o not in valid_entities):
            continue
        
        # Check predicates
        if p in METADATA_PROPERTIES or p in FILTERED_RELATIONS:
            continue
        
        filtered.add((s, p, o))
    
    return filtered


def deduplicate_by_synonymy(triples: Set[Tuple[str, str, str]]) -> Set[Tuple[str, str, str]]:
    """Remove duplicate triples that are semantically equivalent.
    
    For each group of equivalent triples, keep only one representative.
    """
    if not triples:
        return triples
    
    seen_equivalents = set()
    deduplicated = set()
    
    for triple in triples:
        s, p, o = triple
        equivalents = get_equivalent_triples(s, p, o)
        
        # Create a canonical form to detect duplicates
        canonical = frozenset(equivalents)
        if canonical not in seen_equivalents:
            seen_equivalents.add(canonical)
            deduplicated.add(triple)
    
    return deduplicated


def calculate_metrics(extracted_triples: Set[Tuple[str, str, str]],
                    ground_truth_triples: Set[Tuple[str, str, str]]) -> Dict[str, float]:
    """Calculate precision, recall, and F1 score."""
    
    # Deduplicate by synonymy
    extracted_dedup = deduplicate_by_synonymy(extracted_triples)
    ground_truth_dedup = deduplicate_by_synonymy(ground_truth_triples)
    
    # Count correct triples (those in both sets, considering synonymy)
    correct = 0
    for extracted_triple in extracted_dedup:
        s, p, o = extracted_triple
        equivalents = get_equivalent_triples(s, p, o)
        
        # Check if any equivalent form exists in ground truth
        for equiv in equivalents:
            if equiv in ground_truth_dedup:
                correct += 1
                break
    
    total_extracted = len(extracted_dedup)
    total_ground_truth = len(ground_truth_dedup)
    
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


def get_valid_entities_from_matching(fuzzy_match_file: str) -> Set[str]:
    """Get set of entities that were successfully matched."""
    valid = set()
    try:
        with open(fuzzy_match_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entity in data.get('entities', []):
                if entity['matched']:
                    ground_truth_uri = entity['ground_truth_uri']
                    if ground_truth_uri:
                        valid.add(normalize_uri(ground_truth_uri))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return valid


def process_run(run_path: str, ground_truths_dir: str) -> Tuple[Dict, List[Dict]]:
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
    
    for subrun_dir in sorted(subrun_dirs, key=lambda x: int(x.split('_')[0])):
        try:
            subrun_path = os.path.join(run_path, subrun_dir)
            
            # Load file paths
            delta_graph_file = os.path.join(subrun_path, "delta_graph.ttl")
            fuzzy_match_file = os.path.join(subrun_path, "fuzzy_entity_match_map.json")
            
            # Get Q-id from fuzzy match file
            qid = get_qid_from_fuzzy_match(fuzzy_match_file)
            if not qid:
                print(f"Warning: Could not extract Q-id from {fuzzy_match_file}")
                continue
            
            # Load ground truth
            ground_truth_file = os.path.join(ground_truths_dir, f"{qid}.ttl")
            if not os.path.exists(ground_truth_file):
                print(f"Warning: Ground truth file not found: {ground_truth_file}")
                continue
            
            if not os.path.exists(delta_graph_file):
                print(f"Warning: delta_graph.ttl not found in {subrun_path}")
                continue
            
            # Get entity mapping
            entity_mapping = get_entity_mapping(fuzzy_match_file)
            
            # Load graphs
            extracted_triples = load_and_normalize_graph(delta_graph_file, entity_mapping)
            ground_truth_triples = load_and_normalize_graph(ground_truth_file, {})
            
            # Get valid entities (those successfully matched)
            valid_entities = get_valid_entities_from_matching(fuzzy_match_file)
            
            # Filter extracted triples
            extracted_filtered = filter_triples(extracted_triples, valid_entities)
            
            # Filter ground truth triples (same filters)
            ground_truth_filtered = filter_triples(ground_truth_triples)
            
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

    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_args()
    run_dir = args.results_root
    
    ground_truths_dir = Path("custom_family_bench") / "royalty" / "ground_truths"
    
    if not os.path.isdir(run_dir):
        raise Exception("The provided run directory isn't a directory...")
    
    final_metrics = {}
    aggregated, subrun_metrics = process_run(str(run_dir), str(ground_truths_dir))
    final_metrics["aggregated"] = aggregated
    final_metrics["subrun_metrics"] = subrun_metrics
    
    print(f"  Micro - Precision: {aggregated['micro']['precision']:.4f}, "
            f"Recall: {aggregated['micro']['recall']:.4f}, "
            f"F1: {aggregated['micro']['f1']:.4f}")
    print(f"  Macro - Precision: {aggregated['macro']['precision']:.4f}, "
            f"Recall: {aggregated['macro']['recall']:.4f}, "
            f"F1: {aggregated['macro']['f1']:.4f}")
    
    # Output results
    output_file = run_dir / "metrics.json"
    print(f"\nWriting results to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_metrics, f, indent=2)

if __name__ == "__main__":
    main()

