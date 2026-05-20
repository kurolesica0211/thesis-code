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
Prince Lennart Bernadotte, Count of Wisborg (born Prince Lennart of Sweden, Duke of Småland; 8 May 1909 – 21 December 2004) was a Swedish-German landscaper, filmmaker, photographer and was a grandson of King Gustaf V of Sweden.
He was born at the Royal Palace in Stockholm, to Prince Wilhelm, Duke of Södermanland, and Grand Duchess Maria Pavlovna of Russia.
At birth Bernadotte was a Swedish prince and was titled Duke of Småland.
Thus, he was called Mr. Bernadotte as a result.
Title

Under the Swedish Act of Succession, a prince or princess marrying without the consent of the monarch and government forfeits the right of succession for themselves and their descendants.
In a new policy adopted in the case of Lennart Bernadotte, they were also forbidden to use their titles and told to use the surname of Bernadotte.
By his marriage on 11 March 1932 Prince Lennart consequently, as far as Swedish records were concerned, was to be called Mr. Lennart Bernadotte.
On 2 July 1951, for himself, his wife and his marital descendants, Bernadotte was admitted by Grand Duchess Charlotte (head of state at the time) into the nobility of Luxembourg as Count of Wisborg and in that conferral was also called Gustaf Lennart Nicolas Paul Prince Bernadotte.
It has been reported (without accuracy) that Lennart and his cousin Sigvard Bernadotte wanted King Carl XVI Gustaf of Sweden to restore their royal titles, which he could have done, but that he chose not to do so; no such request was actually ever made however.
Career

In 1944 Bernadotte portrayed the young Crown Prince Carl of Sweden and Norway in the historical film Prince Gustaf, Bernadotte's only screen acting role.
He served as head of the Sveriges Scoutförbund (Scouting Association of Sweden) from 1948 to 1951


Lennart Bernadotte concentrated his energy on his estate on the island of Mainau in Lake Constance, Germany, where he died, and on his charitable fund, the Lennart Bernadotte Stiftung.
Family

In London on 11 March 1932, Bernadotte married firstly Karin Emma Louise Nissvandt (7 July 1911 – 9 September 1991).
In Mainau on 29 April 1972, Bernadotte married Sonja Anita Maria Haunz (7 May 1944 – 21 October 2008).
Bernadotte died on 21 December 2004.



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
  AssignClass (2f833303-b82c-470b-86b5-e62a10c4f804)
 Call ID: 2f833303-b82c-470b-86b5-e62a10c4f804
  Args:
    source: :LennartBernadotte
    type: :Man
  AssignClass (a40d383f-3137-43eb-b1b6-4ce46c3b4e9b)
 Call ID: a40d383f-3137-43eb-b1b6-4ce46c3b4e9b
  Args:
    source: :LennartBernadotte
    type: :Person
  AssignClass (226ca24d-6174-4256-9fa7-4604917940ab)
 Call ID: 226ca24d-6174-4256-9fa7-4604917940ab
  Args:
    type: :Man
    source: :WilhelmDukeOfSödermanland
  AssignClass (4fb70fbd-d3da-4b42-8a51-506fe4638a9f)
 Call ID: 4fb70fbd-d3da-4b42-8a51-506fe4638a9f
  Args:
    type: :Person
    source: :WilhelmDukeOfSödermanland
  AssignClass (459c3f67-48b6-49e1-b5fc-29874439415a)
 Call ID: 459c3f67-48b6-49e1-b5fc-29874439415a
  Args:
    type: :Woman
    source: :MariaPavlovnaOfRussia
  AssignClass (2f3d1b4b-e46a-4748-9c09-10e5f1d7d243)
 Call ID: 2f3d1b4b-e46a-4748-9c09-10e5f1d7d243
  Args:
    source: :MariaPavlovnaOfRussia
    type: :Person
  AssignClass (5647f1b6-78d6-41d4-a256-01e59dc1de33)
 Call ID: 5647f1b6-78d6-41d4-a256-01e59dc1de33
  Args:
    type: :Woman
    source: :KarinEmmaLouiseNissvandt
  AssignClass (6055e7f1-751a-4efb-bcc1-c38201df97a8)
 Call ID: 6055e7f1-751a-4efb-bcc1-c38201df97a8
  Args:
    source: :KarinEmmaLouiseNissvandt
    type: :Person
  AssignClass (c47d265b-38c3-4829-810f-7131706ff74c)
 Call ID: c47d265b-38c3-4829-810f-7131706ff74c
  Args:
    type: :Woman
    source: :SonjaAnitaMariaHaunz
  AssignClass (1b6dced9-ff0d-4ae5-905b-f544895724cb)
 Call ID: 1b6dced9-ff0d-4ae5-905b-f544895724cb
  Args:
    source: :SonjaAnitaMariaHaunz
    type: :Person
  AddLiteral (df92a8fe-3c47-4465-8833-c370ab84a4b6)
 Call ID: df92a8fe-3c47-4465-8833-c370ab84a4b6
  Args:
    relation: :hasSex
    source: :LennartBernadotte
    literal_value: Male
    literal_type: xsd:string
  AddLiteral (54d6d360-728d-413f-9d0b-00c34c527fe8)
 Call ID: 54d6d360-728d-413f-9d0b-00c34c527fe8
  Args:
    literal_type: xsd:string
    literal_value: Female
    source: :MariaPavlovnaOfRussia
    relation: :hasSex
  AddLiteral (771f0570-c705-417c-85b4-1fc8510f53a7)
 Call ID: 771f0570-c705-417c-85b4-1fc8510f53a7
  Args:
    literal_value: Female
    source: :KarinEmmaLouiseNissvandt
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (294fc19b-f2ba-4918-97a6-e2287610e258)
 Call ID: 294fc19b-f2ba-4918-97a6-e2287610e258
  Args:
    relation: :hasSex
    literal_type: xsd:string
    source: :SonjaAnitaMariaHaunz
    literal_value: Female
  AddLiteral (015491ca-740e-4001-8f40-d0c59238f572)
 Call ID: 015491ca-740e-4001-8f40-d0c59238f572
  Args:
    relation: :hasBirthYear
    source: :LennartBernadotte
    literal_value: 1909
    literal_type: xsd:integer
  AddLiteral (eb0ce0e5-3d51-4576-9c07-ca8018042458)
 Call ID: eb0ce0e5-3d51-4576-9c07-ca8018042458
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :LennartBernadotte
    literal_value: 2004
  AddLiteral (d1dab1c6-62f9-489f-a11a-303f21c3ee29)
 Call ID: d1dab1c6-62f9-489f-a11a-303f21c3ee29
  Args:
    source: :KarinEmmaLouiseNissvandt
    literal_value: 1991
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (9e7a6d50-2d54-4a72-9b6e-d41e98f4c37a)
 Call ID: 9e7a6d50-2d54-4a72-9b6e-d41e98f4c37a
  Args:
    source: :SonjaAnitaMariaHaunz
    literal_value: 2008
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (37f28f01-4d37-468b-a495-472f0906d408)
 Call ID: 37f28f01-4d37-468b-a495-472f0906d408
  Args:
    source: :LennartBernadotte
    target: :WilhelmDukeOfSödermanland
    relation: :hasFather
  AddTriple (ef6c11c2-566d-4390-a902-89d8eca5a989)
 Call ID: ef6c11c2-566d-4390-a902-89d8eca5a989
  Args:
    relation: :hasMother
    source: :LennartBernadotte
    target: :MariaPavlovnaOfRussia
  AddLiteral (75f35642-243c-4be2-b07b-0796156883e5)
 Call ID: 75f35642-243c-4be2-b07b-0796156883e5
  Args:
    literal_type: xsd:integer
    source: :LennartBernadotte
    literal_value: 1932
    relation: :hasMarriageYear
  AddLiteral (4c08e795-bd86-4427-9b4f-56fe3aa2b6aa)
 Call ID: 4c08e795-bd86-4427-9b4f-56fe3aa2b6aa
  Args:
    source: :LennartBernadotte
    literal_value: 1972
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (45bee78a-63e0-4484-bd52-2f05cdc4e71c)
 Call ID: 45bee78a-63e0-4484-bd52-2f05cdc4e71c
  Args: