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
Prince Nikola of Yugoslavia (29 June 1928 – 12 April 1954), also known in Britain as Prince Nicholas and in Serbia as Nikola Karađorđević (Serbian Cyrillic: Никола Карађорђевић), was the younger son of Prince Paul of Yugoslavia by his wife Princess Olga of Greece and Denmark.
Biography

Prince Nikola was born into the House of Karađorđević, the dynasty that ruled Serbia and later the Kingdom of Yugoslavia.
Known as "Nicky", he was educated in England at Oxford University and was a frequent social escort to Princess Margaret, sister of Queen Elizabeth II.
Prince Nikola died unmarried in 1954, survived by his parents, Prince Paul and Princess Olga of Yugoslavia; older brother Prince Alexander and younger sister, Princess Elizabeth; also his maternal grandmother, Grand Duchess Elena Vladimirovna of Russia (Princess Nicholas of Greece and Denmark) and his maternal aunts, Princess Elizabeth, Countess of Toerring-Jettenbach, and Princess Marina, Duchess of Kent.
Death

Nikola died in a road accident at Datchet, now in Berkshire, England, some five miles from the home of his aunt, the Duchess of Kent.
He was
driving himself alone towards London, on his way to a meeting with Princess Margaret the same evening, to attend a full-dress rehearsal of a play being performed by a group of young socialites.
He was a paternal grandson of Arsen Karađorđević, Prince of Serbia and Princess Aurora Pavlovna Demidova di San Donato.
He was a maternal grandson of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.



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
  AssignClass (af41e817-40cd-4bfc-83f8-2d77f45fbbb2)
 Call ID: af41e817-40cd-4bfc-83f8-2d77f45fbbb2
  Args:
    type: :Man
    source: Prince_Nikola_of_Yugoslavia
  AssignClass (82aea08b-90e9-418e-9891-b10024a1ece1)
 Call ID: 82aea08b-90e9-418e-9891-b10024a1ece1
  Args:
    type: :Person
    source: Prince_Nikola_of_Yugoslavia
  AddLiteral (fc2888ba-5c1e-4b77-958c-dc631d1cdb78)
 Call ID: fc2888ba-5c1e-4b77-958c-dc631d1cdb78
  Args:
    literal_type: xsd:integer
    literal_value: 1928
    source: Prince_Nikola_of_Yugoslavia
    relation: :hasBirthYear
  AddLiteral (f5b918d0-ae2a-4544-8ee6-03a63d294e38)
 Call ID: f5b918d0-ae2a-4544-8ee6-03a63d294e38
  Args:
    source: Prince_Nikola_of_Yugoslavia
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1954
  AddLiteral (1a3c6b08-5fc3-4032-8448-5a87c0bc8a17)
 Call ID: 1a3c6b08-5fc3-4032-8448-5a87c0bc8a17
  Args:
    literal_value: Prince Nicholas
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Prince_Nikola_of_Yugoslavia
  AddLiteral (1ac02bee-7ea8-4376-bbf7-9692ce0d52b3)
 Call ID: 1ac02bee-7ea8-4376-bbf7-9692ce0d52b3
  Args:
    literal_value: Nikola Karađorđević
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Prince_Nikola_of_Yugoslavia
  AddLiteral (7722098d-e67c-4e78-a177-0486dbd99373)
 Call ID: 7722098d-e67c-4e78-a177-0486dbd99373
  Args:
    literal_type: xsd:string
    literal_value: Nicky
    source: Prince_Nikola_of_Yugoslavia
    relation: :knownAs
  AssignClass (ef21362a-4d46-4134-8ac3-a6da142bf673)
 Call ID: ef21362a-4d46-4134-8ac3-a6da142bf673
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (acdd9a9b-8d6b-40a6-be8a-028eb950f7f8)
 Call ID: acdd9a9b-8d6b-40a6-be8a-028eb950f7f8
  Args:
    type: :Person
    source: Prince_Paul_of_Yugoslavia
  AssignClass (f31f232a-ccc8-442a-ae4f-b29cc2ed24c4)
 Call ID: f31f232a-ccc8-442a-ae4f-b29cc2ed24c4
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (b6cad7dc-49f3-40fa-a600-df6e2d5e28e2)
 Call ID: b6cad7dc-49f3-40fa-a600-df6e2d5e28e2
  Args:
    type: :Person
    source: Princess_Olga_of_Greece_and_Denmark
  AddTriple (0f1c0c68-5e83-4d95-8c5b-f18b8ff8581c)
 Call ID: 0f1c0c68-5e83-4d95-8c5b-f18b8ff8581c
  Args:
    target: Prince_Paul_of_Yugoslavia
    relation: :hasFather
    source: Prince_Nikola_of_Yugoslavia
  AddTriple (370e2f46-26fd-421f-be5b-89e1a487311b)
 Call ID: 370e2f46-26fd-421f-be5b-89e1a487311b
  Args:
    source: Prince_Nikola_of_Yugoslavia
    relation: :hasMother
    target: Princess_Olga_of_Greece_and_Denmark
  AssignClass (ed37e762-ae82-40ad-a088-2759178bf112)
 Call ID: ed37e762-ae82-40ad-a088-2759178bf112
  Args:
    type: :Man
    source: Prince_Alexander
  AssignClass (4dc9c03c-bbb8-4737-b944-fab2db62c007)
 Call ID: 4dc9c03c-bbb8-4737-b944-fab2db62c007
  Args:
    type: :Person
    source: Prince_Alexander
  AddTriple (35414c7a-6e94-40c7-ab26-726859d71a99)
 Call ID: 35414c7a-6e94-40c7-ab26-726859d71a99
  Args:
    source: Prince_Nikola_of_Yugoslavia
    relation: :hasBrother
    target: Prince_Alexander
  AssignClass (b0606bc0-8d43-44fc-a55a-fa3375d306d7)
 Call ID: b0606bc0-8d43-44fc-a55a-fa3375d306d7
  Args:
    type: :Woman
    source: Princess_Elizabeth
  AssignClass (a4eb38eb-43ac-431a-8c11-c14c662113f3)
 Call ID: a4eb38eb-43ac-431a-8c11-c14c662113f3
  Args:
    type: :Person
    source: Princess_Elizabeth
  AddTriple (317d2f2c-e969-4e2d-aee0-6b4bbe6df0d5)
 Call ID: 317d2f2c-e969-4e2d-aee0-6b4bbe6df0d5
  Args:
    relation: :hasSister
    target: Princess_Elizabeth
    source: Prince_Nikola_of_Yugoslavia
  AssignClass (a2d42d70-cb30-4c21-a7f2-6f5e2c539e61)
 Call ID: a2d42d70-cb30-4c21-a7f2-6f5e2c539e61
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (9a756d3c-7b01-4141-82ec-bae5d056e874)
 Call ID: 9a756d3c-7b01-4141-82ec-bae5d056e874
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (76aa49ee-90ce-4640-81ea-353e8d581580)
 Call ID: 76aa49ee-90ce-4640-81ea-353e8d581580
  Args:
    type: :Woman
    source: Princess_Elizabeth_Countess_of_Toerring_Jettenbach
  AssignClass (5f6cb88f-95b4-41ab-bc13-c00f35d85fdb)
 Call ID: 5f6cb88f-95b4-41ab-bc13-c00f35d85fdb
  Args:
    type: :Person
    source: Princess_Elizabeth_Countess_of_Toerring_Jettenbach
  AssignClass (ed4f6d38-91d4-428a-9994-7fd1c55fd78e)
 Call ID: ed4f6d38-91d4-428a-9994-7fd1c55fd78e
  Args:
    type: :Woman
    source: Princess_Marina_Duchess_of_Kent
  AssignClass (0e62355a-fb0f-4b40-95dd-a7347c2f4777)
 Call ID: 0e62355a-fb0f-4b40-95dd-a7347c2f4777
  Args:
    type: :Person
    source: Princess_Marina_Duchess_of_Kent
  AssignClass (8dcf6a3f-b1a0-4d8d-8dc2-408922e65ba2)
 Call ID: 8dcf6a3f-b1a0-4d8d-8dc2-408922e65ba2
  Args:
    type: :Man
    source: Arsen_Karađorđević
  AssignClass (84324ec6-2e06-4f1d-876e-527a57589c4a)
 Call ID: 84324ec6-2e06-4f1d-876e-527a57589c4a
  Args:
    type: :Person
    source: Arsen_Karađorđević
  AssignClass (4570dde9-146d-4c6e-8409-911f33b48edc)
 Call ID: 4570dde9-146d-4c6e-8409-911f33b48edc
  Args:
    type: :Woman
    source: Princess_Aurora_Pavlovna_Demidova_di_San_Donato
  AssignClass (ffe2e8c0-bf33-4094-9525-36c376bc61e2)
 Call ID: ffe2e8c0-bf33-4094-9525-36c376bc61e2
  Args:
    type: :Person
    source: Princess_Aurora_Pavlovna_Demidova_di_San_Donato
  AssignClass (73cf7420-a4e0-4813-b558-2d705c15aad2)
 Call ID: 73cf7420-a4e0-4813-b558-2d705c15aad2
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (acbd129e-28a8-458d-b5d1-f23b857427d8)
 Call ID: acbd129e-28a8-458d-b5d1-f23b857427d8
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (f488ab95-a550-4329-85b4-c69587c3b356)
 Call ID: f488ab95-a550-4329-85b4-c69587c3b356
  Args:
    relation: :hasFather
    target: Arsen_Karađorđević
    source: Prince_Paul_of_Yugoslavia
  AddTriple (d6662bfc-df86-4bd2-9072-18fb45e746a6)
 Call ID: d6662bfc-df86-4bd2-9072-18fb45e746a6
  Args:
    source: Prince_Paul_of_Yugoslavia
    relation: :hasMother
    target: Princess_Aurora_Pavlovna_Demidova_di_San_Donato
  AddTriple (0368c8ea-a1a2-4289-837c-529286645b3b)
 Call ID: 0368c8ea-a1a2-4289-837c-529286645b3b
  Args:
    relation: :hasFather
    target: Prince_Nicholas_of_Greece_and_Denmark
    source: Princess_Olga_of_Greece_and_Denmark
  AddTriple (a73511bf-6ce2-45d6-8571-8066124f7870)
 Call ID: a73511bf-6ce2-45d6-8571-8066124f7870
  Args:
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
    source: Princess_Olga_of_Greece_and_Denmark
  Finish (b22e0f9b-2bba-45a2-acdc-0b9fe69cd739)
 Call ID: b22e0f9b-2bba-45a2-acdc-0b9fe69cd739
  Args: