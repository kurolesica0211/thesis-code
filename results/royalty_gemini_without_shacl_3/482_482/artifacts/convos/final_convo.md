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
  AssignClass (b362f90a-64b8-48d2-a9e9-1573b71db602)
 Call ID: b362f90a-64b8-48d2-a9e9-1573b71db602
  Args:
    type: :Person
    source: :Catharina-Amalia
  AssignClass (d000a277-81c1-434a-9920-95b998176f63)
 Call ID: d000a277-81c1-434a-9920-95b998176f63
  Args:
    source: :Catharina-Amalia
    type: :Woman
  AddLiteral (7f6c6944-b722-4282-b3fc-9211681d43bd)
 Call ID: 7f6c6944-b722-4282-b3fc-9211681d43bd
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2003
    source: :Catharina-Amalia
  AssignClass (fc9e6789-4d3d-423c-82eb-5f5dffc222ad)
 Call ID: fc9e6789-4d3d-423c-82eb-5f5dffc222ad
  Args:
    source: :Willem-Alexander
    type: :Person
  AssignClass (9992a904-0645-4d3a-ae75-7b35f23b80ff)
 Call ID: 9992a904-0645-4d3a-ae75-7b35f23b80ff
  Args:
    source: :Willem-Alexander
    type: :Man
  AssignClass (fb4e3e40-5afc-4d48-b5df-0dff62f796eb)
 Call ID: fb4e3e40-5afc-4d48-b5df-0dff62f796eb
  Args:
    source: :Máxima
    type: :Person
  AssignClass (fd9a6bd9-f880-4a6f-85ef-0b7f59de6ea2)
 Call ID: fd9a6bd9-f880-4a6f-85ef-0b7f59de6ea2
  Args:
    type: :Woman
    source: :Máxima
  AddTriple (8904a25f-159d-4f51-b16d-7396ab362dd3)
 Call ID: 8904a25f-159d-4f51-b16d-7396ab362dd3
  Args:
    source: :Catharina-Amalia
    target: :Willem-Alexander
    relation: :hasFather
  AddTriple (b1977744-23d0-4f24-9e31-e24b96e89853)
 Call ID: b1977744-23d0-4f24-9e31-e24b96e89853
  Args:
    source: :Catharina-Amalia
    target: :Máxima
    relation: :hasMother
  AssignClass (27be4584-5b2c-4b23-9d2a-25efeac386ca)
 Call ID: 27be4584-5b2c-4b23-9d2a-25efeac386ca
  Args:
    source: :Alexia
    type: :Person
  AssignClass (5218beb4-0a05-478a-afbd-8a900bedea82)
 Call ID: 5218beb4-0a05-478a-afbd-8a900bedea82
  Args:
    source: :Alexia
    type: :Woman
  AddLiteral (76a7614a-aff8-4d6b-a43c-bc7f9124f552)
 Call ID: 76a7614a-aff8-4d6b-a43c-bc7f9124f552
  Args:
    relation: :hasBirthYear
    source: :Alexia
    literal_value: 2005
    literal_type: xsd:integer
  AddTriple (ae53c956-9653-45cf-8b80-32fe0bc51553)
 Call ID: ae53c956-9653-45cf-8b80-32fe0bc51553
  Args:
    source: :Alexia
    relation: :isSisterOf
    target: :Catharina-Amalia
  AssignClass (bb90b13f-3449-4f00-ac00-d1d0c993c6b4)
 Call ID: bb90b13f-3449-4f00-ac00-d1d0c993c6b4
  Args:
    type: :Person
    source: :Ariane
  AssignClass (5312cd29-bb03-40c0-b91e-e7027ea3ea2e)
 Call ID: 5312cd29-bb03-40c0-b91e-e7027ea3ea2e
  Args:
    source: :Ariane
    type: :Woman
  AddLiteral (952c85d0-381d-4590-9f01-b476337a7814)
 Call ID: 952c85d0-381d-4590-9f01-b476337a7814
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Ariane
    literal_value: 2007
  AddTriple (3e85a729-da70-49e5-9bd2-5da61c32a58a)
 Call ID: 3e85a729-da70-49e5-9bd2-5da61c32a58a
  Args:
    relation: :isSisterOf
    target: :Catharina-Amalia
    source: :Ariane
  AssignClass (a2efa9a4-9960-4ef9-98fb-abe047c674d5)
 Call ID: a2efa9a4-9960-4ef9-98fb-abe047c674d5
  Args:
    type: :Person
    source: :Beatrix
  AssignClass (56055347-d281-4ce8-821e-029b7567566b)
 Call ID: 56055347-d281-4ce8-821e-029b7567566b
  Args:
    type: :Woman
    source: :Beatrix
  AddTriple (ed32ffbe-7b9d-4021-8aa4-dd45dd231a43)
 Call ID: ed32ffbe-7b9d-4021-8aa4-dd45dd231a43
  Args:
    source: :Willem-Alexander
    target: :Beatrix
    relation: :hasMother
  AssignClass (986c5f6b-0e83-4c31-9657-1c53ee127698)
 Call ID: 986c5f6b-0e83-4c31-9657-1c53ee127698
  Args:
    type: :Person
    source: :Jorge_Zorreguieta
  AssignClass (fc8a95c7-52ee-46a6-8125-0637276aaf41)
 Call ID: fc8a95c7-52ee-46a6-8125-0637276aaf41
  Args:
    source: :Jorge_Zorreguieta
    type: :Man
  AssignClass (6ab394be-7e4d-4698-823d-04c622660742)
 Call ID: 6ab394be-7e4d-4698-823d-04c622660742
  Args:
    type: :Person
    source: :Maria_del_Carmen_Cerruti
  AssignClass (3e84fd84-b360-4a9b-8f10-b44e5714466f)
 Call ID: 3e84fd84-b360-4a9b-8f10-b44e5714466f
  Args:
    type: :Woman
    source: :Maria_del_Carmen_Cerruti
  AddTriple (ed9a36e1-4b5b-41ef-820f-b53e7e5a1b1a)
 Call ID: ed9a36e1-4b5b-41ef-820f-b53e7e5a1b1a
  Args:
    source: :Máxima
    relation: :hasFather
    target: :Jorge_Zorreguieta
  AddTriple (8ebe6d3b-a7a9-4a0b-8571-cef93e8ec759)
 Call ID: 8ebe6d3b-a7a9-4a0b-8571-cef93e8ec759
  Args:
    source: :Máxima
    relation: :hasMother
    target: :Maria_del_Carmen_Cerruti
  AssignClass (99f99a78-0377-4a7b-a34d-0b42ec9e4e5b)
 Call ID: 99f99a78-0377-4a7b-a34d-0b42ec9e4e5b
  Args:
    type: :Person
    source: :Constantijn
  AssignClass (4d68b380-fbcd-4d7f-87c6-5c4c65a5c469)
 Call ID: 4d68b380-fbcd-4d7f-87c6-5c4c65a5c469
  Args:
    type: :Man
    source: :Constantijn
  AddTriple (f4b90c61-cbcb-45a6-9e3b-ba657c7c998f)
 Call ID: f4b90c61-cbcb-45a6-9e3b-ba657c7c998f
  Args:
    source: :Constantijn
    target: :Beatrix
    relation: :hasFather
  AssignClass (4c55ad0c-b744-492d-a443-45b35f89e2a6)
 Call ID: 4c55ad0c-b744-492d-a443-45b35f89e2a6
  Args:
    source: :Laurentien
    type: :Person
  AssignClass (81ab46d0-fc71-422b-b8d8-e553d641eff8)
 Call ID: 81ab46d0-fc71-422b-b8d8-e553d641eff8
  Args:
    source: :Laurentien
    type: :Woman
  AddTriple (ae343864-fa23-4633-adff-3fc4a0304bbe)
 Call ID: ae343864-fa23-4633-adff-3fc4a0304bbe
  Args:
    source: :Laurentien
    relation: :isSisterOf
    target: :Constantijn
  AssignClass (604eec34-a425-4c2f-97c0-77c843aa84a7)
 Call ID: 604eec34-a425-4c2f-97c0-77c843aa84a7
  Args:
    type: :Person
    source: :Margriet
  AssignClass (82ea88d2-400c-49e4-a037-5f578672a36f)
 Call ID: 82ea88d2-400c-49e4-a037-5f578672a36f
  Args:
    source: :Margriet
    type: :Woman
  AssignClass (d5925ea6-db7d-4b1f-99cc-5ef5f4253128)
 Call ID: d5925ea6-db7d-4b1f-99cc-5ef5f4253128
  Args:
    source: :Pieter_van_Vollenhoven
    type: :Person
  AssignClass (d3b2cd04-88e3-4350-a96d-8f07a8852286)
 Call ID: d3b2cd04-88e3-4350-a96d-8f07a8852286
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  Finish (84d216b8-8d43-452e-841b-276f19bafb4b)
 Call ID: 84d216b8-8d43-452e-841b-276f19bafb4b
  Args: