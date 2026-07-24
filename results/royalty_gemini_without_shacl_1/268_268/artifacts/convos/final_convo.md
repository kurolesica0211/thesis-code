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
Grand Duke Boris Vladimirovich of Russia (Russian: Борис Владимирович; 24 November 1877 – 9 November 1943) was a son of Grand Duke Vladimir Alexandrovich of Russia, a grandson of Tsar Alexander II of Russia and a first cousin of Tsar Nicholas II.
He was known in Imperial Russia for his restless behavior and as a notorious playboy.
He departed revolutionary Russia in March 1919 with his longtime mistress, whom he married in exile.
Early life

Grand Duke Boris Vladimirovich was born on 24 November  1877 at his parents' palace in Saint Petersburg.
He was the third child and second surviving son among the five children of Grand Duke Vladimir Alexandrovich of Russia and his wife Grand Duchess Maria Pavlovna, née Duchess Marie Alexandrine of Mecklenburg-Schwerin.
His parents were very wealthy and lived in the luxurious Vladimir Palace in Saint Petersburg.
His father, Vladimir Alexandrovich, a brother of Tsar Alexander III of Russia, was a renowned patron of the arts; his mother, Maria Pavlovna, one of the greatest hostesses of Russian society.
Boris, more extroverted than his siblings, was his mother's favorite.
Grand Duke Boris was educated at home.
As was customary in the Russian Imperial family, Boris and his siblings also have a sailor "nanny", a male attendant from the Imperial navy, who served as the children's companion looking after them.
Boris Vladimirovich's education emphasized languages and military training.
From his birth, Grand Duke Boris was appointed patron of the 45th Azov Infantry Regiment, and enrolled into the Semeonovsky Life Guards and the Life Guards Dragoon regiment, the 4th Life Guard Rifle Battalion of the Imperial Family.
A Russian Grand Duke

At age eighteen, upon coming of age, Grand Duke Boris received from his father a plot of land at Tsarskoye Selo on the eastern bank of the Kolonistky pond near the Moskovskaya Gate.
There, in 1895, the Grand Duke built his own residence in the style of an English country house.
The estate, named Wolf Garden, compromised a cottage, coach house, stables, and a small tea house, where the grand duke could entertain his friends.
Boris Vladimirovich lived in Wolf Garden all year round while still serving in the army.
From his early youth Boris was notorious for his restless life style.
The grand duke also got entangled with a Mademoiselle Demidov.
The famous ballerina Anna Pavlova was one of Boris' lovers.
Although loaded with wealth and privilege, Grand Duke Boris found his income insufficient and ran up a huge debt of nearly half a million rubles with his mother.
In 1901, Grand Duke Boris, age twenty five, had a liaison with a Frenchwoman, Jeanne Aumont-Lacroix, and had a son by her, born in Paris.
The child, Jean Boris Lacroix (1902–1984), was not recognized.
To break the relationship and strengthen his character Boris's parents sent him, with the Tsar's approval, on a world tour.
World tour

Grand Duke Boris' tour around the world lasted from 6 January  1902  until 20 October  1902.
As there was an unexpected delay in the expedition, he spent the holidays with his aunt Grand Duchess Maria Alexandrovna and his cousin Victoria Melita in their winter home in Nice.
On 1 August 1902, Grand Duke Boris arrived in San Francisco where he toured the city; attended the opera and went to a boxing match.
In Newport, Boris Vladimirovich was invited to dinners and parties, he played tennis and even learned to play golf.
The grand duke was favorably impressed with the city's skyline and the modern use of electricity Boris visited President Theodore Roosevelt at his estate Sagamore Hill, on the North Shore of Long Island.
After six hectic weeks in America, Grand Duke Boris sailed back to Europe.
Jovial and increasingly stout, Boris was famous for his wild and unpredictable behavior, but eventually these excesses began to lose their appeal.
On 26 February, he left Russia for the Far East to take part in the Russo-Japanese War.
He served under the command of the Russian governor in the Far East at the headquarters of the commander in chief of the Army, General A.N.  Kuropatkin, taking part in combat


On the morning of 31 March 1904, while galloping from the heights of Dacha Hill on the rim of Port Arthur, he witnessed the sinking of the Russian battleship Petropavlovsk in which more than 600 men died; his brother Grand Duke Kirill was among the few survivors.
In 1905, in Nice, Grand Duke Boris proposed to Princess Victoria Eugenia of Battenberg.
By then she had forgotten about Boris and in the next season she met her future husband King Alfonso XIII of Spain.
1911 was a busy year for the grand duke.
He was made colonel and in April he represented Russia at the Turin World Fair and the Fine Arts Exhibition in Rome during the celebrations for the 50th anniversary of Italy's unification.
In November the same year, he was Russia's emissary at the coronation of Vajiravudh the King of Siam.
War

When World War I broke out, Boris Vladimirovich was put in command of the Guards regiment of the Ataman Cossacks.
Military service was a burden to Boris, who sought every opportunity that would make him return to St. Petersburg.
Even during the war Grand Duke Boris gave many parties at his luxurious mansion, furnished in the English style, which at night was a gathering place for the "golden youth" of St. Petersburg.
The grand duke was famous for his hospitality, cheerful disposition, passion for entertainment, gourmet cuisine and excellent wines.
In spite of Boris' reputation, his ambitious mother wanted to arrange a splendid marriage for him.
In February 1916, she tried to marry him to Grand Duchess Olga Nikolaevna, Tsar Nicholas II's eldest daughter.
Boris was thirty-eight with a long line of mistresses linked to his name.
The refusal provoked the enmity of Boris' mother.
Towards the end of the monarchy, they were involved in a conspiracy to put Boris' brother Kirill on the throne.
Boris' Anglophobia got him into trouble during the War.
His behavior was so insulting that the British Ambassador made a formal protest, and Boris was forced by the Emperor to apologize.
By the summer of 1916, Grand Duke Boris fell in love with Zinaida Sergeievna Rachevskaya (1896–1963), the daughter of Colonel Sergei Alexandrovich Rachevsky, who had died in 1904 commanding the fortifications at Port Arthur.
Zinaida, a vivacious brunette twenty years younger than Boris, belonged the minor Russian nobility.
Grand Duke Boris would have liked to marry her, but as he was close in line to the Russian throne a morganatic marriage would not have been authorized.
To get out of his predicament, Boris quickly arranged Zinaida's marriage to Peter Eliseev, a military officer from a prestigious family who accepted the deal in exchange for the grand duke payment of his gambling debts.
Back in Russia, a divorce was obtained for her.
Grand Duke Boris began to live openly with his mistress at his dasha in Tsarskoye Selo as the Russian Empire began to crumble.
When Nicholas II abdicated, Boris was at Gatchina with Grand Duke Michael Alexandrovich, who declined the throne.
This marked the fall of the Russian monarchy and Boris was one of the few members of the Romanov family who went to Mogilev to pay final respects to Tsar Nicholas II.


Revolution

During the period of the provisional government Boris Vladimirovich was living in Tsarskoye Selo.
He was able to gain entrance to the Vladimir Palace.
Disguised, with the help of Englishman Albert Stopford and a caretaker, Boris retrieved the money and jewels from the secret safe in his mother's bedroom.
Before the Bolsheviks took power, Boris escaped the former Imperial capital to the Caucasus with his mistress Zinaida Rachevskaya.
In September 1917, he joined his mother and younger brother Grand Duke Andrei Vladimirovich in Kislovodsk, a spa and resort town in the Caucasus.
He lived in a villa with his brother, but their mistresses were placed in separate houses, because Grand Duchess Maria Pavlovna would not acknowledge their existence.
For the next year they lived quietly away from danger, but in August 1918 Boris and his brother Andrei were arrested in the night after a systematic search of their villa.
The Bolshevik commander sent to execute them had once been a struggling artist in Paris before the war whom Boris had helped by buying some of his paintings.
Since they were no longer safe and would probably be arrested again, the two grand dukes decided to flee.
On 26 August 1918, armed with false papers stating they were on a mission for the soviets, Boris and Andrei escaped heading for Kabarda, where the chief Circassian tribe, the Kabards, lived on the north slope of the mountain.
However, Grand Duchess Maria Pavlovna was determined to remain in Russia hoping that the White movement would prevail and Boris' brother Grand Duke Kirill Vladimirovich would be installed as Tsar.
By March 1919 Boris decided to leave with his mistress.
Against his mother's wishes, he left Russia from Anapa by boat through the Black Sea.
Exile

Once safe in exile in Constantinople, Boris tried to get permission to go to Britain but was refused passage on a British warship.
Boris and Zinaida went to France but were expelled after a few weeks.
They wanted to settle in Spain, as Grand Duke Boris was a friend of King Alfonso XIII of Spain, but received no reply and settled in San Remo, instead.
Eventually Boris and his wife settled provisionally in Nice, France.
Boris and his siblings were reunited in exile in September 1920, at Contrexéville in the south of France, by the death of their mother Grand Duchess Maria Pavlovna.
Boris inherited his mother's emeralds, the most valuable items of the Grand Duchess' jewel collection.
With the money from the emeralds, and from an account with an American bank which he had opened prior to the Revolution, Boris bought a chateau, "Sans Souci", in Meudon near Paris, living comfortably with his wife.
When asked by a reporter whether Henry Ford was a financial supporter of the effort to restore the monarchy in Russia, Boris did not know who Henry Ford was.
His brother, Grand Duke Kirill, wanted to restore the Russian monarchy and in 1924 proclaimed himself czar-in-exile, but Boris was largely uninterested in politics.
Last years

During the long years of exile the former playboy-Grand Duke remained in love with his wife, who was twenty years his junior.
Of the Romanovs, the couple was close only with Grand Duke Andrei Vladimirovich and his morganatic wife Mathilde Kschessinskaya.
Zinaida was widely looked down upon by Boris' relatives.
In exile, Boris frequented his illegitimate son, Boris Lacroix, who had been raised in France by his mother's family.
Boris often visited his son, who became a famous designer under the name Jean Boris Lacroix.
During World War II, Boris and Zinaida were at their villa in Biarritz when German troops occupied Paris in June 1940.
Fleeing the French capital Grand Duke Andrei Vladimirovich and his wife Mathilde came to live with Boris.
In 1943, Grand Duke Boris became critically ill, and died in his bed on 9 November 1943, in Paris, at age 65.
In popular culture

Grand Duke Boris was well known before the war as an international playboy, and appears in many memoirs and novels of the period.
"If you'd only throw in Harry Thaw, Tod Sloan, Abe Hummel, and Grand Duke Boris it would be really chic, — a real salon!”



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
  AssignClass (93cda9f2-e787-45b4-aacf-aa7b63dc4316)
 Call ID: 93cda9f2-e787-45b4-aacf-aa7b63dc4316
  Args:
    type: :Man
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
  AssignClass (141962af-144d-42a2-a757-fee41fd3d2a6)
 Call ID: 141962af-144d-42a2-a757-fee41fd3d2a6
  Args:
    type: :Man
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AssignClass (64434778-c0d8-4684-bdb0-9d6ee436d0bc)
 Call ID: 64434778-c0d8-4684-bdb0-9d6ee436d0bc
  Args:
    type: :Man
    source: Tsar_Alexander_II_of_Russia
  AssignClass (fdcfd4b7-45ce-4e8e-8217-93275dfc0951)
 Call ID: fdcfd4b7-45ce-4e8e-8217-93275dfc0951
  Args:
    type: :Man
    source: Tsar_Nicholas_II
  AssignClass (896d8ae8-d80f-46c1-9086-c087efbec198)
 Call ID: 896d8ae8-d80f-46c1-9086-c087efbec198
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Pavlovna
  AssignClass (62d77d80-0057-41ad-89c7-b9bee9fd2ec0)
 Call ID: 62d77d80-0057-41ad-89c7-b9bee9fd2ec0
  Args:
    type: :Woman
    source: Duchess_Marie_Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (006988c8-ae5e-4d4b-8041-0ca02ba44c6a)
 Call ID: 006988c8-ae5e-4d4b-8041-0ca02ba44c6a
  Args:
    type: :Man
    source: Tsar_Alexander_III_of_Russia
  AssignClass (c5065f1b-af70-4dbd-8796-2307143a0d26)
 Call ID: c5065f1b-af70-4dbd-8796-2307143a0d26
  Args:
    type: :Woman
    source: Jeanne_Aumont-Lacroix
  AssignClass (6bb01fa2-ef0b-4e0f-a6eb-e82c9534649c)
 Call ID: 6bb01fa2-ef0b-4e0f-a6eb-e82c9534649c
  Args:
    type: :Man
    source: Jean_Boris_Lacroix
  AssignClass (3c495f71-5c1a-4f44-a417-21a37f08ff73)
 Call ID: 3c495f71-5c1a-4f44-a417-21a37f08ff73
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Alexandrovna
  AssignClass (ed352071-46af-4dab-aa62-79e43db78ec9)
 Call ID: ed352071-46af-4dab-aa62-79e43db78ec9
  Args:
    type: :Woman
    source: Victoria_Melita
  AssignClass (8768bdc1-0661-4606-bc65-fa7fea29b095)
 Call ID: 8768bdc1-0661-4606-bc65-fa7fea29b095
  Args:
    type: :Woman
    source: Princess_Victoria_Eugenia_of_Battenberg
  AssignClass (a7201d71-8b64-4c54-9f05-ded93bc45697)
 Call ID: a7201d71-8b64-4c54-9f05-ded93bc45697
  Args:
    type: :Man
    source: King_Alfonso_XIII_of_Spain
  AssignClass (05f96479-9c09-49fb-af3c-405550d78409)
 Call ID: 05f96479-9c09-49fb-af3c-405550d78409
  Args:
    type: :Woman
    source: Zinaida_Sergeievna_Rachevskaya
  AssignClass (477cbd58-1b79-419e-b882-b29501132b3f)
 Call ID: 477cbd58-1b79-419e-b882-b29501132b3f
  Args:
    type: :Man
    source: Colonel_Sergei_Alexandrovich_Rachevsky
  AssignClass (c18084fc-00b2-4f3d-ac60-e085bd0f8ab7)
 Call ID: c18084fc-00b2-4f3d-ac60-e085bd0f8ab7
  Args:
    type: :Man
    source: Peter_Eliseev
  AssignClass (d94e5372-feeb-4e60-8361-56fb414d66cd)
 Call ID: d94e5372-feeb-4e60-8361-56fb414d66cd
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AssignClass (7a541b2c-d7ce-4379-aa7e-5965d80399c8)
 Call ID: 7a541b2c-d7ce-4379-aa7e-5965d80399c8
  Args:
    type: :Man
    source: Grand_Duke_Michael_Alexandrovich_of_Russia
  AssignClass (92d6368d-8fa1-49d8-ab2d-fe74735cae7a)
 Call ID: 92d6368d-8fa1-49d8-ab2d-fe74735cae7a
  Args:
    type: :Man
    source: Grand_Duke_Andrei_Vladimirovich_of_Russia
  AssignClass (cb04e450-d7a7-4779-af01-a1375e6d5740)
 Call ID: cb04e450-d7a7-4779-af01-a1375e6d5740
  Args:
    type: :Woman
    source: Mathilde_Kschessinskaya

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .

  data:Colonel_Sergei_Alexandrovich_Rachevsky a :Man .

  data:Duchess_Marie_Alexandrine_of_Mecklenburg-Schwerin a :Woman .

  data:Grand_Duchess_Maria_Alexandrovna a :Woman .

  data:Grand_Duchess_Maria_Pavlovna a :Woman .

  data:Grand_Duke_Andrei_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Boris_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Kirill_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Michael_Alexandrovich_of_Russia a :Man .

  data:Grand_Duke_Vladimir_Alexandrovich_of_Russia a :Man .

  data:Jean_Boris_Lacroix a :Man .

  data:Jeanne_Aumont-Lacroix a :Woman .

  data:King_Alfonso_XIII_of_Spain a :Man .

  data:Mathilde_Kschessinskaya a :Woman .

  data:Peter_Eliseev a :Man .

  data:Princess_Victoria_Eugenia_of_Battenberg a :Woman .

  data:Tsar_Alexander_III_of_Russia a :Man .

  data:Tsar_Alexander_II_of_Russia a :Man .

  data:Tsar_Nicholas_II a :Man .

  data:Victoria_Melita a :Woman .

  data:Zinaida_Sergeievna_Rachevskaya a :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  AddLiteral (22f7eaee-46d2-4b36-8c90-455de9e40c0b)
 Call ID: 22f7eaee-46d2-4b36-8c90-455de9e40c0b
  Args:
    literal_type: xsd:integer
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    literal_value: 1877
    relation: :hasBirthYear
  AddLiteral (56dd8a73-7c56-4a50-992d-21ef803700ce)
 Call ID: 56dd8a73-7c56-4a50-992d-21ef803700ce
  Args:
    relation: :hasDeathYear
    literal_value: 1943
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    literal_type: xsd:integer
  AddTriple (ff605251-cc48-457f-9bda-4fc93eed099e)
 Call ID: ff605251-cc48-457f-9bda-4fc93eed099e
  Args:
    target: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (52028bad-c054-4b95-ba31-7be39e2f8b6c)
 Call ID: 52028bad-c054-4b95-ba31-7be39e2f8b6c
  Args:
    target: Grand_Duchess_Maria_Pavlovna
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    relation: :hasMother
  AddTriple (057d04c4-08a4-4ac4-8458-b076e657cd64)
 Call ID: 057d04c4-08a4-4ac4-8458-b076e657cd64
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    target: Tsar_Alexander_II_of_Russia
    relation: :hasFather
  AddTriple (3718fbf9-3e25-48cb-b405-3af3722888ee)
 Call ID: 3718fbf9-3e25-48cb-b405-3af3722888ee
  Args:
    relation: :isBrotherOf
    target: Tsar_Alexander_III_of_Russia
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AddTriple (daa6921a-5665-4286-9c01-282d61cdbf4d)
 Call ID: daa6921a-5665-4286-9c01-282d61cdbf4d
  Args:
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    target: Jean_Boris_Lacroix
    relation: :hasFather
  AddTriple (cbbfac0e-bb6f-4c92-b279-4858ab902e3c)
 Call ID: cbbfac0e-bb6f-4c92-b279-4858ab902e3c
  Args:
    target: Jeanne_Aumont-Lacroix
    source: Jean_Boris_Lacroix
    relation: :hasMother
  AddTriple (5009f622-06aa-4ad4-801e-f6dd2ac192d3)
 Call ID: 5009f622-06aa-4ad4-801e-f6dd2ac192d3
  Args:
    relation: :hasFather
    target: Colonel_Sergei_Alexandrovich_Rachevsky
    source: Zinaida_Sergeievna_Rachevskaya
  AddTriple (7fa723cf-55c9-4ade-bf54-c82bc4c7ef36)
 Call ID: 7fa723cf-55c9-4ade-bf54-c82bc4c7ef36
  Args:
    target: Grand_Duke_Kirill_Vladimirovich_of_Russia
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    relation: :hasBrother
  AddTriple (bed8f3de-8f99-41bb-939f-7a17b970e317)
 Call ID: bed8f3de-8f99-41bb-939f-7a17b970e317
  Args:
    target: Grand_Duke_Andrei_Vladimirovich_of_Russia
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    relation: :hasBrother

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Duchess_Marie_Alexandrine_of_Mecklenburg-Schwerin a :Woman .

  data:Grand_Duchess_Maria_Alexandrovna a :Woman .

  data:Grand_Duke_Boris_Vladimirovich_of_Russia a :Man ;
      :hasBirthYear 1877 ;
      :hasBrother data:Grand_Duke_Andrei_Vladimirovich_of_Russia,
          data:Grand_Duke_Kirill_Vladimirovich_of_Russia ;
      :hasDeathYear 1943 ;
      :hasFather data:Grand_Duke_Vladimir_Alexandrovich_of_Russia,
          data:Jean_Boris_Lacroix ;
      :hasMother data:Grand_Duchess_Maria_Pavlovna .

  data:Grand_Duke_Michael_Alexandrovich_of_Russia a :Man .

  data:King_Alfonso_XIII_of_Spain a :Man .

  data:Mathilde_Kschessinskaya a :Woman .

  data:Peter_Eliseev a :Man .

  data:Princess_Victoria_Eugenia_of_Battenberg a :Woman .

  data:Tsar_Nicholas_II a :Man .

  data:Victoria_Melita a :Woman .

  data:Zinaida_Sergeievna_Rachevskaya a :Woman ;
      :hasFather data:Colonel_Sergei_Alexandrovich_Rachevsky .

  data:Colonel_Sergei_Alexandrovich_Rachevsky a :Man .

  data:Grand_Duchess_Maria_Pavlovna a :Woman .

  data:Grand_Duke_Andrei_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Kirill_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Vladimir_Alexandrovich_of_Russia a :Man ;
      :hasFather data:Tsar_Alexander_II_of_Russia ;
      :isBrotherOf data:Tsar_Alexander_III_of_Russia .

  data:Jean_Boris_Lacroix a :Man ;
      :hasMother data:Jeanne_Aumont-Lacroix .

  data:Jeanne_Aumont-Lacroix a :Woman .

  data:Tsar_Alexander_III_of_Russia a :Man .

  data:Tsar_Alexander_II_of_Russia a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (54c60248-862c-4f22-8fed-2e5dc78b132e)
 Call ID: 54c60248-862c-4f22-8fed-2e5dc78b132e
  Args:
    relation: :hasFather
    target: Jean_Boris_Lacroix
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
  AddTriple (6993060d-e6f9-46b4-949e-92bb066005dc)
 Call ID: 6993060d-e6f9-46b4-949e-92bb066005dc
  Args:
    relation: :isFatherOf
    source: Grand_Duke_Boris_Vladimirovich_of_Russia
    target: Jean_Boris_Lacroix

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Duchess_Marie_Alexandrine_of_Mecklenburg-Schwerin a :Woman .

  data:Grand_Duchess_Maria_Alexandrovna a :Woman .

  data:Grand_Duke_Boris_Vladimirovich_of_Russia a :Man ;
      :hasBirthYear 1877 ;
      :hasBrother data:Grand_Duke_Andrei_Vladimirovich_of_Russia,
          data:Grand_Duke_Kirill_Vladimirovich_of_Russia ;
      :hasDeathYear 1943 ;
      :hasFather data:Grand_Duke_Vladimir_Alexandrovich_of_Russia ;
      :hasMother data:Grand_Duchess_Maria_Pavlovna ;
      :isFatherOf data:Jean_Boris_Lacroix .

  data:Grand_Duke_Michael_Alexandrovich_of_Russia a :Man .

  data:King_Alfonso_XIII_of_Spain a :Man .

  data:Mathilde_Kschessinskaya a :Woman .

  data:Peter_Eliseev a :Man .

  data:Princess_Victoria_Eugenia_of_Battenberg a :Woman .

  data:Tsar_Nicholas_II a :Man .

  data:Victoria_Melita a :Woman .

  data:Zinaida_Sergeievna_Rachevskaya a :Woman ;
      :hasFather data:Colonel_Sergei_Alexandrovich_Rachevsky .

  data:Colonel_Sergei_Alexandrovich_Rachevsky a :Man .

  data:Grand_Duchess_Maria_Pavlovna a :Woman .

  data:Grand_Duke_Andrei_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Kirill_Vladimirovich_of_Russia a :Man .

  data:Grand_Duke_Vladimir_Alexandrovich_of_Russia a :Man ;
      :hasFather data:Tsar_Alexander_II_of_Russia ;
      :isBrotherOf data:Tsar_Alexander_III_of_Russia .

  data:Jean_Boris_Lacroix a :Man ;
      :hasMother data:Jeanne_Aumont-Lacroix .

  data:Jeanne_Aumont-Lacroix a :Woman .

  data:Tsar_Alexander_III_of_Russia a :Man .

  data:Tsar_Alexander_II_of_Russia a :Man .



================================== Ai Message ==================================

[]
Tool Calls:
  Finish (8b8d066d-e201-4b79-8133-9bfd6e9883b3)
 Call ID: 8b8d066d-e201-4b79-8133-9bfd6e9883b3
  Args: