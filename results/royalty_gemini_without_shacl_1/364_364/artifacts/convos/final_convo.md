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
  AssignClass (843913e5-e085-433b-8a43-73914864b2a0)
 Call ID: 843913e5-e085-433b-8a43-73914864b2a0
  Args:
    type: :Man
    source: Philipp_of_Hesse
  AssignClass (3806ccd3-9c85-4789-a365-f2343451a017)
 Call ID: 3806ccd3-9c85-4789-a365-f2343451a017
  Args:
    type: :Person
    source: Philipp_of_Hesse
  AddLiteral (fa27181f-7581-486e-ae2b-ab2708ec3b20)
 Call ID: fa27181f-7581-486e-ae2b-ab2708ec3b20
  Args:
    source: Philipp_of_Hesse
    literal_type: xsd:integer
    literal_value: 1896
    relation: :hasBirthYear
  AddLiteral (6512f276-dc15-48d3-827e-5e128fce0489)
 Call ID: 6512f276-dc15-48d3-827e-5e128fce0489
  Args:
    source: Philipp_of_Hesse
    relation: :hasDeathYear
    literal_value: 1980
    literal_type: xsd:integer
  AssignClass (d0bf4d78-daca-4bad-a757-04d525fd154a)
 Call ID: d0bf4d78-daca-4bad-a757-04d525fd154a
  Args:
    source: Frederick_III_German_Emperor
    type: :Man
  AssignClass (8d89004b-3204-4344-96e0-f227201c10b0)
 Call ID: 8d89004b-3204-4344-96e0-f227201c10b0
  Args:
    source: Frederick_III_German_Emperor
    type: :Ancestor
  AddTriple (2aeeefb7-25cf-4461-8f48-cecbceefec59)
 Call ID: 2aeeefb7-25cf-4461-8f48-cecbceefec59
  Args:
    source: Philipp_of_Hesse
    target: Frederick_III_German_Emperor
    relation: :hasAncestor
  AssignClass (9cfbe7b1-88e6-4fce-a7cf-0fdf2b144268)
 Call ID: 9cfbe7b1-88e6-4fce-a7cf-0fdf2b144268
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (5476d0de-1669-4862-bb9e-6c8d2a12a090)
 Call ID: 5476d0de-1669-4862-bb9e-6c8d2a12a090
  Args:
    type: :Ancestor
    source: Queen_Victoria
  AddTriple (18ba8a56-d7c0-401c-86d7-cb3132a8b49c)
 Call ID: 18ba8a56-d7c0-401c-86d7-cb3132a8b49c
  Args:
    source: Philipp_of_Hesse
    target: Queen_Victoria
    relation: :hasAncestor
  AssignClass (1f0f4b27-0311-4b48-8af8-78652d3473ce)
 Call ID: 1f0f4b27-0311-4b48-8af8-78652d3473ce
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Man
  AssignClass (c7cd8082-c0ef-438e-8b29-93b112182f8e)
 Call ID: c7cd8082-c0ef-438e-8b29-93b112182f8e
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Ancestor
  AssignClass (f78a74b9-abac-4317-a915-98319d045d87)
 Call ID: f78a74b9-abac-4317-a915-98319d045d87
  Args:
    source: Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (fd3eb2bf-9689-4590-88b8-2fe181954fcc)
 Call ID: fd3eb2bf-9689-4590-88b8-2fe181954fcc
  Args:
    type: :Ancestor
    source: Frederick_Charles_of_Hesse
  AddTriple (71dc217c-733a-4e8c-b8af-065e027226e3)
 Call ID: 71dc217c-733a-4e8c-b8af-065e027226e3
  Args:
    source: Philipp_of_Hesse
    target: Frederick_Charles_of_Hesse
    relation: :hasFather
  AssignClass (9f61d23b-78f1-4db3-8725-e181f498bc12)
 Call ID: 9f61d23b-78f1-4db3-8725-e181f498bc12
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (eeb6278c-5531-4bd6-a387-2c533c6fc5d8)
 Call ID: eeb6278c-5531-4bd6-a387-2c533c6fc5d8
  Args:
    source: Margaret_of_Prussia
    type: :Ancestor
  AddTriple (2c4f3510-7c43-470f-b498-6201c70070df)
 Call ID: 2c4f3510-7c43-470f-b498-6201c70070df
  Args:
    source: Philipp_of_Hesse
    target: Margaret_of_Prussia
    relation: :hasMother
  AssignClass (a02576e0-6c67-4ab5-9081-d5e78bba142e)
 Call ID: a02576e0-6c67-4ab5-9081-d5e78bba142e
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (6dec0c80-7925-4359-8a24-67fd3381a019)
 Call ID: 6dec0c80-7925-4359-8a24-67fd3381a019
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AddTriple (0d2e9837-fe75-4bda-9a6d-284d7fd61248)
 Call ID: 0d2e9837-fe75-4bda-9a6d-284d7fd61248
  Args:
    target: Margaret_of_Prussia
    relation: :hasSister
    source: Wilhelm_II_German_Emperor
  AssignClass (79f7c4ce-d786-4715-91f6-7d4968b4528a)
 Call ID: 79f7c4ce-d786-4715-91f6-7d4968b4528a
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    type: :Man
  AssignClass (f1c45ad3-7af5-4bcc-ae1b-ab3bfa632845)
 Call ID: f1c45ad3-7af5-4bcc-ae1b-ab3bfa632845
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Hesse
  AddTriple (542daf71-86d3-47a1-9c77-ab32a669d0f8)
 Call ID: 542daf71-86d3-47a1-9c77-ab32a669d0f8
  Args:
    source: Philipp_of_Hesse
    target: Friedrich_Wilhelm_of_Hesse
    relation: :hasBrother
  AssignClass (f9899c99-8db4-48c8-87c1-3f64bd11ac42)
 Call ID: f9899c99-8db4-48c8-87c1-3f64bd11ac42
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (3e632e64-c2ed-431e-b38d-ef6686c4c393)
 Call ID: 3e632e64-c2ed-431e-b38d-ef6686c4c393
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AddTriple (ad212930-b466-4067-9cca-84834731667c)
 Call ID: ad212930-b466-4067-9cca-84834731667c
  Args:
    source: Philipp_of_Hesse
    target: Wolfgang_of_Hesse
    relation: :hasBrother
  AssignClass (176f1ced-3d1a-4421-9a9a-7954f86f69ff)
 Call ID: 176f1ced-3d1a-4421-9a9a-7954f86f69ff
  Args:
    source: Sophie_of_Prussia
    type: :Woman
  AssignClass (dfb8b61c-d254-4938-860f-53329dcce329)
 Call ID: dfb8b61c-d254-4938-860f-53329dcce329
  Args:
    type: :Person
    source: Sophie_of_Prussia
  AddTriple (afb1c1c1-42f7-4449-8d5b-5990c8f33b9d)
 Call ID: afb1c1c1-42f7-4449-8d5b-5990c8f33b9d
  Args:
    source: Sophie_of_Prussia
    target: Margaret_of_Prussia
    relation: :hasSister
  AssignClass (169692e8-905d-4cbf-8198-74f1512878e1)
 Call ID: 169692e8-905d-4cbf-8198-74f1512878e1
  Args:
    source: Constantine_I_of_Greece
    type: :Man
  AssignClass (67482218-f7f6-4c86-a703-7a2fb11a629f)
 Call ID: 67482218-f7f6-4c86-a703-7a2fb11a629f
  Args:
    type: :Person
    source: Constantine_I_of_Greece
  AddTriple (e5167530-578e-4992-b31c-b7e55d573275)
 Call ID: e5167530-578e-4992-b31c-b7e55d573275
  Args:
    source: Sophie_of_Prussia
    target: Constantine_I_of_Greece
    relation: :hasRelation
  AssignClass (ec9e97f0-a3ac-4788-8240-8f4ff7065d53)
 Call ID: ec9e97f0-a3ac-4788-8240-8f4ff7065d53
  Args:
    source: Mafalda_of_Savoy
    type: :Woman
  AssignClass (bf5f038a-4a78-4160-91f4-04c8e19f5de1)
 Call ID: bf5f038a-4a78-4160-91f4-04c8e19f5de1
  Args:
    type: :Person
    source: Mafalda_of_Savoy
  AddTriple (9e19cf34-fd19-4aa5-b654-e99b306d266a)
 Call ID: 9e19cf34-fd19-4aa5-b654-e99b306d266a
  Args:
    target: Victor_Emmanuel_III_of_Italy
    relation: :hasMother
    source: Mafalda_of_Savoy
  AddLiteral (5712b11d-d540-489b-9014-d2147c26ea3b)
 Call ID: 5712b11d-d540-489b-9014-d2147c26ea3b
  Args:
    source: Philipp_of_Hesse
    literal_value: 1925
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (37ae3dbc-d415-4df1-9b87-b08be05d8dd5)
 Call ID: 37ae3dbc-d415-4df1-9b87-b08be05d8dd5
  Args:
    relation: :hasRelation
    target: Mafalda_of_Savoy
    source: Philipp_of_Hesse
  AssignClass (595755d6-958c-42ff-a635-7d2e1572ca3b)
 Call ID: 595755d6-958c-42ff-a635-7d2e1572ca3b
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AssignClass (944b91b3-e750-46d2-9d98-8bf95cb37bcf)
 Call ID: 944b91b3-e750-46d2-9d98-8bf95cb37bcf
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AddTriple (3fbb4347-151c-4254-a5d3-1bec79fcaa66)
 Call ID: 3fbb4347-151c-4254-a5d3-1bec79fcaa66
  Args:
    relation: :hasSon
    target: Moritz_of_Hesse
    source: Philipp_of_Hesse
  AssignClass (a15e57b4-6a87-484b-a288-7f321adf34b2)
 Call ID: a15e57b4-6a87-484b-a288-7f321adf34b2
  Args:
    type: :Man
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (3d6b7e87-c429-468b-89d9-673d183a59b7)
 Call ID: 3d6b7e87-c429-468b-89d9-673d183a59b7
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Person
  Finish (de425c92-7057-4e78-9065-55fe7ce75086)
 Call ID: de425c92-7057-4e78-9065-55fe7ce75086
  Args: