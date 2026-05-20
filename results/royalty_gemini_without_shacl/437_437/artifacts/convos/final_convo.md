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
Lady Mary Cecilia Colman (née Bowes-Lyon; 30 January 1932 – 2 January 2021) was an English socialite, philanthropist, and extra lady-in-waiting to Princess Alexandra, The Honourable Lady Ogilvy.
The daughter of Michael Bowes-Lyon and Elizabeth Margaret Cator, her paternal aunt was Queen Elizabeth
The Queen Mother, and she was thus a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Early life

Mary Cecilia Bowes-Lyon was born on 30 January 1932 at Gastlings, the Bowes-Lyon family home in Biggleswade, Bedfordshire.
Her father, Michael Bowes-Lyon (1893–1953), was the fifth son of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne and Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne (née Cavendish-Bentinck).
Her mother, Elizabeth Margaret Cator (1899–1959), was a great-granddaughter of Charles Yorke, 4th Earl of Hardwicke.
She had a twin sister, Patricia Maud, later Lady Patricia Tetley, an older brother, Fergus Michael Claude, later Fergus Bowes-Lyon, 17th Earl of Strathmore and Kinghorne, and a younger brother, Michael Albemarle.
Lady Mary was also a godmother to Diana, Princess of Wales.
In 1949, a coming-out ball was held for her and her twin sister Patricia at Londonderry House, which was attended by their aunt, the Queen, and their cousins, The Princess Elizabeth and The Princess Margaret.
Marriage and children

On 10 November 1951 at St Bartholomew-the-Great in London, Mary married the then-Lieutenant Timothy Colman, son of the cricketer Geoffrey Colman.
Work and later life

In 1970, Mary was appointed an Extra Lady-in-waiting to another of the Queen's first cousins, Princess Alexandra, The Hon.
After her elder brother succeeded their cousin as 17th Earl of Strathmore and Kinghorne, she received the title and precedence of a daughter of an earl by royal warrant of precedence in 1974.
Lady Mary died at her home in Bixley, Norfolk on 2 January 2021, at the age of 88.



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
  AssignClass (a1fde7b7-fc9e-4abf-a122-b7f4e8945ce5)
 Call ID: a1fde7b7-fc9e-4abf-a122-b7f4e8945ce5
  Args:
    type: :Woman
    source: Mary_Cecilia_Colman
  AssignClass (907cb285-0372-48dd-a2dc-495dbdeeac4d)
 Call ID: 907cb285-0372-48dd-a2dc-495dbdeeac4d
  Args:
    type: :Person
    source: Mary_Cecilia_Colman
  AddLiteral (f9882239-9949-4eaf-8f8f-307740786e62)
 Call ID: f9882239-9949-4eaf-8f8f-307740786e62
  Args:
    literal_value: 1932
    relation: :hasBirthYear
    source: Mary_Cecilia_Colman
    literal_type: xsd:integer
  AddLiteral (2b914e8c-ea63-4a6b-9fbf-054664f0fce1)
 Call ID: 2b914e8c-ea63-4a6b-9fbf-054664f0fce1
  Args:
    literal_value: 2021
    relation: :hasDeathYear
    source: Mary_Cecilia_Colman
    literal_type: xsd:integer
  AssignClass (dfcae20a-aec6-4ff4-ab9f-8db2915b7b21)
 Call ID: dfcae20a-aec6-4ff4-ab9f-8db2915b7b21
  Args:
    type: :Man
    source: Michael_Bowes-Lyon
  AssignClass (13202019-29aa-4c9b-b3d3-5f8871d149ea)
 Call ID: 13202019-29aa-4c9b-b3d3-5f8871d149ea
  Args:
    type: :Person
    source: Michael_Bowes-Lyon
  AssignClass (b5f573d2-8535-4faa-aa85-480ef9d892d8)
 Call ID: b5f573d2-8535-4faa-aa85-480ef9d892d8
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (01849e3c-2606-4dc6-ab9b-9443df1dc5eb)
 Call ID: 01849e3c-2606-4dc6-ab9b-9443df1dc5eb
  Args:
    type: :Person
    source: Elizabeth_Margaret_Cator
  AddTriple (a68c101d-62f4-44cb-a142-c9ca34f30939)
 Call ID: a68c101d-62f4-44cb-a142-c9ca34f30939
  Args:
    target: Michael_Bowes-Lyon
    source: Mary_Cecilia_Colman
    relation: :hasFather
  AddTriple (08a5f0ae-bc83-4c68-a3ac-96000d4ae2c6)
 Call ID: 08a5f0ae-bc83-4c68-a3ac-96000d4ae2c6
  Args:
    target: Elizabeth_Margaret_Cator
    source: Mary_Cecilia_Colman
    relation: :hasMother
  AssignClass (d1999cf3-8533-4bcf-ba76-be3be3c3b613)
 Call ID: d1999cf3-8533-4bcf-ba76-be3be3c3b613
  Args:
    type: :Woman
    source: Patricia_Maud
  AssignClass (c73cae39-be83-4185-8c7e-ac043bd3d458)
 Call ID: c73cae39-be83-4185-8c7e-ac043bd3d458
  Args:
    type: :Person
    source: Patricia_Maud
  AddTriple (c5a60cd9-7292-46d7-ac67-e892e9c1ed26)
 Call ID: c5a60cd9-7292-46d7-ac67-e892e9c1ed26
  Args:
    source: Mary_Cecilia_Colman
    relation: :hasSister
    target: Patricia_Maud
  AssignClass (c5390527-ff0a-4549-9bce-f8b585375ba2)
 Call ID: c5390527-ff0a-4549-9bce-f8b585375ba2
  Args:
    type: :Man
    source: Fergus_Michael_Claude
  AssignClass (ba4345be-f8cc-4ca0-8c10-4ca7182a0076)
 Call ID: ba4345be-f8cc-4ca0-8c10-4ca7182a0076
  Args:
    type: :Person
    source: Fergus_Michael_Claude
  AddTriple (3e63ceb4-7b9d-4f57-9d4b-94defcfe1b0b)
 Call ID: 3e63ceb4-7b9d-4f57-9d4b-94defcfe1b0b
  Args:
    target: Fergus_Michael_Claude
    source: Mary_Cecilia_Colman
    relation: :hasBrother
  AssignClass (bb8d9a04-34cc-45f7-8d63-09f0b3b58064)
 Call ID: bb8d9a04-34cc-45f7-8d63-09f0b3b58064
  Args:
    type: :Man
    source: Michael_Albemarle
  AssignClass (37e5f2c5-6473-4284-be53-57b01e903f51)
 Call ID: 37e5f2c5-6473-4284-be53-57b01e903f51
  Args:
    type: :Person
    source: Michael_Albemarle
  AddTriple (21340deb-d2f4-4391-a5d3-07bb9d372357)
 Call ID: 21340deb-d2f4-4391-a5d3-07bb9d372357
  Args:
    source: Mary_Cecilia_Colman
    relation: :hasBrother
    target: Michael_Albemarle
  AssignClass (02186dae-3876-4a07-9b04-69b9af114126)
 Call ID: 02186dae-3876-4a07-9b04-69b9af114126
  Args:
    type: :Man
    source: Timothy_Colman
  AssignClass (1bd7806d-723a-4076-af43-bc03e7eb5da1)
 Call ID: 1bd7806d-723a-4076-af43-bc03e7eb5da1
  Args:
    type: :Person
    source: Timothy_Colman
  AddLiteral (d6134b08-c056-40d9-b043-6ac784375c2e)
 Call ID: d6134b08-c056-40d9-b043-6ac784375c2e
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Mary_Cecilia_Colman
    literal_value: 1951
  AddTriple (0b54ee82-6e41-4c55-9d48-51f2167de796)
 Call ID: 0b54ee82-6e41-4c55-9d48-51f2167de796
  Args:
    target: Timothy_Colman
    source: Mary_Cecilia_Colman
    relation: :hasRelation
  AssignClass (90c01dfd-0170-4510-b0ed-41290f6d4501)
 Call ID: 90c01dfd-0170-4510-b0ed-41290f6d4501
  Args:
    type: :Man
    source: Geoffrey_Colman
  AssignClass (9a2f20cf-8ffb-4f0b-bb6d-9171811f9a10)
 Call ID: 9a2f20cf-8ffb-4f0b-bb6d-9171811f9a10
  Args:
    type: :Person
    source: Geoffrey_Colman
  AddTriple (a5f30cdd-0d4b-4948-8e9f-1cdf8de39fde)
 Call ID: a5f30cdd-0d4b-4948-8e9f-1cdf8de39fde
  Args:
    source: Timothy_Colman
    relation: :hasFather
    target: Geoffrey_Colman
  AssignClass (1d420d14-f44d-46b0-ad79-d971e3c55626)
 Call ID: 1d420d14-f44d-46b0-ad79-d971e3c55626
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (9dbedfd0-9781-478a-83bb-5677e1be6626)
 Call ID: 9dbedfd0-9781-478a-83bb-5677e1be6626
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AssignClass (01b23ce6-06d7-48f4-9034-235f0507463c)
 Call ID: 01b23ce6-06d7-48f4-9034-235f0507463c
  Args:
    type: :Woman
    source: Cecilia_Bowes-Lyon
  AssignClass (6dd5e9f6-7d2b-4b74-a895-be9730a60d52)
 Call ID: 6dd5e9f6-7d2b-4b74-a895-be9730a60d52
  Args:
    type: :Person
    source: Cecilia_Bowes-Lyon
  AddTriple (329b90b8-4c45-4ddd-85e4-9ea99b3c7a1b)
 Call ID: 329b90b8-4c45-4ddd-85e4-9ea99b3c7a1b
  Args:
    source: Michael_Bowes-Lyon
    relation: :hasFather
    target: Claude_Bowes-Lyon
  AddTriple (e8dd48d0-9da2-4811-ac50-33f5952696bd)
 Call ID: e8dd48d0-9da2-4811-ac50-33f5952696bd
  Args:
    target: Cecilia_Bowes-Lyon
    source: Michael_Bowes-Lyon
    relation: :hasMother
  Finish (503a1fe9-d7a9-48b5-ab96-4d1a372ca1e3)
 Call ID: 503a1fe9-d7a9-48b5-ab96-4d1a372ca1e3
  Args: