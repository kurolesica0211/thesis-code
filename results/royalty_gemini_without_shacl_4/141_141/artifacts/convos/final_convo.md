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
Prince Ernst August of Lippe (German: Prinz Ernst August Bernhard Alexander Eduard Friedrich Wilhelm zur Lippe; 1 April 1917 – 15 June 1990) was a claimant to the headship of the House of Lippe.
Early life

Prince Ernst August was born at Dresden, Kingdom of Saxony, the second child and first son of Prince Julius Ernst of Lippe  (1873–1952; son of Ernst, Count of Lippe-Biesterfeld and Countess Caroline von Wartensleben) and his wife, Duchess Marie of Mecklenburg-Strelitz (1878–1948; daughter of Adolphus Frederick V, Grand Duke of Mecklenburg-Strelitz and his wife Princess Elisabeth of Anhalt).
Through his father he was first cousin of Prince Bernhard, consort to Queen Juliana of the Netherlands, and was a guest at their 1937 wedding.
Marriage

Ernst August married on 3 March 1948 in Oberkassel, Bonn to Christa von Arnim (b. 2 July 1923-20 February 2020), elder daughter of Curt David von Arnim, and his wife, Stephanie von Stechow.
They had four children:


House of Lippe

On 30 December 1949 his younger half-brother Prince Armin succeeded his father Leopold IV as head of the House of Lippe.
On 22 March 1953, he renounced his position in favour of his older half brother Prince Leopold.
Prince Leopold later in 1958 renounced the headship in favour of his older brother Hereditary Prince Ernst.
Later that year the Hereditary Prince called a family council where it was agreed by the princes in attendance that the oldest prince living in Germany would be head of the house.
So the position was taken by Prince Simon Casimir (1900–1980).
Prince Ernst August changed his mind, believing all princes of the house, not just those living in Germany, should be considered.
Ernst August died in 1990 and his son Prince Friedrich Wilhelm has continued his claim.
Prince Armin, who said he did not think his decision in 1953 was irrevocable, also claimed to be head of the house until his death in 2015, with his son Stephan, Prince of Lippe continuing his claim.
Prince Ernst August grew up and lived at Lippesches Palais in Oberkassel, Bonn, which had been home to the Lippe-Biesterfeld family for the past 209 years.
In 1970 he also acquired Syburg castle at Bergen, Middle Franconia, which however he was forced to auction in 1977, followed by the sale of Lippe House in 1979.



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
  AssignClass (628c553a-15a0-419d-b4d6-d1ae64ea1c34)
 Call ID: 628c553a-15a0-419d-b4d6-d1ae64ea1c34
  Args:
    type: :Man
    source: Prince_Ernst_August_of_Lippe
  AddLiteral (b8de33a2-7814-4b59-a52c-df8ddae77ed7)
 Call ID: b8de33a2-7814-4b59-a52c-df8ddae77ed7
  Args:
    literal_value: 1917
    source: Prince_Ernst_August_of_Lippe
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4e989a18-22e8-43dc-b3fe-2be87e9724d8)
 Call ID: 4e989a18-22e8-43dc-b3fe-2be87e9724d8
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Ernst_August_of_Lippe
    literal_value: 1990
  AssignClass (09a934a3-2efa-4c10-89a7-53cd7edc5784)
 Call ID: 09a934a3-2efa-4c10-89a7-53cd7edc5784
  Args:
    type: :Man
    source: Prince_Julius_Ernst_of_Lippe
  AddLiteral (c0224168-4bf9-4d92-9778-fdcd64119666)
 Call ID: c0224168-4bf9-4d92-9778-fdcd64119666
  Args:
    literal_value: 1873
    source: Prince_Julius_Ernst_of_Lippe
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (ba3581ca-40c7-44a4-addc-1113569d4e30)
 Call ID: ba3581ca-40c7-44a4-addc-1113569d4e30
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1952
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (d69c5887-8d56-4f33-8873-a706c107380e)
 Call ID: d69c5887-8d56-4f33-8873-a706c107380e
  Args:
    type: :Woman
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AddLiteral (a4ae7e6b-07d3-477a-9038-af005583286b)
 Call ID: a4ae7e6b-07d3-477a-9038-af005583286b
  Args:
    literal_type: xsd:integer
    literal_value: 1878
    source: Duchess_Marie_of_Mecklenburg-Strelitz
    relation: :hasBirthYear
  AddLiteral (b525548f-73f1-4fea-bbf0-8620deba028a)
 Call ID: b525548f-73f1-4fea-bbf0-8620deba028a
  Args:
    source: Duchess_Marie_of_Mecklenburg-Strelitz
    literal_value: 1948
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (490f24e2-61d5-4549-9264-c2b952960c98)
 Call ID: 490f24e2-61d5-4549-9264-c2b952960c98
  Args:
    source: Prince_Ernst_August_of_Lippe
    relation: :hasFather
    target: Prince_Julius_Ernst_of_Lippe
  AddTriple (c856104a-f1ab-4c90-91b0-d57c7d45b397)
 Call ID: c856104a-f1ab-4c90-91b0-d57c7d45b397
  Args:
    target: Duchess_Marie_of_Mecklenburg-Strelitz
    relation: :hasMother
    source: Prince_Ernst_August_of_Lippe
  AssignClass (9dcf00df-af5b-41f2-9be6-d45577bee87d)
 Call ID: 9dcf00df-af5b-41f2-9be6-d45577bee87d
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (20f096a7-80f7-4672-9dd8-691c29d7d898)
 Call ID: 20f096a7-80f7-4672-9dd8-691c29d7d898
  Args:
    type: :Woman
    source: Countess_Caroline_von_Wartensleben
  AddTriple (66df6ed2-9cb5-475a-9b66-9c5331382c1a)
 Call ID: 66df6ed2-9cb5-475a-9b66-9c5331382c1a
  Args:
    target: Ernst_Count_of_Lippe-Biesterfeld
    relation: :hasFather
    source: Prince_Julius_Ernst_of_Lippe
  AddTriple (3da0cc95-6549-4486-b75d-2a049914d2b8)
 Call ID: 3da0cc95-6549-4486-b75d-2a049914d2b8
  Args:
    target: Countess_Caroline_von_Wartensleben
    relation: :hasMother
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (21998222-948b-4df8-83e6-216b918a5047)
 Call ID: 21998222-948b-4df8-83e6-216b918a5047
  Args:
    type: :Man
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (db5b2678-c7be-4ad8-b0e9-c65faa4c91b9)
 Call ID: db5b2678-c7be-4ad8-b0e9-c65faa4c91b9
  Args:
    type: :Woman
    source: Princess_Elisabeth_of_Anhalt
  AddTriple (61139e33-51cd-4897-a094-e225686c3191)
 Call ID: 61139e33-51cd-4897-a094-e225686c3191
  Args:
    source: Duchess_Marie_of_Mecklenburg-Strelitz
    relation: :hasFather
    target: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AddTriple (d3c94d9a-4599-43e8-aaa3-9ffc59401649)
 Call ID: d3c94d9a-4599-43e8-aaa3-9ffc59401649
  Args:
    relation: :hasMother
    source: Duchess_Marie_of_Mecklenburg-Strelitz
    target: Princess_Elisabeth_of_Anhalt
  AssignClass (2505bd4c-42f0-49bb-838e-12782a69726d)
 Call ID: 2505bd4c-42f0-49bb-838e-12782a69726d
  Args:
    type: :Woman
    source: Christa_von_Arnim
  AddLiteral (2191f0bc-bfe0-4c4b-a410-1885c840a746)
 Call ID: 2191f0bc-bfe0-4c4b-a410-1885c840a746
  Args:
    literal_type: xsd:integer
    literal_value: 1923
    source: Christa_von_Arnim
    relation: :hasBirthYear
  AddLiteral (953fb7ed-4df2-4c21-8a82-b2d2f7d40337)
 Call ID: 953fb7ed-4df2-4c21-8a82-b2d2f7d40337
  Args:
    literal_type: xsd:integer
    literal_value: 2020
    source: Christa_von_Arnim
    relation: :hasDeathYear
  AddTriple (d69bc8b3-4045-486f-8187-f71a3b7123b6)
 Call ID: d69bc8b3-4045-486f-8187-f71a3b7123b6
  Args:
    target: Christa_von_Arnim
    relation: :hasRelation
    source: Prince_Ernst_August_of_Lippe
  AddLiteral (f3190101-3ecb-4fe1-9c88-37eefc630a59)
 Call ID: f3190101-3ecb-4fe1-9c88-37eefc630a59
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_Ernst_August_of_Lippe
    literal_value: 1948
  AssignClass (54d9315a-88e9-48a8-af73-84bb469f7910)
 Call ID: 54d9315a-88e9-48a8-af73-84bb469f7910
  Args:
    type: :Man
    source: Curt_David_von_Arnim
  AssignClass (87af6784-c531-4d62-8ffb-b04670930703)
 Call ID: 87af6784-c531-4d62-8ffb-b04670930703
  Args:
    type: :Woman
    source: Stephanie_von_Stechow
  AddTriple (ecef8127-22b6-446d-bbf5-75690c24290c)
 Call ID: ecef8127-22b6-446d-bbf5-75690c24290c
  Args:
    target: Curt_David_von_Arnim
    source: Christa_von_Arnim
    relation: :hasFather
  AddTriple (0729ff3f-c4b0-4c91-a8e5-b43fbe0b9cf7)
 Call ID: 0729ff3f-c4b0-4c91-a8e5-b43fbe0b9cf7
  Args:
    target: Stephanie_von_Stechow
    source: Christa_von_Arnim
    relation: :hasMother
  AssignClass (0a37cf06-0e73-42fc-a46e-860bdc51e657)
 Call ID: 0a37cf06-0e73-42fc-a46e-860bdc51e657
  Args:
    type: :Man
    source: Prince_Armin
  AddTriple (d69e85bc-5934-4c4b-8fff-18bbd25ee3d7)
 Call ID: d69e85bc-5934-4c4b-8fff-18bbd25ee3d7
  Args:
    source: Prince_Ernst_August_of_Lippe
    relation: :isSiblingOf
    target: Prince_Armin
  AssignClass (b955d452-7375-43e5-b06c-126ca5f09663)
 Call ID: b955d452-7375-43e5-b06c-126ca5f09663
  Args:
    type: :Man
    source: Leopold_IV
  AddTriple (ae5f46f3-ed17-4e87-9bcc-8f408034d7a0)
 Call ID: ae5f46f3-ed17-4e87-9bcc-8f408034d7a0
  Args:
    target: Leopold_IV
    relation: :hasFather
    source: Prince_Armin
  AssignClass (fcd3b204-dfa4-4f91-aa05-a3ea1caf7fbe)
 Call ID: fcd3b204-dfa4-4f91-aa05-a3ea1caf7fbe
  Args:
    type: :Man
    source: Prince_Leopold
  AddTriple (a917f2d2-6e69-43cb-817a-b2c18eccd145)
 Call ID: a917f2d2-6e69-43cb-817a-b2c18eccd145
  Args:
    target: Prince_Leopold
    source: Prince_Ernst_August_of_Lippe
    relation: :isSiblingOf
  AssignClass (e171e59d-7503-414c-8d7e-64321d3152f5)
 Call ID: e171e59d-7503-414c-8d7e-64321d3152f5
  Args:
    type: :Man
    source: Prince_Friedrich_Wilhelm
  AddTriple (3bc1af43-b8f1-4ed2-bc7e-4a3fc3e7aa03)
 Call ID: 3bc1af43-b8f1-4ed2-bc7e-4a3fc3e7aa03
  Args:
    target: Prince_Ernst_August_of_Lippe
    source: Prince_Friedrich_Wilhelm
    relation: :isSonOf
  AssignClass (c32b4e8b-4b97-432d-b4bc-7668d1b9abba)
 Call ID: c32b4e8b-4b97-432d-b4bc-7668d1b9abba
  Args:
    type: :Man
    source: Stephan_Prince_of_Lippe
  AddTriple (331ffb05-6c94-4597-83d2-409f94a24e0e)
 Call ID: 331ffb05-6c94-4597-83d2-409f94a24e0e
  Args:
    target: Prince_Armin
    relation: :isSonOf
    source: Stephan_Prince_of_Lippe
  AssignClass (b623d438-b6b0-4916-b8cb-9c40f7cd59ea)
 Call ID: b623d438-b6b0-4916-b8cb-9c40f7cd59ea
  Args:
    type: :Man
    source: Prince_Simon_Casimir
  AddLiteral (6e4d9964-f090-4f3d-b732-3d39170bca6e)
 Call ID: 6e4d9964-f090-4f3d-b732-3d39170bca6e
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Simon_Casimir
    literal_value: 1900
  AddLiteral (0f41c4e4-385f-431e-a8c5-1069c27ade8a)
 Call ID: 0f41c4e4-385f-431e-a8c5-1069c27ade8a
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Prince_Simon_Casimir
    relation: :hasDeathYear
  Finish (4b0c044d-9020-4bb0-8e03-97e1110d23f5)
 Call ID: 4b0c044d-9020-4bb0-8e03-97e1110d23f5
  Args: