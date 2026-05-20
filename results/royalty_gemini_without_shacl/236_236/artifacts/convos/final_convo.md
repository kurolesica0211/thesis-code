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
Duke Friedrich August of Oldenburg (11 January 1936 – 9 July 2017) was a member of the House of Holstein-Gottorp.
He is a son of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.
Family and early life

Frederich August is the sixth child and fourth son of Nikolaus, Hereditary Grand Duke of Oldenburg and his first wife Princess Helena of Waldeck and Pyrmont.
His paternal grandparents are Frederick Augustus II, Grand Duke of Oldenburg and Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin.
His maternal grandparents are Friedrich, Prince of Waldeck and Pyrmont and Princess Bathildis of Schaumburg-Lippe.
His grandfather was overthrown as Grand Duke of Oldenburg in 1918, at the end of World War I.
His father Nikolaus thus never legally succeeded to the title when the deposed Grand Duke died in 1931.
Friedrich is an uncle of Christian, Duke of Oldenburg, the current head of the House of Oldenburg.
Marriage and issue

Friedrich August's first wife was Princess Marie Cécile of Prussia, a daughter of Louis Ferdinand, Prince of Prussia (second son of William, German Crown Prince) and his wife, Grand Duchess Kira Kirillovna of Russia.
Friedrich August and Marie-Cécile have three children: a son, and two daughters.
Marie-Cécile and Friedrich August divorced on 23 November 1989.
On 9 February 1991, Friedrich August was remarried to Donata Countess of Castell-Rüdenhausen in Rüdenhausen, Germany.



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
  AssignClass (0e6f2417-7dee-429d-b5e9-aa457970a8ca)
 Call ID: 0e6f2417-7dee-429d-b5e9-aa457970a8ca
  Args:
    type: :Man
    source: Friedrich_August_of_Oldenburg
  AssignClass (835a754e-2ab8-439b-a952-cf593a40ff81)
 Call ID: 835a754e-2ab8-439b-a952-cf593a40ff81
  Args:
    source: Nikolaus_of_Oldenburg
    type: :Man
  AssignClass (ccd264de-dd3b-4b5e-9e8a-3d6be8d66fb8)
 Call ID: ccd264de-dd3b-4b5e-9e8a-3d6be8d66fb8
  Args:
    type: :Woman
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (aa6d1902-7ae3-4ec7-8532-b4e00bbfb296)
 Call ID: aa6d1902-7ae3-4ec7-8532-b4e00bbfb296
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    type: :Man
  AssignClass (e73f3212-7941-40ea-909f-011f4b329e9f)
 Call ID: e73f3212-7941-40ea-909f-011f4b329e9f
  Args:
    type: :Woman
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (c8ecbace-0246-4abe-9c70-71ed2b71d77a)
 Call ID: c8ecbace-0246-4abe-9c70-71ed2b71d77a
  Args:
    source: Friedrich_of_Waldeck_and_Pyrmont
    type: :Man
  AssignClass (bf991610-ac15-4cc2-94ae-0b1887c05d70)
 Call ID: bf991610-ac15-4cc2-94ae-0b1887c05d70
  Args:
    type: :Woman
    source: Bathildis_of_Schaumburg-Lippe
  AssignClass (13fa4ce9-3535-46ed-adb8-44c24beb03a7)
 Call ID: 13fa4ce9-3535-46ed-adb8-44c24beb03a7
  Args:
    source: Christian_of_Oldenburg
    type: :Man
  AssignClass (71a6167d-03ee-4868-8722-8a0c31d5261a)
 Call ID: 71a6167d-03ee-4868-8722-8a0c31d5261a
  Args:
    source: Marie_Cecile_of_Prussia
    type: :Woman
  AssignClass (860115c9-ea30-416d-aa81-1099e8dd2ba5)
 Call ID: 860115c9-ea30-416d-aa81-1099e8dd2ba5
  Args:
    type: :Man
    source: Louis_Ferdinand_of_Prussia
  AssignClass (2721a568-e2d7-432c-9efe-3a49bdabc83c)
 Call ID: 2721a568-e2d7-432c-9efe-3a49bdabc83c
  Args:
    source: William_German_Crown_Prince
    type: :Man
  AssignClass (deefac90-6a8f-4195-b265-9f8e0ac25e80)
 Call ID: deefac90-6a8f-4195-b265-9f8e0ac25e80
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Woman
  AssignClass (e31777f3-cc9e-4866-b679-191ba0780913)
 Call ID: e31777f3-cc9e-4866-b679-191ba0780913
  Args:
    type: :Woman
    source: Donata_of_Castell-Rudenhausen
  AddLiteral (992f247e-1897-462b-bfd7-9854c7149cb9)
 Call ID: 992f247e-1897-462b-bfd7-9854c7149cb9
  Args:
    source: Friedrich_August_of_Oldenburg
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasBirthYear
  AddLiteral (f54c2e34-956f-4d03-b23d-1403263145d6)
 Call ID: f54c2e34-956f-4d03-b23d-1403263145d6
  Args:
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Friedrich_August_of_Oldenburg
  AddTriple (7f8aea1c-d2aa-447d-81a5-ad5aeea2e059)
 Call ID: 7f8aea1c-d2aa-447d-81a5-ad5aeea2e059
  Args:
    relation: :hasFather
    source: Friedrich_August_of_Oldenburg
    target: Nikolaus_of_Oldenburg
  AddTriple (63b61da1-0d04-43d2-a91f-d9101b45addf)
 Call ID: 63b61da1-0d04-43d2-a91f-d9101b45addf
  Args:
    source: Friedrich_August_of_Oldenburg
    relation: :hasMother
    target: Helena_of_Waldeck_and_Pyrmont
  AddTriple (5f7720c0-9de8-46e5-a267-3f4fda71defe)
 Call ID: 5f7720c0-9de8-46e5-a267-3f4fda71defe
  Args:
    target: Frederick_Augustus_II_of_Oldenburg
    source: Friedrich_August_of_Oldenburg
    relation: :hasFather
  AddTriple (8649456c-ac4f-4617-89ac-36fa8abe6273)
 Call ID: 8649456c-ac4f-4617-89ac-36fa8abe6273
  Args:
    target: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    source: Friedrich_August_of_Oldenburg
    relation: :hasMother
  AddTriple (eff2d134-abd9-4358-8262-046ada754420)
 Call ID: eff2d134-abd9-4358-8262-046ada754420
  Args:
    source: Friedrich_August_of_Oldenburg
    relation: :hasFather
    target: Friedrich_of_Waldeck_and_Pyrmont
  AddTriple (b857bda8-877b-40f8-ba41-121af79cb2d0)
 Call ID: b857bda8-877b-40f8-ba41-121af79cb2d0
  Args:
    target: Bathildis_of_Schaumburg-Lippe
    relation: :hasMother
    source: Friedrich_August_of_Oldenburg
  AddTriple (4619a76d-4a69-4d8f-b2c2-33f71c9ddcdc)
 Call ID: 4619a76d-4a69-4d8f-b2c2-33f71c9ddcdc
  Args:
    relation: :isUncleOf
    source: Friedrich_August_of_Oldenburg
    target: Christian_of_Oldenburg
  AddTriple (2ce02c29-feae-4105-b061-1d200599e3cc)
 Call ID: 2ce02c29-feae-4105-b061-1d200599e3cc
  Args:
    target: Louis_Ferdinand_of_Prussia
    relation: :hasFather
    source: Marie_Cecile_of_Prussia
  AddTriple (cb1285ea-00b6-43d0-b946-4e03d2714680)
 Call ID: cb1285ea-00b6-43d0-b946-4e03d2714680
  Args:
    target: Kira_Kirillovna_of_Russia
    relation: :hasMother
    source: Marie_Cecile_of_Prussia
  AddTriple (3a8cf348-6369-4b8e-b323-7837a437629f)
 Call ID: 3a8cf348-6369-4b8e-b323-7837a437629f
  Args:
    source: Louis_Ferdinand_of_Prussia
    relation: :hasFather
    target: William_German_Crown_Prince
  Finish (9fc8de55-f385-440b-bbb6-87c0e154e0c8)
 Call ID: 9fc8de55-f385-440b-bbb6-87c0e154e0c8
  Args: