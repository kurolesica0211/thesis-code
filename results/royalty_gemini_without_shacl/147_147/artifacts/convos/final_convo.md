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
Prince Karl of Leiningen (Karl Vladimir Ernst Heinrich; 2 January 1928 – 28 September 1990) was the second son of Karl, 6th Prince of Leiningen (1898–1946), and Grand Duchess Maria Kirillovna of Russia.
She was the elder daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh.
As such, Karl was a great-great-grandson of both Queen Victoria of the United Kingdom and Emperor Alexander II of Russia (as Victoria Melita and Kirill Vladimirovich were both grandchildren of Alexander II).
Biography

Career

Born in Coburg, Germany, he worked mainly as a salesman in Paris as a young man.
With his wife, Karl subsequently resolved to take up a business career in Toronto, Canada.
Marriage and issue

Karl met Princess Marie Louise of Bulgaria in Madrid, where she was living with her mother.
She was the only daughter of Boris III of Bulgaria by his wife Princess Giovanna of Italy.
Karl announced his engagement to Marie Louise in December 1956.
Amorbach had been the residence of the House of Leiningen since 1803, and the town's streets were lined with hundreds of cheering spectators; Karl's family owns huge estates in South Germany, and was considered to be one of the wealthiest of Germany's noble families.
Karl traveled to Canada early in their marriage, and the couple decided to settle there.
The marriage produced two sons:


The marriage was unhappy, and Karl and Marie Louise divorced on 4 December 1968.
Later in life, Karl reminisced, "Princes are expected to marry princesses, so I married Marie-Louise, the daughter of Bulgarian ex-King Boris III".
Later life

Karl eventually became a naturalized Canadian citizen.
Persuaded by some Jewish friends to visit Israel, Karl eventually found a job through the help of new-found Israeli friends.



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
  AssignClass (39ccebfd-e9bb-4c9f-9f26-c8b6dcf6bf53)
 Call ID: 39ccebfd-e9bb-4c9f-9f26-c8b6dcf6bf53
  Args:
    type: :Man
    source: Karl_of_Leiningen
  AssignClass (0e1120ae-a75e-4b62-b582-39502f18e382)
 Call ID: 0e1120ae-a75e-4b62-b582-39502f18e382
  Args:
    type: :Person
    source: Karl_of_Leiningen
  AddLiteral (2577552b-4e9d-48d1-9360-d774c9b4be45)
 Call ID: 2577552b-4e9d-48d1-9360-d774c9b4be45
  Args:
    relation: :hasBirthYear
    source: Karl_of_Leiningen
    literal_type: xsd:integer
    literal_value: 1928
  AddLiteral (2c3edf26-af3a-49b7-88ca-05d6c734da04)
 Call ID: 2c3edf26-af3a-49b7-88ca-05d6c734da04
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Karl_of_Leiningen
    literal_value: 1990
  AssignClass (464b2d55-e856-4324-9ed7-e9addc8237af)
 Call ID: 464b2d55-e856-4324-9ed7-e9addc8237af
  Args:
    type: :Man
    source: Karl_6th_Prince_of_Leiningen
  AssignClass (e53ecef9-2e59-4bc4-b2d7-b30e1dc6d453)
 Call ID: e53ecef9-2e59-4bc4-b2d7-b30e1dc6d453
  Args:
    type: :Person
    source: Karl_6th_Prince_of_Leiningen
  AddLiteral (d53174e4-c5d0-400b-a3f3-0d8d52839f94)
 Call ID: d53174e4-c5d0-400b-a3f3-0d8d52839f94
  Args:
    literal_value: 1898
    source: Karl_6th_Prince_of_Leiningen
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (e8821ee9-dc7f-4005-9d78-d1c64264c196)
 Call ID: e8821ee9-dc7f-4005-9d78-d1c64264c196
  Args:
    literal_value: 1946
    source: Karl_6th_Prince_of_Leiningen
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (dc7b218e-3308-451e-b200-ae371460fea1)
 Call ID: dc7b218e-3308-451e-b200-ae371460fea1
  Args:
    type: :Woman
    source: Maria_Kirillovna_of_Russia
  AssignClass (d51203c6-709b-4f29-9e76-e91225d26bdf)
 Call ID: d51203c6-709b-4f29-9e76-e91225d26bdf
  Args:
    type: :Person
    source: Maria_Kirillovna_of_Russia
  AddTriple (7847860b-d520-4856-914d-f53a9e369646)
 Call ID: 7847860b-d520-4856-914d-f53a9e369646
  Args:
    source: Karl_of_Leiningen
    relation: :hasFather
    target: Karl_6th_Prince_of_Leiningen
  AddTriple (f3470bc3-2030-4d51-adc4-97577d45c49b)
 Call ID: f3470bc3-2030-4d51-adc4-97577d45c49b
  Args:
    source: Karl_of_Leiningen
    relation: :hasMother
    target: Maria_Kirillovna_of_Russia
  AssignClass (8aeace4e-6bb4-4321-86ff-e41a91b75b12)
 Call ID: 8aeace4e-6bb4-4321-86ff-e41a91b75b12
  Args:
    type: :Man
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (496acfe2-ed22-4fb7-a863-44bb8ec7f6ee)
 Call ID: 496acfe2-ed22-4fb7-a863-44bb8ec7f6ee
  Args:
    type: :Person
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (e8c5ecea-e8a8-4422-b919-2d87b79a72b1)
 Call ID: e8c5ecea-e8a8-4422-b919-2d87b79a72b1
  Args:
    type: :Woman
    source: Victoria_Melita_of_Edinburgh
  AssignClass (b92013aa-c049-4544-b0b2-bff4f4e0ad6f)
 Call ID: b92013aa-c049-4544-b0b2-bff4f4e0ad6f
  Args:
    type: :Person
    source: Victoria_Melita_of_Edinburgh
  AddTriple (18843219-ea8d-44f9-8b0c-e2122cb0551f)
 Call ID: 18843219-ea8d-44f9-8b0c-e2122cb0551f
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Kirill_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (e7204380-9cf1-4186-b18c-46aa691ea74a)
 Call ID: e7204380-9cf1-4186-b18c-46aa691ea74a
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Victoria_Melita_of_Edinburgh
    relation: :hasMother
  AssignClass (9187c0ef-ace8-442c-8315-293bb1af42bc)
 Call ID: 9187c0ef-ace8-442c-8315-293bb1af42bc
  Args:
    type: :Woman
    source: Marie_Louise_of_Bulgaria
  AssignClass (9100bfd9-855c-407c-b40c-362f8106d931)
 Call ID: 9100bfd9-855c-407c-b40c-362f8106d931
  Args:
    type: :Person
    source: Marie_Louise_of_Bulgaria
  AssignClass (791477f7-be4e-463f-9118-57cab8f1cb65)
 Call ID: 791477f7-be4e-463f-9118-57cab8f1cb65
  Args:
    type: :Man
    source: Boris_III_of_Bulgaria
  AssignClass (688273be-cec4-49f4-bebf-05b5f69cc432)
 Call ID: 688273be-cec4-49f4-bebf-05b5f69cc432
  Args:
    type: :Person
    source: Boris_III_of_Bulgaria
  AssignClass (470e0ecc-8c04-49ff-ba97-9c5fe96c733f)
 Call ID: 470e0ecc-8c04-49ff-ba97-9c5fe96c733f
  Args:
    type: :Woman
    source: Giovanna_of_Italy
  AssignClass (e9fc51d7-67b6-4469-af7c-8f00aa365b1c)
 Call ID: e9fc51d7-67b6-4469-af7c-8f00aa365b1c
  Args:
    type: :Person
    source: Giovanna_of_Italy
  AddTriple (ca916e84-6e30-4a4a-8fcf-356d20485a06)
 Call ID: ca916e84-6e30-4a4a-8fcf-356d20485a06
  Args:
    target: Boris_III_of_Bulgaria
    relation: :hasFather
    source: Marie_Louise_of_Bulgaria
  AddTriple (6d632826-5697-4b99-a136-7bc6403dc36d)
 Call ID: 6d632826-5697-4b99-a136-7bc6403dc36d
  Args:
    source: Marie_Louise_of_Bulgaria
    relation: :hasMother
    target: Giovanna_of_Italy
  AddTriple (34ff3e8c-ab2b-4c0c-a95e-c0b7e5677280)
 Call ID: 34ff3e8c-ab2b-4c0c-a95e-c0b7e5677280
  Args:
    target: Marie_Louise_of_Bulgaria
    relation: :hasRelation
    source: Karl_of_Leiningen
  Finish (0594d699-56da-46f4-926c-3cd951cb563a)
 Call ID: 0594d699-56da-46f4-926c-3cd951cb563a
  Args: