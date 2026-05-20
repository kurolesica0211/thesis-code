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
Grand Duchess Maria Pavlovna of Russia (Russian: Мари́я Па́вловна Романова, romanized: Mariya Pavlovna Romanova; born Duchess Marie of Mecklenberg-Schwerin 14
May  1854 – 6 September 1920), was the eldest daughter of Grand Duke Friedrich Franz II of Mecklenburg-Schwerin and his first wife, Princess Augusta Reuss of Köstritz.
A prominent hostess in Saint Petersburg following her marriage in 1874 to the Grand Duke Vladimir Alexandrovich of Russia, she was known by many as the "grandest of the grand duchesses".
Appearance and personality

Marie was noted for her attractiveness and sense of style.
When Prince Arthur, Duke of Connaught and Strathearn visited Germany in search of brides, Queen Victoria noted that Marie was "said to be very pretty."
When they first met, her future husband Grand Duke Vladimir Alexandrovich of Russia admired her "wonderfully expressive eyes."
At her wedding, Thomas W. Knox observed that "Vladimir's bride is good-looking, solid, well-formed, with plump and finely rounded shoulders; a neck neither long nor short; regularly formed features, with the exception of the nose, which has a slight tendency to pugginess."
At the coronation of her brother-in-law Alexander III, her niece, Marie of Edinburgh, noted that "she is not thin enough for classical lines but she wears her clothes better than any other woman present; her shoulders are superb and as white as cream; there is a smartness about her that no one else can attain."
In 1910, author Elinor Glyn wrote that Marie was "a most stately, magnificent looking princess.
"


Marie was famous for her wittiness and sociability.
Meriel Buchanan attended one of Marie's dinner parties at Vladimir Palace, and she wrote that Marie "know exactly what to say to each individual person, an inimitable gift which royalties do not always possess, but which she had at her command in the fullest sense."
He wrote: "For three hours, the Grand Duchess was the centre of the animated and brilliant conversation.
Author Elinor Glyn reflected that Marie "had a very highly cultivated and far-seeing mind, with a delightful sense of humour, and was adored by everyone.
"


Marie was interested in literature.
In late 1909, she invited the popular British novelist Elinor Glyn to come to Russia to write a Russian-based story.
Glyn produced a piece of fiction called His Hour, which she dedicated to Marie, saying "her kind appreciation of the finished work is a source of the deepest gratification to me."
Glyn modeled one of the characters, Princess Ardacheff, after Marie.
Like her husband, Marie loved the arts.
After her husband's death, Marie succeeded him as president of the Academy of Fine Arts.
Marie was addicted to gambling.
The painter Henry Jones Thaddeus attended one of Marie's parties, where she insisted that her guests play roulette.
Early life

Marie Alexandrine Elisabeth Eleonore was born a duchess of the Grand Ducal House of Mecklenburg to Frederick Francis II, Grand Duke of Mecklenburg-Schwerin - the then Grand Duke of Mecklenburg-Schwerin and his first wife, Princess Augusta Reuss of Köstritz (1822–1862) - in the Schloss Ludwigslust.
Marriage

Marie married Grand Duke Vladimir Alexandrovich of Russia, the third son of Alexander II of Russia.
Previously, she had been engaged to George Albert I, Prince of Schwarzburg-Rudolstadt, but broke it off as soon as she met Vladimir.
Marie and Vladimir married on 28 August 1874.
It was not as lavish as the wedding of Vladimir's sister Grand Duchess Maria Alexandrovna of Russia to the Duke of Edinburgh.
Lord Augustus Loftus noted, "Every thing went off very well; although the marriage was not so resplendent as that of the Duke of Edinburgh.
"


As the Russian Emperor's daughter-in-law, Marie took on a new style Her Imperial Highness.
Marie and Vladimir had four sons and one daughter.
She was Emperor Paul I of Russia's great-great-granddaughter, and she wished to emphasize her exalted ancestry with the patronymic "Pavlovna.
"


Religion

For three years, Marie and Vladimir could not marry, because Marie refused to convert from Lutheranism to the Russian Orthodox Church.
Vladimir's mother, Empress Maria Alexandrovna was disappointed by Marie's refusal to convert: She herself had converted from Lutheranism to Russian Orthodoxy, and she thought that the Russian Orthodox church was "quite good enough for any daughter-in-law of hers."
She told Vladimir that she hoped that Marie would "become Russian in body and soul," indicating her hope that Marie would convert.
Emperor Alexander II finally agreed to let Vladimir marry Marie without insisting on her conversion to Orthodoxy.
Every bride of a Russian grand duke needed to convert to Russian Orthodoxy before Marie, so Marie's decision was shocking and unprecedented.
Lord Augustus Loftus noted: "It is a matter of surprise here for a Foreign Princess married to a grand duke to retain her own religion but it is a process to which they will have to accustom themselves or they will find no wives for the Russian grand dukes.
In a letter to Hamilton Fish, Eugene Schuyler wrote "The Grand Duchess will retain the Lutheran religion.
This is worthy of note, as hitherto the Russian laws have required the wives of all grand dukes to adopt the orthodox Russian faith.
"


Marie set the precedent for brides who did not have to convert to Russian Orthodoxy to marry Russian grand dukes.
At the time of Marie's marriage, Alice, Grand Duchess of Hesse and by Rhine wrote to her mother, Queen Victoria, "My mother-in-law tells me that since Miechen has been allowed to retain her religion, this right will of course be conceded to all Princesses in the future."
Many years later, Alice's daughter Princess Elisabeth of Hesse and by Rhine would use Marie's precedent to retain her Lutheran faith and marry Marie's brother-in-law, Grand Duke Sergei Alexandrovich of Russia.
Marie was furious when her sister-in-law Grand Duchess Elizabeth Feodorovna of Russia converted to Russian Orthodoxy after her marriage.
Grand Duchess Elizabeth predicted Marie's response, and she asked her father Louis IV, Grand Duke of Hesse and by Rhine: "Please do not yet tell anybody at Darmstadt until I write again when Miechen  knows.
"


In 1908, Marie converted to Orthodoxy.
Meriel Buchanan, daughter of a British ambassador to Russia, defended Marie's conversion as sincere: "For some time past the Grand Duchess had turned more and more to the colour and ceremonial of the Russian Church.
However, some believed that the ambitious Marie acted to improve the chances of her own sons ascending the throne.
After Emperor Nicholas II's sickly son Tsesarevich Alexei and unmarried, childless brother Grand Duke Michael Alexandrovich of Russia, Marie's husband and her sons were in line for the throne.
In 1916, Vladimir Purishkevich wrote in his diary: "I shall never forget the story of Ivan Grigorevich Scheglovitov, former Minister of Justice.
He said that one day Grand Duke Boris Vladimirovich asked him whether the descendants of the Vladimir line have any legal rights to the throne and if not, why not?
Scheglovitov... told him that the Grand Dukes had no rights whatsoever because their mother continued in the Lutheran faith even after marriage.
Boris left him but came back sometime later with a paper showing that the Grand Duchess had given up her Protestant religion and had embraced the Orthodox.
"


Life in Russia

Marie lived at the Vladimir Palace situated on the Palace Embankment on the Neva River.
Marie was famous for being one of the best hostesses in the capital.
During the reign of her nephew Emperor Nicholas II, her Grand Ducal court was the most cosmopolitan and popular one in the capital.
Meriel Buchanan attended Marie's dinner party at Vladimir Palace, and she wrote, "Here one always met only the prettiest and smartest women, the most distinguished men, the most entertaining members of the diplomatic body.
"


During Alexander II's reign, Marie survived the Winter Palace explosion of February 1880.
"


Marie was close to her father-in-law, Alexander II.
She resented him for forcing his family to accept Catherine, and she expressed her anger in a letter to the late Empress Maria's brother, Louis III, Grand Duke of Hesse and by Rhine: "The Tsar has commanded us as his subjects to be friendly with this wife; if not he would force us to it.
"


Marie had a distant relationship with her sister-in-law, Maria Feodorovna.
Maria Feodorovna disliked Marie because of her German origins.
Marie openly declared that her husband would make a better Emperor than Maria Feodorovna's husband, Alexander III of Russia.
After the Borki train disaster in which Alexander III, Maria Feodorovna, and their children narrowly escaped death, Marie allegedly said, "We shall never have such a chance again.
"


Marie had an antagonistic relationship with Emperor Nicholas II and Empress Alexandra, because of her ambitions for her own sons.
On 14 June 1897, the Boston Daily Globe reported that she had "consulted a gypsy fortune teller, who had predicted that one of her sons would sit on the throne of Russia."
At this time, Empress Alexandra had given birth to her second daughter Grand Duchess Tatiana.
As girls were ineligible for the Imperial Throne, Emperor Nicholas' heirs were his two unmarried, childless brothers and his uncle Vladimir, Marie's husband.
In 1912, Emperor Nicholas's only living brother Grand Duke Michael married a commoner, which led Emperor Nicholas to strip him of his military command, imperial honors, and right as the heir presumptive to serve as regent for Tsesarevich Alexei should Emperor Nicholas die prematurely.
According to the laws of the succession, Marie's oldest son Kirill, the heir presumptive now that Grand Duke Michael was ineligible and his own father, Vladimir, was dead, would become regent should the Emperor die before Alexei turned 21.
However, Emperor Nicholas overruled the existing law and nominated his oldest daughter Grand Duchess Olga as regent with his wife Empress Alexandra as guardian during Alexei's minority.
Marie was furious, but Emperor Nicholas refused to change his mind.
In 1916, Marie approached Empress Alexandra about a potential marriage between Grand Duchess Olga and her second son Grand Duke Boris Vladimirovich.
Empress Alexandra refused Marie's proposal, claiming that she could not let "a pure, fresh girl, 18 years his junior" marry a "well used, half worn out, blasé young man."
Marie was outraged by Empress Alexandra's abrupt refusal.
In 1909, Marie's husband died.
During World War I, Marie whole-heartedly supported Russia.
Born a German princess, she was troubled by the outbreak of WW I but decided that she was now a Russian.
it is my forty years’ residence in Russia— all the happiness I have known here, all the dreams that have come to me, all the affection and kindness I have received— which has given me a wholly Russian soul."
The French ambassador Maurice Paléologue was impressed by Marie's "long diatribe which made me feel all the sentiments of inveterate hatred, of mute and  tenacious detestation which the small and once independent states of Germany have for the despotic house of Prussia.
"


Marie supervised many projects for the Russian army.
Albert Stopford admired Marie's efficiency and skill in organizing, claiming that Marie "spar herself no trouble" and was "quite thorough."
Like many other Romanovs, Marie feared that Empress Alexandra would "be the sole ruler of Russia" after Nicholas took supreme command of the Russian armies on 23 August 1915 (O.S.), hoping this would lift morale.
It was widely speculated that along with her sons, she contemplated a coup against the Emperor in the winter of 1916–17, that would force the Tsar's abdication and replacement by his son Tsesarevich Alexei, and her son, Grand Duke Kirill or Grand Duke Nicholas Nikolaevich, as regent.
Escape from Russia

Marie was the last of the Romanovs to escape Revolutionary Russia and the first to die in exile.
Maria spent fourteen months in Anapa, refusing to join her son Boris in leaving Russia.
Maria, her son Andrei, Andrei's mistress Mathilde Kschessinska, and Andrei and Mathilde's son Vladimir, boarded an Italian ship headed to Venice on 13 February 1920.
Grand Duchess Olga Alexandrovna of Russia encountered Maria at the port of Novorossiysk in early 1920: "Disregarding peril and hardship, she stubbornly kept to all the trimmings of bygone splendour and glory.
Jewels

Marie had a passion for jewels, and her collection was renowned.
In 1899, she and Vladimir received a number of jewels for their silver wedding anniversary.
Nicholas II of Russia and Alexandra Feodorovna (Alix of Hesse) gave them "an aigrette and diadem composed of magnificent diamonds."
Each grand duke and grand duchess gave them a golden plate, which formed a collection of 36 plates, "the most magnificent service that can be imagined."
Marie was a major client of Cartier, and she bought many jewels from them.
Following the Revolution, a family friend Albert Stopford rescued the jewels from her Palace safe and smuggled them out of Russia.
After the Duchess's death, they were sold by her children to support their lives in exile.
Queen Mary, Queen Consort of the United Kingdom purchased a Bolin tiara of diamond loops with pearl drops, later worn by Queen Elizabeth II, although the original gold frame has been replaced by Garrard with one of platinum; Her niece by marriage, Queen Marie, Queen Consort of Romania purchased a sapphire kokoshnik-style tiara by Cartier and Nancy Leeds (later Princess Christopher of Greece), the ruby parure.
It had been rumored that some of the stones in Elizabeth Taylor's Bulgari Emerald necklace were from the Vladimir collection but this has been disproved by jeweler historian Vincent Meylan.
In 2008 a collection of cufflinks, cigarette cases and other small jewellery items belonging to the Vladimir family were discovered in the archives of the Swedish foreign ministry, having presumably been deposited at the Swedish Embassy in St Petersburg following the Revolution.
They were sold on behalf of the Vladimir heirs; some of the proceeds were used to restore the Grand Duchess's tomb in Contrexéville.
Children

Marie's eldest surviving son, Grand Duke Cyril Vladimirovich, married, in 1905, his first cousin Victoria Melita of Saxe-Coburg and Gotha, daughter of Vladimir's sister, the Duchess of Edinburgh and of Saxe-Coburg and Gotha.
Other than the fact that first cousin marriages were not allowed, she was also the former wife of Ernst Louis, Grand Duke of Hesse, the brother of the Empress.
However, after several deaths in the family put Cyril third in the line of succession to the Imperial Throne, Nicholas agreed to reinstate Cyril's Imperial titles, and the latter's wife was acknowledged as HIH Grand Duchess Viktoria Fedorovna.
Marie was a doting grandmother.
Marie's favorite was Princess Marina of Greece and Denmark.
Meriel Buchanan heard Marie say "Marina is the cleverest one," "Marina has the sweetest nature," and "Marina is the most affectionate."
Marie gave her granddaughters "dresses, dolls, prams, bicycles, a pony and carriage and jewellery suitable for their ages, such as silver muff-chains, watches, strings of pearls and diamonds and turquoise pendants".
During the First Balkan War, Elena sent her daughters to Paris to stay with Marie.
Marie took her granddaughters out for drives in the Bois de Boulogne, showed them off to her French friends, took them to see puppet shows, and gave them numerous "toys, presents, and chic new dresses".



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
  AssignClass (1b524faa-7031-4f35-ac29-7656c3533259)
 Call ID: 1b524faa-7031-4f35-ac29-7656c3533259
  Args:
    source: Maria_Pavlovna_of_Russia
    type: :Woman
  AssignClass (b3a3a3cc-c596-447c-867d-7fe8923e0443)
 Call ID: b3a3a3cc-c596-447c-867d-7fe8923e0443
  Args:
    source: Friedrich_Franz_II_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (94277de8-1cc1-4ba6-9293-174528d51937)
 Call ID: 94277de8-1cc1-4ba6-9293-174528d51937
  Args:
    source: Augusta_Reuss_of_Köstritz
    type: :Woman
  AssignClass (e6cea145-c99f-4ae3-b30c-5ff6e99933f1)
 Call ID: e6cea145-c99f-4ae3-b30c-5ff6e99933f1
  Args:
    type: :Man
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (4a40020d-54eb-4e4d-b52c-27653814e8d6)
 Call ID: 4a40020d-54eb-4e4d-b52c-27653814e8d6
  Args:
    source: Alexander_II_of_Russia
    type: :Man
  AddLiteral (77843d30-721c-4b7d-adc3-131f3767d2f1)
 Call ID: 77843d30-721c-4b7d-adc3-131f3767d2f1
  Args:
    literal_value: 1854
    literal_type: xsd:integer
    source: Maria_Pavlovna_of_Russia
    relation: :hasBirthYear
  AddLiteral (5fb09892-8174-4010-a179-8bf2631d00d7)
 Call ID: 5fb09892-8174-4010-a179-8bf2631d00d7
  Args:
    literal_value: 1920
    literal_type: xsd:integer
    source: Maria_Pavlovna_of_Russia
    relation: :hasDeathYear
  AddTriple (b13331a7-3f30-4d4a-a1c3-87a39a622ff8)
 Call ID: b13331a7-3f30-4d4a-a1c3-87a39a622ff8
  Args:
    source: Maria_Pavlovna_of_Russia
    relation: :hasFather
    target: Friedrich_Franz_II_of_Mecklenburg-Schwerin
  AddTriple (02955377-986e-41c9-9c8e-b3da23ef2169)
 Call ID: 02955377-986e-41c9-9c8e-b3da23ef2169
  Args:
    source: Maria_Pavlovna_of_Russia
    relation: :hasMother
    target: Augusta_Reuss_of_Köstritz
  AddTriple (b964238b-2d6f-4647-a03a-6e6f519c9050)
 Call ID: b964238b-2d6f-4647-a03a-6e6f519c9050
  Args:
    source: Vladimir_Alexandrovich_of_Russia
    relation: :hasFather
    target: Alexander_II_of_Russia
  AddLiteral (ea92479f-8f99-4bf4-aef1-eba41bd78ca9)
 Call ID: ea92479f-8f99-4bf4-aef1-eba41bd78ca9
  Args:
    source: Maria_Pavlovna_of_Russia
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1874
  AddTriple (210301cc-4df5-45d7-817e-f8c0a10c64e6)
 Call ID: 210301cc-4df5-45d7-817e-f8c0a10c64e6
  Args:
    source: Maria_Pavlovna_of_Russia
    relation: :hasRelation
    target: Vladimir_Alexandrovich_of_Russia
  Finish (f3ea8bd5-4475-4306-8413-aca794091b68)
 Call ID: f3ea8bd5-4475-4306-8413-aca794091b68
  Args: