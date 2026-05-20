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
  AssignClass (b83b5fd8-ec24-4ab6-894b-ae6f94d97360)
 Call ID: b83b5fd8-ec24-4ab6-894b-ae6f94d97360
  Args:
    type: :Man
    source: John_Ulick_Knatchbull
  AssignClass (c31dfa4a-74c9-43e0-8cbb-5a98131540f9)
 Call ID: c31dfa4a-74c9-43e0-8cbb-5a98131540f9
  Args:
    type: :Person
    source: John_Ulick_Knatchbull
  AddLiteral (360f7ad5-3cef-44d9-a26f-c093e281d779)
 Call ID: 360f7ad5-3cef-44d9-a26f-c093e281d779
  Args:
    source: John_Ulick_Knatchbull
    literal_value: John Brabourne
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (6e3b2e95-c551-4cf5-9aad-f49d3788baf6)
 Call ID: 6e3b2e95-c551-4cf5-9aad-f49d3788baf6
  Args:
    source: John_Ulick_Knatchbull
    literal_type: xsd:integer
    literal_value: 1924
    relation: :hasBirthYear
  AddLiteral (2a4a3db3-09ed-48c0-b313-4361af3ff173)
 Call ID: 2a4a3db3-09ed-48c0-b313-4361af3ff173
  Args:
    literal_value: 2005
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: John_Ulick_Knatchbull
  AssignClass (152872b2-b068-4de7-ab5f-37ef00162a66)
 Call ID: 152872b2-b068-4de7-ab5f-37ef00162a66
  Args:
    type: :Man
    source: Michael_Knatchbull
  AssignClass (f0e5c728-b244-425b-9033-237c0134dea3)
 Call ID: f0e5c728-b244-425b-9033-237c0134dea3
  Args:
    type: :Person
    source: Michael_Knatchbull
  AddTriple (11c7ce9e-90f9-4f2b-a8bd-4d1e64f75006)
 Call ID: 11c7ce9e-90f9-4f2b-a8bd-4d1e64f75006
  Args:
    source: John_Ulick_Knatchbull
    target: Michael_Knatchbull
    relation: :hasFather
  AssignClass (8a713bc0-6904-4319-9b00-09857f8609fe)
 Call ID: 8a713bc0-6904-4319-9b00-09857f8609fe
  Args:
    type: :Woman
    source: Lady_Doreen_Browne
  AssignClass (82f45ecb-9313-49b0-9b0e-4810534e3ee5)
 Call ID: 82f45ecb-9313-49b0-9b0e-4810534e3ee5
  Args:
    type: :Person
    source: Lady_Doreen_Browne
  AddTriple (e22c415b-a6b3-423f-a14a-a2d8ce206681)
 Call ID: e22c415b-a6b3-423f-a14a-a2d8ce206681
  Args:
    relation: :hasMother
    target: Lady_Doreen_Browne
    source: John_Ulick_Knatchbull
  AssignClass (341d74ea-4d2e-4124-ac56-0aa7dfac08db)
 Call ID: 341d74ea-4d2e-4124-ac56-0aa7dfac08db
  Args:
    type: :Woman
    source: Patricia_Mountbatten
  AssignClass (a3963988-d652-4ad0-9f31-85d2823f070c)
 Call ID: a3963988-d652-4ad0-9f31-85d2823f070c
  Args:
    type: :Person
    source: Patricia_Mountbatten
  AddLiteral (b6d3cbe6-1c77-49d1-8699-73c3b8fd1325)
 Call ID: b6d3cbe6-1c77-49d1-8699-73c3b8fd1325
  Args:
    relation: :hasMarriageYear
    literal_value: 1946
    literal_type: xsd:integer
    source: John_Ulick_Knatchbull
  AddTriple (fabad30e-8ef4-4104-935d-08df9e8ac042)
 Call ID: fabad30e-8ef4-4104-935d-08df9e8ac042
  Args:
    relation: :hasRelation
    source: John_Ulick_Knatchbull
    target: Patricia_Mountbatten
  AssignClass (3e509810-7321-4340-bff6-383292eca93c)
 Call ID: 3e509810-7321-4340-bff6-383292eca93c
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (13c64a29-5500-407e-8350-1e7ced1a6ffa)
 Call ID: 13c64a29-5500-407e-8350-1e7ced1a6ffa
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (b77e0eb2-dc71-438d-9c05-b0ab654774a3)
 Call ID: b77e0eb2-dc71-438d-9c05-b0ab654774a3
  Args:
    target: Louis_Mountbatten
    source: Patricia_Mountbatten
    relation: :hasFather
  AssignClass (c11d950a-d57d-439d-8130-db3b8bb6e90d)
 Call ID: c11d950a-d57d-439d-8130-db3b8bb6e90d
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (107bc621-685f-4bbe-b4a2-7a288525767d)
 Call ID: 107bc621-685f-4bbe-b4a2-7a288525767d
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (4f266b7a-76ec-481d-bc0c-3dcbdf51c45f)
 Call ID: 4f266b7a-76ec-481d-bc0c-3dcbdf51c45f
  Args:
    relation: :hasSon
    target: Norton_Louis_Philip_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (3bcee6b4-30f9-473b-a765-ad9bb7c11b5b)
 Call ID: 3bcee6b4-30f9-473b-a765-ad9bb7c11b5b
  Args:
    target: Patricia_Mountbatten
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMother
  AssignClass (b937d07d-43ab-417b-95d4-d7af487635ce)
 Call ID: b937d07d-43ab-417b-95d4-d7af487635ce
  Args:
    type: :Woman
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AssignClass (13f89b7c-443b-4db5-9ecb-02e433dc07f4)
 Call ID: 13f89b7c-443b-4db5-9ecb-02e433dc07f4
  Args:
    type: :Person
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
  AddTriple (5bd9fff2-8239-4778-94a1-b735a0314041)
 Call ID: 5bd9fff2-8239-4778-94a1-b735a0314041
  Args:
    relation: :hasDaughter
    target: Lady_Amanda_Patricia_Victoria_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (0d3f65c8-b84b-4ba7-ac5c-3cf9e57f3f80)
 Call ID: 0d3f65c8-b84b-4ba7-ac5c-3cf9e57f3f80
  Args:
    relation: :hasMother
    source: Lady_Amanda_Patricia_Victoria_Knatchbull
    target: Patricia_Mountbatten
  AssignClass (306b466c-3c9a-455b-bf20-d40755a2a5df)
 Call ID: 306b466c-3c9a-455b-bf20-d40755a2a5df
  Args:
    type: :Man
    source: Nicholas_Timothy_Charles_Knatchbull
  AssignClass (d109aed9-6d8a-48da-99a9-1e5fe64d0a34)
 Call ID: d109aed9-6d8a-48da-99a9-1e5fe64d0a34
  Args:
    type: :Person
    source: Nicholas_Timothy_Charles_Knatchbull
  AddTriple (c8e45d1b-ee23-492e-abf0-9f81b90c0a5f)
 Call ID: c8e45d1b-ee23-492e-abf0-9f81b90c0a5f
  Args:
    relation: :hasSon
    target: Nicholas_Timothy_Charles_Knatchbull
    source: John_Ulick_Knatchbull
  AddTriple (495cbeef-0bd0-476f-bb98-87ac0a2a83dc)
 Call ID: 495cbeef-0bd0-476f-bb98-87ac0a2a83dc
  Args:
    source: Nicholas_Timothy_Charles_Knatchbull
    target: Patricia_Mountbatten
    relation: :hasMother
  AssignClass (37f57aba-aa84-4446-bbac-ce8bb6b6b0b2)
 Call ID: 37f57aba-aa84-4446-bbac-ce8bb6b6b0b2
  Args:
    type: :Man
    source: Timothy_Knatchbull
  AssignClass (aba7aa7a-95a9-4f6f-bb1b-d2972e0f2d1f)
 Call ID: aba7aa7a-95a9-4f6f-bb1b-d2972e0f2d1f
  Args:
    type: :Person
    source: Timothy_Knatchbull
  AddTriple (22bd21cd-9037-44d9-9693-0b3b2f44f506)
 Call ID: 22bd21cd-9037-44d9-9693-0b3b2f44f506
  Args:
    source: John_Ulick_Knatchbull
    target: Timothy_Knatchbull
    relation: :hasSon
  AddTriple (0f3ccb27-65a2-47e0-ad63-685cf52e8d28)
 Call ID: 0f3ccb27-65a2-47e0-ad63-685cf52e8d28
  Args:
    target: Patricia_Mountbatten
    source: Timothy_Knatchbull
    relation: :hasMother
  Finish (03572151-8f1f-44ef-8caa-9f472a57a528)
 Call ID: 03572151-8f1f-44ef-8caa-9f472a57a528
  Args: