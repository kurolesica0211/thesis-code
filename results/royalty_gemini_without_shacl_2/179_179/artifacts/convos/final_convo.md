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
Princess Isabel Alfonsa of Bourbon-Two Sicilies, Infanta of Spain, (Isabel Alfonsa María Teresa Antonia Cristina Mercedes Carolina Adelaida Rafaela de Borbón-Dos Sicilias y Borbón; 16 October 1904 – 18 July 1985) was a member of the House of Bourbon-Two Sicilies and a princess of Bourbon-Two Sicilies by birth.
Family

Isabel Alfonsa was the third child of Prince Carlos of Bourbon-Two Sicilies and his first wife María de las Mercedes, Princess of Asturias.
Isabel Alfonsa's maternal grandparents were Alfonso XII of Spain and Maria Christina of Austria.
Marriage and issue

Isabel Alfonsa married her first cousin once removed Count Jan Kanty Zamoyski, seventh child and third son of Count Andrzej Zamoyski and his wife Princess Maria Carolina of Bourbon-Two Sicilies, on 9 March 1929 in Madrid.



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
  AssignClass (ba915145-01d8-4581-8d9d-54ae2ba56433)
 Call ID: ba915145-01d8-4581-8d9d-54ae2ba56433
  Args:
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (060a6b2e-3ac8-493e-bb5e-1a3841f64119)
 Call ID: 060a6b2e-3ac8-493e-bb5e-1a3841f64119
  Args:
    type: :Woman
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
  AddLiteral (3151df65-bbc2-4eb5-9bda-e4baac2050ea)
 Call ID: 3151df65-bbc2-4eb5-9bda-e4baac2050ea
  Args:
    literal_type: xsd:integer
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    literal_value: 1904
    relation: :hasBirthYear
  AddLiteral (9d1e8c7e-9f28-4b64-86fa-77906d8dc56b)
 Call ID: 9d1e8c7e-9f28-4b64-86fa-77906d8dc56b
  Args:
    literal_value: 1985
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (5b5195d2-e5f6-4ba0-9b4e-c995c6fcd347)
 Call ID: 5b5195d2-e5f6-4ba0-9b4e-c995c6fcd347
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (495a23b6-ebe2-4a4e-8284-cb2479ca8536)
 Call ID: 495a23b6-ebe2-4a4e-8284-cb2479ca8536
  Args:
    type: :Man
    source: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (22e60c43-49ca-491a-840d-ae2409c78bae)
 Call ID: 22e60c43-49ca-491a-840d-ae2409c78bae
  Args:
    target: Carlos_of_Bourbon-Two_Sicilies
    relation: :hasFather
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
  AssignClass (5816e1db-b5b9-4b89-a616-266a1361a4e3)
 Call ID: 5816e1db-b5b9-4b89-a616-266a1361a4e3
  Args:
    type: :Person
    source: Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (7452c810-5473-4482-bfeb-fad32fd3d5cc)
 Call ID: 7452c810-5473-4482-bfeb-fad32fd3d5cc
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_Princess_of_Asturias
  AddTriple (e8a2568f-557b-47be-87ae-96e14010dc93)
 Call ID: e8a2568f-557b-47be-87ae-96e14010dc93
  Args:
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (b0248177-68a0-4eef-9f89-56ad978dd154)
 Call ID: b0248177-68a0-4eef-9f89-56ad978dd154
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (f6a5fc35-5bac-4ee9-9589-fdf85ff797c0)
 Call ID: f6a5fc35-5bac-4ee9-9589-fdf85ff797c0
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (6ae0beb5-4fad-478b-94c0-4f26060487e8)
 Call ID: 6ae0beb5-4fad-478b-94c0-4f26060487e8
  Args:
    type: :Person
    source: Maria_Christina_of_Austria
  AssignClass (847a4b25-3e35-48db-ab46-cc19c706842c)
 Call ID: 847a4b25-3e35-48db-ab46-cc19c706842c
  Args:
    source: Maria_Christina_of_Austria
    type: :Woman
  AddTriple (050670f3-1250-4c54-a66a-0b7f9d246a87)
 Call ID: 050670f3-1250-4c54-a66a-0b7f9d246a87
  Args:
    relation: :isFatherOf
    source: Alfonso_XII_of_Spain
    target: Maria_de_las_Mercedes_Princess_of_Asturias
  AddTriple (0973c10c-c0b5-4dde-9da7-9d5b2e52970f)
 Call ID: 0973c10c-c0b5-4dde-9da7-9d5b2e52970f
  Args:
    source: Maria_Christina_of_Austria
    relation: :isMotherOf
    target: Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (20972e0b-d16f-40a2-bf08-74b04f187aca)
 Call ID: 20972e0b-d16f-40a2-bf08-74b04f187aca
  Args:
    source: Jan_Kanty_Zamoyski
    type: :Person
  AssignClass (6eb824fe-08bb-469e-bbc3-86938a27c16f)
 Call ID: 6eb824fe-08bb-469e-bbc3-86938a27c16f
  Args:
    source: Jan_Kanty_Zamoyski
    type: :Man
  AddTriple (01ae06fd-cb98-4b65-af73-5567b34d082a)
 Call ID: 01ae06fd-cb98-4b65-af73-5567b34d082a
  Args:
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Jan_Kanty_Zamoyski
  AddLiteral (29b98629-ffbc-46be-a79d-013f6bd45691)
 Call ID: 29b98629-ffbc-46be-a79d-013f6bd45691
  Args:
    literal_type: xsd:integer
    source: Isabel_Alfonsa_of_Bourbon-Two_Sicilies
    literal_value: 1929
    relation: :hasMarriageYear
  AssignClass (da0b3464-7415-4ff7-90a4-0aef20b87ec0)
 Call ID: da0b3464-7415-4ff7-90a4-0aef20b87ec0
  Args:
    source: Andrzej_Zamoyski
    type: :Person
  AssignClass (50d632da-854c-4725-b5b3-4350acb9d5d3)
 Call ID: 50d632da-854c-4725-b5b3-4350acb9d5d3
  Args:
    source: Andrzej_Zamoyski
    type: :Man
  AssignClass (7858f3f6-227e-461a-84aa-14ba9c2c3c63)
 Call ID: 7858f3f6-227e-461a-84aa-14ba9c2c3c63
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (fc0f275b-3b57-4d4c-a042-6145e03d515d)
 Call ID: fc0f275b-3b57-4d4c-a042-6145e03d515d
  Args:
    source: Maria_Carolina_of_Bourbon-Two_Sicilies
    type: :Woman
  AddTriple (8f05f91f-7b73-4e14-a849-1fab64a47ea7)
 Call ID: 8f05f91f-7b73-4e14-a849-1fab64a47ea7
  Args:
    target: Andrzej_Zamoyski
    source: Jan_Kanty_Zamoyski
    relation: :hasFather
  AddTriple (471f6a33-1883-4439-915a-859c4d719298)
 Call ID: 471f6a33-1883-4439-915a-859c4d719298
  Args:
    relation: :hasMother
    source: Jan_Kanty_Zamoyski
    target: Maria_Carolina_of_Bourbon-Two_Sicilies
  Finish (59869bf1-94c6-45cc-a3cd-6cacdc5e03f8)
 Call ID: 59869bf1-94c6-45cc-a3cd-6cacdc5e03f8
  Args: