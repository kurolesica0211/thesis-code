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
  AssignClass (dde141d7-ecd1-442f-9bea-b39d2ac70593)
 Call ID: dde141d7-ecd1-442f-9bea-b39d2ac70593
  Args:
    source: Peter_Phillips
    type: :Man
  AssignClass (df41cda6-8eb9-4af6-9f7f-ecc6ba929da4)
 Call ID: df41cda6-8eb9-4af6-9f7f-ecc6ba929da4
  Args:
    type: :Person
    source: Peter_Phillips
  AddLiteral (50b86a7b-b8c6-46f1-bf7d-c7be4b858eca)
 Call ID: 50b86a7b-b8c6-46f1-bf7d-c7be4b858eca
  Args:
    literal_value: 1977
    literal_type: xsd:integer
    source: Peter_Phillips
    relation: :hasBirthYear
  AssignClass (6871a44d-d158-4280-98b4-553828dabb92)
 Call ID: 6871a44d-d158-4280-98b4-553828dabb92
  Args:
    source: Anne_Princess_Royal
    type: :Woman
  AssignClass (9b83c7eb-7b93-4ab2-aaf0-53d755165b71)
 Call ID: 9b83c7eb-7b93-4ab2-aaf0-53d755165b71
  Args:
    type: :Person
    source: Anne_Princess_Royal
  AssignClass (1b83555d-2d22-4cec-be8c-cbc73f55620b)
 Call ID: 1b83555d-2d22-4cec-be8c-cbc73f55620b
  Args:
    type: :Man
    source: Mark_Phillips
  AssignClass (1d13d141-e51c-4e35-bc3b-80e95bbfe318)
 Call ID: 1d13d141-e51c-4e35-bc3b-80e95bbfe318
  Args:
    source: Mark_Phillips
    type: :Person
  AddTriple (50d440b5-61af-4f5c-8c77-2b25c5a02202)
 Call ID: 50d440b5-61af-4f5c-8c77-2b25c5a02202
  Args:
    relation: :hasMother
    source: Peter_Phillips
    target: Anne_Princess_Royal
  AddTriple (5377d398-1972-41b8-8759-a56d0df99338)
 Call ID: 5377d398-1972-41b8-8759-a56d0df99338
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Peter_Phillips
  AssignClass (64f53c4b-2f4c-40fd-8926-f25b650af601)
 Call ID: 64f53c4b-2f4c-40fd-8926-f25b650af601
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (096d22a9-97a7-49be-b9b6-96b68e0bfce4)
 Call ID: 096d22a9-97a7-49be-b9b6-96b68e0bfce4
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (ed2b50a3-4e42-4582-95ab-98df0ecabf54)
 Call ID: ed2b50a3-4e42-4582-95ab-98df0ecabf54
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (0ee81b7e-2e2e-4745-ba26-4e636a6f40a1)
 Call ID: 0ee81b7e-2e2e-4745-ba26-4e636a6f40a1
  Args:
    type: :Person
    source: Prince_Philip
  AddTriple (067a808f-8deb-476e-bae2-9648cca1bfe0)
 Call ID: 067a808f-8deb-476e-bae2-9648cca1bfe0
  Args:
    relation: :hasMother
    target: Queen_Elizabeth_II
    source: Anne_Princess_Royal
  AddTriple (72bf1384-6341-43a9-a032-956f1a0b93e1)
 Call ID: 72bf1384-6341-43a9-a032-956f1a0b93e1
  Args:
    source: Anne_Princess_Royal
    target: Prince_Philip
    relation: :hasFather
  AssignClass (c3277f78-bfa9-4036-8fd1-73ff37455765)
 Call ID: c3277f78-bfa9-4036-8fd1-73ff37455765
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (8cba8d7f-57dd-4574-a829-375aa7caadb6)
 Call ID: 8cba8d7f-57dd-4574-a829-375aa7caadb6
  Args:
    type: :Person
    source: Zara_Tindall
  AddTriple (3bab8ee6-2d5c-41e9-a26c-4b04e5a9c15e)
 Call ID: 3bab8ee6-2d5c-41e9-a26c-4b04e5a9c15e
  Args:
    relation: :isSiblingOf
    target: Zara_Tindall
    source: Peter_Phillips
  AddTriple (37592b04-4002-4267-b530-3cb633a5fc1c)
 Call ID: 37592b04-4002-4267-b530-3cb633a5fc1c
  Args:
    relation: :hasMother
    source: Zara_Tindall
    target: Anne_Princess_Royal
  AddTriple (0aca2541-edd4-4aa8-844d-825c97fe1921)
 Call ID: 0aca2541-edd4-4aa8-844d-825c97fe1921
  Args:
    relation: :hasFather
    source: Zara_Tindall
    target: Mark_Phillips
  AssignClass (2f4e5039-c195-4b09-82b8-55901cbc8fe6)
 Call ID: 2f4e5039-c195-4b09-82b8-55901cbc8fe6
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (8ee3f39d-5974-4365-8f18-fbf7de534369)
 Call ID: 8ee3f39d-5974-4365-8f18-fbf7de534369
  Args:
    type: :Person
    source: Autumn_Kelly
  AddTriple (0db5577e-de95-4cf5-8d00-f0f84ff8a9f2)
 Call ID: 0db5577e-de95-4cf5-8d00-f0f84ff8a9f2
  Args:
    target: Autumn_Kelly
    source: Peter_Phillips
    relation: :hasRelation
  AddLiteral (5fc13faa-787d-4cd6-b56d-ad310ed4be0e)
 Call ID: 5fc13faa-787d-4cd6-b56d-ad310ed4be0e
  Args:
    literal_type: xsd:integer
    source: Peter_Phillips
    relation: :hasMarriageYear
    literal_value: 2008
  AssignClass (e413621d-4ce3-4f9e-9af3-10f7bf1f796a)
 Call ID: e413621d-4ce3-4f9e-9af3-10f7bf1f796a
  Args:
    source: Savannah_Phillips
    type: :Woman
  AssignClass (44809d54-47ec-45e2-85b0-f650fe2f3cf2)
 Call ID: 44809d54-47ec-45e2-85b0-f650fe2f3cf2
  Args:
    source: Savannah_Phillips
    type: :Person
  AssignClass (4c9958a8-e681-4296-a097-9cc2deb34d6a)
 Call ID: 4c9958a8-e681-4296-a097-9cc2deb34d6a
  Args:
    type: :Woman
    source: Isla_Phillips
  AssignClass (d3c8aee9-2a76-42b4-b137-c3bf0c474d75)
 Call ID: d3c8aee9-2a76-42b4-b137-c3bf0c474d75
  Args:
    type: :Person
    source: Isla_Phillips
  AddTriple (f521b294-9ff5-4bea-9799-627ada198d4d)
 Call ID: f521b294-9ff5-4bea-9799-627ada198d4d
  Args:
    source: Savannah_Phillips
    target: Autumn_Kelly
    relation: :hasMother
  AddTriple (f89852ff-f080-446f-9e50-b8ed78d29d5c)
 Call ID: f89852ff-f080-446f-9e50-b8ed78d29d5c
  Args:
    source: Savannah_Phillips
    target: Peter_Phillips
    relation: :hasFather
  AddTriple (7928b414-c94c-4b4c-9577-13b3e2494bd8)
 Call ID: 7928b414-c94c-4b4c-9577-13b3e2494bd8
  Args:
    relation: :hasMother
    target: Autumn_Kelly
    source: Isla_Phillips
  AddTriple (d1c293fc-6cbb-45d5-ae74-0511fbf7c0cf)
 Call ID: d1c293fc-6cbb-45d5-ae74-0511fbf7c0cf
  Args:
    relation: :hasFather
    source: Isla_Phillips
    target: Peter_Phillips
  AssignClass (cec0f85b-e684-4d7b-89db-3aed4f769d1d)
 Call ID: cec0f85b-e684-4d7b-89db-3aed4f769d1d
  Args:
    type: :Woman
    source: Felicity_Wade
  AssignClass (9711d813-8287-440d-8f32-fc291a4e2fb5)
 Call ID: 9711d813-8287-440d-8f32-fc291a4e2fb5
  Args:
    type: :Person
    source: Felicity_Wade
  AssignClass (8f15b0d1-358f-4bdd-a04d-f03c1574c92b)
 Call ID: 8f15b0d1-358f-4bdd-a04d-f03c1574c92b
  Args:
    source: Stephanie_Phillips
    type: :Woman
  AssignClass (2c2fe1eb-d382-4790-9b45-0b0f8793fedd)
 Call ID: 2c2fe1eb-d382-4790-9b45-0b0f8793fedd
  Args:
    source: Stephanie_Phillips
    type: :Person
  AddTriple (3e8295bd-6088-4fd5-83c2-fd9cbea7b1a8)
 Call ID: 3e8295bd-6088-4fd5-83c2-fd9cbea7b1a8
  Args:
    target: Mark_Phillips
    source: Felicity_Wade
    relation: :hasFather
  AddTriple (e525165a-3702-4c0a-9938-0305e98fc21b)
 Call ID: e525165a-3702-4c0a-9938-0305e98fc21b
  Args:
    target: Mark_Phillips
    source: Stephanie_Phillips
    relation: :hasFather
  AssignClass (09dbdaa4-a362-4d16-8b51-31f7706cd825)
 Call ID: 09dbdaa4-a362-4d16-8b51-31f7706cd825
  Args:
    type: :Woman
    source: Heather_Tonkin
  AssignClass (a7006c0a-6fb5-450e-b671-3d88877dd50f)
 Call ID: a7006c0a-6fb5-450e-b671-3d88877dd50f
  Args:
    source: Heather_Tonkin
    type: :Person
  AddTriple (1b1b69b3-2d05-420a-b9ae-deeb1c341262)
 Call ID: 1b1b69b3-2d05-420a-b9ae-deeb1c341262
  Args:
    source: Felicity_Wade
    target: Heather_Tonkin
    relation: :hasMother
  AssignClass (4d602d94-6a95-44a2-8f88-8f97a8e6bad5)
 Call ID: 4d602d94-6a95-44a2-8f88-8f97a8e6bad5
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (dc307aa2-02ac-41e7-a94b-de73e5cca310)
 Call ID: dc307aa2-02ac-41e7-a94b-de73e5cca310
  Args:
    type: :Person
    source: Sandy_Pflueger
  AddTriple (5d82a765-7f96-4097-b7b3-7a5576adf2a7)
 Call ID: 5d82a765-7f96-4097-b7b3-7a5576adf2a7
  Args:
    source: Stephanie_Phillips
    target: Sandy_Pflueger
    relation: :hasMother
  AssignClass (79f9067e-ae68-4c6b-9140-8d0ea5bc254c)
 Call ID: 79f9067e-ae68-4c6b-9140-8d0ea5bc254c
  Args:
    type: :Woman
    source: Lindsay_Wallace
  AssignClass (83d7673b-bb4f-41e0-812c-5d208fab886b)
 Call ID: 83d7673b-bb4f-41e0-812c-5d208fab886b
  Args:
    source: Lindsay_Wallace
    type: :Person
  AddTriple (a9d61565-ccd3-430f-87ae-2eb9c0e2d495)
 Call ID: a9d61565-ccd3-430f-87ae-2eb9c0e2d495
  Args:
    relation: :hasRelation
    source: Peter_Phillips
    target: Lindsay_Wallace
  AssignClass (25783064-3d6a-4861-bbf8-9fb2fa06c6a2)
 Call ID: 25783064-3d6a-4861-bbf8-9fb2fa06c6a2
  Args:
    type: :Woman
    source: Harriet_Sperling
  AssignClass (a1817a38-978e-4b74-b97a-612314f7194a)
 Call ID: a1817a38-978e-4b74-b97a-612314f7194a
  Args:
    type: :Person
    source: Harriet_Sperling
  AddTriple (c26e1f65-addd-4792-83af-31c4ee09612f)
 Call ID: c26e1f65-addd-4792-83af-31c4ee09612f
  Args:
    relation: :hasRelation
    target: Harriet_Sperling
    source: Peter_Phillips
  AssignClass (61c2710e-674f-42c7-a668-8d84f13573b4)
 Call ID: 61c2710e-674f-42c7-a668-8d84f13573b4
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (0ca651f0-ae56-48b9-b596-18bf29972a8d)
 Call ID: 0ca651f0-ae56-48b9-b596-18bf29972a8d
  Args:
    source: King_Charles_III
    type: :Person
  AddTriple (c975644e-e887-431f-85ba-eb3a50b099e0)
 Call ID: c975644e-e887-431f-85ba-eb3a50b099e0
  Args:
    source: Anne_Princess_Royal
    target: King_Charles_III
    relation: :isSiblingOf
  Finish (8cf6586b-2c34-463b-85c6-830488558514)
 Call ID: 8cf6586b-2c34-463b-85c6-830488558514
  Args: