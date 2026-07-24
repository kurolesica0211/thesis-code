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
Prince Harry, Duke of Sussex (Henry Charles Albert David; born 15 September 1984) is a member of the British royal family.
He is the younger son of King Charles III and Diana, Princess of Wales, and is fifth in the line of succession to the British throne.
Harry was educated at Wetherby School, Ludgrove School, and Eton College, before completing officer training at the Royal Military Academy Sandhurst.
He was commissioned as a cornet in the Blues and Royals and served briefly alongside his elder brother, William, Prince of Wales.
He was deployed twice on active service in Afghanistan: for ten weeks in Helmand Province during 2007–2008, and for twenty weeks with the Army Air Corps in 2012–2013.
Inspired by the Warrior Games in the United States, Harry founded the Invictus Games in 2014 and remains actively involved as its patron.
In 2016, together with his brother William and sister-in-law Catherine, Princess of Wales, he co-founded the mental health awareness initiative Heads Together.
In 2018, Harry was created Duke of Sussex ahead of his wedding to American actress Meghan Markle.
In January 2020, Harry and Meghan stepped back from their roles as working members of the royal family and relocated to Southern California.
In March 2021, Harry and Meghan gave a widely publicised interview to Oprah Winfrey on Oprah with Meghan and Harry.
In December 2022, they appeared in the Netflix documentary series Harry & Meghan.
In 2023, Harry published his memoir, Spare.
Early life

Harry was born at 4:20 pm on 15 September 1984 at St Mary's Hospital, London, during the reign of his paternal grandmother, Queen Elizabeth II.
He was the second child of Charles, Prince of Wales (later King Charles III), and his first wife, Diana, Princess of Wales.
He was christened Henry Charles Albert David on 21 December at St George's Chapel, Windsor Castle, by Robert Runcie, the then archbishop of Canterbury.
From childhood he was known as "Harry" to family, friends, and the public, and was nicknamed "Harold" by his elder brother, William.
Harry and William were raised at Kensington Palace in London, and at Highgrove House in Gloucestershire.
Diana sought to give her sons a broader range of experiences and a clearer understanding of ordinary life than previous generations of royal children.
Harry began accompanying his parents on official visits at an early age; his first overseas tour was to Italy in 1985.
Harry's parents divorced in 1996.
The following year,  his mother died in a car crash in Paris while he and William were staying with their father at Balmoral Castle.
Charles informed his sons of her death.
At Diana's funeral, Harry, then aged 12, walked behind the cortège from Kensington Palace to Westminster Abbey alongside his father, his brother, his paternal grandfather Prince Philip, Duke of Edinburgh, and his maternal uncle Charles Spencer, 9th Earl Spencer.
Harry and William inherited the "bulk" of the £12.9 million left by their mother on their 30th birthdays, a sum that had increased to about £10 million each by 2014.
In the same year, they inherited Diana's wedding dress and many of her personal possessions, including dresses, diamond tiaras, jewellery, letters, and paintings.
They also received the original lyrics and score of "Candle in the Wind", by Bernie Taupin and Elton John, as performed by John at Diana's funeral.
In 2002, The Times reported that Harry would share with his brother a disbursement of £4.9 million from trust funds established by their great-grandmother, Queen Elizabeth the Queen Mother, on their 21st birthdays, and a further £8 million on their 40th birthdays.
It was also reported that Harry would inherit the larger share of the money left by the Queen Mother for the two brothers, as William is expected to ascend the throne and receive additional financial benefits.
Education

Like his father and brother, Harry was educated at private schools.
The decision to place him at Eton departed from the past practice of the Mountbatten-Windsors, who traditionally sent their children to Gordonstoun, which his grandfather, father, two uncles, and two cousins had attended.
It did, however, see Harry follow in his brother's footsteps and the Spencer family tradition, as both his maternal grandfather and his maternal uncle attended Eton.
As with William, the royal family and the tabloid press agreed that Harry would be allowed to study free from intrusion in exchange for occasional photograph opportunities, in what became known as the "pressure cooker agreement".
In June 2003, Harry completed his education at Eton with two A-Levels, achieving a grade B in art and a D in geography, having decided to drop history of art after AS level.
Both Eton and Harry denied the allegations.
A tribunal made no ruling on the cheating claim, but it "accepted the prince had received help in preparing his A-level 'expressive' project, which he needed to pass to secure his place at Sandhurst."
While at Eton, Harry joined the Combined Cadet Force and was made cadet officer in his final year, leading the corps' annual parade at the Eton tattoo.
After leaving school, Harry took a gap year, during which he spent time in Australia working as a jackaroo on a cattle station and taking part in the Young England vs Young Australia Polo Test match.
He also travelled to Lesotho, where he worked with orphaned children and produced the documentary film The Forgotten Kingdom: Prince Harry in Lesotho.
Military career

Sandhurst; Blues and Royals; deployment to Afghanistan

Harry passed the Regular Commissions Board (RCB) in September 2004 and entered the Royal Military Academy Sandhurst on 8 May 2005, where he was known as Officer Cadet Wales and joined Alamein Company.
In 2006, it was announced that Harry's unit was scheduled to be deployed to Iraq the following year.
In April 2006, the Ministry of Defence stated that Harry would be shielded from the front line if his unit went to war, with a spokeswoman noting that he was expected to "undertake the fullest range of deployments", but that his role required monitoring because "his overt presence might attract additional attention" that could endanger him or those he commanded.
Defence Secretary John Reid argued that he should be allowed to serve on the front line.
Harry agreed, saying, "If they said 'no, you can't go front line'
Harry completed the Troop Leaders' Course in October 2006 and rejoined his regiment in Windsor, where he was put in charge of a troop of 11 soldiers and four Scimitar reconnaissance vehicles.
On 22 February 2007, the Ministry of Defence and Clarence House jointly announced that Harry would be deployed with his regiment to Iraq as part of the 1st Mechanised Brigade of the 3rd Mechanised Division – a move supported by Harry, who had said he would leave the army if ordered to remain in safety while his regiment went to war.
General Sir Richard Dannatt, the head of the British Army said on 30 April 2007 that he had personally decided Harry would serve with his unit in Iraq as a troop commander, and he was scheduled for deployment in May or June 2007 to patrol the Maysan Governorate.
By 16 May, however, Dannatt announced that Harry would not serve in Iraq; concerns included his status as a high-value target – several threats had already been made against him – and the risks this posed to the soldiers around him should any attempt be made on his life or if he were captured.
Clarence House made public Harry's disappointment with the decision, though he said he would abide by it.
In the summer of 2007 Harry trained as a joint terminal attack controller at RAF Leeming.
This was confirmed in February 2008 when the Ministry of Defence revealed that Harry had been secretly deployed as a joint terminal attack controller to Helmand Province in Afghanistan for the previous ten weeks.
Harry returned on a flight carrying servicemen injured by an IED, including Ben McBean.
It was later reported that Harry had helped Gurkha troops repel an attack by Taliban insurgents, and had carried out patrol duties in hostile areas while in Afghanistan.
Harry's tour made him the first member of the British royal family to serve in a war zone since his uncle Prince Andrew, who flew helicopters during the Falklands War.
For Harry's service, his aunt Princess Anne presented him with the Operational Service Medal for Afghanistan at Combermere Barracks in May 2008.
Army Air Corps and second deployment to Afghanistan

In October 2008, it was announced that Harry would follow his brother, father, and uncle, in learning to fly military helicopters.
Harry initially failed his pilot's theory test in February 2009.
Prince Charles presented him with his flying brevet (wings) on 7 May 2010 at a ceremony at the Army Air Corps Base (AAC) at Middle Wallop.
Harry was awarded his Apache Flying Badge on 14 April 2011.
In June 2011, Clarence House announced that Harry would be available for deployment in current operations in Afghanistan as an Apache helicopter pilot.
The final decision rested with the Ministry of Defence's senior commanders, principally the Chief of the Defence Staff, in consultation with the wishes of Harry, the Prince of Wales, and the Queen.
In October 2011, Harry was transferred to a United States military base in California to complete his helicopter gunship training.
This final phase included live-fire training and "environmental and judgment training" at naval and air force facilities in California and Arizona.
While training in Southern California, Harry also spent time in San Diego.
On 7 September 2012, Harry arrived at Camp Bastion in southern Afghanistan as part of the 100-strong 662 Squadron, 3 Regiment, Army Air Corps, to begin a four-month combat tour as a co-pilot and gunner for an Apache helicopter.
On 10 September, within days of his arrival, it was reported that the Taliban had threatened his life.
On 18 September, Harry was moved to a safe location after a Taliban attack on Camp Bastion that killed two US marines.
Defence Secretary Philip Hammond stated that "additional security arrangements" had been put in place because Harry could be a potential target, but added that he would face "the same risk as any other Apache pilot" while in combat.
He came and went, and you never would have known he was there" and, "The only thing special we did for him was we had a place identified as a safe house in case the base came under attack."
On 21 January 2013, it was announced that Harry was returning from a 20-week deployment in Afghanistan.
Harry compared operating the Apache's weapons systems in Afghanistan to playing video games.
Harry later revealed in his 2023 memoir Spare that he flew on six missions that resulted in him killing 25 Taliban members, writing that he felt he had been trained not to view them as "people" but as "chess pieces" removed from the board.
Following the publication of Harry's claims, Pen Farthing, a British former Royal Marines commando and founder of the Nowzad Dogs charity, was evacuated from Kabul on 6 January 2023 to avoid "potential reprisal attacks on ex-forces people".
Harry's revelations prompted criticism from Taliban members, British politicians, and military figures.
On 17 January 2014, the Ministry of Defence announced that Harry had completed his attachment to 3 Regiment Army Air Corps and would take up a staff officer role, SO3 (Defence Engagement), in HQ London District.
On 6 March 2014, Harry launched Invictus Games, a Paralympic-style sporting event for injured servicemen and women, which was held from 10 to 14 September 2014.
On 15 May 2014, Harry attended a ticket-sale launch for the Invictus Games at the BT Tower, from where he tweeted on the Games' official Twitter account as its president.
Harry later wrote an article in The Sunday Times about his experiences in Afghanistan, explaining how they had inspired him to support injured personnel and how, after attending the Warrior Games, he had vowed to create the Invictus Games.
Harry and officials attended the British Armed Forces Team announcement for the Games at Potters Field Park in August 2014.
In January 2015, it was reported that Harry would take on a new role supporting wounded service personnel by working alongside members of the London District's Personal Recovery Unit for the MOD's Defence Recovery Capability scheme, ensuring that wounded personnel had adequate recovery plans.
The palace confirmed weeks later that the scheme had been established in partnership with Help for Heroes and the Royal British Legion.
In late January 2015, Harry visited The Battle Back Centre set up by the Royal British Legion, and Fisher House UK at the Queen Elizabeth Hospital Birmingham.
The Centre was created through a partnership between Help for Heroes, the Fisher House Foundation, and the Queen Elizabeth Hospital Birmingham (QEHB) Charity.
In February and March 2015, Harry visited Phoenix House in Catterick Garrison, North Yorkshire, a recovery centre run by Help for Heroes.
He also visited Merville Barracks in Colchester, where Chavasse VC House Personnel Recovery Centre is located, run by Help for Heroes in partnership with the Ministry of Defence and Royal British Legion.
Secondment to Australian Defence Force

On 17 March 2015, Kensington Palace announced that Harry would leave the Armed Forces in June.
On 6 April 2015, Harry reported for duty to Australia's Chief of the Defence Force, Air Chief Marshal Mark Binskin, at the Royal Military College, Duntroon, in Canberra.
Harry flew to Darwin later that day to begin his month-long secondment to the ADF's 1st Brigade.
He also joined SASR for live-fire shooting exercises with numerous Special Forces weapons at a variety of ranges.
Harry completed an insertion-training exercise using a rigid-hull inflatable boat.
He also spent time flying over Sydney as co-pilot of an Army Black Hawk helicopter and participated in counter-terrorism training in Sydney Harbour with Royal Australian Navy clearance divers.
Harry's attachment with the ADF ended on 8 May 2015, and on 19 June 2015 he resigned his short service commission.
Post-military service

In 2021, Harry described his 10 years (2005–2015) in the army as "the happiest times in my life".
On 19 December 2017, he succeeded his grandfather Prince Philip as Captain General Royal Marines.
In May 2018, he was promoted to the substantive ranks of Lieutenant Commander in the Royal Navy, Major of the British Army, and Squadron Leader in the Royal Air Force.
On 18 January 2020, Buckingham Palace announced that an agreement had been reached for Harry "to step back from Royal duties, including official military appointments".
In February 2021, the Palace confirmed that the Duke would give up his position as Captain General Royal Marines and relinquish all his other honorary military appointments.
In January 2026, Harry said that the sacrifices of NATO troops in Afghanistan must be spoken about "truthfully and with respect", emphasising that allied forces had fought on the front lines and had paid a heavy price.
Personal life

Bachelorhood

Chelsy Davy, the daughter of Zimbabwean-born, South Africa-based businessman Charles Davy, was referred to as Harry's girlfriend in an interview conducted for his 21st birthday.
Harry said he "would love to tell everyone how amazing she is but once I start talking about that, I have left myself open....
Davy was present when Harry received his Operational Service Medal for Afghanistan and also attended his graduation ceremony when he received his flying wings from his father.
In his 2023 memoir, Harry states that months after breaking up with Davy he was introduced to Caroline Flack, whom he described as "funny", "sweet", and "cool".
The two saw each other for a while before press intrusion "tainted" their relationship "irredeemably", according to Harry.
In May 2012, Harry's cousin Princess Eugenie introduced him to Cressida Bonas, an actress and model who is the granddaughter of Edward Curzon, 6th Earl Howe.
Marriage and family

In mid-2016, Harry began a relationship with American actress Meghan Markle.
On 8 November, eight days after the relationship was made public by the press, Harry directed his communications secretary to release a statement on his behalf expressing concern about pejorative and false comments made about his girlfriend by mainstream media and internet trolls.
In September 2017, Harry and Markle made their first public appearance together at the Invictus Games in Toronto.
Their engagement was announced on 27 November 2017 by Harry's father.
The announcement prompted generally positive commentary about having a mixed‐race person as a member of the royal family, particularly in Commonwealth countries with populations of blended or native ancestry.
On the morning of the wedding, Queen Elizabeth II conferred the title of Duke of Sussex upon Harry; Markle became Duchess of Sussex through her marriage to him later that day.
The ceremony was held at St George's Chapel, Windsor Castle on 19 May 2018.
The couple later revealed in the 2021 television interview Oprah with Meghan and Harry that, three days before the ceremony, they had privately exchanged vows in their garden in the presence of the Archbishop of Canterbury.
The Duke and Duchess initially lived at Nottingham Cottage in London, within the grounds of Kensington Palace.
The couple considered settling in the 21-room Apartment 1 at Kensington Palace, but instead moved to Frogmore Cottage in the Home Park of Windsor Castle, which Queen Elizabeth II had recently gifted to them.
The Crown Estate refurbished the cottage at a cost of £2.4 million, paid from the Sovereign Grant, with the Duke later reimbursing expenses beyond restoration and ordinary maintenance, part of which was offset against rental payments due at the time.
On 6 May 2019, the Duke and Duchess's son, Archie, was born.
Their office was moved to Buckingham Palace and officially closed on 31 March 2020 when the Sussexes ceased "undertaking official engagements in support of the Queen".
The following month, the Duchess suffered a miscarriage.
The Duke and Duchess have owned a Labrador named Pula and two Beagles named Guy and Mamma Mia.
In 2017, Harry stated that he had "five or six" godchildren, some of whom later attended his wedding.
Health

In May 1988, Harry underwent a surgery for a minor hernia.
In his memoir Spare, Harry states that he took cocaine at the age of 17.
In 2002, it was reported that, with Charles's encouragement, Harry had visited a drug-rehabilitation unit to speak with recovering drug addicts after it emerged that he had been smoking cannabis and drinking at his father's Highgrove House and at a local pub in the summer of 2001.
He adds in the memoir that he smoked cannabis at Eton and in the gardens Kensington Palace, though he later told a court that "he never smoked in  father's house".
In 2017, during an appearance on Bryony Gordon's podcast Mad World, Harry said that, with the support of his brother, he had sought counselling years after his mother's death.
He stated that he had struggled with aggression, experienced anxiety during royal engagements, and had been "very close to a complete breakdown on numerous occasions".
He also said that what he experienced after his mother's death "was very much" post-traumatic stress disorder (PTSD).
In his mental-health documentary, The Me You Can't See which premiered in 2021, Harry said that he had undergone four years of therapy to address his mental-health difficulties, having been encouraged to do so by his future wife after they began dating.
In his 2023 memoir, Harry described himself as an agoraphobe.
Political views

In September 2020, Harry and his wife released a video addressing American voters, urging them to "reject hate speech, misinformation and online negativity" in the 2020 United States presidential election, a message that some commentators interpreted as an implicit endorsement of Joe Biden.
Earlier that year, Harry had been the subject of a prank by the Russian comedy duo Vovan and Lexus, who posed as climate activist Greta Thunberg and her father during two phone calls on New Year's Eve and 22 January 2020.
During the conversations, Harry described his decision to leave the monarchy as "not easy" and criticised Donald Trump's stance on climate change and his support for the coal industry.
In May 2021, Harry appeared on Dax Shepard and Monica Padman's podcast Armchair Expert, where he discussed freedom of speech and related laws in the US, saying, "I've got so much I want to say about the First Amendment as I sort of understand it, but it is bonkers."
His comments drew criticism from a number of conservative American public figures, including Ted Cruz, Dan Crenshaw, Candace Owens, Jack Posobiec, and Laura Ingraham, as well as British politician Nigel Farage.
In November 2021, during a panel at Wired's Re:Wired Conference, Harry said that he had emailed Jack Dorsey, CEO of Twitter, the day before the January 6 United States Capitol attack to "warn" of potential civil unrest, but had not received a response.
In the same month, Conservative MP Johnny Mercer, who was leading efforts to waive visa fees for foreign-born UK veterans and their families, told the Commons that the Duke of Sussex supported the proposal and viewed it as "morally right", adding that it should not be interpreted as "a political intervention".
In June 2022, in an interview with Jessica Yellin for Vogue, Meghan described Harry's reaction to the Supreme Court of the United States's decision that abortion is not a constitutionally protected right as "guttural".
Harry later criticised the ruling as "rolling back of constitutional rights" in his address to the United Nations on Mandela Day in July 2022.
Associate justice Samuel Alito, who wrote the majority opinion in the case, subsequently criticised foreign figures, including Harry,  for commenting on "American law" during a public speech.
In June 2023, Harry broke with royal protocol by criticising the UK government in a witness statement submitted to a court.
In February 2026, Harry stated in an interview with Channel 4 that aid corridors had been shut to Gaza in the aftermath of the Gaza war, which prompted Israel's deputy minister of foreign affairs, Sharren Haskel, to invite him "to speak directly with the British general serving at the CMCC center ...
She described his comments as "deeply disappointing" given his position as a member of the British royal family.
Drug use and U.S. visa application

In March 2023, the Heritage Foundation (HF) sent a dossier on Harry's past drug use to various government entities, asking whether he had disclosed such use on his U.S. visa application.
In March 2024, the U.S. government was ordered to provide Harry's visa-application materials to a D.C. court, following an earlier unsuccessful freedom‐of‐information request submitted by the HF.
Immigration officials argued that the HF could "not point to any evidence of government misconduct", while Harry's representatives said he had been "truthful" and that the documents indicated he had not received preferential treatment.
In February 2025, the U.S. president Donald Trump ruled out deporting Harry, telling the New York Post: "I'll leave him alone.
"


Public life

At the age of 21, Harry was appointed a Counsellor of State and began his duties in that capacity.
The Queen granted Harry and William their own royal household on 6 January 2009.
Previously, William and Harry's affairs had been handled by their father's office at Clarence House in central London.
The new household released a statement announcing they had established their own office at nearby St James's Palace to look after their public, military and charitable activities.
In March 2012, Harry led an official visit to Belize as part of the Queen's Diamond Jubilee celebrations.
Harry also played tambourine and took part in the music video for the song "Sing", which was released in May 2012 to commemorate the Diamond Jubilee.
In Italy, Harry attended commemorations of the 70th anniversary of the Monte Cassino battles, in which Polish, Commonwealth and British troops fought.
He opened the Field of Remembrance at Westminster Abbey on 6 November 2014, a task usually performed by Prince Philip.
Before reporting for duty to the Australian Defence Force (ADF), Harry visited the Australian War Memorial in Canberra on 6 April 2015.
In October 2015, Harry carried out a day of engagements in the US.
Harry, as patron of Sentebale, travelled to Lesotho to attend the opening of the Mamohato Children's Centre in November 2015.
He visited Cape Town, where he presented the insignia of the Order of the Companions of Honour to the Archbishop on behalf of the Queen.
Harry also played the Sentebale Royal Salute Polo Cup, at Val de Vie Estate in Cape Town, fundraising for Sentebale.
Also in that month, Harry became a patron of Walk of America, a campaign which brings together a number of veterans who will take part in a 1,000-mile expedition across the US in mid-2018.
The Prince was appointed the president of The Queen's Commonwealth Trust, which focuses on projects involving children and welfare of prisoners, in April.
In July 2018, Harry travelled to Dublin, Ireland, alongside his wife Meghan, which marked their first overseas visit as a couple.
In October 2018, the Duke and Duchess of Sussex travelled to Sydney, for the 2018 Invictus Games.
Harry identifies as a feminist.
During their visit to Morocco in February 2019, the Duke and Duchess focused on projects centred on "women's empowerment, girls' education, inclusivity and encouragement of social entrepreneurship".
As part of establishing a separate office from that of the Duke and Duchess of Cambridge in 2019, the Duke and Duchess created an Instagram social media account, which broke the record for the fastest account at the time to reach a million followers.
During his trip to Angola in 2019, the Duke visited the Born Free to Shine project in Luanda, an initiative by First Lady Ana Dias Lourenço which aims to "prevent HIV transmission from mothers to babies" through education, medical testing and treatment.
During his visit to the Luengue-Luiana National Park, the Duke unveiled an initiative by the Queen's Commonwealth Canopy to help with protecting "an ancient elephant migration route" by providing safe passage for them in the forest.
Harry completed 1,190 engagements between 2006 and 2019.
Stepping back and subsequent public appearances

In January 2020, the Duke and Duchess announced that they were stepping back from their role as senior members of the royal family, and would balance their time between the United Kingdom and North America.
A statement released by the Palace confirmed that the Duke and Duchess were to become financially independent and cease to represent the Queen.
At the time of the announcement of Harry and Meghan's decision to "step back" as senior members of the royal family in 2020, 95% of the couple's income derived from the £2.3 million given to them annually by Harry's father, Charles, as part of his income from the Duchy of Cornwall.
The formal role of the Duke and Duchess was subject to a twelve-month review period, ending in March 2021.
In March 2020, Harry attended the opening of the Silverstone Experience in Silverstone Circuit together with racing driver Lewis Hamilton.
Harry's appearance at the museum was his final solo engagement as a senior royal.
He and Meghan attended the Commonwealth Day service at Westminster Abbey on 9 March 2020, which was their last engagement as a couple before they officially stepped down on 31 March.
Harry's personal wealth was estimated at £30 million by The Daily Telegraph in 2020.
In April 2021, Harry returned to the UK to attend the funeral of his grandfather, Prince Philip, Duke of Edinburgh.
Meghan did not attend due to her pregnancy.
On 8 September, while Harry and Meghan were in London preparing to attend a charity event, Queen Elizabeth II died at Balmoral Castle in Scotland, and they remained in the United Kingdom for her funeral.
Harry and Meghan visited Nigeria in May 2024 to honour the work of the Invictus Games.
In August that year, the couple visited Colombia at the invitation of the country's vice-president, Francia Márquez.
Harry visited the Superhumans Center in Lviv, Ukraine, in April 2025 after an invitation from its chief executive.
On 3 November 2025, Harry's office announced that he would travel to Toronto, Canada, for a series of events ahead of Remembrance Day.
He and Meghan visited Jordan in February 2026 with the Director-General of the World Health Organization (WHO) Tedros Adhanom Ghebreyesus.
In April 2026, Harry and Meghan undertook a four‐day visit to Australia.
Australian police later announced that they would be conducting an operation to ensure safety during parts of the couple's tour.
Later that month, Harry made another visit to Kyiv, where he used a speech at the Kyiv Security Forum to urge the U.S. to take a stronger role in supporting Ukraine and said to Russian President Vladimir Putin that "there is still a moment – now – to stop this war."
In response to the remarks, U.S. president Donald Trump stated, "I know one thing, Prince Harry is not speaking for the UK, that's for sure".


Publicly funded police security

Harry faced difficulties with obtaining and maintaining publicly funded security, both in Canada and the United Kingdom, after he and Meghan announced their self-demotion within the royal family.
While the couple resided on Vancouver Island, the Canadian Taxpayers Federation launched a petition calling for the Royal Canadian Mounted Police to cease providing security to the Sussexes.
In January 2022, it was reported that Harry had been in a legal fight since September 2021 over the Home Office's refusal to allow him to pay for police protection.
Following the first court hearing of the case by the High Court, it was revealed that Harry had 'exceptional status' and the Royal and VIP Executive Committee (RAVEC) still determined his personal protective security on a case-by-case basis.
After receiving applications by the Duke and the Home Office to keep parts of the case private, the High Court ruled in March 2022 that some parts of it would remain confidential.
Mr Justice Swift also reacted to the Duke's legal team sending a copy of the ruling to someone who was not a lawyer, describing it as "entirely unacceptable".
In July 2022, Mr Justice Swift granted permission for part of Harry's claim to proceed for a judicial review.
Harry filed a lawsuit against the Home Office and the Metropolitan Police in August 2022, challenging the decision by RAVEC from January 2022 which stated that State security could not be made available to private individuals even if they wished to pay for it themselves.
In February 2023, a High Court judge ruled that the second case should be thrown out; however, the decision was later appealed by Harry's legal team.
He lost the legal challenge in May 2023, meaning that he will not be allowed to make private payments for police protection.
In June 2023, a Freedom of Information request revealed that Harry's legal fight with the Home Office had cost £502,236, with £492,000 covered by the state and the remaining £10,000 covered by Harry.
In February 2024, the High Court ruled against Harry in his case against the Home Office and upheld the decision by RAVEC, stating that there had been no unlawfulness in the decision-making process for his security arrangements.
It was also revealed that during the proceedings Harry had leaked information via email to "a partner of Schillings" and to Johnny Mercer, for which he apologised to the court.
In December 2025, it was announced that, for the first time since April 2019, RAVEC would reassess Harry's threat level.
Civilian career and investments

In summer 2019, before announcing their decision to step back in January 2020, Harry and his wife were involved in talks with Jeffrey Katzenberg, the founder of the now-defunct streaming platform Quibi, over a possible role in the service without gaining personal profits, but they eventually decided against joining the project.
Between 2019 and 2020, Harry and Meghan contributed to the book Finding Freedom through a third-party source.
Despite initially denying their involvement with the book, their contributions to the book became apparent during Meghan's court case against Associated Newspapers who were trying to use the book in their defense.
In June 2020, they signed with the Harry Walker Agency, owned by media company Endeavor, to conduct paid public speaking engagements.
In December 2020, the Duke and Duchess signed a multi-year deal with Spotify to produce and host their own programs through their audio producing company, Archewell Audio.
Harry & Meghan, a docuseries about the Sussexes, was produced by Netflix and the couple's Archewell Productions and premiered on 8 December 2022.
In March 2021, San Francisco-based mental health start-up BetterUp, a company that helps people get in contact with coaches or counsellors, said that Harry would become its first chief impact officer.
In the same month, Harry was appointed as a commissioner for the Aspen Institute's Commission on Information Disorder to carry out a six-month study on the state of misinformation and disinformation in the US.
In the following month, in his capacity as BetterUp's chief impact officer, Harry was interviewed by Fast Company, stating that the recent trend of people leaving their jobs (known as the Great Resignation) was something that needed to be celebrated, though his remarks were criticised for coming from a position of privilege.
In April 2022, reports emerged of criticism by the company's coaches over the new metrics placed for evaluating their services and over the opacity surrounding Harry's actual role in the firm.
In April 2019, it was announced that Harry was working as co-creator and executive producer on a documentary series about mental health together with Oprah Winfrey, which was initially set to air in 2020 on Apple TV+.
In the following month, UCAS reported an increase in the percentage of students declaring mental health issues on their university applications, citing self-help books and Harry's statements on his struggles with "panic attacks and anxiety" as contributing factors.
In October 2021, Harry and Meghan announced their partnership with Ethic, a sustainable investment firm based in New York City, which also manages the couple's investments.
According to state filings from Delaware, where the couple's Archewell foundation is registered, Harry and Meghan incorporated 11 companies and a trust beginning in early 2020 which include Orinoco Publishing LLC and Peca Publishing LLC to hold the rights for their books as well as Cobblestone Lane LLC and IPHW LLC which are holders of their foundation's logos.
In July 2021, it was announced that Harry was set to publish his memoir Spare via Penguin Random House, with Harry reportedly earning an advance of at least $20 million.
The memoir is reportedly the first of a four-book publishing deal that is set to include a second book by Harry and a wellness guide by Meghan.
Harry announced that $1.5 million of the proceeds from the memoir were pledged to the charity Sentebale, while £300,000 would be given to WellChild.
Charity work

Humanitarian and environmental activities

Harry has granted his patronage to organisations including WellChild, Dolen Cymru, MapAction and the London Marathon Charitable Trust; he stepped down from MapAction in 2019 and the London Marathon Charitable Trust in 2021.
In 2007 he and William organised the Concert for Diana, in memory of their mother, which benefited the charities and patronages of Diana, William, and Harry.
In October 2008, Harry and his brother embarked on the 1,000 mile eight-day Enduro Africa motorbike ride across South Africa to raise money for Sentebale, UNICEF and the Nelson Mandela Children's Fund.
In September 2009, William and Harry set up The Foundation of Prince William and Prince Harry to enable them to take forward their charitable ambitions.
Harry left the charity in June 2019.
After taking part in an unfinished trip to the North Pole with Walking With The Wounded in 2011, Harry joined the charity's 200-mile expedition to the South Pole in Antarctica during December 2013, accompanying twelve injured servicemen and women from the UK, the US and the Commonwealth.
To raise awareness for HIV testing, Harry took a test live on the royal family Facebook page on 14 July 2016.
On World AIDS Day, Harry and Rihanna helped publicise HIV testing by taking the test themselves.
Since 2016 Harry has been working with Terrence Higgins Trust to raise awareness about HIV and sexual health.
In November 2019, to mark the National HIV Testing Week, the Duke interviewed HIV+ Rugby player Gareth Thomas on behalf of the trust.
In December 2017, Harry guest edited BBC Radio 4's Today programme, conducting interviews with his father, then Prince of Wales, former US president Barack Obama, and others on issues such as youth violence, the Armed Forces, mental health, the Commonwealth, conservation and the environment.
Harry was officially appointed the new president of African Parks (a conservation NGO) on 27 December 2017, a position which he held until 2023 when he was appointed a member of its board of directors.
Harry had previously helped with relocating rhinos in the Okavango Delta and later became patron of the Rhino Conservation Botswana.
In July 2018, the Elton John AIDS Foundation announced that the Duke of Sussex and British singer Elton John were about to launch a global coalition called MenStar that would focus "on treating HIV infections in men".
In May 2019, the Duke and Duchess of Sussex together with Harry's brother and sister-in-law launched Shout, the UK's first 24/7 text messaging service for those who suffer from mental issues.
In September 2019, the Duke launched Travalyst during his visit to the Netherlands after two years of development.
In October 2019, along with other members of the royal family, Harry voiced a Public Health England announcement, for the "Every Mind Matters" mental health program.
In February 2020, Harry recorded a new version of the song "Unbroken" with Jon Bon Jovi.
In April 2020, Harry launched a new initiative named HeadFIT, a platform designed to provide mental support for members of the armed forces.
The initiative was developed mutually by the Royal Foundation's Heads Together campaign, the Ministry of Defence, and King's College London.
In June 2020, the Duke and Duchess backed the Stop Hate for Profit campaign and encouraged CEOs of different companies to join the movement.
In April 2021, Harry and Meghan were announced as campaign chairs for Vax Live: The Concert to Reunite the World, an event organised by Global Citizen to increase access to COVID-19 vaccinations.
Later that month, he narrated "Hope Starts Here", a special video rereleased by African Parks to mark the Earth Day in which he urged organisations and communities to preserve biodiversity and paid tribute to his grandfather Prince Philip for his efforts as a conservationist.
Like his mother, Harry has worked with the HALO Trust, an organisation that removes debris—particularly landmines—left behind by war.
In April 2017, he hosted the Landmine Free 2025 reception at Kensington Palace, during which the UK government announced an increase in its financial support for de-mining efforts.
In September 2019, he walked through a de-mining site in Angola, the same country visited by his mother 22 years earlier.
In June 2021, after ten members of the trust were killed by an armed group at a mine clearance camp in Afghanistan, Harry issued a statement saying the attack "was nothing less than an act of barbarism".
In the same month and ahead of the 2021 G20 Rome summit, Harry and his wife penned an open letter together with the Director-General of the World Health Organization, Tedros Adhanom Ghebreyesus, asking the G20 leaders to expedite efforts for the global distribution of COVID-19 vaccines.
In April 2022 and in a video featuring Rhys Darby and Dave Fane on Māori Television, Harry launched an eco-travel campaign through his non-profit Travalyst, encouraging people to travel sustainably.
In September 2025, Harry announced that he had personally donated £1.1 million to BBC Children in Need in December 2024, describing it as a "significant investment" in grassroots organisations in Nottingham supporting young people affected by violence.
In the following month, he and Meghan joined a coalition of public figures, scientists, and tech experts in signing an open letter calling for a global ban on the development of artificial superintelligence until there is strong scientific consensus and public support ensuring it can be created safely and ethically, emphasising the existential risks such unchecked AI could pose to humanity.
Sport

Harry has enjoyed playing sports, such as competitive polo, skiing, and motocross.
Like his brother and father, he has participated in polo matches to raise money for charitable causes.
Harry is also a keen Rugby football fan and supported England's bid to host rugby union's 2015 Rugby World Cup, and presented the trophy at rugby league's 2019 Challenge Cup finals.
In 2004 Harry trained as a Rugby Development Officer for the Rugby Football Union and coached students in schools to encourage them to learn the sport.
He had served as the RFU's vice-royal patron since 2010, supporting the Queen as patron.
In 2012 Harry launched Coach Core alongside his brother and sister-in-law, the Duke and Duchess of Cambridge.
In January 2017, Harry visited the Running Charity and its partner Depaul UK to highlight the role of sport in helping homeless and vulnerable people.
In June 2019, the Duke was present at the launch of Made by Sport, a charity coalition set to raise money to boost sport in disadvantaged communities.
In his statement, he lent his support to the charity by arguing that its role in bringing sport into the life of disadvantaged people would save "hundreds of millions of pounds" towards treating the issues among young people.
Sussex Royal and Archewell

In June 2019, it was announced that the Duke and Duchess of Sussex would split from The Royal Foundation and establish their own charity foundation by the end of 2019.
Nevertheless, the couple would collaborate with Harry's brother and his wife on mutual projects, such as the mental health initiative Heads Together.
In July 2019, Harry and Meghan's new charity was registered in England and Wales under the title "Sussex Royal The Foundation of The Duke and Duchess of Sussex".
It was confirmed on 21 February 2020 that "Sussex Royal" would not be used as a brand name for the couple following their withdrawal from public life.
Sussex Royal Foundation was renamed "MWX Foundation" on 5 August 2020 and dissolved the same day.
In March 2021, it was reported that the Charity Commission for England and Wales was conducting a review of the Sussex Royal organisation in a "regulatory and compliance case" regarding its conduct under charity law during dissolution.
Representatives for the couple claimed that Sussex Royal was "managed by a board of trustees" and that "suggestion of mismanagement" directed exclusively at the Duke and Duchess would be incorrect.
In April 2020, Meghan and Harry confirmed their new foundation (in lieu of Sussex Royal) would be called "Archewell".
Sentebale

In 2006 Harry visited Mants'ase Children's Home near Mohale's Hoek in Lesotho, which he had first toured in 2004, and alongside Prince Seeiso of Lesotho, he launched Sentebale: The Princes' Fund for Lesotho, a charity to assist children orphaned by HIV/AIDS.
In March 2025, Harry and Prince Seeiso of Lesotho resigned from their roles as patrons of Sentebale following a dispute between the charity's trustees and the chair of the board, Sophie Chandauka.
Chandauka later accused Harry of "harassment and bullying at scale" by authorising "the release of a damaging piece of news to the outside world", adding that his "toxic" brand was "the number one risk" for the organisation.
There were also allegations that through his contacts Harry had asked Chandauka to issue a statement in support of his wife following an awkward interaction between the two women during a polo match in Miami, and had later demanded that she "explain herself" in a note that was described as "unpleasant" in tone and reportedly used "imperious" language.
In August 2025 the Charity Commission announced it found no evidence of "widespread or systemic bullying or harassment, including misogyny or misogynoir" or "over-reach" by either Chandauka or Harry but acknowledged a "strong perception of ill treatment felt by a number of parties" and stated that deciding on specific allegations of bullying was outside the purview of its regulatory authority.
In March 2026, Sentebale filed a defamation claim against Harry and former trustee Mark Dyer, with documents lodged in the High Court in London alleging that they had conducted an "adverse media campaign" against the charity since March 2025.
Public image

In his youth, Harry earned a reputation for being rebellious, leading the tabloid press to label him a "wild child".
Clarence House later issued a public statement in which Harry apologised for his behaviour.
In January 2005, in response to an inquiry about his Zimbabwean girlfriend Chelsy Davy, Harry responded "She's not black or anything, you know".
In January 2009, the British tabloid, the News of the World, revealed a video made by Harry three years earlier in which he referred to a Pakistani fellow officer cadet as "our little Paki friend" and called a soldier wearing a camouflage hood a "raghead".
A British Muslim youth organisation called Harry a "thug".
Clarence House immediately issued an apology from Harry, who stated that no malice was intended in his remarks.
Subsequently, it was reported that the military had instructed Harry to attend a diversity course.
In the same year, British stand-up comedian Stephen K. Amos alleged that after a stand-up show for Charles's 60th birthday celebrations in November 2008 Harry had commented on his performance by saying, "You don't sound like a black chap", though he hoped that the remarks were made in jest.
In October 2007, a video from Harry's trip to Namibia with his friends surfaced, which showed him snorting vodka and licking a male friend's nipples.
While on holiday in Las Vegas in August 2012, Harry and an unknown young woman were photographed naked in a Wynn Las Vegas hotel room, reportedly during a game of strip billiards.
Royal aides suggested Clarence House would contact the Press Complaints Commission (PCC) if British publications used the pictures.
St James's Palace confirmed that Harry was in the photographs, saying that he was essentially a victim whose privacy had been invaded and contacted the PCC upon hearing that a number of British newspapers were considering publishing the photographs.
At a 2014 event in England, Foo Fighters drummer Taylor Hawkins was slapped by Harry after he had told him "I can't wake up, so tired", with Harry subsequently stating "You awake now?"
Hawkins added "I got slapped in the face by the prince.
But in the moment, I was like, 'You fucking slapped me, dude.'
"


In December 2021, reports emerged about Harry's meetings with Saudi businessman Mahfouz Marei Mubarak bin Mahfouz, whose receipt of a CBE became the subject of an investigation by the Scottish Charity Regulator.
Mahfouz had met Harry in 2013 and 2014 and donated £50,000 to his charity Sentebale and £10,000 to Walking With The Wounded, of which Harry is patron.
The Sunday Times claimed that the meetings with Harry opened the way for Mahfouz to get access to the Prince of Wales.
Harry referred to the incident as the "CBE scandal" in December 2021 and stated that he severed ties with Mahfouz in 2015 after expressing "growing concerns" about his motives, though aides from his father's household denied having any discussions with him regarding Mahfouz.
In March 2024, Harry was named in a lawsuit against P. Diddy who was facing allegations of sexual trafficking.
In view of their environmental activism, Harry and Meghan were criticised in August 2019 for reportedly taking four private jet journeys in 11 days, including one to Elton John's home in Nice, France.
The criticism was in line with the reactions the royal family faced in June 2019, after it was revealed that they "had doubled  carbon footprint from business travel".
Harry received backlash again in August 2021 and 2022 for taking a two-hour flight on private jets between California and Aspen, Colorado, to participate in an annual charity polo tournament.
In June 2022 and on their way to California after the Queen's Platinum Jubilee, Harry and Meghan boarded a private jet that was estimated to have emitted "ten times more carbon than flying commercial".
After his marriage, Harry's popularity skyrocketed above all the other royals as he was deemed likable by 77 per cent of respondents in a poll of 3,600 Britons conducted by statistics and polling company YouGov.
However, his popularity fell after stepping back from royal duties, and it plummeted after the release of his controversial interview with Oprah Winfrey, his Netflix docuseries, and his memoir.
In December 2022, Harry was found to be the third most disliked member of the British royal family by YouGov, preceded by his uncle Prince Andrew and his wife Meghan.
Writing for The New York Times, Sarah Lyall noted that following the release of his memoir Harry and his wife lost support within segments of the American public and press.
It has been suggested by critics that this fall from public esteem is due to Harry and Meghan's frequent attempts to achieve ongoing relevancy, and their perceived hypocrisy and selfishness.
Harry and Meghan's exit from the royal family was satirized in a 2023 episode of South Park.
In 2018 and 2021, Harry was selected as one of the 100 Most Influential People in the World by Time magazine.
In 2019, the magazine named Harry and his wife as among the 25 Most Influential People on the Internet.
In the same year, James Hibberd of The Hollywood Reporter named Harry and Meghan among the Hollywood losers of 2023.
Following Harry and Meghan's trip to Nigeria in May 2024, Lucia Stein of the ABC argued that the couple could have been used by the royal family, and added that "perhaps how helpful they would have been" had an agreement on a "hybrid working model" been achieved.
Media editor, Tina Brown commented in relation to the visit, they are "enormously appealing to the public, and very good at ."
In the same year Harry's role as founder of Travalyst was recognised in the second edition of the Time 100 Climate list which ranked the most influential climate action leaders.
In January 2025, Harry and Meghan's appearance at a food bank during the Southern California wildfires in the Pacific Palisades drew mixed reactions from segments of the media and public figures, who labeled it "disaster tourism".
Privacy and the media

Legal issues and incidents

Associated Newspapers

In January 2020, the Independent Press Standards Organisation (IPSO) sided with the Mail on Sunday over a dispute between the Duke and the newspaper regarding an Instagram photo involving Harry in which, according to the newspaper, elephants were in fact "tranquilised" and "tethered" during a relocating process.
The IPSO rejected Harry's claim that the paper's description was "inaccurate" or "misleading".
In December 2020, Harry's legal team sued Associated Newspapers Limited (ANL) for publishing a story in the Mail on Sunday claiming his working relationship with the Royal Marines had suffered post-royal departure.
The prince's lawyer said the "substantial damages" paid by the publisher would be donated to the Invictus Games Foundation.
In February 2022, Harry filed a libel suit in the High Court against ANL for a Mail on Sunday article which alleged he was trying to keep his legal battle against the Home Office to restore his police protection secret from the public through requesting a confidentiality order on the case and that he offered to pay for police protection only after filing a lawsuit against the government.
In June 2022, Mr Justice Nicklin ruled that parts of the article were potentially defamatory, though Nicklin rejected claims by Harry's lawyers that the article portrayed him as a liar.
Harry attempted to have the publisher's defence thrown out, but the judge rejected his motion in December 2023 and decided that the case should proceed to trial.
He later ordered Harry to pay Mail on Sunday £48,447 in legal costs.
Harry withdrew the libel claim in January 2024 and became liable for the publisher's £250,000 legal costs.
In October 2022, the Duke of Sussex joined Doreen Lawrence, Sir Elton John, David Furnish, Sadie Frost, Elizabeth Hurley, and Sir Simon Hughes in launching a legal action against ANL for their alleged "abhorrent criminal activity", which was said to involve listening to and recording people's phone calls and daily activities, obtaining sensitive information and medical records, and accessing bank accounts and financial transactions.
In November 2023, Mr Justice Nicklin ruled that the case brought by Harry and the other claimants could proceed but unpublished material provided to the Leveson Inquiry was inadmissible as proof in this case.
Harry's claims relate to 14 articles published between 2001 and 2013, which his lawyer argued could not have been lawfully sourced.
During the trial, it was revealed that between 2011 and 2012 Harry himself had a close relationship with Charlotte Griffiths, a Mail on Sunday reporter, whom he had exchanges with via Facebook and phones.
News Group and Mirror Group newspapers

In October 2019, it was announced that Harry had sued the Daily Mirror, The Sun and the now-defunct News of the World "in relation to alleged phone-hacking".
Former News of the World royal editor Clive Goodman had previously stated that he had hacked Harry's phone on nine occasions.
Andy Coulson, the editor of the News of the World, apologised to Harry and his brother for invading their privacy, accepting "ultimate responsibility" for the actions of Goodman.
In his lawsuit, Harry sought damages in excess of £200,000 from the publisher of the News of the World and The Sun and alleged an earlier agreement between News Group Newspapers (NGN) and the royal family which would see he and William not take legal action in return for an apology had not been honoured.
Both brothers brought a claim privately through their mutual attorneys, but Harry decided to pursue his case separately with a new solicitor in 2019.
In July 2023, the judge ruled that part of Harry's case involving allegations of illegal information gathering would go to trial but his phone-hacking claims were dismissed for being made too late.
In May 2024, Mr Justice Fancourt refused Harry the permission to include claims against Rupert Murdoch, expand his case's scope back to 1994 and 1995 to cover allegations involving his mother or to add new allegations from 2016 involving his then-girlfriend Meghan.
In October 2024, the judge announced that the two sides should either settle or go to trial in January 2025 and refused to let Harry's team include allegations that bugs were placed in rooms and cars, and trackers placed on vehicles as "no particulars whatsoever of such allegations" were provided.
In January 2025, the two parties settled with NGN paying more than £10 million in pay outs and legal fees in the settlements involving both Harry and former Labour deputy leader Tom Watson.
NGN made a "full and unequivocal apology" for "serious intrusion" by The Sun between 1996 and 2011, for "phone hacking, surveillance and misuse of private information by journalists and private investigators instructed by them at the News of the World" and the intrusion into the life of his mother, and admitted "incidents of unlawful activity" were carried out by private investigators working for the newspaper, but "not by journalists".
The BBC reported on the "scrapped case", highlighting NGN's statement which said that the settlement agreement "drew a line under the past" and that they rejected the claims that would have been made in court about a corporate cover-up.
Lawyers for the Mirror denied accessing Harry's voicemail messages and other allegations, but admitted to instructing "private investigators to unlawfully obtain private information" about Harry on a single occasion that involved him visiting Chinawhite.
In January 2023, a High Court judge ruled that Harry's lawsuit against Mirror Group Newspapers (MGN) as well as other similar lawsuits against the publisher would go to trial in May 2023.
At the beginning of trial, MGN apologised for one instance of unlawful information gathering against Harry and added that his legal challenge "warrants compensation".
In June 2023, Harry testified in the court case accusing former Daily Mirror editor Piers Morgan of horrific personal attacks and claimed that his phone had been hacked dating back to when he was still at Eton.
His appearance marked the first time a member of the royal family had been cross-examined in court since Albert Edward, Prince of Wales, appeared as a witness in court in 1891.
In December 2023, the High Court ruled in favour of Harry for 15 of the 33 sample stories used in his claims of phone hacking against MGN and awarded him £140,600 of the £440,000 he sought in damages.
Harry through his lawyer David Sherborne called the ruling "vindicating and affirming" and urged the authorities to further investigate and prosecute the company.
An additional 115 articles from Harry's claim might have been the focus of two further trials, but in February 2024 he settled his claim with MGN.
The publisher agreed to cover Harry's legal costs and pay damages reported to be in the region of £300,000.
Other cases

In October 2013, Jo Brand appeared on Have I Got News for You and while talking about Prince George's christening she said: "George's godparents include Hugh van Cutsem ...
I presume that's a nickname as in Hugh van cuts 'em and Harry then snorts 'em."
Representatives of Kensington Palace contacted the BBC after the programme aired, pointing out the error and the implications of the joke.
The BBC wrote to Kensington Palace apologising for the "factual inaccuracy" as George's godfather was William van Cutsem, but it did not apologise for the comment itself as it was part of the show's "irreverent humor".
In February 2014, a judge sentenced the convicted criminal Ashraf Islam to three years in prison, as he had plotted to murder Harry and had given it "considerable thought" due to his belief that Harry had "a moral guilt" since he was in the army.
In June 2019, two members of the neo-Nazi group Sonnenkrieg Division were jailed for eighteen months and four years, respectively, for sharing propaganda posters among which was one that labelled Harry as a "race traitor" with a gun pointed at his head.
The pair had called for the execution of Prince Harry and his son.
In December 2019, PA Media retracted the publishing of a Christmas card photograph of Harry, Meghan, and their son Archie.
The agency said that the photo was retracted because they had been advised that the photograph was "not representative of the Christmas card sent by the Duke and Duchess of Sussex".
In March 2020, the couple took Splash UK to court after the Duchess and their son were photographed without permission during a "private family outing" while staying in Canada.
In April 2020, the Duke and Duchess announced that they would no longer cooperate with the Daily Mail, the Sun, the Mirror and the Express.
In June 2020, it was reported that Harry's lawyers had issued a 'letter before action', threatening to sue the Sun and Dan Wootton, based on the allegations that they had paid money to associates of palace officials to secure their stories.
It was alleged that the Sun had made two payments amounting to £4,000 to the partner of a royal official in relation to stories published in June and July 2019 which detailed the nannying and god-parenting arrangements for Harry and Meghan's son Archie.
Wootton has been credited with breaking the story about Megxit and Harry and Meghan's initial plans for moving to Canada in the Sun on 8 January 2020, which prompted the couple to issue an announcement within hours, confirming their plans for stepping back from their royal duties.
"


A September 2020 article by The Times claiming an Invictus Games fundraiser had been cancelled due to its affiliation with a competitor of Netflix, Harry's business partner, became the subject of a legal complaint issued by the Duke.
Despite the palace congratulating the Duke and Duchess on the birth of their daughter Lilibet in June 2021, a few days later the BBC reported that Harry and Meghan had not sought the permission of the Queen before naming their daughter with her personal family nickname.
Lawyers for the couple subsequently accused the BBC of defamation and sent letters out to various media organisations saying the report was false and defamatory, and the allegations should not be repeated as Harry had spoken to the Queen before announcing their daughter's name.
In January 2024, two neo-Nazis, Christopher Gibbons and Tyrone Patten-Walsh, were given prison sentences between 8 and 11 years for terrorism, which included calling for the deaths of Harry and his son Archie on their podcast.
In April 2026, Harry and Meghan's team refused to provide details of the couple's visit to Australia to Guardian Australia, alleging that Daily Mail, Daily Mirror and Sky News Australia had broken a strict embargo on the couple's tour itinerary.
Interviews

Harry and his wife were interviewed by Oprah Winfrey in a television special for CBS, broadcast on 7 March 2021.
Meghan spoke about marriage, motherhood, and the pressures of public life.
Harry joined her later, and the pair talked about the initial difficulties associated with their move to the US in 2020 and their plans for the future.
During the interview, Harry criticised his father's parenting style, mentioned his father did not answer his calls and had cut him off financially, and he had no relationship with his brother.
In April 2022, Harry sat down for an interview with Today's Hoda Kotb during the Invictus Games, during which he claimed that he had visited his grandmother the Queen earlier to make sure that she was "protected and got the right people around her."
In January 2023 and ahead of the release of his memoir Spare, Harry sat down for a series of interviews, including an interview by Anderson Cooper on 60 Minutes, another one by Tom Bradby titled
Harry: The Interview on ITV1, an interview on The Late Show with Stephen Colbert and a fourth interview by Michael Strahan on Good Morning America, titled Prince Harry:
In the interview with Bradby, Harry said that he "would like to get my father back, I would like to have my brother back".
In a live-streamed interview with Harry in March 2023, physician Gabor Maté suggested publicly that he could be suffering from PTSD, ADD, anxiety, and depression based on his conversation with him and having read his autobiography Spare.
In May 2025, Harry was interviewed by Nada Tawfik of the BBC, during which he reflected on his loss of taxpayer-funded security and his ongoing estrangement from his family.
Writing for The Guardian, Stephen Bates stated that Harry's "megaphone diplomacy isn't working" and "his private security needs are probably not near the top of anybody's priorities".
On social media and other platforms

In October 2021, Twitter analytics service Bot Sentinel alleged that 83 accounts with a combined number of 187,631 followers were responsible for approximately 70% of the negative content posted about Harry and Meghan.
In January 2022, the BBC named Harry and Meghan among people whose photos and videos were used in fake instant profits advertisements and bitcoin-related investment schemes.


Titles, styles, honours and arms

Titles and styles

Harry was originally styled "His Royal Highness Prince Henry of Wales".
He used Wales as his surname for military purposes and was known as "Captain Harry Wales" in such contexts.
On the morning of his wedding, Elizabeth II granted him the Dukedom of Sussex, the Earldom of Dumbarton and Barony of Kilkeel.
He thus became known as "His Royal Highness The Duke of Sussex".
On 18 January 2020, Buckingham Palace announced that, following their decision to step back from royal duties, from 31 March 2020 the Duke and Duchess would not use their Royal Highness styles in practice or publicly.
They are still referred to as "His/Her Royal Highness" in legal and private settings.
While on his gap year in Lesotho in 2003, Harry was given the nickname Mohale (transl.
'the warrior'), a name that belonged to the younger brother of Moshoeshoe I.


Military ranks

Honours

Wear of orders, decorations, and medals

The ribbons worn regularly by Harry in undress uniform are as follows:


Appointments

Former honorary military appointments

The honorary military appointments above were returned to Elizabeth II in February 2021.
In August 2018, the Royal Canadian Legion granted him the 2018 Founders Award for his role in founding the Invictus Games.
In July 2021, Harry and Meghan were among people who were selected by UK-based charity Population Matters to receive the Change Champions Award for their decision to have only two children and help with maintaining a smaller and more sustainable population.
In February 2022, Harry and Meghan were selected to receive the NAACP's President's Award for their work on causes related to social justice and equity.
Harry was inducted into the Living Legends of Aviation in January 2024.
He received the Pat Tillman Award for Service during the 2024 ESPY Awards ceremony, recognising his service in the British Armed Forces and work with the Invictus Games, despite Tillman's mother believing that the award should have gone to "more fitting" recipients.
Arms

Ancestry

Agnatically, Harry is a member of the House of Glücksburg, a cadet branch of the House of Oldenburg, one of Europe's oldest royal houses.
Harry's paternal grandmother, Elizabeth II, issued letters patent on 8 February 1960 declaring his father to be a member of the House of Windsor.
Ancestors on Harry's father's side include most of the royal families of Europe, and on his mother's side, the earls Spencer—a cadet branch of the Spencer family descended from the earls of Sunderland; the senior branch are now also dukes of Marlborough; the Barons Fermoy; and more anciently from Henry FitzRoy, 1st Duke of Grafton; and Charles Lennox, 1st Duke of Richmond—two illegitimate sons of King Charles II.
Harry and his brother William descend matrilineally from Eliza Kewark (18th-century), who is variously described in contemporary documents as "a dark-skinned native woman", "an Armenian woman from Bombay", and "Mrs. Forbesian".
Genealogist William Addams Reitwiesner assumed Kewark was Armenian.
In June 2013, BritainsDNA announced that genealogical DNA tests on two of Harry and William's distant matrilineal cousins confirm Kewark was matrilineally of Indian descent.



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
  AssignClass (3afd3b04-fe61-41d9-bc12-49160e83c988)
 Call ID: 3afd3b04-fe61-41d9-bc12-49160e83c988
  Args:
    source: Prince_Harry
    type: :Man
  AssignClass (c0336efe-3fd4-418f-8d86-02821c54e0a2)
 Call ID: c0336efe-3fd4-418f-8d86-02821c54e0a2
  Args:
    type: :Person
    source: Prince_Harry
  AddLiteral (42c15e80-5fb7-445f-8409-5b654755e051)
 Call ID: 42c15e80-5fb7-445f-8409-5b654755e051
  Args:
    literal_value: 1984
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Harry
  AddLiteral (67c0e67c-7ae1-41e4-b483-bdc9f2fb3619)
 Call ID: 67c0e67c-7ae1-41e4-b483-bdc9f2fb3619
  Args:
    relation: :knownAs
    literal_value: Harry
    literal_type: xsd:string
    source: Prince_Harry
  AssignClass (a8c711dc-63af-4260-8691-e0e3ba2fae64)
 Call ID: a8c711dc-63af-4260-8691-e0e3ba2fae64
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (fcc5bdce-4649-42fa-9422-66083f1bb59c)
 Call ID: fcc5bdce-4649-42fa-9422-66083f1bb59c
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (02e8b99f-0b59-4226-9ee9-3945ff504f59)
 Call ID: 02e8b99f-0b59-4226-9ee9-3945ff504f59
  Args:
    type: :Woman
    source: Diana_Princess_of_Wales
  AssignClass (1a925204-ad7c-4626-99d9-ddcb6d0a08a1)
 Call ID: 1a925204-ad7c-4626-99d9-ddcb6d0a08a1
  Args:
    source: Diana_Princess_of_Wales
    type: :Person
  AddTriple (285dc872-ab9b-4787-9bd7-14bf43808338)
 Call ID: 285dc872-ab9b-4787-9bd7-14bf43808338
  Args:
    source: Prince_Harry
    relation: :hasFather
    target: King_Charles_III
  AddTriple (a8647091-4dda-4c19-8b7d-b05c004414df)
 Call ID: a8647091-4dda-4c19-8b7d-b05c004414df
  Args:
    target: Diana_Princess_of_Wales
    relation: :hasMother
    source: Prince_Harry
  AssignClass (d50b1d97-b9ef-4206-902b-e53ed78c4301)
 Call ID: d50b1d97-b9ef-4206-902b-e53ed78c4301
  Args:
    source: William_Prince_of_Wales
    type: :Man
  AssignClass (fec20dcd-5d88-4331-a849-f44c50536761)
 Call ID: fec20dcd-5d88-4331-a849-f44c50536761
  Args:
    type: :Person
    source: William_Prince_of_Wales
  AddTriple (cf443ac7-daa2-4675-8297-e8971f5e7370)
 Call ID: cf443ac7-daa2-4675-8297-e8971f5e7370
  Args:
    relation: :isBrotherOf
    target: William_Prince_of_Wales
    source: Prince_Harry
  AddTriple (d150f781-dda1-4cef-b6af-6b7709aa6273)
 Call ID: d150f781-dda1-4cef-b6af-6b7709aa6273
  Args:
    source: William_Prince_of_Wales
    target: Prince_Harry
    relation: :isBrotherOf
  AssignClass (ae670277-ab04-4a09-b194-085293978c8d)
 Call ID: ae670277-ab04-4a09-b194-085293978c8d
  Args:
    type: :Woman
    source: Meghan_Markle
  AssignClass (b12d2398-29ac-4731-b343-c46fddfde537)
 Call ID: b12d2398-29ac-4731-b343-c46fddfde537
  Args:
    source: Meghan_Markle
    type: :Person
  AddTriple (391dff97-55b3-4c39-bb5b-8ab84c6149ee)
 Call ID: 391dff97-55b3-4c39-bb5b-8ab84c6149ee
  Args:
    source: Prince_Harry
    target: Meghan_Markle
    relation: :hasRelation
  AddLiteral (57768e40-c675-4de7-be9a-529ac597655a)
 Call ID: 57768e40-c675-4de7-be9a-529ac597655a
  Args:
    source: Prince_Harry
    literal_type: xsd:integer
    literal_value: 2018
    relation: :hasMarriageYear
  AssignClass (0f6d1b6c-9a19-40e4-9ab9-3cc0f8e27dca)
 Call ID: 0f6d1b6c-9a19-40e4-9ab9-3cc0f8e27dca
  Args:
    type: :Man
    source: Archie
  AssignClass (b6c2ec35-dc4c-4dab-82ee-f65c0026722f)
 Call ID: b6c2ec35-dc4c-4dab-82ee-f65c0026722f
  Args:
    type: :Person
    source: Archie
  AddTriple (34479534-e0fd-4f3b-8046-1a9c0d478be1)
 Call ID: 34479534-e0fd-4f3b-8046-1a9c0d478be1
  Args:
    source: Archie
    target: Prince_Harry
    relation: :hasFather
  AddTriple (0ef20d3d-c5fb-47b9-94c9-42aaceddde68)
 Call ID: 0ef20d3d-c5fb-47b9-94c9-42aaceddde68
  Args:
    relation: :hasMother
    target: Meghan_Markle
    source: Archie
  AssignClass (e94f85e0-e9e2-4ef1-9ac8-de0be11cec6d)
 Call ID: e94f85e0-e9e2-4ef1-9ac8-de0be11cec6d
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (91eb41b5-5ac7-4a84-bdef-90d3e2a294eb)
 Call ID: 91eb41b5-5ac7-4a84-bdef-90d3e2a294eb
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (6c138e4e-3f3b-4f9c-83ff-1d958b5e02f8)
 Call ID: 6c138e4e-3f3b-4f9c-83ff-1d958b5e02f8
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (5109755a-f1c7-4add-8bce-8fde84dee2a6)
 Call ID: 5109755a-f1c7-4add-8bce-8fde84dee2a6
  Args:
    type: :Person
    source: Prince_Philip
  AssignClass (43c6a297-4ff0-4c53-8518-c8b943504c35)
 Call ID: 43c6a297-4ff0-4c53-8518-c8b943504c35
  Args:
    source: Charles_Spencer
    type: :Man
  AssignClass (3df08b1c-ac6b-4772-9a76-977109b42695)
 Call ID: 3df08b1c-ac6b-4772-9a76-977109b42695
  Args:
    source: Charles_Spencer
    type: :Person
  AddTriple (88c57b78-8885-4c6f-bcfb-d0efb55c18de)
 Call ID: 88c57b78-8885-4c6f-bcfb-d0efb55c18de
  Args:
    target: Queen_Elizabeth_II
    relation: :hasMother
    source: King_Charles_III
  AddTriple (b1142855-5c25-46a9-859b-f6ff47b3609d)
 Call ID: b1142855-5c25-46a9-859b-f6ff47b3609d
  Args:
    source: King_Charles_III
    target: Prince_Philip
    relation: :hasFather
  Finish (eb00fe1f-2221-40ad-b623-61879859c623)
 Call ID: eb00fe1f-2221-40ad-b623-61879859c623
  Args: