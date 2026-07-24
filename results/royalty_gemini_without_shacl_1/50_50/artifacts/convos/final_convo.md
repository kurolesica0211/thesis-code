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
Alexander (Greek: Αλέξανδρος, romanized: Aléxandros; 1 August 1893 – 25 October 1920) was King of Greece from 11 June 1917 until his death on 25 October 1920.
The second son of King Constantine I, Alexander was born in the summer palace of Tatoi on the outskirts of Athens.
He succeeded his father in 1917, during World War I, after the Entente Powers and the followers of Eleftherios Venizelos pushed King Constantine and his eldest son, Crown Prince George, into exile.
Under his reign, the territorial extent of Greece considerably increased, following the victory of the Entente and their Allies in the First World War and the early stages of the Greco-Turkish War of 1919–1922.
Alexander controversially married the commoner Aspasia Manos in 1919, provoking a major scandal that forced the couple to leave Greece for several months.
Soon after returning to Greece with his wife, Alexander was bitten by a domestic Barbary macaque and died aged 27 of sepsis.
After a general election and a referendum, Constantine I was restored to the throne.
Early life

Alexander was born at Tatoi Palace on 1 August 1893 (20 July in the Julian calendar), the second son of Crown Prince Constantine of Greece and Princess Sophia of Prussia.
His father was the eldest son of King George I of Greece by his wife, Olga Constantinovna of Russia; his mother was the daughter of Frederick III, German Emperor, and Victoria, Princess Royal of the United Kingdom.
His parents' cousins included King George V of the United Kingdom and Emperor Nicholas II of Russia.
Wilhelm II, German Emperor, was his maternal uncle.
Alexander's early life alternated between the Royal Palace in Athens, and Tatoi Palace in the city's suburbs.
Though he was very close to his younger sister Helen, Alexander was less warm towards his elder brother, George, with whom he had little in common.
While George was a serious and thoughtful child, Alexander was mischievous and extroverted; he smoked cigarettes made from blotting paper, set fire to the games room in the palace, and recklessly lost control of a toy cart in which he and his younger brother Paul were rolling down a hill, tipping his toddler brother a distance of 6 ft (1.8 m) into brambles.
His education was expensive and carefully planned, but while George spent part of his military training in Germany, Alexander was educated in Greece.
King George I was assassinated in Thessaloniki soon afterwards on 18 March 1913, and Alexander's father ascended the throne as Constantine I.


Courtship of Aspasia Manos

In 1915, at a party held in Athens by court marshal Theodore Ypsilantis, Alexander became re-acquainted with one of his childhood friends, Aspasia Manos.
She was the daughter of Constantine's Master of the Horse, Colonel Petros Manos, and his wife Maria Argyropoulos.
Initially, Aspasia was resistant to his charm; although considered very handsome by his contemporaries, Alexander had a reputation as a ladies' man from numerous past liaisons.
However, for King Constantine I, Queen Sophia and much of European society of the time, it was inconceivable for a royal prince to marry someone of a different social rank.
World War I

During World War I, Constantine I followed a formal policy of neutrality, yet he was openly benevolent towards Germany, which was fighting alongside Austria-Hungary, Bulgaria and the Ottoman Empire against the Triple Entente of Russia, France and Britain.
Constantine was the brother-in-law of Kaiser Wilhelm II, and had also become something of a Germanophile following his military training in Prussia.
His pro-German attitude provoked a split between the monarch and the prime minister, Eleftherios Venizelos, who wanted to support the Entente in the hope of expanding Greek territory to incorporate the Greek minorities in the Ottoman Empire and the Balkans.
Parts of Greece were occupied by the Allied Entente forces, but Constantine I refused to modify his policy and faced increasingly open opposition from the Entente and the Venizelists.
In July 1916, an arson attack ravaged Tatoi Palace and the royal family barely escaped the flames; Alexander was not injured but his mother narrowly saved Princess Katherine by carrying her through the woods for more than 2 km (1.2 mi).
Finally on 10 June 1917, Charles Jonnart, the Entente's High Commissioner in Greece, ordered King Constantine to give up his power.
The Allies, while determined to be rid of Constantine, did not wish to create a Greek republic, and sought to replace the king with another member of the royal family.
Crown Prince George, who was the natural heir, was ruled out by the Allies because they thought him too pro-German, like his father.
Instead, they considered installing Constantine's brother (and Alexander's uncle), Prince George, but he had tired of public life during his difficult tenure as High Commissioner of Crete between 1901 and 1905; above all, he sought to remain loyal to his brother, and categorically refused to take the throne.
As a result, Constantine's second son, Prince Alexander, was chosen to become the new monarch.
Reign

Accession

The dismissal of Constantine was not unanimously supported by the Entente powers; while France and Britain did nothing to stop Jonnart's actions, the Russian provisional government officially protested to Paris.
Russia's protests were brushed aside, and Alexander ascended the Greek throne.
Alexander swore the oath of loyalty to the Greek constitution on the afternoon of 11 June 1917 in the ballroom of the Royal Palace.
Apart from the Archbishop of Athens, Theocletus I, who administered the oath, only King Constantine I, Crown Prince George and the king's prime minister, Alexandros Zaimis, attended.
Constantine had informed his son that he should consider himself a regent, rather than a true monarch.
In the evening, after the ceremony, the royal family decided to leave their palace in Athens for Tatoi, but city residents opposed the exile of their sovereign and crowds formed outside the palace to prevent Constantine and his family from leaving.
At Tatoi, Constantine again impressed upon Alexander that he held the crown in trust only.
The next day, Constantine, Sophia and all of their children except Alexander arrived at the small port of Oropos and set off into exile.
Eventually, they all followed Constantine into exile.
Royal household staff were gradually replaced by enemies of the former king, and Alexander's allies were either imprisoned or distanced from him.
Portraits of the royal family were removed from public buildings, and Alexander's new ministers openly called him the "son of a traitor".
Despite promises given by the Entente on Constantine's departure, the previous prime minister, Zaimis, was effectively forced to resign as Venizelos returned to Athens.
Greek expansion

By the end of World War I, Greece had grown beyond its 1914 borders, and the treaties of Neuilly (1919) and Sèvres (1920) confirmed the Greek territorial conquests.
The majority of Thrace (previously split between Bulgaria and Turkey) and several Aegean Islands (such as Imbros and Tenedos) became part of Greece, and the region of Smyrna, in Ionia, was placed under Greek mandate.
Upon his return to Greece in August 1920, Venizelos received a laurel crown from the king for his work in support of panhellenism.
Marriage

Controversy

On 12 June 1917, the day after his accession, Alexander revealed his liaison with Aspasia Manos to his father and asked for his permission to marry her.
Constantine was reluctant to let his son marry a non-royal, and demanded that Alexander wait until the end of the war before considering the engagement, to which Alexander agreed.
Alexander's only source of comfort was Aspasia, and he decided to marry her despite his father's request.
The ruling dynasty of Greece (the House of Glücksburg) was of German-Danish origin, and Constantine and Sophia were seen as far too German by the Venizelists, but even though the marriage of the king to a Greek presented an opportunity to Hellenize the royal family, and counter criticisms that it was a foreign institution, both Venizelists and Constantinists opposed the match.
The Venizelists feared it would give Alexander a means to communicate with his exiled family through Colonel Manos and both sides of the political divide were unhappy at the king marrying a commoner.
Although Venizelos was a friend of Petros Manos, the prime minister warned the king that marrying her would be unpopular in the eyes of the people.
When Prince Arthur, Duke of Connaught and Strathearn, visited Athens in March 1918, to confer the Order of the Bath upon the king, Alexander feared that a marriage between him and Princess Mary of the United Kingdom would be discussed as part of an attempt to consolidate the relationship between Greece and Britain.
To Alexander's relief, Arthur asked to meet Aspasia, and declared that, if he were younger, he would have sought to marry her himself.
The British authorities feared that Alexander would abdicate in order to marry Aspasia if the wedding was blocked, and they wanted to avoid Greece becoming a republic in case it led to instability or an increase in French influence at their expense.
Sophia disapproved of her son marrying a commoner, while Constantine wanted a delay but was prepared to be his son's best man if Alexander would be patient.
Alexander visited Paris at the end of 1918, raising hopes among his family that they would be able to contact him once he was outside Greece.
When Queen Sophia attempted to telephone her son in his Parisian hotel, a minister intercepted the call and informed her that "His Majesty is sorry, but he cannot respond to the telephone".
Public scandal

With the help of Aspasia's brother-in-law, Christo Zalocostas, and after three unsuccessful attempts, the couple eventually married in secret before a royal chaplain, Archimandrite Zacharistas, on the evening of 17 November 1919.
According to the Greek constitution, members of the royal family had to obtain permission to marry from both the sovereign and the head of the Greek Orthodox Church.
By marrying Aspasia without the permission of the Archbishop, Alexander caused a major scandal.
Despite his disapproval of the union, Venizelos allowed Aspasia and her mother to move into the Royal Palace on condition that the marriage remain secret.
The information leaked, however, and to escape public opprobrium Aspasia was forced to leave Greece.
The king drove the injured to hospital in his own car, while Aspasia, who had trained as a nurse during World War I, rendered first aid.
The government allowed the couple to return to Greece in mid-1920.
Although their marriage was legalized, Aspasia was not recognized as queen, but was instead known as "Madame Manos".
A domestic Barbary macaque belonging to the steward of the palace's grapevines attacked or was attacked by the king's German Shepherd dog, Fritz, and Alexander attempted to separate the two animals.
Finally, the queen dowager, Olga, George I's widow and Alexander's grandmother, was allowed to return alone to Athens to tend to the king.
The other members of the royal family received the news by telegram that night.
Once again, the royal family were refused permission to return to Greece, and Queen Olga was the only member who attended.
Foreign powers were represented by the Prince Regent of Serbia with his sister Princess Helen wife of John Constantinovich of Russia, the Crown Prince of Sweden with his uncle Prince Eugene, Duke of Nericia, and Rear-Admirals Sir George Hope of the United Kingdom and Dumesnil of France, as well as members of the Athens diplomatic corps.
After the cathedral service, Alexander's body was interred on the grounds of the royal estate at Tatoi.
The Greek royal family never regarded Alexander's reign as fully legitimate.
In the royal cemetery, while other monarchs are given the inscription "King of the Hellenes, Prince of Denmark", Alexander's reads "Alexander, son of the King of the Hellenes, Prince of Denmark.
According to Alexander's favorite sister, Queen Helen of Romania, this feeling of illegitimacy was also shared by Alexander himself, a sentiment that helps explain his mésalliance with Aspasia Manos.
The Hellenic Parliament demanded that Constantine I and Crown Prince George be excluded from the succession but sought to preserve the monarchy by selecting another member of the royal house as the new sovereign.
On 29 October 1920, the Greek minister in Berne, acting under the direction of the Greek authorities, offered the throne to Alexander's younger brother, Prince Paul.
Paul, however, refused to become king while his father and elder brother were alive, insisting that neither of them had renounced their rights to the throne and that he therefore could never legitimately wear the crown.
The throne remained vacant and the legislative elections of 1920 turned into an open conflict between the Venizelists, who favored republicanism, and the supporters of the ex-King Constantine.
On 14 November 1920, with the war with Turkey dragging on, the monarchists won, and Dimitrios Rallis became prime minister; Venizelos (who lost his own parliamentary seat) chose to leave Greece in self-exile.
Rallis asked Queen Olga to become regent until Constantine's return.
Under the restored King Constantine I, whose return was endorsed overwhelmingly in a referendum, Greece went on to lose the Greco–Turkish War with heavy military and civilian casualties.
Alexander's death in the midst of an election campaign helped destabilize the Venizelos regime, and the resultant loss of Allied support contributed to the failure of Greece's territorial ambitions.
"


Issue

Alexander's daughter by Aspasia Manos, Alexandra (1921–1993), was born five months after his death.
Initially, the government took the line that since Alexander had married Aspasia without the permission of his father or the church, his marriage was illegal and his posthumous daughter was illegitimate.
However, in July 1922, Parliament passed a law which allowed the King to recognize royal marriages retroactively on a non-dynastic basis.
That September, Constantine—at Sophia's insistence—recognized his son's marriage to Aspasia and granted her the style of "Princess Alexander".
Her daughter (Constantine I's granddaughter) was legitimized as a princess of Greece and Denmark, and later married King Peter II of Yugoslavia in London in 1944.
Alexander, Crown Prince of Yugoslavia.



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
  AssignClass (354761cd-ffb8-4ed5-980c-e144a9988bcf)
 Call ID: 354761cd-ffb8-4ed5-980c-e144a9988bcf
  Args:
    source: :Alexander
    type: :Man
  AssignClass (eab5ac17-cc6d-4a9e-9f31-d97c84635ecc)
 Call ID: eab5ac17-cc6d-4a9e-9f31-d97c84635ecc
  Args:
    source: :Alexander
    type: :Person
  AddLiteral (278e446b-bbcf-458f-b238-88226cc8324c)
 Call ID: 278e446b-bbcf-458f-b238-88226cc8324c
  Args:
    source: :Alexander
    literal_value: 1893
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (ad45da4f-8f40-4eac-8f26-8f97c966b1e9)
 Call ID: ad45da4f-8f40-4eac-8f26-8f97c966b1e9
  Args:
    relation: :hasDeathYear
    literal_value: 1920
    literal_type: xsd:integer
    source: :Alexander
  AssignClass (342763a6-6c99-4f23-929f-104dbe0d05b3)
 Call ID: 342763a6-6c99-4f23-929f-104dbe0d05b3
  Args:
    source: :ConstantineI
    type: :Man
  AssignClass (3aa23d00-6131-4c03-a872-f3c99ca3838e)
 Call ID: 3aa23d00-6131-4c03-a872-f3c99ca3838e
  Args:
    type: :Person
    source: :ConstantineI
  AssignClass (e931e645-bba7-4cd6-9bf2-9de30316e10e)
 Call ID: e931e645-bba7-4cd6-9bf2-9de30316e10e
  Args:
    source: :Sophia
    type: :Woman
  AssignClass (4b1b784f-195a-401c-821a-b18237df7df4)
 Call ID: 4b1b784f-195a-401c-821a-b18237df7df4
  Args:
    source: :Sophia
    type: :Person
  AddTriple (ec0698ac-de5d-4c7e-b4bb-58f4387b1ccc)
 Call ID: ec0698ac-de5d-4c7e-b4bb-58f4387b1ccc
  Args:
    source: :Alexander
    target: :ConstantineI
    relation: :hasFather
  AddTriple (12d77951-f1af-4992-9f6e-eb9f8e799b56)
 Call ID: 12d77951-f1af-4992-9f6e-eb9f8e799b56
  Args:
    relation: :hasMother
    source: :Alexander
    target: :Sophia
  AssignClass (a8204e3b-e6df-461e-a524-8bac45d05095)
 Call ID: a8204e3b-e6df-461e-a524-8bac45d05095
  Args:
    type: :Man
    source: :GeorgeI
  AssignClass (e4216be2-52ac-4ffa-8c73-18ca8d6a8115)
 Call ID: e4216be2-52ac-4ffa-8c73-18ca8d6a8115
  Args:
    source: :GeorgeI
    type: :Person
  AssignClass (772eac98-3b4a-4120-817f-3c777d362922)
 Call ID: 772eac98-3b4a-4120-817f-3c777d362922
  Args:
    type: :Woman
    source: :OlgaConstantinovna
  AssignClass (931eca64-a6e5-47ac-8362-dd60f59ef05c)
 Call ID: 931eca64-a6e5-47ac-8362-dd60f59ef05c
  Args:
    type: :Person
    source: :OlgaConstantinovna
  AddTriple (ab10a05a-67b8-4bf7-82f8-d90c3a5e93d1)
 Call ID: ab10a05a-67b8-4bf7-82f8-d90c3a5e93d1
  Args:
    relation: :hasFather
    source: :ConstantineI
    target: :GeorgeI
  AddTriple (3fbd1edc-d684-4da6-b795-cebb0d55d706)
 Call ID: 3fbd1edc-d684-4da6-b795-cebb0d55d706
  Args:
    source: :ConstantineI
    target: :OlgaConstantinovna
    relation: :hasMother
  AssignClass (7df85ba8-b892-4987-9d97-8df984942fc1)
 Call ID: 7df85ba8-b892-4987-9d97-8df984942fc1
  Args:
    type: :Man
    source: :FrederickIII
  AssignClass (748e927c-9376-4d79-8a59-b408fef2b2f0)
 Call ID: 748e927c-9376-4d79-8a59-b408fef2b2f0
  Args:
    type: :Person
    source: :FrederickIII
  AssignClass (fd56452b-58e4-48fd-9513-a9020351d71b)
 Call ID: fd56452b-58e4-48fd-9513-a9020351d71b
  Args:
    type: :Woman
    source: :VictoriaPrincessRoyal
  AssignClass (c5cfe703-1f70-4398-bb72-6060bf75d484)
 Call ID: c5cfe703-1f70-4398-bb72-6060bf75d484
  Args:
    source: :VictoriaPrincessRoyal
    type: :Person
  AddTriple (9b8aec52-b479-4705-afd8-eaf1b14174e1)
 Call ID: 9b8aec52-b479-4705-afd8-eaf1b14174e1
  Args:
    target: :FrederickIII
    source: :Sophia
    relation: :hasFather
  AddTriple (f5eea74d-eea8-4d67-934b-771c74b916dd)
 Call ID: f5eea74d-eea8-4d67-934b-771c74b916dd
  Args:
    source: :Sophia
    target: :VictoriaPrincessRoyal
    relation: :hasMother
  AssignClass (b0b5e856-3149-49d3-a5b4-cc09a3aac19f)
 Call ID: b0b5e856-3149-49d3-a5b4-cc09a3aac19f
  Args:
    type: :Woman
    source: :Helen
  AssignClass (d4645307-8d26-4a74-80d2-8372be3300a1)
 Call ID: d4645307-8d26-4a74-80d2-8372be3300a1
  Args:
    type: :Person
    source: :Helen
  AssignClass (90b18142-a837-495a-a968-74326990fe62)
 Call ID: 90b18142-a837-495a-a968-74326990fe62
  Args:
    type: :Man
    source: :George
  AssignClass (05b9f705-8728-462a-baae-c628c27849d5)
 Call ID: 05b9f705-8728-462a-baae-c628c27849d5
  Args:
    source: :George
    type: :Person
  AssignClass (abe010a4-5031-4363-967f-aec9be27977d)
 Call ID: abe010a4-5031-4363-967f-aec9be27977d
  Args:
    type: :Man
    source: :Paul
  AssignClass (28a8de90-84b8-4efd-9174-82dea1cc63b9)
 Call ID: 28a8de90-84b8-4efd-9174-82dea1cc63b9
  Args:
    type: :Person
    source: :Paul
  AddTriple (119c998c-52fc-4553-a7ca-df7a327cefd8)
 Call ID: 119c998c-52fc-4553-a7ca-df7a327cefd8
  Args:
    target: :Helen
    source: :Alexander
    relation: :isSiblingOf
  AddTriple (ffbeff17-602b-4e3c-a27f-9e37046932dd)
 Call ID: ffbeff17-602b-4e3c-a27f-9e37046932dd
  Args:
    target: :George
    source: :Alexander
    relation: :isSiblingOf
  AddTriple (89c0effb-d386-4f91-a9bc-44d1b659465f)
 Call ID: 89c0effb-d386-4f91-a9bc-44d1b659465f
  Args:
    target: :Paul
    source: :Alexander
    relation: :isSiblingOf
  AssignClass (0eaced42-5405-470c-8457-85c58f0af494)
 Call ID: 0eaced42-5405-470c-8457-85c58f0af494
  Args:
    source: :AspasiaManos
    type: :Woman
  AssignClass (b14dbcc9-a762-4d44-ba62-3bf947310f65)
 Call ID: b14dbcc9-a762-4d44-ba62-3bf947310f65
  Args:
    type: :Person
    source: :AspasiaManos
  AddTriple (d17ed05a-8c85-46a7-ad01-0612b5c2f747)
 Call ID: d17ed05a-8c85-46a7-ad01-0612b5c2f747
  Args:
    relation: :hasRelation
    source: :Alexander
    target: :AspasiaManos
  AddLiteral (bcc0361e-efe0-4d61-9a6d-2e07a2801da5)
 Call ID: bcc0361e-efe0-4d61-9a6d-2e07a2801da5
  Args:
    relation: :hasMarriageYear
    literal_value: 1919
    literal_type: xsd:integer
    source: :Alexander
  AssignClass (dacfb6a1-8398-4658-9ba4-56853995e829)
 Call ID: dacfb6a1-8398-4658-9ba4-56853995e829
  Args:
    type: :Man
    source: :PetrosManos
  AssignClass (8e03aa64-6634-4ece-b6e8-d7d40a8735ba)
 Call ID: 8e03aa64-6634-4ece-b6e8-d7d40a8735ba
  Args:
    type: :Person
    source: :PetrosManos
  AssignClass (f143a957-76e2-4649-ab3b-d927552e09f2)
 Call ID: f143a957-76e2-4649-ab3b-d927552e09f2
  Args:
    type: :Woman
    source: :MariaArgyropoulos
  AssignClass (0f2fbb5d-a594-4f5f-a5a8-6a2a68ba0e67)
 Call ID: 0f2fbb5d-a594-4f5f-a5a8-6a2a68ba0e67
  Args:
    source: :MariaArgyropoulos
    type: :Person
  AddTriple (4dcb7323-edae-4f6a-a87b-a114aa80ca42)
 Call ID: 4dcb7323-edae-4f6a-a87b-a114aa80ca42
  Args:
    target: :PetrosManos
    source: :AspasiaManos
    relation: :hasFather
  AddTriple (685f6e76-8a22-4520-8b59-e7bb9a422d29)
 Call ID: 685f6e76-8a22-4520-8b59-e7bb9a422d29
  Args:
    relation: :hasMother
    source: :AspasiaManos
    target: :MariaArgyropoulos
  AssignClass (b40476c6-f9f9-424d-96b1-86e87e0887c2)
 Call ID: b40476c6-f9f9-424d-96b1-86e87e0887c2
  Args:
    type: :Woman
    source: :Alexandra
  AssignClass (a2b8a7d8-0e81-4304-8899-f86598f94240)
 Call ID: a2b8a7d8-0e81-4304-8899-f86598f94240
  Args:
    type: :Person
    source: :Alexandra
  AddTriple (e7c14e0a-c715-4e86-9600-7459e9768dc8)
 Call ID: e7c14e0a-c715-4e86-9600-7459e9768dc8
  Args:
    relation: :hasFather
    source: :Alexandra
    target: :Alexander
  AddTriple (f7d27cab-6d51-4a3d-b6b6-4b605487dbef)
 Call ID: f7d27cab-6d51-4a3d-b6b6-4b605487dbef
  Args:
    source: :Alexandra
    target: :AspasiaManos
    relation: :hasMother
  AssignClass (dd233aaf-9609-4051-b1fd-6bcf46e40565)
 Call ID: dd233aaf-9609-4051-b1fd-6bcf46e40565
  Args:
    type: :Woman
    source: :Katherine
  AssignClass (a739279f-b6ed-4234-b60b-c7c4ed630a5d)
 Call ID: a739279f-b6ed-4234-b60b-c7c4ed630a5d
  Args:
    type: :Person
    source: :Katherine
  AddTriple (97be0ef6-3935-4d63-aa43-81650c3512c4)
 Call ID: 97be0ef6-3935-4d63-aa43-81650c3512c4
  Args:
    source: :Katherine
    target: :Sophia
    relation: :hasMother
  Finish (376718d4-83f2-4eb9-a8aa-0fd4f3c1f93c)
 Call ID: 376718d4-83f2-4eb9-a8aa-0fd4f3c1f93c
  Args: