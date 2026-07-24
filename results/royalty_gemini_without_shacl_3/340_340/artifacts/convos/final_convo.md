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
  AssignClass (8b480a8d-cb62-4324-899b-ac2e6d9b4551)
 Call ID: 8b480a8d-cb62-4324-899b-ac2e6d9b4551
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (3b54206a-76c3-4c5a-acc0-1cf8b6408136)
 Call ID: 3b54206a-76c3-4c5a-acc0-1cf8b6408136
  Args:
    source: Victoria_Louise_of_Prussia
    type: :Person
  AddLiteral (60ee9429-1972-411c-a952-69520281ac31)
 Call ID: 60ee9429-1972-411c-a952-69520281ac31
  Args:
    relation: :hasBirthYear
    literal_value: 1892
    literal_type: xsd:integer
    source: Victoria_Louise_of_Prussia
  AddLiteral (3e941faa-7293-4219-83ca-a51fb03e4c3d)
 Call ID: 3e941faa-7293-4219-83ca-a51fb03e4c3d
  Args:
    literal_type: xsd:integer
    source: Victoria_Louise_of_Prussia
    relation: :hasDeathYear
    literal_value: 1980
  AddLiteral (fd885954-7b51-460d-be40-e534027890c8)
 Call ID: fd885954-7b51-460d-be40-e534027890c8
  Args:
    literal_value: Viktoria Luise Adelheid Mathilde Charlotte
    relation: :alsoKnownAs
    source: Victoria_Louise_of_Prussia
    literal_type: xsd:string
  AddLiteral (f0bbff3f-5d24-47b0-b844-7787419458ae)
 Call ID: f0bbff3f-5d24-47b0-b844-7787419458ae
  Args:
    literal_type: xsd:string
    source: Victoria_Louise_of_Prussia
    relation: :knownAs
    literal_value: Sissy
  AssignClass (51b65f1f-8192-492b-81a4-3c155ac4e960)
 Call ID: 51b65f1f-8192-492b-81a4-3c155ac4e960
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (52957801-63c5-448e-b6bd-1649c73a29c9)
 Call ID: 52957801-63c5-448e-b6bd-1649c73a29c9
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (8063031b-7894-46ad-9a19-c5eb4063a2bb)
 Call ID: 8063031b-7894-46ad-9a19-c5eb4063a2bb
  Args:
    source: Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (31f687bc-6554-4dee-b3f5-75ecf515b20d)
 Call ID: 31f687bc-6554-4dee-b3f5-75ecf515b20d
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (431b557d-5a9a-4a59-a333-f132b73dd339)
 Call ID: 431b557d-5a9a-4a59-a333-f132b73dd339
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (c5c4f923-f7c1-46bb-a246-60f542effd58)
 Call ID: c5c4f923-f7c1-46bb-a246-60f542effd58
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
    source: Victoria_Louise_of_Prussia
  AssignClass (49ca3f9c-fd24-4d82-9e42-71d76760a190)
 Call ID: 49ca3f9c-fd24-4d82-9e42-71d76760a190
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (2dfb2ca0-6743-4959-80d1-2ef9ae00794c)
 Call ID: 2dfb2ca0-6743-4959-80d1-2ef9ae00794c
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (afd1fc4d-7a58-4577-811c-d2b1a8f21b37)
 Call ID: afd1fc4d-7a58-4577-811c-d2b1a8f21b37
  Args:
    relation: :hasAncestor
    target: Queen_Victoria
    source: Victoria_Louise_of_Prussia
  AssignClass (220608b4-d79a-42a1-8108-69e88c9e8728)
 Call ID: 220608b4-d79a-42a1-8108-69e88c9e8728
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (6b926854-cc49-4cf3-8e09-a13312b0e71d)
 Call ID: 6b926854-cc49-4cf3-8e09-a13312b0e71d
  Args:
    type: :Person
    source: Ernest_Augustus_of_Hanover
  AddLiteral (f1319e7a-0025-4493-a260-7021a05ee237)
 Call ID: f1319e7a-0025-4493-a260-7021a05ee237
  Args:
    source: Victoria_Louise_of_Prussia
    literal_type: xsd:integer
    literal_value: 1913
    relation: :hasMarriageYear
  AddTriple (8e564be3-2819-42e1-8426-8c9fcbc36323)
 Call ID: 8e564be3-2819-42e1-8426-8c9fcbc36323
  Args:
    source: Victoria_Louise_of_Prussia
    target: Ernest_Augustus_of_Hanover
    relation: :hasRelation
  AssignClass (f41c8f82-b16a-4f9c-926f-1ed8a8244956)
 Call ID: f41c8f82-b16a-4f9c-926f-1ed8a8244956
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_1914
  AssignClass (a5a958f4-7518-48a6-b7c5-ceb744b57719)
 Call ID: a5a958f4-7518-48a6-b7c5-ceb744b57719
  Args:
    source: Prince_Ernest_Augustus_1914
    type: :Person
  AddTriple (8b5bb981-a9ed-481a-8c84-fe61ad90aa41)
 Call ID: 8b5bb981-a9ed-481a-8c84-fe61ad90aa41
  Args:
    source: Prince_Ernest_Augustus_1914
    relation: :hasMother
    target: Victoria_Louise_of_Prussia
  AddTriple (9dc6c114-641e-4cc3-8bbf-5b0869a38c60)
 Call ID: 9dc6c114-641e-4cc3-8bbf-5b0869a38c60
  Args:
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
    source: Prince_Ernest_Augustus_1914
  AssignClass (573e1c95-9d32-467a-8934-046b64f0d695)
 Call ID: 573e1c95-9d32-467a-8934-046b64f0d695
  Args:
    type: :Man
    source: Prince_George_William
  AssignClass (879c5ffd-e9e9-4307-b453-5697fbc06e38)
 Call ID: 879c5ffd-e9e9-4307-b453-5697fbc06e38
  Args:
    source: Prince_George_William
    type: :Person
  AddTriple (57814f25-fe82-4556-b8ba-3f5ea61e01f9)
 Call ID: 57814f25-fe82-4556-b8ba-3f5ea61e01f9
  Args:
    source: Prince_George_William
    target: Victoria_Louise_of_Prussia
    relation: :hasMother
  AddTriple (3702eac9-87be-47a6-b2ef-5812c56fc3a7)
 Call ID: 3702eac9-87be-47a6-b2ef-5812c56fc3a7
  Args:
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
    source: Prince_George_William
  AssignClass (3d731cc4-5af7-4964-96fd-aa74f9b29f53)
 Call ID: 3d731cc4-5af7-4964-96fd-aa74f9b29f53
  Args:
    type: :Woman
    source: Princess_Frederica
  AssignClass (ea7a3b35-342e-4ee9-aee7-bfd775e1ddd8)
 Call ID: ea7a3b35-342e-4ee9-aee7-bfd775e1ddd8
  Args:
    type: :Person
    source: Princess_Frederica
  AddTriple (922bdbc0-da58-437c-b44d-9311ea90c86b)
 Call ID: 922bdbc0-da58-437c-b44d-9311ea90c86b
  Args:
    source: Princess_Frederica
    target: Victoria_Louise_of_Prussia
    relation: :hasMother
  AddTriple (a9a4dc9e-f01b-45d7-aa94-3680b373ec77)
 Call ID: a9a4dc9e-f01b-45d7-aa94-3680b373ec77
  Args:
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
    source: Princess_Frederica
  AssignClass (77073394-045a-4063-b238-40f43df12651)
 Call ID: 77073394-045a-4063-b238-40f43df12651
  Args:
    source: Prince_Christian_Oscar
    type: :Man
  AssignClass (deb3a686-62c1-4d7c-82b4-9aebcc85fe2a)
 Call ID: deb3a686-62c1-4d7c-82b4-9aebcc85fe2a
  Args:
    type: :Person
    source: Prince_Christian_Oscar
  AddTriple (dd7bb3f4-987a-4f82-be21-e5bcc6bef5a4)
 Call ID: dd7bb3f4-987a-4f82-be21-e5bcc6bef5a4
  Args:
    relation: :hasMother
    target: Victoria_Louise_of_Prussia
    source: Prince_Christian_Oscar
  AddTriple (1dbf78b4-aa43-4cf7-ba0c-c7b9fcf878d1)
 Call ID: 1dbf78b4-aa43-4cf7-ba0c-c7b9fcf878d1
  Args:
    source: Prince_Christian_Oscar
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
  AssignClass (0c8238e9-9d80-479f-a7e5-c2588f04f68c)
 Call ID: 0c8238e9-9d80-479f-a7e5-c2588f04f68c
  Args:
    source: Prince_Welf_Henry
    type: :Man
  AssignClass (c0d58193-d10f-4a1b-b7ab-c203509e3c11)
 Call ID: c0d58193-d10f-4a1b-b7ab-c203509e3c11
  Args:
    source: Prince_Welf_Henry
    type: :Person
  AddTriple (4ea15d3e-2913-40aa-9187-a901e7f05a43)
 Call ID: 4ea15d3e-2913-40aa-9187-a901e7f05a43
  Args:
    source: Prince_Welf_Henry
    target: Victoria_Louise_of_Prussia
    relation: :hasMother
  AddTriple (d3da34b0-a30d-483e-8519-408acc00b592)
 Call ID: d3da34b0-a30d-483e-8519-408acc00b592
  Args:
    source: Prince_Welf_Henry
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
  AssignClass (7b263ed1-4c0b-4451-b066-13bf0ff22f0d)
 Call ID: 7b263ed1-4c0b-4451-b066-13bf0ff22f0d
  Args:
    type: :Man
    source: Crown_Prince_Wilhelm
  AssignClass (98112614-7179-43ee-80a4-a3b85ea0c9bc)
 Call ID: 98112614-7179-43ee-80a4-a3b85ea0c9bc
  Args:
    type: :Person
    source: Crown_Prince_Wilhelm
  AddTriple (28f3f792-4b7f-4166-bcf8-ae65961d258f)
 Call ID: 28f3f792-4b7f-4166-bcf8-ae65961d258f
  Args:
    relation: :isSiblingOf
    target: Crown_Prince_Wilhelm
    source: Victoria_Louise_of_Prussia
  AssignClass (8497e990-3306-499f-9345-03278fb19979)
 Call ID: 8497e990-3306-499f-9345-03278fb19979
  Args:
    source: Prince_Joachim
    type: :Man
  AssignClass (3e5dfbc5-ab70-48ac-8b0b-ddf03c99710e)
 Call ID: 3e5dfbc5-ab70-48ac-8b0b-ddf03c99710e
  Args:
    type: :Person
    source: Prince_Joachim
  AddTriple (1dbd627a-09d0-40c4-8a08-d49fb28a1af5)
 Call ID: 1dbd627a-09d0-40c4-8a08-d49fb28a1af5
  Args:
    source: Victoria_Louise_of_Prussia
    target: Prince_Joachim
    relation: :isSiblingOf
  AssignClass (bc9ef44e-390d-4a34-b08b-7f8d5f026548)
 Call ID: bc9ef44e-390d-4a34-b08b-7f8d5f026548
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (caf7f7ee-50d6-44ba-9d72-2ebb9152b9a6)
 Call ID: caf7f7ee-50d6-44ba-9d72-2ebb9152b9a6
  Args:
    type: :Person
    source: Prince_Eitel_Friedrich
  AddTriple (ee9c180c-ba15-410f-ba96-1979a7fe083b)
 Call ID: ee9c180c-ba15-410f-ba96-1979a7fe083b
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :isSiblingOf
    target: Prince_Eitel_Friedrich
  AssignClass (a5f75795-b50e-4539-8cbf-a47877d192ec)
 Call ID: a5f75795-b50e-4539-8cbf-a47877d192ec
  Args:
    type: :Man
    source: Prince_August_Wilhelm
  AssignClass (a2bd8b70-c9e8-40c3-baf3-694f1bd10c43)
 Call ID: a2bd8b70-c9e8-40c3-baf3-694f1bd10c43
  Args:
    type: :Person
    source: Prince_August_Wilhelm
  AddTriple (2cd3c9a1-f52c-42eb-9aa0-4c7306e80a4d)
 Call ID: 2cd3c9a1-f52c-42eb-9aa0-4c7306e80a4d
  Args:
    relation: :isSiblingOf
    target: Prince_August_Wilhelm
    source: Victoria_Louise_of_Prussia
  Finish (49de6d33-7f70-4140-a854-3b78bfda827c)
 Call ID: 49de6d33-7f70-4140-a854-3b78bfda827c
  Args: