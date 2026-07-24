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
  AssignClass (b8aa9b14-4476-42f8-beef-4785b8f345c7)
 Call ID: b8aa9b14-4476-42f8-beef-4785b8f345c7
  Args:
    type: :Woman
    source: :PrincessKiraOfPrussia
  AssignClass (5cdecc9b-3ea6-46f2-93e3-77647f401ef2)
 Call ID: 5cdecc9b-3ea6-46f2-93e3-77647f401ef2
  Args:
    type: :Person
    source: :PrincessKiraOfPrussia
  AddLiteral (d8ee25cb-ebe1-4584-8951-ef21170c2afb)
 Call ID: d8ee25cb-ebe1-4584-8951-ef21170c2afb
  Args:
    literal_value: 1943
    source: :PrincessKiraOfPrussia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (fc90cbfd-d722-4c9d-8f8e-f0ffea4531f5)
 Call ID: fc90cbfd-d722-4c9d-8f8e-f0ffea4531f5
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :PrincessKiraOfPrussia
    literal_value: 2004
  AssignClass (7d9fd49f-4adf-423a-a14f-bff2c399a5c3)
 Call ID: 7d9fd49f-4adf-423a-a14f-bff2c399a5c3
  Args:
    source: :LouisFerdinandPrinceOfPrussia
    type: :Man
  AssignClass (55fc1215-b8c4-4412-9459-776b866923c8)
 Call ID: 55fc1215-b8c4-4412-9459-776b866923c8
  Args:
    type: :Person
    source: :LouisFerdinandPrinceOfPrussia
  AssignClass (5ebf3291-d1e9-4e7c-8648-122c4437d5bd)
 Call ID: 5ebf3291-d1e9-4e7c-8648-122c4437d5bd
  Args:
    source: :GrandDuchessKiraKirillovnaOfRussia
    type: :Woman
  AssignClass (01d0b968-5a39-4386-a15d-6c745f58f570)
 Call ID: 01d0b968-5a39-4386-a15d-6c745f58f570
  Args:
    type: :Person
    source: :GrandDuchessKiraKirillovnaOfRussia
  AddTriple (4ca4ed9c-162c-4ec6-89a5-af9b02707416)
 Call ID: 4ca4ed9c-162c-4ec6-89a5-af9b02707416
  Args:
    target: :LouisFerdinandPrinceOfPrussia
    source: :PrincessKiraOfPrussia
    relation: :hasFather
  AddTriple (998ad66e-27f0-40ce-ab66-3b7843a87674)
 Call ID: 998ad66e-27f0-40ce-ab66-3b7843a87674
  Args:
    target: :GrandDuchessKiraKirillovnaOfRussia
    relation: :hasMother
    source: :PrincessKiraOfPrussia
  AssignClass (4680c26d-f86e-46d5-b215-3b3f12ddb7f8)
 Call ID: 4680c26d-f86e-46d5-b215-3b3f12ddb7f8
  Args:
    source: :KiraMarinaLiepsner
    type: :Woman
  AssignClass (405db416-7128-4d58-a36b-8cf268b3417a)
 Call ID: 405db416-7128-4d58-a36b-8cf268b3417a
  Args:
    type: :Person
    source: :KiraMarinaLiepsner
  AddLiteral (1d555ea1-ed28-41a2-b318-4354c8fff579)
 Call ID: 1d555ea1-ed28-41a2-b318-4354c8fff579
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1977
    source: :KiraMarinaLiepsner
  AddTriple (595b9cbf-42e8-400a-abdd-1ce2e1c8044f)
 Call ID: 595b9cbf-42e8-400a-abdd-1ce2e1c8044f
  Args:
    target: :PrincessKiraOfPrussia
    source: :KiraMarinaLiepsner
    relation: :hasMother
  AssignClass (92a7dfff-d9db-456d-91b4-1b433c798204)
 Call ID: 92a7dfff-d9db-456d-91b4-1b433c798204
  Args:
    type: :Man
    source: :AndreasFelixPaulVonBismarck
  AssignClass (b4fd8c6d-3028-4c8d-af56-125d7b08de64)
 Call ID: b4fd8c6d-3028-4c8d-af56-125d7b08de64
  Args:
    type: :Person
    source: :AndreasFelixPaulVonBismarck
  AddLiteral (ae543a42-4324-4921-8af0-4aa9757a745a)
 Call ID: ae543a42-4324-4921-8af0-4aa9757a745a
  Args:
    literal_value: 1979
    source: :AndreasFelixPaulVonBismarck
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (d6d87d3d-128d-4981-931b-ddfaf7d0b84d)
 Call ID: d6d87d3d-128d-4981-931b-ddfaf7d0b84d
  Args:
    source: :AndreasFelixPaulVonBismarck
    literal_value: 2019
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (bf983b45-3589-4334-9488-4ac162dfa8bc)
 Call ID: bf983b45-3589-4334-9488-4ac162dfa8bc
  Args:
    target: :AndreasFelixPaulVonBismarck
    source: :KiraMarinaLiepsner
    relation: :hasRelation
  AddTriple (3aa880ef-9572-465e-85dc-bf6367bc0a48)
 Call ID: 3aa880ef-9572-465e-85dc-bf6367bc0a48
  Args:
    target: :AndreasFelixPaulVonBismarck
    relation: :hasFather
    source: :Granddaughter1OfKiraMarina
  AddTriple (847cb21d-774c-4ab1-8824-a39bb0745298)
 Call ID: 847cb21d-774c-4ab1-8824-a39bb0745298
  Args:
    target: :KiraMarinaLiepsner
    relation: :hasMother
    source: :Granddaughter1OfKiraMarina
  AddTriple (763880bc-0342-4b05-84e8-f439ee9d7748)
 Call ID: 763880bc-0342-4b05-84e8-f439ee9d7748
  Args:
    source: :Granddaughter2OfKiraMarina
    relation: :hasFather
    target: :AndreasFelixPaulVonBismarck
  AddTriple (ddc1f7d4-dbe5-40a2-8d5b-d53705f8270f)
 Call ID: ddc1f7d4-dbe5-40a2-8d5b-d53705f8270f
  Args:
    source: :Granddaughter2OfKiraMarina
    relation: :hasMother
    target: :KiraMarinaLiepsner
  AssignClass (d4919708-1287-46e1-b36e-1dae45097cf7)
 Call ID: d4919708-1287-46e1-b36e-1dae45097cf7
  Args:
    type: :Woman
    source: :Granddaughter1OfKiraMarina
  AssignClass (d918b2d1-951f-4b27-951f-24486b17a01e)
 Call ID: d918b2d1-951f-4b27-951f-24486b17a01e
  Args:
    type: :Person
    source: :Granddaughter1OfKiraMarina
  AssignClass (3178a8b3-3e1e-47ae-8cb1-abec6b31766e)
 Call ID: 3178a8b3-3e1e-47ae-8cb1-abec6b31766e
  Args:
    source: :Granddaughter2OfKiraMarina
    type: :Woman
  AssignClass (5fb545af-3c8c-48a6-b6f3-c8082fcf6969)
 Call ID: 5fb545af-3c8c-48a6-b6f3-c8082fcf6969
  Args:
    type: :Person
    source: :Granddaughter2OfKiraMarina
  Finish (fb7da619-1e8a-4542-b81e-95e89946490a)
 Call ID: fb7da619-1e8a-4542-b81e-95e89946490a
  Args: