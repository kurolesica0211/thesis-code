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
Klaus Felix von Amsberg (German: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg; 1 September 1890 – 19 December 1953) was a member of the German Niederer Adel (lower nobility) and father of Prince Claus of the Netherlands.
Early life

He was born at Rehna, Mecklenburg-Schwerin, German Empire (now Mecklenburg-Vorpommern, Germany), the first child of Wilhelm von Amsberg (1856–1929), by his marriage to Elise von Vieregg (1866–1951), member of an old aristocratic family.
Claus was from 1917 the steward of an estate after a failed venture in Africa as a planter.
Marriage

Claus married on 4 September 1924 at Hitzacker to Baroness Gösta von dem Bussche-Haddenhausen (26 January 1902 –
13 June 1996), daughter of Baron Georg von dem Bussche-Haddenhausen (1869–1923) and Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).



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
  AssignClass (08fb98e8-5411-4e78-b16d-393eff97d51d)
 Call ID: 08fb98e8-5411-4e78-b16d-393eff97d51d
  Args:
    type: :Man
    source: Klaus_Felix_von_Amsberg
  AssignClass (e3a12000-46fa-40ba-9119-4fecbbce2fdb)
 Call ID: e3a12000-46fa-40ba-9119-4fecbbce2fdb
  Args:
    source: Klaus_Felix_von_Amsberg
    type: :Person
  AssignClass (2fe9f69a-9bbd-45d0-90b9-eaee0e52be17)
 Call ID: 2fe9f69a-9bbd-45d0-90b9-eaee0e52be17
  Args:
    type: :Ancestor
    source: Klaus_Felix_von_Amsberg
  AddLiteral (8fa31847-92e9-4acd-8219-11dd62cf70aa)
 Call ID: 8fa31847-92e9-4acd-8219-11dd62cf70aa
  Args:
    literal_type: xsd:integer
    source: Klaus_Felix_von_Amsberg
    literal_value: 1890
    relation: :hasBirthYear
  AddLiteral (737ddd7b-0c9e-4182-b690-3c3747053bae)
 Call ID: 737ddd7b-0c9e-4182-b690-3c3747053bae
  Args:
    literal_value: 1953
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Klaus_Felix_von_Amsberg
  AddLiteral (f5b95df8-30f8-4a6c-ac87-89b6ae729c8b)
 Call ID: f5b95df8-30f8-4a6c-ac87-89b6ae729c8b
  Args:
    source: Klaus_Felix_von_Amsberg
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg
  AssignClass (1f1f2000-1ae5-4578-9cac-b5bb131f26f2)
 Call ID: 1f1f2000-1ae5-4578-9cac-b5bb131f26f2
  Args:
    source: Wilhelm_von_Amsberg
    type: :Man
  AssignClass (03847dcd-cd9e-4a5a-86ff-376b45d39b59)
 Call ID: 03847dcd-cd9e-4a5a-86ff-376b45d39b59
  Args:
    type: :Person
    source: Wilhelm_von_Amsberg
  AssignClass (545d876b-f478-40c1-8485-fa84b351d78f)
 Call ID: 545d876b-f478-40c1-8485-fa84b351d78f
  Args:
    source: Wilhelm_von_Amsberg
    type: :Ancestor
  AddLiteral (893ae494-8245-4ed7-93be-a32243cd129f)
 Call ID: 893ae494-8245-4ed7-93be-a32243cd129f
  Args:
    relation: :hasBirthYear
    literal_value: 1856
    source: Wilhelm_von_Amsberg
    literal_type: xsd:integer
  AddLiteral (1665508e-1cf5-40dd-9e1b-89dd78ad5c80)
 Call ID: 1665508e-1cf5-40dd-9e1b-89dd78ad5c80
  Args:
    literal_type: xsd:integer
    source: Wilhelm_von_Amsberg
    literal_value: 1929
    relation: :hasDeathYear
  AssignClass (ca127eb0-e7ba-43c3-8ba3-c08bdb395b03)
 Call ID: ca127eb0-e7ba-43c3-8ba3-c08bdb395b03
  Args:
    source: Elise_von_Vieregg
    type: :Woman
  AssignClass (ae7a7216-7a02-4f3f-8146-a73357abf4a8)
 Call ID: ae7a7216-7a02-4f3f-8146-a73357abf4a8
  Args:
    source: Elise_von_Vieregg
    type: :Person
  AssignClass (b484650b-feca-481c-b35e-feade84833ea)
 Call ID: b484650b-feca-481c-b35e-feade84833ea
  Args:
    source: Elise_von_Vieregg
    type: :Ancestor
  AddLiteral (2d90ac42-7afb-4bfc-bb05-be23d9ade08d)
 Call ID: 2d90ac42-7afb-4bfc-bb05-be23d9ade08d
  Args:
    literal_value: 1866
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Elise_von_Vieregg
  AddLiteral (4c129b60-d6e3-4f12-b423-66f0932214d1)
 Call ID: 4c129b60-d6e3-4f12-b423-66f0932214d1
  Args:
    relation: :hasDeathYear
    literal_value: 1951
    source: Elise_von_Vieregg
    literal_type: xsd:integer
  AddTriple (fe7e2b9c-9cc5-4d81-86ba-602e55366d8b)
 Call ID: fe7e2b9c-9cc5-4d81-86ba-602e55366d8b
  Args:
    relation: :hasFather
    target: Wilhelm_von_Amsberg
    source: Klaus_Felix_von_Amsberg
  AddTriple (57e9536f-20ab-4556-875f-2537eec4be77)
 Call ID: 57e9536f-20ab-4556-875f-2537eec4be77
  Args:
    relation: :hasMother
    source: Klaus_Felix_von_Amsberg
    target: Elise_von_Vieregg
  AssignClass (65cd6c5a-2faf-420a-8744-73fe83ae2e13)
 Call ID: 65cd6c5a-2faf-420a-8744-73fe83ae2e13
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (526a5783-283b-41ba-9bc3-0f2acef83620)
 Call ID: 526a5783-283b-41ba-9bc3-0f2acef83620
  Args:
    type: :Person
    source: Prince_Claus_of_the_Netherlands
  AddTriple (e3c1d4ca-efed-4a3a-8512-38ccb9da3270)
 Call ID: e3c1d4ca-efed-4a3a-8512-38ccb9da3270
  Args:
    source: Klaus_Felix_von_Amsberg
    target: Prince_Claus_of_the_Netherlands
    relation: :isFatherOf
  AssignClass (43bdaa2a-fecf-4129-9d63-2eed3239a11f)
 Call ID: 43bdaa2a-fecf-4129-9d63-2eed3239a11f
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (e5ff9d3e-e10b-4744-9767-51da3e40cc7d)
 Call ID: e5ff9d3e-e10b-4744-9767-51da3e40cc7d
  Args:
    type: :Person
    source: Gosta_von_dem_Bussche-Haddenhausen
  AssignClass (ff4a3f60-f4d6-4e32-9b4a-da7c40c196c8)
 Call ID: ff4a3f60-f4d6-4e32-9b4a-da7c40c196c8
  Args:
    type: :Ancestor
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddLiteral (56635d2b-0b4b-4c59-8f26-68131d6bbd88)
 Call ID: 56635d2b-0b4b-4c59-8f26-68131d6bbd88
  Args:
    literal_type: xsd:integer
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_value: 1902
    relation: :hasBirthYear
  AddLiteral (a3b16264-b668-4320-b37f-38bbef652ead)
 Call ID: a3b16264-b668-4320-b37f-38bbef652ead
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
  AddLiteral (84d4d98e-8e7a-4936-adc5-3557e4dcbd2a)
 Call ID: 84d4d98e-8e7a-4936-adc5-3557e4dcbd2a
  Args:
    source: Klaus_Felix_von_Amsberg
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1924
  AddTriple (95406625-81c5-4d54-ae33-ca2c2530932e)
 Call ID: 95406625-81c5-4d54-ae33-ca2c2530932e
  Args:
    relation: :hasRelation
    source: Klaus_Felix_von_Amsberg
    target: Gosta_von_dem_Bussche-Haddenhausen
  AssignClass (e9f98954-d5b1-41df-98f6-89102625ace9)
 Call ID: e9f98954-d5b1-41df-98f6-89102625ace9
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (7d5d8c9b-df64-42c6-851f-c7727a83db3e)
 Call ID: 7d5d8c9b-df64-42c6-851f-c7727a83db3e
  Args:
    type: :Person
    source: Georg_von_dem_Bussche-Haddenhausen
  AssignClass (d4d5ded7-d3bf-43aa-9627-38603d3be615)
 Call ID: d4d5ded7-d3bf-43aa-9627-38603d3be615
  Args:
    type: :Ancestor
    source: Georg_von_dem_Bussche-Haddenhausen
  AddLiteral (2400fec1-ceeb-4b35-8e82-afd21cb52b72)
 Call ID: 2400fec1-ceeb-4b35-8e82-afd21cb52b72
  Args:
    literal_type: xsd:integer
    source: Georg_von_dem_Bussche-Haddenhausen
    literal_value: 1869
    relation: :hasBirthYear
  AddLiteral (1187870c-185c-4249-a45a-e42c642fae2f)
 Call ID: 1187870c-185c-4249-a45a-e42c642fae2f
  Args:
    relation: :hasDeathYear
    literal_value: 1923
    source: Georg_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AssignClass (0e41452a-0a6b-40b0-8f09-1e865720d015)
 Call ID: 0e41452a-0a6b-40b0-8f09-1e865720d015
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    type: :Woman
  AssignClass (020cd941-28c5-4fc6-b17a-2289e8359dbb)
 Call ID: 020cd941-28c5-4fc6-b17a-2289e8359dbb
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    type: :Person
  AssignClass (0b78cc34-7bac-41fb-ac83-b82ffcfc5c1e)
 Call ID: 0b78cc34-7bac-41fb-ac83-b82ffcfc5c1e
  Args:
    type: :Ancestor
    source: Gabriele_von_dem_Bussche-Ippenburg
  AddLiteral (2928b7be-2c6a-49ad-8b1c-bf86d980e307)
 Call ID: 2928b7be-2c6a-49ad-8b1c-bf86d980e307
  Args:
    literal_type: xsd:integer
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_value: 1877
    relation: :hasBirthYear
  AddLiteral (01170919-7c17-4bed-9ca6-929d38cbb408)
 Call ID: 01170919-7c17-4bed-9ca6-929d38cbb408
  Args:
    relation: :hasDeathYear
    literal_value: 1973
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_type: xsd:integer
  AddTriple (70f114c9-aef5-423e-b223-93463aacf7e1)
 Call ID: 70f114c9-aef5-423e-b223-93463aacf7e1
  Args:
    relation: :hasFather
    target: Georg_von_dem_Bussche-Haddenhausen
    source: Gosta_von_dem_Bussche-Haddenhausen
  AddTriple (ddc45c90-3b15-4c1e-aaf2-6f72f88f2863)
 Call ID: ddc45c90-3b15-4c1e-aaf2-6f72f88f2863
  Args:
    target: Gabriele_von_dem_Bussche-Ippenburg
    source: Gosta_von_dem_Bussche-Haddenhausen
    relation: :hasMother
  Finish (9efed486-ff1d-40d8-8659-e51b60159e24)
 Call ID: 9efed486-ff1d-40d8-8659-e51b60159e24
  Args: