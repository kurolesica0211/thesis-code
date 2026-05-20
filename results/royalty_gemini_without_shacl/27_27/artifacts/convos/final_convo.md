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
Prince Henry, Duke of Gloucester (Henry William Frederick Albert; 31 March 1900 – 10 June 1974), was a member of the British royal family.
He was the third son of King George V and Queen Mary, and was a younger brother of kings Edward VIII and George VI.
He served as the 11th governor-general of Australia from 1945 to 1947, the only prince to hold the post.
Henry was the first son of a British monarch to be educated at school, where he excelled at sports, and went on to attend Eton College, after which he was commissioned in the 10th Royal Hussars, a regiment he hoped to command.
In 1935, also under parental pressure, he married Lady Alice Montagu Douglas Scott, with whom he had two sons, princes William and Richard.
From 1939 to 1940, Henry served in France as a liaison officer to Lord Gort.
The post had originally been offered to his younger brother the Duke of Kent, who died in an air crash.
Henry attended the coronation of his niece Queen Elizabeth II in 1953 and carried out several overseas tours, often accompanied by his wife.
Upon his death, he was succeeded as the Duke of Gloucester by his only living son, Richard.
Henry was the last surviving son of King George V and Queen Mary.
Early life

Henry was born at 7:30 am on 31 March 1900 at York Cottage on the Sandringham Estate, during the reign of his great-grandmother Queen Victoria.
His father was the Duke of York (later King George V), the only surviving son of the Prince and Princess of Wales (later King Edward VII and Queen Alexandra).
His mother was the Duchess of York (later Queen Mary), the only daughter of the Duke and Duchess of Teck.
Childhood and education

As a child, Henry suffered from poor health, much like his elder brother Albert.
Both brothers had rhotacism, which prevented them from pronouncing the sound r; while Albert's pronunciation was reminiscent of the "French r", Henry was unable to produce the sound at all, replacing it with .
He also had a nasal lisp and an unusually high-pitched tone, which together gave him a distinctive voice.
By 1909, Henry's health had become a matter of concern to his parents.
George wrote to Henry's tutor, Henry Peter Hansell, that he should be treated differently from his more robust elder brothers, noting, "You must remember that he is rather fragile and must be treated differently to his two elder brothers who are more robust".
On 6 May 1910, George succeeded to the throne as George V, and Henry became third in line to the throne.
Hansell persuaded the King that attending school would benefit Henry's character by allowing him to mix with boys of his own age.
Although the King had previously rejected the idea for his elder sons, he agreed on the grounds that it would help Henry "behave like a boy and not like a little child".
Henry thus became the first son of a British monarch to attend school.
Henry spent three years at St Peter’s Court.
His mother once wrote to him in exasperation, "All you write about is your everlasting football of which I am heartily sick", replying to a detailed letter he had sent about a match..
In September 1913, Henry entered Eton College.
During the First World War, Crown Prince Leopold of Belgium, later Leopold III, was a member of his house, Mr Lubbock's.
Henry's academic performance did not improve, but his nerves and general disposition did.
By the time he began his studies at Trinity College, Cambridge in 1919 with Albert, Henry had outgrown all his brothers in height and build and enjoyed good health.
Military career

Unlike his brothers, Henry joined the Army rather than the Royal Navy.
He attended the Royal Military College, Sandhurst, in 1919, and was commissioned as a second lieutenant in the King's Royal Rifle Corps on 16 July.
On 16 July 1921, he was promoted to lieutenant in the 10th Royal Hussars, with whom he continued to serve.
Although he wished to undertake more active military duties, his position as a senior member of the royal family effectively precluded such roles.
He retained a strong interest in sport, and The Cricketer reported in August 1921 that the touring Philadelphians had been presented to Henry at The Oval.
Henry was promoted to captain on 11 May 1927, and was appointed a personal aide-de-camp to his father on 2 August 1929.
On 23 June 1936, he was appointed a personal aide-de-camp to his eldest brother, Edward VIII.
Following Edward's abdication and the accession of Albert as George VI, Henry was effectively retired from active duty and received a ceremonial promotion to major‐general on 1 January 1937, skipping three ranks.
He was also granted a Royal Air Force commission as air vice-marshal on the same day.
On 12 March, he received the colonelcy of his former regiment, the 10th Royal Hussars, together with the colonelcies of the Royal Inniskilling Fusiliers and the Gordon Highlanders.
On 28 May, he received an honorary appointment as a captain in the Royal Naval Volunteer Reserve, followed on 10 November by the honorary colonelcies of the Ceylon Planters' Rifle Corps and the Ceylon Light Infantry (now the Sri Lanka Light Infantry).
In January 1940, he was appointed to the colonelcies of the Ulster Anti‐Aircraft Regiments of the Royal Artillery in the Territorial Army.
He was appointed a Field Marshal in 1955 and a Marshal of the Royal Air Force in 1958.
Duke of Gloucester

On 31 March 1928, his father created him Duke of Gloucester, Earl of Ulster, and Baron Culloden, three titles that linked him with England, Northern Ireland, and Scotland.
Later that year, Henry visited Canada.
Before his marriage, Henry's chief ambition was to command his regiment, the 10th Royal Hussars, or at least to spend as much time in the Army as possible.
To his increasing frustration, he was required to undertake the many royal duties assigned to him by his father.
In September 1928, Henry left England with his brother Edward to shoot big game in Africa.
The brothers parted in Nairobi, where Henry remained for a time.
Henry and Beryl began an affair, although sources differ on when it started; many state that it did not begin until her later visit to England.
At the Grosvenor Hotel, near Buckingham Palace, the affair continued, with Henry openly hosting parties in her suite and drinking heavily.
The affair, widely known in London society, shocked the Queen, much to the amusement of the Prince of Wales, who remarked that "for once, Queen Mary's blue-eyed boy was in trouble instead of himself".
The King intervened, believing that keeping Henry occupied would help end the affair and curb his drinking.
In 1929, Henry travelled to Japan to confer the Garter on the Emperor, and the following year he attended the coronation of Haile Selassie of Ethiopia in Addis Ababa.
In 1934, George V appointed him a Knight of St Patrick, Ireland's chivalric order.
It was the second‐to‐last time the order was awarded; at the time of his death, Henry was its only surviving knight.
Marriage and family

When Henry returned from his visit to Japan in 1929, his affair with Beryl Markham came to an end.
Her husband sought a divorce and threatened to disclose Henry's private letters to his wife unless he was prepared to "take care of Beryl".
Henry and Beryl did not meet again, although she wrote to him when he visited Kenya in 1950 with his wife; he did not reply.
Henry's solicitors paid her an annuity until her death in 1985.
After his tour of Australia and New Zealand, and under pressure from his parents, Henry decided it was time to settle and proposed to Lady Alice Montagu Douglas Scott, sister of one of his closest friends, Lord William Montagu Douglas Scott.
Alice later wrote that the proposal was not romantic, as "it was not his way", and that he simply "mumbled it as we were on a walk one day".
The wedding had originally been planned for Westminster Abbey, but was moved to the Private Chapel at Buckingham Palace following the death of Alice's father, the Duke of Buccleuch, on 19 October 1935.
After two miscarriages, Alice gave birth to two sons:


Residences

During the early years of their marriage, Henry and Alice lived at the Royal Pavilion, Aldershot, near the barracks of Henry's regiment.
Alice later recalled that "It was a very simple cabin," and "the only royal thing about it was my husband's presence."
After his father's death, Henry bought Barnwell Manor in 1938.
The price for the house and four tenanted farms was £37,500; in her memoirs, Alice described this as "the greater part of the money left to Prince Henry by the King."
However, records of the financial arrangements following the abdication of Edward VIII state that Henry received a legacy of £750,000 from his father’s private fortune.
In 1937, Henry and Alice were given York House, St James's Palace, as their London residence.
Following Henry's appointment as Governor-General of Australia in 1945, the tenanted parts of the Barnwell estate were sold for £47,500.
Abdication of Edward VIII

In December 1936, Henry's brother Edward VIII abdicated the throne to marry the divorcée Wallis Simpson.
Their brother Albert ascended as King George VI.
Although Henry was third in line to the throne, after his two nieces Princesses Elizabeth and Margaret, he became the first adult in line, meaning he would act as regent if anything happened to the King before Elizabeth reached the age of 18 on 21 April 1944.
Because of this, Henry could not leave the United Kingdom at the same time as the King, and he and his younger brother, Prince George, Duke of Kent, had to increase their royal engagements considerably to support the new monarch.
Edward VIII, who became Duke of Windsor after abdicating, later recalled that Henry reacted least to the news of his abdication.
Edward admitted, however, that he regretted the implications the abdication would have for "The Unknown Soldier", a teasing nickname he used for Henry because of his low public profile.
The abrupt change in Henry's previously carefree life was made clear by the new King on the first evening of his reign.
Although Henry supported his brother, and later his niece, tirelessly and dutifully, he had a fondness for whisky.
On one occasion, Queen Mary wrote to Alice suggesting that, if they were planning to visit, Henry should bring his own supply, "as we have not got much left, and it is so expensive".
Even Noble Frankland, who wrote Henry's biography after his death at Alice's request and under her supervision, noted that "He did not eschew a glass of whisky ... or the occasional blasphemous oath.
"


King George VI had great affection for Henry.
Circumstances had brought them closer after the abdication, and the King trusted him with important matters, which Henry undertook dutifully.
A member of staff suggested telephoning Henry, who was staying at Birkhall.
When Henry confirmed he had taken the birds, the King's gruff warning that he should never again take birds without telling him surprised the staff member.
Second World War

After the outbreak of World War II, Henry, serving as Chief Liaison Officer to Lord Gort, spent almost the entire first year of the conflict in France.
Writing to Alice, he remarked in his typically direct manner: "Motoring about is not nice as many villages are being bombed".
Henry had known King Leopold III of Belgium since their school days and wished to offer personal support when rumours circulated that Belgium might surrender to Germany.
That night, the Hotel Univers was bombed, killing several people, including those in the rooms adjacent to Henry's.
On the return journey, Henry and Scott were caught in heavy bombing in Tournai, where their car caught fire; they escaped into an alleyway, although Henry required medical attention for a profusely bleeding wound.
Although generally optimistic, Henry experienced bouts of depression during his service in 1940, particularly at the end of his occasional periods of leave.
"My beloved Alice, I did hate leaving you yesterday so very much that I could hardly keep a straight face," he wrote after reporting back.
it is such an awful waste of everything," he told Alice.
In June, after the fall of Dunkirk, Henry was ordered back to England by an embarrassed General Headquarters, which had been unable to guarantee the King's brother's safety.
"Wherever I went or had been, I was bombed," he wrote to his mother, amused by the situation.
In early 1942, the King arranged a four‐month military and diplomatic mission for Henry to the Middle East, India, and East Africa.
The King wrote to his sister‐in‐law that he would act as guardian to the newborn William should anything happen to Henry.
After Henry's younger brother, the Duke of Kent, was killed in a plane crash in Scotland in August 1942, it was decided that Henry would not be sent on any further missions that might place him at similar risk.
Governor-General of Australia

In late 1944, Henry was unexpectedly appointed Governor-General of Australia following the death in 1942 of his younger brother, the Duke of Kent, who had previously been offered the post.
Although naturally shy, which sometimes made him appear formal, Henry and Alice travelled extensively during their tenure, using his own aircraft for official journeys.
When Prime Minister John Curtin died in 1945, Henry appointed Frank Forde as his successor.
Henry left Australia in March 1947 after two years in office.
He was recalled to the United Kingdom to act as Counsellor of State on behalf of the King during the visit by George VI and Princesses Elizabeth and Margaret to South Africa.
Later life

In May 1949, May 1961, May 1962, and May 1963, Henry served as Lord High Commissioner to the General Assembly of the Church of Scotland, a role that temporarily placed him in precedence in Scotland immediately below the King and Queen.
He attended the coronation of his niece, Queen Elizabeth II, in 1953, and he and Alice continued to undertake royal engagements, including several overseas tours.
In 1954, Henry was Treasurer of the Honourable Society of Gray's Inn, and in 1957 he represented Elizabeth II at the Malayan Declaration of Independence on 31 August.
The first occurred in 1965 while he and Alice were returning by car from Sir Winston Churchill's funeral, causing a crash.
His last public appearance was in 1967 at the unveiling of Queen Mary's plaque at Marlborough House, where he appeared frail and noticeably older than the Duke of Windsor.
By 1972, his health had deteriorated to the extent that he was unable to attend the Duke of Windsor's funeral in May or the wedding of his younger son, Richard, in July.
In August, his elder son, William, was killed in a plane crash; Henry's condition was so poor that Alice hesitated to tell him.
Death

Henry died on 10 June 1974 at the age of 74.
He was the last surviving son of King George V and Queen Mary, and the last living knight of the Order of St Patrick.
He was buried in the Royal Burial Ground, Frogmore.
His only living son, Richard, inherited the title of Duke of Gloucester.
Alice received permission from Queen Elizabeth II to be styled Princess Alice, Duchess of Gloucester, to distinguish her from Richard's wife.
She outlived Henry by 30 years, dying on 29 October 2004 at the age of 102, and became the longest-lived member of the British royal family in history.
Honours and arms

Honours

Military

Arms

In 1921, Prince Henry was granted a personal coat of arms, being the royal arms, differenced by a label argent of three points, the centre bearing a lion rampant gules, and the outer points crosses gules.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (9d1b71f2-5713-4dfb-9d25-cb52370de0b2)
 Call ID: 9d1b71f2-5713-4dfb-9d25-cb52370de0b2
  Args:
    type: :Man
    source: :PrinceHenry
  AssignClass (24528fbd-e15e-470b-a346-b6ffb4b41c0e)
 Call ID: 24528fbd-e15e-470b-a346-b6ffb4b41c0e
  Args:
    type: :Man
    source: :KingGeorgeV
  AssignClass (f8d00086-c631-4bf9-8704-179916d41545)
 Call ID: f8d00086-c631-4bf9-8704-179916d41545
  Args:
    type: :Woman
    source: :QueenMary
  AssignClass (50ed8f86-4679-4846-a1df-5576e6c3b453)
 Call ID: 50ed8f86-4679-4846-a1df-5576e6c3b453
  Args:
    type: :Man
    source: :EdwardVIII
  AssignClass (d852c1c6-12b9-4025-ada8-492110efcebb)
 Call ID: d852c1c6-12b9-4025-ada8-492110efcebb
  Args:
    type: :Man
    source: :GeorgeVI
  AssignClass (69fc6e05-9fd3-47d9-8693-fbcfb453e1c2)
 Call ID: 69fc6e05-9fd3-47d9-8693-fbcfb453e1c2
  Args:
    type: :Woman
    source: :LadyAliceMontaguDouglasScott
  AssignClass (f5e53a0d-d6f7-4a7d-ab71-199f4bf8189b)
 Call ID: f5e53a0d-d6f7-4a7d-ab71-199f4bf8189b
  Args:
    type: :Man
    source: :PrinceWilliam
  AssignClass (879b39de-639a-4921-b0c8-aed4ac151cb9)
 Call ID: 879b39de-639a-4921-b0c8-aed4ac151cb9
  Args:
    type: :Man
    source: :PrinceRichard
  AssignClass (666f268b-a291-4e0d-814b-6ad8a76473ca)
 Call ID: 666f268b-a291-4e0d-814b-6ad8a76473ca
  Args:
    type: :Man
    source: :DukeOfKent
  AddLiteral (e917161e-41fd-4a3f-9ceb-73044331ed90)
 Call ID: e917161e-41fd-4a3f-9ceb-73044331ed90
  Args:
    source: :PrinceHenry
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1900
  AddLiteral (01d28e51-754d-4ce6-9a20-952532e93dbe)
 Call ID: 01d28e51-754d-4ce6-9a20-952532e93dbe
  Args:
    source: :PrinceHenry
    literal_value: 1974
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (9a381056-3900-4e54-bcc7-22d998c98141)
 Call ID: 9a381056-3900-4e54-bcc7-22d998c98141
  Args:
    source: :PrinceHenry
    relation: :hasFather
    target: :KingGeorgeV
  AddTriple (3d103db7-8c3d-41f8-960d-ffe9a9b5f798)
 Call ID: 3d103db7-8c3d-41f8-960d-ffe9a9b5f798
  Args:
    source: :PrinceHenry
    target: :QueenMary
    relation: :hasMother
  AddTriple (20f2bbda-3ab0-439b-b51b-9ad752b0cb34)
 Call ID: 20f2bbda-3ab0-439b-b51b-9ad752b0cb34
  Args:
    source: :PrinceHenry
    relation: :isBrotherOf
    target: :EdwardVIII
  AddTriple (0a5e89ca-2f1e-4dbf-892e-8d9d0a28cc54)
 Call ID: 0a5e89ca-2f1e-4dbf-892e-8d9d0a28cc54
  Args:
    target: :GeorgeVI
    relation: :isBrotherOf
    source: :PrinceHenry
  AddTriple (6209a49c-1608-42ed-90a9-6cd8727c1de4)
 Call ID: 6209a49c-1608-42ed-90a9-6cd8727c1de4
  Args:
    relation: :isBrotherOf
    target: :DukeOfKent
    source: :PrinceHenry
  AddTriple (dd49d59b-8771-4e48-9580-1c9b9a597541)
 Call ID: dd49d59b-8771-4e48-9580-1c9b9a597541
  Args:
    target: :PrinceWilliam
    relation: :hasSon
    source: :PrinceHenry
  AddTriple (36bddf9c-7ab6-4831-8e5d-af6d3c650ba7)
 Call ID: 36bddf9c-7ab6-4831-8e5d-af6d3c650ba7
  Args:
    source: :PrinceHenry
    relation: :hasSon
    target: :PrinceRichard
  AddTriple (97e01660-fb98-4a19-b75d-e0fc2a838514)
 Call ID: 97e01660-fb98-4a19-b75d-e0fc2a838514
  Args:
    relation: :hasSon
    target: :PrinceWilliam
    source: :LadyAliceMontaguDouglasScott
  AddTriple (78afc884-0c5c-47bf-b95a-3f8430d31606)
 Call ID: 78afc884-0c5c-47bf-b95a-3f8430d31606
  Args:
    source: :LadyAliceMontaguDouglasScott
    target: :PrinceRichard
    relation: :hasSon
  AddLiteral (ed15f150-639e-4fa6-89c4-0ef364603b14)
 Call ID: ed15f150-639e-4fa6-89c4-0ef364603b14
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1935
    source: :PrinceHenry
  AddTriple (8be6aeb8-f576-44a0-bb6b-be9489e6b83b)
 Call ID: 8be6aeb8-f576-44a0-bb6b-be9489e6b83b
  Args:
    relation: :hasRelation
    target: :LadyAliceMontaguDouglasScott
    source: :PrinceHenry
  Finish (faec0df6-8594-4608-bbab-d30d1ef6e894)
 Call ID: faec0df6-8594-4608-bbab-d30d1ef6e894
  Args: