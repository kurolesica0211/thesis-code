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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (98a3d0ff-28d3-401e-b63d-8188ced4ce02)
 Call ID: 98a3d0ff-28d3-401e-b63d-8188ced4ce02
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (fa85f9df-dc4f-489a-96a5-889276f9f28d)
 Call ID: fa85f9df-dc4f-489a-96a5-889276f9f28d
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (d8c18dbb-e895-479a-9204-24e9e3999379)
 Call ID: d8c18dbb-e895-479a-9204-24e9e3999379
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (a6bf3c61-d02a-4ea9-a244-60ae186dc92d)
 Call ID: a6bf3c61-d02a-4ea9-a244-60ae186dc92d
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (ee290ac2-7046-41ce-9869-942003ed9ffd)
 Call ID: ee290ac2-7046-41ce-9869-942003ed9ffd
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasMother
    target: Augusta_Victoria_of_Schleswig-Holstein
  AddLiteral (b9fb776e-2134-4cf5-be3c-465b54feef48)
 Call ID: b9fb776e-2134-4cf5-be3c-465b54feef48
  Args:
    source: Wilhelm_German_Crown_Prince
    literal_value: 1882
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (a2d59bea-4e45-450f-ba24-f712257a7e45)
 Call ID: a2d59bea-4e45-450f-ba24-f712257a7e45
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Wilhelm_German_Crown_Prince
    literal_value: 1951
  AssignClass (2753a5d7-54d7-4db8-b775-186f22a50aa9)
 Call ID: 2753a5d7-54d7-4db8-b775-186f22a50aa9
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (350148a2-c24e-4a53-b0ed-82e82297b5b6)
 Call ID: 350148a2-c24e-4a53-b0ed-82e82297b5b6
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasRelation
    target: Cecilie_of_Mecklenburg-Schwerin
  AddLiteral (3167d819-b251-49d7-a8f6-c9230b05926c)
 Call ID: 3167d819-b251-49d7-a8f6-c9230b05926c
  Args:
    source: Wilhelm_German_Crown_Prince
    literal_value: 1905
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (4bf746c9-7b69-4943-b308-f1c48b51f333)
 Call ID: 4bf746c9-7b69-4943-b308-f1c48b51f333
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich
  AssignClass (db1cf503-2976-426b-8207-053dbfc2b60b)
 Call ID: db1cf503-2976-426b-8207-053dbfc2b60b
  Args:
    type: :Man
    source: Prince_Adalbert
  AssignClass (a416bdcd-7e6a-466c-adae-fe00d19d45d1)
 Call ID: a416bdcd-7e6a-466c-adae-fe00d19d45d1
  Args:
    type: :Man
    source: Prince_August_Wilhelm
  AssignClass (16ae4673-de55-4b1e-95de-03b634a34138)
 Call ID: 16ae4673-de55-4b1e-95de-03b634a34138
  Args:
    type: :Man
    source: Prince_Oskar
  AssignClass (5562630f-d233-44f7-b8f5-6526c87d7cd1)
 Call ID: 5562630f-d233-44f7-b8f5-6526c87d7cd1
  Args:
    type: :Man
    source: Prince_Joachim
  AssignClass (1759d59c-d7f9-4e6b-a50a-bc7eebc3672f)
 Call ID: 1759d59c-d7f9-4e6b-a50a-bc7eebc3672f
  Args:
    type: :Woman
    source: Princess_Viktoria_Luise
  AddTriple (4ce78e55-3fcc-4d00-90df-9b1899516388)
 Call ID: 4ce78e55-3fcc-4d00-90df-9b1899516388
  Args:
    target: Prince_Eitel_Friedrich
    relation: :hasBrother
    source: Wilhelm_German_Crown_Prince
  AddTriple (49d95f7d-a483-407b-be76-793beb81b4de)
 Call ID: 49d95f7d-a483-407b-be76-793beb81b4de
  Args:
    relation: :hasBrother
    source: Wilhelm_German_Crown_Prince
    target: Prince_Adalbert
  AddTriple (63a29dec-fbfa-4f77-974d-cda38a586733)
 Call ID: 63a29dec-fbfa-4f77-974d-cda38a586733
  Args:
    target: Prince_August_Wilhelm
    relation: :hasBrother
    source: Wilhelm_German_Crown_Prince
  AddTriple (6caaf36e-830d-40a1-b0f5-43780d739914)
 Call ID: 6caaf36e-830d-40a1-b0f5-43780d739914
  Args:
    source: Wilhelm_German_Crown_Prince
    relation: :hasBrother
    target: Prince_Oskar
  AddTriple (8f6681fb-a932-4c22-bf2d-27c13498843e)
 Call ID: 8f6681fb-a932-4c22-bf2d-27c13498843e
  Args:
    target: Prince_Joachim
    relation: :hasBrother
    source: Wilhelm_German_Crown_Prince
  AddTriple (d9b7e09a-fe1d-435d-8019-98548c56df6f)
 Call ID: d9b7e09a-fe1d-435d-8019-98548c56df6f
  Args:
    relation: :hasSister
    source: Wilhelm_German_Crown_Prince
    target: Princess_Viktoria_Luise
  AssignClass (4e929d59-1fc3-4c60-983e-614fba4fe2f5)
 Call ID: 4e929d59-1fc3-4c60-983e-614fba4fe2f5
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Prussia
  AddTriple (92b2aa11-f21f-4cf4-8e98-49f6cf2c7fc0)
 Call ID: 92b2aa11-f21f-4cf4-8e98-49f6cf2c7fc0
  Args:
    target: Prince_Wilhelm_of_Prussia
    source: Wilhelm_German_Crown_Prince
    relation: :hasSon
  AssignClass (c8c6369c-13d1-4359-bea0-49505d4e9f34)
 Call ID: c8c6369c-13d1-4359-bea0-49505d4e9f34
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (3507c6e5-c848-4ea4-984d-e99d8636edf1)
 Call ID: 3507c6e5-c848-4ea4-984d-e99d8636edf1
  Args:
    type: :Woman
    source: Anastasia_Mikhailovna
  AddTriple (7e1cec06-49d0-45c3-b11e-0c4ce8c284b6)
 Call ID: 7e1cec06-49d0-45c3-b11e-0c4ce8c284b6
  Args:
    target: Frederick_Francis_III
    source: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (d77bfce9-68af-46c0-9fd2-de0b461143e1)
 Call ID: d77bfce9-68af-46c0-9fd2-de0b461143e1
  Args:
    relation: :hasMother
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Anastasia_Mikhailovna
  Finish (1b8ca0e9-d021-4747-8194-7a641c6de25b)
 Call ID: 1b8ca0e9-d021-4747-8194-7a641c6de25b
  Args: