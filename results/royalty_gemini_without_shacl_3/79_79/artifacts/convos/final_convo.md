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
Helen of Greece and Denmark (Greek: Ελένη, romanized: Eléni; Romanian: Elena; 2 May 1896 – 28 November 1982) was the queen mother of Romania during the reign of her son King Michael I (1940–1947).
Daughter of King Constantine I of Greece and his wife, Princess Sophia of Prussia, Helen spent her childhood in Greece, the United Kingdom and Germany.
The outbreak of World War I and the overthrow of her father by the Allies in 1917 permanently marked her and also separated her from her favorite brother, the young Alexander I of Greece.
Exiled in Switzerland along with most members of the royal family, Helen then spent several months caring for her father, plagued by disease and depression.
In 1920, the princess met Carol, Crown Prince of Romania, who quickly asked her hand in marriage.
Despite the bad reputation of the prince, Helen accepted and moved to Romania, where she soon gave birth to their only son, Prince Michael, in 1921.
The situation of her family, however, continued to worry Helen, who made several trips abroad to visit her parents when they did not simply reside with her in Bucharest.
Distraught, Helen tried to persuade her husband to return to her but eventually she accepted the divorce in 1928.
In the meanwhile, Helen was proclaimed "Queen Mother of Romania"  in 1927, as her son Michael ascended to the throne under the regency of his uncle Prince Nicolae.
However, the political situation in Romania was complicated and Carol took advantage of the increased instability to return to Bucharest in 1930 and be acclaimed as king.
In these circumstances, Helen moved to Villa Sparta at Fiesole, Tuscany.
The outbreak of World War II, the deposition of Carol II and the subsequent dismemberment of Greater Romania in 1940, however, brought Helen back to be with her son in Bucharest.
They did not show their opposition to the participation of Romania in the invasion of the Soviet Union and the deportation of Jews.
Finally, King Michael organized a coup against Antonescu on 23 August 1944 and Romania turned against the Axis powers; however, the country was, in the end, occupied by the Red Army.
For Helen and her son, the post-war period was marked by the interference of the Soviet Union in Romanian political life.
Finally, Michael I was forced to abdicate on 30 December 1947 and the royal family took the path of exile.
Increasingly concerned about her finances, Helen finally left Italy for Switzerland in 1979 and died three years later with her son at her side.
Princess of Greece and Denmark

A Greek childhood

The third child and eldest daughter of Crown Prince Constantine of Greece and Princess Sophia of Prussia, Helen was born on 2 May 1896 in Athens during the reign of her grandfather, King George I.  From birth, she received the nickname "Sitta" as her brother Alexander failed to correctly pronounce the English word "sister".
Growing up, Helen developed a special affection for Alexander, only three years her senior.
Helen spent most of her childhood in the Greek capital.
Every summer, the princess and her family travelled to the Hellenic Mediterranean aboard the royal yacht Amphitrite or visited Sophia's mother, the Dowager Empress Victoria in Germany.
From the age of 8, Helen began to spend part of the summer in Great Britain, in the regions of Seaford and Eastbourne.
The princess grew up in a strongly anglophile environment, among a cohort of British tutors and governesses, including Miss Nichols, who took special care of her.
From the Goudi coup to the Balkan Wars

On 28 August 1909 a group of Greek officers, known as the "Military League", organized a coup d'état (called the Goudi coup) against the government of King George I, Helen's grandfather.
But the reality was quite different: the officers blamed Constantine for the defeat of Greece against the Ottoman Empire during the Thirty Days' War of 1897.
The situation was so tense that the sons of George I were finally forced to resign from their military posts to save their father from the shame of their being expelled.
The Diadochos also decided to leave Greece with his wife and children.
It was the first of many times that the 14-year-old Helen would have to go into exile.
After much tension, the political situation eventually subsided in Greece and Constantine and his family were allowed to return to their homeland.
A year later, the First Balkan War broke out, which allowed Greece to annex large territories in Macedonia, Epirus, Crete and the North Aegean.
It was also at the end of this conflict that King George I was assassinated in Thessaloniki on 18 March 1913 and Helen's father succeeded him on the Hellenic throne as King Constantine I.
After these events, Helen spent long weeks touring Greece, of which she previously only knew the main towns and the island of Corfu.
With her father and brother Alexander, she travelled in Greek Macedonia and the various battlefields of the First Balkan War.
Once again, Greece emerged victorious from the conflict, allowing it to significantly expand its territory, which grew by 68% after the signing of the Treaty of Bucharest.
World War I

During World War I, King Constantine I first sought to maintain Greece in a position of neutrality.
But, educated in Germany and linked to Emperor William II (who was his brother-in-law), Constantine I was quickly accused of supporting the Triple Alliance and wishing for the defeat of the Allies.
Central Greece was occupied by the allied forces and the country was soon in the middle of a civil war, the so-called National Schism.
Weakened by all these tensions, Constantine I became seriously ill in 1915.
In Greece, public opinion was affected by the rumor, spread by Venizelists, that the king was not sick but that Queen Sophia in fact injured him in the course of an argument where she tried to force him to fight alongside the emperor.
These events had a special impact on Princess Helen, who was very close to her father: impressed by his recovery, she developed a deep religiosity, a trait that she would retain throughout her life.
Despite these difficulties, Constantine I refused to change his policies and was faced with the increasingly clear opposition of the Triple Entente and Venizelists.
On this occasion, Helen was nearly killed by a gunfire from the Zappeion.
After hearing the gunshots and worried for the life of her father, the princess ran to the gardens of the royal palace but was saved by the royal Garde du Corps which took her back inside the palace.
Finally, on 10 June 1917, Charles Jonnart, the Allied High Commissioner in Greece, asked the king for his abdication.
The Allies did not wish to establish a Republic in Greece, so one of the members of the royal family had to stay and succeed him.
Because the Diadochos George was also considered pro-German like his father, they wanted someone considered malleable, as a puppet ruler of Constantine
Finally the younger brother of the Diadochos, Prince Alexander, was chosen by Venizelos and the Triple Entente as the new king.
In the days that followed, Constantine I, Queen Sophia and five of their children left Greece from the port of Oropos and took the road to exile.
This was the last time that Helen saw her favorite brother.
In fact, on their return to power, the Venizelists prohibited any contact between King Alexander I and the rest of the royal family.
After crossing the Ionian Sea and Italy, Helen and her family settled in Switzerland, mainly among the cities of St. Moritz, Zürich and Lucerne.
In exile, Helen's parents were soon followed by almost all members of the royal family, who left their country with the return of Venizelos as Prime Minister and the entry of Greece to the war alongside the Triple Entente.
However, the financial position of the royal family was precarious and Constantine I, haunted by a deep sense of failure, soon fell ill.
Very concerned about the fate of their father, Helen and her sisters Irene and Katherine spent a long time with him to distract him from his worries.
Helen also sought to reconnect with Alexander I.
However, the officer who escorted the king in the French capital refused to pass along either her communications or those of other members of the royal family (with the exception of his aunt Princess Maria of Greece and Denmark).
Meeting with Crown Prince Carol of Romania

In 1920, the Greek exiles were visited in Lucerne by Queen Marie of Romania (Sophia's first cousin) and her daughters Elisabeth, Maria and Ileana.
Worried about the future of her eldest and still single son, the Diadochos George, who had already proposed to Princess Elisabeth a few years earlier, Queen Sophia was anxious for him to marry.
Homeless, penniless and without any real political value since his exclusion from the Greek throne in 1917, Helen's elder brother reiterated his request of marriage to Princess Elisabeth, who, despite her initial reticence, finally decided to accept.
Pleased with the union, the Queen of Romania then invited her future son-in-law and his sisters Helen and Irene to go to Bucharest in order to publicly announce the royal engagement.
This was Elisabeth's brother, the Crown Prince Carol, who had just completed a trip around the world which he had undertaken in order to forget his morganatic wife Zizi Lambrino and their son Carol.
In Romania George, Helen and Irene were received with pomp by the royal family.
Housed at Pelișor Castle, they were a central part of the celebrations for the return of Crown Prince Carol to his country (10 October) and the announcement of the engagement of Elisabeth with the Diadochos (12 October).
On 24 October, a telegram arrived which announced the death in Zurich of the Dowager Duchess of Saxe-Coburg-Gotha, who was the mother of the queen of Romania.
The very next day, another message arrived informing the Greek princesses that Alexander I had suddenly died in Athens, following a monkey bite.
Under these circumstances, the three Greek princesses and Queen Marie of Romania decided to make an emergency return to Switzerland.
Moved by the situation and probably pushed by his mother, Crown Prince Carol at the last moment decided to travel along with them.
After being cold and distant to Helen during her stay at Romania, the crown prince suddenly turned very attentive to the princess.
During the train journey, the two told their life stories to each other and Carol confided in Helen about his affair with Zizi Lambrino.
Helen likewise told him of her life and of family matters, including her great grief for her brother Alexander's death and how she did not want to return to Greece now that her only real friend, her beloved brother, was dead.
This opening of the hearts to each other had the result that Helen fell in love with the heir to the Romanian throne.
Restoration and marriage

Soon after their arrival in Switzerland, Crown Prince Carol asked for Helen's hand in marriage, much to the joy of the queen of Romania, but not to the princess' parents.
Helen was determined to accept the marriage proposal, therefore King Constantine I assented to the engagement, but only after the marriage of Carol and Zizi Lambrino could be quickly dissolved.
For her part, Queen Sophia was much less favorable to her daughter's wedding.
Having no confidence in the Romanian crown prince, she tried to convince Helen to reject the proposal.
However, Helen insisted, and despite the doubts of her mother, the engagement was announced in Zürich in November 1920.
Meanwhile, in Greece, the Venizelists lost the election in favor of Constantine
Under these conditions, the royal family returned to Athens and Helen was accompanied by her fiancé on her return.
For two months, the two traveled discovering inner Greece and its ancient ruins.
They then went to Bucharest to attend the wedding of Diadochos George with Elisabeth of Romania (27 February 1921) before returning to Athens to celebrate their own wedding in the Metropolitan Cathedral on 10 March 1921.
Being the first Greek princess to marry in Athens, Helen wore the Romanian 'Greek Key' tiara, a gift from her mother-in-law.
The newlyweds then spent their honeymoon in Tatoi, where they remained for two months before returning to Romania, on 8 May 1921.
Crown Princess of Romania

Installation in Bucharest

Upon her return to Romania, Helen was already pregnant.
She spent some time with Carol at the Cotroceni Palace, where the pomp and protocol of the Court both impressed and bored her at the same time.
It was there that the crown princess gave birth after only seven and a half months after her wedding.
Her only child, Prince Michael, named in honor to Michael the Brave, the first unifier of the Danubian Principalities, was born on 25 October 1921; the childbirth was difficult and required surgery.
The ordeal significantly weakened Helen, and the doctors forbade her from having a second pregnancy.
Once Helen had recovered, in December 1921 the couple moved to Bucharest, in a large villa at the Șoseaua Kiseleff.
Despite their significantly different points of interest, Carol and Helen managed, for some time, to lead a bourgeois and happy existence.
The crown princess was very involved in social work and founded a nursing school in the capital.
Reunion with family

In the meantime, the political situation was deteriorating in Greece.
The Hellenic Kingdom endured a period of unrest during the Greco-Turkish War, and by 1919 the health of King Constantine I was deteriorating once again.
Worried about the future of her father, Helen asked for her husband's permission to return to Greece.
But while Carol left Greece in February to attend the betrothal of his sister Maria to King Alexander I of Yugoslavia, Helen remained with her parents until April, when she returned to Romania, bringing her sister Irene.
In June 1922, Carol and Helen went to Belgrade with the whole Romanian royal family to attend the wedding of Alexander I and Maria.
Back in Bucharest, the crown princess then resumed her role as wife of the heir to the throne.
Like many women of her rank, Helen was also interested in social works.
Nevertheless, she continued to be worried for her family, and even visited her sister Irene, her aunt Maria and her Greek cousins in an futile attempt to console herself about the remoteness of her parents.
In September 1922, a military coup forced King Constantine I to abdicate in favor of his son George II, and to go into exile.
Devastated by these events, Helen immediately went to Italy to be with her parents in their exile.
Shortly after the coronation of King Ferdinand I and Queen Marie of Romania in Alba Iulia on 15 October 1922, Helen left for Palermo, where she remained until the death of her father, on 11 January 1923.
Bored by the absence of his wife, Carol finally invited his mother-in-law to stay in Bucharest.
Increasingly irritated by the invasive presence of his wife's family, Carol also was hurt by Helen's attitude because she refused to fulfil her marital duties.
It was due to these circumstances that Helen and Carol began their separation, though the crown princess saved appearances by devoting more time to the education of her son, Prince Michael.
Abandonment of Crown Prince Carol

In the summer of 1924, Carol met Elena Lupescu (better known under the name of "Magda" Lupescu), with whom he began an affair in or around 14 February 1925.
However, for Carol, this time there was a serious bond, a fact that would soon worry not only Helen (always of a conciliatory and tolerant disposition with her husband's infidelities) but also the rest of the Romanian royal family, which feared that Lupescu could turn into a new Zizi Lambrino.
In November 1925, Carol was sent to the United Kingdom to represent the royal family at the funeral of the Dowager Queen Alexandra.
Refusing to return to Bucharest, Carol finally officially renounced the throne and prerogatives as crown prince on 28 December 1925.
In Romania, Helen was distraught by Carol's attitude, especially as Queen Marie made her partly responsible for the failure of her marriage.
The crown princess wrote to her husband to convince him to return.
She also attempted to convince politicians to delay Carol's exclusion to the royal succession and proposed to her in-laws that she herself take a trip to meet with her husband.
The head of government even accelerated the exclusion procedures by summoning both Houses of the Parliament to register the act of renunciation and appoint little Prince Michael as the new heir to the throne.
On 4 January 1926, the Romanian Parliament ratified the acceptance of Carol's renunciation and a royal ordinance was issued giving Helen the title princess of Romania; in addition, she was included in the Civil list, a privilege previously reserved to the sovereign and the heir to the throne.
After King Ferdinand I was diagnosed with cancer, a Regency Council was also formed during Michael's minority with Prince Nicholas as the Head, assisted by Patriarch Miron and the magistrate Gheorghe Buzdugan, replaced after his death in 1929 by Constantine Sărățeanu.
Despite this, Helen continued to hope for the return of her husband and obstinately refused requests for a divorce that he sent to her from abroad.
In June 1926, shortly before the death of her father-in-law, Helen went to Italy to attend the funeral of her paternal grandmother, Dowager Queen Olga of Greece, and moved with her mother to the Villa Bobolina in Fiesole.
The princess took advantage of her stay in Italy and to try to arrange for an encounter with her husband but, having initially agreeing to see her, Carol canceled the meeting at the last minute.
First reign of Michael I and Italian exile

In the spring of 1927, Queen Marie made an official visit to the United States.
During her absence, Helen and her sister-in-law Elisabeth took care of King Ferdinand I, whose health declined rapidly.
The king died on 20 July 1927 at Peleș Castle and his 5-year-old grandson succeeded him under the name of Michael
However, in Romania, Carol retained many supporters (soon nicknamed "Carlists") and the National Liberal Party began to fear the return of the Prince.
After trying to convince her husband to go to Bucharest, Helen gradually changed her attitude towards him.
Anxious to preserve the rights of her son and probably convinced by Prime Minister Barbu Știrbey, the princess requested a divorce, which she easily obtained.
Helen also distanced herself from her mother-in-law, who complained of being separated from the young king and criticized more openly the Greek entourage of the Princess.
After the Regency Council failed to govern the country, Carol appeared increasingly as a providential man who could solve the problems of Romania.
Still, his supporters (as Prime Minister Iuliu Maniu, leader of the National Peasants' Party) continued to demand his separation from Magda Lupescu and his reconciliation with Helen, which he refused.
Joyfully welcomed by the population and the political class, he then proclaimed himself king under the name of Carol II.
Impossible reconciliation with Carol II

When he came to power, Carol II initially refused to see Helen though he expressed his desire to meet his son, demoted to the rank of heir-apparent to the throne with the title of Grand Voivod of Alba Iulia by the Romanian Parliament (8 June 1930).
In order to be reunited with Michael, the king therefore resolved to meet his former wife.
Accompanied by his brother Nicholas and his sister Elizabeth, he visited the princess in her villa in the Șoseaua Kiseleff.
At the sight of her former husband, Helen showed coldness
In the following weeks, Helen suffered the combined pressures of politicians and the Romanian Orthodox Church, who were trying to persuade her to resume her conjugal life with Carol II and accept to be crowned along with him at a ceremony in Alba Iulia, scheduled on 21 September 1930.
Despite her reluctance, the princess agreed to a reconciliation and reconsidered the annulment of her divorce, but under the condition of having a separate residence.
These were the circumstances under which the former spouses lived and while Carol II sometimes went to Helen for lunch with her, the princess would, from time to time, have tea with him in the royal palace.
In July, the king, his former wife and son traveled together in Sinaia but while Carol II moved to Foișor, Helen and Michael stayed at Peleș Castle.
Each day, the family gathered for tea and, on 20 July, Carol II and Helen appeared publicly together on the occasion of a ceremony in memory of King Ferdinand I.


In August 1930, the government presented a decree to Carol II for his signature officially confirming Helen as Her Majesty, the Queen of Romania.
The king, however, crossed this out and declared Helen to be Her Majesty Helen (i.e. with the style Majesty, but not the title Queen).
Helen refused to allow anyone to use this style in her presence.
The return of Magda Lupescu to Romania finally put an end to the reconciliation efforts of the pair.
Soon the king was able to get Michael moved to his side, and Helen was allowed to see her son every day in exchange for her political silence.
Increasingly isolated, the princess was forced into exile by her former husband, she consented to a separation agreement in October 1931.
In exchange for her silence, and through the mediation of her brother, the former King George II of Greece, and her sister-in-law Elisabeth, Helen then obtained a substantial monetary compensation.
With the approval of Carol II, she obtained the right to stay four months a year in Romania and to receive her son abroad during two months of the year.
Especially, Helen received a sum of thirty million lei to buy a home abroad and in addition she obtained an annual pension of seven million lei.
Between scandal and exile

In November 1931, Helen left Romania for Germany, where she went to the bedside of her mother, the Dowager Queen Sophia of Greece, seriously ill with cancer.
After her death on 13 January 1932, Helen bought her house in Fiesole, Tuscany, which she used as her main residence.
In this large house, that she renamed Villa Sparta, the princess received the visit of her sisters Irene and Katherine and her brother Paul, who remained with Helen on long stays.
Despite the distance, the friction between Helen and Carol II continued.
In September 1932, a visit from Michael and his mother to the United Kingdom was used by Helen as an opportunity for a new, very public conflict, which soon made the headlines of the international press, just as Helen wanted.
Helen was incensed at the second stipulation and, as was her wont, took the trouble to aggravate the situation by defying the first stipulation as well.
Helen now decided to grant an interview to the Daily Mail "in the hope," she said, "that public opinion would help to preserve her parental rights".
Despite these events, Helen chose to return to Romania for Michael's birthday and threatened to go to the International Court of Justice if Carol II did not allow her to see their son.
Back in Bucharest, the princess tried, without much success, to get the government involved in a case against the king.
However, the latter was deeply shocked by the interview given to the Daily Mail, and the two women had a violent fight during their reunion, where Elisabeth slapped Helen.
Carol II then considered his former wife as a political opponent, and in order to undermine her prestige, the king initiated a campaign in the press against her, claiming that she had tried to commit suicide twice.
After only a month in the country, Carol II imposed a new separation agreement (1 November 1932), under which Helen was denied the right to return to Romania and the next day, finally forced her into permanent exile in Italy.
Despite the tensions, Prince Michael was able to see his mother every year in Florence for two months.
In Fiesole, the life of Helen and her sisters was relatively retired, even though they were frequently visited by the Italian House of Savoy, which had always been welcoming to the Greek royal family during its exile.
In 1935, they took advantage of the presence in Florence of Princess Frederica of Hanover to arrange an encounter between her and their brother.
However, the princess' parents were reluctant to approve this relationship and it was not until 1937 that Paul and Frederica were finally allowed to get engaged.
In the meantime, the Greek monarchy was restored and George II once again became King of Greece, but his wife Elisabeth, who filed for divorce on 6 July 1935, remained in Romania.
Queen Mother of Romania

World War II and the dictatorship of Antonescu

In Tuscany, Helen found real stability, despite the absence of her son most of the year.
In accordance with the Molotov–Ribbentrop Pact, the Soviet Union forced Romania to cede Bessarabia and Northern Bukovina to them on 26 June 1940, and a few weeks later, the country was also forced to surrender Northern Transylvania to Hungary (Second Vienna Award, 30 August 1940) and the Southern Dobruja to Bulgaria (Treaty of Craiova, 7 September 1940); these territorial losses ended the Greater Romania, created at the end of World War I. Unable to maintain the territorial integrity of his country and under pressure from the Iron Guard, a fascist party supported by Nazi Germany, Carol II became increasingly unpopular and finally was forced to abdicate on 6 September 1940.
His son Michael, aged 18, became king while General Ion Antonescu established a dictatorship with the support of members of the Iron Guard.
Eager to obtain the favor of the new sovereign (and some legitimation to his dictatorship), Antonescu granted Helen the title of "Queen Mother of Romania" (Regina-mamă Elena) with the style "Her Majesty" on 8 September 1940 and sent the diplomat Raoul Bossy to Fiesole to persuade her to return to Bucharest (12 September 1940).
Back in Romania (14 September 1940), Helen found herself, however, subject to the whim of the dictator, determined to keep the royal family in a purely ceremonial role.
In this difficult context, Michael I was at times prone to bouts of depression and Helen then concentrated all of her efforts to make him more active.
Alerted by the Rabbi Alexandru Șafran about the anti-Jewish persecutions, Helen personally appealed to the German ambassador Manfred Freiherr von Killinger and Antonescu to convince them to halt the deportations, being supported in her efforts by Patriarch Nicodim.
For his part, the king vigorously protested to the Conducător at the time of the Odessa massacre and notably obtained the release of Wilhelm Filderman, president of the Romanian Jewish community.
Despite these few attempts of emancipation, Helen and her son spent most of the conflict playing as hosts of the German officers passing through Bucharest.
The queen mother even met Hitler twice: firstly informally, with her sister Irene, to discuss the fate of Greece and Romania within the new Europe (December 1940) and secondly formally with Michael I during a trip in Italy (winter of 1941).
Above all, Helen and her son had no choice but to officially support the dictatorship of Antonescu.
Thus, it was Michael I who gave the Conducător the title of Marshal (21 August 1941) after the reconquest of Bessarabia by the Romanian Army.
In the fall of 1942, Helen played a major role in stopping Antonescu from his plans to deport all of the Jews of the Regat to the German death camp of Bełżec in Poland.
According to SS Hauptsturmführer Gustav Richter, the counselor for Jewish Affairs at the German legation in Bucharest in a report sent to Berlin on 30 October 1942: .mw-parser-output .templatequote{overflow:hidden;margin:1em 0;padding:0 32px}.mw-parser-output .templatequotecite{line-height:1.5em;text-align:left;margin-top:0}@media(min-width:500px){.mw-parser-output .templatequotecite{padding-left:1.6em}}

"The queen mother told the king that what was happening...was a disgrace and that she could not bear it any longer, all the more so because  would be permanently associated...with the crimes committed against the Jews, while she would be known as the mother of "Michael the Wicked".
As a result the King...telephoned Prime Minister Ion Antonescu and...a meeting of the Council of Ministers took place."

Coup of Michael I and end of the war

From 1941, the participation of the Romanian army in the invasion of the Soviet Union further damaged the relations between Antonescu and the royal family, who disapproved of the conquests of Odessa and Ukraine.
However, it was the Battle of Stalingrad (23 August 1942 – 2 February 1943) and the losses incurred by the Romanian side that finally forced Michael I to organize around him a resistance against the dictatorship of the Conducător.
During an official speech on 1 January 1943, the sovereign publicly condemned the participation of Romania in the war against the Soviet Union, triggering the wrath of both Antonescu and the Nazi Germany, who accused Helen of being behind the royal initiative.
In retaliation, Antonescu tightened his control over Michael I and his mother, and threatened the royal family with the abolition of the monarchy if any further provocation were to occur.
Over the next few months, the suspicious death of Tsar Boris III of Bulgaria (28 August 1943) and the successive arrests of princesses Mafalda of Savoy (23 September 1943) and Irene of Greece (October 1943) after the overthrow of Mussolini by King Victor Emmanuel III of Italy (25 July 1943), proved to Michael I and his mother just how dangerous opposition to the Axis powers was.
On 23 August 1944 Michael I organized a coup d'état against the Conducător, who was imprisoned.
However, the Allies did not immediately recognize the reversal of Romania and the Soviets entered the capital on 31 August 1944.
Visiting Sinaia at the time of the royal coup d'état, Helen found her son the next day at Craiova.
Back in Bucharest on 10 September 1944, the king and his mother moved into the residence of Princess Elizabeth, whose relations with Helen remained tense despite their reconciliation in 1940.
With the increased instability in Romania, the queen mother was extremely concerned about the safety of her son, fearing that he could eventually be killed, like Prince-Regent Kiril of Bulgaria, shot by the Communists on 1 February 1945.
She was also concerned about the machinations of Carol II, who apparently waited for the end of the war to return to Romania, and observed with anxiety the political crisis that prevented King George II from regaining power in Greece.
In this difficult context, Helen had the joy of learning that her sister Irene and her little nephew Amedeo were alive, although still in German hands.
Imposition of a communist regime

With the Soviet occupation, the staff of the Romanian Communist Party, which counted only a few thousand members during the coup of Michael I, exploded and demonstrations against the government of Constantin Sănătescu multiplied.
On 6 March 1945 Michael I finally called Petru Groza, leader of the Ploughmen's Front, as the new head of a government which had no association with any representative of either the Peasants and the Liberal parties.
Satisfied with this appointment, the Soviet authorities were more conciliatory with Romania.
A few months later, on 19 July 1945, Michael I was decorated with the Order of Victory, one of the most prestigious Soviet military orders.
After the Potsdam Conference and the reaffirmation by the Allies of the need to establish democratically elected governments in Europe, Michael I demanded the resignation of Petru Groza, who refused.
The resistance of the monarch, however, was not supported by the West, who after the Moscow Conference of 25 December 1945, asked Romania to allow two opposition figures to enter the government.
Disgusted by all these betrayals, Helen, in turn, encouraged fewer meetings with Soviet officials and worried every day for the life of her son.
In their palace, they had no access to running water for three hours a day and the electricity was off most of the day.
This did not prevent Helen from maintaining her charitable activities and continuing to send food and clothing to Moldavia.
She then reunited with her sister Irene, weakened after her deportation to Austria, attended the funeral of her elder brother, King George II, and participated in the marriage of her youngest sister, Princess Katherine, with British Major Richard Brandram.
Under these conditions, the queen mother considered exile with more determination but she was concerned that they did not possess any foreign resources, because her son refused to save money outside of Romania.
As guests to the marriage of Princess Elizabeth of the United Kingdom with Prince Philip of Greece and Denmark (Helen's first cousin) on 20 November 1947, Michael I and his mother were provided with an opportunity to travel together abroad.
During this stay, the king fell in love with Princess Anne of Bourbon-Parma, with whom he became engaged much to Helen's delight.
This trip was also an opportunity for the queen mother to place two small paintings of El Greco from the royal collections in a Swiss bank.
Abolition of the Romanian monarchy and Michael
I's wedding

Deposition of Michael I and the first months of exile

Despite the advice of their relatives, who urged them not to return to Romania in order to escape the communists, the king and his mother returned to Bucharest on 21 December 1947.
The two politicians asked Michael I to sign a declaration of abdication.
The heavy clashes ensued in Bucharest and other big cities in Romania after the Communist Party falsified the votes for the 1946 Parliament elections, which the National Peasant's Party (PNȚ) had won with over 70%.
Forced with this blackmail, Michael I renounced the crown.
Michael I and Helen left Romania with some partisans on 3 January 1948.
In exile, Michael I and Helen settled for some time in Switzerland, where the deposed sovereign bitterly observed the Western acceptance of the establishment of a communist republic in Romania.
For her part, Helen was mostly concerned with the state of their finances because the Communists allowed them to part with almost nothing.
At the same time, the king and his mother had to deal with the intrigues of Carol II, who still considered himself the only legitimate sovereign of Romania and accused his ex-wife of keeping him away from their son.
To achieve his ends, Carol II did not hesitate to involve Frederick, Prince of Hohenzollern-Sigmaringen (Head of the dynasty) and Prince Nicholas of Romania in his intrigues.
These concerns did not prevent Michael I and his mother from undertaking several political trips to the United Kingdom, France and the United States to meet with government leaders and representatives of the Romanian diaspora.
Marriage of Michael I and Anne of Bourbon-Parma

Another source of concern from Michael I and his mother during their first months of exile was his marriage with Princess Anne of Bourbon-Parma.
To discredit the former monarch, the Romanian authorities promoted rumors that Michael I gave up his dynastic rights in order to marry the woman of his heart, as his father did in 1925.
Added to this, the most serious difficulties were related to religion.
Being a Roman Catholic, Princess Anne had to obtain a papal dispensation to marry an Orthodox.
However, the Vatican had been extremely reluctant to grant consent because, for dynastic reasons, the couple's children would have to be raised in Michael
After Prince René of Bourbon-Parma, father of the bride, failed in his negotiations with the Vatican, Helen decided to go to Rome with Princess Margaret of Denmark (Anne's mother) to meet Pope Pius XII.
Under these circumstances, Princess Anne had no choice but to override the pontifical will and abandon a Catholic marriage.
Once again, the queen mother tried to mediate, this time with Anne's family, but without success.
Helen had better luck with her own family.
Her brother, King Paul I of Greece, offered to organize Michael's wedding in Athens, despite official protests from the Romanian government.
Celebrated in the throne room of the Royal Palace, the wedding brought together most of the members of the Greek dynasty but no representative of the Houses of Bourbon-Parma or Hohenzollern-Sigmaringen.
In fact, Carol II was not invited to the wedding, despite Helen having written to him about the marriage.
Exile and later years

Return to Villa Sparta

After the marriage of Michael I and Anne, Helen returned to Villa Sparta in Fiesole.
Over the years, the family of the former king grew with the successive births of princesses Margareta (1949), Elena (1950), Irina (1953), Sophie (1957) and Maria (1964).
From 1949 to 1950, Helen also housed her sister Irene and her nephew Amedeo, who later settled in a neighboring residence.
Throughout her life, Helen also remained deeply attached to Amedeo and his first wife, Princess Claude of Orléans.
Helen also made many trips abroad to visit her relatives.
Despite her sometimes stormy relationship with her sister-in-law, Queen Frederica, Helen also spent long periods in Greece and participated in the Cruise of the Kings in 1954, the marriage of Princess Sophia with the future
Despite this, Helen's life was not solely devoted to her family.
From 1968 to 1973, Helen had a romantic relationship with the twice-widower King Gustaf VI Adolf of Sweden, with whom she shared a love of art and plants.
In 1956 Helen consented for Arthur Gould Lee to publish her biography.
Despite still being deprived of income by the Romanian authorities, the queen mother economically supported her son, and also helped him to find jobs, first as a pilot in Switzerland, then as a broker on Wall Street.
Helen also supported the studies of her eldest granddaughter Margareta, and even welcomed her at Villa Sparta for a year before she entered a British university.
To do this, Helen was forced to sell her assets one by one and in the early 1970s, she hardly had anything left.
In 1973, she mortgaged her residence and three years later, she sold the two Greco paintings that she had brought with her from Romania in 1947.
Life in Switzerland and death

Becoming too old to live alone, Helen finally left Fiesole in 1979.
She then moved to a small apartment in Lausanne, located 45 minutes from the residence of Michael I and Anne, before moving in with them at Versoix in 1981.
Helen, queen mother of Romania, died one year later on 28 November 1982, aged 86.
Eleven years after her death, in March 1993, the State of Israel gave Helen the title of Righteous Among the Nations in recognition for her actions during World War II towards Romanian Jews, several thousands of whom she managed to save from 1941 to 1944.
In January 2018, it was announced that the remains of King Carol II would be moved to the new Archdiocesan and Royal Cathedral, along with those of Queen Mother Helen.
Queen Mother Helen of Romania was reburied at the New Episcopal and Royal Cathedral in Curtea de Argeș on 19 October 2019.
Archives

Queen Helen's correspondence with the Romanian diplomat George I. Duca between 1940 and 1982 is preserved in the "George I. Duca Papers" collection in the Hoover Institution Archives (Stanford, California, USA).



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (11c6ada6-d409-42b0-96bd-c6c0790527a4)
 Call ID: 11c6ada6-d409-42b0-96bd-c6c0790527a4
  Args:
    type: :Woman
    source: :Helen_of_Greece_and_Denmark
  AssignClass (ce1df9c0-71fc-4f2b-9cab-a147a988ea62)
 Call ID: ce1df9c0-71fc-4f2b-9cab-a147a988ea62
  Args:
    type: :Person
    source: :Helen_of_Greece_and_Denmark
  AddLiteral (a85bbf68-7fb5-41b4-ba0f-ca3c4d4e1107)
 Call ID: a85bbf68-7fb5-41b4-ba0f-ca3c4d4e1107
  Args:
    literal_type: xsd:integer
    source: :Helen_of_Greece_and_Denmark
    literal_value: 1896
    relation: :hasBirthYear
  AddLiteral (01f1b4ee-4aa9-4366-a025-835966f0f151)
 Call ID: 01f1b4ee-4aa9-4366-a025-835966f0f151
  Args:
    relation: :hasDeathYear
    literal_value: 1982
    source: :Helen_of_Greece_and_Denmark
    literal_type: xsd:integer
  AssignClass (1d362d7c-ae55-4018-afea-32834e291742)
 Call ID: 1d362d7c-ae55-4018-afea-32834e291742
  Args:
    type: :Man
    source: :King_Constantine_I_of_Greece
  AssignClass (daa4c9cc-a3c4-4337-9034-83460d39b6cd)
 Call ID: daa4c9cc-a3c4-4337-9034-83460d39b6cd
  Args:
    source: :King_Constantine_I_of_Greece
    type: :Person
  AssignClass (e7c9a46d-caea-49af-a559-bc3208bb4124)
 Call ID: e7c9a46d-caea-49af-a559-bc3208bb4124
  Args:
    type: :Woman
    source: :Princess_Sophia_of_Prussia
  AssignClass (a06295c5-5089-4ce8-9c76-1913bfa7065a)
 Call ID: a06295c5-5089-4ce8-9c76-1913bfa7065a
  Args:
    type: :Person
    source: :Princess_Sophia_of_Prussia
  AddTriple (9047ef6b-92f0-4dfd-a636-5a28b8ff35be)
 Call ID: 9047ef6b-92f0-4dfd-a636-5a28b8ff35be
  Args:
    relation: :hasFather
    source: :Helen_of_Greece_and_Denmark
    target: :King_Constantine_I_of_Greece
  AddTriple (ed53e5a5-16cf-492a-87f2-1647d9babbe6)
 Call ID: ed53e5a5-16cf-492a-87f2-1647d9babbe6
  Args:
    relation: :hasMother
    source: :Helen_of_Greece_and_Denmark
    target: :Princess_Sophia_of_Prussia
  AssignClass (bdb49083-177c-4fc3-b00b-4d88a2469991)
 Call ID: bdb49083-177c-4fc3-b00b-4d88a2469991
  Args:
    type: :Man
    source: :King_Michael_I_of_Romania
  AssignClass (40bce6aa-1072-4f08-88f9-00300520637a)
 Call ID: 40bce6aa-1072-4f08-88f9-00300520637a
  Args:
    source: :King_Michael_I_of_Romania
    type: :Person
  AddTriple (39dae733-3a7d-400c-a603-0cc681498d38)
 Call ID: 39dae733-3a7d-400c-a603-0cc681498d38
  Args:
    source: :King_Michael_I_of_Romania
    target: :Helen_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (d2a93f46-57b3-489e-8538-81aab96ba6df)
 Call ID: d2a93f46-57b3-489e-8538-81aab96ba6df
  Args:
    source: :King_Carol_II_of_Romania
    type: :Man
  AssignClass (1ec85827-c00d-4c30-80d6-ad50dffc1def)
 Call ID: 1ec85827-c00d-4c30-80d6-ad50dffc1def
  Args:
    source: :King_Carol_II_of_Romania
    type: :Person
  AddTriple (3e4e92e3-a646-4786-998e-d065e7ad0d88)
 Call ID: 3e4e92e3-a646-4786-998e-d065e7ad0d88
  Args:
    target: :King_Carol_II_of_Romania
    source: :King_Michael_I_of_Romania
    relation: :hasFather
  AddTriple (29433740-abeb-473c-b31e-2689bd61114a)
 Call ID: 29433740-abeb-473c-b31e-2689bd61114a
  Args:
    relation: :hasMother
    source: :King_Carol_II_of_Romania
    target: :Queen_Marie_of_Romania
  AssignClass (5ca0b40e-196b-4351-b8a6-1a4d1c431efa)
 Call ID: 5ca0b40e-196b-4351-b8a6-1a4d1c431efa
  Args:
    source: :Queen_Marie_of_Romania
    type: :Woman
  AssignClass (47787866-4d4a-4aa8-9dfb-a137c6e8648c)
 Call ID: 47787866-4d4a-4aa8-9dfb-a137c6e8648c
  Args:
    type: :Person
    source: :Queen_Marie_of_Romania
  AssignClass (ad0d608d-b794-448a-88e8-ee1833115389)
 Call ID: ad0d608d-b794-448a-88e8-ee1833115389
  Args:
    source: :Alexander_I_of_Greece
    type: :Man
  AssignClass (331b06c4-7766-4f4b-804e-9c578e9a5700)
 Call ID: 331b06c4-7766-4f4b-804e-9c578e9a5700
  Args:
    source: :Alexander_I_of_Greece
    type: :Person
  AddTriple (3b112535-33cb-45dd-8d62-eddad6b47f0e)
 Call ID: 3b112535-33cb-45dd-8d62-eddad6b47f0e
  Args:
    relation: :hasBrother
    source: :Helen_of_Greece_and_Denmark
    target: :Alexander_I_of_Greece
  AssignClass (69752816-82a4-47ff-82bf-f4e43d511d7e)
 Call ID: 69752816-82a4-47ff-82bf-f4e43d511d7e
  Args:
    source: :King_George_I_of_Greece
    type: :Man
  AssignClass (6183d170-b2f6-4b7e-a3e2-1437f7eba54d)
 Call ID: 6183d170-b2f6-4b7e-a3e2-1437f7eba54d
  Args:
    source: :King_George_I_of_Greece
    type: :Person
  AddTriple (2040119b-29cd-488d-a6a6-81bf4154b3cd)
 Call ID: 2040119b-29cd-488d-a6a6-81bf4154b3cd
  Args:
    target: :King_George_I_of_Greece
    source: :King_Constantine_I_of_Greece
    relation: :hasFather
  AssignClass (b75b9596-799b-4bde-bd94-a5c8ab437c12)
 Call ID: b75b9596-799b-4bde-bd94-a5c8ab437c12
  Args:
    type: :Woman
    source: :Princess_Irene_of_Greece_and_Denmark
  AssignClass (ad6898e7-a565-4e9a-a742-84146963248e)
 Call ID: ad6898e7-a565-4e9a-a742-84146963248e
  Args:
    source: :Princess_Irene_of_Greece_and_Denmark
    type: :Person
  AddTriple (c737d5ab-19ab-4ca0-a8d9-95523ecd8ab2)
 Call ID: c737d5ab-19ab-4ca0-a8d9-95523ecd8ab2
  Args:
    target: :Princess_Irene_of_Greece_and_Denmark
    source: :Helen_of_Greece_and_Denmark
    relation: :hasSister
  AssignClass (69681be1-9622-46b9-a8bb-f5472b8d1fa2)
 Call ID: 69681be1-9622-46b9-a8bb-f5472b8d1fa2
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    type: :Woman
  AssignClass (53019f4f-40ec-4f79-ba21-45ed7c88dfd0)
 Call ID: 53019f4f-40ec-4f79-ba21-45ed7c88dfd0
  Args:
    source: :Princess_Katherine_of_Greece_and_Denmark
    type: :Person
  AddTriple (b07d1cf5-0b82-4fa0-b530-0b3e745d035e)
 Call ID: b07d1cf5-0b82-4fa0-b530-0b3e745d035e
  Args:
    source: :Helen_of_Greece_and_Denmark
    target: :Princess_Katherine_of_Greece_and_Denmark
    relation: :hasSister
  AssignClass (b9551e12-e7c9-47a5-909f-a367e900f4f3)
 Call ID: b9551e12-e7c9-47a5-909f-a367e900f4f3
  Args:
    source: :King_George_II_of_Greece
    type: :Man
  AssignClass (aadb11a3-95cf-4694-8c31-ae34ff0d792f)
 Call ID: aadb11a3-95cf-4694-8c31-ae34ff0d792f
  Args:
    type: :Person
    source: :King_George_II_of_Greece
  AddTriple (39de8b64-b9de-4cb3-b03c-a0326a4e09ff)
 Call ID: 39de8b64-b9de-4cb3-b03c-a0326a4e09ff
  Args:
    relation: :hasBrother
    source: :Helen_of_Greece_and_Denmark
    target: :King_George_II_of_Greece
  AssignClass (b29b5f54-8352-4671-8481-89083905d22c)
 Call ID: b29b5f54-8352-4671-8481-89083905d22c
  Args:
    type: :Man
    source: :Prince_Paul_of_Greece_and_Denmark
  AssignClass (3c3fe1d8-2846-44be-aa66-9b36fc49af65)
 Call ID: 3c3fe1d8-2846-44be-aa66-9b36fc49af65
  Args:
    source: :Prince_Paul_of_Greece_and_Denmark
    type: :Person
  AddTriple (59fa1672-2032-4369-8180-06f5f448f42d)
 Call ID: 59fa1672-2032-4369-8180-06f5f448f42d
  Args:
    relation: :hasBrother
    source: :Helen_of_Greece_and_Denmark
    target: :Prince_Paul_of_Greece_and_Denmark
  AssignClass (702bc162-261d-4ccf-bbf4-8651c70a3374)
 Call ID: 702bc162-261d-4ccf-bbf4-8651c70a3374
  Args:
    type: :Woman
    source: :Princess_Elisabeth_of_Romania
  AssignClass (9d295279-e5cd-4263-9e0e-426a2adb2218)
 Call ID: 9d295279-e5cd-4263-9e0e-426a2adb2218
  Args:
    type: :Person
    source: :Princess_Elisabeth_of_Romania
  AddTriple (4f4baa31-3f77-41e1-b989-2c0fda192017)
 Call ID: 4f4baa31-3f77-41e1-b989-2c0fda192017
  Args:
    relation: :hasSister
    source: :King_Carol_II_of_Romania
    target: :Princess_Elisabeth_of_Romania
  AssignClass (89b15164-9498-467d-9683-5c79a66cf8ea)
 Call ID: 89b15164-9498-467d-9683-5c79a66cf8ea
  Args:
    type: :Woman
    source: :Princess_Maria_of_Romania
  AssignClass (daaccb8e-eb2c-4372-9438-8867c1f115ec)
 Call ID: daaccb8e-eb2c-4372-9438-8867c1f115ec
  Args:
    type: :Person
    source: :Princess_Maria_of_Romania
  AddTriple (80aa4146-014f-481a-9d9a-6333918994fc)
 Call ID: 80aa4146-014f-481a-9d9a-6333918994fc
  Args:
    source: :King_Carol_II_of_Romania
    target: :Princess_Maria_of_Romania
    relation: :hasSister
  AssignClass (da47d895-e76f-4d7d-aa56-d38d011ca562)
 Call ID: da47d895-e76f-4d7d-aa56-d38d011ca562
  Args:
    source: :Princess_Ileana_of_Romania
    type: :Woman
  AssignClass (f683421e-1466-48ea-97f3-5b07c441facd)
 Call ID: f683421e-1466-48ea-97f3-5b07c441facd
  Args:
    type: :Person
    source: :Princess_Ileana_of_Romania
  AddTriple (099413cb-9d86-4de9-a764-b80ca842b47b)
 Call ID: 099413cb-9d86-4de9-a764-b80ca842b47b
  Args:
    target: :Princess_Ileana_of_Romania
    source: :King_Carol_II_of_Romania
    relation: :hasSister
  AssignClass (c4bca0e9-e648-46a3-a81a-e5f9d0575f69)
 Call ID: c4bca0e9-e648-46a3-a81a-e5f9d0575f69
  Args:
    type: :Man
    source: :Prince_Nicolae_of_Romania
  AssignClass (44d296fc-e342-46bf-b43a-8e3e3d9ed298)
 Call ID: 44d296fc-e342-46bf-b43a-8e3e3d9ed298
  Args:
    source: :Prince_Nicolae_of_Romania
    type: :Person
  AddTriple (2b8a6b12-87c3-46f3-b508-b8f62a5b686e)
 Call ID: 2b8a6b12-87c3-46f3-b508-b8f62a5b686e
  Args:
    target: :Prince_Nicolae_of_Romania
    source: :King_Carol_II_of_Romania
    relation: :hasBrother
  Finish (31bf4c1b-a564-43d5-8c4a-2b74503f69c9)
 Call ID: 31bf4c1b-a564-43d5-8c4a-2b74503f69c9
  Args: