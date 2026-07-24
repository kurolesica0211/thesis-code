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
Anton-Günther, Duke of Oldenburg (Anton-Günther Friedrich August Wilhelm Josias von Holstein-Gottorp, Erbgroßherzog von Oldenburg, Prinz von Lübeck; 16 January 1923 – 20 September 2014) was the head of the Grand Ducal Family of Oldenburg.
Life

He was born in Lensahn the son of Hereditary Grand Duke Nikolaus of Oldenburg (1897–1970) and his first wife Princess Helena of Waldeck and Pyrmont (1899–1948).
Duke Anton-Günther was a grandson of Frederick Augustus II, the last Grand Duke of Oldenburg, and through his mother a grandson of Friedrich, the last Prince of Waldeck and Pyrmont.
He studied for a Diploma in Forestry and succeeded as head of the Grand Ducal Family of Oldenburg upon the death of his father, the Hereditary Grand Duke, on 3 April 1970.
The ancestral home of the House of Oldenburg is Oldenburg castle, nowadays a museum owned by the state.
Private seats of the Duke of Oldenburg are Rastede Palace near Oldenburg and Güldenstein Manor, Harmsdorf, in Schleswig-Holstein.
Eutin Castle in Schleswig-Holstein is a museum owned by a family foundation set up by Duke Anton-Günther.
According to his obituary issued by the family his ancestral titles (however not all part of his official German surname) were: HRH The Duke of Oldenburg, Heir in Norway, Duke of Schleswig, Holstein, Stormarn, Dithmarschen and Oldenburg, Prince of Lübeck and Birkenfeld, Lord of Jever and Knyphausen.
Marriage and children

Duke Anton-Günther was married to Princess Ameli of Löwenstein-Wertheim-Freudenberg (1923-2016) at Kreuzwertheim on 7 August 1951.
They have two children:


The Duke and the Duchess lived at Güldenstein Manor, Harmsdorf, Schleswig Holstein.
The Duke also owned Eutin Castle and Rastede Castle.



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
  AssignClass (cd4e15cf-3c02-4062-afbd-7b85ef45d6a2)
 Call ID: cd4e15cf-3c02-4062-afbd-7b85ef45d6a2
  Args:
    source: Anton-Günther_Duke_of_Oldenburg
    type: :Man
  AssignClass (98e83b5a-b493-4f2f-bdc5-f311277a7e2a)
 Call ID: 98e83b5a-b493-4f2f-bdc5-f311277a7e2a
  Args:
    type: :Person
    source: Anton-Günther_Duke_of_Oldenburg
  AddLiteral (9b9da19c-f883-4016-b6ea-9cb6ec3ddd68)
 Call ID: 9b9da19c-f883-4016-b6ea-9cb6ec3ddd68
  Args:
    source: Anton-Günther_Duke_of_Oldenburg
    literal_value: 1923
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3d5bb476-626a-4bdd-9dfd-b5559759111a)
 Call ID: 3d5bb476-626a-4bdd-9dfd-b5559759111a
  Args:
    literal_value: 2014
    source: Anton-Günther_Duke_of_Oldenburg
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (f4ff79f1-e2f7-41f1-8a1f-ce3ef7c6ffe1)
 Call ID: f4ff79f1-e2f7-41f1-8a1f-ce3ef7c6ffe1
  Args:
    type: :Man
    source: Nikolaus_of_Oldenburg
  AssignClass (f435ad49-101b-4a72-b15b-f958a4be9bdc)
 Call ID: f435ad49-101b-4a72-b15b-f958a4be9bdc
  Args:
    source: Nikolaus_of_Oldenburg
    type: :Person
  AddLiteral (33fdc342-d314-46a2-8b49-9d17c1a611cb)
 Call ID: 33fdc342-d314-46a2-8b49-9d17c1a611cb
  Args:
    literal_value: 1897
    source: Nikolaus_of_Oldenburg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f5c0b932-5d77-4e41-a337-d35966c0bf3c)
 Call ID: f5c0b932-5d77-4e41-a337-d35966c0bf3c
  Args:
    literal_value: 1970
    source: Nikolaus_of_Oldenburg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (b830b11f-3d96-48a7-b043-25d359a1cb87)
 Call ID: b830b11f-3d96-48a7-b043-25d359a1cb87
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    type: :Woman
  AssignClass (c1278b1d-0a68-4c7a-8b74-422a64d44eaa)
 Call ID: c1278b1d-0a68-4c7a-8b74-422a64d44eaa
  Args:
    type: :Person
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (7ba24913-b5df-490f-8c2d-4e1394bceb27)
 Call ID: 7ba24913-b5df-490f-8c2d-4e1394bceb27
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1899
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (92326d78-ca3a-46e2-9e78-2f71ce9c43e7)
 Call ID: 92326d78-ca3a-46e2-9e78-2f71ce9c43e7
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Helena_of_Waldeck_and_Pyrmont
    literal_value: 1948
  AddTriple (47cc5189-c3d4-47bb-90fb-1472327e13a4)
 Call ID: 47cc5189-c3d4-47bb-90fb-1472327e13a4
  Args:
    target: Nikolaus_of_Oldenburg
    source: Anton-Günther_Duke_of_Oldenburg
    relation: :hasFather
  AddTriple (b6433928-6ec5-481c-83d6-f419015f9ceb)
 Call ID: b6433928-6ec5-481c-83d6-f419015f9ceb
  Args:
    target: Helena_of_Waldeck_and_Pyrmont
    source: Anton-Günther_Duke_of_Oldenburg
    relation: :hasMother
  AssignClass (1315b23c-60e0-4e60-a467-23f74367548d)
 Call ID: 1315b23c-60e0-4e60-a467-23f74367548d
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (e5e6c9b1-91da-4f3f-bd0e-5330388b0f1c)
 Call ID: e5e6c9b1-91da-4f3f-bd0e-5330388b0f1c
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    type: :Person
  AddTriple (49db5634-f22c-4c4e-9cb0-f9f58a02e835)
 Call ID: 49db5634-f22c-4c4e-9cb0-f9f58a02e835
  Args:
    target: Frederick_Augustus_II_of_Oldenburg
    relation: :hasAncestor
    source: Anton-Günther_Duke_of_Oldenburg
  AssignClass (76351b64-1f83-4176-b70f-1528112dbafb)
 Call ID: 76351b64-1f83-4176-b70f-1528112dbafb
  Args:
    type: :Man
    source: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (603c0b9f-954a-4055-8d94-b3d8963762f2)
 Call ID: 603c0b9f-954a-4055-8d94-b3d8963762f2
  Args:
    type: :Person
    source: Friedrich_of_Waldeck_and_Pyrmont
  AddTriple (d8223608-c24b-4c39-8e46-69de8cae6682)
 Call ID: d8223608-c24b-4c39-8e46-69de8cae6682
  Args:
    target: Friedrich_of_Waldeck_and_Pyrmont
    relation: :hasAncestor
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (b6d2cb72-e372-4a89-8f9e-33468a931675)
 Call ID: b6d2cb72-e372-4a89-8f9e-33468a931675
  Args:
    type: :Woman
    source: Ameli_of_Löwenstein-Wertheim-Freudenberg
  AssignClass (ad4d8b84-60dd-4972-8f90-75a7e0101e0d)
 Call ID: ad4d8b84-60dd-4972-8f90-75a7e0101e0d
  Args:
    source: Ameli_of_Löwenstein-Wertheim-Freudenberg
    type: :Person
  AddLiteral (660943cd-c2b5-4ce9-983c-45c994f7e73b)
 Call ID: 660943cd-c2b5-4ce9-983c-45c994f7e73b
  Args:
    literal_value: 1923
    source: Ameli_of_Löwenstein-Wertheim-Freudenberg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (32ba53e8-6f55-4cbb-9d04-5b198ab1c8b6)
 Call ID: 32ba53e8-6f55-4cbb-9d04-5b198ab1c8b6
  Args:
    source: Ameli_of_Löwenstein-Wertheim-Freudenberg
    literal_value: 2016
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (38660252-42cb-47b1-acb2-bd8d40cb5c0a)
 Call ID: 38660252-42cb-47b1-acb2-bd8d40cb5c0a
  Args:
    source: Anton-Günther_Duke_of_Oldenburg
    literal_value: 1951
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (c90eecf5-4fd1-45ab-a826-fd3a770f6b6f)
 Call ID: c90eecf5-4fd1-45ab-a826-fd3a770f6b6f
  Args:
    target: Ameli_of_Löwenstein-Wertheim-Freudenberg
    source: Anton-Günther_Duke_of_Oldenburg
    relation: :hasRelation
  Finish (b9ab163d-67ef-4d57-913e-020de0b65132)
 Call ID: b9ab163d-67ef-4d57-913e-020de0b65132
  Args: