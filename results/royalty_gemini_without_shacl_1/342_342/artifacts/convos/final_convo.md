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
Wilhelm, German Crown Prince, Crown Prince of Prussia (Friedrich Wilhelm Victor August Ernst; 6 May 1882 – 20 July 1951), was the eldest child of the last German emperor, Wilhelm II, and his consort Augusta Victoria of Schleswig-Holstein.
As Emperor Wilhelm's heir, he was the last German Crown Prince and Crown Prince of Prussia, until the abolition of the monarchy.
Wilhelm became crown prince at the age of six in 1888, when his grandfather Frederick III died and his father became emperor.
He was crown prince for 30 years until his father's abdication and the fall of the empire on 9 November 1918.
During World War I, he commanded the 5th Army from 1914 to 1916 and was commander of the Army Group German Crown Prince for the remainder of the war.
After his plans to become President had been blocked by his father, Wilhelm supported Adolf Hitler's rise to power, but when Wilhelm realised that Hitler had no intention of restoring the monarchy, their relationship cooled.
Wilhelm became head of the House of Hohenzollern on 4 June 1941 following the death of his father and held the position until his own death on 20 July 1951.
Early life

Wilhelm was born on 6 May 1882 as the eldest son of the then Prince Wilhelm of Prussia, and his first wife, Princess Augusta Victoria of Schleswig-Holstein.
When he was born, his great-grandfather Wilhelm I was the German Emperor and his grandfather Crown Prince Frederick was the heir apparent, making Wilhelm third in line to the throne.
His birth sparked an argument between his parents and his grandmother Crown Princess Victoria.
Before Wilhelm was born, his grandmother had expected to be asked to help find a nurse, but since her son did everything he could to snub her, the future Wilhelm II asked his aunt Princess Helena to help instead.
His mother was hurt and his grandmother, Queen Victoria, who was the younger Wilhelm's great-grandmother, was furious.
Prince Wilhelm would have five younger brothers – Prince Eitel Friedrich, Prince Adalbert, Prince August Wilhelm, Prince Oskar and Prince Joachim – and one younger sister: Princess Viktoria Luise.
In 1888, the Year of the Three Emperors when his great-grandfather and grandfather both died, his father became German Emperor, and six-year-old Wilhelm became the heir apparent to the German and Prussian thrones with the title of crown prince.
He spent his school days with his brothers at the Prinzenhaus in Plön in his mother's ancestral Schleswig-Holstein.
Wilhelm was a supporter of association football, then a relatively new sport in the country, donating a cup to the German Football Association in 1908 and thereby initiating the Kronprinzenpokal (now Länderpokal), the oldest cup competition in German football.
The German club BFC Preussen was also originally named BFC Friedrich Wilhelm in his honour.
In 1914, the Kaiser ordered the construction of Schloss Cecilienhof in Potsdam for Prince Wilhelm and his family which angered him.
Completed in 1917, it became the main residence for the Crown Prince for a time.
World War I

Wilhelm had been active in pushing German expansion, and sought a leading role on the outbreak of war.
Despite being only thirty-two and having never commanded a unit larger than a regiment, the German crown prince was named commander of the 5th Army in August 1914, shortly after the outbreak of World War I.
However, under the well-established Prussian/German General Staff model then in use, inexperienced nobles who were afforded commands of large army formations were always provided with (and expected to defer to the advice of) experienced chiefs of staff to assist them in their duties.
As emperor, Wilhelm's father instructed the crown prince to defer to the advice of his experienced chief of staff Konstantin Schmidt von Knobelsdorf.
In October 1914 Wilhelm gave his first interview to a foreign correspondent and the first statement to the press made by a German noble since the outbreak of war.
He denied promoting military solutions to diplomatic problems, and said this in English:


Undoubtedly this is the most stupid, senseless and unnecessary war of modern times.
It is a war not wanted by Germany, I can assure you, but it was forced on us, and the fact that we were so effectually prepared to defend ourselves is now being used as an argument to convince the world that we desired conflict.

— Crown Prince Wilhelm, Wiegand

From August 1915 onwards, Wilhelm was given the additional role as commander of the Army Group German Crown Prince.
However, even these sorts of duties were essentially ceremonial with the actual planning of operations involving units under the Crown Prince's formal command being carried out by staff officers.
Wilhelm relinquished command of the 5th Army in November of that year, but remained commander of the Army Group German Crown Prince for the rest of the war.
1918–34

After the outbreak of the German Revolution in 1918, both Emperor Wilhelm II and the crown prince signed the document of abdication.
On 13 November, the former crown prince fled Germany, crossed into the Netherlands at Oudvroenhoven and was later interned on the island of Wieringen (now part of the mainland), near Den Helder.
In the autumn of 1921, Gustav Stresemann visited Wilhelm, and the former crown prince voiced an interest in returning to Germany, even as a private citizen.
After Stresemann became chancellor in August 1923, Wilhelm was allowed to return after giving assurances that he would not engage in politics.
A settlement between the state and the family made Cecilienhof property of the state but granted a right of residence to Wilhelm and his wife Cecilie.
9–12 


Wilhelm broke the promise he had made to Stresemann to stay out of politics.
Adolf Hitler visited Wilhelm at Cecilienhof three times, in 1926, in 1933 (on the "Day of Potsdam") and in 1935.
Wilhelm joined Der Stahlhelm, which merged in 1931 into the Harzburg Front, a right-wing organisation of those opposed to the democratic republic.
: 13 


The former crown prince was reportedly interested in the idea of running for President as the right-wing candidate against Paul von Hindenburg in 1932, until his father (who privately supported Hindenburg) forbade him from acting on the idea.
After this, Wilhelm supported Hitler's rise to power.
Schleicher, the former Chancellor, in the Night of the Long Knives, Wilhelm withdrew from all political activities.
When Wilhelm realised that Hitler had no intention of restoring the monarchy, their relationship cooled.
Upon his father's death in 1941, Wilhelm succeeded him as head of the House of Hohenzollern, the former German imperial dynasty.
He was approached by those in the military and the diplomatic service who wanted to replace Hitler, but Wilhelm turned them down.
After the ill-fated assassination attempt on 20 July 1944, Hitler nevertheless had Wilhelm placed under supervision by the Gestapo and had his home at Cecilienhof watched.:
11–15 


In January 1945, Wilhelm left Potsdam for Oberstdorf for a treatment of his gall and liver problems.
At the end of World War II in Europe, Wilhelm's home, Cecilienhof, was seized by the Soviets.:
16 


At the end of the war, Wilhelm was captured by French Moroccan troops in Baad, Austria, and was interned as a (World War I) war criminal.
Wilhelm and his wife are buried at Hohenzollern Castle.
Family and children

Wilhelm married his third cousin, Duchess Cecilie of Mecklenburg-Schwerin (20 September 1886 – 6 May 1954) in Berlin on 6 June 1905.
After their marriage, the couple lived at the Crown Prince's Palace in Berlin during the winter and at the Marmorpalais in Potsdam, later at Cecilienhof in Potsdam.
Cecilie was the daughter of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin (1851–1897) and his wife, Grand Duchess Anastasia Mikhailovna of Russia (1860–1922).
Their eldest son, Prince Wilhelm of Prussia, was killed fighting for the German Army in France in 1940.
Their children were:


In literature and popular culture

Wilhelm's reputation as a military commander was satirised by Neil Munro in his Erchie MacPherson story, "Bad News", first published in the Glasgow Evening News on 8 January 1917.



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
  AssignClass (6061558a-b8af-4dcd-ad62-7e7d22f69f9d)
 Call ID: 6061558a-b8af-4dcd-ad62-7e7d22f69f9d
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (a8bf4eb3-1865-4888-ae46-edcdd2f6a99d)
 Call ID: a8bf4eb3-1865-4888-ae46-edcdd2f6a99d
  Args:
    type: :Person
    source: Wilhelm_German_Crown_Prince
  AddLiteral (bce96011-6fc0-4293-89f4-503b3b5808ed)
 Call ID: bce96011-6fc0-4293-89f4-503b3b5808ed
  Args:
    relation: :hasBirthYear
    source: Wilhelm_German_Crown_Prince
    literal_value: 1882
    literal_type: xsd:integer
  AddLiteral (b794819c-fdbb-4f67-86a2-c51bfc56d323)
 Call ID: b794819c-fdbb-4f67-86a2-c51bfc56d323
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasDeathYear
    literal_value: 1951
    literal_type: xsd:integer
  AssignClass (f7050070-2953-477b-8705-6baefa61f88a)
 Call ID: f7050070-2953-477b-8705-6baefa61f88a
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (fb720c03-4417-4212-b8cf-579316a5f111)
 Call ID: fb720c03-4417-4212-b8cf-579316a5f111
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (9d7622a0-ad94-41ad-aab0-f5a1045ed2c9)
 Call ID: 9d7622a0-ad94-41ad-aab0-f5a1045ed2c9
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (7d5ddf1a-bc54-4872-9e3a-91c819aaa7bc)
 Call ID: 7d5ddf1a-bc54-4872-9e3a-91c819aaa7bc
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (d2d7c69d-3287-491d-ab07-c0e0b2543374)
 Call ID: d2d7c69d-3287-491d-ab07-c0e0b2543374
  Args:
    relation: :hasFather
    target: Wilhelm_II
    source: Wilhelm_German_Crown_Prince
  AddTriple (b842ada6-c856-49af-85b0-9b8e6446fac1)
 Call ID: b842ada6-c856-49af-85b0-9b8e6446fac1
  Args:
    relation: :hasMother
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Wilhelm_German_Crown_Prince
  AssignClass (6c8a0f6f-8ed0-4b53-8127-75bf48bcc0ba)
 Call ID: 6c8a0f6f-8ed0-4b53-8127-75bf48bcc0ba
  Args:
    source: Frederick_III
    type: :Man
  AssignClass (00cfea40-d137-47e3-9a8d-dd67baaad925)
 Call ID: 00cfea40-d137-47e3-9a8d-dd67baaad925
  Args:
    type: :Person
    source: Frederick_III
  AssignClass (eb6a2fa0-b2e4-4a86-93e3-2d6c96c53c1e)
 Call ID: eb6a2fa0-b2e4-4a86-93e3-2d6c96c53c1e
  Args:
    type: :Man
    source: Wilhelm_I
  AssignClass (fe801d37-7438-4865-b810-9988db7a9a10)
 Call ID: fe801d37-7438-4865-b810-9988db7a9a10
  Args:
    type: :Person
    source: Wilhelm_I
  AssignClass (316f5ce5-7f10-4ded-9a06-2fc17a68de2c)
 Call ID: 316f5ce5-7f10-4ded-9a06-2fc17a68de2c
  Args:
    source: Crown_Princess_Victoria
    type: :Woman
  AssignClass (01bf9996-a08a-4dd2-bd0b-caf6c1d3f30d)
 Call ID: 01bf9996-a08a-4dd2-bd0b-caf6c1d3f30d
  Args:
    source: Crown_Princess_Victoria
    type: :Person
  AssignClass (cf12441f-3392-4510-bed4-ba80dea6f1b3)
 Call ID: cf12441f-3392-4510-bed4-ba80dea6f1b3
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (6c3d4f94-2d84-4285-84b5-a0ae700bce64)
 Call ID: 6c3d4f94-2d84-4285-84b5-a0ae700bce64
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (d645fdd0-e2fa-4644-b9e6-2168af1e5273)
 Call ID: d645fdd0-e2fa-4644-b9e6-2168af1e5273
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (b785a6e3-fac9-40d7-83f2-30e4ba5c2b25)
 Call ID: b785a6e3-fac9-40d7-83f2-30e4ba5c2b25
  Args:
    type: :Person
    source: Prince_Eitel_Friedrich
  AssignClass (63ba4b70-576e-4228-b270-7834327922bc)
 Call ID: 63ba4b70-576e-4228-b270-7834327922bc
  Args:
    type: :Man
    source: Prince_Adalbert
  AssignClass (ee458637-e607-4c82-9c1b-bbf8d6b14074)
 Call ID: ee458637-e607-4c82-9c1b-bbf8d6b14074
  Args:
    source: Prince_Adalbert
    type: :Person
  AssignClass (3207dc35-0d3f-41fd-a168-a14c269566dc)
 Call ID: 3207dc35-0d3f-41fd-a168-a14c269566dc
  Args:
    source: Prince_August_Wilhelm
    type: :Man
  AssignClass (e5a8c87a-3ecf-4f0d-a7c2-1483e1c3c5b9)
 Call ID: e5a8c87a-3ecf-4f0d-a7c2-1483e1c3c5b9
  Args:
    type: :Person
    source: Prince_August_Wilhelm
  AssignClass (eebb2304-55be-423c-831b-c2b328a50ea6)
 Call ID: eebb2304-55be-423c-831b-c2b328a50ea6
  Args:
    source: Prince_Oskar
    type: :Man
  AssignClass (9f9e5f0f-e99a-4fea-9601-1c51e7dc7254)
 Call ID: 9f9e5f0f-e99a-4fea-9601-1c51e7dc7254
  Args:
    type: :Person
    source: Prince_Oskar
  AssignClass (a430f103-a632-4a3e-bf80-9f67708a8b42)
 Call ID: a430f103-a632-4a3e-bf80-9f67708a8b42
  Args:
    source: Prince_Joachim
    type: :Man
  AssignClass (54c0538d-f1d1-48b5-ae4b-6db572ceb8b0)
 Call ID: 54c0538d-f1d1-48b5-ae4b-6db572ceb8b0
  Args:
    type: :Person
    source: Prince_Joachim
  AssignClass (ff6e0490-4d84-4c54-bd5c-d5f2b4721766)
 Call ID: ff6e0490-4d84-4c54-bd5c-d5f2b4721766
  Args:
    source: Princess_Viktoria_Luise
    type: :Woman
  AssignClass (cabf14f3-2356-405f-a4e6-fc1b2069366c)
 Call ID: cabf14f3-2356-405f-a4e6-fc1b2069366c
  Args:
    source: Princess_Viktoria_Luise
    type: :Person
  AddTriple (6acb115d-d804-4bdb-82c9-f7cd90e36631)
 Call ID: 6acb115d-d804-4bdb-82c9-f7cd90e36631
  Args:
    relation: :isBrotherOf
    target: Wilhelm_German_Crown_Prince
    source: Prince_Eitel_Friedrich
  AddTriple (3699126b-47ec-447a-8082-97f8f76e5add)
 Call ID: 3699126b-47ec-447a-8082-97f8f76e5add
  Args:
    relation: :isBrotherOf
    source: Prince_Adalbert
    target: Wilhelm_German_Crown_Prince
  AddTriple (473ac1d8-75bd-4767-98e5-4ec31a7821ef)
 Call ID: 473ac1d8-75bd-4767-98e5-4ec31a7821ef
  Args:
    target: Wilhelm_German_Crown_Prince
    source: Prince_August_Wilhelm
    relation: :isBrotherOf
  AddTriple (dff762d3-aea8-409a-a5bb-4eb55269ba54)
 Call ID: dff762d3-aea8-409a-a5bb-4eb55269ba54
  Args:
    source: Prince_Oskar
    target: Wilhelm_German_Crown_Prince
    relation: :isBrotherOf
  AddTriple (fea64470-37d2-447b-ae00-563d6603d000)
 Call ID: fea64470-37d2-447b-ae00-563d6603d000
  Args:
    relation: :isBrotherOf
    target: Wilhelm_German_Crown_Prince
    source: Prince_Joachim
  AddTriple (e7ef3109-c5b8-4202-9a34-938027e9ecf5)
 Call ID: e7ef3109-c5b8-4202-9a34-938027e9ecf5
  Args:
    relation: :isSisterOf
    target: Wilhelm_German_Crown_Prince
    source: Princess_Viktoria_Luise
  AssignClass (ee65beae-48aa-4125-bc09-b333308ae45e)
 Call ID: ee65beae-48aa-4125-bc09-b333308ae45e
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (5d1c52f3-7704-4f65-9866-9dd05fa84874)
 Call ID: 5d1c52f3-7704-4f65-9866-9dd05fa84874
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddLiteral (aec76fd0-9389-411d-a121-75d4e1a1f28a)
 Call ID: aec76fd0-9389-411d-a121-75d4e1a1f28a
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Wilhelm_German_Crown_Prince
    literal_value: 1905
  AddTriple (2a587a9b-38d3-464b-ab83-94e714378f77)
 Call ID: 2a587a9b-38d3-464b-ab83-94e714378f77
  Args:
    source: Wilhelm_German_Crown_Prince
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasRelation
  AssignClass (bc6d6f3d-905f-4d1a-8907-5dac8d172fde)
 Call ID: bc6d6f3d-905f-4d1a-8907-5dac8d172fde
  Args:
    source: Prince_Wilhelm_of_Prussia_Son
    type: :Man
  AssignClass (5a04bdd4-c798-4c8b-834a-fe438637adc4)
 Call ID: 5a04bdd4-c798-4c8b-834a-fe438637adc4
  Args:
    source: Prince_Wilhelm_of_Prussia_Son
    type: :Person
  AddTriple (2c3cadcf-f979-44ab-8892-a1c5451c8180)
 Call ID: 2c3cadcf-f979-44ab-8892-a1c5451c8180
  Args:
    relation: :hasFather
    source: Prince_Wilhelm_of_Prussia_Son
    target: Wilhelm_German_Crown_Prince
  AddTriple (53facf8c-eaae-4251-a08b-4b6c71118369)
 Call ID: 53facf8c-eaae-4251-a08b-4b6c71118369
  Args:
    source: Prince_Wilhelm_of_Prussia_Son
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (7c8a6328-b8d7-4d3a-b8c6-83b29f562dd6)
 Call ID: 7c8a6328-b8d7-4d3a-b8c6-83b29f562dd6
  Args:
    source: Frederick_Francis_III
    type: :Man
  AssignClass (faa88505-dc81-4773-af18-73563c42d9fe)
 Call ID: faa88505-dc81-4773-af18-73563c42d9fe
  Args:
    type: :Person
    source: Frederick_Francis_III
  AssignClass (8ed571f7-e9b8-49cc-bbf7-24b8782c31a6)
 Call ID: 8ed571f7-e9b8-49cc-bbf7-24b8782c31a6
  Args:
    source: Anastasia_Mikhailovna
    type: :Woman
  AssignClass (9defe865-aeea-4e87-b87d-fe15d6d16dd3)
 Call ID: 9defe865-aeea-4e87-b87d-fe15d6d16dd3
  Args:
    type: :Person
    source: Anastasia_Mikhailovna
  AddTriple (8634e99e-9b5e-4d41-a911-e237b1f3ceb9)
 Call ID: 8634e99e-9b5e-4d41-a911-e237b1f3ceb9
  Args:
    relation: :hasFather
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III
  AddTriple (cf7e8244-9b74-4399-9104-1846b9e21c66)
 Call ID: cf7e8244-9b74-4399-9104-1846b9e21c66
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Anastasia_Mikhailovna
    relation: :hasMother
  Finish (7d5213f6-28f1-47d8-adb8-6de011a732d5)
 Call ID: 7d5213f6-28f1-47d8-adb8-6de011a732d5
  Args: