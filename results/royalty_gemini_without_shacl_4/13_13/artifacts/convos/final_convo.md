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
Elizabeth Angela Marguerite Bowes-Lyon (4 August 1900 – 30 March 2002) was Queen of the United Kingdom and the Dominions of the British Commonwealth from 11 December 1936 to 6 February 1952 as the wife of King George VI.
After her husband died, she was officially known as Queen Elizabeth the Queen Mother to avoid confusion with her daughter Queen Elizabeth II.
Born into a family of British nobility, Elizabeth came to prominence in 1923 when she married Prince Albert, Duke of York, the second son of King George V and Queen Mary.
The couple and their daughters, Elizabeth and Margaret, embodied traditional ideas of family and public service.
As Duchess of York, Elizabeth undertook a variety of public engagements and became known for her consistently cheerful countenance.
In 1936, Elizabeth's husband unexpectedly ascended the throne as George VI when his older brother, Edward VIII, abdicated in order to marry American divorcée Wallis Simpson.
Elizabeth then became queen consort.
After the death of Queen Mary in 1953, Elizabeth was viewed as the matriarch of the British royal family.
Early life

Elizabeth Angela Marguerite Bowes-Lyon was born on 4 August 1900, the youngest daughter and the ninth of ten children of Claude Bowes-Lyon, Lord Glamis (later the 14th Earl of Strathmore and Kinghorne in the Peerage of Scotland), and his wife, Cecilia Cavendish-Bentinck.
Her mother was descended from British prime minister William Cavendish-Bentinck, 3rd Duke of Portland, and Governor-General of India Richard Wellesley, 1st Marquess Wellesley, who was the elder brother of another prime minister, Arthur Wellesley, 1st Duke of Wellington.
The location of Elizabeth's birth remains uncertain, but reputedly she was born either in her parents' Westminster home at Belgrave Mansions, Grosvenor Gardens, or in a horse-drawn ambulance on the way to a hospital.
Elizabeth spent much of her childhood at St Paul's Walden and at Glamis Castle, the Earl's ancestral home in Scotland.
On Elizabeth's 14th birthday, Britain declared war on Germany.
Glamis was turned into a convalescent home for wounded soldiers, which Elizabeth helped to run.
The first love of Elizabeth was considered to be Charles Gordon-Lennox, Lord Settrington, whose sister, Lady Doris, was a close friend of hers.
Upon his death, Elizabeth called him "my only true friend", writing: "I was not shy about him and he was so delightful.
Charlie was the only one I could talk to in a completely natural and simple way – he was dear to me, and I miss him very much".
Marriage

Prince Albert, Duke of York – "Bertie" to the family – was the second son of King George V and Queen Mary.
He initially proposed to Elizabeth in 1921, but she turned him down, being "afraid never, never again to be free to think, speak and act as I feel I really ought to".
When he declared he would marry no other, Queen Mary visited Glamis to see for herself the young woman who had won her son's love.
She became convinced that Elizabeth was "the one girl who could make Bertie happy", but refused to interfere.
At the same time, Elizabeth was courted by James Stuart, Albert's equerry, until he left the prince's service for a better-paid job in the American oil business.
In February 1922, Elizabeth was a bridesmaid at the wedding of Albert's sister, Princess Mary, to Viscount Lascelles.
Eventually in January 1923, Elizabeth agreed to marry Albert, despite her misgivings about royal life.
Albert's freedom in choosing Elizabeth, not a member of a royal family, though the daughter of a peer, was considered a gesture in favour of political modernisation; previously, princes were expected to marry princesses from other royal families.
Unexpectedly, Elizabeth laid her bouquet at the Tomb of the Unknown Warrior on her way into the abbey, in memory of her brother Fergus.
Following a wedding breakfast at Buckingham Palace prepared by chef Gabriel Tschumi, Elizabeth and Albert honeymooned at Polesden Lacey, a manor house in Surrey owned by the wealthy socialite and friend Margaret Greville.
Duchess of York

After a successful royal visit to Northern Ireland in July 1924, the Labour government agreed that Albert and Elizabeth could tour East Africa from December 1924 to April 1925.
The Labour government was defeated by the Conservatives in a general election in November (which Elizabeth described as "marvellous" to her mother) and the Governor-General of Anglo-Egyptian Sudan, Sir Lee Stack, was assassinated three weeks later.
Albert had a stammer, which affected his ability to deliver speeches, and after October 1925, Elizabeth assisted in helping him through the therapy devised by Lionel Logue, an episode portrayed in the 2010 film The King's Speech.
In 1926, Elizabeth gave birth to their first child, Princess Elizabeth – known as "Lilibet" to the family – who would later become Queen Elizabeth II.
Albert and Elizabeth, without their child, travelled to Australia to open Parliament House in Canberra in 1927.
Their journey by sea took them via Jamaica, the Panama Canal and the Pacific; Elizabeth fretted constantly over her baby back in Britain, but their journey was a public relations success.
In New Zealand she fell ill with a cold and missed some engagements, but enjoyed the local fishing in the Bay of Islands accompanied by Australian sports fisherman Harry Andreas.
Queen consort

On 20 January 1936, George V died and his eldest son, Edward, Prince of Wales, became King Edward VIII.
Elizabeth's husband, Albert, became heir presumptive.
Albert reluctantly became king of the United Kingdom and emperor of India on 11 December 1936 under the regnal name of George VI.
Elizabeth became queen and empress.
Elizabeth's crown was made of platinum and was set with the Koh-i-Noor diamond.
Edward married Wallis Simpson, and they became the Duke and Duchess of Windsor, but while Edward was a Royal Highness, George VI withheld the style from Wallis, a decision that Elizabeth supported.
Elizabeth was later quoted as referring to Wallis as "that woman", and Wallis referred to Elizabeth as "Cookie", because of her supposed resemblance to a fat Scots cook.
Claims that Elizabeth remained embittered towards Wallis were denied by her close friends; the Duke of Grafton wrote that she "never said anything nasty about the Duchess of Windsor, except to say she really hadn't got a clue what she was dealing with".
Overseas visits

In summer 1938, a state visit to France by the King and Queen was postponed for three weeks because of the death of Elizabeth's mother.
In two weeks, Norman Hartnell created an all-white trousseau for Elizabeth, who could not wear colours as she was still in mourning.
After the Munich Agreement of 1938 appeared to forestall the advent of armed conflict, the British prime minister Neville Chamberlain was invited onto the balcony of Buckingham Palace with the King and Queen to receive acclamation from a crowd of well-wishers.
While broadly popular among the general public, Chamberlain's policy towards Hitler was the subject of some opposition in the House of Commons, which led historian John Grigg to describe George VI's behaviour in associating himself so prominently with a politician as "the most unconstitutional act by a British sovereign in the present century".
In May and June 1939, Elizabeth and her husband toured Canada from coast to coast and back, the first time a reigning monarch had toured Canada.
First Lady Eleanor Roosevelt said that Elizabeth was "perfect as a Queen, gracious, informed, saying the right thing & kind but a little self-consciously regal".
According to an often-told story, during one of the earliest of the royal couple's repeated encounters with the crowds, a Boer War veteran asked Elizabeth, "Are you Scots or are you English?"
Elizabeth told Canadian prime minister William Lyon Mackenzie King, "that tour made us", and she returned to Canada frequently both on official tours and privately.
Shortly after the declaration of war, The Queen's Book of the Red Cross was conceived.
Fifty authors and artists contributed to the book, which was fronted by Cecil Beaton's portrait of Elizabeth and was sold in aid of the Red Cross.
Elizabeth publicly refused to leave London or send the children to Canada, even during the Blitz, when the British Cabinet advised her to do so.
"


Elizabeth visited troops, hospitals, factories, and parts of Britain that were targeted by the German Luftwaffe, in particular the East End near London's docks.
When Buckingham Palace itself took several hits during the height of the bombing, Elizabeth said, "I'm glad we've been bombed.
"


Though the King and Queen spent the working day at Buckingham Palace, partly for security and family reasons they stayed at night at Windsor Castle about 20 miles (32 km) west of central London with their daughters.
During the "Phoney War" the Queen was given revolver training because of fears of imminent invasion.
French prime minister Édouard Daladier characterised Elizabeth as "an excessively ambitious young woman who would be ready to sacrifice every other country in the world so that she may remain Queen."
Post-war years

In the 1945 British general election, Churchill's Conservative Party was soundly defeated by the Labour Party of Clement Attlee.
Elizabeth's political views were rarely disclosed, but a letter she wrote in 1947 described Attlee's "high hopes of a socialist heaven on earth" as fading and presumably describes those who voted for him as "poor people, so many half-educated and bemused.
"


During the 1947 royal tour of South Africa, Elizabeth's serene public behaviour was broken, exceptionally, when she rose from the royal car to strike an admirer with her umbrella because she had mistaken his enthusiasm for hostility.
In summer 1951, Elizabeth and her daughters fulfilled the King's public engagements in his place.
After a lung resection, he appeared to recover, but the delayed trip to Australia and New Zealand was altered so that Princess Elizabeth and her husband, the Duke of Edinburgh, went in the King and Queen's place in January 1952.
George VI died in his sleep on 6 February 1952 while Princess Elizabeth and the Duke of Edinburgh were in Kenya on a Commonwealth tour, and with George's death his daughter immediately became Queen Elizabeth II.
Queen mother

Widowhood

Shortly after George VI's death, Elizabeth began to be styled as Her Majesty Queen Elizabeth The Queen Mother because the normal style for the widow of a king, "Queen Elizabeth", would have been too similar to the style of her elder daughter, Queen Elizabeth II.
Popularly, she became the "Queen Mother" or the "Queen Mum".
Eventually, she became just as busy as queen mother as she had been as queen consort.
Upon her return to the region in 1957, Elizabeth was inaugurated as the college's president, and attended other events that were deliberately designed to be multi-racial.
During her daughter's extensive tour of the Commonwealth over 1953–54, Elizabeth acted as a counsellor of state and looked after her grandchildren, Charles and Anne.
Elizabeth oversaw the restoration of the remote Castle of Mey, on the north coast of Scotland, which she used to "get away from everything" for three weeks in August and ten days in October each year.
In February 1964, Elizabeth had an emergency appendectomy, which led to the postponement of a planned tour of Australia, New Zealand, and Fiji until 1966.
During her widowhood, Elizabeth continued to travel extensively, including on over forty official visits overseas.
In 1982, Elizabeth was rushed to hospital when a fish bone became stuck in her throat, and had an operation to remove it.
In 1987, Elizabeth was criticised when it emerged that two of her nieces, Nerissa and Katherine Bowes-Lyon, had been committed to a psychiatric hospital in Redhill, Surrey, in 1941 because they had severe learning disabilities.
However, Burke's Peerage had listed the sisters as dead, apparently because their mother, Fenella (Elizabeth's sister-in-law), "was 'extremely vague' when it came to filling in forms and might not have completed the paperwork for the family entry correctly".
Elizabeth said that the news of their institutionalisation came as a surprise to her.
Centenarian

In her later years, Elizabeth became known for her longevity.
Elizabeth's 100th birthday was celebrated in a number of ways: a parade, with contributions from Sir Norman Wisdom and Sir John Mills, celebrated highlights of her life; the Royal Bank of Scotland issued a commemorative £20 note with her image; and she attended a lunch at the Guildhall, London, at which George Carey, the Archbishop of Canterbury, accidentally attempted to drink her glass of wine.
On 1 August 2001, Elizabeth had a blood transfusion for anaemia after suffering from mild heat exhaustion, though she was well enough to make her traditional appearance outside Clarence House three days later to celebrate her 101st birthday.
In December 2001, aged 101, Elizabeth fractured her pelvis in a fall.
On 13 February 2002, Elizabeth fell and cut her arm in her sitting room at Sandringham House; an ambulance and doctor were called, and the wound was dressed.
She was still determined to attend Margaret's funeral at St George's Chapel, Windsor Castle, two days later on the Friday of that week, even though Queen Elizabeth II and the rest of the royal family were concerned about the journey the Queen Mother would face to get from Norfolk to Windsor; she was also rumoured to be hardly eating.
Nevertheless, she flew to Windsor by helicopter, and so that no photographs of her in a wheelchair (which she hated being seen in) could be taken—she insisted that she be shielded from the press—she travelled to the service in a people carrier with blacked-out windows, which had been previously used by Margaret.
On 5 March 2002, Elizabeth attended the luncheon of the annual lawn party of the Eton Beagles and watched the Cheltenham Races on television; however, her health began to deteriorate precipitously during her last weeks, after she retreated to Royal Lodge for the final time.
Death

Elizabeth died at 3:15 pm on 30 March 2002 at Royal Lodge, Windsor, aged 101.
Her daughter, Queen Elizabeth II, was by her side.
The Queen Mother had been suffering from a chest cold since Christmas 2001.
Elizabeth grew camellias in each of her gardens, and before her flag-draped coffin was taken from Windsor to lie in state at Westminster Hall, an arrangement of camellias from her own gardens was placed on top.
At one point, her four grandsons–Prince Charles, Prince Andrew, Prince Edward and Viscount Linley–mounted the guard as a mark of respect, an honour similar to the Vigil of the Princes at the lying in state of King George V.


On the day of Elizabeth's funeral, 9 April, the governor general of Canada, Adrienne Clarkson, issued a proclamation asking Canadians to honour Elizabeth's memory that day.
In Australia, Governor-General Peter Hollingworth read the lesson at a memorial service held in St Andrew's Cathedral, Sydney.
In London, more than a million people filled the area outside Westminster Abbey and along the 23-mile (37 km) route from central London to Elizabeth's final resting place in the King George VI Memorial Chapel beside her husband and younger daughter in St George's Chapel.
Legacy

Known for her personal and public charm, Elizabeth was one of the most popular members of the royal family, and helped to stabilise the popularity of the monarchy as a whole.
Elizabeth's critics included Kitty Kelley, who falsely alleged that she did not abide by the rationing regulations during the Second World War.
Claims that Elizabeth used racist slurs to refer to black people were strongly denied by Major Colin Burgess, the husband of Elizabeth Burgess, a mixed-race secretary who accused members of Prince Charles's household of racial abuse.
Elizabeth made no public comments on race, but according to Robert Rhodes James, in private she "abhorred racial discrimination" and decried apartheid as "dreadful".
In his official biography, William Shawcross portrays Elizabeth as a person whose indomitable optimism, zest for life, good manners, mischievous sense of humour, and interest in people and subjects of all kinds contributed to her exceptional popularity and to her longevity.
Sir Hugh Casson said Elizabeth was like "a wave breaking on a rock, because although she is sweet and pretty and charming, she also has a basic streak of toughness and tenacity. ...
The Queen Mother stopped and picked these up as though somebody had misplaced them.
Elizabeth was well known for her dry witticisms.
On hearing that Edwina Mountbatten was buried at sea, she said: "Dear Edwina, she always liked to make a splash."
"


After being advised by a Conservative minister in the 1970s not to employ homosexuals, Elizabeth observed that without them, "we'd have to go self-service".
Elizabeth's habits were parodied by the satirical 1980s television programme Spitting Image.
She was portrayed by Juliet Aubrey in Bertie and Elizabeth, Sylvia Syms in The Queen, Natalie Dormer in W.E., Olivia Colman in Hyde Park on Hudson, Victoria Hamilton (Seasons 1 and 2), Marion Bailey (Seasons 3 and 4) and Marcia Warren (Season 5 and 6) in The Crown and in The King's Speech by Helena Bonham Carter, who was nominated for an Academy Award for Best Supporting Actress and won a BAFTA Award for Best Actress in a Supporting Role for her portrayal.
The Cunard White Star Line's RMS Queen Elizabeth was named after her.
Supposedly, the liner started to slide into the water before Elizabeth could officially launch her, and acting sharply, she managed to smash a bottle of Australian red over the liner's bow just before it slid out of reach.
In 1954, Elizabeth sailed to New York on her namesake.
A statue of Elizabeth by sculptor Philip Jackson was unveiled in front of the George VI Memorial, off The Mall, London, on 24 February 2009, creating the King George VI and Queen Elizabeth Memorial.
In March 2011, Elizabeth's eclectic musical taste was revealed when details of her small record collection kept at the Castle of Mey were made public.
Eight years before her death, Elizabeth had reportedly placed two-thirds of her money (an estimated £19 million) into trusts, for the benefit of her great-grandchildren.
She left the bulk of her estate, estimated to be worth between £50 and £70 million, including paintings, Fabergé eggs, jewellery, and horses, to her surviving daughter, Queen Elizabeth II.
The most important pieces of art were transferred to the Royal Collection by Elizabeth II.
Following her death, 
Queen Elizabeth II successfully applied to the High Court so that details of her mother's will would be kept secret.
This brought criticism from Labour politicians and segments of the public, and Queen Elizabeth II eventually released the outlines of her mother's will.
Titles, honours and arms

Titles and styles

Elizabeth held numerous titles starting with her birth, as the daughter of an earl and through her marriage to the-then Duke of York, who later became King-Emperor.
She was the last person to be Empress of India, and was Queen Mother during widowhood.
Arms

Elizabeth's coat of arms was the royal coat of arms of the United Kingdom (in either the English or the Scottish version) impaled with the canting arms of her father, the Earl of Strathmore; the latter being: 1st and 4th quarters, Argent, a lion rampant Azure, armed and langued Gules, within a double tressure flory-counter-flory of the second (Lyon); 2nd and 3rd quarters, Ermine, three bows stringed paleways proper (Bowes).



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
  AssignClass (13a5eab0-5b99-4810-9575-34b4ed95db2a)
 Call ID: 13a5eab0-5b99-4810-9575-34b4ed95db2a
  Args:
    type: :Woman
    source: Elizabeth_Bowes-Lyon
  AssignClass (299ee7dd-1236-42d7-aff4-f3a7ef8d18ac)
 Call ID: 299ee7dd-1236-42d7-aff4-f3a7ef8d18ac
  Args:
    type: :Person
    source: Elizabeth_Bowes-Lyon
  AddLiteral (1fbc8c96-de80-4cc9-abd0-943aa670f83a)
 Call ID: 1fbc8c96-de80-4cc9-abd0-943aa670f83a
  Args:
    literal_type: xsd:integer
    source: Elizabeth_Bowes-Lyon
    literal_value: 1900
    relation: :hasBirthYear
  AddLiteral (0a82a64e-b82f-4d08-8bba-e98aa1a3662f)
 Call ID: 0a82a64e-b82f-4d08-8bba-e98aa1a3662f
  Args:
    literal_value: 2002
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Elizabeth_Bowes-Lyon
  AssignClass (71bd5033-5f56-44ca-88cd-48450d3b2f38)
 Call ID: 71bd5033-5f56-44ca-88cd-48450d3b2f38
  Args:
    type: :Man
    source: George_VI
  AssignClass (2e799e9c-b52a-4101-82ff-871f8e7121f9)
 Call ID: 2e799e9c-b52a-4101-82ff-871f8e7121f9
  Args:
    type: :Person
    source: George_VI
  AddTriple (bd8be8c2-0d37-4e20-ab54-293866e78c8a)
 Call ID: bd8be8c2-0d37-4e20-ab54-293866e78c8a
  Args:
    target: Elizabeth_Bowes-Lyon_II
    source: George_VI
    relation: :hasChild
  AddTriple (0c69cb57-9ba7-4856-bd38-a4912d203ac6)
 Call ID: 0c69cb57-9ba7-4856-bd38-a4912d203ac6
  Args:
    source: George_VI
    target: Margaret
    relation: :hasChild
  AddTriple (8504caab-3761-4763-a6a9-fe706ffdb75b)
 Call ID: 8504caab-3761-4763-a6a9-fe706ffdb75b
  Args:
    source: Elizabeth_Bowes-Lyon
    target: Elizabeth_Bowes-Lyon_II
    relation: :hasChild
  AddTriple (ae31b3db-722d-445f-9531-881ae5f79da7)
 Call ID: ae31b3db-722d-445f-9531-881ae5f79da7
  Args:
    relation: :hasChild
    target: Margaret
    source: Elizabeth_Bowes-Lyon
  AssignClass (dee2898f-b822-49d3-ad51-2a4cbdb9c312)
 Call ID: dee2898f-b822-49d3-ad51-2a4cbdb9c312
  Args:
    type: :Woman
    source: Elizabeth_Bowes-Lyon_II
  AssignClass (f26ac743-22fd-48e3-8e0d-c22ce161bf86)
 Call ID: f26ac743-22fd-48e3-8e0d-c22ce161bf86
  Args:
    type: :Person
    source: Elizabeth_Bowes-Lyon_II
  AssignClass (669e7a7d-e9db-488f-bb6a-d42c673d71c4)
 Call ID: 669e7a7d-e9db-488f-bb6a-d42c673d71c4
  Args:
    type: :Woman
    source: Margaret
  AssignClass (619864dc-4e35-4841-a09d-30f9afaca640)
 Call ID: 619864dc-4e35-4841-a09d-30f9afaca640
  Args:
    type: :Person
    source: Margaret
  AssignClass (b5b79b54-1c95-439a-b736-5ba4bc930d42)
 Call ID: b5b79b54-1c95-439a-b736-5ba4bc930d42
  Args:
    type: :Man
    source: George_V
  AssignClass (803b2f9b-1087-4555-b621-7129fcb4aada)
 Call ID: 803b2f9b-1087-4555-b621-7129fcb4aada
  Args:
    type: :Person
    source: George_V
  AssignClass (b0dfe853-1bfa-4a5c-9c0e-0399da0c0138)
 Call ID: b0dfe853-1bfa-4a5c-9c0e-0399da0c0138
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (44e11031-1b43-4a25-88ce-e4931eac9b2f)
 Call ID: 44e11031-1b43-4a25-88ce-e4931eac9b2f
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (e027854a-2f77-40f9-9d2f-dd98c981bb18)
 Call ID: e027854a-2f77-40f9-9d2f-dd98c981bb18
  Args:
    source: George_V
    target: George_VI
    relation: :hasChild
  AddTriple (42b80fd8-b21e-4d7c-abd0-1af8f8ef172c)
 Call ID: 42b80fd8-b21e-4d7c-abd0-1af8f8ef172c
  Args:
    relation: :hasChild
    source: Queen_Mary
    target: George_VI
  AssignClass (0f0df926-fae3-4829-a319-9027c3f1acda)
 Call ID: 0f0df926-fae3-4829-a319-9027c3f1acda
  Args:
    type: :Man
    source: Edward_VIII
  AssignClass (0d756738-dd2e-46bb-bb69-e0f400d9b739)
 Call ID: 0d756738-dd2e-46bb-bb69-e0f400d9b739
  Args:
    type: :Person
    source: Edward_VIII
  AddTriple (3c5636a4-f380-465f-a193-235449c865e0)
 Call ID: 3c5636a4-f380-465f-a193-235449c865e0
  Args:
    source: George_V
    target: Edward_VIII
    relation: :hasChild
  AddTriple (f60ab3cb-3ce1-4e58-890c-16dd1e2bba50)
 Call ID: f60ab3cb-3ce1-4e58-890c-16dd1e2bba50
  Args:
    relation: :hasChild
    source: Queen_Mary
    target: Edward_VIII
  AddTriple (775e3c0e-8da2-4cff-aefb-bcf1ef698f3e)
 Call ID: 775e3c0e-8da2-4cff-aefb-bcf1ef698f3e
  Args:
    relation: :hasChild
    target: Princess_Mary
    source: George_V
  AddTriple (7dde2a43-f695-43cf-b255-03bbb20ae617)
 Call ID: 7dde2a43-f695-43cf-b255-03bbb20ae617
  Args:
    relation: :hasChild
    target: Princess_Mary
    source: Queen_Mary
  AssignClass (e5fc0722-66c4-4bf2-b507-4aa5fbdfba57)
 Call ID: e5fc0722-66c4-4bf2-b507-4aa5fbdfba57
  Args:
    type: :Woman
    source: Princess_Mary
  AssignClass (3ee875b4-7838-4eab-b8a5-ef71ee105e2c)
 Call ID: 3ee875b4-7838-4eab-b8a5-ef71ee105e2c
  Args:
    type: :Person
    source: Princess_Mary
  AssignClass (a59a537b-a897-48aa-9648-3763f2aa3c62)
 Call ID: a59a537b-a897-48aa-9648-3763f2aa3c62
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (520d33ed-3018-4add-b845-f38e832e60e6)
 Call ID: 520d33ed-3018-4add-b845-f38e832e60e6
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AssignClass (7906b08d-48e1-4a88-bc8f-c2d7cf1b95e9)
 Call ID: 7906b08d-48e1-4a88-bc8f-c2d7cf1b95e9
  Args:
    type: :Woman
    source: Cecilia_Cavendish-Bentinck
  AssignClass (cd54b434-3810-40dc-aea9-f4f5922d735a)
 Call ID: cd54b434-3810-40dc-aea9-f4f5922d735a
  Args:
    type: :Person
    source: Cecilia_Cavendish-Bentinck
  AddTriple (ca8ba6e9-3ebf-445d-840d-ebc7bf110046)
 Call ID: ca8ba6e9-3ebf-445d-840d-ebc7bf110046
  Args:
    target: Elizabeth_Bowes-Lyon
    source: Claude_Bowes-Lyon
    relation: :hasChild
  AddTriple (c4ec3598-b4bd-4c8c-83ac-612c71306447)
 Call ID: c4ec3598-b4bd-4c8c-83ac-612c71306447
  Args:
    target: Elizabeth_Bowes-Lyon
    source: Cecilia_Cavendish-Bentinck
    relation: :hasChild
  AddTriple (2a9b0627-e16e-444d-829a-ca71cb8e7a99)
 Call ID: 2a9b0627-e16e-444d-829a-ca71cb8e7a99
  Args:
    source: Claude_Bowes-Lyon
    target: Fergus
    relation: :hasChild
  AddTriple (44f084c5-fcb8-462f-89a7-de301bb9d5b8)
 Call ID: 44f084c5-fcb8-462f-89a7-de301bb9d5b8
  Args:
    source: Cecilia_Cavendish-Bentinck
    target: Fergus
    relation: :hasChild
  AssignClass (5824e44f-7a39-4d80-a17c-5bd193e9e1c1)
 Call ID: 5824e44f-7a39-4d80-a17c-5bd193e9e1c1
  Args:
    type: :Man
    source: Fergus
  AssignClass (ebbd2b99-ee7b-48d5-a3b5-d31a5ee30946)
 Call ID: ebbd2b99-ee7b-48d5-a3b5-d31a5ee30946
  Args:
    type: :Person
    source: Fergus
  Finish (7e2fd524-b46c-4455-9734-0274a134e682)
 Call ID: 7e2fd524-b46c-4455-9734-0274a134e682
  Args: