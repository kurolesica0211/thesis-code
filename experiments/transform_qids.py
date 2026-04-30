with open('experiments/oldest_relatives_qids.txt', 'r') as f:
    qids = [line.strip() for line in f if line.strip()]

output = ' '.join([f'wd:{qid}' for qid in qids])

with open('experiments/oldest_relatives_qids.txt', 'w') as f:
    f.write(output)

print(f"Transformed {len(qids)} Q-IDs")
print(f"\nOutput (first 200 chars):\n{output[:200]}...")
