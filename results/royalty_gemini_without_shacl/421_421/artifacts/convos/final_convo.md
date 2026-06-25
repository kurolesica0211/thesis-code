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
Friedrich Wilhelm of Lippe (German: Friedrich Wilhelm Ernst Viktor Alexander Prinz zur Lippe; born 7 September 1947) is a claimant to the headship of the House of Lippe.
Early life

Friedrich Wilhelm was born out of wedlock at Neuwied, West Germany, the first child of Prince Ernst August of Lippe (1917–1990; son of Prince Julius Ernst of Lippe and Duchess Marie of Mecklenburg-Strelitz) and his wife, Christa von Arnim (b. 1923; daughter of Curt David von Arnim and his wife, Stephanie von Stechow).
Marriage

Friedrich Wilhelm married on 18 September 1991 in Munich to Andrea Messner (b. 1966), daughter of Günther Messner, and his wife, Lieselotte Trzoska.
House of Lippe

On 30 December 1949 his father's first cousin Prince Armin succeeded his father, Leopold IV as head of the House of Lippe.
On 22 March 1953, he renounced his position in favour of his older half-brother, Prince Leopold.
Prince Leopold later in 1958 renounced the headship in favour of his older brother, Hereditary Prince Ernst.
Later in that year the Hereditary Prince called a family council where it was agreed by the princes in attendance that the oldest prince living in Germany would be head of the house.
Therefore, the position went to Prince Simon Casimir (1900–1980).
His father died in 1990 and Friedrich Wilhelm continued the claim, despite his illegitimate birth.
Prince Armin, who has said he did not think his decision in 1953 was irrevocable, also claimed to be head of the house until his death in 2015, with his son Stephan, Prince of Lippe continuing his claim.



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
  AssignClass (9d1735e5-6a44-4c6c-9628-0ffc2efc6175)
 Call ID: 9d1735e5-6a44-4c6c-9628-0ffc2efc6175
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Lippe
  AddLiteral (cef3009a-5a18-4fd1-9a00-36c9d4f15931)
 Call ID: cef3009a-5a18-4fd1-9a00-36c9d4f15931
  Args:
    source: Friedrich_Wilhelm_of_Lippe
    literal_type: xsd:integer
    literal_value: 1947
    relation: :hasBirthYear
  AssignClass (1bedecaa-dbde-4f68-b67b-0e05623088b1)
 Call ID: 1bedecaa-dbde-4f68-b67b-0e05623088b1
  Args:
    source: Ernst_August_of_Lippe
    type: :Man
  AddLiteral (24f650fa-1ed3-4265-9e54-e202eb356b98)
 Call ID: 24f650fa-1ed3-4265-9e54-e202eb356b98
  Args:
    source: Ernst_August_of_Lippe
    relation: :hasBirthYear
    literal_value: 1917
    literal_type: xsd:integer
  AddLiteral (becbbe62-656f-4503-81d6-8b6fe37f23c7)
 Call ID: becbbe62-656f-4503-81d6-8b6fe37f23c7
  Args:
    literal_value: 1990
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Ernst_August_of_Lippe
  AssignClass (67466e92-2614-4b0b-9f40-a518c6f4fe96)
 Call ID: 67466e92-2614-4b0b-9f40-a518c6f4fe96
  Args:
    type: :Woman
    source: Christa_von_Arnim
  AddLiteral (b9165776-5512-46fa-bd17-0b960bcc0c63)
 Call ID: b9165776-5512-46fa-bd17-0b960bcc0c63
  Args:
    literal_value: 1923
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Christa_von_Arnim
  AddTriple (fd35cb5b-24be-419f-95a9-78954f7022c1)
 Call ID: fd35cb5b-24be-419f-95a9-78954f7022c1
  Args:
    source: Friedrich_Wilhelm_of_Lippe
    target: Ernst_August_of_Lippe
    relation: :hasFather
  AddTriple (5949fef8-7c34-47c1-b388-f931d6b4cf03)
 Call ID: 5949fef8-7c34-47c1-b388-f931d6b4cf03
  Args:
    target: Christa_von_Arnim
    relation: :hasMother
    source: Friedrich_Wilhelm_of_Lippe
  AssignClass (1902a7fc-7a80-444e-8e96-2daaf7a9b4cc)
 Call ID: 1902a7fc-7a80-444e-8e96-2daaf7a9b4cc
  Args:
    type: :Man
    source: Julius_Ernst_of_Lippe
  AssignClass (ad5665f5-c7f0-4a2e-8ce1-bf520e0b2364)
 Call ID: ad5665f5-c7f0-4a2e-8ce1-bf520e0b2364
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg_Strelitz
  AddTriple (6ef9e763-c151-4541-b756-980f7e6fb51b)
 Call ID: 6ef9e763-c151-4541-b756-980f7e6fb51b
  Args:
    source: Ernst_August_of_Lippe
    target: Julius_Ernst_of_Lippe
    relation: :hasFather
  AddTriple (744717ac-fe4d-4282-9a58-bdce2be34046)
 Call ID: 744717ac-fe4d-4282-9a58-bdce2be34046
  Args:
    source: Ernst_August_of_Lippe
    relation: :hasMother
    target: Marie_of_Mecklenburg_Strelitz
  AssignClass (82ffc35b-0aee-47bb-8075-2442ac347224)
 Call ID: 82ffc35b-0aee-47bb-8075-2442ac347224
  Args:
    type: :Man
    source: Curt_David_von_Arnim
  AssignClass (97862b30-49cd-4ba4-9a64-5eda8efd3b3b)
 Call ID: 97862b30-49cd-4ba4-9a64-5eda8efd3b3b
  Args:
    type: :Woman
    source: Stephanie_von_Stechow
  AddTriple (8a42562d-4fe2-4ba7-8f5a-ec6ea261acea)
 Call ID: 8a42562d-4fe2-4ba7-8f5a-ec6ea261acea
  Args:
    source: Christa_von_Arnim
    target: Curt_David_von_Arnim
    relation: :hasFather
  AddTriple (c24b232e-7ed4-4ea7-8812-b1310c7cbe98)
 Call ID: c24b232e-7ed4-4ea7-8812-b1310c7cbe98
  Args:
    relation: :hasMother
    target: Stephanie_von_Stechow
    source: Christa_von_Arnim
  AssignClass (2a40b9ff-6deb-44e7-9d95-ce8bd72c8433)
 Call ID: 2a40b9ff-6deb-44e7-9d95-ce8bd72c8433
  Args:
    source: Andrea_Messner
    type: :Woman
  AddLiteral (55c8b29f-682f-4a50-bd64-5725e52e178f)
 Call ID: 55c8b29f-682f-4a50-bd64-5725e52e178f
  Args:
    source: Andrea_Messner
    relation: :hasBirthYear
    literal_value: 1966
    literal_type: xsd:integer
  AddTriple (5176841a-2ff1-420d-9c62-ddd53e1022c8)
 Call ID: 5176841a-2ff1-420d-9c62-ddd53e1022c8
  Args:
    source: Friedrich_Wilhelm_of_Lippe
    relation: :hasRelation
    target: Andrea_Messner
  AddLiteral (3c16f1be-cf58-4cb1-8676-e63b0e2a99be)
 Call ID: 3c16f1be-cf58-4cb1-8676-e63b0e2a99be
  Args:
    source: Friedrich_Wilhelm_of_Lippe
    relation: :hasMarriageYear
    literal_value: 1991
    literal_type: xsd:integer
  AssignClass (c8fefabd-757a-4d96-8a88-709d989d78a8)
 Call ID: c8fefabd-757a-4d96-8a88-709d989d78a8
  Args:
    source: Günther_Messner
    type: :Man
  AssignClass (9f42be6d-a75f-4f8c-9f35-667adaa49e40)
 Call ID: 9f42be6d-a75f-4f8c-9f35-667adaa49e40
  Args:
    source: Lieselotte_Trzoska
    type: :Woman
  AddTriple (02fabff3-4925-42f0-a08c-f8794c39a24d)
 Call ID: 02fabff3-4925-42f0-a08c-f8794c39a24d
  Args:
    source: Andrea_Messner
    target: Günther_Messner
    relation: :hasFather
  AddTriple (f29f076e-baf3-4056-b623-dbd80869e119)
 Call ID: f29f076e-baf3-4056-b623-dbd80869e119
  Args:
    target: Lieselotte_Trzoska
    relation: :hasMother
    source: Andrea_Messner
  AssignClass (c7002370-2a40-4b7c-8dbb-51352be8cf6a)
 Call ID: c7002370-2a40-4b7c-8dbb-51352be8cf6a
  Args:
    type: :Man
    source: Armin_of_Lippe
  AddLiteral (ec4efd41-0732-42a0-a941-f531ae379c20)
 Call ID: ec4efd41-0732-42a0-a941-f531ae379c20
  Args:
    source: Armin_of_Lippe
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2015
  AssignClass (a5d56a8f-1d66-416d-8219-2f59a376bab7)
 Call ID: a5d56a8f-1d66-416d-8219-2f59a376bab7
  Args:
    source: Leopold_IV_of_Lippe
    type: :Man
  AssignClass (10ed299c-3c11-41f5-8856-c9f3660197a9)
 Call ID: 10ed299c-3c11-41f5-8856-c9f3660197a9
  Args:
    type: :Man
    source: Leopold_of_Lippe
  AssignClass (e7fef818-eeb9-4a4f-9c3d-9375cb7ff4f6)
 Call ID: e7fef818-eeb9-4a4f-9c3d-9375cb7ff4f6
  Args:
    type: :Man
    source: Ernst_of_Lippe
  AssignClass (31de5a9d-8a95-4119-9dd0-84c3388a7738)
 Call ID: 31de5a9d-8a95-4119-9dd0-84c3388a7738
  Args:
    source: Simon_Casimir_of_Lippe
    type: :Man
  AddLiteral (382b8f3b-552e-48ae-bf1f-277cd0f1de5a)
 Call ID: 382b8f3b-552e-48ae-bf1f-277cd0f1de5a
  Args:
    literal_value: 1900
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Simon_Casimir_of_Lippe
  AddLiteral (5d3f7364-7228-4c53-b346-d748906792c3)
 Call ID: 5d3f7364-7228-4c53-b346-d748906792c3
  Args:
    source: Simon_Casimir_of_Lippe
    relation: :hasDeathYear
    literal_value: 1980
    literal_type: xsd:integer
  AssignClass (16f0fad9-c4ad-4753-bfbf-3f756318226f)
 Call ID: 16f0fad9-c4ad-4753-bfbf-3f756318226f
  Args:
    type: :Man
    source: Stephan_of_Lippe
  AddTriple (4cb0db51-ed6a-46fd-ace8-36fceda9403c)
 Call ID: 4cb0db51-ed6a-46fd-ace8-36fceda9403c
  Args:
    target: Armin_of_Lippe
    relation: :hasFather
    source: Stephan_of_Lippe
  Finish (40b36d86-3f3b-4c8a-a54f-e6c0155a5ad3)
 Call ID: 40b36d86-3f3b-4c8a-a54f-e6c0155a5ad3
  Args: