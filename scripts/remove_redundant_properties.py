#!/usr/bin/env python3
"""
Remove redundant and reflexive triples from an RDF graph based on property hierarchy.

A triple (s, p, o) is considered redundant if there exists another triple (s, p', o)
where p' is a subproperty of p. This keeps the most specific properties and removes
the more general ones.

Reflexive triples (where s == o) are also removed as they are logically invalid
for most family relations (e.g., an individual cannot be their own parent, sibling, etc).

Example: If both hasMother(X, Y) and hasParent(X, Y) exist, and hasMother is a 
subproperty of hasParent, then hasParent is redundant. Also, hasSister(X, X) is invalid.
"""

from rdflib import Graph, RDFS
import sys

def build_subproperty_map(tbox_path):
    """
    Build a map of properties to their subproperties (transitive closure).
    
    Args:
        tbox_path: Path to the ontology (TBOX) file
        
    Returns:
        A dict mapping each property to the set of all its subproperties (including itself)
    """
    g = Graph()
    g.parse(tbox_path, format='turtle')
    
    # Collect direct subproperty relationships: property -> set of immediate subproperties
    subprop_of = {}
    
    for subprop, _, superprop in g.triples((None, RDFS.subPropertyOf, None)):
        if superprop not in subprop_of:
            subprop_of[superprop] = set()
        subprop_of[superprop].add(subprop)
    
    # Compute transitive closure: for each property, find ALL subproperties
    def get_all_subprops(prop, memo=None):
        if memo is None:
            memo = {}
        if prop in memo:
            return memo[prop]
        
        # Start with the property itself
        result = {prop}
        
        # Add all immediate subproperties and their subproperties recursively
        if prop in subprop_of:
            for subprop in subprop_of[prop]:
                result.update(get_all_subprops(subprop, memo))
        
        memo[prop] = result
        return result
    
    # Identify all properties in the ontology
    all_props = set()
    for subprop, _, superprop in g.triples((None, RDFS.subPropertyOf, None)):
        all_props.add(subprop)
        all_props.add(superprop)
    
    # Build complete subproperty map with transitive closure
    memo = {}
    subprops_map = {}
    for prop in all_props:
        subprops_map[prop] = get_all_subprops(prop, memo)
    
    return subprops_map

def remove_redundant_triples(inferred_path, tbox_path, output_path):
    """
    Remove redundant and reflexive triples from the inferred graph.
    
    A triple (s, p, o) is redundant if there exists another triple (s, p', o)
    where p' is a subproperty of p. Only the most specific properties are kept.
    
    Reflexive triples (where s == o) are removed as they are logically invalid
    for family relations.
    
    Args:
        inferred_path: Path to the input RDF graph with inferred triples
        tbox_path: Path to the ontology (TBOX) file
        output_path: Path where the cleaned graph will be saved
    """
    print(f"Loading property hierarchy from {tbox_path}...")
    subprops_map = build_subproperty_map(tbox_path)
    print(f"Found {len(subprops_map)} properties with subproperty relationships")
    
    print(f"\nLoading inferred graph from {inferred_path}...")
    g = Graph()
    g.parse(inferred_path, format='turtle')
    print(f"Loaded {len(g)} triples")
    
    # Group triples by (subject, object) pair
    so_pairs = {}
    all_triples = list(g)
    
    for s, p, o in all_triples:
        key = (s, o)
        if key not in so_pairs:
            so_pairs[key] = []
        so_pairs[key].append(p)
    
    # Find redundant triples
    triples_to_remove = []
    
    for (s, o), properties in so_pairs.items():
        # For each property connecting this subject-object pair
        for p in properties:
            # Get all subproperties of p (including p itself)
            subprops = subprops_map.get(p, {p})
            
            # Check if any other property is a subproperty of p
            for other_p in properties:
                if other_p != p and other_p in subprops:
                    # other_p is more specific than p, so p is redundant
                    triples_to_remove.append((s, p, o))
                    break
    
    print(f"\nIdentified {len(triples_to_remove)} redundant triples")
    
    # Find reflexive triples (where subject == object)
    reflexive_triples = [(s, p, o) for s, p, o in g if s == o]
    print(f"Identified {len(reflexive_triples)} reflexive triples")
    
    # Remove redundant triples
    for triple in triples_to_remove:
        g.remove(triple)
    
    # Remove reflexive triples
    for triple in reflexive_triples:
        g.remove(triple)
    
    # Save result
    g.serialize(output_path, format='turtle')
    
    print(f"Saved cleaned graph to {output_path}")
    print(f"Final graph contains {len(g)} triples")
    print(f"\nRemoval summary:")
    print(f"  Original:            {len(all_triples)} triples")
    print(f"  Removed (redundant): {len(triples_to_remove)} triples ({100*len(triples_to_remove)/len(all_triples):.1f}%)")
    print(f"  Removed (reflexive): {len(reflexive_triples)} triples ({100*len(reflexive_triples)/len(all_triples):.1f}%)")
    print(f"  Final:               {len(g)} triples")

if __name__ == '__main__':
    remove_redundant_triples(
        'custom_family_bench/royalty/ground_truth_fully_inferred.ttl',
        'custom_family_bench/family_TBOX.ttl',
        'custom_family_bench/royalty/ground_truth_inferred.ttl'
    )
