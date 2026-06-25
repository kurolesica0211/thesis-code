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
  AssignClass (32afde72-b79e-4cac-8085-72ca5c28ec0b)
 Call ID: 32afde72-b79e-4cac-8085-72ca5c28ec0b
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    type: :Person
  AssignClass (4cebda71-10df-4e46-817d-db79fea5f226)
 Call ID: 4cebda71-10df-4e46-817d-db79fea5f226
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    type: :Woman
  AddLiteral (f1950b39-f9d8-4bf4-9a2e-1d40128ed5e2)
 Call ID: f1950b39-f9d8-4bf4-9a2e-1d40128ed5e2
  Args:
    literal_value: 1904
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
  AddLiteral (64f67e3c-19e7-4661-af63-e48cce4de249)
 Call ID: 64f67e3c-19e7-4661-af63-e48cce4de249
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1985
  AssignClass (8534414e-eb62-4b10-8888-58442989543c)
 Call ID: 8534414e-eb62-4b10-8888-58442989543c
  Args:
    source: :Prince_Carlos_of_Bourbon_Two_Sicilies
    type: :Person
  AssignClass (0a2a6db7-8871-4a58-adac-2688f8510d8e)
 Call ID: 0a2a6db7-8871-4a58-adac-2688f8510d8e
  Args:
    source: :Prince_Carlos_of_Bourbon_Two_Sicilies
    type: :Man
  AssignClass (fcaefd30-8aa5-411f-8244-073541e21f4f)
 Call ID: fcaefd30-8aa5-411f-8244-073541e21f4f
  Args:
    type: :Person
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (d22e74a2-1053-46b7-9970-e1f2ff98fec3)
 Call ID: d22e74a2-1053-46b7-9970-e1f2ff98fec3
  Args:
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
    type: :Woman
  AddTriple (74b4bd74-2b2a-44bb-ade3-194ab2348d92)
 Call ID: 74b4bd74-2b2a-44bb-ade3-194ab2348d92
  Args:
    target: :Prince_Carlos_of_Bourbon_Two_Sicilies
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    relation: :hasFather
  AddTriple (a9ae0a8a-77d5-4863-b236-8352ba1df5a6)
 Call ID: a9ae0a8a-77d5-4863-b236-8352ba1df5a6
  Args:
    relation: :hasMother
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    target: :Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (1fbea287-fc6c-4211-a3e7-b7687a15ef07)
 Call ID: 1fbea287-fc6c-4211-a3e7-b7687a15ef07
  Args:
    source: :Alfonso_XII_of_Spain
    type: :Person
  AssignClass (5dc3e436-171a-4fdb-8c60-aefe19dea0e2)
 Call ID: 5dc3e436-171a-4fdb-8c60-aefe19dea0e2
  Args:
    type: :Man
    source: :Alfonso_XII_of_Spain
  AssignClass (2a01c38e-874c-4c26-8be4-fcb7f7152a61)
 Call ID: 2a01c38e-874c-4c26-8be4-fcb7f7152a61
  Args:
    source: :Maria_Christina_of_Austria
    type: :Person
  AssignClass (72a53197-2228-45e5-91a8-741cc385033a)
 Call ID: 72a53197-2228-45e5-91a8-741cc385033a
  Args:
    type: :Woman
    source: :Maria_Christina_of_Austria
  AddTriple (83b9d406-b29d-41fe-a55c-276cca1a507e)
 Call ID: 83b9d406-b29d-41fe-a55c-276cca1a507e
  Args:
    relation: :hasFather
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
    target: :Alfonso_XII_of_Spain
  AddTriple (f4c8f2b7-b36b-4be8-9be8-1059194dfbbd)
 Call ID: f4c8f2b7-b36b-4be8-9be8-1059194dfbbd
  Args:
    relation: :hasMother
    target: :Maria_Christina_of_Austria
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (323cb021-e2c5-4fb2-bfd2-789a21b8cbd7)
 Call ID: 323cb021-e2c5-4fb2-bfd2-789a21b8cbd7
  Args:
    type: :Person
    source: :Jan_Kanty_Zamoyski
  AssignClass (353d46db-093f-4e42-a15e-91a059b4dd16)
 Call ID: 353d46db-093f-4e42-a15e-91a059b4dd16
  Args:
    source: :Jan_Kanty_Zamoyski
    type: :Man
  AddTriple (1da2d537-d54c-43ea-9c75-7fe05286f5a9)
 Call ID: 1da2d537-d54c-43ea-9c75-7fe05286f5a9
  Args:
    relation: :hasRelation
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    target: :Jan_Kanty_Zamoyski
  AddLiteral (d5da2966-4b0b-40d9-ac98-1d7845f52373)
 Call ID: d5da2966-4b0b-40d9-ac98-1d7845f52373
  Args:
    source: :Isabel_Alfonsa_of_Bourbon_Two_Sicilies
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1929
  AssignClass (22334e3c-f239-46af-b759-037f74401c19)
 Call ID: 22334e3c-f239-46af-b759-037f74401c19
  Args:
    source: :Andrzej_Zamoyski
    type: :Person
  AssignClass (76901ad8-452f-41be-9427-9c98a1704aec)
 Call ID: 76901ad8-452f-41be-9427-9c98a1704aec
  Args:
    type: :Man
    source: :Andrzej_Zamoyski
  AssignClass (0f472fb4-e290-4cb5-9098-6615234c4523)
 Call ID: 0f472fb4-e290-4cb5-9098-6615234c4523
  Args:
    source: :Maria_Carolina_of_Bourbon_Two_Sicilies
    type: :Person
  AssignClass (0c79df7c-f424-432d-9822-3d455f4c5409)
 Call ID: 0c79df7c-f424-432d-9822-3d455f4c5409
  Args:
    source: :Maria_Carolina_of_Bourbon_Two_Sicilies
    type: :Woman
  AddTriple (9c621da1-e2f6-466e-818b-8fce31e02970)
 Call ID: 9c621da1-e2f6-466e-818b-8fce31e02970
  Args:
    source: :Jan_Kanty_Zamoyski
    target: :Andrzej_Zamoyski
    relation: :hasFather
  AddTriple (64df5563-5963-476d-8d13-e2572b37fe94)
 Call ID: 64df5563-5963-476d-8d13-e2572b37fe94
  Args:
    target: :Maria_Carolina_of_Bourbon_Two_Sicilies
    source: :Jan_Kanty_Zamoyski
    relation: :hasMother
  Finish (365c3ac3-55ab-4d3b-9a26-3271ea41c117)
 Call ID: 365c3ac3-55ab-4d3b-9a26-3271ea41c117
  Args: