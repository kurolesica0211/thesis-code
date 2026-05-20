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
Princess Alexandra of Hanover (Alexandra Louise Marie Olga Elisabeth Therese Vera; 29 September 1882 – 30 August 1963) was Grand Duchess of Mecklenburg-Schwerin as the wife of Grand Duke Frederick Francis IV from their marriage on 7 June 1904 until the Grand Duke abdicated on 14 November 1918, following the German Revolution of 1918.
Alexandra was the daughter of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark.
Family

Alexandra was the second eldest daughter and third child of Ernest Augustus, Crown Prince of Hanover (1845–1923) and Princess Thyra of Denmark (1853–1933), the youngest daughter of Christian IX of Denmark (1818–1906) and Louise of Hesse-Kassel (1817–1898).
Alexandra was a great-great-granddaughter of George III of the United Kingdom (1738–1820) and Charlotte of Mecklenburg-Strelitz (1744–1818).
Marriage and issue

Alexandra married on 7 June 1904 in Gmunden, Austria-Hungary to Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin (1882–1945), son of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin and his wife Grand Duchess Anastasia Mikhailovna of Russia.
The bridegroom gave Alexandra a diamond and aquamarine tiara by Faberge.
Alexandra and Frederick Francis had five children:


Grand Duchess of Mecklenburg-Schwerin

In 1913, a fire broke out at Schwerin Castle while the Grand Duke and Duchess were dining there with guests.
Later life

After the Grand Duke's forced abdication in 1918, the family briefly went into exile in Denmark, the native country of Alexandra's mother, Princess Thyra.
After his death in 1945, the widowed Alexandra retired to the Glucksburg family estates in Schleswig-Holstein.



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
  AssignClass (7841502e-7ad7-452e-b146-1e5b71e347e2)
 Call ID: 7841502e-7ad7-452e-b146-1e5b71e347e2
  Args:
    source: Alexandra_of_Hanover
    type: :Person
  AssignClass (62f38880-be05-42e6-90b6-e8e6c9c073ec)
 Call ID: 62f38880-be05-42e6-90b6-e8e6c9c073ec
  Args:
    source: Alexandra_of_Hanover
    type: :Woman
  AddLiteral (12de1ae3-f8b8-445a-a1e5-e834724a8947)
 Call ID: 12de1ae3-f8b8-445a-a1e5-e834724a8947
  Args:
    relation: :hasBirthYear
    literal_value: 1882
    source: Alexandra_of_Hanover
    literal_type: xsd:integer
  AddLiteral (258f1552-beda-484d-84d9-1d6684f86e32)
 Call ID: 258f1552-beda-484d-84d9-1d6684f86e32
  Args:
    literal_type: xsd:integer
    source: Alexandra_of_Hanover
    relation: :hasDeathYear
    literal_value: 1963
  AssignClass (6f0545dc-4e3e-4435-91bf-7d7f85bda75a)
 Call ID: 6f0545dc-4e3e-4435-91bf-7d7f85bda75a
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (51786112-421e-42b2-9f5d-b62a1f6e0dd1)
 Call ID: 51786112-421e-42b2-9f5d-b62a1f6e0dd1
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (bc39dacd-9dd6-48c6-a84b-053c1bf9a571)
 Call ID: bc39dacd-9dd6-48c6-a84b-053c1bf9a571
  Args:
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Ancestor
  AddLiteral (ae83b563-85c1-41dd-8493-86d3d866b0bb)
 Call ID: ae83b563-85c1-41dd-8493-86d3d866b0bb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1845
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddLiteral (f7dd27af-9a25-4931-bc4d-b70c8100d176)
 Call ID: f7dd27af-9a25-4931-bc4d-b70c8100d176
  Args:
    literal_type: xsd:integer
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasDeathYear
    literal_value: 1923
  AssignClass (7e954a86-a089-4973-96fb-12016261a7fb)
 Call ID: 7e954a86-a089-4973-96fb-12016261a7fb
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AssignClass (2fbcfd4c-9f6b-4771-b64f-eb61f0b5876d)
 Call ID: 2fbcfd4c-9f6b-4771-b64f-eb61f0b5876d
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (10d5f9ae-b17f-4e98-9fcb-1de5a11bfd15)
 Call ID: 10d5f9ae-b17f-4e98-9fcb-1de5a11bfd15
  Args:
    source: Thyra_of_Denmark
    type: :Ancestor
  AddLiteral (fdec8a5d-13f5-49e2-8881-b2b90200e8fc)
 Call ID: fdec8a5d-13f5-49e2-8881-b2b90200e8fc
  Args:
    source: Thyra_of_Denmark
    literal_value: 1853
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (24a634ce-f6cf-4086-b670-9a8ee0ee542d)
 Call ID: 24a634ce-f6cf-4086-b670-9a8ee0ee542d
  Args:
    literal_value: 1933
    relation: :hasDeathYear
    source: Thyra_of_Denmark
    literal_type: xsd:integer
  AddTriple (8bf00315-3c5c-4580-83ed-4608d015988e)
 Call ID: 8bf00315-3c5c-4580-83ed-4608d015988e
  Args:
    source: Alexandra_of_Hanover
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
  AddTriple (8a5b2d5c-ce32-438c-82c3-ca62e3c7733c)
 Call ID: 8a5b2d5c-ce32-438c-82c3-ca62e3c7733c
  Args:
    source: Alexandra_of_Hanover
    relation: :hasMother
    target: Thyra_of_Denmark
  AssignClass (f8c18f6b-8e98-4164-b9df-685d1ab545c5)
 Call ID: f8c18f6b-8e98-4164-b9df-685d1ab545c5
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Person
  AssignClass (01a9b784-3ebe-4539-9af6-85bc88446162)
 Call ID: 01a9b784-3ebe-4539-9af6-85bc88446162
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (8ab58426-a9aa-4c11-adad-9564163ef032)
 Call ID: 8ab58426-a9aa-4c11-adad-9564163ef032
  Args:
    type: :Ancestor
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (cbefe00f-723c-409d-8a82-5678ad39df4d)
 Call ID: cbefe00f-723c-409d-8a82-5678ad39df4d
  Args:
    literal_type: xsd:integer
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    literal_value: 1882
    relation: :hasBirthYear
  AddLiteral (7022b70e-8c13-4e38-be31-46566f70f746)
 Call ID: 7022b70e-8c13-4e38-be31-46566f70f746
  Args:
    literal_type: xsd:integer
    literal_value: 1945
    relation: :hasDeathYear
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (d7850fcc-28c7-4faa-aec3-4445d9b2aade)
 Call ID: d7850fcc-28c7-4faa-aec3-4445d9b2aade
  Args:
    relation: :hasMarriageYear
    literal_value: 1904
    source: Alexandra_of_Hanover
    literal_type: xsd:integer
  AssignClass (91f98284-0a06-4ad3-9e0c-86176b3b9b9f)
 Call ID: 91f98284-0a06-4ad3-9e0c-86176b3b9b9f
  Args:
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Person
  AssignClass (3415c386-8772-49c1-b358-09095c17c9e9)
 Call ID: 3415c386-8772-49c1-b358-09095c17c9e9
  Args:
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (365c26c2-f093-461a-88ed-37e5425be314)
 Call ID: 365c26c2-f093-461a-88ed-37e5425be314
  Args:
    type: :Ancestor
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (dab37c1b-410d-4bf3-8ab8-6f48e50c20f9)
 Call ID: dab37c1b-410d-4bf3-8ab8-6f48e50c20f9
  Args:
    type: :Person
    source: Anastasia_Mikhailovna_of_Russia
  AssignClass (c3abca7c-7e0f-41d7-9111-073084d5eff5)
 Call ID: c3abca7c-7e0f-41d7-9111-073084d5eff5
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (2bc9fc06-bf38-47c9-92a7-16db0ea313ca)
 Call ID: 2bc9fc06-bf38-47c9-92a7-16db0ea313ca
  Args:
    type: :Ancestor
    source: Anastasia_Mikhailovna_of_Russia
  AddTriple (73cb0d99-c537-440d-a04f-55f9a669d1c3)
 Call ID: 73cb0d99-c537-440d-a04f-55f9a669d1c3
  Args:
    target: Frederick_Francis_III_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasFather
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (7682b1d6-a8a3-49b4-b420-94d4563e0425)
 Call ID: 7682b1d6-a8a3-49b4-b420-94d4563e0425
  Args:
    relation: :hasMother
    target: Anastasia_Mikhailovna_of_Russia
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (1c1e71bc-bb1b-4ed8-b39a-683c1a00b8a4)
 Call ID: 1c1e71bc-bb1b-4ed8-b39a-683c1a00b8a4
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (7e3a0c87-c3b0-4dec-952f-a4a06cc70f9c)
 Call ID: 7e3a0c87-c3b0-4dec-952f-a4a06cc70f9c
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (23ce7da8-3183-4dac-91bd-40cf914a5fe1)
 Call ID: 23ce7da8-3183-4dac-91bd-40cf914a5fe1
  Args:
    source: Christian_IX_of_Denmark
    type: :Ancestor
  AddLiteral (4833a43d-abde-4273-ac64-0916a821643d)
 Call ID: 4833a43d-abde-4273-ac64-0916a821643d
  Args:
    literal_type: xsd:integer
    source: Christian_IX_of_Denmark
    literal_value: 1818
    relation: :hasBirthYear
  AddLiteral (aa3d1d76-45a6-4989-832b-fc95b9169828)
 Call ID: aa3d1d76-45a6-4989-832b-fc95b9169828
  Args:
    source: Christian_IX_of_Denmark
    literal_value: 1906
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (5b90be96-f40b-4027-bcc0-9d61ee84d626)
 Call ID: 5b90be96-f40b-4027-bcc0-9d61ee84d626
  Args:
    type: :Person
    source: Louise_of_Hesse_Kassel
  AssignClass (61536d4b-2d8f-4cef-b7d2-c0812c768342)
 Call ID: 61536d4b-2d8f-4cef-b7d2-c0812c768342
  Args:
    type: :Woman
    source: Louise_of_Hesse_Kassel
  AssignClass (edff1a08-2db2-4710-80f3-d018188ba40e)
 Call ID: edff1a08-2db2-4710-80f3-d018188ba40e
  Args:
    source: Louise_of_Hesse_Kassel
    type: :Ancestor
  AddLiteral (d7e13a5d-4659-454d-9bf9-17e47618a370)
 Call ID: d7e13a5d-4659-454d-9bf9-17e47618a370
  Args:
    literal_type: xsd:integer
    literal_value: 1817
    relation: :hasBirthYear
    source: Louise_of_Hesse_Kassel
  AddLiteral (0989935a-0299-4081-bb2f-9b60c349e8fc)
 Call ID: 0989935a-0299-4081-bb2f-9b60c349e8fc
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1898
    source: Louise_of_Hesse_Kassel
  AddTriple (9bb53232-da61-4409-9161-9a5a0834f682)
 Call ID: 9bb53232-da61-4409-9161-9a5a0834f682
  Args:
    source: Thyra_of_Denmark
    target: Christian_IX_of_Denmark
    relation: :hasFather
  AddTriple (24d99333-af61-4985-8ed9-4a4a6a50f538)
 Call ID: 24d99333-af61-4985-8ed9-4a4a6a50f538
  Args:
    relation: :hasMother
    target: Louise_of_Hesse_Kassel
    source: Thyra_of_Denmark
  AssignClass (03774947-effe-4b10-9c55-56cfed45f930)
 Call ID: 03774947-effe-4b10-9c55-56cfed45f930
  Args:
    source: George_III_of_the_United_Kingdom
    type: :Person
  AssignClass (d8ba037f-9d82-4f62-bc51-e7ab0ea8a310)
 Call ID: d8ba037f-9d82-4f62-bc51-e7ab0ea8a310
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (221dc4a0-e4de-4f94-b048-01063b6d1db3)
 Call ID: 221dc4a0-e4de-4f94-b048-01063b6d1db3
  Args:
    type: :Ancestor
    source: George_III_of_the_United_Kingdom
  AddLiteral (72337b9a-d793-4628-ad87-fbe76f080941)
 Call ID: 72337b9a-d793-4628-ad87-fbe76f080941
  Args:
    literal_type: xsd:integer
    source: George_III_of_the_United_Kingdom
    literal_value: 1738
    relation: :hasBirthYear
  AddLiteral (d932368e-f9c7-44b9-9b57-56d096855ce5)
 Call ID: d932368e-f9c7-44b9-9b57-56d096855ce5
  Args:
    literal_value: 1820
    relation: :hasDeathYear
    source: George_III_of_the_United_Kingdom
    literal_type: xsd:integer
  AssignClass (ff7a1ebd-4ed0-4e20-ae13-270bbe3ec8e6)
 Call ID: ff7a1ebd-4ed0-4e20-ae13-270bbe3ec8e6
  Args:
    source: Charlotte_of_Mecklenburg_Strelitz
    type: :Person
  AssignClass (0fb99968-4dc8-4d09-9d36-7ca8bc6b994a)
 Call ID: 0fb99968-4dc8-4d09-9d36-7ca8bc6b994a
  Args:
    source: Charlotte_of_Mecklenburg_Strelitz
    type: :Woman
  AssignClass (7f2802ae-309f-4bda-b670-39eb51303fc1)
 Call ID: 7f2802ae-309f-4bda-b670-39eb51303fc1
  Args:
    source: Charlotte_of_Mecklenburg_Strelitz
    type: :Ancestor
  AddLiteral (fcd90166-1adb-46b8-882e-aef8617b078e)
 Call ID: fcd90166-1adb-46b8-882e-aef8617b078e
  Args:
    literal_type: xsd:integer
    source: Charlotte_of_Mecklenburg_Strelitz
    literal_value: 1744
    relation: :hasBirthYear
  AddLiteral (62bad179-7c83-4cfb-a680-68589002b70a)
 Call ID: 62bad179-7c83-4cfb-a680-68589002b70a
  Args:
    relation: :hasDeathYear
    literal_value: 1818
    source: Charlotte_of_Mecklenburg_Strelitz
    literal_type: xsd:integer
  Finish (167c0265-31c1-4db9-bf71-9e3bfd4551c4)
 Call ID: 167c0265-31c1-4db9-bf71-9e3bfd4551c4
  Args: