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
Lady Iris Victoria Beatrice Grace Kemp (née Mountbatten, formerly O'Malley, later Bryan; 13 January 1920 – 1 September 1982) was an English actress and model, and a member of the Battenberg/Mountbatten family.
She was also a niece of Queen Victoria Eugenie of Spain, making her a first cousin of Infante Juan, Count of Barcelona, father of Juan Carlos I and grandfather of current King Felipe VI of Spain, as well as Infante Jaime, Duke of Segovia, the Legitimist claimant to the French throne.
She was also a second cousin of Prince Philip, Duke of Edinburgh, consort of Queen Elizabeth II.
Family and early life

Iris Victoria Beatrice Grace Mountbatten was born at Kensington Palace, London on 13 January 1920, the only child of Alexander Mountbatten, 1st Marquess of Carisbrooke, eldest of three sons and one daughter of Princess Beatrice and Prince Henry of Battenberg.
Her mother, the Marchioness of Carisbrooke, was born Lady Irene Frances Adza Denison (4 July 1890 – 16 July 1956)
the only daughter of William Francis Henry Denison, 2nd Earl of Londesborough and Lady Grace Adelaide Fane (3 October 1860 – 13 June 1933), a daughter of Francis William Henry Fane, 12th Earl of Westmorland.
Lady Carisbrooke had two brothers of whom only one, Hugo William Cecil Denison, 4th and last Earl of Londesborough, was married.
He and his wife had one child, Iris's only maternal first cousin, Lady Zinnia Rosemary Denison (25 November 1937 – 13 July 1997) a keen equestrian and Master of the Whaddon Chase Hunt 1982–84. '
On 29 November 1934, Iris was a bridesmaid at the wedding of her third cousin, Princess Marina of Greece and Denmark, to Iris’ second cousin, Prince George, Duke of Kent.
(Marina and Iris were related through the Hesse family, while George and Iris were both great-grandchildren of Queen Victoria.)
On 12 May 1937 at their coronation, Iris was one of the six train bearers to Queen Elizabeth, wife and consort of her second cousin King George VI.
During World War II she worked as a nurse's aide, later moving to the United States, where she taught dance.
Marriages

Lady Iris was married three times.
On 29 January 1941 Lady Iris received Royal Licence by King George VI to marry Captain (later Major) Hamilton Joseph Keyes O'Malley (after an engagement formally announced in The Times on 18 January 1941).
Lady Iris formally reverted to her maiden name of Mountbatten by Deed poll dated 7 January 1949.
Lady Iris, by her second marriage, had one child, Robin Alexander Bryan (born Mount Sinai Hospital, Manhattan, New York City, 20 December 1957), who has three natural children from three different women.
On 11 December 1965, she married William Alexander Kemp (10 July 1921 – 12 December 1991), son of Clarence Arthur Kemp and Helen Janet Ballantyne, a Canadian actor and announcer.
Death

Lady Iris died on 1 September 1982 at Wellesley Hospital, Toronto, Ontario, Canada, of a brain tumour.
Her ashes were brought to the Isle of Wight for interment in the Battenberg Chapel, at St. Mildred's Church, Whippingham.



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
  AssignClass (c6e3705e-25c3-40f7-a438-581c35401130)
 Call ID: c6e3705e-25c3-40f7-a438-581c35401130
  Args:
    type: :Woman
    source: Lady_Iris_Mountbatten
  AssignClass (d047d03c-bd68-4a9e-8b60-fcdbf12a4876)
 Call ID: d047d03c-bd68-4a9e-8b60-fcdbf12a4876
  Args:
    type: :Person
    source: Lady_Iris_Mountbatten
  AddLiteral (78d81bd4-9c76-4fd1-8adc-51a33684fd9c)
 Call ID: 78d81bd4-9c76-4fd1-8adc-51a33684fd9c
  Args:
    source: Lady_Iris_Mountbatten
    relation: :knownAs
    literal_value: Lady Iris Victoria Beatrice Grace Kemp
    literal_type: xsd:string
  AddLiteral (cf8b9285-f936-4932-bcbf-2ded3e6de5ae)
 Call ID: cf8b9285-f936-4932-bcbf-2ded3e6de5ae
  Args:
    source: Lady_Iris_Mountbatten
    literal_value: 1920
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (69d14910-434d-4f31-afb3-335cd037f15b)
 Call ID: 69d14910-434d-4f31-afb3-335cd037f15b
  Args:
    literal_type: xsd:integer
    literal_value: 1982
    relation: :hasDeathYear
    source: Lady_Iris_Mountbatten
  AssignClass (a4550617-2f0a-4684-bd0d-b625970474e2)
 Call ID: a4550617-2f0a-4684-bd0d-b625970474e2
  Args:
    type: :Man
    source: Alexander_Mountbatten
  AssignClass (21a371b8-761e-4e3f-bc18-5c96714ce3d9)
 Call ID: 21a371b8-761e-4e3f-bc18-5c96714ce3d9
  Args:
    type: :Ancestor
    source: Alexander_Mountbatten
  AddTriple (64aaef10-193d-4ffb-8a21-2e72450d33dc)
 Call ID: 64aaef10-193d-4ffb-8a21-2e72450d33dc
  Args:
    source: Lady_Iris_Mountbatten
    target: Alexander_Mountbatten
    relation: :hasFather
  AssignClass (094a97a3-af15-4252-94ef-5778f4d40118)
 Call ID: 094a97a3-af15-4252-94ef-5778f4d40118
  Args:
    type: :Woman
    source: Irene_Frances_Adza_Denison
  AssignClass (a5f28151-b853-41ca-890e-9a82dce0d954)
 Call ID: a5f28151-b853-41ca-890e-9a82dce0d954
  Args:
    type: :Ancestor
    source: Irene_Frances_Adza_Denison
  AddTriple (9659d368-0f15-404b-a3a6-69ba74775d53)
 Call ID: 9659d368-0f15-404b-a3a6-69ba74775d53
  Args:
    source: Lady_Iris_Mountbatten
    relation: :hasMother
    target: Irene_Frances_Adza_Denison
  AssignClass (76188bb0-22a0-4413-bf7f-a42ed45e7d47)
 Call ID: 76188bb0-22a0-4413-bf7f-a42ed45e7d47
  Args:
    type: :Man
    source: William_Francis_Henry_Denison
  AssignClass (083a3dff-43b8-4d35-b10b-a67838e9e823)
 Call ID: 083a3dff-43b8-4d35-b10b-a67838e9e823
  Args:
    type: :Ancestor
    source: William_Francis_Henry_Denison
  AssignClass (19be8c45-b3e1-49eb-bae5-0355cd10048d)
 Call ID: 19be8c45-b3e1-49eb-bae5-0355cd10048d
  Args:
    type: :Woman
    source: Grace_Adelaide_Fane
  AssignClass (19856a50-81df-4a2d-b001-dfe644e45f03)
 Call ID: 19856a50-81df-4a2d-b001-dfe644e45f03
  Args:
    type: :Ancestor
    source: Grace_Adelaide_Fane
  AddTriple (663243f7-1ee0-4b7d-ac90-9d2ef240c815)
 Call ID: 663243f7-1ee0-4b7d-ac90-9d2ef240c815
  Args:
    target: William_Francis_Henry_Denison
    relation: :hasFather
    source: Irene_Frances_Adza_Denison
  AddTriple (7dbdb1fa-30ca-4ebe-8cdf-12dec308a82d)
 Call ID: 7dbdb1fa-30ca-4ebe-8cdf-12dec308a82d
  Args:
    target: Grace_Adelaide_Fane
    relation: :hasMother
    source: Irene_Frances_Adza_Denison
  AssignClass (98ead8e3-6510-433b-9d73-97af00e844a4)
 Call ID: 98ead8e3-6510-433b-9d73-97af00e844a4
  Args:
    type: :Man
    source: Francis_William_Henry_Fane
  AssignClass (152a058d-e493-4e05-b2e2-d27fb78e4d18)
 Call ID: 152a058d-e493-4e05-b2e2-d27fb78e4d18
  Args:
    type: :Ancestor
    source: Francis_William_Henry_Fane
  AddTriple (0651cabf-e917-434c-b7c0-81ea336e80f6)
 Call ID: 0651cabf-e917-434c-b7c0-81ea336e80f6
  Args:
    source: Grace_Adelaide_Fane
    target: Francis_William_Henry_Fane
    relation: :hasFather
  AssignClass (5b90eee5-98fc-40f1-a2c0-8fcc226ba29e)
 Call ID: 5b90eee5-98fc-40f1-a2c0-8fcc226ba29e
  Args:
    type: :Man
    source: Hugo_William_Cecil_Denison
  AssignClass (c0eafdb0-d0ea-48c4-a912-1e1ca0a7f9e1)
 Call ID: c0eafdb0-d0ea-48c4-a912-1e1ca0a7f9e1
  Args:
    type: :Ancestor
    source: Hugo_William_Cecil_Denison
  AddTriple (58b3d818-b2cf-4675-8d3a-7fa4ee4e27f5)
 Call ID: 58b3d818-b2cf-4675-8d3a-7fa4ee4e27f5
  Args:
    source: Hugo_William_Cecil_Denison
    target: William_Francis_Henry_Denison
    relation: :hasFather
  AssignClass (4def1a96-7817-4503-b32a-51e643a639e5)
 Call ID: 4def1a96-7817-4503-b32a-51e643a639e5
  Args:
    type: :Woman
    source: Zinnia_Rosemary_Denison
  AssignClass (bc757616-bd0b-4274-84b4-8d239a84d3fb)
 Call ID: bc757616-bd0b-4274-84b4-8d239a84d3fb
  Args:
    type: :Person
    source: Zinnia_Rosemary_Denison
  AddTriple (68e0bd16-07ab-4090-a810-e134107f0481)
 Call ID: 68e0bd16-07ab-4090-a810-e134107f0481
  Args:
    source: Zinnia_Rosemary_Denison
    relation: :hasFather
    target: Hugo_William_Cecil_Denison
  AssignClass (25de7835-b9a7-4e56-9b30-89a441493d98)
 Call ID: 25de7835-b9a7-4e56-9b30-89a441493d98
  Args:
    type: :Man
    source: Hamilton_Joseph_Keyes_O_Malley
  AssignClass (1947b9b3-4e65-4cfd-94e5-2a2393dacbc7)
 Call ID: 1947b9b3-4e65-4cfd-94e5-2a2393dacbc7
  Args:
    type: :Person
    source: Hamilton_Joseph_Keyes_O_Malley
  AddLiteral (85d717ee-425f-4817-9a45-1300facdaf8e)
 Call ID: 85d717ee-425f-4817-9a45-1300facdaf8e
  Args:
    literal_value: 1941
    relation: :hasMarriageYear
    source: Lady_Iris_Mountbatten
    literal_type: xsd:integer
  AssignClass (2fd66689-7473-4c44-a9e0-06f6209447ce)
 Call ID: 2fd66689-7473-4c44-a9e0-06f6209447ce
  Args:
    type: :Man
    source: Robin_Alexander_Bryan
  AssignClass (42438d16-ac3f-4fb2-82e4-6fd9465d0345)
 Call ID: 42438d16-ac3f-4fb2-82e4-6fd9465d0345
  Args:
    type: :Person
    source: Robin_Alexander_Bryan
  AddTriple (14b35e91-92a7-4605-9cba-460d95e8775c)
 Call ID: 14b35e91-92a7-4605-9cba-460d95e8775c
  Args:
    target: Lady_Iris_Mountbatten
    relation: :hasMother
    source: Robin_Alexander_Bryan
  AssignClass (cd917fee-2911-4233-813d-5cceef0dae0f)
 Call ID: cd917fee-2911-4233-813d-5cceef0dae0f
  Args:
    type: :Man
    source: William_Alexander_Kemp
  AssignClass (b9285ed2-58c7-4d53-a22f-099af4a8a50d)
 Call ID: b9285ed2-58c7-4d53-a22f-099af4a8a50d
  Args:
    type: :Person
    source: William_Alexander_Kemp
  AddLiteral (73a13e2f-3ce2-41bc-bfe0-bac6d3b57b6e)
 Call ID: 73a13e2f-3ce2-41bc-bfe0-bac6d3b57b6e
  Args:
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasMarriageYear
    source: Lady_Iris_Mountbatten
  AssignClass (f19e521b-538f-4c16-ae6b-b4f6157574b5)
 Call ID: f19e521b-538f-4c16-ae6b-b4f6157574b5
  Args:
    type: :Man
    source: Clarence_Arthur_Kemp
  AssignClass (2869b0f3-6bc7-4434-82d6-ed87fe9d12c1)
 Call ID: 2869b0f3-6bc7-4434-82d6-ed87fe9d12c1
  Args:
    type: :Ancestor
    source: Clarence_Arthur_Kemp
  AssignClass (0f36ca7a-bc6b-4356-8794-0cbc0a930182)
 Call ID: 0f36ca7a-bc6b-4356-8794-0cbc0a930182
  Args:
    type: :Woman
    source: Helen_Janet_Ballantyne
  AssignClass (e5a18d66-d042-42ad-b34f-a407c4bfb27a)
 Call ID: e5a18d66-d042-42ad-b34f-a407c4bfb27a
  Args:
    type: :Ancestor
    source: Helen_Janet_Ballantyne
  AddTriple (4445f6f0-21de-4a76-824c-7f768bd67c92)
 Call ID: 4445f6f0-21de-4a76-824c-7f768bd67c92
  Args:
    source: William_Alexander_Kemp
    target: Clarence_Arthur_Kemp
    relation: :hasFather
  AddTriple (17021990-0ff0-4485-a275-4a4bd38499e2)
 Call ID: 17021990-0ff0-4485-a275-4a4bd38499e2
  Args:
    source: William_Alexander_Kemp
    target: Helen_Janet_Ballantyne
    relation: :hasMother
  AssignClass (c490a162-fe17-472c-8b4e-fc066e60d7e4)
 Call ID: c490a162-fe17-472c-8b4e-fc066e60d7e4
  Args:
    type: :Woman
    source: Princess_Beatrice
  AssignClass (c5428169-e4b2-4fd5-966e-411cfabab194)
 Call ID: c5428169-e4b2-4fd5-966e-411cfabab194
  Args:
    type: :Ancestor
    source: Princess_Beatrice
  AssignClass (124988e2-c759-434f-a79d-9a27c92011b1)
 Call ID: 124988e2-c759-434f-a79d-9a27c92011b1
  Args:
    type: :Man
    source: Prince_Henry_of_Battenberg
  AssignClass (a0a3a6c1-18da-42d1-b816-25f381853076)
 Call ID: a0a3a6c1-18da-42d1-b816-25f381853076
  Args:
    type: :Ancestor
    source: Prince_Henry_of_Battenberg
  AddTriple (91282a85-db35-4e85-b85c-83b4361853ec)
 Call ID: 91282a85-db35-4e85-b85c-83b4361853ec
  Args:
    source: Alexander_Mountbatten
    relation: :hasMother
    target: Princess_Beatrice
  AddTriple (e9c5d7a4-202c-451b-8e44-cfcfefba84c6)
 Call ID: e9c5d7a4-202c-451b-8e44-cfcfefba84c6
  Args:
    source: Alexander_Mountbatten
    target: Prince_Henry_of_Battenberg
    relation: :hasFather
  Finish (8f740c50-bfc6-4ccb-ba28-4be4561d5653)
 Call ID: 8f740c50-bfc6-4ccb-ba28-4be4561d5653
  Args: