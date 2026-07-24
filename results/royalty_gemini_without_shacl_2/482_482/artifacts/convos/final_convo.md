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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (f9f8cdc5-61c0-42d5-8577-a1c71021ff22)
 Call ID: f9f8cdc5-61c0-42d5-8577-a1c71021ff22
  Args:
    type: :Person
    source: :Catharina-Amalia
  AssignClass (6ae3404b-539b-41cc-b8c3-f1369a660951)
 Call ID: 6ae3404b-539b-41cc-b8c3-f1369a660951
  Args:
    type: :Woman
    source: :Catharina-Amalia
  AssignClass (6659522e-fb8c-44a4-b12e-617a34be5de0)
 Call ID: 6659522e-fb8c-44a4-b12e-617a34be5de0
  Args:
    type: :Person
    source: :Willem-Alexander
  AssignClass (b4ac7f7f-effa-4939-8b47-f7fbc6fca871)
 Call ID: b4ac7f7f-effa-4939-8b47-f7fbc6fca871
  Args:
    type: :Man
    source: :Willem-Alexander
  AssignClass (77217ba7-6234-4972-9b0a-a119b3eeedcd)
 Call ID: 77217ba7-6234-4972-9b0a-a119b3eeedcd
  Args:
    type: :Person
    source: :Máxima
  AssignClass (736646ba-4bbd-4821-99cc-054f994143df)
 Call ID: 736646ba-4bbd-4821-99cc-054f994143df
  Args:
    type: :Woman
    source: :Máxima
  AssignClass (d151c166-8ed3-4995-9b4b-2f457c19a6b8)
 Call ID: d151c166-8ed3-4995-9b4b-2f457c19a6b8
  Args:
    type: :Person
    source: :Alexia
  AssignClass (fc06641c-faef-4466-8e22-002d2589ba9f)
 Call ID: fc06641c-faef-4466-8e22-002d2589ba9f
  Args:
    type: :Woman
    source: :Alexia
  AssignClass (d93f4679-db62-4117-bc74-9a7a1505c38a)
 Call ID: d93f4679-db62-4117-bc74-9a7a1505c38a
  Args:
    type: :Person
    source: :Ariane
  AssignClass (1eb906bd-2e9c-4865-8eb6-b67781afae2f)
 Call ID: 1eb906bd-2e9c-4865-8eb6-b67781afae2f
  Args:
    type: :Woman
    source: :Ariane
  AssignClass (5d54df35-c2bf-4545-8dc2-c1eb0d3e1aa0)
 Call ID: 5d54df35-c2bf-4545-8dc2-c1eb0d3e1aa0
  Args:
    type: :Person
    source: :Beatrix
  AssignClass (8fc414a7-2dd1-411f-8791-db36670145f3)
 Call ID: 8fc414a7-2dd1-411f-8791-db36670145f3
  Args:
    type: :Woman
    source: :Beatrix
  AssignClass (c3bd3781-44c2-4658-8764-f15701240988)
 Call ID: c3bd3781-44c2-4658-8764-f15701240988
  Args:
    type: :Person
    source: :Constantijn
  AssignClass (ddc34d7b-81b4-4d66-a76d-ab85a4e81e0a)
 Call ID: ddc34d7b-81b4-4d66-a76d-ab85a4e81e0a
  Args:
    type: :Man
    source: :Constantijn
  AssignClass (5fb51945-c6ab-43f1-af85-996f4fdcc016)
 Call ID: 5fb51945-c6ab-43f1-af85-996f4fdcc016
  Args:
    type: :Person
    source: :JorgeZorreguieta
  AssignClass (09b6772d-96df-419d-ae52-156f6f582fc7)
 Call ID: 09b6772d-96df-419d-ae52-156f6f582fc7
  Args:
    type: :Man
    source: :JorgeZorreguieta
  AssignClass (d2e12ee9-92a9-48ca-bf7c-272cde684d23)
 Call ID: d2e12ee9-92a9-48ca-bf7c-272cde684d23
  Args:
    type: :Person
    source: :MaríaDelCarmenCerruti
  AssignClass (9b6211d8-9cee-4405-ae86-98ea835b7938)
 Call ID: 9b6211d8-9cee-4405-ae86-98ea835b7938
  Args:
    type: :Woman
    source: :MaríaDelCarmenCerruti
  AssignClass (2b840a04-e250-416d-8b1c-24bd49d10bdd)
 Call ID: 2b840a04-e250-416d-8b1c-24bd49d10bdd
  Args:
    type: :Person
    source: :MartínZorreguieta
  AssignClass (545f4c6c-28b6-45d3-8223-5f715aa7560f)
 Call ID: 545f4c6c-28b6-45d3-8223-5f715aa7560f
  Args:
    type: :Man
    source: :MartínZorreguieta
  AddLiteral (25a2f50e-64fa-4664-a97e-003fdc371bd5)
 Call ID: 25a2f50e-64fa-4664-a97e-003fdc371bd5
  Args:
    source: :Catharina-Amalia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2003
  AddTriple (cc4154d4-0982-459d-9ec1-db3f5835f406)
 Call ID: cc4154d4-0982-459d-9ec1-db3f5835f406
  Args:
    relation: :hasFather
    target: :Willem-Alexander
    source: :Catharina-Amalia
  AddTriple (cff0c777-0232-420c-a5ad-9f5ad4fda333)
 Call ID: cff0c777-0232-420c-a5ad-9f5ad4fda333
  Args:
    relation: :hasMother
    source: :Catharina-Amalia
    target: :Máxima
  AddTriple (0d553b4a-ffee-43e4-90ff-670efe47f545)
 Call ID: 0d553b4a-ffee-43e4-90ff-670efe47f545
  Args:
    target: :Alexia
    source: :Catharina-Amalia
    relation: :hasSister
  AddTriple (49263500-ee75-4492-bd43-2a5067d6e03e)
 Call ID: 49263500-ee75-4492-bd43-2a5067d6e03e
  Args:
    source: :Catharina-Amalia
    target: :Ariane
    relation: :hasSister
  AddTriple (d6caa2ba-e7be-463e-acdb-124c46eb0f91)
 Call ID: d6caa2ba-e7be-463e-acdb-124c46eb0f91
  Args:
    target: :Beatrix
    source: :Willem-Alexander
    relation: :hasFather
  AddTriple (402aa10e-c551-42cd-9588-8267dbde9ce1)
 Call ID: 402aa10e-c551-42cd-9588-8267dbde9ce1
  Args:
    relation: :hasMother
    source: :Willem-Alexander
    target: :Beatrix
  AddTriple (3dacef89-4065-4fa9-8d0a-9bf30680766d)
 Call ID: 3dacef89-4065-4fa9-8d0a-9bf30680766d
  Args:
    relation: :hasMother
    target: :MaríaDelCarmenCerruti
    source: :Catharina-Amalia
  AddTriple (01054b44-1b2b-4631-b94e-ee46b5760f04)
 Call ID: 01054b44-1b2b-4631-b94e-ee46b5760f04
  Args:
    source: :Catharina-Amalia
    target: :JorgeZorreguieta
    relation: :hasFather
  AddTriple (c1dd69ca-fd00-4cb4-ad6b-257d27e3b47b)
 Call ID: c1dd69ca-fd00-4cb4-ad6b-257d27e3b47b
  Args:
    target: :Willem-Alexander
    source: :Constantijn
    relation: :isBrotherOf
  AddTriple (8df973bc-2a72-48d0-a492-f30a71e90978)
 Call ID: 8df973bc-2a72-48d0-a492-f30a71e90978
  Args:
    relation: :isBrotherOf
    source: :MartínZorreguieta
    target: :Máxima
  Finish (70a2d35b-7d36-42f8-9130-7603ab93b188)
 Call ID: 70a2d35b-7d36-42f8-9130-7603ab93b188
  Args: