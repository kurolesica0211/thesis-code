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
Princess Elizabeth of Greece and Denmark (Greek: Ελισάβετ; 24 May 1904 – 11 January 1955) was a Greek and Danish princess who became Countess of Törring-Jettenbach upon marrying Bavarian count Carl Theodor of Törring-Jettenbach .
The second of three daughters of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia, Princess Elizabeth spent her childhood between the Kingdom of Greece and the Russian Empire.
However, the First World War and the divisions it brought to Greece forced the teenager and her family into exile in Switzerland between 1917 and 1920.
Returning to her country after the restoration of King Constantine I, she was banished once again by the proclamation of the Second Hellenic Republic in 1924.
Settled in Paris with her parents and sisters, the princess then undertook numerous trips that took her to visit her extended family in the United Kingdom, Italy, Yugoslavia, Romania, and Germany.
Penniless and single, the princess sold her image to an American cosmetics brand.
After unsuccessful attempts at courtships with the Prince of Wales, the Prince of Piedmont, Prince Nicholas of Romania, and Lord Ivor Spencer-Churchill, Elizabeth married Count Carl Theodor of Törring-Jettenbach, head of a high-profile Bavarian house, in 1934.
At the time of Elizabeth's arrival in Germany, Adolf Hitler had just established his dictatorship, and although the princess and her husband never joined the Nazi Party, they felt its full influence.
Used for their family ties to the Prince Regent of Yugoslavia and the Duke of Kent, husbands of Elizabeth's sisters, the Törrings were required to support the Führer's policies together with some other relatives, which led to tensions during the Second World War.
Isolated from her family after the Third Reich's invasion of Yugoslavia (1941), Elizabeth emerged weakened from the global conflict, but nevertheless regained her place within the European royalty.
Biography

Early childhood (1904–1909)

Childhood in Greece

Second daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia, Princess Elizabeth was born on 24 May 1904, at the Tatoi Palace.
Two years later, the family expanded again with the arrival of Princess Marina, who did not quite have the same closeness with her elder sisters.
During their early childhood, Elizabeth and her sisters received a relatively simple education, under the supervision of a British governess named Kate Fox.
In Greece, Elizabeth and her family resided at the Nicholas Palace, an Athenian wedding gift from the Tsar of Russia to his cousin.
During the reign of George I, the family also stayed regularly in Tatoi, where Elizabeth and her sisters were happy to meet up with their many Greek cousins.
After Constantine I's accession to the throne, however, the princess's parents acquired their own second home, in Kifissia.
With Kate Fox being a fan of outdoor activities, Elizabeth regularly visited the beaches of Vouliagmeni and Phalerum, where she enjoyed swimming and sunbathing.
Travel and family relationships

Prince Nicholas and his wife travelled to Russia once or twice a year, and Elizabeth and her sisters spent time in their mother's country from their early childhood.
For the girls, these trips to Russia were an opportunity to meet their numerous Romanov relatives: first the Vladimirovich branch (in other words, Grand Duke Vladimir Alexandrovich, Grand Duchess Maria Pavlovna, their three sons and their families), then the Konstantinovich branch (descended from Grand Duke Konstantin Nikolayevich, maternal grandfather of Prince Nicholas) and finally the main branch of the imperial family (and in particular the three younger children of Tsar Nicholas II, who were closer in age to the Greek princesses).
While Grand Duke Vladimir intimidated his granddaughters with his booming voice, Grand Duchess Maria Pavlovna proved to be a loving and generous grandmother, pampering the princesses while carefully monitoring their upbringing and manners.
The Grand Duchess, however, caused significant issues in the lives of Elizabeth and her sisters.
Despite this event, Elizabeth and her family retained all their affection for the governess, who returned to their service in 1921, a few months after the death of Maria Pavlovna.
Besides Russia, Princess Elizabeth explored, at a very young age, the United Kingdom, Germany, France, and Italy.
Political turbulence (1909–1920)

Rise of Venizelos and the Balkan Wars (1909–1913)

Elizabeth's early childhood was also marked by the series of upheavals that shook Greece from 1909.
That year, a military coup, known as the Goudi coup, forced the sons of King George I, including Prince Nicholas, to resign from the Army.
Under his leadership, Greece engaged in the Balkan Wars of 1912–1913, which allowed it to considerably expand its territory at the expense of the Ottoman Empire.
However, King George I was assassinated during the conflict, causing great grief to Elizabeth and her sisters.
With her sister Olga, Elizabeth also took riding lessons and soon became a skilled rider, which distinguished her from her elder sister.
Initially, these lessons were held in the gardens of the royal palace and the little girls learned to ride on ponies belonging to their cousins Prince Paul and Princess Irene.
However, the deterioration of the relations between Queen Sophia and Grand Duchess Elena then led the little girls to train far from the royal palace.
Despite the assassination of Archduke Franz Ferdinand in Sarajevo and the tensions it caused in the Balkans, Elizabeth and her family undertook their annual visit to Russia in July 1914.
Even within the royal family, the question of participation in the global conflict was causing tensions, especially since Elizabeth's mother suspected Queen Sophia of supporting the cause of her brother, Kaiser Wilhelm II.
In addition to these divisions, which led Elizabeth to see the daughters of King Constantine I less regularly, the war also brought its share of financial difficulties.
Prince Nicholas's income depended very largely on his wife's appanage, and his household was heavily affected by the economic crisis that was raging in the Russian Empire.
Long protected from fighting, the Hellenic capital was also hit by Allied fire in December 1916, forcing Elizabeth and her sisters to seek refuge in the cellars of the Nicholas Palace.
In February, a revolution overthrew the Tsarist regime, depriving Constantine I of the last of his supporters within the Entente.
Like many other Romanovs, Elizabeth's two grandmothers found themselves trapped in their palace, while several other relatives were arrested.
Finally, in June, the Entente forced Constantine I to abdicate in favor of his second son, Prince Alexander, and go into exile.
Initially spared by the events, Prince Nicholas and his family were soon forced to abandon Greece in turn, which they did on 4 July.
In Switzerland, Elizabeth and her family led an itinerant life which took them successively to St. Moritz, Zurich, Ouchy, Villeneuve and Montreux.
With Grand Duchess Elena's fortune having been confiscated by the Bolsheviks, the family was forced to dismiss some of its servants.
As a cost-saving measure, Elizabeth also had to share a room with her sisters for the first time in her life.
For a time, the princess and her sisters attended a school in Zurich, but their difficulties with German eventually forced their parents to resort to home education, supervised by a trilingual tutor named Miss Genand.
The situation of their Russian relatives was another source of concern for Elizabeth and her family.
While Prince Nicholas's family was relieved to find Queen Olga (in June–July 1918) safe and sound, and Grand Duchess Maria Pavlovna (in February 1920), the latter had been greatly weakened by deprivation, and she died only a few months after having managed to flee her country.
The only consolation for the small group: the Vladimirovich branch (to which Grand Duchess Elena belonged) was entirely spared by the civil war and communist repression.
Grand Duchess Maria Pavlovna also managed to save her jewels, which provided some support for Elizabeth's family.
Despite these concerns and the pettiness periodically suffered by the Greek exiles at the hands of the Entente and the Swiss authorities, exile was also a time of discovery for Elizabeth and her sisters.
With her elder, Elizabeth also played tennis, a sport for which both sisters were passionate.
Finally, the Swiss stay was also an opportunity for the teenagers to attend the wedding of their uncle Prince Christopher to a wealthy American woman named Nancy Stewart in January 1920.
Defeated in the November elections, he was forced to abandon the government to the monarchists, who then organized a referendum to restore Constantine I to the throne.
The ensuing royalist wave thus allowed members of the dynasty to return to Greece, which happened in December 1920.
A few weeks after these events, Kate Fox resumed her position in Prince Nicholas's household, much to the delight of Elizabeth and her sisters.
Within the royal family, the end of exile was also the occasion for other celebrations, which led Elizabeth to travel to France, Romania and Greece.
In February 1921, Crown Prince George married Princess Elisabeth of Romania in Bucharest.
The following month, Princess Helen married Prince Carol of Romania in Athens.
Finally, in November, the baptism of Prince Philip took place in Corfu.
In March 1922, another union seemed to be taking shape with the engagement of Princess Olga and Crown Prince Frederik of Denmark.
The engagement had barely been made public when it was cancelled by the heir to the Danish throne, who also made the mistake of disclosing his decision to Elizabeth before even speaking to Olga, placing the princess in a very uncomfortable position with her elder sister.
However, the prince had already committed another faux pas involving Elizabeth some time before: during the official presentation of the young couple to the Athenian crowd, Frederik took Elizabeth's hand instead of Olga's, thus humiliating his bride.
Added to this rupture was another misfortune, the consequences of which were far more serious for Elizabeth and her family.
With Greece's military situation in Asia Minor, which was deteriorating with Turkey, a coup d'état took place in the Hellenic kingdom, forcing Constantine I to abdicate in favor of the Diadochos on 27 September 1922.
In the following weeks, a purge hit the Greek state and Prince Andrew was arrested.
Narrowly saved by the intervention of foreign powers, he nevertheless had to go into exile, something to which Prince Nicholas also resolved.
Reduced to the status of a puppet king, George II himself was eventually forced to abandon Greece, and the republic was proclaimed on 25 March 1924, depriving Elizabeth and her relatives of their Greek nationality.
Itinerant life (1922–1933)

When King Constantine I abdicated, Elizabeth was in Paris with her mother and sisters.
Once reassured about the fate of her father, who was rumored to have been assassinated during the coup d'état, Elizabeth nevertheless left Paris with Kate Fox and Marina, for a vacation in Chamonix.
The reunion was short-lived, however, due to the death of the former king Constantine I on 11 January 1923 and the subsequent departure of the princess's parents to Palermo for the funeral.
Despite the events, Elizabeth and Olga went to Grasse for the wedding of their friend Marie-Laure Bischoffsheim with Viscount Charles de Noailles.
After that, Elizabeth went to Tyrol with Marina, where the two sisters had their adenoids removed.
As their exile dragged on, Prince Nicholas and his family established their residence in Paris.
Encouraged by her father, Elizabeth then took drawing and painting lessons with Marina.
Prince Nicholas having managed to rent his Athenian palace, the family's financial situation improved and the small group moved to the United Kingdom, where Olga and Elizabeth made their debut in high society in June 1923.
After being received by King George V and Queen Mary, the two sisters went from ball to ball, hoping to attract the attention of the Prince of Wales or one of his bachelor brothers, without any success.
During an evening at Lady Zia Wernher's, Princess Olga nevertheless met Prince Paul of Serbia, who soon asked for her hand in marriage.
Less fortunate than her elder sister, Elizabeth nevertheless had the satisfaction of going to Belgrade to attend the wedding on 22 October 1923.
In the years that followed, the princess led an itinerant life throughout Europe.
In September 1925, she travelled to Italy to attend the wedding of Princess Mafalda of Savoy to Prince Philip of Hesse-Kassel.
In addition to the future Edward VIII, attempts were made to match Elizabeth with Prince Umberto of Italy and Prince Nicholas of Romania.
Penniless but renowned for her beauty, the princess then sold her image to the American cosmetics brand Pond's, which has belonged to Unilever since 1987.
In the advertisements in which she appeared alongside her sister Marina, she was described as "as pretty as a fairy tale princess and possessing all the grace and dignity of her Greek heritage because she is charming, cheerful, versatile and very beautiful."


Engagement and marriage (1933–1934)
In March 1933, Princess Elizabeth finally met Count Carl Theodor of Törring-Jettenbach  during a trip to Munich with her sisters and brother-in-law Paul.
Nephew of Queen Elisabeth of the Belgians and first cousin of Prince Albrecht of Bavaria, he was at the head of a comfortable fortune and had an important collection of modern art.
Elizabeth and Carl Theodor quickly became friends and met several times, both in Bavaria and in Bohinj, Yugoslavia.
However, the count initially showed only limited interest in the princess, much to the dismay of her family.
On 21 September 1934, Carl Theodor nevertheless took advantage of a new stay in Bohinj to ask for Elizabeth's hand, which she accepted without hesitation.
With Prince Nicholas still experiencing financial difficulties, his son-in-law Paul bought back some of Grand Duchess Elena's jewels to help her raise the money needed to put together Elizabeth's trousseau.
The marriage of Elizabeth and Carl Theodor was finally celebrated on 10 January 1934 at Seefeld Castle, owned by the groom's brother.
The ceremony, which took place according to Catholic rites, brought together several figures from the European royalty and nobility, including King George II of Greece, Crown Prince Umberto of Italy, Crown Prince Rupprecht of Bavaria, Infanta Beatrice of Spain, and General von Epp, Reichsstatthalter of Bavaria.
Countess of Törring-Jettenbach (1934–1955)

Relationship with family

After their marriage, Elizabeth and Carl Theodor settled in Munich.
The princess gave birth to a boy there, born just over a year after his parents' union, on 11 January 1935, and named Hans Veit after his late paternal grandfather.
A loving and caring mother, Elizabeth communicated with her children in English, a language she also used with her husband.
Although she remained Orthodox until her death, the princess raised her offspring in the Catholic faith.
The arrival of the two children did not prevent Elizabeth and her husband from continuing to travel around Europe to meet their relatives.
Princess Marina married the Duke of Kent in November 1934, and the Törrings made several trips to Great Britain.
They also continued to frequently visit Princess Olga and Prince Paul in Yugoslavia.
In 1935, the monarchy was restored in Greece and Elizabeth's parents decided to return to live in Athens.
In 1937, Elizabeth returned to the country of her childhood on the occasion of the marriage of Crown Prince Paul to Princess Frederica of Hanover.
The death of Prince Nicholas in 1938 led his daughter to return to Greece for his funeral.
The princess subsequently made further visits there to help Grand Duchess Elena settle her affairs.
During these years, Elizabeth also regularly welcomed her relatives to Bavaria.
In 1938, Princess Olga's 35th birthday was celebrated at the Törrings' house at Winhöring Castle.
In her adopted country, Elizabeth was also in close contact with her cousins Margarita, Theodora, Cecilie, and Sophie, who had also married German princes.
In fact, Elizabeth and her husband never joined the Nazi Party, unlike several of the princess's cousins.
Furthermore, the communications of Elizabeth and Carl Theodor were closely monitored by the German authorities because of their connections with foreign powers.
Nevertheless, the often heated discussions between the Törrings, on the one hand, and the Kents, the Yugoslavians and Grand Duchess Elena, on the other, show that at the end of the 1930s, Carl Theodor and Elizabeth readily supported the policies pursued by the Führer.
As for Elizabeth, she actively helped her sister Olga organise the reception of Hermann Göring and his wife Emmy in Belgrade in 1935.
Later, at the beginning of the Second World War, the princess took refuge in Yugoslavia with her children for a while, but it was only to escape rationing and not for political reasons that she left Germany.
It was therefore not insignificant that Elizabeth and her husband were invited to Berlin by the German authorities at the time of the official visit of Paul, Prince Regent of Yugoslavia, in June 1939.
Similarly, the links between Count of Törring-Jettenbach and his brother-in-law the Duke of Kent were probably used by the Nazi regime to establish direct contact with the Windsors.
As Jonathan Petropoulos wrote, "there have been indications that Count Törring and Philipp  helped to sway Prince Paul to the German camp, but if so, they were merely pawns in a much larger equation."


Later years

Cut off from her family after the invasion of Yugoslavia by the forces of the Third Reich in April 1941, Elizabeth emerged physically weakened from the Second World War.
With the fall of the Third Reich and the Allied occupation of Germany, the princess was arrested and held overnight by the Americans.
In the years that followed, the Princess had the pleasure of reconnecting directly with her European relatives.
In May 1947, Elizabeth was granted permission to visit her sister Marina in the United Kingdom.
Then, in June, Elizabeth went to Athens with Marina to meet Olga and their mother.
However, the following November, Elizabeth was not invited to the wedding of her cousin Philip to Princess Elizabeth, the heir to the British throne.
In November 1949, Elizabeth met her brother-in-law, Prince Paul, for the first time.
In the years that followed, Elizabeth suffered from various health problems.
In December 1954, the princess was hospitalised again for an attack of arthritis and rheumatism.
After a private ceremony, the princess was buried in the Törring mausoleum, adjacent to the chapel of the family castle in Winhöring.
Honours

Marriage and issue

On 9 and 10 January 1934, Elisabeth married Carl Theodor, Count of Toerring-Jettenbach (1900–1967), son of Count Hans Veit zu Toerring-Jettenbach (1862–1929) and Duchess Sophie in Bavaria (1875–1957), at Munich and Seefeld Castle.
They had two children:


Ancestry

Notes and references

Notes

References

Bibliography

About Elizabeth

On Elizabeth's sisters and their husbands

On the royal family of Greece in general

Photographic albums dedicated to the royal family of Greece

Other works about royal families

External links

@media screen{html.skin-theme-clientpref-night .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}}@media screen and (prefers-color-scheme:dark){html.skin-theme-clientpref-os .mw-parser-output .sister-inline-image img{filter:invert(1)brightness(55%)contrast(250%)hue-rotate(180deg)}} Media related to Princess Elizabeth of Greece and Denmark at Wikimedia Commons



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
  AssignClass (e6495487-e41b-45b3-913f-64de9c9cb4b5)
 Call ID: e6495487-e41b-45b3-913f-64de9c9cb4b5
  Args:
    source: Princess_Elizabeth_of_Greece_and_Denmark
    type: :Woman
  AssignClass (601fad18-c181-4ed3-8a1d-76d0b9e5d613)
 Call ID: 601fad18-c181-4ed3-8a1d-76d0b9e5d613
  Args:
    type: :Person
    source: Princess_Elizabeth_of_Greece_and_Denmark
  AddLiteral (dcd18e9c-e5a2-42db-9a7d-753919c6f134)
 Call ID: dcd18e9c-e5a2-42db-9a7d-753919c6f134
  Args:
    literal_value: 1904
    source: Princess_Elizabeth_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0e43cc5f-e687-4ae9-b206-f398e8c27561)
 Call ID: 0e43cc5f-e687-4ae9-b206-f398e8c27561
  Args:
    source: Princess_Elizabeth_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1955
    relation: :hasDeathYear
  AssignClass (8bbf8155-8454-4a28-983d-bb39c6c24e75)
 Call ID: 8bbf8155-8454-4a28-983d-bb39c6c24e75
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (0c54b392-c398-4daf-a1ec-1ab6ab719d3f)
 Call ID: 0c54b392-c398-4daf-a1ec-1ab6ab719d3f
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (a1cf3037-4ce6-4c39-9a5a-fbe65e84fc2d)
 Call ID: a1cf3037-4ce6-4c39-9a5a-fbe65e84fc2d
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (e1825229-a3ea-48e5-8922-c019b11757f3)
 Call ID: e1825229-a3ea-48e5-8922-c019b11757f3
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddTriple (662d9365-5106-4283-a2d4-8e52e046b17a)
 Call ID: 662d9365-5106-4283-a2d4-8e52e046b17a
  Args:
    relation: :hasFather
    target: Prince_Nicholas_of_Greece_and_Denmark
    source: Princess_Elizabeth_of_Greece_and_Denmark
  AddTriple (cf001757-83ad-4571-a3be-0485e20158b9)
 Call ID: cf001757-83ad-4571-a3be-0485e20158b9
  Args:
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    source: Princess_Elizabeth_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (1ef5b4eb-ecdb-41be-87bc-ff733bf4fc10)
 Call ID: 1ef5b4eb-ecdb-41be-87bc-ff733bf4fc10
  Args:
    source: Carl_Theodor_of_Törring-Jettenbach
    type: :Man
  AssignClass (d29cfe6c-ed30-4568-9344-7e38ee3d7b38)
 Call ID: d29cfe6c-ed30-4568-9344-7e38ee3d7b38
  Args:
    source: Carl_Theodor_of_Törring-Jettenbach
    type: :Person
  AddTriple (84edb2d5-4620-4bca-b95f-cea35380b855)
 Call ID: 84edb2d5-4620-4bca-b95f-cea35380b855
  Args:
    relation: :hasRelation
    source: Princess_Elizabeth_of_Greece_and_Denmark
    target: Carl_Theodor_of_Törring-Jettenbach
  AddLiteral (c7f19c9f-54c2-40e4-9283-826e35248dfd)
 Call ID: c7f19c9f-54c2-40e4-9283-826e35248dfd
  Args:
    relation: :hasMarriageYear
    literal_value: 1934
    literal_type: xsd:integer
    source: Princess_Elizabeth_of_Greece_and_Denmark
  AssignClass (fa0ada91-aebb-4bb0-90ae-0e9be5456320)
 Call ID: fa0ada91-aebb-4bb0-90ae-0e9be5456320
  Args:
    source: Princess_Marina
    type: :Woman
  AssignClass (d2c2da96-9e51-448e-a5b7-6acd961b2851)
 Call ID: d2c2da96-9e51-448e-a5b7-6acd961b2851
  Args:
    type: :Person
    source: Princess_Marina
  AddTriple (c67f4c73-971a-4ba9-ab02-8847292fa413)
 Call ID: c67f4c73-971a-4ba9-ab02-8847292fa413
  Args:
    relation: :isSisterOf
    target: Princess_Elizabeth_of_Greece_and_Denmark
    source: Princess_Marina
  AssignClass (673275b7-f95b-45ee-9d7d-2a8d0bcbef4f)
 Call ID: 673275b7-f95b-45ee-9d7d-2a8d0bcbef4f
  Args:
    source: Princess_Olga
    type: :Woman
  AssignClass (1e87b28b-baec-4851-bf89-e0786e517226)
 Call ID: 1e87b28b-baec-4851-bf89-e0786e517226
  Args:
    type: :Person
    source: Princess_Olga
  AddTriple (78a59d53-6517-4a82-b0b1-ca37ed56d1af)
 Call ID: 78a59d53-6517-4a82-b0b1-ca37ed56d1af
  Args:
    source: Princess_Olga
    target: Princess_Elizabeth_of_Greece_and_Denmark
    relation: :isSisterOf
  AssignClass (f72bd5cf-c382-42d5-8eda-e95446b10d42)
 Call ID: f72bd5cf-c382-42d5-8eda-e95446b10d42
  Args:
    source: Hans_Veit_of_Törring-Jettenbach
    type: :Man
  AssignClass (a757e861-cdbb-43b1-bb40-9e91335086b3)
 Call ID: a757e861-cdbb-43b1-bb40-9e91335086b3
  Args:
    type: :Person
    source: Hans_Veit_of_Törring-Jettenbach
  AddTriple (2a543cf5-759f-4849-8010-bfdcaea32bbb)
 Call ID: 2a543cf5-759f-4849-8010-bfdcaea32bbb
  Args:
    target: Princess_Elizabeth_of_Greece_and_Denmark
    source: Hans_Veit_of_Törring-Jettenbach
    relation: :isSonOf
  AddTriple (d9a45894-4111-4ed8-8849-cba0a84dfad8)
 Call ID: d9a45894-4111-4ed8-8849-cba0a84dfad8
  Args:
    target: Carl_Theodor_of_Törring-Jettenbach
    source: Hans_Veit_of_Törring-Jettenbach
    relation: :isSonOf
  AssignClass (82fa31c7-5330-4044-9664-4284d7265761)
 Call ID: 82fa31c7-5330-4044-9664-4284d7265761
  Args:
    type: :Man
    source: Count_Hans_Veit_zu_Toerring-Jettenbach
  AssignClass (0e0946de-c9b6-4648-80bb-68fe51505411)
 Call ID: 0e0946de-c9b6-4648-80bb-68fe51505411
  Args:
    source: Count_Hans_Veit_zu_Toerring-Jettenbach
    type: :Person
  AssignClass (04e2f96b-6e59-4c6f-bf1c-cd2a4adc9b64)
 Call ID: 04e2f96b-6e59-4c6f-bf1c-cd2a4adc9b64
  Args:
    source: Duchess_Sophie_in_Bavaria
    type: :Woman
  AssignClass (ff1784d5-a628-4e7c-87d2-3e9b75c630e8)
 Call ID: ff1784d5-a628-4e7c-87d2-3e9b75c630e8
  Args:
    source: Duchess_Sophie_in_Bavaria
    type: :Person
  AddTriple (e0b6638b-eb63-4f7c-84c1-e7ef5927f81b)
 Call ID: e0b6638b-eb63-4f7c-84c1-e7ef5927f81b
  Args:
    relation: :hasFather
    target: Count_Hans_Veit_zu_Toerring-Jettenbach
    source: Carl_Theodor_of_Törring-Jettenbach
  AddTriple (f94df518-a06b-49a4-9f18-4a7a92662928)
 Call ID: f94df518-a06b-49a4-9f18-4a7a92662928
  Args:
    relation: :hasMother
    source: Carl_Theodor_of_Törring-Jettenbach
    target: Duchess_Sophie_in_Bavaria
  Finish (eac612fa-d78f-4794-a277-c5525394a125)
 Call ID: eac612fa-d78f-4794-a277-c5525394a125
  Args: