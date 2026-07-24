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
John David James Dalrymple, 14th Earl of Stair (born 4 September 1961) is a British politician and a former crossbench member of the House of Lords.
Background

Stair is the eldest child of John Dalrymple, 13th
Earl of Stair and Davina Katherine Bowes-Lyon (2 May 1930 – 1 November 2017), daughter of David Bowes-Lyon, brother of Queen Elizabeth
Lord Stair's mother, Davina, therefore, was a first cousin of Queen Elizabeth II and he is a second cousin of The King, The Princess Royal, Andrew Mountbatten-Windsor, and The Duke of Edinburgh.
Through his mother, he is descended from the Bowes-Lyon, Astor, and Cavendish-Bentinck families.
Through his paternal-grandmother, Violet Evelyn Dalrymple (Née Harford), he is a direct descendent of Frederick Calvert, 6th Baron Baltimore, the Calvert family were the founders and Proprietors of Province of Maryland.
Political career

Upon inheriting his peerage in 1996, Lord Stair entered the House of Lords and sat as a crossbencher.
Following the death of Davina Ingrams, 18th Baroness Darcy de Knayth in 2008, Lord Stair was elected to the Lords.
Family

Lord Stair married Emily Mary Julia Stonor (daughter of Ralph Stonor, 7th Baron Camoys, and Elizabeth Mary Hyde Parker) in 2006.



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
  AssignClass (5034f5e9-256b-4722-834e-e20aaa2368cd)
 Call ID: 5034f5e9-256b-4722-834e-e20aaa2368cd
  Args:
    type: :Man
    source: :John_David_James_Dalrymple
  AssignClass (1c8b3102-03c3-4a06-88f2-e9a696b1d76f)
 Call ID: 1c8b3102-03c3-4a06-88f2-e9a696b1d76f
  Args:
    source: :John_David_James_Dalrymple
    type: :Person
  AddLiteral (009875e7-9dbf-4aa7-ae97-e9d37b50cc00)
 Call ID: 009875e7-9dbf-4aa7-ae97-e9d37b50cc00
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1961
    source: :John_David_James_Dalrymple
  AssignClass (a3f27bb9-0b9a-4dbf-9566-10e16e92b39a)
 Call ID: a3f27bb9-0b9a-4dbf-9566-10e16e92b39a
  Args:
    source: :John_Dalrymple_13th_Earl_of_Stair
    type: :Man
  AssignClass (3bbb742f-b517-42d6-8e5f-bdebe147d2db)
 Call ID: 3bbb742f-b517-42d6-8e5f-bdebe147d2db
  Args:
    source: :John_Dalrymple_13th_Earl_of_Stair
    type: :Person
  AddTriple (5c1042ae-3bec-4a13-bb83-fe76da9e67b7)
 Call ID: 5c1042ae-3bec-4a13-bb83-fe76da9e67b7
  Args:
    relation: :hasFather
    source: :John_David_James_Dalrymple
    target: :John_Dalrymple_13th_Earl_of_Stair
  AssignClass (ae2ed9cb-b2c6-4ef5-9135-d83b1154eaed)
 Call ID: ae2ed9cb-b2c6-4ef5-9135-d83b1154eaed
  Args:
    source: :Davina_Katherine_Bowes-Lyon
    type: :Woman
  AssignClass (8bcf252c-a467-4f05-a019-00ea05fc61f8)
 Call ID: 8bcf252c-a467-4f05-a019-00ea05fc61f8
  Args:
    source: :Davina_Katherine_Bowes-Lyon
    type: :Person
  AddTriple (cbed4762-018d-471a-8415-726803230554)
 Call ID: cbed4762-018d-471a-8415-726803230554
  Args:
    relation: :hasMother
    target: :Davina_Katherine_Bowes-Lyon
    source: :John_David_James_Dalrymple
  AddLiteral (f84277bb-e475-4590-81a0-69160133ef00)
 Call ID: f84277bb-e475-4590-81a0-69160133ef00
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1930
    source: :Davina_Katherine_Bowes-Lyon
  AddLiteral (6e8b7f7d-22f4-4a37-aa39-14bf3a6e8056)
 Call ID: 6e8b7f7d-22f4-4a37-aa39-14bf3a6e8056
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2017
    source: :Davina_Katherine_Bowes-Lyon
  AssignClass (79811069-dc8a-478a-9686-db63f0dd8d44)
 Call ID: 79811069-dc8a-478a-9686-db63f0dd8d44
  Args:
    source: :David_Bowes-Lyon
    type: :Man
  AssignClass (4366ff81-2e11-4b0c-a231-dcac39b7cdae)
 Call ID: 4366ff81-2e11-4b0c-a231-dcac39b7cdae
  Args:
    source: :David_Bowes-Lyon
    type: :Person
  AddTriple (7b9e73a1-68d0-488e-9644-e321b5d76915)
 Call ID: 7b9e73a1-68d0-488e-9644-e321b5d76915
  Args:
    relation: :hasFather
    target: :David_Bowes-Lyon
    source: :Davina_Katherine_Bowes-Lyon
  AssignClass (10c7c5c0-1cff-4461-b5a3-13a90a0ea2f3)
 Call ID: 10c7c5c0-1cff-4461-b5a3-13a90a0ea2f3
  Args:
    type: :Woman
    source: :Violet_Evelyn_Dalrymple
  AssignClass (22ff4bcf-1f4a-4ad3-8fce-f1c3c5915d70)
 Call ID: 22ff4bcf-1f4a-4ad3-8fce-f1c3c5915d70
  Args:
    source: :Violet_Evelyn_Dalrymple
    type: :Person
  AddTriple (93ef8ec2-1aa3-4963-9cb4-6b5d099b6609)
 Call ID: 93ef8ec2-1aa3-4963-9cb4-6b5d099b6609
  Args:
    source: :John_Dalrymple_13th_Earl_of_Stair
    target: :Violet_Evelyn_Dalrymple
    relation: :hasMother
  AssignClass (a4d2456d-81b8-466e-b71c-4d1438ca9f74)
 Call ID: a4d2456d-81b8-466e-b71c-4d1438ca9f74
  Args:
    type: :Man
    source: :Frederick_Calvert_6th_Baron_Baltimore
  AssignClass (c11646a5-e71b-42d5-b5b7-328a89d0208e)
 Call ID: c11646a5-e71b-42d5-b5b7-328a89d0208e
  Args:
    type: :Person
    source: :Frederick_Calvert_6th_Baron_Baltimore
  AddTriple (948dcda5-0018-4a15-a43c-58c98aa5101d)
 Call ID: 948dcda5-0018-4a15-a43c-58c98aa5101d
  Args:
    relation: :hasAncestor
    source: :John_David_James_Dalrymple
    target: :Frederick_Calvert_6th_Baron_Baltimore
  AssignClass (19b62b27-9498-4e01-8819-ad2a7bdf6256)
 Call ID: 19b62b27-9498-4e01-8819-ad2a7bdf6256
  Args:
    type: :Woman
    source: :Emily_Mary_Julia_Stonor
  AssignClass (2dc44740-923e-474b-8047-90d949b4fbbe)
 Call ID: 2dc44740-923e-474b-8047-90d949b4fbbe
  Args:
    source: :Emily_Mary_Julia_Stonor
    type: :Person
  AddTriple (b206cee1-5d48-4547-9e83-c8dd53e97346)
 Call ID: b206cee1-5d48-4547-9e83-c8dd53e97346
  Args:
    relation: :hasRelation
    source: :John_David_James_Dalrymple
    target: :Emily_Mary_Julia_Stonor
  AddLiteral (613f4286-4a9d-4433-a93e-b79116970f5e)
 Call ID: 613f4286-4a9d-4433-a93e-b79116970f5e
  Args:
    source: :John_David_James_Dalrymple
    literal_value: 2006
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (ff324f08-f067-4337-b623-61f69e94f2c2)
 Call ID: ff324f08-f067-4337-b623-61f69e94f2c2
  Args:
    source: :Ralph_Stonor_7th_Baron_Camoys
    type: :Man
  AssignClass (676cd5b5-128d-45b1-9010-112d89252c09)
 Call ID: 676cd5b5-128d-45b1-9010-112d89252c09
  Args:
    type: :Person
    source: :Ralph_Stonor_7th_Baron_Camoys
  AddTriple (32068edf-ec93-4506-b77e-8a8b03c6ff4d)
 Call ID: 32068edf-ec93-4506-b77e-8a8b03c6ff4d
  Args:
    source: :Emily_Mary_Julia_Stonor
    target: :Ralph_Stonor_7th_Baron_Camoys
    relation: :hasFather
  AssignClass (f1558f38-6f13-44bd-ae79-1bb8b9955f68)
 Call ID: f1558f38-6f13-44bd-ae79-1bb8b9955f68
  Args:
    type: :Woman
    source: :Elizabeth_Mary_Hyde_Parker
  AssignClass (7642705f-9551-466c-85ec-b5437be7880d)
 Call ID: 7642705f-9551-466c-85ec-b5437be7880d
  Args:
    source: :Elizabeth_Mary_Hyde_Parker
    type: :Person
  AddTriple (86960daa-5778-4321-a1fb-fc1bfbb3c610)
 Call ID: 86960daa-5778-4321-a1fb-fc1bfbb3c610
  Args:
    relation: :hasMother
    source: :Emily_Mary_Julia_Stonor
    target: :Elizabeth_Mary_Hyde_Parker
  Finish (d7a55d8a-214d-47e3-b67e-e8edd4b3c926)
 Call ID: d7a55d8a-214d-47e3-b67e-e8edd4b3c926
  Args: