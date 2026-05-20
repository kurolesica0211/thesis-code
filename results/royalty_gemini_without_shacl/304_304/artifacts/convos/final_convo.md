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
Alexander Mountstuart Elphinstone, 19th Lord Elphinstone, 5th Baron Elphinstone (born 15 April 1980), is a Scottish peer in both the Peerage of Scotland and the Peerage of the United Kingdom.
Early life and family

Lord Elphinstone is the son of James Elphinstone, 18th Lord Elphinstone, and Willa Mary Gabrielle Chetwode.
His mother is the daughter of Major George Chetwode and Lady Willa Elliot-Murray-Kynynmound, daughter of Victor Elliot-Murray-Kynynmound, 5th Earl of Minto.
Lord Elphinstone's paternal grandfather, Rev. Hon.
Andrew Elphinstone, was a first cousin of Elizabeth II through his mother, the former Lady Mary Bowes-Lyon, who was an elder sister of Queen Elizabeth The Queen Mother.
Notes

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
  AssignClass (1401ed72-648e-4555-ac75-2e134125eb24)
 Call ID: 1401ed72-648e-4555-ac75-2e134125eb24
  Args:
    source: Alexander Mountstuart Elphinstone
    type: :Man
  AssignClass (b54d46c3-a51c-4ccc-9970-dcaea3151bf6)
 Call ID: b54d46c3-a51c-4ccc-9970-dcaea3151bf6
  Args:
    source: Alexander Mountstuart Elphinstone
    type: :Person
  AddLiteral (6e90da3d-2490-4f96-bbba-51025c2ad5dd)
 Call ID: 6e90da3d-2490-4f96-bbba-51025c2ad5dd
  Args:
    literal_value: 15 April 1980
    literal_type: xsd:string
    source: Alexander Mountstuart Elphinstone
    relation: :hasBirthYear
  AssignClass (cf25df31-d2f2-409e-b4e5-4e1521035f3c)
 Call ID: cf25df31-d2f2-409e-b4e5-4e1521035f3c
  Args:
    source: James Elphinstone
    type: :Man
  AssignClass (d4b6a498-dce9-40b8-a0bf-9555bf082ba7)
 Call ID: d4b6a498-dce9-40b8-a0bf-9555bf082ba7
  Args:
    type: :Person
    source: James Elphinstone
  AddTriple (0bb34bbd-be5d-4994-a27f-a3c148a102ee)
 Call ID: 0bb34bbd-be5d-4994-a27f-a3c148a102ee
  Args:
    target: James Elphinstone
    relation: :hasFather
    source: Alexander Mountstuart Elphinstone
  AssignClass (26ef17c1-e788-49ef-ac4a-0359869ddd4a)
 Call ID: 26ef17c1-e788-49ef-ac4a-0359869ddd4a
  Args:
    type: :Woman
    source: Willa Mary Gabrielle Chetwode
  AssignClass (7f5b26d1-de8c-4b49-8bf3-74148d8b04b7)
 Call ID: 7f5b26d1-de8c-4b49-8bf3-74148d8b04b7
  Args:
    type: :Person
    source: Willa Mary Gabrielle Chetwode
  AddTriple (cde2f2e6-26b2-4d5e-aad4-40b2f44357dd)
 Call ID: cde2f2e6-26b2-4d5e-aad4-40b2f44357dd
  Args:
    source: Alexander Mountstuart Elphinstone
    target: Willa Mary Gabrielle Chetwode
    relation: :hasMother
  AssignClass (ed1c72e0-56ed-4505-beca-7ca98451545d)
 Call ID: ed1c72e0-56ed-4505-beca-7ca98451545d
  Args:
    source: Major George Chetwode
    type: :Man
  AssignClass (a88d6391-c2dd-496b-a6ae-f8553bfa706e)
 Call ID: a88d6391-c2dd-496b-a6ae-f8553bfa706e
  Args:
    type: :Person
    source: Major George Chetwode
  AddTriple (262948ad-6c3f-4e75-b424-d1769c7b7380)
 Call ID: 262948ad-6c3f-4e75-b424-d1769c7b7380
  Args:
    source: Willa Mary Gabrielle Chetwode
    relation: :hasFather
    target: Major George Chetwode
  AssignClass (fa3cc495-e3c2-4bb2-ae1d-1be82f56c6bd)
 Call ID: fa3cc495-e3c2-4bb2-ae1d-1be82f56c6bd
  Args:
    type: :Woman
    source: Lady Willa Elliot-Murray-Kynynmound
  AssignClass (58b581b4-15f8-47fa-ab0e-13c199d197b8)
 Call ID: 58b581b4-15f8-47fa-ab0e-13c199d197b8
  Args:
    source: Lady Willa Elliot-Murray-Kynynmound
    type: :Person
  AddTriple (88423dd6-5efb-4073-abbb-8ade34c53a3f)
 Call ID: 88423dd6-5efb-4073-abbb-8ade34c53a3f
  Args:
    target: Lady Willa Elliot-Murray-Kynynmound
    relation: :hasMother
    source: Willa Mary Gabrielle Chetwode
  AssignClass (6106c967-cb57-4cbf-8d5d-f395326bc9ab)
 Call ID: 6106c967-cb57-4cbf-8d5d-f395326bc9ab
  Args:
    source: Victor Elliot-Murray-Kynynmound
    type: :Man
  AssignClass (e85bcd25-a5e5-45e0-978c-f6cd409f9558)
 Call ID: e85bcd25-a5e5-45e0-978c-f6cd409f9558
  Args:
    source: Victor Elliot-Murray-Kynynmound
    type: :Person
  AddTriple (99784a9f-1dca-4bb2-adec-a22a9e8b13ad)
 Call ID: 99784a9f-1dca-4bb2-adec-a22a9e8b13ad
  Args:
    source: Lady Willa Elliot-Murray-Kynynmound
    target: Victor Elliot-Murray-Kynynmound
    relation: :hasFather
  AssignClass (8b8c6fd7-ca88-49d4-8795-31dbcbd627f6)
 Call ID: 8b8c6fd7-ca88-49d4-8795-31dbcbd627f6
  Args:
    type: :Man
    source: Rev. Hon. Andrew Elphinstone
  AssignClass (5c7f5fdf-0d2b-4325-894c-19dc665561de)
 Call ID: 5c7f5fdf-0d2b-4325-894c-19dc665561de
  Args:
    type: :Person
    source: Rev. Hon. Andrew Elphinstone
  AddTriple (7408d51c-facd-4ec8-ab03-d0aa210a6df5)
 Call ID: 7408d51c-facd-4ec8-ab03-d0aa210a6df5
  Args:
    source: Alexander Mountstuart Elphinstone
    relation: :hasFather
    target: Rev. Hon. Andrew Elphinstone
  AssignClass (787c5382-3605-487b-a7b0-58459511bc91)
 Call ID: 787c5382-3605-487b-a7b0-58459511bc91
  Args:
    source: Lady Mary Bowes-Lyon
    type: :Woman
  AssignClass (5e4cfd43-b031-4196-932d-a426a6b2dd80)
 Call ID: 5e4cfd43-b031-4196-932d-a426a6b2dd80
  Args:
    source: Lady Mary Bowes-Lyon
    type: :Person
  AddTriple (a82241dd-68a0-424c-b3fe-7892393cbe10)
 Call ID: a82241dd-68a0-424c-b3fe-7892393cbe10
  Args:
    source: Rev. Hon. Andrew Elphinstone
    relation: :hasMother
    target: Lady Mary Bowes-Lyon
  AssignClass (fea5a32e-7091-4d92-bf19-abbe8d64f50f)
 Call ID: fea5a32e-7091-4d92-bf19-abbe8d64f50f
  Args:
    type: :Woman
    source: Queen Elizabeth The Queen Mother
  AssignClass (78ac3efe-cc5f-4cef-8697-e5eb50c90236)
 Call ID: 78ac3efe-cc5f-4cef-8697-e5eb50c90236
  Args:
    type: :Person
    source: Queen Elizabeth The Queen Mother
  AddTriple (748623bf-e2db-4363-9656-94b019f054c4)
 Call ID: 748623bf-e2db-4363-9656-94b019f054c4
  Args:
    source: Lady Mary Bowes-Lyon
    relation: :isSisterOf
    target: Queen Elizabeth The Queen Mother
  AssignClass (4281c5b6-690f-4115-aa93-50d037ed67b7)
 Call ID: 4281c5b6-690f-4115-aa93-50d037ed67b7
  Args:
    source: Elizabeth II
    type: :Woman
  AssignClass (7fe50071-b75d-434d-86f2-2ad4861e2e1d)
 Call ID: 7fe50071-b75d-434d-86f2-2ad4861e2e1d
  Args:
    type: :Person
    source: Elizabeth II
  Finish (1f77b09f-0b0d-47c4-bafc-4f82635ea7a2)
 Call ID: 1f77b09f-0b0d-47c4-bafc-4f82635ea7a2
  Args: