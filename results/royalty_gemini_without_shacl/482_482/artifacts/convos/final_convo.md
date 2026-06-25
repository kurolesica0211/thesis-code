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
  AssignClass (571ea07d-1bb5-4a4d-99db-ae85c83492d5)
 Call ID: 571ea07d-1bb5-4a4d-99db-ae85c83492d5
  Args:
    source: Catharina-Amalia
    type: :Woman
  AssignClass (21b39583-0022-46c9-80eb-8e9836236109)
 Call ID: 21b39583-0022-46c9-80eb-8e9836236109
  Args:
    type: :Person
    source: Catharina-Amalia
  AddLiteral (41a368e7-7ead-4bf8-8aea-61206e793fc5)
 Call ID: 41a368e7-7ead-4bf8-8aea-61206e793fc5
  Args:
    literal_type: xsd:integer
    source: Catharina-Amalia
    literal_value: 2003
    relation: :hasBirthYear
  AssignClass (86c7d980-d4a9-4e29-a817-3bc8aa215521)
 Call ID: 86c7d980-d4a9-4e29-a817-3bc8aa215521
  Args:
    source: Willem-Alexander
    type: :Man
  AssignClass (de18db86-fa19-430e-92dc-ac4b7ab56d1a)
 Call ID: de18db86-fa19-430e-92dc-ac4b7ab56d1a
  Args:
    type: :Person
    source: Willem-Alexander
  AssignClass (7bf27c41-f99a-4be2-90d8-20e8f189c1dc)
 Call ID: 7bf27c41-f99a-4be2-90d8-20e8f189c1dc
  Args:
    source: Máxima
    type: :Woman
  AssignClass (566886b3-b113-4957-9d66-5c52eaf5f54c)
 Call ID: 566886b3-b113-4957-9d66-5c52eaf5f54c
  Args:
    type: :Person
    source: Máxima
  AddTriple (0da798a4-22f4-42cf-aa19-69c745fae245)
 Call ID: 0da798a4-22f4-42cf-aa19-69c745fae245
  Args:
    relation: :hasFather
    target: Willem-Alexander
    source: Catharina-Amalia
  AddTriple (90e2cceb-e83b-4f7b-92d4-83bba3bde7ba)
 Call ID: 90e2cceb-e83b-4f7b-92d4-83bba3bde7ba
  Args:
    source: Catharina-Amalia
    target: Máxima
    relation: :hasMother
  AssignClass (2b9f6412-b5e6-48e5-bd7e-40dcd7f1089e)
 Call ID: 2b9f6412-b5e6-48e5-bd7e-40dcd7f1089e
  Args:
    type: :Woman
    source: Alexia
  AssignClass (a382ff8d-3750-457b-99b8-4b609b505e25)
 Call ID: a382ff8d-3750-457b-99b8-4b609b505e25
  Args:
    source: Alexia
    type: :Person
  AssignClass (90267e55-c256-488b-8ea5-f87621802355)
 Call ID: 90267e55-c256-488b-8ea5-f87621802355
  Args:
    type: :Woman
    source: Ariane
  AssignClass (0a122115-59ee-4f46-9298-7c6f44a2d8d7)
 Call ID: 0a122115-59ee-4f46-9298-7c6f44a2d8d7
  Args:
    source: Ariane
    type: :Person
  AddTriple (010eb67b-60dc-41af-ad63-ddb6403ba5ec)
 Call ID: 010eb67b-60dc-41af-ad63-ddb6403ba5ec
  Args:
    target: Catharina-Amalia
    source: Alexia
    relation: :isSisterOf
  AddTriple (7ea604a8-286b-4d56-b227-8c0fa42c0eb0)
 Call ID: 7ea604a8-286b-4d56-b227-8c0fa42c0eb0
  Args:
    target: Catharina-Amalia
    source: Ariane
    relation: :isSisterOf
  AddTriple (e3494308-7c0a-4e64-a58c-14c989cdbefc)
 Call ID: e3494308-7c0a-4e64-a58c-14c989cdbefc
  Args:
    relation: :hasFather
    target: Willem-Alexander
    source: Alexia
  AddTriple (62f4b290-b721-4923-aee7-d1a35a99fd48)
 Call ID: 62f4b290-b721-4923-aee7-d1a35a99fd48
  Args:
    target: Máxima
    source: Alexia
    relation: :hasMother
  AddTriple (96102351-6920-4ffb-adfb-9248f2a1bd74)
 Call ID: 96102351-6920-4ffb-adfb-9248f2a1bd74
  Args:
    relation: :hasFather
    target: Willem-Alexander
    source: Ariane
  AddTriple (9f9c3811-5af8-423f-a980-6c9d80034891)
 Call ID: 9f9c3811-5af8-423f-a980-6c9d80034891
  Args:
    source: Ariane
    target: Máxima
    relation: :hasMother
  AssignClass (e903275a-8ab4-4f0d-8559-86a56f7567cf)
 Call ID: e903275a-8ab4-4f0d-8559-86a56f7567cf
  Args:
    source: Beatrix
    type: :Woman
  AssignClass (d095ddfc-231d-4752-8aa6-bb6516de8d03)
 Call ID: d095ddfc-231d-4752-8aa6-bb6516de8d03
  Args:
    type: :Person
    source: Beatrix
  AddTriple (101b6886-5f96-43e4-872b-a9e2d192ba2e)
 Call ID: 101b6886-5f96-43e4-872b-a9e2d192ba2e
  Args:
    relation: :hasMother
    target: Beatrix
    source: Willem-Alexander
  AssignClass (88cfcb72-9366-4ee9-8f8c-f8454c9cca97)
 Call ID: 88cfcb72-9366-4ee9-8f8c-f8454c9cca97
  Args:
    type: :Man
    source: Jorge_Zorreguieta
  AssignClass (e97f55ef-b503-475e-b1b3-b9df2d4d9e9b)
 Call ID: e97f55ef-b503-475e-b1b3-b9df2d4d9e9b
  Args:
    type: :Person
    source: Jorge_Zorreguieta
  AssignClass (6b821ae3-8812-4279-a4cb-f23246affeb3)
 Call ID: 6b821ae3-8812-4279-a4cb-f23246affeb3
  Args:
    source: María_del_Carmen_Cerruti
    type: :Woman
  AssignClass (4fd68fa8-730d-4f4b-8762-4520d0854d90)
 Call ID: 4fd68fa8-730d-4f4b-8762-4520d0854d90
  Args:
    source: María_del_Carmen_Cerruti
    type: :Person
  AddTriple (b466902e-9996-481e-bf12-1800f06a402b)
 Call ID: b466902e-9996-481e-bf12-1800f06a402b
  Args:
    relation: :hasFather
    source: Máxima
    target: Jorge_Zorreguieta
  AddTriple (3c79d9cf-b0d4-4376-849a-3e95ed343352)
 Call ID: 3c79d9cf-b0d4-4376-849a-3e95ed343352
  Args:
    relation: :hasMother
    source: Máxima
    target: María_del_Carmen_Cerruti
  AssignClass (454d19d0-8804-4b8b-818b-bc7ce245758f)
 Call ID: 454d19d0-8804-4b8b-818b-bc7ce245758f
  Args:
    source: Constantijn
    type: :Man
  AssignClass (284cb2b2-5372-4946-adc4-7849adc70762)
 Call ID: 284cb2b2-5372-4946-adc4-7849adc70762
  Args:
    type: :Person
    source: Constantijn
  AddTriple (091362e1-3299-4596-b436-99e9be6513d8)
 Call ID: 091362e1-3299-4596-b436-99e9be6513d8
  Args:
    relation: :hasMother
    target: Beatrix
    source: Constantijn
  AssignClass (4b5bbbf4-4a35-4141-bb8c-a094d3aebcfe)
 Call ID: 4b5bbbf4-4a35-4141-bb8c-a094d3aebcfe
  Args:
    source: Martín_Zorreguieta
    type: :Man
  AssignClass (6c878e8f-f9d3-4caf-b364-2a13d9ced5e1)
 Call ID: 6c878e8f-f9d3-4caf-b364-2a13d9ced5e1
  Args:
    type: :Person
    source: Martín_Zorreguieta
  AddTriple (40360d54-b9fc-4d44-981b-d3d52f3c7e7c)
 Call ID: 40360d54-b9fc-4d44-981b-d3d52f3c7e7c
  Args:
    target: Jorge_Zorreguieta
    source: Martín_Zorreguieta
    relation: :hasFather
  AddTriple (f22e7596-0131-40b2-af53-7ea9abc66802)
 Call ID: f22e7596-0131-40b2-af53-7ea9abc66802
  Args:
    source: Martín_Zorreguieta
    target: María_del_Carmen_Cerruti
    relation: :hasMother
  Finish (d978183e-b5c2-417d-b4ee-d5722153dc79)
 Call ID: d978183e-b5c2-417d-b4ee-d5722153dc79
  Args: