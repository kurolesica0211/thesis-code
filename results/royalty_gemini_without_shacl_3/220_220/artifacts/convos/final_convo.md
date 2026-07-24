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
Zara Anne Elizabeth Tindall (née Phillips; born 15 May 1981) is a British equestrian, Olympian, and member of the British royal family.
She is the daughter of Anne, Princess Royal, and Captain Mark Phillips, and the eldest niece of King Charles III.
At birth she was sixth in the line of succession to the British throne during the reign of her maternal grandmother, Queen Elizabeth II, and as of 2026 is 22nd.
Tindall won the individual eventing world title at Aachen in 2006 and was later named BBC Sports Personality of the Year.
She married former rugby union player Mike Tindall in 2011, and the couple have three children.
Early life and education

Zara Anne Elizabeth Phillips was born at 8:15 pm on 15 May 1981 at St Mary's Hospital, London.
She has an elder brother, Peter, and two younger half-sisters, Felicity Wade (née Tonkin), from her father's affair with Heather Tonkin; and Stephanie Phillips, from his second marriage to Sandy Pflueger.
Phillips attended Beaudesert Park School in Stroud, Gloucestershire, and Port Regis School in Shaftesbury, Dorset, before following other members of the royal family in attending Gordonstoun School in Moray, Scotland.
Equestrianism

After leaving university, Phillips began to pursue an equestrian career, following in the footsteps of her parents.
Phillips missed the 2004 Summer Olympics in Athens after her horse was injured during training.
Riding Toytown, Phillips won individual and team gold medals at the 2005 European Eventing Championship at Blenheim.
The British Olympic Association selected Phillips and Toytown for the 2008 Olympic Games in Hong Kong; however, Toytown sustained an injury during training and she withdrew from the team.
On 25 October 2008, Phillips fell from her horse, Tsunami II, at the 15th fence of a cross‐country event in Pau, France, breaking her right collarbone.
In July 2010, Musto launched a range of equestrian clothing designed by Phillips, named ZP176 after her team number when she first represented Great Britain.
Phillips competed at the 2012 London Olympic Games on High Kingdom, winning a silver medal in the team event.
She stopped using her maiden name in March 2016 and competed as Zara Tindall for the first time during her unsuccessful attempt to qualify for the 2016 Rio Olympic Games.
In 2017, Tindall finished third at the Kentucky Three-Day Event on High Kingdom, who retired from competition in 2018.
Charity work

Tindall frequently supports and attends events for a range of charitable causes, particularly those connected with spinal injuries, equestrianism, and children's welfare.
Tindall has appeared at events for The Caudwell Charitable Trust, which supports children with special needs, disabilities, and serious illnesses.
The following year, she became patron of the Mark Davies Injured Riders Fund.
In 2013, she visited Stroud Maternity Ward to mark its 60th anniversary, and in 2014 she lent her support to the #bringbackourgirls campaign.
In April 2020, Tindall participated in the Equestrian Relief initiative to help provide additional personal protective equipment for National Health Service workers.
Other activities

In June 2015, Tindall launched an equestrian-themed jewellery collection, named "Zara Phillips Collection", in collaboration with Australian designer John Calleija.
On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Tindall joined her brother and six cousins to mount a 15-minute vigil around the coffin of the Queen, as it lay in state at Westminster Hall.
On 19 September, with her husband Mike and daughter Mia, she joined other family members at the state funeral.
Personal life

Phillips met rugby union player Mike Tindall, who was then playing for the England national team, during the squad's Rugby World Cup-winning campaign in Australia in 2003.
As required at the time by the Royal Marriages Act 1772, the Queen gave her consent to the marriage at a meeting of the Privy Council on 10 May 2011.
A celebration was held on the royal yacht Britannia prior to the wedding.
The Tindalls lived in Cheltenham, Gloucestershire, before moving to Aston Farm, a seven-bedroom property adjoining the Princess Royal's Gatcombe Park estate.
Their first child, Mia Grace, was born on 17 January 2014 at Gloucestershire Royal Hospital and was 16th, later 23rd in the line of succession.
A second daughter, Lena Elizabeth, was born on 18 June 2018 at Stroud Maternity Hospital and was 19th, later 24th, in the line of succession.
Tindall is a godmother to Prince George of Wales, the son of her cousin William, Prince of Wales.
In December 2000, before her marriage, Phillips was involved in a serious car crash near Bourton-on-the-Water, escaping injury after overturning her Land Rover.



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
  AssignClass (f4b28163-5532-4d75-9a8e-6f4ecfc8d434)
 Call ID: f4b28163-5532-4d75-9a8e-6f4ecfc8d434
  Args:
    type: :Person
    source: :ZaraTindall
  AssignClass (6b935bd1-bdb2-441a-89cf-88cb26e5c7de)
 Call ID: 6b935bd1-bdb2-441a-89cf-88cb26e5c7de
  Args:
    source: :ZaraTindall
    type: :Woman
  AssignClass (e812becc-2c2d-485e-b787-19845447cfd5)
 Call ID: e812becc-2c2d-485e-b787-19845447cfd5
  Args:
    type: :Person
    source: :AnnePrincessRoyal
  AssignClass (2568f153-a6a3-4c48-b96a-57931720ecd7)
 Call ID: 2568f153-a6a3-4c48-b96a-57931720ecd7
  Args:
    source: :AnnePrincessRoyal
    type: :Woman
  AssignClass (43320e98-25d6-49f8-96e3-9454596b0a93)
 Call ID: 43320e98-25d6-49f8-96e3-9454596b0a93
  Args:
    source: :AnnePrincessRoyal
    type: :Ancestor
  AssignClass (89495cb1-5dfb-4c16-b525-11569cfc045a)
 Call ID: 89495cb1-5dfb-4c16-b525-11569cfc045a
  Args:
    source: :MarkPhillips
    type: :Person
  AssignClass (29a3f2ba-ddc3-4027-a577-7d5cf0a179d6)
 Call ID: 29a3f2ba-ddc3-4027-a577-7d5cf0a179d6
  Args:
    type: :Man
    source: :MarkPhillips
  AssignClass (e4d9c252-ece4-447f-a45f-b59b04af1cd1)
 Call ID: e4d9c252-ece4-447f-a45f-b59b04af1cd1
  Args:
    type: :Ancestor
    source: :MarkPhillips
  AssignClass (a752fa7a-17ec-4893-b3b4-14c7ce259f87)
 Call ID: a752fa7a-17ec-4893-b3b4-14c7ce259f87
  Args:
    type: :Person
    source: :MikeTindall
  AssignClass (6c5d6989-8e19-4690-9830-ebfc1cd8e564)
 Call ID: 6c5d6989-8e19-4690-9830-ebfc1cd8e564
  Args:
    source: :MikeTindall
    type: :Man
  AssignClass (6109e9f6-ff16-456c-82de-324ac790d5e6)
 Call ID: 6109e9f6-ff16-456c-82de-324ac790d5e6
  Args:
    type: :Person
    source: :MiaGraceTindall
  AssignClass (ae17d87a-2e8d-4a05-98b3-904274ef31fb)
 Call ID: ae17d87a-2e8d-4a05-98b3-904274ef31fb
  Args:
    type: :Woman
    source: :MiaGraceTindall
  AssignClass (80359cdb-7356-42c7-9ade-09bcc764904f)
 Call ID: 80359cdb-7356-42c7-9ade-09bcc764904f
  Args:
    type: :Person
    source: :LenaElizabethTindall
  AssignClass (597f8509-56d7-41b3-ab69-02415aedf88c)
 Call ID: 597f8509-56d7-41b3-ab69-02415aedf88c
  Args:
    type: :Woman
    source: :LenaElizabethTindall
  AssignClass (bedc60dc-f903-4987-b71a-4b13920391ae)
 Call ID: bedc60dc-f903-4987-b71a-4b13920391ae
  Args:
    source: :PeterPhillips
    type: :Person
  AssignClass (747f204f-37f0-4add-a679-6ca16952b409)
 Call ID: 747f204f-37f0-4add-a679-6ca16952b409
  Args:
    source: :PeterPhillips
    type: :Man
  AssignClass (7f5d017b-b202-4497-94d5-443c136dc9dd)
 Call ID: 7f5d017b-b202-4497-94d5-443c136dc9dd
  Args:
    type: :Person
    source: :FelicityWade
  AssignClass (3bf1bca7-5b46-4fc6-8379-57bc11785a15)
 Call ID: 3bf1bca7-5b46-4fc6-8379-57bc11785a15
  Args:
    type: :Woman
    source: :FelicityWade
  AssignClass (ebd05958-0cf8-4303-a90a-b8ab73ded8fe)
 Call ID: ebd05958-0cf8-4303-a90a-b8ab73ded8fe
  Args:
    type: :Person
    source: :StephaniePhillips
  AssignClass (89d1c4a0-1720-44c8-b10b-cf087cfd58cc)
 Call ID: 89d1c4a0-1720-44c8-b10b-cf087cfd58cc
  Args:
    source: :StephaniePhillips
    type: :Woman
  AddLiteral (25295ea5-5489-40b7-a143-d5164210f7b5)
 Call ID: 25295ea5-5489-40b7-a143-d5164210f7b5
  Args:
    source: :ZaraTindall
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1981
  AddTriple (4ef3300b-24e6-497c-8de6-fa7dae918edb)
 Call ID: 4ef3300b-24e6-497c-8de6-fa7dae918edb
  Args:
    target: :AnnePrincessRoyal
    source: :ZaraTindall
    relation: :hasMother
  AddTriple (e926fcb8-ed29-47aa-a18e-6d62497fa641)
 Call ID: e926fcb8-ed29-47aa-a18e-6d62497fa641
  Args:
    source: :ZaraTindall
    target: :MarkPhillips
    relation: :hasFather
  AddTriple (ddebde18-c19a-40ab-b193-5fc00ad500ea)
 Call ID: ddebde18-c19a-40ab-b193-5fc00ad500ea
  Args:
    relation: :hasBrother
    source: :ZaraTindall
    target: :PeterPhillips
  AddTriple (c7b9552d-c19d-46f0-bf44-1ec528cad271)
 Call ID: c7b9552d-c19d-46f0-bf44-1ec528cad271
  Args:
    relation: :hasMother
    source: :MiaGraceTindall
    target: :ZaraTindall
  AddTriple (a65263d6-51e1-48e1-a10b-16b6545544cb)
 Call ID: a65263d6-51e1-48e1-a10b-16b6545544cb
  Args:
    source: :MiaGraceTindall
    target: :MikeTindall
    relation: :hasFather
  AddTriple (74187f18-3dd0-4e8c-bd36-ac789afe8826)
 Call ID: 74187f18-3dd0-4e8c-bd36-ac789afe8826
  Args:
    target: :ZaraTindall
    source: :LenaElizabethTindall
    relation: :hasMother
  AddTriple (dbd87db0-249e-47b9-8b8a-69e0fa23269b)
 Call ID: dbd87db0-249e-47b9-8b8a-69e0fa23269b
  Args:
    relation: :hasFather
    target: :MikeTindall
    source: :LenaElizabethTindall
  AddTriple (654e6dab-0785-4f36-811a-30c805867b1b)
 Call ID: 654e6dab-0785-4f36-811a-30c805867b1b
  Args:
    relation: :hasFather
    target: :MarkPhillips
    source: :FelicityWade
  AddTriple (ee4eabd1-35c7-4c7b-926d-d95c29fc5063)
 Call ID: ee4eabd1-35c7-4c7b-926d-d95c29fc5063
  Args:
    relation: :hasFather
    source: :StephaniePhillips
    target: :MarkPhillips
  AddLiteral (67e2b4ce-d9c4-4a37-a527-9003f08abb19)
 Call ID: 67e2b4ce-d9c4-4a37-a527-9003f08abb19
  Args:
    literal_type: xsd:integer
    literal_value: 2011
    relation: :hasMarriageYear
    source: :ZaraTindall
  AddTriple (9f35cb64-ab1c-4da4-adeb-f6177b65df52)
 Call ID: 9f35cb64-ab1c-4da4-adeb-f6177b65df52
  Args:
    target: :MikeTindall
    source: :ZaraTindall
    relation: :hasRelation
  Finish (c48ff69e-02c7-447e-b6ef-ce2798012de7)
 Call ID: c48ff69e-02c7-447e-b6ef-ce2798012de7
  Args: