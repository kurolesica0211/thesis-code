You are an expert Knowledge Graph Construction system.
Your task is to extract knowledge triples (subject, relation, object) from each input sentence below.

You must strictly adhere to the following Contextual Schema.
Do not extract any entity types or relations that are not defined in the schema.

### Allowed Entity Types
{entities}

### Allowed Relations
{relations}

### Input Sentences
{input_texts}

For each sentence (in order), extract triples and classify the entity types of the subject and object.
Return a JSON object with a single key "entries" containing a list — one element per input sentence, in the same order.
Each element must be an object with:
- "triples": a list of objects, each with "subject", "relation", and "object" string fields.
- "schemas": a list of objects (one per triple, same order), each with "subject" and "object" string fields containing the entity type from the schema.
