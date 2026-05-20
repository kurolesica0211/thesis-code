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
Princess Alexandra, The Honourable Lady Ogilvy (Alexandra Helen Elizabeth Olga Christabel; born 25 December 1936), is a member of the British royal family.
She is the only daughter of Prince George, Duke of Kent, and Princess Marina of Greece and Denmark, the only living granddaughter of George V, a niece of Edward VIII and George VI, and a first cousin of Elizabeth II.
Alexandra's mother was also a first cousin of Prince Philip, Duke of Edinburgh, consort of Elizabeth II, making her both a second cousin and first cousin once removed of Charles III.
Alexandra was married to the businessman Sir Angus Ogilvy from 1963 until his death in 2004.
Early life

Alexandra was born at 11:20 am on Christmas Day 1936 at 3 Belgrave Square, London, the second child and only daughter of Prince George, Duke of Kent, the fourth son of King George V and Queen Mary, and Princess Marina of Greece and Denmark, a daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
She was named after her paternal great-grandmother, Queen Alexandra; her grandmother, Grand Duchess Elena Vladimirovna of Russia; and both of her maternal aunts, Countess Elizabeth of Törring-Jettenbach and Princess Olga of Yugoslavia.
She received the name Christabel because she was born on Christmas Day, like her aunt Princess Alice, Duchess of Gloucester.
As a male-line granddaughter of the British monarch, she was styled as a British princess with the prefix Her Royal Highness.
At the time of her birth she was sixth in the line of succession to the British throne, behind her cousins Princess Elizabeth (later Queen Elizabeth II) and Princess Margaret, her uncle the Duke of Gloucester, her father the Duke of Kent, and her elder brother Prince Edward.
She was born two weeks after the abdication of her uncle King Edward VIII.
Alexandra was baptised in the Private Chapel at Buckingham Palace on 9 February 1937, and her godparents were King George VI and Queen Elizabeth (her paternal uncle and aunt); the Queen of Norway (her great-aunt); Princess Nicholas of Greece and Denmark (her maternal grandmother); Princess Olga of Yugoslavia (her maternal aunt); Princess Beatrice (her paternal great-great-aunt); the Earl of Athlone (her paternal great-uncle); and Count Karl Theodor of Törring-Jettenbach (her maternal uncle by marriage).
Alexandra spent most of her childhood at her family's country house, Coppins, in Buckinghamshire.
Alexandra has the distinction of being the first British princess to have attended a boarding school, Heathfield School near Ascot.
Marriage and personal life

On 24 April 1963, Alexandra married The Hon.
Angus James Bruce Ogilvy (1928–2004), the second son of David Ogilvy, 12th Earl of Airlie, and Lady Alexandra Coke, at Westminster Abbey.
Ogilvy presented Alexandra with an engagement ring made of a cabochon sapphire set in gold and surrounded by diamonds on both sides.
Alexandra travelled with her brother, the Duke of Kent, from Kensington Palace to the Abbey.
The bridesmaids included Princess Anne and Archduchess Elisabeth of Austria, and the best man was Peregrine Fairfax.
Ogilvy declined the Queen's offer to be created an earl upon marriage, so the couple's children carry no titles.
Ogilvy was knighted in 1988 (when Alexandra assumed the style of The Hon.
Lady Ogilvy), and was sworn of the Privy Council in 1997.
Alexandra and Ogilvy had two children:


Marina's first pregnancy, announced in late 1989, caused controversy as the couple were not married.
The situation led to a feud with her parents, who suggested that Marina either marry her companion in a shotgun wedding or have an abortion.
In an interview with a tabloid at the time, Marina claimed that her parents had cut off her trust fund and monthly allowance due to their disapproval of her conduct.
She also said that she wrote a letter to Queen Elizabeth II, addressing her "Dear Cousin Lilibet", asking the Queen to intervene in the family dispute.
Marina's parents denied her allegations, stating that they loved her, had not cut her off, and that she was welcome at home at any time.
Activities

Beginning in the late 1950s, Alexandra undertook an extensive programme of engagements in support of the Queen, both in the United Kingdom and overseas.
The "Alexandra Waltz" was composed for the visit by radio announcer Russ Tyson and television musical director Clyde Collins, and was sung for the princess by the teenage Gay Kahler, who later performed under the name Gay Kayler.
In 1961, Alexandra visited Hong Kong, including stops at Aberdeen Fish Market, Lok Ma Chau police station, and So Uk Estate, a public housing complex.
The Princess Alexandra Hospital in Brisbane is named in her honour.
Alexandra represented the Queen when Nigeria gained independence from the United Kingdom on 1 October 1960, and she opened the first Parliament on 3 October.
Alexandra opened the new hospital in Harlow, Essex, named in her honour, on 27 April 1965.
The Princess Alexandra Hospital NHS Trust was announced by the Prime Minister, Boris Johnson, in September 2019 as part of the government's new health infrastructure programme to build a replacement hospital.
Alexandra is an honorary fellow of the Royal College of Physicians and Surgeons of Glasgow, the Faculty of Anaesthetists of the Royal College of Surgeons of England, the Royal College of Obstetricians and Gynaecologists, and the Royal College of Physicians.
She is president of Alexandra Rose Day, founded in honour of her great-grandmother, Queen Alexandra, and was patron of The Royal School, Hampstead.
Until its abolition in 2013, she received £225,000 per year from the Civil List to cover the cost of official expenses, although, as with other members of the royal family (except the Duke of Edinburgh), the Queen repaid this amount to HM Treasury.
Alexandra lives at Thatched House Lodge in Richmond, London, a Crown property purchased on a 150-year lease from the Crown Estate Commissioners by Angus Ogilvy after their wedding in 1963.
She has been patron of the Royal Alexandra Children's Hospital in Brighton since 1954 and of Alzheimer's Society since 1990.
Alexandra is also the royal patron of Children and Families Across Borders (CFAB), a charity dedicated to reuniting children separated from their families.
In November 2016, one month before Alexandra's 80th birthday, the Queen held a reception at Buckingham Palace in honour of her charitable work.
In February 2024, she began using a wheelchair and attended a thanksgiving service for Constantine II of Greece later that month.
In April 2026, Alexandra attended a commemorative reception held to mark the centenary of Queen Elizabeth II's birth.
Titles, styles, honours and arms

Titles and styles

Alexandra is often referred to simply as Her Royal Highness Princess Alexandra.
She has held the following styles officially:


Honours

Eponyms

Appointments

Honorary military appointments

Arms

Issue

Ancestry

Since Princess Alexandra's mother was a first cousin of Prince Philip, Duke of Edinburgh, she is a second cousin to King Charles III and his siblings, in addition to being their first cousin once removed because her father was Queen Elizabeth II's uncle.



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
  AssignClass (e1fb0d1c-af73-4fd1-b966-1651b6aabb45)
 Call ID: e1fb0d1c-af73-4fd1-b966-1651b6aabb45
  Args:
    source: PrincessAlexandra
    type: :Woman
  AssignClass (0cbde812-7dc7-444c-9949-fc48415c2d80)
 Call ID: 0cbde812-7dc7-444c-9949-fc48415c2d80
  Args:
    type: :Person
    source: PrincessAlexandra
  AssignClass (9beeb381-2c46-4828-829c-4f997db82233)
 Call ID: 9beeb381-2c46-4828-829c-4f997db82233
  Args:
    type: :Man
    source: PrinceGeorgeDukeOfKent
  AssignClass (86ff89c8-e1e4-4c29-a427-24eae9a822e7)
 Call ID: 86ff89c8-e1e4-4c29-a427-24eae9a822e7
  Args:
    source: PrinceGeorgeDukeOfKent
    type: :Person
  AssignClass (00c55a92-7713-458c-9034-ff9f5e18c551)
 Call ID: 00c55a92-7713-458c-9034-ff9f5e18c551
  Args:
    type: :Woman
    source: PrincessMarinaOfGreeceAndDenmark
  AssignClass (7b05b2f5-b127-4b54-999e-6d5e21e46394)
 Call ID: 7b05b2f5-b127-4b54-999e-6d5e21e46394
  Args:
    type: :Person
    source: PrincessMarinaOfGreeceAndDenmark
  AddLiteral (18d5de7f-9c2a-42f4-9724-179a8f9ea24b)
 Call ID: 18d5de7f-9c2a-42f4-9724-179a8f9ea24b
  Args:
    source: PrincessAlexandra
    relation: :hasBirthYear
    literal_value: 1936
    literal_type: xsd:integer
  AddTriple (55fcf80c-1ad0-4dbb-b888-1d0438e3c019)
 Call ID: 55fcf80c-1ad0-4dbb-b888-1d0438e3c019
  Args:
    target: PrinceGeorgeDukeOfKent
    source: PrincessAlexandra
    relation: :hasFather
  AddTriple (bbaf58cc-3115-4ac4-ad11-92a969c4a522)
 Call ID: bbaf58cc-3115-4ac4-ad11-92a969c4a522
  Args:
    relation: :hasMother
    source: PrincessAlexandra
    target: PrincessMarinaOfGreeceAndDenmark
  AssignClass (8f8c6d0e-4441-457a-b71c-a20a6ddecc4d)
 Call ID: 8f8c6d0e-4441-457a-b71c-a20a6ddecc4d
  Args:
    source: SirAngusOgilvy
    type: :Man
  AssignClass (d54ad669-c306-42b9-8ab9-cd2df91f585b)
 Call ID: d54ad669-c306-42b9-8ab9-cd2df91f585b
  Args:
    type: :Person
    source: SirAngusOgilvy
  AddLiteral (10d22fb5-e2c9-4d4e-ae77-51f26ae065df)
 Call ID: 10d22fb5-e2c9-4d4e-ae77-51f26ae065df
  Args:
    source: PrincessAlexandra
    relation: :hasMarriageYear
    literal_value: 1963
    literal_type: xsd:integer
  AddLiteral (fdd1f3d0-135a-424b-b515-4d9f9b50f59e)
 Call ID: fdd1f3d0-135a-424b-b515-4d9f9b50f59e
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasDeathYear
    source: SirAngusOgilvy
  AddTriple (7ae73017-7098-4fc6-be38-e4aaf0e9f3d2)
 Call ID: 7ae73017-7098-4fc6-be38-e4aaf0e9f3d2
  Args:
    source: PrincessAlexandra
    relation: :hasRelation
    target: SirAngusOgilvy
  AssignClass (beaaaf4a-5edc-48b5-9ba6-774b6c552f09)
 Call ID: beaaaf4a-5edc-48b5-9ba6-774b6c552f09
  Args:
    source: GeorgeV
    type: :Man
  AssignClass (ecefae34-2410-46d4-ad19-c823ae87925d)
 Call ID: ecefae34-2410-46d4-ad19-c823ae87925d
  Args:
    source: GeorgeV
    type: :Person
  AssignClass (2ecad1a6-ab26-4221-89f9-4ce794da6f17)
 Call ID: 2ecad1a6-ab26-4221-89f9-4ce794da6f17
  Args:
    source: QueenMary
    type: :Woman
  AssignClass (b8a6a584-26e5-4188-bea8-5c2074446506)
 Call ID: b8a6a584-26e5-4188-bea8-5c2074446506
  Args:
    type: :Person
    source: QueenMary
  AddTriple (610b3bde-5275-45fc-aa18-8ac4083caee3)
 Call ID: 610b3bde-5275-45fc-aa18-8ac4083caee3
  Args:
    relation: :hasFather
    source: PrinceGeorgeDukeOfKent
    target: GeorgeV
  AddTriple (09bc38bc-070b-450c-b6c2-f16dfc32b57a)
 Call ID: 09bc38bc-070b-450c-b6c2-f16dfc32b57a
  Args:
    target: QueenMary
    source: PrinceGeorgeDukeOfKent
    relation: :hasMother
  AssignClass (d2029b14-a4de-460d-bb97-e90cb68adcce)
 Call ID: d2029b14-a4de-460d-bb97-e90cb68adcce
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    type: :Man
  AssignClass (cd07be2b-5262-4a54-9e9a-e3153d7e4a57)
 Call ID: cd07be2b-5262-4a54-9e9a-e3153d7e4a57
  Args:
    type: :Person
    source: PrinceNicholasOfGreeceAndDenmark
  AssignClass (8e77b85f-58e3-48c8-b74e-d23427f68506)
 Call ID: 8e77b85f-58e3-48c8-b74e-d23427f68506
  Args:
    type: :Woman
    source: GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (63f2f6f0-5532-440f-a6ab-b0d857659fa4)
 Call ID: 63f2f6f0-5532-440f-a6ab-b0d857659fa4
  Args:
    type: :Person
    source: GrandDuchessElenaVladimirovnaOfRussia
  AddTriple (6c9aa769-304a-4b5d-9eb3-347fb679b929)
 Call ID: 6c9aa769-304a-4b5d-9eb3-347fb679b929
  Args:
    target: PrinceNicholasOfGreeceAndDenmark
    source: PrincessMarinaOfGreeceAndDenmark
    relation: :hasFather
  AddTriple (71bd51f9-5bf3-4d04-aa56-2484fe3769e0)
 Call ID: 71bd51f9-5bf3-4d04-aa56-2484fe3769e0
  Args:
    target: GrandDuchessElenaVladimirovnaOfRussia
    source: PrincessMarinaOfGreeceAndDenmark
    relation: :hasMother
  AssignClass (4061d6f9-c896-4a22-adeb-44df33f040c1)
 Call ID: 4061d6f9-c896-4a22-adeb-44df33f040c1
  Args:
    source: PrinceEdward
    type: :Man
  AssignClass (626a4e18-e412-44d9-be9c-90f6d293760e)
 Call ID: 626a4e18-e412-44d9-be9c-90f6d293760e
  Args:
    type: :Person
    source: PrinceEdward
  AddTriple (a34c534d-a286-48de-a701-03078df452cc)
 Call ID: a34c534d-a286-48de-a701-03078df452cc
  Args:
    target: PrinceEdward
    relation: :hasBrother
    source: PrincessAlexandra
  AddTriple (99b02c7d-faeb-4d18-b809-879b24bb4723)
 Call ID: 99b02c7d-faeb-4d18-b809-879b24bb4723
  Args:
    target: PrinceGeorgeDukeOfKent
    relation: :hasFather
    source: PrinceEdward
  AddTriple (8ba8995b-2688-4949-b205-f3a47a3a3abe)
 Call ID: 8ba8995b-2688-4949-b205-f3a47a3a3abe
  Args:
    source: PrinceEdward
    relation: :hasMother
    target: PrincessMarinaOfGreeceAndDenmark
  AssignClass (900a1be5-a02e-4570-a2f1-f2ea8c70b1f5)
 Call ID: 900a1be5-a02e-4570-a2f1-f2ea8c70b1f5
  Args:
    type: :Man
    source: DavidOgilvy12thEarlOfAirlie
  AssignClass (a1bf44c3-c3b3-4754-a3d3-5f44bc96ebf1)
 Call ID: a1bf44c3-c3b3-4754-a3d3-5f44bc96ebf1
  Args:
    type: :Person
    source: DavidOgilvy12thEarlOfAirlie
  AssignClass (31e0e67e-b6cb-4e12-bcb4-c494a2c5df6e)
 Call ID: 31e0e67e-b6cb-4e12-bcb4-c494a2c5df6e
  Args:
    type: :Woman
    source: LadyAlexandraCoke
  AssignClass (30cde55a-3bc0-4601-ab2c-4c9fd659ae9d)
 Call ID: 30cde55a-3bc0-4601-ab2c-4c9fd659ae9d
  Args:
    type: :Person
    source: LadyAlexandraCoke
  AddTriple (1daf19f8-43f3-48e9-ba61-21488a10d1d4)
 Call ID: 1daf19f8-43f3-48e9-ba61-21488a10d1d4
  Args:
    target: DavidOgilvy12thEarlOfAirlie
    source: SirAngusOgilvy
    relation: :hasFather
  AddTriple (d3a790a5-8a59-4a80-aefb-354b75975c1c)
 Call ID: d3a790a5-8a59-4a80-aefb-354b75975c1c
  Args:
    relation: :hasMother
    source: SirAngusOgilvy
    target: LadyAlexandraCoke
  Finish (d059e4cc-4901-43e1-a638-80c7796ffa86)
 Call ID: d059e4cc-4901-43e1-a638-80c7796ffa86
  Args: