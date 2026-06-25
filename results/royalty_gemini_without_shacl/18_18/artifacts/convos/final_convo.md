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
  AssignClass (2ab76ef0-479c-4b90-bc5e-13723059df59)
 Call ID: 2ab76ef0-479c-4b90-bc5e-13723059df59
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (f5372fb9-0065-4fa0-af71-12aa9cb0ecd5)
 Call ID: f5372fb9-0065-4fa0-af71-12aa9cb0ecd5
  Args:
    type: :Person
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AddLiteral (3e68e5be-73d0-45f8-8420-3de1a25c1471)
 Call ID: 3e68e5be-73d0-45f8-8420-3de1a25c1471
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1914
    relation: :hasBirthYear
  AddLiteral (d39a915b-f6cb-471c-8c1e-bd83c082ad34)
 Call ID: d39a915b-f6cb-471c-8c1e-bd83c082ad34
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2005
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (8eb7b8d6-5f23-4d36-810e-b50da152f828)
 Call ID: 8eb7b8d6-5f23-4d36-810e-b50da152f828
  Args:
    type: :Man
    source: Prince_Pedro_Gastao_of_Orleans-Braganza
  AssignClass (e24d832f-a4a6-4ad1-8e09-75e33fb256fd)
 Call ID: e24d832f-a4a6-4ad1-8e09-75e33fb256fd
  Args:
    source: Prince_Pedro_Gastao_of_Orleans-Braganza
    type: :Person
  AddTriple (3cde512b-f9f2-449f-895a-efb1f3263bfe)
 Call ID: 3cde512b-f9f2-449f-895a-efb1f3263bfe
  Args:
    target: Prince_Pedro_Gastao_of_Orleans-Braganza
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (4838c514-acbe-464d-8321-d2008a59a705)
 Call ID: 4838c514-acbe-464d-8321-d2008a59a705
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1944
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (67b3b50f-92ee-47a8-a018-38c9da275182)
 Call ID: 67b3b50f-92ee-47a8-a018-38c9da275182
  Args:
    source: King_Juan_Carlos_I_of_Spain
    type: :Man
  AssignClass (55f49cb7-0186-4dcc-a340-c2c592edf422)
 Call ID: 55f49cb7-0186-4dcc-a340-c2c592edf422
  Args:
    type: :Person
    source: King_Juan_Carlos_I_of_Spain
  AddTriple (631c8089-6654-4406-9b1e-2fb2bd38c6a4)
 Call ID: 631c8089-6654-4406-9b1e-2fb2bd38c6a4
  Args:
    target: King_Juan_Carlos_I_of_Spain
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :isAuntOf
  AssignClass (9b4162e6-b367-4b5a-89ac-2ce9a07e9fb4)
 Call ID: 9b4162e6-b367-4b5a-89ac-2ce9a07e9fb4
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (aad3ecc5-f049-43ed-a266-7e5ec6ce2d38)
 Call ID: aad3ecc5-f049-43ed-a266-7e5ec6ce2d38
  Args:
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (9981745a-3753-4fbc-b473-a6a6c57bf7bb)
 Call ID: 9981745a-3753-4fbc-b473-a6a6c57bf7bb
  Args:
    relation: :hasFather
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (4025dd47-1124-4376-bc5a-cdc73620ecbc)
 Call ID: 4025dd47-1124-4376-bc5a-cdc73620ecbc
  Args:
    source: Princess_Louise_of_Orleans
    type: :Woman
  AssignClass (7a3ae055-20b4-4d84-9a59-6df7e49c3c1b)
 Call ID: 7a3ae055-20b4-4d84-9a59-6df7e49c3c1b
  Args:
    type: :Person
    source: Princess_Louise_of_Orleans
  AddTriple (35113783-d247-477a-8936-54d540837aa2)
 Call ID: 35113783-d247-477a-8936-54d540837aa2
  Args:
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: Princess_Louise_of_Orleans
  AssignClass (45db567b-6e02-48b2-b020-a1d97c2f5f07)
 Call ID: 45db567b-6e02-48b2-b020-a1d97c2f5f07
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (5fadf472-11ca-416c-a0c1-85865cdb91bc)
 Call ID: 5fadf472-11ca-416c-a0c1-85865cdb91bc
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AddTriple (6c7448d8-a375-40c6-bca6-ef7b9309286f)
 Call ID: 6c7448d8-a375-40c6-bca6-ef7b9309286f
  Args:
    target: Philippe_Count_of_Paris
    source: Princess_Louise_of_Orleans
    relation: :hasFather
  AssignClass (381ac310-9013-4d73-b924-ef147ae79863)
 Call ID: 381ac310-9013-4d73-b924-ef147ae79863
  Args:
    source: Princess_Maria_de_las_Mercedes
    type: :Woman
  AssignClass (8abbdb3e-6a07-4ffd-a376-d24c1fb553c5)
 Call ID: 8abbdb3e-6a07-4ffd-a376-d24c1fb553c5
  Args:
    source: Princess_Maria_de_las_Mercedes
    type: :Person
  AddTriple (a47990e1-96ab-4d8e-a683-d5473b26a620)
 Call ID: a47990e1-96ab-4d8e-a683-d5473b26a620
  Args:
    target: Princess_Maria_de_las_Mercedes
    relation: :hasSister
    source: Maria_de_la_Esperanza_of_Bourbon-Two_Sicilies
  AssignClass (131b810d-0684-448d-be9d-dbbbedff3529)
 Call ID: 131b810d-0684-448d-be9d-dbbbedff3529
  Args:
    type: :Man
    source: Infante_Juan_Count_of_Barcelona
  AssignClass (dbc731b8-bcc8-4437-accc-66fb9d8752bc)
 Call ID: dbc731b8-bcc8-4437-accc-66fb9d8752bc
  Args:
    source: Infante_Juan_Count_of_Barcelona
    type: :Person
  AddTriple (2a8e34d1-088e-423f-83cf-963f52b16bc1)
 Call ID: 2a8e34d1-088e-423f-83cf-963f52b16bc1
  Args:
    target: Princess_Maria_de_las_Mercedes
    relation: :hasMother
    source: King_Juan_Carlos_I_of_Spain
  AddTriple (eafbeb90-eda5-4063-99a6-cdb2e4943f9e)
 Call ID: eafbeb90-eda5-4063-99a6-cdb2e4943f9e
  Args:
    target: Infante_Juan_Count_of_Barcelona
    source: King_Juan_Carlos_I_of_Spain
    relation: :hasFather
  AssignClass (fc1b47c2-9f35-4a64-a75f-f8534fcf53e5)
 Call ID: fc1b47c2-9f35-4a64-a75f-f8534fcf53e5
  Args:
    type: :Man
    source: Prince_Pedro_de_Alcantara_of_Orleans-Braganza
  AssignClass (7ee4425d-ea9c-42df-94f2-b5e70b810f39)
 Call ID: 7ee4425d-ea9c-42df-94f2-b5e70b810f39
  Args:
    type: :Person
    source: Prince_Pedro_de_Alcantara_of_Orleans-Braganza
  AddTriple (9b3a20c2-3eb3-4fcc-8e1d-f646d22d784c)
 Call ID: 9b3a20c2-3eb3-4fcc-8e1d-f646d22d784c
  Args:
    target: Prince_Pedro_de_Alcantara_of_Orleans-Braganza
    relation: :hasFather
    source: Prince_Pedro_Gastao_of_Orleans-Braganza
  AssignClass (9c4c6394-e59d-40b2-a7f7-0bc429fa4062)
 Call ID: 9c4c6394-e59d-40b2-a7f7-0bc429fa4062
  Args:
    source: Queen_Sofia_of_Spain
    type: :Woman
  AssignClass (a9650682-213c-42c7-9ad6-38371eeaa1ee)
 Call ID: a9650682-213c-42c7-9ad6-38371eeaa1ee
  Args:
    type: :Person
    source: Queen_Sofia_of_Spain
  Finish (d2a78481-3ac6-4554-9dea-f7625d4409d1)
 Call ID: d2a78481-3ac6-4554-9dea-f7625d4409d1
  Args: