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
  AssignClass (9fbb71a1-bfc6-4d26-825b-77a27ce413e6)
 Call ID: 9fbb71a1-bfc6-4d26-825b-77a27ce413e6
  Args:
    type: :Man
    source: Vladimir_Kirillovich_of_Russia
  AssignClass (ab082487-4bf5-4f62-a8a0-dd13807cb627)
 Call ID: ab082487-4bf5-4f62-a8a0-dd13807cb627
  Args:
    source: Vladimir_Kirillovich_of_Russia
    type: :Person
  AddLiteral (19c4d177-f9c4-47e9-ae59-19b47e183aab)
 Call ID: 19c4d177-f9c4-47e9-ae59-19b47e183aab
  Args:
    literal_type: xsd:integer
    literal_value: 1917
    relation: :hasBirthYear
    source: Vladimir_Kirillovich_of_Russia
  AddLiteral (d2b41f44-b88e-4b91-ad88-0b06d3969cd3)
 Call ID: d2b41f44-b88e-4b91-ad88-0b06d3969cd3
  Args:
    literal_type: xsd:integer
    literal_value: 1992
    relation: :hasDeathYear
    source: Vladimir_Kirillovich_of_Russia
  AssignClass (8cf5b047-c48d-45ee-a268-ee93cb3be4dd)
 Call ID: 8cf5b047-c48d-45ee-a268-ee93cb3be4dd
  Args:
    type: :Man
    source: Cyril_Vladimirovich
  AssignClass (06bdc463-c93c-43c0-b339-9099d081659b)
 Call ID: 06bdc463-c93c-43c0-b339-9099d081659b
  Args:
    source: Cyril_Vladimirovich
    type: :Person
  AssignClass (493f1b57-6070-4d51-b012-cf51da50e5b8)
 Call ID: 493f1b57-6070-4d51-b012-cf51da50e5b8
  Args:
    type: :Woman
    source: Viktoria_Feodorovna
  AssignClass (56675158-9ff0-4e8e-9893-849f6ddbf8c6)
 Call ID: 56675158-9ff0-4e8e-9893-849f6ddbf8c6
  Args:
    source: Viktoria_Feodorovna
    type: :Person
  AddTriple (7e48e2eb-c6dd-4389-b018-52a08c1ee408)
 Call ID: 7e48e2eb-c6dd-4389-b018-52a08c1ee408
  Args:
    target: Cyril_Vladimirovich
    source: Vladimir_Kirillovich_of_Russia
    relation: :hasFather
  AddTriple (27ddaef7-685e-4c08-bb5b-8c754deb5780)
 Call ID: 27ddaef7-685e-4c08-bb5b-8c754deb5780
  Args:
    source: Vladimir_Kirillovich_of_Russia
    relation: :hasMother
    target: Viktoria_Feodorovna
  AssignClass (39e3772c-b303-4575-97d2-8b4f198e43ad)
 Call ID: 39e3772c-b303-4575-97d2-8b4f198e43ad
  Args:
    type: :Man
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (571fcb9c-2efa-437f-8ec2-3e378a9f28a8)
 Call ID: 571fcb9c-2efa-437f-8ec2-3e378a9f28a8
  Args:
    type: :Person
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (b1729abb-466a-4b0d-85f1-8643da297fde)
 Call ID: b1729abb-466a-4b0d-85f1-8643da297fde
  Args:
    source: Maria_Pavlovna
    type: :Woman
  AssignClass (5f7a370b-ee9e-4ecd-ad39-f1698a11dba9)
 Call ID: 5f7a370b-ee9e-4ecd-ad39-f1698a11dba9
  Args:
    type: :Person
    source: Maria_Pavlovna
  AddTriple (2cf0cd36-6464-49de-82c4-f78ce030b2d2)
 Call ID: 2cf0cd36-6464-49de-82c4-f78ce030b2d2
  Args:
    target: Vladimir_Alexandrovich_of_Russia
    source: Cyril_Vladimirovich
    relation: :hasFather
  AddTriple (44b92b41-6dff-486c-a94c-0c5e7710f7a5)
 Call ID: 44b92b41-6dff-486c-a94c-0c5e7710f7a5
  Args:
    relation: :hasMother
    source: Cyril_Vladimirovich
    target: Maria_Pavlovna
  AssignClass (a968d4b7-a64c-4d8c-8470-dbd0c14c2561)
 Call ID: a968d4b7-a64c-4d8c-8470-dbd0c14c2561
  Args:
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    type: :Man
  AssignClass (a2707cba-0e92-4d1d-b59d-4238d9f0366d)
 Call ID: a2707cba-0e92-4d1d-b59d-4238d9f0366d
  Args:
    type: :Person
    source: Alfred_Duke_of_Saxe_Coburg_and_Gotha
  AssignClass (d237261a-7f5e-41c1-a51a-4a37a1620b46)
 Call ID: d237261a-7f5e-41c1-a51a-4a37a1620b46
  Args:
    type: :Woman
    source: Marie_Alexandrovna_of_Russia
  AssignClass (b3729c50-e1eb-42ca-8439-4c26cd9f987d)
 Call ID: b3729c50-e1eb-42ca-8439-4c26cd9f987d
  Args:
    type: :Person
    source: Marie_Alexandrovna_of_Russia
  AddTriple (0b052053-18c3-4845-b577-196c10e69c4a)
 Call ID: 0b052053-18c3-4845-b577-196c10e69c4a
  Args:
    target: Alfred_Duke_of_Saxe_Coburg_and_Gotha
    source: Viktoria_Feodorovna
    relation: :hasFather
  AddTriple (cb8434ac-4e0c-4160-9d94-5b583f640831)
 Call ID: cb8434ac-4e0c-4160-9d94-5b583f640831
  Args:
    source: Viktoria_Feodorovna
    relation: :hasMother
    target: Marie_Alexandrovna_of_Russia
  AssignClass (f1a30c30-3fa8-4139-ad67-54f64344fffa)
 Call ID: f1a30c30-3fa8-4139-ad67-54f64344fffa
  Args:
    source: Maria_Kirillovna
    type: :Woman
  AssignClass (d95f2c6f-f121-44b0-93d2-10e5ece2345a)
 Call ID: d95f2c6f-f121-44b0-93d2-10e5ece2345a
  Args:
    source: Maria_Kirillovna
    type: :Person
  AddTriple (c5b8ad54-313d-422b-bd71-cb753cfd0740)
 Call ID: c5b8ad54-313d-422b-bd71-cb753cfd0740
  Args:
    relation: :isSisterOf
    source: Maria_Kirillovna
    target: Vladimir_Kirillovich_of_Russia
  AssignClass (2cbf3c9d-c232-4ba4-8745-d73b107ae52f)
 Call ID: 2cbf3c9d-c232-4ba4-8745-d73b107ae52f
  Args:
    source: Leonida_Georgievna_Bagration_Moukhransky
    type: :Woman
  AssignClass (114b9930-e146-4acc-b7e9-94ba1f2c623f)
 Call ID: 114b9930-e146-4acc-b7e9-94ba1f2c623f
  Args:
    source: Leonida_Georgievna_Bagration_Moukhransky
    type: :Person
  AddTriple (46215363-e1ab-4c53-b510-a9de62b331bb)
 Call ID: 46215363-e1ab-4c53-b510-a9de62b331bb
  Args:
    target: Leonida_Georgievna_Bagration_Moukhransky
    relation: :hasRelation
    source: Vladimir_Kirillovich_of_Russia
  AddLiteral (161dd40f-afaf-4f4d-b121-3751cb46b338)
 Call ID: 161dd40f-afaf-4f4d-b121-3751cb46b338
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: Vladimir_Kirillovich_of_Russia
    relation: :hasMarriageYear
  AssignClass (f91f64d5-7e4b-4d7c-a550-167601097014)
 Call ID: f91f64d5-7e4b-4d7c-a550-167601097014
  Args:
    type: :Woman
    source: Maria_Vladimirovna
  AssignClass (4ae6a223-cff7-4ede-8b6c-86aad6821b6a)
 Call ID: 4ae6a223-cff7-4ede-8b6c-86aad6821b6a
  Args:
    source: Maria_Vladimirovna
    type: :Person
  AddTriple (e6c56955-a2f0-4791-8dcd-4d4d8f4b094e)
 Call ID: e6c56955-a2f0-4791-8dcd-4d4d8f4b094e
  Args:
    target: Vladimir_Kirillovich_of_Russia
    relation: :hasFather
    source: Maria_Vladimirovna
  AddTriple (6e80684f-241e-4968-8919-a0037203859d)
 Call ID: 6e80684f-241e-4968-8919-a0037203859d
  Args:
    relation: :hasMother
    source: Maria_Vladimirovna
    target: Leonida_Georgievna_Bagration_Moukhransky
  AssignClass (82d4720e-d340-4a5b-baa7-93723eef62e1)
 Call ID: 82d4720e-d340-4a5b-baa7-93723eef62e1
  Args:
    type: :Woman
    source: Beatrice_of_Orleans_Borbon
  AssignClass (8c5a6cc4-100f-4b5b-9ac8-d144194561f2)
 Call ID: 8c5a6cc4-100f-4b5b-9ac8-d144194561f2
  Args:
    type: :Person
    source: Beatrice_of_Orleans_Borbon
  AddTriple (c9a47289-16f8-4c46-9c3d-7d3a212f380e)
 Call ID: c9a47289-16f8-4c46-9c3d-7d3a212f380e
  Args:
    target: Marie_Alexandrovna_of_Russia
    relation: :isSisterOf
    source: Beatrice_of_Orleans_Borbon
  Finish (0a2004c9-3c86-4acd-9460-65bae0aa35eb)
 Call ID: 0a2004c9-3c86-4acd-9460-65bae0aa35eb
  Args: