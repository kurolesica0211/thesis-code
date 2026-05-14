from __future__ import annotations

from generate_fuzzy_denoised_pairs import (build_matcher, collect_mentions_for_sentence,
                                        load_spacy_pipeline, load_ground_truth_graph)

graph, entity_by_qid = load_ground_truth_graph("custom_family_bench/royalty/ground_truth_inferred.ttl")
nlp = load_spacy_pipeline("en_core_web_sm")

sentence_text = "After her husband died, she was officially known as Queen Elizabeth the Queen Mother to avoid confusion with her daughter Queen Elizabeth II."