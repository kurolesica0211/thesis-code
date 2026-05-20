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
Don Carlos, Prince of Bourbon-Two Sicilies, Infante of Spain (Full Italian name: Carlo Maria Francesco d'Assisi Pasquale Ferdinando Antonio di Padova Francesco de Paola Alfonso Andrea Avelino Tancredi, Principe di Borbone delle Due Sicilie, Infante di Spagna; 10 November 1870 – 11 November 1949) was the son of Prince Alfonso of the Two Sicilies, Count of Caserta and Princess Maria Antonietta of Bourbon-Two Sicilies, and nephew of the last King of the Two Sicilies, Francis II.


Marriages and children

On 14 February 1901 in Madrid, Carlos married Mercedes, Princess of Asturias, elder daughter of the late King Alfonso XII of Spain and of his wife Archduchess Maria Christina of Austria.
Mercedes was the elder sister and heir presumptive to King Alfonso XIII of Spain, an unmarried teenager.
A week before the wedding, on 7 February, Carlos was given the title of Infante of Spain.
In 1907, Carlos married secondly to Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris.
The couple had four children:


Prince Carlos's descendants include King Felipe VI of Spain, Prince Pedro, Duke of Calabria, Prince Pedro Carlos of Orléans-Braganza, and Philip, Hereditary Prince of Yugoslavia, among others.
Military service

Carlos served in the Spanish Army in the Spanish–American War and received the Military Order of Maria Cristina.
Two Sicilies succession

In 1894, Carlos's father Alfonso became the head of the House of Bourbon-Two Sicilies.
On marrying his first wife, Carlos renounced on 14 December 1900 his future rights of succession to the non-existent Crown of Two Sicilies in an official document, known as the Act of Cannes, subject to a requirement in the Treaty of Naples of 1759 and the Pragmatic Decree of 6 October 1759 that the Crown of Spain should not be combined with the "Italian Sovereignty".
In 1960, Carlos' elder brother Ferdinand died without male issue, and a dispute arose between Carlos' son Alfonso and Carlos' younger brother Ranieri on the headship of the house, this with competing claims: by the law of primogeniture, Carlos' son Alfonso was considered the heir, but Ranieri claimed that Carlos had renounced his rights and those of his descendants according to the Act of Cannes.
Alfonso refuted that claim by stating that it was only a promise from his father to relinquish this right if the crown of the Kingdom of the Two Sicilies were to be united with the Spanish Crown.
Since this did not happen, the act had no effect and Carlos' son Alfonso reclaimed his rights.
Alfonso's claim was recognised by the heads of the different lines of the House of Bourbon, although not by the head of the Orleans family, and in 1983 the Spanish Council of State, following an investigation by the Ministries of Justice and Foreign Affairs, the Royal Academy of Jurisprudence and Legislation and the Institute Salazar y Castro concluded unanimously in favour of Infante Don Alfonso's only son, Prince and Infante Don Carlos, a position shared by the Spanish Royal House.



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
  AssignClass (2f552507-8e30-42a3-84a2-81bb0dc4fc3f)
 Call ID: 2f552507-8e30-42a3-84a2-81bb0dc4fc3f
  Args:
    type: :Man
    source: Don_Carlos
  AssignClass (15dd341d-9c12-47e1-a251-5cc677672f45)
 Call ID: 15dd341d-9c12-47e1-a251-5cc677672f45
  Args:
    type: :Person
    source: Don_Carlos
  AddLiteral (503f11fd-8e8d-4627-aae8-99589eead609)
 Call ID: 503f11fd-8e8d-4627-aae8-99589eead609
  Args:
    source: Don_Carlos
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1870
  AddLiteral (96471a6d-1a29-46b2-8308-dd974f7a702a)
 Call ID: 96471a6d-1a29-46b2-8308-dd974f7a702a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1949
    source: Don_Carlos
  AssignClass (e4ee32fa-f7d6-4ccf-95c8-8ac2157bcdcd)
 Call ID: e4ee32fa-f7d6-4ccf-95c8-8ac2157bcdcd
  Args:
    type: :Man
    source: Prince_Alfonso
  AssignClass (af7d11a2-9662-4e4d-9ea4-a382f606e9d3)
 Call ID: af7d11a2-9662-4e4d-9ea4-a382f606e9d3
  Args:
    source: Prince_Alfonso
    type: :Person
  AssignClass (73632c8d-ec9b-442e-8047-bcddc5ca1ae0)
 Call ID: 73632c8d-ec9b-442e-8047-bcddc5ca1ae0
  Args:
    type: :Woman
    source: Maria_Antonietta
  AssignClass (f81115ad-d50d-4949-9804-1fd39da6e33c)
 Call ID: f81115ad-d50d-4949-9804-1fd39da6e33c
  Args:
    source: Maria_Antonietta
    type: :Person
  AddTriple (dca44752-7b38-4cf3-a577-47a1ee0f5cf1)
 Call ID: dca44752-7b38-4cf3-a577-47a1ee0f5cf1
  Args:
    target: Prince_Alfonso
    relation: :hasFather
    source: Don_Carlos
  AddTriple (a69c9616-4ec8-40fa-8e87-74dd18f3dac6)
 Call ID: a69c9616-4ec8-40fa-8e87-74dd18f3dac6
  Args:
    target: Maria_Antonietta
    relation: :hasMother
    source: Don_Carlos
  AssignClass (7cf5b542-7960-4988-8e1d-1558649a463b)
 Call ID: 7cf5b542-7960-4988-8e1d-1558649a463b
  Args:
    source: Francis_II
    type: :Man
  AssignClass (fbf12a61-c42b-4c2a-b483-bee386efd6ee)
 Call ID: fbf12a61-c42b-4c2a-b483-bee386efd6ee
  Args:
    type: :Person
    source: Francis_II
  AssignClass (a217b5f3-b88c-4938-8d48-90d19eaa897f)
 Call ID: a217b5f3-b88c-4938-8d48-90d19eaa897f
  Args:
    type: :Woman
    source: Mercedes
  AssignClass (1208b090-1d17-44fe-9e81-03dd6b10bb37)
 Call ID: 1208b090-1d17-44fe-9e81-03dd6b10bb37
  Args:
    source: Mercedes
    type: :Person
  AddLiteral (b2235cb0-0337-4242-89c3-85ce05036f2b)
 Call ID: b2235cb0-0337-4242-89c3-85ce05036f2b
  Args:
    source: Don_Carlos
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1901
  AssignClass (fca8157e-6014-4f80-a7b8-0a92dd208efd)
 Call ID: fca8157e-6014-4f80-a7b8-0a92dd208efd
  Args:
    type: :Man
    source: Alfonso_XII
  AssignClass (406ba103-fb79-44c7-bd12-6501270b3cce)
 Call ID: 406ba103-fb79-44c7-bd12-6501270b3cce
  Args:
    type: :Person
    source: Alfonso_XII
  AssignClass (0501a31e-7fe7-4d47-9a45-8947ce15ad71)
 Call ID: 0501a31e-7fe7-4d47-9a45-8947ce15ad71
  Args:
    source: Maria_Christina
    type: :Woman
  AssignClass (c634e25f-620d-4e1f-b3e4-458f8423fbab)
 Call ID: c634e25f-620d-4e1f-b3e4-458f8423fbab
  Args:
    type: :Person
    source: Maria_Christina
  AddTriple (7c8ba5b5-d350-4457-b166-4362e48c475d)
 Call ID: 7c8ba5b5-d350-4457-b166-4362e48c475d
  Args:
    target: Alfonso_XII
    relation: :hasFather
    source: Mercedes
  AddTriple (b49cb8b4-f05b-41d3-9022-d68c1bf135b6)
 Call ID: b49cb8b4-f05b-41d3-9022-d68c1bf135b6
  Args:
    relation: :hasMother
    target: Maria_Christina
    source: Mercedes
  AssignClass (27a5e66a-ce69-4d24-8e93-a7f0b8df11c0)
 Call ID: 27a5e66a-ce69-4d24-8e93-a7f0b8df11c0
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (7df0a83e-1d5e-4013-8c3f-a350a31c6084)
 Call ID: 7df0a83e-1d5e-4013-8c3f-a350a31c6084
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (e75d3da5-4887-4e0d-8200-ac0a0b4918c9)
 Call ID: e75d3da5-4887-4e0d-8200-ac0a0b4918c9
  Args:
    type: :Woman
    source: Louise_of_Orleans
  AssignClass (73da1555-b991-462c-a22f-b847e6da7985)
 Call ID: 73da1555-b991-462c-a22f-b847e6da7985
  Args:
    type: :Person
    source: Louise_of_Orleans
  AddLiteral (9d19bd0c-f648-4d7a-bb8d-ee291640a3fc)
 Call ID: 9d19bd0c-f648-4d7a-bb8d-ee291640a3fc
  Args:
    literal_value: 1907
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Don_Carlos
  AssignClass (b3021096-bd6f-45a1-86a0-6305ec881230)
 Call ID: b3021096-bd6f-45a1-86a0-6305ec881230
  Args:
    source: Philippe_Count_of_Paris
    type: :Man
  AssignClass (15ae7a06-1f08-4503-a815-1518c5ae7aec)
 Call ID: 15ae7a06-1f08-4503-a815-1518c5ae7aec
  Args:
    source: Philippe_Count_of_Paris
    type: :Person
  AddTriple (d4d75802-3dde-4c17-a2c1-698e0f3dd305)
 Call ID: d4d75802-3dde-4c17-a2c1-698e0f3dd305
  Args:
    relation: :hasFather
    target: Philippe_Count_of_Paris
    source: Louise_of_Orleans
  AssignClass (a41e06e8-e30d-4669-8cbb-34144720f98c)
 Call ID: a41e06e8-e30d-4669-8cbb-34144720f98c
  Args:
    type: :Man
    source: Ferdinand
  AssignClass (d7556a12-12cc-483c-bcbc-b0bfdf410315)
 Call ID: d7556a12-12cc-483c-bcbc-b0bfdf410315
  Args:
    type: :Person
    source: Ferdinand
  AddTriple (b47125a1-9d96-46a1-bbe3-c143c538c490)
 Call ID: b47125a1-9d96-46a1-bbe3-c143c538c490
  Args:
    relation: :isBrotherOf
    target: Don_Carlos
    source: Ferdinand
  AssignClass (cc8159be-eb02-400a-9cfd-b8e8ee5b5c81)
 Call ID: cc8159be-eb02-400a-9cfd-b8e8ee5b5c81
  Args:
    type: :Man
    source: Ranieri
  AssignClass (39138fda-b0ef-45d1-a40b-c29fbd53902f)
 Call ID: 39138fda-b0ef-45d1-a40b-c29fbd53902f
  Args:
    type: :Person
    source: Ranieri
  AddTriple (e45de5e9-bd13-44c1-a28b-b49df379b13b)
 Call ID: e45de5e9-bd13-44c1-a28b-b49df379b13b
  Args:
    source: Ranieri
    relation: :isBrotherOf
    target: Don_Carlos
  AssignClass (da426309-dae3-4f1d-9c7e-f310e5f77ca9)
 Call ID: da426309-dae3-4f1d-9c7e-f310e5f77ca9
  Args:
    source: Alfonso_son_of_Carlos
    type: :Man
  AssignClass (7f844c13-ecbf-424e-bfae-a10de271f9e6)
 Call ID: 7f844c13-ecbf-424e-bfae-a10de271f9e6
  Args:
    source: Alfonso_son_of_Carlos
    type: :Person
  AddTriple (f7694e04-2e2d-4ff2-9030-a5ffae8d3ae1)
 Call ID: f7694e04-2e2d-4ff2-9030-a5ffae8d3ae1
  Args:
    relation: :hasFather
    target: Don_Carlos
    source: Alfonso_son_of_Carlos
  Finish (8c55f4d6-696b-4e8f-a1c3-4a9f1636dc58)
 Call ID: 8c55f4d6-696b-4e8f-a1c3-4a9f1636dc58
  Args: