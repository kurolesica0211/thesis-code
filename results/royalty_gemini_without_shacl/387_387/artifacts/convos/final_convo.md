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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (1775144b-b8f7-48a6-9b7e-b73dcec7d010)
 Call ID: 1775144b-b8f7-48a6-9b7e-b73dcec7d010
  Args:
    type: :Woman
    source: :ZaraTindall
  AssignClass (c9089f0d-2c96-413c-af17-b97eb56a8ade)
 Call ID: c9089f0d-2c96-413c-af17-b97eb56a8ade
  Args:
    source: :ZaraTindall
    type: :Person
  AddLiteral (fa8fd9ad-dbd3-45e6-b2b2-29ecacf67b33)
 Call ID: fa8fd9ad-dbd3-45e6-b2b2-29ecacf67b33
  Args:
    source: :ZaraTindall
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Zara Anne Elizabeth Tindall
  AddLiteral (b4d38ecf-2c60-48e1-ada2-a175a2744410)
 Call ID: b4d38ecf-2c60-48e1-ada2-a175a2744410
  Args:
    literal_value: Zara Anne Elizabeth Phillips
    literal_type: xsd:string
    relation: :formerlyKnownAs
    source: :ZaraTindall
  AddLiteral (380b4b52-6e42-4343-9207-da7011c47698)
 Call ID: 380b4b52-6e42-4343-9207-da7011c47698
  Args:
    source: :ZaraTindall
    literal_value: 1981
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (919294a0-5f47-42be-8c74-b9ca0f7614da)
 Call ID: 919294a0-5f47-42be-8c74-b9ca0f7614da
  Args:
    source: :AnnePrincessRoyal
    type: :Woman
  AssignClass (8c83bac4-ee24-4dd9-a1ef-8ac1e818343e)
 Call ID: 8c83bac4-ee24-4dd9-a1ef-8ac1e818343e
  Args:
    source: :AnnePrincessRoyal
    type: :Person
  AssignClass (786a6977-33a1-4d06-8e17-7c6a5eff377e)
 Call ID: 786a6977-33a1-4d06-8e17-7c6a5eff377e
  Args:
    source: :MarkPhillips
    type: :Man
  AssignClass (2742bb33-63dd-4054-ac43-9e5f80094b4c)
 Call ID: 2742bb33-63dd-4054-ac43-9e5f80094b4c
  Args:
    type: :Person
    source: :MarkPhillips
  AddTriple (5eb8907e-130e-45a2-a299-894f33b24065)
 Call ID: 5eb8907e-130e-45a2-a299-894f33b24065
  Args:
    target: :AnnePrincessRoyal
    relation: :hasMother
    source: :ZaraTindall
  AddTriple (96c8a4e9-6814-46a2-ae8f-63f1f3c2ee5f)
 Call ID: 96c8a4e9-6814-46a2-ae8f-63f1f3c2ee5f
  Args:
    target: :MarkPhillips
    relation: :hasFather
    source: :ZaraTindall
  AssignClass (15adada5-7c9c-4015-9036-05624e81f5d1)
 Call ID: 15adada5-7c9c-4015-9036-05624e81f5d1
  Args:
    source: :PeterPhillips
    type: :Man
  AssignClass (57b2ea42-380b-4b5d-891a-30e1847aff3a)
 Call ID: 57b2ea42-380b-4b5d-891a-30e1847aff3a
  Args:
    source: :PeterPhillips
    type: :Person
  AddTriple (e56f6d38-257f-45d2-a796-d2af46416251)
 Call ID: e56f6d38-257f-45d2-a796-d2af46416251
  Args:
    source: :ZaraTindall
    relation: :hasBrother
    target: :PeterPhillips
  AssignClass (b63380f6-3107-409d-91e2-f54451c7ae04)
 Call ID: b63380f6-3107-409d-91e2-f54451c7ae04
  Args:
    source: :FelicityWade
    type: :Woman
  AssignClass (be4c4c37-3da3-4a39-8b0c-cf6f762855fe)
 Call ID: be4c4c37-3da3-4a39-8b0c-cf6f762855fe
  Args:
    source: :FelicityWade
    type: :Person
  AssignClass (786e0a8a-ea5a-4360-8500-5a40ade81680)
 Call ID: 786e0a8a-ea5a-4360-8500-5a40ade81680
  Args:
    source: :StephaniePhillips
    type: :Woman
  AssignClass (2c191764-c37f-49d4-b3f1-a777b5e62687)
 Call ID: 2c191764-c37f-49d4-b3f1-a777b5e62687
  Args:
    type: :Person
    source: :StephaniePhillips
  AddTriple (93710496-6048-4fb9-ac10-edc4d42577f2)
 Call ID: 93710496-6048-4fb9-ac10-edc4d42577f2
  Args:
    source: :ZaraTindall
    target: :FelicityWade
    relation: :hasSister
  AddTriple (b1e109f6-a3bc-4ad3-afc7-e6382ecfd8b9)
 Call ID: b1e109f6-a3bc-4ad3-afc7-e6382ecfd8b9
  Args:
    target: :StephaniePhillips
    relation: :hasSister
    source: :ZaraTindall
  AssignClass (2088e599-9b94-4df5-bd0a-6b88d610a0f9)
 Call ID: 2088e599-9b94-4df5-bd0a-6b88d610a0f9
  Args:
    source: :MikeTindall
    type: :Man
  AssignClass (0f7673b0-89e7-4e2c-b677-a9f19e15269a)
 Call ID: 0f7673b0-89e7-4e2c-b677-a9f19e15269a
  Args:
    type: :Person
    source: :MikeTindall
  AddLiteral (dd8760ee-5b3e-427b-8e24-ab112b50056d)
 Call ID: dd8760ee-5b3e-427b-8e24-ab112b50056d
  Args:
    relation: :hasMarriageYear
    literal_value: 2011
    literal_type: xsd:integer
    source: :ZaraTindall
  AddTriple (7a44d5bb-6817-47cf-8a03-bcbb15b96e48)
 Call ID: 7a44d5bb-6817-47cf-8a03-bcbb15b96e48
  Args:
    relation: :hasRelation
    target: :MikeTindall
    source: :ZaraTindall
  AssignClass (f443e031-629c-4d65-abc0-2d202040e056)
 Call ID: f443e031-629c-4d65-abc0-2d202040e056
  Args:
    type: :Woman
    source: :MiaGraceTindall
  AssignClass (548843ef-2f25-48d7-88a1-704b22a127f7)
 Call ID: 548843ef-2f25-48d7-88a1-704b22a127f7
  Args:
    type: :Person
    source: :MiaGraceTindall
  AssignClass (97bbb57d-220c-4dc9-a03e-1f8f9a368e81)
 Call ID: 97bbb57d-220c-4dc9-a03e-1f8f9a368e81
  Args:
    source: :LenaElizabethTindall
    type: :Woman
  AssignClass (f4a88c20-01de-4f44-a569-b033420d68f7)
 Call ID: f4a88c20-01de-4f44-a569-b033420d68f7
  Args:
    type: :Person
    source: :LenaElizabethTindall
  AddTriple (e94ea56a-fc55-444a-80ee-dbd454982e6b)
 Call ID: e94ea56a-fc55-444a-80ee-dbd454982e6b
  Args:
    source: :MiaGraceTindall
    relation: :hasMother
    target: :ZaraTindall
  AddTriple (56317bbf-fe27-4c69-bd7d-fd6d55a283de)
 Call ID: 56317bbf-fe27-4c69-bd7d-fd6d55a283de
  Args:
    source: :LenaElizabethTindall
    relation: :hasMother
    target: :ZaraTindall
  AddTriple (c7f6595c-f924-4a58-aec7-3628b621d7d3)
 Call ID: c7f6595c-f924-4a58-aec7-3628b621d7d3
  Args:
    source: :MiaGraceTindall
    relation: :hasFather
    target: :MikeTindall
  AddTriple (af03f87e-987f-437b-abdc-1bff88b3d968)
 Call ID: af03f87e-987f-437b-abdc-1bff88b3d968
  Args:
    relation: :hasFather
    target: :MikeTindall
    source: :LenaElizabethTindall
  Finish (99d23ca4-4b10-42ac-bd4a-cfac399cfe75)
 Call ID: 99d23ca4-4b10-42ac-bd4a-cfac399cfe75
  Args: