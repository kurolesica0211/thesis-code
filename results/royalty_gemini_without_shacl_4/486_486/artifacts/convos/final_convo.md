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
Prince Heinrich Wilhelm Konstantin Viktor Franz of Hesse-Kassel (30 October 1927 – 18 November 1999), also known as Enrico d'Assia, was the second child of Prince Philipp of Hesse and Princess Mafalda of Savoy.
Heinrich became an artist, set designer, and memoirist after World War II.
Life

Prince Heinrich was born in Rome, Italy, as the second son of Prince Philipp of Hesse and Princess Mafalda of Savoy, daughter of King Victor Emmanuel III of Italy.
During the Second World War, Heinrich's father, an important former aristocratic Nazi party member, was arrested by the Gestapo.
Heinrich and his siblings (Moritz, Otto and Elisabeth) were given sanctuary in the Vatican under the care of their aunt and uncle, Margaret Campbell Geddes and Louis, Prince of Hesse and by Rhine, who adopted them.
Heinrich was an artist and set designer, active mainly in Italy under the name Enrico d'Assia.



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
  AssignClass (8883d4d2-4d83-4131-b907-bfc93426dde2)
 Call ID: 8883d4d2-4d83-4131-b907-bfc93426dde2
  Args:
    type: :Man
    source: PrinceHeinrichOfHesseKassel
  AssignClass (d99c12cb-3e6c-49ec-a864-034db5738d95)
 Call ID: d99c12cb-3e6c-49ec-a864-034db5738d95
  Args:
    source: PrinceHeinrichOfHesseKassel
    type: :Person
  AssignClass (3668cf5f-8eee-413b-9735-5476bd5dc9fb)
 Call ID: 3668cf5f-8eee-413b-9735-5476bd5dc9fb
  Args:
    source: PrincePhilippOfHesse
    type: :Man
  AssignClass (4935a8ea-80d8-4502-8683-7578ae0f0a29)
 Call ID: 4935a8ea-80d8-4502-8683-7578ae0f0a29
  Args:
    source: PrincePhilippOfHesse
    type: :Person
  AssignClass (3f4fb4ee-ab51-4184-9340-23cbf136047d)
 Call ID: 3f4fb4ee-ab51-4184-9340-23cbf136047d
  Args:
    source: PrincessMafaldaOfSavoy
    type: :Woman
  AssignClass (f0302cf7-0812-46ef-8726-73e25bb4b699)
 Call ID: f0302cf7-0812-46ef-8726-73e25bb4b699
  Args:
    type: :Person
    source: PrincessMafaldaOfSavoy
  AssignClass (007e827d-d696-45f8-afc1-07ee4bd201ba)
 Call ID: 007e827d-d696-45f8-afc1-07ee4bd201ba
  Args:
    source: KingVictorEmmanuelIIIOfItaly
    type: :Man
  AssignClass (e34c9a58-5140-44df-9233-4cf279746534)
 Call ID: e34c9a58-5140-44df-9233-4cf279746534
  Args:
    type: :Person
    source: KingVictorEmmanuelIIIOfItaly
  AssignClass (7c215340-defc-48fe-89d7-94be3dea2ec3)
 Call ID: 7c215340-defc-48fe-89d7-94be3dea2ec3
  Args:
    source: MoritzOfHesse
    type: :Man
  AssignClass (4460b104-127e-4521-b2f1-5f4cf169b6aa)
 Call ID: 4460b104-127e-4521-b2f1-5f4cf169b6aa
  Args:
    type: :Person
    source: MoritzOfHesse
  AssignClass (e2414050-56fe-48a4-a165-46a09697f6b5)
 Call ID: e2414050-56fe-48a4-a165-46a09697f6b5
  Args:
    type: :Man
    source: OttoOfHesse
  AssignClass (17b417f1-c9e6-4cd2-ac72-19d94b933da3)
 Call ID: 17b417f1-c9e6-4cd2-ac72-19d94b933da3
  Args:
    source: OttoOfHesse
    type: :Person
  AssignClass (70ba150f-dc2d-494b-8224-4f0f70ab7ba2)
 Call ID: 70ba150f-dc2d-494b-8224-4f0f70ab7ba2
  Args:
    source: ElisabethOfHesse
    type: :Woman
  AssignClass (3db4a371-daa8-4c52-84e5-5497524f1fcd)
 Call ID: 3db4a371-daa8-4c52-84e5-5497524f1fcd
  Args:
    source: ElisabethOfHesse
    type: :Person
  AssignClass (36ab6fc6-e3c0-4a6f-974d-3f9f289f16c6)
 Call ID: 36ab6fc6-e3c0-4a6f-974d-3f9f289f16c6
  Args:
    source: MargaretCampbellGeddes
    type: :Woman
  AssignClass (11faeabd-722b-4779-b21b-075121614e30)
 Call ID: 11faeabd-722b-4779-b21b-075121614e30
  Args:
    source: MargaretCampbellGeddes
    type: :Person
  AssignClass (c8407f32-9937-4107-ad4d-2d897fa0ffa1)
 Call ID: c8407f32-9937-4107-ad4d-2d897fa0ffa1
  Args:
    source: LouisPrinceOfHesseAndByRhine
    type: :Man
  AssignClass (615a51e7-262a-4522-8119-4087867a1384)
 Call ID: 615a51e7-262a-4522-8119-4087867a1384
  Args:
    type: :Person
    source: LouisPrinceOfHesseAndByRhine
  AddLiteral (a8d4d7e7-5e21-4c02-b71e-c60d39031aa4)
 Call ID: a8d4d7e7-5e21-4c02-b71e-c60d39031aa4
  Args:
    relation: :alsoKnownAs
    literal_value: Enrico d'Assia
    source: PrinceHeinrichOfHesseKassel
    literal_type: xsd:string
  AddLiteral (b5210db7-a603-470c-a2d1-b3940134d6bd)
 Call ID: b5210db7-a603-470c-a2d1-b3940134d6bd
  Args:
    source: PrinceHeinrichOfHesseKassel
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1927
  AddLiteral (4a0e81a8-8fed-4190-8493-e88f476d2a5d)
 Call ID: 4a0e81a8-8fed-4190-8493-e88f476d2a5d
  Args:
    literal_value: 1999
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: PrinceHeinrichOfHesseKassel
  AddTriple (ac40fc07-c5a9-4da5-bdc4-33ccb86d1f37)
 Call ID: ac40fc07-c5a9-4da5-bdc4-33ccb86d1f37
  Args:
    target: PrincePhilippOfHesse
    source: PrinceHeinrichOfHesseKassel
    relation: :hasFather
  AddTriple (07a67696-c25a-4c59-84e4-7099ffa631df)
 Call ID: 07a67696-c25a-4c59-84e4-7099ffa631df
  Args:
    relation: :hasMother
    target: PrincessMafaldaOfSavoy
    source: PrinceHeinrichOfHesseKassel
  AddTriple (927a8776-8e46-47c8-abe9-18b555093fbd)
 Call ID: 927a8776-8e46-47c8-abe9-18b555093fbd
  Args:
    relation: :hasFather
    target: KingVictorEmmanuelIIIOfItaly
    source: PrincessMafaldaOfSavoy
  AddTriple (82f87fc7-d631-4cbf-8dbb-294af1ab1dd0)
 Call ID: 82f87fc7-d631-4cbf-8dbb-294af1ab1dd0
  Args:
    target: MoritzOfHesse
    source: PrinceHeinrichOfHesseKassel
    relation: :isSiblingOf
  AddTriple (c59b281a-96ed-4960-9bf9-58840bacb50d)
 Call ID: c59b281a-96ed-4960-9bf9-58840bacb50d
  Args:
    relation: :isSiblingOf
    target: OttoOfHesse
    source: PrinceHeinrichOfHesseKassel
  AddTriple (6aa30281-9ab1-4e4e-8c0b-890cef07dca6)
 Call ID: 6aa30281-9ab1-4e4e-8c0b-890cef07dca6
  Args:
    target: ElisabethOfHesse
    source: PrinceHeinrichOfHesseKassel
    relation: :isSiblingOf
  AddTriple (b1577c2d-db8b-4dc2-8408-4af3c95dd395)
 Call ID: b1577c2d-db8b-4dc2-8408-4af3c95dd395
  Args:
    source: MargaretCampbellGeddes
    target: PrinceHeinrichOfHesseKassel
    relation: :isAuntOf
  AddTriple (42e9d11f-8351-4e96-91e7-221e51a6af21)
 Call ID: 42e9d11f-8351-4e96-91e7-221e51a6af21
  Args:
    relation: :isUncleOf
    target: PrinceHeinrichOfHesseKassel
    source: LouisPrinceOfHesseAndByRhine
  AddTriple (ea912b46-e67c-4e44-a45e-2c77cc0b5d77)
 Call ID: ea912b46-e67c-4e44-a45e-2c77cc0b5d77
  Args:
    source: MoritzOfHesse
    target: OttoOfHesse
    relation: :isSiblingOf
  AddTriple (c82c36c1-ec6d-485a-9396-266111ea9b38)
 Call ID: c82c36c1-ec6d-485a-9396-266111ea9b38
  Args:
    target: ElisabethOfHesse
    source: MoritzOfHesse
    relation: :isSiblingOf
  AddTriple (7427738e-ed48-4711-8feb-9e0c491df740)
 Call ID: 7427738e-ed48-4711-8feb-9e0c491df740
  Args:
    source: OttoOfHesse
    target: ElisabethOfHesse
    relation: :isSiblingOf
  Finish (18d9c964-a691-4fc1-a6be-8cfd3afc988c)
 Call ID: 18d9c964-a691-4fc1-a6be-8cfd3afc988c
  Args: