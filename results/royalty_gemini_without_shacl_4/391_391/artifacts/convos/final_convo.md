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
Lady Amanda Patricia Victoria Ellingworth (née Knatchbull; born 26 June 1957), styled The Honourable Amanda Knatchbull between 1957 and 1979, is a British voluntary sector executive.
The granddaughter of Admiral of the Fleet Louis Mountbatten, 1st Earl Mountbatten of Burma, she is a descendant of Queen Victoria through her daughter Princess Alice, Mountbatten's grandmother.
Ancestry

Early life and education

Born as The Honourable Amanda Patricia Victoria Knatchbull, on 26 June 1957, in London, she was the fifth of eight children of the 7th Baron Brabourne and the 2nd Countess Mountbatten of Burma.
Earl Mountbatten of Burma, who was an uncle of Prince Philip, Duke of Edinburgh and a second cousin once removed of Queen Elizabeth II.
Ellingworth earned a BA Hons degree from the University of Kent, a CQSW qualification from Goldsmiths College, London, and a Certificate in Mandarin Language from the Beijing Language Institute.
, Ellingworth worked at a senior level in health services, children's services, adult social care and affordable housing.
Personal life

Marriage and family

Lady Amanda married novelist and property entrepreneur Charles Vincent Ellingworth on 31 October 1987.
Relationship with Prince of Wales

Ellingworth's grandfather Lord Mountbatten recommended her as a potential bride for his grandnephew, Charles, Prince of Wales.
According to his biographer, Jonathan Dimbleby, "In 1974, following his correspondence with Mountbatten on the subject, the Prince had tentatively raised the question of marriage to Amanda with her mother (and his godmother)
"


Mountbatten intended for himself and Lady Amanda to accompany Prince Charles on his planned 1980 tour of India.
Before Prince Charles was to depart, Mountbatten was assassinated by the IRA in August 1979.
When Prince Charles returned, he proposed to Lady Amanda.



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
  AssignClass (9343ff55-deb8-40c6-899e-0c8bfafd0465)
 Call ID: 9343ff55-deb8-40c6-899e-0c8bfafd0465
  Args:
    source: Amanda_Patricia_Victoria_Ellingworth
    type: :Woman
  AssignClass (2d404766-68f9-4c3b-897e-e2371cf9ae49)
 Call ID: 2d404766-68f9-4c3b-897e-e2371cf9ae49
  Args:
    source: Amanda_Patricia_Victoria_Ellingworth
    type: :Person
  AddLiteral (10f92115-7850-4686-bbd9-2a50bea4460a)
 Call ID: 10f92115-7850-4686-bbd9-2a50bea4460a
  Args:
    source: Amanda_Patricia_Victoria_Ellingworth
    literal_value: 1957
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (3958216b-26c5-4206-ac2b-646394348d20)
 Call ID: 3958216b-26c5-4206-ac2b-646394348d20
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    source: Amanda_Patricia_Victoria_Ellingworth
    literal_value: The Honourable Amanda Knatchbull
  AssignClass (f23be1bc-05f1-45a5-88ef-bd8fb3297567)
 Call ID: f23be1bc-05f1-45a5-88ef-bd8fb3297567
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (d19df572-8998-4bc8-9c1e-6eea3f992b07)
 Call ID: d19df572-8998-4bc8-9c1e-6eea3f992b07
  Args:
    type: :Person
    source: Louis_Mountbatten
  AssignClass (c76db2fb-7d17-4968-8cd7-63f49455548a)
 Call ID: c76db2fb-7d17-4968-8cd7-63f49455548a
  Args:
    type: :Ancestor
    source: Louis_Mountbatten
  AddTriple (761f166b-6c2d-4c37-99b0-b9c2a52ea044)
 Call ID: 761f166b-6c2d-4c37-99b0-b9c2a52ea044
  Args:
    source: Amanda_Patricia_Victoria_Ellingworth
    target: Louis_Mountbatten
    relation: :hasAncestor
  AssignClass (04ff93b3-f57a-4301-b63e-b239add1d700)
 Call ID: 04ff93b3-f57a-4301-b63e-b239add1d700
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (5bcaa0b8-d61c-46c9-bee2-5c3c65e2128e)
 Call ID: 5bcaa0b8-d61c-46c9-bee2-5c3c65e2128e
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (92aeed2d-ce69-4675-8000-c05dde45e877)
 Call ID: 92aeed2d-ce69-4675-8000-c05dde45e877
  Args:
    type: :Ancestor
    source: Queen_Victoria
  AddTriple (db381ac0-9fc1-443a-84c3-737aca45d514)
 Call ID: db381ac0-9fc1-443a-84c3-737aca45d514
  Args:
    source: Amanda_Patricia_Victoria_Ellingworth
    target: Queen_Victoria
    relation: :hasAncestor
  AssignClass (d9e29a64-50b2-4c50-b921-8eb34709edfa)
 Call ID: d9e29a64-50b2-4c50-b921-8eb34709edfa
  Args:
    type: :Woman
    source: Princess_Alice
  AssignClass (b0dc45cd-04a9-4896-bf51-42a50ee44059)
 Call ID: b0dc45cd-04a9-4896-bf51-42a50ee44059
  Args:
    source: Princess_Alice
    type: :Person
  AssignClass (e3cb92c3-bf47-4db9-a99d-978d9dad6e3a)
 Call ID: e3cb92c3-bf47-4db9-a99d-978d9dad6e3a
  Args:
    source: Princess_Alice
    type: :Ancestor
  AddTriple (aeede704-fd5a-4fe4-b35f-be1b9d91669a)
 Call ID: aeede704-fd5a-4fe4-b35f-be1b9d91669a
  Args:
    relation: :hasMother
    target: Princess_Alice
    source: Louis_Mountbatten
  AddTriple (a53e5515-e9d1-4e1e-879b-1d36faf751cc)
 Call ID: a53e5515-e9d1-4e1e-879b-1d36faf751cc
  Args:
    target: Queen_Victoria
    source: Princess_Alice
    relation: :hasMother
  AssignClass (61636e97-9735-44c6-a997-d34ec3c3ae41)
 Call ID: 61636e97-9735-44c6-a997-d34ec3c3ae41
  Args:
    type: :Man
    source: 7th_Baron_Brabourne
  AssignClass (421697b0-6171-422e-a9d9-738160ee7aa6)
 Call ID: 421697b0-6171-422e-a9d9-738160ee7aa6
  Args:
    source: 7th_Baron_Brabourne
    type: :Person
  AssignClass (37ab9da9-9248-4b81-b8cb-7bffe2d2ee5f)
 Call ID: 37ab9da9-9248-4b81-b8cb-7bffe2d2ee5f
  Args:
    source: 7th_Baron_Brabourne
    type: :Ancestor
  AssignClass (5b9e8783-6598-4bfb-8487-e9dc3024de87)
 Call ID: 5b9e8783-6598-4bfb-8487-e9dc3024de87
  Args:
    source: 2nd_Countess_Mountbatten_of_Burma
    type: :Woman
  AssignClass (f76abaa3-5313-4571-8ce6-34fb327ffbb2)
 Call ID: f76abaa3-5313-4571-8ce6-34fb327ffbb2
  Args:
    type: :Person
    source: 2nd_Countess_Mountbatten_of_Burma
  AssignClass (b845de45-68d6-4e26-b5e5-9c760c65b33f)
 Call ID: b845de45-68d6-4e26-b5e5-9c760c65b33f
  Args:
    source: 2nd_Countess_Mountbatten_of_Burma
    type: :Ancestor
  AddTriple (184b0941-af80-4dda-be6f-0ce9c51e1e38)
 Call ID: 184b0941-af80-4dda-be6f-0ce9c51e1e38
  Args:
    source: Amanda_Patricia_Victoria_Ellingworth
    target: 7th_Baron_Brabourne
    relation: :hasFather
  AddTriple (0fe02b2f-dd0f-4377-80a1-0770f7fbd2bc)
 Call ID: 0fe02b2f-dd0f-4377-80a1-0770f7fbd2bc
  Args:
    target: 2nd_Countess_Mountbatten_of_Burma
    source: Amanda_Patricia_Victoria_Ellingworth
    relation: :hasMother
  AssignClass (1c0e8e93-46e2-40ea-b139-0d18cb335f72)
 Call ID: 1c0e8e93-46e2-40ea-b139-0d18cb335f72
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (ce811edd-70cf-4a1a-bb1b-164d8817051f)
 Call ID: ce811edd-70cf-4a1a-bb1b-164d8817051f
  Args:
    source: Prince_Philip
    type: :Person
  AddTriple (49594b11-bb63-47b1-88ff-dc1aeca4eac0)
 Call ID: 49594b11-bb63-47b1-88ff-dc1aeca4eac0
  Args:
    source: Louis_Mountbatten
    target: Prince_Philip
    relation: :isUncleOf
  AssignClass (17099df9-50b9-4494-88b3-88af48b81b22)
 Call ID: 17099df9-50b9-4494-88b3-88af48b81b22
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (13b1413c-86a4-447a-8352-f6436117e8cb)
 Call ID: 13b1413c-86a4-447a-8352-f6436117e8cb
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (474b62d5-1201-4b86-8522-843275222a5b)
 Call ID: 474b62d5-1201-4b86-8522-843275222a5b
  Args:
    source: Charles_Vincent_Ellingworth
    type: :Man
  AssignClass (5190b2fc-f246-4fed-b805-ca074a7d1517)
 Call ID: 5190b2fc-f246-4fed-b805-ca074a7d1517
  Args:
    source: Charles_Vincent_Ellingworth
    type: :Person
  AddLiteral (1f276439-8ddc-4059-acaf-69e82a107700)
 Call ID: 1f276439-8ddc-4059-acaf-69e82a107700
  Args:
    literal_value: 1987
    source: Amanda_Patricia_Victoria_Ellingworth
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
  AddTriple (1299079b-8bef-48f8-8f92-64e1a5816294)
 Call ID: 1299079b-8bef-48f8-8f92-64e1a5816294
  Args:
    target: Charles_Vincent_Ellingworth
    source: Amanda_Patricia_Victoria_Ellingworth
    relation: :hasRelation
  AssignClass (e5fc5fde-afd2-4d6a-8906-75951dfaba69)
 Call ID: e5fc5fde-afd2-4d6a-8906-75951dfaba69
  Args:
    source: Prince_Charles
    type: :Man
  AssignClass (a9acc9ea-1c29-470c-a618-af55a3d9f8cb)
 Call ID: a9acc9ea-1c29-470c-a618-af55a3d9f8cb
  Args:
    type: :Person
    source: Prince_Charles
  AddLiteral (59f14924-99fe-47de-9271-593f5593eef2)
 Call ID: 59f14924-99fe-47de-9271-593f5593eef2
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1979
    source: Louis_Mountbatten
  Finish (7487bfdd-91fc-4867-b822-714f9b5a0490)
 Call ID: 7487bfdd-91fc-4867-b822-714f9b5a0490
  Args: