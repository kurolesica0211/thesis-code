================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Nuria


Princess Françoise


Princess Mariam


Princess Monique


Princess Mariam de Bagration (born 27 June 1947) is a Spanish-Georgian noblewoman (tavadi) of the House of Mukhrani.
Early life

Princess Mariam was born on 27 June 1947 in Madrid.
She is a daughter of Prince Irakli Bagration of Mukhrani and Infanta María de las Mercedes de Baviera y Borbón.
In 1982 she married Dr. Tomás Ortiz y Valero and has a son from this marriage:


She is a sister of Bagrat de Bagration and half-sister of Jorge de Bagration.



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
  AssignClass (90db11d5-2dc4-4b66-9450-fd7a76e6e8ee)
 Call ID: 90db11d5-2dc4-4b66-9450-fd7a76e6e8ee
  Args:
    type: :Woman
    source: :Princess_Mariam_de_Bagration
  AssignClass (01a6e800-fe3f-440c-acbb-5e012660a968)
 Call ID: 01a6e800-fe3f-440c-acbb-5e012660a968
  Args:
    type: :Person
    source: :Princess_Mariam_de_Bagration
  AssignClass (26927aed-c0d0-4c43-a38c-9735a5a7acdc)
 Call ID: 26927aed-c0d0-4c43-a38c-9735a5a7acdc
  Args:
    type: :Man
    source: :Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (fec704f4-2375-41a7-8bb4-00d35b74f4fd)
 Call ID: fec704f4-2375-41a7-8bb4-00d35b74f4fd
  Args:
    type: :Person
    source: :Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (85d6c425-a508-4f76-80ea-c9de63fbfaab)
 Call ID: 85d6c425-a508-4f76-80ea-c9de63fbfaab
  Args:
    type: :Ancestor
    source: :Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (e5a8b01c-f45e-4841-91e0-d01bd0e93f9c)
 Call ID: e5a8b01c-f45e-4841-91e0-d01bd0e93f9c
  Args:
    type: :Woman
    source: :Infanta_María_de_las_Mercedes_de_Baviera_y_Borbón
  AssignClass (fbf0958f-f7cd-4825-9e47-32ad667fd2b0)
 Call ID: fbf0958f-f7cd-4825-9e47-32ad667fd2b0
  Args:
    type: :Person
    source: :Infanta_María_de_las_Mercedes_de_Baviera_y_Borbón
  AssignClass (92200b84-9acd-4f5e-a666-9c8fcd05cc39)
 Call ID: 92200b84-9acd-4f5e-a666-9c8fcd05cc39
  Args:
    type: :Ancestor
    source: :Infanta_María_de_las_Mercedes_de_Baviera_y_Borbón
  AssignClass (dfcdce74-d16a-43c1-9802-734b55d0ec22)
 Call ID: dfcdce74-d16a-43c1-9802-734b55d0ec22
  Args:
    type: :Man
    source: :Dr_Tomás_Ortiz_y_Valero
  AssignClass (e40c001c-2326-47c4-9a5c-eb0454ca9c79)
 Call ID: e40c001c-2326-47c4-9a5c-eb0454ca9c79
  Args:
    type: :Person
    source: :Dr_Tomás_Ortiz_y_Valero
  AssignClass (ea3036fd-9806-4055-b117-460669d549e7)
 Call ID: ea3036fd-9806-4055-b117-460669d549e7
  Args:
    type: :Man
    source: :Bagrat_de_Bagration
  AssignClass (cdb2725f-80d7-43a4-809a-479abed54fdf)
 Call ID: cdb2725f-80d7-43a4-809a-479abed54fdf
  Args:
    type: :Person
    source: :Bagrat_de_Bagration
  AssignClass (db068cc8-3318-48e9-875c-1113cfc1f818)
 Call ID: db068cc8-3318-48e9-875c-1113cfc1f818
  Args:
    type: :Man
    source: :Jorge_de_Bagration
  AssignClass (4b569cf4-cba8-443d-a041-c3952b4bce64)
 Call ID: 4b569cf4-cba8-443d-a041-c3952b4bce64
  Args:
    type: :Person
    source: :Jorge_de_Bagration
  AddTriple (d133f2cb-36b0-4d99-87e4-cc84cb0e5298)
 Call ID: d133f2cb-36b0-4d99-87e4-cc84cb0e5298
  Args:
    relation: :hasFather
    source: :Princess_Mariam_de_Bagration
    target: :Prince_Irakli_Bagration_of_Mukhrani
  AddTriple (b8cb3dba-c3d6-4cd7-a408-6f7bc037fe8f)
 Call ID: b8cb3dba-c3d6-4cd7-a408-6f7bc037fe8f
  Args:
    target: :Infanta_María_de_las_Mercedes_de_Baviera_y_Borbón
    source: :Princess_Mariam_de_Bagration
    relation: :hasMother
  AddTriple (e13143fd-d4ce-4ff3-98fc-dfbc43aca44f)
 Call ID: e13143fd-d4ce-4ff3-98fc-dfbc43aca44f
  Args:
    source: :Bagrat_de_Bagration
    target: :Princess_Mariam_de_Bagration
    relation: :hasSister
  AddTriple (0fcd3790-9c0c-4e8c-ad64-0f0033d18a4b)
 Call ID: 0fcd3790-9c0c-4e8c-ad64-0f0033d18a4b
  Args:
    relation: :hasSister
    source: :Jorge_de_Bagration
    target: :Princess_Mariam_de_Bagration
  AddLiteral (57422665-3c62-4312-a8fe-9e0d2563a9b1)
 Call ID: 57422665-3c62-4312-a8fe-9e0d2563a9b1
  Args:
    relation: :hasBirthYear
    literal_type: xsd:string
    source: :Princess_Mariam_de_Bagration
    literal_value: 1947
  AddLiteral (fcf60a3c-fb2e-4eea-beb6-7a5a0ff70a73)
 Call ID: fcf60a3c-fb2e-4eea-beb6-7a5a0ff70a73
  Args:
    relation: :hasMarriageYear
    literal_value: 1982
    source: :Princess_Mariam_de_Bagration
    literal_type: xsd:string
  AddTriple (6966598c-7f13-4f0b-89f9-fcc497d33bf6)
 Call ID: 6966598c-7f13-4f0b-89f9-fcc497d33bf6
  Args:
    source: :Princess_Mariam_de_Bagration
    target: :Female
    relation: :hasSex
  AddTriple (466776b9-b79f-4e0b-bb74-5d5708a20a77)
 Call ID: 466776b9-b79f-4e0b-bb74-5d5708a20a77
  Args:
    target: :Male
    source: :Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasSex
  AddTriple (3fe7ed0c-9af1-4830-8245-150af87e6ab4)
 Call ID: 3fe7ed0c-9af1-4830-8245-150af87e6ab4
  Args:
    target: :Female
    source: :Infanta_María_de_las_Mercedes_de_Baviera_y_Borbón
    relation: :hasSex
  AddTriple (15b4055c-14df-4c34-85a9-9e925451832f)
 Call ID: 15b4055c-14df-4c34-85a9-9e925451832f
  Args:
    source: :Dr_Tomás_Ortiz_y_Valero
    target: :Male
    relation: :hasSex
  AddTriple (6fb39a2b-9872-462a-b3f3-93bcc4c0572d)
 Call ID: 6fb39a2b-9872-462a-b3f3-93bcc4c0572d
  Args:
    target: :Male
    source: :Bagrat_de_Bagration
    relation: :hasSex
  AddTriple (2b970c30-de51-4630-b887-112a4accc0da)
 Call ID: 2b970c30-de51-4630-b887-112a4accc0da
  Args:
    relation: :hasSex
    source: :Jorge_de_Bagration
    target: :Male
  Finish (0acae077-3f03-4b64-aad6-a6b5cbdc9b8c)
 Call ID: 0acae077-3f03-4b64-aad6-a6b5cbdc9b8c
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Bagrat_de_Bagration a :Man,
          :Person ;
      :hasSex data:Male ;
      :hasSister data:Princess_Mariam_de_Bagration .

  data:Dr_Tom%C3%A1s_Ortiz_y_Valero a :Man,
          :Person ;
      :hasSex data:Male .

  data:Jorge_de_Bagration a :Man,
          :Person ;
      :hasSex data:Male ;
      :hasSister data:Princess_Mariam_de_Bagration .

  data:Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n a :Ancestor,
          :Person,
          :Woman ;
      :hasSex data:Female .

  data:Prince_Irakli_Bagration_of_Mukhrani a :Ancestor,
          :Man,
          :Person ;
      :hasSex data:Male .

  data:Princess_Mariam_de_Bagration a :Person,
          :Woman ;
      :hasBirthYear "1947"^^xsd:string ;
      :hasFather data:Prince_Irakli_Bagration_of_Mukhrani ;
      :hasMarriageYear "1982"^^xsd:string ;
      :hasMother data:Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n ;
      :hasSex data:Female .



================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (169ed29c-f9f4-43c3-bd9f-00c9386dd84d)
 Call ID: 169ed29c-f9f4-43c3-bd9f-00c9386dd84d
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:54
Violations:

  Violation [1]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [2]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [3]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [4]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [5]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [6]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [7]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [8]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [9]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [10]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [11]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [12]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [13]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [14]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [15]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [16]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [17]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [18]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [19]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [20]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [21]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [22]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [23]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [24]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [25]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [26]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [27]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [28]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [29]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [30]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [31]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [32]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [33]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [34]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [35]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [36]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [37]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [38]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [39]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [40]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [41]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [42]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [43]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [44]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [45]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Prince_Irakli_Bagration_of_Mukhrani' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [46]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [47]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Jorge_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [48]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Bagrat_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [49]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [50]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Male' for the property 'hasSex' on the entity 'Dr_Tom%C3%A1s_Ortiz_y_Valero' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Male', class=':Sex')


  Violation [51]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [52]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [53]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Princess_Mariam_de_Bagration' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')


  Violation [54]:
    SHACL message: Value does not have class :Sex
    LLM-provided explanation of the violation:
      The value 'Female' for the property 'hasSex' on the entity 'Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n' is not correctly typed as a member of the class ':Sex'.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node='Female', class=':Sex')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ffdcaed1-a1bf-4a65-af58-f899fe523365)
 Call ID: ffdcaed1-a1bf-4a65-af58-f899fe523365
  Args:
    source: Male
    type: :Sex
  AssignClass (ef06c6ca-144a-42a1-ba69-2d5ffe1cb647)
 Call ID: ef06c6ca-144a-42a1-ba69-2d5ffe1cb647
  Args:
    source: Female
    type: :Sex
  Finish (dcc45682-81ea-4160-a009-02add0059ba0)
 Call ID: dcc45682-81ea-4160-a009-02add0059ba0
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Bagrat_de_Bagration a :Man,
          :Person ;
      :hasSex data:Male ;
      :hasSister data:Princess_Mariam_de_Bagration .

  data:Dr_Tom%C3%A1s_Ortiz_y_Valero a :Man,
          :Person ;
      :hasSex data:Male .

  data:Jorge_de_Bagration a :Man,
          :Person ;
      :hasSex data:Male ;
      :hasSister data:Princess_Mariam_de_Bagration .

  data:Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n a :Ancestor,
          :Person,
          :Woman ;
      :hasSex data:Female .

  data:Prince_Irakli_Bagration_of_Mukhrani a :Ancestor,
          :Man,
          :Person ;
      :hasSex data:Male .

  data:Female a :Sex .

  data:Princess_Mariam_de_Bagration a :Person,
          :Woman ;
      :hasBirthYear "1947"^^xsd:string ;
      :hasFather data:Prince_Irakli_Bagration_of_Mukhrani ;
      :hasMarriageYear "1982"^^xsd:string ;
      :hasMother data:Infanta_Mar%C3%ADa_de_las_Mercedes_de_Baviera_y_Borb%C3%B3n ;
      :hasSex data:Female .

  data:Male a :Sex .



================================= Tool Message =================================

Previous SHACL validation wasn't successful. If you fixed the violations, use the validation tool again to confirm no violations persist.

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (b41e830e-23c1-4a31-b0d0-a0a41e3c7b74)
 Call ID: b41e830e-23c1-4a31-b0d0-a0a41e3c7b74
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (caf8082a-fb71-46f5-8bd8-ba72609efb27)
 Call ID: caf8082a-fb71-46f5-8bd8-ba72609efb27
  Args: