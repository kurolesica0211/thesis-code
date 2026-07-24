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
  AssignClass (cad86104-1f88-4429-a73d-6dc053aa2c8b)
 Call ID: cad86104-1f88-4429-a73d-6dc053aa2c8b
  Args:
    type: :Man
    source: Alexander
  AssignClass (44611e12-c38d-4595-9b8c-30054557b318)
 Call ID: 44611e12-c38d-4595-9b8c-30054557b318
  Args:
    type: :Person
    source: Alexander
  AddLiteral (de3e8a6f-7440-4a5d-9c67-8e8d9769e31f)
 Call ID: de3e8a6f-7440-4a5d-9c67-8e8d9769e31f
  Args:
    source: Alexander
    literal_type: xsd:integer
    literal_value: 1893
    relation: :hasBirthYear
  AddLiteral (b51f536a-c3ae-41bc-ab25-f9fa2fb5367a)
 Call ID: b51f536a-c3ae-41bc-ab25-f9fa2fb5367a
  Args:
    source: Alexander
    literal_type: xsd:integer
    literal_value: 1920
    relation: :hasDeathYear
  AssignClass (200172a3-0c09-459e-a422-608b1fd3d6dd)
 Call ID: 200172a3-0c09-459e-a422-608b1fd3d6dd
  Args:
    type: :Man
    source: Constantine_I
  AssignClass (67de187c-69b0-4dad-a565-bf6276dd2998)
 Call ID: 67de187c-69b0-4dad-a565-bf6276dd2998
  Args:
    type: :Person
    source: Constantine_I
  AssignClass (c192322a-6771-469b-b6c2-c62e19d38482)
 Call ID: c192322a-6771-469b-b6c2-c62e19d38482
  Args:
    type: :Woman
    source: Sophia_of_Prussia
  AssignClass (871db826-fc8d-4580-aa31-ac14c8a71966)
 Call ID: 871db826-fc8d-4580-aa31-ac14c8a71966
  Args:
    type: :Person
    source: Sophia_of_Prussia
  AddTriple (6da7122a-255f-45f0-b807-8aed08d23c18)
 Call ID: 6da7122a-255f-45f0-b807-8aed08d23c18
  Args:
    target: Constantine_I
    relation: :hasFather
    source: Alexander
  AddTriple (77b1b395-77ef-40cf-ad9a-e6290a865b20)
 Call ID: 77b1b395-77ef-40cf-ad9a-e6290a865b20
  Args:
    source: Alexander
    target: Sophia_of_Prussia
    relation: :hasMother
  AssignClass (82dc2e5e-2bdb-4cee-be3f-d2ca3750e395)
 Call ID: 82dc2e5e-2bdb-4cee-be3f-d2ca3750e395
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (0fd7a435-11fb-412e-9574-0eaafb4a53f9)
 Call ID: 0fd7a435-11fb-412e-9574-0eaafb4a53f9
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (35196ebc-552a-41e3-9f10-1497920907df)
 Call ID: 35196ebc-552a-41e3-9f10-1497920907df
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (288630c1-8313-48ab-bbdc-344c58cdd873)
 Call ID: 288630c1-8313-48ab-bbdc-344c58cdd873
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AddTriple (1fb0a326-06f0-4cbd-9c23-cbcd0d891b71)
 Call ID: 1fb0a326-06f0-4cbd-9c23-cbcd0d891b71
  Args:
    relation: :hasFather
    target: George_I_of_Greece
    source: Constantine_I
  AddTriple (80cf35c9-3dc6-4680-ba9c-1c6b48ddb3b9)
 Call ID: 80cf35c9-3dc6-4680-ba9c-1c6b48ddb3b9
  Args:
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
    source: Constantine_I
  AssignClass (e4e58114-b8b1-4b2b-aa72-6aefd07b5c1f)
 Call ID: e4e58114-b8b1-4b2b-aa72-6aefd07b5c1f
  Args:
    type: :Man
    source: Frederick_III_German_Emperor
  AssignClass (c31fe2ba-7455-4c35-ac0e-3c666c083097)
 Call ID: c31fe2ba-7455-4c35-ac0e-3c666c083097
  Args:
    type: :Person
    source: Frederick_III_German_Emperor
  AssignClass (d77badfe-a010-474f-ac23-2d1bced22903)
 Call ID: d77badfe-a010-474f-ac23-2d1bced22903
  Args:
    type: :Woman
    source: Victoria_Princess_Royal
  AssignClass (25bbf434-79fc-4ade-955c-400738b79c0a)
 Call ID: 25bbf434-79fc-4ade-955c-400738b79c0a
  Args:
    type: :Person
    source: Victoria_Princess_Royal
  AddTriple (83236362-fa3a-4ce1-bb5e-7fb4823b2f8b)
 Call ID: 83236362-fa3a-4ce1-bb5e-7fb4823b2f8b
  Args:
    source: Sophia_of_Prussia
    target: Frederick_III_German_Emperor
    relation: :hasFather
  AddTriple (6125b77f-40e5-4273-9eec-c635d20a7c60)
 Call ID: 6125b77f-40e5-4273-9eec-c635d20a7c60
  Args:
    target: Victoria_Princess_Royal
    relation: :hasMother
    source: Sophia_of_Prussia
  AssignClass (6cfc16d3-dbc9-44d4-a094-f6e395a4620a)
 Call ID: 6cfc16d3-dbc9-44d4-a094-f6e395a4620a
  Args:
    type: :Woman
    source: Helen_of_Romania
  AssignClass (21d8ac00-50a5-4192-a107-9012a82a7961)
 Call ID: 21d8ac00-50a5-4192-a107-9012a82a7961
  Args:
    type: :Person
    source: Helen_of_Romania
  AddTriple (e1b0f432-865d-4467-8871-e63949a29fb3)
 Call ID: e1b0f432-865d-4467-8871-e63949a29fb3
  Args:
    relation: :isSiblingOf
    target: Helen_of_Romania
    source: Alexander
  AssignClass (3d647cd3-f7a5-415d-a567-d60ffd47cf39)
 Call ID: 3d647cd3-f7a5-415d-a567-d60ffd47cf39
  Args:
    type: :Man
    source: George_Crown_Prince
  AssignClass (4d77fc38-0a24-4d4a-ae61-6a8f07a49e94)
 Call ID: 4d77fc38-0a24-4d4a-ae61-6a8f07a49e94
  Args:
    type: :Person
    source: George_Crown_Prince
  AddTriple (49eccc10-0043-4958-8a95-6c7ea75a7c62)
 Call ID: 49eccc10-0043-4958-8a95-6c7ea75a7c62
  Args:
    source: Alexander
    relation: :isSiblingOf
    target: George_Crown_Prince
  AssignClass (0e75fbe5-84d0-433a-b24a-34fe4db6d10a)
 Call ID: 0e75fbe5-84d0-433a-b24a-34fe4db6d10a
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (ac62ce2c-f237-4dd1-92e7-219c42821f09)
 Call ID: ac62ce2c-f237-4dd1-92e7-219c42821f09
  Args:
    type: :Person
    source: Paul_of_Greece
  AddTriple (ef4e73d3-8d43-448a-b3e7-941135a947d8)
 Call ID: ef4e73d3-8d43-448a-b3e7-941135a947d8
  Args:
    source: Alexander
    relation: :isSiblingOf
    target: Paul_of_Greece
  AssignClass (3b220be6-0fc2-4204-a3c4-9ea2cfb4ef61)
 Call ID: 3b220be6-0fc2-4204-a3c4-9ea2cfb4ef61
  Args:
    type: :Woman
    source: Aspasia_Manos
  AssignClass (a2e931d5-0320-4485-af56-7763db384e82)
 Call ID: a2e931d5-0320-4485-af56-7763db384e82
  Args:
    type: :Person
    source: Aspasia_Manos
  AddLiteral (8a767296-04ef-4abc-ae42-36cabf82a33e)
 Call ID: 8a767296-04ef-4abc-ae42-36cabf82a33e
  Args:
    source: Alexander
    literal_type: xsd:integer
    literal_value: 1919
    relation: :hasMarriageYear
  AddTriple (e1cdefde-ed41-4dbb-8efa-1abccd905693)
 Call ID: e1cdefde-ed41-4dbb-8efa-1abccd905693
  Args:
    source: Alexander
    target: Aspasia_Manos
    relation: :hasRelation
  AssignClass (111d519b-c076-41de-b1b4-968b004f311d)
 Call ID: 111d519b-c076-41de-b1b4-968b004f311d
  Args:
    type: :Man
    source: Petros_Manos
  AssignClass (32fdf18f-c493-4f03-a818-2aa357c356bb)
 Call ID: 32fdf18f-c493-4f03-a818-2aa357c356bb
  Args:
    type: :Person
    source: Petros_Manos
  AssignClass (ab2eec8f-d47c-4d66-a758-ec35681d3a6f)
 Call ID: ab2eec8f-d47c-4d66-a758-ec35681d3a6f
  Args:
    type: :Woman
    source: Maria_Argyropoulos
  AssignClass (0943d19c-830e-4929-90ec-16b44a6f81ff)
 Call ID: 0943d19c-830e-4929-90ec-16b44a6f81ff
  Args:
    type: :Person
    source: Maria_Argyropoulos
  AddTriple (61d70522-4ebf-4f0d-8428-5ca9b853e88d)
 Call ID: 61d70522-4ebf-4f0d-8428-5ca9b853e88d
  Args:
    relation: :hasFather
    target: Petros_Manos
    source: Aspasia_Manos
  AddTriple (92fefde5-3709-40ab-8c2f-134e87ccaa42)
 Call ID: 92fefde5-3709-40ab-8c2f-134e87ccaa42
  Args:
    target: Maria_Argyropoulos
    relation: :hasMother
    source: Aspasia_Manos
  AssignClass (7845dcc3-efb8-4feb-9d20-a6430755e104)
 Call ID: 7845dcc3-efb8-4feb-9d20-a6430755e104
  Args:
    type: :Woman
    source: Alexandra_of_Greece
  AssignClass (27fd8cc4-9b51-480c-ae2d-4e2ce6e59327)
 Call ID: 27fd8cc4-9b51-480c-ae2d-4e2ce6e59327
  Args:
    type: :Person
    source: Alexandra_of_Greece
  AddTriple (70bdc080-c5d0-4ce0-b6dc-82d3acd667d5)
 Call ID: 70bdc080-c5d0-4ce0-b6dc-82d3acd667d5
  Args:
    source: Alexandra_of_Greece
    relation: :hasFather
    target: Alexander
  AddTriple (db38195c-5be3-4d37-a56d-517ff9a155ee)
 Call ID: db38195c-5be3-4d37-a56d-517ff9a155ee
  Args:
    relation: :hasMother
    target: Aspasia_Manos
    source: Alexandra_of_Greece
  Finish (2ff20689-5b5c-4d54-82d2-5f8ed8811876)
 Call ID: 2ff20689-5b5c-4d54-82d2-5f8ed8811876
  Args: