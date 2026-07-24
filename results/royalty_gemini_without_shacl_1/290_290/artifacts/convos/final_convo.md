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
Charles III (Charles Philip Arthur George; born 14
Charles was born during the reign of his maternal grandfather, King George VI, and became heir apparent when his mother, Queen Elizabeth II, acceded to the throne in 1952.
Charles was educated at Cheam School and Gordonstoun, and later spent six months at the Timbertop campus of Geelong Grammar School in Victoria, Australia.
He married Lady Diana Spencer in 1981 and they had two sons, William and Harry.
Charles and Diana divorced in 1996 after years of estrangement and well-publicised extramarital affairs.
Diana died the following year from injuries sustained in a car crash.
In 2005, Charles married his long-time partner, Camilla Parker Bowles.
As heir apparent, Charles undertook official duties and engagements on behalf of his mother and represented the United Kingdom on visits abroad.
He founded the Prince's Trust in 1976, sponsored the Prince's Charities and became patron or president of more than 800 other charities and organisations.
An environmentalist, Charles supported organic farming and action to address climate change during his time as manager of the Duchy of Cornwall estates, earning him awards and recognition.
Charles became king upon his mother's death in 2022.
At the age of 73 he was the oldest person to accede to the British throne, after having been the longest-serving heir apparent and Prince of Wales in British history.
Early life, family, and education

Charles was born at 9:14 pm on 14 November 1948 by caesarean section at Buckingham Palace, during the reign of his maternal grandfather, King George VI.
He was the first child of Princess Elizabeth, Duchess of Edinburgh (later Queen Elizabeth II), and Philip, Duke of Edinburgh.
He was christened Charles Philip Arthur George on 15 December in the Music Room at Buckingham Palace by the archbishop of Canterbury, Geoffrey Fisher.
George VI died on 6 February 1952, after which Charles's mother acceded to the throne as Elizabeth II and he became heir apparent.
Under a charter issued by Edward III in 1337, and as the monarch's eldest son, he automatically assumed the titles of Duke of Cornwall and, in the Scottish peerage, Duke of Rothesay, Earl of Carrick, Baron of Renfrew, Lord of the Isles, and Prince and Great Steward of Scotland.
He attended his mother's coronation at Westminster Abbey on 2 June 1953.
When Charles was five, Catherine Peebles was appointed as his governess to oversee his education at Buckingham Palace.
He did not receive preferential treatment from the school's founder and headmaster, Stuart Townend, who encouraged the Queen to have Charles train in football, noting that boys on the pitch were never deferential to anyone.
Charles later attended two of his father's former schools: Cheam School in Hampshire from 1958, followed by Gordonstoun in Moray, where he began classes in April 1962.
Jonathan Dimbleby's authorised 1994 biography described Elizabeth and Philip as physically and emotionally distant parents, and criticised Philip for disregarding Charles's sensitive nature, including insisting that Charles attend Gordonstoun, where he was bullied.
Although Charles reportedly referred to the school as "Colditz in kilts", he later praised Gordonstoun for teaching him "a great deal about myself and my own abilities and disabilities".
In a 1975 interview Charles said he was "glad" to have attended the school and that its "toughness" had been "much exaggerated".
In 1966, Charles spent two terms at the Timbertop campus of Geelong Grammar School in Victoria, Australia, during which he visited Papua New Guinea on a school trip with his history tutor, Michael Collins Persse.
Charles later described his time at Timbertop as the most enjoyable part of his education.
Reflecting on his schooling, Charles later remarked that he "didn't enjoy school as much as I might have", adding that he was "happier at home than anywhere else".
Breaking royal tradition, Charles proceeded directly to university after completing his A‐levels rather than joining the British Armed Forces.
During his second year he spent one term at the University College of Wales in Aberystwyth, studying Welsh history and Welsh language.
Charles became the first British heir apparent to earn a university degree, graduating from Cambridge in June 1970 with a Bachelor of Arts (BA) degree with lower second-class honours (2:2).
Prince of Wales

Charles was created Prince of Wales and Earl of Chester on 26 July 1958, although his investiture did not take place until 1 July 1969, when he was crowned by his mother in a televised ceremony at Caernarfon Castle.
The event was controversial in Wales amid rising Welsh nationalist sentiment.
He took his seat in the House of Lords the following year, delivering his maiden speech on 13 June 1974, the first royal to speak from the floor since the future Edward VII in 1884.
Charles increasingly undertook public duties, founding the Prince's Trust in 1976 and travelling to the United States in 1981.
Charles later remarked, "so, what are you supposed to think when you are prepared to do something to help and you are just told you're not wanted?"

Military training and career

Charles served in the Royal Air Force (RAF) and the Royal Navy during the 1970s.
After the passing-out parade that September, Charles embarked on a naval career and undertook a six-week course at the Royal Naval College, Dartmouth.
That same year he qualified as a helicopter pilot at RNAS Yeovilton, and during his helicopter training completed commando instruction at the Commando Training Centre Royal Marines at Lympstone.
Charles then joined 845 Naval Air Squadron, a Royal Marines air support unit of the Fleet Air Arm, serving as a pilot aboard HMS Hermes and flying the Royal Marines commando variant of the Westland Wessex helicopter.
Charles spent his final ten months of active naval service commanding the coastal minehunter HMS Bronington, beginning on 9 February 1976.
Charles gave up flying after crash-landing a BAe 146 in Islay in 1994, when, as a passenger invited to fly the aircraft, he was at the controls; a board of inquiry found the crew negligent.
Relationships and marriages

Bachelorhood

In his youth, Charles was romantically linked to several women.
Charles's great-uncle Lord Mountbatten advised him to "sow his wild oats and have as many affairs as he can before settling down", but, for a wife, he "should choose a suitable, attractive, and sweet-charactered girl before she has met anyone else she might fall for ...
Early in 1974, Mountbatten began corresponding with 25-year-old Charles about a potential marriage to his granddaughter, Amanda Knatchbull.
Charles wrote to Amanda's mother, Lady Brabourne, who was also his godmother, expressing interest in her daughter.
Four years later, Mountbatten arranged for Amanda and himself to accompany Charles on his 1980 visit to India.
Both fathers, however, objected: Prince Philip feared that his famous uncle would eclipse Charles, while Lord Brabourne warned that a joint visit would concentrate media attention on the cousins before they could decide whether to become a couple.
In August 1979, before Charles was due to depart alone for India, Mountbatten was assassinated by the Provisional Irish Republican Army.
When Charles returned, he proposed to Amanda.
But in addition to her grandfather, she had lost her paternal grandmother and younger brother in the bomb attack, and was now reluctant to join the royal family.
Lady Diana Spencer

Charles first met Lady Diana Spencer in 1977, while he was visiting her home, Althorp.
He was then the companion of her elder sister Sarah and did not consider Diana romantically until mid-1980.
While Charles and Diana were sitting together on a bale of hay at a friend's barbecue in July, she mentioned that he had looked forlorn and in need of care at the funeral of Lord Mountbatten.
Charles's cousin Norton Knatchbull and his wife told Charles that Diana appeared awestruck by his position and that he did not seem to be in love with her.
When Charles's father told him that the media speculation would injure Diana's reputation if Charles did not come to a decision about marrying her soon, and realising that she was a suitable royal bride (according to Mountbatten's criteria), Charles construed his father's advice as a warning to proceed without further delay.
He proposed to Diana in February 1981, with their engagement becoming official on 24 February; the wedding took place at St Paul's Cathedral on 29 July.
Upon his marriage, Charles reduced his voluntary tax contribution from the profits of the Duchy of Cornwall from 50 per cent to 25 per cent.
The couple lived at Kensington Palace and Highgrove House, near Tetbury, and had two children: William, in 1982, and Harry, in 1984.
As of 2025, Charles has an estranged relationship with his son Harry, who relinquished his royal family obligations and moved to the United States in 2020.
In 1986 Charles had fully resumed his affair with former girlfriend, Camilla Parker Bowles.
In a video tape recorded by Peter Settelen in 1992, Diana admitted that, from 1985 to 1986, she had been "deeply in love with someone who worked in this environment."
It was assumed that she was referring to Barry Mannakee, who had been transferred to the Diplomatic Protection Squad in 1986, after his managers determined his relationship with Diana had been inappropriate.
Diana later commenced a relationship with Major James Hewitt, the family's former riding instructor.
Charles and Diana's evident discomfort in each other's company led to them being dubbed "The Glums" by the press.
Diana exposed Charles's affair with Parker Bowles in a book by Andrew Morton, Diana: Her True Story.
Audio tapes of her own extramarital flirtations also surfaced, as did persistent suggestions that Hewitt is Prince Harry's father, based on a physical similarity between Hewitt and Harry.
However, Harry had already been born by the time Diana's affair with Hewitt began.
Early the following year, the British press published transcripts of a passionate, bugged telephone conversation between Charles and Parker Bowles that had taken place in 1989, which was dubbed "Tampongate" and "Camillagate".
Charles subsequently sought public understanding in a television film with Dimbleby, Charles: The Private Man, the Public Role, broadcast in June 1994.
In an interview in the film, Charles confirmed his own extramarital affair with Parker Bowles, saying that he had rekindled their association in 1986, only after his marriage to Diana had "irretrievably broken down".
This was followed by Diana's own admission of marital troubles in an interview on the BBC current affairs programme Panorama, broadcast in November 1995.
Referring to Charles's relationship with Parker Bowles, she said, "well, there were three of us in this marriage.
Charles and Diana divorced on 28 August 1996, after being advised by the Queen in December 1995 to end the marriage.
Diana died following a car crash in Paris on 31 August 1997.
Charles flew to Paris with Diana's sisters to accompany her body back to Britain.
In 2003, Diana's butler Paul Burrell published a note that he claimed had been written by Diana in 1995, in which there were allegations that Charles was "planning 'an accident' in  car, brake failure and serious head injury", so that he could remarry.
She had allegedly expressed similar concerns in October 1995 to Lord Mishcon, her solicitor, that "reliable sources" had told her "that she and Camilla would be put aside" for Charles to marry Tiggy Legge-Bourke.
When questioned by the Metropolitan Police inquiry team as a part of Operation Paget, Charles told the authorities that he did not know about his former wife's note from 1995 and could not understand why she had those feelings.
The allegations were later revealed to have been among the smears spread by journalist Martin Bashir to secure an interview with Diana for the BBC.
Camilla Parker Bowles

Because Charles and Parker Bowles were romantically involved periodically, both before and during their respective first marriages, their relationship received criticism from the public and the media.
Following both of their divorces, Charles declared his relationship with Parker Bowles was "non-negotiable" and appointed Mark Bolland to enhance Parker Bowles's public profile.
In 1999 Charles and Parker Bowles made their first public appearance as a couple at the Ritz London Hotel and the following year, she met Queen Elizabeth II at the 60th birthday party of former King Constantine II of Greece, which was seen as  an apparent seal of approval by the Queen on the relationship.
In 2003, Parker Bowles moved into Charles's official residence, Clarence House  and she accompanied Charles on almost all of his official events, including the annual Highland Games in Scotland.
Former Archbishop of Canterbury, George Carey, told The Times that Charles and Parker Bowles should marry, "He is heir to the throne and he loves her.
The Queen's consent to the marriage – as required by the Royal Marriages Act 1772 – was recorded in a Privy Council meeting on 2 March.
In Canada, the Department of Justice determined the consent of the Queen's Privy Council for Canada was not required, as the union would not produce any heirs to the Canadian throne.
Charles was the only member of the royal family to have a civil, rather than a church, wedding in England.
British government documents from the 1950s and 1960s, published by the BBC, stated that such a marriage was illegal; these claims were dismissed by Charles's spokesman and explained by the sitting government to have been repealed by the Registration Service Act 1953.
The union was scheduled to take place in a civil ceremony at Windsor Castle, with a subsequent religious blessing at the castle's St George's Chapel.
Four days before the event, it was postponed from the originally scheduled date of 8 April until the following day in order to allow Charles and some of the invited dignitaries to attend the funeral of Pope John Paul II.
Charles's parents did not attend the marriage ceremony; the Queen's reluctance to attend possibly arose from her position as Supreme Governor of the Church of England.
The blessing by Archbishop of Canterbury Rowan Williams was televised.
Since their marriage in 2005, Charles has paid tribute to Camilla repeatedly in public letters, speeches and interviews, thanking her for "steadfast support" and referring to her as "my darling wife".
Official duties

In 1965, Charles undertook his first public engagement by attending a student garden party at the Palace of Holyroodhouse.
During his time as Prince of Wales, he undertook official duties on behalf of the Queen, completing 10,934 engagements between 2002 and 2022.
Charles made regular tours of Wales, fulfilling a week of engagements each summer, and attending important national occasions, such as opening the Senedd.
The six trustees of the Royal Collection Trust met three times a year under his chairmanship.
Charles also represented his mother at the independence celebrations in Fiji in 1970, The Bahamas in 1973, Papua New Guinea in 1975, Zimbabwe in 1980 and Brunei in 1984.
In 1983, a man named Christopher John Lewis, who had fired a shot with a .22 rifle at the Queen in 1981, attempted to escape a psychiatric hospital in order to assassinate Charles, who was visiting New Zealand with Diana and William.
While Charles was visiting Australia on Australia Day in January 1994, David Kang fired two shots at him from a starting pistol in protest against the treatment of several hundred Cambodian asylum-seekers held in detention camps.
In 1995 Charles became the first member of the royal family to visit the Republic of Ireland in an official capacity.
In 1997 he represented the Queen at the Hong Kong handover ceremony.
At the funeral of Pope John Paul II in 2005, Charles caused controversy when he shook hands with Zimbabwean president Robert Mugabe, who had been seated next to him.
Charles's office subsequently released a statement saying that he could not avoid shaking Mugabe's hand and that he "finds the current Zimbabwean regime abhorrent".
Charles represented the Queen at the opening ceremony of the 2010 Commonwealth Games in Delhi, India.
In November 2013 he represented the Queen for the first time at a Commonwealth Heads of Government Meeting, in Colombo, Sri Lanka.
Charles and Camilla made their first joint trip to the Republic of Ireland in May 2015.
During the trip, he shook hands in Galway with Gerry Adams, leader of Sinn Féin and widely believed to be the leader of the IRA, the militant group that had assassinated Lord Mountbatten in 1979.
Commonwealth heads of government decided at their 2018 meeting that Charles would be the next Head of the Commonwealth after the Queen.
In March 2019, at the request of the British government, Charles and Camilla went on an official tour of Cuba, making them the first British royals to visit the country.
Charles contracted COVID-19 during the pandemic in March 2020.
Several newspapers were critical that Charles and Camilla were tested promptly at a time when many National Health Service doctors, nurses and patients had been unable to be tested expeditiously.
Charles attended the November 2021 ceremonies to mark Barbados's transition into a parliamentary republic, abolishing the position of monarch of Barbados.
He was invited by Prime Minister Mia Mottley as the future Head of the Commonwealth; it was the first time that a member of the royal family attended the transition of a realm to a republic.
In May of the following year, Charles attended the State Opening of the British Parliament, delivering the Queen's Speech on behalf of his mother, as a counsellor of state.
Reign

Charles acceded to the British throne on his mother's death on 8 September 2022.
Charles was the oldest person to succeed to the British throne, at the age of 73, surpassing the previous record holder, William IV, who was 64 when he became king in 1830.
Charles gave his first speech to the nation at 6 pm on 9 September, in which he paid tribute to his mother and announced the appointment of his elder son, William, as Prince of Wales.
The following day, the Accession Council publicly proclaimed Charles as king, the ceremony being televised for the first time.
Attendees included Queen Camilla, Prince William and the British prime minister, Liz Truss, along with her six living predecessors.
Other realms signed and read their own proclamations, as did Scotland, Wales, Northern Ireland, the British Overseas Territories, the Crown Dependencies, Canadian provinces and Australian states.
In November 2022, the King and Queen hosted the South African president, Cyril Ramaphosa, during the first official state visit to Britain of Charles's reign.
The following March, they undertook a state visit to Germany, where Charles became the first British monarch to address the Bundestag.
On 6 May 2023, Charles and Camilla's coronation took place at Westminster Abbey, in a ceremony planned for many years under the code name Operation Golden Orb.
Prior to Charles's accession, reports suggested that the coronation would be "shorter, smaller, less expensive, and more representative of different faiths and community groups than that of his mother in 1953, reflecting the King's wish to acknowledge the ethnic diversity of modern Britain".
In July 2023, the royal couple attended a national service of thanksgiving at St Giles' Cathedral, where Charles was presented with the Honours of Scotland.
In September, Charles became the first British monarch to give a speech from the French Senate chamber during a state visit to France.
In May 2024, the British prime minister, Rishi Sunak, asked the King to call a general election; subsequently, royal engagements that could divert attention from the election campaign were postponed.
In June 2024, Charles and Camilla travelled to Normandy to attend the 80th anniversary commemorations of D-Day.
In July, the annual Holyrood Week, which is usually spent in Scotland, was shortened so that Charles could return to London and appoint a new prime minister following the general election.
After Sunak's Conservative Party lost the election to the Labour Party led by Sir Keir Starmer, Charles appointed Starmer as prime minister.
In October 2024, the King and Queen toured Australia and Samoa; Australia was the first Commonwealth realm Charles visited since his accession.
Charles temporarily paused his cancer treatment during the tour.
Zelenskyy later told The Guardian that Charles played a quiet but influential role in altering US president Donald Trump's attitude toward Ukraine.
The King and Queen initially cancelled a planned visit to Vatican City during their state visit to Italy, but on 9 April 2025 – their 20th wedding anniversary – they visited Pope Francis at Domus Sanctae Marthae as he was recovering from pneumonia.
The King, accompanied by the Queen, made his first visit to Canada as monarch in May 2025 at the invitation of Prime Minister Mark Carney, a trip that took place during a period of tension with the United States after President Trump made comments questioning Canada's sovereignty.
In June 2025, the King approved the decommissioning of the British Royal Train ahead of its maintenance contract ending in 2027.
Described by the Keeper of the Privy Purse as part of a commitment to "fiscal discipline", the decision marked the end of 180 years of the royal family's use of a dedicated royal train.
In October 2025, during his state visit to the Holy See, Charles became the first British monarch to pray alongside a pope since the Reformation, joining Pope Leo XIV for a church service in the Sistine Chapel of the Apostolic Palace in Vatican City.
Later that month, Charles undertook his first official engagement in support of the LGBT+ community, unveiling "An Opened Letter", the UK's first national memorial honouring LGBT armed forces veterans, at the National Memorial Arboretum in Staffordshire.
On 30 October, amid continuing controversy surrounding his brother Andrew's association with the American financier and child sex offender Jeffrey Epstein, Charles initiated a formal process to remove his style, titles and honours.
Following Andrew's arrest on 19 February 2026 on suspicion of misconduct in public office, the King expressed his "deepest concern" and stated that "the law must take its course".
In April 2026, during a state visit to the United States, Charles became the second British monarch to address a joint meeting of Congress, after his mother Elizabeth II in 1991.
Health

In March 1998, Charles had laser keyhole surgery on his right knee and in March 2003, he underwent surgery at King Edward VII's Hospital to treat a hernia injury.
In January 2024, Charles underwent a "corrective procedure" at the London Clinic to treat benign prostate enlargement, which resulted in the postponement of some of his public engagements.
In February Buckingham Palace announced that cancer had been discovered during the treatment, but that it was not prostate cancer.
Although his public duties were postponed, it was reported Charles would continue to fulfil his constitutional functions during his outpatient treatment.
In March, Camilla deputised for him in his absence at the Commonwealth Day service at Westminster Abbey and at the Royal Maundy at Worcester Cathedral.
He made his first major public appearance since his cancer diagnosis at the Easter service held at St George's Chapel, Windsor Castle, on 31 March.
In March 2025, Charles was briefly admitted to hospital after experiencing temporary side effects from his cancer treatment.
Diet

As early as 1985, Charles was questioning meat consumption.
In the 1985 Royal Special television programme, he told the host, Alastair Burnet, that "I actually now don't eat as much meat as I used to.
In 2021, Charles spoke to the BBC about the environment and revealed that, two days per week, he eats no meat nor fish and, one day per week, he eats no dairy products.
Ahead of Christmas dinner in 2022, Charles confirmed to the animal rights group People for the Ethical Treatment of Animals that foie gras would not be served at any royal residences; he had stopped the use of foie gras at his own properties for more than a decade before becoming king.
During a September 2023 state banquet at the Palace of Versailles, it was reported that he did not want foie gras or out-of-season asparagus on the menu.
Charity work

Since founding the Prince's Trust in 1976, using his £7,500 of severance pay from the Royal Navy, Charles has established 16 more charitable organisations and now serves as president of each.
Together they form a loose alliance, the Prince's Charities, which describes itself as "the largest multi-cause charitable enterprise in the United Kingdom, raising more than £100 million annually ...  active across a broad range of areas including education and young people, environmental sustainability, the built environment, responsible business and enterprise, and international".
King Charles III Charitable Fund has donated over £73 million to various causes since 1979.
By September 2020 the Prince's Trust had supported over 1,000,000 young people and created 125,000 entrepreneurs.
As Prince of Wales, Charles became patron or president of more than 800 other charities and organisations.
He received a Gold Blue Peter badge in 2023 for his environmental work and for his support of young people through the Prince's Trust.
The Prince's Charities Canada was established in 2010, in a similar fashion to its namesake in Britain.
Charles uses his tours of Canada as a way to help to draw attention to youth, the disabled, the environment, the arts, medicine, the elderly, heritage conservation and education.
He has also set up the Prince's Charities Australia, based in Melbourne, to provide a co-ordinating presence for his Australian and international charitable endeavours.
Charles has supported humanitarian projects; for example, he has been known to donate his blood to raise awareness for health causes..
Charles and his sons took part in ceremonies that marked the 1998 International Day for the Elimination of Racial Discrimination.
Charles expressed strong concerns about the human rights record of the Romanian dictator Nicolae Ceaușescu.
Charles has also supported humanitarian causes in Israel, including a private donation to the Peres Center for Peace and Innovation in 2020.
Investigations of donations

Two of Charles's charities, the Prince's Foundation and the Prince of Wales's Charitable Fund (later renamed the King's Foundation and King Charles III Charitable Fund), came under scrutiny in 2021 and 2022 for accepting donations many in the media deemed inappropriate.
In August 2021 it was announced that the Prince's Foundation was launching an investigation into the reports, with Charles's support.
The Charity Commission also launched an investigation into allegations that the donations meant for the Prince's Foundation had been instead sent to the Mahfouz Foundation.
In February 2022, the Metropolitan Police launched an investigation into the cash-for-honours allegations linked to the foundation, passing their evidence to the Crown Prosecution Service for deliberation in October.
In August 2023 the Metropolitan Police announced that they had concluded their investigations and no further action would be taken.
The Times reported in June 2022 that, between 2011 and 2015, Charles accepted €3 million in cash from the Prime Minister of Qatar, Hamad bin Jassim bin Jaber Al Thani.
In the same month, The Times reported that the Prince of Wales's Charitable Fund received a donation of £1 million from Bakr bin Laden and Shafiq bin Laden – both half-brothers of Osama bin Laden – during a private meeting in 2013.
Personal interests

From young adulthood, Charles encouraged the understanding of Indigenous voices, saying they held crucial messages about preservation of the land, respecting community and shared values, resolving conflict, and recognising and making good on past iniquities.
At the 2022 Commonwealth Heads of Government Meeting Charles, who was representing his mother, raised that reconciliation process as an example for dealing with the history of slavery in the British Empire, for which he expressed his sorrow.
Letters sent by Charles to British government ministers in 2004 and 2005 expressing his concerns over various policy issues – known as the black spider memos – presented potential embarrassment following a challenge by The Guardian to release the letters under the Freedom of Information Act 2000.
In March 2015 the Supreme Court of the United Kingdom decided that Charles's letters must be released.
The reaction was largely supportive of Charles, with little criticism of him; the press variously described the memos as "underwhelming" and "harmless", and concluded that their release had "backfired on those who seek to belittle him".
It was revealed in the same year that Charles had access to confidential Cabinet papers.
In October 2020, a letter sent by Charles to the Governor-General of Australia, Sir John Kerr, after Kerr's dismissal of Prime Minister Gough Whitlam in 1975, was released as part of the collection of palace letters regarding the Australian constitutional crisis.
In the letter, Charles was supportive of Kerr's decision, writing that what Kerr "did last year was right and the courageous thing to do".
The Times reported in June 2022 that Charles had privately described the British government's Rwanda asylum plan as "appalling" and he feared that it would overshadow the Commonwealth Heads of Government Meeting in Rwanda that same month.
It was later claimed that Cabinet ministers had warned Charles to avoid making political comments, as they feared a constitutional crisis could arise if he continued to make such statements once he became King.
Built environment

Charles has openly expressed his views on architecture and urban planning; he fostered the advancement of New Classical architecture and asserted that he "care deeply about issues such as the environment, architecture, inner-city renewal, and the quality of life."
In a speech given for the 150th anniversary of the Royal Institute of British Architects in May 1984, he described a proposed extension to the National Gallery in London as a "monstrous carbuncle on the face of a much-loved friend" and deplored the "glass stumps and concrete towers" of modern architecture.
Charles called for local community involvement in architectural choices and asked, "why has everything got to be vertical, straight, unbending, only at right angles – and functional?"
Charles has "a deep understanding of Islamic art and architecture", according to the Oxford professor Mohammed Talib, and has been involved in the construction of a building and garden at the Oxford Centre for Islamic Studies that combine Islamic and Oxford architectural styles.
In Charles's 1989 book A Vision of Britain, and in speeches and essays, he has been critical of modern architecture, arguing that traditional designs and methods should guide contemporary ones.
Two of his charities – the Prince's Regeneration Trust and the Prince's Foundation for Building Community, which were later merged into one charity – promote his views.
The village of Poundbury was built on land owned by the Duchy of Cornwall to a master plan by Léon Krier, under the guidance of Charles and in line with his philosophy.
In 2013 developments for the suburb of Nansledan began on the estate of the Duchy of Cornwall with Charles's endorsement.
Charles helped purchase Dumfries House and its complete collection of 18th century furnishings in 2007, taking a £20 million loan from his charitable trust to contribute towards the £45 million cost.
The house and gardens remain property of the Prince's Foundation and serve as a museum and community and skills training centre.
After lamenting in 1996 the unbridled destruction of many of Canada's historic urban cores, Charles offered his assistance to the Department of Canadian Heritage in creating a trust modelled on Britain's National Trust, a plan that was implemented with the passage of the federal budget in 2007.
In 1999 Charles agreed to the use of his title for the Prince of Wales Prize for Municipal Heritage Leadership, awarded by the National Trust for Canada to municipal governments that have committed to the conservation of historic places.
Whilst visiting the US and surveying the damage caused by Hurricane Katrina, Charles received the National Building Museum's Vincent Scully Prize in 2005 for his efforts in regard to architecture; he donated US$25,000 of the prize money towards restoring storm-damaged communities.
For his work as patron of New Classical architecture, Charles was awarded the 2012 Driehaus Architecture Prize from the University of Notre Dame.
The Worshipful Company of Carpenters installed Charles as an Honorary Liveryman "in recognition of his interest in London's architecture.
"


Charles has occasionally intervened in projects that employ architectural styles such as modernism and functionalism.
In 2009 he wrote to the Qatari royal family – the financier of the redevelopment of the Chelsea Barracks site – labelling Lord Rogers's design for the site "unsuitable".
Rogers claimed that Charles had also intervened to block his designs for the Royal Opera House and Paternoster Square.
CPC Group, the project developer, took a case against Qatari Diar to the High Court.
After the suit was settled, the CPC Group apologised to Charles "for any offence caused ... during the course of the proceedings".
Natural environment

Since the 1970s, Charles has promoted environmental awareness.
Charles was named one of Time Magazine's 100 most influential climate leaders of 2025.
An avid gardener, Charles has also emphasised the importance of talking to plants, stating that "I happily talk to the plants and trees, and listen to them.
Upon moving into Highgrove House, Charles developed an interest in organic farming, which culminated in the 1990 launch of his own organic brand, Duchy Originals, which sells more than 200 different sustainably produced products; the profits (more than £6 million by 2010) are donated to the Prince's Charities.
Charles became involved with farming and various industries within it, regularly meeting with farmers to discuss their trade.
A prominent critic of the practice, Charles has also spoken against the use of genetically modified crops, and in a letter to Tony Blair in 1998 he criticised the development of genetically modified foods.
The Sustainable Markets Initiative – a project that encourages putting sustainability at the centre of all activities – was launched by Charles at the World Economic Forum's annual meeting in Davos in January 2020.
The holy chrism oil used at Charles's coronation was vegan, made from oils of olive, sesame, rose, jasmine, cinnamon, neroli and benzoin, along with amber and orange blossom.
His mother's chrism oil contained animal-based oils.
Charles delivered a speech at the 2021 G20 Rome summit, describing COP26 as "the last chance saloon" for preventing climate change and asking for actions that would lead to a green-led, sustainable economy.
In 2022, the media alleged that Liz Truss had advised Charles against attending COP27, to which advice he agreed.
Charles delivered the opening speech at COP28, saying among others he prayed "with all my heart that COP28 will be a critical turning point towards genuine transformational action."
Charles, who is patron of the Cambridge Institute for Sustainability Leadership, introduced the Climate Action Scholarships for students from small island nations in partnership with the University of Cambridge, the University of Toronto, the University of Melbourne, McMaster University and the University of Montreal in March 2022.
In 2010, he funded the Prince's Countryside Fund (renamed the Royal Countryside Fund in 2023), a charity that aims for a "confident, robust and sustainable agricultural and rural community".
Alternative medicine

Charles has controversially championed alternative medicine, including homeopathy.
Similarly, the Prince's Foundation for Integrated Health (FIH) attracted opposition from the scientific and medical community over its campaign encouraging general practitioners to offer herbal and other alternative treatments to NHS patients.
That year, Ernst published a book with Simon Singh called Trick or Treatment: Alternative Medicine on Trial and mockingly dedicated to "HRH the Prince of Wales".
The last chapter is highly critical of Charles's advocacy of complementary and alternative treatments.
Charles's Duchy Originals produced a variety of complementary medicinal products, including a "Detox Tincture" that Ernst denounced as "financially exploiting the vulnerable" and "outright quackery".
Charles personally wrote at least seven letters to the Medicines and Healthcare products Regulatory Agency shortly before it relaxed the rules governing labelling of such herbal products, a move that was widely condemned by scientists and medical bodies.
It was reported in October 2009 that Charles had lobbied the health secretary, Andy Burnham, regarding greater provision of alternative treatments in the NHS.
The FIH was re-branded and re-launched later in 2010 as the College of Medicine, of which Charles became a patron in 2019.
Sports

From his youth until 2005, Charles was an avid player of competitive polo.
Charles also frequently took part in fox hunting until the sport was banned in the United Kingdom, also in 2005.
By the late 1990s opposition to the activity was growing when Charles's participation was viewed as a "political statement" by those who were opposed to it.
Charles suffered several polo- and hunting-related injuries throughout the years, including a two-inch scar on his left cheek in 1980, a broken arm in 1990, a torn cartilage in his left knee in 1992, a broken rib in 1998, and a fractured shoulder in 2001.
Charles has been a keen salmon angler since youth and supported Orri Vigfússon's efforts to protect the North Atlantic salmon.
Charles is a supporter of Burnley F.C.


Apart from hunting, Charles has also participated in target rifle competitions, representing the House of Lords in the Vizianagram Match (Lords vs. Commons) at Bisley.
Visual, performing, and literary arts

Charles has been involved in performance since his youth, and appeared in sketches and revues while studying at Cambridge.
Charles is president or patron of more than 20 performing arts organisations, including the Royal College of Music, Royal Opera, English Chamber Orchestra, Philharmonia Orchestra, Welsh National Opera, Royal Shakespeare Company (attending performances in Stratford-Upon-Avon, supporting fundraising events, and attending the company's annual general meeting), British Film Institute, and Purcell School.
In 2000 he revived the tradition of appointing an official harpist to the Prince of Wales, in order to foster Welsh talent at playing the national instrument of Wales.
Charles is a keen watercolourist, having published books on the subject and exhibited and sold a number of his works to raise money for charity; in 2016 it was estimated that he had sold lithographs of his watercolours for a total of £2 million from a shop at his Highgrove House residence.
For his 50th birthday 50 of his watercolours were exhibited at Hampton Court Palace and, for his 70th birthday, his works were exhibited at the National Gallery of Australia.
Charles founded the Royal Drawing School in 2000, which offers drawing classes to children and the public.
To mark the 25th anniversary of his investiture as Prince of Wales in 1994, the Royal Mail issued a series of postage stamps that featured his paintings.
Charles is Honorary President of the Royal Academy of Arts Development Trust and, in 2015, 2022 and 2023, commissioned paintings of 12 D-Day veterans, seven Holocaust survivors, and ten members of the Windrush generation, respectively, which went on display at the Queen's Gallery in Buckingham Palace.
Charles is the author of several books and has contributed a foreword or preface to numerous books by others.
Religion and philosophy

Shortly after his accession to the throne, Charles publicly described himself as "a committed Anglican Christian"; at age 16, during Easter 1965, he had been confirmed into the Anglican Communion by Archbishop of Canterbury Michael Ramsey in St George's Chapel, Windsor Castle.
He attends services at various Anglican churches close to Highgrove and attends the Church of Scotland's Crathie Kirk with the rest of the royal family when staying at Balmoral Castle.
Laurens van der Post became a friend of Charles in 1977; he was dubbed Charles's "spiritual guru" and was godfather to Prince William.
From van der Post, Charles developed a focus on philosophy and an interest in other religions.
Charles expressed his philosophical views in his 2010 book, Harmony: A New Way of Looking at Our World, which won a Nautilus Book Award.
Charles also attended the consecration of Britain's first Syriac Orthodox cathedral, St Thomas Cathedral, Acton.
Charles is patron of the Oxford Centre for Islamic Studies at the University of Oxford and attended the inauguration of the Markfield Institute of Higher Education, which is dedicated to Islamic studies in a multicultural context.
In his 1994 documentary with Dimbleby, Charles said that, when king, he wished to be seen as a "defender of faith", rather than the British monarch's traditional title of Defender of the Faith, "prefer to embrace all religious traditions and 'the pattern of the divine, which I think is in all of us.'"
Charles reaffirmed this theme shortly after his accession and declared that his duties as sovereign included "the duty to protect the diversity of our country, including by protecting the space for faith itself and its practice through the religions, cultures, traditions, and beliefs to which our hearts and minds direct us as individuals."
Although the text of the coronation oath was not altered, because the process of passing new legislation through Parliament would be lengthy and liable to raise divisive issues, a preamble spoken by the Archbishop of Canterbury was added to the text:


Your Majesty, the Church established by law, whose settlement you will swear to maintain, is committed to the true profession of the Gospel, and, in so doing, will seek to foster an environment in which people of all faiths and beliefs may live freely.
In line with his multi-faith approach, Charles has served as a patron of the Council of Christians and Jews and of the Jewish Museum London.
Media image and public opinion

Since his birth, Charles has received close media attention, which increased as he matured.
It has been an ambivalent relationship, largely impacted by his marriages to Diana and Camilla and their aftermath, but also centred on his future conduct as king.
Described as the "world's most eligible bachelor" in the late 1970s, Charles was subsequently overshadowed by Diana.
After her death the media regularly breached Charles's privacy and printed exposés.
In September 2025, The Economist analysed all Charles's public speeches over the past 30 years and concluded that he has mellowed over the past three decades.
In 2009, Charles was named the world's best-dressed man by Esquire magazine.
Fashion magazine British GQ described Charles as "the true guardian of traditional British menswear" in 2012 and named him one of the most stylish people of 2025.
Italian designer Donatella Versace once said Charles "is an archetype of style".
In 2023 the New Statesman named Charles as the fourth-most-powerful right-wing figure of the year, describing him as a "romantic traditionalist" and "the very last reactionary in public life" for his support of various traditionalist think tanks and previous writings.
Charles and Camilla topped Tatler's Social Power Index for 2022 and 2023.
A 2018 BMG Research poll found that 46 per cent of Britons wanted Charles to abdicate immediately on his mother's death, in favour of William.
On his accession to the throne, The Statesman reported an opinion poll that put Charles's popularity with the British people at 42 per cent.
As of August 2025, Charles continues to hold majority support with an approval rating of 59 per cent, and 62 percent of the public say "he is doing a good job", according to YouGov.
Reaction to press treatment

In 1994, the German tabloid Bild published nude photos of Charles that were taken while he was vacationing in Le Barroux; they had reportedly been put up for sale for £30,000.
Buckingham Palace reacted by stating that it was "unjustifiable for anybody to suffer this sort of intrusion".
Charles, "so often a target of the press, got his chance to return fire" in 2002, when addressing "scores of editors, publishers, and other media executives" gathered at St Bride's Fleet Street to celebrate 300 years of journalism.
"


In 2006, Charles filed a court case against The Mail on Sunday, after excerpts of his personal journals were published, revealing his opinions on matters such as the transfer of sovereignty over Hong Kong to China in 1997, in which Charles described the Chinese government officials as "appalling old waxworks".
Charles and Camilla were named in 2011 as individuals whose confidential information was reportedly targeted or actually acquired in conjunction with the news media phone hacking scandal.
The Independent noted in 2015 that Charles would only speak to broadcasters "on the condition they have signed a 15-page contract, demanding that Clarence House attends both the 'rough cut' and 'fine cut' edits of films and, if it is unhappy with the final product, can 'remove the contribution in its entirety from the programme'."
This contract stipulated that all questions directed at Charles must be pre-approved and vetted by his representatives.
Residences and finance


In 2023, The Guardian estimated Charles's personal wealth at £1.8 billion.
This estimate includes the assets of the Duchy of Lancaster worth £653 million (and paying Charles an annual income of £20 million), jewels worth £533 million, real estate worth £330 million, shares and investments worth £142 million, a stamp collection worth at least £100 million, racehorses worth £27 million, artworks worth £24 million and cars worth £6.3 million.
Most of this wealth, which he inherited from his mother, Elizabeth II, was exempt from inheritance tax.
Clarence House, previously the residence of the Queen Mother, was Charles's official London residence from 2003, after being renovated at a cost of £6.1 million.
He previously shared apartments eight and nine at Kensington Palace with Diana before moving to York House at St James's Palace, which remained his principal residence until 2003.
Highgrove House in Gloucestershire is owned by the Duchy of Cornwall, having been purchased for Charles's use in 1980, and which he rented for £336,000 per annum.
Since William became Duke of Cornwall, Charles is expected to pay £700,000 per annum for use of the property.
Charles also owns a property near the village of Viscri in Romania.
As Prince of Wales, Charles's primary source of income was generated from the Duchy of Cornwall, which owns 133,658 acres of land (around 54,090 hectares), including farming, residential, and commercial properties, as well as an investment portfolio.
Since 1993, he has paid tax voluntarily under the Memorandum of Understanding on Royal Taxation, updated in 2013.
Titles, styles, honours, and arms

Titles and styles

Charles has held many titles and honorary military positions throughout the Commonwealth, is sovereign of many orders in his own countries and has received honours and awards from around the world.
Charles is also styled Defender of the Faith.
There had been speculation throughout Elizabeth II's reign as to what regnal name Charles would choose upon his accession; instead of Charles III, he could have chosen to reign as George VII or used one of his other given names.
It was reported that he might use George in honour of his grandfather George VI and to avoid associations with previous controversial kings named Charles.
Charles's office asserted in 2005 that no decision had yet been made.
Speculation continued for a few hours following his mother's death, until Prime Minister Liz Truss announced and Clarence House confirmed that Charles had chosen the regnal name Charles III.
Charles, who left active military service in 1976, was awarded the highest rank in all three armed services in 2012 by his mother: Admiral of the Fleet, Field Marshal, and Marshal of the Royal Air Force.
Arms

As Prince of Wales, Charles's coat of arms was based on the arms of the United Kingdom, differenced with a white label and an inescutcheon of the Principality of Wales, surmounted by the heir apparent's crown, and with the motto Ich dien (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}German: , "I serve") instead of Dieu et mon droit.
When Charles became king, he inherited the royal coats of arms of the United Kingdom and of Canada.
The design of his royal cypher, featuring a depiction of the Tudor Crown instead of St Edward's Crown, was revealed on 27 September 2022.
On 10 October 2024, designed by artist Timothy Noad, the new Royal Arms, alongside the new Lesser Arms, used by the UK government were officially unveiled, with both arms reflecting the stylistic changes made after Charles's accession.
Banners, flags, and standards

As heir apparent

The banners used by Charles as Prince of Wales varied depending upon location.
His personal standard for the United Kingdom was the Royal Standard of the United Kingdom differenced as in his arms, with a label of three points argent and the escutcheon of the arms of the Principality of Wales in the centre.
It was used outside Wales, Scotland, Cornwall and Canada, and throughout the entire United Kingdom when Charles was acting in an official capacity associated with the British Armed Forces.
The personal flag for use in Wales was based upon the Royal Badge of Wales.
In Scotland the personal banner used between 1974 and 2022 was based upon three ancient Scottish titles: Duke of Rothesay (heir apparent to the King of Scots), High Steward of Scotland, and Lord of the Isles.
In Cornwall, the banner was the arms of the Duke of Cornwall.
In 2011, the Canadian Heraldic Authority introduced a personal heraldic banner for the Prince of Wales for Canada, consisting of the shield of the Royal Coat of Arms of Canada defaced with both a blue roundel of the Prince of Wales's feathers surrounded by a wreath of gold maple leaves and a white label of three points.
As sovereign

The royal standard of the United Kingdom is used to represent the King in the United Kingdom and on official visits overseas, except in Australia and Canada.
It is the royal arms in banner form undifferentiated, having been used by successive British monarchs since 1702.
The royal standard of Canada is used by the King in Canada and while acting on behalf of Canada overseas.
It is the escutcheon of the Royal Coat of Arms of Canada in banner form undifferentiated.
Ancestry

Published works

As Prince of Wales, Charles wrote four books and was a co-author of other works.
See also

Notes

References

Citations

Bibliography

Further reading

External links

  Royal Navy (1SL & CNS)


  British Army (CGS)


  Royal Air Force (CAS)



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
  AssignClass (f6e379f3-37f6-4794-838f-b50a08d59472)
 Call ID: f6e379f3-37f6-4794-838f-b50a08d59472
  Args:
    type: :Man
    source: Charles_III
  AssignClass (9858c279-6e30-4ecf-b2ba-b9e70e7eaa2e)
 Call ID: 9858c279-6e30-4ecf-b2ba-b9e70e7eaa2e
  Args:
    type: :Person
    source: Charles_III
  AddLiteral (20827a24-dbe1-4704-8bc5-ba46675803cb)
 Call ID: 20827a24-dbe1-4704-8bc5-ba46675803cb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Charles_III
    literal_value: 1948
  AssignClass (964be994-4f0e-42fb-bc05-f43c92bce08c)
 Call ID: 964be994-4f0e-42fb-bc05-f43c92bce08c
  Args:
    type: :Man
    source: George_VI
  AssignClass (d7b4bcd0-b0db-4acf-bfa0-ab3c4632330f)
 Call ID: d7b4bcd0-b0db-4acf-bfa0-ab3c4632330f
  Args:
    type: :Person
    source: George_VI
  AddTriple (39c9ccb6-0713-4b47-9e07-6b4b5c5aac19)
 Call ID: 39c9ccb6-0713-4b47-9e07-6b4b5c5aac19
  Args:
    target: George_VI
    relation: :hasFather
    source: Charles_III
  AssignClass (c02e3b83-e7af-4781-b60d-a45545dfb975)
 Call ID: c02e3b83-e7af-4781-b60d-a45545dfb975
  Args:
    type: :Woman
    source: Elizabeth_II
  AssignClass (b8da7bbd-f2ce-456c-97b8-a423e6f1f4ee)
 Call ID: b8da7bbd-f2ce-456c-97b8-a423e6f1f4ee
  Args:
    type: :Person
    source: Elizabeth_II
  AddTriple (5bd8d9bd-b7b9-4882-9bef-80c75348c6f8)
 Call ID: 5bd8d9bd-b7b9-4882-9bef-80c75348c6f8
  Args:
    source: Charles_III
    target: Elizabeth_II
    relation: :hasMother
  AssignClass (d0081ec0-8fe1-4e45-af55-fb2c6b6e8006)
 Call ID: d0081ec0-8fe1-4e45-af55-fb2c6b6e8006
  Args:
    type: :Man
    source: Philip_Duke_of_Edinburgh
  AssignClass (3384e061-9cc4-4a0f-b400-3156888e1c3a)
 Call ID: 3384e061-9cc4-4a0f-b400-3156888e1c3a
  Args:
    type: :Person
    source: Philip_Duke_of_Edinburgh
  AddTriple (e4cc46db-0265-4036-8c81-f9de36883448)
 Call ID: e4cc46db-0265-4036-8c81-f9de36883448
  Args:
    source: Charles_III
    relation: :hasFather
    target: Philip_Duke_of_Edinburgh
  AssignClass (66d3e222-c649-409d-b39b-5ad26e20ecd4)
 Call ID: 66d3e222-c649-409d-b39b-5ad26e20ecd4
  Args:
    type: :Woman
    source: Diana_Spencer
  AssignClass (06f0b004-1cc9-41f9-a246-ef1d90365a60)
 Call ID: 06f0b004-1cc9-41f9-a246-ef1d90365a60
  Args:
    type: :Person
    source: Diana_Spencer
  AddLiteral (88d08f2d-0bb9-4eca-8e2c-7ab2f52b128c)
 Call ID: 88d08f2d-0bb9-4eca-8e2c-7ab2f52b128c
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Charles_III
    literal_value: 1981
  AssignClass (893233a4-adb4-4f56-b35d-aad5d5f85ba8)
 Call ID: 893233a4-adb4-4f56-b35d-aad5d5f85ba8
  Args:
    type: :Man
    source: William
  AssignClass (b14f26d6-5728-4fd3-9fbc-f484118415cc)
 Call ID: b14f26d6-5728-4fd3-9fbc-f484118415cc
  Args:
    type: :Person
    source: William
  AddTriple (40633412-e442-4941-bfe4-e18dfe226b83)
 Call ID: 40633412-e442-4941-bfe4-e18dfe226b83
  Args:
    source: Charles_III
    target: William
    relation: :hasSon
  AddTriple (5cfbd6ed-a796-4069-88b8-05350181b28c)
 Call ID: 5cfbd6ed-a796-4069-88b8-05350181b28c
  Args:
    source: William
    target: Diana_Spencer
    relation: :hasMother
  AssignClass (984a1683-1577-4eae-9fff-2ff016c1ce8f)
 Call ID: 984a1683-1577-4eae-9fff-2ff016c1ce8f
  Args:
    type: :Man
    source: Harry
  AssignClass (4cde12c7-8891-471b-b3f8-dc85da9aa16a)
 Call ID: 4cde12c7-8891-471b-b3f8-dc85da9aa16a
  Args:
    type: :Person
    source: Harry
  AddTriple (f372b01f-3f65-4d9b-a5fa-07e3b80a1db3)
 Call ID: f372b01f-3f65-4d9b-a5fa-07e3b80a1db3
  Args:
    relation: :hasSon
    target: Harry
    source: Charles_III
  AddTriple (48d2ae79-3949-4d19-9ff7-d7bb6d9fee30)
 Call ID: 48d2ae79-3949-4d19-9ff7-d7bb6d9fee30
  Args:
    source: Harry
    target: Diana_Spencer
    relation: :hasMother
  AssignClass (24995e70-306c-42e4-87e6-172d0a5b4df0)
 Call ID: 24995e70-306c-42e4-87e6-172d0a5b4df0
  Args:
    type: :Woman
    source: Camilla_Parker_Bowles
  AssignClass (8e9b3df1-dbd4-4aa2-95fc-139469e939f1)
 Call ID: 8e9b3df1-dbd4-4aa2-95fc-139469e939f1
  Args:
    type: :Person
    source: Camilla_Parker_Bowles
  AddLiteral (da57c7be-0939-4e1f-a6cb-6da8d6997649)
 Call ID: da57c7be-0939-4e1f-a6cb-6da8d6997649
  Args:
    source: Charles_III
    literal_value: 2005
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (5accf833-a56d-4cd6-8076-89f7cb095107)
 Call ID: 5accf833-a56d-4cd6-8076-89f7cb095107
  Args: