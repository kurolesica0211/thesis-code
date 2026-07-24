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
Ferdinand Habsburg-Lothringen  (given names: Ferdinand Zvonimir Maria Balthus Keith Michael Otto Antal Bahnam Leonhard; born 21 June 1997) is an Austrian motor racing driver and heir apparent to the headship of the House of Habsburg-Lorraine.
Early life and family

Ferdinand Habsburg was born on 21 June 1997 to Karl von Habsburg and Francesca von Thyssen-Bornemisza.
A member of the House of Habsburg, his paternal grandparents were Otto von Habsburg, the last crown prince of Austria-Hungary, and Princess Regina of Saxe-Meiningen.
His maternal grandparents are Baron Hans Heinrich Thyssen-Bornemisza and Fiona Campbell-Walter, descendant of the Campbell baronets of Airds – his cousin, Jamie Campbell-Walter, is also a racing driver and doubles as Habsburg's manager.
Habsburg was baptised on 20 September 1997 in Zagreb by Cardinal Franjo Kuharić.
His godparents were his uncle Georg von Habsburg; Alois-Konstantin, 9th Prince of Löwenstein-Wertheim-Rosenberg; Queen Margarita of Bulgaria; and Agnes Husslein (born Countess Agnes von Arco).
He was also given the traditional Croatian name Zvonimir.
Habsburg is the brother of Eleonore von Habsburg and Gloria von Habsburg.
former driver Jérôme d'Ambrosio.


Habsburg is the heir apparent to the headship of the House of Habsburg-Lorraine, held by his father on 1 January 2007.
His titles and honorifics are unofficial as Austria is a republic with all royal titles being legally abolished in 1918.
Early career

Karting

Habsburg began his racing career at the age of 14 with the Austrian team Speedworld Academy.
Formula Renault 1.6 NEC

In 2014, Habsburg made his début in single seaters, taking part in the Formula Renault 1.6 NEC Championship with Lechner Racing.
Toyota Racing Series

For 2015, Habsburg contested New Zealand's Toyota Racing Series in January and February 2015 with Victory Motor Racing, finishing 11th in the championship and fifth in the rookie class with two podium finishes.
Habsburg contested his final season in the series in 2017, this time driving for M2 Competition.
Formula Renault 2.0 NEC

For 2015, Habsburg decided to switch to the Formula Renault Northern European Cup with Fortec Motorsports.
Euroformula Open Championship

Habsburg made his debut in the Euroformula Open Championship in the 2015 season finale at the Circuit de Barcelona-Catalunya, where he finished both races in the top ten.
The following year, Habsburg committed to the series full-time, racing for Drivex School.
Having lost ground to the more experienced title-favourite Leonardo Pulcini during the first few rounds, Habsburg was able to achieve his first race win in the series at the Circuit Paul Ricard.
FIA Formula 3 European Championship

2017

For 2017, Habsburg stepped up to the FIA European F3 Championship, racing for Carlin.
On the final lap, Habsburg took the lead around the outside of the final corner at Fisherman's Bend, but braked too late and understeered into the barriers on the exit of the corner, with Sette Câmara doing exactly the same thing, handing the race win to Câmara's teammate Dan Ticktum.
Habsburg eventually limped across the line fourth despite broken front suspension.
2018

Habsburg returned to the series in 2018 with Carlin, this time partnering Jehan Daruvala, Sacha Fenestraz, Nikita Troitskiy and Ameya Vaidyanathan.
However, Habsburg was unable to find the form from the previous year, scoring just a lone podium at Misano and finishing 13th in the championship.
Sportscar career

Deutsche Tourenwagen Masters

2019

In 2019, Habsburg signed for R-Motorsport II to race the Aston Martin Vantage DTM in the Deutsche Tourenwagen Masters.
2020

For the 2020 season, Habsburg made the switch to Audi Sport Team WRT racing the Audi RS5 Turbo DTM.
This season was comparatively successful for Habsburg as he secured ten points positions, one of which was a podium in Circuit Zolder.
This meant that Habsburg finished tenth in the driver's championship with 68 points, beating both of his teammates Fabio Scherer and Harrison Newey.
, Habsburg competed in the 24 Hours of Le Mans Virtual with Mahle Racing, driving the 2018 Aston Martin Vantage GTE alongside former IndyCar Series driver Robert Wickens and sim-racers Jimmy Broadbent and Kevin Rotting.
Endurance racing

2021

Habsburg started his 2021 campaign by racing in the Asian Le Mans Series with G-Drive Racing.
Alongside this, Habsburg raced with High Class Racing in the 2021 24 Hours of Daytona alongside Robert Kubica, Dennis Andersen, and Anders Fjordbach.
On 26 February, it was confirmed Habsburg would compete in the FIA World Endurance Championship for Team WRT alongside Robin Frijns and Charles Milesi, driving an Oreca 07 in the LMP2 class.
During the first round in the 6 Hours of Spa-Francorchamps, Habsburg and his team finished tenth and in the following race, the 8 Hours of Portimão, his team finished in fourth position.
However, it was in the next race, the 6 Hours of Monza that Habsburg clinched his first LMP2 podium, finishing in second place.
In round four, that being the 24 Hours of Le Mans, Habsburg and his Team WRT teammates clinched a dramatic LMP2 class win after their sister Team WRT car suffered a throttle Sensor failure on the final lap whilst in the lead of the race.
The following weekend, Habsburg, Frijns and Milesi clinched the LMP2 title after scoring a third consecutive victory in the series at the 8-hour race at the same venue.
Habsburg also became the first Austrian to win the LMP2 title in the World Endurance Championship.
The following year, Habsburg returned to the WEC, driving the No. 41 car for RealTeam by WRT with Rui Andrade and Norman Nato.
Parallel to his WEC campaign, Habsburg competed for Prema Racing in the European Le Mans Series.
The team started the season in controlling fashion, winning the season opener at Paul Ricard, after which Habsburg described himself as "honoured", and taking victory in Imola despite Lorenzo Colombo having to serve two drive-through penalties for a pair of separate infringements.
After a fifth place in Monza, Habsburg and his teammates Colombo and Louis Delétraz took yet another victory at Barcelona to extend their championship advantage.
Another podium came in the penultimate race at Spa, before the team clinched the title with a victory at the finale in Portimão, meaning that Habsburg and Delétraz claimed the ELMS drivers' title.
2023

Habsburg remained with Team WRT for the 2023 WEC season, this time partnering Sean Gelael and reuniting with Robin Frijns.
2024

For the 2024 season, Habsburg stepped up to the top class in the WEC, joining the Alpine Endurance Team to drive an Alpine A424.
Habsburg competed in the first round, the Qatar 1812 km, finishing eighth.
As von Habsburg was a guest driver, he was ineligible to score championship points.
As Habsburg was a guest driver, he was ineligible for points.
Complete Formula Renault 2.0 NEC results

(key) (Races in bold indicate pole position) (Races in italics indicate fastest lap)


Complete Euroformula Open Championship results

(key) (Races in bold indicate pole position; races in italics indicate points for the fastest lap of top ten finishers)


† As von Habsburg was a guest driver, he was ineligible to score championship points.
Complete 24 Hours of Le Mans results

Dynastic activities

In 2011, Ferdinand attended the Requiem Mass in Vienna's St. Stephen's Cathedral of his grandfather, Otto von Habsburg, former head of the House of Habsburg, former Crown Prince and by pretense, Emperor-King of Austria-Hungary.
On 28 June 2014, Austrian royal family members including Ferdinand and more than 120 direct descendants of Archduke Franz Ferdinand gathered in Lower Austria to mark the 100th anniversary of his death.
The heir to the house of Austria received the knighthood from his father, Archduke Karl, Grand Master.
The history of the order goes back many centuries, created by Rudolph, Count of Habsburg who reigned as Emperor of the Holy Roman Empire from 1273-1291.
In 2022, Ferdinand with his family observed the 100th anniversary of the death of Charles I of Austria.



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
  AssignClass (520b7768-961c-42fa-9c03-d3ba56de3672)
 Call ID: 520b7768-961c-42fa-9c03-d3ba56de3672
  Args:
    type: :Person
    source: Ferdinand Habsburg-Lothringen
  AssignClass (2e745526-7ec8-4437-b8c7-4fd6fb4b6d0f)
 Call ID: 2e745526-7ec8-4437-b8c7-4fd6fb4b6d0f
  Args:
    source: Ferdinand Habsburg-Lothringen
    type: :Man
  AddLiteral (8555295c-2e05-4001-a330-c58a6799320e)
 Call ID: 8555295c-2e05-4001-a330-c58a6799320e
  Args:
    source: Ferdinand Habsburg-Lothringen
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1997
  AssignClass (a33fb510-a526-4324-8bb3-013bf8c9d3b1)
 Call ID: a33fb510-a526-4324-8bb3-013bf8c9d3b1
  Args:
    source: Karl von Habsburg
    type: :Person
  AssignClass (53eda0ab-b446-4a0b-83ab-f2321ae612e9)
 Call ID: 53eda0ab-b446-4a0b-83ab-f2321ae612e9
  Args:
    source: Karl von Habsburg
    type: :Man
  AssignClass (2de44530-fb09-40bd-9400-2be143ff0da2)
 Call ID: 2de44530-fb09-40bd-9400-2be143ff0da2
  Args:
    source: Francesca von Thyssen-Bornemisza
    type: :Person
  AssignClass (1073ebe1-2bda-42eb-a657-494fceed217b)
 Call ID: 1073ebe1-2bda-42eb-a657-494fceed217b
  Args:
    source: Francesca von Thyssen-Bornemisza
    type: :Woman
  AddTriple (eb71ec6f-a295-4d5f-9b35-7ac981fc58f2)
 Call ID: eb71ec6f-a295-4d5f-9b35-7ac981fc58f2
  Args:
    source: Ferdinand Habsburg-Lothringen
    relation: :hasFather
    target: Karl von Habsburg
  AddTriple (bf080686-513b-45a3-afdb-5b3c71a330a4)
 Call ID: bf080686-513b-45a3-afdb-5b3c71a330a4
  Args:
    source: Ferdinand Habsburg-Lothringen
    relation: :hasMother
    target: Francesca von Thyssen-Bornemisza
  AssignClass (bfebaee6-5a59-4b5f-8f26-c096f64e5c7d)
 Call ID: bfebaee6-5a59-4b5f-8f26-c096f64e5c7d
  Args:
    type: :Person
    source: Otto von Habsburg
  AssignClass (8f6f945d-5278-4512-8ed8-bff45c8aa8c6)
 Call ID: 8f6f945d-5278-4512-8ed8-bff45c8aa8c6
  Args:
    type: :Man
    source: Otto von Habsburg
  AssignClass (5121cf7b-5a25-4c77-ab44-e0d73d531f78)
 Call ID: 5121cf7b-5a25-4c77-ab44-e0d73d531f78
  Args:
    type: :Person
    source: Princess Regina of Saxe-Meiningen
  AssignClass (23482415-3bab-444a-9b80-28ae67cdb34c)
 Call ID: 23482415-3bab-444a-9b80-28ae67cdb34c
  Args:
    type: :Woman
    source: Princess Regina of Saxe-Meiningen
  AddTriple (68c5d5d3-7267-45dd-845a-0ab533ade948)
 Call ID: 68c5d5d3-7267-45dd-845a-0ab533ade948
  Args:
    source: Karl von Habsburg
    relation: :hasFather
    target: Otto von Habsburg
  AddTriple (88ca8cc9-cc09-4028-a381-0b142360fdf9)
 Call ID: 88ca8cc9-cc09-4028-a381-0b142360fdf9
  Args:
    target: Princess Regina of Saxe-Meiningen
    relation: :hasMother
    source: Karl von Habsburg
  AssignClass (f25d83bb-c2c7-4cd0-8af6-9fbdfd7bc9d8)
 Call ID: f25d83bb-c2c7-4cd0-8af6-9fbdfd7bc9d8
  Args:
    source: Baron Hans Heinrich Thyssen-Bornemisza
    type: :Person
  AssignClass (6a1f7a57-e1ae-4d4c-9f32-aa335bea3793)
 Call ID: 6a1f7a57-e1ae-4d4c-9f32-aa335bea3793
  Args:
    source: Baron Hans Heinrich Thyssen-Bornemisza
    type: :Man
  AssignClass (f24eabcc-3d72-4b99-85ac-367fed97cfe6)
 Call ID: f24eabcc-3d72-4b99-85ac-367fed97cfe6
  Args:
    source: Fiona Campbell-Walter
    type: :Person
  AssignClass (12b229d6-b92f-4ebb-a995-c7881c34fba8)
 Call ID: 12b229d6-b92f-4ebb-a995-c7881c34fba8
  Args:
    type: :Woman
    source: Fiona Campbell-Walter
  AddTriple (f5481d0e-9c42-4b64-9f60-61646aed7320)
 Call ID: f5481d0e-9c42-4b64-9f60-61646aed7320
  Args:
    target: Baron Hans Heinrich Thyssen-Bornemisza
    relation: :hasFather
    source: Francesca von Thyssen-Bornemisza
  AddTriple (bf7e4024-d9a7-413d-aaa4-9f2014bc5e96)
 Call ID: bf7e4024-d9a7-413d-aaa4-9f2014bc5e96
  Args:
    source: Francesca von Thyssen-Bornemisza
    relation: :hasMother
    target: Fiona Campbell-Walter
  AssignClass (64195b88-a6ea-4ef3-b352-e0608574e1be)
 Call ID: 64195b88-a6ea-4ef3-b352-e0608574e1be
  Args:
    source: Eleonore von Habsburg
    type: :Person
  AssignClass (4a40f8a4-7edc-457f-a1cf-4dfec12cc474)
 Call ID: 4a40f8a4-7edc-457f-a1cf-4dfec12cc474
  Args:
    type: :Woman
    source: Eleonore von Habsburg
  AssignClass (4c2f3dc8-b0d6-4bff-9fd0-0320ec5eccbd)
 Call ID: 4c2f3dc8-b0d6-4bff-9fd0-0320ec5eccbd
  Args:
    source: Gloria von Habsburg
    type: :Person
  AssignClass (26c80916-24f7-463b-a043-a510cd6b66a3)
 Call ID: 26c80916-24f7-463b-a043-a510cd6b66a3
  Args:
    type: :Woman
    source: Gloria von Habsburg
  AddTriple (0d1cf2db-c23f-4b59-91ed-713987090466)
 Call ID: 0d1cf2db-c23f-4b59-91ed-713987090466
  Args:
    relation: :isSiblingOf
    source: Ferdinand Habsburg-Lothringen
    target: Eleonore von Habsburg
  AddTriple (31b4c6aa-4c8a-4e96-bb51-2070765b587f)
 Call ID: 31b4c6aa-4c8a-4e96-bb51-2070765b587f
  Args:
    target: Gloria von Habsburg
    relation: :isSiblingOf
    source: Ferdinand Habsburg-Lothringen
  AssignClass (d69d4b2d-e4cf-4fd6-b89e-268ff5ef9974)
 Call ID: d69d4b2d-e4cf-4fd6-b89e-268ff5ef9974
  Args:
    source: Georg von Habsburg
    type: :Person
  AssignClass (d332901b-c740-4f21-b560-7f9fef74f127)
 Call ID: d332901b-c740-4f21-b560-7f9fef74f127
  Args:
    type: :Man
    source: Georg von Habsburg
  AddTriple (747f9fa6-533a-4467-b21d-213b27b80d7f)
 Call ID: 747f9fa6-533a-4467-b21d-213b27b80d7f
  Args:
    relation: :hasBrother
    source: Karl von Habsburg
    target: Georg von Habsburg
  Finish (4e59e6f9-ebe4-467a-ba8e-fef65070e451)
 Call ID: 4e59e6f9-ebe4-467a-ba8e-fef65070e451
  Args: