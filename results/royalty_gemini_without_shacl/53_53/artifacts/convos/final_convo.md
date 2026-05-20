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
In late 1916, his pro-German policies led to the unconditional surrender of Fort Roupel and the loss of much of newly conquered Macedonian territories to Bulgaria.
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
In the following elections Trikoupis was defeated, and the new prime minister, Theodoros Deligiannis, seeking to downplay hostility between government and the Palace, regarded the matter closed.
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
Advancing on foot, the Greeks soundly defeated the Turks twice, and were in Thessaloniki within 4 weeks.
With the Bulgarians directing the bulk of their force towards Constantinople, the capture of Thessaloniki would ensure that the railway axis between these two main cities was lost to the Turks, causing loss of logistics and supplies and severe impairment of command and control capability.
The Turks would be hard placed to recruit locals, as their loyalties would be liable to lie with the Balkan Allies.
Ottoman armies in Europe would be quickly cut off and their loss of morale and operational capability would lead them toward a quick surrender.
Macedonian Front

Previously the Inspector General of the Army, Constantine was appointed commander-in-chief of the "Army of Thessaly" when the First Balkan War broke out in October 1912.
At this point, his first clash with Venizelos occurred, as Constantine desired to press north, towards Monastir, where the bulk of the Ottoman army lay, and where the Greeks would rendezvous their Serb allies.
Venizelos notified Constantine that "... political considerations of the utmost importance dictate that Thessaloniki be taken as soon as possible".
After Constantine impudently cabled: "The army will not march on Thessaloniki.
As prime minister and war minister, he outranked Constantine and his response was famously three words long, a crisp military order to be obeyed forthwith: "I forbid you".
Constantine was left with no choice but to turn east, and after defeating the Ottoman army at Giannitsa, he accepted the surrender of the city of Thessaloniki and of its Ottoman garrison on 27 October (O.S.), less than 24 hours before the arrival of Bulgarian forces who hoped to capture the city first.
The capture of Thessaloniki against Constantine's whim proved a crucial achievement: the pacts of the Balkan League had provided that in the forthcoming war against the Ottoman Empire, the four Balkan allies would provisionally hold any ground they took from the Turks, without contest from the other allies.
With operations in Macedonia complete, Constantine transferred the bulk of his forces to Epirus, and assumed command.
After lengthy preparations, the Greeks broke through the Ottoman defences in the Battle of Bizani and captured Ioannina and most of Epirus up into what is today southern Albania (Northern Epirus).
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
In July 1916, arsonists set fire to the forest surrounding the summer palace at Tatoi.
With Allied support, the revolutionary government of Venizelos gained control of half the country – significantly, most of the "New Lands" won during the Balkan Wars.
This cemented the National Schism, a division of Greek society between Venizelists and anti-Venizelist monarchists, which was to have repercussions in Greek politics until past World War II.
The royal governments of Constantine in Athens continued to negotiate with the Allies a possible entry in the war.
During November/December 1916, the British and French landed units at Athens claiming the surrender of war materiel equivalent to what was lost at Fort Rupel as a guarantee of Greece's neutrality.
Constantine so became the most hated person for the Allies after his best man Kaiser Wilhelm.
After the fall of the monarchy in Russia, Constantine lost his last supporter inside the Entente opposed to his removal from the throne.
In the face of Venizelist and Anglo-French pressure, King Constantine finally left the country for Switzerland on 11 June 1917; his second-born son Alexander became king in his place.
The Allied Powers were opposed to Constantine's first born son George becoming king, as he had served in the German army before the war and like his father was thought to be a Germanophile.
What seemed like a minor injury turned to sepsis, and he died a few days later.
Greece had at this point been at war for eight continuous years: World War I had come and gone, but yet no sign of an enduring peace was near, as the country was already at war against the Kemalist forces in Asia Minor.
Following a plebiscite in which nearly 99% of votes were cast in favor of his return, Constantine returned as king on 19 December 1920.
This caused great dissatisfaction not only to the newly liberated populations in Asia Minor, but also to the British and even more the French, who opposed the return of Constantine.
In March 1921, despite his health problems, Constantine was landed in Anatolia to boost the Army's morale and command personally the Battle of Kütahya-Eskişehir.
Following an army revolt by Venizelist officers, considering him as key responsible for the defeat, Constantine abdicated the throne again on 27 September 1922 and was succeeded by his eldest son, George II.
Second exile and death

He spent the last four months of his life in exile in Italy and died at 1:30 am on 11 January 1923 at Palermo, Sicily of heart failure.
His wife, Sophie of Prussia, was never allowed back to Greece and was later interred beside her husband in the Russian Church in Florence.
After his restoration on the Greek throne, George II organized the repatriation of the remains of members of his family who died in exile; an important religious ceremony that brought together, for six days in November 1936, all members of the royal family still alive.
Constantine's body was buried at the royal burial ground at Tatoi Palace, where he remains.
Marriage and issue

As Crown Prince of Greece, Constantine married Princess Sophia of Prussia, a granddaughter of Queen Victoria and sister of Kaiser Wilhelm II, on 27 October 1889 in Athens.
Their eldest daughter Helen married Crown Prince Carol of Romania; their second daughter married the 4th Duke of Aosta; while their youngest child, Princess Katherine, married a British commoner.
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
  AssignClass (fdd75982-65a5-405c-98f0-e717a23ae11d)
 Call ID: fdd75982-65a5-405c-98f0-e717a23ae11d
  Args:
    type: :Man
    source: Constantine_I
  AssignClass (367c1c73-f3a7-43ab-94b4-6611658d5025)
 Call ID: 367c1c73-f3a7-43ab-94b4-6611658d5025
  Args:
    type: :Person
    source: Constantine_I
  AssignClass (da734ea2-578c-4138-909f-72346d8c8e40)
 Call ID: da734ea2-578c-4138-909f-72346d8c8e40
  Args:
    source: George_I
    type: :Man
  AssignClass (ba8ac41f-f7e4-49c4-b8da-e4682dd10fef)
 Call ID: ba8ac41f-f7e4-49c4-b8da-e4682dd10fef
  Args:
    type: :Person
    source: George_I
  AssignClass (b26b815e-c7d4-4b38-8149-5835050fc9ba)
 Call ID: b26b815e-c7d4-4b38-8149-5835050fc9ba
  Args:
    source: Olga
    type: :Woman
  AssignClass (e8bdca0b-c6bf-448d-8f49-78d89b1f5a82)
 Call ID: e8bdca0b-c6bf-448d-8f49-78d89b1f5a82
  Args:
    type: :Person
    source: Olga
  AssignClass (e4258825-27d2-4cba-ae09-2fa872ec175d)
 Call ID: e4258825-27d2-4cba-ae09-2fa872ec175d
  Args:
    source: Sophia_of_Prussia
    type: :Woman
  AssignClass (eedf031e-6a14-4470-a891-05f9c2a130df)
 Call ID: eedf031e-6a14-4470-a891-05f9c2a130df
  Args:
    source: Sophia_of_Prussia
    type: :Person
  AssignClass (26d1b3ae-dd98-4fa8-8753-0617be15988c)
 Call ID: 26d1b3ae-dd98-4fa8-8753-0617be15988c
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (349d39dd-ed74-4ee9-bbb2-d633f9ed4f43)
 Call ID: 349d39dd-ed74-4ee9-bbb2-d633f9ed4f43
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (6da5fda6-cd3e-47d4-b17d-7290fe4cbebe)
 Call ID: 6da5fda6-cd3e-47d4-b17d-7290fe4cbebe
  Args:
    type: :Man
    source: Alexander
  AssignClass (090e1ed2-bee1-4fe3-93be-4055b6f7f7bc)
 Call ID: 090e1ed2-bee1-4fe3-93be-4055b6f7f7bc
  Args:
    type: :Person
    source: Alexander
  AssignClass (40cf03af-a299-47ac-9248-565b722afb47)
 Call ID: 40cf03af-a299-47ac-9248-565b722afb47
  Args:
    source: George_II
    type: :Man
  AssignClass (0c91b191-0f20-45a8-9d11-ab78640ecc09)
 Call ID: 0c91b191-0f20-45a8-9d11-ab78640ecc09
  Args:
    source: George_II
    type: :Person
  AssignClass (200bae47-0288-4625-a29f-2f71daeccf46)
 Call ID: 200bae47-0288-4625-a29f-2f71daeccf46
  Args:
    type: :Woman
    source: Helen
  AssignClass (84aa4d53-6f6c-48e6-9bfd-2fa8e35e029b)
 Call ID: 84aa4d53-6f6c-48e6-9bfd-2fa8e35e029b
  Args:
    type: :Person
    source: Helen
  AssignClass (8082e631-aece-4685-8a73-fe369f1695c5)
 Call ID: 8082e631-aece-4685-8a73-fe369f1695c5
  Args:
    type: :Woman
    source: Katherine
  AssignClass (37b67e39-731b-4dfd-8b3d-530dc9debbf2)
 Call ID: 37b67e39-731b-4dfd-8b3d-530dc9debbf2
  Args:
    type: :Person
    source: Katherine
  AssignClass (be44c914-8109-47c5-b230-d753841067b3)
 Call ID: be44c914-8109-47c5-b230-d753841067b3
  Args:
    source: Konstantin_Romanov
    type: :Man
  AssignClass (499bbf83-c1ae-4b62-a560-f92dfa3e4479)
 Call ID: 499bbf83-c1ae-4b62-a560-f92dfa3e4479
  Args:
    type: :Person
    source: Konstantin_Romanov
  AddTriple (5cca96d8-768d-492e-92df-3812afa244e2)
 Call ID: 5cca96d8-768d-492e-92df-3812afa244e2
  Args:
    source: Constantine_I
    target: George_I
    relation: :hasFather
  AddTriple (a2f23930-c649-47ac-9015-aba76eb8155a)
 Call ID: a2f23930-c649-47ac-9015-aba76eb8155a
  Args:
    source: Constantine_I
    target: Olga
    relation: :hasMother
  AddTriple (e9b1d69d-7195-4bba-b580-b11925193a89)
 Call ID: e9b1d69d-7195-4bba-b580-b11925193a89
  Args:
    source: Constantine_I
    relation: :hasFather
    target: Konstantin_Romanov
  AddTriple (8da0bf19-cec1-4b2c-bc1a-a0eeb38a138d)
 Call ID: 8da0bf19-cec1-4b2c-bc1a-a0eeb38a138d
  Args:
    target: Sophia_of_Prussia
    relation: :hasSister
    source: Wilhelm_II
  AddTriple (57e7697c-52a8-431e-b7a8-6acb26d12045)
 Call ID: 57e7697c-52a8-431e-b7a8-6acb26d12045
  Args:
    relation: :hasSon
    target: Alexander
    source: Constantine_I
  AddTriple (49dc75aa-8a15-41de-88fb-c19a41a4c344)
 Call ID: 49dc75aa-8a15-41de-88fb-c19a41a4c344
  Args:
    source: Constantine_I
    relation: :hasSon
    target: George_II
  AddTriple (44150c78-9087-4528-b460-d9374d2cf2bb)
 Call ID: 44150c78-9087-4528-b460-d9374d2cf2bb
  Args:
    source: Constantine_I
    target: Helen
    relation: :hasDaughter
  AddTriple (efa72ac1-8fa3-419b-b467-e21030bfd07c)
 Call ID: efa72ac1-8fa3-419b-b467-e21030bfd07c
  Args:
    relation: :hasDaughter
    target: Katherine
    source: Constantine_I
  AddLiteral (c47112f9-8956-49d2-94d3-4d88f9b9276c)
 Call ID: c47112f9-8956-49d2-94d3-4d88f9b9276c
  Args:
    source: Constantine_I
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1868
  AddLiteral (e41103b2-36ba-4e87-8df4-ba66364f0072)
 Call ID: e41103b2-36ba-4e87-8df4-ba66364f0072
  Args:
    literal_value: 1923
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Constantine_I
  AddLiteral (d85573da-6858-42e7-904a-fc90afa2425f)
 Call ID: d85573da-6858-42e7-904a-fc90afa2425f
  Args:
    literal_type: xsd:integer
    source: Constantine_I
    literal_value: 1889
    relation: :hasMarriageYear
  Finish (6810be97-8a79-4cd9-a4d7-1b901a0aeb35)
 Call ID: 6810be97-8a79-4cd9-a4d7-1b901a0aeb35
  Args: