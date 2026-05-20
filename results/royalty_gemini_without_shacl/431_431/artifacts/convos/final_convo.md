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
Bernhard, Prince of Saxe-Meiningen (German: Bernhard, Prinz von Sachsen-Meiningen; 30 June 1901 – 4 October 1984) was the head of the House of Saxe-Meiningen from 1946 until his death.
Prince of Saxe-Meiningen

Bernhard was born in Köln the third son of Prince Frederick Johann of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
His father was the second son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
After the death of his older brother Prince Georg in 1946 his nephew Prince Frederick Alfred renounced his succession rights and so Bernhard succeeded to the headship of the house of Saxe-Meiningen and the nominal title of Duke of Saxe-Meiningen (as Bernhard IV).
As his first marriage was morganatic his second son Prince Frederick Konrad succeeded him as head of the ducal house following his death in Bad Krozingen.
Bernhard and his first wife were declared guilty of a Nazi conspiracy against Austria in 1933; he was sentenced to six weeks in prison, while she was placed under house arrest.
Family

Bernhard was married morganatically to Margot Grössler (1911–1998), from Wrocław, daughter of Friedrich Grössler, a merchant, and Erika Wägner, in Eichenhof
They had two children, both of whom had no succession rights:


Bernhard married secondly in Ziegenberg über Bad Nauheim on 11 August 1948 to Baroness Vera Schäffer von Bernstein (1914–1994), daughter of Baron Friedrich "Fritz" Schäffer von Bernstein (1868–1958) and Emma Carola, née Passavant (1884–1971).
They had three children, including a son, Konrad, with full rights to the succession to the house of Saxe-Meiningen:


Ancestry

References



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
  AssignClass (23eb4708-489b-4511-88d7-011981fa102d)
 Call ID: 23eb4708-489b-4511-88d7-011981fa102d
  Args:
    type: :Man
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (56d8840d-4faa-4832-b059-33b99986cc65)
 Call ID: 56d8840d-4faa-4832-b059-33b99986cc65
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Man
  AssignClass (a1c7d708-799e-43c7-a4e4-373a5e79ba07)
 Call ID: a1c7d708-799e-43c7-a4e4-373a5e79ba07
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (7842e693-670f-4d6e-91d8-4007678f58f2)
 Call ID: 7842e693-670f-4d6e-91d8-4007678f58f2
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (919653c4-34b7-4f4a-8b61-894a87b0783b)
 Call ID: 919653c4-34b7-4f4a-8b61-894a87b0783b
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (3f84ee63-f84f-45a3-acc6-0de99bfde1ce)
 Call ID: 3f84ee63-f84f-45a3-acc6-0de99bfde1ce
  Args:
    type: :Man
    source: Prince_Georg
  AssignClass (0165b090-de4b-4f02-ba1a-016130ae8145)
 Call ID: 0165b090-de4b-4f02-ba1a-016130ae8145
  Args:
    source: Prince_Frederick_Alfred
    type: :Man
  AssignClass (97652f77-27b1-4a41-b0a0-6bd63c8ea7fd)
 Call ID: 97652f77-27b1-4a41-b0a0-6bd63c8ea7fd
  Args:
    type: :Man
    source: Prince_Frederick_Konrad
  AssignClass (3f3082eb-b5c5-4251-a0b8-cab396f9a0f0)
 Call ID: 3f3082eb-b5c5-4251-a0b8-cab396f9a0f0
  Args:
    type: :Woman
    source: Margot_Grössler
  AssignClass (23b6cd58-3631-4549-bd6a-c1bae4e1be51)
 Call ID: 23b6cd58-3631-4549-bd6a-c1bae4e1be51
  Args:
    source: Friedrich_Grössler
    type: :Man
  AssignClass (f80f943c-1a2d-4e95-a193-32483cd76bd8)
 Call ID: f80f943c-1a2d-4e95-a193-32483cd76bd8
  Args:
    type: :Woman
    source: Erika_Wägner
  AssignClass (afac7606-1e77-412e-b034-47dbfb83381b)
 Call ID: afac7606-1e77-412e-b034-47dbfb83381b
  Args:
    type: :Woman
    source: Baroness_Vera_Schäffer_von_Bernstein
  AssignClass (c32b33e7-5cda-4632-83f8-e796ba3f9db2)
 Call ID: c32b33e7-5cda-4632-83f8-e796ba3f9db2
  Args:
    type: :Man
    source: Baron_Friedrich_Schäffer_von_Bernstein
  AssignClass (1876dc32-7d8e-49b8-beb5-70f6c7959e9a)
 Call ID: 1876dc32-7d8e-49b8-beb5-70f6c7959e9a
  Args:
    type: :Woman
    source: Emma_Carola_Passavant
  AssignClass (0cf7afc6-904e-4979-8984-db0e73ef2780)
 Call ID: 0cf7afc6-904e-4979-8984-db0e73ef2780
  Args:
    source: Konrad
    type: :Man
  AddLiteral (a473e3f5-8bc4-4e9e-89fb-f579b048e1d1)
 Call ID: a473e3f5-8bc4-4e9e-89fb-f579b048e1d1
  Args:
    relation: :hasBirthYear
    literal_value: 1901
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_type: xsd:integer
  AddLiteral (da40fd01-f2cc-47ce-b9df-1ca620c5b68a)
 Call ID: da40fd01-f2cc-47ce-b9df-1ca620c5b68a
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1984
  AddTriple (4c2ddbc4-1d78-47de-86af-ae0dd6dbefbe)
 Call ID: 4c2ddbc4-1d78-47de-86af-ae0dd6dbefbe
  Args:
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasFather
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddTriple (54863d13-b944-4d2e-a185-50b6641828c5)
 Call ID: 54863d13-b944-4d2e-a185-50b6641828c5
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
  AddTriple (62182809-d43b-4d76-b37a-fe9b9b4be1fe)
 Call ID: 62182809-d43b-4d76-b37a-fe9b9b4be1fe
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    relation: :hasFather
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddTriple (c9512e1c-21cf-4265-9a25-30b387ca0c97)
 Call ID: c9512e1c-21cf-4265-9a25-30b387ca0c97
  Args:
    target: Count_Ernst_of_Lippe-Biesterfeld
    relation: :hasFather
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (2b18408b-a29c-4715-9489-5712fcf4da76)
 Call ID: 2b18408b-a29c-4715-9489-5712fcf4da76
  Args:
    relation: :isBrotherOf
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Prince_Georg
  AddTriple (b55a809e-d63b-42fb-ac4e-f3675fcd32ca)
 Call ID: b55a809e-d63b-42fb-ac4e-f3675fcd32ca
  Args:
    source: Prince_Frederick_Konrad
    target: Bernhard_Prince_of_Saxe-Meiningen
    relation: :isSonOf
  AddTriple (62aa93c7-d1ca-4d27-8455-a671e8c70cc0)
 Call ID: 62aa93c7-d1ca-4d27-8455-a671e8c70cc0
  Args:
    source: Margot_Grössler
    target: Friedrich_Grössler
    relation: :hasFather
  AddTriple (9b2a3fd2-7aa4-421f-a94d-dc3e90740f82)
 Call ID: 9b2a3fd2-7aa4-421f-a94d-dc3e90740f82
  Args:
    source: Margot_Grössler
    target: Erika_Wägner
    relation: :hasMother
  AddLiteral (9b7734df-00a0-48bd-b844-55270bfacf19)
 Call ID: 9b7734df-00a0-48bd-b844-55270bfacf19
  Args:
    source: Margot_Grössler
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1911
  AddLiteral (71284979-ff6d-4462-a59a-4bee26dc82dd)
 Call ID: 71284979-ff6d-4462-a59a-4bee26dc82dd
  Args:
    relation: :hasDeathYear
    literal_value: 1998
    literal_type: xsd:integer
    source: Margot_Grössler
  AddTriple (d64ff066-ba56-484b-92a9-860a997db6f0)
 Call ID: d64ff066-ba56-484b-92a9-860a997db6f0
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    target: Baron_Friedrich_Schäffer_von_Bernstein
    relation: :hasFather
  AddTriple (0bad3c83-5c53-442c-9b0a-974b8445bfa3)
 Call ID: 0bad3c83-5c53-442c-9b0a-974b8445bfa3
  Args:
    target: Emma_Carola_Passavant
    relation: :hasMother
    source: Baroness_Vera_Schäffer_von_Bernstein
  AddLiteral (0e1dd87b-1ff8-47c9-9666-3d421b0322b1)
 Call ID: 0e1dd87b-1ff8-47c9-9666-3d421b0322b1
  Args:
    relation: :hasBirthYear
    literal_value: 1914
    literal_type: xsd:integer
    source: Baroness_Vera_Schäffer_von_Bernstein
  AddLiteral (d4a8d274-3666-4eff-bd26-61d8d2dfb628)
 Call ID: d4a8d274-3666-4eff-bd26-61d8d2dfb628
  Args:
    literal_value: 1994
    relation: :hasDeathYear
    source: Baroness_Vera_Schäffer_von_Bernstein
    literal_type: xsd:integer
  AddLiteral (48ea474e-cdc8-4aa1-b10c-2ce050866df4)
 Call ID: 48ea474e-cdc8-4aa1-b10c-2ce050866df4
  Args:
    literal_value: 1868
    relation: :hasBirthYear
    source: Baron_Friedrich_Schäffer_von_Bernstein
    literal_type: xsd:integer
  AddLiteral (f2b79125-79db-4835-819b-3f7afa6521c9)
 Call ID: f2b79125-79db-4835-819b-3f7afa6521c9
  Args:
    source: Baron_Friedrich_Schäffer_von_Bernstein
    literal_type: xsd:integer
    literal_value: 1958
    relation: :hasDeathYear
  AddLiteral (3931f08e-0548-4ba1-b06b-ae4de851c908)
 Call ID: 3931f08e-0548-4ba1-b06b-ae4de851c908
  Args:
    relation: :hasBirthYear
    literal_value: 1884
    source: Emma_Carola_Passavant
    literal_type: xsd:integer
  AddLiteral (1d8c519d-c488-425f-981b-39800b727172)
 Call ID: 1d8c519d-c488-425f-981b-39800b727172
  Args:
    source: Emma_Carola_Passavant
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1971
  AddTriple (5b354857-ec04-4304-8b56-0efc48960182)
 Call ID: 5b354857-ec04-4304-8b56-0efc48960182
  Args:
    source: Konrad
    relation: :isSonOf
    target: Bernhard_Prince_of_Saxe-Meiningen
  AddTriple (f4ab6b45-5478-433e-8886-6d4fc64d8be2)
 Call ID: f4ab6b45-5478-433e-8886-6d4fc64d8be2
  Args:
    target: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasMother
    source: Konrad
  AddLiteral (57d2c06e-22cb-4c54-8797-bc596fbafa03)
 Call ID: 57d2c06e-22cb-4c54-8797-bc596fbafa03
  Args:
    source: Baroness_Vera_Schäffer_von_Bernstein
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasMarriageYear
  Finish (b12c9858-43c6-4f9b-b882-c2a32f99c1ba)
 Call ID: b12c9858-43c6-4f9b-b882-c2a32f99c1ba
  Args: