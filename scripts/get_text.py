from __future__ import annotations

import urllib.parse
import requests
import csv
import time
from tqdm import tqdm


links = set()
with open("custom_family_bench/british_royalty/ground_truth.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        links.add(row.get("article"))

base_url = "https://wikitext.eluni.co/api/extract?"
for link in tqdm(links, desc="Fetching articles"):
    wiki_url = urllib.parse.quote(link, safe="")
    params = {
        "url": wiki_url,
        "format": "text"
    }

    final_url = base_url + urllib.parse.urlencode(params)

    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(final_url, timeout=10)
            
            # Handle 429 Rate Limit error
            if response.status_code == 429:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"\n⚠️  Rate limited (429) for {link}. Retrying in 30 seconds...")
                    time.sleep(30)
                    continue
                else:
                    print(f"\n❌ Failed to fetch {link} after {max_retries} retries (429)")
                    break
            
            # Raise exception for other HTTP errors
            response.raise_for_status()
            
            text = response.content.decode()
            filename = link.split("/")[-1]
            filepath = f"custom_family_bench/british_royalty/texts/{filename}.txt"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            
            # Success - wait 5 seconds before next request
            time.sleep(5)
            break
            
        except requests.exceptions.RequestException as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"\n⚠️  Request failed for {link}: {e}. Retrying in 30 seconds...")
                time.sleep(30)
            else:
                print(f"\n❌ Failed to fetch {link} after {max_retries} attempts: {e}")