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
  AssignClass (67fe15b7-4c0f-45cf-b97d-196a3ab6cd16)
 Call ID: 67fe15b7-4c0f-45cf-b97d-196a3ab6cd16
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (e2c6f8dd-2162-47ef-b1c5-566bc93cc48f)
 Call ID: e2c6f8dd-2162-47ef-b1c5-566bc93cc48f
  Args:
    type: :Person
    source: Victoria_Louise_of_Prussia
  AssignClass (5d4d0d58-79e4-44ce-8faa-3a818d53ce6c)
 Call ID: 5d4d0d58-79e4-44ce-8faa-3a818d53ce6c
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (d01a4f12-9710-4d43-b0ff-a8fb31bfc17f)
 Call ID: d01a4f12-9710-4d43-b0ff-a8fb31bfc17f
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (18c48ac1-71f8-43ec-8a3d-80ee94bea51e)
 Call ID: 18c48ac1-71f8-43ec-8a3d-80ee94bea51e
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (ee2f896a-5271-486f-8bbd-57a8ea8a2a9c)
 Call ID: ee2f896a-5271-486f-8bbd-57a8ea8a2a9c
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Person
  AddLiteral (4943e25e-d589-4695-8e3a-bce9682f465c)
 Call ID: 4943e25e-d589-4695-8e3a-bce9682f465c
  Args:
    literal_value: 1892
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Victoria_Louise_of_Prussia
  AddLiteral (16c9b3be-08de-4727-9e58-662ee32cce8d)
 Call ID: 16c9b3be-08de-4727-9e58-662ee32cce8d
  Args:
    source: Victoria_Louise_of_Prussia
    literal_type: xsd:integer
    literal_value: 1980
    relation: :hasDeathYear
  AddTriple (292b2290-7536-4b8c-8418-b592fffc7cd3)
 Call ID: 292b2290-7536-4b8c-8418-b592fffc7cd3
  Args:
    relation: :hasFather
    target: Wilhelm_II
    source: Victoria_Louise_of_Prussia
  AddTriple (9100ce5b-bbdb-4909-ab6d-9b4db2d95e05)
 Call ID: 9100ce5b-bbdb-4909-ab6d-9b4db2d95e05
  Args:
    relation: :hasMother
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Victoria_Louise_of_Prussia
  AddLiteral (b5040b3f-c199-488b-8e64-a9f9fb6edeef)
 Call ID: b5040b3f-c199-488b-8e64-a9f9fb6edeef
  Args:
    relation: :knownAs
    literal_value: Sissy
    literal_type: xsd:string
    source: Victoria_Louise_of_Prussia
  AssignClass (fc3ec461-18b6-403c-98ee-fe6957e9e124)
 Call ID: fc3ec461-18b6-403c-98ee-fe6957e9e124
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Man
  AssignClass (71564759-b43b-462d-b171-5d331f05f4ff)
 Call ID: 71564759-b43b-462d-b171-5d331f05f4ff
  Args:
    type: :Person
    source: Ernest_Augustus_of_Hanover
  AddLiteral (c1ed311b-e08a-4ed9-848c-9a25c68be0c9)
 Call ID: c1ed311b-e08a-4ed9-848c-9a25c68be0c9
  Args:
    relation: :hasMarriageYear
    literal_value: 1913
    source: Victoria_Louise_of_Prussia
    literal_type: xsd:integer
  AddTriple (3435e88c-0197-4d32-ac5f-5f549d1f3ec5)
 Call ID: 3435e88c-0197-4d32-ac5f-5f549d1f3ec5
  Args:
    source: Victoria_Louise_of_Prussia
    target: Ernest_Augustus_of_Hanover
    relation: :hasRelation
  AssignClass (a9dd55cf-8aca-47bd-957f-9d033c703002)
 Call ID: a9dd55cf-8aca-47bd-957f-9d033c703002
  Args:
    source: Prince_Ernest_Augustus_1914
    type: :Man
  AssignClass (8b5756bb-2b8f-4f0c-8103-02ec2ea860a0)
 Call ID: 8b5756bb-2b8f-4f0c-8103-02ec2ea860a0
  Args:
    source: Prince_Ernest_Augustus_1914
    type: :Person
  AddTriple (1d13011b-5e8c-43f2-a465-06f2ebf83394)
 Call ID: 1d13011b-5e8c-43f2-a465-06f2ebf83394
  Args:
    source: Prince_Ernest_Augustus_1914
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (c06e720a-2d15-46d1-94df-814c05ac74b1)
 Call ID: c06e720a-2d15-46d1-94df-814c05ac74b1
  Args:
    relation: :hasMother
    target: Victoria_Louise_of_Prussia
    source: Prince_Ernest_Augustus_1914
  AssignClass (54ab3c0c-f165-45c7-96cf-bd8ee0469e99)
 Call ID: 54ab3c0c-f165-45c7-96cf-bd8ee0469e99
  Args:
    type: :Man
    source: Prince_George_William_1915
  AssignClass (88d0dfb8-eda6-4170-860a-5173ccdaac7c)
 Call ID: 88d0dfb8-eda6-4170-860a-5173ccdaac7c
  Args:
    source: Prince_George_William_1915
    type: :Person
  AddTriple (9a165005-88ee-4cd1-90d7-e47b7d944491)
 Call ID: 9a165005-88ee-4cd1-90d7-e47b7d944491
  Args:
    target: Ernest_Augustus_of_Hanover
    source: Prince_George_William_1915
    relation: :hasFather
  AddTriple (57a58c19-8f62-4d0b-9800-dd542209f440)
 Call ID: 57a58c19-8f62-4d0b-9800-dd542209f440
  Args:
    relation: :hasMother
    source: Prince_George_William_1915
    target: Victoria_Louise_of_Prussia
  AssignClass (ba6dcfc2-bb9b-4dd3-bb6d-16c5e5b80c75)
 Call ID: ba6dcfc2-bb9b-4dd3-bb6d-16c5e5b80c75
  Args:
    type: :Woman
    source: Princess_Frederica_1917
  AssignClass (a4e8959d-2e78-4ed1-9e26-ef9fd37ac3cd)
 Call ID: a4e8959d-2e78-4ed1-9e26-ef9fd37ac3cd
  Args:
    type: :Person
    source: Princess_Frederica_1917
  AddTriple (72946ea5-7406-408c-9270-abe78fec354b)
 Call ID: 72946ea5-7406-408c-9270-abe78fec354b
  Args:
    source: Princess_Frederica_1917
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (34c6c906-e745-4788-9870-326c71971fee)
 Call ID: 34c6c906-e745-4788-9870-326c71971fee
  Args:
    relation: :hasMother
    target: Victoria_Louise_of_Prussia
    source: Princess_Frederica_1917
  AssignClass (437d7bb5-f8f3-47d7-a307-004604a47fe7)
 Call ID: 437d7bb5-f8f3-47d7-a307-004604a47fe7
  Args:
    type: :Man
    source: Prince_Christian_Oscar_1919
  AssignClass (814d4da8-505b-457c-a1ff-f485e52de314)
 Call ID: 814d4da8-505b-457c-a1ff-f485e52de314
  Args:
    source: Prince_Christian_Oscar_1919
    type: :Person
  AddTriple (dd0bdf64-9e6d-4edd-a9fb-2baeed9a6466)
 Call ID: dd0bdf64-9e6d-4edd-a9fb-2baeed9a6466
  Args:
    relation: :hasFather
    source: Prince_Christian_Oscar_1919
    target: Ernest_Augustus_of_Hanover
  AddTriple (77f5caf1-a7be-424a-b89c-1ea478a3d9bb)
 Call ID: 77f5caf1-a7be-424a-b89c-1ea478a3d9bb
  Args:
    relation: :hasMother
    source: Prince_Christian_Oscar_1919
    target: Victoria_Louise_of_Prussia
  AssignClass (2d9a50c3-d1fd-4776-85cd-f5a9851c38ef)
 Call ID: 2d9a50c3-d1fd-4776-85cd-f5a9851c38ef
  Args:
    type: :Man
    source: Prince_Welf_Henry_1923
  AssignClass (140606a3-5499-47ac-986b-bfc1179ab101)
 Call ID: 140606a3-5499-47ac-986b-bfc1179ab101
  Args:
    source: Prince_Welf_Henry_1923
    type: :Person
  AddTriple (86191086-f199-4232-9660-b644ae356f86)
 Call ID: 86191086-f199-4232-9660-b644ae356f86
  Args:
    source: Prince_Welf_Henry_1923
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (7e606857-442e-46ee-bdf9-36385e832b0c)
 Call ID: 7e606857-442e-46ee-bdf9-36385e832b0c
  Args:
    relation: :hasMother
    source: Prince_Welf_Henry_1923
    target: Victoria_Louise_of_Prussia
  AssignClass (d525bc3e-0709-4cef-aa28-2693311be9ab)
 Call ID: d525bc3e-0709-4cef-aa28-2693311be9ab
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (d9ff18a6-5af8-4d69-a4c8-e69388607c48)
 Call ID: d9ff18a6-5af8-4d69-a4c8-e69388607c48
  Args:
    type: :Person
    source: Prince_Joachim
  AddTriple (53b3a58c-d2ef-4bdc-a0f8-a584b950723e)
 Call ID: 53b3a58c-d2ef-4bdc-a0f8-a584b950723e
  Args:
    target: Wilhelm_II
    source: Prince_Joachim
    relation: :hasFather
  AddTriple (17c07126-cc5b-49a0-81d7-116d92b630f2)
 Call ID: 17c07126-cc5b-49a0-81d7-116d92b630f2
  Args:
    relation: :hasMother
    source: Prince_Joachim
    target: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (174d9154-3eb6-4f54-a573-09fee2f16e0b)
 Call ID: 174d9154-3eb6-4f54-a573-09fee2f16e0b
  Args:
    type: :Man
    source: Crown_Prince_Wilhelm
  AssignClass (9d3002ba-d69d-41e5-af77-b7965fe20fd2)
 Call ID: 9d3002ba-d69d-41e5-af77-b7965fe20fd2
  Args:
    source: Crown_Prince_Wilhelm
    type: :Person
  AddTriple (4ac6c125-5f3b-4c7e-88b6-4c1f617e85db)
 Call ID: 4ac6c125-5f3b-4c7e-88b6-4c1f617e85db
  Args:
    target: Wilhelm_II
    source: Crown_Prince_Wilhelm
    relation: :hasFather
  AddTriple (2a4310f3-d223-45b0-bc6a-74140dea6626)
 Call ID: 2a4310f3-d223-45b0-bc6a-74140dea6626
  Args:
    relation: :hasMother
    source: Crown_Prince_Wilhelm
    target: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (af4efab5-44c5-4cdc-b184-8c47d94f3274)
 Call ID: af4efab5-44c5-4cdc-b184-8c47d94f3274
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (ee93fa4f-db3e-4502-8a18-d63c7bec80b4)
 Call ID: ee93fa4f-db3e-4502-8a18-d63c7bec80b4
  Args:
    source: Prince_Eitel_Friedrich
    type: :Person
  AddTriple (1f56b3b8-fb0c-4207-a39c-13217c0ebe85)
 Call ID: 1f56b3b8-fb0c-4207-a39c-13217c0ebe85
  Args:
    target: Wilhelm_II
    source: Prince_Eitel_Friedrich
    relation: :hasFather
  AddTriple (3c656fba-2d6b-4339-bcb3-7d2be45e4d3a)
 Call ID: 3c656fba-2d6b-4339-bcb3-7d2be45e4d3a
  Args:
    relation: :hasMother
    source: Prince_Eitel_Friedrich
    target: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (2889e274-e8cf-4666-a217-8f76c0813d40)
 Call ID: 2889e274-e8cf-4666-a217-8f76c0813d40
  Args:
    type: :Man
    source: Prince_August_Wilhelm
  AssignClass (bc2bf183-ccd0-4cd8-a902-d75fec2c646f)
 Call ID: bc2bf183-ccd0-4cd8-a902-d75fec2c646f
  Args:
    type: :Person
    source: Prince_August_Wilhelm
  AddTriple (c12edf7f-78d8-4e12-9a5a-911f06eae73e)
 Call ID: c12edf7f-78d8-4e12-9a5a-911f06eae73e
  Args:
    target: Wilhelm_II
    source: Prince_August_Wilhelm
    relation: :hasFather
  AddTriple (56c6210b-e6b6-4000-977f-8dd8b6e27821)
 Call ID: 56c6210b-e6b6-4000-977f-8dd8b6e27821
  Args:
    relation: :hasMother
    source: Prince_August_Wilhelm
    target: Augusta_Victoria_of_Schleswig-Holstein
  Finish (0d3c3931-eaa5-4d80-bf5d-9feffbeb3eb7)
 Call ID: 0d3c3931-eaa5-4d80-bf5d-9feffbeb3eb7
  Args: