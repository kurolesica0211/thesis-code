"""
Generate denoised texts for the family benchmark (Option A).

For each Wikipedia article in ground_truth.csv:
1. Collect related entity labels: parents of the subject + children of the subject
2. Fetch the Wikipedia article text via the wikitext API
3. Split into sentences and keep only those mentioning at least one related entity
4. Write filtered text to custom_family_bench/royalty/denoised_texts/{page_name}.txt

Run from the project root:
    python scripts/generate_denoised_texts.py
"""

from __future__ import annotations

import csv
import re
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path

import requests
from tqdm import tqdm


GROUND_TRUTH_PATH = Path("custom_family_bench/royalty/ground_truth.csv")
DENOISED_DIR = Path("custom_family_bench/royalty/denoised_texts")
FETCH_API = "https://wikitext.eluni.co/api/extract"
REQUEST_DELAY = 3.0
MAX_RETRIES = 3

# Short words that are not useful as standalone entity name variants
_STOP_WORDS = {
    "of", "the", "von", "van", "de", "du", "di", "vom", "den",
    "der", "und", "and", "for", "with", "from",
}


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_article(url: str) -> str | None:
    encoded = urllib.parse.quote(url, safe="")
    final_url = f"{FETCH_API}?url={encoded}&format=text"
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(final_url, timeout=15)
            if resp.status_code == 429:
                tqdm.write(f"    Rate limited — waiting 30s...")
                time.sleep(30)
                continue
            resp.raise_for_status()
            return resp.content.decode("utf-8")
        except requests.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(10)
            else:
                tqdm.write(f"    Failed after {MAX_RETRIES} attempts: {e}")
                return None
    return None


# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list[str]:
    # Split on sentence-ending punctuation followed by whitespace or end-of-string
    raw = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in raw if s.strip()]


# ---------------------------------------------------------------------------
# Entity matching
# ---------------------------------------------------------------------------

def name_variants(label: str) -> list[str]:
    """
    Generate candidate substrings for matching a label in free text.

    E.g. "Prince Bernhard of Lippe" →
         ["Prince Bernhard of Lippe", "Prince", "Bernhard", "Lippe"]
    Short prepositions and stop words are excluded as standalone variants.
    """
    variants = [label]
    for word in label.split():
        if len(word) > 3 and word[0].isupper() and word.lower() not in _STOP_WORDS:
            variants.append(word)
    return variants


def sentence_covers_entity(sentence: str, label: str) -> bool:
    return any(variant in sentence for variant in name_variants(label))


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_sentences(text: str, related_labels: set[str]) -> str:
    kept = [
        sent for sent in split_sentences(text)
        if any(sentence_covers_entity(sent, label) for label in related_labels)
    ]
    return " ".join(kept)


# ---------------------------------------------------------------------------
# Ground truth loading
# ---------------------------------------------------------------------------

def load_ground_truth(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    DENOISED_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_ground_truth(GROUND_TRUTH_PATH)

    # Group rows by article URL
    article_rows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        article_rows[row["article"]].append(row)

    # Build reverse map: parent Q-ID → set of child labels
    # (so we can also find sentences mentioning the subject's children)
    child_labels_by_parent: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        child_labels_by_parent[row["parent"]].add(row["itemLabel"])

    articles = sorted(article_rows.keys())
    print(f"Found {len(articles)} unique articles.")

    skipped, saved, failed = 0, 0, 0

    for article_url in tqdm(articles, desc="Generating denoised texts"):
        page_name = article_url.split("/")[-1]
        out_path = DENOISED_DIR / f"{page_name}.txt"

        if out_path.exists():
            skipped += 1
            continue

        url_rows = article_rows[article_url]
        item_qid = url_rows[0]["item"]

        # Related entities: direct parents + children of the subject
        parent_labels: set[str] = {row["parentLabel"] for row in url_rows}
        child_labels: set[str] = child_labels_by_parent.get(item_qid, set())
        related_labels = parent_labels | child_labels

        text = fetch_article(article_url)
        if text is None:
            tqdm.write(f"  SKIP (fetch failed): {page_name}")
            failed += 1
            continue

        denoised = filter_sentences(text, related_labels)

        if not denoised:
            tqdm.write(f"  WARNING: no sentences matched for {page_name} — keeping first paragraph")
            denoised = split_sentences(text)[0] if text.strip() else text

        out_path.write_text(denoised, encoding="utf-8")
        tqdm.write(
            f"  {page_name}: {len(related_labels)} entities, "
            f"{len(split_sentences(text))} → {len(split_sentences(denoised))} sentences"
        )
        saved += 1
        time.sleep(REQUEST_DELAY)

    print(f"\nDone. Saved: {saved} | Skipped (exists): {skipped} | Failed: {failed}")


if __name__ == "__main__":
    main()
