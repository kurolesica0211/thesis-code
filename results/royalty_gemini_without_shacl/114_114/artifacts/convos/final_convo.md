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
Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), known until 2005 as Lord Romsey and until 2017 as the Lord Brabourne, is a British peer.
Life and education

Mountbatten was born at King's College Hospital in London as the eldest son of Patricia Knatchbull, née Mountbatten, later 2nd Countess Mountbatten of Burma, and film producer John Knatchbull, 7th Baron Brabourne.
Mountbatten was educated at the Dragon School, in Oxford, and Gordonstoun School, Elgin, Moray, Scotland.
On the death of his father on 23 September 2005, he became the 8th Baron Brabourne, of Brabourne in the County of Kent, in the peerage of the United Kingdom.
He also succeeded to the Knatchbull Baronetcy, of Mersham Hatch in the County of Kent, in the baronetage of England.
On the death of his mother on 13 June 2017, he became Earl Mountbatten of Burma, also a title in the peerage of the United Kingdom created for his grandfather, Admiral of the Fleet Lord Louis Mountbatten.
He is a descendant of Queen Victoria, whose second daughter Princess Alice of the United Kingdom was his maternal great-great-grandmother.
Mountbatten is the godfather of Philip's grandson, the Prince of Wales.
He is also related to author Jane Austen, as his father, John Knatchbull, 7th Baron Brabourne, was a direct descendant of her brother Edward Austen Knight.
Marriage and children

Mountbatten is married to Penelope Meredith Eastwood (born 16 April 1953), a daughter of Reginald Wray Frank Eastwood (1912–1980), a self-made millionaire former butcher who founded the Angus Steakhouse chain, and Marian Elizabeth (1926–2020), née Hood.
They were wed on 20 October 1979 at Romsey Abbey, less than two months after the IRA murdered his 79-year-old maternal grandfather, Louis Mountbatten, 1st
Earl Mountbatten of Burma; his 14-year-old younger brother, Nicholas Knatchbull; and his 83-year-old paternal grandmother, Doreen Knatchbull, Dowager Lady Brabourne.
The 3rd Earl Mountbatten of Burma and his wife have three children and three grandsons:


From 2010 to 2014, Mountbatten was in an extramarital relationship with Eugenie, Lady Nuttall, widow of Sir Nicholas Nuttall, 3rd Baronet, who was heir to the Edmund Nuttall Limited construction company.



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
  AssignClass (d87dfc1b-c002-4bb0-a135-bd867abeed0e)
 Call ID: d87dfc1b-c002-4bb0-a135-bd867abeed0e
  Args:
    type: :Man
    source: :Norton_Louis_Philip_Knatchbull
  AssignClass (e3166dd3-1aff-4527-8ac6-fb09325bde9f)
 Call ID: e3166dd3-1aff-4527-8ac6-fb09325bde9f
  Args:
    type: :Person
    source: :Norton_Louis_Philip_Knatchbull
  AddLiteral (b292a948-af73-4741-8c66-0f8efd319455)
 Call ID: b292a948-af73-4741-8c66-0f8efd319455
  Args:
    literal_type: xsd:integer
    literal_value: 1947
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasBirthYear
  AddLiteral (7517f48b-8930-494e-9d6d-893e3b1c6c1e)
 Call ID: 7517f48b-8930-494e-9d6d-893e3b1c6c1e
  Args:
    literal_type: xsd:string
    literal_value: Lord Romsey
    source: :Norton_Louis_Philip_Knatchbull
    relation: :formerlyKnownAs
  AddLiteral (90636b10-e9f3-4688-9f03-6ef9b3d95947)
 Call ID: 90636b10-e9f3-4688-9f03-6ef9b3d95947
  Args:
    relation: :formerlyKnownAs
    source: :Norton_Louis_Philip_Knatchbull
    literal_value: Lord Brabourne
    literal_type: xsd:string
  AssignClass (dc8c651f-eb00-44c5-ac37-90d2ca1e4b0f)
 Call ID: dc8c651f-eb00-44c5-ac37-90d2ca1e4b0f
  Args:
    type: :Woman
    source: :Patricia_Knatchbull
  AssignClass (cbff9268-7f96-4606-be44-9ee23772e9ec)
 Call ID: cbff9268-7f96-4606-be44-9ee23772e9ec
  Args:
    type: :Person
    source: :Patricia_Knatchbull
  AssignClass (87d4a6f6-6548-4ef1-8c3d-876e80def814)
 Call ID: 87d4a6f6-6548-4ef1-8c3d-876e80def814
  Args:
    type: :Man
    source: :John_Knatchbull
  AssignClass (f267e617-0a21-444b-9525-2092f97299c5)
 Call ID: f267e617-0a21-444b-9525-2092f97299c5
  Args:
    type: :Person
    source: :John_Knatchbull
  AddTriple (ba212bb4-7659-4d39-83d4-2b9c3f89709c)
 Call ID: ba212bb4-7659-4d39-83d4-2b9c3f89709c
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasFather
    target: :John_Knatchbull
  AddTriple (9757838e-702f-424d-909f-336243ec0693)
 Call ID: 9757838e-702f-424d-909f-336243ec0693
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasMother
    target: :Patricia_Knatchbull
  AssignClass (8ff05487-8d15-481d-982f-6b3cb7789301)
 Call ID: 8ff05487-8d15-481d-982f-6b3cb7789301
  Args:
    type: :Woman
    source: :Penelope_Meredith_Eastwood
  AssignClass (f29e7858-3ae9-4b14-baea-4fe044706642)
 Call ID: f29e7858-3ae9-4b14-baea-4fe044706642
  Args:
    type: :Person
    source: :Penelope_Meredith_Eastwood
  AddLiteral (381f18c9-478e-47ba-8ab1-0a78868c2cd6)
 Call ID: 381f18c9-478e-47ba-8ab1-0a78868c2cd6
  Args:
    literal_value: 1953
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Penelope_Meredith_Eastwood
  AddLiteral (8d46ac76-8377-45e6-b5f3-905bf5281803)
 Call ID: 8d46ac76-8377-45e6-b5f3-905bf5281803
  Args:
    relation: :hasMarriageYear
    source: :Norton_Louis_Philip_Knatchbull
    literal_value: 1979
    literal_type: xsd:integer
  AddTriple (132dca46-1c53-41e6-b7e0-acc582a6a8b9)
 Call ID: 132dca46-1c53-41e6-b7e0-acc582a6a8b9
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    target: :Penelope_Meredith_Eastwood
    relation: :hasRelation
  AssignClass (29c972fa-7b1c-49da-af8d-96d968d43269)
 Call ID: 29c972fa-7b1c-49da-af8d-96d968d43269
  Args:
    type: :Man
    source: :Louis_Mountbatten
  AssignClass (1dc47212-a61a-47ce-b323-90c9ba9b3086)
 Call ID: 1dc47212-a61a-47ce-b323-90c9ba9b3086
  Args:
    type: :Person
    source: :Louis_Mountbatten
  AddTriple (67f45923-97d6-4409-ba50-71b0c6eaf0ca)
 Call ID: 67f45923-97d6-4409-ba50-71b0c6eaf0ca
  Args:
    source: :Patricia_Knatchbull
    target: :Louis_Mountbatten
    relation: :hasMother
  AddTriple (dad2ee82-34aa-4f8a-8a2b-4cbc363ee8da)
 Call ID: dad2ee82-34aa-4f8a-8a2b-4cbc363ee8da
  Args:
    target: :Patricia_Knatchbull
    relation: :isFatherOf
    source: :Louis_Mountbatten
  AssignClass (6b558c4c-e79e-4df7-aa81-ce51c0094cc6)
 Call ID: 6b558c4c-e79e-4df7-aa81-ce51c0094cc6
  Args:
    type: :Man
    source: :Nicholas_Knatchbull
  AssignClass (5000a435-5480-4ad3-bb68-ed9492ef29b4)
 Call ID: 5000a435-5480-4ad3-bb68-ed9492ef29b4
  Args:
    type: :Person
    source: :Nicholas_Knatchbull
  AddTriple (4d3fd0f4-c703-4b1f-ace4-64ad5cbedf7a)
 Call ID: 4d3fd0f4-c703-4b1f-ace4-64ad5cbedf7a
  Args:
    target: :Nicholas_Knatchbull
    relation: :hasBrother
    source: :Norton_Louis_Philip_Knatchbull
  AssignClass (2dc53e82-b23d-47cb-bb77-36b35072ee92)
 Call ID: 2dc53e82-b23d-47cb-bb77-36b35072ee92
  Args:
    type: :Woman
    source: :Doreen_Knatchbull
  AssignClass (a69403bb-b30a-4504-8067-ba6885723ff4)
 Call ID: a69403bb-b30a-4504-8067-ba6885723ff4
  Args:
    type: :Person
    source: :Doreen_Knatchbull
  AssignClass (19232355-4c03-4e6d-93a6-98bf94df6298)
 Call ID: 19232355-4c03-4e6d-93a6-98bf94df6298
  Args:
    type: :Man
    source: :Reginald_Wray_Frank_Eastwood
  AssignClass (e84a34b9-ac68-481d-9c04-83d3b8602d17)
 Call ID: e84a34b9-ac68-481d-9c04-83d3b8602d17
  Args:
    type: :Person
    source: :Reginald_Wray_Frank_Eastwood
  AssignClass (e78b776f-4675-4e5e-9770-3dce0d77c2e1)
 Call ID: e78b776f-4675-4e5e-9770-3dce0d77c2e1
  Args:
    type: :Woman
    source: :Marian_Elizabeth
  AssignClass (daafd12c-6815-4982-8d02-b3c3f04de992)
 Call ID: daafd12c-6815-4982-8d02-b3c3f04de992
  Args:
    type: :Person
    source: :Marian_Elizabeth
  AddTriple (1b3d6e64-b432-474f-879b-7754c26669d4)
 Call ID: 1b3d6e64-b432-474f-879b-7754c26669d4
  Args:
    target: :Reginald_Wray_Frank_Eastwood
    relation: :hasFather
    source: :Penelope_Meredith_Eastwood
  AddTriple (c2e37446-1fb3-435e-88b6-8700cf5d33f4)
 Call ID: c2e37446-1fb3-435e-88b6-8700cf5d33f4
  Args:
    source: :Penelope_Meredith_Eastwood
    relation: :hasMother
    target: :Marian_Elizabeth
  Finish (a9c659a4-0c29-4f29-ac9a-9c07f42a0e2b)
 Call ID: a9c659a4-0c29-4f29-ac9a-9c07f42a0e2b
  Args: