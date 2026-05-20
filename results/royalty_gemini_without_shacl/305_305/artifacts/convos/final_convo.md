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
Alexander Edgar Lascelles, Viscount Lascelles (born 13 May 1980) is an English chef, and the third child and second son of David Lascelles, 8th Earl of Harewood, and his first wife Margaret, Viscountess Lascelles.
He is heir apparent to the earldom of Harewood, due to his elder brother having been born before their parents' marriage.
A chef, Lascelles has also taught about food at the John of Gaunt School, Trowbridge.
Personal life

Lascelles has a son, Leo (b. 2008), with his former girlfriend, Laleh Yeganegy.
Lascelles has a daughter, Ivy, and a son, Kit, with his wife Annika Reed (m. 2017), born in 2018 and 2023, respectively.



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
  AssignClass (e11b690a-526c-4858-9dfe-2537cae458fa)
 Call ID: e11b690a-526c-4858-9dfe-2537cae458fa
  Args:
    type: :Man
    source: Alexander_Edgar_Lascelles
  AssignClass (3ac96db1-155a-4e68-b294-0e914be2f125)
 Call ID: 3ac96db1-155a-4e68-b294-0e914be2f125
  Args:
    type: :Person
    source: Alexander_Edgar_Lascelles
  AssignClass (e270a4d0-c1f2-4f29-8d6b-b284ac3fb2cd)
 Call ID: e270a4d0-c1f2-4f29-8d6b-b284ac3fb2cd
  Args:
    type: :Man
    source: David_Lascelles
  AssignClass (c0e044b6-08bc-4dc0-bb9d-de5dd2a9dca4)
 Call ID: c0e044b6-08bc-4dc0-bb9d-de5dd2a9dca4
  Args:
    type: :Person
    source: David_Lascelles
  AssignClass (d42d8ee0-9368-4b64-a5ee-eaac950af07b)
 Call ID: d42d8ee0-9368-4b64-a5ee-eaac950af07b
  Args:
    type: :Woman
    source: Margaret_Lascelles
  AssignClass (79f4b3fd-c0da-4fa3-b40c-348b6a24fb7c)
 Call ID: 79f4b3fd-c0da-4fa3-b40c-348b6a24fb7c
  Args:
    type: :Person
    source: Margaret_Lascelles
  AssignClass (dd933e93-c0dd-40da-a156-8d672a21a1e9)
 Call ID: dd933e93-c0dd-40da-a156-8d672a21a1e9
  Args:
    type: :Man
    source: Leo_Lascelles
  AssignClass (5cd67e64-39fa-4b66-b5b0-20a7f0221e4d)
 Call ID: 5cd67e64-39fa-4b66-b5b0-20a7f0221e4d
  Args:
    type: :Person
    source: Leo_Lascelles
  AssignClass (943f9127-6b2d-4c46-b98d-646d74f99a80)
 Call ID: 943f9127-6b2d-4c46-b98d-646d74f99a80
  Args:
    type: :Woman
    source: Laleh_Yeganegy
  AssignClass (4c1978d8-80a8-4b48-b5fb-fdbfd6d031d4)
 Call ID: 4c1978d8-80a8-4b48-b5fb-fdbfd6d031d4
  Args:
    type: :Person
    source: Laleh_Yeganegy
  AssignClass (48b64a53-5d6b-48aa-9a58-8b5cfb78fc89)
 Call ID: 48b64a53-5d6b-48aa-9a58-8b5cfb78fc89
  Args:
    type: :Woman
    source: Ivy_Lascelles
  AssignClass (6734635e-3be8-4482-aac4-9651d4f93556)
 Call ID: 6734635e-3be8-4482-aac4-9651d4f93556
  Args:
    type: :Person
    source: Ivy_Lascelles
  AssignClass (4792cb58-e505-467e-bc63-0f03b1837846)
 Call ID: 4792cb58-e505-467e-bc63-0f03b1837846
  Args:
    type: :Man
    source: Kit_Lascelles
  AssignClass (3a5abd5c-e63f-455f-87e8-a6e21cb20978)
 Call ID: 3a5abd5c-e63f-455f-87e8-a6e21cb20978
  Args:
    type: :Person
    source: Kit_Lascelles
  AssignClass (ffa6893e-2e3d-47ef-b9db-0adc602cd7e7)
 Call ID: ffa6893e-2e3d-47ef-b9db-0adc602cd7e7
  Args:
    type: :Woman
    source: Annika_Reed
  AssignClass (e2e754c0-800c-4e2a-9f2f-f0c6a6a9be62)
 Call ID: e2e754c0-800c-4e2a-9f2f-f0c6a6a9be62
  Args:
    type: :Person
    source: Annika_Reed
  AddLiteral (5bce8292-4ba9-44db-a310-4b1123238110)
 Call ID: 5bce8292-4ba9-44db-a310-4b1123238110
  Args:
    relation: :hasBirthYear
    literal_value: 1980
    source: Alexander_Edgar_Lascelles
    literal_type: xsd:integer
  AddTriple (a023c8a7-e7cd-4127-9c30-4b26c8e49786)
 Call ID: a023c8a7-e7cd-4127-9c30-4b26c8e49786
  Args:
    target: David_Lascelles
    source: Alexander_Edgar_Lascelles
    relation: :hasFather
  AddTriple (871e0beb-d80c-4a50-b9e1-5a202760d6a6)
 Call ID: 871e0beb-d80c-4a50-b9e1-5a202760d6a6
  Args:
    relation: :hasMother
    target: Margaret_Lascelles
    source: Alexander_Edgar_Lascelles
  AddTriple (35d6bc7d-df62-48c6-a034-baa7fcba4e9e)
 Call ID: 35d6bc7d-df62-48c6-a034-baa7fcba4e9e
  Args:
    target: Leo_Lascelles
    source: Alexander_Edgar_Lascelles
    relation: :hasSon
  AddTriple (20afd486-382c-4fff-9bf8-2d040e33fb85)
 Call ID: 20afd486-382c-4fff-9bf8-2d040e33fb85
  Args:
    source: Leo_Lascelles
    target: Laleh_Yeganegy
    relation: :hasMother
  AddLiteral (0a9af1fd-bfd1-48e4-ab9b-ebfcb7360a3d)
 Call ID: 0a9af1fd-bfd1-48e4-ab9b-ebfcb7360a3d
  Args:
    literal_value: 2008
    relation: :hasBirthYear
    source: Leo_Lascelles
    literal_type: xsd:integer
  AddTriple (bdc8a419-bfac-474f-b8b0-3d27ea276970)
 Call ID: bdc8a419-bfac-474f-b8b0-3d27ea276970
  Args:
    source: Alexander_Edgar_Lascelles
    target: Ivy_Lascelles
    relation: :hasDaughter
  AddTriple (c39ff9dd-9ab1-4aed-b831-bbbb9e0d4ba8)
 Call ID: c39ff9dd-9ab1-4aed-b831-bbbb9e0d4ba8
  Args:
    relation: :hasSon
    source: Alexander_Edgar_Lascelles
    target: Kit_Lascelles
  AddTriple (b80fb0ac-8373-4ae9-ac94-b47db6549604)
 Call ID: b80fb0ac-8373-4ae9-ac94-b47db6549604
  Args:
    source: Ivy_Lascelles
    target: Annika_Reed
    relation: :hasMother
  AddTriple (de062d1b-ebc8-4332-ab18-c2a31fa76c70)
 Call ID: de062d1b-ebc8-4332-ab18-c2a31fa76c70
  Args:
    source: Kit_Lascelles
    target: Annika_Reed
    relation: :hasMother
  AddLiteral (0bff4bae-215f-4c34-9687-2448f26cc05a)
 Call ID: 0bff4bae-215f-4c34-9687-2448f26cc05a
  Args:
    source: Alexander_Edgar_Lascelles
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2017
  AddLiteral (dca01439-0fc3-4abb-8a60-63612e172381)
 Call ID: dca01439-0fc3-4abb-8a60-63612e172381
  Args:
    literal_value: 2018
    relation: :hasBirthYear
    source: Ivy_Lascelles
    literal_type: xsd:integer
  AddLiteral (ed54c30c-ac41-4f5d-8b67-35099475ba84)
 Call ID: ed54c30c-ac41-4f5d-8b67-35099475ba84
  Args:
    literal_value: 2023
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Kit_Lascelles
  Finish (068f8ff6-0826-43c0-9bbc-b9e6c32e1d66)
 Call ID: 068f8ff6-0826-43c0-9bbc-b9e6c32e1d66
  Args: