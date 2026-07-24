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
  AssignClass (68e1c192-12be-4e71-87de-30b6fedf406d)
 Call ID: 68e1c192-12be-4e71-87de-30b6fedf406d
  Args:
    type: :Person
    source: :Alexandrine_of_Prussia
  AssignClass (1bd5ef95-a982-47a2-9e87-21b0b78322d0)
 Call ID: 1bd5ef95-a982-47a2-9e87-21b0b78322d0
  Args:
    type: :Woman
    source: :Alexandrine_of_Prussia
  AddLiteral (4037effe-fc01-48db-b8f2-f6c761b88dc6)
 Call ID: 4037effe-fc01-48db-b8f2-f6c761b88dc6
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1915
    relation: :hasBirthYear
    source: :Alexandrine_of_Prussia
  AddLiteral (c84e65ac-0976-40d0-afa5-8aef1eb5d2b4)
 Call ID: c84e65ac-0976-40d0-afa5-8aef1eb5d2b4
  Args:
    source: :Alexandrine_of_Prussia
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1980
  AssignClass (6b867fea-8b7a-4acf-afca-35de0bda8de2)
 Call ID: 6b867fea-8b7a-4acf-afca-35de0bda8de2
  Args:
    type: :Person
    source: :Wilhelm_German_Crown_Prince
  AssignClass (b44cbbf6-5b25-4fcc-a2d1-d5c08bced763)
 Call ID: b44cbbf6-5b25-4fcc-a2d1-d5c08bced763
  Args:
    type: :Man
    source: :Wilhelm_German_Crown_Prince
  AssignClass (b1b6a763-9776-4848-a547-b7d5fbfa2925)
 Call ID: b1b6a763-9776-4848-a547-b7d5fbfa2925
  Args:
    type: :Person
    source: :Cecilie_of_Mecklenburg-Schwerin
  AssignClass (b49c7c5a-052c-434d-945e-34d2d5bcba19)
 Call ID: b49c7c5a-052c-434d-945e-34d2d5bcba19
  Args:
    type: :Woman
    source: :Cecilie_of_Mecklenburg-Schwerin
  AddTriple (a5314a4e-61e9-464a-b3c7-4637a7059d12)
 Call ID: a5314a4e-61e9-464a-b3c7-4637a7059d12
  Args:
    target: :Wilhelm_German_Crown_Prince
    relation: :hasFather
    source: :Alexandrine_of_Prussia
  AddTriple (8105430a-1523-4945-8c62-5c13ab3bc0f4)
 Call ID: 8105430a-1523-4945-8c62-5c13ab3bc0f4
  Args:
    source: :Alexandrine_of_Prussia
    relation: :hasMother
    target: :Cecilie_of_Mecklenburg-Schwerin
  AssignClass (c6e38409-e6a6-4dd3-819b-bf4b8a4b7ecc)
 Call ID: c6e38409-e6a6-4dd3-819b-bf4b8a4b7ecc
  Args:
    type: :Person
    source: :Wilhelm_II
  AssignClass (156d9fed-d2ec-4554-987f-41c46574bc49)
 Call ID: 156d9fed-d2ec-4554-987f-41c46574bc49
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (29715f65-b5e1-47c1-ab99-e2ef965134d5)
 Call ID: 29715f65-b5e1-47c1-ab99-e2ef965134d5
  Args:
    type: :Person
    source: :Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (77a33e7b-fe5d-48b2-bf39-72236a7f6f48)
 Call ID: 77a33e7b-fe5d-48b2-bf39-72236a7f6f48
  Args:
    type: :Woman
    source: :Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (fdf5f2a7-6f32-4ae9-971e-60642569ff8b)
 Call ID: fdf5f2a7-6f32-4ae9-971e-60642569ff8b
  Args:
    type: :Person
    source: :Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (7aab8cb4-5c2c-4900-94b2-e59e899025ac)
 Call ID: 7aab8cb4-5c2c-4900-94b2-e59e899025ac
  Args:
    type: :Man
    source: :Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (fb673df2-e181-4b31-b726-0962c4171f30)
 Call ID: fb673df2-e181-4b31-b726-0962c4171f30
  Args:
    type: :Person
    source: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AssignClass (75860218-00cb-493e-850b-589017ff3e70)
 Call ID: 75860218-00cb-493e-850b-589017ff3e70
  Args:
    type: :Woman
    source: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AddTriple (9da4e7d9-973b-44c8-bd18-1f9e3c8d0437)
 Call ID: 9da4e7d9-973b-44c8-bd18-1f9e3c8d0437
  Args:
    relation: :hasFather
    source: :Wilhelm_German_Crown_Prince
    target: :Wilhelm_II
  AddTriple (7be43a6b-6e0d-4947-a3dc-d6071051e184)
 Call ID: 7be43a6b-6e0d-4947-a3dc-d6071051e184
  Args:
    target: :Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
    source: :Wilhelm_German_Crown_Prince
  AddTriple (8a6c13f4-2fbc-48ab-8698-83e150e7f101)
 Call ID: 8a6c13f4-2fbc-48ab-8698-83e150e7f101
  Args:
    relation: :hasFather
    source: :Cecilie_of_Mecklenburg-Schwerin
    target: :Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (c74a0e98-22d0-4480-a2de-32f87d43d942)
 Call ID: c74a0e98-22d0-4480-a2de-32f87d43d942
  Args:
    target: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    source: :Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (70d0d8d6-304f-4cac-9744-faecc82d5663)
 Call ID: 70d0d8d6-304f-4cac-9744-faecc82d5663
  Args:
    type: :Person
    source: :Wilhelm_brother
  AssignClass (22482cf4-cc50-413b-9b02-0556c7abff4b)
 Call ID: 22482cf4-cc50-413b-9b02-0556c7abff4b
  Args:
    type: :Man
    source: :Wilhelm_brother
  AssignClass (102d86d8-bfe1-4508-b400-9414b7d22cd8)
 Call ID: 102d86d8-bfe1-4508-b400-9414b7d22cd8
  Args:
    type: :Person
    source: :Louis_Ferdinand
  AssignClass (e94aa155-5049-4fe5-9174-25be988148f0)
 Call ID: e94aa155-5049-4fe5-9174-25be988148f0
  Args:
    type: :Man
    source: :Louis_Ferdinand
  AssignClass (7bd5eb84-2717-482f-bfda-c79f798cfc91)
 Call ID: 7bd5eb84-2717-482f-bfda-c79f798cfc91
  Args:
    type: :Person
    source: :Hubertus
  AssignClass (b7fa2f85-8a9e-4332-9fb3-2ed245e24cec)
 Call ID: b7fa2f85-8a9e-4332-9fb3-2ed245e24cec
  Args:
    type: :Man
    source: :Hubertus
  AssignClass (5336b6c9-8e4b-49d2-adb7-e75a3b661750)
 Call ID: 5336b6c9-8e4b-49d2-adb7-e75a3b661750
  Args:
    type: :Person
    source: :Frederick
  AssignClass (84683af3-7813-442f-8d8c-5904aa97431f)
 Call ID: 84683af3-7813-442f-8d8c-5904aa97431f
  Args:
    type: :Man
    source: :Frederick
  AssignClass (18b92bed-f114-4b3e-80dd-060b522e447e)
 Call ID: 18b92bed-f114-4b3e-80dd-060b522e447e
  Args:
    type: :Person
    source: :Cecilie_sister
  AssignClass (4c119be3-14f1-40a5-8518-dac42f8ca7d3)
 Call ID: 4c119be3-14f1-40a5-8518-dac42f8ca7d3
  Args:
    type: :Woman
    source: :Cecilie_sister
  AddTriple (f4d0d985-e82c-42a4-89ad-fe5d79a01925)
 Call ID: f4d0d985-e82c-42a4-89ad-fe5d79a01925
  Args:
    target: :Wilhelm_German_Crown_Prince
    source: :Wilhelm_brother
    relation: :hasFather
  AddTriple (7c5bcd82-32f6-4119-8fdf-1c8599422249)
 Call ID: 7c5bcd82-32f6-4119-8fdf-1c8599422249
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
    source: :Wilhelm_brother
  AddTriple (a96e91c2-cb14-4c8c-825f-4a67c49c5c82)
 Call ID: a96e91c2-cb14-4c8c-825f-4a67c49c5c82
  Args:
    source: :Louis_Ferdinand
    relation: :hasFather
    target: :Wilhelm_German_Crown_Prince
  AddTriple (6167010f-24c5-42da-8b26-4906ad5dda66)
 Call ID: 6167010f-24c5-42da-8b26-4906ad5dda66
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    source: :Louis_Ferdinand
    relation: :hasMother
  AddTriple (e2e989ab-7a2f-4a06-a60b-37b697f64c45)
 Call ID: e2e989ab-7a2f-4a06-a60b-37b697f64c45
  Args:
    target: :Wilhelm_German_Crown_Prince
    source: :Hubertus
    relation: :hasFather
  AddTriple (f5131352-efc1-473b-ae8a-701e1800e383)
 Call ID: f5131352-efc1-473b-ae8a-701e1800e383
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
    source: :Hubertus
  AddTriple (8aa91a20-36e9-4f09-ae06-4df09e46378e)
 Call ID: 8aa91a20-36e9-4f09-ae06-4df09e46378e
  Args:
    relation: :hasFather
    source: :Frederick
    target: :Wilhelm_German_Crown_Prince
  AddTriple (c15f9efd-faf9-4c6b-a7c9-e46aad4c033e)
 Call ID: c15f9efd-faf9-4c6b-a7c9-e46aad4c033e
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    source: :Frederick
    relation: :hasMother
  AddTriple (16630306-512e-45e6-9122-ea5f79615171)
 Call ID: 16630306-512e-45e6-9122-ea5f79615171
  Args:
    relation: :hasFather
    source: :Cecilie_sister
    target: :Wilhelm_German_Crown_Prince
  AddTriple (bc1c16b7-432d-4ede-801c-11c72c30ce4d)
 Call ID: bc1c16b7-432d-4ede-801c-11c72c30ce4d
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    source: :Cecilie_sister
    relation: :hasMother
  Finish (c9960a0f-48fe-4bc5-b821-324c621c630c)
 Call ID: c9960a0f-48fe-4bc5-b821-324c621c630c
  Args: