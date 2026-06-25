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
George II (Greek: Γεώργιος Β', romanized: Geórgios II; 19 July  1890 – 1 April 1947) was King of Greece from 27 September 1922 until 25 March 1924, and again from 25 November 1935 until his death on 1 April 1947.
The eldest son of King Constantine I of Greece and Princess Sophia of Prussia, George followed his father into exile in 1917 following the National Schism, while his younger brother Alexander was installed as king.
Constantine was restored to the throne in 1920 after Alexander's death, but was forced to abdicate two years later in the aftermath of the Greco-Turkish War.
Greece was proclaimed a republic in March 1924 and George was formally deposed and stripped of Greek nationality.
Greece was overrun following a German invasion in April 1941, forcing George into his third exile.
At the end of the war, George returned to Greece after a 1946 referendum had preserved the monarchy.
Early life

Birth and childhood

George was born at the royal villa at Tatoi, near Athens, the eldest son of Crown Prince Constantine of Greece and the crown princess, Sophia of Prussia.
George was named after his paternal grandfather, King George I of Greece, following traditional Greek naming practices.
George was the eldest of six siblings, born between 1890 and 1913, and spent most of his childhood in Athens in a villa on Kifisias Avenue.
As a child, George also made numerous visits to Great Britain, where he stayed for several weeks to visit his British relatives.
George also made visits to Germany to see his mother's family and they stayed in Schlosshotel Kronberg with his grandmother Victoria, but also took summer holidays in Corfu and Venice, travelling on their private yacht, Amphritrite IV.
George has been described by historians John Van der Kiste and Vicente Mateos Sáinz de Medrano as the most introverted and distant of his siblings, having been aware of his role as heir from a young age.
Van der Kiste presents George as a child who often misbehaved, especially during visits to Germany, but less turbulent than his younger brother, Alexander, who was described as mischievous, and less sporty than his younger sister, Helen, who was seen as a tomboy.
Goudi coup and Balkan Wars

George pursued a military career, training with the Prussian Guard at the age of 18, then serving in the Balkan Wars as a member of the 1st Infantry Regiment.
George received a military education as the heir to the throne.
He was trained at the Hellenic Military Academy in Athens, which allowed him to enroll in Greece's infantry as a second lieutenant on 27 May  1909.
However, a few months after he joined, on 15 August  1909, a group of military officers organised a coup d'état against George I, the concurrent king and grandfather of George.
However, it is argued by Van der Kiste that many of the officers involved in the coup blamed the high-ranking princes for the defeat of Greece in the 1897 Greco-Turkish War.
They particularly placed blame on George's father, Crown Prince Constantine, believing that the royal family was monopolising the highest army positions.
Some of the officers involved in the coup believed that the country would be better off if King George I was deposed and replaced by another neutral candidate, such as by George, his grandson.
However, George was the most desirable candidate as he was more popular than his father, was an adult and was politically inexperienced, so was seen as easily more controllable.
George, his siblings and his parents evacuated Greece and moved to Germany for three years in exile.
To avoid controversy, their exile was branded as a three-year "education leave", which was approved and so George continued his military training, but with the prestigious First Foot Guards Regiment of the Prussian army.
This period of absence from Greece reduced his popularity as a potential replacement for his grandfather.
As Greece became more politically stable as violent protests lessened, George, his siblings and his parents returned to Greece at the end of 1910.
In 1911, Prime Minister Eleftherios Venizelos allowed members of the royal family to be given back their former ranks in the military, but George returned to Germany to continue training with the Prussian army.
When the First Balkan War commenced in October 1912, George returned to Greece to fight against the Ottoman Empire.
George and his brother, Alexander, served as officers on his father's staff.
George served in numerous battles, which was criticised by the media as it put the country's future monarch as risk of being killed.
One such battle that George participated in was the capture of Thessaloniki on 8 November  1912, which marked major progress for Greece in the war.
On 18 March  1913, George's grandfather and the reigning king, George I, was assassinated while taking his daily walk in Thessaloniki.
Crown Prince Constantine, whose popularity had grown due to Greece's successes in the First Balkan War, acceded to the throne as King Constantine I. George thus became the Crown Prince of Greece at age 23.
In the early weeks of being crown prince, George and his family moved to their new residence, where George developed a close friendship with his uncle, Prince Christopher, who was only two years older than him.
On 30 June  1913, the Second Balkan War broke out between Bulgaria and its former allies, which included Greece.
Relations between Greece and many of its Balkan allies grew during the war, notably with Romania, which paved the way towards the marriage between George and Elisabeth, the daughter of King Ferdinand I and Queen Marie of Romania.
When Greece and its allies won the war in August 1913, George and his family resumed their European trips.
George accompanied his father on a state visit to Berlin and received the Order of the Red Eagle from his uncle, Wilhelm II, the German Kaiser.
The following summer, George travelled to the United Kingdom with Christopher and was in London when he heard of the assassination of Archduke Franz Ferdinand of Austria on 28 June 1914.
The assassination sparked the outbreak of World War I, in which Constantine wished to maintain Greece's neutrality.
Constantine believed that Greece was unready to fight after its involvement in the Balkan Wars and also feared displeasing his brother-in-law, Wilhelm II.
Opposition soon accused Constantine of supporting the Triple Alliance, made up of Germany, Austria-Hungary and Italy, and relations between him and Venizelos, who believed that Greece should side with the Triple Entente, made up of Great Britain, France and Russia, quickly deteriorated.
Central Greece was occupied by the Western Allies, an extension of the Triple Entente, and a National Schism between supporters of Constantine and supporters of Venizelos broke out.
Constantine refused to alter his opinion and his popularity heavily decreased.
Though George was not present at the time, his younger sister, Princess Katherine, who was only three years old, was carried into the palace woods for two kilometres to be saved.
On 19 June  1917, French politician and leader of the Entente Charles Jonnart ordered George's father, Constantine, to abdicate.
Due to worry of the impending Allied invasion at Piraeus, Constantine agreed to be placed in exile without having to abdicate.
The Allies were against establishing a republic in Greece and thus looked for a replacement.
George's name was put forward, but the Allies perceived him as a germanophile, like his father, due to his links to the Prussian army and German imperial family.
George's uncle, Prince George, was offered the position, but he refused out of loyalty to Constantine.
Ultimately, George's younger brother, Alexander, was chosen by Venizelos and the Entente to replace Constantine.
On 10 June  1917, Alexander officially ascended to the throne in a small ceremony that was only attended by George and former prime minister Alexandros Zaimis.
In addition, Theocletus I , the Archbishop of Athens and All Greece, did not attend.
Neither Constantine nor George had renounced their rights to the throne, and Constantine told Alexander that he viewed him as the country's regent, not monarch.
George and all other members of the royal family had planned to leave for exile, however crowds of people protested outside the mansion to prevent them from leaving, so they had to escape in secret the following day.
This was the final time that George had contact with his brother, Alexander.
First exile

George and his family settled in Switzerland, first in Saint Moritz and then in Zürich.
Almost all members of the royal family moved with them after Venizelos returned to power as head of the Cabinet and organised Greece's entry into World War I.
The family were financially strained and Constantine soon became ill.
At the Treaty of Sèvres and Treaty of Neuilly-sur-Seine, part of the end of World War I, Greece made territorial gains in Thrace and Anatolia.
Although initially seen as gains to the country, Greece soon fell into the Second Greco-Turkish War in 1919.
According to historian Marlene Eilers Koenig, George was in love with his cousin Anastasia de Torby, however their relationship was opposed by George's mother, Sophia, as Anastasia was the result of a morganatic marriage.
George later became engaged in October 1920 to Elisabeth of Romania, who had been in touch with George since 1911.
George had previously asked Elisabeth to marry in 1914, but she declined off the advice of her great-aunt, Elisabeth of Wied, who thought of George as being two small and too English.
Elisabeth herself had declared that George was a prince whom God had forgotten to complete.
Although George's family had lost most of their wealth in exile, the Romanian royal family swiftly invited George and Elisabeth to return to Bucharest, in Romania, to announce their engagement.
Greco-Turkish war

George was in Romania when Alexander died following an infection from a monkey bite in 1920.
Parliament continued to refuse the crown to either George or Constantine, so it was offered to Constantine's third son, Paul, who refused to break the legitimate line of succession.
Greece was making no progress in the Greco-Turkish War and in the 1920 Greek legislative election, Venizelos was voted out of office.
Dimitrios Rallis, a monarchist, was appointed prime minister and the 1920 Greek referendum restored Constantine to the throne.
According to Van der Kiste, the referendum was most likely rigged by Rallis.
Before Venizelos fled to Constantinople in exile, he asked George's grandmother, Olga Constantinovna, to act as regent while Constantine returned to Greece.
On 19 December, George returned to Greece as the crown prince under his father's second reign.
A few weeks later, on 27 February  1921, George married Elisabeth in Bucharest.
Two weeks later, George's younger sister, Helen, married Elisabeth's brother, Crown Prince Carol of Romania, in Athens.
Constantine's restoration to the Greek throne was opposed by the former Allies of World War I, and thus Greece received minimal support in the Greco-Turkish War against Mustafa Kemal's Turkey.
The former Allies stated that they were not ready to provide support, and continued to hold distaste against Constantine.
For example, at the wedding of Princess Helen and Crown Prince Carol, the British ambassador and his wife refused to greet Constantine and Sophia.
In response to the ongoing war, Constantine quickly assumed the role of commander-in-chief of the army and resided in Asia Minor from May to September 1921.
George served as a colonel, and later a major general in the war.
Greece was pushed back from the Anatolian lands granted to them in the Treaty of Sèvres to Ankara and suffered heavy defeats at the Battle of Sakarya in August and September 1921.
The royal family became more criticised and Greek media turned against George and two of his uncles when they made comments critiquing Venizelos.
Prince Andrew, the father of the future Prince Philip, Duke of Edinburgh, fled from Asia Minor before Greece's defeat at Sakarya, which was mocked by Turkish forces.
In the next few months, Greek forces continued to be defeated and slowly retreated towards Smyrna, while George was stationed in Ionia and Elisabeth joined the Red Cross to help Christian refugees who had escaped villages that had fallen to the Turkish army.
Elisabeth's distance from George furthers her struggles of integrating into the Greek culture.
Elisabeth had been pregnant since her and George's marriage, but suffered a miscarriage while travelling to Smyrna.
Though George and Elisabeth's mother were attempting to convince her to return to Greece, her health never fully recovered after her miscarriage.
When the Turks again defeated Greece at the Battle of Dumlupınar, a sector of the military, led by colonels Nikolaos Plastiras and Stylianos Gonatas, demanded the abdication of Constantine and the dissolution of the parliament.
To avoid more unrest, Constantine officially abdicated on 27 September  1922 and moved to Italy with Sophia and his daughters in exile, while George became monarch.
George left for Bucharest to retrieve his wife and the pair returned to Greece to be crowned.
George officially ascended to the throne as George II, but did not receive a happy reception and faced harsh criticism.
In Greece, there had been greater political instability since the 1922 Greek coup d'état, which influenced Constantine's abdication, and a large influx of refugees from Asia Minor as a result of the war.
George and Elisabeth were confined to Tatoi and were highly monitored by the government, while George worried about the growing instability in Greece and criticism from the former Allies, who had previously refused to recognise Constantine's second reign.
All six of them had been strong supporters of the monarchy and their executions were to the dismay of George, who had lost his right to pardon and could not intervene in the trial.
The Greek government was criticised by George V of the United Kingdom, Alfonso XIII of Spain and Pope Pius XI, before Andrew's sentence was reduced to capital banishment in order to avoid sanctions.
On 5 December , a British ship was sent to transport Andrew and his family, including the young Prince Philip, out of Greece and to Britain, to the dismay of George.
Constantine died in Palermo on 11 January 1923  without being granted a state funeral, which left George considering abdication.
General Ioannis Metaxas, who was a supporter of the monarchy, encouraged George to stay in the country with the hope that instability would gradually reduce.
Following a failed royalist coup d'état in October 1923, the Greek government, led by the republican prime minister, Gonatas, asked George to leave the country while the National Assembly considered the question of the future form of government.
Though most likely uninvolved, George was accused of initiating the coup d'état, and Plastiras and Theodoros Pangalos openly campaigned for the abolition of the monarchy for the first time.
The 1923 Greek legislative election determined that Venizelos would replace Gonatas, however before the changeover in government, Gonatas demanded that George leave the country.
George complied and although he refused to abdicate, George departed on 19 December 1923 for exile in his wife's home nation of Romania.
Before fleeing, George was described as a cold and aloof man, who rarely inspired love or affection from his subjects.
Many commented that his moody, sullen personality seemed more appropriate for his ancestral homeland of Denmark than Greece.
Furthermore, George's long years spent living abroad had caused him to struggle in identifying with the Greek culture.
George and Elisabeth were officially deposed and banished, along with all members of the royal family, who were stripped of their Greek citizenship.
Exiled in Romania from December 1923, George and his wife settled in Bucharest, where Elisabeth's parents, King Ferdinand and Queen Marie, put at their disposal a wing of the Cotroceni Palace for some time.
As regular guests of the Romanian sovereigns, George and Elisabeth took part in the ceremonies which punctuated the life of the Hohenzollern-Sigmaringen family.
Despite the kindness with which his mother-in-law treated him, George felt idle in Bucharest and struggled to hide the boredom he felt from the splendors of the Romanian court.
After their exile, financial difficulties and absence of children, George and Elisabeth's marriage deteriorated.
In exile, George stayed half the year in Romania with Elisabeth, and the other half living with his mother at Villa Bobolina in Tuscany, either with or without his wife.
George eventually moved to the United Kingdom, where he had numerous extended family members and friends.
On 16 September 1930, George was initiated into Freemasonry in London and became venerable master of the Wellwood Lodge in 1933.
After the death of Sophia in 1932, George chose to permanently leave Bucharest and his wife to establish his residence in London.
Accompanied by his squire, Major Dimitrios Levidis, and one of his servants, Mitso Panteleos, George rented a small suite with two rooms at Brown's Hotel in Mayfair.
George still lacked much wealth and received a mixed reception in Britain, where he was criticised for his relations with Wilhelm II.
In London, George was finally reunited with Andrew and his wife.
George also regularly attended hunting trips in Scotland with his companions and members of the British royal family, who he frequently went to pubs and antique dealers with.
George became quite knowledgeable in old furniture and English silverware.
George avoided mentioning his political views or any plans for restoring the Greek monarchy, but made himself clear that he would return as monarch if asked to and that he still considered himself Greek.
George attended the wedding of his cousin, Marina, and George, Duke of Kent, in Greek army uniform.
After the wedding celebrations had concluded, George left on a trip to British India for several months.
Under Lord Willingdon, the Viceroy and Governor-General of India, George was treated as the sovereign of Greece and met numerous officials stationed there, while being enthusiastically interested in the Indian culture.
During his stay, George fell in love with a young woman named Joyce Wallach, who was married to John Britten-Jones, the aide-de-camp to the Governor of India.
Wallach filed for divorce and moved back to London with George, however would continue to have numerous affairs up until George's death in 1947.
On 6 July 1935, George learned through the newspaper that Elisabeth had filed for divorce after she accused him of "desertion from the family home".
A court in Bucharest processed the divorce without inviting George to attend.
In just over ten years, Greece had twenty-three governments, thirteen coup d'états and one dictatorship.
Having failed to restore political stability, the republicanism movement in Greece became criticised and opposed by the public.
Although most protestors wished to have George reinstalled, there were voices to have a new monarch from a new dynasty be inducted, such as George, Duke of Kent.
Aware of Kondylis' ultimate aim of restoring the monarchy, George, who had been living at Brown's Hotel, demanded a plebiscite be held in order to determine whether he would be reinstalled.
As Time described it at the time, "As a voter one could drop into the ballot box a blue vote for George II and please General George Kondylis ... or one could cast a red ballot for the Republic and get roughed up.
When the election results were announced, a delegation was sent to the Greek embassy in London to officially ask George and his younger brother, Paul, to return to Athens, which they accepted on 5 November 1935.
Before returning to Greece, they first travelled to France and Italy.
In Paris, George and Prince Andrew were greeted by French President Albert Lebrun and interviewed by French media.
George and Paul then travelled to Villa Sparta, Italy, to retrieve their sisters and pay respects to their parents' graves at the Church of the Nativity of Christ and St. Nicholas, a Russian Orthodox Church in Florence.
Kondylis lost his status as Regent of Greece, but ensured that George kept him as prime minister, before awarding him with the Grand Cross of the Order of George I. Almost immediately after being restored, George and Kondylis disagreed over the terms of a general amnesty that George wanted to declare, so Kondylis resigned on 30 November 1935 and George appointed Konstantinos Demertzis as interim prime minister.
In the election, the Communist Party of Greece (KKE) gained fifteen seats, which established it as a buffer between monarchists and republicans.
George appointed Metaxas as prime minister on 13 April 1936.
Metaxas also told George that he wished to suspend certain articles of the constitution in order to establish a dictatorship.
Metaxas dictatorship

On 4 August 1936, George endorsed Metaxas's dictatorship, known as the "4th of August Regime", signing decrees that dissolved the parliament, banned political parties, abolished the constitution and purported to create a "Third Hellenic Civilization".
George, ruling jointly with Metaxas, oversaw a right-wing regime in which political opponents were arrested and strict censorship was imposed.
George disliked dealing with both Greek politicians and ordinary Greeks, and preferred to let Metaxas undertake tours around the country..
George retained full control of the army and he was largely responsible for foreign policy making.
Although his reign was mostly guaranteed under the dictatorship, George was weary of Metaxas' growing power and the influence of the army.
George told his cousin, Princess Victoria Louise of Prussia, that he felt so isolated that he could not trust anyone in Greece.
To avoid a possible overthrow by Metaxas, George declared to the Greek ambassador to the United Kingdom that he supported Metaxas's policies, though he also voiced his concern.
They are the most democratic people in the world, but once they take power, they automatically become tyrannical.
— George II to the Greek ambassador to the United Kingdom.
Most of the royal family's possessions had been either ransacked, lost or sold during the republic.
When the monarchy was restored, George nor any member of the royal family requested compensation for their lost property.
Lacking wealth, George took charge of the restoration and redecoration works of his residencies, which he refurnished by gaining items from auctions and markets.
George continued his relationship with Wallach, but it was kept secret from the public and any possible marriage between the pair would not be allowed due to Wallach's commoner status.
When engagements required a first lady to be present, George would call his sister Katherine or his sister Irene, who were both single at the time.
George made very frequent visits back to London, at least once every year, typically at the end of the year, to reunite with his extended family and friends.
He was weary of Metaxas when taking these trips and would never be away from Greece for too long.
His trips though allowed for the acquisition by Greece of more military equipment and vehicles from Britain.
One of George's priorities was to retrieve the bodies of his mother and father from Italy.
In November 1936, he sent Paul to Florence to recover the bodies of their parents, Constantine and Sophie, and of their grandmother, Olga.
They were transferred to Greece by the ship Averof and exhibited for the public for six days in the Metropolitan Cathedral of Athens.
It was attended by members of the royal family and foreign European royals and nobles.
George would go on, in 1940, to retrieve the remains of his aunt, Alexandra, who had died in Russia in 1891, from the Soviet Union.
With George's divorce, his relationship with a commoner and his lack of offspring, Paul assumed the role of heir apparent to the throne, however he too was still single.
After facing pressure to marry, Paul wedded Frederica of Hanover, the daughter of his cousin, Victoria Louise, and Ernest Augustus, Duke of Brunswick, on 9 January 1938.
Though a notable amount of dignitaries were in Athens for their wedding, many Greeks feared having another queen who was German and who was the granddaughter of Wilhelm II.
George was quick to oppose this and managed to avoid any Nazi influence on the day.
On 1 July 1939, George's sister, Irene, married Prince Aimone, Duke of Aosta, a cousin of Victor Emmanuel III and the future King of Croatia.
As a result, George threatened to boycott the ceremony, but Metaxas advised him to attend to avoid further deterioration in Greco-Italian relations.
World War II

Home front

On 2 June 1940 Frederica gave birth to the future Constantine II.
Mussolini commenced a violent propaganda campaign against Greece and accused George, who had declared Greece's neutrality, of harbouring British ships in Greek waters.
The Nazi government in Germany proposed mediation between Italy and Greece.
Hitler promised that if George, who he saw as an anglophile, abdicated from the throne, Germany would guarantee no Italian invasion of Greece and grant Greece territories off the coast of the Balkans.
George was outraged at this proposition and stated, " would do better to not stick their noses in the affairs of this country if they know what is good for them!"
Plastiras, head of the opposition-in-exile, proclaimed their support of George and Metaxas.
George consequentially took charge of Greek armed forces and established contact with the Allies, while conducting daily war council meetings at the Hotel Grande Bretagne.
George travelled up north to support soldiers as well.
Greece successfully repelled the Italian invasion and launched a successful counter-attack, eventually occupying the southern half of Italian Albania.
Metaxas died on 29 January 1941 and George refused to set up a government of national unity, despite calls from both wings of politics to do so.
George appointed Alexandros Koryzis as the new prime minister and he retained the dictatorial power that Metaxas did.
Koryzis told George to accept capitulation, but George reportedly burst into anger and gave his intentions of never surrendering.
Following Koryzis' suicide on 18 April 1941 in the face of the rapid German advance, George unable to find a speedy successor, found himself as the de facto head of government as well as head of the armed services.
George had thus a unique opportunity to form a broader government of national consensus, and abolish the hated dictatorial regime—whose sole bastion of support he now was.
Though urged to this step by the influential British ambassador, Michael Palairet, George refused.
George initially proposed Konstantinos Kotzias, one of Metaxas's ministers, but his ties to the regime made him an unfeasible choice.
Finally, Emmanouil Tsouderos, former governor of the Bank of Greece, was chosen, chiefly on account of his known Anglophile sentiments, Venizelist past, and Cretan origin-where with mainland Greece being overrun, the government was preparing to evacuate too.
Most Cretans supported Venizelos but were generally seen as anti-monarchical, this appointment was seen as a sop to local sentiment.
On 22 April most members of the royal family were evacuated from the Greek mainland to Crete, but George and Paul remained in Athens until the next day, when they and the government too fled.
George established headquarters in Chania, a few weeks before a German airborne attack.
Hitler had named George the "number one enemy of the Reich in Greece" and George had narrowly escaped German paratroopers, so he decided that the royals and the government were to evacuate.
For his actions on Crete, George was awarded with the Distinguished Service Order, becoming the only monarch in history to be decorated with the award.
King-in-exile

Throughout the Axis occupation, George remained the internationally recognised head of state, backed by the Greek government-in-exile and the Free Greek Forces.
However, the British Foreign Office found George exceedingly difficult to deal with.
He was deeply obstinate about upholding what he regarded as his royal prerogatives.
As late as 1942, George kept on Cabinet ministers from the Metaxas regime, most notably Maniadakis.
The Greek royals' presence in Egypt upset Farouk of Egypt and his pro-Italian ministry, forcing George to find a new place of refuge for the family.
George VI of the United Kingdom opposed having Frederica in Britain out of worry that she would bring attention to the British royal family's German origins.
After deliberation, George and Paul only were granted permission to reside in London, with the rest of the family relocating to Cape Town, South Africa.
George, Wallach, Paul and Levidis stationed themselves at Claridge's in Mayfair.
George and Tsouderos organised with Winston Churchill and the British Cabinet the placement of Greek troops in the Middle East and the purification of the Greek army by eliminating communist and Venizelist ideals.
On 22 October 1941, George finally, yet reluctantly, drafted with his Cabinet-in-exile, due to pressure from the British government and republican Greek opposition, a decree that would establish a new parliamentary regime and the dissolution of Metaxas's dictatorship by restoring the previously abolished articles; articles 5, 6, 10, 12, 14, 20 and 95.
The following month, George and Tsouderos returned to Egypt to organise Greek troops and stayed there until June.
George travelled to the United States and met with President Franklin D. Roosevelt, before flying to London and then Cairo.
Perhaps deeply paranoid and insecure, George believed that the British government was plotting to prevent his return to Greece, despite all of the evidence to the contrary.
George repeatedly asked that Soteriadis be replaced with a monarchist.
One of George's few friends was Churchill, who was determined to see him restored and often backed the king's complaints against his own officials.
In occupied Greece, however, the leftist partisans of the National Liberation Front (EAM) and National Popular Liberation Army (ELAS), now unfettered by Metaxas's oppression, had become the largest Greek Resistance movement, enjoying considerable popular support.
As liberation drew nearer however, the prospect of George's return caused dissensions both inside Greece and among the Greeks abroad.
In November 1943, George wrote to Tsouderos, "I shall examine anew the question of the date of my return to Greece in agreement with the Government".
Either deliberately or accidentally, the version released for publication omitted the words "of the date", creating the impression that George had agreed to a further plebiscite on the monarchy, even though a retraction was issued.
After Italy joined the Allies on 8 September 1943, communists in Greece seized weapons of the Axis and gained territorial power within the country.
There were growing calls for George to hold a referendum and appoint a regent before he returned to Greece.
It was suggested that the regent be the Archbishop of Athens and All Greece, Archbishop Damaskinos, who was a strong supporter of republicanism, and thus George heavily opposed this.
Communists became the monarchy's main political opponent and a rival communist-led government, called the Political Committee of National Liberation, was established in occupied Greece and a pro-EAM mutiny, the 1944 Greek naval mutiny, among the armed forces in the Middle East, occurs.
On 8 April 1944, Tsouderis resigned and George appointed the liberal Sophoklis Venizelos.
However, when Venizelos is discovered to have been involved in the mutiny, George appoints Georgios Papandreou as prime minister and Papandreou selects a Cabinet made up of multiple republican ministers.
George was very much opposed to a regency, and tried his best to turn Churchill against Archbishop Damaskinos, accusing him of being a communist and a Nazi collaborator.
Finally, Greece is liberated from the Axis.
As late as Christmas Eve 1944, during the height of the Dekemvriana, George had rejected the compromise solution of a regency, demanding that he return to Greece at once to reclaim his throne.
George's private secretary recalled, "I could hear through the door the voices of Churchill and Eden, particularly the latter, raised in anger at the king.
Bowing to pressure, George was forced to appoint Archbishop Damaskinos of Athens as regent in January 1945.
Ailing, exhausted and powerless, George bought a lease on a house in Chester Square, Belgravia, and made a home there with Wallach, his long-time mistress.
Return to Greece

Though World War II was over, political instability in Greece remained very high.
The announced results claimed 68.4% in favour of George's return on an 86.6% turnout.
"


The new prime minister, Konstantinos Tsaldaris, went to London to invite George II back to Greece.
On 27 September, George returned to Elefsina, Greece, and met with Paul and Frederica.
From there, they and other members of the royal family travelled to Athens and were greeted by a large crowd and a Te Deum, celebrated by Damaskinos.
George returned to find Tatoi Palace looted, the surrounding woods chopped down for fuel and corpses buried in shallow graves outside.
With his residencies having been badly damaged, George moved into a cottage built for his father.
George attempted to depict his lifestyle as modest during a time of high rationing, and spent most of his time working in his office and opening letters addressed to him.
While the Greek Civil War began raging in the north, the Paris Peace Treaties on 10 February 1947 allows Greece to annex the Dodecanese islands, which had been Italian territories since the Italo-Turkish War between 1911 and 1912.
George proclaimed Admiral Perikles Ioannidis, the second husband of his aunt, Maria, as the first governor of the Dodecanese.
George also aimed to annex Northern Epirus and a resolution vote by the American Senate approved this, but he was ultimately unsuccessful.


Death

From the announcement of Princess Katherine's engagement to British Major Richard Brandram, George's health began declining without his doctors being concerned.
On 31 March 1947, George attended a performance of Laurence Olivier's Henry V at the British embassy in Athens as part of a charity gala.
At lunch the following day, George told a servant that he felt tired.
He was then discovered unconscious in his office in the New Royal Palace in Athens on 1 April 1947.
At 4:00 pm, George's death was announced on the radio and his cause of death was given as arteriosclerosis.
George's nephew, Constantine, thus became the crown prince.
In popular culture

War propaganda

During World War II, the Allies used the figure of George II as an instrument of propaganda to reinforce Greek patriotic sentiment.
Several short films centred on the sovereign and his government were thus shot, such as Heroic Greece!
Television and literature

The romantic relationship of King George II and his mistress, nicknamed "Mrs. Brown", is briefly mentioned in the third episode ("The New King") of the British mini-series Edward & Mrs. Simpson, which features the king's cruise with Edward VIII and Wallis Simpson in the Greek Islands, in 1936.
In addition, George is depicted in the English detective novel, A Royal Affair (1920), by Allisan Montclair.
Music

On the occasion of the restoration of George II as monarch in 1935, the rebetiko singer Markos Vamvakaris wrote a song titled "We welcome you, King" (Greek: Καλώς μας ήρθες Bασιλιά, romanized: Kalós mas írthes Vasiliá).
Philately

Various stamps bearing the effigy of George II have been issued by Greek Post during his reign:


Numismatics

Various Greek coins bearing the image of George II have been issued by the Bank of Greece.



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
  AssignClass (761c1769-70ad-47b2-b44c-2825d725c61c)
 Call ID: 761c1769-70ad-47b2-b44c-2825d725c61c
  Args:
    source: George_II_of_Greece
    type: :Man
  AssignClass (617022a3-2522-42e5-a0a7-a9aa4731f8ba)
 Call ID: 617022a3-2522-42e5-a0a7-a9aa4731f8ba
  Args:
    source: George_II_of_Greece
    type: :Person
  AddLiteral (ab273fc8-afdd-4874-a5fd-3d94ea285077)
 Call ID: ab273fc8-afdd-4874-a5fd-3d94ea285077
  Args:
    relation: :hasBirthYear
    source: George_II_of_Greece
    literal_type: xsd:integer
    literal_value: 1890
  AddLiteral (4fc1ce1a-5a7e-40f1-9bee-4080f928738f)
 Call ID: 4fc1ce1a-5a7e-40f1-9bee-4080f928738f
  Args:
    literal_value: 1947
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: George_II_of_Greece
  AssignClass (1e0e44f5-9f7a-4ad5-98a4-badbc261d6ab)
 Call ID: 1e0e44f5-9f7a-4ad5-98a4-badbc261d6ab
  Args:
    source: Constantine_I_of_Greece
    type: :Man
  AssignClass (a81e6d2d-3260-404b-b5ab-387a2c1da5b3)
 Call ID: a81e6d2d-3260-404b-b5ab-387a2c1da5b3
  Args:
    source: Constantine_I_of_Greece
    type: :Person
  AssignClass (fb7c3ca6-6149-44e0-9efc-cf6f48ada9bf)
 Call ID: fb7c3ca6-6149-44e0-9efc-cf6f48ada9bf
  Args:
    source: Sophia_of_Prussia
    type: :Woman
  AssignClass (17dbe673-4a99-4812-b716-0e64edaa9786)
 Call ID: 17dbe673-4a99-4812-b716-0e64edaa9786
  Args:
    source: Sophia_of_Prussia
    type: :Person
  AddTriple (78b9e939-bd93-4594-a7be-7ceac5cd2487)
 Call ID: 78b9e939-bd93-4594-a7be-7ceac5cd2487
  Args:
    target: Constantine_I_of_Greece
    relation: :hasFather
    source: George_II_of_Greece
  AddTriple (14b3b5c7-9203-4e8b-8b67-f60d4a0a84d4)
 Call ID: 14b3b5c7-9203-4e8b-8b67-f60d4a0a84d4
  Args:
    target: Sophia_of_Prussia
    relation: :hasMother
    source: George_II_of_Greece
  AssignClass (e138e1ab-35b6-4ce4-839a-7cc06fdb0bb1)
 Call ID: e138e1ab-35b6-4ce4-839a-7cc06fdb0bb1
  Args:
    source: Alexander_of_Greece
    type: :Man
  AssignClass (3f326c70-8c1b-489a-8ba6-fd6b43164f06)
 Call ID: 3f326c70-8c1b-489a-8ba6-fd6b43164f06
  Args:
    source: Alexander_of_Greece
    type: :Person
  AddTriple (8f8ed63c-17ef-44ce-bbf7-d94a948fca5d)
 Call ID: 8f8ed63c-17ef-44ce-bbf7-d94a948fca5d
  Args:
    relation: :isBrotherOf
    source: Alexander_of_Greece
    target: George_II_of_Greece
  AssignClass (717aede0-6f72-42f6-8bb8-f8c15a667462)
 Call ID: 717aede0-6f72-42f6-8bb8-f8c15a667462
  Args:
    source: George_I_of_Greece
    type: :Man
  AssignClass (4ed7d40f-c5b5-4fcd-935f-3467b8dac859)
 Call ID: 4ed7d40f-c5b5-4fcd-935f-3467b8dac859
  Args:
    source: George_I_of_Greece
    type: :Person
  AddTriple (aeddef13-3708-4af9-b7dd-0993c2c45cd4)
 Call ID: aeddef13-3708-4af9-b7dd-0993c2c45cd4
  Args:
    relation: :hasFather
    source: Constantine_I_of_Greece
    target: George_I_of_Greece
  AssignClass (c56f6621-d34a-4e0a-89b7-17356449839f)
 Call ID: c56f6621-d34a-4e0a-89b7-17356449839f
  Args:
    source: Katherine_of_Greece
    type: :Woman
  AssignClass (64586469-fd40-4e57-b456-096b00023704)
 Call ID: 64586469-fd40-4e57-b456-096b00023704
  Args:
    source: Katherine_of_Greece
    type: :Person
  AddTriple (0241b20a-93f9-49e2-bc2a-8fbc99e73b94)
 Call ID: 0241b20a-93f9-49e2-bc2a-8fbc99e73b94
  Args:
    relation: :isSisterOf
    source: Katherine_of_Greece
    target: George_II_of_Greece
  AssignClass (f236d24d-4ff4-4c94-84a9-312abeadc8bf)
 Call ID: f236d24d-4ff4-4c94-84a9-312abeadc8bf
  Args:
    source: Helen_of_Greece
    type: :Woman
  AssignClass (7db500f5-0eed-43b3-9968-44a7edddc1cd)
 Call ID: 7db500f5-0eed-43b3-9968-44a7edddc1cd
  Args:
    source: Helen_of_Greece
    type: :Person
  AddTriple (1021cd9a-51b1-4947-bf16-578e1a05ae44)
 Call ID: 1021cd9a-51b1-4947-bf16-578e1a05ae44
  Args:
    target: George_II_of_Greece
    relation: :isSisterOf
    source: Helen_of_Greece
  AssignClass (f934b41b-036e-45d6-8cd7-bd86304f4300)
 Call ID: f934b41b-036e-45d6-8cd7-bd86304f4300
  Args:
    source: Christopher_of_Greece
    type: :Man
  AssignClass (53124f0d-34dc-4464-a49f-f51552e345fa)
 Call ID: 53124f0d-34dc-4464-a49f-f51552e345fa
  Args:
    source: Christopher_of_Greece
    type: :Person
  AddTriple (e152535e-f2da-4b1e-acbf-e24528fc5ff9)
 Call ID: e152535e-f2da-4b1e-acbf-e24528fc5ff9
  Args:
    source: Christopher_of_Greece
    relation: :isBrotherOf
    target: Constantine_I_of_Greece
  AssignClass (9da42721-a85c-4c19-a2ce-1932fb7b61d6)
 Call ID: 9da42721-a85c-4c19-a2ce-1932fb7b61d6
  Args:
    source: Elisabeth_of_Romania
    type: :Woman
  AssignClass (316d4a38-07dc-41ed-9d85-f895b05ca767)
 Call ID: 316d4a38-07dc-41ed-9d85-f895b05ca767
  Args:
    source: Elisabeth_of_Romania
    type: :Person
  AddTriple (971ab0db-bebc-4aac-bed2-48ef46f633a8)
 Call ID: 971ab0db-bebc-4aac-bed2-48ef46f633a8
  Args:
    relation: :hasRelation
    source: George_II_of_Greece
    target: Elisabeth_of_Romania
  AddLiteral (be849c74-641e-4907-979f-36c86484925e)
 Call ID: be849c74-641e-4907-979f-36c86484925e
  Args:
    literal_value: 1921
    source: George_II_of_Greece
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (e5867444-71d6-45e5-a201-344da841f4ae)
 Call ID: e5867444-71d6-45e5-a201-344da841f4ae
  Args:
    source: Ferdinand_I_of_Romania
    type: :Man
  AssignClass (4ad39100-428c-495f-99bc-f3eceae2103e)
 Call ID: 4ad39100-428c-495f-99bc-f3eceae2103e
  Args:
    source: Ferdinand_I_of_Romania
    type: :Person
  AssignClass (3dc24d8c-7bcb-4104-bca4-60433b1de45d)
 Call ID: 3dc24d8c-7bcb-4104-bca4-60433b1de45d
  Args:
    source: Marie_of_Romania
    type: :Woman
  AssignClass (b3e985a0-621a-44b7-a273-68f277f5d51c)
 Call ID: b3e985a0-621a-44b7-a273-68f277f5d51c
  Args:
    source: Marie_of_Romania
    type: :Person
  AddTriple (b9d9c682-5e85-4543-923e-f9579f264fcf)
 Call ID: b9d9c682-5e85-4543-923e-f9579f264fcf
  Args:
    relation: :hasFather
    source: Elisabeth_of_Romania
    target: Ferdinand_I_of_Romania
  AddTriple (d8ac3c35-25e9-4dfc-8d7b-55b57b938f92)
 Call ID: d8ac3c35-25e9-4dfc-8d7b-55b57b938f92
  Args:
    target: Marie_of_Romania
    source: Elisabeth_of_Romania
    relation: :hasMother
  AssignClass (59f0d804-8560-448b-911f-1b5e02f243b3)
 Call ID: 59f0d804-8560-448b-911f-1b5e02f243b3
  Args:
    source: Paul_of_Greece
    type: :Man
  AssignClass (c21fd957-8d1f-4a6d-ad4e-4adc8bc535d1)
 Call ID: c21fd957-8d1f-4a6d-ad4e-4adc8bc535d1
  Args:
    source: Paul_of_Greece
    type: :Person
  AddTriple (8dbbc105-319b-4f0d-aff0-18cfe20d3b10)
 Call ID: 8dbbc105-319b-4f0d-aff0-18cfe20d3b10
  Args:
    relation: :isBrotherOf
    source: Paul_of_Greece
    target: George_II_of_Greece
  AssignClass (f99723b9-b9d2-408e-af48-967bef65f4cd)
 Call ID: f99723b9-b9d2-408e-af48-967bef65f4cd
  Args:
    source: Frederica_of_Hanover
    type: :Woman
  AssignClass (d95819d7-98f6-4c98-a92b-1028e17f6c8e)
 Call ID: d95819d7-98f6-4c98-a92b-1028e17f6c8e
  Args:
    source: Frederica_of_Hanover
    type: :Person
  AddTriple (19605022-1e9a-4e8a-9571-9a5294573696)
 Call ID: 19605022-1e9a-4e8a-9571-9a5294573696
  Args:
    source: Paul_of_Greece
    relation: :hasRelation
    target: Frederica_of_Hanover
  AddLiteral (287bf7b5-7a14-4bf9-a047-c5ba0cc8d5c1)
 Call ID: 287bf7b5-7a14-4bf9-a047-c5ba0cc8d5c1
  Args:
    literal_value: 1938
    source: Paul_of_Greece
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (b5a218e1-3bd5-4b25-a3b3-3a13734e64f2)
 Call ID: b5a218e1-3bd5-4b25-a3b3-3a13734e64f2
  Args:
    source: Constantine_II_of_Greece
    type: :Man
  AssignClass (e9849831-5a88-489a-89d7-b537c4ad1ba0)
 Call ID: e9849831-5a88-489a-89d7-b537c4ad1ba0
  Args:
    source: Constantine_II_of_Greece
    type: :Person
  AddTriple (a707c733-aef0-493d-874a-769494e4361d)
 Call ID: a707c733-aef0-493d-874a-769494e4361d
  Args:
    source: Constantine_II_of_Greece
    relation: :hasFather
    target: Paul_of_Greece
  AddTriple (6a12b042-d6ad-49e9-a7c3-967cbe6a0dbf)
 Call ID: 6a12b042-d6ad-49e9-a7c3-967cbe6a0dbf
  Args:
    target: Frederica_of_Hanover
    relation: :hasMother
    source: Constantine_II_of_Greece
  AssignClass (b4761bbf-da48-4098-b2b3-cf0dd062cb0b)
 Call ID: b4761bbf-da48-4098-b2b3-cf0dd062cb0b
  Args:
    source: Irene_of_Greece
    type: :Woman
  AssignClass (c0790dea-0560-4d4f-83a5-0c70c2cf4d32)
 Call ID: c0790dea-0560-4d4f-83a5-0c70c2cf4d32
  Args:
    source: Irene_of_Greece
    type: :Person
  AddTriple (f1bc31eb-3b30-40f2-930b-ce6f74ea7424)
 Call ID: f1bc31eb-3b30-40f2-930b-ce6f74ea7424
  Args:
    source: Irene_of_Greece
    relation: :isSisterOf
    target: George_II_of_Greece
  AssignClass (9d1d28bd-41af-479c-a729-8395ba3dd0dd)
 Call ID: 9d1d28bd-41af-479c-a729-8395ba3dd0dd
  Args:
    source: Aimone_Duke_of_Aosta
    type: :Man
  AssignClass (1431b850-987f-4c01-b51f-336d5036ca5c)
 Call ID: 1431b850-987f-4c01-b51f-336d5036ca5c
  Args:
    source: Aimone_Duke_of_Aosta
    type: :Person
  AddTriple (5b583b98-bd0c-4abb-8dc7-77409110bcda)
 Call ID: 5b583b98-bd0c-4abb-8dc7-77409110bcda
  Args:
    target: Aimone_Duke_of_Aosta
    relation: :hasRelation
    source: Irene_of_Greece
  AssignClass (0cd22def-dc8d-4bea-9a40-596380ce27a5)
 Call ID: 0cd22def-dc8d-4bea-9a40-596380ce27a5
  Args:
    source: Olga_Constantinovna
    type: :Woman
  AssignClass (c0d7d147-2ea1-4d78-9e77-b172415855bb)
 Call ID: c0d7d147-2ea1-4d78-9e77-b172415855bb
  Args:
    source: Olga_Constantinovna
    type: :Person
  AddTriple (90503e84-98df-495a-a560-fecaf8e41293)
 Call ID: 90503e84-98df-495a-a560-fecaf8e41293
  Args:
    target: Olga_Constantinovna
    source: Constantine_I_of_Greece
    relation: :hasMother
  AssignClass (67f3e060-eadf-4938-b871-e662fcdc65d9)
 Call ID: 67f3e060-eadf-4938-b871-e662fcdc65d9
  Args:
    source: Carol_of_Romania
    type: :Man
  AssignClass (724533a8-8131-453b-b1b6-e601466f0d27)
 Call ID: 724533a8-8131-453b-b1b6-e601466f0d27
  Args:
    source: Carol_of_Romania
    type: :Person
  AddTriple (29525660-111f-4fb1-9c59-224189f6bf2c)
 Call ID: 29525660-111f-4fb1-9c59-224189f6bf2c
  Args:
    source: Carol_of_Romania
    relation: :isBrotherOf
    target: Elisabeth_of_Romania
  AddTriple (b18e2a93-8d4d-4c92-b4f6-a89d00ad1ae9)
 Call ID: b18e2a93-8d4d-4c92-b4f6-a89d00ad1ae9
  Args:
    source: Helen_of_Greece
    relation: :hasRelation
    target: Carol_of_Romania
  AddLiteral (6456e7df-0d38-48e8-a34a-773a1d429f03)
 Call ID: 6456e7df-0d38-48e8-a34a-773a1d429f03
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Helen_of_Greece
    literal_value: 1921
  AssignClass (eac14552-a463-4bd7-a5f7-f5e2d967d91f)
 Call ID: eac14552-a463-4bd7-a5f7-f5e2d967d91f
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (26ac596e-e789-407c-9e3f-a9a724b6b6bf)
 Call ID: 26ac596e-e789-407c-9e3f-a9a724b6b6bf
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Person
  AddTriple (31844e85-4e6b-4a9e-a652-69be3b728db2)
 Call ID: 31844e85-4e6b-4a9e-a652-69be3b728db2
  Args:
    target: Victoria_Louise_of_Prussia
    relation: :hasMother
    source: Frederica_of_Hanover
  AssignClass (e2e4139b-050f-490a-a7ba-b42a7da3ba69)
 Call ID: e2e4139b-050f-490a-a7ba-b42a7da3ba69
  Args:
    source: Ernest_Augustus_Duke_of_Brunswick
    type: :Man
  AssignClass (787d7156-989d-417a-8cb6-380aca782e81)
 Call ID: 787d7156-989d-417a-8cb6-380aca782e81
  Args:
    source: Ernest_Augustus_Duke_of_Brunswick
    type: :Person
  AddTriple (e7a70279-e588-4b6a-89f6-4570b89f3172)
 Call ID: e7a70279-e588-4b6a-89f6-4570b89f3172
  Args:
    relation: :hasFather
    source: Frederica_of_Hanover
    target: Ernest_Augustus_Duke_of_Brunswick
  AssignClass (9f7c819e-58f9-4010-bca2-f808ac7237bc)
 Call ID: 9f7c819e-58f9-4010-bca2-f808ac7237bc
  Args:
    source: Alexandra_of_Greece
    type: :Woman
  AssignClass (c0a89543-44a9-4da8-82fa-8d61438ad890)
 Call ID: c0a89543-44a9-4da8-82fa-8d61438ad890
  Args:
    source: Alexandra_of_Greece
    type: :Person
  AddTriple (fd1fb006-6ead-4184-b764-86f0c467d166)
 Call ID: fd1fb006-6ead-4184-b764-86f0c467d166
  Args:
    target: Constantine_I_of_Greece
    relation: :isSisterOf
    source: Alexandra_of_Greece
  AssignClass (ad7fba61-b4db-4bb9-b8d1-016c7b6f1175)
 Call ID: ad7fba61-b4db-4bb9-b8d1-016c7b6f1175
  Args:
    source: Maria_of_Greece
    type: :Woman
  AssignClass (83386a2d-f4fb-4660-a5cc-0c6828a1b892)
 Call ID: 83386a2d-f4fb-4660-a5cc-0c6828a1b892
  Args:
    source: Maria_of_Greece
    type: :Person
  AddTriple (14d4848c-482e-4643-b0c1-1030470b2987)
 Call ID: 14d4848c-482e-4643-b0c1-1030470b2987
  Args:
    source: Maria_of_Greece
    relation: :isSisterOf
    target: Constantine_I_of_Greece
  AssignClass (f7bf5d7c-2b2d-431c-b51c-add6e4619930)
 Call ID: f7bf5d7c-2b2d-431c-b51c-add6e4619930
  Args:
    source: Perikles_Ioannidis
    type: :Man
  AssignClass (ea5425a9-81b3-4c91-9fea-7831cd0e2475)
 Call ID: ea5425a9-81b3-4c91-9fea-7831cd0e2475
  Args:
    source: Perikles_Ioannidis
    type: :Person
  AddTriple (a3b2b641-b187-4ffe-822c-40c3635bd3f6)
 Call ID: a3b2b641-b187-4ffe-822c-40c3635bd3f6
  Args:
    target: Maria_of_Greece
    relation: :hasRelation
    source: Perikles_Ioannidis
  Finish (60a144b7-9733-4649-9c84-7cbcafaa8d05)
 Call ID: 60a144b7-9733-4649-9c84-7cbcafaa8d05
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

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Alexander_of_Greece a :Man,
          :Person ;
      :isBrotherOf data:George_II_of_Greece .

  data:Alexandra_of_Greece a :Person,
          :Woman ;
      :isSisterOf data:Constantine_I_of_Greece .

  data:Christopher_of_Greece a :Man,
          :Person ;
      :isBrotherOf data:Constantine_I_of_Greece .

  data:Constantine_II_of_Greece a :Man,
          :Person ;
      :hasFather data:Paul_of_Greece ;
      :hasMother data:Frederica_of_Hanover .

  data:Helen_of_Greece a :Person,
          :Woman ;
      :hasMarriageYear 1921 ;
      :hasRelation data:Carol_of_Romania ;
      :isSisterOf data:George_II_of_Greece .

  data:Irene_of_Greece a :Person,
          :Woman ;
      :hasRelation data:Aimone_Duke_of_Aosta ;
      :isSisterOf data:George_II_of_Greece .

  data:Katherine_of_Greece a :Person,
          :Woman ;
      :isSisterOf data:George_II_of_Greece .

  data:Perikles_Ioannidis a :Man,
          :Person ;
      :hasRelation data:Maria_of_Greece .

  data:Aimone_Duke_of_Aosta a :Man,
          :Person .

  data:Carol_of_Romania a :Man,
          :Person ;
      :isBrotherOf data:Elisabeth_of_Romania .

  data:Ernest_Augustus_Duke_of_Brunswick a :Man,
          :Person .

  data:Ferdinand_I_of_Romania a :Man,
          :Person .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Maria_of_Greece a :Person,
          :Woman ;
      :isSisterOf data:Constantine_I_of_Greece .

  data:Marie_of_Romania a :Person,
          :Woman .

  data:Olga_Constantinovna a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person ;
      :hasMarriageYear 1938 ;
      :hasRelation data:Frederica_of_Hanover ;
      :isBrotherOf data:George_II_of_Greece .

  data:Sophia_of_Prussia a :Person,
          :Woman .

  data:Victoria_Louise_of_Prussia a :Person,
          :Woman .

  data:Elisabeth_of_Romania a :Person,
          :Woman ;
      :hasFather data:Ferdinand_I_of_Romania ;
      :hasMother data:Marie_of_Romania .

  data:Frederica_of_Hanover a :Person,
          :Woman ;
      :hasFather data:Ernest_Augustus_Duke_of_Brunswick ;
      :hasMother data:Victoria_Louise_of_Prussia .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece ;
      :hasMother data:Olga_Constantinovna .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Elisabeth_of_Romania .



================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (eedfe06a-5538-4546-8ae8-7cbe27183859)
 Call ID: eedfe06a-5538-4546-8ae8-7cbe27183859
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:30
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Constantine_I_of_Greece' used for the 'hasFather' property of 'George_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Constantine_I_of_Greece', class=':Ancestor')


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Paul_of_Greece' used for the 'hasFather' property of 'Constantine_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Paul_of_Greece', class=':Ancestor')


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'George_I_of_Greece' used for the 'hasFather' property of 'Constantine_I_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='George_I_of_Greece', class=':Ancestor')


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Sophia_of_Prussia' used for the 'hasMother' property of 'George_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Sophia_of_Prussia', class=':Ancestor')


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Frederica_of_Hanover' used for the 'hasMother' property of 'Constantine_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Frederica_of_Hanover', class=':Ancestor')


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Olga_Constantinovna' used for the 'hasMother' property of 'Constantine_I_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Olga_Constantinovna', class=':Ancestor')


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Paul_of_Greece' used for the 'hasFather' property of 'Constantine_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Paul_of_Greece', class=':Ancestor')


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'George_I_of_Greece' used for the 'hasFather' property of 'Constantine_I_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='George_I_of_Greece', class=':Ancestor')


  Violation [9]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Ernest_Augustus_Duke_of_Brunswick' used for the 'hasFather' property of 'Frederica_of_Hanover' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Ernest_Augustus_Duke_of_Brunswick', class=':Ancestor')


  Violation [10]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Constantine_I_of_Greece' used for the 'hasFather' property of 'George_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Constantine_I_of_Greece', class=':Ancestor')


  Violation [11]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Ferdinand_I_of_Romania' used for the 'hasFather' property of 'Elisabeth_of_Romania' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Ferdinand_I_of_Romania', class=':Ancestor')


  Violation [12]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Frederica_of_Hanover' used for the 'hasMother' property of 'Constantine_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Frederica_of_Hanover', class=':Ancestor')


  Violation [13]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Olga_Constantinovna' used for the 'hasMother' property of 'Constantine_I_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Olga_Constantinovna', class=':Ancestor')


  Violation [14]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Victoria_Louise_of_Prussia' used for the 'hasMother' property of 'Frederica_of_Hanover' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Victoria_Louise_of_Prussia', class=':Ancestor')


  Violation [15]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Sophia_of_Prussia' used for the 'hasMother' property of 'George_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Sophia_of_Prussia', class=':Ancestor')


  Violation [16]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Marie_of_Romania' used for the 'hasMother' property of 'Elisabeth_of_Romania' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Marie_of_Romania', class=':Ancestor')


  Violation [17]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Paul_of_Greece' used for the 'hasFather' property of 'Constantine_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Paul_of_Greece', class=':Ancestor')


  Violation [18]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'George_I_of_Greece' used for the 'hasFather' property of 'Constantine_I_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='George_I_of_Greece', class=':Ancestor')


  Violation [19]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Ernest_Augustus_Duke_of_Brunswick' used for the 'hasFather' property of 'Frederica_of_Hanover' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Ernest_Augustus_Duke_of_Brunswick', class=':Ancestor')


  Violation [20]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Constantine_I_of_Greece' used for the 'hasFather' property of 'George_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Constantine_I_of_Greece', class=':Ancestor')


  Violation [21]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Ferdinand_I_of_Romania' used for the 'hasFather' property of 'Elisabeth_of_Romania' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Ferdinand_I_of_Romania', class=':Ancestor')


  Violation [22]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Frederica_of_Hanover' used for the 'hasMother' property of 'Constantine_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Frederica_of_Hanover', class=':Ancestor')


  Violation [23]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Olga_Constantinovna' used for the 'hasMother' property of 'Constantine_I_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Olga_Constantinovna', class=':Ancestor')


  Violation [24]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Victoria_Louise_of_Prussia' used for the 'hasMother' property of 'Frederica_of_Hanover' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Victoria_Louise_of_Prussia', class=':Ancestor')


  Violation [25]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Sophia_of_Prussia' used for the 'hasMother' property of 'George_II_of_Greece' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Sophia_of_Prussia', class=':Ancestor')


  Violation [26]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Marie_of_Romania' used for the 'hasMother' property of 'Elisabeth_of_Romania' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Marie_of_Romania', class=':Ancestor')


  Violation [27]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Ernest_Augustus_Duke_of_Brunswick' used for the 'hasFather' property of 'Frederica_of_Hanover' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Ernest_Augustus_Duke_of_Brunswick', class=':Ancestor')


  Violation [28]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The value node 'Ferdinand_I_of_Romania' used for the 'hasFather' property of 'Elisabeth_of_Romania' does not belong to the required classes ':Ancestor' or ':Man'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Ferdinand_I_of_Romania', class=':Ancestor')


  Violation [29]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Victoria_Louise_of_Prussia' used for the 'hasMother' property of 'Frederica_of_Hanover' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Victoria_Louise_of_Prussia', class=':Ancestor')


  Violation [30]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The value node 'Marie_of_Romania' used for the 'hasMother' property of 'Elisabeth_of_Romania' does not belong to the required classes ':Ancestor' or ':Woman'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Marie_of_Romania', class=':Ancestor')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (1ed0d426-73d4-4e28-8e5d-ddcb8f498efb)
 Call ID: 1ed0d426-73d4-4e28-8e5d-ddcb8f498efb
  Args:
    type: :Ancestor
    source: Constantine_I_of_Greece
  AssignClass (fb3615c1-6ced-4ff7-a10c-4df0e4b2e0e2)
 Call ID: fb3615c1-6ced-4ff7-a10c-4df0e4b2e0e2
  Args:
    type: :Ancestor
    source: Paul_of_Greece
  AssignClass (6e5eab89-353c-4ade-883f-c310ecbe22d7)
 Call ID: 6e5eab89-353c-4ade-883f-c310ecbe22d7
  Args:
    source: George_I_of_Greece
    type: :Ancestor
  AssignClass (b0e6e1c2-daa8-4478-99fb-34bbdd587cb8)
 Call ID: b0e6e1c2-daa8-4478-99fb-34bbdd587cb8
  Args:
    source: Sophia_of_Prussia
    type: :Ancestor
  AssignClass (8286dd13-67e7-4261-95f1-a0601fd5c332)
 Call ID: 8286dd13-67e7-4261-95f1-a0601fd5c332
  Args:
    source: Frederica_of_Hanover
    type: :Ancestor
  AssignClass (9b000579-23a0-48f0-83f9-a75adf6af48d)
 Call ID: 9b000579-23a0-48f0-83f9-a75adf6af48d
  Args:
    type: :Ancestor
    source: Olga_Constantinovna
  AssignClass (89a58cf0-8ec9-4067-8406-ac1f51c756d4)
 Call ID: 89a58cf0-8ec9-4067-8406-ac1f51c756d4
  Args:
    source: Ernest_Augustus_Duke_of_Brunswick
    type: :Ancestor
  AssignClass (309c5a5a-55f6-458b-acf4-4a55d016933b)
 Call ID: 309c5a5a-55f6-458b-acf4-4a55d016933b
  Args:
    source: Ferdinand_I_of_Romania
    type: :Ancestor
  AssignClass (784c21a0-5566-491a-962e-cdbcdc59c9bb)
 Call ID: 784c21a0-5566-491a-962e-cdbcdc59c9bb
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Ancestor
  AssignClass (54743150-051e-4ebc-8565-8958faa03334)
 Call ID: 54743150-051e-4ebc-8565-8958faa03334
  Args:
    source: Marie_of_Romania
    type: :Ancestor
  ValidateShacl (f8d5e44c-b1b4-4028-98ed-c347ae2a87f3)
 Call ID: f8d5e44c-b1b4-4028-98ed-c347ae2a87f3
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

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Alexander_of_Greece a :Man,
          :Person ;
      :isBrotherOf data:George_II_of_Greece .

  data:Alexandra_of_Greece a :Person,
          :Woman ;
      :isSisterOf data:Constantine_I_of_Greece .

  data:Christopher_of_Greece a :Man,
          :Person ;
      :isBrotherOf data:Constantine_I_of_Greece .

  data:Constantine_II_of_Greece a :Man,
          :Person ;
      :hasFather data:Paul_of_Greece ;
      :hasMother data:Frederica_of_Hanover .

  data:Helen_of_Greece a :Person,
          :Woman ;
      :hasMarriageYear 1921 ;
      :hasRelation data:Carol_of_Romania ;
      :isSisterOf data:George_II_of_Greece .

  data:Irene_of_Greece a :Person,
          :Woman ;
      :hasRelation data:Aimone_Duke_of_Aosta ;
      :isSisterOf data:George_II_of_Greece .

  data:Katherine_of_Greece a :Person,
          :Woman ;
      :isSisterOf data:George_II_of_Greece .

  data:Perikles_Ioannidis a :Man,
          :Person ;
      :hasRelation data:Maria_of_Greece .

  data:Aimone_Duke_of_Aosta a :Man,
          :Person .

  data:Carol_of_Romania a :Man,
          :Person ;
      :isBrotherOf data:Elisabeth_of_Romania .

  data:Ernest_Augustus_Duke_of_Brunswick a :Ancestor,
          :Man,
          :Person .

  data:Ferdinand_I_of_Romania a :Ancestor,
          :Man,
          :Person .

  data:George_I_of_Greece a :Ancestor,
          :Man,
          :Person .

  data:Maria_of_Greece a :Person,
          :Woman ;
      :isSisterOf data:Constantine_I_of_Greece .

  data:Marie_of_Romania a :Ancestor,
          :Person,
          :Woman .

  data:Olga_Constantinovna a :Ancestor,
          :Person,
          :Woman .

  data:Paul_of_Greece a :Ancestor,
          :Man,
          :Person ;
      :hasMarriageYear 1938 ;
      :hasRelation data:Frederica_of_Hanover ;
      :isBrotherOf data:George_II_of_Greece .

  data:Sophia_of_Prussia a :Ancestor,
          :Person,
          :Woman .

  data:Victoria_Louise_of_Prussia a :Ancestor,
          :Person,
          :Woman .

  data:Elisabeth_of_Romania a :Person,
          :Woman ;
      :hasFather data:Ferdinand_I_of_Romania ;
      :hasMother data:Marie_of_Romania .

  data:Frederica_of_Hanover a :Ancestor,
          :Person,
          :Woman ;
      :hasFather data:Ernest_Augustus_Duke_of_Brunswick ;
      :hasMother data:Victoria_Louise_of_Prussia .

  data:Constantine_I_of_Greece a :Ancestor,
          :Man,
          :Person ;
      :hasFather data:George_I_of_Greece ;
      :hasMother data:Olga_Constantinovna .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Elisabeth_of_Romania .



================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (16b921a0-2533-44fe-a584-8da478ead957)
 Call ID: 16b921a0-2533-44fe-a584-8da478ead957
  Args: