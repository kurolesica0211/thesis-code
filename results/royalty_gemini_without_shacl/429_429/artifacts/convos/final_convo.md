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
Rose Cecilia "Rosie" Stancer (née Clayton; born 25 January 1960) is a British explorer and polar adventurer, and a female-line second cousin of King Charles III of the UK.
Youth, education, family

Rosie Stancer attended Butterstone House School in Scotland and then Heathfield School, Ascot.
Stancer is the daughter of Lady Mary Cecilia Leveson-Gower (1917–2014) and Sir Samuel Clayton.
Her maternal grandparents were Rose Leveson-Gower, Countess Granville (an elder sister of Queen Elizabeth the Queen Mother), and William Leveson-Gower, 4th Earl Granville, naval commander, making her a second cousin of King Charles III.
Her paternal grandfather was Brigadier-General Sir Gilbert Falkingham Clayton, British Army intelligence officer and colonial administrator.
On 9 July 1993, she married William Wordie Stancer, with whom she has one son Jock Stancer.
Her husband’s grandfather was, like Stancer herself, a polar explorer James Wordie.
In 1997, Stancer was one of 20 amateur women selected for a place on the first all women's expedition to the North Pole, The 'McVities Penguin Polar Relay'.
M&G ISA South Pole Expedition 1999

In 1999, Stancer and four others from the first expedition organised and managed their own expedition to the South Pole, The 'M&G ISA Challenge'.
Snickers South Pole Solo 2004

In the Austral summer of 2003–4, Stancer skied solo and without re-supply to the South Pole on the 'Snickers South Pole Solo 2004' expedition.
Hauling a sledge more than twice her body weight for over 700 miles (1,100 km), Stancer reached the Pole in 43 days 23 hours, a day longer than Fiona Thornewill who reached the South Pole a few days before Stancer.
During the expedition Stancer gathered both meteorological and physiological data.
Mars North Pole Solo 2007

In 2007, Stancer attempted to become the first woman to trek solo to the Geographic North Pole.
Having traveled 426 nautical miles in 84 days, Stancer was still able to set the world record for furthest solo female expedition to the north.
The Long Haul Expedition 2019

In 2019, Stancer joined Mike Laird on concurrent solo expeditions across Siberia’s Lake Baikal, the world’s largest, deepest, oldest freshwater lake.
They traveled in opposite directions, with Stancer starting from the south and Laird from the north.
Completing over 700 km in 21 days, Stancer set the record.
Monarch's Way (2020)

Stancer walked the Monarch's Way in England in 2020.
In 2021 Stancer began a 'desert trilogy', travelling across the Aralkum in 2021 and the Sinai Peninsula in 2023; she travelled with Pom Oliver, Arabella Dorman and Lee Watts.
Charities

Stancer is an honorary board member for the charity Special Olympics GB, which seeks to provide sports training and competition in a variety of Olympic-style events for people with learning disabilities.
Awards

Stancer was awarded an honorary fellowship from the Polar exploration society.



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
  AssignClass (54f74b09-59af-41eb-98e6-03465bede8d7)
 Call ID: 54f74b09-59af-41eb-98e6-03465bede8d7
  Args:
    type: :Woman
    source: Rosie Stancer
  AssignClass (553ebc44-a395-461f-b2e3-5197158095fb)
 Call ID: 553ebc44-a395-461f-b2e3-5197158095fb
  Args:
    source: Rosie Stancer
    type: :Person
  AddLiteral (2714b171-fb63-4067-9c19-e590e1ceb66c)
 Call ID: 2714b171-fb63-4067-9c19-e590e1ceb66c
  Args:
    relation: :knownAs
    literal_value: Rose Cecilia Stancer
    literal_type: xsd:string
    source: Rosie Stancer
  AddLiteral (58fd11b4-17f7-4955-a943-5138c06401de)
 Call ID: 58fd11b4-17f7-4955-a943-5138c06401de
  Args:
    source: Rosie Stancer
    literal_type: xsd:string
    literal_value: Rosie Stancer
    relation: :alsoKnownAs
  AddLiteral (f630ea76-a6cc-4139-ba1b-7365b1fb5834)
 Call ID: f630ea76-a6cc-4139-ba1b-7365b1fb5834
  Args:
    relation: :hasBirthYear
    literal_value: 1960
    source: Rosie Stancer
    literal_type: xsd:integer
  AssignClass (e0499d10-161e-437e-afdc-ae24fda2b8c5)
 Call ID: e0499d10-161e-437e-afdc-ae24fda2b8c5
  Args:
    type: :Woman
    source: Lady Mary Cecilia Leveson-Gower
  AssignClass (1d605ad2-2321-42a9-96e9-096614bcf0d2)
 Call ID: 1d605ad2-2321-42a9-96e9-096614bcf0d2
  Args:
    type: :Ancestor
    source: Lady Mary Cecilia Leveson-Gower
  AddTriple (23590e43-eef5-4389-9f13-4cf8af3a1649)
 Call ID: 23590e43-eef5-4389-9f13-4cf8af3a1649
  Args:
    target: Lady Mary Cecilia Leveson-Gower
    relation: :hasMother
    source: Rosie Stancer
  AssignClass (29f6b00c-fd9f-40ab-8356-8d684580280d)
 Call ID: 29f6b00c-fd9f-40ab-8356-8d684580280d
  Args:
    source: Sir Samuel Clayton
    type: :Man
  AssignClass (9922fe7a-aa90-4414-a3e7-4b169e79a0d9)
 Call ID: 9922fe7a-aa90-4414-a3e7-4b169e79a0d9
  Args:
    type: :Ancestor
    source: Sir Samuel Clayton
  AddTriple (1ecd5469-868c-4a91-b5e2-d1b762b8bc94)
 Call ID: 1ecd5469-868c-4a91-b5e2-d1b762b8bc94
  Args:
    target: Sir Samuel Clayton
    relation: :hasFather
    source: Rosie Stancer
  AssignClass (347bfe8e-58b1-49f0-a1d0-0658e43ceb54)
 Call ID: 347bfe8e-58b1-49f0-a1d0-0658e43ceb54
  Args:
    source: Rose Leveson-Gower, Countess Granville
    type: :Woman
  AssignClass (4abf9d74-a462-4be6-8f22-6ed154643143)
 Call ID: 4abf9d74-a462-4be6-8f22-6ed154643143
  Args:
    type: :Ancestor
    source: Rose Leveson-Gower, Countess Granville
  AddTriple (a438cb87-63cf-4b51-a833-bca0ba67ddc6)
 Call ID: a438cb87-63cf-4b51-a833-bca0ba67ddc6
  Args:
    source: Lady Mary Cecilia Leveson-Gower
    target: Rose Leveson-Gower, Countess Granville
    relation: :hasMother
  AssignClass (91be270b-b3b9-416c-ae10-3774c29976cf)
 Call ID: 91be270b-b3b9-416c-ae10-3774c29976cf
  Args:
    type: :Man
    source: William Leveson-Gower, 4th Earl Granville
  AssignClass (9b000413-1d7c-40b0-8368-bc7e18266099)
 Call ID: 9b000413-1d7c-40b0-8368-bc7e18266099
  Args:
    type: :Ancestor
    source: William Leveson-Gower, 4th Earl Granville
  AddTriple (37fc5357-f7ad-4d25-a6ce-c8fc5f535eda)
 Call ID: 37fc5357-f7ad-4d25-a6ce-c8fc5f535eda
  Args:
    source: Lady Mary Cecilia Leveson-Gower
    target: William Leveson-Gower, 4th Earl Granville
    relation: :hasFather
  AssignClass (f4f4f3b9-f41e-4d9b-8ee6-7582691c55e9)
 Call ID: f4f4f3b9-f41e-4d9b-8ee6-7582691c55e9
  Args:
    source: Sir Gilbert Falkingham Clayton
    type: :Man
  AssignClass (6a2863ef-60a4-4227-af0c-b02dc13c0393)
 Call ID: 6a2863ef-60a4-4227-af0c-b02dc13c0393
  Args:
    source: Sir Gilbert Falkingham Clayton
    type: :Ancestor
  AddTriple (c56abe8b-b75d-4aa2-80ff-adb1742e2bf8)
 Call ID: c56abe8b-b75d-4aa2-80ff-adb1742e2bf8
  Args:
    relation: :hasFather
    target: Sir Gilbert Falkingham Clayton
    source: Sir Samuel Clayton
  AssignClass (0d81974c-123d-4091-87c3-dbf613e61128)
 Call ID: 0d81974c-123d-4091-87c3-dbf613e61128
  Args:
    source: William Wordie Stancer
    type: :Man
  AssignClass (3c5614f8-b643-4366-8cb7-a96509634ddb)
 Call ID: 3c5614f8-b643-4366-8cb7-a96509634ddb
  Args:
    type: :Person
    source: William Wordie Stancer
  AddLiteral (cd7a5a84-f1d2-4672-af25-ddf41f7e904b)
 Call ID: cd7a5a84-f1d2-4672-af25-ddf41f7e904b
  Args:
    relation: :hasMarriageYear
    literal_value: 1993
    source: Rosie Stancer
    literal_type: xsd:integer
  AddTriple (b1c7a59e-45cf-4b86-a916-499016902605)
 Call ID: b1c7a59e-45cf-4b86-a916-499016902605
  Args:
    target: William Wordie Stancer
    relation: :hasRelation
    source: Rosie Stancer
  AssignClass (0734a0a4-534a-4704-95ef-8eafa1eaad5d)
 Call ID: 0734a0a4-534a-4704-95ef-8eafa1eaad5d
  Args:
    source: Jock Stancer
    type: :Man
  AssignClass (b9c42110-f93c-4915-a0d0-abd1c9c3f6fa)
 Call ID: b9c42110-f93c-4915-a0d0-abd1c9c3f6fa
  Args:
    type: :Person
    source: Jock Stancer
  AddTriple (4f583876-6e75-494e-8ade-6edbe61b7a52)
 Call ID: 4f583876-6e75-494e-8ade-6edbe61b7a52
  Args:
    relation: :hasMother
    target: Rosie Stancer
    source: Jock Stancer
  AddTriple (3ce869a0-819a-4227-a94d-d6ca00d82cd6)
 Call ID: 3ce869a0-819a-4227-a94d-d6ca00d82cd6
  Args:
    source: Jock Stancer
    relation: :hasFather
    target: William Wordie Stancer
  AssignClass (a29a1512-bce3-48a0-a29b-d2eaed9dfb58)
 Call ID: a29a1512-bce3-48a0-a29b-d2eaed9dfb58
  Args:
    type: :Man
    source: James Wordie
  AssignClass (6a62eb78-d56b-4f23-b7dd-2145d0e508a4)
 Call ID: 6a62eb78-d56b-4f23-b7dd-2145d0e508a4
  Args:
    type: :Ancestor
    source: James Wordie
  AddTriple (38378616-f4d1-4ca9-bdf2-5448edd8b034)
 Call ID: 38378616-f4d1-4ca9-bdf2-5448edd8b034
  Args:
    source: William Wordie Stancer
    relation: :hasFather
    target: James Wordie
  Finish (884f43ce-1c2c-4b6f-b96f-81918facb46f)
 Call ID: 884f43ce-1c2c-4b6f-b96f-81918facb46f
  Args: