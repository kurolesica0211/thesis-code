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
Paul (Greek: Παύλος, romanized: Pavlos; 14 December 1901 – 6 March 1964) was King of Greece from 1 April 1947 until his death on 6 March 1964.
Paul was born in Athens as the third son of Crown Prince Constantine and Crown Princess Sophia of Greece.
At the 1936 Berlin Olympic Games, Paul successfully proposed to Frederica of Hanover, whom he had been seeing regularly for the past year.
Though Paul successfully secured money from the Marshall Plan to fund recovery and infrastructure projects, he was criticised for limiting democracy when the new 1952 Greek constitution gave extensive powers to the monarch.
He was succeeded by his only son, who became Constantine II.
Paul had three children: Queen Sofía of Spain, Constantine II of Greece, and Princess Irene.
Early life

Paul was born on 14 December  1901 at the Tatoi Palace in Attica north of Athens, the third son of Crown Prince Constantine and his wife, Princess Sophia of Prussia.
He was privately tutored by foreign teachers, Greek university professors, who were chosen by Constantine, and Dr Hoenig, his mother's Pomeranian chaplain.
In 1909, when Paul was seven years old, a group of Greek officers mounted a coup d'état against his grandfather, George I of Greece.
The officers, led by Nikolaos Zorbas, declared themselves in support of the monarchy, however, asked George I to dismiss his sons from the army.
As a result of criticism, Constantine decided to move with his wife and his sons, including Paul, to Germany for several months.
The family stayed with Princess Margaret of Prussia, who was Paul's maternal aunt, in Kronberg.
The family returned to Greece at the beginning of 1911, when the new Greek Prime minister, Eleftherios Venizelos, allowed the princes to regain the ranks in the military.
The following year, in 1912, and until 1913, Greece fought in the Balkan Wars.
Greece was able to double its size in territory in the wars, during which Paul served as the youngest cadet in the Hellenic navy, at eleven years old.
World War I and aftermath

National Schism

Paul's father, Constantine, ascended to the throne upon the assassination of George I in 1913.
Constantine wished to keep Greece neutral during the prelude to World War I, but was in support of the Central Powers, since he was the brother-in-law of the German Kaiser, Wilhelm II.
The disagreement between Constantine and Venizelos quickly resulted in the National Schism, a civil war between the two opposing sides.
Per Van der Kiste, possibly due to "being afraid" of Wilhelm II, Constantine continued to refuse to succumb to Venizelos' demands.
Constantine was also pressured to oppose Venizelos by Ioannis Metaxas.
On 10 June 1917, Charles Jonnart, who acted as the Allies' representative in Greece, ordered Constantine to abdicate.
The Allies threatened to invade Greece from a military landing at Piraeus, so Constantine unofficially abdicated.
The Allies did not wish to replace Greece with a republican system, so Venizelos scrambled to find a replacement king.
It was finally decided that Paul's older brother, Alexander, though not the eldest son of Constantine, would succeed to the throne, as Constantine's eldest son, George, was also seen as pro-German.
The rest of the extended Greek royal family joined them when Venizelos announced Greece's entry into World War I. In 1918, Constantine contracted the Spanish flu, causing him to fall severely ill and restricting him from providing for Paul and his other children.
Constantine remained concerned about Paul's lack of education after the Greek government refused his entry into the British Royal Navy.
To Paul's dismay, Constantine accepted the offer made by Wilhelm II for Paul to join the Imperial German Navy.
Paul continued to join the German Imperial Naval Academy, where his training was supervised by his uncle, Prince Henry of Prussia.
After World War I, Greece had made territorial gains in Thrace and Anatolia per the Treaty of Sèvres, to the dismay of the Ottomans, causing the Greco-Turkish War.
Despite the war's resolution, tension between Constantine and Venizelos still remained high.
Paul's brother, Alexander, died of sepsis after having been bitten by a monkey, leaving Greece without a monarch and plunging the country into a constitutional crisis.
The Greek parliament refused to reinstate Constantine, and thus Venizelos, on 29 October 1920, sent a letter to the Greek ambassador to Switzerland at the National Hotel in Lucerne, requesting that he meet with Paul, who he saw as the new potential king.
Paul wrote that neither his father, Constantine, nor his older brother, George, had ever renounced their rights to the throne and that therefore, his ascension to the throne would be illegitimate.
The Greek throne remained vacant while Greece fought in the Greco-Turkish War, during the Turkish War of Independence.
During the 1920 Greek legislative election, fighting broke out between a sector of monarchists, who protested for Constantine's reascension to the throne, and supporters of Venizelos.
On 14 November 1920, the monarchists won and it was organised for Constantine to become King of the Hellenes, while Venizelos was replaced with Dimitrios Rallis.
Before Venizelos' exit from office, he requested that Paul's grandmother, Olga Constantinovna of Russia, act as regent before Constantine returned.
Return to Greece

On 19 December 1920, Paul and the other Greek royals returned to Greece.
However, Constantine's restoration was criticised by Greece's allies in the concurrent Greco-Turkish war, most of which were also Greece's allies in World War I, to which Constantine refused to join.
Constantine was denied additional support from the Allies in the war against Turkey, allowing Mustafa Kemal to eventually make more territorial gains.
Constantine left Paul and his other children with his wife in 1921 when he travelled to Anatolia to boost the morale of Greek troops.
While on the frontlines, Constantine attempted to boost confidence by reminding soldiers of their successes in the Balkan Wars.
However, after only a few months, Constantine reunited with his children at Tatoi in September 1921.
Upon their return to Greece, Paul wished to resume his naval training and joined the Hellenic Naval Academy, taking up residence in the academy's boarding school, located in Piraeus.
Despite Greece's involvement in the Turkish War of Independence, Paul never fought in a battle but participated in the evacuation of Greek and Armenian refugees from Smyrnan shores following the burning of Smyrna by Turkish troops.
Turkey later defeated Greece and their allies, who had been suffering since the fall of Smyrna in August 1922.
Crown Prince

Abdication of father

Republican propaganda began gaining speed and was being produced by supporters of Venizelos, who was no longer serving in office.
On 11 September 1922, a precinct of the army, led by colonels Nikolaos Plastiras and Stylianos Gonatas, conducted a coup d'état which turned into the 11 September 1922 Revolution, where the second abdication of Constantine was demanded, in addition to the dissolution of the Greek parliament.
To avoid unrest and civil war, Constantine abdicated on 27 September, before fleeing to Palermo with his wife and daughters, leaving his two sons, Paul and George, behind.
George, the eldest son, succeeded him as George II during political instability caused by the ongoing effects and aftermath of the Greek genocide.
With his brother remaining childless, Paul was officially declared the Crown Prince of Greece.
However, the birth of a child between George and his wife, Elisabeth of Romania, would remove Paul from his first-in-line position to the throne.
With greater roles as Crown Prince, Paul greater divided his time between serving as a lieutenant in the navy and completing his royal duties in Athens, where he attempted to assist George and Elisabeth in their roles of positively representing the monarchy, which had been facing backlash for almost the past decade.
Paul and George's father, Constantine, died in exile on 11 January 1923.
The government refused to give Constantine a state funeral and Paul was placed in charge of organising his funeral in Italy.
George was forced to pay a large sum of money as compensation for the victim's family by using the royal family's funds, which had already been greatly depleted because of the Greco-Turkish war.
George succumbed to political pressure but refused to abdicate.
Tatoi told the press that George and the royal family would be taking an official visit to Romania to visit Elisabeth's family, however they were going into exile.
George and Elisabeth left the country first, followed by Paul and other members of the royal family on 19 December 1923, residing in Bucharest.
Two months after Venizelos' government was proclaimed, the Kingdom of Greece was replaced by the Second Hellenic Republic on 25 March 1924, Greece's national independence day.
Two and a half weeks later, the democratically conducted 1924 Greek republic referendum occurred, confirming the abolition of the monarchy and officially removing George as Greece's head of state and Paul as the Crown Prince of Greece.
In Bucharest, where the royal family remained, Paul was welcomed by his sister, Princess Helen, who was unhappily married to the future Carol II of Romania.
Not too long after arriving in Romania, Paul departed to stay with his mother and sisters, Princess Irene and Princess Katherine, at the Viva Bobolina in Fiesole.
According to historian Stelios Hourmouzios, Henry Drummond Wolff, and according to historian Ricardo Mateos Sáinz de Medrano, Alphonse d'Orléans, helped Paul become hired as an apprentice mechanic for Armstrong Siddeley.
Paul's family discovered an affair between him and Princess Nina Georgievna of Russia, but he claimed that he had fallen in love.
Nina was the elder daughter of Paul's aunt, Maria, and Grand Duke George Mikhailovich of Russia, making her Paul's first cousin.
However, Nina rejected his later marriage proposal, choosing instead to marry Prince Paul Aleksandrovich Chavchavadze in 1922.
Paul became pressured as the responsibility of continuing the family's lineage increased due to George and Elisabeth's sterility.
In Spring 1930 Paul met Captain Frederick Wessel, a wealthy annuitant of Danish origin.
While illegally travelling through Greece, Paul visited his former residences, Mon Repos, the former royal palace in Athens, and Tatoi.
Restoration of the monarchy

The Second Hellenic Republic had tired most Greeks out, with, in only eleven years, 23 governments, 13 coup d'états and one dictatorship.
Most supported George's restoration, however, there were large minorities that wished for the king to be a different person, such as Prince George, Duke of Kent.
Kondylis' government proclaimed that the Kingdom of Greece had been restored, and he became the regent of Greece while George travelled from England to take back the crown.
Before doing so, George, supported by Paul and other members of the family, ordered that a referendum be hosted to confirm his return.
Once the figure of the supposed overwhelming support for the monarchy was announced, a Greek ambassador met with George and Paul at the Greek embassy in London and officially requested that they return to Tatoi.
On 5 November 1935, they accepted and began their journeys back to Greece on 14 November.
Before returning to Greece, they stopped in Paris and met President Albert Lebrun and their uncle, Prince Andrew.
Paul and George then stopped in Italy to collect their sisters, who had been living in the Villa Sparta, and other members of the Greek royal family, such as Prince Christopher.
Paul and his family briefly went to Florence to pay homage to their parents, who had been buried temporarily beside the Church of the Nativity of Christ and St. Nicholas, a Russian Orthodox Church.
In Rome, Victor Emmanuel III gifted the Greek royals the Supreme Order of the Most Holy Annunciation.
Paul became overwhelmed with his royal duties upon George's almost immediate neglect of his role within Greece.
Historian John Van der Kiste describes George as having become a "suspicious and taciturn man" who had little interest in showing affinity and becoming close with his younger brother, Paul.
Paul frequently acted as the unofficial regent for Greece and often represented George at events, such as at the repatriation of their parents' bodies to the Tatoi burial grounds and at Venizelos' funeral in 1936.
His royal duties restricted him from working out at sea, however, he worked to develop and modernise the Scouts of Greece, which he became the president of during the 1920s.
On 4 August 1936, while George continued to neglect his role, General Metaxas overthrew the democratically elected government with a dictatorship.
Paul distanced himself from both George and Metaxas after the Scouts of Greece was forced to be integrated into the National Youth Organisation, a fascist movement supported by Metaxas.
Earlier in 1927 while visiting his mother in Austria, Paul had met Frederica of Hanover at the Hubertihaus estate.
Frederica was only ten years old at the time and called Paul, who was sixteen years older, "my uncle", as Paul was a first cousin of Frederica's mother, Princess Victoria Louise.
In 1934, Paul and Frederica met again in London at the wedding of Princess Marina of Greece and Denmark and Prince George, Duke of Kent.
The next year, Frederica met Paul in Florence while studying at the American College.
Frederica stayed with Paul's sisters during this time.
Paul's sisters were highly supportive of the relationship and attempted to encourage it, before Paul wrote to Frederica's parents, Victoria Louise and Ernest Augustus, Duke of Brunswick, and asked for their consent to marry her.
However, Ernest Augustus declined because of Frederica's young age.
Mateos Sáinz de Medrano describes Paul as having been "highly disappointed" at Ernest Augustus's response, but he did not give up on finding a spouse.
Although it is reported that Paul was looking for a Greek commoner to marry, he searched and found Frederica during his trip to Germany for the 1936 Berlin Olympic Games.
He went to the Königinvilla in Gmunden and asked Frederica's parents again if he could marry her, to which they finally agreed.
Paul and Frederica's engagement was soon announced to the public.
When Paul returned to Greece, his engagement was met with mixed reception.
Many Greeks had turned against the royal family when George consented to the Metaxas dictatorship due to his lack of interest in his role.
Many citizens were also worried of the cost of the Crown Prince's wedding due to the effects of the Great Depression, and protests against taxpayer money being spent of glamorous royal events were held across the country.
The public was also scared of the backlash from the former Allies of World War I, especially since Constantine
I's marriage to a German princess had caused the National Schism within the country.
Metaxas, however, approved of Paul’s marriage to Frederica because he hoped that it would strengthen ties between Greece and the fascist Nazi regime in Germany, led by Adolf Hitler, who wanted to use the marriage to spread influence in Greece.
George wished to distance Greece from the dynasty's German origins and was thus opposed to their marriage.
Frederica, being Hanoverian, was a close relative of the British family and had to ask permission from George VI to marry Paul, a Greek Orthodox prince.
Frederica had not arrived yet in Greece when the Church of Greece asked her to adopt a Greek name as there was no Orthodox Saint yet that had ever had her first name.
The Church explained that by choosing a Greek name, she would be able to identify with Greece's culture and religion, and would provide her with more popularity.
However, Frederica refused this request by the Holy Synod by claiming that her name was an integral part of her identity.
Frederica's insistence continued and the Church was forced to reluctantly abandon their request.
The Greek public however was arguably more shocked at the fact that swastikas, a symbol used by the Nazi Party, were present at Paul and Frederica's wedding ceremony.
To block Nazi flags, Paul and George planned to raise Greek flags and also the former Hanoverian kingdom's flags throughout the streets of Athens.
However, the former official regional flags were banned in Germany and thus Frederica opposed this because she was worried about displeasing Hitler, who she feared would threaten her parents, who resided in Germany.
In early January 1938, Frederica and her parents arrived in Greece through the country's border with Yugoslavia, where Paul and Metaxas personally greeted them.
Many Greek citizens were opposed to the wedding's high costs resulting from the accommodation and transport of high-profile guests and wedding participants, most of whom stayed at the Hotel Grande Bretagne while waiting for the wedding.
At the wedding, Paul wore the outfit of an admiral in the Greek navy and his witnesses were his nephew, the Crown Prince of Romania, and his cousin, Grand Duke Dimitri Pavlovich of Russia, along with his three brothers-in-law, the Hereditary Prince of Brunswick, Prince George William and Prince Christian Oscar.
It was redecorated by his sister, Irene, before Paul and Frederica moved in.
The government gave Frederica a small farm in Polydendri forest, near the town of Larissa in Thessaly.
Frederica soon became pregnant and gave birth to a daughter on 2 November 1938 at Psychiko Palace.
Paul and Frederica wish to name their daughter, the future Queen Sofía of Spain, Olga, but Greek naming tradition required them to name the child Sophia after Paul's mother.
On 2 June 1940, Frederica gave birth to an heir, the future Constantine II.
World War II

While Frederica was pregnant and giving birth to her three children, the last of which was Princess Irene, Nazi troops were gradually invading different countries throughout Europe, including France, which collapsed under the Nazi tactic of blitzkrieg.
Benito Mussolini launched a violent propaganda campaign against Greece and accused George of violating its neutrality by harbouring British ships within its waters.
On 15 August 1940, an Italian submarine sunk the Elli, which was escorting pilgrims from Tinos.
Germany offered mediation between Greece and Italy.
It was agreed that if George were to abdicate and Paul become the monarch, Germany would prevent an Italian invasion of Greece.
George was furious and made the Nazis write in response to Greece's actions: "They would do better not to stick their noses in the affairs of  country in they know what is good for them!"
Both the opposition, led by Plastiras, and the current government, pledged their support for George, who took charge of the Greek armed forces.
Greece automatically joined the Allies and remained in close contact with their leaders.
George held daily war council meetings at the Hotel Grande Bretagne, while Paul hosted communication links from each war front and continued his role in the navy from Athens.
Greece successfully repelled Mussolini's invasion and occupied southern Albania.
George refused to establish a national unity government and appointed the Governor of the National Bank of Greece, Alexandros Koryzis, as the new prime minister.
This gave George an even worse reputation as his decision to inaugurate Koryzis continued the dictatorship established by Metaxas in 1936.
George faced criticism not only in Greece but also by the Allies.
After several victories in Albania, Greek forces capitulated in the German invasion of Greece, which proceeded the German invasion of Yugoslavia.
By mid-April, Koryzis asked George to accept capitulation, but George refused to compromise with enemy forces.
Fearful of their impending arrests, Paul, George, other members of the royal family, and some government officials agreed to flee the mainland and land in Crete on 9 April.
George asked the British government if they could stay in British Cyprus, alongside the cabinet and some 50,000 Greek soldiers.
By 22 April, almost everyone but Paul and George had left Athens.
George and Paul set up a temporary headquarters in Chania with their cousin, Prince Peter.
George was given the title of "Number 1 enemy of the Reich in Greece" by Hitler and all three royals were forced to evacuate the island when the Fallschirmjäger commenced an attack.
Paul, George and Peter narrowly escaped the Fallschirmjäger by taking the British ship HMS Decoy from Sfakia to Alexandria, where the rest of the royal family had fled to.
In Alexandria, the Greek diaspora of Egypt welcomed Paul, George and members of the royal family with accommodation, clothing and money.
The Axis government established in occupied Greece worried Farouk of Egypt, who had many pro-Italian ministers.
George VI denied them access to the United Kingdom as he opposed Frederica's entry into the country, worried that a descendant of Wilhelm II would cause a revolt against the British monarchy, which had German roots.
After mediations, it was decided that Paul and George would stay in London, with other members of the family moving to South Africa, a British colony.
Following many requests, Paul managed to gain authority to go to Cairo and join the Free Greek Forces in August 1942, wishing to help liberate Greece.
However, there was growing republicanism in the Greek forces and thus George prohibited Paul from fighting in Greece.
Frederica moved to Cairo to be with Paul in January 1944, while their children stayed in South Africa with Smuts until March.
There, the royal couple connected with the Egyptian royal family, particularly Farida of Egypt and her children, who were of similar age to Paul.
Greece was slowly liberated through 1944 and most Greek exiles had the opportunity to return home, however, Paul and his family were forced to stay in Egypt due to the rise of republican opposition in Greece following the war.
Under the guidance of Winston Churchill and Anthony Eden, George appointed Archbishop Damaskinos of Athens as regent of the country on 29 December 1944.
George considered abdicating in favour of Paul, however ultimately remained as the monarch.
Paul believed that if he were able to return to Greece, he could have acted as the regent and prevented a republican government.
However, George ignored any calls from Paul.
The 1946 Greek referendum was held and monarchists received 68.41% of the votes, which allowed members of the Greek royal family, including Paul and George, to return.
Reign

Accession

Paul succeeded to the throne on 1 April 1947 upon the death of his childless elder brother, George II, during the Greek Civil War.
Paul and Frederica spoke English to each other and to their children despite being fluent in the Greek language.
The two girls were influenced by the teachings of Kurt Hahn, a Judo-German teacher whose ideas were commonly found as principles in royal families of German origin.
Meanwhile, the new Crown Prince, Constantine, was sent by Paul and Frederica to the Anavryta Experimental Lyceum in Marousi.
Starting in 1947, Paul and Frederica took their children to Falken, Austria, for a skiing holiday every winter, and to Petalis in the summer, where the family was lent yachts.
On these holidays, Frederica's German relatives were frequently invited, such as princes and princesses of the royal houses of Baden, Hesse, Hanover and Hohenlohe.
In 1947, Paul was unable to attend the wedding of Prince Philip to the future Elizabeth II as he was suffering from typhoid fever.
In June 1948, the wedding of Michael I of Romania and Anne of Bourbon-Parma was held in Athens.
During Paul's early reign, there was tension between certain members of the Greek royal family.
Paul and his cousin, Peter, maintained a strained relationship after the royal family accused him of entering a misalliance by marrying Irina Ovtchinnikova, a divorced Russian commoner.
Paul's aunt, Princess Alice of Battenberg, who was the mother of Prince Philip, regularly engaged in disagreements with Frederica, who she thought was clumsy and scared of her sister-in-law, Elena Vladimirovna of Russia.
Instead, Frederica held numerous talks between her and the fighting soldiers.
At a point in time, Frederica herself travelled to the Epirus frontline, which, according to Hourmouzios, boosted her popularity and branded her a "strong and courageous woman".
In response to these damages, Paul and Frederica created the Her Majesty's Fund foundation in 1947 to give financial aid to victims of the civil war.
In June 1952, Paul and Frederica made an official state visit to Turkey to ease Greco-Turkish relations.
The Turkish government invited the couple to the Hagia Sophia, a Greek Orthodox Church that had been converted into a mosque and then to a museum, but they declined, instead only visiting the tomb of Mustafa Kemal.
The state visit marked the first time a Greek head of state had made a state visit to Turkey, which had occupied Greece for over 400 years.
The following year, Yugoslav President Josip Broz Tito and First Lady Jovanka Broz privately met Paul and Frederica in Corfu.
Paul and Frederica also made state visits to the United Kingdom in 1952 and 1963, to the United States in 1953, to France and West Germany in 1956, to Switzerland in 1958, to Ethiopia and Italy in 1959, and to India and Thailand in 1963.
During his visit to the United Kingdom in 1952, Paul walked behind the coffin of George VI during his state funeral procession.
Alongside Paul were members of the British royal family, Haakon VII of Norway, Frederik IX of Denmark, Gustaf VI Adolf of Sweden and President Vincent Auriol of France.
Paul and Frederica also made trips to different regions of Greece.
Every year on 21 February, the liberation day of Ioannina, on 26 October, the liberation day of Thessaloniki, and on 30 November, the liberation day of Patras and Saint Andrew's Day, Paul and Frederica would celebrate these regional festivities.
Paul also habitually ensured that Greece's borders with its neighbours were secured.
In order to promote the then barely developed tourism on the Greek islands, Paul and Frederica invited all ruling and former ruling European royal families to a cruise between the islands in 1954, for which the shipowner Pétros Nomikós made his passenger ship Agamemnon available.
Albrecht, Duke of Bavaria, and his family took part in these trips, which is why he decided to return to Paul the Greek crown jewels of the Wittelsbach king Otto of Greece, who had been deposed in 1862.
Albrecht's son Prince Max presented these to Paul in December 1959.
It had been almost a century since they were last in Greece.
Despite Greek visits to the United Kingdom, links with Britain became strained over Cyprus, where the majority Greek population favored union with Greece, which Britain, as the colonial power, would not endorse.
The idea of a union between Greece and Cyprus became known as enosis.
Cyprus had been an issue of contention since the conclusion of the Greek Civil War and at George VI's funeral, Paul unsuccessfully attempted to host talks with the British government to achieve enosis.
The British government invited Greek and Turkish delegates to London for mediation talks on 29 August 1955.
The talks only resulted in stiff relations between Greece, Turkey, and Britain.
Paul and Greece's reputation in Turkey was then damaged by the Istanbul pogrom.
After the British government arrested Archbishop Makarios III and deported him to the Seychelles, anti-British sentiment in Greece grew as displayed through protests in some of Greece's largest cities.
The Turkish government then proposed Taksim, which would divide Cyprus between Greece and Turkey, however, both Greece and Paul opposed this idea.
On 5 February 1959, the London and Zürich Agreements established the resumption of real negotiations between Greece and Turkey, to the delight of Paul.
Economic miracle and growing authoritarianism

Greece was one of the first nations to benefit from the Marshall Plan and took advantage of American economic aid.
Between 1948 and 1952, Greece received over US$376 million in financial aid from the United States.
Economic growth was also due to growing political stability within Greece, something that Paul was greatly credited for.
In eleven years, Greece was governed by only two prime ministers, Papagos and Konstantinos Karamanlis, a record for the past few decades.
The Greek drachma stabilised, while many Greeks moved into West Germany to send back large parts of their incomes.
Economists, however, continued to worry about the fact that Greece's economy was very reliant on foreign loans and a majority of food consumed needed to be imported into the country.
Although written out as a constitutional monarchy, critics of Greece's politics claimed that the country contained traits of an authoritarian monarchy.
The cost of the monarchy was also questioned, and Paul and Frederica were accused of spending public funds for their own personal holidays and expensive lifestyle while having a lack of worry for the Greek public.
The couple were also accused of taking money from Her Majesty's Fund for their personal use.
Papandreou made the words in one of his speeches – "The king reigns, but does not govern" – his motto and boycotted several royal events.
By 1956 the King received 635,000 drachmae per month (7,620,000 annually, then worth approximately US $254,000) from the Civil list; from this he was expected to cover the costs of maintaining the Royal Palace in Athens and the Royal Yacht, as well as any private or official entertaining.
Later reign

On 2 June 1958, Crown Prince Constantine turned 18 and thus commenced his royal duties.
Constantine often shadowed Paul, who taught him the role of being the monarch.
Paul was also very weary of the struggles he and his brother faced and wished to teach Constantine ways of avoiding the types of issues they experienced.
Since the age of six, Constantine accompanied Paul in his sailing trips, and in December 1958, Paul and Frederica gifted him with his private sailboat.
Constantine trained daily with Odysseus Eskitzoglou and Georgios Zaimis.
It was marked with celebrations in Greece, being the second time Greece had won a gold medal in the Modern Olympics, the first being at the 1896 Summer Olympics and won by Spyridon Louis.
Paul was also pleased with the wedding of his eldest daughter, Sofía, to Prince Juan Carlos of Spain, who was the heir to the Spanish throne.
After having first met on the Cruise of the Kings, Sofía and Juan Carlos reunited at the Rome Olympics, where their relationship and future marriage was pathed.
In early 1963, Frederica was invited to attend the wedding of Princess Alexandra of Kent and Angus Ogilvy.
Karamanlis feared that their attendance at the British royal wedding would create public uproar and opposition.
However, Frederica did not listen to his advice and when she arrived in London, English tabloids released photos from the 1930s that showed Frederica and her brothers in the Hitler Youth uniform, describing her as a right-wing extremist with an iron fist.
Protests against Frederica were held in the United Kingdom, however few were in Greece.
Papandreou and his allies used it as an opportunity to claim that the lack of protests in Greece was because the monarchy had restricted freedom of speech, saying that Greece had committed "crimes".
Communist Betty Ambatielos, whose husband had been imprisoned, organised violent demonstrations in London outside the hotel that Frederica was staying in.
Frederica is forced to escape with members of the public who support her.
Paul soon became medically restricted to Tatoi, where Frederica took care of him, while Constantine urgently travelled to Tinos to bring a holy icon.
Paul's funeral was held on 11 March 1964 and was attended by his family, as well as Prince Philip, Duke of Edinburgh, Umberto II of Italy, Infante Juan, Count of Barcelona, Gustaf VI Adolf of Sweden, American First Lady Bird Johnson, Simeon II of Bulgaria, Rainier III of Monaco and former American President Harry Truman.
Paul was buried in the Tatoi gardens, where other deceased members of the Greek royal family are.
Paul was succeeded by his son, who became King Constantine II.
Paul's wife, Frederica, died 17 years later in 1981.
Members of the Greek and Spanish royal families were present.
In September 2020, Paul and Frederica's graves were minimally vandalised, but soon restored by the Greek government.
In popular culture

Film and documentaries

Paul appears in various films and documentaries:


Numismatics

Various coins featuring Paul were issued by the National Bank of Greece:


Philately

Various stamps featuring Paul were issued by the Hellenic Post:


Honours

Marriage and issue

On 9 January 1938, Paul married Princess Frederica of Hanover, his first cousin once removed through Frederick III, German Emperor, and Victoria, Princess Royal, and second cousin through Christian IX of Denmark, in Athens.



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
  AssignClass (cb013a6e-ebf9-4104-9a95-5e4e16b4d69c)
 Call ID: cb013a6e-ebf9-4104-9a95-5e4e16b4d69c
  Args:
    type: :Man
    source: Paul
  AddLiteral (7a7d8f99-2481-4302-a28a-1e08eb3fd95e)
 Call ID: 7a7d8f99-2481-4302-a28a-1e08eb3fd95e
  Args:
    literal_type: xsd:integer
    source: Paul
    literal_value: 1901
    relation: :hasBirthYear
  AddLiteral (5b59ab42-bf14-408b-9acb-dc22f3a77c81)
 Call ID: 5b59ab42-bf14-408b-9acb-dc22f3a77c81
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1964
    source: Paul
  AssignClass (e95e7509-3021-494e-a070-96c9c2d1139a)
 Call ID: e95e7509-3021-494e-a070-96c9c2d1139a
  Args:
    type: :Man
    source: Constantine
  AssignClass (f62d4c64-01f7-495e-ad3d-789d47326b14)
 Call ID: f62d4c64-01f7-495e-ad3d-789d47326b14
  Args:
    source: Sophia
    type: :Woman
  AddTriple (c595cda1-3e77-4da4-83da-371ee682fb02)
 Call ID: c595cda1-3e77-4da4-83da-371ee682fb02
  Args:
    target: Constantine
    relation: :hasFather
    source: Paul
  AddTriple (d4489ac5-d26b-45b2-ae47-be26ad205886)
 Call ID: d4489ac5-d26b-45b2-ae47-be26ad205886
  Args:
    relation: :hasMother
    source: Paul
    target: Sophia
  AssignClass (715a10c3-e4d6-4404-bb54-a345ff138f9c)
 Call ID: 715a10c3-e4d6-4404-bb54-a345ff138f9c
  Args:
    source: Frederica
    type: :Woman
  AddLiteral (4acb9491-b8aa-4b78-b4db-409722cae859)
 Call ID: 4acb9491-b8aa-4b78-b4db-409722cae859
  Args:
    literal_type: xsd:integer
    source: Paul
    literal_value: 1938
    relation: :hasMarriageYear
  AddTriple (70a47ad9-04a3-4af8-bd42-91416a0ba81e)
 Call ID: 70a47ad9-04a3-4af8-bd42-91416a0ba81e
  Args:
    source: Paul
    relation: :hasRelation
    target: Frederica
  AssignClass (83c53a74-eab2-43a9-aa61-c850c2413ff5)
 Call ID: 83c53a74-eab2-43a9-aa61-c850c2413ff5
  Args:
    source: ConstantineII
    type: :Man
  AssignClass (32f815ef-765d-4efa-b663-1ebf18c191be)
 Call ID: 32f815ef-765d-4efa-b663-1ebf18c191be
  Args:
    source: Sofia
    type: :Woman
  AssignClass (cacdc853-efb1-489b-8426-9ffe96f4fc43)
 Call ID: cacdc853-efb1-489b-8426-9ffe96f4fc43
  Args:
    type: :Woman
    source: Irene
  AddTriple (4c5f94d2-57cc-414a-b188-ba5715a33944)
 Call ID: 4c5f94d2-57cc-414a-b188-ba5715a33944
  Args:
    source: Paul
    relation: :hasChild
    target: Sofia
  AddTriple (da544509-1b83-492c-a00d-c1e55da5aebb)
 Call ID: da544509-1b83-492c-a00d-c1e55da5aebb
  Args:
    source: Paul
    relation: :hasChild
    target: ConstantineII
  AddTriple (250c014c-c11c-4cbb-aafe-fb62c8f1f149)
 Call ID: 250c014c-c11c-4cbb-aafe-fb62c8f1f149
  Args:
    relation: :hasChild
    source: Paul
    target: Irene
  AddTriple (278bba2c-0d89-4104-8d6e-06687c8140b7)
 Call ID: 278bba2c-0d89-4104-8d6e-06687c8140b7
  Args:
    relation: :hasChild
    source: Frederica
    target: Sofia
  AddTriple (036e2852-8494-40dd-adc2-202773503abb)
 Call ID: 036e2852-8494-40dd-adc2-202773503abb
  Args:
    relation: :hasChild
    source: Frederica
    target: ConstantineII
  AddTriple (05323bc4-ff71-48a6-8f94-faf956e737a5)
 Call ID: 05323bc4-ff71-48a6-8f94-faf956e737a5
  Args:
    target: Irene
    relation: :hasChild
    source: Frederica
  AssignClass (c4f0ff67-b20d-4d09-9d54-cc2068e993f1)
 Call ID: c4f0ff67-b20d-4d09-9d54-cc2068e993f1
  Args:
    type: :Man
    source: GeorgeI
  AddTriple (708b0187-bcee-480e-9461-efe0b8d3a701)
 Call ID: 708b0187-bcee-480e-9461-efe0b8d3a701
  Args:
    source: Constantine
    relation: :hasFather
    target: GeorgeI
  AssignClass (86f3c838-0d6c-4c9a-93da-4bc0bc0ebc4b)
 Call ID: 86f3c838-0d6c-4c9a-93da-4bc0bc0ebc4b
  Args:
    type: :Man
    source: Alexander
  AssignClass (d56c5dbe-4285-459b-82b5-fa8168a657d9)
 Call ID: d56c5dbe-4285-459b-82b5-fa8168a657d9
  Args:
    source: GeorgeII
    type: :Man
  AddTriple (46e52896-eb74-4112-974b-90db12abdc0e)
 Call ID: 46e52896-eb74-4112-974b-90db12abdc0e
  Args:
    target: Constantine
    source: Alexander
    relation: :hasFather
  AddTriple (fc7b9c45-4273-4cd2-849d-07e37b8e2de9)
 Call ID: fc7b9c45-4273-4cd2-849d-07e37b8e2de9
  Args:
    source: GeorgeII
    relation: :hasFather
    target: Constantine
  AssignClass (fc27944f-2b99-4be0-9a46-4ecd7db2e794)
 Call ID: fc27944f-2b99-4be0-9a46-4ecd7db2e794
  Args:
    source: Elisabeth
    type: :Woman
  AddTriple (4aa994d7-261f-4186-a89b-6ec0202cbef4)
 Call ID: 4aa994d7-261f-4186-a89b-6ec0202cbef4
  Args:
    relation: :hasRelation
    source: GeorgeII
    target: Elisabeth
  AssignClass (7aa75c0b-baea-4a32-90d7-be85ecca96fe)
 Call ID: 7aa75c0b-baea-4a32-90d7-be85ecca96fe
  Args:
    type: :Woman
    source: Helen
  AddTriple (ddd82859-c2a4-4208-9768-02ddc3a907b6)
 Call ID: ddd82859-c2a4-4208-9768-02ddc3a907b6
  Args:
    target: Constantine
    source: Helen
    relation: :hasFather
  AssignClass (b6fc73d4-a167-414f-8ada-0b5101b64ba7)
 Call ID: b6fc73d4-a167-414f-8ada-0b5101b64ba7
  Args:
    source: Katherine
    type: :Woman
  AddTriple (113972d1-7121-4284-80c1-1735d735a43d)
 Call ID: 113972d1-7121-4284-80c1-1735d735a43d
  Args:
    relation: :hasFather
    source: Katherine
    target: Constantine
  AssignClass (2fe2dcdc-6dd7-40a6-b4eb-90b409322c40)
 Call ID: 2fe2dcdc-6dd7-40a6-b4eb-90b409322c40
  Args:
    type: :Woman
    source: Maria
  AssignClass (623b022f-7c0f-4e01-8edb-2e831bdbbb1b)
 Call ID: 623b022f-7c0f-4e01-8edb-2e831bdbbb1b
  Args:
    source: NinaGeorgievna
    type: :Woman
  AddTriple (48accf6f-edea-4d03-8dd4-7bf14057223f)
 Call ID: 48accf6f-edea-4d03-8dd4-7bf14057223f
  Args:
    target: Maria
    relation: :hasMother
    source: NinaGeorgievna
  AssignClass (4821426a-a2ef-4421-9073-ae03269f984b)
 Call ID: 4821426a-a2ef-4421-9073-ae03269f984b
  Args:
    type: :Man
    source: PrinceAndrew
  AssignClass (084f10ba-769b-48cc-a37c-98c78d72609a)
 Call ID: 084f10ba-769b-48cc-a37c-98c78d72609a
  Args:
    type: :Man
    source: PrinceChristopher
  Finish (24b9f26c-1384-4bff-b2a9-8bf1819ed71b)
 Call ID: 24b9f26c-1384-4bff-b2a9-8bf1819ed71b
  Args: