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
Prince Bernhard of Lippe-Biesterfeld (later Prince Bernhard of the Netherlands; 29 June 1911 – 1 December 2004) was Prince of the Netherlands from 6 September 1948 to 30 April 1980 as the husband of Queen Juliana.
They had four daughters together, including Queen Beatrix of the Netherlands.
Bernhard belonged to the German princely House of Lippe-Biesterfeld and was a nephew of the last sovereign prince of Lippe, Leopold IV.
From birth he held the title Count of Biesterfeld; his uncle raised him to princely rank with the style of Serene Highness in 1916.
In 1937 he married Princess Juliana of the Netherlands, and was immediately given the title Prince of the Netherlands with the style of Royal Highness.
Upon his wife's accession to the throne in 1948, he became prince consort.
Bernhard was an early member of the Nazi Party (NSDAP) as well as the brown shirts or Sturmabteilung (SA), and served as an officer in the Schutzstaffel (SS).
He switched his political allegiance to the Allies after the invasion of the Netherlands.
Until his death, Bernhard denied being a NSDAP member or holding a NSDAP membership card.
He was respected for his performance as a combat pilot and his activities as a liaison officer and personal aide to his mother-in-law, Queen Wilhelmina, during the conflict, and for his work during post-war reconstruction.
He was also an honorary general officer in the Dutch army and was an observer in negotiating the terms of surrender of Nazi forces in the Netherlands.
Officially for proven bravery, leadership and loyalty during his wartime efforts, he was appointed a Commander of the Military William Order, the Netherlands' oldest and highest honour.
In 1969, Bernhard was awarded the Grand Cross (Special Class) of the Order of Merit of the Federal Republic of Germany.
Bernhard helped found the World Wildlife Fund (WWF, later renamed World Wide Fund for Nature), becoming its first president in 1961.
In 1970, along with Prince Philip, Duke of Edinburgh, and other associates, he established the WWF's financial endowment "The 1001: A Nature Trust".
Early life

Bernhard was born Bernhard Leopold Friedrich Eberhard Julius Kurt Karl Gottfried Peter, Count of Biesterfeld in Jena, Saxe-Weimar-Eisenach, German Empire on 29 June 1911, the elder son of Prince Bernhard of Lippe and his wife, Baroness Armgard von Sierstorpff-Cramm, member of one of the oldest Lower Saxon noble families, House of Cramm.
He was a grandson of Ernest, Count of Lippe-Biesterfeld, who was regent of the Principality of Lippe until 1904, and was also a nephew of the principality's last sovereign, Leopold IV, Prince of Lippe.
Because his parents' marriage did not conform with the marriage laws of the House of Lippe, it was initially deemed morganatic, as Armgard did not belong by birth to any ruling or the former ruling families of Europe, Bernhard was granted only the title of Count of Biesterfeld at birth.
In 1916, his uncle Leopold IV as reigning Prince raised him and his mother to the rank of Prince and Princess of Lippe-Biesterfeld, thereby retroactively according his parents' marriage dynastic status.
The suffix Biesterfeld revived the beginning of a new cadet line of the House of Lippe.
After World War I, Bernhard's family lost their German Principality and the revenue that had accompanied it, but the family was still reasonably well-off.
Bernhard spent his early years at Reckenwalde palace (Wojnowo, Poland), the family's new estate in East Brandenburg, thirty kilometres east of the River Oder.
Bernhard suffered from poor health as a boy.
This prediction might have inspired Bernhard's reckless driving and the risks that he took in the Second World War and thereafter.
The prince wrecked several cars and planes in his lifetime.
Bernhard studied law at the University of Lausanne, Switzerland, in fall 1929 until the spring of 1930, then in Berlin, then in Munich the following year in the fall of 1931, and then again in Berlin.
In Munich Bernhard enrolled himself on 24 October 1930.
(He later suffered a broken neck and crushed ribs in a 160 km/h (100 mph) car crash after his marriage to princess Juliana in 1938).
Bernhard was an active member of the Motor-SA and of the Deutsche Studentenschaft, where he inscribed himself on 27 April 1933.
While at university in Berlin for the year 1933, Bernhard joined the Nazi Party, exactly dated on his membership card as 1 May 1933.
Bernhard left Berlin in December 1934 when he graduated and went to work for IG Farben.
The Prince later denied that he had belonged to SA, to the Reiter-SS (SS Cavalry Corps), and to the paramilitary National-sozialistisches Kraftfahrerkorps (NSKK), but these are well-documented memberships.
According to journalist Philip Dröge, Bernhard was also a member of Nazi youth movement Sturm.
While he was not a fierce champion of democracy, the Prince was never known to hold any radical political views or express any racist sentiments, although he admitted that he briefly had sympathised with Adolf Hitler's regime.
van der Zijl clearly demonstrates, that Bernhard again and again fabulates on his memberships and other activities, to enhance his postwar stance that he never willingly would have joined any Nazi-organization.
In October 2023, Bernhard's original NSDAP membership card was discovered in his old residence in Germany.
The Prince eventually went to work for the German chemical giant IG Farben in the early-to-mid 1930s, then the world's fourth-largest company.
After training, Bernhard became a secretary in 1935 to the board of directors at IG Farben's Paris office.
Marriage and children

Bernhard met then-Princess Juliana at the 1936 Winter Olympics at Garmisch-Partenkirchen.
Juliana's mother, Queen Wilhelmina, had spent most of the 1930s looking for a suitable husband for Juliana.
As a Protestant of royal rank (the House of Lippe was a sovereign house in the German Empire), Bernhard was deemed acceptable for the devoutly religious Wilhelmina.
They were distantly related, seventh cousins, both descending from Lebrecht, Prince of Anhalt-Zeitz-Hoym.
Wilhelmina left nothing to chance, and had her lawyers draft a very detailed prenuptial agreement that specified exactly what Bernhard could and could not do.
Earlier, Bernhard had been granted Dutch citizenship and changed the spelling of his names from German to Dutch.
Prince Bernhard fathered six children, four of them with Queen Juliana.
The eldest daughter is Beatrix, (born 1938), who later became Queen of the Netherlands.
His other daughters with Juliana are Irene (born 1939), Margriet (born 1943) and Christina (1947–2019).
In December 2004, Dutch historian Cees Fasseur claimed that Jonathan Aitken, former British Conservative Cabinet Minister, is also a child of Prince Bernhard, the result of his wartime affair with Penelope Maffey.


1930s:
Relationship with Nazi Party

Prince Bernhard was a member of the "Reiter-SS", a mounted unit of the SS, part of the National Socialist Motor Corps.
Bernhard denied being a paid or active member of the Nazi party throughout his life, although he did admit to being part of the movement as part of the Sturmabteilung; he falsely claimed it was needed for him to be member of this organization as a student at the university.
Bernhard claimed to have severed all ties to the ruling Nazi regime in 1937 when he married princess Juliana of the Netherlands.
Protocol demanded that the prospective Prince-Consort be invited to an audience with his head of state, who was Adolf Hitler.
Hitler gave an account of the conversation that he had with Bernhard in his Tischgespräche (Table Conversations).
In those notes, Hitler is recorded to have said that Bernhard approached him, shortly after the start of the Nazi regime, with an offer of support to increase German influence in the Netherlands.
When asked in an interview in 2004 why he changed sides and started fighting against his homeland Germany, Bernhard claimed that he did not believe that Hitler and his regime had no plans to invade the Netherlands.
Once Germany attacked his new homeland of the Netherlands in 1940; Bernhard's feelings towards his birth country of Germany changed to antagonism, and he had no problems fighting against Germany for the rest of the war.
The Dutch government's information bureau Rijksvoorlichtingsdienst (RVD) would later confirm in 2023, years after the death, that Bernhard was member of the NSDAP, and that the Koninklijk Huisarchief (Royal House Archive) does still have Bernhard's original party membership card in his file.
Second World War

At the outset of the Second World War, during the German invasion of the Netherlands; the prince, carrying a machine gun, organised the palace guards into a combat group and shot at German warplanes.
The royal family fled the Netherlands and took refuge in England.
Disagreeing with Queen Wilhelmina's decision to leave the Kingdom, the prince, aged 28, is said at first to have refused to go and to have wanted to oppose the German occupation from within the country.
His wife Princess Juliana and their children continued on to Canada, where they remained until the end of the war.
In England, Prince Bernhard asked to work in British Intelligence.
On the recommendation of Bernhard's friend and admirer King George VI; however, who was also of German aristocratic descent through his mother Mary of Teck, he was given access into the Intelligence organization.
Prince Bernhard was personally screened by British intelligence officer Ian Fleming at the behest of Winston Churchill.
Ian Fleming, who personally knew Bernhard from their war efforts and from luncheons in the Lincoln's Inn Hotel in London, based some features of his fictional character James Bond on Bernhard.
Prince Bernhard then lowered himself 20 feet to the lowest bit of staircase standing, and then said staunchly and with a mixture of Dutch/British flair, as nothing happened: "Most enjoyable evening!"
Bernhard's favorite drink during his meeting with Ian Fleming was a vodka martini shaken, not stirred.
Bernhard's favorite car in London was a Bentley 4.5 litre, the same car Bond had in Fleming's first books.
Bernhard also had a close relationship with the Americans during the war, that continued after the war in his work as chairman of the Bilderberg conference.
Bernhard also became acquainted with Ambassador Joseph Kennedy due to his role as a liaison between Europe and the US, connection to intelligence, multinationals and European royalty.
"For Bernhard, the Prince of the Netherlands, the war was a frustrating business.
Born a German, he had married Queen Wilhelmina's only child, Princess Juliana, and in due time made a conscious and meaningful transition of loyalties to his new homeland.
On 25 June 1940, three days after France fell to the German war machine, Bernhard spoke on the Overseas Service of the BBC.
In 1940, Flight Lieutenant Murray Payne gave the prince instruction in flying a Spitfire.
The prince made 1,000 flight-hours in a Spitfire with the RAF's No. 322 (Dutch) Squadron RAF, wrecking two planes during landings.
In 1941, Prince Bernhard was given the honorary rank of wing commander in the Royal Air Force.
As "Wing Commander Gibbs (RAF)", Prince Bernhard flew over occupied Europe, attacking V-1 launch pads in a B-24 Liberator, bombing Pisa, and engaging submarines over the Atlantic in a B-25 Mitchell, and conducting reconnaissance over enemy-held territory in an L-5 Grasshopper.
Prince Bernhard was awarded the Dutch Airman's Cross for his "ability and perseverance" (Dutch: "bekwaamheid en volharding").
He also helped organise the Dutch resistance movement and acted as the personal secretary for Queen Wilhelmina.
Queen Wilhelmina erased the style "honorary" (the exact words were "à la suite") in the decree promoting Bernhard to General.
In this unconstitutional manner, she gave this Royal Prince a status that was never intended by either Parliament or her Ministers.
The Minister of Defence did not choose to correct the Monarch, and the Prince took an active and important role in the Dutch armed forces.
By 1944, Prince Bernhard became Commander of the Dutch Armed Forces.
After the liberation of the Netherlands, he returned with his family and became active in the negotiations for the German surrender.
He was present during the Armistice negotiations and German surrender at Hotel de Wereld                                                 ("The World Hotel"), Wageningen in The Netherlands on 5 May 1945, where he avoided speaking German.
The Prince was a genuine war hero in the eyes of most of the Dutch; he kept cordial relations with the Communists who fought against the Nazis.
In the post-war years, he earned respect for his work in helping to reinvigorate the economy of the Netherlands.
Postwar roles

After the War, the position of Inspector General was created for the Prince.
On 4 September 1948, his mother-in-law Queen Wilhelmina abdicated the throne and Juliana became Queen of the Netherlands with Bernhard becoming prince consort.
There have been claims that KLM helped Nazis to leave Germany for Argentina on KLM flights while Bernhard was on its board.
After a 1952 trip with Queen Juliana to the United States, Prince Bernhard was heralded by the media as a business ambassador extraordinaire for the Netherlands.
Bilderberg

In the early 1951 Polish diplomat, Józef Retinger contacted Prince Berhard with the idea to create an international conference between European and US greatest influencers to create a better relationship between Europe and the United States.
After this Bernhard contacted Walter Bedell Smith, director of the CIA and old war friend to help him get things started in the US.
Finally in May 1954 Bernhard was organizer and chairman of the first Bilderberg and essential in organising a meeting at the Bilderberg Hotel in the Netherlands for the business elite and intellectuals of the Western World to discuss the economic problems in the face of what they characterised as the growing threat from Communism.
Prince Bernhard was a very outspoken person who often flouted protocol by remarking upon subjects about which he felt deeply.
Almost until his last day, he called for more recognition for the Polish veterans of the Second World War, who had figured greatly in the liberation of the Netherlands but it was not until after his death that the Dutch Government publicly recognised the important role of the Polish Army in the liberation, when on 31 May 2006, at the Binnenhof in The Hague, Queen Beatrix conferred the Military William Order, the highest Dutch military decoration, on the Polish 1st
First president of the World Wildlife Fund

Prince Bernhard helped found the WWF and was the first president of the WWF from its founding year 1961 until 1976.
Friendships, jetset and international connections

Prince Bernhard was seen as a jet-setting and charismatic ambassador for the Dutch during post-war reconstruction.
Prince Bernhard reportedly maintained friendships with several high-profile international figures.
Scandals and rumours

BS militia

The Binnenlandse Strijdkrachten (BS, Domestic Armed Forces) militia, set up and under command of Prince Bernhard towards the end of World War II, gained a notorious reputation for unruly and out-of-control behavior including incidents of pillaging and plundering at the time the country was being liberated from Nazi occupation.
Prince Bernhard was appointed commander of this militia in early September 1944 by Queen Wilhelmina, who had unified several Dutch resistance groups into the BS.
However, under Bernhard's leadership, the militia proved difficult to control and was marred by controversy due to its disorderly conduct and failure to reign in misbehavior among its ranks.
The armistice agreement on May 4, 1945, included the condition that only Allied units would directly carry out the disarming of German troops in the Netherlands.
However, Prince Bernhard's BS militia on the ground disregarded their orders and arrested two German soldiers nearby Dam square.
In the mid-1950s, Queen Juliana and Prince Bernhard's marriage faced significant strain because of the ongoing influence of Greet Hofmans, a faith healer and layer-on of hands.
For nine years she acted as a confidante and adviser to Queen Juliana, often residing at Palace Soestdijk.
Originally, Hofmans was introduced to Queen Juliana at the initiative of Prince Bernhard in 1948 to treat an eye illness of their youngest daughter, Princess Christina (then still called Marijke).
This illness arose because Juliana was infected with rubella during pregnancy.
While the Dutch press did not report widely on the issue, outside the Netherlands, a great deal was written about the Hofmans affair.
Later, Bernhard admitted that he had personally provided the information for the article.
Historian Cees Fasseur drew from it for his book, Juliana & Bernhard (2008); in addition, the Queen had granted him access to the private royal archive.
He noted that Bernhard was reprimanded in 1956 for having leaked confidential information to the international press.
Fasseur said that Bernhard resorted to bringing in the international press only after repeated, desperate and often dramatic pleading with his wife to distance herself from the Hofmans group.
"

Lockheed scandal

Scandal rocked the royal family in 1976 when the press reported that Prince Bernhard had accepted a US$1.1 million bribe from U.S. aircraft manufacturer Lockheed Corporation to influence the Dutch government's purchase of fighter aircraft.
At the time he had served on more than 300 corporate boards and committees worldwide and had been praised in the Netherlands for his efforts to promote the economic well-being of the country.
Prime Minister of the Netherlands Joop den Uyl ordered an inquiry into the Lockheed affair.
Prince Bernhard refused to answer reporters' questions, stating: "I am above such things".
They also brought up records of Prince Bernhard's Reiter SS membership and details of his numerous extramarital affairs.
Bernhard had an older illegitimate daughter, Alicia, born in the United States (with a German pilot whom he met in Mexico in 1951).
On 26 August 1976, a full report of Prince Bernhard's activities was released to a shocked Dutch public.
The Prince's own letter of 1974, to Lockheed Corporation, was publicised; he had demanded "commissions" be paid to him on Dutch government aircraft purchases.
Out of respect for Queen Juliana, the government did not press charges against Bernhard.
Prince Bernhard resigned as Inspector-General of the Dutch Armed Forces.
Prime Minister Joop den Uyl made a statement in Parliament and told the delegates that the Prince would also resign from his various high-profile positions in businesses, charities, and other institutions.
Prince Bernhard turned over the Presidency of the international World Wildlife Fund to Prince Philip, Duke of Edinburgh.
In an interview published after his death, on 14 December 2004, Prince Bernhard admitted that he had accepted more than one million dollars (US) in bribes from Lockheed.
In February 2008, Joop den Uyl's biography claimed that the official report investigating the Lockheed bribe scandal also presented proof that the Prince had accepted money from yet another aerospace firm:
Project Lock

In 1988, Prince Bernhard and Princess Juliana sold two paintings from their personal collection to raise money for the World Wildlife Fund.
In 1989, however, Charles de Haes, Director-General of the WWF, transferred £500,000 back to Bernhard, for what De Haes called a private project.
In 1991, newspapers reported that WWF was acting as a front for an operation involving people of military and intelligence background and under the leadership or coordination of Prince Bernhard, who had hired KAS International or KAS Enterprises, a private contractor owned by Special Air Service founder Sir David Stirling, to use mercenaries – mostly British – to ostensibly fight poachers in nature reserves.
Prince Bernhard was never accused of any crime in this context, but the Project Lock scandal negatively impacted the Prince's reputation.
Additional controversies and rumours

Prince Bernhard garnered media attention when, on 30 October 2002, he paid the fines of two Albert Heijn supermarket staff members, who were convicted of assaulting a shoplifter after they detained him.
High Stakes at the Court of His Royal Highness by historian Harry Veenendaal and journalist Jort Kelder alleges that the Prince in 1950 attempted to oust the young government of the newly founded Republic of Indonesia and place himself to lead the islands as viceroy similar to Lord Mountbatten's role in British India.
This was particularly contentious as in 1949 the Netherlands had already officially recognised its former colony as an independent nation.
A 2016 biography by Jolande Withuis about Queen Juliana, titled Juliana, posited further rumours including that Bernhard had once sexually assaulted a minor, that he had refused to divorce the queen twice, and that later on during their final years in life he prohibited Juliana from seeing him.
Later life and death

In 1994, the Prince had a colon tumour removed and suffered severe complications due to respiratory distress.
In December, his daughter Queen Beatrix rushed to the hospital straight after landing from a trip to Africa.
Two days after intensive medical attention the Royal Press Office issued a statement the Prince was reading newspapers again.
Over the following years Bernhard continued to appear at the military parades on the national liberation day celebrating the defeat of Nazi Germany.
Only when Juliana died in March 2004 did Bernhard become exceedingly fragile.
Bernhard died of lung cancer at the age of 93 at University Medical Center Utrecht in Utrecht on 1 December 2004.
Bernhard's funeral was different from those of Prince Claus and Queen Juliana in that Bernhard's coffin was transported on the undercarriage of a cannon instead of in the traditional carriage used when the coffins of Prince Claus and Queen Juliana were transported to Delft.
Together with the playing of many military marches and the forming of guards of honour by Second World War veterans this gave the funeral procession a military character as the late Prince, a Second World War veteran, had wished.
As a final tribute to his former military role in the Royal Netherlands Air Force, three modern F-16 jet fighters and a World War II Spitfire plane performed a low flypast during the funeral in a classic missing man formation.
In popular culture

In the years after Bernhard died his life story has been the inspiration for literature, theatre, television and comic books.
In 2010 fact and fiction of the life of Bernhard was portrayed in a Dutch television series.
In a biographical dissertation by Dutch journalist and historian Annejet van der Zijl published in March 2010, Bernhard was called "a failure" in the history of the Dutch royal family and a "creature of his own myths".
Titles, styles and honours

Titles

Honours

National honours

Foreign honours

Military ranks

Netherlands

Discharged from all military functions in September 1976


Honorary foreign ranks




Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (fb8a7ab0-6bdf-4e03-a542-8e312a215322)
 Call ID: fb8a7ab0-6bdf-4e03-a542-8e312a215322
  Args:
    source: :Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (9172c50e-33f1-4ebf-bc18-481f99de71c6)
 Call ID: 9172c50e-33f1-4ebf-bc18-481f99de71c6
  Args:
    type: :Person
    source: :Bernhard_of_Lippe-Biesterfeld
  AddLiteral (b225f48e-0d5e-4582-87ab-7d63f4b1ce9a)
 Call ID: b225f48e-0d5e-4582-87ab-7d63f4b1ce9a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Bernhard_of_Lippe-Biesterfeld
    literal_value: 1911
  AddLiteral (60d2cf12-7448-491b-81f9-9c8115bf6441)
 Call ID: 60d2cf12-7448-491b-81f9-9c8115bf6441
  Args:
    relation: :hasDeathYear
    source: :Bernhard_of_Lippe-Biesterfeld
    literal_type: xsd:integer
    literal_value: 2004
  AssignClass (cd79b621-6c9c-4699-af74-30c61b0c4219)
 Call ID: cd79b621-6c9c-4699-af74-30c61b0c4219
  Args:
    type: :Woman
    source: :Juliana_of_the_Netherlands
  AssignClass (1481329d-8690-4504-accb-1af51520aae4)
 Call ID: 1481329d-8690-4504-accb-1af51520aae4
  Args:
    type: :Person
    source: :Juliana_of_the_Netherlands
  AddLiteral (5286e5c4-97a3-4a5f-815b-61b46463f51b)
 Call ID: 5286e5c4-97a3-4a5f-815b-61b46463f51b
  Args:
    source: :Bernhard_of_Lippe-Biesterfeld
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1937
  AddTriple (2e0b6d9b-035b-4f8d-9c63-9a13a8c33bdc)
 Call ID: 2e0b6d9b-035b-4f8d-9c63-9a13a8c33bdc
  Args:
    relation: :hasRelation
    source: :Bernhard_of_Lippe-Biesterfeld
    target: :Juliana_of_the_Netherlands
  AssignClass (c26dc5c8-28f7-4d5a-ba10-42b1df5f1faf)
 Call ID: c26dc5c8-28f7-4d5a-ba10-42b1df5f1faf
  Args:
    type: :Woman
    source: :Beatrix_of_the_Netherlands
  AssignClass (e3538256-3a82-4320-94c2-607d4a5b9cef)
 Call ID: e3538256-3a82-4320-94c2-607d4a5b9cef
  Args:
    type: :Person
    source: :Beatrix_of_the_Netherlands
  AddTriple (3e2624a6-2f09-4eb0-aba5-873aa1fcee7e)
 Call ID: 3e2624a6-2f09-4eb0-aba5-873aa1fcee7e
  Args:
    relation: :isDaughterOf
    source: :Beatrix_of_the_Netherlands
    target: :Bernhard_of_Lippe-Biesterfeld
  AddTriple (0042ebf5-1e74-4f20-ba8b-f96d038c8c6d)
 Call ID: 0042ebf5-1e74-4f20-ba8b-f96d038c8c6d
  Args:
    target: :Juliana_of_the_Netherlands
    relation: :isDaughterOf
    source: :Beatrix_of_the_Netherlands
  AssignClass (c81ca6b1-08f8-4280-8fe8-4f0cd0c14e7b)
 Call ID: c81ca6b1-08f8-4280-8fe8-4f0cd0c14e7b
  Args:
    source: :Irene_of_the_Netherlands
    type: :Woman
  AssignClass (9245efe2-15c2-44ca-8c66-1973939242a3)
 Call ID: 9245efe2-15c2-44ca-8c66-1973939242a3
  Args:
    source: :Irene_of_the_Netherlands
    type: :Person
  AddTriple (63bf1196-5913-435d-8c70-c7d3cf14110d)
 Call ID: 63bf1196-5913-435d-8c70-c7d3cf14110d
  Args:
    relation: :isDaughterOf
    source: :Irene_of_the_Netherlands
    target: :Bernhard_of_Lippe-Biesterfeld
  AddTriple (cc738247-c8e8-4d79-b1cc-a674287cd0ea)
 Call ID: cc738247-c8e8-4d79-b1cc-a674287cd0ea
  Args:
    relation: :isDaughterOf
    source: :Irene_of_the_Netherlands
    target: :Juliana_of_the_Netherlands
  AssignClass (2d9bede1-5cdb-4ab2-8add-aeb1e4d4ceb8)
 Call ID: 2d9bede1-5cdb-4ab2-8add-aeb1e4d4ceb8
  Args:
    type: :Woman
    source: :Margriet_of_the_Netherlands
  AssignClass (e5c20ee5-fc84-4360-9846-baf67e11914e)
 Call ID: e5c20ee5-fc84-4360-9846-baf67e11914e
  Args:
    type: :Person
    source: :Margriet_of_the_Netherlands
  AddTriple (d0624389-c21f-4de2-bce5-19c610a760b8)
 Call ID: d0624389-c21f-4de2-bce5-19c610a760b8
  Args:
    relation: :isDaughterOf
    source: :Margriet_of_the_Netherlands
    target: :Bernhard_of_Lippe-Biesterfeld
  AddTriple (24eedcf6-b5aa-42ac-8ac2-bed14cdf3e8b)
 Call ID: 24eedcf6-b5aa-42ac-8ac2-bed14cdf3e8b
  Args:
    target: :Juliana_of_the_Netherlands
    source: :Margriet_of_the_Netherlands
    relation: :isDaughterOf
  AssignClass (c6ba83bd-4b78-4cd9-a8af-aaceee71896e)
 Call ID: c6ba83bd-4b78-4cd9-a8af-aaceee71896e
  Args:
    source: :Christina_of_the_Netherlands
    type: :Woman
  AssignClass (c9f4e3bb-90d7-4195-9661-71897d6c017a)
 Call ID: c9f4e3bb-90d7-4195-9661-71897d6c017a
  Args:
    source: :Christina_of_the_Netherlands
    type: :Person
  AddTriple (c3dfb0b2-78ea-4029-bbc3-824e1fa6cf9e)
 Call ID: c3dfb0b2-78ea-4029-bbc3-824e1fa6cf9e
  Args:
    relation: :isDaughterOf
    source: :Christina_of_the_Netherlands
    target: :Bernhard_of_Lippe-Biesterfeld
  AddTriple (74e10f83-8018-4230-bdd6-9d37c0f89d31)
 Call ID: 74e10f83-8018-4230-bdd6-9d37c0f89d31
  Args:
    source: :Christina_of_the_Netherlands
    relation: :isDaughterOf
    target: :Juliana_of_the_Netherlands
  AssignClass (df4119bc-4a0e-497a-9fe3-22ac8b0185a1)
 Call ID: df4119bc-4a0e-497a-9fe3-22ac8b0185a1
  Args:
    type: :Man
    source: :Prince_Bernhard_of_Lippe
  AssignClass (3a05a476-0eaf-4c8a-83e1-0a248723768a)
 Call ID: 3a05a476-0eaf-4c8a-83e1-0a248723768a
  Args:
    source: :Prince_Bernhard_of_Lippe
    type: :Person
  AssignClass (cba791d2-d049-4f16-b4ce-e61a263f099b)
 Call ID: cba791d2-d049-4f16-b4ce-e61a263f099b
  Args:
    type: :Woman
    source: :Baroness_Armgard_von_Sierstorpff-Cramm
  AssignClass (1cd55b20-bf9d-4a81-9295-f54db8b61d3c)
 Call ID: 1cd55b20-bf9d-4a81-9295-f54db8b61d3c
  Args:
    source: :Baroness_Armgard_von_Sierstorpff-Cramm
    type: :Person
  AddTriple (48004f7a-5ac7-4249-a7b4-65566f171eb4)
 Call ID: 48004f7a-5ac7-4249-a7b4-65566f171eb4
  Args:
    relation: :hasFather
    source: :Bernhard_of_Lippe-Biesterfeld
    target: :Prince_Bernhard_of_Lippe
  AddTriple (ce32d2ec-654e-4b42-bcc6-83d4c78e70ef)
 Call ID: ce32d2ec-654e-4b42-bcc6-83d4c78e70ef
  Args:
    target: :Baroness_Armgard_von_Sierstorpff-Cramm
    relation: :hasMother
    source: :Bernhard_of_Lippe-Biesterfeld
  AssignClass (7957da38-15fc-4a49-a75f-e0ede7aae40b)
 Call ID: 7957da38-15fc-4a49-a75f-e0ede7aae40b
  Args:
    type: :Man
    source: :Leopold_IV_Prince_of_Lippe
  AssignClass (6dba26e6-5145-4f73-a8b1-4a0c258d0d9f)
 Call ID: 6dba26e6-5145-4f73-a8b1-4a0c258d0d9f
  Args:
    type: :Person
    source: :Leopold_IV_Prince_of_Lippe
  Finish (95775af3-cb63-450d-a170-9a8084a7f76f)
 Call ID: 95775af3-cb63-450d-a170-9a8084a7f76f
  Args: