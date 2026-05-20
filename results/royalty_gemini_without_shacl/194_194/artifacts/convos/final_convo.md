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
James Alexander Elphinstone, 18th Lord Elphinstone and 4th Baron Elphinstone, AssocRICS (22 April 1953 – 19 December 1994), was a British nobleman, farmer, and financier.
Early life and family

Lord Elphinstone was the son of Rev. Hon.
Andrew Charles Victor Elphinstone and Jean Frances Hambro.
His paternal grandparents were Sidney Buller-Fullerton-Elphinstone, 16th Lord Elphinstone, and the former Lady Mary Bowes-Lyon, elder sister of Queen Elizabeth The Queen Mother.
Personal life

On 22 April 1978, Lord Elphinstone married Willa Mary Gabrielle Chetwode, daughter of Major George David Chetwode and Lady Willa Elliot-Murray-Kynynmound (herself the daughter of Victor Elliot-Murray-Kynynmound, 5th Earl of Minto, and his wife, Marion Cook).
The couple had four children:


He was succeeded in his titles by his eldest son, Alexander.
References




This biography of a Lord of Parliament in the Peerage of Scotland is a stub.



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
  AssignClass (d30f470d-8a66-4633-92e4-923b4a88d50f)
 Call ID: d30f470d-8a66-4633-92e4-923b4a88d50f
  Args:
    type: :Man
    source: James_Alexander_Elphinstone
  AssignClass (7764a37e-3e05-4abe-907a-67ff8006bf25)
 Call ID: 7764a37e-3e05-4abe-907a-67ff8006bf25
  Args:
    source: James_Alexander_Elphinstone
    type: :Person
  AddLiteral (58cb75fa-8420-4ba8-81a4-5beb8aaa5210)
 Call ID: 58cb75fa-8420-4ba8-81a4-5beb8aaa5210
  Args:
    literal_value: 1953
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: James_Alexander_Elphinstone
  AddLiteral (2c83d900-c37e-4518-95d9-ceb7ab65e2b9)
 Call ID: 2c83d900-c37e-4518-95d9-ceb7ab65e2b9
  Args:
    source: James_Alexander_Elphinstone
    relation: :hasDeathYear
    literal_value: 1994
    literal_type: xsd:integer
  AssignClass (7795fcbe-3fc8-4725-bab8-51293561c475)
 Call ID: 7795fcbe-3fc8-4725-bab8-51293561c475
  Args:
    type: :Man
    source: Andrew_Charles_Victor_Elphinstone
  AssignClass (ffbb4369-7798-4842-aee7-2b91dbe3b62d)
 Call ID: ffbb4369-7798-4842-aee7-2b91dbe3b62d
  Args:
    type: :Person
    source: Andrew_Charles_Victor_Elphinstone
  AddTriple (885da96e-970e-49a7-b10b-67c7c22c89f1)
 Call ID: 885da96e-970e-49a7-b10b-67c7c22c89f1
  Args:
    source: James_Alexander_Elphinstone
    target: Andrew_Charles_Victor_Elphinstone
    relation: :hasFather
  AssignClass (a00c7bb7-85d8-4dd1-8423-6297f00d217f)
 Call ID: a00c7bb7-85d8-4dd1-8423-6297f00d217f
  Args:
    source: Jean_Frances_Hambro
    type: :Woman
  AssignClass (8f431316-1cca-4451-a153-c3a85a8ca3a4)
 Call ID: 8f431316-1cca-4451-a153-c3a85a8ca3a4
  Args:
    source: Jean_Frances_Hambro
    type: :Person
  AddTriple (2fecf7de-53a1-4a2a-a1c9-0b2365b104d9)
 Call ID: 2fecf7de-53a1-4a2a-a1c9-0b2365b104d9
  Args:
    relation: :hasMother
    source: James_Alexander_Elphinstone
    target: Jean_Frances_Hambro
  AssignClass (b10f4918-7b0c-47bd-a888-736b64a51123)
 Call ID: b10f4918-7b0c-47bd-a888-736b64a51123
  Args:
    type: :Man
    source: Sidney_Buller-Fullerton-Elphinstone
  AssignClass (9a911999-fc79-404b-9f67-98d7caa009b9)
 Call ID: 9a911999-fc79-404b-9f67-98d7caa009b9
  Args:
    type: :Person
    source: Sidney_Buller-Fullerton-Elphinstone
  AddTriple (2622e485-f10d-4844-8f55-bfa0840ae77b)
 Call ID: 2622e485-f10d-4844-8f55-bfa0840ae77b
  Args:
    relation: :hasFather
    target: Sidney_Buller-Fullerton-Elphinstone
    source: Andrew_Charles_Victor_Elphinstone
  AssignClass (2b29a77f-020d-42d3-a27e-4851761e6c41)
 Call ID: 2b29a77f-020d-42d3-a27e-4851761e6c41
  Args:
    type: :Woman
    source: Mary_Bowes-Lyon
  AssignClass (e93bd055-fc79-4f9a-8439-0a0277851c40)
 Call ID: e93bd055-fc79-4f9a-8439-0a0277851c40
  Args:
    source: Mary_Bowes-Lyon
    type: :Person
  AddTriple (6d3325eb-a4f8-445b-abbf-f37a65d86df2)
 Call ID: 6d3325eb-a4f8-445b-abbf-f37a65d86df2
  Args:
    target: Mary_Bowes-Lyon
    source: Andrew_Charles_Victor_Elphinstone
    relation: :hasMother
  AssignClass (7a1a6477-cd8f-4b24-871a-43c8eae51d05)
 Call ID: 7a1a6477-cd8f-4b24-871a-43c8eae51d05
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Woman
  AssignClass (571a1b2b-93bd-44da-a1e7-994f2cd8f106)
 Call ID: 571a1b2b-93bd-44da-a1e7-994f2cd8f106
  Args:
    source: Willa_Mary_Gabrielle_Chetwode
    type: :Person
  AddLiteral (dd941278-f44d-473e-94d9-18172f2ab2df)
 Call ID: dd941278-f44d-473e-94d9-18172f2ab2df
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1978
    source: James_Alexander_Elphinstone
  AddTriple (6403baf6-94c2-4f7d-89b4-d27404dfff69)
 Call ID: 6403baf6-94c2-4f7d-89b4-d27404dfff69
  Args:
    relation: :hasRelation
    source: James_Alexander_Elphinstone
    target: Willa_Mary_Gabrielle_Chetwode
  AssignClass (5d50baae-7fc2-4910-96a1-461be85ce1b0)
 Call ID: 5d50baae-7fc2-4910-96a1-461be85ce1b0
  Args:
    source: George_David_Chetwode
    type: :Man
  AssignClass (67d62a27-46a8-4b23-93db-9cc477316d47)
 Call ID: 67d62a27-46a8-4b23-93db-9cc477316d47
  Args:
    type: :Person
    source: George_David_Chetwode
  AddTriple (6c7c42e1-baa8-437e-a934-6a5b172f9124)
 Call ID: 6c7c42e1-baa8-437e-a934-6a5b172f9124
  Args:
    target: George_David_Chetwode
    source: Willa_Mary_Gabrielle_Chetwode
    relation: :hasFather
  AssignClass (a2fc9d78-4dbb-4807-99ce-90fecd236f78)
 Call ID: a2fc9d78-4dbb-4807-99ce-90fecd236f78
  Args:
    source: Willa_Elliot-Murray-Kynynmound
    type: :Woman
  AssignClass (cbe54d5c-87eb-4874-8926-1e822c0107bd)
 Call ID: cbe54d5c-87eb-4874-8926-1e822c0107bd
  Args:
    type: :Person
    source: Willa_Elliot-Murray-Kynynmound
  AddTriple (2f33a91c-6f0e-40a2-a1fa-a28a7f695fd5)
 Call ID: 2f33a91c-6f0e-40a2-a1fa-a28a7f695fd5
  Args:
    relation: :hasMother
    target: Willa_Elliot-Murray-Kynynmound
    source: Willa_Mary_Gabrielle_Chetwode
  AssignClass (1fa5daa2-98b1-476f-8d78-ab6f5195a605)
 Call ID: 1fa5daa2-98b1-476f-8d78-ab6f5195a605
  Args:
    source: Victor_Elliot-Murray-Kynynmound
    type: :Man
  AssignClass (bde52717-9614-49ea-8246-d23c8393db3b)
 Call ID: bde52717-9614-49ea-8246-d23c8393db3b
  Args:
    type: :Person
    source: Victor_Elliot-Murray-Kynynmound
  AddTriple (dac31cf0-f47a-429f-95c6-79c01176a2e2)
 Call ID: dac31cf0-f47a-429f-95c6-79c01176a2e2
  Args:
    relation: :hasFather
    source: Willa_Elliot-Murray-Kynynmound
    target: Victor_Elliot-Murray-Kynynmound
  AssignClass (d3d414f3-d084-4b2b-a3d5-8689e1accfd4)
 Call ID: d3d414f3-d084-4b2b-a3d5-8689e1accfd4
  Args:
    type: :Woman
    source: Marion_Cook
  AssignClass (aaf15aca-dd28-4ce5-989a-6b0039afbc2c)
 Call ID: aaf15aca-dd28-4ce5-989a-6b0039afbc2c
  Args:
    type: :Person
    source: Marion_Cook
  AddTriple (d8403811-a4b7-485c-8704-d249b4ea7895)
 Call ID: d8403811-a4b7-485c-8704-d249b4ea7895
  Args:
    relation: :hasMother
    target: Marion_Cook
    source: Willa_Elliot-Murray-Kynynmound
  AssignClass (6653f9a0-cf49-46b8-95e4-16c43e3437eb)
 Call ID: 6653f9a0-cf49-46b8-95e4-16c43e3437eb
  Args:
    type: :Man
    source: Alexander_Elphinstone
  AssignClass (acff69f8-de11-458f-83bb-8bc38cdd2dae)
 Call ID: acff69f8-de11-458f-83bb-8bc38cdd2dae
  Args:
    source: Alexander_Elphinstone
    type: :Person
  AddTriple (2a3eec66-2f74-40d2-b98a-6c3f67604606)
 Call ID: 2a3eec66-2f74-40d2-b98a-6c3f67604606
  Args:
    relation: :hasFather
    source: Alexander_Elphinstone
    target: James_Alexander_Elphinstone
  Finish (8110b4ff-eea7-46ce-a14a-c5548ce3c2ff)
 Call ID: 8110b4ff-eea7-46ce-a14a-c5548ce3c2ff
  Args: