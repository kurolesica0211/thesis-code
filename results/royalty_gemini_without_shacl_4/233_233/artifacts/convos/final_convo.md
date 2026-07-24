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
  AssignClass (8199e69c-f370-4942-a392-b88311152c6b)
 Call ID: 8199e69c-f370-4942-a392-b88311152c6b
  Args:
    type: :Man
    source: Prince_Michael_of_Kent
  AssignClass (73cb96ee-83d2-4458-abd1-277f71087c90)
 Call ID: 73cb96ee-83d2-4458-abd1-277f71087c90
  Args:
    type: :Person
    source: Prince_Michael_of_Kent
  AddLiteral (b9f0530d-55ba-47b3-a4e8-c38fe31679c9)
 Call ID: b9f0530d-55ba-47b3-a4e8-c38fe31679c9
  Args:
    literal_value: 1942
    literal_type: xsd:positiveInteger
    source: Prince_Michael_of_Kent
    relation: :hasBirthYear
  AssignClass (0f66a614-62fb-4035-a075-c9e3e7fba0f4)
 Call ID: 0f66a614-62fb-4035-a075-c9e3e7fba0f4
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (ecf18f04-2cef-459f-916f-1e97d35b3d96)
 Call ID: ecf18f04-2cef-459f-916f-1e97d35b3d96
  Args:
    type: :Person
    source: Prince_George_Duke_of_Kent
  AssignClass (23a0e7fc-8bc5-4015-aa8a-e526ca1a7781)
 Call ID: 23a0e7fc-8bc5-4015-aa8a-e526ca1a7781
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (6ec033fa-4550-4773-bb39-f814bcb46275)
 Call ID: 6ec033fa-4550-4773-bb39-f814bcb46275
  Args:
    type: :Person
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (e7fcca19-0463-4774-acc4-29d5dd501ee2)
 Call ID: e7fcca19-0463-4774-acc4-29d5dd501ee2
  Args:
    source: Prince_Michael_of_Kent
    relation: :hasFather
    target: Prince_George_Duke_of_Kent
  AddTriple (3eb90b0b-772f-4a01-bb54-9904476edae5)
 Call ID: 3eb90b0b-772f-4a01-bb54-9904476edae5
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
    source: Prince_Michael_of_Kent
  AssignClass (8486de7d-451b-45ae-8353-c973cef552e6)
 Call ID: 8486de7d-451b-45ae-8353-c973cef552e6
  Args:
    type: :Man
    source: George_V
  AssignClass (ef937259-1b81-4800-87b9-76a3793af967)
 Call ID: ef937259-1b81-4800-87b9-76a3793af967
  Args:
    type: :Person
    source: George_V
  AssignClass (a2d0f6c2-d4da-48ac-9240-0e69756190e8)
 Call ID: a2d0f6c2-d4da-48ac-9240-0e69756190e8
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (e609f5ae-6c86-4f7e-93f2-a8d5d77fc16e)
 Call ID: e609f5ae-6c86-4f7e-93f2-a8d5d77fc16e
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (a0f3f33f-d808-4901-bb4e-c7ee12da0871)
 Call ID: a0f3f33f-d808-4901-bb4e-c7ee12da0871
  Args:
    source: Prince_George_Duke_of_Kent
    relation: :hasFather
    target: George_V
  AddTriple (def5db41-d555-4c4c-aa1b-c8bd610bb0bc)
 Call ID: def5db41-d555-4c4c-aa1b-c8bd610bb0bc
  Args:
    source: Prince_George_Duke_of_Kent
    target: Queen_Mary
    relation: :hasMother
  AssignClass (82137f52-6893-424c-937b-545d70bbea22)
 Call ID: 82137f52-6893-424c-937b-545d70bbea22
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (f9d984a9-9154-4594-86a0-a2e80792628b)
 Call ID: f9d984a9-9154-4594-86a0-a2e80792628b
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (959992ad-d8af-4b6f-b1ba-444237d5c486)
 Call ID: 959992ad-d8af-4b6f-b1ba-444237d5c486
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (4454c78f-3aee-4001-8854-9875a421035f)
 Call ID: 4454c78f-3aee-4001-8854-9875a421035f
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (440fbd31-a8a1-47e1-b3ee-cef58813d858)
 Call ID: 440fbd31-a8a1-47e1-b3ee-cef58813d858
  Args:
    target: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
    source: Princess_Marina_of_Greece_and_Denmark
  AddTriple (59ab81fa-25bc-41fb-ad73-9532376c85bd)
 Call ID: 59ab81fa-25bc-41fb-ad73-9532376c85bd
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AssignClass (43a7676f-3ea3-49b8-8a34-19827fda4709)
 Call ID: 43a7676f-3ea3-49b8-8a34-19827fda4709
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Kent
  AssignClass (8b4341aa-f53a-433e-971f-95d64a205b20)
 Call ID: 8b4341aa-f53a-433e-971f-95d64a205b20
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Kent
  AssignClass (7ebdf03e-b7cd-466e-8ccd-84f7b9997bee)
 Call ID: 7ebdf03e-b7cd-466e-8ccd-84f7b9997bee
  Args:
    type: :Woman
    source: Princess_Alexandra
  AssignClass (8156f684-7a51-4c35-be42-b1801d53df35)
 Call ID: 8156f684-7a51-4c35-be42-b1801d53df35
  Args:
    type: :Person
    source: Princess_Alexandra
  AddTriple (1a6227b1-1d51-4118-a337-680d90146aa4)
 Call ID: 1a6227b1-1d51-4118-a337-680d90146aa4
  Args:
    target: Prince_Edward_Duke_of_Kent
    relation: :isSiblingOf
    source: Prince_Michael_of_Kent
  AddTriple (bfe6bcf0-2ac0-41c1-977b-65e221a5164f)
 Call ID: bfe6bcf0-2ac0-41c1-977b-65e221a5164f
  Args:
    source: Prince_Michael_of_Kent
    target: Princess_Alexandra
    relation: :isSiblingOf
  AssignClass (2db9b8d2-99dc-48bd-b066-4d343ff24e93)
 Call ID: 2db9b8d2-99dc-48bd-b066-4d343ff24e93
  Args:
    type: :Woman
    source: Baroness_Marie_Christine_von_Reibnitz
  AssignClass (14cba0e8-a001-4d99-9083-66ea8dc0488e)
 Call ID: 14cba0e8-a001-4d99-9083-66ea8dc0488e
  Args:
    type: :Person
    source: Baroness_Marie_Christine_von_Reibnitz
  AddLiteral (90b60a2e-0151-4a80-9992-932f0095df98)
 Call ID: 90b60a2e-0151-4a80-9992-932f0095df98
  Args:
    relation: :hasMarriageYear
    source: Prince_Michael_of_Kent
    literal_type: xsd:positiveInteger
    literal_value: 1978
  AddTriple (46fefd44-4102-45e9-8e57-d4283b094a40)
 Call ID: 46fefd44-4102-45e9-8e57-d4283b094a40
  Args:
    source: Prince_Michael_of_Kent
    relation: :hasRelation
    target: Baroness_Marie_Christine_von_Reibnitz
  Finish (f25bcedf-7375-43c1-bf18-5995fc8fb619)
 Call ID: f25bcedf-7375-43c1-bf18-5995fc8fb619
  Args: