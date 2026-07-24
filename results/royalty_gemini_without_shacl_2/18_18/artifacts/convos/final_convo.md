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
  AssignClass (25dbb4b2-c111-41ad-b20f-95f0f3a99c35)
 Call ID: 25dbb4b2-c111-41ad-b20f-95f0f3a99c35
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (e4e30cfa-2c43-4fc3-8ce4-2f9f6c25a186)
 Call ID: e4e30cfa-2c43-4fc3-8ce4-2f9f6c25a186
  Args:
    type: :Person
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AddLiteral (f4376cf3-b154-4d2d-aaf9-6b99457230d8)
 Call ID: f4376cf3-b154-4d2d-aaf9-6b99457230d8
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1914
  AddLiteral (aa363b2f-94f2-434e-a030-7f6d1e7b90e4)
 Call ID: aa363b2f-94f2-434e-a030-7f6d1e7b90e4
  Args:
    literal_value: 2005
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (52292a8d-b98b-4afa-ad7f-3d6f55d36bd1)
 Call ID: 52292a8d-b98b-4afa-ad7f-3d6f55d36bd1
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (74129587-0812-4e9e-a1a6-0abbb615990d)
 Call ID: 74129587-0812-4e9e-a1a6-0abbb615990d
  Args:
    type: :Person
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AddTriple (1c45ae02-8297-4191-b428-94cf8f2edb07)
 Call ID: 1c45ae02-8297-4191-b428-94cf8f2edb07
  Args:
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    relation: :hasFather
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (11831e24-aefe-468b-b59d-8a61d67e80b8)
 Call ID: 11831e24-aefe-468b-b59d-8a61d67e80b8
  Args:
    source: Princess_Louise_of_Orleans
    type: :Woman
  AssignClass (22d2c7e2-a676-4fed-98df-110b44845f2b)
 Call ID: 22d2c7e2-a676-4fed-98df-110b44845f2b
  Args:
    source: Princess_Louise_of_Orleans
    type: :Person
  AddTriple (c389fc0e-bf1a-4a67-891c-3c22333b7997)
 Call ID: c389fc0e-bf1a-4a67-891c-3c22333b7997
  Args:
    target: Princess_Louise_of_Orleans
    relation: :hasMother
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (80eaf28b-0bfc-41e9-ae8d-43887a4afa67)
 Call ID: 80eaf28b-0bfc-41e9-ae8d-43887a4afa67
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (d038cc9b-1186-41e6-9488-ce4acd9577fa)
 Call ID: d038cc9b-1186-41e6-9488-ce4acd9577fa
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AddTriple (63b27e5e-4b1b-498c-8294-2bb7d9b4dd2d)
 Call ID: 63b27e5e-4b1b-498c-8294-2bb7d9b4dd2d
  Args:
    relation: :hasFather
    source: Princess_Louise_of_Orleans
    target: Philippe_Count_of_Paris
  AssignClass (2db24e49-fbbc-4402-9186-ce2453496366)
 Call ID: 2db24e49-fbbc-4402-9186-ce2453496366
  Args:
    source: Princess_Maria_de_las_Mercedes
    type: :Woman
  AssignClass (0421a946-0e29-4ae6-aeb8-3ef0ba607306)
 Call ID: 0421a946-0e29-4ae6-aeb8-3ef0ba607306
  Args:
    type: :Person
    source: Princess_Maria_de_las_Mercedes
  AddTriple (0db32575-23f6-4d18-8764-6c3304853905)
 Call ID: 0db32575-23f6-4d18-8764-6c3304853905
  Args:
    relation: :isSisterOf
    source: Princess_Maria_de_las_Mercedes
    target: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (0b58a7ce-ebe8-40e7-9a06-65dc8f2d6b22)
 Call ID: 0b58a7ce-ebe8-40e7-9a06-65dc8f2d6b22
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Man
  AssignClass (bef87eec-d4d9-4ff4-8b16-952e8c18ba57)
 Call ID: bef87eec-d4d9-4ff4-8b16-952e8c18ba57
  Args:
    type: :Person
    source: Infante_Juan_Count_of_Barcelona
  AddTriple (d17f8a67-5184-4a36-80e9-5b3dc4b84ea3)
 Call ID: d17f8a67-5184-4a36-80e9-5b3dc4b84ea3
  Args:
    source: King_Juan_Carlos_I
    relation: :hasMother
    target: Princess_Maria_de_las_Mercedes
  AddTriple (cc75352d-f464-437e-8fde-4bf1effc5485)
 Call ID: cc75352d-f464-437e-8fde-4bf1effc5485
  Args:
    source: King_Juan_Carlos_I
    relation: :hasFather
    target: Infante_Juan_Count_of_Barcelona
  AssignClass (aa3daf3c-8ae9-48c1-b173-822d6fac09be)
 Call ID: aa3daf3c-8ae9-48c1-b173-822d6fac09be
  Args:
    source: King_Juan_Carlos_I
    type: :Man
  AssignClass (679fdadd-0dae-4b67-817b-8e87851761ef)
 Call ID: 679fdadd-0dae-4b67-817b-8e87851761ef
  Args:
    type: :Person
    source: King_Juan_Carlos_I
  AssignClass (1e188ac2-166a-4f26-bcb3-a2cf638366be)
 Call ID: 1e188ac2-166a-4f26-bcb3-a2cf638366be
  Args:
    type: :Man
    source: Prince_Pedro_Gastao_of_Orleans-Braganza
  AssignClass (5f009f08-35c7-4df4-b6d8-49b3fc4c6642)
 Call ID: 5f009f08-35c7-4df4-b6d8-49b3fc4c6642
  Args:
    type: :Person
    source: Prince_Pedro_Gastao_of_Orleans-Braganza
  AddLiteral (cb58e95e-a66b-46de-a656-f0c7a1a25758)
 Call ID: cb58e95e-a66b-46de-a656-f0c7a1a25758
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1944
  AddTriple (0d100c60-4195-4171-979c-495a13962c29)
 Call ID: 0d100c60-4195-4171-979c-495a13962c29
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Prince_Pedro_Gastao_of_Orleans-Braganza
  AssignClass (4a285c7c-0496-4fe2-9359-5819b7ba6b42)
 Call ID: 4a285c7c-0496-4fe2-9359-5819b7ba6b42
  Args:
    source: Prince_Pedro_de_Alcantara_of_Orleans-Braganza
    type: :Man
  AssignClass (39795bdd-ca38-4d75-9eed-dfebb1cdf52e)
 Call ID: 39795bdd-ca38-4d75-9eed-dfebb1cdf52e
  Args:
    type: :Person
    source: Prince_Pedro_de_Alcantara_of_Orleans-Braganza
  AddTriple (eb729475-599a-4546-8dc2-21482d2622b9)
 Call ID: eb729475-599a-4546-8dc2-21482d2622b9
  Args:
    target: Prince_Pedro_de_Alcantara_of_Orleans-Braganza
    source: Prince_Pedro_Gastao_of_Orleans-Braganza
    relation: :hasFather
  AssignClass (1f3d79da-c167-4dc9-8325-53c2c1a52c0a)
 Call ID: 1f3d79da-c167-4dc9-8325-53c2c1a52c0a
  Args:
    type: :Woman
    source: Queen_Sofia
  AssignClass (ff72a4ff-aece-4373-81fa-4c0d4064cbb7)
 Call ID: ff72a4ff-aece-4373-81fa-4c0d4064cbb7
  Args:
    type: :Person
    source: Queen_Sofia
  Finish (398416bc-d9af-4031-b306-6a523119e115)
 Call ID: 398416bc-d9af-4031-b306-6a523119e115
  Args: