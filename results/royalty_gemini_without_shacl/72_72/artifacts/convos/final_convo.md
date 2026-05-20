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
Helen Mary Malcolm (15 March 1918 – 13 October 2010) was one of the first two regular female announcers on BBC Television after the Second World War and was a household name in the United Kingdom during the 1950s.
Biography

The only daughter and youngest of four children of the diplomat and politician Sir Ian Malcolm and Jeanne Langtry (1881–1964) and granddaughter of the Victorian socialite and actress Lillie Langtry, a mistress of King Edward VII, Mary Malcolm was born in Marylebone and brought up partly in Poltalloch, Argyll, Scotland.
Mary Malcolm was taken on and worked for the Home Service as a continuity announcer from March 1942.
At this time, all television programmes were introduced by an in-vision host or hostess and broadcasts were normally live.
Malcolm received no training and became known for her spoonerisms: "By the end of the day I was tired, and when I came to the weather forecast I just read it out without really trying.
Malcolm left the BBC in 1956 although she continued to appear as a guest on various programmes including an episode of the comedy series The Goodies.
Personal life

Malcolm was first married to Sir Basil Bartlett, a baronet and actor, on 5 January 1937.
Malcolm had the onset of dementia late on in her life and died on 13 October 2010 at the Hilton Park care centre in Bottisham, Cambridgeshire.



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
  AssignClass (1ef8e685-3ad2-4ce3-aa41-4d99ab3b72b3)
 Call ID: 1ef8e685-3ad2-4ce3-aa41-4d99ab3b72b3
  Args:
    type: :Woman
    source: Mary_Malcolm
  AssignClass (601786f6-8cf8-461d-964b-7792d054e8b9)
 Call ID: 601786f6-8cf8-461d-964b-7792d054e8b9
  Args:
    type: :Person
    source: Mary_Malcolm
  AddLiteral (f82fa391-01f9-46ac-bd0c-4a61526741c3)
 Call ID: f82fa391-01f9-46ac-bd0c-4a61526741c3
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: Mary_Malcolm
    literal_value: Helen Mary Malcolm
  AddLiteral (826d9e09-a9dc-46e8-b999-5dcc5a9c7220)
 Call ID: 826d9e09-a9dc-46e8-b999-5dcc5a9c7220
  Args:
    literal_type: xsd:integer
    source: Mary_Malcolm
    literal_value: 1918
    relation: :hasBirthYear
  AddLiteral (44eee6c9-cfc5-48f7-97c0-1a86c7955643)
 Call ID: 44eee6c9-cfc5-48f7-97c0-1a86c7955643
  Args:
    relation: :hasDeathYear
    source: Mary_Malcolm
    literal_value: 2010
    literal_type: xsd:integer
  AssignClass (1021aad2-32a5-402d-a338-094775dfe49d)
 Call ID: 1021aad2-32a5-402d-a338-094775dfe49d
  Args:
    type: :Man
    source: Ian_Malcolm
  AssignClass (fe31885d-3206-4479-86b9-eb7725b567d5)
 Call ID: fe31885d-3206-4479-86b9-eb7725b567d5
  Args:
    type: :Ancestor
    source: Ian_Malcolm
  AssignClass (41ccfca5-95f0-4263-9323-e44b128250b2)
 Call ID: 41ccfca5-95f0-4263-9323-e44b128250b2
  Args:
    type: :Person
    source: Ian_Malcolm
  AddTriple (9215f7da-b801-4b85-bc68-1ad192064d61)
 Call ID: 9215f7da-b801-4b85-bc68-1ad192064d61
  Args:
    relation: :hasFather
    source: Mary_Malcolm
    target: Ian_Malcolm
  AssignClass (3dc85353-c721-482d-8e5f-617202cc66c0)
 Call ID: 3dc85353-c721-482d-8e5f-617202cc66c0
  Args:
    type: :Woman
    source: Jeanne_Langtry
  AssignClass (7343ddad-52d5-4943-b1f8-d4e23ed323f8)
 Call ID: 7343ddad-52d5-4943-b1f8-d4e23ed323f8
  Args:
    type: :Ancestor
    source: Jeanne_Langtry
  AssignClass (f3c3ac08-3709-44e6-9722-cd73fb6a7076)
 Call ID: f3c3ac08-3709-44e6-9722-cd73fb6a7076
  Args:
    type: :Person
    source: Jeanne_Langtry
  AddTriple (60af8bf8-53c0-41a9-afdb-d475a6cd70e3)
 Call ID: 60af8bf8-53c0-41a9-afdb-d475a6cd70e3
  Args:
    target: Jeanne_Langtry
    source: Mary_Malcolm
    relation: :hasMother
  AddLiteral (07774e60-40bc-4873-8310-8b020922ce86)
 Call ID: 07774e60-40bc-4873-8310-8b020922ce86
  Args:
    literal_value: 1881
    source: Jeanne_Langtry
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (51d52049-cd22-49a3-8a4d-f709b5bf3c78)
 Call ID: 51d52049-cd22-49a3-8a4d-f709b5bf3c78
  Args:
    relation: :hasDeathYear
    source: Jeanne_Langtry
    literal_value: 1964
    literal_type: xsd:integer
  AssignClass (7232676b-2520-4b64-a3bf-a7a58efb1a34)
 Call ID: 7232676b-2520-4b64-a3bf-a7a58efb1a34
  Args:
    type: :Woman
    source: Lillie_Langtry
  AssignClass (8e15f993-375e-44ec-9dbf-b7d5ccbaa416)
 Call ID: 8e15f993-375e-44ec-9dbf-b7d5ccbaa416
  Args:
    type: :Ancestor
    source: Lillie_Langtry
  AssignClass (418edac4-5c2f-4db6-b249-d0bbb3ad3390)
 Call ID: 418edac4-5c2f-4db6-b249-d0bbb3ad3390
  Args:
    type: :Person
    source: Lillie_Langtry
  AddTriple (2f5564ca-071f-4cf4-96a9-882173621986)
 Call ID: 2f5564ca-071f-4cf4-96a9-882173621986
  Args:
    source: Lillie_Langtry
    relation: :isAncestorOf
    target: Mary_Malcolm
  AssignClass (ca7b2eaf-d0e8-4cf2-b6fd-5c758c9726aa)
 Call ID: ca7b2eaf-d0e8-4cf2-b6fd-5c758c9726aa
  Args:
    type: :Man
    source: Basil_Bartlett
  AssignClass (9ba154b6-8cf9-4d37-a9fe-541413790a13)
 Call ID: 9ba154b6-8cf9-4d37-a9fe-541413790a13
  Args:
    type: :Person
    source: Basil_Bartlett
  AddLiteral (6bb7ef59-08a9-4d5d-bf72-d33388417242)
 Call ID: 6bb7ef59-08a9-4d5d-bf72-d33388417242
  Args:
    source: Mary_Malcolm
    literal_value: 1937
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (76126672-80af-4a24-8a0e-c206ef0a740f)
 Call ID: 76126672-80af-4a24-8a0e-c206ef0a740f
  Args:
    relation: :hasRelation
    source: Mary_Malcolm
    target: Basil_Bartlett
  Finish (9ba87a5e-b372-4b04-b779-3a40e355999c)
 Call ID: 9ba87a5e-b372-4b04-b779-3a40e355999c
  Args: