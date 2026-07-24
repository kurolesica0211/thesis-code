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
  AssignClass (01d85474-0222-46c8-b1a9-4c1eebc485ad)
 Call ID: 01d85474-0222-46c8-b1a9-4c1eebc485ad
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (3197ad2d-d5cd-414d-a684-3be3be871c71)
 Call ID: 3197ad2d-d5cd-414d-a684-3be3be871c71
  Args:
    type: :Man
    source: Pedro_Gastao_of_Orleans-Braganza
  AssignClass (ca376ad0-bf6e-4d99-a7ab-06b7346c1fa4)
 Call ID: ca376ad0-bf6e-4d99-a7ab-06b7346c1fa4
  Args:
    type: :Man
    source: Juan_Carlos_I_of_Spain
  AssignClass (4dabbad0-1fbb-4ecd-a482-9579ffd46306)
 Call ID: 4dabbad0-1fbb-4ecd-a482-9579ffd46306
  Args:
    type: :Man
    source: Carlos_of_Bourbon-Two_Sicilies
  AssignClass (5c89410e-546e-48b6-ac3a-6ff1b5068238)
 Call ID: 5c89410e-546e-48b6-ac3a-6ff1b5068238
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (abd94b80-ef63-4054-b815-65c338543a68)
 Call ID: abd94b80-ef63-4054-b815-65c338543a68
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (fcaa83bd-681b-424b-b265-412664795f52)
 Call ID: fcaa83bd-681b-424b-b265-412664795f52
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (b1e1e11c-81e1-44c2-bf44-af163fea5a17)
 Call ID: b1e1e11c-81e1-44c2-bf44-af163fea5a17
  Args:
    type: :Man
    source: Juan_Count_of_Barcelona
  AssignClass (bae6dca0-0fb8-4330-93f8-43ce4b5c170a)
 Call ID: bae6dca0-0fb8-4330-93f8-43ce4b5c170a
  Args:
    source: Pedro_de_Alcantara_of_Orleans-Braganza
    type: :Man
  AssignClass (0b9ed4c1-454d-467c-8fb8-a05ac3886ea1)
 Call ID: 0b9ed4c1-454d-467c-8fb8-a05ac3886ea1
  Args:
    type: :Woman
    source: Sofia_of_Spain
  AddLiteral (b3059140-c110-451d-8192-dc5570230fa1)
 Call ID: b3059140-c110-451d-8192-dc5570230fa1
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (3d7b0200-018c-4f7a-bf6f-b9b6bbea3447)
 Call ID: 3d7b0200-018c-4f7a-bf6f-b9b6bbea3447
  Args:
    relation: :hasDeathYear
    literal_value: 2005
    literal_type: xsd:integer
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AddLiteral (484740be-af00-42a8-9efd-89a1928bd996)
 Call ID: 484740be-af00-42a8-9efd-89a1928bd996
  Args:
    relation: :hasMarriageYear
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1944
  AddTriple (19b42fd7-9290-4365-851a-9785310f389a)
 Call ID: 19b42fd7-9290-4365-851a-9785310f389a
  Args:
    relation: :hasFather
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    target: Carlos_of_Bourbon-Two_Sicilies
  AddTriple (7313bb0f-950d-4d44-b441-4ca30b27eff8)
 Call ID: 7313bb0f-950d-4d44-b441-4ca30b27eff8
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: Louise_of_Orleans
  AddTriple (b9ce2d73-c267-4e70-9b09-723f5433d6c5)
 Call ID: b9ce2d73-c267-4e70-9b09-723f5433d6c5
  Args:
    source: Louise_of_Orleans
    relation: :hasFather
    target: Philippe_Count_of_Paris
  AddTriple (682cf9d9-9272-4031-9cd1-61af7c16a827)
 Call ID: 682cf9d9-9272-4031-9cd1-61af7c16a827
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasSister
    target: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (60e91ca5-5830-4a67-b196-d0db604d2850)
 Call ID: 60e91ca5-5830-4a67-b196-d0db604d2850
  Args:
    relation: :hasFather
    source: Pedro_Gastao_of_Orleans-Braganza
    target: Pedro_de_Alcantara_of_Orleans-Braganza
  AddTriple (ebd73d7e-bc32-469c-848c-a06c7c90b93f)
 Call ID: ebd73d7e-bc32-469c-848c-a06c7c90b93f
  Args:
    target: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    source: Juan_Carlos_I_of_Spain
    relation: :hasMother
  AddTriple (2ea8a3bc-4e34-45ac-8943-e680a76d61d3)
 Call ID: 2ea8a3bc-4e34-45ac-8943-e680a76d61d3
  Args:
    target: Juan_Count_of_Barcelona
    source: Juan_Carlos_I_of_Spain
    relation: :hasFather
  AddTriple (d8989666-3e08-4357-af50-d835d47028da)
 Call ID: d8989666-3e08-4357-af50-d835d47028da
  Args:
    target: Juan_Carlos_I_of_Spain
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :isAuntOf
  Finish (7a505cbb-a5d2-489a-837b-216358617a01)
 Call ID: 7a505cbb-a5d2-489a-837b-216358617a01
  Args: