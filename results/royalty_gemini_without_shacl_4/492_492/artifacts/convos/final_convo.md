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
Philipp, Prince of Hohenlohe-Langenburg (Philipp Gottfried Alexander; born 20 January 1970), is the head of the House of Hohenlohe-Langenburg, since the death of his father in 2004.
Early life and ancestry

He was born in Crailsheim, West Germany, the middle child and only son of Kraft, Prince of Hohenlohe-Langenburg (1935–2004) and his first wife, Princess Charlotte of Croÿ (b. 1938).
Paternally, he is a grandson of Princess Margarita of Greece and Denmark, and a grandnephew of Prince Philip, Duke of Edinburgh, whose funeral he attended.
Anne, Princess Royal is one of his godmothers.
Maternally, he is the grandson of Prince Alexander of Croy (1912–2002) and his Scottish wife, Anna Elspeth Campbell (1917–1986), granddaughter of Archibald Campbell, 6th of Glendaruel.
He sought public support from (then) Charles, Prince of Wales, the current King Charles III, and from former vice chancellor and foreign minister Joschka Fischer of the Green Party, who both attended a conference at Langenburg Castle in 2013.
Together with Fischer he founded the Langenburg Forum for Sustainability which cooperates with Charles' International Sustainability Unit


Langenburg castle is partially open to the public, including the state rooms and a museum of classic cars.
Marriage and issue

He married Saskia Binder (b. 15 January 1973 in Munich), daughter of former Deutsche Bank Munich director Hans Peter Binder, on 6 September 2003 in a civil ceremony at Langenburg.



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
  AssignClass (e6fe69ff-7255-4b17-b696-af6ac1982aa4)
 Call ID: e6fe69ff-7255-4b17-b696-af6ac1982aa4
  Args:
    type: :Man
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AssignClass (3b739791-92e6-4a14-ad79-72c7b11c3e17)
 Call ID: 3b739791-92e6-4a14-ad79-72c7b11c3e17
  Args:
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (57ab23b5-8b8a-4d4f-8b10-8fca8b019c99)
 Call ID: 57ab23b5-8b8a-4d4f-8b10-8fca8b019c99
  Args:
    type: :Woman
    source: Princess_Charlotte_of_Croy
  AssignClass (3f882442-85ae-40c8-8649-61bc1f224495)
 Call ID: 3f882442-85ae-40c8-8649-61bc1f224495
  Args:
    type: :Woman
    source: Princess_Margarita_of_Greece_and_Denmark
  AssignClass (6da3e4ad-e929-4fe0-9d17-7951fc5d2452)
 Call ID: 6da3e4ad-e929-4fe0-9d17-7951fc5d2452
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (aeac2b24-cd8b-4977-bd1a-35d2ac96eee9)
 Call ID: aeac2b24-cd8b-4977-bd1a-35d2ac96eee9
  Args:
    type: :Woman
    source: Anne_Princess_Royal
  AssignClass (42a980cb-97f2-4686-a327-a674a2ca6588)
 Call ID: 42a980cb-97f2-4686-a327-a674a2ca6588
  Args:
    type: :Man
    source: Prince_Alexander_of_Croy
  AssignClass (f92d73ee-2dc1-4cbc-a47e-45ce2182310a)
 Call ID: f92d73ee-2dc1-4cbc-a47e-45ce2182310a
  Args:
    type: :Woman
    source: Anna_Elspeth_Campbell
  AssignClass (5a8c9238-ae07-4474-9cdf-54e1402a4549)
 Call ID: 5a8c9238-ae07-4474-9cdf-54e1402a4549
  Args:
    type: :Man
    source: Archibald_Campbell_6th_of_Glendaruel
  AssignClass (a7dab61c-8a76-4c2e-8113-e8b55ffa4069)
 Call ID: a7dab61c-8a76-4c2e-8113-e8b55ffa4069
  Args:
    source: Saskia_Binder
    type: :Woman
  AssignClass (ac68e39d-a7a9-4246-878e-2fdf5280dc3e)
 Call ID: ac68e39d-a7a9-4246-878e-2fdf5280dc3e
  Args:
    source: Hans_Peter_Binder
    type: :Man
  AddLiteral (ff535e16-359c-4a4f-a623-00b0860b78c0)
 Call ID: ff535e16-359c-4a4f-a623-00b0860b78c0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_value: 1970
  AddLiteral (dd30562c-39dd-41ec-b850-4de7db21e068)
 Call ID: dd30562c-39dd-41ec-b850-4de7db21e068
  Args:
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    literal_value: 1935
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (ec939998-0c7f-464b-bbe6-06a618cec28c)
 Call ID: ec939998-0c7f-464b-bbe6-06a618cec28c
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    literal_value: 2004
  AddLiteral (b65811b3-e77f-44c5-971d-f4094987f582)
 Call ID: b65811b3-e77f-44c5-971d-f4094987f582
  Args:
    source: Princess_Charlotte_of_Croy
    literal_value: 1938
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (df881f16-8620-4071-b97c-3ea8e5687752)
 Call ID: df881f16-8620-4071-b97c-3ea8e5687752
  Args:
    source: Prince_Alexander_of_Croy
    literal_value: 1912
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (569cedee-2523-4cd1-b4cc-57d3fef6b5b8)
 Call ID: 569cedee-2523-4cd1-b4cc-57d3fef6b5b8
  Args:
    source: Prince_Alexander_of_Croy
    literal_value: 2002
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (5471ca54-3d32-476a-b1b6-9dcc5278bfc4)
 Call ID: 5471ca54-3d32-476a-b1b6-9dcc5278bfc4
  Args:
    literal_value: 1917
    source: Anna_Elspeth_Campbell
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (fb29faec-7231-4bb7-81c3-64c596092f5f)
 Call ID: fb29faec-7231-4bb7-81c3-64c596092f5f
  Args:
    source: Anna_Elspeth_Campbell
    literal_value: 1986
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (35c47987-7094-4230-90bf-1dabd09c0d68)
 Call ID: 35c47987-7094-4230-90bf-1dabd09c0d68
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1973
    source: Saskia_Binder
  AddLiteral (05e35824-5340-4f7f-a656-d580e3613df5)
 Call ID: 05e35824-5340-4f7f-a656-d580e3613df5
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2003
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AddTriple (6d4ee987-64b8-4ef2-8ee5-88a23848246f)
 Call ID: 6d4ee987-64b8-4ef2-8ee5-88a23848246f
  Args:
    relation: :hasFather
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Kraft_Prince_of_Hohenlohe-Langenburg
  AddTriple (80fda714-f7f5-4029-b4a0-37b110625a19)
 Call ID: 80fda714-f7f5-4029-b4a0-37b110625a19
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Princess_Charlotte_of_Croy
    relation: :hasMother
  AddTriple (d72307e8-8ea1-4ecd-abdc-3f6f127e50d0)
 Call ID: d72307e8-8ea1-4ecd-abdc-3f6f127e50d0
  Args:
    source: Princess_Charlotte_of_Croy
    target: Prince_Alexander_of_Croy
    relation: :hasFather
  AddTriple (b1bb5c65-15aa-44ca-a44a-4b8b9b0d02ba)
 Call ID: b1bb5c65-15aa-44ca-a44a-4b8b9b0d02ba
  Args:
    relation: :hasMother
    source: Princess_Charlotte_of_Croy
    target: Anna_Elspeth_Campbell
  AddTriple (5ee49747-ec8c-4df5-806e-f8962f57550e)
 Call ID: 5ee49747-ec8c-4df5-806e-f8962f57550e
  Args:
    relation: :hasFather
    source: Anna_Elspeth_Campbell
    target: Archibald_Campbell_6th_of_Glendaruel
  AddTriple (2e5e17a6-00c0-4f78-b5f8-3f8db16478d4)
 Call ID: 2e5e17a6-00c0-4f78-b5f8-3f8db16478d4
  Args:
    relation: :hasFather
    target: Hans_Peter_Binder
    source: Saskia_Binder
  Finish (ae6aa4b5-c414-4f5c-826a-385b862a29ed)
 Call ID: ae6aa4b5-c414-4f5c-826a-385b862a29ed
  Args: