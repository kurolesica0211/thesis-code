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
Anne, Princess Royal (Anne Elizabeth Alice Louise; born 15 August 1950), is a member of the British royal family.
She is the second child and only daughter of Queen Elizabeth II and Prince Philip, Duke of Edinburgh, and the sister of King Charles III.
Third in the line of succession to the British throne at birth, she is 18th in line as of 2026.
She has held the title of Princess Royal since 1987.
Born at Clarence House, Anne was educated at Benenden School and began carrying out official royal duties in early adulthood.
In 1976, she became the first member of the British royal family to compete in the Olympic Games.
Anne continues to undertake engagements and official duties on behalf of the monarch – she has attended more than 20,000 such events since commencing royal duties in 1968.
In 1973, Anne married Captain Mark Phillips; the couple separated in 1989 and divorced in 1992.
They have two children, Peter Phillips and Zara Tindall.
In 1992, she married Commander (now Vice Admiral)
Sir Timothy Laurence, whom she met during his service as an equerry to Queen Elizabeth II.
Early life and education

Anne was born at 11:50 am on 15 August 1950 at Clarence House in London, during the reign of her maternal grandfather, King George VI.
She was the second child and only daughter of Princess Elizabeth, Duchess of Edinburgh (later Queen Elizabeth II), and Philip, Duke of Edinburgh.
Anne was baptised in the Music Room at Buckingham Palace on 21 October 1950, by the Archbishop of York, Cyril Garbett.
At the time of her birth, she was third in the line of succession to the British throne, behind her mother and elder brother, Charles (later King Charles III).
She rose to second in 1952 after her grandfather's death and her mother's accession; she is currently 18th in line.
A governess, Catherine Peebles, was appointed to oversee the early education of Anne and her brothers, Charles, Andrew, and Edward.
Peebles supervised Anne's lessons at Buckingham Palace.
Owing to her young age, Anne did not attend her mother's coronation in June 1953.
In May 1959, a Girl Guides unit, the 1st Buckingham Palace Guide Company, incorporating the  Holy Trinity Brompton Brownie pack, was re-formed specifically so that Anne, like her mother and her aunt Princess Margaret before her, could socialise with girls her own age.
The company remained active until 1963, when Anne left for boarding school.
She began undertaking royal engagements in 1969, at the age of 18.
In 1970, Anne briefly had a relationship with Andrew Parker Bowles, who later married Camilla Shand.
Camilla subsequently became the second wife and queen consort of Anne's elder brother, Charles III.
Anne was also briefly linked to the Olympic equestrian Richard Meade.
Equestrianism

In spring 1971, Anne finished fourth at the Rushall Horse Trials.
She also rode winners in horse racing, competing in the Grand Military Steeplechase at Sandown Park Racecourse and the Diamond Stakes at Royal Ascot.
For more than five years, Anne competed with the British eventing team, winning silver medals in both the individual and team disciplines at the 1975 European Eventing Championship.
The following year, she took part in the 1976 Olympic Games in Montreal as a member of the British team, riding the Queen's horse Goodwill in Eventing.
Anne suffered a concussion halfway through the cross-country course but remounted and completed the event; she later stated that she had no memory of making the remaining jumps.
Anne served as president of the Fédération Équestre Internationale from 1986 until 1994.
On 5 February 1987, she became the first member of the royal family to appear as a contestant on a television quiz show when she took part in the BBC panel game A Question of Sport.
In June 2024, Anne was taken to Southmead Hospital in Bristol with minor injuries and concussion, believed to have been caused by an impact with a horse's legs or head.
Marriages and children

Marriage to Mark Phillips

Anne met Mark Phillips, a lieutenant in the 1st Queen's Dragoon Guards, in 1968 at a party for horse enthusiasts.
Media reports stated that Phillips was offered an earldom, as was then customary for untitled men marrying into the royal family, but he and Anne declined the honour.
The couple had two children: Peter (born 1977) and Zara Phillips (born 1981).
Anne and Phillips have five grandchildren.
On 31 August 1989, Anne and Phillips announced their intention to separate; the couple had been rarely seen together in public, and both had been romantically linked with other people.
On 13 April 1992, the Palace announced that Anne had filed for divorce, which was finalised ten days later.
Marriage to Sir Timothy Laurence

Anne met Timothy Laurence, a commander in the Royal Navy, while he was serving on the Royal Yacht Britannia.
Their relationship developed in early 1989, three years after Laurence had been appointed an equerry to the Queen.
In 1989, the existence of private letters from Laurence to Anne was revealed by The Sun newspaper.
For the wedding, Anne wore a white jacket over a "demure, cropped-to-the-knee dress" and a spray of white flowers in her hair.
Kidnapping attempt

On 20 March 1974, Anne and Mark Phillips were returning to Buckingham Palace when a car forced their Rolls-Royce to stop on Pall Mall.
Inspector James Beaton, Anne's personal protection officer, left the car to shield her and attempted to disarm Ball.
Beaton's Walther PPK jammed, and he was shot, as was Anne's chauffeur, Alex Callender, when he tried to intervene.
Ball approached Anne's car and told her that he intended to kidnap her and hold her for ransom, the amount reported variously as £2 million or £3 million, which he claimed he intended to donate to the National Health Service.
When Ball ordered Anne to get out of the car, she replied, "Not bloody likely!"
Anne eventually exited from the opposite side of the limousine, as did her lady-in-waiting, Rowena Brassey.
A passing pedestrian, former boxer Ron Russell, punched Ball and led Anne away from the scene.
Police Constable Michael Hills then arrived; he too was shot, but had already called assistance.
Detective Constable Peter Edmonds responded, pursued Ball, and arrested him.
Beaton, who had been Anne's sole bodyguard, later reflected on royal security at the time "I had nothing...
For his defence of Anne, Beaton was awarded the George Cross by the Queen, who was visiting Indonesia when the incident occurred; Hills and Russell were awarded the George Medal, and Callender, McConnell, and Edmonds were awarded the Queen's Gallantry Medal.
Anne visited Beaton in hospital to thank him.
It was widely reported that the Queen paid off Russell's mortgage, but this was untrue: Russell stated in 2020 that a police officer had suggested it might happen, leading him to stop making payments and nearly lose his home after four months.
The attempted kidnapping is the subject of the Granada Television docudrama To Kidnap a Princess (2006) and inspired storylines in Tom Clancy's novel Patriot Games.
Activities

Public appearances

Anne undertakes a wide range of duties and engagements on behalf of the sovereign.
Kevin S. MacLeod, the then Canadian Secretary to the Queen, said of her in 2014: "Her credo is, 'Keep me busy.
In December 2017, it was reported that Anne had carried out the most official engagements that year of any member of the royal family, including the Queen.
Anne's first public engagement took place in 1969, when she opened an educational and training centre in Shropshire.
In 1990, she became the first member of the royal family to make an official visit to the Soviet Union, travelling there as a guest of President Mikhail Gorbachev and his government.
In August 2016, Anne returned to Russia to visit the city of Arkhangelsk for the 75th anniversary of Operation Dervish, one of the first Arctic convoys of World War II.
In April 2022, Anne and her husband toured Australia and Papua New Guinea to mark the Queen's Platinum Jubilee.
On 12 September 2022, at St Giles' Cathedral in Edinburgh, Anne became the first woman to participate in a Vigil of the Princes, standing guard by her mother's coffin.
It was later revealed that she had been the informant at her mother's death at Balmoral, signing the death certificate alongside the attending doctor.
On 21 April 2026, Anne opened the Queen Elizabeth II Garden on the centenary of her mother's birth.
Patronages

Anne is involved with more than 200 charities and organisations in an official capacity.
She founded The Princess Royal Trust for Carers in 1991.
She is also patron of St. Andrew's First Aid.
Anne serves as a British representative in the International Olympic Committee as an administrator, and was a member of the London Organising Committee for the Olympic Games.
Following the retirement of the Queen Mother in 1981, Anne was elected by graduates of the University of London as Chancellor, a position she has held since that year.
In 2007, she was appointed by the Queen as Grand Master of the Royal Victorian Order, a role previously held by her grandmother.
She is a Royal Fellow of both the Royal Society and the Academy of Medical Sciences, becoming the latter's first Royal Fellow.
As of 2022, the Royal Society has four Royal Fellows:
Anne; William, Prince of Wales; Edward, Duke of Kent; and King Charles.
Anne was elected Chancellor of the University of Edinburgh with effect from 31 March 2011, succeeding her father, who stepped down in 2010.
Also in 2011, she became president of City and Guilds of London Institute, Master of the Corporation of Trinity House, and president of the Royal Society of Arts, all in succession to her father.
In 2023, she succeeded the Duke of Kent as president of the Commonwealth War Graves Commission.
Anne is the patron of Transaid, a charity founded by Save the Children and the Chartered Institute of Logistics and Transport that aims to provide safe and sustainable transport in developing countries.
She has been patron of the Royal National Children's Foundation since 2002, and of the industrial heritage museum, Aerospace Bristol since 2016.
In 2022, Anne was named honorary chair of National Lighthouse Museum's Illuminating Future Generations campaign, a project established to raise funds for the museum's gallery space.
She is also patron of the Royal College of Occupational Therapists, the Special Forces Club, Royal College of Midwives, Royal College of Emergency Medicine, Magpas Air Ambulance, Edinburgh University's Royal (Dick) School of Veterinary Studies, Royal Holloway, University of London, International Students House, London, Acid Survivors Trust International, Townswomen's Guilds, Citizens Advice, the Royal Edinburgh Military Tattoo, the Scottish Rugby Union, and the Royal Society of Arts, Manufactures and Commerce.
In 2017, Anne became Prime Warden of the Worshipful Company of Fishmongers and a Governor of Gresham's School.
In 2025, she was announced as patron of Friends of the Elderly, taking on the role previously held by Queen Elizabeth II for more than 60 years.
Public image and style

Anne has been described as the royal family's "trustiest anchor" and a "beacon of good, old-fashioned public service" and has carried out more than 20,000 engagements since her 18th birthday.
In her early adulthood, she was characterised as a "royal renegade" for choosing to forgo titles for her children despite being the "spare to the heir".
The media often labelled the young Anne "aloof" and "haughty", earning her the nickname "her royal rudeness".
Vanity Fair wrote that Anne "has a reputation for having inherited her father's famously sharp tongue and waspish wit".
She has frequently been named the "hardest working royal", and carried out 11,088 engagements between 2002 and 2022, more than any other member of the royal family.
Anne remains one of Britain's most popular royals.
Tominey wrote that Anne's public role is a "contradiction of both protocol taskmaster and occasional rule-breaker".
Anne reportedly "insists on doing her own make-up and hair" and sometimes drives herself to engagements, having pleaded guilty to two separate speeding offences after running late.
In 1974, she became the first member of the royal family to hold an HGV licence, later saying "I was considering earning my living by driving, and with my HGV licence, I don't mind spending time on my own behind the wheel".
She does not shake hands with the public during walkabouts, explaining, "the theory was that you couldn't shake hands with everybody, so don't start."
British Vogue editor Edward Enninful has said that "Princess Anne is a true style icon and was all about sustainable fashion before the rest of us really knew what that meant".
She is known for recycling outfits, including a floral-print dress worn both to the wedding of the Prince of Wales in 1981 and the wedding of Lady Rose Windsor in 2008.
Anne is patron of the UK Fashion and Textile Association.
She is also one of the few women in the royal family to wear a military uniform.
According to The Guardian, she is "rarely seen without a brooch" at royal events.
She presented the Queen Elizabeth II award for British design at London Fashion Week in 2020.
Anne has appeared on three British Vogue covers: the September 1971 issue at age 21, and the May and November 1973 issues marking her engagement to Mark Phillips.
Anne is the first member of the royal family to have been convicted of a criminal offence.
Titles, styles, honours and arms

Titles and styles

Anne is the seventh Princess Royal, an appellation granted only to the eldest daughter of the Sovereign.
The previous holder was Princess Mary, Countess of Harewood, the daughter of King George V and Anne's great-aunt.
Honours

Anne is a Royal Knight Companion of the Most Noble Order of the Garter, an Extra Knight of the Most Ancient and Most Noble Order of the Thistle, Grand Master and Dame Grand Cross of the Royal Victorian Order, and a Dame Grand Cross of the Most Venerable Order of the Hospital of St John of Jerusalem.
She is a recipient of the Royal Family Order of Elizabeth II, the Royal Family Order of Charles III, and serves as a Personal Aide-de-Camp to the Sovereign.
Arms

Ancestry

Anne's ancestry can be traced as far back as Cerdic, King of Wessex (519–534).



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
  AssignClass (e1231979-bafe-4b08-a783-96b6e81c0482)
 Call ID: e1231979-bafe-4b08-a783-96b6e81c0482
  Args:
    source: Anne, Princess Royal
    type: :Woman
  AssignClass (e0317229-4364-460a-b83e-af06e0793c5f)
 Call ID: e0317229-4364-460a-b83e-af06e0793c5f
  Args:
    source: Anne, Princess Royal
    type: :Person
  AssignClass (c39e38fd-7a93-4c1b-957b-4fe2dfe860e7)
 Call ID: c39e38fd-7a93-4c1b-957b-4fe2dfe860e7
  Args:
    type: :Woman
    source: Queen Elizabeth II
  AssignClass (207ee456-50a4-4883-b618-9259a890dd04)
 Call ID: 207ee456-50a4-4883-b618-9259a890dd04
  Args:
    type: :Person
    source: Queen Elizabeth II
  AssignClass (e81112a9-7fa6-426e-9c0e-400232232aab)
 Call ID: e81112a9-7fa6-426e-9c0e-400232232aab
  Args:
    type: :Man
    source: Prince Philip, Duke of Edinburgh
  AssignClass (d6933680-7a20-4a68-b786-6cc6f532e664)
 Call ID: d6933680-7a20-4a68-b786-6cc6f532e664
  Args:
    source: Prince Philip, Duke of Edinburgh
    type: :Person
  AssignClass (4c616885-e612-44ac-9cbd-63662a1f1771)
 Call ID: 4c616885-e612-44ac-9cbd-63662a1f1771
  Args:
    source: King Charles III
    type: :Man
  AssignClass (87fbfb86-2fe1-48ca-8af4-23570004d2b6)
 Call ID: 87fbfb86-2fe1-48ca-8af4-23570004d2b6
  Args:
    source: King Charles III
    type: :Person
  AssignClass (2150dd18-0639-4f08-a320-c34a01d22242)
 Call ID: 2150dd18-0639-4f08-a320-c34a01d22242
  Args:
    type: :Man
    source: Mark Phillips
  AssignClass (e3d9596a-0019-46a5-ba85-7ca8a7c5e623)
 Call ID: e3d9596a-0019-46a5-ba85-7ca8a7c5e623
  Args:
    source: Mark Phillips
    type: :Person
  AssignClass (e33cdfcc-758b-46af-af39-f1bfe5d557cf)
 Call ID: e33cdfcc-758b-46af-af39-f1bfe5d557cf
  Args:
    source: Peter Phillips
    type: :Man
  AssignClass (b0425ed0-3f45-44d1-b88b-22033798cdc5)
 Call ID: b0425ed0-3f45-44d1-b88b-22033798cdc5
  Args:
    type: :Person
    source: Peter Phillips
  AssignClass (90e9be49-dfbc-498e-ab08-69fa907de9c0)
 Call ID: 90e9be49-dfbc-498e-ab08-69fa907de9c0
  Args:
    source: Zara Tindall
    type: :Woman
  AssignClass (573350c8-17bb-432b-acdb-802b2ce34672)
 Call ID: 573350c8-17bb-432b-acdb-802b2ce34672
  Args:
    type: :Person
    source: Zara Tindall
  AssignClass (60075e09-93cf-4bd8-8873-5e6fb99c7cbe)
 Call ID: 60075e09-93cf-4bd8-8873-5e6fb99c7cbe
  Args:
    type: :Man
    source: Timothy Laurence
  AssignClass (45167060-9c51-401a-beb4-165e5131eb49)
 Call ID: 45167060-9c51-401a-beb4-165e5131eb49
  Args:
    source: Timothy Laurence
    type: :Person
  AddLiteral (b94203be-8f5a-4e0f-92ba-56faeefbc636)
 Call ID: b94203be-8f5a-4e0f-92ba-56faeefbc636
  Args:
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    literal_value: 1950
    source: Anne, Princess Royal
  AddTriple (d07b37ec-1af5-4e2d-8c17-269760779ed5)
 Call ID: d07b37ec-1af5-4e2d-8c17-269760779ed5
  Args:
    target: Queen Elizabeth II
    source: Anne, Princess Royal
    relation: :hasMother
  AddTriple (a83396e6-7c3f-4afa-9b87-a70a2accce60)
 Call ID: a83396e6-7c3f-4afa-9b87-a70a2accce60
  Args:
    target: Prince Philip, Duke of Edinburgh
    relation: :hasFather
    source: Anne, Princess Royal
  AddTriple (55ee56b0-123a-45cc-a862-a331e09937f8)
 Call ID: 55ee56b0-123a-45cc-a862-a331e09937f8
  Args:
    relation: :isSisterOf
    source: Anne, Princess Royal
    target: King Charles III
  AddTriple (89513b36-630f-420f-9bc5-54b2735b89c6)
 Call ID: 89513b36-630f-420f-9bc5-54b2735b89c6
  Args:
    target: Peter Phillips
    relation: :hasChild
    source: Anne, Princess Royal
  AddTriple (0ef37afb-5594-4c01-b03f-adef8ca76a3d)
 Call ID: 0ef37afb-5594-4c01-b03f-adef8ca76a3d
  Args:
    target: Zara Tindall
    source: Anne, Princess Royal
    relation: :hasChild
  AddTriple (391b8fda-7811-47eb-a647-b4fddf9bb702)
 Call ID: 391b8fda-7811-47eb-a647-b4fddf9bb702
  Args:
    relation: :hasChild
    source: Mark Phillips
    target: Peter Phillips
  AddTriple (7b7027c6-5e16-4a6c-9d3e-1440f44c8ef5)
 Call ID: 7b7027c6-5e16-4a6c-9d3e-1440f44c8ef5
  Args:
    source: Mark Phillips
    relation: :hasChild
    target: Zara Tindall
  Finish (35c3252a-f11a-466f-b9c4-bc7325e0ab85)
 Call ID: 35c3252a-f11a-466f-b9c4-bc7325e0ab85
  Args: