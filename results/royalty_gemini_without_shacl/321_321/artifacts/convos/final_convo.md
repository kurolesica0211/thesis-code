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
Duchess Donata of Mecklenburg (born 11 March 1956) is the senior remaining member of the House of Mecklenburg-Schwerin.
Since there are no males left in the family, the Schwerin branch itself is considered extinct due to the Salic law of succession, leaving Mecklenburg-Strelitz as the only remaining line of the House of Mecklenburg.
Duchess of Mecklenburg

She was born in Kiel in the state of Schleswig-Holstein the eldest daughter of Duke Christian Louis of Mecklenburg-Schwerin and his wife Princess Barbara of Prussia (1920-1994).
Her father was the younger brother to the last surviving male of the House of Mecklenburg-Schwerin, Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin.
Her mother was the daughter of Princess Charlotte of Saxe-Altenburg, the eldest daughter of Ernst II, the last duke of Saxe-Altenburg.
Donata had only one sister Edwina (born 25 September 1960), and as her uncle had no children the House of Mecklenburg-Schwerin became extinct in the male line in 2001 when her uncle died.
As a result, the Mecklenburg-Strelitz line, headed by Borwin, Duke of Mecklenburg, will become the only surviving line of the House of Mecklenburg when both Donata and Edwina are dead.
Her paternal grandfather was the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
She is also a descendant of Christian IX of Denmark as her paternal grandmother, Alexandra of Hanover and Cumberland, a daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark, was the youngest daughter and fifth child of Christian IX of Denmark and Louise of Hesse-Kassel.
Her maternal grandfather was Prince Sigismund of Prussia, a grandson of Grand Duke Louis IV and Alice, Grand Duchess of Hesse and by Rhine, the second daughter of Queen Victoria.



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
  AssignClass (64b16b8f-adaa-4bd0-bcbe-bb16c18c68f8)
 Call ID: 64b16b8f-adaa-4bd0-bcbe-bb16c18c68f8
  Args:
    source: DonataOfMecklenburg
    type: :Woman
  AssignClass (1119a672-cfa4-4123-b72a-03da0ba3400b)
 Call ID: 1119a672-cfa4-4123-b72a-03da0ba3400b
  Args:
    type: :Person
    source: DonataOfMecklenburg
  AddLiteral (d5570cc8-1df7-4e4f-80ad-d96e6d202cce)
 Call ID: d5570cc8-1df7-4e4f-80ad-d96e6d202cce
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: DonataOfMecklenburg
    literal_value: 1956
  AssignClass (a37de5d7-0157-412d-82a0-856aa2c59321)
 Call ID: a37de5d7-0157-412d-82a0-856aa2c59321
  Args:
    type: :Man
    source: ChristianLouisOfMecklenburgSchwerin
  AssignClass (4e2737fd-27be-467a-8475-0e748eff16d0)
 Call ID: 4e2737fd-27be-467a-8475-0e748eff16d0
  Args:
    source: ChristianLouisOfMecklenburgSchwerin
    type: :Person
  AssignClass (f5e24e60-f414-492f-bbaf-afa5d3569a73)
 Call ID: f5e24e60-f414-492f-bbaf-afa5d3569a73
  Args:
    type: :Woman
    source: BarbaraOfPrussia
  AssignClass (7b14d7f1-4407-46b8-b5b3-b2c18712f844)
 Call ID: 7b14d7f1-4407-46b8-b5b3-b2c18712f844
  Args:
    source: BarbaraOfPrussia
    type: :Person
  AddLiteral (bf17b019-3d7b-49e0-8421-9db69c8d6a2f)
 Call ID: bf17b019-3d7b-49e0-8421-9db69c8d6a2f
  Args:
    relation: :hasBirthYear
    source: BarbaraOfPrussia
    literal_type: xsd:integer
    literal_value: 1920
  AddLiteral (0535609b-37f7-4a97-b8a6-15bbf0251f4f)
 Call ID: 0535609b-37f7-4a97-b8a6-15bbf0251f4f
  Args:
    literal_value: 1994
    relation: :hasDeathYear
    source: BarbaraOfPrussia
    literal_type: xsd:integer
  AddTriple (6efb625d-e413-4a4b-8c06-618fa693a625)
 Call ID: 6efb625d-e413-4a4b-8c06-618fa693a625
  Args:
    target: ChristianLouisOfMecklenburgSchwerin
    relation: :hasFather
    source: DonataOfMecklenburg
  AddTriple (72df175a-dbe6-4aa1-8cdf-04b5548fcbe0)
 Call ID: 72df175a-dbe6-4aa1-8cdf-04b5548fcbe0
  Args:
    source: DonataOfMecklenburg
    target: BarbaraOfPrussia
    relation: :hasMother
  AssignClass (f23b48ec-7d0b-4ae0-89f3-b66d7d2111eb)
 Call ID: f23b48ec-7d0b-4ae0-89f3-b66d7d2111eb
  Args:
    type: :Man
    source: FriedrichFranzOfMecklenburgSchwerin
  AssignClass (48af26bf-fa2e-4918-85d4-a9e639131f61)
 Call ID: 48af26bf-fa2e-4918-85d4-a9e639131f61
  Args:
    source: FriedrichFranzOfMecklenburgSchwerin
    type: :Person
  AddTriple (7c33ee09-c332-451a-b897-ab4cce32aec6)
 Call ID: 7c33ee09-c332-451a-b897-ab4cce32aec6
  Args:
    source: ChristianLouisOfMecklenburgSchwerin
    target: FriedrichFranzOfMecklenburgSchwerin
    relation: :isBrotherOf
  AssignClass (c0335d8b-4949-435b-9fa8-954281f22d31)
 Call ID: c0335d8b-4949-435b-9fa8-954281f22d31
  Args:
    source: EdwinaOfMecklenburg
    type: :Woman
  AssignClass (49be7d1b-4a01-4a13-8c00-bca99d4e05ab)
 Call ID: 49be7d1b-4a01-4a13-8c00-bca99d4e05ab
  Args:
    type: :Person
    source: EdwinaOfMecklenburg
  AddLiteral (6e6da8a4-fe11-4f2e-add8-114529e6908b)
 Call ID: 6e6da8a4-fe11-4f2e-add8-114529e6908b
  Args:
    relation: :hasBirthYear
    source: EdwinaOfMecklenburg
    literal_type: xsd:integer
    literal_value: 1960
  AddTriple (ed88d6be-71b9-4dfc-bc0f-8b492b0ccf41)
 Call ID: ed88d6be-71b9-4dfc-bc0f-8b492b0ccf41
  Args:
    source: EdwinaOfMecklenburg
    target: DonataOfMecklenburg
    relation: :isSisterOf
  AddTriple (00dafacb-97f8-41ad-9318-5fb2a18a4a41)
 Call ID: 00dafacb-97f8-41ad-9318-5fb2a18a4a41
  Args:
    source: EdwinaOfMecklenburg
    target: ChristianLouisOfMecklenburgSchwerin
    relation: :hasFather
  AddTriple (d28e96e9-29f3-49ee-abfc-c6673acab09f)
 Call ID: d28e96e9-29f3-49ee-abfc-c6673acab09f
  Args:
    source: EdwinaOfMecklenburg
    target: BarbaraOfPrussia
    relation: :hasMother
  AssignClass (a703c2c0-2ba1-4bd1-aaec-9326479d70e5)
 Call ID: a703c2c0-2ba1-4bd1-aaec-9326479d70e5
  Args:
    type: :Woman
    source: CharlotteOfSaxeAltenburg
  AssignClass (67255e5a-bfcf-41b6-a7ae-59057becd323)
 Call ID: 67255e5a-bfcf-41b6-a7ae-59057becd323
  Args:
    type: :Person
    source: CharlotteOfSaxeAltenburg
  AddTriple (89bd85ba-43b3-4e4b-8636-77bfc4ac5056)
 Call ID: 89bd85ba-43b3-4e4b-8636-77bfc4ac5056
  Args:
    target: BarbaraOfPrussia
    relation: :isMotherOf
    source: CharlotteOfSaxeAltenburg
  AssignClass (e206a6d7-6319-4140-bef8-7592382eef59)
 Call ID: e206a6d7-6319-4140-bef8-7592382eef59
  Args:
    type: :Man
    source: ErnstIIOfSaxeAltenburg
  AssignClass (4c197d20-0334-46c7-a57d-200a36e83660)
 Call ID: 4c197d20-0334-46c7-a57d-200a36e83660
  Args:
    source: ErnstIIOfSaxeAltenburg
    type: :Person
  AddTriple (242255d3-c2ad-4ac0-bc55-2dfb55b50a75)
 Call ID: 242255d3-c2ad-4ac0-bc55-2dfb55b50a75
  Args:
    relation: :isFatherOf
    target: CharlotteOfSaxeAltenburg
    source: ErnstIIOfSaxeAltenburg
  AssignClass (e02da58d-b5a9-4793-837a-622ab94cb119)
 Call ID: e02da58d-b5a9-4793-837a-622ab94cb119
  Args:
    type: :Man
    source: FrederickFrancisIVOfMecklenburgSchwerin
  AssignClass (f4a1322e-ff32-45c9-897c-fd370dccad96)
 Call ID: f4a1322e-ff32-45c9-897c-fd370dccad96
  Args:
    type: :Person
    source: FrederickFrancisIVOfMecklenburgSchwerin
  AddTriple (c514f359-8629-4809-90cc-803b97551188)
 Call ID: c514f359-8629-4809-90cc-803b97551188
  Args:
    source: FrederickFrancisIVOfMecklenburgSchwerin
    relation: :isFatherOf
    target: ChristianLouisOfMecklenburgSchwerin
  AssignClass (8ca06e76-ad6e-491d-80d2-deadabba6fcc)
 Call ID: 8ca06e76-ad6e-491d-80d2-deadabba6fcc
  Args:
    type: :Man
    source: ChristianIXOfDenmark
  AssignClass (315792ad-c488-40d4-acbe-1ca9ae94b8e4)
 Call ID: 315792ad-c488-40d4-acbe-1ca9ae94b8e4
  Args:
    source: ChristianIXOfDenmark
    type: :Person
  AssignClass (1fc691d8-d4e3-40b3-b4a3-e76940f94a1e)
 Call ID: 1fc691d8-d4e3-40b3-b4a3-e76940f94a1e
  Args:
    type: :Woman
    source: AlexandraOfHanoverAndCumberland
  AssignClass (0b8528e3-6d89-4e68-a321-a10e0c8964b1)
 Call ID: 0b8528e3-6d89-4e68-a321-a10e0c8964b1
  Args:
    type: :Person
    source: AlexandraOfHanoverAndCumberland
  AddTriple (f6b6d700-60a1-40af-9a5d-1cbfd82fa7cc)
 Call ID: f6b6d700-60a1-40af-9a5d-1cbfd82fa7cc
  Args:
    relation: :isMotherOf
    target: ChristianLouisOfMecklenburgSchwerin
    source: AlexandraOfHanoverAndCumberland
  AssignClass (24ad6e01-4b1d-411b-b928-8c3c154b3aeb)
 Call ID: 24ad6e01-4b1d-411b-b928-8c3c154b3aeb
  Args:
    source: ErnestAugustusCrownPrinceOfHanover
    type: :Man
  AssignClass (b7eebbec-1be7-4c0f-8a47-6ca2bac8d34f)
 Call ID: b7eebbec-1be7-4c0f-8a47-6ca2bac8d34f
  Args:
    type: :Person
    source: ErnestAugustusCrownPrinceOfHanover
  AssignClass (7d9990ed-6076-4658-aa54-2607a49cf9aa)
 Call ID: 7d9990ed-6076-4658-aa54-2607a49cf9aa
  Args:
    source: ThyraOfDenmark
    type: :Woman
  AssignClass (b52ff313-cb29-44e2-af2e-9f4526c49dde)
 Call ID: b52ff313-cb29-44e2-af2e-9f4526c49dde
  Args:
    source: ThyraOfDenmark
    type: :Person
  AddTriple (de8d14a9-16f5-4ef8-b2d0-6f42ec1f389c)
 Call ID: de8d14a9-16f5-4ef8-b2d0-6f42ec1f389c
  Args:
    relation: :isFatherOf
    target: AlexandraOfHanoverAndCumberland
    source: ErnestAugustusCrownPrinceOfHanover
  AddTriple (e693986e-f3c2-42ca-b9b3-428f79de0361)
 Call ID: e693986e-f3c2-42ca-b9b3-428f79de0361
  Args:
    source: ThyraOfDenmark
    target: AlexandraOfHanoverAndCumberland
    relation: :isMotherOf
  AssignClass (9f75253d-b908-4d6e-a1bf-b1b08baba71a)
 Call ID: 9f75253d-b908-4d6e-a1bf-b1b08baba71a
  Args:
    source: LouiseOfHesseKassel
    type: :Woman
  AssignClass (733bd64f-6bf8-4373-8f12-6dd760929821)
 Call ID: 733bd64f-6bf8-4373-8f12-6dd760929821
  Args:
    type: :Person
    source: LouiseOfHesseKassel
  AddTriple (d41f6b41-d19b-467e-9144-7fe2fdff3302)
 Call ID: d41f6b41-d19b-467e-9144-7fe2fdff3302
  Args:
    source: ChristianIXOfDenmark
    target: ThyraOfDenmark
    relation: :isFatherOf
  AddTriple (1be8fa00-6a4e-40ad-81c1-db6b2483b2bb)
 Call ID: 1be8fa00-6a4e-40ad-81c1-db6b2483b2bb
  Args:
    target: ThyraOfDenmark
    relation: :isMotherOf
    source: LouiseOfHesseKassel
  AssignClass (c996a115-c727-4560-96b1-16ca80b41dca)
 Call ID: c996a115-c727-4560-96b1-16ca80b41dca
  Args:
    source: SigismundOfPrussia
    type: :Man
  AssignClass (7e1ec2c5-d041-4f7b-8f83-1c0606eb119f)
 Call ID: 7e1ec2c5-d041-4f7b-8f83-1c0606eb119f
  Args:
    type: :Person
    source: SigismundOfPrussia
  AddTriple (aa5cc623-6e8b-4a0a-9748-2d482d08f9fa)
 Call ID: aa5cc623-6e8b-4a0a-9748-2d482d08f9fa
  Args:
    target: BarbaraOfPrussia
    relation: :isFatherOf
    source: SigismundOfPrussia
  AssignClass (44591ef1-4856-48aa-b372-5234090ea72b)
 Call ID: 44591ef1-4856-48aa-b372-5234090ea72b
  Args:
    type: :Man
    source: LouisIVOfHesse
  AssignClass (f9db6820-8f3f-4c4a-a475-0f26cf01ad0a)
 Call ID: f9db6820-8f3f-4c4a-a475-0f26cf01ad0a
  Args:
    type: :Person
    source: LouisIVOfHesse
  AssignClass (1367093d-b4f3-4670-917d-0387a1875f88)
 Call ID: 1367093d-b4f3-4670-917d-0387a1875f88
  Args:
    type: :Woman
    source: AliceOfHesseAndByRhine
  AssignClass (8f52c3cd-7828-4698-a5b8-3becbfadff41)
 Call ID: 8f52c3cd-7828-4698-a5b8-3becbfadff41
  Args:
    source: AliceOfHesseAndByRhine
    type: :Person
  AssignClass (62026d0f-e604-48a4-831c-a06487e78a7f)
 Call ID: 62026d0f-e604-48a4-831c-a06487e78a7f
  Args:
    type: :Woman
    source: QueenVictoria
  AssignClass (7006b21a-b057-4fd1-a082-1be132a6c6d1)
 Call ID: 7006b21a-b057-4fd1-a082-1be132a6c6d1
  Args:
    source: QueenVictoria
    type: :Person
  AddTriple (0dec43ac-cfa6-47e9-a5f9-07c5c1430c53)
 Call ID: 0dec43ac-cfa6-47e9-a5f9-07c5c1430c53
  Args:
    target: AliceOfHesseAndByRhine
    relation: :isFatherOf
    source: QueenVictoria
  AddTriple (fe4300fe-9a39-46d0-b6b4-b38cc4010e30)
 Call ID: fe4300fe-9a39-46d0-b6b4-b38cc4010e30
  Args:
    source: LouisIVOfHesse
    target: SigismundOfPrussia
    relation: :isFatherOf
  AddTriple (18fe3a79-7bfb-4db9-832c-dfe93e726102)
 Call ID: 18fe3a79-7bfb-4db9-832c-dfe93e726102
  Args:
    source: AliceOfHesseAndByRhine
    target: SigismundOfPrussia
    relation: :isMotherOf
  Finish (f55a5b4c-8a37-40e1-aca6-9ad313b32508)
 Call ID: f55a5b4c-8a37-40e1-aca6-9ad313b32508
  Args: