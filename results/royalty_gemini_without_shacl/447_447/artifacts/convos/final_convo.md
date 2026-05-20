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
John Ulick Knatchbull, 7th Baron Brabourne, CBE (9 November 1924 – 23 September 2005), professionally known as John Brabourne, was a British peer, television producer and Oscar-nominated film producer.
Married to the elder daughter of 1st Earl Mountbatten, Brabourne was a survivor of the bombing which killed his father-in-law, mother and son.
Biography

Brabourne was born in 1924, the second son of Michael Knatchbull, 5th Baron Brabourne, and his wife, Lady Doreen Browne.
Marriage

At the end of the war, Brabourne returned to England and settled in the family seat, Mersham in Kent.
On 26 October 1946, at Romsey Abbey in Hampshire, at the age of 21, he married Patricia Mountbatten, elder daughter of Louis Mountbatten, 1st Viscount Mountbatten, later 1st
Earl Mountbatten of Burma.
Brabourne's best man at the wedding was Squadron Leader Charles Harris-St. John.
Lady Brabourne was to inherit her father's peerages in due course.
This would make Lord and Lady Brabourne among the few married couples to each hold peerages in their own right.
Also, Lady Brabourne was related to the British royal family, and her aunt Louise Mountbatten was at that time the Crown Princess (later Queen) of Sweden.
In February 1947, only months after the wedding, Brabourne's father-in-law was appointed Viceroy of India.
The newly-wed couple spent several months in India, residing with her parents in the viceregal palace.
In November the same year, Lady Brabourne's first cousin Philip, Duke of Edinburgh, wed Princess Elizabeth, future queen of the United Kingdom.
Lord and Lady Brabourne had eight children, including Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), Lady Amanda Patricia Victoria Knatchbull (born 26 June 1957), and Nicholas Timothy Charles Knatchbull.
Career and service

In the late 1940s, shortly after leaving the army, Brabourne began working as an assistant production manager for certain television productions, mostly based on war-related themes.
John Brabourne received two Academy Award nominations for Best Picture, as producer of Romeo and Juliet (1968) and A Passage to India (1984).
In 1985, Brabourne was invested as a Fellow of the British Film Institute, an organisation he also served as a Governor.
He was the subject of This Is Your Life in 1990 when he was surprised by Michael Aspel at the Old Brewery venue in London.
Brabourne served as a governor of various schools, including Norton Knatchbull School (founded by an ancestor c. 1630 AD) from 1947 to 2000; Wye College in Kent from 1955 to 2000, and Gordonstoun School from 1964 to 1994.
IRA bombing

On 27 August 1979, while the family was on holiday in Mullaghmore, County Sligo, Lord Brabourne's father-in-law, Earl Mountbatten of Burma, took a number of family members out lobstering on his motorboat, Shadow V, in Donegal Bay.
Having planned to murder Mountbatten, the Irish Republican Army (IRA) placed a bomb inside the boat on the night of the 26th.
Mountbatten and several members of the party were killed the next morning when the bomb was triggered by an IRA observer onshore who was armed with a radio detonator.
The dead included Brabourne's 83-year-old mother, the Dowager Baroness Brabourne; one of his twin 14-year-old sons, Nicholas Knatchbull; and 15-year-old Paul Maxwell from County Fermanagh who had been hired for the summer as Mountbatten's boat boy.
Brabourne, his wife Patricia, and their other twin son Timothy were severely injured, but survived the attack.
Lord Brabourne died on 23 September 2005 at his home in Kent, aged 80.
His wife Patricia, Countess Mountbatten of Burma, died in June 2017.



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
  AssignClass (e756837e-3422-45c7-b053-2cec56e40c84)
 Call ID: e756837e-3422-45c7-b053-2cec56e40c84
  Args:
    type: :Man
    source: John_Ulick_Knatchbull
  AssignClass (f593edac-dcbd-49aa-bd72-a0e81e0cf178)
 Call ID: f593edac-dcbd-49aa-bd72-a0e81e0cf178
  Args:
    type: :Person
    source: John_Ulick_Knatchbull
  AddLiteral (f2f1905d-b143-49cc-9bb9-06a8bbfee379)
 Call ID: f2f1905d-b143-49cc-9bb9-06a8bbfee379
  Args:
    source: John_Ulick_Knatchbull
    relation: :knownAs
    literal_value: John Brabourne
    literal_type: xsd:string
  AddLiteral (62e2f298-e95c-4943-94f6-e6bf8d8f7bfa)
 Call ID: 62e2f298-e95c-4943-94f6-e6bf8d8f7bfa
  Args:
    literal_value: 1924
    literal_type: xsd:integer
    source: John_Ulick_Knatchbull
    relation: :hasBirthYear
  AddLiteral (ec03492a-9bf7-41c5-9a23-7d615d1530a3)
 Call ID: ec03492a-9bf7-41c5-9a23-7d615d1530a3
  Args:
    relation: :hasDeathYear
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    literal_value: 2005
  AssignClass (8ea16832-6771-4bbd-9a10-16564efff6a0)
 Call ID: 8ea16832-6771-4bbd-9a10-16564efff6a0
  Args:
    source: Michael_Knatchbull
    type: :Man
  AssignClass (a90cef00-3eb4-4cf0-9157-bf04524887a0)
 Call ID: a90cef00-3eb4-4cf0-9157-bf04524887a0
  Args:
    type: :Person
    source: Michael_Knatchbull
  AddTriple (e5a07c22-3613-41d8-90e1-52220e16397c)
 Call ID: e5a07c22-3613-41d8-90e1-52220e16397c
  Args:
    source: John_Ulick_Knatchbull
    relation: :hasFather
    target: Michael_Knatchbull
  AssignClass (c663591a-a5a7-47fc-a093-598cf69b7553)
 Call ID: c663591a-a5a7-47fc-a093-598cf69b7553
  Args:
    source: Lady_Doreen_Browne
    type: :Woman
  AssignClass (d6954653-ef41-4b35-b07c-caaeda1c58b3)
 Call ID: d6954653-ef41-4b35-b07c-caaeda1c58b3
  Args:
    source: Lady_Doreen_Browne
    type: :Person
  AddTriple (c438cc80-4665-4cd3-9b61-9847dadb745c)
 Call ID: c438cc80-4665-4cd3-9b61-9847dadb745c
  Args:
    relation: :hasMother
    target: Lady_Doreen_Browne
    source: John_Ulick_Knatchbull
  AssignClass (3cac6644-1593-4450-95a3-2f64f942b5db)
 Call ID: 3cac6644-1593-4450-95a3-2f64f942b5db
  Args:
    source: Patricia_Mountbatten
    type: :Woman
  AssignClass (a5a62096-bfc0-449d-8d58-6684d7b4b6d4)
 Call ID: a5a62096-bfc0-449d-8d58-6684d7b4b6d4
  Args:
    source: Patricia_Mountbatten
    type: :Person
  AddLiteral (51953c85-b3f7-4357-a7e8-25e4530644a7)
 Call ID: 51953c85-b3f7-4357-a7e8-25e4530644a7
  Args:
    source: John_Ulick_Knatchbull
    relation: :hasMarriageYear
    literal_value: 1946
    literal_type: xsd:integer
  AddTriple (570cb03c-c9be-4eb6-8b2f-1435f01b5e6d)
 Call ID: 570cb03c-c9be-4eb6-8b2f-1435f01b5e6d
  Args:
    relation: :hasRelation
    target: Patricia_Mountbatten
    source: John_Ulick_Knatchbull
  AssignClass (4dbb53fc-3cb7-4dcf-8ab9-0f9e4f3eee1d)
 Call ID: 4dbb53fc-3cb7-4dcf-8ab9-0f9e4f3eee1d
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (115ac288-e700-4a9c-8e63-ebdd9c609160)
 Call ID: 115ac288-e700-4a9c-8e63-ebdd9c609160
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (8ea964e3-1da2-49c9-aeb6-1da95a801389)
 Call ID: 8ea964e3-1da2-49c9-aeb6-1da95a801389
  Args:
    source: Patricia_Mountbatten
    target: Louis_Mountbatten
    relation: :hasFather
  AssignClass (184eaee9-6ea2-4ec6-995e-b96f8cfeedfe)
 Call ID: 184eaee9-6ea2-4ec6-995e-b96f8cfeedfe
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (ee05000c-38d6-4461-8823-3a50af28b545)
 Call ID: ee05000c-38d6-4461-8823-3a50af28b545
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Person
  AddTriple (87da6498-30ad-4978-a9f2-821c09163667)
 Call ID: 87da6498-30ad-4978-a9f2-821c09163667
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasFather
    target: John_Ulick_Knatchbull
  AddTriple (1d2aaa8b-bb6a-458e-bbe8-41bb5af8526f)
 Call ID: 1d2aaa8b-bb6a-458e-bbe8-41bb5af8526f
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMother
    target: Patricia_Mountbatten
  AssignClass (3beb94cc-2b72-49e7-a0b7-bb34af90ed98)
 Call ID: 3beb94cc-2b72-49e7-a0b7-bb34af90ed98
  Args:
    type: :Woman
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (51011138-4f88-4d2a-ae07-9f914d7f7c15)
 Call ID: 51011138-4f88-4d2a-ae07-9f914d7f7c15
  Args:
    type: :Person
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (fe5666c8-9b09-486c-980d-159ba27c1769)
 Call ID: fe5666c8-9b09-486c-980d-159ba27c1769
  Args:
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    relation: :hasFather
    target: John_Ulick_Knatchbull
  AddTriple (8c05d3b7-998a-4120-aa29-ffaf17760e32)
 Call ID: 8c05d3b7-998a-4120-aa29-ffaf17760e32
  Args:
    target: Patricia_Mountbatten
    relation: :hasMother
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (e6e4e28d-3074-4251-8f1b-38adcdca1341)
 Call ID: e6e4e28d-3074-4251-8f1b-38adcdca1341
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    type: :Man
  AssignClass (556563e7-313d-4cbd-90d0-d18b70940a00)
 Call ID: 556563e7-313d-4cbd-90d0-d18b70940a00
  Args:
    type: :Person
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (e0d770b6-8699-49ed-89be-4a09b98fb8d9)
 Call ID: e0d770b6-8699-49ed-89be-4a09b98fb8d9
  Args:
    target: John_Ulick_Knatchbull
    relation: :hasFather
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (7c10b26b-d21b-40a8-bbea-f418112477ff)
 Call ID: 7c10b26b-d21b-40a8-bbea-f418112477ff
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    target: Patricia_Mountbatten
    relation: :hasMother
  AssignClass (442f87dd-b3b8-4d51-a9e6-7170de38a804)
 Call ID: 442f87dd-b3b8-4d51-a9e6-7170de38a804
  Args:
    type: :Man
    source: Timothy_Knatchbull
  AssignClass (f6afd2a5-ee8a-4234-9774-1944fb021105)
 Call ID: f6afd2a5-ee8a-4234-9774-1944fb021105
  Args:
    source: Timothy_Knatchbull
    type: :Person
  AddTriple (bcce01fc-e64d-43f4-899f-414844a17333)
 Call ID: bcce01fc-e64d-43f4-899f-414844a17333
  Args:
    source: Timothy_Knatchbull
    target: John_Ulick_Knatchbull
    relation: :hasFather
  AddTriple (be2f5472-b876-4995-be1a-78706370b302)
 Call ID: be2f5472-b876-4995-be1a-78706370b302
  Args:
    target: Patricia_Mountbatten
    relation: :hasMother
    source: Timothy_Knatchbull
  Finish (7a8e4e1f-d1c5-4996-ba89-7edd63f23c14)
 Call ID: 7a8e4e1f-d1c5-4996-ba89-7edd63f23c14
  Args: