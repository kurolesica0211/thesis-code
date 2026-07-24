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
Princess Herzeleide Ina-Marie Sophie Charlotte Else of Prussia (25 December 1918 – 22 March 1989) was a member of the deposed House of Hohenzollern.
She was the only daughter of Prince Oskar of Prussia (the second youngest son of Emperor Wilhelm II) and his initially morganatic wife, Countess Ina Marie von Bassewitz.
She is the mother of Ernst-Johann Biron, Prince of Courland, the current head of the House of Biron.
Biography

Family and early life

Countess Herzeleide-Ina-Marie von Ruppin was born in Bristow, Mecklenburg, on 25 December 1918, shortly after the defeat of the German Empire and the collapse of the monarchy.
She was consequently given the name Herzeleide, meaning "heart's sorrow".
She had three brothers: Oscar, Burchard, and Wilhelm-Karl.
Herzeleide and her brothers became Princess/Prince of Prussia on 21 June 1920 when their parents' morganatic marriage was recognised as dynastic by the deposed Emperor Wilhelm II.
In early 1938, Herzeleide was one of three bridesmaids at the wedding of the future King Paul of Greece to Frederica of Hanover, her first cousin.
Marriage and issue

On 15 August 1938 in Potsdam Garrison Church, Herzeleide married Prince Karl Biron von Courland (15 June 1907 – 28 February 1982).
Karl was the eldest son and heir of Prince Gustav Biron of Courland and Françoise Lévisse de Montigny, daughter of Marquis de Jaucourt.
Along with the bride and groom's parents, in attendance were the former German Crown Prince Wilhelm and Emperor Wilhelm's consort, Empress Hermine.
All male guests wore uniforms of the former German army.
The couple's honeymoon plans included a visit to Doorn to pay respects to Emperor Wilhelm in exile, the bride's paternal grandfather.



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
  AssignClass (76ee2f61-04f8-4b9e-86c6-f10e800317ae)
 Call ID: 76ee2f61-04f8-4b9e-86c6-f10e800317ae
  Args:
    type: :Person
    source: Herzeleide_of_Prussia
  AssignClass (5c5bee8a-644a-4cba-b9dd-480d3bab9474)
 Call ID: 5c5bee8a-644a-4cba-b9dd-480d3bab9474
  Args:
    source: Herzeleide_of_Prussia
    type: :Woman
  AddLiteral (cc6dbc44-737c-4916-b134-672ed0f50337)
 Call ID: cc6dbc44-737c-4916-b134-672ed0f50337
  Args:
    literal_value: 1918
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Herzeleide_of_Prussia
  AddLiteral (1139a9af-317a-49aa-be52-926a491b814f)
 Call ID: 1139a9af-317a-49aa-be52-926a491b814f
  Args:
    source: Herzeleide_of_Prussia
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1989
  AssignClass (8475f027-0199-451f-bca7-b9637b465dc3)
 Call ID: 8475f027-0199-451f-bca7-b9637b465dc3
  Args:
    source: Oskar_of_Prussia
    type: :Person
  AssignClass (6f149f35-0101-4ac9-8db9-d2af1fd9d7c9)
 Call ID: 6f149f35-0101-4ac9-8db9-d2af1fd9d7c9
  Args:
    type: :Man
    source: Oskar_of_Prussia
  AssignClass (8638937d-3f9b-465b-8db3-6599ba873668)
 Call ID: 8638937d-3f9b-465b-8db3-6599ba873668
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Person
  AssignClass (434dd8c7-ac6d-4906-b82f-a8300c50e019)
 Call ID: 434dd8c7-ac6d-4906-b82f-a8300c50e019
  Args:
    type: :Woman
    source: Ina_Marie_von_Bassewitz
  AddTriple (75b59cc7-076f-4607-b85b-2fe488c3fdb2)
 Call ID: 75b59cc7-076f-4607-b85b-2fe488c3fdb2
  Args:
    target: Oskar_of_Prussia
    source: Herzeleide_of_Prussia
    relation: :hasFather
  AddTriple (54388fc1-ca40-44d8-9c54-a6c7572467b8)
 Call ID: 54388fc1-ca40-44d8-9c54-a6c7572467b8
  Args:
    source: Herzeleide_of_Prussia
    target: Ina_Marie_von_Bassewitz
    relation: :hasMother
  AssignClass (3cfb9cbf-8be0-4785-99ec-faa82bbc81d8)
 Call ID: 3cfb9cbf-8be0-4785-99ec-faa82bbc81d8
  Args:
    type: :Person
    source: Ernst-Johann_Biron
  AssignClass (4b3caee6-4308-4fee-ac23-3efabbdf2c71)
 Call ID: 4b3caee6-4308-4fee-ac23-3efabbdf2c71
  Args:
    type: :Man
    source: Ernst-Johann_Biron
  AddTriple (ea74934c-3352-4c5d-b941-b3986487936b)
 Call ID: ea74934c-3352-4c5d-b941-b3986487936b
  Args:
    relation: :isMotherOf
    source: Herzeleide_of_Prussia
    target: Ernst-Johann_Biron
  AssignClass (f7ef1d64-d0c0-4842-adaf-c22c6bb3e9f5)
 Call ID: f7ef1d64-d0c0-4842-adaf-c22c6bb3e9f5
  Args:
    source: Oscar_brother
    type: :Person
  AssignClass (b0b85d8d-5bfc-4320-835a-81595d2ea41c)
 Call ID: b0b85d8d-5bfc-4320-835a-81595d2ea41c
  Args:
    source: Oscar_brother
    type: :Man
  AssignClass (b33a1e0f-7798-4394-ae7b-db32780b19f6)
 Call ID: b33a1e0f-7798-4394-ae7b-db32780b19f6
  Args:
    source: Burchard_brother
    type: :Person
  AssignClass (60b8001f-3532-4f93-b3f5-b55303a5ecbe)
 Call ID: 60b8001f-3532-4f93-b3f5-b55303a5ecbe
  Args:
    source: Burchard_brother
    type: :Man
  AssignClass (d44c7eb2-3fd9-4b1f-bc4b-d99f922958cb)
 Call ID: d44c7eb2-3fd9-4b1f-bc4b-d99f922958cb
  Args:
    type: :Person
    source: Wilhelm-Karl_brother
  AssignClass (6ba40701-68ad-48c9-b7b0-fe1db539475d)
 Call ID: 6ba40701-68ad-48c9-b7b0-fe1db539475d
  Args:
    type: :Man
    source: Wilhelm-Karl_brother
  AddTriple (986192a7-cda5-4b47-9ad6-969906ae16c4)
 Call ID: 986192a7-cda5-4b47-9ad6-969906ae16c4
  Args:
    relation: :hasBrother
    source: Herzeleide_of_Prussia
    target: Oscar_brother
  AddTriple (fc89e07c-49ff-4f01-8fc8-205b3465fe2d)
 Call ID: fc89e07c-49ff-4f01-8fc8-205b3465fe2d
  Args:
    relation: :hasBrother
    target: Burchard_brother
    source: Herzeleide_of_Prussia
  AddTriple (fb9b9106-d79a-4095-a456-7116be955c7e)
 Call ID: fb9b9106-d79a-4095-a456-7116be955c7e
  Args:
    source: Herzeleide_of_Prussia
    target: Wilhelm-Karl_brother
    relation: :hasBrother
  AssignClass (cb6d4654-6117-4285-931f-3845de91db02)
 Call ID: cb6d4654-6117-4285-931f-3845de91db02
  Args:
    type: :Person
    source: Karl_Biron_von_Courland
  AssignClass (225f7603-3852-478a-b2a6-68872c51bb05)
 Call ID: 225f7603-3852-478a-b2a6-68872c51bb05
  Args:
    type: :Man
    source: Karl_Biron_von_Courland
  AddLiteral (5c1164de-b342-4088-8c95-dea3bf81fcce)
 Call ID: 5c1164de-b342-4088-8c95-dea3bf81fcce
  Args:
    literal_value: 1938
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (65a1716f-9715-4b49-8040-8cb9cec5c4df)
 Call ID: 65a1716f-9715-4b49-8040-8cb9cec5c4df
  Args:
    source: Herzeleide_of_Prussia
    target: Karl_Biron_von_Courland
    relation: :hasRelation
  AssignClass (94e50305-458a-4c1d-a87c-66168e4d67a6)
 Call ID: 94e50305-458a-4c1d-a87c-66168e4d67a6
  Args:
    source: Gustav_Biron_of_Courland
    type: :Person
  AssignClass (7711aa2b-2254-4886-ac11-df2d66b819b5)
 Call ID: 7711aa2b-2254-4886-ac11-df2d66b819b5
  Args:
    type: :Man
    source: Gustav_Biron_of_Courland
  AssignClass (792a447b-936c-42d6-9f32-cc28d98a3746)
 Call ID: 792a447b-936c-42d6-9f32-cc28d98a3746
  Args:
    type: :Person
    source: Francoise_Levisse_de_Montigny
  AssignClass (4751ef85-a677-4aeb-ae72-d9c8b3d45cb0)
 Call ID: 4751ef85-a677-4aeb-ae72-d9c8b3d45cb0
  Args:
    type: :Woman
    source: Francoise_Levisse_de_Montigny
  AddTriple (d6022feb-440d-4ff5-a837-247831cafd7f)
 Call ID: d6022feb-440d-4ff5-a837-247831cafd7f
  Args:
    relation: :hasFather
    target: Gustav_Biron_of_Courland
    source: Karl_Biron_von_Courland
  AddTriple (fb59041b-cc41-4822-be2e-360fc2e20139)
 Call ID: fb59041b-cc41-4822-be2e-360fc2e20139
  Args:
    relation: :hasMother
    source: Karl_Biron_von_Courland
    target: Francoise_Levisse_de_Montigny
  Finish (fe669eea-9270-458e-b34c-356501e1d680)
 Call ID: fe669eea-9270-458e-b34c-356501e1d680
  Args: