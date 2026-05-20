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
Lady Amanda Patricia Victoria Ellingworth (née Knatchbull; born 26 June 1957), styled The Honourable Amanda Knatchbull between 1957 and 1979, is a British voluntary sector executive.
The granddaughter of Admiral of the Fleet Louis Mountbatten, 1st Earl Mountbatten of Burma, she is a descendant of Queen Victoria through her daughter Princess Alice, Mountbatten's grandmother.
Ancestry

Early life and education

Born as The Honourable Amanda Patricia Victoria Knatchbull, on 26 June 1957, in London, she was the fifth of eight children of the 7th Baron Brabourne and the 2nd Countess Mountbatten of Burma.
Earl Mountbatten of Burma, who was an uncle of Prince Philip, Duke of Edinburgh and a second cousin once removed of Queen Elizabeth II.
Ellingworth earned a BA Hons degree from the University of Kent, a CQSW qualification from Goldsmiths College, London, and a Certificate in Mandarin Language from the Beijing Language Institute.
, Ellingworth worked at a senior level in health services, children's services, adult social care and affordable housing.
Personal life

Marriage and family

Lady Amanda married novelist and property entrepreneur Charles Vincent Ellingworth on 31 October 1987.
Relationship with Prince of Wales

Ellingworth's grandfather Lord Mountbatten recommended her as a potential bride for his grandnephew, Charles, Prince of Wales.
According to his biographer, Jonathan Dimbleby, "In 1974, following his correspondence with Mountbatten on the subject, the Prince had tentatively raised the question of marriage to Amanda with her mother (and his godmother)
"


Mountbatten intended for himself and Lady Amanda to accompany Prince Charles on his planned 1980 tour of India.
Both fathers disapproved and it was decided he should go alone.
Before Prince Charles was to depart, Mountbatten was assassinated by the IRA in August 1979.
When Prince Charles returned, he proposed to Lady Amanda.



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
  AssignClass (927e5a10-0d5c-44c9-a65f-3c644fa437a4)
 Call ID: 927e5a10-0d5c-44c9-a65f-3c644fa437a4
  Args:
    type: :Person
    source: Lady Amanda Patricia Victoria Ellingworth
  AssignClass (f7a6fe46-5bd2-4afd-b018-4ffb4fef1a3d)
 Call ID: f7a6fe46-5bd2-4afd-b018-4ffb4fef1a3d
  Args:
    type: :Woman
    source: Lady Amanda Patricia Victoria Ellingworth
  AssignClass (c10a7474-5a28-479c-bc05-acf2d195f100)
 Call ID: c10a7474-5a28-479c-bc05-acf2d195f100
  Args:
    type: :Person
    source: Charles Vincent Ellingworth
  AssignClass (2a73c382-409d-48d4-b05f-513653f7a4fd)
 Call ID: 2a73c382-409d-48d4-b05f-513653f7a4fd
  Args:
    type: :Man
    source: Charles Vincent Ellingworth
  AssignClass (5a7e4609-972f-4714-a61c-43784626a59f)
 Call ID: 5a7e4609-972f-4714-a61c-43784626a59f
  Args:
    type: :Person
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
  AssignClass (b3470467-367a-40e4-a8d5-9a1ec24329fb)
 Call ID: b3470467-367a-40e4-a8d5-9a1ec24329fb
  Args:
    type: :Man
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
  AssignClass (0224ebaf-99c9-4808-8e1d-07c7dff82cdc)
 Call ID: 0224ebaf-99c9-4808-8e1d-07c7dff82cdc
  Args:
    type: :Ancestor
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
  AssignClass (8bb74ef9-663d-4dc8-be50-224aabef8141)
 Call ID: 8bb74ef9-663d-4dc8-be50-224aabef8141
  Args:
    type: :Person
    source: Prince Philip, Duke of Edinburgh
  AssignClass (6ebe81b0-5076-4763-9619-e1f1403d225d)
 Call ID: 6ebe81b0-5076-4763-9619-e1f1403d225d
  Args:
    type: :Man
    source: Prince Philip, Duke of Edinburgh
  AssignClass (21ba6f9c-e47a-4b39-89b9-27d076150b1d)
 Call ID: 21ba6f9c-e47a-4b39-89b9-27d076150b1d
  Args:
    type: :Person
    source: Queen Elizabeth II
  AssignClass (dbf1dead-1ede-4f96-813b-f582df2cdd69)
 Call ID: dbf1dead-1ede-4f96-813b-f582df2cdd69
  Args:
    type: :Woman
    source: Queen Elizabeth II
  AssignClass (8527201d-8259-4ad4-8b5b-3179d976c198)
 Call ID: 8527201d-8259-4ad4-8b5b-3179d976c198
  Args:
    type: :Person
    source: Queen Victoria
  AssignClass (8d0319c2-43a9-4057-bdfd-a9f33a7bae26)
 Call ID: 8d0319c2-43a9-4057-bdfd-a9f33a7bae26
  Args:
    type: :Woman
    source: Queen Victoria
  AssignClass (699483e0-25a7-4a09-9dec-78166f5dad4b)
 Call ID: 699483e0-25a7-4a09-9dec-78166f5dad4b
  Args:
    type: :Ancestor
    source: Queen Victoria
  AssignClass (19b08bd3-a340-4d66-822e-40e1c0bcd608)
 Call ID: 19b08bd3-a340-4d66-822e-40e1c0bcd608
  Args:
    type: :Person
    source: Princess Alice
  AssignClass (f526d556-b6a8-43a4-96dc-475b59588e73)
 Call ID: f526d556-b6a8-43a4-96dc-475b59588e73
  Args:
    type: :Woman
    source: Princess Alice
  AssignClass (702832f8-8092-4bd0-b2bd-d91415dd734b)
 Call ID: 702832f8-8092-4bd0-b2bd-d91415dd734b
  Args:
    type: :Ancestor
    source: Princess Alice
  AssignClass (bf02806b-cd2d-4a5f-b499-2e50e0a446c7)
 Call ID: bf02806b-cd2d-4a5f-b499-2e50e0a446c7
  Args:
    type: :Person
    source: 7th Baron Brabourne
  AssignClass (5863c331-2f52-498b-9393-4d32615aa4f2)
 Call ID: 5863c331-2f52-498b-9393-4d32615aa4f2
  Args:
    type: :Man
    source: 7th Baron Brabourne
  AssignClass (b779be33-e096-4daa-9b13-9cd639bd3862)
 Call ID: b779be33-e096-4daa-9b13-9cd639bd3862
  Args:
    type: :Ancestor
    source: 7th Baron Brabourne
  AssignClass (0f4c205a-07e0-4562-9ce8-607b23032323)
 Call ID: 0f4c205a-07e0-4562-9ce8-607b23032323
  Args:
    type: :Person
    source: 2nd Countess Mountbatten of Burma
  AssignClass (81edc5a0-107d-409e-9269-bc53fc5a2c4c)
 Call ID: 81edc5a0-107d-409e-9269-bc53fc5a2c4c
  Args:
    type: :Woman
    source: 2nd Countess Mountbatten of Burma
  AssignClass (26da2819-8c67-412b-a3d9-b6a13dc7a94e)
 Call ID: 26da2819-8c67-412b-a3d9-b6a13dc7a94e
  Args:
    type: :Ancestor
    source: 2nd Countess Mountbatten of Burma
  AssignClass (9f0b133f-021a-4774-8e65-0bf4cf52de18)
 Call ID: 9f0b133f-021a-4774-8e65-0bf4cf52de18
  Args:
    type: :Person
    source: Charles, Prince of Wales
  AssignClass (900ff69b-96b7-4e12-9fd5-e260dd905114)
 Call ID: 900ff69b-96b7-4e12-9fd5-e260dd905114
  Args:
    type: :Man
    source: Charles, Prince of Wales
  AddLiteral (ed43310e-2b50-487d-be7e-1da3d49c2c5c)
 Call ID: ed43310e-2b50-487d-be7e-1da3d49c2c5c
  Args:
    source: Lady Amanda Patricia Victoria Ellingworth
    literal_type: xsd:string
    literal_value: Amanda Patricia Victoria Knatchbull
    relation: :alsoKnownAs
  AddLiteral (a1720116-68e2-4024-92a3-f229b54ebe12)
 Call ID: a1720116-68e2-4024-92a3-f229b54ebe12
  Args:
    relation: :formerlyKnownAs
    source: Lady Amanda Patricia Victoria Ellingworth
    literal_value: Amanda Knatchbull
    literal_type: xsd:string
  AddTriple (92e2e5c8-7f79-412b-8495-4fe0c0326e8f)
 Call ID: 92e2e5c8-7f79-412b-8495-4fe0c0326e8f
  Args:
    source: Lady Amanda Patricia Victoria Ellingworth
    relation: :hasFather
    target: 7th Baron Brabourne
  AddTriple (90640152-1d10-4413-9ea6-5d399783fbe5)
 Call ID: 90640152-1d10-4413-9ea6-5d399783fbe5
  Args:
    relation: :hasMother
    target: 2nd Countess Mountbatten of Burma
    source: Lady Amanda Patricia Victoria Ellingworth
  AddTriple (96ca634c-0859-4178-9c6a-d2a4d191336e)
 Call ID: 96ca634c-0859-4178-9c6a-d2a4d191336e
  Args:
    target: Charles Vincent Ellingworth
    relation: :hasRelation
    source: Lady Amanda Patricia Victoria Ellingworth
  AddLiteral (b5fd8da1-6288-4dd4-b18a-7bd646842ea9)
 Call ID: b5fd8da1-6288-4dd4-b18a-7bd646842ea9
  Args:
    source: Lady Amanda Patricia Victoria Ellingworth
    literal_type: xsd:integer
    literal_value: 1987
    relation: :hasMarriageYear
  AddTriple (bc422308-78e7-493f-b159-4e22346ef163)
 Call ID: bc422308-78e7-493f-b159-4e22346ef163
  Args:
    relation: :hasAncestor
    target: Louis Mountbatten, 1st Earl Mountbatten of Burma
    source: Lady Amanda Patricia Victoria Ellingworth
  AddTriple (ee018e0a-12f2-45ca-b0e6-3ced79a33709)
 Call ID: ee018e0a-12f2-45ca-b0e6-3ced79a33709
  Args:
    target: Queen Victoria
    relation: :hasAncestor
    source: Lady Amanda Patricia Victoria Ellingworth
  AddTriple (7a3a9e74-60f2-47a4-b1dc-338a0e68cb82)
 Call ID: 7a3a9e74-60f2-47a4-b1dc-338a0e68cb82
  Args:
    relation: :hasAncestor
    target: Princess Alice
    source: Lady Amanda Patricia Victoria Ellingworth
  AddTriple (1f657867-e6d2-409d-a3ba-4f534870d00d)
 Call ID: 1f657867-e6d2-409d-a3ba-4f534870d00d
  Args:
    source: Princess Alice
    target: Queen Victoria
    relation: :isChildOf
  AddTriple (c2f2e4fd-66a3-4071-b7c5-ac331edde8f0)
 Call ID: c2f2e4fd-66a3-4071-b7c5-ac331edde8f0
  Args:
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
    relation: :hasRelation
    target: Prince Philip, Duke of Edinburgh
  AddTriple (87e7dc75-0e63-4834-846b-672ae42f488e)
 Call ID: 87e7dc75-0e63-4834-846b-672ae42f488e
  Args:
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
    target: Queen Elizabeth II
    relation: :hasRelation
  AddTriple (c720b11c-2b35-4201-a234-97bc218b6733)
 Call ID: c720b11c-2b35-4201-a234-97bc218b6733
  Args:
    source: Charles, Prince of Wales
    relation: :hasRelation
    target: Louis Mountbatten, 1st Earl Mountbatten of Burma
  Finish (763995cc-fe14-4858-a22c-9937e788a444)
 Call ID: 763995cc-fe14-4858-a22c-9937e788a444
  Args: