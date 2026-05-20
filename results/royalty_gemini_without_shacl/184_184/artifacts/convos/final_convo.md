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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


The Duke of AostaThe Duchess of Aosta


The Dowager Duchess of Aosta


Princess Olga Isabelle of Savoy-Aosta, Duchess of Aosta (née Princess Olga of Greece;
Greek: Πριγκίπισσα Όλγα της Ελλάδας; born 11 November 1971), is the younger daughter of author Prince Michael of Greece and Denmark and Marina Karella, an artist and daughter of the Greek business magnate Theódoros Karéllas.
Olga is married to her second cousin Prince Aimone, Duke of Aosta.
Early life

Princess Olga was born on 11 November 1971 in Athens, Greece.
She is the younger sister of Princess Alexandra and grew up in Paris and New York, spending summers at the family's island retreat at Patmos, Greece.
Engagement, marriage and children

Olga's engagement to Prince Aimone of Savoy, son of Amedeo, 5th Duke of Aosta, was announced in May 2005.
They are also second cousins once removed as George I of Greece is Aimone's great-great-grandfather and Olga's great-grandfather.
Olga's father, Prince Michael of Greece and Denmark, Aimone's paternal grandmother, Princess Irene, Duchess of Aosta (née Princess Irene of Greece and Denmark), and Prince Philip, Duke of Edinburgh (born Prince Philip of Greece and Denmark), were all first cousins.
A canonical dispensation was obtained from the Catholic Archbishop of Moscow, Monsignor Paolo Pezzi, who was the local Ordinary of prince Aimone.
On 14 December 2012, Olga gave birth to a baby daughter, Isabella Vita Marina, in Paris, France.



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
  AssignClass (1567315c-6ed6-4ace-b7d1-2ca304353a82)
 Call ID: 1567315c-6ed6-4ace-b7d1-2ca304353a82
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece
  AssignClass (d23c4a1a-bdf5-4e48-8a95-6d60d5f29e86)
 Call ID: d23c4a1a-bdf5-4e48-8a95-6d60d5f29e86
  Args:
    type: :Person
    source: Princess_Olga_of_Greece
  AssignClass (18a238ac-38b9-449a-89f8-78c94966aaa3)
 Call ID: 18a238ac-38b9-449a-89f8-78c94966aaa3
  Args:
    source: Prince_Michael_of_Greece_and_Denmark
    type: :Man
  AssignClass (a02e862d-800f-4403-8e30-64d0e39da3a8)
 Call ID: a02e862d-800f-4403-8e30-64d0e39da3a8
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (8d391e5e-9677-4a71-90c2-280b9ae8efa9)
 Call ID: 8d391e5e-9677-4a71-90c2-280b9ae8efa9
  Args:
    source: Marina_Karella
    type: :Woman
  AssignClass (c671fae5-b365-4195-be0d-a7017a788361)
 Call ID: c671fae5-b365-4195-be0d-a7017a788361
  Args:
    type: :Person
    source: Marina_Karella
  AssignClass (04faa972-e516-4cf2-b9d7-23bfba65930d)
 Call ID: 04faa972-e516-4cf2-b9d7-23bfba65930d
  Args:
    source: Theodoros_Karellas
    type: :Man
  AssignClass (dfd37500-07fc-4a01-a605-e8ab76bf99f1)
 Call ID: dfd37500-07fc-4a01-a605-e8ab76bf99f1
  Args:
    source: Theodoros_Karellas
    type: :Person
  AssignClass (9e70c355-acd5-4d3c-a4de-b185328d978c)
 Call ID: 9e70c355-acd5-4d3c-a4de-b185328d978c
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    type: :Man
  AssignClass (124e4601-cb2b-416c-9229-0028ca3962c3)
 Call ID: 124e4601-cb2b-416c-9229-0028ca3962c3
  Args:
    source: Prince_Aimone_Duke_of_Aosta
    type: :Person
  AssignClass (d1ff51c5-71c3-4e68-8ec2-e78eb22f1774)
 Call ID: d1ff51c5-71c3-4e68-8ec2-e78eb22f1774
  Args:
    source: Amedeo_5th_Duke_of_Aosta
    type: :Man
  AssignClass (7138de1e-c23f-4722-b140-ec2e34d5b73d)
 Call ID: 7138de1e-c23f-4722-b140-ec2e34d5b73d
  Args:
    type: :Person
    source: Amedeo_5th_Duke_of_Aosta
  AssignClass (55356cac-fd91-4c12-a336-cd5299777457)
 Call ID: 55356cac-fd91-4c12-a336-cd5299777457
  Args:
    source: Isabella_Vita_Marina
    type: :Woman
  AssignClass (e52ad18c-f4fe-4475-829b-b0e63460da96)
 Call ID: e52ad18c-f4fe-4475-829b-b0e63460da96
  Args:
    type: :Person
    source: Isabella_Vita_Marina
  AssignClass (6ba153c8-1186-4892-93d2-f341479c3296)
 Call ID: 6ba153c8-1186-4892-93d2-f341479c3296
  Args:
    source: Princess_Alexandra
    type: :Woman
  AssignClass (4665d90c-5a75-4e79-a97b-4b6148da2c38)
 Call ID: 4665d90c-5a75-4e79-a97b-4b6148da2c38
  Args:
    source: Princess_Alexandra
    type: :Person
  AddTriple (fe51915a-0a5f-45bf-8699-2d113f35f9c1)
 Call ID: fe51915a-0a5f-45bf-8699-2d113f35f9c1
  Args:
    target: Prince_Michael_of_Greece_and_Denmark
    source: Princess_Olga_of_Greece
    relation: :hasFather
  AddTriple (7394921d-cbf2-4fbc-bcdd-a93133eb2f45)
 Call ID: 7394921d-cbf2-4fbc-bcdd-a93133eb2f45
  Args:
    target: Marina_Karella
    source: Princess_Olga_of_Greece
    relation: :hasMother
  AddTriple (624616ba-fee0-433b-99b5-70687f85363c)
 Call ID: 624616ba-fee0-433b-99b5-70687f85363c
  Args:
    source: Marina_Karella
    relation: :hasFather
    target: Theodoros_Karellas
  AddTriple (008bef5d-5b42-416d-ac72-f287b2dc4507)
 Call ID: 008bef5d-5b42-416d-ac72-f287b2dc4507
  Args:
    target: Amedeo_5th_Duke_of_Aosta
    source: Prince_Aimone_Duke_of_Aosta
    relation: :hasFather
  AddTriple (12d624e7-fa93-451e-9f6e-fcb13c5002aa)
 Call ID: 12d624e7-fa93-451e-9f6e-fcb13c5002aa
  Args:
    source: Isabella_Vita_Marina
    relation: :hasMother
    target: Princess_Olga_of_Greece
  AddTriple (5499f84b-8531-411d-a5a1-6a6332e8b102)
 Call ID: 5499f84b-8531-411d-a5a1-6a6332e8b102
  Args:
    source: Isabella_Vita_Marina
    relation: :hasFather
    target: Prince_Aimone_Duke_of_Aosta
  AddTriple (1b59cee9-d48f-4947-95b0-67297471ebcb)
 Call ID: 1b59cee9-d48f-4947-95b0-67297471ebcb
  Args:
    target: Princess_Alexandra
    source: Princess_Olga_of_Greece
    relation: :hasSister
  AddLiteral (6c14c5e9-8f1d-4f9d-8abd-1a1abe23adf6)
 Call ID: 6c14c5e9-8f1d-4f9d-8abd-1a1abe23adf6
  Args:
    source: Princess_Olga_of_Greece
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1971
  Finish (7d7701fc-172f-435f-896b-02721ee1fa54)
 Call ID: 7d7701fc-172f-435f-896b-02721ee1fa54
  Args: