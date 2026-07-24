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
  AssignClass (9c96cb80-9cd7-457b-a8d9-eb8e3b0a9bf5)
 Call ID: 9c96cb80-9cd7-457b-a8d9-eb8e3b0a9bf5
  Args:
    type: :Man
    source: Peter Phillips
  AssignClass (263ce13a-8c05-4405-a092-d3e450c5200e)
 Call ID: 263ce13a-8c05-4405-a092-d3e450c5200e
  Args:
    type: :Person
    source: Peter Phillips
  AddLiteral (19b7216f-9c39-4861-ab05-54e0b2314fb6)
 Call ID: 19b7216f-9c39-4861-ab05-54e0b2314fb6
  Args:
    literal_value: 1977
    source: Peter Phillips
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AssignClass (840da117-8908-4838-b298-28550886e5ea)
 Call ID: 840da117-8908-4838-b298-28550886e5ea
  Args:
    type: :Woman
    source: Anne, Princess Royal
  AssignClass (f9a0ac92-3e6e-4af4-bc9b-fa8aaa05813a)
 Call ID: f9a0ac92-3e6e-4af4-bc9b-fa8aaa05813a
  Args:
    type: :Person
    source: Anne, Princess Royal
  AssignClass (62924772-0750-4143-8432-af979284b7b1)
 Call ID: 62924772-0750-4143-8432-af979284b7b1
  Args:
    type: :Man
    source: Mark Phillips
  AssignClass (89d50dea-c9d3-4610-8c63-dc2fa77f9de8)
 Call ID: 89d50dea-c9d3-4610-8c63-dc2fa77f9de8
  Args:
    type: :Person
    source: Mark Phillips
  AddTriple (81e13c0a-8c17-4bde-bc5b-4fd18153b42f)
 Call ID: 81e13c0a-8c17-4bde-bc5b-4fd18153b42f
  Args:
    source: Peter Phillips
    target: Anne, Princess Royal
    relation: :isSonOf
  AddTriple (d38e4d95-6ec6-40b1-9801-65e5b6478812)
 Call ID: d38e4d95-6ec6-40b1-9801-65e5b6478812
  Args:
    relation: :isSonOf
    target: Mark Phillips
    source: Peter Phillips
  AssignClass (ff184716-2540-4c81-a2ab-062f4ea6b89c)
 Call ID: ff184716-2540-4c81-a2ab-062f4ea6b89c
  Args:
    type: :Man
    source: King Charles III
  AssignClass (373053f2-ff66-4fda-b651-7fb1d6109eea)
 Call ID: 373053f2-ff66-4fda-b651-7fb1d6109eea
  Args:
    type: :Person
    source: King Charles III
  AddTriple (8248738f-79c8-4319-a46e-c77bd8d2eaac)
 Call ID: 8248738f-79c8-4319-a46e-c77bd8d2eaac
  Args:
    source: Peter Phillips
    target: King Charles III
    relation: :hasRelation
  AssignClass (55dec580-b605-4dab-be08-10b61f6d00ce)
 Call ID: 55dec580-b605-4dab-be08-10b61f6d00ce
  Args:
    type: :Woman
    source: Queen Elizabeth II
  AssignClass (13836265-749f-4717-9a78-d3c3679cea35)
 Call ID: 13836265-749f-4717-9a78-d3c3679cea35
  Args:
    type: :Person
    source: Queen Elizabeth II
  AssignClass (d881bc30-58ff-4451-88b4-38974e61e56d)
 Call ID: d881bc30-58ff-4451-88b4-38974e61e56d
  Args:
    type: :Man
    source: Prince Philip, Duke of Edinburgh
  AssignClass (7b6d9384-c251-45e1-905a-792aff60bde8)
 Call ID: 7b6d9384-c251-45e1-905a-792aff60bde8
  Args:
    type: :Person
    source: Prince Philip, Duke of Edinburgh
  AddTriple (b1145b8c-5179-4cc3-942a-7eca2fdfb549)
 Call ID: b1145b8c-5179-4cc3-942a-7eca2fdfb549
  Args:
    relation: :isChildOf
    target: Queen Elizabeth II
    source: Anne, Princess Royal
  AddTriple (144583ce-c058-4fd2-97b2-7f3a6f700939)
 Call ID: 144583ce-c058-4fd2-97b2-7f3a6f700939
  Args:
    relation: :isChildOf
    target: Prince Philip, Duke of Edinburgh
    source: Anne, Princess Royal
  AssignClass (328503d8-c56f-41ed-8626-a95c4531402f)
 Call ID: 328503d8-c56f-41ed-8626-a95c4531402f
  Args:
    type: :Woman
    source: Zara Tindall
  AssignClass (bc73db7d-170a-447e-8e63-2f50f51ff732)
 Call ID: bc73db7d-170a-447e-8e63-2f50f51ff732
  Args:
    type: :Person
    source: Zara Tindall
  AddTriple (12f909c7-26b0-45e1-9285-0aad84dc9085)
 Call ID: 12f909c7-26b0-45e1-9285-0aad84dc9085
  Args:
    source: Peter Phillips
    relation: :isSiblingOf
    target: Zara Tindall
  AddTriple (172e44d1-b7cf-4445-9460-592721bf5e80)
 Call ID: 172e44d1-b7cf-4445-9460-592721bf5e80
  Args:
    relation: :isChildOf
    target: Anne, Princess Royal
    source: Zara Tindall
  AddTriple (053c3f6d-2996-454a-8f58-845b28ef4e13)
 Call ID: 053c3f6d-2996-454a-8f58-845b28ef4e13
  Args:
    target: Mark Phillips
    relation: :isChildOf
    source: Zara Tindall
  AssignClass (58db9e4e-1277-4063-9ac3-308e2ebbd47b)
 Call ID: 58db9e4e-1277-4063-9ac3-308e2ebbd47b
  Args:
    type: :Woman
    source: Felicity Wade
  AssignClass (0a595a68-8cab-429b-877d-1879cbe586f5)
 Call ID: 0a595a68-8cab-429b-877d-1879cbe586f5
  Args:
    type: :Person
    source: Felicity Wade
  AddTriple (85249821-0d08-450a-95e0-c3045f8a8f55)
 Call ID: 85249821-0d08-450a-95e0-c3045f8a8f55
  Args:
    relation: :isChildOf
    target: Mark Phillips
    source: Felicity Wade
  AssignClass (2e5a590d-5e50-457e-8a79-b22d3dfa4a8c)
 Call ID: 2e5a590d-5e50-457e-8a79-b22d3dfa4a8c
  Args:
    type: :Woman
    source: Heather Tonkin
  AssignClass (f0a081cc-2981-4e97-8663-3b12d365448a)
 Call ID: f0a081cc-2981-4e97-8663-3b12d365448a
  Args:
    type: :Person
    source: Heather Tonkin
  AddTriple (4d2db025-1e3f-43cf-9b1a-2f38e7c12442)
 Call ID: 4d2db025-1e3f-43cf-9b1a-2f38e7c12442
  Args:
    target: Heather Tonkin
    relation: :isChildOf
    source: Felicity Wade
  AssignClass (11421c09-cbe5-4dd2-9bfe-f7cf5c87c5db)
 Call ID: 11421c09-cbe5-4dd2-9bfe-f7cf5c87c5db
  Args:
    type: :Woman
    source: Stephanie Phillips
  AssignClass (a4b773f8-e7c1-4255-a8bb-8a1619dbb951)
 Call ID: a4b773f8-e7c1-4255-a8bb-8a1619dbb951
  Args:
    type: :Person
    source: Stephanie Phillips
  AddTriple (e1f014c2-16bf-4b45-bce3-970a5833650a)
 Call ID: e1f014c2-16bf-4b45-bce3-970a5833650a
  Args:
    relation: :isChildOf
    target: Mark Phillips
    source: Stephanie Phillips
  AssignClass (48b37046-1ffa-43d1-9c67-17b0b674cc9b)
 Call ID: 48b37046-1ffa-43d1-9c67-17b0b674cc9b
  Args:
    type: :Woman
    source: Sandy Pflueger
  AssignClass (11542043-619c-4961-ac88-0c6459225a8d)
 Call ID: 11542043-619c-4961-ac88-0c6459225a8d
  Args:
    type: :Person
    source: Sandy Pflueger
  AddTriple (2a1aea54-2c3c-4706-83a5-8ac773924586)
 Call ID: 2a1aea54-2c3c-4706-83a5-8ac773924586
  Args:
    target: Sandy Pflueger
    relation: :isChildOf
    source: Stephanie Phillips
  AssignClass (ebde89eb-e181-4511-9182-85a853e4b64a)
 Call ID: ebde89eb-e181-4511-9182-85a853e4b64a
  Args:
    type: :Woman
    source: Autumn Kelly
  AssignClass (876a3842-47eb-4083-95d1-f571a6c3cccc)
 Call ID: 876a3842-47eb-4083-95d1-f571a6c3cccc
  Args:
    type: :Person
    source: Autumn Kelly
  AddLiteral (035a28ef-00f0-45e6-b9b2-7362cf7018f7)
 Call ID: 035a28ef-00f0-45e6-b9b2-7362cf7018f7
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    literal_value: 2008
    source: Peter Phillips
  AddTriple (135602d0-7aa7-4be6-a662-017c812e8524)
 Call ID: 135602d0-7aa7-4be6-a662-017c812e8524
  Args:
    source: Peter Phillips
    relation: :hasRelation
    target: Autumn Kelly
  AssignClass (d3b99c04-61a7-440f-95e5-95b565bb5bbc)
 Call ID: d3b99c04-61a7-440f-95e5-95b565bb5bbc
  Args:
    type: :Woman
    source: Savannah Anne Kathleen Phillips
  AssignClass (bc64680f-676e-4d20-8cba-2cc3ffc3b31a)
 Call ID: bc64680f-676e-4d20-8cba-2cc3ffc3b31a
  Args:
    type: :Person
    source: Savannah Anne Kathleen Phillips
  AddTriple (1c771d42-2244-454c-9ea2-7abfdc81649b)
 Call ID: 1c771d42-2244-454c-9ea2-7abfdc81649b
  Args:
    target: Peter Phillips
    relation: :isChildOf
    source: Savannah Anne Kathleen Phillips
  AddTriple (3e93dd68-ebdc-48d6-a679-d51b39534ae0)
 Call ID: 3e93dd68-ebdc-48d6-a679-d51b39534ae0
  Args:
    target: Autumn Kelly
    relation: :isChildOf
    source: Savannah Anne Kathleen Phillips
  AssignClass (9fcc16ed-d0d0-4e1c-925e-68f25f1ea94a)
 Call ID: 9fcc16ed-d0d0-4e1c-925e-68f25f1ea94a
  Args:
    type: :Woman
    source: Isla Elizabeth Phillips
  AssignClass (f8aaa6a1-26be-4c2b-8cf7-a80c9a2fb498)
 Call ID: f8aaa6a1-26be-4c2b-8cf7-a80c9a2fb498
  Args:
    type: :Person
    source: Isla Elizabeth Phillips
  AddTriple (3026833c-7d93-40df-92c9-a1e4e05ff9aa)
 Call ID: 3026833c-7d93-40df-92c9-a1e4e05ff9aa
  Args:
    source: Isla Elizabeth Phillips
    relation: :isChildOf
    target: Peter Phillips
  AddTriple (06abb2b5-2f42-48dc-b208-5846033607b1)
 Call ID: 06abb2b5-2f42-48dc-b208-5846033607b1
  Args:
    source: Isla Elizabeth Phillips
    target: Autumn Kelly
    relation: :isChildOf
  AssignClass (760e02e8-3201-4c44-8703-5e83f6714bea)
 Call ID: 760e02e8-3201-4c44-8703-5e83f6714bea
  Args:
    type: :Woman
    source: Lindsay Wallace
  AssignClass (68748a8b-588f-42ce-9eae-befedfbbe9d2)
 Call ID: 68748a8b-588f-42ce-9eae-befedfbbe9d2
  Args:
    type: :Person
    source: Lindsay Wallace
  AddTriple (7af36586-8a3a-48b8-92d8-187e0528aa6d)
 Call ID: 7af36586-8a3a-48b8-92d8-187e0528aa6d
  Args:
    source: Peter Phillips
    target: Lindsay Wallace
    relation: :hasRelation
  AssignClass (fff5cb5f-eca5-4c35-aea1-cd28d4bced93)
 Call ID: fff5cb5f-eca5-4c35-aea1-cd28d4bced93
  Args:
    type: :Woman
    source: Harriet Sperling
  AssignClass (3a8de041-a9bb-44a4-a10d-1ec929f270cb)
 Call ID: 3a8de041-a9bb-44a4-a10d-1ec929f270cb
  Args:
    type: :Person
    source: Harriet Sperling
  AddTriple (9083c950-8369-470f-a6ed-2566c95424c9)
 Call ID: 9083c950-8369-470f-a6ed-2566c95424c9
  Args:
    target: Harriet Sperling
    relation: :hasRelation
    source: Peter Phillips
  AssignClass (d25ae9e4-3a7b-47e1-960d-e6a980745b8e)
 Call ID: d25ae9e4-3a7b-47e1-960d-e6a980745b8e
  Args:
    type: :Man
    source: Rupert Sanders
  AssignClass (0b4dccb0-8520-4dde-9259-a333574258c1)
 Call ID: 0b4dccb0-8520-4dde-9259-a333574258c1
  Args:
    type: :Person
    source: Rupert Sanders
  AddTriple (d6548771-ae04-48e8-9daa-1851579709aa)
 Call ID: d6548771-ae04-48e8-9daa-1851579709aa
  Args:
    source: Harriet Sperling
    relation: :isChildOf
    target: Rupert Sanders
  Finish (275ca133-687c-4cd2-8243-7f3cff68f864)
 Call ID: 275ca133-687c-4cd2-8243-7f3cff68f864
  Args: