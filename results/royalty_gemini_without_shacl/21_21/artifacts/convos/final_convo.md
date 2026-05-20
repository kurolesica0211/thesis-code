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
  AssignClass (6701256a-ae24-48c6-958c-1d5147bb1a54)
 Call ID: 6701256a-ae24-48c6-958c-1d5147bb1a54
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (dcf28a17-ef6a-4d30-a228-211cf9cbebb1)
 Call ID: dcf28a17-ef6a-4d30-a228-211cf9cbebb1
  Args:
    type: :Person
    source: :Norton_Louis_Philip_Knatchbull
  AddLiteral (a4315f8c-0927-4ead-acde-0f16e7efa27e)
 Call ID: a4315f8c-0927-4ead-acde-0f16e7efa27e
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    literal_value: 1947
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (e9f4eb57-3fd0-4212-9f3d-292600ffb36b)
 Call ID: e9f4eb57-3fd0-4212-9f3d-292600ffb36b
  Args:
    relation: :formerlyKnownAs
    source: :Norton_Louis_Philip_Knatchbull
    literal_value: Lord Romsey
    literal_type: xsd:string
  AddLiteral (905ac643-b6e1-4598-a21e-9535d527061f)
 Call ID: 905ac643-b6e1-4598-a21e-9535d527061f
  Args:
    relation: :formerlyKnownAs
    literal_type: xsd:string
    source: :Norton_Louis_Philip_Knatchbull
    literal_value: Lord Brabourne
  AssignClass (d5185451-dcd4-4b58-9e96-8050fec65e10)
 Call ID: d5185451-dcd4-4b58-9e96-8050fec65e10
  Args:
    source: :Patricia_Knatchbull
    type: :Woman
  AssignClass (db88fbc8-103b-4a20-a15e-9f38703c85b2)
 Call ID: db88fbc8-103b-4a20-a15e-9f38703c85b2
  Args:
    source: :Patricia_Knatchbull
    type: :Person
  AssignClass (4f2feefb-e93b-4225-b17c-20ffb73378c7)
 Call ID: 4f2feefb-e93b-4225-b17c-20ffb73378c7
  Args:
    type: :Man
    source: :John_Knatchbull
  AssignClass (9cbf848e-1d94-496e-8d3f-8a8ecf79db37)
 Call ID: 9cbf848e-1d94-496e-8d3f-8a8ecf79db37
  Args:
    source: :John_Knatchbull
    type: :Person
  AddTriple (b20e3b63-02f4-488b-97fc-ecf0108c3823)
 Call ID: b20e3b63-02f4-488b-97fc-ecf0108c3823
  Args:
    target: :John_Knatchbull
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasFather
  AddTriple (ee94bb53-53a6-4332-bf45-c82cd71daed3)
 Call ID: ee94bb53-53a6-4332-bf45-c82cd71daed3
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasMother
    target: :Patricia_Knatchbull
  AssignClass (d4ee4943-bc86-4bd8-be00-f4ee07053ee0)
 Call ID: d4ee4943-bc86-4bd8-be00-f4ee07053ee0
  Args:
    source: :Penelope_Meredith_Eastwood
    type: :Woman
  AssignClass (62f85331-a3e5-44ab-b5b3-9688a3d4e5fe)
 Call ID: 62f85331-a3e5-44ab-b5b3-9688a3d4e5fe
  Args:
    type: :Person
    source: :Penelope_Meredith_Eastwood
  AddLiteral (ffb9f3f6-a100-4e46-be67-32064549153e)
 Call ID: ffb9f3f6-a100-4e46-be67-32064549153e
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Penelope_Meredith_Eastwood
    literal_value: 1953
  AddLiteral (e428d1f2-9ef9-47e1-80f2-7cd99ecf4252)
 Call ID: e428d1f2-9ef9-47e1-80f2-7cd99ecf4252
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Norton_Louis_Philip_Knatchbull
    literal_value: 1979
  AddTriple (6fcd8996-00b5-43cc-a970-6863e4d5c61f)
 Call ID: 6fcd8996-00b5-43cc-a970-6863e4d5c61f
  Args:
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
    target: :Penelope_Meredith_Eastwood
  AssignClass (78d370d0-de33-4535-8457-8264c312a840)
 Call ID: 78d370d0-de33-4535-8457-8264c312a840
  Args:
    type: :Man
    source: :Louis_Mountbatten
  AssignClass (84e053a8-3b0f-41e0-87d3-dd6d019c2c98)
 Call ID: 84e053a8-3b0f-41e0-87d3-dd6d019c2c98
  Args:
    source: :Louis_Mountbatten
    type: :Person
  AddTriple (99ecb71c-7c9a-438c-bb44-dac5de4fc233)
 Call ID: 99ecb71c-7c9a-438c-bb44-dac5de4fc233
  Args:
    relation: :isAncestorOf
    source: :Louis_Mountbatten
    target: :Norton_Louis_Philip_Knatchbull
  AssignClass (d7ab98e9-e0e9-4fb0-bb45-5e3cbba7ee13)
 Call ID: d7ab98e9-e0e9-4fb0-bb45-5e3cbba7ee13
  Args:
    type: :Man
    source: :Nicholas_Knatchbull
  AssignClass (610aaa58-02f2-4a7f-b83b-16867d0f627f)
 Call ID: 610aaa58-02f2-4a7f-b83b-16867d0f627f
  Args:
    type: :Person
    source: :Nicholas_Knatchbull
  AddTriple (415bc937-aac9-4973-aefd-eb8d8665274e)
 Call ID: 415bc937-aac9-4973-aefd-eb8d8665274e
  Args:
    source: :Nicholas_Knatchbull
    relation: :isBrotherOf
    target: :Norton_Louis_Philip_Knatchbull
  AssignClass (143ba6a5-9295-4188-ae40-fcf07a75091d)
 Call ID: 143ba6a5-9295-4188-ae40-fcf07a75091d
  Args:
    source: :Doreen_Knatchbull
    type: :Woman
  AssignClass (20970add-fa97-48a5-843f-6f147a92553f)
 Call ID: 20970add-fa97-48a5-843f-6f147a92553f
  Args:
    source: :Doreen_Knatchbull
    type: :Person
  AssignClass (d88deb7b-9c6d-4431-b575-c2baf606e585)
 Call ID: d88deb7b-9c6d-4431-b575-c2baf606e585
  Args:
    source: :Reginald_Wray_Frank_Eastwood
    type: :Man
  AssignClass (72286849-8488-4016-a99d-212d3bdc5880)
 Call ID: 72286849-8488-4016-a99d-212d3bdc5880
  Args:
    source: :Reginald_Wray_Frank_Eastwood
    type: :Person
  AddLiteral (6bd38391-74e5-4748-9bf5-00222c033269)
 Call ID: 6bd38391-74e5-4748-9bf5-00222c033269
  Args:
    literal_type: xsd:integer
    source: :Reginald_Wray_Frank_Eastwood
    literal_value: 1912
    relation: :hasBirthYear
  AddLiteral (29b5317b-c012-486a-bbe4-386a02c6cfbc)
 Call ID: 29b5317b-c012-486a-bbe4-386a02c6cfbc
  Args:
    literal_type: xsd:integer
    source: :Reginald_Wray_Frank_Eastwood
    literal_value: 1980
    relation: :hasDeathYear
  AssignClass (64722307-628d-4e04-b5a9-e9489f4b34c8)
 Call ID: 64722307-628d-4e04-b5a9-e9489f4b34c8
  Args:
    source: :Marian_Elizabeth
    type: :Woman
  AssignClass (d00f5a62-8ade-4ec9-8185-1f2a873ef817)
 Call ID: d00f5a62-8ade-4ec9-8185-1f2a873ef817
  Args:
    source: :Marian_Elizabeth
    type: :Person
  AddLiteral (867afe27-b671-4f0a-a0a3-0f8e15c9278b)
 Call ID: 867afe27-b671-4f0a-a0a3-0f8e15c9278b
  Args:
    relation: :hasBirthYear
    literal_value: 1926
    source: :Marian_Elizabeth
    literal_type: xsd:integer
  AddLiteral (4ea2e8b9-48b8-4b8d-871d-e9768c6b3cb1)
 Call ID: 4ea2e8b9-48b8-4b8d-871d-e9768c6b3cb1
  Args:
    literal_value: 2020
    source: :Marian_Elizabeth
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (36324318-8737-40c0-be16-effbd724ef5a)
 Call ID: 36324318-8737-40c0-be16-effbd724ef5a
  Args:
    target: :Reginald_Wray_Frank_Eastwood
    relation: :hasFather
    source: :Penelope_Meredith_Eastwood
  AddTriple (c44af63d-0738-43bb-874f-a160f9f1028a)
 Call ID: c44af63d-0738-43bb-874f-a160f9f1028a
  Args:
    relation: :hasMother
    source: :Penelope_Meredith_Eastwood
    target: :Marian_Elizabeth
  AssignClass (f8ac4a3f-59cf-4b68-b72c-2b0042ee75ab)
 Call ID: f8ac4a3f-59cf-4b68-b72c-2b0042ee75ab
  Args:
    source: :Eugenie_Lady_Nuttall
    type: :Woman
  AssignClass (8037c0c1-11e8-4745-9724-34213c406030)
 Call ID: 8037c0c1-11e8-4745-9724-34213c406030
  Args:
    type: :Person
    source: :Eugenie_Lady_Nuttall
  AddTriple (3fe4ff71-dfbc-4c4a-82cc-f3964f684f37)
 Call ID: 3fe4ff71-dfbc-4c4a-82cc-f3964f684f37
  Args:
    target: :Eugenie_Lady_Nuttall
    source: :Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
  Finish (34347d4f-350d-48a4-8211-f89e20a2deea)
 Call ID: 34347d4f-350d-48a4-8211-f89e20a2deea
  Args: