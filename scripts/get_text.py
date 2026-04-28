from __future__ import annotations

import urllib.parse
import requests
import csv


links = []
with open("custom_family_bench/wpLinks.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        links.append(row.get("article"))

base_url = "https://wikitext.eluni.co/api/extract?"
for link in links:
    wiki_url = urllib.parse.quote(link, safe="")
    params = {
        "url": wiki_url,
        "format": "text"
    }

    final_url = base_url + urllib.parse.urlencode(params)

    response = requests.get(final_url)
    text = response.content.decode()

    filename = link.split("/")[-1]
    filepath = f"custom_family_bench/potential_texts/{filename}.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)