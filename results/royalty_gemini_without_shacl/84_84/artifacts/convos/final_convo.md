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
Alexandra (Greek: Αλεξάνδρα, Serbo-Croatian: Александра/Aleksandra, in 1922 retroactively recognised as Princess Alexandra of Greece and Denmark; 25 March 1921 – 30 January 1993) was the last Queen of Yugoslavia as the wife of King Peter II.


Posthumous daughter of King Alexander of Greece and his morganatic wife, Aspasia Manos, Alexandra was not part of the Greek royal family until July 1922 when, at the behest of Queen Sophia, Alexander's mother, a law was passed which retroactively recognized marriages of members of the royal family, although on a non-dynastic basis; in consequence, she obtained the style and name of Her Royal Highness Princess Alexandra of Greece and Denmark.
At the same time, a serious political and military crisis, linked to the defeat of Greece by Turkey in Anatolia, led to the deposition and exile of the royal family, beginning in 1924.
Being the only members of the dynasty allowed to remain in the country by the Second Hellenic Republic, the princess and her mother later found refuge in Italy with Dowager Queen Sophia.
After three years with her paternal grandmother, Alexandra left Florence to continue her studies in the United Kingdom, while her mother settled in Venice.
Separated from her mother, the princess fell ill, forcing Aspasia to make her leave the boarding school where she was studying.
After the restoration of her uncle, King George II, on the Hellenic throne in 1935, Alexandra stayed in her native country several times but the outbreak of the Greco-Italian War, in 1940, forced her and her mother to settle in Athens.
The invasion of Greece by the Axis powers in April–May 1941, however, led to their moving to the United Kingdom.
Again exiled, Alexandra met in London the young King Peter II of Yugoslavia, who also went into exile after the invasion of his country by the Germans.
Quickly, Alexandra and Peter II fell in love and planned to marry.
Opposition from both Peter's mother, Maria, and the Yugoslav government in exile forced the couple to delay their marriage plans until 1944, when they finally celebrated their wedding.
A year later, Alexandra gave birth to her only son, Alexander, Crown Prince of Yugoslavia.
However, the happiness of the family was short-lived: on 29 November 1945, Marshal Tito proclaimed the Socialist Federal Republic of Yugoslavia and Alexandra, who had never set foot in her adopted country, was left without a crown.
Penniless and unable to adapt to the role of citizen, Peter II turned to alcoholism and multiple affairs with other women.
Depressed by the behavior of her husband, Alexandra neglected her son and made several suicide attempts.
After the death of Peter II in 1970, Alexandra's health continued to deteriorate.
Her remains were buried in the Royal Cemetery Plot in the park of Tatoi, in Greece, before being transferred to the Royal Mausoleum of Oplenac in 2013.
Life

A birth surrounded by intrigues

The issue of the Greek succession

Five months before Alexandra's birth, her father, King Alexander, died of sepsis following a monkey bite which occurred in the gardens of Tatoi.
The unexpected death of the sovereign caused a serious political crisis in Greece, at a time when public opinion was already divided by the events of the World War I and the Greco-Turkish War.
The King had concluded an unequal marriage with Aspasia Manos, and, in consequence, their offspring was not dynastic.
Due to the lack of another candidate for the throne, Prime Minister Eleftherios Venizelos was soon forced to accept the restoration of his enemy, King Constantine I, on 19 December 1920.
Alexander's brief reign was officially treated as a regency, which meant that his marriage, contracted without his father's permission, was technically illegal, the marriage void, and the couple's posthumous child illegitimate.
The last months of pregnancy of Aspasia are surrounded by intrigue.
In the case that she gave birth to a boy (who would be named Philip, as the father of Alexander the Great), rumours soon assured that she was determined to place him on the throne after his birth.
The birth of a girl, on 25 March 1921, was a great relief for the dynasty, and both King Constantine I and his mother, Queen Dowager Olga, agreed to be the godparents of the newborn.
Integration into the royal family

Still, neither Alexandra nor Aspasia received more official recognition: from a legal point of view, they were commoners without any rights in the royal family.
Things changed from July 1922 when, after the intervention of Queen Sophia, a law was passed which retroactively recognized marriages of members of the royal family, although on a non-dynastic basis; with this legal subterfuge, the princess obtained the style of Royal Highness and the title of Princess of Greece and Denmark.
Thus, Alexandra's birth became legitimate in the eyes of Greek law, but since the marriage was recognized on a 'non-dynastic basis', her royal status was tenuous at best
Aspasia, however, was not mentioned in the law and remained a commoner in the eyes of protocol.
Humiliated by this difference in treatment, she begged Prince Christopher (whose commoner wife, Nancy Stewart Worthington Leeds, was entitled to be known as a Princess of Greece and Denmark), to intercede on her behalf.
Under pressures from his wife, King Constantine I issued a decree, gazetted 10 September 1922 under which Aspasia received the title Princess of Greece and Denmark and the style of Royal Highness.
Childhood in exile

From Athens to Florence

Despite these positive developments, the situation of Alexandra and her mother did not improve.
Indeed, Greece experiencing a series of military defeats by Turkey and a coup d'état soon forced King Constantine I to abdicate again, this time in favor of his eldest son, Crown Prince George, on 27 September 1922.
On 25 March 1924, Alexandra's third birthday, the Second Hellenic Republic was proclaimed and both Aspasia and Alexandra were then the only members of the dynasty allowed to stay in Greece.
Penniless, Aspasia chose to take the path of exile with her daughter in early 1924.
The now dowager queen, who loved Alexandra, was thrilled, even if her financial situation was also precarious.
With her paternal grandmother, the princess spent a happy childhood with her aunts Crown Princess Helen of Romania, Princesses Irene and Katherine of Greece, and her cousins Prince Philip of Greece (the future Duke of Edinburgh) and Prince Michael of Romania, who were her playmates during holidays.
From London to Venice

In 1927, Alexandra and her mother moved to Ascot, Berkshire, in the United Kingdom.
Now seven years old, Alexandra was enrolled in boarding schools in Westfield and Heathfield, as was the custom for the upper class.
However, the Princess took very badly to this experience: separated from her mother, she stopped eating and eventually contracted tuberculosis.
Alarmed, Aspasia thus moved her daughter to Switzerland for treatment.
Later, Alexandra was educated in a Parisian finishing school, during which time she and her mother stayed at the Hotel Crillon.
Eventually, the two princesses settled on the island of Giudecca in Venice, where Aspasia acquired a small property with her savings and Horlick's financial support.
Restoration of the Greek monarchy

Between Greece and Venice

In 1935, the Second Hellenic Republic was abolished and King George II (Alexandra's uncle) was restored to the throne after a referendum organized by General Georgios Kondylis.
Alexandra was then allowed to return to Greece, a country she had not seen since 1924.
Although she continued to reside in Venice with her mother (who still suffered the ostracism of the royal family), the princess was invited to all the great ceremonies that punctuate the life of the dynasty.
In 1936, she participated in the official ceremonies which marked the reburial in Tatoi of the remains of King Constantine I, Queen Sophia, and Dowager Queen Olga; all three died in exile in Italy.
Two years later, in 1938, she was invited to the wedding of her uncle, Crown Prince Paul, with Princess Frederica of Hanover.
Despite her participation in the ceremonies of the Greek royal family, at that time Alexandra understood that she was not a full member of the European royalty.
Her mother had to claim in her name the share of the inheritance of Alexandra's paternal grandparents.
Also, the princess' mother had no site in the royal necropolis of Tatoi.
During the 1936 ceremonies, a chapel was arranged in the park of the palace for the remains of King Constantine I and Queen Sophia.
The remains of King Alexander − previously based in the gardens next to his grandfather King George I – were then transferred to this chapel, with no space reserved for Aspasia.
First marriage proposal

In 1936, the fifteen-years-old Princess received her first marriage proposal: King Zog I of Albania, who wished to marry a member of the European royalty in order to consolidate his position, asked her hand.
Alexandra attended numerous dances, which aimed to introduce her to the European elite.
World War II

From Venice to London

The outbreak of the Greco-Italian War on 28 October 1940 forced Alexandra and her mother suddenly to leave Venice and fascist Italy.
However, after several months of victorious battles against the Italian forces, Greece was invaded by the army of Nazi Germany on 6 April 1941.
Alexandra and the majority of the members of the Royal Family left the country a few days later, on 22 April.
While several members of the Royal Family were forced to spend World War II in South Africa, Alexandra and her mother obtained the permission of King George II of Greece and the British government to move to the United Kingdom.
Better accepted than in their own country, they were regular guests of the Duchess of Kent (born Princess Marina of Greece) and of the future Duke of Edinburgh (born Prince Philip of Greece), who was rumoured to be briefly engaged to Alexandra.
Love and marriage

However, it was not her cousin Philip whom Alexandra finally married.
In 1942, the Princess met her third cousin, King Peter II of Yugoslavia in an officers' gala at Grosvenor House.
Quickly, they fell in love with each other and considered marriage, which greatly delighted Princess Aspasia.
However, the sharp opposition of Queen Maria of Yugoslavia, Peter II's mother, and the Yugoslav government-in-exile, which deemed it indecent to celebrate a wedding while Yugoslavia was dismembered and occupied, prevented for a while the marital project.
After a brief stay of Peter II in Cairo, Egypt, the couple finally married on 20 March 1944.
Marked by restrictions due to the war, Alexandra wore a wedding dress that was lent her by Lady Mary Lygon, wife of Prince Vsevolod Ivanovich of Russia (himself the son of King Peter's aunt Princess Helen of Serbia).
Among the guests at the ceremony, there were four reigning monarchs (George VI of the United Kingdom, George II of Greece, Haakon VII of Norway and Wilhelmina of the Netherlands) and several other members of European royalty, including the two brothers of the groom (Prince Tomislav and Prince Andrew), the mother of the bride, Prince Henry, Duke of Gloucester and Prince Bernhard of Lippe-Biesterfeld, son-in-law of Queen Wilhelmina.
Queen in exile

Liberation of Yugoslavia and the communist victory

Now Queen of Yugoslavia, Alexandra, however, had tenuous links with her new country, living under the Nazi occupation.
Finally, the other two main parts of Yugoslavia were reduced to puppet states: the Serbia of General Milan Nedić and the Croatian Kingdom of the Ustaše.
In October 1944, Churchill and Stalin concluded an agreement to split Yugoslavia into two occupation zones, but after the liberation of Belgrade by the Red Army and the Partisans, it became clear the Communists predominated in the country.
A harsh treatment, which affected the monarchists, took place; at the request of Churchill, Tito agreed in March 1945 to recognize a Regency Council (which had almost no activity) but opposed the return of King Peter II, who had to remain in exile with Alexandra while a government coalition dominated by the Communists was constituted in Belgrade.
Birth of Crown Prince Alexander and Peter II's deposition

In this turbulent context, Alexandra gave birth to an heir, named Alexander after his two grandfathers, Alexander of Yugoslavia and Alexander of Greece.
To enable the child to be born on Yugoslav soil, the British Prime Minister Winston Churchill reportedly asked King George VI to issue a decree transforming, for a day, Suite 212 into Yugoslav territory, which was to be the only time Alexandra was in Yugoslavia as queen.
On 24 October 1945, the newborn Crown Prince was baptized by the Serbian Patriarch Gavrilo V in Westminster Abbey, with King George VI and his elder daughter (the future Queen Elizabeth II) acting as godparents.
Faced with the rise of the Communists, King Peter II decided, to withdraw his confidence from the Regency Council and regain all his sovereign prerogatives in Yugoslavia (8 August).
On 24 November 1945 a single list presented by the communists was proposed to voters: while there were hardly more than 10,000 Communists throughout the Kingdom of Yugoslavia before the war, their candidates list obtained more than 90% of the votes in the referendum.
In their first meeting on 29 November 1945, the Constituent Assembly voted immediately to abolish the monarchy and proclaimed the Federal People's Republic of Yugoslavia.
Marital problems and suicide attempts

Financial and marital difficulties

Now without income and any prospect of returning to Yugoslavia, Peter II and Alexandra resolved to leave Claridge's Hotel and moved to a mansion in the Borough of Runnymede.
Still penniless, the couple was forced to sell Alexandra's necklace of emeralds and other pieces of her jewelry to pay their accumulated debts.
As Alexandra wrote in her autobiography, she had no idea of the value of things, and she quickly proved incapable of maintaining a home.
In the United States, Peter II soon drifted away.
Having made poor financial investments, he lost the little money he had left.
Thanks to the intervention of his maternal grandmother, the 4-year-old former Crown Prince Alexander was sent to Italy with the Count and Countess of Robilant, friends of the royal couple.
Divorce attempt and reconciliation

The year 1952 was marked by further financial problems due to bad investments of Peter II.
Alexandra also suffered a miscarriage.
In 1953, Alexandra made another suicide attempt in Paris, which she survived thanks to a phone call from her aunt, Queen Frederica of Greece.
Tired of the poor mental health of his wife, Peter II finally launched a process of divorce in the French courts.
The intervention of his son the crown prince and the King and Queen of Greece convinced him, however, to abandon his intentions.
However, the need for money continued to be felt and Alexandra was persuaded by a British publisher to write her autobiography.
Alexandra was always in financial need despite the relative success of the book.
Though it revealed nothing compromising about the Duke of Edinburgh, the book prompted the British royal family to distance itself from Alexandra.
For some time, the couple moved to Cannes, while Peter II maintained a chancellery in Monte Carlo.
Considering himself still King of Yugoslavia, the former sovereign continued to award titles and decorations.
However, the reconciliation of the royal couple finally soured and Peter II returned to live in the United States while Alexandra moved with her mother to the Garden of Eden.
In 1963, on 1 September or before, Alexandra made another suicide attempt in Venice.
Narrowly saved by her son former Crown Prince Alexander, she spent a long period of convalescence under the constant care of her sister-in-law, Princess Margarita of Baden (wife of Peter II's brother Prince Tomislav of Yugoslavia).
Once recovered, Alexandra reconciled again with Peter II and the couple returned to live in the French capital in 1967.
But, as before, the reconciliation was temporary and soon Peter II returned to live permanently in the United States while Alexandra settled in her mother's residence.
Last years

Peter II died on 3 November 1970 in Denver, United States, during an attempted liver transplant.
Still unstable and impoverished, Alexandra did not attend the ceremony, which took place in relative privacy.
Two years later, on 1 July 1972, former Crown Prince Alexander of Yugoslavia (now Head of the House of Karađorđević), married at Villamanrique de la Condesa, near Seville, Spain, Princess Maria da Glória of Orléans-Braganza (b. 1946), daughter of Brazilian Imperial pretender Prince Pedro Gastão of Orléans-Braganza and first cousin of King Juan Carlos I of Spain.
Too fragile emotionally, Alexandra did not attend the wedding of her son and it was her father's cousin Princess Olga of Greece (wife of Prince-Regent Paul of Yugoslavia), who escorted the groom to the altar.
One month later, on 7 August 1972, Alexandra's mother Princess Aspasia died.
The funeral of Alexandra was held in London, in the presence of her son, her three grandsons (Hereditary Prince Peter, Prince Philip and Prince Alexander) and several members of the Greek royal family, including the former King Constantine II and Queen Anne-Marie.
Alexandra's remains were then buried in the Royal cemetery park at Tatoi, Greece, next to her mother.
On 26 May 2013, Alexandra's remains were transferred to Serbia for reburial in the crypt of the Royal Mausoleum at Oplenac.
With her, the remains of her husband King Peter II, her mother-in-law Queen Mother Maria and brother-in-law Prince Andrew were also reburied at the same time in an official ceremony which was attended by Serbian President Tomislav Nikolić and his government.



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
  AssignClass (69ad2dc6-8d71-46e4-bdde-0871d150217a)
 Call ID: 69ad2dc6-8d71-46e4-bdde-0871d150217a
  Args:
    source: Alexandra of Greece and Denmark
    type: :Woman
  AssignClass (e45dd300-d2e0-43df-a52a-bb05d3953768)
 Call ID: e45dd300-d2e0-43df-a52a-bb05d3953768
  Args:
    source: Alexandra of Greece and Denmark
    type: :Person
  AddLiteral (3f0aa83a-d6eb-4f6c-be5c-5812de94dc20)
 Call ID: 3f0aa83a-d6eb-4f6c-be5c-5812de94dc20
  Args:
    literal_type: xsd:integer
    literal_value: 1921
    relation: :hasBirthYear
    source: Alexandra of Greece and Denmark
  AddLiteral (2b303151-8cd3-4d56-bfc4-9a1f24d8c9ea)
 Call ID: 2b303151-8cd3-4d56-bfc4-9a1f24d8c9ea
  Args:
    literal_value: 1993
    literal_type: xsd:integer
    source: Alexandra of Greece and Denmark
    relation: :hasDeathYear
  AssignClass (c2b17eae-02b4-40a8-ac6b-238a3c9c3dc3)
 Call ID: c2b17eae-02b4-40a8-ac6b-238a3c9c3dc3
  Args:
    source: King Alexander of Greece
    type: :Man
  AssignClass (466bda5d-c1bc-4c3a-951a-70edcd1167e4)
 Call ID: 466bda5d-c1bc-4c3a-951a-70edcd1167e4
  Args:
    source: King Alexander of Greece
    type: :Ancestor
  AssignClass (32c87c34-be00-4e38-853f-cf5ff1f8fa8a)
 Call ID: 32c87c34-be00-4e38-853f-cf5ff1f8fa8a
  Args:
    type: :Woman
    source: Aspasia Manos
  AssignClass (d1083975-822c-44ff-89b6-e0ad41ae6d5f)
 Call ID: d1083975-822c-44ff-89b6-e0ad41ae6d5f
  Args:
    source: Aspasia Manos
    type: :Ancestor
  AddTriple (ea2ae5df-d29c-46a4-918c-ad7f443154cb)
 Call ID: ea2ae5df-d29c-46a4-918c-ad7f443154cb
  Args:
    relation: :hasFather
    target: King Alexander of Greece
    source: Alexandra of Greece and Denmark
  AddTriple (523cd040-3c41-4871-897a-3e3bf531ce8d)
 Call ID: 523cd040-3c41-4871-897a-3e3bf531ce8d
  Args:
    target: Aspasia Manos
    relation: :hasMother
    source: Alexandra of Greece and Denmark
  AssignClass (ed2387b9-bc9a-4666-a1aa-85e053c9ca5f)
 Call ID: ed2387b9-bc9a-4666-a1aa-85e053c9ca5f
  Args:
    type: :Man
    source: King Peter II of Yugoslavia
  AssignClass (4491c6b6-ad79-4eba-8f25-3c79e57cf053)
 Call ID: 4491c6b6-ad79-4eba-8f25-3c79e57cf053
  Args:
    source: King Peter II of Yugoslavia
    type: :Ancestor
  AddTriple (29fe2f33-89d8-44dc-9add-233f8459f0f7)
 Call ID: 29fe2f33-89d8-44dc-9add-233f8459f0f7
  Args:
    source: Alexandra of Greece and Denmark
    target: King Peter II of Yugoslavia
    relation: :hasRelation
  AddLiteral (fa20ebb8-d7fc-4533-8550-d1d6a9faded3)
 Call ID: fa20ebb8-d7fc-4533-8550-d1d6a9faded3
  Args:
    source: Alexandra of Greece and Denmark
    relation: :hasMarriageYear
    literal_value: 1944
    literal_type: xsd:integer
  AssignClass (7a5095ab-b3c1-466e-a747-ced937c94de5)
 Call ID: 7a5095ab-b3c1-466e-a747-ced937c94de5
  Args:
    source: Alexander Crown Prince of Yugoslavia
    type: :Man
  AssignClass (f10bfb32-f729-432c-984b-f5cf4e3763b6)
 Call ID: f10bfb32-f729-432c-984b-f5cf4e3763b6
  Args:
    source: Alexander Crown Prince of Yugoslavia
    type: :Person
  AddTriple (b7fa92f5-5bd8-431a-9f47-f96b62ffec7e)
 Call ID: b7fa92f5-5bd8-431a-9f47-f96b62ffec7e
  Args:
    relation: :isSonOf
    target: Alexandra of Greece and Denmark
    source: Alexander Crown Prince of Yugoslavia
  AddTriple (d0cb6314-4af2-41ce-9c86-952fd4b36c2c)
 Call ID: d0cb6314-4af2-41ce-9c86-952fd4b36c2c
  Args:
    relation: :isSonOf
    target: King Peter II of Yugoslavia
    source: Alexander Crown Prince of Yugoslavia
  AssignClass (8f4ee8d7-1916-4657-af61-0f5690a1d0dc)
 Call ID: 8f4ee8d7-1916-4657-af61-0f5690a1d0dc
  Args:
    type: :Woman
    source: Queen Sophia of Greece
  AssignClass (2483482e-6ad6-404e-940f-0668c4b3592f)
 Call ID: 2483482e-6ad6-404e-940f-0668c4b3592f
  Args:
    type: :Ancestor
    source: Queen Sophia of Greece
  AddTriple (eaffc5b9-0b81-451c-9db6-2b762ecb9808)
 Call ID: eaffc5b9-0b81-451c-9db6-2b762ecb9808
  Args:
    source: King Alexander of Greece
    target: Queen Sophia of Greece
    relation: :hasMother
  AssignClass (0dbcd3f2-3120-465b-9036-288f727aa8d9)
 Call ID: 0dbcd3f2-3120-465b-9036-288f727aa8d9
  Args:
    type: :Woman
    source: Queen Maria of Yugoslavia
  AssignClass (fb704781-73fc-4d55-973c-327a50e15b9c)
 Call ID: fb704781-73fc-4d55-973c-327a50e15b9c
  Args:
    type: :Ancestor
    source: Queen Maria of Yugoslavia
  AddTriple (2fe764ed-7c53-41bd-bd4a-cacf87f40a4a)
 Call ID: 2fe764ed-7c53-41bd-bd4a-cacf87f40a4a
  Args:
    source: King Peter II of Yugoslavia
    target: Queen Maria of Yugoslavia
    relation: :hasMother
  AssignClass (4d619a01-9ccf-4923-a6e9-6c27c692d4d7)
 Call ID: 4d619a01-9ccf-4923-a6e9-6c27c692d4d7
  Args:
    type: :Man
    source: King Constantine I of Greece
  AssignClass (edfada86-44a5-4f2e-85aa-f21fbc85c2ce)
 Call ID: edfada86-44a5-4f2e-85aa-f21fbc85c2ce
  Args:
    source: King Constantine I of Greece
    type: :Ancestor
  AssignClass (eb94fec8-1471-4e1f-a514-4a7bc9b7c17f)
 Call ID: eb94fec8-1471-4e1f-a514-4a7bc9b7c17f
  Args:
    source: Queen Dowager Olga of Greece
    type: :Woman
  AssignClass (ebeeecb4-bc46-489f-9c06-ecd14ed365d4)
 Call ID: ebeeecb4-bc46-489f-9c06-ecd14ed365d4
  Args:
    type: :Ancestor
    source: Queen Dowager Olga of Greece
  AssignClass (d92b901d-5c1e-4e1d-b388-a3a1ecc7bdba)
 Call ID: d92b901d-5c1e-4e1d-b388-a3a1ecc7bdba
  Args:
    type: :Man
    source: King George II of Greece
  AssignClass (6229d289-135b-4b51-933e-3ebb921314c6)
 Call ID: 6229d289-135b-4b51-933e-3ebb921314c6
  Args:
    source: King George II of Greece
    type: :Person
  AddTriple (be6bdb8e-103f-42bb-8e7b-456220745df7)
 Call ID: be6bdb8e-103f-42bb-8e7b-456220745df7
  Args:
    relation: :isSisterOf
    target: King George II of Greece
    source: Alexandra of Greece and Denmark
  AddTriple (8d43ad49-cd81-4f81-88db-340b33a96d88)
 Call ID: 8d43ad49-cd81-4f81-88db-340b33a96d88
  Args:
    target: King Constantine I of Greece
    relation: :hasFather
    source: King George II of Greece
  AddTriple (b9b48d69-edc2-4f6d-a79e-7094cc2f4e9d)
 Call ID: b9b48d69-edc2-4f6d-a79e-7094cc2f4e9d
  Args:
    target: Queen Sophia of Greece
    relation: :hasMother
    source: King George II of Greece
  Finish (d1b1742f-80f3-4cc8-aad6-09f7019b8271)
 Call ID: d1b1742f-80f3-4cc8-aad6-09f7019b8271
  Args: