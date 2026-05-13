"""
Generate denoised texts for the family benchmark (Option A).

For each Wikipedia article in ground_truth.csv:
1. Collect related entity labels: parents of the subject + children of the subject
2. Read the Wikipedia article text from custom_family_bench/royalty/texts
3. Split into sentences and keep only those mentioning at least one related entity
4. Write filtered text to custom_family_bench/royalty/denoised_texts/{wikidata_id}.txt

Run from the project root:
    python scripts/generate_denoised_texts.py
"""

from __future__ import annotations

import csv
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm


GROUND_TRUTH_PATH = Path("custom_family_bench/royalty/ground_truth.csv")
TEXTS_DIR = Path("custom_family_bench/royalty/texts")
DENOISED_DIR = Path("custom_family_bench/royalty/denoised_texts")

# Short words that are not useful as standalone entity name variants
_STOP_WORDS = {
    "of", "the", "von", "van", "de", "du", "di", "vom", "den",
    "der", "und", "and", "for", "with", "from",
}


# ---------------------------------------------------------------------------
# File naming and loading
# ---------------------------------------------------------------------------

def wikidata_id(link: str) -> str:
    return link.rsplit("/", 1)[-1]


def text_filename_from_article(article_url: str) -> str:
    return urllib.parse.urlparse(article_url).path.rsplit("/", 1)[-1] + ".txt"


def text_filename_from_label(label: str) -> str:
    normalized = label.replace(" ", "_")
    return urllib.parse.quote(normalized, safe=",()_-.") + ".txt"


def load_article_text(article_url: str, label: str) -> str | None:
    path = TEXTS_DIR / text_filename_from_article(article_url)
    if not path.exists():
        path = TEXTS_DIR / text_filename_from_label(label)
    if not path.exists():
        tqdm.write(f"    Missing text file: {path.name}")
        return None
    return path.read_text(encoding="utf-8")


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

    # Group rows by item QID so each subject is processed once.
    item_rows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        item_rows[wikidata_id(row["item"])].append(row)

    # Build reverse map: parent Q-ID → set of child labels
    # (so we can also find sentences mentioning the subject's children)
    child_labels_by_parent: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        child_labels_by_parent[wikidata_id(row["parent"])].add(row["itemLabel"])

    items = sorted(item_rows.keys())
    print(f"Found {len(items)} unique items.")

    skipped, saved, failed = 0, 0, 0

    for item_qid in tqdm(items, desc="Generating denoised texts"):
        out_path = DENOISED_DIR / f"{item_qid}.txt"

        if out_path.exists():
            skipped += 1
            continue

        url_rows = item_rows[item_qid]

        # Related entities: direct parents + children of the subject
        parent_labels: set[str] = {row["parentLabel"] for row in url_rows}
        child_labels: set[str] = child_labels_by_parent.get(item_qid, set())
        related_labels = parent_labels | child_labels

        text = load_article_text(url_rows[0]["article"], url_rows[0]["itemLabel"])
        if text is None:
            tqdm.write(f"  SKIP (missing text): {item_qid}")
            failed += 1
            continue

        denoised = filter_sentences(text, related_labels)

        if not denoised:
            tqdm.write(f"  WARNING: no sentences matched for {item_qid} — keeping first paragraph")
            denoised = split_sentences(text)[0] if text.strip() else text

        out_path.write_text(denoised, encoding="utf-8")
        tqdm.write(
            f"  {item_qid}: {len(related_labels)} entities, "
            f"{len(split_sentences(text))} → {len(split_sentences(denoised))} sentences"
        )
        saved += 1

    print(f"\nDone. Saved: {saved} | Skipped (exists): {skipped} | Failed: {failed}")


if __name__ == "__main__":
    main()
