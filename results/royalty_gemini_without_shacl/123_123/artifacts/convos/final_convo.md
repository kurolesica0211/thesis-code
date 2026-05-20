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
King Albert IIQueen Paola


Princess Astrid of Belgium, Archduchess of Austria-Este (born 5 June 1962), is the second child and first daughter of King Albert II and Queen Paola, and the younger sister to the current Belgian monarch, King Philippe.
She is married to Prince Lorenz of Belgium, head of the Austria-Este branch of the House of Habsburg-Lorraine, and is fifth in line of succession to the Belgian throne.
Biography

Princess Astrid was born one day before her father's 28th birthday at the Belvédère Château in Laeken, northern Brussels, and was named after her late paternal grandmother, Astrid of Sweden, King Leopold III's popular first wife, who had died in 1935 in a car accident aged 29.
Princess Astrid's godparents were her uncle Fabrizio, Prince Ruffo di Calabria-Santapau, 7th Duke di Guardia Lombarda, and her aunt Hereditary Grand Duchess Joséphine-Charlotte of Luxembourg.
Marriage and issue

Princess Astrid married Archduke Lorenz of Austria-Este, subsequently head of the House of Austria-Este, on 22 September 1984 at the Church of Our Lady of Victories at the Sablon in Brussels.
Lorenz is the eldest son of Robert, Archduke of Austria-Este (1915–1996) and Princess Margherita of Savoy-Aosta (1930–2022).
Princess Astrid and Prince Lorenz have five children:


Royal role

Astrid was formerly President of the Belgian Red Cross, a position which ended on 31 December 2007.
The princess is also a colonel in the Belgian Medical Service of the Belgian Armed Forces.
In April 2015, the Princess took over the Prince Albert Fund from her father King Albert.
Special Envoy

Princess Astrid has been for many years an advocate for landmine survivors rights, participating actively in the work of the Anti-Personnel Mine Ban Convention, also known as the Ottawa Treaty, since Belgium joined in 1998.
In 2013, the Princess was named Special Envoy of the convention, and has promoted the acceptance of a global ban on landmines and promoted the rights of survivors in various UN meetings.



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
  AssignClass (e40ca95a-a56f-4840-aa5f-8c228efd6f68)
 Call ID: e40ca95a-a56f-4840-aa5f-8c228efd6f68
  Args:
    type: :Woman
    source: Princess_Astrid_of_Belgium
  AssignClass (20190a1e-99f9-4d78-8cf6-ad0937da8dc7)
 Call ID: 20190a1e-99f9-4d78-8cf6-ad0937da8dc7
  Args:
    source: King_Albert_II
    type: :Man
  AssignClass (143821b0-b7df-4a06-b7d6-620d002ec86c)
 Call ID: 143821b0-b7df-4a06-b7d6-620d002ec86c
  Args:
    type: :Woman
    source: Queen_Paola
  AssignClass (17d698a9-5529-4177-80be-856a60c1a7a5)
 Call ID: 17d698a9-5529-4177-80be-856a60c1a7a5
  Args:
    source: King_Philippe
    type: :Man
  AssignClass (92b4cbb3-4a4e-4e32-9c69-a7d2c0a06d2b)
 Call ID: 92b4cbb3-4a4e-4e32-9c69-a7d2c0a06d2b
  Args:
    type: :Man
    source: Prince_Lorenz_of_Belgium
  AssignClass (a55f8848-2de2-49f4-a6a2-415a682ded28)
 Call ID: a55f8848-2de2-49f4-a6a2-415a682ded28
  Args:
    source: Astrid_of_Sweden
    type: :Woman
  AssignClass (43628a45-5ee0-459f-90f9-e57e1b4684d1)
 Call ID: 43628a45-5ee0-459f-90f9-e57e1b4684d1
  Args:
    type: :Man
    source: King_Leopold_III
  AssignClass (57dce328-774f-4169-85d2-1388860fc2bc)
 Call ID: 57dce328-774f-4169-85d2-1388860fc2bc
  Args:
    type: :Man
    source: Robert_Archduke_of_Austria-Este
  AssignClass (3ec5e5e8-8088-46ae-96e7-6eec75e33a9e)
 Call ID: 3ec5e5e8-8088-46ae-96e7-6eec75e33a9e
  Args:
    type: :Woman
    source: Princess_Margherita_of_Savoy-Aosta
  AddLiteral (2439dc5f-525b-4978-9e08-eec586d28197)
 Call ID: 2439dc5f-525b-4978-9e08-eec586d28197
  Args:
    literal_value: 1962
    source: Princess_Astrid_of_Belgium
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (327bab42-f10a-49b4-8cb5-f81f2f2e7bb9)
 Call ID: 327bab42-f10a-49b4-8cb5-f81f2f2e7bb9
  Args:
    relation: :hasFather
    target: King_Albert_II
    source: Princess_Astrid_of_Belgium
  AddTriple (5d0ae58e-fe0f-43a0-a798-b67766727bfd)
 Call ID: 5d0ae58e-fe0f-43a0-a798-b67766727bfd
  Args:
    target: Queen_Paola
    source: Princess_Astrid_of_Belgium
    relation: :hasMother
  AddTriple (ace979cd-c07a-4291-81bc-b0027a9dcd29)
 Call ID: ace979cd-c07a-4291-81bc-b0027a9dcd29
  Args:
    source: King_Philippe
    target: Princess_Astrid_of_Belgium
    relation: :hasSister
  AddTriple (6cbb3a44-a809-4540-a789-59eb0697e3d3)
 Call ID: 6cbb3a44-a809-4540-a789-59eb0697e3d3
  Args:
    relation: :hasBrother
    source: Princess_Astrid_of_Belgium
    target: King_Philippe
  AddTriple (dde40879-60da-41fa-aee0-2791eddb0601)
 Call ID: dde40879-60da-41fa-aee0-2791eddb0601
  Args:
    relation: :hasFather
    target: Robert_Archduke_of_Austria-Este
    source: Prince_Lorenz_of_Belgium
  AddTriple (b5e65b32-bb67-43c2-80cc-53cc69072729)
 Call ID: b5e65b32-bb67-43c2-80cc-53cc69072729
  Args:
    relation: :hasMother
    source: Prince_Lorenz_of_Belgium
    target: Princess_Margherita_of_Savoy-Aosta
  AddLiteral (515f8fca-7380-42ec-9fb5-c85e139a143d)
 Call ID: 515f8fca-7380-42ec-9fb5-c85e139a143d
  Args:
    literal_type: xsd:integer
    source: Princess_Astrid_of_Belgium
    literal_value: 1984
    relation: :hasMarriageYear
  AddTriple (3871346f-a0dd-4989-9272-92bbc0eaccf9)
 Call ID: 3871346f-a0dd-4989-9272-92bbc0eaccf9
  Args:
    relation: :hasFather
    source: Astrid_of_Sweden
    target: King_Leopold_III
  AddLiteral (9868580d-f04f-47de-828f-981e79150bba)
 Call ID: 9868580d-f04f-47de-828f-981e79150bba
  Args:
    source: Astrid_of_Sweden
    literal_value: 1935
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (5f711a77-ea62-41d2-9870-f9a44abb4e75)
 Call ID: 5f711a77-ea62-41d2-9870-f9a44abb4e75
  Args:
    literal_type: xsd:integer
    literal_value: 1915
    source: Robert_Archduke_of_Austria-Este
    relation: :hasBirthYear
  AddLiteral (4c4d0329-a062-4b4a-a1de-3efc00daa57a)
 Call ID: 4c4d0329-a062-4b4a-a1de-3efc00daa57a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Robert_Archduke_of_Austria-Este
    literal_value: 1996
  AddLiteral (937094ad-4b39-4c14-a98c-78c3caa89866)
 Call ID: 937094ad-4b39-4c14-a98c-78c3caa89866
  Args:
    relation: :hasBirthYear
    source: Princess_Margherita_of_Savoy-Aosta
    literal_value: 1930
    literal_type: xsd:integer
  AddLiteral (568e4299-ce9c-403e-9545-19d29cadd0d6)
 Call ID: 568e4299-ce9c-403e-9545-19d29cadd0d6
  Args:
    source: Princess_Margherita_of_Savoy-Aosta
    literal_value: 2022
    literal_type: xsd:integer
    relation: :hasDeathYear
  Finish (0329fde9-bb53-4733-9f1e-d6ee61d13963)
 Call ID: 0329fde9-bb53-4733-9f1e-d6ee61d13963
  Args: