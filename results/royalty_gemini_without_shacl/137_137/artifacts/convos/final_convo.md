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
Prince Alexander of Yugoslavia (Serbian: Александар П. Карађорђевић / Aleksandar P. Karađorđević; 13 August 1924 – 12 May 2016) was the elder son of Prince Paul, who served as Regent of Yugoslavia in the 1930s, and his wife, Princess Olga of Greece and Denmark.
Birth and education

Alexander was born at White Lodge, Richmond Park, United Kingdom.
As a nephew of Princess Marina, Duchess of Kent (née of Greece and Denmark), he was a first cousin of Prince Edward, Duke of Kent, Prince Michael of Kent, and Princess Alexandra of Kent; he was also a first cousin once removed of Prince Philip, Duke of Edinburgh.
Marriages and family

He took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On 12 February 1955, Alexander married Princess Maria Pia of Savoy, daughter of King Umberto II of Italy and of his wife, Princess Marie José of Belgium.
The couple had met on 22 August 1954 during the royal cruise of the Agamemnon, hosted by King Paul and Queen Frederica of Greece.
Alexander and Maria Pia have twin sons born in 1958:
Alexander and Maria Pia divorced in 1967, and in 2003 she married Prince Michel of Bourbon-Parma, himself divorced from Princess Yolande de Broglie-Revel.
On 2 November 1973, in a civil ceremony in Paris, Alexander married Princess Barbara Eleonore Marie of Liechtenstein(born 9 July 1942), daughter of Prince Johannes of Liechtenstein (first cousin once removed to Prince Hans-Adam II of Liechtenstein) and Countess Karoline of Ledebur-Wicheln (aunt of Hans Adam's late wife Marie, Princess of Liechtenstein).
On 28 October 1995 Prince Alexander and Princess Barbara were married in the Orthodox faith in
Oplenac, and had issue:


Flying career

The Prince wished to serve in the British Royal Air Force during World War Two, but was initially prevented by his father's political affiliations.
He was eventually commissioned in the RAF through the intervention of Prince George, Duke of Kent, his uncle.
Associations

Alexander was one of the four founding members of the Serbian Unity Congress.
On 17 February 2008, Alexander issued a statement condemning the declaration of independence by Kosovo.
On the occasion of Prince Alexander's 90th birthday on 13 August 2014, a celebration of his life in words and pictures appeared in that month's UK magazine Majesty.
Death

Prince Alexander died on 12 May 2016 in Paris, where he and his wife had lived for many years.
He was buried at Oplenac, Serbia, with his parents and brother, his coffin being carried by Serbian Air Force fighter pilots.



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
  AssignClass (5397dc42-446e-43d9-be36-b0a02ac0731a)
 Call ID: 5397dc42-446e-43d9-be36-b0a02ac0731a
  Args:
    type: :Man
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (c7d46a8e-2b62-4a83-967f-4810868e7b3f)
 Call ID: c7d46a8e-2b62-4a83-967f-4810868e7b3f
  Args:
    type: :Person
    source: Prince_Alexander_of_Yugoslavia
  AddLiteral (0e9de1b9-1442-4485-be18-7c1764165c3a)
 Call ID: 0e9de1b9-1442-4485-be18-7c1764165c3a
  Args:
    literal_value: 1924
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e0f3c736-d43e-444f-9c2e-3fb9356a6d66)
 Call ID: e0f3c736-d43e-444f-9c2e-3fb9356a6d66
  Args:
    literal_value: 2016
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (84bb69c0-0aee-40d2-9ef2-352aeee1b013)
 Call ID: 84bb69c0-0aee-40d2-9ef2-352aeee1b013
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (921453d4-4224-4533-8ff9-de96f750f871)
 Call ID: 921453d4-4224-4533-8ff9-de96f750f871
  Args:
    source: Prince_Paul_of_Yugoslavia
    type: :Person
  AssignClass (b97e8e34-9bef-4061-a1b9-efc9ca888cac)
 Call ID: b97e8e34-9bef-4061-a1b9-efc9ca888cac
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (face9a8e-4e1f-4bb4-954e-17d95c016e2f)
 Call ID: face9a8e-4e1f-4bb4-954e-17d95c016e2f
  Args:
    type: :Person
    source: Princess_Olga_of_Greece_and_Denmark
  AddTriple (c481b843-606e-4bb4-a33d-46da9187e9e6)
 Call ID: c481b843-606e-4bb4-a33d-46da9187e9e6
  Args:
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasFather
    target: Prince_Paul_of_Yugoslavia
  AddTriple (da111f89-7988-445f-bdf9-bade4f2f509f)
 Call ID: da111f89-7988-445f-bdf9-bade4f2f509f
  Args:
    source: Prince_Alexander_of_Yugoslavia
    target: Princess_Olga_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (fb32b063-0138-4c11-9848-f867f5a73f83)
 Call ID: fb32b063-0138-4c11-9848-f867f5a73f83
  Args:
    type: :Woman
    source: Princess_Maria_Pia_of_Savoy
  AssignClass (fa083c48-c85f-4278-85f7-6ca34518fab1)
 Call ID: fa083c48-c85f-4278-85f7-6ca34518fab1
  Args:
    type: :Person
    source: Princess_Maria_Pia_of_Savoy
  AddTriple (3f63a0dd-0134-450f-abbc-ed6304d5816d)
 Call ID: 3f63a0dd-0134-450f-abbc-ed6304d5816d
  Args:
    source: Prince_Alexander_of_Yugoslavia
    target: Princess_Maria_Pia_of_Savoy
    relation: :hasRelation
  AddLiteral (0eef1556-1e31-4015-9986-e8b7b4c0feda)
 Call ID: 0eef1556-1e31-4015-9986-e8b7b4c0feda
  Args:
    literal_value: 1955
    source: Prince_Alexander_of_Yugoslavia
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (a87f48ec-1b75-4e66-8089-f2bad5611b9f)
 Call ID: a87f48ec-1b75-4e66-8089-f2bad5611b9f
  Args:
    source: King_Umberto_II_of_Italy
    type: :Man
  AssignClass (8f4037bd-e422-4e76-a4b6-af4d9f911594)
 Call ID: 8f4037bd-e422-4e76-a4b6-af4d9f911594
  Args:
    type: :Person
    source: King_Umberto_II_of_Italy
  AssignClass (8e28b6de-5971-4b40-8552-fbc03b9e36db)
 Call ID: 8e28b6de-5971-4b40-8552-fbc03b9e36db
  Args:
    type: :Woman
    source: Princess_Marie_Jose_of_Belgium
  AssignClass (b90db39d-d555-4493-9d2a-23c4c0c5f8c4)
 Call ID: b90db39d-d555-4493-9d2a-23c4c0c5f8c4
  Args:
    source: Princess_Marie_Jose_of_Belgium
    type: :Person
  AddTriple (79aa287d-75e7-427a-996a-d6b18e22bb3d)
 Call ID: 79aa287d-75e7-427a-996a-d6b18e22bb3d
  Args:
    source: Princess_Maria_Pia_of_Savoy
    relation: :hasFather
    target: King_Umberto_II_of_Italy
  AddTriple (ac3c58d8-3b90-4ba0-a0bf-cd2176db3ea8)
 Call ID: ac3c58d8-3b90-4ba0-a0bf-cd2176db3ea8
  Args:
    source: Princess_Maria_Pia_of_Savoy
    relation: :hasMother
    target: Princess_Marie_Jose_of_Belgium
  AssignClass (e86da9dc-4b1a-4757-9630-1fcac8334bf2)
 Call ID: e86da9dc-4b1a-4757-9630-1fcac8334bf2
  Args:
    type: :Woman
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AssignClass (a93192b6-b414-4f01-a44a-ca4eb4b7261f)
 Call ID: a93192b6-b414-4f01-a44a-ca4eb4b7261f
  Args:
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    type: :Person
  AddTriple (c9ec08ee-766d-44d6-8d00-772859f5031c)
 Call ID: c9ec08ee-766d-44d6-8d00-772859f5031c
  Args:
    target: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    relation: :hasRelation
    source: Prince_Alexander_of_Yugoslavia
  AddLiteral (be0062c0-2e9f-4247-a90e-3095658d1f77)
 Call ID: be0062c0-2e9f-4247-a90e-3095658d1f77
  Args:
    literal_value: 1973
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (35c3d670-66df-42dc-9ea0-2eb498ec4f67)
 Call ID: 35c3d670-66df-42dc-9ea0-2eb498ec4f67
  Args:
    type: :Man
    source: Prince_Johannes_of_Liechtenstein
  AssignClass (9361265a-cd05-44e3-b548-9268d03f1b9e)
 Call ID: 9361265a-cd05-44e3-b548-9268d03f1b9e
  Args:
    source: Prince_Johannes_of_Liechtenstein
    type: :Person
  AssignClass (42a29935-ffd8-4558-8dd7-fb66a150c0fa)
 Call ID: 42a29935-ffd8-4558-8dd7-fb66a150c0fa
  Args:
    type: :Woman
    source: Countess_Karoline_of_Ledebur-Wicheln
  AssignClass (9ff61eda-68e4-4489-bcff-44f3afffea3b)
 Call ID: 9ff61eda-68e4-4489-bcff-44f3afffea3b
  Args:
    type: :Person
    source: Countess_Karoline_of_Ledebur-Wicheln
  AddTriple (d8ddcb26-316f-4951-8820-7783d6fffcdc)
 Call ID: d8ddcb26-316f-4951-8820-7783d6fffcdc
  Args:
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    relation: :hasFather
    target: Prince_Johannes_of_Liechtenstein
  AddTriple (acf84cd6-0302-48d2-aea1-d3e9c78f118a)
 Call ID: acf84cd6-0302-48d2-aea1-d3e9c78f118a
  Args:
    target: Countess_Karoline_of_Ledebur-Wicheln
    relation: :hasMother
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AssignClass (fff24aeb-9ca3-4a06-b7c3-ae23d25f8aa5)
 Call ID: fff24aeb-9ca3-4a06-b7c3-ae23d25f8aa5
  Args:
    source: Prince_Michel_of_Bourbon-Parma
    type: :Man
  AssignClass (95debf23-9ef9-4894-a414-e15c67f02598)
 Call ID: 95debf23-9ef9-4894-a414-e15c67f02598
  Args:
    type: :Person
    source: Prince_Michel_of_Bourbon-Parma
  AddTriple (2b4d99cb-5a5b-4f04-af43-a3f3d9f7339d)
 Call ID: 2b4d99cb-5a5b-4f04-af43-a3f3d9f7339d
  Args:
    relation: :hasRelation
    target: Prince_Michel_of_Bourbon-Parma
    source: Princess_Maria_Pia_of_Savoy
  AssignClass (9e56fd25-3cc0-4626-ac32-f3d4e62a910e)
 Call ID: 9e56fd25-3cc0-4626-ac32-f3d4e62a910e
  Args:
    type: :Woman
    source: Princess_Yolande_de_Broglie-Revel
  AssignClass (75b03712-7d30-4856-b8e8-a836a5a2ccd6)
 Call ID: 75b03712-7d30-4856-b8e8-a836a5a2ccd6
  Args:
    type: :Person
    source: Princess_Yolande_de_Broglie-Revel
  AddTriple (a9419fc8-bd22-489d-ac45-74d5626a5c6e)
 Call ID: a9419fc8-bd22-489d-ac45-74d5626a5c6e
  Args:
    relation: :hasRelation
    target: Princess_Yolande_de_Broglie-Revel
    source: Prince_Michel_of_Bourbon-Parma
  Finish (7fd31a9d-a536-4d34-9e38-69ec6d5368e0)
 Call ID: 7fd31a9d-a536-4d34-9e38-69ec6d5368e0
  Args: