import csv
import re

def extract_qid(uri):
    """Extract Q-ID from a Wikidata URI."""
    match = re.search(r'Q\d+', uri)
    return match.group(0) if match else None

def trace_ancestors(csv_file, output_file):
    """
    Trace ancestors from CSV and find the oldest relatives (leaf nodes).
    A leaf node is someone who appears as an ancestor but not as an item.
    """
    # Read CSV
    items = {}  # map: item_uri -> ancestor_uri
    item_qids = set()  # set of all item Q-IDs
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_uri = row['item']
            ancestor_uri = row['ancestor']
            items[item_uri] = ancestor_uri
            item_qids.add(extract_qid(item_uri))
    
    # Find all unique ancestor URIs
    all_ancestors = set(items.values())
    
    # Find leaf nodes: ancestors that don't appear as items
    leaf_nodes = set()
    for ancestor_uri in all_ancestors:
        ancestor_qid = extract_qid(ancestor_uri)
        if ancestor_uri not in items:
            # This ancestor doesn't have their own row, so they're a leaf node
            leaf_nodes.add(ancestor_qid)
    
    # Write results
    sorted_qids = sorted(leaf_nodes)
    with open(output_file, 'w', encoding='utf-8') as f:
        for qid in sorted_qids:
            f.write(qid + '\n')
    
    print(f"Found {len(leaf_nodes)} oldest relatives (leaf nodes)")
    print(f"Results written to {output_file}")
    print(f"\nFirst 20 Q-IDs:")
    for qid in sorted_qids[:20]:
        print(qid)

if __name__ == '__main__':
    csv_file = 'experiments/gold_triples_csvs/query.csv'
    output_file = 'experiments/oldest_relatives_qids.txt'
    trace_ancestors(csv_file, output_file)
