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
  AssignClass (b34d53b4-405f-4f67-9914-e3f839543c50)
 Call ID: b34d53b4-405f-4f67-9914-e3f839543c50
  Args:
    type: :Woman
    source: Victoria_Louise_of_Prussia
  AssignClass (90562ab2-c79d-49eb-ac9b-a994d9e1702f)
 Call ID: 90562ab2-c79d-49eb-ac9b-a994d9e1702f
  Args:
    type: :Person
    source: Victoria_Louise_of_Prussia
  AddLiteral (7584b15f-8c96-4471-93c4-f5f2c32dda3a)
 Call ID: 7584b15f-8c96-4471-93c4-f5f2c32dda3a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Victoria_Louise_of_Prussia
    literal_value: 1892
  AddLiteral (b1f3756f-cc2f-4c18-8043-9347ad6aaa60)
 Call ID: b1f3756f-cc2f-4c18-8043-9347ad6aaa60
  Args:
    literal_value: 1980
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Victoria_Louise_of_Prussia
  AddLiteral (32e51691-490a-451d-8770-76deced09da0)
 Call ID: 32e51691-490a-451d-8770-76deced09da0
  Args:
    source: Victoria_Louise_of_Prussia
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Sissy
  AssignClass (eeb26bca-8755-4422-82f1-e988cfd3dc6f)
 Call ID: eeb26bca-8755-4422-82f1-e988cfd3dc6f
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (dc2daf55-e755-4da4-ba41-9626060ae991)
 Call ID: dc2daf55-e755-4da4-ba41-9626060ae991
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (a85eea41-eca2-492e-9750-c462f5d310ab)
 Call ID: a85eea41-eca2-492e-9750-c462f5d310ab
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (c645fb36-b60f-498e-8c88-01d0e4b4669d)
 Call ID: c645fb36-b60f-498e-8c88-01d0e4b4669d
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (bedf3cc3-165b-4b2d-8089-65f8eb99f3dd)
 Call ID: bedf3cc3-165b-4b2d-8089-65f8eb99f3dd
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (bf4d9f5f-8f95-49f5-9afe-5c4bcc289962)
 Call ID: bf4d9f5f-8f95-49f5-9afe-5c4bcc289962
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :hasMother
    target: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (c948b501-327e-42a7-870f-16a120084825)
 Call ID: c948b501-327e-42a7-870f-16a120084825
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (326fb73b-9e20-4149-92b1-5add7460d6f0)
 Call ID: 326fb73b-9e20-4149-92b1-5add7460d6f0
  Args:
    type: :Person
    source: Ernest_Augustus_of_Hanover
  AddLiteral (566068fc-2ab4-4410-9ebf-6278190482af)
 Call ID: 566068fc-2ab4-4410-9ebf-6278190482af
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Victoria_Louise_of_Prussia
    literal_value: 1913
  AddTriple (dc4c1169-32d0-4dd8-97a0-f74fdc12a7f7)
 Call ID: dc4c1169-32d0-4dd8-97a0-f74fdc12a7f7
  Args:
    target: Ernest_Augustus_of_Hanover
    relation: :hasRelation
    source: Victoria_Louise_of_Prussia
  AssignClass (7bcb38c8-3a26-4f7b-b081-61e677258de6)
 Call ID: 7bcb38c8-3a26-4f7b-b081-61e677258de6
  Args:
    type: :Man
    source: Prince_Ernest_Augustus
  AssignClass (5b4dc4e2-2520-4501-bf6f-5994744449c9)
 Call ID: 5b4dc4e2-2520-4501-bf6f-5994744449c9
  Args:
    type: :Person
    source: Prince_Ernest_Augustus
  AssignClass (df443794-61cc-4bb1-973d-520caa5f517a)
 Call ID: df443794-61cc-4bb1-973d-520caa5f517a
  Args:
    type: :Man
    source: Prince_George_William
  AssignClass (82c4c1ff-53af-4bc3-b657-1cb392f32859)
 Call ID: 82c4c1ff-53af-4bc3-b657-1cb392f32859
  Args:
    type: :Person
    source: Prince_George_William
  AssignClass (27182138-d0ea-431e-afc7-9614095dccc3)
 Call ID: 27182138-d0ea-431e-afc7-9614095dccc3
  Args:
    type: :Woman
    source: Princess_Frederica
  AssignClass (a857603d-9c4d-4c74-8671-9c538f2667d0)
 Call ID: a857603d-9c4d-4c74-8671-9c538f2667d0
  Args:
    type: :Person
    source: Princess_Frederica
  AssignClass (00296ce9-1ece-4bbb-99be-acd31fa514fd)
 Call ID: 00296ce9-1ece-4bbb-99be-acd31fa514fd
  Args:
    type: :Man
    source: Prince_Christian_Oscar
  AssignClass (ddd2d648-390b-4dd5-a7e3-05372e755f0f)
 Call ID: ddd2d648-390b-4dd5-a7e3-05372e755f0f
  Args:
    type: :Person
    source: Prince_Christian_Oscar
  AssignClass (b5ce7786-cbfc-422e-961f-742996f125dc)
 Call ID: b5ce7786-cbfc-422e-961f-742996f125dc
  Args:
    type: :Man
    source: Prince_Welf_Henry
  AssignClass (0aef04da-c120-479f-8ac0-f85ace5c3e71)
 Call ID: 0aef04da-c120-479f-8ac0-f85ace5c3e71
  Args:
    type: :Person
    source: Prince_Welf_Henry
  AddTriple (cb70ce5b-02d4-42a2-ba7c-b8adc2faf68c)
 Call ID: cb70ce5b-02d4-42a2-ba7c-b8adc2faf68c
  Args:
    relation: :hasChild
    target: Prince_Ernest_Augustus
    source: Victoria_Louise_of_Prussia
  AddTriple (6282bb6a-8302-4a38-9145-8a78ab667189)
 Call ID: 6282bb6a-8302-4a38-9145-8a78ab667189
  Args:
    source: Victoria_Louise_of_Prussia
    target: Prince_George_William
    relation: :hasChild
  AddTriple (7d404f58-e073-42ea-8f72-c8856e6b700e)
 Call ID: 7d404f58-e073-42ea-8f72-c8856e6b700e
  Args:
    target: Princess_Frederica
    relation: :hasChild
    source: Victoria_Louise_of_Prussia
  AddTriple (3d10af31-dd2e-4acd-8f1b-36b58fd2fdf1)
 Call ID: 3d10af31-dd2e-4acd-8f1b-36b58fd2fdf1
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :hasChild
    target: Prince_Christian_Oscar
  AddTriple (6d5ae83e-a125-4bdf-b3a3-58b03d8eda71)
 Call ID: 6d5ae83e-a125-4bdf-b3a3-58b03d8eda71
  Args:
    source: Victoria_Louise_of_Prussia
    target: Prince_Welf_Henry
    relation: :hasChild
  AssignClass (936bec1c-4087-40cc-a0fc-a06ce26a669b)
 Call ID: 936bec1c-4087-40cc-a0fc-a06ce26a669b
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (cde28f83-8165-4c1d-9fc0-067a3f1d3302)
 Call ID: cde28f83-8165-4c1d-9fc0-067a3f1d3302
  Args:
    type: :Person
    source: Prince_Joachim
  AddTriple (4faf4903-e005-4c4d-bcf9-40f78c5f2290)
 Call ID: 4faf4903-e005-4c4d-bcf9-40f78c5f2290
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :hasBrother
    target: Prince_Joachim
  AssignClass (624254a2-5fd1-4138-9849-feb69ea2f413)
 Call ID: 624254a2-5fd1-4138-9849-feb69ea2f413
  Args:
    type: :Man
    source: Crown_Prince_Wilhelm
  AssignClass (259ff275-4b09-4f70-8545-7a1e20bd1bb4)
 Call ID: 259ff275-4b09-4f70-8545-7a1e20bd1bb4
  Args:
    type: :Person
    source: Crown_Prince_Wilhelm
  AddTriple (0f422150-ef87-46c2-807e-5acc6ad9a36f)
 Call ID: 0f422150-ef87-46c2-807e-5acc6ad9a36f
  Args:
    source: Victoria_Louise_of_Prussia
    target: Crown_Prince_Wilhelm
    relation: :hasBrother
  AssignClass (e716599d-0819-452d-80fb-5e9147ad0095)
 Call ID: e716599d-0819-452d-80fb-5e9147ad0095
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (e6fa29eb-85c1-456c-b0f3-99c069dd6341)
 Call ID: e6fa29eb-85c1-456c-b0f3-99c069dd6341
  Args:
    type: :Person
    source: Prince_Eitel_Friedrich
  AddTriple (5e2f2f17-ba96-481b-9f5e-cefdbefd792f)
 Call ID: 5e2f2f17-ba96-481b-9f5e-cefdbefd792f
  Args:
    source: Victoria_Louise_of_Prussia
    relation: :hasBrother
    target: Prince_Eitel_Friedrich
  AssignClass (99628624-26e3-48bf-ada5-e6361dfd6f5c)
 Call ID: 99628624-26e3-48bf-ada5-e6361dfd6f5c
  Args:
    type: :Man
    source: Prince_August_Wilhelm
  AssignClass (c6f4f2d7-7f17-4004-92ff-bf731b0e6c3b)
 Call ID: c6f4f2d7-7f17-4004-92ff-bf731b0e6c3b
  Args:
    type: :Person
    source: Prince_August_Wilhelm
  AddTriple (7eadd8a9-ca27-4aeb-81c4-a89f599788ce)
 Call ID: 7eadd8a9-ca27-4aeb-81c4-a89f599788ce
  Args:
    relation: :hasBrother
    target: Prince_August_Wilhelm
    source: Victoria_Louise_of_Prussia
  Finish (cf3d55b3-7b8f-4a8b-991f-778327b95f03)
 Call ID: cf3d55b3-7b8f-4a8b-991f-778327b95f03
  Args: