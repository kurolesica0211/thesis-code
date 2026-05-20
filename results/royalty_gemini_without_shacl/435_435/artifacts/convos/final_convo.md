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
India Riven Oxenberg (born June 7, 1991) is an American actress and documentary film producer.
A granddaughter of Princess Elizabeth of Yugoslavia, she is a relative of the House of Karađorđević, the former royal family of Serbia and, later, Yugoslavia.
Oxenberg began her career as a child actress, with small roles in film and television projects that her mother, Catherine Oxenberg, and then-stepfather, Casper Van Dien, were involved in.
As a teenager, she was a cast member of the reality television series I Married a Princess.
From 2011 to 2018, Oxenberg was involved in NXIVM, an American multi-level marketing company that was later exposed as a cult.
Early life and education

Oxenberg was born on June 7, 1991, to actress Catherine Oxenberg and William Weitz Shaffer.
Oxenberg's father was arrested in 1992 for smuggling marijuana from Thailand, reportedly profiting $50 million from drug trading.
Her maternal grandparents are Princess Elizabeth of Yugoslavia and Howard Oxenberg, a Jewish dress manufacturer.
As a great-granddaughter of Prince Regent Paul of Yugoslavia (Elizabeth's father), Oxenberg is a descendant of the House of Karađorđević, which ruled Serbia and Yugoslavia.
Oxenberg is also a relative of the British royal family, the Danish royal family, and the Greek royal family through her great-grandmother, Princess Olga of Greece and Denmark.
She is a niece of writer and fashion designer Christina Oxenberg.
In 2008, Oxenberg was presented to society at Le Bal des débutantes at the Hôtel de Crillon in Paris.
She was one of two descendants of the Karađorđević dynasty to make her debut at Le Bal that year, alongside her cousin Victoria de Silva, the daughter of Princess Katarina and Sir Desmond de Silva.
Career

Oxenberg's first film was the 2001 television drama The Miracle of the Cards.
In 2002, Oxenberg played the role of Mattie in the science fiction television film The Vector File.
Oxenberg was a cast member on the 2005 Lifetime reality television series I Married a Princess, which followed her family while her mother was married to Casper Van Dien.
In 2009, she had a small role in the Disney film Princess Protection Program.
Personal life

In 2018, Oxenberg met Patrick D'Ignazio, a chef, while working as a manager for a restaurant in New York City.
Oxenberg and D’Ignazio had their first child, a girl, in 2024.
NXIVM

After attending college for one year, Oxenberg, alongside her mother, enrolled in a self-help entrepreneurship course hosted by NXIVM, following a recommendation from a family friend.
While they initially started the program together, Oxenberg's mother eventually withdrew.
In January 2015, after five years in NXIVM, Oxenberg was approached by Allison Mack about joining a secret sorority, "DOS".
In DOS, Mack became a mentor to Oxenberg.
Oxenberg was instructed to provide personal family secrets and pose for nude photographs for Mack, who also limited the amount of food Oxenberg could eat and required her to cook and clean for her while living with Mack in Albany, New York.
Throughout this process, Oxenberg was groomed to become a sexual partner for NXIVM's founder and the leader of DOS, Keith Raniere.
In January 2016, Oxenberg was held down and branded with the initials of Raniere.
Oxenberg left NXIVM in 2018.
While Oxenberg was involved in NXIVM, her mother Catherine tried to get her out of the organization and expose the cult through media in 2017.
In 2018, Catherine wrote the book Captive: A Mother's Crusade to Save Her Daughter from a Terrifying Cult.
In 2019, Catherine produced the Lifetime television movie Escaping the NXIVM Cult: A Mother's Fight to Save Her Daughter.
Oxenberg officially left NXIVM in the summer of 2018 and moved back to Malibu with her mother.
Oxenberg's time in the cult was discussed in the HBO 2020 documentary The Vow.
Oxenberg produced and starred in the 2020 Starz documentary series Seduced: Inside the NXIVM Cult.
Oxenberg had her NXIVM brand covered up with a tattoo of a mandala and the inscription "ancora imparo" (i'm still learning) by a tattoo artist in New York City's East Village.



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
  AssignClass (bc57be10-0389-43f2-88ec-f67b6d4907b4)
 Call ID: bc57be10-0389-43f2-88ec-f67b6d4907b4
  Args:
    type: :Person
    source: India Riven Oxenberg
  AssignClass (7ac093a4-d384-41b7-bfbf-5a711e0d8245)
 Call ID: 7ac093a4-d384-41b7-bfbf-5a711e0d8245
  Args:
    type: :Woman
    source: India Riven Oxenberg
  AddLiteral (7f8ecd08-6b47-4f79-9c0e-e2fb3d825af5)
 Call ID: 7f8ecd08-6b47-4f79-9c0e-e2fb3d825af5
  Args:
    relation: :hasBirthYear
    literal_value: 1991
    literal_type: xsd:integer
    source: India Riven Oxenberg
  AssignClass (f6b3f301-23dc-450d-8052-a136620c8453)
 Call ID: f6b3f301-23dc-450d-8052-a136620c8453
  Args:
    type: :Person
    source: Catherine Oxenberg
  AssignClass (72841aae-10c9-4fd1-bfe4-5e52bdc051f9)
 Call ID: 72841aae-10c9-4fd1-bfe4-5e52bdc051f9
  Args:
    source: Catherine Oxenberg
    type: :Woman
  AssignClass (4aca9bc4-a1bb-41e7-879d-dbc9abfaccc2)
 Call ID: 4aca9bc4-a1bb-41e7-879d-dbc9abfaccc2
  Args:
    type: :Ancestor
    source: Catherine Oxenberg
  AddTriple (d7697864-b79c-4e6b-a47b-57317a99b649)
 Call ID: d7697864-b79c-4e6b-a47b-57317a99b649
  Args:
    relation: :hasMother
    target: Catherine Oxenberg
    source: India Riven Oxenberg
  AssignClass (6b535779-db1f-497d-a402-60c7dfa87a21)
 Call ID: 6b535779-db1f-497d-a402-60c7dfa87a21
  Args:
    type: :Person
    source: William Weitz Shaffer
  AssignClass (1973b401-b69b-4a9c-b081-ea65ace2e9ec)
 Call ID: 1973b401-b69b-4a9c-b081-ea65ace2e9ec
  Args:
    source: William Weitz Shaffer
    type: :Man
  AssignClass (de768465-109d-4f2c-9f6e-a9ab1c19d029)
 Call ID: de768465-109d-4f2c-9f6e-a9ab1c19d029
  Args:
    type: :Ancestor
    source: William Weitz Shaffer
  AddTriple (b836a938-970d-4713-942a-3e63f88b8c09)
 Call ID: b836a938-970d-4713-942a-3e63f88b8c09
  Args:
    target: William Weitz Shaffer
    relation: :hasFather
    source: India Riven Oxenberg
  AssignClass (448f31c7-a3a8-4ae8-b4d1-6b7dcb4c2cc5)
 Call ID: 448f31c7-a3a8-4ae8-b4d1-6b7dcb4c2cc5
  Args:
    type: :Person
    source: Princess Elizabeth of Yugoslavia
  AssignClass (38050c0d-117a-491a-815b-ea374d98afec)
 Call ID: 38050c0d-117a-491a-815b-ea374d98afec
  Args:
    type: :Woman
    source: Princess Elizabeth of Yugoslavia
  AssignClass (62b1ceda-cb12-4d4d-86bb-e2616fdab554)
 Call ID: 62b1ceda-cb12-4d4d-86bb-e2616fdab554
  Args:
    source: Princess Elizabeth of Yugoslavia
    type: :Ancestor
  AssignClass (052b437f-5be6-4445-a205-2e67690e2e9c)
 Call ID: 052b437f-5be6-4445-a205-2e67690e2e9c
  Args:
    source: Howard Oxenberg
    type: :Person
  AssignClass (265985ab-12e6-4baa-9368-ad7afd80431f)
 Call ID: 265985ab-12e6-4baa-9368-ad7afd80431f
  Args:
    type: :Man
    source: Howard Oxenberg
  AssignClass (3d8e129a-46a6-4a2a-80d5-3c2efdcf7ec8)
 Call ID: 3d8e129a-46a6-4a2a-80d5-3c2efdcf7ec8
  Args:
    source: Howard Oxenberg
    type: :Ancestor
  AddTriple (dcf0e3f5-5b84-4b44-9ed6-35606a460a89)
 Call ID: dcf0e3f5-5b84-4b44-9ed6-35606a460a89
  Args:
    relation: :hasMother
    target: Princess Elizabeth of Yugoslavia
    source: Catherine Oxenberg
  AddTriple (b08b598f-673f-47ff-811f-96c6ce10807f)
 Call ID: b08b598f-673f-47ff-811f-96c6ce10807f
  Args:
    source: Catherine Oxenberg
    target: Howard Oxenberg
    relation: :hasFather
  AssignClass (f1e3550a-f2af-47e9-a9af-3448d1c03bea)
 Call ID: f1e3550a-f2af-47e9-a9af-3448d1c03bea
  Args:
    source: Prince Regent Paul of Yugoslavia
    type: :Person
  AssignClass (1c86a326-6dd9-4348-9a4e-b69cd1902795)
 Call ID: 1c86a326-6dd9-4348-9a4e-b69cd1902795
  Args:
    type: :Man
    source: Prince Regent Paul of Yugoslavia
  AssignClass (783c29f3-8bcc-4d4c-8759-141e666ea805)
 Call ID: 783c29f3-8bcc-4d4c-8759-141e666ea805
  Args:
    source: Prince Regent Paul of Yugoslavia
    type: :Ancestor
  AddTriple (836d2134-82a5-41fa-8e86-e77a918d2acc)
 Call ID: 836d2134-82a5-41fa-8e86-e77a918d2acc
  Args:
    relation: :hasFather
    target: Prince Regent Paul of Yugoslavia
    source: Princess Elizabeth of Yugoslavia
  AssignClass (1afbcca8-94d2-44a2-85f4-26ee0321f4f2)
 Call ID: 1afbcca8-94d2-44a2-85f4-26ee0321f4f2
  Args:
    source: Princess Olga of Greece and Denmark
    type: :Person
  AssignClass (18c55adb-8314-468e-b636-371f645c3f58)
 Call ID: 18c55adb-8314-468e-b636-371f645c3f58
  Args:
    source: Princess Olga of Greece and Denmark
    type: :Woman
  AssignClass (866b6c0d-0a33-41c5-9f67-c3d6a467d8a7)
 Call ID: 866b6c0d-0a33-41c5-9f67-c3d6a467d8a7
  Args:
    type: :Ancestor
    source: Princess Olga of Greece and Denmark
  AddTriple (169eebe2-99fe-478a-b972-46799ed9a02e)
 Call ID: 169eebe2-99fe-478a-b972-46799ed9a02e
  Args:
    source: Princess Elizabeth of Yugoslavia
    target: Princess Olga of Greece and Denmark
    relation: :hasMother
  AssignClass (87e1b5be-c251-4d29-8c45-b92140de28cf)
 Call ID: 87e1b5be-c251-4d29-8c45-b92140de28cf
  Args:
    type: :Person
    source: Christina Oxenberg
  AssignClass (d050cc43-bc22-4be5-963d-1a5ebc8c6fcf)
 Call ID: d050cc43-bc22-4be5-963d-1a5ebc8c6fcf
  Args:
    type: :Woman
    source: Christina Oxenberg
  AddTriple (21e552d1-0174-4b64-8000-2dea632f8482)
 Call ID: 21e552d1-0174-4b64-8000-2dea632f8482
  Args:
    source: Christina Oxenberg
    target: Catherine Oxenberg
    relation: :isSisterOf
  AssignClass (cfd17143-a18b-494a-822c-44b457b2c601)
 Call ID: cfd17143-a18b-494a-822c-44b457b2c601
  Args:
    type: :Person
    source: Casper Van Dien
  AssignClass (64f926e9-bc19-4a7f-9d92-17028f72df8c)
 Call ID: 64f926e9-bc19-4a7f-9d92-17028f72df8c
  Args:
    source: Casper Van Dien
    type: :Man
  AssignClass (1abf15dd-4614-4f0e-9ba1-80b9a15651ee)
 Call ID: 1abf15dd-4614-4f0e-9ba1-80b9a15651ee
  Args:
    source: Victoria de Silva
    type: :Person
  AssignClass (9bb50d32-6492-450d-a430-11e8775f9a5b)
 Call ID: 9bb50d32-6492-450d-a430-11e8775f9a5b
  Args:
    source: Victoria de Silva
    type: :Woman
  AssignClass (00daa5c0-802e-4c43-a657-348ab6207803)
 Call ID: 00daa5c0-802e-4c43-a657-348ab6207803
  Args:
    type: :Person
    source: Princess Katarina
  AssignClass (e5feb102-9c50-4946-8004-e06bf62ae5f2)
 Call ID: e5feb102-9c50-4946-8004-e06bf62ae5f2
  Args:
    type: :Woman
    source: Princess Katarina
  AssignClass (ab391209-5206-4d77-b48e-a1dca7bc0e84)
 Call ID: ab391209-5206-4d77-b48e-a1dca7bc0e84
  Args:
    type: :Ancestor
    source: Princess Katarina
  AssignClass (b14aff24-780f-493e-a784-3d58802ef65f)
 Call ID: b14aff24-780f-493e-a784-3d58802ef65f
  Args:
    type: :Person
    source: Sir Desmond de Silva
  AssignClass (f4a38b21-cbf5-498e-8d97-4af8879954d9)
 Call ID: f4a38b21-cbf5-498e-8d97-4af8879954d9
  Args:
    source: Sir Desmond de Silva
    type: :Man
  AssignClass (b31d28f6-4082-4117-968c-d69e2e782ab2)
 Call ID: b31d28f6-4082-4117-968c-d69e2e782ab2
  Args:
    type: :Ancestor
    source: Sir Desmond de Silva
  AddTriple (acd1819a-b426-40fd-bc2f-e0cd8842668e)
 Call ID: acd1819a-b426-40fd-bc2f-e0cd8842668e
  Args:
    source: Victoria de Silva
    relation: :hasMother
    target: Princess Katarina
  AddTriple (7387dc24-c5eb-4c8e-b3af-2a3c044653a5)
 Call ID: 7387dc24-c5eb-4c8e-b3af-2a3c044653a5
  Args:
    source: Victoria de Silva
    target: Sir Desmond de Silva
    relation: :hasFather
  AssignClass (9d06b12d-3d20-4723-a98f-ebed51a59cb4)
 Call ID: 9d06b12d-3d20-4723-a98f-ebed51a59cb4
  Args:
    source: Patrick D'Ignazio
    type: :Person
  AssignClass (0ae6ab2c-6273-48e2-bed8-6146422a8de0)
 Call ID: 0ae6ab2c-6273-48e2-bed8-6146422a8de0
  Args:
    type: :Man
    source: Patrick D'Ignazio
  AssignClass (b5749baf-dfa1-483d-98f9-8cab49a0eb3b)
 Call ID: b5749baf-dfa1-483d-98f9-8cab49a0eb3b
  Args:
    type: :Person
    source: India Riven Oxenberg's daughter
  AssignClass (5bff8e22-e8fd-4bcb-b97b-e583fc0c902f)
 Call ID: 5bff8e22-e8fd-4bcb-b97b-e583fc0c902f
  Args:
    source: India Riven Oxenberg's daughter
    type: :Woman
  AddTriple (a4182e97-28b7-49e6-a803-e141fb54e19f)
 Call ID: a4182e97-28b7-49e6-a803-e141fb54e19f
  Args:
    source: India Riven Oxenberg's daughter
    relation: :hasMother
    target: India Riven Oxenberg
  AddTriple (b4debf93-baec-4ac9-ac03-476e7e706e5a)
 Call ID: b4debf93-baec-4ac9-ac03-476e7e706e5a
  Args:
    relation: :hasFather
    target: Patrick D'Ignazio
    source: India Riven Oxenberg's daughter
  Finish (0d3e8a8d-ac8a-4627-9097-17c01049fdb4)
 Call ID: 0d3e8a8d-ac8a-4627-9097-17c01049fdb4
  Args: