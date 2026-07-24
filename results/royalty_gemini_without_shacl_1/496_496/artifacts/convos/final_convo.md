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
Elizabeth II (Elizabeth Alexandra Mary; 21 April 1926 – 8 September 2022) was Queen of the United Kingdom and other Commonwealth realms from 6 February 1952 until her death in 2022.
Elizabeth was born in Mayfair, London, during the reign of her paternal grandfather, King George V.
She was the first child of the Duke and Duchess of York (later King George VI and Queen Elizabeth the Queen Mother).
Her father acceded to the throne in 1936 upon the abdication of his brother Edward VIII, making the ten-year-old Princess Elizabeth the heir presumptive.
In November 1947, she married Philip Mountbatten, a former prince of Greece and Denmark.
They had four children: Charles, Anne, Andrew, and Edward.
When her father died in February 1952, Elizabeth, then 25 years old, became queen of seven independent Commonwealth countries: the United Kingdom, Canada, Australia, New Zealand, South Africa, Pakistan, and Ceylon, as well as head of the Commonwealth.
Elizabeth reigned as a constitutional monarch through times of significant political change such as the Troubles in Northern Ireland, devolution in the United Kingdom, the decolonisation of Africa, and the United Kingdom's accession to the European Communities as well as its subsequent withdrawal.
As queen, Elizabeth was advised by more than 170 prime ministers across her realms.
Although there were occasional republican sentiment and media criticism of her family—particularly after the breakdowns of her children's marriages, her annus horribilis in 1992, and the death of her former daughter-in-law Diana in 1997—support for the monarchy and her popularity in the United Kingdom remained consistently high.
Elizabeth died aged 96 at Balmoral Castle in Scotland, and was succeeded by her eldest son as Charles III.
Early life

Elizabeth was born at 2:40 am on 21 April 1926 by Caesarean section at her maternal grandfather's London home, 17 Bruton Street in Mayfair, the first child of Prince Albert, Duke of York (later King George VI), and his wife, Elizabeth, Duchess of York (later Queen Elizabeth the Queen Mother).
Her father was the second son of King George V and Queen Mary, and her mother was the youngest daughter of Scottish aristocrat Claude Bowes-Lyon, 14th
She was baptised by the Archbishop of York, Cosmo Gordon Lang in the private chapel at Buckingham Palace on 29 May, and she was named Elizabeth after her mother; Alexandra after her paternal great-grandmother, who had died five months earlier; and Mary after her paternal grandmother.
She was cherished by her grandfather George V, whom she affectionately called "Grandpa England", and her regular visits during his serious illness in 1929 were credited in the popular press and by later biographers with raising his spirits and aiding his recovery.
Elizabeth's sole sibling, Princess Margaret, was born in 1930.
The two princesses were cared for by their nanny, Clara Knight, and educated at home under the supervision of their mother and their governess, Marion Crawford.
Crawford published a biography of Elizabeth and Margaret's childhood years titled The Little Princesses in 1950, much to the dismay of the royal family.
The book describes Elizabeth's love of horses and dogs, her orderliness, and her attitude of responsibility.
Others echoed such observations: Winston Churchill described Elizabeth when she was two as "a character.
Elizabeth's early life was spent primarily at the Yorks' residences at 145 Piccadilly (their town house in London) and Royal Lodge in Windsor.
Heir presumptive

During her grandfather's reign, Elizabeth was third in the line of succession to the British throne, behind her uncle Edward, Prince of Wales, and her father.
Although her birth generated public interest, she was not expected to become queen, as Edward was still young and expected to marry and have children of his own, who would precede Elizabeth in the line of succession.
When her grandfather died in 1936 and her uncle succeeded as Edward VIII, she became second in line to the throne, after her father.
Later that year, Edward abdicated, after his proposed marriage to divorced American socialite Wallis Simpson provoked a constitutional crisis.
Consequently, Elizabeth's father became king, taking the regnal name George VI.
Since Elizabeth had no brothers, she became heir presumptive.
If her parents had subsequently had a son, he would have been heir apparent and before her in the line of succession, which was determined by the male-preference primogeniture in effect at the time.
Elizabeth received private tuition in constitutional history from Henry Marten, Vice-Provost of Eton College, and learned French from a succession of native-speaking governesses.
A Girl Guides company, the 1st Buckingham Palace Company, was formed specifically so she could socialise with girls her age.
In 1939, Elizabeth's parents toured Canada and the United States.
As in 1927, when they had toured Australia and New Zealand, Elizabeth remained in Britain since her father thought she was too young to undertake public tours.
Lord Hailsham suggested that Princesses Elizabeth and Margaret should be evacuated to Canada to avoid the frequent aerial bombings of London by the Luftwaffe.
This was rejected by their mother, who declared, "The children won't go without me.
At Windsor, the princesses staged pantomimes at Christmas in aid of the Queen's Wool Fund, which bought yarn to knit into military garments.
In 1940, the 14-year-old Elizabeth made her first radio broadcast during the BBC's Children's Hour, addressing other children who had been evacuated from the cities.
"


In 1943, Elizabeth undertook her first solo public appearance on a visit to the Grenadier Guards, of which she had been appointed colonel the previous year.
At the end of the war in Europe, on Victory in Europe Day, Elizabeth and Margaret mingled incognito with the celebrating crowds in the streets of London.
In 1985, Elizabeth recalled in a rare interview, "... we asked my parents if we could go out and see for ourselves.
"


During the war, plans were drawn to quell Welsh nationalism by affiliating Elizabeth more closely with Wales.
Proposals, such as appointing her Constable of Caernarfon Castle or a patron of Urdd Gobaith Cymru (the Welsh League of Youth), were abandoned for several reasons, including fear of associating Elizabeth with conscientious objectors in the Urdd at a time when Britain was at war.
Welsh politicians suggested she be made Princess of Wales on her 18th birthday.
Home Secretary Herbert Morrison supported the idea, but the King rejected it because he felt such a title belonged solely to the wife of a prince of Wales and the prince of Wales had always been the heir apparent.
In 1946, she was inducted into the Gorsedd of Bards at the National Eisteddfod of Wales.
Elizabeth went on her first overseas tour in 1947, accompanying her parents through southern Africa.
I declare before you all that my whole life, whether it be long or short, shall be devoted to your service and the service of our great imperial family to which we all belong.
But I shall not have strength to carry out this resolution alone unless you join in it with me, as I now invite you to do: I know that your support will be unfailingly given.
Marriage

Elizabeth met her future husband, Prince Philip of Greece and Denmark, in 1934 and again in 1937.
They were second cousins once removed through King Christian IX of Denmark and third cousins through Queen Victoria.
After meeting for the third time at the Royal Naval College in Dartmouth in July 1939, Elizabeth—though only 13 years old—said she fell in love with Philip, who was 18, and they began to exchange letters.
Philip had no financial standing, was foreign-born (though a British subject who had served in the Royal Navy throughout the Second World War), and his sisters had married German noblemen with Nazi links.
He was a prince without a home or kingdom.
Some of the papers played long and loud tunes on the string of Philip's foreign origin."
Later biographies reported that Elizabeth's mother had reservations about the union initially and teased Philip as "the Hun".
In later life, however, she told the biographer Tim Heald that Philip was "an English gentleman".
Before the marriage, Philip renounced his Greek and Danish titles, officially converted from Greek Orthodoxy to Anglicanism, and adopted the style Lieutenant Philip Mountbatten, taking the surname of his mother's British family.
Shortly before the wedding, he was created Duke of Edinburgh and granted the style His Royal Highness.
Elizabeth and Philip were married on 20 November 1947 at Westminster Abbey.
Elizabeth required ration coupons to buy the material for her gown (which was designed by Norman Hartnell) because Britain had not yet completely recovered from the devastation of the war.
In post-war Britain, it was not acceptable for Philip's German relations, including his three surviving sisters, to be invited to the wedding.
Neither was an invitation extended to the Duke of Windsor, formerly King Edward VIII.
Elizabeth gave birth to her first child, Prince Charles, in November 1948.
One month earlier, the King had issued letters patent allowing her children to use the style and title of a royal prince or princess, to which they otherwise would not have been entitled, as their father was no longer a royal prince.
A second child, Princess Anne, was born in August 1950.
At various times between 1949 and 1951, Philip was stationed in the British Crown Colony of Malta as a serving Royal Navy officer.
He and Elizabeth lived intermittently in Malta for several months at a time in the hamlet of Gwardamanġa, at Villa Guardamangia, the rented home of Philip's uncle Lord Mountbatten.
Reign

Accession and coronation

As George VI's health declined during 1951, Elizabeth frequently stood in for him at public events.
When she visited Canada and Harry S. Truman in Washington, DC, in October 1951, her private secretary Martin Charteris carried a draft accession declaration in case the King died while she was on tour.
In early 1952, Elizabeth and Philip set out for a tour of Australia and New Zealand by way of the British colony of Kenya.
On 6 February, they had just returned to their Kenyan home, Sagana Lodge, after a night spent at Treetops Hotel, when word arrived of the death of Elizabeth's father.
Philip broke the news to the new queen.
She chose to retain Elizabeth as her regnal name, and was therefore called Elizabeth II.
The numeral offended some Scots, as she was the first Elizabeth to rule in Scotland.
She was proclaimed queen throughout her realms, and the royal party hastily returned to the United Kingdom.
Elizabeth and Philip moved into Buckingham Palace.
With Elizabeth's accession, it seemed possible that the royal house would take her husband's name, in line with the custom for married women of the time.
Lord Mountbatten advocated for House of Mountbatten, and Philip suggested House of Edinburgh, after his ducal title.
The British prime minister, Winston Churchill, and Elizabeth's grandmother Queen Mary favoured the retention of the House of Windsor.
Elizabeth issued a declaration on 9 April 1952 that the royal house would continue to be Windsor.
Philip complained, "I am the only man in the country not allowed to give his name to his own children."
In 1960, the surname Mountbatten-Windsor was adopted for Philip and Elizabeth's male-line descendants who do not carry royal titles.
Amid preparations for the coronation, Princess Margaret told her sister she wished to marry Peter Townsend, a divorcé 16 years Margaret's senior with two sons from his previous marriage.
Elizabeth asked them to wait for a year; in the words of her private secretary, "the Queen was naturally sympathetic towards the Princess, but I think she thought—she hoped—given time, the affair would peter out."
In 1960, she married Antony Armstrong-Jones, who was created Earl of Snowdon the following year.
Despite Queen Mary's death on 24 March 1953, the coronation went as planned on 2 June, as Mary had requested.
On Elizabeth's instruction, her coronation gown was embroidered with the floral emblems of Commonwealth countries.
Early reign

From Elizabeth's birth onwards, the British Empire continued its transformation into the Commonwealth of Nations.
In 1953, Elizabeth and Philip embarked on a seven-month round-the-world tour, visiting 13 countries and covering more than 40,000 miles (64,000 km) by land, sea and air.
Lord Mountbatten said that Elizabeth was opposed to the invasion, though Eden denied it.
The governing Conservative Party had no formal mechanism for choosing a leader, meaning that it fell to Elizabeth to decide whom to commission to form a government following Eden's resignation.
Lord Salisbury and Lord Kilmuir, the lord chancellor, consulted the British Cabinet, Churchill, and the chairman of the backbench 1922 Committee, resulting in Elizabeth appointing their recommended candidate: Harold Macmillan.
The Suez crisis and the choice of Eden's successor led, in 1957, to the first major personal criticism of Elizabeth.
Six years later, in 1963, Macmillan resigned and advised Elizabeth to appoint Alec Douglas-Home as the prime minister, advice she followed.
Elizabeth again came under criticism for appointing the prime minister on the advice of a small number of ministers or a single minister.
In 1965, the Conservatives adopted a formal mechanism for electing a leader, thus relieving the Queen of her involvement.
In 1957, Elizabeth made a state visit to the United States, where she addressed the United Nations General Assembly on behalf of the Commonwealth.
Two years later, solely in her capacity as Queen of Canada, she revisited the United States and toured Canada.
On a visit to Ghana the same year, she dismissed fears for her safety, even though her host, President Kwame Nkrumah, who had replaced her as head of state, was a target for assassins.
Harold Macmillan wrote, "The Queen has been absolutely determined all through ...
She loves her duty and means to be a Queen."
Before her tour through parts of Quebec in 1964, the press reported that extremists within the Quebec separatist movement were plotting Elizabeth's assassination.
Elizabeth gave birth to her third child, Andrew, in February 1960; this was the first birth to a reigning British monarch since 1857.
Her fourth child, Prince Edward, was born in March 1964.
According to biographer Gyles Brandreth, Elizabeth suffered a miscarriage at some point during her reign.
In 1965, however, the Rhodesian prime minister, Ian Smith, in opposition to moves towards majority rule, unilaterally declared independence with Elizabeth as "Queen of Rhodesia".
Although Elizabeth formally dismissed him, and the international community applied sanctions against Rhodesia, his regime survived for over a decade.
In 1966, the Queen was criticised for waiting eight days before visiting the village of Aberfan, where a mining disaster killed 116 children and 28 adults.
Martin Charteris said that the delay, made on his advice, was a mistake that she later regretted.
Elizabeth toured Yugoslavia in October 1972, becoming the first British monarch to visit a communist country.
In February 1974, British prime minister Edward Heath advised Elizabeth to call a general election in the middle of her tour of the Austronesian Pacific Rim, requiring her to fly back to Britain.
When discussions on forming a coalition foundered, Heath resigned, and Elizabeth asked the Leader of the Opposition, Labour's Harold Wilson, to form a government.
As Whitlam had a majority in the House of Representatives, Speaker Gordon Scholes appealed to Elizabeth to reverse Kerr's decision.
In 1977, Elizabeth marked the Silver Jubilee of her accession.
Parties and events took place throughout the Commonwealth, many coinciding with her associated national and Commonwealth tours.
The celebrations re-affirmed Elizabeth's popularity, despite virtually coincident negative press coverage of Princess Margaret's separation from her husband, Lord Snowdon.
In 1978, Elizabeth endured a state visit to the United Kingdom by Romania's communist leader, Nicolae Ceaușescu, and his wife, Elena, though privately she thought they had "blood on their hands".
The following year brought two blows: the unmasking of Anthony Blunt, former Surveyor of the Queen's Pictures, as a communist spy and the assassination of Lord Mountbatten by the Provisional Irish Republican Army.
According to Paul Martin Sr., by the end of the 1970s, Elizabeth was worried the Crown "had little meaning for" Pierre Trudeau, the Canadian prime minister.
Tony Benn said Elizabeth found Trudeau "rather disappointing".
Trudeau's supposed republicanism seemed to be confirmed by his antics, such as sliding down banisters at Buckingham Palace and pirouetting behind Elizabeth's back in 1977, and the removal of various Canadian royal symbols during his term of office.
In 1980, Canadian politicians sent to London to discuss the patriation of the Canadian constitution found Elizabeth "better informed ... than any of the British politicians or bureaucrats".
Perils and dissent

During the 1981 Trooping the Colour ceremony, six weeks before the wedding of Prince Charles and Lady Diana Spencer, six shots were fired at Elizabeth from close range as she rode down The Mall, London, on her horse, Burmese.
Police later discovered the shots were blanks.
Elizabeth's composure and skill in controlling her mount were widely praised.
That October, Elizabeth was the subject of another attack while on a visit to Dunedin, New Zealand.
Lewis was arrested, but instead of being charged with attempted murder or treason was sentenced to three years in jail for unlawful possession and discharge of a firearm.
Two years into his sentence, he attempted to escape a psychiatric hospital with the intention of assassinating Charles, who was visiting the country with Diana and their son Prince William.
From April to September 1982, Elizabeth's son Andrew served with British forces in the Falklands War, for which she reportedly felt anxiety and pride.
On 9 July, she awoke in her bedroom at Buckingham Palace to find an intruder, Michael Fagan, in the room with her.
In a serious lapse of security, assistance only arrived after two calls to the Palace police switchboard.
After hosting US president Ronald Reagan at Windsor Castle in 1982 and visiting his California ranch in 1983, Elizabeth was angered when his administration ordered the invasion of Grenada, one of her Caribbean realms, without informing her.
Intense media interest in the opinions and private lives of the royal family during the 1980s led to a series of sensational stories in the press, pioneered by The Sun tabloid.
Newspaper editor Donald Trelford wrote in The Observer of 21 September 1986: "The royal soap opera has now reached such a pitch of public interest that the boundary between fact and fiction has been lost sight of ... it is not just that some papers don't check their facts or accept denials: they don't care if the stories are true or not."
It was reported, most notably in The Sunday Times of 20 July 1986, that Elizabeth was worried that Margaret Thatcher's economic policies fostered social divisions and was alarmed by high unemployment, a series of riots, the violence of a miners' strike, and Thatcher's refusal to apply sanctions against the apartheid regime in South Africa.
The sources of the rumours included royal aide Michael Shea and Commonwealth secretary-general Shridath Ramphal, but Shea claimed his remarks were taken out of context and embellished by speculation.
Thatcher reputedly said Elizabeth would vote for the Social Democratic Party—Thatcher's political opponents.
Reports of acrimony between them were exaggerated, and Elizabeth gave two honours in her personal gift—membership in the Order of Merit and the Order of the Garter—to Thatcher after her replacement as prime minister by John Major.
Brian Mulroney, Canadian prime minister between 1984 and 1993, said Elizabeth was a "behind the scenes force" in ending apartheid.
In 1986, Elizabeth paid a six-day state visit to the People's Republic of China, becoming the first British monarch to visit the country.
At a state banquet, Elizabeth joked about the first British emissary to China being lost at sea with Queen Elizabeth
Elizabeth's visit also signified the acceptance of both countries that sovereignty over Hong Kong would be transferred from the United Kingdom to China in 1997.
By the end of the 1980s, Elizabeth had become the target of satire.
The involvement of younger members of the royal family in the charity game show It's a Royal Knockout in 1987 was ridiculed.
In Canada, Elizabeth publicly supported politically divisive constitutional amendments, prompting criticism from opponents of the proposed changes, including Pierre Trudeau.
As monarch of Fiji, Elizabeth supported the attempts of Governor-General Ratu Sir Penaia Ganilau to assert executive power and negotiate a settlement.
Turbulent years

In the wake of coalition victory in the Gulf War, Elizabeth became the first British monarch to address a joint meeting of the United States Congress in May 1991.
In November 1992, in a speech to mark the Ruby Jubilee of her accession, Elizabeth called 1992 her annus horribilis (a Latin phrase, meaning 'horrible year').
Republican feeling in Britain had risen because of press estimates of Elizabeth's private wealth—contradicted by the Palace—and reports of affairs and strained marriages among her extended family.
In March, her second son, Andrew, separated from his wife, Sarah; her daughter, Princess Anne, divorced Captain Mark Phillips in April; angry demonstrators in Dresden threw eggs at Elizabeth during a state visit to Germany in October; and a large fire broke out at Windsor Castle, one of her official residences, in November.
In an unusually personal speech, Elizabeth said that any institution must expect criticism, but suggested it might be done with "a touch of humour, gentleness and understanding".
Two days later, John Major announced plans to reform the royal finances, drawn up the previous year, including Elizabeth paying income tax from 1993 onwards, and a reduction in the civil list.
In December, Prince Charles and his wife, Diana, formally separated.
At the end of the year, Elizabeth sued The Sun newspaper for breach of copyright when it published the text of her annual Christmas message two days before it was broadcast.
Elizabeth's solicitors had taken successful action against The Sun five years earlier for breach of copyright after it published a photograph of her daughter-in-law the Duchess of York and her granddaughter Princess Beatrice.
In January 1994, Elizabeth broke her left wrist when a horse she was riding at Sandringham tripped and fell.
Elizabeth, who believed that she was speaking to Chrétien, said she supported Canadian unity and would try to influence Quebec's referendum on proposals to break away from Canada.
In the year that followed, public revelations on the state of Charles and Diana's marriage continued.
In consultation with her husband and John Major, as well as the Archbishop of Canterbury (George Carey) and her private secretary (Robert Fellowes), Elizabeth wrote to Charles and Diana at the end of December 1995, suggesting that a divorce would be advisable.
In August 1997, a year after the divorce, Diana was killed in a car crash in Paris.
Elizabeth was on holiday with her extended family at Balmoral.
Diana's two sons, Princes William and Harry, wanted to attend church, so Elizabeth and Philip took them that morning.
Afterwards, for five days, the royal couple shielded their grandsons from the intense press interest by keeping them at Balmoral where they could grieve in private, but the royal family's silence and seclusion, and the failure to fly a flag at half-mast over Buckingham Palace, caused public dismay.
Pressured by the hostile reaction, Elizabeth agreed to return to London and address the nation in a live television broadcast on 5 September, the day before Diana's funeral.
In the broadcast, she expressed admiration for Diana and her feelings "as a grandmother" for the two princes.
In October 1997, Elizabeth and Philip made a state visit to India, which included a controversial visit to the site of the Jallianwala Bagh massacre to pay her respects.
Protesters chanted "Killer Queen, go back", and there were demands for her to apologise for the action of British troops 78 years earlier.
At the memorial in the park, she and Philip laid a wreath and stood for a 30‐second moment of silence.
That November, the royal couple held a reception at Banqueting House to mark their golden wedding anniversary.
Elizabeth made a speech and praised Philip for his role as consort, referring to him as "my strength and stay".
In 1999, as part of the process of devolution in the United Kingdom, Elizabeth formally opened newly established legislatures for Wales and Scotland: the National Assembly for Wales at Cardiff in May, and the Scottish Parliament at Edinburgh in July.
Dawn of the new millennium

On the eve of the new millennium, Elizabeth and Philip boarded a vessel from Southwark, bound for the Millennium Dome.
During the singing of Auld Lang Syne, Elizabeth held hands with Philip and British prime minister Tony Blair.
Following the 9/11 attacks in the United States, Elizabeth, breaking with tradition, ordered the American national anthem to be played during the changing of the guard at Buckingham Palace to express her solidarity with the country.
In 2002, Elizabeth marked her Golden Jubilee, the 50th anniversary of her accession.
Her sister died in February and her mother in March, and the media speculated on whether the Jubilee would be a success or a failure.
Princess Margaret's death shook Elizabeth; her funeral was one of the rare occasions where Elizabeth openly cried.
Elizabeth again undertook an extensive tour of her realms, beginning in Jamaica in February, where she called the farewell banquet "memorable" after a power cut plunged King's House, the official residence of the governor-general, into darkness.
One million people attended each day of the three-day main Jubilee celebration in London, and the enthusiasm shown for Elizabeth by the public was greater than many journalists had anticipated.
In 2003, Elizabeth sued the Daily Mirror for breach of confidence and obtained an injunction which prevented the outlet from publishing information gathered by a reporter who posed as a footman at Buckingham Palace.
Though generally healthy throughout her life, in 2003 she had keyhole surgery on both knees.
In May 2007, citing unnamed sources, The Daily Telegraph reported that Elizabeth was "exasperated and frustrated" by the policies of Tony Blair, that she was concerned the British Armed Forces were overstretched in Iraq and Afghanistan, and that she had raised concerns over rural and countryside issues with Blair.
On 20 March 2008, at the Church of Ireland St Patrick's Cathedral, Armagh, Elizabeth attended the first Maundy service held outside England and Wales.
Elizabeth addressed the UN General Assembly for a second time in 2010, again in her capacity as Queen of all Commonwealth realms and Head of the Commonwealth.
During her visit to New York, which followed a tour of Canada, she officially opened a memorial garden for British victims of the 9/11 attacks.
Elizabeth's 11-day visit to Australia in October 2011 was her 16th visit to the country since 1954.
Diamond Jubilee and milestones

The 2012 Diamond Jubilee marked 60 years since Elizabeth's accession, and celebrations were held throughout her realms, the wider Commonwealth, and beyond.
She and Philip undertook an extensive tour of the United Kingdom, while their children and grandchildren embarked on royal tours of other Commonwealth states on her behalf.
On 18 December, the Queen became the first British sovereign to attend a peacetime Cabinet meeting since George III in 1781.
Elizabeth, who opened the Montreal Summer Olympics in 1976, also opened the 2012 Summer Olympics and Paralympics in London, making her the first head of state to open two Olympic Games in two countries.
For the London Olympics, she portrayed herself in a short film as part of the opening ceremony, alongside Daniel Craig as James Bond.
On 4 April 2013, she received an honorary BAFTA award for her patronage of the film industry and was called "the most memorable Bond girl yet" at a special presentation at Windsor Castle.
In March 2013, the Queen stayed overnight at King Edward VII's Hospital as a precaution after developing symptoms of gastroenteritis.
She was represented at the summit in Sri Lanka by Prince Charles.
On 20 April 2018, the Commonwealth heads of government announced that Charles would succeed her as Head of the Commonwealth, which the Queen stated as her "sincere wish".
On 21 December 2007, Elizabeth surpassed her great-great-grandmother, Queen Victoria, to become the longest-lived British monarch, and she became the longest-reigning British monarch and longest-reigning queen regnant and female head of state in the world on 9 September 2015.
Philip had retired from his official duties as the Queen's consort in August 2017.
Pandemic and widowhood

On 19 March 2020, as the COVID-19 pandemic hit the United Kingdom, Elizabeth moved to Windsor Castle and sequestered there as a precaution.
Public engagements were cancelled and Windsor Castle followed a strict sanitary protocol nicknamed "HMS Bubble".
On 5 April, in a televised broadcast watched by an estimated 24 million viewers in the United Kingdom, Elizabeth asked people to "take comfort that while we may have more still to endure, better days will return: we will be with our friends again; we will be with our families again; we will meet again."
Prince Philip died on 9 April 2021, after 73 years of marriage, making Elizabeth the first British monarch to reign as a widow or widower since Queen Victoria.
Due to the COVID-19 restrictions in place in England at the time, Elizabeth sat alone at Philip's funeral service, which evoked sympathy from people around the world.
It was later reported in the press that Elizabeth had rejected a government offer to relax the rules.
In her Christmas broadcast that year, which was ultimately her last, she paid a personal tribute to her "beloved Philip", saying, "That mischievous, inquiring twinkle was as bright at the end as when I first set eyes on him.
"


Despite the pandemic, Elizabeth attended the 2021 State Opening of Parliament in May, the 47th G7 summit in June, and hosted US president Joe Biden at Windsor Castle.
Biden was the 14th US president that the Queen had met.
In October 2021, Elizabeth cancelled a planned trip to Northern Ireland and stayed overnight at King Edward VII's Hospital for "preliminary investigations".
On Christmas Day 2021, while she was staying at Windsor Castle, 19-year-old Jaswant Singh Chail broke into the gardens using a rope ladder and carrying a crossbow with the aim of assassinating Elizabeth in revenge for the Amritsar massacre.
Platinum Jubilee and beyond

Elizabeth's Platinum Jubilee celebrations began on 6 February 2022, marking 70 years since her accession.
Later that month, Elizabeth fell ill with COVID-19 along with several family members, but she only exhibited "mild cold-like symptoms" and recovered by the end of the month.
She was present at the service of thanksgiving for her husband at Westminster Abbey on 29 March, but was unable to attend both the annual Commonwealth Day service that month and the Royal Maundy service in April, because of "episodic mobility problems".
(She did not attend the state openings in 1959 and 1963 as she was pregnant with Andrew and Edward, respectively.)
Later that month she made a surprise visit to Paddington Station and officially opened the Elizabeth line, named in her honour.
The Queen was largely confined to balcony appearances during the public jubilee celebrations, and she missed the National Service of Thanksgiving on 3 June.
This was the only occasion on which Elizabeth received a new prime minister at a location other than Buckingham Palace.
The Queen's last public message was issued on 7 September, in which she expressed her sympathy for those affected by the Saskatchewan stabbings.
Elizabeth did not plan to abdicate, though she took on fewer public engagements in her later years and Prince Charles performed more of her duties.
In June 2022, Elizabeth met the Archbishop of Canterbury, Justin Welby, who "came away thinking there is someone who has no fear of death, has hope in the future, knows the rock on which she stands and that gives her strength."
, Buckingham Palace stated, "Following further evaluation this morning, the Queen's doctors are concerned for Her Majesty's health and have recommended she remain under medical supervision.
The Queen remains comfortable and at Balmoral."
Elizabeth was the first monarch to die in Scotland since James V in 1542.
On 12 September, Elizabeth's coffin was carried up the Royal Mile in a procession to St Giles' Cathedral, where the Crown of Scotland was placed on it.
Her coffin lay at rest at the cathedral for 24 hours, guarded by the Royal Company of Archers, during which around 33,000 people filed past it.
On 13 September, the coffin was flown to RAF Northolt in west London, before continuing its journey by road to Buckingham Palace.
On 14 September, her coffin was taken in a military procession to Westminster Hall, where Elizabeth's body lay in state for four days.
On 16 September, Elizabeth's children held a vigil around her coffin, and the next day her eight grandchildren did the same.
Elizabeth's state funeral was held at Westminster Abbey on 19 September, marking the first time a monarch's funeral service had been held there since George II in 1760.
In Windsor, a final procession involving 1,000 military personnel took place and was witnessed by 97,000 people.
Elizabeth's fell pony and two royal corgis stood at the side of the procession.
After a committal service at St George's Chapel, Windsor Castle, Elizabeth's body was interred with her husband Philip's in the King George VI Memorial Chapel later the same day, in a private ceremony attended by her closest family members.
Public image

Beliefs, activities, and interests

Elizabeth rarely gave interviews, and little was known of her political opinions, which she did not express explicitly in public.
When Times journalist Paul Routledge asked her about the miners' strike of 1984–85 during a royal tour of the newspaper's offices, she replied that it was "all about one man" (a reference to Arthur Scargill), with which Routledge disagreed.
After the 2014 Scottish independence referendum, Prime Minister David Cameron was overheard saying that Elizabeth was pleased with the outcome.
Elizabeth had a deep sense of religious and civic duty, and took her Coronation Oath seriously.
Aside from her official religious role as supreme governor of the established Church of England, she worshipped with that church and with the national Church of Scotland.
For me the teachings of Christ and my own personal accountability before God provide a framework in which I try to lead my life.
I, like so many of you, have drawn great comfort in difficult times from Christ's words and example.
Elizabeth was patron of more than 600 organisations and charities.
The Charities Aid Foundation estimated that Elizabeth helped raise over £1.4 billion for her patronages during her reign.
Her lifelong love of corgis began in 1933 with Dookie, the first of many royal corgis.
Scenes of a relaxed, informal home life were occasionally witnessed; she and her family, from time to time, prepared a meal together and washed the dishes afterwards.
Media depiction and public opinion

In the 1950s, as a young woman at the start of her reign, Elizabeth was depicted as a glamorous "fairytale Queen".
Lord Altrincham's accusation in 1957 that her speeches sounded like those of a "priggish schoolgirl" was an extremely rare criticism.
In the late 1960s, attempts to portray a more modern image of the monarchy were made in the television documentary Royal Family and by televising Prince Charles's investiture as Prince of Wales.
Elizabeth also instituted other new practices; her first royal walkabout, meeting ordinary members of the public, took place during a tour of Australia and New Zealand in 1970.
By the end of her reign, nearly one third of Britons had seen or met Elizabeth in person.
At Elizabeth's Silver Jubilee in 1977, the crowds and celebrations were genuinely enthusiastic; but, in the 1980s, public criticism of the royal family increased, as the personal and working lives of Elizabeth's children came under media scrutiny.
Under pressure from public opinion, she began to pay income tax for the first time, and Buckingham Palace was opened to the public.
Although support for republicanism in Britain seemed higher than at any time in living memory, republican ideology was still a minority viewpoint, and Elizabeth herself had high approval ratings.
Criticism was focused on the institution of the monarchy itself, and the conduct of Elizabeth's wider family, rather than her own behaviour and actions.
Discontent with the monarchy reached its peak on the death of Diana, Princess of Wales, although Elizabeth's personal popularity—as well as general support for the monarchy—rebounded after her live television broadcast to the world five days after Diana's death.
Many republicans credited Elizabeth's personal popularity with the survival of the monarchy in Australia.
In 2010, Prime Minister Julia Gillard noted that there was a "deep affection" for Elizabeth in Australia and that another referendum on the monarchy should wait until after her reign.
Polls in Britain in 2006 and 2007 revealed strong support for the monarchy, and in 2012, Elizabeth's Diamond Jubilee year, her approval ratings hit 90 per cent.
Her family came under scrutiny again in the last few years of her life due to her son Andrew's association with convicted sex offenders Jeffrey Epstein and Ghislaine Maxwell, his lawsuit with Virginia Giuffre amidst accusations of sexual impropriety, and her grandson Harry and his wife Meghan's exit from the working royal family and subsequent move to the United States.
Polling in Great Britain during the Platinum Jubilee, however, showed support for maintaining the monarchy and Elizabeth's personal popularity remained strong.
Elizabeth was portrayed in a variety of media by many notable artists, including painters Pietro Annigoni, Peter Blake, Chinwe Chukwuogo-Roy, Terence Cuneo, Lucian Freud, Rolf Harris, Damien Hirst, Juliet Pannett and Tai-Shan Schierenberg.
Notable photographers of Elizabeth included Cecil Beaton, Yousuf Karsh, Anwar Hussein, Annie Leibovitz, Lord Lichfield, Terry O'Neill, John Swannell and Dorothy Wilding.
The first official portrait photograph of Elizabeth was taken by Marcus Adams in 1926.
Titles, styles, honours, and arms

Titles and styles

Elizabeth held many titles and honorary military positions throughout the Commonwealth, was sovereign of many orders in her own countries and received honours and awards from around the world.
In each of her realms, she had a distinct title that follows a similar formula: Queen of Saint Lucia and of Her other Realms and Territories in Saint Lucia, Queen of Australia and Her other Realms and Territories in Australia, etc.
Arms

From 21 April 1944 until her accession, Elizabeth's arms consisted of a lozenge bearing the royal coat of arms of the United Kingdom differenced with a label of three points argent, the centre point bearing a Tudor rose and the first and third a cross of Saint George.
Elizabeth also possessed royal standards and personal flags for use in the United Kingdom, Canada, Australia, New Zealand, Jamaica, and elsewhere.
Elizabeth approved her modified British arms on 26 May 1954.



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
  AssignClass (031ff5e3-80a7-4318-b6e0-0eb67fdd738f)
 Call ID: 031ff5e3-80a7-4318-b6e0-0eb67fdd738f
  Args:
    type: :Woman
    source: :Elizabeth_II
  AssignClass (61657ebb-bc2c-4f46-bc18-82fadf4a0cc7)
 Call ID: 61657ebb-bc2c-4f46-bc18-82fadf4a0cc7
  Args:
    type: :Person
    source: :Elizabeth_II
  AddLiteral (89fe0ec9-2a89-40e1-b66d-6dfe8c7235b1)
 Call ID: 89fe0ec9-2a89-40e1-b66d-6dfe8c7235b1
  Args:
    relation: :hasBirthYear
    literal_value: 1926
    literal_type: xsd:integer
    source: :Elizabeth_II
  AddLiteral (6e73982c-5189-4dcb-9883-3c93b5e314ba)
 Call ID: 6e73982c-5189-4dcb-9883-3c93b5e314ba
  Args:
    literal_value: 2022
    literal_type: xsd:integer
    source: :Elizabeth_II
    relation: :hasDeathYear
  AssignClass (c136aea9-81c1-49a8-aaba-6d91ed0518d9)
 Call ID: c136aea9-81c1-49a8-aaba-6d91ed0518d9
  Args:
    type: :Man
    source: :George_VI
  AssignClass (4cc4cd2f-9e01-4285-bf72-ebf59d5e103a)
 Call ID: 4cc4cd2f-9e01-4285-bf72-ebf59d5e103a
  Args:
    type: :Person
    source: :George_VI
  AssignClass (f2a0e3c4-312c-4f8b-9ede-4aecec06e173)
 Call ID: f2a0e3c4-312c-4f8b-9ede-4aecec06e173
  Args:
    type: :Woman
    source: :Elizabeth_the_Queen_Mother
  AssignClass (eea1fba4-5bec-47c6-8bd1-d9910544a393)
 Call ID: eea1fba4-5bec-47c6-8bd1-d9910544a393
  Args:
    type: :Person
    source: :Elizabeth_the_Queen_Mother
  AddTriple (1d868f2e-9bc3-42c3-9081-04b813770c8e)
 Call ID: 1d868f2e-9bc3-42c3-9081-04b813770c8e
  Args:
    relation: :hasFather
    source: :Elizabeth_II
    target: :George_VI
  AddTriple (39c67ec5-d099-4616-9e5e-de8079c81205)
 Call ID: 39c67ec5-d099-4616-9e5e-de8079c81205
  Args:
    relation: :hasMother
    target: :Elizabeth_the_Queen_Mother
    source: :Elizabeth_II
  AssignClass (43a76dbf-b55f-47ff-ae11-be982735d2d9)
 Call ID: 43a76dbf-b55f-47ff-ae11-be982735d2d9
  Args:
    type: :Man
    source: :George_V
  AssignClass (cf3b9daa-0de2-48b7-a684-b76a804b5727)
 Call ID: cf3b9daa-0de2-48b7-a684-b76a804b5727
  Args:
    type: :Person
    source: :George_V
  AssignClass (eb642503-8fc9-40c3-9a38-ee3e2e3ddf51)
 Call ID: eb642503-8fc9-40c3-9a38-ee3e2e3ddf51
  Args:
    type: :Woman
    source: :Queen_Mary
  AssignClass (3a575be8-97af-418a-81e2-f576ad609c9a)
 Call ID: 3a575be8-97af-418a-81e2-f576ad609c9a
  Args:
    type: :Person
    source: :Queen_Mary
  AddTriple (3c683d71-a618-47fb-afb2-8ef05fe78b12)
 Call ID: 3c683d71-a618-47fb-afb2-8ef05fe78b12
  Args:
    target: :George_V
    source: :George_VI
    relation: :hasFather
  AddTriple (c53f6574-a9eb-4011-8811-b1ba148d3f7d)
 Call ID: c53f6574-a9eb-4011-8811-b1ba148d3f7d
  Args:
    relation: :hasMother
    target: :Queen_Mary
    source: :George_VI
  AssignClass (7ab11420-7d7d-42a4-af2a-efee380c22f1)
 Call ID: 7ab11420-7d7d-42a4-af2a-efee380c22f1
  Args:
    type: :Woman
    source: :Margaret
  AssignClass (df2d7a02-cf94-4c0e-ba15-9323412fe18a)
 Call ID: df2d7a02-cf94-4c0e-ba15-9323412fe18a
  Args:
    type: :Person
    source: :Margaret
  AddTriple (8edf84c5-b415-4ae6-bafd-8e4ed5017a60)
 Call ID: 8edf84c5-b415-4ae6-bafd-8e4ed5017a60
  Args:
    target: :Elizabeth_II
    source: :Margaret
    relation: :isSisterOf
  AssignClass (7699240c-8766-4644-aac4-aa738fe23568)
 Call ID: 7699240c-8766-4644-aac4-aa738fe23568
  Args:
    type: :Man
    source: :Philip_Mountbatten
  AssignClass (8ec0a035-f221-4446-829f-5e39ff502ee2)
 Call ID: 8ec0a035-f221-4446-829f-5e39ff502ee2
  Args:
    type: :Person
    source: :Philip_Mountbatten
  AddLiteral (20ca1e3f-4ded-4d9c-8390-8bacf3dab1eb)
 Call ID: 20ca1e3f-4ded-4d9c-8390-8bacf3dab1eb
  Args:
    source: :Elizabeth_II
    literal_value: 1947
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (59362114-653e-422d-8c6e-33952917df13)
 Call ID: 59362114-653e-422d-8c6e-33952917df13
  Args:
    source: :Elizabeth_II
    target: :Philip_Mountbatten
    relation: :hasRelation
  AssignClass (e977792c-9879-432b-9ded-99f887f0e0cf)
 Call ID: e977792c-9879-432b-9ded-99f887f0e0cf
  Args:
    type: :Man
    source: :Charles
  AssignClass (f93fd26e-920e-4b2e-9f4d-324fff5862a7)
 Call ID: f93fd26e-920e-4b2e-9f4d-324fff5862a7
  Args:
    type: :Person
    source: :Charles
  AssignClass (12565bb2-2b1d-4944-98a3-dd1781373ed0)
 Call ID: 12565bb2-2b1d-4944-98a3-dd1781373ed0
  Args:
    type: :Woman
    source: :Anne
  AssignClass (640f2b46-59d8-485d-9c34-34138d208969)
 Call ID: 640f2b46-59d8-485d-9c34-34138d208969
  Args:
    type: :Person
    source: :Anne
  AssignClass (d99c17d7-e047-44ab-a4f9-dbc1da581c4f)
 Call ID: d99c17d7-e047-44ab-a4f9-dbc1da581c4f
  Args:
    type: :Man
    source: :Andrew
  AssignClass (d5343997-861f-48e1-8e83-7c7664a2e711)
 Call ID: d5343997-861f-48e1-8e83-7c7664a2e711
  Args:
    type: :Person
    source: :Andrew
  AssignClass (61d57974-1439-4890-a070-17b718bf3ab4)
 Call ID: 61d57974-1439-4890-a070-17b718bf3ab4
  Args:
    type: :Man
    source: :Edward
  AssignClass (8cefe831-180b-4e72-a5e7-bc84d8737bc8)
 Call ID: 8cefe831-180b-4e72-a5e7-bc84d8737bc8
  Args:
    type: :Person
    source: :Edward
  AddTriple (5f5195e0-327d-404e-8021-fa8a6930e074)
 Call ID: 5f5195e0-327d-404e-8021-fa8a6930e074
  Args:
    source: :Elizabeth_II
    target: :Charles
    relation: :hasChild
  AddTriple (0c9fdec8-12d8-444f-bab6-65dd7451ec6a)
 Call ID: 0c9fdec8-12d8-444f-bab6-65dd7451ec6a
  Args:
    relation: :hasChild
    target: :Anne
    source: :Elizabeth_II
  AddTriple (f1f0aeab-8b79-4e8e-8fa7-4ceb83a6b950)
 Call ID: f1f0aeab-8b79-4e8e-8fa7-4ceb83a6b950
  Args:
    relation: :hasChild
    target: :Andrew
    source: :Elizabeth_II
  AddTriple (90dc83eb-1b88-49e7-b460-c65de2d49e68)
 Call ID: 90dc83eb-1b88-49e7-b460-c65de2d49e68
  Args:
    source: :Elizabeth_II
    target: :Edward
    relation: :hasChild
  AssignClass (e5b5095e-8d42-43c3-9e84-2b98c27b8893)
 Call ID: e5b5095e-8d42-43c3-9e84-2b98c27b8893
  Args:
    type: :Man
    source: :Edward_VIII
  AssignClass (1e5a54fb-fd5e-4038-9231-ca3d55d5fff3)
 Call ID: 1e5a54fb-fd5e-4038-9231-ca3d55d5fff3
  Args:
    type: :Person
    source: :Edward_VIII
  AddTriple (3dcf6da2-35dd-4961-b19f-5cbd68b45fc2)
 Call ID: 3dcf6da2-35dd-4961-b19f-5cbd68b45fc2
  Args:
    relation: :isBrotherOf
    target: :George_VI
    source: :Edward_VIII
  AssignClass (751bd322-05f5-4af3-9ba6-6d4ad0d3c17c)
 Call ID: 751bd322-05f5-4af3-9ba6-6d4ad0d3c17c
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon
  AssignClass (9131c859-e658-48e6-a0ce-471231554f36)
 Call ID: 9131c859-e658-48e6-a0ce-471231554f36
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon
  AddTriple (456b65ff-259c-420a-b9e1-b26fa1f3b24f)
 Call ID: 456b65ff-259c-420a-b9e1-b26fa1f3b24f
  Args:
    source: :Elizabeth_the_Queen_Mother
    target: :Claude_Bowes-Lyon
    relation: :hasFather
  Finish (fbdb75a4-52e0-464a-abf4-7c3559198491)
 Call ID: fbdb75a4-52e0-464a-abf4-7c3559198491
  Args: