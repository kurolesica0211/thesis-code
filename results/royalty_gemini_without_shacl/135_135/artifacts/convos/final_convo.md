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
  AssignClass (e707f929-522f-4a81-a1f8-4f82559eaef7)
 Call ID: e707f929-522f-4a81-a1f8-4f82559eaef7
  Args:
    type: :Woman
    source: Herzeleide_of_Prussia
  AssignClass (41118333-9582-43b3-8a0c-01d10bb51130)
 Call ID: 41118333-9582-43b3-8a0c-01d10bb51130
  Args:
    source: Herzeleide_of_Prussia
    type: :Person
  AddLiteral (9085ada0-3a29-4dc6-92f9-5e9e4a71453c)
 Call ID: 9085ada0-3a29-4dc6-92f9-5e9e4a71453c
  Args:
    literal_value: 1918
    relation: :hasBirthYear
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
  AddLiteral (9fe22018-dc79-4d18-9d2a-3bbea2bade94)
 Call ID: 9fe22018-dc79-4d18-9d2a-3bbea2bade94
  Args:
    relation: :hasDeathYear
    literal_value: 1989
    source: Herzeleide_of_Prussia
    literal_type: xsd:integer
  AssignClass (2c6933a0-c902-4b64-9676-8f0df4f7f7c8)
 Call ID: 2c6933a0-c902-4b64-9676-8f0df4f7f7c8
  Args:
    type: :Man
    source: Oskar_of_Prussia
  AssignClass (93297c98-790b-4e52-8e03-8d3ad7aa90ea)
 Call ID: 93297c98-790b-4e52-8e03-8d3ad7aa90ea
  Args:
    type: :Person
    source: Oskar_of_Prussia
  AssignClass (27276c7f-ae92-4957-ba66-e0b7f975c75f)
 Call ID: 27276c7f-ae92-4957-ba66-e0b7f975c75f
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Woman
  AssignClass (ab81c6cc-33f5-4b23-8a41-134269fb79ee)
 Call ID: ab81c6cc-33f5-4b23-8a41-134269fb79ee
  Args:
    type: :Person
    source: Ina_Marie_von_Bassewitz
  AddTriple (815322ee-82d7-431a-9b58-1ba67d92f126)
 Call ID: 815322ee-82d7-431a-9b58-1ba67d92f126
  Args:
    relation: :hasFather
    target: Oskar_of_Prussia
    source: Herzeleide_of_Prussia
  AddTriple (0f5cd0c0-ff66-4405-bd10-e37f380b718f)
 Call ID: 0f5cd0c0-ff66-4405-bd10-e37f380b718f
  Args:
    source: Herzeleide_of_Prussia
    target: Ina_Marie_von_Bassewitz
    relation: :hasMother
  AssignClass (0297c68b-dd45-4790-9e94-e6cba13edb0c)
 Call ID: 0297c68b-dd45-4790-9e94-e6cba13edb0c
  Args:
    source: Ernst-Johann_Biron
    type: :Man
  AssignClass (e7cc27aa-aabf-4c78-b1e1-19ea9535d395)
 Call ID: e7cc27aa-aabf-4c78-b1e1-19ea9535d395
  Args:
    type: :Person
    source: Ernst-Johann_Biron
  AddTriple (b681562a-2bc1-4998-8ca4-991cb5e99117)
 Call ID: b681562a-2bc1-4998-8ca4-991cb5e99117
  Args:
    relation: :hasMother
    target: Herzeleide_of_Prussia
    source: Ernst-Johann_Biron
  AssignClass (9929c4f6-10aa-4492-9a5b-08a24a1de83a)
 Call ID: 9929c4f6-10aa-4492-9a5b-08a24a1de83a
  Args:
    type: :Man
    source: Oscar_brother
  AssignClass (9f5def7f-8fed-41f9-b759-5f842bc0d003)
 Call ID: 9f5def7f-8fed-41f9-b759-5f842bc0d003
  Args:
    source: Oscar_brother
    type: :Person
  AssignClass (74a5db1b-a24f-4ad8-a3bd-823769a96cc8)
 Call ID: 74a5db1b-a24f-4ad8-a3bd-823769a96cc8
  Args:
    type: :Man
    source: Burchard_brother
  AssignClass (2a0c546d-5d03-4164-91be-0ce2d39c46cb)
 Call ID: 2a0c546d-5d03-4164-91be-0ce2d39c46cb
  Args:
    type: :Person
    source: Burchard_brother
  AssignClass (ade783a1-2339-4d65-af50-b4697fe36532)
 Call ID: ade783a1-2339-4d65-af50-b4697fe36532
  Args:
    source: Wilhelm-Karl_brother
    type: :Man
  AssignClass (ceeabf4a-1db1-437c-b22d-c46ce11c41f4)
 Call ID: ceeabf4a-1db1-437c-b22d-c46ce11c41f4
  Args:
    source: Wilhelm-Karl_brother
    type: :Person
  AddTriple (f9584984-86c0-47ee-b883-39f8dc40e5bc)
 Call ID: f9584984-86c0-47ee-b883-39f8dc40e5bc
  Args:
    relation: :hasBrother
    target: Oscar_brother
    source: Herzeleide_of_Prussia
  AddTriple (0ca4db38-13c6-4ae4-8d10-9d77d0451042)
 Call ID: 0ca4db38-13c6-4ae4-8d10-9d77d0451042
  Args:
    target: Burchard_brother
    source: Herzeleide_of_Prussia
    relation: :hasBrother
  AddTriple (b3bef754-f646-49c5-a994-00bf4dc17b75)
 Call ID: b3bef754-f646-49c5-a994-00bf4dc17b75
  Args:
    relation: :hasBrother
    source: Herzeleide_of_Prussia
    target: Wilhelm-Karl_brother
  AssignClass (3711b99d-f23a-40b1-8495-44bb66d2803e)
 Call ID: 3711b99d-f23a-40b1-8495-44bb66d2803e
  Args:
    source: Karl_Biron_von_Courland
    type: :Man
  AssignClass (c4bc2d4e-91bf-4bb2-b86e-d327074f596e)
 Call ID: c4bc2d4e-91bf-4bb2-b86e-d327074f596e
  Args:
    source: Karl_Biron_von_Courland
    type: :Person
  AddLiteral (d7652aa3-1207-4f45-8f03-20c8b5b62832)
 Call ID: d7652aa3-1207-4f45-8f03-20c8b5b62832
  Args:
    literal_type: xsd:integer
    source: Herzeleide_of_Prussia
    literal_value: 1938
    relation: :hasMarriageYear
  AddTriple (94590f91-995f-42ec-a232-451ebdce57b4)
 Call ID: 94590f91-995f-42ec-a232-451ebdce57b4
  Args:
    relation: :hasRelation
    source: Herzeleide_of_Prussia
    target: Karl_Biron_von_Courland
  AssignClass (53390fab-079e-4dfd-a5a3-6d6c22aac2b5)
 Call ID: 53390fab-079e-4dfd-a5a3-6d6c22aac2b5
  Args:
    type: :Man
    source: Gustav_Biron_of_Courland
  AssignClass (a59e903b-cdaf-48c0-8d8d-7af983a7c46e)
 Call ID: a59e903b-cdaf-48c0-8d8d-7af983a7c46e
  Args:
    type: :Person
    source: Gustav_Biron_of_Courland
  AssignClass (e7ca0f8e-1188-4ea2-a52c-be3a4f04ee4d)
 Call ID: e7ca0f8e-1188-4ea2-a52c-be3a4f04ee4d
  Args:
    source: Francoise_Levisse_de_Montigny
    type: :Woman
  AssignClass (b6c07c55-40f9-4e2a-9929-743b76ed7beb)
 Call ID: b6c07c55-40f9-4e2a-9929-743b76ed7beb
  Args:
    source: Francoise_Levisse_de_Montigny
    type: :Person
  AddTriple (442e5731-8a5f-4a9c-92e2-1bd089ddd4a6)
 Call ID: 442e5731-8a5f-4a9c-92e2-1bd089ddd4a6
  Args:
    source: Karl_Biron_von_Courland
    target: Gustav_Biron_of_Courland
    relation: :hasFather
  AddTriple (128719f2-1460-462f-aef3-bfe1217bc894)
 Call ID: 128719f2-1460-462f-aef3-bfe1217bc894
  Args:
    source: Karl_Biron_von_Courland
    target: Francoise_Levisse_de_Montigny
    relation: :hasMother
  Finish (311aff57-f51f-483f-9670-d0d460d0ce3d)
 Call ID: 311aff57-f51f-483f-9670-d0d460d0ce3d
  Args: