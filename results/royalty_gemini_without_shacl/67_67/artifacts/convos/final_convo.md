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
Prince Edward, Duke of Kent (Edward George Nicholas Paul Patrick; born 9 October 1935), is a member of the British royal family.
The elder son of Prince George, Duke of Kent, and Princess Marina of Greece and Denmark, he is a grandson of George V, nephew of Edward VIII and George VI, and first cousin of Elizabeth II.
Edward's mother was also a first cousin of Prince Philip, Elizabeth's husband, making him both a second cousin and first cousin once removed to Charles III.
In 2025, following the death of his wife, Katharine, Duchess of Kent, Edward became the oldest living member of the British royal family.
Edward has held the title of Duke of Kent for over 83 years.
Edward carried out engagements on behalf of Elizabeth II and is involved with over 140 charitable organisations.
Edward has been Chancellor of the University of Surrey since June 1976.
Early life and education

Edward was born at 2:05 am on 9 October 1935 at No. 3
Belgrave Square, London, the eldest child of  Prince George, Duke of Kent, and Princess Marina, Duchess of Kent.
His father was the fourth son of King George V and Queen Mary, and his mother was the daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
His godparents were his grandparents, King George V, Queen Mary, and Prince Nicholas of Greece and Denmark; the Prince of Wales; the Princess Royal; the Duke of Connaught and Strathearn (whose son, Prince Arthur of Connaught, stood proxy); and the Duchess of Argyll.
Edward began his education at Ludgrove, a preparatory school in Berkshire, before going on to Eton College and subsequently Le Rosey in Switzerland.
Edward speaks fluent French, having been raised in a house where, according to his younger brother, Prince Michael of Kent, their mother and aunts spoke French as a matter of preference.
On 25 August 1942, Edward's father, the Duke of Kent, was killed when his aircraft crashed in bad weather in Caithness.
Edward, then six years old, succeeded to his father's titles as Duke of Kent, Earl of St Andrews, and Baron Downpatrick.
In 1952, at the age of 16, he walked behind the coffin of his uncle, George VI, at the King's state funeral.
The following year, he attended the coronation of his cousin, Elizabeth II, and was the third to pay homage at her throne, following the dukes of Edinburgh and Gloucester.
Military service

On 29 July 1955, Edward graduated from the Royal Military Academy Sandhurst as a second lieutenant in the Royal Scots Greys, marking the beginning of a military career that lasted more than 20 years.
From 1962 to 1963, Edward served in Hong Kong, later joining the staff in Eastern Command.
During the early 1970s, Edward also served briefly in Northern Ireland with his regiment.
Edward, then aged 35, had been deployed to Northern Ireland with his unit, but the Queen raised concerns during her weekly audience with the prime minister, Edward Heath.
Edward retired from the army on 15 April 1976.
Marriage and personal life

Edward met Katharine Worsley while he was based at Catterick Garrison.
Marina reportedly disapproved of her son's choice of bride and twice forbade the match before agreeing to the marriage in 1961.
Katharine converted to Catholicism in 1994, but because the conversion occurred during, and not before, their marriage, it did not cause Edward to lose his place in the line of succession, as the Act of Settlement 1701 applied only where the spouse was a Catholic at the time of marriage.
The couple have three living children:


Katharine had a miscarriage in 1975 owing to rubella, and gave birth to a stillborn son, Patrick, in 1977.
Edward resides at Wren House, Kensington Palace, in London.
In 2011, close associates of Jonathan Rees, a private investigator connected to the News International phone hacking scandal, alleged that he had accessed the bank accounts of Edward and his wife.
Edward had a mild stroke on the morning of 18 March 2013.
His wife, Katharine, died on 4 September 2025 at the age of 92.
Following her death, Edward became the oldest living member of the British royal family.
Activities

Edward performed engagements on behalf of his cousin, Queen Elizabeth II, for more than 50 years.
One of Edward's major public roles for many years was vice-chairman of British Trade International, formerly known as the British Overseas Trade Board, and later as the United Kingdom's Special Representative for International Trade and Investment.
The then Prince Andrew succeeded him in this position, later known as UK Trade & Investment (or UKTI), although Andrew resigned from the post in 2011.
In 1979, Edward became the first member of the royal family to visit China, focusing on the British Energy Exhibition in Beijing.
From 1971 to 2000, Edward served as president of The Football Association, the governing body of English football.
He has been president of The Scout Association since 1975, and, together with Prince William of Wales, visited the Centenary World Scout Jamboree at Hylands Park, Chelmsford, in July 2007.
His other roles include president of the RAF Benevolent Fund, the Royal National Lifeboat Institution, the Stroke Association, the Royal United Services Institute, the Royal Institution, the British Racing Drivers' Club, and patron of the American Air Museum in Britain, Royal West Norfolk Golf Club, Kent County Cricket Club, Opera North, and Trinity Laban Conservatoire of Music and Dance.
Edward is also one of the Royal Fellows of the Royal Academy of Engineering.
For almost 29 years, Edward has been the patron of Endeavour, a national youth organisation.
"


On 2 June 2022, Edward appeared alongside the Queen on the balcony of Buckingham Palace during the Trooping the Colour, which formed part of the Platinum Jubilee celebrations.
Edward was colonel of the Scots Guards for 50 years from 9 September 1974 to 14 April 2024, being succeeded by the Duke of Edinburgh.
In April 2026, Edward attended a commemorative reception held to mark the centenary of Queen Elizabeth II's birth.
Freemasonry

Edward was initiated into Royal Alpha Lodge No. 16 on 16 December 1963, and was elected its Worshipful Master for 1965 and 1966.
Having been appointed Senior Grand Warden in 1966, he was elected Grand Master the following year and was installed on 14 June 1967 during the United Grand Lodge of England's 250th-anniversary celebrations at the Royal Albert Hall.
He is the 10th, and longest-serving, Grand Master of UGLE, the governing body of Freemasonry in England and Wales.
In December 2013, Edward celebrated 50 years as a freemason.
In October 2017, he presided over the tercentenary celebrations of UGLE, marking the 300th anniversary of the founding of the original Grand Lodge, one of the two bodies that merged to form UGLE in 1813.
The main ceremony was held at the Royal Albert Hall, in the year that also marked Edward's 50th anniversary of installation as Grand Master.
Titles, styles, honours and arms

Titles and styles

Military ranks

Honours

Foreign

Civilian appointments

Wear of orders, decorations, and medals

The ribbons worn regularly by Edward in undress uniform are as follows:


With medals, Edward normally wears the breast stars of the Garter, St Michael and St George, and Royal Victorian Order.



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
  AssignClass (6d70fb54-f897-4a5d-9bc4-6b692a14ec73)
 Call ID: 6d70fb54-f897-4a5d-9bc4-6b692a14ec73
  Args:
    type: :Man
    source: Prince Edward, Duke of Kent
  AssignClass (31353f52-ea40-4048-82f4-d3a5ef85e6d0)
 Call ID: 31353f52-ea40-4048-82f4-d3a5ef85e6d0
  Args:
    type: :Man
    source: Prince George, Duke of Kent
  AssignClass (7949087e-121c-4a5f-adf7-5f2e98a5e447)
 Call ID: 7949087e-121c-4a5f-adf7-5f2e98a5e447
  Args:
    source: Princess Marina of Greece and Denmark
    type: :Woman
  AssignClass (6224d34f-04fb-4b29-98bb-fa8261c7e521)
 Call ID: 6224d34f-04fb-4b29-98bb-fa8261c7e521
  Args:
    type: :Man
    source: George V
  AssignClass (cb45af1e-5631-4b82-87eb-3bbbac158174)
 Call ID: cb45af1e-5631-4b82-87eb-3bbbac158174
  Args:
    source: Queen Mary
    type: :Woman
  AssignClass (5f8304fc-601d-4119-b52b-ee1c734275e8)
 Call ID: 5f8304fc-601d-4119-b52b-ee1c734275e8
  Args:
    source: Prince Nicholas of Greece and Denmark
    type: :Man
  AssignClass (6b22ea1d-2c24-41e1-b258-dba36d3f06f4)
 Call ID: 6b22ea1d-2c24-41e1-b258-dba36d3f06f4
  Args:
    type: :Woman
    source: Grand Duchess Elena Vladimirovna of Russia
  AssignClass (29a78cd4-5377-493e-8e16-5e75352e7358)
 Call ID: 29a78cd4-5377-493e-8e16-5e75352e7358
  Args:
    source: Prince Michael of Kent
    type: :Man
  AssignClass (766a2b36-2242-4fcb-b64b-3a95dd43ba91)
 Call ID: 766a2b36-2242-4fcb-b64b-3a95dd43ba91
  Args:
    type: :Woman
    source: Katharine, Duchess of Kent
  AssignClass (6c8572a3-8824-47ed-9497-231bccb6175b)
 Call ID: 6c8572a3-8824-47ed-9497-231bccb6175b
  Args:
    source: Patrick
    type: :Man
  AddTriple (1e2ed2c4-915d-45dd-89a4-30145ab66f3e)
 Call ID: 1e2ed2c4-915d-45dd-89a4-30145ab66f3e
  Args:
    target: Prince George, Duke of Kent
    relation: :hasFather
    source: Prince Edward, Duke of Kent
  AddTriple (e99ca6eb-b9d8-4ddc-8a42-ca3643f39ee6)
 Call ID: e99ca6eb-b9d8-4ddc-8a42-ca3643f39ee6
  Args:
    source: Prince Edward, Duke of Kent
    target: Princess Marina of Greece and Denmark
    relation: :hasMother
  AddLiteral (8cdb9d4e-792c-4a65-9884-1e917895d908)
 Call ID: 8cdb9d4e-792c-4a65-9884-1e917895d908
  Args:
    relation: :hasBirthYear
    literal_value: 1935
    literal_type: xsd:integer
    source: Prince Edward, Duke of Kent
  AddTriple (20dfbb7c-b561-4051-b526-8631c44b571f)
 Call ID: 20dfbb7c-b561-4051-b526-8631c44b571f
  Args:
    relation: :hasFather
    target: George V
    source: Prince George, Duke of Kent
  AddTriple (9d71f89e-b670-4d85-8e70-c2aca05f1292)
 Call ID: 9d71f89e-b670-4d85-8e70-c2aca05f1292
  Args:
    source: Prince George, Duke of Kent
    relation: :hasMother
    target: Queen Mary
  AddTriple (7f98c1bb-ff17-45ed-8ade-7e16b54a7f81)
 Call ID: 7f98c1bb-ff17-45ed-8ade-7e16b54a7f81
  Args:
    relation: :hasFather
    target: Prince Nicholas of Greece and Denmark
    source: Princess Marina of Greece and Denmark
  AddTriple (79505470-1b3d-4dfc-9db2-732bb191bcb6)
 Call ID: 79505470-1b3d-4dfc-9db2-732bb191bcb6
  Args:
    target: Grand Duchess Elena Vladimirovna of Russia
    relation: :hasMother
    source: Princess Marina of Greece and Denmark
  AddTriple (3363b68a-531e-41cf-af0c-7cc838f16027)
 Call ID: 3363b68a-531e-41cf-af0c-7cc838f16027
  Args:
    relation: :hasBrother
    target: Prince Michael of Kent
    source: Prince Edward, Duke of Kent
  AddTriple (e31c8f7e-6848-43a2-854c-a144cbe2efad)
 Call ID: e31c8f7e-6848-43a2-854c-a144cbe2efad
  Args:
    source: Prince Michael of Kent
    target: Princess Marina of Greece and Denmark
    relation: :hasMother
  AddTriple (084644ad-0c1c-4b58-8c7d-96ee774e4eec)
 Call ID: 084644ad-0c1c-4b58-8c7d-96ee774e4eec
  Args:
    relation: :hasFather
    target: Prince George, Duke of Kent
    source: Prince Michael of Kent
  AddTriple (80d4e37a-84c1-4f9c-9d73-4a5523f61c51)
 Call ID: 80d4e37a-84c1-4f9c-9d73-4a5523f61c51
  Args:
    relation: :hasMother
    target: Katharine, Duchess of Kent
    source: Patrick
  AddTriple (8403a949-3848-4dc1-bf42-6bcb49db52d8)
 Call ID: 8403a949-3848-4dc1-bf42-6bcb49db52d8
  Args:
    target: Prince Edward, Duke of Kent
    relation: :hasFather
    source: Patrick
  AddLiteral (d978ceaa-a7af-4d91-8d91-1d6dd8ec7c19)
 Call ID: d978ceaa-a7af-4d91-8d91-1d6dd8ec7c19
  Args:
    literal_value: 2025
    literal_type: xsd:integer
    source: Katharine, Duchess of Kent
    relation: :hasDeathYear
  AddLiteral (d833d827-b29e-4db2-97fe-07a5a1762111)
 Call ID: d833d827-b29e-4db2-97fe-07a5a1762111
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1961
    source: Prince Edward, Duke of Kent
  AddTriple (3218b01b-61de-4730-9c1c-3d6c1e0dad3c)
 Call ID: 3218b01b-61de-4730-9c1c-3d6c1e0dad3c
  Args:
    relation: :hasRelation
    target: Katharine, Duchess of Kent
    source: Prince Edward, Duke of Kent
  Finish (22dc135a-3c36-4d79-a5a5-2f067e2ce796)
 Call ID: 22dc135a-3c36-4d79-a5a5-2f067e2ce796
  Args: