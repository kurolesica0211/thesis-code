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
Princess Kira Auguste Viktoria Friederike of Prussia (27 June 1943 – 10 January 2004) was the fourth child and second daughter of Louis Ferdinand, Prince of Prussia and Grand Duchess Kira Kirillovna of Russia.
Princess Kira was born in Cadienen, East Prussia (today Kadyny, Poland).
They had one daughter, Kira-Marina Liepsner (born 22 January 1977), who married Andreas Felix Paul von Bismarck (31 January 1979 – 31 October 2019)
Kira-Marina and Andreas had two daughters, Princess Kira’s granddaughters.
When her father died in 1994, Princess Kira took his seat on the board of the Kissinger Sommer classical music festival.



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
  AssignClass (9cd51b5f-6c6c-4eb1-95b4-e5beb3f8383f)
 Call ID: 9cd51b5f-6c6c-4eb1-95b4-e5beb3f8383f
  Args:
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
    type: :Person
  AssignClass (b5180b09-473a-47b1-9690-5db52a2bef2a)
 Call ID: b5180b09-473a-47b1-9690-5db52a2bef2a
  Args:
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
    type: :Woman
  AssignClass (28997b3c-7a71-460f-8071-3fac9ae11f3d)
 Call ID: 28997b3c-7a71-460f-8071-3fac9ae11f3d
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (8e562bd5-1520-458b-92f4-efc722cfda27)
 Call ID: 8e562bd5-1520-458b-92f4-efc722cfda27
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Man
  AssignClass (74c9fc6c-d99b-4b6d-bbb8-8620b6c22c0f)
 Call ID: 74c9fc6c-d99b-4b6d-bbb8-8620b6c22c0f
  Args:
    type: :Person
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AssignClass (14267941-8d9d-42db-abcc-1f858bbc9607)
 Call ID: 14267941-8d9d-42db-abcc-1f858bbc9607
  Args:
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    type: :Woman
  AddTriple (e48d56b8-1c2b-4664-a5c5-bfffe43294f1)
 Call ID: e48d56b8-1c2b-4664-a5c5-bfffe43294f1
  Args:
    target: Louis_Ferdinand_Prince_of_Prussia
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
    relation: :hasFather
  AddTriple (bee01380-3f7a-4e89-8d52-a95f90370362)
 Call ID: bee01380-3f7a-4e89-8d52-a95f90370362
  Args:
    target: Grand_Duchess_Kira_Kirillovna_of_Russia
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
    relation: :hasMother
  AddLiteral (19c32263-8b7b-4c7e-bf39-232b9d5a4071)
 Call ID: 19c32263-8b7b-4c7e-bf39-232b9d5a4071
  Args:
    relation: :hasBirthYear
    literal_value: 1943
    literal_type: xsd:string
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
  AddLiteral (489c1dce-f734-4727-80dd-9636315e9f5c)
 Call ID: 489c1dce-f734-4727-80dd-9636315e9f5c
  Args:
    literal_value: 2004
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
    literal_type: xsd:string
    relation: :hasDeathYear
  AssignClass (8b93f5c5-4d24-44e0-a13e-8e03443785dd)
 Call ID: 8b93f5c5-4d24-44e0-a13e-8e03443785dd
  Args:
    type: :Person
    source: Kira-Marina_Liepsner
  AssignClass (30952927-0fd0-40c6-a52e-9f794be00157)
 Call ID: 30952927-0fd0-40c6-a52e-9f794be00157
  Args:
    source: Kira-Marina_Liepsner
    type: :Woman
  AddTriple (94cfead5-461c-4201-a983-564ce71ccfd8)
 Call ID: 94cfead5-461c-4201-a983-564ce71ccfd8
  Args:
    relation: :hasDaughter
    source: Princess_Kira_Auguste_Viktoria_Friederike_of_Prussia
    target: Kira-Marina_Liepsner
  AssignClass (fdec76c4-9a67-4a33-810d-82afa30518e0)
 Call ID: fdec76c4-9a67-4a33-810d-82afa30518e0
  Args:
    source: Andreas_Felix_Paul_von_Bismarck
    type: :Person
  AssignClass (d1278968-fd07-4044-8f48-8a34af1ee638)
 Call ID: d1278968-fd07-4044-8f48-8a34af1ee638
  Args:
    type: :Man
    source: Andreas_Felix_Paul_von_Bismarck
  AddLiteral (c464132c-9375-44cd-b7a6-38f4be086400)
 Call ID: c464132c-9375-44cd-b7a6-38f4be086400
  Args:
    literal_type: xsd:string
    source: Andreas_Felix_Paul_von_Bismarck
    literal_value: 1979
    relation: :hasBirthYear
  AddLiteral (e36d4286-90db-4c43-8d47-591f6b474985)
 Call ID: e36d4286-90db-4c43-8d47-591f6b474985
  Args:
    literal_value: 2019
    source: Andreas_Felix_Paul_von_Bismarck
    literal_type: xsd:string
    relation: :hasDeathYear
  AddTriple (935e909f-cb7e-4e05-998f-a69fc07feabd)
 Call ID: 935e909f-cb7e-4e05-998f-a69fc07feabd
  Args:
    relation: :hasSon
    source: Kira-Marina_Liepsner
    target: Andreas_Felix_Paul_von_Bismarck
  Finish (afa12005-f7f1-4f34-bd1e-20c7a89084b4)
 Call ID: afa12005-f7f1-4f34-bd1e-20c7a89084b4
  Args: