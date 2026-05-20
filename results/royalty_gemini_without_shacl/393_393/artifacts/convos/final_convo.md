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
Nikolaus, Hereditary Grand Duke of Oldenburg (German: Nikolaus Friedrich Wilhelm von Holstein-Gottorp, Erbgroßherzog von Oldenburg; 10 August 1897 – 3 April 1970) was the eldest son of Frederick Augustus II, Grand Duke of Oldenburg, who was the last ruling Grand Duke of Oldenburg.
In 1931, Nikolaus succeeded to his father's titles and assumed the role of pretender to the Grand Duchy, until his death in 1970.
Early life

Nikolaus was born at Oldenburg, Grand Duchy of Oldenburg, the third child and first son of Frederick Augustus II, Grand Duke of Oldenburg (1852–1931) (son of Peter II, Grand Duke of Oldenburg and Princess Elisabeth of Saxe-Altenburg) and his wife, Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin (1869–1955) (daughter of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and Princess Marie of Schwarzburg-Rudolstadt).
He was a first cousin of Queen Juliana of the Netherlands and with his wife and other family members was a guest at her 1937 wedding to Prince Bernhard of Lippe-Biesterfeld.
Marriage and issue

Nikolaus married on 26 October 1921 in Arolsen to Princess Helena of Waldeck and Pyrmont (1899–1948), only daughter of Friedrich, Prince of Waldeck and Pyrmont, and Princess Bathildis of Schaumburg-Lippe.
They had nine children:


When his first wife died in 1948, he married secondly on 20 September 1950 in Güldenstein to a fellow noblewoman, Anne-Marie von Schutzbar genannt Milchling (1903–1991), former wife of Count Bechtold von Bernstorff, daughter of Rudolf von Schutzbar gen. Milchling (1853-1935) and Rose Marston (1872-1957).



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
  AssignClass (5c157b37-cef3-4f1a-b5c6-58fc359a9ed3)
 Call ID: 5c157b37-cef3-4f1a-b5c6-58fc359a9ed3
  Args:
    source: Nikolaus_of_Oldenburg
    type: :Man
  AssignClass (d716c858-b5b7-4b87-9968-49b1e88150c7)
 Call ID: d716c858-b5b7-4b87-9968-49b1e88150c7
  Args:
    type: :Person
    source: Nikolaus_of_Oldenburg
  AddLiteral (48a009be-486b-489f-83cc-43347e8a5630)
 Call ID: 48a009be-486b-489f-83cc-43347e8a5630
  Args:
    source: Nikolaus_of_Oldenburg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1897
  AddLiteral (c726e914-8eb9-4b7d-b2f4-f5c7de66bf19)
 Call ID: c726e914-8eb9-4b7d-b2f4-f5c7de66bf19
  Args:
    relation: :hasDeathYear
    source: Nikolaus_of_Oldenburg
    literal_value: 1970
    literal_type: xsd:integer
  AssignClass (9e401ee3-6ebd-4e65-9201-c01e002813c5)
 Call ID: 9e401ee3-6ebd-4e65-9201-c01e002813c5
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (6d5c38c6-a4c4-49aa-9282-13c965978576)
 Call ID: 6d5c38c6-a4c4-49aa-9282-13c965978576
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    type: :Person
  AddTriple (6a399291-0f5c-4071-a7dc-7c0aaacd98f8)
 Call ID: 6a399291-0f5c-4071-a7dc-7c0aaacd98f8
  Args:
    source: Nikolaus_of_Oldenburg
    relation: :hasFather
    target: Frederick_Augustus_II_of_Oldenburg
  AssignClass (c9eabf3b-1417-425a-9d92-c152773914da)
 Call ID: c9eabf3b-1417-425a-9d92-c152773914da
  Args:
    type: :Woman
    source: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
  AssignClass (63087894-5edb-438d-9f93-3936fe97087d)
 Call ID: 63087894-5edb-438d-9f93-3936fe97087d
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (8a2945df-8776-4691-8232-6f39d7275baa)
 Call ID: 8a2945df-8776-4691-8232-6f39d7275baa
  Args:
    target: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    relation: :hasMother
    source: Nikolaus_of_Oldenburg
  AssignClass (9ee88de4-75bf-4cc8-ae20-82b117c07671)
 Call ID: 9ee88de4-75bf-4cc8-ae20-82b117c07671
  Args:
    source: Peter_II_of_Oldenburg
    type: :Man
  AssignClass (a6e9f8cb-ae2f-4b20-8dde-67d237c40f99)
 Call ID: a6e9f8cb-ae2f-4b20-8dde-67d237c40f99
  Args:
    type: :Person
    source: Peter_II_of_Oldenburg
  AddTriple (c82ed043-2b21-4a30-a45e-f83a25f04e73)
 Call ID: c82ed043-2b21-4a30-a45e-f83a25f04e73
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    relation: :hasFather
    target: Peter_II_of_Oldenburg
  AssignClass (e1e152ff-3b37-46d6-8ecc-f984e6fe90cc)
 Call ID: e1e152ff-3b37-46d6-8ecc-f984e6fe90cc
  Args:
    source: Elisabeth_of_Saxe_Altenburg
    type: :Woman
  AssignClass (a82efefd-7572-42b1-bf36-f32e7da18688)
 Call ID: a82efefd-7572-42b1-bf36-f32e7da18688
  Args:
    type: :Person
    source: Elisabeth_of_Saxe_Altenburg
  AddTriple (64fa387a-ddf3-45c8-92c6-91f2d9dc7013)
 Call ID: 64fa387a-ddf3-45c8-92c6-91f2d9dc7013
  Args:
    target: Elisabeth_of_Saxe_Altenburg
    relation: :hasMother
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (12343064-86d5-4db6-8b5b-8921779968e5)
 Call ID: 12343064-86d5-4db6-8b5b-8921779968e5
  Args:
    source: Frederick_Francis_II_of_Mecklenburg_Schwerin
    type: :Man
  AssignClass (02235796-7b4b-40ff-a0ea-36444af128ab)
 Call ID: 02235796-7b4b-40ff-a0ea-36444af128ab
  Args:
    type: :Person
    source: Frederick_Francis_II_of_Mecklenburg_Schwerin
  AddTriple (144d72a1-10bb-4423-b68f-a2c7783a24f4)
 Call ID: 144d72a1-10bb-4423-b68f-a2c7783a24f4
  Args:
    target: Frederick_Francis_II_of_Mecklenburg_Schwerin
    relation: :hasFather
    source: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
  AssignClass (e31f8d38-ef73-4dd7-9e2f-1e0a31f5acca)
 Call ID: e31f8d38-ef73-4dd7-9e2f-1e0a31f5acca
  Args:
    source: Marie_of_Schwarzburg_Rudolstadt
    type: :Woman
  AssignClass (5617c0ad-5df3-4945-b777-cb7c843174f4)
 Call ID: 5617c0ad-5df3-4945-b777-cb7c843174f4
  Args:
    source: Marie_of_Schwarzburg_Rudolstadt
    type: :Person
  AddTriple (f80697fc-2380-464a-8818-19f478f92d39)
 Call ID: f80697fc-2380-464a-8818-19f478f92d39
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    relation: :hasMother
    target: Marie_of_Schwarzburg_Rudolstadt
  AssignClass (b32a4eda-ca74-4dac-9ca5-cfe0ae9b6bf3)
 Call ID: b32a4eda-ca74-4dac-9ca5-cfe0ae9b6bf3
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    type: :Woman
  AssignClass (5b29da2a-c392-452a-9b8e-f8273482de57)
 Call ID: 5b29da2a-c392-452a-9b8e-f8273482de57
  Args:
    type: :Person
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (7dd35eba-40dc-4240-b47c-54cf965a3698)
 Call ID: 7dd35eba-40dc-4240-b47c-54cf965a3698
  Args:
    source: Nikolaus_of_Oldenburg
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1921
  AddTriple (c1539070-c7e6-4ecc-b6da-713066892b8f)
 Call ID: c1539070-c7e6-4ecc-b6da-713066892b8f
  Args:
    relation: :hasRelation
    source: Nikolaus_of_Oldenburg
    target: Helena_of_Waldeck_and_Pyrmont
  AssignClass (e484f33f-120a-4bf7-9ea3-4396b459079a)
 Call ID: e484f33f-120a-4bf7-9ea3-4396b459079a
  Args:
    type: :Man
    source: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (d1b34547-4880-46dc-97b6-13bb476079e8)
 Call ID: d1b34547-4880-46dc-97b6-13bb476079e8
  Args:
    source: Friedrich_of_Waldeck_and_Pyrmont
    type: :Person
  AddTriple (23b60247-de51-4657-a2ef-673ff188d7bf)
 Call ID: 23b60247-de51-4657-a2ef-673ff188d7bf
  Args:
    target: Friedrich_of_Waldeck_and_Pyrmont
    source: Helena_of_Waldeck_and_Pyrmont
    relation: :hasFather
  AssignClass (c8b6500b-30d3-4aae-a3fe-46ceb9a7f943)
 Call ID: c8b6500b-30d3-4aae-a3fe-46ceb9a7f943
  Args:
    source: Bathildis_of_Schaumburg_Lippe
    type: :Woman
  AssignClass (0aa42a3c-2772-48f9-9e8c-5f769c77a5ee)
 Call ID: 0aa42a3c-2772-48f9-9e8c-5f769c77a5ee
  Args:
    source: Bathildis_of_Schaumburg_Lippe
    type: :Person
  AddTriple (7ebad23f-b3e8-4ee3-b1d6-0b150b3f36d6)
 Call ID: 7ebad23f-b3e8-4ee3-b1d6-0b150b3f36d6
  Args:
    target: Bathildis_of_Schaumburg_Lippe
    relation: :hasMother
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (56980f98-be9a-4952-91f8-b30093cbd0a9)
 Call ID: 56980f98-be9a-4952-91f8-b30093cbd0a9
  Args:
    source: Anne_Marie_von_Schutzbar_genannt_Milchling
    type: :Woman
  AssignClass (f85ba720-3525-4f49-a4b7-f527f1a1d6f2)
 Call ID: f85ba720-3525-4f49-a4b7-f527f1a1d6f2
  Args:
    type: :Person
    source: Anne_Marie_von_Schutzbar_genannt_Milchling
  AddLiteral (be8700d0-6893-4b5b-ad55-d7f56b807f5c)
 Call ID: be8700d0-6893-4b5b-ad55-d7f56b807f5c
  Args:
    source: Nikolaus_of_Oldenburg
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1950
  AddTriple (07ca7958-d878-4bb5-beb5-51b522dcb24f)
 Call ID: 07ca7958-d878-4bb5-beb5-51b522dcb24f
  Args:
    target: Anne_Marie_von_Schutzbar_genannt_Milchling
    relation: :hasRelation
    source: Nikolaus_of_Oldenburg
  AssignClass (4e7b9332-1da2-402d-b0ed-0695263c7485)
 Call ID: 4e7b9332-1da2-402d-b0ed-0695263c7485
  Args:
    type: :Man
    source: Rudolf_von_Schutzbar_gen_Milchling
  AssignClass (4b9c77a5-ac5d-4169-bbad-20a390a08ee2)
 Call ID: 4b9c77a5-ac5d-4169-bbad-20a390a08ee2
  Args:
    source: Rudolf_von_Schutzbar_gen_Milchling
    type: :Person
  AddTriple (cab000af-e777-4e7e-829a-7731cb3bb47d)
 Call ID: cab000af-e777-4e7e-829a-7731cb3bb47d
  Args:
    target: Rudolf_von_Schutzbar_gen_Milchling
    relation: :hasFather
    source: Anne_Marie_von_Schutzbar_genannt_Milchling
  AssignClass (6e471894-0740-4491-98de-a3fb538d7ca9)
 Call ID: 6e471894-0740-4491-98de-a3fb538d7ca9
  Args:
    type: :Woman
    source: Rose_Marston
  AssignClass (d744d4af-d6a5-4426-8147-e546959cb631)
 Call ID: d744d4af-d6a5-4426-8147-e546959cb631
  Args:
    source: Rose_Marston
    type: :Person
  AddTriple (9aab7386-97b0-46dd-987a-ca44290b21a1)
 Call ID: 9aab7386-97b0-46dd-987a-ca44290b21a1
  Args:
    relation: :hasMother
    source: Anne_Marie_von_Schutzbar_genannt_Milchling
    target: Rose_Marston
  Finish (c24a2a1c-991d-4d6d-ad7f-d3190cdf99ac)
 Call ID: c24a2a1c-991d-4d6d-ad7f-d3190cdf99ac
  Args: