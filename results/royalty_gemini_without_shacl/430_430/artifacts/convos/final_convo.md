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
Dame Sarah Rose Troughton (née Colman; born 3
Early life

Troughton was born in Paddington in 1953.
She is the eldest of the five children of Sir Timothy Colman, a past Lord Lieutenant of Norfolk, and Lady Mary Cecilia Bowes-Lyon, a granddaughter of Claude Bowes-Lyon, 14th
Her ancestor Jeremiah Colman (1777–1851) made a fortune from Colman's mustard, a business which eventually grew into Reckitt & Colman, of which her father was a director until 1989.
Public life

From 1990 to 2000, Troughton was lady-in-waiting to the Duchess of Kent.
As Lord Lieutenant, Troughton's public duties include overseeing arrangements for visits to Wiltshire by members of the Royal Family and escorting royal visitors; representing the King at events and presenting awards and medals on his behalf; liaising with the Wiltshire units of the Royal Navy, Army and Royal Air Force; leading the local magistracy as chairman of the Lord Chancellor's Advisory Committee on Justices of the Peace; and advising on nominations for national honours.
In January 2013, Troughton was appointed a Commander of the Order of St John by the Queen, and advanced to Dame of Grace of the order in 2021.
A BBC News article described Troughton as one of Camilla's longstanding personal friends.
Troughton was appointed a Dame Commander of the Royal Victorian Order in the 2025 New Year Honours.
Personal life

In 1977 she married Peter Troughton (born 1948), a member of HM Diplomatic Service, and the eldest son of Sir Charles Troughton, chairman of W H Smith.



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
  AssignClass (1858246d-c695-4792-8f7e-20f32f54b456)
 Call ID: 1858246d-c695-4792-8f7e-20f32f54b456
  Args:
    source: Sarah_Troughton
    type: :Woman
  AssignClass (868b6daf-94d2-45b6-9dbc-a0ae6d63b114)
 Call ID: 868b6daf-94d2-45b6-9dbc-a0ae6d63b114
  Args:
    type: :Person
    source: Sarah_Troughton
  AddLiteral (72752203-26bb-4a23-8cf2-36f725a5e137)
 Call ID: 72752203-26bb-4a23-8cf2-36f725a5e137
  Args:
    source: Sarah_Troughton
    literal_type: xsd:integer
    literal_value: 1953
    relation: :hasBirthYear
  AssignClass (1aa57b59-f814-4109-a343-69f3cc7b8d74)
 Call ID: 1aa57b59-f814-4109-a343-69f3cc7b8d74
  Args:
    source: Timothy_Colman
    type: :Man
  AssignClass (9f797e28-d222-4091-9e4b-83b343ef546a)
 Call ID: 9f797e28-d222-4091-9e4b-83b343ef546a
  Args:
    type: :Person
    source: Timothy_Colman
  AddTriple (80bcc153-8158-4f9f-b7c0-5d431e856f55)
 Call ID: 80bcc153-8158-4f9f-b7c0-5d431e856f55
  Args:
    target: Timothy_Colman
    source: Sarah_Troughton
    relation: :hasFather
  AssignClass (2de6aa64-b81a-4c0f-bda1-aa8437adfc15)
 Call ID: 2de6aa64-b81a-4c0f-bda1-aa8437adfc15
  Args:
    type: :Woman
    source: Mary_Cecilia_Bowes-Lyon
  AssignClass (5ec3e82d-3927-4055-af4d-c2ee48e31b25)
 Call ID: 5ec3e82d-3927-4055-af4d-c2ee48e31b25
  Args:
    type: :Person
    source: Mary_Cecilia_Bowes-Lyon
  AddTriple (583f36e8-aeb6-4ff6-b49d-88b6b7770018)
 Call ID: 583f36e8-aeb6-4ff6-b49d-88b6b7770018
  Args:
    target: Mary_Cecilia_Bowes-Lyon
    source: Sarah_Troughton
    relation: :hasMother
  AssignClass (c2ea9449-8815-4851-bea9-bb2404abcc30)
 Call ID: c2ea9449-8815-4851-bea9-bb2404abcc30
  Args:
    source: Claude_Bowes-Lyon
    type: :Man
  AssignClass (7933268b-65d7-473d-8fac-e1d7faa98216)
 Call ID: 7933268b-65d7-473d-8fac-e1d7faa98216
  Args:
    source: Claude_Bowes-Lyon
    type: :Person
  AddTriple (33686c03-58f3-431d-a9ff-6e8b233e90a9)
 Call ID: 33686c03-58f3-431d-a9ff-6e8b233e90a9
  Args:
    relation: :hasAncestor
    source: Mary_Cecilia_Bowes-Lyon
    target: Claude_Bowes-Lyon
  AssignClass (90bad6eb-9220-44d4-91a9-2d7a04c44e67)
 Call ID: 90bad6eb-9220-44d4-91a9-2d7a04c44e67
  Args:
    type: :Man
    source: Jeremiah_Colman
  AssignClass (0de6cddd-a459-40c7-a6c6-41acccfdaa06)
 Call ID: 0de6cddd-a459-40c7-a6c6-41acccfdaa06
  Args:
    type: :Person
    source: Jeremiah_Colman
  AddLiteral (6b27b30c-80cd-4ce2-ad29-e8eb67b1b559)
 Call ID: 6b27b30c-80cd-4ce2-ad29-e8eb67b1b559
  Args:
    source: Jeremiah_Colman
    literal_type: xsd:integer
    literal_value: 1777
    relation: :hasBirthYear
  AddLiteral (2011cf7a-1496-48c2-9338-daa90fa1808c)
 Call ID: 2011cf7a-1496-48c2-9338-daa90fa1808c
  Args:
    relation: :hasDeathYear
    literal_value: 1851
    source: Jeremiah_Colman
    literal_type: xsd:integer
  AddTriple (422c92a7-a540-40ef-a6eb-0ea2ff3082ae)
 Call ID: 422c92a7-a540-40ef-a6eb-0ea2ff3082ae
  Args:
    relation: :hasAncestor
    source: Sarah_Troughton
    target: Jeremiah_Colman
  AssignClass (b2c7c5f2-e48b-46a5-bbf4-7bec8c384ceb)
 Call ID: b2c7c5f2-e48b-46a5-bbf4-7bec8c384ceb
  Args:
    source: Peter_Troughton
    type: :Man
  AssignClass (06900898-8171-4fdc-be1b-c8e55b5e65e9)
 Call ID: 06900898-8171-4fdc-be1b-c8e55b5e65e9
  Args:
    type: :Person
    source: Peter_Troughton
  AddLiteral (bdf50db4-cea8-4a4a-90e9-aad5b8f7b8c9)
 Call ID: bdf50db4-cea8-4a4a-90e9-aad5b8f7b8c9
  Args:
    literal_value: 1948
    relation: :hasBirthYear
    source: Peter_Troughton
    literal_type: xsd:integer
  AddLiteral (00af7a89-030a-4036-a4f8-3b731a69ae40)
 Call ID: 00af7a89-030a-4036-a4f8-3b731a69ae40
  Args:
    relation: :hasMarriageYear
    literal_value: 1977
    literal_type: xsd:integer
    source: Sarah_Troughton
  AddTriple (b3dfe969-6421-49ec-a235-3a846be32dfd)
 Call ID: b3dfe969-6421-49ec-a235-3a846be32dfd
  Args:
    source: Sarah_Troughton
    relation: :hasRelation
    target: Peter_Troughton
  AssignClass (08cfe405-6b02-4230-aede-e54143da4f0c)
 Call ID: 08cfe405-6b02-4230-aede-e54143da4f0c
  Args:
    type: :Man
    source: Charles_Troughton
  AssignClass (5c3ac03a-cf57-4a08-83c4-e15707e4b0d8)
 Call ID: 5c3ac03a-cf57-4a08-83c4-e15707e4b0d8
  Args:
    source: Charles_Troughton
    type: :Person
  AddTriple (107850ee-7f69-4807-b157-688ef8c03300)
 Call ID: 107850ee-7f69-4807-b157-688ef8c03300
  Args:
    source: Peter_Troughton
    relation: :hasFather
    target: Charles_Troughton
  Finish (00f93131-a5de-482c-a3ba-a367d769fa66)
 Call ID: 00f93131-a5de-482c-a3ba-a367d769fa66
  Args: