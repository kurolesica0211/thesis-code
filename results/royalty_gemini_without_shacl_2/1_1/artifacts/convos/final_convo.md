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


Frederik X (Frederik André Henrik Christian, .mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}pronounced ; born 26
May 1968) is King of Denmark, reigning since the abdication of his mother, Margrethe II, in January 2024.
Frederik is the elder son of Queen Margrethe II and Prince Henrik.
He was born during the reign of his maternal grandfather, King Frederik IX, and became Crown Prince of Denmark following his mother's accession in 1972.
Frederik met Australian marketing consultant Mary Donaldson while attending the 2000 Summer Olympics in Sydney.
Early life and education

Frederik was born at 23:50 on 26 May 1968 by emergency caesarean section at Rigshospitalet, the Copenhagen University Hospital in Copenhagen, to the then Princess Margrethe (later Queen Margrethe II), oldest daughter of King Frederik IX and heir presumptive to the Danish throne, and Prince Henrik.
At the time of his birth, his maternal grandfather was on the throne of Denmark, his maternal uncle-by-marriage Constantine II was king of Greece and his matrilineal great-grandfather, Gustaf VI Adolf, was on the throne of Sweden.
He was named Frederik after his maternal grandfather, King Frederik IX, continuing the Danish royal tradition of the heir apparent being named either Frederik or Christian.
He became Crown Prince of Denmark when his mother ascended the throne on 14 January 1972.
Frederik's only sibling is Prince Joachim of Denmark.
Frederik attended primary school at Krebs' Skole between 1974 and 1981, as a private pupil at Amalienborg Palace from 1974 to 1976, and from the third form again at Krebs' Skole.
In 1986, Frederik graduated from Øregård Gymnasium.
In the autumn of 1989, Frederik began studying political science at Aarhus University.
As part of his education, he spent the 1992–1993 academic year at Harvard University, where he studied political science under the name Frederik Henriksen.
Frederik is the first Danish royal to complete a university education.
Early career

Frederik took up a position for three months with the Danish UN mission in New York in 1994.
The prince was posted as First Secretary to the Danish Embassy in Paris from October 1998 to October 1999.
Military service

Frederik has completed extensive military studies and training in all three services, including training as a frogman in the naval elite special operations forces Frømandskorpset.
Frederik remained active in the defence services, and in the period 2002–2003 served as a staff officer at Defence Command Denmark, and from 2003 as a senior lecturer with the Institute of Strategy at the Royal Danish Defence College.
By his appointment, Frederik has the same grade as the Danish Chief of Defence.
Marriage and children

During a Council of State on 8 October 2003, Queen Margrethe gave her consent to the marriage of Crown Prince Frederik to Mary Elizabeth Donaldson, an Australian marketing consultant whom the prince had met while attending the Sydney Olympics in 2000.
Reign

Queen Margrethe II announced her abdication during her annual live broadcast New Year's Eve address on 31 December 2023.
Frederik succeeded her as King of Denmark on 14 January 2024, after Margrethe formally signed an instrument of abdication during a meeting of the Council of State.
His motto is Forbundne, forpligtet, for Kongeriget Danmark (English: "United, committed, for the Kingdom of Denmark"), the first motto that does not mention God since Frederik VII.
On 21 January, the royal family attended a celebratory church service at Aarhus Cathedral, led by the Bishop of Aarhus and Royal Chaplain-in-Ordinary, Henrik Wigh-Poulsen.
On 31 January 2024, Frederik visited Poland and was received by its president Andrzej Duda, in his first overseas trip as monarch.
Danish monarchs traditionally travel first to another Scandinavian country, but Frederik had planned the trip prior to Margrethe's abdication.
The King and Queen made their first state visits in May 2024, visiting Sweden and Norway.
In June, they toured Greenland, one of the autonomous territories of the Kingdom of Denmark.
In November 2024 the Royal Court announced that the King had decided to phase out the system of granting companies royal warrants, which has been extant in Denmark since the 19th century.
In January 2025, when U.S president elect Donald Trump renewed talks about the intended U.S purchase of Greenland, the King made a speech promoting unity and collaboration within the Kingdom of Denmark.
State visits

Personal interests

Scientific research, climate change and sustainability

Frederik has a special interest in scientific research, climate change, and sustainability.
The prince has represented Denmark as a promoter of sustainable Danish energy.
The prince was one of the authors of the Kongelig Polartokt (Polar Cruise Royal), about the challenges of climate, published in 2009 with a preface written by Kofi Annan.
Frederik is an avid sportsman, running marathons in Copenhagen, New York, and Paris, and completing the 42 kilometers with a respectable time of 3 hours, 22 minutes and 50 seconds in the Copenhagen Marathon.
Frederik is a keen sailor, being an accomplished Farr 40 and International Dragon skipper.
At the 2003 Dragon European Championship, where 51 boats participated, the Prince and his crew had been leading after four out of six races; they finished in fourth place.
At the 2008 Farr 40 World Championship with 33 boats participating, Frederik and his crew also took fourth place.
Helming the Swan 60 yacht Emma, he won its IRC category in the 2010 Fyn Cup in Denmark, and was fourth in the 2011 Danish Dragon Championship with Nanoq.
In 2016, on the subject of the Olympics in Rio, Frederik told the press that he did not regret not chasing his dream to compete in the Olympics after meeting his wife.
In October 2016, Frederik had to cancel his appearance at the royal reception for the Danish Olympic and Paralympic athletes after he fractured his spine while jumping on a trampoline with his eldest son.
Frederik took part in the relay event during the 2019 IAAF World Cross Country Championships in Aarhus in March 2019.
Frederik has competed in cross-country skiing; he skied the 90 km (56 mi) Swedish Vasaloppet, the oldest cross-country ski race in the world, in 2012, 2013, 2014, and 2015.
In 2016, he completed the 54 kilometres (34 mi) Norwegian Birkebeinerrennet with Norway's Crown Prince Haakon.
Also in 2016, Frederik completed the 160 km (99 mi) Arctic Circle Race  in Sisimiut, Greenland.
International Olympic Committee

On 9 October 2009, Crown Prince Frederik was elected a member of the International Olympic Committee, replacing former Danish member Kaj Holm, who had reached the age of retirement.
The Crown Prince's candidature was met with some skepticism in Denmark, as it would mean that the Crown Prince would be on a semi-political committee along with several people who are suspected or even convicted of criminal acts.
Another concern was whether or not the Crown Prince's loyalty would be towards his country and government, as the Danish constitution prescribes, or with the International Olympic Committee, as is sworn upon election to the committee.
The Crown Prince was given special observer status in National Olympic Committee and Sports Confederation of Denmark, as a way to allow him to work, without having political power.
Frederik announced that his point of focus and reason for joining the International Olympic Committee is to promote an active lifestyle among youth.
In 2012, Frederik carried the Olympic flame through Notting Hill, a neighbourhood in West London.
In 2016, Frederik faced criticism for voting against Danish Minister for Culture Bertel Haarder and a majority in the Danish Parliament's wishes on the subject of whether or not Russia should be allowed to compete at the 2016 Summer Olympics following allegations of state-sponsored doping.
On 19 June 2017, the Crown Prince announced that he would continue another term of 8 years.
However, in 2021, Frederik was announced that he would step down as an active member of the International Olympic Committee at the committee's annual session prior to the 2020 Summer Olympics, citing a wish to intensify his everyday work as the reason for stepping down in the middle of his term.
Royal Run

In celebration of his 50th birthday, on 21 May 2018, Frederik initiated a public running event across five cities in Denmark called Royal Run  with more than 70,000 participants, including himself and his own family.
The 2020 edition was cancelled due to the COVID-19 situation in Denmark.
Expeditions

The Crown Prince participated in an expedition to Mongolia in 1986.
Prince Frederik was part of the polar expedition as a film photographer, whose job was to ensure an optimal coverage of this event.
Crown Prince Frederik's Foundation

The purpose of the foundation is to provide financial assistance to students of social policy and sciences, for one year's study at Harvard.
Titles, styles, honours and arms

Titles and styles

Frederik was originally styled "His Royal Highness Prince Frederik of Denmark".
On the accession of his mother on 14 January 1972, he became known as "His Royal Highness The Crown Prince of Denmark".



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
  AssignClass (ed3f951e-b580-47b5-b3d4-fd18cdd81a62)
 Call ID: ed3f951e-b580-47b5-b3d4-fd18cdd81a62
  Args:
    type: :Man
    source: :Frederik_X
  AssignClass (b5beec32-caf8-419b-8d9f-9c96cf2c0990)
 Call ID: b5beec32-caf8-419b-8d9f-9c96cf2c0990
  Args:
    type: :Person
    source: :Frederik_X
  AddLiteral (6a673fd0-9b6e-4f3b-9b45-d92a7e814f80)
 Call ID: 6a673fd0-9b6e-4f3b-9b45-d92a7e814f80
  Args:
    source: :Frederik_X
    literal_value: 1968
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (d97ea29e-5810-43dd-b42d-72e9762e0900)
 Call ID: d97ea29e-5810-43dd-b42d-72e9762e0900
  Args:
    type: :Woman
    source: :Margrethe_II
  AssignClass (9bd575b9-d61a-43ef-a4d9-d0c51f46d92c)
 Call ID: 9bd575b9-d61a-43ef-a4d9-d0c51f46d92c
  Args:
    type: :Person
    source: :Margrethe_II
  AssignClass (94e6eea3-b446-46ca-801a-b938b8288bed)
 Call ID: 94e6eea3-b446-46ca-801a-b938b8288bed
  Args:
    type: :Man
    source: :Prince_Henrik
  AssignClass (ddddfb45-9bf0-44a8-9a0f-dde75bf94eab)
 Call ID: ddddfb45-9bf0-44a8-9a0f-dde75bf94eab
  Args:
    type: :Person
    source: :Prince_Henrik
  AddTriple (e15781b0-e673-4c71-86bb-bd89f90ed62b)
 Call ID: e15781b0-e673-4c71-86bb-bd89f90ed62b
  Args:
    source: :Frederik_X
    target: :Prince_Henrik
    relation: :hasFather
  AddTriple (be2d6a18-dbca-4943-bbe4-ea6cd2583603)
 Call ID: be2d6a18-dbca-4943-bbe4-ea6cd2583603
  Args:
    source: :Frederik_X
    target: :Margrethe_II
    relation: :hasMother
  AssignClass (c270b606-e418-4bdd-b2d2-bd323aaeb1dd)
 Call ID: c270b606-e418-4bdd-b2d2-bd323aaeb1dd
  Args:
    type: :Man
    source: :Frederik_IX
  AssignClass (54b78f55-311e-47a5-9b94-8db9c8458e15)
 Call ID: 54b78f55-311e-47a5-9b94-8db9c8458e15
  Args:
    type: :Person
    source: :Frederik_IX
  AddTriple (03e80f9a-1ef3-4606-98b6-0fbea647498d)
 Call ID: 03e80f9a-1ef3-4606-98b6-0fbea647498d
  Args:
    relation: :hasFather
    source: :Margrethe_II
    target: :Frederik_IX
  AssignClass (150f40e8-f905-4d3d-b6fc-b200ff0e85c0)
 Call ID: 150f40e8-f905-4d3d-b6fc-b200ff0e85c0
  Args:
    type: :Man
    source: :Prince_Joachim
  AssignClass (a02873cc-9657-46e3-90f4-9d7f235574f1)
 Call ID: a02873cc-9657-46e3-90f4-9d7f235574f1
  Args:
    type: :Person
    source: :Prince_Joachim
  AddTriple (cde430a3-088f-408c-896c-b11f075f8fda)
 Call ID: cde430a3-088f-408c-896c-b11f075f8fda
  Args:
    source: :Prince_Joachim
    target: :Frederik_X
    relation: :isBrotherOf
  AssignClass (d2c4d07c-a591-45a9-8ecf-06a67c9c2c56)
 Call ID: d2c4d07c-a591-45a9-8ecf-06a67c9c2c56
  Args:
    type: :Woman
    source: :Mary_Elizabeth_Donaldson
  AssignClass (c30e34d5-381d-4a3f-83c8-09b1ede1664d)
 Call ID: c30e34d5-381d-4a3f-83c8-09b1ede1664d
  Args:
    type: :Person
    source: :Mary_Elizabeth_Donaldson
  AssignClass (3ea40fc8-70b5-4156-9c97-17ebca92f647)
 Call ID: 3ea40fc8-70b5-4156-9c97-17ebca92f647
  Args:
    type: :Man
    source: :Constantine_II
  AssignClass (bb87f523-6731-4e4e-89cb-cb96307ac5c0)
 Call ID: bb87f523-6731-4e4e-89cb-cb96307ac5c0
  Args:
    type: :Person
    source: :Constantine_II
  AssignClass (6ed70945-3faf-48e0-aa7e-46d4cfc23cb2)
 Call ID: 6ed70945-3faf-48e0-aa7e-46d4cfc23cb2
  Args:
    type: :Man
    source: :Gustaf_VI_Adolf
  AssignClass (0b7efdc2-5a71-489c-b4ef-cfddeae36077)
 Call ID: 0b7efdc2-5a71-489c-b4ef-cfddeae36077
  Args:
    type: :Person
    source: :Gustaf_VI_Adolf
  Finish (49b35edd-46b5-4f9a-acd9-dae53d853af0)
 Call ID: 49b35edd-46b5-4f9a-acd9-dae53d853af0
  Args: