================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
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
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix data: <http://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:Sof%C3%ADa a :Woman ;
    :hasBirthYear 1938 ;
    :hasBrother data:Constantine_II ;
    :hasChild data:Cristina,
        data:Elena,
        data:Felipe_VI ;
    :hasFather data:Paul_of_Greece ;
    :hasMarriageYear 1962 ;
    :hasMother data:Frederica_of_Hanover ;
    :hasParent data:Juan_Carlos_I ;
    :hasSister data:Irene .

data:Constantine_I a :Man .

data:Constantine_II a :Man .

data:Frederica_of_Hanover a :Woman .

data:Irene a :Woman .

data:Juan_Carlos_I a :Man ;
    :hasChild data:Cristina,
        data:Elena,
        data:Felipe_VI .

data:Paul_of_Greece a :Man ;
    :hasFather data:Constantine_I ;
    :hasMother data:Sophia_of_Greece .

data:Sophia_of_Greece a :Woman .

data:Cristina a :Woman .

data:Elena a :Woman .

data:Felipe_VI a :Man .



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (86c3833f-6d0d-4562-adce-1e7c858e582e)
 Call ID: 86c3833f-6d0d-4562-adce-1e7c858e582e
  Args:
    type: :Ancestor
    source: data:Juan_Carlos_I

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sophia_of_Greece a :Woman .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (3cb449cd-83d8-4000-8efc-694df5bc452b)
 Call ID: 3cb449cd-83d8-4000-8efc-694df5bc452b
  Args:
    target: data:Sophia_of_Greece
    source: data:Sof%C3%ADa
    relation: :hasMother

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover,
          data:Sophia_of_Greece ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .

  data:Sophia_of_Greece a :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (f51f889b-5755-4250-ad7f-fa7a16f0abf2)
 Call ID: f51f889b-5755-4250-ad7f-fa7a16f0abf2
  Args:
    relation: :hasMother
    source: data:Sof%C3%ADa
    target: data:Sophia_of_Greece

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sophia_of_Greece a :Woman .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (ad24ed32-1a4e-4ec5-9eeb-2d3972aec7c6)
 Call ID: ad24ed32-1a4e-4ec5-9eeb-2d3972aec7c6
  Args:
    relation: :isAncestorOf
    target: data:Sof%C3%ADa
    source: data:Sophia_of_Greece

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Sophia_of_Greece a :Woman ;
      :isAncestorOf data:Sof%C3%ADa .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ddcb19df-a5f3-4c1d-81b5-ff12379d3e9f)
 Call ID: ddcb19df-a5f3-4c1d-81b5-ff12379d3e9f
  Args:
    source: data:Sophia_of_Greece
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Sophia_of_Greece a :Ancestor,
          :Woman ;
      :isAncestorOf data:Sof%C3%ADa .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (08f9c302-f6c0-4cfe-8a4b-3117eff80da0)
 Call ID: 08f9c302-f6c0-4cfe-8a4b-3117eff80da0
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:9
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Paul_of_Greece is assigned to Sofía via hasFather, but Paul_of_Greece is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Paul_of_Greece', class=':Ancestor')


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Frederica_of_Hanover is assigned to Sofía via hasMother, but Frederica_of_Hanover is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Frederica_of_Hanover', class=':Ancestor')


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Constantine_I is assigned to Paul_of_Greece via hasFather, but Constantine_I is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Constantine_I', class=':Ancestor')


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Constantine_I is assigned to Paul_of_Greece via hasFather, but Constantine_I is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Constantine_I', class=':Ancestor')


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Paul_of_Greece is assigned to Sofía via hasFather, but Paul_of_Greece is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Paul_of_Greece', class=':Ancestor')


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Frederica_of_Hanover is assigned to Sofía via hasMother, but Frederica_of_Hanover is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Frederica_of_Hanover', class=':Ancestor')


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Constantine_I is assigned to Paul_of_Greece via hasFather, but Constantine_I is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Constantine_I', class=':Ancestor')


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Paul_of_Greece is assigned to Sofía via hasFather, but Paul_of_Greece is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Paul_of_Greece', class=':Ancestor')


  Violation [9]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Frederica_of_Hanover is assigned to Sofía via hasMother, but Frederica_of_Hanover is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Frederica_of_Hanover', class=':Ancestor')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (be92e437-c880-4fe1-85dc-e678aadb717e)
 Call ID: be92e437-c880-4fe1-85dc-e678aadb717e
  Args:
    source: data:Paul_of_Greece
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Ancestor,
          :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Sophia_of_Greece a :Ancestor,
          :Woman ;
      :isAncestorOf data:Sof%C3%ADa .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (2b15f5e0-7191-49df-8252-40551d17b2b2)
 Call ID: 2b15f5e0-7191-49df-8252-40551d17b2b2
  Args:
    source: data:Frederica_of_Hanover
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Constantine_I a :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Ancestor,
          :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Ancestor,
          :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Sophia_of_Greece a :Ancestor,
          :Woman ;
      :isAncestorOf data:Sof%C3%ADa .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b1b7b45f-09f2-4f44-9c15-62a7ae9156c2)
 Call ID: b1b7b45f-09f2-4f44-9c15-62a7ae9156c2
  Args:
    type: :Ancestor
    source: data:Constantine_I

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Constantine_I a :Ancestor,
          :Man .

  data:Constantine_II a :Man .

  data:Frederica_of_Hanover a :Ancestor,
          :Woman .

  data:Irene a :Woman .

  data:Juan_Carlos_I a :Ancestor,
          :Man ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI .

  data:Paul_of_Greece a :Ancestor,
          :Man ;
      :hasFather data:Constantine_I ;
      :hasMother data:Sophia_of_Greece .

  data:Sof%C3%ADa a :Woman ;
      :hasBirthYear 1938 ;
      :hasBrother data:Constantine_II ;
      :hasChild data:Cristina,
          data:Elena,
          data:Felipe_VI ;
      :hasFather data:Paul_of_Greece ;
      :hasMarriageYear 1962 ;
      :hasMother data:Frederica_of_Hanover ;
      :hasParent data:Juan_Carlos_I ;
      :hasSister data:Irene .

  data:Sophia_of_Greece a :Ancestor,
          :Woman ;
      :isAncestorOf data:Sof%C3%ADa .

  data:Cristina a :Woman .

  data:Elena a :Woman .

  data:Felipe_VI a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (bb92634d-e67e-4282-b97d-daf257b1b012)
 Call ID: bb92634d-e67e-4282-b97d-daf257b1b012
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (3aeab934-c6c2-4893-919e-69c8247daa48)
 Call ID: 3aeab934-c6c2-4893-919e-69c8247daa48
  Args: