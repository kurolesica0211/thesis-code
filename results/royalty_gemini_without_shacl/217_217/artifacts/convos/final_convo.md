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
George VI (Albert Frederick Arthur George; 14 December 1895 – 6 February 1952) was King of the United Kingdom and the Dominions of the British Commonwealth from 11 December 1936 until his death in 1952.
The future George VI was born during the reign of his great-grandmother Queen Victoria; he was named Albert at birth after his late great-grandfather Prince Albert of Saxe-Coburg and Gotha and was known as "Bertie" to his family and close friends.
His father ascended the throne as George V in 1910.
He married Lady Elizabeth Bowes-Lyon in 1923, and they had two daughters, Elizabeth and Margaret.
His elder brother ascended the throne as Edward VIII after their father died in 1936, but Edward abdicated later that year to marry the twice-divorced American socialite Wallis Simpson.
As heir presumptive to Edward VIII, Albert became king, taking the regnal name George VI.
George VI was seen as sharing the hardships of the common people and his popularity soared.
Buckingham Palace was bombed during the Blitz while the King and Queen were there, and his younger brother the Duke of Kent was killed on active service.
George became known as a symbol of British determination to win the war.
George relinquished the title of Emperor of India in June 1948 and instead adopted the new title of Head of the Commonwealth.
He was succeeded by his elder daughter, Elizabeth II.
Early life

Albert was born at 3:05 am on 14 December 1895 at York Cottage, on the Sandringham Estate in Norfolk, during the reign of his great-grandmother Queen Victoria.
His father was Prince George, Duke of York (later King George V), the second and only surviving son of the Prince and Princess of Wales (later King Edward VII and Queen Alexandra).
His mother, the Duchess of York (later Queen Mary), was the eldest child and only daughter of Francis, Duke of Teck, and Princess Mary Adelaide, Duchess of Teck.
His birth date coincided with the 34th anniversary of the death of his great-grandfather Albert, Prince Consort.
Uncertain of how the Prince Consort's widow, Queen Victoria, would take the news of the birth, the Prince of Wales wrote to the Duke of York that the Queen had been "rather distressed".
"


The Queen was mollified by the proposal to name the new baby Albert, and wrote to the Duchess of York: "I am all impatience to see the new one, born on such a sad day but rather more dear to me, especially as he will be called by that dear name which is a byword for all that is great and good."
Consequently, he was baptised "Albert Frederick Arthur George" at St Mary Magdalene Church, Sandringham on 17 February 1896.
Formally he was His Highness Prince Albert of York; within the royal family he was known informally as "Bertie".
Albert was fourth in line to the throne at birth, after his grandfather, father and elder brother, Edward.
Queen Victoria died on 22 January 1901, and the Prince of Wales succeeded her as King Edward VII.
Prince Albert moved up to third in line to the throne, after his father and elder brother.
Military career and education

Beginning in 1909, Albert attended the Royal Naval College, Osborne, as a naval cadet.
In 1911, he came bottom of the class in the final examination, but despite this he progressed to the Royal Naval College, Dartmouth.
When his grandfather Edward VII died in 1910, his father became King George V. Prince Edward became Prince of Wales, with Albert second in line to the throne.
In February 1918, Albert was appointed Officer in Charge of Boys at the Royal Naval Air Service's training establishment at Cranwell.
With the establishment of the Royal Air Force Albert transferred from the Royal Navy to the Royal Air Force.
He was the first member of the British royal family to be certified as a fully qualified pilot.
The prince qualified as an RAF pilot on 31 July 1919 and was promoted to squadron leader the following day.
On 4 June 1920, his father created him Duke of York, Earl of Inverness and Baron Killarney.
He began to take on more royal duties.
Through such visits he acquired the nickname of the "Industrial Prince".
His stutter, and his embarrassment over it, together with a tendency to shyness, caused him to appear less confident in public than his older brother, Edward.
That year, Albert met for the first time since childhood Lady Elizabeth Bowes-Lyon, the youngest daughter of the Earl and Countess of Strathmore.
Elizabeth rejected his proposal twice, in 1921 and 1922, reportedly because she was reluctant to make the sacrifices necessary to become a member of the royal family.
After a protracted courtship, Elizabeth agreed to marry him.
Albert and Elizabeth were married on 26 April 1923 at Westminster Abbey.
Albert's marriage to someone not of royal birth was considered a modernising gesture.
The newly formed British Broadcasting Company wished to record and broadcast the event on radio, but the Abbey Chapter vetoed the idea (although the Dean, Herbert Edward Ryle, was in favour).
From December 1924 to April 1925, the Duke and Duchess toured Kenya, Uganda, and the Sudan, travelling via the Suez Canal and Aden.
The Duke and Logue practised breathing exercises, and the Duchess rehearsed with him patiently.
The Duke and Duchess had two children, Elizabeth (called "Lilibet" by the family, later Elizabeth II) in 1926 and Margaret in 1930.
The family lived at White Lodge, Richmond Park, and then at 145 Piccadilly, rather than one of the royal palaces.
In 1931, the Canadian prime minister, R. B. Bennett, considered Albert for Governor General of Canada—a proposal that King George V rejected on the advice of the Secretary of State for Dominion Affairs, J. H. Thomas.
Reign

Reluctant king

King George V had severe reservations about Prince Edward, saying "After I am dead, the boy will ruin himself in twelve months" and "I pray God that my eldest son will never marry and that nothing will come between Bertie and Lilibet and the throne."
On 20 January 1936, George V died and Edward ascended the throne as King Edward VIII.
In the Vigil of the Princes, Prince Albert and his three brothers (the new king; Prince Henry, Duke of Gloucester; and Prince George, Duke of Kent) took a shift standing guard over their father's body as it lay in state, in a closed casket, in Westminster Hall.
As Edward was unmarried and had no children, Albert was the heir presumptive to the throne.
Less than a year later, on 11 December 1936, Edward abdicated in order to marry Wallis Simpson, who was divorced from her first husband and divorcing her second.
Edward had been advised by British prime minister Stanley Baldwin that he could not remain king and marry a divorced woman with two living ex-husbands.
The day before the abdication, Albert went to London to see his mother, Queen Mary.
"


On the day of Edward's abdication, the Oireachtas, the parliament of the Irish Free State, removed all direct mention of the monarch from the Irish constitution.
No evidence has been found to support the contemporaneous rumour that the government considered bypassing him, his children and his brother Prince Henry, in favour of their younger brother Prince George, Duke of Kent.
This seems to have been suggested on the grounds that Prince George was at that time the only brother with a son.
Early reign

Albert assumed the regnal name "George VI" to emphasise continuity with his father and restore confidence in the monarchy.
The beginning of George VI's reign was taken up by questions surrounding his predecessor and brother, whose titles, style and position were uncertain.
He had been introduced as "His Royal Highness Prince Edward" for the abdication broadcast, but George VI felt that by abdicating and renouncing the succession, Edward had lost the right to bear royal titles, including "Royal Highness".
In settling the issue, George's first act as king was to confer upon Edward the title "Duke of Windsor" with the style "Royal Highness", but the letters patent creating the dukedom prevented any wife or children from bearing royal styles.
George VI was forced to buy from Edward the royal residences of Balmoral Castle and Sandringham House, as these were private properties and did not pass to him automatically.
Three days after his accession, on his 41st birthday, he invested his wife, the new queen consort, with the Order of the Garter.
George VI's coronation at Westminster Abbey took place on 12 May 1937, the date previously intended for Edward's coronation.
In a break with tradition, Queen Mary attended the ceremony in a show of support for her son.
There was no Durbar held in Delhi for George VI, as had occurred for his father, as the cost would have been a burden to the Government of India.
Rising Indian nationalism made the welcome that the royal party would have received likely to be muted at best, and a prolonged absence from Britain would have been undesirable in the tense period before the Second World War.
The growing likelihood of war in Europe dominated the early reign of George VI.
When the King and Queen greeted Chamberlain on his return from negotiating the Munich Agreement in 1938, they invited him to appear on the balcony of Buckingham Palace with them.
This public association of the monarchy with a politician was exceptional, as balcony appearances were traditionally restricted to the royal family.
While broadly popular among the general public, Chamberlain's policy towards Hitler was the subject of some opposition in the House of Commons, which led historian and politician John Grigg to describe George's behaviour in associating himself so prominently with a politician as "the most unconstitutional act by a British sovereign in the present century".
In May and June 1939, the King and Queen toured Canada and the United States; it was the first visit of a reigning British monarch to North America, although George had been to Canada prior to his accession.
From Ottawa, George and Elizabeth were accompanied by Canadian prime minister Mackenzie King, to present themselves in North America as King and Queen of Canada.
Both Mackenzie King and the Canadian governor general, Lord Tweedsmuir, hoped that George's presence in Canada would demonstrate the principles of the Statute of Westminster 1931, which gave full sovereignty to the British Dominions.
On 19 May, George personally accepted and approved the letter of credence of the new U.S. ambassador to Canada, Daniel Calhoun Roper; gave royal assent to nine parliamentary bills; and ratified two   international treaties with the Great Seal of Canada.
The official royal tour historian, Gustave Lanctot, wrote "the Statute of Westminster had assumed full reality" and George gave a speech emphasising "the free and equal association of the nations of the Commonwealth".
Although the aim of the tour was mainly political, to shore up Atlantic support for the United Kingdom in any future war, the King and Queen were enthusiastically received by the public.
The fear that George would be compared unfavourably to his predecessor was dispelled.
A strong bond of friendship was forged between Roosevelt and the royal couple during the tour, which had major significance in the relations between the United States and the United Kingdom through the ensuing war years.
The King and Queen resolved to stay in London, despite German bombing raids.
They officially stayed in Buckingham Palace throughout the war, although they usually spent nights at Windsor Castle.
In defiance, the Queen declared: "I am glad we have been bombed.
The royal family were portrayed as sharing the same dangers and deprivations as the rest of the country.
In August 1942, the King's brother, the Duke of Kent, was killed on active service.
In 1940, Winston Churchill replaced Neville Chamberlain as prime minister, though personally George would have preferred to appoint Lord Halifax.
George related much of what the two discussed in his diary, which is the only extant first-hand account of these conversations.
Throughout the war, George and Elizabeth provided morale-boosting visits throughout the United Kingdom, visiting bomb sites, munitions factories, and troops.
George visited military forces abroad in France in December 1939, North Africa and Malta in June 1943, Normandy in June 1944, southern Italy in July 1944, and the Low Countries in October 1944.
George replied: "You should worry, when I meet him, I always think he's after mine!"
In an echo of Chamberlain's appearance, the King invited Churchill to appear with the royal family on the balcony to public acclaim.
In January 1946, George addressed the United Nations at its first assembly, which was held in London, and reaffirmed "our faith in the equal rights of men and women and of nations great and small".
Empire to Commonwealth

George VI's reign saw the acceleration of the dissolution of the British Empire.
George relinquished the title of Emperor of India, and became King of India and King of Pakistan instead.
In late April 1949, the Commonwealth leaders issued the London Declaration, which laid the foundation of the modern Commonwealth and recognised George as Head of the Commonwealth.
In 1947, George and his family toured southern Africa.
George was appalled, however, when instructed by the South African government to shake hands only with whites, and referred to his South African bodyguards as "the Gestapo".
Illness and death

The stress of the war had taken its toll on George's health, made worse by his heavy smoking, and subsequent development of lung cancer, as well as other ailments including arteriosclerosis and Buerger's disease.
His elder daughter and heir presumptive, Elizabeth, took on more royal duties as his health deteriorated.
The delayed tour was re-organised, with Princess Elizabeth and her husband, Philip, Duke of Edinburgh, taking the place of the King and Queen.
George was well enough to open the Festival of Britain in May 1951, but on 4 June it was announced that he would need immediate and complete rest for the next four weeks, despite the arrival of Haakon VII of Norway the following afternoon for an official visit.
In October 1951, Elizabeth and Philip undertook a month-long tour of Canada; the trip had been delayed for a week because of George's illness.
On 31 January 1952, against the advice of those close to him, George travelled to London Airport to see Elizabeth and Philip depart for their tour of Australia via Kenya.
His daughter returned to Britain from Kenya as Queen Elizabeth II.
From 9 February, George's coffin rested in St Mary Magdalene Church, Sandringham, before lying in state at Westminster Hall from 11 February.
His funeral took place at St George's Chapel, Windsor Castle, on 15 February.
He was interred initially in the Royal Vault, and was transferred to the King George VI Memorial Chapel inside St George's on 26 March 1969.
In 2002, fifty years after his death, the remains of his widow, Queen Elizabeth the Queen Mother, and the ashes of his younger daughter, Princess Margaret, who both died that year, were interred in the chapel alongside him.
In 2022, the remains of Queen Elizabeth II and her husband, Prince Philip, were also interred in the chapel.
Legacy

In the words of Labour Member of Parliament (MP) George Hardie, the abdication crisis of 1936 did "more for republicanism than fifty years of propaganda".
George VI wrote to his brother Edward that in the aftermath of the abdication he had reluctantly assumed "a rocking throne" and tried "to make it steady again".
The George Cross and the George Medal were founded at the King's suggestion during the Second World War to recognise acts of exceptional civilian bravery.
He bestowed the George Cross on the entire "island fortress of Malta" in 1943.
Colin Firth won an Academy Award for Best Actor for his performance as George VI in the 2010 film The King's Speech.
Titles, honours and arms

As Duke of York, Albert bore the royal arms of the United Kingdom differenced with a label of three points argent, the centre point bearing an anchor azure—a difference earlier awarded to his father, George V, when he was Duke of York, and then later awarded to his grandson Andrew Mountbatten-Windsor, when he bore the title Prince.
As king he bore the royal arms undifferenced.



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
  AssignClass (9d47db10-1fb1-4406-9227-c1548eb0e8a9)
 Call ID: 9d47db10-1fb1-4406-9227-c1548eb0e8a9
  Args:
    source: GeorgeVI
    type: :Man
  AssignClass (2327461b-17c9-47ba-83d5-0342d58589de)
 Call ID: 2327461b-17c9-47ba-83d5-0342d58589de
  Args:
    source: GeorgeVI
    type: :Person
  AddLiteral (2c2057d0-60dc-4801-924c-7c74c83554d8)
 Call ID: 2c2057d0-60dc-4801-924c-7c74c83554d8
  Args:
    literal_value: 1895
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: GeorgeVI
  AddLiteral (493797d0-f7f8-460f-a21e-5b9c9e2b890d)
 Call ID: 493797d0-f7f8-460f-a21e-5b9c9e2b890d
  Args:
    literal_value: 1952
    relation: :hasDeathYear
    source: GeorgeVI
    literal_type: xsd:integer
  AddLiteral (de7da3b6-a353-49ac-9159-08f38747b071)
 Call ID: de7da3b6-a353-49ac-9159-08f38747b071
  Args:
    source: GeorgeVI
    literal_type: xsd:string
    relation: :knownAs
    literal_value: Bertie
  AssignClass (6c3a6dde-14e9-4c56-8ab1-be728b0b1279)
 Call ID: 6c3a6dde-14e9-4c56-8ab1-be728b0b1279
  Args:
    source: GeorgeV
    type: :Man
  AssignClass (d92bcb20-af92-4a18-a906-3f9f56c73eb8)
 Call ID: d92bcb20-af92-4a18-a906-3f9f56c73eb8
  Args:
    source: GeorgeV
    type: :Person
  AddTriple (30fcbb2f-2184-476b-85fc-da660c11bdc9)
 Call ID: 30fcbb2f-2184-476b-85fc-da660c11bdc9
  Args:
    source: GeorgeVI
    relation: :hasFather
    target: GeorgeV
  AssignClass (57b93d6a-0f61-4713-87f2-6b696d90fe1f)
 Call ID: 57b93d6a-0f61-4713-87f2-6b696d90fe1f
  Args:
    source: QueenMary
    type: :Woman
  AssignClass (1e5f98e5-59a4-4fea-9ee7-42044a88e252)
 Call ID: 1e5f98e5-59a4-4fea-9ee7-42044a88e252
  Args:
    source: QueenMary
    type: :Person
  AddTriple (3b8c4afe-dad6-4e2b-acb0-1fbd13cb1c75)
 Call ID: 3b8c4afe-dad6-4e2b-acb0-1fbd13cb1c75
  Args:
    relation: :hasMother
    target: QueenMary
    source: GeorgeVI
  AssignClass (c5733ba0-e188-47ee-be73-8a2b1ca5479f)
 Call ID: c5733ba0-e188-47ee-be73-8a2b1ca5479f
  Args:
    source: ElizabethBowesLyon
    type: :Woman
  AssignClass (ceed060f-9011-4a4d-85a6-f12fb9803c82)
 Call ID: ceed060f-9011-4a4d-85a6-f12fb9803c82
  Args:
    source: ElizabethBowesLyon
    type: :Person
  AddTriple (6f5064a8-66d3-414d-b8d4-f9a3cfd9cd2e)
 Call ID: 6f5064a8-66d3-414d-b8d4-f9a3cfd9cd2e
  Args:
    source: GeorgeVI
    target: ElizabethBowesLyon
    relation: :hasRelation
  AddLiteral (ef76815e-5ff7-49de-b554-a0043f542724)
 Call ID: ef76815e-5ff7-49de-b554-a0043f542724
  Args:
    literal_type: xsd:integer
    source: GeorgeVI
    literal_value: 1923
    relation: :hasMarriageYear
  AssignClass (b120aed0-2982-436f-8ab4-42d3a09b8fcb)
 Call ID: b120aed0-2982-436f-8ab4-42d3a09b8fcb
  Args:
    source: ElizabethII
    type: :Woman
  AssignClass (deb6974b-2dbb-43a1-b015-9f0d5ff01c7f)
 Call ID: deb6974b-2dbb-43a1-b015-9f0d5ff01c7f
  Args:
    source: ElizabethII
    type: :Person
  AssignClass (8627b187-9861-4873-9306-3abb6534d668)
 Call ID: 8627b187-9861-4873-9306-3abb6534d668
  Args:
    source: Margaret
    type: :Woman
  AssignClass (7ef3c9f1-46d4-43e4-aed2-cbbd37827a6a)
 Call ID: 7ef3c9f1-46d4-43e4-aed2-cbbd37827a6a
  Args:
    source: Margaret
    type: :Person
  AddTriple (3c0854d5-ac77-4fea-bbe2-2d8570a9cc8c)
 Call ID: 3c0854d5-ac77-4fea-bbe2-2d8570a9cc8c
  Args:
    relation: :hasDaughter
    target: ElizabethII
    source: GeorgeVI
  AddTriple (064bab26-1690-4dd7-8798-38d112ae8445)
 Call ID: 064bab26-1690-4dd7-8798-38d112ae8445
  Args:
    target: Margaret
    relation: :hasDaughter
    source: GeorgeVI
  AssignClass (0c2f3dc0-0396-4fd1-8c2d-247282fe715b)
 Call ID: 0c2f3dc0-0396-4fd1-8c2d-247282fe715b
  Args:
    source: EdwardVIII
    type: :Man
  AssignClass (e687e1dc-a792-4d60-b6fe-6e86b9de6943)
 Call ID: e687e1dc-a792-4d60-b6fe-6e86b9de6943
  Args:
    source: EdwardVIII
    type: :Person
  AddTriple (531e0cc6-9ac6-46bf-81e9-830ce09a7780)
 Call ID: 531e0cc6-9ac6-46bf-81e9-830ce09a7780
  Args:
    source: GeorgeVI
    target: EdwardVIII
    relation: :hasBrother
  AssignClass (744071ac-bc0c-43f1-acd1-a4fdca6ce27a)
 Call ID: 744071ac-bc0c-43f1-acd1-a4fdca6ce27a
  Args:
    source: DukeOfKent
    type: :Man
  AssignClass (8c3ae3f2-37c0-4c7f-b3f1-b9936c266822)
 Call ID: 8c3ae3f2-37c0-4c7f-b3f1-b9936c266822
  Args:
    source: DukeOfKent
    type: :Person
  AddTriple (a3df6eb9-77c9-4ec4-90fe-88b4f95e84cc)
 Call ID: a3df6eb9-77c9-4ec4-90fe-88b4f95e84cc
  Args:
    source: GeorgeVI
    relation: :hasBrother
    target: DukeOfKent
  AssignClass (5541bff4-d5d7-4bf8-a94e-f8c9fe87ad6f)
 Call ID: 5541bff4-d5d7-4bf8-a94e-f8c9fe87ad6f
  Args:
    source: PrinceHenry
    type: :Man
  AssignClass (eba22f7e-e179-431f-8a16-3af69419f96e)
 Call ID: eba22f7e-e179-431f-8a16-3af69419f96e
  Args:
    source: PrinceHenry
    type: :Person
  AddTriple (87630a76-77fe-49ec-8284-bdef50c55028)
 Call ID: 87630a76-77fe-49ec-8284-bdef50c55028
  Args:
    target: PrinceHenry
    relation: :hasBrother
    source: GeorgeVI
  AssignClass (22e6c885-0716-491e-8bb8-24ef2a1083e0)
 Call ID: 22e6c885-0716-491e-8bb8-24ef2a1083e0
  Args:
    source: QueenVictoria
    type: :Woman
  AssignClass (a0e8929a-e901-4fe7-a807-249a3543155f)
 Call ID: a0e8929a-e901-4fe7-a807-249a3543155f
  Args:
    source: QueenVictoria
    type: :Person
  AddTriple (cf5a1744-115a-493b-89f6-3dda12a06ac0)
 Call ID: cf5a1744-115a-493b-89f6-3dda12a06ac0
  Args:
    relation: :hasAncestor
    target: QueenVictoria
    source: GeorgeVI
  AssignClass (4967ee7e-d208-425f-9b92-21dc184bef16)
 Call ID: 4967ee7e-d208-425f-9b92-21dc184bef16
  Args:
    source: PrinceAlbertPrinceConsort
    type: :Man
  AssignClass (6336df64-4bad-41d3-9d4b-2807c838e756)
 Call ID: 6336df64-4bad-41d3-9d4b-2807c838e756
  Args:
    source: PrinceAlbertPrinceConsort
    type: :Person
  AddTriple (d327c609-b089-45da-bbb5-33d517ac0e9b)
 Call ID: d327c609-b089-45da-bbb5-33d517ac0e9b
  Args:
    target: PrinceAlbertPrinceConsort
    relation: :hasAncestor
    source: GeorgeVI
  Finish (0a4a903e-d3e8-4285-aae9-1ad761acbd6e)
 Call ID: 0a4a903e-d3e8-4285-aae9-1ad761acbd6e
  Args: