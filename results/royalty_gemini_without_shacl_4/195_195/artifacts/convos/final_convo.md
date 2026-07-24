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
James Alexander Elphinstone, 18th Lord Elphinstone and 4th Baron Elphinstone, AssocRICS (22 April 1953 – 19 December 1994), was a British nobleman, farmer, and financier.
Early life and family

Lord Elphinstone was the son of Rev. Hon.
Andrew Charles Victor Elphinstone and Jean Frances Hambro.
His paternal grandparents were Sidney Buller-Fullerton-Elphinstone, 16th Lord Elphinstone, and the former Lady Mary Bowes-Lyon, elder sister of Queen Elizabeth The Queen Mother.
Personal life

On 22 April 1978, Lord Elphinstone married Willa Mary Gabrielle Chetwode, daughter of Major George David Chetwode and Lady Willa Elliot-Murray-Kynynmound (herself the daughter of Victor Elliot-Murray-Kynynmound, 5th Earl of Minto, and his wife, Marion Cook).
The couple had four children:


He was succeeded in his titles by his eldest son, Alexander.
References




This biography of a Lord of Parliament in the Peerage of Scotland is a stub.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (417aa562-dd5c-4ec2-ab3a-cb816fdd6b0a)
 Call ID: 417aa562-dd5c-4ec2-ab3a-cb816fdd6b0a
  Args:
    type: :Man
    source: James_Alexander_Elphinstone
  AssignClass (dc6df566-23df-43e8-8ae2-20083b3855fa)
 Call ID: dc6df566-23df-43e8-8ae2-20083b3855fa
  Args:
    source: James_Alexander_Elphinstone
    type: :Person
  AddLiteral (44f1282c-64ac-4b51-854f-f9a2aad7decd)
 Call ID: 44f1282c-64ac-4b51-854f-f9a2aad7decd
  Args:
    literal_value: 1953
    source: James_Alexander_Elphinstone
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (601b3593-37f5-4953-bd2c-e361f4458fe6)
 Call ID: 601b3593-37f5-4953-bd2c-e361f4458fe6
  Args:
    source: James_Alexander_Elphinstone
    literal_value: 1994
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (f60121ba-8380-4886-bd3b-ba040a6a3c05)
 Call ID: f60121ba-8380-4886-bd3b-ba040a6a3c05
  Args:
    type: :Man
    source: Andrew_Charles_Victor_Elphinstone
  AssignClass (ef53b7fe-654a-4e95-92e0-34a1eef78c84)
 Call ID: ef53b7fe-654a-4e95-92e0-34a1eef78c84
  Args:
    source: Andrew_Charles_Victor_Elphinstone
    type: :Person
  AddTriple (39fe8f04-f371-496d-9bf9-8b7f2a105dbb)
 Call ID: 39fe8f04-f371-496d-9bf9-8b7f2a105dbb
  Args:
    source: James_Alexander_Elphinstone
    target: Andrew_Charles_Victor_Elphinstone
    relation: :hasFather
  AssignClass (8cff3130-d62a-49c8-8a24-1a434047bfea)
 Call ID: 8cff3130-d62a-49c8-8a24-1a434047bfea
  Args:
    type: :Woman
    source: Jean_Frances_Hambro
  AssignClass (9d367ce2-03cd-45c2-8e18-e908692d3adb)
 Call ID: 9d367ce2-03cd-45c2-8e18-e908692d3adb
  Args:
    source: Jean_Frances_Hambro
    type: :Person
  AddTriple (0c23fe26-c770-44c6-941d-e555fcdadb06)
 Call ID: 0c23fe26-c770-44c6-941d-e555fcdadb06
  Args:
    source: James_Alexander_Elphinstone
    target: Jean_Frances_Hambro
    relation: :hasMother
  AssignClass (531634c2-dac5-4900-9a85-5cf188f88304)
 Call ID: 531634c2-dac5-4900-9a85-5cf188f88304
  Args:
    source: Sidney_Buller_Fullerton_Elphinstone
    type: :Man
  AssignClass (b78260dc-1293-4759-aa30-623e7ad7c755)
 Call ID: b78260dc-1293-4759-aa30-623e7ad7c755
  Args:
    source: Sidney_Buller_Fullerton_Elphinstone
    type: :Person
  AddTriple (d8b4049e-0dd2-45cb-9815-932973798b48)
 Call ID: d8b4049e-0dd2-45cb-9815-932973798b48
  Args:
    target: Sidney_Buller_Fullerton_Elphinstone
    source: Andrew_Charles_Victor_Elphinstone
    relation: :hasFather
  AssignClass (44a0ac44-51f2-4f7b-b848-fd1009215925)
 Call ID: 44a0ac44-51f2-4f7b-b848-fd1009215925
  Args:
    type: :Woman
    source: Mary_Bowes_Lyon
  AssignClass (6f2ce8db-d55a-4a42-89c5-4e79cd040261)
 Call ID: 6f2ce8db-d55a-4a42-89c5-4e79cd040261
  Args:
    type: :Person
    source: Mary_Bowes_Lyon
  AddTriple (b5f5190e-b8c6-4040-9563-6017eb2b0453)
 Call ID: b5f5190e-b8c6-4040-9563-6017eb2b0453
  Args:
    relation: :hasMother
    source: Andrew_Charles_Victor_Elphinstone
    target: Mary_Bowes_Lyon
  AssignClass (0d9b9a9b-0a64-4171-8efc-16692fc58bfa)
 Call ID: 0d9b9a9b-0a64-4171-8efc-16692fc58bfa
  Args:
    source: Queen_Elizabeth_The_Queen_Mother
    type: :Woman
  AssignClass (18113bb9-1919-4e31-ae29-abf1a547f9b0)
 Call ID: 18113bb9-1919-4e31-ae29-abf1a547f9b0
  Args:
    type: :Person
    source: Queen_Elizabeth_The_Queen_Mother
  AddTriple (da4d2264-334f-42e5-b3a3-aa6202294570)
 Call ID: da4d2264-334f-42e5-b3a3-aa6202294570
  Args:
    target: Queen_Elizabeth_The_Queen_Mother
    source: Mary_Bowes_Lyon
    relation: :isSisterOf
  AssignClass (2e080f17-71f4-4cff-8877-8ada9fa01710)
 Call ID: 2e080f17-71f4-4cff-8877-8ada9fa01710
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Woman
  AssignClass (85e42bf5-0e2e-4aea-8085-847c707e8034)
 Call ID: 85e42bf5-0e2e-4aea-8085-847c707e8034
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Person
  AddLiteral (069d10d4-6ab3-4437-96c1-b2a079c39200)
 Call ID: 069d10d4-6ab3-4437-96c1-b2a079c39200
  Args:
    literal_value: 1978
    source: James_Alexander_Elphinstone
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (0c3eff50-b902-4ac4-89a8-45db5001386f)
 Call ID: 0c3eff50-b902-4ac4-89a8-45db5001386f
  Args:
    target: Willa_Mary_Gabrielle_Chetwode
    source: James_Alexander_Elphinstone
    relation: :hasRelation
  AssignClass (980e412a-8f7c-4023-b1a8-acd82f9ec76b)
 Call ID: 980e412a-8f7c-4023-b1a8-acd82f9ec76b
  Args:
    type: :Man
    source: George_David_Chetwode
  AssignClass (681836f5-3261-44a8-8459-b0c9f89f3f70)
 Call ID: 681836f5-3261-44a8-8459-b0c9f89f3f70
  Args:
    source: George_David_Chetwode
    type: :Person
  AddTriple (c5b84865-bb69-4de4-801c-0265030e37cc)
 Call ID: c5b84865-bb69-4de4-801c-0265030e37cc
  Args:
    target: George_David_Chetwode
    source: Willa_Mary_Gabrielle_Chetwode
    relation: :hasFather
  AssignClass (e30c5548-c204-4d90-89ea-b508b9034c75)
 Call ID: e30c5548-c204-4d90-89ea-b508b9034c75
  Args:
    type: :Woman
    source: Willa_Elliot_Murray_Kynynmound
  AssignClass (9f104e43-94a0-4020-bde5-2ee45405876a)
 Call ID: 9f104e43-94a0-4020-bde5-2ee45405876a
  Args:
    source: Willa_Elliot_Murray_Kynynmound
    type: :Person
  AddTriple (37ec9a2d-1e72-46b6-a5d7-faffe79683a7)
 Call ID: 37ec9a2d-1e72-46b6-a5d7-faffe79683a7
  Args:
    target: Willa_Elliot_Murray_Kynynmound
    source: Willa_Mary_Gabrielle_Chetwode
    relation: :hasMother
  AssignClass (79a07d8e-7883-4f05-9fd8-bdb6ad94ddad)
 Call ID: 79a07d8e-7883-4f05-9fd8-bdb6ad94ddad
  Args:
    source: Victor_Elliot_Murray_Kynynmound
    type: :Man
  AssignClass (4ad054e5-a5f1-4d03-8c20-fc5f7ad2c299)
 Call ID: 4ad054e5-a5f1-4d03-8c20-fc5f7ad2c299
  Args:
    type: :Person
    source: Victor_Elliot_Murray_Kynynmound
  AddTriple (8d1eb676-892d-40dd-ba0f-e0206396c420)
 Call ID: 8d1eb676-892d-40dd-ba0f-e0206396c420
  Args:
    source: Willa_Elliot_Murray_Kynynmound
    target: Victor_Elliot_Murray_Kynynmound
    relation: :hasFather
  AssignClass (621e1728-eb04-4d35-80df-f2e9af0be5ff)
 Call ID: 621e1728-eb04-4d35-80df-f2e9af0be5ff
  Args:
    source: Marion_Cook
    type: :Woman
  AssignClass (72b7ee85-0ac7-4be1-b41c-b847fe237801)
 Call ID: 72b7ee85-0ac7-4be1-b41c-b847fe237801
  Args:
    source: Marion_Cook
    type: :Person
  AddTriple (b1f32850-2d33-4eec-a4cc-90b82acf609a)
 Call ID: b1f32850-2d33-4eec-a4cc-90b82acf609a
  Args:
    relation: :hasMother
    target: Marion_Cook
    source: Willa_Elliot_Murray_Kynynmound
  AssignClass (a3dd995e-537c-480e-babf-59513e909af0)
 Call ID: a3dd995e-537c-480e-babf-59513e909af0
  Args:
    type: :Man
    source: Alexander_Elphinstone
  AssignClass (07d89ac4-8df7-4acb-a4f9-6df533f9a27b)
 Call ID: 07d89ac4-8df7-4acb-a4f9-6df533f9a27b
  Args:
    source: Alexander_Elphinstone
    type: :Person
  AddTriple (093a6603-ef27-42f3-940d-4ed185aa92ff)
 Call ID: 093a6603-ef27-42f3-940d-4ed185aa92ff
  Args:
    source: James_Alexander_Elphinstone
    target: Alexander_Elphinstone
    relation: :hasSon
  Finish (6f007311-1f8e-4d77-83ee-69431f206eb5)
 Call ID: 6f007311-1f8e-4d77-83ee-69431f206eb5
  Args: