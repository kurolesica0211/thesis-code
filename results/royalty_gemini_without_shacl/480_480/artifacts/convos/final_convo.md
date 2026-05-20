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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Catharina-Amalia, Princess of Orange (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Dutch pronunciation: ; Catharina-Amalia Beatrix Carmen Victoria; born 7 December 2003) is the heir apparent to the throne of the Kingdom of the Netherlands, which consists of the constituent countries of Aruba, Curaçao, the Netherlands, and Sint Maarten.
Catharina-Amalia is the eldest child of King Willem-Alexander and Queen Máxima.
She has two younger sisters, Princess Alexia and Princess Ariane.
Early life

Princess Catharina-Amalia Beatrix Carmen Victoria of the Netherlands was born at 17:01 CET on 7 December 2003 in the HMC Bronovo in The Hague, the first child of the then Willem-Alexander, Prince of Orange (now king) and Princess Máxima.
Upon the public announcement of her birth, 101 salute shots were fired at four places in the Kingdom of the Netherlands: Den Helder and The Hague in the Netherlands, Willemstad in Curaçao, and Oranjestad in Aruba.
On 12 June 2004, Catharina-Amalia was baptised by the Rev. Carel ter Linden in the Great Church in The Hague.
Her godparents are her uncle Prince Constantijn, Crown Princess Victoria of Sweden, the (then) vice-president of the Council of State of the Netherlands Herman Tjeenk Willink, her mother's friend Samantha Deane, her uncle Martín Zorreguieta, and her father's friend Marc ter Haar.
Catharina-Amalia's maternal grandparents, Jorge Zorreguieta and María del Carmen Cerruti, were prohibited from attending her parents' wedding in 2002 due to Zorreguieta's involvement in the regime of General Jorge Rafael Videla, but were present at her baptism, which was a private rather than a state affair.
Princess Catharina-Amalia has two younger sisters: Princess Alexia (born in 2005) and Princess Ariane (born in 2007).
Her birthdays are traditionally celebrated with a concert at the Kloosterkerk in The Hague, which is attended by ambassadors and members of the royal household and the Council of State of the Netherlands.
Catharina-Amalia's paternal grandmother, Queen Beatrix, abdicated on 30 April 2013 and her father ascended the throne.
Catharina-Amalia, as the new heir apparent, assumed the title of Princess of Orange, becoming the first to do so in her own right.
Education

In December 2007, Catharina-Amalia started attending Bloemcamp Primary School, a public primary school in Wassenaar.
After graduating from primary school, she attended the Christelijk Gymnasium Sorghvliet in The Hague, where her aunt Princess Laurentien attended.
After completing her studies at Sorghvliet, Catharina-Amalia took a gap year, during which she interned at the Orange Fund and volunteered at other organisations.
Catharina-Amalia studied at the University of Amsterdam for a Bachelor of Science degree in Politics, Psychology, Law and Economics (PPLE).
In April 2024, King Willem-Alexander revealed that Catharina-Amalia lived in Madrid in 2023 under the protection of the Spanish monarchy, while she continued her studies online, due to the threats from the Moroccan mafia, a criminal organization dedicated to drug trafficking that has been threatening to kidnap her.
In August 2024, the Dutch Broadcasting Foundation announced that Catharina-Amalia joined Amsterdam corps, a Dutch student association.
Catharina-Amalia graduated with a Bachelor of Science degree in PPLE in July 2025.
Catharina-Amalia speaks Dutch, English, and Spanish (her mother's first language).
Public life

Catharina-Amalia and her sisters attended the annual Koningsdag.
On 19 June 2010, Catharina-Amalia served as a bridesmaid at the wedding of Crown Princess Victoria of Sweden and Daniel Westling.
On the occasion of her 18th birthday in 2021, a biography of Catharina-Amalia was published.
Similar books were published on the 18th birthday of Princess Beatrix in 1956 and Prince Willem-Alexander in 1985.
The book titled "Amalia" is written by Dutch entertainer Claudia de Breij.
On 8 December 2021, Catharina-Amalia assumed her seat in the Advisory Division of the Council of State when she reached the age of majority at 18 the day before.
On 17 June 2022, together with her parents, she was among the royal guests invited to the celebrations of the 18th birthday of Princess Ingrid Alexandra of Norway.
This was Catharina-Amalia's first public engagement outside of the Netherlands and the first occasion to which she was allowed to wear a tiara.
On 20 September 2022, together with her parents, Catharina-Amalia attended Prinsjesdag, where the King addressed a joint session of the States General of the Netherlands to outline government policy for the upcoming parliamentary session.
In November 2022, Catharina-Amalia and her family visited an exhibition at Nieuwe Kerk dedicated to Queen Juliana.
In January and February 2023, Catharina-Amalia went on a tour of the Dutch Caribbean with her parents.
In April 2023, Catharina-Amalia and her sister Princess Ariane attended King's Day concert in Rotterdam.
On 5 May 2023, she accompanied her grandmother to a reception held at Buckingham Palace the evening before the coronation of King Charles III and Queen Camilla of the United Kingdom.
Catharina-Amalia attended her first state banquet, honouring King Felipe VI and Queen Letizia of Spain, in April 2024.
In June 2025, Catharina-Amalia underwent surgery after falling from a horse and fracturing her arm.
Public image

Catharina-Amalia has experienced repeated fat shaming by tabloids and on social media since she was young, most notably by the Portuguese celebrity magazine Caras labeling her as plus size.
In response to the body shaming, members of the public have expressed their support for the princess, calling the fat shaming against her unacceptable.
Annual allowance

Catharina-Amalia became entitled to an annual allowance from the Dutch state upon reaching the age of 18.
Following her high school graduation, Catharina-Amalia opted to decline the annual allowance until she completed her studies.
In May 2024, citing changed circumstances, Catharina-Amalia announced she would begin utilizing her annual allowance for staff and operational expenses, starting in January 2025.
Titles, styles, honours and arms

Titles

Honours

National

Foreign

Honorific eponyms

Geographic locations

Structures

Other

Arms

See also

Notes

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (af700ab4-ca1f-4403-86d2-133143933845)
 Call ID: af700ab4-ca1f-4403-86d2-133143933845
  Args:
    type: :Person
    source: Catharina-Amalia
  AssignClass (f0a6a6d3-8a65-42e9-8dcb-95c048730efe)
 Call ID: f0a6a6d3-8a65-42e9-8dcb-95c048730efe
  Args:
    source: Catharina-Amalia
    type: :Woman
  AssignClass (80856640-7695-4702-b0b9-e387c4088cb5)
 Call ID: 80856640-7695-4702-b0b9-e387c4088cb5
  Args:
    type: :Person
    source: Willem-Alexander
  AssignClass (7b30f8b6-4f41-4505-9e14-eb571ee45d44)
 Call ID: 7b30f8b6-4f41-4505-9e14-eb571ee45d44
  Args:
    type: :Man
    source: Willem-Alexander
  AssignClass (3da30b1e-8f8f-49da-97dd-e914fca593fb)
 Call ID: 3da30b1e-8f8f-49da-97dd-e914fca593fb
  Args:
    type: :Person
    source: Máxima
  AssignClass (d2f09f09-f0dc-48c5-a1e3-bfbfae7dcbf5)
 Call ID: d2f09f09-f0dc-48c5-a1e3-bfbfae7dcbf5
  Args:
    source: Máxima
    type: :Woman
  AssignClass (791a6e01-cdf3-46f6-925e-e2508af65236)
 Call ID: 791a6e01-cdf3-46f6-925e-e2508af65236
  Args:
    type: :Person
    source: Alexia
  AssignClass (04ed06e6-76ea-4553-a6db-a7b52eca64a1)
 Call ID: 04ed06e6-76ea-4553-a6db-a7b52eca64a1
  Args:
    type: :Woman
    source: Alexia
  AssignClass (101920df-c39f-44e8-9fce-b4cd6ad3622d)
 Call ID: 101920df-c39f-44e8-9fce-b4cd6ad3622d
  Args:
    source: Ariane
    type: :Person
  AssignClass (18de7609-bb89-4a99-b7f5-2fd77dc80488)
 Call ID: 18de7609-bb89-4a99-b7f5-2fd77dc80488
  Args:
    type: :Woman
    source: Ariane
  AssignClass (ef69a2b7-6335-4433-9ed2-1e70f6e13a41)
 Call ID: ef69a2b7-6335-4433-9ed2-1e70f6e13a41
  Args:
    source: Beatrix
    type: :Person
  AssignClass (68025ed1-16e7-4c10-8c1d-ad041c138fcd)
 Call ID: 68025ed1-16e7-4c10-8c1d-ad041c138fcd
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (de19949b-efee-4a9a-8503-c789df644256)
 Call ID: de19949b-efee-4a9a-8503-c789df644256
  Args:
    type: :Person
    source: Jorge Zorreguieta
  AssignClass (ba0c9803-a81d-4f16-80a3-ce946dede974)
 Call ID: ba0c9803-a81d-4f16-80a3-ce946dede974
  Args:
    type: :Man
    source: Jorge Zorreguieta
  AssignClass (be538e28-8429-485d-8ef7-07a4914f1e45)
 Call ID: be538e28-8429-485d-8ef7-07a4914f1e45
  Args:
    type: :Person
    source: María del Carmen Cerruti
  AssignClass (5519c0c9-22e5-4bb9-aabb-11d5c853449a)
 Call ID: 5519c0c9-22e5-4bb9-aabb-11d5c853449a
  Args:
    source: María del Carmen Cerruti
    type: :Woman
  AddTriple (63128c4b-e4fb-4704-94ae-d73c165172ea)
 Call ID: 63128c4b-e4fb-4704-94ae-d73c165172ea
  Args:
    relation: :hasFather
    target: Willem-Alexander
    source: Catharina-Amalia
  AddTriple (787649fa-da4a-41e8-8e35-6fd862c4391a)
 Call ID: 787649fa-da4a-41e8-8e35-6fd862c4391a
  Args:
    relation: :hasMother
    source: Catharina-Amalia
    target: Máxima
  AddTriple (21c63fc7-0cd7-40dd-aff1-77aecd018f99)
 Call ID: 21c63fc7-0cd7-40dd-aff1-77aecd018f99
  Args:
    relation: :hasSister
    target: Alexia
    source: Catharina-Amalia
  AddTriple (347625ec-2905-479b-91f6-abb86f11d992)
 Call ID: 347625ec-2905-479b-91f6-abb86f11d992
  Args:
    source: Catharina-Amalia
    target: Ariane
    relation: :hasSister
  AddTriple (4fe4ad35-649f-482d-a180-a5303c119de1)
 Call ID: 4fe4ad35-649f-482d-a180-a5303c119de1
  Args:
    target: Willem-Alexander
    source: Alexia
    relation: :hasFather
  AddTriple (40035c16-86ac-4de5-aaa2-991fb2edc0bd)
 Call ID: 40035c16-86ac-4de5-aaa2-991fb2edc0bd
  Args:
    source: Alexia
    target: Máxima
    relation: :hasMother
  AddTriple (5df93d8e-db3b-46a0-93f3-4cf6a010fd30)
 Call ID: 5df93d8e-db3b-46a0-93f3-4cf6a010fd30
  Args:
    target: Willem-Alexander
    source: Ariane
    relation: :hasFather
  AddTriple (263f502c-6da0-43b6-8cc1-2c5ed9d2ae9a)
 Call ID: 263f502c-6da0-43b6-8cc1-2c5ed9d2ae9a
  Args:
    relation: :hasMother
    source: Ariane
    target: Máxima
  AddLiteral (ecdb712e-fe74-455e-9472-fb989e6a4043)
 Call ID: ecdb712e-fe74-455e-9472-fb989e6a4043
  Args:
    source: Catharina-Amalia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2003
  AddLiteral (f8dbc894-c3ae-404d-9bfd-fab977490137)
 Call ID: f8dbc894-c3ae-404d-9bfd-fab977490137
  Args:
    relation: :hasBirthYear
    literal_value: 2005
    source: Alexia
    literal_type: xsd:integer
  AddLiteral (120c19da-2251-42c0-97e4-d47844c651a9)
 Call ID: 120c19da-2251-42c0-97e4-d47844c651a9
  Args:
    literal_value: 2007
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Ariane
  AddTriple (7731bd31-f8da-455c-a6ee-886b598a24ba)
 Call ID: 7731bd31-f8da-455c-a6ee-886b598a24ba
  Args:
    relation: :hasMother
    source: Máxima
    target: María del Carmen Cerruti
  AddTriple (6c0a3edd-d0d3-4d0a-821e-8ee0851163bb)
 Call ID: 6c0a3edd-d0d3-4d0a-821e-8ee0851163bb
  Args:
    relation: :hasFather
    source: Máxima
    target: Jorge Zorreguieta
  AddTriple (fc28812e-5da8-4b48-ac8c-f15066ee66e2)
 Call ID: fc28812e-5da8-4b48-ac8c-f15066ee66e2
  Args:
    relation: :hasMother
    target: Beatrix
    source: Willem-Alexander
  Finish (563df21d-7d0c-4be5-9ee7-c39fb47749e9)
 Call ID: 563df21d-7d0c-4be5-9ee7-c39fb47749e9
  Args: