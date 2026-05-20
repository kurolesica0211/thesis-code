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
King Albert IIQueen Paola


Amedeo of Austria-Este (Habsburg-Lorraine)
Birth and family

Amedeo was born on 21 February 1986 at the Saint-Luc University Hospital in Woluwe-Saint-Lambert, Belgium, as the first child and elder son of Lorenz, Archduke of Austria-Este, and Princess Astrid of Belgium.
Amedeo himself is godfather to his cousin, Princess Elisabeth, Duchess of Brabant.
The couple's wedding was celebrated on 5 July 2014 in Rome's Basilica of Santa Maria in Trastevere, in the presence of the royal family (with the exception of his great-aunt Queen Fabiola), as well as members of the cadet branches of the House of Habsburg-Lorraine, including the bridegroom's grandmother, Margherita of Savoy, Dowager Archduchess of Austria-Este, and members of other dynasties, including Princess Margaretha of Luxembourg and her husband Prince Nikolaus of Liechtenstein, Princess Beatrice of York and Jean-Christophe, Prince Napoléon.
Titles and styles

All the children of Princess Astrid and Archduke Lorenz bear the title of "Prince(ss) of Belgium", with the style of "Royal Highness", by Belgian Royal Decree of 2 December 1991, which is distinct from their traditional Austro-Hungarian titles.



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
  AssignClass (cb15bba9-5cfc-476b-bfef-add862c95843)
 Call ID: cb15bba9-5cfc-476b-bfef-add862c95843
  Args:
    type: :Man
    source: Amedeo_of_Austria-Este
  AssignClass (71db5632-8ebc-4fb3-947c-9967a26cd209)
 Call ID: 71db5632-8ebc-4fb3-947c-9967a26cd209
  Args:
    type: :Man
    source: Lorenz_Archduke_of_Austria-Este
  AssignClass (2349ac54-7d1b-499d-84a4-9d47613cc89d)
 Call ID: 2349ac54-7d1b-499d-84a4-9d47613cc89d
  Args:
    type: :Woman
    source: Princess_Astrid_of_Belgium
  AddLiteral (1cb3e661-7af2-4f8b-b90e-4ad198073f2f)
 Call ID: 1cb3e661-7af2-4f8b-b90e-4ad198073f2f
  Args:
    literal_type: xsd:integer
    source: Amedeo_of_Austria-Este
    relation: :hasBirthYear
    literal_value: 1986
  AddTriple (e42ac8e5-d3c9-45dd-a3fd-a80b7d474952)
 Call ID: e42ac8e5-d3c9-45dd-a3fd-a80b7d474952
  Args:
    target: Lorenz_Archduke_of_Austria-Este
    source: Amedeo_of_Austria-Este
    relation: :hasFather
  AddTriple (134ce6a0-6d37-4d77-a8a2-56646209259f)
 Call ID: 134ce6a0-6d37-4d77-a8a2-56646209259f
  Args:
    target: Princess_Astrid_of_Belgium
    source: Amedeo_of_Austria-Este
    relation: :hasMother
  Finish (39fdaedf-76f9-40b2-8d5a-a462510e2a3e)
 Call ID: 39fdaedf-76f9-40b2-8d5a-a462510e2a3e
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

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Amedeo_of_Austria-Este a :Man ;
      :hasBirthYear 1986 ;
      :hasFather data:Lorenz_Archduke_of_Austria-Este ;
      :hasMother data:Princess_Astrid_of_Belgium .

  data:Lorenz_Archduke_of_Austria-Este a :Man .

  data:Princess_Astrid_of_Belgium a :Woman .



================================= Tool Message =================================

You have not used SHACL validation even once, though you should! Check your work with the SHACL tool!

================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (bd1ec39a-a624-439c-9202-41da616ef0de)
 Call ID: bd1ec39a-a624-439c-9202-41da616ef0de
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:6
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Lorenz_Archduke_of_Austria-Este is linked via hasFather but lacks the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: 'Lorenz_Archduke_of_Austria-Este', class: ':Ancestor')


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Princess_Astrid_of_Belgium is linked via hasMother but lacks the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: 'Princess_Astrid_of_Belgium', class: ':Ancestor')


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Lorenz_Archduke_of_Austria-Este is linked via hasFather but lacks the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: 'Lorenz_Archduke_of_Austria-Este', class: ':Ancestor')


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Princess_Astrid_of_Belgium is linked via hasMother but lacks the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: 'Princess_Astrid_of_Belgium', class: ':Ancestor')


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Lorenz_Archduke_of_Austria-Este is linked via hasFather but lacks the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: 'Lorenz_Archduke_of_Austria-Este', class: ':Ancestor')


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Princess_Astrid_of_Belgium is linked via hasMother but lacks the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: 'Princess_Astrid_of_Belgium', class: ':Ancestor')




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (61c2f5ed-eee5-4170-9948-ecc48a33cede)
 Call ID: 61c2f5ed-eee5-4170-9948-ecc48a33cede
  Args:
    source: Lorenz_Archduke_of_Austria-Este
    type: :Ancestor
  AssignClass (6ccd1ffc-efcc-444e-ba39-4e00bead5598)
 Call ID: 6ccd1ffc-efcc-444e-ba39-4e00bead5598
  Args:
    type: :Ancestor
    source: Princess_Astrid_of_Belgium
  AssignClass (0c287210-6423-4b5e-8732-d497359f8e0b)
 Call ID: 0c287210-6423-4b5e-8732-d497359f8e0b
  Args:
    source: Amedeo_of_Austria-Este
    type: :Person
  AssignClass (f268218d-f765-4569-bcc5-332c355c9a59)
 Call ID: f268218d-f765-4569-bcc5-332c355c9a59
  Args:
    type: :Person
    source: Lorenz_Archduke_of_Austria-Este
  AssignClass (776824b1-9c7c-4582-b85e-82737afb68d3)
 Call ID: 776824b1-9c7c-4582-b85e-82737afb68d3
  Args:
    type: :Person
    source: Princess_Astrid_of_Belgium
  ValidateShacl (e7d7dd86-52a0-47f3-bd01-c8c5b153f8ce)
 Call ID: e7d7dd86-52a0-47f3-bd01-c8c5b153f8ce
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

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Amedeo_of_Austria-Este a :Man,
          :Person ;
      :hasBirthYear 1986 ;
      :hasFather data:Lorenz_Archduke_of_Austria-Este ;
      :hasMother data:Princess_Astrid_of_Belgium .

  data:Lorenz_Archduke_of_Austria-Este a :Ancestor,
          :Man,
          :Person .

  data:Princess_Astrid_of_Belgium a :Ancestor,
          :Person,
          :Woman .



================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (e1e93ce5-9eff-4ac2-98ca-d1a8bd1f54d8)
 Call ID: e1e93ce5-9eff-4ac2-98ca-d1a8bd1f54d8
  Args: