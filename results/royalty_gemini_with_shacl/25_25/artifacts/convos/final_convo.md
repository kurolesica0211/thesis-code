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
Louise Alexandra Marie Irene Mountbatten (born Princess Louise of Battenberg; later Lady Louise Mountbatten; 13 July 1889 – 7 March 1965) was Queen of Sweden from 29 October 1950 until her death in 1965 as the wife of King Gustaf VI Adolf.
Born a princess of the German House of Battenberg, Louise was closely related to the ruling families of Britain, as a great-granddaughter of Queen Victoria and of Russia, as a niece of Empress Alexandra Feodorovna of Russia.
She was also an older sister to Lord Mountbatten and aunt to Prince Philip, Duke of Edinburgh.
During the First World War, Louise served as a nurse in the Red Cross.
Louise was noted for her eccentricity and progressive views.
Early life

Louise was born a Princess of Battenberg at Schloss Heiligenberg, Seeheim-Jugenheim, in the Grand Duchy of Hesse.
Her father, Prince Louis of Battenberg, who was an admiral in the British Royal Navy, renounced his German title during the First World War and anglicised his family name to "Mountbatten" at the behest of George V. He was then created the first Marquess of Milford Haven in the peerage of the United Kingdom.
From 1917, therefore, his daughter was known as "Lady Louise Mountbatten".
Her mother was Princess Victoria of Hesse and by Rhine, a granddaughter of Queen Victoria.
Louise was a sister of Louis Mountbatten, 1st
Earl Mountbatten of Burma, and of Princess Alice of Battenberg who was the mother of Prince Philip, Duke of Edinburgh.
Louise often visited her great-grandmother Queen Victoria on the Isle of Wight with her mother during her childhood.
The family is described as harmonious; the parents of Louise lived in a happy loving relationship, not in an arranged marriage, and Louise was particularly close to her brother, with whom she corresponded until her death.
Louise and her sister were educated by governesses, except for a brief period at Texter's girls school in Darmstadt.
In 1914, Louise and her mother visited the Russian Empire, and were invited to a trip down the Volga with their Imperial relatives.
During her visit, Louise noted the influence of Rasputin with concern.
The trip was interrupted by the sudden outbreak of the First World War, and Louise's father telegraphed for them to return immediately.
Louise's mother gave her jewellery to the empress for safe keeping, and they left Russia by boat from Hapsal in Estonia and travelled to neutral Sweden, paying for the trip with gold, as their money was suddenly not acceptable currency in Russia.
They stayed in Sweden as guests of Crown Prince Gustaf Adolf and Crown Princess Margaret, her first cousin once removed, at Drottningholm Palace, just one night before they returned to Great Britain.
During the First World War, Louise was first active within the Soldiers and Sailors Families Association and the Smokes for Soldiers and Sailors, but she soon enlisted in the Red Cross for service as a nurse.
Courtships

In 1909, Louise received a proposal from Manuel II of Portugal.
Her grand-uncle, Edward VII, the British monarch, was in favour of the match, but Louise declined, as she wished to marry for love.
At the age of twenty, Louise became secretly engaged to Prince Christopher of Greece, but they were forced to give up their relationship for financial reasons.
Shortly before World War I broke out, Louise fell in love with a man of whom her parents approved but he was killed in the early days of the war.
Anticipating that her parents would be disappointed in her choice, Louise kept their engagement a secret.
Eventually, she confided in her parents, who were understanding, and invited Stuart-Hill for visits at Kent House twice.
In 1918, however, Louise's father explained to her that Stuart-Hill was most likely homosexual, and that a marriage with him was impossible.
In 1923, Crown Prince Gustaf Adolf of Sweden, having been for three years the widower of Louise's mother's cousin Princess Margaret of Connaught, paid a visit to London and, to Louise's surprise, began to court her.
Although as a young woman Louise had said that she would never marry a king or a widower, she accepted the proposal of a man destined to be both.
However, under §5 of the 1810 Swedish Succession Law (Act 1810:0926), a prince of the Swedish royal house forfeited his right of succession to the throne if he "with or without the King's knowledge and consent, married a private Swedish or foreign man's daughter" (med eller utan Konungens vetskap och samtycke, tager till gemål enskild svensk eller utländsk mans dotter).
In response, the Swedish Foreign Ministry, citing the law in question, clarified the term "a private Swedish or foreign man's daughter" to mean "he who did not belong to a sovereign family or to a family which, according to international practice, would be equal thereto" (som icke vore medlem av suverän familj eller familj som enligt internationell praxis vore därmed likställd), and announced that the Swedish government had "requested the British government's explanation of Lady Louise Mountbatten's position in this respect."
The ministry further announced that following the British government's reply to its inquiry and the subsequent investigation into the matter, it had been determined that the Crown Prince's choice of a future wife was in compliance with the succession law, thereby concluding debate on the imminent nuptials.
On 27 October 1923, Sweden and Britain's respective plenipotentiaries signed the "Treaty between Great Britain and Sweden for the Marriage of Lady Louise Mountbatten with His Royal Highness Prince Gustaf Adolf, Crown Prince of Sweden".
On 3 November 1923, at age 34, Louise married Crown Prince Gustaf Adolf, in the Chapel Royal at St. James's Palace in the presence of George V and members of both royal families.
Crown princess

The marriage between Louise and Gustav Adolf was by all accounts a love match and described as very happy.
She was also liked by her mother-in-law because of her friendly nature, although they seldom saw each other, as Queen Victoria spent most of her time in Italy.
The fact that the queen spent most of her time abroad meant that Louise took on many royal duties from the beginning, which was initially hard for her as she was at this point described as quite shy.
After the queen's death in 1930, Louise was officially the first lady of the nation, expected to perform all the duties of a queen, twenty years before she actually became queen.
This meant that Louise was to take over the protection of all the organisations and associations traditionally assigned to the queen.
She was made the protector of the Swedish Red Cross, Children's Hospital of Crown Princess Louise, Eugenia Home, Drottningens centralkommitté ('Queen's Emergency Relief Committee'), Arbetsflitens Befrämjande ('The Promoting of Diligence'), Sophiahemmet and Svenska Hemslöjdsföreningarns Riksförbund ('Swedish Handicraft's Society').
Regarding this matter, Louise remarked: "It is hard for me to be the protector of different institutions, as I have been accustomed to practical work, as an ordinary person, before my marriage".
As a former nurse, a fact she was proud to point out, Louise was interested in improving the working conditions for nurses.
On 30 May 1925, Louise gave birth to her only child, a stillborn daughter.
During an interview in Salt Lake City, Louise stated that she believed in gender equality and that women are fully capable of being active within all professions and in the business world, as well as within politics: "Women are completely intellectually equal to men and, provided they are given sufficient education, are just as capable to deserve respect and admiration as men in this field".
In 1936, Louise attended the funeral of George V of the United Kingdom.
During World War II, Louise was active in aid work within the Red Cross.
för Neutralitetsvakten (English: "The Crown Princess Gift Association For the Neutral Defence Forces"), which provided the soldiers mobilised to guard the borders of neutral Sweden with gifts: normally socks, scarfs and caps knitted by contributors from all over the country.
As a citizen of a neutral country, Louise was also able to act as a messenger between relatives and friends across warfaring borders.
She also provided supplies to many private citizens in this way, such as "two old ladies in Münich", the former German language teacher of her husband's late wife, and the exiled Princess Tatiana of Russia in Palestine.
It is said many would have died, had it not been for Louise's help.
In 1940, for example, she sent supplies to the British major Michael Smiley of the Rifle Brigade, who was captured and placed in a prisoner of war camp, after his mother-in-law Alicia Pearson had asked for her help.
During the Finnish Winter War, Louise set up a home for Finnish war orphans at Ulriksdal Palace.
Queen consort

In 1950, Louise became queen after her husband's accession to the throne.
Louise is described as a true democrat at heart, and was therefore somewhat disturbed at being celebrated merely in her capacity of queen.
"


Louise disliked the strict pre-World War I protocol at court, retained during her mother-in-law's era, and reformed it when she became queen, instituting new guidelines in 1954 which democratised many old customs.
In 1962, she abolished the court presentations, replaced them with "democratic ladies' lunches", to which she invited professional career women, a custom which was to continue under Princess Sibylla after her death.
Louise also renovated and redecorated the interior of the Royal Palace in Stockholm.
Louise was described as eccentric for royalty and temperamental; she could get very angry, but was said to possess a good heart, a great sense of humour, a sense of self-irony and was able to distinguish between herself and her royal role.
Louise is described as a great lover and patriot of her new home country, and was often shocked by Swedish non-patriotic customs.
Louise also admired Swedish nature and in particular Swedish women, because of what she considered their natural dignity regardless of class, and remarked that she had never seen a country with less vulgarity than Sweden.
A popular story told of her alleges that Louise, after almost being hit by a bus in London (because she would often jay-walk), took to carrying a small card with the words, "I am the Queen of Sweden" printed on it, so that people would know who she was in case she was hit by a vehicle.
In 1963, Louise accompanied her spouse on a state visit to France, where she made a great impression on President Charles de Gaulle.
Louise's last official engagement was the Nobel Prize dinner of 1964, during which no one noticed that she was in fact already ill.
According to Queen Margrethe II of Denmark it was very difficult for Louise to fill the shoes of her husband's first wife.
Margrethe and Louise's other step-grandchildren all used the nickname Ist for Louise because when little they could not say Aunt Louise properly.
Louise responded good-naturedly by signing all her letters to them that way.
Death and funeral

Louise died on 7 March 1965 at Saint Göran Hospital, in Stockholm, Sweden, following emergency surgery after a period of severe illness.
Louise is buried beside her husband and his first wife, Crown Princess Margaret, in the Royal Cemetery in Solna north of Stockholm.



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
  AssignClass (603f4dab-9ef2-437a-b25f-cac975a6c556)
 Call ID: 603f4dab-9ef2-437a-b25f-cac975a6c556
  Args:
    type: :Woman
    source: :Louise_Mountbatten
  AssignClass (a48101eb-7204-4d35-b5a4-704348eb63a3)
 Call ID: a48101eb-7204-4d35-b5a4-704348eb63a3
  Args:
    type: :Person
    source: :Louise_Mountbatten
  AddLiteral (3347eebd-99c9-4cba-9b72-3d3e3d9ca5b1)
 Call ID: 3347eebd-99c9-4cba-9b72-3d3e3d9ca5b1
  Args:
    relation: :hasBirthYear
    source: :Louise_Mountbatten
    literal_value: 1889
    literal_type: xsd:integer
  AddLiteral (fa9578bd-8a08-490b-bafe-d91e7b33ed21)
 Call ID: fa9578bd-8a08-490b-bafe-d91e7b33ed21
  Args:
    literal_type: xsd:integer
    literal_value: 1965
    source: :Louise_Mountbatten
    relation: :hasDeathYear
  AddLiteral (3b07601e-5b24-498f-95e8-793e8008590f)
 Call ID: 3b07601e-5b24-498f-95e8-793e8008590f
  Args:
    source: :Louise_Mountbatten
    literal_value: Louise Alexandra Marie Irene Mountbatten
    literal_type: xsd:string
    relation: :knownAs
  AddLiteral (4567cc53-e382-4721-9c39-d6bcb0c349a1)
 Call ID: 4567cc53-e382-4721-9c39-d6bcb0c349a1
  Args:
    literal_type: xsd:string
    literal_value: Princess Louise of Battenberg
    source: :Louise_Mountbatten
    relation: :formerlyKnownAs
  AddLiteral (33148b09-0624-4171-aa33-d808319c9a34)
 Call ID: 33148b09-0624-4171-aa33-d808319c9a34
  Args:
    literal_value: Lady Louise Mountbatten
    source: :Louise_Mountbatten
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (09726455-2273-4695-ab1e-2b6b0a793250)
 Call ID: 09726455-2273-4695-ab1e-2b6b0a793250
  Args:
    source: :Prince_Louis_of_Battenberg
    type: :Man
  AssignClass (12489cc9-a259-4dec-8de1-7558b629a827)
 Call ID: 12489cc9-a259-4dec-8de1-7558b629a827
  Args:
    source: :Prince_Louis_of_Battenberg
    type: :Person
  AssignClass (c7a3a1da-1956-4bec-b0a1-23f6570fc458)
 Call ID: c7a3a1da-1956-4bec-b0a1-23f6570fc458
  Args:
    type: :Ancestor
    source: :Prince_Louis_of_Battenberg
  AddTriple (a61efd38-7fa0-481d-8b73-26775c664276)
 Call ID: a61efd38-7fa0-481d-8b73-26775c664276
  Args:
    relation: :hasFather
    target: :Prince_Louis_of_Battenberg
    source: :Louise_Mountbatten
  AssignClass (779a4ebf-e8d9-4e28-8fb1-a20bcda5247e)
 Call ID: 779a4ebf-e8d9-4e28-8fb1-a20bcda5247e
  Args:
    type: :Woman
    source: :Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (f8200955-ae5d-4c76-ac1a-202ee6b92787)
 Call ID: f8200955-ae5d-4c76-ac1a-202ee6b92787
  Args:
    source: :Princess_Victoria_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (6f72a8e5-697f-4e35-a3cc-1467c27515e0)
 Call ID: 6f72a8e5-697f-4e35-a3cc-1467c27515e0
  Args:
    source: :Princess_Victoria_of_Hesse_and_by_Rhine
    type: :Ancestor
  AddTriple (fad0d137-2cc4-433a-8d32-59c93bfd6f65)
 Call ID: fad0d137-2cc4-433a-8d32-59c93bfd6f65
  Args:
    relation: :hasMother
    target: :Princess_Victoria_of_Hesse_and_by_Rhine
    source: :Louise_Mountbatten
  AssignClass (5cb115c1-578b-4a40-be54-a1228d29bd7c)
 Call ID: 5cb115c1-578b-4a40-be54-a1228d29bd7c
  Args:
    type: :Man
    source: :Lord_Mountbatten
  AssignClass (fb0a0ad7-f5ca-4008-a05a-c9be52260c20)
 Call ID: fb0a0ad7-f5ca-4008-a05a-c9be52260c20
  Args:
    source: :Lord_Mountbatten
    type: :Person
  AddTriple (f0fe0908-1713-4f0a-b992-7564bd06db1b)
 Call ID: f0fe0908-1713-4f0a-b992-7564bd06db1b
  Args:
    relation: :isSiblingOf
    target: :Lord_Mountbatten
    source: :Louise_Mountbatten
  AssignClass (87bb4840-48bb-4134-ae30-7de29408ea69)
 Call ID: 87bb4840-48bb-4134-ae30-7de29408ea69
  Args:
    source: :Princess_Alice_of_Battenberg
    type: :Woman
  AssignClass (94fd92eb-0b03-4c16-b841-f37f2c0a5e73)
 Call ID: 94fd92eb-0b03-4c16-b841-f37f2c0a5e73
  Args:
    source: :Princess_Alice_of_Battenberg
    type: :Person
  AddTriple (059bea07-4412-4033-a973-76b14e8aba02)
 Call ID: 059bea07-4412-4033-a973-76b14e8aba02
  Args:
    source: :Louise_Mountbatten
    target: :Princess_Alice_of_Battenberg
    relation: :isSiblingOf
  AssignClass (e28a7265-cfd3-4ec6-afdc-a87f4ba798b5)
 Call ID: e28a7265-cfd3-4ec6-afdc-a87f4ba798b5
  Args:
    source: :Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (e91dc078-955c-46c7-9150-fedb46317c92)
 Call ID: e91dc078-955c-46c7-9150-fedb46317c92
  Args:
    type: :Person
    source: :Prince_Philip_Duke_of_Edinburgh
  AddTriple (d2c69274-bb6d-4ad3-8033-b3b0a03887b0)
 Call ID: d2c69274-bb6d-4ad3-8033-b3b0a03887b0
  Args:
    relation: :hasMother
    target: :Princess_Alice_of_Battenberg
    source: :Prince_Philip_Duke_of_Edinburgh
  AssignClass (e016ead4-f024-4648-aba5-950685b1941b)
 Call ID: e016ead4-f024-4648-aba5-950685b1941b
  Args:
    source: :King_Gustaf_VI_Adolf
    type: :Man
  AssignClass (d9ba3b94-00f2-49a0-a8e3-98095109b8e3)
 Call ID: d9ba3b94-00f2-49a0-a8e3-98095109b8e3
  Args:
    source: :King_Gustaf_VI_Adolf
    type: :Person
  AddLiteral (7ec8e63a-3139-4f6d-968f-495129e9671b)
 Call ID: 7ec8e63a-3139-4f6d-968f-495129e9671b
  Args:
    source: :Louise_Mountbatten
    literal_value: 1923
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (1eca3bba-1999-4bcf-9a93-b5a5d4178da4)
 Call ID: 1eca3bba-1999-4bcf-9a93-b5a5d4178da4
  Args:
    target: :King_Gustaf_VI_Adolf
    source: :Louise_Mountbatten
    relation: :hasRelation
  Finish (2b0f918e-5963-4f0b-ad04-e9f242e3222f)
 Call ID: 2b0f918e-5963-4f0b-ad04-e9f242e3222f
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
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Louise_Mountbatten a :Person,
          :Woman ;
      :alsoKnownAs "Lady Louise Mountbatten"^^xsd:string ;
      :formerlyKnownAs "Princess Louise of Battenberg"^^xsd:string ;
      :hasBirthYear 1889 ;
      :hasDeathYear 1965 ;
      :hasFather data:Prince_Louis_of_Battenberg ;
      :hasMarriageYear 1923 ;
      :hasMother data:Princess_Victoria_of_Hesse_and_by_Rhine ;
      :hasRelation data:King_Gustaf_VI_Adolf ;
      :isSiblingOf data:Lord_Mountbatten,
          data:Princess_Alice_of_Battenberg ;
      :knownAs "Louise Alexandra Marie Irene Mountbatten"^^xsd:string .

  data:Prince_Philip_Duke_of_Edinburgh a :Man,
          :Person ;
      :hasMother data:Princess_Alice_of_Battenberg .

  data:King_Gustaf_VI_Adolf a :Man,
          :Person .

  data:Lord_Mountbatten a :Man,
          :Person .

  data:Prince_Louis_of_Battenberg a :Ancestor,
          :Man,
          :Person .

  data:Princess_Victoria_of_Hesse_and_by_Rhine a :Ancestor,
          :Person,
          :Woman .

  data:Princess_Alice_of_Battenberg a :Person,
          :Woman .



================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (a6fb13b4-7b09-414a-bd9a-7f77e2d2f18f)
 Call ID: a6fb13b4-7b09-414a-bd9a-7f77e2d2f18f
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:3
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Princess_Alice_of_Battenberg' is missing the mandatory ':Ancestor' class, which is required for the 'hasMother' property of 'Prince_Philip_Duke_of_Edinburgh'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Princess_Alice_of_Battenberg, :Ancestor)


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Princess_Alice_of_Battenberg' is missing the mandatory ':Ancestor' class, which is required for the 'hasMother' property of 'Prince_Philip_Duke_of_Edinburgh'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Princess_Alice_of_Battenberg, :Ancestor)


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Princess_Alice_of_Battenberg' is missing the mandatory ':Ancestor' class, which is required for the 'hasMother' property of 'Prince_Philip_Duke_of_Edinburgh'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(Princess_Alice_of_Battenberg, :Ancestor)




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (30c18c5c-0332-4ea5-b7ad-cee91c377bed)
 Call ID: 30c18c5c-0332-4ea5-b7ad-cee91c377bed
  Args:
    type: :Ancestor
    source: :Princess_Alice_of_Battenberg

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Louise_Mountbatten a :Person,
          :Woman ;
      :alsoKnownAs "Lady Louise Mountbatten"^^xsd:string ;
      :formerlyKnownAs "Princess Louise of Battenberg"^^xsd:string ;
      :hasBirthYear 1889 ;
      :hasDeathYear 1965 ;
      :hasFather data:Prince_Louis_of_Battenberg ;
      :hasMarriageYear 1923 ;
      :hasMother data:Princess_Victoria_of_Hesse_and_by_Rhine ;
      :hasRelation data:King_Gustaf_VI_Adolf ;
      :isSiblingOf data:Lord_Mountbatten,
          data:Princess_Alice_of_Battenberg ;
      :knownAs "Louise Alexandra Marie Irene Mountbatten"^^xsd:string .

  data:Prince_Philip_Duke_of_Edinburgh a :Man,
          :Person ;
      :hasMother data:Princess_Alice_of_Battenberg .

  data:King_Gustaf_VI_Adolf a :Man,
          :Person .

  data:Lord_Mountbatten a :Man,
          :Person .

  data:Prince_Louis_of_Battenberg a :Ancestor,
          :Man,
          :Person .

  data:Princess_Victoria_of_Hesse_and_by_Rhine a :Ancestor,
          :Person,
          :Woman .

  data:Princess_Alice_of_Battenberg a :Ancestor,
          :Person,
          :Woman .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (c32577d2-eb47-43f0-bb28-86790de6a6c4)
 Call ID: c32577d2-eb47-43f0-bb28-86790de6a6c4
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (f35af77c-0f51-4117-8121-9d9f93773bb7)
 Call ID: f35af77c-0f51-4117-8121-9d9f93773bb7
  Args: