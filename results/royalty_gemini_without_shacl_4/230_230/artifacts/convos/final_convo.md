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
  AssignClass (a1abad38-d458-4f5a-a11a-7e82e09a6f99)
 Call ID: a1abad38-d458-4f5a-a11a-7e82e09a6f99
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (ea96f184-a2f3-4f9e-8c0b-ffdde6770112)
 Call ID: ea96f184-a2f3-4f9e-8c0b-ffdde6770112
  Args:
    type: :Person
    source: Peter_Phillips
  AddLiteral (7e998ebf-104f-4f6f-975b-4208679d3ffe)
 Call ID: 7e998ebf-104f-4f6f-975b-4208679d3ffe
  Args:
    source: Peter_Phillips
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1977
  AssignClass (506ee23e-19f7-44dc-bd4f-37c2c3ea0793)
 Call ID: 506ee23e-19f7-44dc-bd4f-37c2c3ea0793
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (bee6d3db-a9a8-42a8-9cfe-a18933c70c82)
 Call ID: bee6d3db-a9a8-42a8-9cfe-a18933c70c82
  Args:
    type: :Person
    source: Anne_Princess_Royal
  AssignClass (c03dde69-8b5f-4ce8-b88b-2bbdf7f0d8ad)
 Call ID: c03dde69-8b5f-4ce8-b88b-2bbdf7f0d8ad
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (0ddb6092-41c1-4389-b57f-3ccc13872ff7)
 Call ID: 0ddb6092-41c1-4389-b57f-3ccc13872ff7
  Args:
    type: :Person
    source: Mark_Phillips
  AddTriple (a0744b31-2e53-4c05-b33f-86e34f26a256)
 Call ID: a0744b31-2e53-4c05-b33f-86e34f26a256
  Args:
    target: Anne_Princess_Royal
    source: Peter_Phillips
    relation: :hasMother
  AddTriple (d7e24fd4-d46b-4aaa-99aa-a92718fecd3d)
 Call ID: d7e24fd4-d46b-4aaa-99aa-a92718fecd3d
  Args:
    source: Peter_Phillips
    relation: :hasFather
    target: Mark_Phillips
  AssignClass (231f5b93-830a-40ef-a07b-0b968e86850a)
 Call ID: 231f5b93-830a-40ef-a07b-0b968e86850a
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (9305ebab-eeb4-4cf4-8bfe-046ae1d68fbb)
 Call ID: 9305ebab-eeb4-4cf4-8bfe-046ae1d68fbb
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (507e567d-b822-430c-9dca-8eac8b9d05b4)
 Call ID: 507e567d-b822-430c-9dca-8eac8b9d05b4
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (055b0651-e411-4f77-a011-368c4fc9c54b)
 Call ID: 055b0651-e411-4f77-a011-368c4fc9c54b
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (572d86e1-33ea-4b18-a7c9-b8db77d8fe48)
 Call ID: 572d86e1-33ea-4b18-a7c9-b8db77d8fe48
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (14e29be9-cc6a-44d0-982a-c498fb9c7100)
 Call ID: 14e29be9-cc6a-44d0-982a-c498fb9c7100
  Args:
    type: :Person
    source: Prince_Philip
  AddTriple (2fb21ca0-b5a9-4df6-9f86-95b2e2996446)
 Call ID: 2fb21ca0-b5a9-4df6-9f86-95b2e2996446
  Args:
    target: Queen_Elizabeth_II
    relation: :hasMother
    source: Anne_Princess_Royal
  AddTriple (6eaad4c5-84f4-4f49-894e-2986454ef11c)
 Call ID: 6eaad4c5-84f4-4f49-894e-2986454ef11c
  Args:
    target: Prince_Philip
    relation: :hasFather
    source: Anne_Princess_Royal
  AssignClass (99c754c5-a5a4-4e70-a1bc-aaa3044de30a)
 Call ID: 99c754c5-a5a4-4e70-a1bc-aaa3044de30a
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (3a494e74-1b77-48af-aa67-16a809423520)
 Call ID: 3a494e74-1b77-48af-aa67-16a809423520
  Args:
    type: :Person
    source: Zara_Tindall
  AddTriple (a66673d0-45d0-4bf5-938e-8dc97a1a8f90)
 Call ID: a66673d0-45d0-4bf5-938e-8dc97a1a8f90
  Args:
    target: Anne_Princess_Royal
    source: Zara_Tindall
    relation: :hasMother
  AddTriple (ba4f3565-6222-4c2f-9b37-eb28023cc8c9)
 Call ID: ba4f3565-6222-4c2f-9b37-eb28023cc8c9
  Args:
    target: Mark_Phillips
    source: Zara_Tindall
    relation: :hasFather
  AssignClass (c5c7d30e-2fd6-4692-a4d5-fb307ff2ea2d)
 Call ID: c5c7d30e-2fd6-4692-a4d5-fb307ff2ea2d
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (dd0ab511-ed09-45e3-a30c-282c3fded94f)
 Call ID: dd0ab511-ed09-45e3-a30c-282c3fded94f
  Args:
    type: :Person
    source: Felicity_Wade
  AssignClass (cbaddd06-7ff8-49fe-91de-dc85b3143a00)
 Call ID: cbaddd06-7ff8-49fe-91de-dc85b3143a00
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (e00309d2-a6f4-4dbf-bbcf-fdabdc04b775)
 Call ID: e00309d2-a6f4-4dbf-bbcf-fdabdc04b775
  Args:
    type: :Person
    source: Heather_Tonkin
  AddTriple (acd81ae1-68ba-47df-84c2-c8fe5ca30c9f)
 Call ID: acd81ae1-68ba-47df-84c2-c8fe5ca30c9f
  Args:
    relation: :hasFather
    source: Felicity_Wade
    target: Mark_Phillips
  AddTriple (59ec1d8b-a738-4f01-812f-6ef3b629c0c4)
 Call ID: 59ec1d8b-a738-4f01-812f-6ef3b629c0c4
  Args:
    target: Heather_Tonkin
    relation: :hasMother
    source: Felicity_Wade
  AssignClass (d81a9823-f516-4347-858a-da30c4d7e41e)
 Call ID: d81a9823-f516-4347-858a-da30c4d7e41e
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (8ed28fac-14dd-42f1-adf4-14d750c91c25)
 Call ID: 8ed28fac-14dd-42f1-adf4-14d750c91c25
  Args:
    type: :Person
    source: Stephanie_Phillips
  AssignClass (ae3a9b40-dbde-4282-9f61-a13c21bbbd2a)
 Call ID: ae3a9b40-dbde-4282-9f61-a13c21bbbd2a
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (29b2eb02-efcb-448a-b25a-c8e1e3e11096)
 Call ID: 29b2eb02-efcb-448a-b25a-c8e1e3e11096
  Args:
    type: :Person
    source: Sandy_Pflueger
  AddTriple (0a734574-14e8-4e92-9880-ca12b1c65046)
 Call ID: 0a734574-14e8-4e92-9880-ca12b1c65046
  Args:
    target: Mark_Phillips
    relation: :hasFather
    source: Stephanie_Phillips
  AddTriple (e96f09c5-7b15-47f8-807e-01dd521bf7cd)
 Call ID: e96f09c5-7b15-47f8-807e-01dd521bf7cd
  Args:
    relation: :hasMother
    source: Stephanie_Phillips
    target: Sandy_Pflueger
  AssignClass (1174dee3-4eb7-4e57-b325-4579ab8f549f)
 Call ID: 1174dee3-4eb7-4e57-b325-4579ab8f549f
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (93ca4fd4-4970-42c4-9a5c-610c387b7e9f)
 Call ID: 93ca4fd4-4970-42c4-9a5c-610c387b7e9f
  Args:
    type: :Person
    source: Autumn_Kelly
  AddLiteral (8cf883c8-2f8a-4497-8b7a-7e6d20bb8c0a)
 Call ID: 8cf883c8-2f8a-4497-8b7a-7e6d20bb8c0a
  Args:
    literal_value: 2008
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Peter_Phillips
  AssignClass (b9765967-c715-4115-b1ed-a9f78609d5b2)
 Call ID: b9765967-c715-4115-b1ed-a9f78609d5b2
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (87bd58c9-8952-4112-82a3-fae783b259e5)
 Call ID: 87bd58c9-8952-4112-82a3-fae783b259e5
  Args:
    type: :Person
    source: Savannah_Phillips
  AddTriple (fcef86a9-6b1d-439f-ae0d-4debfdf91254)
 Call ID: fcef86a9-6b1d-439f-ae0d-4debfdf91254
  Args:
    target: Autumn_Kelly
    source: Savannah_Phillips
    relation: :hasMother
  AddTriple (5d3d8413-998d-4d9c-b7a3-8de8531f76bd)
 Call ID: 5d3d8413-998d-4d9c-b7a3-8de8531f76bd
  Args:
    target: Peter_Phillips
    relation: :hasFather
    source: Savannah_Phillips
  AssignClass (205ad2e1-babe-49ff-b6a9-774a06f7c2f5)
 Call ID: 205ad2e1-babe-49ff-b6a9-774a06f7c2f5
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (b12b4b80-f51a-4bc3-8864-f3eee6bd38a1)
 Call ID: b12b4b80-f51a-4bc3-8864-f3eee6bd38a1
  Args:
    type: :Person
    source: Isla_Phillips
  AddTriple (19482ef8-9775-4ef5-8996-e87394c4f2c3)
 Call ID: 19482ef8-9775-4ef5-8996-e87394c4f2c3
  Args:
    target: Autumn_Kelly
    source: Isla_Phillips
    relation: :hasMother
  AddTriple (8aface85-3146-46a5-b5d6-d62ed34553ac)
 Call ID: 8aface85-3146-46a5-b5d6-d62ed34553ac
  Args:
    target: Peter_Phillips
    relation: :hasFather
    source: Isla_Phillips
  AssignClass (e0ccaf13-ab05-4a7f-902c-f2070a14eba3)
 Call ID: e0ccaf13-ab05-4a7f-902c-f2070a14eba3
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (a040377a-a72d-4248-a602-988a6f01f5d0)
 Call ID: a040377a-a72d-4248-a602-988a6f01f5d0
  Args:
    type: :Person
    source: Harriet_Sperling
  AssignClass (56170e62-c125-4b3f-8215-32e73d0cf8ee)
 Call ID: 56170e62-c125-4b3f-8215-32e73d0cf8ee
  Args:
    type: :Man
    source: Rupert_Sanders
  AssignClass (3e793eca-3e25-4163-85fc-76fd1342ebc1)
 Call ID: 3e793eca-3e25-4163-85fc-76fd1342ebc1
  Args:
    type: :Person
    source: Rupert_Sanders
  AddTriple (45cc1c25-5a2a-4522-80aa-b23b7bb1972f)
 Call ID: 45cc1c25-5a2a-4522-80aa-b23b7bb1972f
  Args:
    relation: :hasFather
    source: Harriet_Sperling
    target: Rupert_Sanders
  Finish (7d07d0a6-280d-43fb-9c46-47417f8a928f)
 Call ID: 7d07d0a6-280d-43fb-9c46-47417f8a928f
  Args: