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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a9f2c1d7-4850-4d44-888a-49c6869924e4)
 Call ID: a9f2c1d7-4850-4d44-888a-49c6869924e4
  Args:
    type: :Woman
    source: :Pilar_de_Borbon
  AssignClass (4b32bbfe-680b-43f2-850c-2e4e0b8cfe08)
 Call ID: 4b32bbfe-680b-43f2-850c-2e4e0b8cfe08
  Args:
    source: :Pilar_de_Borbon
    type: :Person
  AddLiteral (53dc46a3-48d7-46da-bb3e-130a5b9708a3)
 Call ID: 53dc46a3-48d7-46da-bb3e-130a5b9708a3
  Args:
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasBirthYear
    source: :Pilar_de_Borbon
  AddLiteral (befab72b-d179-4922-b129-9580dc12ed15)
 Call ID: befab72b-d179-4922-b129-9580dc12ed15
  Args:
    literal_value: 2020
    relation: :hasDeathYear
    source: :Pilar_de_Borbon
    literal_type: xsd:integer
  AddLiteral (db422b9d-e937-495c-8fca-481ebb0cb57c)
 Call ID: db422b9d-e937-495c-8fca-481ebb0cb57c
  Args:
    literal_value: Pilar de Borbón
    source: :Pilar_de_Borbon
    relation: :knownAs
    literal_type: xsd:string
  AssignClass (c9b6c8fb-deef-4cb0-a65d-98bce475489b)
 Call ID: c9b6c8fb-deef-4cb0-a65d-98bce475489b
  Args:
    source: :Juan_de_Borbon
    type: :Man
  AssignClass (6b4cdda8-3695-4a41-bf12-8bd9d31175ed)
 Call ID: 6b4cdda8-3695-4a41-bf12-8bd9d31175ed
  Args:
    source: :Juan_de_Borbon
    type: :Ancestor
  AssignClass (c820801e-a12d-4cc4-b7e2-2850df4f6744)
 Call ID: c820801e-a12d-4cc4-b7e2-2850df4f6744
  Args:
    source: :Juan_de_Borbon
    type: :Person
  AssignClass (ebd858d8-2d19-478c-8133-f082d6125153)
 Call ID: ebd858d8-2d19-478c-8133-f082d6125153
  Args:
    type: :Woman
    source: :Maria_Mercedes_de_Borbon
  AssignClass (ee364720-b3d2-414c-888b-7440da41667f)
 Call ID: ee364720-b3d2-414c-888b-7440da41667f
  Args:
    source: :Maria_Mercedes_de_Borbon
    type: :Ancestor
  AssignClass (7a2905a9-c52a-4b9b-96bb-a396c136a37e)
 Call ID: 7a2905a9-c52a-4b9b-96bb-a396c136a37e
  Args:
    source: :Maria_Mercedes_de_Borbon
    type: :Person
  AddTriple (a148610f-536f-4893-938b-6eca3e6bebb1)
 Call ID: a148610f-536f-4893-938b-6eca3e6bebb1
  Args:
    target: :Juan_de_Borbon
    relation: :hasFather
    source: :Pilar_de_Borbon
  AddTriple (637216f6-575d-485f-b2f3-570df8444138)
 Call ID: 637216f6-575d-485f-b2f3-570df8444138
  Args:
    source: :Pilar_de_Borbon
    relation: :hasMother
    target: :Maria_Mercedes_de_Borbon
  AssignClass (e0e1626b-1399-4007-bd16-6714d63880f6)
 Call ID: e0e1626b-1399-4007-bd16-6714d63880f6
  Args:
    type: :Man
    source: :Juan_Carlos_I
  AssignClass (18819b43-7f01-46f0-835d-cfcc9f678c40)
 Call ID: 18819b43-7f01-46f0-835d-cfcc9f678c40
  Args:
    source: :Juan_Carlos_I
    type: :Person
  AddTriple (abfde567-ff68-4156-b314-8c5ae4c7504a)
 Call ID: abfde567-ff68-4156-b314-8c5ae4c7504a
  Args:
    target: :Juan_Carlos_I
    source: :Pilar_de_Borbon
    relation: :hasBrother
  AssignClass (eb9ab886-2e24-4c9d-a767-eb36279ef696)
 Call ID: eb9ab886-2e24-4c9d-a767-eb36279ef696
  Args:
    type: :Man
    source: :Bruno_Alejandro_Gomez_Acebo_Borbon
  AssignClass (0928bc8d-bc21-4c61-8162-b3057800d2fe)
 Call ID: 0928bc8d-bc21-4c61-8162-b3057800d2fe
  Args:
    type: :Person
    source: :Bruno_Alejandro_Gomez_Acebo_Borbon
  AddTriple (4db651fc-8c69-4858-b510-5148629ec063)
 Call ID: 4db651fc-8c69-4858-b510-5148629ec063
  Args:
    relation: :isSonOf
    source: :Bruno_Alejandro_Gomez_Acebo_Borbon
    target: :Pilar_de_Borbon
  AssignClass (2e910481-7fbf-45f4-89d4-0ec98dd3f3b7)
 Call ID: 2e910481-7fbf-45f4-89d4-0ec98dd3f3b7
  Args:
    type: :Man
    source: :Felipe_VI
  AssignClass (c32d58ca-3a16-4775-ad2d-198835dfb6fc)
 Call ID: c32d58ca-3a16-4775-ad2d-198835dfb6fc
  Args:
    type: :Person
    source: :Felipe_VI
  AddTriple (9f3b0af7-95a7-42fd-8ac3-0948df71af7c)
 Call ID: 9f3b0af7-95a7-42fd-8ac3-0948df71af7c
  Args:
    relation: :hasRelation
    source: :Pilar_de_Borbon
    target: :Felipe_VI
  Finish (44e41ea2-e06f-4bb4-ae15-8342a089e66f)
 Call ID: 44e41ea2-e06f-4bb4-ae15-8342a089e66f
  Args: