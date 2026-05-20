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
James Robert Bruce Ogilvy (born 29 February 1964) is a British landscape designer, and the founder and editor of the magazine Luxury Briefing.
He is a member of the extended British royal family as the elder child and only son of Princess Alexandra of Kent and Sir Angus Ogilvy.
Early life and family

James Robert Bruce Ogilvy was born on Leap Year Day in 1964, making him a leapling.
He was the first of four children born to royalty within a space of nine weeks in 1964, the others being Prince Edward, Lady Helen Windsor and Lady Sarah Armstrong-Jones.
Ogilvy was baptised by Michael Ramsey, Archbishop of Canterbury, with Queen Elizabeth II among his seven godparents.
His education began in the "palace school" with his cousins Prince Edward, Lady Helen Windsor and Lady Sarah Armstrong-Jones.
Subsequently, Ogilvy attended Gibbs pre-prep and Heatherdown Preparatory School (with Prince Edward).
After that, Ogilvy and Prince Edward went separate ways, the prince to Gordonstoun and Cambridge, and Ogilvy to Eton College and the University of St Andrews.
Ogilvy is also a professional photographer and landscape designer.
Ogilvy had several leg wounds and required 30 stitches.
Ancestry

His maternal grandparents were Prince George, Duke of Kent, the fourth son of King George V; and Princess Marina of Greece and Denmark.
Princess Marina was the daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia (later known as Princess Nicholas of Greece and Denmark).
He has a younger sister, Marina Ogilvy.



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
  AssignClass (8de2ac76-7800-4394-ab37-2458a204fa0e)
 Call ID: 8de2ac76-7800-4394-ab37-2458a204fa0e
  Args:
    source: James_Robert_Bruce_Ogilvy
    type: :Man
  AssignClass (5fc14f08-e434-4e24-995d-ce67f8e8249f)
 Call ID: 5fc14f08-e434-4e24-995d-ce67f8e8249f
  Args:
    source: Princess_Alexandra_of_Kent
    type: :Woman
  AssignClass (dd91187c-8293-4cb9-899b-20c72e5e2b14)
 Call ID: dd91187c-8293-4cb9-899b-20c72e5e2b14
  Args:
    source: Sir_Angus_Ogilvy
    type: :Man
  AssignClass (c12fb845-8cd9-4e28-8507-475940524aeb)
 Call ID: c12fb845-8cd9-4e28-8507-475940524aeb
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AssignClass (2e9613a0-2d5e-4ec1-b6ba-78d17eb72a43)
 Call ID: 2e9613a0-2d5e-4ec1-b6ba-78d17eb72a43
  Args:
    source: King_George_V
    type: :Man
  AssignClass (f83120ee-c970-47e7-bc05-b379651108d5)
 Call ID: f83120ee-c970-47e7-bc05-b379651108d5
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (1985eb1d-b9e3-4c77-8a04-1d6aeb6c9ad2)
 Call ID: 1985eb1d-b9e3-4c77-8a04-1d6aeb6c9ad2
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (e263190b-3303-4252-ac7c-4237bca5bd7e)
 Call ID: e263190b-3303-4252-ac7c-4237bca5bd7e
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (dbda0b94-f2f3-4cf1-9775-5de0cafd8ee0)
 Call ID: dbda0b94-f2f3-4cf1-9775-5de0cafd8ee0
  Args:
    type: :Woman
    source: Marina_Ogilvy
  AddLiteral (b1f3a0d1-2059-4e69-a877-cd6d1d38be18)
 Call ID: b1f3a0d1-2059-4e69-a877-cd6d1d38be18
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1964
    source: James_Robert_Bruce_Ogilvy
  AddTriple (eb8304ed-2fd5-4d9f-a6e5-1c28b5a0f38f)
 Call ID: eb8304ed-2fd5-4d9f-a6e5-1c28b5a0f38f
  Args:
    relation: :hasMother
    source: James_Robert_Bruce_Ogilvy
    target: Princess_Alexandra_of_Kent
  AddTriple (5e89dbc3-7557-4fb2-9b1e-f2e717bde05c)
 Call ID: 5e89dbc3-7557-4fb2-9b1e-f2e717bde05c
  Args:
    relation: :hasFather
    source: James_Robert_Bruce_Ogilvy
    target: Sir_Angus_Ogilvy
  AddTriple (3b26899b-11a8-46dd-a4db-89ce95889852)
 Call ID: 3b26899b-11a8-46dd-a4db-89ce95889852
  Args:
    target: Princess_Marina_of_Greece_and_Denmark
    source: Princess_Alexandra_of_Kent
    relation: :hasMother
  AddTriple (858796d6-4b0a-4f07-8979-f6eb797c1a65)
 Call ID: 858796d6-4b0a-4f07-8979-f6eb797c1a65
  Args:
    relation: :hasFather
    source: Princess_Alexandra_of_Kent
    target: Prince_George_Duke_of_Kent
  AddTriple (a4234e6a-6fe9-4567-bc3f-d0c78129de41)
 Call ID: a4234e6a-6fe9-4567-bc3f-d0c78129de41
  Args:
    relation: :hasFather
    source: Prince_George_Duke_of_Kent
    target: King_George_V
  AddTriple (2f4e4e1e-aad7-4e2b-8da0-f0c29ff8a6f1)
 Call ID: 2f4e4e1e-aad7-4e2b-8da0-f0c29ff8a6f1
  Args:
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    source: Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
  AddTriple (1f6af89e-3d93-47ab-b923-51f56fc0280c)
 Call ID: 1f6af89e-3d93-47ab-b923-51f56fc0280c
  Args:
    source: Princess_Marina_of_Greece_and_Denmark
    target: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (c2fbcd29-4380-4e4c-be8b-290abc918ac0)
 Call ID: c2fbcd29-4380-4e4c-be8b-290abc918ac0
  Args:
    source: James_Robert_Bruce_Ogilvy
    target: Marina_Ogilvy
    relation: :hasSister
  AddTriple (6a97b9a0-68f8-4c59-a8ea-c1687010bda8)
 Call ID: 6a97b9a0-68f8-4c59-a8ea-c1687010bda8
  Args:
    target: Princess_Alexandra_of_Kent
    source: Marina_Ogilvy
    relation: :hasMother
  AddTriple (580825f8-7a61-48bf-9459-e1853f9c2891)
 Call ID: 580825f8-7a61-48bf-9459-e1853f9c2891
  Args:
    relation: :hasFather
    target: Sir_Angus_Ogilvy
    source: Marina_Ogilvy
  Finish (5fe3ebf9-35bc-43d6-a2df-8275ca3f7a77)
 Call ID: 5fe3ebf9-35bc-43d6-a2df-8275ca3f7a77
  Args: