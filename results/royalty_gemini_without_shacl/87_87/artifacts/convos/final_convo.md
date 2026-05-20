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
John David James Dalrymple, 14th Earl of Stair (born 4 September 1961) is a British politician and a former crossbench member of the House of Lords.
Background

Stair is the eldest child of John Dalrymple, 13th
Earl of Stair and Davina Katherine Bowes-Lyon (2 May 1930 – 1 November 2017), daughter of David Bowes-Lyon, brother of Queen Elizabeth
Lord Stair's mother, Davina, therefore, was a first cousin of Queen Elizabeth II and he is a second cousin of The King, The Princess Royal, Andrew Mountbatten-Windsor, and The Duke of Edinburgh.
Through his mother, he is descended from the Bowes-Lyon, Astor, and Cavendish-Bentinck families.
Through his paternal-grandmother, Violet Evelyn Dalrymple (Née Harford), he is a direct descendent of Frederick Calvert, 6th Baron Baltimore, the Calvert family were the founders and Proprietors of Province of Maryland.
Political career

Upon inheriting his peerage in 1996, Lord Stair entered the House of Lords and sat as a crossbencher.
Following the death of Davina Ingrams, 18th Baroness Darcy de Knayth in 2008, Lord Stair was elected to the Lords.
Family

Lord Stair married Emily Mary Julia Stonor (daughter of Ralph Stonor, 7th Baron Camoys, and Elizabeth Mary Hyde Parker) in 2006.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (1c62bf69-01b4-46c1-9d8e-d29f75aabb9f)
 Call ID: 1c62bf69-01b4-46c1-9d8e-d29f75aabb9f
  Args:
    type: :Man
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
  AssignClass (9c18eb9d-4601-4b06-8960-ad94b86f2f52)
 Call ID: 9c18eb9d-4601-4b06-8960-ad94b86f2f52
  Args:
    type: :Person
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
  AssignClass (daf6c1a0-4cb2-4756-9edb-7ccf74d2eafd)
 Call ID: daf6c1a0-4cb2-4756-9edb-7ccf74d2eafd
  Args:
    type: :Man
    source: John_Dalrymple_13th_Earl_of_Stair
  AssignClass (e860419e-d8d1-4d82-9ff3-b333df16daf4)
 Call ID: e860419e-d8d1-4d82-9ff3-b333df16daf4
  Args:
    type: :Person
    source: John_Dalrymple_13th_Earl_of_Stair
  AssignClass (e52318a2-c32f-44f4-bf9e-532c7b410166)
 Call ID: e52318a2-c32f-44f4-bf9e-532c7b410166
  Args:
    type: :Woman
    source: Davina_Katherine_Bowes-Lyon
  AssignClass (bbe1ad22-f4e9-4a6d-9674-4b1f8d6fd42b)
 Call ID: bbe1ad22-f4e9-4a6d-9674-4b1f8d6fd42b
  Args:
    type: :Person
    source: Davina_Katherine_Bowes-Lyon
  AssignClass (e330dae7-e649-4515-8147-a387455e19f5)
 Call ID: e330dae7-e649-4515-8147-a387455e19f5
  Args:
    type: :Man
    source: David_Bowes-Lyon
  AssignClass (704e2a05-b297-418c-b634-0e4f3fd27b48)
 Call ID: 704e2a05-b297-418c-b634-0e4f3fd27b48
  Args:
    type: :Person
    source: David_Bowes-Lyon
  AssignClass (69fdd81e-7c7b-4e09-89e1-c8caac0f8dd2)
 Call ID: 69fdd81e-7c7b-4e09-89e1-c8caac0f8dd2
  Args:
    type: :Woman
    source: Violet_Evelyn_Dalrymple
  AssignClass (fe8d2206-1d11-4671-a8c3-4c318ac1902e)
 Call ID: fe8d2206-1d11-4671-a8c3-4c318ac1902e
  Args:
    type: :Person
    source: Violet_Evelyn_Dalrymple
  AssignClass (88bcb424-af43-47b3-be48-802d39f66aa7)
 Call ID: 88bcb424-af43-47b3-be48-802d39f66aa7
  Args:
    type: :Man
    source: Frederick_Calvert_6th_Baron_Baltimore
  AssignClass (161a411f-d110-4fd9-b2db-d186a9f1cd09)
 Call ID: 161a411f-d110-4fd9-b2db-d186a9f1cd09
  Args:
    type: :Person
    source: Frederick_Calvert_6th_Baron_Baltimore
  AssignClass (d8f202f0-c10b-497d-9076-cf581dfd5903)
 Call ID: d8f202f0-c10b-497d-9076-cf581dfd5903
  Args:
    type: :Woman
    source: Emily_Mary_Julia_Stonor
  AssignClass (2eaedf6b-2645-4cf4-acd3-244904e67228)
 Call ID: 2eaedf6b-2645-4cf4-acd3-244904e67228
  Args:
    type: :Person
    source: Emily_Mary_Julia_Stonor
  AssignClass (42d4a13c-0215-4bba-b6e9-eb10dca87e98)
 Call ID: 42d4a13c-0215-4bba-b6e9-eb10dca87e98
  Args:
    type: :Man
    source: Ralph_Stonor_7th_Baron_Camoys
  AssignClass (58b3aae1-321f-4f34-8544-0dd423e45c8a)
 Call ID: 58b3aae1-321f-4f34-8544-0dd423e45c8a
  Args:
    type: :Person
    source: Ralph_Stonor_7th_Baron_Camoys
  AssignClass (f3ebb8b7-bd18-4ec4-b427-b42ad1aae0ff)
 Call ID: f3ebb8b7-bd18-4ec4-b427-b42ad1aae0ff
  Args:
    type: :Woman
    source: Elizabeth_Mary_Hyde_Parker
  AssignClass (7a02a6bb-3744-4e6f-be96-c111b8d4257a)
 Call ID: 7a02a6bb-3744-4e6f-be96-c111b8d4257a
  Args:
    type: :Person
    source: Elizabeth_Mary_Hyde_Parker
  AddLiteral (9dd38887-d9f7-471d-85bd-f43a031db1c3)
 Call ID: 9dd38887-d9f7-471d-85bd-f43a031db1c3
  Args:
    literal_type: xsd:integer
    literal_value: 1961
    relation: :hasBirthYear
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
  AddLiteral (3749706c-04f7-4b87-9c28-d63e0c52ae22)
 Call ID: 3749706c-04f7-4b87-9c28-d63e0c52ae22
  Args:
    literal_value: 1930
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Davina_Katherine_Bowes-Lyon
  AddLiteral (56e3cab3-342a-46b1-b1e0-1416662cd6d3)
 Call ID: 56e3cab3-342a-46b1-b1e0-1416662cd6d3
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2017
    source: Davina_Katherine_Bowes-Lyon
  AddTriple (f8e2c46e-e051-42ec-af88-1900814950a6)
 Call ID: f8e2c46e-e051-42ec-af88-1900814950a6
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    target: John_Dalrymple_13th_Earl_of_Stair
    relation: :hasFather
  AddTriple (505dcb5d-a8ed-4822-8cae-5af2cb46bc32)
 Call ID: 505dcb5d-a8ed-4822-8cae-5af2cb46bc32
  Args:
    target: Davina_Katherine_Bowes-Lyon
    relation: :hasMother
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
  AddTriple (d79b6a6f-fe46-419c-8805-9c633cc5200a)
 Call ID: d79b6a6f-fe46-419c-8805-9c633cc5200a
  Args:
    source: Davina_Katherine_Bowes-Lyon
    target: David_Bowes-Lyon
    relation: :hasFather
  AddTriple (d6b79e55-edef-46a8-abc4-e635a11b4bb3)
 Call ID: d6b79e55-edef-46a8-abc4-e635a11b4bb3
  Args:
    target: Ralph_Stonor_7th_Baron_Camoys
    relation: :hasFather
    source: Emily_Mary_Julia_Stonor
  AddTriple (dc5cb054-f008-422d-a8c7-940a2395a599)
 Call ID: dc5cb054-f008-422d-a8c7-940a2395a599
  Args:
    source: Emily_Mary_Julia_Stonor
    target: Elizabeth_Mary_Hyde_Parker
    relation: :hasMother
  AddTriple (2319f388-4384-4cd3-ad22-e5a9b0bfc4d5)
 Call ID: 2319f388-4384-4cd3-ad22-e5a9b0bfc4d5
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    target: Emily_Mary_Julia_Stonor
    relation: :hasMarriageYear
  AddLiteral (a380649a-ea03-402e-b753-d47d06cae48c)
 Call ID: a380649a-ea03-402e-b753-d47d06cae48c
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2006
  Finish (9fb5c4f1-625e-4237-b4c9-60055c2239ad)
 Call ID: 9fb5c4f1-625e-4237-b4c9-60055c2239ad
  Args: