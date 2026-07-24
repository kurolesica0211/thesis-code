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
  AssignClass (5bb1ddd1-7aec-4010-b990-79b20d12a3d4)
 Call ID: 5bb1ddd1-7aec-4010-b990-79b20d12a3d4
  Args:
    type: :Man
    source: Philipp
  AssignClass (7f1c3f40-4373-4500-8464-283f4debfe5a)
 Call ID: 7f1c3f40-4373-4500-8464-283f4debfe5a
  Args:
    type: :Person
    source: Philipp
  AddLiteral (bca2c9ed-4a5a-4bde-9f97-8a2f2d556a0b)
 Call ID: bca2c9ed-4a5a-4bde-9f97-8a2f2d556a0b
  Args:
    literal_type: xsd:integer
    source: Philipp
    literal_value: 1896
    relation: :hasBirthYear
  AddLiteral (58fc1ca8-b32b-4b0e-a72f-6ddde08a83b8)
 Call ID: 58fc1ca8-b32b-4b0e-a72f-6ddde08a83b8
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Philipp
    relation: :hasDeathYear
  AssignClass (ddb06e5e-a9ef-41b9-b660-2e4e1a152b0c)
 Call ID: ddb06e5e-a9ef-41b9-b660-2e4e1a152b0c
  Args:
    source: Frederick_III
    type: :Man
  AssignClass (e4bb4b81-a33d-4304-9807-a648447847f6)
 Call ID: e4bb4b81-a33d-4304-9807-a648447847f6
  Args:
    type: :Person
    source: Frederick_III
  AssignClass (4222c6ac-249c-4202-bfd1-d12b021eb338)
 Call ID: 4222c6ac-249c-4202-bfd1-d12b021eb338
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (591b0d5b-ac4d-4607-8d69-7b12721a7482)
 Call ID: 591b0d5b-ac4d-4607-8d69-7b12721a7482
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (d679f5dc-10bd-435a-874a-3fa2c4bde62b)
 Call ID: d679f5dc-10bd-435a-874a-3fa2c4bde62b
  Args:
    type: :Man
    source: Victor_Emmanuel_III
  AssignClass (f0e385a8-7587-4c45-897b-bfdc602e82a2)
 Call ID: f0e385a8-7587-4c45-897b-bfdc602e82a2
  Args:
    source: Victor_Emmanuel_III
    type: :Person
  AssignClass (9c484709-7b8f-441d-8340-63bc0839bbdc)
 Call ID: 9c484709-7b8f-441d-8340-63bc0839bbdc
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AssignClass (a1b8e0c6-b061-4b34-9ae1-5c53fcc9b27c)
 Call ID: a1b8e0c6-b061-4b34-9ae1-5c53fcc9b27c
  Args:
    type: :Person
    source: Frederick_Charles_of_Hesse
  AssignClass (0f6aeb74-6ebc-4909-a97f-74c59eec2453)
 Call ID: 0f6aeb74-6ebc-4909-a97f-74c59eec2453
  Args:
    source: Margaret_of_Prussia
    type: :Woman
  AssignClass (37b20dd8-1aed-4506-9f51-3f9a45059ab8)
 Call ID: 37b20dd8-1aed-4506-9f51-3f9a45059ab8
  Args:
    type: :Person
    source: Margaret_of_Prussia
  AssignClass (7eab431a-ac5b-485d-a24c-9c48875eaed2)
 Call ID: 7eab431a-ac5b-485d-a24c-9c48875eaed2
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (4320eaa7-7009-4666-9661-e8b301438d67)
 Call ID: 4320eaa7-7009-4666-9661-e8b301438d67
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (c3b62290-52ef-4a4f-a4af-d550d3ec3b90)
 Call ID: c3b62290-52ef-4a4f-a4af-d550d3ec3b90
  Args:
    type: :Man
    source: Friedrich_Wilhelm
  AssignClass (339b03bd-1eb8-470d-9c69-d3d7b866a9bf)
 Call ID: 339b03bd-1eb8-470d-9c69-d3d7b866a9bf
  Args:
    source: Friedrich_Wilhelm
    type: :Person
  AssignClass (d8c24d23-48db-406c-84ee-c6c3481a08cf)
 Call ID: d8c24d23-48db-406c-84ee-c6c3481a08cf
  Args:
    source: Wolfgang
    type: :Man
  AssignClass (50e96a86-f8ab-45ce-8667-328128d9413e)
 Call ID: 50e96a86-f8ab-45ce-8667-328128d9413e
  Args:
    type: :Person
    source: Wolfgang
  AssignClass (76a133e8-c921-4eab-aed3-6e2774bfa141)
 Call ID: 76a133e8-c921-4eab-aed3-6e2774bfa141
  Args:
    source: Sophie_of_Prussia
    type: :Woman
  AssignClass (56a21006-0aef-4ae3-a481-28f2d0d63d7c)
 Call ID: 56a21006-0aef-4ae3-a481-28f2d0d63d7c
  Args:
    type: :Person
    source: Sophie_of_Prussia
  AssignClass (864c98fb-6217-44d2-a613-e3488e5801d6)
 Call ID: 864c98fb-6217-44d2-a613-e3488e5801d6
  Args:
    type: :Man
    source: Constantine_I
  AssignClass (0fb2ad58-000c-4e8d-b18e-c6e8aa82f3b7)
 Call ID: 0fb2ad58-000c-4e8d-b18e-c6e8aa82f3b7
  Args:
    source: Constantine_I
    type: :Person
  AssignClass (8188e622-ea8d-478f-be3a-fcb45030b6bc)
 Call ID: 8188e622-ea8d-478f-be3a-fcb45030b6bc
  Args:
    source: Mafalda_of_Savoy
    type: :Woman
  AssignClass (5294a76c-36a3-4973-90f5-73270e58173b)
 Call ID: 5294a76c-36a3-4973-90f5-73270e58173b
  Args:
    source: Mafalda_of_Savoy
    type: :Person
  AssignClass (5725102f-35a8-4b27-b9cd-991fdf5d1fc3)
 Call ID: 5725102f-35a8-4b27-b9cd-991fdf5d1fc3
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Man
  AssignClass (4eb3412b-a21f-477a-b06e-e3e44cc48766)
 Call ID: 4eb3412b-a21f-477a-b06e-e3e44cc48766
  Args:
    type: :Person
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (0e65618c-5db5-44ca-8b76-3608c68cd84c)
 Call ID: 0e65618c-5db5-44ca-8b76-3608c68cd84c
  Args:
    type: :Man
    source: Moritz
  AssignClass (fdd781c9-4730-46bf-8145-fdacbd01b10b)
 Call ID: fdd781c9-4730-46bf-8145-fdacbd01b10b
  Args:
    source: Moritz
    type: :Person
  AddTriple (05a86d14-e87e-4e91-b07e-941979e0c11b)
 Call ID: 05a86d14-e87e-4e91-b07e-941979e0c11b
  Args:
    source: Philipp
    target: Frederick_Charles_of_Hesse
    relation: :hasFather
  AddTriple (06d7b841-a7e3-4966-899b-6bb897383787)
 Call ID: 06d7b841-a7e3-4966-899b-6bb897383787
  Args:
    target: Margaret_of_Prussia
    relation: :hasMother
    source: Philipp
  AddTriple (8ce49b80-c503-4825-88d0-5e3b662807d5)
 Call ID: 8ce49b80-c503-4825-88d0-5e3b662807d5
  Args:
    relation: :isBrotherOf
    target: Philipp
    source: Friedrich_Wilhelm
  AddTriple (8bbfd6e7-4dd7-48a5-8a30-d4ba67488f6d)
 Call ID: 8bbfd6e7-4dd7-48a5-8a30-d4ba67488f6d
  Args:
    source: Wolfgang
    relation: :isBrotherOf
    target: Philipp
  AddTriple (cef0be04-19c9-4727-ae62-bb5a4f2ee186)
 Call ID: cef0be04-19c9-4727-ae62-bb5a4f2ee186
  Args:
    relation: :isSisterOf
    target: Wilhelm_II
    source: Margaret_of_Prussia
  AddTriple (f282ee77-e00a-4fed-8525-54629bde29f4)
 Call ID: f282ee77-e00a-4fed-8525-54629bde29f4
  Args:
    source: Sophie_of_Prussia
    target: Wilhelm_II
    relation: :isSisterOf
  AddTriple (f6ad28d6-e556-46b8-a65d-455f2fcbb754)
 Call ID: f6ad28d6-e556-46b8-a65d-455f2fcbb754
  Args:
    source: Victor_Emmanuel_III
    relation: :isFatherOf
    target: Mafalda_of_Savoy
  AddTriple (ee8e9853-d891-4e8b-82fd-db00c296734b)
 Call ID: ee8e9853-d891-4e8b-82fd-db00c296734b
  Args:
    source: Philipp
    relation: :hasFather
    target: Victor_Emmanuel_III
  AddLiteral (e4f34b36-a10d-4484-9e34-4a8532b61ae7)
 Call ID: e4f34b36-a10d-4484-9e34-4a8532b61ae7
  Args:
    relation: :hasMarriageYear
    source: Philipp
    literal_value: 1925
    literal_type: xsd:integer
  AddTriple (249cc048-d381-4612-a8aa-975c790d0acb)
 Call ID: 249cc048-d381-4612-a8aa-975c790d0acb
  Args:
    target: Moritz
    relation: :hasChild
    source: Philipp
  AddTriple (e4354257-21c5-403e-a186-a7b6cf597ace)
 Call ID: e4354257-21c5-403e-a186-a7b6cf597ace
  Args:
    source: Moritz
    target: Mafalda_of_Savoy
    relation: :hasMother
  AddTriple (5940eb74-90e4-4996-ab20-bb56b86e39d4)
 Call ID: 5940eb74-90e4-4996-ab20-bb56b86e39d4
  Args:
    source: Moritz
    relation: :hasFather
    target: Philipp
  Finish (9e01548e-79ad-40c5-9f9b-a0d903f0d3e5)
 Call ID: 9e01548e-79ad-40c5-9f9b-a0d903f0d3e5
  Args: