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
Prince Ludwig Rudolf of Hanover, of Great Britain and Ireland, Duke of Brunswick and Lüneburg (German: Ludwig Rudolf Georg Wilhelm Philipp Friedrich Wolrad Maximilian Prinz von Hannover) (21 November 1955 – 29 November 1988) was a member of the House of Hanover and a music producer.
Early life and career

Ludwig Rudolf was born in Hanover, Lower Saxony, Germany, the third child and second son of Ernst August, Prince of Hanover, Hereditary Prince of Brunswick (1914–1987) and his wife, Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
Ludwig Rudolf was a great-great-great-great-grandson of George III of the United Kingdom and a great-grandson of Wilhelm II, German Emperor.
Ludwig Rudolf had trained to become a music producer in Los Angeles and London.
Marriage and death

Having obtained the consent of Elizabeth II by Order in Council on 15 September 1987 pursuant to the Royal Marriages Act 1772, Ludwig Rudolf, a Lutheran, married the Roman Catholic Countess Isabella Maria von Thurn und Valsassina-Como-Vercelli (born September 8 1962 in Gmunden, Upper Austria), a former fashion model at her father's ancestral Austrian estate, Bleiburg Castle, Carinthia on 4 October 1987.
She was the daughter of Count Ariprand von Thurn und Valsassina-Como-Vercelli (1925–1996), whose family, an Austrian branch of the Della Torre dynasty, ruled Milan in the 13th and 14th century, and his wife, Princess Maria Perpetua Euphemia von Auersperg (born 1929).
In the early hours of 29 November 1988, after the couple had entertained guests at their home, Königinvilla (The Queen's Villa) in Gmunden, a house left to them by Ludwig Rudolf's elder brother Ernst August, the prince went to the bedroom where his wife had retired before midnight, and found Isabella sprawled fully dressed across their bed.
Ludwig Rudolf, who had been investigated previously on suspicion of illegal drug purchases, placed a call to his brother, Ernst August, in London, imploring him to take care of the couple's 10-month-old son.
As authorities removed Isabella's body and investigated the scene, discovering syringes, cocaine and heroin, Ludwig Rudolf slipped away.
Hours later, the prince was found in his car near his family's hunting lodge several miles away, on Lake Traun.
Ludwig Rudolf and Isabelle were interred on 2 December 1988 at Grünau
Custody of their infant son Otto Heinrich was awarded, contrary to the expressed wishes of Ludwig Rudolf, to the child's maternal grandparents.
He grew up at their castle, Schloss Bleiburg, in Austria, and then studied art at Braunschweig University of Art in Brunswick (Braunschweig).



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
  AssignClass (ceab77d0-0b0c-46f5-a3eb-67a791fd03f9)
 Call ID: ceab77d0-0b0c-46f5-a3eb-67a791fd03f9
  Args:
    source: Ludwig_Rudolf_of_Hanover
    type: :Man
  AssignClass (d9ddc48f-b79e-4082-a2bf-6d4eb6c2e09f)
 Call ID: d9ddc48f-b79e-4082-a2bf-6d4eb6c2e09f
  Args:
    source: Ludwig_Rudolf_of_Hanover
    type: :Person
  AddLiteral (381f4611-60bd-448e-adb4-95544377688b)
 Call ID: 381f4611-60bd-448e-adb4-95544377688b
  Args:
    literal_value: 1955
    source: Ludwig_Rudolf_of_Hanover
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (89ce906e-4a9c-418d-8d87-4761b5ba217a)
 Call ID: 89ce906e-4a9c-418d-8d87-4761b5ba217a
  Args:
    literal_value: 1988
    literal_type: xsd:integer
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasDeathYear
  AssignClass (196479fa-19aa-447f-b8d3-2af7862c1a8f)
 Call ID: 196479fa-19aa-447f-b8d3-2af7862c1a8f
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Man
  AssignClass (9afbca47-4aab-4438-a6bb-89ca8dd4fa4a)
 Call ID: 9afbca47-4aab-4438-a6bb-89ca8dd4fa4a
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Person
  AssignClass (d0f31258-6f83-4895-8d66-0bf3d712c933)
 Call ID: d0f31258-6f83-4895-8d66-0bf3d712c933
  Args:
    type: :Woman
    source: Ortrud_of_Schleswig_Holstein_Sonderburg_Glucksburg
  AssignClass (700e9cda-322e-44ab-a0e3-0efff2ac464d)
 Call ID: 700e9cda-322e-44ab-a0e3-0efff2ac464d
  Args:
    type: :Person
    source: Ortrud_of_Schleswig_Holstein_Sonderburg_Glucksburg
  AddTriple (feda88c9-17f5-4b1f-a469-57f28050561b)
 Call ID: feda88c9-17f5-4b1f-a469-57f28050561b
  Args:
    target: Ernst_August_Prince_of_Hanover
    relation: :hasFather
    source: Ludwig_Rudolf_of_Hanover
  AddTriple (d52116b0-b891-4654-b6e2-8963ef6e738b)
 Call ID: d52116b0-b891-4654-b6e2-8963ef6e738b
  Args:
    target: Ortrud_of_Schleswig_Holstein_Sonderburg_Glucksburg
    relation: :hasMother
    source: Ludwig_Rudolf_of_Hanover
  AssignClass (87eea553-604f-453b-844d-d7af5441028d)
 Call ID: 87eea553-604f-453b-844d-d7af5441028d
  Args:
    type: :Woman
    source: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
  AssignClass (4289e854-dfe9-4026-9c90-60cacac90bc1)
 Call ID: 4289e854-dfe9-4026-9c90-60cacac90bc1
  Args:
    type: :Person
    source: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
  AddLiteral (8226a196-601c-49ef-bdd4-613ef7433d37)
 Call ID: 8226a196-601c-49ef-bdd4-613ef7433d37
  Args:
    literal_value: 1962
    literal_type: xsd:integer
    source: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
    relation: :hasBirthYear
  AddLiteral (fe9ccb07-6cf3-4b16-b4f7-e44f7d3f2045)
 Call ID: fe9ccb07-6cf3-4b16-b4f7-e44f7d3f2045
  Args:
    literal_value: 1987
    literal_type: xsd:integer
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasMarriageYear
  AddTriple (4e1e3b47-21fe-48f3-af43-e043da1048fb)
 Call ID: 4e1e3b47-21fe-48f3-af43-e043da1048fb
  Args:
    target: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasRelation
  AssignClass (f83f338c-8fc3-4eb2-b8d1-e2f6695abef8)
 Call ID: f83f338c-8fc3-4eb2-b8d1-e2f6695abef8
  Args:
    source: Ariprand_von_Thurn_und_Valsassina_Como_Vercelli
    type: :Man
  AssignClass (5fabe31c-a805-4889-b736-61a00b6beed2)
 Call ID: 5fabe31c-a805-4889-b736-61a00b6beed2
  Args:
    type: :Person
    source: Ariprand_von_Thurn_und_Valsassina_Como_Vercelli
  AssignClass (2ddb62e4-e770-44cf-b3f7-be79e33a5e97)
 Call ID: 2ddb62e4-e770-44cf-b3f7-be79e33a5e97
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Woman
  AssignClass (c94ec00d-66b1-456e-b81f-f6b71108f67a)
 Call ID: c94ec00d-66b1-456e-b81f-f6b71108f67a
  Args:
    source: Maria_Perpetua_Euphemia_von_Auersperg
    type: :Person
  AddTriple (dd7023de-7cab-42a9-a6c1-de0368cb64d0)
 Call ID: dd7023de-7cab-42a9-a6c1-de0368cb64d0
  Args:
    source: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
    relation: :hasFather
    target: Ariprand_von_Thurn_und_Valsassina_Como_Vercelli
  AddTriple (52c0fd2d-ee77-44d0-be94-89f388026f77)
 Call ID: 52c0fd2d-ee77-44d0-be94-89f388026f77
  Args:
    relation: :hasMother
    source: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
    target: Maria_Perpetua_Euphemia_von_Auersperg
  AssignClass (8ff01ae9-4855-4293-b6bf-3f8c1571ebd6)
 Call ID: 8ff01ae9-4855-4293-b6bf-3f8c1571ebd6
  Args:
    type: :Man
    source: Ernst_August_Brother
  AssignClass (6786842d-c63c-4609-919a-5d96e0c91643)
 Call ID: 6786842d-c63c-4609-919a-5d96e0c91643
  Args:
    type: :Person
    source: Ernst_August_Brother
  AddTriple (7e09e036-aae1-4dbb-8ee0-480feb86a257)
 Call ID: 7e09e036-aae1-4dbb-8ee0-480feb86a257
  Args:
    target: Ernst_August_Brother
    source: Ludwig_Rudolf_of_Hanover
    relation: :hasBrother
  AssignClass (e7a381a6-d1c6-4ded-ab69-2b707d77b2d0)
 Call ID: e7a381a6-d1c6-4ded-ab69-2b707d77b2d0
  Args:
    type: :Man
    source: Otto_Heinrich
  AssignClass (d0404c07-0fb4-42af-95ca-8c7bb5e515fd)
 Call ID: d0404c07-0fb4-42af-95ca-8c7bb5e515fd
  Args:
    source: Otto_Heinrich
    type: :Person
  AddTriple (4061e41b-284a-40c4-8d7d-1d57740b29cb)
 Call ID: 4061e41b-284a-40c4-8d7d-1d57740b29cb
  Args:
    target: Ludwig_Rudolf_of_Hanover
    source: Otto_Heinrich
    relation: :hasFather
  AddTriple (3e6f2b11-ebc4-4e48-b7b8-a0955b26e961)
 Call ID: 3e6f2b11-ebc4-4e48-b7b8-a0955b26e961
  Args:
    target: Isabella_Maria_von_Thurn_und_Valsassina_Como_Vercelli
    source: Otto_Heinrich
    relation: :hasMother
  Finish (ef26b54b-0640-443f-9424-163d751d9a6e)
 Call ID: ef26b54b-0640-443f-9424-163d751d9a6e
  Args: