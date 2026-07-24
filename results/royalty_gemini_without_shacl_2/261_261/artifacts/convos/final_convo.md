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
He was baptised on 22 December by the Archbishop of Canterbury Donald Coggan in the Music Room of Buckingham Palace.
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
Savannah was born 12th in the line to the throne and is now 20th.
On 29 March 2012, the couple's second daughter, Isla Elizabeth, was born at Gloucestershire Royal Hospital.
She was born 13th in the line to the throne and is now 21st.
On 11 February 2020, Phillips and his wife confirmed that they had separated in 2019 and announced they were planning to divorce.
Lindsay Wallace

After his divorce, Phillips began a relationship with Lindsay Wallace in 2021, with whom he made his official debut as a couple at the Epsom Derby in June 2022.
Harriet Sperling

By June 2024, Phillips had introduced his partner, NHS paediatric nurse and freelance writer Harriet Sperling (née Sanders; born 1980), to King Charles III and Queen Camilla.
According to the BBC, Sperling is a distant relation of Prince Richard, Duke of Gloucester through her father Rupert Sanders (1946–2023).



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
  AssignClass (18a82f5e-7914-48f8-bd27-fca339d1f7c6)
 Call ID: 18a82f5e-7914-48f8-bd27-fca339d1f7c6
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (4b31a15e-d248-46bd-84c5-bcb6a2e4fafc)
 Call ID: 4b31a15e-d248-46bd-84c5-bcb6a2e4fafc
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (b02117ce-37f4-4184-b874-bb8a85550fa0)
 Call ID: b02117ce-37f4-4184-b874-bb8a85550fa0
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (58f4ee05-499c-441a-9050-6f7b54d9cb5a)
 Call ID: 58f4ee05-499c-441a-9050-6f7b54d9cb5a
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (d0b6f8bf-f141-4a3a-b9e0-cd60596383f5)
 Call ID: d0b6f8bf-f141-4a3a-b9e0-cd60596383f5
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (0203da84-2f3c-4ded-b11f-c5f50c0b938d)
 Call ID: 0203da84-2f3c-4ded-b11f-c5f50c0b938d
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (6cdfcb03-e5a1-484d-b200-6bd5b768fa1a)
 Call ID: 6cdfcb03-e5a1-484d-b200-6bd5b768fa1a
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (553dfde5-31a0-42dc-a67f-752448316084)
 Call ID: 553dfde5-31a0-42dc-a67f-752448316084
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (b8d0ce83-30fd-43ba-9c61-d0eb79ed34e0)
 Call ID: b8d0ce83-30fd-43ba-9c61-d0eb79ed34e0
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (9030f2de-011b-46ef-bdb3-ddff2c49bb0b)
 Call ID: 9030f2de-011b-46ef-bdb3-ddff2c49bb0b
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (145bc64c-3bd6-4c62-9c6f-8d4ff4436016)
 Call ID: 145bc64c-3bd6-4c62-9c6f-8d4ff4436016
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (21af3287-ad42-4bdf-8246-4ad93675533f)
 Call ID: 21af3287-ad42-4bdf-8246-4ad93675533f
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (8b69a764-5b75-4a23-bdfd-f738744d3911)
 Call ID: 8b69a764-5b75-4a23-bdfd-f738744d3911
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (d8e11879-3640-4f32-8dd7-8d3f8fea26fa)
 Call ID: d8e11879-3640-4f32-8dd7-8d3f8fea26fa
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (0151bce7-ac2f-4db0-b94a-a19ddcde8e1a)
 Call ID: 0151bce7-ac2f-4db0-b94a-a19ddcde8e1a
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (ecf58e1a-e279-464e-ad9b-1e25b391d1da)
 Call ID: ecf58e1a-e279-464e-ad9b-1e25b391d1da
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (8c34bfbc-76ad-4439-8d20-ee122396deda)
 Call ID: 8c34bfbc-76ad-4439-8d20-ee122396deda
  Args:
    type: :Man
    source: Rupert_Sanders
  AssignClass (170ea35d-9e62-4582-93f8-9fb964c90e58)
 Call ID: 170ea35d-9e62-4582-93f8-9fb964c90e58
  Args:
    type: :Man
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (55e88d17-265f-4269-9bbc-5b0dde7bb2b7)
 Call ID: 55e88d17-265f-4269-9bbc-5b0dde7bb2b7
  Args:
    type: :Woman
    source: Queen_Camilla
  AddLiteral (de964d48-089b-4cdc-9e5b-8d4ae7e8042f)
 Call ID: de964d48-089b-4cdc-9e5b-8d4ae7e8042f
  Args:
    literal_value: 1977
    source: Peter_Phillips
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (df71aa7d-42ab-4bab-8ded-9d1f7fb7c930)
 Call ID: df71aa7d-42ab-4bab-8ded-9d1f7fb7c930
  Args:
    literal_value: 1981
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Zara_Tindall
  AddLiteral (a9b28d81-c82e-4d49-b238-175dd70e517a)
 Call ID: a9b28d81-c82e-4d49-b238-175dd70e517a
  Args:
    source: Felicity_Wade
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1985
  AddLiteral (9348c132-c144-431e-8112-2ce9600657da)
 Call ID: 9348c132-c144-431e-8112-2ce9600657da
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Stephanie_Phillips
    literal_value: 1997
  AddLiteral (39205255-d1de-4529-9bad-de55f0c00437)
 Call ID: 39205255-d1de-4529-9bad-de55f0c00437
  Args:
    literal_value: 1980
    source: Harriet_Sperling
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (50272c9f-388f-40dc-8ea7-9f36f0f72580)
 Call ID: 50272c9f-388f-40dc-8ea7-9f36f0f72580
  Args:
    literal_value: 2023
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Rupert_Sanders
  AddTriple (104829d1-3222-4cee-a786-413dbb26dd41)
 Call ID: 104829d1-3222-4cee-a786-413dbb26dd41
  Args:
    source: Peter_Phillips
    relation: :hasMother
    target: Anne_Princess_Royal
  AddTriple (f1558b5f-6523-448c-a360-c2f39cac717f)
 Call ID: f1558b5f-6523-448c-a360-c2f39cac717f
  Args:
    relation: :hasFather
    source: Peter_Phillips
    target: Mark_Phillips
  AddTriple (d32f16ee-1dce-4899-aaa6-f3f8e59033a6)
 Call ID: d32f16ee-1dce-4899-aaa6-f3f8e59033a6
  Args:
    relation: :hasMother
    source: Zara_Tindall
    target: Anne_Princess_Royal
  AddTriple (f50747c8-7706-45fa-b068-7936fbcdf815)
 Call ID: f50747c8-7706-45fa-b068-7936fbcdf815
  Args:
    source: Zara_Tindall
    relation: :hasFather
    target: Mark_Phillips
  AddTriple (ea7729df-0850-45d1-aeb6-e98c9c1b2287)
 Call ID: ea7729df-0850-45d1-aeb6-e98c9c1b2287
  Args:
    target: Heather_Tonkin
    relation: :hasMother
    source: Felicity_Wade
  AddTriple (01b77bcd-1bd0-42c4-a529-7eb16a71861b)
 Call ID: 01b77bcd-1bd0-42c4-a529-7eb16a71861b
  Args:
    target: Mark_Phillips
    source: Felicity_Wade
    relation: :hasFather
  AddTriple (4f2ffcfc-fcf1-4ba2-ae75-38a97e0fa234)
 Call ID: 4f2ffcfc-fcf1-4ba2-ae75-38a97e0fa234
  Args:
    target: Sandy_Pflueger
    source: Stephanie_Phillips
    relation: :hasMother
  AddTriple (2751612b-b6a7-45ad-b5c7-deb1a02a074b)
 Call ID: 2751612b-b6a7-45ad-b5c7-deb1a02a074b
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Stephanie_Phillips
  AddTriple (66c8da9a-9c09-4c55-b844-4d73fe042b55)
 Call ID: 66c8da9a-9c09-4c55-b844-4d73fe042b55
  Args:
    source: Anne_Princess_Royal
    relation: :hasMother
    target: Queen_Elizabeth_II
  AddTriple (2d055137-2fe7-48f5-9654-d6b653b5db86)
 Call ID: 2d055137-2fe7-48f5-9654-d6b653b5db86
  Args:
    relation: :hasFather
    source: Anne_Princess_Royal
    target: Prince_Philip
  AddTriple (36aa3e07-d22f-45e8-b8ed-8b5748c31b98)
 Call ID: 36aa3e07-d22f-45e8-b8ed-8b5748c31b98
  Args:
    source: Anne_Princess_Royal
    relation: :hasChild
    target: Peter_Phillips
  AddTriple (6e523dcd-a4f9-4a60-a90a-1ab0e1596426)
 Call ID: 6e523dcd-a4f9-4a60-a90a-1ab0e1596426
  Args:
    relation: :hasChild
    source: Mark_Phillips
    target: Peter_Phillips
  AddTriple (7fe808ea-8a35-41d7-a86f-5803e5c2b378)
 Call ID: 7fe808ea-8a35-41d7-a86f-5803e5c2b378
  Args:
    target: Zara_Tindall
    source: Anne_Princess_Royal
    relation: :hasChild
  AddTriple (4103329c-fb38-4896-bb98-41dea9a75257)
 Call ID: 4103329c-fb38-4896-bb98-41dea9a75257
  Args:
    relation: :hasChild
    source: Mark_Phillips
    target: Zara_Tindall
  AddTriple (1a2ea333-807a-4be3-99f8-2e91e45a376b)
 Call ID: 1a2ea333-807a-4be3-99f8-2e91e45a376b
  Args:
    source: Mark_Phillips
    relation: :hasChild
    target: Felicity_Wade
  AddTriple (b9fc24f3-5a61-4b36-afa4-384496e0688b)
 Call ID: b9fc24f3-5a61-4b36-afa4-384496e0688b
  Args:
    source: Heather_Tonkin
    relation: :hasChild
    target: Felicity_Wade
  AddTriple (b5b25a53-78ba-4506-920c-1fd087197f3c)
 Call ID: b5b25a53-78ba-4506-920c-1fd087197f3c
  Args:
    relation: :hasChild
    source: Mark_Phillips
    target: Stephanie_Phillips
  AddTriple (683cc30e-35f4-440e-a0c0-17c45b247c2e)
 Call ID: 683cc30e-35f4-440e-a0c0-17c45b247c2e
  Args:
    target: Stephanie_Phillips
    relation: :hasChild
    source: Sandy_Pflueger
  AddTriple (081165f3-c9d0-42f7-a2a9-879c9c38f4a7)
 Call ID: 081165f3-c9d0-42f7-a2a9-879c9c38f4a7
  Args:
    target: Anne_Princess_Royal
    source: Queen_Elizabeth_II
    relation: :hasChild
  AddTriple (ba14c87d-59d0-4848-a2a9-ff7399edb44f)
 Call ID: ba14c87d-59d0-4848-a2a9-ff7399edb44f
  Args:
    source: Prince_Philip
    relation: :hasChild
    target: Anne_Princess_Royal
  AddTriple (c2c4eead-2185-4e88-a2c1-8ac74a4037d5)
 Call ID: c2c4eead-2185-4e88-a2c1-8ac74a4037d5
  Args:
    relation: :hasChild
    source: Queen_Elizabeth_II
    target: King_Charles_III
  AddTriple (295fd1df-86d8-4a3f-a222-a16a610d51fe)
 Call ID: 295fd1df-86d8-4a3f-a222-a16a610d51fe
  Args:
    source: Prince_Philip
    relation: :hasChild
    target: King_Charles_III
  AddTriple (30876663-ff4d-4046-8eef-08dd117cb6de)
 Call ID: 30876663-ff4d-4046-8eef-08dd117cb6de
  Args:
    relation: :hasMother
    source: King_Charles_III
    target: Queen_Elizabeth_II
  AddTriple (67ffa795-111b-4cc4-a103-2cb3898663d5)
 Call ID: 67ffa795-111b-4cc4-a103-2cb3898663d5
  Args:
    relation: :hasFather
    source: King_Charles_III
    target: Prince_Philip
  AddTriple (b3869233-e93f-44ad-a2d4-eea2e30fae92)
 Call ID: b3869233-e93f-44ad-a2d4-eea2e30fae92
  Args:
    source: Rupert_Sanders
    relation: :hasChild
    target: Harriet_Sperling
  AddTriple (34e033b7-8b8d-4919-a6c5-a9b76e3cf6c1)
 Call ID: 34e033b7-8b8d-4919-a6c5-a9b76e3cf6c1
  Args:
    target: Rupert_Sanders
    source: Harriet_Sperling
    relation: :hasFather
  AddTriple (cfe52d39-9f67-4f5d-9340-c167f7f6646b)
 Call ID: cfe52d39-9f67-4f5d-9340-c167f7f6646b
  Args:
    target: Savannah_Phillips
    relation: :hasChild
    source: Peter_Phillips
  AddTriple (3c15b467-c2f0-4e2e-8b4a-ad5630abfdc1)
 Call ID: 3c15b467-c2f0-4e2e-8b4a-ad5630abfdc1
  Args:
    relation: :hasChild
    source: Peter_Phillips
    target: Isla_Phillips
  AddTriple (bf9ac6ea-caca-426e-a841-ab34ab67312c)
 Call ID: bf9ac6ea-caca-426e-a841-ab34ab67312c
  Args:
    target: Autumn_Kelly
    relation: :hasMother
    source: Savannah_Phillips
  AddTriple (693586c5-d6e3-4e2b-8f86-10ff18bcdb3a)
 Call ID: 693586c5-d6e3-4e2b-8f86-10ff18bcdb3a
  Args:
    target: Autumn_Kelly
    source: Isla_Phillips
    relation: :hasMother
  AddTriple (f04a03fc-a124-40a7-b93d-ab1604dbbb33)
 Call ID: f04a03fc-a124-40a7-b93d-ab1604dbbb33
  Args:
    relation: :hasFather
    source: Savannah_Phillips
    target: Peter_Phillips
  AddTriple (e1d8ab8c-aa8c-420d-b144-8818611afa16)
 Call ID: e1d8ab8c-aa8c-420d-b144-8818611afa16
  Args:
    target: Peter_Phillips
    relation: :hasFather
    source: Isla_Phillips
  AddTriple (2d6f69ee-48ad-499e-be02-81d7a017a843)
 Call ID: 2d6f69ee-48ad-499e-be02-81d7a017a843
  Args:
    relation: :hasChild
    source: Autumn_Kelly
    target: Savannah_Phillips
  AddTriple (c98619f0-5e7a-4110-9969-7a905e9db376)
 Call ID: c98619f0-5e7a-4110-9969-7a905e9db376
  Args:
    source: Autumn_Kelly
    relation: :hasChild
    target: Isla_Phillips
  Finish (f7231b65-1d01-46f2-b241-6ed71b5ef1c9)
 Call ID: f7231b65-1d01-46f2-b241-6ed71b5ef1c9
  Args: