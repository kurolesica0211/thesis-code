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
In August 1944, the factory was bombed by the Allies.
Mafalda was seriously injured and died several days later following a belated operation by camp medical staff.
After only ten days, he was transferred to Tyrol to Hotel "Bachmann" along with about 140 other prominent prisoners (for example Kurt Schuschnigg, Bogislaw von Bonin, Hjalmar Schacht, Martin Niemöller, Georg Thomas, and Alexander von Falkenhausen), freed by the Wehrmacht on 30 April 1945 (SS-Obergruppenführer Karl Wolff received a telephone call from the SS guards and ordered them to hand over the prisoners to the German army officers Hauptmann Wichard von Alvensleben and Hauptmann Gebhard von Alvensleben), and was then arrested by U.S. troops on 4 May 1945 in Niederdorf in the Italian Dolomites due to his role in the Nazi Party.
On 28 May 1940, Philipp succeeded his father as Head of the Electoral House of Hesse.
In 1968, upon the death of his distant agnatic relative, Louis, Prince of Hesse and by Rhine (who was also his second cousin as Philipp's mother and Louis' father were grandchildren of Queen Victoria), Philipp succeeded as head of the entire House of Hesse, including grand ducal Hesse (Hesse and by Rhine/Hesse-Darmstadt).
Louis had nominally adopted Philipp's son Moritz, who at that time inherited the Hessian and by-Rhine properties, including remarkable cultural collections: for the first time since the division of Hesse into branches after the death of Philip the Magnanimous in 1567, all sovereign branches of the house of Hesse were reunited again.



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
  AssignClass (09593b50-d42d-4105-a8cd-0d13eaa6545d)
 Call ID: 09593b50-d42d-4105-a8cd-0d13eaa6545d
  Args:
    source: Philipp_of_Hesse
    type: :Man
  AssignClass (24e75576-1fc9-4a30-9eb6-5e40caea99e3)
 Call ID: 24e75576-1fc9-4a30-9eb6-5e40caea99e3
  Args:
    type: :Person
    source: Philipp_of_Hesse
  AddLiteral (0084ded6-f26e-40ae-82b9-835530794c7d)
 Call ID: 0084ded6-f26e-40ae-82b9-835530794c7d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Philipp_of_Hesse
    literal_value: 1896
  AddLiteral (022bfaf0-d522-446a-9375-1688f1dda264)
 Call ID: 022bfaf0-d522-446a-9375-1688f1dda264
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Philipp_of_Hesse
    literal_value: 1980
  AssignClass (04d5dd25-f94c-40e4-8c26-329951046339)
 Call ID: 04d5dd25-f94c-40e4-8c26-329951046339
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AssignClass (04d52c57-362c-4636-b6e4-34981e8800e6)
 Call ID: 04d52c57-362c-4636-b6e4-34981e8800e6
  Args:
    type: :Person
    source: Frederick_Charles_of_Hesse
  AddTriple (279ae965-a595-403f-9c73-7699d91a5647)
 Call ID: 279ae965-a595-403f-9c73-7699d91a5647
  Args:
    source: Philipp_of_Hesse
    relation: :hasFather
    target: Frederick_Charles_of_Hesse
  AssignClass (0adf728f-21f5-4fd2-95fe-3dd30b7f1da0)
 Call ID: 0adf728f-21f5-4fd2-95fe-3dd30b7f1da0
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (9bfd9a4d-79ac-4714-9f19-be759a70b1ff)
 Call ID: 9bfd9a4d-79ac-4714-9f19-be759a70b1ff
  Args:
    source: Margaret_of_Prussia
    type: :Person
  AddTriple (3361adb6-e7fa-48b6-85a3-e96c8c4473d5)
 Call ID: 3361adb6-e7fa-48b6-85a3-e96c8c4473d5
  Args:
    relation: :hasMother
    target: Margaret_of_Prussia
    source: Philipp_of_Hesse
  AssignClass (b5563a4d-52c4-4e98-ab80-b58c6c310551)
 Call ID: b5563a4d-52c4-4e98-ab80-b58c6c310551
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    type: :Man
  AssignClass (3a3b3c0f-f29a-4e44-8a4c-af7ae3be1c47)
 Call ID: 3a3b3c0f-f29a-4e44-8a4c-af7ae3be1c47
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    type: :Person
  AddTriple (7b7ce656-d9a8-47ef-8b65-f4498188ccab)
 Call ID: 7b7ce656-d9a8-47ef-8b65-f4498188ccab
  Args:
    source: Friedrich_Wilhelm_of_Hesse
    relation: :isBrotherOf
    target: Philipp_of_Hesse
  AssignClass (a387173d-42f9-4d8e-a0c6-5ca8944cb536)
 Call ID: a387173d-42f9-4d8e-a0c6-5ca8944cb536
  Args:
    source: Wolfgang_of_Hesse
    type: :Man
  AssignClass (afa9f17d-bc0b-4328-9ccd-529932b589f6)
 Call ID: afa9f17d-bc0b-4328-9ccd-529932b589f6
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AddTriple (aedefb69-3fa6-459e-ba35-f060e86b134d)
 Call ID: aedefb69-3fa6-459e-ba35-f060e86b134d
  Args:
    source: Wolfgang_of_Hesse
    relation: :isBrotherOf
    target: Philipp_of_Hesse
  AssignClass (2d16e288-f7cb-4431-aac3-8207b8c8f9fd)
 Call ID: 2d16e288-f7cb-4431-aac3-8207b8c8f9fd
  Args:
    type: :Woman
    source: Mafalda_of_Savoy
  AssignClass (3f8a5525-0185-4189-8160-cdb20d15bc50)
 Call ID: 3f8a5525-0185-4189-8160-cdb20d15bc50
  Args:
    source: Mafalda_of_Savoy
    type: :Person
  AddTriple (a2d79cbe-6f7d-4269-8cbe-3841d237d7f5)
 Call ID: a2d79cbe-6f7d-4269-8cbe-3841d237d7f5
  Args:
    source: Philipp_of_Hesse
    relation: :hasRelation
    target: Mafalda_of_Savoy
  AddLiteral (16addf6f-1656-4c9f-8fe4-b69b7a11a144)
 Call ID: 16addf6f-1656-4c9f-8fe4-b69b7a11a144
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Philipp_of_Hesse
    literal_value: 1925
  AssignClass (66aa6c1b-a80d-4099-adda-347940c03821)
 Call ID: 66aa6c1b-a80d-4099-adda-347940c03821
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Man
  AssignClass (d7080793-b0f9-4ee8-8f7f-ee83fcdd7265)
 Call ID: d7080793-b0f9-4ee8-8f7f-ee83fcdd7265
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Person
  AddTriple (566d7c36-1b60-4f4d-bb2c-3793952e6c9e)
 Call ID: 566d7c36-1b60-4f4d-bb2c-3793952e6c9e
  Args:
    source: Victor_Emmanuel_III_of_Italy
    relation: :isFatherOf
    target: Mafalda_of_Savoy
  AssignClass (9d288ea1-f497-4c68-95da-38154d8a5de6)
 Call ID: 9d288ea1-f497-4c68-95da-38154d8a5de6
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AssignClass (05570de6-8ae7-4107-a412-90c4aa24fb77)
 Call ID: 05570de6-8ae7-4107-a412-90c4aa24fb77
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AddTriple (dd8d5d36-aa20-42af-8fe6-64eea5585c1d)
 Call ID: dd8d5d36-aa20-42af-8fe6-64eea5585c1d
  Args:
    source: Moritz_of_Hesse
    relation: :isSonOf
    target: Philipp_of_Hesse
  AddTriple (deea6cb4-352c-4fbd-a67d-7effb90667ce)
 Call ID: deea6cb4-352c-4fbd-a67d-7effb90667ce
  Args:
    relation: :isSonOf
    target: Mafalda_of_Savoy
    source: Moritz_of_Hesse
  AssignClass (3e71b8b3-2a47-49fe-9453-39b1d2f22c87)
 Call ID: 3e71b8b3-2a47-49fe-9453-39b1d2f22c87
  Args:
    type: :Woman
    source: Sophie_of_Prussia
  AssignClass (4a37d8ee-65be-4445-a72a-e877f51cd126)
 Call ID: 4a37d8ee-65be-4445-a72a-e877f51cd126
  Args:
    source: Sophie_of_Prussia
    type: :Person
  AddTriple (0f620fd2-3803-4398-a2d6-403960af0748)
 Call ID: 0f620fd2-3803-4398-a2d6-403960af0748
  Args:
    source: Sophie_of_Prussia
    relation: :isAuntOf
    target: Philipp_of_Hesse
  AssignClass (e81225a4-5c95-43bb-8989-31209e1e79a0)
 Call ID: e81225a4-5c95-43bb-8989-31209e1e79a0
  Args:
    source: Constantine_I_of_Greece
    type: :Man
  AssignClass (fea7532e-69e5-422b-9c25-ff9e7811fc16)
 Call ID: fea7532e-69e5-422b-9c25-ff9e7811fc16
  Args:
    source: Constantine_I_of_Greece
    type: :Person
  AddTriple (8bc9defd-294c-499d-832e-4701f872437e)
 Call ID: 8bc9defd-294c-499d-832e-4701f872437e
  Args:
    source: Sophie_of_Prussia
    relation: :hasRelation
    target: Constantine_I_of_Greece
  Finish (4c67e960-2e7d-4d6c-80dc-8b6ada536bd8)
 Call ID: 4c67e960-2e7d-4d6c-80dc-8b6ada536bd8
  Args: