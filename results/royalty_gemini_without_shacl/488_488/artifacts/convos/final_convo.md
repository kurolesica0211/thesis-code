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
Michael I (Romanian: Mihai I .mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Romanian:  i; 25 October 1921 – 5 December 2017) was the last king of Romania, reigning from 20 July 1927 to 8 June 1930 and again from 6 September 1940 until his forced abdication on 30 December 1947.
Shortly after Michael's birth, his father, Crown Prince Carol, had become involved in a controversial relationship with Magda Lupescu.
In 1925, Carol was pressured to renounce his rights (in favour of his son Michael) to the throne and moved to Paris in exile with Lupescu.
In July 1927, following the death of his grandfather Ferdinand I, Michael ascended the throne at age five, the youngest crowned head in Europe.
As Michael was still a minor, a regency council was instituted, composed of his uncle Prince Nicolas, Patriarch Miron Cristea and Chief Justice Gheorghe Buzdugan.
The council proved to be ineffective and, in 1930, Carol returned to Romania and replaced his son as monarch, reigning as Carol II.
As a result, Michael returned to being heir apparent to the throne and was given the additional title of Grand Voievod of Alba-Iulia.
Carol II was forced to abdicate in 1940, and Michael once again became king.
Under the government led by the military dictator Ion Antonescu, Romania became aligned with Nazi Germany.
In 1944, Michael participated in a coup against Antonescu, appointed Constantin Sănătescu as his replacement, and subsequently declared an alliance with the Allies.
In March 1945, political pressures forced Michael to appoint a pro-Soviet government headed by Petru Groza.
From August 1945 to January 1946, Michael went on a "royal strike" and unsuccessfully tried to oppose Groza's communist-controlled government by refusing to sign and endorse its decrees.
In November 1947, Michael attended the wedding of his cousins, the future Queen Elizabeth II of the United Kingdom and Prince Philip of Greece and Denmark in London.
Shortly thereafter, on the morning of 30 December 1947, Groza met with Michael and compelled him to abdicate, while the monarchy was abolished.
Michael was forced into exile, his properties confiscated, and his citizenship stripped.
In 1948, he married Princess Anne of Bourbon-Parma, with whom he had five daughters.
Nicolae Ceaușescu's communist dictatorship was overthrown in December 1989, and the following year Michael attempted to return to Romania, only to be arrested and forced to leave upon arrival.
In 1992, Michael was allowed to visit Romania for Easter, where he was greeted by huge crowds; a speech he gave from his hotel window drew an estimated one million people to Bucharest.
Alarmed by Michael's popularity, the post-communist government of Ion Iliescu refused to allow him any further visits.
In 1997, after Iliescu's defeat by Emil Constantinescu in the presidential election of the previous year, Michael's citizenship was restored and he was allowed to visit Romania again.
Early life

Michael was born in 1921 at Foișor Castle on the Royal Complex of Peleș in Sinaia, Romania, the son of Crown Prince Carol of Romania and Crown Princess Elena.
He was born as the paternal grandson of the then reigning King Ferdinand I of Romania and maternal grandson of the then reigning King Constantine I of Greece.
Michael's parents had married on 10 March 1921, and he was thus born just seven months after the wedding.
When Carol eloped with his mistress Elena Magda Lupescu and renounced his rights to the throne in December 1925, Michael was declared heir apparent.
Michael succeeded to the throne of Romania upon Ferdinand's death in July 1927, before his sixth birthday.
Later, Michael attended a special school established in 1932 by his father.
Reign

1930s and the Antonescu era

A regency, which included his uncle, Prince Nicolae, Patriarch Miron Cristea, and the country's Chief Justice (Gheorghe Buzdugan, and from October 1929, Constantin Sărăţeanu) functioned on behalf of the five-year-old Michael, when he succeeded Ferdinand in 1927.
In 1930, Carol II returned to the country at the invitation of politicians dissatisfied with the regency in the context of the Great Depression, and was proclaimed king by the Parliament.
Michael was demoted to crown prince with the title "Grand Voivode of Alba Iulia".
In November 1939, Michael joined the Romanian Senate, as the 1938 Constitution guaranteed him a seat there upon reaching the age of eighteen.
Just days after the Second Vienna Award, the pro-Nazi anti-Soviet regime of Prime Minister Marshal Ion Antonescu staged a coup d'état against Carol II, whom he claimed to be "anti-German".
Antonescu suspended the Constitution, dissolved the Parliament, and re-installed the 18-year-old Michael as king, by popular acclaim in September 1940.
(Although the Constitution was restored in 1944, and the Romanian Parliament in 1946, Michael did not subsequently take a formal oath nor have his reign approved retroactively by Parliament.)
Michael was crowned with the Steel Crown and anointed King of Romania by the Orthodox Patriarch of Romania, Nicodim Munteanu, in the Patriarchal Cathedral of Bucharest, on the day of his accession, 6 September 1940.
Although King Michael was formally the Supreme Head of the Army, named Conducător ("Leader of the people"), and entitled to appoint the Prime Minister with full powers, in reality he was forced to remain a figurehead for most of the war, until August 1944.
Michael had lunch with Adolf Hitler twice—once with his father in Bavaria in 1937, and with his mother in Berlin in 1941.
Turning against Nazi Germany

In 1944, World War II was going badly for the Axis powers, but Antonescu was still in control of Romania.
By August 1944, the Soviet conquest of Romania had become inevitable, and was expected in a few months.
On 23 August 1944, Michael joined the pro-Allies politicians, a number of army officers, and armed Communist-led civilians in staging a coup against Antonescu.
Michael ordered his arrest by the Royal Palace Guard.
On the same night, the new Prime Minister, Lt. General Constantin Sănătescu—appointed by King Michael—gave custody of Antonescu to the communists (in spite of alleged instructions to the contrary by the King), and the latter delivered him to the Soviets on 1 September.
In a radio broadcast to the Romanian nation and army, Michael issued a ceasefire just as the Red Army was penetrating the Moldavian front, proclaimed Romania's loyalty to the Allies, announced the acceptance of the armistice offered by the United Kingdom, the United States, and the Soviet Union, and declared war on Germany.
Although the country's alliance with Nazi Germany was ended, the coup sped the Red Army's advance into Romania.
Under the terms of the armistice, Romania recognized its defeat by the USSR and was placed under occupation of the Allied forces, with the Soviets, as their representative, in control of media, communication, post, and civil administration behind the front.
At the end of the war, King Michael was awarded the highest degree (Chief Commander) of the American Legion of Merit by U.S. President Harry S. Truman.
He was also decorated with the Soviet Order of Victory by Joseph Stalin "for the courageous act of the radical change in Romania's politics towards a break-up from Hitler's Germany and an alliance with the United Nations, at the moment when there was no clear sign yet of Germany's defeat", according to the official description of the decoration.
With the death of Michał Rola-Żymierski in 1989, Michael became the sole surviving recipient of the Order of Victory.
Reign under Communism

In March 1945, political pressures forced King Michael to appoint a pro-Soviet government headed by Petru Groza.
For the next two-plus years, Michael functioned again as little more than a figurehead.
Between August 1945 and January 1946, during what was later known as the "royal strike", King Michael tried unsuccessfully to oppose the Groza government by refusing to sign its decrees.
In response to Soviet, British, and American pressures, King Michael eventually gave up his opposition to the communist government and stopped demanding its resignation.
He did not pardon Mareșal Antonescu, the former Prime Minister, who was sentenced to death "for betrayal of the Romanian people for the benefit of Nazi Germany, for the economic and political subjugation of Romania to Germany, for cooperation with the Iron Guard, for murdering his political opponents, for the mass murder of civilians and crimes against peace".
Nor did King Michael manage to save such leaders of the opposition as Iuliu Maniu and the Bratianus, victims of Communist political trials, as the Constitution prevented him from doing so without the counter-signature of Communist Justice Minister Lucrețiu Pătrășcanu (who himself was later eliminated by Gheorghiu-Dej's opposing Communist faction).
The memoirs of King Michael's aunt Princess Ileana quoted Emil Bodnăraș—her alleged lover, Romania's Communist minister of defence, and a Soviet spy—as saying: "Well, if the King decides not to sign the death warrant, I promise that we will uphold his point of view."
Princess Ileana was sceptical: "You know quite well (...) that the King will never of his free will sign such an unconstitutional document.
Surely you do not wish this additional handicap at this moment!"


Forced abdication

In November 1947, King Michael travelled to London for the wedding of his cousins, Princess Elizabeth (later Queen Elizabeth II) and Prince Philip of Greece and Denmark, an occasion during which he met Princess Anne of Bourbon-Parma (his second cousin once removed), who was to become his wife.
According to his own account, King Michael rejected any offers of asylum and decided to return to Romania, contrary to the confidential, strong advice of the British Ambassador to Romania.
Early on the morning of 30 December 1947, Michael was preparing for a New Year's party at Peleș Castle in Sinaia, when Groza summoned him back to Bucharest.
Michael returned to Elisabeta Palace in Bucharest, to find it surrounded by troops from the Tudor Vladimirescu Division, an army unit completely loyal to the Communists.
Unable to call in loyal troops, due to his telephone lines allegedly being cut, Michael signed the document.
On 3 January 1948, Michael was forced to leave the country, followed over a week later by Princesses Elisabeth and Ileana, who collaborated so closely with the Soviets that they became known as the King's "Red Aunts".
Michael's own account of the abdication varied over time, and was gradually embellished, especially after 1990.
Thus, in accounts published in 1950 and 1977, Michael only mentioned seeing armed groups with machine-guns on their shoulders around the palace, while in much later accounts these were described as "heavy artillery, ready to fire at any moment".
The story of the supposed blackmail also evolved: in the 1950 account, Groza tried to negotiate some form of material compensations for the abdication, noting he could not guarantee for Michael's life in case he refused, and his refusal could lead to thousand of arrests and possibly a civil war; in a hearing before the United States House of Representatives in 1954, Michael mentioned Groza's generic threats regarding his personal security, bloodshed and ruin of the country, as well as "vague hints" of persecution, with Groza suggesting the government had a large dossier on Michael; the possible arrest of thousands and a generic threat of bloodshed is also mentioned in the 1977 account; however, beginning with 1990, Michael claimed that Groza threatened to shoot 1,000 students that had already been arrested for publicly showing their attachment to the throne.
Thus, while according to a Time article published in 1948, Groza threatened to arrest thousands of people and order a bloodbath unless Michael abdicated, in an interview with The New York Times from 2007, Michael recounted: "It was blackmail.
Another new element in Michael's account after 1990 was that Groza had threatened him at gunpoint; in earlier accounts Michael mentioned that Groza had shown him the pistol he was carrying only after Michael signed the abdication.
According to the autobiography of the former head of the Soviet intelligence agency NKVD, Major General Pavel Sudoplatov, the Deputy Soviet Foreign Commissar Andrey Vyshinsky personally conducted negotiations with King Michael for his abdication, guaranteeing part of a pension to be paid to Michael in Mexico.
According to a few articles in Jurnalul Național, Michael's abdication was negotiated with the Communist government, which allowed him to leave the country with the goods he requested, accompanied by some of the royal retinue.
According to Albanian Communist leader Enver Hoxha's account of his conversations with the Romanian Communist leaders on the monarch's abdication, it was Gheorghiu-Dej, not Groza, who forced Michael's abdication at gunpoint.
In March 1948, Michael denounced his abdication as illegal, and contended he was still the rightful King of Romania.
According to Time magazine, he would have done so sooner, but for much of early 1948, he had been negotiating with the Communists over properties he had left in Romania.
There are reports that Romanian Communist authorities allowed King Michael to depart with 42 valuable Crown-owned paintings in November 1947, so that he would leave Romania faster.
One of the paintings belonging to the Romanian Crown, which was supposedly taken out of the country by King Michael in November 1947, returned to Romania in 2004 as a donation made by John Kreuger, the former husband of King Michael's daughter Irina.
In 2005, Romanian Prime Minister Călin Popescu-Tăriceanu denied these accusations about King Michael, stating that the Romanian government has no proof of any such action by King Michael and that, prior to 1949, the government had no official records of any artwork taken over from the former royal residences.
According to Ivor Porter's authorized biography, Michael of Romania: The King and The Country (2005), which quotes Queen Mother Helen's daily diary, the Romanian royal family took out paintings belonging to the Romanian Royal Crown, on their November 1947 trip to London to the wedding of the future Queen Elizabeth II; two of these paintings, signed by El Greco, were sold in 1976.
According to declassified Foreign Office documents that were the subject of news reports in 2005, when he left Romania, the exiled King Michael's only assets amounted to 500,000 Swiss francs.
Recently declassified Soviet transcripts of talks between Joseph Stalin and the Romanian Prime Minister Petru Groza show that shortly before his abdication, King Michael received from the communist government assets amounting to 500,000 Swiss francs.
King Michael, however, repeatedly denied that the Communist government had allowed him to take into exile any financial assets or valuable goods besides four personal automobiles loaded on two train cars.
Marriage

Engagement

In November 1947, Michael I met a distant relative, Princess Anne of Bourbon-Parma, who was visiting London for the wedding of Princess Elizabeth and Philip Mountbatten, Duke of Edinburgh.
A year before this, Queen Helen, the Queen Mother, had invited Princess Margaret of Bourbon-Parma and her children, who included Anne, to make a visit to Bucharest, but the plan did not come off.
Meanwhile, King Michael I had glimpsed Princess Anne in a newsreel and requested a photograph from the film footage.
She did not want to accompany her parents to London for the royal wedding as she wished to avoid meeting Michael I in official surroundings.
Upon arrival in London, she stopped by Claridge's to see her parents, and found herself being introduced unexpectedly to King Michael I. Abashed to the point of confusion, she clicked her heels instead of curtseying, and fled in embarrassment.
Charmed, the king saw her again the night of the wedding at the Luxembourg embassy soirée, confided in her some of his concerns about the Communist takeover of Romania and fears for his mother's safety, and nicknamed her Nan.
A few days later, she accepted an invitation to accompany Michael and his mother when he piloted a Beechcraft aeroplane to take his aunt Princess Irene, Duchess of Aosta, back home to Lausanne.
Sixteen days after meeting, Michael proposed to Anne while the couple were out on a drive in Lausanne.
Although Michael gave her an engagement ring a few days later, he felt obliged to refrain from a public announcement until he informed his government, despite the fact that the press besieged them in anticipation.
Michael I returned to Romania, where he was told by the prime minister that a wedding announcement was not "opportune".
Yet within days it was used as the government's public explanation for Michael's sudden "abdication", when in fact the king was deposed by the Communists on 30 December.
Princess Anne was unable to get further news of King Michael
Wedding

As a Bourbon, Anne was bound by the canon law of the Roman Catholic Church, which required that she receive a dispensation to marry a non-Catholic Christian (King Michael I was Orthodox).
Michael refused to make this promise since it would have violated Romania's monarchical constitution, and would be likely to have a detrimental impact upon any possible restoration.
The Holy See (which handled the matter directly since King Michael I was a member of a reigning dynasty) refused to grant the dispensation unless Michael made the required promise.
Helen, Queen Mother of Romania and her sister Princess Irene, Duchess of Aosta (an Orthodox married to a Catholic Prince) met with the fiancée's parents in Paris, where the two families resolved to take their case to the Vatican in person.
In early March, the couple's mothers met with Pope Pius XII who, despite the entreaties of the Queen Mother and the fact that Anne's mother, Princess Margrethe pounded her fist on the table in anger, refused permission for Anne to marry King Michael I.


It has been surmised that the Pope's refusal was, in part, motivated by the fact that when Princess Giovanna of Savoy married Anne's cousin, King Boris III of Bulgaria, in 1930, the couple had undertaken to raise their future children as Roman Catholics, but had baptized them in the Orthodox faith in deference to Bulgaria's state religion.
However, King Michael I declined to make a promise he could not keep politically, while Anne's mother was herself the daughter of a mixed marriage between a Catholic (Princess Marie d'Orléans) and a Protestant (Prince Valdemar of Denmark), who had abided by their pre-ne temere compromise to raise their sons as Protestant and their daughter, Margrethe, as Catholic.
Anne's paternal uncle, Prince Xavier of Bourbon-Parma, issued a statement objecting to any marriage conducted against the will of the Pope and the bride's family.
It was he, not the Pontiff, who forbade Anne's parents to attend the wedding.
King Michael I's spokesman declared on 9 June that the parents had been asked and had given their consent, and that the bride's family would be represented at the nuptials by her maternal uncle, the Protestant Prince Erik of Denmark, who was to give the bride away.
The wedding ceremony was held on 10 June 1948 in Athens, Greece, in the throne room of the Royal Palace; the ceremony was performed by Archbishop Damaskinos, and King Paul I of Greece served as koumbaros.
Guests at the wedding included: Michael's mother The Queen Mother of Romania, aunts Queen Frederica, The Dowager Duchess of Aosta, Lady Katherine Brandram; cousins Prince Amedeo, 5th Duke of Aosta, Princess Sophia of Greece and Denmark, Crown Prince Constantine of Greece and Princess Irene of Greece and Denmark, the three youngest ones serving as bridesmaids and pageboy; Anne's maternal uncle Prince Erik of Denmark; Grand Duchess Elena Vladimirovna of Russia, Princess Olga of Greece and Denmark, Princess Elizabeth of Yugoslavia, Prince George Wilhelm of Hanover and many other dignitaries.
King Michael I's father, Carol, and his sisters, Maria, Queen Mother of Yugoslavia, Princess Elisabeth of Romania (ex-Queen Consort of Greece) and Princess Ileana of Romania were notified, but not invited.
Family

Michael and Anne had five daughters:


Life in exile

Michael would never see his father again, after Carol II's 1940 abdication.
Michael could see no point in meeting his father who had humiliated his mother so many times via his open affairs and did not attend his father's funeral in 1953.
In January 1948, Michael began using one of his family's ancestral titles, "Prince of Hohenzollern", instead of using the title of "King of Romania".
After denouncing his abdication as forced and illegal in March 1948, Michael resumed use of the kingly title.
Michael and Princess Anne lived near Florence, Italy, until 1948, near Lausanne, Switzerland, until 1950, and then in Hertfordshire, England, until 1956.
The Communist Romanian authorities stripped Michael of his Romanian citizenship in 1948.
During exile, Michael had a variety of occupations including farming, stockbroker, entrepreneur, and pilot.
Together with his wife, he took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Return and rehabilitation

On 25 December 1990—a year after the revolution which overthrew the dictatorship of Nicolae Ceaușescu—Michael, accompanied by several members of the royal family, landed at Otopeni Airport and entered Romania for the first time in 43 years.
Using a Danish diplomatic passport, Michael was able to obtain a 24-hour visa.
In 1992, the Romanian government allowed Michael to return to Romania for Easter celebrations, where he drew large crowds.
Michael refused the offer of the president of the National Liberal Party, Radu Câmpeanu, to run for elections as president of Romania.
Michael's popularity alarmed the government of President Ion Iliescu, and he was forbidden to re-visit Romania, being denied entry twice in 1994 and 1995.
In 1997, after Iliescu's defeat by Emil Constantinescu, the Romanian government restored Michael's citizenship and again allowed him to visit the country.
He then lived partly in Switzerland at Aubonne and partly in Romania, either at Săvârșin Castle in Arad County or in an official residence in Bucharest—the Elisabeta Palace—voted by the Romanian Parliament by a law concerning arrangements for former heads of state.
Later years

Michael neither encouraged nor opposed monarchist agitation in Romania and royalist parties have made little impact in post-communist Romanian politics.
He took the view that the restoration of the monarchy in Romania can only result from a decision by the Romanian people.
King Michael's belief was that there is still a role for, and value in, the monarchy today: "We are trying to make people understand what the Romanian monarchy was, and what it can still do .
Michael himself, however, was shown to be much more popular personally with the Romanian people: In a July 2013 survey, 45% of Romanians had a good or very good opinion of Michael, with 6.5% thinking the opposite.
Michael undertook some quasi-diplomatic roles on behalf of post-communist Romania.
In 1997 and 2002 he toured Western Europe, lobbying for Romania's admission into NATO and the European Union, and was received by heads of state and government officials.
In December 2003, to the "stupefaction of the public opinion in Romania",   Michael awarded the "Man of The Year 2003" prize to Prime Minister Adrian Năstase, leader of the Social Democratic Party (PSD), on behalf of the tabloid VIP.
The daily Evenimentul Zilei subsequently complained that 'such an activity was unsuited to a king and that Michael was wasting away his prestige', with the majority of the political analysts 'considering his gesture as a fresh abdication'.
On 10 May 2007, King Michael received the Prague Society for International Cooperation and Global Panel Foundation 's 6th Annual Hanno R. Ellenbogen Citizenship Award, previously awarded to Vladimir Ashkenazy, Madeleine Albright, Václav Havel, Lord Robertson, and Miloš Forman.
On 8 April 2008, King Michael and Patriarch Daniel were elected as honorary members of the Romanian Academy.
Michael participated in the Victory Parade in Moscow in 2010 as the only living Supreme Commander-in-Chief of a European State in the Second World War.
The name of Michael I is listed on the memorial in the Grand Kremlin Palace as one of only 20 recipients of the Order of Victory.
In old age, Michael enjoyed a strong revival in popularity.
An opinion poll in January 2012 placed him as the most trusted public figure in Romania, far ahead of the political leaders.
Later, in October 2012, celebrating Michael's 91st birthday, a square in Bucharest was renamed after him.
On 1 August 2016, he became a widower when Queen Anne died at the age of 92.
Health issues

On 2 March 2016, the Royal Council announced King Michael's retirement from public life; with tasks assumed by Crown Princess Margareta, his daughter.
After surgery, Michael was diagnosed with chronic leukemia and metastatic epidermoid carcinoma and faced a complex and lengthy treatment.
King Michael is quiet, has soulful appreciation and appreciates the care of his medical team.
"


At the end of August 2017, the Royal House announced that King Michael was "in a fragile but balanced state, and has a good mood," stating that Princess Elena had completed a visit to Switzerland for a few days to see her father, at the private residence.
According to the Royal House, Michael remained "daily under close supervision of physicians, medical staff of various specialties, and in the presence of devoted members of the staff of His Majesty's House, stationed in Switzerland."
Death and state funeral

On 5 December 2017, Michael died at his residence in Switzerland at the age of 96, in the presence of his youngest daughter Princess Maria.
His coffin, draped by his Royal Standard, was brought back to Romania on 13 December, arriving at the Otopeni Airport in Bucharest from Lausanne, via Payerne Air Base, escorted by his second daughter, Princess Elena with her husband Alexander Nixon, fourth daughter Sophie and also members of the Royal Household, were transported by the Romanian Air Force's Alenia C-27J Spartan transport aircraft, which was flanked by four Mikoyan-Gurevich MiG-21 jet fighters.
King Michael I was buried on 16 December with full state honours in the Mausoleum of the Royal Family, on the grounds of the Curtea de Argeș Cathedral together with his wife Queen Anne who died in 2016.
His funeral is stated to have been one of the largest in Romania, with almost a million Romanians flocking to the capital to pay their respects and watch the funeral, with it being comparable to the one of Corneliu Coposu in 1995.
According to the succession provisions of the Romanian kingdom's last democratically approved monarchical constitution of 1923, upon the death of King Michael without sons, the claim to the Crown devolves once again upon the Hohenzollern family.
However, on 30 December 2007, on the 60th anniversary of his abdication, King Michael signed the Fundamental Rules of the Royal Family of Romania, by which he designated Princess Margareta as his heir.
On 10 May 2011, on a background of lawsuits in Germany brought against his family by Michael's German relatives regarding the former name Hohenzollern-Veringen of his son-in-law, Radu, and of fears expressed by some that the German Hohenzollerns may claim succession to the headship of the Romanian royal house, Michael severed all of the dynastic and historical ties with the princely house of Hohenzollern, changed the name of his family to "of Romania", and gave up all princely titles conferred upon him and his family by the German Hohenzollerns.
On 1 August 2015, Michael signed a document removing the title Prince of Romania and the qualification of Royal Highness from his grandson, Nicholas Medforth-Mills, who was also removed from the line of succession.
The former king took the decision "with an eye on Romania's future after the reign and life of his eldest daughter, Margareta".
Nicholas's mother, Princess Elena, received notification of the former king's decision in a personal letter.
Personality and personal interests

Aged 16, when Michael was crown prince, he hit a bicyclist while driving a car, causing the cyclist's death.
Michael was head of the Romanian Boy Scouts in the 1930s.
Shortly after the Second World War, Michael became interested in Moral Rearmament, which was introduced to him by his first cousin Prince Richard of Hesse-Cassel, and as Swiss residents after 1956 he and Queen Anne paid numerous visits to the MRA conference centre of Caux, where he found solace for the loss of his country and his émigré status as well as new hope for future reconciliation.
Arms, honours and awards

Honours

Awards

National awards

Foreign awards

Military ranks

Honorific eponyms

Statues and monuments

On 25 October 2012, a large monument to Michael including a large bronze bust was unveiled at King Michael I Square in Bucharest.
Michael attended and unveiled the statue.
On 25 October 2021, a statue of Michael was unveiled in the town of Sinaia, on the occasion of the centenary of his birth.
Minister of Culture Bogdan Gheorghiu was in attendance, along with Margareta of Romania, other government representatives, and members of parliament.



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
  AssignClass (d9292558-6410-4c9b-b117-b34e06e1caa9)
 Call ID: d9292558-6410-4c9b-b117-b34e06e1caa9
  Args:
    source: :Michael_I
    type: :Man
  AssignClass (fc6b9107-ce05-4943-92bf-6c2533a644e8)
 Call ID: fc6b9107-ce05-4943-92bf-6c2533a644e8
  Args:
    source: :Michael_I
    type: :Person
  AssignClass (34e3e462-1aa3-4161-9899-80e772f26dbb)
 Call ID: 34e3e462-1aa3-4161-9899-80e772f26dbb
  Args:
    type: :Ancestor
    source: :Michael_I
  AddLiteral (042923af-8f03-4cfd-8604-f609f9f9d60c)
 Call ID: 042923af-8f03-4cfd-8604-f609f9f9d60c
  Args:
    source: :Michael_I
    literal_value: 1921
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (6594db6f-0120-4b41-bbb0-5de9b57a0b66)
 Call ID: 6594db6f-0120-4b41-bbb0-5de9b57a0b66
  Args:
    literal_value: 2017
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Michael_I
  AssignClass (a5de5f4b-2203-4240-901e-9d7936d73d87)
 Call ID: a5de5f4b-2203-4240-901e-9d7936d73d87
  Args:
    type: :Man
    source: :Carol_II
  AssignClass (e92fe33c-79b2-4ba6-bc69-7ef2f635923b)
 Call ID: e92fe33c-79b2-4ba6-bc69-7ef2f635923b
  Args:
    source: :Carol_II
    type: :Person
  AssignClass (f1121018-980b-4898-8eb3-c88b1d933afa)
 Call ID: f1121018-980b-4898-8eb3-c88b1d933afa
  Args:
    source: :Carol_II
    type: :Ancestor
  AddTriple (c011ee73-a126-4c62-8efa-cab5ece554f7)
 Call ID: c011ee73-a126-4c62-8efa-cab5ece554f7
  Args:
    source: :Michael_I
    relation: :hasFather
    target: :Carol_II
  AssignClass (c8df7fd0-cb4f-44cc-b645-5f2a09711e1e)
 Call ID: c8df7fd0-cb4f-44cc-b645-5f2a09711e1e
  Args:
    type: :Woman
    source: :Elena_of_Romania
  AssignClass (d6207f63-6a03-4efb-8e46-dde2a42e7c3a)
 Call ID: d6207f63-6a03-4efb-8e46-dde2a42e7c3a
  Args:
    source: :Elena_of_Romania
    type: :Person
  AssignClass (ced6d0ca-4e84-4de3-9119-d88eb1b80eeb)
 Call ID: ced6d0ca-4e84-4de3-9119-d88eb1b80eeb
  Args:
    type: :Ancestor
    source: :Elena_of_Romania
  AddTriple (1b9568ac-7412-429a-952b-0b69f00c6283)
 Call ID: 1b9568ac-7412-429a-952b-0b69f00c6283
  Args:
    source: :Michael_I
    relation: :hasMother
    target: :Elena_of_Romania
  AddLiteral (2e70ddb2-2902-4f95-917a-c366fe840b20)
 Call ID: 2e70ddb2-2902-4f95-917a-c366fe840b20
  Args:
    literal_value: 1921
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Carol_II
  AddTriple (d0374cfa-2a8c-4b31-ad8e-d81c4172229f)
 Call ID: d0374cfa-2a8c-4b31-ad8e-d81c4172229f
  Args:
    relation: :hasRelation
    target: :Elena_of_Romania
    source: :Carol_II
  AssignClass (129bc3e0-e64b-4dd3-9a85-8acb278b387b)
 Call ID: 129bc3e0-e64b-4dd3-9a85-8acb278b387b
  Args:
    source: :Ferdinand_I
    type: :Man
  AssignClass (678451b8-cf5c-4c2d-b7b2-481503890581)
 Call ID: 678451b8-cf5c-4c2d-b7b2-481503890581
  Args:
    type: :Person
    source: :Ferdinand_I
  AssignClass (d1571387-9600-4c52-b19d-fd2907a6e933)
 Call ID: d1571387-9600-4c52-b19d-fd2907a6e933
  Args:
    type: :Ancestor
    source: :Ferdinand_I
  AddTriple (14cc58c5-8220-4fa3-919b-70b908422c57)
 Call ID: 14cc58c5-8220-4fa3-919b-70b908422c57
  Args:
    relation: :hasFather
    target: :Ferdinand_I
    source: :Carol_II
  AssignClass (739843e3-43b4-4d50-b18b-ccdb095fe420)
 Call ID: 739843e3-43b4-4d50-b18b-ccdb095fe420
  Args:
    source: :Constantine_I_of_Greece
    type: :Man
  AssignClass (1e2d241b-4ace-4d7b-88b1-6feaed2e8b21)
 Call ID: 1e2d241b-4ace-4d7b-88b1-6feaed2e8b21
  Args:
    type: :Person
    source: :Constantine_I_of_Greece
  AssignClass (c838b2c6-917c-4e58-b317-fb2c1b2d5570)
 Call ID: c838b2c6-917c-4e58-b317-fb2c1b2d5570
  Args:
    type: :Ancestor
    source: :Constantine_I_of_Greece
  AddTriple (c7b95915-90d5-497b-a00e-e5fcba763d07)
 Call ID: c7b95915-90d5-497b-a00e-e5fcba763d07
  Args:
    source: :Elena_of_Romania
    relation: :hasFather
    target: :Constantine_I_of_Greece
  AssignClass (e5cdcf71-c111-4471-b263-0a5a6f6f1686)
 Call ID: e5cdcf71-c111-4471-b263-0a5a6f6f1686
  Args:
    type: :Woman
    source: :Anne_of_Bourbon-Parma
  AssignClass (91412eb6-6263-400e-a76d-9de9d23ec4cf)
 Call ID: 91412eb6-6263-400e-a76d-9de9d23ec4cf
  Args:
    source: :Anne_of_Bourbon-Parma
    type: :Person
  AddLiteral (8b1ef6a1-0066-4c9f-b4b1-db8fd51cf307)
 Call ID: 8b1ef6a1-0066-4c9f-b4b1-db8fd51cf307
  Args:
    literal_value: 1948
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Michael_I
  AddTriple (f438c12a-f89e-4d34-8587-9db8b6bac901)
 Call ID: f438c12a-f89e-4d34-8587-9db8b6bac901
  Args:
    source: :Michael_I
    relation: :hasRelation
    target: :Anne_of_Bourbon-Parma
  AssignClass (19c40653-98bb-4e90-be57-ec7691cbeee6)
 Call ID: 19c40653-98bb-4e90-be57-ec7691cbeee6
  Args:
    type: :Woman
    source: :Princess_Maria
  AssignClass (51ac1616-983c-4860-85e7-93fbcc9acfc1)
 Call ID: 51ac1616-983c-4860-85e7-93fbcc9acfc1
  Args:
    source: :Princess_Maria
    type: :Person
  AddTriple (1b85c817-2366-41ed-a9b2-82ec147f9fb4)
 Call ID: 1b85c817-2366-41ed-a9b2-82ec147f9fb4
  Args:
    source: :Princess_Maria
    target: :Michael_I
    relation: :isDaughterOf
  AddTriple (cbdc31b5-dad5-4807-ae77-401b0b378582)
 Call ID: cbdc31b5-dad5-4807-ae77-401b0b378582
  Args:
    relation: :isDaughterOf
    target: :Anne_of_Bourbon-Parma
    source: :Princess_Maria
  AssignClass (13c80363-3f01-478c-a953-7f66bbbee80a)
 Call ID: 13c80363-3f01-478c-a953-7f66bbbee80a
  Args:
    type: :Woman
    source: :Princess_Elena
  AssignClass (242c0273-57c7-4955-a7d4-274fab86f304)
 Call ID: 242c0273-57c7-4955-a7d4-274fab86f304
  Args:
    type: :Person
    source: :Princess_Elena
  AddTriple (e2033174-ff7b-42b5-baca-ae0181d7cff8)
 Call ID: e2033174-ff7b-42b5-baca-ae0181d7cff8
  Args:
    source: :Princess_Elena
    target: :Michael_I
    relation: :isDaughterOf
  AddTriple (d7519477-3208-4b25-b4d6-5092d3be1164)
 Call ID: d7519477-3208-4b25-b4d6-5092d3be1164
  Args:
    relation: :isDaughterOf
    target: :Anne_of_Bourbon-Parma
    source: :Princess_Elena
  AssignClass (225da5b6-3032-4f53-8721-101465ae03ce)
 Call ID: 225da5b6-3032-4f53-8721-101465ae03ce
  Args:
    source: :Princess_Sophie
    type: :Woman
  AssignClass (b8777e5e-eb5a-4c40-8b56-b6a0ee7a6430)
 Call ID: b8777e5e-eb5a-4c40-8b56-b6a0ee7a6430
  Args:
    type: :Person
    source: :Princess_Sophie
  AddTriple (5258b229-8afd-477b-8a2b-0456ecad6994)
 Call ID: 5258b229-8afd-477b-8a2b-0456ecad6994
  Args:
    relation: :isDaughterOf
    target: :Michael_I
    source: :Princess_Sophie
  AddTriple (b2f78805-a4a5-4e92-a3ed-eb2d1d5db90c)
 Call ID: b2f78805-a4a5-4e92-a3ed-eb2d1d5db90c
  Args:
    source: :Princess_Sophie
    target: :Anne_of_Bourbon-Parma
    relation: :isDaughterOf
  AssignClass (74bfc8bc-e4b1-4659-a782-a5607bb4e1a2)
 Call ID: 74bfc8bc-e4b1-4659-a782-a5607bb4e1a2
  Args:
    source: :Princess_Irina
    type: :Woman
  AssignClass (dca9c6fd-e00d-4c76-b09e-72706f9dab06)
 Call ID: dca9c6fd-e00d-4c76-b09e-72706f9dab06
  Args:
    type: :Person
    source: :Princess_Irina
  AddTriple (e61c91eb-6889-4290-bcf5-0ce12b743bb1)
 Call ID: e61c91eb-6889-4290-bcf5-0ce12b743bb1
  Args:
    target: :Michael_I
    relation: :isDaughterOf
    source: :Princess_Irina
  AddTriple (c6805690-82b3-4b7e-8940-a24d584c81cc)
 Call ID: c6805690-82b3-4b7e-8940-a24d584c81cc
  Args:
    source: :Princess_Irina
    relation: :isDaughterOf
    target: :Anne_of_Bourbon-Parma
  AssignClass (92648807-1db1-4555-9a5b-67b07c243a4a)
 Call ID: 92648807-1db1-4555-9a5b-67b07c243a4a
  Args:
    type: :Woman
    source: :Princess_Margareta
  AssignClass (0ea8f174-63fd-4421-b59d-9ca9f1f734df)
 Call ID: 0ea8f174-63fd-4421-b59d-9ca9f1f734df
  Args:
    source: :Princess_Margareta
    type: :Person
  AddTriple (e6288304-648d-4c45-960e-cb67eb241f16)
 Call ID: e6288304-648d-4c45-960e-cb67eb241f16
  Args:
    target: :Michael_I
    relation: :isDaughterOf
    source: :Princess_Margareta
  AddTriple (3b7569e6-9b4e-4673-8795-66d4e8c493e5)
 Call ID: 3b7569e6-9b4e-4673-8795-66d4e8c493e5
  Args:
    relation: :isDaughterOf
    target: :Anne_of_Bourbon-Parma
    source: :Princess_Margareta
  Finish (6ac6fa3b-4a82-4ebb-a241-09fd2eab5e1a)
 Call ID: 6ac6fa3b-4a82-4ebb-a241-09fd2eab5e1a
  Args: