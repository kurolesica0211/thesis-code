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
Princess Marie Alexandra of Baden (Marie Alexandra Thyra Victoria Louise Carola Hilda; 1 August 1902 – 29 January 1944) was a Hessian princess by marriage.
Family

She was the only daughter and elder child of Prince Maximilian of Baden (1867–1929) and Princess Marie Louise of Hanover and Cumberland.
Her paternal grandparents were Prince Wilhelm of Baden (1829–97) and Princess Maria Maximilianovna of Leuchtenberg (1841–1914), a daughter of Maximilian, Duke of Leuchtenberg (1817–52) and Grand Duchess Maria Nikolaevna (1819–1876).
Princess Marie-Louise of Hanover (1879–1948) was a daughter of Ernest Augustus, Crown Prince of Hanover, claimant of the annexed Kingdom of Hanover.
Marriage

On 17 September 1924, she married her fourth cousin Prince Wolfgang of Hesse (1896–1989).
Death

Princess Marie Alexandra was killed in an attack by the U.S. Army Air Forces during an air-raid on Frankfurt am Main on 29–30 January 1944 during World War II.
She and seven other women, who were aid workers, were killed when the cellar, in which they had taken refuge, collapsed under the weight of the building, rendering Marie Alexandra's body barely recognisable.



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
  AssignClass (98f52653-37d5-47e6-855a-7a180f9a98c7)
 Call ID: 98f52653-37d5-47e6-855a-7a180f9a98c7
  Args:
    type: :Woman
    source: :Marie_Alexandra_of_Baden
  AssignClass (a82896c4-938c-4899-b69a-5a280b5ac798)
 Call ID: a82896c4-938c-4899-b69a-5a280b5ac798
  Args:
    type: :Person
    source: :Marie_Alexandra_of_Baden
  AddLiteral (f103478e-77bb-495e-b12b-036f0156cd47)
 Call ID: f103478e-77bb-495e-b12b-036f0156cd47
  Args:
    literal_value: 1902
    source: :Marie_Alexandra_of_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (45584b1b-84cd-483c-a22d-0edb64b3984b)
 Call ID: 45584b1b-84cd-483c-a22d-0edb64b3984b
  Args:
    source: :Marie_Alexandra_of_Baden
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1944
  AssignClass (365c6977-1ea0-4629-a1c2-2a43d6eecc54)
 Call ID: 365c6977-1ea0-4629-a1c2-2a43d6eecc54
  Args:
    type: :Man
    source: :Maximilian_of_Baden
  AssignClass (eac4b5d7-c3d5-4c51-9948-1eac4c8da3f7)
 Call ID: eac4b5d7-c3d5-4c51-9948-1eac4c8da3f7
  Args:
    type: :Person
    source: :Maximilian_of_Baden
  AddLiteral (5c7df2c2-a190-4ee7-8119-b5e53c59ee5f)
 Call ID: 5c7df2c2-a190-4ee7-8119-b5e53c59ee5f
  Args:
    literal_value: 1867
    relation: :hasBirthYear
    source: :Maximilian_of_Baden
    literal_type: xsd:integer
  AddLiteral (4183df5a-12b6-4224-bdae-a0cc6a46f5b0)
 Call ID: 4183df5a-12b6-4224-bdae-a0cc6a46f5b0
  Args:
    literal_type: xsd:integer
    source: :Maximilian_of_Baden
    relation: :hasDeathYear
    literal_value: 1929
  AssignClass (62402b4e-027a-4375-9451-1a8006948757)
 Call ID: 62402b4e-027a-4375-9451-1a8006948757
  Args:
    type: :Woman
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (c33fbb5d-ead2-4eba-a705-02bb0701b414)
 Call ID: c33fbb5d-ead2-4eba-a705-02bb0701b414
  Args:
    type: :Person
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (65c7d8df-23b6-4401-a795-ed3375221dcf)
 Call ID: 65c7d8df-23b6-4401-a795-ed3375221dcf
  Args:
    target: :Maximilian_of_Baden
    relation: :hasFather
    source: :Marie_Alexandra_of_Baden
  AddTriple (7dc028ae-d822-4069-9046-489f01c4d4bc)
 Call ID: 7dc028ae-d822-4069-9046-489f01c4d4bc
  Args:
    source: :Marie_Alexandra_of_Baden
    relation: :hasMother
    target: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (31dce950-6abe-4465-8038-2934e9610df1)
 Call ID: 31dce950-6abe-4465-8038-2934e9610df1
  Args:
    type: :Man
    source: :Wilhelm_of_Baden
  AssignClass (2f42441c-fd71-46e7-a8c5-9155f94f226f)
 Call ID: 2f42441c-fd71-46e7-a8c5-9155f94f226f
  Args:
    type: :Person
    source: :Wilhelm_of_Baden
  AddLiteral (e473c73b-8bd9-4880-8616-5641f2589e5a)
 Call ID: e473c73b-8bd9-4880-8616-5641f2589e5a
  Args:
    literal_value: 1829
    relation: :hasBirthYear
    source: :Wilhelm_of_Baden
    literal_type: xsd:integer
  AddLiteral (6538e0d2-9688-43ea-ae18-fd6cd70a9089)
 Call ID: 6538e0d2-9688-43ea-ae18-fd6cd70a9089
  Args:
    literal_value: 1897
    relation: :hasDeathYear
    source: :Wilhelm_of_Baden
    literal_type: xsd:integer
  AssignClass (caa0ad7d-a1cf-48e1-9fa4-6b9aeed84ec1)
 Call ID: caa0ad7d-a1cf-48e1-9fa4-6b9aeed84ec1
  Args:
    type: :Woman
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (5772991f-cd9b-418d-b21e-b6d919d94c67)
 Call ID: 5772991f-cd9b-418d-b21e-b6d919d94c67
  Args:
    type: :Person
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddLiteral (f1b2f368-8a8d-42be-8ee9-2fc22894c656)
 Call ID: f1b2f368-8a8d-42be-8ee9-2fc22894c656
  Args:
    relation: :hasBirthYear
    source: :Maria_Maximilianovna_of_Leuchtenberg
    literal_type: xsd:integer
    literal_value: 1841
  AddLiteral (9e05249a-535c-486e-acb9-21a4be6bca2b)
 Call ID: 9e05249a-535c-486e-acb9-21a4be6bca2b
  Args:
    literal_type: xsd:integer
    source: :Maria_Maximilianovna_of_Leuchtenberg
    relation: :hasDeathYear
    literal_value: 1914
  AddTriple (b3db7d2f-ee55-4a4c-aff5-018081457cc4)
 Call ID: b3db7d2f-ee55-4a4c-aff5-018081457cc4
  Args:
    target: :Wilhelm_of_Baden
    relation: :hasFather
    source: :Maximilian_of_Baden
  AddTriple (ab204f32-976e-46c1-927b-fd2b3931a98b)
 Call ID: ab204f32-976e-46c1-927b-fd2b3931a98b
  Args:
    source: :Maximilian_of_Baden
    relation: :hasMother
    target: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (4bb79aa0-9e32-4e0c-9264-9904926ce8f9)
 Call ID: 4bb79aa0-9e32-4e0c-9264-9904926ce8f9
  Args:
    type: :Man
    source: :Maximilian_Duke_of_Leuchtenberg
  AssignClass (d695db69-fdd2-427d-bce7-e2f02adee571)
 Call ID: d695db69-fdd2-427d-bce7-e2f02adee571
  Args:
    type: :Person
    source: :Maximilian_Duke_of_Leuchtenberg
  AddLiteral (ec4c3df7-1387-4204-8f60-e0e207bb13c2)
 Call ID: ec4c3df7-1387-4204-8f60-e0e207bb13c2
  Args:
    relation: :hasBirthYear
    source: :Maximilian_Duke_of_Leuchtenberg
    literal_type: xsd:integer
    literal_value: 1817
  AddLiteral (b63efd9f-c270-43bd-9d95-6def787717b3)
 Call ID: b63efd9f-c270-43bd-9d95-6def787717b3
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Maximilian_Duke_of_Leuchtenberg
    literal_value: 1852
  AssignClass (31a0107b-b8bb-4e95-9dee-2868fcdc8dfe)
 Call ID: 31a0107b-b8bb-4e95-9dee-2868fcdc8dfe
  Args:
    type: :Woman
    source: :Maria_Nikolaevna
  AssignClass (a4077da2-1a41-419b-98ce-f036fabffa45)
 Call ID: a4077da2-1a41-419b-98ce-f036fabffa45
  Args:
    type: :Person
    source: :Maria_Nikolaevna
  AddLiteral (106b539e-7a9a-4ac4-beb9-33defc7abb6a)
 Call ID: 106b539e-7a9a-4ac4-beb9-33defc7abb6a
  Args:
    literal_value: 1819
    source: :Maria_Nikolaevna
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (58595248-c585-487f-a6dc-88106fd0e388)
 Call ID: 58595248-c585-487f-a6dc-88106fd0e388
  Args:
    literal_value: 1876
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Maria_Nikolaevna
  AddTriple (12693fbe-4646-4be7-a8ca-de7116e0a160)
 Call ID: 12693fbe-4646-4be7-a8ca-de7116e0a160
  Args:
    target: :Maximilian_Duke_of_Leuchtenberg
    source: :Maria_Maximilianovna_of_Leuchtenberg
    relation: :hasFather
  AddTriple (7c9495f5-17d2-4fda-aa47-827676d0a7ee)
 Call ID: 7c9495f5-17d2-4fda-aa47-827676d0a7ee
  Args:
    target: :Maria_Nikolaevna
    relation: :hasMother
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (1d8a6f62-f6e5-4c60-ad7e-1e8d0165e415)
 Call ID: 1d8a6f62-f6e5-4c60-ad7e-1e8d0165e415
  Args:
    type: :Man
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (a546217d-a385-4882-973c-3b067d97cfec)
 Call ID: a546217d-a385-4882-973c-3b067d97cfec
  Args:
    type: :Person
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (1c86e49b-7e0a-40ab-b226-f996d26d196d)
 Call ID: 1c86e49b-7e0a-40ab-b226-f996d26d196d
  Args:
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasFather
  AddLiteral (a3d0c98e-ba1c-4ba9-bf04-bbeaa1a2095e)
 Call ID: a3d0c98e-ba1c-4ba9-bf04-bbeaa1a2095e
  Args:
    literal_value: 1879
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0c3601aa-2981-4d3f-aba8-dc5c329ab1d6)
 Call ID: 0c3601aa-2981-4d3f-aba8-dc5c329ab1d6
  Args:
    relation: :hasDeathYear
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
    literal_value: 1948
  AssignClass (0563315c-91a1-4d48-a042-04989848df3f)
 Call ID: 0563315c-91a1-4d48-a042-04989848df3f
  Args:
    type: :Man
    source: :Wolfgang_of_Hesse
  AssignClass (50e838fe-830a-4ee8-9cfc-d3b72a608e12)
 Call ID: 50e838fe-830a-4ee8-9cfc-d3b72a608e12
  Args:
    type: :Person
    source: :Wolfgang_of_Hesse
  AddLiteral (3d07fc55-3aae-482e-9eba-cd9db8c121b7)
 Call ID: 3d07fc55-3aae-482e-9eba-cd9db8c121b7
  Args:
    literal_value: 1896
    literal_type: xsd:integer
    source: :Wolfgang_of_Hesse
    relation: :hasBirthYear
  AddLiteral (89a030e2-075d-498d-abc9-9d315b2f3b85)
 Call ID: 89a030e2-075d-498d-abc9-9d315b2f3b85
  Args:
    literal_value: 1989
    literal_type: xsd:integer
    source: :Wolfgang_of_Hesse
    relation: :hasDeathYear
  AddLiteral (c5c1506d-259d-4fb8-b94b-5e487af0de5d)
 Call ID: c5c1506d-259d-4fb8-b94b-5e487af0de5d
  Args:
    relation: :hasMarriageYear
    source: :Marie_Alexandra_of_Baden
    literal_type: xsd:integer
    literal_value: 1924
  AddTriple (55a52032-333a-4341-b657-04145ef33735)
 Call ID: 55a52032-333a-4341-b657-04145ef33735
  Args:
    relation: :hasRelation
    source: :Marie_Alexandra_of_Baden
    target: :Wolfgang_of_Hesse
  Finish (32fe1387-4246-4406-b027-e814b7b518ef)
 Call ID: 32fe1387-4246-4406-b027-e814b7b518ef
  Args: