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
Sophia of Prussia (Sophie Dorothea Ulrike Alice, Greek: Σοφία Δωροθέα Ουλρίκη Αλίκη, romanized: Sofía Dorothéa Oulríki Alíki; 14 June 1870 –
13 January 1932) was Queen of Greece from 18 March 1913 to 11 June 1917 and again from 19 December 1920 to 27 September 1922 as the wife of King Constantine I.


A member of the House of Hohenzollern and child of Frederick III, German Emperor, Sophia received a liberal and Anglophile education, under the supervision of her mother Victoria, Princess Royal.
In 1889, less than a year after the death of her father, she married her third cousin Constantine, heir apparent to the Greek throne.
After a difficult period of adaptation in her new country, Sophia gave birth to six children and became involved in the assistance to the poor, following in the footsteps of her mother-in-law, Queen Olga.
However, it was during the wars which Greece faced during the end of the 19th and the beginning of the 20th century that Sophia showed the most social activity: she founded field hospitals, oversaw the training of Greek nurses, and treated wounded soldiers.
However, Sophia was hardly rewarded for her actions, even after her grandmother Queen Victoria decorated her with the Royal Red Cross after the Thirty Days' War: the Greeks criticized her links with Germany.
Her eldest brother, German Emperor William II, was indeed an ally of the Ottoman Empire and openly opposed the construction of the Megali Idea, which could establish a Greek state that would encompass all ethnic Greek-inhabited areas.
During World War I, the blood ties between Sophia and the Emperor also aroused the suspicion of the Triple Entente, which criticized Constantine I for his neutrality in the conflict.
After imposing a blockade of Greece and supporting the rebel government of Eleftherios Venizelos, causing the National Schism, France and its allies deposed Constantine in June 1917.
Sophia and her family then went into exile in Switzerland.
Sophia's second son, Alexander, replaced his father on the throne.
At the same time, Greece entered the war alongside the Triple Entente, which allowed for impressive, but eventually temporary, territorial gains.
After the outbreak of the Greco-Turkish War in 1919 and the untimely death of Alexander the following year, the Venizelists abandoned power, allowing the royal family to return to Athens.
However, the defeat of the Greek army against the Turkish troops of Mustafa Kemal forced Constantine to abdicate in 1922, at which point his eldest son became King George II.
Sophia and her family were then forced to a new exile, and settled in Italy, where Constantine died one year later, in 1923.
With the proclamation of the Republic in Athens the following year, Sophia spent her last years alongside her family, before dying of cancer in Germany in 1932 at the age of 61.
Princess of Prussia and Germany (1870-1889)

Birth in a difficult context

Princess Sophie was born in the Neues Palais in Potsdam, Prussia, on 14 June 1870 as the daughter of Frederick William, Crown Prince of Prussia, and Victoria, Princess Royal of the United Kingdom.
The Crown Prince was the son of King William I of Prussia, and the Princess Royal was the eldest child of Queen Victoria and Prince Albert.
Frederick William and Victoria were already the parents of a large family and as the penultimate child, Sophie was eleven years younger than her eldest brother, the future William II of Germany.
Being staunch liberals, they lived away from the Berlin court and suffered the intrigues of a very conservative German chancellor, Otto von Bismarck, and members of the House of Hohenzollern.
Six days later, the French government under Emperor Napoleon III declared war on Prussia and the states of the German Confederation offered support to Prussia, which then appeared as the victim of French imperialism.
It was in this difficult context that Sophie was christened the following month, though all the men present were in uniform, as France had declared war on Prussia.
Sophie's mother described the event to Queen Victoria: "The Christening went off well, but was sad and serious; anxious faces and tearful eyes, and a gloom and foreshadowing of all the misery in store spread a cloud over the ceremony, which should have been one of gladness and thanksgiving".
However, the conflict lasted only a few months and even led to a brilliant German victory, leading to the proclamation of Sophie's grandfather William I as the first German emperor on 18 January 1871.
Anglophile education

Sophie was known as "Sossy" during her childhood (the name was thought to have been picked because it rhymed with "Mossy", the nickname of her younger sister Margaret).
William, Charlotte, and Henry who were favored by their paternal grandparents, while Viktoria, Sophie and Margaret were largely ignored by them.
Sophie's two other brothers, Sigismund and Waldemar, died at a young age (Sigismund died before she was born, and Waldemar when he was 11 and she was 8); this drew the Crown Princess and her three younger daughters closer together, calling them "my three sweet girls" and "my trio".
The Crown Princess, believing in the superiority of all things English, had her children's nurseries modeled on her childhood.
Sophie was raised with a great love for England and all things associated with it as a result, and had frequent trips to visit her grandmother Queen Victoria, whom she loved.
As a little girl she was so deeply attached to Queen Victoria that the Crown Princess did not hesitate to leave her daughter for long periods under the care of her grandmother.
Like her sisters Viktoria and Margaret, she was particularly close to her parents and their relationship became even closer after the death in 1879 of Waldemar, the favorite son of the Crown Princely couple.
Meeting and engagement to Constantine

In 1884, Constantine, Crown Prince of Greece, turned sixteen and his majority was declared by the government.
Soon after, Constantine completed his military training in Germany, where he spent two full years in the company of a tutor, Dr. Lüders.
He served in the Prussian Guard, took lessons of riding in Hanover and studied political science at the Universities of Heidelberg and Leipzig.
After a long stay in England celebrating her grandmother's Golden Jubilee, Sophie became better acquainted with Constantine in the summer of 1887.
Crown Princess Victoria also hoped that Sophie would make a good marriage, considering her the most attractive among her daughters.
During his stay at the Hohenzollern court in Berlin representing the Kingdom of Greece at the funeral of Emperor William I in March 1888, Constantine saw Sophie again.
However, their relationship was viewed with suspicion by Sophie's older brother William and his wife Augusta Victoria, the latter of whom she despised.
This betrothal was not completely supported in the Greek royal family either: Queen Olga showed some reluctance to the projected union because Sophie was Lutheran and Olga would have preferred that her son marry an Orthodox Christian.
Death of Emperor Frederick III

This period fell on an unhappy time for Sophie's family however, as her father Emperor Frederick III was dying an agonizing death of throat cancer.
Frederick died the next day.
Sophie's eldest brother became Emperor William II.
Knowing that her three youngest daughters were more dependent on her than ever for emotional support, the now-Dowager Empress Frederick remained close to them: "I have my three sweet girls - he loved so much - that are my consolation".


Already shocked by the attitude of her eldest son, the Dowager Empress was deeply saddened by Sophie's upcoming marriage and move to Athens.
Crown princess of Greece (1889-1913)

Auspicious marriage to the Greeks

On 27 October 1889, Sophie married Constantine in Athens in two religious ceremonies, one public and Orthodox and another private and Protestant.
They were third cousins in descent from Paul I of Russia, and second cousins once removed through Frederick William III of Prussia.
Sophie's witnesses were her brother Henry and her cousins Princes Albert Victor and George of Wales; for Constantine's side, the witnesses were his brothers Princes George and Nicholas and his cousin the Tsarevich of Russia.
The names of the couple were reminiscent to the public of an old legend which suggested that when a King Constantine and a Queen Sophia ascended the Greek throne, Constantinople and the Hagia Sophia would fall to Greek hands.
Abroad, the marriage of Constantine and Sophie raised much less enthusiasm.
In France, it was feared that the arrival of a Prussian princess in Athens would switch the Kingdom of Greece to the side of the Triple Alliance.
In Berlin, the union was also unpopular: German interests were indeed important in the Ottoman Empire and the Emperor did not intend to help Greece simply because the Greek crown prince was his new brother-in-law.
Platforms were also built on the Syntagma Square so the public could better admire the procession between the Royal Palace and the Cathedral.
The newlyweds were related to most of the European dynasties, so representatives of all the royal houses of the continent were part of the festivities: Christian IX of Denmark (grandfather of the groom), Emperor William II of Germany (brother of the bride), the Prince of Wales (uncle of both groom and bride) and the Tsarevich of Russia (groom's cousin) were among the guests of honor.
In fact, the hosts and their retinues were so many in Athens that King George I could not receive all of them in his palace.
In addition, George was forced to hastily buy dozens of additional liveries for the lackeys at the service of the guests.
Installation in Athens

In Athens, Constantine and Sophia settled in a small villa of French style located on Kifisias Avenue, while waiting for the Greek state to build a new home for them, the Crown Prince's Palace, located near the Royal Palace.
The couple also ordered the building of another house on the royal estate of Tatoi because King George I refused to allow work to be undertaken in the main palace.
In Athens, Constantine and Sophia lived a relatively simple life far removed from the protocol of other European courts, but life in Greece was often monotonous and Sophia lamented for any company, save only for the wives of the tobacco merchants.
Sophia had difficulties adjusting to her new life.
Less than nine months after her marriage, on 19 July 1890, the Crown Princess gave birth to her first child, a slightly premature son who was named George after his paternal grandfather, but the birth went wrong and the umbilical cord was wrapped around the baby's neck, almost choking him.
Fortunately for the mother and child, the German midwife sent by the Dowager Empress Victoria to help her daughter in childbirth managed to resolve the situation and no tragic consequences occurred.
Conversion to Orthodoxy

After the birth of her eldest son, Sophia decided to embrace the faith of her subjects and convert to the Orthodox faith.
Having requested and received the blessing of the Empress Dowager and Queen Victoria, the Crown Princess informed her in-laws of her intention and asked Queen Olga for instruction in Orthodoxy.
The Greek royal family was delighted by the news, because the announcement of the conversion would be popular among the Greeks but King George insisted that Germanus II, Metropolitan of Athens and head of the autocephalous Church of Greece, would instruct Sophie in the Orthodox faith, rather than his wife.
Though the news of her conversion was greeted calmly by most members of her family, Sophia feared the reaction of her brother William II, who took his status as Head of the Prussian Union of Churches very seriously and hated disobedience more than anything.
Sophia and Constantine took a trip to Germany for the occasion of the wedding of her sister Viktoria to Prince Adolf of Schaumburg-Lippe in November 1890.
The Crown Princess personally announced to her brother her intentions to change her religion.
As expected, the news strongly displeased the Emperor and his wife, the very pious Augusta Victoria.
Augusta later claimed that this caused her to go into premature labor, and deliver her sixth child, Prince Joachim, too early.
William, meanwhile, was so angry that he threatened Sophia with exclusion from the Prussian royal family.
Pressed by her mother to appear conciliatory, Sophia ended up writing a letter to her brother explaining the reasons for her conversion but the Emperor would not listen, and for three years he forbade his sister to enter Germany.
"


Sophia officially converted on 2 May 1891; however, the imperial sentence was ultimately never implemented.
Nevertheless, relations between William and Sophia were permanently marked by Sophia's decision.
Indeed, the Emperor was an extremely resentful man and he never stopped making his sister pay for her disobedience.
Social work

Throughout her life in Greece, Sophia was actively involved in social work and helping the underprivileged.
In 1896, the Crown Princess also founded the Union of Greek Women, a particularly active organization in the field of assistance to refugees from the Ottoman Empire.
Fascinated by arboriculture and concerned by the fires that regularly ravaged the country, Sophia was also interested in the reforestation.
However, it was during wartime that Sophie showed the most resilience.
In 1897, when the Thirty Days' War broke out, Sophia and other female members of the royal family actively worked with the Greek Red Cross in order to help wounded soldiers.
On the Thessalian front, the Crown Princess founded field hospitals, visited the wounded and even directly administered care for victims of the fighting.
Sophia also facilitated the arrival of English nurses in Greece and even participated in the training of young women volunteers to provide assistance to wounded soldiers.
The involvement of Sophia and her mother-in-law in the aid to the victims of fighting (either of Greek or Turkish origin) was so active that it elicited admiration from other European courts.
As a reward for their work, both women were decorated with the Royal Red Cross by Queen Victoria, in December 1897.
Unfortunately for the Crown Princess, her help for the wounded soldiers was less appreciated in Greece, where the population blamed the royal family, and especially Constantine, who was commander-in-chief of the Greek army in Thessaly, for the loss against the Ottomans.
Consequences of the War of Thirty Days

After the Thirty Days' War, a powerful anti-monarchical movement developed in Greece and Sophia herself was not immune to criticism.
Always eager to punish his sister for her disobedience, Emperor William II of Germany openly supported the Ottoman Empire during the conflict and agreed to offer his mediation after being begged by his sister, his mother and his grandmother.
He demanded that Greece agree to humiliating conditions in exchange for his intervention and the population believed that he did so with the consent of his sister.
However Sophia was not the only victim of popular condemnation.
In fact, it was openly discussed in Athens that the Crown Prince should be sent before a military court to punish him for the national defeat and depose George I as was previously done with his predecessor Otto I. Several weeks after the signing of the peace treaty between Greece and the Ottoman Empire, the situation became so tense that the sovereign was a subject of an assassination attempt when he traveled in an open carriage with his daughter, Princess Maria, but George I defended himself so bravely that he recovered at least some estimation from his subjects.
In these difficult conditions, Constantine and Sophia choose to live some time abroad.
There Constantine resumed his military training with General Colmar von der Goltz and for a year, he received the command of a Prussian division.
To mark their reconciliation, Emperor William II also appointed Sophia as colonel-in-chief of the 3rd (Queen Elisabeth)
The couple returned to Greece in 1899 and the government of Georgios Theotokis appointed Constantine as inspector-general of the army.
This promotion, however, caused some controversy among the army, which still considered the Crown Prince as the main person responsible for the defeat in 1897.
Family deaths

Back in Greece with her husband, the Crown Princess resumed her charity work.
Sophia was concerned that the difficulties suffered by the British in South Africa would undermine the already fragile health of her grandmother.
Queen Victoria finally died of a cerebral hemorrhage on 22 January 1901 in Osborne House.
Very affected by the death of the sovereign, Sophia traveled to the United Kingdom for her funeral and attended a religious ceremony in her honor in Athens with the rest of the Greek royal family.
Five months pregnant, the Crown Princess knew that the Dowager Empress was dying and, with her sisters Viktoria and Margaret, she accompanied her until her last breath on 5 August.
In the space of seven months Sophia lost two of her closest relatives.
Goudi coup and its consequences

In Greece, political life remained volatile throughout the first years of the 20th century and the Megali Idea continued to be a central concern of the population.
In 1908, the Cretan authorities unilaterally proclaimed the attachment of their island to the Kingdom of Greece but for fear of Turkish reprisals, the Greek government refused to recognize the annexation.
On 15 August 1909, a group of officers gathered in the "Military League" (Στρατιωτικός Σύνδεσμος) and organized the so-called Goudi coup.
Officially, this was to protect the Crown Prince from the jealousies that could arise from his friendship with some soldiers but the reality was quite different: officers continued to hold the Crown Prince responsible for the 1897 defeat.
The situation became so tense that George I's sons had to resign from their military posts to save their father the shame of having to expelled them.
In September, the Crown Prince, his wife and their children also chose to leave Greece and seek refuge in Germany at Friedrichshof, now owned by the Princess Margaret of Prussia.
Meanwhile, in Athens, discussions began in some circles about dethroning the House of Glücksburg to establishing a republic or replacing the sovereign with either a bastard son of Otto I, a foreign prince or with Prince George, with Sophia as regent.
In December 1909, Colonel Zorbas, head of the Military League, pressured George I to appoint him as the head of the government in place of Prime Minister Kyriakoulis Mavromichalis.
The staff was reorganized and supporters of the Crown Prince, including Ioannis Metaxas, were expelled.
At the same time, a French army mission was called to reorganize the Greek army, which threatened both Sophia and her husband, as they helped develop republican ideas within the military.
They then traveled to Crete to meet the prominent Cretan politician Eleftherios Venizelos, and offered him the post of Prime Minister of Greece.
However the Cretan leader did not want to appear in Greece to be supported by the army and convinced them to arrange for new elections.
For the royal family, this was a difficult time.
To show that he did not obey the army, he restored the members of the royal family to their military duties and the Crown Prince thus again became inspector-general of the army.
Back in Greece on 21 October 1910, after over a year of exile, Sophia nevertheless remained very suspicious of the new government and the militia.
She refused any contact with Venizelos, blaming him as partly responsible for the humiliation suffered by the royal family.
The Princess also had problems with her father-in-law, whom she accused of having been weak during the crisis.
The aim of the modernization was to make the country ready for a new war against the Ottoman Empire but to defeat the enemy and achieve the Megali Idea, Greece needed allies.
That was why, under the initiative of the new Prime Minister, Greece signed alliances with its neighbors and participated in the creation of the Balkan League in June 1912.
Thus, when Montenegro declared war on the Ottoman Empire on 8 October 1912, they were joined less than ten days later by Serbia, Bulgaria and Greece.
While the Crown Prince and his brothers took command of Greek troops, Queen Olga, Sophia, and her sisters-in-law (Marie Bonaparte, Elena Vladimirovna of Russia and Alice of Battenberg) took in charge the aid to wounded soldiers and refugees.
The Queen and Crown Princess also opened a public subscription in order to create new hospitals in Athens and on the front.
Queen Olga and Sophia visited Larissa and Elassona, while Alice made long stays in Epirus and Macedonia.
The war was an opportunity for the princesses to prove themselves useful to their adopted country but it also exacerbated rivalries within the royal family.
Conflict began due to Sophia's jealousy of her cousin and sister-in-law Alice.
In fact, a heated argument between the two young women erupted after Alice sent, without requesting permission from Sophia, nurses dependent on the Crown Princess to Thessaloniki.
One seemingly innocuous event provoked a real discomfort within the family and Queen Olga was shocked when Sophia's attitude was supported by her husband.
Marital problems and private life

Sophia and Constantine's marriage was harmonious during the first years.
However, faithfulness was not the greatest quality of the Crown Prince and his wife soon had to deal with his numerous extramarital affairs.
Initially shocked by his betrayal, Sophia soon followed the example of her mother-in-law and condoned the behavior of her husband.
At that time, Constantine began an affair with Countess Paola von Ostheim (née Wanda Paola Lottero), an Italian stage actress who had recently divorced from Prince Hermann of Saxe-Weimar-Eisenach; this relationship lasted until Constantine's death.
When Sophia gave birth to her sixth and last child, a daughter named Katherine, on 4 May 1913, a persistent gossip stated that the child was the result of her own affairs.
The rumors, true or false, did not affect Constantine, who easily recognized his paternity.
Like her mother, Sophia inculcated in her offspring the love for the United Kingdom and for several weeks every year, the family spent time in Great Britain, where she visited the beaches of Seaford and Eastbourne.
However, the summer vacations of the family were spent not only in Friedrichshof with the Empress Dowager, but also in Corfu and Venice, where the Greek royal family went aboard the yacht Amphitrite.
Queen of the Hellenes: 1st tenure (1913-1917)

Assassination of George I and Second Balkan War

The First Balkan War ended in 1913 with the defeat of the Ottoman Empire by the Greek, Bulgarian, Serbian and Montenegrin coalition.
The Kingdom of Greece was greatly expanded after the conflict but disagreements soon arose between the allied powers: Greece and Bulgaria competed for possession of Thessaloniki and its surrounding region.
To affirm the sovereignty of the Greeks over the main city of Macedonia, George I moved to the city soon after its conquest by the Crown Prince, on 8 December 1912.
Sophia was in Athens when she learned of the murder of her father-in-law, the king.
Together with her eldest daughter, Princess Helen, both comforted the now Dowager Queen, who received the news stoically.
The next day, members of the royal family who were present in the capital went to Thessaloniki.
In this difficult context, the death of George I sealed the possession of Thessaloniki to Greece.
Victorious again, Greece came out of this war considerably enlarged, with the prestige of King Constantine I and Queen Sophia also increased.
Private life

After their accession to the throne, Constantine and Sophia continued to lead the simple lifestyle that they had enjoyed during their time as heirs.
They spent their free time practising botany, which was their common passion, and transformed the gardens of the New Royal Palace on the English model.
The couple was very close to other members of the royal family, especially Prince Nicholas.
Every Tuesday, the King and Queen dined with him and his wife Elena, and on Thursdays, they returned the visit with the royal couple at the Royal Palace.
Outbreak of World War I

At the outbreak of World War I on 4 August 1914 Sophia was in England at Eastbourne with several of her children while her husband and their daughter Helen were the only representatives of the dynasty still present in Athens.
However, given the gravity of events, the Queen quickly returned to Greece, where she was soon joined by the rest of the royal family.
While the greater European states entered into the conflict one by one, Greece officially proclaimed its neutrality.
Being grandchildren of the so-called "Father-in-law and Grandmother of Europe" (as Christian IX of Denmark and Queen Victoria respectively were known), Constantine and Sophia were closely related to the monarchs of the Triple Alliance and the Triple Entente.
The King and Queen were aware that Greece was already weakened by the Balkan Wars and was not ready to participate in a new conflict.
Prime Minister Eleftherios Venizelos, whose great diplomatic skills had been greatly acknowledged at the London Conference of 1912-1913, especially by David Lloyd George and Georges Clemenceau, knew that Greece's newly acquired dominions were in a precarious state, so Greece had to participate in the war with the Entente Cordiale in order to safeguard its winnings from the Second Balkan War.
Moreover, the Ottoman Empire, Bulgaria and even Romania had aligned themselves with Germany and, if Germany won the war, it would most certainly be at Greece's expense, given that Bulgaria's and the Ottoman Empire's winnings in land would inevitably come from Greek lands acquired in 1913, since both countries, greatly angered at the loss of Macedonia, were looking to overthrow the Treaty of Bucharest.
Wanting to release the Greek populations of Asia Minor from Ottoman rule, Constantine I was at first ready to offer his support to the Allies and bring his country into the war.
However, the King faced the opposition of his Staff and, in particular, Ioannis Metaxas, who threatened to resign if Greece entered the war.
The country did not have the means, even though the Allies offered great advantages for Greece in return for its participation.
Constantine I was a great Germanophile; he had been educated in Germany, was almost raised as a German and admired immensely the Kaiser.
Constantine I therefore desisted, causing the wrath of Venizelos, who saw his country being in great peril because of the King.
Because of Constantine I's actions, the Prime Minister handed over his resignation in 1915 (even after he won twice the elections held on the subject of war).
A royal government then emerged.
However, Venizelos was proven right on 25 May 1916, when the royal Greek government of Athens permitted the surrender of the Fort Roupel to the Germans and their Bulgarian allies as a counterbalance to the Allied forces that had been established in Thessaloniki.
The German-Bulgarian troops then proceeded to occupy most of eastern Macedonia without resistance, resulting in the massacre of the Greek population there.
This act led to the outbreak of a revolt of Venizelist army officers in Thessaloniki and the establishment of the Provisional Government of National Defence under Entente auspices there, opposed to the official government of Athens and Constantine I, cementing the so-called "National Schism".
Weakened by all these events, Constantine I became seriously ill after this crisis.
In Greece, public opinion was outraged by a rumour, spread by Venizelists, who said that the King was not sick but was in fact wounded with a knife by Sophia during an argument where she wanted to force him to go to war alongside her brother.
In the words of G. Leon, "She remained a German, and Germany's interests were placed above those of her adopted country which meant little to her.
Various sources from the period-whose diaries, journals and extensive correspondence have been a subject of great study in Greece-note that Sophia used to hide behind a curtain in her husband's apartments during Cabinet meetings and private audiences with the King, in order to be informed on the state of affairs.
While Constantine I had already received the last sacraments, he partly recovered his health after kissing the icon.
Relieved by the recovery of her husband, Sophia offered then, by way of ex-voto, a sapphire to enrich the icon.
During the King's illness period, the Triple Entente continued to put pressure on Greece to go to war alongside them.
A month later, Constantine I, still convalescent, reassumed his official duties and eventually called on Venizelos to head the Cabinet on 16 August.
In September, Bulgaria entered the war alongside the Central Powers and attacked Serbia, ally of Greece since 1913.
However, to avoid a new political crisis, Constantine I finally proclaimed mobilization while making it clear that this was a purely defensive measure.
On 3 October, in order to force the King to react, the Prime Minister called on the Allied Powers to occupy the port of Thessaloniki but Constantine I left the city when the French, Italian and British forces landed in the city.
The break was now final between Venizelos and the royal family.
As for the Allied governments, the attitude of Constantine and Sophia appeared as a betrayal and they appeared as such in the newspapers of the Triple Entente.
The French press accused the Queen of regularly visiting the beaches of Phalerum in order to supply German submarines with fuel.
It must be said that by refusing to go to war, Greece prevented the Franco-British troops of helping Serbia, whose armies soon found themselves overwhelmed by the Austro-Bulgarian coalition, and it made even more uncertain an Allied victory in the Dardanelles.
In retaliation, the Triple Entente ordered Greece to demobilize its army while martial law was proclaimed in Thessaloniki and a blockade was imposed on the Greeks.
The withdrawal of British troops from the Dardanelles in December 1915 reinforced the confidence of a part of the "Old Greece" (meaning the conservative parts of the country, namely around Attica and Peloponnese that constituted the original Greek state in 1830).
This  "New Greece" was composed of a more cosmopolitan and broadly educated populace, while "Old Greece" was essentially a poorer, debt-ridden area, still largely relying on agriculture.
In the eyes of those in "Old Greece," the Greeks living in the new lands were strangers, almost foreigners.
Thus, "oOd Greece" xenophobia was exploited by the King and the church for propaganda purposes in order to get rid of the liberal  government of Venizelos.
However, a by-election followed in the first half of 1915, from which Venizelos again emerged victorious, having the support of "new Greece" (namely the lands awarded to Greece by the Treaty of Bucharest) and of the more liberal, affluent and well-educated elements of "Old Greece" society.
Finally, in April 1916, Constantine I symbolically proclaimed the annexation of Northern Epirus to Greece in response to the Italian intervention into Albania.
Now considered enemies of the Triple Entente, the royal couple faced increasingly violent opposition.
In the confusion, Sophia saved her youngest daughter, Princess Katherine, and ran over 2 km into the woods with the child in her arms.
Several members of the royal family, including Constantine I himself, were wounded and the residence of the rulers was largely destroyed by the fire, which lasted 48 hours.
After these events, the attitude of the royal family in regard to Germany changed considerably.
However, Sophia still had some resentment against the Emperor because of his anger at the time of her marriage and her conversion to Orthodoxy; but the violation of Greece's neutrality by the Triple Entente and the threats against the life of her husband and children gradually changed her views against the Allies.
Sophia redoubled her efforts to help the poor.
On 1 December 1916, Constantine I finally agreed to the French demands, and soldiers of the Triple Entente landed in Athens to seize guns promised by the sovereign two months earlier.
The French fleet bombarded the royal palace in Athens, forcing Sophia and her children to take refuge in the castle cellars for several hours.
Above all, the government of Aristide Briand offered to depose Constantine I and replaced him by his younger brother, Prince George.
However, Russia and Italy refused to intervene because of fears of Greek claims on Asia Minor and the blood ties between Constantine I and Tsar Nicholas II.
First exile

Dethronement and family separation

With the Russian Revolution of 1917 and the deposition of Nicholas II, Constantine and Sophia lost the last of their supporters in the Triple Entente.
Thus, on 10 June 1917 Charles Jonnart, the Allied High Commissioner, asked the Greek Government for the abdication of the King and his replacement by another prince.
The Diadochos George was also considered a pro-German.
Under the threat of an invasion of 10,000 troops in Piraeus, Constantine I  relinquished power in favor of his second son, Prince Alexander.
Nevertheless, Constantine refused to abdicate.
On 11 June, the royal family secretly left the Royal Palace, surrounded by a group of loyalists, and arrived at Tatoi.
The next day, Constantine, Sophia and five of their children left Greece from the port of Oropos, taking the road to exile.
This was the last time Sophia saw her second son, now proclaimed king as Alexander I. Venizelists prohibited any contact between the new sovereign and the rest of the royal family.
After crossing the Ionian Sea and Italy, Sophia and her family settled in Switzerland, mainly between the cities of St. Moritz, Zürich and Lucerne.
In exile, the rulers were soon followed by almost all the members of the royal family who left Greece on the return of Venizelos as head of the government and as Greece entered the war at the side of the Triple Entente.
In addition, the financial position of the royal family was precarious and Constantine I, haunted by a deep sense of failure, soon fell ill.
Already concerned about the health of her husband, Sophia was devastated by the prohibition against contact with her second son.
Even during a short stay in Paris in May 1920, guards closely monitored Constantine's activity.
When Sophia telephoned him at his hotel, a man coldly answered stating "His Majesty is sorry but he can't answer the phone".
With the end of World War I and the signing of the Treaties of Neuilly and Sèvres, the Kingdom of Greece achieved significant territorial gains in Thrace and Anatolia.
The decision of Alexander I to marry Aspasia Manos rather than a European princess displeased both the Head of the government and the King's parents.
Very attached to social conventions, Sophia condemned what she saw as a mésalliance while the Prime Minister saw in this marriage a lost opportunity to get closer to Great Britain.
I

On 2 October 1920, King Alexander I was bitten by a pet monkey as he walked on the royal estate of Tatoi.
However, the Greek government refused to allow Sophia to return to Greece; they feared that the loyalists would benefit from the presence of the Queen in Athens to organize action against them.
Sophia begged the government to allow her entry in the country for what would likely be a last visit with her son.
After several days of negotiations, Olga obtained permission to return to Greece.
Two days later, the remains of the young King were buried in the royal crypt of Tatoi.
The loss of her son and the impossibility to go to his funeral deeply affected Sophia.
Many observers noticed the sadness that perpetually showed on the Queen's face after this loss.
Always opposed to the return of Constantine I and 'Diadochos George' to Greece, the government of Eleftherios Venizelos offered the throne to Prince Paul, the third son of the deposed sovereign.
Supporters of King Constantine I therefore experienced a resurgence of popularity and Venizelos was defeated in the parliamentary elections of November 1920.
For about a month, she was the head of the Greek kingdom but her role was roughly limited to preparing for the restoration of Constantine I.
In the meantime, in Switzerland, the royal family was preparing for the wedding of two of their children with children of King Ferdinand I of Romania.
A few weeks before the death of Alexander I,  'Diadochos George' became engaged to Princess Elisabeth of Romania, while Princess Helen of Greece had secretly been engaged to Crown Prince Carol of Romania since 1913.
Sophia was satisfied with her son's upcoming wedding, but she disapproved of her daughter's romance with the Romanian Crown Prince.
Sophia had no confidence in the future Carol II, whose marriage and divorce from Zizi Lambrino had already shocked her.
Queen of the Hellenes: 2nd tenure (1920-1922)

Return to Greece

The return of Constantine I and Sophia to Athens on 19 December 1920, was accompanied by large demonstrations of joy.
Everywhere in the streets, portraits of Venizelos were pulled and replaced by those of the royal family.
A huge crowd surrounded the royal couple in the streets of the capital and, after returning to the Royal Palace, they had to appear repeatedly on the balcony to greet the people who cheered them.
However, the presence of the sovereigns in Greece did not bring the expected peace.
The antipathy of the great powers toward Constantine I and Sophia was evident on the occasion of the marriage, in Athens, of Princess Helen and Crown Prince Carol of Romania.
Present at the wedding, the ambassador of Great Britain and his wife pointedly refused to salute the Greek King and Queen while clearly showing such respect to Queen Marie of Romania.
For Sophia, the snub was more difficult to bear because she had always been on good terms with the United Kingdom representatives before the deposition of Constantine I and she continued to nurture loving feelings for the country of her mother.
The main source of joy for Sophia after her return to Greece was the birth of her granddaughter Alexandra, on 25 March 1921.
Although initially opposed to Alexander's marriage with Aspasia Manos, the Queen welcomed their daughter with delight and pressed both her husband and eldest son to give her granddaughter the status and titles reserved to members of the royal family.
Constantine I decided to travel there in May 1921 to support the morale; however he wasn't the dynamic Commander-in-chief that led his country to victory in the Balkan Wars of 1912–1913.
Seriously diminished by illness, he had to return to Greece in September, which was perceived as a real military desertion by some.
As for Sophia, she could do more than support her husband and reassume her nursing work with wounded soldiers.
The Greco-Turkish War continued until the Greek defeat of Sakarya in August–September 1921, and the siege and burning of Smyrna (now İzmir) by the Turks in September 1922.
While Mustafa Kemal and his armies gradually reconquered Anatolia and east Thrace, thousands of Greeks were murdered and others fled from Asia Minor to find refuge in Greece.
Abdication of Constantine I

In response to the military defeat by the Turks, a part of the Greek army, commanded by General Nikolaos Plastiras, revolted on 11 September 1922 (on the Julian calendar, 24 September on the Gregorian calendar in use in the rest of the world).
They demanded the abdication of Constantine I and the dissolution of the Hellenic Parliament.
Having consulted his friend, General Ioannis Metaxas, the King abdicated three days later on 27 September in favor of his eldest son, who succeeded him on the throne under the name of George II.


Dowager Queen (1922-1932)
Second exile and concerns for Greece

To ensure their security and stabilize the throne of their son, Constantine I and Sophia once again chose to take the path of exile.
On 30 October 1922 the deposed royal couple, Princesses Irene and Katherine and Prince Nicholas with his family, went again to the port of Oropos to leave their country but, contrary to what happened in 1917, few followers awaited them this time before their departure into exile.
On board the Greek steamboat SS Patris, the royal family arrived in Sicily and moved to the Villa Hygeia in Palermo.
Above all, the life of Prince Andrew, brother of Constantine I, was also threatened in November–December 1922 and only the intervention from foreign governments commuted his sentence from death to exile.
Death of Constantine I and deposition of George II

Increasingly depressed by the events that had shaken Greece and sick with arteriosclerosis, Constantine I developed a deep depression.
Faced with this situation, Sophia's anxiety (already bigger by the fate of George II and other members of the royal family who remained in Greece), only increased.
However, Constantine I died of a brain hemorrhage shortly before their departure, on 11 January 1923, and Sophia found herself even more isolated than she was previously.
After the death of her husband, Sophia wanted to repatriate his remains to be buried in Tatoi but the Greek government refused, with George II being unable to do anything.
In fact, the situation of the new King was increasingly precarious and at the end, he himself went into exile in Romania a few months after the death of his father, on 19 December 1923.
The republic was then proclaimed in Greece on 25 March 1924 and Sophia and the other members of the royal family were stripped of their Hellenic nationality.
However, the Greek royals had maintained their Danish titles since George I ascended to the Greek throne in 1863 and they almost immediately received Danish passports.
Last years

Sophia, now Dowager Queen, left Southern Italy with her daughters Irene and Katherine and moved to Tuscany, in the Villa Bobolina of Fiesole.
From 1924 to 1927, the three women were joined by Princesses Aspasia and Alexandra, much to Sophia's delight, because she was very attached to her granddaughter.
In 1930, Princess Helen also came to live with her mother after her disastrous marriage with King Carol II of Romania ended in divorce.
During summer vacations, the Dowager Queen had the opportunity to see her grandson Prince Michael of Romania, when he came to visit his mother.
Surrounded by her family, Sophia found some stability but, convinced that Greece would not remain a republic forever, refused to acquire the villa where she settled.
She made frequent trips to Germany, where she reunited with her sister Margaret, but also to Great Britain, after having obtained the permission of King George V. The Dowager Queen also witnessed several strong moments in the life of the European elite.
In 1929, she went to Doorn in the Netherlands for the 70th birthday of her brother, the former Emperor William II, whom she had not seen since 1914.
Illness, death and burial

Sick for many years, Sophia saw her condition worsen from 1930, which forced her to go to a hospital in Frankfurt to follow a treatment.
After the New Year celebrations of 1932, Sophia gradually stopped eating and her health declined rapidly.
Sophia's body was transferred to the castle of Friedrichshof, where she rested a few days before being sent to the Russian Church in Florence, where she was buried alongside her husband and mother-in-law.
They stayed there for four years until the restoration of George II on the Greek throne in 1935.
After his restoration on the Greek throne, George II organized the repatriation of the remains of members of his family who died in exile.
An important religious ceremony that brought together, for six days in November 1936, all members of the royal family still alive.
Sophia's body was buried at the royal burial ground at Tatoi Palace, where she still rests today.
Archives

Sophia's letters to her sister Margaret are preserved in the Archive of the House of Hesse, which is kept in Fasanerie Palace in Eichenzell, Germany.
}} Media related to Queen Sophia of Greece at Wikimedia Commons



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
  AssignClass (0e411d55-ea5d-45dc-b266-6d3ceb6aac37)
 Call ID: 0e411d55-ea5d-45dc-b266-6d3ceb6aac37
  Args:
    source: Sophia_of_Prussia
    type: :Woman
  AddLiteral (98ea63e4-187b-4f1c-b2a6-ac279e5be3c0)
 Call ID: 98ea63e4-187b-4f1c-b2a6-ac279e5be3c0
  Args:
    relation: :knownAs
    literal_value: Sophia of Prussia
    source: Sophia_of_Prussia
    literal_type: xsd:string
  AddLiteral (30092d69-f3f1-4ab6-b91e-22db374632a2)
 Call ID: 30092d69-f3f1-4ab6-b91e-22db374632a2
  Args:
    relation: :hasBirthYear
    literal_value: 1870
    source: Sophia_of_Prussia
    literal_type: xsd:integer
  AddLiteral (3424115b-5dae-49c0-b189-ead9a998f419)
 Call ID: 3424115b-5dae-49c0-b189-ead9a998f419
  Args:
    source: Sophia_of_Prussia
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1932
  AssignClass (3d87fa8c-2b94-46f8-827a-338c846c2c41)
 Call ID: 3d87fa8c-2b94-46f8-827a-338c846c2c41
  Args:
    type: :Man
    source: Frederick_III
  AddTriple (55696040-3613-46a7-b6d2-3fe9596b7e55)
 Call ID: 55696040-3613-46a7-b6d2-3fe9596b7e55
  Args:
    relation: :hasFather
    target: Frederick_III
    source: Sophia_of_Prussia
  AssignClass (af81aba3-a4f5-43bc-adee-5d9dc90a6c94)
 Call ID: af81aba3-a4f5-43bc-adee-5d9dc90a6c94
  Args:
    type: :Woman
    source: Victoria_Princess_Royal
  AddTriple (92d4c5fc-ce37-49b0-8ad4-0e7e9fccd2dc)
 Call ID: 92d4c5fc-ce37-49b0-8ad4-0e7e9fccd2dc
  Args:
    target: Victoria_Princess_Royal
    source: Sophia_of_Prussia
    relation: :hasMother
  AssignClass (e95ff5a1-ec7e-4e54-9e04-1f005bb27506)
 Call ID: e95ff5a1-ec7e-4e54-9e04-1f005bb27506
  Args:
    source: Constantine_I
    type: :Man
  AddTriple (1e8a53b2-2255-4937-bf6c-1a624eb8349b)
 Call ID: 1e8a53b2-2255-4937-bf6c-1a624eb8349b
  Args:
    relation: :hasRelation
    source: Sophia_of_Prussia
    target: Constantine_I
  AddLiteral (5fa36bdd-a5a6-4436-b406-488e6ebb0feb)
 Call ID: 5fa36bdd-a5a6-4436-b406-488e6ebb0feb
  Args:
    literal_type: xsd:integer
    source: Sophia_of_Prussia
    literal_value: 1889
    relation: :hasMarriageYear
  AssignClass (e19898f2-a1f8-4445-9453-d82a84e5fb20)
 Call ID: e19898f2-a1f8-4445-9453-d82a84e5fb20
  Args:
    type: :Man
    source: William_I_of_Prussia
  AddTriple (238eb35c-a1bd-4603-ab65-5ea0f26a092e)
 Call ID: 238eb35c-a1bd-4603-ab65-5ea0f26a092e
  Args:
    target: William_I_of_Prussia
    source: Frederick_III
    relation: :hasFather
  AssignClass (8f4e35e1-df89-4ee1-a2f3-0744cf8afcf4)
 Call ID: 8f4e35e1-df89-4ee1-a2f3-0744cf8afcf4
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (b669dfa1-862b-42bc-b946-896689af34f2)
 Call ID: b669dfa1-862b-42bc-b946-896689af34f2
  Args:
    type: :Man
    source: Prince_Albert
  AddTriple (c1bc0448-dcea-4a93-9614-8e780ea17b8e)
 Call ID: c1bc0448-dcea-4a93-9614-8e780ea17b8e
  Args:
    source: Victoria_Princess_Royal
    target: Prince_Albert
    relation: :hasFather
  AddTriple (9bb923a5-11c6-4ab8-abce-331250c5b645)
 Call ID: 9bb923a5-11c6-4ab8-abce-331250c5b645
  Args:
    relation: :hasMother
    target: Queen_Victoria
    source: Victoria_Princess_Royal
  AssignClass (5749773f-34cb-4c6e-bd99-83a1187d4677)
 Call ID: 5749773f-34cb-4c6e-bd99-83a1187d4677
  Args:
    type: :Man
    source: William_II_of_Germany
  AddTriple (7d70193b-b579-429e-9d79-9b65d2d12746)
 Call ID: 7d70193b-b579-429e-9d79-9b65d2d12746
  Args:
    relation: :hasBrother
    target: William_II_of_Germany
    source: Sophia_of_Prussia
  AssignClass (cd854ad3-29be-47d9-b7ce-13b4a5838d56)
 Call ID: cd854ad3-29be-47d9-b7ce-13b4a5838d56
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AddTriple (dfa3f1e6-15a5-499f-961e-7bf4e45c2cba)
 Call ID: dfa3f1e6-15a5-499f-961e-7bf4e45c2cba
  Args:
    source: Sophia_of_Prussia
    target: Margaret_of_Prussia
    relation: :hasSister
  AssignClass (ee977c68-1034-480d-8e17-02d4b09f0698)
 Call ID: ee977c68-1034-480d-8e17-02d4b09f0698
  Args:
    type: :Man
    source: Sigismund_of_Prussia
  AddTriple (9bf060ca-1d25-44d6-8b98-33afd6004e30)
 Call ID: 9bf060ca-1d25-44d6-8b98-33afd6004e30
  Args:
    target: Sigismund_of_Prussia
    source: Sophia_of_Prussia
    relation: :hasBrother
  AssignClass (55c64479-9f54-4e1b-9b14-7ed0128a51fe)
 Call ID: 55c64479-9f54-4e1b-9b14-7ed0128a51fe
  Args:
    source: Waldemar_of_Prussia
    type: :Man
  AddTriple (02d94c67-1017-4a45-b069-518ea27c1314)
 Call ID: 02d94c67-1017-4a45-b069-518ea27c1314
  Args:
    source: Sophia_of_Prussia
    target: Waldemar_of_Prussia
    relation: :hasBrother
  AssignClass (7ab20e36-1632-480b-a806-d6413a3a2dfc)
 Call ID: 7ab20e36-1632-480b-a806-d6413a3a2dfc
  Args:
    type: :Woman
    source: Viktoria_of_Prussia
  AddTriple (f1e72c73-f013-4ad9-8117-e0a31d0cf05c)
 Call ID: f1e72c73-f013-4ad9-8117-e0a31d0cf05c
  Args:
    relation: :hasSister
    source: Sophia_of_Prussia
    target: Viktoria_of_Prussia
  AssignClass (1f26651c-1a72-43b3-83ae-2b02a0c45f15)
 Call ID: 1f26651c-1a72-43b3-83ae-2b02a0c45f15
  Args:
    type: :Man
    source: Alexander_I_of_Greece
  AddTriple (ba186965-47d2-4a67-8e5c-9c8eef92f6bf)
 Call ID: ba186965-47d2-4a67-8e5c-9c8eef92f6bf
  Args:
    relation: :hasSon
    target: Alexander_I_of_Greece
    source: Sophia_of_Prussia
  AssignClass (d591bb55-ab7b-4ce7-adf0-08bcf59a77fb)
 Call ID: d591bb55-ab7b-4ce7-adf0-08bcf59a77fb
  Args:
    type: :Man
    source: George_II_of_Greece
  AddTriple (bc259166-3944-4f37-8261-8253cbdf70a1)
 Call ID: bc259166-3944-4f37-8261-8253cbdf70a1
  Args:
    relation: :hasSon
    source: Sophia_of_Prussia
    target: George_II_of_Greece
  AssignClass (2444ecc8-bef6-4f69-933f-78986132afc0)
 Call ID: 2444ecc8-bef6-4f69-933f-78986132afc0
  Args:
    type: :Woman
    source: Katherine_of_Greece
  AddTriple (65d2e2c0-d450-4ebd-9ffd-03e014f149ee)
 Call ID: 65d2e2c0-d450-4ebd-9ffd-03e014f149ee
  Args:
    target: Katherine_of_Greece
    source: Sophia_of_Prussia
    relation: :hasDaughter
  AssignClass (1a082db5-c8ae-4510-9b27-fbc6f40058fd)
 Call ID: 1a082db5-c8ae-4510-9b27-fbc6f40058fd
  Args:
    source: Helen_of_Greece
    type: :Woman
  AddTriple (9fc77d0a-d6b8-467d-afe2-8fb3a09d8f38)
 Call ID: 9fc77d0a-d6b8-467d-afe2-8fb3a09d8f38
  Args:
    target: Helen_of_Greece
    source: Sophia_of_Prussia
    relation: :hasDaughter
  AssignClass (d83e2406-69ea-495c-95ad-b0beda3415c8)
 Call ID: d83e2406-69ea-495c-95ad-b0beda3415c8
  Args:
    source: Irene_of_Greece
    type: :Woman
  AddTriple (b0131a76-ba2b-437a-9f31-6c8cf5072b0c)
 Call ID: b0131a76-ba2b-437a-9f31-6c8cf5072b0c
  Args:
    relation: :hasDaughter
    source: Sophia_of_Prussia
    target: Irene_of_Greece
  AssignClass (e61dc316-c8fe-45d4-9ad5-3981f7b2402b)
 Call ID: e61dc316-c8fe-45d4-9ad5-3981f7b2402b
  Args:
    source: Paul_of_Greece
    type: :Man
  AddTriple (8c06cf63-0fd7-4659-8605-e4a96786ec54)
 Call ID: 8c06cf63-0fd7-4659-8605-e4a96786ec54
  Args:
    source: Sophia_of_Prussia
    target: Paul_of_Greece
    relation: :hasSon
  AssignClass (d80dbc77-c4c5-4fbb-8649-38b803a4aab3)
 Call ID: d80dbc77-c4c5-4fbb-8649-38b803a4aab3
  Args:
    source: George_I_of_Greece
    type: :Man
  AssignClass (dd39555f-6cf4-4955-b52f-66ce0dc74c8e)
 Call ID: dd39555f-6cf4-4955-b52f-66ce0dc74c8e
  Args:
    type: :Woman
    source: Queen_Olga_of_Greece
  AddTriple (3e616f1b-b5be-4820-963d-7c720b98f58a)
 Call ID: 3e616f1b-b5be-4820-963d-7c720b98f58a
  Args:
    relation: :hasFather
    source: Constantine_I
    target: George_I_of_Greece
  AddTriple (885e218b-6978-460d-9947-5fe89332a271)
 Call ID: 885e218b-6978-460d-9947-5fe89332a271
  Args:
    relation: :hasMother
    source: Constantine_I
    target: Queen_Olga_of_Greece
  Finish (aacfa5af-b448-456b-9eaf-a71888fc2ace)
 Call ID: aacfa5af-b448-456b-9eaf-a71888fc2ace
  Args: