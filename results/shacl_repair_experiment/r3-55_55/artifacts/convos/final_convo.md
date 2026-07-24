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
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix data: <http://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:George_II_of_Greece a :Man,
        :Person ;
    :hasBirthYear 1890 ;
    :hasDeathYear 1947 ;
    :hasFather data:Constantine_I_of_Greece ;
    :hasMarriageYear 1921 ;
    :hasMother data:Sophia_of_Prussia ;
    :hasRelation data:Christopher_of_Greece,
        data:Elisabeth_of_Romania ;
    :isBrotherOf data:Alexander_of_Greece,
        data:Paul_of_Greece ;
    :isSisterOf data:Helen_of_Greece,
        data:Irene_of_Greece,
        data:Katherine_of_Greece .

data:Alexander_of_Greece a :Man,
        :Person .

data:Christopher_of_Greece a :Man,
        :Person .

data:Constantine_I_of_Greece a :Man,
        :Person ;
    :hasFather data:George_I_of_Greece .

data:Elisabeth_of_Romania a :Person,
        :Woman .

data:George_I_of_Greece a :Man,
        :Person .

data:Helen_of_Greece a :Person,
        :Woman .

data:Irene_of_Greece a :Person,
        :Woman .

data:Katherine_of_Greece a :Person,
        :Woman .

data:Paul_of_Greece a :Man,
        :Person .

data:Sophia_of_Prussia a :Person,
        :Woman .



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (92468b0a-2aa4-4689-a20f-5e52a2451b66)
 Call ID: 92468b0a-2aa4-4689-a20f-5e52a2451b66
  Args:
    source: data:Constantine_I_of_Greece
    type: :Man

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece ;
      :isSisterOf data:Helen_of_Greece,
          data:Irene_of_Greece,
          data:Katherine_of_Greece .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b0eaacee-9642-40a0-a533-3605c6ae773d)
 Call ID: b0eaacee-9642-40a0-a533-3605c6ae773d
  Args:
    type: :Man
    source: data:George_I_of_Greece

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece ;
      :isSisterOf data:Helen_of_Greece,
          data:Irene_of_Greece,
          data:Katherine_of_Greece .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (c72c7fcb-2140-4b98-9781-280f64342709)
 Call ID: c72c7fcb-2140-4b98-9781-280f64342709
  Args:
    source: data:Constantine_I_of_Greece
    target: data:George_I_of_Greece
    relation: :hasFather

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece ;
      :isSisterOf data:Helen_of_Greece,
          data:Irene_of_Greece,
          data:Katherine_of_Greece .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AddTriple (9da62fe9-3c86-4544-aaa6-00164de1b62a)
 Call ID: 9da62fe9-3c86-4544-aaa6-00164de1b62a
  Args:
    target: data:Sophia_of_Prussia
    relation: :hasMother
    source: data:George_II_of_Greece

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece ;
      :isSisterOf data:Helen_of_Greece,
          data:Irene_of_Greece,
          data:Katherine_of_Greece .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (c12fdb7b-7472-4fa2-9fff-c91faf629aab)
 Call ID: c12fdb7b-7472-4fa2-9fff-c91faf629aab
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:12
Violations:

  Violation [1]:
    SHACL message: Node data:George_II_of_Greece is closed. It cannot have value: data:Katherine_of_Greece
    LLM-provided explanation of the violation:
      The node George_II_of_Greece is defined as a closed shape, meaning it cannot have the property 'isSisterOf'.
    LLM-provided instruction on how to handle the violation:
      RemoveTriple(George_II_of_Greece, :isSisterOf, Katherine_of_Greece)


  Violation [2]:
    SHACL message: Node data:George_II_of_Greece is closed. It cannot have value: data:Helen_of_Greece
    LLM-provided explanation of the violation:
      The node George_II_of_Greece is defined as a closed shape, meaning it cannot have the property 'isSisterOf'.
    LLM-provided instruction on how to handle the violation:
      RemoveTriple(George_II_of_Greece, :isSisterOf, Helen_of_Greece)


  Violation [3]:
    SHACL message: Node data:George_II_of_Greece is closed. It cannot have value: data:Irene_of_Greece
    LLM-provided explanation of the violation:
      The node George_II_of_Greece is defined as a closed shape, meaning it cannot have the property 'isSisterOf'.
    LLM-provided instruction on how to handle the violation:
      RemoveTriple(George_II_of_Greece, :isSisterOf, Irene_of_Greece)


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_I_of_Greece is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasFather' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(George_I_of_Greece, :Ancestor)


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Constantine_I_of_Greece is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasFather' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Constantine_I_of_Greece, :Ancestor)


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Sophia_of_Prussia is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasMother' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Sophia_of_Prussia, :Ancestor)


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_I_of_Greece is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasFather' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(George_I_of_Greece, :Ancestor)


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Constantine_I_of_Greece is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasFather' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Constantine_I_of_Greece, :Ancestor)


  Violation [9]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Sophia_of_Prussia is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasMother' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Sophia_of_Prussia, :Ancestor)


  Violation [10]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_I_of_Greece is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasFather' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(George_I_of_Greece, :Ancestor)


  Violation [11]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Constantine_I_of_Greece is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasFather' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Constantine_I_of_Greece, :Ancestor)


  Violation [12]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Sophia_of_Prussia is currently missing the required ':Ancestor' class assignment, which is needed to satisfy the 'hasMother' relationship constraints.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Sophia_of_Prussia, :Ancestor)




================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (226c2c51-2565-4e83-b361-320742768242)
 Call ID: 226c2c51-2565-4e83-b361-320742768242
  Args:
    target: data:Katherine_of_Greece
    source: data:George_II_of_Greece
    relation: :isSisterOf

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece ;
      :isSisterOf data:Helen_of_Greece,
          data:Irene_of_Greece .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (ddd6a889-e7cc-41ef-ad3c-593ecb228602)
 Call ID: ddd6a889-e7cc-41ef-ad3c-593ecb228602
  Args:
    relation: :isSisterOf
    source: data:George_II_of_Greece
    target: data:Helen_of_Greece

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece ;
      :isSisterOf data:Irene_of_Greece .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (f4d6073a-63e4-48bd-b3dc-f6cd40f7911a)
 Call ID: f4d6073a-63e4-48bd-b3dc-f6cd40f7911a
  Args:
    source: data:George_II_of_Greece
    target: data:Irene_of_Greece
    relation: :isSisterOf

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Man,
          :Person .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e38f11d2-43e1-420f-b8b7-e81e3ef9bd1c)
 Call ID: e38f11d2-43e1-420f-b8b7-e81e3ef9bd1c
  Args:
    type: :Ancestor
    source: data:George_I_of_Greece

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Ancestor,
          :Man,
          :Person .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (5c546bac-df31-44fa-810b-767acd139085)
 Call ID: 5c546bac-df31-44fa-810b-767acd139085
  Args:
    source: data:Constantine_I_of_Greece
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Ancestor,
          :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Ancestor,
          :Man,
          :Person .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c6a94a64-96f4-484d-86a8-346c6ab15d9b)
 Call ID: c6a94a64-96f4-484d-86a8-346c6ab15d9b
  Args:
    source: data:Sophia_of_Prussia
    type: :Ancestor

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:George_II_of_Greece a :Man,
          :Person ;
      :hasBirthYear 1890 ;
      :hasDeathYear 1947 ;
      :hasFather data:Constantine_I_of_Greece ;
      :hasMarriageYear 1921 ;
      :hasMother data:Sophia_of_Prussia ;
      :hasRelation data:Christopher_of_Greece,
          data:Elisabeth_of_Romania ;
      :isBrotherOf data:Alexander_of_Greece,
          data:Paul_of_Greece .

  data:Helen_of_Greece a :Person,
          :Woman .

  data:Irene_of_Greece a :Person,
          :Woman .

  data:Katherine_of_Greece a :Person,
          :Woman .

  data:Alexander_of_Greece a :Man,
          :Person .

  data:Christopher_of_Greece a :Man,
          :Person .

  data:Constantine_I_of_Greece a :Ancestor,
          :Man,
          :Person ;
      :hasFather data:George_I_of_Greece .

  data:Elisabeth_of_Romania a :Person,
          :Woman .

  data:George_I_of_Greece a :Ancestor,
          :Man,
          :Person .

  data:Paul_of_Greece a :Man,
          :Person .

  data:Sophia_of_Prussia a :Ancestor,
          :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (eaa1f1e8-fa3f-42af-a0a3-74856a7138ae)
 Call ID: eaa1f1e8-fa3f-42af-a0a3-74856a7138ae
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (6abab23c-3369-4053-8cf4-6ca710bab204)
 Call ID: 6abab23c-3369-4053-8cf4-6ca710bab204
  Args: