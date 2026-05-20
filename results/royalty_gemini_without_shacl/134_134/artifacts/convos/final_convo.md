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
Princess Herzeleide Ina-Marie Sophie Charlotte Else of Prussia (25 December 1918 – 22 March 1989) was a member of the deposed House of Hohenzollern.
She was the only daughter of Prince Oskar of Prussia (the second youngest son of Emperor Wilhelm II) and his initially morganatic wife, Countess Ina Marie von Bassewitz.
She is the mother of Ernst-Johann Biron, Prince of Courland, the current head of the House of Biron.
Biography

Family and early life

Countess Herzeleide-Ina-Marie von Ruppin was born in Bristow, Mecklenburg, on 25 December 1918, shortly after the defeat of the German Empire and the collapse of the monarchy.
She was consequently given the name Herzeleide, meaning "heart's sorrow".
She had three brothers: Oscar, Burchard, and Wilhelm-Karl.
Herzeleide and her brothers became Princess/Prince of Prussia on 21 June 1920 when their parents' morganatic marriage was recognised as dynastic by the deposed Emperor Wilhelm II.
In early 1938, Herzeleide was one of three bridesmaids at the wedding of the future King Paul of Greece to Frederica of Hanover, her first cousin.
Marriage and issue

On 15 August 1938 in Potsdam Garrison Church, Herzeleide married Prince Karl Biron von Courland (15 June 1907 – 28 February 1982).
Karl was the eldest son and heir of Prince Gustav Biron of Courland and Françoise Lévisse de Montigny, daughter of Marquis de Jaucourt.
Along with the bride and groom's parents, in attendance were the former German Crown Prince Wilhelm and Emperor Wilhelm's consort, Empress Hermine.
All male guests wore uniforms of the former German army.
The couple's honeymoon plans included a visit to Doorn to pay respects to Emperor Wilhelm in exile, the bride's paternal grandfather.



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
  AssignClass (292e2763-c35b-47f8-bc4b-cd993fe28374)
 Call ID: 292e2763-c35b-47f8-bc4b-cd993fe28374
  Args:
    source: Herzeleide_of_Prussia
    type: :Woman
  AssignClass (4ddcca47-747a-4d98-80c7-d693e0085c5e)
 Call ID: 4ddcca47-747a-4d98-80c7-d693e0085c5e
  Args:
    type: :Person
    source: Herzeleide_of_Prussia
  AddLiteral (96eb8b61-1337-4162-8f0a-49233cf0aaed)
 Call ID: 96eb8b61-1337-4162-8f0a-49233cf0aaed
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1918
    source: Herzeleide_of_Prussia
  AddLiteral (f5750278-d16f-4197-a5fa-bab6ac01b665)
 Call ID: f5750278-d16f-4197-a5fa-bab6ac01b665
  Args:
    literal_type: xsd:integer
    source: Herzeleide_of_Prussia
    literal_value: 1989
    relation: :hasDeathYear
  AssignClass (d1dbe3eb-7f1a-469e-931f-3e1f92b94e11)
 Call ID: d1dbe3eb-7f1a-469e-931f-3e1f92b94e11
  Args:
    type: :Man
    source: Oskar_of_Prussia
  AssignClass (6d135b24-4af4-44d4-a705-8ff46107be03)
 Call ID: 6d135b24-4af4-44d4-a705-8ff46107be03
  Args:
    source: Oskar_of_Prussia
    type: :Ancestor
  AssignClass (6492c2e2-1e29-466f-bb69-42e3cdeb070d)
 Call ID: 6492c2e2-1e29-466f-bb69-42e3cdeb070d
  Args:
    type: :Person
    source: Oskar_of_Prussia
  AddTriple (0b61f204-25eb-4f8f-a802-a551747cf71c)
 Call ID: 0b61f204-25eb-4f8f-a802-a551747cf71c
  Args:
    source: Herzeleide_of_Prussia
    relation: :hasFather
    target: Oskar_of_Prussia
  AssignClass (9fb67ba3-84a2-4f59-bd8a-60982a7d7434)
 Call ID: 9fb67ba3-84a2-4f59-bd8a-60982a7d7434
  Args:
    type: :Woman
    source: Ina_Marie_von_Bassewitz
  AssignClass (cd941e2c-a9b1-491c-a4ae-43b494b27384)
 Call ID: cd941e2c-a9b1-491c-a4ae-43b494b27384
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Ancestor
  AssignClass (524ef760-c1fc-4acd-abd4-be4ca5b99abb)
 Call ID: 524ef760-c1fc-4acd-abd4-be4ca5b99abb
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Person
  AddTriple (57552f31-92f6-42d6-9362-2f9fddfb7052)
 Call ID: 57552f31-92f6-42d6-9362-2f9fddfb7052
  Args:
    relation: :hasMother
    target: Ina_Marie_von_Bassewitz
    source: Herzeleide_of_Prussia
  AssignClass (d43d38f2-b734-4510-90dc-3bc88f96b6ad)
 Call ID: d43d38f2-b734-4510-90dc-3bc88f96b6ad
  Args:
    type: :Man
    source: Ernst-Johann_Biron
  AssignClass (29eb8432-3296-42f3-84ea-bfdc8ff7c0e5)
 Call ID: 29eb8432-3296-42f3-84ea-bfdc8ff7c0e5
  Args:
    source: Ernst-Johann_Biron
    type: :Person
  AddTriple (3cdbe62e-ed8e-4112-97f1-9e191d8be436)
 Call ID: 3cdbe62e-ed8e-4112-97f1-9e191d8be436
  Args:
    source: Herzeleide_of_Prussia
    relation: :isMotherOf
    target: Ernst-Johann_Biron
  AssignClass (a8351a11-6bfa-41ab-ae83-3d98ead10d86)
 Call ID: a8351a11-6bfa-41ab-ae83-3d98ead10d86
  Args:
    type: :Man
    source: Oscar_brother
  AssignClass (23e1afd4-991e-416b-a986-320ea67aaf47)
 Call ID: 23e1afd4-991e-416b-a986-320ea67aaf47
  Args:
    type: :Person
    source: Oscar_brother
  AddTriple (ac67bd56-5660-4fd1-9f10-fa80dfca8c10)
 Call ID: ac67bd56-5660-4fd1-9f10-fa80dfca8c10
  Args:
    relation: :hasBrother
    target: Oscar_brother
    source: Herzeleide_of_Prussia
  AssignClass (014c69e8-5615-480f-800e-9cf7badfed7e)
 Call ID: 014c69e8-5615-480f-800e-9cf7badfed7e
  Args:
    type: :Man
    source: Burchard
  AssignClass (e8110310-3915-4390-ac01-8d7c943efa27)
 Call ID: e8110310-3915-4390-ac01-8d7c943efa27
  Args:
    source: Burchard
    type: :Person
  AddTriple (200882ab-a0aa-433d-a2b0-c95e63062daa)
 Call ID: 200882ab-a0aa-433d-a2b0-c95e63062daa
  Args:
    source: Herzeleide_of_Prussia
    relation: :hasBrother
    target: Burchard
  AssignClass (72cd0f8b-ff13-42bb-a2c7-a1ce8a88b758)
 Call ID: 72cd0f8b-ff13-42bb-a2c7-a1ce8a88b758
  Args:
    type: :Man
    source: Wilhelm-Karl
  AssignClass (514ad4fc-a3b6-4f84-9e74-588a039081d2)
 Call ID: 514ad4fc-a3b6-4f84-9e74-588a039081d2
  Args:
    source: Wilhelm-Karl
    type: :Person
  AddTriple (14469035-0747-4c3c-9b2d-a861caadd678)
 Call ID: 14469035-0747-4c3c-9b2d-a861caadd678
  Args:
    source: Herzeleide_of_Prussia
    relation: :hasBrother
    target: Wilhelm-Karl
  AssignClass (b09999a5-9fa2-42f3-a0af-23c28938c72c)
 Call ID: b09999a5-9fa2-42f3-a0af-23c28938c72c
  Args:
    source: Karl_Biron_von_Courland
    type: :Man
  AssignClass (f73d2b60-af18-45f4-a9b8-c1fc3997331a)
 Call ID: f73d2b60-af18-45f4-a9b8-c1fc3997331a
  Args:
    type: :Person
    source: Karl_Biron_von_Courland
  AddLiteral (8becd6a8-b6a3-4ff2-8cdb-dcbaf3545b45)
 Call ID: 8becd6a8-b6a3-4ff2-8cdb-dcbaf3545b45
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
  AddTriple (993c27c8-f2bc-4a40-84da-985ee2dbbe3c)
 Call ID: 993c27c8-f2bc-4a40-84da-985ee2dbbe3c
  Args:
    source: Herzeleide_of_Prussia
    relation: :hasRelation
    target: Karl_Biron_von_Courland
  AssignClass (fdac4b1d-2c61-44dd-87a8-a1af179a3f07)
 Call ID: fdac4b1d-2c61-44dd-87a8-a1af179a3f07
  Args:
    type: :Man
    source: Gustav_Biron_of_Courland
  AssignClass (5376201a-cc5d-4aa8-9d94-1c1a36b5fa97)
 Call ID: 5376201a-cc5d-4aa8-9d94-1c1a36b5fa97
  Args:
    type: :Ancestor
    source: Gustav_Biron_of_Courland
  AssignClass (bc67e563-2d13-48a7-a0e2-69d06f735886)
 Call ID: bc67e563-2d13-48a7-a0e2-69d06f735886
  Args:
    type: :Person
    source: Gustav_Biron_of_Courland
  AddTriple (061b4cd1-36f8-432b-a364-086fb5ed267a)
 Call ID: 061b4cd1-36f8-432b-a364-086fb5ed267a
  Args:
    source: Karl_Biron_von_Courland
    target: Gustav_Biron_of_Courland
    relation: :hasFather
  AssignClass (3ea9403d-37ce-4ad7-b164-e577e7e33fb8)
 Call ID: 3ea9403d-37ce-4ad7-b164-e577e7e33fb8
  Args:
    type: :Woman
    source: Francoise_Levisse_de_Montigny
  AssignClass (d18815e0-d6c4-42c3-a1f9-9d5d8a8118e8)
 Call ID: d18815e0-d6c4-42c3-a1f9-9d5d8a8118e8
  Args:
    type: :Ancestor
    source: Francoise_Levisse_de_Montigny
  AssignClass (fc3d7579-f683-4ecb-b563-2739f56bb775)
 Call ID: fc3d7579-f683-4ecb-b563-2739f56bb775
  Args:
    type: :Person
    source: Francoise_Levisse_de_Montigny
  AddTriple (9177f64e-7c0d-4e06-9dfa-d91910d3ae67)
 Call ID: 9177f64e-7c0d-4e06-9dfa-d91910d3ae67
  Args:
    source: Karl_Biron_von_Courland
    target: Francoise_Levisse_de_Montigny
    relation: :hasMother
  AssignClass (8682a7f0-bcfc-4770-9ec6-d7fd14ead9c0)
 Call ID: 8682a7f0-bcfc-4770-9ec6-d7fd14ead9c0
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (0227ec4b-6e7a-4bcb-b49b-d4f269288239)
 Call ID: 0227ec4b-6e7a-4bcb-b49b-d4f269288239
  Args:
    type: :Ancestor
    source: Wilhelm_II
  AssignClass (338ad53f-29ae-4330-9381-10f2f87a9283)
 Call ID: 338ad53f-29ae-4330-9381-10f2f87a9283
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (fa78ead6-0bb4-40a6-a782-8ccbaf98e276)
 Call ID: fa78ead6-0bb4-40a6-a782-8ccbaf98e276
  Args:
    source: Oskar_of_Prussia
    target: Wilhelm_II
    relation: :hasFather
  Finish (38995ec0-e59d-4d4c-a66a-f66133cd7a96)
 Call ID: 38995ec0-e59d-4d4c-a66a-f66133cd7a96
  Args: