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
Andrew Albert Christian Edward Mountbatten-Windsor (born 19 February 1960), formerly Prince Andrew, Duke of York, is the third child and second son of Queen Elizabeth II and Prince Philip, Duke of Edinburgh, and a younger brother of King Charles III.
Andrew was born second in the line of succession to the British throne and is eighth as of 2026.
Serving in the Royal Navy from 1979 to 2001, Andrew saw active duty as a helicopter pilot during the Falklands War; he later became a helicopter instructor and commanded a warship.
He married Sarah Ferguson in 1986, and was created Duke of York on their wedding day.
From 2001 to 2011, Andrew served as the UK's Special Representative for International Trade and Investment, but resigned following scrutiny of his expenses and associations with controversial figures.
He continued to undertake official duties on behalf of Elizabeth II until 2019.
Andrew had a long-standing association with the American financier and child sex offender Jeffrey Epstein.
In 2014, Virginia Giuffre said that she had been sex trafficked to Andrew by Epstein and Ghislaine Maxwell.
Andrew denied any wrongdoing, and in 2022 settled a civil lawsuit with Giuffre in the United States without admission of liability.
In the same year, Elizabeth II removed his military affiliations and patronages, and he ceased using the style "Royal Highness".
In 2025, Charles III removed Andrew's remaining royal styles and honours, and restricted his use of titles and peerages.
Following the release of more Epstein files in early 2026, Andrew was arrested on suspicion of misconduct in public office and was later released under investigation.
Early life

During a 45-day tour of Canada in June and July 1959, Queen Elizabeth II discovered that she was pregnant.
After her return to London, Buckingham Palace announced on 7 August that she would not undertake further public engagements, a customary indication of royal pregnancy.
Andrew was born a prince at 3:30 pm on 19 February 1960 at Buckingham Palace, the third child and second son of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
He was christened Andrew Albert Christian Edward in the Music Room at the palace on 8 April.
Andrew was the first child born to a reigning British monarch since Princess Beatrice, the youngest daughter of Queen Victoria, in 1857.
Like his siblings, Charles, Anne and Edward, he was looked after by a governess, who oversaw his early education at Buckingham Palace.
Naval military service

Training

The Royal Household announced in November 1978 that Andrew would join the Royal Navy the following year.
On 1 September that year, Andrew was appointed a midshipman and entered Britannia Royal Naval College, Dartmouth.
After passing out from Dartmouth, Andrew undertook elementary flying training with the Royal Air Force at RAF Leeming, followed by basic flying training with the navy at HMS Seahawk, where he learned to fly the Gazelle helicopter.
Andrew's presence on board, and the risk of a royal family member being killed in action, made the British government apprehensive, and the Cabinet sought to move him to a desk role for the duration of the conflict.
The Queen, however, insisted that her son remain with his ship.
Andrew served on Invincible as a Sea King helicopter co-pilot, flying missions that included anti-submarine and anti-surface warfare, Exocet missile decoy operations, casualty evacuation, transport, and search and air rescue.
At the end of the war, Invincible returned to Portsmouth, where Elizabeth and Philip joined other families of the crew in welcoming the vessel home.
According to historian Andrew Lownie, the Argentine military government planned, but ultimately did not attempt, to assassinate Andrew on Mustique in July 1982.
Although he had brief assignments to HMS Illustrious, RNAS Culdrose, and the School of Service Intelligence, Andrew remained with Invincible until 1983.
Commander Nigel Ward's memoir Sea Harrier Over the Falklands described Andrew as "an excellent pilot and a very promising officer.
"


Career officer

In late 1983, Andrew transferred to RNAS Portland and was trained to fly the Lynx helicopter.
On 1 February 1984, he was promoted to lieutenant, after which Elizabeth appointed him her personal aide-de-camp.
Andrew served aboard HMS Brazen as a flight pilot until 1986, including deployment to the Mediterranean Sea as part of Standing NRF Maritime Group 2.
He later served on HMS Edinburgh as officer of the watch and Assistant Navigating Officer until 1989, including a six-month deployment to the Far East as part of exercise Outback 88.
From 1989 to 1991, Andrew served as flight commander and pilot of the Lynx HAS3 on HMS Campbeltown.
From 1993 to 1994 Andrew commanded the Hunt-class minehunter HMS Cottesmore.
From 1995 to 1996, Andrew was posted as senior pilot of 815 Naval Air Squadron, then the largest flying unit in the Fleet Air Arm.
In July that year, Andrew was retired from the Active List of the Navy.
He was made an honorary captain in 2004, promoted to rear admiral on his 50th birthday on 19 February 2010, and to vice admiral in 2015.
Personal life

Relationships

Before marriage

In May 1978, the Evening News reported that Andrew had acquired the nickname "Randy Andy" (with "randy" being British slang for "sexually eager") while at Gordonstoun, owing to his being romantically involved with several women.
Andrew met the American photographer and actress Koo Stark in February 1981, before his active service in the Falklands War.
Tina Brown later described Stark as Andrew's only serious love interest.
The couple separated in 1983 under pressure from the press and the palace.
In 1997, Andrew became godfather to Stark's daughter.
When Andrew faced accusations in 2015 regarding his association to Jeffrey Epstein, Stark publicly defended him.
Marriage and children

Andrew married Sarah Ferguson at Westminster Abbey on 23 July 1986.
On the same day, Elizabeth created him Duke of York, Earl of Inverness and Baron Killyleagh; the first two of these titles had previously been held by both his maternal grandfather, George VI, and his great-grandfather George V. Andrew had known Ferguson since childhood; they had met occasionally at polo matches and became reacquainted at Royal Ascot in 1985.
The couple initially appeared to have a happy marriage and had two daughters, Princess Beatrice (born 1988) and Princess Eugenie (born 1990), presenting a united public image during the late 1980s.
Sarah's personal qualities were regarded as refreshing within the formal protocol of the royal family.
Andrew's frequent travel due to his naval career, combined with relentless and often critical media attention on the Duchess of York, contributed to strains in the marriage.
That August, tabloid newspapers published photographs of the businessman John Bryan sucking Sarah's toes, effectively ending any prospect of reconciliation.
Throughout the separation, Ferguson had maintained that Bryan was her financial adviser, a claim Andrew accepted.
Andrew spoke warmly of his former wife in 2008, saying, "We have managed to work together to bring our children up in a way that few others have been able to and I am extremely grateful to be able to do that.
"


In May 2010, Ferguson was filmed by a News of the World reporter stating that Andrew had agreed that, if she were to receive £500,000, he would meet the donor and provide useful top-level business contacts.
The newspaper reported that Andrew had no knowledge of the arrangement.
In July 2011, Ferguson said that her multi-million-pound debts had been cleared through the intervention of her former husband, whom she described as a "knight on a white charger".
In 2011, Ferguson said that she had made a "gigantic error of judgement" in allowing Epstein to pay off a debt for her, and apologised for accepting money from him.
She nevertheless continued to defend Andrew's former friendship with Epstein.
Post-divorce

In 1999, Andrew was briefly in a relationship with Lady Victoria Hervey, who has since made a number of controversial statements in his support.
Residences

As Andrew and Ferguson shared custody of their two daughters, the family continued to live at Sunninghill Park, which had been built for the couple near Windsor Great Park in 1990, until Andrew moved to Royal Lodge in 2004.
In 2007, Ferguson moved into Dolphin House in Englefield Green, less than a mile from Royal Lodge.
A fire at Dolphin House in 2008 led her to move into Royal Lodge, once again sharing a home with Andrew.
Andrew's lease of Royal Lodge was for 75 years, held from the Crown Estate, with a single £1 million premium and a commitment to spend £7.5 million on refurbishment.
In March 2023, it was reported that Andrew had been offered Frogmore Cottage after his nephew Prince Harry was asked to vacate the residence.
The offer came amid reports that Andrew could no longer afford the running costs of Royal Lodge, as he was due to lose his annual grant.
In October 2025, it was reported that Andrew had paid a peppercorn rent for the Royal Lodge lease in exchange for upfront payments totalling £8.5 million, with the agreement entitling him and his family to reside at the property until 2078.
Later that month, Buckingham Palace announced that formal notice had been served to surrender the lease.
The Crown Estate later clarified that Andrew "will not be owed any compensation for early surrender of the lease ... once dilapidations are taken into account".
On 2 February 2026, Andrew left Royal Lodge and moved temporarily to Wood Farm on the Sandringham estate while his future accommodation underwent renovation.
Andrew is a keen skier, and in 2014 he bought a chalet in Verbier, Switzerland, for £13 million, jointly with his ex-wife.
Despite claims that the Queen would assist with the payment, a spokesperson for Andrew confirmed that she "will not be stepping in to settle the debt".
The Times reported in September 2021 that Andrew and Ferguson had reached a legal agreement with the chalet's previous owner and would sell the property.
The owner agreed to accept £3.4 million – half of what she was owed – after being informed that Andrew and Ferguson were experiencing financial difficulties.
Proceeds from the sale were reportedly intended to contribute to Andrew's legal expenses in relation to the civil lawsuit with Virginia Giuffre.
In June 2022, Le Temps reported that the chalet had been frozen because of a £1.6 million debt Andrew owed to unnamed individuals.
"


Health

On 2 June 2022, Andrew tested positive for COVID-19, and it was announced that he would not attend the Platinum Jubilee National Service of Thanksgiving at St Paul's Cathedral on 3 June.
Andrew is a teetotaller.
Interests

Andrew is a keen golfer and has held a low single-figure handicap.
In 2004, he was criticised by the Labour and Co-operative MP Ian Davidson, who, in a letter to the National Audit Office, questioned Andrew's decision to fly to St Andrews on RAF aircraft for two golfing trips.
Andrew resigned his honorary membership of the Royal and Ancient Golf Club of St Andrews after the Queen removed royal patronages at several golf clubs.
Charitable work

Patronages

Andrew was patron of the Middle East Association (MEA), the UK's premier organisation for promoting trade and good relations with the Middle East, North Africa, Turkey, and Iran.
Robert Jobson wrote that Andrew carried out this working effectively, noting that "He is particularly passionate when dealing with young start-up entrepreneurs and bringing them together with successful businesses at networking and showcasing events.
Andrew is direct and to the point, and his methods seem to work".
Andrew was patron of Fight for Sight, a charity dedicated to research into the prevention and treatment of blindness and eye disease, and was a member of the Scout Association.
Andrew toured Canada frequently to undertake duties related to his Canadian military role.
Rick Peters, former commanding officer of the Royal Highland Fusiliers of Canada, stated that Andrew was "very well informed on Canadian military methods".
On 3 September 2012, Andrew was among a team of 40 people who abseiled down The Shard, then the tallest building in Europe, to raise money for the educational charities the Outward Bound Trust and the Royal Marines Charitable Trust Fund.
In 2014, Andrew visited Geneva, Switzerland, to promote British science at CERN's 60th anniversary celebrations.
In 2013, it was announced that Andrew would become patron of London Metropolitan University and the University of Huddersfield.
On 19 November 2019, the Students' Union of the University of Huddersfield passed a motion to lobby Andrew to resign as its chancellor, while London Metropolitan University was also reviewing his role as patron.
On 21 November, Andrew relinquished his role as Chancellor of the University of Huddersfield.
In March 2019, Andrew took over the patronage of the Outward Bound Trust from his father, the Duke of Edinburgh, serving until his own resignation in November 2019.
Andrew had been chairman of the organisation's board of trustees since 1999.
In May 2019, it was announced that Andrew had succeeded Lord Carrington as patron of the Royal Fine Art Commission Trust.
On 13 January 2022, it was announced that his royal patronages had been returned to the Queen to be redistributed among other members of the royal family.
In January 2023, it was reported that King Charles III had agreed that Andrew could pursue some business interests.
In July 2025, the philanthropy adviser Giving Evidence published research examining the impact of Andrew's charity patronages on the incomes of the organisations he supported prior to his retirement from public duties.
The study found that revenues at roughly half of the 35 registered charities in England for which Andrew had been the sole royal patron rose after his patronage ended, while revenues at the other half fell.
Researchers then compared the 35 charities with others across the country and found "no material differences in revenue patterns when Andrew's patronages ceased".
Initiatives

While touring India as part of the Queen's Diamond Jubilee in 2012, Andrew became interested in the work of Women's Interlink Foundation (WIF), a charity that helps women acquire skills to earn an income.
In 2014, Andrew founded the Pitch@Palace initiative to support entrepreneurs by amplifying and accelerating their business ideas.
Entrepreneurs selected for Pitch@Palace Bootcamp were officially invited by Andrew to attend St James's Palace to pitch their ideas and connect with potential investors, mentors, and business contacts.
Amanda Thirsk became chief executive of Pitch@Palace in November 2019, following Andrew's withdrawal from royal duties.
In 2023, ownership of Knox House Trustees (UK) Limited was transferred to Andrew's accountant Arthur Lancaster.
Andrew founded the Prince Andrew Charitable Trust which aimed to support young people in different areas such as education and training.
He also established several awards, including the Inspiring Digital Enterprise Award (iDEA), a programme designed to develop digital and enterprise skills, the Duke of York Award for Technical Education, presented to talented young people in technical fields, and the Duke of York Young Entrepreneur Award, which recognised young entrepreneurial talent.
Andrew was additionally involved with the private limited company the Duke of York's Community Initiative (known as the Yorkshire Foundation between 2005 and 2011) and with a separate charity of a similar name, both of which supported voluntary organisations in Yorkshire.
Trade and commercial activities

Special Representative for International Trade and Investment

From 2001 to July 2011, Andrew worked with UK Trade & Investment, part of the Department for Business, Innovation and Skills, as the United Kingdom's Special Representative for International Trade and Investment.
The post, previously held by Prince Edward, Duke of Kent, involved representing and promoting the UK at trade fairs and conferences around the world.
Further criticism arose after Andrew hosted a lunch for Sakher El Materi, a member of the corrupt Tunisian regime, at Buckingham Palace around the time of the Tunisian Revolution.
Andrew also formed a friendship with Ilham Aliyev, the president of Azerbaijan, who has been criticised for corruption and human-rights abuses by Amnesty International, and visited him both during and after his tenure as the trade envoy.
As of November 2014, Andrew had met Aliyev on 12 occasions.
Reports indicated that Andrew maintained close ties with the Saudi royal family, which was deemed helpful to British trade interests, particularly in the defense sector.
Andrew did not receive a salary from the UK Trade & Investment for his role as Special Representative, but he travelled on expenses-paid delegations and was alleged to have occasionally used government-funded trips paid for personal leisure, earning him the nickname "Airmiles Andy" in the press.
On 8 March 2011, The Daily Telegraph reported: "In 2010, the Prince spent £620,000 as a trade envoy, including £154,000 on hotels, food and hospitality and £465,000 on travel."
In 2026, an anonymous former civil servant alleged that while trade envoy, Andrew used taxpayer money for "massage services".
Official documents relating to Andrew's business trips between 2001 and 2011 will not be released by the Foreign Office until 2065.
Alleged comments on corruption and Kazakhstan

As the United Kingdom's Special Trade Representative, Andrew travelled widely to promote British businesses.
The United States diplomatic cables leak revealed that Tatiana Gfoeller, the United States Ambassador to Kyrgyzstan, had reported Andrew discussing bribery in Kyrgyzstan and the investigation into the Al-Yamamah arms deal.
The dispatch continued: "His mother's subjects seated around the table roared their approval.
In May 2008, Andrew attended a goose-hunt in Kazakhstan with President Nursultan Nazarbayev.
In 2010, it emerged that the president's son-in-law, Timur Kulibayev, had paid Andrew's representatives £15 million – £3 million above the asking price – via offshore companies, for Andrew's Surrey mansion, Sunninghill Park.
The BBC further reported that the final payments associated with the alleged scheme occurred only weeks before contracts were exchanged for Sunninghill Park, raising questions about whether Andrew may have inadvertently benefited from the proceeds of crime, and whether appropriate due-diligence checks had been carried out.
It was later reported that Andrew's office had attempted to secure a crown estate property close to Kensington Palace for Kulibayev at the time.
In May 2012, Swiss and Italian police investigating "a network of personal and business relationships" allegedly used for "international corruption" examined the activities of Enviro Pacific Investments, which charged "multi-million pound fees" to energy companies seeking to operate in Kazakhstan.
A Palace spokesman responded: "This was a private sale between two trusts.
There was never any impropriety on the part of The Duke of York".
Libby Purves wrote in The Times in January 2015: "Prince Andrew dazzles easily when confronted with immense wealth and apparent power.
"


In May 2016, a further controversy arose when the Daily Mail alleged that Andrew had brokered a deal to assist a Greek and Swiss consortium in securing a £385-million contract to build water and sewerage networks in two of Kazakhstan's largest cities while serving as trade envoy, and that he stood to gain a £4-million commission.
The newspaper published an email from Andrew to Kazakh oligarch Kenges Rakishev – who had allegedly brokered the sale of Sunninghill Park – and reported that Rakishev had arranged meetings for the consortium.
After initially stating that the email was a forgery, Buckingham Palace sought to block its publication as a privacy breach.
The Palace denied that Andrew had acted as a "fixer" calling the article "untrue, defamatory and a breach of the editor's code of conduct".
Arms sales

During his tenure as the UK's Special Representative for International Trade and Investment, Andrew faced significant controversy regarding his role in fostering arms deals with Saudi Arabia, particularly in relation to alleged bribery and corruption involving BAE Systems.
In March 2011, Kaye Stearman of the Campaign Against the Arms Trade told Channel 4 News that the organisation viewed Andrew as part of a wider problem: "He is the front man for UKTI.
Our concerns are not just Prince Andrew, it's the whole UKTI set up.
We are concerned that Prince Andrew is used to sell arms, and where you sell arms it is likely to be to despotic regimes.
He is the cheerleader in chief for the arms industry, shaking hands and paving the way for the salesmen.
"


In January 2014, Andrew took part in a delegation to Bahrain, a close ally of the United Kingdom.
Andrew Smith, a spokesman for CAAT, said: "We are calling on Prince Andrew and the UK government to stop selling arms to Bahrain.
By endorsing the Bahraini dictatorship Prince Andrew is giving his implicit support to their oppressive practices.
Smith also stated: "The prince has consistently used his position to promote arms sales and boost some of the most unpleasant governments in the world, his arms sales haven't just given military support to corrupt and repressive regimes.
They've lent those regimes political and international legitimacy."


Promotion of Banque Havilland

In November 2020, following reviews of emails, internal documents, and unreported regulatory filings, as well as interviews with former bank insiders, Bloomberg Businessweek reported that Andrew had used his royal status and his role as trade envoy to assist David Rowland and his private bank, Banque Havilland, in securing clients around the world.
The Rowland family were among Andrew's investment advisers, and he attended the bank's official opening ceremony in July 2009.
In his email exchanges with Jeffrey Epstein in May 2010, Andrew described Rowland as his "trusted money man" although despite Andrew's encouragement for Epstein to invest in the Rowlands' venture he appeared to be reluctant.
In 2021, Bloomberg News reported that a firm connected to Rowland had been paying off Andrew's debts.
In November 2017, Andrew borrowed £250,000 from Banque Havilland, adding to an existing £1.25 million loan that had been "extended or increased 10 times" since 2015.
Eleven days later, in December 2017, £1.5 million was transferred from an account at Albany Reserves – controlled by the Rowland family – to Andrew's account at Banque Havilland, paying off the loan due in March 2018.
In February 2026, The Daily Telegraph reported that, in February 2010, while serving as the UK's trade envoy, Andrew forwarded a confidential Treasury briefing on the Icelandic financial crisis to Jonathan Rowland, the chief executive of Banque Havilland.
Relationship with alleged Chinese spy

In December 2024, it was reported that Andrew had invited Chris Yang, a Chinese businessman initially identified as "H6" in legal documents, to events at royal residences.
Yang had been authorised by a royal aide, Dominic Hampshire, to act on Andrew's behalf when dealing with potential investors in China.
Andrew ceased all contact with Yang following government concerns.
According to a 2025 report by The Telegraph, UK intelligence agencies deemed Andrew a potential national‐security risk because of his repeated meetings and close relationship with Yang, with concerns dating back to 2021 that his vulnerability and access could be exploited.
In 2025, it was reported that Andrew had met Cai Qi – who later became the first-ranked member of the Secretariat of the Chinese Communist Party (CCP) and de facto chief of staff to Xi Jinping – in London in 2018 and in Beijing in 2018 and 2019.
Andrew's subsequent meetings with Cai were connected to the expansion and launch of his Pitch@Palace business initiative in China.
Finances

Andrew received a £249,000 annuity from Queen Elizabeth II, which was reduced by King Charles III in April 2023.
The Sunday Times reported in July 2008 that, for "the Duke of York's public role ... he last year received £436,000 to cover his expenses".
In June 2019, Andrew arranged a private Buckingham Palace tour for Jay Bloom and Michael Evers, businessmen from the US cryptocurrency mining company Pegasus Group Holdings, which had agreed to pay his ex-wife up to £1.4 million for her role as a "brand ambassador".
Bloom and Evers were driven into the Palace in Andrew's car from their Knightsbridge hotel and later attended his Pitch@Palace event at St James's Palace before dining that evening with Andrew, Ferguson, and their daughter Beatrice.
Ferguson was promoting Pegasus's plan to use thousands of solar-powered generators to mine Bitcoin in Arizona, though the project collapsed after acquiring only 615 of the planned 16,000 units and generating just $33,779 (£25,000) in cryptocurrency.
Ferguson first met Bloom in Las Vegas in 2018, and he and Evers visited London frequently in 2019, meeting the York family on several occasions.
In October 2019, Ferguson signed a contract via Alphabet Capital, a British company owned by Adrian Gleave, through which she was paid more than £200,000 for Pegasus-related work.
Court documents showed that Andrew also received £60,500 traced to Gleave's businesses, though neither party explained the payments.
Several months after Andrew's controversial 2019 Newsnight interview, his private office established the Urramoor Trust, which owned both Lincelles (established 2020) and Urramoor Ltd (established 2013), and was, according to The Times, set up to support his family.
Andrew was described as a "settlor but not a beneficiary" and did not own either company, though Companies House listed him and his long-time private banker Harry Keogh as persons with "significant control".
In March 2022, it was reported that, on 15 November 2019, the wife of jailed former Turkish politician İlhan İşbilen had transferred £750,000 to Andrew in the belief that it would help her secure a passport.
The Telegraph reported that the payment had been described to the bankers "as a wedding gift" for his elder daughter, Beatrice, though court documents did not suggest that Beatrice was aware of the transaction.
İşbilen alleges that a further £350,000 was paid to Andrew through businessman Selman Turk, who she is suing for fraud.
Turk had received the People's Choice Award for his business Heyman AI at a Pitch@Palace event held at St James's Palace days before the £750,000 transfer.
In October 2025, it was reported that in December 2019 Andrew received £60,500 from Adrian Gleave, whose company Alphabet Capital Limited had also funneled money from Nebahat İşbilen to Andrew and Ferguson.
Court documents indicated that Alphabet Capital had made – and might continue to make – substantial payments to Andrew, despite being listed as a dormant company with minimal turnover.
Tarek Kaituni, a Libyan-born convicted gun smuggler, introduced Andrew to Selman Turk in May or June 2019 and met him on at least two occasions.
Kaituni, for whom Andrew had allegedly lobbied a British company, had reportedly given Beatrice an £18,000 gold and diamond necklace for her 21st birthday in 2009 and was invited to Eugenie's wedding in 2018.
Andrew also received "half" of £100,000 that Turk claimed was a payment to businessman Adrian Gleave to fund a search for "finding yoghurt production facilities in America".
In October 2025, The Guardian reported that Andrew was set to receive a one-off six-figure payment from the King's private funds to help finance his move from Royal Lodge to a smaller property on the Sandringham estate.
Epstein scandal

Jeffrey Epstein and related associations

Andrew was a friend of Jeffrey Epstein, an American financier who pleaded guilty in 2008 to soliciting prostitution from a person under the age of 18.
In December 2010, Andrew was photographed walking with Epstein in Central Park during a visit to New York City.
In July 2011, Andrew's role as trade envoy was terminated, amid escalating controversy over his associations, particularly with Epstein.
In 2011, Virginia Giuffre, a prominent accuser of Epstein, told the Daily Mail that she had never had sexual contact with the then-Prince Andrew, but she later alleged that Epstein trafficked her to Andrew on several occasions.
It has been alleged that Andrew "pulled strings" to enable Epstein to use the RAF base.
On 30 December 2014, a court filing in Florida by the lawyers Bradley J. Edwards and Paul G. Cassell alleged that Andrew was among several prominent figures, including lawyer Alan Dershowitz and "a former prime minister", who had participated in sexual activities with a minor later identified as Virginia Giuffre (then known by her maiden name, Virginia Roberts), who was allegedly trafficked by Epstein.
In January 2015, there was renewed media and public pressure for Buckingham Palace to explain Andrew's connection with Epstein.
The Palace stated that "any suggestion of impropriety with underage minors is categorically untrue", and later repeated the denial.
Giuffre stated that she had sex with Andrew on three occasions, including during a trip to London in 2001 when she was 17, and later in New York and on Little Saint James in the US Virgin Islands during an orgy.
She alleged that Epstein paid her $15,000 after she had sex with Andrew in London.
Flight logs place Andrew and Giuffre in the locations where she said their meetings occurred.
Andrew and Giuffre were also photographed together, with his arm around her waist and Ghislaine Maxwell in the background, though Andrew's supporters have repeatedly claimed the image is fake or edited.
An email sent by "G Maxwell" to Epstein in 2015, released as part of the Epstein files, appears to confirm that a photograph had been taken, stating: "In 2001 I was in London when  met a number of friends of mine including Prince Andrew.
"


In August 2019, court documents associated with the defamation case between Giuffre and Maxwell revealed that a second woman, Johanna Sjoberg, alleged that Andrew had placed his hand on her breast while posing for a photo with his Spitting Image puppet in Epstein's mansion.
In January 2026, another Epstein victim alleged, through her lawyer Bradley J. Edwards, that she had been sent to the UK for a sexual encounter with Andrew at Royal Lodge in 2010, when she was in her twenties.
Her lawyer also said that she was subsequently shown around Buckingham Palace and served tea.
The letter alleged that in 2006, an unnamed exotic dancer was hired for $10,000 to perform at Epstein's Florida home for him and Andrew and was then propositioned for a threesome.
Newsnight interview

In November 2019, the BBC's Newsnight broadcast an interview between Andrew and presenter Emily Maitlis, in which he discussed his friendship with Epstein publicly for the first time.
Andrew said he met Epstein in 1999 through Maxwell, contradicting comments made by his private secretary in 2011 that the two met in "the early 1990s".
In the interview, Andrew denied having sex with Giuffre on 10 March 2001, as she alleged, saying he had been at home with his daughters after attending a party at a PizzaExpress branch in Woking with his elder daughter, Beatrice.
The interview was believed by Maitlis and the Newsnight team to have been approved by the Queen, though "palace insiders" quoted by The Sunday Telegraph disputed this.
Although Andrew was reportedly pleased with the outcome – giving Maitlis and the Newsnight team a tour of Buckingham Palace – the interview received overwhelmingly negative reactions from the media and the public.
It was described as a "car crash", "nuclear explosion level bad", and the worst public-relations crisis for the royal family since the death of Diana, Princess of Wales.
Lawsuit

In August 2021, Giuffre sued Andrew in the federal District Court for the Southern District of New York, accusing him of "sexual assault and intentional infliction of emotional distress".
On 29 October 2021, Andrew's lawyers filed a response stating that he "unequivocally denies Giuffre's false allegations".
On 12 January 2022, Judge Kaplan rejected Andrew's attempts to dismiss the case, allowing the lawsuit to proceed.
In February, the case was settled out of court, with Andrew making a donation to Giuffre's charity for victims of abuse, without any admission of liability.
Repercussions

On 20 November 2019, Buckingham Palace announced that Andrew was suspending his public duties "for the foreseeable future".
The decision, made with the Queen's consent, was accompanied by an insistence that Andrew sympathised with Epstein's victims.
On 24 November, the palace confirmed that Andrew would step down from all 230 of his patronages.
The scrutiny of Andrew's relationship with Epstein also led to scrutiny of other public figures' ties to Epstein, notably the relationship of Mette-Marit, Crown Princess of Norway, and Epstein.
In March 2020, Andrew hired Mark Gallagher, a crisis-management expert who had assisted high-profile clients falsely accused during Operation Midland.
In May 2020, it was announced that Andrew would permanently resign from all public roles due to his ties to Epstein.
In January 2022, Andrew's social-media accounts were deleted, his page on the royal family's website was rewritten in the past tense, and his military affiliations and patronages were removed to emphasise his withdrawal from public life.
In June 2022, Rachael Maskell, Labour MP for York Central, introduced a 'Removal of Titles' private members bill in the House of Commons, which would have enabled the monarch or a parliamentary committee to strip aristocratic titles from individuals deemed unworthy.
In March 2022, Andrew made his first public appearance in months, helping the Queen walk into Westminster Abbey for a memorial service for his father, the Duke of Edinburgh.
In June 2022, Andrew took part in the private elements of the Garter Day ceremony, including lunch and the investiture of new members, but was excluded from the public procession amid reports that his brother Charles and nephew William had intervened to prevent him appearing in view of the public.
Following the death of Queen Elizabeth II on 8 September 2022, Andrew appeared in civilian clothing at various ceremonial events.
He wore military uniform for a 15-minute vigil beside the Queen's coffin at Westminster Hall on 16 September.
In October 2022, it was reported that Andrew no longer received government funding.
The following month, it was also reported that he was set to lose his police protection, as he was no longer expected to undertake public duties in line with King Charles's wishes.
In January 2023, it was reported that Andrew could no longer use his suite of rooms at Buckingham Palace.
In August 2024, The Telegraph reported that Charles would withdraw funding for Andrew's security by the end of October, requiring him to pay for future security operations at Royal Lodge.
On 2 November 2025, Defence Secretary John Healey confirmed that Andrew's honorary rank of vice-admiral – retained after he relinquished his other military titles in 2022 – would be removed following direction from Charles III, a process finalised by 13 December.
On 3 November, letters patent were issued removing Andrew's style of "Royal Highness" and the title "prince"; without these honorifics, it was agreed that he would use the family surname Mountbatten-Windsor.
His appointments to the Royal Victorian Order and Order of the Garter were also rescinded, and his banner was removed from St George's Chapel, Windsor Castle, the chapel of the Order of the Garter.
Later that month, Andrew's life membership of the Savage Club was withdrawn.
Commemorative plaques bearing his name were removed from several locations in the Falkland Islands, and Mid and East Antrim Council agreed to rename Prince Andrew Way in Carrickfergus.
On 19 November, Metropolitan Police firearms-licensing officers requested that Andrew voluntarily surrender his firearms and shotgun certificate, which he did.
Misconduct in public office

Emails disclosed as part of the Epstein files in early 2026 appear to indicate that, between 2010 and 2011, Andrew may have knowingly shared confidential information with Epstein about his official work as trade envoy; trade envoys have a duty of confidentiality over sensitive, commercial, or political information arising from their official visits.
It is further alleged that in 2010, Andrew passed on an email conversation about the Royal Bank of Scotland and Aston Martin to Terence Allen and David Stern.
In February 2026, Thames Valley Police stated that they were considering investigating Republic's report concerning Andrew for suspected misconduct in public office and an alleged breach of official secrets.
Arrest

On the morning of 19 February 2026, his 66th birthday, Andrew was arrested on suspicion of misconduct in public office at the Sandringham estate, where he had been living since leaving his home in Windsor.
It was the first arrest of a senior member of the British royal family since that of King Charles I in 1647, and the first arrest of a sibling of the reigning monarch since that of Elizabeth I in 1554.
Thames Valley Police stated that they were searching addresses in Berkshire and Norfolk, and it was subsequently confirmed that officers were searching Royal Lodge in Windsor Great Park, where Andrew previously lived.
Charles III released a statement expressing his "deepest concern", and said that "the law must take its course".
Andrew was released from Aylsham police station later that day, around 11 hours after his arrest, under investigation.
Investigation

Metropolitan Police officials have sought the cooperation of the United States Department of Justice in relation to the investigation into Andrew.
Sir Mark Rowley, Commissioner of the Metropolitan Police, said that the force is assessing a "whole range of sexual allegations" concerning Andrew to determine whether they "merit a criminal investigation".
Reuters photograph

A Reuters photograph by Phil Noble, showing what BBC News described as a "shell-shocked, haunted" Andrew slumping in his car as he left the police station, attracted international attention.
The image was briefly hung at the Louvre by activists from Everyone Hates Elon under the title He's Sweating Now – a reference to Andrew's widely publicised claim in his 2019 Newsnight interview that he had been unable to sweat at the time of the alleged events –  before being removed by museum staff after approximately 15 minutes.
Other allegations

Racist language

Rohan Silva, a former Downing Street aide, claimed that, when they met in 2012, Andrew had commented, "Well, if you'll pardon the expression, that really is the nigger in the woodpile."
The former home secretary Jacqui Smith claimed that Andrew made a racist comment about Arabs during a state dinner for the Saudi royal family in 2007.
Buckingham Palace denied that Andrew had used racist language on either occasion.
Treatment of others

During his four-day tour of Southern California in 1984, Andrew squirted paint at American and British journalists and photographers who were reporting on the visit, after which he told Los Angeles county supervisor Kenneth Hahn, "I enjoyed that."
A senior footman once told a reporter who worked undercover at Buckingham Palace that on waking Andrew "the response can easily be 'fuck off' as 'good morning'".
Former royal protection officer Paul Page, who himself was convicted and given a six-year prison sentence following a £3 million property investment scam in 2009, said in an ITV documentary that Andrew kept a collection of "50 or 60 stuffed toys" and would "shout and scream and become verbally abusive" if they "weren't put back in the right order by the maids".
Page later alleged in the documentary Prince Andrew:
Banished that different women visited Andrew daily, and that when one was denied entry by security, Andrew allegedly called an officer a "fat, lardy cunt" over the phone.
Page said of Andrew: "He's a bully."


Andrew's former maid, Charlotte Briggs, also recalled arranging the teddy bears on his bed and told The Sun that when she was bitten by his Norfolk Terrier in 1996 he "wasn't bothered".
Briggs said that a butler later told her that Andrew and his personal doctor "laughed" about the incident.
Andrew's dog was subsequently banned from Buckingham Palace.
Briggs said she had been reduced to tears after being reprimanded for not properly closing the heavy curtains in his office, adding that his behaviour contrasted with that of his brothers Charles and Edward, who "weren't anything like him" and his father Philip, whom she described as "so nice and gentlemanly".
Emma Gruenbaum, a massage therapist, told The Sun that Andrew regularly overstepped boundaries, making sexual comments during appointments.
Gruenbaum said Andrew arranged regular massages for around two months, and she believed the requests stopped when he realised he would not get more.
In 2025, Andrew Lownie alleged in his book Entitled: The Rise and Fall of the House of York that Andrew reprimanded a palace employee for not using the proper name and title when referring to his grandmother Queen Elizabeth the Queen Mother, calling him a "fucking imbecile".
Another employee alleged that Andrew would "explode one minute and then try to take it back the next".
Biographer Robert Hardman alleged in Elizabeth II: In Private.
The Inside Story that Andrew had struck the Master of the Household, Tony Johnstone-Burt, during a dispute over room availability for one of Andrew's events, and that the incident led to Prince Philip sending Johnstone‐Burt a letter of apology.
Andrew was also alleged to have damaged sensor-operated gates in Windsor Great Park by forcing them open in his Range Rover to avoid going an extra mile on his way home.
In March 2016, the Thames Valley Police dismissed the formal report by the Republic due to lack of details.
Titles, styles, honours and arms

Titles and styles


As a son of the reigning monarch, he was styled at birth as "His Royal Highness The Prince Andrew".
On 23 July 1986, the day of his wedding, he was created Duke of York, Earl of Inverness, and Baron Killyleagh, and assumed the style "His Royal Highness The Duke of York".
He was occasionally known as Earl of Inverness in Scotland and Baron Killyleagh in Northern Ireland.
In 2019, in light of Andrew's friendship with the convicted sex offender Epstein, residents of Inverness began a campaign to strip him of his earldom, saying that "it is inappropriate that Prince Andrew is associated with our beautiful city".
Rachael Maskell, the Labour Co-op MP for York Central, said she would seek ways to make Andrew give up his dukedom if he did not do so voluntarily; the City of York Council removed his honorary freedom of the city by a unanimous vote, and several York councillors called for him to lose the title Duke of York.
In January 2022, Andrew ceased using the style "Royal Highness" in a public capacity, though he remained permitted to use it privately.
2025 changes

On 17 October 2025, following discussions with King Charles III, Andrew agreed to cease using his peerages and honours, including his dukedom and his knighthoods as a Royal Knight Companion of the Order of the Garter and a Knight Grand Cross of the Royal Victorian Order.
His banner of arms, which had hung in St George's Chapel, Windsor Castle, since 2006 to signify his membership of the Order of the Garter, was removed.
On 30 October, Buckingham Palace announced that the King had begun a "formal process" to remove his brother's style, titles, and honours.
Andrew's name was removed from the Roll of the Peerage the same day.
Although this did not revoke his peerages, it meant he was no longer entitled to any place in the orders of precedence in the United Kingdom derived from them, and ceased to be addressed or referred to by any title derived from his peerages in official documents.
On 3 November, letters patent were issued that removed the style "Royal Highness" and the title "prince" from Andrew, and on 1 December, a notice, backdated to 30 October, was published in The London Gazette, stating that his appointments to the Order of the Garter and Royal Victorian Order had been annulled.
He is to use the surname "Mountbatten-Windsor", in accordance with the 1960 Privy Council declaration on the family surname by Queen Elizabeth II.
On 13 December, the Ministry of Defence announced that the Defence Council of the United Kingdom had removed Andrew's honorary rank of vice-admiral, whereupon he reverted to the rank of commander (retired).
2026

Andrew remains eighth in the line of succession to the British throne as of 2026.
The UK government has indicated that it is considering legislation to remove him from the line of succession, a step that would require the consent of all Commonwealth realms.
Andrew also holds the position of Counsellor of State, although it is unlikely he would be called upon to exercise any royal functions in that capacity because he is no longer a working member of the royal family; he would automatically cease to hold the role if removed from the line of succession.
Naval ranks

Honours

Commonwealth

Foreign

Appointments

Freedom of the City

Former honorary military appointments

In 2019, Andrew's military affiliations were suspended and on 13 January 2022 they were formally returned to Queen Elizabeth II.
Canada


 New Zealand


 United Kingdom


Arms

Depictions

Andrew was portrayed by Rufus Sewell in the 2024 Netflix drama film Scoop, which depicts the 2019 BBC Newsnight interview "Prince Andrew & the Epstein Scandal".
Andrew was portrayed by Tom Byrne in the fourth season, and by James Murray in the final two seasons, of Netflix's The Crown.



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
  AssignClass (ce0318e0-4cbb-4db7-9c9f-e1082e5b5ae2)
 Call ID: ce0318e0-4cbb-4db7-9c9f-e1082e5b5ae2
  Args:
    source: :Andrew_Mountbatten-Windsor
    type: :Man
  AssignClass (09da5460-8c00-4a97-8caf-2ac6e0d217bb)
 Call ID: 09da5460-8c00-4a97-8caf-2ac6e0d217bb
  Args:
    source: :Andrew_Mountbatten-Windsor
    type: :Person
  AssignClass (6b247910-72fd-41ab-9492-4cfd92a56c59)
 Call ID: 6b247910-72fd-41ab-9492-4cfd92a56c59
  Args:
    source: :Queen_Elizabeth_II
    type: :Woman
  AssignClass (c9ac576d-79c0-4a1b-82c8-d4ef9f8e6e07)
 Call ID: c9ac576d-79c0-4a1b-82c8-d4ef9f8e6e07
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AssignClass (34c4e6ba-e53a-4d42-b9aa-2edc23aeff18)
 Call ID: 34c4e6ba-e53a-4d42-b9aa-2edc23aeff18
  Args:
    type: :Man
    source: :Prince_Philip
  AssignClass (aaffdcd2-4df7-4cf7-ab9e-795a997e01d7)
 Call ID: aaffdcd2-4df7-4cf7-ab9e-795a997e01d7
  Args:
    type: :Person
    source: :Prince_Philip
  AssignClass (7504d509-38fb-4f66-a450-ad6e38084362)
 Call ID: 7504d509-38fb-4f66-a450-ad6e38084362
  Args:
    type: :Man
    source: :King_Charles_III
  AssignClass (d5f47eda-2294-4d57-b0c7-79d66a3c1959)
 Call ID: d5f47eda-2294-4d57-b0c7-79d66a3c1959
  Args:
    type: :Person
    source: :King_Charles_III
  AssignClass (210e9a92-2b02-4ef2-aa3e-7b1e2d890e38)
 Call ID: 210e9a92-2b02-4ef2-aa3e-7b1e2d890e38
  Args:
    type: :Woman
    source: :Sarah_Ferguson
  AssignClass (ff101b88-079f-404e-badd-718b1f402ac1)
 Call ID: ff101b88-079f-404e-badd-718b1f402ac1
  Args:
    type: :Person
    source: :Sarah_Ferguson
  AssignClass (1423f6b4-3ee9-4807-be27-36aa6a09ab23)
 Call ID: 1423f6b4-3ee9-4807-be27-36aa6a09ab23
  Args:
    source: :Princess_Beatrice
    type: :Woman
  AssignClass (87d53db1-6627-448d-9285-1f17073027de)
 Call ID: 87d53db1-6627-448d-9285-1f17073027de
  Args:
    source: :Princess_Beatrice
    type: :Person
  AssignClass (00f2c76d-94a9-42d2-b8e1-97a4da1ed8dc)
 Call ID: 00f2c76d-94a9-42d2-b8e1-97a4da1ed8dc
  Args:
    type: :Woman
    source: :Princess_Eugenie
  AssignClass (5dc5d54a-e887-48ec-9399-c8145b7fc3d7)
 Call ID: 5dc5d54a-e887-48ec-9399-c8145b7fc3d7
  Args:
    source: :Princess_Eugenie
    type: :Person
  AddLiteral (fc5fdd0c-2d46-4b7a-8da5-f6c60304b3cd)
 Call ID: fc5fdd0c-2d46-4b7a-8da5-f6c60304b3cd
  Args:
    relation: :hasBirthYear
    literal_value: 1960
    literal_type: xsd:integer
    source: :Andrew_Mountbatten-Windsor
  AddTriple (f2bc5799-070a-42fa-a27b-7211d1536ad0)
 Call ID: f2bc5799-070a-42fa-a27b-7211d1536ad0
  Args:
    relation: :hasFather
    source: :Andrew_Mountbatten-Windsor
    target: :Prince_Philip
  AddTriple (8db32cca-1a42-4736-ae54-28cc7fabe685)
 Call ID: 8db32cca-1a42-4736-ae54-28cc7fabe685
  Args:
    relation: :hasMother
    source: :Andrew_Mountbatten-Windsor
    target: :Queen_Elizabeth_II
  AddTriple (56e6cfb0-6b74-4420-a895-7c65c197b28b)
 Call ID: 56e6cfb0-6b74-4420-a895-7c65c197b28b
  Args:
    relation: :isBrotherOf
    target: :King_Charles_III
    source: :Andrew_Mountbatten-Windsor
  AddLiteral (1b19747e-f5e9-423c-99a9-296fc796022c)
 Call ID: 1b19747e-f5e9-423c-99a9-296fc796022c
  Args:
    relation: :hasMarriageYear
    source: :Andrew_Mountbatten-Windsor
    literal_type: xsd:integer
    literal_value: 1986
  AddTriple (3ab99e9f-4f28-4d34-bed7-9322fc526424)
 Call ID: 3ab99e9f-4f28-4d34-bed7-9322fc526424
  Args:
    source: :Andrew_Mountbatten-Windsor
    target: :Sarah_Ferguson
    relation: :hasRelation
  AddTriple (c82602c0-ad31-4fd0-b1a8-ffd8e214f2c1)
 Call ID: c82602c0-ad31-4fd0-b1a8-ffd8e214f2c1
  Args:
    target: :Princess_Beatrice
    source: :Andrew_Mountbatten-Windsor
    relation: :isFatherOf
  AddTriple (3d8a4dfb-925e-40bf-8ce2-07eb10cd46fd)
 Call ID: 3d8a4dfb-925e-40bf-8ce2-07eb10cd46fd
  Args:
    relation: :isFatherOf
    source: :Andrew_Mountbatten-Windsor
    target: :Princess_Eugenie
  AddTriple (29223343-76c7-4ffa-8905-6ac6374dc02e)
 Call ID: 29223343-76c7-4ffa-8905-6ac6374dc02e
  Args:
    target: :Princess_Beatrice
    source: :Sarah_Ferguson
    relation: :isMotherOf
  AddTriple (e2b8bb95-3ff3-4d41-9c06-e081d6350484)
 Call ID: e2b8bb95-3ff3-4d41-9c06-e081d6350484
  Args:
    relation: :isMotherOf
    target: :Princess_Eugenie
    source: :Sarah_Ferguson
  Finish (12af4cb9-bf32-458c-a6f2-14c575a2c1cc)
 Call ID: 12af4cb9-bf32-458c-a6f2-14c575a2c1cc
  Args: