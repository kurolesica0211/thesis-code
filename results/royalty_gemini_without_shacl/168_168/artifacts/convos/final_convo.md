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
Infanta Pilar, Duchess of Badajoz, Viscountess of La Torre (Spanish: María del Pilar Alfonsa Juana
Luisa Ignacia y Todos los Santos de Borbón y Borbón; 30 July 1936 – 8 January 2020), sometimes known more simply as Pilar de Borbón, was the elder daughter of Infante Juan, Count of Barcelona and Princess María Mercedes of the Two Sicilies, and older sister of King Juan Carlos I.


Early life

Infanta Pilar was the firstborn daughter of Juan de Borbón y Battenberg and María de las Mercedes de Borbón y Orleans, Counts of Barcelona, she was born in Ville Saint Blaise, home of the counts of Barcelona in Cannes (Alpes-Maritimes, France), on 30 July 1936.
She was baptized in Cannes, in the church of Rins, with the name of María del Pilar Alfonsa Juana
Her godparents were her paternal grandfather, King Alfonso XIII and her maternal grandmother the Princess Louise of Orléans, although Alfonso XIII acted by delegation as he did not want to meet his wife Queen Victoria Eugenia.
From her birth, as the daughter of the heir to the Crown of Spain she was given the title of Infanta of Spain with treatment of Royal Highness.
In 1941, after the resignation of Alfonso XIII, her father became the holder of the dynastic rights of the Spanish Crown in exile.
Together with her parents and her brother Juan Carlos, she took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On this trip, Juan Carlos met the hosts' 15-year-old daughter, Sofia, his future wife, for the first time.
At the wedding of her brother Juan Carlos I of Spain with Princess Sofía of Greece, in 1962, she was one of eight bridesmaids.
Marriage and family

Pilar needed to renounce her rights of succession to the Spanish throne to marry a commoner as stipulated by the Pragmatic Sanction of Charles III on marriages of members of the royal family.
To honor the marriage, Infante Juan, Count of Barcelona, created her Duchess of Badajoz.
Equestrian sport

Pilar de Borbón had been supporting international equestrian sport.
She was President of the International Equestrian Federation from 1994 to 2006, succeeded by HRH Princess Haya bint al Hussein.
From 1996 to 2006 she was a member of the International Olympic Committee for Spain, when she became an honorary member, and Member of the Executive Board of the Spanish Olympic Committee.
Philanthropic and other activities

Pilar de Borbón was one of the founders of Asociación Nuevo Futuro ("New Future Association") in 1968, an international child support organization, and was its president and then president of honor.
The event even received the visit of the Queens of Spain, Letizia and Sofia.
Pilar de Borbón was also a member of the board of directors of the Queen Sofía Spanish Institute in New York City, president of the World Monuments Fund España and, from 2007 to 2009, president of Europa Nostra, the European Federation for the Defense of Cultural Heritage.
She was also a music fan and accompanied her brother, King Juan Carlos of Spain, and nephews to bullfighting matches.
Financial holdings

Mossack Fonseca files document that in August 1974, Pilar de Borbón became president and director of the Panama-registered company Delantera Financiera SA (registered May 1969) with her husband as secretary-treasurer and director.
In 1993, London-based Timothy Lloyd who had represented the undisclosed owner of the company said that Pilar de Borbón owned it.
After March 1993, the intermediary representing the company was Madrid-based Gómez-Acebo & Pombo  Abogados, a law firm founded by Pilar de Borbón's brother-in-law Ignacio Gómez-Acebo .
From July 2006 until its dissolution in June 2014, five days before the installation of her nephew Felipe VI, Pilar de Borbón's son Bruno Alejandro Gómez-Acebo Borbón was director and treasurer of the company.
Illness and death

Pilar was operated for an intestinal obstruction on 2 February 2019 in Madrid, and was diagnosed with colon cancer in 2019, being made public in May of the same year.
On 28 January, her funeral was held in El Escorial basilica, attended by her nephew King Felipe VI, former Queen of the Netherlands, Princess Beatrix, her brother Juan Carlos I and Queen Sofía, cousin-in-law by marriage Queen Margarita (wife of Simeon II of Bulgaria), the Duke of Braganza Duarte Pio, and Spanish political authorities represented by Deputy Prime Minister Carmen Calvo, Mayor of Madrid José Luis Martínez-Almeida and President of the Congress of Deputies Meritxell Batet.
Titles, styles and honours

As daughter of the prince of Asturias, Pilar was born infanta of Spain with the style of Royal Highness.
Later, her father granted her the title of Duchess of Badajoz, a title of the Royal House that cannot be inherited by her children.



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
  AssignClass (be9481bf-380d-429b-9f4c-cf9ab9671810)
 Call ID: be9481bf-380d-429b-9f4c-cf9ab9671810
  Args:
    type: :Woman
    source: Infanta_Pilar
  AssignClass (de99b860-2a7e-4364-96a4-464a440c3873)
 Call ID: de99b860-2a7e-4364-96a4-464a440c3873
  Args:
    type: :Person
    source: Infanta_Pilar
  AddLiteral (f1e55847-ae63-462c-a730-bf26222a4536)
 Call ID: f1e55847-ae63-462c-a730-bf26222a4536
  Args:
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Pilar de Borbón
    source: Infanta_Pilar
  AssignClass (bf920a88-a0c8-487c-b9f4-c9e9094dbcd6)
 Call ID: bf920a88-a0c8-487c-b9f4-c9e9094dbcd6
  Args:
    type: :Man
    source: Juan_de_Borbon_y_Battenberg
  AssignClass (b0a76819-8595-442b-bcab-bd29a51eebf8)
 Call ID: b0a76819-8595-442b-bcab-bd29a51eebf8
  Args:
    type: :Person
    source: Juan_de_Borbon_y_Battenberg
  AssignClass (d8b86477-30b9-4514-bc61-4c0b71265f98)
 Call ID: d8b86477-30b9-4514-bc61-4c0b71265f98
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_de_Borbon_y_Orleans
  AssignClass (125f4a0d-4e2c-4d80-ab8d-6c31cd6d2ffb)
 Call ID: 125f4a0d-4e2c-4d80-ab8d-6c31cd6d2ffb
  Args:
    type: :Person
    source: Maria_de_las_Mercedes_de_Borbon_y_Orleans
  AddTriple (fa0bde19-b72e-4118-843b-be8f40a2a8ee)
 Call ID: fa0bde19-b72e-4118-843b-be8f40a2a8ee
  Args:
    relation: :hasFather
    source: Infanta_Pilar
    target: Juan_de_Borbon_y_Battenberg
  AddTriple (ba9040b1-3651-468e-864a-4cdcc0080d61)
 Call ID: ba9040b1-3651-468e-864a-4cdcc0080d61
  Args:
    relation: :hasMother
    source: Infanta_Pilar
    target: Maria_de_las_Mercedes_de_Borbon_y_Orleans
  AssignClass (221aaf17-b587-45d8-87c6-11b32f8ab1ee)
 Call ID: 221aaf17-b587-45d8-87c6-11b32f8ab1ee
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (e163b424-b5a9-4ecc-8207-e592886975d8)
 Call ID: e163b424-b5a9-4ecc-8207-e592886975d8
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (4568b025-8e49-40b3-ab6f-bb0c977c0802)
 Call ID: 4568b025-8e49-40b3-ab6f-bb0c977c0802
  Args:
    source: Infanta_Pilar
    target: Juan_Carlos_I
    relation: :hasBrother
  AddTriple (b4b18669-c7ad-4048-93b3-d2e59ca521bf)
 Call ID: b4b18669-c7ad-4048-93b3-d2e59ca521bf
  Args:
    relation: :hasFather
    source: Juan_Carlos_I
    target: Juan_de_Borbon_y_Battenberg
  AddTriple (e6a6325d-0bdc-4adc-a346-b1aaf3bdb23c)
 Call ID: e6a6325d-0bdc-4adc-a346-b1aaf3bdb23c
  Args:
    relation: :hasMother
    source: Juan_Carlos_I
    target: Maria_de_las_Mercedes_de_Borbon_y_Orleans
  AssignClass (7eb9add2-e266-4e77-9c24-b12972bc7acf)
 Call ID: 7eb9add2-e266-4e77-9c24-b12972bc7acf
  Args:
    type: :Man
    source: Bruno_Alejandro_Gomez_Acebo_Borbon
  AssignClass (effe54ea-85cf-4ec6-a2e9-166192200866)
 Call ID: effe54ea-85cf-4ec6-a2e9-166192200866
  Args:
    type: :Person
    source: Bruno_Alejandro_Gomez_Acebo_Borbon
  AddTriple (bc24897c-c9f5-427d-b1d4-df55710e1d38)
 Call ID: bc24897c-c9f5-427d-b1d4-df55710e1d38
  Args:
    relation: :isSonOf
    source: Bruno_Alejandro_Gomez_Acebo_Borbon
    target: Infanta_Pilar
  Finish (65c8a72c-6c3d-41bd-bf17-1f8c7e827b92)
 Call ID: 65c8a72c-6c3d-41bd-bf17-1f8c7e827b92
  Args: