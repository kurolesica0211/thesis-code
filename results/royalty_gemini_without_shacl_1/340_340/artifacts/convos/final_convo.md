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
  AssignClass (74bc55dc-bb62-4dd5-ad79-8217a2a8810d)
 Call ID: 74bc55dc-bb62-4dd5-ad79-8217a2a8810d
  Args:
    source: VictoriaLouiseOfPrussia
    type: :Woman
  AssignClass (536d65d3-4ab0-4c10-92e8-29a3d96f264c)
 Call ID: 536d65d3-4ab0-4c10-92e8-29a3d96f264c
  Args:
    type: :Person
    source: VictoriaLouiseOfPrussia
  AddLiteral (8e19a13f-47be-4db3-bb39-df655c281ff9)
 Call ID: 8e19a13f-47be-4db3-bb39-df655c281ff9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1892
    source: VictoriaLouiseOfPrussia
  AddLiteral (1fd190bc-6c8e-469a-963f-69fdf5f92e47)
 Call ID: 1fd190bc-6c8e-469a-963f-69fdf5f92e47
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1980
    source: VictoriaLouiseOfPrussia
  AddLiteral (28f038ee-9efd-4e48-843e-cf5f220b2168)
 Call ID: 28f038ee-9efd-4e48-843e-cf5f220b2168
  Args:
    source: VictoriaLouiseOfPrussia
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Sissy
  AssignClass (6f6af212-7e4b-4168-a1fd-26d5d3282215)
 Call ID: 6f6af212-7e4b-4168-a1fd-26d5d3282215
  Args:
    type: :Man
    source: WilhelmII
  AssignClass (3e759eab-c5a0-4067-b777-ac10a7cb88f1)
 Call ID: 3e759eab-c5a0-4067-b777-ac10a7cb88f1
  Args:
    type: :Person
    source: WilhelmII
  AssignClass (08d350a7-c283-40a8-ad7b-2bb86b0fcff5)
 Call ID: 08d350a7-c283-40a8-ad7b-2bb86b0fcff5
  Args:
    type: :Woman
    source: AugustaVictoriaOfSchleswigHolstein
  AssignClass (9574fb69-9cd6-42db-8d2b-882a7cb9d354)
 Call ID: 9574fb69-9cd6-42db-8d2b-882a7cb9d354
  Args:
    source: AugustaVictoriaOfSchleswigHolstein
    type: :Person
  AddTriple (28de12ce-e346-4bcd-9b45-cc686593fb28)
 Call ID: 28de12ce-e346-4bcd-9b45-cc686593fb28
  Args:
    source: VictoriaLouiseOfPrussia
    target: WilhelmII
    relation: :hasFather
  AddTriple (6ee53548-665c-4619-875e-7207ecea1dfe)
 Call ID: 6ee53548-665c-4619-875e-7207ecea1dfe
  Args:
    relation: :hasMother
    source: VictoriaLouiseOfPrussia
    target: AugustaVictoriaOfSchleswigHolstein
  AssignClass (357c1a70-b584-489f-a852-b2bfc90953f1)
 Call ID: 357c1a70-b584-489f-a852-b2bfc90953f1
  Args:
    type: :Woman
    source: QueenVictoria
  AssignClass (2bbbe5e1-53bf-46bf-9fe3-83c235d012bf)
 Call ID: 2bbbe5e1-53bf-46bf-9fe3-83c235d012bf
  Args:
    type: :Person
    source: QueenVictoria
  AddTriple (28f7230b-8e65-4133-bce8-af9a8255ec36)
 Call ID: 28f7230b-8e65-4133-bce8-af9a8255ec36
  Args:
    relation: :hasAncestor
    source: VictoriaLouiseOfPrussia
    target: QueenVictoria
  AssignClass (88b209ac-66b9-496a-a4df-a672202ba6eb)
 Call ID: 88b209ac-66b9-496a-a4df-a672202ba6eb
  Args:
    source: ErnestAugustusOfHanover
    type: :Man
  AssignClass (b960634b-ccc0-40ea-b02d-13fc5198dd11)
 Call ID: b960634b-ccc0-40ea-b02d-13fc5198dd11
  Args:
    source: ErnestAugustusOfHanover
    type: :Person
  AddLiteral (e30c5872-ee98-4c0c-aa54-434717da36b1)
 Call ID: e30c5872-ee98-4c0c-aa54-434717da36b1
  Args:
    source: VictoriaLouiseOfPrussia
    literal_value: 1913
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (ebd562be-f043-4e15-828d-379a470a335c)
 Call ID: ebd562be-f043-4e15-828d-379a470a335c
  Args:
    source: VictoriaLouiseOfPrussia
    target: ErnestAugustusOfHanover
    relation: :hasRelation
  AssignClass (a9c2aee5-d938-462a-a81c-c375a51f278b)
 Call ID: a9c2aee5-d938-462a-a81c-c375a51f278b
  Args:
    source: PrinceErnestAugustus
    type: :Man
  AssignClass (4afe83d2-6b39-49f2-9e0e-fb450a8fa2e5)
 Call ID: 4afe83d2-6b39-49f2-9e0e-fb450a8fa2e5
  Args:
    source: PrinceErnestAugustus
    type: :Person
  AddTriple (e0c3a14c-c92b-4f52-8149-3c83d4f769bb)
 Call ID: e0c3a14c-c92b-4f52-8149-3c83d4f769bb
  Args:
    relation: :hasSon
    source: VictoriaLouiseOfPrussia
    target: PrinceErnestAugustus
  AddTriple (5ed5607f-b564-4db8-a3de-74affcd597e3)
 Call ID: 5ed5607f-b564-4db8-a3de-74affcd597e3
  Args:
    relation: :hasFather
    target: ErnestAugustusOfHanover
    source: PrinceErnestAugustus
  AddTriple (a80078ba-ebd7-45e6-996d-79bb25a77b69)
 Call ID: a80078ba-ebd7-45e6-996d-79bb25a77b69
  Args:
    relation: :hasMother
    target: VictoriaLouiseOfPrussia
    source: PrinceErnestAugustus
  AssignClass (c7e534a7-1388-4241-a66f-31d84d0412a7)
 Call ID: c7e534a7-1388-4241-a66f-31d84d0412a7
  Args:
    type: :Man
    source: PrinceGeorgeWilliam
  AssignClass (e602507a-5c57-407f-9b06-3637eb107614)
 Call ID: e602507a-5c57-407f-9b06-3637eb107614
  Args:
    source: PrinceGeorgeWilliam
    type: :Person
  AddTriple (ad95b38a-ca39-4654-a697-b96d3ab2f412)
 Call ID: ad95b38a-ca39-4654-a697-b96d3ab2f412
  Args:
    relation: :hasSon
    source: VictoriaLouiseOfPrussia
    target: PrinceGeorgeWilliam
  AddTriple (bf5f5d62-fb57-4039-a110-812b4ebda745)
 Call ID: bf5f5d62-fb57-4039-a110-812b4ebda745
  Args:
    source: PrinceGeorgeWilliam
    target: ErnestAugustusOfHanover
    relation: :hasFather
  AddTriple (318206db-6bd0-4eed-af2f-9d5231ffa353)
 Call ID: 318206db-6bd0-4eed-af2f-9d5231ffa353
  Args:
    source: PrinceGeorgeWilliam
    target: VictoriaLouiseOfPrussia
    relation: :hasMother
  AssignClass (8f3b146b-fea4-4f66-8058-7660211a5127)
 Call ID: 8f3b146b-fea4-4f66-8058-7660211a5127
  Args:
    type: :Woman
    source: PrincessFrederica
  AssignClass (553c58f8-8056-4c46-a61f-5cb375735965)
 Call ID: 553c58f8-8056-4c46-a61f-5cb375735965
  Args:
    type: :Person
    source: PrincessFrederica
  AddTriple (ad9d543c-a11e-4a84-abd1-8f47b3320b92)
 Call ID: ad9d543c-a11e-4a84-abd1-8f47b3320b92
  Args:
    target: PrincessFrederica
    source: VictoriaLouiseOfPrussia
    relation: :hasDaughter
  AddTriple (787115f9-3923-4821-a148-8f98f05e004b)
 Call ID: 787115f9-3923-4821-a148-8f98f05e004b
  Args:
    source: PrincessFrederica
    target: ErnestAugustusOfHanover
    relation: :hasFather
  AddTriple (c8e7fd67-0199-4f87-994c-3a931b3b230f)
 Call ID: c8e7fd67-0199-4f87-994c-3a931b3b230f
  Args:
    source: PrincessFrederica
    target: VictoriaLouiseOfPrussia
    relation: :hasMother
  AssignClass (3699bc06-b7ba-41ea-95d1-3408c90b79a4)
 Call ID: 3699bc06-b7ba-41ea-95d1-3408c90b79a4
  Args:
    type: :Man
    source: PrinceChristianOscar
  AssignClass (64061455-d44f-46fc-941d-3f0d9238bf9a)
 Call ID: 64061455-d44f-46fc-941d-3f0d9238bf9a
  Args:
    type: :Person
    source: PrinceChristianOscar
  AddTriple (ae593c1b-01cf-44c7-a3b6-05734e7f88ec)
 Call ID: ae593c1b-01cf-44c7-a3b6-05734e7f88ec
  Args:
    relation: :hasSon
    target: PrinceChristianOscar
    source: VictoriaLouiseOfPrussia
  AddTriple (b43aee37-2117-400b-ae5c-2c5b9ed202f3)
 Call ID: b43aee37-2117-400b-ae5c-2c5b9ed202f3
  Args:
    relation: :hasFather
    target: ErnestAugustusOfHanover
    source: PrinceChristianOscar
  AddTriple (e5f18c20-772e-4e20-b605-1ba0cd519f7b)
 Call ID: e5f18c20-772e-4e20-b605-1ba0cd519f7b
  Args:
    relation: :hasMother
    source: PrinceChristianOscar
    target: VictoriaLouiseOfPrussia
  AssignClass (9476f983-8a1c-46a5-b5b1-6624288f74b6)
 Call ID: 9476f983-8a1c-46a5-b5b1-6624288f74b6
  Args:
    source: PrinceWelfHenry
    type: :Man
  AssignClass (0d0758cb-5053-4a1b-a781-5db62bedab11)
 Call ID: 0d0758cb-5053-4a1b-a781-5db62bedab11
  Args:
    source: PrinceWelfHenry
    type: :Person
  AddTriple (b66e8859-69ec-4c48-bd5d-b981ef2999ab)
 Call ID: b66e8859-69ec-4c48-bd5d-b981ef2999ab
  Args:
    target: PrinceWelfHenry
    source: VictoriaLouiseOfPrussia
    relation: :hasSon
  AddTriple (76560c41-1825-4c6d-87b4-25c1e98de676)
 Call ID: 76560c41-1825-4c6d-87b4-25c1e98de676
  Args:
    source: PrinceWelfHenry
    target: ErnestAugustusOfHanover
    relation: :hasFather
  AddTriple (5784ddb7-4a0b-4fc9-8aa5-cb9278026d5b)
 Call ID: 5784ddb7-4a0b-4fc9-8aa5-cb9278026d5b
  Args:
    target: VictoriaLouiseOfPrussia
    source: PrinceWelfHenry
    relation: :hasMother
  AssignClass (db12c57a-a2fb-4d4c-8a9f-3afde3fd77cf)
 Call ID: db12c57a-a2fb-4d4c-8a9f-3afde3fd77cf
  Args:
    type: :Man
    source: PrinceJoachim
  AssignClass (67b9e43d-a786-4d34-a9dc-0ce32df6e3ba)
 Call ID: 67b9e43d-a786-4d34-a9dc-0ce32df6e3ba
  Args:
    source: PrinceJoachim
    type: :Person
  AddTriple (f1d75b16-a4cf-4178-97d6-3f339e72b0b6)
 Call ID: f1d75b16-a4cf-4178-97d6-3f339e72b0b6
  Args:
    target: PrinceJoachim
    source: VictoriaLouiseOfPrussia
    relation: :isSiblingOf
  Finish (0630710c-c59d-497c-bb0b-23d2cceeefe7)
 Call ID: 0630710c-c59d-497c-bb0b-23d2cceeefe7
  Args: