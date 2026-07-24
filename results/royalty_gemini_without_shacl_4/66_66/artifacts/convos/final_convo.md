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
Louis Francis Albert Victor Nicholas Mountbatten, 1st
Earl Mountbatten of Burma (born Prince Louis of Battenberg; 25 June 1900 – 27 August 1979), commonly known as Lord Mountbatten, was a British statesman, naval officer, and member of the British royal family.
A maternal uncle of Prince Philip and second cousin once removed of Queen Elizabeth II, he served in the Royal Navy during both world wars and rose to become Supreme Allied Commander, South East Asia Command, in the later stages of the Second World War.
As the last viceroy of India, Mountbatten also oversaw its partition into the Dominions of India and Pakistan and the integration of the princely states into India.
Mountbatten later held senior posts in the post‐war armed forces, serving as First Sea Lord and then as Chief of the Defence Staff until 1965, making him the longest-serving professional head of the British Armed Forces to date.
During this period Mountbatten also served as chairman of the NATO Military Committee for a year.
He remained closely associated with the royal family throughout his life and acted as a mentor to his great‐nephew, the future King Charles III.
His private life attracted scrutiny, and after his death allegations of sexual abuse were made, some of which were dismissed by official inquiries.
In August 1979, Mountbatten was assassinated by the Provisional Irish Republican Army when a bomb exploded aboard his fishing boat in Mullaghmore, County Sligo.
Early life

Mountbatten, then styled Prince Louis of Battenberg, was born on 25 June 1900 at Frogmore House in the Home Park, Windsor, Berkshire.
He was the youngest child and second son of Prince Louis of Battenberg and his wife Princess Victoria of Hesse and by Rhine.
Mountbatten's maternal grandparents were Louis IV, Grand Duke of Hesse, and Princess Alice of the United Kingdom, a daughter of Queen Victoria and Prince Albert of Saxe-Coburg and Gotha.
His paternal grandparents were Prince Alexander of Hesse and by Rhine and Julia, Princess of Battenberg.
Their marriage was morganatic, as Julia was not of royal lineage; consequently, Mountbatten and his father bore the style Serene Highness rather than Royal Highness, were ineligible for the title Princes of Hesse, and held the lesser Battenberg designation.
His elder siblings were Princess Alice of Battenberg (mother of Prince Philip, Duke of Edinburgh), Princess Louise of Battenberg (later Queen Louise of Sweden), and Prince George of Battenberg (later George Mountbatten, 2nd Marquess of Milford Haven).
Mountbatten was baptised in the large drawing room of Frogmore House on 17 July by the Dean of Windsor, Philip Eliot.
His godparents were Queen Victoria (his maternal great-grandmother), Nicholas II of Russia (his maternal uncle through marriage and paternal second cousin, represented by the child's father) and Prince Francis Joseph of Battenberg (his paternal uncle, represented by Lord Edward Clinton).
Mountbatten's nickname among family and friends was "Dickie"; although "Richard" was not among his given names.
His great-grandmother, Queen Victoria, had originally suggested "Nicky", but as the name was already widely used within the Russian imperial family (particularly for Nicholas II), it was altered to "Dickie" to avoid confusion.
Mountbatten was educated at home for the first ten years of his life; he was then sent to Lockers Park School in Hertfordshire and later to the Royal Naval College, Osborne, in May 1913.
Mountbatten's mother's younger sister was the Russian Empress Alexandra Feodorovna.
As a child he visited the imperial court at St Petersburg and became close to the Russian imperial family, harbouring romantic feelings for his maternal first cousin Grand Duchess Maria Nikolaevna, whose photograph he kept at his bedside for the rest of his life.
Mountbatten adopted his surname as a result of World War I. From 1914 to 1918, Britain and its allies were at war with the Central Powers, led by the German Empire.
To appease British nationalist sentiment, in 1917 King George V issued a royal proclamation changing the name of the British royal house from the German House of Saxe-Coburg and Gotha to the House of Windsor.
The King's British relatives with German names and titles followed suit, with Mountbatten's father adopting the surname Mountbatten, an anglicisation of Battenberg.
His father was subsequently created Marquess of Milford Haven.
First World War

At the age of 16, Mountbatten was posted as midshipman to the battlecruiser HMS Lion in July 1916 and, after seeing action in August, transferred to the battleship HMS Queen Elizabeth during the closing phases of the First World War.
In 1917, when the royal family abandoned their German names and titles and adopted the more British-sounding "Windsor", Mountbatten acquired the courtesy title appropriate to a younger son of a marquess, becoming known as Lord Louis Mountbatten (Lord Louis for short) until he was created a peer in his own right in 1946.
While still an acting-sub-lieutenant, Mountbatten was appointed first lieutenant (second-in-command) of the P-class sloop HMS P. 31 on 13 October 1918 and was confirmed as a substantive sub-lieutenant on 15 January 1919.
Mountbatten attended Christ's College, Cambridge, for two terms from October 1919, studying English literature (including John Milton and Lord Byron) in a programme designed to augment the education of junior officers whose studies had been curtailed by the war.
Interwar period

Mountbatten was posted to the battlecruiser HMS Renown in March 1920 and accompanied Edward, Prince of Wales, on a royal tour of Australia.
Early in 1921, Royal Navy personnel were deployed for civil defence duties as serious industrial unrest appeared imminent, and Mountbatten was required to command a platoon of stokers in Northern England, many of whom had never handled a rifle before.
He transferred to the battlecruiser HMS Repulse in March 1921 and again accompanied the Prince of Wales, this time on a royal tour of India and Japan.
Edward and Mountbatten formed a close friendship during the trip.
Mountbatten survived the deep defence cuts known as the Geddes Axe; fifty-two percent of the officers of his year had left the Royal Navy by the end of 1923.
Pursuing his interests in technological development and gadgetry, Mountbatten joined the Portsmouth Signals School in August 1924 and then briefly studied electronics at the Royal Naval College, Greenwich.
Promoted lieutenant commander on 15 April 1928, Mountbatten returned to the Signals School in July 1929 as Senior Wireless Instructor.
In 1934, Mountbatten received his first command, the destroyer HMS Daring.
He successfully brought Wishart back to Malta and then attended the funeral of George V in January 1936.
Mountbatten was appointed a personal naval aide-de-camp to King Edward VIII on 23 June 1936, and, having joined the Naval Air Division of the Admiralty in July 1936, he attended the coronation of George VI and Elizabeth in May 1937.
Within the Admiralty, Mountbatten was known as "The Master of Disaster" for his penchant for getting into difficult situations.
Second World War

When war broke out in September 1939, Mountbatten became Captain (D) (commander) of the 5th Destroyer Flotilla aboard HMS Kelly, which soon became noted for its exploits.
In late 1939 he brought the Duke of Windsor back from exile in France, and in early May 1940 Mountbatten led a British convoy through fog to evacuate Allied forces participating in the Namsos campaign during the Norwegian campaign.
On the night of 9–10 May 1940, Kelly was torpedoed amidships by a German E-boat S 31 off the Dutch coast, and Mountbatten thereafter commanded the 5th Destroyer Flotilla from the destroyer HMS Javelin.
Mountbatten turned to port to match a German course change, a move described as "a rather disastrous" one, as the directors swung off and lost target, resulting in Javelin being struck by two torpedoes.
Coward, a personal friend of Mountbatten, incorporated some of his speeches into the film.
Mountbatten was mentioned in despatches on 9 August 1940 and 21 March 1941, and was awarded the Distinguished Service Order in January 1941.
In August 1941, Mountbatten was appointed captain of the aircraft carrier HMS Illustrious, which was in Norfolk, Virginia, for repairs following action at Malta in January.
Mountbatten was appalled at the US naval base's lack of preparedness and, drawing on Japan's history of launching wars with surprise attacks, the recent British success at the Battle of Taranto, and the demonstrated effectiveness of aircraft against warships, accurately predicted that the United States would enter the war after a Japanese surprise attack on Pearl Harbor.
Mountbatten was a favourite of Winston Churchill.
On 27 October 1941, Mountbatten replaced Admiral of the Fleet Sir Roger Keyes as Chief of Combined Operations Headquarters and was promoted to commodore.
Noteworthy technical achievements by Mountbatten and his staff included the construction of "PLUTO", an underwater oil pipeline to Normandy; an artificial Mulberry harbour built from concrete caissons and sunken ships; and the development of tank-landing ships.
Mountbatten also proposed Project Habakkuk to Churchill, an ambitious plan for an unsinkable 600-metre aircraft carrier made from reinforced ice ("Pykrete").
As commander of Combined Operations, Mountbatten and his staff planned the highly successful Bruneval raid, which gained important intelligence and captured part of a German Würzburg radar installation, along with one of its technicians, on 27 February 1942.
Mountbatten recognised that surprise and speed were essential to securing the radar and concluded that an airborne assault was the only viable method.
On 18 March 1942, he was promoted to the acting rank of vice admiral and given the honorary ranks of lieutenant general and air marshal to provide the authority required for his duties in Combined Operations.
Despite the misgivings of General Sir Alan Brooke, the Chief of the Imperial General Staff, Mountbatten was placed on the Chiefs of Staff Committee.
Mountbatten was central to the planning and promotion of the assault, which proved a marked failure, with casualties of almost 60%, the great majority of them Canadians.
Mountbatten claimed that the lessons learned from the Dieppe Raid were necessary for planning the Normandy invasion on D-Day nearly two years later.
SEAC and Burma campaign

In August 1943, Churchill appointed Mountbatten Supreme Allied Commander, South East Asia Command (SEAC), with promotion to acting full admiral.
British interpreter Hugh Lunghi recounted an embarrassing episode during the Potsdam Conference when Mountbatten, hoping for an invitation to visit the Soviet Union, repeatedly attempted to impress Joseph Stalin with his former connections to the Russian imperial family.
Mountbatten left with his tail between his legs.
"


During his time as Supreme Allied Commander of the Southeast Asia Theatre, Mountbatten's command oversaw the recapture of Burma from the Japanese by General Sir William Slim.
South East Asia Command was disbanded in May 1946, and Mountbatten returned home with the substantive rank of rear-admiral.
That year, he was made a Knight Companion of the Garter and created Viscount Mountbatten of Burma, of Romsey in the County of Southampton, as a victory title for war service.
In 1947, he was further created Earl Mountbatten of Burma and Baron Romsey, of Romsey in the County of Southampton.
Following the war, Mountbatten largely shunned the Japanese out of respect for his men killed during the conflict, and, in accordance with his will, Japan was not invited to send diplomatic representatives to his funeral in 1979.
Viceroy of India

Mountbatten's experience in the region, and in particular his perceived Labour sympathies at the time, together with his wife's longstanding friendship and collaboration with V. K. Krishna Menon, led Menon to put forward Mountbatten's name alone as a viceregal candidate acceptable to the Indian National Congress, in clandestine meetings with Sir Stafford Cripps and Clement Attlee.
Attlee advised King George VI to appoint Mountbatten Viceroy of India on 20 February 1947, charging him with overseeing the transition of British India to independence no later than 30 June 1948.
Mountbatten's instructions were to avoid partition and preserve a united India as the outcome of the transfer of power, but he was authorised to adapt to a changing situation in order to secure Britain's prompt withdrawal with minimal reputational damage.
Mountbatten arrived in India on 22 March by air from London.
Mountbatten concluded that the situation was too volatile to wait even a year before granting independence.
Mountbatten also hurried the process so that he could return to the Royal Navy.
Mountbatten was fond of Congress leader Jawaharlal Nehru and his liberal outlook for the country, and, through the efforts of their close mutual friend, Krishna Menon, developed a depth of feeling and intimacy with Nehru that was shared by his wife, Edwina.
He felt differently about the Muslim League leader Muhammad Ali Jinnah, but recognised his influence, stating "If it could be said that any single man held the future of India in the palm of his hand in 1947, that man was Mohammad Ali Jinnah."
During his meeting with Jinnah on 5 April 1947, Mountbatten tried to persuade him of the merits of a united India, citing the difficultly of dividing the mixed provinces of Punjab and Bengal, but Jinnah remained unyielding in his goal of establishing a separate Muslim state called Pakistan.
Given the British government's recommendation to grant independence quickly, Mountbatten concluded that a united India was no longer an achievable goal and resigned himself to a plan for partition, creating the independent nations of India and Pakistan.
During his meeting with Mountbatten, Gandhi asked him to invite Jinnah to form a new central government, but Mountbatten never conveyed Gandhi's proposal to Jinnah.
When Mountbatten's accelerated timeline offered the prospect of attaining independence soon, political sentiment shifted.
Given Mountbatten's determination, the inability of Nehru and Sardar Patel to reach an accommodation with the Muslim League, and Jinnah's obstinacy, all Indian party leaders (except Gandhi) acquiesced to Jinnah's plan to divide India, which in turn eased Mountbatten's task.
Mountbatten also developed a strong relationship with the Indian princes, who ruled those parts of India not directly under British administration, and his intervention was decisive in persuading the vast majority of them to see the advantages of joining the Indian Union.
Mountbatten brought forward the date of partition from June 1948 to 15 August 1947.
This left 14 million people on the "wrong" side of the line, and many fled to "safety" on the other side when the boundaries were announced.
Independence of India and Pakistan

When India and Pakistan attained independence at midnight on 14–15 August 1947, Mountbatten was alone in his study at the Viceroy's House, reflecting that for a few minutes more he remained the most powerful man on Earth.
Notwithstanding the self-promotion of his own role in Indian independence – notably in the television series The Life and Times of Admiral of the Fleet Lord Mountbatten of Burma, produced by his son-in-law Lord Brabourne, and in Freedom at Midnight by Dominique Lapierre and Larry Collins, for which he was the principal quoted source – his record is regarded as very mixed.
One common view is that he hastened the process of independence unduly and recklessly, foreseeing vast disruption and loss of life and not wanting this to occur on his watch, but thereby helping to bring it about indirectly, especially in Punjab and Bengal.
John Kenneth Galbraith, the Canadian-American Harvard University economist who advised Indian governments during the 1950s and, as an intimate of Nehru, served as the American ambassador from 1961 to 1963, was a particularly harsh critic of Mountbatten in this regard.
According to historian Lawrence James, Mountbatten had no option but to cut and run, the alternative being British involvement in a civil war with no viable exit.
The creation of Pakistan was never emotionally accepted by many British leaders, Mountbatten among them.
Jinnah refused Mountbatten's offer to serve as Governor-General of Pakistan.
When Mountbatten was asked by Collins and Lapierre whether he would have sabotaged the creation of Pakistan had he known that Jinnah was dying of tuberculosis, he replied, "Most probably".
Governor-General of India

Mountbatten became the first Governor-General of independent India on 15 August 1947 at the request of Indian Prime Minister Jawaharlal Nehru.
Life magazine noted of his reception in India that, "The people gathered in the streets to cheer Mountbatten as no European had ever been cheered before.
"


During his tenure as governor-general, which lasted until 21 June 1948, Mountbatten played a significant role in the political integration of India and persuaded many princely states to join the new dominion.
On his advice, India took the issue of Kashmir to the newly formed United Nations in January 1948.
Accounts differ on the future Mountbatten desired for Kashmir.
Pakistani sources suggest that he favoured the accession of Kashmir to India, citing his close relationship with Nehru, while Mountbatten's own account states that he simply wanted Maharaja Hari Singh to make a decision.
He made several attempts to mediate between the Congress leaders, Muhammad Ali Jinnah, and Hari Singh on issues relating to accession of Kashmir, though he was largely unsuccessful in resolving the conflict.
After his tenure concluded, Mountbatten continued to enjoy close relations with Nehru and the post-Independence Indian leadership, and he was welcomed as a former governor-general on subsequent visits, including during an official trip in March 1956.
The Pakistani government, by contrast, held a negative view of Mountbatten for what it perceived as his hostile attitude towards Pakistan and deemed him persona non grata, barring him from transiting its airspace during the same visit.
Later career

After leaving India, Mountbatten served as commander of the 1st Cruiser Squadron in the Mediterranean Fleet and, having been granted the substantive rank of vice-admiral on 22 June 1949, became Second-in-Command of the Mediterranean Fleet in April 1950.
He was promoted to the substantive rank of full admiral on 27 February 1953, and in March 1953 was appointed Personal aide-de-camp to the Queen.
Mountbatten served his final posting at the Admiralty as First Sea Lord and Chief of the Naval Staff from April 1955 to July 1959, a position his father had held some forty years earlier.
During the Suez Crisis of 1956, Mountbatten strongly advised his old friend, Prime Minister Anthony Eden against the Conservative government's plan to seize the Suez Canal in conjunction with France and Israel.
His advice was not taken.
Eden insisted that Mountbatten should not resign, and Mountbatten instead worked hard to prepare the Royal Navy for war with characteristic professionalism and thoroughness.
Despite his military rank, Mountbatten was initially ignorant of the physics involved in a nuclear explosion and had to be reassured that the fission reactions from the Bikini Atoll tests would not spread through the oceans and destroy the planet.
After leaving the Admiralty, Mountbatten became Chief of the Defence Staff.
Ian Jacob, co-author of the 1963 Report on the Central Organisation of Defence that underpinned these reforms, described Mountbatten as "universally mistrusted in spite of his great qualities".
The Defence Secretary, Denis Healey, interviewed the forty most senior officials in the Ministry of Defence; only one, Sir Kenneth Strong, a personal friend of Mountbatten, recommended his reappointment.
"


Mountbatten was appointed Colonel of The Life Guards and Gold Stick in Waiting on 29 January 1965, and Life Colonel Commandant of the Royal Marines later that year.
Mountbatten was elected a Fellow of the Royal Society and received an honorary doctorate from Heriot-Watt University in 1968.
The following year, Mountbatten attended an official White House dinner, during which he held a 20-minute conversation with Richard Nixon and Secretary of State William P. Rogers.
In January 1971, Nixon hosted Juan Carlos and his wife, Sofia (sister of the exiled King Constantine), during a visit to Washington, and later that year The Washington Post published an article alleging that the Nixon administration was seeking to persuade Franco to retire in favour of the young Bourbon prince.
From 1967 until 1978, Mountbatten served as president of the United World Colleges Organisation, then represented by a single institution: Atlantic College in South Wales.
Under his presidency and personal involvement, the United World College of South East Asia was established in Singapore in 1971, followed by the United World College of the Pacific in Victoria, British Columbia, in 1974.
In 1978, he passed the presidency to his great-nephew, Charles, Prince of Wales.
Mountbatten also helped to launch the International Baccalaureate; in 1971 he presented the first IB diplomas in the Greek Theatre of the International School of Geneva, Switzerland.
In 1975, Mountbatten finally visited the Soviet Union, leading the United Kingdom's delegation as the personal representative of Queen Elizabeth II at the celebrations marking the 30th anniversary of Victory Day in the Second World War in Moscow.
Alleged plots against Harold Wilson

Peter Wright, in his 1987 book Spycatcher, claimed that in May 1968 Mountbatten attended a private meeting with press baron Cecil King and the government's Chief Scientific Adviser, Solly Zuckerman.
At the meeting, King allegedly urged Mountbatten to lead a government of national salvation.
Zuckerman pointed out that such an idea amounted to "rank treachery" and it came to nothing owing to Mountbatten's reluctance to act.
In contrast, Andrew Lownie has suggested that it took the intervention of the Queen to dissuade Mountbatten from plotting against Wilson.
In 2006, the BBC documentary The Plot Against Harold Wilson alleged that there had been another plot involving Mountbatten to oust Wilson during his second term in office (1974–1976).
The documentary makers alleged that a coup was planned to overthrow Wilson and replace him with Mountbatten, using these private armies and sympathisers within the military and MI5.
The first official history of MI5, The Defence of the Realm (2009), implied that there had indeed been a plot against Wilson and that MI5 maintained a file on Mountbatten.
This had already been confirmed by former cabinet secretary Lord Hunt, who concluded in a secret inquiry in 1996 that "there is absolutely no doubt at all that a few, a very few, malcontents in MI5 ... a lot of them like Peter Wright who were right-wing, malicious and had serious personal grudges – gave vent to these and spread damaging malicious stories about that Labour government."


Personal life

Marriage and sexual relationships

Mountbatten was married on 18 July 1922 to Edwina Cynthia Annette Ashley, daughter of Wilfred William Ashley, later 1st
Baron Mount Temple, himself a grandson of Anthony Ashley-Cooper, 7th Earl of Shaftesbury.
During their stay in California, the newlyweds appeared in a silent home movie by Charlie Chaplin, called Nice And Friendly, which was not shown in cinemas.
Mountbatten later admitted: "Edwina and I spent all our married lives getting into other people's beds."
Yola Letellier's life story was the inspiration for Colette's novel Gigi.
After Edwina's death in 1960, Mountbatten was involved in relationships with young women, according to his daughter Patricia, his secretary John Barratt, his valet Bill Evans, and William Stadiem, an employee of Madame Claude.
In 2019, Ron Perks, Mountbatten's driver in Malta in 1948, alleged that Mountbatten had visited the Red House, an upmarket gay brothel in Rabat used by naval officers.
Andrew Lownie, a fellow of the Royal Historical Society, wrote that the United States Federal Bureau of Investigation (FBI) maintained files concerning Mountbatten's alleged homosexuality.
Lownie also interviewed several young men who claimed to have been in a relationship with Mountbatten.
John Barratt, Mountbatten's personal and private secretary for twenty years, stated that Mountbatten was not homosexual and that it would have been impossible for such a fact to have been concealed from him.
Wealth

Due to Edwina's considerable inheritance, the couple were extremely wealthy during their married life.
Following the death of her maternal grandfather, Sir Ernest Cassel, in 1921, Edwina received a life-interest trust fund comprising .mw-parser-output .frac{white-space:nowrap}.mw-parser-output .frac .num,.mw-parser-output .frac .den{font-size:80%;line-height:0;vertical-align:super}.mw-parser-output .frac .den{vertical-align:sub}.mw-parser-output .sr-only{border:0;clip:rect(0,0,0,0);clip-path:polygon(0px 0px,0px 0px,0px 0px);height:1px;margin:-1px;overflow:hidden;padding:0;position:absolute;width:1px}25⁄64 of Cassel's residuary estate.
After taxes and other expenses, the net value of the trust fund Edwina received from her grandfather's will was approximately £1,600,000.
In contrast to his new wife's extreme wealth, Mountbatten's salary as a Royal Navy lieutenant was £310 a year (equivalent to £17,200 in 2024), which was doubled by his private income.
Edwina later inherited the country seat of Broadlands, Hampshire, from her father, Lord Mount Temple.
Mountbatten would later confide to his elder daughter that he and Edwina sometimes struggled to spend their £60,000 post-tax annual income during the early years of their marriage.
Upon Mountbatten's appointment as Supreme Allied Commander in South East Asia during the later stages of the war, his salary was £6,000, upon which he paid £2,400 in Indian income tax.
By the end of the Second World War, the highest rate of income tax in Great Britain had risen to 19s 6d in the pound (97.5%), reducing the post-tax income they enjoyed from Edwina's fund to £4,500.
The Mountbattens sought a Private members' bills in the Parliament of the United Kingdom, and in 1949 the "Mountbatten Estate Bill" was introduced to amend the terms of Edwina's trust fund by removing the restrictions her grandfather's will placed on her borrowing against the capital assets or anticipating future income.
The justification for the bill was that Lord and Lady Mountbatten undertook an exceptionally large number of public duties, which they argued placed a significant drain on their private wealth.
In an address to the House of Lords committee, Edwina's representative, Sir Walter Monckton KC, noted that she had enjoyed a post-tax income of about £40,000 prior to the war.
Following Edwina's death in 1960, her gross personal estate was valued at £589,655, with a net value of £478,618.
Death duties of £333,153 were levied on her personal estate; Mountbatten reportedly complained to friends that his net inheritance from his wife's estate amounted to about one shilling on the pound (5%).
Following his own death in 1979, Mountbatten's estate was valued for probate purposes at £2,196,494 (equivalent to £11,000,000 in 2025).
Daughter as heir

Lord and Lady Mountbatten had two daughters: Patricia Knatchbull (14 February 1924 – 13 June 2017), who served at times as lady-in-waiting to Queen Elizabeth II, and Lady Pamela Hicks (born 19 April 1929), who accompanied her parents to India in 1947–1948 and also served as a lady-in-waiting to the Queen.
As Mountbatten had no sons when he was created Viscount Mountbatten of Burma, of Romsey in the County of Southampton, on 27 August 1946, and subsequently Earl Mountbatten of Burma and Baron Romsey, in the County of Southampton, on 18 October 1947, the Letters Patent were drafted so that, in the event he left no sons or male-line issue, the titles could pass to his daughters in order of seniority.
Leisure interests

Mountbatten was passionate about genealogy, an interest he shared with other European royalty and nobility; according to Ziegler, he spent a great deal of his leisure time studying his links with European royal houses.
Throughout his career, Mountbatten consistently sought to secure as many orders and decorations as possible.
Like many members of the royal family, Mountbatten was an aficionado of polo.
Mentorship of King Charles III

Mountbatten was a strong influence in the upbringing of his great-nephew, the future King Charles III, and later acted as a mentor.
"Honorary Grandfather" and "Honorary Grandson", they fondly called each other according to Jonathan Dimbleby's biography of the then-Prince, though both the Ziegler biography of Mountbatten and Dimbleby's account suggest that the results of this mentorship were mixed.
From time to time, he strongly upbraided the Prince for showing tendencies towards the idle, pleasure-seeking dilettantism of his predecessor as Prince of Wales, King Edward VIII, whom Mountbatten had known well in their youth.
Yet he also encouraged Charles to enjoy the bachelor life while he could, and then to marry a young and inexperienced girl so as to ensure a stable married life.
His qualification for offering advice to this particular heir to the throne was unique.
It was Mountbatten who had arranged the visit of King George VI and Queen Elizabeth to Dartmouth Royal Naval College on 22 July 1939, taking care to include the young Princesses Elizabeth and Margaret in the invitation, and assigning his nephew, Cadet Prince Philip of Greece, to keep them amused while their parents toured the facility.
A few months later, however, his efforts nearly came to naught when he received a letter from his sister Alice in Athens informing him that Philip was visiting her and had agreed to repatriate permanently to Greece.
Within days, Philip received a command from his cousin and sovereign, King George II of Greece, to resume his naval career in Britain which, though given without explanation, the young prince obeyed.
In 1974, Mountbatten began corresponding with Charles about a potential marriage to his granddaughter, Amanda Knatchbull, who was also Charles's second cousin.
Around this time, he also recommended that the 25-year-old prince get on with "sowing some wild oats".
Charles dutifully wrote to Amanda's mother (who was also his godmother and his father's first cousin), Lady Brabourne, expressing his interest.
In February 1975, Charles visited New Delhi to play polo and was shown around Rashtrapati Bhavan, the former Viceroy's House, by Mountbatten.
Four years later, Mountbatten secured an invitation for himself and Amanda to accompany Charles on his planned 1980 tour of India.
Prince Philip believed that the Indian public's reception would more likely reflect their response to the uncle than to the nephew.
Lord Brabourne counselled that the intense scrutiny of the press would be more likely to drive Mountbatten's godson and granddaughter apart than together.
Charles was rescheduled to tour India alone, but Mountbatten did not live to the planned date of departure.
When Charles finally proposed marriage to Amanda later in 1979, the circumstances had changed and she refused him.
Allegations of paedophilia

In 2019, files were opened showing that the FBI had been aware in the 1940s of allegations that Mountbatten was homosexual and a paedophile.
The FBI file on Mountbatten, begun after he became Supreme Allied Commander in Southeast Asia in 1944, described Mountbatten and his wife Edwina as "persons of extremely low morals", and included a claim by American author Elizabeth, Baroness Decies, that Mountbatten was known to be a homosexual and had "a perversion for young boys".
Norman Nield, Mountbatten's driver from 1942 to 1943, told the tabloid New Zealand Truth that he had transported young boys aged eight to twelve who had been procured for Mountbatten to his official residence, and that he had been paid to keep quiet.
Robin Bryans also claimed, in the Irish magazine Now, that Mountbatten and Anthony Blunt, among others, were part of a ring that engaged in homosexual orgies and procured boys in their first year at public schools such as Portora Royal School in Enniskillen.
Former residents of the Kincora Boys' Home in Belfast have asserted that they were trafficked to Mountbatten at Classiebawn Castle, his residence in Mullaghmore, County Sligo.
In October 2022, Arthur Smyth, a former resident of Kincora, waived his anonymity to make allegations of child abuse against Mountbatten.
Smyth claims that he was raped twice by Mountbatten in encounters facilitated by the house father of Kincora.
In 2025, journalist Chris Moore published a book, Kincora: Britain's Shame, in which he detailed allegations by five men that Mountbatten had raped them when they were children in Kincora.
Television appearances

Instead of writing a memoir, Mountbatten presented a television series.
Produced by Thames Television for ITV in 1969, the 12-episode documentary The Life and Times of Lord Mountbatten retraced his life and the major historical events of the century.
On 27 April 1977, shortly before his 77th birthday, he became the first member of the royal family to appear on the TV guest show This Is Your Life.
Assassination

Mountbatten usually holidayed at his summer home, Classiebawn Castle, on the Mullaghmore Peninsula in County Sligo, in the north-west of Ireland.
In 1978, the IRA had allegedly attempted to shoot Mountbatten as he was aboard his boat, but poor weather had prevented the sniper from taking his shot.
On 27 August 1979, Mountbatten went lobster-potting and tuna fishing in his 30-foot (9-metre) wooden boat, Shadow V, which had been moored in the harbour at Mullaghmore.
The boat was destroyed by the force of the blast and Mountbatten's legs were all but severed.
Then aged 79, he was pulled alive from the water by nearby fishermen, but died from his injuries before reaching the shore.
Also aboard were his elder daughter Patricia, Lady Brabourne; her husband Lord Brabourne; their twin sons Nicholas and Timothy Knatchbull; Lord Brabourne's mother Doreen, Dowager Lady Brabourne; and Paul Maxwell, a young crew member from Enniskillen in County Fermanagh.
Doreen, Dowager Lady Brabourne (aged 83), died from her injuries the following day.
Many in the Irish-American community were appalled by the attack, particularly as many American soldiers had served under Mountbatten during the Second World War.
Jim Rooney, son of Pittsburgh Steelers president Dan M. Rooney (who co-founded The Ireland Funds in 1976), recalled that:

Mountbatten's murder shocked many Irish-Americans, my parents included, because they remembered him for the role he played in defeating the Axis.
"It was quite sad because being in America, you were familiar with Lord Mountbatten because of World War II," my mother recalled.
The British people give thanks for his life and grieve at his passing.
George Colley, the Tánaiste (Deputy head of the Government of Ireland), said:

No effort will be spared to bring those responsible to justice.
Assuming that police investigations substantiate the claim, I know that the Irish people will join me in condemning this heartless and terrible outrage.
The IRA issued a statement afterward, saying:

The IRA claim responsibility for the execution of Lord Louis Mountbatten.
The death of Mountbatten and the tributes paid to him will be seen in sharp contrast to the apathy of the British Government and the English people to the deaths of over three hundred British soldiers, and the deaths of Irish men, women, and children at the hands of their forces.
Six weeks later, Sinn Féin vice-president Gerry Adams said of Mountbatten's death:

The IRA gave clear reasons for the execution.
I think it is unfortunate that anyone has to be killed, but the furor created by Mountbatten's death showed up the hypocritical attitude of the media establishment.
As a member of the House of Lords, Mountbatten was an emotional figure in both British and Irish politics.
What the IRA did to him is what Mountbatten had been doing all his life to other people; and with his war record I don't think he could have objected to dying in what was clearly a war situation.
It was in recognition of our affection for him, respect for his impartiality and regard for his concern for India's freedom that the entire nation readily accepted Lord Mountbatten as the first Governor General of Independent India.
In India, a week of national mourning was declared following Mountbatten's death.
Burma announced a three-day period of mourning.
Funeral

On 5 September 1979, Mountbatten received a ceremonial funeral at Westminster Abbey, attended by Queen Elizabeth II, the royal family, and members of the European royal houses.
Watched by thousands of people, the funeral procession, which began at Wellington Barracks, included representatives of all three British Armed Services and military contingents from Burma, India, the United States (represented by 70 sailors of the US Navy and 50 US Marines), France (represented by the French Navy), and Canada.
Mountbatten's funeral was the first major royal funeral to be held in the Abbey since the 18th century.
In his address, the Archbishop of Canterbury, Donald Coggan, highlighted Mountbatten's various achievements and his "lifelong devotion to the Royal Navy".
On hearing of Mountbatten's death, the then Master of the Queen's Music, Malcolm Williamson, composed the Lament in Memory of Lord Mountbatten of Burma for violin and string orchestra.
The Mountbatten Brailler was developed after a bequest in his will was left for the creation of a modern, low cost, portable brailler.
Legacy

Mountbatten's faults, according to his biographer Philip Ziegler, like everything else about him, "were on the grandest scale.
His vanity though child-like, was monstrous, his ambition unbridled ...
However, Ziegler concludes that Mountbatten's virtues outweighed his defects:


He was generous and loyal ...
He was warm-hearted, predisposed to like everyone he met, quick-tempered but never bearing grudges ...
His tolerance was extraordinary; his readiness to respect and listen to the views of others was remarkable throughout his life.
Mountbatten supported the burgeoning nationalist movements that grew up in the shadow of Japanese occupation.
Ziegler writes that in Malaya, where the main resistance to the Japanese came from Chinese groups under considerable communist influence, "Mountbatten proved to have been naïve in his assessment. ...
Mountbatten took pride in enhancing intercultural understanding, and in 1984, with his elder daughter as patron, the Mountbatten Institute was established to give young adults opportunities to develop intercultural appreciation and experience by spending time abroad.
The IET annually awards the Mountbatten Medal for an outstanding contribution, or contributions over a period, to the promotion of electronics or information technology and their application.
Canada's capital city of Ottawa named Mountbatten Avenue in his memory.
Java Street in Kuala Lumpur, Malaysia was renamed Jalan Mountbatten after the Second World War; it was renamed again to Jalan Tun Perak in 1981.
The Mountbatten estate and Mountbatten MRT station in Singapore were also named after him.
The Lord Louis Mountbatten Memorial Loyal Orange Lodge 781 was created in his memory in 1980.
Mountbatten's personal papers, comprising approximately 250,000 documents and 50,000 photographs, are preserved in the University of Southampton Library.
Awards and decorations

letters


He was appointed personal aide-de-camp by Edward VIII, George VI and Elizabeth II and wore each of their royal cyphers on his epaulettes.



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
  AssignClass (e7d28912-6f29-4ffc-8ab2-db9f08a243e3)
 Call ID: e7d28912-6f29-4ffc-8ab2-db9f08a243e3
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (b65ad428-1c65-400d-8b85-d8bf11d025bd)
 Call ID: b65ad428-1c65-400d-8b85-d8bf11d025bd
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddLiteral (6e9bf0de-fd15-4dc4-b7a0-c2d5be042c17)
 Call ID: 6e9bf0de-fd15-4dc4-b7a0-c2d5be042c17
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Louis_Mountbatten
    literal_value: 1900
  AddLiteral (2d401973-e510-4c36-91f0-0d7610fa5e04)
 Call ID: 2d401973-e510-4c36-91f0-0d7610fa5e04
  Args:
    literal_type: xsd:integer
    source: Louis_Mountbatten
    literal_value: 1979
    relation: :hasDeathYear
  AssignClass (aaa21a46-30a9-4b73-93d3-e5eb50c6a3b3)
 Call ID: aaa21a46-30a9-4b73-93d3-e5eb50c6a3b3
  Args:
    type: :Man
    source: Prince_Louis_of_Battenberg
  AssignClass (49a4817d-17b6-4cef-afc1-eaa2719dabad)
 Call ID: 49a4817d-17b6-4cef-afc1-eaa2719dabad
  Args:
    source: Princess_Victoria_of_Hesse_and_by_Rhine
    type: :Woman
  AddTriple (e054edf2-3fdf-4f6d-b0e2-fd1d38f4d8a7)
 Call ID: e054edf2-3fdf-4f6d-b0e2-fd1d38f4d8a7
  Args:
    target: Prince_Louis_of_Battenberg
    relation: :hasFather
    source: Louis_Mountbatten
  AddTriple (cd70adca-4350-460f-b579-4a1c9bb455cc)
 Call ID: cd70adca-4350-460f-b579-4a1c9bb455cc
  Args:
    source: Louis_Mountbatten
    target: Princess_Victoria_of_Hesse_and_by_Rhine
    relation: :hasMother
  AssignClass (ef0010ab-72a0-40cb-adbb-7371d179425b)
 Call ID: ef0010ab-72a0-40cb-adbb-7371d179425b
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AssignClass (dca5676b-cc54-42fe-911f-625405210268)
 Call ID: dca5676b-cc54-42fe-911f-625405210268
  Args:
    type: :Woman
    source: Princess_Louise_of_Battenberg
  AssignClass (c678c46e-daac-4376-88dd-35a1224eb94d)
 Call ID: c678c46e-daac-4376-88dd-35a1224eb94d
  Args:
    type: :Man
    source: George_Mountbatten
  AddTriple (07f372fb-5ade-4d34-ac9c-c5b9d8bc6562)
 Call ID: 07f372fb-5ade-4d34-ac9c-c5b9d8bc6562
  Args:
    relation: :hasSister
    target: Princess_Alice_of_Battenberg
    source: Louis_Mountbatten
  AddTriple (fe61264d-9c07-4e3c-8107-b2dabdff98a1)
 Call ID: fe61264d-9c07-4e3c-8107-b2dabdff98a1
  Args:
    target: Princess_Louise_of_Battenberg
    relation: :hasSister
    source: Louis_Mountbatten
  AddTriple (7c6d15f0-fef5-447e-8815-a3a96b3a1b3e)
 Call ID: 7c6d15f0-fef5-447e-8815-a3a96b3a1b3e
  Args:
    source: Louis_Mountbatten
    relation: :hasBrother
    target: George_Mountbatten
  AssignClass (983c3d50-a1cf-48b3-8b26-64affe7b6de1)
 Call ID: 983c3d50-a1cf-48b3-8b26-64affe7b6de1
  Args:
    type: :Woman
    source: Edwina_Ashley
  AddTriple (9299ae91-7e9a-486d-b611-6412452be9e0)
 Call ID: 9299ae91-7e9a-486d-b611-6412452be9e0
  Args:
    relation: :hasRelation
    target: Edwina_Ashley
    source: Louis_Mountbatten
  AddLiteral (cb5118a4-fd98-441c-8453-f5228f6cf5cc)
 Call ID: cb5118a4-fd98-441c-8453-f5228f6cf5cc
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Louis_Mountbatten
    literal_value: 1922
  AssignClass (1f7b327a-ce86-4094-9009-1f3c6b250c96)
 Call ID: 1f7b327a-ce86-4094-9009-1f3c6b250c96
  Args:
    source: Patricia_Knatchbull
    type: :Woman
  AssignClass (4342c0ce-325b-44e8-a270-ee0dd9676621)
 Call ID: 4342c0ce-325b-44e8-a270-ee0dd9676621
  Args:
    type: :Woman
    source: Lady_Pamela_Hicks
  AddTriple (f6fab60e-1b23-4ddb-9199-73dd7c0977b4)
 Call ID: f6fab60e-1b23-4ddb-9199-73dd7c0977b4
  Args:
    relation: :hasDaughter
    target: Patricia_Knatchbull
    source: Louis_Mountbatten
  AddTriple (aa4173a5-18fe-4cf7-84b9-3a28ba7535aa)
 Call ID: aa4173a5-18fe-4cf7-84b9-3a28ba7535aa
  Args:
    target: Lady_Pamela_Hicks
    relation: :hasDaughter
    source: Louis_Mountbatten
  AssignClass (c1f82701-5985-4d69-b3c2-13b46650f059)
 Call ID: c1f82701-5985-4d69-b3c2-13b46650f059
  Args:
    type: :Man
    source: Louis_IV_Grand_Duke_of_Hesse
  AssignClass (dde5feef-85d4-4a38-b704-f03bd42dc6e6)
 Call ID: dde5feef-85d4-4a38-b704-f03bd42dc6e6
  Args:
    source: Princess_Alice_of_the_United_Kingdom
    type: :Woman
  AddTriple (d5000170-526b-43c6-907b-381af85f6a0a)
 Call ID: d5000170-526b-43c6-907b-381af85f6a0a
  Args:
    source: Princess_Victoria_of_Hesse_and_by_Rhine
    relation: :hasFather
    target: Louis_IV_Grand_Duke_of_Hesse
  AddTriple (cc0b0741-ec4b-4904-8329-a4329d147c06)
 Call ID: cc0b0741-ec4b-4904-8329-a4329d147c06
  Args:
    source: Princess_Victoria_of_Hesse_and_by_Rhine
    target: Princess_Alice_of_the_United_Kingdom
    relation: :hasMother
  AssignClass (181d4eba-6b5b-478c-9843-d39cb4ab845c)
 Call ID: 181d4eba-6b5b-478c-9843-d39cb4ab845c
  Args:
    type: :Man
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (be139b3c-7a67-4744-97a4-b31f8489614e)
 Call ID: be139b3c-7a67-4744-97a4-b31f8489614e
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Woman
  AddTriple (f7bd2a1e-06b1-4f47-9852-a8d0e96cda08)
 Call ID: f7bd2a1e-06b1-4f47-9852-a8d0e96cda08
  Args:
    source: Prince_Louis_of_Battenberg
    target: Prince_Alexander_of_Hesse_and_by_Rhine
    relation: :hasFather
  AddTriple (9d5eb372-9f19-4950-aa9d-3937bdc0b92b)
 Call ID: 9d5eb372-9f19-4950-aa9d-3937bdc0b92b
  Args:
    source: Prince_Louis_of_Battenberg
    target: Julia_Princess_of_Battenberg
    relation: :hasMother
  Finish (7c2a8d3d-ef77-4962-920c-265042f0b56f)
 Call ID: 7c2a8d3d-ef77-4962-920c-265042f0b56f
  Args: