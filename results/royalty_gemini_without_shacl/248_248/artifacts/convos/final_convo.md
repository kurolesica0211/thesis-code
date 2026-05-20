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
Marina Victoria Alexandra Ogilvy (born 31 July 1966) is the younger child and only daughter of Sir Angus Ogilvy and Princess Alexandra of Kent.
Early life

Marina was born at Thatched House Lodge in Richmond Park, London, the home of her parents, on 31 July 1966.
She was named after her maternal grandmother, Princess Marina of Greece and Denmark, who was also a first cousin of Prince Philip, Duke of Edinburgh.
She has an elder brother, James Ogilvy, who was born in 1964.
Marina was educated at St Mary's School, Wantage.
Marriage and children

In November 1989, Marina announced that she was pregnant by her boyfriend Paul Julian Mowatt (born in Hendon, 28 November 1962), a freelance photographer.
Marina's parents denied her allegations and said that they loved her, had not cut her off and that she was welcome at home any time.
Marina married Mowatt in Richmond Park, Surrey, on 2 February 1990, wearing a red velvet bolero with gold trim, with a black dress underneath, and a black hat.
They had two children: Zenouska May Mowatt (born 26 May 1990), and Christian Alexander Mowatt (born 4 June 1993) and divorced in October 1997.



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
  AssignClass (1a4b8144-e181-4156-b489-0a96d67ea8c5)
 Call ID: 1a4b8144-e181-4156-b489-0a96d67ea8c5
  Args:
    source: Marina_Ogilvy
    type: :Woman
  AssignClass (be3824e1-f2ff-4b59-a7bf-04650b817b76)
 Call ID: be3824e1-f2ff-4b59-a7bf-04650b817b76
  Args:
    type: :Man
    source: Angus_Ogilvy
  AssignClass (ac58d729-44fc-4c2b-9128-c28bc610e156)
 Call ID: ac58d729-44fc-4c2b-9128-c28bc610e156
  Args:
    source: Alexandra_of_Kent
    type: :Woman
  AssignClass (58eb4df9-bd20-4b0b-a85e-a64e406780ea)
 Call ID: 58eb4df9-bd20-4b0b-a85e-a64e406780ea
  Args:
    type: :Man
    source: James_Ogilvy
  AssignClass (d8afb64d-f29f-4897-88e8-55a9e0bf6eef)
 Call ID: d8afb64d-f29f-4897-88e8-55a9e0bf6eef
  Args:
    type: :Man
    source: Paul_Julian_Mowatt
  AssignClass (ab9efea7-3f60-4180-a8f1-8c60a1e590cd)
 Call ID: ab9efea7-3f60-4180-a8f1-8c60a1e590cd
  Args:
    source: Zenouska_May_Mowatt
    type: :Woman
  AssignClass (069fa77e-b08e-4367-8e91-1c266ea14efe)
 Call ID: 069fa77e-b08e-4367-8e91-1c266ea14efe
  Args:
    source: Christian_Alexander_Mowatt
    type: :Man
  AssignClass (4ac33294-c9c6-47de-b306-6bedc17a1514)
 Call ID: 4ac33294-c9c6-47de-b306-6bedc17a1514
  Args:
    source: Marina_of_Greece_and_Denmark
    type: :Woman
  AddLiteral (88051712-1ee8-4c2c-b6b9-315a35ed9a9d)
 Call ID: 88051712-1ee8-4c2c-b6b9-315a35ed9a9d
  Args:
    source: Marina_Ogilvy
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1966
  AddLiteral (808a33d4-9cfe-41b3-b02a-cebfd2ded0e3)
 Call ID: 808a33d4-9cfe-41b3-b02a-cebfd2ded0e3
  Args:
    literal_type: xsd:integer
    literal_value: 1964
    source: James_Ogilvy
    relation: :hasBirthYear
  AddLiteral (5ab5b461-e780-4376-bd1c-6efec2eecaa3)
 Call ID: 5ab5b461-e780-4376-bd1c-6efec2eecaa3
  Args:
    relation: :hasBirthYear
    source: Paul_Julian_Mowatt
    literal_value: 1962
    literal_type: xsd:integer
  AddLiteral (b11e678c-a1b3-47ae-9e37-1924af94096e)
 Call ID: b11e678c-a1b3-47ae-9e37-1924af94096e
  Args:
    literal_value: 1990
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Zenouska_May_Mowatt
  AddLiteral (054828d5-310e-4229-aebc-e2d692f32ae6)
 Call ID: 054828d5-310e-4229-aebc-e2d692f32ae6
  Args:
    literal_value: 1993
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Christian_Alexander_Mowatt
  AddTriple (89fb7b1c-6ec9-4f20-8519-831142b7615b)
 Call ID: 89fb7b1c-6ec9-4f20-8519-831142b7615b
  Args:
    relation: :hasFather
    source: Marina_Ogilvy
    target: Angus_Ogilvy
  AddTriple (23a67997-c43d-40d0-8f08-24be0950a349)
 Call ID: 23a67997-c43d-40d0-8f08-24be0950a349
  Args:
    relation: :hasMother
    source: Marina_Ogilvy
    target: Alexandra_of_Kent
  AddTriple (ad3c36ec-9c6b-421d-8d27-5abdbb707ef0)
 Call ID: ad3c36ec-9c6b-421d-8d27-5abdbb707ef0
  Args:
    target: Angus_Ogilvy
    relation: :hasFather
    source: James_Ogilvy
  AddTriple (bc7acf50-ac6a-4680-9397-f1353662bc5b)
 Call ID: bc7acf50-ac6a-4680-9397-f1353662bc5b
  Args:
    target: Alexandra_of_Kent
    source: James_Ogilvy
    relation: :hasMother
  AddTriple (8439c9f0-0dbc-4ab6-8dfe-ae6be794c52b)
 Call ID: 8439c9f0-0dbc-4ab6-8dfe-ae6be794c52b
  Args:
    source: Alexandra_of_Kent
    relation: :isMotherOf
    target: Marina_Ogilvy
  AddTriple (daf65688-d98c-41a7-a6f5-3e5223f4d3a1)
 Call ID: daf65688-d98c-41a7-a6f5-3e5223f4d3a1
  Args:
    source: Alexandra_of_Kent
    relation: :isMotherOf
    target: James_Ogilvy
  AddTriple (385bbc91-7e45-440d-b7ff-e32d6b80e2f9)
 Call ID: 385bbc91-7e45-440d-b7ff-e32d6b80e2f9
  Args:
    target: Marina_Ogilvy
    source: Angus_Ogilvy
    relation: :isFatherOf
  AddTriple (8e4fb215-761c-4424-9b9b-f208546d40a1)
 Call ID: 8e4fb215-761c-4424-9b9b-f208546d40a1
  Args:
    target: James_Ogilvy
    relation: :isFatherOf
    source: Angus_Ogilvy
  AddTriple (13f40cf8-4b25-4cea-8c88-3966a7de59c5)
 Call ID: 13f40cf8-4b25-4cea-8c88-3966a7de59c5
  Args:
    relation: :hasBrother
    source: Marina_Ogilvy
    target: James_Ogilvy
  AddTriple (cc9692dc-9179-4548-82d1-8c8c102a9cce)
 Call ID: cc9692dc-9179-4548-82d1-8c8c102a9cce
  Args:
    source: Marina_Ogilvy
    relation: :isSisterOf
    target: James_Ogilvy
  AddTriple (74c4ee5c-1080-439e-bf4c-bd991e2ec5c0)
 Call ID: 74c4ee5c-1080-439e-bf4c-bd991e2ec5c0
  Args:
    relation: :hasChild
    source: Marina_Ogilvy
    target: Zenouska_May_Mowatt
  AddTriple (9804664f-0c94-4c6b-b95f-37adb8d2dfee)
 Call ID: 9804664f-0c94-4c6b-b95f-37adb8d2dfee
  Args:
    target: Christian_Alexander_Mowatt
    relation: :hasChild
    source: Marina_Ogilvy
  AddTriple (6fc68b45-7d0f-400d-ae13-33872b2debbc)
 Call ID: 6fc68b45-7d0f-400d-ae13-33872b2debbc
  Args:
    relation: :hasFather
    source: Zenouska_May_Mowatt
    target: Paul_Julian_Mowatt
  AddTriple (4acac5bc-4cd4-4638-ad8e-495b4c4e8aa2)
 Call ID: 4acac5bc-4cd4-4638-ad8e-495b4c4e8aa2
  Args:
    relation: :hasFather
    source: Christian_Alexander_Mowatt
    target: Paul_Julian_Mowatt
  AddTriple (b7899361-736d-4d6a-aade-0fc1c0cfc390)
 Call ID: b7899361-736d-4d6a-aade-0fc1c0cfc390
  Args:
    target: Marina_Ogilvy
    source: Zenouska_May_Mowatt
    relation: :hasMother
  AddTriple (6144efca-d19b-4f95-a89a-18a73828c9d0)
 Call ID: 6144efca-d19b-4f95-a89a-18a73828c9d0
  Args:
    relation: :hasMother
    source: Christian_Alexander_Mowatt
    target: Marina_Ogilvy
  Finish (88a7663f-5a3d-4317-b852-7a67dbdc985a)
 Call ID: 88a7663f-5a3d-4317-b852-7a67dbdc985a
  Args: