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
In 1896 during the coronation ceremonies of Tsar Nicholas II, he flirted with Crown Princess Marie of Romania, who was his first cousin and was already married.
She said that "he had an attractive, rather husky voice, kind eyes, and humorous smile, which crinkled his forehead into unexpected lines.
The grand duke also got entangled with a Mademoiselle Demidov.
The famous ballerina Anna Pavlova was one of Boris' lovers.
Princess Catherine Radziwill called him "the terror of jealous husbands as well as of watchful mothers".
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
  AssignClass (a7cc018f-838e-43f5-8481-df2491131b09)
 Call ID: a7cc018f-838e-43f5-8481-df2491131b09
  Args:
    type: :Man
    source: Grand Duke Boris Vladimirovich of Russia
  AssignClass (83818ead-76ec-4e6d-9e0d-9f41228b4c53)
 Call ID: 83818ead-76ec-4e6d-9e0d-9f41228b4c53
  Args:
    type: :Person
    source: Grand Duke Boris Vladimirovich of Russia
  AddLiteral (bafa996a-349e-418b-b820-4226f5432c31)
 Call ID: bafa996a-349e-418b-b820-4226f5432c31
  Args:
    literal_type: xsd:integer
    source: Grand Duke Boris Vladimirovich of Russia
    literal_value: 1877
    relation: :hasBirthYear
  AddLiteral (7191c985-f211-4c82-bb16-5b6ae40f1dd0)
 Call ID: 7191c985-f211-4c82-bb16-5b6ae40f1dd0
  Args:
    literal_type: xsd:integer
    source: Grand Duke Boris Vladimirovich of Russia
    literal_value: 1943
    relation: :hasDeathYear
  AssignClass (4005a371-0aa6-4c93-98bb-8c927e304348)
 Call ID: 4005a371-0aa6-4c93-98bb-8c927e304348
  Args:
    type: :Man
    source: Grand Duke Vladimir Alexandrovich of Russia
  AssignClass (07cb3368-5bdb-48eb-9db1-1b56a7cb91fd)
 Call ID: 07cb3368-5bdb-48eb-9db1-1b56a7cb91fd
  Args:
    type: :Person
    source: Grand Duke Vladimir Alexandrovich of Russia
  AssignClass (d3a64e27-c203-4601-935b-83ab8ef89fb6)
 Call ID: d3a64e27-c203-4601-935b-83ab8ef89fb6
  Args:
    type: :Woman
    source: Grand Duchess Maria Pavlovna
  AssignClass (60bef23b-dd3c-42ca-b0d1-e913a6ae625a)
 Call ID: 60bef23b-dd3c-42ca-b0d1-e913a6ae625a
  Args:
    type: :Person
    source: Grand Duchess Maria Pavlovna
  AddTriple (8d1dde65-7717-49fe-807c-9bea92930458)
 Call ID: 8d1dde65-7717-49fe-807c-9bea92930458
  Args:
    relation: :hasFather
    target: Grand Duke Vladimir Alexandrovich of Russia
    source: Grand Duke Boris Vladimirovich of Russia
  AddTriple (2f8461ad-837d-4397-8f71-ddb9022c3cb9)
 Call ID: 2f8461ad-837d-4397-8f71-ddb9022c3cb9
  Args:
    relation: :hasMother
    source: Grand Duke Boris Vladimirovich of Russia
    target: Grand Duchess Maria Pavlovna
  AssignClass (83d640d8-f70e-4fef-9138-330cb1e3967c)
 Call ID: 83d640d8-f70e-4fef-9138-330cb1e3967c
  Args:
    type: :Man
    source: Tsar Alexander II of Russia
  AssignClass (85a355a5-5905-4aed-bb27-13196bf41534)
 Call ID: 85a355a5-5905-4aed-bb27-13196bf41534
  Args:
    type: :Person
    source: Tsar Alexander II of Russia
  AddTriple (35b9be01-3fb8-4a5f-8920-ce7dfcc84d81)
 Call ID: 35b9be01-3fb8-4a5f-8920-ce7dfcc84d81
  Args:
    relation: :hasAncestor
    target: Tsar Alexander II of Russia
    source: Grand Duke Boris Vladimirovich of Russia
  AssignClass (a4565d12-8168-4a40-ad4c-26e7730c4388)
 Call ID: a4565d12-8168-4a40-ad4c-26e7730c4388
  Args:
    type: :Man
    source: Tsar Nicholas II
  AssignClass (e2f9e956-f872-4f21-bb72-de91bacbc5ed)
 Call ID: e2f9e956-f872-4f21-bb72-de91bacbc5ed
  Args:
    type: :Person
    source: Tsar Nicholas II
  AssignClass (5f385718-c26c-44e9-9264-244588d5c3ac)
 Call ID: 5f385718-c26c-44e9-9264-244588d5c3ac
  Args:
    type: :Man
    source: Grand Duke Kirill Vladimirovich
  AssignClass (855bda6c-93fe-47af-99da-28319fd70482)
 Call ID: 855bda6c-93fe-47af-99da-28319fd70482
  Args:
    type: :Person
    source: Grand Duke Kirill Vladimirovich
  AddTriple (8d39d5ea-8417-42eb-a780-4222266c5888)
 Call ID: 8d39d5ea-8417-42eb-a780-4222266c5888
  Args:
    source: Grand Duke Boris Vladimirovich of Russia
    target: Grand Duke Kirill Vladimirovich
    relation: :hasBrother
  AssignClass (49666f9d-5ba0-457f-a6f4-e51414987cbe)
 Call ID: 49666f9d-5ba0-457f-a6f4-e51414987cbe
  Args:
    type: :Man
    source: Grand Duke Andrei Vladimirovich
  AssignClass (44f219a0-67af-4e70-a280-b21190dd7798)
 Call ID: 44f219a0-67af-4e70-a280-b21190dd7798
  Args:
    type: :Person
    source: Grand Duke Andrei Vladimirovich
  AddTriple (089bfebd-7f4b-4bf6-907e-7fbd334f8a80)
 Call ID: 089bfebd-7f4b-4bf6-907e-7fbd334f8a80
  Args:
    target: Grand Duke Andrei Vladimirovich
    source: Grand Duke Boris Vladimirovich of Russia
    relation: :hasBrother
  AssignClass (0384319c-e5b5-46ae-85e0-720d29f40646)
 Call ID: 0384319c-e5b5-46ae-85e0-720d29f40646
  Args:
    type: :Man
    source: Jean Boris Lacroix
  AssignClass (09e11eed-ca47-4659-819a-986c850e0fed)
 Call ID: 09e11eed-ca47-4659-819a-986c850e0fed
  Args:
    type: :Person
    source: Jean Boris Lacroix
  AddTriple (0db77941-b205-4a8b-826c-c897d0488659)
 Call ID: 0db77941-b205-4a8b-826c-c897d0488659
  Args:
    relation: :isSonOf
    source: Jean Boris Lacroix
    target: Grand Duke Boris Vladimirovich of Russia
  AssignClass (8e4dbac0-d1db-4b01-ae67-ee0bd91ff5e6)
 Call ID: 8e4dbac0-d1db-4b01-ae67-ee0bd91ff5e6
  Args:
    type: :Woman
    source: Jeanne Aumont-Lacroix
  AssignClass (29bb5e90-eb6a-4e87-a0e2-3176b36f9f79)
 Call ID: 29bb5e90-eb6a-4e87-a0e2-3176b36f9f79
  Args:
    type: :Person
    source: Jeanne Aumont-Lacroix
  AddTriple (85c04740-9187-4e5a-901b-7112456098ba)
 Call ID: 85c04740-9187-4e5a-901b-7112456098ba
  Args:
    relation: :isMotherOf
    source: Jeanne Aumont-Lacroix
    target: Jean Boris Lacroix
  AssignClass (ad22e23e-c42d-4655-9b2b-3286e01f01e6)
 Call ID: ad22e23e-c42d-4655-9b2b-3286e01f01e6
  Args:
    type: :Woman
    source: Zinaida Sergeievna Rachevskaya
  AssignClass (abff22f9-f718-436f-88f9-c95f6b476c3f)
 Call ID: abff22f9-f718-436f-88f9-c95f6b476c3f
  Args:
    type: :Person
    source: Zinaida Sergeievna Rachevskaya
  AssignClass (1c21a248-645e-4961-8939-9f5922716350)
 Call ID: 1c21a248-645e-4961-8939-9f5922716350
  Args:
    type: :Man
    source: Colonel Sergei Alexandrovich Rachevsky
  AssignClass (dfe233e6-a1ea-4b63-ad3b-7a3965f13491)
 Call ID: dfe233e6-a1ea-4b63-ad3b-7a3965f13491
  Args:
    type: :Person
    source: Colonel Sergei Alexandrovich Rachevsky
  AddTriple (860143cf-d63a-42d6-bc95-97dadbf037f8)
 Call ID: 860143cf-d63a-42d6-bc95-97dadbf037f8
  Args:
    target: Colonel Sergei Alexandrovich Rachevsky
    source: Zinaida Sergeievna Rachevskaya
    relation: :isDaughterOf
  AssignClass (0df4800d-1c21-4be9-a0ee-73f0fe518b1d)
 Call ID: 0df4800d-1c21-4be9-a0ee-73f0fe518b1d
  Args:
    type: :Man
    source: Peter Eliseev
  AssignClass (dc7986d4-0fa5-46df-8f24-5cb0fd083b7d)
 Call ID: dc7986d4-0fa5-46df-8f24-5cb0fd083b7d
  Args:
    type: :Person
    source: Peter Eliseev
  Finish (89ef04b3-7964-4363-9acc-50e0ab5856b7)
 Call ID: 89ef04b3-7964-4363-9acc-50e0ab5856b7
  Args: