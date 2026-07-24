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
Princess Alexandrine Irene of Prussia (7 April 1915 – 2 October 1980) was the elder daughter and fifth child of Wilhelm, German Crown Prince, and Cecilie of Mecklenburg-Schwerin.
Her grandparents were Wilhelm II, German Emperor and his wife Augusta Victoria of Schleswig-Holstein, and Frederick Francis III of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
Alexandrine was a member of the House of Hohenzollern.
She was a great-great-granddaughter of Queen Victoria.
Life

Alexandrine was born at the Kronprinzenpalais in Berlin.
She followed older brothers Wilhelm, Louis Ferdinand, Hubertus, and Frederick.
Alexandrine's only sister, Cecilie, was born in 1917.
It became clear shortly after Alexandrine's birth that she had Down syndrome.
Unlike other disabled royal children, Alexandrine was not hidden away.
As a teenager, Alexandrine attended the Trüpersche Sonderschule, a school dedicated to the education of children with special needs.
Alexandrine celebrated her confirmation along with her sister Cecilie in October 1934.
Alexandrine lived most of her later life in Bavaria, first in Pöcking and later near Lake Starnberg, where she was visited there regularly by her family, particularly her brother Louis Ferdinand.
Alexandrine died on 2 October 1980.
She was buried near her parents and brother Frederick at Hohenzollern Castle.



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
  AssignClass (49c5cc81-7e7e-4bab-80d3-83bd9643477c)
 Call ID: 49c5cc81-7e7e-4bab-80d3-83bd9643477c
  Args:
    type: :Woman
    source: Alexandrine_of_Prussia
  AssignClass (57a6d190-9f02-40bc-8bc7-ac5b4f66e9e0)
 Call ID: 57a6d190-9f02-40bc-8bc7-ac5b4f66e9e0
  Args:
    type: :Person
    source: Alexandrine_of_Prussia
  AddLiteral (ae788867-c6de-4f66-bf0a-81ba216003be)
 Call ID: ae788867-c6de-4f66-bf0a-81ba216003be
  Args:
    source: Alexandrine_of_Prussia
    literal_value: 1915
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4d9b136f-4794-42f4-b72d-a8b92136c2b9)
 Call ID: 4d9b136f-4794-42f4-b72d-a8b92136c2b9
  Args:
    source: Alexandrine_of_Prussia
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1980
  AssignClass (e2b529c4-7ff5-49f3-a043-525e0707e3c0)
 Call ID: e2b529c4-7ff5-49f3-a043-525e0707e3c0
  Args:
    source: Wilhelm_German_Crown_Prince
    type: :Man
  AssignClass (b96e3cbd-aa78-4aec-8b07-ba44a78d3b1f)
 Call ID: b96e3cbd-aa78-4aec-8b07-ba44a78d3b1f
  Args:
    type: :Ancestor
    source: Wilhelm_German_Crown_Prince
  AssignClass (0d62e46e-e5a4-4f55-9670-a25076d590ea)
 Call ID: 0d62e46e-e5a4-4f55-9670-a25076d590ea
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (febdc853-e0bb-4d52-b072-1a967ec252aa)
 Call ID: febdc853-e0bb-4d52-b072-1a967ec252aa
  Args:
    source: Cecilie_of_Mecklenburg-Schwerin
    type: :Ancestor
  AddTriple (864815e0-2fe6-406c-9f86-69de771f6f08)
 Call ID: 864815e0-2fe6-406c-9f86-69de771f6f08
  Args:
    relation: :hasFather
    source: Alexandrine_of_Prussia
    target: Wilhelm_German_Crown_Prince
  AddTriple (23f45944-514c-4011-aa98-9d7430e83d16)
 Call ID: 23f45944-514c-4011-aa98-9d7430e83d16
  Args:
    source: Alexandrine_of_Prussia
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (99619c6a-c98a-4aea-bedd-f6963c5c7f1b)
 Call ID: 99619c6a-c98a-4aea-bedd-f6963c5c7f1b
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (b217243f-83e3-4d46-8865-ae8eec4a3498)
 Call ID: b217243f-83e3-4d46-8865-ae8eec4a3498
  Args:
    type: :Ancestor
    source: Wilhelm_II_German_Emperor
  AssignClass (cb1e2e43-5d98-4629-8b73-6c76b3b39f48)
 Call ID: cb1e2e43-5d98-4629-8b73-6c76b3b39f48
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (4fd6128a-4ba1-4efe-8fff-6a225dc74be6)
 Call ID: 4fd6128a-4ba1-4efe-8fff-6a225dc74be6
  Args:
    type: :Ancestor
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (60998a00-efe4-4632-9ba2-240973c14393)
 Call ID: 60998a00-efe4-4632-9ba2-240973c14393
  Args:
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (4f4b4436-4ae6-4366-aee7-81eb0ff3e769)
 Call ID: 4f4b4436-4ae6-4366-aee7-81eb0ff3e769
  Args:
    type: :Ancestor
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (b3764837-ebb3-48c8-8c4c-7dd38eead8a7)
 Call ID: b3764837-ebb3-48c8-8c4c-7dd38eead8a7
  Args:
    source: Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (71ce6ac7-b145-4ca3-a426-c6a120b80722)
 Call ID: 71ce6ac7-b145-4ca3-a426-c6a120b80722
  Args:
    type: :Ancestor
    source: Anastasia_Mikhailovna_of_Russia
  AddTriple (8d7f3303-f7de-436e-85f3-5ea574aa5572)
 Call ID: 8d7f3303-f7de-436e-85f3-5ea574aa5572
  Args:
    relation: :hasParent
    target: Wilhelm_II_German_Emperor
    source: Wilhelm_German_Crown_Prince
  AddTriple (465c684e-bdd2-4064-9761-f637d15c2a51)
 Call ID: 465c684e-bdd2-4064-9761-f637d15c2a51
  Args:
    relation: :hasParent
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: Wilhelm_German_Crown_Prince
  AddTriple (19e71360-eed2-4219-b162-b6147860cd85)
 Call ID: 19e71360-eed2-4219-b162-b6147860cd85
  Args:
    relation: :hasParent
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (1150c51a-b663-49f8-b56d-8b60188acc22)
 Call ID: 1150c51a-b663-49f8-b56d-8b60188acc22
  Args:
    relation: :hasParent
    source: Cecilie_of_Mecklenburg-Schwerin
    target: Anastasia_Mikhailovna_of_Russia
  AssignClass (cb7e7b5c-36fb-44f9-ab77-bd437b20d2fb)
 Call ID: cb7e7b5c-36fb-44f9-ab77-bd437b20d2fb
  Args:
    type: :Man
    source: Wilhelm_brother
  AssignClass (ccb16513-fc4f-4efd-b303-c3f1a0dd3462)
 Call ID: ccb16513-fc4f-4efd-b303-c3f1a0dd3462
  Args:
    type: :Person
    source: Wilhelm_brother
  AssignClass (6ca070ac-edda-4ab8-ab0c-91159be2519d)
 Call ID: 6ca070ac-edda-4ab8-ab0c-91159be2519d
  Args:
    source: Louis_Ferdinand
    type: :Man
  AssignClass (a504aa9d-10a3-4c4f-80b6-5d5a8e44894f)
 Call ID: a504aa9d-10a3-4c4f-80b6-5d5a8e44894f
  Args:
    type: :Person
    source: Louis_Ferdinand
  AssignClass (19adfc3b-6235-4f79-ae00-ed371ec1e0e6)
 Call ID: 19adfc3b-6235-4f79-ae00-ed371ec1e0e6
  Args:
    type: :Man
    source: Hubertus
  AssignClass (c2b59d3e-1bcd-41a0-86ab-762fb4bfd713)
 Call ID: c2b59d3e-1bcd-41a0-86ab-762fb4bfd713
  Args:
    source: Hubertus
    type: :Person
  AssignClass (e7a901b9-d8cb-463f-bdb3-6a5e5ec9eef9)
 Call ID: e7a901b9-d8cb-463f-bdb3-6a5e5ec9eef9
  Args:
    source: Frederick_brother
    type: :Man
  AssignClass (68401d8a-7d16-4db0-82a7-c23345e8783b)
 Call ID: 68401d8a-7d16-4db0-82a7-c23345e8783b
  Args:
    type: :Person
    source: Frederick_brother
  AssignClass (415322ef-e130-4412-8e87-f480087e9d78)
 Call ID: 415322ef-e130-4412-8e87-f480087e9d78
  Args:
    source: Cecilie_sister
    type: :Woman
  AssignClass (43b5d332-d69f-4619-9fff-15f83dc6d2d8)
 Call ID: 43b5d332-d69f-4619-9fff-15f83dc6d2d8
  Args:
    type: :Person
    source: Cecilie_sister
  AddTriple (f21fcd3e-0c0c-484b-87b8-37cbc512c9cf)
 Call ID: f21fcd3e-0c0c-484b-87b8-37cbc512c9cf
  Args:
    source: Alexandrine_of_Prussia
    target: Wilhelm_brother
    relation: :isSiblingOf
  AddTriple (bdd04a73-cf42-468a-a3c0-f641e6bd2975)
 Call ID: bdd04a73-cf42-468a-a3c0-f641e6bd2975
  Args:
    relation: :isSiblingOf
    target: Louis_Ferdinand
    source: Alexandrine_of_Prussia
  AddTriple (7df1e46d-05d2-40a4-b070-542b13192c4a)
 Call ID: 7df1e46d-05d2-40a4-b070-542b13192c4a
  Args:
    relation: :isSiblingOf
    target: Hubertus
    source: Alexandrine_of_Prussia
  AddTriple (98d84ea4-1f03-4de0-9da6-d325a43d5a7d)
 Call ID: 98d84ea4-1f03-4de0-9da6-d325a43d5a7d
  Args:
    relation: :isSiblingOf
    target: Frederick_brother
    source: Alexandrine_of_Prussia
  AddTriple (6e07e202-898a-419c-80ca-3a57197a9240)
 Call ID: 6e07e202-898a-419c-80ca-3a57197a9240
  Args:
    relation: :isSiblingOf
    source: Alexandrine_of_Prussia
    target: Cecilie_sister
  Finish (662ff76c-cc01-4d66-adcb-ba27d266bc92)
 Call ID: 662ff76c-cc01-4d66-adcb-ba27d266bc92
  Args: