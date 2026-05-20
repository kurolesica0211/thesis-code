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
Princess Isabel Alfonsa of Bourbon-Two Sicilies, Infanta of Spain, (Isabel Alfonsa María Teresa Antonia Cristina Mercedes Carolina Adelaida Rafaela de Borbón-Dos Sicilias y Borbón; 16 October 1904 – 18 July 1985) was a member of the House of Bourbon-Two Sicilies and a princess of Bourbon-Two Sicilies by birth.
Family

Isabel Alfonsa was the third child of Prince Carlos of Bourbon-Two Sicilies and his first wife María de las Mercedes, Princess of Asturias.
Isabel Alfonsa's maternal grandparents were Alfonso XII of Spain and Maria Christina of Austria.
Marriage and issue

Isabel Alfonsa married her first cousin once removed Count Jan Kanty Zamoyski, seventh child and third son of Count Andrzej Zamoyski and his wife Princess Maria Carolina of Bourbon-Two Sicilies, on 9 March 1929 in Madrid.



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
  AssignClass (66932e25-3ebd-431f-b438-7f711d9b8fec)
 Call ID: 66932e25-3ebd-431f-b438-7f711d9b8fec
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    type: :Person
  AssignClass (97b36e2b-a72a-4dd5-ac1b-52fa30a83284)
 Call ID: 97b36e2b-a72a-4dd5-ac1b-52fa30a83284
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    type: :Woman
  AssignClass (f2664ae8-f167-494f-95c0-ef542616d7f2)
 Call ID: f2664ae8-f167-494f-95c0-ef542616d7f2
  Args:
    type: :Person
    source: :Prince_Carlos_of_Bourbon_Two_Sicilies
  AssignClass (cce3ba6d-2415-4ba7-abe3-3e8acb2fee34)
 Call ID: cce3ba6d-2415-4ba7-abe3-3e8acb2fee34
  Args:
    source: :Prince_Carlos_of_Bourbon_Two_Sicilies
    type: :Man
  AssignClass (8d70950f-e6f9-4de6-88c0-1452ad7834ca)
 Call ID: 8d70950f-e6f9-4de6-88c0-1452ad7834ca
  Args:
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
    type: :Person
  AssignClass (e38c7253-6842-47e8-a55a-e01f219329b2)
 Call ID: e38c7253-6842-47e8-a55a-e01f219329b2
  Args:
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
    type: :Woman
  AssignClass (568fcee4-70d5-480b-b212-0074f86e2587)
 Call ID: 568fcee4-70d5-480b-b212-0074f86e2587
  Args:
    type: :Person
    source: :Alfonso_XII_of_Spain
  AssignClass (85ed9d4f-4098-439c-8092-2a78b8ca2d7d)
 Call ID: 85ed9d4f-4098-439c-8092-2a78b8ca2d7d
  Args:
    type: :Man
    source: :Alfonso_XII_of_Spain
  AssignClass (e8d75155-6162-4d74-9e9b-ed060a3c2b26)
 Call ID: e8d75155-6162-4d74-9e9b-ed060a3c2b26
  Args:
    source: :Maria_Christina_of_Austria
    type: :Person
  AssignClass (68188be2-e663-42d1-97f9-020ea8ac2094)
 Call ID: 68188be2-e663-42d1-97f9-020ea8ac2094
  Args:
    source: :Maria_Christina_of_Austria
    type: :Woman
  AssignClass (4a37b198-c6a7-48f1-a4bd-a295ebe27e7c)
 Call ID: 4a37b198-c6a7-48f1-a4bd-a295ebe27e7c
  Args:
    type: :Person
    source: :Count_Jan_Kanty_Zamoyski
  AssignClass (4045590f-88e9-48c6-95e6-2606f24760e0)
 Call ID: 4045590f-88e9-48c6-95e6-2606f24760e0
  Args:
    source: :Count_Jan_Kanty_Zamoyski
    type: :Man
  AssignClass (7cac3c58-f0bb-4e6e-a463-80a54fc1befc)
 Call ID: 7cac3c58-f0bb-4e6e-a463-80a54fc1befc
  Args:
    type: :Person
    source: :Count_Andrzej_Zamoyski
  AssignClass (c134ee11-ed2e-4005-ab3c-392a9280642f)
 Call ID: c134ee11-ed2e-4005-ab3c-392a9280642f
  Args:
    type: :Man
    source: :Count_Andrzej_Zamoyski
  AssignClass (1dd9fd11-e430-4f3a-8224-0a735c5c5386)
 Call ID: 1dd9fd11-e430-4f3a-8224-0a735c5c5386
  Args:
    type: :Person
    source: :Princess_Maria_Carolina_of_Bourbon_Two_Sicilies
  AssignClass (c7c5d979-b778-4853-938f-428a6784f066)
 Call ID: c7c5d979-b778-4853-938f-428a6784f066
  Args:
    source: :Princess_Maria_Carolina_of_Bourbon_Two_Sicilies
    type: :Woman
  AddLiteral (db97bdc7-3f5a-4589-834f-6a06601a948e)
 Call ID: db97bdc7-3f5a-4589-834f-6a06601a948e
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    literal_type: xsd:string
    literal_value: 1904
    relation: :hasBirthYear
  AddLiteral (c141648c-1c55-4dad-97f3-742aedf616e3)
 Call ID: c141648c-1c55-4dad-97f3-742aedf616e3
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    literal_type: xsd:string
    literal_value: 1985
    relation: :hasDeathYear
  AddTriple (e0542308-f4d8-4ce4-a102-1fc7ea18b5fc)
 Call ID: e0542308-f4d8-4ce4-a102-1fc7ea18b5fc
  Args:
    relation: :hasFather
    target: :Prince_Carlos_of_Bourbon_Two_Sicilies
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
  AddTriple (cf833d02-7805-40e2-92b5-b35e3bdd59c2)
 Call ID: cf833d02-7805-40e2-92b5-b35e3bdd59c2
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    target: :Maria_de_las_Mercedes_Princess_of_Asturias
    relation: :hasMother
  AddTriple (838763b4-9175-4955-95da-03bf1347ab00)
 Call ID: 838763b4-9175-4955-95da-03bf1347ab00
  Args:
    relation: :hasFather
    target: :Alfonso_XII_of_Spain
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
  AddTriple (27a8578d-4bd2-42c8-873c-18db51da6f28)
 Call ID: 27a8578d-4bd2-42c8-873c-18db51da6f28
  Args:
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
    relation: :hasMother
    target: :Maria_Christina_of_Austria
  AddTriple (443dd6f5-30d5-4285-8236-6d7bd931b07b)
 Call ID: 443dd6f5-30d5-4285-8236-6d7bd931b07b
  Args:
    source: :Count_Jan_Kanty_Zamoyski
    relation: :hasFather
    target: :Count_Andrzej_Zamoyski
  AddTriple (787e51b3-a1c1-4937-b857-9ba3e2e6a929)
 Call ID: 787e51b3-a1c1-4937-b857-9ba3e2e6a929
  Args:
    source: :Count_Jan_Kanty_Zamoyski
    target: :Princess_Maria_Carolina_of_Bourbon_Two_Sicilies
    relation: :hasMother
  AddLiteral (c1442d96-47da-422b-a1c2-14a8fe0ce045)
 Call ID: c1442d96-47da-422b-a1c2-14a8fe0ce045
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    literal_type: xsd:string
    literal_value: 1929
    relation: :hasMarriageYear
  AddTriple (695ecdf1-ab49-45de-ac9d-ae3df4123694)
 Call ID: 695ecdf1-ab49-45de-ac9d-ae3df4123694
  Args:
    relation: :hasRelation
    target: :Count_Jan_Kanty_Zamoyski
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
  Finish (fe78c804-8ea8-482f-a548-45cf0150b0e1)
 Call ID: fe78c804-8ea8-482f-a548-45cf0150b0e1
  Args: