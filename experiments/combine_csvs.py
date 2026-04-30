import csv
import glob
import os

# Get all CSV files in the gold_triples_csvs directory
csv_dir = 'experiments/gold_triples_csvs'
csv_files = sorted(glob.glob(os.path.join(csv_dir, '*.csv')))

print(f"Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f"  - {f}")

# Read and combine all CSV files
output_file = 'experiments/combined_gold_triples.csv'
row_count = 0
duplicate_count = 0
seen_rows = set()

with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = None
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            if writer is None:
                # Initialize writer with fieldnames from first file
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                print(f"Columns: {fieldnames}")
            
            # Write all rows from this file
            for row in reader:
                # Use all columns as a stable deduplication key.
                row_key = tuple(row.get(col, '') for col in fieldnames)
                if row_key in seen_rows:
                    duplicate_count += 1
                    continue

                seen_rows.add(row_key)
                writer.writerow(row)
                row_count += 1

print(f"\nCombined {row_count} rows")
print(f"Skipped {duplicate_count} duplicate rows")
print(f"Output saved to {output_file}")
