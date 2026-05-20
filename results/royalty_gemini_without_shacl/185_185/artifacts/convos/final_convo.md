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
Duchess Elisabeth of Mecklenburg-Schwerin (10 August 1869 – 3 September 1955) was a daughter of Frederick Francis II, Grand Duke of Mecklenburg by his third wife Princess Marie of Schwarzburg-Rudolstadt.
By her marriage to Frederick Augustus II, she became the consort of the last reigning Grand Duke of Oldenburg.
Family

Elisabeth was related to many of Europe's royal families.
She was the eldest child of Frederick Francis II, Grand Duke of Mecklenburg by his third wife, Princess Marie of Schwarzburg-Rudolstadt.
She was an older sister of Hendrik, Prince consort of the Netherlands, husband of Queen Wilhelmina of the Netherlands, making her an aunt of Queen Juliana of the Netherlands.
She was also a younger half-sister of Frederick Francis III, Grand Duke of Mecklenburg-Schwerin.
Through Frederick Francis, she was an aunt of Alexandrine, Queen of Denmark and Cecilie, German Crown Princess.
Elisabeth was also a half sister of Marie, Grand Duchess of Russia, who was the mother of Grand Duke Cyril Vladimirovich of Russia, the pretender to the Russian throne.
Her paternal grandparents were Paul Frederick, Grand Duke of Mecklenburg and Princess Alexandrine of Prussia.
Her maternal grandparents were Prince Adolph of Schwarzburg-Rudolstadt and Princess Mathilde of Schönburg-Waldenburg.
Marriage

On 24 October 1896, Elisabeth married Frederick Augustus, Hereditary Grand Duke of Oldenburg.
His first wife Elisabeth Anna had died the previous year, leaving only one surviving daughter: Duchess Sophia Charlotte of Oldenburg.
Frederick Augustus was thus in need of a male heir.
He succeeded as Grand Duke of Oldenburg in 1900, making Elisabeth Grand Duchess consort of Oldenburg.
They had five children:


Frederick was forced to abdicate his throne at the end of World War I, when the former Grand Duchy of the German Empire joined the post-war German Republic.
A year after his abdication, he asked the Oldenburg Diet for a yearly allowance of 150,000 marks, stating that his financial condition was "extremely precarious".
In 1931, Frederick died in Rastede.
Elisabeth died on 3 September 1955, having been widowed for 24 years.



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
  AssignClass (4375f8b3-3d0b-4303-8d48-55312df24dd9)
 Call ID: 4375f8b3-3d0b-4303-8d48-55312df24dd9
  Args:
    type: :Woman
    source: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (570d3b14-273a-42d5-96d9-b610a17c0423)
 Call ID: 570d3b14-273a-42d5-96d9-b610a17c0423
  Args:
    type: :Person
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddLiteral (ef6d690d-d6db-40c9-bd46-3519333d3683)
 Call ID: ef6d690d-d6db-40c9-bd46-3519333d3683
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Elisabeth_of_Mecklenburg-Schwerin
    literal_value: 1869
  AddLiteral (086b28ca-7b3b-44fe-955b-2494ada0f15b)
 Call ID: 086b28ca-7b3b-44fe-955b-2494ada0f15b
  Args:
    literal_type: xsd:integer
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_value: 1955
  AssignClass (b7729bad-3499-41d4-b52e-f87f790e4b28)
 Call ID: b7729bad-3499-41d4-b52e-f87f790e4b28
  Args:
    type: :Man
    source: Frederick_Francis_II_of_Mecklenburg
  AssignClass (9405eeb4-ea19-41fc-97b4-87de82909d17)
 Call ID: 9405eeb4-ea19-41fc-97b4-87de82909d17
  Args:
    type: :Person
    source: Frederick_Francis_II_of_Mecklenburg
  AssignClass (b547308f-b02c-4794-9a69-464053b25091)
 Call ID: b547308f-b02c-4794-9a69-464053b25091
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (f07b6d7a-a9f0-4f19-9ae8-20f0853347ee)
 Call ID: f07b6d7a-a9f0-4f19-9ae8-20f0853347ee
  Args:
    type: :Person
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (60f81b96-ae09-4c07-abeb-b7322a20e0aa)
 Call ID: 60f81b96-ae09-4c07-abeb-b7322a20e0aa
  Args:
    target: Frederick_Francis_II_of_Mecklenburg
    relation: :hasFather
    source: Elisabeth_of_Mecklenburg-Schwerin
  AddTriple (272afb93-e0af-41e6-9a1e-e239a43e7951)
 Call ID: 272afb93-e0af-41e6-9a1e-e239a43e7951
  Args:
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (c9f561d4-0e0c-455b-8422-e8052cf8fa98)
 Call ID: c9f561d4-0e0c-455b-8422-e8052cf8fa98
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (07fec00a-de99-4abf-98ba-35c058a2b912)
 Call ID: 07fec00a-de99-4abf-98ba-35c058a2b912
  Args:
    type: :Person
    source: Frederick_Augustus_II_of_Oldenburg
  AddLiteral (758fcb39-30fd-47e2-ac55-72bcf81c6836)
 Call ID: 758fcb39-30fd-47e2-ac55-72bcf81c6836
  Args:
    literal_value: 1896
    literal_type: xsd:integer
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasMarriageYear
  AddTriple (ee2a61dc-a957-4c54-ae96-79defa45d27e)
 Call ID: ee2a61dc-a957-4c54-ae96-79defa45d27e
  Args:
    target: Frederick_Augustus_II_of_Oldenburg
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :hasRelation
  AssignClass (c8cf6d6e-4a1c-45be-bf90-b11fef559d06)
 Call ID: c8cf6d6e-4a1c-45be-bf90-b11fef559d06
  Args:
    type: :Man
    source: Hendrik_of_the_Netherlands
  AssignClass (a7acd544-766a-47c4-a6e7-51445287a17f)
 Call ID: a7acd544-766a-47c4-a6e7-51445287a17f
  Args:
    type: :Person
    source: Hendrik_of_the_Netherlands
  AddTriple (ee41c243-b8cd-487c-a78f-12ef27b4c9ed)
 Call ID: ee41c243-b8cd-487c-a78f-12ef27b4c9ed
  Args:
    source: Hendrik_of_the_Netherlands
    relation: :hasSister
    target: Elisabeth_of_Mecklenburg-Schwerin
  AssignClass (cdc0f322-9860-4298-9ce1-66526d8193ff)
 Call ID: cdc0f322-9860-4298-9ce1-66526d8193ff
  Args:
    type: :Man
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (4a6f7037-5263-4ca3-bd56-57bd8b77ce7a)
 Call ID: 4a6f7037-5263-4ca3-bd56-57bd8b77ce7a
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (1fdcc0ea-1e1a-40a6-bd1e-b1742d376353)
 Call ID: 1fdcc0ea-1e1a-40a6-bd1e-b1742d376353
  Args:
    relation: :isSiblingOf
    source: Elisabeth_of_Mecklenburg-Schwerin
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (f0f51850-0bff-4fa1-ad2f-e2c5d3f45352)
 Call ID: f0f51850-0bff-4fa1-ad2f-e2c5d3f45352
  Args:
    type: :Woman
    source: Marie_of_Russia
  AssignClass (f43bdec4-8353-4668-9a57-13791b766efb)
 Call ID: f43bdec4-8353-4668-9a57-13791b766efb
  Args:
    type: :Person
    source: Marie_of_Russia
  AddTriple (0b044bc3-fd09-44dc-8ad5-305800be2ebc)
 Call ID: 0b044bc3-fd09-44dc-8ad5-305800be2ebc
  Args:
    target: Marie_of_Russia
    source: Elisabeth_of_Mecklenburg-Schwerin
    relation: :isSiblingOf
  AssignClass (1c993ec8-1b03-4404-8b40-d71c91128078)
 Call ID: 1c993ec8-1b03-4404-8b40-d71c91128078
  Args:
    type: :Man
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (02f44cf9-72bd-410f-ac4b-a986b3ed53f4)
 Call ID: 02f44cf9-72bd-410f-ac4b-a986b3ed53f4
  Args:
    type: :Person
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (63f10648-9ee6-40c1-a8d1-2f9d5c9165c8)
 Call ID: 63f10648-9ee6-40c1-a8d1-2f9d5c9165c8
  Args:
    type: :Woman
    source: Alexandrine_of_Prussia
  AssignClass (6fc46a3a-65ea-42c9-9e12-fa79ff192441)
 Call ID: 6fc46a3a-65ea-42c9-9e12-fa79ff192441
  Args:
    type: :Person
    source: Alexandrine_of_Prussia
  AddTriple (b9b850c1-a1a0-423f-9546-3450e53e231f)
 Call ID: b9b850c1-a1a0-423f-9546-3450e53e231f
  Args:
    target: Paul_Frederick_of_Mecklenburg
    relation: :hasFather
    source: Frederick_Francis_II_of_Mecklenburg
  AddTriple (25c804f9-d75d-467c-8ce0-291fe6767d6b)
 Call ID: 25c804f9-d75d-467c-8ce0-291fe6767d6b
  Args:
    relation: :hasMother
    source: Frederick_Francis_II_of_Mecklenburg
    target: Alexandrine_of_Prussia
  AssignClass (485b393e-37f2-4dca-be7f-2403efcab05f)
 Call ID: 485b393e-37f2-4dca-be7f-2403efcab05f
  Args:
    type: :Man
    source: Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (f8a3a86d-7daf-4e42-b8cf-62266b7ee40b)
 Call ID: f8a3a86d-7daf-4e42-b8cf-62266b7ee40b
  Args:
    type: :Person
    source: Adolph_of_Schwarzburg-Rudolstadt
  AssignClass (de95581f-a1a8-4480-9863-959bab083153)
 Call ID: de95581f-a1a8-4480-9863-959bab083153
  Args:
    type: :Woman
    source: Mathilde_of_Schönburg-Waldenburg
  AssignClass (9d8e1073-9e58-42d8-9504-dc0360e5f6a7)
 Call ID: 9d8e1073-9e58-42d8-9504-dc0360e5f6a7
  Args:
    type: :Person
    source: Mathilde_of_Schönburg-Waldenburg
  AddTriple (9636d65e-6005-430e-8d76-cc4bcf6b2de8)
 Call ID: 9636d65e-6005-430e-8d76-cc4bcf6b2de8
  Args:
    target: Adolph_of_Schwarzburg-Rudolstadt
    source: Marie_of_Schwarzburg-Rudolstadt
    relation: :hasFather
  AddTriple (b4299ed1-005c-413e-a5d6-d71badeac664)
 Call ID: b4299ed1-005c-413e-a5d6-d71badeac664
  Args:
    target: Mathilde_of_Schönburg-Waldenburg
    relation: :hasMother
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (877b7cca-3137-4f17-8571-54c112bbd94e)
 Call ID: 877b7cca-3137-4f17-8571-54c112bbd94e
  Args:
    type: :Woman
    source: Elisabeth_Anna_of_Oldenburg
  AssignClass (4d752a9e-3dcc-45f3-a113-ce3e7ed0ba91)
 Call ID: 4d752a9e-3dcc-45f3-a113-ce3e7ed0ba91
  Args:
    type: :Person
    source: Elisabeth_Anna_of_Oldenburg
  AddTriple (1053971a-f369-4029-a712-29ef88498272)
 Call ID: 1053971a-f369-4029-a712-29ef88498272
  Args:
    relation: :hasRelation
    source: Frederick_Augustus_II_of_Oldenburg
    target: Elisabeth_Anna_of_Oldenburg
  AssignClass (09636f8b-088e-4e1b-ae39-cea679c8a658)
 Call ID: 09636f8b-088e-4e1b-ae39-cea679c8a658
  Args:
    type: :Woman
    source: Sophia_Charlotte_of_Oldenburg
  AssignClass (a0bdbff5-115e-4e14-8fbd-86636ac93973)
 Call ID: a0bdbff5-115e-4e14-8fbd-86636ac93973
  Args:
    type: :Person
    source: Sophia_Charlotte_of_Oldenburg
  AddTriple (eec4d6a9-4e2a-4055-bb28-33514cf4bc0a)
 Call ID: eec4d6a9-4e2a-4055-bb28-33514cf4bc0a
  Args:
    source: Sophia_Charlotte_of_Oldenburg
    relation: :isDaughterOf
    target: Frederick_Augustus_II_of_Oldenburg
  AddTriple (eaf91dea-f85b-4287-bdc1-8f97236b55a6)
 Call ID: eaf91dea-f85b-4287-bdc1-8f97236b55a6
  Args:
    target: Elisabeth_Anna_of_Oldenburg
    relation: :isDaughterOf
    source: Sophia_Charlotte_of_Oldenburg
  Finish (2595a346-54b6-48a7-bafc-ccd8504f58eb)
 Call ID: 2595a346-54b6-48a7-bafc-ccd8504f58eb
  Args: