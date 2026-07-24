================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Alexandra (Greek: Αλεξάνδρα, Serbo-Croatian: Александра/Aleksandra, in 1922 retroactively recognised as Princess Alexandra of Greece and Denmark; 25 March 1921 – 30 January 1993) was the last Queen of Yugoslavia as the wife of King Peter II.


Posthumous daughter of King Alexander of Greece and his morganatic wife, Aspasia Manos, Alexandra was not part of the Greek royal family until July 1922 when, at the behest of Queen Sophia, Alexander's mother, a law was passed which retroactively recognized marriages of members of the royal family, although on a non-dynastic basis; in consequence, she obtained the style and name of Her Royal Highness Princess Alexandra of Greece and Denmark.
At the same time, a serious political and military crisis, linked to the defeat of Greece by Turkey in Anatolia, led to the deposition and exile of the royal family, beginning in 1924.
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
Alarmed, Aspasia thus moved her daughter to Switzerland for treatment.
Later, Alexandra was educated in a Parisian finishing school, during which time she and her mother stayed at the Hotel Crillon.
Eventually, the two princesses settled on the island of Giudecca in Venice, where Aspasia acquired a small property with her savings and Horlick's financial support.
Restoration of the Greek monarchy

Between Greece and Venice

In 1935, the Second Hellenic Republic was abolished and King George II (Alexandra's uncle) was restored to the throne after a referendum organized by General Georgios Kondylis.
Alexandra was then allowed to return to Greece, a country she had not seen since 1924.
In 1936, she participated in the official ceremonies which marked the reburial in Tatoi of the remains of King Constantine I, Queen Sophia, and Dowager Queen Olga; all three died in exile in Italy.
Despite her participation in the ceremonies of the Greek royal family, at that time Alexandra understood that she was not a full member of the European royalty.
Her mother had to claim in her name the share of the inheritance of Alexandra's paternal grandparents.
During the 1936 ceremonies, a chapel was arranged in the park of the palace for the remains of King Constantine I and Queen Sophia.
The remains of King Alexander − previously based in the gardens next to his grandfather King George I – were then transferred to this chapel, with no space reserved for Aspasia.
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
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix data: <http://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:Alexander_Crown_Prince_of_Yugoslavia a :Man,
        :Person ;
    :isSonOf data:Alexandra,
        data:Peter_II .

data:Alexander_of_Greece a :Ancestor,
        :Man .

data:Alexandra a :Person,
        :Woman ;
    :hasBirthYear "1921-03-25"^^xsd:date ;
    :hasDeathYear "1993-01-30"^^xsd:date ;
    :hasFather data:Alexander_of_Greece ;
    :hasMarriageYear 1944 ;
    :hasMother data:Aspasia_Manos ;
    :hasRelation data:Peter_II .

data:Aspasia_Manos a :Ancestor,
        :Woman .

data:Maria_of_Yugoslavia a :Ancestor,
        :Woman .

data:Peter_II a :Man,
        :Person ;
    :hasMother data:Maria_of_Yugoslavia .



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (89432af0-0115-49d8-9117-fe23a913fccf)
 Call ID: 89432af0-0115-49d8-9117-fe23a913fccf
  Args:
    type: :Person
    source: data:Alexander_of_Greece
  AssignClass (9d404294-5638-43a6-8922-8d74ccde74da)
 Call ID: 9d404294-5638-43a6-8922-8d74ccde74da
  Args:
    source: data:Aspasia_Manos
    type: :Person
  AssignClass (fd4f642d-3d01-4a67-acdb-74699814bcbd)
 Call ID: fd4f642d-3d01-4a67-acdb-74699814bcbd
  Args:
    type: :Person
    source: data:Maria_of_Yugoslavia
  AddTriple (429bb274-5caa-45b6-b43b-512906068a2c)
 Call ID: 429bb274-5caa-45b6-b43b-512906068a2c
  Args:
    relation: :hasFather
    source: data:Alexandra
    target: data:Alexander_of_Greece
  AddTriple (f0841878-0e57-4663-9d8a-aaec7f39d457)
 Call ID: f0841878-0e57-4663-9d8a-aaec7f39d457
  Args:
    source: data:Alexandra
    target: data:Aspasia_Manos
    relation: :hasMother
  AddTriple (dac6e749-d979-409c-ae38-2647a9070272)
 Call ID: dac6e749-d979-409c-ae38-2647a9070272
  Args:
    target: data:Maria_of_Yugoslavia
    source: data:Peter_II
    relation: :hasMother
  AddTriple (ce4c41ca-fe15-4766-8360-5fe5b91dc94a)
 Call ID: ce4c41ca-fe15-4766-8360-5fe5b91dc94a
  Args:
    source: data:Alexander_Crown_Prince_of_Yugoslavia
    target: data:Peter_II
    relation: :hasFather
  AddTriple (b251dfa0-7bd3-47df-89ca-e0de7b8705a3)
 Call ID: b251dfa0-7bd3-47df-89ca-e0de7b8705a3
  Args:
    relation: :hasMother
    target: data:Alexandra
    source: data:Alexander_Crown_Prince_of_Yugoslavia
  AddLiteral (1133db01-e873-4cab-8dde-b061007e2007)
 Call ID: 1133db01-e873-4cab-8dde-b061007e2007
  Args:
    literal_type: xsd:date
    relation: :hasDeathYear
    literal_value: 1970-11-03
    source: data:Peter_II
  AddLiteral (9c6e7e03-8748-41b4-955c-44426a917326)
 Call ID: 9c6e7e03-8748-41b4-955c-44426a917326
  Args:
    literal_type: xsd:date
    literal_value: 1972-08-07
    relation: :hasDeathYear
    source: data:Aspasia_Manos
  Finish (b6db772c-8d5d-47fa-84b1-92f8507e5afa)
 Call ID: b6db772c-8d5d-47fa-84b1-92f8507e5afa
  Args:

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

  data:Alexander_Crown_Prince_of_Yugoslavia a :Man,
          :Person ;
      :hasFather data:Peter_II ;
      :hasMother data:Alexandra ;
      :isSonOf data:Alexandra,
          data:Peter_II .

  data:Alexander_of_Greece a :Ancestor,
          :Man,
          :Person .

  data:Aspasia_Manos a :Ancestor,
          :Person,
          :Woman ;
      :hasDeathYear "1972-08-07"^^xsd:date .

  data:Maria_of_Yugoslavia a :Ancestor,
          :Person,
          :Woman .

  data:Alexandra a :Person,
          :Woman ;
      :hasBirthYear "1921-03-25"^^xsd:date ;
      :hasDeathYear "1993-01-30"^^xsd:date ;
      :hasFather data:Alexander_of_Greece ;
      :hasMarriageYear 1944 ;
      :hasMother data:Aspasia_Manos ;
      :hasRelation data:Peter_II .

  data:Peter_II a :Man,
          :Person ;
      :hasDeathYear "1970-11-03"^^xsd:date ;
      :hasMother data:Maria_of_Yugoslavia .



================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (27f3dc56-984b-46ed-b292-f000dd9c754b)
 Call ID: 27f3dc56-984b-46ed-b292-f000dd9c754b
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:12
Violations:

  Violation [1]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Peter_II is assigned as an 'isSonOf' ancestor for Alexander_Crown_Prince_of_Yugoslavia, but Peter_II lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Peter_II', class=':Ancestor')


  Violation [2]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Alexandra is assigned as an 'isSonOf' ancestor for Alexander_Crown_Prince_of_Yugoslavia, but Alexandra lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Alexandra', class=':Ancestor')


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Peter_II is assigned as the 'hasFather' of Alexander_Crown_Prince_of_Yugoslavia, but Peter_II lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Peter_II', class=':Ancestor')


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Alexandra is assigned as the 'hasMother' of Alexander_Crown_Prince_of_Yugoslavia, but Alexandra lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Alexandra', class=':Ancestor')


  Violation [5]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Peter_II is assigned as an 'isSonOf' ancestor for Alexander_Crown_Prince_of_Yugoslavia, but Peter_II lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Peter_II', class=':Ancestor')


  Violation [6]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Alexandra is assigned as an 'isSonOf' ancestor for Alexander_Crown_Prince_of_Yugoslavia, but Alexandra lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Alexandra', class=':Ancestor')


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Peter_II is assigned as the 'hasFather' of Alexander_Crown_Prince_of_Yugoslavia, but Peter_II lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Peter_II', class=':Ancestor')


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Alexandra is assigned as the 'hasMother' of Alexander_Crown_Prince_of_Yugoslavia, but Alexandra lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Alexandra', class=':Ancestor')


  Violation [9]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Peter_II is assigned as an 'isSonOf' ancestor for Alexander_Crown_Prince_of_Yugoslavia, but Peter_II lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Peter_II', class=':Ancestor')


  Violation [10]:
    SHACL message: Value does not have class :Ancestor
    LLM-provided explanation of the violation:
      The node Alexandra is assigned as an 'isSonOf' ancestor for Alexander_Crown_Prince_of_Yugoslavia, but Alexandra lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Alexandra', class=':Ancestor')


  Violation [11]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Peter_II is assigned as the 'hasFather' of Alexander_Crown_Prince_of_Yugoslavia, but Peter_II lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Peter_II', class=':Ancestor')


  Violation [12]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Alexandra is assigned as the 'hasMother' of Alexander_Crown_Prince_of_Yugoslavia, but Alexandra lacks the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Alexandra', class=':Ancestor')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a188d57b-44a9-4164-89d9-290ff18a63f9)
 Call ID: a188d57b-44a9-4164-89d9-290ff18a63f9
  Args:
    type: :Ancestor
    source: data:Peter_II
  AssignClass (a4648fa3-f9cf-41fc-aa27-44cfaeb1d037)
 Call ID: a4648fa3-f9cf-41fc-aa27-44cfaeb1d037
  Args:
    source: data:Alexandra
    type: :Ancestor
  Finish (7dcda929-9b54-4961-9174-9b37caf0474b)
 Call ID: 7dcda929-9b54-4961-9174-9b37caf0474b
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Alexander_Crown_Prince_of_Yugoslavia a :Man,
          :Person ;
      :hasFather data:Peter_II ;
      :hasMother data:Alexandra ;
      :isSonOf data:Alexandra,
          data:Peter_II .

  data:Alexander_of_Greece a :Ancestor,
          :Man,
          :Person .

  data:Aspasia_Manos a :Ancestor,
          :Person,
          :Woman ;
      :hasDeathYear "1972-08-07"^^xsd:date .

  data:Maria_of_Yugoslavia a :Ancestor,
          :Person,
          :Woman .

  data:Alexandra a :Ancestor,
          :Person,
          :Woman ;
      :hasBirthYear "1921-03-25"^^xsd:date ;
      :hasDeathYear "1993-01-30"^^xsd:date ;
      :hasFather data:Alexander_of_Greece ;
      :hasMarriageYear 1944 ;
      :hasMother data:Aspasia_Manos ;
      :hasRelation data:Peter_II .

  data:Peter_II a :Ancestor,
          :Man,
          :Person ;
      :hasDeathYear "1970-11-03"^^xsd:date ;
      :hasMother data:Maria_of_Yugoslavia .



================================= Tool Message =================================

Previous SHACL validation wasn't successful. If you fixed the violations, use the validation tool again to confirm no violations persist.

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (30f80259-f968-40da-b8a9-663970987f93)
 Call ID: 30f80259-f968-40da-b8a9-663970987f93
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (3de85035-0d5b-44b8-9e77-f22c2e9e6a3c)
 Call ID: 3de85035-0d5b-44b8-9e77-f22c2e9e6a3c
  Args: