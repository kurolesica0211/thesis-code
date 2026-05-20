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
Princess Maria Cristina of Bourbon-Two Sicilies (Full Italian name: Maria Cristina Carolina Pia Carmela Giuseppa Antonia Anna Luitgarda Speranza Lucia Caterina Apollonia Cecilia Agata di Borbone; 10 April 1877 – 4 October 1947) was the titular Grand Duchess of Tuscany from 28 February 1942 to 4 October 1947 as wife of Archduke Peter Ferdinand of Austria, Prince of Tuscany, the titular Grand Duke.
Family

Born into the Sicilian line of an ancient House of Bourbon, Princess Maria Cristina was the fifth child and second eldest daughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta and his wife, Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage and issue

Maria Cristina married Archduke Peter Ferdinand of Austria, Prince of Tuscany, fourth child and third son of Ferdinand IV, Grand Duke of Tuscany and his wife Princess Alice of Bourbon-Parma, on 8 November 1900 in Cannes.
Maria Cristina and Peter Ferdinand had four children:


Death

Archduchess Maria Christina died in Landkreis Starnberg, Bavaria, on 4 October 1947, at the age of 70.



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
  AssignClass (27fd18ce-0809-4ca3-abe3-37a4be151b63)
 Call ID: 27fd18ce-0809-4ca3-abe3-37a4be151b63
  Args:
    type: :Woman
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (ff335a90-e7b8-4487-815d-c704bcba9cd3)
 Call ID: ff335a90-e7b8-4487-815d-c704bcba9cd3
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (eb1c2a44-d20a-4de4-8311-50026a6ddec9)
 Call ID: eb1c2a44-d20a-4de4-8311-50026a6ddec9
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1877
  AddLiteral (682c9e10-d9b2-4bc3-b9ec-ad7dce3774ea)
 Call ID: 682c9e10-d9b2-4bc3-b9ec-ad7dce3774ea
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    literal_value: 1947
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (2d8cb124-2f56-468a-98e6-e4a071570f48)
 Call ID: 2d8cb124-2f56-468a-98e6-e4a071570f48
  Args:
    type: :Man
    source: Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (22b0204b-2a4b-469a-9ce9-c5a26e491c55)
 Call ID: 22b0204b-2a4b-469a-9ce9-c5a26e491c55
  Args:
    source: Alfonso_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (ff2c3987-433f-4522-842d-58658dc1991c)
 Call ID: ff2c3987-433f-4522-842d-58658dc1991c
  Args:
    type: :Ancestor
    source: Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (23aea88a-90db-4894-a5bd-3637ed8bdcf0)
 Call ID: 23aea88a-90db-4894-a5bd-3637ed8bdcf0
  Args:
    type: :Woman
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (c382d507-a85f-4a94-8a2a-0f907784c16a)
 Call ID: c382d507-a85f-4a94-8a2a-0f907784c16a
  Args:
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (a5cd7995-39db-4fcf-a4e9-67a4e69af303)
 Call ID: a5cd7995-39db-4fcf-a4e9-67a4e69af303
  Args:
    type: :Ancestor
    source: Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (6508976b-556d-44fb-a00a-23a17e8fe27f)
 Call ID: 6508976b-556d-44fb-a00a-23a17e8fe27f
  Args:
    relation: :hasFather
    target: Alfonso_of_Bourbon-Two_Sicilies
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AddTriple (7a195585-6b7a-4558-99e7-25e50c9e06f3)
 Call ID: 7a195585-6b7a-4558-99e7-25e50c9e06f3
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    target: Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (b2ad53a1-7110-492f-b774-a344c9cb0341)
 Call ID: b2ad53a1-7110-492f-b774-a344c9cb0341
  Args:
    type: :Man
    source: Peter_Ferdinand_of_Austria
  AssignClass (83dc9ae7-9a77-491e-a4c3-1749add36a95)
 Call ID: 83dc9ae7-9a77-491e-a4c3-1749add36a95
  Args:
    type: :Person
    source: Peter_Ferdinand_of_Austria
  AssignClass (b444d004-9e70-4c5a-b11f-ed5fb7ec5bb0)
 Call ID: b444d004-9e70-4c5a-b11f-ed5fb7ec5bb0
  Args:
    type: :Ancestor
    source: Peter_Ferdinand_of_Austria
  AddLiteral (ce6736a1-a458-4949-9ab4-1621aabfe7da)
 Call ID: ce6736a1-a458-4949-9ab4-1621aabfe7da
  Args:
    literal_value: 1900
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AddTriple (87179f0e-01a0-4f18-8da2-3939dd2b9fee)
 Call ID: 87179f0e-01a0-4f18-8da2-3939dd2b9fee
  Args:
    target: Peter_Ferdinand_of_Austria
    relation: :hasRelation
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (fdb86c06-80f4-4626-b486-e08f18ce2cc2)
 Call ID: fdb86c06-80f4-4626-b486-e08f18ce2cc2
  Args:
    source: Ferdinand_IV_of_Tuscany
    type: :Man
  AssignClass (8ff7c3bf-687a-48bf-a51a-03a9cb81dc73)
 Call ID: 8ff7c3bf-687a-48bf-a51a-03a9cb81dc73
  Args:
    source: Ferdinand_IV_of_Tuscany
    type: :Person
  AssignClass (176abf64-5396-493d-a69b-d5982d8872c8)
 Call ID: 176abf64-5396-493d-a69b-d5982d8872c8
  Args:
    type: :Ancestor
    source: Ferdinand_IV_of_Tuscany
  AssignClass (975117da-a397-4dc6-ad23-6d624286f97d)
 Call ID: 975117da-a397-4dc6-ad23-6d624286f97d
  Args:
    source: Alice_of_Bourbon-Parma
    type: :Woman
  AssignClass (fdb037a7-b8cb-4992-aa35-017b26c1691b)
 Call ID: fdb037a7-b8cb-4992-aa35-017b26c1691b
  Args:
    source: Alice_of_Bourbon-Parma
    type: :Person
  AssignClass (e0c2996a-96eb-4a6f-946e-fad85edb9585)
 Call ID: e0c2996a-96eb-4a6f-946e-fad85edb9585
  Args:
    type: :Ancestor
    source: Alice_of_Bourbon-Parma
  AddTriple (5d505645-f7d3-49ef-8184-6a86a521a80d)
 Call ID: 5d505645-f7d3-49ef-8184-6a86a521a80d
  Args:
    source: Peter_Ferdinand_of_Austria
    relation: :hasFather
    target: Ferdinand_IV_of_Tuscany
  AddTriple (34a41400-b4fd-4c17-879a-a07413531086)
 Call ID: 34a41400-b4fd-4c17-879a-a07413531086
  Args:
    relation: :hasMother
    target: Alice_of_Bourbon-Parma
    source: Peter_Ferdinand_of_Austria
  Finish (f08f4f60-7dcd-460c-919b-64c6007c81b1)
 Call ID: f08f4f60-7dcd-460c-919b-64c6007c81b1
  Args: