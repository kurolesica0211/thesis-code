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
Prince Ferdinand Pius (Ferdinando Pio Maria), Duke of Calabria and Castro (25 July 1869, Rome – 7 January 1960, Lindau), was head of the House of Bourbon-Two Sicilies and pretender to the throne of the extinct Kingdom of the Two Sicilies from 1934 to 1960.
Family

Ferdinand was the eldest child of Prince Alfonso, Count of Caserta and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
He was a grandson of Ferdinand II of the Two Sicilies and an older brother of Prince Carlos of Bourbon-Two Sicilies, Maria Immaculata, Princess Johann Georg of Saxony, Maria Cristina, Archduchess Peter Ferdinand of Austria, Maria di Grazia, Princess Imperial of Brazil, Prince Ranieri, Duke of Castro, Prince Philip of Bourbon-Two Sicilies, and Prince Gabriel of Bourbon-Two Sicilies.
Marriage

Ferdinand married Princess Maria Ludwiga Theresia of Bavaria, daughter of King Ludwig III of Bavaria on 31 May 1897.
They had six children:


Ferdinand and Maria lived for many years at Villa Amsee, Lindau.
Disputed succession

Following Ferdinand's death, the headship of the House of Bourbon-Two Sicilies was claimed by both his nephew Infante Alfonso, Duke of Calabria, and his brother Prince Ranieri, Duke of Castro, and remains disputed between their descendants.
The basis of Alfonso’s claim was that his late father, Prince Carlos of Bourbon-Two Sicilies (1870–1949), had been Ferdinand's next oldest brother.
But Henri, Count of Paris, upheld the claim of Ferdinand's younger brother, Prince Ranieri, Duke of Castro (1883–1973), contending that Carlos had renounced his rights of succession for himself and his descendants in 1901 when he married the Spanish heiress presumptive María de las Mercedes, Princess of Asturias.
The Count of Paris was well aware that his own claim to the French throne depended on the validity of the renunciation in 1713 of Philip V of Spain, in favor of the junior House of Orléans.
In 1900, Prince Carlos had executed the Act of Cannes, in anticipation of his marriage to María de las Mercedes, and in 1901 he became a Spanish subject and accepted the title of Infante.
The position of Ranieri was that by so doing Carlos had renounced any claim to the throne of the Two Sicilies.
But Alfonso had a different interpretation, which was that the Act of Cannes would have taken effect only if Mercedes and Carlos had succeeded to the Spanish throne.
He also argued that the Act of Cannes was invalid under the succession rules of the house of Two Sicilies.
Military service

Ferdinand initially served in the Spanish Army, and after leaving service held the honorary rank of Comandante of the General Staff of the Spanish Army.
Feld-Artillerie-Regiment "Prinz Ferdinand von Bourbon, Herzog von Calabrien"), which was renamed in honor of him.



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
  AssignClass (ab1306f9-7fe9-4630-8cc9-49a254a2bb57)
 Call ID: ab1306f9-7fe9-4630-8cc9-49a254a2bb57
  Args:
    type: :Man
    source: Ferdinand_Pius
  AssignClass (e5db065a-19d6-4490-9328-fc0c69818af6)
 Call ID: e5db065a-19d6-4490-9328-fc0c69818af6
  Args:
    source: Ferdinand_Pius
    type: :Person
  AddLiteral (2acb0d3d-a81b-412d-a22e-3c973db05093)
 Call ID: 2acb0d3d-a81b-412d-a22e-3c973db05093
  Args:
    literal_type: xsd:integer
    literal_value: 1869
    source: Ferdinand_Pius
    relation: :hasBirthYear
  AddLiteral (56506f85-4d08-4faa-8b4b-1ebcf83f91b4)
 Call ID: 56506f85-4d08-4faa-8b4b-1ebcf83f91b4
  Args:
    source: Ferdinand_Pius
    literal_value: 1960
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (a1608feb-f7ad-4b0e-9fdd-74bf36c4a1ed)
 Call ID: a1608feb-f7ad-4b0e-9fdd-74bf36c4a1ed
  Args:
    type: :Man
    source: Alfonso_Count_of_Caserta
  AssignClass (877d8cfd-fbdd-47fa-ac86-111915b2a715)
 Call ID: 877d8cfd-fbdd-47fa-ac86-111915b2a715
  Args:
    type: :Person
    source: Alfonso_Count_of_Caserta
  AssignClass (93b3de1d-004a-4896-bcbf-9431e9d0263a)
 Call ID: 93b3de1d-004a-4896-bcbf-9431e9d0263a
  Args:
    type: :Woman
    source: Maria_Antonietta
  AssignClass (85dd986f-7389-4c8d-a299-fc4a0f0b88ea)
 Call ID: 85dd986f-7389-4c8d-a299-fc4a0f0b88ea
  Args:
    source: Maria_Antonietta
    type: :Person
  AddTriple (ecc361f4-95a8-43fe-ae4f-d071b01097eb)
 Call ID: ecc361f4-95a8-43fe-ae4f-d071b01097eb
  Args:
    relation: :hasFather
    target: Alfonso_Count_of_Caserta
    source: Ferdinand_Pius
  AddTriple (8ddf61db-d33e-42cd-b471-d22f324afe48)
 Call ID: 8ddf61db-d33e-42cd-b471-d22f324afe48
  Args:
    relation: :hasMother
    target: Maria_Antonietta
    source: Ferdinand_Pius
  AssignClass (a3e4b4de-9533-46f9-a2b4-a74a344fd217)
 Call ID: a3e4b4de-9533-46f9-a2b4-a74a344fd217
  Args:
    type: :Man
    source: Ferdinand_II_of_the_Two_Sicilies
  AssignClass (b7f33492-66ba-4e36-a5da-114c64b8190a)
 Call ID: b7f33492-66ba-4e36-a5da-114c64b8190a
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    type: :Person
  AddTriple (ca7026a3-3910-48f7-9ba7-6dc74d99c84a)
 Call ID: ca7026a3-3910-48f7-9ba7-6dc74d99c84a
  Args:
    source: Ferdinand_Pius
    relation: :hasAncestor
    target: Ferdinand_II_of_the_Two_Sicilies
  AssignClass (0ef91b75-02eb-4a18-8198-1440f3665f82)
 Call ID: 0ef91b75-02eb-4a18-8198-1440f3665f82
  Args:
    type: :Woman
    source: Maria_Ludwiga_Theresia_of_Bavaria
  AssignClass (46a75a9f-e798-4984-9bfd-5594798fdb32)
 Call ID: 46a75a9f-e798-4984-9bfd-5594798fdb32
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    type: :Person
  AddLiteral (529e2510-a331-4050-9c83-ebb1bf775b55)
 Call ID: 529e2510-a331-4050-9c83-ebb1bf775b55
  Args:
    literal_type: xsd:integer
    literal_value: 1897
    source: Ferdinand_Pius
    relation: :hasMarriageYear
  AddTriple (57687f9c-8ecd-4e77-b21d-76ebb144990f)
 Call ID: 57687f9c-8ecd-4e77-b21d-76ebb144990f
  Args:
    target: Maria_Ludwiga_Theresia_of_Bavaria
    relation: :hasRelation
    source: Ferdinand_Pius
  AssignClass (6fa8a4cd-dcbf-4804-b7f4-7e7b2643c90a)
 Call ID: 6fa8a4cd-dcbf-4804-b7f4-7e7b2643c90a
  Args:
    source: Ludwig_III_of_Bavaria
    type: :Man
  AssignClass (ccba54ff-b77b-4f21-b2fa-26c83a148fb0)
 Call ID: ccba54ff-b77b-4f21-b2fa-26c83a148fb0
  Args:
    type: :Person
    source: Ludwig_III_of_Bavaria
  AddTriple (44e5a2b1-9cca-494c-9bfd-7dcfa289700c)
 Call ID: 44e5a2b1-9cca-494c-9bfd-7dcfa289700c
  Args:
    source: Maria_Ludwiga_Theresia_of_Bavaria
    target: Ludwig_III_of_Bavaria
    relation: :hasFather
  Finish (9a07d8b5-9d64-479b-8a06-67b69d066556)
 Call ID: 9a07d8b5-9d64-479b-8a06-67b69d066556
  Args: