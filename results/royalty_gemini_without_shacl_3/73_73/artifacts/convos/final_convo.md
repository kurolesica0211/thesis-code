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


Christian, Crown Prince of Denmark, Count of Monpezat RE (Christian Valdemar Henri John; born 15 October 2005), is the heir apparent to the Danish throne.
He is the eldest child of King Frederik X and Queen Mary.
He was born during the reign of his paternal grandmother, Queen Margrethe II.
He became Crown Prince of Denmark following his grandmother's abdication and his father's subsequent ascension to the Danish throne in January 2024.
Early life

Christian was born on 15 October 2005 at 1:57 am CET at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen.
At sunset on the same day beacon bonfires were lit all across Denmark, while Naval Home Guard vessels lit their searchlights and directed them towards the capital.
Christian was baptised on 21 January 2006 in Christiansborg Palace Chapel by the Bishop of Copenhagen Erik Norman Svendsen.
He was baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671, and wore the royal christening gown which was made for his great-great-grandfather, King Christian X, in 1870.
Christian's godparents are his paternal uncle, Prince Joachim of Denmark; his maternal aunt, Jane Stephens; his father's first cousin, the Crown Prince of Greece; the Crown Prince and Crown Princess of Norway; the Crown Princess of Sweden; and two friends of the couple, Jeppe Handwerk and Hamish Campbell.
He was named Christian Valdemar Henri John, continuing the Danish royal tradition of alternating between the names Christian and Frederik in direct line.
He received a number of presents on the occasion of his christening, including a pony called Flikflak from the Folketing, Denmark's national parliament.
On 11 September 2006, Per Stig Møller, Denmark's Minister for Foreign Affairs, formally wrote and signed a hand-written document confirming Prince Christian's place in the line of succession.
The prince's full name, his dates of birth and baptism, and the names of his godparents were recorded as dictated by the Royal Law of 1799.
Education

Christian was the first member of the Danish royal family to attend nursery school.
The Danish court announced in October 2019 that Christian and his three younger siblings would undertake a 12-week school stay at Lemania-Verbier International School in Verbier, Switzerland, in the beginning of 2020.
The stay was cut short and the siblings returned home in March due to the intensification of the COVID-19 situation in Denmark.
In April 2021, it was announced that Christian would undertake his secondary education at the Danish boarding school Herlufsholm, starting in August 2021.
In June 2022, shortly after finishing the first year of his upper secondary education, it was announced that Christian would no longer attend the school, after recurring allegations of bullying, violence and sexual abuse at the institution surfaced in a documentary.
Activities

Christian undertook his first official engagement when he attended the opening of a new elephant house at the Copenhagen Zoo with his grandfather, Prince Henrik in 2008.
Christian opened the elephant house by pressing a button on an interactive console.
The elephants were a gift from the King and Queen of Thailand to the Queen and Prince Consort of Denmark on their visit to Thailand.
In 2010, Christian and his grandfather revealed a portrait of Prince Ulrik at the Museum of National History at Frederiksborg Castle, and in 2012, also at the Museum of National History, he and Queen Margrethe II revealed the first ever portrait of him (with his father and grandmother), commissioned for the Queen's Ruby Jubilee.
He and his siblings accompanied their parents on an official visit to Greenland on 1–8 August 2014, where Christian partook in several official engagements.
Christian was confirmed on 15 May 2021 in the Royal Chapel of Fredensborg Palace.
On 13 June 2021, Christian accompanied his grandmother and father at the COVID-19 postponed centenary of the reunification of Denmark and Northern Schleswig, following the route his great-great-grandfather Christian X rode on 15 July 1920 over the old border between Denmark and Germany.
Accompanying his father, Christian attended a memorial for the victims of the 2022 Copenhagen mall shooting on 5 July 2022.
For the 18th birthday of Prince Christian, which marked the beginning of his royal duties, Margrethe II hosted a banquet at Christianborg Palace.
In attendance were members of the Danish royal family, including Christian's parents, siblings, cousins and Princess Benedikte, and 200 members of the Danish public youth who had distinguished themselves in sport, art and culture.
Additionally, Margrethe II invited eleven members of foreign royal families – Queen Anne-Marie of Greece, the Crown Prince and Crown Princess of Greece, the Crown Prince and Crown Princess of Norway, Princess Ingrid Alexandra of Norway, the Crown Princess of Sweden, the Duke of Västergötland, the Duchess of Östergötland, the Princess of Orange and the Duchess of Brabant.
A photo was captured on the night that contained the future monarchs of Belgium, Denmark, the Netherlands, Norway and Sweden.
"


On 20 May 2024, Christian carried out his first solo engagement when he participated in Royal Run 2024's Brønderslev leg.
Military service

On 3 February 2025, Christian began his conscription with the Guard Hussar Regiment at Antvorskov Barracks in Slagelse.
During his military service, Christian has renounced his salary and any money that conscripts receive.
On 28 May 2025, Christian completed his conscription following the completion of the traditional "REX-tour", a strenuous four-day military exercise undertaken by conscripts in the Guard Hussar Regiment and the Royal Life Guards.
In January 2026, it was announced that Christian will serve as a platoon commander in the Royal Life Guards based at Høvelte Barracks starting August 2026.
Crown Prince of Denmark

Christian is first in line to the Danish throne and eldest child of King Frederik X. Since the 16th century, first-born sons of Danish monarchs have traditionally been alternately named Frederik and Christian.
He is expected to reign as Christian XI.
Christian's grandmother, Queen Margrethe II, announced her pending abdication on live television in her New Year's Eve address on 31 December 2023.
On 14 January 2024, Prince Christian, the Queen, and Crown Prince Frederik participated in a meeting of the Council of State, with the cabinet ministers and the council of state secretary in attendance.
The moment the Queen signed a declaration of her abdication, Crown Prince Frederik acceded to the Danish throne as King Frederik X. Christian, who became the heir apparent, is referred to as "HRH Crown Prince Christian".
In January 2024, Christian became a regent for the first time during his father's three day state visit to Poland.
Personal life

Christian is godfather to his second cousin, Prince Gustav Albrecht, the son of Gustav, 7th Prince of Sayn-Wittgenstein-Berleburg.
He served as page boy at the 2010 wedding of his godmother, the Crown Princess of Sweden.
Christian is an avid fan of the football club F.C. Copenhagen and has frequently been seen attending their matches.
Titles, styles, honours, and arms

Titles

Honours

National honours

Orders and appointments

Medals and decorations

Foreign honours

Other honours

In 2006 Scandinavian Airlines System was in the process of purchasing new Airbus A319 aircraft and in Christian's honour the first of these, delivered on 8 August 2006, was named Christian Valdemar Viking.
Arms

Crown Prince Christian’s coat of arms is similar to the royal coat of arms except for the heir apparent's crown and the purple mantle.



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
  AssignClass (2d43cf17-af08-4e83-8c4a-7fd4823cabeb)
 Call ID: 2d43cf17-af08-4e83-8c4a-7fd4823cabeb
  Args:
    type: :Man
    source: Christian_Crown_Prince_of_Denmark
  AssignClass (93dcea74-933b-4243-a157-76913a8b78b5)
 Call ID: 93dcea74-933b-4243-a157-76913a8b78b5
  Args:
    source: King_Frederik_X
    type: :Man
  AssignClass (645b9fa5-87f9-474f-a2d3-de5f3468820b)
 Call ID: 645b9fa5-87f9-474f-a2d3-de5f3468820b
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (19070067-da99-47e9-8e06-24c41893e75d)
 Call ID: 19070067-da99-47e9-8e06-24c41893e75d
  Args:
    type: :Woman
    source: Queen_Margrethe_II
  AssignClass (43ff477e-bb16-4bcc-a1f5-3a199bdd89ff)
 Call ID: 43ff477e-bb16-4bcc-a1f5-3a199bdd89ff
  Args:
    source: Prince_Henrik
    type: :Man
  AddLiteral (148d5eae-1e91-41e8-a0a9-95555d26e27b)
 Call ID: 148d5eae-1e91-41e8-a0a9-95555d26e27b
  Args:
    source: Christian_Crown_Prince_of_Denmark
    literal_type: xsd:integer
    literal_value: 2005
    relation: :hasBirthYear
  AddTriple (096ba6c1-64e1-4680-8d16-dde1932ace5d)
 Call ID: 096ba6c1-64e1-4680-8d16-dde1932ace5d
  Args:
    target: King_Frederik_X
    source: Christian_Crown_Prince_of_Denmark
    relation: :hasFather
  AddTriple (eb451837-58c2-483c-8b32-c0abbcd14f64)
 Call ID: eb451837-58c2-483c-8b32-c0abbcd14f64
  Args:
    relation: :hasMother
    source: Christian_Crown_Prince_of_Denmark
    target: Queen_Mary
  AddTriple (3e0c3e9f-485c-405a-8f75-c6cff4f16007)
 Call ID: 3e0c3e9f-485c-405a-8f75-c6cff4f16007
  Args:
    relation: :hasMother
    target: Queen_Margrethe_II
    source: King_Frederik_X
  AddTriple (a0900f4d-3ea2-472e-a211-47723d41c9cf)
 Call ID: a0900f4d-3ea2-472e-a211-47723d41c9cf
  Args:
    relation: :hasFather
    source: King_Frederik_X
    target: Prince_Henrik
  Finish (c83694ce-c365-45c2-8bce-9b35095d25cb)
 Call ID: c83694ce-c365-45c2-8bce-9b35095d25cb
  Args: