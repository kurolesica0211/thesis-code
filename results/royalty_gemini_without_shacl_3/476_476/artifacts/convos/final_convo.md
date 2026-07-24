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
Prince Philip, Duke of Edinburgh (born Prince Philip of Greece and Denmark,
later Philip Mountbatten; 10 June 1921 – 9 April 2021), was the husband of Queen Elizabeth II and served as consort of the British monarch from her accession on 6 February 1952 until his death in 2021, making him the longest-serving royal consort in British history.
Philip was born in Greece into the Greek and Danish royal families.
In July 1939, he began corresponding with Princess Elizabeth, then aged 13, the elder daughter and heir presumptive of King George VI.
During the Second World War, Philip served with distinction in the Mediterranean and Pacific fleets of the Royal Navy.
In the summer of 1946, King George VI granted Philip permission to marry Elizabeth, who was then 20.
Prior to the official announcement of their engagement in July 1947, Philip renounced his Greek and Danish royal titles and styles, became a naturalised British subject, and adopted the surname Mountbatten from his maternal grandparents.
In November 1947, he married Elizabeth, was granted the style "His Royal Highness", and was created Duke of Edinburgh, Earl of Merioneth, and Baron Greenwich.
Following Elizabeth’s accession to the throne in 1952, Philip left active naval service, having attained the rank of commander.
In 1957, he was formally created a British prince.
A keen sportsman, Philip played a significant role in the development of the equestrian discipline of carriage driving.
He served as patron, president, or member of more than 780 organisations, including the World Wide Fund for Nature, and was chairman of The Duke of Edinburgh's Award, an international youth awards programme for people aged 14 to 24.
Philip was the longest-lived male member of the British royal family.
Early life and education

Family, infancy and exile from Greece

Philip (Greek: Φίλιππος, romanised: Phílippos) was born on 10 June 1921 on the dining room table at Mon Repos, a villa on the Greek island of Corfu.
He was the only son and the fifth and final child of Prince Andrew of Greece and Denmark and his wife, Princess Alice of Battenberg.
Philip's father was the fourth son of King George I and Queen Olga of Greece, and his mother was the eldest child of Louis Mountbatten, 1st Marquess of Milford Haven, and Victoria Mountbatten, Marchioness of Milford Haven (formerly Prince Louis of Battenberg and Princess Victoria of Hesse and by Rhine).
A member of the House of Glücksburg, Philip was a prince of both Greece and Denmark by virtue of his patrilineal descent from George I of Greece and George's father, Christian IX of Denmark; he was from birth in the line of succession to both thrones.
Philip's four elder sisters were Margarita, Theodora, Cecilie, and Sophie.
He was baptised in the Greek Orthodox rite at St. George's Church in the Old Fortress in Corfu.
His godparents were his paternal grandmother, Queen Olga of Greece; his cousin George, Crown Prince of Greece; his uncle Lord Louis Mountbatten; and the municipality of Corfu, represented by its mayor, Alexandros Kokotos, and by the president of the council, Stylianos Maniarizis.
Shortly after Philip's birth, his maternal grandfather died in London.
The Marquess of Milford Haven was a naturalised British subject who, after a career in the Royal Navy, had renounced his German titles and adopted the surname Mountbatten – an Anglicised form of Battenberg – during the First World War owing to anti-German sentiment in the United Kingdom.
After attending his grandfather's memorial service in London, Philip and his mother returned to Greece, where Andrew had remained to command a Greek Army division in the Greco-Turkish War.
Greece suffered significant losses in the conflict, while the Turkish forces made substantial gains.
Philip's uncle, King Constantine I, who was high commander of the Greek expeditionary force, was blamed for the defeat and forced to abdicate in September 1922.
The new military government arrested Andrew and several others.
Andrew's life was also believed to be in danger, and Alice was placed under surveillance.
In December, a revolutionary court banished Andrew from Greece for life.
The British naval vessel HMS Calypso evacuated Andrew's family, with the infant Philip carried to safety in a fruit box.
Upbringing in France, Britain and Germany

Philip's family settled in a house in the Paris suburb of Saint-Cloud lent to them by his wealthy aunt Princess George of Greece and Denmark.
In 1930, Philip was sent to Britain to live with his maternal grandmother at Kensington Palace and with his uncle George Mountbatten, 2nd Marquess of Milford Haven, at Lynden Manor in Bray, Berkshire.
Over the next three years, his four sisters married German princes and moved to Germany, his mother was diagnosed with schizophrenia and placed in an asylum, and his father settled in Monte Carlo.
Philip had little contact with his mother for the remainder of his childhood.
In 1933, Philip was sent to Schule Schloss Salem in Germany, which had the "advantage of saving school fees", because it was owned by the family of his brother-in-law Berthold, Margrave of Baden.
With the rise of Nazism, Salem's Jewish founder, Kurt Hahn, fled persecution and established Gordonstoun School in Scotland, to which Philip transferred after two terms at Salem.
In 1937, his sister Cecilie; her husband, Georg Donatus, Hereditary Grand Duke of Hesse; their two sons; and Georg Donatus's mother were killed in an air crash at Ostend.
Philip, then 16, attended the funeral in Darmstadt.
The following year, Philip's uncle and guardian Lord Milford Haven died of bone marrow cancer.
Milford Haven's younger brother, Lord Louis, assumed parental responsibility for Philip for the remainder of his youth.
Philip did not speak Greek because he had left Greece as an infant.
Known for his charm in his youth, Philip was linked to several women, including Osla Benning.
Naval and wartime service

After leaving Gordonstoun in early 1939, Philip completed a term as a cadet at the Royal Naval College, Dartmouth, then repatriated to Greece, living with his mother in Athens for a month in mid-1939.
At the behest of King George II of Greece, his first cousin, he returned to Britain in September to resume training for the Royal Navy.
During the Second World War, he continued to serve in the British forces, while two of his brothers-in-law, Prince Christoph of Hesse and Berthold, Margrave of Baden, fought on the opposing German side.
Philip was appointed as a midshipman in January 1940.
After the invasion of Greece by Italy in October 1940, he was transferred from the Indian Ocean to the battleship HMS Valiant in the Mediterranean Fleet.
Philip was commissioned as a sub-lieutenant on 1 February 1941 after a series of courses at Portsmouth, in which he gained the top grade in four out of five sections of the qualifying examination.
That October Philip, aged 21, became first lieutenant of HMS Wallace, one of the youngest first lieutenants in the Royal Navy.
The ship was attacked at night by German aircraft, which were expected to return to finish off the damaged vessel; it was saved by Philip's devising a plan to launch a raft with smoke floats that successfully decoyed the bombers, allowing the ship to slip away unnoticed.
Philip returned to the United Kingdom on Whelp in January 1946 and was posted as an instructor at HMS Royal Arthur, the Petty Officers' School in Corsham, Wiltshire.
Marriage

In 1939, the British King George VI and Queen Elizabeth toured the Royal Naval College, Dartmouth.
During the visit, the Queen and Lord Louis Mountbatten asked his nephew Philip to escort the royal couple's daughters, 13-year-old Princess Elizabeth and 9-year-old Princess Margaret, who were Philip's third cousins through Queen Victoria of the United Kingdom and second cousins once removed through King Christian IX of Denmark.
Philip and Elizabeth had first met as children in 1934 at the wedding of Elizabeth's uncle Prince George, Duke of Kent, to Philip's first cousin Princess Marina of Greece and Denmark.
After their 1939 meeting, Elizabeth fell in love with Philip, and they began to exchange letters.
In the summer of 1946, Philip asked George VI for his daughter's hand in marriage.
The King granted his request, provided that any formal engagement be delayed until Elizabeth's 21st birthday the following April.
By March 1947, Philip had adopted the surname Mountbatten from his mother's family and had stopped using his Greek and Danish royal titles upon becoming a naturalised British subject.
The engagement attracted some controversy; Philip had no financial standing, was foreign-born, and had sisters who had married German noblemen with Nazi links.
He was a prince without a home or kingdom.
Some of the papers played long and loud tunes on the string of Philip's foreign origin."
Later biographies reported that Elizabeth's mother had reservations about the union initially and teased Philip as "the Hun".
In later life, however, she told the biographer Tim Heald that Philip was "an English gentleman".
Although Philip appeared "always to have regarded himself as an Anglican", and he had attended Anglican services with his classmates and relations in England and throughout his Royal Navy career, he had been baptised in the Greek Orthodox Church.
The archbishop of Canterbury, Geoffrey Fisher, wanted to "regularise" Philip's position by officially receiving him into the Church of England, which he did in October 1947.
The day before the wedding, the King bestowed the style of "Royal Highness" on Philip, and on the morning of the wedding, 20 November 1947, he was created Duke of Edinburgh, Earl of Merioneth, and Baron Greenwich of Greenwich in the County of London.
Consequently, being already a Knight of the Garter, between 19 and 20 November 1947 he bore the unusual style Lieutenant His Royal Highness Sir Philip Mountbatten, and is so described in the letters patent of 20 November 1947.
Concerned by her father's poor health, Elizabeth insisted that Philip give up smoking, which he did on their wedding day.
Philip and Elizabeth were married in a ceremony at Westminster Abbey, recorded and broadcast by BBC radio to 200 million people around the world.
In post-war Britain, it was unacceptable for any of Philip's German relations, including his three surviving sisters, to be invited to the wedding.
After their marriage, Philip and Elizabeth took up residence at Clarence House.
Their first two children were born before Elizabeth's accession in 1952:
Prince Charles in November 1948 and Princess Anne in August 1950.
Philip was introduced to the House of Lords on 21 July 1948, immediately before his uncle Louis Mountbatten, who had been created Earl Mountbatten of Burma.
Philip is not recorded as having spoken in the House.
He, his sons, and other hereditary peers in the royal family ceased to be members following the House of Lords Act 1999, although all peers whose titles were of the first creation were offered life peerages.
The only member of the royal family to accept was Philip's former brother-in-law, Antony Armstrong-Jones, 1st Earl of Snowdon, who therefore remained in the Lords.
Early duties

After their honeymoon at the Mountbatten family home, Broadlands, Philip returned to the navy, at first in a desk job at the Admiralty and later on a staff course at the Naval Staff College, Greenwich.
Philip was promoted to commander on 30 June 1952, although his active naval career had ended in July 1951.
With the King in ill health, Elizabeth and Philip were both appointed to the Privy Council on 4 November 1951, after a coast-to-coast tour of Canada.
They were in Kenya when Elizabeth's father died on 6 February 1952, and she became queen.
Philip broke the news to Elizabeth at Sagana Lodge, and the royal party immediately returned to the United Kingdom.
In December 1952, Philip was initiated into Freemasonry by the Worshipful Master of Navy Lodge
No 2612, honouring a commitment he had made to George VI, who had made it clear that he expected Philip to maintain the tradition of royal patronage of Freemasonry.
However, according to one journalist writing in 1983, Philip's mother-in-law and his uncle Lord Mountbatten held unfavourable views of Freemasonry; after his initiation, Philip took no further part in the organisation.
Although, as the consort of the Queen, he might in time have been made Grand Master of British Freemasonry, Elizabeth's cousin Prince Edward, Duke of Kent, assumed that role in 1967.
Philip's son Charles apparently never joined Freemasonry.
Consort of the Queen

Royal house

Elizabeth's accession to the throne raised the question of the name of the royal house, as she would typically have taken Philip's surname upon marriage.
Lord Mountbatten advocated the name "House of Mountbatten", while Philip suggested "House of Edinburgh" after his ducal title.
When Elizabeth's grandmother Queen Mary heard of this, she informed Winston Churchill, who later advised Elizabeth to issue a royal proclamation declaring that the royal house was to remain known as the House of Windsor.
Philip privately complained, "I am nothing but a bloody amoeba.
"


In February 1960, the Queen issued an Order in Council declaring that Mountbatten-Windsor would be the surname of the couple's male-line descendants who are not styled as "Royal Highness" or titled as prince or princess.
Although Elizabeth had "absolutely set her heart" on such a change and had considered it for some time, it occurred only 11 days before the birth of their third child, Prince Andrew, and only after three months of protracted correspondence between English constitutional expert Edward Iwi – who argued that, without such a change, the royal child would be born with "the Badge of Bastardy" – and Harold Macmillan, who had attempted to refute Iwi's arguments.
Philip and Elizabeth's fourth child, Prince Edward, was born in March 1964.
Six months after she acceded to the throne, Elizabeth announced that Philip was to have "place, pre-eminence and precedence" next to her "on all occasions and in all meetings, except where otherwise provided by Act of Parliament".
She also intervened to ensure that Philip would serve as regent for their son Charles in the event of her unexpected death.
Contrary to rumours over the years, Elizabeth and Philip were said by insiders to have had a strong relationship throughout their marriage, despite the challenges of Elizabeth's reign.
Elizabeth referred to Philip in a speech on the occasion of her Diamond Jubilee in 2012 as her "constant strength and guide".
Philip received a Parliamentary annuity (of £359,000 from 1990) to meet official expenses in carrying out public duties.
The annuity was unaffected by the reform of royal finances under the Sovereign Grant Act 2011.
Supporting the Queen

As consort, Philip supported his wife in her duties as sovereign, accompanying her to ceremonies such as the State Opening of Parliament in various countries, state dinners, and tours abroad.
As chairman of the Coronation Commission, he became the first member of the royal family to fly in a helicopter, visiting the troops that were to take part in the ceremony.
Philip was not himself crowned in the coronation service, but knelt before Elizabeth, with her hands enclosing his, and swore to be her "liege man of life and limb".
In the early 1950s, Philip's sister-in-law, Margaret, considered marrying a divorced older man, Peter Townsend.
The press accused Philip of being hostile to the match, to which he replied: "I haven't done anything."
In 1960, Margaret married Antony Armstrong-Jones, who was created Earl of Snowdon the following year.
In 1956, Philip and Kurt Hahn founded The Duke of Edinburgh's Award to give young people "a sense of responsibility to themselves and their communities".
From 1956 to 1957, he travelled around the world aboard the newly commissioned HMY Britannia, during which he opened the 1956 Summer Olympics in Melbourne and visited the Antarctic, becoming the first royal to cross the Antarctic Circle.
Elizabeth and the children remained in Britain.
On the return leg of the journey, Philip's private secretary, Mike Parker, was sued for divorce by his wife.
He later said that Philip had been very supportive and "the Queen was wonderful throughout.
In a public show of support, Elizabeth created Parker a Commander of the Royal Victorian Order.
Further press reports claimed that the royal couple were drifting apart, which enraged Philip and dismayed Elizabeth, who issued a strongly worded denial.
She granted him the style and title of a Prince of the United Kingdom by Letters Patent on 22 February 1957; it was gazetted that Philip was to be known as "His Royal Highness The Prince Philip, Duke of Edinburgh".
Philip was appointed to the Queen's Privy Council for Canada on 14 October 1957, taking his Oath of Allegiance before the Queen in person at her Canadian residence, Rideau Hall.
This was at first considered "tactless", but Philip was later admired for his encouragement of physical fitness.
In 1960, Philip attended the National Eisteddfod of Wales wearing a long green robe, where he was initiated as an Honorary Ovate by the Archdruid of Wales, Edgar Phillips, through his bardic name Philip Meirionnydd, reflecting his title of Earl of Merioneth.
In 1961, he became the first member of the royal family to be interviewed on television, appearing on Panorama to answer questions by Richard Dimbleby about the Commonwealth Technical Training Week, an initiative of which he was patron.
When, in 1965, the prime minister of Southern Rhodesia, Ian Smith, enacted his illegal Unilateral Declaration of Independence from the United Kingdom, the British diplomat Michael Palliser suggested to Foreign Office Minister George Thomson that Elizabeth appoint Philip as governor-general of Rhodesia and have him arrive with a detachment of Coldstream Guards to dismiss Smith and the Rhodesian Front government.
Palliser and Thomson decided the plan was not feasible, both because it would draw the royal family into politics and because of the risk to Philip's safety.
In October 1994, Philip became the first member of the British royal family to visit Israel.
He travelled to Jerusalem to attend a ceremony at Yad Vashem honouring his mother, Princess Alice of Battenberg, who had been recognised as one of the Righteous Among the Nations for sheltering members of a Jewish family during the Nazi occupation of Greece.
Charities and patronages

Philip was patron of some 800 organisations, particularly focused on the environment, industry, sport, and education.
His first solo engagement as Duke of Edinburgh was in March 1948, presenting prizes at the boxing finals of the London Federation of Boys' Clubs at the Royal Albert Hall.
He was president of the National Playing Fields Association (now known as Fields in Trust) for 64 years, from 1947 until his grandson Prince William took over the role in 2013.
He was appointed a fellow of the Royal Society in 1951.
In the same year, following his father-in-law's death, he took over the role of the Ranger of Windsor Great Park, overseeing its protection and maintenance.
From 1955 to 1957, Philip was president of The Football Association and also served two terms as president of the Marylebone Cricket Club, with his tenures beginning in 1949 and 1974, respectively.
Between 1959 and 1965, Philip was president of BAFTA.
He served as chancellor of the universities of Cambridge, Edinburgh, Salford, and Wales.
In 1965, at the suggestion of Harold Wilson, Philip became chair of a scheme established to recognise industrial innovation, which later became known as The Queen's Awards for Enterprise.
In the same year, he became president of the Council of Engineering Institutions and, in that capacity, assisted with the inception of the Fellowship of Engineering (later the Royal Academy of Engineering), of which he later became the senior fellow.
He also commissioned the Prince Philip Designers Prize and the Prince Philip Medal to recognise designers and engineers who made exceptional contributions.
In 2017, the British Heart Foundation thanked Philip for being its patron for 55 years, during which time, in addition to organising fundraisers, he "supported the creation of nine BHF-funded centres of excellence".
Charles and Diana

At the beginning of 1981, Philip wrote to his son Charles counselling him to make up his mind to either propose to Lady Diana Spencer or to end their courtship.
Charles felt pressured by his father to make a decision and did so, proposing to Diana in February.
Philip and Elizabeth hosted a meeting between Charles and Diana in an attempt to effect a reconciliation, but without success.
Philip wrote to Diana, expressing his disappointment at both Charles's and her extra-marital affairs and asking her to examine their behaviour from each other's point of view.
Charles and Diana separated in 1992 and divorced in 1996.
A year after the divorce, Diana was killed in a car crash in Paris on 31 August 1997.
At the time, Philip was on holiday at Balmoral with the extended royal family.
In their grief, Diana's sons, Princes William and Harry, wished to attend church, so Philip and Elizabeth took them that morning.
For five days, the royal couple shielded their grandsons from the intense press interest by keeping them at Balmoral, where they could grieve in private.
The royal family's seclusion caused public dismay, but the mood shifted after a live broadcast made by Elizabeth on 5 September.
Unsure whether they should walk behind their mother's coffin during the funeral procession, William and Harry hesitated.
Philip told William, "If you don't walk, I think you'll regret it later.
On the day of the funeral, Philip, William, Harry, Charles, and Diana's brother, Earl Spencer, walked through London behind her gun carriage.
Over the next few years, Mohamed Al-Fayed, whose son Dodi Fayed was also killed in the crash, claimed that Philip had ordered Diana's death and that the accident was staged.
The inquest into Diana's death concluded in 2008 that there was no evidence of a conspiracy.
Longevity

In April 2009, Philip became the longest-serving British royal consort, surpassing Queen Charlotte.
He became the oldest-ever male British royal in February 2013, and in April 2019 he became the third-longest-lived member of the British royal family, after Princess Alice, Duchess of Gloucester, and Queen Elizabeth the Queen Mother.
Personally, he was not enthused about living an extremely long life; in a 2000 interview, when he was 79, he said he could not "imagine anything worse" and had "no desire whatsoever" to become a centenarian, remarking that "bits of me are falling off already".
In 2008, Philip was admitted to King Edward VII's Hospital, London, for a chest infection.
After the Evening Standard reported that Philip had prostate cancer, Buckingham Palace – which usually refused to comment on health rumours – denied the story, and the paper retracted it.
In June 2011, in an interview marking his 90th birthday, Philip said that he would now slow down and reduce his duties, stating that he had "done  bit".
The Queen appointed him Lord High Admiral for his 90th birthday.
While staying at Sandringham House in December 2011, Philip suffered chest pains and was taken to the cardio-thoracic unit at Papworth Hospital, Cambridgeshire, where he underwent successful coronary angioplasty and stenting.
In June 2012, during the celebrations making his wife's diamond jubilee, Philip was taken from Windsor Castle to King Edward VII's Hospital suffering from a bladder infection.
After a recurrence of infection in August 2012, while staying at Balmoral Castle, he was admitted to Aberdeen Royal Infirmary for five nights as a precaution.
In June 2013, Philip was admitted to the London Clinic for an exploratory operation on his abdomen, spending 11 days in hospital.
In May 2014, he appeared in public with a bandage on his right hand after a "minor procedure" at Buckingham Palace the previous day.
In June 2017, Philip was taken from Windsor to London and admitted to King Edward VII's Hospital after being diagnosed with an infection.
He spent two nights in hospital and was unable to attend the State Opening of Parliament, and Royal Ascot.
Final years and retirement

Philip retired from royal duties on 2 August 2017, meeting Royal Marines in his final solo public engagement at the age of 96.
On 20 November 2017, he celebrated his 70th wedding anniversary with Elizabeth, making her the first British monarch to mark a platinum wedding anniversary.
In April 2018, Philip was admitted to King Edward VII's Hospital for a planned hip replacement, having missed the annual Maundy and Easter Sunday services.
His daughter Anne visited him for about 50 minutes afterwards and said her father was "on good form".
In May that year, he attended the wedding of his grandson Harry and Meghan Markle and was able to walk with Elizabeth unaided.
In October, he accompanied Elizabeth to the wedding of their granddaughter Princess Eugenie of York and Jack Brooksbank, with The Telegraph reporting that Philip decided whether to attend events on a "wake up and see how I feel" basis.
In January 2019, Philip was involved in a car collision as he drove onto a main road near the Sandringham Estate.
Philip attended hospital the next morning as a precaution.
He was still permitted to drive on private estates, and was seen behind the wheel in the grounds of Windsor Castle in April 2019.
In December 2019, Philip stayed at King Edward VII's Hospital and received treatment for a "pre-existing condition" in what Buckingham Palace described as a "precautionary measure".
He had not been seen in public since attending Lady Gabriella Windsor's wedding in May 2019.
A photograph of Philip and Elizabeth while they isolated at Windsor Castle during the COVID-19 pandemic was released ahead of his 99th birthday in June 2020.
In January 2021, Philip and Elizabeth were vaccinated against COVID-19 by a household doctor at Windsor Castle.
In February 2021, Philip was admitted to King Edward VII's Hospital as a "precautionary measure" after feeling unwell; he was visited by his son Charles.
Buckingham Palace confirmed that Philip was "responding to treatment" for an infection.
In March, Philip was transferred by ambulance to St Bartholomew's Hospital to continue treatment for the infection and to undergo "testing and observation" relating to a pre-existing heart condition.
He underwent a successful procedure for the heart condition and was transferred back to King Edward VII's Hospital.
He was discharged a week later and returned to Windsor Castle.
Death

Philip died of "old age" on the morning of 9 April 2021 at Windsor Castle, aged 99.
He was the longest-serving royal consort in world history.
Elizabeth was reported, through her son Andrew, to have said that Philip's death had "left a huge void in her life".
The palace said that Philip died peacefully, a description confirmed by his daughter‐in‐law Sophie, Countess of Wessex, who told the press it was "so gentle.
It was just like somebody took him by the hand and off he went."
The usual public ceremonial could not take place because COVID-19 regulations restricted the number of mourners to 30; it was later reported that Elizabeth had rejected a government offer to relax the rules.
The funeral took place on 17 April 2021 at St George's Chapel, Windsor Castle, and Philip was temporarily interred alongside 25 other coffins, including that of George III, in the Royal Vault inside St George's.
Representatives of countries around the world sent condolences to the royal family upon his death.
As with other senior members of the royal family, Philip's last will and testament will be sealed for at least 90 years, according to a High Court ruling that deemed it necessary to protect the Sovereign's "dignity and standing".
This led to speculation that the will might contain material harmful to the reputation of the royal family.
A service of thanksgiving for Philip's life took place on 29 March 2022 at Westminster Abbey, attended by Elizabeth, foreign royalty, and politicians.
Elizabeth died on 8 September 2022, and the royal couple's bodies were interred in the King George VI Memorial Chapel at St George's on the evening of 19 September after her state funeral.
Legacy

Interests

Philip played polo until 1971, when he began competing in carriage driving, a sport he helped to expand; its early rule book was drafted under his supervision.
Philip's first airborne flying lesson took place in 1952, and by his 70th birthday he had accrued 5,150 pilot hours.
He was presented with Royal Air Force wings in 1953, helicopter wings with the Royal Navy in 1956, and his private pilot's licence in 1959.
In April 2014, it was reported that a British Pathé newsreel had been discovered showing Philip's two‐month flying tour of South America in 1962.
Sitting alongside him at the aircraft's controls was his co-pilot, Captain Peter Middleton, the grandfather of Philip's granddaughter-in-law Catherine.
In 1959, Philip flew solo in a Druine Turbulent, becoming the first and, as of April 2021, the only member of the royal family to have flown a single‐seat aircraft.
Philip painted with oils and collected artworks, including contemporary cartoons, which hang at Buckingham Palace, Windsor Castle, Sandringham House, and Balmoral Castle.
Hugh Casson described Philip's own artwork as "exactly what you'd expect ... totally direct, no hanging about.
He was patron of the Royal Society of Arts from 1952 until 2011.
He was "fascinated" by cartoons about the monarchy and the royal family, and was a patron of The Cartoon Museum.
Personality and image

Philip's down-to-earth manner was attested to by a White House butler, who recalled that, during a visit in 1976, Philip engaged him and a fellow butler in conversation and poured them drinks.
As well as having a reputation for bluntness and plain speaking, Philip was noted for occasionally making observations and jokes that were construed as funny or typical for someone of his age and background by some, but as gaffes, awkward, politically incorrect, or even offensive by others.
Later in life, he suggested that his comments may have contributed to the perception that he was "a cantankerous old sod".
In a private conversation with British students from Xi'an's Northwest University during a state visit to China in 1986, Philip joked: "If you stay here much longer, you'll go slit-eyed."
Philip also made comments on the eating habits of Cantonese people, stating: "If it has four legs and is not a chair, has wings and is not an airplane, or swims and is not a submarine, the Cantonese will eat it."
In Australia, he asked an Indigenous Australian entrepreneur: "Do you still throw spears at each other?"


In 2011, historian David Starkey described Philip as a kind of "HRH Victor Meldrew".
For example, in May 1999, British newspapers accused Philip of insulting deaf children at a pop concert in Wales by saying: "No wonder you are deaf listening to this row."
Philip later wrote: "The story is largely invention.
It so happens that my mother was quite seriously deaf and I have been Patron of the Royal National Institute for the Deaf for ages, so it's hardly likely that I would do any such thing."
When he and Elizabeth met Stephen Menary, an army cadet blinded by a Real IRA bomb, and Elizabeth asked how much sight he retained, Philip quipped: "Not a lot, judging by the tie he's wearing."
Philip's comparison of prostitutes and wives was also perceived as offensive after he reportedly stated: "I don't think a prostitute is more moral than a wife, but they are doing the same thing.
"


Centenary

To mark the centenary of Philip's birth in June 2021, the Royal Collection Trust held an exhibition at Windsor Castle and the Palace of Holyroodhouse.
Titled Prince Philip: A Celebration, it showcased around 150 personal items related to him, including his wedding card, wedding menu, midshipman's logbook from 1940 to 1941, Chair of Estate, and the coronation robes and coronet he wore at his wife's coronation in 1953.
George Alexis Weymouth's portrait of Philip in the ruins of Windsor Castle after the fire of 1992 formed part of a focus on Philip's involvement in the subsequent restoration.
The Royal Horticultural Society also marked Philip's centenary by breeding a new rose in his honour, christened "The Duke of Edinburgh Rose", created by British rose breeder Harkness Roses.
Elizabeth, as patron of the society, was given the deep pink commemorative rose in honour of her husband, and she remarked that "It looks lovely".
A Duke of Edinburgh Rose has since been planted in the mixed rose border of Windsor Castle's East Terrace Garden.
Philip played a major role in the garden's design.
In September 2021, the Royal National Lifeboat Institution honoured Philip by naming a new Shannon-class lifeboat Duke of Edinburgh.
The tribute had initially been planned to mark his 100th birthday.
In the same month, a documentary originally intended for his centenary was broadcast on BBC One under the title Prince Philip: The Royal Family Remembers, with contributions from his children, their spouses, and seven of his grandchildren.
Portrayals

Philip has been portrayed by several actors, including Stewart Granger (The Royal Romance of Charles and Diana, 1982), Christopher Lee (Charles & Diana: A Royal Love Story, 1982), David Threlfall (The Queen's Sister, 2005), James Cromwell (The Queen, 2006), and Finn Elliot, Matt Smith, Tobias Menzies, and Jonathan Pryce (The Crown, 2016 onwards).
He also appears as a fictional character in Nevil Shute's In the Wet (1952), Paul Gallico's Mrs. 'Arris Goes to Moscow (1974), Tom Clancy's Patriot Games (1987), and Sue Townsend's The Queen and I (1992).
Books

Philip authored:
Forewords to:


Titles, styles, honours, and arms

Philip held many titles throughout his life.
Originally a prince of Greece and Denmark, he abandoned these titles before his marriage and was thereafter created a British duke, among other noble titles.
In 1957, Elizabeth formally issued letters patent making him a British prince.
Honours and honorary military appointments

Philip received medals from Britain, France, and Greece for his service during the Second World War, as well as medals commemorating the coronations of George VI and Elizabeth II, and the silver, gold, and diamond jubilees of Elizabeth.
George VI appointed him to the Order of the Garter on the eve of his wedding on 19 November 1947.
Thereafter, Philip received 17 appointments and decorations within Commonwealth and 48 from foreign states.
The inhabitants of several villages on the island of Tanna, Vanuatu, worship Philip as a god-like spiritual figure; they keep portraits of him and hold feasts on his birthday.
Upon his wife's accession to the throne in 1952, Philip was appointed Admiral of the Sea Cadet Corps, Colonel-in-Chief of the British Army Cadet Force, and Air Commodore-in-Chief of the Air Training Corps.
The following year, he was appointed to the equivalent positions in Canada and made Admiral of the Fleet, Captain General Royal Marines, Field Marshal, and Marshal of the Royal Air Force in the United Kingdom.
In 1975, he was appointed colonel of the Grenadier Guards, a position he handed over to his son Andrew in 2017.
To mark Philip's 90th birthday, Elizabeth appointed him Lord High Admiral, as well as to the highest ranks available in all three branches of the Canadian Armed Forces.
On their 70th wedding anniversary, 20 November 2017, she appointed him Knight Grand Cross of the Royal Victorian Order, making him the first British national since his uncle Lord Mountbatten to be entitled to wear the breast stars of four orders of chivalry in the United Kingdom.
Arms

Genealogy

Both Philip and Elizabeth were great-great-grandchildren of Queen Victoria, Elizabeth by descent from Victoria's eldest son, King Edward VII, and Philip by descent from Victoria's second daughter, Princess Alice.
Both were also descended from King Christian IX of Denmark.
Philip was also related to the House of Romanov through all four of his grandparents.
His paternal grandmother, Olga Constantinovna of Russia, was the granddaughter of Emperor Nicholas I of Russia.
His maternal grandmother, Princess Victoria of Hesse and by Rhine, was a sister of Empress Alexandra of Russia.
In 1993 scientists were able to confirm the identity of the remains of several members of the Romanov family, more than seventy years after their murder in 1918, by comparing their mitochondrial DNA to living matrilineal relatives, including Philip.
Philip, Alexandra, and her children were all descended from Princess Alice through a purely female line.



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
  AssignClass (9bdebc44-eebb-4aa1-8c9f-2da7a3ff29fa)
 Call ID: 9bdebc44-eebb-4aa1-8c9f-2da7a3ff29fa
  Args:
    source: Prince_Philip
    type: :Man
  AssignClass (3aeefa0e-b576-4ab4-af7d-31aec49ddd17)
 Call ID: 3aeefa0e-b576-4ab4-af7d-31aec49ddd17
  Args:
    type: :Person
    source: Prince_Philip
  AddLiteral (916f9b6b-109d-41f5-9856-eb50f4ddd841)
 Call ID: 916f9b6b-109d-41f5-9856-eb50f4ddd841
  Args:
    source: Prince_Philip
    literal_value: 1921
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4f7028a7-e674-4dbf-bcde-d6be68e57084)
 Call ID: 4f7028a7-e674-4dbf-bcde-d6be68e57084
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Philip
    literal_value: 2021
  AssignClass (466b1c93-5acd-4128-a007-1c89d3be7959)
 Call ID: 466b1c93-5acd-4128-a007-1c89d3be7959
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (f996d359-1e07-4f81-83f7-eaba4c249f03)
 Call ID: f996d359-1e07-4f81-83f7-eaba4c249f03
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AddLiteral (5bfd461e-0db9-45b1-a46d-6aefdaae3db6)
 Call ID: 5bfd461e-0db9-45b1-a46d-6aefdaae3db6
  Args:
    literal_value: 1947
    source: Prince_Philip
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (c7ec7f85-75d2-430a-8202-730512b9839d)
 Call ID: c7ec7f85-75d2-430a-8202-730512b9839d
  Args:
    source: Prince_Philip
    target: Queen_Elizabeth_II
    relation: :hasRelation
  AssignClass (845506b8-03d0-40ee-8677-627e3dc87400)
 Call ID: 845506b8-03d0-40ee-8677-627e3dc87400
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (18ba1bd7-8e03-47c7-8ce7-6a79beccb4fa)
 Call ID: 18ba1bd7-8e03-47c7-8ce7-6a79beccb4fa
  Args:
    type: :Person
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (13c7e074-17ab-4beb-9490-5efe028be841)
 Call ID: 13c7e074-17ab-4beb-9490-5efe028be841
  Args:
    type: :Woman
    source: Princess_Alice_of_Battenberg
  AssignClass (e9545c8f-5fa7-45ab-bc82-7fcb06a47381)
 Call ID: e9545c8f-5fa7-45ab-bc82-7fcb06a47381
  Args:
    type: :Person
    source: Princess_Alice_of_Battenberg
  AddTriple (08ca6b3a-4752-46a6-a3ff-061dcacb9f64)
 Call ID: 08ca6b3a-4752-46a6-a3ff-061dcacb9f64
  Args:
    source: Prince_Philip
    target: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (82f1d3a4-82d3-4ead-99c5-a8b2948ec6b1)
 Call ID: 82f1d3a4-82d3-4ead-99c5-a8b2948ec6b1
  Args:
    target: Princess_Alice_of_Battenberg
    relation: :hasMother
    source: Prince_Philip
  AssignClass (a41ed0a8-3d14-44bb-bf84-ca39496cb027)
 Call ID: a41ed0a8-3d14-44bb-bf84-ca39496cb027
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (3dc6897f-6940-4f29-9f64-35d584055cc3)
 Call ID: 3dc6897f-6940-4f29-9f64-35d584055cc3
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (c5122d09-afae-4740-a9d2-a0cde8a720ed)
 Call ID: c5122d09-afae-4740-a9d2-a0cde8a720ed
  Args:
    type: :Woman
    source: Queen_Olga_of_Greece
  AssignClass (1ed42eba-cc72-4741-9e40-956a15104829)
 Call ID: 1ed42eba-cc72-4741-9e40-956a15104829
  Args:
    source: Queen_Olga_of_Greece
    type: :Person
  AddTriple (b7c2b42d-e0ea-47cb-be45-74bc96a45ba9)
 Call ID: b7c2b42d-e0ea-47cb-be45-74bc96a45ba9
  Args:
    target: King_George_I_of_Greece
    relation: :hasFather
    source: Prince_Andrew_of_Greece_and_Denmark
  AddTriple (11e1dd15-9662-458f-9b94-fe0b44ea61c8)
 Call ID: 11e1dd15-9662-458f-9b94-fe0b44ea61c8
  Args:
    target: Queen_Olga_of_Greece
    relation: :hasMother
    source: Prince_Andrew_of_Greece_and_Denmark
  AssignClass (ed42d259-9817-4fe5-94fc-7ce1554b27f7)
 Call ID: ed42d259-9817-4fe5-94fc-7ce1554b27f7
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Marquess_of_Milford_Haven
  AssignClass (16e6aa48-ab32-4ca5-bbb2-79589b235707)
 Call ID: 16e6aa48-ab32-4ca5-bbb2-79589b235707
  Args:
    type: :Person
    source: Louis_Mountbatten_1st_Marquess_of_Milford_Haven
  AssignClass (293ba9fd-3e07-4032-a3d9-130282ffbd26)
 Call ID: 293ba9fd-3e07-4032-a3d9-130282ffbd26
  Args:
    source: Victoria_Mountbatten_Marchioness_of_Milford_Haven
    type: :Woman
  AssignClass (77de8886-3024-46cb-bff0-6cc04f1bf04b)
 Call ID: 77de8886-3024-46cb-bff0-6cc04f1bf04b
  Args:
    type: :Person
    source: Victoria_Mountbatten_Marchioness_of_Milford_Haven
  AddTriple (68dadc48-79ef-4371-87b4-9e7585b36506)
 Call ID: 68dadc48-79ef-4371-87b4-9e7585b36506
  Args:
    source: Princess_Alice_of_Battenberg
    relation: :hasFather
    target: Louis_Mountbatten_1st_Marquess_of_Milford_Haven
  AddTriple (a59b596b-9d4c-44ee-97f8-5f944ac02164)
 Call ID: a59b596b-9d4c-44ee-97f8-5f944ac02164
  Args:
    source: Princess_Alice_of_Battenberg
    relation: :hasMother
    target: Victoria_Mountbatten_Marchioness_of_Milford_Haven
  AssignClass (61222eb5-254e-438b-9d0f-5f2d2113284b)
 Call ID: 61222eb5-254e-438b-9d0f-5f2d2113284b
  Args:
    source: Margarita
    type: :Woman
  AssignClass (e642708a-46c8-459a-9bf5-17eaf2f8811c)
 Call ID: e642708a-46c8-459a-9bf5-17eaf2f8811c
  Args:
    type: :Person
    source: Margarita
  AssignClass (516c40d1-728a-42af-a71a-36aa985b7b2a)
 Call ID: 516c40d1-728a-42af-a71a-36aa985b7b2a
  Args:
    type: :Woman
    source: Theodora
  AssignClass (b3f7c3bd-f0ce-4a4b-b0ec-de3d9810cab1)
 Call ID: b3f7c3bd-f0ce-4a4b-b0ec-de3d9810cab1
  Args:
    source: Theodora
    type: :Person
  AssignClass (21f59a7c-1f15-4656-8dfd-893018eb4a96)
 Call ID: 21f59a7c-1f15-4656-8dfd-893018eb4a96
  Args:
    source: Cecilie
    type: :Woman
  AssignClass (5ac8e110-4d57-4eb0-9a3c-449af9a46be4)
 Call ID: 5ac8e110-4d57-4eb0-9a3c-449af9a46be4
  Args:
    source: Cecilie
    type: :Person
  AssignClass (39d20177-8871-4f80-836a-cc7554a4225f)
 Call ID: 39d20177-8871-4f80-836a-cc7554a4225f
  Args:
    source: Sophie
    type: :Woman
  AssignClass (f12d49ca-3d87-4982-b9c8-adb27a47b6e1)
 Call ID: f12d49ca-3d87-4982-b9c8-adb27a47b6e1
  Args:
    type: :Person
    source: Sophie
  AddTriple (c8592a9e-9e44-4569-b472-3acbb48d35c7)
 Call ID: c8592a9e-9e44-4569-b472-3acbb48d35c7
  Args:
    target: Margarita
    relation: :hasChild
    source: Prince_Andrew_of_Greece_and_Denmark
  AddTriple (2d0f6c90-bef5-48cf-adea-437296775b7c)
 Call ID: 2d0f6c90-bef5-48cf-adea-437296775b7c
  Args:
    source: Princess_Alice_of_Battenberg
    relation: :hasChild
    target: Margarita
  AddTriple (7c136f62-fdbe-46c2-a45b-eb0435ab6f17)
 Call ID: 7c136f62-fdbe-46c2-a45b-eb0435ab6f17
  Args:
    relation: :hasChild
    target: Theodora
    source: Prince_Andrew_of_Greece_and_Denmark
  AddTriple (f67fd481-1ce1-468e-bc3f-ef359b5f3f21)
 Call ID: f67fd481-1ce1-468e-bc3f-ef359b5f3f21
  Args:
    target: Theodora
    relation: :hasChild
    source: Princess_Alice_of_Battenberg
  AddTriple (453f7f50-7f2c-43c8-93ce-bc4a1957a83e)
 Call ID: 453f7f50-7f2c-43c8-93ce-bc4a1957a83e
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    target: Cecilie
    relation: :hasChild
  AddTriple (ea9a10ad-f9b4-400b-97aa-221279d55129)
 Call ID: ea9a10ad-f9b4-400b-97aa-221279d55129
  Args:
    source: Princess_Alice_of_Battenberg
    relation: :hasChild
    target: Cecilie
  AddTriple (5bc943ee-0636-48b6-aba0-bab7dab9b509)
 Call ID: 5bc943ee-0636-48b6-aba0-bab7dab9b509
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    relation: :hasChild
    target: Sophie
  AddTriple (e424c92c-2753-419c-a5ca-eaecfe304c9a)
 Call ID: e424c92c-2753-419c-a5ca-eaecfe304c9a
  Args:
    source: Princess_Alice_of_Battenberg
    relation: :hasChild
    target: Sophie
  AssignClass (4073fdcc-b800-4b3e-9202-f01d52b71b81)
 Call ID: 4073fdcc-b800-4b3e-9202-f01d52b71b81
  Args:
    source: Prince_Charles
    type: :Man
  AssignClass (32120c82-8c9a-4b04-bcd9-baac9af0bf40)
 Call ID: 32120c82-8c9a-4b04-bcd9-baac9af0bf40
  Args:
    type: :Person
    source: Prince_Charles
  AssignClass (a5870a98-0e77-4b5c-9898-0a312af84aaa)
 Call ID: a5870a98-0e77-4b5c-9898-0a312af84aaa
  Args:
    source: Princess_Anne
    type: :Woman
  AssignClass (ef533b15-e7c1-4c16-a988-969107ca9343)
 Call ID: ef533b15-e7c1-4c16-a988-969107ca9343
  Args:
    type: :Person
    source: Princess_Anne
  AssignClass (85b7e07f-fa7e-4c60-824e-f368bac67810)
 Call ID: 85b7e07f-fa7e-4c60-824e-f368bac67810
  Args:
    source: Prince_Andrew
    type: :Man
  AssignClass (dcd1b9f3-0a8e-4afc-8f25-896fe386e5b6)
 Call ID: dcd1b9f3-0a8e-4afc-8f25-896fe386e5b6
  Args:
    type: :Person
    source: Prince_Andrew
  AssignClass (7095d3a6-18e9-4e32-b76d-1dffe78407a5)
 Call ID: 7095d3a6-18e9-4e32-b76d-1dffe78407a5
  Args:
    type: :Man
    source: Prince_Edward
  AssignClass (ad82eaa9-3a87-43f7-a860-bd0113af1388)
 Call ID: ad82eaa9-3a87-43f7-a860-bd0113af1388
  Args:
    source: Prince_Edward
    type: :Person
  AddTriple (daba1433-735d-43c7-a6e8-07620b83f22c)
 Call ID: daba1433-735d-43c7-a6e8-07620b83f22c
  Args:
    relation: :hasChild
    target: Prince_Charles
    source: Prince_Philip
  AddTriple (079718ca-b89f-45f0-a6b1-af7fc9a7ad38)
 Call ID: 079718ca-b89f-45f0-a6b1-af7fc9a7ad38
  Args:
    relation: :hasChild
    target: Prince_Charles
    source: Queen_Elizabeth_II
  AddTriple (db082026-3558-4a74-8ad1-ac91919a46e8)
 Call ID: db082026-3558-4a74-8ad1-ac91919a46e8
  Args:
    source: Prince_Philip
    target: Princess_Anne
    relation: :hasChild
  AddTriple (ad07624e-4735-4fc6-8140-7331a04fa4e1)
 Call ID: ad07624e-4735-4fc6-8140-7331a04fa4e1
  Args:
    source: Queen_Elizabeth_II
    target: Princess_Anne
    relation: :hasChild
  AddTriple (f8c9c094-cc6b-4769-86ab-259a456dccc3)
 Call ID: f8c9c094-cc6b-4769-86ab-259a456dccc3
  Args:
    target: Prince_Andrew
    relation: :hasChild
    source: Prince_Philip
  AddTriple (fe6887ac-7bd7-453e-bbcc-7dc9939de213)
 Call ID: fe6887ac-7bd7-453e-bbcc-7dc9939de213
  Args:
    target: Prince_Andrew
    relation: :hasChild
    source: Queen_Elizabeth_II
  AddTriple (900ad6f8-4010-410b-8ebf-ec4d9e5611c8)
 Call ID: 900ad6f8-4010-410b-8ebf-ec4d9e5611c8
  Args:
    target: Prince_Edward
    relation: :hasChild
    source: Prince_Philip
  AddTriple (cdc52a76-b628-49c3-8083-9b5999fe85a7)
 Call ID: cdc52a76-b628-49c3-8083-9b5999fe85a7
  Args:
    relation: :hasChild
    target: Prince_Edward
    source: Queen_Elizabeth_II
  AssignClass (2fc0dd38-b180-444c-8250-2ba87ecbaba0)
 Call ID: 2fc0dd38-b180-444c-8250-2ba87ecbaba0
  Args:
    type: :Man
    source: King_George_VI
  AssignClass (0c10e4a4-2662-4dcb-bb66-2c20c8c1f08b)
 Call ID: 0c10e4a4-2662-4dcb-bb66-2c20c8c1f08b
  Args:
    source: King_George_VI
    type: :Person
  AddTriple (54d82e13-f321-45ec-b8ef-cbd6b119108a)
 Call ID: 54d82e13-f321-45ec-b8ef-cbd6b119108a
  Args:
    source: Queen_Elizabeth_II
    target: King_George_VI
    relation: :hasFather
  Finish (d616bed8-8a00-4998-8a69-d61defd7dcee)
 Call ID: d616bed8-8a00-4998-8a69-d61defd7dcee
  Args: