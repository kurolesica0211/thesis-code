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
Granville James Leveson-Gower, 5th Earl Granville MC (6 December 1918 – 31 October 1996) was a British soldier, banker, peer, and landowner, a member of the House of Lords from 1953 until his death.
Early life

The son of Vice-Admiral William Leveson-Gower, 4th Earl Granville, and his wife Lady Rose Bowes-Lyon, a daughter of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne, he was educated at Eton College.
Known formally as Lord Leveson until 1953, he was commissioned into the Coldstream Guards and saw active service during the Second World War, in which he was twice wounded and mentioned in despatches.
Later career

After the war, Lord Leveson joined Coutts & Co., a private bank.
On 25 June 1953, he succeeded his father as Earl Granville (created 1833), Viscount Granville (1814), and Baron Leveson of Stone (1814), giving him a seat in the House of Lords.
In 1958, Granville married Doon Aileen Plunket, daughter of Brindsley Sheridan Bushe Plunket and granddaughter of William Plunket, 5th Baron Plunket.
Her mother was Aileen Sibell Mary Guinness, a granddaughter of Edward Guinness, 1st Earl of Iveagh.
In 1960, shortly after the birth of his first child, Granville bought the island of North Uist in the Outer Hebrides from the Duke of Hamilton, becoming its laird.
In 1974 Granville was appointed as a Deputy Lieutenant of Inverness-shire and was Vice-Lord-Lieutenant of the Western Isles between January 1976 and 1983, then Lord-Lieutenant from 1983 to December 1993, when he was succeeded by Viscount Dunrossil.



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
  AssignClass (c78ff800-ea18-4b28-ba90-4798c60e5e09)
 Call ID: c78ff800-ea18-4b28-ba90-4798c60e5e09
  Args:
    type: :Person
    source: Granville_James_Leveson-Gower
  AssignClass (42f778d0-41fb-441c-ac90-c1602e89cc96)
 Call ID: 42f778d0-41fb-441c-ac90-c1602e89cc96
  Args:
    type: :Man
    source: Granville_James_Leveson-Gower
  AddLiteral (b4de4fbb-d416-40bc-b902-5053be7d070f)
 Call ID: b4de4fbb-d416-40bc-b902-5053be7d070f
  Args:
    source: Granville_James_Leveson-Gower
    literal_type: xsd:integer
    literal_value: 1918
    relation: :hasBirthYear
  AddLiteral (bc911552-c067-4aaf-8b69-1fcfc5b38cf3)
 Call ID: bc911552-c067-4aaf-8b69-1fcfc5b38cf3
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1996
    source: Granville_James_Leveson-Gower
  AssignClass (092b45e0-73aa-464b-9a49-766afc4afe7f)
 Call ID: 092b45e0-73aa-464b-9a49-766afc4afe7f
  Args:
    type: :Person
    source: William_Leveson-Gower
  AssignClass (8679cd80-f168-4be5-8b1a-dab7e31db567)
 Call ID: 8679cd80-f168-4be5-8b1a-dab7e31db567
  Args:
    type: :Man
    source: William_Leveson-Gower
  AssignClass (dde4af75-aaf8-486c-9a90-9908a493ae92)
 Call ID: dde4af75-aaf8-486c-9a90-9908a493ae92
  Args:
    type: :Ancestor
    source: William_Leveson-Gower
  AddTriple (2c134f9a-d645-4e05-b378-3882d27dbd0f)
 Call ID: 2c134f9a-d645-4e05-b378-3882d27dbd0f
  Args:
    relation: :hasFather
    source: Granville_James_Leveson-Gower
    target: William_Leveson-Gower
  AssignClass (fb003f89-21be-47b6-bd0f-b72f4076397b)
 Call ID: fb003f89-21be-47b6-bd0f-b72f4076397b
  Args:
    type: :Person
    source: Rose_Bowes-Lyon
  AssignClass (c08cc60c-20d9-4326-86a6-04a179531ba6)
 Call ID: c08cc60c-20d9-4326-86a6-04a179531ba6
  Args:
    type: :Woman
    source: Rose_Bowes-Lyon
  AssignClass (10bf8b59-8709-473a-a139-1d95ac4f24b7)
 Call ID: 10bf8b59-8709-473a-a139-1d95ac4f24b7
  Args:
    type: :Ancestor
    source: Rose_Bowes-Lyon
  AddTriple (a9513bd1-d540-4f3f-8610-6406dfc06cb4)
 Call ID: a9513bd1-d540-4f3f-8610-6406dfc06cb4
  Args:
    source: Granville_James_Leveson-Gower
    relation: :hasMother
    target: Rose_Bowes-Lyon
  AssignClass (46e6ccdb-901c-420f-8097-1995cd70cd8b)
 Call ID: 46e6ccdb-901c-420f-8097-1995cd70cd8b
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AssignClass (105479de-0301-482d-9489-2e4f9283ae7b)
 Call ID: 105479de-0301-482d-9489-2e4f9283ae7b
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (68994629-4531-42e8-962e-c4c90ac70cd5)
 Call ID: 68994629-4531-42e8-962e-c4c90ac70cd5
  Args:
    type: :Ancestor
    source: Claude_Bowes-Lyon
  AddTriple (184ac11e-65de-4086-a926-162f3400ae8a)
 Call ID: 184ac11e-65de-4086-a926-162f3400ae8a
  Args:
    source: Rose_Bowes-Lyon
    relation: :hasFather
    target: Claude_Bowes-Lyon
  AddLiteral (276716e1-23c3-434c-b94d-5f987ae143b1)
 Call ID: 276716e1-23c3-434c-b94d-5f987ae143b1
  Args:
    source: Granville_James_Leveson-Gower
    literal_value: Lord Leveson
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AssignClass (d54455d3-4e94-4e6c-a361-b42a25d231ce)
 Call ID: d54455d3-4e94-4e6c-a361-b42a25d231ce
  Args:
    type: :Person
    source: Doon_Aileen_Plunket
  AssignClass (9104a8b3-25de-4588-838a-6ef088ae71bb)
 Call ID: 9104a8b3-25de-4588-838a-6ef088ae71bb
  Args:
    type: :Woman
    source: Doon_Aileen_Plunket
  AddLiteral (6c3b2648-d878-4d0f-8988-37d7157cd772)
 Call ID: 6c3b2648-d878-4d0f-8988-37d7157cd772
  Args:
    source: Granville_James_Leveson-Gower
    literal_type: xsd:integer
    literal_value: 1958
    relation: :hasMarriageYear
  AddTriple (59c02f94-2dda-4e94-8fc9-785bdb5fb281)
 Call ID: 59c02f94-2dda-4e94-8fc9-785bdb5fb281
  Args:
    target: Doon_Aileen_Plunket
    relation: :hasRelation
    source: Granville_James_Leveson-Gower
  AssignClass (85eedecb-7f76-4af6-8165-6f4a2253298a)
 Call ID: 85eedecb-7f76-4af6-8165-6f4a2253298a
  Args:
    type: :Person
    source: Brindsley_Sheridan_Bushe_Plunket
  AssignClass (714408ea-d2fa-4847-b815-30342e44a442)
 Call ID: 714408ea-d2fa-4847-b815-30342e44a442
  Args:
    type: :Man
    source: Brindsley_Sheridan_Bushe_Plunket
  AssignClass (2003d8db-d937-4ed9-9d4e-5b1c364d3f9b)
 Call ID: 2003d8db-d937-4ed9-9d4e-5b1c364d3f9b
  Args:
    type: :Ancestor
    source: Brindsley_Sheridan_Bushe_Plunket
  AddTriple (07571be1-b318-4c7b-82c1-ba447f46a9d9)
 Call ID: 07571be1-b318-4c7b-82c1-ba447f46a9d9
  Args:
    target: Brindsley_Sheridan_Bushe_Plunket
    source: Doon_Aileen_Plunket
    relation: :hasFather
  AssignClass (77c060ec-b706-4333-829e-daebe44bd250)
 Call ID: 77c060ec-b706-4333-829e-daebe44bd250
  Args:
    type: :Person
    source: William_Plunket
  AssignClass (ddd04494-8747-4318-868d-98c7d23f8c97)
 Call ID: ddd04494-8747-4318-868d-98c7d23f8c97
  Args:
    type: :Man
    source: William_Plunket
  AssignClass (56ed0fcc-ed1a-485c-80a3-24545d775477)
 Call ID: 56ed0fcc-ed1a-485c-80a3-24545d775477
  Args:
    type: :Ancestor
    source: William_Plunket
  AddTriple (67732ae0-a4b5-4ece-906c-a426739052ce)
 Call ID: 67732ae0-a4b5-4ece-906c-a426739052ce
  Args:
    target: William_Plunket
    relation: :hasFather
    source: Brindsley_Sheridan_Bushe_Plunket
  AssignClass (e623f782-6d04-4196-99db-a002d7b8e325)
 Call ID: e623f782-6d04-4196-99db-a002d7b8e325
  Args:
    type: :Person
    source: Aileen_Sibell_Mary_Guinness
  AssignClass (b2e6b58e-b399-4d16-b2e4-25b9e459e870)
 Call ID: b2e6b58e-b399-4d16-b2e4-25b9e459e870
  Args:
    type: :Woman
    source: Aileen_Sibell_Mary_Guinness
  AssignClass (5e51b50d-a83b-412b-8b39-c26f2701766f)
 Call ID: 5e51b50d-a83b-412b-8b39-c26f2701766f
  Args:
    type: :Ancestor
    source: Aileen_Sibell_Mary_Guinness
  AddTriple (64a414a6-6d4a-45a5-b4b6-f55ce683a8d7)
 Call ID: 64a414a6-6d4a-45a5-b4b6-f55ce683a8d7
  Args:
    target: Aileen_Sibell_Mary_Guinness
    relation: :hasMother
    source: Doon_Aileen_Plunket
  AssignClass (0fdd3522-0cfe-4adf-833d-3fbaa61530c1)
 Call ID: 0fdd3522-0cfe-4adf-833d-3fbaa61530c1
  Args:
    type: :Person
    source: Edward_Guinness
  AssignClass (d8751281-232b-400f-81fc-63bb7b42b0e7)
 Call ID: d8751281-232b-400f-81fc-63bb7b42b0e7
  Args:
    type: :Man
    source: Edward_Guinness
  AssignClass (49ffe66a-a9d3-42f9-a868-f34f7488f348)
 Call ID: 49ffe66a-a9d3-42f9-a868-f34f7488f348
  Args:
    type: :Ancestor
    source: Edward_Guinness
  AddTriple (ccc03b11-56f3-433b-b32c-542d1e7c164a)
 Call ID: ccc03b11-56f3-433b-b32c-542d1e7c164a
  Args:
    source: Aileen_Sibell_Mary_Guinness
    relation: :hasFather
    target: Edward_Guinness
  Finish (c127273c-31c3-442a-9021-15f66613d23e)
 Call ID: c127273c-31c3-442a-9021-15f66613d23e
  Args: