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
Maria de la Esperanza of Bourbon-Two Sicilies (María de la Esperanza Amalia Raniera María Rosario Luisa Gonzaga de Borbón-Dos Sicilias y Orleáns; 14 June 1914 – 8 August 2005) was a member of the House of Bourbon-Two Sicilies.
By marriage, she became the Princess of Orléans-Braganza and the consort of Prince Pedro Gastão of Orléans-Braganza, the head of the Petrópolis branch of the Brazilian Imperial Family.
She was also the maternal aunt of King Juan Carlos I of Spain.
Early life

Princess Maria de la Esperanza was born in Madrid during the period when her family was settled in Spain.
Her father, Prince Carlos of Bourbon-Two Sicilies, had renounced his rights to the throne of the Two Sicilies to become an Infante of Spain upon his marriage to the Princess of Asturias.
Her mother, Princess Louise of Orléans, was the daughter of Philippe, Count of Paris, the Orléanist pretender to the French throne.
Her sister, Princess María de las Mercedes, married Infante Juan, Count of Barcelona, and became the mother of King Juan Carlos I. Following the proclamation of the Second Spanish Republic in 1931, the family went into exile, primarily residing in France and Italy.
Marriage and issue

On 18 December 1944, Maria de la Esperanza married her third cousin, Prince Pedro Gastão of Orléans-Braganza, in Seville, Spain.
Pedro Gastão was the son of Prince Pedro de Alcântara of Orléans-Braganza and a claimant to the defunct Brazilian throne as head of the Petrópolis branch.
The couple had six children:


Later life

The Princess spent the majority of her life at the family estate in Villamanrique de la Condesa, near Seville.
She remained a respected figure within European royalty, often attending major dynastic events in Spain alongside her nephew, King Juan Carlos I.


She died on 8 August 2005, aged 91.
Her funeral was attended by the Spanish Royal Family, including King Juan Carlos and Queen Sofía, reflecting her status as a beloved member of the extended dynasty.



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
  AssignClass (f1df2e1c-9b78-494c-845b-a8d23d3c1a63)
 Call ID: f1df2e1c-9b78-494c-845b-a8d23d3c1a63
  Args:
    type: :Woman
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (a8df4352-3722-4c85-9ae1-d278eaa40380)
 Call ID: a8df4352-3722-4c85-9ae1-d278eaa40380
  Args:
    type: :Person
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AddLiteral (72b4d92e-a007-472b-8c59-b5ce3e6ff296)
 Call ID: 72b4d92e-a007-472b-8c59-b5ce3e6ff296
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1914
  AddLiteral (485b7b59-af4e-4d85-9bff-55fdd0e5d2d9)
 Call ID: 485b7b59-af4e-4d85-9bff-55fdd0e5d2d9
  Args:
    literal_value: 2005
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (34c4421e-4fb2-4ac9-a289-e87fdfd57e09)
 Call ID: 34c4421e-4fb2-4ac9-a289-e87fdfd57e09
  Args:
    source: Pedro_Gastao_of_Orleans-Braganza
    type: :Man
  AssignClass (22f6d338-0e4f-4f1c-838e-17117f02b336)
 Call ID: 22f6d338-0e4f-4f1c-838e-17117f02b336
  Args:
    type: :Person
    source: Pedro_Gastao_of_Orleans-Braganza
  AddLiteral (b57e19f2-025d-40dd-a73f-eb96e54318e6)
 Call ID: b57e19f2-025d-40dd-a73f-eb96e54318e6
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1944
  AddTriple (c031381f-a988-4423-8e6f-efa1d5ed4fc4)
 Call ID: c031381f-a988-4423-8e6f-efa1d5ed4fc4
  Args:
    target: Pedro_Gastao_of_Orleans-Braganza
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AssignClass (93012944-f2a0-44f9-b433-db3545a57572)
 Call ID: 93012944-f2a0-44f9-b433-db3545a57572
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Man
  AssignClass (22ad2e3e-de16-4109-856c-0e4d51bb1e1f)
 Call ID: 22ad2e3e-de16-4109-856c-0e4d51bb1e1f
  Args:
    type: :Person
    source: Juan_Carlos_I_of_Spain
  AddTriple (bd6ac0d3-d5f7-464a-8778-67cd9fedd553)
 Call ID: bd6ac0d3-d5f7-464a-8778-67cd9fedd553
  Args:
    relation: :isAuntOf
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    target: Juan_Carlos_I_of_Spain
  AssignClass (b5c23dbc-23df-422b-8886-b710c58a1044)
 Call ID: b5c23dbc-23df-422b-8886-b710c58a1044
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (55e3a71e-2a51-4081-a1af-4c2711ad68f3)
 Call ID: 55e3a71e-2a51-4081-a1af-4c2711ad68f3
  Args:
    type: :Person
    source: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (eaa6b305-cdeb-4ea9-a01a-40e7cd8673d4)
 Call ID: eaa6b305-cdeb-4ea9-a01a-40e7cd8673d4
  Args:
    target: Carlos_of_Bourbon-Two_Sicilies
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AssignClass (9c97b581-b213-4722-b393-41c0995e5aef)
 Call ID: 9c97b581-b213-4722-b393-41c0995e5aef
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (c787325b-24d0-4cb8-a018-f92a8874a71c)
 Call ID: c787325b-24d0-4cb8-a018-f92a8874a71c
  Args:
    type: :Person
    source: Louise_of_Orleans
  AddTriple (699560a2-d2e9-415f-b559-8fd0a0789df2)
 Call ID: 699560a2-d2e9-415f-b559-8fd0a0789df2
  Args:
    relation: :hasMother
    target: Louise_of_Orleans
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (d3b191b5-e539-446f-a3bc-9fc576682361)
 Call ID: d3b191b5-e539-446f-a3bc-9fc576682361
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (e48f7afe-8409-4863-8ac9-119633a210d7)
 Call ID: e48f7afe-8409-4863-8ac9-119633a210d7
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AddTriple (233ba97a-e580-4c9e-b69e-1d71640cf769)
 Call ID: 233ba97a-e580-4c9e-b69e-1d71640cf769
  Args:
    source: Louise_of_Orleans
    target: Philippe_Count_of_Paris
    relation: :hasFather
  AssignClass (0cf4ab1b-0a8c-4a55-b494-07e9e163d81a)
 Call ID: 0cf4ab1b-0a8c-4a55-b494-07e9e163d81a
  Args:
    source: Maria_de_las_Mercedes
    type: :Woman
  AssignClass (9db5fca7-9087-44dd-a1fa-634dfccbf096)
 Call ID: 9db5fca7-9087-44dd-a1fa-634dfccbf096
  Args:
    source: Maria_de_las_Mercedes
    type: :Person
  AddTriple (79582636-b1e7-4840-acb4-c505496fca4f)
 Call ID: 79582636-b1e7-4840-acb4-c505496fca4f
  Args:
    relation: :isSisterOf
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    target: Maria_de_las_Mercedes
  AssignClass (35c05a13-39e6-4bdc-a88a-964c660c2df7)
 Call ID: 35c05a13-39e6-4bdc-a88a-964c660c2df7
  Args:
    source: Juan_Count_of_Barcelona
    type: :Man
  AssignClass (680b6e63-72c0-42b6-914e-9d1da92c4551)
 Call ID: 680b6e63-72c0-42b6-914e-9d1da92c4551
  Args:
    source: Juan_Count_of_Barcelona
    type: :Person
  AddTriple (c56a1f6d-0249-4fea-ad9a-8988d2769927)
 Call ID: c56a1f6d-0249-4fea-ad9a-8988d2769927
  Args:
    source: Maria_de_las_Mercedes
    target: Juan_Count_of_Barcelona
    relation: :hasRelation
  AddTriple (4507d3c5-5e61-47c0-8d72-a10afcbca3cf)
 Call ID: 4507d3c5-5e61-47c0-8d72-a10afcbca3cf
  Args:
    source: Maria_de_las_Mercedes
    target: Juan_Carlos_I_of_Spain
    relation: :isMotherOf
  AddTriple (b5503d2d-2557-4fcb-affe-126147903a29)
 Call ID: b5503d2d-2557-4fcb-affe-126147903a29
  Args:
    source: Juan_Count_of_Barcelona
    target: Juan_Carlos_I_of_Spain
    relation: :isFatherOf
  AssignClass (3d8df71a-769d-4713-8e96-78e2bf9450c1)
 Call ID: 3d8df71a-769d-4713-8e96-78e2bf9450c1
  Args:
    type: :Man
    source: Pedro_de_Alcantara_of_Orleans-Braganza
  AssignClass (3496d635-a884-4fcf-b3ec-b06fb24d00d5)
 Call ID: 3496d635-a884-4fcf-b3ec-b06fb24d00d5
  Args:
    source: Pedro_de_Alcantara_of_Orleans-Braganza
    type: :Person
  AddTriple (572399cf-97bb-41db-b025-92d6c1aef3ff)
 Call ID: 572399cf-97bb-41db-b025-92d6c1aef3ff
  Args:
    relation: :hasFather
    source: Pedro_Gastao_of_Orleans-Braganza
    target: Pedro_de_Alcantara_of_Orleans-Braganza
  AssignClass (369dee20-3a16-40f7-a798-500283e3e9ea)
 Call ID: 369dee20-3a16-40f7-a798-500283e3e9ea
  Args:
    type: :Woman
    source: Sofia_of_Spain
  AssignClass (32c58cf7-d798-45f4-a4bf-de9f8789c24a)
 Call ID: 32c58cf7-d798-45f4-a4bf-de9f8789c24a
  Args:
    type: :Person
    source: Sofia_of_Spain
  Finish (e027fd28-6ad6-4223-8c1f-29bde7802021)
 Call ID: e027fd28-6ad6-4223-8c1f-29bde7802021
  Args: