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
Philipp, Prince and Landgrave of Hesse (6 November 1896 – 25 October 1980) was head of the Electoral House of Hesse from 1940 to 1980.
Philipp was a grandson of Frederick III, German Emperor, and a great-grandson of Queen Victoria, as well as the son-in-law of Victor Emmanuel III of Italy.
Early life

Philipp was born at Schloss Rumpenheim in Offenbach, the third son of Prince Frederick Charles of Hesse and of his wife Princess Margaret of Prussia (sister of the German Emperor Wilhelm II).
He held the rank of lieutenant (Leutnant, an extremely low rank considering his aristocratic background) and was mostly responsible for the procurement of munitions.
In 1916, Philipp's oldest brother Friedrich Wilhelm died (in World War I) and Philipp became second in line to succeed his uncle as Head of the Electoral House of Hesse.
It was intended that Philipp would eventually succeed his father as Head of the House of Hesse, while his (younger) twin brother Wolfgang would be heir to the Finnish throne.
He made several visits to Greece where his aunt, Princess Sophie of Prussia was the wife of King Constantine I. In 1922, he left university without completing a degree and took a job at the Kaiser-Friedrich-Museum in Berlin.
Marriage and children

He married Princess Mafalda of Savoy, daughter of King Victor Emmanuel III of Italy, on 23 September 1925 at the Castello di Racconigi near Turin.
The couple had four children:


The family lived mostly at Villa Polissena (named after Queen Polyxena), part of Villa Savoia, the King of Italy's estate on the outskirts of Rome.
On his return to Germany in October 1930, he joined the National Socialist German Workers' Party.
Through his party membership, Philipp became a particularly close friend of Hermann Göring, the future head of the German Air Force (Luftwaffe).
Following the appointment of Adolf Hitler as the German Chancellor on 30 January 1933, Philipp was appointed Oberpräsident (Governor) of Hesse-Nassau on 7 June 1933 by Prussian Minister-President Göring, who also named him to the Prussian State Council in July.
For this purpose, the Reich Chancellery established a special account for him at the German Embassy in Rome, over which Prince Philipp could freely dispose.
In 1940/41, German art purchases in Italy increased to such an extent that the Fascist government prohibited the sale of art treasures to foreigners in September 1941.
As governor of Hesse-Nassau, Philipp was associated with the Aktion T4 euthanasia programme.
As the war progressed, the attitude of the National Socialist authorities towards members of the German princely houses changed.
In late April 1943, Philipp was ordered to report to Hitler's headquarters, where he stayed for most of the next four months.
On 25 January 1944, his political disgrace became public when he was dismissed from his office as Oberpräsident of Hesse-Nassau.
Philipp's wife Mafalda was arrested and placed under military custody in Rome.
Mafalda was seriously injured and died several days later following a belated operation by camp medical staff.
After only ten days, he was transferred to Tyrol to Hotel "Bachmann" along with about 140 other prominent prisoners (for example Kurt Schuschnigg, Bogislaw von Bonin, Hjalmar Schacht, Martin Niemöller, Georg Thomas, and Alexander von Falkenhausen), freed by the Wehrmacht on 30 April 1945 (SS-Obergruppenführer Karl Wolff received a telephone call from the SS guards and ordered them to hand over the prisoners to the German army officers Hauptmann Wichard von Alvensleben and Hauptmann Gebhard von Alvensleben), and was then arrested by U.S. troops on 4 May 1945 in Niederdorf in the Italian Dolomites due to his role in the Nazi Party.
On 28 May 1940, Philipp succeeded his father as Head of the Electoral House of Hesse.
In 1968, upon the death of his distant agnatic relative, Louis, Prince of Hesse and by Rhine (who was also his second cousin as Philipp's mother and Louis' father were grandchildren of Queen Victoria), Philipp succeeded as head of the entire House of Hesse, including grand ducal Hesse (Hesse and by Rhine/Hesse-Darmstadt).
Louis had nominally adopted Philipp's son Moritz, who at that time inherited the Hessian and by-Rhine properties, including remarkable cultural collections: for the first time since the division of Hesse into branches after the death of Philip the Magnanimous in 1567, all sovereign branches of the house of Hesse were reunited again.



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
  AssignClass (c613a31c-13c5-41f5-aff3-449f06170a32)
 Call ID: c613a31c-13c5-41f5-aff3-449f06170a32
  Args:
    type: :Man
    source: Philipp_Prince_and_Landgrave_of_Hesse
  AssignClass (48ce6db4-aed8-48de-a1c4-cde02e8793dc)
 Call ID: 48ce6db4-aed8-48de-a1c4-cde02e8793dc
  Args:
    source: Philipp_Prince_and_Landgrave_of_Hesse
    type: :Person
  AddLiteral (f1f8fa9e-7e41-4fe0-80fe-d7183eee3d89)
 Call ID: f1f8fa9e-7e41-4fe0-80fe-d7183eee3d89
  Args:
    literal_type: xsd:integer
    source: Philipp_Prince_and_Landgrave_of_Hesse
    literal_value: 1896
    relation: :hasBirthYear
  AddLiteral (dc4f61cf-eb4b-412e-bd48-3af86cde706f)
 Call ID: dc4f61cf-eb4b-412e-bd48-3af86cde706f
  Args:
    literal_type: xsd:integer
    source: Philipp_Prince_and_Landgrave_of_Hesse
    literal_value: 1980
    relation: :hasDeathYear
  AssignClass (84652ec4-5877-4d31-90f4-57f392e308a8)
 Call ID: 84652ec4-5877-4d31-90f4-57f392e308a8
  Args:
    source: Frederick_III_German_Emperor
    type: :Man
  AssignClass (05bc787f-3379-4477-a34d-f06794cc29a4)
 Call ID: 05bc787f-3379-4477-a34d-f06794cc29a4
  Args:
    source: Frederick_III_German_Emperor
    type: :Person
  AssignClass (4aa04d84-9c1c-42f2-9b50-628263279606)
 Call ID: 4aa04d84-9c1c-42f2-9b50-628263279606
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (5c627d4f-b483-41d7-84c1-91e62d320c45)
 Call ID: 5c627d4f-b483-41d7-84c1-91e62d320c45
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (0e5ed598-8331-406d-b487-b5d3b03091d6)
 Call ID: 0e5ed598-8331-406d-b487-b5d3b03091d6
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Man
  AssignClass (f367917d-86ff-403b-b341-9f75f184cd1e)
 Call ID: f367917d-86ff-403b-b341-9f75f184cd1e
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Person
  AssignClass (5f1c94db-83e6-4aa9-8e28-9eb61d26f53f)
 Call ID: 5f1c94db-83e6-4aa9-8e28-9eb61d26f53f
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (6bb7b0f5-8c39-406b-8c50-f1eee97c7744)
 Call ID: 6bb7b0f5-8c39-406b-8c50-f1eee97c7744
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Person
  AssignClass (03c25ef1-2f9a-4b2a-9eaf-efc469db859f)
 Call ID: 03c25ef1-2f9a-4b2a-9eaf-efc469db859f
  Args:
    type: :Woman
    source: Princess_Margaret_of_Prussia
  AssignClass (9d86a67d-b898-49c4-80f5-00120512c245)
 Call ID: 9d86a67d-b898-49c4-80f5-00120512c245
  Args:
    type: :Person
    source: Princess_Margaret_of_Prussia
  AssignClass (707deab5-1273-45d4-9eda-5f1759a0471f)
 Call ID: 707deab5-1273-45d4-9eda-5f1759a0471f
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (9d9ce393-f59d-44f4-b3da-82aabcd67602)
 Call ID: 9d9ce393-f59d-44f4-b3da-82aabcd67602
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (b9d95351-5b97-4d17-ab02-49e7326bcdb2)
 Call ID: b9d95351-5b97-4d17-ab02-49e7326bcdb2
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (786a483a-7bac-422d-b7ce-4339107cb62d)
 Call ID: 786a483a-7bac-422d-b7ce-4339107cb62d
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (052ae1b6-ffe8-4d6c-8c43-3217f1d610b8)
 Call ID: 052ae1b6-ffe8-4d6c-8c43-3217f1d610b8
  Args:
    source: Wolfgang_of_Hesse
    type: :Man
  AssignClass (119e0a10-4bce-4f20-9af4-b2be69155f7e)
 Call ID: 119e0a10-4bce-4f20-9af4-b2be69155f7e
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AssignClass (d698ddbb-3b44-4ded-8aae-fc8c44dab4dc)
 Call ID: d698ddbb-3b44-4ded-8aae-fc8c44dab4dc
  Args:
    type: :Woman
    source: Princess_Sophie_of_Prussia
  AssignClass (4f241fa1-7e65-43bf-ace6-4d8bc73139cb)
 Call ID: 4f241fa1-7e65-43bf-ace6-4d8bc73139cb
  Args:
    type: :Person
    source: Princess_Sophie_of_Prussia
  AssignClass (a5f21de9-ba3a-4506-aaf4-3c77f8f437d2)
 Call ID: a5f21de9-ba3a-4506-aaf4-3c77f8f437d2
  Args:
    type: :Man
    source: King_Constantine_I_of_Greece
  AssignClass (997c0865-02d7-4b46-b185-f016873a34cd)
 Call ID: 997c0865-02d7-4b46-b185-f016873a34cd
  Args:
    type: :Person
    source: King_Constantine_I_of_Greece
  AssignClass (83a1f9d3-29b2-48a6-88be-e5e3c8547430)
 Call ID: 83a1f9d3-29b2-48a6-88be-e5e3c8547430
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Woman
  AssignClass (4fd69a26-af86-4931-bf82-3bdded791f21)
 Call ID: 4fd69a26-af86-4931-bf82-3bdded791f21
  Args:
    source: Princess_Mafalda_of_Savoy
    type: :Person
  AssignClass (66d15624-5974-4dc0-8225-cab3165761ac)
 Call ID: 66d15624-5974-4dc0-8225-cab3165761ac
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AssignClass (a686a7f8-780f-4cd1-80e9-6dc5e35c88c8)
 Call ID: a686a7f8-780f-4cd1-80e9-6dc5e35c88c8
  Args:
    source: Moritz_of_Hesse
    type: :Person
  AssignClass (c14ca882-8fec-40ad-9617-f414500328ca)
 Call ID: c14ca882-8fec-40ad-9617-f414500328ca
  Args:
    type: :Man
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (e4a22707-762b-434e-ac6f-faff1876e8bf)
 Call ID: e4a22707-762b-434e-ac6f-faff1876e8bf
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (a00890b9-a77f-4a23-8dcf-07a0bc246619)
 Call ID: a00890b9-a77f-4a23-8dcf-07a0bc246619
  Args:
    source: Philipp_Prince_and_Landgrave_of_Hesse
    relation: :hasFather
    target: Prince_Frederick_Charles_of_Hesse
  AddTriple (559d3ed3-1fb9-4e85-8b77-48032d940b23)
 Call ID: 559d3ed3-1fb9-4e85-8b77-48032d940b23
  Args:
    relation: :hasMother
    target: Princess_Margaret_of_Prussia
    source: Philipp_Prince_and_Landgrave_of_Hesse
  AddTriple (4e57c404-73cd-48be-bc94-adde5079d943)
 Call ID: 4e57c404-73cd-48be-bc94-adde5079d943
  Args:
    target: Friedrich_Wilhelm_of_Hesse
    relation: :hasBrother
    source: Philipp_Prince_and_Landgrave_of_Hesse
  AddTriple (da845028-13b7-40d8-8e86-dac32ca2f756)
 Call ID: da845028-13b7-40d8-8e86-dac32ca2f756
  Args:
    source: Philipp_Prince_and_Landgrave_of_Hesse
    target: Wolfgang_of_Hesse
    relation: :hasBrother
  AddTriple (ca6b7a04-8cbd-4e00-8fb1-c5f860aca42d)
 Call ID: ca6b7a04-8cbd-4e00-8fb1-c5f860aca42d
  Args:
    relation: :hasSister
    target: Wilhelm_II_German_Emperor
    source: Princess_Margaret_of_Prussia
  AddTriple (bd2d5210-0c5d-444f-a979-efe53651849b)
 Call ID: bd2d5210-0c5d-444f-a979-efe53651849b
  Args:
    relation: :hasSister
    target: Wilhelm_II_German_Emperor
    source: Princess_Sophie_of_Prussia
  AddTriple (d54fd953-59aa-4ec3-86b5-a702237c1aee)
 Call ID: d54fd953-59aa-4ec3-86b5-a702237c1aee
  Args:
    source: Princess_Mafalda_of_Savoy
    target: Victor_Emmanuel_III_of_Italy
    relation: :hasFather
  AddTriple (7df2263c-68b0-4723-8bfe-a5b485fd02c4)
 Call ID: 7df2263c-68b0-4723-8bfe-a5b485fd02c4
  Args:
    target: Philipp_Prince_and_Landgrave_of_Hesse
    relation: :hasFather
    source: Moritz_of_Hesse
  AddTriple (31f97bff-4d4d-4bed-8e46-3848503e08b4)
 Call ID: 31f97bff-4d4d-4bed-8e46-3848503e08b4
  Args:
    relation: :hasMother
    target: Princess_Mafalda_of_Savoy
    source: Moritz_of_Hesse
  AddLiteral (0f28e8a2-b6cf-4376-a72c-e84df23d3d27)
 Call ID: 0f28e8a2-b6cf-4376-a72c-e84df23d3d27
  Args:
    source: Philipp_Prince_and_Landgrave_of_Hesse
    literal_value: 1925
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (5f2044db-87d5-48fb-bff3-d1f63c61c542)
 Call ID: 5f2044db-87d5-48fb-bff3-d1f63c61c542
  Args: