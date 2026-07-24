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
  AssignClass (3bd0de76-b5b6-49e1-a6b8-45f15dc8c947)
 Call ID: 3bd0de76-b5b6-49e1-a6b8-45f15dc8c947
  Args:
    source: Philipp_Prince_of_Hesse
    type: :Man
  AssignClass (a89f9bf6-6619-4240-bb3d-ab1b17054f8c)
 Call ID: a89f9bf6-6619-4240-bb3d-ab1b17054f8c
  Args:
    type: :Person
    source: Philipp_Prince_of_Hesse
  AddLiteral (2932f876-e06c-4b9e-8633-0e4f59033fc8)
 Call ID: 2932f876-e06c-4b9e-8633-0e4f59033fc8
  Args:
    relation: :hasBirthYear
    literal_value: 1896
    source: Philipp_Prince_of_Hesse
    literal_type: xsd:positiveInteger
  AddLiteral (c85e735d-2cfe-45dc-b844-a63e3def66f6)
 Call ID: c85e735d-2cfe-45dc-b844-a63e3def66f6
  Args:
    source: Philipp_Prince_of_Hesse
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1980
  AssignClass (520a4338-c97d-41f2-b0b3-40d9ad7bbb0c)
 Call ID: 520a4338-c97d-41f2-b0b3-40d9ad7bbb0c
  Args:
    source: Frederick_III_German_Emperor
    type: :Man
  AssignClass (3c8bfea5-2a95-4258-a29c-b9b7bd7e5d7c)
 Call ID: 3c8bfea5-2a95-4258-a29c-b9b7bd7e5d7c
  Args:
    type: :Person
    source: Frederick_III_German_Emperor
  AssignClass (1a6da839-ef5a-4ec7-9977-31cb289b4d55)
 Call ID: 1a6da839-ef5a-4ec7-9977-31cb289b4d55
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (1c8e1524-90a2-4cd7-9bfd-75b7fd6161b5)
 Call ID: 1c8e1524-90a2-4cd7-9bfd-75b7fd6161b5
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (e0095168-4e4e-468e-ba92-a05dc339104c)
 Call ID: e0095168-4e4e-468e-ba92-a05dc339104c
  Args:
    source: Victor_Emmanuel_III_of_Italy
    type: :Man
  AssignClass (2bf26f7d-f025-4373-9b8d-21c728f3dc3c)
 Call ID: 2bf26f7d-f025-4373-9b8d-21c728f3dc3c
  Args:
    type: :Person
    source: Victor_Emmanuel_III_of_Italy
  AssignClass (9cefee09-0e8d-42c2-a19f-bf5c4c32eec6)
 Call ID: 9cefee09-0e8d-42c2-a19f-bf5c4c32eec6
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Man
  AssignClass (70b227a5-318c-4e9d-9812-31073aa4ffc5)
 Call ID: 70b227a5-318c-4e9d-9812-31073aa4ffc5
  Args:
    source: Prince_Frederick_Charles_of_Hesse
    type: :Person
  AssignClass (200d206a-14e4-4f23-86c8-84e3bccff6a3)
 Call ID: 200d206a-14e4-4f23-86c8-84e3bccff6a3
  Args:
    type: :Woman
    source: Princess_Margaret_of_Prussia
  AssignClass (b0f8aedc-b2e7-411b-a643-415d07caa252)
 Call ID: b0f8aedc-b2e7-411b-a643-415d07caa252
  Args:
    type: :Person
    source: Princess_Margaret_of_Prussia
  AssignClass (9fa02ac9-9639-42f8-810e-cf86752944fb)
 Call ID: 9fa02ac9-9639-42f8-810e-cf86752944fb
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (a8e879a7-48ab-4577-90bc-b2e5ee7f7260)
 Call ID: a8e879a7-48ab-4577-90bc-b2e5ee7f7260
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Person
  AssignClass (3660b05b-8d47-4529-bb01-69d1011386b1)
 Call ID: 3660b05b-8d47-4529-bb01-69d1011386b1
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (134e964a-e5f0-4417-ba05-c53bb8cbf84f)
 Call ID: 134e964a-e5f0-4417-ba05-c53bb8cbf84f
  Args:
    type: :Person
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (73213cfc-eec8-4124-93e2-f1d83ff23054)
 Call ID: 73213cfc-eec8-4124-93e2-f1d83ff23054
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (cf23c266-da6c-4b9c-a20f-3502cab2a642)
 Call ID: cf23c266-da6c-4b9c-a20f-3502cab2a642
  Args:
    source: Wolfgang_of_Hesse
    type: :Person
  AssignClass (75b943b1-f8f4-4c53-a7d0-a6048fba44a7)
 Call ID: 75b943b1-f8f4-4c53-a7d0-a6048fba44a7
  Args:
    source: Princess_Sophie_of_Prussia
    type: :Woman
  AssignClass (f7282d48-b78f-4d3d-9331-b6b6246a7b47)
 Call ID: f7282d48-b78f-4d3d-9331-b6b6246a7b47
  Args:
    source: Princess_Sophie_of_Prussia
    type: :Person
  AssignClass (d3fc15d0-47fa-40f2-91bd-b8f7e0372189)
 Call ID: d3fc15d0-47fa-40f2-91bd-b8f7e0372189
  Args:
    type: :Man
    source: King_Constantine_I_of_Greece
  AssignClass (bf1ed991-13bb-47aa-ac9a-45b0067fd390)
 Call ID: bf1ed991-13bb-47aa-ac9a-45b0067fd390
  Args:
    type: :Person
    source: King_Constantine_I_of_Greece
  AssignClass (150208fe-1089-4f5c-8ea8-52c0e9d35245)
 Call ID: 150208fe-1089-4f5c-8ea8-52c0e9d35245
  Args:
    type: :Woman
    source: Princess_Mafalda_of_Savoy
  AssignClass (c7347b17-08a7-49bd-9512-4ef21e56c89d)
 Call ID: c7347b17-08a7-49bd-9512-4ef21e56c89d
  Args:
    type: :Person
    source: Princess_Mafalda_of_Savoy
  AssignClass (f27e7115-5452-444c-9f6d-3eb3b57c01ae)
 Call ID: f27e7115-5452-444c-9f6d-3eb3b57c01ae
  Args:
    type: :Man
    source: Louis_Prince_of_Hesse_and_by_Rhine
  AssignClass (5fb170dd-9cdf-4599-bf49-d352e74c2441)
 Call ID: 5fb170dd-9cdf-4599-bf49-d352e74c2441
  Args:
    source: Louis_Prince_of_Hesse_and_by_Rhine
    type: :Person
  AssignClass (c86d8709-6ff0-47af-b90e-64bc1e39e5dd)
 Call ID: c86d8709-6ff0-47af-b90e-64bc1e39e5dd
  Args:
    type: :Man
    source: Moritz_of_Hesse
  AssignClass (3ba1966c-de17-4ec5-9d32-2206a076eb44)
 Call ID: 3ba1966c-de17-4ec5-9d32-2206a076eb44
  Args:
    type: :Person
    source: Moritz_of_Hesse
  AddTriple (6ba085d5-b6ae-498a-89bc-9592251f0ee6)
 Call ID: 6ba085d5-b6ae-498a-89bc-9592251f0ee6
  Args:
    source: Philipp_Prince_of_Hesse
    relation: :hasFather
    target: Prince_Frederick_Charles_of_Hesse
  AddTriple (f3fa3078-c376-4498-85dc-838335fc749e)
 Call ID: f3fa3078-c376-4498-85dc-838335fc749e
  Args:
    target: Princess_Margaret_of_Prussia
    relation: :hasMother
    source: Philipp_Prince_of_Hesse
  AddTriple (7599eec0-eb53-4748-a32e-fb3ed0f4bb9f)
 Call ID: 7599eec0-eb53-4748-a32e-fb3ed0f4bb9f
  Args:
    source: Philipp_Prince_of_Hesse
    target: Victor_Emmanuel_III_of_Italy
    relation: :hasFather
  AddTriple (2b53d3d4-8baa-4979-b9d5-f3bf6cec5089)
 Call ID: 2b53d3d4-8baa-4979-b9d5-f3bf6cec5089
  Args:
    source: Philipp_Prince_of_Hesse
    target: Friedrich_Wilhelm_of_Hesse
    relation: :hasBrother
  AddTriple (ab0820a9-f635-4cbd-afd9-74f98d3be822)
 Call ID: ab0820a9-f635-4cbd-afd9-74f98d3be822
  Args:
    source: Philipp_Prince_of_Hesse
    target: Wolfgang_of_Hesse
    relation: :hasBrother
  AddTriple (e29ad464-bcf6-4696-a394-59c56970c2ec)
 Call ID: e29ad464-bcf6-4696-a394-59c56970c2ec
  Args:
    source: Wilhelm_II_German_Emperor
    relation: :hasSister
    target: Princess_Margaret_of_Prussia
  AddTriple (9c3ae492-eab9-49fb-928f-46261114f348)
 Call ID: 9c3ae492-eab9-49fb-928f-46261114f348
  Args:
    target: Victor_Emmanuel_III_of_Italy
    relation: :hasMother
    source: Princess_Mafalda_of_Savoy
  AddTriple (723a6cc1-ad10-4fbc-b0f1-5ff2a32249cd)
 Call ID: 723a6cc1-ad10-4fbc-b0f1-5ff2a32249cd
  Args:
    target: Moritz_of_Hesse
    relation: :hasSon
    source: Philipp_Prince_of_Hesse
  AddLiteral (7b789833-42cf-4c36-8d53-b22e70fec03a)
 Call ID: 7b789833-42cf-4c36-8d53-b22e70fec03a
  Args:
    literal_type: xsd:positiveInteger
    source: Philipp_Prince_of_Hesse
    literal_value: 1925
    relation: :hasMarriageYear
  Finish (ca2f3612-6458-43fd-a186-e82f1b56b7c7)
 Call ID: ca2f3612-6458-43fd-a186-e82f1b56b7c7
  Args: