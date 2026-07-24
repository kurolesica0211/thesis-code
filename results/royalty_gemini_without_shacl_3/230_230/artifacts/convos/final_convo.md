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
Peter Mark Andrew Phillips (born 15 November 1977) is a British businessman and member of the British royal family.
He is the son of Anne, Princess Royal, and Mark Phillips, and a nephew of King Charles III.
Born during the reign of his maternal grandmother Queen Elizabeth II, Phillips was fifth in the line of succession to the British throne; as of 2026, he is 19th.
Phillips attended the University of Exeter and later worked for Jaguar Racing.
In 2008, he married Canadian management consultant Autumn Kelly at St George's Chapel, Windsor Castle; they have two children.
Early life and education

Peter Mark Andrew Phillips was born at 10:46 am on 15 November 1977 at St Mary's Hospital, London.
He was the first child of Princess Anne and Mark Phillips, who had married in 1973, and the first grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
His godparents were his maternal uncle, Prince Charles; Geoffrey Tiarks; Captain Hamish Lochore; Lady Cecil Cameron of Lochiel and Jane Holderness-Roddam.
Phillips was fifth in line to the throne at birth and remained so until the birth of his cousin William, Prince of Wales in 1982.
His parents were said to have refused offers from his grandmother Queen Elizabeth II that would have led to his being born in the peerage.
Phillips was the first legitimate grandchild of a monarch in more than 500 years to be born without a title or courtesy title.
Phillips has a younger sister, Zara Tindall (née Phillips; born 1981), and two younger half-sisters, Felicity Wade (née Tonkin; born 1985), the daughter of Mark Phillips and his former mistress Heather Tonkin; and Stephanie Phillips (born 1997), the daughter from his father's second marriage to Sandy Pflueger.
Phillips went to Port Regis Prep School in Shaftesbury, Dorset before following some of his family by attending Gordonstoun School in Moray, Scotland.
Phillips represented Scotland at rugby union at youth and junior level in the mid-1990s.
Career

After his graduation in 2000, Phillips worked for Jaguar as corporate hospitality manager and then for Williams racing team, where he was sponsorship accounts manager.
He left Williams in September 2005, for a job as a manager at the Royal Bank of Scotland in Edinburgh.
In the year leading up to June 2016, Phillips was responsible for organising the "Patron's Lunch", in celebration of the Queen's 90th birthday.
In January 2020, Phillips appeared in an advertisement for Chinese company Bright Food.
In the video, he uses his status as a "British royal family member" to promote the company's milk, while surrounded by luxury.
Royal funeral participation

On 17 September 2022, during the period of official mourning for Queen Elizabeth II, Phillips joined his sister and six cousins to mount a 15-minute vigil around the coffin of their grandmother as it lay in state at Westminster Hall.
On 19 September 2022, he joined the Queen's children and other senior members of the royal family in walking behind the cortege in the state funeral procession.
Personal life

Relationships

Elizabeth Iorio and Tara Swain

Phillips dated Elizabeth Iorio, a cod liver oil heiress from the United States, for two years.
Autumn Kelly

In 2003, Phillips met Autumn Kelly, a Canadian management consultant, at the Formula 1 Canadian Grand Prix in Montreal.
If she had been Roman Catholic at the time of the marriage, Phillips would have lost his place in the line of the succession to the throne because of since-repealed terms of the Act of Settlement 1701.
Shortly before their wedding, the couple were interviewed and photographed by Hello! magazine, and were reported to have been paid £500,000, resulting in some concern in royal circles.
The couple lived in Hong Kong after Phillips changed positions within the Royal Bank of Scotland and became head of their sponsorships activities in the region.
Their first child, and the Queen's first great-grandchild, a daughter named Savannah Anne Kathleen, was born on 29 December 2010 at Gloucestershire Royal Hospital.
The Queen was present for the baby's baptism, which took place on 23 April 2011 at Church of the Holy Cross in Avening, Gloucestershire, near Gatcombe Park, the home of Phillips' mother.
On 29 March 2012, the couple's second daughter, Isla Elizabeth, was born at Gloucestershire Royal Hospital.
On 11 February 2020, Phillips and his wife confirmed that they had separated in 2019 and announced they were planning to divorce.
Lindsay Wallace

After his divorce, Phillips began a relationship with Lindsay Wallace in 2021, with whom he made his official debut as a couple at the Epsom Derby in June 2022.
Harriet Sperling

By June 2024, Phillips had introduced his partner, NHS paediatric nurse and freelance writer Harriet Sperling (née Sanders; born 1980), to King Charles III and Queen Camilla.
According to the BBC, Sperling is a distant relation of Prince Richard, Duke of Gloucester through her father Rupert Sanders (1946–2023).



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
  AssignClass (71968723-93f1-4a66-98d7-7b8f1e4df7a9)
 Call ID: 71968723-93f1-4a66-98d7-7b8f1e4df7a9
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (a0255858-c63c-4846-9a25-a3cb031f1143)
 Call ID: a0255858-c63c-4846-9a25-a3cb031f1143
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (973eef22-d255-4c05-bbc6-78149e38f580)
 Call ID: 973eef22-d255-4c05-bbc6-78149e38f580
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (d8e0956e-b60d-4914-9765-7c384b773739)
 Call ID: d8e0956e-b60d-4914-9765-7c384b773739
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (dd695bec-0dae-4724-a773-023d8cc2d0b8)
 Call ID: dd695bec-0dae-4724-a773-023d8cc2d0b8
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (4013e6c2-cd11-4801-84fb-126d69739f55)
 Call ID: 4013e6c2-cd11-4801-84fb-126d69739f55
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (627418e0-2c20-44ea-9fa3-d6c4f86aed35)
 Call ID: 627418e0-2c20-44ea-9fa3-d6c4f86aed35
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (02890ec9-0149-4b6f-bf5f-ad2127783a8a)
 Call ID: 02890ec9-0149-4b6f-bf5f-ad2127783a8a
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (3d275247-a620-433f-abdd-ee436af9169b)
 Call ID: 3d275247-a620-433f-abdd-ee436af9169b
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (187d0465-dca5-495d-9a58-9239f87e0e13)
 Call ID: 187d0465-dca5-495d-9a58-9239f87e0e13
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (3ae27802-5863-434c-a684-c40f45b181cc)
 Call ID: 3ae27802-5863-434c-a684-c40f45b181cc
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (26158a91-ec40-409b-9149-2f339e9c7eaf)
 Call ID: 26158a91-ec40-409b-9149-2f339e9c7eaf
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (2ac13dbf-234a-4079-982b-74a5bb17c6a9)
 Call ID: 2ac13dbf-234a-4079-982b-74a5bb17c6a9
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (a74b0987-24ff-4789-b519-460191cbcabb)
 Call ID: a74b0987-24ff-4789-b519-460191cbcabb
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (6e56200e-6967-4754-a648-1e7a97d7d792)
 Call ID: 6e56200e-6967-4754-a648-1e7a97d7d792
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (8df34c93-b36c-4133-84c0-9db730727d4a)
 Call ID: 8df34c93-b36c-4133-84c0-9db730727d4a
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (c2e31101-3d38-497e-a672-9e430b734978)
 Call ID: c2e31101-3d38-497e-a672-9e430b734978
  Args:
    type: :Man
    source: Rupert_Sanders
  AddLiteral (198048a7-41f3-46c8-a63f-e178c7f33520)
 Call ID: 198048a7-41f3-46c8-a63f-e178c7f33520
  Args:
    literal_value: 1977
    source: Peter_Phillips
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (393b2630-6572-4b11-932a-089cf84d8577)
 Call ID: 393b2630-6572-4b11-932a-089cf84d8577
  Args:
    relation: :hasMother
    target: Anne_Princess_Royal
    source: Peter_Phillips
  AddTriple (8ecf274d-6baf-48aa-9034-43d217c6bef0)
 Call ID: 8ecf274d-6baf-48aa-9034-43d217c6bef0
  Args:
    relation: :hasFather
    source: Peter_Phillips
    target: Mark_Phillips
  AddTriple (3d0e7ade-52d6-4554-a51b-11ccf00103bf)
 Call ID: 3d0e7ade-52d6-4554-a51b-11ccf00103bf
  Args:
    relation: :hasMother
    target: Queen_Elizabeth_II
    source: Anne_Princess_Royal
  AddTriple (0f9ecf28-dc80-4ab4-ae11-7fbf82c63140)
 Call ID: 0f9ecf28-dc80-4ab4-ae11-7fbf82c63140
  Args:
    source: Anne_Princess_Royal
    target: Prince_Philip
    relation: :hasFather
  AddTriple (89d60cdf-5161-460e-adce-314c425f70fa)
 Call ID: 89d60cdf-5161-460e-adce-314c425f70fa
  Args:
    relation: :hasMother
    source: Zara_Tindall
    target: Anne_Princess_Royal
  AddTriple (f4a4708c-8038-40ba-ac59-7ae387f34d4e)
 Call ID: f4a4708c-8038-40ba-ac59-7ae387f34d4e
  Args:
    relation: :hasFather
    source: Zara_Tindall
    target: Mark_Phillips
  AddTriple (160d2d5f-89d4-4b3f-b8a1-18dc2220726c)
 Call ID: 160d2d5f-89d4-4b3f-b8a1-18dc2220726c
  Args:
    source: Felicity_Wade
    target: Heather_Tonkin
    relation: :hasMother
  AddTriple (e251121d-65e2-47be-a3aa-abe6ca8e8a9f)
 Call ID: e251121d-65e2-47be-a3aa-abe6ca8e8a9f
  Args:
    target: Mark_Phillips
    source: Felicity_Wade
    relation: :hasFather
  AddTriple (896bac46-d7c7-49f8-8d55-7f9a07b306e3)
 Call ID: 896bac46-d7c7-49f8-8d55-7f9a07b306e3
  Args:
    relation: :hasMother
    target: Sandy_Pflueger
    source: Stephanie_Phillips
  AddTriple (27dcd1d6-fadd-4d5f-8ae4-d8a8c958a8d3)
 Call ID: 27dcd1d6-fadd-4d5f-8ae4-d8a8c958a8d3
  Args:
    relation: :hasFather
    source: Stephanie_Phillips
    target: Mark_Phillips
  AddTriple (437c0176-de4e-41b5-8959-f34307ba0052)
 Call ID: 437c0176-de4e-41b5-8959-f34307ba0052
  Args:
    relation: :hasMother
    source: Savannah_Phillips
    target: Autumn_Kelly
  AddTriple (b99cd8ae-f36d-4f11-94e7-664dc3fc9880)
 Call ID: b99cd8ae-f36d-4f11-94e7-664dc3fc9880
  Args:
    source: Savannah_Phillips
    target: Peter_Phillips
    relation: :hasFather
  AddTriple (2af4475d-c3f7-46bf-ae70-22643638302f)
 Call ID: 2af4475d-c3f7-46bf-ae70-22643638302f
  Args:
    source: Isla_Phillips
    target: Autumn_Kelly
    relation: :hasMother
  AddTriple (91d393a5-e87d-4256-9fcc-c86dc38131bc)
 Call ID: 91d393a5-e87d-4256-9fcc-c86dc38131bc
  Args:
    relation: :hasFather
    source: Isla_Phillips
    target: Peter_Phillips
  AddLiteral (ded91141-370d-4fa4-ab8b-71c7e28700fd)
 Call ID: ded91141-370d-4fa4-ab8b-71c7e28700fd
  Args:
    literal_type: xsd:integer
    source: Zara_Tindall
    literal_value: 1981
    relation: :hasBirthYear
  AddLiteral (8cde3714-35d8-4ca2-994a-ac6e4def73ec)
 Call ID: 8cde3714-35d8-4ca2-994a-ac6e4def73ec
  Args:
    literal_value: 1985
    source: Felicity_Wade
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (56902b8f-8634-4b0b-9e3d-07f1ee19b8e3)
 Call ID: 56902b8f-8634-4b0b-9e3d-07f1ee19b8e3
  Args:
    source: Stephanie_Phillips
    literal_type: xsd:integer
    literal_value: 1997
    relation: :hasBirthYear
  AddLiteral (d7e1fc2f-b61a-449c-8752-2e27cd43e2ee)
 Call ID: d7e1fc2f-b61a-449c-8752-2e27cd43e2ee
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Savannah_Phillips
    literal_value: 2010
  AddLiteral (acbfde09-82c2-4bd4-b161-e96109b16ba4)
 Call ID: acbfde09-82c2-4bd4-b161-e96109b16ba4
  Args:
    literal_type: xsd:integer
    source: Isla_Phillips
    literal_value: 2012
    relation: :hasBirthYear
  AddLiteral (513b67da-34a0-4340-a006-423d1ab60f9b)
 Call ID: 513b67da-34a0-4340-a006-423d1ab60f9b
  Args:
    relation: :hasBirthYear
    literal_value: 1980
    literal_type: xsd:integer
    source: Harriet_Sperling
  AddLiteral (4a680a19-2c82-4cf9-a49f-f903a68bfde6)
 Call ID: 4a680a19-2c82-4cf9-a49f-f903a68bfde6
  Args:
    relation: :hasDeathYear
    literal_value: 2023
    source: Rupert_Sanders
    literal_type: xsd:integer
  AddTriple (41ff5557-6ec7-434b-bc83-24846fa999f5)
 Call ID: 41ff5557-6ec7-434b-bc83-24846fa999f5
  Args:
    relation: :hasFather
    source: Harriet_Sperling
    target: Rupert_Sanders
  Finish (77404fbc-57c5-4513-abe6-cb476e6c728d)
 Call ID: 77404fbc-57c5-4513-abe6-cb476e6c728d
  Args: