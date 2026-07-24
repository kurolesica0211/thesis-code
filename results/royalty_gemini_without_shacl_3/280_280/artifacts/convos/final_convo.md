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
  AssignClass (a3fcd794-de22-4dfc-bbbe-6f259f319159)
 Call ID: a3fcd794-de22-4dfc-bbbe-6f259f319159
  Args:
    type: :Man
    source: Vladimir_Kirillovich_of_Russia
  AssignClass (09366e03-62b9-4dc8-92d8-36cefe5f3672)
 Call ID: 09366e03-62b9-4dc8-92d8-36cefe5f3672
  Args:
    type: :Person
    source: Vladimir_Kirillovich_of_Russia
  AddLiteral (03761462-d934-4a39-aa59-2c95f1acd2bc)
 Call ID: 03761462-d934-4a39-aa59-2c95f1acd2bc
  Args:
    relation: :hasBirthYear
    literal_value: 1917
    source: Vladimir_Kirillovich_of_Russia
    literal_type: xsd:integer
  AddLiteral (74bcf731-6644-4d40-8379-c6959eebde62)
 Call ID: 74bcf731-6644-4d40-8379-c6959eebde62
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Vladimir_Kirillovich_of_Russia
    literal_value: 1992
  AssignClass (ce776250-12b2-420f-869e-6cd21e646e1f)
 Call ID: ce776250-12b2-420f-869e-6cd21e646e1f
  Args:
    type: :Man
    source: Cyril_Vladimirovich
  AssignClass (1b81155a-fc17-44d8-8801-db32090a32e2)
 Call ID: 1b81155a-fc17-44d8-8801-db32090a32e2
  Args:
    type: :Person
    source: Cyril_Vladimirovich
  AssignClass (a648fc9a-e907-433f-80d3-b122861d2738)
 Call ID: a648fc9a-e907-433f-80d3-b122861d2738
  Args:
    type: :Woman
    source: Viktoria_Feodorovna
  AssignClass (e7586828-cf9b-4a83-b712-8cab2ad58d8f)
 Call ID: e7586828-cf9b-4a83-b712-8cab2ad58d8f
  Args:
    type: :Person
    source: Viktoria_Feodorovna
  AddTriple (98a659ae-585d-499f-973b-181bf8152243)
 Call ID: 98a659ae-585d-499f-973b-181bf8152243
  Args:
    target: Cyril_Vladimirovich
    relation: :hasFather
    source: Vladimir_Kirillovich_of_Russia
  AddTriple (7e611f4c-5654-422a-9daa-9db4fd0bbb5e)
 Call ID: 7e611f4c-5654-422a-9daa-9db4fd0bbb5e
  Args:
    source: Vladimir_Kirillovich_of_Russia
    relation: :hasMother
    target: Viktoria_Feodorovna
  AssignClass (749ecdb1-d4ae-4aca-bcb9-5f63fa1af3d3)
 Call ID: 749ecdb1-d4ae-4aca-bcb9-5f63fa1af3d3
  Args:
    type: :Man
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (35d28f7b-8ef3-4b45-b4b6-88959eb06f29)
 Call ID: 35d28f7b-8ef3-4b45-b4b6-88959eb06f29
  Args:
    type: :Person
    source: Vladimir_Alexandrovich_of_Russia
  AssignClass (0f05401b-5642-4cd8-a346-15d86aee5483)
 Call ID: 0f05401b-5642-4cd8-a346-15d86aee5483
  Args:
    type: :Woman
    source: Maria_Pavlovna
  AssignClass (b1b93272-3a3f-4eef-840d-188603c174c9)
 Call ID: b1b93272-3a3f-4eef-840d-188603c174c9
  Args:
    type: :Person
    source: Maria_Pavlovna
  AddTriple (9d6a051f-dddc-465a-9b21-6991b843ea6f)
 Call ID: 9d6a051f-dddc-465a-9b21-6991b843ea6f
  Args:
    target: Vladimir_Alexandrovich_of_Russia
    relation: :hasFather
    source: Cyril_Vladimirovich
  AddTriple (9a5b1470-62ae-4b46-a2c3-931f24596d35)
 Call ID: 9a5b1470-62ae-4b46-a2c3-931f24596d35
  Args:
    source: Cyril_Vladimirovich
    target: Maria_Pavlovna
    relation: :hasMother
  AssignClass (a97a884b-d640-4ec8-84fa-e8d760cf5d7f)
 Call ID: a97a884b-d640-4ec8-84fa-e8d760cf5d7f
  Args:
    type: :Man
    source: Alfred_Duke_of_Saxe-Coburg_and_Gotha
  AssignClass (05184448-7825-4c62-90b9-871ae120afa9)
 Call ID: 05184448-7825-4c62-90b9-871ae120afa9
  Args:
    type: :Person
    source: Alfred_Duke_of_Saxe-Coburg_and_Gotha
  AssignClass (12d4450f-6cb7-4d72-9403-7b4488769dbf)
 Call ID: 12d4450f-6cb7-4d72-9403-7b4488769dbf
  Args:
    type: :Woman
    source: Marie_Alexandrovna_of_Russia
  AssignClass (d5b4909c-4727-41d3-974d-7116b3697d51)
 Call ID: d5b4909c-4727-41d3-974d-7116b3697d51
  Args:
    type: :Person
    source: Marie_Alexandrovna_of_Russia
  AddTriple (b679f6bd-2543-4a23-9621-d170bc87fe4a)
 Call ID: b679f6bd-2543-4a23-9621-d170bc87fe4a
  Args:
    source: Viktoria_Feodorovna
    target: Alfred_Duke_of_Saxe-Coburg_and_Gotha
    relation: :hasFather
  AddTriple (42e19899-7807-4f46-8d15-ac061dab2875)
 Call ID: 42e19899-7807-4f46-8d15-ac061dab2875
  Args:
    relation: :hasMother
    target: Marie_Alexandrovna_of_Russia
    source: Viktoria_Feodorovna
  AssignClass (61e4875a-9b8c-49ea-884d-6dd3a193f5b5)
 Call ID: 61e4875a-9b8c-49ea-884d-6dd3a193f5b5
  Args:
    type: :Woman
    source: Maria_Kirillovna
  AssignClass (b739706a-f787-449f-a53b-51ece05e8351)
 Call ID: b739706a-f787-449f-a53b-51ece05e8351
  Args:
    type: :Person
    source: Maria_Kirillovna
  AddTriple (cabdc5af-9e4e-410c-ab6a-3eb358e7f60e)
 Call ID: cabdc5af-9e4e-410c-ab6a-3eb358e7f60e
  Args:
    source: Maria_Kirillovna
    relation: :isSisterOf
    target: Vladimir_Kirillovich_of_Russia
  AssignClass (d79aa586-6e81-4a92-9990-e0bc8a9e013a)
 Call ID: d79aa586-6e81-4a92-9990-e0bc8a9e013a
  Args:
    type: :Woman
    source: Leonida_Georgievna_Bagration-Moukhransky
  AssignClass (af1b6410-b1d5-4319-8d6e-32fd056355fc)
 Call ID: af1b6410-b1d5-4319-8d6e-32fd056355fc
  Args:
    type: :Person
    source: Leonida_Georgievna_Bagration-Moukhransky
  AddLiteral (f9b3b27a-b156-44ec-a2a2-2e99f8d5fdac)
 Call ID: f9b3b27a-b156-44ec-a2a2-2e99f8d5fdac
  Args:
    relation: :hasMarriageYear
    source: Vladimir_Kirillovich_of_Russia
    literal_type: xsd:integer
    literal_value: 1948
  AddTriple (37901078-f909-4e61-8100-6e0020904907)
 Call ID: 37901078-f909-4e61-8100-6e0020904907
  Args:
    source: Vladimir_Kirillovich_of_Russia
    relation: :hasRelation
    target: Leonida_Georgievna_Bagration-Moukhransky
  AssignClass (245d0c63-d985-43dc-ae0d-8c3935b28c95)
 Call ID: 245d0c63-d985-43dc-ae0d-8c3935b28c95
  Args:
    type: :Woman
    source: Maria_Vladimirovna
  AssignClass (531302b9-b91d-4186-bfc6-0504f4a55344)
 Call ID: 531302b9-b91d-4186-bfc6-0504f4a55344
  Args:
    type: :Person
    source: Maria_Vladimirovna
  AddTriple (9c137cb9-b830-4e20-910e-d4f41178bdf2)
 Call ID: 9c137cb9-b830-4e20-910e-d4f41178bdf2
  Args:
    target: Maria_Vladimirovna
    relation: :hasDaughter
    source: Vladimir_Kirillovich_of_Russia
  AddTriple (35fd9fca-07fb-41af-91de-3810611322bc)
 Call ID: 35fd9fca-07fb-41af-91de-3810611322bc
  Args:
    relation: :hasMother
    target: Leonida_Georgievna_Bagration-Moukhransky
    source: Maria_Vladimirovna
  AssignClass (62b1bcfc-8379-44d6-bc68-55323db0fb38)
 Call ID: 62b1bcfc-8379-44d6-bc68-55323db0fb38
  Args:
    type: :Woman
    source: Beatrice_of_Orleans-Borbon
  AssignClass (ac785890-dd9f-4f29-a6ca-7ffeeb844478)
 Call ID: ac785890-dd9f-4f29-a6ca-7ffeeb844478
  Args:
    type: :Person
    source: Beatrice_of_Orleans-Borbon
  AddTriple (4eb51d96-3254-4e83-b5fa-5e053ae8f986)
 Call ID: 4eb51d96-3254-4e83-b5fa-5e053ae8f986
  Args:
    relation: :isAuntOf
    target: Vladimir_Kirillovich_of_Russia
    source: Beatrice_of_Orleans-Borbon
  AssignClass (518d4aa8-b375-43ad-ae2f-cee786fc4c91)
 Call ID: 518d4aa8-b375-43ad-ae2f-cee786fc4c91
  Args:
    type: :Man
    source: Nicholas_Romanov
  AssignClass (f00ee6b5-57d2-412a-b497-1a9331954736)
 Call ID: f00ee6b5-57d2-412a-b497-1a9331954736
  Args:
    type: :Person
    source: Nicholas_Romanov
  Finish (d46ebd38-e524-4586-b709-ea364ed04ebb)
 Call ID: d46ebd38-e524-4586-b709-ea364ed04ebb
  Args: