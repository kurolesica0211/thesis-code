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
Queen Margrethe II


Margrethe II (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Danish: ; Margrethe Alexandrine Þórhildur Ingrid, born 16 April 1940) is a member of the Danish royal family who reigned as Queen of Denmark from 14 January 1972 until her abdication on 14 January 2024.
Margrethe was born into the House of Glücksburg, a cadet branch of the House of Oldenburg, during the reign of her paternal grandfather, King Christian X.
She is the eldest child of King Frederik IX and Queen Ingrid (born Princess of Sweden).
In 1967 she married Henri de Laborde de Monpezat, with whom she had two sons, Frederik and Joachim.
Margrethe succeeded her father upon his death in January 1972.
Margrethe has worked as a scenographer, costume designer, and illustrator of works by J. R. R. Tolkien.
Support for the monarchy in Denmark, alongside her personal popularity, gradually rose throughout the course of her reign, attaining around eighty per cent by the time of her abdication.
She was succeeded by her elder son, Frederik X.


Early life and education

Margrethe was born on 16 April 1940 at 10:10 CET at Frederik VIII's Palace, in her parents' residence at Amalienborg, the principal residence of the Danish royal family in the district of Frederiksstaden in central Copenhagen.
She was the first child of Crown Prince Frederik (later King Frederik IX) and Crown Princess Ingrid (later Queen Ingrid).
Her father was the elder son of the then-reigning King Christian X, while her mother was the only daughter of Crown Prince Gustaf Adolf of Sweden (later King Gustaf VI Adolf).
Her birth took place just one week after the beginning of Nazi Germany's occupation of Denmark following the war invasion.
Margrethe was baptised on 14 May at the Holmen Church in Copenhagen.
Her godparents were her grandfathers, King Christian X of Denmark and Crown Prince Gustaf Adolf of Sweden; her maternal great-grandfathers, King Gustaf V of Sweden and Prince Arthur, Duke of Connaught and Strathearn; her uncles Prince Knud of Denmark and Prince Gustaf Adolf, Duke of Västerbotten; as well as her first cousin twice removed, Prince Axel of Denmark.
She was named Margrethe—the Danish variation of her late maternal grandmother Crown Princess Margareta of Sweden's name—Alexandrine after her paternal grandmother, Queen Alexandrine, and Ingrid after her mother.
Like her maternal grandmother, Margrethe is known affectionately as "Daisy" to her family and close friends.
The birth of Margrethe's younger sisters Benedikte and Anne-Marie followed in 1944 and 1946, respectively.
The princesses grew up in apartments at Frederik VIII's Palace at Amalienborg in Copenhagen and in Fredensborg Palace in North Zealand.
Margrethe spent holidays with the royal family in her parents' residences at Gråsten Palace in Southern Jutland and Trend Hunting Lodge in Vesthimmerland in Northern Jutland.
On 20 April 1947, following the death of Christian X, Margrethe's father acceded to the throne as Frederik IX.
Education

Margrethe received her early education at home at Amalienborg Palace alongside a group of 6 girls her age.
Margrethe doesn't hold a full university degree but passed the examen philosophicum at University of Copenhagen in 1960 and subsequently undertook courses at several European universities: She studied prehistoric archaeology at Girton College, Cambridge, between 1960 and 1961 and political science at Aarhus University between 1961 and 1962, the Sorbonne in 1963 and the London School of Economics in 1965.
Between 1958 and 1970, Margrethe performed voluntary service with the Women's Flying Corps, a branch of the Home Guard, where she eventually rose to the rank of lieutenant.
Heir presumptive

At the time of her birth, only males could accede to the throne of Denmark, owing to the changes in succession laws enacted in the 1850s when the Glücksburg branch was chosen to succeed.
As Margrethe had no brothers, it was assumed that her uncle Prince Knud would one day assume the throne.
The process of changing the constitution started in 1947, not long after Margrethe's father acceded to the throne and it became clear that Queen Ingrid would have no more children.
The popularity of Frederik and his daughters and the more prominent role of women in Danish life started the complicated process of altering the constitution.
The new Act of Succession permitted female succession to the throne of Denmark, according to male-preference cognatic primogeniture, where a female can accede to the throne only if she does not have a brother.
Princess Margrethe therefore became heir presumptive.
Margrethe attended the traditional New Year Courts for the first time in 1956.
On her eighteenth birthday, 16 April 1958, Margrethe was given a seat in the Council of State.
In 1960, with her first cousin, Princess Margaretha of Sweden, and Princess Astrid of Norway, she travelled to the United States, which included a visit to Los Angeles, and to the Paramount Studios, where they met several celebrities, including Dean Martin, Jerry Lewis and Elvis Presley.
Marriage and family

While Margrethe studied in London, she met the French diplomat Henri de Laborde de Monpezat, who was legation secretary at the French Embassy in London.
Laborde de Monpezat received the style and title of "His Royal Highness Prince Henrik of Denmark" because of his new position as the spouse of the heir presumptive to the Danish throne.
Less than a year after the wedding, Margrethe gave birth to her first child, a son, on 26 May 1968.
By tradition, Danish kings were alternately named either Frederik or Christian.
She chose to maintain this by assuming the position of a Christian, and thus named her elder son Frederik.
In 1974, she and Henrik purchased Château de Cayx in the wine district of Cahors in Southern France.
Among others, Margrethe is the godmother of King Willem-Alexander of the Netherlands, Crown Prince Haakon of Norway and Prince Carl Philip of Sweden as well as actress Ellen Hillingsø and politician Marcus Knuth.
Margrethe announced in 2008 that her male-line descendants would bear the additional title of Count or Countess of Monpezat in recognition of her husband's ancestry.
In 2022, the Queen announced that, from the start of 2023, the descendants of Prince Joachim will only be able to use their titles of Count and Countess of Monpezat, their previous titles of Prince and Princess of Denmark ceasing to exist.
Her son, Joachim, daughter-in-law, Marie, former daughter-in-law, Alexandra, and eldest grandson, Nikolai, publicly expressed shock and confusion because of the decision, after which Margrethe released a statement in which she said that it saddened her that she had upset Joachim's family.
Along with her late husband, Margrethe has kept dachshunds since the 1970s.
As of April 2026, she has one dog, the dachshund Tilia, who was Prince Henrik's dog until his death in 2018 (her own dog, Helike, passed away the same year).
Reign

Accession

On 3 January 1972, three days after King Frederik IX delivered his New Year's address, he suffered a heart attack and was admitted to the Copenhagen Municipal Hospital.
Margrethe was subsequently designated regent due to her father's declining health.
She ascended the throne on Frederik's death on 14 January, becoming the first female Danish sovereign under the new Act of Succession.
The following day, Prime Minister Jens Otto Krag led her formal proclamation ceremony from the balcony of Christiansborg Palace, in which she also announced her royal motto as "God's help, the love of the people, Denmark's strength" (Danish: Guds hjælp, folkets kærlighed, Danmarks styrke).
Her regnal number was chosen in recognition of Margrethe I, the 14th-century queen regnant of the Kalmar Union.
As queen, she relinquished all the monarch's former titles except the title to Denmark, hence her style "By the Grace of God, Queen of Denmark" (Danish: Margrethe den Anden, af Guds Nåde Danmarks Dronning).
As a constitutional sovereign, Margrethe took no part in party politics and does not express any political opinions.
In practice, nearly all of the Queen's formal powers were exercised by the Cabinet of Denmark.
It was customary for Margrethe, as the Danish monarch, to host the annual New Year levées.
Every year on 1 January, a banquet was held for the government, the Speaker of the Danish Parliament, representatives of official Denmark and the Royal Court at Christian VIII's Palace at Amalienborg.
On day two, a levée was held at Christian VIII's Palace for the justices of Supreme Court of Denmark and the Officer Corps of the Royal Life Guards and the Guard Hussar Regiment, followed by a levée at Christiansborg Palace for the diplomatic corps.
Official duties

Up to the end of her reign, Margrethe held 72 Danish and eight foreign patronages as queen, including Aarhus Festuge, ARoS Aarhus Kunstmuseum, DaneAge Association, Danes Worldwide, the Danish Animal Welfare Society , the Danish Cancer Society , Den Gamle By, Det Classenske Fideicommis, the Danish Bible Society , Det Kongelige Vajsenhus, Diakonissestiftelsen, Foreningen Norden, Land of Legends (Sagnlandet Lejre), M/S Maritime Museum of Denmark, Moesgaard Museum, National Olympic Committee and Sports Confederation of Denmark, Nyborg Slot, Rebild National Park, the Royal Danish Academy of Music, Royal Danish Academy of Sciences and Letters, Royal Danish Yacht Club, Rungstedlund Foundation , Sankt Lukas Stiftelsen, Vallø stift and Vemmetofte.
In 2016, she contributed to a book about Denmark's history.
Until her abdication, Margrethe served as colonel-in-chief of the Princess of Wales's Royal Regiment, an infantry regiment of the British Army, following a tradition dating back to 1906 when Edward VII, married to Alexandra of Denmark, appointed his brother-in-law, Frederik VIII of Denmark, colonel-in-chief of the then Buffs (Royal East Kent Regiment).
As sovereign, Margrethe received 42 official state visits and she undertook 55 foreign state visits herself.
Residences

As queen, her official residences were Amalienborg (where she resides at Christian IX's Palace) in Copenhagen and Fredensborg Palace near Hillerød.
Her summer residences were Marselisborg Palace near Aarhus and Gråsten Palace near Sønderborg, the former home of her mother, Queen Ingrid, who died in 2000.
Immigration debate


In her New Year's address at the end of 1984, the Queen addressed the xenophobia experienced by many immigrants in Denmark: .mw-parser-output .templatequote{overflow:
In an interview within the 2016 book De dybeste rødder (The Deepest Roots), according to historians at the Saxo Institute of the University of Copenhagen, Margrethe showed a change in attitude to immigration towards a more conservative stance.
Silver, Ruby and Golden Jubilees

Margrethe marked her Silver Jubilee in 1997 with a religious service and a gala dinner attended by fellow Scandinavian royals.
Between Elizabeth II's death and her abdication, Margrethe was Europe's longest-reigning monarch, the world's only queen regnant, and the longest-serving incumbent female head of state.
Sitting reign record

In July 2023, the Danish Royal House recognized Margrethe II as Denmark's longest-reigning sitting monarch.
Though Christian IV reigned for more than 59 years between 1588 and 1648, he was not officially installed until 1596, ruling with a "guardian government" up until then.
, Margrethe announced her abdication, which took place on 14 January 2024, the 52nd anniversary of her accession to the throne.
Margrethe's elder son, Frederik, assumed the throne as Frederik X. Mirroring her first New Year Address in 1973, she said of the succession: "The support and assistance which I have received throughout the years, have been crucial to the success of my task.
"


Since her abdication, she has been referred to as "Her Majesty Queen Margrethe".
She is eligible to serve as regent in the event of the incapacity or absence of the King and Crown Prince Christian.
As regent, Margrethe can perform the duties of the head of state on certain occasions, for example during Frederik and Christian's stays abroad.
In October 2025, Margrethe undertook her first official visit abroad after her abdication when she visited Rome, Italy, in honour of the 10th anniversary of Queen Margrethe's Roman Prize, which aims to strengthen cultural ties between Denmark and Italy.
Health issues

Queen Margrethe II has had a number of health issues.
On 21 September 2022, the Danish Royal House disclosed in a press release that Margrethe had tested positive for COVID-19 a second time after attending the state funeral of Elizabeth II, her third cousin, in London.
Margrethe has been a chain smoker and was well known for her tobacco habit.
In 2023, the Court confirmed that Margrethe had quit smoking in connection with her back surgery the same year.
Public image and style

Margrethe wears designs by former Pierre Balmain designer Erik Mortensen, Jørgen Bender, and Birgitte Taulow.
"


A 2012 poll showed support for the monarchy in Denmark remained consistently high at around 82%, compared to less than half when she acceded to the throne in 1972.
Margrethe was included in Andy Warhol's portrait series in 1985 as one of four Reigning Queens, along with queens Ntfombi of Eswatini, Elizabeth II and Beatrix of the Netherlands.
Tributes

Margrethe, a musical about Margrethe II premiered under Danish conductor Mikkel Rønnow's direction in June 2023 at The Royal Danish Theatre and since The Concert Hall of Aarhus.
A drama series titled da:Margrethe (serie) created by Søren Sveistrup and based on Queen Margrethe II's life from her birth to her becoming heir presumptive in 1953 will premiere on TV2 in 2027.
Upon her abdication in 2024, tributes were paid to Margrethe, not only in Denmark, but from around the world.
Personal interests and artistic work

Alongside her sisters, Margrethe started dancing ballet as a child and she continued to take weekly lessons even after her accession to the throne.
Margrethe has maintained avid engagement with the creative arts throughout her reign.
Archaeology

Margrethe is known for her strong archaeological passion and has participated in several excavations, including in Italy, Egypt, Denmark, Sudan and South America.
She shared this interest with her grandfather, Gustaf VI Adolf of Sweden, with whom she visited multiple archaeological digs, among them in Etruria in 1962.
In the 2019 biography Dronning Margrethe, Margrethe revealed that if she hadn't been destined to become queen, she would have "tried to become an archaeologist".
Church textiles

Since the 1970s, Margrethe has designed and embroidered several vestments and church textiles for churches in Denmark, Greenland, Germany and England.
She has designed a chasuble for Fredensborg Palace Church which was since embroidered by her mother, Queen Ingrid, and appliquéd by her sister, Princess Benedikte.
In 1989, Margrethe designed the bishop's robe for the Diocese of Viborg.
In addition to the church textiles, Margrethe has designed various other things including an altarpiece for Skei Mountain Church in Norway, a Christmas spoon, the annual Danish Christmas seals in 1970, 2003 and 2015, and Greenland's Christmas seal in 1983.
Découpage

Since the mid-1970s, Margrethe has been using the découpage technique, which involves combining clippings from periodicals and books for new motifs.
The découpage often references literary, mythological, or art-historical topics, and is often displayed in royal palaces, particularly Christian VII's Palace at Amalienborg.
Margrethe's découpage works have also been used in various books and films, including Prince Henrik's poetry collections Cantabile (2000) and Frihjul (2010).
Embroidery

As a child, Margrethe preferred drawing rather than needlework, but since 1960, numerous embroideries have been presented as gifts or used in the Queen's own rooms.
The embroideries are made from patterns that Margrethe herself creates on graph paper, which includes twining shapes and the recipient's monogram.
Margrethe has also designed evening bags and spectacle cases for friends and family members, including Christmas calendars for all of the grandchildren, cushion covers and furniture covers for the palaces, and fireplace screens for Fredensborg Palace.
Films

The Queen has worked as a screenwriter alongside Per Brink Abrahamsen on the two Hans Christian Andersen adaptations The Snow Queen  from 2000 and The Wild Swans  from 2009.
Using decoupage as her primary craft, she has also been a set designer for:


For her work on Ehrengard: The Art of Seduction, Margrethe won the Robert Award for Best Costume Design at the 41st Robert Awards on 3 February 2024.
Monograms

In 2004, Margrethe designed the official monogram of her second cousin twice removed, Princess Ingrid Alexandra of Norway.
She has also designed her own personal monogram; the personal monograms of her son Frederik X, daughter-in-law Mary and grandson Christian; as well as the joint monograms of the Danish Crown Prince couple as well as the Norwegian Crown Prince couple, her godson Haakon, Crown Prince of Norway, and his wife Mette-Marit.
Scenography and costume design

Over the years, Margrethe has become involved in ballet as a scenographer and costume designer.
Margrethe has designed sets and costumes for numerous ballets.
Since 2001, she has worked with the Tivoli Ballet Theatre:


Visual art




Margrethe is an accomplished painter and has exhibited many of her works over the years.
In 2000, she illustrated Prince Henrik's poetry collection Cantabile.
Under the pseudonym Ingahild Grathmer (the latter being an anagram for Margrethe and the former made up of her secondary names Ingrid, Alexandrine and Þórhildur), her illustrations were used for Danish editions of The Lord of the Rings, which she was encouraged to illustrate in the early 1970s.



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
  AssignClass (69b7c5d7-7a1e-44a4-a1a7-08c95bea53d3)
 Call ID: 69b7c5d7-7a1e-44a4-a1a7-08c95bea53d3
  Args:
    source: MargretheII
    type: :Woman
  AssignClass (04f68c7a-3801-44ab-8dc3-008987e35400)
 Call ID: 04f68c7a-3801-44ab-8dc3-008987e35400
  Args:
    type: :Man
    source: FrederikIX
  AssignClass (7850196f-866f-4799-b454-66d830f99dd0)
 Call ID: 7850196f-866f-4799-b454-66d830f99dd0
  Args:
    type: :Woman
    source: Ingrid
  AssignClass (decabb08-32d9-4fa3-a383-6fb50e581666)
 Call ID: decabb08-32d9-4fa3-a383-6fb50e581666
  Args:
    type: :Man
    source: ChristianX
  AssignClass (6f9e3d2e-7177-4456-9d70-55e64a409730)
 Call ID: 6f9e3d2e-7177-4456-9d70-55e64a409730
  Args:
    source: GustafVIAldolf
    type: :Man
  AssignClass (0768c3bc-ffbe-476d-8cbe-353958a0b943)
 Call ID: 0768c3bc-ffbe-476d-8cbe-353958a0b943
  Args:
    type: :Man
    source: Henrik
  AssignClass (d5a5a213-137f-46ee-984e-1f2c2ad5ba65)
 Call ID: d5a5a213-137f-46ee-984e-1f2c2ad5ba65
  Args:
    source: FrederikX
    type: :Man
  AssignClass (12ddd211-36a6-482d-8456-ecf7b3894104)
 Call ID: 12ddd211-36a6-482d-8456-ecf7b3894104
  Args:
    source: Joachim
    type: :Man
  AssignClass (ab47282d-2ffc-4b52-9957-4c1853fcd92e)
 Call ID: ab47282d-2ffc-4b52-9957-4c1853fcd92e
  Args:
    type: :Woman
    source: Benedikte
  AssignClass (0613c026-4350-40f1-a00e-26e5df37423b)
 Call ID: 0613c026-4350-40f1-a00e-26e5df37423b
  Args:
    source: AnneMarie
    type: :Woman
  AddLiteral (c54959a9-8db0-46ed-8ea4-08b7d362b8ae)
 Call ID: c54959a9-8db0-46ed-8ea4-08b7d362b8ae
  Args:
    source: MargretheII
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1940
  AddTriple (6b1e725b-fafb-4407-aa2d-c055a40e00d4)
 Call ID: 6b1e725b-fafb-4407-aa2d-c055a40e00d4
  Args:
    source: MargretheII
    target: FrederikIX
    relation: :hasFather
  AddTriple (475e0758-ce2f-4403-b156-147a503e8124)
 Call ID: 475e0758-ce2f-4403-b156-147a503e8124
  Args:
    target: Ingrid
    source: MargretheII
    relation: :hasMother
  AddTriple (481583d5-2173-41d0-a1e7-ae7adb6b78f1)
 Call ID: 481583d5-2173-41d0-a1e7-ae7adb6b78f1
  Args:
    source: FrederikIX
    target: ChristianX
    relation: :hasFather
  AddTriple (b00f2b69-f511-4731-9ee6-83bf337a0e1b)
 Call ID: b00f2b69-f511-4731-9ee6-83bf337a0e1b
  Args:
    relation: :hasFather
    source: Ingrid
    target: GustafVIAldolf
  AddTriple (10a9aea5-3bf1-4e32-b2e9-1b993dad24f7)
 Call ID: 10a9aea5-3bf1-4e32-b2e9-1b993dad24f7
  Args:
    relation: :hasChild
    target: FrederikX
    source: MargretheII
  AddTriple (477398de-6baf-4180-afd6-cb7c56a99760)
 Call ID: 477398de-6baf-4180-afd6-cb7c56a99760
  Args:
    relation: :hasChild
    target: Joachim
    source: MargretheII
  AddTriple (b235c53c-d3c2-466b-a5cb-554f6e64c990)
 Call ID: b235c53c-d3c2-466b-a5cb-554f6e64c990
  Args:
    target: Henrik
    source: FrederikX
    relation: :hasFather
  AddTriple (63644ea2-f07e-40bd-bbf1-632aef0566b0)
 Call ID: 63644ea2-f07e-40bd-bbf1-632aef0566b0
  Args:
    source: FrederikX
    target: MargretheII
    relation: :hasMother
  AddTriple (1ede7084-ff48-4e80-9e0a-9648c50fc4f8)
 Call ID: 1ede7084-ff48-4e80-9e0a-9648c50fc4f8
  Args:
    relation: :hasFather
    source: Joachim
    target: Henrik
  AddTriple (6a1bb62d-e94c-4c23-841f-f2ee494fc08f)
 Call ID: 6a1bb62d-e94c-4c23-841f-f2ee494fc08f
  Args:
    relation: :hasMother
    target: MargretheII
    source: Joachim
  AddTriple (f1b21427-c899-43dd-936d-efca181176b8)
 Call ID: f1b21427-c899-43dd-936d-efca181176b8
  Args:
    relation: :isSiblingOf
    target: Benedikte
    source: MargretheII
  AddTriple (72f30e3b-d24f-46fd-ad50-c45d6a31774a)
 Call ID: 72f30e3b-d24f-46fd-ad50-c45d6a31774a
  Args:
    relation: :isSiblingOf
    source: MargretheII
    target: AnneMarie
  AddTriple (bba4a2e0-18a8-473a-a3aa-2264aea80bd3)
 Call ID: bba4a2e0-18a8-473a-a3aa-2264aea80bd3
  Args:
    relation: :isSiblingOf
    target: AnneMarie
    source: Benedikte
  AddTriple (ab9ba5b1-0ccb-43c6-8b3e-9988012dd095)
 Call ID: ab9ba5b1-0ccb-43c6-8b3e-9988012dd095
  Args:
    relation: :hasParent
    source: Benedikte
    target: FrederikIX
  AddTriple (38533a56-a715-4981-84f9-228910384b5d)
 Call ID: 38533a56-a715-4981-84f9-228910384b5d
  Args:
    source: Benedikte
    target: Ingrid
    relation: :hasParent
  AddTriple (c94b2e6f-f849-4e68-a2da-d11449689647)
 Call ID: c94b2e6f-f849-4e68-a2da-d11449689647
  Args:
    target: FrederikIX
    source: AnneMarie
    relation: :hasParent
  AddTriple (24d0ccfa-5d58-47ee-9c38-beb285889a36)
 Call ID: 24d0ccfa-5d58-47ee-9c38-beb285889a36
  Args:
    relation: :hasParent
    target: Ingrid
    source: AnneMarie
  Finish (154a7cc7-e93f-4267-b06f-27fb0fb622b3)
 Call ID: 154a7cc7-e93f-4267-b06f-27fb0fb622b3
  Args: