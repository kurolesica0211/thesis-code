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
  AssignClass (cc016424-5559-4078-b684-b247b0372f63)
 Call ID: cc016424-5559-4078-b684-b247b0372f63
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (7ed9173f-5557-454b-b224-cda8cf597d96)
 Call ID: 7ed9173f-5557-454b-b224-cda8cf597d96
  Args:
    source: Peter_Phillips
    type: :Person
  AddLiteral (9ec0aee5-28bc-4863-b960-b1a0ed9c0cb5)
 Call ID: 9ec0aee5-28bc-4863-b960-b1a0ed9c0cb5
  Args:
    literal_value: 1977
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Peter_Phillips
  AssignClass (52aff0e8-8fcd-4f34-8d27-11247c69598b)
 Call ID: 52aff0e8-8fcd-4f34-8d27-11247c69598b
  Args:
    source: Anne_Princess_Royal
    type: :Woman
  AssignClass (f0f9c7cd-eb40-43b9-8cef-579195d33f1a)
 Call ID: f0f9c7cd-eb40-43b9-8cef-579195d33f1a
  Args:
    source: Anne_Princess_Royal
    type: :Person
  AssignClass (8e8fa7be-ec5c-4161-bdce-3aaf22b95cdb)
 Call ID: 8e8fa7be-ec5c-4161-bdce-3aaf22b95cdb
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (7f62f3fe-f013-4b01-962f-6032bafbfaad)
 Call ID: 7f62f3fe-f013-4b01-962f-6032bafbfaad
  Args:
    source: Mark_Phillips
    type: :Person
  AddTriple (e62560db-2857-46c4-b49c-44e1c94ecd45)
 Call ID: e62560db-2857-46c4-b49c-44e1c94ecd45
  Args:
    relation: :hasMother
    target: Anne_Princess_Royal
    source: Peter_Phillips
  AddTriple (55ad9501-a06a-49f3-8d79-21743598ad0e)
 Call ID: 55ad9501-a06a-49f3-8d79-21743598ad0e
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Peter_Phillips
  AssignClass (04011a64-99bb-4f86-accf-a4ac4fa15024)
 Call ID: 04011a64-99bb-4f86-accf-a4ac4fa15024
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (76c5f2ab-ce0f-4fc9-beaa-d8f08b2c1b33)
 Call ID: 76c5f2ab-ce0f-4fc9-beaa-d8f08b2c1b33
  Args:
    type: :Person
    source: King_Charles_III
  AddTriple (159d105a-bad3-4377-9405-cd010cc892eb)
 Call ID: 159d105a-bad3-4377-9405-cd010cc892eb
  Args:
    source: Peter_Phillips
    target: King_Charles_III
    relation: :hasRelation
  AssignClass (e706955a-bc79-47be-95cb-1e8ca2776d45)
 Call ID: e706955a-bc79-47be-95cb-1e8ca2776d45
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (3a307674-d490-48e3-8e6f-ebed285c5d16)
 Call ID: 3a307674-d490-48e3-8e6f-ebed285c5d16
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AddTriple (e3e36b32-e9c4-4675-a29b-9b88b944d325)
 Call ID: e3e36b32-e9c4-4675-a29b-9b88b944d325
  Args:
    source: Queen_Elizabeth_II
    target: Anne_Princess_Royal
    relation: :isMotherOf
  AssignClass (93f930ef-3907-42d8-aa3f-60f30698e8d4)
 Call ID: 93f930ef-3907-42d8-aa3f-60f30698e8d4
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (88ff903a-17a8-4166-a766-e5996745bc1f)
 Call ID: 88ff903a-17a8-4166-a766-e5996745bc1f
  Args:
    type: :Person
    source: Prince_Philip
  AddTriple (2ce9d566-d46f-4fad-af81-e1c24c052eb1)
 Call ID: 2ce9d566-d46f-4fad-af81-e1c24c052eb1
  Args:
    relation: :hasFather
    target: Prince_Philip
    source: Anne_Princess_Royal
  AddTriple (15f6b3b7-fe02-46e6-8ea8-1ab44793f32d)
 Call ID: 15f6b3b7-fe02-46e6-8ea8-1ab44793f32d
  Args:
    relation: :hasMother
    target: Queen_Elizabeth_II
    source: Anne_Princess_Royal
  AssignClass (304a33e0-0122-4d7a-a0a8-4ebbbe33b3b8)
 Call ID: 304a33e0-0122-4d7a-a0a8-4ebbbe33b3b8
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (5ab805cc-87cb-4c4c-ac39-94fc003e2243)
 Call ID: 5ab805cc-87cb-4c4c-ac39-94fc003e2243
  Args:
    type: :Person
    source: Zara_Tindall
  AddTriple (4d4dd958-e906-4e95-a3ba-bfe698a8c2c5)
 Call ID: 4d4dd958-e906-4e95-a3ba-bfe698a8c2c5
  Args:
    target: Zara_Tindall
    relation: :hasSister
    source: Peter_Phillips
  AddTriple (f8bbe69e-9695-4cd8-8dd8-1543445919c4)
 Call ID: f8bbe69e-9695-4cd8-8dd8-1543445919c4
  Args:
    relation: :hasMother
    target: Anne_Princess_Royal
    source: Zara_Tindall
  AddTriple (dc4561fd-5124-49f0-aea8-662c0663df13)
 Call ID: dc4561fd-5124-49f0-aea8-662c0663df13
  Args:
    source: Zara_Tindall
    relation: :hasFather
    target: Mark_Phillips
  AssignClass (bb622988-1276-4ab3-9ef1-942fe3b58bc2)
 Call ID: bb622988-1276-4ab3-9ef1-942fe3b58bc2
  Args:
    source: Felicity_Wade
    type: :Woman
  AssignClass (286116ef-36f1-4c10-8aa9-2e89d2c9fff9)
 Call ID: 286116ef-36f1-4c10-8aa9-2e89d2c9fff9
  Args:
    type: :Person
    source: Felicity_Wade
  AddTriple (7e19aec2-dabe-4728-a3be-2b09ddd7fef3)
 Call ID: 7e19aec2-dabe-4728-a3be-2b09ddd7fef3
  Args:
    source: Felicity_Wade
    target: Mark_Phillips
    relation: :hasFather
  AssignClass (56ccbd1c-951e-4a73-aeb1-21e03534ef1c)
 Call ID: 56ccbd1c-951e-4a73-aeb1-21e03534ef1c
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (345fac74-9db9-4460-b1f1-beeff643ce54)
 Call ID: 345fac74-9db9-4460-b1f1-beeff643ce54
  Args:
    type: :Person
    source: Heather_Tonkin
  AddTriple (599e37e6-d581-40a3-a8b5-22e45f547cf5)
 Call ID: 599e37e6-d581-40a3-a8b5-22e45f547cf5
  Args:
    relation: :hasMother
    target: Heather_Tonkin
    source: Felicity_Wade
  AssignClass (22bb58aa-d15c-4098-b787-e56daf7488a1)
 Call ID: 22bb58aa-d15c-4098-b787-e56daf7488a1
  Args:
    source: Stephanie_Phillips
    type: :Woman
  AssignClass (fc877974-6058-44c0-81d7-23d39be55087)
 Call ID: fc877974-6058-44c0-81d7-23d39be55087
  Args:
    type: :Person
    source: Stephanie_Phillips
  AddTriple (62e7ac54-c6e9-413c-a021-9c6243a44037)
 Call ID: 62e7ac54-c6e9-413c-a021-9c6243a44037
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Stephanie_Phillips
  AssignClass (fd665192-94e7-438f-92d2-32ef9cd9e5c0)
 Call ID: fd665192-94e7-438f-92d2-32ef9cd9e5c0
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (92024037-226b-4cdc-9882-aadc75117480)
 Call ID: 92024037-226b-4cdc-9882-aadc75117480
  Args:
    source: Sandy_Pflueger
    type: :Person
  AddTriple (043ec5f3-0ce4-4acb-a9d5-2e9dbc6c6c34)
 Call ID: 043ec5f3-0ce4-4acb-a9d5-2e9dbc6c6c34
  Args:
    relation: :hasMother
    target: Sandy_Pflueger
    source: Stephanie_Phillips
  AssignClass (fb480182-2da8-45df-899a-36cf000c01ec)
 Call ID: fb480182-2da8-45df-899a-36cf000c01ec
  Args:
    source: Autumn_Kelly
    type: :Woman
  AssignClass (d21040b2-2ee5-456a-bca7-b45a36e52b57)
 Call ID: d21040b2-2ee5-456a-bca7-b45a36e52b57
  Args:
    type: :Person
    source: Autumn_Kelly
  AddTriple (996e164c-1a89-44e3-ba55-43c0d7fbe2b0)
 Call ID: 996e164c-1a89-44e3-ba55-43c0d7fbe2b0
  Args:
    target: Autumn_Kelly
    relation: :hasRelation
    source: Peter_Phillips
  AddLiteral (25fb8750-e740-420e-b406-0f60e6438c3a)
 Call ID: 25fb8750-e740-420e-b406-0f60e6438c3a
  Args:
    literal_value: 2008
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Peter_Phillips
  AssignClass (8b590574-4a57-44b3-bbe0-d62acbeefedf)
 Call ID: 8b590574-4a57-44b3-bbe0-d62acbeefedf
  Args:
    source: Savannah_Anne_Kathleen
    type: :Woman
  AssignClass (03b7b2d7-e500-48c4-851c-6aacdb1451b8)
 Call ID: 03b7b2d7-e500-48c4-851c-6aacdb1451b8
  Args:
    type: :Person
    source: Savannah_Anne_Kathleen
  AddTriple (d2dc38ca-e1bd-421f-a69b-2a81986f4e51)
 Call ID: d2dc38ca-e1bd-421f-a69b-2a81986f4e51
  Args:
    source: Savannah_Anne_Kathleen
    relation: :hasMother
    target: Autumn_Kelly
  AddTriple (60bea8fc-a50e-432b-ac49-7caef4a28143)
 Call ID: 60bea8fc-a50e-432b-ac49-7caef4a28143
  Args:
    relation: :hasFather
    target: Peter_Phillips
    source: Savannah_Anne_Kathleen
  AssignClass (75b4a507-1ce0-4254-a1b0-fb06c603e5c2)
 Call ID: 75b4a507-1ce0-4254-a1b0-fb06c603e5c2
  Args:
    source: Isla_Elizabeth
    type: :Woman
  AssignClass (5d731640-1990-41bb-bc1f-5814117a4574)
 Call ID: 5d731640-1990-41bb-bc1f-5814117a4574
  Args:
    type: :Person
    source: Isla_Elizabeth
  AddTriple (14c2917e-c65b-4204-b044-bd921078f9bf)
 Call ID: 14c2917e-c65b-4204-b044-bd921078f9bf
  Args:
    source: Isla_Elizabeth
    relation: :hasMother
    target: Autumn_Kelly
  AddTriple (a90ca83a-6cd5-44da-95f8-559b8458d08b)
 Call ID: a90ca83a-6cd5-44da-95f8-559b8458d08b
  Args:
    source: Isla_Elizabeth
    relation: :hasFather
    target: Peter_Phillips
  AssignClass (26170075-b4f9-4ed1-b24d-4ea5b5c8af94)
 Call ID: 26170075-b4f9-4ed1-b24d-4ea5b5c8af94
  Args:
    source: Lindsay_Wallace
    type: :Woman
  AssignClass (1022b4c8-8f87-4d27-93b5-e13ed93c7783)
 Call ID: 1022b4c8-8f87-4d27-93b5-e13ed93c7783
  Args:
    source: Lindsay_Wallace
    type: :Person
  AddTriple (62051d4e-e207-49d5-8e27-f31fdcbd0039)
 Call ID: 62051d4e-e207-49d5-8e27-f31fdcbd0039
  Args:
    source: Peter_Phillips
    target: Lindsay_Wallace
    relation: :hasRelation
  AssignClass (e537c3cd-7393-43e3-b156-7a33d5b7cd74)
 Call ID: e537c3cd-7393-43e3-b156-7a33d5b7cd74
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (4cf92171-32d8-49fa-a111-ee1869da8759)
 Call ID: 4cf92171-32d8-49fa-a111-ee1869da8759
  Args:
    source: Harriet_Sperling
    type: :Person
  AddTriple (59c10b65-9b82-4c07-877f-5a8ac2d156a7)
 Call ID: 59c10b65-9b82-4c07-877f-5a8ac2d156a7
  Args:
    source: Peter_Phillips
    relation: :hasRelation
    target: Harriet_Sperling
  AssignClass (de93a968-6cd6-4c97-b8c2-ed7868dc9d28)
 Call ID: de93a968-6cd6-4c97-b8c2-ed7868dc9d28
  Args:
    source: Rupert_Sanders
    type: :Man
  AssignClass (844c4f8a-bf5e-480d-9ec2-f1a94ca0baf8)
 Call ID: 844c4f8a-bf5e-480d-9ec2-f1a94ca0baf8
  Args:
    type: :Person
    source: Rupert_Sanders
  AddTriple (d04f1e3a-e387-4b2f-a66d-6220a6b7b18d)
 Call ID: d04f1e3a-e387-4b2f-a66d-6220a6b7b18d
  Args:
    source: Harriet_Sperling
    relation: :hasFather
    target: Rupert_Sanders
  Finish (a81eb1b6-96da-4c4a-a3a9-70d6f63a6d92)
 Call ID: a81eb1b6-96da-4c4a-a3a9-70d6f63a6d92
  Args: