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
The Royal Household commented that the book "puts in Her Majesty's mouth alleged claims that  do not correspond exactly to the opinions expressed by Her Majesty".
In May 2012, Sofía was reportedly refused permission to  attend the celebrations for the Diamond Jubilee of Elizabeth II by the Spanish government, citing tensions over fishing rights at Gibraltar.
In July 2012, Sofía visited the Philippines for a fourth time.
She visited the National Library, National Museum and the Pontifical and Royal University of Santo Tomas, The Catholic University of the Philippines, which had the oldest extant university charter in Asia and housed the world's largest collection of suyat scripts.
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
  AssignClass (320a12cf-bdfa-4b5b-ad6c-9eeebff4d958)
 Call ID: 320a12cf-bdfa-4b5b-ad6c-9eeebff4d958
  Args:
    type: :Woman
    source: Sofía
  AssignClass (34273203-23ae-4871-91c6-be70e871fcee)
 Call ID: 34273203-23ae-4871-91c6-be70e871fcee
  Args:
    type: :Person
    source: Sofía
  AddLiteral (2aa9d375-588c-4383-8aad-f43a4be10ad6)
 Call ID: 2aa9d375-588c-4383-8aad-f43a4be10ad6
  Args:
    source: Sofía
    literal_value: 1938
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
  AssignClass (40cc7e1d-3572-4c9a-b1b7-11e6a3f3d152)
 Call ID: 40cc7e1d-3572-4c9a-b1b7-11e6a3f3d152
  Args:
    type: :Man
    source: Juan Carlos I
  AssignClass (42c1f501-9564-431b-8f84-3ae056218df8)
 Call ID: 42c1f501-9564-431b-8f84-3ae056218df8
  Args:
    type: :Person
    source: Juan Carlos I
  AddTriple (72e27994-79fa-41eb-bfa4-80613f6a7443)
 Call ID: 72e27994-79fa-41eb-bfa4-80613f6a7443
  Args:
    target: Juan Carlos I
    source: Sofía
    relation: :hasRelation
  AssignClass (297f24c9-7b38-4ed4-82cf-1781d07274da)
 Call ID: 297f24c9-7b38-4ed4-82cf-1781d07274da
  Args:
    type: :Man
    source: Paul of Greece
  AssignClass (0d866797-ee95-4326-b5fd-8e0feb95889e)
 Call ID: 0d866797-ee95-4326-b5fd-8e0feb95889e
  Args:
    type: :Person
    source: Paul of Greece
  AssignClass (cb440a8b-8afc-4e4b-afcf-57ba76e06e01)
 Call ID: cb440a8b-8afc-4e4b-afcf-57ba76e06e01
  Args:
    type: :Woman
    source: Frederica of Greece
  AssignClass (85d96bc1-8ded-4e26-aa5d-393b5539246e)
 Call ID: 85d96bc1-8ded-4e26-aa5d-393b5539246e
  Args:
    type: :Person
    source: Frederica of Greece
  AddTriple (b25c8687-3d5d-4121-ad35-4d59fb5a4e73)
 Call ID: b25c8687-3d5d-4121-ad35-4d59fb5a4e73
  Args:
    source: Sofía
    target: Paul of Greece
    relation: :isChildOf
  AddTriple (e35cdbac-3227-4fbc-a070-b7dcee8020ec)
 Call ID: e35cdbac-3227-4fbc-a070-b7dcee8020ec
  Args:
    target: Frederica of Greece
    source: Sofía
    relation: :isChildOf
  AssignClass (f1e908ca-8291-44fd-a02e-c34e1bfc3621)
 Call ID: f1e908ca-8291-44fd-a02e-c34e1bfc3621
  Args:
    type: :Man
    source: Constantine II
  AssignClass (03185296-cda8-49b4-a628-4b9949e7ef52)
 Call ID: 03185296-cda8-49b4-a628-4b9949e7ef52
  Args:
    type: :Person
    source: Constantine II
  AssignClass (a4ab4d8b-1c91-434e-b228-1fae1c0b2368)
 Call ID: a4ab4d8b-1c91-434e-b228-1fae1c0b2368
  Args:
    type: :Woman
    source: Irene
  AssignClass (ce4c6ab8-5eff-4b69-a11d-4a0fc2b9f979)
 Call ID: ce4c6ab8-5eff-4b69-a11d-4a0fc2b9f979
  Args:
    type: :Person
    source: Irene
  AddTriple (fa4323c3-9bc0-4e88-8198-5b321b86c589)
 Call ID: fa4323c3-9bc0-4e88-8198-5b321b86c589
  Args:
    source: Sofía
    target: Constantine II
    relation: :isSiblingOf
  AddTriple (1025f8e3-065e-4ddd-a69a-4a9b0b33b02d)
 Call ID: 1025f8e3-065e-4ddd-a69a-4a9b0b33b02d
  Args:
    source: Sofía
    target: Irene
    relation: :isSiblingOf
  AssignClass (b492867e-e165-4c2c-8bda-f5fa7dfd7ec5)
 Call ID: b492867e-e165-4c2c-8bda-f5fa7dfd7ec5
  Args:
    type: :Woman
    source: Elena
  AssignClass (de9cdc3a-fe5d-467c-99b7-833c72a80aa8)
 Call ID: de9cdc3a-fe5d-467c-99b7-833c72a80aa8
  Args:
    type: :Person
    source: Elena
  AssignClass (a13413d0-b885-40ac-aaf5-4c2e9e815f99)
 Call ID: a13413d0-b885-40ac-aaf5-4c2e9e815f99
  Args:
    type: :Woman
    source: Cristina
  AssignClass (25d5f0aa-0da9-4a68-b035-e4e55ff4dcbb)
 Call ID: 25d5f0aa-0da9-4a68-b035-e4e55ff4dcbb
  Args:
    type: :Person
    source: Cristina
  AssignClass (51441c68-0c44-402a-8aaa-5dfd2cf06f4c)
 Call ID: 51441c68-0c44-402a-8aaa-5dfd2cf06f4c
  Args:
    type: :Man
    source: Felipe VI
  AssignClass (2e6683d5-6ae7-450b-a9b2-3f7cf03e2670)
 Call ID: 2e6683d5-6ae7-450b-a9b2-3f7cf03e2670
  Args:
    type: :Person
    source: Felipe VI
  AddTriple (d5f7f80b-b084-47d0-a378-4ff9e0da1e28)
 Call ID: d5f7f80b-b084-47d0-a378-4ff9e0da1e28
  Args:
    relation: :isChildOf
    target: Sofía
    source: Elena
  AddTriple (c4ece7b7-bc16-4d5d-9aea-9056390e81f1)
 Call ID: c4ece7b7-bc16-4d5d-9aea-9056390e81f1
  Args:
    relation: :isChildOf
    source: Elena
    target: Juan Carlos I
  AddTriple (60c98a38-5e2d-45ac-b153-9d1a10b5e9ee)
 Call ID: 60c98a38-5e2d-45ac-b153-9d1a10b5e9ee
  Args:
    source: Cristina
    target: Sofía
    relation: :isChildOf
  AddTriple (0572e54d-49b5-408a-9cbe-cf9384f9f642)
 Call ID: 0572e54d-49b5-408a-9cbe-cf9384f9f642
  Args:
    target: Juan Carlos I
    source: Cristina
    relation: :isChildOf
  AddTriple (c9210cb5-cd0a-4715-8ba6-3db71d54924d)
 Call ID: c9210cb5-cd0a-4715-8ba6-3db71d54924d
  Args:
    relation: :isChildOf
    target: Sofía
    source: Felipe VI
  AddTriple (66ab44ac-c4bc-4e9f-8411-ad142b521543)
 Call ID: 66ab44ac-c4bc-4e9f-8411-ad142b521543
  Args:
    relation: :isChildOf
    source: Felipe VI
    target: Juan Carlos I
  AssignClass (3a5c8462-8e64-411a-8340-05f623e734ed)
 Call ID: 3a5c8462-8e64-411a-8340-05f623e734ed
  Args:
    type: :Man
    source: Constantine I
  AssignClass (5efdb1a4-f9d9-465b-a694-dee9a8e9fa55)
 Call ID: 5efdb1a4-f9d9-465b-a694-dee9a8e9fa55
  Args:
    type: :Person
    source: Constantine I
  AssignClass (0999d65c-6855-40c7-acf9-1839e6ad4c00)
 Call ID: 0999d65c-6855-40c7-acf9-1839e6ad4c00
  Args:
    type: :Woman
    source: Sophia of Greece
  AssignClass (b47193e1-62c3-4b6a-92f2-2a10c5df5ade)
 Call ID: b47193e1-62c3-4b6a-92f2-2a10c5df5ade
  Args:
    type: :Person
    source: Sophia of Greece
  AddTriple (8cf2b635-75c5-48f6-96ee-5877254403e9)
 Call ID: 8cf2b635-75c5-48f6-96ee-5877254403e9
  Args:
    relation: :isChildOf
    source: Paul of Greece
    target: Constantine I
  AddTriple (3f2c1d7a-1b47-4797-8fc9-b93146704c20)
 Call ID: 3f2c1d7a-1b47-4797-8fc9-b93146704c20
  Args:
    relation: :isChildOf
    target: Sophia of Greece
    source: Paul of Greece
  Finish (c8184870-63f2-4959-aa84-1817da11580b)
 Call ID: c8184870-63f2-4959-aa84-1817da11580b
  Args: