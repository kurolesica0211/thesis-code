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
Duchess Donata of Mecklenburg (born 11 March 1956) is the senior remaining member of the House of Mecklenburg-Schwerin.
Since there are no males left in the family, the Schwerin branch itself is considered extinct due to the Salic law of succession, leaving Mecklenburg-Strelitz as the only remaining line of the House of Mecklenburg.
Duchess of Mecklenburg

She was born in Kiel in the state of Schleswig-Holstein the eldest daughter of Duke Christian Louis of Mecklenburg-Schwerin and his wife Princess Barbara of Prussia (1920-1994).
Her father was the younger brother to the last surviving male of the House of Mecklenburg-Schwerin, Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin.
Her mother was the daughter of Princess Charlotte of Saxe-Altenburg, the eldest daughter of Ernst II, the last duke of Saxe-Altenburg.
Donata had only one sister Edwina (born 25 September 1960), and as her uncle had no children the House of Mecklenburg-Schwerin became extinct in the male line in 2001 when her uncle died.
As a result, the Mecklenburg-Strelitz line, headed by Borwin, Duke of Mecklenburg, will become the only surviving line of the House of Mecklenburg when both Donata and Edwina are dead.
Her paternal grandfather was the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
She is also a descendant of Christian IX of Denmark as her paternal grandmother, Alexandra of Hanover and Cumberland, a daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark, was the youngest daughter and fifth child of Christian IX of Denmark and Louise of Hesse-Kassel.
Her maternal grandfather was Prince Sigismund of Prussia, a grandson of Grand Duke Louis IV and Alice, Grand Duchess of Hesse and by Rhine, the second daughter of Queen Victoria.



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
  AssignClass (419d6148-3cc8-4dc8-ad81-82c411f60b56)
 Call ID: 419d6148-3cc8-4dc8-ad81-82c411f60b56
  Args:
    type: :Woman
    source: Donata_of_Mecklenburg
  AddLiteral (5b602409-fc01-4703-b347-7cbb87e7fcf7)
 Call ID: 5b602409-fc01-4703-b347-7cbb87e7fcf7
  Args:
    source: Donata_of_Mecklenburg
    relation: :hasBirthYear
    literal_value: 1956
    literal_type: xsd:integer
  AssignClass (0362252a-7c34-4e5b-a06b-c41092976f81)
 Call ID: 0362252a-7c34-4e5b-a06b-c41092976f81
  Args:
    source: Christian_Louis_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (8d9dff0b-20fa-4817-adbd-8fe195fe2cf9)
 Call ID: 8d9dff0b-20fa-4817-adbd-8fe195fe2cf9
  Args:
    source: Barbara_of_Prussia
    type: :Woman
  AddLiteral (9fea5050-b745-4d6b-a728-68ec25685731)
 Call ID: 9fea5050-b745-4d6b-a728-68ec25685731
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1920
    source: Barbara_of_Prussia
  AddLiteral (78aa34b8-e700-40b7-a116-edf584cbf7c8)
 Call ID: 78aa34b8-e700-40b7-a116-edf584cbf7c8
  Args:
    relation: :hasDeathYear
    literal_value: 1994
    literal_type: xsd:integer
    source: Barbara_of_Prussia
  AddTriple (494afdc1-c91d-4331-be94-7a74fcf9e165)
 Call ID: 494afdc1-c91d-4331-be94-7a74fcf9e165
  Args:
    source: Donata_of_Mecklenburg
    target: Christian_Louis_of_Mecklenburg-Schwerin
    relation: :isDaughterOf
  AddTriple (9ca216db-7d79-4238-9b8f-336c2d7083d0)
 Call ID: 9ca216db-7d79-4238-9b8f-336c2d7083d0
  Args:
    source: Donata_of_Mecklenburg
    target: Barbara_of_Prussia
    relation: :isDaughterOf
  AssignClass (dfd70c3e-16e8-48d6-b983-459f1b4d043a)
 Call ID: dfd70c3e-16e8-48d6-b983-459f1b4d043a
  Args:
    source: Friedrich_Franz_Mecklenburg-Schwerin
    type: :Man
  AddTriple (07794dbf-9662-46a4-a7cc-3cceecad81fc)
 Call ID: 07794dbf-9662-46a4-a7cc-3cceecad81fc
  Args:
    source: Christian_Louis_of_Mecklenburg-Schwerin
    target: Friedrich_Franz_Mecklenburg-Schwerin
    relation: :isBrotherOf
  AssignClass (26af70aa-e0da-46e3-9ee9-58e2e3451b70)
 Call ID: 26af70aa-e0da-46e3-9ee9-58e2e3451b70
  Args:
    type: :Woman
    source: Edwina_Mecklenburg-Schwerin
  AddLiteral (c1acceec-3b8e-41c7-be2c-25f94166b559)
 Call ID: c1acceec-3b8e-41c7-be2c-25f94166b559
  Args:
    source: Edwina_Mecklenburg-Schwerin
    literal_value: 1960
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (13064434-e799-4695-bdcc-031cbdcbd3b2)
 Call ID: 13064434-e799-4695-bdcc-031cbdcbd3b2
  Args:
    target: Donata_of_Mecklenburg
    relation: :isSisterOf
    source: Edwina_Mecklenburg-Schwerin
  AddTriple (7aa87211-0903-48d9-9121-4116d1455afb)
 Call ID: 7aa87211-0903-48d9-9121-4116d1455afb
  Args:
    source: Edwina_Mecklenburg-Schwerin
    target: Christian_Louis_of_Mecklenburg-Schwerin
    relation: :isDaughterOf
  AddTriple (48ecadc3-7191-4750-be41-8432802328a4)
 Call ID: 48ecadc3-7191-4750-be41-8432802328a4
  Args:
    target: Barbara_of_Prussia
    relation: :isDaughterOf
    source: Edwina_Mecklenburg-Schwerin
  AssignClass (161320e6-1b03-4a39-9ae3-0895e0703982)
 Call ID: 161320e6-1b03-4a39-9ae3-0895e0703982
  Args:
    source: Charlotte_of_Saxe-Altenburg
    type: :Woman
  AddTriple (0d5aa0c4-7865-4dac-a493-c1ddd420a243)
 Call ID: 0d5aa0c4-7865-4dac-a493-c1ddd420a243
  Args:
    source: Charlotte_of_Saxe-Altenburg
    relation: :isMotherOf
    target: Barbara_of_Prussia
  AssignClass (7d43df08-26a6-4d95-a05c-7a977f80f369)
 Call ID: 7d43df08-26a6-4d95-a05c-7a977f80f369
  Args:
    type: :Man
    source: Ernst_II_Saxe-Altenburg
  AddTriple (c6088146-49d9-4191-ad99-34d81f877de1)
 Call ID: c6088146-49d9-4191-ad99-34d81f877de1
  Args:
    relation: :isFatherOf
    target: Charlotte_of_Saxe-Altenburg
    source: Ernst_II_Saxe-Altenburg
  AssignClass (7da0678f-007a-4345-95de-81700075c812)
 Call ID: 7da0678f-007a-4345-95de-81700075c812
  Args:
    source: Frederick_Francis_IV_Mecklenburg-Schwerin
    type: :Man
  AddTriple (52a142d9-192e-4894-aca9-4bdb88dea902)
 Call ID: 52a142d9-192e-4894-aca9-4bdb88dea902
  Args:
    relation: :isFatherOf
    target: Christian_Louis_of_Mecklenburg-Schwerin
    source: Frederick_Francis_IV_Mecklenburg-Schwerin
  AssignClass (0adb88c0-5007-48b9-8c14-98e51e171467)
 Call ID: 0adb88c0-5007-48b9-8c14-98e51e171467
  Args:
    type: :Woman
    source: Alexandra_of_Hanover_and_Cumberland
  AddTriple (c6a523fa-098a-4b2c-8b8b-41b82a196f87)
 Call ID: c6a523fa-098a-4b2c-8b8b-41b82a196f87
  Args:
    relation: :isMotherOf
    target: Christian_Louis_of_Mecklenburg-Schwerin
    source: Alexandra_of_Hanover_and_Cumberland
  AssignClass (e2bb8939-0b03-48de-a961-dbd34a38fe70)
 Call ID: e2bb8939-0b03-48de-a961-dbd34a38fe70
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (56eb4a38-b30d-4f18-9058-807453c11f00)
 Call ID: 56eb4a38-b30d-4f18-9058-807453c11f00
  Args:
    source: Louise_of_Hesse-Kassel
    type: :Woman
  AddTriple (9b988c58-0687-439e-a8c3-493afdb61f80)
 Call ID: 9b988c58-0687-439e-a8c3-493afdb61f80
  Args:
    source: Christian_IX_of_Denmark
    relation: :isFatherOf
    target: Alexandra_of_Hanover_and_Cumberland
  AddTriple (2bd153f0-84be-403f-bc42-6fc89c4c7dc5)
 Call ID: 2bd153f0-84be-403f-bc42-6fc89c4c7dc5
  Args:
    source: Louise_of_Hesse-Kassel
    relation: :isMotherOf
    target: Alexandra_of_Hanover_and_Cumberland
  AssignClass (2f039466-1d3a-45bc-8d05-30315b26526f)
 Call ID: 2f039466-1d3a-45bc-8d05-30315b26526f
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (79fa2912-42ae-4e01-a3aa-ac4d750ebf21)
 Call ID: 79fa2912-42ae-4e01-a3aa-ac4d750ebf21
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AddTriple (09f603ba-e085-4557-9cb3-2db08feb0cdf)
 Call ID: 09f603ba-e085-4557-9cb3-2db08feb0cdf
  Args:
    target: Alexandra_of_Hanover_and_Cumberland
    relation: :isFatherOf
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (f342c5ae-90ed-4286-8d6a-fae7aa91c9e2)
 Call ID: f342c5ae-90ed-4286-8d6a-fae7aa91c9e2
  Args:
    source: Thyra_of_Denmark
    relation: :isMotherOf
    target: Alexandra_of_Hanover_and_Cumberland
  AssignClass (813377a3-463f-450e-8eb5-7f7df5474ef7)
 Call ID: 813377a3-463f-450e-8eb5-7f7df5474ef7
  Args:
    source: Sigismund_of_Prussia
    type: :Man
  AddTriple (d6eef20f-4bad-434c-aa1f-03246e46cf7a)
 Call ID: d6eef20f-4bad-434c-aa1f-03246e46cf7a
  Args:
    source: Sigismund_of_Prussia
    target: Barbara_of_Prussia
    relation: :isFatherOf
  AssignClass (c56e7d50-9934-4036-86ee-ef7ce9a441d9)
 Call ID: c56e7d50-9934-4036-86ee-ef7ce9a441d9
  Args:
    type: :Man
    source: Louis_IV_Grand_Duke_of_Hesse
  AssignClass (696b9312-b378-44eb-804e-b59a2cead4a7)
 Call ID: 696b9312-b378-44eb-804e-b59a2cead4a7
  Args:
    source: Alice_Grand_Duchess_of_Hesse
    type: :Woman
  AssignClass (30cc142d-2265-4c0c-9db4-bb691869c21b)
 Call ID: 30cc142d-2265-4c0c-9db4-bb691869c21b
  Args:
    type: :Woman
    source: Queen_Victoria
  AddTriple (4c8690d6-470c-4f93-ba79-e044975f1ec9)
 Call ID: 4c8690d6-470c-4f93-ba79-e044975f1ec9
  Args:
    source: Alice_Grand_Duchess_of_Hesse
    relation: :isMotherOf
    target: Queen_Victoria
  Finish (bdade65e-74b8-4dde-bc52-f87453dfabd2)
 Call ID: bdade65e-74b8-4dde-bc52-f87453dfabd2
  Args: