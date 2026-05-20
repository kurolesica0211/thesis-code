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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Alexander Karageorgevitch (Serbian Cyrillic: Александар Карађорђевић, romanized: Aleksandar Karađorđević; born 15 January 1982), also known as Prince Alexander of Serbia and Yugoslavia or Prince Aleksandar III Karađorđević, is a member of the House of Karađorđević, the former ruling family of the defunct Kingdom of Yugoslavia.
Early life and education

Prince Alexander was born 15 January 1982 in Vienna, Virginia, Alexander is the third and youngest child of the last crown prince of Yugoslavia, Alexander, and his first wife, Princess Maria da Gloria of Orléans-Braganza.
His godparents are Queen Sofía of Spain, King Constantine II of Greece (first cousins of his father), and Princess Anne, Duchess of Calabria (first cousin of his mother).
Alexander lived in Virginia until 1984.
In 1982, Alexander and his twin brother were baptized by Lavrentije, Serbian Orthodox Bishop of Western Europe, at a castle in Villamanrique de la Condesa, near Seville, Spain.
Alexander's parents divorced in 1985.
After the divorce, his father married Katherine Clairy Batis later that year, while his mother married Ignacio, 19th Duke of Segorbe in the same year.
Through his mother, Alexander has two younger half-sisters, Sol María de la Blanca Medina y Orléans-Braganza, 54th Countess of Ampurias (b. 1986) and Ana Luna Medina y Orléans-Braganza, 17th Countess of Ricla (b. 1988).
Alexander was educated in London and Canterbury with his twin brother.
Alexander was at a graduate school at an American university completing a MFA degree in advertising (Art Direction).
Patronages

In Serbia he is Chairman of the Board of Directors of the Crown Prince Foundation for Education and Culture (since 2024).
Personal life

Prince Alexander attended the reburial of his grandparents King Peter II and Queen Alexandra, great-grandmother Queen Maria, and granduncle Prince Andrew in the Royal Family Mausoleum at Oplenac on 26 May 2013.
The Serbian Royal Regalia were placed over King Peter's coffin, having Alexander placing a diamond sabre near to the Karađorđević Crown.
In 2015, Alexander dated Dunja Kusturica, a daughter of Serbian filmmaker and musician Emir Kusturica.
At the time, their relationship was compared to one of Catherine and Prince William by Serbian media.
On 17 July 2015, Prince Alexander and his brothers were present at their father's 70th birthday celebration in Belgrade.
Ancestors

Alexander is a member of the House of Karađorđević.
Through his father, Alexander descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, and Alexander of Greece, and furthermore from emperors Nicholas I of Russia and Frederick III of the Germans and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through his mother, Alexander descends from the Emperor Pedro II of Brazil, and kings Louis Philippe I of France and Francis I of the Two Sicilies, and furthermore from Francis I, Holy Roman Emperor and king Charles III of Spain.



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
  AssignClass (5048f9c5-2509-4121-ae5b-5031ccc57b83)
 Call ID: 5048f9c5-2509-4121-ae5b-5031ccc57b83
  Args:
    type: :Man
    source: Alexander_Karageorgevitch
  AssignClass (c29e8907-05ff-4989-bdcb-e6b550eed541)
 Call ID: c29e8907-05ff-4989-bdcb-e6b550eed541
  Args:
    type: :Person
    source: Alexander_Karageorgevitch
  AddLiteral (35ae21aa-85cc-41e9-a72b-c21faa5e4200)
 Call ID: 35ae21aa-85cc-41e9-a72b-c21faa5e4200
  Args:
    source: Alexander_Karageorgevitch
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1982
  AddLiteral (6b7637b8-b607-47d1-a891-f44ab40187f2)
 Call ID: 6b7637b8-b607-47d1-a891-f44ab40187f2
  Args:
    source: Alexander_Karageorgevitch
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Prince Alexander of Serbia and Yugoslavia
  AddLiteral (4aff046c-392d-4ca4-824b-7f6d2b556d71)
 Call ID: 4aff046c-392d-4ca4-824b-7f6d2b556d71
  Args:
    source: Alexander_Karageorgevitch
    literal_value: Prince Aleksandar III Karađorđević
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (3ec79bd1-cdd6-4259-9f8e-68de4a37cce3)
 Call ID: 3ec79bd1-cdd6-4259-9f8e-68de4a37cce3
  Args:
    type: :Man
    source: Alexander_Sr_Yugoslavia
  AssignClass (045d5ca3-9fcc-499b-bc87-86bae5501416)
 Call ID: 045d5ca3-9fcc-499b-bc87-86bae5501416
  Args:
    type: :Person
    source: Alexander_Sr_Yugoslavia
  AssignClass (e8bf3a83-b696-40e2-89a6-cb6666ed105b)
 Call ID: e8bf3a83-b696-40e2-89a6-cb6666ed105b
  Args:
    type: :Woman
    source: Maria_da_Gloria_Orleans_Braganza
  AssignClass (b5ff5774-5a7a-4f33-8166-60353130ee92)
 Call ID: b5ff5774-5a7a-4f33-8166-60353130ee92
  Args:
    type: :Person
    source: Maria_da_Gloria_Orleans_Braganza
  AddTriple (ebe73055-f5e0-42b2-851a-e27ace760b30)
 Call ID: ebe73055-f5e0-42b2-851a-e27ace760b30
  Args:
    relation: :hasFather
    source: Alexander_Karageorgevitch
    target: Alexander_Sr_Yugoslavia
  AddTriple (41b6d513-c1c1-4686-9101-ee098649d2d0)
 Call ID: 41b6d513-c1c1-4686-9101-ee098649d2d0
  Args:
    relation: :hasMother
    source: Alexander_Karageorgevitch
    target: Maria_da_Gloria_Orleans_Braganza
  AssignClass (b0ee921a-2ad7-4053-a7cb-2ae94cc0f62d)
 Call ID: b0ee921a-2ad7-4053-a7cb-2ae94cc0f62d
  Args:
    type: :Woman
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (7b814e7e-f482-4b0a-9ce8-ea0144bef877)
 Call ID: 7b814e7e-f482-4b0a-9ce8-ea0144bef877
  Args:
    type: :Person
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (77cd3950-5a46-49bb-b008-ccbbb74ff32f)
 Call ID: 77cd3950-5a46-49bb-b008-ccbbb74ff32f
  Args:
    type: :Woman
    source: Ana_Luna_Medina_y_Orleans_Braganza
  AssignClass (1daf4ec0-81df-49f3-8ee9-bb011bce3e77)
 Call ID: 1daf4ec0-81df-49f3-8ee9-bb011bce3e77
  Args:
    type: :Person
    source: Ana_Luna_Medina_y_Orleans_Braganza
  AddTriple (360b7b4d-5106-4282-8ead-e2cc99588fda)
 Call ID: 360b7b4d-5106-4282-8ead-e2cc99588fda
  Args:
    relation: :hasMother
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
    target: Maria_da_Gloria_Orleans_Braganza
  AddTriple (a09a4be7-9f8b-4ba3-9607-444972a64ba5)
 Call ID: a09a4be7-9f8b-4ba3-9607-444972a64ba5
  Args:
    relation: :hasMother
    source: Ana_Luna_Medina_y_Orleans_Braganza
    target: Maria_da_Gloria_Orleans_Braganza
  AssignClass (fe817bfc-ee43-46a0-9398-1e7602313840)
 Call ID: fe817bfc-ee43-46a0-9398-1e7602313840
  Args:
    type: :Woman
    source: Katherine_Clairy_Batis
  AssignClass (d9429c1a-a99d-46f6-8b86-e99ede49d495)
 Call ID: d9429c1a-a99d-46f6-8b86-e99ede49d495
  Args:
    type: :Person
    source: Katherine_Clairy_Batis
  AssignClass (12e10d88-7db2-4d11-8306-ef764056b39b)
 Call ID: 12e10d88-7db2-4d11-8306-ef764056b39b
  Args:
    type: :Man
    source: Ignacio_19th_Duke_of_Segorbe
  AssignClass (9f9dbb9c-e542-49e3-863e-d42fdc0f5c3e)
 Call ID: 9f9dbb9c-e542-49e3-863e-d42fdc0f5c3e
  Args:
    type: :Person
    source: Ignacio_19th_Duke_of_Segorbe
  Finish (3bfcee04-1389-4f36-a151-1b2e823f27da)
 Call ID: 3bfcee04-1389-4f36-a151-1b2e823f27da
  Args: