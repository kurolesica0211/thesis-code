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
  AssignClass (46af1902-d4f5-4e77-8af2-67180c7bfdd7)
 Call ID: 46af1902-d4f5-4e77-8af2-67180c7bfdd7
  Args:
    type: :Man
    source: Boris_Vladimirovich
  AssignClass (ab78fb6f-e33b-4a56-bbe8-106ceaa0f3dd)
 Call ID: ab78fb6f-e33b-4a56-bbe8-106ceaa0f3dd
  Args:
    type: :Person
    source: Boris_Vladimirovich
  AddLiteral (74485308-69e5-4b5e-9412-1ffd1bc2a739)
 Call ID: 74485308-69e5-4b5e-9412-1ffd1bc2a739
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Boris_Vladimirovich
    literal_value: 1877
  AddLiteral (70b69123-48cf-4c0c-9c0c-8ebf9d0f291e)
 Call ID: 70b69123-48cf-4c0c-9c0c-8ebf9d0f291e
  Args:
    source: Boris_Vladimirovich
    literal_value: 1943
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (87c7cfcd-f6fc-449f-b0b5-f48676cef822)
 Call ID: 87c7cfcd-f6fc-449f-b0b5-f48676cef822
  Args:
    type: :Man
    source: Vladimir_Alexandrovich
  AssignClass (8fc7007f-e835-4bc8-8cb4-2a1d333f4a42)
 Call ID: 8fc7007f-e835-4bc8-8cb4-2a1d333f4a42
  Args:
    type: :Person
    source: Vladimir_Alexandrovich
  AssignClass (ca85dc99-20b8-4bf9-9f21-07aca2277e3c)
 Call ID: ca85dc99-20b8-4bf9-9f21-07aca2277e3c
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (7bdb3f8b-c0f2-4706-8fce-fcaf3b8177f2)
 Call ID: 7bdb3f8b-c0f2-4706-8fce-fcaf3b8177f2
  Args:
    type: :Person
    source: Maria_Pavlovna
  AddTriple (0be4de39-7198-4d58-b757-bde53acd1896)
 Call ID: 0be4de39-7198-4d58-b757-bde53acd1896
  Args:
    relation: :hasFather
    target: Vladimir_Alexandrovich
    source: Boris_Vladimirovich
  AddTriple (21f4f147-ca0b-4c24-84f3-7f3f3de3d46f)
 Call ID: 21f4f147-ca0b-4c24-84f3-7f3f3de3d46f
  Args:
    source: Boris_Vladimirovich
    relation: :hasMother
    target: Maria_Pavlovna
  AssignClass (968d07a0-ce60-4cd0-9264-1e63d9ff04b5)
 Call ID: 968d07a0-ce60-4cd0-9264-1e63d9ff04b5
  Args:
    type: :Man
    source: Alexander_II
  AssignClass (8570b7a4-7aec-4829-b264-0af1fe9d36fc)
 Call ID: 8570b7a4-7aec-4829-b264-0af1fe9d36fc
  Args:
    type: :Person
    source: Alexander_II
  AssignClass (cf18306a-6c35-4232-a7af-ab3d0b2a263b)
 Call ID: cf18306a-6c35-4232-a7af-ab3d0b2a263b
  Args:
    type: :Man
    source: Nicholas_II
  AssignClass (28603378-de21-4f77-9b94-1e524349f6db)
 Call ID: 28603378-de21-4f77-9b94-1e524349f6db
  Args:
    type: :Person
    source: Nicholas_II
  AssignClass (721d6845-f534-4658-8ac9-a6b53aaaadf1)
 Call ID: 721d6845-f534-4658-8ac9-a6b53aaaadf1
  Args:
    type: :Man
    source: Alexander_III
  AssignClass (9c62a05c-eea4-4812-8ab9-debc331f395a)
 Call ID: 9c62a05c-eea4-4812-8ab9-debc331f395a
  Args:
    type: :Person
    source: Alexander_III
  AddTriple (5e3a7766-3de7-4305-9ffd-aec88a1bdf66)
 Call ID: 5e3a7766-3de7-4305-9ffd-aec88a1bdf66
  Args:
    source: Vladimir_Alexandrovich
    relation: :hasFather
    target: Alexander_II
  AddTriple (17d1b212-817f-4daf-9264-02845eca9e7f)
 Call ID: 17d1b212-817f-4daf-9264-02845eca9e7f
  Args:
    source: Vladimir_Alexandrovich
    relation: :hasBrother
    target: Alexander_III
  AssignClass (b17f57e1-1c46-40ac-8a1b-b1449b23ff89)
 Call ID: b17f57e1-1c46-40ac-8a1b-b1449b23ff89
  Args:
    type: :Man
    source: Jean_Boris_Lacroix
  AssignClass (8c0cc0ae-094b-4d23-aa31-61189bcf84e5)
 Call ID: 8c0cc0ae-094b-4d23-aa31-61189bcf84e5
  Args:
    type: :Person
    source: Jean_Boris_Lacroix
  AssignClass (4bd2ff50-af4d-445e-b425-0f24ae057231)
 Call ID: 4bd2ff50-af4d-445e-b425-0f24ae057231
  Args:
    type: :Woman
    source: Jeanne_Aumont-Lacroix
  AssignClass (01a43344-56bd-4a3b-b8e6-ec1178fc1179)
 Call ID: 01a43344-56bd-4a3b-b8e6-ec1178fc1179
  Args:
    type: :Person
    source: Jeanne_Aumont-Lacroix
  AddTriple (f6559f08-aeca-481f-adec-6f7cbb3415ed)
 Call ID: f6559f08-aeca-481f-adec-6f7cbb3415ed
  Args:
    target: Jean_Boris_Lacroix
    relation: :isFatherOf
    source: Boris_Vladimirovich
  AddTriple (b4f3bfb6-9cc6-4a99-bd8c-3f4b1477f4f1)
 Call ID: b4f3bfb6-9cc6-4a99-bd8c-3f4b1477f4f1
  Args:
    target: Jean_Boris_Lacroix
    relation: :isMotherOf
    source: Jeanne_Aumont-Lacroix
  AssignClass (7ef053c6-50ed-4bdc-84a6-2b020a66db51)
 Call ID: 7ef053c6-50ed-4bdc-84a6-2b020a66db51
  Args:
    type: :Man
    source: Kirill_Vladimirovich
  AssignClass (c8c89892-4f53-4700-8f73-e9cfd7d0c61f)
 Call ID: c8c89892-4f53-4700-8f73-e9cfd7d0c61f
  Args:
    type: :Person
    source: Kirill_Vladimirovich
  AddTriple (9ca206cb-ac0e-4353-9d4d-52b315a89e8d)
 Call ID: 9ca206cb-ac0e-4353-9d4d-52b315a89e8d
  Args:
    source: Boris_Vladimirovich
    relation: :hasBrother
    target: Kirill_Vladimirovich
  AssignClass (0153fd0b-cb2d-498c-a1d3-06689b931d85)
 Call ID: 0153fd0b-cb2d-498c-a1d3-06689b931d85
  Args:
    type: :Man
    source: Andrei_Vladimirovich
  AssignClass (5fd6a5a4-ee39-45ac-9183-92c5226e348c)
 Call ID: 5fd6a5a4-ee39-45ac-9183-92c5226e348c
  Args:
    type: :Person
    source: Andrei_Vladimirovich
  AddTriple (dd1ce5d7-6c3c-4cd6-849a-f7f1894da102)
 Call ID: dd1ce5d7-6c3c-4cd6-849a-f7f1894da102
  Args:
    target: Andrei_Vladimirovich
    relation: :hasBrother
    source: Boris_Vladimirovich
  AssignClass (fed7556b-eff2-4049-9e3b-526853ae770d)
 Call ID: fed7556b-eff2-4049-9e3b-526853ae770d
  Args:
    type: :Woman
    source: Zinaida_Sergeievna_Rachevskaya
  AssignClass (350686d9-06fc-4e3a-8d8e-c0aeb4e5586f)
 Call ID: 350686d9-06fc-4e3a-8d8e-c0aeb4e5586f
  Args:
    type: :Person
    source: Zinaida_Sergeievna_Rachevskaya
  AssignClass (e3cf8a58-0283-4beb-8fbb-9caae41bcfab)
 Call ID: e3cf8a58-0283-4beb-8fbb-9caae41bcfab
  Args:
    type: :Man
    source: Sergei_Alexandrovich_Rachevsky
  AssignClass (bf248341-b5c8-4fa4-8c39-9b5f5d12f99b)
 Call ID: bf248341-b5c8-4fa4-8c39-9b5f5d12f99b
  Args:
    type: :Person
    source: Sergei_Alexandrovich_Rachevsky
  AddTriple (f7ff38a0-dac5-430a-abdd-4654255025a9)
 Call ID: f7ff38a0-dac5-430a-abdd-4654255025a9
  Args:
    source: Zinaida_Sergeievna_Rachevskaya
    relation: :hasFather
    target: Sergei_Alexandrovich_Rachevsky
  Finish (b24e6fc5-90f1-4298-9470-f47559a2944c)
 Call ID: b24e6fc5-90f1-4298-9470-f47559a2944c
  Args: