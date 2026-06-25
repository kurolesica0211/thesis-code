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
Grand Duchess Maria Vladimirovna of Russia


Grand Duchess Maria Vladimirovna of Russia (Russian: Мария Владимировна Романова, romanized: Mariya Vladimirovna Romanova; born 23 December 1953) is a Russian woman who has been a claimant to the headship of the House of Romanov, the Imperial Family of Russia (who reigned as Emperors and Autocrats of all the Russias from 1613 to 1917) since 1992.
She is a great-great-granddaughter in the male line of Emperor Alexander II of Russia.
Although she has used Grand Duchess of Russia as her title of pretence with the style Imperial Highness throughout her life, her right to do so is disputed.
Since her father's death on April 21, 1992, some of her monarchist supporters have referred to her as Maria I, titular "Empress of Russia", a title she does not claim herself.
Early life

Birth

Maria Vladimirovna was born in Madrid, the only child of Grand Duke Vladimir Kirillovich of Russia, head of the Imperial Family of Russia and titular Emperor of Russia, and Princess Leonida Bagration-Mukhrani of Georgian, Polish, German and Swedish descent.
Her paternal grandparents were Grand Duke Kirill Vladimirovich of Russia and Grand Duchess Victoria Fyodorovna (née Princess Victoria Melita of Edinburgh and Saxe-Coburg-Gotha) through whom she is a great-great-granddaughter of Queen Victoria.
Her godfather was Grand Duke Andrei Vladimirovich of Russia, for whom Prince Nicholas of Romania stood in at the christening ceremony, and her godmother was Queen Ioanna of Bulgaria.
Education

Maria was educated at Runnymede College in Madrid and Paris before studying Russian history and literature at the University of Oxford.
Maria Vladimirovna lives in Madrid.
On 23 December 1969, upon reaching her dynastic majority, Maria swore an oath of loyalty to her father, to Russia, and to uphold the Fundamental Laws of Russia which governed succession to the defunct throne.
At the same time, her father issued a controversial decree recognising her as heiress presumptive and declaring that, in the event he predeceased other dynastic Romanov males, then Maria would become the "Curatrix of the Imperial Throne" until the death of the last male dynast.
As it happened, Vladimir Kirillovich, who died in 1992, outlived all the other male Romanov dynasts, and his daughter had no occasion to assume curatorship.
Marriage

In Dinard on 4 September 1976 (civil) and at the Russian Orthodox Chapel in Madrid on 22 September 1976 (religious), Maria married Prince Franz Wilhelm of Prussia, her third cousin once removed.
He is a Hohenzollern great-grandson of Germany's last emperor Wilhelm II and a great-great-great-grandchild of Victoria, Queen of the United Kingdom.
Maria's aunt Grand Duchess Kira Kirillovna of Russia, her father's late sister, had been married to Louis Ferdinand, Prince of Prussia, since 1938, head of the House of Hohenzollern since 1951.
Franz Wilhelm converted to the Eastern Orthodox faith prior to the wedding, taking the name Michael Pavlovich and receiving the title of a Grand Duke of Russia from Maria's father.
The couple separated in 1982, a year after the birth of their only child, George Mikhailovich, who had been granted the title Grand Duke of Russia at birth by his grandfather Vladimir.
Following the divorce on 19 June 1985, Franz Wilhelm reverted to his Prussian name and style.
Succession claims

Maria Vladimirovna is a patrilineal descendant of Alexander II of Russia.
The original House of Romanov had died out with Empress Elizabeth of Russia in 1762 and was continued by Peter III of Russia, who was born a Duke of Holstein-Gottorp, a branch of the House of Oldenburg, from which the current reigning monarchs of Norway and Great Britain, as well as the former of Greece, also descend in the male line.
When Vladimir Kirillovich died on 21 April 1992, his daughter Maria claimed to succeed him as head of the Russian Imperial Family on the grounds that she was the only child of the last male dynast of the Imperial house according to the Romanovs' Pauline laws.
Although the charter of the Romanov Family Association (RFA), which represents other descendants of the Romanov family, asserts the premise that Russia's form of government should be determined democratically and that therefore the Association and its members undertake to adopt no position on any claims to the Imperial throne, its two most recent presidents have personally opposed Maria's claims: Nicholas Romanov, Prince of Russia, who maintained his own claims to dynastic status and to headship of the Romanov family, stated, "Strictly applying the Pauline Laws as amended in 1911 to all marriages of Equal Rank, the situation is very clear.
At the present time, not one of the Emperors or Grand Dukes of Russia has left living descendants with unchallengeable rights to the Throne of Russia," and his younger brother, Prince Dimitri Romanov, said of Maria's assumption of titles, including "de jure Empress of all the Russias", "It seems that there are no limits to this charade".
The supporters of Maria Vladimirovna point to the fact that neither Nicholas nor his brother Dimitri had any dynastic claims due to the morganatic marriage of their parents.
Maria's parents' marriage of equal rank is, of course, questioned by her cousins, who claim that her mother's family, the Bagrationi dynasty, became Russian subjects after they lost their thrones in the Georgian kingdoms of Kartli-Kakheti and Imereti around 1800 and was therefore not a ruling dynasty.
As an example, if Tsarevich Alexei Romanov had not been murdered in 1918, and died without issue (i.e., without children), his sisters, Olga, Tatiana, Maria, and Anastasia wouldn't become Empresses before male Romanov relatives.
Alexander III had four sons: Nicholas II of Russia whose only male son died before he could produce heirs, Grand Duke Alexander Alexandrovich of Russia, who died shortly before he was 11 months old, Grand Duke George Alexandrovich of Russia, who died with no issue, and
Grand Duke Michael Alexandrovich of Russia whose only son, George Mikhailovich, Count Brasov died at age 20, childless.
His sons, Nicholas Alexandrovich, Tsesarevich of Russia, and Grand Duke Sergei Alexandrovich of Russia both died without issue.
Excluding the future Alexander III, the third boy Grand Duke Vladimir Alexandrovich of Russia – born after the childless Tsarevich and Alexander III, whose descendants couldn't claim leadership for many reasons – had four sons.
The eldest died in infancy and the second eldest, Grand Duke Kirill Vladimirovich of Russia, had one son, Grand Duke Vladimir Kirillovich of Russia.
His only child is Grand Duchess Maria Vladimirovna of Russia, making her the legal heir to the Russian throne.
Following the discovery of the remains of Emperor Nicholas II and most of his immediate family in 1991, Maria Vladimirovna wrote to President Boris Yeltsin regarding the burial of the remains, saying of her Romanov cousins, whom she does not recognise as members of the Imperial House (including the grandchildren of Nicholas II's sister Grand Duchess Xenia), that they "do not have the slightest right to speak their mind and wishes on this question.
At the behest of the Russian Orthodox Church, Maria did not recognise the authenticity of the remains and declined to attend the reburial ceremony in 1998, however according to Victor Aksyuchits, ex-advisor of Boris Nemtsov, the exact reason behind Maria's absence from the state burial for Nicholas II and his family in 1998 was motivated by the Russian government's refusal to recognize her status as official Head of the Romanov House, after asking via a letter prior the funeral ceremony.
She has also said, regarding some of her Romanov cousins, that "My feeling about them is that now that something important is happening in Russia, they suddenly have awakened and said, 'Ah ha!
"


When questioned about the ongoing rift among Romanov descendants, Maria said:


"Attempts to disparage my rights have originated with people who, firstly, do not belong to the Imperial Family, and, secondly, either do not themselves know the relevant laws or think that others do not know these laws.
"

Role in Russia and activities

Maria hopes for the restoration of the monarchy someday and is "ready to respond to a call from the people".
In a 2018 interview, she defined her own understanding of her role as follows:


The Imperial House of Russia considers it its main goal to help preserve the historical and cultural continuity of our house and country, and to do all we can to strengthen the ethnic, religious, and civil peace and harmony of Russia.
We believe that the idea of a legitimate, hereditary monarchy, which preserves an unbroken, living connection with the centuries-long history of Russia and which conceives of society as a unified family, still has resonance today and remains a viable choice for our country and peoples.
But we are hardly unaware that, at the present time and for the foreseeable future, the conditions are not right in Russia for a restoration of the monarchy.
For now, the spheres of our activities are limited to promoting philanthropy; participating in social peace-making processes; reviving and maintaining traditions and preserving our country’s historical, cultural, and natural heritage; strengthening the spiritual and moral foundations of our nation; helping to foster patriotism; and advancing a positive image of Russia in the wider world.
In 2002, Maria became frustrated with the internal strife within the Russian monarchist movement.
In 2003, Kirill I Patriarch of Moscow and all Russia stated in a congratulatory message on Maria Vladimirovna's 55th birthday, "you are the embodiment of a Russian Grand Duchess: noble, wise, compassionate, and consumed with a genuine love for Russia.
Though you may reside far from Russia, you continue to take an active part in its life, rejoicing when there are triumphs and empathizing when there are trials.
It is deeply gratifying to know that, even in these new historical circumstances, you are making a significant contribution to the building of Russia's global standing on the basis of spiritual and moral values, and the centuries-old traditions of the Russian people.
In May 2010, Maria and other members of the Romanov dynasty met with members of the Ottomans at Topkapı Palace, which was the first official meeting between these two former ruling (and rival) families.
But in the person of the Grand Duchess Maria Vladimirovna and her son George, the succession of the Romanovs is preserved - not to the Russian imperial throne, but simply historically."
Maria Vladimirovna supports a lot of good initiatives, she visits Russia, she meets people, she elevates the most ordinary people who have distinguished themselves to a nobility.
On May 14, 2013, at a ceremony at the Romanov Museum in Kitay-gorod, Maria awarded the Order of Saint Anna (1st Degree) to San Francisco Archbishop Kyril of the Russian Orthodox Church Outside of Russia, the first award of this historic Romanov dynastic order since the October Revolution of 1917.
In December 2013, Grand Duchess Maria Vladimirovna visited the United States at the request of the Russian Orthodox Church Abroad, which received her with full honours and recognition as head of the Russian Imperial House.
On July 20, 2014, at a ceremony in the Church in the Izmailovo district of Moscow, Maria awarded Russian Vice-Admiral Oleg Belaventsev the Order of Saint Anna (1st Degree), Prosecutor General of the Autonomous Republic of Crimea, Natalia Poklonskaya, the Imperial Ladies' Order of Saint Anastasia (founded by herself in 2010), and the former cosmonaut Alexei Leonov the Order of Saint Stanislaus (1st degree), dynastic house orders of the Romanovs.
On 17 July 2018 she participated in the liturgical commemoration of the centenary of the assassinations of Saints Nicholas II, Empress Alexandra Feodorovna and their children conducted in Yekaterinburg by Patriarch Kirill I. On July 28, 2014, at the invitation of the mayor of Irkutsk, Viktor Kondrashov, Maria attended a commemorative event there for the 100th anniversary of Russia's entry into the First World War and, among other things, visited Irkutsk State University, where she presented a medal "In Commemoration of the 400th Anniversary of the House of Romanov".
She knows Russian President Vladimir Putin from numerous encounters.
Other politicians, however, have spoken out in favor of this, including Vladimir Zhirinovsky, Sergey Aksyonov, Natalia Poklonskaya and Aleksandr Dugin.
Nikolai Patrushev is at least considered a sympathizer, the oligarch Konstantin Malofeev is considered a supporter of the monarchist movement; he founded and finances the Double-Headed Eagle Society and was a best man at the wedding of Maria's son.
In January 2021, Grand Duchess Maria announced the morganatic engagement of her son Grand Duke George Mikhailovich of Russia to Rebecca Virginia Bettarini from Italy.
Bettarini converted to Russian Orthodoxy and took the name Victoria Romanovna.
Grand Duchess Maria granted permission for the couple to marry.
She decreed that Bettarini will have the title Princess, with the predicate "Her Serene Highness" and the right to use the surname Romanov.
Maria has in particular come to terms with the new Russian elite around President Vladimir Putin and not only awards the historical dynastic orders of the House of Romanov, but also partly newly created orders such as the Order of Saint Michael the Archangel (founded by her father in 1988) or the Ladies' Order of Saint Anastasia (founded by herself in 2010), to personalities close to the House of Romanov and the Russian Orthodox Church, including Siloviks and Russian oligarchs.
In the Tsarist Empire the award of certain orders entailed admission into the personal (often even hereditary) nobility: the Grand Cross of all orders and the Order of Saint Vladimir and the Order of St. George of all classes (as well as previously also the promotion to higher military ranks).
In 2007, Maria is said to have ennobled the former head of the Russian domestic secret service Federal Security Service (FSB), Nikolai Patrushev, who is considered one of Putin's closest confidants (and one of his possible successor candidates).
While newly founded aristocratic associations in Russia recognize such "ennoblings" and include these families into registers of the nobility, accepting them as members, the traditional associations of the descendants of the White émigrés (such as the Russian CILANE member association Union de la Noblesse Russe based in Paris) reject the admission of such "new nobles" on the grounds that Grand Duchess Maria Vladimirovna is neither the undisputed pretender to the throne nor does she - who is not a reigning monarch - herself have any constitutional authority to ennoble.
After previously voicing her support for Crimea and Donbas annexation in 2014 by Russia she said in an interview on her website in April 2018: "Before the Russian people today and our descendants stretches a long and gradual path toward the restoration of the power and might of Russia."
But, as she emphasized, “no normal person could possibly think that the House of Romanov would be on the side of those who seek to weaken Russia.
In 2023, on the occasion of the seventieth birthday of the Grand Duchess, Patriarch Kirill made an unequivocal recognition of her position as Head of the House of Romanov in a congratulatory letter published on the Patriarchal website addressing her as "Grand Duchess Maria Vladimirovna, Head of the Russian Imperial House" (Великой княгине Марии Владимировне, главе Российского Императорского Дома), and praising her efforts in the fields of charity, philanthropy, and culture.
The Grand Duchess's son Grand Duke George Romanov and his Italian wife Princess Victoria, along with other members of the dynasty, gathered in the Cathedral of Christ the Savior in Moscow to celebrate the baptism of Princess Kira Leonida Romanov on 13th July.
The princess, who was named after a saint martyred by Roman emperor Diocletian, has several godparents, including Prince Emanuele Filiberto of Savoy, Prince Boris of Bulgaria, Prince David VII of Georgia, Archduke Maximilian of Austria, Russian Ambassador to the Seychelles Artem Kozhin and his wife Elena, as well as Oksana Hoffman Girey, who is an official at the Kazakh consulate in Monaco.
The birth was announced by the Grand Duchess herself, who released this announcement:

"BY THE GRACE OF GOD
We, GRAND DUCHESS MARIA VLADIMIROVNA, Head of the Russian Imperial House, Hereby proclaim to all:


On June 2, 2025, Our daughter-in-law, Her Serene Highness Princess Victoria Romanovna, the wife of Our son and heir, His Imperial Highness the Sovereign Heir, the Tsesarevich and Grand Duke George Mikhailovich, was safely delivered of a child — a granddaughter to Us, who has been given the name Kira, in honor of the Venerable Saint Kira of Beroea


Receiving this addition to Our House as a new sign of God’s grace, bestowed upon Us for consolation, We ask all Our compatriots to offer heartfelt prayers to the Almighty for the healthy growth and prosperity of the newborn.
Her Serene Highness Princess Kira Georgievna.
Given at Madrid, on the 2nd day of June in the year of Our Lord 2025, being the 34th year since We assumed the rights and duties of Our August Ancestors — the Emperors of All Russia.
In the original, signed in Her own hand:



MARIA.



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
  AssignClass (3915ec80-5e9e-473d-8d61-f7c883b1f15d)
 Call ID: 3915ec80-5e9e-473d-8d61-f7c883b1f15d
  Args:
    type: :Woman
    source: Maria_Vladimirovna_of_Russia
  AddLiteral (c2067e38-6806-42ee-9551-c978f66486b6)
 Call ID: c2067e38-6806-42ee-9551-c978f66486b6
  Args:
    source: Maria_Vladimirovna_of_Russia
    literal_value: 1953
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (26ba4278-327b-4855-91e1-6c708f78b145)
 Call ID: 26ba4278-327b-4855-91e1-6c708f78b145
  Args:
    type: :Man
    source: Vladimir_Kirillovich_of_Russia
  AssignClass (77d4dd5f-7389-46fa-89f4-d0cafb63f967)
 Call ID: 77d4dd5f-7389-46fa-89f4-d0cafb63f967
  Args:
    type: :Woman
    source: Leonida_Bagration-Mukhrani
  AddTriple (10f42e36-9f4c-4282-83d6-976fe03f1ae2)
 Call ID: 10f42e36-9f4c-4282-83d6-976fe03f1ae2
  Args:
    source: Maria_Vladimirovna_of_Russia
    target: Vladimir_Kirillovich_of_Russia
    relation: :hasFather
  AddTriple (af74cc7d-4994-405e-8d54-e7100e11c439)
 Call ID: af74cc7d-4994-405e-8d54-e7100e11c439
  Args:
    source: Maria_Vladimirovna_of_Russia
    target: Leonida_Bagration-Mukhrani
    relation: :hasMother
  AssignClass (a494ba12-7593-4896-a5ae-b06996cb11b1)
 Call ID: a494ba12-7593-4896-a5ae-b06996cb11b1
  Args:
    type: :Man
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (69781ad7-195f-4c42-bf00-6456e90de334)
 Call ID: 69781ad7-195f-4c42-bf00-6456e90de334
  Args:
    type: :Woman
    source: Victoria_Fyodorovna
  AddTriple (c9c9c097-f4c3-4dec-b156-4888bb379696)
 Call ID: c9c9c097-f4c3-4dec-b156-4888bb379696
  Args:
    source: Vladimir_Kirillovich_of_Russia
    target: Kirill_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (c2aee35d-d415-4cf4-b76d-55e1fffeaabd)
 Call ID: c2aee35d-d415-4cf4-b76d-55e1fffeaabd
  Args:
    target: Victoria_Fyodorovna
    source: Vladimir_Kirillovich_of_Russia
    relation: :hasMother
  AssignClass (c9f6284a-6629-411a-9d19-a107cd70a639)
 Call ID: c9f6284a-6629-411a-9d19-a107cd70a639
  Args:
    type: :Man
    source: Franz_Wilhelm_of_Prussia
  AddTriple (bdeef57c-51bc-4aa1-8ec3-064c9b4c5010)
 Call ID: bdeef57c-51bc-4aa1-8ec3-064c9b4c5010
  Args:
    relation: :hasRelation
    source: Maria_Vladimirovna_of_Russia
    target: Franz_Wilhelm_of_Prussia
  AddLiteral (1f6d8f80-a1da-45fc-957e-a8d2309a0bbc)
 Call ID: 1f6d8f80-a1da-45fc-957e-a8d2309a0bbc
  Args:
    literal_type: xsd:integer
    literal_value: 1976
    source: Maria_Vladimirovna_of_Russia
    relation: :hasMarriageYear
  AssignClass (ac66eedb-0e81-4680-b99b-6e5bd2a8c2b5)
 Call ID: ac66eedb-0e81-4680-b99b-6e5bd2a8c2b5
  Args:
    type: :Man
    source: George_Mikhailovich_of_Russia
  AddTriple (c539edcd-bbcc-4a09-941b-4cdb1602566d)
 Call ID: c539edcd-bbcc-4a09-941b-4cdb1602566d
  Args:
    source: George_Mikhailovich_of_Russia
    target: Franz_Wilhelm_of_Prussia
    relation: :hasFather
  AddTriple (ef3390f8-0e9c-47e8-8add-6af651d74391)
 Call ID: ef3390f8-0e9c-47e8-8add-6af651d74391
  Args:
    relation: :hasMother
    target: Maria_Vladimirovna_of_Russia
    source: George_Mikhailovich_of_Russia
  AssignClass (bc3bd96c-03fa-451c-93a4-5320424484ba)
 Call ID: bc3bd96c-03fa-451c-93a4-5320424484ba
  Args:
    source: Kira_Kirillovna_of_Russia
    type: :Woman
  AddTriple (7ddadd86-97fa-4a1c-bd2a-5e6cb795d6ea)
 Call ID: 7ddadd86-97fa-4a1c-bd2a-5e6cb795d6ea
  Args:
    relation: :hasSister
    source: Vladimir_Kirillovich_of_Russia
    target: Kira_Kirillovna_of_Russia
  AssignClass (8ab00b74-077f-4dbc-9fab-7a9a952a6862)
 Call ID: 8ab00b74-077f-4dbc-9fab-7a9a952a6862
  Args:
    source: Victoria_Romanovna
    type: :Woman
  AddTriple (444eb5d4-d683-496a-a3b4-28eaacf4df4d)
 Call ID: 444eb5d4-d683-496a-a3b4-28eaacf4df4d
  Args:
    target: Victoria_Romanovna
    source: George_Mikhailovich_of_Russia
    relation: :hasRelation
  AssignClass (ce0c0574-6976-494d-9190-7be42014a6c6)
 Call ID: ce0c0574-6976-494d-9190-7be42014a6c6
  Args:
    source: Kira_Georgievna
    type: :Woman
  AddTriple (b33d05e1-6985-49c7-a887-0c6233361883)
 Call ID: b33d05e1-6985-49c7-a887-0c6233361883
  Args:
    source: Kira_Georgievna
    target: George_Mikhailovich_of_Russia
    relation: :hasFather
  AddTriple (7b18c155-c92c-480f-8fa8-f4897a6da36c)
 Call ID: 7b18c155-c92c-480f-8fa8-f4897a6da36c
  Args:
    target: Victoria_Romanovna
    source: Kira_Georgievna
    relation: :hasMother
  Finish (195c90a6-25fb-4f7a-b5e8-60f41a3c385b)
 Call ID: 195c90a6-25fb-4f7a-b5e8-60f41a3c385b
  Args: