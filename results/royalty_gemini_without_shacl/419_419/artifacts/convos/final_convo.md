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
Friedrich Wilhelm of Lippe (German: Friedrich Wilhelm Ernst Viktor Alexander Prinz zur Lippe; born 7 September 1947) is a claimant to the headship of the House of Lippe.
Early life

Friedrich Wilhelm was born out of wedlock at Neuwied, West Germany, the first child of Prince Ernst August of Lippe (1917–1990; son of Prince Julius Ernst of Lippe and Duchess Marie of Mecklenburg-Strelitz) and his wife, Christa von Arnim (b. 1923; daughter of Curt David von Arnim and his wife, Stephanie von Stechow).
Marriage

Friedrich Wilhelm married on 18 September 1991 in Munich to Andrea Messner (b. 1966), daughter of Günther Messner, and his wife, Lieselotte Trzoska.
House of Lippe

On 30 December 1949 his father's first cousin Prince Armin succeeded his father, Leopold IV as head of the House of Lippe.
On 22 March 1953, he renounced his position in favour of his older half-brother, Prince Leopold.
Prince Leopold later in 1958 renounced the headship in favour of his older brother, Hereditary Prince Ernst.
Later in that year the Hereditary Prince called a family council where it was agreed by the princes in attendance that the oldest prince living in Germany would be head of the house.
Therefore, the position went to Prince Simon Casimir (1900–1980).
His father died in 1990 and Friedrich Wilhelm continued the claim, despite his illegitimate birth.
Prince Armin, who has said he did not think his decision in 1953 was irrevocable, also claimed to be head of the house until his death in 2015, with his son Stephan, Prince of Lippe continuing his claim.



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
  AssignClass (1d265d2c-8dd7-4a85-90b2-c2457bf48f18)
 Call ID: 1d265d2c-8dd7-4a85-90b2-c2457bf48f18
  Args:
    type: :Man
    source: FriedrichWilhelmOfLippe
  AssignClass (8cfab7a1-efea-4bb7-98f4-02f1faec8f19)
 Call ID: 8cfab7a1-efea-4bb7-98f4-02f1faec8f19
  Args:
    source: ErnstAugustOfLippe
    type: :Man
  AssignClass (0bab169f-188e-4194-8f8d-437f591262b2)
 Call ID: 0bab169f-188e-4194-8f8d-437f591262b2
  Args:
    type: :Man
    source: JuliusErnstOfLippe
  AssignClass (294a77a6-614b-4d3e-8253-1777140ceef4)
 Call ID: 294a77a6-614b-4d3e-8253-1777140ceef4
  Args:
    type: :Woman
    source: MarieOfMecklenburgStrelitz
  AssignClass (0b8f3949-e999-49c3-be30-5db4abaa167a)
 Call ID: 0b8f3949-e999-49c3-be30-5db4abaa167a
  Args:
    source: ChristaVonArnim
    type: :Woman
  AssignClass (3eb7cec0-149c-4b2e-99d1-efb530d88095)
 Call ID: 3eb7cec0-149c-4b2e-99d1-efb530d88095
  Args:
    type: :Man
    source: CurtDavidVonArnim
  AssignClass (501252b7-fb50-4564-b0e7-641eaf060f28)
 Call ID: 501252b7-fb50-4564-b0e7-641eaf060f28
  Args:
    source: StephanieVonStechow
    type: :Woman
  AssignClass (183e7254-a086-4970-bc24-d9de20bf76a8)
 Call ID: 183e7254-a086-4970-bc24-d9de20bf76a8
  Args:
    type: :Woman
    source: AndreaMessner
  AssignClass (35dd04fd-d953-4d8e-a55c-88e3249953ef)
 Call ID: 35dd04fd-d953-4d8e-a55c-88e3249953ef
  Args:
    type: :Man
    source: GüntherMessner
  AssignClass (5146fce8-bdb3-4f92-8b7e-d573ad8379a0)
 Call ID: 5146fce8-bdb3-4f92-8b7e-d573ad8379a0
  Args:
    source: LieselotteTrzoska
    type: :Woman
  AddLiteral (39713b08-d468-4fe8-9ee3-9860757f807b)
 Call ID: 39713b08-d468-4fe8-9ee3-9860757f807b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1947
    source: FriedrichWilhelmOfLippe
  AddLiteral (644c4824-9d4c-49fc-bf8b-656dcd3ffae3)
 Call ID: 644c4824-9d4c-49fc-bf8b-656dcd3ffae3
  Args:
    source: ErnstAugustOfLippe
    literal_value: 1917
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (abfca86e-daa4-4d3c-88cc-d2d1d7dc9d76)
 Call ID: abfca86e-daa4-4d3c-88cc-d2d1d7dc9d76
  Args:
    source: ErnstAugustOfLippe
    literal_value: 1990
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (a4e444bf-b60e-49ef-9ef5-b9cb8a09fd48)
 Call ID: a4e444bf-b60e-49ef-9ef5-b9cb8a09fd48
  Args:
    literal_value: 1923
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: ChristaVonArnim
  AddLiteral (539f5c02-9d78-41db-920c-318735ca6741)
 Call ID: 539f5c02-9d78-41db-920c-318735ca6741
  Args:
    literal_value: 1966
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: AndreaMessner
  AddLiteral (959891ea-aaa6-44bf-ba45-85f4d97ae403)
 Call ID: 959891ea-aaa6-44bf-ba45-85f4d97ae403
  Args:
    source: FriedrichWilhelmOfLippe
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1991
  AddTriple (f4886152-fd1b-44ea-892c-e1a3d34a0583)
 Call ID: f4886152-fd1b-44ea-892c-e1a3d34a0583
  Args:
    target: ErnstAugustOfLippe
    source: FriedrichWilhelmOfLippe
    relation: :hasFather
  AddTriple (0d247fd0-3946-419e-b8e3-c2bd2e328eaf)
 Call ID: 0d247fd0-3946-419e-b8e3-c2bd2e328eaf
  Args:
    relation: :hasMother
    source: FriedrichWilhelmOfLippe
    target: ChristaVonArnim
  AddTriple (96950808-1fd3-4a07-a528-bd8e2fc57cfc)
 Call ID: 96950808-1fd3-4a07-a528-bd8e2fc57cfc
  Args:
    relation: :hasFather
    target: JuliusErnstOfLippe
    source: ErnstAugustOfLippe
  AddTriple (bd0dba21-e20b-4a4c-a8f4-f7a467f053d5)
 Call ID: bd0dba21-e20b-4a4c-a8f4-f7a467f053d5
  Args:
    target: MarieOfMecklenburgStrelitz
    source: ErnstAugustOfLippe
    relation: :hasMother
  AddTriple (9e9c78c8-cd1c-43c3-80be-dadb854891c7)
 Call ID: 9e9c78c8-cd1c-43c3-80be-dadb854891c7
  Args:
    source: ChristaVonArnim
    target: CurtDavidVonArnim
    relation: :hasFather
  AddTriple (232a4c4e-dedc-4dc0-83d5-6db8b28da8f2)
 Call ID: 232a4c4e-dedc-4dc0-83d5-6db8b28da8f2
  Args:
    relation: :hasMother
    target: StephanieVonStechow
    source: ChristaVonArnim
  AddTriple (c36b81a2-fd30-4aac-9c38-9018e07da609)
 Call ID: c36b81a2-fd30-4aac-9c38-9018e07da609
  Args:
    relation: :hasFather
    source: AndreaMessner
    target: GüntherMessner
  AddTriple (b34bedc1-6cec-4c9a-b6db-b6ec0c8af164)
 Call ID: b34bedc1-6cec-4c9a-b6db-b6ec0c8af164
  Args:
    source: AndreaMessner
    target: LieselotteTrzoska
    relation: :hasMother
  Finish (07f18bb0-eb15-4130-a625-de558898aebb)
 Call ID: 07f18bb0-eb15-4130-a625-de558898aebb
  Args: