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
Victoria Eugenie Julia Ena of Battenberg (24 October 1887 – 15 April 1969), commonly known as Ena, was Queen of Spain as the wife of King Alfonso XIII from their marriage on 31 May 1906 until 14 April 1931, when the Second Spanish Republic was proclaimed.
A princess of the Grand Duchy of Hesse by birth, she was a member of the Battenberg family, a morganatic branch of the House of Hesse-Darmstadt.
She was the youngest granddaughter of Queen Victoria and Prince Albert of Saxe-Coburg and Gotha.
Unlike most members of the Battenberg family, who bore the style of Serene Highness, Victoria Eugenie was born with the style of Highness, by virtue of a royal warrant issued by Queen Victoria in 1886.
Early life

Victoria Eugenie of Battenberg was born on 24 October 1887 at Balmoral Castle in Aberdeenshire, Scotland.
Her father was Prince Henry of Battenberg, the fourth child and third son of Prince Alexander of Hesse and by Rhine and Julia, Princess of Battenberg, and her mother was Princess Beatrice, the fifth daughter of Queen Victoria of the United Kingdom and Prince Albert of Saxe-Coburg and Gotha.
Victoria Eugenie was the last grandchild of a British monarch to be born in Scotland until Princess Margaret was born at Glamis Castle in Angus in August 1930.
As Prince Henry was the product of a morganatic marriage, he took his style of Prince of Battenberg from his mother, who had been created Princess of Battenberg in her own right.
As such, Henry's children would normally have been born with the style "Serene Highness"; however, Queen Victoria had issued a Royal Warrant on 4 December 1886 granting the higher style of "Highness" to all sons and daughters of Prince Henry and Princess Beatrice, thus she was born Her Highness Princess Victoria Eugenie of Battenberg.
To her family, and the British general public, she was known by a diminutive of the last of her names, as Ena.
She was born in the 50th year of Queen Victoria's reign, so she was called "the Jubilee baby".
Her godparents were Empress Eugénie (represented by Princess Frederica of Hanover), the German Crown Princess (her maternal aunt; represented by the Duchess of Roxburghe), the Princess of Battenberg (her paternal grandmother; represented by the Marchioness of Ely), Princess Christian of Schleswig-Holstein (her maternal aunt; represented by the Countess of Erroll), Prince Louis of Battenberg (her paternal uncle; represented by the Earl of Hopetoun) and the Duke of Edinburgh (her maternal uncle; represented by Sir Henry Ponsonby).
Ena grew up in Queen Victoria's household, as the British monarch had reluctantly allowed Beatrice to marry on the condition that she remain her mother's full-time companion and personal secretary.
When she was six, Ena suffered a severe concussion when she was thrown off her pony at Osborne and hit her head on the ground.
Queen Victoria's physicians noticed "dangerous symptoms", such as "evident signs of brain pressure, probably a haemorrhage".
Her aunt Victoria, Princess Royal, wrote, "it is so grievous that  cannot take notice or open her eyes".
Ena was close to her grandmother Queen Victoria.
She reflected that "having been born and brought up in her home, Queen Victoria was like a second mother to us.
When Ena said, "I think it is time for us to go to bed", Queen Victoria corrected her.
"Young woman, a princess should say, 'I think it is time for me to retire'.
Queen Victoria wrote that "I love these darling children so, almost as much as their own parent" and referred to Ena as "the little treasure".
After the death of Queen Victoria in 1901, her mother and her family moved out of Osborne House and took up residence in Kensington Palace in London.
Princess Beatrice inherited Osborne Cottage on the Isle of Wight from her mother.
Engagement and wedding

In 1905, King Alfonso XIII of Spain made an official state visit to the United Kingdom.
Ena's maternal uncle, King Edward VII, hosted a dinner in Buckingham Palace in honour of the Spanish monarch.
Alfonso was seated between Queen Alexandra and Princess Helena, King Edward's sister.
He noticed Ena and asked who the dinner guest with almost white hair was.
Everybody knew that King Alfonso was looking for a suitable bride and one of the strongest candidates was Princess Patricia of Connaught, another niece of King Edward.
As Princess Patricia seemed not to be impressed by the Spanish monarch, Alfonso indulged his interest in Ena, and so the courtship began.
When Alfonso returned to Spain he frequently sent postcards to Ena and spoke of her approvingly.
His mother, Queen Maria Christina, did not like her son's choice, in part because she considered the Battenbergs non-royal because of the obscure origin of Prince Henry's mother, and in part because she wanted her son to marry within her own family.
Other obstacles to a marriage were religion (Alfonso was Roman Catholic, and Ena was Anglican); and, the potential problem of haemophilia, the disease that Queen Victoria had transmitted to some of her descendants.
Ena's brother, Leopold, was a haemophiliac, so there was a 50% probability that she would be a carrier, although the degree of risk was not yet known.
Still, if Alfonso married her, their issue could be affected by the disease.
Nonetheless, Alfonso was not dissuaded.
After a year of rumours about which princess Alfonso would marry, his mother finally acceded to her son's selection in January 1906 and wrote a letter to Ena's mother, telling her about the love Alfonso felt for her daughter and seeking unofficial contact with the king.
Princess Beatrice and her daughter arrived in Biarritz on 22 January and stayed at the Villa Mauriscot where some days later King Alfonso met them.
At the Villa Mauriscot, Alfonso and his future bride conducted a chaperoned, three-day romance.
Then, Alfonso took Ena and her mother to San Sebastián to meet Queen Maria Christina.
On 3 February, the king left San Sebastian to go to Madrid and Ena and her mother went to Versailles where the Princess would be instructed in the Catholic faith: as the future Queen of Spain, she agreed to convert.
The official reception of Ena into the Catholic faith took place on 5 March 1906 at Miramar Palace in San Sebastián.
The treaty was executed between Spain and the United Kingdom in London on 7 May 1906 by their respective plenipotentiaries, the Spanish Ambassador to the Court of St James's, Don Luis Polo de Bernabé, and the British Foreign Secretary, Sir Edward Grey, Bt.
Among other conditions, the treaty stipulated:


BE it known unto all men by these Presents that whereas His Catholic Majesty Alfonso XIII, King of Spain, has judged it proper to announce his intention of contracting a marriage with Her Royal Highness Princess Victoria Eugénie Julia Ena, niece of His Majesty Edward VII, King of the United Kingdom of Great Britain and Ireland and of the British Dominions beyond the Seas, Emperor of India, and daughter of Her Royal Highness the Princess Beatrice Mary Victoria Feodore (Princess Henry of Battenberg)...
It is concluded and agreed that the marriage between His said Majesty King Alfonso XIII and
Her said Royal Highness the Princess Victoria Eugénie Julia Ena shall be solemnized in person at Madrid as soon as the same may conveniently be done.
His said Majesty King Alfonso XIII engages to secure to Her said Royal Highness the Princess Victoria Eugénie Julia
Ena from the date of her marriage with His Majesty, and for the whole period of the marriage, an annual grant of 450,000 pesetas.
His said Majesty King Alfonso XIII also engages, if, by the will of Divine Providence, the said Princess Victoria Eugénie Julia Ena should become his widow, to secure to her, from the date of his death, an annual grant of 250,000 pesetas, unless and until she contracts a second marriage, both these grants having already been voted by the Cortes.
The High Contracting Parties take note of the fact that Her Royal Highness the Princess Victoria Eugénie Julia Ena, according to the due tenor of the law of England, forfeits for ever all hereditary rights of succession to the Crown and Government of Great Britain...
The treaty's reference to the forfeiture of Ena's British succession rights reflected neither any British government censure of the alliance nor any renunciation made by her.
Rather, it was an explicit recognition of the fact that by marrying (and becoming) a Roman Catholic, Ena lost any right to inherit the British crown as a consequence of Britain's Act of Settlement 1701.
Despite this treaty, concern about the reaction to the marriage and to Ena's conversion among Protestants was accommodated by the British government's decision that King Edward need not grant official consent to the marriage in his Privy Council, despite the fact that his niece was a British subject.
Although the naturalisation of Ena's father in the United Kingdom had been initiated in Parliament a week prior to his marriage to Princess Beatrice, the nuptials were completed before the naturalisation, thus the government was able to take the position that Ena was not bound by the Royal Marriages Act 1772, and therefore the British king had legal authority neither to authorise nor forbid her marriage.
The king did, however, issue a royal warrant which read:


"Our Will and Pleasure is and we do hereby declare and ordain that from and after the date of this Warrant our Most Dear Niece Princess Victoria Eugénie Julia Ena, only daughter of Our Most Dear Sister Beatrice Mary Victoria Feodore (Princess Henry of Battenberg) shall be styled entitled and called Her Royal Highness before her name and such Titles and Appellations which to her belong in all Deeds Records Instruments or Documents whatsoever wherein she may at any time hereafter be named or described.
The KING has been graciously pleased to declare and ordain that His Majesty's niece, Her Highness Princess Victoria Eugenie Julia Ena, daughter of Her Royal Highness the Princess Beatrice Mary Victoria Feodore (Princess Henry of Battenberg), shall henceforth be styled and called 'Her Royal Highness'; And to command that the said Royal concession and declaration be registered in His Majesty's College of Arms."

Princess Ena married King Alfonso XIII at the Royal Monastery of San Jerónimo in Madrid on 31 May 1906.
Present at the ceremony were her widowed mother and brothers, as well as her cousins, the Prince and Princess of Wales.
Ena's life was saved because, at the exact moment the bomb exploded, she turned her head in order to see St. Mary's Church, which Alfonso was showing her.
His bride, with a Spanish venia and an English coat of arms, is Doña Victoria Eugenia.
King Alfonso, King of Spain, you know that Madrid loves you.
, Ena became isolated from the Spanish people and was unpopular in her new land.
Her married life improved when she gave birth to a son and heir apparent to the kingdom, Alfonso, Prince of Asturias.
However, while the baby prince was being circumcised, the doctors noted that he did not stop bleeding — the first sign that the infant heir had haemophilia.
Ena was the obvious source of the condition, which was inherited by her eldest and youngest sons.
Contrary to the response of Emperor Nicholas II of Russia, whose son and heir by another granddaughter of Queen Victoria was similarly afflicted, Alfonso is alleged never to have forgiven Ena nor to have come to terms with what had happened.
In all, King Alfonso XIII and Queen Ena had seven children, five sons and two daughters.
After the births of their children, Ena's relationship with Alfonso deteriorated, and he had numerous affairs.
It has been said that he had a dalliance with the Queen's cousin, Beatrice, Duchess of Galliera, but this is disputed.
Then members of the king's circle spread rumours that Beatrice had been expelled because of her bad behaviour, which was not true.
Ena disliked Spanish religious conservatism and the customs of the Royal Court, such as bullfighting, describing it as a cruel spectacle typical of a backward people like the Spanish.
Later she confided to her grandson Juan Carlos's then-fiancée, Princess Sofía of Greece and Denmark, that she was forced to attend and pretend to enjoy bullfights.
When the Greek princess replied that no one would force her to watch bullfights, Ena replied: "You can't refuse, they will force you".
Feeling increasingly isolated, Ena turned to her passion for collecting jewellery.
Ena also devoted herself to work for hospitals and services for the poor, as well as to education.
Various Spanish landmarks have been named after Ena.
For instance, in 1909, Madrid's stately neoclassical bridge crossing the Manzanares River was named after her as the "Puente de la Reina Victoria".
In 1912, the monumental opera house and theatre "Teatro Victoria Eugenia" in San Sebastián, Spain, was named after her.
In 1920, she launched the Spanish Navy cruiser Reina Victoria Eugenia which was named after her.
In 1923, the Pope conferred upon her the Golden Rose which was the first time this honour had been awarded to a British princess since 1555 when Pope Julius III conferred one upon Queen Mary I of England.
She was also granted the Royal Order of Victoria and Albert by her grandmother, Queen Victoria.
Alfonso XIII had hoped that his voluntary exile might avert a civil war between the Republicans and the Monarchists.
Ena and Alfonso later separated, and she lived partly in the UK and in Switzerland.
A soccer enthusiast, Ena frequently attended matches and in exile received the Real Madrid delegation in Vieille Fontaine.
In 1938, the whole family gathered in Rome for the baptism at the Palazzo Malta of Alfonso and Ena's son Juan's eldest son, Juan Carlos, by Vatican Cardinal Secretary of State Eugenio Pacelli (who stood in for the dying Pope Pius XI and would himself become Pope Pius XII in a few months).
On 15 January 1941, Alfonso, feeling his death was near, transferred his rights to the Spanish crown to his son, the Count of Barcelona.
On 12 February, Alfonso suffered a first heart attack and died on 28 February 1941.
In 1942, Ena was obliged to leave Italy, having become persona non grata to the Italian government, according to Harold H. Tittmann Jr., a U.S. representative at the Vatican at the time, for her "ill-disguised leanings to the Allied cause".
Ena returned briefly to Spain in February 1968, to stand as godmother at the baptism of her great-grandson, Infante Felipe, the son of Infante Juan Carlos and Infanta Sofía.
Felipe became King of Spain after his father, King Juan Carlos I, abdicated in June 2014.
Ena Eugenie died in Lausanne on 15 April 1969, aged 81, exactly 38 years after she had left Spain for exile.
She was the last surviving child of Princess Beatrice and Prince Henry of Battenberg.
On 25 April 1985, her remains were returned to Spain and re-interred in the Royal Vault in the Escorial, outside Madrid, next to the remains of her husband, Alfonso XIII, and not far from her sons, Infante Alfonso, Infante Jaime, and Infante Gonzalo.
Legacy

After the death of Spanish dictator Francisco Franco in 1975, the monarchy was restored and Ena's grandson, Juan Carlos I, became King of Spain; her great-grandson, Felipe VI, is the current king.
Her godchildren included the Prince of Monaco, Queen Fabiola of Belgium, and Cayetana Fitz-James Stuart, 18th Duchess of Alba.
Ena left eight important pieces of jewellery written in her will that, following her instructions, would be transmitted privately to the head of the royal family successively to be worn by the following Queens of Spain.
The jewellery collection, known as the joyas de pasar, includes her Ansorena fleur-de-lis tiara  given to her by Alfonso XIII as a wedding gift in addition to other wedding gift jewellery from the King.
She left her other jewels to be distributed between her daughters Infanta Beatriz and Infanta María Cristina –who received Victoria Eugenie's Cartier tiara of diamonds set with pearls (or alternatively with emeralds)–.
The jewels in the collection are currently the most important of the royal family and are worn by the Queen of Spain on solemn occasions.
A sapphire ring owned by Ena was sold at Sotheby's in May 2012 for $50,000.
That same year, Sotheby's also sold at auction Victoria Eugenie's diamond and pink conch shell bracelet by Cartier for $3.4 million.
In 2025, a Spanish series called Ena.
Queen Victoria Eugenia was released in Finland, Portugal and Spain.



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
  AssignClass (cb80f707-69c7-4983-b19c-a796602b1bb6)
 Call ID: cb80f707-69c7-4983-b19c-a796602b1bb6
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (62c21af3-f4f6-465e-b23a-d762a34f82eb)
 Call ID: 62c21af3-f4f6-465e-b23a-d762a34f82eb
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AddLiteral (7bb41d23-3ab3-4824-94e7-14ddb898cea5)
 Call ID: 7bb41d23-3ab3-4824-94e7-14ddb898cea5
  Args:
    literal_value: Ena
    source: Victoria_Eugenie_of_Battenberg
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (1a53d47e-055b-44a6-ae44-fb48976256f5)
 Call ID: 1a53d47e-055b-44a6-ae44-fb48976256f5
  Args:
    source: Victoria_Eugenie_of_Battenberg
    literal_value: 1887
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (33d4dc9c-f737-4e42-b141-3f291d1af46e)
 Call ID: 33d4dc9c-f737-4e42-b141-3f291d1af46e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Victoria_Eugenie_of_Battenberg
    literal_value: 1969
  AssignClass (8bdb8105-52de-404d-b6fc-1bcf5f7798f6)
 Call ID: 8bdb8105-52de-404d-b6fc-1bcf5f7798f6
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (591d4a93-b972-4c4e-a5e8-bf2533ebb1f5)
 Call ID: 591d4a93-b972-4c4e-a5e8-bf2533ebb1f5
  Args:
    source: Alfonso_XIII
    type: :Person
  AddLiteral (5fdd24f0-fbb5-4de3-a056-252feeee5a39)
 Call ID: 5fdd24f0-fbb5-4de3-a056-252feeee5a39
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Victoria_Eugenie_of_Battenberg
    literal_value: 1906
  AddTriple (908a2761-c553-48cd-a9f9-f2886ced93f1)
 Call ID: 908a2761-c553-48cd-a9f9-f2886ced93f1
  Args:
    target: Alfonso_XIII
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasRelation
  AssignClass (836bd5a8-b8b0-44aa-bf04-f02d251a8f86)
 Call ID: 836bd5a8-b8b0-44aa-bf04-f02d251a8f86
  Args:
    source: Prince_Henry_of_Battenberg
    type: :Man
  AssignClass (d0ab1b4b-f022-4a48-967f-5ef4c08569d9)
 Call ID: d0ab1b4b-f022-4a48-967f-5ef4c08569d9
  Args:
    type: :Ancestor
    source: Prince_Henry_of_Battenberg
  AssignClass (75d77a58-d374-4562-a2c0-3fa9c4392818)
 Call ID: 75d77a58-d374-4562-a2c0-3fa9c4392818
  Args:
    type: :Person
    source: Prince_Henry_of_Battenberg
  AssignClass (d806c28b-ba4c-4efb-a04b-8169f1e4d1ea)
 Call ID: d806c28b-ba4c-4efb-a04b-8169f1e4d1ea
  Args:
    source: Princess_Beatrice
    type: :Woman
  AssignClass (6bfe505c-cb6a-4d22-9eda-e210e8118765)
 Call ID: 6bfe505c-cb6a-4d22-9eda-e210e8118765
  Args:
    source: Princess_Beatrice
    type: :Ancestor
  AssignClass (2a5a06c0-d4fe-41ee-b066-c558e8457784)
 Call ID: 2a5a06c0-d4fe-41ee-b066-c558e8457784
  Args:
    type: :Person
    source: Princess_Beatrice
  AddTriple (6f48a621-7326-41fe-a009-56fd921e6d75)
 Call ID: 6f48a621-7326-41fe-a009-56fd921e6d75
  Args:
    relation: :hasFather
    target: Prince_Henry_of_Battenberg
    source: Victoria_Eugenie_of_Battenberg
  AddTriple (5ed839cc-dba5-4762-9803-cc70998a2bdc)
 Call ID: 5ed839cc-dba5-4762-9803-cc70998a2bdc
  Args:
    source: Victoria_Eugenie_of_Battenberg
    target: Princess_Beatrice
    relation: :hasMother
  AssignClass (d06d4dee-46f6-49e1-8d74-c95bfbaa24c0)
 Call ID: d06d4dee-46f6-49e1-8d74-c95bfbaa24c0
  Args:
    type: :Man
    source: Prince_Alexander_of_Hesse_and_by_Rhine
  AssignClass (9864d0e5-83f1-4a41-9b15-5cd4baadab87)
 Call ID: 9864d0e5-83f1-4a41-9b15-5cd4baadab87
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Ancestor
  AssignClass (e10a5507-deea-465a-84f1-d1365094fe1a)
 Call ID: e10a5507-deea-465a-84f1-d1365094fe1a
  Args:
    source: Prince_Alexander_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (88dd0529-00fe-4cee-a364-d53ab8cdcc1f)
 Call ID: 88dd0529-00fe-4cee-a364-d53ab8cdcc1f
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Woman
  AssignClass (261f8ab9-468f-4eef-909e-2a47d4b2350f)
 Call ID: 261f8ab9-468f-4eef-909e-2a47d4b2350f
  Args:
    source: Julia_Princess_of_Battenberg
    type: :Ancestor
  AssignClass (24d40787-fe8d-4831-8f82-31b17aaf9794)
 Call ID: 24d40787-fe8d-4831-8f82-31b17aaf9794
  Args:
    type: :Person
    source: Julia_Princess_of_Battenberg
  AddTriple (6e949de3-6687-4f15-bc53-f39a04558c71)
 Call ID: 6e949de3-6687-4f15-bc53-f39a04558c71
  Args:
    relation: :hasFather
    target: Prince_Alexander_of_Hesse_and_by_Rhine
    source: Prince_Henry_of_Battenberg
  AddTriple (aeda1b81-482e-436f-a49f-f5a406fe4004)
 Call ID: aeda1b81-482e-436f-a49f-f5a406fe4004
  Args:
    target: Julia_Princess_of_Battenberg
    source: Prince_Henry_of_Battenberg
    relation: :hasMother
  AssignClass (127fa729-b455-4b79-9646-4af025aa564a)
 Call ID: 127fa729-b455-4b79-9646-4af025aa564a
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (a17d9d7c-407a-4492-b96a-e8380cd4a03f)
 Call ID: a17d9d7c-407a-4492-b96a-e8380cd4a03f
  Args:
    type: :Ancestor
    source: Queen_Victoria
  AssignClass (ed9bfa5f-8f86-4e60-9544-1d7ac1de95c9)
 Call ID: ed9bfa5f-8f86-4e60-9544-1d7ac1de95c9
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (08c95540-4e0a-437f-a8a1-708007774216)
 Call ID: 08c95540-4e0a-437f-a8a1-708007774216
  Args:
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
    type: :Man
  AssignClass (278b9653-a9e7-4e9c-a5c7-bd98d3f49685)
 Call ID: 278b9653-a9e7-4e9c-a5c7-bd98d3f49685
  Args:
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
    type: :Ancestor
  AssignClass (25958523-9a3d-4e61-9f7f-7279d1e630c3)
 Call ID: 25958523-9a3d-4e61-9f7f-7279d1e630c3
  Args:
    type: :Person
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
  AddTriple (23aed7c7-453a-449d-b0fd-8793e6d2faaa)
 Call ID: 23aed7c7-453a-449d-b0fd-8793e6d2faaa
  Args:
    relation: :hasFather
    target: Prince_Albert_of_Saxe-Coburg_and_Gotha
    source: Princess_Beatrice
  AddTriple (938a3852-8e38-4eed-aeca-34204782ccc1)
 Call ID: 938a3852-8e38-4eed-aeca-34204782ccc1
  Args:
    relation: :hasMother
    source: Princess_Beatrice
    target: Queen_Victoria
  AssignClass (64eb1c91-7d43-47a9-bf3f-cace795846c9)
 Call ID: 64eb1c91-7d43-47a9-bf3f-cace795846c9
  Args:
    type: :Man
    source: Leopold
  AssignClass (88d7ff70-5d8f-4f81-8ab6-8e8b7ac0bd67)
 Call ID: 88d7ff70-5d8f-4f81-8ab6-8e8b7ac0bd67
  Args:
    source: Leopold
    type: :Person
  AddTriple (30818851-25ae-49fb-9a1e-d6c15fc2fcbd)
 Call ID: 30818851-25ae-49fb-9a1e-d6c15fc2fcbd
  Args:
    source: Victoria_Eugenie_of_Battenberg
    target: Leopold
    relation: :isSiblingOf
  AssignClass (9f83a3ae-9a50-493f-b64a-760c0b4fc7ea)
 Call ID: 9f83a3ae-9a50-493f-b64a-760c0b4fc7ea
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (a9bad651-71b3-413b-b94d-f6cb55fb5b37)
 Call ID: a9bad651-71b3-413b-b94d-f6cb55fb5b37
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Person
  AddTriple (435d4136-e916-4b9b-ba96-530f01edcc0e)
 Call ID: 435d4136-e916-4b9b-ba96-530f01edcc0e
  Args:
    target: Victoria_Eugenie_of_Battenberg
    source: Alfonso_Prince_of_Asturias
    relation: :hasMother
  AddTriple (df164d15-9281-49f2-a01b-160cbb20e203)
 Call ID: df164d15-9281-49f2-a01b-160cbb20e203
  Args:
    relation: :hasFather
    target: Alfonso_XIII
    source: Alfonso_Prince_of_Asturias
  AssignClass (01737ff7-9006-42d5-bf01-487ad7307335)
 Call ID: 01737ff7-9006-42d5-bf01-487ad7307335
  Args:
    type: :Man
    source: Juan_Count_of_Barcelona
  AssignClass (5b1d951c-7051-4ce8-8d37-8aaa059bab56)
 Call ID: 5b1d951c-7051-4ce8-8d37-8aaa059bab56
  Args:
    source: Juan_Count_of_Barcelona
    type: :Person
  AddTriple (51dc4c56-aa52-4540-85aa-72440bb5b51e)
 Call ID: 51dc4c56-aa52-4540-85aa-72440bb5b51e
  Args:
    source: Juan_Count_of_Barcelona
    target: Victoria_Eugenie_of_Battenberg
    relation: :hasMother
  AddTriple (382ba2f3-f2a0-48c6-8da5-363b4f595844)
 Call ID: 382ba2f3-f2a0-48c6-8da5-363b4f595844
  Args:
    relation: :hasFather
    target: Alfonso_XIII
    source: Juan_Count_of_Barcelona
  AssignClass (e4479894-0789-4e25-8701-6cd6e3ca00e2)
 Call ID: e4479894-0789-4e25-8701-6cd6e3ca00e2
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (d618fa5f-e85f-4e45-bd9e-289e97ce4e37)
 Call ID: d618fa5f-e85f-4e45-bd9e-289e97ce4e37
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (86d782d3-e215-4fe0-879c-0fe26dcda6e3)
 Call ID: 86d782d3-e215-4fe0-879c-0fe26dcda6e3
  Args:
    relation: :hasFather
    source: Juan_Carlos_I
    target: Juan_Count_of_Barcelona
  AssignClass (43ba8fee-b7b2-454f-a2b0-3c0041a9c9e8)
 Call ID: 43ba8fee-b7b2-454f-a2b0-3c0041a9c9e8
  Args:
    source: Infante_Felipe
    type: :Man
  AssignClass (1972c19e-8c9a-4f45-ae07-0e653345bd75)
 Call ID: 1972c19e-8c9a-4f45-ae07-0e653345bd75
  Args:
    source: Infante_Felipe
    type: :Person
  AddTriple (923fba91-f4a1-4fb7-b1ee-6b6a541ff961)
 Call ID: 923fba91-f4a1-4fb7-b1ee-6b6a541ff961
  Args:
    source: Infante_Felipe
    target: Juan_Carlos_I
    relation: :hasFather
  AssignClass (c1b4bf55-b76e-4430-880a-4337102b2229)
 Call ID: c1b4bf55-b76e-4430-880a-4337102b2229
  Args:
    source: Infanta_Sofia
    type: :Woman
  AssignClass (ad991f5c-b82a-4235-b795-654338146822)
 Call ID: ad991f5c-b82a-4235-b795-654338146822
  Args:
    source: Infanta_Sofia
    type: :Person
  AddTriple (1d84f907-f8a8-44ee-a683-74568d727c46)
 Call ID: 1d84f907-f8a8-44ee-a683-74568d727c46
  Args:
    source: Infante_Felipe
    target: Infanta_Sofia
    relation: :hasMother
  AssignClass (2f8821bd-f5df-4fd5-b262-7e9ab9999625)
 Call ID: 2f8821bd-f5df-4fd5-b262-7e9ab9999625
  Args:
    source: Infante_Alfonso
    type: :Man
  AssignClass (34eb94db-cc32-4a51-9cd6-a1a38a471c5b)
 Call ID: 34eb94db-cc32-4a51-9cd6-a1a38a471c5b
  Args:
    source: Infante_Alfonso
    type: :Person
  AssignClass (ced3f843-5ec6-4fe1-a251-ff924be91cd8)
 Call ID: ced3f843-5ec6-4fe1-a251-ff924be91cd8
  Args:
    source: Infante_Jaime
    type: :Man
  AssignClass (5dd13f9c-d342-4a4b-8258-dd619a2ecb18)
 Call ID: 5dd13f9c-d342-4a4b-8258-dd619a2ecb18
  Args:
    source: Infante_Jaime
    type: :Person
  AssignClass (2a5cf7b5-ed54-405a-9b57-e87b91866172)
 Call ID: 2a5cf7b5-ed54-405a-9b57-e87b91866172
  Args:
    type: :Man
    source: Infante_Gonzalo
  AssignClass (8279ac11-235f-4d7e-96e7-e8744d4bc93e)
 Call ID: 8279ac11-235f-4d7e-96e7-e8744d4bc93e
  Args:
    type: :Person
    source: Infante_Gonzalo
  AssignClass (919d588c-e1d5-4b27-aba3-ee7b0b3029af)
 Call ID: 919d588c-e1d5-4b27-aba3-ee7b0b3029af
  Args:
    type: :Woman
    source: Infanta_Beatriz
  AssignClass (5112f536-4210-4a7b-8094-420b9ff8a06b)
 Call ID: 5112f536-4210-4a7b-8094-420b9ff8a06b
  Args:
    source: Infanta_Beatriz
    type: :Person
  AssignClass (68714af1-e08a-415d-8c2b-35e6d7446685)
 Call ID: 68714af1-e08a-415d-8c2b-35e6d7446685
  Args:
    type: :Woman
    source: Infanta_Maria_Cristina
  AssignClass (44b85876-e2a6-4abc-980d-ec3b4416860f)
 Call ID: 44b85876-e2a6-4abc-980d-ec3b4416860f
  Args:
    type: :Person
    source: Infanta_Maria_Cristina
  Finish (f88a7e16-b948-4b5d-8827-b35bb955d59b)
 Call ID: f88a7e16-b948-4b5d-8827-b35bb955d59b
  Args: