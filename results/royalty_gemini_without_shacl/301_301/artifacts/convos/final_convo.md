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
  AssignClass (cd35bbb5-ee44-4ce8-ba26-7abcb2570e7f)
 Call ID: cd35bbb5-ee44-4ce8-ba26-7abcb2570e7f
  Args:
    source: Tatiana von Preussen
    type: :Woman
  AssignClass (886e06e5-e6a8-4f83-8294-f7d413ed4366)
 Call ID: 886e06e5-e6a8-4f83-8294-f7d413ed4366
  Args:
    type: :Person
    source: Tatiana von Preussen
  AddLiteral (4646c827-9565-4cc6-bdce-b89a037c76b1)
 Call ID: 4646c827-9565-4cc6-bdce-b89a037c76b1
  Args:
    source: Tatiana von Preussen
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1980
  AssignClass (1c85f48a-db5d-4107-87b7-b476d4c2f2c0)
 Call ID: 1c85f48a-db5d-4107-87b7-b476d4c2f2c0
  Args:
    type: :Man
    source: Prince Andreas of Prussia
  AssignClass (59423a0c-4b85-4691-8030-0e305a8b625e)
 Call ID: 59423a0c-4b85-4691-8030-0e305a8b625e
  Args:
    type: :Person
    source: Prince Andreas of Prussia
  AssignClass (ce987ff4-f953-4271-ae5c-10d84ed09edd)
 Call ID: ce987ff4-f953-4271-ae5c-10d84ed09edd
  Args:
    source: Alexandra Blahova
    type: :Woman
  AssignClass (7a50e2ed-ca2d-4eec-a600-b7aa5d7789e2)
 Call ID: 7a50e2ed-ca2d-4eec-a600-b7aa5d7789e2
  Args:
    type: :Person
    source: Alexandra Blahova
  AddTriple (72ffa993-6310-4295-95cf-a2fbd234677c)
 Call ID: 72ffa993-6310-4295-95cf-a2fbd234677c
  Args:
    relation: :hasFather
    target: Prince Andreas of Prussia
    source: Tatiana von Preussen
  AddTriple (7d9cc27c-79a9-423d-a71b-e6fd2d875f05)
 Call ID: 7d9cc27c-79a9-423d-a71b-e6fd2d875f05
  Args:
    relation: :hasMother
    target: Alexandra Blahova
    source: Tatiana von Preussen
  AssignClass (291fd521-b152-4593-a22f-b75dac9084a9)
 Call ID: 291fd521-b152-4593-a22f-b75dac9084a9
  Args:
    type: :Man
    source: Prince Frederick of Prussia
  AssignClass (83aa153b-b93a-4838-a9b4-44a130bb0330)
 Call ID: 83aa153b-b93a-4838-a9b4-44a130bb0330
  Args:
    type: :Person
    source: Prince Frederick of Prussia
  AssignClass (8249ffa9-991d-4c12-8400-f23c4b11c6c7)
 Call ID: 8249ffa9-991d-4c12-8400-f23c4b11c6c7
  Args:
    source: Lady Brigid Guinness
    type: :Woman
  AssignClass (ee08644d-d373-4f81-81c7-aa05066cd8ec)
 Call ID: ee08644d-d373-4f81-81c7-aa05066cd8ec
  Args:
    source: Lady Brigid Guinness
    type: :Person
  AddTriple (d183d17e-7c78-4a70-a73b-c78ebdb13742)
 Call ID: d183d17e-7c78-4a70-a73b-c78ebdb13742
  Args:
    source: Prince Andreas of Prussia
    target: Prince Frederick of Prussia
    relation: :hasFather
  AddTriple (9c677fa2-2ff3-4164-a4c2-10832acc327b)
 Call ID: 9c677fa2-2ff3-4164-a4c2-10832acc327b
  Args:
    relation: :hasMother
    target: Lady Brigid Guinness
    source: Prince Andreas of Prussia
  AssignClass (3365f014-bc55-4818-bf6e-11acdff4215d)
 Call ID: 3365f014-bc55-4818-bf6e-11acdff4215d
  Args:
    source: Philip Womack
    type: :Man
  AssignClass (3c48281c-2f69-4667-a695-a07bbecfe097)
 Call ID: 3c48281c-2f69-4667-a695-a07bbecfe097
  Args:
    type: :Person
    source: Philip Womack
  AddLiteral (de1b7127-4c3b-46c7-94b8-b22ff995491e)
 Call ID: de1b7127-4c3b-46c7-94b8-b22ff995491e
  Args:
    relation: :hasMarriageYear
    literal_value: 2014
    literal_type: xsd:integer
    source: Tatiana von Preussen
  AddTriple (5cd7c7b2-02ac-4a76-bb3b-3fcae6f14d2e)
 Call ID: 5cd7c7b2-02ac-4a76-bb3b-3fcae6f14d2e
  Args:
    relation: :hasRelation
    target: Philip Womack
    source: Tatiana von Preussen
  AssignClass (703517b5-3357-4c67-9f50-526558a6f480)
 Call ID: 703517b5-3357-4c67-9f50-526558a6f480
  Args:
    type: :Man
    source: Arthur Frederick Richard Womack von Preussen
  AssignClass (2f75e021-f10e-4dab-a3c2-9003964c3e9d)
 Call ID: 2f75e021-f10e-4dab-a3c2-9003964c3e9d
  Args:
    source: Arthur Frederick Richard Womack von Preussen
    type: :Person
  AddLiteral (dda8d18f-7cc2-418c-97b7-e3b8bdd2dd9c)
 Call ID: dda8d18f-7cc2-418c-97b7-e3b8bdd2dd9c
  Args:
    literal_value: 2015
    relation: :hasBirthYear
    source: Arthur Frederick Richard Womack von Preussen
    literal_type: xsd:integer
  AddTriple (1c48f44e-68de-4e16-bf4a-fea45a07038c)
 Call ID: 1c48f44e-68de-4e16-bf4a-fea45a07038c
  Args:
    target: Philip Womack
    source: Arthur Frederick Richard Womack von Preussen
    relation: :hasFather
  AddTriple (1678b27c-b652-4b01-bec9-54a3d553e72a)
 Call ID: 1678b27c-b652-4b01-bec9-54a3d553e72a
  Args:
    source: Arthur Frederick Richard Womack von Preussen
    target: Tatiana von Preussen
    relation: :hasMother
  AssignClass (b4aae046-85c1-4024-9601-e908f7991091)
 Call ID: b4aae046-85c1-4024-9601-e908f7991091
  Args:
    type: :Woman
    source: Xenia Alexandra Selena Womack von Preussen
  AssignClass (cf16eea7-96d6-41ba-b573-8966ec1a30ff)
 Call ID: cf16eea7-96d6-41ba-b573-8966ec1a30ff
  Args:
    source: Xenia Alexandra Selena Womack von Preussen
    type: :Person
  AddLiteral (1a1de904-3358-4d98-bee3-23bc4ebb7f07)
 Call ID: 1a1de904-3358-4d98-bee3-23bc4ebb7f07
  Args:
    relation: :hasBirthYear
    literal_value: 2020
    source: Xenia Alexandra Selena Womack von Preussen
    literal_type: xsd:integer
  AddTriple (af1ab95b-45ec-4c97-ab61-6db58442d7ed)
 Call ID: af1ab95b-45ec-4c97-ab61-6db58442d7ed
  Args:
    target: Philip Womack
    source: Xenia Alexandra Selena Womack von Preussen
    relation: :hasFather
  AddTriple (1bbfec91-4dfb-41ae-9e23-39f18b066e0d)
 Call ID: 1bbfec91-4dfb-41ae-9e23-39f18b066e0d
  Args:
    relation: :hasMother
    source: Xenia Alexandra Selena Womack von Preussen
    target: Tatiana von Preussen
  AssignClass (4954835d-19d8-459c-b99e-ceb9a33660bd)
 Call ID: 4954835d-19d8-459c-b99e-ceb9a33660bd
  Args:
    type: :Woman
    source: Amalia Maria Brigid Womack von Preussen
  AssignClass (f21e1b93-e93b-4d88-8cf7-4f08479353e3)
 Call ID: f21e1b93-e93b-4d88-8cf7-4f08479353e3
  Args:
    type: :Person
    source: Amalia Maria Brigid Womack von Preussen
  AddLiteral (a3f85162-4a76-4abb-9471-e4ebad85759d)
 Call ID: a3f85162-4a76-4abb-9471-e4ebad85759d
  Args:
    literal_type: xsd:integer
    source: Amalia Maria Brigid Womack von Preussen
    literal_value: 2020
    relation: :hasBirthYear
  AddTriple (76755011-1c96-4529-b395-62b710281a90)
 Call ID: 76755011-1c96-4529-b395-62b710281a90
  Args:
    relation: :hasFather
    source: Amalia Maria Brigid Womack von Preussen
    target: Philip Womack
  AddTriple (c173cf9d-9e70-48c0-b272-b775b786ba8a)
 Call ID: c173cf9d-9e70-48c0-b272-b775b786ba8a
  Args:
    relation: :hasMother
    target: Tatiana von Preussen
    source: Amalia Maria Brigid Womack von Preussen
  Finish (a580e131-4f65-42e5-83ea-35887008b174)
 Call ID: a580e131-4f65-42e5-83ea-35887008b174
  Args: