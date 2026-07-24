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
Princess Maria of Greece and Denmark (Greek: Μαρία; romanized: María)
(Russian: Мария Георгиевна; 3 March  1876 – 14 December 1940) was a daughter of King George I of Greece and his wife  Grand Duchess  Olga Constantinovna of Russia.
She was a sister of King Constantine I of Greece and a first cousin of Tsar Nicholas II of Russia and King George V of the United Kingdom.
Born as a princess of Greece and Denmark, she was educated in Athens by private tutors.
Her father instilled in her a great love for Greece and throughout her life, she remained a fervent patriot.
She married Grand Duke George Mikhailovich of Russia, her first cousin once removed, who courted her for five years.
Grand Duke George Mikhailovich had a house built for her in Crimea and he was a devoted father and husband, but the marriage was unhappy.
Princess Maria, known upon her marriage as Grand Duchess Maria Georgievna of Russia, neither got to love her husband nor her adopted country.
Longing for her native Greece, she never adapted to life in Russia.
At the outbreak of World War I, she was vacationing in England with her daughters and chose not to return to Russia.
Her husband was trapped in Russia after the revolution and he was shot by the Bolsheviks with several other Romanov relatives in January 1919.
In her widowhood, deprived of her Russian income, Princess Maria faced serious financial difficulties.
She returned to live in Greece with her daughters in 1920.
The princess returned to live in Britain for a couple of years and she settled in Rome in 1926 with her second husband.
She lived in Italy for over a decade until the outbreak of the Greco-Italian War in 1940 forced her to return to her native Greece.
She was in poor health and was cared for by her nephew King Paul of Greece and his wife Frederica.
Early life

Princess Maria of Greece and Denmark was born on 3 March  1876  at the Royal Palace in Athens.
She was the fifth child and second daughter of King George I of Greece and Grand Duchess Olga Constantinovna of Russia.
Maria's father was born a Danish prince.
Princess Maria, nicknamed "Greek Minnie" to tell her apart from the elder "Minnie", her paternal aunt (Empress Maria Feodorovna of Russia), grew up as part of a large family of eight children.
One sister, named Olga, died in childhood, but  she had five brothers:  (Constantine, George, Nicholas, Andrew, Christopher) and one surviving sister: Alexandra.
King George and Queen Olga were devoted parents who provided a happy, homely environment for their children.
King George was a strict and demanding father, but contrary to the general approach of the time, he believed in happy rambunctious children.
Maria and her siblings were mischievous, playing pranks, even taking "bike rides" through the long corridors of the Royal palace, sometimes led by the King himself.
Education

Maria and her siblings were raised by British nannies and educated by governesses and private tutors.
Maria's education followed the conventions for princesses of her time.
As Maria's eldest brothers were already occupied by their studies, she grew up closer to her sister Alexandra and her brother Nicholas, who preceded her in age.
In 1886, her mother took her to Russia for the first time.
Every two years, Princess Maria spent holidays in Denmark, visiting her paternal grandparents.
At Fredensborg Palace on the island of Zealand, Maria and her siblings met their Russian and British cousins in large family gatherings.
She became lifelong friends with two of her cousins: Grand Duchess Xenia of Russia and Princess Victoria of the United Kingdom.
A Princess of Greece

King George I instilled in his offspring a great love for Greece.
In her book of memoirs, she described herself as: " A true daughter of Greece".
In February 1897, King George sent his son, Prince George, to take possession of the island.
During the conflict, Queen Olga organized a military hospital and Princess Maria served as a nurse.
Since her sister Alexandra's marriage in 1889, Princess Maria became her father's favorite child and constant companion.
She helped her father acting as his unofficial secretary as her mother, Queen Olga, suffered from bad eyesight.
A Russian marriage

Princess Maria wanted to spend her entire life in Greece instead of following the traditional path of Princesses of her time that had to marry a foreign prince and move abroad.
Princess Maria found King Alexander too ugly and rejected him.
Since her childhood, Princess Maria of Greece had visited Russia many times with her mother, who remained very attached to her native country.
They usually stayed at Pavlovsk Palace with Princess Maria's maternal grandmother, Grand Duchess Alexandra Iosifovna.
While in Russia, in summer 1894, for the wedding of her cousin Grand Duchess Xenia to Grand Duke Alexander Mikhailovich, Princess Maria became smitten with the groom's brother, Grand Duke George Mikhailovich of Russia, who was her mother's first cousin.
In a subsequent visit to Russia in the autumn of 1895, they were reunited at a Court Ball.
She turned him down, to the dismay of Maria's mother, Queen Olga, who was in favor of a Russian marriage for her daughter.
In spring 1896, Grand Duke George Mikhailovich arrived in Athens and proposed while they were playing billiards.
For five years, Grand Duke George Mikhailovich of Russia persisted in his intention.
Twice a year, he proposed to Princess Maria who continued refusing him.
Tsar Nicholas II finally intervened, telling the grand duke to make only one more attempt and give up.
George Mikhailovich arrived in Greece in spring 1900.
This time, under pressure from her family, the Greek princess finally accepted his proposal, yet reluctantly.
Before she had a change of heart, Queen Olga hurried the wedding.
The marriage took place in Greece at the church of the old Venetian fortress in Corfu on 12 May  1900.
Grand Duchess of Russia

After the wedding, the couple boarded the Greek royal yacht and sailed to the Bay of Naples.
From Vienna, they arrived in Russia by the way of Warsaw.
Princess Maria of Greece, known in Russia as Grand Duchess Maria Georgievna of Russia, was welcomed by the Romanovs as one of their own.
Her mother, Queen Olga of Greece,  was a Russian Grand Duchess by birth, a first cousin of Tsar Alexander III of Russia.
Maria's father, King George of Greece, was Empress Maria Feodorovna's favorite brother.
Maria was a first cousin of Tsar Nicholas II, who she had known all her life.
Grand Duchess Maria and her husband settled in apartments located within the New Michael Palace on the Palace Quay in Saint Petersburg, the household of her father-in-law, Grand Duke Michael Nicholaievich.
They shared the large palace with the Grand Duke's widowed father and two unmarried brothers: Grand Duke Nicholas Mikhailovich, and Grand Duke Sergei Mihailovich, to whom Maria Gerogievna became particularly close.
Grand Duke George Mikhailovich had an injury in one leg in his youth, which curtailed the active military career he would have wanted; he occupied his time as director of the Alexander III museum where he moved his large numismatic collection.
Two days after Empress Alexandra Feodorovna gave birth to her fourth daughter, Grand Duchess Anastasia Nikolaevna, Grand Duchess Maria Georgievna gave birth to her first child, Princess Nina Georgievna on 20 June  1901.
Two years, two months and two days later on 22 August 1903, she had her second daughter and last child Princess Xenia Georgievna.
Shortly after Xenia's birth, Grand Duchess Maria's father in law became paralyzed by a stroke and moved permanently to the south of France to recover.
During the years living in Russia (1900–1914), Grand Duchess Maria traveled frequently to the South of France, Denmark, England, Germany, Italy and yearly to her native Greece.
In the summer of 1900, Maria Georgievna visited Crimea with her husband.
It was there, in a piece of land Grand Duke George had bought in the 1890s near Ai-Todor, on a  high cliff above the sea, that the couple decided to build their residence.
They commissioned the construction to Nikolay Petrovich Krasnov, a Russian architect who had built  the palace of Dulber between 1895 and 1897 for Grand Duke Peter Nikolaevich, and  who would build the white Palace at Livadia for Tsar Nicholas II and his wife Alexandra between (1910–1911).
Harax

As Grand Duchess Maria Georgievna was very fond of everything English, the villa was constructed in the English style with local limestone, but they gave the property a Greek name, Harax, the fortress, in memory of an  ancient fortress that once stood on the tip of Ai-Todor.
Grand Duchess Maria sketched the exterior elevations and draw floor plans while Grand Duke George painted renderings in watercolors and pen and ink sketches.
The two-story house, overlooking the Black Sea with a red-tiled roof and dotted with chimneys, was decorated by the Grand Duchess with English furniture, silverware, textiles, and wallpaper all imported from England.
For seven years the Grand Duke and his wife led a quiet life in Crimea, returning to St Petersburg in the winter for the social season at the Imperial capital.
With a poor command of Russian, Grand Duchess Maria spoke in French with her husband and in English with her daughters.
Princess Nina, the eldest was described by Baroness Agnes von Stoeckl  as "dark, calm and indolent" while Xenia, the youngest was "blond, vivacious and full of life".
Grand Duchess Maria hired an English nanny to educate them.
On 18 March 1913, King George I was assassinated in Thessalonica, a city that Greece had seized on during the First Balkan War.
For Maria Georgieva, who had been so close to her father it was a  terrible blow.
By 1914 the relationship between the Grand Duchess and her husband had deteriorated.
Grand Duke George was a devoted father and husband, but the Grand Duchess never fell in love with him.
She never liked Russia either and eventually became estranged from her husband.
War and Revolution

In the summer of 1914, the Grand Duchess left Russia with her two daughters and her lady in waiting, Baroness Agnes von Stoeckl for England to improve her daughter Xenia's frail health with the mineral waters of the Spa town of Harrogate, where they had been three times before.
The Grand Duke accompanied them to Warsaw in July.
After a stay at the Claridge's Hotel, the Princess moved to Harrogate, where Grand Duke George Mikhailovich was going to join them a few weeks later.
Grand Duke George was forced to cancel his trip as he had to resume his duties in the Tsarist army.
For her part, Grand Duchess Maria declined the chance to rush back to Russia with her aunt the Empress Maria Feodorovna, who was in London that summer.
Instead, the Grand Duchess decided to extend her stay in the United Kingdom with her daughters and later used  the dangers involved in a trip back during wartime in not attempting a return to Russia.
Determine to help with the war of the Triple Entente against the Central Powers, Grand Duchess Maria founded a small military hospital N 2 in Harrogate.
She undertook a Red Cross nursing course and already had experience of army medical service as a young princess in Greece, nursing patients herself.
This institution was so successful that by 1915 the Grand Duchess eventually created two other hospitals:  N 3 and a  home for convalescent patients in Harrogate.
Impressed by her work, her cousin, King George V, conferred her the Royal Red Cross in July 1915.
During the war years, Grand Duchess Maria lived with her daughters in Harrogate until July 1916 when they moved to a large mansion in Grosvenor Square in  London.
Grand Duchess Maria also regularly visited her cousin, Princess Victoria of the United Kingdom, her close friend since childhood.
The outbreak of the Russian Revolution in 1917 disrupted the daily life of  Grand Duchess Maria and her daughters, who ceased to receive income from St. Petersburg.
Unable to subsidize any longer the hospitals she patronized, the Grand Duchess entrusted them to the protection of her aunt Queen Alexandra.
Her reduced financial circumstances forced Grand Duchess Maria to move to a smaller residence next to Regent's Park.
It was though the financial support of her future sister-in-law, the wealthy American Nancy Leeds, that the Grand Duchess was able to maintain her finances afloat.
In 1918, Grand Duke George Mikhailovich was arrested by the Bolsheviks as he sought to emigrate to Britain.
Alarmed with the fate of her husband, Maria Georgievna made many efforts to obtain her husband's release, along with others of her Russian relatives.
After several months of uncertainty, the Grand Duke was finally shot on 30 January 1919 at the Peter and Paul Fortress by the Bolsheviks.
Along with her husband, Maria lost her brother-in-law Grand Duke Nicholas Mikhailovich, her former brother-in-law Grand Duke Paul Alexandrovich and her younger maternal uncle, Grand Duke Dimitri Constantinovich.
A Greek marriage

In her widowhood, Princess Maria of Greece reverted to her original name and title and her focus shifted to her own family.
At the outbreak of World War I, as Greece had been weakened by the Balkan Wars, King Constantine I opted for his country's neutrality.
His prime minister, Eleftherios Venizelos, who wanted Greece to enter the conflict on the side of the allies, clashed with the King.
In order to force the Greeks to join the allied cause, the French bombarded Athens and demanded King Constantine's departure.
Greece entered the war on the side of the allies while the Greek Royal Family left for exile in Switzerland with the sole exception of King Alexander.
With the tumultuous political situation in Greece, Princess Maria could not count on the support of her relatives.
While on a visit to Paris, Princess Maria met her nephew Alexander who Venizelos kept isolated from the Greek Royal Family.
King Alexander died in October 1920, following an infection from a monkey bite, and a plebiscite restored King Constantine I on the throne.
Princess Maria and her two daughters then joined King Constantine and the Greek Royal family in Italy, where the small group boarded a ship of the Hellenic Navy towards Corfu.
During this trip, Princess Maria met the commander of the ship, Admiral Perikles Ioannidis.
Widowed and determined to end her days with "Greek blood", the princess was smitten with the Greek Admiral.
Back in Greece, Maria settled in Athens.
She was much loved by the royal family, even winning the affection of the wife of the Diadochos George, Princess Elizabeth of Romania, whose relationship with the rest of her in-laws was difficult.
On the other hand, Princess Maria's relationship with her daughters was strained.
That they never were able to see him again, as Grand Duke George Mikhailovich had been killed during the Russian Revolution, only increased their resentment and they disapproved of their mother's relationship with Ioannidis.
In 1921, 17-year-old, Princess Xenia married William Bateman Leeds Jr., son of Nancy Leeds.
Princess Nina was married in London in September 1922 to Prince Paul Chavchavadze (1899–1971), son of Prince Alexander Chavchavadze and Maria Rodzianko.
The same month King Constantine had to abdicate after Greece lost the Greco-Turkish War of 1919–1922.
Princess Maria's eldest nephew succeeded him as King George II of Greece on 27 September 1922.
Three months later, despite her daughters' opposition, Princess Maria married Admiral Pericles Ioannides on 16 December 1922 in Wiesbaden, Germany.
A wandering life

After a honeymoon in Frankfurt and Munich Princess Maria of Greece and her second husband returned to Athens.
They left Greece at the time of the proclamation of the Second Hellenic Republic in 1924.
The couple moved to London to the house the Princess had in Regent's Park where they lived for a couple of years.
The Greek Princess devoted herself to drawing and she made a series of whimsical illustrations in color of exotic people and animals that she called "Katoufs" "making a face" in Greek.
She published her drawing as a children's book in 1925 with rhymes written by Princess Maria Trubetskoy, née Rodzianko (1877–1958).
The two women dedicated the book to their common grandson, Prince David Chavchavadze.
Princess Maria was Queen Alexandra's favorite niece and she was her constant companion during the Queen's last years at Sandringham.
After her two daughters had moved to the United States and her aunt Queen Alexandra had died, Princess Maria and her husband moved to Rome in 1926.
The Princess acquired a residence, the Villa Attica, located on via Antonio-Bertoloni.
The couple followed a relatively simple existence, and Princess Maria divided her time between gardening and the writing of her memoirs, published years later by her grandchildren.
Maria was an inveterate backgammon player while her husband carefully monitored their expenses.
Later life

Grand Duchess Maria Georgievna died in her native Athens during the Greco-Italian War (28 October 1940 – 30 April 1941)
Her daughter Xenia lived for years in Long Island and was for a time married to millionaire William Leeds, son of Nancy Stewart Worthington Leeds and the stepson of Maria's brother Prince Christopher.
Anderson fraudulently claimed to be Grand Duchess Anastasia Nikolaevna of Russia, the youngest daughter of her cousin, Emperor Nicholas II, and was forced to leave Xenia's house at the demand of William Leeds.
Grand Duchess Maria never recognized Anderson.
}} Media related to Grand Duchess Maria Georgievna of Russia at Wikimedia Commons



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
  AssignClass (47580741-93b3-40b8-af21-5ec819693f09)
 Call ID: 47580741-93b3-40b8-af21-5ec819693f09
  Args:
    source: :Princess_Maria_of_Greece_and_Denmark
    type: :Woman
  AssignClass (4248e602-503b-4d86-9dd8-a85fb939cda5)
 Call ID: 4248e602-503b-4d86-9dd8-a85fb939cda5
  Args:
    type: :Person
    source: :Princess_Maria_of_Greece_and_Denmark
  AddLiteral (f2064bfe-d628-49ed-bb44-74bb2313f36a)
 Call ID: f2064bfe-d628-49ed-bb44-74bb2313f36a
  Args:
    literal_value: 1876
    literal_type: xsd:integer
    source: :Princess_Maria_of_Greece_and_Denmark
    relation: :hasBirthYear
  AddLiteral (8f22c6cf-8d24-49ae-812f-d3ebe37f9f93)
 Call ID: 8f22c6cf-8d24-49ae-812f-d3ebe37f9f93
  Args:
    literal_value: 1940
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Princess_Maria_of_Greece_and_Denmark
  AssignClass (0bc9686b-7e81-449a-81ac-e11bf3851ac4)
 Call ID: 0bc9686b-7e81-449a-81ac-e11bf3851ac4
  Args:
    type: :Man
    source: :King_George_I_of_Greece
  AssignClass (8356c2b8-fcf2-4620-b7c3-56f18ff31bc5)
 Call ID: 8356c2b8-fcf2-4620-b7c3-56f18ff31bc5
  Args:
    type: :Person
    source: :King_George_I_of_Greece
  AssignClass (8f2fe4ad-763d-4b59-a804-8d3f9cfad1ad)
 Call ID: 8f2fe4ad-763d-4b59-a804-8d3f9cfad1ad
  Args:
    type: :Woman
    source: :Grand_Duchess_Olga_Constantinovna_of_Russia
  AssignClass (62c23b85-c849-4e40-8525-fd2b9d3f87a0)
 Call ID: 62c23b85-c849-4e40-8525-fd2b9d3f87a0
  Args:
    type: :Person
    source: :Grand_Duchess_Olga_Constantinovna_of_Russia
  AddTriple (6694d9bb-c867-4dcc-9daa-95a117db1c2d)
 Call ID: 6694d9bb-c867-4dcc-9daa-95a117db1c2d
  Args:
    source: :Princess_Maria_of_Greece_and_Denmark
    relation: :hasFather
    target: :King_George_I_of_Greece
  AddTriple (e8ecc775-f3b8-4733-9ec8-2ac9174c5530)
 Call ID: e8ecc775-f3b8-4733-9ec8-2ac9174c5530
  Args:
    target: :Grand_Duchess_Olga_Constantinovna_of_Russia
    source: :Princess_Maria_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (8e6ba4d7-4000-4ccd-a372-3a92dd8f4380)
 Call ID: 8e6ba4d7-4000-4ccd-a372-3a92dd8f4380
  Args:
    source: :King_Constantine_I_of_Greece
    type: :Man
  AssignClass (3e16278a-2552-4f11-add3-e535036d4ed0)
 Call ID: 3e16278a-2552-4f11-add3-e535036d4ed0
  Args:
    source: :King_Constantine_I_of_Greece
    type: :Person
  AddTriple (75c74b5c-8173-4974-a155-e5aef7f5d08f)
 Call ID: 75c74b5c-8173-4974-a155-e5aef7f5d08f
  Args:
    target: :King_Constantine_I_of_Greece
    relation: :hasBrother
    source: :Princess_Maria_of_Greece_and_Denmark
  AssignClass (346ff32c-39ef-4c85-8782-0014c4a90ec5)
 Call ID: 346ff32c-39ef-4c85-8782-0014c4a90ec5
  Args:
    type: :Man
    source: :Grand_Duke_George_Mikhailovich_of_Russia
  AssignClass (9abcdcbb-af57-4c29-a649-2692318a676d)
 Call ID: 9abcdcbb-af57-4c29-a649-2692318a676d
  Args:
    source: :Grand_Duke_George_Mikhailovich_of_Russia
    type: :Person
  AddLiteral (ba51ee21-d1b3-404e-a0ce-2d9650fe8687)
 Call ID: ba51ee21-d1b3-404e-a0ce-2d9650fe8687
  Args:
    literal_value: 1900
    source: :Princess_Maria_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (6c435270-157f-4125-bc3e-216def8d0c99)
 Call ID: 6c435270-157f-4125-bc3e-216def8d0c99
  Args:
    relation: :hasRelation
    source: :Princess_Maria_of_Greece_and_Denmark
    target: :Grand_Duke_George_Mikhailovich_of_Russia
  AssignClass (64d335b9-4e6b-44d3-b35c-3c82d4c331d5)
 Call ID: 64d335b9-4e6b-44d3-b35c-3c82d4c331d5
  Args:
    source: :Princess_Nina_Georgievna
    type: :Woman
  AssignClass (67815296-6166-4371-a947-b5ed122bfafe)
 Call ID: 67815296-6166-4371-a947-b5ed122bfafe
  Args:
    source: :Princess_Nina_Georgievna
    type: :Person
  AddTriple (5c187a8e-930e-448f-8b6c-b812cf1b467a)
 Call ID: 5c187a8e-930e-448f-8b6c-b812cf1b467a
  Args:
    target: :Princess_Nina_Georgievna
    source: :Princess_Maria_of_Greece_and_Denmark
    relation: :hasChild
  AssignClass (3eca71fe-6391-476d-a95a-d40b8b063bfc)
 Call ID: 3eca71fe-6391-476d-a95a-d40b8b063bfc
  Args:
    type: :Woman
    source: :Princess_Xenia_Georgievna
  AssignClass (5bf031bb-7407-4f3f-8561-e3498a793bf5)
 Call ID: 5bf031bb-7407-4f3f-8561-e3498a793bf5
  Args:
    source: :Princess_Xenia_Georgievna
    type: :Person
  AddTriple (917e582b-ef05-4a51-a118-8723cf32d8aa)
 Call ID: 917e582b-ef05-4a51-a118-8723cf32d8aa
  Args:
    relation: :hasChild
    source: :Princess_Maria_of_Greece_and_Denmark
    target: :Princess_Xenia_Georgievna
  AssignClass (c237284a-656e-47aa-8de0-1d4ea4bd1dae)
 Call ID: c237284a-656e-47aa-8de0-1d4ea4bd1dae
  Args:
    source: :Admiral_Pericles_Ioannides
    type: :Man
  AssignClass (7e3bd6fb-6a71-48c4-b70e-dbc59163c625)
 Call ID: 7e3bd6fb-6a71-48c4-b70e-dbc59163c625
  Args:
    source: :Admiral_Pericles_Ioannides
    type: :Person
  AddLiteral (871ed606-51f8-4a00-8ecf-1f96b3ad950b)
 Call ID: 871ed606-51f8-4a00-8ecf-1f96b3ad950b
  Args:
    literal_value: 1922
    source: :Princess_Maria_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (b3de7a74-4975-40e1-8a8e-292766b4788a)
 Call ID: b3de7a74-4975-40e1-8a8e-292766b4788a
  Args:
    target: :Admiral_Pericles_Ioannides
    relation: :hasRelation
    source: :Princess_Maria_of_Greece_and_Denmark
  Finish (93cdb41f-3a8f-49c3-bf18-5a0c4eff9cb2)
 Call ID: 93cdb41f-3a8f-49c3-bf18-5a0c4eff9cb2
  Args: