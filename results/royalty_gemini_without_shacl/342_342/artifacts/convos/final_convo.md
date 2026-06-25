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
  AssignClass (597023d0-a0f8-4337-ba39-d39c3907ee4a)
 Call ID: 597023d0-a0f8-4337-ba39-d39c3907ee4a
  Args:
    type: :Man
    source: :Wilhelm_Crown_Prince
  AssignClass (ff25ac61-c237-4106-8b5c-50a43c01e3fd)
 Call ID: ff25ac61-c237-4106-8b5c-50a43c01e3fd
  Args:
    source: :Wilhelm_Crown_Prince
    type: :Person
  AddLiteral (e7c1b2e5-b1d5-4f39-bf15-6ff66e2a6507)
 Call ID: e7c1b2e5-b1d5-4f39-bf15-6ff66e2a6507
  Args:
    relation: :hasBirthYear
    literal_value: 1882
    source: :Wilhelm_Crown_Prince
    literal_type: xsd:integer
  AddLiteral (fbd16dae-4b18-4744-913b-5e011c086958)
 Call ID: fbd16dae-4b18-4744-913b-5e011c086958
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Wilhelm_Crown_Prince
    literal_value: 1951
  AssignClass (0ce7cfb8-50bd-4f32-8c9a-87c3c87f30c4)
 Call ID: 0ce7cfb8-50bd-4f32-8c9a-87c3c87f30c4
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (5f07585a-4f98-47bc-84f9-dd3340764f42)
 Call ID: 5f07585a-4f98-47bc-84f9-dd3340764f42
  Args:
    source: :Wilhelm_II
    type: :Person
  AssignClass (af57b338-5bf8-4317-b7c7-6e776030084a)
 Call ID: af57b338-5bf8-4317-b7c7-6e776030084a
  Args:
    type: :Woman
    source: :Augusta_Victoria
  AssignClass (a437829d-0781-45cf-bfae-e7a2f2274811)
 Call ID: a437829d-0781-45cf-bfae-e7a2f2274811
  Args:
    source: :Augusta_Victoria
    type: :Person
  AddTriple (55464764-53fe-4dd1-9fbc-a4e35709a897)
 Call ID: 55464764-53fe-4dd1-9fbc-a4e35709a897
  Args:
    relation: :hasFather
    source: :Wilhelm_Crown_Prince
    target: :Wilhelm_II
  AddTriple (1f96a258-70f0-48e7-8d01-321476c9761d)
 Call ID: 1f96a258-70f0-48e7-8d01-321476c9761d
  Args:
    target: :Augusta_Victoria
    source: :Wilhelm_Crown_Prince
    relation: :hasMother
  AssignClass (f52e7737-b48b-4649-94eb-833ec07ca6e2)
 Call ID: f52e7737-b48b-4649-94eb-833ec07ca6e2
  Args:
    type: :Man
    source: :Eitel_Friedrich
  AssignClass (28366fe0-77a0-4c69-9b4d-2ca303169900)
 Call ID: 28366fe0-77a0-4c69-9b4d-2ca303169900
  Args:
    source: :Eitel_Friedrich
    type: :Person
  AddTriple (8e7cf525-d8c2-48e3-ad3a-d6ac6263d30e)
 Call ID: 8e7cf525-d8c2-48e3-ad3a-d6ac6263d30e
  Args:
    target: :Eitel_Friedrich
    relation: :hasBrother
    source: :Wilhelm_Crown_Prince
  AssignClass (19b337da-7c9b-47e8-8b54-a618c3d48177)
 Call ID: 19b337da-7c9b-47e8-8b54-a618c3d48177
  Args:
    type: :Man
    source: :Adalbert
  AssignClass (27c83519-3673-4102-a7c9-a8561821572e)
 Call ID: 27c83519-3673-4102-a7c9-a8561821572e
  Args:
    source: :Adalbert
    type: :Person
  AddTriple (77d29ea7-7f52-469c-8072-a22402b0dfbf)
 Call ID: 77d29ea7-7f52-469c-8072-a22402b0dfbf
  Args:
    target: :Adalbert
    relation: :hasBrother
    source: :Wilhelm_Crown_Prince
  AssignClass (78a1e97f-8057-4c8d-90bf-1e88142235ed)
 Call ID: 78a1e97f-8057-4c8d-90bf-1e88142235ed
  Args:
    type: :Man
    source: :August_Wilhelm
  AssignClass (7a1612f5-5d62-49ab-9de6-1581cbd2d579)
 Call ID: 7a1612f5-5d62-49ab-9de6-1581cbd2d579
  Args:
    type: :Person
    source: :August_Wilhelm
  AddTriple (ed36600e-59d2-4d78-a364-5647e82895c8)
 Call ID: ed36600e-59d2-4d78-a364-5647e82895c8
  Args:
    target: :August_Wilhelm
    relation: :hasBrother
    source: :Wilhelm_Crown_Prince
  AssignClass (3f4c4a46-4830-46be-8ebb-033c786a52bd)
 Call ID: 3f4c4a46-4830-46be-8ebb-033c786a52bd
  Args:
    source: :Oskar
    type: :Man
  AssignClass (2c784322-5678-4601-b50e-54c254054d35)
 Call ID: 2c784322-5678-4601-b50e-54c254054d35
  Args:
    type: :Person
    source: :Oskar
  AddTriple (ded5c925-5f91-4a5b-9fad-f9809dd5d46d)
 Call ID: ded5c925-5f91-4a5b-9fad-f9809dd5d46d
  Args:
    source: :Wilhelm_Crown_Prince
    relation: :hasBrother
    target: :Oskar
  AssignClass (a68cad54-ab83-4bfd-b4c6-96842f8677b8)
 Call ID: a68cad54-ab83-4bfd-b4c6-96842f8677b8
  Args:
    source: :Joachim
    type: :Man
  AssignClass (7e528e7e-899e-4c12-97dd-74699e7c9232)
 Call ID: 7e528e7e-899e-4c12-97dd-74699e7c9232
  Args:
    source: :Joachim
    type: :Person
  AddTriple (ab339d56-3f28-418f-9b2c-cb6f20f079b2)
 Call ID: ab339d56-3f28-418f-9b2c-cb6f20f079b2
  Args:
    relation: :hasBrother
    source: :Wilhelm_Crown_Prince
    target: :Joachim
  AssignClass (6cd44ef9-90cb-4c13-b852-06a69d8c4786)
 Call ID: 6cd44ef9-90cb-4c13-b852-06a69d8c4786
  Args:
    source: :Viktoria_Luise
    type: :Woman
  AssignClass (69aee11e-d4fe-49aa-91bb-e3a54e97e551)
 Call ID: 69aee11e-d4fe-49aa-91bb-e3a54e97e551
  Args:
    source: :Viktoria_Luise
    type: :Person
  AddTriple (58cb992d-f96b-4585-bf10-97b2923e9cab)
 Call ID: 58cb992d-f96b-4585-bf10-97b2923e9cab
  Args:
    source: :Wilhelm_Crown_Prince
    relation: :hasSister
    target: :Viktoria_Luise
  AssignClass (fb76c17e-73dd-4511-919d-4fe33702ea68)
 Call ID: fb76c17e-73dd-4511-919d-4fe33702ea68
  Args:
    type: :Woman
    source: :Cecilie_of_Mecklenburg-Schwerin
  AssignClass (8bf9e2c4-bc18-4d21-8289-36e0e8b6c48d)
 Call ID: 8bf9e2c4-bc18-4d21-8289-36e0e8b6c48d
  Args:
    type: :Person
    source: :Cecilie_of_Mecklenburg-Schwerin
  AddLiteral (31013a5f-dbce-40f7-bf09-8efd3408cbf2)
 Call ID: 31013a5f-dbce-40f7-bf09-8efd3408cbf2
  Args:
    source: :Wilhelm_Crown_Prince
    literal_type: xsd:integer
    literal_value: 1905
    relation: :hasMarriageYear
  AddTriple (c7f14535-f991-4e10-b2c3-f88d83f140c5)
 Call ID: c7f14535-f991-4e10-b2c3-f88d83f140c5
  Args:
    source: :Wilhelm_Crown_Prince
    relation: :hasRelation
    target: :Cecilie_of_Mecklenburg-Schwerin
  AssignClass (c2d55e96-b490-4710-a0d5-a6f95f2d5a5a)
 Call ID: c2d55e96-b490-4710-a0d5-a6f95f2d5a5a
  Args:
    type: :Man
    source: :Prince_Wilhelm_of_Prussia
  AssignClass (9e5b4833-2d4d-40c0-885f-f86a879c02b5)
 Call ID: 9e5b4833-2d4d-40c0-885f-f86a879c02b5
  Args:
    source: :Prince_Wilhelm_of_Prussia
    type: :Person
  AddTriple (387d24b6-f09c-4c1f-b6d2-86e194b17855)
 Call ID: 387d24b6-f09c-4c1f-b6d2-86e194b17855
  Args:
    target: :Wilhelm_Crown_Prince
    source: :Prince_Wilhelm_of_Prussia
    relation: :isSonOf
  AddTriple (33633155-00cf-41d9-9228-73487d724c50)
 Call ID: 33633155-00cf-41d9-9228-73487d724c50
  Args:
    relation: :isSonOf
    source: :Prince_Wilhelm_of_Prussia
    target: :Cecilie_of_Mecklenburg-Schwerin
  AssignClass (22cadd7e-5d03-4409-9ee9-0eb393a908cb)
 Call ID: 22cadd7e-5d03-4409-9ee9-0eb393a908cb
  Args:
    source: :Frederick_Francis_III
    type: :Man
  AssignClass (533c0fc6-484d-4eab-86c9-f2b6631891ae)
 Call ID: 533c0fc6-484d-4eab-86c9-f2b6631891ae
  Args:
    source: :Frederick_Francis_III
    type: :Person
  AssignClass (06c68f79-e82a-4c93-8e34-49cf3d920bd5)
 Call ID: 06c68f79-e82a-4c93-8e34-49cf3d920bd5
  Args:
    type: :Woman
    source: :Anastasia_Mikhailovna
  AssignClass (480bd469-6fcc-4c60-83fe-21716468ed5f)
 Call ID: 480bd469-6fcc-4c60-83fe-21716468ed5f
  Args:
    source: :Anastasia_Mikhailovna
    type: :Person
  AddTriple (5789fd46-48a2-44e3-8c75-a98ebb22036e)
 Call ID: 5789fd46-48a2-44e3-8c75-a98ebb22036e
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    source: :Frederick_Francis_III
    relation: :isFatherOf
  AddTriple (92572318-bbd1-41c5-b881-a41d257c03b6)
 Call ID: 92572318-bbd1-41c5-b881-a41d257c03b6
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    source: :Anastasia_Mikhailovna
    relation: :isMotherOf
  Finish (89e541b2-06bd-463f-b3e1-21bda9124ccd)
 Call ID: 89e541b2-06bd-463f-b3e1-21bda9124ccd
  Args: