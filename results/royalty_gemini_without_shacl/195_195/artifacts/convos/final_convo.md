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
  AssignClass (01827ac4-c88d-4f0e-a755-5ffd3dac081b)
 Call ID: 01827ac4-c88d-4f0e-a755-5ffd3dac081b
  Args:
    source: James_Alexander_Elphinstone
    type: :Man
  AssignClass (af057d62-824f-4169-be00-811a3d18c9fa)
 Call ID: af057d62-824f-4169-be00-811a3d18c9fa
  Args:
    source: James_Alexander_Elphinstone
    type: :Person
  AddLiteral (8431eddc-4ff0-4698-9c4d-fe55e9ccb44d)
 Call ID: 8431eddc-4ff0-4698-9c4d-fe55e9ccb44d
  Args:
    literal_value: 1953
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: James_Alexander_Elphinstone
  AddLiteral (f988cc73-8f43-40eb-97d4-23a112ccc445)
 Call ID: f988cc73-8f43-40eb-97d4-23a112ccc445
  Args:
    literal_type: xsd:integer
    source: James_Alexander_Elphinstone
    relation: :hasDeathYear
    literal_value: 1994
  AssignClass (6c5a6fd0-23af-40af-9cfd-d62c77f0096d)
 Call ID: 6c5a6fd0-23af-40af-9cfd-d62c77f0096d
  Args:
    source: Andrew_Charles_Victor_Elphinstone
    type: :Man
  AssignClass (70b7303f-e159-433c-9d5e-49725fa9560a)
 Call ID: 70b7303f-e159-433c-9d5e-49725fa9560a
  Args:
    source: Andrew_Charles_Victor_Elphinstone
    type: :Person
  AssignClass (9957bcbf-db40-4212-9c16-f840c8010319)
 Call ID: 9957bcbf-db40-4212-9c16-f840c8010319
  Args:
    source: Jean_Frances_Hambro
    type: :Woman
  AssignClass (3093418b-1575-4a9a-882e-6a160326c1fb)
 Call ID: 3093418b-1575-4a9a-882e-6a160326c1fb
  Args:
    source: Jean_Frances_Hambro
    type: :Person
  AddTriple (1330a28e-1f50-4188-81f9-a9f38e59637f)
 Call ID: 1330a28e-1f50-4188-81f9-a9f38e59637f
  Args:
    relation: :hasFather
    target: Andrew_Charles_Victor_Elphinstone
    source: James_Alexander_Elphinstone
  AddTriple (77597d44-2187-4ef9-b1a2-0ccd2b0b24cd)
 Call ID: 77597d44-2187-4ef9-b1a2-0ccd2b0b24cd
  Args:
    source: James_Alexander_Elphinstone
    relation: :hasMother
    target: Jean_Frances_Hambro
  AssignClass (58f24776-c964-4d9a-8898-afe302afbaf8)
 Call ID: 58f24776-c964-4d9a-8898-afe302afbaf8
  Args:
    source: Sidney_Buller-Fullerton-Elphinstone
    type: :Man
  AssignClass (ee86cbb7-cc03-4f60-a5b2-86cc7f81e930)
 Call ID: ee86cbb7-cc03-4f60-a5b2-86cc7f81e930
  Args:
    source: Sidney_Buller-Fullerton-Elphinstone
    type: :Person
  AssignClass (b95837e5-1c90-4418-81bd-38742af85d8e)
 Call ID: b95837e5-1c90-4418-81bd-38742af85d8e
  Args:
    source: Mary_Bowes-Lyon
    type: :Woman
  AssignClass (a1e34963-1ffd-4685-b0b4-03be52fbe852)
 Call ID: a1e34963-1ffd-4685-b0b4-03be52fbe852
  Args:
    source: Mary_Bowes-Lyon
    type: :Person
  AddTriple (207c415e-cc2f-487e-a468-5e9f56470e32)
 Call ID: 207c415e-cc2f-487e-a468-5e9f56470e32
  Args:
    source: Andrew_Charles_Victor_Elphinstone
    relation: :hasFather
    target: Sidney_Buller-Fullerton-Elphinstone
  AddTriple (88103e7c-59a7-4afe-9bba-71eacd9820c1)
 Call ID: 88103e7c-59a7-4afe-9bba-71eacd9820c1
  Args:
    source: Andrew_Charles_Victor_Elphinstone
    target: Mary_Bowes-Lyon
    relation: :hasMother
  AssignClass (db7e0e95-d1a6-41d3-91c4-f4280381e4de)
 Call ID: db7e0e95-d1a6-41d3-91c4-f4280381e4de
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Woman
  AssignClass (e1b787a5-d3e0-48c0-8635-c3fa9a18f481)
 Call ID: e1b787a5-d3e0-48c0-8635-c3fa9a18f481
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Person
  AddLiteral (fc04372a-d56b-4708-9e27-d5a1ccc436b4)
 Call ID: fc04372a-d56b-4708-9e27-d5a1ccc436b4
  Args:
    relation: :hasMarriageYear
    literal_value: 1978
    literal_type: xsd:integer
    source: James_Alexander_Elphinstone
  AddTriple (4cbe8673-390e-4806-812b-021a6a381dc1)
 Call ID: 4cbe8673-390e-4806-812b-021a6a381dc1
  Args:
    source: James_Alexander_Elphinstone
    relation: :hasRelation
    target: Willa_Mary_Gabrielle_Chetwode
  AssignClass (4fbc5be3-97c8-42d2-91c3-3b97be1a22aa)
 Call ID: 4fbc5be3-97c8-42d2-91c3-3b97be1a22aa
  Args:
    source: George_David_Chetwode
    type: :Man
  AssignClass (5a4d2aa8-31ec-430a-9c82-1ccebb9a5978)
 Call ID: 5a4d2aa8-31ec-430a-9c82-1ccebb9a5978
  Args:
    source: George_David_Chetwode
    type: :Person
  AssignClass (022bade9-4c3a-4bf7-945a-14289f0e2638)
 Call ID: 022bade9-4c3a-4bf7-945a-14289f0e2638
  Args:
    source: Willa_Elliot-Murray-Kynynmound
    type: :Woman
  AssignClass (7addcb5d-6a7e-4cc7-8cb5-32dde7662439)
 Call ID: 7addcb5d-6a7e-4cc7-8cb5-32dde7662439
  Args:
    source: Willa_Elliot-Murray-Kynynmound
    type: :Person
  AddTriple (4aa63b8f-bbdf-422f-b6dc-9ee318f4f7c2)
 Call ID: 4aa63b8f-bbdf-422f-b6dc-9ee318f4f7c2
  Args:
    target: George_David_Chetwode
    relation: :hasFather
    source: Willa_Mary_Gabrielle_Chetwode
  AddTriple (6b8d5311-8d55-4b34-a843-567967c28471)
 Call ID: 6b8d5311-8d55-4b34-a843-567967c28471
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    target: Willa_Elliot-Murray-Kynynmound
    relation: :hasMother
  AssignClass (d2296431-3f93-42dc-b809-29664a5e21ae)
 Call ID: d2296431-3f93-42dc-b809-29664a5e21ae
  Args:
    source: Victor_Elliot-Murray-Kynynmound
    type: :Man
  AssignClass (fe953873-7263-4f56-9ef3-8ca5dd6d9da7)
 Call ID: fe953873-7263-4f56-9ef3-8ca5dd6d9da7
  Args:
    source: Victor_Elliot-Murray-Kynynmound
    type: :Person
  AssignClass (b22f1ea1-c845-41d0-87b7-fb79189f1ada)
 Call ID: b22f1ea1-c845-41d0-87b7-fb79189f1ada
  Args:
    source: Marion_Cook
    type: :Woman
  AssignClass (66ee04e2-5996-4fe1-8934-91c7efedc416)
 Call ID: 66ee04e2-5996-4fe1-8934-91c7efedc416
  Args:
    source: Marion_Cook
    type: :Person
  AddTriple (c348e363-57dc-492f-bea2-15c65c3abe93)
 Call ID: c348e363-57dc-492f-bea2-15c65c3abe93
  Args:
    target: Victor_Elliot-Murray-Kynynmound
    relation: :hasFather
    source: Willa_Elliot-Murray-Kynynmound
  AddTriple (43d68162-65b1-4874-b90b-2e01dc6b92ed)
 Call ID: 43d68162-65b1-4874-b90b-2e01dc6b92ed
  Args:
    source: Willa_Elliot-Murray-Kynynmound
    target: Marion_Cook
    relation: :hasMother
  AssignClass (43df8d54-f6ed-4de4-8513-4fada2fb02f9)
 Call ID: 43df8d54-f6ed-4de4-8513-4fada2fb02f9
  Args:
    source: Alexander_Elphinstone
    type: :Man
  AssignClass (6162cc15-23cc-4003-9331-6043f526ab84)
 Call ID: 6162cc15-23cc-4003-9331-6043f526ab84
  Args:
    source: Alexander_Elphinstone
    type: :Person
  AddTriple (113d9f17-b22e-4a32-a5f0-05237e8d1869)
 Call ID: 113d9f17-b22e-4a32-a5f0-05237e8d1869
  Args:
    relation: :hasSon
    target: Alexander_Elphinstone
    source: James_Alexander_Elphinstone
  Finish (82155b38-abb9-471c-8454-991afef57415)
 Call ID: 82155b38-abb9-471c-8454-991afef57415
  Args: