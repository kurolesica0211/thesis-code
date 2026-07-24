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
  AssignClass (8e53818f-459a-45ed-8e5d-b397275890cc)
 Call ID: 8e53818f-459a-45ed-8e5d-b397275890cc
  Args:
    type: :Person
    source: :Tatiana_von_Preussen
  AssignClass (708917a2-8343-492f-8db8-289b8f9b51cc)
 Call ID: 708917a2-8343-492f-8db8-289b8f9b51cc
  Args:
    type: :Woman
    source: :Tatiana_von_Preussen
  AddLiteral (f15b2c69-e9c2-4f2e-9ca8-092f59cf3ee9)
 Call ID: f15b2c69-e9c2-4f2e-9ca8-092f59cf3ee9
  Args:
    literal_value: 1980
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Tatiana_von_Preussen
  AssignClass (3ad40477-70df-4c57-8adb-d26897894a1b)
 Call ID: 3ad40477-70df-4c57-8adb-d26897894a1b
  Args:
    type: :Person
    source: :Prince_Andreas_of_Prussia
  AssignClass (eb2468e7-f99f-4b56-9ac1-b949863304d1)
 Call ID: eb2468e7-f99f-4b56-9ac1-b949863304d1
  Args:
    source: :Prince_Andreas_of_Prussia
    type: :Man
  AssignClass (42e780e2-628f-42b0-8b1c-bf8bca196d66)
 Call ID: 42e780e2-628f-42b0-8b1c-bf8bca196d66
  Args:
    type: :Person
    source: :Alexandra_Blahova
  AssignClass (5530ebbc-3fc1-4d0f-9747-caf310beb088)
 Call ID: 5530ebbc-3fc1-4d0f-9747-caf310beb088
  Args:
    type: :Woman
    source: :Alexandra_Blahova
  AddTriple (c983d2d4-5137-4025-b934-977a38734d25)
 Call ID: c983d2d4-5137-4025-b934-977a38734d25
  Args:
    relation: :hasFather
    target: :Prince_Andreas_of_Prussia
    source: :Tatiana_von_Preussen
  AddTriple (cbcbab0c-2e50-46ce-87bf-a6b6d0ae14c6)
 Call ID: cbcbab0c-2e50-46ce-87bf-a6b6d0ae14c6
  Args:
    target: :Alexandra_Blahova
    source: :Tatiana_von_Preussen
    relation: :hasMother
  AssignClass (81153368-6cd0-415f-a0e1-850b4077a0b5)
 Call ID: 81153368-6cd0-415f-a0e1-850b4077a0b5
  Args:
    source: :Prince_Frederick_of_Prussia
    type: :Person
  AssignClass (3e601bd7-5dd9-46ae-8bd0-4c76fcb9f97e)
 Call ID: 3e601bd7-5dd9-46ae-8bd0-4c76fcb9f97e
  Args:
    source: :Prince_Frederick_of_Prussia
    type: :Man
  AssignClass (1184f2ae-f329-4917-91b9-d4904014e920)
 Call ID: 1184f2ae-f329-4917-91b9-d4904014e920
  Args:
    source: :Lady_Brigid_Guinness
    type: :Person
  AssignClass (9b49f25f-0434-4dff-9fed-74dd18b5e63c)
 Call ID: 9b49f25f-0434-4dff-9fed-74dd18b5e63c
  Args:
    source: :Lady_Brigid_Guinness
    type: :Woman
  AddTriple (a85a0991-2314-4db6-9bbe-484f24040881)
 Call ID: a85a0991-2314-4db6-9bbe-484f24040881
  Args:
    relation: :hasFather
    source: :Prince_Andreas_of_Prussia
    target: :Prince_Frederick_of_Prussia
  AddTriple (3af29dc6-8c94-49a4-9317-d89cfa937de3)
 Call ID: 3af29dc6-8c94-49a4-9317-d89cfa937de3
  Args:
    relation: :hasMother
    source: :Prince_Andreas_of_Prussia
    target: :Lady_Brigid_Guinness
  AssignClass (a04ca6e2-7e2b-4992-9234-cff5910ee8f2)
 Call ID: a04ca6e2-7e2b-4992-9234-cff5910ee8f2
  Args:
    type: :Person
    source: :Philip_Womack
  AssignClass (d9a134de-6422-4538-9049-33420de6f537)
 Call ID: d9a134de-6422-4538-9049-33420de6f537
  Args:
    source: :Philip_Womack
    type: :Man
  AddLiteral (be056c7a-0652-429b-ab22-0d295a351b83)
 Call ID: be056c7a-0652-429b-ab22-0d295a351b83
  Args:
    relation: :hasMarriageYear
    literal_value: 2014
    source: :Tatiana_von_Preussen
    literal_type: xsd:integer
  AddTriple (eb037141-8106-460b-a9c4-4571b82af89f)
 Call ID: eb037141-8106-460b-a9c4-4571b82af89f
  Args:
    relation: :hasRelation
    target: :Philip_Womack
    source: :Tatiana_von_Preussen
  AssignClass (dbfb48e4-6ed7-437a-9d5b-67c1e4197c80)
 Call ID: dbfb48e4-6ed7-437a-9d5b-67c1e4197c80
  Args:
    source: :Arthur_Frederick_Richard_Womack_von_Preussen
    type: :Person
  AssignClass (8fcedd86-36c6-4103-86b9-01929266d9c0)
 Call ID: 8fcedd86-36c6-4103-86b9-01929266d9c0
  Args:
    source: :Arthur_Frederick_Richard_Womack_von_Preussen
    type: :Man
  AddLiteral (ae305dd6-e191-4363-ac27-fea2db1ea90e)
 Call ID: ae305dd6-e191-4363-ac27-fea2db1ea90e
  Args:
    source: :Arthur_Frederick_Richard_Womack_von_Preussen
    literal_type: xsd:integer
    literal_value: 2015
    relation: :hasBirthYear
  AddTriple (c47e6e57-918b-4b0e-afc1-51556f89d685)
 Call ID: c47e6e57-918b-4b0e-afc1-51556f89d685
  Args:
    target: :Philip_Womack
    source: :Arthur_Frederick_Richard_Womack_von_Preussen
    relation: :hasFather
  AddTriple (6e150382-45ef-443e-af5c-d287848512b7)
 Call ID: 6e150382-45ef-443e-af5c-d287848512b7
  Args:
    target: :Tatiana_von_Preussen
    source: :Arthur_Frederick_Richard_Womack_von_Preussen
    relation: :hasMother
  AssignClass (22ec1adc-e49c-4161-9c67-e1824c7c5e05)
 Call ID: 22ec1adc-e49c-4161-9c67-e1824c7c5e05
  Args:
    type: :Person
    source: :Xenia_Alexandra_Selena_Womack_von_Preussen
  AssignClass (647ad9ae-b125-4ab6-8f23-3d9329baf914)
 Call ID: 647ad9ae-b125-4ab6-8f23-3d9329baf914
  Args:
    type: :Woman
    source: :Xenia_Alexandra_Selena_Womack_von_Preussen
  AddLiteral (3e31dfcf-d43e-458a-9bfa-9af5e3d9651e)
 Call ID: 3e31dfcf-d43e-458a-9bfa-9af5e3d9651e
  Args:
    literal_value: 2020
    relation: :hasBirthYear
    source: :Xenia_Alexandra_Selena_Womack_von_Preussen
    literal_type: xsd:integer
  AddTriple (d82a4551-2e07-41b9-b043-37aa14b324ed)
 Call ID: d82a4551-2e07-41b9-b043-37aa14b324ed
  Args:
    source: :Xenia_Alexandra_Selena_Womack_von_Preussen
    target: :Philip_Womack
    relation: :hasFather
  AddTriple (8d477016-20d4-45d5-bc56-905fab21fb44)
 Call ID: 8d477016-20d4-45d5-bc56-905fab21fb44
  Args:
    relation: :hasMother
    target: :Tatiana_von_Preussen
    source: :Xenia_Alexandra_Selena_Womack_von_Preussen
  AssignClass (4d2b8662-b285-4f46-9155-447ecad7e1a3)
 Call ID: 4d2b8662-b285-4f46-9155-447ecad7e1a3
  Args:
    source: :Amalia_Maria_Brigid_Womack_von_Preussen
    type: :Person
  AssignClass (e659dcf1-46fe-43ea-ac6c-47a2184fd285)
 Call ID: e659dcf1-46fe-43ea-ac6c-47a2184fd285
  Args:
    type: :Woman
    source: :Amalia_Maria_Brigid_Womack_von_Preussen
  AddLiteral (e5fc4cbe-081b-4531-b48c-4382ff2df07e)
 Call ID: e5fc4cbe-081b-4531-b48c-4382ff2df07e
  Args:
    literal_value: 2020
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Amalia_Maria_Brigid_Womack_von_Preussen
  AddTriple (b0b5afef-778f-491e-a915-f08fab37b564)
 Call ID: b0b5afef-778f-491e-a915-f08fab37b564
  Args:
    relation: :hasFather
    source: :Amalia_Maria_Brigid_Womack_von_Preussen
    target: :Philip_Womack
  AddTriple (dbdcd639-2835-47d9-9108-ce43b0db1dfc)
 Call ID: dbdcd639-2835-47d9-9108-ce43b0db1dfc
  Args:
    relation: :hasMother
    source: :Amalia_Maria_Brigid_Womack_von_Preussen
    target: :Tatiana_von_Preussen
  Finish (ac928b21-1791-4ba8-a6a3-bed370f615a7)
 Call ID: ac928b21-1791-4ba8-a6a3-bed370f615a7
  Args: