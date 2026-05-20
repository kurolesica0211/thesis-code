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
Princess Alexia of Greece and Denmark (Greek: Αλεξία Ντε Γκρες, romanized: Alexía de Grèce; born 10 July 1965) is the eldest child of Constantine II and Anne-Marie, who were King and Queen of Greece from 1964 until the abolition of the monarchy in 1973.
Biography

Alexia was born on 10 July 1965 at Mon Repos, a villa on the Greek island of Corfu used at the time as a summer residence by the Greek royal family.
She was the first child born to the then King Constantine II and Queen Anne-Marie of the Hellenes.
At the time of her birth, her father was King of Greece, her grandfather was King of Denmark, and her great-grandfather was King of Sweden.
As the monarch's only child, between her own birth and the birth on 20 May 1967 of her brother Pavlos, Alexia was heir presumptive to the throne of the Hellenes, then an extant monarchy.
The Greek Constitution of 1952 had changed Greece's order of succession to the throne from the previous Salic law, prevalent in much of the continent, and which precluded the succession of women, to male-preference primogeniture, which accorded succession to the throne to a female member of a dynasty if she has no brothers, similar to the then extant succession laws of the United Kingdom, Denmark and Spain.
Alexia grew up in exile and was raised in between Rome and London.
The family then briefly moved to Denmark and stayed at Amalienborg Palace, and then to London the following year.
Prior to Alexia's education at the Hellenic College of London, she attended the Miss Surtee's School for Boys and Girls in Rome, Italy.
Οn 20 December 2024, Alexia along with other members of the former royal family acquired Greek citizenship, under the surname "de Grèce".
Marriage and children

Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


On 9 July 1999, Alexia married Carlos Javier Morales Quintana, an architect and a champion yachtsman, at St. Sophia Cathedral, London.
In May 1999, two months before their wedding, Alexia and Carlos were involved in a yachting accident on a boat named the Alexia.
Alexia and Carlos were the only two people out of the thirteen on board to be injured.
Alexia suffered a broken collarbone and Carlos a fractured kneecap.
At her wedding, Alexia wore a gown by the Austrian designer Inge Sprawson.
Alexia's mother, Anne-Marie, and grandmother, Ingrid, had both also worn the same tiara on their own wedding day.
Her attendants included her sister Princess Theodora, her niece Princess Maria-Olympia, and Princess Mafalda, daughter of Kyril, Prince of Preslav, a son of former King Simeon of Bulgaria.
The couple have four children: 


Their children's last names are "Morales y de Grecia", which translates to "Morales and of Greece", taking their father's surname and their mother's royal title.
Alexia and her family now live in her husband's native land, at Puerto Calero marina, Yaiza, Lanzarote in the Canary Islands, in a house designed by her husband.
The Canary Islands are an autonomous community of Spain, where Alexia's aunt, Queen Sofía, lives and first cousin, Felipe VI, lives and rules.



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
  AssignClass (56fc30e0-8829-4e15-a8a6-5d81abfddb91)
 Call ID: 56fc30e0-8829-4e15-a8a6-5d81abfddb91
  Args:
    type: :Woman
    source: Alexia_of_Greece_and_Denmark
  AssignClass (61dfe8a1-a359-4272-9467-28ab7b27d42c)
 Call ID: 61dfe8a1-a359-4272-9467-28ab7b27d42c
  Args:
    type: :Man
    source: Constantine_II_of_Greece
  AssignClass (6f70a4a2-b159-4e40-91ea-9cae7d7a2ef0)
 Call ID: 6f70a4a2-b159-4e40-91ea-9cae7d7a2ef0
  Args:
    source: Anne-Marie_of_Greece
    type: :Woman
  AssignClass (076e0ea4-6445-4e89-8aab-a521b8c701fb)
 Call ID: 076e0ea4-6445-4e89-8aab-a521b8c701fb
  Args:
    type: :Man
    source: Pavlos_of_Greece
  AssignClass (1265642e-b135-4510-b8a2-6ed365cad77b)
 Call ID: 1265642e-b135-4510-b8a2-6ed365cad77b
  Args:
    type: :Man
    source: Carlos_Javier_Morales_Quintana
  AssignClass (84f03fe6-4749-4d61-a650-f660a327b00b)
 Call ID: 84f03fe6-4749-4d61-a650-f660a327b00b
  Args:
    source: Theodora_of_Greece
    type: :Woman
  AssignClass (cb8385d0-cac5-444f-a0ef-94b4371e4190)
 Call ID: cb8385d0-cac5-444f-a0ef-94b4371e4190
  Args:
    source: Maria-Olympia_of_Greece
    type: :Woman
  AssignClass (b8e29e00-ff8d-43bb-b730-2d3d8478b4ce)
 Call ID: b8e29e00-ff8d-43bb-b730-2d3d8478b4ce
  Args:
    type: :Woman
    source: Mafalda_of_Preslav
  AssignClass (b328ae24-db8d-42ca-80d1-c03a591d86f5)
 Call ID: b328ae24-db8d-42ca-80d1-c03a591d86f5
  Args:
    source: Kyril_of_Preslav
    type: :Man
  AssignClass (e974c6c6-9dcb-4f7c-83f8-a8b0687dd517)
 Call ID: e974c6c6-9dcb-4f7c-83f8-a8b0687dd517
  Args:
    type: :Man
    source: Simeon_of_Bulgaria
  AssignClass (6450bbaf-872a-4409-bd45-06f0ecaad4b4)
 Call ID: 6450bbaf-872a-4409-bd45-06f0ecaad4b4
  Args:
    source: Ingrid_of_Denmark
    type: :Woman
  AssignClass (5c7c01c1-c297-4fc9-a8b9-2b9feeef0129)
 Call ID: 5c7c01c1-c297-4fc9-a8b9-2b9feeef0129
  Args:
    source: Sofia_of_Spain
    type: :Woman
  AssignClass (b6e785cf-8ef3-437a-bbe4-89dcfb4ef62d)
 Call ID: b6e785cf-8ef3-437a-bbe4-89dcfb4ef62d
  Args:
    type: :Man
    source: Felipe_VI_of_Spain
  AddLiteral (5b134704-86bb-4815-baf4-e29842ead9c4)
 Call ID: 5b134704-86bb-4815-baf4-e29842ead9c4
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Alexia_of_Greece_and_Denmark
    literal_value: 1965
  AddTriple (bd12dcc1-54aa-4812-9f86-346e1027207b)
 Call ID: bd12dcc1-54aa-4812-9f86-346e1027207b
  Args:
    relation: :hasFather
    source: Alexia_of_Greece_and_Denmark
    target: Constantine_II_of_Greece
  AddTriple (14e27a49-2d08-4dee-b69f-ab71481065e3)
 Call ID: 14e27a49-2d08-4dee-b69f-ab71481065e3
  Args:
    source: Alexia_of_Greece_and_Denmark
    relation: :hasMother
    target: Anne-Marie_of_Greece
  AddTriple (a0e5ee79-ea29-40f0-a607-01bd0be32aaf)
 Call ID: a0e5ee79-ea29-40f0-a607-01bd0be32aaf
  Args:
    target: Pavlos_of_Greece
    relation: :hasBrother
    source: Alexia_of_Greece_and_Denmark
  AddTriple (a1c752ef-2fbc-46dc-a040-af1997bb7896)
 Call ID: a1c752ef-2fbc-46dc-a040-af1997bb7896
  Args:
    relation: :hasFather
    source: Pavlos_of_Greece
    target: Constantine_II_of_Greece
  AddTriple (4eb0d434-5a8d-4210-a58a-e6c1d7ec82a4)
 Call ID: 4eb0d434-5a8d-4210-a58a-e6c1d7ec82a4
  Args:
    target: Anne-Marie_of_Greece
    relation: :hasMother
    source: Pavlos_of_Greece
  AddTriple (f92f4ed1-3163-448d-933e-da2a3dd77d69)
 Call ID: f92f4ed1-3163-448d-933e-da2a3dd77d69
  Args:
    target: Theodora_of_Greece
    relation: :hasSister
    source: Alexia_of_Greece_and_Denmark
  AddTriple (e356ebe2-ce4b-4bc0-aff1-cbd5a2fad4f9)
 Call ID: e356ebe2-ce4b-4bc0-aff1-cbd5a2fad4f9
  Args:
    target: Constantine_II_of_Greece
    source: Theodora_of_Greece
    relation: :hasFather
  AddTriple (5414fab0-c38c-4faa-a444-c72e871ec597)
 Call ID: 5414fab0-c38c-4faa-a444-c72e871ec597
  Args:
    target: Anne-Marie_of_Greece
    source: Theodora_of_Greece
    relation: :hasMother
  AddLiteral (f6f5d517-1fd8-47c9-a5e6-5f0a16a50c91)
 Call ID: f6f5d517-1fd8-47c9-a5e6-5f0a16a50c91
  Args:
    source: Alexia_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1999
  AddTriple (c8f8dc86-9b3f-4053-a4d0-6095889ad808)
 Call ID: c8f8dc86-9b3f-4053-a4d0-6095889ad808
  Args:
    target: Carlos_Javier_Morales_Quintana
    relation: :hasRelation
    source: Alexia_of_Greece_and_Denmark
  AddTriple (360c6794-7a6a-417a-a94a-0e27fe60ab62)
 Call ID: 360c6794-7a6a-417a-a94a-0e27fe60ab62
  Args:
    target: Kyril_of_Preslav
    relation: :hasFather
    source: Mafalda_of_Preslav
  AddTriple (73592aa2-3488-44f0-8407-eb4ebcfad20e)
 Call ID: 73592aa2-3488-44f0-8407-eb4ebcfad20e
  Args:
    relation: :hasFather
    source: Kyril_of_Preslav
    target: Simeon_of_Bulgaria
  Finish (83707582-9e28-49bc-abf7-a54fc4bb7092)
 Call ID: 83707582-9e28-49bc-abf7-a54fc4bb7092
  Args: