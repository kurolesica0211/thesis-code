================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
The Duke of Castro  The Duchess of Castro


Princess Béatrice Marie Caroline Louise Françoise of Bourbon-Two Sicilies (born 16 June 1950 in Saint-Raphaël, Var, France) is the eldest daughter of Prince Ferdinand, Duke of Castro, Castro-line claimant to the headship of the House of Bourbon-Two Sicilies, and his wife, Chantal de Chevron-Villette.
Her younger brother, Prince Carlo, Duke of Castro, is the current Castro-line claimant to the headship of the House of Bourbon-Two Sicilies.
Marriage and issue

Béatrice married Charles Napoléon Bonaparte, eldest son of Louis, Prince Napoléon and his wife, Alix de Foresta, on 19 December 1978 in Paris, France.
Charles was the great-great-grandnephew of Napoleon I of France, founder of the Imperial House of France.
Béatrice and Charles had two children:


Title, styles and honours

Title and styles

Honours

Ancestry

References



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (59d3aa66-a63e-43a9-bb8e-62bfc74e1e7b)
 Call ID: 59d3aa66-a63e-43a9-bb8e-62bfc74e1e7b
  Args:
    source: Béatrice_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (7772f2ba-efa4-4c12-a34d-1b014e82e40a)
 Call ID: 7772f2ba-efa4-4c12-a34d-1b014e82e40a
  Args:
    source: Béatrice_of_Bourbon-Two_Sicilies
    type: :Woman
  AddLiteral (3fac8030-83eb-44af-a312-c4d0519f2f27)
 Call ID: 3fac8030-83eb-44af-a312-c4d0519f2f27
  Args:
    literal_type: xsd:integer
    source: Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_value: 1950
  AssignClass (f7d05ce3-2ba5-4232-b5bd-3c0871113717)
 Call ID: f7d05ce3-2ba5-4232-b5bd-3c0871113717
  Args:
    source: Ferdinand_Duke_of_Castro
    type: :Person
  AssignClass (2c319d91-5703-4f68-befe-3c53f156830c)
 Call ID: 2c319d91-5703-4f68-befe-3c53f156830c
  Args:
    source: Ferdinand_Duke_of_Castro
    type: :Man
  AssignClass (9d3f9f1f-9b2a-4b7d-a8c5-99e21c108c3e)
 Call ID: 9d3f9f1f-9b2a-4b7d-a8c5-99e21c108c3e
  Args:
    source: Ferdinand_Duke_of_Castro
    type: :Ancestor
  AssignClass (4dd3ddbd-7621-46af-bbb3-21645ed23141)
 Call ID: 4dd3ddbd-7621-46af-bbb3-21645ed23141
  Args:
    source: Chantal_de_Chevron-Villette
    type: :Person
  AssignClass (94e45373-c265-4622-b30a-593b4e48fee6)
 Call ID: 94e45373-c265-4622-b30a-593b4e48fee6
  Args:
    type: :Woman
    source: Chantal_de_Chevron-Villette
  AssignClass (6ba983cc-e65f-4215-8ee6-9a82853f0b5b)
 Call ID: 6ba983cc-e65f-4215-8ee6-9a82853f0b5b
  Args:
    source: Chantal_de_Chevron-Villette
    type: :Ancestor
  AddTriple (36022fc3-1daf-4e63-beec-3c0aecc53728)
 Call ID: 36022fc3-1daf-4e63-beec-3c0aecc53728
  Args:
    target: Ferdinand_Duke_of_Castro
    source: Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (1f874878-5f8d-41ea-b4dc-f47c34223240)
 Call ID: 1f874878-5f8d-41ea-b4dc-f47c34223240
  Args:
    target: Chantal_de_Chevron-Villette
    source: Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (60dd317c-6f86-4abe-a0ba-baa3e27dded7)
 Call ID: 60dd317c-6f86-4abe-a0ba-baa3e27dded7
  Args:
    type: :Person
    source: Carlo_Duke_of_Castro
  AssignClass (ade1a0b4-bf5f-4d48-bf0f-5cb2e94dc17a)
 Call ID: ade1a0b4-bf5f-4d48-bf0f-5cb2e94dc17a
  Args:
    source: Carlo_Duke_of_Castro
    type: :Man
  AddTriple (44fbaca5-8fc0-47cb-be8f-f62870197b20)
 Call ID: 44fbaca5-8fc0-47cb-be8f-f62870197b20
  Args:
    target: Carlo_Duke_of_Castro
    source: Béatrice_of_Bourbon-Two_Sicilies
    relation: :hasBrother
  AddTriple (ff5b84a7-1688-4c72-a683-6c5b1ff1cdd9)
 Call ID: ff5b84a7-1688-4c72-a683-6c5b1ff1cdd9
  Args:
    target: Ferdinand_Duke_of_Castro
    source: Carlo_Duke_of_Castro
    relation: :hasFather
  AddTriple (5392376c-ff0c-4236-b170-68dc26c50095)
 Call ID: 5392376c-ff0c-4236-b170-68dc26c50095
  Args:
    target: Chantal_de_Chevron-Villette
    source: Carlo_Duke_of_Castro
    relation: :hasMother
  AssignClass (f9a4d02f-2a4b-4d6f-b90e-90d5e0242c02)
 Call ID: f9a4d02f-2a4b-4d6f-b90e-90d5e0242c02
  Args:
    source: Charles_Napoléon_Bonaparte
    type: :Person
  AssignClass (19935dc7-a05c-416c-92b1-0c971cfd2559)
 Call ID: 19935dc7-a05c-416c-92b1-0c971cfd2559
  Args:
    source: Charles_Napoléon_Bonaparte
    type: :Man
  AddLiteral (c5bee8a1-23f0-4c9c-ae27-3413b9824ada)
 Call ID: c5bee8a1-23f0-4c9c-ae27-3413b9824ada
  Args:
    relation: :hasMarriageYear
    source: Béatrice_of_Bourbon-Two_Sicilies
    literal_value: 1978
    literal_type: xsd:integer
  AddTriple (287c5304-4387-46ae-af46-fdef4379872c)
 Call ID: 287c5304-4387-46ae-af46-fdef4379872c
  Args:
    target: Charles_Napoléon_Bonaparte
    relation: :hasRelation
    source: Béatrice_of_Bourbon-Two_Sicilies
  AssignClass (504b8c13-01d8-457e-815f-c584cb86d77a)
 Call ID: 504b8c13-01d8-457e-815f-c584cb86d77a
  Args:
    type: :Person
    source: Louis_Prince_Napoléon
  AssignClass (9b998efa-5155-4db0-8288-d13f4d4b1399)
 Call ID: 9b998efa-5155-4db0-8288-d13f4d4b1399
  Args:
    type: :Man
    source: Louis_Prince_Napoléon
  AssignClass (c92ac324-0f2d-4490-9718-fa9a6933facf)
 Call ID: c92ac324-0f2d-4490-9718-fa9a6933facf
  Args:
    source: Louis_Prince_Napoléon
    type: :Ancestor
  AssignClass (6922d233-8b04-438a-bbb3-40e2765c46be)
 Call ID: 6922d233-8b04-438a-bbb3-40e2765c46be
  Args:
    type: :Person
    source: Alix_de_Foresta
  AssignClass (19f48ad7-f187-489c-bea1-dfe0da71383d)
 Call ID: 19f48ad7-f187-489c-bea1-dfe0da71383d
  Args:
    type: :Woman
    source: Alix_de_Foresta
  AssignClass (71dc6f7d-b015-4fb2-b0f4-6b2b234f774a)
 Call ID: 71dc6f7d-b015-4fb2-b0f4-6b2b234f774a
  Args:
    type: :Ancestor
    source: Alix_de_Foresta
  AddTriple (15b64d3e-25df-4b73-8633-8ae5b5e0f07e)
 Call ID: 15b64d3e-25df-4b73-8633-8ae5b5e0f07e
  Args:
    source: Charles_Napoléon_Bonaparte
    relation: :hasFather
    target: Louis_Prince_Napoléon
  AddTriple (21994cef-3663-4a17-b9f7-8d005f5c6c5b)
 Call ID: 21994cef-3663-4a17-b9f7-8d005f5c6c5b
  Args:
    source: Charles_Napoléon_Bonaparte
    relation: :hasMother
    target: Alix_de_Foresta
  AssignClass (842af3ca-a5ad-408d-926f-e0ef3b4c8b2f)
 Call ID: 842af3ca-a5ad-408d-926f-e0ef3b4c8b2f
  Args:
    type: :Person
    source: Napoleon_I_of_France
  AssignClass (1daba7c3-c7b1-4861-bed6-cda12a9e1721)
 Call ID: 1daba7c3-c7b1-4861-bed6-cda12a9e1721
  Args:
    source: Napoleon_I_of_France
    type: :Man
  Finish (d4149430-219f-4ca6-ad8b-e69a485cff0c)
 Call ID: d4149430-219f-4ca6-ad8b-e69a485cff0c
  Args: