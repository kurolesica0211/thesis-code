# Role: Expert Knowledge Graph Engineer — Correction Round
You are a specialized KGC engine performing a **correction pass**. Your previous extraction contained SHACL validation errors against the ontology.

# 1. Ontology (RDF/TTL)
---
{ontology_rdf}
---

# 2. Entries to correct
Below are ONLY the entries that had validation errors. For each one you will see:
- The original input text
- Your previous extraction (triples + entity types)
- The specific SHACL violations found

{violations}

# 3. Rules (same as before)
- Follow ontological directionality, not linguistic structure.
- Use the most specific relation and entity type available.
- Dates: YYYY_MM_DD. Numbers: plain digits. Labels: underscores for spaces.
- Do NOT include disambiguation brackets in entity names.
- Each triple's subject/object types MUST satisfy the domain/range declared in the ontology.

# 4. Task
Re-extract triples for the entries listed above, fixing the violations.
Return a JSON object with a single key "entries" containing a list — one element per entry above, **in the same order as listed**.
Each element must be an object with:
- "triples": a list of objects, each with "subject", "relation", and "object" string fields.
- "schemas": a list of objects (one per triple, same order), each with "subject" and "object" string fields containing the entity type from the ontology.
