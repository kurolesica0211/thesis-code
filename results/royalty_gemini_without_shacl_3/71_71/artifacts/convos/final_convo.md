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
  AssignClass (9fbe2dc0-3b6a-49c1-bb95-3189adcfab4a)
 Call ID: 9fbe2dc0-3b6a-49c1-bb95-3189adcfab4a
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (e12a63c5-e59c-4806-bdad-d226c63184e1)
 Call ID: e12a63c5-e59c-4806-bdad-d226c63184e1
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AddLiteral (e6ae0b32-8f26-427c-88bb-b169acfc07d7)
 Call ID: e6ae0b32-8f26-427c-88bb-b169acfc07d7
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Victoria_Eugenie_of_Battenberg
    literal_value: 1887
  AddLiteral (0af085c2-cfd4-4713-8423-173aabd03c71)
 Call ID: 0af085c2-cfd4-4713-8423-173aabd03c71
  Args:
    literal_type: xsd:integer
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasDeathYear
    literal_value: 1969
  AddLiteral (a7908c7a-fb4f-4fab-88c3-5416bdbcb7a1)
 Call ID: a7908c7a-fb4f-4fab-88c3-5416bdbcb7a1
  Args:
    literal_value: Ena
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (0ae60db3-7428-4de7-9e83-25e6004a003b)
 Call ID: 0ae60db3-7428-4de7-9e83-25e6004a003b
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (7c9cd0c9-bb83-47c4-8fe0-e0ad20060d71)
 Call ID: 7c9cd0c9-bb83-47c4-8fe0-e0ad20060d71
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddLiteral (a618effc-89ff-42e2-8356-adb76e5641d3)
 Call ID: a618effc-89ff-42e2-8356-adb76e5641d3
  Args:
    literal_type: xsd:integer
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasMarriageYear
    literal_value: 1906
  AddTriple (61232287-409a-4a4b-aa45-4e85020267ff)
 Call ID: 61232287-409a-4a4b-aa45-4e85020267ff
  Args:
    relation: :hasRelation
    source: Victoria_Eugenie_of_Battenberg
    target: Alfonso_XIII_of_Spain
  AssignClass (433d4088-345e-48f2-a511-8866d240c4d2)
 Call ID: 433d4088-345e-48f2-a511-8866d240c4d2
  Args:
    type: :Man
    source: Prince_Henry_of_Battenberg
  AssignClass (f234e0ec-c803-4979-ab13-c237d0bc3564)
 Call ID: f234e0ec-c803-4979-ab13-c237d0bc3564
  Args:
    type: :Person
    source: Prince_Henry_of_Battenberg
  AssignClass (74fc604d-74c6-446d-b4b4-0f07ff525ff2)
 Call ID: 74fc604d-74c6-446d-b4b4-0f07ff525ff2
  Args:
    type: :Woman
    source: Princess_Beatrice
  AssignClass (671337af-ada6-4da5-bc1d-7cf2a090ea1b)
 Call ID: 671337af-ada6-4da5-bc1d-7cf2a090ea1b
  Args:
    type: :Person
    source: Princess_Beatrice
  AddTriple (43c9bf9b-4e7e-4fc0-a24a-8eba96427159)
 Call ID: 43c9bf9b-4e7e-4fc0-a24a-8eba96427159
  Args:
    relation: :hasFather
    source: Victoria_Eugenie_of_Battenberg
    target: Prince_Henry_of_Battenberg
  AddTriple (141b4313-8d0d-4638-9042-38a18bf5cefa)
 Call ID: 141b4313-8d0d-4638-9042-38a18bf5cefa
  Args:
    relation: :hasMother
    source: Victoria_Eugenie_of_Battenberg
    target: Princess_Beatrice
  AssignClass (c8268c38-8054-4391-a510-7ca9a4280978)
 Call ID: c8268c38-8054-4391-a510-7ca9a4280978
  Args:
    type: :Man
    source: Prince_Alexander_of_Hesse
  AssignClass (f8091b63-4443-4b79-be71-c2b7fd182934)
 Call ID: f8091b63-4443-4b79-be71-c2b7fd182934
  Args:
    type: :Person
    source: Prince_Alexander_of_Hesse
  AssignClass (b53914fd-ef41-40b5-8327-3e8240a853ac)
 Call ID: b53914fd-ef41-40b5-8327-3e8240a853ac
  Args:
    type: :Woman
    source: Julia_Princess_of_Battenberg
  AssignClass (1b6d3d82-1ed8-46d9-bf98-5d1abbf7ad90)
 Call ID: 1b6d3d82-1ed8-46d9-bf98-5d1abbf7ad90
  Args:
    type: :Person
    source: Julia_Princess_of_Battenberg
  AddTriple (df0f4a77-c3f4-45e2-8c6a-0c5d87900e43)
 Call ID: df0f4a77-c3f4-45e2-8c6a-0c5d87900e43
  Args:
    source: Prince_Henry_of_Battenberg
    relation: :hasFather
    target: Prince_Alexander_of_Hesse
  AddTriple (f228bd66-7bdc-4504-ac33-408b6ea7cc79)
 Call ID: f228bd66-7bdc-4504-ac33-408b6ea7cc79
  Args:
    target: Julia_Princess_of_Battenberg
    source: Prince_Henry_of_Battenberg
    relation: :hasMother
  AssignClass (00e64c00-3ae1-4545-b6d9-3c7ea592dd3c)
 Call ID: 00e64c00-3ae1-4545-b6d9-3c7ea592dd3c
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (f0541583-1c16-4d18-9980-4d7a63500ecf)
 Call ID: f0541583-1c16-4d18-9980-4d7a63500ecf
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (0849c5e6-4ff1-4d04-bc47-925086095a46)
 Call ID: 0849c5e6-4ff1-4d04-bc47-925086095a46
  Args:
    type: :Man
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
  AssignClass (c07f2f60-de21-4d45-9194-094ed2f08ea0)
 Call ID: c07f2f60-de21-4d45-9194-094ed2f08ea0
  Args:
    type: :Person
    source: Prince_Albert_of_Saxe-Coburg_and_Gotha
  AddTriple (cabdff69-9b68-4ee8-9d0e-848702cce665)
 Call ID: cabdff69-9b68-4ee8-9d0e-848702cce665
  Args:
    target: Queen_Victoria
    relation: :hasMother
    source: Princess_Beatrice
  AddTriple (b410ef8f-82dc-4a5e-b070-813bdf29e5b8)
 Call ID: b410ef8f-82dc-4a5e-b070-813bdf29e5b8
  Args:
    target: Prince_Albert_of_Saxe-Coburg_and_Gotha
    source: Princess_Beatrice
    relation: :hasFather
  AssignClass (d6583503-1737-4061-822f-7566f355f9b7)
 Call ID: d6583503-1737-4061-822f-7566f355f9b7
  Args:
    type: :Man
    source: Leopold_of_Battenberg
  AssignClass (5a993fb2-b089-4b85-89da-46bd440e686b)
 Call ID: 5a993fb2-b089-4b85-89da-46bd440e686b
  Args:
    type: :Person
    source: Leopold_of_Battenberg
  AddTriple (b73fb67b-b4e9-4f1a-ae6c-d764eea9b304)
 Call ID: b73fb67b-b4e9-4f1a-ae6c-d764eea9b304
  Args:
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasBrother
    target: Leopold_of_Battenberg
  AssignClass (d4e68de4-839d-4d40-9466-50c8941411d0)
 Call ID: d4e68de4-839d-4d40-9466-50c8941411d0
  Args:
    type: :Man
    source: Alfonso_Prince_of_Asturias
  AssignClass (e63f419a-ab8d-4e4a-918c-ca27e546e59d)
 Call ID: e63f419a-ab8d-4e4a-918c-ca27e546e59d
  Args:
    type: :Person
    source: Alfonso_Prince_of_Asturias
  AddTriple (aab40059-e3df-493c-914c-81bec6429457)
 Call ID: aab40059-e3df-493c-914c-81bec6429457
  Args:
    target: Alfonso_Prince_of_Asturias
    relation: :hasSon
    source: Victoria_Eugenie_of_Battenberg
  AddTriple (f57d02bb-a501-4bc9-a18c-196ddc06c365)
 Call ID: f57d02bb-a501-4bc9-a18c-196ddc06c365
  Args:
    target: Alfonso_Prince_of_Asturias
    relation: :hasSon
    source: Alfonso_XIII_of_Spain
  AssignClass (2b4cab8d-e887-480e-ab70-11b7c61c0ea7)
 Call ID: 2b4cab8d-e887-480e-ab70-11b7c61c0ea7
  Args:
    type: :Man
    source: Juan_Count_of_Barcelona
  AssignClass (d487023b-731f-490b-b1ac-db1470f5c068)
 Call ID: d487023b-731f-490b-b1ac-db1470f5c068
  Args:
    type: :Person
    source: Juan_Count_of_Barcelona
  AddTriple (551ce592-d3ea-490a-84e7-b129beb7f79a)
 Call ID: 551ce592-d3ea-490a-84e7-b129beb7f79a
  Args:
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasSon
    target: Juan_Count_of_Barcelona
  AddTriple (f9d6e05a-5d5b-4e04-b3c7-5429961e3f80)
 Call ID: f9d6e05a-5d5b-4e04-b3c7-5429961e3f80
  Args:
    target: Juan_Count_of_Barcelona
    relation: :hasSon
    source: Alfonso_XIII_of_Spain
  AssignClass (479de6a2-74dc-4542-92a7-bb0c34237e99)
 Call ID: 479de6a2-74dc-4542-92a7-bb0c34237e99
  Args:
    type: :Woman
    source: Infanta_Beatriz
  AssignClass (eae48aed-a695-4ab5-8183-d39ab3e4c4e6)
 Call ID: eae48aed-a695-4ab5-8183-d39ab3e4c4e6
  Args:
    type: :Person
    source: Infanta_Beatriz
  AddTriple (f878ba5e-c1e1-47cd-9a84-8a1e6f971677)
 Call ID: f878ba5e-c1e1-47cd-9a84-8a1e6f971677
  Args:
    target: Infanta_Beatriz
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasDaughter
  AssignClass (e91f752b-bb33-45e8-a37d-905948d9ae20)
 Call ID: e91f752b-bb33-45e8-a37d-905948d9ae20
  Args:
    type: :Woman
    source: Infanta_Maria_Cristina
  AssignClass (41657d74-e55c-450c-a631-45a9ad6244a5)
 Call ID: 41657d74-e55c-450c-a631-45a9ad6244a5
  Args:
    type: :Person
    source: Infanta_Maria_Cristina
  AddTriple (38d40115-4c65-421f-95c4-0d747ce74032)
 Call ID: 38d40115-4c65-421f-95c4-0d747ce74032
  Args:
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasDaughter
    target: Infanta_Maria_Cristina
  AssignClass (4f499412-3e18-48b8-8f4d-ffeb39471204)
 Call ID: 4f499412-3e18-48b8-8f4d-ffeb39471204
  Args:
    type: :Man
    source: Infante_Jaime
  AssignClass (45123156-7573-4f11-9551-1849fde8e464)
 Call ID: 45123156-7573-4f11-9551-1849fde8e464
  Args:
    type: :Person
    source: Infante_Jaime
  AddTriple (a62702cc-f446-4aef-b55c-4c52c5887017)
 Call ID: a62702cc-f446-4aef-b55c-4c52c5887017
  Args:
    target: Infante_Jaime
    source: Victoria_Eugenie_of_Battenberg
    relation: :hasSon
  AssignClass (f66d511d-f864-4d47-9146-2dd9796cf431)
 Call ID: f66d511d-f864-4d47-9146-2dd9796cf431
  Args:
    type: :Man
    source: Infante_Gonzalo
  AssignClass (af697bc3-e412-45d6-bb71-b67290c3a350)
 Call ID: af697bc3-e412-45d6-bb71-b67290c3a350
  Args:
    type: :Person
    source: Infante_Gonzalo
  AddTriple (80e73ac7-466f-4f55-8e5a-8d034ab9aba3)
 Call ID: 80e73ac7-466f-4f55-8e5a-8d034ab9aba3
  Args:
    target: Infante_Gonzalo
    relation: :hasSon
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (ea24d5a9-1f77-4a91-ad1a-aa78b675800a)
 Call ID: ea24d5a9-1f77-4a91-ad1a-aa78b675800a
  Args:
    type: :Man
    source: Infante_Alfonso
  AssignClass (f11cd0c0-4cf9-441c-a010-7797eacb618e)
 Call ID: f11cd0c0-4cf9-441c-a010-7797eacb618e
  Args:
    type: :Person
    source: Infante_Alfonso
  AddTriple (e5464904-e981-463f-8d22-4626d4427563)
 Call ID: e5464904-e981-463f-8d22-4626d4427563
  Args:
    target: Infante_Alfonso
    relation: :hasSon
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (dcd4f12e-611b-4659-ac83-1a5f53a7d20a)
 Call ID: dcd4f12e-611b-4659-ac83-1a5f53a7d20a
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (bdfa4906-3d67-4326-ab5c-5ece01d2768d)
 Call ID: bdfa4906-3d67-4326-ab5c-5ece01d2768d
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (f75e7b6a-9da2-4161-a1a3-dcb92e4c175b)
 Call ID: f75e7b6a-9da2-4161-a1a3-dcb92e4c175b
  Args:
    target: Juan_Carlos_I
    relation: :hasSon
    source: Juan_Count_of_Barcelona
  AssignClass (1ce182ec-9734-472a-8ce1-8c8b0de1e05d)
 Call ID: 1ce182ec-9734-472a-8ce1-8c8b0de1e05d
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (09d4cd5f-138f-45d7-9ee8-6020a72d70e9)
 Call ID: 09d4cd5f-138f-45d7-9ee8-6020a72d70e9
  Args:
    type: :Person
    source: Felipe_VI
  AddTriple (563a99f7-2f6f-4282-92cb-3efcc5052d1d)
 Call ID: 563a99f7-2f6f-4282-92cb-3efcc5052d1d
  Args:
    relation: :hasSon
    source: Juan_Carlos_I
    target: Felipe_VI
  Finish (cf76e5f9-a1b4-462e-b501-1e7edb0ecc12)
 Call ID: cf76e5f9-a1b4-462e-b501-1e7edb0ecc12
  Args: