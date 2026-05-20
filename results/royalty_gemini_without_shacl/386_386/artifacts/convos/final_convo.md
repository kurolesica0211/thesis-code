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
Duke Paul Frederick of Mecklenburg (German: Herzog Paul Friedrich zu Mecklenburg; 19 September 1852 – 17 May 1923) was a member of the House of Mecklenburg-Schwerin and general of the Mecklenburg cavalry.
Life

Duke Paul Frederick was born in Ludwigslust Castle as the second eldest son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and his first wife Princess Augusta Reuss of Köstritz, the daughter of Prince Henry LXIII Reuss of Köstritz.
Duke Paul Frederick married in Schwerin on 5 May 1881 his cousin, the Austrian born Princess Marie of Windisch-Graetz, the daughter of Prince Hugo of Windisch-Graetz and his wife Duchess Louise of Mecklenburg-Schwerin.
The couple who had five children who were all raised Roman Catholic, the religion of Princess Marie, lived a quiet life in Venice.
On 21 April 1884 Duke Paul Frederick renounced his and his sons rights of succession to Mecklenburg-Schwerin in favour of his younger brothers and their sons, so they would take precedence over him and his.
In 1887, Duke Paul Fredrick raised a Lutheran decided to convert to Roman Catholicism the religion of his wife and children.
In 1906 after upsetting his nephew Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, over the amount of money that he was spending Duke Paul Frederick and his wife were ordered to submit to the controller of the royal household.
Duke Paul Frederick died in Ludwigslust, where he and his wife are both buried in the Louisenkapelle.



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
  AssignClass (83674579-ce9d-4249-bdf4-35932b6f7147)
 Call ID: 83674579-ce9d-4249-bdf4-35932b6f7147
  Args:
    type: :Man
    source: Duke_Paul_Frederick_of_Mecklenburg
  AssignClass (d41f5cb7-b7bc-4d6d-b117-4d22be86486d)
 Call ID: d41f5cb7-b7bc-4d6d-b117-4d22be86486d
  Args:
    type: :Person
    source: Duke_Paul_Frederick_of_Mecklenburg
  AssignClass (afa18d93-4173-4690-990f-8c2034dc60f4)
 Call ID: afa18d93-4173-4690-990f-8c2034dc60f4
  Args:
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (98e56836-de26-4652-bb8e-e9e1548508f0)
 Call ID: 98e56836-de26-4652-bb8e-e9e1548508f0
  Args:
    type: :Person
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (d3d5180f-94c9-4ceb-b607-32f7122808dd)
 Call ID: d3d5180f-94c9-4ceb-b607-32f7122808dd
  Args:
    source: Princess_Augusta_Reuss_of_Köstritz
    type: :Woman
  AssignClass (997d3a4c-0468-4f7e-8cf9-9f42fc712ce1)
 Call ID: 997d3a4c-0468-4f7e-8cf9-9f42fc712ce1
  Args:
    source: Princess_Augusta_Reuss_of_Köstritz
    type: :Person
  AssignClass (dbcfeb4c-bca5-4015-be91-c2e293e9d5ea)
 Call ID: dbcfeb4c-bca5-4015-be91-c2e293e9d5ea
  Args:
    type: :Man
    source: Prince_Henry_LXIII_Reuss_of_Köstritz
  AssignClass (fa4c8122-14b1-4cb6-8ed3-4024cef0c4ea)
 Call ID: fa4c8122-14b1-4cb6-8ed3-4024cef0c4ea
  Args:
    type: :Person
    source: Prince_Henry_LXIII_Reuss_of_Köstritz
  AssignClass (15898015-c072-4143-9d78-fea9e47ea9ff)
 Call ID: 15898015-c072-4143-9d78-fea9e47ea9ff
  Args:
    source: Princess_Marie_of_Windisch_Graetz
    type: :Woman
  AssignClass (2ea44249-32d0-4bf7-9d9d-c8e5ffdb5545)
 Call ID: 2ea44249-32d0-4bf7-9d9d-c8e5ffdb5545
  Args:
    type: :Person
    source: Princess_Marie_of_Windisch_Graetz
  AssignClass (a88c1304-61f8-494c-a9d9-e5ffef7f293c)
 Call ID: a88c1304-61f8-494c-a9d9-e5ffef7f293c
  Args:
    type: :Man
    source: Prince_Hugo_of_Windisch_Graetz
  AssignClass (0ea286ae-3687-4f1a-a0ee-9b62c085b9af)
 Call ID: 0ea286ae-3687-4f1a-a0ee-9b62c085b9af
  Args:
    type: :Person
    source: Prince_Hugo_of_Windisch_Graetz
  AssignClass (c81936ee-2b42-4138-820b-45586baa9a44)
 Call ID: c81936ee-2b42-4138-820b-45586baa9a44
  Args:
    type: :Woman
    source: Duchess_Louise_of_Mecklenburg_Schwerin
  AssignClass (2f3cd9f4-7234-440a-aff9-25242be3b0e5)
 Call ID: 2f3cd9f4-7234-440a-aff9-25242be3b0e5
  Args:
    type: :Person
    source: Duchess_Louise_of_Mecklenburg_Schwerin
  AssignClass (9f282df5-7355-46db-a802-86a27dadde19)
 Call ID: 9f282df5-7355-46db-a802-86a27dadde19
  Args:
    type: :Man
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (3f9bd9a1-5c82-4cd2-9493-f0681fd799d5)
 Call ID: 3f9bd9a1-5c82-4cd2-9493-f0681fd799d5
  Args:
    type: :Person
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddLiteral (536ea41f-4c59-46f5-a01f-90681519be09)
 Call ID: 536ea41f-4c59-46f5-a01f-90681519be09
  Args:
    relation: :hasBirthYear
    literal_type: xsd:string
    source: Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1852
  AddLiteral (4c0c28d4-10bd-4ce4-bbe6-cabcd51d6db9)
 Call ID: 4c0c28d4-10bd-4ce4-bbe6-cabcd51d6db9
  Args:
    relation: :hasDeathYear
    literal_type: xsd:string
    source: Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1923
  AddTriple (b718f384-f79f-43ab-8d6b-fa5708f99980)
 Call ID: b718f384-f79f-43ab-8d6b-fa5708f99980
  Args:
    source: Duke_Paul_Frederick_of_Mecklenburg
    relation: :hasFather
    target: Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (91ad4d73-3953-4e97-bff7-bcd1a9a0a4be)
 Call ID: 91ad4d73-3953-4e97-bff7-bcd1a9a0a4be
  Args:
    relation: :hasMother
    target: Princess_Augusta_Reuss_of_Köstritz
    source: Duke_Paul_Frederick_of_Mecklenburg
  AddTriple (8dd7fa26-29d4-41f3-a759-a9a584483ead)
 Call ID: 8dd7fa26-29d4-41f3-a759-a9a584483ead
  Args:
    source: Princess_Augusta_Reuss_of_Köstritz
    target: Prince_Henry_LXIII_Reuss_of_Köstritz
    relation: :hasFather
  AddLiteral (9c3b561f-e0b6-4714-bca6-2be1bbd6e93f)
 Call ID: 9c3b561f-e0b6-4714-bca6-2be1bbd6e93f
  Args:
    literal_type: xsd:string
    relation: :hasMarriageYear
    source: Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1881
  AddTriple (285c7436-598b-434d-b047-66eebeac6460)
 Call ID: 285c7436-598b-434d-b047-66eebeac6460
  Args:
    target: Princess_Marie_of_Windisch_Graetz
    relation: :hasRelation
    source: Duke_Paul_Frederick_of_Mecklenburg
  AddTriple (359155a6-813d-423b-8cb2-1deb76b698ca)
 Call ID: 359155a6-813d-423b-8cb2-1deb76b698ca
  Args:
    source: Princess_Marie_of_Windisch_Graetz
    relation: :hasFather
    target: Prince_Hugo_of_Windisch_Graetz
  AddTriple (3b5d4bed-2d7e-4383-bb26-99f5dda1423c)
 Call ID: 3b5d4bed-2d7e-4383-bb26-99f5dda1423c
  Args:
    source: Princess_Marie_of_Windisch_Graetz
    target: Duchess_Louise_of_Mecklenburg_Schwerin
    relation: :hasMother
  AddTriple (4ad09b3d-5834-4ca2-af1e-ae895334da11)
 Call ID: 4ad09b3d-5834-4ca2-af1e-ae895334da11
  Args:
    target: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :hasRelation
    source: Duke_Paul_Frederick_of_Mecklenburg
  Finish (a3c578a2-2360-49af-8b15-3c6cf809226e)
 Call ID: a3c578a2-2360-49af-8b15-3c6cf809226e
  Args: