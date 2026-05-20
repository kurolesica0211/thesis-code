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
Princess Elisabeth of Denmark (Elisabeth Caroline-Mathilde Alexandrine Helena Olga Thyra Feodora Estrid Margrethe Désirée; 8 May 1935 – 19 June 2018) was a member of the Danish royal family.
The only daughter and eldest child of Knud, Hereditary Prince of Denmark, and Princess Caroline-Mathilde of Denmark, she was a granddaughter of Christian X, niece of Frederik IX, and first cousin of Margrethe II.
In addition to undertaking occasionally royal duties, she was a career diplomat with the Ministry of Foreign Affairs of Denmark.
Early life and education

Elisabeth was born on 8 May 1935 in Copenhagen to Prince Knud and Princess Caroline-Mathilde of Denmark.
Her father was the second son of Christian X.
The family resided at Sorgenfri Palace in Kongens Lyngby, where she was raised with her two younger brothers Prince Ingolf and Prince Christian.
During the 1938-39 Mørkefjord expedition, paleontologist Eigil Nielsen named the Princess Elisabeth Alps in northeastern Greenland after her.
Elisabeth began her education privately at Sorgenfri.
Subsequently, she attended Suhr's School of Home Economics and then Margrethe-Skolen (now the Scandinavian Academy of International Fashion and Design) from 1954 to 1956.
In 1953, when  succession to the Danish throne switched from agnatic primogeniture to male-preference primogeniture, Elisabeth gained succession rights and became seventh in line to the throne.
She was titled of Prinsesse til Danmark (literally translated as "Princess to Denmark", reserved for members of the Royal Family in the line of succession) with the style of Highness.
She was the only one of her siblings to retain her title and succession rights, as her younger brothers married commoners without the permission of their uncle, Frederik IX.
Career

In 1956, Elisabeth began her career with the Danish Ministry of Foreign Affairs.
She was posted to the Embassy of Denmark, Washington, D.C. from 1973 to 1976 and again from 1981 to 1985.
In addition to her diplomatic career, Elisabeth occasionally undertook royal duties on behalf of her uncle and later cousin.
Personal life and death

Elisabeth never married nor had children.
After a long period of ill health, Elisabeth died on 19 June 2018, at the age of 83.



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
  AssignClass (d9869d9d-59c1-4481-91aa-3329458b31e3)
 Call ID: d9869d9d-59c1-4481-91aa-3329458b31e3
  Args:
    type: :Woman
    source: Elisabeth_of_Denmark
  AssignClass (874111ad-7bdc-4666-8e78-408e2c1c5364)
 Call ID: 874111ad-7bdc-4666-8e78-408e2c1c5364
  Args:
    type: :Person
    source: Elisabeth_of_Denmark
  AddLiteral (0f830fff-56eb-449d-b7f3-85c6189351b2)
 Call ID: 0f830fff-56eb-449d-b7f3-85c6189351b2
  Args:
    source: Elisabeth_of_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1935
  AddLiteral (ff4e1ab2-7acc-4803-8b76-db0ca7899d1d)
 Call ID: ff4e1ab2-7acc-4803-8b76-db0ca7899d1d
  Args:
    literal_value: 2018
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Elisabeth_of_Denmark
  AssignClass (b1edaeba-dd12-45d4-8678-7b9e2d565483)
 Call ID: b1edaeba-dd12-45d4-8678-7b9e2d565483
  Args:
    type: :Man
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (f7f69659-780f-4d38-9914-1be80355ecac)
 Call ID: f7f69659-780f-4d38-9914-1be80355ecac
  Args:
    source: Knud_Hereditary_Prince_of_Denmark
    type: :Person
  AssignClass (17fa5f22-2694-47ef-b5cb-de8e5d3687e0)
 Call ID: 17fa5f22-2694-47ef-b5cb-de8e5d3687e0
  Args:
    type: :Woman
    source: Caroline-Mathilde_of_Denmark
  AssignClass (66066e00-c6ce-45be-9af3-c2c9aa23fb4c)
 Call ID: 66066e00-c6ce-45be-9af3-c2c9aa23fb4c
  Args:
    type: :Person
    source: Caroline-Mathilde_of_Denmark
  AddTriple (c74eb686-8723-4d23-a706-542f87f4d9a3)
 Call ID: c74eb686-8723-4d23-a706-542f87f4d9a3
  Args:
    relation: :hasFather
    source: Elisabeth_of_Denmark
    target: Knud_Hereditary_Prince_of_Denmark
  AddTriple (c90d7a7c-eab2-4a20-8875-0adf9e9c73c3)
 Call ID: c90d7a7c-eab2-4a20-8875-0adf9e9c73c3
  Args:
    relation: :hasMother
    source: Elisabeth_of_Denmark
    target: Caroline-Mathilde_of_Denmark
  AssignClass (be2cd5f2-9a07-4a54-97be-cfed0561e4f4)
 Call ID: be2cd5f2-9a07-4a54-97be-cfed0561e4f4
  Args:
    source: Christian_X
    type: :Man
  AssignClass (751d0c46-8977-4c6b-b7c1-6dd9b1c8133a)
 Call ID: 751d0c46-8977-4c6b-b7c1-6dd9b1c8133a
  Args:
    type: :Person
    source: Christian_X
  AddTriple (a0d26f1c-3003-442e-bc60-c7910e5b5a9d)
 Call ID: a0d26f1c-3003-442e-bc60-c7910e5b5a9d
  Args:
    relation: :hasFather
    target: Christian_X
    source: Knud_Hereditary_Prince_of_Denmark
  AssignClass (0fc2ef80-86d0-47b4-8026-883e20e27433)
 Call ID: 0fc2ef80-86d0-47b4-8026-883e20e27433
  Args:
    source: Ingolf_of_Denmark
    type: :Man
  AssignClass (5531d4bc-2c99-42d9-9da6-48dc306f1b93)
 Call ID: 5531d4bc-2c99-42d9-9da6-48dc306f1b93
  Args:
    source: Ingolf_of_Denmark
    type: :Person
  AssignClass (ec967ccb-99dd-4013-a17a-abd1f30b855c)
 Call ID: ec967ccb-99dd-4013-a17a-abd1f30b855c
  Args:
    source: Christian_of_Denmark
    type: :Man
  AssignClass (ad54f1ab-9b6d-4577-8e71-8f9833fd9909)
 Call ID: ad54f1ab-9b6d-4577-8e71-8f9833fd9909
  Args:
    type: :Person
    source: Christian_of_Denmark
  AddTriple (d45410b6-c1bf-47e7-9d05-56ac975c8854)
 Call ID: d45410b6-c1bf-47e7-9d05-56ac975c8854
  Args:
    relation: :hasBrother
    target: Ingolf_of_Denmark
    source: Elisabeth_of_Denmark
  AddTriple (7956a33e-3186-43d4-9408-f36ae50ae7a5)
 Call ID: 7956a33e-3186-43d4-9408-f36ae50ae7a5
  Args:
    source: Elisabeth_of_Denmark
    target: Christian_of_Denmark
    relation: :hasBrother
  AddTriple (c63a63e1-43ac-4316-a501-5ec7038b5620)
 Call ID: c63a63e1-43ac-4316-a501-5ec7038b5620
  Args:
    source: Ingolf_of_Denmark
    target: Knud_Hereditary_Prince_of_Denmark
    relation: :hasFather
  AddTriple (c382d3d5-d52b-41ad-ab10-b895468f2fa6)
 Call ID: c382d3d5-d52b-41ad-ab10-b895468f2fa6
  Args:
    source: Christian_of_Denmark
    target: Knud_Hereditary_Prince_of_Denmark
    relation: :hasFather
  AddTriple (16156d87-c1b2-4b6c-80a4-22cf7c07c314)
 Call ID: 16156d87-c1b2-4b6c-80a4-22cf7c07c314
  Args:
    source: Ingolf_of_Denmark
    target: Caroline-Mathilde_of_Denmark
    relation: :hasMother
  AddTriple (de98625e-9e25-4875-bb34-64058df5d90c)
 Call ID: de98625e-9e25-4875-bb34-64058df5d90c
  Args:
    source: Christian_of_Denmark
    target: Caroline-Mathilde_of_Denmark
    relation: :hasMother
  AssignClass (82beb66b-e3fb-42bf-80a7-844d99040611)
 Call ID: 82beb66b-e3fb-42bf-80a7-844d99040611
  Args:
    source: Frederik_IX
    type: :Man
  AssignClass (70184723-62d1-484c-b74b-74599d8f9430)
 Call ID: 70184723-62d1-484c-b74b-74599d8f9430
  Args:
    source: Frederik_IX
    type: :Person
  AssignClass (a9e33107-a9f8-402c-bd0e-b20afcb2e09f)
 Call ID: a9e33107-a9f8-402c-bd0e-b20afcb2e09f
  Args:
    source: Margrethe_II
    type: :Woman
  AssignClass (8fafe77a-7370-4dd8-a404-4aab16c5e456)
 Call ID: 8fafe77a-7370-4dd8-a404-4aab16c5e456
  Args:
    type: :Person
    source: Margrethe_II
  Finish (e0778348-0452-4708-ae74-ae3d68963732)
 Call ID: e0778348-0452-4708-ae74-ae3d68963732
  Args: