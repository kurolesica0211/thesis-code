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
By 1909, Henry's health had become a matter of concern to his parents.
George wrote to Henry's tutor, Henry Peter Hansell, that he should be treated differently from his more robust elder brothers, noting, "You must remember that he is rather fragile and must be treated differently to his two elder brothers who are more robust".
On 6 May 1910, George succeeded to the throne as George V, and Henry became third in line to the throne.
Hansell persuaded the King that attending school would benefit Henry's character by allowing him to mix with boys of his own age.
Although the King had previously rejected the idea for his elder sons, he agreed on the grounds that it would help Henry "behave like a boy and not like a little child".
Henry thus became the first son of a British monarch to attend school.
Henry spent three years at St Peter’s Court.
In September 1913, Henry entered Eton College.
During the First World War, Crown Prince Leopold of Belgium, later Leopold III, was a member of his house, Mr Lubbock's.
Henry's academic performance did not improve, but his nerves and general disposition did.
By the time he began his studies at Trinity College, Cambridge in 1919 with Albert, Henry had outgrown all his brothers in height and build and enjoyed good health.
Military career

Unlike his brothers, Henry joined the Army rather than the Royal Navy.
He retained a strong interest in sport, and The Cricketer reported in August 1921 that the touring Philadelphians had been presented to Henry at The Oval.
Henry was promoted to captain on 11 May 1927, and was appointed a personal aide-de-camp to his father on 2 August 1929.
On 23 June 1936, he was appointed a personal aide-de-camp to his eldest brother, Edward VIII.
Following Edward's abdication and the accession of Albert as George VI, Henry was effectively retired from active duty and received a ceremonial promotion to major‐general on 1 January 1937, skipping three ranks.
Duke of Gloucester

On 31 March 1928, his father created him Duke of Gloucester, Earl of Ulster, and Baron Culloden, three titles that linked him with England, Northern Ireland, and Scotland.
Later that year, Henry visited Canada.
Before his marriage, Henry's chief ambition was to command his regiment, the 10th Royal Hussars, or at least to spend as much time in the Army as possible.
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
  AssignClass (5bc1991a-068e-4e82-8fda-a4347416bd7c)
 Call ID: 5bc1991a-068e-4e82-8fda-a4347416bd7c
  Args:
    type: :Man
    source: :Henry
  AssignClass (91d6765e-0318-4f11-90c2-3cff20b5fee1)
 Call ID: 91d6765e-0318-4f11-90c2-3cff20b5fee1
  Args:
    source: :Henry
    type: :Person
  AddLiteral (d5764410-d3d0-44a3-9a6d-133172dc27f0)
 Call ID: d5764410-d3d0-44a3-9a6d-133172dc27f0
  Args:
    literal_value: 1900
    literal_type: xsd:integer
    source: :Henry
    relation: :hasBirthYear
  AddLiteral (f7cb8190-c0b9-422d-a994-e8840c652d21)
 Call ID: f7cb8190-c0b9-422d-a994-e8840c652d21
  Args:
    literal_type: xsd:integer
    literal_value: 1974
    relation: :hasDeathYear
    source: :Henry
  AssignClass (258ce2b5-b70f-4f96-9a41-4ffe00ed3481)
 Call ID: 258ce2b5-b70f-4f96-9a41-4ffe00ed3481
  Args:
    type: :Man
    source: :GeorgeV
  AssignClass (e81f228a-966e-43b9-ad44-9797906b0f6c)
 Call ID: e81f228a-966e-43b9-ad44-9797906b0f6c
  Args:
    type: :Person
    source: :GeorgeV
  AssignClass (2284bbe6-b4c7-45d7-81a1-e652b9320cfd)
 Call ID: 2284bbe6-b4c7-45d7-81a1-e652b9320cfd
  Args:
    source: :QueenMary
    type: :Woman
  AssignClass (39dcf725-f155-453d-8f22-61df96c38f68)
 Call ID: 39dcf725-f155-453d-8f22-61df96c38f68
  Args:
    type: :Person
    source: :QueenMary
  AddTriple (515b5618-a375-4372-a6a8-bc7a10431179)
 Call ID: 515b5618-a375-4372-a6a8-bc7a10431179
  Args:
    relation: :hasFather
    source: :Henry
    target: :GeorgeV
  AddTriple (9067a875-12b9-44b3-b287-6902771ba18d)
 Call ID: 9067a875-12b9-44b3-b287-6902771ba18d
  Args:
    source: :Henry
    relation: :hasMother
    target: :QueenMary
  AssignClass (4f1434c9-8a31-424e-8d52-163625e79876)
 Call ID: 4f1434c9-8a31-424e-8d52-163625e79876
  Args:
    source: :EdwardVIII
    type: :Man
  AssignClass (2bb03b75-4a79-4b0e-9162-c0c8b64dd0fd)
 Call ID: 2bb03b75-4a79-4b0e-9162-c0c8b64dd0fd
  Args:
    source: :EdwardVIII
    type: :Person
  AssignClass (7f4f87a8-e84d-4d6a-9f4e-49403a975e5a)
 Call ID: 7f4f87a8-e84d-4d6a-9f4e-49403a975e5a
  Args:
    type: :Man
    source: :GeorgeVI
  AssignClass (674043f0-2948-4f83-b042-1ecea3cee1cf)
 Call ID: 674043f0-2948-4f83-b042-1ecea3cee1cf
  Args:
    source: :GeorgeVI
    type: :Person
  AddTriple (393c4ded-0f29-4a26-8e44-ddb22b98d3c2)
 Call ID: 393c4ded-0f29-4a26-8e44-ddb22b98d3c2
  Args:
    target: :EdwardVIII
    source: :Henry
    relation: :isBrotherOf
  AddTriple (c29deabc-a7e4-4a46-92b8-6be0fa5230a7)
 Call ID: c29deabc-a7e4-4a46-92b8-6be0fa5230a7
  Args:
    relation: :isBrotherOf
    source: :Henry
    target: :GeorgeVI
  AssignClass (fba9e7c1-ebe9-4490-a38c-eca454f66162)
 Call ID: fba9e7c1-ebe9-4490-a38c-eca454f66162
  Args:
    source: :AliceMontaguDouglasScott
    type: :Woman
  AssignClass (8e11782d-b914-4ca3-b232-cf3ae782d9dc)
 Call ID: 8e11782d-b914-4ca3-b232-cf3ae782d9dc
  Args:
    source: :AliceMontaguDouglasScott
    type: :Person
  AddLiteral (13533189-c3d7-43ac-b3fa-0eaa6f9fd2e1)
 Call ID: 13533189-c3d7-43ac-b3fa-0eaa6f9fd2e1
  Args:
    source: :Henry
    relation: :hasMarriageYear
    literal_value: 1935
    literal_type: xsd:integer
  AddTriple (48de73d5-090d-45f0-8162-efaecb0869ba)
 Call ID: 48de73d5-090d-45f0-8162-efaecb0869ba
  Args:
    target: :AliceMontaguDouglasScott
    relation: :hasRelation
    source: :Henry
  AssignClass (bc9e4e66-68d5-4b17-88de-05f3c762c44e)
 Call ID: bc9e4e66-68d5-4b17-88de-05f3c762c44e
  Args:
    source: :William
    type: :Man
  AssignClass (93d6b03e-0aef-49b4-831b-f33d1324fa40)
 Call ID: 93d6b03e-0aef-49b4-831b-f33d1324fa40
  Args:
    type: :Person
    source: :William
  AssignClass (3a88abf4-5cb8-4ca3-b12c-4ba42cf9fe9f)
 Call ID: 3a88abf4-5cb8-4ca3-b12c-4ba42cf9fe9f
  Args:
    source: :Richard
    type: :Man
  AssignClass (df5a6fe0-6b86-4e6c-8eb2-3020765ce144)
 Call ID: df5a6fe0-6b86-4e6c-8eb2-3020765ce144
  Args:
    type: :Person
    source: :Richard
  AddTriple (f034bb7a-4286-4c84-aa51-c8d92be21746)
 Call ID: f034bb7a-4286-4c84-aa51-c8d92be21746
  Args:
    relation: :hasSon
    source: :Henry
    target: :William
  AddTriple (8702d676-39d8-4239-8ae4-d398cbf0dd5a)
 Call ID: 8702d676-39d8-4239-8ae4-d398cbf0dd5a
  Args:
    target: :Richard
    source: :Henry
    relation: :hasSon
  AddTriple (89f6ae45-9f01-4d44-a661-987a974cd484)
 Call ID: 89f6ae45-9f01-4d44-a661-987a974cd484
  Args:
    relation: :hasMother
    source: :William
    target: :AliceMontaguDouglasScott
  AddTriple (10e8ef72-d532-4c44-9db5-dbc81c30cd97)
 Call ID: 10e8ef72-d532-4c44-9db5-dbc81c30cd97
  Args:
    target: :AliceMontaguDouglasScott
    source: :Richard
    relation: :hasMother
  AssignClass (1317778c-6ecf-40e1-af1d-bc03be8c871a)
 Call ID: 1317778c-6ecf-40e1-af1d-bc03be8c871a
  Args:
    type: :Man
    source: :DukeOfKent
  AssignClass (c4635af3-29b1-4092-823c-7cd00f84e2f0)
 Call ID: c4635af3-29b1-4092-823c-7cd00f84e2f0
  Args:
    source: :DukeOfKent
    type: :Person
  AddTriple (609bfd55-26c4-46bf-aee3-2c24214972cd)
 Call ID: 609bfd55-26c4-46bf-aee3-2c24214972cd
  Args:
    source: :Henry
    relation: :isBrotherOf
    target: :DukeOfKent
  AssignClass (b8b74d3f-230c-43dc-9353-9beefb19c200)
 Call ID: b8b74d3f-230c-43dc-9353-9beefb19c200
  Args:
    type: :Woman
    source: :ElizabethII
  AssignClass (7ab80a3d-2722-4e44-bbc2-a61b85660f96)
 Call ID: 7ab80a3d-2722-4e44-bbc2-a61b85660f96
  Args:
    source: :ElizabethII
    type: :Person
  AddTriple (b00ab1c9-2760-4586-905a-7480095b7a4e)
 Call ID: b00ab1c9-2760-4586-905a-7480095b7a4e
  Args:
    target: :Margaret
    relation: :isSiblingOf
    source: :ElizabethII
  AssignClass (8313a5d6-3778-4dbf-8fc4-1bd10e82a562)
 Call ID: 8313a5d6-3778-4dbf-8fc4-1bd10e82a562
  Args:
    type: :Woman
    source: :Margaret
  AssignClass (5051f062-e68f-4f1f-8a6b-68bb744172c1)
 Call ID: 5051f062-e68f-4f1f-8a6b-68bb744172c1
  Args:
    type: :Person
    source: :Margaret
  Finish (311893bb-2680-43f0-8893-9fd4415c18b4)
 Call ID: 311893bb-2680-43f0-8893-9fd4415c18b4
  Args: