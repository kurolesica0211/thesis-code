# Dataset Collection Pipeline

This document describes how the royalty family-tree dataset (text/knowledge-graph pairs) used in the paper was built. The paper itself only has room for a brief summary; this is the full account, with pointers to the scripts that implement each step.

The pipeline has four stages:

1. [Querying Wikidata for ground-truth relations](#1-querying-wikidata-for-ground-truth-relations)
2. [Converting the ground truth to RDF](#2-converting-the-ground-truth-to-rdf)
3. [Fetching source texts and deriving denoised text/graph pairs](#3-fetching-source-texts-and-deriving-denoised-textgraph-pairs)
4. [Computing the inferential closure](#4-computing-the-inferential-closure)

## 1. Querying Wikidata for ground-truth relations

Ground-truth parent/child relations were collected by hand via the [Wikidata Query Service](https://query.wikidata.org/) web interface, using one SPARQL query per royal house. Each query starts from a "seed" individual — the reigning monarch of the United Kingdom (`wd:Q43274`, Charles III), Spain (`wd:Q191045`, Felipe VI), and the Netherlands (`wd:Q154952`, Willem-Alexander) — and expands outward along parent/child links to build a bounded family "pool," then extracts every parent/child edge inside that pool.

```sparql
#defaultView:Graph
SELECT DISTINCT ?item ?itemLabel ?parent ?parentLabel ?genderLabel ?article ?parentGenderLabel
WHERE {
  # 1. Define the 'Pool': Get ancestors (0 to 2 steps up)
  wd:Q43274 (wdt:P22|wdt:P25)?/(wdt:P22|wdt:P25)? ?ancestor .

  # Then all their descendants (0 to 2 steps down)
  ?ancestor wdt:P40?/wdt:P40? ?item .

  # 2. Define the 'Links': For every item in the pool, find their parents
  ?item (wdt:P22|wdt:P25) ?parent .

  ?item wdt:P21 ?gender .
  ?parent wdt:P21 ?parentGender .

  ?article schema:about ?item .
  ?article schema:isPartOf <https://en.wikipedia.org/> .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

The same query is re-run with `wd:Q191045` (Spain) and `wd:Q154952` (Netherlands) in place of `wd:Q43274`. All three are recorded in [`experiments/dataset_creation/queries.txt`](../experiments/dataset_creation/queries.txt).

What each query does:

- **Build the pool** — starting from the seed, walk up to 2 steps up the father/mother properties (`wdt:P22` "father", `wdt:P25` "mother") to reach ancestors, then up to 2 steps down the child property (`wdt:P40` "child") from each of those ancestors. This yields a bounded window of relatives around the seed (roughly great-grandparents down to great-grandchildren) rather than the entire, effectively unbounded, royal family graph.
- **Extract the links** — for every person in that pool, look up their parents directly (`wdt:P22`/`wdt:P25`), regardless of whether the parent itself is in the pool. This can pull in parents just outside the pool's boundary (e.g. someone who married into the family).
- **Filter for text availability** — `?article schema:about ?item` / `schema:isPartOf <https://en.wikipedia.org/>` restricts results to people who have an English Wikipedia article, since the downstream pipeline needs source text for each person.
- **Attach gender** — `wdt:P21` ("sex or gender") is fetched for both the person and the parent, later used to populate `hasSex`/`Man`/`Woman` in the RDF and to derive `hasFather`/`hasMother` distinctions.

The three result sets were concatenated into [`experiments/dataset_creation/ground_truth.csv`](../experiments/dataset_creation/ground_truth.csv) (one row per parent/child edge, 995 rows spanning 818 distinct people).

A second query then fetches English aliases (alternate names/titles) for every person appearing in `ground_truth.csv`, by pasting their Wikidata IDs into a `VALUES` clause:

```sparql
#defaultView:Graph
SELECT ?item ?itemLabel ?alias WHERE {
  # Define your list of Q-ids here
  VALUES ?item {
    # all people from ground_truth.csv
  }

  # Fetch the English alias
  ?item skos:altLabel ?alias .
  FILTER (LANG(?alias) = "en")

  # Optional: Fetch the English Label for clarity
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

The output was saved as [`experiments/dataset_creation/aliases.csv`](../experiments/dataset_creation/aliases.csv) (2,496 aliases). Aliases matter because Wikipedia prose frequently refers to royals by a title or historical name (e.g. "the Queen", "Prince of Wales") rather than their canonical Wikidata label, and the entity-matching step in stage 3 needs those variants to recognize a mention.

## 2. Converting the ground truth to RDF

[`experiments/dataset_creation/ground_truth_csv2ttl.py`](../experiments/dataset_creation/ground_truth_csv2ttl.py) merges `ground_truth.csv` and `aliases.csv` into a single Turtle graph, [`experiments/dataset_creation/ground_truth.ttl`](../experiments/dataset_creation/ground_truth.ttl), expressed against the family ontology TBox at [`custom_family_bench/family_TBOX.ttl`](../custom_family_bench/family_TBOX.ttl). For each CSV row it asserts:

- `:hasParent` between child and parent individuals,
- `rdf:type :Person` for both,
- `:hasSex` (pointing at a shared `:male`/`:female` individual, derived from `genderLabel`/`parentGenderLabel`),
- `rdfs:label` (the Wikidata label) and `:alsoKnownAs` (for each matching row in `aliases.csv`),
- `data:wdtLink`, an annotation property linking each generated individual back to its source Wikidata URI (used for lookups in later stages).

Individuals are named after a sanitized version of their Wikidata label (e.g. `data:Elizabeth_II`); if two different Wikidata entities would sanitize to the same name, a numeric suffix is appended to disambiguate them. An `owl:AllDifferent` axiom over all generated individuals is also emitted, since without it OWL would not otherwise treat two distinctly-named people as necessarily non-identical.

## 3. Fetching source texts and deriving denoised text/graph pairs

### 3a. Downloading article text

[`experiments/dataset_creation/get_text.py`](../experiments/dataset_creation/get_text.py) downloads the plain-text body of the English Wikipedia article for every `article` URL in `ground_truth.csv`, one file per person, into `custom_family_bench/royalty/original_texts/`.

### 3b. Denoising and localizing

[`experiments/dataset_creation/generate_fuzzy_denoised_pairs.py`](../experiments/dataset_creation/generate_fuzzy_denoised_pairs.py) is the core dataset-generation script. For each downloaded article it produces a matched pair:

- a **denoised text** — the subset of sentences from the article that mention a family member from the ground-truth graph — written to `custom_family_bench/royalty/denoised_texts_fuzzy_match/<QID>.txt`;
- a **localized ground-truth graph** — the subgraph of `ground_truth.ttl` restricted to the people mentioned in those sentences — written to `custom_family_bench/royalty/ground_truths/<QID>.ttl`.

This step exists because a full Wikipedia biography contains a lot of text unrelated to family relations (career, works, awards, etc.), and the full `ground_truth.ttl` graph contains relations for hundreds of people who are never mentioned in any one article. Pairing each article with only the graph fragment it actually supports keeps the text/graph pairs tight and avoids rewarding the pipeline for "hallucinating" a correct triple it had no textual basis for.

The main steps, per article:

1. **Restrict the candidate entity set.** Starting from the article's main subject, the script takes the subgraph reachable within 3 relation hops in `ground_truth.ttl` (ignoring purely metadata predicates like `rdf:type` or labels) as the pool of people who could plausibly be mentioned in that person's biography.
2. **Segment into sentences** with spaCy (`en_core_web_sm`).
3. **Fuzzy-match full names.** For each candidate entity, every known label/alias is tokenized, and a spaCy `Matcher` pattern is built that allows up to edit-distance-2 fuzzy matches (`FUZZY2`) on tokens of 4+ characters — this absorbs OCR noise, alternate spellings, and diacritic variation (e.g. "Alexandrine" vs. "Alexandrina") without requiring an exact string match.
4. **Fall back to surname/given-name tokens.** A person's full name rarely reappears in every sentence about them; after their first full-name match, later sentences are also scanned for standalone tokens from their name (excluding function words, Roman numerals, and ordinals like "3rd"), so that a sentence like "His son later succeeded him" — read together with a previous match — still counts if a bare surname is present. This fallback is only applied for entities already fully matched in an earlier sentence, and only outside spans already claimed by a full match, to avoid falsely tagging generic words.
5. **Keep sentences with at least one match.** Sentences with no matched entity are dropped; the retained sentences are concatenated (in original order) to form the denoised text. The article's opening sentence is always kept (even with no match) to preserve basic context about who the article is about.
6. **Emit the localized graph.** All entities mentioned across the kept sentences (plus the article's main subject) are kept, along with every ground-truth relation between two kept entities, their labels/aliases/sex, and annotations recording each mention's character offsets in the denoised text (`data:posIndicesFull` for full fuzzy name matches, `data:posIndicesPart` for the fallback token matches).

Run over all downloaded articles, this produced 499 denoised text/localized-graph pairs (a handful of articles were dropped because the fuzzy matcher found no sentence mentioning a known family member).

## 4. Computing the inferential closure

The localized graphs from stage 3 only contain the relations pulled directly from Wikidata (essentially `:hasParent` and `:hasSex`) — they don't spell out derived facts like `:hasFather`, `:hasBrother`, or `:hasChild`. [`experiments/infer_kg.py`](../experiments/infer_kg.py) materializes those by loading each localized graph together with the ontology TBox ([`custom_family_bench/family_TBOX.ttl`](../custom_family_bench/family_TBOX.ttl)) into [Owlready2](https://owlready2.readthedocs.io/) and running the [Pellet](https://github.com/stardog-union/pellet) OWL reasoner (`sync_reasoner_pellet`) with property-value inference enabled.

The TBox encodes the family-relation vocabulary as OWL axioms plus a handful of SWRL rules, so a single reasoning pass derives, for example:

- `:hasFather` / `:hasMother` from `:hasParent` combined with the parent's `:hasSex`,
- `:hasChild` and its sex-specific subproperties `:hasSon` / `:hasDaughter` as the inverse of `:hasParent`, via SWRL rules keyed on the child's sex,
- `:hasBrother` / `:hasSister` from the `:isSiblingOf` property chain (`:hasParent` ∘ `:isParentOf`) combined with sex, again via SWRL,
- `:isAuntOf` / `:isUncleOf` from property chains over sibling and parent relations,
- class memberships (`:Person`, `:Man`, `:Woman`, `:Ancestor`) implied by the property assertions and their domain/range restrictions.

Each `<QID>.ttl` localized graph therefore has a sibling `<QID>_inferred.ttl` containing its materialized closure — the final text/KG pairs used in the paper are (denoised text, inferred closure graph).

## Directory summary

| Path | Contents |
| --- | --- |
| [`experiments/dataset_creation/queries.txt`](../experiments/dataset_creation/queries.txt) | The four SPARQL queries (3 seed-family queries + the alias query) |
| [`experiments/dataset_creation/ground_truth.csv`](../experiments/dataset_creation/ground_truth.csv) | Concatenated Wikidata parent/child query results |
| [`experiments/dataset_creation/aliases.csv`](../experiments/dataset_creation/aliases.csv) | English aliases per person |
| [`experiments/dataset_creation/ground_truth_csv2ttl.py`](../experiments/dataset_creation/ground_truth_csv2ttl.py) | CSV → Turtle conversion |
| [`experiments/dataset_creation/ground_truth.ttl`](../experiments/dataset_creation/ground_truth.ttl) | Full ground-truth RDF graph |
| [`experiments/dataset_creation/get_text.py`](../experiments/dataset_creation/get_text.py) | Wikipedia article downloader |
| [`custom_family_bench/royalty/original_texts/`](../custom_family_bench/royalty/original_texts/) | Raw downloaded article text |
| [`experiments/dataset_creation/generate_fuzzy_denoised_pairs.py`](../experiments/dataset_creation/generate_fuzzy_denoised_pairs.py) | Denoising + graph localization |
| [`custom_family_bench/royalty/denoised_texts_fuzzy_match/`](../custom_family_bench/royalty/denoised_texts_fuzzy_match/) | Denoised per-person texts |
| [`custom_family_bench/royalty/ground_truths/`](../custom_family_bench/royalty/ground_truths/) | Localized graphs (`<QID>.ttl`) and their inferred closures (`<QID>_inferred.ttl`) |
| [`experiments/infer_kg.py`](../experiments/infer_kg.py) | Pellet-based inferential closure |
| [`custom_family_bench/family_TBOX.ttl`](../custom_family_bench/family_TBOX.ttl) | Family-relation ontology (OWL + SWRL) |
