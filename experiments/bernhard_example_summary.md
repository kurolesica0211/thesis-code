# Prince Bernhard Example & Triple Extraction Pipeline Summary

## Input Text (verbatim from Wikipedia)

> "Bernhard was born Bernhard Leopold Friedrich Eberhard Julius Kurt Karl Gottfried Peter, Count of Biesterfeld in Jena, Saxe-Weimar-Eisenach, German Empire on 29 June 1911, the elder son of **Prince Bernhard of Lippe** (1872–1934) and his wife, **Baroness Armgard von Sierstorpff-Cramm**. The eldest daughter is **Beatrix** (born 1938), who later became Queen of the Netherlands. His other daughters with **Juliana** are **Irene** (born 1939), **Margriet** (born 1943) and **Christina** (1947–2019)."

---

## Ground Truth Triples (from Wikidata `ground_truth.csv`)

| Subject | Relation | Object |
|---|---|---|
| Q57304 (Bernhard) | `hasParent` | Q649601 (Prince Bernhard of Lippe) |
| Q57304 (Bernhard) | `hasParent` | Q2802589 (Baroness Armgard) |
| Q29574 (Beatrix) | `hasParent` | Q57304 (Bernhard) |
| Q263623 (Irene) | `hasParent` | Q57304 (Bernhard) |
| Q268821 (Margriet) | `hasParent` | Q57304 (Bernhard) |
| Q435324 (Christina) | `hasParent` | Q57304 (Bernhard) |

---

## Pipeline Architecture

The system is a **LangGraph agent loop** that iteratively edits an RDF graph using LLM tool calls, validated by SHACL constraints.

```
Input text + Ontology (TTL) + empty Data Graph
        ↓
   [LLM Node] — reads messages, issues tool calls
        ↓
   [Tools Node] — executes: AssignClass / AddTriple / AddLiteral / ValidateShacl / Finish
        ↓ (violation message fed back as ToolMessage)
   [LLM Node] — iterates to fix violations
        ↓ (Finish passes all checks)
   final_data_graph.ttl + delta_graph.ttl + conversation log
```

Key design choices:
- **Tool arguments are constrained** to valid ontology terms via Pydantic `Literal` types — the model cannot invent relations outside `family_TBOX.ttl`
- **SHACL validation** runs on demand; violations are translated to natural language instructions and fed back to the LLM
- **Finish is gated**: model must have called `ValidateShacl`, all nodes must be typed, and minimum iterations must be reached before the run ends

---

## Iteration-by-Iteration Trace

The run used 10 iterations (the configured maximum). Each iteration corresponds to one LLM turn → tool execution cycle. The graph state after each iteration is shown below.

| Iter | Tool call | Result | Graph delta |
|---|---|---|---|
| 1 | `AssignClass(Bernhard, :Man)` | ✅ | Bernhard typed as `:Man` |
| 2 | `AddLiteral(Bernhard, :hasBirthYear, 1911, xsd:year)` | ❌ silent fail | No change — `xsd:year` is not a valid XSD type |
| 3 | `AssignClass(Prince Bernhard of Lippe, :Man)` | ✅ | Father node typed as `:Man` |
| 4 | `AddLiteral(Prince Bernhard of Lippe, :hasBirthYear, 1872, xsd:year)` | ❌ silent fail | No change |
| 5 | `AddLiteral(Prince Bernhard of Lippe, :hasDeathYear, 1934, xsd:year)` | ❌ silent fail | No change |
| 6 | `AssignClass(Baroness Armgard, :Woman)` | ✅ | Mother node typed as `:Woman` |
| 7 | `AddTriple(Bernhard, :hasFather, Prince Bernhard of Lippe)` | ✅ | Father relation added |
| 8 | `AddTriple(Bernhard, :hasMother, Baroness Armgard)` | ✅ | Mother relation added |
| 9 | `AssignClass(Beatrix, :Woman)` | ✅ | Beatrix typed as `:Woman` |
| 10 | `AddLiteral(Beatrix, :hasBirthYear, 1938, xsd:year)` | ❌ silent fail | No change — **max_iterations hit, run terminated** |

### Graph state after each iteration

**Iter 1**
```turtle
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man .
```

**Iter 2–3** *(iter 2 no-op)*
```turtle
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man .
data:Prince_Bernhard_of_Lippe a :Man .
```

**Iter 4–5** *(no-ops)*
```turtle
— no change —
```

**Iter 6**
```turtle
data:Baroness_Armgard_von_Sierstorpff-Cramm a :Woman .
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man .
data:Prince_Bernhard_of_Lippe a :Man .
```

**Iter 7**
```turtle
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man ;
    :hasFather data:Prince_Bernhard_of_Lippe .
data:Baroness_Armgard_von_Sierstorpff-Cramm a :Woman .
data:Prince_Bernhard_of_Lippe a :Man .
```

**Iter 8**
```turtle
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man ;
    :hasFather data:Prince_Bernhard_of_Lippe ;
    :hasMother data:Baroness_Armgard_von_Sierstorpff-Cramm .
data:Baroness_Armgard_von_Sierstorpff-Cramm a :Woman .
data:Prince_Bernhard_of_Lippe a :Man .
```

**Iter 9**
```turtle
data:Beatrix a :Woman .
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man ;
    :hasFather data:Prince_Bernhard_of_Lippe ;
    :hasMother data:Baroness_Armgard_von_Sierstorpff-Cramm .
data:Baroness_Armgard_von_Sierstorpff-Cramm a :Woman .
data:Prince_Bernhard_of_Lippe a :Man .
```

**Iter 10 — final (no change, run terminated)**
```turtle
data:Beatrix a :Woman .
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man ;
    :hasFather data:Prince_Bernhard_of_Lippe ;
    :hasMother data:Baroness_Armgard_von_Sierstorpff-Cramm .
data:Baroness_Armgard_von_Sierstorpff-Cramm a :Woman .
data:Prince_Bernhard_of_Lippe a :Man .
```

---

## Extracted Graph (actual pipeline output)

```turtle
data:Bernhard_Leopold_Friedrich_..._Count_of_Biesterfeld a :Man ;
    :hasFather data:Prince_Bernhard_of_Lippe ;
    :hasMother data:Baroness_Armgard_von_Sierstorpff-Cramm .

data:Prince_Bernhard_of_Lippe a :Man .
data:Baroness_Armgard_von_Sierstorpff-Cramm a :Woman .
data:Beatrix a :Woman .
```

---

## Evaluation Against Ground Truth

| Triple | Status | Issue |
|---|---|---|
| Bernhard `hasFather` Prince Bernhard of Lippe | ✅ | — |
| Bernhard `hasMother` Baroness Armgard | ✅ | — |
| Beatrix typed `:Woman` | ✅ | — |
| Beatrix `hasParent` Bernhard | ❌ | Not reached |
| Irene, Margriet, Christina typed + `hasParent` | ❌ | Not reached |
| Entity naming | ⚠️ | Used full birth name instead of `Prince_Bernhard_of_Lippe-Biesterfeld` |

**Root cause of incomplete extraction:** 3 of 10 iterations were wasted on `AddLiteral` calls using `xsd:year` (invalid XSD type; correct form is `xsd:gYear`), which failed silently without advancing the graph. Combined with the model issuing one tool call per turn instead of batching, the 10-iteration budget was exhausted before Beatrix's parent relation and Irene, Margriet, and Christina were processed. Increasing `max_iterations` and reinforcing batching in the system prompt are the two levers to address this.
