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
  AssignClass (228c61d8-6887-4f31-8943-ca4e555a56a1)
 Call ID: 228c61d8-6887-4f31-8943-ca4e555a56a1
  Args:
    source: :VictoriaEugenieOfBattenberg
    type: :Woman
  AssignClass (2881bc46-dcf4-4c3b-955d-958efc17ce38)
 Call ID: 2881bc46-dcf4-4c3b-955d-958efc17ce38
  Args:
    source: :VictoriaEugenieOfBattenberg
    type: :Person
  AddLiteral (af39456b-9cb6-4ec6-ba8c-ac93b40ea2d2)
 Call ID: af39456b-9cb6-4ec6-ba8c-ac93b40ea2d2
  Args:
    source: :VictoriaEugenieOfBattenberg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1887
  AddLiteral (1605a306-6aaf-406e-a332-8fc32e6aadb2)
 Call ID: 1605a306-6aaf-406e-a332-8fc32e6aadb2
  Args:
    source: :VictoriaEugenieOfBattenberg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1969
  AddLiteral (c98643f3-fabd-426a-b4ff-13eb31c5dc73)
 Call ID: c98643f3-fabd-426a-b4ff-13eb31c5dc73
  Args:
    relation: :alsoKnownAs
    literal_value: Ena
    literal_type: xsd:string
    source: :VictoriaEugenieOfBattenberg
  AssignClass (b778c3ec-4784-4db2-80dc-9c0479963bad)
 Call ID: b778c3ec-4784-4db2-80dc-9c0479963bad
  Args:
    type: :Man
    source: :AlfonsoXIII
  AssignClass (5aaae861-a600-4f67-acd0-336e5c87cc76)
 Call ID: 5aaae861-a600-4f67-acd0-336e5c87cc76
  Args:
    source: :AlfonsoXIII
    type: :Person
  AddLiteral (27d33917-47f6-4616-862e-1e6a30d0090f)
 Call ID: 27d33917-47f6-4616-862e-1e6a30d0090f
  Args:
    source: :VictoriaEugenieOfBattenberg
    relation: :hasMarriageYear
    literal_value: 1906
    literal_type: xsd:integer
  AddTriple (8e5531fc-d2a3-4231-8529-17f922ed0725)
 Call ID: 8e5531fc-d2a3-4231-8529-17f922ed0725
  Args:
    source: :VictoriaEugenieOfBattenberg
    target: :AlfonsoXIII
    relation: :hasRelation
  AssignClass (a4e07480-11db-43a2-8759-e3ca111e5319)
 Call ID: a4e07480-11db-43a2-8759-e3ca111e5319
  Args:
    type: :Man
    source: :PrinceHenryOfBattenberg
  AssignClass (3638ad4e-6861-417b-bdbc-f88e42a171ea)
 Call ID: 3638ad4e-6861-417b-bdbc-f88e42a171ea
  Args:
    source: :PrinceHenryOfBattenberg
    type: :Person
  AssignClass (42ead7d0-6c17-4119-a99d-c96052a66186)
 Call ID: 42ead7d0-6c17-4119-a99d-c96052a66186
  Args:
    source: :PrincessBeatrice
    type: :Woman
  AssignClass (0bc4dd71-cd0f-4062-bb86-e06b91bb4fb3)
 Call ID: 0bc4dd71-cd0f-4062-bb86-e06b91bb4fb3
  Args:
    type: :Person
    source: :PrincessBeatrice
  AddTriple (dc9f2163-54ae-4d12-a58b-c3985b97a854)
 Call ID: dc9f2163-54ae-4d12-a58b-c3985b97a854
  Args:
    source: :VictoriaEugenieOfBattenberg
    target: :PrinceHenryOfBattenberg
    relation: :hasFather
  AddTriple (69ff2e77-64af-4ad5-9b61-efedf567e7c2)
 Call ID: 69ff2e77-64af-4ad5-9b61-efedf567e7c2
  Args:
    source: :VictoriaEugenieOfBattenberg
    target: :PrincessBeatrice
    relation: :hasMother
  AssignClass (295895a9-11cb-4b16-9493-11e48372f5be)
 Call ID: 295895a9-11cb-4b16-9493-11e48372f5be
  Args:
    type: :Man
    source: :PrinceAlexanderOfHesse
  AssignClass (16330449-d652-44f1-86fd-b6bea785d7d5)
 Call ID: 16330449-d652-44f1-86fd-b6bea785d7d5
  Args:
    source: :PrinceAlexanderOfHesse
    type: :Person
  AssignClass (ece6d46b-60d0-4000-b927-1ae932ab264c)
 Call ID: ece6d46b-60d0-4000-b927-1ae932ab264c
  Args:
    type: :Woman
    source: :JuliaPrincessOfBattenberg
  AssignClass (9f6e0418-0fcf-4d1b-aab0-b591b9052b82)
 Call ID: 9f6e0418-0fcf-4d1b-aab0-b591b9052b82
  Args:
    source: :JuliaPrincessOfBattenberg
    type: :Person
  AddTriple (38d0c568-8b49-4109-8e50-3c6104af909b)
 Call ID: 38d0c568-8b49-4109-8e50-3c6104af909b
  Args:
    target: :PrinceAlexanderOfHesse
    relation: :hasFather
    source: :PrinceHenryOfBattenberg
  AddTriple (63472d8e-5bd9-4884-ba60-c353e4aa3aa9)
 Call ID: 63472d8e-5bd9-4884-ba60-c353e4aa3aa9
  Args:
    target: :JuliaPrincessOfBattenberg
    relation: :hasMother
    source: :PrinceHenryOfBattenberg
  AssignClass (ebc4ed78-3f95-4883-a635-14b0aa347315)
 Call ID: ebc4ed78-3f95-4883-a635-14b0aa347315
  Args:
    source: :QueenVictoria
    type: :Woman
  AssignClass (3f06a79d-fd47-4d48-98b1-1c574d7917e9)
 Call ID: 3f06a79d-fd47-4d48-98b1-1c574d7917e9
  Args:
    source: :QueenVictoria
    type: :Person
  AssignClass (a285c3dc-b8da-40eb-a3a0-de273bb436a6)
 Call ID: a285c3dc-b8da-40eb-a3a0-de273bb436a6
  Args:
    type: :Man
    source: :PrinceAlbertOfSaxeCoburgAndGotha
  AssignClass (46a01d2d-43c9-483d-9c21-8d1f67b0dcf0)
 Call ID: 46a01d2d-43c9-483d-9c21-8d1f67b0dcf0
  Args:
    type: :Person
    source: :PrinceAlbertOfSaxeCoburgAndGotha
  AddTriple (6c3a642c-2aa9-43a8-bd1f-505848342eb9)
 Call ID: 6c3a642c-2aa9-43a8-bd1f-505848342eb9
  Args:
    relation: :hasFather
    target: :PrinceAlbertOfSaxeCoburgAndGotha
    source: :PrincessBeatrice
  AddTriple (361aa06e-a491-463b-9a83-522651ec06ce)
 Call ID: 361aa06e-a491-463b-9a83-522651ec06ce
  Args:
    relation: :hasMother
    target: :QueenVictoria
    source: :PrincessBeatrice
  AssignClass (5eebee4b-11b1-4a84-b7ea-b184b8ac6e14)
 Call ID: 5eebee4b-11b1-4a84-b7ea-b184b8ac6e14
  Args:
    type: :Man
    source: :Leopold
  AssignClass (e50b159f-083a-4505-92e1-d5528c419822)
 Call ID: e50b159f-083a-4505-92e1-d5528c419822
  Args:
    type: :Person
    source: :Leopold
  AddTriple (7413f0f1-c83b-4ca9-8d30-30b88face715)
 Call ID: 7413f0f1-c83b-4ca9-8d30-30b88face715
  Args:
    source: :VictoriaEugenieOfBattenberg
    relation: :hasBrother
    target: :Leopold
  AssignClass (4b0cf75b-55dd-441c-aeb3-f2e0afe143b3)
 Call ID: 4b0cf75b-55dd-441c-aeb3-f2e0afe143b3
  Args:
    type: :Man
    source: :AlfonsoPrinceOfAsturias
  AssignClass (f9476e4c-362f-4cd0-a406-0eaa218dda9d)
 Call ID: f9476e4c-362f-4cd0-a406-0eaa218dda9d
  Args:
    type: :Person
    source: :AlfonsoPrinceOfAsturias
  AddTriple (ddffb25c-19a5-41eb-b1cb-ee68064d275b)
 Call ID: ddffb25c-19a5-41eb-b1cb-ee68064d275b
  Args:
    target: :AlfonsoPrinceOfAsturias
    relation: :hasSon
    source: :VictoriaEugenieOfBattenberg
  AddTriple (b02ec94e-62d4-47cc-8c04-5582db6a5d9a)
 Call ID: b02ec94e-62d4-47cc-8c04-5582db6a5d9a
  Args:
    source: :AlfonsoPrinceOfAsturias
    target: :AlfonsoXIII
    relation: :hasFather
  AssignClass (6f5802b5-cd20-44e2-951b-d7f6f87c1a9b)
 Call ID: 6f5802b5-cd20-44e2-951b-d7f6f87c1a9b
  Args:
    type: :Man
    source: :Juan
  AssignClass (ce7afe51-120e-404f-87ed-aca789c252b9)
 Call ID: ce7afe51-120e-404f-87ed-aca789c252b9
  Args:
    type: :Person
    source: :Juan
  AddTriple (68fa63a1-077e-4c64-be5b-92fe7a9f0c14)
 Call ID: 68fa63a1-077e-4c64-be5b-92fe7a9f0c14
  Args:
    target: :Juan
    relation: :hasSon
    source: :VictoriaEugenieOfBattenberg
  AddTriple (50c54262-c5f7-44d8-9815-ea32f33ae411)
 Call ID: 50c54262-c5f7-44d8-9815-ea32f33ae411
  Args:
    source: :Juan
    target: :AlfonsoXIII
    relation: :hasFather
  AssignClass (b4302cdc-3609-4969-a4f0-e78364db59c9)
 Call ID: b4302cdc-3609-4969-a4f0-e78364db59c9
  Args:
    source: :InfantaBeatriz
    type: :Woman
  AssignClass (c8ad7006-1a75-423b-a0a6-a33f4b75dd5e)
 Call ID: c8ad7006-1a75-423b-a0a6-a33f4b75dd5e
  Args:
    source: :InfantaBeatriz
    type: :Person
  AssignClass (9ead8d6e-2cae-4901-9eac-e6bda5652929)
 Call ID: 9ead8d6e-2cae-4901-9eac-e6bda5652929
  Args:
    type: :Woman
    source: :InfantaMariaCristina
  AssignClass (41228e88-22b5-499c-8a57-117fdfdbda8c)
 Call ID: 41228e88-22b5-499c-8a57-117fdfdbda8c
  Args:
    type: :Person
    source: :InfantaMariaCristina
  AddTriple (61b21ca3-8b25-4be2-a0d4-b47f1b677aa1)
 Call ID: 61b21ca3-8b25-4be2-a0d4-b47f1b677aa1
  Args:
    relation: :hasDaughter
    target: :InfantaBeatriz
    source: :VictoriaEugenieOfBattenberg
  AddTriple (dbeed51e-1033-4aa0-a835-a6f8f3c0e01d)
 Call ID: dbeed51e-1033-4aa0-a835-a6f8f3c0e01d
  Args:
    target: :InfantaMariaCristina
    relation: :hasDaughter
    source: :VictoriaEugenieOfBattenberg
  AssignClass (5b2e88ab-7648-4c84-8e3c-a97a9d0dbe5a)
 Call ID: 5b2e88ab-7648-4c84-8e3c-a97a9d0dbe5a
  Args:
    source: :InfanteAlfonso
    type: :Man
  AssignClass (738e38fc-8d40-4aa4-b150-f2dcd81af0db)
 Call ID: 738e38fc-8d40-4aa4-b150-f2dcd81af0db
  Args:
    type: :Person
    source: :InfanteAlfonso
  AssignClass (982d5143-7f2a-499d-9459-9f500b911682)
 Call ID: 982d5143-7f2a-499d-9459-9f500b911682
  Args:
    source: :InfanteJaime
    type: :Man
  AssignClass (2dc12cd6-010a-480d-ac7f-55991e3833f1)
 Call ID: 2dc12cd6-010a-480d-ac7f-55991e3833f1
  Args:
    type: :Person
    source: :InfanteJaime
  AssignClass (4a621f83-2155-4070-b493-d9e663bac380)
 Call ID: 4a621f83-2155-4070-b493-d9e663bac380
  Args:
    type: :Man
    source: :InfanteGonzalo
  AssignClass (11cac7d8-e248-4590-b720-358d3da17caf)
 Call ID: 11cac7d8-e248-4590-b720-358d3da17caf
  Args:
    source: :InfanteGonzalo
    type: :Person
  AddTriple (d8e31d65-fa4b-4eda-84cd-325c3e5667e0)
 Call ID: d8e31d65-fa4b-4eda-84cd-325c3e5667e0
  Args:
    target: :InfanteAlfonso
    relation: :hasSon
    source: :VictoriaEugenieOfBattenberg
  AddTriple (3a58473f-79ff-430f-ae13-d5988fa80ac9)
 Call ID: 3a58473f-79ff-430f-ae13-d5988fa80ac9
  Args:
    source: :VictoriaEugenieOfBattenberg
    relation: :hasSon
    target: :InfanteJaime
  AddTriple (a361b40b-54f3-4cf2-9b45-6f1ce9ae7c2a)
 Call ID: a361b40b-54f3-4cf2-9b45-6f1ce9ae7c2a
  Args:
    relation: :hasSon
    target: :InfanteGonzalo
    source: :VictoriaEugenieOfBattenberg
  Finish (e9a2a465-a9f1-49b0-ade2-64cb3989e733)
 Call ID: e9a2a465-a9f1-49b0-ade2-64cb3989e733
  Args: