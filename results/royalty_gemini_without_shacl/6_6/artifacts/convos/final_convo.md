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
  AssignClass (297e5294-4879-48b5-b894-b82d1c3db2cf)
 Call ID: 297e5294-4879-48b5-b894-b82d1c3db2cf
  Args:
    type: :Man
    source: :Ferdinand_Habsburg-Lothringen
  AssignClass (50fc06f4-3a62-4fd5-af48-a4ca387b380e)
 Call ID: 50fc06f4-3a62-4fd5-af48-a4ca387b380e
  Args:
    source: :Ferdinand_Habsburg-Lothringen
    type: :Person
  AddLiteral (c59259d9-c122-42d0-b027-24e3dfc5aec0)
 Call ID: c59259d9-c122-42d0-b027-24e3dfc5aec0
  Args:
    literal_value: 1997
    source: :Ferdinand_Habsburg-Lothringen
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b2698433-bb78-4ccc-9fe4-edd349c90e74)
 Call ID: b2698433-bb78-4ccc-9fe4-edd349c90e74
  Args:
    literal_type: xsd:string
    source: :Ferdinand_Habsburg-Lothringen
    literal_value: Ferdinand Zvonimir Maria Balthus Keith Michael Otto Antal Bahnam Leonhard
    relation: :knownAs
  AddLiteral (2b526508-c67b-41bc-9dc4-ff05f3cd409f)
 Call ID: 2b526508-c67b-41bc-9dc4-ff05f3cd409f
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Ferdinand_Habsburg-Lothringen
    literal_value: Zvonimir
  AssignClass (f7072d0c-8192-4341-bf3e-c6f92b22270a)
 Call ID: f7072d0c-8192-4341-bf3e-c6f92b22270a
  Args:
    type: :Man
    source: :Karl_von_Habsburg
  AssignClass (cb8395b0-7b44-47ba-959e-df9b0adb3c66)
 Call ID: cb8395b0-7b44-47ba-959e-df9b0adb3c66
  Args:
    source: :Karl_von_Habsburg
    type: :Person
  AssignClass (6f007d44-18df-4ff8-84b4-26ae5dd6a5ff)
 Call ID: 6f007d44-18df-4ff8-84b4-26ae5dd6a5ff
  Args:
    source: :Francesca_von_Thyssen-Bornemisza
    type: :Woman
  AssignClass (5ef90a9a-e862-4480-ad79-295e6ce7972b)
 Call ID: 5ef90a9a-e862-4480-ad79-295e6ce7972b
  Args:
    source: :Francesca_von_Thyssen-Bornemisza
    type: :Person
  AddTriple (08628bb5-f54e-4b30-a1c1-e086fb704167)
 Call ID: 08628bb5-f54e-4b30-a1c1-e086fb704167
  Args:
    target: :Karl_von_Habsburg
    relation: :hasFather
    source: :Ferdinand_Habsburg-Lothringen
  AddTriple (5c748721-4cc7-426d-9169-4bd9b146292f)
 Call ID: 5c748721-4cc7-426d-9169-4bd9b146292f
  Args:
    source: :Ferdinand_Habsburg-Lothringen
    relation: :hasMother
    target: :Francesca_von_Thyssen-Bornemisza
  AssignClass (3e37a179-7a70-4fb3-808a-cddc72c428e2)
 Call ID: 3e37a179-7a70-4fb3-808a-cddc72c428e2
  Args:
    type: :Man
    source: :Otto_von_Habsburg
  AssignClass (ae6e7d56-3d78-4a7f-b320-695f84411e39)
 Call ID: ae6e7d56-3d78-4a7f-b320-695f84411e39
  Args:
    type: :Person
    source: :Otto_von_Habsburg
  AssignClass (0b5b3021-d28b-479b-89fa-b19b9b1212ef)
 Call ID: 0b5b3021-d28b-479b-89fa-b19b9b1212ef
  Args:
    type: :Woman
    source: :Regina_of_Saxe-Meiningen
  AssignClass (02919d32-6d81-42c1-995e-bd980780568b)
 Call ID: 02919d32-6d81-42c1-995e-bd980780568b
  Args:
    type: :Person
    source: :Regina_of_Saxe-Meiningen
  AddTriple (70558041-8a28-418f-9a00-3546ba59d81b)
 Call ID: 70558041-8a28-418f-9a00-3546ba59d81b
  Args:
    target: :Otto_von_Habsburg
    relation: :hasFather
    source: :Karl_von_Habsburg
  AddTriple (87b2d25c-3fe5-4c08-9a48-081fc319bef7)
 Call ID: 87b2d25c-3fe5-4c08-9a48-081fc319bef7
  Args:
    relation: :hasMother
    target: :Regina_of_Saxe-Meiningen
    source: :Karl_von_Habsburg
  AssignClass (a601398f-34fd-4468-8538-8e43ed796144)
 Call ID: a601398f-34fd-4468-8538-8e43ed796144
  Args:
    source: :Hans_Heinrich_Thyssen-Bornemisza
    type: :Man
  AssignClass (c26192a4-029f-452d-b299-9ecd4749332a)
 Call ID: c26192a4-029f-452d-b299-9ecd4749332a
  Args:
    source: :Hans_Heinrich_Thyssen-Bornemisza
    type: :Person
  AssignClass (acb894f7-6b98-4718-8036-d844bbaf723e)
 Call ID: acb894f7-6b98-4718-8036-d844bbaf723e
  Args:
    source: :Fiona_Campbell-Walter
    type: :Woman
  AssignClass (9594ff12-e2f9-4ebe-86ee-1de8ebf1457e)
 Call ID: 9594ff12-e2f9-4ebe-86ee-1de8ebf1457e
  Args:
    type: :Person
    source: :Fiona_Campbell-Walter
  AddTriple (3fd118b9-b219-4dc1-abac-34055340b550)
 Call ID: 3fd118b9-b219-4dc1-abac-34055340b550
  Args:
    source: :Francesca_von_Thyssen-Bornemisza
    relation: :hasFather
    target: :Hans_Heinrich_Thyssen-Bornemisza
  AddTriple (1104a68c-1f16-4062-bcf7-196aafe076c1)
 Call ID: 1104a68c-1f16-4062-bcf7-196aafe076c1
  Args:
    source: :Francesca_von_Thyssen-Bornemisza
    target: :Fiona_Campbell-Walter
    relation: :hasMother
  AssignClass (f72c0db6-c5db-4471-a2ea-9cfb6d40fd68)
 Call ID: f72c0db6-c5db-4471-a2ea-9cfb6d40fd68
  Args:
    type: :Woman
    source: :Eleonore_von_Habsburg
  AssignClass (46166e63-72ec-4d08-a769-8acb13ec72c6)
 Call ID: 46166e63-72ec-4d08-a769-8acb13ec72c6
  Args:
    source: :Eleonore_von_Habsburg
    type: :Person
  AssignClass (9722c07b-6f55-49f3-a07f-bf05327cf353)
 Call ID: 9722c07b-6f55-49f3-a07f-bf05327cf353
  Args:
    source: :Gloria_von_Habsburg
    type: :Woman
  AssignClass (3af939e4-30cc-4d3e-aa16-b1bc83e58de1)
 Call ID: 3af939e4-30cc-4d3e-aa16-b1bc83e58de1
  Args:
    type: :Person
    source: :Gloria_von_Habsburg
  AddTriple (d46ee948-2e9a-4b38-88ff-97ea4c80bbb6)
 Call ID: d46ee948-2e9a-4b38-88ff-97ea4c80bbb6
  Args:
    source: :Ferdinand_Habsburg-Lothringen
    relation: :hasSister
    target: :Eleonore_von_Habsburg
  AddTriple (d19945e8-96ad-46c2-ade7-5c91e53752a2)
 Call ID: d19945e8-96ad-46c2-ade7-5c91e53752a2
  Args:
    target: :Gloria_von_Habsburg
    relation: :hasSister
    source: :Ferdinand_Habsburg-Lothringen
  AssignClass (2c0c59a2-d41a-4471-9452-c3cf9867910d)
 Call ID: 2c0c59a2-d41a-4471-9452-c3cf9867910d
  Args:
    source: :Georg_von_Habsburg
    type: :Man
  AssignClass (a19299f4-640e-403e-8280-d752b1a2cf36)
 Call ID: a19299f4-640e-403e-8280-d752b1a2cf36
  Args:
    type: :Person
    source: :Georg_von_Habsburg
  AddTriple (28441e63-5657-4d2b-b0d0-671436b01e4a)
 Call ID: 28441e63-5657-4d2b-b0d0-671436b01e4a
  Args:
    source: :Georg_von_Habsburg
    target: :Karl_von_Habsburg
    relation: :isBrotherOf
  Finish (98acdefb-9de6-4f75-924f-10d7482b7066)
 Call ID: 98acdefb-9de6-4f75-924f-10d7482b7066
  Args: