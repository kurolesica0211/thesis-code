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
Lady Marina Charlotte
Alexandra Katharine Helen Windsor (born 30 September 1992) is a British philanthropic executive and relative of the British royal family.
Early life, family, and education

Lady Marina Charlotte
Alexandra Katharine Helen Windsor was born on 30 September 1992 at the Rosie Hospital in Cambridge, Cambridgeshire, the second child of George Windsor, Earl of St Andrews, a diplomat and member of the House of Windsor, and Sylvana Tomaselli, a Canadian historian and member of the Austrian-Italian Tomaselli family.
Her older brother is Edward Windsor, Lord Downpatrick, and her younger sister is Lady Amelia Windsor.
She is a paternal granddaughter of Prince Edward, Duke of Kent, who is a first cousin of Elizabeth II, and Katharine, Duchess of Kent, the only daughter of Sir William Worsley, 4th Baronet.
Alexandra Katharine Helen Windsor in a Church of England ceremony by William Booth, the sub-dean of the Chapel Royal at St James's Palace.
Her godparents are Lady Ralph Kerr, Katherine Ruth Panter, William Hanbury-Tenison, and Sasha Poklewski-Koziell.
Personal life

She attended the wedding of her third cousin Prince William, Duke of Cambridge to Catherine Middleton in 2011.



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
  AssignClass (b8466be8-9729-41fb-990e-cf09e0f5e443)
 Call ID: b8466be8-9729-41fb-990e-cf09e0f5e443
  Args:
    type: :Person
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AssignClass (636426dd-2e0f-4300-9099-0bcd02632abf)
 Call ID: 636426dd-2e0f-4300-9099-0bcd02632abf
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    type: :Woman
  AssignClass (c4ba29d2-26b7-4ebe-a326-8edc63bb5417)
 Call ID: c4ba29d2-26b7-4ebe-a326-8edc63bb5417
  Args:
    type: :Person
    source: :George_Windsor_Earl_of_St_Andrews
  AssignClass (d47d72c1-69ac-4a40-bcce-cf21e48be360)
 Call ID: d47d72c1-69ac-4a40-bcce-cf21e48be360
  Args:
    source: :George_Windsor_Earl_of_St_Andrews
    type: :Man
  AssignClass (29681346-f7b2-4caa-a6fa-31c692ee69c0)
 Call ID: 29681346-f7b2-4caa-a6fa-31c692ee69c0
  Args:
    type: :Person
    source: :Sylvana_Tomaselli
  AssignClass (00d5e40a-413f-4ed9-bc00-4c18c50b99f6)
 Call ID: 00d5e40a-413f-4ed9-bc00-4c18c50b99f6
  Args:
    source: :Sylvana_Tomaselli
    type: :Woman
  AssignClass (8db052cf-7a7a-452b-bb65-762aec6cbe3f)
 Call ID: 8db052cf-7a7a-452b-bb65-762aec6cbe3f
  Args:
    type: :Person
    source: :Edward_Windsor_Lord_Downpatrick
  AssignClass (ecc5a595-e162-4091-bfc4-3eb732044942)
 Call ID: ecc5a595-e162-4091-bfc4-3eb732044942
  Args:
    source: :Edward_Windsor_Lord_Downpatrick
    type: :Man
  AssignClass (eac5fea2-0c11-4a59-a2ab-2a03b5bf18a9)
 Call ID: eac5fea2-0c11-4a59-a2ab-2a03b5bf18a9
  Args:
    source: :Lady_Amelia_Windsor
    type: :Person
  AssignClass (5625a9b6-f7c8-4d19-9d7e-a51575bffd2d)
 Call ID: 5625a9b6-f7c8-4d19-9d7e-a51575bffd2d
  Args:
    type: :Woman
    source: :Lady_Amelia_Windsor
  AssignClass (c1f0ef35-1b77-4697-a2b9-59a48a3929e1)
 Call ID: c1f0ef35-1b77-4697-a2b9-59a48a3929e1
  Args:
    type: :Person
    source: :Prince_Edward_Duke_of_Kent
  AssignClass (ed831427-c8ed-4bce-85dc-0f1ae2573be8)
 Call ID: ed831427-c8ed-4bce-85dc-0f1ae2573be8
  Args:
    type: :Man
    source: :Prince_Edward_Duke_of_Kent
  AssignClass (7fcbe673-2b71-40fc-947c-3b71e0cb8510)
 Call ID: 7fcbe673-2b71-40fc-947c-3b71e0cb8510
  Args:
    source: :Katharine_Duchess_of_Kent
    type: :Person
  AssignClass (3e8f041a-77af-448f-a7e4-43c50110debb)
 Call ID: 3e8f041a-77af-448f-a7e4-43c50110debb
  Args:
    type: :Woman
    source: :Katharine_Duchess_of_Kent
  AssignClass (78dbf516-8405-4415-ae4f-cba0667ad7f3)
 Call ID: 78dbf516-8405-4415-ae4f-cba0667ad7f3
  Args:
    source: :Sir_William_Worsley_4th_Baronet
    type: :Person
  AssignClass (1e5bb6a8-f4ff-4ad2-adf8-0563e1062f88)
 Call ID: 1e5bb6a8-f4ff-4ad2-adf8-0563e1062f88
  Args:
    type: :Man
    source: :Sir_William_Worsley_4th_Baronet
  AddLiteral (af40bd71-0c13-4d7c-9c57-a05defced585)
 Call ID: af40bd71-0c13-4d7c-9c57-a05defced585
  Args:
    literal_type: xsd:integer
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    literal_value: 1992
    relation: :hasBirthYear
  AddTriple (2f7e5b62-5304-426a-ba0c-643c6e20a755)
 Call ID: 2f7e5b62-5304-426a-ba0c-643c6e20a755
  Args:
    relation: :hasFather
    target: :George_Windsor_Earl_of_St_Andrews
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AddTriple (7150722c-54fb-44da-a207-5ede870ec98c)
 Call ID: 7150722c-54fb-44da-a207-5ede870ec98c
  Args:
    relation: :hasMother
    target: :Sylvana_Tomaselli
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AddTriple (2288b822-8e95-4e28-822a-debb763022ba)
 Call ID: 2288b822-8e95-4e28-822a-debb763022ba
  Args:
    target: :Edward_Windsor_Lord_Downpatrick
    relation: :hasBrother
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AddTriple (b9ce3520-f0f1-46ac-ad9c-14648745d49f)
 Call ID: b9ce3520-f0f1-46ac-ad9c-14648745d49f
  Args:
    target: :Lady_Amelia_Windsor
    relation: :hasSister
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
  AddTriple (ab19a564-1819-49db-b9bf-045d6db30617)
 Call ID: ab19a564-1819-49db-b9bf-045d6db30617
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    target: :Prince_Edward_Duke_of_Kent
    relation: :hasFather
  AddTriple (95ff7da3-753a-42fe-8d4b-a75fb178bdc8)
 Call ID: 95ff7da3-753a-42fe-8d4b-a75fb178bdc8
  Args:
    source: :Lady_Marina_Charlotte_Alexandra_Katharine_Helen_Windsor
    target: :Katharine_Duchess_of_Kent
    relation: :hasMother
  AddTriple (7a4f321c-a151-4087-8a25-dcadd8a79416)
 Call ID: 7a4f321c-a151-4087-8a25-dcadd8a79416
  Args:
    relation: :hasFather
    target: :Sir_William_Worsley_4th_Baronet
    source: :Katharine_Duchess_of_Kent
  Finish (4bc32cd5-f8bc-4b29-8aef-7df8d4ed0734)
 Call ID: 4bc32cd5-f8bc-4b29-8aef-7df8d4ed0734
  Args: