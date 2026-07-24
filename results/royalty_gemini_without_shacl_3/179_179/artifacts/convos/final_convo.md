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
Princess Isabel Alfonsa of Bourbon-Two Sicilies, Infanta of Spain, (Isabel Alfonsa María Teresa Antonia Cristina Mercedes Carolina Adelaida Rafaela de Borbón-Dos Sicilias y Borbón; 16 October 1904 – 18 July 1985) was a member of the House of Bourbon-Two Sicilies and a princess of Bourbon-Two Sicilies by birth.
Family

Isabel Alfonsa was the third child of Prince Carlos of Bourbon-Two Sicilies and his first wife María de las Mercedes, Princess of Asturias.
Isabel Alfonsa's maternal grandparents were Alfonso XII of Spain and Maria Christina of Austria.
Marriage and issue

Isabel Alfonsa married her first cousin once removed Count Jan Kanty Zamoyski, seventh child and third son of Count Andrzej Zamoyski and his wife Princess Maria Carolina of Bourbon-Two Sicilies, on 9 March 1929 in Madrid.



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
  AssignClass (ac38ac26-69a1-45c6-848c-ae79e486abdc)
 Call ID: ac38ac26-69a1-45c6-848c-ae79e486abdc
  Args:
    type: :Person
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
  AssignClass (fa3e0253-f0b5-416a-ad92-94cf640c4c47)
 Call ID: fa3e0253-f0b5-416a-ad92-94cf640c4c47
  Args:
    type: :Woman
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
  AddLiteral (8df37ba9-43e9-49fb-a9c9-f7cfe6dc6808)
 Call ID: 8df37ba9-43e9-49fb-a9c9-f7cfe6dc6808
  Args:
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    literal_value: 1904
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4e3a24ea-d670-43c3-91c2-a449297558d4)
 Call ID: 4e3a24ea-d670-43c3-91c2-a449297558d4
  Args:
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    literal_value: 1985
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (ee39ec9d-b5b3-4d26-a6da-931e5a02b1b1)
 Call ID: ee39ec9d-b5b3-4d26-a6da-931e5a02b1b1
  Args:
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (0f08d902-2b5a-4bd5-ac91-80e7848209ef)
 Call ID: 0f08d902-2b5a-4bd5-ac91-80e7848209ef
  Args:
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (41faa7ba-86a9-4ed7-b381-7d9960f04d19)
 Call ID: 41faa7ba-86a9-4ed7-b381-7d9960f04d19
  Args:
    source: Maria_de_las_Mercedes_Princess_of_Asturias
    type: :Person
  AssignClass (883f90ab-61f9-4e74-83dd-bafc73aa2950)
 Call ID: 883f90ab-61f9-4e74-83dd-bafc73aa2950
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_Princess_of_Asturias
  AddTriple (cc090a1b-62ad-407e-83ea-be293b4104c7)
 Call ID: cc090a1b-62ad-407e-83ea-be293b4104c7
  Args:
    relation: :hasFather
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
  AddTriple (79a8d6b3-6b2d-419e-a3b0-da13ff407605)
 Call ID: 79a8d6b3-6b2d-419e-a3b0-da13ff407605
  Args:
    target: Maria_de_las_Mercedes_Princess_of_Asturias
    relation: :hasMother
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
  AssignClass (60c4b4f5-28ba-4989-ab70-6c95ef123bb0)
 Call ID: 60c4b4f5-28ba-4989-ab70-6c95ef123bb0
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (8cab1650-b337-475e-b276-f1f7723dd9b0)
 Call ID: 8cab1650-b337-475e-b276-f1f7723dd9b0
  Args:
    source: Alfonso_XII_of_Spain
    type: :Man
  AssignClass (979d7e6b-2dc1-4c8d-b3a3-d9d165672a67)
 Call ID: 979d7e6b-2dc1-4c8d-b3a3-d9d165672a67
  Args:
    source: Maria_Christina_of_Austria
    type: :Person
  AssignClass (29cd908f-1e40-4cd7-9912-0cc394379a51)
 Call ID: 29cd908f-1e40-4cd7-9912-0cc394379a51
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AddTriple (0248a3f5-b238-4f4e-9650-763ddf6a611e)
 Call ID: 0248a3f5-b238-4f4e-9650-763ddf6a611e
  Args:
    source: Maria_de_las_Mercedes_Princess_of_Asturias
    target: Alfonso_XII_of_Spain
    relation: :hasFather
  AddTriple (ccc5e37e-25eb-4967-8df0-f924d0f3ef0b)
 Call ID: ccc5e37e-25eb-4967-8df0-f924d0f3ef0b
  Args:
    source: Maria_de_las_Mercedes_Princess_of_Asturias
    relation: :hasMother
    target: Maria_Christina_of_Austria
  AssignClass (97778fcd-5cfe-4443-9514-dee0534fe5b6)
 Call ID: 97778fcd-5cfe-4443-9514-dee0534fe5b6
  Args:
    type: :Person
    source: Jan_Kanty_Zamoyski
  AssignClass (c7ec4ba2-6acb-44b5-96da-f40bd53cc1a6)
 Call ID: c7ec4ba2-6acb-44b5-96da-f40bd53cc1a6
  Args:
    source: Jan_Kanty_Zamoyski
    type: :Man
  AddTriple (73242d5d-bf9a-467b-abf5-aa901e31cd29)
 Call ID: 73242d5d-bf9a-467b-abf5-aa901e31cd29
  Args:
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Jan_Kanty_Zamoyski
  AddLiteral (7a188c41-d776-4aad-9fed-dbc3c559df74)
 Call ID: 7a188c41-d776-4aad-9fed-dbc3c559df74
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    literal_value: 1929
  AssignClass (df4454d9-9081-4984-b307-5301e123ad20)
 Call ID: df4454d9-9081-4984-b307-5301e123ad20
  Args:
    type: :Person
    source: Andrzej_Zamoyski
  AssignClass (984be2b0-13ab-432c-8713-17abc72275b5)
 Call ID: 984be2b0-13ab-432c-8713-17abc72275b5
  Args:
    type: :Man
    source: Andrzej_Zamoyski
  AssignClass (21ef5e90-ea21-4afa-8de1-844c0cf1bbf7)
 Call ID: 21ef5e90-ea21-4afa-8de1-844c0cf1bbf7
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (f43c5d8b-16ee-47a9-a129-6b2efc5c848c)
 Call ID: f43c5d8b-16ee-47a9-a129-6b2efc5c848c
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    type: :Woman
  AddTriple (55c94015-72b6-477a-9308-6dc4d888af69)
 Call ID: 55c94015-72b6-477a-9308-6dc4d888af69
  Args:
    target: Andrzej_Zamoyski
    relation: :hasFather
    source: Jan_Kanty_Zamoyski
  AddTriple (562258c4-4fda-46fa-a0f2-f689979870d2)
 Call ID: 562258c4-4fda-46fa-a0f2-f689979870d2
  Args:
    source: Jan_Kanty_Zamoyski
    target: Maria_Carolina_of_Bourbon-Two_Sicilies
    relation: :hasMother
  Finish (f68b47f0-4b0a-4265-bec5-8e9df538f4d3)
 Call ID: f68b47f0-4b0a-4265-bec5-8e9df538f4d3
  Args: