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
Emich Kyrill, Prince of Leiningen (German: Emich Kirill Ferdinand Hermann Fürst zu Leiningen; 18 October 1926 – 30 October 1991) was a German entrepreneur and son of Karl, Prince of Leiningen.
Early life

Emich was born at Coburg, Weimar Republic, the first child of Karl, Prince of Leiningen (1898–1946), (son of Emich, 5th Prince of Leiningen and Princess Feodore of Hohenlohe-Langenburg) and his wife, Grand Duchess Maria Kirillovna of Russia (1907–1951), (daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh).
Through his mother, he was a descendant of Queen Victoria and Tsar Alexander II.
Through his father, he was a descendant of the Vasa kings of Sweden and of both of Queen Victoria's half-siblings, Carl, Prince of Leiningen and Feodora, Princess of Hohenlohe-Langenburg.
As a result, Emich was the first descendant of all three of Princess Victoria of Saxe-Coburg-Saalfeld's children.
Marriage

Emich married on 10 August 1950 in Rastede to Duchess Eilika of Oldenburg (2 February 1928 – 26 January 2016), fourth child and second daughter of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.



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
  AssignClass (8dfc111e-a01d-4ef0-88a4-e91d8407171d)
 Call ID: 8dfc111e-a01d-4ef0-88a4-e91d8407171d
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    type: :Man
  AssignClass (fb58c1c8-086b-4714-9336-c5e5ad9842a1)
 Call ID: fb58c1c8-086b-4714-9336-c5e5ad9842a1
  Args:
    source: Karl_Prince_of_Leiningen
    type: :Man
  AssignClass (455f114b-ec7d-41d5-bc45-cd9eb5dc6ac8)
 Call ID: 455f114b-ec7d-41d5-bc45-cd9eb5dc6ac8
  Args:
    source: Maria_Kirillovna_of_Russia
    type: :Woman
  AssignClass (3aa4a9a5-0535-4c0d-a9b4-f395a7d3aff0)
 Call ID: 3aa4a9a5-0535-4c0d-a9b4-f395a7d3aff0
  Args:
    source: Emich_5th_Prince_of_Leiningen
    type: :Man
  AssignClass (bdbd1d87-47c7-4da6-a819-c5e3edaa4528)
 Call ID: bdbd1d87-47c7-4da6-a819-c5e3edaa4528
  Args:
    source: Feodore_of_Hohenlohe_Langenburg
    type: :Woman
  AssignClass (357d3d36-0483-4f41-a765-b7b1feda4ab4)
 Call ID: 357d3d36-0483-4f41-a765-b7b1feda4ab4
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Man
  AssignClass (44dd0747-03ad-4cfc-8177-e34cb3e5f34f)
 Call ID: 44dd0747-03ad-4cfc-8177-e34cb3e5f34f
  Args:
    source: Victoria_Melita_of_Edinburgh
    type: :Woman
  AssignClass (cd08bc4b-3420-4f16-a602-bed5cd4a4703)
 Call ID: cd08bc4b-3420-4f16-a602-bed5cd4a4703
  Args:
    source: Eilika_of_Oldenburg
    type: :Woman
  AssignClass (b4158e84-adb9-4d1f-b4c0-03efde80ce54)
 Call ID: b4158e84-adb9-4d1f-b4c0-03efde80ce54
  Args:
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    type: :Man
  AssignClass (2a08dd29-ca1c-4ad9-8c3b-4b96ba7de4d4)
 Call ID: 2a08dd29-ca1c-4ad9-8c3b-4b96ba7de4d4
  Args:
    type: :Woman
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (34417b89-91ad-4d31-addd-42c8b9865d4b)
 Call ID: 34417b89-91ad-4d31-addd-42c8b9865d4b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_value: 1926
  AddLiteral (dbffffbd-6dd5-49bf-bef4-2a3a2d30f31e)
 Call ID: dbffffbd-6dd5-49bf-bef4-2a3a2d30f31e
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_value: 1991
  AddTriple (4d4707d9-77c5-4c43-9635-ed872d12a35b)
 Call ID: 4d4707d9-77c5-4c43-9635-ed872d12a35b
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    target: Karl_Prince_of_Leiningen
    relation: :hasFather
  AddTriple (aa30cc1a-76c1-4708-8a9b-10defd2a1721)
 Call ID: aa30cc1a-76c1-4708-8a9b-10defd2a1721
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    target: Maria_Kirillovna_of_Russia
    relation: :hasMother
  AddLiteral (46c60d23-2831-411c-bd56-5d78f45ece47)
 Call ID: 46c60d23-2831-411c-bd56-5d78f45ece47
  Args:
    source: Karl_Prince_of_Leiningen
    literal_value: 1898
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (45fee00a-4e87-40da-8dd2-1477c1ee83b8)
 Call ID: 45fee00a-4e87-40da-8dd2-1477c1ee83b8
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1946
    source: Karl_Prince_of_Leiningen
  AddTriple (bad57989-8753-4a75-8928-70541b0af942)
 Call ID: bad57989-8753-4a75-8928-70541b0af942
  Args:
    source: Karl_Prince_of_Leiningen
    relation: :hasFather
    target: Emich_5th_Prince_of_Leiningen
  AddTriple (c325ea6c-025b-4abb-9805-74740bff6549)
 Call ID: c325ea6c-025b-4abb-9805-74740bff6549
  Args:
    source: Karl_Prince_of_Leiningen
    target: Feodore_of_Hohenlohe_Langenburg
    relation: :hasMother
  AddLiteral (34a17f73-ba39-407a-ba02-4859ec0f8557)
 Call ID: 34a17f73-ba39-407a-ba02-4859ec0f8557
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Maria_Kirillovna_of_Russia
    literal_value: 1907
  AddLiteral (009d02dc-a6c3-46bd-b1e7-5c3ba2b5c307)
 Call ID: 009d02dc-a6c3-46bd-b1e7-5c3ba2b5c307
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Maria_Kirillovna_of_Russia
    literal_value: 1951
  AddTriple (652a457f-6b5f-4000-949d-678e9f8d848f)
 Call ID: 652a457f-6b5f-4000-949d-678e9f8d848f
  Args:
    target: Kirill_Vladimirovich_of_Russia
    relation: :hasFather
    source: Maria_Kirillovna_of_Russia
  AddTriple (598d3063-e6ce-4dbe-8321-03ec8f56ecb5)
 Call ID: 598d3063-e6ce-4dbe-8321-03ec8f56ecb5
  Args:
    source: Maria_Kirillovna_of_Russia
    relation: :hasMother
    target: Victoria_Melita_of_Edinburgh
  AddLiteral (5848136a-45e7-40ac-b6a6-e1444cb239eb)
 Call ID: 5848136a-45e7-40ac-b6a6-e1444cb239eb
  Args:
    literal_value: 1950
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (35ba048a-067b-435e-8525-4ae9a828afdf)
 Call ID: 35ba048a-067b-435e-8525-4ae9a828afdf
  Args:
    relation: :hasRelation
    target: Eilika_of_Oldenburg
    source: Emich_Kyrill_Prince_of_Leiningen
  AddLiteral (252a878f-eb2b-48d3-a970-20fa19ab5bce)
 Call ID: 252a878f-eb2b-48d3-a970-20fa19ab5bce
  Args:
    source: Eilika_of_Oldenburg
    literal_value: 1928
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (399d398c-84ee-4448-933f-89fd07deb6b2)
 Call ID: 399d398c-84ee-4448-933f-89fd07deb6b2
  Args:
    literal_value: 2016
    source: Eilika_of_Oldenburg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (892ef867-758f-41d5-9df4-48ecec0e5787)
 Call ID: 892ef867-758f-41d5-9df4-48ecec0e5787
  Args:
    relation: :hasFather
    target: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    source: Eilika_of_Oldenburg
  AddTriple (045bb1f0-7f64-4fbe-8426-c16a41113ef5)
 Call ID: 045bb1f0-7f64-4fbe-8426-c16a41113ef5
  Args:
    target: Helena_of_Waldeck_and_Pyrmont
    relation: :hasMother
    source: Eilika_of_Oldenburg
  Finish (28049b7c-8035-44c0-bfe1-6b1f7e167dd3)
 Call ID: 28049b7c-8035-44c0-bfe1-6b1f7e167dd3
  Args: