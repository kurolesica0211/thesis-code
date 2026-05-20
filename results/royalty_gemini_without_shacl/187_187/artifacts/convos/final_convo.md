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
Infanta María Teresa of Spain (Spanish: María Teresa Isabel Eugenia del Patrocinio Diega de Borbón y Habsburgo, Infanta de España; 12 November 1882 – 23 September 1912) was the second eldest child and daughter of Alfonso XII of Spain and his second wife Maria Christina of Austria.
Maria Teresa was an Infanta of Spain and a member of the House of Bourbon by birth.
Marriage and issue

Maria Teresa married her first cousin, Prince Ferdinand of Bavaria, Infante of Spain, eldest son and child of Prince Ludwig Ferdinand of Bavaria and his wife Infanta María de la Paz of Spain, on 12 January 1906 in Madrid.
Maria Teresa and Ferdinand had four children:


She passed away after giving birth to her last child.



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
  AssignClass (6040d716-bfc1-486e-8cf6-a037f2c16c78)
 Call ID: 6040d716-bfc1-486e-8cf6-a037f2c16c78
  Args:
    type: :Person
    source: Infanta_María_Teresa_of_Spain
  AssignClass (6fd0b254-b454-4e47-bf2e-3574d6ac3d33)
 Call ID: 6fd0b254-b454-4e47-bf2e-3574d6ac3d33
  Args:
    type: :Woman
    source: Infanta_María_Teresa_of_Spain
  AssignClass (5231b521-aec6-4549-be71-4fe37823dbf4)
 Call ID: 5231b521-aec6-4549-be71-4fe37823dbf4
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (c9649779-afbf-424f-b3ca-6bb12e341e7f)
 Call ID: c9649779-afbf-424f-b3ca-6bb12e341e7f
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (e840488f-2204-4f2f-bf06-aea9e4b7f68f)
 Call ID: e840488f-2204-4f2f-bf06-aea9e4b7f68f
  Args:
    type: :Person
    source: Maria_Christina_of_Austria
  AssignClass (14e37ebf-dca1-41b0-b963-8d062eb5b930)
 Call ID: 14e37ebf-dca1-41b0-b963-8d062eb5b930
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AssignClass (ccc32fbc-170a-4c9b-9d14-24936ba8db05)
 Call ID: ccc32fbc-170a-4c9b-9d14-24936ba8db05
  Args:
    type: :Person
    source: Prince_Ferdinand_of_Bavaria
  AssignClass (08c2646b-d875-4e41-9ed2-4a49d6855f41)
 Call ID: 08c2646b-d875-4e41-9ed2-4a49d6855f41
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Bavaria
  AssignClass (421aa00d-adbf-49ca-a4ff-6ea0a47d6cb9)
 Call ID: 421aa00d-adbf-49ca-a4ff-6ea0a47d6cb9
  Args:
    type: :Person
    source: Prince_Ludwig_Ferdinand_of_Bavaria
  AssignClass (4dab29b8-e115-40a6-9572-3b19842ae5af)
 Call ID: 4dab29b8-e115-40a6-9572-3b19842ae5af
  Args:
    type: :Man
    source: Prince_Ludwig_Ferdinand_of_Bavaria
  AssignClass (fcdaca55-1058-492c-af8a-5012bcbf29dd)
 Call ID: fcdaca55-1058-492c-af8a-5012bcbf29dd
  Args:
    type: :Person
    source: Infanta_María_de_la_Paz_of_Spain
  AssignClass (3dd2a4ad-2eb4-484a-8795-b1186b91690f)
 Call ID: 3dd2a4ad-2eb4-484a-8795-b1186b91690f
  Args:
    type: :Woman
    source: Infanta_María_de_la_Paz_of_Spain
  AddLiteral (9bfab13d-522a-4d3f-9006-6b64c5889bce)
 Call ID: 9bfab13d-522a-4d3f-9006-6b64c5889bce
  Args:
    source: Infanta_María_Teresa_of_Spain
    literal_type: xsd:integer
    literal_value: 1882
    relation: :hasBirthYear
  AddLiteral (97395a72-bdf5-4e2a-982e-673acf7f17e5)
 Call ID: 97395a72-bdf5-4e2a-982e-673acf7f17e5
  Args:
    relation: :hasDeathYear
    literal_value: 1912
    literal_type: xsd:integer
    source: Infanta_María_Teresa_of_Spain
  AddTriple (34fe2c77-6157-4052-83be-15ef8a3bfa76)
 Call ID: 34fe2c77-6157-4052-83be-15ef8a3bfa76
  Args:
    relation: :hasFather
    target: Alfonso_XII_of_Spain
    source: Infanta_María_Teresa_of_Spain
  AddTriple (846c38ff-7486-4595-bec3-5d73058b2695)
 Call ID: 846c38ff-7486-4595-bec3-5d73058b2695
  Args:
    source: Infanta_María_Teresa_of_Spain
    target: Maria_Christina_of_Austria
    relation: :hasMother
  AddLiteral (628f6abb-f048-49ae-8851-11e418266c16)
 Call ID: 628f6abb-f048-49ae-8851-11e418266c16
  Args:
    literal_value: 1906
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Infanta_María_Teresa_of_Spain
  AddTriple (d0e97b63-0948-481e-ace9-75879477eed1)
 Call ID: d0e97b63-0948-481e-ace9-75879477eed1
  Args:
    target: Prince_Ludwig_Ferdinand_of_Bavaria
    relation: :hasFather
    source: Prince_Ferdinand_of_Bavaria
  AddTriple (20d66dd1-c1f8-423e-98f5-8c539cc8d39c)
 Call ID: 20d66dd1-c1f8-423e-98f5-8c539cc8d39c
  Args:
    target: Infanta_María_de_la_Paz_of_Spain
    relation: :hasMother
    source: Prince_Ferdinand_of_Bavaria
  Finish (83be5b5f-aafa-4a94-9a2e-9497bdf78a7d)
 Call ID: 83be5b5f-aafa-4a94-9a2e-9497bdf78a7d
  Args: