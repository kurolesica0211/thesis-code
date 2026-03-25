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
Correct ONLY the violated triples for the entries listed above.

Every listed "Correction item" must be addressed. Do not leave any listed violated indexed triple unchanged.

Return JSON in this exact shape:
- top-level key: "entries"
- "entries" must be an OBJECT with keys "entry_1", "entry_2", ... in the same order as listed above

For each `entries.entry_k`:
- "triples": list of corrected factual assertions, each with subject/relation/object entity IDs
- "schemas": list of corrected type-pairs (same length/order as "triples"), where each pair gives ontology class types for that triple's subject and object

Meaning of each part:
- `triples[i]` is the instance-level fact: (`subject`, `relation`, `object`).
- `schemas[i]` is the type signature for `triples[i]`: (`subject` class, `object` class).
- Therefore, each `schemas[i].subject` and `schemas[i].object` MUST be ontology class/type names (e.g., `Person`, `Man`, `Woman`, `Sex`, `DomainEntity`) and NOT entity IDs.

Schema typing constraints:
- Use only class/type identifiers present in the ontology for schema values.
- Never put entry/entity labels in `schemas` (invalid examples: `entry_1__Albert_I`, `Radbot`).
- Keep `triples` and `schemas` aligned one-to-one and in the same order.

Each triple object MUST contain:
- "triple_idx" (integer)
- "subject" (string)
- "relation" (string)
- "object" (string)

Index rules:
- For an existing violated triple, keep its exact `triple_idx` from the prompt.
- Use `triple_idx = -1` ONLY when adding a brand-new triple to satisfy an unmapped violation.
- Do NOT invent arbitrary new positive indices.
- Do NOT return a full re-extraction of the whole text; return only corrections for listed violations.
