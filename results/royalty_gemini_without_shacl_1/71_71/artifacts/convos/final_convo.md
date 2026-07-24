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
  AssignClass (218fdc60-7463-4ce8-8948-81cb0bc89928)
 Call ID: 218fdc60-7463-4ce8-8948-81cb0bc89928
  Args:
    type: :Woman
    source: :VictoriaEugenieOfBattenberg
  AssignClass (de912869-5df4-461d-8ab3-20e958f845cd)
 Call ID: de912869-5df4-461d-8ab3-20e958f845cd
  Args:
    type: :Person
    source: :VictoriaEugenieOfBattenberg
  AddLiteral (4a6ebae5-e444-45e1-931d-b9b081ab4866)
 Call ID: 4a6ebae5-e444-45e1-931d-b9b081ab4866
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1887
    source: :VictoriaEugenieOfBattenberg
  AddLiteral (f199be4d-8c58-41ec-9fc0-a16d8849caf7)
 Call ID: f199be4d-8c58-41ec-9fc0-a16d8849caf7
  Args:
    literal_type: xsd:integer
    literal_value: 1969
    source: :VictoriaEugenieOfBattenberg
    relation: :hasDeathYear
  AddLiteral (b41d3126-6213-4f35-a032-1d5ccd03c198)
 Call ID: b41d3126-6213-4f35-a032-1d5ccd03c198
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Ena
    source: :VictoriaEugenieOfBattenberg
  AssignClass (c7d023b2-9514-40fe-9980-60bbd0c2a54e)
 Call ID: c7d023b2-9514-40fe-9980-60bbd0c2a54e
  Args:
    source: :AlfonsoXIII
    type: :Man
  AssignClass (d39b31c7-f310-4370-8855-c127528a856d)
 Call ID: d39b31c7-f310-4370-8855-c127528a856d
  Args:
    type: :Person
    source: :AlfonsoXIII
  AddLiteral (583c4ff4-87d8-4080-8163-2736017e63e7)
 Call ID: 583c4ff4-87d8-4080-8163-2736017e63e7
  Args:
    relation: :hasMarriageYear
    literal_value: 1906
    literal_type: xsd:integer
    source: :VictoriaEugenieOfBattenberg
  AddTriple (21d06a3a-7870-4761-8370-112c3e235cd1)
 Call ID: 21d06a3a-7870-4761-8370-112c3e235cd1
  Args:
    relation: :hasRelation
    target: :AlfonsoXIII
    source: :VictoriaEugenieOfBattenberg
  AssignClass (f7d2d0f1-6d48-4c09-8901-5fba9062f75e)
 Call ID: f7d2d0f1-6d48-4c09-8901-5fba9062f75e
  Args:
    type: :Man
    source: :PrinceHenryOfBattenberg
  AssignClass (be4faeb4-e190-4328-a5d4-472c2a70f627)
 Call ID: be4faeb4-e190-4328-a5d4-472c2a70f627
  Args:
    source: :PrinceHenryOfBattenberg
    type: :Person
  AssignClass (d65ba59a-6449-4f1f-a17a-54b271a1d890)
 Call ID: d65ba59a-6449-4f1f-a17a-54b271a1d890
  Args:
    type: :Ancestor
    source: :PrinceHenryOfBattenberg
  AssignClass (4da4262c-1f2c-422f-8a7f-14f9c189af66)
 Call ID: 4da4262c-1f2c-422f-8a7f-14f9c189af66
  Args:
    type: :Woman
    source: :PrincessBeatrice
  AssignClass (87883729-0023-4ef7-a4d8-66840093fb4d)
 Call ID: 87883729-0023-4ef7-a4d8-66840093fb4d
  Args:
    type: :Person
    source: :PrincessBeatrice
  AssignClass (14be0171-388a-49c3-ba92-91222ca0f041)
 Call ID: 14be0171-388a-49c3-ba92-91222ca0f041
  Args:
    type: :Ancestor
    source: :PrincessBeatrice
  AddTriple (2240767e-7fa8-4c99-b6f4-80f9e95e99c1)
 Call ID: 2240767e-7fa8-4c99-b6f4-80f9e95e99c1
  Args:
    source: :VictoriaEugenieOfBattenberg
    target: :PrinceHenryOfBattenberg
    relation: :hasFather
  AddTriple (2ed1fe7a-c42a-4902-8254-c25947b1f90b)
 Call ID: 2ed1fe7a-c42a-4902-8254-c25947b1f90b
  Args:
    source: :VictoriaEugenieOfBattenberg
    target: :PrincessBeatrice
    relation: :hasMother
  AssignClass (873b72fa-0432-43d2-91f9-5ac9183fe33e)
 Call ID: 873b72fa-0432-43d2-91f9-5ac9183fe33e
  Args:
    type: :Man
    source: :PrinceAlexanderOfHesseAndByRhine
  AssignClass (093d044d-2473-4cf3-b7de-ada7b3ddff94)
 Call ID: 093d044d-2473-4cf3-b7de-ada7b3ddff94
  Args:
    type: :Person
    source: :PrinceAlexanderOfHesseAndByRhine
  AssignClass (82452ac8-9379-4091-bf7f-ebe2c7b33fc8)
 Call ID: 82452ac8-9379-4091-bf7f-ebe2c7b33fc8
  Args:
    source: :PrinceAlexanderOfHesseAndByRhine
    type: :Ancestor
  AssignClass (da95943d-f17d-4a41-bec3-7166aebcb536)
 Call ID: da95943d-f17d-4a41-bec3-7166aebcb536
  Args:
    type: :Woman
    source: :JuliaPrincessOfBattenberg
  AssignClass (d087b3f4-7253-4ba9-bddd-d089fb611e3e)
 Call ID: d087b3f4-7253-4ba9-bddd-d089fb611e3e
  Args:
    source: :JuliaPrincessOfBattenberg
    type: :Person
  AssignClass (244229cf-7516-4bcf-8cf6-346e3a02e15e)
 Call ID: 244229cf-7516-4bcf-8cf6-346e3a02e15e
  Args:
    source: :JuliaPrincessOfBattenberg
    type: :Ancestor
  AddTriple (6e277e03-7914-4ec5-9405-ee60c39813b2)
 Call ID: 6e277e03-7914-4ec5-9405-ee60c39813b2
  Args:
    relation: :hasFather
    target: :PrinceAlexanderOfHesseAndByRhine
    source: :PrinceHenryOfBattenberg
  AddTriple (fc603cce-4202-4a77-bc4d-c96459201663)
 Call ID: fc603cce-4202-4a77-bc4d-c96459201663
  Args:
    target: :JuliaPrincessOfBattenberg
    relation: :hasMother
    source: :PrinceHenryOfBattenberg
  AssignClass (afffb4f1-b1be-4c52-b5df-d0ee15bf07c2)
 Call ID: afffb4f1-b1be-4c52-b5df-d0ee15bf07c2
  Args:
    type: :Woman
    source: :QueenVictoria
  AssignClass (53fc882e-7fb7-4589-88dc-5ca0c101ac6c)
 Call ID: 53fc882e-7fb7-4589-88dc-5ca0c101ac6c
  Args:
    source: :QueenVictoria
    type: :Person
  AssignClass (1e172560-ead5-4691-8a31-70b8429b16e5)
 Call ID: 1e172560-ead5-4691-8a31-70b8429b16e5
  Args:
    type: :Ancestor
    source: :QueenVictoria
  AssignClass (33fdd6c7-f7a1-4319-83e1-7daa1c56796b)
 Call ID: 33fdd6c7-f7a1-4319-83e1-7daa1c56796b
  Args:
    source: :PrinceAlbertOfSaxeCoburgAndGotha
    type: :Man
  AssignClass (b4c5730d-b61c-4887-ac79-3e7de167d8db)
 Call ID: b4c5730d-b61c-4887-ac79-3e7de167d8db
  Args:
    type: :Person
    source: :PrinceAlbertOfSaxeCoburgAndGotha
  AssignClass (5957c8bf-74d8-4cd9-948f-a8f8d87ca380)
 Call ID: 5957c8bf-74d8-4cd9-948f-a8f8d87ca380
  Args:
    type: :Ancestor
    source: :PrinceAlbertOfSaxeCoburgAndGotha
  AddTriple (15210875-72b0-46a8-a206-3662e41ffe2a)
 Call ID: 15210875-72b0-46a8-a206-3662e41ffe2a
  Args:
    source: :PrincessBeatrice
    target: :PrinceAlbertOfSaxeCoburgAndGotha
    relation: :hasFather
  AddTriple (1f643909-0f53-4eca-a5d7-946b5282e242)
 Call ID: 1f643909-0f53-4eca-a5d7-946b5282e242
  Args:
    relation: :hasMother
    target: :QueenVictoria
    source: :PrincessBeatrice
  AssignClass (01018000-a1a6-4893-9834-24b3be888a5a)
 Call ID: 01018000-a1a6-4893-9834-24b3be888a5a
  Args:
    source: :Leopold
    type: :Man
  AssignClass (5087a8c9-9b49-420d-b8ec-ea561cbc9c9a)
 Call ID: 5087a8c9-9b49-420d-b8ec-ea561cbc9c9a
  Args:
    type: :Person
    source: :Leopold
  AddTriple (c1a11c0a-ffc7-4e51-8f96-47effe0fc13d)
 Call ID: c1a11c0a-ffc7-4e51-8f96-47effe0fc13d
  Args:
    relation: :hasSister
    target: :VictoriaEugenieOfBattenberg
    source: :Leopold
  AddTriple (28cf6aff-4a5c-4f8f-95aa-86b17e642dde)
 Call ID: 28cf6aff-4a5c-4f8f-95aa-86b17e642dde
  Args:
    source: :Leopold
    target: :PrincessBeatrice
    relation: :hasMother
  AddTriple (03516c32-cae2-4b5e-afe3-7a93fd721df4)
 Call ID: 03516c32-cae2-4b5e-afe3-7a93fd721df4
  Args:
    source: :Leopold
    relation: :hasFather
    target: :PrinceHenryOfBattenberg
  AssignClass (44945fb6-7d3e-4995-a26c-11f920d18347)
 Call ID: 44945fb6-7d3e-4995-a26c-11f920d18347
  Args:
    type: :Man
    source: :AlfonsoPrinceOfAsturias
  AssignClass (a8119774-ea59-42c3-a6e9-1eac8ea7fe61)
 Call ID: a8119774-ea59-42c3-a6e9-1eac8ea7fe61
  Args:
    source: :AlfonsoPrinceOfAsturias
    type: :Person
  AddTriple (7788a0ef-9aad-483e-af76-48b72769abf8)
 Call ID: 7788a0ef-9aad-483e-af76-48b72769abf8
  Args:
    source: :AlfonsoPrinceOfAsturias
    relation: :hasMother
    target: :VictoriaEugenieOfBattenberg
  AddTriple (015f1834-7ed2-4fb4-afb1-72223ec656e7)
 Call ID: 015f1834-7ed2-4fb4-afb1-72223ec656e7
  Args:
    source: :AlfonsoPrinceOfAsturias
    target: :AlfonsoXIII
    relation: :hasFather
  AssignClass (5397c15c-6ebc-4e1e-8431-f3f6a6c09e5d)
 Call ID: 5397c15c-6ebc-4e1e-8431-f3f6a6c09e5d
  Args:
    type: :Man
    source: :JuanCountOfBarcelona
  AssignClass (7cb72385-9819-4a74-b7d0-f621dfbf8d52)
 Call ID: 7cb72385-9819-4a74-b7d0-f621dfbf8d52
  Args:
    source: :JuanCountOfBarcelona
    type: :Person
  AddTriple (e5a1aaae-7225-486a-8483-9f2e2753a2d4)
 Call ID: e5a1aaae-7225-486a-8483-9f2e2753a2d4
  Args:
    relation: :hasMother
    target: :VictoriaEugenieOfBattenberg
    source: :JuanCountOfBarcelona
  AddTriple (d270e939-872f-4eb8-b4c7-8f1a7145f5d5)
 Call ID: d270e939-872f-4eb8-b4c7-8f1a7145f5d5
  Args:
    source: :JuanCountOfBarcelona
    relation: :hasFather
    target: :AlfonsoXIII
  AssignClass (1af1b6a9-3858-4fb9-8ee7-1102a5ab09c5)
 Call ID: 1af1b6a9-3858-4fb9-8ee7-1102a5ab09c5
  Args:
    source: :JuanCarlosI
    type: :Man
  AssignClass (861c3bf0-fcfe-4d55-b045-b48e1cb4f2c2)
 Call ID: 861c3bf0-fcfe-4d55-b045-b48e1cb4f2c2
  Args:
    source: :JuanCarlosI
    type: :Person
  AddTriple (e009172d-1494-4a76-a87d-b9094c909171)
 Call ID: e009172d-1494-4a76-a87d-b9094c909171
  Args:
    source: :JuanCarlosI
    relation: :hasFather
    target: :JuanCountOfBarcelona
  AssignClass (45ee72cf-4326-4d80-ad7e-a0d59147a922)
 Call ID: 45ee72cf-4326-4d80-ad7e-a0d59147a922
  Args:
    type: :Man
    source: :FelipeVI
  AssignClass (0390aacc-8933-435d-bca2-de2cd8852bea)
 Call ID: 0390aacc-8933-435d-bca2-de2cd8852bea
  Args:
    type: :Person
    source: :FelipeVI
  AddTriple (0145ef19-5205-495a-bc02-2c5a64f1c89f)
 Call ID: 0145ef19-5205-495a-bc02-2c5a64f1c89f
  Args:
    source: :FelipeVI
    relation: :hasFather
    target: :JuanCarlosI
  AssignClass (e47cc676-fdc9-4bae-9d57-51347c8e4c90)
 Call ID: e47cc676-fdc9-4bae-9d57-51347c8e4c90
  Args:
    source: :InfantaBeatriz
    type: :Woman
  AssignClass (4004eb21-5b6e-48ee-964a-c6b3737585ca)
 Call ID: 4004eb21-5b6e-48ee-964a-c6b3737585ca
  Args:
    type: :Person
    source: :InfantaBeatriz
  AddTriple (fa58c042-2e8f-4e6a-8401-dd1a41fda267)
 Call ID: fa58c042-2e8f-4e6a-8401-dd1a41fda267
  Args:
    source: :InfantaBeatriz
    relation: :hasMother
    target: :VictoriaEugenieOfBattenberg
  AddTriple (7c8038bd-5d2d-4951-a399-9fc9a849a434)
 Call ID: 7c8038bd-5d2d-4951-a399-9fc9a849a434
  Args:
    source: :InfantaBeatriz
    target: :AlfonsoXIII
    relation: :hasFather
  AssignClass (393d60fd-fc6f-4d3a-a563-8e25d01afcd3)
 Call ID: 393d60fd-fc6f-4d3a-a563-8e25d01afcd3
  Args:
    type: :Woman
    source: :InfantaMariaCristina
  AssignClass (b0c05728-7d6a-411d-a486-5720b364c9ce)
 Call ID: b0c05728-7d6a-411d-a486-5720b364c9ce
  Args:
    type: :Person
    source: :InfantaMariaCristina
  AddTriple (8ffeecd4-33a9-44c9-9d1b-7416d8855127)
 Call ID: 8ffeecd4-33a9-44c9-9d1b-7416d8855127
  Args:
    target: :VictoriaEugenieOfBattenberg
    relation: :hasMother
    source: :InfantaMariaCristina
  AddTriple (08c52865-0ca7-4512-830e-b3286a3d589b)
 Call ID: 08c52865-0ca7-4512-830e-b3286a3d589b
  Args:
    target: :AlfonsoXIII
    relation: :hasFather
    source: :InfantaMariaCristina
  AssignClass (295af686-f2b8-4bc0-af05-566da3688af0)
 Call ID: 295af686-f2b8-4bc0-af05-566da3688af0
  Args:
    type: :Man
    source: :InfanteJaime
  AssignClass (e265bbde-125f-428f-9a72-76883eb2f54f)
 Call ID: e265bbde-125f-428f-9a72-76883eb2f54f
  Args:
    source: :InfanteJaime
    type: :Person
  AddTriple (7b6b4803-dd7d-4035-be3d-bdc193af71f5)
 Call ID: 7b6b4803-dd7d-4035-be3d-bdc193af71f5
  Args:
    target: :VictoriaEugenieOfBattenberg
    relation: :hasMother
    source: :InfanteJaime
  AddTriple (246e63e3-8ac8-4452-b13e-aacd484923af)
 Call ID: 246e63e3-8ac8-4452-b13e-aacd484923af
  Args:
    relation: :hasFather
    target: :AlfonsoXIII
    source: :InfanteJaime
  AssignClass (454b3fc3-c65f-4fde-99ab-db155dbc2ed7)
 Call ID: 454b3fc3-c65f-4fde-99ab-db155dbc2ed7
  Args:
    source: :InfanteGonzalo
    type: :Man
  AssignClass (51a809a2-f831-4912-88d0-b25ddbc410b8)
 Call ID: 51a809a2-f831-4912-88d0-b25ddbc410b8
  Args:
    source: :InfanteGonzalo
    type: :Person
  AddTriple (64c6a574-e518-4a1f-80e6-619adff30401)
 Call ID: 64c6a574-e518-4a1f-80e6-619adff30401
  Args:
    source: :InfanteGonzalo
    relation: :hasMother
    target: :VictoriaEugenieOfBattenberg
  AddTriple (013b7ae7-3d46-40b0-b0a4-23f03d7995e4)
 Call ID: 013b7ae7-3d46-40b0-b0a4-23f03d7995e4
  Args:
    relation: :hasFather
    target: :AlfonsoXIII
    source: :InfanteGonzalo
  AssignClass (b3a81a19-aafe-4cea-9de5-9ba2eb31018b)
 Call ID: b3a81a19-aafe-4cea-9de5-9ba2eb31018b
  Args:
    source: :QueenMariaChristina
    type: :Woman
  AssignClass (00402595-7901-42e1-8bf3-97bdab6b5384)
 Call ID: 00402595-7901-42e1-8bf3-97bdab6b5384
  Args:
    type: :Person
    source: :QueenMariaChristina
  AddTriple (64b805f7-0009-480b-a31f-d648d21725c0)
 Call ID: 64b805f7-0009-480b-a31f-d648d21725c0
  Args:
    target: :QueenMariaChristina
    relation: :hasMother
    source: :AlfonsoXIII
  AssignClass (752d3126-4cf1-4976-9ab1-b4a079876f3f)
 Call ID: 752d3126-4cf1-4976-9ab1-b4a079876f3f
  Args:
    type: :Man
    source: :KingEdwardVII
  AssignClass (903084ea-273f-407a-aff7-a8897debb80f)
 Call ID: 903084ea-273f-407a-aff7-a8897debb80f
  Args:
    source: :KingEdwardVII
    type: :Person
  AddTriple (f49aacf9-4084-4b7a-8373-ea21412e3b59)
 Call ID: f49aacf9-4084-4b7a-8373-ea21412e3b59
  Args:
    target: :PrincessBeatrice
    relation: :isBloodrelationOf
    source: :KingEdwardVII
  Finish (2e70a91d-f684-4390-beca-f50d0322ea04)
 Call ID: 2e70a91d-f684-4390-beca-f50d0322ea04
  Args: