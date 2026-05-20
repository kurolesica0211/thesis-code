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
Sir Simon Alexander Bowes-Lyon (born 17 June 1932) is a British businessman who served as Lord Lieutenant of Hertfordshire from 1986 to 2007.
He was a maternal first cousin of Elizabeth II.
Early life and family

Bowes-Lyon was born in 1932, the son of The Hon.
Sir David Bowes-Lyon (1902–1961) and Rachel Pauline Spender-Clay (1907–1996).
His mother was the daughter of Herbert Spender-Clay and Pauline Astor.
He resides at St Paul's Walden Bury, the reputed birthplace of his aunt, Queen Elizabeth The Queen Mother.
Career

Bowes-Lyon was educated at Eton College and graduated from Magdalen College, Oxford with a Master of Arts.
On 12 November 1971, Bowes-Lyon was nominated as Sheriff of Hertfordshire in the Queen's Bench Division of the High Court of Justice, a position previously held by his father.
Bowes-Lyon was appointed Lord Lieutenant of Hertfordshire on 12 February 1986, a position his father held from 1952–1961.



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
  AssignClass (719a3a36-d6bc-4a7a-a65a-bc268d02351a)
 Call ID: 719a3a36-d6bc-4a7a-a65a-bc268d02351a
  Args:
    type: :Man
    source: :SimonAlexanderBowesLyon
  AssignClass (ad23d811-cfed-403c-8fe8-d1be4f49c944)
 Call ID: ad23d811-cfed-403c-8fe8-d1be4f49c944
  Args:
    type: :Person
    source: :SimonAlexanderBowesLyon
  AddLiteral (6104557a-5660-4692-a1c2-cb7bd9bb651d)
 Call ID: 6104557a-5660-4692-a1c2-cb7bd9bb651d
  Args:
    relation: :hasBirthYear
    source: :SimonAlexanderBowesLyon
    literal_type: xsd:integer
    literal_value: 1932
  AssignClass (5f730a93-8dff-4989-94cd-cde23070160d)
 Call ID: 5f730a93-8dff-4989-94cd-cde23070160d
  Args:
    type: :Man
    source: :DavidBowesLyon
  AssignClass (f71b1293-c25b-46f5-baa8-6f8473585b90)
 Call ID: f71b1293-c25b-46f5-baa8-6f8473585b90
  Args:
    source: :DavidBowesLyon
    type: :Person
  AddLiteral (dfbc4099-98f7-43ab-b055-760ee8cbf8c7)
 Call ID: dfbc4099-98f7-43ab-b055-760ee8cbf8c7
  Args:
    literal_value: 1902
    literal_type: xsd:integer
    source: :DavidBowesLyon
    relation: :hasBirthYear
  AddLiteral (b80d1e62-5e62-44fe-9b78-95bd3341dcc7)
 Call ID: b80d1e62-5e62-44fe-9b78-95bd3341dcc7
  Args:
    relation: :hasDeathYear
    source: :DavidBowesLyon
    literal_type: xsd:integer
    literal_value: 1961
  AssignClass (28786043-9fc6-4e9f-8a7c-bcd32765a031)
 Call ID: 28786043-9fc6-4e9f-8a7c-bcd32765a031
  Args:
    source: :RachelPaulineSpenderClay
    type: :Woman
  AssignClass (6e535749-7790-44a7-9f55-22b96523913b)
 Call ID: 6e535749-7790-44a7-9f55-22b96523913b
  Args:
    source: :RachelPaulineSpenderClay
    type: :Person
  AddLiteral (9bac113f-1cbf-4330-a134-c29ad3c6d20b)
 Call ID: 9bac113f-1cbf-4330-a134-c29ad3c6d20b
  Args:
    relation: :hasBirthYear
    source: :RachelPaulineSpenderClay
    literal_type: xsd:integer
    literal_value: 1907
  AddLiteral (ade1d9de-4f6f-4281-92b2-5a3d31fe6a03)
 Call ID: ade1d9de-4f6f-4281-92b2-5a3d31fe6a03
  Args:
    relation: :hasDeathYear
    source: :RachelPaulineSpenderClay
    literal_type: xsd:integer
    literal_value: 1996
  AddTriple (3f56f166-b944-47ec-aa39-3b4697ae67d0)
 Call ID: 3f56f166-b944-47ec-aa39-3b4697ae67d0
  Args:
    target: :DavidBowesLyon
    relation: :hasFather
    source: :SimonAlexanderBowesLyon
  AddTriple (c7520369-7cfc-42a3-ad40-ad474cf33325)
 Call ID: c7520369-7cfc-42a3-ad40-ad474cf33325
  Args:
    source: :SimonAlexanderBowesLyon
    target: :RachelPaulineSpenderClay
    relation: :hasMother
  AssignClass (551a4e3c-c127-4353-b145-d9e7becdd97c)
 Call ID: 551a4e3c-c127-4353-b145-d9e7becdd97c
  Args:
    type: :Man
    source: :HerbertSpenderClay
  AssignClass (7f8fd005-b2bb-4788-b8b1-8adc1c4d8713)
 Call ID: 7f8fd005-b2bb-4788-b8b1-8adc1c4d8713
  Args:
    type: :Person
    source: :HerbertSpenderClay
  AssignClass (c9c9b19b-dabc-4cd9-bfa5-663dc3be9dd7)
 Call ID: c9c9b19b-dabc-4cd9-bfa5-663dc3be9dd7
  Args:
    type: :Woman
    source: :PaulineAstor
  AssignClass (275800b6-6598-486e-8a33-dd716a8ba2b6)
 Call ID: 275800b6-6598-486e-8a33-dd716a8ba2b6
  Args:
    source: :PaulineAstor
    type: :Person
  AddTriple (1c0a3229-beb4-410c-9895-7456e89b30ac)
 Call ID: 1c0a3229-beb4-410c-9895-7456e89b30ac
  Args:
    target: :HerbertSpenderClay
    relation: :hasFather
    source: :RachelPaulineSpenderClay
  AddTriple (f39a44e4-436b-432e-9296-c162f0b59139)
 Call ID: f39a44e4-436b-432e-9296-c162f0b59139
  Args:
    relation: :hasMother
    target: :PaulineAstor
    source: :RachelPaulineSpenderClay
  Finish (2d079af8-b739-49df-8668-a45789d13aee)
 Call ID: 2d079af8-b739-49df-8668-a45789d13aee
  Args: