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
Edward VIII (Edward Albert Christian George Andrew Patrick David; 23 June 1894 – 28 May 1972), later known as the Duke of Windsor, was King of the United Kingdom and the British Dominions, and Emperor of India, from 20 January 1936 until his abdication in December of the same year.
Edward was born during the reign of his great-grandmother Queen Victoria as the eldest child of the Duke and Duchess of York, later King George V and Queen Mary.
As a young man, Edward served in the British Army during the First World War and undertook several overseas tours on behalf of his father.
Upon his father's death in 1936, Edward became the second monarch of the House of Windsor.
Only months into his reign, Edward caused a constitutional crisis through his proposal to marry Wallis Simpson, an American who had divorced her first husband and was seeking a divorce from her second.
Additionally, such a marriage would have conflicted with Edward's status as titular head of the Church of England, which, at the time, disapproved of remarriage after divorce if a former spouse was still alive.
Edward knew the Baldwin government would resign if the marriage went ahead, which could have forced a general election and would have ruined his status as a politically neutral constitutional monarch.
He was succeeded by his younger brother, George VI.
With a reign of 326 days, Edward was one of the shortest-reigning British monarchs to date, and is the most recent British monarch to abdicate.
After his abdication, Edward was created Duke of Windsor.
He married Simpson in France on 3 June 1937, after her second divorce became final.
During the Second World War, Edward was at first stationed with the British Military Mission to France.
After the war, Edward spent the rest of his life in France.
Early life

Edward was born at 10:00 pm on 23 June 1894 at White Lodge, Richmond Park, on the outskirts of London, during the reign of his great-grandmother, Queen Victoria.
He was the eldest son of the Duke and Duchess of York (later King George V and Queen Mary).
His father was the son of the Prince and Princess of Wales (later King Edward VII and Queen Alexandra) and his mother was the eldest daughter of Princess Mary Adelaide of Cambridge and Francis, Duke of Teck.
Edward was baptised Edward Albert Christian George Andrew Patrick David in the Green Drawing Room of White Lodge on 16 July by Edward White Benson, Archbishop of Canterbury.
The name Edward was chosen in honour of Edward's late uncle Prince Albert Victor, Duke of Clarence and Avondale, who was known within the family as "Eddy" (Edward being among his given names); Albert was included at the behest of Queen Victoria for her late husband Albert, Prince Consort; Christian was in honour of his great-grandfather King Christian IX of Denmark; and the last four names – George, Andrew, Patrick and David – came from, respectively, the patron saints of England, Scotland, Ireland and Wales.
As was common practice among upper-class families of the period, Edward and his younger siblings were brought up by nannies rather than directly by their parents.
One of Edward's early nannies frequently mistreated him by pinching him before he was due to be presented to his parents.
His resulting crying and distress would prompt the Duke and Duchess to send him and the nanny away.
Edward's father, though a harsh disciplinarian, was demonstratively affectionate, and his mother displayed a playful side with her children that belied her austere public image.
Education

Initially, Edward was tutored at home by Hélène Bricka.
When his parents travelled the British Empire for almost nine months following the death of Queen Victoria in 1901, Edward and his siblings remained in Britain with their grandparents, Queen Alexandra and King Edward VII, who showered them with affection.
Upon his parents' return, Edward was placed under the care of two men, Frederick Finch and Henry Hansell, who virtually brought up Edward and his siblings for the rest of their nursery years.
Edward stayed under Hansell's strict tutorship until he was almost 13.
He took the examination for entry to the Royal Naval College, Osborne, and began there in 1907.
Hansell had wanted Edward to enter school earlier, but the prince's father disagreed.
After two years at Osborne College, which he did not enjoy, Edward moved on to the Royal Naval College at Dartmouth.
A two-year course, followed by entry into the Royal Navy, was planned.
Upon the death of Edward VII, Edward's father ascended the throne as George V, and Edward himself became heir apparent.
Prince of Wales

Edward automatically became Duke of Cornwall and Duke of Rothesay on 6 May 1910 upon his father's accession.
He was created, by letters patent, Prince of Wales and Earl of Chester a month later, on 23 June 1910, his 16th birthday.
Edward was officially invested as Prince of Wales in a special ceremony at Caernarfon Castle on 13 July 1911.
The investiture took place in Wales at the instigation of the Welsh politician David Lloyd George, Constable of the Castle and Chancellor of the Exchequer in the Liberal government.
Lloyd George devised a rather fanciful ceremony in the style of a Welsh pageant and coached Edward to speak a few words in Welsh.
When the First World War broke out in 1914, Edward had reached the minimum age for active service and was keen to participate.
Edward visited frontline trenches several times, for which he was awarded the Military Cross in 1916.
Edward's youngest brother, Prince John, died at the age of 13 on 18 January 1919 after a severe epileptic seizure.
Edward, who was eleven years older than John and had hardly known him, saw his death as "little more than a regrettable nuisance".
"


In 1919, Edward agreed to serve as president of the organising committee for the proposed British Empire Exhibition at Wembley Park, Middlesex.
He wished the Exhibition to include "a great national sports ground", and so played a part in the creation of Wembley Stadium.


Throughout the 1920s, Edward, as Prince of Wales, represented his father at home and overseas on many occasions.
During his 1924 visit to the United States, Men's Wear magazine observed that, "The average young man in America is more interested in the clothes of the Prince of Wales than in any other individual on earth.
"


Edward visited poverty-stricken areas of Britain, and undertook sixteen tours to various parts of the Empire between 1919 and 1935.
Named the E. P. Ranch (for Edward, Prince), he attempted unsuccessfully to develop it for the breeding of animals, including Shorthorn cattle, Dartmoor ponies, and Clydesdale horses.
Edward's November 1921 visit to India came during the non-cooperation movement protests for Indian self-rule and was marked by riots in Bombay.
From January to April 1931, the Prince of Wales and his brother Prince George travelled 18,000 miles (29,000 km) on a tour of South America, steaming out on the ocean liner Oropesa, and returning via Paris and an Imperial Airways flight from Paris–Le Bourget Airport that landed specially in Windsor Great Park.
Though widely travelled, Edward shared a then-common racial prejudice against foreigners and many of the Empire's subjects, believing that whites were inherently superior.
"


Romances

Before the First World War, a royal match between Edward and his second cousin, Princess Victoria Louise of Prussia, was suggested.
Nothing came of it, and Victoria Louise married Edward's first cousin once removed, Ernest Augustus, Duke of Brunswick.
In 1934, Adolf Hitler, seeking to forge a link between the British and German royal houses, asked Victoria Louise to arrange a marriage between the 40-year-old Edward and her 17-year-old daughter, Frederica of Hanover, who was then at boarding school in England.
By 1917, Edward liked to spend time partying in Paris while on leave from his regiment on the Western Front.
After about a year, Edward ended the affair.
Desperate efforts were made by the Royal Household to ensure that Edward's name was not mentioned in connection with the trial or Alibert.
Also in 1917, Edward began a relationship with Lady Rosemary Leveson-Gower, the youngest daughter of the 4th Duke of Sutherland.
According to Leveson-Gower's friends, Edward proposed to her, but the relationship ended when the King and Queen expressed their disapproval of certain relatives of hers, namely Daisy, Countess of Warwick, a maternal aunt, and the 5th Earl of Rosslyn, a maternal uncle.
Edward's womanising and reckless behaviour during the 1920s and 1930s worried Prime Minister Stanley Baldwin, King George V, and those close to the prince.
"After I am dead," George said, "the boy will ruin himself in twelve months.
"


George V favoured his second son Albert ("Bertie") and Albert's daughter Elizabeth ("Lilibet"), later King George VI and Queen Elizabeth II respectively.
He told a courtier, "I pray to God that my eldest son will never marry and have children, and that nothing will come between Bertie and Lilibet and the throne."
In 1929, Time magazine reported that Edward teased Albert's wife, also named Elizabeth (later the Queen Mother), by calling her "Queen Elizabeth".
The magazine asked whether "she did not sometimes wonder how much truth there is in the story that he once said he would renounce his rights upon the death of George V – which would make her nickname come true".
In 1930, the King gave Edward the lease of Fort Belvedere in Windsor Great Park.
Wallis Simpson and the Prince of Wales, it is generally accepted, became lovers while Lady Furness was travelling abroad, although Edward adamantly insisted to his father that he was not having an affair with her and that it was not appropriate to describe her as his mistress.
Edward's relationship with Simpson, however, further strained his already poor relationship with his father.
Edward's affair with an American divorcée caused such grave concern that the couple were followed by members of the Metropolitan Police Special Branch, who examined in secret the nature of their relationship.
Reign

George V died on 20 January 1936, and Edward ascended the throne as Edward VIII.
Edward caused unease in government circles with actions that were interpreted as interference in political matters.
Government ministers were reluctant to send confidential documents and state papers to Fort Belvedere because it was clear that Edward was paying little attention to them, and it was feared that Simpson and other house guests might read them, improperly or inadvertently revealing government secrets.
Edward's unorthodox approach to his role also extended to the coinage that bore his image.
Edward insisted that he face left (as his father had done), to show the parting in his hair.
When George VI succeeded to the throne, he also faced left to maintain the tradition by suggesting that, had any further coins been minted featuring Edward's portrait, they would have shown him facing right.
On 16 July 1936, George Andrew McMahon produced a loaded revolver as Edward rode on horseback at Constitution Hill, near Buckingham Palace.
McMahon alleged at his trial that "a foreign power" had approached him to kill Edward, that he had informed MI5 of the plan, and that he was merely seeing the plan through to help MI5 catch the real culprits.
In August and September, Edward and Simpson cruised the Eastern Mediterranean on the steam yacht Nahlin.
Although gossip about his affair was widespread in the United States, the British media kept silent voluntarily, and the general public knew nothing until early December.
, Edward invited Prime Minister Stanley Baldwin to Buckingham Palace and expressed his desire to marry Simpson when she became free to remarry.
As king, Edward was the titular head of the Church, and the clergy expected him to uphold its teachings.
The Archbishop of Canterbury, Cosmo Gordon Lang, was vocal in insisting that Edward must go.
Edward proposed an alternative solution of a morganatic marriage, in which he would remain king but Simpson would not become queen consort.
Their views were sought pursuant to the Statute of Westminster 1931, which provided in part that "any alteration in the law touching the Succession to the Throne or the Royal Style and Titles shall hereafter require the assent as well of the Parliaments of all the Dominions as of the Parliament of the United Kingdom."
Faced with this opposition, Edward initially responded that there were "not many people in Australia" and that their opinion did not matter.
Edward informed Baldwin that he would relinquish the throne if he could not marry Simpson.
It was clear that Edward was not prepared to give up Simpson, and he knew that if he married against the advice of his ministers, he would cause the government to resign, prompting a constitutional crisis.
Edward duly signed the instruments of abdication at Fort Belvedere on 10 December 1936 in the presence of his younger brothers: Prince Albert, Duke of York, next in line for the throne; Prince Henry, Duke of Gloucester; and Prince George, Duke of Kent.
The next day, the last act of his reign was the royal assent to His Majesty's Declaration of Abdication Act 1936.
On the night of 11 December 1936, Edward, now reverted to the title and style of a prince, explained his decision to abdicate in a worldwide BBC radio broadcast.
Edward departed Britain for Austria the following day; he was unable to join Simpson until her divorce became absolute several months later.
The Duke of York succeeded to the throne as George VI.
Accordingly, George VI's elder daughter, Princess Elizabeth, became heir presumptive.
Duke of Windsor

On 12 December 1936, at the accession meeting of the British Privy Council, George VI announced his intention to make his brother the "Duke of Windsor" with the style of Royal Highness.
During the interim, Edward was known as the Duke of Windsor.
George's decision to create Edward a royal duke ensured that he could neither stand for election to the British House of Commons nor speak on political subjects in the House of Lords.
Letters Patent dated 27 May 1937 re-conferred the "title, style, or attribute of Royal Highness" upon the Duke, but specifically stated that "his wife and descendants, if any, shall not hold said title or attribute".
Some British ministers advised that the reconfirmation was unnecessary, since Edward had retained the style automatically, and further that Simpson would automatically obtain the rank of wife of a prince with the style Her Royal Highness; others maintained that he had lost all royal rank and should no longer carry any royal title or style as an abdicated king, and should instead be referred to simply as "Mr Edward Windsor".
On 14 April 1937, Sir Donald Somervell, the Attorney General for England and Wales, submitted to Sir John Simon, the Home Secretary, a memorandum summarising the views of Lord Advocate T. M. Cooper, Parliamentary Counsel Sir Granville Ram, and himself:
Wedding

The Duke married Simpson, who had changed her name by deed poll to Wallis Warfield (her birth surname), in a private ceremony on 3 June 1937, at Château de Candé, near Tours, France.
When the Church of England refused to sanction the union, a County Durham clergyman, Robert Anderson Jardine (Vicar of St Paul's, Darlington), offered to perform the ceremony, and Edward accepted.
George VI forbade members of the royal family to attend, to the enduring resentment of the Duke and Duchess of Windsor.
Edward had particularly wished his brothers, the Dukes of Gloucester and Kent, and his second cousin Lord Louis Mountbatten, to attend the ceremony.
The denial of the style Royal Highness to the Duchess of Windsor caused further conflict, as did the financial settlement.
The Government declined to include the Duke or Duchess on the Civil List, and the Duke's allowance was paid personally by George VI.
Edward compromised his position with his brother by concealing his full financial worth when they informally agreed upon the amount of the annual allowance.
Edward had accumulated wealth over the previous twenty-six years from the revenues of the Duchy of Cornwall, paid to him as Prince of Wales, which was ordinarily at the disposal of the incoming monarch.
George also purchased Sandringham House and Balmoral Castle from Edward; both were Edward's personal property, inherited from his father, and thus did not automatically pass to George VI on his accession.
Edward received approximately £300,000 (equivalent to between £23.8 million and £173 million in 2024) for both residences, which was paid to him in yearly instalments.
In the early days of George VI's reign, Edward telephoned daily, importuning for money and urging that Wallis be granted the style of Royal Highness, until the harassed king ordered that the calls not be put through.
Relations between the Duke of Windsor and the rest of the royal family remained strained for decades.
Edward had assumed that he would settle in Britain after a year or two of exile in France.
King George VI (with the support of Queen Mary and his wife Queen Elizabeth) threatened to cut off Edward's allowance if he returned to Britain without an invitation.
Edward became embittered toward his mother, Queen Mary, writing to her in 1939: " destroy the last vestige of feeling I had left for you ...  made further normal correspondence between us impossible.
"


1937 tour of Germany

In October 1937, the Duke and Duchess visited Nazi Germany, against the advice of the British government, and met Adolf Hitler at his Berghof retreat in Bavaria.
During it, Edward gave full Nazi salutes.
In Germany, "they were treated like royalty ... members of the aristocracy would bow and curtsy towards her, and she was treated with all the dignity and status that the duke always wanted", according to royal biographer Andrew Morton in a 2016 BBC interview.
The former Austrian ambassador Count Albert von Mensdorff-Pouilly-Dietrichstein, who was also a second cousin once removed and friend of George V, believed that Edward favoured German fascism as a bulwark against communism, and even that he initially favoured an alliance with Germany.
According to the Duke of Windsor, the experience of "the unending scenes of horror" during the First World War led him to support appeasement.
Hitler considered Edward to be friendly towards Germany and thought that Anglo-German relations could have been improved through Edward had it not been for the abdication.
The Duke and Duchess settled in Paris, leasing a mansion in Boulevard Suchet  from late 1938.
Second World War

In May 1939, Edward was commissioned by NBC to give a radio broadcast (his first since abdicating) during a visit to the First World War battlefields of Verdun.
It was transmitted outside the United States on shortwave radio and was reported in full by British broadsheet newspapers.
On the outbreak of the Second World War in September 1939, the Duke and Duchess were brought back to Britain by Louis Mountbatten on board HMS Kelly, and Edward, although he held the rank of field marshal, was made a major-general attached to the British Military Mission in France.
In February 1940, the German ambassador in The Hague, Count Julius von Zech-Burkersroda, claimed that Edward had leaked the Allied war plans for the defence of Belgium, which the Duke later denied.
Under the code name Operation Willi, Nazi agents, principally Walter Schellenberg, plotted unsuccessfully to persuade the Duke to leave Portugal and return to Spain, kidnapping him if necessary.
Churchill threatened Edward with a court-martial if he did not return to British soil.
In July 1940, Edward was appointed governor of the Bahamas.
The Duke and Duchess left Lisbon on 1 August aboard the American Export Lines steamship Excalibur, which was specially diverted from its usual direct course to New York City so that they could be dropped off at Bermuda on the 9th.
Edward did not enjoy being governor and privately referred to the islands as "a third-class British colony".
The British Foreign Office strenuously objected when Edward and Wallis planned to cruise aboard a yacht belonging to Swedish magnate Axel Wenner-Gren, whom British and American intelligence wrongly believed to be a close friend of Luftwaffe commander Hermann Göring.
Edward was praised for his efforts to combat poverty on the islands.
He was "considerably more enlightened in his attitudes than the majority of Bahamian whites, or either of his predecessors", and had an "excellent relationship" with Black individuals such as jazz musician Bert Cambridge (later elected to the Bahamian House of Assembly, to Edward's delight) and valet Sydney Johnson, whom Edward retained for thirty years and was said to have "loved as a son".
Edward maintained a long-standing dispute with Étienne Dupuch, the editor of the Nassau Daily Tribune, writing privately at one point that Dupuch was "more than half Negro, and due to the peculiar mentality of this Race, they seem unable to rise to prominence without losing their equilibrium".
But even Dupuch praised Edward for his resolution of civil unrest over low wages in Nassau in 1942, though Edward blamed the trouble on "mischief makers – communists" and "men of Central European Jewish descent, who had secured jobs as a pretext for obtaining a deferment of draft".
Many historians have suggested that Hitler was prepared to reinstate Edward as king in the hope of establishing a fascist puppet government in Britain after Operation Sea Lion.
It is widely believed that the Duke and Duchess sympathised with fascism before and during the Second World War, and were moved to the Bahamas to minimise their opportunities to act on those feelings.
During the occupation of France, the Duke asked the German Wehrmacht forces to place guards at his Paris and Riviera homes; they did so.
In December 1940, Edward gave Fulton Oursler of Liberty magazine an interview at Government House in Nassau.
The interview was published on 22 March 1941, and in it Edward was reported to have said that "Hitler was the right and logical leader of the German people" and that the time was coming for President Roosevelt to mediate a peace settlement.
Edward protested that he had been misquoted and misinterpreted.
The Allies became sufficiently disturbed by German plots revolving around Edward that President Roosevelt ordered covert surveillance of the Duke and Duchess when they visited Palm Beach, Florida, in April 1941.
Duke Carl Alexander of Württemberg (then a monk in an American monastery) had told the Federal Bureau of Investigation that Wallis had slept with the German ambassador in London, Joachim von Ribbentrop, in 1936; had remained in constant contact with him; and had continued to leak secrets.
Author Charles Higham claimed that Anthony Blunt, an MI5 agent and Soviet spy, acting on orders from the British royal family, made a successful secret trip to Schloss Friedrichshof in Allied-occupied Germany towards the end of the war to retrieve sensitive letters between the Duke of Windsor and Hitler and other leading Nazis.
What is certain is that George VI sent the Royal Librarian, Owen Morshead, accompanied by Blunt – then working part-time in the Royal Library as well as for British intelligence – to Friedrichshof in March 1945 to secure papers relating to Victoria, German Empress, the eldest child of Queen Victoria.
The papers rescued by Morshead and Blunt, and those returned by the American authorities from Chicago, were deposited in the Royal Archives.
Documents, since titled the Marburg Files, recovered by US troops in Marburg, Germany, in May 1945, include key material that relates directly to theories of Edward's Nazi sympathies.
After the war, Edward admitted in his memoirs that he admired the Germans, but he denied being pro-Nazi.
In the 1950s, journalist Frank Giles heard the Duke blame British foreign secretary Anthony Eden for helping to "precipitate the war through his treatment of Mussolini ... that's what  did, he helped to bring on the war ... and of course Roosevelt and the Jews".
During the 1960s, in private, Edward reportedly said to a friend, Patrick Balfour, 3rd Baron Kinross, "I never thought Hitler was such a bad chap.
"


Later life

At the end of the war, the couple returned to France and spent the remainder of their lives essentially in retirement, as Edward never again held an official role.
Letters written by Kenneth de Courcy to the Duke, dated between 1946 and 1949 and published in extract form in 2009, suggest a scheme in which Edward would return to England and place himself in a position for a possible regency.
The health of George VI was failing and de Courcy was concerned about the influence of the Mountbatten family over the young Princess Elizabeth.
De Courcy proposed that Edward should buy a working agricultural estate within easy reach of London in order to gain favour with the British public and make himself available should the King become incapacitated.
The Duke, however, hesitated, and the King recovered from his surgery.
De Courcy also mentioned the possibility of the British occupation zone in Germany becoming a kingdom with Edward as its monarch.
Edward's allowance was supplemented by government favours and illegal currency trading.
The City of Paris provided the Duke with a house at 4 route du Champ d'Entraînement, on the Neuilly-sur-Seine side of the Bois de Boulogne, for a nominal rent.
In 1951, Edward produced a memoir, A King's Story ghost-written by Charles Murphy, in which he expressed disagreement with liberal politics.
The royalties from the book added to Edward and Wallis's income.
Edward and Wallis effectively took on the role of celebrities and were regarded as part of café society in the 1950s and 1960s.
They hosted parties and shuttled between Paris and New York; Gore Vidal, who met the Windsors socially, reported on the vacuity of the Duke's conversation.
In June 1953, instead of attending the coronation of Queen Elizabeth II, his niece, in London, Edward and Wallis watched the ceremony on television in Paris.
Edward said that it was contrary to precedent for a sovereign or former sovereign to attend the coronation of another.
The couple appeared on Edward R. Murrow's television-interview show Person to Person in 1956, and in a 50-minute BBC television interview in 1970.
On 4 April of that year President Richard Nixon invited them as guests of honour to a dinner at the White House with Chief Justice Warren E. Burger, Charles Lindbergh, Alice Roosevelt Longworth, Arnold Palmer, George H. W. Bush, and Frank Borman.
The royal family never fully accepted the Duchess.
Queen Mary refused to receive her formally.
Edward, however, sometimes met his mother and his brother, George VI; he attended George's funeral in 1952.
Mary remained angry with Edward and indignant over his marriage to Wallis: "To give up all this for that", she said.
In 1965, the Duke and Duchess returned to London.
They were visited by his niece Elizabeth II, his sister-in-law Princess Marina, Duchess of Kent, and his sister Mary, Princess Royal and Countess of Harewood.
A week later, the Princess Royal died, and they attended her memorial service.
In 1966, Edward gave the journalist Georg Stefan Troller a ZDF TV interview in German; he answered questions about his abdication.
In 1967, the Duke and Duchess joined the royal family for the centenary of Queen Mary's birth.
The last royal ceremony Edward attended was the funeral of Princess Marina in 1968.
He declined an invitation from Elizabeth II to attend the investiture of Charles, Prince of Wales, in 1969, replying that Charles would not want his "aged great-uncle" there.
In the 1960s, Edward's health deteriorated.
Michael E. DeBakey operated on him in Houston for an aneurysm of the abdominal aorta in December 1964, and Sir Stewart Duke-Elder treated a detached retina in his left eye in February 1965.
In late 1971, Edward, who had been a smoker from an early age, was diagnosed with throat cancer and underwent cobalt therapy.
On 18 May 1972, Queen Elizabeth II visited the Duke and Duchess of Windsor while on a state visit to France; she met Edward alone for 15 minutes, but only Wallis appeared with the royal party for a photocall, which included Prince Philip and Prince Charles, as Edward was too ill.
Death and legacy

Edward died at his home in Paris on 28 May 1972, aged 77, ten days after Elizabeth's visit.
His body was returned to Britain, lying in state at St George's Chapel, Windsor Castle.
The funeral service took place in the chapel on 5 June in the presence of the Queen, the royal family, and the Duchess of Windsor, who stayed at Buckingham Palace during her visit.
He was buried in the Royal Burial Ground behind the Royal Mausoleum of Queen Victoria and Prince Albert at Frogmore.
Until a 1965 agreement with the Queen, the Duke and Duchess had planned for a burial in a cemetery plot they had purchased at Green Mount Cemetery in Baltimore, where Wallis's father was interred.
To modern sensibilities, the religious restrictions that prevented Edward from continuing as king while planning to marry Wallis Simpson "seem, wrongly, to provide insufficient explanation" for his abdication.
Titles, honours and arms

Edward's coat of arms as the Prince of Wales was the royal coat of arms of the United Kingdom, differenced with a label of three points argent, with an inescutcheon representing Wales surmounted by a coronet.
As Sovereign, he bore the royal arms undifferenced.



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
  AssignClass (4386aa05-ac03-48b7-a541-97be2b25ca95)
 Call ID: 4386aa05-ac03-48b7-a541-97be2b25ca95
  Args:
    type: :Man
    source: :EdwardVIII
  AssignClass (0bb51535-81ad-46e9-83b2-ea7e32688418)
 Call ID: 0bb51535-81ad-46e9-83b2-ea7e32688418
  Args:
    type: :Person
    source: :EdwardVIII
  AddLiteral (f55379e2-1951-4b21-8bd3-221650412c39)
 Call ID: f55379e2-1951-4b21-8bd3-221650412c39
  Args:
    relation: :hasBirthYear
    literal_value: 1894
    source: :EdwardVIII
    literal_type: xsd:integer
  AddLiteral (30c0cd89-e44c-4cf9-b8b0-bfd7e7015311)
 Call ID: 30c0cd89-e44c-4cf9-b8b0-bfd7e7015311
  Args:
    relation: :hasDeathYear
    source: :EdwardVIII
    literal_value: 1972
    literal_type: xsd:integer
  AddLiteral (d900f53c-f765-45c3-a4d4-37869201a08a)
 Call ID: d900f53c-f765-45c3-a4d4-37869201a08a
  Args:
    source: :EdwardVIII
    literal_value: Duke of Windsor
    relation: :alsoKnownAs
    literal_type: xsd:string
  AssignClass (ee166548-30fa-418a-904e-5ac48df5a80e)
 Call ID: ee166548-30fa-418a-904e-5ac48df5a80e
  Args:
    type: :Man
    source: :GeorgeV
  AssignClass (d0b1aab2-361d-4ead-8d00-f56fff871ee3)
 Call ID: d0b1aab2-361d-4ead-8d00-f56fff871ee3
  Args:
    type: :Person
    source: :GeorgeV
  AssignClass (51cff69c-7958-4e4c-aa88-7c803d0cc65e)
 Call ID: 51cff69c-7958-4e4c-aa88-7c803d0cc65e
  Args:
    type: :Woman
    source: :QueenMary
  AssignClass (0276f75a-7084-4ed1-8367-0b42a302b417)
 Call ID: 0276f75a-7084-4ed1-8367-0b42a302b417
  Args:
    type: :Person
    source: :QueenMary
  AddTriple (d590bd9f-6edf-4c3a-a14b-fc58728c9d7e)
 Call ID: d590bd9f-6edf-4c3a-a14b-fc58728c9d7e
  Args:
    target: :GeorgeV
    relation: :hasFather
    source: :EdwardVIII
  AddTriple (c51591be-b5ab-4c1e-9788-d60e65dca56e)
 Call ID: c51591be-b5ab-4c1e-9788-d60e65dca56e
  Args:
    target: :QueenMary
    relation: :hasMother
    source: :EdwardVIII
  AssignClass (a81a9d59-0263-45d8-ac63-872dda3be047)
 Call ID: a81a9d59-0263-45d8-ac63-872dda3be047
  Args:
    type: :Woman
    source: :QueenVictoria
  AssignClass (fa275c79-bd25-4526-919f-05e96d8999ed)
 Call ID: fa275c79-bd25-4526-919f-05e96d8999ed
  Args:
    type: :Person
    source: :QueenVictoria
  AddTriple (3e47089d-28dc-444e-a64b-e93e0a6d5e0b)
 Call ID: 3e47089d-28dc-444e-a64b-e93e0a6d5e0b
  Args:
    target: :QueenVictoria
    relation: :hasAncestor
    source: :EdwardVIII
  AssignClass (19096688-d191-43f5-aabc-d5c5e698a966)
 Call ID: 19096688-d191-43f5-aabc-d5c5e698a966
  Args:
    type: :Man
    source: :EdwardVII
  AssignClass (cb608a17-bb44-4e5f-a0af-a24772812666)
 Call ID: cb608a17-bb44-4e5f-a0af-a24772812666
  Args:
    type: :Person
    source: :EdwardVII
  AssignClass (352b68be-11ea-4f20-916f-4ced3f2a2a32)
 Call ID: 352b68be-11ea-4f20-916f-4ced3f2a2a32
  Args:
    type: :Woman
    source: :QueenAlexandra
  AssignClass (0b44dc68-7699-43c4-b647-3a1b4bfd8b8c)
 Call ID: 0b44dc68-7699-43c4-b647-3a1b4bfd8b8c
  Args:
    type: :Person
    source: :QueenAlexandra
  AddTriple (bd27e66a-73de-4c29-8adb-ea09bf69f35a)
 Call ID: bd27e66a-73de-4c29-8adb-ea09bf69f35a
  Args:
    target: :EdwardVII
    source: :GeorgeV
    relation: :hasFather
  AddTriple (67c393c4-93dd-482c-81fb-33ebfb4ca45b)
 Call ID: 67c393c4-93dd-482c-81fb-33ebfb4ca45b
  Args:
    target: :QueenAlexandra
    relation: :hasMother
    source: :GeorgeV
  AssignClass (c23a06b9-e9db-46f9-a124-fa34afd6c3af)
 Call ID: c23a06b9-e9db-46f9-a124-fa34afd6c3af
  Args:
    type: :Woman
    source: :PrincessMaryAdelaideOfCambridge
  AssignClass (4b3a0c95-f000-4770-9a66-d89b26370ec8)
 Call ID: 4b3a0c95-f000-4770-9a66-d89b26370ec8
  Args:
    type: :Person
    source: :PrincessMaryAdelaideOfCambridge
  AssignClass (c444474f-a0fd-4da5-8fd5-c26f749e0fc1)
 Call ID: c444474f-a0fd-4da5-8fd5-c26f749e0fc1
  Args:
    type: :Man
    source: :FrancisDukeOfTeck
  AssignClass (5eb3e378-8d2d-4fbf-837f-2c7813613ef0)
 Call ID: 5eb3e378-8d2d-4fbf-837f-2c7813613ef0
  Args:
    type: :Person
    source: :FrancisDukeOfTeck
  AddTriple (354f4d5a-ae69-4e75-b2f4-e7e5bbde80cc)
 Call ID: 354f4d5a-ae69-4e75-b2f4-e7e5bbde80cc
  Args:
    target: :PrincessMaryAdelaideOfCambridge
    source: :QueenMary
    relation: :hasMother
  AddTriple (7b06423a-8061-411e-93c1-ea94be7ef305)
 Call ID: 7b06423a-8061-411e-93c1-ea94be7ef305
  Args:
    source: :QueenMary
    relation: :hasFather
    target: :FrancisDukeOfTeck
  AssignClass (faca4cba-c6f8-4c1d-99fd-e91c4e787725)
 Call ID: faca4cba-c6f8-4c1d-99fd-e91c4e787725
  Args:
    type: :Man
    source: :PrinceJohn
  AssignClass (cce0a373-af8b-40df-88d2-e5ace3395acc)
 Call ID: cce0a373-af8b-40df-88d2-e5ace3395acc
  Args:
    type: :Person
    source: :PrinceJohn
  AddTriple (c92f47ee-1463-4788-9261-9d883284c45d)
 Call ID: c92f47ee-1463-4788-9261-9d883284c45d
  Args:
    target: :EdwardVIII
    relation: :isBrotherOf
    source: :PrinceJohn
  AddTriple (ea5be85d-11fd-4870-a42c-ff31cf9e72fd)
 Call ID: ea5be85d-11fd-4870-a42c-ff31cf9e72fd
  Args:
    target: :GeorgeV
    source: :PrinceJohn
    relation: :hasFather
  AddTriple (06406a94-7515-46a8-8eeb-8cd018dbb629)
 Call ID: 06406a94-7515-46a8-8eeb-8cd018dbb629
  Args:
    target: :QueenMary
    relation: :hasMother
    source: :PrinceJohn
  AssignClass (1ef80c1d-2b27-4f2c-853b-33fa5ee73d0a)
 Call ID: 1ef80c1d-2b27-4f2c-853b-33fa5ee73d0a
  Args:
    type: :Man
    source: :GeorgeVI
  AssignClass (76e672c6-a8b0-479b-b2b0-3801eae32579)
 Call ID: 76e672c6-a8b0-479b-b2b0-3801eae32579
  Args:
    type: :Person
    source: :GeorgeVI
  AddTriple (50f53282-6f76-4d51-a4e9-3d2c745739dd)
 Call ID: 50f53282-6f76-4d51-a4e9-3d2c745739dd
  Args:
    target: :EdwardVIII
    relation: :isBrotherOf
    source: :GeorgeVI
  AddTriple (2457f7df-ca1a-4bd5-8454-bc9ed9a77514)
 Call ID: 2457f7df-ca1a-4bd5-8454-bc9ed9a77514
  Args:
    target: :GeorgeV
    relation: :hasFather
    source: :GeorgeVI
  AddTriple (20b36862-02ec-44d6-829b-de92432b2342)
 Call ID: 20b36862-02ec-44d6-829b-de92432b2342
  Args:
    source: :GeorgeVI
    relation: :hasMother
    target: :QueenMary
  AssignClass (cf1e62c5-66ce-4884-b095-8483652fad74)
 Call ID: cf1e62c5-66ce-4884-b095-8483652fad74
  Args:
    type: :Woman
    source: :WallisSimpson
  AssignClass (ef34799e-a60f-4255-bc48-b51418417145)
 Call ID: ef34799e-a60f-4255-bc48-b51418417145
  Args:
    type: :Person
    source: :WallisSimpson
  AddLiteral (7cab10bc-ed6a-468f-955e-5f5ba17c1019)
 Call ID: 7cab10bc-ed6a-468f-955e-5f5ba17c1019
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1937
    source: :EdwardVIII
  AddTriple (c9b4a514-5271-445d-b351-2ec41edfa175)
 Call ID: c9b4a514-5271-445d-b351-2ec41edfa175
  Args:
    relation: :hasRelation
    source: :EdwardVIII
    target: :WallisSimpson
  AssignClass (e30aaec2-fc6e-49a1-bcb2-012eae4bedcc)
 Call ID: e30aaec2-fc6e-49a1-bcb2-012eae4bedcc
  Args:
    type: :Woman
    source: :PrincessElizabeth
  AssignClass (e0fd56c7-1ca3-45f0-b97a-e1cd89e34b6f)
 Call ID: e0fd56c7-1ca3-45f0-b97a-e1cd89e34b6f
  Args:
    type: :Person
    source: :PrincessElizabeth
  AddTriple (a3739820-e47f-4f9b-a2fc-97f759a464e7)
 Call ID: a3739820-e47f-4f9b-a2fc-97f759a464e7
  Args:
    target: :GeorgeVI
    source: :PrincessElizabeth
    relation: :isDaughterOf
  Finish (35403178-ae0c-49a6-bca2-08031b829005)
 Call ID: 35403178-ae0c-49a6-bca2-08031b829005
  Args: