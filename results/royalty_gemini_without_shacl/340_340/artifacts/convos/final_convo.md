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
Princess Victoria Louise of Prussia (German: Viktoria Luise Adelheid Mathilde Charlotte; 13 September 1892 – 11 December 1980) was the only daughter and youngest child of Wilhelm II, and Augusta Victoria of Schleswig-Holstein.
Through her father, Victoria Louise was a great-granddaughter of Queen Victoria of the United Kingdom.
Victoria Louise's 1913 wedding to Prince Ernest Augustus of Hanover was the largest gathering of reigning monarchs in Germany since German unification in 1871, and one of the last great social events of European royalty before the First World War began fourteen months later.
Upon marriage, she became the Duchess of Brunswick.
Early life and education

Victoria Louise was born on 13 September 1892 at the Marmorpalais in Potsdam, the seventh child and only daughter of German Emperor Wilhelm II and Empress Augusta Victoria.
The princess was baptised in the Marble Gallery of the New Palace in Potsdam on 22 October, the birthday of the empress.
She was named Victoria after her paternal great-grandmother, Queen Victoria, and Louise after her paternal great-great-grandmother, Louise of Mecklenburg-Strelitz.
Known officially as Victoria Louise, she was nicknamed "Sissy" by her family.
Historian Justin C. Vovk writes that Victoria Louise was intelligent like her paternal grandmother Empress Frederick, stately and dignified like her mother, but imperious and willful like her father.
According to her eldest brother Crown Prince Wilhelm, Victoria Louise was "the only one of us who succeeded in her childhood in gaining a snug place" in their father's heart.
In 1902, her English governess, Anne Topham, observed in their first meeting that the nine-year-old princess was friendly, energetic, and always quarreling with her next eldest brother, Prince Joachim.
"


The family resided at Homburg Castle, and Victoria Louise and Joachim would often visit their cousins – the children of the Prussian princesses Margaret and Sophia – at nearby Kronberg Castle.
In 1905, the princess studied music with concert pianist Sandra Droucker.
For one week in May 1911, Victoria Louise traveled to England aboard the royal yacht Hohenzollern with her parents, where they visited their cousin George V, for the unveiling of a statue of Queen Victoria in front of Buckingham Palace.
The princess's confirmation took place at Friedenskirche in Potsdam on 18 October 1909.
Marriage

In 1912, Ernest Augustus, the wealthy heir-apparent to the title of Duke of Cumberland and Teviotdale, came to the Berlin court to thank Emperor Wilhelm for having Crown Prince Wilhelm and Prince Eitel Friedrich attend the funeral of his brother, Prince George William.
At the time, the House of Hanover lived in exile at Gmunden, Austria.
While in Berlin, Ernest Augustus met Victoria Louise and the two became smitten with each other.
However, any discussions of marriage were prolonged for months due to political concerns; Ernest Augustus was also the heir to the Kingdom of Hanover, which the Kingdom of Prussia annexed following the 1866 Austro-Prussian War.
The Prussian crown prince was displeased with the match and wished that Ernest Augustus would abdicate his rights to Hanover; in a compromise, it was decided that, in exchange, he would succeed to the smaller duchy of Brunswick, of which his father was the lawful heir.
The family had been barred from the succession to Brunswick due to their claims towards the Hanoverian kingdom.
Ernest and Victoria became engaged in Karlsruhe on 11 February 1913.
It was hailed in the press as the end of the rift between the House of Hanover and House of Hohenzollern that had existed since the 1866 annexation.
Despite press fixation on the union as a love match, whether the match was one of love or politics remains unclear; historian Eva Giloi believes that the marriage was more likely the result of Prussia's desire to end the rift, though Victoria Louise described it as a "love match” in one of her letters.
In a diplomatic gesture, Emperor Wilhelm invited almost all of his extended family.
He also pardoned and released two imprisoned British spies, Captain Bertrand Stewart and Captain Bernard Frederick Trench, as a present to the United Kingdom.
The wedding became the largest gathering of reigning monarchs in Germany since German unification in 1871, and one of the last great social events of European royalty before World War I began fourteen months later.
Attendees included Wilhelm's cousins George V and Tsar Nicholas II, who were also cousins of Ernest Augustus through their mothers.
Empress Augusta Victoria took the separation from her only daughter badly and wept.
In a 2003 documentary, Constantine II of Greece, a grandson of the couple, recounted that their wedding was "the last time all the heads of state of Europe met" before the start of World War I.


Husband and children

The new duke and duchess of Brunswick moved into Brunswick Palace in the capital of Brunswick and began their family with the birth of their eldest son, Prince Ernest Augustus (1914–1987), less than a year after their wedding.
They had four further children: Prince George William (1915–2006), Princess Frederica (1917–1981), Prince Christian Oscar (1919–1981), and Prince Welf Henry (1923–1997).
Through Frederica, Victoria Louise was a great-grandmother of Felipe VI of Spain.
On 8 November 1918, her husband was forced to abdicate his throne along with the other German kings, grand dukes, dukes, and princes, and the duchy of Brunswick was subsequently abolished.
The next year, he was deprived of his British peerages under the Titles Deprivation Act 1917 as a result of his service in the German army during the war.
Thus, when his father died in 1923, Ernest Augustus did not succeed to his father's British title of Duke of Cumberland.
Interwar years

For the next thirty years, Ernest Augustus remained the head of the House of Hanover, living in retirement on his various estates with his family, mainly Blankenburg Castle in Germany and Cumberland Castle in Gmunden, Austria.
He also owned Marienburg Castle near Hanover; however, the couple rarely lived there until 1945.
Several of Victoria Louise's brothers were early members of the Nazi party, including former Crown Prince Wilhelm and Prince August Wilhelm.
While Ernest Augustus never officially joined the party, he donated funds and was close to several leaders.
As a former British prince, Ernest Augustus as well as Victoria Louise desired a rapprochement between the United Kingdom and Germany.
Ostensibly desiring to pursue an alliance with the UK, in the mid-1930s, Adolf Hitler took advantage of their sentiment by asking the couple to arrange a match between their daughter Princess Frederica and the Prince of Wales.
The Duke and Duchess of Brunswick refused, believing that the age difference was too great; Princess Frederica would have been around 18 years of age while Edward was over 22 years older.
Following his brief reign as King Edward VIII in 1936 Edward, now Duke of Windsor, and his wife Wallis visited "the Cumberlands" at Cumberland Castle in Gmunden, Austria.
Instead, in 1938 Princess Frederica married her second cousin, the future King Paul of Greece.
World War II

In May 1941, her father fell ill from an intestinal blockage, and Victoria Louise traveled to Doorn to visit him, as did several of her brothers.
Wilhelm recovered enough for them to feel able to depart, but soon relapsed.
Victoria Louise returned in time to be at her father's bedside, along with nephew Louis Ferdinand and stepmother Hermine, when he died on 4 June 1941 of a pulmonary embolism.
By the time of the war's ending in Europe in April 1945, Victoria Louise was living with her husband at Blankenburg Castle.
Later life

After the war, Victoria Louise spent much of her time attending public events in Lower Saxony, supporting palace restoration projects, high-society parties, hunting, and the showing of horses.
Instead, she moved back to Brunswick, occupying a house which had been offered to her by a wealthy industrialist and a circle of fans called "Braunschweiger Freundeskreis" (circle of Brunswick friends).
In 1965 she published her autobiography Life as Daughter of the Emperor, and thereafter several other books, including biographies of her mother and of her sister-in-law Cecilie, the last crown princess of Germany.
She is buried next to her husband in front of the Royal Mausoleum in the Berggarten at Herrenhausen Gardens in Hanover, which is the burial chapel of Ernest Augustus, King of Hanover, and his wife and, since his reburial after World War II, also of George I of Great Britain.
A number of vessels were named after the princess:


Honours

Regimental commissions

Issue

married second 1981, Countess Monika zu Solms-Laubach; no issue.



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
  AssignClass (a93d3df9-5525-4007-9569-b85bd4d069ae)
 Call ID: a93d3df9-5525-4007-9569-b85bd4d069ae
  Args:
    source: Victoria_Louise
    type: :Woman
  AssignClass (8939d27a-9456-49da-a365-f7af804389eb)
 Call ID: 8939d27a-9456-49da-a365-f7af804389eb
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (39c75d96-c783-4b4c-9aab-4e68db25a84c)
 Call ID: 39c75d96-c783-4b4c-9aab-4e68db25a84c
  Args:
    source: Augusta_Victoria
    type: :Woman
  AssignClass (ba5843bd-294c-43f7-a51e-a9c9156afa72)
 Call ID: ba5843bd-294c-43f7-a51e-a9c9156afa72
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (b75c8160-92f6-4771-b788-a4b6db857c4f)
 Call ID: b75c8160-92f6-4771-b788-a4b6db857c4f
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (9912b3f6-5212-497d-8175-bc4336267e67)
 Call ID: 9912b3f6-5212-497d-8175-bc4336267e67
  Args:
    type: :Woman
    source: Louise_of_Mecklenburg-Strelitz
  AssignClass (4819219e-978e-4fe4-83b5-d88393ff6ee5)
 Call ID: 4819219e-978e-4fe4-83b5-d88393ff6ee5
  Args:
    source: Joachim
    type: :Man
  AssignClass (5d5e1277-e9dd-4f00-8b17-f3ef661e6bf3)
 Call ID: 5d5e1277-e9dd-4f00-8b17-f3ef661e6bf3
  Args:
    type: :Man
    source: George_V
  AssignClass (d53313af-bd2c-439b-9a3c-22fd45e2444e)
 Call ID: d53313af-bd2c-439b-9a3c-22fd45e2444e
  Args:
    source: Nicholas_II
    type: :Man
  AssignClass (49cfea5c-b6c6-44e1-a138-25ef58e4ef52)
 Call ID: 49cfea5c-b6c6-44e1-a138-25ef58e4ef52
  Args:
    source: Ernest_Augustus_Junior
    type: :Man
  AssignClass (310aec5b-abb6-4b2e-bc5a-3a6517262291)
 Call ID: 310aec5b-abb6-4b2e-bc5a-3a6517262291
  Args:
    type: :Man
    source: George_William
  AssignClass (a3efea6a-dfd3-4fa0-9546-425212effb13)
 Call ID: a3efea6a-dfd3-4fa0-9546-425212effb13
  Args:
    source: Frederica
    type: :Woman
  AssignClass (2dcd2d95-e925-463d-bd1c-30f5b4d1ce4b)
 Call ID: 2dcd2d95-e925-463d-bd1c-30f5b4d1ce4b
  Args:
    source: Christian_Oscar
    type: :Man
  AssignClass (71fe753c-2ee8-4e1d-b42f-36e499807611)
 Call ID: 71fe753c-2ee8-4e1d-b42f-36e499807611
  Args:
    source: Welf_Henry
    type: :Man
  AssignClass (1058f470-5753-492f-8597-461ab9ac6f92)
 Call ID: 1058f470-5753-492f-8597-461ab9ac6f92
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (1e8d6476-9e98-4f8f-9982-c45c0c758d60)
 Call ID: 1e8d6476-9e98-4f8f-9982-c45c0c758d60
  Args:
    source: Paul_of_Greece
    type: :Man
  AddLiteral (4975fb32-9ecb-455e-bf9b-21da648b92b9)
 Call ID: 4975fb32-9ecb-455e-bf9b-21da648b92b9
  Args:
    source: Victoria_Louise
    literal_value: 1892
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (dc2dd91c-051b-45fb-bd5e-e8d3cd8c8d89)
 Call ID: dc2dd91c-051b-45fb-bd5e-e8d3cd8c8d89
  Args:
    literal_value: 1980
    source: Victoria_Louise
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (bd56a341-f1ef-4d42-ac26-fddd014d3e77)
 Call ID: bd56a341-f1ef-4d42-ac26-fddd014d3e77
  Args:
    source: Victoria_Louise
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (c161a01b-0eec-4086-8ab0-176b0891540c)
 Call ID: c161a01b-0eec-4086-8ab0-176b0891540c
  Args:
    relation: :hasMother
    target: Augusta_Victoria
    source: Victoria_Louise
  AddTriple (29f62dfe-464a-4568-9072-dd0dbcb5174b)
 Call ID: 29f62dfe-464a-4568-9072-dd0dbcb5174b
  Args:
    source: Victoria_Louise
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (59d23b3d-fb29-4359-9568-dd917ace5c93)
 Call ID: 59d23b3d-fb29-4359-9568-dd917ace5c93
  Args:
    source: Victoria_Louise
    relation: :hasMother
    target: Augusta_Victoria
  AddTriple (e63ee016-de11-4a65-befe-48073c94459f)
 Call ID: e63ee016-de11-4a65-befe-48073c94459f
  Args:
    source: Wilhelm_II
    relation: :isFatherOf
    target: Victoria_Louise
  AddTriple (49a6dd3c-c679-4bc3-994b-ad468bb24f19)
 Call ID: 49a6dd3c-c679-4bc3-994b-ad468bb24f19
  Args:
    relation: :isMotherOf
    target: Victoria_Louise
    source: Augusta_Victoria
  AddTriple (2a4deb43-a6a7-4351-be15-2d41609a68d8)
 Call ID: 2a4deb43-a6a7-4351-be15-2d41609a68d8
  Args:
    source: Ernest_Augustus_Junior
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (b8988614-23b6-4439-9318-e89b3296dbd2)
 Call ID: b8988614-23b6-4439-9318-e89b3296dbd2
  Args:
    target: Victoria_Louise
    relation: :hasMother
    source: Ernest_Augustus_Junior
  AddTriple (cf7c3243-19fd-4b80-9b54-c7ec8a655b25)
 Call ID: cf7c3243-19fd-4b80-9b54-c7ec8a655b25
  Args:
    source: George_William
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (9698c001-ee52-461f-ac14-2a7fd3b2dc42)
 Call ID: 9698c001-ee52-461f-ac14-2a7fd3b2dc42
  Args:
    target: Victoria_Louise
    relation: :hasMother
    source: George_William
  AddTriple (dc201506-6ae0-4316-a84f-d64d8951208e)
 Call ID: dc201506-6ae0-4316-a84f-d64d8951208e
  Args:
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
    source: Frederica
  AddTriple (025773d7-3170-4c0a-a6da-1f0d66a669ec)
 Call ID: 025773d7-3170-4c0a-a6da-1f0d66a669ec
  Args:
    source: Frederica
    relation: :hasMother
    target: Victoria_Louise
  AddTriple (43285e37-0b56-4dea-a246-cb09a2cb810f)
 Call ID: 43285e37-0b56-4dea-a246-cb09a2cb810f
  Args:
    source: Christian_Oscar
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
  AddTriple (5119abee-d309-4528-be2f-b5092ba0d736)
 Call ID: 5119abee-d309-4528-be2f-b5092ba0d736
  Args:
    source: Christian_Oscar
    target: Victoria_Louise
    relation: :hasMother
  AddTriple (8e4f7b0c-b62e-446c-98be-0e9a5024cb19)
 Call ID: 8e4f7b0c-b62e-446c-98be-0e9a5024cb19
  Args:
    source: Welf_Henry
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (4445cb73-0e4b-44bf-9e73-82f2450d1183)
 Call ID: 4445cb73-0e4b-44bf-9e73-82f2450d1183
  Args:
    source: Welf_Henry
    target: Victoria_Louise
    relation: :hasMother
  AddTriple (8cddc5f7-799f-48cc-a11d-f0218dd84cb8)
 Call ID: 8cddc5f7-799f-48cc-a11d-f0218dd84cb8
  Args:
    relation: :hasBrother
    target: Joachim
    source: Victoria_Louise
  AddTriple (7ae44870-b45d-4d2a-9512-63a67e00e380)
 Call ID: 7ae44870-b45d-4d2a-9512-63a67e00e380
  Args:
    source: Joachim
    target: Victoria_Louise
    relation: :isBrotherOf
  AddTriple (44e42adf-b3f4-4705-8894-e402fdf22d60)
 Call ID: 44e42adf-b3f4-4705-8894-e402fdf22d60
  Args:
    target: Felipe_VI
    relation: :isFatherOf
    source: Paul_of_Greece
  AddTriple (26be237f-dbe5-4b57-aed8-6e7bfaeb1cf3)
 Call ID: 26be237f-dbe5-4b57-aed8-6e7bfaeb1cf3
  Args:
    target: Felipe_VI
    relation: :isMotherOf
    source: Frederica
  AddLiteral (2ea07373-83d1-4cdb-830d-14779c49c2b1)
 Call ID: 2ea07373-83d1-4cdb-830d-14779c49c2b1
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Victoria_Louise
    literal_value: 1913
  Finish (8eaad1a1-e124-4c26-8f9e-49a52917d58a)
 Call ID: 8eaad1a1-e124-4c26-8f9e-49a52917d58a
  Args: