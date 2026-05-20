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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Princess Maria-Olympia of Greece and Denmark (Greek: Μαρία Ολυμπία Ντε Γκρες, romanized: María-Olympía de Grèce; born 25 July 1996) is a fashion model, socialite and member of the former Greek royal family.
She is the oldest child and only daughter of Pavlos, Crown Prince of Greece, and his wife, Marie-Chantal Miller.
Her paternal grandparents are Constantine II of Greece and Anne-Marie of Denmark, who were the last King and Queen of the Hellenes, while her maternal grandfather is duty free entrepreneur Robert Warren Miller.
Early life

Princess Maria-Olympia of Greece and Denmark was born on 25 July 1996 at Weill Cornell Medical Center in Lenox Hill, New York in Manhattan to Pavlos, Crown Prince of Greece, and his wife, Marie-Chantal.
Her godparents are her paternal aunt Princess Alexia of Greece and Denmark, her maternal aunt Pia Getty, her grandfather's second cousin Charles III, and Prince Michael of Greece and Denmark.
She is the older sister of Prince Constantine-Alexios, Prince Achileas-Andreas, Prince Odysseas Kimon, and Prince Aristidis-Stavros.
She uses the name Olympia in everyday life.
Olympia attended her first couture show around the age of 11 in Rome together with her parents.
Maria-Olympia registered at college in New York in the fall of 2015.
Fashion career

In April 2016, Maria-Olympia posed alongside two of her first cousins, Isabel Getty and Princess Talita
She has modeled for Teen Vogue, Town & Country, Tatler, Hello!, ¡Hola!, and W. In June 2017, Maria-Olympia walked the runway for Dolce & Gabbana.
Using her name Olympia the Saks Potts S/S 2019 show during Copenhagen Fashion Week in August 2018 was named OLYMPIA after her and opened by the princess herself as the first model on the stage.
Personal life

It was reported in May 2016 that Maria-Olympia was romantically involved with her godfather's son and third cousin once removed Prince Harry, but a representative of the British royal family denied the rumors.
On 28 September 2024, she served as a bridesmaid at the wedding of her aunt Princess Theodora of Greece and Denmark and Matthew Kumar at the Metropolitan Cathedral in Athens.
Οn 20 December 2024, Maria-Olympia acquired Greek citizenship, along with other members of the former Greek royal family, under the surname de Grèce.



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
  AssignClass (c757d5c5-1a3e-46a4-9989-a22a1b7de8b3)
 Call ID: c757d5c5-1a3e-46a4-9989-a22a1b7de8b3
  Args:
    type: :Woman
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AssignClass (44ccfbfd-5364-4ed1-aa33-bb4c86b51446)
 Call ID: 44ccfbfd-5364-4ed1-aa33-bb4c86b51446
  Args:
    type: :Person
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddLiteral (c0f9ca16-13c3-4b65-b4fe-026763b55d10)
 Call ID: c0f9ca16-13c3-4b65-b4fe-026763b55d10
  Args:
    relation: :knownAs
    literal_value: Olympia
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    literal_type: xsd:string
  AddLiteral (6e7c7e95-c731-453f-a1e2-0fe8c6a28235)
 Call ID: 6e7c7e95-c731-453f-a1e2-0fe8c6a28235
  Args:
    literal_value: 1996
    relation: :hasBirthYear
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (c3a0c9d7-e1ae-4a72-8d09-45e4c37b32a1)
 Call ID: c3a0c9d7-e1ae-4a72-8d09-45e4c37b32a1
  Args:
    type: :Man
    source: Pavlos_Crown_Prince_of_Greece
  AssignClass (bf1ee954-62ce-4d33-bb74-cb4a0f3644d8)
 Call ID: bf1ee954-62ce-4d33-bb74-cb4a0f3644d8
  Args:
    type: :Person
    source: Pavlos_Crown_Prince_of_Greece
  AssignClass (649a05c9-e2e3-41b5-80f3-79c1f52e6cae)
 Call ID: 649a05c9-e2e3-41b5-80f3-79c1f52e6cae
  Args:
    type: :Woman
    source: Marie-Chantal_Miller
  AssignClass (1e1b4ec7-4057-47ff-9631-1d31945335ef)
 Call ID: 1e1b4ec7-4057-47ff-9631-1d31945335ef
  Args:
    type: :Person
    source: Marie-Chantal_Miller
  AddTriple (dd33c60e-dc0a-49f2-83f8-b6086c787577)
 Call ID: dd33c60e-dc0a-49f2-83f8-b6086c787577
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    relation: :hasFather
    target: Pavlos_Crown_Prince_of_Greece
  AddTriple (6b1f8895-4918-4ec2-8b12-3d1d90259468)
 Call ID: 6b1f8895-4918-4ec2-8b12-3d1d90259468
  Args:
    relation: :hasMother
    target: Marie-Chantal_Miller
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AssignClass (77aa11e7-9347-4ff1-ae0a-971a8755adc6)
 Call ID: 77aa11e7-9347-4ff1-ae0a-971a8755adc6
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (456a2ac0-648e-4864-b531-c442f95e821b)
 Call ID: 456a2ac0-648e-4864-b531-c442f95e821b
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AssignClass (78b4b989-5c42-4b41-9b93-dce51583b830)
 Call ID: 78b4b989-5c42-4b41-9b93-dce51583b830
  Args:
    type: :Woman
    source: Anne-Marie_of_Denmark
  AssignClass (31563aa1-6ed8-4abe-bd38-360b86e1c39f)
 Call ID: 31563aa1-6ed8-4abe-bd38-360b86e1c39f
  Args:
    type: :Person
    source: Anne-Marie_of_Denmark
  AddTriple (57f90914-6b0e-426d-a3b8-b45f93fe66b6)
 Call ID: 57f90914-6b0e-426d-a3b8-b45f93fe66b6
  Args:
    target: Constantine_II_of_Greece
    relation: :hasFather
    source: Pavlos_Crown_Prince_of_Greece
  AddTriple (71008897-42cd-4a3a-815d-9690b3637948)
 Call ID: 71008897-42cd-4a3a-815d-9690b3637948
  Args:
    source: Pavlos_Crown_Prince_of_Greece
    target: Anne-Marie_of_Denmark
    relation: :hasMother
  AssignClass (bb59fbbf-f4bb-41f2-b5de-bb5a0d9f6315)
 Call ID: bb59fbbf-f4bb-41f2-b5de-bb5a0d9f6315
  Args:
    type: :Man
    source: Robert_Warren_Miller
  AssignClass (27d9b1f7-efb8-4fe2-bac2-d46bdfae38ba)
 Call ID: 27d9b1f7-efb8-4fe2-bac2-d46bdfae38ba
  Args:
    type: :Person
    source: Robert_Warren_Miller
  AddTriple (d1a32f51-04e5-484a-941e-393b8a78439b)
 Call ID: d1a32f51-04e5-484a-941e-393b8a78439b
  Args:
    relation: :hasFather
    target: Robert_Warren_Miller
    source: Marie-Chantal_Miller
  AssignClass (caa4a2af-267d-4f4d-a0e8-dcd1588a54d0)
 Call ID: caa4a2af-267d-4f4d-a0e8-dcd1588a54d0
  Args:
    type: :Man
    source: Prince_Constantine-Alexios
  AssignClass (482bd368-ef30-4a68-a5d0-a28a455b1bdd)
 Call ID: 482bd368-ef30-4a68-a5d0-a28a455b1bdd
  Args:
    type: :Person
    source: Prince_Constantine-Alexios
  AssignClass (69e65444-afb4-4742-abc8-c1aa7c45e10c)
 Call ID: 69e65444-afb4-4742-abc8-c1aa7c45e10c
  Args:
    type: :Man
    source: Prince_Achileas-Andreas
  AssignClass (c0b86edd-40b6-4131-aa73-b698e8792ff4)
 Call ID: c0b86edd-40b6-4131-aa73-b698e8792ff4
  Args:
    type: :Person
    source: Prince_Achileas-Andreas
  AssignClass (a49b4dfd-98fc-48c8-87c7-284402d02a8b)
 Call ID: a49b4dfd-98fc-48c8-87c7-284402d02a8b
  Args:
    type: :Man
    source: Prince_Odysseas_Kimon
  AssignClass (8afa8470-60b5-4c29-8ca5-e943637306a4)
 Call ID: 8afa8470-60b5-4c29-8ca5-e943637306a4
  Args:
    type: :Person
    source: Prince_Odysseas_Kimon
  AssignClass (558e6fa3-1bb2-43d3-801c-5d13eb72aa5c)
 Call ID: 558e6fa3-1bb2-43d3-801c-5d13eb72aa5c
  Args:
    type: :Man
    source: Prince_Aristidis-Stavros
  AssignClass (a8b9a26b-47fc-4b75-a8b0-9709f70fd873)
 Call ID: a8b9a26b-47fc-4b75-a8b0-9709f70fd873
  Args:
    type: :Person
    source: Prince_Aristidis-Stavros
  AddTriple (0732d295-4cdf-4170-a3ce-e79fe86a455b)
 Call ID: 0732d295-4cdf-4170-a3ce-e79fe86a455b
  Args:
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
    relation: :hasBrother
    target: Prince_Constantine-Alexios
  AddTriple (cffe35ef-28ed-4828-895c-e822a41cfe86)
 Call ID: cffe35ef-28ed-4828-895c-e822a41cfe86
  Args:
    relation: :hasBrother
    target: Prince_Achileas-Andreas
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddTriple (eaba64c5-5da3-4e47-b4f6-d2ea5588e94f)
 Call ID: eaba64c5-5da3-4e47-b4f6-d2ea5588e94f
  Args:
    target: Prince_Odysseas_Kimon
    relation: :hasBrother
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AddTriple (d53fbfcf-ea4d-4773-a9e4-afba0fef8a25)
 Call ID: d53fbfcf-ea4d-4773-a9e4-afba0fef8a25
  Args:
    relation: :hasBrother
    target: Prince_Aristidis-Stavros
    source: Princess_Maria-Olympia_of_Greece_and_Denmark
  AssignClass (7b6f88d0-7368-4466-91a2-4717cde571df)
 Call ID: 7b6f88d0-7368-4466-91a2-4717cde571df
  Args:
    type: :Woman
    source: Princess_Alexia_of_Greece_and_Denmark
  AssignClass (3e75a202-654b-43a8-a4dc-6172b7afbfd8)
 Call ID: 3e75a202-654b-43a8-a4dc-6172b7afbfd8
  Args:
    type: :Person
    source: Princess_Alexia_of_Greece_and_Denmark
  AssignClass (767e7d9f-5feb-4e08-925e-363503faeebc)
 Call ID: 767e7d9f-5feb-4e08-925e-363503faeebc
  Args:
    type: :Woman
    source: Pia_Getty
  AssignClass (a8989ca0-5ad6-43c8-9f71-011b38b150ed)
 Call ID: a8989ca0-5ad6-43c8-9f71-011b38b150ed
  Args:
    type: :Person
    source: Pia_Getty
  AssignClass (09b3a6f1-b412-4388-abc2-b6d310382836)
 Call ID: 09b3a6f1-b412-4388-abc2-b6d310382836
  Args:
    type: :Man
    source: Charles_III
  AssignClass (829866cd-1d8f-4973-9535-22ebd15dca75)
 Call ID: 829866cd-1d8f-4973-9535-22ebd15dca75
  Args:
    type: :Person
    source: Charles_III
  AssignClass (677f830a-902f-4ac4-aff8-0b5c2096cffa)
 Call ID: 677f830a-902f-4ac4-aff8-0b5c2096cffa
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (ffdeddb9-e4e4-4489-94c4-c45bb4621aee)
 Call ID: ffdeddb9-e4e4-4489-94c4-c45bb4621aee
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (a5ee21d5-37ba-4257-86a9-d225d900b8df)
 Call ID: a5ee21d5-37ba-4257-86a9-d225d900b8df
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (099370fd-b648-4df1-a5e4-b58699ab6f73)
 Call ID: 099370fd-b648-4df1-a5e4-b58699ab6f73
  Args:
    type: :Person
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (018bbfb5-dce6-4613-96ec-6d0191ad1ca0)
 Call ID: 018bbfb5-dce6-4613-96ec-6d0191ad1ca0
  Args:
    type: :Man
    source: Matthew_Kumar
  AssignClass (3e77bc20-6728-4646-a7ca-2acd07cdee1f)
 Call ID: 3e77bc20-6728-4646-a7ca-2acd07cdee1f
  Args:
    type: :Person
    source: Matthew_Kumar
  Finish (6bfc7703-925c-4229-911d-450d3d32f91a)
 Call ID: 6bfc7703-925c-4229-911d-450d3d32f91a
  Args: