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
  AssignClass (e5132042-6475-40d5-b0f6-53793e273f78)
 Call ID: e5132042-6475-40d5-b0f6-53793e273f78
  Args:
    type: :Man
    source: Prince_Ernst_August_of_Lippe
  AssignClass (f13f7ba2-1cd9-4d36-b652-61a6fcf9fe2c)
 Call ID: f13f7ba2-1cd9-4d36-b652-61a6fcf9fe2c
  Args:
    type: :Person
    source: Prince_Ernst_August_of_Lippe
  AddLiteral (1351732b-f39f-4307-99cf-b65ec9b146e9)
 Call ID: 1351732b-f39f-4307-99cf-b65ec9b146e9
  Args:
    literal_type: xsd:integer
    literal_value: 1917
    source: Prince_Ernst_August_of_Lippe
    relation: :hasBirthYear
  AddLiteral (e69bf676-d4bb-4779-9aa3-4e72679e7b0b)
 Call ID: e69bf676-d4bb-4779-9aa3-4e72679e7b0b
  Args:
    literal_value: 1990
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Ernst_August_of_Lippe
  AssignClass (fc93ed8d-1909-4201-b88b-cf7224bead4f)
 Call ID: fc93ed8d-1909-4201-b88b-cf7224bead4f
  Args:
    type: :Ancestor
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (403bb90a-9d27-491f-935e-58a203f381b2)
 Call ID: 403bb90a-9d27-491f-935e-58a203f381b2
  Args:
    type: :Man
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (88c057e7-ab2c-4d70-9438-638716387ade)
 Call ID: 88c057e7-ab2c-4d70-9438-638716387ade
  Args:
    type: :Person
    source: Prince_Julius_Ernst_of_Lippe
  AddLiteral (e9f73905-48cd-4190-aa94-10f70fbd2243)
 Call ID: e9f73905-48cd-4190-aa94-10f70fbd2243
  Args:
    relation: :hasBirthYear
    source: Prince_Julius_Ernst_of_Lippe
    literal_value: 1873
    literal_type: xsd:integer
  AddLiteral (f4d2dc90-50bb-4836-9c3f-2c9b1917e6c9)
 Call ID: f4d2dc90-50bb-4836-9c3f-2c9b1917e6c9
  Args:
    literal_type: xsd:integer
    literal_value: 1952
    relation: :hasDeathYear
    source: Prince_Julius_Ernst_of_Lippe
  AssignClass (ef294bb7-9ffa-43cf-8a5a-0aa34678f0b4)
 Call ID: ef294bb7-9ffa-43cf-8a5a-0aa34678f0b4
  Args:
    type: :Ancestor
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AssignClass (53f784b7-c503-4576-b151-bb3942474e71)
 Call ID: 53f784b7-c503-4576-b151-bb3942474e71
  Args:
    type: :Woman
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AssignClass (85cc448b-535e-436b-8829-ef829081cf99)
 Call ID: 85cc448b-535e-436b-8829-ef829081cf99
  Args:
    type: :Person
    source: Duchess_Marie_of_Mecklenburg-Strelitz
  AddLiteral (d19bf36f-19f9-4ba4-914d-88fc1ccc0731)
 Call ID: d19bf36f-19f9-4ba4-914d-88fc1ccc0731
  Args:
    relation: :hasBirthYear
    source: Duchess_Marie_of_Mecklenburg-Strelitz
    literal_value: 1878
    literal_type: xsd:integer
  AddLiteral (30fdad3c-6bc9-4a66-8102-0686175eccef)
 Call ID: 30fdad3c-6bc9-4a66-8102-0686175eccef
  Args:
    source: Duchess_Marie_of_Mecklenburg-Strelitz
    relation: :hasDeathYear
    literal_value: 1948
    literal_type: xsd:integer
  AddTriple (f1e79478-4cee-4089-8394-cfc141fde99d)
 Call ID: f1e79478-4cee-4089-8394-cfc141fde99d
  Args:
    target: Prince_Julius_Ernst_of_Lippe
    source: Prince_Ernst_August_of_Lippe
    relation: :hasFather
  AddTriple (1812085e-f81f-4c72-b2ab-9da2e89e3361)
 Call ID: 1812085e-f81f-4c72-b2ab-9da2e89e3361
  Args:
    relation: :hasMother
    source: Prince_Ernst_August_of_Lippe
    target: Duchess_Marie_of_Mecklenburg-Strelitz
  AssignClass (8e5f0724-bd77-4c5f-a137-4ab554afdb82)
 Call ID: 8e5f0724-bd77-4c5f-a137-4ab554afdb82
  Args:
    type: :Ancestor
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (d882f5d7-bde6-47b8-98f2-e54e4ec4b045)
 Call ID: d882f5d7-bde6-47b8-98f2-e54e4ec4b045
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (0922e755-eb84-47e3-84a5-d351c46487d9)
 Call ID: 0922e755-eb84-47e3-84a5-d351c46487d9
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (89f00cb7-6df0-4427-84fe-b93ce3a2a13f)
 Call ID: 89f00cb7-6df0-4427-84fe-b93ce3a2a13f
  Args:
    relation: :isFatherOf
    source: Ernst_Count_of_Lippe-Biesterfeld
    target: Prince_Julius_Ernst_of_Lippe
  AssignClass (7186ffa8-1bbd-45a1-abb4-717218582009)
 Call ID: 7186ffa8-1bbd-45a1-abb4-717218582009
  Args:
    type: :Ancestor
    source: Countess_Caroline_von_Wartensleben
  AssignClass (c5d27a72-ca7b-4415-9f4a-195cc94e7fc9)
 Call ID: c5d27a72-ca7b-4415-9f4a-195cc94e7fc9
  Args:
    type: :Woman
    source: Countess_Caroline_von_Wartensleben
  AssignClass (c7613b5c-f44c-443c-93c5-a5e625b9dd28)
 Call ID: c7613b5c-f44c-443c-93c5-a5e625b9dd28
  Args:
    type: :Person
    source: Countess_Caroline_von_Wartensleben
  AddTriple (cc9d12e0-8a81-48c2-82e4-c31e2fd43623)
 Call ID: cc9d12e0-8a81-48c2-82e4-c31e2fd43623
  Args:
    source: Countess_Caroline_von_Wartensleben
    target: Prince_Julius_Ernst_of_Lippe
    relation: :isMotherOf
  AssignClass (99a2dca4-66a7-4dae-bc51-0ab5625aebf7)
 Call ID: 99a2dca4-66a7-4dae-bc51-0ab5625aebf7
  Args:
    type: :Ancestor
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (99894948-b81e-4c78-8825-d8cd130e9f0b)
 Call ID: 99894948-b81e-4c78-8825-d8cd130e9f0b
  Args:
    type: :Man
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AssignClass (ca32f92e-454b-4fcc-af3b-77d5efd49936)
 Call ID: ca32f92e-454b-4fcc-af3b-77d5efd49936
  Args:
    type: :Person
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
  AddTriple (bb69c103-0b24-4cba-8bfc-094d84a39f76)
 Call ID: bb69c103-0b24-4cba-8bfc-094d84a39f76
  Args:
    source: Adolphus_Frederick_V_Grand_Duke_of_Mecklenburg-Strelitz
    target: Duchess_Marie_of_Mecklenburg-Strelitz
    relation: :isFatherOf
  AssignClass (20e2a76f-2f15-4a18-930c-b71e73d622e4)
 Call ID: 20e2a76f-2f15-4a18-930c-b71e73d622e4
  Args:
    type: :Ancestor
    source: Princess_Elisabeth_of_Anhalt
  AssignClass (fbfbe615-653e-4589-b727-946cfd45ac5d)
 Call ID: fbfbe615-653e-4589-b727-946cfd45ac5d
  Args:
    type: :Woman
    source: Princess_Elisabeth_of_Anhalt
  AssignClass (7cae65b6-7490-4cc6-8126-d99c3c4a54a3)
 Call ID: 7cae65b6-7490-4cc6-8126-d99c3c4a54a3
  Args:
    type: :Person
    source: Princess_Elisabeth_of_Anhalt
  AddTriple (cfb5152c-9acc-4327-aa79-22bba8b94c94)
 Call ID: cfb5152c-9acc-4327-aa79-22bba8b94c94
  Args:
    source: Princess_Elisabeth_of_Anhalt
    target: Duchess_Marie_of_Mecklenburg-Strelitz
    relation: :isMotherOf
  AssignClass (560f9346-d752-4d20-b14d-eb152160dd07)
 Call ID: 560f9346-d752-4d20-b14d-eb152160dd07
  Args:
    type: :Woman
    source: Christa_von_Arnim
  AssignClass (eafa7d42-3644-414b-b432-c987c88a9ed9)
 Call ID: eafa7d42-3644-414b-b432-c987c88a9ed9
  Args:
    type: :Person
    source: Christa_von_Arnim
  AddLiteral (6fdd391e-355a-492f-a9a4-fa989d76729b)
 Call ID: 6fdd391e-355a-492f-a9a4-fa989d76729b
  Args:
    literal_value: 1948
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Prince_Ernst_August_of_Lippe
  AddTriple (b5089f08-8d0a-40bd-853f-0ffc98812af6)
 Call ID: b5089f08-8d0a-40bd-853f-0ffc98812af6
  Args:
    relation: :hasRelation
    target: Christa_von_Arnim
    source: Prince_Ernst_August_of_Lippe
  AssignClass (ce0955d2-7041-43fe-8c27-89e0a6e91021)
 Call ID: ce0955d2-7041-43fe-8c27-89e0a6e91021
  Args:
    type: :Ancestor
    source: Curt_David_von_Arnim
  AssignClass (1be3618e-2192-453e-a591-331b39bc0d5a)
 Call ID: 1be3618e-2192-453e-a591-331b39bc0d5a
  Args:
    type: :Man
    source: Curt_David_von_Arnim
  AssignClass (30f5f2e5-6038-483c-9883-374d5bffdc3f)
 Call ID: 30f5f2e5-6038-483c-9883-374d5bffdc3f
  Args:
    type: :Person
    source: Curt_David_von_Arnim
  AddTriple (7ec20e77-d2ca-4444-b3f1-a1ae5ca8906a)
 Call ID: 7ec20e77-d2ca-4444-b3f1-a1ae5ca8906a
  Args:
    target: Christa_von_Arnim
    source: Curt_David_von_Arnim
    relation: :isFatherOf
  AssignClass (044dd12a-2a28-4a66-abae-4012ebeb6ed8)
 Call ID: 044dd12a-2a28-4a66-abae-4012ebeb6ed8
  Args:
    type: :Ancestor
    source: Stephanie_von_Stechow
  AssignClass (da602054-d223-47eb-873f-0ae7b83ce072)
 Call ID: da602054-d223-47eb-873f-0ae7b83ce072
  Args:
    type: :Woman
    source: Stephanie_von_Stechow
  AssignClass (269ac4d8-2917-4ef0-94b3-74dcc503c5d2)
 Call ID: 269ac4d8-2917-4ef0-94b3-74dcc503c5d2
  Args:
    type: :Person
    source: Stephanie_von_Stechow
  AddTriple (88cd203a-91b1-4f1c-b135-b8f36267b672)
 Call ID: 88cd203a-91b1-4f1c-b135-b8f36267b672
  Args:
    relation: :isMotherOf
    target: Christa_von_Arnim
    source: Stephanie_von_Stechow
  AssignClass (d4ee82a5-7a5e-480a-84d3-a2c1e4c03668)
 Call ID: d4ee82a5-7a5e-480a-84d3-a2c1e4c03668
  Args:
    type: :Man
    source: Prince_Armin
  AssignClass (53a8ef55-ad26-4829-b95f-e9ca1dc229e8)
 Call ID: 53a8ef55-ad26-4829-b95f-e9ca1dc229e8
  Args:
    type: :Person
    source: Prince_Armin
  AssignClass (4b326e17-a798-43c3-8c0e-e869c6ed03a5)
 Call ID: 4b326e17-a798-43c3-8c0e-e869c6ed03a5
  Args:
    type: :Man
    source: Prince_Leopold
  AssignClass (63ceddf1-7e20-4318-9c97-6f49e369d4e8)
 Call ID: 63ceddf1-7e20-4318-9c97-6f49e369d4e8
  Args:
    type: :Person
    source: Prince_Leopold
  AssignClass (fb051998-4f28-4129-b38a-dd2ba7a312b8)
 Call ID: fb051998-4f28-4129-b38a-dd2ba7a312b8
  Args:
    type: :Man
    source: Prince_Simon_Casimir
  AssignClass (95d73bb7-5be1-4c31-b89f-a2a93d88afc2)
 Call ID: 95d73bb7-5be1-4c31-b89f-a2a93d88afc2
  Args:
    type: :Person
    source: Prince_Simon_Casimir
  AssignClass (335add86-88b3-470c-b55b-f498ebb2c661)
 Call ID: 335add86-88b3-470c-b55b-f498ebb2c661
  Args:
    type: :Man
    source: Prince_Friedrich_Wilhelm
  AssignClass (b224fff5-3465-41eb-b478-fa09f5261b58)
 Call ID: b224fff5-3465-41eb-b478-fa09f5261b58
  Args:
    type: :Person
    source: Prince_Friedrich_Wilhelm
  AddTriple (82dd5034-9013-4430-b825-89e1770235d0)
 Call ID: 82dd5034-9013-4430-b825-89e1770235d0
  Args:
    target: Prince_Ernst_August_of_Lippe
    source: Prince_Friedrich_Wilhelm
    relation: :isSonOf
  AssignClass (a77c3961-a416-4a26-86be-41ddd41ca2e4)
 Call ID: a77c3961-a416-4a26-86be-41ddd41ca2e4
  Args:
    type: :Man
    source: Stephan_Prince_of_Lippe
  AssignClass (5cc2ef33-156f-46da-a807-82ac0e3e1743)
 Call ID: 5cc2ef33-156f-46da-a807-82ac0e3e1743
  Args:
    type: :Person
    source: Stephan_Prince_of_Lippe
  AddTriple (947c4b90-f5f4-450e-8664-349d21b5d932)
 Call ID: 947c4b90-f5f4-450e-8664-349d21b5d932
  Args:
    relation: :isSonOf
    target: Prince_Armin
    source: Stephan_Prince_of_Lippe
  Finish (1b3892c8-c4d3-4b19-b134-d1046eb4c8fe)
 Call ID: 1b3892c8-c4d3-4b19-b134-d1046eb4c8fe
  Args: