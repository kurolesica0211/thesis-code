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
  AssignClass (d278e707-38cc-4b9f-9120-2be9aac8352b)
 Call ID: d278e707-38cc-4b9f-9120-2be9aac8352b
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (231ea12e-b523-4f16-8149-1950de7275ef)
 Call ID: 231ea12e-b523-4f16-8149-1950de7275ef
  Args:
    type: :Person
    source: Peter_Phillips
  AddLiteral (71d26a52-29d3-460c-95de-8911a5ec41ed)
 Call ID: 71d26a52-29d3-460c-95de-8911a5ec41ed
  Args:
    literal_value: 1977
    relation: :hasBirthYear
    source: Peter_Phillips
    literal_type: xsd:integer
  AssignClass (1cd3fbf5-5738-4ca0-a1c2-3ddae690bdf9)
 Call ID: 1cd3fbf5-5738-4ca0-a1c2-3ddae690bdf9
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (bc960e69-06f6-46f9-8ae6-1fcc0131f53c)
 Call ID: bc960e69-06f6-46f9-8ae6-1fcc0131f53c
  Args:
    source: Anne_Princess_Royal
    type: :Person
  AssignClass (1fb09818-b9f2-406b-a6eb-903aaf4245d7)
 Call ID: 1fb09818-b9f2-406b-a6eb-903aaf4245d7
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (73c23bb7-9fbd-4d43-a58f-03d78cdab95d)
 Call ID: 73c23bb7-9fbd-4d43-a58f-03d78cdab95d
  Args:
    source: Mark_Phillips
    type: :Person
  AddTriple (eba470e5-5a4e-4cbd-8dbb-0d07a45e59e7)
 Call ID: eba470e5-5a4e-4cbd-8dbb-0d07a45e59e7
  Args:
    relation: :hasFather
    source: Peter_Phillips
    target: Mark_Phillips
  AddTriple (f5b8e993-673e-4d23-8e3c-343f8797cd0a)
 Call ID: f5b8e993-673e-4d23-8e3c-343f8797cd0a
  Args:
    source: Peter_Phillips
    relation: :hasMother
    target: Anne_Princess_Royal
  AssignClass (4f873abe-c0dd-47db-8aaa-d30cece6658c)
 Call ID: 4f873abe-c0dd-47db-8aaa-d30cece6658c
  Args:
    source: Charles_III
    type: :Man
  AssignClass (acdb5994-dc54-4e94-bcd0-61cfc1b4af93)
 Call ID: acdb5994-dc54-4e94-bcd0-61cfc1b4af93
  Args:
    type: :Person
    source: Charles_III
  AddTriple (69ef5197-84de-428e-ab33-8a3a58ca623e)
 Call ID: 69ef5197-84de-428e-ab33-8a3a58ca623e
  Args:
    target: Charles_III
    source: Anne_Princess_Royal
    relation: :isSisterOf
  AssignClass (5a3df5fe-1198-47f0-a27a-7153468cb772)
 Call ID: 5a3df5fe-1198-47f0-a27a-7153468cb772
  Args:
    type: :Woman
    source: Elizabeth_II
  AssignClass (e8561db7-1b5e-4d47-84b4-09a4e7008346)
 Call ID: e8561db7-1b5e-4d47-84b4-09a4e7008346
  Args:
    source: Elizabeth_II
    type: :Person
  AddTriple (ee05ea9b-cffe-4fe0-be62-b1db67f90ea9)
 Call ID: ee05ea9b-cffe-4fe0-be62-b1db67f90ea9
  Args:
    target: Anne_Princess_Royal
    relation: :isMotherOf
    source: Elizabeth_II
  AssignClass (b3cf11c9-6b48-4b11-97b0-73968f976732)
 Call ID: b3cf11c9-6b48-4b11-97b0-73968f976732
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (a32e0e7d-98b2-4c01-9b34-d06e7fa9317c)
 Call ID: a32e0e7d-98b2-4c01-9b34-d06e7fa9317c
  Args:
    source: Prince_Philip
    type: :Person
  AddTriple (2e6e5ba6-7f04-41be-b7e4-9848b29f24cc)
 Call ID: 2e6e5ba6-7f04-41be-b7e4-9848b29f24cc
  Args:
    target: Anne_Princess_Royal
    relation: :isFatherOf
    source: Prince_Philip
  AssignClass (f2d6f290-738f-44b5-b5ee-6d4d185cd1c2)
 Call ID: f2d6f290-738f-44b5-b5ee-6d4d185cd1c2
  Args:
    source: Zara_Tindall
    type: :Woman
  AssignClass (385f0a8c-1a8e-49e4-abb3-cf5c834fdcd5)
 Call ID: 385f0a8c-1a8e-49e4-abb3-cf5c834fdcd5
  Args:
    source: Zara_Tindall
    type: :Person
  AddTriple (d3d7a2ac-2c26-478e-91a9-5cfb64d6e5a3)
 Call ID: d3d7a2ac-2c26-478e-91a9-5cfb64d6e5a3
  Args:
    source: Peter_Phillips
    relation: :isSiblingOf
    target: Zara_Tindall
  AddTriple (da4ddc19-a7a5-4d71-a023-11d1878f94dd)
 Call ID: da4ddc19-a7a5-4d71-a023-11d1878f94dd
  Args:
    target: Anne_Princess_Royal
    relation: :hasMother
    source: Zara_Tindall
  AddTriple (8d3c5df0-1416-42b6-9eca-61b85fe179e5)
 Call ID: 8d3c5df0-1416-42b6-9eca-61b85fe179e5
  Args:
    relation: :hasFather
    source: Zara_Tindall
    target: Mark_Phillips
  AssignClass (a9bc1a21-5fcb-4a8c-bb6d-f63b5cf2c47f)
 Call ID: a9bc1a21-5fcb-4a8c-bb6d-f63b5cf2c47f
  Args:
    source: Felicity_Wade
    type: :Woman
  AssignClass (19d50688-a256-49df-b63e-24a6d6202ceb)
 Call ID: 19d50688-a256-49df-b63e-24a6d6202ceb
  Args:
    type: :Person
    source: Felicity_Wade
  AddTriple (bfa98b47-bbe6-47f7-965b-0fd06bc9fcd1)
 Call ID: bfa98b47-bbe6-47f7-965b-0fd06bc9fcd1
  Args:
    target: Mark_Phillips
    source: Felicity_Wade
    relation: :hasFather
  AssignClass (f2f7d3a3-0799-49c7-935b-2eb94bd38e9d)
 Call ID: f2f7d3a3-0799-49c7-935b-2eb94bd38e9d
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (60f343b0-9d79-4e95-b672-4acba8c983aa)
 Call ID: 60f343b0-9d79-4e95-b672-4acba8c983aa
  Args:
    type: :Person
    source: Stephanie_Phillips
  AddTriple (0d503093-e473-48c5-9e77-84bdc8000013)
 Call ID: 0d503093-e473-48c5-9e77-84bdc8000013
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Stephanie_Phillips
  AssignClass (6c47312a-368b-4988-9454-d16bcc39acb9)
 Call ID: 6c47312a-368b-4988-9454-d16bcc39acb9
  Args:
    source: Autumn_Kelly
    type: :Woman
  AssignClass (e53c3335-92e2-4065-9fca-802f7c2e2ae5)
 Call ID: e53c3335-92e2-4065-9fca-802f7c2e2ae5
  Args:
    source: Autumn_Kelly
    type: :Person
  AddTriple (7d7a1e14-ddc5-4279-9666-7fed8f139520)
 Call ID: 7d7a1e14-ddc5-4279-9666-7fed8f139520
  Args:
    target: Autumn_Kelly
    relation: :hasRelation
    source: Peter_Phillips
  AddLiteral (de718a3d-3861-451c-ab9c-e69099162fb5)
 Call ID: de718a3d-3861-451c-ab9c-e69099162fb5
  Args:
    literal_type: xsd:integer
    literal_value: 2008
    relation: :hasMarriageYear
    source: Peter_Phillips
  AssignClass (2d50f50c-7baa-4029-b423-f7db1f3c8e9e)
 Call ID: 2d50f50c-7baa-4029-b423-f7db1f3c8e9e
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (20c33248-1153-4c16-a314-4af673452a19)
 Call ID: 20c33248-1153-4c16-a314-4af673452a19
  Args:
    source: Savannah_Phillips
    type: :Person
  AddTriple (1791a3f3-2fe2-4ffd-92d8-5e9c6a133563)
 Call ID: 1791a3f3-2fe2-4ffd-92d8-5e9c6a133563
  Args:
    relation: :hasFather
    source: Savannah_Phillips
    target: Peter_Phillips
  AddTriple (fa4f5c44-1fa4-40cc-9a14-7696408fbc39)
 Call ID: fa4f5c44-1fa4-40cc-9a14-7696408fbc39
  Args:
    relation: :hasMother
    source: Savannah_Phillips
    target: Autumn_Kelly
  AssignClass (7cb55e90-961a-49fd-8194-5ad912431cbd)
 Call ID: 7cb55e90-961a-49fd-8194-5ad912431cbd
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (dd07fd1d-eb7b-42c3-a9c0-257a2504fad2)
 Call ID: dd07fd1d-eb7b-42c3-a9c0-257a2504fad2
  Args:
    source: Isla_Phillips
    type: :Person
  AddTriple (95b88dd6-c590-4550-8142-bcbddc743c99)
 Call ID: 95b88dd6-c590-4550-8142-bcbddc743c99
  Args:
    target: Peter_Phillips
    relation: :hasFather
    source: Isla_Phillips
  AddTriple (f8db68d9-9543-461e-af58-6c4d61728660)
 Call ID: f8db68d9-9543-461e-af58-6c4d61728660
  Args:
    source: Isla_Phillips
    relation: :hasMother
    target: Autumn_Kelly
  AssignClass (f946b1e3-01eb-494a-914c-d5f7a786447d)
 Call ID: f946b1e3-01eb-494a-914c-d5f7a786447d
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (d6838040-36ff-4926-b24b-e80927d5d6cd)
 Call ID: d6838040-36ff-4926-b24b-e80927d5d6cd
  Args:
    type: :Person
    source: Lindsay_Wallace
  AddTriple (e969b9b9-404b-4793-9b65-e2cf6a33046a)
 Call ID: e969b9b9-404b-4793-9b65-e2cf6a33046a
  Args:
    target: Lindsay_Wallace
    source: Peter_Phillips
    relation: :hasRelation
  AssignClass (f4a25b83-db18-475e-909b-955e69a6afa9)
 Call ID: f4a25b83-db18-475e-909b-955e69a6afa9
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (9fd0ba65-a60c-4b45-a22b-7e5433c7d78d)
 Call ID: 9fd0ba65-a60c-4b45-a22b-7e5433c7d78d
  Args:
    source: Harriet_Sperling
    type: :Person
  AddTriple (8eb938c7-1429-46ec-979a-036d8cf5c5e4)
 Call ID: 8eb938c7-1429-46ec-979a-036d8cf5c5e4
  Args:
    relation: :hasRelation
    source: Peter_Phillips
    target: Harriet_Sperling
  Finish (1cf7b109-233d-4b62-9ebd-fe911ed6090c)
 Call ID: 1cf7b109-233d-4b62-9ebd-fe911ed6090c
  Args: