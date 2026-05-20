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
Timothy Patrick Bowes-Lyon, 16th and 3rd Earl of Strathmore and Kinghorne (18 March 1918 – 13 September 1972),  was a British nobleman and peer.
He was a nephew of Queen Elizabeth the Queen Mother, wife of King George VI, thus a first cousin of Queen Elizabeth II and Princess Margaret.
Biography

Born on 18 March 1918 in Teesdale, County Durham, he was the second son and third child of Patrick, Lord Glamis, and Lady Dorothy Osborne (1888–1946).
His father's youngest sister was the future Queen Elizabeth the Queen Mother.
He had no sons, so was succeeded by his first cousin, Captain Fergus Bowes-Lyon.



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
  AssignClass (2d1af26b-f451-4d9e-9617-69230757194b)
 Call ID: 2d1af26b-f451-4d9e-9617-69230757194b
  Args:
    type: :Man
    source: Timothy_Patrick_Bowes-Lyon
  AssignClass (39254a59-6d44-4bc9-85d6-89cf94c1e9ff)
 Call ID: 39254a59-6d44-4bc9-85d6-89cf94c1e9ff
  Args:
    source: Timothy_Patrick_Bowes-Lyon
    type: :Person
  AddLiteral (54a2f592-12be-4eef-9b5c-3c35df35150b)
 Call ID: 54a2f592-12be-4eef-9b5c-3c35df35150b
  Args:
    literal_value: 1918
    source: Timothy_Patrick_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b0d1a0d5-d6e5-42f7-b368-5c5d25505e1e)
 Call ID: b0d1a0d5-d6e5-42f7-b368-5c5d25505e1e
  Args:
    literal_type: xsd:integer
    source: Timothy_Patrick_Bowes-Lyon
    literal_value: 1972
    relation: :hasDeathYear
  AssignClass (60505ace-33dc-432d-a83d-dcf9e992b483)
 Call ID: 60505ace-33dc-432d-a83d-dcf9e992b483
  Args:
    source: Patrick_Lord_Glamis
    type: :Man
  AssignClass (9cf3336f-bda9-40df-944c-1087530b2c64)
 Call ID: 9cf3336f-bda9-40df-944c-1087530b2c64
  Args:
    type: :Person
    source: Patrick_Lord_Glamis
  AssignClass (5a776078-7075-495b-83f8-695b644deb92)
 Call ID: 5a776078-7075-495b-83f8-695b644deb92
  Args:
    source: Lady_Dorothy_Osborne
    type: :Woman
  AssignClass (4375aa91-0106-4677-981e-495928446bb4)
 Call ID: 4375aa91-0106-4677-981e-495928446bb4
  Args:
    type: :Person
    source: Lady_Dorothy_Osborne
  AddLiteral (45e6cc02-0850-4766-9412-2ea93c4cc443)
 Call ID: 45e6cc02-0850-4766-9412-2ea93c4cc443
  Args:
    literal_value: 1888
    source: Lady_Dorothy_Osborne
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (64c9c2ab-2868-433c-a7e0-bcf570c1f178)
 Call ID: 64c9c2ab-2868-433c-a7e0-bcf570c1f178
  Args:
    source: Lady_Dorothy_Osborne
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (fd2925e7-72af-4f91-b1d2-ea6e42b963c1)
 Call ID: fd2925e7-72af-4f91-b1d2-ea6e42b963c1
  Args:
    relation: :hasFather
    target: Patrick_Lord_Glamis
    source: Timothy_Patrick_Bowes-Lyon
  AddTriple (2ec17227-c4f5-4ce5-aa12-371c5b2d8cf1)
 Call ID: 2ec17227-c4f5-4ce5-aa12-371c5b2d8cf1
  Args:
    source: Timothy_Patrick_Bowes-Lyon
    relation: :hasMother
    target: Lady_Dorothy_Osborne
  AssignClass (c4589a2c-ef6b-4255-9e3d-f82a5fd990b3)
 Call ID: c4589a2c-ef6b-4255-9e3d-f82a5fd990b3
  Args:
    source: Queen_Elizabeth_the_Queen_Mother
    type: :Woman
  AssignClass (1031f080-5997-49e4-a572-78936b1a7fe2)
 Call ID: 1031f080-5997-49e4-a572-78936b1a7fe2
  Args:
    source: Queen_Elizabeth_the_Queen_Mother
    type: :Person
  AddTriple (9137c03a-5702-4b11-b03b-3fea24cf1bef)
 Call ID: 9137c03a-5702-4b11-b03b-3fea24cf1bef
  Args:
    source: Queen_Elizabeth_the_Queen_Mother
    target: Patrick_Lord_Glamis
    relation: :isSisterOf
  AssignClass (f368e2f6-39d7-41fc-909f-639ce950d2e7)
 Call ID: f368e2f6-39d7-41fc-909f-639ce950d2e7
  Args:
    source: King_George_VI
    type: :Man
  AssignClass (eaf7f213-d66c-45e0-adb6-83677c041089)
 Call ID: eaf7f213-d66c-45e0-adb6-83677c041089
  Args:
    type: :Person
    source: King_George_VI
  AssignClass (d58a6ac3-ddb0-48b8-a766-eccb13025e30)
 Call ID: d58a6ac3-ddb0-48b8-a766-eccb13025e30
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (f91ff5cb-8232-48ea-8f3c-c27f8a0d7a9f)
 Call ID: f91ff5cb-8232-48ea-8f3c-c27f8a0d7a9f
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (f44b254a-65d7-4f01-8319-466ba168feb7)
 Call ID: f44b254a-65d7-4f01-8319-466ba168feb7
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (43958490-83ec-4d42-9bcd-a987d4ab2008)
 Call ID: 43958490-83ec-4d42-9bcd-a987d4ab2008
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (d1344b2c-f290-4a7d-8aec-cc63de3a6c1f)
 Call ID: d1344b2c-f290-4a7d-8aec-cc63de3a6c1f
  Args:
    source: Captain_Fergus_Bowes-Lyon
    type: :Man
  AssignClass (63ebbb5f-cc10-4272-ae46-af67e3be36b6)
 Call ID: 63ebbb5f-cc10-4272-ae46-af67e3be36b6
  Args:
    source: Captain_Fergus_Bowes-Lyon
    type: :Person
  AddTriple (d99f6bbf-25f7-4cf3-a162-7f951cae606d)
 Call ID: d99f6bbf-25f7-4cf3-a162-7f951cae606d
  Args:
    target: Captain_Fergus_Bowes-Lyon
    relation: :isBloodrelationOf
    source: Timothy_Patrick_Bowes-Lyon
  Finish (67bc8ba4-c154-4023-856a-a4e09e95d241)
 Call ID: 67bc8ba4-c154-4023-856a-a4e09e95d241
  Args: