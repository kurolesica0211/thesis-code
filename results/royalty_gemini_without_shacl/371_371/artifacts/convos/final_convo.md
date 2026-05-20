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
David Henry George Lascelles, 8th Earl of Harewood (born 21 October 1950), styled as Viscount Lascelles until July 2011, is a British hereditary peer and film and television producer.
Early life and earldom

David Henry George Lascelles was born at his parents' London house, 2 Orme Square, Bayswater, London, on 21 October 1950.
He is the eldest son of the 7th Earl of Harewood and his first wife, Marion Stein.
He was baptised at All Saints' Church, Harewood.
His godparents were The Princess Elizabeth, Duchess of Edinburgh (later Queen Elizabeth II), his great-grandmother Queen Mary, his great-aunt Viscountess Boyne (Margaret Hamilton-Russell), his uncle Gerald Lascelles and Benjamin Britten.
He is a second cousin of King Charles III and a great-grandson of King George V.


He succeeded to the Earldom of Harewood on the death of his father in July 2011.
Career and other activities

Lascelles is a film and television producer.
In 2007, as part of the commemoration of the bi-centenary of the Abolition of the Slave Trade Act, Lascelles was executive producer of the theatrical project by Geraldine Connor entitled Carnival Messiah that was staged in the grounds of Harewood House, which was built in the 18th century with funds from slave trading.
Following Connor's death in 2011, Lascelles organised a concert in her memory at West Yorkshire Playhouse, and he is a founder and patron of the Geraldine Connor Foundation, established in 2012 to continue her work and vision by bringing people together through arts and culture.
As Earl of Harewood, he continues the tradition begun by his father in 1961 by serving as the honorary lifetime president of Leeds United Football Club.
It is on display in one of the bookcases at Harewood House.
Personal life

On 12 February 1979, at St Mary's Church, Paddington, London, Lascelles married Margaret Rosalind Messenger, Viscountess Lascelles, daughter of Edgar Frank Messenger.
Their children are:


In 1990, Lascelles married artist Diane Howse, now the Countess of Harewood.



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
  AssignClass (71e4b156-7fe0-4773-929b-837cf0236ce3)
 Call ID: 71e4b156-7fe0-4773-929b-837cf0236ce3
  Args:
    source: David_Henry_George_Lascelles
    type: :Man
  AssignClass (a1e27775-53a4-4bc0-a809-825cef9407ef)
 Call ID: a1e27775-53a4-4bc0-a809-825cef9407ef
  Args:
    source: 7th_Earl_of_Harewood
    type: :Man
  AssignClass (ff5050ec-5921-4550-8b17-8a0822b1cffa)
 Call ID: ff5050ec-5921-4550-8b17-8a0822b1cffa
  Args:
    source: Marion_Stein
    type: :Woman
  AssignClass (68de8f6e-8495-444e-a84d-09e8695f5152)
 Call ID: 68de8f6e-8495-444e-a84d-09e8695f5152
  Args:
    source: Margaret_Rosalind_Messenger
    type: :Woman
  AssignClass (47a9be39-083b-468a-ac8d-7738f1e2a186)
 Call ID: 47a9be39-083b-468a-ac8d-7738f1e2a186
  Args:
    source: Edgar_Frank_Messenger
    type: :Man
  AssignClass (6f6d96da-1aa4-452a-a180-d814ffbd5401)
 Call ID: 6f6d96da-1aa4-452a-a180-d814ffbd5401
  Args:
    type: :Woman
    source: Diane_Howse
  AddLiteral (8fb2fa44-bd27-4e24-841c-0aee739ffb1f)
 Call ID: 8fb2fa44-bd27-4e24-841c-0aee739ffb1f
  Args:
    literal_value: 1950
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: David_Henry_George_Lascelles
  AddTriple (502e99d7-b207-463e-910d-6a6f0c5e8414)
 Call ID: 502e99d7-b207-463e-910d-6a6f0c5e8414
  Args:
    relation: :hasFather
    target: 7th_Earl_of_Harewood
    source: David_Henry_George_Lascelles
  AddTriple (92339d35-3f81-41b4-9e75-e74ead120a4f)
 Call ID: 92339d35-3f81-41b4-9e75-e74ead120a4f
  Args:
    relation: :hasMother
    source: David_Henry_George_Lascelles
    target: Marion_Stein
  AddTriple (c8d5311b-1f0b-4cec-8404-5bef962ad90e)
 Call ID: c8d5311b-1f0b-4cec-8404-5bef962ad90e
  Args:
    relation: :isFatherOf
    source: Edgar_Frank_Messenger
    target: Margaret_Rosalind_Messenger
  AddLiteral (96e47a0a-2ff4-4a8b-9d08-0f5cccfddf8e)
 Call ID: 96e47a0a-2ff4-4a8b-9d08-0f5cccfddf8e
  Args:
    source: David_Henry_George_Lascelles
    literal_value: 1979
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (ff10139d-7f87-4b86-8746-3b3781ecd8ce)
 Call ID: ff10139d-7f87-4b86-8746-3b3781ecd8ce
  Args:
    relation: :hasRelation
    target: Margaret_Rosalind_Messenger
    source: David_Henry_George_Lascelles
  AddLiteral (fa5cf2bb-6e23-4ba1-8003-6062f0ea0fd0)
 Call ID: fa5cf2bb-6e23-4ba1-8003-6062f0ea0fd0
  Args:
    literal_value: 1990
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: David_Henry_George_Lascelles
  AddTriple (8034e4bd-f854-4874-9ed6-6ea8d0ab6c63)
 Call ID: 8034e4bd-f854-4874-9ed6-6ea8d0ab6c63
  Args:
    relation: :hasRelation
    source: David_Henry_George_Lascelles
    target: Diane_Howse
  Finish (090d7f4d-f509-4f56-a28e-ed43240a99c4)
 Call ID: 090d7f4d-f509-4f56-a28e-ed43240a99c4
  Args: