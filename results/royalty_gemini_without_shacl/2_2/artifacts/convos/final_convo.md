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
Queen Margrethe II


Count Felix of Monpezat SK (born Prince Felix of Denmark; 22 July 2002) is a member of the Danish royal family.
He is a grandson of Queen Margrethe II and Prince Henrik, and a nephew of King Frederik X. Felix is currently seventh in the line of succession to the Danish throne.
Biography

Felix was born a Prince of Denmark at Rigshospitalet, the Copenhagen University Hospital in Copenhagen, Denmark, on 22 July 2002.
His names were revealed to be Felix Henrik Valdemar Christian.
His godparents are his maternal aunt, Martina Bent; and friends of his parents, Count Christian Ahlefeldt-Laurvig, Oscar Davidsen Siesbye, Damian Sibley and Annick Boel.
At the christening, the musical work Dåbens Pagt composed by Frederik Magle, dedicated to Prince Felix, saw its inaugural performance.
After their divorce, Prince Joachim and Countess Alexandra shared joint custody of Felix and his older brother Prince Nikolai.
The prince attended pre-school at the Garnison Church in Copenhagen, and at age six, followed in the footsteps of his father, brother and uncle at Krebs School in Østerbro.
Titles and styles

Originally known as "His Highness Prince Felix of Denmark", Felix assumed the style "His Highness Prince Felix of Denmark, Count of Monpezat" on 29 April 2008.
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
From 1 January 2023, Felix is known as "His Excellency Count Felix of Monpezat".



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
  AssignClass (f637083e-3b7b-469f-ba28-ee3dbb1c58c5)
 Call ID: f637083e-3b7b-469f-ba28-ee3dbb1c58c5
  Args:
    type: :Person
    source: Count_Felix_of_Monpezat
  AssignClass (d857df3c-e8b0-4c76-b325-73a9be70cfcd)
 Call ID: d857df3c-e8b0-4c76-b325-73a9be70cfcd
  Args:
    type: :Man
    source: Count_Felix_of_Monpezat
  AddLiteral (fb3257a7-64b2-4306-bd69-98c8b3185600)
 Call ID: fb3257a7-64b2-4306-bd69-98c8b3185600
  Args:
    literal_value: Male
    source: Count_Felix_of_Monpezat
    literal_type: xsd:string
    relation: :hasSex
  AddLiteral (58b46156-50ff-4329-9831-00fc1561505c)
 Call ID: 58b46156-50ff-4329-9831-00fc1561505c
  Args:
    literal_type: xsd:integer
    source: Count_Felix_of_Monpezat
    relation: :hasBirthYear
    literal_value: 2002
  AssignClass (d1535512-cbd5-4842-961a-cd72fddcb41e)
 Call ID: d1535512-cbd5-4842-961a-cd72fddcb41e
  Args:
    type: :Person
    source: Queen_Margrethe_II
  AssignClass (81f91094-0c39-482d-b469-59cbeb440bcf)
 Call ID: 81f91094-0c39-482d-b469-59cbeb440bcf
  Args:
    type: :Woman
    source: Queen_Margrethe_II
  AssignClass (a646a1b2-3462-4be0-8d7f-f544e3d8a55d)
 Call ID: a646a1b2-3462-4be0-8d7f-f544e3d8a55d
  Args:
    type: :Person
    source: Prince_Henrik
  AssignClass (f4be3aec-65d7-4b67-8614-20e392a3fd4e)
 Call ID: f4be3aec-65d7-4b67-8614-20e392a3fd4e
  Args:
    type: :Man
    source: Prince_Henrik
  AssignClass (92c81994-b549-490d-9d66-b2dc40b26fb1)
 Call ID: 92c81994-b549-490d-9d66-b2dc40b26fb1
  Args:
    type: :Person
    source: King_Frederik_X
  AssignClass (cf5cdda7-3515-4f8d-8d71-fa13bcdc7f08)
 Call ID: cf5cdda7-3515-4f8d-8d71-fa13bcdc7f08
  Args:
    type: :Man
    source: King_Frederik_X
  AddTriple (19e86411-5fa0-41fe-b745-66e2fa5657e3)
 Call ID: 19e86411-5fa0-41fe-b745-66e2fa5657e3
  Args:
    target: Count_Felix_of_Monpezat
    source: Queen_Margrethe_II
    relation: :isAncestorOf
  AddTriple (e992f2e7-3e41-48b3-81d2-0a0e67498210)
 Call ID: e992f2e7-3e41-48b3-81d2-0a0e67498210
  Args:
    target: Count_Felix_of_Monpezat
    relation: :isAncestorOf
    source: Prince_Henrik
  AssignClass (0ec9d1a3-4136-4d9c-9bce-bbbcea9f40df)
 Call ID: 0ec9d1a3-4136-4d9c-9bce-bbbcea9f40df
  Args:
    type: :Person
    source: Prince_Joachim
  AssignClass (e8eb651b-6a1a-4747-93eb-c951dd2fe39e)
 Call ID: e8eb651b-6a1a-4747-93eb-c951dd2fe39e
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (4c4b84a1-6c39-4364-b6b9-0d6ff8d4ba0a)
 Call ID: 4c4b84a1-6c39-4364-b6b9-0d6ff8d4ba0a
  Args:
    type: :Person
    source: Countess_Alexandra
  AssignClass (11031b68-513a-4977-8cc7-2a0f93edb800)
 Call ID: 11031b68-513a-4977-8cc7-2a0f93edb800
  Args:
    type: :Woman
    source: Countess_Alexandra
  AddTriple (8ab90a41-cd02-414b-9af7-c243069850ea)
 Call ID: 8ab90a41-cd02-414b-9af7-c243069850ea
  Args:
    relation: :isFatherOf
    source: Prince_Joachim
    target: Count_Felix_of_Monpezat
  AddTriple (48202793-f4f8-430e-9dcf-03dd57e5633e)
 Call ID: 48202793-f4f8-430e-9dcf-03dd57e5633e
  Args:
    target: Count_Felix_of_Monpezat
    relation: :isMotherOf
    source: Countess_Alexandra
  AssignClass (14fa927f-fb52-4fa4-83ea-10ac3081ebe7)
 Call ID: 14fa927f-fb52-4fa4-83ea-10ac3081ebe7
  Args:
    type: :Person
    source: Prince_Nikolai
  AssignClass (56f5930e-88a5-49cf-8cba-495faeb3eb5b)
 Call ID: 56f5930e-88a5-49cf-8cba-495faeb3eb5b
  Args:
    type: :Man
    source: Prince_Nikolai
  AddTriple (d6374684-7ae1-49a9-89b9-441f81de74d4)
 Call ID: d6374684-7ae1-49a9-89b9-441f81de74d4
  Args:
    source: Count_Felix_of_Monpezat
    relation: :hasBrother
    target: Prince_Nikolai
  AddTriple (67c58286-25c6-4e5d-b204-381815a50d2a)
 Call ID: 67c58286-25c6-4e5d-b204-381815a50d2a
  Args:
    source: Prince_Nikolai
    relation: :hasBrother
    target: Count_Felix_of_Monpezat
  Finish (3c76fd74-58c8-49c4-8e62-30314c46f3b2)
 Call ID: 3c76fd74-58c8-49c4-8e62-30314c46f3b2
  Args: