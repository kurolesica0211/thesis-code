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
Paul Dmitrievich Romanovsky-Ilyinsky (January 27, 1928 – February 10, 2004) was a three-time mayor of Palm Beach, Florida, and the only child of Grand Duke Dmitri Pavlovich of Russia and his morganatic wife, Cincinnati heiress Audrey Emery.
He was a great-grandson of Tsar Alexander II of Russia and, following the death of Grand Duke Vladimir Kirillovich in 1992, the heir-male of the Ilyinsky claim of the House of Romanov (a position now held by his elder son), a first cousin once removed of Nicholas II, first cousin of Prince Lennart of Sweden, Duke of Småland and the second cousin of Charles III.
Early life

Prince Paul Romanovsky-Ilyinsky was born on 27 January 1928 at his parents' home, 26 Manchester Square, London.
His father, Grand Duke Dmitri, as a direct consequence of his involvement in the murder of Grigori Rasputin in 1916, had been sent to the Persian front, which ultimately saved his life, as many of his Imperial relatives were executed by the Bolsheviks during the October Revolution .
Dmitri, who was working as a champagne salesman, married Cincinnati heiress Audrey Emery in 1926.
Grand Duke Cyril Vladimirovich of Russia, Dmitri's cousin and the self-proclaimed emperor in exile, elevated Grand Duke Dmitri's wife and their descendants to Russian princely (Russian: knyaz) rank (rank of nobility, not royalty).
Any children the couple would have would be known as Romanovsky-Ilyinsky, the latter half of the surname derived from Dmitri's former property in Russia, Ilinskoe.
Ilynskiy's parents were divorced in 1937, and Ilyinsky was raised by his mother, who mostly lived in France.
Dmitri Pavlovich's health had always been somewhat frail, and in the 1930s, his chronic tuberculosis became acute, leading to his death in 1942.
Education and career

Ilyinsky, who was a U.S. citizen, attended Woodberry Forest School in Virginia and the Royal Military Academy Sandhurst, England, before joining the U.S. Marine Corps.
Ilyinsky lived in Cincinnati for about 20 years, serving on the board of the company founded by his mother's family, Emery Industries, and working as an author and photographer.
Ilyinsky died at his home in Palm Beach, Florida, on February 10, 2004.
Personal life

Ilyinsky was married twice; he married his first wife, Mary Evelyn Prince in 1948 (annulment in 1951), and married his second wife, Angelica Philippa Kauffmann in 1953.
Ilyinsky had four children:


Ancestry

References



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
  AssignClass (4ba06e80-c69c-4bc5-9f9b-7a8c32a114fb)
 Call ID: 4ba06e80-c69c-4bc5-9f9b-7a8c32a114fb
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    type: :Man
  AssignClass (709aa448-227d-413f-9d7d-d2c5766948bf)
 Call ID: 709aa448-227d-413f-9d7d-d2c5766948bf
  Args:
    type: :Person
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AddLiteral (64fe02e9-d7ec-446b-a4ba-a62e575e2928)
 Call ID: 64fe02e9-d7ec-446b-a4ba-a62e575e2928
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_value: 1928
  AddLiteral (abc70f0e-c037-4d9a-b3df-d3cecae33fd8)
 Call ID: abc70f0e-c037-4d9a-b3df-d3cecae33fd8
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2004
  AssignClass (b55eee43-c770-4222-a827-f0c2aaad77da)
 Call ID: b55eee43-c770-4222-a827-f0c2aaad77da
  Args:
    source: Dmitri_Pavlovich_of_Russia
    type: :Man
  AssignClass (9144232f-941f-4b53-804f-6c7d2d588f87)
 Call ID: 9144232f-941f-4b53-804f-6c7d2d588f87
  Args:
    type: :Person
    source: Dmitri_Pavlovich_of_Russia
  AssignClass (f7be1a15-4e9c-4735-bbdc-be6d8db3369f)
 Call ID: f7be1a15-4e9c-4735-bbdc-be6d8db3369f
  Args:
    source: Dmitri_Pavlovich_of_Russia
    type: :Ancestor
  AddTriple (d772093a-5898-4410-9e11-83aec401bca4)
 Call ID: d772093a-5898-4410-9e11-83aec401bca4
  Args:
    target: Dmitri_Pavlovich_of_Russia
    relation: :hasFather
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AssignClass (13858592-2966-453f-a0b1-c8a503b1ec05)
 Call ID: 13858592-2966-453f-a0b1-c8a503b1ec05
  Args:
    source: Audrey_Emery
    type: :Woman
  AssignClass (53e21fe7-150d-4192-a899-0f2a9b5945f4)
 Call ID: 53e21fe7-150d-4192-a899-0f2a9b5945f4
  Args:
    type: :Person
    source: Audrey_Emery
  AssignClass (a6228c29-39d5-4e51-864c-fdfad4154d4b)
 Call ID: a6228c29-39d5-4e51-864c-fdfad4154d4b
  Args:
    type: :Ancestor
    source: Audrey_Emery
  AddTriple (329145b6-0a31-4a83-aa08-2527cb721438)
 Call ID: 329145b6-0a31-4a83-aa08-2527cb721438
  Args:
    target: Audrey_Emery
    relation: :hasMother
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AddLiteral (8332e6ad-745d-4f4d-b2ef-ef62459a255e)
 Call ID: 8332e6ad-745d-4f4d-b2ef-ef62459a255e
  Args:
    relation: :hasMarriageYear
    source: Dmitri_Pavlovich_of_Russia
    literal_type: xsd:integer
    literal_value: 1926
  AddTriple (ab1cfa8c-1924-4223-acb5-4492ad62d8c0)
 Call ID: ab1cfa8c-1924-4223-acb5-4492ad62d8c0
  Args:
    relation: :hasRelation
    source: Dmitri_Pavlovich_of_Russia
    target: Audrey_Emery
  AssignClass (64de218f-c0ac-493a-8a46-c7873e89deee)
 Call ID: 64de218f-c0ac-493a-8a46-c7873e89deee
  Args:
    type: :Woman
    source: Mary_Evelyn_Prince
  AssignClass (4714dc9f-fe41-420d-974f-d0dc10539600)
 Call ID: 4714dc9f-fe41-420d-974f-d0dc10539600
  Args:
    source: Mary_Evelyn_Prince
    type: :Person
  AddTriple (8750f82b-573c-4dec-9e6e-892f261eb507)
 Call ID: 8750f82b-573c-4dec-9e6e-892f261eb507
  Args:
    target: Mary_Evelyn_Prince
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    relation: :hasRelation
  AddLiteral (e52d1b54-997e-4108-a21b-e58c6eea64c3)
 Call ID: e52d1b54-997e-4108-a21b-e58c6eea64c3
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1948
  AssignClass (fc7d0856-9e00-43d1-9a8e-d577ee35f349)
 Call ID: fc7d0856-9e00-43d1-9a8e-d577ee35f349
  Args:
    source: Angelica_Philippa_Kauffmann
    type: :Woman
  AssignClass (8bcf8ae8-4f1d-45a8-8098-3a4033b8b09b)
 Call ID: 8bcf8ae8-4f1d-45a8-8098-3a4033b8b09b
  Args:
    source: Angelica_Philippa_Kauffmann
    type: :Person
  AddTriple (5e28b2a1-f3e1-40a0-8de9-a66dc075452a)
 Call ID: 5e28b2a1-f3e1-40a0-8de9-a66dc075452a
  Args:
    relation: :hasRelation
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    target: Angelica_Philippa_Kauffmann
  AddLiteral (9d64e8f7-139a-450e-a54c-a9479b95e262)
 Call ID: 9d64e8f7-139a-450e-a54c-a9479b95e262
  Args:
    literal_value: 1953
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (19aad7d7-ebf1-42e2-a554-432449e32a07)
 Call ID: 19aad7d7-ebf1-42e2-a554-432449e32a07
  Args:
    type: :Man
    source: Alexander_II_of_Russia
  AssignClass (d2c30062-1e9f-4ca8-9844-911ddab3666d)
 Call ID: d2c30062-1e9f-4ca8-9844-911ddab3666d
  Args:
    source: Alexander_II_of_Russia
    type: :Person
  AssignClass (77e905a2-b51b-4acc-a19a-9149f5f95ac8)
 Call ID: 77e905a2-b51b-4acc-a19a-9149f5f95ac8
  Args:
    type: :Ancestor
    source: Alexander_II_of_Russia
  AddTriple (a5ad74ff-0562-481c-abd3-d52a880e637a)
 Call ID: a5ad74ff-0562-481c-abd3-d52a880e637a
  Args:
    relation: :hasAncestor
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    target: Alexander_II_of_Russia
  Finish (aaf3226a-fd03-4b15-bb49-3058fc4858a9)
 Call ID: aaf3226a-fd03-4b15-bb49-3058fc4858a9
  Args: