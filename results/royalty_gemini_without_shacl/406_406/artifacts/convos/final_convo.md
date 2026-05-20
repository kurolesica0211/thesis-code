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
Margaret Rhodes (née Elphinstone; 9 June 1925 – 25 November 2016) was a British aristocrat, niece of Queen Elizabeth the Queen Mother and first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
From 1991 to 2002, she served as Woman of the Bedchamber to her aunt, the Queen Mother.
Early life and education

Born The Honourable Margaret Elphinstone in Westminster, London, Rhodes was the youngest daughter of the 16th Lord Elphinstone and his wife, Lady Mary Bowes-Lyon, an elder sister of Queen Elizabeth the Queen Mother.
Less than a year older than her cousin Elizabeth, she was a frequent playmate of the future Queen.
On 20 November 1947, she was a bridesmaid to Princess Elizabeth at her wedding to Philip Mountbatten, Duke of Edinburgh.
She was a Woman of the Bedchamber – a mix of lady-in-waiting and companion – to her aunt Queen Elizabeth the Queen Mother, from 1991 until the latter's death in 2002.
In the 2000 Birthday Honours Rhodes was appointed Lieutenant of the Royal Victorian Order (LVO).
In the run-up to the Queen's 80th birthday in April 2006, Rhodes gave an interview to the BBC in which she stated her belief that the Queen would not abdicate.
Rhodes appeared in seven documentaries about her first cousin Queen Elizabeth II.
On 27 November 2016, Buckingham Palace confirmed that Rhodes had died, aged 91, on 25 November following a short illness.
The Queen and the Duke of Edinburgh attended her funeral in the Royal Chapel of All Saints, Windsor Great Park, on 12 December 2016, accompanied by the Duke of York, the Earl and Countess of Wessex, the Duke and Duchess of Gloucester, and Princess Alexandra, The Hon.
Lady Ogilvy.
Personal life

On 31 July 1950, she married the writer Denys Gravenor Rhodes (1919–1981), with Princess Margaret as one of the bridesmaids.



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
  AssignClass (e705524a-4ea7-40fb-a689-6375bf4b17f6)
 Call ID: e705524a-4ea7-40fb-a689-6375bf4b17f6
  Args:
    type: :Woman
    source: Margaret_Rhodes
  AssignClass (5b7acba2-203f-4cbd-8d53-ba934004a1b0)
 Call ID: 5b7acba2-203f-4cbd-8d53-ba934004a1b0
  Args:
    type: :Person
    source: Margaret_Rhodes
  AddLiteral (8b1e03e2-3515-4450-ab95-ce92c23ff4ac)
 Call ID: 8b1e03e2-3515-4450-ab95-ce92c23ff4ac
  Args:
    source: Margaret_Rhodes
    literal_value: 1925
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (018c0b6c-996b-4f5d-a1ed-27b05b189c09)
 Call ID: 018c0b6c-996b-4f5d-a1ed-27b05b189c09
  Args:
    source: Margaret_Rhodes
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2016
  AssignClass (8d85c002-0270-4340-9466-692b22928362)
 Call ID: 8d85c002-0270-4340-9466-692b22928362
  Args:
    type: :Man
    source: Lord_Elphinstone_16th
  AssignClass (5b514846-0ede-4a50-af09-80862170d928)
 Call ID: 5b514846-0ede-4a50-af09-80862170d928
  Args:
    type: :Person
    source: Lord_Elphinstone_16th
  AssignClass (e10251d7-659c-44b8-b0e0-439de00f6e65)
 Call ID: e10251d7-659c-44b8-b0e0-439de00f6e65
  Args:
    type: :Woman
    source: Lady_Mary_Bowes-Lyon
  AssignClass (a7d54259-6d7b-43a4-8732-786147abd3f8)
 Call ID: a7d54259-6d7b-43a4-8732-786147abd3f8
  Args:
    type: :Person
    source: Lady_Mary_Bowes-Lyon
  AddTriple (a7bf22be-57a3-4fdb-9d73-e205150c84f4)
 Call ID: a7bf22be-57a3-4fdb-9d73-e205150c84f4
  Args:
    relation: :hasFather
    target: Lord_Elphinstone_16th
    source: Margaret_Rhodes
  AddTriple (cea098a9-ffed-48ef-9860-ecf1bf6e609d)
 Call ID: cea098a9-ffed-48ef-9860-ecf1bf6e609d
  Args:
    relation: :hasMother
    source: Margaret_Rhodes
    target: Lady_Mary_Bowes-Lyon
  AssignClass (7721035f-f48d-482d-96dc-44b660bbee9a)
 Call ID: 7721035f-f48d-482d-96dc-44b660bbee9a
  Args:
    type: :Woman
    source: Queen_Elizabeth_The_Queen_Mother
  AssignClass (9493becc-a727-49c2-95ed-0639ee0dee2d)
 Call ID: 9493becc-a727-49c2-95ed-0639ee0dee2d
  Args:
    type: :Person
    source: Queen_Elizabeth_The_Queen_Mother
  AddTriple (ec7a7422-512f-4cb2-a313-31f7b9a19823)
 Call ID: ec7a7422-512f-4cb2-a313-31f7b9a19823
  Args:
    target: Queen_Elizabeth_The_Queen_Mother
    source: Lady_Mary_Bowes-Lyon
    relation: :isSisterOf
  AssignClass (3b65af4e-195b-4b70-9501-0a253f73085c)
 Call ID: 3b65af4e-195b-4b70-9501-0a253f73085c
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (62e224d8-05f0-4631-95ad-bab2891905eb)
 Call ID: 62e224d8-05f0-4631-95ad-bab2891905eb
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (987828da-eede-4fdc-a08f-ba10b260c6f9)
 Call ID: 987828da-eede-4fdc-a08f-ba10b260c6f9
  Args:
    type: :Woman
    source: Princess_Margaret
  AssignClass (676ad40d-bf97-4393-a2aa-2f496ab5e218)
 Call ID: 676ad40d-bf97-4393-a2aa-2f496ab5e218
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (4929b0c4-3439-404a-9aa3-541f88b79341)
 Call ID: 4929b0c4-3439-404a-9aa3-541f88b79341
  Args:
    type: :Man
    source: Denys_Gravenor_Rhodes
  AssignClass (dc7f30e5-c405-4d0d-a26a-951fb9482eb2)
 Call ID: dc7f30e5-c405-4d0d-a26a-951fb9482eb2
  Args:
    type: :Person
    source: Denys_Gravenor_Rhodes
  AddLiteral (188a2385-cc27-4587-921b-738715a5709a)
 Call ID: 188a2385-cc27-4587-921b-738715a5709a
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1950
    source: Margaret_Rhodes
  AddTriple (192a4a6e-cf8e-4ba6-b56f-c0c11057d6dd)
 Call ID: 192a4a6e-cf8e-4ba6-b56f-c0c11057d6dd
  Args:
    relation: :hasRelation
    target: Denys_Gravenor_Rhodes
    source: Margaret_Rhodes
  Finish (0adf672e-0a31-4fca-b5a7-3ca1951b39a1)
 Call ID: 0adf672e-0a31-4fca-b5a7-3ca1951b39a1
  Args: