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
Infante Alfonso of Spain, Prince of the Two Sicilies, Duke of Calabria (30 November 1901 – 3 February 1964) was one of two claimants to the title of the head of the House of Bourbon-Two Sicilies from 1960 until his death in 1964.
He was the son of Prince Carlos of Bourbon-Two Sicilies and María de las Mercedes, Princess of Asturias.
He was born and died in Madrid, Spain.
Alfonso's mother was María de las Mercedes, Princess of Asturias, but she died in childbirth in 1904.
Alfonso XIII, King of Spain, was unmarried at the time so as the Princess of the Asturias's eldest son, the young infante became heir presumptive to the Spanish crown, though, unlike his mother, he never held the title of Prince of Asturias.
He was heir presumptive until the birth of his cousin, Alfonso, to Alfonso XIII and Queen Victoria Eugenie in 1907.
Marriage and issue

Alfonso married Princess Alice of Bourbon-Parma (1917–2017), his second cousin, daughter of Elias, Duke of Parma and Piacenza, and Archduchess Maria Anna of Austria, on 16 April 1936 in Vienna, Austria.



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
  AssignClass (e3a279a6-a396-4a15-85af-ee8f2122a08a)
 Call ID: e3a279a6-a396-4a15-85af-ee8f2122a08a
  Args:
    type: :Man
    source: Alfonso_of_Spain
  AssignClass (1f2f2b20-d653-46a5-a4a7-4daac282e61a)
 Call ID: 1f2f2b20-d653-46a5-a4a7-4daac282e61a
  Args:
    type: :Person
    source: Alfonso_of_Spain
  AddLiteral (e9697ec9-a338-4c81-895e-34ddfb3ceebb)
 Call ID: e9697ec9-a338-4c81-895e-34ddfb3ceebb
  Args:
    source: Alfonso_of_Spain
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1901
  AddLiteral (fcfe1b4e-f2da-4439-996b-81a67b4977bd)
 Call ID: fcfe1b4e-f2da-4439-996b-81a67b4977bd
  Args:
    source: Alfonso_of_Spain
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1964
  AssignClass (3a11f5a8-2d9e-4ca8-b10c-58baf0010fdf)
 Call ID: 3a11f5a8-2d9e-4ca8-b10c-58baf0010fdf
  Args:
    type: :Man
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (b6932f8b-b44f-414d-91df-0e7b2c865875)
 Call ID: b6932f8b-b44f-414d-91df-0e7b2c865875
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (5bd99266-1293-4eaa-bd5c-da02404f9e09)
 Call ID: 5bd99266-1293-4eaa-bd5c-da02404f9e09
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes
  AssignClass (2fa090e0-7a98-46a2-ab68-d598cee75902)
 Call ID: 2fa090e0-7a98-46a2-ab68-d598cee75902
  Args:
    type: :Person
    source: Maria_de_las_Mercedes
  AddTriple (bd2024f1-41b7-4edf-a220-ad2e780e290c)
 Call ID: bd2024f1-41b7-4edf-a220-ad2e780e290c
  Args:
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Alfonso_of_Spain
    relation: :hasFather
  AddTriple (f30b59c8-65e8-49da-bb04-e3952ed1db8c)
 Call ID: f30b59c8-65e8-49da-bb04-e3952ed1db8c
  Args:
    source: Alfonso_of_Spain
    relation: :hasMother
    target: Maria_de_las_Mercedes
  AssignClass (5662e99f-2e75-49e7-b106-1e1855e1ec93)
 Call ID: 5662e99f-2e75-49e7-b106-1e1855e1ec93
  Args:
    type: :Woman
    source: Alice_of_Bourbon-Parma
  AssignClass (da1055a8-a7f4-4f9a-a563-7036f8038c1c)
 Call ID: da1055a8-a7f4-4f9a-a563-7036f8038c1c
  Args:
    type: :Person
    source: Alice_of_Bourbon-Parma
  AddTriple (1f1babb2-3158-48f0-854a-0686e3346e8d)
 Call ID: 1f1babb2-3158-48f0-854a-0686e3346e8d
  Args:
    target: Alice_of_Bourbon-Parma
    relation: :hasRelation
    source: Alfonso_of_Spain
  AddLiteral (5ea74b2a-1168-4085-b87d-2ff3d052842e)
 Call ID: 5ea74b2a-1168-4085-b87d-2ff3d052842e
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Alfonso_of_Spain
    literal_value: 1936
  AssignClass (348beaf5-d112-4782-9951-11f3a3aa8c3d)
 Call ID: 348beaf5-d112-4782-9951-11f3a3aa8c3d
  Args:
    type: :Man
    source: Elias_of_Parma
  AssignClass (684901e0-c131-460c-8747-be7c0774797b)
 Call ID: 684901e0-c131-460c-8747-be7c0774797b
  Args:
    type: :Person
    source: Elias_of_Parma
  AssignClass (ab9f640f-500a-4942-99a2-392c537a992f)
 Call ID: ab9f640f-500a-4942-99a2-392c537a992f
  Args:
    type: :Woman
    source: Maria_Anna_of_Austria
  AssignClass (07586aeb-9dc2-4c38-accf-61e311f5e0f8)
 Call ID: 07586aeb-9dc2-4c38-accf-61e311f5e0f8
  Args:
    type: :Person
    source: Maria_Anna_of_Austria
  AddTriple (6bb04c08-5741-4571-8e8f-9e7a334b72f1)
 Call ID: 6bb04c08-5741-4571-8e8f-9e7a334b72f1
  Args:
    relation: :hasFather
    source: Alice_of_Bourbon-Parma
    target: Elias_of_Parma
  AddTriple (634e56b5-713e-4707-b3b8-49f4ff691eb6)
 Call ID: 634e56b5-713e-4707-b3b8-49f4ff691eb6
  Args:
    source: Alice_of_Bourbon-Parma
    relation: :hasMother
    target: Maria_Anna_of_Austria
  Finish (6fdaef96-994e-4869-90d9-8c483f75ae92)
 Call ID: 6fdaef96-994e-4869-90d9-8c483f75ae92
  Args: