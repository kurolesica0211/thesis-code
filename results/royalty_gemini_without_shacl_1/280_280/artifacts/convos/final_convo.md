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
Grand Duke Vladimir Kirillovich of Russia (Russian: Владимир Кириллович Романов; 30 August  1917 – 21 April 1992) was the Head of the Imperial Family of Russia, a position which he claimed from 1938 to his death in 1992.
Early life

Vladimir was born Prince Vladimir Kirillovich of Russia at Porvoo in the Grand Duchy of Finland, the only son of Grand Duke Cyril Vladimirovich and Grand Duchess Viktoria Feodorovna (née Princess Victoria Melita of Saxe-Coburg and Gotha).
Vladimir's paternal grandparents were Grand Duke Vladimir Alexandrovich of Russia and Grand Duchess Maria Pavlovna (née Duchess Marie of Mecklenburg-Schwerin).
His maternal grandparents were Alfred, Duke of Saxe-Coburg and Gotha (the second son and fourth child of Queen Victoria) and Grand Duchess Marie Alexandrovna of Russia.
Vladimir's family had fled to Finland after the Russian Revolution of 1917.
His family left Finland in 1920, moving to Coburg, Germany.
On 8 August 1922 Vladimir's father declared himself Curator of the Russian throne.
With his father's assumption of the Imperial title Vladimir was granted the title of Tsesarevich (heir apparent) and Grand Duke with the style of Imperial Highness.
In the 1930s Vladimir lived for a period in England studying at the University of London and working at the Blackstone agricultural equipment factory in Lincolnshire.
Russian heir and World War II

On the death of his father on 12 October 1938, Vladimir assumed the Headship of the Imperial Family of Russia.
In 1938 there were suggestions that he would be made regent of Ukraine but he rebuffed the idea, saying he would not help dissolve Russia.
During World War II, Vladimir was living in Saint-Briac-sur-Mer in Brittany.
On June 26, 1941, he issued this statement: "In this grave hour, when Germany and almost all the nations of Europe have declared a crusade against Communism and Bolshevism, which has enslaved and oppressed the people of Russia for twenty-four years, I turn to all the faithful and loyal sons of our Homeland with this appeal: Do what you can, to the best of your ability, to bring down the Bolshevik regime and to liberate our Homeland from the terrible yoke of Communism."
In 1942, Vladimir and his entourage were placed in an internment camp at Compiègne after he refused to issue a manifesto calling on Russian émigrés to support Nazi Germany's war against the Soviet Union.
Vladimir lived in a castle belonging to the husband of his elder sister Maria Kirillovna in Amorbach, Bavaria until 1945.
After Germany's defeat, Vladimir's fear of being captured by the Soviets prompted relocation to Austria and next to the border of Liechtenstein.
Vladimir's maternal aunt, Infanta Beatrice of Orléans-Borbon, secured for him a Spanish visa.
Vladimir married Princess Leonida Georgievna Bagration-Moukhransky on 13 August 1948 in Lausanne.
The family to which Princess Leonida belonged, the Bagrationi dynasty, had been kings in Georgia from the medieval era until the early 19th century, but no male line ancestor of hers had reigned as a king in Georgia since 1505 and her branch of the Bagrationis, the House of Mukhrani, had been naturalised among the non-ruling nobility of Russia after Georgia was annexed to the Russian Empire in 1801.
Yet the royal status of the House of Bagrationi had been recognized by Russia in the 1783 Treaty of Georgievsk and was confirmed by Vladimir Kirillovich on 5 December 1946 as claimed head of the Russian imperial house.
However the last ruling emperor of Imperial Russia Nicholas II had deemed marriage in this family of Princess Tatiana Constantinova in 1911, as morganatic.
Some controversy therefore arises as to whether Vladimir's marriage to Leonida was equal or morganatic, and whether his claim to the Imperial throne validly passed to his daughter Maria, to some other dynast, or to no one upon his death.
Following Vladimir's public designation of his daughter as "curatrix of the throne", in anticipation that she would eventually succeed him as head of the dynasty in exile, the heads of three of the other branches of the imperial family — the Princes Vsevolod Ioannovich (Konstantinovichi), Roman Petrovich (Nikolaevichi) and Andrei Alexandrovich (Mihailovichi) — wrote to Vladimir in 1969, asserting that the dynastic status of his daughter was no different from that of their own children (Vsevolod Ioannovich was childless, but Roman Petrovich had two sons by Countess Prascovia Sheremetyev, while Andrei Alexandrovich had two sons by Donna Elisabeth Ruffo of a Russian branch of the Princes di San Sant' Antimo) and that his wife was of no higher status than the wives of the other Romanov princes.
On 23 December 1969 Vladimir issued a controversial decree whereby in the event he predeceased the living male Romanovs that he recognised as dynasts then his daughter Maria would become the "Curatrix of the Imperial Throne".
This has been viewed as an attempt by Vladimir to ensure the succession remained in his branch of the imperial family, while the heads of the other branches declared that Vladimir's actions were illegal.
Vladimir was able to visit Russia in November 1991 when he was invited to visit St Petersburg by its Mayor Anatoly Sobchak.
Death and succession dispute

Grand Duke Vladimir died while addressing a gathering of Spanish-speaking bankers and investors in Northern Trust Bank Miami in the United States on 21 April 1992.
His body was returned to Russia and he was buried in the Peter and Paul Fortress in St. Petersburg, the first Romanov to be honoured in this way since before the revolution.
As he was only a great-grandson of a recognized Russian emperor, his claimed title of "Grand Duke of Russia" caused problems as to what to put on his tombstone.
After his death, his daughter Maria Vladimirovna assumed the headship of the Imperial Family of Russia according to his branch's interpretation of the Russian house laws.
This was disputed by Nicholas Romanov, Prince of Russia who had been chosen president of the self-styled "Romanov Family Association" prior to the death of Grand Duke Vladimir.
}} Media related to Vladimir Kirillovich Romanov at Wikimedia Commons



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
  AssignClass (625a7e20-b7a0-465d-9049-57a3978aa833)
 Call ID: 625a7e20-b7a0-465d-9049-57a3978aa833
  Args:
    source: :Vladimir_Kirillovich_of_Russia
    type: :Man
  AssignClass (410301e7-60f2-4b8f-94f6-7ca236160a1c)
 Call ID: 410301e7-60f2-4b8f-94f6-7ca236160a1c
  Args:
    source: :Vladimir_Kirillovich_of_Russia
    type: :Person
  AddLiteral (e3d226f7-e512-4da5-b9e7-2bc26b9f3d55)
 Call ID: e3d226f7-e512-4da5-b9e7-2bc26b9f3d55
  Args:
    literal_type: xsd:integer
    literal_value: 1917
    source: :Vladimir_Kirillovich_of_Russia
    relation: :hasBirthYear
  AddLiteral (25888634-44e7-464d-bbed-4a7ccc18406e)
 Call ID: 25888634-44e7-464d-bbed-4a7ccc18406e
  Args:
    relation: :hasDeathYear
    source: :Vladimir_Kirillovich_of_Russia
    literal_value: 1992
    literal_type: xsd:integer
  AssignClass (bfdf7afd-fb74-401f-b57a-f88ce94f4b89)
 Call ID: bfdf7afd-fb74-401f-b57a-f88ce94f4b89
  Args:
    type: :Man
    source: :Cyril_Vladimirovich
  AssignClass (3719faec-09da-43b6-adec-0903827b6464)
 Call ID: 3719faec-09da-43b6-adec-0903827b6464
  Args:
    type: :Person
    source: :Cyril_Vladimirovich
  AssignClass (e14aab93-f01b-4f83-bd7e-6460c0739111)
 Call ID: e14aab93-f01b-4f83-bd7e-6460c0739111
  Args:
    source: :Viktoria_Feodorovna
    type: :Woman
  AssignClass (5cc2f4b6-c47c-4181-956a-70a47e1ceccc)
 Call ID: 5cc2f4b6-c47c-4181-956a-70a47e1ceccc
  Args:
    type: :Person
    source: :Viktoria_Feodorovna
  AddTriple (e2c24800-d3d1-4ba5-bd76-9ba585ec1693)
 Call ID: e2c24800-d3d1-4ba5-bd76-9ba585ec1693
  Args:
    source: :Vladimir_Kirillovich_of_Russia
    relation: :hasFather
    target: :Cyril_Vladimirovich
  AddTriple (0c5d8c19-1cec-4e9a-b188-7a7171aa18fd)
 Call ID: 0c5d8c19-1cec-4e9a-b188-7a7171aa18fd
  Args:
    target: :Viktoria_Feodorovna
    relation: :hasMother
    source: :Vladimir_Kirillovich_of_Russia
  AssignClass (c2ee55c6-f2e5-4931-a7da-320a052d759c)
 Call ID: c2ee55c6-f2e5-4931-a7da-320a052d759c
  Args:
    source: :Vladimir_Alexandrovich_of_Russia
    type: :Man
  AssignClass (ae30ee08-bd6d-4409-b1c5-910ea41ab087)
 Call ID: ae30ee08-bd6d-4409-b1c5-910ea41ab087
  Args:
    source: :Vladimir_Alexandrovich_of_Russia
    type: :Person
  AssignClass (71a1ec66-61b9-4aed-901c-f61fb6fc9a23)
 Call ID: 71a1ec66-61b9-4aed-901c-f61fb6fc9a23
  Args:
    type: :Woman
    source: :Maria_Pavlovna
  AssignClass (3bb27c47-1162-4ea0-aeb0-d7b7fd59f749)
 Call ID: 3bb27c47-1162-4ea0-aeb0-d7b7fd59f749
  Args:
    type: :Person
    source: :Maria_Pavlovna
  AddTriple (bceb9423-3472-4d0c-82d0-c0b394579672)
 Call ID: bceb9423-3472-4d0c-82d0-c0b394579672
  Args:
    target: :Vladimir_Alexandrovich_of_Russia
    relation: :hasFather
    source: :Cyril_Vladimirovich
  AddTriple (d1b8cae9-d89d-4a22-9122-166e0202c913)
 Call ID: d1b8cae9-d89d-4a22-9122-166e0202c913
  Args:
    target: :Maria_Pavlovna
    relation: :hasMother
    source: :Cyril_Vladimirovich
  AssignClass (0aa0c724-6ffc-4a69-9fc1-adbbb201f416)
 Call ID: 0aa0c724-6ffc-4a69-9fc1-adbbb201f416
  Args:
    type: :Man
    source: :Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (4d224adc-f909-4a39-a883-745b26d5d13a)
 Call ID: 4d224adc-f909-4a39-a883-745b26d5d13a
  Args:
    source: :Alfred_Duke_of_Saxe_Coburg_and_Gotha
    type: :Person
  AssignClass (6c47018a-b2e8-4c9a-a0c8-f1b57464d567)
 Call ID: 6c47018a-b2e8-4c9a-a0c8-f1b57464d567
  Args:
    source: :Marie_Alexandrovna_of_Russia
    type: :Woman
  AssignClass (5eb10bca-6fb2-48ff-8d09-06bc0019a5e3)
 Call ID: 5eb10bca-6fb2-48ff-8d09-06bc0019a5e3
  Args:
    source: :Marie_Alexandrovna_of_Russia
    type: :Person
  AddTriple (e1a19df7-fd21-459b-a403-3cd27002e5a7)
 Call ID: e1a19df7-fd21-459b-a403-3cd27002e5a7
  Args:
    relation: :hasFather
    target: :Alfred_Duke_of_Saxe_Coburg_and_Gotha
    source: :Viktoria_Feodorovna
  AddTriple (fbd20b84-c048-4ecd-a73a-7126a8428e5b)
 Call ID: fbd20b84-c048-4ecd-a73a-7126a8428e5b
  Args:
    source: :Viktoria_Feodorovna
    relation: :hasMother
    target: :Marie_Alexandrovna_of_Russia
  AssignClass (c1eaa57a-08da-4ce4-8cc6-474069a8f999)
 Call ID: c1eaa57a-08da-4ce4-8cc6-474069a8f999
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (e621d0cf-cb40-42a3-9936-5176e71a4765)
 Call ID: e621d0cf-cb40-42a3-9936-5176e71a4765
  Args:
    type: :Person
    source: :Queen_Victoria
  AddTriple (d4e41807-9620-442d-a7cd-cc21a2069df8)
 Call ID: d4e41807-9620-442d-a7cd-cc21a2069df8
  Args:
    source: :Queen_Victoria
    relation: :isMotherOf
    target: :Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (89ee24d8-800e-479e-8af3-a2797d51e6b4)
 Call ID: 89ee24d8-800e-479e-8af3-a2797d51e6b4
  Args:
    source: :Maria_Kirillovna
    type: :Woman
  AssignClass (ce1bf389-6d89-49f0-8f0e-cb9294cdd2bc)
 Call ID: ce1bf389-6d89-49f0-8f0e-cb9294cdd2bc
  Args:
    type: :Person
    source: :Maria_Kirillovna
  AddTriple (e9dc4afa-484a-4cf6-b701-31a55d6870e8)
 Call ID: e9dc4afa-484a-4cf6-b701-31a55d6870e8
  Args:
    source: :Vladimir_Kirillovich_of_Russia
    relation: :hasSister
    target: :Maria_Kirillovna
  AssignClass (d901f4f6-e75e-4ee1-bc2e-d26a114cf6cd)
 Call ID: d901f4f6-e75e-4ee1-bc2e-d26a114cf6cd
  Args:
    source: :Leonida_Georgievna_Bagration_Moukhransky
    type: :Woman
  AssignClass (0825edb4-4256-447e-a325-ce307656a21d)
 Call ID: 0825edb4-4256-447e-a325-ce307656a21d
  Args:
    source: :Leonida_Georgievna_Bagration_Moukhransky
    type: :Person
  AddTriple (36d13843-f5b4-4cff-a19c-0ccd38cb85c0)
 Call ID: 36d13843-f5b4-4cff-a19c-0ccd38cb85c0
  Args:
    source: :Vladimir_Kirillovich_of_Russia
    relation: :hasRelation
    target: :Leonida_Georgievna_Bagration_Moukhransky
  AddLiteral (67bc5b5d-920a-46e9-9fea-191d3b12ec18)
 Call ID: 67bc5b5d-920a-46e9-9fea-191d3b12ec18
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: :Vladimir_Kirillovich_of_Russia
    relation: :hasMarriageYear
  AssignClass (e32dd9fd-a7dd-4520-9eac-1fe4749daf31)
 Call ID: e32dd9fd-a7dd-4520-9eac-1fe4749daf31
  Args:
    source: :Maria_Vladimirovna
    type: :Woman
  AssignClass (7036ddcd-617b-44c8-8c20-aabf1afd0b79)
 Call ID: 7036ddcd-617b-44c8-8c20-aabf1afd0b79
  Args:
    source: :Maria_Vladimirovna
    type: :Person
  AddTriple (9ace209a-c727-416c-b453-065253b51eda)
 Call ID: 9ace209a-c727-416c-b453-065253b51eda
  Args:
    target: :Vladimir_Kirillovich_of_Russia
    relation: :isDaughterOf
    source: :Maria_Vladimirovna
  AddTriple (fccf89ae-1e0e-4d0e-81aa-73a6c8b39126)
 Call ID: fccf89ae-1e0e-4d0e-81aa-73a6c8b39126
  Args:
    relation: :hasMother
    target: :Leonida_Georgievna_Bagration_Moukhransky
    source: :Maria_Vladimirovna
  AssignClass (db8df80f-6202-4454-90ae-4fe5b6a4b312)
 Call ID: db8df80f-6202-4454-90ae-4fe5b6a4b312
  Args:
    type: :Woman
    source: :Beatrice_of_Orleans_Borbon
  AssignClass (7409eb81-2232-4f17-b12d-07e9dbabb256)
 Call ID: 7409eb81-2232-4f17-b12d-07e9dbabb256
  Args:
    source: :Beatrice_of_Orleans_Borbon
    type: :Person
  AddTriple (5d80259c-2799-42b5-82e9-4e698ad003db)
 Call ID: 5d80259c-2799-42b5-82e9-4e698ad003db
  Args:
    relation: :isAuntOf
    target: :Vladimir_Kirillovich_of_Russia
    source: :Beatrice_of_Orleans_Borbon
  AssignClass (eec0e047-2c00-47c3-b3b2-a717977d9a28)
 Call ID: eec0e047-2c00-47c3-b3b2-a717977d9a28
  Args:
    source: :Nicholas_Romanov
    type: :Man
  AssignClass (945c8d29-5daf-4036-80c0-ba59a0a9050d)
 Call ID: 945c8d29-5daf-4036-80c0-ba59a0a9050d
  Args:
    source: :Nicholas_Romanov
    type: :Person
  Finish (beebf431-6ae7-4e50-96f9-51487be1b4da)
 Call ID: beebf431-6ae7-4e50-96f9-51487be1b4da
  Args: