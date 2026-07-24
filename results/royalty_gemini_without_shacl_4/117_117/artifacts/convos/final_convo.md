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


Juan Carlos I (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Spanish: ; Juan Carlos Alfonso Víctor María de Borbón y Borbón-Dos Sicilias; born 5 January 1938) is a member of the Spanish royal family who reigned as King of Spain from 22 November 1975 until his abdication on 19 June 2014.
In Spain, since his abdication, Juan Carlos has usually been referred to as the rey emérito ('king emeritus') by the press.
Juan Carlos is the son of Infante Juan, Count of Barcelona, and grandson of Alfonso XIII, the last king of Spain before the abolition of the monarchy in 1931 and the subsequent declaration of the Second Spanish Republic.
Juan Carlos was born in Rome, Italy, during his family's exile.
General Francisco Franco took over the government of Spain after his victory in the Spanish Civil War in 1939, yet in 1947 Spain's status as a monarchy was affirmed and a law was passed allowing Franco to choose his successor.
Juan Carlos's father assumed his claims to the throne after King Alfonso XIII died in February 1941.
However, Franco saw Juan Carlos's father to be too liberal and in 1969 declared Juan Carlos his successor as head of state.
Juan Carlos spent his early years in Italy and came to Spain in 1947 to continue his studies.
In 1962, Juan Carlos married Princess Sophia of Greece and Denmark in Athens.
Due to Franco's advanced age and declining health amid his struggle with Parkinson's disease, Juan Carlos first began periodically acting as Spain's head of state in the summer of 1974.
In November the following year, Franco died and Juan Carlos became king.
Juan Carlos was expected to continue Franco's legacy, but instead introduced reforms to dismantle the Francoist regime and to begin the Spanish transition to democracy soon after his accession.
In 1981, Juan Carlos played a major role in preventing a coup that attempted to revert to Francoist government in the King's name.
Hailed for his role in Spain's transition to democracy, the King and the monarchy's reputation began to suffer after controversies surrounding his family arose, exacerbated by the public controversy centering on an elephant-hunting trip he undertook during a time of financial crisis in Spain.
In June 2014, Juan Carlos abdicated in favour of his son, who acceded to the throne as Felipe VI.
Since August 2020, Juan Carlos has lived in self-imposed exile from Spain over allegedly improper ties to business deals in Saudi Arabia.
The New York Times estimated in 2014 that Juan Carlos's fortune was around €1.8 billion ($2.3 billion).
Early life

Juan Carlos was born on 5 January 1938 to Infante Juan, Count of Barcelona, and Princess María de las Mercedes of Bourbon-Two Sicilies in their family home in Rome, where his grandfather King Alfonso XIII and other members of the Spanish royal family lived in exile following the proclamation of the Second Spanish Republic in 1931.
He was baptised as Juan Carlos Alfonso Víctor María de Borbón y Borbón-Dos Sicilias by Cardinal Eugenio Pacelli, the future Pope Pius XII.
Juan Carlos's early life was dictated largely by the political concerns of his father and General Francisco Franco.
He moved to Spain in 1948 to be educated there after his father persuaded Franco to allow it.
Juan Carlos had two sisters: Infanta Pilar, Duchess of Badajoz (1936–2020); and Infanta Margarita, Duchess of Soria (born 1939).
He also had a younger brother, Alfonso (1941–1956).
The rendering of his name as "Juan Carlos" (the first and second particles of his baptismal name) was a modification by choice of Franco.
He was always known in his familiar circle simply as "Juan" or "Juanito".
Together with his parents and his sister Pilar, he took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On this trip, Juan Carlos met the hosts' 15-year-old daughter, Sofia, his future wife, for the first time.
Brother's death

On the evening of Holy Thursday, 29 March 1956, Infante Alfonso died in a gun accident at the family's home Villa Giralda in Estoril, on the Portuguese Riviera.
Whilst His Highness Prince Alfonso was cleaning a revolver last evening with his brother, a shot was fired hitting his forehead and killing him in a few minutes.
The accident took place at 20.30 hours, after the Infante's return from the Maundy Thursday religious service, during which he had received holy communion.
Alfonso had won a local junior golf tournament earlier in the day, then went to evening Mass and rushed up to the room to see Juan Carlos who had come home for the Easter holidays from military school.
Both Juan Carlos, age 18, and Alfonso, age 14, had been apparently playing with a .22LR Star Bonifacio Echeverria Automatic pistol owned by Alfonso.
As they were alone in the room, it is unclear how Alfonso was shot, but according to Josefina Carolo, dressmaker to Juan Carlos's mother, Juan Carlos pointed the pistol at Alfonso and pulled the trigger, unaware that it was loaded.
Bernardo Arnoso, a Portuguese friend of Juan Carlos, also said that Juan Carlos had told him he had fired the pistol not knowing that it was loaded, and adding that the bullet ricocheted off a wall, hitting Alfonso in the face.
Helena Matheopoulos, a Greek author who spoke with the infantes' sister Pilar, said that Alfonso had been out of the room and when he returned and pushed the door open, the door knocked Juan Carlos in the arm, causing him to fire the pistol.
After learning this news, the Count of Barcelona reportedly grabbed Juan Carlos by the neck and shouted at him angrily, "Swear to me that you didn't do it on purpose!"
Two days later, the Count sent his son back to the military academy.
Following a later declaration of Juan Carlos's mother, Paul Preston argues that the content of the former testimony implies that Juan Carlos had pointed the gun at Alfonso, apparently not knowing that the gun was loaded, and pulled the trigger.
Juan Carlos himself did not refer to the incident firsthand until he published his memoirs in 2025.
Juan Carlos acknowledged that it was "difficult" for him to speak about the shooting, but added that he "thought about it every day".
Education

In 1957, Juan Carlos spent a year in the naval school at Marín, Pontevedra, and another in the Air Force school in San Javier in Murcia.
Prince of Spain

The dictatorial regime of Francisco Franco came to power during the Spanish Civil War, which pitted a government of democrats, anarchists, socialists, and communists, supported by the Soviet Union and international volunteers, against a rebellion of conservatives, monarchists, nationalists, and fascists, supported by both Hitler and Mussolini, with the rebels ultimately winning.
Franco's authoritarian government remained dominant in Spain until the 1960s.
At the time, the heir to the throne of Spain was Infante Juan, Count of Barcelona, the son of King Alfonso XIII.
Juan Carlos's first cousin Alfonso, Duke of Anjou and Cádiz, was also briefly considered as a candidate.
Alfonso was known to be an ardent Francoist and married Franco's granddaughter, Doña María del Carmen Martínez-Bordiú y Franco, in 1972.
Ultimately, Franco decided to skip a generation and name Infante Juan Carlos as his personal successor.
In 1969, Juan Carlos was officially designated heir apparent and was given the new title of Prince of Spain (not the traditional Prince of Asturias).
Juan Carlos met and consulted Franco many times while heir apparent and often took part in official and ceremonial state functions, standing alongside the dictator, much to the anger of hardline republicans and more moderate liberals, who hoped that Franco's death would bring in an era of reform.
During 1969–1975, Juan Carlos publicly supported Franco's regime.
Although Franco's health worsened during those years, whenever he did appear in public, from state dinners to military parades, it was in Juan Carlos's company.
However, as the years progressed, Juan Carlos began meeting secretly with political opposition leaders and exiles, who were fighting to bring liberal reform to the country.
Franco, for his part, remained largely oblivious to the prince's actions and denied allegations from his ministers and advisors that Juan Carlos was in any way disloyal to his vision of the regime.
During periods of Franco's temporary incapacity in 1974 and 1975, Juan Carlos was acting head of state.
On 30 October 1975, Franco gave full control to Juan Carlos.
According to declassified CIA reports, during this time Juan Carlos secretly acquiesced and arranged with King Hassan II of Morocco the terms of the so-called Green March, the partial invasion of the Spanish Sahara by Moroccan civilians, followed by the Madrid Accords handing over the control of the territory to Morocco and Mauritania.
Reign

Franco died on 20 November 1975, and two days later on 22 November the Cortes Españolas proclaimed Juan Carlos King of Spain.
In his address to the Cortes, Juan Carlos spoke of three factors: historical tradition, national laws, and the will of the people, and in so doing referred to a process dating back to the Civil War of 1936–39.
He opted not to call himself Juan III or Carlos V, but Juan Carlos I. Juan Carlos is reported to have been pressured by Valéry Giscard d'Estaing to personally tell Chilean dictator Augusto Pinochet, who had traveled to Spain for Franco's funeral, not to attend his inauguration.
In the end Pinochet did participate of the proclamation at the Palacio de las Cortes, Madrid but not in the follow-up Te Deum.
In private Pinochet expressed later his disapproval of what he saw as a lack of recognition of Franco by Juan Carlos I in his speech at the Cortes.
Transition

Juan Carlos's accession met with relatively little parliamentary opposition.
Juan Carlos quickly instituted reforms, to the great displeasure of Falangist and conservative (monarchist) elements, especially in the military, who had expected him to maintain the authoritarian state.
In July 1976, Juan Carlos dismissed prime minister Carlos Arias Navarro, who had been attempting to continue Francoist policies in the face of the King's attempts at democratization.
Further legitimacy was restored to Juan Carlos's position on 14 May 1977, when his father (whom many monarchists had recognized as the legitimate, exiled King of Spain during the Franco era) formally renounced his claim to the throne and recognized his son as the sole head of the Spanish Royal House, transferring to him the historical heritage of the Spanish monarchy, thus making Juan Carlos both de facto and de jure king in the eyes of the traditional monarchists.
On 20 May 1977, the leader of the only recently legalized Spanish Socialist Workers' Party (PSOE), Felipe González, accompanied by Javier Solana, visited Juan Carlos in the Zarzuela Palace.
The event represented a key endorsement of the monarchy from Spain's political left, who had been historically republican.
Left-wing support for the monarchy had grown when the Communist Party of Spain was legalized on 9 April 1977, a move Juan Carlos had pressed for, despite enormous right-wing military opposition at that time, during the Cold War.
On 15 June 1977, Spain held its first post-Franco democratic elections.
Juan Carlos had played a role as middleman in order to channel $10 million from the Shah of Iran to Adolfo Suárez's election campaign, reportedly asking the Shah for the money to "save Spain from Marxism".
In 1978, the government promulgated a new constitution that acknowledged Juan Carlos as rightful heir of the Spanish dynasty and king; specifically, Title II, Section 57 asserted Juan Carlos's right to the throne of Spain by dynastic succession in the Bourbon tradition, as "the legitimate heir of the historic dynasty" rather than as the designated successor of Franco.
When Juan Carlos became king, Communist leader Santiago Carrillo had nicknamed him Juan Carlos the Brief, predicting that the monarchy would soon be swept away with the other remnants of the Franco era.
Above all, Juan Carlos and the main political parties were aware of a plan to put General Alfonso Armada in charge of the government, particularly in order to crack down on the Basque independence organization Euskadi ta Askatasuna (ETA).
Although Juan Carlos strongly condemned the coup attempt — more than six hours after the armed guards invaded Congress — it is still difficult to establish whether he acted out of democratic conviction or because the operation was not going as well as expected, with little support.
Antonio Tejero would later claim that Juan Carlos knew about the coup.
On paper, Juan Carlos retained fairly extensive reserve powers.
As head of the Spanish state, Juan Carlos "held political power, gave his opinion and exerted his influence in the economic sphere, for example, in the area of company mergers or public policy during the transition period," analyses journalist Ana Pardo.
In October 1990, Juan Carlos visited the Chilean city of Valdivia amidst the beginning of the Chilean transition to democracy.
While he and the Queen were cheered by some, groups of indigenous Mapuches approached the King, some to protest past colonialism, and others to have the King ratify past Mapuche-Spanish treaties.
According to El País political infighting between Mapuches prevented Juan Carlos from hosting an official meeting with Mapuche representatives.
In July 2000, Juan Carlos was the target of an enraged protester when former priest Juan María Fernández y Krohn, who had once attacked Pope John Paul II, breached security and attempted to approach the king.
When the media asked Juan Carlos in 2005 whether he would endorse the bill legalising same-sex marriage that was then being debated in the Cortes Generales, he answered "Soy el Rey de España y
no el de Bélgica" ("I am the King of Spain, not of Belgium") – a reference to King Baudouin of Belgium, who had refused to sign the Belgian law legalising abortion.
According to a poll in the newspaper El Mundo in November 2005, 77.5% of Spaniards thought Juan Carlos was "good or very good", 15.4% "not so good", and only 7.1% "bad or very bad".
2007 Ibero-American Summit

In November 2007, at the Ibero-American Summit in Santiago, during a heated exchange, Juan Carlos interrupted Venezuelan President Hugo Chávez, saying, "¿Por qué no te callas?"
Chávez had been interrupting the Spanish Prime Minister, José Luis Rodríguez Zapatero, while the latter was defending his predecessor and political opponent, José María Aznar, after Chávez had referred to Aznar as a fascist and "less human than snakes".
The King shortly afterwards left the hall when President Daniel Ortega of Nicaragua accused Spain of intervention in his country's elections and complained about some Spanish energy companies working in Nicaragua.
Budget of the royal house

Juan Carlos detailed for the first time in 2011 the yearly royal budget of €8.3 million, excluding expenses such as the electricity bill, paid by the State.
Botswana hunting trip

In April 2012, Juan Carlos faced criticism for an elephant-hunting trip in Botswana.
said Juan Carlos should choose between "public responsibilities or an abdication".
In April 2012, Spain's unemployment was at 23% and nearly 50% for young workers.
El País estimated the total cost of a hunting trip at €44,000, about twice the average annual salary in Spain.
In July 2012, WWF Spain held a meeting in Madrid and decided with 226 votes to 13 to remove the King from its honorary presidency.
Up until the Botswana elephant trip, Juan Carlos had enjoyed a high level of shielding from media scrutiny, described as "rare among Western leaders".
Interfaith work

On the 500th anniversary of the Alhambra Decree in 1992, King Juan Carlos I and Queen Sofia visited the Beth Yaacov Synagogue in Madrid, led by Chief Rabbi of Madrid Yehuda Benasouli to commemorate the occasion.
While Sofia had been to the synagogue in the 1970s, the occasion marked the first time that the king had visited a synagogue in Spain.
Also present were descendants of Abraham Senior and Isaac Abarbanel, who had unsuccessfully petitioned King Ferdinand and Queen Isabella to retract the edict.
In 2008, Juan Carlos spoke at the opening of a 3-day Saudi-sponsored World Conference on Dialogue interfaith conference at the Royal Palace of El Pardo outside Madrid.
Abdication

Spanish news media started to speculate about the King's future in 2013, following public criticism over his taking an elephant hunting safari in Botswana and an embezzlement scandal involving his daughter, Infanta Cristina, Duchess of Palma de Mallorca, and her husband Iñaki Urdangarin.
The King reportedly said, "No quiero que mi hijo se marchite esperando como Carlos."
Felipe was enthroned the following morning, and Juan Carlos's granddaughter Leonor became the new Princess of Asturias.
Juan Carlos was the fourth European monarch to abdicate in just over a year, following Pope Benedict XVI (28 February 2013), Queen Beatrix of the Netherlands (30 April 2013), and King Albert II of Belgium (21 July 2013).
However, unlike his previous immunity, the new legislation left him accountable to the supreme court, in a similar type of protection afforded to many high-ranking civil servants and politicians in Spain.
Reactions

The Spanish press gave the announcement a broadly positive reception, but described the moment as an "institutional crisis" and "a very important moment in the history of democratic Spain".
Around Spain and in major cities (including London) the news was met by republican celebration and protests, calling for the end of the monarchy.
Iñigo Urkullu, the President of the Basque government, concluded that the King's reign was "full of light yet also darkness" and said that his successor Felipe should remember that "the Basque Question has not been resolved".
Other regional leaders had more positive evaluations of Juan Carlos following his decision to abdicate: Alberto Núñez Feijóo of Galicia called him "the King of Democracy" who "guaranteed the continuation of constitutional monarchy" and Alberto Fabra of the Valencian Community said that Spaniards are proud of their king who had been "at the forefront of protecting our interests inside and outside of our borders".
British Prime Minister David Cameron stated: "I would like to use this opportunity to make a tribute to King Juan Carlos, who has done so much during his reign to aid the successful Spanish transition to democracy, and has been a great friend of the United Kingdom."
The President of the European Commission, José Manuel Barroso, said that Juan Carlos was a "believer in Europeanism and modernity...without whom one could not understand modern Spain".
Overall, 55.7% of those polled in the 3–5 June survey by Sigma Dos supported the institution of the monarchy in Spain, up from 49.9% when the same question was posed six months prior.
An overwhelming majority of Spaniards believed the new King, Felipe VI, would make a good monarch and more than three-quarters believed King Juan Carlos had been right to hand over the throne to his son.
Post-abdication

After abdication, Juan Carlos continued to have a role as institutional representative of the Crown.
From June 2014 to June 2019, he attended several Latin American presidential inaugurations such as the second inauguration of Juan Manuel Santos as president of Colombia, the inauguration of Tabaré Vázquez as president of Uruguay, and the inauguration of Mauricio Macri as president of Argentina.
On 27 May 2019, King Juan Carlos announced by a letter to his son Felipe his intention to retire from public life on 2 June 2019, five years after he announced his abdication.
Sayn-Wittgenstein claimed that Juan Carlos received kick-backs from commercial contracts in the Gulf States – particularly in the late-2000s construction of the €6.7 billion Haramain high-speed railway in Saudi Arabia – and maintained these proceeds in a bank account in Switzerland.
The allegations drew demands for Juan Carlos to be investigated for corruption in early June 2019.
Swiss authorities began investigating Juan Carlos in March 2020 in relation to a $100 million gift to Sayn-Wittgenstein in 2012.
Sayn-Wittgenstein reportedly told the head Swiss prosecutor on 19 December 2018 that Juan Carlos had given her €65 million out of "gratitude and love", to guarantee her future and her children's, because "he still had hopes to win her back".
A letter written by Juan Carlos to his Swiss lawyers in 2018 stated the gift was irrevocable, despite his having asked in 2014 for the return of the money.
On 14 March 2020, The Telegraph reported that his son Felipe, King of Spain since 2014, appeared as second beneficiary (after Juan Carlos) of the Lucum Foundation, which had received a €65 million donation by King Abdullah of Saudi Arabia.
On 15 March 2020, the Royal Household declared that Felipe VI would renounce any inheritance from his father.
In June 2020, the public prosecutor's office of the Supreme Court of Spain agreed to investigate Juan Carlos's role as facilitator in Phase II of the high speed rail connecting Mecca and Medina, intending to determine the criminal relevance of events that took place after his abdication in June 2014.
As King of Spain, Juan Carlos was immune from prosecution from 1975 to 2014 by sovereign immunity.
Credit cards and bank accounts

Spanish prosecutors opened an investigation into the use by Juan Carlos and other members of the royal family of credit cards used between 2016 and 2018 which were paid for by an overseas account to which neither Juan Carlos nor any member of the royal family were signatories, leading to accusations that the funds are undisclosed assets of Juan Carlos, and as the card drawings exceeded €120,000 in one year, comprised undisclosed income and was therefore a tax offence in Spain.
Mexican millionaire and investment banker Allen Sanginés-Krause has been named as the owner of the cards, a friend of Juan Carlos to whom he donated sums of money using Air Force Colonel Nicolás Murga Mendoza as an intermediary.
In December 2020, Juan Carlos reportedly paid €678,393.72 to Spain's tax agency for the concept of defrauded money in an affair of "opaque credit cards" used between 2016 and 2018 by himself, his wife and some grandchildren, intending to avoid further scrutiny from the Supreme Court's prosecutor, the payment being an admission of fraud.
Swiss and Spanish prosecutors also investigated several accounts related to the former King, such as an account in Switzerland with almost €8 million and an attempt to withdraw nearly €10 million from Jersey, possibly from a trust set up by or for Juan Carlos in the 1990s.
Juan Carlos claims he is "not responsible for any Jersey trust and never has been, either directly or indirectly".
Zagatka Foundation

Founded in Liechtenstein in 2003 and owned by Álvaro de Orleans-Borbón, a distant cousin of Juan Carlos who lives in Monaco, the foundation received a large sum of money from Switzerland; Juan Carlos is named as the third beneficiary.
In 2009 Álvaro de Orleans-Borbón paid a cheque from Mexico for €4.3 million into the account which the Swiss adjudicated belonged to Juan Carlos.
Juan Carlos appears to have drawn down funds from the Zagatka foundation to spend €8 million between 2009 and 2018 on private flights, with Air Partner receiving around €6.1 million.
Zagatka used commissions due to Juan Carlos and paid to Zagatka to invest millions, mainly in Ibex35 companies between 2003 and 2018.
On 25 February 2021, Juan Carlos paid 4 million euros to the Spanish Tax Agency to avoid new tax offenses in relation with these flights.
Lucum foundation

A Panamanian Lucum foundation had Juan Carlos as the first beneficiary and King Felipe VI as a named second beneficiary, although Felipe has subsequently relinquished any inheritance from his father Juan Carlos.
Claims of harassment

In 2020, Sayn-Wittgenstein, resident in the United Kingdom, filed an harassment case in London against Juan Carlos, claiming he had pressured her to return the money given to her after their break up in 2012.
In 2022, Juan Carlos won an appeal that he had immunity from those allegations relating to 2012–2014 when he was still King.
Relocation abroad

On 3 August 2020, the Royal Household announced Juan Carlos wished to relocate from Spain because of increased media press about his business dealings in Saudi Arabia, and he had left a letter to his son saying so.
The Royal Household initially declined requests to publicly disclose Juan Carlos's location; on 17 August, the Royal Household confirmed that, since 3 August, Juan Carlos had been in the United Arab Emirates, where he arrived by taking a private plane from Vigo Airport.
Since then, he has visited Spain regularly, mainly the town of Sanxenxo, in the north of Spain, to do one of his favorite activities, sailing.
In 2025, Juan Carlos published his memoir, titled Reconciliation.
The book was criticized by culture minister Ernest Urtasun as "sickening" for passages in which Juan Carlos wrote of his "great respect" for Francisco Franco and other favorable descriptions of him.
Family and private life

Juan Carlos was married on 14 May 1962, to Princess Sophia of Greece and Denmark, daughter of King Paul of Greece, firstly in a Roman Catholic ceremony at the Church of St. Denis, followed by a Greek Orthodox ceremony at the Metropolitan Cathedral of Athens.
They have three children:


Juan Carlos is also allegedly the father of Albert Solà, born in Barcelona in 1956, also of a woman born in Catalonia in 1964, and of Ingrid Sartiau, a Belgian woman born in 1966 who has filed a paternity suit, but complete sovereign immunity prevented that suit prior to his abdication.
Juan Carlos is alleged to have had several extramarital affairs, which adversely affected his marriage.
In 2021, the former police official José Manuel Villarejo testified that Juan Carlos was given hormones to reduce his sex drive, as it was seen as a state problem.
In 1972, Juan Carlos, a keen sailor, competed in the Dragon class event at the Olympic Games, finishing 15th.
It was alleged by the Russian regional authorities that in August 2006 Juan Carlos shot a drunken tame bear (Mitrofan the Bear) during a private hunting trip to Russia; the Royal Household denied this claim.
He is a member of the World Scout Foundation and of the Sons of the American Revolution.
Health

A benign 17–19 mm tumour was removed under general anaesthetic from King Juan Carlos's right lung in an operation carried out in the Hospital Clínic de Barcelona in May 2010.
The operation followed an annual check-up, and Juan Carlos was not expected to need any further treatment.
In April 2018, Juan Carlos was admitted to hospital for a surgery on his right knee.
In the documentary Yo, Juan Carlos I, rey de España , released in 2015, his sister Infanta Pilar revealed that Juan Carlos I suffers from dyslexia.
In popular culture

Juan Carlos I is portrayed on screen by Fernando Cayo in the Antena 3 mini-series 20-N: los últimos días de Franco  (2008); by Lluís Homar in the Televisión Española mini-series 23-F: El día más difícil del Rey (2009); by Fernando Cayo in the Antena 3 mini-series Adolfo Suárez, el presidente (2010); by Fernando Gil in the Telecinco mini-series Alfonso, el príncipe maldito  (2010); by Juanjo Puigcorbé in the Telecinco mini-series Felipe y Letizia  (2010); by Jorge Suquet  in the Antena 3 mini-series Sofía  (2011); by Fernando Cayo in the film 17 Hours (2011); by Álex Tormo  in the Televisión Española mini-series Tarancón, el quinto mandamiento  (2011); by Enrique Aragonés, Patrick Criado, and Fernando Gil in the Telecinco mini-series El Rey  (2014); by Fernando Andina in the Televisión Española telefilm De la ley a la ley  (2017); by Cristóbal Suárez  in the Atresmedia mini-series Untameable (2023); and by Miki Esparbé in the Movistar Plus+ mini-series The Anatomy of a Moment (2025).
Titles, styles, honours and arms

In 1969, Juan Carlos was named as General Franco's successor and was given the title of 'Prince of Spain'.
Upon the death of Franco in 1975, Juan Carlos acceded to the throne of Spain.
The current Spanish constitution refers to the monarch by the simple title "King of Spain".
Since his abdication in 2014, King Juan Carlos has retained, by courtesy, the title of king and style of "majesty" that he enjoyed during his reign.
Arms

The coat of arms used as Prince of Spain which was virtually identical to the one later adopted when he became King, differed only that it featured the crown of heir to the throne, decorated with only four half-arches.



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
  AssignClass (81a3d090-df3b-4dae-9a1c-c6535cc56b4d)
 Call ID: 81a3d090-df3b-4dae-9a1c-c6535cc56b4d
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (ed83f5f2-3303-41cc-abdb-361efd8b4b9b)
 Call ID: ed83f5f2-3303-41cc-abdb-361efd8b4b9b
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (f5f4e003-36a7-41cd-8257-60e27f302f8c)
 Call ID: f5f4e003-36a7-41cd-8257-60e27f302f8c
  Args:
    type: :Woman
    source: Queen_Sofia
  AssignClass (3b07dea1-f876-412c-ac3b-0a1386278868)
 Call ID: 3b07dea1-f876-412c-ac3b-0a1386278868
  Args:
    type: :Person
    source: Queen_Sofia
  AssignClass (dfdd561a-124c-4253-9e82-2e29d927a5e5)
 Call ID: dfdd561a-124c-4253-9e82-2e29d927a5e5
  Args:
    type: :Man
    source: Infante_Juan_Count_of_Barcelona
  AssignClass (c4b11961-b418-4abd-b29f-69f08e6ad751)
 Call ID: c4b11961-b418-4abd-b29f-69f08e6ad751
  Args:
    type: :Person
    source: Infante_Juan_Count_of_Barcelona
  AssignClass (4fec5f9b-cbd8-4864-8d15-28a63b22e395)
 Call ID: 4fec5f9b-cbd8-4864-8d15-28a63b22e395
  Args:
    type: :Woman
    source: Princess_Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (da0f12b9-7d35-400e-ab5c-a0e81ed4aee9)
 Call ID: da0f12b9-7d35-400e-ab5c-a0e81ed4aee9
  Args:
    type: :Person
    source: Princess_Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (5133fb87-51cd-4c54-a3e0-6b7d394da578)
 Call ID: 5133fb87-51cd-4c54-a3e0-6b7d394da578
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (090bc229-bce8-4567-b3ab-d5fc612ab398)
 Call ID: 090bc229-bce8-4567-b3ab-d5fc612ab398
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (b37427f4-c610-45eb-94f8-bb1dfa33245b)
 Call ID: b37427f4-c610-45eb-94f8-bb1dfa33245b
  Args:
    type: :Woman
    source: Infanta_Pilar_Duchess_of_Badajoz
  AssignClass (62c3250a-fc26-4d8d-9829-a0c76442d79b)
 Call ID: 62c3250a-fc26-4d8d-9829-a0c76442d79b
  Args:
    type: :Person
    source: Infanta_Pilar_Duchess_of_Badajoz
  AssignClass (97417095-b198-4ba4-a6cd-a3e0f9fed831)
 Call ID: 97417095-b198-4ba4-a6cd-a3e0f9fed831
  Args:
    type: :Woman
    source: Infanta_Margarita_Duchess_of_Soria
  AssignClass (8c12c99e-5e24-4f5b-8b49-63ecddbfcd00)
 Call ID: 8c12c99e-5e24-4f5b-8b49-63ecddbfcd00
  Args:
    type: :Person
    source: Infanta_Margarita_Duchess_of_Soria
  AssignClass (104dab95-576f-457f-9010-01382c752deb)
 Call ID: 104dab95-576f-457f-9010-01382c752deb
  Args:
    type: :Man
    source: Alfonso
  AssignClass (3ff1c22e-6377-426f-baff-8281f87d342a)
 Call ID: 3ff1c22e-6377-426f-baff-8281f87d342a
  Args:
    type: :Person
    source: Alfonso
  AssignClass (ffe7adfa-6ba7-4be2-b5ae-d055ac5b675b)
 Call ID: ffe7adfa-6ba7-4be2-b5ae-d055ac5b675b
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (f2f7ba1a-3b7b-4fd8-b29e-963cf8ce7f9f)
 Call ID: f2f7ba1a-3b7b-4fd8-b29e-963cf8ce7f9f
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (07235a1c-f8c1-4fda-9e1d-5b83e7cc5c6a)
 Call ID: 07235a1c-f8c1-4fda-9e1d-5b83e7cc5c6a
  Args:
    type: :Man
    source: King_Paul_of_Greece
  AssignClass (e3550899-6e79-4743-b42f-c02dae6bde3d)
 Call ID: e3550899-6e79-4743-b42f-c02dae6bde3d
  Args:
    type: :Person
    source: King_Paul_of_Greece
  AddLiteral (2458a7d6-9367-4637-9b09-0a99fb057c90)
 Call ID: 2458a7d6-9367-4637-9b09-0a99fb057c90
  Args:
    source: Juan_Carlos_I
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (5b634a4c-7e7d-4b5f-bd15-3e2a9c0133e0)
 Call ID: 5b634a4c-7e7d-4b5f-bd15-3e2a9c0133e0
  Args:
    relation: :hasFather
    target: Infante_Juan_Count_of_Barcelona
    source: Juan_Carlos_I
  AddTriple (ebce5422-aca1-4ac6-972c-ce58c32e5a19)
 Call ID: ebce5422-aca1-4ac6-972c-ce58c32e5a19
  Args:
    source: Juan_Carlos_I
    target: Princess_Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AddTriple (494044c4-beb8-47b5-b204-a00c7c8d7ec0)
 Call ID: 494044c4-beb8-47b5-b204-a00c7c8d7ec0
  Args:
    source: Infante_Juan_Count_of_Barcelona
    target: Alfonso_XIII
    relation: :hasFather
  AddTriple (909ce650-dbd7-4461-9401-f6e201a02663)
 Call ID: 909ce650-dbd7-4461-9401-f6e201a02663
  Args:
    target: Infanta_Pilar_Duchess_of_Badajoz
    relation: :hasSister
    source: Juan_Carlos_I
  AddTriple (515e1666-c855-4eba-860e-aec5f37e79bf)
 Call ID: 515e1666-c855-4eba-860e-aec5f37e79bf
  Args:
    source: Juan_Carlos_I
    target: Infanta_Margarita_Duchess_of_Soria
    relation: :hasSister
  AddTriple (678d1bec-ed31-4e5d-8035-27845518b73d)
 Call ID: 678d1bec-ed31-4e5d-8035-27845518b73d
  Args:
    source: Juan_Carlos_I
    target: Alfonso
    relation: :hasBrother
  AddTriple (9c2a2933-c880-40c2-9df0-660848d4ab3b)
 Call ID: 9c2a2933-c880-40c2-9df0-660848d4ab3b
  Args:
    target: Juan_Carlos_I
    relation: :hasFather
    source: Felipe_VI
  AddTriple (188ad2bd-6391-4031-8e6e-f45fcdb736f0)
 Call ID: 188ad2bd-6391-4031-8e6e-f45fcdb736f0
  Args:
    relation: :hasMother
    target: Queen_Sofia
    source: Felipe_VI
  AddTriple (c9a8394a-79d4-4dd2-b606-6e30273b21aa)
 Call ID: c9a8394a-79d4-4dd2-b606-6e30273b21aa
  Args:
    source: Queen_Sofia
    target: King_Paul_of_Greece
    relation: :hasFather
  AddLiteral (532bfe69-a439-4320-af65-d7db81be2012)
 Call ID: 532bfe69-a439-4320-af65-d7db81be2012
  Args:
    relation: :hasMarriageYear
    literal_value: 1962
    source: Juan_Carlos_I
    literal_type: xsd:integer
  AddTriple (ad525cf3-688c-4d05-8b49-f9e4cac18a78)
 Call ID: ad525cf3-688c-4d05-8b49-f9e4cac18a78
  Args:
    relation: :hasRelation
    target: Queen_Sofia
    source: Juan_Carlos_I
  Finish (e7928c88-a992-48c8-aa3e-820d58ba502d)
 Call ID: e7928c88-a992-48c8-aa3e-820d58ba502d
  Args: