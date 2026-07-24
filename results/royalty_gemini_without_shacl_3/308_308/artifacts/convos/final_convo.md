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
Paul Dmitrievich Romanovsky-Ilyinsky (January 27, 1928 – February 10, 2004) was a three-time mayor of Palm Beach, Florida, and the only child of Grand Duke Dmitri Pavlovich of Russia and his morganatic wife, Cincinnati heiress Audrey Emery.
He was a great-grandson of Tsar Alexander II of Russia and, following the death of Grand Duke Vladimir Kirillovich in 1992, the heir-male of the Ilyinsky claim of the House of Romanov (a position now held by his elder son), a first cousin once removed of Nicholas II, first cousin of Prince Lennart of Sweden, Duke of Småland and the second cousin of Charles III.
Early life

Prince Paul Romanovsky-Ilyinsky was born on 27 January 1928 at his parents' home, 26 Manchester Square, London.
His father, Grand Duke Dmitri, as a direct consequence of his involvement in the murder of Grigori Rasputin in 1916, had been sent to the Persian front, which ultimately saved his life, as many of his Imperial relatives were executed by the Bolsheviks during the October Revolution .
Dmitri, who was working as a champagne salesman, married Cincinnati heiress Audrey Emery in 1926.
Grand Duke Cyril Vladimirovich of Russia, Dmitri's cousin and the self-proclaimed emperor in exile, elevated Grand Duke Dmitri's wife and their descendants to Russian princely (Russian: knyaz) rank (rank of nobility, not royalty).
Any children the couple would have would be known as Romanovsky-Ilyinsky, the latter half of the surname derived from Dmitri's former property in Russia, Ilinskoe.
Ilynskiy's parents were divorced in 1937, and Ilyinsky was raised by his mother, who mostly lived in France.
Dmitri Pavlovich's health had always been somewhat frail, and in the 1930s, his chronic tuberculosis became acute, leading to his death in 1942.
Education and career

Ilyinsky, who was a U.S. citizen, attended Woodberry Forest School in Virginia and the Royal Military Academy Sandhurst, England, before joining the U.S. Marine Corps.
Ilyinsky lived in Cincinnati for about 20 years, serving on the board of the company founded by his mother's family, Emery Industries, and working as an author and photographer.
Ilyinsky died at his home in Palm Beach, Florida, on February 10, 2004.
Personal life

Ilyinsky was married twice; he married his first wife, Mary Evelyn Prince in 1948 (annulment in 1951), and married his second wife, Angelica Philippa Kauffmann in 1953.
Ilyinsky had four children:


Ancestry

References



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
  AssignClass (a6919c6b-35e6-4ec9-8947-c4ad11c4c00c)
 Call ID: a6919c6b-35e6-4ec9-8947-c4ad11c4c00c
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    type: :Man
  AssignClass (926785ac-7668-4c1c-bad6-e2159f313f50)
 Call ID: 926785ac-7668-4c1c-bad6-e2159f313f50
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    type: :Person
  AddLiteral (06c7d5be-2dbf-4f32-a2db-3194df698bcc)
 Call ID: 06c7d5be-2dbf-4f32-a2db-3194df698bcc
  Args:
    relation: :hasBirthYear
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_value: 1928
    literal_type: xsd:integer
  AddLiteral (75572c91-60a7-4558-97cb-bc932d82c25d)
 Call ID: 75572c91-60a7-4558-97cb-bc932d82c25d
  Args:
    relation: :hasDeathYear
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    literal_value: 2004
    literal_type: xsd:integer
  AssignClass (0e16ec56-8ac5-4a93-9103-4f02faf00f42)
 Call ID: 0e16ec56-8ac5-4a93-9103-4f02faf00f42
  Args:
    source: Dmitri_Pavlovich_of_Russia
    type: :Man
  AssignClass (67b9ac8b-d297-4108-9633-2f178624b7ff)
 Call ID: 67b9ac8b-d297-4108-9633-2f178624b7ff
  Args:
    type: :Person
    source: Dmitri_Pavlovich_of_Russia
  AddLiteral (84eaae3f-fec3-43fa-baca-99413cfc4a96)
 Call ID: 84eaae3f-fec3-43fa-baca-99413cfc4a96
  Args:
    literal_value: 1942
    relation: :hasDeathYear
    source: Dmitri_Pavlovich_of_Russia
    literal_type: xsd:integer
  AssignClass (e2427f55-c512-4279-acf3-700a84eb4638)
 Call ID: e2427f55-c512-4279-acf3-700a84eb4638
  Args:
    type: :Woman
    source: Audrey_Emery
  AssignClass (859f0d79-874c-4145-8d41-2c8029411e41)
 Call ID: 859f0d79-874c-4145-8d41-2c8029411e41
  Args:
    type: :Person
    source: Audrey_Emery
  AddTriple (c9f9cd01-2b36-45f7-8e48-492ac0b2fb05)
 Call ID: c9f9cd01-2b36-45f7-8e48-492ac0b2fb05
  Args:
    target: Dmitri_Pavlovich_of_Russia
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    relation: :hasFather
  AddTriple (d379a3e5-cc58-4860-8586-8955bf2db775)
 Call ID: d379a3e5-cc58-4860-8586-8955bf2db775
  Args:
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    relation: :hasMother
    target: Audrey_Emery
  AddLiteral (49f810f5-efa7-4d7b-b5c9-36b29b7ffdf6)
 Call ID: 49f810f5-efa7-4d7b-b5c9-36b29b7ffdf6
  Args:
    literal_value: 1926
    relation: :hasMarriageYear
    source: Dmitri_Pavlovich_of_Russia
    literal_type: xsd:integer
  AddTriple (4009605b-1b6b-4d05-b5ec-94a239e2da31)
 Call ID: 4009605b-1b6b-4d05-b5ec-94a239e2da31
  Args:
    source: Dmitri_Pavlovich_of_Russia
    relation: :hasRelation
    target: Audrey_Emery
  AssignClass (8ad3d8e4-9982-4cb7-bdf1-5774bd3bbf57)
 Call ID: 8ad3d8e4-9982-4cb7-bdf1-5774bd3bbf57
  Args:
    source: Mary_Evelyn_Prince
    type: :Woman
  AssignClass (d05fdd73-5fa3-47d3-9987-21340f28d0b8)
 Call ID: d05fdd73-5fa3-47d3-9987-21340f28d0b8
  Args:
    type: :Person
    source: Mary_Evelyn_Prince
  AddLiteral (429ec4d7-e0f8-4196-b1f7-a7072d132223)
 Call ID: 429ec4d7-e0f8-4196-b1f7-a7072d132223
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasMarriageYear
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  AddTriple (1ea21d15-fc5f-474d-b028-bbc1b4ea07c2)
 Call ID: 1ea21d15-fc5f-474d-b028-bbc1b4ea07c2
  Args:
    relation: :hasRelation
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    target: Mary_Evelyn_Prince
  AssignClass (9ba97d43-7379-4dd3-b45f-de69ad7db046)
 Call ID: 9ba97d43-7379-4dd3-b45f-de69ad7db046
  Args:
    source: Angelica_Philippa_Kauffmann
    type: :Woman
  AssignClass (06513156-958c-4101-b8ed-4c6d3ce39c23)
 Call ID: 06513156-958c-4101-b8ed-4c6d3ce39c23
  Args:
    type: :Person
    source: Angelica_Philippa_Kauffmann
  AddLiteral (047b69c9-de85-4d38-ab2e-7410f41e43a8)
 Call ID: 047b69c9-de85-4d38-ab2e-7410f41e43a8
  Args:
    literal_value: 1953
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (7ce92e1b-c11d-4666-a0c1-ba33df4f80bd)
 Call ID: 7ce92e1b-c11d-4666-a0c1-ba33df4f80bd
  Args:
    target: Angelica_Philippa_Kauffmann
    relation: :hasRelation
    source: Paul_Dmitrievich_Romanovsky-Ilyinsky
  Finish (0c6040af-58b4-4b92-a587-787f7056cf74)
 Call ID: 0c6040af-58b4-4b92-a587-787f7056cf74
  Args: