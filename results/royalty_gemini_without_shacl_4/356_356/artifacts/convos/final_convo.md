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
  AssignClass (84d48b98-1929-40a7-b0bb-d616ece53e42)
 Call ID: 84d48b98-1929-40a7-b0bb-d616ece53e42
  Args:
    type: :Man
    source: Peter_Phillips
  AssignClass (ed9f67c1-b3fb-41f9-ae77-ed2fb9f71f69)
 Call ID: ed9f67c1-b3fb-41f9-ae77-ed2fb9f71f69
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (ea866cc4-5cc7-4072-aa25-b316e77c384e)
 Call ID: ea866cc4-5cc7-4072-aa25-b316e77c384e
  Args:
    source: Mark_Phillips
    type: :Man
  AssignClass (cddbddcb-63c9-4a23-a749-2767fbcba2a3)
 Call ID: cddbddcb-63c9-4a23-a749-2767fbcba2a3
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (25d91411-d2dd-4b5c-a584-eca82a1c9532)
 Call ID: 25d91411-d2dd-4b5c-a584-eca82a1c9532
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (b6fc2616-ecaf-4761-b767-c3506f9e5f9b)
 Call ID: b6fc2616-ecaf-4761-b767-c3506f9e5f9b
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (997f5b0b-9083-4dea-809e-d23d4a74c617)
 Call ID: 997f5b0b-9083-4dea-809e-d23d4a74c617
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (313d220d-4330-44bc-ab82-702406fed246)
 Call ID: 313d220d-4330-44bc-ab82-702406fed246
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (fff43166-2728-4954-86bc-be2c72aa0639)
 Call ID: fff43166-2728-4954-86bc-be2c72aa0639
  Args:
    source: Heather_Tonkin
    type: :Woman
  AssignClass (5e847dd6-3f2d-4294-b682-669f2e4fef1d)
 Call ID: 5e847dd6-3f2d-4294-b682-669f2e4fef1d
  Args:
    source: Stephanie_Phillips
    type: :Woman
  AssignClass (7aa8df3a-a38f-44c2-afc7-afa8012b77c7)
 Call ID: 7aa8df3a-a38f-44c2-afc7-afa8012b77c7
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (cce17820-acf8-454c-a6a8-9ef9171b33c9)
 Call ID: cce17820-acf8-454c-a6a8-9ef9171b33c9
  Args:
    source: Autumn_Kelly
    type: :Woman
  AssignClass (068f888e-5222-4f29-9115-c2fedaaf0ad2)
 Call ID: 068f888e-5222-4f29-9115-c2fedaaf0ad2
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (c149aaa0-9929-4ea2-9915-52417e99ccb5)
 Call ID: c149aaa0-9929-4ea2-9915-52417e99ccb5
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (eae02f13-591e-44c8-a296-ee09cd9ccd4b)
 Call ID: eae02f13-591e-44c8-a296-ee09cd9ccd4b
  Args:
    source: Lindsay_Wallace
    type: :Woman
  AssignClass (26adb8a0-bc07-4e20-b1be-9718303e63c9)
 Call ID: 26adb8a0-bc07-4e20-b1be-9718303e63c9
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (b7c38ee7-fd26-4f2c-b3cc-876092e23b36)
 Call ID: b7c38ee7-fd26-4f2c-b3cc-876092e23b36
  Args:
    source: Rupert_Sanders
    type: :Man
  AssignClass (12f35179-5bdb-4edd-a13d-cd1125b07cb3)
 Call ID: 12f35179-5bdb-4edd-a13d-cd1125b07cb3
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    type: :Man
  AddLiteral (79084d7b-1d81-4958-8d65-fbf7852f0ad6)
 Call ID: 79084d7b-1d81-4958-8d65-fbf7852f0ad6
  Args:
    literal_type: xsd:integer
    source: Peter_Phillips
    relation: :hasBirthYear
    literal_value: 1977
  AddLiteral (1b64665c-affe-495e-a245-0c6506e80de2)
 Call ID: 1b64665c-affe-495e-a245-0c6506e80de2
  Args:
    literal_value: 1981
    relation: :hasBirthYear
    source: Zara_Tindall
    literal_type: xsd:integer
  AddLiteral (b44d82bc-2dd7-490e-82d9-9838f0859188)
 Call ID: b44d82bc-2dd7-490e-82d9-9838f0859188
  Args:
    literal_value: 1985
    relation: :hasBirthYear
    source: Felicity_Wade
    literal_type: xsd:integer
  AddLiteral (3ae8cc49-3e43-4441-a889-c6fe3dc0711f)
 Call ID: 3ae8cc49-3e43-4441-a889-c6fe3dc0711f
  Args:
    literal_type: xsd:integer
    source: Stephanie_Phillips
    relation: :hasBirthYear
    literal_value: 1997
  AddLiteral (24068e66-8f9c-4d82-83d3-1724e1b3fe65)
 Call ID: 24068e66-8f9c-4d82-83d3-1724e1b3fe65
  Args:
    literal_type: xsd:integer
    source: Harriet_Sperling
    relation: :hasBirthYear
    literal_value: 1980
  AddLiteral (0046cd78-16f0-4149-bb57-3787659d4aab)
 Call ID: 0046cd78-16f0-4149-bb57-3787659d4aab
  Args:
    relation: :hasBirthYear
    literal_value: 1946
    literal_type: xsd:integer
    source: Rupert_Sanders
  AddLiteral (4d3c1a05-882e-41b2-9bdb-e51d9a92a522)
 Call ID: 4d3c1a05-882e-41b2-9bdb-e51d9a92a522
  Args:
    relation: :hasDeathYear
    literal_value: 2023
    literal_type: xsd:integer
    source: Rupert_Sanders
  AddTriple (0263d5a1-9dfb-4dbd-9d80-269e1bfb3da9)
 Call ID: 0263d5a1-9dfb-4dbd-9d80-269e1bfb3da9
  Args:
    source: Peter_Phillips
    target: Mark_Phillips
    relation: :hasFather
  AddTriple (97093679-7aad-42a5-8e88-d93d8cb6af31)
 Call ID: 97093679-7aad-42a5-8e88-d93d8cb6af31
  Args:
    target: Anne_Princess_Royal
    source: Peter_Phillips
    relation: :hasMother
  AddTriple (e65cdaac-55c9-4def-a8ab-c9c0723dff3a)
 Call ID: e65cdaac-55c9-4def-a8ab-c9c0723dff3a
  Args:
    source: Zara_Tindall
    target: Mark_Phillips
    relation: :hasFather
  AddTriple (3f68f765-d1b5-4509-9ba9-bac8b64797bd)
 Call ID: 3f68f765-d1b5-4509-9ba9-bac8b64797bd
  Args:
    target: Anne_Princess_Royal
    source: Zara_Tindall
    relation: :hasMother
  AddTriple (0f5fe54a-3c5f-4d26-a731-f8ca8f160943)
 Call ID: 0f5fe54a-3c5f-4d26-a731-f8ca8f160943
  Args:
    relation: :hasFather
    source: Felicity_Wade
    target: Mark_Phillips
  AddTriple (fe40a2b9-4be1-4358-8961-30f29c1fe418)
 Call ID: fe40a2b9-4be1-4358-8961-30f29c1fe418
  Args:
    relation: :hasMother
    target: Heather_Tonkin
    source: Felicity_Wade
  AddTriple (8a5d0822-15fc-49d2-9f10-e0c9c649bfef)
 Call ID: 8a5d0822-15fc-49d2-9f10-e0c9c649bfef
  Args:
    relation: :hasFather
    source: Stephanie_Phillips
    target: Mark_Phillips
  AddTriple (51fefc6a-5146-48da-bcf9-17d031682a2a)
 Call ID: 51fefc6a-5146-48da-bcf9-17d031682a2a
  Args:
    relation: :hasMother
    target: Sandy_Pflueger
    source: Stephanie_Phillips
  AddTriple (98e73ae0-b205-47de-9a37-b4222d6e4ed2)
 Call ID: 98e73ae0-b205-47de-9a37-b4222d6e4ed2
  Args:
    source: Anne_Princess_Royal
    target: Prince_Philip
    relation: :hasFather
  AddTriple (ebd814b2-9628-4cda-b0b7-16d1f053ca33)
 Call ID: ebd814b2-9628-4cda-b0b7-16d1f053ca33
  Args:
    target: Queen_Elizabeth_II
    source: Anne_Princess_Royal
    relation: :hasMother
  AddTriple (4bdd2073-c56f-4961-809a-524390fcf7dc)
 Call ID: 4bdd2073-c56f-4961-809a-524390fcf7dc
  Args:
    relation: :hasFather
    source: King_Charles_III
    target: Prince_Philip
  AddTriple (548e7f33-93fd-4aca-accd-ace2a0d250f2)
 Call ID: 548e7f33-93fd-4aca-accd-ace2a0d250f2
  Args:
    target: Queen_Elizabeth_II
    source: King_Charles_III
    relation: :hasMother
  AddTriple (b19ce6da-d4f2-436d-bb17-583d27f1f436)
 Call ID: b19ce6da-d4f2-436d-bb17-583d27f1f436
  Args:
    source: Savannah_Phillips
    target: Peter_Phillips
    relation: :hasFather
  AddTriple (67dc73bf-2680-4178-950f-f1e22eee0a2a)
 Call ID: 67dc73bf-2680-4178-950f-f1e22eee0a2a
  Args:
    relation: :hasMother
    target: Autumn_Kelly
    source: Savannah_Phillips
  AddTriple (026fc472-f5ec-486f-b2dd-9052b6d78e9a)
 Call ID: 026fc472-f5ec-486f-b2dd-9052b6d78e9a
  Args:
    relation: :hasFather
    source: Isla_Phillips
    target: Peter_Phillips
  AddTriple (eaf96719-0fab-4aff-b313-f48ab8585ab8)
 Call ID: eaf96719-0fab-4aff-b313-f48ab8585ab8
  Args:
    target: Autumn_Kelly
    source: Isla_Phillips
    relation: :hasMother
  AddTriple (b9a1cfe8-9975-45ec-add8-2a2481fc7ea2)
 Call ID: b9a1cfe8-9975-45ec-add8-2a2481fc7ea2
  Args:
    source: Harriet_Sperling
    target: Rupert_Sanders
    relation: :hasFather
  Finish (8dd7c2a0-f41e-499f-84aa-5d2af0bddb6e)
 Call ID: 8dd7c2a0-f41e-499f-84aa-5d2af0bddb6e
  Args: