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
  AssignClass (f3a2f53b-c33b-4598-a1d9-d023e324e439)
 Call ID: f3a2f53b-c33b-4598-a1d9-d023e324e439
  Args:
    type: :Woman
    source: Herzeleide_of_Prussia
  AssignClass (a9856ade-9530-4a91-98e1-ec26cf49c4ed)
 Call ID: a9856ade-9530-4a91-98e1-ec26cf49c4ed
  Args:
    type: :Person
    source: Herzeleide_of_Prussia
  AddLiteral (9dd7e01e-ac58-4652-9ebc-f99fb7597cad)
 Call ID: 9dd7e01e-ac58-4652-9ebc-f99fb7597cad
  Args:
    relation: :hasBirthYear
    literal_value: 1918
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
  AddLiteral (ca5c5666-6b18-43bf-b18d-e4d7cd61dd1f)
 Call ID: ca5c5666-6b18-43bf-b18d-e4d7cd61dd1f
  Args:
    relation: :hasDeathYear
    literal_value: 1989
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
  AssignClass (eeddacd5-a01c-4147-8a32-b4437f2859a1)
 Call ID: eeddacd5-a01c-4147-8a32-b4437f2859a1
  Args:
    type: :Man
    source: Oskar_of_Prussia
  AssignClass (8f451907-889b-466c-87d3-737558230066)
 Call ID: 8f451907-889b-466c-87d3-737558230066
  Args:
    type: :Person
    source: Oskar_of_Prussia
  AssignClass (825d6536-8f6e-40c4-8b0d-6d320d31114c)
 Call ID: 825d6536-8f6e-40c4-8b0d-6d320d31114c
  Args:
    type: :Woman
    source: Ina_Marie_von_Bassewitz
  AssignClass (0d5e4b8d-f6ec-4f76-b881-317353bcf0a3)
 Call ID: 0d5e4b8d-f6ec-4f76-b881-317353bcf0a3
  Args:
    type: :Person
    source: Ina_Marie_von_Bassewitz
  AddTriple (0364c829-9957-47ae-9002-244f698aeacd)
 Call ID: 0364c829-9957-47ae-9002-244f698aeacd
  Args:
    target: Oskar_of_Prussia
    source: Herzeleide_of_Prussia
    relation: :hasFather
  AddTriple (0658a9d0-edc3-4add-8417-f752964da787)
 Call ID: 0658a9d0-edc3-4add-8417-f752964da787
  Args:
    relation: :hasMother
    target: Ina_Marie_von_Bassewitz
    source: Herzeleide_of_Prussia
  AssignClass (9a660236-a194-4c7a-baff-c98fb637487f)
 Call ID: 9a660236-a194-4c7a-baff-c98fb637487f
  Args:
    type: :Man
    source: Oscar_of_Prussia_brother
  AssignClass (c30056bf-f015-4991-a1e3-204201bc57f0)
 Call ID: c30056bf-f015-4991-a1e3-204201bc57f0
  Args:
    type: :Person
    source: Oscar_of_Prussia_brother
  AssignClass (f7cba99c-685c-487b-8dd9-34ba93ea1065)
 Call ID: f7cba99c-685c-487b-8dd9-34ba93ea1065
  Args:
    type: :Man
    source: Burchard_of_Prussia
  AssignClass (d7fb620c-1ad5-43cc-8261-e129392f019f)
 Call ID: d7fb620c-1ad5-43cc-8261-e129392f019f
  Args:
    type: :Person
    source: Burchard_of_Prussia
  AssignClass (43fd6049-1d70-4ee6-afbd-16a596c8524a)
 Call ID: 43fd6049-1d70-4ee6-afbd-16a596c8524a
  Args:
    type: :Man
    source: Wilhelm-Karl_of_Prussia
  AssignClass (a16b121a-be2a-48e0-8b33-871523f918f9)
 Call ID: a16b121a-be2a-48e0-8b33-871523f918f9
  Args:
    type: :Person
    source: Wilhelm-Karl_of_Prussia
  AddTriple (aee7427b-a41c-43e4-83ce-d0c7a1e788b4)
 Call ID: aee7427b-a41c-43e4-83ce-d0c7a1e788b4
  Args:
    relation: :hasBrother
    source: Herzeleide_of_Prussia
    target: Oscar_of_Prussia_brother
  AddTriple (aaa19af7-a856-4ff3-a3d8-d1819510388a)
 Call ID: aaa19af7-a856-4ff3-a3d8-d1819510388a
  Args:
    relation: :hasBrother
    source: Herzeleide_of_Prussia
    target: Burchard_of_Prussia
  AddTriple (fd719c7b-a470-490a-a9ec-69dfe291249e)
 Call ID: fd719c7b-a470-490a-a9ec-69dfe291249e
  Args:
    relation: :hasBrother
    source: Herzeleide_of_Prussia
    target: Wilhelm-Karl_of_Prussia
  AssignClass (33b7ce91-d27d-46a7-af09-074ec47ae4ea)
 Call ID: 33b7ce91-d27d-46a7-af09-074ec47ae4ea
  Args:
    type: :Man
    source: Ernst-Johann_Biron
  AssignClass (a1f82c33-451d-4cb6-9cee-713ac1236ffb)
 Call ID: a1f82c33-451d-4cb6-9cee-713ac1236ffb
  Args:
    type: :Person
    source: Ernst-Johann_Biron
  AddTriple (ce32b669-c54b-471f-baed-60d91003d8d4)
 Call ID: ce32b669-c54b-471f-baed-60d91003d8d4
  Args:
    relation: :isMotherOf
    source: Herzeleide_of_Prussia
    target: Ernst-Johann_Biron
  AssignClass (a797aea1-5e53-44a8-a4cf-e510607f8b48)
 Call ID: a797aea1-5e53-44a8-a4cf-e510607f8b48
  Args:
    type: :Man
    source: Karl_Biron_von_Courland
  AssignClass (bd22c815-4386-4df2-ab52-b2af03a43522)
 Call ID: bd22c815-4386-4df2-ab52-b2af03a43522
  Args:
    type: :Person
    source: Karl_Biron_von_Courland
  AddLiteral (78286d08-d32e-4cf7-b40a-1f879e828e4d)
 Call ID: 78286d08-d32e-4cf7-b40a-1f879e828e4d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1907
    source: Karl_Biron_von_Courland
  AddLiteral (02c28912-fe83-477c-b299-7ab528e4541c)
 Call ID: 02c28912-fe83-477c-b299-7ab528e4541c
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1982
    source: Karl_Biron_von_Courland
  AddLiteral (e292bdb5-7745-411c-87c7-4b3cb63ef139)
 Call ID: e292bdb5-7745-411c-87c7-4b3cb63ef139
  Args:
    literal_type: xsd:integer
    literal_value: 1938
    source: Herzeleide_of_Prussia
    relation: :hasMarriageYear
  AddTriple (2651668c-615a-400e-bcc0-d9dd250b716c)
 Call ID: 2651668c-615a-400e-bcc0-d9dd250b716c
  Args:
    relation: :hasRelation
    target: Karl_Biron_von_Courland
    source: Herzeleide_of_Prussia
  AssignClass (1524628e-1b94-43f7-8a97-316f88dcef3a)
 Call ID: 1524628e-1b94-43f7-8a97-316f88dcef3a
  Args:
    type: :Man
    source: Gustav_Biron_von_Courland
  AssignClass (b49e2bc2-6bc1-4dc1-b999-f5c497bb3df9)
 Call ID: b49e2bc2-6bc1-4dc1-b999-f5c497bb3df9
  Args:
    type: :Person
    source: Gustav_Biron_von_Courland
  AssignClass (5e18f979-3955-4bfe-bedb-77420627d243)
 Call ID: 5e18f979-3955-4bfe-bedb-77420627d243
  Args:
    type: :Woman
    source: Francoise_Levisse_de_Montigny
  AssignClass (c5ed1426-a62c-41fb-ac05-54000ba93f23)
 Call ID: c5ed1426-a62c-41fb-ac05-54000ba93f23
  Args:
    type: :Person
    source: Francoise_Levisse_de_Montigny
  AddTriple (8365dfcf-a5cf-483f-94ef-6528f512cc23)
 Call ID: 8365dfcf-a5cf-483f-94ef-6528f512cc23
  Args:
    relation: :hasFather
    target: Gustav_Biron_von_Courland
    source: Karl_Biron_von_Courland
  AddTriple (3de04994-1a1f-4932-9b24-b814599916f5)
 Call ID: 3de04994-1a1f-4932-9b24-b814599916f5
  Args:
    source: Karl_Biron_von_Courland
    target: Francoise_Levisse_de_Montigny
    relation: :hasMother
  Finish (032e5a70-1390-4e2a-bf28-fef30fb4a8cf)
 Call ID: 032e5a70-1390-4e2a-bf28-fef30fb4a8cf
  Args: