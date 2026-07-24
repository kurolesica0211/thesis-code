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
  AssignClass (a3d93301-642d-4384-8ce4-497363df55d6)
 Call ID: a3d93301-642d-4384-8ce4-497363df55d6
  Args:
    source: Zara_Tindall
    type: :Woman
  AssignClass (98bf18fe-cd26-4be8-863c-dca0c923b79b)
 Call ID: 98bf18fe-cd26-4be8-863c-dca0c923b79b
  Args:
    source: Zara_Tindall
    type: :Person
  AddLiteral (af7c6ed9-6699-4a82-82a0-f92ccf39a2e2)
 Call ID: af7c6ed9-6699-4a82-82a0-f92ccf39a2e2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Zara_Tindall
    literal_value: 1981
  AssignClass (d17f1f35-7ea9-49dd-89fc-70c1ffa43327)
 Call ID: d17f1f35-7ea9-49dd-89fc-70c1ffa43327
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (922542e4-e4eb-4a86-9722-bd828a4dd2b9)
 Call ID: 922542e4-e4eb-4a86-9722-bd828a4dd2b9
  Args:
    type: :Ancestor
    source: Anne_Princess_Royal
  AssignClass (31bdc007-5ea5-4126-9c8d-c4f1430a2c96)
 Call ID: 31bdc007-5ea5-4126-9c8d-c4f1430a2c96
  Args:
    source: Mark_Phillips
    type: :Man
  AssignClass (e025ac14-23e1-4c04-bcda-48fc578b6289)
 Call ID: e025ac14-23e1-4c04-bcda-48fc578b6289
  Args:
    source: Mark_Phillips
    type: :Ancestor
  AddTriple (877eddfa-97da-4978-92ff-6c354d147f77)
 Call ID: 877eddfa-97da-4978-92ff-6c354d147f77
  Args:
    source: Zara_Tindall
    relation: :hasMother
    target: Anne_Princess_Royal
  AddTriple (9c13f243-fff3-4fa6-a1a4-f6160ec1e14e)
 Call ID: 9c13f243-fff3-4fa6-a1a4-f6160ec1e14e
  Args:
    source: Zara_Tindall
    relation: :hasFather
    target: Mark_Phillips
  AssignClass (7890a3dd-6ae1-4548-9ca2-1f169dd6c7f9)
 Call ID: 7890a3dd-6ae1-4548-9ca2-1f169dd6c7f9
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (37765cd1-9a59-463e-b3b7-94da1eee2a50)
 Call ID: 37765cd1-9a59-463e-b3b7-94da1eee2a50
  Args:
    source: King_Charles_III
    type: :Person
  AssignClass (072b41f2-a5af-40b5-a89d-9becf9cf49ed)
 Call ID: 072b41f2-a5af-40b5-a89d-9becf9cf49ed
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (10151047-2631-472e-a8e0-c35c5fb53ea6)
 Call ID: 10151047-2631-472e-a8e0-c35c5fb53ea6
  Args:
    type: :Ancestor
    source: Queen_Elizabeth_II
  AddTriple (e030957e-131e-49ba-8c2b-c209fc0aee3b)
 Call ID: e030957e-131e-49ba-8c2b-c209fc0aee3b
  Args:
    source: Anne_Princess_Royal
    relation: :hasMother
    target: Queen_Elizabeth_II
  AssignClass (2a771cc3-8d04-4af6-8a98-3c3efe8ee509)
 Call ID: 2a771cc3-8d04-4af6-8a98-3c3efe8ee509
  Args:
    source: Mike_Tindall
    type: :Man
  AssignClass (b29b677b-f79f-439d-a444-1a44fbf47078)
 Call ID: b29b677b-f79f-439d-a444-1a44fbf47078
  Args:
    source: Mike_Tindall
    type: :Person
  AddLiteral (9f132360-6b7b-4dc1-b0ef-6d0dcd9c2fe4)
 Call ID: 9f132360-6b7b-4dc1-b0ef-6d0dcd9c2fe4
  Args:
    source: Zara_Tindall
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2011
  AddTriple (7eb63213-630d-41ee-b974-e36b842929b3)
 Call ID: 7eb63213-630d-41ee-b974-e36b842929b3
  Args:
    target: Mike_Tindall
    source: Zara_Tindall
    relation: :hasRelation
  AssignClass (cbc75472-a6c3-4486-b46f-17fad1e09fcc)
 Call ID: cbc75472-a6c3-4486-b46f-17fad1e09fcc
  Args:
    source: Peter_Phillips
    type: :Man
  AssignClass (7a43a576-c491-431d-bae4-29e88eda0262)
 Call ID: 7a43a576-c491-431d-bae4-29e88eda0262
  Args:
    type: :Person
    source: Peter_Phillips
  AddTriple (6cc85a0d-67f0-42c5-b770-f803533206a4)
 Call ID: 6cc85a0d-67f0-42c5-b770-f803533206a4
  Args:
    source: Zara_Tindall
    relation: :hasBrother
    target: Peter_Phillips
  AssignClass (f20ac48a-c4d9-4475-8e04-bef4abdba120)
 Call ID: f20ac48a-c4d9-4475-8e04-bef4abdba120
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (f2d20e36-4c8d-4ebb-bc93-742765599997)
 Call ID: f2d20e36-4c8d-4ebb-bc93-742765599997
  Args:
    type: :Person
    source: Felicity_Wade
  AddTriple (31c5f1c4-f0b5-4a66-8959-d3db281167a2)
 Call ID: 31c5f1c4-f0b5-4a66-8959-d3db281167a2
  Args:
    target: Mark_Phillips
    source: Felicity_Wade
    relation: :hasFather
  AssignClass (b3b7af72-313b-48c7-bb21-ea8ab336486d)
 Call ID: b3b7af72-313b-48c7-bb21-ea8ab336486d
  Args:
    source: Stephanie_Phillips
    type: :Woman
  AssignClass (c719103a-18ab-4316-a68d-6439e4674708)
 Call ID: c719103a-18ab-4316-a68d-6439e4674708
  Args:
    source: Stephanie_Phillips
    type: :Person
  AddTriple (6e7ed19b-92db-429a-ac68-8b753a2b935b)
 Call ID: 6e7ed19b-92db-429a-ac68-8b753a2b935b
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Stephanie_Phillips
  AssignClass (6cde65c8-c194-4a93-a8d4-c6d19889753c)
 Call ID: 6cde65c8-c194-4a93-a8d4-c6d19889753c
  Args:
    type: :Woman
    source: Mia_Grace_Tindall
  AssignClass (2791e410-0541-4d10-ba45-6ca60116e3a7)
 Call ID: 2791e410-0541-4d10-ba45-6ca60116e3a7
  Args:
    source: Mia_Grace_Tindall
    type: :Person
  AddTriple (83d2c3a3-748b-4cb3-9b1f-ed8bcc3d7f05)
 Call ID: 83d2c3a3-748b-4cb3-9b1f-ed8bcc3d7f05
  Args:
    target: Zara_Tindall
    relation: :hasMother
    source: Mia_Grace_Tindall
  AddTriple (d642a014-3e7c-4500-b4a2-8537a42a1c55)
 Call ID: d642a014-3e7c-4500-b4a2-8537a42a1c55
  Args:
    target: Mike_Tindall
    relation: :hasFather
    source: Mia_Grace_Tindall
  AssignClass (d4a090d4-75f1-49a7-9ea1-4163fb20a63e)
 Call ID: d4a090d4-75f1-49a7-9ea1-4163fb20a63e
  Args:
    type: :Woman
    source: Lena_Elizabeth_Tindall
  AssignClass (e1c5eaa5-3e0c-4edc-a3c9-404b0203c75e)
 Call ID: e1c5eaa5-3e0c-4edc-a3c9-404b0203c75e
  Args:
    type: :Person
    source: Lena_Elizabeth_Tindall
  AddTriple (feecb66c-8c7d-4354-98a7-90919d7ff11c)
 Call ID: feecb66c-8c7d-4354-98a7-90919d7ff11c
  Args:
    target: Zara_Tindall
    relation: :hasMother
    source: Lena_Elizabeth_Tindall
  AddTriple (c347f221-aa27-485b-8238-34953360bca1)
 Call ID: c347f221-aa27-485b-8238-34953360bca1
  Args:
    relation: :hasFather
    source: Lena_Elizabeth_Tindall
    target: Mike_Tindall
  AssignClass (b52c59cc-6374-4809-92c5-7d0475ed27e6)
 Call ID: b52c59cc-6374-4809-92c5-7d0475ed27e6
  Args:
    source: William_Prince_of_Wales
    type: :Man
  AssignClass (fb0b71e2-5755-46ee-a33c-75d93d047139)
 Call ID: fb0b71e2-5755-46ee-a33c-75d93d047139
  Args:
    source: William_Prince_of_Wales
    type: :Person
  AssignClass (4ea443df-2f36-48af-abdd-07edcd979395)
 Call ID: 4ea443df-2f36-48af-abdd-07edcd979395
  Args:
    type: :Man
    source: Prince_George_of_Wales
  AssignClass (913add31-200a-48f2-ba47-3af8ee558886)
 Call ID: 913add31-200a-48f2-ba47-3af8ee558886
  Args:
    type: :Person
    source: Prince_George_of_Wales
  AddTriple (e2479606-316b-467b-9907-7010b0238cd5)
 Call ID: e2479606-316b-467b-9907-7010b0238cd5
  Args:
    relation: :hasFather
    source: Prince_George_of_Wales
    target: William_Prince_of_Wales
  Finish (52514587-6e50-4070-bb7f-13f937a130c2)
 Call ID: 52514587-6e50-4070-bb7f-13f937a130c2
  Args: