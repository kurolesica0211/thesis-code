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


Prince Achileas-Andreas of Greece and Denmark (Greek: Αχιλλέας Ανδρέας Ντε Γκρες, romanized: Achilléas-Andréas de Grèce; born 12 August 2000), known by the stage name Achi Miller, is an actor, socialite, and member of the former Greek royal family and the extended Danish royal family.
He is the second son and third child of Crown Prince Pavlos of Greece and Marie-Chantal Miller.
His paternal grandparents are Constantine II of Greece and Anne-Marie of Denmark, who were the last King and Queen of the Hellenes.
Early life and education

Achileas-Andreas was born on 12 August 2000 at Weill Cornell Medical Center in New York City.
Personal life

On September 28, 2024, Achileas-Andreas served as a groomsman at the wedding of Princess Theodora of Greece and Denmark and Matthew Kumar at the Metropolitan Cathedral in Athens.
Achileas-Andreas was in a relationship with Isabella Massenet, daughter of Dame Natalie Massenet, until October 2024.
Οn 20 December 2024, Achileas-Andreas along with other members of the former royal family acquired Greek citizenship, under the surname "de Grèce".
Under the stage name Achi Miller, he had a minor role in the 2023 film No Hard Feelings.



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
  AssignClass (171b4776-554c-4a79-b838-5daa041605e0)
 Call ID: 171b4776-554c-4a79-b838-5daa041605e0
  Args:
    type: :Man
    source: Achileas-Andreas_of_Greece_and_Denmark
  AssignClass (9a6f1216-4a6b-4e99-bbce-625bcd44adc5)
 Call ID: 9a6f1216-4a6b-4e99-bbce-625bcd44adc5
  Args:
    type: :Person
    source: Achileas-Andreas_of_Greece_and_Denmark
  AddLiteral (f76353fd-a773-433c-91ca-b4f649d856f3)
 Call ID: f76353fd-a773-433c-91ca-b4f649d856f3
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Achi Miller
    source: Achileas-Andreas_of_Greece_and_Denmark
  AddLiteral (bd6d4dad-f30f-4e65-8693-69079bc39131)
 Call ID: bd6d4dad-f30f-4e65-8693-69079bc39131
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Achileas-Andreas_of_Greece_and_Denmark
    literal_value: 2000
  AssignClass (f535d85e-c0df-46cf-9b73-f96371c8a8e1)
 Call ID: f535d85e-c0df-46cf-9b73-f96371c8a8e1
  Args:
    type: :Man
    source: Pavlos_of_Greece
  AssignClass (583b7d87-de52-45ee-b1ef-c4e1b8b9a3d8)
 Call ID: 583b7d87-de52-45ee-b1ef-c4e1b8b9a3d8
  Args:
    source: Pavlos_of_Greece
    type: :Person
  AddTriple (bf2fbd71-848b-4c76-a439-1b5b01ad5368)
 Call ID: bf2fbd71-848b-4c76-a439-1b5b01ad5368
  Args:
    target: Pavlos_of_Greece
    relation: :hasFather
    source: Achileas-Andreas_of_Greece_and_Denmark
  AssignClass (a44bbada-65fd-4a4b-9b97-352c58b14419)
 Call ID: a44bbada-65fd-4a4b-9b97-352c58b14419
  Args:
    source: Marie-Chantal_Miller
    type: :Woman
  AssignClass (c6e9ba2b-82a9-4c2c-a9d5-c1f29b9efbf8)
 Call ID: c6e9ba2b-82a9-4c2c-a9d5-c1f29b9efbf8
  Args:
    type: :Person
    source: Marie-Chantal_Miller
  AddTriple (61311704-e88c-4534-9c1f-38db799b3941)
 Call ID: 61311704-e88c-4534-9c1f-38db799b3941
  Args:
    source: Achileas-Andreas_of_Greece_and_Denmark
    target: Marie-Chantal_Miller
    relation: :hasMother
  AssignClass (dfd8a274-fc6c-4029-99d1-b15d21d6ecee)
 Call ID: dfd8a274-fc6c-4029-99d1-b15d21d6ecee
  Args:
    source: Constantine_II_of_Greece
    type: :Man
  AssignClass (78e7d6c5-671d-41d0-8e98-857106c582a4)
 Call ID: 78e7d6c5-671d-41d0-8e98-857106c582a4
  Args:
    type: :Person
    source: Constantine_II_of_Greece
  AddTriple (aa2ce01b-f63b-4405-b4a3-963297cb5757)
 Call ID: aa2ce01b-f63b-4405-b4a3-963297cb5757
  Args:
    source: Pavlos_of_Greece
    target: Constantine_II_of_Greece
    relation: :hasFather
  AssignClass (38020480-cb51-40c2-baf9-c3cecd039268)
 Call ID: 38020480-cb51-40c2-baf9-c3cecd039268
  Args:
    type: :Woman
    source: Anne-Marie_of_Denmark
  AssignClass (66880653-d03f-4bf2-a1a2-e2f8194321db)
 Call ID: 66880653-d03f-4bf2-a1a2-e2f8194321db
  Args:
    source: Anne-Marie_of_Denmark
    type: :Person
  AddTriple (049584f1-4b82-43e2-82f9-82cacf433b40)
 Call ID: 049584f1-4b82-43e2-82f9-82cacf433b40
  Args:
    target: Anne-Marie_of_Denmark
    relation: :hasMother
    source: Pavlos_of_Greece
  AssignClass (21eaede7-6a46-4e90-8d51-116911ec8c14)
 Call ID: 21eaede7-6a46-4e90-8d51-116911ec8c14
  Args:
    source: Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (f28fe8d2-3ec2-4caf-afeb-4899309ae465)
 Call ID: f28fe8d2-3ec2-4caf-afeb-4899309ae465
  Args:
    source: Theodora_of_Greece_and_Denmark
    type: :Person
  AssignClass (b3d6b8a9-c19d-4a91-8421-50eb8fa4f89f)
 Call ID: b3d6b8a9-c19d-4a91-8421-50eb8fa4f89f
  Args:
    type: :Man
    source: Matthew_Kumar
  AssignClass (1de8e1f2-69b3-4026-97ba-0193f29e0912)
 Call ID: 1de8e1f2-69b3-4026-97ba-0193f29e0912
  Args:
    type: :Person
    source: Matthew_Kumar
  AssignClass (49f89b68-eaef-4256-b4f4-754f3ab084dd)
 Call ID: 49f89b68-eaef-4256-b4f4-754f3ab084dd
  Args:
    source: Isabella_Massenet
    type: :Woman
  AssignClass (5f2679ff-56dc-4334-934e-15c100b9c034)
 Call ID: 5f2679ff-56dc-4334-934e-15c100b9c034
  Args:
    type: :Person
    source: Isabella_Massenet
  AssignClass (cc5c7ab3-389a-4324-bd58-c9e63cebc92f)
 Call ID: cc5c7ab3-389a-4324-bd58-c9e63cebc92f
  Args:
    source: Natalie_Massenet
    type: :Woman
  AssignClass (d34fcf13-d2f4-4f25-b0c8-4cc18e0db3da)
 Call ID: d34fcf13-d2f4-4f25-b0c8-4cc18e0db3da
  Args:
    source: Natalie_Massenet
    type: :Person
  AddTriple (f79f209c-85bd-45d6-a9b1-5295f7e88a4b)
 Call ID: f79f209c-85bd-45d6-a9b1-5295f7e88a4b
  Args:
    relation: :hasMother
    target: Natalie_Massenet
    source: Isabella_Massenet
  AssignClass (1b8e670c-442f-4b3f-a0be-fdbd173828af)
 Call ID: 1b8e670c-442f-4b3f-a0be-fdbd173828af
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AssignClass (2319c221-cc28-4ae5-8109-c92481f78ac0)
 Call ID: 2319c221-cc28-4ae5-8109-c92481f78ac0
  Args:
    type: :Person
    source: Sofia_of_Spain
  AssignClass (929b3a3e-a6f7-42f4-85dd-870e6d145a46)
 Call ID: 929b3a3e-a6f7-42f4-85dd-870e6d145a46
  Args:
    source: Marina_consort_of_Prince_Michael
    type: :Woman
  AssignClass (024d3552-486a-45b8-ad7a-b890649454bc)
 Call ID: 024d3552-486a-45b8-ad7a-b890649454bc
  Args:
    type: :Person
    source: Marina_consort_of_Prince_Michael
  Finish (3d7497e4-4fe0-41c4-acf7-5f6657fe122a)
 Call ID: 3d7497e4-4fe0-41c4-acf7-5f6657fe122a
  Args: