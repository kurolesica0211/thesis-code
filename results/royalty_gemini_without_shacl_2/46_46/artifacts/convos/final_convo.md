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
The following year she carried the Olympic flame at Cheltenham Racecourse on her horse Toytown, and went on to win a team silver medal in eventing at the 2012 London Summer Olympics, presented to her by her mother.
Early life and education

Zara Anne Elizabeth Phillips was born at 8:15 pm on 15 May 1981 at St Mary's Hospital, London.
Her first name was suggested by her uncle, Charles, the then Prince of Wales.
Her godparents are her maternal uncle, Andrew Mountbatten-Windsor; the Countess of Lichfield; Helen, Lady Stewart, the wife of Sir Jackie Stewart; Andrew Parker Bowles; and Hugh Thomas.
She has an elder brother, Peter, and two younger half-sisters, Felicity Wade (née Tonkin), from her father's affair with Heather Tonkin; and Stephanie Phillips, from his second marriage to Sandy Pflueger.
Phillips attended Beaudesert Park School in Stroud, Gloucestershire, and Port Regis School in Shaftesbury, Dorset, before following other members of the royal family in attending Gordonstoun School in Moray, Scotland.
Equestrianism

After leaving university, Phillips began to pursue an equestrian career, following in the footsteps of her parents.
Phillips missed the 2004 Summer Olympics in Athens after her horse was injured during training.
Riding Toytown, Phillips won individual and team gold medals at the 2005 European Eventing Championship at Blenheim.
Following her success in Germany, she was voted BBC Sports Personality of the Year, an award previously won by her mother in 1971.
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
A reception followed at the Palace of Holyroodhouse.
The Tindalls lived in Cheltenham, Gloucestershire, before moving to Aston Farm, a seven-bedroom property adjoining the Princess Royal's Gatcombe Park estate.
Their first child, Mia Grace, was born on 17 January 2014 at Gloucestershire Royal Hospital and was 16th, later 23rd in the line of succession.
A second daughter, Lena Elizabeth, was born on 18 June 2018 at Stroud Maternity Hospital and was 19th, later 24th, in the line of succession.
Their son, Lucas Philip, was born on 21 March 2021 at the family home on the Gatcombe Park estate and was 22nd, later 25th, in the line of succession.
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
  AssignClass (ac817ab8-37ed-4b35-870c-bd37e1ef643b)
 Call ID: ac817ab8-37ed-4b35-870c-bd37e1ef643b
  Args:
    source: :Zara_Tindall
    type: :Woman
  AssignClass (1b4fbcb1-f6db-4324-9923-30856d85c3d7)
 Call ID: 1b4fbcb1-f6db-4324-9923-30856d85c3d7
  Args:
    source: :Zara_Tindall
    type: :Person
  AddLiteral (e961917d-3088-4868-9e3b-629d9c03ef57)
 Call ID: e961917d-3088-4868-9e3b-629d9c03ef57
  Args:
    literal_value: 1981
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Zara_Tindall
  AssignClass (67354275-71de-483e-9874-3750756f527c)
 Call ID: 67354275-71de-483e-9874-3750756f527c
  Args:
    source: :Anne_Princess_Royal
    type: :Woman
  AssignClass (a3c15578-feb2-4c49-b8fe-4bc221a2c50d)
 Call ID: a3c15578-feb2-4c49-b8fe-4bc221a2c50d
  Args:
    source: :Anne_Princess_Royal
    type: :Person
  AssignClass (44afe430-f035-4c93-a281-e9cbcd1fac23)
 Call ID: 44afe430-f035-4c93-a281-e9cbcd1fac23
  Args:
    type: :Man
    source: :Mark_Phillips
  AssignClass (c91bd329-3829-4ebe-ac32-055e79652190)
 Call ID: c91bd329-3829-4ebe-ac32-055e79652190
  Args:
    type: :Person
    source: :Mark_Phillips
  AddTriple (411cb095-c2e8-42f4-948c-fffad61fe787)
 Call ID: 411cb095-c2e8-42f4-948c-fffad61fe787
  Args:
    source: :Zara_Tindall
    target: :Anne_Princess_Royal
    relation: :hasMother
  AddTriple (d9f6cc5e-b146-47b6-ba4a-2a262fed000d)
 Call ID: d9f6cc5e-b146-47b6-ba4a-2a262fed000d
  Args:
    source: :Zara_Tindall
    target: :Mark_Phillips
    relation: :hasFather
  AssignClass (13df1794-6676-455e-b7f6-e3b822e1e887)
 Call ID: 13df1794-6676-455e-b7f6-e3b822e1e887
  Args:
    source: :King_Charles_III
    type: :Man
  AssignClass (f9802fce-8c4c-4189-8888-c4c3ecf8f1b5)
 Call ID: f9802fce-8c4c-4189-8888-c4c3ecf8f1b5
  Args:
    type: :Person
    source: :King_Charles_III
  AssignClass (0e1dd548-9660-4ee7-b431-1753be5637a1)
 Call ID: 0e1dd548-9660-4ee7-b431-1753be5637a1
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (dc1670e8-882a-4b64-9a5a-7927a7767a7a)
 Call ID: dc1670e8-882a-4b64-9a5a-7927a7767a7a
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AddTriple (64a967f8-0abf-4fe1-afae-1c25b3305637)
 Call ID: 64a967f8-0abf-4fe1-afae-1c25b3305637
  Args:
    target: :Queen_Elizabeth_II
    relation: :hasMother
    source: :Anne_Princess_Royal
  AssignClass (a79a88c6-5ccc-4cbb-97ab-73115a3c7488)
 Call ID: a79a88c6-5ccc-4cbb-97ab-73115a3c7488
  Args:
    source: :Mike_Tindall
    type: :Man
  AssignClass (dcba1850-6714-4dbc-ad65-782aa14bf55e)
 Call ID: dcba1850-6714-4dbc-ad65-782aa14bf55e
  Args:
    source: :Mike_Tindall
    type: :Person
  AddLiteral (a1ccf0d2-4e1e-4bfa-aaea-ffc3676d15c7)
 Call ID: a1ccf0d2-4e1e-4bfa-aaea-ffc3676d15c7
  Args:
    source: :Zara_Tindall
    literal_type: xsd:integer
    literal_value: 2011
    relation: :hasMarriageYear
  AddTriple (4bd9bbc8-8774-45c7-8a0d-e38ba938f561)
 Call ID: 4bd9bbc8-8774-45c7-8a0d-e38ba938f561
  Args:
    source: :Zara_Tindall
    relation: :hasRelation
    target: :Mike_Tindall
  AssignClass (98d39d7d-4fb3-4a9e-bea9-30db37359608)
 Call ID: 98d39d7d-4fb3-4a9e-bea9-30db37359608
  Args:
    type: :Man
    source: :Peter_Phillips
  AssignClass (4e779c0a-da68-4fd0-80ca-351802578811)
 Call ID: 4e779c0a-da68-4fd0-80ca-351802578811
  Args:
    source: :Peter_Phillips
    type: :Person
  AddTriple (85e68094-70db-4253-84a6-7334d465a0ce)
 Call ID: 85e68094-70db-4253-84a6-7334d465a0ce
  Args:
    target: :Peter_Phillips
    relation: :hasBrother
    source: :Zara_Tindall
  AssignClass (cb5d4058-eb46-420b-9f43-64af1b5617bb)
 Call ID: cb5d4058-eb46-420b-9f43-64af1b5617bb
  Args:
    source: :Felicity_Wade
    type: :Woman
  AssignClass (23e9ffca-0d27-4332-844b-850aa389f03b)
 Call ID: 23e9ffca-0d27-4332-844b-850aa389f03b
  Args:
    source: :Felicity_Wade
    type: :Person
  AddTriple (09d744f3-0a13-48c4-b0a8-da68d5c0f95f)
 Call ID: 09d744f3-0a13-48c4-b0a8-da68d5c0f95f
  Args:
    source: :Felicity_Wade
    target: :Mark_Phillips
    relation: :hasFather
  AssignClass (e0af6140-1f16-4a02-aa86-d2dc5e9e4975)
 Call ID: e0af6140-1f16-4a02-aa86-d2dc5e9e4975
  Args:
    source: :Stephanie_Phillips
    type: :Woman
  AssignClass (541f2f01-7ade-437a-b1ec-af4add50969d)
 Call ID: 541f2f01-7ade-437a-b1ec-af4add50969d
  Args:
    source: :Stephanie_Phillips
    type: :Person
  AddTriple (902c4905-51a5-49e7-b4ea-56fef80171b3)
 Call ID: 902c4905-51a5-49e7-b4ea-56fef80171b3
  Args:
    source: :Stephanie_Phillips
    relation: :hasFather
    target: :Mark_Phillips
  AssignClass (b65a3ca0-1146-461a-93c3-c44f1ea68893)
 Call ID: b65a3ca0-1146-461a-93c3-c44f1ea68893
  Args:
    type: :Woman
    source: :Mia_Grace_Tindall
  AssignClass (e60789c1-c9af-4ffe-bb1f-6604723bff16)
 Call ID: e60789c1-c9af-4ffe-bb1f-6604723bff16
  Args:
    source: :Mia_Grace_Tindall
    type: :Person
  AddTriple (3892b8ef-7d68-42ca-bda7-e38767b475ef)
 Call ID: 3892b8ef-7d68-42ca-bda7-e38767b475ef
  Args:
    source: :Mia_Grace_Tindall
    target: :Zara_Tindall
    relation: :hasMother
  AddTriple (a9332f4e-094a-4554-a63f-1a90c0f8678e)
 Call ID: a9332f4e-094a-4554-a63f-1a90c0f8678e
  Args:
    relation: :hasFather
    target: :Mike_Tindall
    source: :Mia_Grace_Tindall
  AssignClass (dcf0a309-6453-4186-a7a0-eb9d9fa3ef7a)
 Call ID: dcf0a309-6453-4186-a7a0-eb9d9fa3ef7a
  Args:
    type: :Woman
    source: :Lena_Elizabeth_Tindall
  AssignClass (6a4d1068-2832-42c1-8400-b6e175cea35a)
 Call ID: 6a4d1068-2832-42c1-8400-b6e175cea35a
  Args:
    source: :Lena_Elizabeth_Tindall
    type: :Person
  AddTriple (2600869a-c80a-4bad-a647-62fd32c4b96f)
 Call ID: 2600869a-c80a-4bad-a647-62fd32c4b96f
  Args:
    source: :Lena_Elizabeth_Tindall
    relation: :hasMother
    target: :Zara_Tindall
  AddTriple (a1b838fc-7b74-4260-bab6-303d058187a3)
 Call ID: a1b838fc-7b74-4260-bab6-303d058187a3
  Args:
    relation: :hasFather
    target: :Mike_Tindall
    source: :Lena_Elizabeth_Tindall
  AssignClass (e8ea6291-b98c-45ef-a987-039bb4a5aa25)
 Call ID: e8ea6291-b98c-45ef-a987-039bb4a5aa25
  Args:
    type: :Man
    source: :Lucas_Philip_Tindall
  AssignClass (82d018cb-909c-486a-8653-6c72d8282912)
 Call ID: 82d018cb-909c-486a-8653-6c72d8282912
  Args:
    type: :Person
    source: :Lucas_Philip_Tindall
  AddTriple (617c5053-1253-4250-85fe-0af53621de19)
 Call ID: 617c5053-1253-4250-85fe-0af53621de19
  Args:
    target: :Zara_Tindall
    relation: :hasMother
    source: :Lucas_Philip_Tindall
  AddTriple (ef901ad1-8dd7-4dfd-affb-2eac14aa314b)
 Call ID: ef901ad1-8dd7-4dfd-affb-2eac14aa314b
  Args:
    source: :Lucas_Philip_Tindall
    relation: :hasFather
    target: :Mike_Tindall
  Finish (8399be30-3485-4637-98df-62ec18c8914d)
 Call ID: 8399be30-3485-4637-98df-62ec18c8914d
  Args: