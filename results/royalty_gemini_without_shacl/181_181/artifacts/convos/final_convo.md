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
Princess Maria Immaculata Cristina Pia Isabella of Bourbon-Two Sicilies (Full Italian name: Maria Immacolata Speranza Pia Teresa Cristina Filomena Lucia Anna Isabella Cecilia Apollonia Barbara Agnese Zenobia, Principessa di Borbone delle
Due Sicilie,) (30 October 1874 – 28 November 1947) was the fourth child and eldest daughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta, and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage

Maria Immaculata married Prince Johann Georg of Saxony, sixth child and second-eldest son of George of Saxony and his wife Maria Anna of Portugal, on 30 October 1906 in Cannes.
Her mother-in-law, Maria Anna, was the daughter of Maria II of Portugal and her husband Ferdinand II of Portugal.
The couple did not have children, but Maria Immaculata cared for the children of her brother-in-law Frederick Augustus III of Saxony.



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
  AssignClass (12d23385-5c38-4eea-99bf-220c280c8ae5)
 Call ID: 12d23385-5c38-4eea-99bf-220c280c8ae5
  Args:
    type: :Woman
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AssignClass (75601a23-090e-4cd5-ba4d-dd24dc04d88a)
 Call ID: 75601a23-090e-4cd5-ba4d-dd24dc04d88a
  Args:
    type: :Person
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AddLiteral (c427b8e6-d720-41e4-997f-2e18f40669b2)
 Call ID: c427b8e6-d720-41e4-997f-2e18f40669b2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1874
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AddLiteral (5536c176-d230-4ed0-8f52-10d0924cd0ea)
 Call ID: 5536c176-d230-4ed0-8f52-10d0924cd0ea
  Args:
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_value: 1947
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (3b24db7b-ea36-4e7c-b58a-1d94d1836a2d)
 Call ID: 3b24db7b-ea36-4e7c-b58a-1d94d1836a2d
  Args:
    type: :Man
    source: Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (7234e855-5020-4c87-9b46-64f81fd62571)
 Call ID: 7234e855-5020-4c87-9b46-64f81fd62571
  Args:
    type: :Person
    source: Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (217628f8-51a5-4376-9d20-4302aed060b1)
 Call ID: 217628f8-51a5-4376-9d20-4302aed060b1
  Args:
    type: :Ancestor
    source: Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (b88fe6f0-4634-41ad-a5ae-d9ebb2449d35)
 Call ID: b88fe6f0-4634-41ad-a5ae-d9ebb2449d35
  Args:
    type: :Woman
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (43e29ded-2840-46f5-bf54-aeea2fc86d70)
 Call ID: 43e29ded-2840-46f5-bf54-aeea2fc86d70
  Args:
    type: :Person
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (40145c6b-9b94-455e-aa47-10fc00ac5909)
 Call ID: 40145c6b-9b94-455e-aa47-10fc00ac5909
  Args:
    type: :Ancestor
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (29abc5cc-53e6-4e3c-a467-64db9824af28)
 Call ID: 29abc5cc-53e6-4e3c-a467-64db9824af28
  Args:
    relation: :hasFather
    target: Alfonso_of_Bourbon-Two_Sicilies
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AddTriple (3eeb617c-c47d-434a-872c-57117f51eb20)
 Call ID: 3eeb617c-c47d-434a-872c-57117f51eb20
  Args:
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (f5c527de-11e2-4434-b34f-22615a1d4f44)
 Call ID: f5c527de-11e2-4434-b34f-22615a1d4f44
  Args:
    type: :Man
    source: Johann_Georg_of_Saxony
  AssignClass (85d4f6db-fb72-4794-a60e-c6457e41da74)
 Call ID: 85d4f6db-fb72-4794-a60e-c6457e41da74
  Args:
    type: :Person
    source: Johann_Georg_of_Saxony
  AddLiteral (77622478-6760-48a2-a4df-c66a1b04c818)
 Call ID: 77622478-6760-48a2-a4df-c66a1b04c818
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_value: 1906
  AddTriple (0f3fa85e-0da6-411d-816a-21ac18423d61)
 Call ID: 0f3fa85e-0da6-411d-816a-21ac18423d61
  Args:
    relation: :hasRelation
    target: Johann_Georg_of_Saxony
    source: Maria_Immaculata_of_Bourbon-Two_Sicilies
  AssignClass (664ad7a9-fd0d-4a77-8854-8095a33b7b56)
 Call ID: 664ad7a9-fd0d-4a77-8854-8095a33b7b56
  Args:
    type: :Man
    source: George_of_Saxony
  AssignClass (e4494824-7c0a-4ab2-bf0e-96dcfdba7ca4)
 Call ID: e4494824-7c0a-4ab2-bf0e-96dcfdba7ca4
  Args:
    type: :Person
    source: George_of_Saxony
  AssignClass (4cceacbd-9932-4843-a9b5-3ece8eb28eae)
 Call ID: 4cceacbd-9932-4843-a9b5-3ece8eb28eae
  Args:
    type: :Woman
    source: Maria_Anna_of_Portugal
  AssignClass (13278e03-9f5a-439d-869b-c9f54597770f)
 Call ID: 13278e03-9f5a-439d-869b-c9f54597770f
  Args:
    type: :Person
    source: Maria_Anna_of_Portugal
  AddTriple (b6e6134f-0b33-479d-a38f-cd1ca3018d0a)
 Call ID: b6e6134f-0b33-479d-a38f-cd1ca3018d0a
  Args:
    relation: :hasFather
    target: George_of_Saxony
    source: Johann_Georg_of_Saxony
  AddTriple (f360496a-7696-452a-b0cc-8b70f01bafc3)
 Call ID: f360496a-7696-452a-b0cc-8b70f01bafc3
  Args:
    source: Johann_Georg_of_Saxony
    target: Maria_Anna_of_Portugal
    relation: :hasMother
  AssignClass (9fcb0172-94cf-492a-9e23-b5de4962a391)
 Call ID: 9fcb0172-94cf-492a-9e23-b5de4962a391
  Args:
    type: :Woman
    source: Maria_II_of_Portugal
  AssignClass (25b8bbb9-ffab-44d8-882f-48e67b86c495)
 Call ID: 25b8bbb9-ffab-44d8-882f-48e67b86c495
  Args:
    type: :Person
    source: Maria_II_of_Portugal
  AssignClass (76db8187-a64a-4ecf-9f4d-7aed295ef204)
 Call ID: 76db8187-a64a-4ecf-9f4d-7aed295ef204
  Args:
    type: :Ancestor
    source: Maria_II_of_Portugal
  AssignClass (40cb81c9-5067-4302-8e7d-8cec53e9d078)
 Call ID: 40cb81c9-5067-4302-8e7d-8cec53e9d078
  Args:
    type: :Man
    source: Ferdinand_II_of_Portugal
  AssignClass (4744be50-a6c8-409f-9e6d-f1db023d5e86)
 Call ID: 4744be50-a6c8-409f-9e6d-f1db023d5e86
  Args:
    type: :Person
    source: Ferdinand_II_of_Portugal
  AssignClass (c51efe5d-09b3-4199-8222-6e93e6b09638)
 Call ID: c51efe5d-09b3-4199-8222-6e93e6b09638
  Args:
    type: :Ancestor
    source: Ferdinand_II_of_Portugal
  AddTriple (a0e614c8-7b48-4456-a6a7-dc5712269a80)
 Call ID: a0e614c8-7b48-4456-a6a7-dc5712269a80
  Args:
    source: Maria_Anna_of_Portugal
    target: Maria_II_of_Portugal
    relation: :hasMother
  AddTriple (1a97cccd-aafe-4b3c-9b97-c575c93853a4)
 Call ID: 1a97cccd-aafe-4b3c-9b97-c575c93853a4
  Args:
    target: Ferdinand_II_of_Portugal
    relation: :hasFather
    source: Maria_Anna_of_Portugal
  AssignClass (8df0c386-2e64-4740-98ed-a2727733f140)
 Call ID: 8df0c386-2e64-4740-98ed-a2727733f140
  Args:
    type: :Man
    source: Frederick_Augustus_III_of_Saxony
  AssignClass (60c18bad-c5a5-437c-9aa7-22f105f9a2cf)
 Call ID: 60c18bad-c5a5-437c-9aa7-22f105f9a2cf
  Args:
    type: :Person
    source: Frederick_Augustus_III_of_Saxony
  AddTriple (d98e650a-5a9c-4f5d-90fb-59d60a9d76d3)
 Call ID: d98e650a-5a9c-4f5d-90fb-59d60a9d76d3
  Args:
    source: Johann_Georg_of_Saxony
    target: Frederick_Augustus_III_of_Saxony
    relation: :hasBrother
  Finish (87648140-6894-4c33-b250-7085d4f114d6)
 Call ID: 87648140-6894-4c33-b250-7085d4f114d6
  Args: