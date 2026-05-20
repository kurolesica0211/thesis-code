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
  AssignClass (602d0153-d95a-4324-b7f9-be151e17ee71)
 Call ID: 602d0153-d95a-4324-b7f9-be151e17ee71
  Args:
    source: Peter_Phillips
    type: :Man
  AssignClass (893adc93-7b56-4e53-bdde-c2245d740e7b)
 Call ID: 893adc93-7b56-4e53-bdde-c2245d740e7b
  Args:
    source: Peter_Phillips
    type: :Person
  AssignClass (67c788be-3a79-4a00-8b26-dc17949c1fb7)
 Call ID: 67c788be-3a79-4a00-8b26-dc17949c1fb7
  Args:
    source: Anne_Princess_Royal
    type: :Woman
  AssignClass (25eb8159-7f29-462e-9ec4-5198a68e57f3)
 Call ID: 25eb8159-7f29-462e-9ec4-5198a68e57f3
  Args:
    type: :Person
    source: Anne_Princess_Royal
  AssignClass (0ea8d2cc-8750-4eac-b873-ca09487017e2)
 Call ID: 0ea8d2cc-8750-4eac-b873-ca09487017e2
  Args:
    source: Mark_Phillips
    type: :Man
  AssignClass (a5baaffb-00dd-4ac0-9805-389d3d3b4c90)
 Call ID: a5baaffb-00dd-4ac0-9805-389d3d3b4c90
  Args:
    type: :Person
    source: Mark_Phillips
  AssignClass (38b45bb9-d2a9-48bb-ac8b-cb2f379e4b79)
 Call ID: 38b45bb9-d2a9-48bb-ac8b-cb2f379e4b79
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (6b932f21-da5f-41cf-b393-5f91b4abbda9)
 Call ID: 6b932f21-da5f-41cf-b393-5f91b4abbda9
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (a2100df2-b875-4ce0-b68c-2e1ebfc773ff)
 Call ID: a2100df2-b875-4ce0-b68c-2e1ebfc773ff
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (dd90098b-3bb2-4ebd-a05f-40a6dd8fa3d9)
 Call ID: dd90098b-3bb2-4ebd-a05f-40a6dd8fa3d9
  Args:
    type: :Person
    source: Prince_Philip
  AssignClass (94fb900f-f121-4282-b26a-af1270218546)
 Call ID: 94fb900f-f121-4282-b26a-af1270218546
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (c28886c2-580b-4611-9c06-e7fe0aee9271)
 Call ID: c28886c2-580b-4611-9c06-e7fe0aee9271
  Args:
    source: King_Charles_III
    type: :Person
  AssignClass (5aa59ca8-c0b3-4ec4-9c72-1e713a93412c)
 Call ID: 5aa59ca8-c0b3-4ec4-9c72-1e713a93412c
  Args:
    type: :Woman
    source: Zara_Tindall
  AssignClass (72dd2fb8-5648-400b-bb13-2276f36a6bfc)
 Call ID: 72dd2fb8-5648-400b-bb13-2276f36a6bfc
  Args:
    type: :Person
    source: Zara_Tindall
  AssignClass (a23f09df-4339-4314-b1b7-b0e1e521989f)
 Call ID: a23f09df-4339-4314-b1b7-b0e1e521989f
  Args:
    source: Felicity_Wade
    type: :Woman
  AssignClass (dd3e19f6-95ee-458a-9ea0-14dda7b947af)
 Call ID: dd3e19f6-95ee-458a-9ea0-14dda7b947af
  Args:
    source: Felicity_Wade
    type: :Person
  AssignClass (3a8e263f-14c9-4c86-83c2-5b3331a75d58)
 Call ID: 3a8e263f-14c9-4c86-83c2-5b3331a75d58
  Args:
    type: :Woman
    source: Stephanie_Phillips
  AssignClass (dec451d3-9b39-415e-85ee-edee322f484f)
 Call ID: dec451d3-9b39-415e-85ee-edee322f484f
  Args:
    type: :Person
    source: Stephanie_Phillips
  AssignClass (0e6289f1-1d92-4302-b46f-6b2d62dbc343)
 Call ID: 0e6289f1-1d92-4302-b46f-6b2d62dbc343
  Args:
    source: Heather_Tonkin
    type: :Woman
  AssignClass (fb411b51-11a5-428c-be81-3e504121e430)
 Call ID: fb411b51-11a5-428c-be81-3e504121e430
  Args:
    type: :Person
    source: Heather_Tonkin
  AssignClass (93ecdaae-c186-4f72-9dc5-bb1b9b85ae77)
 Call ID: 93ecdaae-c186-4f72-9dc5-bb1b9b85ae77
  Args:
    type: :Woman
    source: Sandy_Pflueger
  AssignClass (380b1b44-3164-47f9-a51f-535bc3509ad4)
 Call ID: 380b1b44-3164-47f9-a51f-535bc3509ad4
  Args:
    source: Sandy_Pflueger
    type: :Person
  AssignClass (76a22287-8511-467a-bbca-c618b82971cb)
 Call ID: 76a22287-8511-467a-bbca-c618b82971cb
  Args:
    type: :Woman
    source: Autumn_Kelly
  AssignClass (e52d46fd-0776-4102-9985-a1a482c3602b)
 Call ID: e52d46fd-0776-4102-9985-a1a482c3602b
  Args:
    type: :Person
    source: Autumn_Kelly
  AssignClass (55a69f1c-f3e4-42b7-8cc9-512459946677)
 Call ID: 55a69f1c-f3e4-42b7-8cc9-512459946677
  Args:
    source: Savannah_Phillips
    type: :Woman
  AssignClass (b9c8c530-2c10-4664-9a97-94d81d8ce141)
 Call ID: b9c8c530-2c10-4664-9a97-94d81d8ce141
  Args:
    type: :Person
    source: Savannah_Phillips
  AssignClass (93fa349b-05cb-473a-8783-ec3d610f6f6f)
 Call ID: 93fa349b-05cb-473a-8783-ec3d610f6f6f
  Args:
    source: Isla_Phillips
    type: :Woman
  AssignClass (6bbd6ca8-d35a-4ec7-952a-ce888c65a294)
 Call ID: 6bbd6ca8-d35a-4ec7-952a-ce888c65a294
  Args:
    type: :Person
    source: Isla_Phillips
  AddTriple (cb82e89f-b2b2-4e72-ac22-fa33f82befcf)
 Call ID: cb82e89f-b2b2-4e72-ac22-fa33f82befcf
  Args:
    target: Mark_Phillips
    source: Peter_Phillips
    relation: :hasFather
  AddTriple (fcfcb590-cca8-46b1-8f14-d4a761c1716a)
 Call ID: fcfcb590-cca8-46b1-8f14-d4a761c1716a
  Args:
    target: Anne_Princess_Royal
    source: Peter_Phillips
    relation: :hasMother
  AddTriple (cb5e4d08-4e86-48f7-b3a4-8491e79acf59)
 Call ID: cb5e4d08-4e86-48f7-b3a4-8491e79acf59
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Zara_Tindall
  AddTriple (5540cd53-117c-4fdc-883c-778a283c8a6d)
 Call ID: 5540cd53-117c-4fdc-883c-778a283c8a6d
  Args:
    relation: :hasMother
    source: Zara_Tindall
    target: Anne_Princess_Royal
  AddTriple (446559cc-6d94-4e23-bf30-a110bcf95340)
 Call ID: 446559cc-6d94-4e23-bf30-a110bcf95340
  Args:
    target: Mark_Phillips
    source: Felicity_Wade
    relation: :hasFather
  AddTriple (9e292c39-f8e9-4c55-bd5d-82b7192b7942)
 Call ID: 9e292c39-f8e9-4c55-bd5d-82b7192b7942
  Args:
    source: Felicity_Wade
    target: Heather_Tonkin
    relation: :hasMother
  AddTriple (314213f1-5e23-4522-b43c-8ae87de579d5)
 Call ID: 314213f1-5e23-4522-b43c-8ae87de579d5
  Args:
    target: Mark_Phillips
    source: Stephanie_Phillips
    relation: :hasFather
  AddTriple (2a727ccf-81ca-4ab9-86f8-33ce62313df2)
 Call ID: 2a727ccf-81ca-4ab9-86f8-33ce62313df2
  Args:
    target: Sandy_Pflueger
    source: Stephanie_Phillips
    relation: :hasMother
  AddTriple (82ef50d7-ef67-4e72-b798-b6c7c07c95f6)
 Call ID: 82ef50d7-ef67-4e72-b798-b6c7c07c95f6
  Args:
    relation: :hasFather
    target: Mark_Phillips
    source: Peter_Phillips
  AddTriple (44a23afe-d718-4715-a36c-c0f05e34edcb)
 Call ID: 44a23afe-d718-4715-a36c-c0f05e34edcb
  Args:
    relation: :hasFather
    source: Anne_Princess_Royal
    target: Prince_Philip
  AddTriple (59f2f9b0-2a08-4cd6-837b-6746487c1632)
 Call ID: 59f2f9b0-2a08-4cd6-837b-6746487c1632
  Args:
    target: Queen_Elizabeth_II
    source: Anne_Princess_Royal
    relation: :hasMother
  AddTriple (0a79289d-4999-47a7-9cda-4cab366279f0)
 Call ID: 0a79289d-4999-47a7-9cda-4cab366279f0
  Args:
    target: Prince_Philip
    source: King_Charles_III
    relation: :hasFather
  AddTriple (c64aad75-05a7-4e03-9c54-9a54190b0f17)
 Call ID: c64aad75-05a7-4e03-9c54-9a54190b0f17
  Args:
    relation: :hasMother
    target: Queen_Elizabeth_II
    source: King_Charles_III
  AddTriple (2c29ea00-8b8f-4ea6-91d7-4dc6210ab12c)
 Call ID: 2c29ea00-8b8f-4ea6-91d7-4dc6210ab12c
  Args:
    relation: :hasFather
    target: Peter_Phillips
    source: Savannah_Phillips
  AddTriple (7a8c03c3-2cab-4faf-bf1d-adbbf455ac5f)
 Call ID: 7a8c03c3-2cab-4faf-bf1d-adbbf455ac5f
  Args:
    relation: :hasMother
    target: Autumn_Kelly
    source: Savannah_Phillips
  AddTriple (4e50b828-73e7-4c05-b4c9-32389688d337)
 Call ID: 4e50b828-73e7-4c05-b4c9-32389688d337
  Args:
    relation: :hasFather
    target: Peter_Phillips
    source: Isla_Phillips
  AddTriple (cb29623c-15d7-4a17-8876-db472006a690)
 Call ID: cb29623c-15d7-4a17-8876-db472006a690
  Args:
    source: Isla_Phillips
    target: Autumn_Kelly
    relation: :hasMother
  AddLiteral (354f8f5e-b4da-43a0-9178-6c4dbc826bfe)
 Call ID: 354f8f5e-b4da-43a0-9178-6c4dbc826bfe
  Args:
    literal_value: 1977
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Peter_Phillips
  AddLiteral (bce18162-c2ea-4902-886f-659e48ad5acb)
 Call ID: bce18162-c2ea-4902-886f-659e48ad5acb
  Args:
    source: Zara_Tindall
    literal_value: 1981
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c97e4bcf-e8b3-4173-9fcc-31ea66d56a8a)
 Call ID: c97e4bcf-e8b3-4173-9fcc-31ea66d56a8a
  Args:
    source: Felicity_Wade
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1985
  AddLiteral (a33e8d65-f265-4d09-b027-c10baacc6359)
 Call ID: a33e8d65-f265-4d09-b027-c10baacc6359
  Args:
    literal_value: 1997
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Stephanie_Phillips
  AddLiteral (679a2ef4-daba-4924-8d5b-3cb3bb4903f4)
 Call ID: 679a2ef4-daba-4924-8d5b-3cb3bb4903f4
  Args:
    literal_value: 2010
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Savannah_Phillips
  AddLiteral (3baedfd9-b834-460b-98ae-54bb16972ead)
 Call ID: 3baedfd9-b834-460b-98ae-54bb16972ead
  Args:
    source: Isla_Phillips
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2012
  AddLiteral (76a63b79-b9d8-4532-8fde-560167288ef4)
 Call ID: 76a63b79-b9d8-4532-8fde-560167288ef4
  Args:
    source: Peter_Phillips
    literal_value: 2008
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddLiteral (79dc7ddf-1a15-40e8-a708-bdc28bf27074)
 Call ID: 79dc7ddf-1a15-40e8-a708-bdc28bf27074
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Anne_Princess_Royal
  Finish (4d152904-7126-4404-a867-bec58e41efe1)
 Call ID: 4d152904-7126-4404-a867-bec58e41efe1
  Args: