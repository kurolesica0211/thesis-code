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
Berthold Prinz und Markgraf von Baden (24 February 1906 – 27 October 1963), styled Margrave of Baden and Duke of Zähringen, was the head of the House of Baden, which had reigned over the Grand Duchy of Baden until 1918, from 1929 until his death.
He was the brother-in-law of Prince Philip, Duke of Edinburgh, through his marriage to Philip's sister, Princess Theodora of Greece and Denmark.
Marriage and children

The only son and younger child of Prince Maximilian, Margrave of Baden and Princess Marie Louise of Hanover, Berthold married his second cousin Princess Theodora of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, on 17 August 1931 in Baden-Baden.
Via his marriage, he was the brother-in-law of Prince Philip of Greece and Denmark, later Prince Philip, Duke of Edinburgh from November 1947.
His bride was also his second cousin, through Christian IX of Denmark.
Death

Berthold died on 27 October 1963, aged 57, in Spaichingen.
He was succeeded as titular margrave and head of house by his son Max.



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
  AssignClass (0e6eb3ad-216a-4298-bbfb-aa896a1c0250)
 Call ID: 0e6eb3ad-216a-4298-bbfb-aa896a1c0250
  Args:
    type: :Man
    source: Berthold
  AssignClass (d58b6a72-e0d2-45ff-af5c-34a119db3cbf)
 Call ID: d58b6a72-e0d2-45ff-af5c-34a119db3cbf
  Args:
    type: :Person
    source: Berthold
  AddLiteral (65d762f9-65a4-4b44-9927-104cba85139b)
 Call ID: 65d762f9-65a4-4b44-9927-104cba85139b
  Args:
    source: Berthold
    literal_value: 1906
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (22655910-f497-416f-8897-31bea282b3b1)
 Call ID: 22655910-f497-416f-8897-31bea282b3b1
  Args:
    literal_value: 1963
    source: Berthold
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (8efbc010-c449-4229-aebf-355aa8e98f0d)
 Call ID: 8efbc010-c449-4229-aebf-355aa8e98f0d
  Args:
    type: :Man
    source: Maximilian
  AssignClass (fe99961a-50ad-4e49-a22f-195a625bfa10)
 Call ID: fe99961a-50ad-4e49-a22f-195a625bfa10
  Args:
    type: :Person
    source: Maximilian
  AssignClass (b7806dab-5919-4fb5-acb3-67bf166217bb)
 Call ID: b7806dab-5919-4fb5-acb3-67bf166217bb
  Args:
    source: MarieLouise
    type: :Woman
  AssignClass (125d4109-5394-4909-afba-cde436fa8e7c)
 Call ID: 125d4109-5394-4909-afba-cde436fa8e7c
  Args:
    type: :Person
    source: MarieLouise
  AddTriple (9b28e192-6cb3-4b3a-ac46-5b2b6ac0bee9)
 Call ID: 9b28e192-6cb3-4b3a-ac46-5b2b6ac0bee9
  Args:
    source: Berthold
    target: Maximilian
    relation: :hasFather
  AddTriple (9df1d301-30b2-4aab-b008-ea018bb6fe55)
 Call ID: 9df1d301-30b2-4aab-b008-ea018bb6fe55
  Args:
    source: Berthold
    target: MarieLouise
    relation: :hasMother
  AssignClass (f1ad94e8-f822-4ed0-b921-4d85e7d3ab26)
 Call ID: f1ad94e8-f822-4ed0-b921-4d85e7d3ab26
  Args:
    type: :Woman
    source: Theodora
  AssignClass (04cdb38b-17ce-4154-834c-28e57f33d104)
 Call ID: 04cdb38b-17ce-4154-834c-28e57f33d104
  Args:
    type: :Person
    source: Theodora
  AddTriple (4eb372c4-307a-488d-9546-384c4dbf96dc)
 Call ID: 4eb372c4-307a-488d-9546-384c4dbf96dc
  Args:
    source: Berthold
    target: Theodora
    relation: :hasRelation
  AddLiteral (2261b7fd-793c-4626-80e4-45e3f18a68b3)
 Call ID: 2261b7fd-793c-4626-80e4-45e3f18a68b3
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Berthold
    literal_value: 1931
  AssignClass (d6aecfdb-517b-4887-bf1e-093dd7c933f1)
 Call ID: d6aecfdb-517b-4887-bf1e-093dd7c933f1
  Args:
    type: :Man
    source: Andrew
  AssignClass (05a1ed3f-1eed-4120-9876-2335339872b1)
 Call ID: 05a1ed3f-1eed-4120-9876-2335339872b1
  Args:
    source: Andrew
    type: :Person
  AssignClass (9f87a0f1-653f-417e-8b3c-92e36dbc923f)
 Call ID: 9f87a0f1-653f-417e-8b3c-92e36dbc923f
  Args:
    source: Alice
    type: :Woman
  AssignClass (0cf7d108-f15c-46a0-bf8b-f0d5ec198553)
 Call ID: 0cf7d108-f15c-46a0-bf8b-f0d5ec198553
  Args:
    type: :Person
    source: Alice
  AddTriple (05a110f8-ed8c-43f8-b78b-4d39a0fef97f)
 Call ID: 05a110f8-ed8c-43f8-b78b-4d39a0fef97f
  Args:
    relation: :hasFather
    source: Theodora
    target: Andrew
  AddTriple (d8e89bc2-f47b-42ee-9c26-07db0ace6add)
 Call ID: d8e89bc2-f47b-42ee-9c26-07db0ace6add
  Args:
    relation: :hasMother
    source: Theodora
    target: Alice
  AssignClass (de7fe412-9291-4a11-a69e-87a263a6bdee)
 Call ID: de7fe412-9291-4a11-a69e-87a263a6bdee
  Args:
    type: :Man
    source: Philip
  AssignClass (68b8ac42-08c3-454c-b59d-1db4e7d7fdde)
 Call ID: 68b8ac42-08c3-454c-b59d-1db4e7d7fdde
  Args:
    source: Philip
    type: :Person
  AddTriple (206061ac-3e58-43ad-a626-d0f9b0fcae12)
 Call ID: 206061ac-3e58-43ad-a626-d0f9b0fcae12
  Args:
    relation: :isBrotherOf
    target: Theodora
    source: Philip
  AssignClass (cfdb0e7a-b933-4ca2-88cf-56004aca3d87)
 Call ID: cfdb0e7a-b933-4ca2-88cf-56004aca3d87
  Args:
    source: Max
    type: :Man
  AssignClass (d95da101-9ed1-43c1-b8a5-a83778abf33a)
 Call ID: d95da101-9ed1-43c1-b8a5-a83778abf33a
  Args:
    source: Max
    type: :Person
  AddTriple (aabc558f-b256-40a4-aa3d-d86ba42cf29f)
 Call ID: aabc558f-b256-40a4-aa3d-d86ba42cf29f
  Args:
    target: Berthold
    source: Max
    relation: :isSonOf
  Finish (25af526e-9829-47bc-aeda-6cf7286837d0)
 Call ID: 25af526e-9829-47bc-aeda-6cf7286837d0
  Args: