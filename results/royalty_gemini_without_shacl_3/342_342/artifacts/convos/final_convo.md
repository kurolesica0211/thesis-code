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
  AssignClass (97206ba7-4b52-485b-8bbd-8d6e4dbdcec0)
 Call ID: 97206ba7-4b52-485b-8bbd-8d6e4dbdcec0
  Args:
    source: Wilhelm_Crown_Prince
    type: :Man
  AssignClass (582315c7-b889-485e-961d-f0022e328644)
 Call ID: 582315c7-b889-485e-961d-f0022e328644
  Args:
    source: Wilhelm_Crown_Prince
    type: :Person
  AddLiteral (99a78bd7-0437-48b7-9313-9b752d8a5c78)
 Call ID: 99a78bd7-0437-48b7-9313-9b752d8a5c78
  Args:
    source: Wilhelm_Crown_Prince
    literal_value: 1882
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (f09572ce-194e-4c2a-93a5-c5c35f85569a)
 Call ID: f09572ce-194e-4c2a-93a5-c5c35f85569a
  Args:
    literal_type: xsd:integer
    literal_value: 1951
    source: Wilhelm_Crown_Prince
    relation: :hasDeathYear
  AssignClass (236b9c11-c695-4f66-b297-d11b647e9792)
 Call ID: 236b9c11-c695-4f66-b297-d11b647e9792
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (e8944e3d-ad96-4f67-9ba6-51692e076c07)
 Call ID: e8944e3d-ad96-4f67-9ba6-51692e076c07
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (bacca284-2819-45c7-b353-b17061dd8110)
 Call ID: bacca284-2819-45c7-b353-b17061dd8110
  Args:
    type: :Woman
    source: Augusta_Victoria
  AssignClass (765767e5-c9ee-4f35-a07b-b529691ee8aa)
 Call ID: 765767e5-c9ee-4f35-a07b-b529691ee8aa
  Args:
    source: Augusta_Victoria
    type: :Person
  AddTriple (647c93fc-9138-421d-99c4-f71429c623a2)
 Call ID: 647c93fc-9138-421d-99c4-f71429c623a2
  Args:
    target: Wilhelm_II
    source: Wilhelm_Crown_Prince
    relation: :hasFather
  AddTriple (8f422335-b2bb-470b-960f-345252e86853)
 Call ID: 8f422335-b2bb-470b-960f-345252e86853
  Args:
    relation: :hasMother
    source: Wilhelm_Crown_Prince
    target: Augusta_Victoria
  AssignClass (60f77e0c-aae0-43cc-8af4-3a1b26d0fdff)
 Call ID: 60f77e0c-aae0-43cc-8af4-3a1b26d0fdff
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (53cd3af8-c7a4-4d16-99a6-c07fdd1e882d)
 Call ID: 53cd3af8-c7a4-4d16-99a6-c07fdd1e882d
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AddLiteral (7b595893-581a-4e98-bcf7-8ca58a6e7493)
 Call ID: 7b595893-581a-4e98-bcf7-8ca58a6e7493
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1905
    source: Wilhelm_Crown_Prince
  AddTriple (9d33fd35-90ac-415f-a85c-97a972f9c61f)
 Call ID: 9d33fd35-90ac-415f-a85c-97a972f9c61f
  Args:
    relation: :hasRelation
    target: Cecilie_of_Mecklenburg-Schwerin
    source: Wilhelm_Crown_Prince
  AssignClass (826f52eb-6585-4ff4-b412-58b43bdc0400)
 Call ID: 826f52eb-6585-4ff4-b412-58b43bdc0400
  Args:
    source: Frederick_Francis_III
    type: :Man
  AssignClass (65f6eeda-beae-44df-8b77-71f47cc73beb)
 Call ID: 65f6eeda-beae-44df-8b77-71f47cc73beb
  Args:
    type: :Person
    source: Frederick_Francis_III
  AssignClass (d7b9c1c5-7e5a-4e4e-a857-970798aaa66a)
 Call ID: d7b9c1c5-7e5a-4e4e-a857-970798aaa66a
  Args:
    source: Anastasia_Mikhailovna
    type: :Woman
  AssignClass (3b6693ec-1cdc-4d9e-88b8-ef2206aeec48)
 Call ID: 3b6693ec-1cdc-4d9e-88b8-ef2206aeec48
  Args:
    source: Anastasia_Mikhailovna
    type: :Person
  AddTriple (8053574b-bff0-4f02-825e-10721017bee1)
 Call ID: 8053574b-bff0-4f02-825e-10721017bee1
  Args:
    relation: :hasFather
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III
  AddTriple (ad88ab3b-e4b7-4fb2-99e3-2a9d65dd305d)
 Call ID: ad88ab3b-e4b7-4fb2-99e3-2a9d65dd305d
  Args:
    target: Anastasia_Mikhailovna
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (0c3d0501-6c6e-4dd0-8eba-3665aa3dc3fe)
 Call ID: 0c3d0501-6c6e-4dd0-8eba-3665aa3dc3fe
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (caa29b7f-7bcd-4bf1-b046-5386bfc45fff)
 Call ID: caa29b7f-7bcd-4bf1-b046-5386bfc45fff
  Args:
    source: Prince_Eitel_Friedrich
    type: :Person
  AssignClass (8c91ad4c-51e4-49f8-a7dc-2731bd578b45)
 Call ID: 8c91ad4c-51e4-49f8-a7dc-2731bd578b45
  Args:
    source: Prince_Adalbert
    type: :Man
  AssignClass (d554c7b6-9237-49f9-b8f5-ff6d0e96a955)
 Call ID: d554c7b6-9237-49f9-b8f5-ff6d0e96a955
  Args:
    type: :Person
    source: Prince_Adalbert
  AssignClass (e0b4bca5-f1e6-4c6a-9830-eea858656f1c)
 Call ID: e0b4bca5-f1e6-4c6a-9830-eea858656f1c
  Args:
    source: Prince_August_Wilhelm
    type: :Man
  AssignClass (994f3571-87c4-4dd0-8504-16d1cbd0c37a)
 Call ID: 994f3571-87c4-4dd0-8504-16d1cbd0c37a
  Args:
    type: :Person
    source: Prince_August_Wilhelm
  AssignClass (ca321473-a72b-49ea-ba5c-7cae4420a53e)
 Call ID: ca321473-a72b-49ea-ba5c-7cae4420a53e
  Args:
    type: :Man
    source: Prince_Oskar
  AssignClass (002fff1d-72fd-41fb-8fcc-bbe31350a284)
 Call ID: 002fff1d-72fd-41fb-8fcc-bbe31350a284
  Args:
    source: Prince_Oskar
    type: :Person
  AssignClass (7793255e-0498-4e98-8aa1-a87b7ab510b0)
 Call ID: 7793255e-0498-4e98-8aa1-a87b7ab510b0
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (de22a5af-88f5-4228-a814-efa39b66a4df)
 Call ID: de22a5af-88f5-4228-a814-efa39b66a4df
  Args:
    type: :Person
    source: Prince_Joachim
  AssignClass (de2cc4e1-e04e-4a6c-b8df-a396e42851d4)
 Call ID: de2cc4e1-e04e-4a6c-b8df-a396e42851d4
  Args:
    type: :Woman
    source: Princess_Viktoria_Luise
  AssignClass (8c03f090-08c5-4243-9f79-32cb7a08f9fd)
 Call ID: 8c03f090-08c5-4243-9f79-32cb7a08f9fd
  Args:
    type: :Person
    source: Princess_Viktoria_Luise
  AddTriple (8e4892cc-77b8-4d65-ae4c-366cff5461a3)
 Call ID: 8e4892cc-77b8-4d65-ae4c-366cff5461a3
  Args:
    target: Prince_Eitel_Friedrich
    source: Wilhelm_Crown_Prince
    relation: :hasBrother
  AddTriple (1dca639f-c56d-4009-a183-928f261479a7)
 Call ID: 1dca639f-c56d-4009-a183-928f261479a7
  Args:
    target: Prince_Adalbert
    source: Wilhelm_Crown_Prince
    relation: :hasBrother
  AddTriple (14b2d459-6aaa-4b9f-82a5-7ce199b1cd70)
 Call ID: 14b2d459-6aaa-4b9f-82a5-7ce199b1cd70
  Args:
    relation: :hasBrother
    target: Prince_August_Wilhelm
    source: Wilhelm_Crown_Prince
  AddTriple (94fa1867-396f-44e8-b070-35eb57d51e47)
 Call ID: 94fa1867-396f-44e8-b070-35eb57d51e47
  Args:
    relation: :hasBrother
    target: Prince_Oskar
    source: Wilhelm_Crown_Prince
  AddTriple (d1010be3-f920-407c-babf-14f58e2bbdbe)
 Call ID: d1010be3-f920-407c-babf-14f58e2bbdbe
  Args:
    source: Wilhelm_Crown_Prince
    target: Prince_Joachim
    relation: :hasBrother
  AddTriple (c9d8d86b-51fe-491b-8bff-1d00f000e9d9)
 Call ID: c9d8d86b-51fe-491b-8bff-1d00f000e9d9
  Args:
    relation: :hasSister
    source: Wilhelm_Crown_Prince
    target: Princess_Viktoria_Luise
  AssignClass (aab4e6c4-9c9b-4084-bd1b-3ff1c20da850)
 Call ID: aab4e6c4-9c9b-4084-bd1b-3ff1c20da850
  Args:
    source: Prince_Wilhelm_of_Prussia
    type: :Man
  AssignClass (29f14574-c65b-4eaa-a774-1d0b9fd7896e)
 Call ID: 29f14574-c65b-4eaa-a774-1d0b9fd7896e
  Args:
    source: Prince_Wilhelm_of_Prussia
    type: :Person
  AddTriple (840bc403-c1b5-4831-9dab-42d17b591b91)
 Call ID: 840bc403-c1b5-4831-9dab-42d17b591b91
  Args:
    relation: :hasSon
    target: Prince_Wilhelm_of_Prussia
    source: Wilhelm_Crown_Prince
  AddTriple (caa2b797-b147-466f-8732-f8d1162feb69)
 Call ID: caa2b797-b147-466f-8732-f8d1162feb69
  Args:
    source: Prince_Wilhelm_of_Prussia
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  Finish (282180b2-ca6a-4db1-bb84-8264cf9a9002)
 Call ID: 282180b2-ca6a-4db1-bb84-8264cf9a9002
  Args: