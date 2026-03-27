import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rdflib import Graph
import json
from validators.shacl_validator import OntologyIndex, validate_batch
from models.data_models import Triple, TripleSchema, EntryExtractionResult
from typing import List
import dataclasses

shapes = Graph()
shapes.parse("custom_family_bench/family_TBOX_shacl_opened.ttl", format="turtle")

with open("custom_family_bench/family_TBOX_shacl_opened.ttl", "r", encoding="utf-8") as f:
    shacl_data = f.read()

with open("custom_family_bench/family_TBOX.owl", "r", encoding="utf-8") as f:
    ontology_data = f.read()

with open("results/habsburgs_rdf_shacl_gemini_gemini-flash-lite-latest/results.json", "r", encoding="utf-8") as f:
    records = json.load(f)
    
ont_idx = OntologyIndex(ontology_data, "xml")

pred_triples: List[Triple] = []
pred_schemas: List[TripleSchema] = []

for triple in records[0]["pred_triples"]:
    pred_triples.append(Triple(**triple))
for schema in records[0]["pred_schemas"]:
    pred_schemas.append(TripleSchema(**schema))

extraction_results = EntryExtractionResult(triples=pred_triples, schemas=pred_schemas)
extraction_dict = {"entry_1": extraction_results}

validation_results = validate_batch(extraction_dict, ontology_data, shacl_data, ontology_format="xml")

with open("validation_report.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(dataclasses.asdict(validation_results[0]), indent=2))
    
with open("data_graph.ttl", "w", encoding="utf-8") as f:
    f.write(validation_results[2])