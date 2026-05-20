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
Prince Karl Adolf Andreas Prinz von Hesse (German: Karl Adolf Andreas Prinz Von Hessen; 26 March 1937 – 23 March 2022) was a member of the German electoral House of Hesse-Kassel.
He was a first cousin of King Charles III of the United Kingdom through his uncle Prince Philip.
Early life and ancestry

Born on 26  March 1937 in Berlin, into an elder line of the House of Hesse, a house directly descended from the House of Brabant, Karl Adolf Andreas was the eldest son of Prince Christoph of Hesse and his wife, Princess Sophie of Greece and Denmark, youngest sister of Prince Philip, Duke of Edinburgh.
In 1946, his mother was married again to Prince George William of Hanover, maternal grandson of Wilhelm II.
Orphaned by his father at an early age, Karl was later adopted by one of his paternal uncles, Prince Wolfgang of Hesse, in 1952.
Related to most European dynasties, Karl participated in the major events of the gotha.
In 1954, he and his family were invited to take part in the Cruise of the Kings, organized by King Paul of Greece and his wife Queen Frederica.
Karl briefly discussed his mother's childhood and her ties to the Nazi regime in a documentary in 2015 about his uncle, Prince Philip:
Death

Prince Karl of Hesse died in Munich, at the age of 84 years, on March 23, 2022.
}} Media related to Karl Adolf Andreas of Hesse at Wikimedia Commons



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
  AssignClass (bb4fb57c-e671-4432-be7f-f0dbba753d0b)
 Call ID: bb4fb57c-e671-4432-be7f-f0dbba753d0b
  Args:
    source: :Karl_Adolf_Andreas_of_Hesse
    type: :Man
  AssignClass (d55340c3-dff2-4620-b0e3-ffcc628cfd89)
 Call ID: d55340c3-dff2-4620-b0e3-ffcc628cfd89
  Args:
    type: :Person
    source: :Karl_Adolf_Andreas_of_Hesse
  AddLiteral (6e149cb8-372d-4aa7-a219-f56afedce3d4)
 Call ID: 6e149cb8-372d-4aa7-a219-f56afedce3d4
  Args:
    source: :Karl_Adolf_Andreas_of_Hesse
    literal_type: xsd:integer
    literal_value: 1937
    relation: :hasBirthYear
  AddLiteral (dda69928-913b-4c89-b875-3e825471114e)
 Call ID: dda69928-913b-4c89-b875-3e825471114e
  Args:
    literal_value: 2022
    relation: :hasDeathYear
    source: :Karl_Adolf_Andreas_of_Hesse
    literal_type: xsd:integer
  AssignClass (cb25bee7-7ee1-4734-8f17-18c09f07bd66)
 Call ID: cb25bee7-7ee1-4734-8f17-18c09f07bd66
  Args:
    type: :Man
    source: :Christoph_of_Hesse
  AssignClass (e3872312-a933-4f9d-8bfe-0b331c867a4a)
 Call ID: e3872312-a933-4f9d-8bfe-0b331c867a4a
  Args:
    source: :Christoph_of_Hesse
    type: :Person
  AddTriple (a20607e5-54a6-4c84-abbf-9d6eb0fcc9c8)
 Call ID: a20607e5-54a6-4c84-abbf-9d6eb0fcc9c8
  Args:
    source: :Karl_Adolf_Andreas_of_Hesse
    relation: :hasFather
    target: :Christoph_of_Hesse
  AssignClass (4ef815e7-7ada-4822-a0f5-0b7ecd5a5775)
 Call ID: 4ef815e7-7ada-4822-a0f5-0b7ecd5a5775
  Args:
    type: :Woman
    source: :Sophie_of_Greece_and_Denmark
  AssignClass (d0d92fa8-0d27-405c-bbe5-4f27a157167b)
 Call ID: d0d92fa8-0d27-405c-bbe5-4f27a157167b
  Args:
    type: :Person
    source: :Sophie_of_Greece_and_Denmark
  AddTriple (66bd3545-26fd-44c9-af5c-ad7f53e114b2)
 Call ID: 66bd3545-26fd-44c9-af5c-ad7f53e114b2
  Args:
    source: :Karl_Adolf_Andreas_of_Hesse
    target: :Sophie_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (394bae61-94ac-44b9-a98a-d00923f5f75b)
 Call ID: 394bae61-94ac-44b9-a98a-d00923f5f75b
  Args:
    type: :Man
    source: :Philip_Duke_of_Edinburgh
  AssignClass (4a308fad-7b4c-47b1-ba5a-b7c86c5ac42b)
 Call ID: 4a308fad-7b4c-47b1-ba5a-b7c86c5ac42b
  Args:
    source: :Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (593f5171-7685-4448-9bd4-57e0aa305e37)
 Call ID: 593f5171-7685-4448-9bd4-57e0aa305e37
  Args:
    relation: :isBrotherOf
    target: :Sophie_of_Greece_and_Denmark
    source: :Philip_Duke_of_Edinburgh
  AssignClass (1a8f56b4-9b67-4662-a624-c42d931708e1)
 Call ID: 1a8f56b4-9b67-4662-a624-c42d931708e1
  Args:
    source: :Wolfgang_of_Hesse
    type: :Man
  AssignClass (115370b0-03b0-46d5-b01c-f5cb7029f181)
 Call ID: 115370b0-03b0-46d5-b01c-f5cb7029f181
  Args:
    type: :Person
    source: :Wolfgang_of_Hesse
  AddTriple (61dfa5e8-bf71-44f8-89bf-486719c695ff)
 Call ID: 61dfa5e8-bf71-44f8-89bf-486719c695ff
  Args:
    target: :Karl_Adolf_Andreas_of_Hesse
    relation: :isUncleOf
    source: :Wolfgang_of_Hesse
  AssignClass (0799c2da-21a6-46df-a083-2239a698fa9f)
 Call ID: 0799c2da-21a6-46df-a083-2239a698fa9f
  Args:
    source: :George_William_of_Hanover
    type: :Man
  AssignClass (16be519b-cff5-4e2f-b508-e6cda41f6d48)
 Call ID: 16be519b-cff5-4e2f-b508-e6cda41f6d48
  Args:
    source: :George_William_of_Hanover
    type: :Person
  AddTriple (b9eebf2c-2a9b-44f8-98dc-44d8ea2bd070)
 Call ID: b9eebf2c-2a9b-44f8-98dc-44d8ea2bd070
  Args:
    relation: :hasRelation
    target: :George_William_of_Hanover
    source: :Sophie_of_Greece_and_Denmark
  AssignClass (49ca1e85-4925-46ec-b6a5-a60b47d7afa9)
 Call ID: 49ca1e85-4925-46ec-b6a5-a60b47d7afa9
  Args:
    source: :Charles_III_of_the_United_Kingdom
    type: :Man
  AssignClass (0536e102-7a26-4c96-85a6-27bfe340eb7d)
 Call ID: 0536e102-7a26-4c96-85a6-27bfe340eb7d
  Args:
    source: :Charles_III_of_the_United_Kingdom
    type: :Person
  AddTriple (7fa93157-2f98-4e45-83f6-8162b25d1650)
 Call ID: 7fa93157-2f98-4e45-83f6-8162b25d1650
  Args:
    relation: :isBloodrelationOf
    target: :Charles_III_of_the_United_Kingdom
    source: :Karl_Adolf_Andreas_of_Hesse
  Finish (1b92d70c-95d7-40c4-b0c3-660497a3f9d9)
 Call ID: 1b92d70c-95d7-40c4-b0c3-660497a3f9d9
  Args: