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
Rose Constance Leveson-Gower, Countess Granville (née Bowes-Lyon; 6 May 1890 – 17 November 1967) was the third daughter of the 14th Earl of Strathmore and Kinghorne by his wife, Cecilia Cavendish-Bentinck.
An elder sister of Queen Elizabeth the Queen Mother, she was therefore a maternal aunt of Queen Elizabeth II.


Life and family

On 24 May 1916, Lady Rose Bowes-Lyon married The Hon.
William Leveson-Gower, who succeeded to his childless brother's earldom on 21 July 1939.
As a result, she was styled as Countess Granville.
The couple had two children:


The Countess Granville stood godmother to her niece, Princess Margaret Rose of York, at the latter's christening on 3 October 1930.
She was also awarded the honorary degree of Doctor of Laws (LL.D.) by Queen's University Belfast.
Lord Granville died on 25 June 1953, aged 72.
Lady Granville outlived him by fourteen years when she died on 17 November 1967, aged 77.
She was the last surviving sibling of Queen Elizabeth The Queen Mother.



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
  AssignClass (2040d6cb-ff19-4c70-9bb8-8fbd16852dd1)
 Call ID: 2040d6cb-ff19-4c70-9bb8-8fbd16852dd1
  Args:
    type: :Woman
    source: Rose_Constance_Leveson-Gower
  AssignClass (0a48ce07-139f-49e8-86bb-6f8f7e24d331)
 Call ID: 0a48ce07-139f-49e8-86bb-6f8f7e24d331
  Args:
    type: :Person
    source: Rose_Constance_Leveson-Gower
  AddLiteral (4bfa8080-9ab7-4057-ac34-07c2043268f0)
 Call ID: 4bfa8080-9ab7-4057-ac34-07c2043268f0
  Args:
    source: Rose_Constance_Leveson-Gower
    literal_type: xsd:integer
    literal_value: 1890
    relation: :hasBirthYear
  AddLiteral (1e1b74a3-c0f9-4f6c-a8f4-ec91d5f4f222)
 Call ID: 1e1b74a3-c0f9-4f6c-a8f4-ec91d5f4f222
  Args:
    source: Rose_Constance_Leveson-Gower
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1967
  AssignClass (58dca83b-79e3-4e9c-b956-7e76fe94fdf4)
 Call ID: 58dca83b-79e3-4e9c-b956-7e76fe94fdf4
  Args:
    source: 14th_Earl_of_Strathmore_and_Kinghorne
    type: :Man
  AssignClass (3a1e7bbd-9f27-46e4-a947-a48d034c98a2)
 Call ID: 3a1e7bbd-9f27-46e4-a947-a48d034c98a2
  Args:
    source: 14th_Earl_of_Strathmore_and_Kinghorne
    type: :Person
  AssignClass (0301f403-9ab6-4d53-8f21-83c54150c296)
 Call ID: 0301f403-9ab6-4d53-8f21-83c54150c296
  Args:
    type: :Woman
    source: Cecilia_Cavendish-Bentinck
  AssignClass (91cc23e3-e8c9-40df-a799-21f045f26a90)
 Call ID: 91cc23e3-e8c9-40df-a799-21f045f26a90
  Args:
    type: :Person
    source: Cecilia_Cavendish-Bentinck
  AddTriple (379dd2db-e38b-4778-b011-f705bd3f3ea1)
 Call ID: 379dd2db-e38b-4778-b011-f705bd3f3ea1
  Args:
    relation: :isDaughterOf
    source: Rose_Constance_Leveson-Gower
    target: 14th_Earl_of_Strathmore_and_Kinghorne
  AddTriple (4b8f2ca8-f7c0-4c4b-ac9b-4c5a71bbb480)
 Call ID: 4b8f2ca8-f7c0-4c4b-ac9b-4c5a71bbb480
  Args:
    relation: :isDaughterOf
    source: Rose_Constance_Leveson-Gower
    target: Cecilia_Cavendish-Bentinck
  AssignClass (9ea2bf94-03f1-40e9-912d-9b96a63bd996)
 Call ID: 9ea2bf94-03f1-40e9-912d-9b96a63bd996
  Args:
    type: :Woman
    source: Queen_Elizabeth_the_Queen_Mother
  AssignClass (17cbbf54-5b64-48a7-969d-b74c5cb1d504)
 Call ID: 17cbbf54-5b64-48a7-969d-b74c5cb1d504
  Args:
    source: Queen_Elizabeth_the_Queen_Mother
    type: :Person
  AddTriple (e174ce14-5f3e-4033-bb1b-509c4e10a689)
 Call ID: e174ce14-5f3e-4033-bb1b-509c4e10a689
  Args:
    relation: :isSisterOf
    source: Rose_Constance_Leveson-Gower
    target: Queen_Elizabeth_the_Queen_Mother
  AssignClass (0995f718-defc-4652-a878-be33e795bd14)
 Call ID: 0995f718-defc-4652-a878-be33e795bd14
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (21643205-c15e-400f-b603-3822ea529298)
 Call ID: 21643205-c15e-400f-b603-3822ea529298
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AddTriple (d7c37331-9b5c-4e8e-a7a1-8c2cd5d9590b)
 Call ID: d7c37331-9b5c-4e8e-a7a1-8c2cd5d9590b
  Args:
    source: Rose_Constance_Leveson-Gower
    target: Queen_Elizabeth_II
    relation: :isAuntOf
  AssignClass (5c72bc0b-d0c4-4fde-87de-fc97b99e1195)
 Call ID: 5c72bc0b-d0c4-4fde-87de-fc97b99e1195
  Args:
    source: William_Leveson-Gower
    type: :Man
  AssignClass (0e0b5333-afb7-430c-99ee-91bad55734bc)
 Call ID: 0e0b5333-afb7-430c-99ee-91bad55734bc
  Args:
    source: William_Leveson-Gower
    type: :Person
  AddLiteral (be823aa9-3ddb-4d4e-937d-84e2dd0682e7)
 Call ID: be823aa9-3ddb-4d4e-937d-84e2dd0682e7
  Args:
    literal_type: xsd:integer
    source: Rose_Constance_Leveson-Gower
    literal_value: 1916
    relation: :hasMarriageYear
  AddTriple (f8f1fad5-a0f4-48b7-a1d4-ef99098ca08a)
 Call ID: f8f1fad5-a0f4-48b7-a1d4-ef99098ca08a
  Args:
    relation: :hasRelation
    source: Rose_Constance_Leveson-Gower
    target: William_Leveson-Gower
  AssignClass (eaea2feb-9591-4e28-b9ff-98744c5f15d1)
 Call ID: eaea2feb-9591-4e28-b9ff-98744c5f15d1
  Args:
    type: :Woman
    source: Princess_Margaret_Rose_of_York
  AssignClass (60577803-95ae-44f8-909b-108fa3281bfc)
 Call ID: 60577803-95ae-44f8-909b-108fa3281bfc
  Args:
    source: Princess_Margaret_Rose_of_York
    type: :Person
  AddTriple (0685484a-7034-42ec-acd6-c85998dc9564)
 Call ID: 0685484a-7034-42ec-acd6-c85998dc9564
  Args:
    relation: :isAuntOf
    target: Princess_Margaret_Rose_of_York
    source: Rose_Constance_Leveson-Gower
  AddLiteral (1a45eaad-fe90-4215-8a05-f4db2648c833)
 Call ID: 1a45eaad-fe90-4215-8a05-f4db2648c833
  Args:
    relation: :hasDeathYear
    literal_value: 1953
    literal_type: xsd:integer
    source: William_Leveson-Gower
  Finish (bbe558ed-add8-429b-ab07-9617ef44ef34)
 Call ID: bbe558ed-add8-429b-ab07-9617ef44ef34
  Args: