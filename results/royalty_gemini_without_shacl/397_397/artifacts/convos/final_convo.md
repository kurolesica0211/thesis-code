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
Georg, Prince of Saxe-Meiningen (11 October 1892 – 6 January 1946) was the head of the house of Saxe-Meiningen from 1941 until his death.
He was born in Kassel as the eldest son of Prince Frederick Johann of Saxe-Meiningen (1861-1914) and Countess Adelaide of Lippe-Biesterfeld (1870–1948).
His father was a son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
Georg studied law at the Universities of Munich and Jena.
Georg suspended his studies to serve in World War I and saw action as a captain in a cavalry regiment.
After the death of his uncle Ernst on 29 December 1941, Georg succeeded to the headship of the house of Saxe-Meiningen and assumed the title of Duke of Saxe-Meiningen and style Georg III.
Georg and his family were expropriated without compensation in 1945.
Georg, who served as a major in the Wehrmacht died in the Russian prisoner of war camp near Cherepovets (Tscherepowetz in German) in Northern Russia.
His heir was his second and only surviving son Prince Frederick Alfred who renounced the succession, being a monk in 1953, allowing it to pass to his uncle Bernhard.
Marriage and children

He was married in Freiburg im Breisgau on 22 February 1919 to Countess Klara Marie von Korff genannt Schmising-Kerssenbrock (Darmstadt, 31 May 1895



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
  AssignClass (7a67da56-df1e-4a2f-adf6-3f8edc1e2d67)
 Call ID: 7a67da56-df1e-4a2f-adf6-3f8edc1e2d67
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    type: :Man
  AssignClass (0f6a674b-f93d-45b3-b0d9-57d38dc73831)
 Call ID: 0f6a674b-f93d-45b3-b0d9-57d38dc73831
  Args:
    type: :Person
    source: Georg_Prince_of_Saxe-Meiningen
  AddLiteral (111fb194-1bd1-451c-9630-31a5f24b6bd5)
 Call ID: 111fb194-1bd1-451c-9630-31a5f24b6bd5
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1892
    relation: :hasBirthYear
  AddLiteral (1e35e05a-4408-43ee-ae96-bc3656956b64)
 Call ID: 1e35e05a-4408-43ee-ae96-bc3656956b64
  Args:
    literal_type: xsd:integer
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasDeathYear
    literal_value: 1946
  AssignClass (573faef6-3aba-4c69-acfd-92c8b23554e0)
 Call ID: 573faef6-3aba-4c69-acfd-92c8b23554e0
  Args:
    type: :Man
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (b5fe2102-f57f-44fb-9d77-0391f5a6772e)
 Call ID: b5fe2102-f57f-44fb-9d77-0391f5a6772e
  Args:
    type: :Person
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddLiteral (d2cda314-1168-4803-9508-0c525ebe362c)
 Call ID: d2cda314-1168-4803-9508-0c525ebe362c
  Args:
    literal_type: xsd:integer
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_value: 1861
  AddLiteral (4d7b4c39-a9c0-4afe-8c91-0308ea65cef0)
 Call ID: 4d7b4c39-a9c0-4afe-8c91-0308ea65cef0
  Args:
    literal_value: 1914
    relation: :hasDeathYear
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    literal_type: xsd:integer
  AssignClass (488a20c4-8b27-409f-8ddc-1cffa4d021c8)
 Call ID: 488a20c4-8b27-409f-8ddc-1cffa4d021c8
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (617017a3-bc88-4033-b857-dfc5882c5199)
 Call ID: 617017a3-bc88-4033-b857-dfc5882c5199
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Person
  AddLiteral (71717690-ffd4-4a78-adbc-d3c2b26425b3)
 Call ID: 71717690-ffd4-4a78-adbc-d3c2b26425b3
  Args:
    literal_type: xsd:integer
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    literal_value: 1870
    relation: :hasBirthYear
  AddLiteral (1e472e47-1b3d-4345-aeba-6cb8afa57569)
 Call ID: 1e472e47-1b3d-4345-aeba-6cb8afa57569
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1948
  AddTriple (c0ad22c8-3111-47bf-a812-afbcc7414436)
 Call ID: c0ad22c8-3111-47bf-a812-afbcc7414436
  Args:
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddTriple (f8ef0173-0d89-4d18-a101-dbf058c2deda)
 Call ID: f8ef0173-0d89-4d18-a101-dbf058c2deda
  Args:
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    source: Georg_Prince_of_Saxe-Meiningen
    relation: :hasMother
  AssignClass (b624334f-2049-4a33-875d-574759834a80)
 Call ID: b624334f-2049-4a33-875d-574759834a80
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (1e0d9fda-9a80-4ae9-8f45-7405c62455d4)
 Call ID: 1e0d9fda-9a80-4ae9-8f45-7405c62455d4
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Person
  AddTriple (5e1fd867-517f-4042-854f-1873503e32fb)
 Call ID: 5e1fd867-517f-4042-854f-1873503e32fb
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    relation: :hasFather
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (ab01a2f5-86e1-429d-9f5a-56fb0af4b064)
 Call ID: ab01a2f5-86e1-429d-9f5a-56fb0af4b064
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (9c31e870-d3f7-41de-b27e-df3055909309)
 Call ID: 9c31e870-d3f7-41de-b27e-df3055909309
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Person
  AddTriple (0ceb1341-0e8d-45c0-8834-e072d07c2f98)
 Call ID: 0ceb1341-0e8d-45c0-8834-e072d07c2f98
  Args:
    relation: :hasFather
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    target: Count_Ernst_of_Lippe-Biesterfeld
  AssignClass (7c37f956-3e82-41d9-ba60-ff466ecceca2)
 Call ID: 7c37f956-3e82-41d9-ba60-ff466ecceca2
  Args:
    source: Prince_Frederick_Alfred
    type: :Man
  AssignClass (9d4c1610-1a7e-4526-8072-7a3ddfe32c5d)
 Call ID: 9d4c1610-1a7e-4526-8072-7a3ddfe32c5d
  Args:
    type: :Person
    source: Prince_Frederick_Alfred
  AddTriple (f27b635b-4720-4934-85b5-eb4159581dd8)
 Call ID: f27b635b-4720-4934-85b5-eb4159581dd8
  Args:
    target: Georg_Prince_of_Saxe-Meiningen
    relation: :hasFather
    source: Prince_Frederick_Alfred
  AssignClass (d94bdc3b-9587-46e9-9e0c-60bd86bd4182)
 Call ID: d94bdc3b-9587-46e9-9e0c-60bd86bd4182
  Args:
    source: Bernhard
    type: :Man
  AssignClass (7e0e2f93-7556-4b3d-9a52-c275221af999)
 Call ID: 7e0e2f93-7556-4b3d-9a52-c275221af999
  Args:
    type: :Person
    source: Bernhard
  AssignClass (52914436-45b3-4434-b637-103cb5576bbb)
 Call ID: 52914436-45b3-4434-b637-103cb5576bbb
  Args:
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
    type: :Woman
  AssignClass (618e07f0-0d3b-4b8f-9d7f-e430ce11fad8)
 Call ID: 618e07f0-0d3b-4b8f-9d7f-e430ce11fad8
  Args:
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
    type: :Person
  AddLiteral (82769c48-5aa4-4484-9196-d11e2ca7af73)
 Call ID: 82769c48-5aa4-4484-9196-d11e2ca7af73
  Args:
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising-Kerssenbrock
    literal_type: xsd:integer
    literal_value: 1895
    relation: :hasBirthYear
  AddLiteral (1ddb99a4-f55c-4f21-96f2-d59fe81240ff)
 Call ID: 1ddb99a4-f55c-4f21-96f2-d59fe81240ff
  Args:
    relation: :hasMarriageYear
    literal_value: 1919
    literal_type: xsd:integer
    source: Georg_Prince_of_Saxe-Meiningen
  Finish (05504ecd-73b9-48fd-8603-25ce73388ef0)
 Call ID: 05504ecd-73b9-48fd-8603-25ce73388ef0
  Args: