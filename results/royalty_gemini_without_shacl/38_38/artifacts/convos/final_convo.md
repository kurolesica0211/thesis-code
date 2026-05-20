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


Princess Alexandra Elli Francisca Maria of Greece (born 15 October 1968), known professionally as Alexandra Mirzayantz, is a Greek artist, art collector, arts patron, and child life specialist.
As the daughter of Prince Michael of Greece and Denmark, she is a member of the Greek royal family and a relative of the Danish royal family.
A morganatic descendant of the House of Glücksburg, she is not a Danish princess nor is she entitled to the style Royal Highness as other members of the Greek royal family are.
She was born a princess of Greece entitled to the style Your Highness, and was excluded from the line of succession to the Greek throne.
She is a second cousin of Constantine II of Greece, who reigned as King of the Hellenes until the monarchy was abolished in 1973.
Early life and family

Princess Alexandra was born in Athens on 15 October 1968.
She is the daughter of the historian Prince Michael of Greece and Denmark and the artist Marina Karella.
She is the older sister of Princess Olga.
She is a great-granddaughter of George I of Greece and Olga Constantinovna of Russia.
She is also a great-granddaughter of Prince Jean, Duke of Guise and a great-great-granddaughter of Christian IX of Denmark.
As Princess Alexandra's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, uses the style Your Highness instead of Her Royal Highness, and is excluded from the line of succession to the former Greek throne.
On 29 July 1973, Princess Alexandra's second cousin, Constantine II of Greece, was deposed and the Greek monarchy was abolished.
Career

Princess Alexandra is a certified child life specialist.
Princess Alexandra and her husband are patrons of the New York art scene.
She owns a portrait of her grandfather, Prince Christopher of Greece and Denmark, painted by Philip de László in 1919, as part of her collection.
Personal life

Princess Alexandra married the perfumer Nicolas Mirzayantz on 27 June 1998 in Torcello.
She attended the funeral of her father, Prince Michael on 1 August 2024, and was seen with other Greek royal family members, including Princess Olga, Queen Anne-Marie of Greece, Queen Sofía of Spain, and Crown Prince Pavlos.



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
  AssignClass (9d8952e3-302c-455b-8500-85b5741456fc)
 Call ID: 9d8952e3-302c-455b-8500-85b5741456fc
  Args:
    type: :Person
    source: Princess_Alexandra_of_Greece
  AssignClass (802fd2c9-89f6-47e6-a06a-8133006e0f75)
 Call ID: 802fd2c9-89f6-47e6-a06a-8133006e0f75
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Greece
  AssignClass (80b7017a-20c1-4c62-b1a2-3e1fd31517bb)
 Call ID: 80b7017a-20c1-4c62-b1a2-3e1fd31517bb
  Args:
    type: :Person
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (9e6b33ed-1370-4e63-b629-7b6f8c04bdb6)
 Call ID: 9e6b33ed-1370-4e63-b629-7b6f8c04bdb6
  Args:
    type: :Man
    source: Prince_Michael_of_Greece_and_Denmark
  AssignClass (ff801267-82c0-4d7a-8e83-25a65c3a92d2)
 Call ID: ff801267-82c0-4d7a-8e83-25a65c3a92d2
  Args:
    type: :Person
    source: Marina_Karella
  AssignClass (765b38f0-cd3e-4e7b-8e96-6d5a61512484)
 Call ID: 765b38f0-cd3e-4e7b-8e96-6d5a61512484
  Args:
    type: :Woman
    source: Marina_Karella
  AssignClass (f4e2e4fc-8953-4976-84a6-fe93342c9762)
 Call ID: f4e2e4fc-8953-4976-84a6-fe93342c9762
  Args:
    type: :Person
    source: Princess_Olga
  AssignClass (2e14dbfa-378d-4909-98b4-50e752733cf4)
 Call ID: 2e14dbfa-378d-4909-98b4-50e752733cf4
  Args:
    type: :Woman
    source: Princess_Olga
  AssignClass (35213276-f6ca-45a8-bf66-7f519b000af1)
 Call ID: 35213276-f6ca-45a8-bf66-7f519b000af1
  Args:
    type: :Person
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (e5ca9fff-3697-479c-9770-ee7557a15774)
 Call ID: e5ca9fff-3697-479c-9770-ee7557a15774
  Args:
    type: :Man
    source: Prince_Christopher_of_Greece_and_Denmark
  AssignClass (bf521248-e460-4ff2-a05a-db16cc79229b)
 Call ID: bf521248-e460-4ff2-a05a-db16cc79229b
  Args:
    type: :Person
    source: Nicolas_Mirzayantz
  AssignClass (86838f90-d0ac-488f-a9ab-c781bdefa13b)
 Call ID: 86838f90-d0ac-488f-a9ab-c781bdefa13b
  Args:
    type: :Man
    source: Nicolas_Mirzayantz
  AddLiteral (82a52f41-f461-4b34-8ec8-411d83333624)
 Call ID: 82a52f41-f461-4b34-8ec8-411d83333624
  Args:
    source: Princess_Alexandra_of_Greece
    relation: :knownAs
    literal_value: Alexandra Mirzayantz
    literal_type: xsd:string
  AddTriple (fccbce79-b28e-45bb-a610-3081099bde78)
 Call ID: fccbce79-b28e-45bb-a610-3081099bde78
  Args:
    source: Princess_Alexandra_of_Greece
    relation: :hasFather
    target: Prince_Michael_of_Greece_and_Denmark
  AddTriple (05ea75c3-ef48-454c-aa6d-e28395f5b208)
 Call ID: 05ea75c3-ef48-454c-aa6d-e28395f5b208
  Args:
    target: Marina_Karella
    source: Princess_Alexandra_of_Greece
    relation: :hasMother
  AddTriple (2908cd17-3923-4b46-b4ce-d6f707a5dc7d)
 Call ID: 2908cd17-3923-4b46-b4ce-d6f707a5dc7d
  Args:
    relation: :hasSister
    source: Princess_Alexandra_of_Greece
    target: Princess_Olga
  AddTriple (74b7678f-dbf7-43f6-ab27-ac5f6a437feb)
 Call ID: 74b7678f-dbf7-43f6-ab27-ac5f6a437feb
  Args:
    relation: :isFatherOf
    source: Prince_Christopher_of_Greece_and_Denmark
    target: Prince_Michael_of_Greece_and_Denmark
  AddTriple (b2b745e1-8012-4eba-a3b6-b6ede7937d6a)
 Call ID: b2b745e1-8012-4eba-a3b6-b6ede7937d6a
  Args:
    source: Princess_Alexandra_of_Greece
    relation: :hasRelation
    target: Nicolas_Mirzayantz
  AddLiteral (d9ad0aab-7c40-451d-821e-1493a381b155)
 Call ID: d9ad0aab-7c40-451d-821e-1493a381b155
  Args:
    source: Princess_Alexandra_of_Greece
    relation: :hasBirthYear
    literal_value: 1968
    literal_type: xsd:integer
  AddLiteral (5863d815-e36f-41d8-abb4-47792291298d)
 Call ID: 5863d815-e36f-41d8-abb4-47792291298d
  Args:
    source: Princess_Alexandra_of_Greece
    relation: :hasMarriageYear
    literal_value: 1998
    literal_type: xsd:integer
  Finish (b7cfd0a7-9689-49fd-b2a8-2e7c087a1a79)
 Call ID: b7cfd0a7-9689-49fd-b2a8-2e7c087a1a79
  Args: