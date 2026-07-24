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
Princess Kira Auguste Viktoria Friederike of Prussia (27 June 1943 – 10 January 2004) was the fourth child and second daughter of Louis Ferdinand, Prince of Prussia and Grand Duchess Kira Kirillovna of Russia.
Princess Kira was born in Cadienen, East Prussia (today Kadyny, Poland).
They had one daughter, Kira-Marina Liepsner (born 22 January 1977), who married Andreas Felix Paul von Bismarck (31 January 1979 – 31 October 2019)
Kira-Marina and Andreas had two daughters, Princess Kira’s granddaughters.
When her father died in 1994, Princess Kira took his seat on the board of the Kissinger Sommer classical music festival.



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
  AssignClass (b32e41e7-1d1e-48c8-bf0a-74d3354521e1)
 Call ID: b32e41e7-1d1e-48c8-bf0a-74d3354521e1
  Args:
    source: Princess_Kira_of_Prussia
    type: :Woman
  AssignClass (a3c41dff-47be-4492-9e11-1d37cb043c26)
 Call ID: a3c41dff-47be-4492-9e11-1d37cb043c26
  Args:
    type: :Person
    source: Princess_Kira_of_Prussia
  AddLiteral (616247b2-01b5-4877-9c49-251092a62f62)
 Call ID: 616247b2-01b5-4877-9c49-251092a62f62
  Args:
    literal_value: 1943
    source: Princess_Kira_of_Prussia
    relation: :hasBirthYear
    literal_type: xsd:string
  AddLiteral (28b20352-95b4-4119-b562-34e367ae672d)
 Call ID: 28b20352-95b4-4119-b562-34e367ae672d
  Args:
    source: Princess_Kira_of_Prussia
    literal_value: 2004
    relation: :hasDeathYear
    literal_type: xsd:string
  AssignClass (f6e56c84-a669-499e-bf0a-f349cb8825de)
 Call ID: f6e56c84-a669-499e-bf0a-f349cb8825de
  Args:
    type: :Man
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (56f6a3b7-8dc1-4aac-a9d0-92a96d1ca015)
 Call ID: 56f6a3b7-8dc1-4aac-a9d0-92a96d1ca015
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Person
  AssignClass (b4428850-3525-464a-b6a3-1254f4319b3f)
 Call ID: b4428850-3525-464a-b6a3-1254f4319b3f
  Args:
    type: :Woman
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AssignClass (e3b90702-fcc9-4e7b-8efd-86e375fd35b9)
 Call ID: e3b90702-fcc9-4e7b-8efd-86e375fd35b9
  Args:
    type: :Person
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AddTriple (762ca142-3264-47c3-bf66-3378fb011354)
 Call ID: 762ca142-3264-47c3-bf66-3378fb011354
  Args:
    source: Princess_Kira_of_Prussia
    relation: :hasFather
    target: Louis_Ferdinand_Prince_of_Prussia
  AddTriple (9fcec581-758d-457e-a5e7-02986c00791b)
 Call ID: 9fcec581-758d-457e-a5e7-02986c00791b
  Args:
    target: Grand_Duchess_Kira_Kirillovna_of_Russia
    relation: :hasMother
    source: Princess_Kira_of_Prussia
  AssignClass (a75840e5-1dab-41e9-ba6c-6a0ccaf53f27)
 Call ID: a75840e5-1dab-41e9-ba6c-6a0ccaf53f27
  Args:
    source: Kira-Marina_Liepsner
    type: :Woman
  AssignClass (4c3bc3a7-82f3-48f3-aa1d-b223c70d7304)
 Call ID: 4c3bc3a7-82f3-48f3-aa1d-b223c70d7304
  Args:
    type: :Person
    source: Kira-Marina_Liepsner
  AddTriple (6b087e15-662e-4620-b5a0-d108eee26f22)
 Call ID: 6b087e15-662e-4620-b5a0-d108eee26f22
  Args:
    target: Princess_Kira_of_Prussia
    relation: :hasMother
    source: Kira-Marina_Liepsner
  AddLiteral (2d77bcae-4ead-4e3e-9520-216584c88ce4)
 Call ID: 2d77bcae-4ead-4e3e-9520-216584c88ce4
  Args:
    literal_type: xsd:string
    relation: :hasBirthYear
    literal_value: 1977
    source: Kira-Marina_Liepsner
  AssignClass (36315dc8-8a7c-4e84-af93-6a20f208eb34)
 Call ID: 36315dc8-8a7c-4e84-af93-6a20f208eb34
  Args:
    type: :Man
    source: Andreas_Felix_Paul_von_Bismarck
  AssignClass (754286ad-32de-48d2-a2de-7cc208aac652)
 Call ID: 754286ad-32de-48d2-a2de-7cc208aac652
  Args:
    type: :Person
    source: Andreas_Felix_Paul_von_Bismarck
  AddLiteral (48aaf79b-3017-4651-9f54-55ea7ab31a93)
 Call ID: 48aaf79b-3017-4651-9f54-55ea7ab31a93
  Args:
    literal_type: xsd:string
    source: Andreas_Felix_Paul_von_Bismarck
    literal_value: 1979
    relation: :hasBirthYear
  AddLiteral (2c6c1917-c027-41fd-aa18-75159e99da3e)
 Call ID: 2c6c1917-c027-41fd-aa18-75159e99da3e
  Args:
    relation: :hasDeathYear
    source: Andreas_Felix_Paul_von_Bismarck
    literal_value: 2019
    literal_type: xsd:string
  AddTriple (7c3ea329-5b18-4ffd-bc43-113b2699ac14)
 Call ID: 7c3ea329-5b18-4ffd-bc43-113b2699ac14
  Args:
    relation: :hasRelation
    source: Kira-Marina_Liepsner
    target: Andreas_Felix_Paul_von_Bismarck
  AssignClass (f51dc489-63b7-4f70-b040-6c0594fbacd0)
 Call ID: f51dc489-63b7-4f70-b040-6c0594fbacd0
  Args:
    type: :Woman
    source: Granddaughter1
  AssignClass (e73a499a-6533-4a17-a109-aae1453eedef)
 Call ID: e73a499a-6533-4a17-a109-aae1453eedef
  Args:
    source: Granddaughter1
    type: :Person
  AssignClass (bc8e2f64-7edc-4cdc-8c8f-fc19be278cfb)
 Call ID: bc8e2f64-7edc-4cdc-8c8f-fc19be278cfb
  Args:
    source: Granddaughter2
    type: :Woman
  AssignClass (881f5b1e-7768-46b6-938f-414009f186a9)
 Call ID: 881f5b1e-7768-46b6-938f-414009f186a9
  Args:
    type: :Person
    source: Granddaughter2
  AddTriple (acd7fde5-f132-4951-9e01-7452d3dfa511)
 Call ID: acd7fde5-f132-4951-9e01-7452d3dfa511
  Args:
    source: Granddaughter1
    relation: :hasMother
    target: Kira-Marina_Liepsner
  AddTriple (25c03a35-cfb4-48ea-92d2-8ef4566db100)
 Call ID: 25c03a35-cfb4-48ea-92d2-8ef4566db100
  Args:
    relation: :hasFather
    source: Granddaughter1
    target: Andreas_Felix_Paul_von_Bismarck
  AddTriple (8bc0440d-1566-4f7b-a422-05efb137b7dd)
 Call ID: 8bc0440d-1566-4f7b-a422-05efb137b7dd
  Args:
    target: Kira-Marina_Liepsner
    relation: :hasMother
    source: Granddaughter2
  AddTriple (d94b80af-1196-436a-92be-65909f1857e1)
 Call ID: d94b80af-1196-436a-92be-65909f1857e1
  Args:
    target: Andreas_Felix_Paul_von_Bismarck
    source: Granddaughter2
    relation: :hasFather
  Finish (526b73b0-b672-467a-91d2-759a156a1c19)
 Call ID: 526b73b0-b672-467a-91d2-759a156a1c19
  Args: