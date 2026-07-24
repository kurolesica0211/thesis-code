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
  AssignClass (04a1b41b-f8cd-4bb8-beaa-08a518f2f61c)
 Call ID: 04a1b41b-f8cd-4bb8-beaa-08a518f2f61c
  Args:
    type: :Woman
    source: Tatiana_von_Preussen
  AssignClass (9f847777-b191-4221-a28d-998a71783087)
 Call ID: 9f847777-b191-4221-a28d-998a71783087
  Args:
    type: :Person
    source: Tatiana_von_Preussen
  AddLiteral (b2a3cf07-cc5d-40eb-b4d5-29954dc0b6e2)
 Call ID: b2a3cf07-cc5d-40eb-b4d5-29954dc0b6e2
  Args:
    literal_value: 1980
    relation: :hasBirthYear
    source: Tatiana_von_Preussen
    literal_type: xsd:integer
  AssignClass (69c5df42-cf82-4d84-bdee-56181090cf3a)
 Call ID: 69c5df42-cf82-4d84-bdee-56181090cf3a
  Args:
    type: :Man
    source: Prince_Andreas_of_Prussia
  AssignClass (243e6eee-c1b9-425b-8e04-356601f2eecc)
 Call ID: 243e6eee-c1b9-425b-8e04-356601f2eecc
  Args:
    type: :Ancestor
    source: Prince_Andreas_of_Prussia
  AssignClass (4f53ea42-a152-438b-a4e9-f69edeb0d40d)
 Call ID: 4f53ea42-a152-438b-a4e9-f69edeb0d40d
  Args:
    type: :Person
    source: Prince_Andreas_of_Prussia
  AssignClass (640bcf28-8017-4f3c-a543-abde4b3061d9)
 Call ID: 640bcf28-8017-4f3c-a543-abde4b3061d9
  Args:
    type: :Woman
    source: Alexandra_Blahova
  AssignClass (b6a85d7a-272c-4d3a-8a98-8e8a74ea7f6e)
 Call ID: b6a85d7a-272c-4d3a-8a98-8e8a74ea7f6e
  Args:
    type: :Ancestor
    source: Alexandra_Blahova
  AssignClass (00be943c-39b5-4e36-8ea8-b706eaefe139)
 Call ID: 00be943c-39b5-4e36-8ea8-b706eaefe139
  Args:
    type: :Person
    source: Alexandra_Blahova
  AddTriple (06f7e09a-2556-4402-92b0-26049a80986e)
 Call ID: 06f7e09a-2556-4402-92b0-26049a80986e
  Args:
    target: Prince_Andreas_of_Prussia
    source: Tatiana_von_Preussen
    relation: :hasFather
  AddTriple (55a8a5f8-d99b-4278-b635-fda21ea9a635)
 Call ID: 55a8a5f8-d99b-4278-b635-fda21ea9a635
  Args:
    relation: :hasMother
    source: Tatiana_von_Preussen
    target: Alexandra_Blahova
  AssignClass (ce70a342-73d6-4cfa-80cf-25d356e8d6ca)
 Call ID: ce70a342-73d6-4cfa-80cf-25d356e8d6ca
  Args:
    type: :Man
    source: Prince_Frederick_of_Prussia
  AssignClass (252c2cbb-efc0-42e1-b2d3-d083c32fee6c)
 Call ID: 252c2cbb-efc0-42e1-b2d3-d083c32fee6c
  Args:
    type: :Ancestor
    source: Prince_Frederick_of_Prussia
  AssignClass (7a7400de-c98b-4ff8-9db5-af7f539772bb)
 Call ID: 7a7400de-c98b-4ff8-9db5-af7f539772bb
  Args:
    type: :Person
    source: Prince_Frederick_of_Prussia
  AssignClass (90db8df4-b912-47dc-b9cb-f0ca63f1eff6)
 Call ID: 90db8df4-b912-47dc-b9cb-f0ca63f1eff6
  Args:
    type: :Woman
    source: Lady_Brigid_Guinness
  AssignClass (8b5cc99c-a248-40f5-98ad-f7565e2cb900)
 Call ID: 8b5cc99c-a248-40f5-98ad-f7565e2cb900
  Args:
    type: :Ancestor
    source: Lady_Brigid_Guinness
  AssignClass (e8cbc30b-9207-487e-80db-f9a6fd640c5c)
 Call ID: e8cbc30b-9207-487e-80db-f9a6fd640c5c
  Args:
    type: :Person
    source: Lady_Brigid_Guinness
  AddTriple (0de46d8e-da9d-443c-b187-068f26580d23)
 Call ID: 0de46d8e-da9d-443c-b187-068f26580d23
  Args:
    source: Prince_Andreas_of_Prussia
    target: Prince_Frederick_of_Prussia
    relation: :hasFather
  AddTriple (b8e6496e-9830-45d8-8047-f932e40de4ce)
 Call ID: b8e6496e-9830-45d8-8047-f932e40de4ce
  Args:
    relation: :hasMother
    source: Prince_Andreas_of_Prussia
    target: Lady_Brigid_Guinness
  AssignClass (6d321409-f168-4409-99b2-839d4df7c4cd)
 Call ID: 6d321409-f168-4409-99b2-839d4df7c4cd
  Args:
    type: :Man
    source: Philip_Womack
  AssignClass (079c2de2-6905-4a1c-83e4-24c5e35b0f11)
 Call ID: 079c2de2-6905-4a1c-83e4-24c5e35b0f11
  Args:
    type: :Person
    source: Philip_Womack
  AddLiteral (03844827-7ea4-4030-b9c5-f0bf262a9380)
 Call ID: 03844827-7ea4-4030-b9c5-f0bf262a9380
  Args:
    source: Tatiana_von_Preussen
    literal_type: xsd:integer
    literal_value: 2014
    relation: :hasMarriageYear
  AddTriple (adf0a5a8-8833-476b-8561-3fd4635e6d98)
 Call ID: adf0a5a8-8833-476b-8561-3fd4635e6d98
  Args:
    relation: :hasRelation
    target: Philip_Womack
    source: Tatiana_von_Preussen
  AssignClass (d3b453f5-8501-4eee-8b64-c8b18088a9b6)
 Call ID: d3b453f5-8501-4eee-8b64-c8b18088a9b6
  Args:
    type: :Man
    source: Arthur_Frederick_Richard_Womack_von_Preussen
  AssignClass (731e08c1-19c1-4894-b99c-8f0c6ca345d3)
 Call ID: 731e08c1-19c1-4894-b99c-8f0c6ca345d3
  Args:
    type: :Person
    source: Arthur_Frederick_Richard_Womack_von_Preussen
  AddLiteral (e76fc8c0-a107-4954-b46a-a932ebb43d37)
 Call ID: e76fc8c0-a107-4954-b46a-a932ebb43d37
  Args:
    literal_value: 2015
    relation: :hasBirthYear
    source: Arthur_Frederick_Richard_Womack_von_Preussen
    literal_type: xsd:integer
  AddTriple (b585a689-aa77-43cd-abf8-f1ff4cf92e4c)
 Call ID: b585a689-aa77-43cd-abf8-f1ff4cf92e4c
  Args:
    source: Arthur_Frederick_Richard_Womack_von_Preussen
    target: Philip_Womack
    relation: :hasFather
  AddTriple (a5b10e0f-5287-4509-8c9d-b2457476ff1b)
 Call ID: a5b10e0f-5287-4509-8c9d-b2457476ff1b
  Args:
    relation: :hasMother
    source: Arthur_Frederick_Richard_Womack_von_Preussen
    target: Tatiana_von_Preussen
  AssignClass (fd78b7f1-47da-4566-86a5-81c4fc4ca480)
 Call ID: fd78b7f1-47da-4566-86a5-81c4fc4ca480
  Args:
    type: :Woman
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
  AssignClass (184d2ac4-df44-4ef0-92f6-4214f3066c15)
 Call ID: 184d2ac4-df44-4ef0-92f6-4214f3066c15
  Args:
    type: :Person
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
  AddLiteral (6473d61c-379f-46fe-b3c7-46fbba303aa6)
 Call ID: 6473d61c-379f-46fe-b3c7-46fbba303aa6
  Args:
    literal_type: xsd:integer
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    relation: :hasBirthYear
    literal_value: 2020
  AddTriple (9a6a2c96-2d27-4e30-8d0c-bac684ac13cc)
 Call ID: 9a6a2c96-2d27-4e30-8d0c-bac684ac13cc
  Args:
    relation: :hasFather
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    target: Philip_Womack
  AddTriple (460257b4-51fa-4798-a82a-e4f3e6d1568f)
 Call ID: 460257b4-51fa-4798-a82a-e4f3e6d1568f
  Args:
    relation: :hasMother
    source: Xenia_Alexandra_Selena_Womack_von_Preussen
    target: Tatiana_von_Preussen
  AssignClass (254db93f-5b81-411b-b733-9b40968b05b1)
 Call ID: 254db93f-5b81-411b-b733-9b40968b05b1
  Args:
    type: :Woman
    source: Amalia_Maria_Brigid_Womack_von_Preussen
  AssignClass (07bf91a9-63ec-4383-a107-3bb1f0271c4f)
 Call ID: 07bf91a9-63ec-4383-a107-3bb1f0271c4f
  Args:
    type: :Person
    source: Amalia_Maria_Brigid_Womack_von_Preussen
  AddLiteral (fe3453e3-9338-4a7e-9743-87f58ec0e4c7)
 Call ID: fe3453e3-9338-4a7e-9743-87f58ec0e4c7
  Args:
    relation: :hasBirthYear
    literal_value: 2020
    literal_type: xsd:integer
    source: Amalia_Maria_Brigid_Womack_von_Preussen
  AddTriple (47f32db1-1868-42dd-9a0a-2d6b74cc1862)
 Call ID: 47f32db1-1868-42dd-9a0a-2d6b74cc1862
  Args:
    relation: :hasFather
    source: Amalia_Maria_Brigid_Womack_von_Preussen
    target: Philip_Womack
  AddTriple (aa6f16bb-51e4-46ca-ae95-84eedf664b85)
 Call ID: aa6f16bb-51e4-46ca-ae95-84eedf664b85
  Args:
    target: Tatiana_von_Preussen
    source: Amalia_Maria_Brigid_Womack_von_Preussen
    relation: :hasMother
  Finish (8e4fcb59-5693-4498-9caa-458d152193f7)
 Call ID: 8e4fcb59-5693-4498-9caa-458d152193f7
  Args: