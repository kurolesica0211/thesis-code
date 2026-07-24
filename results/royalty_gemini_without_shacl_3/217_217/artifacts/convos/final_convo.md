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
  AssignClass (04d9a221-ad65-4ccc-8184-d722976b1646)
 Call ID: 04d9a221-ad65-4ccc-8184-d722976b1646
  Args:
    type: :Man
    source: :GeorgeVI
  AssignClass (144d5402-8489-459d-ae79-b90cdbc70ba5)
 Call ID: 144d5402-8489-459d-ae79-b90cdbc70ba5
  Args:
    type: :Person
    source: :GeorgeVI
  AssignClass (7393a027-8507-4189-8406-3f9c081e2166)
 Call ID: 7393a027-8507-4189-8406-3f9c081e2166
  Args:
    source: :GeorgeVI
    type: :Ancestor
  AddLiteral (7bf30680-9dfb-459f-a633-fe68e8624fb6)
 Call ID: 7bf30680-9dfb-459f-a633-fe68e8624fb6
  Args:
    literal_type: xsd:integer
    literal_value: 1895
    relation: :hasBirthYear
    source: :GeorgeVI
  AddLiteral (adc36116-efad-4b30-8144-3c47105db6ce)
 Call ID: adc36116-efad-4b30-8144-3c47105db6ce
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1952
    source: :GeorgeVI
  AddLiteral (37af81d3-2e9b-48b5-9ee0-c1a1c1215b9d)
 Call ID: 37af81d3-2e9b-48b5-9ee0-c1a1c1215b9d
  Args:
    relation: :alsoKnownAs
    literal_value: Bertie
    source: :GeorgeVI
    literal_type: xsd:string
  AddLiteral (bc431f8c-6260-45e2-8e8e-a3ae8000e210)
 Call ID: bc431f8c-6260-45e2-8e8e-a3ae8000e210
  Args:
    relation: :knownAs
    literal_value: Albert Frederick Arthur George
    source: :GeorgeVI
    literal_type: xsd:string
  AssignClass (c961ccbf-0bc4-447d-8e29-a91816efe3a1)
 Call ID: c961ccbf-0bc4-447d-8e29-a91816efe3a1
  Args:
    source: :QueenVictoria
    type: :Woman
  AssignClass (42930d55-544a-4109-9f7c-df62cf1afdf2)
 Call ID: 42930d55-544a-4109-9f7c-df62cf1afdf2
  Args:
    source: :QueenVictoria
    type: :Person
  AssignClass (ccd867f5-c54c-4ba7-af69-8424bb1f1930)
 Call ID: ccd867f5-c54c-4ba7-af69-8424bb1f1930
  Args:
    source: :QueenVictoria
    type: :Ancestor
  AddTriple (9e7187bc-e7ba-4166-b13a-bf0707139344)
 Call ID: 9e7187bc-e7ba-4166-b13a-bf0707139344
  Args:
    target: :GeorgeVI
    relation: :isAncestorOf
    source: :QueenVictoria
  AssignClass (16c19cba-f9ba-4e77-b838-f772129fb34c)
 Call ID: 16c19cba-f9ba-4e77-b838-f772129fb34c
  Args:
    type: :Man
    source: :PrinceAlbertPrinceConsort
  AssignClass (70312215-0ecc-4610-82a2-f5e98aac0f2f)
 Call ID: 70312215-0ecc-4610-82a2-f5e98aac0f2f
  Args:
    type: :Person
    source: :PrinceAlbertPrinceConsort
  AssignClass (17a426b4-c377-4f67-a07e-d78d0f060b73)
 Call ID: 17a426b4-c377-4f67-a07e-d78d0f060b73
  Args:
    source: :PrinceAlbertPrinceConsort
    type: :Ancestor
  AddTriple (3d01e144-bab7-4faf-8395-def5c39c3666)
 Call ID: 3d01e144-bab7-4faf-8395-def5c39c3666
  Args:
    relation: :isAncestorOf
    source: :PrinceAlbertPrinceConsort
    target: :GeorgeVI
  AssignClass (0e00d431-1380-4446-9b08-a5e78e11b6df)
 Call ID: 0e00d431-1380-4446-9b08-a5e78e11b6df
  Args:
    source: :GeorgeV
    type: :Man
  AssignClass (716270b4-42a2-4802-b52f-081e3e8408d7)
 Call ID: 716270b4-42a2-4802-b52f-081e3e8408d7
  Args:
    type: :Person
    source: :GeorgeV
  AssignClass (55bb086e-ba1e-4de9-9dab-72ad7b745126)
 Call ID: 55bb086e-ba1e-4de9-9dab-72ad7b745126
  Args:
    type: :Ancestor
    source: :GeorgeV
  AddTriple (88f86321-57e0-434d-ad06-3f9ddce7fb52)
 Call ID: 88f86321-57e0-434d-ad06-3f9ddce7fb52
  Args:
    relation: :isFatherOf
    source: :GeorgeV
    target: :GeorgeVI
  AssignClass (66bd544c-eaaa-41ca-8149-51b6c42e6f0c)
 Call ID: 66bd544c-eaaa-41ca-8149-51b6c42e6f0c
  Args:
    type: :Woman
    source: :QueenMary
  AssignClass (8a65c9db-cd05-41e8-b05e-2a2cf2f4d55a)
 Call ID: 8a65c9db-cd05-41e8-b05e-2a2cf2f4d55a
  Args:
    source: :QueenMary
    type: :Person
  AssignClass (318677d1-8c3d-4cac-bcf4-3e12abbf5932)
 Call ID: 318677d1-8c3d-4cac-bcf4-3e12abbf5932
  Args:
    source: :QueenMary
    type: :Ancestor
  AddTriple (c13d5a7e-df71-404f-b3c0-adb45f5f180f)
 Call ID: c13d5a7e-df71-404f-b3c0-adb45f5f180f
  Args:
    source: :QueenMary
    relation: :isMotherOf
    target: :GeorgeVI
  AssignClass (bf54d1c5-bbba-4051-86e2-1c2512d70964)
 Call ID: bf54d1c5-bbba-4051-86e2-1c2512d70964
  Args:
    source: :LadyElizabethBowesLyon
    type: :Woman
  AssignClass (5a24a155-941d-471c-b5d9-f83a50bd0afe)
 Call ID: 5a24a155-941d-471c-b5d9-f83a50bd0afe
  Args:
    type: :Person
    source: :LadyElizabethBowesLyon
  AssignClass (6cce3b4c-dd70-4d0b-80a7-a10a5acf1f26)
 Call ID: 6cce3b4c-dd70-4d0b-80a7-a10a5acf1f26
  Args:
    type: :Ancestor
    source: :LadyElizabethBowesLyon
  AddTriple (0662e0d4-236e-440b-b959-f670e7bbd9ee)
 Call ID: 0662e0d4-236e-440b-b959-f670e7bbd9ee
  Args:
    target: :ElizabethII
    source: :GeorgeVI
    relation: :isFatherOf
  AddTriple (bdb25258-aa3b-43f2-8f84-b05eb91ae559)
 Call ID: bdb25258-aa3b-43f2-8f84-b05eb91ae559
  Args:
    target: :Margaret
    source: :GeorgeVI
    relation: :isFatherOf
  AddTriple (947c3397-1e40-4c27-926d-a5dde17d10aa)
 Call ID: 947c3397-1e40-4c27-926d-a5dde17d10aa
  Args:
    target: :ElizabethII
    relation: :isMotherOf
    source: :LadyElizabethBowesLyon
  AddTriple (553f5b4f-deff-4b6c-8b2b-fbf9014055d6)
 Call ID: 553f5b4f-deff-4b6c-8b2b-fbf9014055d6
  Args:
    source: :LadyElizabethBowesLyon
    relation: :isMotherOf
    target: :Margaret
  AddLiteral (dc933806-9023-46d3-ad69-f98b09501b4a)
 Call ID: dc933806-9023-46d3-ad69-f98b09501b4a
  Args:
    literal_type: xsd:integer
    literal_value: 1923
    relation: :hasMarriageYear
    source: :GeorgeVI
  AssignClass (a1bc0cc5-91ac-4c67-a138-72268d0409c8)
 Call ID: a1bc0cc5-91ac-4c67-a138-72268d0409c8
  Args:
    source: :EdwardVIII
    type: :Man
  AssignClass (5589a59a-5e71-4d01-b59f-784a94877093)
 Call ID: 5589a59a-5e71-4d01-b59f-784a94877093
  Args:
    type: :Person
    source: :EdwardVIII
  AddTriple (1eebeb52-a046-49cf-bfb6-cc9bece82e12)
 Call ID: 1eebeb52-a046-49cf-bfb6-cc9bece82e12
  Args:
    source: :GeorgeVI
    relation: :isSiblingOf
    target: :EdwardVIII
  AssignClass (5813c342-8ed5-44eb-8541-f6eaad66d540)
 Call ID: 5813c342-8ed5-44eb-8541-f6eaad66d540
  Args:
    source: :PrinceHenryDukeOfGloucester
    type: :Man
  AssignClass (b9064b16-e68a-4c1c-85bd-71b15908e8ac)
 Call ID: b9064b16-e68a-4c1c-85bd-71b15908e8ac
  Args:
    source: :PrinceHenryDukeOfGloucester
    type: :Person
  AddTriple (78f545c5-c11f-4a6c-98ba-d6a92c4ee10a)
 Call ID: 78f545c5-c11f-4a6c-98ba-d6a92c4ee10a
  Args:
    source: :GeorgeVI
    relation: :isSiblingOf
    target: :PrinceHenryDukeOfGloucester
  AssignClass (a2071136-e7f3-4be9-bd3d-39a06b94596f)
 Call ID: a2071136-e7f3-4be9-bd3d-39a06b94596f
  Args:
    type: :Man
    source: :PrinceGeorgeDukeOfKent
  AssignClass (e731d646-fc14-4c72-8299-10f109fa62e8)
 Call ID: e731d646-fc14-4c72-8299-10f109fa62e8
  Args:
    type: :Person
    source: :PrinceGeorgeDukeOfKent
  AddTriple (218f3b0f-b2bf-41be-81bc-1c9528394d51)
 Call ID: 218f3b0f-b2bf-41be-81bc-1c9528394d51
  Args:
    target: :PrinceGeorgeDukeOfKent
    source: :GeorgeVI
    relation: :isSiblingOf
  AssignClass (0b6d1768-9c01-4dfa-8d50-125f4d580ba8)
 Call ID: 0b6d1768-9c01-4dfa-8d50-125f4d580ba8
  Args:
    source: :ElizabethII
    type: :Woman
  AssignClass (c3fbbf5c-a461-40a9-93a7-1e273454e60d)
 Call ID: c3fbbf5c-a461-40a9-93a7-1e273454e60d
  Args:
    type: :Person
    source: :ElizabethII
  AssignClass (c8f2497a-369c-4e4a-b9b4-efd27548bd71)
 Call ID: c8f2497a-369c-4e4a-b9b4-efd27548bd71
  Args:
    source: :Margaret
    type: :Woman
  AssignClass (280131f2-2c9d-4530-b463-49f02f69e3a5)
 Call ID: 280131f2-2c9d-4530-b463-49f02f69e3a5
  Args:
    source: :Margaret
    type: :Person
  Finish (898ceaa1-dde8-43d2-a31f-fb57804bedf6)
 Call ID: 898ceaa1-dde8-43d2-a31f-fb57804bedf6
  Args: