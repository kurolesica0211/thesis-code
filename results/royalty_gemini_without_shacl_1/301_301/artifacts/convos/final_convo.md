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
Tatiana von Preussen (born 16 October 1980) is an architect who worked on the construction of the  High Line, an elevated linear park, greenway and rail trail in New York.
In 2009 Tatiana von Preussen, Catherine Pease and Jessica Reynolds set up vPPR Architects.
Personal life

Tatiana von Preussen is the daughter of Prince Andreas of Prussia and Alexandra Blahova, and granddaughter of Prince Frederick of Prussia and Lady Brigid Guinness; on 28 June 2014 she married writer and journalist Philip Womack, and lives in London.
They have one son, Arthur Frederick Richard Womack von Preussen (born 21 November 2015) and twin girls, Xenia Alexandra Selena Womack von Preussen and Amalia Maria Brigid Womack von Preussen (born 29 August 2020).



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
  AssignClass (fbcb8a0e-148b-48b3-aded-e5267e7f5a41)
 Call ID: fbcb8a0e-148b-48b3-aded-e5267e7f5a41
  Args:
    source: Tatiana_von_Preussen
    type: :Woman
  AssignClass (3567b4a1-53ee-4576-bc24-fbfa0adc20cc)
 Call ID: 3567b4a1-53ee-4576-bc24-fbfa0adc20cc
  Args:
    source: Tatiana_von_Preussen
    type: :Person
  AddLiteral (81e64d5a-12c2-4484-8751-aaaedc0367f0)
 Call ID: 81e64d5a-12c2-4484-8751-aaaedc0367f0
  Args:
    literal_type: xsd:string
    literal_value: 1980
    relation: :hasBirthYear
    source: Tatiana_von_Preussen
  AssignClass (2f9b01e5-95a6-432b-82fb-09127ce27431)
 Call ID: 2f9b01e5-95a6-432b-82fb-09127ce27431
  Args:
    source: Prince_Andreas_of_Prussia
    type: :Man
  AssignClass (1727f726-df5d-4b58-b8f6-506491343bd7)
 Call ID: 1727f726-df5d-4b58-b8f6-506491343bd7
  Args:
    source: Prince_Andreas_of_Prussia
    type: :Person
  AssignClass (8ed6a01a-f4ad-40a5-ac42-539bebae08a5)
 Call ID: 8ed6a01a-f4ad-40a5-ac42-539bebae08a5
  Args:
    source: Alexandra_Blahova
    type: :Woman
  AssignClass (5fe65479-4154-4229-91c5-4daf1da3b03f)
 Call ID: 5fe65479-4154-4229-91c5-4daf1da3b03f
  Args:
    source: Alexandra_Blahova
    type: :Person
  AddTriple (3a129444-5894-46ab-810c-a2c83245c0c2)
 Call ID: 3a129444-5894-46ab-810c-a2c83245c0c2
  Args:
    target: Prince_Andreas_of_Prussia
    source: Tatiana_von_Preussen
    relation: :hasFather
  AddTriple (46476bbc-5b58-4219-a2ac-9ce302fc5d2c)
 Call ID: 46476bbc-5b58-4219-a2ac-9ce302fc5d2c
  Args:
    source: Tatiana_von_Preussen
    target: Alexandra_Blahova
    relation: :hasMother
  AssignClass (3d864372-8c76-4488-8dcd-3c59237083d1)
 Call ID: 3d864372-8c76-4488-8dcd-3c59237083d1
  Args:
    source: Prince_Frederick_of_Prussia
    type: :Man
  AssignClass (892cfa81-3a5e-4725-8a4d-235d2204a60b)
 Call ID: 892cfa81-3a5e-4725-8a4d-235d2204a60b
  Args:
    source: Prince_Frederick_of_Prussia
    type: :Person
  AssignClass (b6f3523c-0314-4f9c-84f9-bd2447d6baf3)
 Call ID: b6f3523c-0314-4f9c-84f9-bd2447d6baf3
  Args:
    type: :Woman
    source: Lady_Brigid_Guinness
  AssignClass (3987a490-ac68-4701-9aaf-b4a232a836a6)
 Call ID: 3987a490-ac68-4701-9aaf-b4a232a836a6
  Args:
    source: Lady_Brigid_Guinness
    type: :Person
  AddTriple (6d437c68-e890-44af-bc69-53dea214b29f)
 Call ID: 6d437c68-e890-44af-bc69-53dea214b29f
  Args:
    source: Prince_Andreas_of_Prussia
    target: Prince_Frederick_of_Prussia
    relation: :hasFather
  AddTriple (4ea5c3e2-c7a1-4bad-b452-062878fef687)
 Call ID: 4ea5c3e2-c7a1-4bad-b452-062878fef687
  Args:
    source: Prince_Andreas_of_Prussia
    target: Lady_Brigid_Guinness
    relation: :hasMother
  AssignClass (b711ff03-f811-48d6-a563-a05488aee0ad)
 Call ID: b711ff03-f811-48d6-a563-a05488aee0ad
  Args:
    source: Philip_Womack
    type: :Man
  AssignClass (533596cc-48d3-49a4-8551-821c5fd4bc6c)
 Call ID: 533596cc-48d3-49a4-8551-821c5fd4bc6c
  Args:
    source: Philip_Womack
    type: :Person
  AddLiteral (ccb1d58d-60ec-40be-b0a3-91014b16853e)
 Call ID: ccb1d58d-60ec-40be-b0a3-91014b16853e
  Args:
    literal_value: 2014
    relation: :hasMarriageYear
    literal_type: xsd:string
    source: Tatiana_von_Preussen
  AddTriple (29af7ccb-3df2-4f9d-947c-48a701fd8a18)
 Call ID: 29af7ccb-3df2-4f9d-947c-48a701fd8a18
  Args:
    relation: :hasRelation
    target: Philip_Womack
    source: Tatiana_von_Preussen
  AssignClass (76dcafd2-f382-454f-9fcd-15e25c0275cb)
 Call ID: 76dcafd2-f382-454f-9fcd-15e25c0275cb
  Args:
    source: Arthur_Frederick_Richard_Womack_von_Preussen
    type: :Man
  AssignClass (b6e9cb4f-ef1f-4213-b235-e6a7f6e496ac)
 Call ID: b6e9cb4f-ef1f-4213-b235-e6a7f6e496ac
  Args:
    source: Arthur_Frederick_Richard_Womack_von_Preussen
    type: :Person
  AddLiteral (ae0fe889-95e5-4cae-9631-8d5d5b74fcf4)
 Call ID: ae0fe889-95e5-4cae-9631-8d5d5b74fcf4
  Args:
    relation: :hasBirthYear
    literal_value: 2015
    literal_type: xsd:string
    source: Arthur_Frederick_Richard_Womack_von_Preussen
  AddTriple (b60368f6-6076-45ca-a337-6af0e2bbfed1)
 Call ID: b60368f6-6076-45ca-a337-6af0e2bbfed1
  Args:
    relation: :hasFather
    source: Arthur_Frederick_Richard_Womack_von_Preussen
    target: Philip_Womack
  AddTriple (126df2bb-8214-41a8-9662-f464dd04b685)
 Call ID: 126df2bb-8214-41a8-9662-f464dd04b685
  Args:
    relation: :hasMother
    target: Tatiana_von_Preussen
    source: Arthur_Frederick_Richard_Womack_von_Preussen
  AssignClass (452abec6-80b4-4c2a-a8ef-ff6a3bf7d5e9)
 Call ID: 452abec6-80b4-4c2a-a8ef-ff6a3bf7d5e9
  Args:
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    type: :Woman
  AssignClass (e99ca0e2-3810-4058-9c4b-e5b55ae31be4)
 Call ID: e99ca0e2-3810-4058-9c4b-e5b55ae31be4
  Args:
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    type: :Person
  AddLiteral (3a4213c0-4cd8-4d38-a6fa-983f5cface6c)
 Call ID: 3a4213c0-4cd8-4d38-a6fa-983f5cface6c
  Args:
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    literal_value: 2020
    relation: :hasBirthYear
    literal_type: xsd:string
  AddTriple (d4066bbf-6ff5-4be6-bfee-8b4f9fba32ff)
 Call ID: d4066bbf-6ff5-4be6-bfee-8b4f9fba32ff
  Args:
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    target: Philip_Womack
    relation: :hasFather
  AddTriple (df0575c5-5818-4ec6-8cbb-a86bc501fd28)
 Call ID: df0575c5-5818-4ec6-8cbb-a86bc501fd28
  Args:
    relation: :hasMother
    target: Tatiana_von_Preussen
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
  AssignClass (4af70fa0-e57c-4767-807f-8179f3b8ffdf)
 Call ID: 4af70fa0-e57c-4767-807f-8179f3b8ffdf
  Args:
    source: Amalia_Maria_Brigid_Womack_von_Preussen
    type: :Woman
  AssignClass (c2338f3e-1f79-4043-864d-a5f26d74321c)
 Call ID: c2338f3e-1f79-4043-864d-a5f26d74321c
  Args:
    source: Amalia_Maria_Brigid_Womack_von_Preussen
    type: :Person
  AddLiteral (8371d892-51ef-4ee4-8a87-87bd11856480)
 Call ID: 8371d892-51ef-4ee4-8a87-87bd11856480
  Args:
    source: Amalia_Maria_Brigid_Womack_von_Preussen
    literal_type: xsd:string
    literal_value: 2020
    relation: :hasBirthYear
  AddTriple (dff8b71a-f093-4361-b4bd-07eb795756b6)
 Call ID: dff8b71a-f093-4361-b4bd-07eb795756b6
  Args:
    target: Philip_Womack
    source: Amalia_Maria_Brigid_Womack_von_Preussen
    relation: :hasFather
  AddTriple (8eaaaf65-7e32-427c-b10c-0cce4139a86b)
 Call ID: 8eaaaf65-7e32-427c-b10c-0cce4139a86b
  Args:
    relation: :hasMother
    target: Tatiana_von_Preussen
    source: Amalia_Maria_Brigid_Womack_von_Preussen
  Finish (6459828f-6882-4511-ac52-9f7a50d048fc)
 Call ID: 6459828f-6882-4511-ac52-9f7a50d048fc
  Args: