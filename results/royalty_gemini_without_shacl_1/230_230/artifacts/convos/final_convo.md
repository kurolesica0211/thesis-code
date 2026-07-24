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
  AssignClass (e1545d08-cc0e-45b5-87a6-ed44ac2e2c47)
 Call ID: e1545d08-cc0e-45b5-87a6-ed44ac2e2c47
  Args:
    source: Peter_Phillips
    type: :Man
  AssignClass (86bcc90d-10aa-4e9d-9930-f1e40cdf0b6c)
 Call ID: 86bcc90d-10aa-4e9d-9930-f1e40cdf0b6c
  Args:
    source: Peter_Phillips
    type: :Person
  AddLiteral (e0de2835-792f-458b-87b5-0eae7b9b5e7c)
 Call ID: e0de2835-792f-458b-87b5-0eae7b9b5e7c
  Args:
    literal_type: xsd:integer
    literal_value: 1977
    relation: :hasBirthYear
    source: Peter_Phillips
  AssignClass (24e203fc-3f6b-4956-ae8e-423732cae2fa)
 Call ID: 24e203fc-3f6b-4956-ae8e-423732cae2fa
  Args:
    source: Anne_Princess_Royal
    type: :Woman
  AssignClass (a5dbf9b9-fc19-456f-aa09-331e97ac5a8e)
 Call ID: a5dbf9b9-fc19-456f-aa09-331e97ac5a8e
  Args:
    source: Anne_Princess_Royal
    type: :Person
  AssignClass (4bc7ebb1-d588-4f7a-b8ef-53e64daf7b27)
 Call ID: 4bc7ebb1-d588-4f7a-b8ef-53e64daf7b27
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (b16887c9-eb39-41fb-85ee-1d2e397dd49f)
 Call ID: b16887c9-eb39-41fb-85ee-1d2e397dd49f
  Args:
    type: :Person
    source: Mark_Phillips
  AddTriple (54d9ee49-aa08-4be3-becd-ba8011b2c555)
 Call ID: 54d9ee49-aa08-4be3-becd-ba8011b2c555
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Peter_Phillips
  AddTriple (7a9f00d3-ab1f-4f55-83db-a014caa552aa)
 Call ID: 7a9f00d3-ab1f-4f55-83db-a014caa552aa
  Args:
    target: Anne_Princess_Royal
    source: Peter_Phillips
    relation: :hasMother
  AssignClass (c9a3cd74-c918-4108-8510-93e65f2a7550)
 Call ID: c9a3cd74-c918-4108-8510-93e65f2a7550
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (7a6b1b7f-f051-45bb-b99b-41258cba7411)
 Call ID: 7a6b1b7f-f051-45bb-b99b-41258cba7411
  Args:
    type: :Person
    source: King_Charles_III
  AddTriple (d7582ab4-5728-4ed6-9626-c7cbb7376d71)
 Call ID: d7582ab4-5728-4ed6-9626-c7cbb7376d71
  Args:
    source: Peter_Phillips
    target: King_Charles_III
    relation: :hasRelation
  AssignClass (d18b7b99-931f-4a0e-89a8-5b1027d49d7e)
 Call ID: d18b7b99-931f-4a0e-89a8-5b1027d49d7e
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (d18c460a-ef7d-414f-831d-cc5ad3a0a649)
 Call ID: d18c460a-ef7d-414f-831d-cc5ad3a0a649
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (9290bc02-23d2-4772-93d1-25b73c5f33d3)
 Call ID: 9290bc02-23d2-4772-93d1-25b73c5f33d3
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (27b7eb80-8d16-4e30-9502-0e2a08f447af)
 Call ID: 27b7eb80-8d16-4e30-9502-0e2a08f447af
  Args:
    source: Prince_Philip
    type: :Person
  AssignClass (a8780497-575b-4dbc-a92f-669af9af5a19)
 Call ID: a8780497-575b-4dbc-a92f-669af9af5a19
  Args:
    source: Zara_Tindall
    type: :Woman
  AssignClass (cd7c9840-e065-467e-9bd2-d0f3873741cb)
 Call ID: cd7c9840-e065-467e-9bd2-d0f3873741cb
  Args:
    source: Zara_Tindall
    type: :Person
  AddTriple (0d50af25-6354-4c93-a203-1e1ea1f5340e)
 Call ID: 0d50af25-6354-4c93-a203-1e1ea1f5340e
  Args:
    relation: :isSisterOf
    source: Zara_Tindall
    target: Peter_Phillips
  AssignClass (631e61e3-9e71-415f-871a-082e48d32e88)
 Call ID: 631e61e3-9e71-415f-871a-082e48d32e88
  Args:
    source: Felicity_Wade
    type: :Woman
  AssignClass (b98ae4eb-3105-41d7-9902-a83c004aa140)
 Call ID: b98ae4eb-3105-41d7-9902-a83c004aa140
  Args:
    source: Felicity_Wade
    type: :Person
  AssignClass (80f3900c-2848-42af-af02-eecddadd452d)
 Call ID: 80f3900c-2848-42af-af02-eecddadd452d
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (e204a992-ad2f-4ce0-8fda-bc6d88b74844)
 Call ID: e204a992-ad2f-4ce0-8fda-bc6d88b74844
  Args:
    type: :Person
    source: Stephanie_Phillips
  AddTriple (443c2a88-716d-448b-bcec-8e83d3be46c0)
 Call ID: 443c2a88-716d-448b-bcec-8e83d3be46c0
  Args:
    source: Felicity_Wade
    target: Mark_Phillips
    relation: :hasFather
  AddTriple (4c3a5bc0-6066-49be-8ccd-742105a61df2)
 Call ID: 4c3a5bc0-6066-49be-8ccd-742105a61df2
  Args:
    relation: :hasFather
    source: Stephanie_Phillips
    target: Mark_Phillips
  AssignClass (9451079c-e1aa-402b-b69a-418b393ced46)
 Call ID: 9451079c-e1aa-402b-b69a-418b393ced46
  Args:
    source: Autumn_Kelly
    type: :Woman
  AssignClass (a5e3f755-6eb3-45f1-b325-e936ea35e8ee)
 Call ID: a5e3f755-6eb3-45f1-b325-e936ea35e8ee
  Args:
    type: :Person
    source: Autumn_Kelly
  AddLiteral (3402b4d7-1c74-472a-ba90-2a456893712a)
 Call ID: 3402b4d7-1c74-472a-ba90-2a456893712a
  Args:
    literal_value: 2008
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Peter_Phillips
  AddTriple (71df3e5f-66a9-4bed-9780-2aa39a4ed128)
 Call ID: 71df3e5f-66a9-4bed-9780-2aa39a4ed128
  Args:
    source: Peter_Phillips
    target: Autumn_Kelly
    relation: :hasRelation
  AssignClass (e2ee7fda-64f2-4ebc-8475-dcbe32645ab2)
 Call ID: e2ee7fda-64f2-4ebc-8475-dcbe32645ab2
  Args:
    type: :Woman
    source: Savannah_Anne_Kathleen_Phillips
  AssignClass (d1a0f662-aead-4673-9283-d3a1d7a81b9b)
 Call ID: d1a0f662-aead-4673-9283-d3a1d7a81b9b
  Args:
    type: :Person
    source: Savannah_Anne_Kathleen_Phillips
  AddTriple (4f1315c2-28bd-4ddc-a12e-d37d3c373e94)
 Call ID: 4f1315c2-28bd-4ddc-a12e-d37d3c373e94
  Args:
    source: Savannah_Anne_Kathleen_Phillips
    target: Peter_Phillips
    relation: :hasFather
  AddTriple (d5f2ae32-3f75-4315-a64a-a418db85f1e2)
 Call ID: d5f2ae32-3f75-4315-a64a-a418db85f1e2
  Args:
    source: Savannah_Anne_Kathleen_Phillips
    target: Autumn_Kelly
    relation: :hasMother
  AssignClass (276233e3-a8d9-4278-9f33-fbae7307e5be)
 Call ID: 276233e3-a8d9-4278-9f33-fbae7307e5be
  Args:
    type: :Woman
    source: Isla_Elizabeth_Phillips
  AssignClass (bac2f1ae-cb1d-4e62-bc94-ce530c8d218a)
 Call ID: bac2f1ae-cb1d-4e62-bc94-ce530c8d218a
  Args:
    type: :Person
    source: Isla_Elizabeth_Phillips
  AddTriple (ce98ea6d-09e0-4fca-876c-a81fec4490fd)
 Call ID: ce98ea6d-09e0-4fca-876c-a81fec4490fd
  Args:
    target: Peter_Phillips
    source: Isla_Elizabeth_Phillips
    relation: :hasFather
  AddTriple (b8bcf042-bf36-4258-bc4d-9f5c1eff0f12)
 Call ID: b8bcf042-bf36-4258-bc4d-9f5c1eff0f12
  Args:
    relation: :hasMother
    source: Isla_Elizabeth_Phillips
    target: Autumn_Kelly
  AssignClass (ae773a0f-3a8b-43f2-9b26-182bc2f2e8c3)
 Call ID: ae773a0f-3a8b-43f2-9b26-182bc2f2e8c3
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (0469b7f0-6f24-441f-83f0-1a45023814f1)
 Call ID: 0469b7f0-6f24-441f-83f0-1a45023814f1
  Args:
    source: Lindsay_Wallace
    type: :Person
  AddTriple (6948a761-9358-4e84-8c42-93f924fb9f2c)
 Call ID: 6948a761-9358-4e84-8c42-93f924fb9f2c
  Args:
    target: Lindsay_Wallace
    source: Peter_Phillips
    relation: :hasRelation
  AssignClass (f4470e11-66b2-423a-8366-ccc34af06329)
 Call ID: f4470e11-66b2-423a-8366-ccc34af06329
  Args:
    source: Harriet_Sperling
    type: :Woman
  AssignClass (9947bcbc-725b-45d7-8817-dfeec85fd3ae)
 Call ID: 9947bcbc-725b-45d7-8817-dfeec85fd3ae
  Args:
    source: Harriet_Sperling
    type: :Person
  AddTriple (2762b0b9-599d-4d59-8870-e09b6cf4c10b)
 Call ID: 2762b0b9-599d-4d59-8870-e09b6cf4c10b
  Args:
    relation: :hasRelation
    target: Harriet_Sperling
    source: Peter_Phillips
  Finish (b557ba07-aa62-4cdf-808c-167bdfa76f85)
 Call ID: b557ba07-aa62-4cdf-808c-167bdfa76f85
  Args: