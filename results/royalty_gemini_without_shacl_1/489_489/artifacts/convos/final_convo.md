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
Wilhelm Karl Adalbert Erich Detloff Prinz von Preussen (30 January 1922 in Potsdam – 9 April 2007 in Holzminden) was the third son of Prince Oskar of Prussia, and the last surviving grandson of Wilhelm II, the last German Emperor.
Biography

Wilhelm-Karl was the youngest of Prince Oskar of Prussia and Countess Ina Marie von Bassewitz's four children.
Wilhelm-Karl worked tirelessly to keep the Order intact during the Cold War and helped to reunite its membership after the fall of East Germany.
Amongst other orders and awards, Wilhelm-Karl received the Grand Merit Cross (with star) of the Order of Merit of the Federal Republic of Germany and the Grand Cross of the Order pro merito Melitensi of the Sovereign Military Order of Malta.
Marriage and issue

In 1952, Wilhelm-Karl married Armgard Else Helene von Veltheim (17 February 1926 - 1 November 2019), daughter of Friedrich von Veltheim (1881–1955) and his wife, Ottonie von Alvensleben (1883–1960).



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
  AssignClass (caf80f90-6f03-4807-be91-d579ff3bb8e5)
 Call ID: caf80f90-6f03-4807-be91-d579ff3bb8e5
  Args:
    source: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    type: :Man
  AssignClass (696d44e1-e6c7-42f8-ab25-52f83ef62f88)
 Call ID: 696d44e1-e6c7-42f8-ab25-52f83ef62f88
  Args:
    source: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    type: :Person
  AddLiteral (a13d93ef-9ea4-4fba-8a81-b0b6bd148a3d)
 Call ID: a13d93ef-9ea4-4fba-8a81-b0b6bd148a3d
  Args:
    relation: :hasBirthYear
    source: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    literal_value: 1922
    literal_type: xsd:integer
  AddLiteral (70c59951-aefa-4caf-9d11-bc5dd4632226)
 Call ID: 70c59951-aefa-4caf-9d11-bc5dd4632226
  Args:
    source: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    relation: :hasDeathYear
    literal_value: 2007
    literal_type: xsd:integer
  AssignClass (7bd06718-5277-41fa-a5bb-2d65397c3b35)
 Call ID: 7bd06718-5277-41fa-a5bb-2d65397c3b35
  Args:
    type: :Man
    source: :PrinceOskarOfPrussia
  AssignClass (529544ad-d05e-422f-bf1c-443b9df8922e)
 Call ID: 529544ad-d05e-422f-bf1c-443b9df8922e
  Args:
    type: :Person
    source: :PrinceOskarOfPrussia
  AssignClass (2f82a7f4-81f6-4936-b9db-5301d016c1e5)
 Call ID: 2f82a7f4-81f6-4936-b9db-5301d016c1e5
  Args:
    type: :Woman
    source: :CountessInaMarieVonBassewitz
  AssignClass (15792be4-9dd5-44f6-9752-0532a8103bb8)
 Call ID: 15792be4-9dd5-44f6-9752-0532a8103bb8
  Args:
    type: :Person
    source: :CountessInaMarieVonBassewitz
  AddTriple (cee95293-be9b-402d-8f75-59f782614568)
 Call ID: cee95293-be9b-402d-8f75-59f782614568
  Args:
    relation: :isFatherOf
    target: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    source: :PrinceOskarOfPrussia
  AddTriple (9af55948-4f75-4bf4-9f49-729445eb9895)
 Call ID: 9af55948-4f75-4bf4-9f49-729445eb9895
  Args:
    relation: :isMotherOf
    target: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    source: :CountessInaMarieVonBassewitz
  AssignClass (213c5db3-447f-49bb-b162-329fc4faea7d)
 Call ID: 213c5db3-447f-49bb-b162-329fc4faea7d
  Args:
    source: :ArmgardElseHeleneVonVeltheim
    type: :Woman
  AssignClass (18458312-f3da-48cb-8832-e8e8c25d1e10)
 Call ID: 18458312-f3da-48cb-8832-e8e8c25d1e10
  Args:
    source: :ArmgardElseHeleneVonVeltheim
    type: :Person
  AddLiteral (9be107ce-637e-4997-9581-8feeaeb67552)
 Call ID: 9be107ce-637e-4997-9581-8feeaeb67552
  Args:
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasBirthYear
    source: :ArmgardElseHeleneVonVeltheim
  AddLiteral (0d5a79a3-da9b-410e-92be-c83ffa26082b)
 Call ID: 0d5a79a3-da9b-410e-92be-c83ffa26082b
  Args:
    literal_value: 2019
    relation: :hasDeathYear
    source: :ArmgardElseHeleneVonVeltheim
    literal_type: xsd:integer
  AddLiteral (34bb347f-1ccc-4dff-8511-9082ff0b3b39)
 Call ID: 34bb347f-1ccc-4dff-8511-9082ff0b3b39
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    literal_value: 1952
  AddTriple (ca5489a9-7522-46f9-b423-9f81f70de220)
 Call ID: ca5489a9-7522-46f9-b423-9f81f70de220
  Args:
    source: :WilhelmKarlAdalbertErichDetloffPrinzVonPreussen
    target: :ArmgardElseHeleneVonVeltheim
    relation: :hasRelation
  AssignClass (b9e9e01b-fbc7-4f8b-82b6-ab03f076c039)
 Call ID: b9e9e01b-fbc7-4f8b-82b6-ab03f076c039
  Args:
    source: :FriedrichVonVeltheim
    type: :Man
  AssignClass (05422757-cbcb-489b-b8ef-b79b6f0cb1bf)
 Call ID: 05422757-cbcb-489b-b8ef-b79b6f0cb1bf
  Args:
    source: :FriedrichVonVeltheim
    type: :Person
  AddLiteral (3abb0776-72db-4824-9174-3d954942eb4d)
 Call ID: 3abb0776-72db-4824-9174-3d954942eb4d
  Args:
    source: :FriedrichVonVeltheim
    relation: :hasBirthYear
    literal_value: 1881
    literal_type: xsd:integer
  AddLiteral (2a32e57b-ae71-4e06-b343-e14389cd08fd)
 Call ID: 2a32e57b-ae71-4e06-b343-e14389cd08fd
  Args:
    literal_type: xsd:integer
    literal_value: 1955
    relation: :hasDeathYear
    source: :FriedrichVonVeltheim
  AssignClass (0da481d3-d736-4a0a-8403-6fe26017039d)
 Call ID: 0da481d3-d736-4a0a-8403-6fe26017039d
  Args:
    source: :OttonieVonAlvensleben
    type: :Woman
  AssignClass (289cd098-032f-48eb-85b9-49287cf7f23d)
 Call ID: 289cd098-032f-48eb-85b9-49287cf7f23d
  Args:
    source: :OttonieVonAlvensleben
    type: :Person
  AddLiteral (2d650e9f-d8af-463c-9175-6a531ec9a7d1)
 Call ID: 2d650e9f-d8af-463c-9175-6a531ec9a7d1
  Args:
    literal_value: 1883
    source: :OttonieVonAlvensleben
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (6c6e574e-98a2-42df-b3b3-81c12504988e)
 Call ID: 6c6e574e-98a2-42df-b3b3-81c12504988e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :OttonieVonAlvensleben
    literal_value: 1960
  AddTriple (bcdb4340-fddf-4e06-a9f4-9ef50c3ddea0)
 Call ID: bcdb4340-fddf-4e06-a9f4-9ef50c3ddea0
  Args:
    source: :FriedrichVonVeltheim
    relation: :isFatherOf
    target: :ArmgardElseHeleneVonVeltheim
  AddTriple (272fbb46-9ebc-4557-8045-5e0f3541b209)
 Call ID: 272fbb46-9ebc-4557-8045-5e0f3541b209
  Args:
    source: :OttonieVonAlvensleben
    relation: :isMotherOf
    target: :ArmgardElseHeleneVonVeltheim
  Finish (ea0fbfd1-e747-4b14-b2b1-bb6999fc9807)
 Call ID: ea0fbfd1-e747-4b14-b2b1-bb6999fc9807
  Args: