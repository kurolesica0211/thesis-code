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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (759d85da-7b82-42d1-8f1e-d4a92b68290a)
 Call ID: 759d85da-7b82-42d1-8f1e-d4a92b68290a
  Args:
    type: :Man
    source: Wilhelm_Crown_Prince
  AssignClass (54605156-d501-4f9c-b7de-50bb74359ff7)
 Call ID: 54605156-d501-4f9c-b7de-50bb74359ff7
  Args:
    source: Wilhelm_Crown_Prince
    type: :Person
  AddLiteral (05394e6c-d60d-4644-b22c-9e49730ad52e)
 Call ID: 05394e6c-d60d-4644-b22c-9e49730ad52e
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1882
    source: Wilhelm_Crown_Prince
  AddLiteral (156da156-7c2f-4919-a575-285481653446)
 Call ID: 156da156-7c2f-4919-a575-285481653446
  Args:
    relation: :hasDeathYear
    source: Wilhelm_Crown_Prince
    literal_value: 1951
    literal_type: xsd:integer
  AssignClass (f097b21f-7eea-4522-92a9-0896d3a1d8e2)
 Call ID: f097b21f-7eea-4522-92a9-0896d3a1d8e2
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (7587269d-6b31-461e-8d0b-2332e761baee)
 Call ID: 7587269d-6b31-461e-8d0b-2332e761baee
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (88e9614e-4ed3-4ea7-ae79-9f34844032c0)
 Call ID: 88e9614e-4ed3-4ea7-ae79-9f34844032c0
  Args:
    source: Augusta_Victoria
    type: :Woman
  AssignClass (759c9979-592b-4112-86c5-0782d645cea1)
 Call ID: 759c9979-592b-4112-86c5-0782d645cea1
  Args:
    type: :Person
    source: Augusta_Victoria
  AddTriple (2f1a57e5-1476-4546-abed-58f4b3cb4f46)
 Call ID: 2f1a57e5-1476-4546-abed-58f4b3cb4f46
  Args:
    relation: :isFatherOf
    source: Wilhelm_II
    target: Wilhelm_Crown_Prince
  AddTriple (7eb8b7f2-762a-445c-965a-d1c1c12223ba)
 Call ID: 7eb8b7f2-762a-445c-965a-d1c1c12223ba
  Args:
    target: Wilhelm_Crown_Prince
    source: Augusta_Victoria
    relation: :isMotherOf
  AddTriple (3e754569-920f-422c-a4bb-88e6e2ace451)
 Call ID: 3e754569-920f-422c-a4bb-88e6e2ace451
  Args:
    target: Wilhelm_II
    source: Wilhelm_Crown_Prince
    relation: :hasFather
  AddTriple (ef5e3333-8da8-4b7d-af53-96bdef930599)
 Call ID: ef5e3333-8da8-4b7d-af53-96bdef930599
  Args:
    target: Augusta_Victoria
    source: Wilhelm_Crown_Prince
    relation: :hasMother
  AssignClass (0b88d2f6-0ba7-465a-8c7e-06a63ed3aff1)
 Call ID: 0b88d2f6-0ba7-465a-8c7e-06a63ed3aff1
  Args:
    source: Eitel_Friedrich
    type: :Man
  AssignClass (40a6ada4-9326-4bb7-87f8-29e75caeaf7f)
 Call ID: 40a6ada4-9326-4bb7-87f8-29e75caeaf7f
  Args:
    source: Eitel_Friedrich
    type: :Person
  AssignClass (00f434b7-c0fe-479b-b3c2-078fc08ec3ec)
 Call ID: 00f434b7-c0fe-479b-b3c2-078fc08ec3ec
  Args:
    source: Adalbert
    type: :Man
  AssignClass (bfdd38fa-1d61-4a76-b3ac-70fa0c9327a5)
 Call ID: bfdd38fa-1d61-4a76-b3ac-70fa0c9327a5
  Args:
    type: :Person
    source: Adalbert
  AssignClass (91af8403-ddcf-4d99-991f-0ed36844664b)
 Call ID: 91af8403-ddcf-4d99-991f-0ed36844664b
  Args:
    type: :Man
    source: August_Wilhelm
  AssignClass (df02c272-238e-444e-9255-2482532864a4)
 Call ID: df02c272-238e-444e-9255-2482532864a4
  Args:
    type: :Person
    source: August_Wilhelm
  AssignClass (576db28d-7b6e-4954-84c7-36328b0e8659)
 Call ID: 576db28d-7b6e-4954-84c7-36328b0e8659
  Args:
    type: :Man
    source: Oskar
  AssignClass (7e01a8ed-2ac3-4d1e-89c7-1c03cc314178)
 Call ID: 7e01a8ed-2ac3-4d1e-89c7-1c03cc314178
  Args:
    type: :Person
    source: Oskar
  AssignClass (9ae9262e-0ece-4029-8f35-50ec2dc1c8f3)
 Call ID: 9ae9262e-0ece-4029-8f35-50ec2dc1c8f3
  Args:
    source: Joachim
    type: :Man
  AssignClass (096b8ba1-8c01-4da6-ad1b-3d000492cc88)
 Call ID: 096b8ba1-8c01-4da6-ad1b-3d000492cc88
  Args:
    source: Joachim
    type: :Person
  AssignClass (34a12e16-8b67-47b9-a11d-6ea9f456ca6c)
 Call ID: 34a12e16-8b67-47b9-a11d-6ea9f456ca6c
  Args:
    source: Viktoria_Luise
    type: :Woman
  AssignClass (44dc04d4-0056-43e8-b2f5-983af0e6fb61)
 Call ID: 44dc04d4-0056-43e8-b2f5-983af0e6fb61
  Args:
    source: Viktoria_Luise
    type: :Person
  AddTriple (b47f3bc3-e4fc-4d3c-95f0-e336a7d77552)
 Call ID: b47f3bc3-e4fc-4d3c-95f0-e336a7d77552
  Args:
    relation: :isSiblingOf
    target: Eitel_Friedrich
    source: Wilhelm_Crown_Prince
  AddTriple (3bfe4e01-e021-403e-aa2b-5e3bff14197d)
 Call ID: 3bfe4e01-e021-403e-aa2b-5e3bff14197d
  Args:
    source: Wilhelm_Crown_Prince
    target: Adalbert
    relation: :isSiblingOf
  AddTriple (7c0b0597-214b-4e6b-8aab-05bf1ac8e526)
 Call ID: 7c0b0597-214b-4e6b-8aab-05bf1ac8e526
  Args:
    relation: :isSiblingOf
    source: Wilhelm_Crown_Prince
    target: August_Wilhelm
  AddTriple (4058e790-742d-45ac-b52b-f9d9cb41ec71)
 Call ID: 4058e790-742d-45ac-b52b-f9d9cb41ec71
  Args:
    source: Wilhelm_Crown_Prince
    target: Oskar
    relation: :isSiblingOf
  AddTriple (4fb276bd-7f52-431d-b9b5-23bb1a03fbdc)
 Call ID: 4fb276bd-7f52-431d-b9b5-23bb1a03fbdc
  Args:
    target: Joachim
    source: Wilhelm_Crown_Prince
    relation: :isSiblingOf
  AddTriple (1fa60009-d043-4f66-9da0-2d9d2fa4d119)
 Call ID: 1fa60009-d043-4f66-9da0-2d9d2fa4d119
  Args:
    relation: :isSiblingOf
    source: Wilhelm_Crown_Prince
    target: Viktoria_Luise
  AssignClass (c5048096-7e6b-48ef-9ec8-9b3a4d402a70)
 Call ID: c5048096-7e6b-48ef-9ec8-9b3a4d402a70
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (5385e25a-f147-4f77-97e2-e9e7e0c0d40b)
 Call ID: 5385e25a-f147-4f77-97e2-e9e7e0c0d40b
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (270f1358-eab4-4872-b590-29270dd20aab)
 Call ID: 270f1358-eab4-4872-b590-29270dd20aab
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Wilhelm_Crown_Prince
    literal_value: 1905
  AddTriple (7a87d2b1-e3bc-4780-9ed6-748b52b754c0)
 Call ID: 7a87d2b1-e3bc-4780-9ed6-748b52b754c0
  Args:
    relation: :hasRelation
    target: Cecilie_of_Mecklenburg-Schwerin
    source: Wilhelm_Crown_Prince
  AssignClass (d1d6bd15-9969-4e19-9990-c55fad56e9a7)
 Call ID: d1d6bd15-9969-4e19-9990-c55fad56e9a7
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (9342c398-a20c-468c-9625-962e3ab17471)
 Call ID: 9342c398-a20c-468c-9625-962e3ab17471
  Args:
    type: :Person
    source: Frederick_Francis_III
  AssignClass (7fc54326-75f4-4366-b4bd-da1ed0e074c6)
 Call ID: 7fc54326-75f4-4366-b4bd-da1ed0e074c6
  Args:
    source: Anastasia_Mikhailovna
    type: :Woman
  AssignClass (47b3674c-f3ee-42ab-9345-ba92f0c6a540)
 Call ID: 47b3674c-f3ee-42ab-9345-ba92f0c6a540
  Args:
    source: Anastasia_Mikhailovna
    type: :Person
  AddTriple (1a39bae8-117e-4999-af27-e4fa4cb1c50b)
 Call ID: 1a39bae8-117e-4999-af27-e4fa4cb1c50b
  Args:
    source: Frederick_Francis_III
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :isFatherOf
  AddTriple (555f27d7-a3b5-4b94-86f2-2479da8a2d26)
 Call ID: 555f27d7-a3b5-4b94-86f2-2479da8a2d26
  Args:
    relation: :isMotherOf
    target: Cecilie_of_Mecklenburg-Schwerin
    source: Anastasia_Mikhailovna
  AssignClass (8a64289d-d3d9-464d-aed7-343e47e0e641)
 Call ID: 8a64289d-d3d9-464d-aed7-343e47e0e641
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Prussia_Jr
  AssignClass (395e23e1-e5b2-4570-87e5-2ac92cb0296b)
 Call ID: 395e23e1-e5b2-4570-87e5-2ac92cb0296b
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Prussia_Jr
  AddTriple (4b3a3634-5aab-491f-a9b2-c95b199c7aa7)
 Call ID: 4b3a3634-5aab-491f-a9b2-c95b199c7aa7
  Args:
    target: Wilhelm_Crown_Prince
    source: Prince_Wilhelm_of_Prussia_Jr
    relation: :hasFather
  AddTriple (e1e90bd2-13b5-45d6-a562-ad193016d98f)
 Call ID: e1e90bd2-13b5-45d6-a562-ad193016d98f
  Args:
    relation: :hasMother
    target: Cecilie_of_Mecklenburg-Schwerin
    source: Prince_Wilhelm_of_Prussia_Jr
  Finish (6fb2aeac-d7a7-47a0-b395-2d9274796cd3)
 Call ID: 6fb2aeac-d7a7-47a0-b395-2d9274796cd3
  Args: