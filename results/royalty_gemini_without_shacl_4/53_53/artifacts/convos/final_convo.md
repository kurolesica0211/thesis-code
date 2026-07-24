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
Constantine I (Greek: Κωνσταντίνος Αʹ, romanized: Konstantínos I; 2 August  1868 – 11 January 1923) was King of Greece from 18 March 1913 to 11 June 1917 and again from 19 December 1920 to 27 September 1922.
The eldest son of George I of Greece, he succeeded to the throne following his father's assassination in 1913.
Educated in Greece and later in Germany, Constantine was an admirer of Prussian militarism.
Later and under the leadership of Prime Minister Eleftherios Venizelos, he led successfully the Greek forces in the Balkan Wars of 1912–1913, in which Greece expanded, doubling in area and population.
He was married to Sophia of Prussia, a younger sister of Wilhelm II, the Emperor of Germany.
During his reign, Constantine's pro-German aligned interests led him to twice refuse Venizelos' popular elected mandates for Greece to join World War I on the side of Allies.
Constantine unconstitutionally dismissed his Prime Minister, causing the National Schism.
The country was split between the pro-Venizelos New Greece (lands of recently liberated in the Balkan Wars) and the royalist Old Greece, driving deep social cleavages and brought Greece at the brink of civil war.
After a five-month naval blockade of Athens by France and Great Britain that caused famine, Constantine abdicated, despite strong popular support for continued resistance.
After Alexander's death, Venizelos' defeat in the 1920 legislative elections, and a plebiscite in favor of his return, Constantine was reinstated.
Constantine I abdicated the throne  in favor of his eldest son George II in September 1922, after an army revolt of Venizelist officers.
Early life

Constantine was born on 2 August 1868 in Athens.
He was the eldest son of King George I and Queen Olga.
As the ceremonial cannon on Lycabettus Hill fired the royal salute, huge crowds gathered outside the Palace shouting what they thought should rightfully be the newborn prince's name: "Constantine".
This was both the name of his maternal grandfather, Grand Duke Konstantin Romanov of Russia, and the name of the "King who would reconquer Constantinople", the future "Constantine XII, legitimate successor to the Emperor Constantine XI Palaiologos", according to popular legend.
He was inevitably christened "Constantine" (Greek: Κωνσταντῖνος, Kōnstantīnos) on 12 August, and his official style was the Diádochos (Διάδοχος, Crown Prince, literally: "Successor").
The most prominent university professors of the time were handpicked to tutor the young Crown Prince: Ioannis Pantazidis taught him Greek literature; Vasileios Lakonas mathematics and physics; and Constantine Paparrigopoulos history, infusing the young prince with the principles of the Megali Idea.
Constantine also studied political science and business in Heidelberg and Leipzig.
In January 1895, Constantine caused political turmoil when he ordered army and gendarmerie forces to break up a street protest against tax policy.
Constantine had previously addressed the crowd and advised them to submit their grievances to the government.
King George responded that the Crown Prince was, in dispersing protesters, merely obeying military orders, and that his conduct lacked political significance.
The organization of the first modern Olympics in Athens was another issue which caused a Constantine-Trikoupis confrontation, with Trikoupis opposed to hosting the Games.
Subsequently, Constantine was instrumental in the organization of the 1896 Summer Olympics; according to Pierre de Coubertin, in 1894 "the Crown Prince learned with great pleasure that the Games will be inaugurated in Athens."
Constantine later conferred more than that; he eagerly assumed the presidency of the 1896 organizing committee.
At the Crown Prince's request, wealthy businessman George Averoff agreed to pay approximately one million drachmas to fund the restoration of the Panathinaiko Stadium in white marble.
Greco-Turkish War and aftermath

Constantine was the commander-in-chief of the Army of Thessaly in the Greco-Turkish War of 1897, which ended in a humiliating defeat.
In its aftermath, the popularity of the monarchy fell, and calls were raised in the army for reforms and the dismissal of the royal princes, and especially Constantine, from their command posts in the armed forces.
In its aftermath, he and his brothers were dismissed from the armed forces, only to be reinstated a few months later by the new prime minister, Eleftherios Venizelos, who was keen on gaining the trust of King George.
Balkan Wars

Overview

In 1912 with the formation of the Balkan League, Greece was ready for war against the Ottoman Empire and Prince Constantine became Chief of the Hellenic Army.
Macedonian Front

Previously the Inspector General of the Army, Constantine was appointed commander-in-chief of the "Army of Thessaly" when the First Balkan War broke out in October 1912.
At this point, his first clash with Venizelos occurred, as Constantine desired to press north, towards Monastir, where the bulk of the Ottoman army lay, and where the Greeks would rendezvous their Serb allies.
Venizelos notified Constantine that "... political considerations of the utmost importance dictate that Thessaloniki be taken as soon as possible".
After Constantine impudently cabled: "The army will not march on Thessaloniki.
As prime minister and war minister, he outranked Constantine and his response was famously three words long, a crisp military order to be obeyed forthwith: "I forbid you".
Constantine was left with no choice but to turn east, and after defeating the Ottoman army at Giannitsa, he accepted the surrender of the city of Thessaloniki and of its Ottoman garrison on 27 October (O.S.), less than 24 hours before the arrival of Bulgarian forces who hoped to capture the city first.
The capture of Thessaloniki against Constantine's whim proved a crucial achievement: the pacts of the Balkan League had provided that in the forthcoming war against the Ottoman Empire, the four Balkan allies would provisionally hold any ground they took from the Turks, without contest from the other allies.
With operations in Macedonia complete, Constantine transferred the bulk of his forces to Epirus, and assumed command.
These victories dispelled the tarnish of the 1897 defeat, and raised Constantine to great popularity with the Greek people.
Accession to the Throne and Second Balkan War

George
I was assassinated in Thessaloniki by an anarchist, Alexandros Schinas, on 18 March 1913, and Constantine succeeded to the throne.
In May, Greece and Serbia concluded a secret defensive pact aimed at Bulgaria.
King Constantine led the Greek Army in its counterattack in the battles of Kilkis-Lahanas and the Kresna Gorge.
On the initiative of Prime Minister Venizelos, Constantine was also awarded the rank and baton of a Field Marshal.
World War I and the National Schism

Overview

The widely held view of Constantine I as a "German sympathizer" owes something to his marriage with Sophia of Prussia, sister of Wilhelm II, to his studies in Germany and his supposed "militaristic" beliefs and attitude.
Constantine did rebuff Kaiser Wilhelm who in 1914 pressed him to bring Greece into the war on the side of Austria-Hungary and Germany.
Constantine then offended also the British and French by blocking popular efforts by Prime Minister Venizelos to bring Greece into the war on the side of the Allies.
Constantine's insistence on neutrality, according to him and his supporters, was based more on his judgement that it was the best policy for Greece, rather than venal self-interest or his German dynastic connections, as he was accused of by the Venizelists.
He wrote in 1920:


"The persecution of King Constantine by the press of the Allied countries, with some few good exceptions, has been one of the most tragic affairs since the Dreyfus case."
Although Venizelos, with Allied support, forced Constantine to leave the throne in 1917, he remained popular with parts of the Greek people (as shown by the vote for his return in the December 1920 plebiscite), who saw the Allied actions as a violation of sovereignty of Greece.
Events

In the aftermath of the victorious Balkan Wars, Greece was in a state of euphoria.
Her territory and population had doubled with the massive liberation of Greeks from Ottoman rule and, under the dual leadership of Constantine and Venizelos, her future seemed bright.
However Constantine had been ill with pleurisy since the Balkan wars and almost died during the summer of 1915.
Constantine was faced with the difficulty of determining where Greece's support lay.
His first concern as King was for the welfare and security of Greece.
He rejected the early appeal from Kaiser Wilhelm that Greece should march on the side of Germany and stated that Greece would remain neutral.
Sophie, Constantine's queen, was popularly thought to support her brother Kaiser Wilhelm, but it seems that she was actually pro-British; like her father the late Kaiser Frederick, Sophie was influenced by her mother, the British-born Victoria.
Both Venizelos and Constantine were keenly aware that a maritime country like Greece could not, and should not, antagonise the Entente, the dominant naval powers in the Mediterranean.
Constantine settled on a policy of neutrality because it seemed the path that best assured that Greece would emerge from the World War intact and with the substantial territorial gains it had won in the recent Balkan Wars.
In January 1915, the Entente made proposals to both Bulgaria and Greece to side with it.
Bulgaria would take eastern Macedonia from Greece (with Drama and Kavala), while Greece in exchange would gain land in Asia Minor from Turkey after the war.
Venizelos agreed but Constantine rejected the proposal.
Constantine claimed his military judgement was right, after the outcome of the Allies' failed operation of landing on Gallipoli.
Despite the popularity of Venizelos and his clear majority in Parliament for supporting the Allies, Constantine opposed Venizelos.
Venizelos actually wanted Greece to participate at the Gallipoli operation, but after military objections by the General Staff (Ioannis Metaxas), the King rejected the idea.
In autumn 1915, Bulgaria joined the Central Powers and attacked Serbia, with which Greece had a treaty of alliance.
Venizelos again urged the King to allow Greece's entry into the war.
The Hellenic army was mobilized for defensive reasons, but Constantine claimed that the treaty had no value in case of a global war, but only of Balkan issues.
The British then offered Cyprus to the Greek Kingdom to join the war, but Constantine rejected this offer as well.
At the same time, Germany offered the protection and security of the Greek population of Turkey during and after the war, in exchange for Greece to remain neutral.
Constantine was accused also by his Venizelist opponents for secret discussions and correspondence with the Central Powers.
In March 1916, in an effort to increase his prestige, Constantine declared the official annexation of Northern Epirus, which was controlled by the Greeks since 1914, but the Greek forces were driven from the area by the Italians and French during the next year.
In June 1916, Constantine, General Metaxas (the future dictator) and Prime Minister Skouloudis allowed Fort Rupel and parts of eastern Macedonia to be occupied, without opposition, by the Germans and Bulgarians, as a counterbalance to the Allied forces in Thessaloniki.
The leadership of the Allied armies in Thessaloniki was worried also about a possible attack by the army of Constantine in their back.
The royal governments of Constantine in Athens continued to negotiate with the Allies a possible entry in the war.
During November/December 1916, the British and French landed units at Athens claiming the surrender of war materiel equivalent to what was lost at Fort Rupel as a guarantee of Greece's neutrality.
Constantine so became the most hated person for the Allies after his best man Kaiser Wilhelm.
After the fall of the monarchy in Russia, Constantine lost his last supporter inside the Entente opposed to his removal from the throne.
In the face of Venizelist and Anglo-French pressure, King Constantine finally left the country for Switzerland on 11 June 1917; his second-born son Alexander became king in his place.
The Allied Powers were opposed to Constantine's first born son George becoming king, as he had served in the German army before the war and like his father was thought to be a Germanophile.
Greece had at this point been at war for eight continuous years: World War I had come and gone, but yet no sign of an enduring peace was near, as the country was already at war against the Kemalist forces in Asia Minor.
Following a plebiscite in which nearly 99% of votes were cast in favor of his return, Constantine returned as king on 19 December 1920.
This caused great dissatisfaction not only to the newly liberated populations in Asia Minor, but also to the British and even more the French, who opposed the return of Constantine.
In March 1921, despite his health problems, Constantine was landed in Anatolia to boost the Army's morale and command personally the Battle of Kütahya-Eskişehir.
Following an army revolt by Venizelist officers, considering him as key responsible for the defeat, Constantine abdicated the throne again on 27 September 1922 and was succeeded by his eldest son, George II.
His wife, Sophie of Prussia, was never allowed back to Greece and was later interred beside her husband in the Russian Church in Florence.
After his restoration on the Greek throne, George II organized the repatriation of the remains of members of his family who died in exile; an important religious ceremony that brought together, for six days in November 1936, all members of the royal family still alive.
Constantine's body was buried at the royal burial ground at Tatoi Palace, where he remains.
Marriage and issue

As Crown Prince of Greece, Constantine married Princess Sophia of Prussia, a granddaughter of Queen Victoria and sister of Kaiser Wilhelm II, on 27 October 1889 in Athens.
Legacy and popular culture

Constantine remained an idol for his supporters (much like Venizelos for his own supporters), and generally for the conservative Right, for years after his death.
In the popular culture, the slogan of the royalists "psomí, elia ke Kotso Vasiliá" ("bread, olives and King Constantine") still survives.
It was a popular phrase during the naval blockade of southern Greece by the Allied fleet (1916/17), which caused hunger to the population.
Titles, styles, honours and arms

Titles and styles

From birth, Constantine was styled "His Royal Highness The Crown Prince (Diadochos) of Greece" until his accession to the throne.
On the day of his baptism, his father issued a royal decree granting him the additional title of Duke of Sparta; however, this title was used only outside of Greece.
He is sometimes numbered Constantine XII in succession to Constantine XI Palaiologos.



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
  AssignClass (4245b943-5fb8-4467-84ad-b36e3c020432)
 Call ID: 4245b943-5fb8-4467-84ad-b36e3c020432
  Args:
    type: :Man
    source: :Constantine_I
  AssignClass (38cded5d-96ab-4f6f-87d1-d84edce1b227)
 Call ID: 38cded5d-96ab-4f6f-87d1-d84edce1b227
  Args:
    type: :Person
    source: :Constantine_I
  AddLiteral (2ce609e7-a73d-4ff7-9aae-1d1640f01c3b)
 Call ID: 2ce609e7-a73d-4ff7-9aae-1d1640f01c3b
  Args:
    literal_value: 1868
    relation: :hasBirthYear
    source: :Constantine_I
    literal_type: xsd:integer
  AddLiteral (ed2a22c2-58f5-4a63-8cad-3a76046ed4dd)
 Call ID: ed2a22c2-58f5-4a63-8cad-3a76046ed4dd
  Args:
    literal_value: 1923
    source: :Constantine_I
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (ebf186ac-e493-4294-bd22-4b522790f242)
 Call ID: ebf186ac-e493-4294-bd22-4b522790f242
  Args:
    type: :Man
    source: :George_I_of_Greece
  AssignClass (69a428ae-38de-4162-a16d-3a4231288cb3)
 Call ID: 69a428ae-38de-4162-a16d-3a4231288cb3
  Args:
    type: :Person
    source: :George_I_of_Greece
  AssignClass (88bc7eff-d580-439b-a02c-a89e948ed2cb)
 Call ID: 88bc7eff-d580-439b-a02c-a89e948ed2cb
  Args:
    type: :Woman
    source: :Olga_of_Greece
  AssignClass (1bd2f201-c63e-4983-b1e3-7831f4453a09)
 Call ID: 1bd2f201-c63e-4983-b1e3-7831f4453a09
  Args:
    type: :Person
    source: :Olga_of_Greece
  AddTriple (37a00d6d-60e7-4240-b82e-1f0eb5c6c1b0)
 Call ID: 37a00d6d-60e7-4240-b82e-1f0eb5c6c1b0
  Args:
    source: :Constantine_I
    relation: :hasFather
    target: :George_I_of_Greece
  AddTriple (68dc6bea-07de-416f-8ef6-38a26e9af4c4)
 Call ID: 68dc6bea-07de-416f-8ef6-38a26e9af4c4
  Args:
    target: :Olga_of_Greece
    relation: :hasMother
    source: :Constantine_I
  AssignClass (73a2120c-ffe3-4a05-a5d9-9e2cbc1923f5)
 Call ID: 73a2120c-ffe3-4a05-a5d9-9e2cbc1923f5
  Args:
    type: :Woman
    source: :Sophia_of_Prussia
  AssignClass (281f582c-c9c9-48b6-8957-4395d37c43cb)
 Call ID: 281f582c-c9c9-48b6-8957-4395d37c43cb
  Args:
    type: :Person
    source: :Sophia_of_Prussia
  AddTriple (97baa729-fa06-4294-8720-d19efac8fd3f)
 Call ID: 97baa729-fa06-4294-8720-d19efac8fd3f
  Args:
    source: :Constantine_I
    relation: :hasRelation
    target: :Sophia_of_Prussia
  AddLiteral (cc7a8a62-e1db-44a5-bbde-636dd22f8103)
 Call ID: cc7a8a62-e1db-44a5-bbde-636dd22f8103
  Args:
    literal_type: xsd:integer
    source: :Constantine_I
    relation: :hasMarriageYear
    literal_value: 1889
  AssignClass (21bf54f4-7c04-4b9a-a024-1f2199e61c1b)
 Call ID: 21bf54f4-7c04-4b9a-a024-1f2199e61c1b
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (f9b95c2f-de3d-437c-b3b6-66fe588b8975)
 Call ID: f9b95c2f-de3d-437c-b3b6-66fe588b8975
  Args:
    type: :Person
    source: :Wilhelm_II
  AddTriple (7fed0b3f-249d-488a-bdeb-a2c616df180c)
 Call ID: 7fed0b3f-249d-488a-bdeb-a2c616df180c
  Args:
    source: :Wilhelm_II
    relation: :hasSister
    target: :Sophia_of_Prussia
  AssignClass (b3736e75-e547-424d-b1c2-23db223eb77b)
 Call ID: b3736e75-e547-424d-b1c2-23db223eb77b
  Args:
    type: :Man
    source: :Alexander_of_Greece
  AssignClass (9167f549-4c9f-4024-9528-32870fa984bf)
 Call ID: 9167f549-4c9f-4024-9528-32870fa984bf
  Args:
    type: :Person
    source: :Alexander_of_Greece
  AddTriple (2465352d-5f57-4098-8833-083158c334ff)
 Call ID: 2465352d-5f57-4098-8833-083158c334ff
  Args:
    source: :Alexander_of_Greece
    relation: :hasFather
    target: :Constantine_I
  AssignClass (18c709d2-1e80-4e1f-be6a-6d31c077eecb)
 Call ID: 18c709d2-1e80-4e1f-be6a-6d31c077eecb
  Args:
    type: :Man
    source: :George_II_of_Greece
  AssignClass (ad0e1d23-6da8-461f-a3ce-f70ec28b4032)
 Call ID: ad0e1d23-6da8-461f-a3ce-f70ec28b4032
  Args:
    type: :Person
    source: :George_II_of_Greece
  AddTriple (4830d270-24f7-4c7a-9d0f-e9fa17673a48)
 Call ID: 4830d270-24f7-4c7a-9d0f-e9fa17673a48
  Args:
    source: :George_II_of_Greece
    relation: :hasFather
    target: :Constantine_I
  AssignClass (47857fa7-4f07-4f92-9091-4a0d857acc85)
 Call ID: 47857fa7-4f07-4f92-9091-4a0d857acc85
  Args:
    type: :Man
    source: :Konstantin_Romanov
  AssignClass (19f75d58-b6e9-495b-b4ec-885f26348be4)
 Call ID: 19f75d58-b6e9-495b-b4ec-885f26348be4
  Args:
    type: :Person
    source: :Konstantin_Romanov
  AddTriple (63768f92-0de4-4933-9cef-f77cc4f52353)
 Call ID: 63768f92-0de4-4933-9cef-f77cc4f52353
  Args:
    relation: :hasFather
    source: :Olga_of_Greece
    target: :Konstantin_Romanov
  Finish (f31b0e28-f007-4471-bd0c-6b5a3c69d103)
 Call ID: f31b0e28-f007-4471-bd0c-6b5a3c69d103
  Args: