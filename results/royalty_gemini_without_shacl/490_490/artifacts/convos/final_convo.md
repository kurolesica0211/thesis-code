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
Philipp, Prince of Hohenlohe-Langenburg (Philipp Gottfried Alexander; born 20 January 1970), is the head of the House of Hohenlohe-Langenburg, since the death of his father in 2004.
Early life and ancestry

He was born in Crailsheim, West Germany, the middle child and only son of Kraft, Prince of Hohenlohe-Langenburg (1935–2004) and his first wife, Princess Charlotte of Croÿ (b. 1938).
Paternally, he is a grandson of Princess Margarita of Greece and Denmark, and a grandnephew of Prince Philip, Duke of Edinburgh, whose funeral he attended.
Anne, Princess Royal is one of his godmothers.
Maternally, he is the grandson of Prince Alexander of Croy (1912–2002) and his Scottish wife, Anna Elspeth Campbell (1917–1986), granddaughter of Archibald Campbell, 6th of Glendaruel.
He sought public support from (then) Charles, Prince of Wales, the current King Charles III, and from former vice chancellor and foreign minister Joschka Fischer of the Green Party, who both attended a conference at Langenburg Castle in 2013.
Together with Fischer he founded the Langenburg Forum for Sustainability which cooperates with Charles' International Sustainability Unit


Langenburg castle is partially open to the public, including the state rooms and a museum of classic cars.
Marriage and issue

He married Saskia Binder (b. 15 January 1973 in Munich), daughter of former Deutsche Bank Munich director Hans Peter Binder, on 6 September 2003 in a civil ceremony at Langenburg.



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
  AssignClass (f173d63a-fe6f-4210-a8ca-19a373f792b7)
 Call ID: f173d63a-fe6f-4210-a8ca-19a373f792b7
  Args:
    type: :Man
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AssignClass (a1805021-037c-42f4-9aa5-b8bc49914fa2)
 Call ID: a1805021-037c-42f4-9aa5-b8bc49914fa2
  Args:
    type: :Person
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AssignClass (2fceeafa-cebf-45f1-8b5d-a8cbf2b35403)
 Call ID: 2fceeafa-cebf-45f1-8b5d-a8cbf2b35403
  Args:
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (f40863ab-3d75-4fb0-9659-4ae213ed56c5)
 Call ID: f40863ab-3d75-4fb0-9659-4ae213ed56c5
  Args:
    type: :Person
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AssignClass (2463c2bc-6bc5-418c-95ac-aab8b3588d51)
 Call ID: 2463c2bc-6bc5-418c-95ac-aab8b3588d51
  Args:
    source: Princess_Charlotte_of_Croy
    type: :Woman
  AssignClass (39170764-00ab-4c59-a09f-62679f6b4680)
 Call ID: 39170764-00ab-4c59-a09f-62679f6b4680
  Args:
    source: Princess_Charlotte_of_Croy
    type: :Person
  AssignClass (fea62e86-24a5-48b3-a61f-6dd937541e3b)
 Call ID: fea62e86-24a5-48b3-a61f-6dd937541e3b
  Args:
    type: :Woman
    source: Saskia_Binder
  AssignClass (2afcf932-df16-4e77-b3db-72edd658015c)
 Call ID: 2afcf932-df16-4e77-b3db-72edd658015c
  Args:
    type: :Person
    source: Saskia_Binder
  AddTriple (9b97b168-3fc4-4c14-a613-52d044db8ea6)
 Call ID: 9b97b168-3fc4-4c14-a613-52d044db8ea6
  Args:
    relation: :hasFather
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Kraft_Prince_of_Hohenlohe-Langenburg
  AddTriple (080ad7d8-e743-4797-bd39-19ecd4c7c412)
 Call ID: 080ad7d8-e743-4797-bd39-19ecd4c7c412
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    relation: :hasMother
    target: Princess_Charlotte_of_Croy
  AddLiteral (36c1a361-b86b-4eff-9586-296d654a9576)
 Call ID: 36c1a361-b86b-4eff-9586-296d654a9576
  Args:
    relation: :hasBirthYear
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_type: xsd:integer
    literal_value: 1970
  AddLiteral (e16570d1-f0a3-414c-9e0b-0190c97a9b14)
 Call ID: e16570d1-f0a3-414c-9e0b-0190c97a9b14
  Args:
    literal_type: xsd:integer
    literal_value: 1935
    relation: :hasBirthYear
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AddLiteral (23c50b4c-efff-4592-90f4-1e5fbcc19338)
 Call ID: 23c50b4c-efff-4592-90f4-1e5fbcc19338
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasDeathYear
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AddLiteral (d6a32ee7-2ebc-40a8-9c53-9d071a6c06bc)
 Call ID: d6a32ee7-2ebc-40a8-9c53-9d071a6c06bc
  Args:
    literal_value: 1938
    literal_type: xsd:integer
    source: Princess_Charlotte_of_Croy
    relation: :hasBirthYear
  AddLiteral (6cb19f4d-d36d-40c4-b4cf-44b4310b6f3f)
 Call ID: 6cb19f4d-d36d-40c4-b4cf-44b4310b6f3f
  Args:
    relation: :hasBirthYear
    source: Saskia_Binder
    literal_type: xsd:integer
    literal_value: 1973
  AddLiteral (b61b7070-23ba-40f4-b33b-da88505f6220)
 Call ID: b61b7070-23ba-40f4-b33b-da88505f6220
  Args:
    relation: :hasMarriageYear
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_type: xsd:integer
    literal_value: 2003
  AddTriple (2a6de782-14d0-4e15-9ffe-56c8616c9ca5)
 Call ID: 2a6de782-14d0-4e15-9ffe-56c8616c9ca5
  Args:
    relation: :hasRelation
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Saskia_Binder
  Finish (6072502b-e128-482c-b756-11f23cab7197)
 Call ID: 6072502b-e128-482c-b756-11f23cab7197
  Args: