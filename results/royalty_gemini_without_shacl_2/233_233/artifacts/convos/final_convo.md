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
Prince Michael of Kent (Michael George Charles Franklin; born 4 July 1942) is a member of the British royal family who is 53rd in line to the British throne as of 2026.
The younger son of Prince George, Duke of Kent, and Princess Marina of Greece and Denmark, he is a grandson of George V, nephew of Edward VIII and George VI, and first cousin of Queen Elizabeth II.
Michael's mother was also a first cousin of Prince Philip, Duke of Edinburgh, consort of Queen Elizabeth II, making him both a second cousin and first cousin once removed to Charles III.
Michael occasionally represented Elizabeth II at some functions in Commonwealth realms outside the United Kingdom during her reign.
Early life

Michael was born at 7:35 pm on 4 July 1942 at Coppins, Iver, Buckinghamshire.
He was the third child of Prince George, Duke of Kent, who was the fourth son of King George V and Queen Mary and a younger brother of kings Edward VIII and George VI.
At birth, Michael was seventh in line to the British throne.
His mother was Princess Marina, a daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
At Michael's baptism on 4 August in the Private Chapel of Windsor Castle, his godparents were his paternal uncle the King; Queen Wilhelmina of the Netherlands (for whom her son-in-law Prince Bernhard stood proxy); King Haakon VII of Norway (his great-uncle); US President Franklin D. Roosevelt (for whom the Duke of Kent stood proxy); Frederica of Hanover, Hereditary Princess of Greece (his first cousin once removed, who was absent); Prince Henry, Duke of Gloucester (his paternal uncle, who was absent); the Dowager Marchioness of Milford Haven (his paternal first cousin twice removed); and Lady Patricia Ramsay (his paternal first cousin twice removed).
Seven weeks after Michael's birth, his father was killed in a plane crash near Dunbeath, Caithness, Scotland, on 25 August 1942.
At the age of five, Michael was a page boy at the wedding of his cousins Princess Elizabeth and Lieutenant Philip Mountbatten.
Education and military service

Michael was educated at Sunningdale School and Eton College and is fluent in French as well as  having a "working knowledge" of German and Italian.
Michael was commissioned into the 11th Hussars (Prince Albert's Own) in 1963.
He later served in The Royal Hussars (Prince of Wales's Own) after the amalgamation between the 11th Hussars and the 10th Royal Hussars (Prince of Wales's Own) in 1969.
In 1994, Michael was made Honorary Commodore (later Honorary Rear Admiral and then Vice Admiral) of the Royal Naval Reserve, and in 2002, he was made Honorary Air Commodore of RAF Benson (promoted to Honorary Air Marshal in 2012).
He is also Colonel-in-Chief of the Essex and Kent Scottish Regiment in Canada.
Activities and patronages

As the third child of George V's fourth son, it was not expected that Michael, as the only second son in the extended royal family, would undertake many engagements on behalf of the royal family.
He has, however, never received a parliamentary annuity or an allowance from the British Privy Purse, unlike both his elder brother, Prince Edward, Duke of Kent, and his sister, Princess Alexandra, who both carry out official royal duties.
Michael represented the Queen at state funerals in India, Cyprus and Swaziland and, with his wife, Princess Michael of Kent, represented the Queen at the independence celebrations in Belize, and at the coronation of King Mswati III of Swaziland.
Michael supports a large number of charities and organisations.
The Prince Michael Road Safety Award was created in 1987 to give public recognition to those improving road safety throughout Great Britain and later the world in general.
Michael also set up the Prince Michael of Kent Foundation in 2004 to support projects in Russia, including heritage and cultural restoration.
Marriage and personal life

On 30 June 1978, Michael married Baroness Marie-Christine von Reibnitz in a civil ceremony at the City Hall (Wiener Rathaus) in Vienna, Austria.
As a Roman Catholic divorcée, previously married to banker Thomas Troubridge, with a Church annulment granted in May 1978, Marie-Christine required papal dispensation for a Catholic ceremony.
Marie-Christine has named Lord Mountbatten as their matchmaker.
Under the terms of the Act of Settlement 1701, Michael forfeited his place in the line of succession to the throne through his marriage to a Catholic.
Michael and Marie-Christine have two children, both brought up as members of the Church of England and therefore in the line of succession to the throne since birth:
In 2014, Michael was successfully treated for prostate cancer.
Personal interests

Commercial

Michael manages his own consultancy business, and undertakes business throughout the world.
Masonic

Michael is an active Freemason.
He is the Grand Master of the Grand Lodge of Mark Master Masons, and Provincial Grand Master of the Provincial Grand Lodge of Middlesex.
Russia

Michael speaks fluent Russian and has a strong interest in Russia, where he is a well-known figure (he is a former recipient of the Order of Friendship).
Tsar Nicholas II was a first cousin of three of his grandparents: George V, Prince Nicholas of Greece and Denmark, and Grand Duchess Elena Vladimirovna of Russia.
When the bodies of the Tsar and some of his family were recovered in 1991, the remains were later identified by DNA using, among others, a sample from Michael for recognition.
He is also the second cousin of Maria Vladimirovna, Grand Duchess of Russia, who is a claimant to the headship of the Imperial Family of Russia.
They share the same great-grandfather, Grand Duke Vladimir Alexandrovich.
Michael is the patron of organisations which have close ties with Russia, including the Russo-British Chamber of Commerce and the St Gregory's Foundation.
In his capacity as patron of Children's Fire and Burns Trust, Michael has led fundraising rallies in 1999 and 2003 in Russia to raise money for the charity.
He also led another rally in 2005 and raised money for the Royal Marsden Hospital and Britain's Charities Aid Foundation Russia.
Michael served as the Patron of the Russo-British Chamber of Commerce (RBCC).
On 4 March 2022, Michael returned the Order of Friendship due to the Russian invasion of Ukraine.
Finland

Michael of Kent made a visit to Finland in 2017, during which he visited Helsinki, Espoo, Porvoo, Pori, and Tampere.
Sport

Michael was a part of the Royal Military Academy Sandhurst rowing crew that won the Maiden Fours at Bedford in 1961.
Media scrutiny

In 2002, both Michael and his wife were the subject of criticism over the rent paid on their accommodation at Kensington Palace following scrutiny by the House of Commons Public Accounts committee on the cost of royal palaces and whether they were value for money.
When it was claimed that the couple paid a rent of only £69 per week for the use of their apartments at Kensington Palace, Buckingham Palace announced that "The Queen is paying the rent for Prince and Princess Michael of Kent's apartment at a commercial rate of £120,000 annually, from her own private funds.
This rent payment by The Queen is in recognition of the Royal engagements and work for various charities which Prince and Princess Michael of Kent have undertaken at their own expense, and without any public funding.
"


In 2003, Michael's judgment was questioned as he developed a close working relationship with businessman Michael Wynne-Parker, who had a history of financial misconduct, bans from serving as a director, and had been described by a judge as having "the modus operandi of a crook".
Wynne-Parker had organised and accompanied the prince on official trips to Estonia, helping arrange meetings with politicians and business figures, which raised concerns about credibility and vetting.
Prince Michael denied receiving "any fees or expenses or been paid in any way" by Wynne-Parker and added that he was not aware of his reputation.
Michael has been scrutinized for financial assistance given to him by exiled Russian oligarch Boris Berezovsky through offshore companies, with a reported total of £320,000 in payments over the period 2002–2008.
In an interview with The Sunday Times, Berezovsky stated, "There is nothing underhand or improper about the financial assistance I have given Prince Michael.
"


In May 2021, reports were published stating that Michael was "selling access" to Vladimir Putin's political representatives.
Footage from a Zoom call was released of Michael, alongside Simon Isaacs, 4th Marquess of Reading, interacting with undercover reporters posing as business executives seeking to make contacts with the Kremlin.
Michael was being offered £143,000 for a proposal and £36,000 a month by the faux businessmen, which he expressed satisfaction with.
The Marquess claimed that Michael was the Queen's "unofficial ambassador to Russia" and had direct access to Putin.
He later stated that he had "overpromised", while Michael said that he had not had contact with Putin since 2003.
In a 2019 interview, Michael stated that he visited Russia twice a year as part of his work for the Russo-British Chamber of Commerce.
Marina Litvinenko denounced Michael's actions, saying that it demonstrated that he did not "care about human rights, democracy, about the people who are dying in Russia or what he did to your own citizens on UK soil".
I'd love to know what Prince Michael thinks he is doing by making the UK's values and standards look optional.
"


Titles, styles, honours and arms

Titles

Official

As a child of a younger son of a British sovereign, he is styled as a British prince with the prefix His Royal Highness and a territorial designation deriving from his father's dukedom: "His Royal Highness Prince Michael of Kent".
Other titles

Honours

Foreign

Wear of orders, decorations, and medals

The ribbons worn regularly by Michael in undress uniform are as follows:


Honorary military appointments

Fellowships

Memberships

Honorary academic degrees and awards

Degrees and appointments

Awards

Arms

Issue

Ancestry

See also

Notes

References

External links



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
  AssignClass (11e86663-af81-4406-8054-cd96d86244cf)
 Call ID: 11e86663-af81-4406-8054-cd96d86244cf
  Args:
    type: :Man
    source: Prince Michael of Kent
  AssignClass (053078e9-c9dc-467b-be60-bb590b5478f8)
 Call ID: 053078e9-c9dc-467b-be60-bb590b5478f8
  Args:
    source: Prince George, Duke of Kent
    type: :Man
  AssignClass (c2e91190-f0a1-4ffe-9dd0-2e38c0db2c73)
 Call ID: c2e91190-f0a1-4ffe-9dd0-2e38c0db2c73
  Args:
    source: Princess Marina of Greece and Denmark
    type: :Woman
  AssignClass (9f5e376a-52d1-4162-a9a0-0792bdcbb79c)
 Call ID: 9f5e376a-52d1-4162-a9a0-0792bdcbb79c
  Args:
    source: George V
    type: :Man
  AssignClass (bbff17d1-2b47-4b36-959a-df53a1e0d19c)
 Call ID: bbff17d1-2b47-4b36-959a-df53a1e0d19c
  Args:
    type: :Woman
    source: Queen Mary
  AssignClass (1ca43a74-dac0-4a94-b535-8ad704ca9f78)
 Call ID: 1ca43a74-dac0-4a94-b535-8ad704ca9f78
  Args:
    type: :Man
    source: Edward VIII
  AssignClass (582fc929-007d-4ca6-8b55-0369cef81092)
 Call ID: 582fc929-007d-4ca6-8b55-0369cef81092
  Args:
    source: George VI
    type: :Man
  AssignClass (75d42d4b-44f1-46c9-922f-05afdae04920)
 Call ID: 75d42d4b-44f1-46c9-922f-05afdae04920
  Args:
    type: :Man
    source: Prince Nicholas of Greece and Denmark
  AssignClass (84d9424c-d9c2-465d-acdf-3ee61ee49326)
 Call ID: 84d9424c-d9c2-465d-acdf-3ee61ee49326
  Args:
    type: :Woman
    source: Grand Duchess Elena Vladimirovna of Russia
  AssignClass (93b7704a-3233-4da0-a781-da1fd777774e)
 Call ID: 93b7704a-3233-4da0-a781-da1fd777774e
  Args:
    source: Baroness Marie-Christine von Reibnitz
    type: :Woman
  AssignClass (7c238a3a-ab89-4264-bd18-43cd47b5669c)
 Call ID: 7c238a3a-ab89-4264-bd18-43cd47b5669c
  Args:
    source: Prince Edward, Duke of Kent
    type: :Man
  AssignClass (01c46b68-f95c-43c4-8445-646502d03f1c)
 Call ID: 01c46b68-f95c-43c4-8445-646502d03f1c
  Args:
    source: Princess Alexandra
    type: :Woman
  AddLiteral (f9314af0-aabd-4c9d-8d68-df8c6e431199)
 Call ID: f9314af0-aabd-4c9d-8d68-df8c6e431199
  Args:
    source: Prince Michael of Kent
    literal_value: 1942
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddTriple (12d004d0-de41-4bde-85f3-44d8fdf9452c)
 Call ID: 12d004d0-de41-4bde-85f3-44d8fdf9452c
  Args:
    relation: :hasFather
    target: Prince George, Duke of Kent
    source: Prince Michael of Kent
  AddTriple (2e02e237-d9ed-4e84-a671-b6d7b0633575)
 Call ID: 2e02e237-d9ed-4e84-a671-b6d7b0633575
  Args:
    target: Princess Marina of Greece and Denmark
    relation: :hasMother
    source: Prince Michael of Kent
  AddTriple (9ccadc3a-eb97-4c97-9087-1d97024d61b3)
 Call ID: 9ccadc3a-eb97-4c97-9087-1d97024d61b3
  Args:
    target: George V
    relation: :hasFather
    source: Prince George, Duke of Kent
  AddTriple (c6e22357-c79d-4fd0-8c49-daa78ae510e0)
 Call ID: c6e22357-c79d-4fd0-8c49-daa78ae510e0
  Args:
    source: Prince George, Duke of Kent
    relation: :hasMother
    target: Queen Mary
  AddTriple (86f0e38c-5651-4e1a-8fbd-e58dd7a9b642)
 Call ID: 86f0e38c-5651-4e1a-8fbd-e58dd7a9b642
  Args:
    target: Prince Nicholas of Greece and Denmark
    relation: :hasFather
    source: Princess Marina of Greece and Denmark
  AddTriple (36d367f1-5aae-4fe1-a32c-1a23bad2ed77)
 Call ID: 36d367f1-5aae-4fe1-a32c-1a23bad2ed77
  Args:
    target: Grand Duchess Elena Vladimirovna of Russia
    relation: :hasMother
    source: Princess Marina of Greece and Denmark
  AddTriple (b9d01a3c-07e6-4b43-8e3b-1d20a5ee0947)
 Call ID: b9d01a3c-07e6-4b43-8e3b-1d20a5ee0947
  Args:
    target: Prince Edward, Duke of Kent
    relation: :hasBrother
    source: Prince Michael of Kent
  AddTriple (6a0eedeb-420f-4cb5-9fd2-fb77c243fbe7)
 Call ID: 6a0eedeb-420f-4cb5-9fd2-fb77c243fbe7
  Args:
    relation: :hasSister
    target: Princess Alexandra
    source: Prince Michael of Kent
  AddTriple (17196a12-65f2-42ef-8a12-006778d7027d)
 Call ID: 17196a12-65f2-42ef-8a12-006778d7027d
  Args:
    source: Prince George, Duke of Kent
    relation: :hasBrother
    target: Edward VIII
  AddTriple (168acf9c-afc5-4780-96c9-6f06197000a0)
 Call ID: 168acf9c-afc5-4780-96c9-6f06197000a0
  Args:
    source: Prince George, Duke of Kent
    target: George VI
    relation: :hasBrother
  AddTriple (d4e805f5-2521-4e98-9b1e-ae88a2087ccc)
 Call ID: d4e805f5-2521-4e98-9b1e-ae88a2087ccc
  Args:
    source: Prince Michael of Kent
    target: 1978
    relation: :hasMarriageYear
  AddTriple (007062e3-b691-41dd-abfa-6896cec54fd3)
 Call ID: 007062e3-b691-41dd-abfa-6896cec54fd3
  Args:
    relation: :hasRelation
    target: Baroness Marie-Christine von Reibnitz
    source: Prince Michael of Kent
  Finish (df4ad046-7b71-487c-8b75-4c71fc24fbfd)
 Call ID: df4ad046-7b71-487c-8b75-4c71fc24fbfd
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Prince_Michael_of_Kent a :Man ;
      :hasBirthYear "1942"^^xsd:positiveInteger ;
      :hasBrother data:Prince_Edward%2C_Duke_of_Kent ;
      :hasFather data:Prince_George%2C_Duke_of_Kent ;
      :hasMarriageYear data:1978 ;
      :hasMother data:Princess_Marina_of_Greece_and_Denmark ;
      :hasRelation data:Baroness_Marie-Christine_von_Reibnitz ;
      :hasSister data:Princess_Alexandra .

  data:Baroness_Marie-Christine_von_Reibnitz a :Woman .

  data:Edward_VIII a :Man .

  data:George_V a :Man .

  data:George_VI a :Man .

  data:Grand_Duchess_Elena_Vladimirovna_of_Russia a :Woman .

  data:Prince_Edward%2C_Duke_of_Kent a :Man .

  data:Prince_George%2C_Duke_of_Kent a :Man ;
      :hasBrother data:Edward_VIII,
          data:George_VI ;
      :hasFather data:George_V ;
      :hasMother data:Queen_Mary .

  data:Prince_Nicholas_of_Greece_and_Denmark a :Man .

  data:Princess_Alexandra a :Woman .

  data:Princess_Marina_of_Greece_and_Denmark a :Woman ;
      :hasFather data:Prince_Nicholas_of_Greece_and_Denmark ;
      :hasMother data:Grand_Duchess_Elena_Vladimirovna_of_Russia .

  data:Queen_Mary a :Woman .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['1978']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  RemoveLiteral (22d2b96f-e527-4078-ae96-20e69a6712c2)
 Call ID: 22d2b96f-e527-4078-ae96-20e69a6712c2
  Args:
    literal_type: xsd:string
    relation: :hasMarriageYear
    source: Prince Michael of Kent
    literal_value: 1978
  AddLiteral (ac0c3f2e-b43b-41bd-a3af-ab28b3a41316)
 Call ID: ac0c3f2e-b43b-41bd-a3af-ab28b3a41316
  Args:
    source: Prince Michael of Kent
    literal_value: 1978
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
  Finish (4d74180b-0414-4cfc-9373-7d10c4ef4f89)
 Call ID: 4d74180b-0414-4cfc-9373-7d10c4ef4f89
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Prince_Michael_of_Kent a :Man ;
      :hasBirthYear "1942"^^xsd:positiveInteger ;
      :hasBrother data:Prince_Edward%2C_Duke_of_Kent ;
      :hasFather data:Prince_George%2C_Duke_of_Kent ;
      :hasMarriageYear data:1978,
          "1978"^^xsd:positiveInteger ;
      :hasMother data:Princess_Marina_of_Greece_and_Denmark ;
      :hasRelation data:Baroness_Marie-Christine_von_Reibnitz ;
      :hasSister data:Princess_Alexandra .

  data:Baroness_Marie-Christine_von_Reibnitz a :Woman .

  data:Edward_VIII a :Man .

  data:George_V a :Man .

  data:George_VI a :Man .

  data:Grand_Duchess_Elena_Vladimirovna_of_Russia a :Woman .

  data:Prince_Edward%2C_Duke_of_Kent a :Man .

  data:Prince_George%2C_Duke_of_Kent a :Man ;
      :hasBrother data:Edward_VIII,
          data:George_VI ;
      :hasFather data:George_V ;
      :hasMother data:Queen_Mary .

  data:Prince_Nicholas_of_Greece_and_Denmark a :Man .

  data:Princess_Alexandra a :Woman .

  data:Princess_Marina_of_Greece_and_Denmark a :Woman ;
      :hasFather data:Prince_Nicholas_of_Greece_and_Denmark ;
      :hasMother data:Grand_Duchess_Elena_Vladimirovna_of_Russia .

  data:Queen_Mary a :Woman .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['1978']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (7ad728cc-e45b-4996-b1c5-fd53f24d5e5b)
 Call ID: 7ad728cc-e45b-4996-b1c5-fd53f24d5e5b
  Args:
    target: 1978
    relation: :hasMarriageYear
    source: Prince Michael of Kent
  Finish (7de723fe-eaae-480a-a7d8-b29aab9c8e5e)
 Call ID: 7de723fe-eaae-480a-a7d8-b29aab9c8e5e
  Args: