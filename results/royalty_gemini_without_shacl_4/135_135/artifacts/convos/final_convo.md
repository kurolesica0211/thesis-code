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
  AssignClass (c6c5b2ec-d40c-4caa-8270-ebf184ec4426)
 Call ID: c6c5b2ec-d40c-4caa-8270-ebf184ec4426
  Args:
    source: :Herzeleide_of_Prussia
    type: :Woman
  AssignClass (cd8c7d0b-d75f-468a-bfe3-444f64053ca5)
 Call ID: cd8c7d0b-d75f-468a-bfe3-444f64053ca5
  Args:
    type: :Person
    source: :Herzeleide_of_Prussia
  AddLiteral (6faecbab-c1c0-425c-9495-232270651a03)
 Call ID: 6faecbab-c1c0-425c-9495-232270651a03
  Args:
    literal_type: xsd:integer
    literal_value: 1918
    source: :Herzeleide_of_Prussia
    relation: :hasBirthYear
  AddLiteral (69d47ab4-dfbc-4c1e-9ea2-5f3230fe92b7)
 Call ID: 69d47ab4-dfbc-4c1e-9ea2-5f3230fe92b7
  Args:
    literal_type: xsd:integer
    literal_value: 1989
    source: :Herzeleide_of_Prussia
    relation: :hasDeathYear
  AssignClass (e98f768b-5a3d-458f-b9cf-fa6671f55e1c)
 Call ID: e98f768b-5a3d-458f-b9cf-fa6671f55e1c
  Args:
    type: :Man
    source: :Oskar_of_Prussia
  AssignClass (890a9990-7878-4232-9c4a-b715f510e907)
 Call ID: 890a9990-7878-4232-9c4a-b715f510e907
  Args:
    source: :Oskar_of_Prussia
    type: :Person
  AssignClass (8a99b489-59e1-4d91-847b-b11e6602d8f3)
 Call ID: 8a99b489-59e1-4d91-847b-b11e6602d8f3
  Args:
    type: :Woman
    source: :Ina_Marie_von_Bassewitz
  AssignClass (e6adb096-e6d7-49f1-ac6c-7592ee4b9c2a)
 Call ID: e6adb096-e6d7-49f1-ac6c-7592ee4b9c2a
  Args:
    type: :Person
    source: :Ina_Marie_von_Bassewitz
  AddTriple (e0465b14-6560-40b7-9cdb-980dd8a5fc30)
 Call ID: e0465b14-6560-40b7-9cdb-980dd8a5fc30
  Args:
    target: :Oskar_of_Prussia
    relation: :hasFather
    source: :Herzeleide_of_Prussia
  AddTriple (c07744c8-659f-44e7-a788-98ea620c4410)
 Call ID: c07744c8-659f-44e7-a788-98ea620c4410
  Args:
    target: :Ina_Marie_von_Bassewitz
    relation: :hasMother
    source: :Herzeleide_of_Prussia
  AssignClass (b4f96c3a-14d5-43b4-9929-cdbf650a5818)
 Call ID: b4f96c3a-14d5-43b4-9929-cdbf650a5818
  Args:
    source: :Wilhelm_II
    type: :Man
  AssignClass (cf9326d8-73c3-46f7-b784-4c40315949db)
 Call ID: cf9326d8-73c3-46f7-b784-4c40315949db
  Args:
    type: :Person
    source: :Wilhelm_II
  AddTriple (0185aaed-62ab-41a8-86f5-0c397196b590)
 Call ID: 0185aaed-62ab-41a8-86f5-0c397196b590
  Args:
    target: :Wilhelm_II
    source: :Oskar_of_Prussia
    relation: :hasFather
  AssignClass (f1ea44b8-a91e-4386-815c-c48fd3aad85f)
 Call ID: f1ea44b8-a91e-4386-815c-c48fd3aad85f
  Args:
    type: :Man
    source: :Ernst-Johann_Biron
  AssignClass (50f95fa7-7467-4b15-960f-5e5df1e4476e)
 Call ID: 50f95fa7-7467-4b15-960f-5e5df1e4476e
  Args:
    type: :Person
    source: :Ernst-Johann_Biron
  AddTriple (c0e97dc2-1760-40fd-bbaa-d6a976eaa169)
 Call ID: c0e97dc2-1760-40fd-bbaa-d6a976eaa169
  Args:
    target: :Herzeleide_of_Prussia
    relation: :hasMother
    source: :Ernst-Johann_Biron
  AssignClass (727270b9-581f-45a1-8828-bd3284045026)
 Call ID: 727270b9-581f-45a1-8828-bd3284045026
  Args:
    type: :Man
    source: :Oscar_of_Prussia_brother
  AssignClass (c5ac6aaf-9aa7-44cf-835b-a798e174e08b)
 Call ID: c5ac6aaf-9aa7-44cf-835b-a798e174e08b
  Args:
    source: :Oscar_of_Prussia_brother
    type: :Person
  AssignClass (4459db99-4081-4c66-b9a4-d2cbeffce008)
 Call ID: 4459db99-4081-4c66-b9a4-d2cbeffce008
  Args:
    type: :Man
    source: :Burchard_of_Prussia
  AssignClass (b02aa6f0-2262-42a0-8848-6bd90ba1b49a)
 Call ID: b02aa6f0-2262-42a0-8848-6bd90ba1b49a
  Args:
    type: :Person
    source: :Burchard_of_Prussia
  AssignClass (500f0b3b-5b53-4e68-b3e5-91f19f6f4649)
 Call ID: 500f0b3b-5b53-4e68-b3e5-91f19f6f4649
  Args:
    source: :Wilhelm-Karl_of_Prussia
    type: :Man
  AssignClass (5eb2dec0-1225-47dc-9be5-8088667983d7)
 Call ID: 5eb2dec0-1225-47dc-9be5-8088667983d7
  Args:
    type: :Person
    source: :Wilhelm-Karl_of_Prussia
  AddTriple (5a2bb67e-331f-43b0-bf30-9926c81b277e)
 Call ID: 5a2bb67e-331f-43b0-bf30-9926c81b277e
  Args:
    relation: :isSiblingOf
    source: :Herzeleide_of_Prussia
    target: :Oscar_of_Prussia_brother
  AddTriple (8116570b-e189-4d34-a7af-6417b19a5eda)
 Call ID: 8116570b-e189-4d34-a7af-6417b19a5eda
  Args:
    target: :Burchard_of_Prussia
    relation: :isSiblingOf
    source: :Herzeleide_of_Prussia
  AddTriple (2714ab0d-97f1-434e-8284-c1248a44ea65)
 Call ID: 2714ab0d-97f1-434e-8284-c1248a44ea65
  Args:
    source: :Herzeleide_of_Prussia
    relation: :isSiblingOf
    target: :Wilhelm-Karl_of_Prussia
  AssignClass (176c1246-0d07-40c0-b70b-a69ba51f55b7)
 Call ID: 176c1246-0d07-40c0-b70b-a69ba51f55b7
  Args:
    source: :Karl_Biron_von_Courland
    type: :Man
  AssignClass (370851d1-8bcc-4ef7-beee-e862cf8254bf)
 Call ID: 370851d1-8bcc-4ef7-beee-e862cf8254bf
  Args:
    source: :Karl_Biron_von_Courland
    type: :Person
  AddLiteral (32ce9876-8ac3-477a-937a-cf1588851175)
 Call ID: 32ce9876-8ac3-477a-937a-cf1588851175
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Herzeleide_of_Prussia
    literal_value: 1938
  AddTriple (9094b958-81b2-4fe0-b6de-a20e7fa256cf)
 Call ID: 9094b958-81b2-4fe0-b6de-a20e7fa256cf
  Args:
    source: :Herzeleide_of_Prussia
    relation: :hasRelation
    target: :Karl_Biron_von_Courland
  AddLiteral (0b213668-a04e-45a8-91c3-8faf941ef08a)
 Call ID: 0b213668-a04e-45a8-91c3-8faf941ef08a
  Args:
    source: :Karl_Biron_von_Courland
    literal_value: 1907
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0c9b2470-1084-4ede-b60a-2d768a0de8c9)
 Call ID: 0c9b2470-1084-4ede-b60a-2d768a0de8c9
  Args:
    source: :Karl_Biron_von_Courland
    literal_value: 1982
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (7b3876a6-bd18-4c4d-94a6-b10ae9edd84c)
 Call ID: 7b3876a6-bd18-4c4d-94a6-b10ae9edd84c
  Args:
    type: :Man
    source: :Gustav_Biron_of_Courland
  AssignClass (1932c527-1f0d-445c-9c85-6269af2f92b5)
 Call ID: 1932c527-1f0d-445c-9c85-6269af2f92b5
  Args:
    type: :Person
    source: :Gustav_Biron_of_Courland
  AssignClass (0b833ad2-9166-43fb-b50b-f2c113331394)
 Call ID: 0b833ad2-9166-43fb-b50b-f2c113331394
  Args:
    source: :Francoise_Levisse_de_Montigny
    type: :Woman
  AssignClass (521d4fca-6478-4195-ac82-8b3ec65af1ef)
 Call ID: 521d4fca-6478-4195-ac82-8b3ec65af1ef
  Args:
    source: :Francoise_Levisse_de_Montigny
    type: :Person
  AddTriple (3f3ea7e2-066f-4b93-8b1e-22ccedfbac7d)
 Call ID: 3f3ea7e2-066f-4b93-8b1e-22ccedfbac7d
  Args:
    relation: :hasFather
    source: :Karl_Biron_von_Courland
    target: :Gustav_Biron_of_Courland
  AddTriple (7087b131-d2bf-41a6-b260-26e0652143dd)
 Call ID: 7087b131-d2bf-41a6-b260-26e0652143dd
  Args:
    target: :Francoise_Levisse_de_Montigny
    source: :Karl_Biron_von_Courland
    relation: :hasMother
  Finish (cba1c31e-5991-4c35-9568-614f68bb07c3)
 Call ID: cba1c31e-5991-4c35-9568-614f68bb07c3
  Args: