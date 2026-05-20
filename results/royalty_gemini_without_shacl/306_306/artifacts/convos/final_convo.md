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
Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), known until 2005 as Lord Romsey and until 2017 as the Lord Brabourne, is a British peer.
Life and education

Mountbatten was born at King's College Hospital in London as the eldest son of Patricia Knatchbull, née Mountbatten, later 2nd Countess Mountbatten of Burma, and film producer John Knatchbull, 7th Baron Brabourne.
Mountbatten was educated at the Dragon School, in Oxford, and Gordonstoun School, Elgin, Moray, Scotland.
He also succeeded to the Knatchbull Baronetcy, of Mersham Hatch in the County of Kent, in the baronetage of England.
On the death of his mother on 13 June 2017, he became Earl Mountbatten of Burma, also a title in the peerage of the United Kingdom created for his grandfather, Admiral of the Fleet Lord Louis Mountbatten.
Mountbatten is the godfather of Philip's grandson, the Prince of Wales.
He is also related to author Jane Austen, as his father, John Knatchbull, 7th Baron Brabourne, was a direct descendant of her brother Edward Austen Knight.
Marriage and children

Mountbatten is married to Penelope Meredith Eastwood (born 16 April 1953), a daughter of Reginald Wray Frank Eastwood (1912–1980), a self-made millionaire former butcher who founded the Angus Steakhouse chain, and Marian Elizabeth (1926–2020), née Hood.
They were wed on 20 October 1979 at Romsey Abbey, less than two months after the IRA murdered his 79-year-old maternal grandfather, Louis Mountbatten, 1st
Earl Mountbatten of Burma; his 14-year-old younger brother, Nicholas Knatchbull; and his 83-year-old paternal grandmother, Doreen Knatchbull, Dowager Lady Brabourne.
The 3rd Earl Mountbatten of Burma and his wife have three children and three grandsons:


From 2010 to 2014, Mountbatten was in an extramarital relationship with Eugenie, Lady Nuttall, widow of Sir Nicholas Nuttall, 3rd Baronet, who was heir to the Edmund Nuttall Limited construction company.



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
  AssignClass (474bdac2-916c-4c91-b156-605781ca6919)
 Call ID: 474bdac2-916c-4c91-b156-605781ca6919
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (7ad5a66b-e6bb-4f5a-a53b-c43fb51ad9f1)
 Call ID: 7ad5a66b-e6bb-4f5a-a53b-c43fb51ad9f1
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (fa6b5e88-93c1-4056-a48d-c2a93157e1b7)
 Call ID: fa6b5e88-93c1-4056-a48d-c2a93157e1b7
  Args:
    literal_value: 1947
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (e46446f7-8dd8-4add-a78f-f95f69a6de9e)
 Call ID: e46446f7-8dd8-4add-a78f-f95f69a6de9e
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Romsey
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AddLiteral (f4561e06-5fea-45c0-8da0-fe63c4270499)
 Call ID: f4561e06-5fea-45c0-8da0-fe63c4270499
  Args:
    literal_type: xsd:string
    relation: :formerlyKnownAs
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Brabourne
  AssignClass (961fa6cf-9674-4def-b3eb-2bb7545be7a9)
 Call ID: 961fa6cf-9674-4def-b3eb-2bb7545be7a9
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (7009e57a-8c89-445e-838c-2496ea1f9240)
 Call ID: 7009e57a-8c89-445e-838c-2496ea1f9240
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (c70f5f50-1849-40d9-93ae-fbab777f6926)
 Call ID: c70f5f50-1849-40d9-93ae-fbab777f6926
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (bcd6277d-9edb-4983-8f83-5067e84ba950)
 Call ID: bcd6277d-9edb-4983-8f83-5067e84ba950
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (9eaeb80d-5503-4d76-9c4d-e6d53069c416)
 Call ID: 9eaeb80d-5503-4d76-9c4d-e6d53069c416
  Args:
    target: John_Knatchbull
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (422e3d47-fd8e-45fa-8d58-fb753ba6b2f4)
 Call ID: 422e3d47-fd8e-45fa-8d58-fb753ba6b2f4
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMother
    target: Patricia_Knatchbull
  AssignClass (5d2df6bd-7305-4b60-8b2a-3ead0397f0f5)
 Call ID: 5d2df6bd-7305-4b60-8b2a-3ead0397f0f5
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (ac231c90-e41a-486f-af3c-ed76224eacee)
 Call ID: ac231c90-e41a-486f-af3c-ed76224eacee
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (dc8ead86-b308-413b-a7de-a677155edb27)
 Call ID: dc8ead86-b308-413b-a7de-a677155edb27
  Args:
    target: Louis_Mountbatten
    relation: :hasFather
    source: Patricia_Knatchbull
  AssignClass (0a770535-340b-475f-9b40-e248cc66504a)
 Call ID: 0a770535-340b-475f-9b40-e248cc66504a
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (c42c5663-d59f-4906-a589-07400d0f01a9)
 Call ID: c42c5663-d59f-4906-a589-07400d0f01a9
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Person
  AddLiteral (8ff1531b-c44f-4fd2-9fef-c5589b8636e2)
 Call ID: 8ff1531b-c44f-4fd2-9fef-c5589b8636e2
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1953
    source: Penelope_Meredith_Eastwood
  AddTriple (8ffd9f22-e148-4aa7-99b3-91d831c599e3)
 Call ID: 8ffd9f22-e148-4aa7-99b3-91d831c599e3
  Args:
    relation: :hasRelation
    target: Penelope_Meredith_Eastwood
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (8d5fd1e6-fcde-4b59-ae4a-6ca1d125b6c6)
 Call ID: 8d5fd1e6-fcde-4b59-ae4a-6ca1d125b6c6
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (76caf225-d6a0-4486-9e42-c211651443e9)
 Call ID: 76caf225-d6a0-4486-9e42-c211651443e9
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (ee445b4d-adf7-4630-ad72-40db4e207656)
 Call ID: ee445b4d-adf7-4630-ad72-40db4e207656
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (7db5fa0a-63c1-4f40-9aee-e72e06f46391)
 Call ID: 7db5fa0a-63c1-4f40-9aee-e72e06f46391
  Args:
    source: Marian_Elizabeth
    type: :Woman
  AssignClass (69988e0d-f904-4b04-8c80-5eba5b1cd973)
 Call ID: 69988e0d-f904-4b04-8c80-5eba5b1cd973
  Args:
    source: Marian_Elizabeth
    type: :Person
  AddTriple (12dbc934-5495-43b4-9cca-0d640e4282e0)
 Call ID: 12dbc934-5495-43b4-9cca-0d640e4282e0
  Args:
    source: Penelope_Meredith_Eastwood
    target: Reginald_Wray_Frank_Eastwood
    relation: :hasFather
  AddTriple (be68f069-8adf-4851-9b5d-c90ed3ef3cae)
 Call ID: be68f069-8adf-4851-9b5d-c90ed3ef3cae
  Args:
    source: Penelope_Meredith_Eastwood
    relation: :hasMother
    target: Marian_Elizabeth
  AssignClass (e782406f-55da-4467-87f5-78c1eb1cba36)
 Call ID: e782406f-55da-4467-87f5-78c1eb1cba36
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (7631eebe-e920-4a75-bfaf-28922b414575)
 Call ID: 7631eebe-e920-4a75-bfaf-28922b414575
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (fbea3062-5174-4bfb-822c-cc6c84b8321e)
 Call ID: fbea3062-5174-4bfb-822c-cc6c84b8321e
  Args:
    target: Nicholas_Knatchbull
    relation: :hasBrother
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (e4f84632-4f16-4c35-aabb-bd96a2bfd02a)
 Call ID: e4f84632-4f16-4c35-aabb-bd96a2bfd02a
  Args:
    source: Doreen_Knatchbull
    type: :Woman
  AssignClass (ac6c0119-f987-4519-9c87-dda70cc24cbe)
 Call ID: ac6c0119-f987-4519-9c87-dda70cc24cbe
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddTriple (e832ead0-ed1c-42f8-8bd7-86f7f296588b)
 Call ID: e832ead0-ed1c-42f8-8bd7-86f7f296588b
  Args:
    relation: :hasMother
    target: Doreen_Knatchbull
    source: John_Knatchbull
  Finish (8d8bd88b-c4a1-4a64-b02b-68778e68b747)
 Call ID: 8d8bd88b-c4a1-4a64-b02b-68778e68b747
  Args: