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
Princess Françoise d'Orléans (Françoise Isabelle Louise Marie; 25 December 1902 - 25 February 1953) was born an Orléans Princess of France and became a Princess of Greece and Denmark by marriage.
She was thus a member of the Greek royal family and a descendant of the "Citizen-King" Louis Philippe I.


Life

Françoise d'Orléans was born in Paris, the second daughter of Jean d'Orléans, duc de Guise (an Orléanist pretender to the throne of France under the name Jean III) and his wife, the French Princess Isabelle of Orléans.
Françoise's brother, Prince Henri, Count of Paris, succeeded their father as the Orleanist pretender, under the name Henri VI.
In Palermo on 11 February 1929, she married Prince Christopher of Greece and Denmark (1888–1940).
This was Christopher's second marriage - he was the youngest son of King George I of Greece (1845–1913) and his wife, Grand Duchess Olga Constantinovna of Russia (1851–1926).
Through his father, he was thus a grandson of King Christian IX of Denmark (1818–1906), nicknamed "the father-in-law of Europe" due to his six children all marrying into other royal families.
They had only one child, the writer Prince Michael of Greece and Denmark (1939–2024), whose marriage to the Greek artist Marina Karella (born 1940) did not conform to the laws of the royal house and thus deprived him of all right of succession to the Greek throne.
She is grandmother of Princess Alexandra of Greece, an artist, art collector, arts patron, and child life specialist.
Her other grand-daughter is Princess Olga of Greece, who married Prince Aimone of Savoy-Aosta, one of two claimants to be Head of the House of Savoy.
The civil war in Greece was preventing her from entering, and the British government refused to grant her asylum.
Françoise and her son Michael went to Paris, where they lived in the home of Princess Isabella and her second husband, Prince Pierre Murat.
Françoise did not want to see anyone in their residence and rarely left her rooms.
She is buried alongside her husband in Tatoi Royal Cemetery, Greece.



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
  AssignClass (9be30181-7c7b-424e-aedc-3f0835b0a9cb)
 Call ID: 9be30181-7c7b-424e-aedc-3f0835b0a9cb
  Args:
    source: Francoise_dOrleans
    type: :Woman
  AssignClass (953bd211-25cd-4781-a3b7-22670590b16c)
 Call ID: 953bd211-25cd-4781-a3b7-22670590b16c
  Args:
    type: :Man
    source: Jean_dOrleans
  AssignClass (fa70f44b-2c3b-46d1-91f7-02b19cdf5496)
 Call ID: fa70f44b-2c3b-46d1-91f7-02b19cdf5496
  Args:
    source: Isabelle_dOrleans
    type: :Woman
  AssignClass (edea256b-2151-487f-bbc2-90f3600c4d0b)
 Call ID: edea256b-2151-487f-bbc2-90f3600c4d0b
  Args:
    type: :Man
    source: Henri_dOrleans
  AssignClass (34c9753e-78c2-40ca-a967-fd9179493651)
 Call ID: 34c9753e-78c2-40ca-a967-fd9179493651
  Args:
    source: Christopher_of_Greece_and_Denmark
    type: :Man
  AssignClass (1de4c867-a1e2-4620-ae4e-767005fedc79)
 Call ID: 1de4c867-a1e2-4620-ae4e-767005fedc79
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (a7150677-39c6-4b40-8086-b3bd73123766)
 Call ID: a7150677-39c6-4b40-8086-b3bd73123766
  Args:
    source: Olga_Constantinovna_of_Russia
    type: :Woman
  AssignClass (cd801bdb-a182-49dc-8183-806ca902c904)
 Call ID: cd801bdb-a182-49dc-8183-806ca902c904
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (4b6b44f1-80b3-43b4-9ddd-9be628d39b49)
 Call ID: 4b6b44f1-80b3-43b4-9ddd-9be628d39b49
  Args:
    type: :Man
    source: Michael_of_Greece_and_Denmark
  AssignClass (77fde275-4118-41ce-9d83-13413edbd107)
 Call ID: 77fde275-4118-41ce-9d83-13413edbd107
  Args:
    source: Marina_Karella
    type: :Woman
  AssignClass (73fd89e9-fc43-4c56-99d1-f7d14be1ccb9)
 Call ID: 73fd89e9-fc43-4c56-99d1-f7d14be1ccb9
  Args:
    source: Alexandra_of_Greece
    type: :Woman
  AssignClass (854768a5-5d8f-4fa9-a7b8-1f90c7459f15)
 Call ID: 854768a5-5d8f-4fa9-a7b8-1f90c7459f15
  Args:
    type: :Woman
    source: Olga_of_Greece
  AssignClass (d108ff34-91e7-442b-be70-41b4b2472d61)
 Call ID: d108ff34-91e7-442b-be70-41b4b2472d61
  Args:
    source: Aimone_of_Savoy_Aosta
    type: :Man
  AssignClass (7185ecb3-b445-445c-ac81-7e45ea8340bd)
 Call ID: 7185ecb3-b445-445c-ac81-7e45ea8340bd
  Args:
    source: Isabella_Murat
    type: :Woman
  AssignClass (5404c050-83fe-43da-a6a3-7abcf4b09a72)
 Call ID: 5404c050-83fe-43da-a6a3-7abcf4b09a72
  Args:
    source: Pierre_Murat
    type: :Man
  AddLiteral (c2416abb-9238-4f14-aa28-2385982fa63b)
 Call ID: c2416abb-9238-4f14-aa28-2385982fa63b
  Args:
    literal_type: xsd:integer
    literal_value: 1902
    relation: :hasBirthYear
    source: Francoise_dOrleans
  AddLiteral (f7dece68-e2c2-41c3-a186-7285cdd259b7)
 Call ID: f7dece68-e2c2-41c3-a186-7285cdd259b7
  Args:
    literal_type: xsd:integer
    literal_value: 1953
    relation: :hasDeathYear
    source: Francoise_dOrleans
  AddTriple (383f9d95-4b7f-4599-9c63-47bc4fb3051e)
 Call ID: 383f9d95-4b7f-4599-9c63-47bc4fb3051e
  Args:
    source: Francoise_dOrleans
    target: Jean_dOrleans
    relation: :hasFather
  AddTriple (7d0ea430-984f-4fcc-be6a-1e6f688e13e0)
 Call ID: 7d0ea430-984f-4fcc-be6a-1e6f688e13e0
  Args:
    relation: :hasMother
    target: Isabelle_dOrleans
    source: Francoise_dOrleans
  AddTriple (99af18c3-2171-46cd-906c-4aece2685a63)
 Call ID: 99af18c3-2171-46cd-906c-4aece2685a63
  Args:
    target: Henri_dOrleans
    relation: :hasBrother
    source: Francoise_dOrleans
  AddTriple (17fd0672-8350-4db0-920a-9f939add3b30)
 Call ID: 17fd0672-8350-4db0-920a-9f939add3b30
  Args:
    source: Jean_dOrleans
    relation: :isFatherOf
    target: Henri_dOrleans
  AddLiteral (aaf87797-ac4c-4a4b-bcc7-f90b27fe6c7d)
 Call ID: aaf87797-ac4c-4a4b-bcc7-f90b27fe6c7d
  Args:
    relation: :hasMarriageYear
    literal_value: 1929
    literal_type: xsd:integer
    source: Francoise_dOrleans
  AddTriple (7f219048-f868-457f-b144-67a1d2d15ce6)
 Call ID: 7f219048-f868-457f-b144-67a1d2d15ce6
  Args:
    relation: :hasRelation
    target: Christopher_of_Greece_and_Denmark
    source: Francoise_dOrleans
  AddTriple (e402b706-af73-4eb7-91c5-ae66464f78ae)
 Call ID: e402b706-af73-4eb7-91c5-ae66464f78ae
  Args:
    source: Christopher_of_Greece_and_Denmark
    target: George_I_of_Greece
    relation: :hasFather
  AddTriple (4f7318a9-cba0-4a31-83d9-ce81284d3f3a)
 Call ID: 4f7318a9-cba0-4a31-83d9-ce81284d3f3a
  Args:
    source: Christopher_of_Greece_and_Denmark
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
  AddTriple (2e15e7e2-216e-493d-a525-bff2248907a1)
 Call ID: 2e15e7e2-216e-493d-a525-bff2248907a1
  Args:
    source: George_I_of_Greece
    target: Christian_IX_of_Denmark
    relation: :hasFather
  AddTriple (b535fd72-4e65-41eb-8045-dd47baaf0ca1)
 Call ID: b535fd72-4e65-41eb-8045-dd47baaf0ca1
  Args:
    relation: :hasSon
    target: Michael_of_Greece_and_Denmark
    source: Francoise_dOrleans
  AddTriple (d9785b3f-5e59-492c-a28c-f2e2e11f0dfb)
 Call ID: d9785b3f-5e59-492c-a28c-f2e2e11f0dfb
  Args:
    target: Christopher_of_Greece_and_Denmark
    relation: :hasFather
    source: Michael_of_Greece_and_Denmark
  AddTriple (3077133c-2c99-4f40-acba-55d19b3304d5)
 Call ID: 3077133c-2c99-4f40-acba-55d19b3304d5
  Args:
    source: Michael_of_Greece_and_Denmark
    target: Francoise_dOrleans
    relation: :hasMother
  AddTriple (85d572d9-6b79-4f40-b0d7-c60b203b9f74)
 Call ID: 85d572d9-6b79-4f40-b0d7-c60b203b9f74
  Args:
    relation: :hasRelation
    target: Marina_Karella
    source: Michael_of_Greece_and_Denmark
  AddTriple (1d67159c-9f6e-44fc-924c-dc534a04e40d)
 Call ID: 1d67159c-9f6e-44fc-924c-dc534a04e40d
  Args:
    relation: :isMotherOf
    target: Alexandra_of_Greece
    source: Francoise_dOrleans
  AddTriple (efaa70c1-c3c9-400b-b02a-6f6647203dfb)
 Call ID: efaa70c1-c3c9-400b-b02a-6f6647203dfb
  Args:
    target: Olga_of_Greece
    relation: :isMotherOf
    source: Francoise_dOrleans
  AddTriple (6b58b143-0b07-445f-a716-babb3f60e1a0)
 Call ID: 6b58b143-0b07-445f-a716-babb3f60e1a0
  Args:
    target: Aimone_of_Savoy_Aosta
    relation: :hasRelation
    source: Olga_of_Greece
  Finish (e4b55b4f-9235-4bad-86b8-9a830e607a1d)
 Call ID: e4b55b4f-9235-4bad-86b8-9a830e607a1d
  Args: