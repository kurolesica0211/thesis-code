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
Grand Duke Andrei Vladimirovich of Russia (Russian: Андре́й Влади́мирович; 14 May  1879 – 30 October 1956) was the youngest son of Grand Duke Vladimir Alexandrovich of Russia, and thus a grandson of Emperor Alexander II and the first cousin of Nicholas II, the last Russian emperor.
In 1900, he began an affair with the famous ballerina Mathilde Kschessinska, becoming the third grand duke to fall for her.
Grand Duke Andrei followed a military career and graduated from the  Alexandrovskaya Military Law academy in Saint Petersburg in 1905.
He took part in World War I, but was away from real combat, spending most of the conflict at Russia's General Staff headquarters or in idle time in ceremonial positions in Saint Petersburg.
In February 1917, shortly before the fall of the Russian monarchy, Grand Duke Andrei left Saint Petersburg to join his mother in Kislovodsk in the northern Caucasus.
After the October Revolution of November 1917, he was briefly arrested along with his brother, Grand Duke Boris, but they escaped.
He departed revolutionary Russia in March 1920, being the last grand duke to leave for exile.
In 1921, he married his longtime mistress, Mathilde Kschessinska (1872-1971), and recognized her son Vladimir (or "Vova") as his own.
After World War II, Grand Duke Andrei lived in reduced circumstances.
At his death at age 77, he was the last surviving Russian grand duke born in Imperial Russia.
Early life

Grand Duke Andrei Vladimirovich of Russia was born on 14 May  1879 in Tsarskoye Selo, at his parents country residence, the Vladimir Villa.
He was the youngest of the four Vladimirovich sons; a sister followed him a few years later, and the eldest of his brothers died in early childhood.
His father, Grand Duke Vladimir Alexandrovich, a brother of Tsar Alexander III of Russia, was a renowned patron of the arts.
Andrei's mother, Grand Duchess, Maria Pavlovna, née a Duchess of Mecklenburg-Schwerin, was one of the greatest hostesses of Russian society.
Both parents doted on their four surviving children: Andrei, his two eldest brothers, Kirill and Boris, and their younger sister, Grand Duchess Elena.
Raised by British nannies, English was Andrei's first language.
Grand Duke Andrei grew up in opulence.
The family's main residence was the Vladimir Palace in Saint Petersburg, but as his father preferred country life, they spent the greater part of the year at the Vladimir Villa, a mansion in Tsarskoye Selo, returning to Saint Petersburg during the winter.
Following Romanov tradition, Andrei was destined to follow a military career.
While his eldest brother, Kirill, chose the Imperial navy, Andrei and his brother Boris joined the infantry.
Andrei began his military service in August 1898 as lieutenant in the Guards Horse-Artillery Brigade.
In spite of his appointments, Grand Duke Andrei did not have much interest in his military career.
Relationship with Kschessinska

Grand Duke Andrei was tall, shy and good looking.
He was a good friend of his cousin Grand Duke Michael Alexandrovich, who was a year older.
In February 1900, Grand Duke Andrei was invited by his brothers, Grand Dukes Kirill and Boris, to a dinner party at the house of Mathilde Kschessinska.
Grand Duke Andrei sat next to his hostess during the dinner, but accidentally spilt a glass of red wine on her.
Mathilde, attracted to the young grand duke, seven years her junior, took the incident as good omen.
She subsequently began a long time affair with Grand Duke Sergei Mikhailovich of Russia, Nicholas and Andrei's first cousin once removed.
As she was not in love with Sergei, but enjoyed his company and protection, Mathilde pursued a relationship with Grand Duke Andrei, the third Romanov to become involved with her.
Grand Duke Sergei tolerated their affair, remaining a close and loyal friend to the famous ballerina, but the relationship between the two grand dukes grew tense.
Both grand dukes were at first convinced they were the child's father.
After the Revolution, Kschessinska and Grand Duke Andrei maintained that Andrei was the father.
The child, who became known within the family by his nickname, Vova, received the name and patronymic Vladimir Sergeievich.
Grand Duke Sergei was devoted to the child, looking after mother and son until his exile and subsequent execution following the fall of the Russian monarchy.
The question of Vladimir's paternity remains unresolved.
However, most sources attribute the paternity to Grand Duke Andrei Vladimirovich, whom the child resembled.
A Russian Grand Duke

In 1903, Grand Duke Andrei purchased his own palace.
As upkeep of the mansion was expensive, it was sold to Grand Duke Andrei for 400 thousand rubles.
Grand Duke Andrei seldom lived there.
Grand Duke Andrei could neither openly live together with Mathilda nor did there exist the possibility of contracting a morganatic marriage with her.
The couple always had to travel with his Aide-de-camp, Feodor Von Kube, and when Grand Duke Andrei was invited to events, Mathilda could not join him.
As a member of the Russian Imperial family, Grand Duke Andrei took some duties of representation.
In 1911, he visited Ferdinand I of Bulgaria for a second time as a representative of Russia, and he was appointed senator in that year.
In the summer of 1912, Grand Duke Andrei fell ill with bronchitis.
Fearing the onset of tuberculosis, he was sent to recuperate in the Crimea, staying in a palace owned by his cousin Grand Duke Nikolai Nikolayevich.
Upon his return to Russia, Andrei Vladimirovich took part in the 300th anniversary celebrations of the Romanov dynasty.
Villa Alam was completely remodeled and Andrei and Mathilde returned there in the spring of 1914, hoping to stay there every spring.
War and revolution

With the outbreak of World War I, Grand Duke Andrei joined the staff at the headquarters of the Northwestern front fighting against Germany.
By 1916, Grand Duke Andrei joined other members of his family in political intrigues against the Empress who was in charge of the government in Saint Petersburg while Nicholas II was away at Russia's war military headquarters.
In December 1916, the Assassination of Rasputin, in which Grand Duke Dmitri Pavlovich and Prince Felix Yusupov took part, divided the Romanov family further.
Grand Duke Andrei joined many of his relatives in asking for clemency for the culprits.
As Andrei's ambitious mother intrigued against Empress Alexandra, Nicholas II ordered the Grand Duchess to leave Saint Petersburg for a time.
After a short personal interview with Nicholas II, on 16 January 1917, Grand Duke Andrei left for Kislovodsk, a spa resort town in the Caucasus.
Andrei Vladimirovich and his mother were in Kislovodsk when Nicholas II was forced to abdicate at the outbreak of the February Revolution.
The diaries of Grand Duke Andrei, written while he was in the army in the North-Eastern Front (1914–1915) and in Petrograd (1916–1917), have survived at the State Archives of the Russian Federation.
In July 1917, Mathilde and her son escaped the disturbance in Saint Petersburg, joining Andrei in Kislovodsk.
However, they could not live together as Grand Duchess Maria Pavlovna was reluctant to acknowledge their presence.
Andrei found separate living arrangements for them while he settled in a different villa with his brother Grand Duke Boris, who arrived in September.
During the period of the provisional government Grand Duke Andrei, his brother and mother lived mostly undisturbed in Kislovodsk, protected by local Cossacks.
Seventeen of the 52 Romanovs living in Russia were executed during the red terror.
Escaping the Bolsheviks

The Bolsheviks arrested Grand Duke Andrei and his brother Boris on the night of 7 August 1918, after a systematic search of their villa.
Likely to be rearrested, the two grand dukes escaped to the surrounding mountains with Andrei's aide-de-camp, Colonel Von Kube, on 26 August 1918.
They lived in hiding for almost five weeks, moving from village to village under protection of the Kabarda tribes, sheltered by Colonel Andrei Shkuro and his band of loyal Cossacks.
On the evening of 23 September, Grand Duke Andrei, his brother Boris and Colonel Von Kube returned to the city on horseback, accompanied by Kabardian nobles who had protected them.
During their time hiding in the mountains, Andrei allowed his beard to become overgrown.
However, Grand Duchess Maria Pavlovna was determined to remain in Russia hoping that the White movement would prevail and Andrei's brother, Grand Duke Kirill Vladimirovich, would be installed as Tsar.
It was suggested that Grand Duke Andrei should join the White army of General Anton Denikin, but the grand duchess opposed the idea, stating that members of the Romanov family should not take part in Russia's civil war.
Against his mother's wishes, Grand Duke Boris left with his future wife, Zinaida Rashevskaya, in March 1919.
On 29 March, Admiral Edward Hobart Seymour, commander of the British fleet in the Black Sea, offered to take Grand Duke Andrei and his mother to Constantinople, but Grand Duchess Maria Pavlovna again flatly refused.
By Christmas, the Red army was to retake Kislovodsk and Grand Duke Andrei, with his mother and their entourage, decided to go to Novorossiysk, on the eastern coast of the Black Sea, where General Peter Wrangel had kept the Reds away.
One day before their departure from Kislovodsk, Von Kube, Andrei's faithful adjutant, died of typhus.
Grand Duke Andrei and his mother were the last Romanovs to leave Russia for exile.
Exile

Once in Venice, Grand Duke Andrei accompanied his mother via train to Cannes, on the French Riviera.
Grand Duchess Maria Pavlovna died a few months later in September 1920.
During her illness in Contrexéville, Grand Duke Andrei was reunited for the first time in exile with his three siblings.
At his mother's death the last obstacle for Grand Duke Andrei to marry Mathilde Kchessinska was lifted.
Andrei asked permission to marry Kchessinska from his brother Grand Duke Kirill and from Empress Maria Feodorovna, widow of Tsar Alexander III, the senior members of the Romanov family; both gave their consent.
Grand Duke Andrei also claimed paternity of Kchessinska's son, Prince Vladimir Romanovsky-Krasinsky (30 June 1902 – 23 April 1974).
In 1924, Grand Duke Andrei's eldest brother, Kirill, proclaimed himself Tsar in exile.
Grand Duke Andrei supported his brother's claim.
Grand Duke Kirill granted to Mathilde and her son the titles of Princess and Prince Romanovsky-Krasinsky, with the treatment of Serene Highness.
During their first years in exile, Grand Duke Andrei and his wife were in better economic circumstances than many of the other Romanovs.
Tsar Nicholas II made his relatives sell their properties abroad, repatriating their fortune to Russia during the war, but Grand Duke Andrei was able to keep Villa Alam in Cap-d'Ail because the property was under Mathilda's name.
To have cash flow and maintain his standard of living, Andrei sold the jewel collection that he inherited from his mother, and he mortgaged Villa Alam.
They traveled frequently to Paris, and Grand Duke Andrei was also active in philanthropic work, raising funds for Russian refugees.
In 1928, Grand Duke Andrei became one of the few members of the Romanov family to believe the claim of Anna Anderson, the best known of several impostors who claimed to be the youngest daughter of Tsar Nicholas II, Grand Duchess Anastasia.
Anderson was on the eve of her first trip to the United States when Grand Duke Andrei visited her once in January 1928.
Although he had not been particularly close to Nicholas II and his family, Grand Duke Andrei had met the real Anastasia in family events through the years and while in service as aide-de-camp to the Tsar.
Grand Duke Kirill protested his brother's support of Anderson and discouraged his intervention in the case.
In later years, Grand Duke Andrei recanted his opinion.
Grand Duke Andrei and his wife liked to gamble.
Last years

During the 1930s, Mathilde's ballet school prospered, allowing Grand Duke Andrei and his family to have a comfortable, yet modest life.
Andrei Vladimirovich also kept in touch with his Romanov relatives, particularly his brothers and many of his cousins, such as Grand Duke Dmitri Pavlovich, Grand Duchess Maria Pavlovna, Jr. and Prince Gabriel Constantinovich.
His relationship with his sister, Grand Duchess Elena Vladimirovna of Russia, became strained as she never truly accepted Mathilde as a member of the family.
At the outbreak of World War II, under the threat of a German bombing of Paris, Grand Duke Andrei and his family moved to Le Vésinet.
Following the German invasion of France, they fled by train to Grand Duke Boris's Villa in Biarritz.
Prince Vladimir Romanovsky-Krasinsky (who took a Westernized version of his mother's Polish name, Krzesińska, hyphenated with the adjective version of his father's name) was spoiled by his parents and never had an independent life.
Vladimir was arrested by the Gestapo and held in a camp for Russian emigrants in Compiègne.
Grand Duke Andrei visited German Police Headquarters multiple times and asked for help from Russian émigrés to get his son released, but neither group would help him.
Vladimir was finally freed after 119 days in detention.
During the war years the two other surviving grand dukes died; Grand Duke Dmitri Pavlovich in 1942 and Grand Duke Boris in 1943.
With the death of his brother Boris, Andrei became the last surviving Grand Duke of the Romanov dynasty who had been born in Imperial Russia.
Grand Duke Andrei's last years were marked by increasingly frail health and straitened financial circumstances.
To balance his finances, he relied partially on economic aid from his nephew, Grand Duke Vladimir Kirillovich.
In 1954, Grand Duke Andrei became a godfather of Grand Duke Vladimir's only child, Grand Duchess Maria Vladimirovna of Russia, the current claimant to the headship of the Romanov family.
Despite poor health, Grand Duke Andrei lived to be 77 years old, an age reached by few in the Romanov family.
He surpassed the longevity record held by his great-uncle, Grand Duke Michael Nikolaevich, by almost six months.
On the morning of 31 October 1956, Grand Duke Andrei worked in his study.
Prince Vladimir Romanovsky-Krasinsky died unmarried and childless in France in 1974, three years after his mother.
Portrayal

Actor Grigory Dobrygin portrayed Grand Duke Andrei Vladimirovich in Matilda, a Russian biopic from director Alexei Uchitel released in 2017.



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
  AssignClass (f45fdb47-4c6c-40c0-9428-f637e72ef152)
 Call ID: f45fdb47-4c6c-40c0-9428-f637e72ef152
  Args:
    source: Grand_Duke_Andrei_Vladimirovich
    type: :Man
  AddLiteral (f89ac3c6-6879-45a6-b51d-cd70c9b8e710)
 Call ID: f89ac3c6-6879-45a6-b51d-cd70c9b8e710
  Args:
    relation: :hasBirthYear
    source: Grand_Duke_Andrei_Vladimirovich
    literal_value: 1879
    literal_type: xsd:integer
  AddLiteral (f7ea4b2f-6aaa-4004-92d9-d4572658c2a5)
 Call ID: f7ea4b2f-6aaa-4004-92d9-d4572658c2a5
  Args:
    literal_type: xsd:integer
    source: Grand_Duke_Andrei_Vladimirovich
    literal_value: 1956
    relation: :hasDeathYear
  AssignClass (8a374ca2-b324-4cd3-9a63-4621e5c899c4)
 Call ID: 8a374ca2-b324-4cd3-9a63-4621e5c899c4
  Args:
    type: :Man
    source: Grand_Duke_Vladimir_Alexandrovich
  AddTriple (9677e7be-e1fd-4a24-a4e6-a4a854298819)
 Call ID: 9677e7be-e1fd-4a24-a4e6-a4a854298819
  Args:
    source: Grand_Duke_Andrei_Vladimirovich
    relation: :hasFather
    target: Grand_Duke_Vladimir_Alexandrovich
  AssignClass (d5b53260-4bee-4a40-9789-479c25b772c6)
 Call ID: d5b53260-4bee-4a40-9789-479c25b772c6
  Args:
    source: Grand_Duchess_Maria_Pavlovna
    type: :Woman
  AddTriple (dc78bb35-4909-4e8d-ae27-846ef37508d9)
 Call ID: dc78bb35-4909-4e8d-ae27-846ef37508d9
  Args:
    source: Grand_Duke_Andrei_Vladimirovich
    relation: :hasMother
    target: Grand_Duchess_Maria_Pavlovna
  AssignClass (06209fbe-8be0-40a7-9384-c964062903ee)
 Call ID: 06209fbe-8be0-40a7-9384-c964062903ee
  Args:
    source: Grand_Duke_Kirill_Vladimirovich
    type: :Man
  AddTriple (ccadd27e-d8c6-478d-b016-e6c8d2b5ba4d)
 Call ID: ccadd27e-d8c6-478d-b016-e6c8d2b5ba4d
  Args:
    source: Grand_Duke_Andrei_Vladimirovich
    relation: :isBrotherOf
    target: Grand_Duke_Kirill_Vladimirovich
  AssignClass (fc922380-2a61-4aa5-9571-f1d6220c607f)
 Call ID: fc922380-2a61-4aa5-9571-f1d6220c607f
  Args:
    type: :Man
    source: Grand_Duke_Boris_Vladimirovich
  AddTriple (dbd86e01-7310-469a-a4f9-03bfdd44a6b0)
 Call ID: dbd86e01-7310-469a-a4f9-03bfdd44a6b0
  Args:
    source: Grand_Duke_Andrei_Vladimirovich
    relation: :isBrotherOf
    target: Grand_Duke_Boris_Vladimirovich
  AssignClass (aad85167-98cc-4b1e-a15f-217dd945e090)
 Call ID: aad85167-98cc-4b1e-a15f-217dd945e090
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna
  AddTriple (ff5885b6-ff7e-4768-98f4-4409b86ec892)
 Call ID: ff5885b6-ff7e-4768-98f4-4409b86ec892
  Args:
    relation: :isSisterOf
    target: Grand_Duchess_Elena_Vladimirovna
    source: Grand_Duke_Andrei_Vladimirovich
  AssignClass (8b2a6464-8e8f-4c2d-a208-a89cd1b085e5)
 Call ID: 8b2a6464-8e8f-4c2d-a208-a89cd1b085e5
  Args:
    source: Mathilde_Kschessinska
    type: :Woman
  AddLiteral (995c714a-5f45-4399-a18e-a208e2e43fde)
 Call ID: 995c714a-5f45-4399-a18e-a208e2e43fde
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1921
    source: Grand_Duke_Andrei_Vladimirovich
  AddTriple (6f96a098-a040-46ab-af67-6313925cb197)
 Call ID: 6f96a098-a040-46ab-af67-6313925cb197
  Args:
    relation: :hasRelation
    target: Mathilde_Kschessinska
    source: Grand_Duke_Andrei_Vladimirovich
  AssignClass (05d1938c-7412-4810-b13c-19b97e424853)
 Call ID: 05d1938c-7412-4810-b13c-19b97e424853
  Args:
    source: Prince_Vladimir_Romanovsky-Krasinsky
    type: :Man
  AddTriple (238f923e-8b99-4644-ab2e-b0eab18bbf92)
 Call ID: 238f923e-8b99-4644-ab2e-b0eab18bbf92
  Args:
    target: Grand_Duke_Andrei_Vladimirovich
    relation: :isSonOf
    source: Prince_Vladimir_Romanovsky-Krasinsky
  AddTriple (4fabe7ae-3975-4dff-8735-4b29dcc05640)
 Call ID: 4fabe7ae-3975-4dff-8735-4b29dcc05640
  Args:
    relation: :isSonOf
    target: Mathilde_Kschessinska
    source: Prince_Vladimir_Romanovsky-Krasinsky
  Finish (6955421c-fb11-4e5e-a4d5-2069923d7211)
 Call ID: 6955421c-fb11-4e5e-a4d5-2069923d7211
  Args: