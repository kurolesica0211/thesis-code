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
  AssignClass (e3014185-7345-455d-adf0-20dcc9f0d96e)
 Call ID: e3014185-7345-455d-adf0-20dcc9f0d96e
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (a7a8f390-179a-4de7-9f17-470f8f4057fc)
 Call ID: a7a8f390-179a-4de7-9f17-470f8f4057fc
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (175a741c-8ef5-492f-a298-9fa4bf81e3bd)
 Call ID: 175a741c-8ef5-492f-a298-9fa4bf81e3bd
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (acb9f5e0-a496-4091-80ca-6cfa43cac28c)
 Call ID: acb9f5e0-a496-4091-80ca-6cfa43cac28c
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (47cc9a53-b4a2-429d-996c-d9487231fa8d)
 Call ID: 47cc9a53-b4a2-429d-996c-d9487231fa8d
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (36bcb2f1-0e82-46e8-b125-7f12e6db9784)
 Call ID: 36bcb2f1-0e82-46e8-b125-7f12e6db9784
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (61c87b22-7f34-4c2e-b8e4-3b2cab5af67e)
 Call ID: 61c87b22-7f34-4c2e-b8e4-3b2cab5af67e
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (87b2146d-e37f-4ff7-851d-4f16e168e428)
 Call ID: 87b2146d-e37f-4ff7-851d-4f16e168e428
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (9ef2245e-9cad-4097-9da1-661522f61e06)
 Call ID: 9ef2245e-9cad-4097-9da1-661522f61e06
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (d1b5f34d-16f9-4826-ac4e-d7fb35b821bb)
 Call ID: d1b5f34d-16f9-4826-ac4e-d7fb35b821bb
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (48e74aae-1756-46eb-810b-7e422457ea2d)
 Call ID: 48e74aae-1756-46eb-810b-7e422457ea2d
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (12a00c4f-154e-4f20-a9cb-1eabce92505d)
 Call ID: 12a00c4f-154e-4f20-a9cb-1eabce92505d
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (3c67c36d-ccd1-4102-80c2-c75e2accf8d6)
 Call ID: 3c67c36d-ccd1-4102-80c2-c75e2accf8d6
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (94353d75-bde9-4a35-877d-ee2ff236a00a)
 Call ID: 94353d75-bde9-4a35-877d-ee2ff236a00a
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (882b7062-5d97-4183-8160-7c32691300de)
 Call ID: 882b7062-5d97-4183-8160-7c32691300de
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (d4a7d97f-26fb-46b6-bafb-554c37cc543f)
 Call ID: d4a7d97f-26fb-46b6-bafb-554c37cc543f
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (3a86cbb3-3f8f-4703-9737-a7f76af6624c)
 Call ID: 3a86cbb3-3f8f-4703-9737-a7f76af6624c
  Args:
    type: :Man
    source: Rupert_Sanders
  AssignClass (8b598881-20c3-40c2-b6db-bffc6573e38f)
 Call ID: 8b598881-20c3-40c2-b6db-bffc6573e38f
  Args:
    type: :Man
    source: Prince_Richard_Duke_of_Gloucester
  AddLiteral (d5c53ebd-bcdb-48ee-b7a6-dec2dbc5719f)
 Call ID: d5c53ebd-bcdb-48ee-b7a6-dec2dbc5719f
  Args:
    relation: :hasBirthYear
    source: Peter_Phillips
    literal_value: 1977
    literal_type: xsd:integer
  AddTriple (663cd016-b9ad-412f-8721-bf2c33f6d76c)
 Call ID: 663cd016-b9ad-412f-8721-bf2c33f6d76c
  Args:
    target: Mark_Phillips
    source: Peter_Phillips
    relation: :hasFather
  AddTriple (a1679728-a3de-4c74-b3ce-ca94617560b9)
 Call ID: a1679728-a3de-4c74-b3ce-ca94617560b9
  Args:
    target: Anne_Princess_Royal
    relation: :hasMother
    source: Peter_Phillips
  AddTriple (c34ffd71-027b-4ae8-8aaa-cf36f23abb9c)
 Call ID: c34ffd71-027b-4ae8-8aaa-cf36f23abb9c
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Peter_Phillips
  AddTriple (60ffdc8a-25bf-4f3e-912c-504fc6a91307)
 Call ID: 60ffdc8a-25bf-4f3e-912c-504fc6a91307
  Args:
    source: Anne_Princess_Royal
    relation: :hasMother
    target: Queen_Elizabeth_II
  AddTriple (d978c475-1c82-4a19-8947-3a9e0b7bec68)
 Call ID: d978c475-1c82-4a19-8947-3a9e0b7bec68
  Args:
    target: Prince_Philip
    source: Anne_Princess_Royal
    relation: :hasFather
  AddTriple (312dff72-0ff8-42cb-914b-282c28e4dbfc)
 Call ID: 312dff72-0ff8-42cb-914b-282c28e4dbfc
  Args:
    source: Peter_Phillips
    relation: :hasSister
    target: Zara_Tindall
  AddTriple (7415fa9d-f046-4e0e-bc53-6f8cb78babb5)
 Call ID: 7415fa9d-f046-4e0e-bc53-6f8cb78babb5
  Args:
    source: Zara_Tindall
    relation: :hasMother
    target: Anne_Princess_Royal
  AddTriple (50f5204e-f7f8-49e2-85b5-fc2b4330c4c0)
 Call ID: 50f5204e-f7f8-49e2-85b5-fc2b4330c4c0
  Args:
    target: Mark_Phillips
    source: Zara_Tindall
    relation: :hasFather
  AddTriple (65ab80c2-f502-4c3f-bb5d-d69c01fe2627)
 Call ID: 65ab80c2-f502-4c3f-bb5d-d69c01fe2627
  Args:
    source: Felicity_Wade
    relation: :hasFather
    target: Mark_Phillips
  AddTriple (1541e49b-6866-4c5a-bd37-c486ac46e914)
 Call ID: 1541e49b-6866-4c5a-bd37-c486ac46e914
  Args:
    source: Felicity_Wade
    relation: :hasMother
    target: Heather_Tonkin
  AddTriple (843cccad-39a8-46f2-ac84-87f114e9d4c3)
 Call ID: 843cccad-39a8-46f2-ac84-87f114e9d4c3
  Args:
    relation: :hasFather
    source: Stephanie_Phillips
    target: Mark_Phillips
  AddTriple (299b6678-0e1d-490b-8ecf-f2edc50da21a)
 Call ID: 299b6678-0e1d-490b-8ecf-f2edc50da21a
  Args:
    target: Sandy_Pflueger
    relation: :hasMother
    source: Stephanie_Phillips
  AddTriple (adb4f6e7-326c-4b25-94c2-88cbaa95894b)
 Call ID: adb4f6e7-326c-4b25-94c2-88cbaa95894b
  Args:
    target: Savannah_Phillips
    source: Peter_Phillips
    relation: :hasChild
  AddTriple (119b1f8d-8a4e-4e7a-9b63-21cf5e1e93c9)
 Call ID: 119b1f8d-8a4e-4e7a-9b63-21cf5e1e93c9
  Args:
    source: Peter_Phillips
    relation: :hasChild
    target: Isla_Phillips
  AddTriple (206684c5-6bae-46cb-947b-3848f7a6f14e)
 Call ID: 206684c5-6bae-46cb-947b-3848f7a6f14e
  Args:
    relation: :hasMother
    source: Savannah_Phillips
    target: Autumn_Kelly
  AddTriple (b64da4c1-42ea-43fc-bae2-7cc1296a973b)
 Call ID: b64da4c1-42ea-43fc-bae2-7cc1296a973b
  Args:
    target: Autumn_Kelly
    source: Isla_Phillips
    relation: :hasMother
  AddLiteral (d32d4cfd-852c-45fc-9ba0-1a3fd255c030)
 Call ID: d32d4cfd-852c-45fc-9ba0-1a3fd255c030
  Args:
    literal_type: xsd:integer
    literal_value: 1985
    source: Felicity_Wade
    relation: :hasBirthYear
  AddLiteral (027cfeb8-6b2f-409b-aa58-384988c033cf)
 Call ID: 027cfeb8-6b2f-409b-aa58-384988c033cf
  Args:
    literal_type: xsd:integer
    source: Zara_Tindall
    relation: :hasBirthYear
    literal_value: 1981
  AddLiteral (08185cf7-938e-4bad-a057-9a11c16b7371)
 Call ID: 08185cf7-938e-4bad-a057-9a11c16b7371
  Args:
    literal_type: xsd:integer
    literal_value: 1997
    source: Stephanie_Phillips
    relation: :hasBirthYear
  AddLiteral (d4b2021c-729a-4fc4-9deb-edd45f7427fd)
 Call ID: d4b2021c-729a-4fc4-9deb-edd45f7427fd
  Args:
    source: Harriet_Sperling
    relation: :hasBirthYear
    literal_value: 1980
    literal_type: xsd:integer
  AddLiteral (e652ce64-36c7-4eba-92c8-a867f01b77ec)
 Call ID: e652ce64-36c7-4eba-92c8-a867f01b77ec
  Args:
    source: Rupert_Sanders
    relation: :hasBirthYear
    literal_value: 1946
    literal_type: xsd:integer
  AddLiteral (70acddd8-18e2-44d2-ad08-840005d45c38)
 Call ID: 70acddd8-18e2-44d2-ad08-840005d45c38
  Args:
    literal_value: 2023
    source: Rupert_Sanders
    relation: :hasDeathYear
    literal_type: xsd:integer
  Finish (5408af59-8ea6-4a10-bf97-f341eadc113e)
 Call ID: 5408af59-8ea6-4a10-bf97-f341eadc113e
  Args: