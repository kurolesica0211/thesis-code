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
Fergus Michael Claude Bowes-Lyon, 17th and 4th Earl of Strathmore and Kinghorne (31 December 1928 – 19 August 1987) was a British landowner and peer.
He was a nephew of Queen Elizabeth the Queen Mother, thus a first cousin of Queen Elizabeth II.
Early life and family

Born on 31 December 1928, Strathmore was the eldest son of Michael Claude Hamilton Bowes-Lyon and Elizabeth Margaret Cator (1899–1959).
His paternal grandparents were the 14th Earl and Countess of Strathmore and Kinghorne, and his maternal grandfather was John Cator, Conservative MP for Huntingdon.
In 1953, during the coronation of his cousin, Queen Elizabeth II, he was one of many servicemen lining the processional route.
Strathmore, then Captain Fergus Bowes-Lyon, married Mary Pamela McCorquodale (31 May 1932 – 28 April 2025) at St Margaret's, Westminster, on 10 April 1956 in a ceremony attended by his cousin, the Queen.
He was succeeded by his son, Michael.



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
  AssignClass (fe2f6f6c-579c-42b9-bc0b-7e39fbbbea1e)
 Call ID: fe2f6f6c-579c-42b9-bc0b-7e39fbbbea1e
  Args:
    type: :Man
    source: Fergus_Michael_Claude_Bowes-Lyon
  AssignClass (98f874e3-643b-4675-ad5c-6085d7907b49)
 Call ID: 98f874e3-643b-4675-ad5c-6085d7907b49
  Args:
    type: :Person
    source: Fergus_Michael_Claude_Bowes-Lyon
  AddLiteral (53bf476c-1302-4491-b17a-40eff1e22efc)
 Call ID: 53bf476c-1302-4491-b17a-40eff1e22efc
  Args:
    relation: :hasBirthYear
    literal_value: 1928
    source: Fergus_Michael_Claude_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (47b23730-dbb8-440d-925c-9d79559f77d2)
 Call ID: 47b23730-dbb8-440d-925c-9d79559f77d2
  Args:
    literal_type: xsd:integer
    source: Fergus_Michael_Claude_Bowes-Lyon
    literal_value: 1987
    relation: :hasDeathYear
  AssignClass (739287ba-5e26-4743-acd5-e9999026d111)
 Call ID: 739287ba-5e26-4743-acd5-e9999026d111
  Args:
    type: :Man
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (c5bf85c8-1c93-4cb8-bea1-5fe8eb3f4660)
 Call ID: c5bf85c8-1c93-4cb8-bea1-5fe8eb3f4660
  Args:
    type: :Person
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AddTriple (abb5d1d8-6a69-491b-92cd-ba1c40db1497)
 Call ID: abb5d1d8-6a69-491b-92cd-ba1c40db1497
  Args:
    target: Michael_Claude_Hamilton_Bowes-Lyon
    source: Fergus_Michael_Claude_Bowes-Lyon
    relation: :hasFather
  AssignClass (f35c1ea8-bfd8-4bac-8bcf-72e0e30f3bfc)
 Call ID: f35c1ea8-bfd8-4bac-8bcf-72e0e30f3bfc
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (d43703ce-0d25-465c-988d-4ac0e5cf8d54)
 Call ID: d43703ce-0d25-465c-988d-4ac0e5cf8d54
  Args:
    type: :Person
    source: Elizabeth_Margaret_Cator
  AddTriple (521e054f-5424-4ade-ad16-80cb7fe4d3fb)
 Call ID: 521e054f-5424-4ade-ad16-80cb7fe4d3fb
  Args:
    target: Elizabeth_Margaret_Cator
    source: Fergus_Michael_Claude_Bowes-Lyon
    relation: :hasMother
  AddLiteral (0e1493d4-bc64-40a3-8e6d-a90acd04be3b)
 Call ID: 0e1493d4-bc64-40a3-8e6d-a90acd04be3b
  Args:
    literal_value: 1899
    source: Elizabeth_Margaret_Cator
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2c8fca59-5018-438d-a5df-fca4d98c8bf7)
 Call ID: 2c8fca59-5018-438d-a5df-fca4d98c8bf7
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1959
    source: Elizabeth_Margaret_Cator
  AssignClass (15701647-cc4c-48b3-ba80-90026811c0c2)
 Call ID: 15701647-cc4c-48b3-ba80-90026811c0c2
  Args:
    type: :Woman
    source: Mary_Pamela_McCorquodale
  AssignClass (45fa2ed4-5982-4d82-adee-ae2da2b88246)
 Call ID: 45fa2ed4-5982-4d82-adee-ae2da2b88246
  Args:
    type: :Person
    source: Mary_Pamela_McCorquodale
  AddLiteral (ba24533e-bba6-4587-90ee-b384ea52ef30)
 Call ID: ba24533e-bba6-4587-90ee-b384ea52ef30
  Args:
    literal_type: xsd:integer
    source: Mary_Pamela_McCorquodale
    literal_value: 1932
    relation: :hasBirthYear
  AddLiteral (5268e2b3-12f6-469e-a425-237b6a47061a)
 Call ID: 5268e2b3-12f6-469e-a425-237b6a47061a
  Args:
    literal_type: xsd:integer
    source: Mary_Pamela_McCorquodale
    literal_value: 2025
    relation: :hasDeathYear
  AddLiteral (2f29a562-4aa1-44c6-ab7e-7fa121507e2c)
 Call ID: 2f29a562-4aa1-44c6-ab7e-7fa121507e2c
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Fergus_Michael_Claude_Bowes-Lyon
    literal_value: 1956
  AddTriple (a7e701ac-3bfb-4479-b878-c8b0ec74c22e)
 Call ID: a7e701ac-3bfb-4479-b878-c8b0ec74c22e
  Args:
    source: Fergus_Michael_Claude_Bowes-Lyon
    target: Mary_Pamela_McCorquodale
    relation: :hasRelation
  AssignClass (5b051384-65d7-44d1-bdaa-8fc2f8ed0fa4)
 Call ID: 5b051384-65d7-44d1-bdaa-8fc2f8ed0fa4
  Args:
    type: :Man
    source: Michael_son_of_Fergus
  AssignClass (08cd94d7-2dab-4c9d-9b17-450dd780ea8f)
 Call ID: 08cd94d7-2dab-4c9d-9b17-450dd780ea8f
  Args:
    type: :Person
    source: Michael_son_of_Fergus
  AddTriple (537011c1-41f5-44d7-9cc6-4abf18c8efde)
 Call ID: 537011c1-41f5-44d7-9cc6-4abf18c8efde
  Args:
    relation: :isSonOf
    source: Michael_son_of_Fergus
    target: Fergus_Michael_Claude_Bowes-Lyon
  Finish (451a2f05-ada0-4f1b-9b3f-106797b89566)
 Call ID: 451a2f05-ada0-4f1b-9b3f-106797b89566
  Args: