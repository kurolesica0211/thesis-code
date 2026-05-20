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
Prince Philip of Bourbon-Two Sicilies (Filippo Maria Alfonso Antonio Ferdinando Francesco di Paola Lodovico Enrico Alberto Taddeo Francesco Saverio Uberto; 10 December 1885 – 9 March 1949) was a member of the House of Bourbon-Two Sicilies and a Prince of Bourbon-Two Sicilies.
Family

Prince Philip was the tenth child of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta, and his wife, Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage and issue

Philip married firstly to Princess Marie Louise of Orléans, eldest daughter and child of Prince Emmanuel, Duke of Vendôme and his wife Princess Henriette of Belgium, on 12 January 1916 in Neuilly-sur-Seine.



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
  AssignClass (8bc0edd4-d5bd-4f25-b3f0-3e769fbcc7c4)
 Call ID: 8bc0edd4-d5bd-4f25-b3f0-3e769fbcc7c4
  Args:
    source: Prince_Philip_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (14a9b7ba-f387-41bb-b684-2d1a23091076)
 Call ID: 14a9b7ba-f387-41bb-b684-2d1a23091076
  Args:
    type: :Man
    source: Prince_Philip_of_Bourbon-Two_Sicilies
  AssignClass (e3fc4cdb-3d3c-4dd3-896e-bafe36beab48)
 Call ID: e3fc4cdb-3d3c-4dd3-896e-bafe36beab48
  Args:
    source: Prince_Alfonso_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (c9649f8c-e559-4ebf-b4cc-b104b829a312)
 Call ID: c9649f8c-e559-4ebf-b4cc-b104b829a312
  Args:
    type: :Man
    source: Prince_Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (1c1cfea7-d374-40c1-b218-e7e8cdc0fc9a)
 Call ID: 1c1cfea7-d374-40c1-b218-e7e8cdc0fc9a
  Args:
    type: :Person
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (a18d9221-f2de-46c9-9127-8e65bf80619a)
 Call ID: a18d9221-f2de-46c9-9127-8e65bf80619a
  Args:
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (240b5a0b-3969-443a-8c5a-1a6d31ef5566)
 Call ID: 240b5a0b-3969-443a-8c5a-1a6d31ef5566
  Args:
    type: :Person
    source: Princess_Marie_Louise_of_Orleans
  AssignClass (2b73146b-3bf3-42e8-b166-11d2350f88fb)
 Call ID: 2b73146b-3bf3-42e8-b166-11d2350f88fb
  Args:
    source: Princess_Marie_Louise_of_Orleans
    type: :Woman
  AssignClass (9125f55b-7e9d-479e-9b19-289687b26452)
 Call ID: 9125f55b-7e9d-479e-9b19-289687b26452
  Args:
    type: :Person
    source: Prince_Emmanuel_Duke_of_Vendome
  AssignClass (07041410-8d25-4645-87f3-2e2afb73e5d8)
 Call ID: 07041410-8d25-4645-87f3-2e2afb73e5d8
  Args:
    type: :Man
    source: Prince_Emmanuel_Duke_of_Vendome
  AssignClass (870bbd90-3ab1-4b0a-8e1d-f6a50c865115)
 Call ID: 870bbd90-3ab1-4b0a-8e1d-f6a50c865115
  Args:
    type: :Person
    source: Princess_Henriette_of_Belgium
  AssignClass (8e7a44b1-dbb0-4c08-9ba2-e9d655ec23e8)
 Call ID: 8e7a44b1-dbb0-4c08-9ba2-e9d655ec23e8
  Args:
    source: Princess_Henriette_of_Belgium
    type: :Woman
  AddLiteral (797b4165-87ca-42a2-af92-4870f214395d)
 Call ID: 797b4165-87ca-42a2-af92-4870f214395d
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Philip_of_Bourbon-Two_Sicilies
    literal_value: 1885
  AddLiteral (3d12a326-87f7-4501-9355-cf1bb85d9a56)
 Call ID: 3d12a326-87f7-4501-9355-cf1bb85d9a56
  Args:
    literal_type: xsd:integer
    literal_value: 1949
    source: Prince_Philip_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
  AddTriple (fdb62416-c196-445b-bf37-b43f59631e53)
 Call ID: fdb62416-c196-445b-bf37-b43f59631e53
  Args:
    relation: :hasFather
    target: Prince_Alfonso_of_Bourbon-Two_Sicilies
    source: Prince_Philip_of_Bourbon-Two_Sicilies
  AddTriple (c8fb3486-a713-4ad4-84ab-6f9e1145ccb8)
 Call ID: c8fb3486-a713-4ad4-84ab-6f9e1145ccb8
  Args:
    source: Prince_Philip_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (9c223c47-1262-485e-987b-616e6b44bc6a)
 Call ID: 9c223c47-1262-485e-987b-616e6b44bc6a
  Args:
    source: Princess_Marie_Louise_of_Orleans
    target: Prince_Emmanuel_Duke_of_Vendome
    relation: :hasFather
  AddTriple (07df7149-69d1-4a16-931f-64996440cfb6)
 Call ID: 07df7149-69d1-4a16-931f-64996440cfb6
  Args:
    source: Princess_Marie_Louise_of_Orleans
    target: Princess_Henriette_of_Belgium
    relation: :hasMother
  AddLiteral (5fdf197e-5980-4d2c-bf31-957353a2f7bc)
 Call ID: 5fdf197e-5980-4d2c-bf31-957353a2f7bc
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_Philip_of_Bourbon-Two_Sicilies
    literal_value: 1916
  AddTriple (9fc64721-2aa3-46dd-a1a7-8c322afdea34)
 Call ID: 9fc64721-2aa3-46dd-a1a7-8c322afdea34
  Args:
    relation: :hasRelation
    target: Princess_Marie_Louise_of_Orleans
    source: Prince_Philip_of_Bourbon-Two_Sicilies
  Finish (d548371a-6ec3-47df-ade9-1df2652ebdcb)
 Call ID: d548371a-6ec3-47df-ade9-1df2652ebdcb
  Args: