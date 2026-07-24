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
Princess Margaret, Countess of Snowdon (Margaret Rose; 21 August 1930 – 9 February 2002), was the younger daughter of King George VI and Queen Elizabeth the Queen Mother, and the only sibling of Queen Elizabeth II.
Margaret spent much of her childhood with her family and elder sister.
During the Second World War, the princess remained at Windsor Castle despite suggestions that she and Elizabeth should be evacuated to Canada.
Her father's death in 1952, which brought Elizabeth to the throne, marked a turning point in Margaret's life and coincided with her relationship with RAF officer Peter Townsend.
Celebrated for her glamour and social life, Margaret attracted widespread attention in the 1950s for her romance with Townsend, which she ended under pressure from government and church.
In 1960 she married photographer Antony Armstrong-Jones, later Earl of Snowdon, with whom she had two children, David and Sarah, before their divorce in 1978.
Margaret's private life, including her reputed romances and social circle, was often the subject of speculation by the press.
Early life

Margaret was born at 9:22 pm on 21 August 1930 at Glamis Castle in Scotland, her mother's ancestral home.
She was the younger daughter and second child of Prince Albert, Duke of York (later King George VI), and Elizabeth, Duchess of York (later Queen Elizabeth the Queen Mother).
Margaret was the first British prince or princess to be born in Scotland since Robert Stuart, Duke of Kintyre, in 1602.
At the time of her birth, Margaret was fourth in the line of succession to the British throne.
Her father was the second son of King George V and Queen Mary, and her mother was the youngest daughter of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne and Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne.
The Duchess of York originally wished to name her second daughter Ann Margaret, writing to Queen Mary that: "I am very anxious to call her Ann Margaret, as I think Ann of York sounds pretty, & Elizabeth and Ann go so well together."
George V disliked the name Ann but approved the alternative, Margaret Rose.
Margaret's early life was spent mainly at the Yorks' residences at 145 Piccadilly, their London town house, and at Royal Lodge in Windsor.
The family were widely regarded by the public as an ideal domestic unit, but unfounded rumours that Margaret was deaf and mute persisted until her first major public appearance at her uncle Prince George's wedding in 1934.
Margaret was educated alongside her sister, Princess Elizabeth, by their Scottish governess, Marion Crawford.
Her education was supervised largely by her mother, who, in the words of Randolph Churchill, "never aimed at bringing her daughters up to be more than nicely behaved young ladies".
When Queen Mary emphasised the importance of education, the Duchess of York replied, "I don't know what she meant.
Margaret later expressed resentment about her limited education and directed criticism towards her mother.
However, the Duchess told a friend that she "regretted" that her daughters did not go to school like other children, and the decision to employ a governess rather than send the girls to school may have been taken at the insistence of their grandfather George V. J. M. Barrie, author of Peter Pan, read stories to the sisters during their childhood.
Margaret's grandfather died in January 1936, and her uncle acceded to the throne as Edward VIII.
Less than a year later, in December 1936, Edward abdicated to marry Wallis Simpson, a twice-divorced American whom neither the Church of England nor the Dominion governments would accept as queen.
Edward's abdication obliged Margaret's father to assume the throne, and Margaret became second in line, with the title The Princess Margaret to indicate her status as a child of the sovereign.
The family moved into Buckingham Palace, where Margaret's room overlooked The Mall.
Margaret was a Brownie in the 1st Buckingham Palace Brownie Pack, formed in 1937.
At the outbreak of World War II, Margaret and Elizabeth were at Birkhall, on the Balmoral Castle estate, where they remained until Christmas 1939, enduring nights so cold that the drinking water in carafes by their bedsides froze.
They spent Christmas at Sandringham House before moving to Windsor Castle, just outside London, for much of the remainder of the war.
Lord Hailsham wrote to Winston Churchill recommending that the princesses be evacuated to the greater safety of Canada, to which their mother famously replied, "The children won't go without me.
At Windsor, the princesses staged pantomimes at Christmas in aid of the Queen's Wool Fund, which bought yarn to be knitted into military garments.
In 1940, Margaret sat beside Elizabeth during their radio broadcast for the BBC's Children's Hour, addressing children who had been evacuated from cities; Margaret spoke at the end, wishing the listeners goodnight.
Unlike other members of the royal family, Margaret was not expected to undertake public or official duties during the war.
Crawford despaired at the attention Margaret received, writing to friends: "Could you this year only ask Princess Elizabeth to your party? ...
Princess Margaret does draw all the attention and Princess Elizabeth lets her do that."
Elizabeth, however, did not mind, remarking, "Oh, it's so much easier when Margaret's there – everybody laughs at what Margaret says".
Their father described Elizabeth as his pride and Margaret as his joy.
When Elizabeth joined the Auxiliary Territorial Service in 1945, Margaret became extremely jealous, lamenting, "I was born too late!"
Post-war years

Margaret appeared on the balcony at Buckingham Palace with her family and Winston Churchill at the end of the war in 1945.
Afterwards, both Margaret and Elizabeth joined the crowds outside the palace, incognito, chanting, "We want the King, we want the Queen!"
"I remember lines of unknown people linking arms and walking down Whitehall, and all of us were swept along by tides of happiness and relief," Elizabeth later recalled.
Margaret and Elizabeth were "terrified" of being recognised, so they did their best to remain hidden in plain sight.
On 15 April 1946, Margaret was confirmed into the Church of England.
On 1 February 1947, she, Elizabeth, and their parents embarked on a state tour of Southern Africa.
The three-month visit was Margaret's first trip abroad.
She later claimed that she remembered "every minute of it", including rides on horseback taken by her and Elizabeth using horses lent by locals near the royal train.
Her chaperon on those occasions was Peter Townsend, the King's equerry, who it was noticed, could be quite sharp with Margaret.
In November 1947, Margaret was a bridesmaid at the wedding of Elizabeth and Philip Mountbatten.
Over the next three years, Elizabeth and Philip had two children, Prince Charles and Princess Anne, whose births moved Margaret further down the line of succession.
In 1950, the former royal governess, Marion Crawford, published an unauthorised biography of Elizabeth's and Margaret's childhood, The Little Princesses, in which she described Margaret's "light-hearted fun and frolics" and her "amusing and outrageous ... antics".
The Margaret Set

Around the time of Elizabeth's wedding, the press began to follow the social life of the "unconventional" Margaret and her reputation for vivacity and wit.
A young woman with "vivid blue eyes", Margaret enjoyed socialising with high society and young aristocrats, including Sharman Douglas, the daughter of the American ambassador, Lewis Williams Douglas.
A celebrated beauty known for her glamour and fashion sense, she was often featured in the press at balls, parties, and nightclubs with friends who became known as the Margaret Set.
Favoured haunts of the Margaret Set were The 400 Club, the Café de Paris, and the Mirabelle restaurant.
Anticipation of an engagement or romance between Margaret and a member of her circle was often reported.
The set also mixed with celebrities, including Danny Kaye, whom Margaret met after watching him perform at the London Palladium in February 1948; he was soon accepted by the royal social circle.
In July 1949, at a fancy-dress ball at the US ambassador's residence, Margaret performed the can-can on stage, accompanied by Douglas and 10 other costumed girls.
A press frenzy followed, with Kaye denying that he had taught Margaret the dance.
Press interest could be intrusive: during a private visit to Paris in 1951, Margaret and Prince Nicholas of Yugoslavia were followed into a nightclub by a paparazzo who photographed them until British detectives physically removed him.
In 1952, although Margaret attended parties and debutante balls with friends such as Douglas and Mark Bonham Carter, the set were seen together less frequently.
In May 1953, Margaret met singer Eddie Fisher when he performed at the Red, White, and Blue Ball; she invited him to her table and he was "invited to all sorts of parties".
Margaret fell out with him in 1957, but Fisher later claimed that the night he met her was the greatest thrill of his life.
Organised by Margaret's close friend Judy Montagu with Margaret as assistant director, it was praised for raising £10,500 for charity but criticised for its amateur performances.
As Margaret reached her late twenties unmarried, the press increasingly shifted from predicting whom she might marry to speculating that she might remain a spinster.
The press avidly discussed "the world's most eligible bachelor-girl" and her alleged romances with more than 30 bachelors, including David Mountbatten, Michael I of Romania, Dominic Elliot, Colin Tennant (later Baron Glenconner), Prince Henry of Hesse-Kassel, and future Canadian prime minister John Turner.
Her family reportedly hoped that Margaret would marry Dalkeith, but, unlike him, she had no interest in outdoor pursuits.
Billy Wallace, sole heir to a £2.8 million (about £64 million today) fortune and an old friend, was reportedly Margaret's favourite companion during the mid‐1950s.
During her 21st birthday party at Balmoral in August 1951, the press were disappointed to photograph Margaret only with Townsend, who was frequently seen in the background of royal engagements and was, to her parents, a trusted companion as Elizabeth's duties increased.
The following month, her father underwent surgery for lung cancer, and Margaret was appointed one of the Counsellors of State who undertook the King's official duties while he was incapacitated.
Her father died five months later, on 6 February 1952, and her sister acceded as Elizabeth II.
Told that a handsome war hero had arrived, the princesses met Townsend, the new equerry, on his first day at Buckingham Palace in 1944; Elizabeth reportedly told her 13‐year‐old sister, "Bad luck, he's married".
The King and Queen were fond of Townsend; the King is said to have regarded the calm and efficient war veteran as the son he never had.
He may also have been aware of Margaret's early infatuation with the non‐titled and non‐wealthy Townsend, reportedly observing the courtier reluctantly obey her instruction to carry her up the palace stairs after a party.
Townsend was so frequently near Margaret that gossip columnists overlooked him as a potential suitor.
Margaret told friends she fell in love with him during the 1947 South Africa tour, where they often went riding together.
In November 1948, they attended the inauguration of Queen Juliana of the Netherlands.
A footman recalled how the King diverted the pair's picnic plans, adding that whatever the King and Queen knew about the developing relationship, most royal staff noticed it as it was obvious to them.
Townsend said that his love for Margaret began at Balmoral in 1951, and remembered an incident that August when the princess woke him from a nap after a picnic lunch while the King watched, suggesting the King was aware.
Margaret was grief-stricken by her father's death and was prescribed sedatives to help her sleep.
She resumed attending events with her family in April and returned to royal engagements and social appearances when official mourning ended in June.
With the widowed Queen Mother, Margaret moved out of Buckingham Palace and into Clarence House in May 1953, while the new queen and her family moved into Buckingham Palace.
After George VI's death, Townsend was appointed Comptroller of the Queen Mother's household.
In June 1952, the estranged Townsends hosted Margaret, Elizabeth, and Philip, at a cocktail party at their home.
A month later, Rosemary Townsend and her new partner John de László, attended the Royal Windsor Horse Show.
It is thought the romance between Margaret and Townsend began around this time.
After the divorce was finalised in December 1952, rumours about Townsend and Margaret spread more widely; the divorce, combined with their shared grief over the King's death, likely brought them closer within the privacy of Clarence House, where Margaret had her own apartment.
Marriage proposal

Private Secretary to the Queen Sir Alan Lascelles wrote that Townsend told him he had asked Margaret to marry him shortly before Christmas 1952.
Margaret accepted and informed her sister, the Queen, whose consent was required under the Royal Marriages Act 1772.
Queen Mary had recently died, and, after the coronation of Elizabeth II, the new queen planned to tour the Commonwealth for six months.
Although foreign media speculated on Margaret and Townsend's relationship, the British press did not.
After reporters saw her plucking fluff from his coat during the coronation on 2 June 1953 – "I never thought a thing about it, and neither did Margaret", Townsend later said; "After that the storm broke" – The People first mentioned the relationship in Britain on 14 June.
With the headline "They Must Deny it NOW", the front-page article warned that "scandalous rumours about Princess Margaret are racing around the world", which it insisted were "of course, utterly untrue".
The foreign press believed that the Regency Act 1953 – which made Prince Philip regent instead of Margaret on the Queen's death – had been enacted to allow Margaret to marry Townsend, but as late as 23 July most British newspapers, except the Daily Mirror did not discuss the rumours.
Acting Prime Minister Rab Butler asked that the "deplorable speculation" cease, without naming Margaret or Townsend.
The Queen was advised by Lascelles to post Townsend abroad, but she refused and instead transferred him from the Queen Mother's household to her own, although he did not accompany Margaret as planned on a tour of Southern Rhodesia.
Churchill personally approved of "a lovely young royal lady married to a gallant young airman", but Clementine Churchill reminded him that he had made the same mistake during the abdication crisis.
The Cabinet refused to approve the marriage, and Geoffrey Fisher, Archbishop of Canterbury, did not support Margaret marrying a divorced man; opponents argued that the marriage would threaten the monarchy as Edward VIII's had.
The Church of England Newspaper stated that Margaret "is a dutiful churchwoman who knows what strong views leaders of the church hold in this matter", while the Sunday Express – which had supported Edward and Wallis – asked, "IF THEY WANT TO MARRY, WHY SHOULDN'T THEY?".
Churchill informed the Queen that both his Cabinet and the Dominion prime ministers opposed the marriage, and that Parliament would not approve a union unrecognised by the Church of England unless Margaret renounced her rights to the throne.
Philip was reportedly the most opposed to Townsend within the royal family, while Margaret's mother and sister wanted her to be happy but could not approve the marriage.
Margaret did not possess her sister's large fortune and would need her £6,000 annual civil list allowance plus the additional £15,000 Parliament had provided for her upon a suitable marriage.
She did not object to being removed from the line of succession, as the death of Elizabeth and all her children was unlikely, but parliamentary approval for the marriage would be difficult and uncertain.
At 25, Margaret would no longer require the Queen's permission under the 1772 Act; after notifying the Privy Council, she could marry in one year unless Parliament intervened.
Churchill told Elizabeth, however, that if one could easily leave the line of succession, another could easily enter it, which he considered dangerous for a hereditary monarchy.
Elizabeth told the couple to wait until 1955, when Margaret would be 25, avoiding the Queen having to publicly disapprove of her sister's marriage.
Churchill arranged for Townsend's assignment as air attaché at the British Embassy in Brussels; he was sent on 15 July 1953, before Margaret's return from Rhodesia on 30 July.
Although Margaret and Townsend knew of his new post, they had reportedly been promised a few days together before his departure.
Margaret was told by the Church that she would be unable to receive communion if she married a divorced man.
Other newspaper polls showed popular support for Margaret's personal choice, regardless of Church teaching or government.
Margaret worked with friends on charity productions of Lord and Lady Algy and The Frog, and publicly dated men such as Tennant and Wallace.
The attaché secretly travelled to Britain; while the palace was aware of one visit, he reportedly made other trips for nights and weekends with the princess at Clarence House—her apartment had its own front door—and friends' homes.
He reportedly believed that his exile from Margaret would soon end, their love was strong, and that the British people would support marrying.
The press described Margaret's 25th birthday, 21 August 1955, as the day she was free to marry, and expected an announcement about Townsend soon.
Three hundred journalists waited outside Balmoral, four times as many as those later following Diana, Princess of Wales.
"COME ON MARGARET!", the Daily Mirror's front page said two days earlier, asking her to "please make up your mind!".
On 12 October Townsend returned from Brussels as Margaret's suitor.
The royal family devised a system in which it did not host Townsend, but he and Margaret formally courted each other at dinner parties hosted by friends such as Mark Bonham Carter.
Women in the East End of London shouted "Go on, Marg, do what you want" at the princess.
"Nothing much else than Princess Margaret's affairs is being talked of in this country", The Manchester Guardian said on 15 October.
Observers interpreted Buckingham Palace's request to the press to respect Margaret's privacy—the first time the palace discussed the princess's recent personal life—as evidence of an imminent betrothal announcement, probably before the Opening of Parliament on 25 October.
As no announcement occurred—the Daily Mirror on 17 October showed a photograph of Margaret's left hand with the headline "NO RING YET!"—the press wondered why.
Margaret may have been uncertain of her desire, having written to Prime Minister Anthony Eden in August that "It is only by seeing him in this way that I feel I can properly decide whether I can marry him or not".
Margaret's authorized biographer Christopher Warwick said that the letter was evidence that her love for Townsend was not as strong as the public believed, and that she wanted only the prime minister and Elizabeth to know of her uncertainty.
Margaret may have told Townsend as early as 12 October that governmental and familial opposition to their marriage had not changed; it is possible that neither they nor Elizabeth fully understood until that year how difficult the 1772 Act made a royal marriage without the monarch's permission.
An influential 26 October editorial in The Times stating that "The QUEEN's sister married to a divorced man (even though the innocent party) would be irrevocably disqualified from playing her part in the essential royal function" represented The Establishment's view of what it considered a possibly dangerous crisis.
It convinced many, who had believed that the media were exaggerating, that Margaret really might defy the Church and royal standards.
Townsend recalled that "we felt mute and numbed at the centre of this maelstrom"; Elizabeth also wanted the media circus to end.
He wrote in his autobiography that Margaret "could have married me only if she had been prepared to give up everything – her position, her prestige, her privy purse.
Royal historian Hugo Vickers wrote that "Lascelles's separation plan had worked and the love between them had died".
Townsend was not the love of her life – the love of her life was her father, King George VI, whom she adored".
More than 100 journalists waited at Balmoral when Eden arrived to discuss the marriage with Elizabeth and Margaret on 1 October 1955.
According to a 1958 biography of Townsend by Norman Barrymaine and other accounts, Eden said that his government would oppose in Parliament Margaret retaining her royal status.
While the government could not prevent the marriage when Margaret became a private individual after a Bill of Renunciation, she would no longer be a Counsellor of State and would lose her civil list allowance; otherwise, taxpayers would subsidise a divorced man and his sons.
Eden recommended that, like her uncle Edward and his wife Wallis, Margaret and Townsend leave Britain for several years.
They show that Elizabeth and Eden (who had been divorced and remarried himself) planned to amend the 1772 Act.
Margaret would have been able to marry Townsend by removing her and any children from the marriage from the line of succession, and thus the Queen's permission would no longer be necessary.
Margaret would be allowed to keep her royal title and her allowance, stay in the country, and even continue with her public duties.
Eden described Elizabeth's attitude in a letter on the subject to the Commonwealth prime ministers as "Her Majesty would not wish to stand in the way of her sister's happiness".
Eden himself was sympathetic; "Exclusion from the Succession would not entail any other change in Princess Margaret's position as a member of the Royal Family", he wrote.
On 28 October 1955 final draft of the plan, Margaret would announce that she would marry Townsend and leave the line of succession.
As prearranged by Eden, the Queen would consult with the British and Commonwealth governments, and then ask them to amend the 1772 Act.
Kilmuir had advised Eden that the 1772 Act was flawed and might not apply to Margaret anyway.
The August letter to Eden is evidence, Warwick said, that Margaret was aware of the government's intention to preserve her title and allowance.
The decision not to marry was made on the 24th and for the following week, Margaret worked on the wording of her statement, which was released on the 31st.
Although Margaret and Townsend had read the editorial the newspaper denounced as from "a dusty world and a forgotten age", they had earlier made their decision and written an announcement.
End of relationship

On 31 October 1955, Margaret issued a statement:


I would like it to be known that I have decided not to marry Group Captain Peter Townsend.
"Thoroughly drained, thoroughly demoralized", Margaret later said, she and Townsend wrote the statement together.
She refused when Oliver Dawnay, the Queen Mother's private secretary, asked to remove the word "devotion".
The written statement, signed "Margaret", was the first official confirmation of the relationship.
Some Britons were disbelieving or angry while others, including clergy, were proud of Margaret for choosing duty and faith; newspapers were evenly divided on the decision.
The Associated Press said that Margaret's statement was almost "a rededication of her life to the duties of royalty, making unlikely any marriage for her in the near future"; the princess may have expected to never marry after the long relationship ended, because most of her eligible male friends were no longer bachelors.
Barrymaine agreed that Margaret intended the statement to mean that she would never marry, but wrote that Townsend likely did not accept any such vow to him by the princess, and his subsequent departure from Britain for two years was to not interfere with her life.
After resigning from the RAF and travelling around the world for 18 months Townsend returned in March 1958; he and Margaret met several times, but could not avoid the press ("TOGETHER AGAIN") or royal disapproval.
Townsend said during a 1970 book tour that he and Margaret did not correspond and they had not seen each other since a "friendly" 1958 meeting, "just like I think a lot of people never see their old girl friends".
Their love letters are in the Royal Archives and will not be available to the public until 100 years after Margaret's birth, August 2030.
These are unlikely to include Margaret's letters.
He claimed he complied with her wishes, but kept this letter and an envelope of burned shards of the vow she had sent, eventually destroying these also.
He was apparently unaware Margaret had already broken the pact by her engagement to Billy Wallace as it was not revealed until many years later.
In October 1993, a friend of Margaret revealed she had met Townsend for what turned out to be the last time before his death in 1995.
Margaret said that he looked "exactly the same, except he had grey hair".
They also found him disgruntled and had convinced himself that in agreeing to part, he and Margaret had set a noble example which seemed to have been in vain.
Marriage to Antony Armstrong-Jones

Margaret accepted one of Wallace's many proposals to marry in 1956, but the engagement ended before an official announcement when he admitted to a romance in the Bahamas; "I had my chance and blew it with my big mouth", Wallace said.
Margaret did not reveal this publicly until an interview and subsequent biography with Nigel Dempster in 1977.
Margaret met the photographer Antony Armstrong-Jones at a supper party in 1958.
Armstrong-Jones proposed to Margaret with a ruby engagement ring surrounded by diamonds in the shape of a rosebud.
She reportedly accepted his proposal a day after learning from Townsend that he intended to marry a young Belgian woman, Marie-Luce Jamagne, who was half his age and greatly resembled Margaret.
Margaret's announcement of her engagement, on 26 February 1960, surprised the press, as she had concealed the romance from reporters.
Margaret married Armstrong-Jones at Westminster Abbey on 6 May 1960.
The ceremony was the first royal wedding to be broadcast on television, and it attracted viewing figures of 300 million worldwide.
Margaret's wedding dress was designed by Norman Hartnell and worn with the Poltimore Tiara.
She had eight young bridesmaids, led by her niece, Princess Anne.
The Duke of Edinburgh escorted the bride, and the best man was Roger Gilliatt.
The honeymoon was a six-week Caribbean cruise aboard the royal yacht Britannia.
In 1961, Margaret's husband was created Earl of Snowdon.
The couple had two children (both born by Caesarean section at Margaret's request): David, born 3 November 1961, and Sarah, born 1 May 1964.
The marriage widened Margaret's social circle beyond the court and aristocracy to include show business celebrities and bohemians.
Lord Snowdon had a series of affairs, including with long-term mistress, Ann Hills, and Lady Jacqueline Rufus-Isaacs, daughter of the 3rd Marquess of Reading.
Anne De Courcy's 2008 biography summarises the situation with a quote from a close friend: "If it moves, he'll have it."
Reportedly, Margaret had her first extramarital affair in 1966, with her daughter's godfather Anthony Barton, a Bordeaux wine producer.
Margaret claimed that her relationship with Douglas-Home was platonic, but her letters to him (which were later sold) were intimate.
Douglas-Home, who suffered from depression, died by suicide 18 months after the split with Margaret.
According to biographer Charlotte Breese, entertainer Leslie Hutchinson had a "brief liaison" with Margaret in 1955.
A 2009 biography of actor David Niven included assertions, based on information from Niven's widow and a good friend of Niven's, that he had had an affair with Margaret, who was 20 years his junior.
In 1975, Margaret was listed among women with whom actor Warren Beatty had had romantic relationships.
John Bindon, an actor from Fulham, who had spent time in prison, sold his story to the Daily Mirror, boasting of a close relationship with Margaret.
Beyond extramarital relationships, the marriage was accompanied by drugs, alcohol, and bizarre behaviour by both parties, such as Snowdon's leaving lists of "things I hate about you" for Margaret to find between the pages of books she read.
In September 1973, Colin Tennant introduced Margaret to Roddy Llewellyn.
Margaret described their relationship as "a loving friendship".
Once, when Llewellyn left on an impulsive trip to Turkey, Margaret became emotionally distraught and took an overdose of sleeping tablets.
As she recovered, her ladies-in-waiting kept Snowdon away from her, afraid that seeing him would distress her further.
In February 1976, a picture of Margaret and Llewellyn in swimsuits on Mustique was published on the front page of a tabloid, the News of the World.
The press portrayed Margaret as a predatory older woman and Llewellyn as her toyboy lover.
On 19 March 1976, Margaret and Snowdon publicly acknowledged that their marriage had irretrievably broken down and that they had decided to separate.
Some politicians suggested removing Margaret from the civil list.
Labour MPs denounced her as "a royal parasite" and a "floosie".
In the same month, Margaret was taken ill, and diagnosed as suffering from gastroenteritis and alcoholic hepatitis, although Warwick denied that she was ever an alcoholic.
It was the first divorce of a senior member of the British royal family since that of Princess Victoria Melita of Edinburgh and Ernest Louis, Grand Duke of Hesse in 1901.
Allegedly, Margaret did not want a divorce: she tried to make her marriage succeed, but there were "too many challenges".
Devastated by the divorce, Margaret never remarried.
On 15 December 1978, Snowdon married Lucy Lindsay-Hogg, but he and Margaret remained close friends.
Margaret remained close friends with them both.
Public life

According to Margaret, her first solo public engagement was presenting a prize at the Princess Margaret Rose School in Windsor when she was 12.
Subsequently, Margaret went on multiple tours of various places; in her first major tour she joined her parents and sister for a tour of South Africa in 1947.
As colonies of the British Commonwealth of Nations sought nationhood, Margaret represented the Crown at independence ceremonies in Jamaica in 1962 and Tuvalu and Dominica in 1978.
In August 1979, Margaret's second cousin once-removed Lord Mountbatten and members of his family were killed by a bomb planted by the Provisional Irish Republican Army.
That October, while on a fundraising tour of the United States on behalf of the Royal Opera House, Margaret was seated at a dinner reception in Chicago with columnist Abra Anderson and Mayor Jane Byrne.
Margaret told them that the royal family had been moved by the many letters of condolence from Ireland.
The following day, Anderson's rival Irv Kupcinet published a claim that Margaret had referred to the Irish as "pigs".
Margaret, Anderson, and Byrne all issued immediate denials, but the damage was already done.
The rest of the tour drew demonstrations, and Margaret's security was doubled in the face of physical threats.
Charity work

Margaret's main interests were welfare charities, music and ballet.
She was president of the National Society for the Prevention of Cruelty to Children (NSPCC), the Royal Scottish Society for the Prevention of Cruelty to Children (Children 1st), and Invalid Children's Aid Nationwide (also called 'I CAN').
Margaret was president or patron of numerous organisations, such as the West Indies Olympic Association, the Girl Guides, Northern Ballet Theatre, Birmingham Royal Ballet, Scottish Ballet, Tenovus Cancer Care, the Royal College of Nursing, and the London Lighthouse (an AIDS charity that has since merged with the Terrence Higgins Trust).
In her capacity as president of the Royal Ballet, she played a key role in launching a fund for Dame Margot Fonteyn, who was experiencing financial troubles.
With the help of the Children's Royal Variety Performance, she also organised yearly fundraisers for NSPCC.
At some points Margaret was criticised for not being as active as other members of the royal family.
Illness and death

Margaret's later life was marred by illness and disability.
In January 1993, Margaret was admitted to hospital for pneumonia.
Margaret's last public appearances were at the 101st birthday celebrations of her mother in August 2001, and the 100th birthday celebration of her aunt Princess Alice, Duchess of Gloucester, that December.
Margaret died in her sleep at King Edward VII's Hospital, London, at 6:30 am on 9 February 2002, aged 71, three days after the 50th anniversary of her father's death.
Prince Charles paid tribute to his aunt in a television broadcast.
Following her death, private memorial services were held at St Mary Magdalene Church and Glamis Castle.
Margaret's coffin, draped in her personal standard, was taken from Kensington Palace to St James's Palace before her funeral.
In line with her wishes, the ceremony was a private service at St George's Chapel, Windsor Castle, for family and friends.
Unlike most other members of the royal family, she was cremated, at Slough Crematorium.
Her lady-in-waiting, Lady Glenconner, stated that Margaret found the Royal Burial Ground at Frogmore "very gloomy" and would have wanted to be where her father was buried.
Margaret's ashes were temporarily placed in the Royal Vault of St George's Chapel.
Following the Queen Mother's death seven weeks later and after her funeral, they were interred in the King George VI Memorial Chapel to rest alongside her parents.
A service of thanksgiving and remembrance for Margaret was held at Westminster Abbey on 19 April 2002.
A memorial service marking the tenth anniversary of the deaths of both Margaret and the Queen Mother was held on 30 March 2012 at St George's Chapel, Windsor Castle, attended by Queen Elizabeth II and other members of the royal family.
Legacy

Image

We thank thee Lord who by thy spirit doth our faith restore
When we with worldly things commune & prayerless close our door
We lose our precious gift divine to worship and adore
Then thou our Saviour, fill our hearts to love thee evermore


Observers often characterised Margaret as a spoiled snob capable of cutting remarks and hauteur.
Critics claimed that she even looked down on her grandmother Queen Mary because Mary was born a princess with the lower "Serene Highness" style, whereas Margaret was a "Royal Highness" by birth.
Margaret could also be charming and informal.
Marion Crawford wrote in her memoir: "Impulsive and bright remarks she made became headlines and, taken out of their context, began to produce in the public eye an oddly distorted personality that bore little resemblance to the Margaret we knew.
"


Margaret's acquaintance Gore Vidal, the American writer, wrote: "She was far too intelligent for her station in life".
He recalled a conversation with Margaret in which, discussing her public notoriety, she said: "It was inevitable, when there are two sisters and one is the Queen, who must be the source of honour and all that is good, while the other must be the focus of the most creative malice, the evil sister".
As a child, Margaret enjoyed pony shows, but unlike other family members she did not express interest in hunting, shooting, and fishing in adulthood.
Her musical choices included "Sixteen Tons" by Tennessee Ernie Ford which she said had entertained her in a traffic jam.
In 1984, she appeared as herself in an episode of the radio drama The Archers, becoming the first member of the royal family to take part in a BBC drama.
Margaret's private life was for many years the subject of intense speculation by media and royalty watchers.
Margaret was a devout Anglican her whole life, though "she had desires that often conflicted with her faith".
Following Margaret's death, her lady-in-waiting, Lady Glenconner, said that " was devoted to the Queen and tremendously supportive of her".
Margaret was described by her cousin Lady Elizabeth Shakerley as "somebody who had a wonderful capacity for giving a lot of people pleasure
Randolph Churchill believed that rumours "that Fisher had intervened to prevent the Princess from marrying Townsend has done incalculable harm to the Church of England"; a Gallup poll found that 28% agreed, and 59% disagreed, with the Church's refusal to remarry a divorced person while the other spouse was alive.
Biographer Warwick suggests that Margaret's most enduring legacy is an accidental one.
Perhaps unwittingly, Margaret paved the way for public acceptance of royal divorce.
Eden reportedly told Elizabeth in Balmoral when discussing Margaret and Townsend that, regardless of outcome, the monarchy would be damaged.
In 1995, Harold Brooks-Baker was quoted in Townsend's obituary: "In my opinion, this was the turning point to disaster for the royal family.
After Princess Margaret was denied marriage, it backfired and more or less ruined Margaret's life.
The Queen decided that from then on, anyone someone in her family wanted to marry would be more or less acceptable.
The royal family and the public now feel that they've gone too far in the other direction".
Fashion and style

During her lifetime, Margaret was considered a fashion icon.
Her fashion earned the nickname 'The Margaret Look'.
The princess, dubbed a 'royal rebel', styled herself in contrast to her sister's prim and timeless style, adopting trendy mod accessories, such as brightly coloured headscarves and glamorous sunglasses.
Margaret developed a close relationship with fashion designer Christian Dior, wearing his designs throughout her life and becoming one of his most prominent customers.
Throughout the decade, Margaret was known for wearing floral-print dresses, bold-hued ballgowns and luxurious fabrics, accessorising with diamonds, pearls, and fur stoles.
British Vogue wrote that Margaret's style 'hit her stride' in the mid-60s, where she was photographed alongside celebrities like The Beatles, Frank Sinatra and Sophia Loren.
Margaret was also known for her "magnificent" hats and headdresses, including a canary feather hat worn on a 1962 Jamaica visit and a peacock feather pillbox hat to the 1973 Royal Ascot.
Marie Claire stated that the princess "refused to compromise" on her style later in life, continuing with trends of big sleeves and strapless evening gowns.
In April 2007, an exhibition titled Princess Line – The Fashion Legacy of Princess Margaret opened at Kensington Palace, showcasing contemporary fashion from British designers such as Vivienne Westwood inspired by Margaret's legacy of style.
Christopher Bailey's Spring 2006 collection for Burberry was inspired by Margaret's look from the 1960s.
Finances

In her lifetime, Margaret's fortune was estimated to be around £20 million, with most of it being inherited from her father.
She also inherited pieces of art and antiques from Queen Mary, and Dame Margaret Greville left her £20,000 in 1943.
In 1999, her son, Lord Linley, sold his mother's Caribbean residence Les Jolies Eaux for a reported £2.4 million.
At the time of her death Margaret received £219,000 from the civil list.
In June 2006, much of Margaret's estate was auctioned by Christie's to meet the tax and, in her son's words, "normal family requirements such as educating her grandchildren", though some of the items were sold in aid of charities such as the Stroke Association.
Reportedly, Elizabeth had made it clear that the proceeds from any item that was given to her sister in an official capacity must be donated to charities.
A portrait of Margaret by Pietro Annigoni was purchased back by her son at the price of £680,000–more than three times the original estimate–once it became apparent that the sale had far exceeded expectations.
In popular culture

Actresses who have portrayed Margaret include Lucy Cohu (The Queen's Sister, 2005), Katie McGrath (The Queen, 2009), Ramona Marquez (The King's Speech, 2010), Bel Powley (A Royal Night Out, 2015), Olivia Benjamin (Father Brown, 2023), and Vanessa Kirby, Helena Bonham Carter, and Lesley Manville, who all played different stages of Margaret's life during The Crown, 2016–2023.
The young Princess Margaret was played by Beau Gadsdon.
The 2008 heist film, The Bank Job, revolves around alleged photos of Margaret.
A character, "Pantomime Princess Margaret", made regular appearances in the BBC's 1970s comedy show Monty Python's Flying Circus.



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
  AssignClass (0e6f9684-96c7-4e29-9468-c3d9d2c6d186)
 Call ID: 0e6f9684-96c7-4e29-9468-c3d9d2c6d186
  Args:
    source: :PrincessMargaret
    type: :Woman
  AssignClass (f6658da2-f67a-4d67-9315-73b02998edd9)
 Call ID: f6658da2-f67a-4d67-9315-73b02998edd9
  Args:
    type: :Person
    source: :PrincessMargaret
  AddLiteral (aa36d15b-1bb1-4d86-83bc-61f078a703ad)
 Call ID: aa36d15b-1bb1-4d86-83bc-61f078a703ad
  Args:
    relation: :hasBirthYear
    source: :PrincessMargaret
    literal_type: xsd:integer
    literal_value: 1930
  AddLiteral (33b8f5fc-eb4c-4c70-8d00-ff5275b63228)
 Call ID: 33b8f5fc-eb4c-4c70-8d00-ff5275b63228
  Args:
    relation: :hasDeathYear
    source: :PrincessMargaret
    literal_type: xsd:integer
    literal_value: 2002
  AssignClass (3556815a-e636-45d6-9de8-94e82163f7ba)
 Call ID: 3556815a-e636-45d6-9de8-94e82163f7ba
  Args:
    source: :KingGeorgeVI
    type: :Man
  AssignClass (dc97c83b-7f7b-42a7-8c84-aab552faae2a)
 Call ID: dc97c83b-7f7b-42a7-8c84-aab552faae2a
  Args:
    type: :Person
    source: :KingGeorgeVI
  AssignClass (fd9a2a62-47f1-428d-b638-b69f77461dfe)
 Call ID: fd9a2a62-47f1-428d-b638-b69f77461dfe
  Args:
    source: :QueenElizabethQueenMother
    type: :Woman
  AssignClass (9a4ce3e9-7ed1-4ab4-aeb3-5872f0939273)
 Call ID: 9a4ce3e9-7ed1-4ab4-aeb3-5872f0939273
  Args:
    type: :Person
    source: :QueenElizabethQueenMother
  AddTriple (18d8c02c-c36b-40d5-8d89-50ef503259bc)
 Call ID: 18d8c02c-c36b-40d5-8d89-50ef503259bc
  Args:
    target: :KingGeorgeVI
    relation: :hasFather
    source: :PrincessMargaret
  AddTriple (4487c98a-920f-4d7c-8dae-ce2fc8a281ba)
 Call ID: 4487c98a-920f-4d7c-8dae-ce2fc8a281ba
  Args:
    relation: :hasMother
    target: :QueenElizabethQueenMother
    source: :PrincessMargaret
  AssignClass (b3d4e0b0-d0bc-45f7-812f-c401044b5f4a)
 Call ID: b3d4e0b0-d0bc-45f7-812f-c401044b5f4a
  Args:
    source: :QueenElizabethII
    type: :Woman
  AssignClass (c7fdd209-2c74-425b-8322-a58478bad595)
 Call ID: c7fdd209-2c74-425b-8322-a58478bad595
  Args:
    type: :Person
    source: :QueenElizabethII
  AddTriple (3df288f7-fe04-41f3-86be-ef29efcb69ed)
 Call ID: 3df288f7-fe04-41f3-86be-ef29efcb69ed
  Args:
    relation: :isSisterOf
    target: :QueenElizabethII
    source: :PrincessMargaret
  AssignClass (c1e47ca6-9a01-4334-a0c5-51af412c6e7b)
 Call ID: c1e47ca6-9a01-4334-a0c5-51af412c6e7b
  Args:
    source: :KingGeorgeV
    type: :Man
  AssignClass (2aff346f-d0cc-4d8c-a078-ca6011b4110d)
 Call ID: 2aff346f-d0cc-4d8c-a078-ca6011b4110d
  Args:
    type: :Person
    source: :KingGeorgeV
  AssignClass (d58e06fb-bbdb-47d2-a7cf-fe79ca453a92)
 Call ID: d58e06fb-bbdb-47d2-a7cf-fe79ca453a92
  Args:
    source: :QueenMary
    type: :Woman
  AssignClass (2f54b883-cff4-4747-993a-e88619a9cc5f)
 Call ID: 2f54b883-cff4-4747-993a-e88619a9cc5f
  Args:
    source: :QueenMary
    type: :Person
  AddTriple (409dbdc3-cd2a-4f64-bf3d-ca6b485ba0a8)
 Call ID: 409dbdc3-cd2a-4f64-bf3d-ca6b485ba0a8
  Args:
    source: :KingGeorgeVI
    target: :KingGeorgeV
    relation: :hasFather
  AddTriple (0f802e62-518b-47dd-877f-93d548c51370)
 Call ID: 0f802e62-518b-47dd-877f-93d548c51370
  Args:
    target: :QueenMary
    relation: :hasMother
    source: :KingGeorgeVI
  AssignClass (334b0a34-0f2d-41b2-b433-3c9aa90fa294)
 Call ID: 334b0a34-0f2d-41b2-b433-3c9aa90fa294
  Args:
    source: :ClaudeBowesLyon
    type: :Man
  AssignClass (0715b723-0e1a-4eed-913b-5f1e83618cb3)
 Call ID: 0715b723-0e1a-4eed-913b-5f1e83618cb3
  Args:
    source: :ClaudeBowesLyon
    type: :Person
  AssignClass (960811f1-6c07-4df3-971d-1c1c2bea0165)
 Call ID: 960811f1-6c07-4df3-971d-1c1c2bea0165
  Args:
    source: :CeciliaBowesLyon
    type: :Woman
  AssignClass (84260f18-25a1-4a68-812f-defa99907b61)
 Call ID: 84260f18-25a1-4a68-812f-defa99907b61
  Args:
    type: :Person
    source: :CeciliaBowesLyon
  AddTriple (47448c57-9323-4e96-878d-d322b4ec61db)
 Call ID: 47448c57-9323-4e96-878d-d322b4ec61db
  Args:
    source: :QueenElizabethQueenMother
    target: :ClaudeBowesLyon
    relation: :hasFather
  AddTriple (37f57c11-50a6-423e-8425-592cedefe4a2)
 Call ID: 37f57c11-50a6-423e-8425-592cedefe4a2
  Args:
    source: :QueenElizabethQueenMother
    relation: :hasMother
    target: :CeciliaBowesLyon
  AssignClass (c19fa0b6-c2f4-458b-82c8-eb8ef8dace94)
 Call ID: c19fa0b6-c2f4-458b-82c8-eb8ef8dace94
  Args:
    source: :AntonyArmstrongJones
    type: :Man
  AssignClass (5aa965ba-834a-41c1-ae0a-2a0435a636e6)
 Call ID: 5aa965ba-834a-41c1-ae0a-2a0435a636e6
  Args:
    source: :AntonyArmstrongJones
    type: :Person
  AddTriple (cc601f30-acc6-4186-8a01-86dbcffc532f)
 Call ID: cc601f30-acc6-4186-8a01-86dbcffc532f
  Args:
    source: :PrincessMargaret
    target: :AntonyArmstrongJones
    relation: :hasMarriageYear
  AddLiteral (a1ce5ad1-1a48-49f6-ae44-bb41a6703e41)
 Call ID: a1ce5ad1-1a48-49f6-ae44-bb41a6703e41
  Args:
    literal_type: xsd:integer
    source: :PrincessMargaret
    relation: :hasMarriageYear
    literal_value: 1960
  AssignClass (c9437ea0-54fa-4e14-b63e-1bdb662d7ddd)
 Call ID: c9437ea0-54fa-4e14-b63e-1bdb662d7ddd
  Args:
    type: :Man
    source: :DavidArmstrongJones
  AssignClass (32573bf9-7484-4e72-93a8-27bc226ebaf6)
 Call ID: 32573bf9-7484-4e72-93a8-27bc226ebaf6
  Args:
    source: :DavidArmstrongJones
    type: :Person
  AssignClass (5ac8aef9-bd5d-4ae0-a8ac-d262527e08fd)
 Call ID: 5ac8aef9-bd5d-4ae0-a8ac-d262527e08fd
  Args:
    source: :SarahArmstrongJones
    type: :Woman
  AssignClass (d40759e4-3a9f-4743-b9d3-0a86a1f7275a)
 Call ID: d40759e4-3a9f-4743-b9d3-0a86a1f7275a
  Args:
    source: :SarahArmstrongJones
    type: :Person
  AddTriple (a0009282-11e6-4c10-a594-dd416331c190)
 Call ID: a0009282-11e6-4c10-a594-dd416331c190
  Args:
    source: :PrincessMargaret
    relation: :hasSon
    target: :DavidArmstrongJones
  AddTriple (19a300e6-c663-4104-a5d9-bac212968dfc)
 Call ID: 19a300e6-c663-4104-a5d9-bac212968dfc
  Args:
    source: :PrincessMargaret
    target: :SarahArmstrongJones
    relation: :hasDaughter
  AddTriple (80302040-76f1-4826-a521-2bb9bd959c2c)
 Call ID: 80302040-76f1-4826-a521-2bb9bd959c2c
  Args:
    source: :DavidArmstrongJones
    target: :AntonyArmstrongJones
    relation: :hasFather
  AddTriple (9387e7fe-416a-40d2-8133-3957ca9ec92e)
 Call ID: 9387e7fe-416a-40d2-8133-3957ca9ec92e
  Args:
    source: :SarahArmstrongJones
    relation: :hasFather
    target: :AntonyArmstrongJones
  Finish (f685463a-9dab-40c8-bccf-65eb10775184)
 Call ID: f685463a-9dab-40c8-bccf-65eb10775184
  Args: