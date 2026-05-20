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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (27c48a57-218b-4025-b75f-2c3e08914bfd)
 Call ID: 27c48a57-218b-4025-b75f-2c3e08914bfd
  Args:
    source: Peter_Phillips
    type: :Man
  AssignClass (72056fe5-3e02-438a-b1ed-8b048438d050)
 Call ID: 72056fe5-3e02-438a-b1ed-8b048438d050
  Args:
    source: Peter_Phillips
    type: :Person
  AddLiteral (dc84e5e8-2b00-469d-8cef-c3c72fe65029)
 Call ID: dc84e5e8-2b00-469d-8cef-c3c72fe65029
  Args:
    source: Peter_Phillips
    literal_value: 1977
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (4d77846d-7ff0-4fef-a4a5-d92627a9a3bf)
 Call ID: 4d77846d-7ff0-4fef-a4a5-d92627a9a3bf
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (73c188e5-f64c-4641-84de-ab81cc236296)
 Call ID: 73c188e5-f64c-4641-84de-ab81cc236296
  Args:
    type: :Person
    source: Anne_Princess_Royal
  AssignClass (69bb487c-08a8-42c0-9495-d40165712ee0)
 Call ID: 69bb487c-08a8-42c0-9495-d40165712ee0
  Args:
    source: Mark_Phillips
    type: :Man
  AssignClass (a8d8dd83-e32f-41af-b1c9-37a2cd908a5a)
 Call ID: a8d8dd83-e32f-41af-b1c9-37a2cd908a5a
  Args:
    source: Mark_Phillips
    type: :Person
  AddTriple (4a2fd2f3-9b96-4b71-8143-97e6f2d67a30)
 Call ID: 4a2fd2f3-9b96-4b71-8143-97e6f2d67a30
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Peter_Phillips
  AddTriple (953e656e-fa9d-48c4-84ea-f280e9ec15d6)
 Call ID: 953e656e-fa9d-48c4-84ea-f280e9ec15d6
  Args:
    target: Anne_Princess_Royal
    source: Peter_Phillips
    relation: :hasMother
  AssignClass (98697df7-ed04-4b2d-9f9c-88142c169743)
 Call ID: 98697df7-ed04-4b2d-9f9c-88142c169743
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (5344ce04-bda6-401c-b835-6b6c50db9c8d)
 Call ID: 5344ce04-bda6-401c-b835-6b6c50db9c8d
  Args:
    source: King_Charles_III
    type: :Person
  AddTriple (9240c3db-8552-4580-b5e0-7786c4d00bd6)
 Call ID: 9240c3db-8552-4580-b5e0-7786c4d00bd6
  Args:
    relation: :hasRelation
    source: Peter_Phillips
    target: King_Charles_III
  AssignClass (dd5f158c-a381-49ce-8056-663361b4385a)
 Call ID: dd5f158c-a381-49ce-8056-663361b4385a
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (5d137040-2125-49f3-9b37-95704e91584f)
 Call ID: 5d137040-2125-49f3-9b37-95704e91584f
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (e0d4fcc0-65a8-4827-9442-0aa5a481cd76)
 Call ID: e0d4fcc0-65a8-4827-9442-0aa5a481cd76
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (518ff9d3-9d4c-4b7b-851c-2062b9eb7e7c)
 Call ID: 518ff9d3-9d4c-4b7b-851c-2062b9eb7e7c
  Args:
    source: Prince_Philip
    type: :Person
  AssignClass (d31de7fc-0477-4f1e-8dfd-642e575646a6)
 Call ID: d31de7fc-0477-4f1e-8dfd-642e575646a6
  Args:
    source: Zara_Tindall
    type: :Woman
  AssignClass (c3198de8-45a8-4cbe-b100-54376e5988de)
 Call ID: c3198de8-45a8-4cbe-b100-54376e5988de
  Args:
    source: Zara_Tindall
    type: :Person
  AddTriple (c28ae16c-ecdc-4131-9542-5ccd00424bd5)
 Call ID: c28ae16c-ecdc-4131-9542-5ccd00424bd5
  Args:
    target: Peter_Phillips
    source: Zara_Tindall
    relation: :isSisterOf
  AssignClass (35020cb9-a204-42e1-97e2-7298237c4185)
 Call ID: 35020cb9-a204-42e1-97e2-7298237c4185
  Args:
    source: Felicity_Wade
    type: :Woman
  AssignClass (682cfe36-c462-4983-a10f-3942e274038c)
 Call ID: 682cfe36-c462-4983-a10f-3942e274038c
  Args:
    type: :Person
    source: Felicity_Wade
  AddTriple (d86ea383-ab84-4173-b596-5f79492d465b)
 Call ID: d86ea383-ab84-4173-b596-5f79492d465b
  Args:
    relation: :hasFather
    source: Felicity_Wade
    target: Mark_Phillips
  AssignClass (113485b7-4e58-4f60-95a0-e18c6b7edad2)
 Call ID: 113485b7-4e58-4f60-95a0-e18c6b7edad2
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (1bdc6b47-fac0-4cae-9fa9-15936f7084da)
 Call ID: 1bdc6b47-fac0-4cae-9fa9-15936f7084da
  Args:
    source: Stephanie_Phillips
    type: :Person
  AddTriple (8d019908-16b9-4957-9465-5be8b2c2004f)
 Call ID: 8d019908-16b9-4957-9465-5be8b2c2004f
  Args:
    target: Mark_Phillips
    source: Stephanie_Phillips
    relation: :hasFather
  AssignClass (439a15f3-372f-4e79-8f67-c3dc174a6b1f)
 Call ID: 439a15f3-372f-4e79-8f67-c3dc174a6b1f
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (e0572cea-3f04-495b-8146-39bf46bea872)
 Call ID: e0572cea-3f04-495b-8146-39bf46bea872
  Args:
    type: :Person
    source: Autumn_Kelly
  AddLiteral (144cabfc-817d-40f0-8976-93764d1d8fae)
 Call ID: 144cabfc-817d-40f0-8976-93764d1d8fae
  Args:
    literal_value: 2008
    source: Peter_Phillips
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (a3d56998-319f-4f55-bcc3-f2cb86fd2454)
 Call ID: a3d56998-319f-4f55-bcc3-f2cb86fd2454
  Args:
    source: Peter_Phillips
    target: Autumn_Kelly
    relation: :hasRelation
  AssignClass (a7cda64a-1e9e-4a0c-b646-9eb9408893ae)
 Call ID: a7cda64a-1e9e-4a0c-b646-9eb9408893ae
  Args:
    type: :Woman
    source: Savannah_Phillips
  AssignClass (c0efbf82-80a1-4b3f-bc3b-6abe0367882e)
 Call ID: c0efbf82-80a1-4b3f-bc3b-6abe0367882e
  Args:
    type: :Person
    source: Savannah_Phillips
  AddTriple (9611c25b-d3ae-4448-b12a-3dc160eb4cef)
 Call ID: 9611c25b-d3ae-4448-b12a-3dc160eb4cef
  Args:
    relation: :hasFather
    target: Peter_Phillips
    source: Savannah_Phillips
  AddTriple (5d95b2ed-a793-40f9-896e-bdf136ef282f)
 Call ID: 5d95b2ed-a793-40f9-896e-bdf136ef282f
  Args:
    relation: :hasMother
    source: Savannah_Phillips
    target: Autumn_Kelly
  AssignClass (01e7f0ab-a4ae-4d8d-813c-b5f7d79882dc)
 Call ID: 01e7f0ab-a4ae-4d8d-813c-b5f7d79882dc
  Args:
    source: Isla_Phillips
    type: :Woman
  AssignClass (9aee713a-b23c-45c0-8291-7b7614fa5229)
 Call ID: 9aee713a-b23c-45c0-8291-7b7614fa5229
  Args:
    type: :Person
    source: Isla_Phillips
  AddTriple (8640c867-af5e-4b42-98a5-8bb6a9996f47)
 Call ID: 8640c867-af5e-4b42-98a5-8bb6a9996f47
  Args:
    relation: :hasFather
    target: Peter_Phillips
    source: Isla_Phillips
  AddTriple (433089b5-2958-4360-9496-c3ace4825006)
 Call ID: 433089b5-2958-4360-9496-c3ace4825006
  Args:
    relation: :hasMother
    source: Isla_Phillips
    target: Autumn_Kelly
  AssignClass (18039837-5abc-47b2-b2c4-66e1603d2028)
 Call ID: 18039837-5abc-47b2-b2c4-66e1603d2028
  Args:
    source: Lindsay_Wallace
    type: :Woman
  AssignClass (d71b5b43-7494-4280-a4d6-0564b3e59c59)
 Call ID: d71b5b43-7494-4280-a4d6-0564b3e59c59
  Args:
    type: :Person
    source: Lindsay_Wallace
  AddTriple (a3708ab8-17f3-4fcb-b9c7-33d073d97492)
 Call ID: a3708ab8-17f3-4fcb-b9c7-33d073d97492
  Args:
    source: Peter_Phillips
    target: Lindsay_Wallace
    relation: :hasRelation
  AssignClass (39a3547e-c499-47dd-a8f0-c3831676f8ae)
 Call ID: 39a3547e-c499-47dd-a8f0-c3831676f8ae
  Args:
    source: Harriet_Sperling
    type: :Woman
  AssignClass (033dd8c0-0b4c-47a6-a7f9-65b4cebafc77)
 Call ID: 033dd8c0-0b4c-47a6-a7f9-65b4cebafc77
  Args:
    source: Harriet_Sperling
    type: :Person
  AddTriple (92d3df87-3409-462f-8ec4-7a3376593cf3)
 Call ID: 92d3df87-3409-462f-8ec4-7a3376593cf3
  Args:
    target: Harriet_Sperling
    source: Peter_Phillips
    relation: :hasRelation
  Finish (7845424f-4f3b-4f84-815d-bbe2f65443ae)
 Call ID: 7845424f-4f3b-4f84-815d-bbe2f65443ae
  Args: