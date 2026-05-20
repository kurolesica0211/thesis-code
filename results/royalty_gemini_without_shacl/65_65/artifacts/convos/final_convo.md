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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Sofía (Sophia Margarita Victoria Frederica; Greek: Σοφία Μαργαρίτα Βικτωρία Φρειδερίκη, romanized: Sofía Margaríta Viktoría Freideríki; born 2 November 1938) is a member of the Spanish royal family who was Queen of Spain as the wife of King Juan Carlos I from 1975 until his abdication in 2014.
She is the eldest and last surviving child of King Paul and Queen Frederica of Greece.
She is also the last surviving grandchild of King Constantine I and Queen Sophia of Greece.
Sofía married then Infante Juan Carlos of Spain in 1962 and became queen of Spain upon her husband's accession in 1975.
On 19 June 2014, Juan Carlos abdicated in favour of their son Felipe VI.
Since her spouse's abdication, Doña Sofía has usually been referred to as reina emérita ('queen emerita') by the press.
Early life

Princess Sophia of Greece and Denmark was born on 2 November 1938, at Tatoi Palace in Acharnes, Athens, Greece, the eldest child of King Paul of Greece and Princess Frederica of Hanover.
Sofía was named after her  paternal grandmother Sophia of Prussia


Sofía is a member of the Greek branch of the Schleswig-Holstein-Sonderburg-Glücksburg dynasty.
Her brother was the deposed King Constantine II and her sister was Princess Irene.
Her maternal grandmother, Princess Victoria Louise of Prussia, wrote in her 1965 memoir: "I have always had a particular fondness for her, and esteemed her modesty, understanding and goodness coupled with her candid realism touches with a fine sense of humour.
My daughter told me what the little Sophia had once said to her about him: 'You know, Mama, I think we have the nicest Papa in the world.'
They returned to Greece in 1946.
She was a reserve member, when her brother Constantine, as helmsman, led Greece's gold medal-winning sailing team in the 1960 Summer Olympics.
Marriage and family

Sofía met her paternal third cousin and maternal third cousin-once-removed, the then Infante Juan Carlos of Spain on a cruise in the Greek Islands in 1954; they met again at the wedding of the Duke of Kent, her paternal second cousin, at York Minster in June 1961.
Sofía and Juan Carlos married on 14 May 1962, at the Catholic Cathedral of Saint Dionysius in Athens.
Sofía converted from Greek Orthodoxy to Catholicism to become more palatable to Catholic Spain.
Sofía was in Greece on a private visit to her brother, King Constantine II, when the 1967 Greek military coup took place.
Except for a brief stay for the funeral of her mother in 1981, Queen Sofía would not visit Greece until 1998.
In 1969, Spanish dictator Francisco Franco named Juan Carlos his successor under the official title "Prince of Spain".
Juan Carlos acceded to the throne in 1975, upon Franco's death.
Juan Carlos, after his accession to the Spanish throne, returned with his family to the Zarzuela Palace.
The couple has three children: Elena (born 20 December 1963); Cristina (born 13 June 1965); and Felipe (born 30 January 1968).
French-Polish princess and Sofía cousin Tatiana Radziwiłł was Sofía's main confident.
Queen consort

Besides accompanying her husband on official visits and occasions, Sofía also has solo engagements.
In her first public appearance as Queen, Sofía attended a Shabbat service at the Beth Yaacov synagogue in Madrid in June 1976, marking the first time in modern Spanish history that a member of the Spanish royal family had visited a Jewish house of worship.
She is executive president of the Queen Sofía Foundation, which in 1993, sent funds for relief in Bosnia and Herzegovina, and is honorary president of the Royal Board on Education and Care of Handicapped Persons of Spain, as well as the Spanish Foundation for Aid for Drug Addicts.
Additionally, she has served as the patroness of the Queen Sofía Spanish Institute since 2003.
Sofía takes special interest in programs against drug addiction, travelling to conferences in both Spain and abroad.
The Museo Nacional Centro de Arte Reina Sofía is named after her, as is Reina Sofía Airport in Tenerife.
Sofía is an Honorary Member of the San Fernando Royal Academy of Fine Arts and of the Spanish Royal Academy of History.
Sofía has been honorary president of the Spanish Unicef Committee since 1971.
Queen Sofía has travelled to Bangladesh, Chile, Colombia, El Salvador and Mexico to support the activities of the organization.
Queen Sofía has also been a strong supporter of Somaly Mam's Agir pour les Femmes en Situation Précaire, an NGO combatting child prostitution and slavery in Cambodia.
In 1998, Mam was awarded the prestigious Prince of Asturias Award for International Cooperation in the Queen's presence.
As Queen, Sofía never publicly commented on political issues.
However, in October 2008, Pilar Urbano's book La Reina muy de cerca ("The Queen up close") sparked strong controversy as it contained alleged statements by the Queen on issues debated in Spanish society.
In May 2012, Sofía was reportedly refused permission to  attend the celebrations for the Diamond Jubilee of Elizabeth II by the Spanish government, citing tensions over fishing rights at Gibraltar.
In July 2012, Sofía visited the Philippines for a fourth time.
Queen emerita

Following her husband's abdication as King in 2014, Sofía has focused on her sponsoring activities, spending her time between La Zarzuela and, in the summer months, the Marivent Palace in Palma de Mallorca.
In September 2025, Sofía opened the "Spain and the Birth of American Democracy: A History Symposium", cohosted by the Queen Sofía Spanish Institute and the Daughters of the American Revolution at DAR Constitution Hall in Washington, D.C.
The symposium, held in celebration of the upcoming United States Semiquincentennial, recognized Spain's role in the American Revolutionary War and the cause for American Independence from the British Empire.
Sofía was received at DAR Constitution Hall by DAR President General Ginnie Sebastian Storage.
She also visited the Spanish Embassy in the United States, where she was received by Ambassador Ángeles Moreno Bau and met with María Isabel Valldecabres, president and general director of the National Mint and Stamp Factory, and Pilar Lladó Arburúa, the chair of the board of directors of the Queen Sofía Spanish Institute.
While there, Sofía chaired the meeting of the executive committee of the Queen Sofía Spanish Institute's board of trustees.
Honours

Queen Sophia was awarded the Order of the Queen of Sheba by Emperor Haile Selassie of Ethiopia in 1973 upon her and her husband King Juan Carlos's visit to the capital Addis Ababa.
Sofía was appointed as a Knight Grand Cross of the Order of Carlos III on 10 May 1962 and a Dame Grand Cross of the Order of Queen Maria Luisa on 14 May 1962.
The Queen of Spain was elevated to Grand Cross with Collar of the Order of Charles III on 31 October 1983.
Since then, Queen Sofía has received different honours and decorations by more than 40 foreign states.
In 2024, Queen Sofía was created as a Knight of the Order of the Golden Fleece.
Arms

In popular culture

Queen Sofía is portrayed on screen by Mónica López in the Televisión Española mini-series 23-F: El día más difícil del Rey (2009); by Marisa Paredes in the Telecinco mini-series Felipe y Letizia  (2010); by Nadia de Santiago in the Antena 3 mini-series Sofía  (2011); by Olga Lozano in the film 17 Hours (2011); by Cristina Brondo  in the Telecinco mini-series El Rey  (2014); by Salomé Jiménez  in the Atresmedia mini-series Untameable (2023); and by Elena Petrova in the Movistar Plus+ mini-series The Anatomy of a Moment (2025).



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
  AssignClass (a30d9592-e2fb-4b2f-ab16-75c6e39bfc65)
 Call ID: a30d9592-e2fb-4b2f-ab16-75c6e39bfc65
  Args:
    source: Sofía
    type: :Woman
  AssignClass (baf2da99-0dec-4333-a554-2a7d532f3987)
 Call ID: baf2da99-0dec-4333-a554-2a7d532f3987
  Args:
    source: Sofía
    type: :Person
  AssignClass (489200a5-2d4b-45b2-b13c-296252468f5a)
 Call ID: 489200a5-2d4b-45b2-b13c-296252468f5a
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (60be518e-4b7d-4309-9ebe-aa6134e52703)
 Call ID: 60be518e-4b7d-4309-9ebe-aa6134e52703
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (31c53fe3-6b62-4616-8b5a-196bcfb4b510)
 Call ID: 31c53fe3-6b62-4616-8b5a-196bcfb4b510
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (154e2f25-5046-40ce-b372-0be0d34379bc)
 Call ID: 154e2f25-5046-40ce-b372-0be0d34379bc
  Args:
    source: Paul_of_Greece
    type: :Person
  AssignClass (889693c4-47c9-45c3-80e5-16a82ce91da5)
 Call ID: 889693c4-47c9-45c3-80e5-16a82ce91da5
  Args:
    type: :Woman
    source: Frederica_of_Hanover
  AssignClass (3502a52a-a0f8-410d-93e1-586863527fdc)
 Call ID: 3502a52a-a0f8-410d-93e1-586863527fdc
  Args:
    source: Frederica_of_Hanover
    type: :Person
  AssignClass (5f9341a1-b0e0-49dd-b581-616af6b473ef)
 Call ID: 5f9341a1-b0e0-49dd-b581-616af6b473ef
  Args:
    source: Constantine_II
    type: :Man
  AssignClass (69645504-2ff5-41ad-8fc5-e95d0f58eb63)
 Call ID: 69645504-2ff5-41ad-8fc5-e95d0f58eb63
  Args:
    type: :Person
    source: Constantine_II
  AssignClass (89153192-ba62-494d-baaf-6b1e6990bcb1)
 Call ID: 89153192-ba62-494d-baaf-6b1e6990bcb1
  Args:
    type: :Woman
    source: Irene
  AssignClass (614a8457-4154-4d78-b7b5-7aa93ee34fab)
 Call ID: 614a8457-4154-4d78-b7b5-7aa93ee34fab
  Args:
    source: Irene
    type: :Person
  AssignClass (dffcb1f3-b205-47c2-a513-664a7dbf8eb8)
 Call ID: dffcb1f3-b205-47c2-a513-664a7dbf8eb8
  Args:
    type: :Woman
    source: Elena
  AssignClass (474911da-b0d2-47ce-87c1-b4023719f342)
 Call ID: 474911da-b0d2-47ce-87c1-b4023719f342
  Args:
    type: :Person
    source: Elena
  AssignClass (e9321e93-18a0-4606-a817-41c2b8a18eaf)
 Call ID: e9321e93-18a0-4606-a817-41c2b8a18eaf
  Args:
    source: Cristina
    type: :Woman
  AssignClass (f2ddabe3-5ba0-4ba0-bd99-74e16a171fa9)
 Call ID: f2ddabe3-5ba0-4ba0-bd99-74e16a171fa9
  Args:
    type: :Person
    source: Cristina
  AssignClass (b92e9df5-4d6c-4a11-8b02-9eda1002e667)
 Call ID: b92e9df5-4d6c-4a11-8b02-9eda1002e667
  Args:
    source: Felipe_VI
    type: :Man
  AssignClass (64559b6d-598c-45ea-95d9-efb0c4b5692b)
 Call ID: 64559b6d-598c-45ea-95d9-efb0c4b5692b
  Args:
    source: Felipe_VI
    type: :Person
  AddTriple (855103e0-119d-408e-9d22-fd3d6619d74c)
 Call ID: 855103e0-119d-408e-9d22-fd3d6619d74c
  Args:
    source: Sofía
    relation: :hasFather
    target: Paul_of_Greece
  AddTriple (cffa479a-7508-4707-b715-8c5c11a3fbcc)
 Call ID: cffa479a-7508-4707-b715-8c5c11a3fbcc
  Args:
    target: Frederica_of_Hanover
    relation: :hasMother
    source: Sofía
  AddTriple (363f9f41-b9e6-4172-bf54-dd0489d2443a)
 Call ID: 363f9f41-b9e6-4172-bf54-dd0489d2443a
  Args:
    target: Constantine_II
    source: Sofía
    relation: :hasBrother
  AddTriple (6c643196-9400-4981-b6e0-c22a0257fd42)
 Call ID: 6c643196-9400-4981-b6e0-c22a0257fd42
  Args:
    source: Sofía
    relation: :hasSister
    target: Irene
  AddTriple (2bf86040-8162-4504-b969-6d149a401f91)
 Call ID: 2bf86040-8162-4504-b969-6d149a401f91
  Args:
    relation: :hasFather
    source: Elena
    target: Juan_Carlos_I
  AddTriple (1dcc9a64-1361-47b2-8624-5037d3fd2b7f)
 Call ID: 1dcc9a64-1361-47b2-8624-5037d3fd2b7f
  Args:
    target: Sofía
    source: Elena
    relation: :hasMother
  AddTriple (42d80c3d-30e2-4e07-85dd-8de08e8fc716)
 Call ID: 42d80c3d-30e2-4e07-85dd-8de08e8fc716
  Args:
    target: Juan_Carlos_I
    relation: :hasFather
    source: Cristina
  AddTriple (91cc8f26-f3eb-42d7-992e-5556b6913a2a)
 Call ID: 91cc8f26-f3eb-42d7-992e-5556b6913a2a
  Args:
    target: Sofía
    relation: :hasMother
    source: Cristina
  AddTriple (456b3f75-e0e4-4bea-b376-df5965085d5d)
 Call ID: 456b3f75-e0e4-4bea-b376-df5965085d5d
  Args:
    target: Juan_Carlos_I
    source: Felipe_VI
    relation: :hasFather
  AddTriple (602ee8b0-fcc1-4639-8e07-ce1c4996ee84)
 Call ID: 602ee8b0-fcc1-4639-8e07-ce1c4996ee84
  Args:
    relation: :hasMother
    source: Felipe_VI
    target: Sofía
  AddLiteral (7a8b2016-6e6c-412e-af55-0bdb1c60ff83)
 Call ID: 7a8b2016-6e6c-412e-af55-0bdb1c60ff83
  Args:
    literal_value: 1938
    relation: :hasBirthYear
    source: Sofía
    literal_type: xsd:integer
  AddLiteral (9c3c972a-15df-4b90-a8a8-c91fb39020ac)
 Call ID: 9c3c972a-15df-4b90-a8a8-c91fb39020ac
  Args:
    relation: :hasMarriageYear
    literal_value: 1962
    source: Sofía
    literal_type: xsd:integer
  Finish (4c7951e4-efc9-4986-9c33-d70803df3de4)
 Call ID: 4c7951e4-efc9-4986-9c33-d70803df3de4
  Args: