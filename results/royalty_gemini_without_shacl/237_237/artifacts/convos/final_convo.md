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
Franz Ulrich, 11th Prince Kinsky of Wchinitz and Tettau (German: Franz Ulrich Johannes Clemens Christophorus Antonius Bonaventura Maria Fürst Kinsky von Wchinitz und Tettau; 7 October 1936 – 2 April 2009) was the titular Prince Kinsky of Wchinitz and Tettau as well the head of an ancient House of Kinsky.
Early life

Franz Ulrich was born at Vienna, Federal State of Austria, as the youngest son of Ulrich, 10th Prince Kinsky of Wchinitz and Tettau by his second marriage to Baroness Marie Julia Mathilde von dem Bussche-Haddenhausen (1900–1974), the eldest daughter of Baron Hilmar von dem Bussche-Haddenhausen.
Franz Ulrich became the titular Prince upon the death of his father in 1938.
He was first cousin of Countess Marie Aglaë Kinsky of Wchinitz and Tettau who later became Princess consort of Liechtenstein, and second cousin of Claus von Amsberg, Prince consort of Queen Beatrix of the Netherlands, both descendants of Baron Julius von dem Bussche-Haddenhausen.
In 1942, Franz Ulrich inherited several estates from the Kinsky family, including the Kinsky Palace in Old Town Square in Prague.
Starting in 2003, Franz Ulrich complained against various Czech courts for the return of the assets.
Marriage and family

Franz Ulrich married on 14 April 1965 in Buenos Aires to Roberta Cavanagh (1942–2002), daughter of Roberto Cavanagh and his wife, Anne Rowell.
After Kinsky's death, his son and his widow, Countess Helena Victoria Hutten-Czapska entered a legal dispute over Kinsky's properties.
Later life

The Prince died on 2 April 2009, aged 72.



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
  AssignClass (5f8a3ad7-f4dc-48c2-ae90-f657448be4f0)
 Call ID: 5f8a3ad7-f4dc-48c2-ae90-f657448be4f0
  Args:
    type: :Man
    source: Franz_Ulrich
  AssignClass (3bc04b7f-cd5c-44c3-b52e-851b6ca3680d)
 Call ID: 3bc04b7f-cd5c-44c3-b52e-851b6ca3680d
  Args:
    source: Franz_Ulrich
    type: :Person
  AddLiteral (dad64333-f67f-4257-bbc1-6afee73e7f85)
 Call ID: dad64333-f67f-4257-bbc1-6afee73e7f85
  Args:
    source: Franz_Ulrich
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1936
  AddLiteral (1c96e27c-f21a-4ed6-b702-1c8b67e7c071)
 Call ID: 1c96e27c-f21a-4ed6-b702-1c8b67e7c071
  Args:
    literal_value: 2009
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Franz_Ulrich
  AssignClass (47138521-f8bb-4c04-9085-8e247f76dd10)
 Call ID: 47138521-f8bb-4c04-9085-8e247f76dd10
  Args:
    source: Ulrich_10th_Prince_Kinsky
    type: :Man
  AssignClass (45dd6cd7-8d63-43fb-b845-c6f03ea1647e)
 Call ID: 45dd6cd7-8d63-43fb-b845-c6f03ea1647e
  Args:
    type: :Person
    source: Ulrich_10th_Prince_Kinsky
  AddTriple (04ab384e-274f-4301-bd7a-9e6b531f3a5e)
 Call ID: 04ab384e-274f-4301-bd7a-9e6b531f3a5e
  Args:
    target: Ulrich_10th_Prince_Kinsky
    source: Franz_Ulrich
    relation: :hasFather
  AssignClass (0cf6d057-0598-4552-93db-e73b2442c208)
 Call ID: 0cf6d057-0598-4552-93db-e73b2442c208
  Args:
    type: :Woman
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AssignClass (3d1b4ad4-7549-45ca-98e3-e57f2b2d94db)
 Call ID: 3d1b4ad4-7549-45ca-98e3-e57f2b2d94db
  Args:
    type: :Person
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
  AddTriple (48e0dffd-eb45-4d85-9bff-7c8185416c24)
 Call ID: 48e0dffd-eb45-4d85-9bff-7c8185416c24
  Args:
    relation: :hasMother
    target: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    source: Franz_Ulrich
  AssignClass (682a37e4-23bd-46d8-af81-c69a435aa2d1)
 Call ID: 682a37e4-23bd-46d8-af81-c69a435aa2d1
  Args:
    type: :Man
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (47f96869-b00c-4021-811e-353bea5b08c3)
 Call ID: 47f96869-b00c-4021-811e-353bea5b08c3
  Args:
    type: :Person
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AddTriple (c31b664b-f0da-47fe-9246-8a1b0643a098)
 Call ID: c31b664b-f0da-47fe-9246-8a1b0643a098
  Args:
    target: Hilmar_von_dem_Bussche-Haddenhausen
    source: Marie_Julia_Mathilde_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AssignClass (09607ba0-d5f1-4e69-9e03-3bcfd9be3154)
 Call ID: 09607ba0-d5f1-4e69-9e03-3bcfd9be3154
  Args:
    type: :Woman
    source: Roberta_Cavanagh
  AssignClass (84ee14c7-5498-4108-9b1a-a59401ffcf95)
 Call ID: 84ee14c7-5498-4108-9b1a-a59401ffcf95
  Args:
    source: Roberta_Cavanagh
    type: :Person
  AddLiteral (4fa227a6-5934-44e5-b26d-b02e8393534a)
 Call ID: 4fa227a6-5934-44e5-b26d-b02e8393534a
  Args:
    source: Franz_Ulrich
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1965
  AddTriple (bed0592f-2676-421c-a574-6085c8a90026)
 Call ID: bed0592f-2676-421c-a574-6085c8a90026
  Args:
    target: Roberta_Cavanagh
    source: Franz_Ulrich
    relation: :hasRelation
  AssignClass (82a64a66-ff80-4f0b-946d-df542841ad80)
 Call ID: 82a64a66-ff80-4f0b-946d-df542841ad80
  Args:
    type: :Man
    source: Roberto_Cavanagh
  AssignClass (8a2a3054-7047-4f4a-a0d3-82e5e740b76f)
 Call ID: 8a2a3054-7047-4f4a-a0d3-82e5e740b76f
  Args:
    source: Roberto_Cavanagh
    type: :Person
  AddTriple (2ae2430e-ddf9-45ab-ae0c-107e83fd30b9)
 Call ID: 2ae2430e-ddf9-45ab-ae0c-107e83fd30b9
  Args:
    relation: :hasFather
    target: Roberto_Cavanagh
    source: Roberta_Cavanagh
  AssignClass (41edcf35-522a-4024-86b5-2b14d526cd65)
 Call ID: 41edcf35-522a-4024-86b5-2b14d526cd65
  Args:
    type: :Woman
    source: Anne_Rowell
  AssignClass (621d6354-3d49-444e-a205-73b2dd2fcb76)
 Call ID: 621d6354-3d49-444e-a205-73b2dd2fcb76
  Args:
    type: :Person
    source: Anne_Rowell
  AddTriple (fbff0597-1a24-4c43-a44e-790a55fafc3a)
 Call ID: fbff0597-1a24-4c43-a44e-790a55fafc3a
  Args:
    relation: :hasMother
    target: Anne_Rowell
    source: Roberta_Cavanagh
  AssignClass (91560625-6cdc-4ef2-8789-4078f0ef7f50)
 Call ID: 91560625-6cdc-4ef2-8789-4078f0ef7f50
  Args:
    source: Helena_Victoria_Hutten-Czapska
    type: :Woman
  AssignClass (e69596b6-8557-4832-a9fe-8bf1d9de480b)
 Call ID: e69596b6-8557-4832-a9fe-8bf1d9de480b
  Args:
    source: Helena_Victoria_Hutten-Czapska
    type: :Person
  AddTriple (31eed313-0b21-48a3-b00e-f02e9d2f6681)
 Call ID: 31eed313-0b21-48a3-b00e-f02e9d2f6681
  Args:
    relation: :hasRelation
    target: Helena_Victoria_Hutten-Czapska
    source: Franz_Ulrich
  Finish (c1ba653b-cbb1-408a-a978-44262a5963f1)
 Call ID: c1ba653b-cbb1-408a-a978-44262a5963f1
  Args: