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
  AssignClass (c99628d4-05a5-4bd6-a3f0-1830472d0413)
 Call ID: c99628d4-05a5-4bd6-a3f0-1830472d0413
  Args:
    type: :Woman
    source: Herzeleide_of_Prussia
  AssignClass (5044beea-2ea5-4874-9940-135f198b9d04)
 Call ID: 5044beea-2ea5-4874-9940-135f198b9d04
  Args:
    type: :Person
    source: Herzeleide_of_Prussia
  AddLiteral (bad391c1-3b1f-4b89-b25d-3e48d3c8db40)
 Call ID: bad391c1-3b1f-4b89-b25d-3e48d3c8db40
  Args:
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1918
  AddLiteral (cf22bc3f-4c75-46ab-ada3-a5e3a90db9ab)
 Call ID: cf22bc3f-4c75-46ab-ada3-a5e3a90db9ab
  Args:
    literal_type: xsd:integer
    source: Herzeleide_of_Prussia
    literal_value: 1989
    relation: :hasDeathYear
  AssignClass (4964f7dc-c0e7-4f1a-9f34-29a58104041b)
 Call ID: 4964f7dc-c0e7-4f1a-9f34-29a58104041b
  Args:
    type: :Man
    source: Oskar_of_Prussia
  AssignClass (58282245-19d6-48f0-8cf7-02caf7e7dcb2)
 Call ID: 58282245-19d6-48f0-8cf7-02caf7e7dcb2
  Args:
    type: :Ancestor
    source: Oskar_of_Prussia
  AssignClass (68bc5332-64bf-424a-b123-1078d6e0d513)
 Call ID: 68bc5332-64bf-424a-b123-1078d6e0d513
  Args:
    type: :Woman
    source: Ina_Marie_von_Bassewitz
  AssignClass (80ac2ccc-e894-4c4d-b57e-0f135ce10b07)
 Call ID: 80ac2ccc-e894-4c4d-b57e-0f135ce10b07
  Args:
    type: :Ancestor
    source: Ina_Marie_von_Bassewitz
  AddTriple (36e2cb2a-2430-405f-af1d-81f23a66ef38)
 Call ID: 36e2cb2a-2430-405f-af1d-81f23a66ef38
  Args:
    source: Herzeleide_of_Prussia
    target: Oskar_of_Prussia
    relation: :hasFather
  AddTriple (8b70ec50-a5c1-442d-b339-9ad1c453c46f)
 Call ID: 8b70ec50-a5c1-442d-b339-9ad1c453c46f
  Args:
    target: Ina_Marie_von_Bassewitz
    relation: :hasMother
    source: Herzeleide_of_Prussia
  AssignClass (f7fd879c-0085-4976-a746-45328570b2eb)
 Call ID: f7fd879c-0085-4976-a746-45328570b2eb
  Args:
    type: :Man
    source: Ernst-Johann_Biron
  AssignClass (6edf0378-9edc-46e5-b6b5-9a97e39876a6)
 Call ID: 6edf0378-9edc-46e5-b6b5-9a97e39876a6
  Args:
    type: :Person
    source: Ernst-Johann_Biron
  AddTriple (685f3fa1-1f64-489e-8047-0df414a2814d)
 Call ID: 685f3fa1-1f64-489e-8047-0df414a2814d
  Args:
    relation: :isMotherOf
    target: Ernst-Johann_Biron
    source: Herzeleide_of_Prussia
  AssignClass (d5ca65de-25a2-4a76-87ac-f9d3a87fba24)
 Call ID: d5ca65de-25a2-4a76-87ac-f9d3a87fba24
  Args:
    type: :Man
    source: Oscar_of_Prussia_brother
  AssignClass (bb3f87ca-6c58-48fa-8ddf-47399ddfa4b1)
 Call ID: bb3f87ca-6c58-48fa-8ddf-47399ddfa4b1
  Args:
    type: :Person
    source: Oscar_of_Prussia_brother
  AssignClass (c8c89612-eeed-49fb-99e1-58c8f77fa2e6)
 Call ID: c8c89612-eeed-49fb-99e1-58c8f77fa2e6
  Args:
    type: :Man
    source: Burchard_of_Prussia
  AssignClass (75c797ab-918e-4741-b351-0156cd9c8693)
 Call ID: 75c797ab-918e-4741-b351-0156cd9c8693
  Args:
    type: :Person
    source: Burchard_of_Prussia
  AssignClass (56df6001-9d86-4dd0-952c-0e2f7127f22f)
 Call ID: 56df6001-9d86-4dd0-952c-0e2f7127f22f
  Args:
    type: :Man
    source: Wilhelm-Karl_of_Prussia
  AssignClass (48bc1420-0c6a-457b-8fb1-10ca0cc33f93)
 Call ID: 48bc1420-0c6a-457b-8fb1-10ca0cc33f93
  Args:
    type: :Person
    source: Wilhelm-Karl_of_Prussia
  AddTriple (70e44e77-3d08-4ac0-9261-831432c3c342)
 Call ID: 70e44e77-3d08-4ac0-9261-831432c3c342
  Args:
    relation: :hasBrother
    target: Oscar_of_Prussia_brother
    source: Herzeleide_of_Prussia
  AddTriple (0a37d984-a361-44bb-b670-5878b710bc79)
 Call ID: 0a37d984-a361-44bb-b670-5878b710bc79
  Args:
    target: Burchard_of_Prussia
    relation: :hasBrother
    source: Herzeleide_of_Prussia
  AddTriple (ac2e055c-7ebe-46d1-81a8-01b338801e82)
 Call ID: ac2e055c-7ebe-46d1-81a8-01b338801e82
  Args:
    relation: :hasBrother
    target: Wilhelm-Karl_of_Prussia
    source: Herzeleide_of_Prussia
  AssignClass (9cfa5226-bd80-4c68-a933-1c1cd1aab0d8)
 Call ID: 9cfa5226-bd80-4c68-a933-1c1cd1aab0d8
  Args:
    type: :Man
    source: Karl_Biron_von_Courland
  AssignClass (1dfc1108-eadf-4700-99b8-edd8a12ecdef)
 Call ID: 1dfc1108-eadf-4700-99b8-edd8a12ecdef
  Args:
    type: :Person
    source: Karl_Biron_von_Courland
  AddLiteral (28db2cc1-76e5-456a-8926-7f2841aaf4b3)
 Call ID: 28db2cc1-76e5-456a-8926-7f2841aaf4b3
  Args:
    relation: :hasMarriageYear
    literal_value: 1938
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
  AddTriple (0d8aa627-2a0f-4d8e-a033-54e873f9f125)
 Call ID: 0d8aa627-2a0f-4d8e-a033-54e873f9f125
  Args:
    source: Herzeleide_of_Prussia
    relation: :hasRelation
    target: Karl_Biron_von_Courland
  AddLiteral (7eb076f6-d982-456b-931b-54c2bfc6dffb)
 Call ID: 7eb076f6-d982-456b-931b-54c2bfc6dffb
  Args:
    literal_value: 1907
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Karl_Biron_von_Courland
  AddLiteral (1b4cd126-3ed6-4f75-b08f-bb18ae7247f5)
 Call ID: 1b4cd126-3ed6-4f75-b08f-bb18ae7247f5
  Args:
    literal_type: xsd:integer
    source: Karl_Biron_von_Courland
    literal_value: 1982
    relation: :hasDeathYear
  AssignClass (eb9e92d4-7f9b-4754-a93d-1d2a4536c999)
 Call ID: eb9e92d4-7f9b-4754-a93d-1d2a4536c999
  Args:
    type: :Man
    source: Gustav_Biron_of_Courland
  AssignClass (9bb582b6-28e8-4156-8322-cbdc82c27a45)
 Call ID: 9bb582b6-28e8-4156-8322-cbdc82c27a45
  Args:
    type: :Ancestor
    source: Gustav_Biron_of_Courland
  AssignClass (3fe76304-9f2a-42f2-84bd-64947a5df3bf)
 Call ID: 3fe76304-9f2a-42f2-84bd-64947a5df3bf
  Args:
    type: :Woman
    source: Francoise_Levisse_de_Montigny
  AssignClass (5816f8de-f8bd-4437-98c3-a58c12e565bf)
 Call ID: 5816f8de-f8bd-4437-98c3-a58c12e565bf
  Args:
    type: :Ancestor
    source: Francoise_Levisse_de_Montigny
  AddTriple (a629cca5-3470-48c4-bd5b-c54193127b74)
 Call ID: a629cca5-3470-48c4-bd5b-c54193127b74
  Args:
    source: Karl_Biron_von_Courland
    relation: :hasFather
    target: Gustav_Biron_of_Courland
  AddTriple (6f218bd1-6cee-450e-a9d5-1a2fa09c7276)
 Call ID: 6f218bd1-6cee-450e-a9d5-1a2fa09c7276
  Args:
    source: Karl_Biron_von_Courland
    relation: :hasMother
    target: Francoise_Levisse_de_Montigny
  Finish (49ce727c-400c-4fbb-85bf-22672e7c1134)
 Call ID: 49ce727c-400c-4fbb-85bf-22672e7c1134
  Args: