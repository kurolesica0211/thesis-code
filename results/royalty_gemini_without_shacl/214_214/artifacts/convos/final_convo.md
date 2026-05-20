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
Queen Victoria, the British monarch from 1837 to 1901, and Prince Albert (her husband from 1840 until his death in 1861) had 9 children, 42 grandchildren, and 87 great-grandchildren.
Their first grandchild was the future German Emperor Wilhelm II, who was born to their eldest child, Princess Victoria, on 27 January 1859; the youngest was Prince Maurice of Battenberg, born on 3 October 1891 to Princess Beatrice (1857–1944), who was herself the last child born to Victoria and Albert and the last child to die.
The last of Victoria and Albert's grandchildren to die (almost exactly 80 years after Queen Victoria herself) was Princess Alice, Countess of Athlone (25 February 1883 – 3 January 1981).
Just as Victoria and Albert shared one grandfather (Duke Francis of Saxe-Coburg-Saalfeld) and one grandmother (Countess Augusta Reuss), two pairs of their grandchildren married each other:


Prince Albert, the Prince Consort (26 August 1819 – 14 December 1861), lived long enough to see only one of his children married (Victoria, the Princess Royal) and two of his grandchildren born (Wilhelm II, 1859–1941, and his sister Princess Charlotte of Prussia, 1860–1919), while Queen Victoria (24 May 1819 – 22 January 1901) lived long enough to see not only all her grandchildren, but many of her 87 great-grandchildren as well.
(Three of Victoria's 56 great-grandsons were stillborn, another died shortly after birth, and one of her 31 great-granddaughters was born out of wedlock).
Victoria, the Princess Royal and first child of Victoria and Albert (21 November 1840 – 5 August 1901), known as "Vicky", was not only the mother to their first grandchild, Wilhelm II; she was also the first of Victoria and Albert's children to become a grandparent, with the birth in 1879 of Princess Feodora of Saxe-Meiningen, who was the daughter of Princess Charlotte (Queen Victoria's first granddaughter).
The Princess Royal was also the grandmother of the last of Victoria and Albert's great-granddaughters to die, Princess Katherine of Greece and Denmark (4 May 1913 – 2 October 2007), daughter of Vicky's fourth daughter, Queen Sophia of Greece.
After Katherine's death in 2007, the only surviving great-grandchild of Queen Victoria was Count Carl Johan Bernadotte of Wisborg (31 October 1916 – 5 May 2012), born to Crown Princess Margaret of Sweden, daughter of Victoria and Albert's third son, Prince Arthur, Duke of Connaught and Strathearn.
The death of Count Carl Johan Bernadotte marked the end of a generation of royalty that began in 1879 with the birth of Princess Feodora and included the British Kings Edward VIII and George VI, the Norwegian King Olav V, the Romanian King Carol II and the Greek Kings George II, Alexander and Paul—as well as six uncrowned victims of political assassination: Earl Mountbatten of Burma (last Viceroy of India), Tsarevich Alexei of Russia, and Alexei’s sisters, the Grand Duchesses Olga, Tatiana, Maria and Anastasia.
Queen Victoria's death in January 1901 was preceded by the deaths of three of her children (Princess Alice in December 1878, Prince Leopold in March 1884, and Prince Alfred in July 1900) and soon followed by the Princess Royal's death in August 1901.
Aside from the four boys who died as infants, Queen Victoria had survived seven of her grandchildren:


Victoria, Albert and their children

Ancestors of Victoria and Albert

Victoria and Albert had one pair of grandparents in common, Francis, Duke of Saxe-Coburg-Saalfeld, and Countess Augusta Reuss of Ebersdorf, who were parents both of Albert's father Ernest I, Duke of Saxe-Coburg and Gotha, and of Victoria's mother (and Ernest I's sister), Princess Victoria of Saxe-Coburg-Saalfeld.
Duke Francis & Countess Augusta → Duke Ernest I → Prince Albert
Duke Francis & Countess Augusta → Princess Victoria → Queen Victoria


Another of Victoria's (but not Albert's) grandfathers was King George III, father of Victoria's father, the Duke of Kent, and his brothers, King George IV and King William IV.
Marriage of Victoria and Albert

Queen Victoria (who had ascended to the throne on 20 June 1837 and been crowned on 28 June 1838) was married to Prince Albert on 10 February 1840 by William Howley, the Archbishop of Canterbury, in the Chapel Royal of St James's Palace in Westminster (London).
(Albert died nearly fifteen years before Victoria was proclaimed Empress of India on 1 May 1876.)


20 grandsons (of whom 2 were stillborn), 22 granddaughters including


Children of Victoria and Albert

Queen Victoria, at times, had contentious relations with her children.
According to one modern author, both Victoria and Albert weren't above playing favourites with their children, and unfortunately did little to hide their favouritism.
According to one modern author, Victoria was initially jealous of the time that Albert had spent with Vicky, but in her widowhood, Victoria made Vicky something of her confidante, and for her part, Vicky had accrued hundreds of letters from her mother, to the point that shortly before her death, she had them smuggled out of Germany by her brother's secretary, Sir Frederick Ponsonby.
Of her sons, Victoria had the most trouble with her eldest, Albert Edward, and her youngest, Leopold.
Among her daughters, Victoria clashed often with Louise.
In her widowhood, Victoria expected Beatrice, who was only 4 when her father died, to remain at home with her, and only permitted her to marry on the condition that she and her husband would remain in England.
Children and grandchildren of Victoria and Albert

Victoria, Princess Royal

The eldest child of Victoria and Albert was Princess Victoria, the Princess Royal, called "Vicky" (1840–1901).
On 25 January 1858, she married Prince Frederick Wilhelm of Prussia (1831–1888; Crown Prince from 1861, German Emperor March–June 1888).
Not only was the Princess Royal the first child of Queen Victoria and Prince Albert, she also gave them their first grandchild (the future Emperor Wilhelm II, 27 January 1859 – 4 June 1941) and was the grandmother to both the first of their 87 great-grandchildren to be born, Princess Feodora of Saxe-Meiningen (12 May 1879 – 26 August 1945), daughter of Princess Charlotte, and to the last of their 29 great-granddaughters to die, Princess Katherine of Greece and Denmark (4 May 1913 – 2 October 2007), daughter of Princess Sophie.
Queen Victoria → Princess Victoria → German Emperor Wilhelm II → Princess Victoria Louise of Prussia → Princess Frederica of Hanover (Queen of the Hellenes) → King Constantine II


Queen Victoria → Princess Victoria → Princess Sophie of Prussia → King Paul → King Constantine II


Queen Victoria → Princess Victoria → Princess Sophie of Prussia → Helen, Queen of Romania → King Michael I


Children of the Princess Royal and Crown Prince Frederick William of Prussia

The portrait below shows the Princess Royal with her husband Frederick William and with Victoria and Albert's first two grandchildren, the future Kaiser Wilhelm II (1859–1941) and Princess Charlotte (1860–1919), who were the only grandchildren born during Albert's lifetime.
Edward VII

Prince Albert Edward (1841–1910), then the Prince of Wales, married Princess Alexandra of Denmark (1844–1925), later Queen Alexandra of the United Kingdom, on 10 March 1863.
The Prince of Wales became King Edward VII and Emperor of India at the death of his mother Queen Victoria on 22 January 1901.
Edward and Alexandra's son, King George V, (reigned 1910–1936) was the father of Kings Edward VIII (reigned 1936) and George VI (1936–1952), and thereby the paternal grandfather of Queen Elizabeth II (reigned 1952–2022) and her sister Princess Margaret (1930–2002).
Elizabeth and Margaret were therefore great-granddaughters of Edward VII and great-great-granddaughters of Queen Victoria.
Queen Victoria → King Edward VII → King George V → King George VI → Queen Elizabeth II → King Charles III


Edward and Alexandra's daughter Princess Maud of Wales became Queen of Norway when her husband, Prince Carl of Denmark, became King Haakon VII (1905–1957) upon the dissolution of Norway's union with Sweden in 1905.
Their son, and Edward's grandson, became King Olav V (1957–1991); and Olav's children, King Harald V (since 1991), Princess Ragnhild and Princess Astrid, are thus great-grandchildren of Edward VII and great-great-grandchildren of Victoria and Albert.
Queen Victoria → King Edward VII → Princess Maud of Wales (Queen of Norway) → King Olav V → King Harald V


Children of King Edward VII and Queen Alexandra

Princess Alice

Princess Alice (1843–1878) married Prince Louis of Hesse (1837–1892), later Grand Duke Louis IV of Hesse, on 1 July 1862.
Prince Ludwig succeeded to the Grand Duchy of Hesse as Grand Duke Louis IV of Hesse, and Princess Alice as the Grand Duchess of Hesse, on 13 July 1877.
Alice and Louis's daughter, Princess Victoria of Hesse and by Rhine, married Prince Louis of Battenberg, and was the mother of Princess Alice of Battenberg (1885–1969), who became Alice, Princess Andrew of Greece and Denmark, when she married Prince Andrew of Greece and Denmark on 6 October 1903.
Princess Alice was the mother of Prince Philip, Duke of Edinburgh, the husband of Queen Elizabeth II.
Princess Victoria was also the mother of Queen Louise of Sweden.
Queen Victoria → Princess Alice → Princess Victoria of Hesse → Princess Alice of Battenberg → Prince Philip, Duke of Edinburgh


Alice and Louis's second daughter, Princess Elisabeth of Hesse and by Rhine, married, in 1884, the Russian Grand Duke Sergei Alexandrovich, the fifth son of Tsar Alexander II and Empress Maria Alexandrovna, and younger brother of the then reigning Tsar Alexander III.
Prince Ernest Louis became Ernest Louis, Grand Duke of Hesse, upon his father's death in March 1892.
He married his first cousin, Princess Victoria Melita of Saxe-Coburg and Gotha (1876-1936), in April 1894, and had one daughter, Princess Elisabeth of Hesse who died of typhoid fever, aged 8.
The Grand Duke married for a second time to Princess Eleonore of Solms-Hohensolms-Lich (1871–1937), and had two sons: Georg Donatus, Hereditary Grand Duke of Hesse who married Princess Cecilie of Greece and Denmark, sister of Prince Philip, Duke of Edinburgh, and had issue, and Prince Louis of Hesse and by Rhine.
Princess Alix of Hesse, the youngest surviving child of the Grand Ducal pair, became the last Empress of All the Russias through her marriage to Nicholas II of Russia in 1894.
Queen Victoria → Princess Alice → Princess Alix of Hesse (Tsarina Alexandra Feodorovna of Russia)


Children of Princess Alice and Louis IV of Hesse

¶
The entire family was killed in July 1918 in the aftermath of the Bolshevik Revolution, as was Alexandra's sister, the Grand Duchess Elisabeth (Princess Elisabeth of Hesse) the following day.
Alfred, Duke of Saxe-Coburg and Gotha

Prince Alfred (1844–1900) married the Grand Duchess Maria Alexandrovna of Russia (1853–1920), the only surviving daughter of Tsar Alexander II and Empress Marie Alexandrovna, on 23 January 1874 at the Winter Palace in St Petersburg, Russia.
In June 1893, Prince Alfred achieved the Royal Navy rank of Admiral of the Fleet, shortly before succeeding his paternal uncle, Ernest II, as Duke of Saxe-Coburg and Gotha in August 1893.
Prince Alfred's daughter (and Queen Victoria's granddaughter) Princess Marie of Edinburgh became Queen of Romania in 1914 after marrying the future King Ferdinand in 1893.
Queen Victoria → Prince Alfred → Princess Marie of Edinburgh (Queen of Romania) → King Carol II → King Michael I
Queen Victoria → Prince Alfred → Princess Marie of Edinburgh (Queen of Romania) → Princess Elisabeth of Romania (Queen of the Hellenes)
Queen Victoria → Prince Alfred → Princess Marie of Edinburgh (Queen of Romania) → Princess Marie of Romania (Queen of Yugoslavia) → King Peter II


Children of Alfred, Duke of Edinburgh, and Grand Duchess Marie

Princess Helena

Princess Helena (1846–1923) married Prince Christian of Schleswig-Holstein (1831–1917) in Windsor Castle's private chapel on 5 July 1866.
Princess Helena and Prince Christian had no legitimate grandchildren and one natural granddaughter who died without having issue of her own.
Like other British royal holders of German titles (such as Admiral Louis Battenberg), Princess Helena, Prince Christian, and their two daughters gave up their titles to Schleswig-Holstein in 1917 when the British and German Empires were at war.
Children of Princess Helena and Prince Christian of Schleswig-Holstein

Princess Louise

Princess Louise (1848–1939), who married John Campbell, 9th Duke of Argyll (1845–1914) in 1871, was the only one of Victoria's nine children who was childless.
She was the first British monarch's child since 1515 to marry a subject rather than someone of royal blood.
Prince Arthur, Duke of Connaught and Strathearn

Prince Arthur (1850–1942) married Princess Louise Margaret of Prussia (1860–1917) on 13 March 1879 at St George's Chapel in Windsor Castle.
He thus became the first, and so far only, Governor General of Canada to be of the Blood Royal, although he had been preceded in this office from 1878 to 1883 by the Marquess of Lorne, the non-royal husband of his sister Princess Louise (see above).
Prince Arthur's elder daughter (and Queen Victoria's granddaughter) Princess Margaret of Connaught became Crown Princess of Sweden in 1907 after marrying the future Gustaf VI Adolf of Sweden in 1905 (however, Margaret died before Gustav became king).
Queen Victoria → Prince Arthur → Princess Margaret of Connaught → Prince Gustaf Adolf, Duke of Västerbotten → King Carl XVI Gustaf
Queen Victoria → Prince Arthur → Princess Margaret of Connaught → Princess Ingrid of Sweden → Queen Margrethe II of Denmark → King Frederik X of Denmark
Queen Victoria → Prince Arthur → Princess Margaret of Connaught → Princess Ingrid of Sweden → Queen Anne Marie of Greece
Queen Victoria → Prince Arthur → Princess Margaret of Connaught → Count Carl Johan Bernadotte


Children of Arthur, Duke of Connaught, and Princess Louise Margaret of Prussia

Prince Leopold, Duke of Albany

Prince Leopold (1853–1884) married Princess Helen of Waldeck and Pyrmont (1861–1922) on 27 April 1882 at St George's Chapel, Windsor Castle.
He inherited the disease of haemophilia from his mother, Queen Victoria, and spent most of his life as a semi-invalid.
His daughter, Princess Alice of Albany, married Prince Alexander of Teck, the younger brother of Queen Mary, in February 1904 and became Countess of Athlone when her husband was created Earl of Athlone in June 1917.
She has, so far, been the longest-lived Princess of the Blood Royal of Britain and was the last surviving grandchild of Queen Victoria.
Prince Charles Edward, Prince Leopold's posthumous son, succeeded him at birth as the 2nd Duke of Albany.
In 1900, Charles Edward succeeded his paternal uncle, Alfred, as Duke of Saxe-Coburg and Gotha, but was forced to abdicate his ducal throne during the German Revolution of 1918, later gaining high positions in and through the Nazi movement.
Because of his support for Germany in World War I, he lost his English knighthood in the Order of the Garter in 1915 and his British royal titles, peerages and honours in 1919.
He is the grandfather of Carl XVI Gustaf of Sweden through his elder daughter, Princess Sibylla.
Queen Victoria → Prince Leopold → Prince Charles Edward → Princess Sibylla of Saxe-Coburg and Gotha → King Carl XVI Gustaf


Children of Leopold, Duke of Albany, and Princess Helena

Princess Beatrice

Princess Beatrice (1857–1944) married Prince Henry of Battenberg (1858–1896) on 23 July 1885 in St. Mildred's Church, Whippingham on the Isle of Wight.
They had 3 sons, 1 daughter (the future Queen Victoria Eugenia of Spain), 5 grandsons (1 stillborn) and 3 granddaughters.
The present King Felipe VI of Spain, as the great-grandson of Victoria Eugenie, is the great-great-grandson of Princess Beatrice and thus the great-great-great-grandson of Queen Victoria.
Queen Victoria → Princess Beatrice → Princess Victoria Eugenie of Battenberg (Queen of Spain) → Infante Juan, Count of Barcelona → King Juan Carlos I → King Felipe VI


Due to anti-German feeling during the First World War, the members of the Battenberg family who were British citizens relinquished their titles of Prince and Princess of Battenberg and the styles of Highness and Serene Highness.
Under Royal Warrant, they instead took the surname Mountbatten, an Anglicised form of Battenberg.
Both Prince Henry and his youngest son Prince Maurice (the lastborn of Victoria's grandchildren) died on active military service, the father from malaria contracted during the Ashanti War and the son in battle on the Western Front of World War I.


Children of Princess Beatrice and Prince Henry of Battenberg

See also

References

Sources and external links



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
  AssignClass (65636dd4-dcb4-403d-bd33-cd909463489a)
 Call ID: 65636dd4-dcb4-403d-bd33-cd909463489a
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (f3e7e4b9-6926-4324-a6cf-9a16ecaf78d4)
 Call ID: f3e7e4b9-6926-4324-a6cf-9a16ecaf78d4
  Args:
    type: :Man
    source: Prince_Albert
  AddLiteral (a59a0b11-2770-4a6c-a2b4-b21958f864b8)
 Call ID: a59a0b11-2770-4a6c-a2b4-b21958f864b8
  Args:
    source: Queen_Victoria
    literal_value: 1819
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (de72055e-1554-4dfe-856c-3ad4f33ed38c)
 Call ID: de72055e-1554-4dfe-856c-3ad4f33ed38c
  Args:
    literal_value: 1901
    source: Queen_Victoria
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (00495914-db6e-41d6-9b63-c8da2439c2cb)
 Call ID: 00495914-db6e-41d6-9b63-c8da2439c2cb
  Args:
    relation: :hasBirthYear
    source: Prince_Albert
    literal_value: 1819
    literal_type: xsd:integer
  AddLiteral (e09820f9-24dd-4964-bf5c-cfc27d024fc0)
 Call ID: e09820f9-24dd-4964-bf5c-cfc27d024fc0
  Args:
    relation: :hasDeathYear
    literal_value: 1861
    source: Prince_Albert
    literal_type: xsd:integer
  AddLiteral (0195efdb-9e03-4605-8329-5f9ef3ab5771)
 Call ID: 0195efdb-9e03-4605-8329-5f9ef3ab5771
  Args:
    source: Queen_Victoria
    literal_value: 1840
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (c5397b7d-8ace-428d-8f2a-d9463487323e)
 Call ID: c5397b7d-8ace-428d-8f2a-d9463487323e
  Args:
    target: Prince_Albert
    source: Queen_Victoria
    relation: :hasRelation
  AssignClass (2ebee6b6-1de8-4b12-8a94-e579c2b4dd31)
 Call ID: 2ebee6b6-1de8-4b12-8a94-e579c2b4dd31
  Args:
    type: :Woman
    source: Princess_Victoria_Princess_Royal
  AddTriple (e885f3fb-3088-40f1-91a9-3201cc325b99)
 Call ID: e885f3fb-3088-40f1-91a9-3201cc325b99
  Args:
    source: Princess_Victoria_Princess_Royal
    relation: :isDaughterOf
    target: Queen_Victoria
  AddTriple (1934e10e-2ee6-44e9-b70f-bc22ffe5998e)
 Call ID: 1934e10e-2ee6-44e9-b70f-bc22ffe5998e
  Args:
    target: Prince_Albert
    relation: :isDaughterOf
    source: Princess_Victoria_Princess_Royal
  AddLiteral (df331111-e7c1-4ecf-a32b-88e506837d7a)
 Call ID: df331111-e7c1-4ecf-a32b-88e506837d7a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1840
    source: Princess_Victoria_Princess_Royal
  AddLiteral (6fc18164-94cc-4a25-85ea-7f76075a9127)
 Call ID: 6fc18164-94cc-4a25-85ea-7f76075a9127
  Args:
    literal_value: 1901
    source: Princess_Victoria_Princess_Royal
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (b0853124-1fcd-4298-8069-ec1730a0f74d)
 Call ID: b0853124-1fcd-4298-8069-ec1730a0f74d
  Args:
    source: Princess_Victoria_Princess_Royal
    literal_value: Vicky
    literal_type: xsd:string
    relation: :knownAs
  AssignClass (db550949-6352-4c47-95ff-2d68f619aa3d)
 Call ID: db550949-6352-4c47-95ff-2d68f619aa3d
  Args:
    type: :Man
    source: Prince_Frederick_Wilhelm_of_Prussia
  AddTriple (e5f67214-1ace-41dd-b4f1-b842e4d7fc09)
 Call ID: e5f67214-1ace-41dd-b4f1-b842e4d7fc09
  Args:
    target: Prince_Frederick_Wilhelm_of_Prussia
    source: Princess_Victoria_Princess_Royal
    relation: :hasRelation
  AssignClass (f9a25f68-7a24-45e3-a3e8-254efe3b95ee)
 Call ID: f9a25f68-7a24-45e3-a3e8-254efe3b95ee
  Args:
    type: :Man
    source: Wilhelm_II
  AddTriple (5484f729-54a1-4f54-99e4-3be6c43a1eaa)
 Call ID: 5484f729-54a1-4f54-99e4-3be6c43a1eaa
  Args:
    target: Princess_Victoria_Princess_Royal
    source: Wilhelm_II
    relation: :isSonOf
  AddTriple (bcfd2948-6d06-47b5-baad-45f0f2749ccb)
 Call ID: bcfd2948-6d06-47b5-baad-45f0f2749ccb
  Args:
    source: Wilhelm_II
    relation: :isSonOf
    target: Prince_Frederick_Wilhelm_of_Prussia
  AddLiteral (1bc67285-3187-4742-9b30-090b9301765e)
 Call ID: 1bc67285-3187-4742-9b30-090b9301765e
  Args:
    relation: :hasBirthYear
    literal_value: 1859
    source: Wilhelm_II
    literal_type: xsd:integer
  AddLiteral (246f845f-6e8b-4705-9a8c-10b3d2769079)
 Call ID: 246f845f-6e8b-4705-9a8c-10b3d2769079
  Args:
    literal_type: xsd:integer
    literal_value: 1941
    source: Wilhelm_II
    relation: :hasDeathYear
  AssignClass (238516a4-f219-47a7-8e76-8ea452dfae6b)
 Call ID: 238516a4-f219-47a7-8e76-8ea452dfae6b
  Args:
    type: :Woman
    source: Princess_Charlotte_of_Prussia
  AddTriple (680700ff-f418-4037-895c-e3c6d0aefd41)
 Call ID: 680700ff-f418-4037-895c-e3c6d0aefd41
  Args:
    target: Princess_Victoria_Princess_Royal
    relation: :isDaughterOf
    source: Princess_Charlotte_of_Prussia
  AddTriple (a41b536c-85bd-4eb1-a192-ce73c075bd0f)
 Call ID: a41b536c-85bd-4eb1-a192-ce73c075bd0f
  Args:
    relation: :isDaughterOf
    source: Princess_Charlotte_of_Prussia
    target: Prince_Frederick_Wilhelm_of_Prussia
  AddLiteral (370d8610-3f28-4cba-ba2b-baee83c504ea)
 Call ID: 370d8610-3f28-4cba-ba2b-baee83c504ea
  Args:
    source: Princess_Charlotte_of_Prussia
    literal_value: 1860
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2c739bda-1723-421f-a04b-da06ec3c0139)
 Call ID: 2c739bda-1723-421f-a04b-da06ec3c0139
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Princess_Charlotte_of_Prussia
    literal_value: 1919
  Finish (0a0e8f2b-0270-4d39-a3cf-74b9e7bcbfa5)
 Call ID: 0a0e8f2b-0270-4d39-a3cf-74b9e7bcbfa5
  Args: