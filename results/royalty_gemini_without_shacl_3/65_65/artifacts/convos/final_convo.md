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
  AssignClass (18ae51ad-f4df-4962-a99d-f74cde830eb0)
 Call ID: 18ae51ad-f4df-4962-a99d-f74cde830eb0
  Args:
    source: Sofía
    type: :Woman
  AssignClass (52b4e52a-f300-495b-850e-1f9fa702e712)
 Call ID: 52b4e52a-f300-495b-850e-1f9fa702e712
  Args:
    type: :Man
    source: Juan Carlos I
  AssignClass (9149c157-372a-4751-b75a-ab73d106088e)
 Call ID: 9149c157-372a-4751-b75a-ab73d106088e
  Args:
    type: :Man
    source: Paul of Greece
  AssignClass (97ae38aa-bbed-438c-874d-7c4fa1c74c99)
 Call ID: 97ae38aa-bbed-438c-874d-7c4fa1c74c99
  Args:
    type: :Woman
    source: Frederica of Hanover
  AssignClass (ea40b352-2aca-4382-8427-ea11d2ace0d0)
 Call ID: ea40b352-2aca-4382-8427-ea11d2ace0d0
  Args:
    type: :Man
    source: Constantine I
  AssignClass (8afcd596-1586-452e-ad56-4043599d26a0)
 Call ID: 8afcd596-1586-452e-ad56-4043599d26a0
  Args:
    type: :Woman
    source: Sophia of Greece
  AssignClass (a143c6b9-1117-4748-acd6-cc05335c2198)
 Call ID: a143c6b9-1117-4748-acd6-cc05335c2198
  Args:
    type: :Man
    source: Constantine II
  AssignClass (3e6a23e9-d063-47a4-86ae-a62c4ad26056)
 Call ID: 3e6a23e9-d063-47a4-86ae-a62c4ad26056
  Args:
    type: :Woman
    source: Irene
  AssignClass (e55185e8-ef35-4315-beae-f7e17fb88e0c)
 Call ID: e55185e8-ef35-4315-beae-f7e17fb88e0c
  Args:
    source: Elena
    type: :Woman
  AssignClass (fca65992-f2a4-4e70-938d-da3d96fbcaa5)
 Call ID: fca65992-f2a4-4e70-938d-da3d96fbcaa5
  Args:
    source: Cristina
    type: :Woman
  AssignClass (244949be-157b-4b03-82b9-9727b66c1437)
 Call ID: 244949be-157b-4b03-82b9-9727b66c1437
  Args:
    source: Felipe VI
    type: :Man
  AddLiteral (9771a080-acce-419e-9b94-4ed0409a444e)
 Call ID: 9771a080-acce-419e-9b94-4ed0409a444e
  Args:
    source: Sofía
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (92c1aaba-6abf-4f3e-8f5a-d02eda2337b9)
 Call ID: 92c1aaba-6abf-4f3e-8f5a-d02eda2337b9
  Args:
    relation: :hasMarriageYear
    literal_value: 1962
    literal_type: xsd:integer
    source: Sofía
  AddTriple (641aa8af-5ef3-4c48-ae36-a9781781f458)
 Call ID: 641aa8af-5ef3-4c48-ae36-a9781781f458
  Args:
    relation: :hasFather
    target: Paul of Greece
    source: Sofía
  AddTriple (8c21318e-5864-46b0-b331-4503c46cfe16)
 Call ID: 8c21318e-5864-46b0-b331-4503c46cfe16
  Args:
    target: Frederica of Hanover
    source: Sofía
    relation: :hasMother
  AddTriple (1899a473-1102-4804-93d8-bad376bf34a1)
 Call ID: 1899a473-1102-4804-93d8-bad376bf34a1
  Args:
    target: Constantine I
    source: Paul of Greece
    relation: :hasFather
  AddTriple (428a0cf2-2829-4640-8033-7b4b0a71b393)
 Call ID: 428a0cf2-2829-4640-8033-7b4b0a71b393
  Args:
    relation: :hasMother
    target: Sophia of Greece
    source: Paul of Greece
  AddTriple (41742d3c-0d59-490a-beca-5bf8034943b4)
 Call ID: 41742d3c-0d59-490a-beca-5bf8034943b4
  Args:
    target: Constantine II
    source: Sofía
    relation: :hasBrother
  AddTriple (6dd45238-6e1c-4b1c-870d-1c4a6b454895)
 Call ID: 6dd45238-6e1c-4b1c-870d-1c4a6b454895
  Args:
    target: Irene
    source: Sofía
    relation: :hasSister
  AddTriple (890494c3-110a-40f1-8a10-17befbe6b988)
 Call ID: 890494c3-110a-40f1-8a10-17befbe6b988
  Args:
    relation: :hasParent
    target: Juan Carlos I
    source: Sofía
  AddTriple (9029689f-e411-45ec-a5fc-ebcad375b074)
 Call ID: 9029689f-e411-45ec-a5fc-ebcad375b074
  Args:
    relation: :hasChild
    target: Elena
    source: Sofía
  AddTriple (d11fa536-f413-45b3-970c-8c7139d266a6)
 Call ID: d11fa536-f413-45b3-970c-8c7139d266a6
  Args:
    relation: :hasChild
    source: Sofía
    target: Cristina
  AddTriple (58becf1a-a78e-4730-af59-318a19b7552c)
 Call ID: 58becf1a-a78e-4730-af59-318a19b7552c
  Args:
    relation: :hasChild
    source: Sofía
    target: Felipe VI
  AddTriple (15689c66-3d41-446d-a93c-4cffc0b738de)
 Call ID: 15689c66-3d41-446d-a93c-4cffc0b738de
  Args:
    relation: :hasChild
    target: Elena
    source: Juan Carlos I
  AddTriple (70afe53c-3aea-45e0-8f33-7f248616b1ae)
 Call ID: 70afe53c-3aea-45e0-8f33-7f248616b1ae
  Args:
    relation: :hasChild
    source: Juan Carlos I
    target: Cristina
  AddTriple (9ea9f165-9a18-4950-891a-50c32f47c5f1)
 Call ID: 9ea9f165-9a18-4950-891a-50c32f47c5f1
  Args:
    source: Juan Carlos I
    target: Felipe VI
    relation: :hasChild
  Finish (1398ae5c-ce46-4e13-b14e-b72b2ebb6215)
 Call ID: 1398ae5c-ce46-4e13-b14e-b72b2ebb6215
  Args: