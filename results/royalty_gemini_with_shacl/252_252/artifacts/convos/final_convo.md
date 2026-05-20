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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Count Claus-Casimir of Orange-Nassau, Jonkheer van Amsberg (Claus-Casimir Bernhard Marius Max; born 21 March 2004), is the second child of Prince Constantijn and Princess Laurentien of the Netherlands and their only son.
Claus-Casimir's godparents are King Willem-Alexander, Prince Maurits of Orange-Nassau, van Vollenhoven, Ed P. Spanjaard, and Countess Tatiana Razumovsky von Wigstein.
Claus-Casimir grew up in Brussels before moving to The Hague in 2015.
After attending high school at Vrijzinnig Christelijk Lyceum (VCL) in The Hague, Claus-Casimir moved to Scotland in 2020 to attend Gordonstoun School, leaving in 2022.
Titles and styles

By royal decree of 11 May 2001 (nr. 227), it was determined that the children born from the marriage of Prince Constantijn and Princess Laurentien of the Netherlands would bear the title Count/Countess of Orange‐Nassau and the honorific Jonkheer/Jonkvrouwe van Amsberg with the surname Van Oranje-Nassau van Amsberg.
Upon the abdication of Queen Beatrix on 30 April 2013, the children of Prince Constantijn and Princess Laurentien ceased to be members of the Royal House, although they continue to be members of the royal family and in the line of succession to the Dutch throne.



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
  AssignClass (a5a7ff79-466a-41d3-9596-f1bd910ec0de)
 Call ID: a5a7ff79-466a-41d3-9596-f1bd910ec0de
  Args:
    type: :Man
    source: :Claus-Casimir_of_Orange-Nassau
  AssignClass (3ac56ac6-54b2-4a62-8f63-e3b0dbe8330f)
 Call ID: 3ac56ac6-54b2-4a62-8f63-e3b0dbe8330f
  Args:
    type: :Person
    source: :Claus-Casimir_of_Orange-Nassau
  AssignClass (b5bba877-ce77-4fc4-b6b8-fb5512580be5)
 Call ID: b5bba877-ce77-4fc4-b6b8-fb5512580be5
  Args:
    type: :Man
    source: :Prince_Constantijn
  AssignClass (594efd6d-c69c-43a6-ab25-578175e4a0d6)
 Call ID: 594efd6d-c69c-43a6-ab25-578175e4a0d6
  Args:
    type: :Person
    source: :Prince_Constantijn
  AssignClass (62e530e5-33b4-4708-b77c-c760f86ac030)
 Call ID: 62e530e5-33b4-4708-b77c-c760f86ac030
  Args:
    type: :Woman
    source: :Princess_Laurentien
  AssignClass (5fd1dd49-cffd-4b61-8400-19f87f3f0645)
 Call ID: 5fd1dd49-cffd-4b61-8400-19f87f3f0645
  Args:
    type: :Person
    source: :Princess_Laurentien
  AddLiteral (93d9d654-114b-4bc0-aa28-e163c84e2d50)
 Call ID: 93d9d654-114b-4bc0-aa28-e163c84e2d50
  Args:
    relation: :hasBirthYear
    literal_value: 2004
    source: :Claus-Casimir_of_Orange-Nassau
    literal_type: xsd:integer
  AddTriple (a17ae95a-6909-45fa-a245-25fa7ff6b6e7)
 Call ID: a17ae95a-6909-45fa-a245-25fa7ff6b6e7
  Args:
    source: :Claus-Casimir_of_Orange-Nassau
    relation: :hasFather
    target: :Prince_Constantijn
  AddTriple (39ec88af-3dab-4bde-a03e-626b8891a176)
 Call ID: 39ec88af-3dab-4bde-a03e-626b8891a176
  Args:
    relation: :hasMother
    target: :Princess_Laurentien
    source: :Claus-Casimir_of_Orange-Nassau
  Finish (3aac9c22-65a8-4fbd-9233-bab52bb8b85a)
 Call ID: 3aac9c22-65a8-4fbd-9233-bab52bb8b85a
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

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Claus-Casimir_of_Orange-Nassau a :Man,
          :Person ;
      :hasBirthYear 2004 ;
      :hasFather data:Prince_Constantijn ;
      :hasMother data:Princess_Laurentien .

  data:Prince_Constantijn a :Man,
          :Person .

  data:Princess_Laurentien a :Person,
          :Woman .



================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (64fca18b-252a-44ca-afcf-3545986a58f6)
 Call ID: 64fca18b-252a-44ca-afcf-3545986a58f6
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:6
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Prince_Constantijn' is assigned as the father of 'Claus-Casimir_of_Orange-Nassau', but it is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      Use 'AssignClass' to add ':Ancestor' to 'Prince_Constantijn'.


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Princess_Laurentien' is assigned as the mother of 'Claus-Casimir_of_Orange-Nassau', but it is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      Use 'AssignClass' to add ':Ancestor' to 'Princess_Laurentien'.


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Prince_Constantijn' is assigned as the father of 'Claus-Casimir_of_Orange-Nassau', but it is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      Use 'AssignClass' to add ':Ancestor' to 'Prince_Constantijn'.


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Princess_Laurentien' is assigned as the mother of 'Claus-Casimir_of_Orange-Nassau', but it is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      Use 'AssignClass' to add ':Ancestor' to 'Princess_Laurentien'.


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node 'Prince_Constantijn' is assigned as the father of 'Claus-Casimir_of_Orange-Nassau', but it is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      Use 'AssignClass' to add ':Ancestor' to 'Prince_Constantijn'.


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node 'Princess_Laurentien' is assigned as the mother of 'Claus-Casimir_of_Orange-Nassau', but it is missing the required class ':Ancestor'.
    LLM-provided instruction on how to handle the violation:
      Use 'AssignClass' to add ':Ancestor' to 'Princess_Laurentien'.




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (64cb30b3-7668-4729-9414-935f75450259)
 Call ID: 64cb30b3-7668-4729-9414-935f75450259
  Args:
    source: :Prince_Constantijn
    type: :Ancestor
  AssignClass (96dda093-fcf9-475c-ab48-ed06c0183296)
 Call ID: 96dda093-fcf9-475c-ab48-ed06c0183296
  Args:
    source: :Princess_Laurentien
    type: :Ancestor
  ValidateShacl (18590dfa-7869-443e-ad01-0e12e0a6877e)
 Call ID: 18590dfa-7869-443e-ad01-0e12e0a6877e
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Claus-Casimir_of_Orange-Nassau a :Man,
          :Person ;
      :hasBirthYear 2004 ;
      :hasFather data:Prince_Constantijn ;
      :hasMother data:Princess_Laurentien .

  data:Prince_Constantijn a :Ancestor,
          :Man,
          :Person .

  data:Princess_Laurentien a :Ancestor,
          :Person,
          :Woman .



================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (adc29fbf-77ef-401b-9d62-1af65d0d8105)
 Call ID: adc29fbf-77ef-401b-9d62-1af65d0d8105
  Args: