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
  AssignClass (d64edb80-fbdc-4f7f-952d-975c946099ce)
 Call ID: d64edb80-fbdc-4f7f-952d-975c946099ce
  Args:
    source: :Marie_Alexandra_of_Baden
    type: :Woman
  AssignClass (f4a117d9-ded3-459d-b461-d67f483445e0)
 Call ID: f4a117d9-ded3-459d-b461-d67f483445e0
  Args:
    type: :Person
    source: :Marie_Alexandra_of_Baden
  AddLiteral (8579d7d7-4a23-4b84-9e3e-258526251c9b)
 Call ID: 8579d7d7-4a23-4b84-9e3e-258526251c9b
  Args:
    relation: :hasBirthYear
    source: :Marie_Alexandra_of_Baden
    literal_value: 1902
    literal_type: xsd:integer
  AddLiteral (31324511-75c6-4a90-aa90-c0a72d8aefdd)
 Call ID: 31324511-75c6-4a90-aa90-c0a72d8aefdd
  Args:
    literal_type: xsd:integer
    source: :Marie_Alexandra_of_Baden
    literal_value: 1944
    relation: :hasDeathYear
  AssignClass (f857c567-b23e-4c0d-b15e-ef298c58d07c)
 Call ID: f857c567-b23e-4c0d-b15e-ef298c58d07c
  Args:
    source: :Maximilian_of_Baden
    type: :Man
  AssignClass (d79f1962-025d-4c36-a503-79d9a18d2fe9)
 Call ID: d79f1962-025d-4c36-a503-79d9a18d2fe9
  Args:
    type: :Person
    source: :Maximilian_of_Baden
  AddLiteral (bd322bbd-f71c-46c6-b0b5-d2173dde84e0)
 Call ID: bd322bbd-f71c-46c6-b0b5-d2173dde84e0
  Args:
    relation: :hasBirthYear
    literal_value: 1867
    source: :Maximilian_of_Baden
    literal_type: xsd:integer
  AddLiteral (60683c3f-aad1-4af1-9e28-ff7b1213feba)
 Call ID: 60683c3f-aad1-4af1-9e28-ff7b1213feba
  Args:
    relation: :hasDeathYear
    source: :Maximilian_of_Baden
    literal_value: 1929
    literal_type: xsd:integer
  AssignClass (494d7082-cb15-4b9a-a8d1-81a94a20bfa0)
 Call ID: 494d7082-cb15-4b9a-a8d1-81a94a20bfa0
  Args:
    type: :Woman
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (2220dc07-632b-4b34-bd0b-77f795d1bc27)
 Call ID: 2220dc07-632b-4b34-bd0b-77f795d1bc27
  Args:
    type: :Person
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AddLiteral (2d0d6276-270b-4b14-884d-8fa0870e8e54)
 Call ID: 2d0d6276-270b-4b14-884d-8fa0870e8e54
  Args:
    relation: :hasBirthYear
    literal_value: 1879
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
  AddLiteral (256099df-bc6b-4b4c-b750-efbc62f65d9c)
 Call ID: 256099df-bc6b-4b4c-b750-efbc62f65d9c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1948
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (c6f8d3bd-042d-401a-b171-4e822e59befd)
 Call ID: c6f8d3bd-042d-401a-b171-4e822e59befd
  Args:
    target: :Maximilian_of_Baden
    relation: :hasFather
    source: :Marie_Alexandra_of_Baden
  AddTriple (cb2085a3-b054-4cda-9314-1491387eca72)
 Call ID: cb2085a3-b054-4cda-9314-1491387eca72
  Args:
    relation: :hasMother
    source: :Marie_Alexandra_of_Baden
    target: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (34550b77-2db3-44f5-9743-27f4c4712a7a)
 Call ID: 34550b77-2db3-44f5-9743-27f4c4712a7a
  Args:
    type: :Man
    source: :Wilhelm_of_Baden
  AssignClass (d8223277-d144-41ed-9e8f-e6860670cede)
 Call ID: d8223277-d144-41ed-9e8f-e6860670cede
  Args:
    type: :Person
    source: :Wilhelm_of_Baden
  AddLiteral (be4a75f9-a549-45ac-8126-c80c6c45f7ef)
 Call ID: be4a75f9-a549-45ac-8126-c80c6c45f7ef
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Wilhelm_of_Baden
    literal_value: 1829
  AddLiteral (ec88f547-0887-4a8d-ad8d-d8f0045c7f1e)
 Call ID: ec88f547-0887-4a8d-ad8d-d8f0045c7f1e
  Args:
    relation: :hasDeathYear
    source: :Wilhelm_of_Baden
    literal_value: 1897
    literal_type: xsd:integer
  AssignClass (da13f004-3e1f-4302-8b63-ed6a145c87bf)
 Call ID: da13f004-3e1f-4302-8b63-ed6a145c87bf
  Args:
    source: :Maria_Maximilianovna_of_Leuchtenberg
    type: :Woman
  AssignClass (8bfef261-b429-4452-be2d-3739d00b7723)
 Call ID: 8bfef261-b429-4452-be2d-3739d00b7723
  Args:
    type: :Person
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddLiteral (dae35733-a01e-45d1-b867-55188e4da62f)
 Call ID: dae35733-a01e-45d1-b867-55188e4da62f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1841
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddLiteral (d85c42d8-68eb-4826-adeb-263f82bfc82b)
 Call ID: d85c42d8-68eb-4826-adeb-263f82bfc82b
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1914
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (df53072b-32e3-42e9-ae63-d2c0238b16a1)
 Call ID: df53072b-32e3-42e9-ae63-d2c0238b16a1
  Args:
    relation: :hasFather
    source: :Maximilian_of_Baden
    target: :Wilhelm_of_Baden
  AddTriple (82d09d9a-fda2-4719-9065-bb8ccc7d7904)
 Call ID: 82d09d9a-fda2-4719-9065-bb8ccc7d7904
  Args:
    source: :Maximilian_of_Baden
    relation: :hasMother
    target: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (6f127c4e-5f57-451e-bfc5-c5223fb7279b)
 Call ID: 6f127c4e-5f57-451e-bfc5-c5223fb7279b
  Args:
    source: :Maximilian_Duke_of_Leuchtenberg
    type: :Man
  AssignClass (eb8a69ae-118b-4105-a83b-a5cf536e1448)
 Call ID: eb8a69ae-118b-4105-a83b-a5cf536e1448
  Args:
    source: :Maximilian_Duke_of_Leuchtenberg
    type: :Person
  AddLiteral (2c815756-2fd5-436b-a3c6-e8c392708c02)
 Call ID: 2c815756-2fd5-436b-a3c6-e8c392708c02
  Args:
    literal_type: xsd:integer
    source: :Maximilian_Duke_of_Leuchtenberg
    literal_value: 1817
    relation: :hasBirthYear
  AddLiteral (27b548f7-0ee5-4799-87d3-56b652151c34)
 Call ID: 27b548f7-0ee5-4799-87d3-56b652151c34
  Args:
    relation: :hasDeathYear
    literal_value: 1852
    source: :Maximilian_Duke_of_Leuchtenberg
    literal_type: xsd:integer
  AssignClass (d28a5f3f-952f-40db-825f-f453721d065f)
 Call ID: d28a5f3f-952f-40db-825f-f453721d065f
  Args:
    type: :Woman
    source: :Maria_Nikolaevna
  AssignClass (69225faa-15e8-4ca3-9ccf-888ccc199dc0)
 Call ID: 69225faa-15e8-4ca3-9ccf-888ccc199dc0
  Args:
    source: :Maria_Nikolaevna
    type: :Person
  AddLiteral (7330ee58-6113-4734-861f-db2cca161721)
 Call ID: 7330ee58-6113-4734-861f-db2cca161721
  Args:
    source: :Maria_Nikolaevna
    literal_value: 1819
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (a4bed0b5-efcd-459f-8366-bd633c2e4391)
 Call ID: a4bed0b5-efcd-459f-8366-bd633c2e4391
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Maria_Nikolaevna
    literal_value: 1876
  AddTriple (e562b561-d9a3-4de1-91cf-c02ea5da98c2)
 Call ID: e562b561-d9a3-4de1-91cf-c02ea5da98c2
  Args:
    target: :Maximilian_Duke_of_Leuchtenberg
    relation: :hasFather
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (652096b3-d724-475e-a564-77171ad939a7)
 Call ID: 652096b3-d724-475e-a564-77171ad939a7
  Args:
    target: :Maria_Nikolaevna
    source: :Maria_Maximilianovna_of_Leuchtenberg
    relation: :hasMother
  AssignClass (a3a37ff4-b5f6-41da-81cf-2051d8b98564)
 Call ID: a3a37ff4-b5f6-41da-81cf-2051d8b98564
  Args:
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
    type: :Man
  AssignClass (cc7a5696-23e2-4049-a61c-6f30a46ae467)
 Call ID: cc7a5696-23e2-4049-a61c-6f30a46ae467
  Args:
    type: :Person
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (04c1a0bf-3934-4d43-9262-277375fa8f51)
 Call ID: 04c1a0bf-3934-4d43-9262-277375fa8f51
  Args:
    relation: :hasFather
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (04a762f3-ea88-4716-b43b-9149cb86e876)
 Call ID: 04a762f3-ea88-4716-b43b-9149cb86e876
  Args:
    source: :Wolfgang_of_Hesse
    type: :Man
  AssignClass (34596f23-b2fb-4e70-a810-efa4dfad95b7)
 Call ID: 34596f23-b2fb-4e70-a810-efa4dfad95b7
  Args:
    source: :Wolfgang_of_Hesse
    type: :Person
  AddLiteral (10a471af-a696-41ba-b33c-d0f7a7e206b8)
 Call ID: 10a471af-a696-41ba-b33c-d0f7a7e206b8
  Args:
    literal_value: 1896
    source: :Wolfgang_of_Hesse
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f52effe5-4438-48fe-ae63-d9c13f751b0a)
 Call ID: f52effe5-4438-48fe-ae63-d9c13f751b0a
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Wolfgang_of_Hesse
    literal_value: 1989
  AddLiteral (862d3507-c7dd-41c0-9e66-83d3b777204c)
 Call ID: 862d3507-c7dd-41c0-9e66-83d3b777204c
  Args:
    literal_type: xsd:integer
    literal_value: 1924
    source: :Marie_Alexandra_of_Baden
    relation: :hasMarriageYear
  AddTriple (b1323439-9877-42c0-8972-875fd651905d)
 Call ID: b1323439-9877-42c0-8972-875fd651905d
  Args:
    target: :Wolfgang_of_Hesse
    relation: :hasRelation
    source: :Marie_Alexandra_of_Baden
  Finish (eeea5138-c652-4f3a-ac0c-d6ba5fba8ef9)
 Call ID: eeea5138-c652-4f3a-ac0c-d6ba5fba8ef9
  Args: