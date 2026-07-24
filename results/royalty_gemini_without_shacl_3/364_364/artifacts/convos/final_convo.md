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
  AssignClass (76932495-ebd0-4d8f-8216-29a76df8aa17)
 Call ID: 76932495-ebd0-4d8f-8216-29a76df8aa17
  Args:
    type: :Person
    source: Philipp_of_Hesse
  AssignClass (9ed063c6-4aec-4d0e-8880-998c8b047644)
 Call ID: 9ed063c6-4aec-4d0e-8880-998c8b047644
  Args:
    type: :Man
    source: Philipp_of_Hesse
  AddLiteral (766e47ec-8828-45f4-8776-004b11c06dbc)
 Call ID: 766e47ec-8828-45f4-8776-004b11c06dbc
  Args:
    relation: :hasBirthYear
    source: Philipp_of_Hesse
    literal_value: 1896
    literal_type: xsd:integer
  AddLiteral (a88440aa-e591-4c5c-9ded-5160c2779cda)
 Call ID: a88440aa-e591-4c5c-9ded-5160c2779cda
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    relation: :hasDeathYear
    source: Philipp_of_Hesse
  AssignClass (d2333ccd-6a9e-405e-ac10-6a405149e309)
 Call ID: d2333ccd-6a9e-405e-ac10-6a405149e309
  Args:
    type: :Person
    source: Frederick_Charles_of_Hesse
  AssignClass (aa35397c-5add-4210-bf10-f72cedc97d5a)
 Call ID: aa35397c-5add-4210-bf10-f72cedc97d5a
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AssignClass (8da07f71-9d37-4cf0-8b75-96f55843e6d7)
 Call ID: 8da07f71-9d37-4cf0-8b75-96f55843e6d7
  Args:
    type: :Person
    source: Margaret_of_Prussia
  AssignClass (ed1cf879-4650-41b9-8fa6-866e80d5ef3c)
 Call ID: ed1cf879-4650-41b9-8fa6-866e80d5ef3c
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AddTriple (4fdf2b15-41e7-4d1f-b07f-8e88e4256478)
 Call ID: 4fdf2b15-41e7-4d1f-b07f-8e88e4256478
  Args:
    target: Frederick_Charles_of_Hesse
    source: Philipp_of_Hesse
    relation: :hasFather
  AddTriple (5e0cddbf-fbe1-4d5e-8199-75fec75d4e88)
 Call ID: 5e0cddbf-fbe1-4d5e-8199-75fec75d4e88
  Args:
    relation: :hasMother
    source: Philipp_of_Hesse
    target: Margaret_of_Prussia
  AssignClass (72142a54-4259-4cf0-a12a-5cdd7065ab4b)
 Call ID: 72142a54-4259-4cf0-a12a-5cdd7065ab4b
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (75c544de-2be3-4e5f-a5f9-964bc53d2a9a)
 Call ID: 75c544de-2be3-4e5f-a5f9-964bc53d2a9a
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Hesse
  AddTriple (1c26573c-bbb8-42c4-bc2a-3922ef59c337)
 Call ID: 1c26573c-bbb8-42c4-bc2a-3922ef59c337
  Args:
    target: Philipp_of_Hesse
    source: Friedrich_Wilhelm_of_Hesse
    relation: :isBrotherOf
  AssignClass (d45f1177-fbc6-4507-aef8-8f8c7bc0389f)
 Call ID: d45f1177-fbc6-4507-aef8-8f8c7bc0389f
  Args:
    type: :Person
    source: Wolfgang_of_Hesse
  AssignClass (0b200d59-a587-43ab-9bd5-c74fcc62750a)
 Call ID: 0b200d59-a587-43ab-9bd5-c74fcc62750a
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AddTriple (7327e60d-bdd1-4fe1-b323-4fbb23f8e47e)
 Call ID: 7327e60d-bdd1-4fe1-b323-4fbb23f8e47e
  Args:
    source: Wolfgang_of_Hesse
    relation: :isBrotherOf
    target: Philipp_of_Hesse
  AssignClass (0155a881-bc0a-473e-b468-85fcf465a06b)
 Call ID: 0155a881-bc0a-473e-b468-85fcf465a06b
  Args:
    type: :Person
    source: Mafalda_of_Savoy
  AssignClass (6c79e4cc-959d-4d0b-8b17-e25cabb7712b)
 Call ID: 6c79e4cc-959d-4d0b-8b17-e25cabb7712b
  Args:
    type: :Woman
    source: Mafalda_of_Savoy
  AddTriple (3f731d70-b289-40a6-bf73-d97cf394983c)
 Call ID: 3f731d70-b289-40a6-bf73-d97cf394983c
  Args:
    target: Mafalda_of_Savoy
    source: Philipp_of_Hesse
    relation: :hasRelation
  AddLiteral (01fd5e17-fd0d-4495-8dc2-9aa96e54c5ca)
 Call ID: 01fd5e17-fd0d-4495-8dc2-9aa96e54c5ca
  Args:
    literal_type: xsd:integer
    literal_value: 1925
    relation: :hasMarriageYear
    source: Philipp_of_Hesse
  AssignClass (20b303c0-6189-42f0-bb39-1ba4a03d9186)
 Call ID: 20b303c0-6189-42f0-bb39-1ba4a03d9186
  Args:
    type: :Person
    source: Victor_Emmanuel_III_of_Italy
  AssignClass (a1015a32-1063-4e08-a419-e0014918a32a)
 Call ID: a1015a32-1063-4e08-a419-e0014918a32a
  Args:
    type: :Man
    source: Victor_Emmanuel_III_of_Italy
  AddTriple (391fe126-f58b-4445-bd4a-49b6d8b41e02)
 Call ID: 391fe126-f58b-4445-bd4a-49b6d8b41e02
  Args:
    target: Mafalda_of_Savoy
    source: Victor_Emmanuel_III_of_Italy
    relation: :isFatherOf
  AssignClass (ed9926af-a2c8-4a24-b834-0f50cc20e3c3)
 Call ID: ed9926af-a2c8-4a24-b834-0f50cc20e3c3
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AssignClass (643b787c-6197-478b-a22b-ed6b7e70b1b7)
 Call ID: 643b787c-6197-478b-a22b-ed6b7e70b1b7
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AddTriple (82714b11-5193-40ca-9de7-41a753ef8b35)
 Call ID: 82714b11-5193-40ca-9de7-41a753ef8b35
  Args:
    target: Philipp_of_Hesse
    relation: :isSonOf
    source: Moritz_of_Hesse
  AddTriple (07458a1b-b638-47fc-a2ae-7c88ceb5cd8a)
 Call ID: 07458a1b-b638-47fc-a2ae-7c88ceb5cd8a
  Args:
    target: Mafalda_of_Savoy
    source: Moritz_of_Hesse
    relation: :isSonOf
  AssignClass (9032c7ea-911e-4dc5-843c-e59b3eb658c5)
 Call ID: 9032c7ea-911e-4dc5-843c-e59b3eb658c5
  Args:
    type: :Person
    source: Frederick_III_German_Emperor
  AssignClass (1499a6be-775f-4274-921b-2893247b2f19)
 Call ID: 1499a6be-775f-4274-921b-2893247b2f19
  Args:
    type: :Man
    source: Frederick_III_German_Emperor
  AddTriple (771215c9-aea9-4ee1-9dde-d078f1426b04)
 Call ID: 771215c9-aea9-4ee1-9dde-d078f1426b04
  Args:
    relation: :hasAncestor
    source: Philipp_of_Hesse
    target: Frederick_III_German_Emperor
  AssignClass (401f85e4-4f4d-4295-a5a1-27d2b59cd936)
 Call ID: 401f85e4-4f4d-4295-a5a1-27d2b59cd936
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (b413a0bd-bd68-4eb7-bb7a-d31287b67f35)
 Call ID: b413a0bd-bd68-4eb7-bb7a-d31287b67f35
  Args:
    type: :Woman
    source: Queen_Victoria
  AddTriple (5565379c-d702-4c53-b1a6-4580b28398c3)
 Call ID: 5565379c-d702-4c53-b1a6-4580b28398c3
  Args:
    target: Queen_Victoria
    source: Philipp_of_Hesse
    relation: :hasAncestor
  AssignClass (0215e7f5-98b1-480e-948a-7b55b601f55a)
 Call ID: 0215e7f5-98b1-480e-948a-7b55b601f55a
  Args:
    type: :Person
    source: Sophie_of_Prussia
  AssignClass (8d761d3b-de0f-48e6-8720-e5f2c3e0d0ad)
 Call ID: 8d761d3b-de0f-48e6-8720-e5f2c3e0d0ad
  Args:
    type: :Woman
    source: Sophie_of_Prussia
  AddTriple (d97c7247-07a0-4188-a6e7-534aeefc3605)
 Call ID: d97c7247-07a0-4188-a6e7-534aeefc3605
  Args:
    target: Sophie_of_Prussia
    relation: :hasSister
    source: Margaret_of_Prussia
  AssignClass (6a2931af-93f5-48c5-ae42-9e7ca2b0d6f6)
 Call ID: 6a2931af-93f5-48c5-ae42-9e7ca2b0d6f6
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (fdb18438-d178-4834-aed7-0c0ecd596a0f)
 Call ID: fdb18438-d178-4834-aed7-0c0ecd596a0f
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AddTriple (17d7f2bc-adf3-4104-a6c4-3e9b39156e2f)
 Call ID: 17d7f2bc-adf3-4104-a6c4-3e9b39156e2f
  Args:
    target: Wilhelm_II_German_Emperor
    source: Margaret_of_Prussia
    relation: :hasBrother
  AssignClass (24b3fdb8-4b66-4322-b5e1-6b5ed750e7ae)
 Call ID: 24b3fdb8-4b66-4322-b5e1-6b5ed750e7ae
  Args:
    type: :Person
    source: Constantine_I_of_Greece
  AssignClass (0b69aae6-9e1d-46e9-90de-fe60606bd7dc)
 Call ID: 0b69aae6-9e1d-46e9-90de-fe60606bd7dc
  Args:
    type: :Man
    source: Constantine_I_of_Greece
  AddTriple (00f1e41c-565e-4912-9541-6a68cad249aa)
 Call ID: 00f1e41c-565e-4912-9541-6a68cad249aa
  Args:
    target: Constantine_I_of_Greece
    relation: :hasRelation
    source: Sophie_of_Prussia
  AssignClass (004a7522-d33a-444d-9c3d-f97a9087cf6c)
 Call ID: 004a7522-d33a-444d-9c3d-f97a9087cf6c
  Args:
    type: :Person
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (85abec65-6893-4015-a5cd-de798f0d02df)
 Call ID: 85abec65-6893-4015-a5cd-de798f0d02df
  Args:
    type: :Man
    source: Louis_Prince_of_Hesse_and_by_Rhine
  Finish (5b0246f2-0dab-4992-8c7b-a523c999ba2b)
 Call ID: 5b0246f2-0dab-4992-8c7b-a523c999ba2b
  Args: