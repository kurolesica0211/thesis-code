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
  AssignClass (5c7cdd9a-8129-4d04-98e8-94b448aae4d7)
 Call ID: 5c7cdd9a-8129-4d04-98e8-94b448aae4d7
  Args:
    source: Ferdinand Habsburg-Lothringen
    type: :Man
  AssignClass (fb887fa0-95a4-48a4-8d22-d85d2496810a)
 Call ID: fb887fa0-95a4-48a4-8d22-d85d2496810a
  Args:
    source: Ferdinand Habsburg-Lothringen
    type: :Person
  AddLiteral (c5af59e1-3727-4508-8bd4-d2374696736b)
 Call ID: c5af59e1-3727-4508-8bd4-d2374696736b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Ferdinand Habsburg-Lothringen
    literal_value: 1997
  AssignClass (593ecae0-57c1-4391-a370-e9dce9ae3c64)
 Call ID: 593ecae0-57c1-4391-a370-e9dce9ae3c64
  Args:
    type: :Man
    source: Karl von Habsburg
  AssignClass (72c72444-b5da-4326-88c2-ca08905ded08)
 Call ID: 72c72444-b5da-4326-88c2-ca08905ded08
  Args:
    type: :Person
    source: Karl von Habsburg
  AssignClass (ea6148e5-fe38-418e-90bf-0be239f2abda)
 Call ID: ea6148e5-fe38-418e-90bf-0be239f2abda
  Args:
    type: :Woman
    source: Francesca von Thyssen-Bornemisza
  AssignClass (86650e22-2495-4ae4-ab59-ca89fd396ed5)
 Call ID: 86650e22-2495-4ae4-ab59-ca89fd396ed5
  Args:
    source: Francesca von Thyssen-Bornemisza
    type: :Person
  AddTriple (458db4c6-2efe-4217-9786-6678567d5cbd)
 Call ID: 458db4c6-2efe-4217-9786-6678567d5cbd
  Args:
    relation: :hasFather
    source: Ferdinand Habsburg-Lothringen
    target: Karl von Habsburg
  AddTriple (4112f0e9-a5a9-454a-b020-d17cb21773e5)
 Call ID: 4112f0e9-a5a9-454a-b020-d17cb21773e5
  Args:
    relation: :hasMother
    source: Ferdinand Habsburg-Lothringen
    target: Francesca von Thyssen-Bornemisza
  AssignClass (600335ac-3d91-41e8-bd1d-46330732ddf9)
 Call ID: 600335ac-3d91-41e8-bd1d-46330732ddf9
  Args:
    type: :Man
    source: Otto von Habsburg
  AssignClass (245214bb-aa5e-4488-bc08-dc9761354d47)
 Call ID: 245214bb-aa5e-4488-bc08-dc9761354d47
  Args:
    type: :Person
    source: Otto von Habsburg
  AssignClass (1f9a94e3-47c9-482e-a7a7-321f0c8bc7cb)
 Call ID: 1f9a94e3-47c9-482e-a7a7-321f0c8bc7cb
  Args:
    type: :Woman
    source: Princess Regina of Saxe-Meiningen
  AssignClass (808f93b7-2bb2-43c9-93df-34eed6b0ccbf)
 Call ID: 808f93b7-2bb2-43c9-93df-34eed6b0ccbf
  Args:
    type: :Person
    source: Princess Regina of Saxe-Meiningen
  AddTriple (9fd9f9f1-259f-4e32-9028-978ad6f32c0c)
 Call ID: 9fd9f9f1-259f-4e32-9028-978ad6f32c0c
  Args:
    relation: :hasFather
    source: Karl von Habsburg
    target: Otto von Habsburg
  AddTriple (f442f6c4-02f5-45a0-ba3b-1245986db31e)
 Call ID: f442f6c4-02f5-45a0-ba3b-1245986db31e
  Args:
    target: Princess Regina of Saxe-Meiningen
    source: Karl von Habsburg
    relation: :hasMother
  AssignClass (b8eaeda6-7670-4b41-a12f-8a33d431e427)
 Call ID: b8eaeda6-7670-4b41-a12f-8a33d431e427
  Args:
    source: Baron Hans Heinrich Thyssen-Bornemisza
    type: :Man
  AssignClass (a143eba5-7889-46e8-9b28-5e181b150cb6)
 Call ID: a143eba5-7889-46e8-9b28-5e181b150cb6
  Args:
    source: Baron Hans Heinrich Thyssen-Bornemisza
    type: :Person
  AssignClass (cd966fe2-be9f-4683-b473-8973468a6e63)
 Call ID: cd966fe2-be9f-4683-b473-8973468a6e63
  Args:
    type: :Woman
    source: Fiona Campbell-Walter
  AssignClass (0f1fff49-50f6-42c7-96ea-52df5d43508e)
 Call ID: 0f1fff49-50f6-42c7-96ea-52df5d43508e
  Args:
    type: :Person
    source: Fiona Campbell-Walter
  AddTriple (8f82e921-72f2-40c7-8e13-7bde989e3d77)
 Call ID: 8f82e921-72f2-40c7-8e13-7bde989e3d77
  Args:
    source: Francesca von Thyssen-Bornemisza
    target: Baron Hans Heinrich Thyssen-Bornemisza
    relation: :hasFather
  AddTriple (4623a60d-5ded-42eb-af7c-4500f26936f4)
 Call ID: 4623a60d-5ded-42eb-af7c-4500f26936f4
  Args:
    relation: :hasMother
    target: Fiona Campbell-Walter
    source: Francesca von Thyssen-Bornemisza
  AssignClass (5025816d-3d57-4a6e-a89e-76ef32d3906c)
 Call ID: 5025816d-3d57-4a6e-a89e-76ef32d3906c
  Args:
    source: Eleonore von Habsburg
    type: :Woman
  AssignClass (5641626d-898c-486d-bffb-1d06d03e1f78)
 Call ID: 5641626d-898c-486d-bffb-1d06d03e1f78
  Args:
    source: Eleonore von Habsburg
    type: :Person
  AssignClass (7368561a-bf4c-47ad-a2b6-d0d28e27338c)
 Call ID: 7368561a-bf4c-47ad-a2b6-d0d28e27338c
  Args:
    source: Gloria von Habsburg
    type: :Woman
  AssignClass (8170d69a-3e40-4ced-94f4-602bf2b164c5)
 Call ID: 8170d69a-3e40-4ced-94f4-602bf2b164c5
  Args:
    source: Gloria von Habsburg
    type: :Person
  AddTriple (e5eabdda-9d2c-4ca9-91e0-2b944fdb036f)
 Call ID: e5eabdda-9d2c-4ca9-91e0-2b944fdb036f
  Args:
    relation: :isSiblingOf
    source: Ferdinand Habsburg-Lothringen
    target: Eleonore von Habsburg
  AddTriple (8fd152bf-b825-4726-88a7-fc15dd97d17a)
 Call ID: 8fd152bf-b825-4726-88a7-fc15dd97d17a
  Args:
    source: Ferdinand Habsburg-Lothringen
    target: Gloria von Habsburg
    relation: :isSiblingOf
  AssignClass (ee14721e-4fc1-4e63-bab8-bf224c7df6c2)
 Call ID: ee14721e-4fc1-4e63-bab8-bf224c7df6c2
  Args:
    source: Georg von Habsburg
    type: :Man
  AssignClass (e600e9b0-ad61-4ed8-8ad5-d56ba4e82e35)
 Call ID: e600e9b0-ad61-4ed8-8ad5-d56ba4e82e35
  Args:
    source: Georg von Habsburg
    type: :Person
  AddTriple (846b5bbf-e040-4cd8-a234-76f52edbea7c)
 Call ID: 846b5bbf-e040-4cd8-a234-76f52edbea7c
  Args:
    target: Karl von Habsburg
    source: Georg von Habsburg
    relation: :isSiblingOf
  Finish (b7b78e1e-edce-46aa-932d-fe248a960ed4)
 Call ID: b7b78e1e-edce-46aa-932d-fe248a960ed4
  Args: