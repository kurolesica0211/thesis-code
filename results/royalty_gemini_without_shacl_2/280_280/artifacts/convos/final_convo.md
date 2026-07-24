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
  AssignClass (19da4edf-8856-46d1-a018-489d39d349b4)
 Call ID: 19da4edf-8856-46d1-a018-489d39d349b4
  Args:
    type: :Man
    source: Vladimir_Kirillovich
  AssignClass (205d2de9-97f5-404d-a41e-52d7e35116d3)
 Call ID: 205d2de9-97f5-404d-a41e-52d7e35116d3
  Args:
    type: :Person
    source: Vladimir_Kirillovich
  AddLiteral (e9220cbc-8223-47cc-ba46-95f39179d07f)
 Call ID: e9220cbc-8223-47cc-ba46-95f39179d07f
  Args:
    literal_type: xsd:integer
    source: Vladimir_Kirillovich
    literal_value: 1917
    relation: :hasBirthYear
  AddLiteral (55ab3c12-6f74-46ae-87ac-7ab10067e68d)
 Call ID: 55ab3c12-6f74-46ae-87ac-7ab10067e68d
  Args:
    relation: :hasDeathYear
    source: Vladimir_Kirillovich
    literal_value: 1992
    literal_type: xsd:integer
  AssignClass (2820675a-9f46-4766-821c-564e9d64f55a)
 Call ID: 2820675a-9f46-4766-821c-564e9d64f55a
  Args:
    type: :Man
    source: Cyril_Vladimirovich
  AssignClass (28364b5d-93e2-4279-8a4a-a205233b299b)
 Call ID: 28364b5d-93e2-4279-8a4a-a205233b299b
  Args:
    type: :Person
    source: Cyril_Vladimirovich
  AssignClass (0d3778c7-5020-43ff-b02a-a2f527d89249)
 Call ID: 0d3778c7-5020-43ff-b02a-a2f527d89249
  Args:
    type: :Woman
    source: Viktoria_Feodorovna
  AssignClass (ffcf31e3-a728-4c14-8c2c-d7209bf5a22c)
 Call ID: ffcf31e3-a728-4c14-8c2c-d7209bf5a22c
  Args:
    type: :Person
    source: Viktoria_Feodorovna
  AddTriple (0cd5ab26-0108-47ee-aa4e-c6d93e09fdca)
 Call ID: 0cd5ab26-0108-47ee-aa4e-c6d93e09fdca
  Args:
    source: Vladimir_Kirillovich
    relation: :hasFather
    target: Cyril_Vladimirovich
  AddTriple (a7e3a336-ac73-457d-a12f-a528c7c9fd77)
 Call ID: a7e3a336-ac73-457d-a12f-a528c7c9fd77
  Args:
    target: Viktoria_Feodorovna
    relation: :hasMother
    source: Vladimir_Kirillovich
  AssignClass (77f8c785-9d22-414d-bff3-fc581530fba8)
 Call ID: 77f8c785-9d22-414d-bff3-fc581530fba8
  Args:
    type: :Man
    source: Vladimir_Alexandrovich
  AssignClass (8f38d5fb-9780-404f-974d-1fefd97e405e)
 Call ID: 8f38d5fb-9780-404f-974d-1fefd97e405e
  Args:
    type: :Person
    source: Vladimir_Alexandrovich
  AssignClass (a8284761-752e-4077-b6c7-a0d9121e9776)
 Call ID: a8284761-752e-4077-b6c7-a0d9121e9776
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (8f21be24-df2d-43de-83da-84b0e397a716)
 Call ID: 8f21be24-df2d-43de-83da-84b0e397a716
  Args:
    type: :Person
    source: Maria_Pavlovna
  AddTriple (6baecb40-70ec-4e86-98b4-cce12b87d202)
 Call ID: 6baecb40-70ec-4e86-98b4-cce12b87d202
  Args:
    target: Vladimir_Alexandrovich
    source: Cyril_Vladimirovich
    relation: :hasFather
  AddTriple (875657ed-6309-432d-9485-6dc96086852b)
 Call ID: 875657ed-6309-432d-9485-6dc96086852b
  Args:
    target: Maria_Pavlovna
    source: Cyril_Vladimirovich
    relation: :hasMother
  AssignClass (c4180a38-7db2-498b-8335-060c5f933eac)
 Call ID: c4180a38-7db2-498b-8335-060c5f933eac
  Args:
    type: :Man
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (75392523-98d9-4c40-b861-1e3b32d89b5e)
 Call ID: 75392523-98d9-4c40-b861-1e3b32d89b5e
  Args:
    type: :Person
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (bbcd8a7a-fde2-40af-a4cb-724b260b235c)
 Call ID: bbcd8a7a-fde2-40af-a4cb-724b260b235c
  Args:
    type: :Woman
    source: Marie_Alexandrovna
  AssignClass (fd3317bb-c0fd-4a34-943c-d87184a0ad81)
 Call ID: fd3317bb-c0fd-4a34-943c-d87184a0ad81
  Args:
    type: :Person
    source: Marie_Alexandrovna
  AddTriple (85587591-41fc-4cde-a424-cb14a5a25c17)
 Call ID: 85587591-41fc-4cde-a424-cb14a5a25c17
  Args:
    target: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    source: Viktoria_Feodorovna
    relation: :hasFather
  AddTriple (315d17b3-c33e-4c01-b1ab-cade5fb2499c)
 Call ID: 315d17b3-c33e-4c01-b1ab-cade5fb2499c
  Args:
    target: Marie_Alexandrovna
    relation: :hasMother
    source: Viktoria_Feodorovna
  AssignClass (77f45cfc-850e-4768-b165-fba47e8772e2)
 Call ID: 77f45cfc-850e-4768-b165-fba47e8772e2
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (31a428d8-3759-4278-a280-5d235a77081b)
 Call ID: 31a428d8-3759-4278-a280-5d235a77081b
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (3b0f55ea-6eee-457c-a84a-f1f2142b5e76)
 Call ID: 3b0f55ea-6eee-457c-a84a-f1f2142b5e76
  Args:
    relation: :hasMother
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    target: Queen_Victoria
  AssignClass (52bdf5a0-11d0-43b2-9f2b-432c1bf8acc7)
 Call ID: 52bdf5a0-11d0-43b2-9f2b-432c1bf8acc7
  Args:
    type: :Woman
    source: Maria_Kirillovna
  AssignClass (c6a0c0bb-9e2f-45dd-9754-325f7cfc0f48)
 Call ID: c6a0c0bb-9e2f-45dd-9754-325f7cfc0f48
  Args:
    type: :Person
    source: Maria_Kirillovna
  AddTriple (d6b67a61-a60c-4d40-b664-3f5d0bb197b8)
 Call ID: d6b67a61-a60c-4d40-b664-3f5d0bb197b8
  Args:
    relation: :isSisterOf
    source: Maria_Kirillovna
    target: Vladimir_Kirillovich
  AssignClass (7b737a61-da8d-4408-9740-7d737b1b492a)
 Call ID: 7b737a61-da8d-4408-9740-7d737b1b492a
  Args:
    type: :Woman
    source: Leonida_Georgievna_Bagration_Moukhransky
  AssignClass (a6d9deb6-b75c-4995-88d7-846c62e5527e)
 Call ID: a6d9deb6-b75c-4995-88d7-846c62e5527e
  Args:
    type: :Person
    source: Leonida_Georgievna_Bagration_Moukhransky
  AddTriple (4923eb01-283d-4216-a7bf-cd8c318d5ff7)
 Call ID: 4923eb01-283d-4216-a7bf-cd8c318d5ff7
  Args:
    source: Vladimir_Kirillovich
    relation: :hasRelation
    target: Leonida_Georgievna_Bagration_Moukhransky
  AddLiteral (6f719217-ff98-42cc-b29a-53d314fa4e66)
 Call ID: 6f719217-ff98-42cc-b29a-53d314fa4e66
  Args:
    literal_value: 1948
    relation: :hasMarriageYear
    source: Vladimir_Kirillovich
    literal_type: xsd:integer
  AssignClass (f3dcc8ef-2280-4f30-ae58-8ea46468a85e)
 Call ID: f3dcc8ef-2280-4f30-ae58-8ea46468a85e
  Args:
    type: :Woman
    source: Maria_Vladimirovna
  AssignClass (b334f7c8-faaa-4f30-a21d-e04a2331f448)
 Call ID: b334f7c8-faaa-4f30-a21d-e04a2331f448
  Args:
    type: :Person
    source: Maria_Vladimirovna
  AddTriple (0e6b77a1-471e-4489-aa50-9afa6bb69471)
 Call ID: 0e6b77a1-471e-4489-aa50-9afa6bb69471
  Args:
    source: Maria_Vladimirovna
    relation: :hasFather
    target: Vladimir_Kirillovich
  AddTriple (4b209d17-dafa-4161-ac44-f3636a7ebb4d)
 Call ID: 4b209d17-dafa-4161-ac44-f3636a7ebb4d
  Args:
    target: Leonida_Georgievna_Bagration_Moukhransky
    relation: :hasMother
    source: Maria_Vladimirovna
  AssignClass (e5f67758-3c24-4c93-994a-a49a726adac2)
 Call ID: e5f67758-3c24-4c93-994a-a49a726adac2
  Args:
    type: :Woman
    source: Beatrice_of_Orléans_Borbon
  AssignClass (47eba239-b4d2-4761-a09f-94455312ff84)
 Call ID: 47eba239-b4d2-4761-a09f-94455312ff84
  Args:
    type: :Person
    source: Beatrice_of_Orléans_Borbon
  AddTriple (bd6a15a0-70be-40dd-9e36-e12565796fee)
 Call ID: bd6a15a0-70be-40dd-9e36-e12565796fee
  Args:
    relation: :isAuntOf
    source: Beatrice_of_Orléans_Borbon
    target: Vladimir_Kirillovich
  AssignClass (daa6ff76-7929-4a22-b4b0-3c9478b29ad9)
 Call ID: daa6ff76-7929-4a22-b4b0-3c9478b29ad9
  Args:
    type: :Man
    source: Nicholas_Romanov
  AssignClass (87298b8d-1e75-43e6-acb6-1d532255953f)
 Call ID: 87298b8d-1e75-43e6-acb6-1d532255953f
  Args:
    type: :Person
    source: Nicholas_Romanov
  Finish (48d2b7e5-897c-4d0f-ad06-60466ae168bb)
 Call ID: 48d2b7e5-897c-4d0f-ad06-60466ae168bb
  Args: