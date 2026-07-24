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
  AssignClass (3f5a6b2d-d6ae-4e45-98fa-587eb8b08a8a)
 Call ID: 3f5a6b2d-d6ae-4e45-98fa-587eb8b08a8a
  Args:
    type: :Person
    source: Vladimir_Kirillovich
  AssignClass (2470fff8-da89-4b81-be46-032e0b283b8a)
 Call ID: 2470fff8-da89-4b81-be46-032e0b283b8a
  Args:
    type: :Man
    source: Vladimir_Kirillovich
  AddLiteral (c512cf41-be6d-4688-a791-a5f64dd1cd85)
 Call ID: c512cf41-be6d-4688-a791-a5f64dd1cd85
  Args:
    relation: :hasBirthYear
    source: Vladimir_Kirillovich
    literal_type: xsd:integer
    literal_value: 1917
  AddLiteral (37aaf798-f4e5-4a8f-ae6b-3694155c9433)
 Call ID: 37aaf798-f4e5-4a8f-ae6b-3694155c9433
  Args:
    source: Vladimir_Kirillovich
    literal_type: xsd:integer
    literal_value: 1992
    relation: :hasDeathYear
  AssignClass (822d1218-98ec-40d6-9c2e-bfb223792051)
 Call ID: 822d1218-98ec-40d6-9c2e-bfb223792051
  Args:
    type: :Person
    source: Cyril_Vladimirovich
  AssignClass (696260b7-333b-4d46-9b95-b30301be8c0c)
 Call ID: 696260b7-333b-4d46-9b95-b30301be8c0c
  Args:
    source: Cyril_Vladimirovich
    type: :Man
  AssignClass (f0a7efd4-19d7-4dba-89e1-472e061a90b6)
 Call ID: f0a7efd4-19d7-4dba-89e1-472e061a90b6
  Args:
    source: Viktoria_Feodorovna
    type: :Person
  AssignClass (064dcec2-5554-482b-975c-52c2fc692109)
 Call ID: 064dcec2-5554-482b-975c-52c2fc692109
  Args:
    type: :Woman
    source: Viktoria_Feodorovna
  AddTriple (c2772384-b6f3-4e94-988d-46665eeb99aa)
 Call ID: c2772384-b6f3-4e94-988d-46665eeb99aa
  Args:
    target: Cyril_Vladimirovich
    source: Vladimir_Kirillovich
    relation: :hasFather
  AddTriple (f94e38e5-4e2f-4506-abc1-5214fd99b48e)
 Call ID: f94e38e5-4e2f-4506-abc1-5214fd99b48e
  Args:
    relation: :hasMother
    source: Vladimir_Kirillovich
    target: Viktoria_Feodorovna
  AssignClass (bdd08eea-ea1d-409b-8818-0358819a6cfc)
 Call ID: bdd08eea-ea1d-409b-8818-0358819a6cfc
  Args:
    source: Vladimir_Alexandrovich
    type: :Person
  AssignClass (bcbe19e3-eb8e-4688-98bf-47716b7c8626)
 Call ID: bcbe19e3-eb8e-4688-98bf-47716b7c8626
  Args:
    source: Vladimir_Alexandrovich
    type: :Man
  AssignClass (ce7125bd-c3c0-4912-a1c5-d2269d7146f8)
 Call ID: ce7125bd-c3c0-4912-a1c5-d2269d7146f8
  Args:
    source: Maria_Pavlovna
    type: :Person
  AssignClass (1dbcecf6-325e-4780-82d9-aa73363f6146)
 Call ID: 1dbcecf6-325e-4780-82d9-aa73363f6146
  Args:
    source: Maria_Pavlovna
    type: :Woman
  AddTriple (6797ef5b-56e3-4b07-9c31-b511e0531ae8)
 Call ID: 6797ef5b-56e3-4b07-9c31-b511e0531ae8
  Args:
    relation: :hasFather
    source: Cyril_Vladimirovich
    target: Vladimir_Alexandrovich
  AddTriple (fe8f3bdb-7d2f-412a-a3e2-8abe7fe68001)
 Call ID: fe8f3bdb-7d2f-412a-a3e2-8abe7fe68001
  Args:
    relation: :hasMother
    source: Cyril_Vladimirovich
    target: Maria_Pavlovna
  AssignClass (f9b0d4ad-9c67-46ec-90db-32ab787ca63d)
 Call ID: f9b0d4ad-9c67-46ec-90db-32ab787ca63d
  Args:
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    type: :Person
  AssignClass (ed9a093d-e74f-42be-b28c-761b90c37fd4)
 Call ID: ed9a093d-e74f-42be-b28c-761b90c37fd4
  Args:
    type: :Man
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (6c986d82-a788-464c-9d9e-da694778df34)
 Call ID: 6c986d82-a788-464c-9d9e-da694778df34
  Args:
    type: :Person
    source: Marie_Alexandrovna
  AssignClass (81d0881d-3814-4bcf-9c94-ff86ff39a567)
 Call ID: 81d0881d-3814-4bcf-9c94-ff86ff39a567
  Args:
    source: Marie_Alexandrovna
    type: :Woman
  AddTriple (bb44d568-ec7a-4dd2-8651-f46fc4d4de34)
 Call ID: bb44d568-ec7a-4dd2-8651-f46fc4d4de34
  Args:
    relation: :hasFather
    source: Viktoria_Feodorovna
    target: Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AddTriple (4da2f909-a225-4326-accc-3c47cc7db7a6)
 Call ID: 4da2f909-a225-4326-accc-3c47cc7db7a6
  Args:
    source: Viktoria_Feodorovna
    relation: :hasMother
    target: Marie_Alexandrovna
  AssignClass (2ef061e1-91d6-4d29-9e6a-0ea53493928c)
 Call ID: 2ef061e1-91d6-4d29-9e6a-0ea53493928c
  Args:
    type: :Person
    source: Maria_Kirillovna
  AssignClass (369dbe79-9a32-4671-802d-d1757f5ff700)
 Call ID: 369dbe79-9a32-4671-802d-d1757f5ff700
  Args:
    source: Maria_Kirillovna
    type: :Woman
  AddTriple (ca44d390-8c3b-4101-bda1-379afd456b94)
 Call ID: ca44d390-8c3b-4101-bda1-379afd456b94
  Args:
    target: Maria_Kirillovna
    source: Vladimir_Kirillovich
    relation: :isSiblingOf
  AssignClass (7b2340fc-b91e-43e1-b8b2-3c93fa7f72b6)
 Call ID: 7b2340fc-b91e-43e1-b8b2-3c93fa7f72b6
  Args:
    source: Leonida_Georgievna_Bagration_Moukhransky
    type: :Person
  AssignClass (1ccfcb67-26a0-4555-ab59-2eb2f89edf62)
 Call ID: 1ccfcb67-26a0-4555-ab59-2eb2f89edf62
  Args:
    source: Leonida_Georgievna_Bagration_Moukhransky
    type: :Woman
  AddTriple (309d0901-3c99-4da8-a8ae-e8f1bc2c25b3)
 Call ID: 309d0901-3c99-4da8-a8ae-e8f1bc2c25b3
  Args:
    source: Vladimir_Kirillovich
    relation: :hasRelation
    target: Leonida_Georgievna_Bagration_Moukhransky
  AddLiteral (972ba252-04ca-4fc1-aa6a-f286a54b3005)
 Call ID: 972ba252-04ca-4fc1-aa6a-f286a54b3005
  Args:
    source: Vladimir_Kirillovich
    literal_value: 1948
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (9d0b42cf-f665-49cc-bbeb-69dd329556ab)
 Call ID: 9d0b42cf-f665-49cc-bbeb-69dd329556ab
  Args:
    type: :Person
    source: Maria_Vladimirovna
  AssignClass (a3eb9585-1445-4f31-85ee-bf930f503610)
 Call ID: a3eb9585-1445-4f31-85ee-bf930f503610
  Args:
    type: :Woman
    source: Maria_Vladimirovna
  AddTriple (038bfb4e-d71e-45ea-959c-d11fc626e8b6)
 Call ID: 038bfb4e-d71e-45ea-959c-d11fc626e8b6
  Args:
    target: Vladimir_Kirillovich
    source: Maria_Vladimirovna
    relation: :hasFather
  AddTriple (9e3bbd9d-de90-4e64-ada4-15a23b471edf)
 Call ID: 9e3bbd9d-de90-4e64-ada4-15a23b471edf
  Args:
    target: Leonida_Georgievna_Bagration_Moukhransky
    relation: :hasMother
    source: Maria_Vladimirovna
  AssignClass (72397310-ff12-4f16-b5c0-222fb85b3664)
 Call ID: 72397310-ff12-4f16-b5c0-222fb85b3664
  Args:
    type: :Person
    source: Beatrice_of_Orleans_Borbon
  AssignClass (b17c185a-baca-40e8-8923-6f1d90c643ba)
 Call ID: b17c185a-baca-40e8-8923-6f1d90c643ba
  Args:
    source: Beatrice_of_Orleans_Borbon
    type: :Woman
  AddTriple (612713e6-e980-4ead-9cc2-0458a5c2d97f)
 Call ID: 612713e6-e980-4ead-9cc2-0458a5c2d97f
  Args:
    source: Beatrice_of_Orleans_Borbon
    relation: :isAuntOf
    target: Vladimir_Kirillovich
  AssignClass (851847c8-fe78-4bea-9e1c-6ca8474bdeeb)
 Call ID: 851847c8-fe78-4bea-9e1c-6ca8474bdeeb
  Args:
    type: :Person
    source: Nicholas_Romanov
  AssignClass (6bb193e5-68e1-4162-a0ef-d6919b92b7d6)
 Call ID: 6bb193e5-68e1-4162-a0ef-d6919b92b7d6
  Args:
    source: Nicholas_Romanov
    type: :Man
  Finish (84f303a8-e066-4468-85d8-5753d8d11d30)
 Call ID: 84f303a8-e066-4468-85d8-5753d8d11d30
  Args: