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
  AssignClass (1f2850e5-f626-4601-afbd-b7c932a2933d)
 Call ID: 1f2850e5-f626-4601-afbd-b7c932a2933d
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (127bf9fc-02c8-4cff-8207-aa49daabc161)
 Call ID: 127bf9fc-02c8-4cff-8207-aa49daabc161
  Args:
    source: Zara_Tindall
    type: :Person
  AddLiteral (badad8c4-387f-4bbd-84be-a943a9883ee9)
 Call ID: badad8c4-387f-4bbd-84be-a943a9883ee9
  Args:
    literal_type: xsd:integer
    source: Zara_Tindall
    literal_value: 1981
    relation: :hasBirthYear
  AddTriple (833eb0a0-7ab9-4660-bd82-92e07029757e)
 Call ID: 833eb0a0-7ab9-4660-bd82-92e07029757e
  Args:
    source: Zara_Tindall
    target: Anne_Princess_Royal
    relation: :hasMother
  AddTriple (31ef96d0-eff8-4d2d-b0ae-4c4951712656)
 Call ID: 31ef96d0-eff8-4d2d-b0ae-4c4951712656
  Args:
    target: Mark_Phillips
    source: Zara_Tindall
    relation: :hasFather
  AssignClass (010e1bbb-5508-4a6a-b950-52825a858570)
 Call ID: 010e1bbb-5508-4a6a-b950-52825a858570
  Args:
    source: Anne_Princess_Royal
    type: :Woman
  AssignClass (154d0dc7-5457-4b88-81f0-9a632b50c444)
 Call ID: 154d0dc7-5457-4b88-81f0-9a632b50c444
  Args:
    type: :Person
    source: Anne_Princess_Royal
  AssignClass (a1411051-7849-4909-b765-b1b02e582dd8)
 Call ID: a1411051-7849-4909-b765-b1b02e582dd8
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (9c645ae3-8d85-48c1-914c-0a0d07005b60)
 Call ID: 9c645ae3-8d85-48c1-914c-0a0d07005b60
  Args:
    type: :Person
    source: Mark_Phillips
  AddTriple (78bae84a-b427-4a04-a5e7-72e38628b834)
 Call ID: 78bae84a-b427-4a04-a5e7-72e38628b834
  Args:
    relation: :hasBrother
    source: Zara_Tindall
    target: Peter_Phillips
  AssignClass (5fb00e0f-7bcc-49f0-866f-93447114ab92)
 Call ID: 5fb00e0f-7bcc-49f0-866f-93447114ab92
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (60f6ba4a-ebdb-4b2c-afec-2db12e4aec44)
 Call ID: 60f6ba4a-ebdb-4b2c-afec-2db12e4aec44
  Args:
    type: :Person
    source: Peter_Phillips
  AddTriple (ab358cdd-ba38-4458-a4ef-026755d625c6)
 Call ID: ab358cdd-ba38-4458-a4ef-026755d625c6
  Args:
    relation: :hasSister
    target: Felicity_Wade
    source: Zara_Tindall
  AssignClass (b6aeb610-dc10-4209-8915-9eb85303af0f)
 Call ID: b6aeb610-dc10-4209-8915-9eb85303af0f
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (c98759f8-b98b-4adf-97ed-4342132af7cd)
 Call ID: c98759f8-b98b-4adf-97ed-4342132af7cd
  Args:
    type: :Person
    source: Felicity_Wade
  AddTriple (a869c667-2d4d-463f-a7c2-257c7124f794)
 Call ID: a869c667-2d4d-463f-a7c2-257c7124f794
  Args:
    relation: :hasSister
    source: Zara_Tindall
    target: Stephanie_Phillips
  AssignClass (04655584-fa8f-4f31-993a-4c883878d2a6)
 Call ID: 04655584-fa8f-4f31-993a-4c883878d2a6
  Args:
    source: Stephanie_Phillips
    type: :Woman
  AssignClass (8ec248b3-7241-4c01-afac-b167b910f1be)
 Call ID: 8ec248b3-7241-4c01-afac-b167b910f1be
  Args:
    source: Stephanie_Phillips
    type: :Person
  AddTriple (49e0d3f0-d62b-4663-8fd8-9c6e3771f87e)
 Call ID: 49e0d3f0-d62b-4663-8fd8-9c6e3771f87e
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Felicity_Wade
  AddTriple (cc250d7a-42de-47bd-92c7-c12398ffd018)
 Call ID: cc250d7a-42de-47bd-92c7-c12398ffd018
  Args:
    target: Mark_Phillips
    source: Stephanie_Phillips
    relation: :hasFather
  AddTriple (1164a9a6-9917-49ad-8303-924e4cf27aee)
 Call ID: 1164a9a6-9917-49ad-8303-924e4cf27aee
  Args:
    relation: :hasMother
    target: Heather_Tonkin
    source: Felicity_Wade
  AddTriple (35eb0d4b-841f-4cd6-aff5-c4f6ec001e01)
 Call ID: 35eb0d4b-841f-4cd6-aff5-c4f6ec001e01
  Args:
    source: Stephanie_Phillips
    target: Sandy_Pflueger
    relation: :hasMother
  AssignClass (22de162c-005f-4f28-97a5-301ec3faa432)
 Call ID: 22de162c-005f-4f28-97a5-301ec3faa432
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (18f04c7a-8497-4090-beb7-2ef9b8cf44b6)
 Call ID: 18f04c7a-8497-4090-beb7-2ef9b8cf44b6
  Args:
    type: :Person
    source: Heather_Tonkin
  AssignClass (5a0c8151-1e1d-4aa3-b8f9-93821f75d669)
 Call ID: 5a0c8151-1e1d-4aa3-b8f9-93821f75d669
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (45729e09-08f4-4f14-8e4b-213121da8e5a)
 Call ID: 45729e09-08f4-4f14-8e4b-213121da8e5a
  Args:
    type: :Person
    source: Sandy_Pflueger
  AddTriple (f3dbe78c-316e-4db3-b0d7-b8cc24c74b9f)
 Call ID: f3dbe78c-316e-4db3-b0d7-b8cc24c74b9f
  Args:
    source: Peter_Phillips
    target: Mark_Phillips
    relation: :hasFather
  AddTriple (edf2df8a-de64-46d0-b906-7006665f8c45)
 Call ID: edf2df8a-de64-46d0-b906-7006665f8c45
  Args:
    source: Peter_Phillips
    target: Anne_Princess_Royal
    relation: :hasMother
  AddTriple (9eb1c11e-0390-479c-843e-591df41048bc)
 Call ID: 9eb1c11e-0390-479c-843e-591df41048bc
  Args:
    target: Queen_Elizabeth_II
    source: Zara_Tindall
    relation: :hasMother
  AssignClass (43385ca1-ce79-440a-ad38-d90668b7970e)
 Call ID: 43385ca1-ce79-440a-ad38-d90668b7970e
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (03b60ce1-9cb1-4410-a215-aa9859c7da3a)
 Call ID: 03b60ce1-9cb1-4410-a215-aa9859c7da3a
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AddTriple (aea65888-0803-4b07-9fe1-7795e812143e)
 Call ID: aea65888-0803-4b07-9fe1-7795e812143e
  Args:
    target: Mike_Tindall
    source: Zara_Tindall
    relation: :hasRelation
  AssignClass (9d77f403-82ef-4c29-9eb6-59d20bdc8209)
 Call ID: 9d77f403-82ef-4c29-9eb6-59d20bdc8209
  Args:
    type: :Man
    source: Mike_Tindall
  AssignClass (cc93ca31-b347-44b4-95ae-ecd6a6ddcad3)
 Call ID: cc93ca31-b347-44b4-95ae-ecd6a6ddcad3
  Args:
    type: :Person
    source: Mike_Tindall
  AddLiteral (526a7c1f-efe9-4637-9166-a846488a668d)
 Call ID: 526a7c1f-efe9-4637-9166-a846488a668d
  Args:
    literal_type: xsd:integer
    source: Zara_Tindall
    literal_value: 2011
    relation: :hasMarriageYear
  AddTriple (bf905f83-f0c0-4171-841d-9a0ce5b7c926)
 Call ID: bf905f83-f0c0-4171-841d-9a0ce5b7c926
  Args:
    source: Zara_Tindall
    target: Mia_Grace_Tindall
    relation: :hasDaughter
  AddTriple (ee7bf72a-0230-4c25-b5dd-c60f4dcb93a5)
 Call ID: ee7bf72a-0230-4c25-b5dd-c60f4dcb93a5
  Args:
    source: Zara_Tindall
    target: Lena_Elizabeth_Tindall
    relation: :hasDaughter
  AssignClass (8662dcfa-9a25-4b93-a809-f9370be1f6ea)
 Call ID: 8662dcfa-9a25-4b93-a809-f9370be1f6ea
  Args:
    type: :Woman
    source: Mia_Grace_Tindall
  AssignClass (a9e2e0cf-426c-40e8-a7f1-ecaaecac6273)
 Call ID: a9e2e0cf-426c-40e8-a7f1-ecaaecac6273
  Args:
    type: :Person
    source: Mia_Grace_Tindall
  AssignClass (739e3c25-3548-4df2-aa00-7b359daefd50)
 Call ID: 739e3c25-3548-4df2-aa00-7b359daefd50
  Args:
    type: :Woman
    source: Lena_Elizabeth_Tindall
  AssignClass (d7b4797a-5bd2-47b1-a9c1-a1bcf9e72238)
 Call ID: d7b4797a-5bd2-47b1-a9c1-a1bcf9e72238
  Args:
    source: Lena_Elizabeth_Tindall
    type: :Person
  AddTriple (9c0da1ec-737a-4ed1-973c-7c39268e117e)
 Call ID: 9c0da1ec-737a-4ed1-973c-7c39268e117e
  Args:
    relation: :hasFather
    source: Mia_Grace_Tindall
    target: Mike_Tindall
  AddTriple (9ed5f837-edd3-42b5-ac7e-1603b6d5cb6d)
 Call ID: 9ed5f837-edd3-42b5-ac7e-1603b6d5cb6d
  Args:
    relation: :hasFather
    target: Mike_Tindall
    source: Lena_Elizabeth_Tindall
  Finish (e92b5c7c-233f-4a4c-a98d-dc0347e90b7f)
 Call ID: e92b5c7c-233f-4a4c-a98d-dc0347e90b7f
  Args: