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
  AssignClass (70108c72-59d3-4212-bd9e-9577d3b83c22)
 Call ID: 70108c72-59d3-4212-bd9e-9577d3b83c22
  Args:
    type: :Woman
    source: :LouiseMountbatten
  AssignClass (d9b0165a-0886-4050-ab2f-4535baddef55)
 Call ID: d9b0165a-0886-4050-ab2f-4535baddef55
  Args:
    type: :Person
    source: :LouiseMountbatten
  AddLiteral (81fedd89-86fe-45a6-9067-e981a3bbb6a2)
 Call ID: 81fedd89-86fe-45a6-9067-e981a3bbb6a2
  Args:
    literal_type: xsd:integer
    literal_value: 1889
    relation: :hasBirthYear
    source: :LouiseMountbatten
  AddLiteral (8edb7abf-d5d5-4e6a-b120-1a46106d63e9)
 Call ID: 8edb7abf-d5d5-4e6a-b120-1a46106d63e9
  Args:
    relation: :hasDeathYear
    source: :LouiseMountbatten
    literal_type: xsd:integer
    literal_value: 1965
  AddLiteral (3a03f3dd-69ac-4270-8cb6-d9f2560242ae)
 Call ID: 3a03f3dd-69ac-4270-8cb6-d9f2560242ae
  Args:
    source: :LouiseMountbatten
    relation: :formerlyKnownAs
    literal_value: Princess Louise of Battenberg
    literal_type: xsd:string
  AddLiteral (33ecf0f9-8906-4ecb-87f9-0a261367496b)
 Call ID: 33ecf0f9-8906-4ecb-87f9-0a261367496b
  Args:
    literal_value: Lady Louise Mountbatten
    literal_type: xsd:string
    source: :LouiseMountbatten
    relation: :knownAs
  AssignClass (a7a3ce7b-40fe-4fbc-9416-2d994c27330b)
 Call ID: a7a3ce7b-40fe-4fbc-9416-2d994c27330b
  Args:
    source: :PrinceLouisOfBattenberg
    type: :Man
  AssignClass (80bf5e99-d70a-4ad8-a585-ca8a9221d1d9)
 Call ID: 80bf5e99-d70a-4ad8-a585-ca8a9221d1d9
  Args:
    type: :Person
    source: :PrinceLouisOfBattenberg
  AssignClass (4be00351-f956-473e-890b-207f78ce4c30)
 Call ID: 4be00351-f956-473e-890b-207f78ce4c30
  Args:
    type: :Woman
    source: :PrincessVictoriaOfHesse
  AssignClass (be78b7a6-a0a0-42ff-baaf-62a71ec1b29e)
 Call ID: be78b7a6-a0a0-42ff-baaf-62a71ec1b29e
  Args:
    source: :PrincessVictoriaOfHesse
    type: :Person
  AddTriple (bc2a04ef-4659-4606-9954-5cd541d5d7d0)
 Call ID: bc2a04ef-4659-4606-9954-5cd541d5d7d0
  Args:
    relation: :hasFather
    target: :PrinceLouisOfBattenberg
    source: :LouiseMountbatten
  AddTriple (eacbfcce-4331-4dd4-8e31-4d16e31abe5a)
 Call ID: eacbfcce-4331-4dd4-8e31-4d16e31abe5a
  Args:
    source: :LouiseMountbatten
    target: :PrincessVictoriaOfHesse
    relation: :hasMother
  AssignClass (afd664a4-60ed-4d2a-afa7-68000edb47a7)
 Call ID: afd664a4-60ed-4d2a-afa7-68000edb47a7
  Args:
    source: :LordMountbatten
    type: :Man
  AssignClass (09414119-4886-4d30-9c3a-81b9544d3cac)
 Call ID: 09414119-4886-4d30-9c3a-81b9544d3cac
  Args:
    source: :LordMountbatten
    type: :Person
  AddTriple (e2efe52d-8da6-4237-b824-2d50a16774e1)
 Call ID: e2efe52d-8da6-4237-b824-2d50a16774e1
  Args:
    target: :LordMountbatten
    relation: :hasBrother
    source: :LouiseMountbatten
  AssignClass (fc9b3b6e-6796-4b02-a2bd-d026b68f585c)
 Call ID: fc9b3b6e-6796-4b02-a2bd-d026b68f585c
  Args:
    source: :PrincessAliceOfBattenberg
    type: :Woman
  AssignClass (6aa141dc-15bb-4df2-ac3c-b91b6b5ad900)
 Call ID: 6aa141dc-15bb-4df2-ac3c-b91b6b5ad900
  Args:
    type: :Person
    source: :PrincessAliceOfBattenberg
  AddTriple (685efc0b-67ec-4457-b760-e95f346e82a0)
 Call ID: 685efc0b-67ec-4457-b760-e95f346e82a0
  Args:
    target: :PrincessAliceOfBattenberg
    relation: :hasSister
    source: :LouiseMountbatten
  AssignClass (d212758e-02ec-4636-b34f-4828f2822762)
 Call ID: d212758e-02ec-4636-b34f-4828f2822762
  Args:
    type: :Man
    source: :PrincePhilip
  AssignClass (e83c994d-77ed-4275-8393-3ee697456dcb)
 Call ID: e83c994d-77ed-4275-8393-3ee697456dcb
  Args:
    type: :Person
    source: :PrincePhilip
  AddTriple (46f33c20-c24e-4500-8667-2e13e7bdff6d)
 Call ID: 46f33c20-c24e-4500-8667-2e13e7bdff6d
  Args:
    source: :PrincePhilip
    relation: :hasMother
    target: :PrincessAliceOfBattenberg
  AssignClass (0445abd2-0f40-4296-84e1-d18f6a7c031a)
 Call ID: 0445abd2-0f40-4296-84e1-d18f6a7c031a
  Args:
    type: :Man
    source: :GustafVIAdolf
  AssignClass (911cb28d-57fd-4d72-aebe-c23cf7197020)
 Call ID: 911cb28d-57fd-4d72-aebe-c23cf7197020
  Args:
    type: :Person
    source: :GustafVIAdolf
  AddLiteral (c705946f-aa20-4d38-b5ef-cbac796e772f)
 Call ID: c705946f-aa20-4d38-b5ef-cbac796e772f
  Args:
    literal_type: xsd:integer
    literal_value: 1923
    relation: :hasMarriageYear
    source: :LouiseMountbatten
  AddTriple (ec2977df-2314-4531-87bf-5c328b44a0c3)
 Call ID: ec2977df-2314-4531-87bf-5c328b44a0c3
  Args:
    source: :LouiseMountbatten
    target: :GustafVIAdolf
    relation: :hasRelation
  Finish (ecf06a74-7079-44a0-a660-4658017f5324)
 Call ID: ecf06a74-7079-44a0-a660-4658017f5324
  Args: