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
James Alexander Elphinstone, 18th Lord Elphinstone and 4th Baron Elphinstone, AssocRICS (22 April 1953 – 19 December 1994), was a British nobleman, farmer, and financier.
Early life and family

Lord Elphinstone was the son of Rev. Hon.
Andrew Charles Victor Elphinstone and Jean Frances Hambro.
His paternal grandparents were Sidney Buller-Fullerton-Elphinstone, 16th Lord Elphinstone, and the former Lady Mary Bowes-Lyon, elder sister of Queen Elizabeth The Queen Mother.
Personal life

On 22 April 1978, Lord Elphinstone married Willa Mary Gabrielle Chetwode, daughter of Major George David Chetwode and Lady Willa Elliot-Murray-Kynynmound (herself the daughter of Victor Elliot-Murray-Kynynmound, 5th Earl of Minto, and his wife, Marion Cook).
The couple had four children:


He was succeeded in his titles by his eldest son, Alexander.
References




This biography of a Lord of Parliament in the Peerage of Scotland is a stub.



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
  AssignClass (64afd0cb-3823-4096-878d-443ea2448b6c)
 Call ID: 64afd0cb-3823-4096-878d-443ea2448b6c
  Args:
    source: James_Alexander_Elphinstone
    type: :Man
  AssignClass (53fca687-be2a-4ee6-930d-836d3866a603)
 Call ID: 53fca687-be2a-4ee6-930d-836d3866a603
  Args:
    type: :Person
    source: James_Alexander_Elphinstone
  AddLiteral (73b770fe-bb74-4419-acd3-52519b29f724)
 Call ID: 73b770fe-bb74-4419-acd3-52519b29f724
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1953
    source: James_Alexander_Elphinstone
  AddLiteral (9136b760-45e0-4666-af2d-cc7ec9df2bfc)
 Call ID: 9136b760-45e0-4666-af2d-cc7ec9df2bfc
  Args:
    source: James_Alexander_Elphinstone
    literal_value: 1994
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (52fb2aaf-38a8-460f-b451-ccf07776358a)
 Call ID: 52fb2aaf-38a8-460f-b451-ccf07776358a
  Args:
    type: :Man
    source: Andrew_Charles_Victor_Elphinstone
  AssignClass (c55b9dd6-048f-48f7-869e-0ce08dab28d7)
 Call ID: c55b9dd6-048f-48f7-869e-0ce08dab28d7
  Args:
    source: Andrew_Charles_Victor_Elphinstone
    type: :Person
  AssignClass (49967cfe-ce35-4110-aff1-b00d8b562617)
 Call ID: 49967cfe-ce35-4110-aff1-b00d8b562617
  Args:
    source: Jean_Frances_Hambro
    type: :Woman
  AssignClass (5f3d5e29-bc5a-48b9-b405-7a14176fdbf6)
 Call ID: 5f3d5e29-bc5a-48b9-b405-7a14176fdbf6
  Args:
    source: Jean_Frances_Hambro
    type: :Person
  AddTriple (96c0cf1e-cb3e-4909-9a61-21285bca7065)
 Call ID: 96c0cf1e-cb3e-4909-9a61-21285bca7065
  Args:
    target: Andrew_Charles_Victor_Elphinstone
    source: James_Alexander_Elphinstone
    relation: :hasFather
  AddTriple (e0731f40-98ba-495c-9a76-ad84a9466739)
 Call ID: e0731f40-98ba-495c-9a76-ad84a9466739
  Args:
    source: James_Alexander_Elphinstone
    target: Jean_Frances_Hambro
    relation: :hasMother
  AssignClass (a1a681f2-ea65-494f-8429-7e98bbf00be1)
 Call ID: a1a681f2-ea65-494f-8429-7e98bbf00be1
  Args:
    type: :Man
    source: Sidney_Buller-Fullerton-Elphinstone
  AssignClass (7138dc7f-5dff-47f1-a910-f10ce0f1b27b)
 Call ID: 7138dc7f-5dff-47f1-a910-f10ce0f1b27b
  Args:
    type: :Person
    source: Sidney_Buller-Fullerton-Elphinstone
  AssignClass (db864a59-6dd6-4372-a500-ce6be78ff05b)
 Call ID: db864a59-6dd6-4372-a500-ce6be78ff05b
  Args:
    type: :Woman
    source: Mary_Bowes-Lyon
  AssignClass (bf98430c-0053-45a7-828b-623fe57bf3e0)
 Call ID: bf98430c-0053-45a7-828b-623fe57bf3e0
  Args:
    type: :Person
    source: Mary_Bowes-Lyon
  AddTriple (bf49e723-d90e-41fa-9f72-25a273f50df7)
 Call ID: bf49e723-d90e-41fa-9f72-25a273f50df7
  Args:
    target: Sidney_Buller-Fullerton-Elphinstone
    source: Andrew_Charles_Victor_Elphinstone
    relation: :hasFather
  AddTriple (c7c49b9e-8a83-412c-a3ac-04af4edcdc6d)
 Call ID: c7c49b9e-8a83-412c-a3ac-04af4edcdc6d
  Args:
    target: Mary_Bowes-Lyon
    source: Andrew_Charles_Victor_Elphinstone
    relation: :hasMother
  AssignClass (e207c269-c206-44be-ad15-c81ebe36cf81)
 Call ID: e207c269-c206-44be-ad15-c81ebe36cf81
  Args:
    type: :Woman
    source: Willa_Mary_Gabrielle_Chetwode
  AssignClass (e96c2e21-c36c-4b21-b2f4-b577a149ffd6)
 Call ID: e96c2e21-c36c-4b21-b2f4-b577a149ffd6
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Person
  AddTriple (54ad3b95-31fa-40bb-a03d-aec3acdebbfa)
 Call ID: 54ad3b95-31fa-40bb-a03d-aec3acdebbfa
  Args:
    relation: :hasRelation
    target: Willa_Mary_Gabrielle_Chetwode
    source: James_Alexander_Elphinstone
  AddLiteral (b72da2ed-0362-47d8-ab44-6e095ef795b0)
 Call ID: b72da2ed-0362-47d8-ab44-6e095ef795b0
  Args:
    source: James_Alexander_Elphinstone
    literal_value: 1978
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (669738c2-8119-45e2-95e4-789b902c5c36)
 Call ID: 669738c2-8119-45e2-95e4-789b902c5c36
  Args:
    source: George_David_Chetwode
    type: :Man
  AssignClass (18d0b871-ac82-4646-804e-304bdcac9c6e)
 Call ID: 18d0b871-ac82-4646-804e-304bdcac9c6e
  Args:
    type: :Person
    source: George_David_Chetwode
  AssignClass (78ff3b47-e330-4ded-a092-4f9f58e822a9)
 Call ID: 78ff3b47-e330-4ded-a092-4f9f58e822a9
  Args:
    source: Willa_Elliot-Murray-Kynynmound
    type: :Woman
  AssignClass (5a55fb0a-34d7-4bc6-9946-d680f8586283)
 Call ID: 5a55fb0a-34d7-4bc6-9946-d680f8586283
  Args:
    type: :Person
    source: Willa_Elliot-Murray-Kynynmound
  AddTriple (9e162ad7-fb71-43ed-961a-ff5f8999cb35)
 Call ID: 9e162ad7-fb71-43ed-961a-ff5f8999cb35
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    target: George_David_Chetwode
    relation: :hasFather
  AddTriple (ee75a8e2-c88a-4f54-99f7-bb5dacdd2d9d)
 Call ID: ee75a8e2-c88a-4f54-99f7-bb5dacdd2d9d
  Args:
    relation: :hasMother
    target: Willa_Elliot-Murray-Kynynmound
    source: Willa_Mary_Gabrielle_Chetwode
  AssignClass (c81564ce-76ab-45bc-a93f-dc5d8e570f32)
 Call ID: c81564ce-76ab-45bc-a93f-dc5d8e570f32
  Args:
    source: Victor_Elliot-Murray-Kynynmound
    type: :Man
  AssignClass (ce867015-b758-4615-98bb-5d2c56224032)
 Call ID: ce867015-b758-4615-98bb-5d2c56224032
  Args:
    type: :Person
    source: Victor_Elliot-Murray-Kynynmound
  AssignClass (5d1e900c-9ebd-4e28-881a-bd811ed61196)
 Call ID: 5d1e900c-9ebd-4e28-881a-bd811ed61196
  Args:
    source: Marion_Cook
    type: :Woman
  AssignClass (9846972a-3dd9-4b49-b963-59a2686e0cd0)
 Call ID: 9846972a-3dd9-4b49-b963-59a2686e0cd0
  Args:
    source: Marion_Cook
    type: :Person
  AddTriple (826d40e1-38da-452c-9b33-bf70294061d7)
 Call ID: 826d40e1-38da-452c-9b33-bf70294061d7
  Args:
    target: Victor_Elliot-Murray-Kynynmound
    source: Willa_Elliot-Murray-Kynynmound
    relation: :hasFather
  AddTriple (96a0a0ba-7882-410f-9022-6c2a89d9cfce)
 Call ID: 96a0a0ba-7882-410f-9022-6c2a89d9cfce
  Args:
    target: Marion_Cook
    source: Willa_Elliot-Murray-Kynynmound
    relation: :hasMother
  AssignClass (f5560dcb-82e9-4927-9fc7-30094dddb072)
 Call ID: f5560dcb-82e9-4927-9fc7-30094dddb072
  Args:
    source: Alexander
    type: :Man
  AssignClass (15b333df-84ea-4069-86cd-8f04d9905992)
 Call ID: 15b333df-84ea-4069-86cd-8f04d9905992
  Args:
    type: :Person
    source: Alexander
  AddTriple (a3fb4884-e22b-46e5-b385-0e7a638b3022)
 Call ID: a3fb4884-e22b-46e5-b385-0e7a638b3022
  Args:
    target: Alexander
    source: James_Alexander_Elphinstone
    relation: :hasSon
  Finish (7ee991a7-cfa0-46f7-a843-7e5f717b0870)
 Call ID: 7ee991a7-cfa0-46f7-a843-7e5f717b0870
  Args: