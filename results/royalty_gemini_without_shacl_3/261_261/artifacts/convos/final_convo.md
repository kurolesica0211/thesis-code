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
  AssignClass (2a667c48-d14c-47da-aeb5-c393ce4bb8c9)
 Call ID: 2a667c48-d14c-47da-aeb5-c393ce4bb8c9
  Args:
    type: :Man
    source: :Peter_Phillips
  AssignClass (45022f27-84a1-4fcf-9aba-26bb98459c7b)
 Call ID: 45022f27-84a1-4fcf-9aba-26bb98459c7b
  Args:
    type: :Person
    source: :Peter_Phillips
  AddLiteral (60663143-4f5c-432c-9ce1-e0ab8b64e714)
 Call ID: 60663143-4f5c-432c-9ce1-e0ab8b64e714
  Args:
    literal_type: xsd:integer
    source: :Peter_Phillips
    relation: :hasBirthYear
    literal_value: 1977
  AssignClass (960bab60-7de1-40fd-97c8-259f44e18c19)
 Call ID: 960bab60-7de1-40fd-97c8-259f44e18c19
  Args:
    type: :Woman
    source: :Anne_Princess_Royal
  AssignClass (3d4a9d07-6199-4814-a383-09647cfd6a51)
 Call ID: 3d4a9d07-6199-4814-a383-09647cfd6a51
  Args:
    type: :Person
    source: :Anne_Princess_Royal
  AssignClass (a983fc79-4e89-497d-addc-0dbb7a333016)
 Call ID: a983fc79-4e89-497d-addc-0dbb7a333016
  Args:
    type: :Man
    source: :Mark_Phillips
  AssignClass (4ddaa369-d0b5-4089-8362-daa5a1fcee0b)
 Call ID: 4ddaa369-d0b5-4089-8362-daa5a1fcee0b
  Args:
    type: :Person
    source: :Mark_Phillips
  AddTriple (f5b2ca8b-4c4a-40c8-acdf-09b73ad9d88b)
 Call ID: f5b2ca8b-4c4a-40c8-acdf-09b73ad9d88b
  Args:
    source: :Peter_Phillips
    relation: :hasFather
    target: :Mark_Phillips
  AddTriple (7b61bfdc-576c-4edb-b9f4-1d4e87df0838)
 Call ID: 7b61bfdc-576c-4edb-b9f4-1d4e87df0838
  Args:
    source: :Peter_Phillips
    relation: :hasMother
    target: :Anne_Princess_Royal
  AssignClass (40972564-4d8a-49dd-84c5-4f4db41f0d4e)
 Call ID: 40972564-4d8a-49dd-84c5-4f4db41f0d4e
  Args:
    type: :Woman
    source: :Zara_Tindall
  AssignClass (e868fa4e-bfa7-4abc-bd05-7110494bdc8a)
 Call ID: e868fa4e-bfa7-4abc-bd05-7110494bdc8a
  Args:
    type: :Person
    source: :Zara_Tindall
  AddTriple (ddffbaa8-4551-4aa0-8139-22bdfb03637d)
 Call ID: ddffbaa8-4551-4aa0-8139-22bdfb03637d
  Args:
    source: :Peter_Phillips
    relation: :isSiblingOf
    target: :Zara_Tindall
  AddTriple (bc5c7839-8cab-441e-a19e-be38db839cd3)
 Call ID: bc5c7839-8cab-441e-a19e-be38db839cd3
  Args:
    relation: :hasMother
    source: :Zara_Tindall
    target: :Anne_Princess_Royal
  AddTriple (5eca47a4-d2f6-42bc-9f38-d5d97b4960d4)
 Call ID: 5eca47a4-d2f6-42bc-9f38-d5d97b4960d4
  Args:
    source: :Zara_Tindall
    relation: :hasFather
    target: :Mark_Phillips
  AssignClass (75b01a1a-0305-4ab1-8bf2-569c75514792)
 Call ID: 75b01a1a-0305-4ab1-8bf2-569c75514792
  Args:
    type: :Woman
    source: :Felicity_Wade
  AssignClass (5aca90ef-d3b8-4ab6-9e74-b66b38e1a63f)
 Call ID: 5aca90ef-d3b8-4ab6-9e74-b66b38e1a63f
  Args:
    type: :Person
    source: :Felicity_Wade
  AddTriple (85aff9f2-998e-4299-a878-8bdecbf28d28)
 Call ID: 85aff9f2-998e-4299-a878-8bdecbf28d28
  Args:
    target: :Mark_Phillips
    source: :Felicity_Wade
    relation: :hasFather
  AssignClass (2178cc3e-a8dc-4dba-a7e0-b1403dbc222c)
 Call ID: 2178cc3e-a8dc-4dba-a7e0-b1403dbc222c
  Args:
    type: :Woman
    source: :Heather_Tonkin
  AssignClass (4abb5502-70e9-4aa0-af20-6e8203b69312)
 Call ID: 4abb5502-70e9-4aa0-af20-6e8203b69312
  Args:
    type: :Person
    source: :Heather_Tonkin
  AddTriple (457e2e85-e8d4-417a-a73b-8e5e7587c961)
 Call ID: 457e2e85-e8d4-417a-a73b-8e5e7587c961
  Args:
    source: :Felicity_Wade
    relation: :hasMother
    target: :Heather_Tonkin
  AssignClass (d025f757-aa75-462e-a41f-2a2e2fbc8b28)
 Call ID: d025f757-aa75-462e-a41f-2a2e2fbc8b28
  Args:
    type: :Woman
    source: :Stephanie_Phillips
  AssignClass (8fe41050-e08e-451d-b71d-27b44ef083f0)
 Call ID: 8fe41050-e08e-451d-b71d-27b44ef083f0
  Args:
    type: :Person
    source: :Stephanie_Phillips
  AddTriple (e26d7cdf-a558-4d03-a396-c596f52fcc48)
 Call ID: e26d7cdf-a558-4d03-a396-c596f52fcc48
  Args:
    target: :Mark_Phillips
    source: :Stephanie_Phillips
    relation: :hasFather
  AssignClass (cc2b6d9a-62e3-4049-a672-09dd5e37ce9e)
 Call ID: cc2b6d9a-62e3-4049-a672-09dd5e37ce9e
  Args:
    type: :Woman
    source: :Sandy_Pflueger
  AssignClass (cf667262-a79a-4c59-b4f7-731aac393904)
 Call ID: cf667262-a79a-4c59-b4f7-731aac393904
  Args:
    type: :Person
    source: :Sandy_Pflueger
  AddTriple (985e5b6b-5f7a-4354-9fc2-6ee09483e8d0)
 Call ID: 985e5b6b-5f7a-4354-9fc2-6ee09483e8d0
  Args:
    source: :Stephanie_Phillips
    relation: :hasMother
    target: :Sandy_Pflueger
  AssignClass (cd4225bf-8ad5-4599-ac1c-7788d228761a)
 Call ID: cd4225bf-8ad5-4599-ac1c-7788d228761a
  Args:
    type: :Woman
    source: :Autumn_Kelly
  AssignClass (cfce8824-2aa5-4a71-a511-7620cffbd72b)
 Call ID: cfce8824-2aa5-4a71-a511-7620cffbd72b
  Args:
    type: :Person
    source: :Autumn_Kelly
  AddLiteral (ea7aaa00-90c7-48b7-baf4-9e073518a803)
 Call ID: ea7aaa00-90c7-48b7-baf4-9e073518a803
  Args:
    literal_value: 2008
    relation: :hasMarriageYear
    source: :Peter_Phillips
    literal_type: xsd:integer
  AssignClass (04cf61e9-c550-4352-931c-d25520635b98)
 Call ID: 04cf61e9-c550-4352-931c-d25520635b98
  Args:
    type: :Woman
    source: :Savannah_Phillips
  AssignClass (de38e462-19e4-45ba-b765-7b176ed364d2)
 Call ID: de38e462-19e4-45ba-b765-7b176ed364d2
  Args:
    type: :Person
    source: :Savannah_Phillips
  AddTriple (5bc8b03c-e604-4548-9245-43c38b8b4a43)
 Call ID: 5bc8b03c-e604-4548-9245-43c38b8b4a43
  Args:
    source: :Savannah_Phillips
    relation: :hasFather
    target: :Peter_Phillips
  AddTriple (6f5b5a75-8a87-4838-aa44-c8f9620a01d0)
 Call ID: 6f5b5a75-8a87-4838-aa44-c8f9620a01d0
  Args:
    source: :Savannah_Phillips
    relation: :hasMother
    target: :Autumn_Kelly
  AssignClass (038457c1-8043-4bc9-8e1c-eeee558a1121)
 Call ID: 038457c1-8043-4bc9-8e1c-eeee558a1121
  Args:
    type: :Woman
    source: :Isla_Phillips
  AssignClass (7c048a9f-9ede-4d5b-9291-86e351177844)
 Call ID: 7c048a9f-9ede-4d5b-9291-86e351177844
  Args:
    type: :Person
    source: :Isla_Phillips
  AddTriple (444ecfa8-645b-4ded-8e99-75961059fc72)
 Call ID: 444ecfa8-645b-4ded-8e99-75961059fc72
  Args:
    source: :Isla_Phillips
    relation: :hasFather
    target: :Peter_Phillips
  AddTriple (7c5e9977-743a-48d0-9468-dda304eb1ca3)
 Call ID: 7c5e9977-743a-48d0-9468-dda304eb1ca3
  Args:
    relation: :hasMother
    source: :Isla_Phillips
    target: :Autumn_Kelly
  AssignClass (18f20dd2-88a0-4b25-a0d8-36f559beccbf)
 Call ID: 18f20dd2-88a0-4b25-a0d8-36f559beccbf
  Args:
    type: :Woman
    source: :Harriet_Sperling
  AssignClass (7b2913dc-96eb-48e7-96ef-b5e082acf9ae)
 Call ID: 7b2913dc-96eb-48e7-96ef-b5e082acf9ae
  Args:
    type: :Person
    source: :Harriet_Sperling
  AssignClass (993e86f5-ade4-49a9-a6a7-b3a49d346d42)
 Call ID: 993e86f5-ade4-49a9-a6a7-b3a49d346d42
  Args:
    type: :Man
    source: :Rupert_Sanders
  AssignClass (923ea7c2-20bd-4ae4-a51d-15a4df742fa9)
 Call ID: 923ea7c2-20bd-4ae4-a51d-15a4df742fa9
  Args:
    type: :Person
    source: :Rupert_Sanders
  AddTriple (a5f4b90d-ec48-45d4-bc6a-767d93f955d2)
 Call ID: a5f4b90d-ec48-45d4-bc6a-767d93f955d2
  Args:
    source: :Harriet_Sperling
    relation: :hasFather
    target: :Rupert_Sanders
  AddLiteral (01f0da25-0788-437f-bae5-406368bbb904)
 Call ID: 01f0da25-0788-437f-bae5-406368bbb904
  Args:
    literal_value: 1946
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Rupert_Sanders
  AddLiteral (74c9dea6-f3fe-4a5c-8bd4-eaf46b9e9e0e)
 Call ID: 74c9dea6-f3fe-4a5c-8bd4-eaf46b9e9e0e
  Args:
    literal_type: xsd:integer
    source: :Rupert_Sanders
    relation: :hasDeathYear
    literal_value: 2023
  Finish (781ebd26-44b4-4b7d-9e2a-c86f00bac15d)
 Call ID: 781ebd26-44b4-4b7d-9e2a-c86f00bac15d
  Args: