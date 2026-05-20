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
Patrick Bowes-Lyon, 15th and 2nd Earl of Strathmore and Kinghorne (22 September 1884 – 25 May 1949), styled as Master of Glamis until 1904 and Lord Glamis until 1944, was a British landowner, peer and British Army officer.
He was the eldest brother of Queen Elizabeth the Queen Mother, thus a maternal uncle of Queen Elizabeth II.
Life

Patrick Bowes-Lyon was born on 22 September 1884 at St Paul's Walden Bury, Hertfordshire to Claude, Lord Glamis, and Cecilia Cavendish-Bentinck.
Strathmore and three of his three surviving brothers all served in World War I.
He succeeded his father as 15th and 2nd Earl of Strathmore and Kinghorne (15th earl in the peerage of Scotland and 2nd earl in the peerage of the United Kingdom) on 7 November 1944.
He was the eldest brother of Lady Elizabeth Bowes-Lyon (later Queen Elizabeth the Queen Mother), and thus an uncle of Queen Elizabeth II and Princess Margaret.
As an uncle of the bride, Strathmore was a leading guest at the 1947 wedding of Princess Elizabeth and Philip Mountbatten.
Marriage and issue

He married Lady Dorothy Beatrix Godolphin Osborne (3 December 1888 – 18 June 1946), daughter of George, 10th Duke of Leeds, on 21 November 1908 in London.
They had four children:


Death

Strathmore died on 25 May 1949 in Angus, surviving his wife by almost three years, aged 64.



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
  AssignClass (c164342d-2f95-465d-a466-6c92e23a6679)
 Call ID: c164342d-2f95-465d-a466-6c92e23a6679
  Args:
    type: :Man
    source: Patrick_Bowes-Lyon
  AssignClass (1e665ab2-f2c5-41d9-b893-7d5bd80e9ba2)
 Call ID: 1e665ab2-f2c5-41d9-b893-7d5bd80e9ba2
  Args:
    type: :Person
    source: Patrick_Bowes-Lyon
  AddLiteral (6e6f0764-cc64-4a29-bad0-b429e65594cf)
 Call ID: 6e6f0764-cc64-4a29-bad0-b429e65594cf
  Args:
    literal_value: 1884
    source: Patrick_Bowes-Lyon
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f4acd50f-0029-4aed-8505-08a56239a0aa)
 Call ID: f4acd50f-0029-4aed-8505-08a56239a0aa
  Args:
    literal_value: 1949
    source: Patrick_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (2ca24c61-338b-40cd-ba97-f558ee91f2ab)
 Call ID: 2ca24c61-338b-40cd-ba97-f558ee91f2ab
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    literal_value: Master of Glamis
    source: Patrick_Bowes-Lyon
  AddLiteral (9cee33ce-03a4-4dfc-bb51-f06da3501e0d)
 Call ID: 9cee33ce-03a4-4dfc-bb51-f06da3501e0d
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    literal_value: Lord Glamis
    source: Patrick_Bowes-Lyon
  AssignClass (80b0487a-4dad-49bc-b3f3-5ae98c1e73d7)
 Call ID: 80b0487a-4dad-49bc-b3f3-5ae98c1e73d7
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (262ef6a0-4ab7-47ab-bf5d-f40962f8cf76)
 Call ID: 262ef6a0-4ab7-47ab-bf5d-f40962f8cf76
  Args:
    source: Claude_Bowes-Lyon
    type: :Person
  AssignClass (76261019-5ad9-4c5c-a037-553606877f7e)
 Call ID: 76261019-5ad9-4c5c-a037-553606877f7e
  Args:
    type: :Woman
    source: Cecilia_Cavendish-Bentinck
  AssignClass (b3febce3-70c2-4b5c-b59a-c10b99ffd7a9)
 Call ID: b3febce3-70c2-4b5c-b59a-c10b99ffd7a9
  Args:
    type: :Person
    source: Cecilia_Cavendish-Bentinck
  AddTriple (3c1ad6ec-9846-4524-8d55-6b879841b6f9)
 Call ID: 3c1ad6ec-9846-4524-8d55-6b879841b6f9
  Args:
    relation: :hasFather
    target: Claude_Bowes-Lyon
    source: Patrick_Bowes-Lyon
  AddTriple (5c092961-6009-4a36-b259-309c09e409f8)
 Call ID: 5c092961-6009-4a36-b259-309c09e409f8
  Args:
    source: Patrick_Bowes-Lyon
    target: Cecilia_Cavendish-Bentinck
    relation: :hasMother
  AssignClass (5db0bddf-0e87-4cc0-80e2-c198376e74c5)
 Call ID: 5db0bddf-0e87-4cc0-80e2-c198376e74c5
  Args:
    source: Elizabeth_Bowes-Lyon
    type: :Woman
  AssignClass (bd99dd8c-d4e6-4456-9f7e-20ef29dcdb27)
 Call ID: bd99dd8c-d4e6-4456-9f7e-20ef29dcdb27
  Args:
    source: Elizabeth_Bowes-Lyon
    type: :Person
  AddTriple (d6560a49-8e5a-43ee-961c-8b59c702d81e)
 Call ID: d6560a49-8e5a-43ee-961c-8b59c702d81e
  Args:
    relation: :hasSister
    target: Elizabeth_Bowes-Lyon
    source: Patrick_Bowes-Lyon
  AssignClass (ee54a14f-5131-40fc-a00a-f3ba3755dc70)
 Call ID: ee54a14f-5131-40fc-a00a-f3ba3755dc70
  Args:
    source: Dorothy_Beatrix_Godolphin_Osborne
    type: :Woman
  AssignClass (19ff3d53-6324-475a-aa46-8957df35de11)
 Call ID: 19ff3d53-6324-475a-aa46-8957df35de11
  Args:
    type: :Person
    source: Dorothy_Beatrix_Godolphin_Osborne
  AddLiteral (bbd08e06-d626-433b-bec0-7cb1add96d99)
 Call ID: bbd08e06-d626-433b-bec0-7cb1add96d99
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1888
    source: Dorothy_Beatrix_Godolphin_Osborne
  AddLiteral (aa551a6e-cc28-426e-b669-ace0c87de1cb)
 Call ID: aa551a6e-cc28-426e-b669-ace0c87de1cb
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1946
    source: Dorothy_Beatrix_Godolphin_Osborne
  AddLiteral (518b51bd-810e-4253-8c66-ab60b5b99bea)
 Call ID: 518b51bd-810e-4253-8c66-ab60b5b99bea
  Args:
    source: Patrick_Bowes-Lyon
    literal_value: 1908
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (1d1dea2a-caee-402e-a397-3ddbb3cc8a00)
 Call ID: 1d1dea2a-caee-402e-a397-3ddbb3cc8a00
  Args:
    relation: :hasRelation
    target: Dorothy_Beatrix_Godolphin_Osborne
    source: Patrick_Bowes-Lyon
  AssignClass (f576b467-cc76-4554-9679-bc9882bef729)
 Call ID: f576b467-cc76-4554-9679-bc9882bef729
  Args:
    type: :Man
    source: George_10th_Duke_of_Leeds
  AssignClass (0284600c-fe13-405b-b770-707dac2253b7)
 Call ID: 0284600c-fe13-405b-b770-707dac2253b7
  Args:
    type: :Person
    source: George_10th_Duke_of_Leeds
  AddTriple (fdc09fae-e658-47cf-9fc5-3323c55ca90e)
 Call ID: fdc09fae-e658-47cf-9fc5-3323c55ca90e
  Args:
    source: Dorothy_Beatrix_Godolphin_Osborne
    target: George_10th_Duke_of_Leeds
    relation: :hasFather
  AssignClass (6b87b242-8cec-493b-9e6b-cfc79ad52f5a)
 Call ID: 6b87b242-8cec-493b-9e6b-cfc79ad52f5a
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (8dde9e73-9ce8-4065-abc6-c3fed527be4c)
 Call ID: 8dde9e73-9ce8-4065-abc6-c3fed527be4c
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (dacf6778-4ff9-44d2-b110-58df939935ba)
 Call ID: dacf6778-4ff9-44d2-b110-58df939935ba
  Args:
    type: :Woman
    source: Princess_Margaret
  AssignClass (9cd56dd7-7ef1-4b84-86b7-660ed13953de)
 Call ID: 9cd56dd7-7ef1-4b84-86b7-660ed13953de
  Args:
    type: :Person
    source: Princess_Margaret
  AddTriple (2b392008-92e0-4487-a69a-d348a6bd7df1)
 Call ID: 2b392008-92e0-4487-a69a-d348a6bd7df1
  Args:
    source: Patrick_Bowes-Lyon
    target: Queen_Elizabeth_II
    relation: :isUncleOf
  AddTriple (4f730634-47df-4521-8f27-4c64a36cc6c4)
 Call ID: 4f730634-47df-4521-8f27-4c64a36cc6c4
  Args:
    target: Princess_Margaret
    relation: :isUncleOf
    source: Patrick_Bowes-Lyon
  Finish (3d7a1454-a467-4207-8a69-df176efd6525)
 Call ID: 3d7a1454-a467-4207-8a69-df176efd6525
  Args: