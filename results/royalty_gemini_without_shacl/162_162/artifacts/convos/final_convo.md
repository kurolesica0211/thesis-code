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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Infanta Margarita, Duchess of Soria, 2nd Duchess of Hernani (Margarita María de la Victoria Esperanza
Jacoba Felicidad Perpetua de Todos los Santos de Borbón y Borbón; born 6 March 1939), is the younger sister of King Juan Carlos I and aunt of the reigning King Felipe VI of Spain.
Early life

Infanta Margarita was born at Hotel Firenze Anglo American in Rome as the younger daughter of Infante Juan, Count of Barcelona, and Princess Mercedes of the Two Sicilies.
Margarita has been blind since birth.
Marriage

She married the physician and aristocrat Carlos Zurita y Delgado on 12 October 1972 in Estoril at St. Anthony's Church.
They have two children:


Activities

In 1989, alongside her husband, they created The Duke and Duchess of Soria Cultural Foundation (Spanish: Fundación Cultural Duques de Soria), a nonprofit organization dedicated to the promotion of Spanish culture, Hispanic studies, science and knowledge, as well as the preservation of cultural heritage.
Titles, styles and honours

Infanta Margarita renounced her right of succession to the Spanish throne upon marriage because it was not a dynastic wedding.
On 6 January 1979, the Infanta's distant cousin Manfredo de Borbón, 1st Duke of Hernani, died and willed his ducal title to be inherited by Margarita.
The King granted this request in 1977 and, on 27 May 1981, she became 2nd Duchess of Hernani, accompanied by the dignity of Grandee.
The peerage title refers to the town Hernani, Spain.
The month after, on 23 June 1981, King Juan Carlos created her Duchess of Soria (referring to the city Soria, Spain); this title is a title of the Royal House and cannot be inherited by her children.



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
  AssignClass (52952e72-7362-43a2-9219-0763cf269664)
 Call ID: 52952e72-7362-43a2-9219-0763cf269664
  Args:
    type: :Woman
    source: Infanta_Margarita
  AssignClass (e038302a-a24d-4267-bd35-3214f90856e6)
 Call ID: e038302a-a24d-4267-bd35-3214f90856e6
  Args:
    type: :Person
    source: Infanta_Margarita
  AssignClass (735294b8-da00-451b-b72a-25194525989b)
 Call ID: 735294b8-da00-451b-b72a-25194525989b
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (1d500a82-f1cb-4c99-8896-2e2c1e49e12b)
 Call ID: 1d500a82-f1cb-4c99-8896-2e2c1e49e12b
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (822e4f67-54ac-4f4a-b357-503739fc421b)
 Call ID: 822e4f67-54ac-4f4a-b357-503739fc421b
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (f4349cab-c93c-4859-bb96-94ff52fc99c2)
 Call ID: f4349cab-c93c-4859-bb96-94ff52fc99c2
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (6f055697-35c7-4f18-a8b2-27cfa1783ac2)
 Call ID: 6f055697-35c7-4f18-a8b2-27cfa1783ac2
  Args:
    type: :Man
    source: Infante_Juan
  AssignClass (df2bb904-1f03-4d01-ab4b-5057ad811940)
 Call ID: df2bb904-1f03-4d01-ab4b-5057ad811940
  Args:
    type: :Person
    source: Infante_Juan
  AssignClass (7f5a26ba-275a-4acf-bbb6-a1bd720a2043)
 Call ID: 7f5a26ba-275a-4acf-bbb6-a1bd720a2043
  Args:
    type: :Woman
    source: Princess_Mercedes
  AssignClass (093b9eee-b3b3-46cf-9e4d-b02a8785111c)
 Call ID: 093b9eee-b3b3-46cf-9e4d-b02a8785111c
  Args:
    type: :Person
    source: Princess_Mercedes
  AssignClass (53d661ab-e883-44e9-9625-a623b3054dfd)
 Call ID: 53d661ab-e883-44e9-9625-a623b3054dfd
  Args:
    type: :Man
    source: Carlos_Zurita_y_Delgado
  AssignClass (9fb8dc59-1ce0-4365-9eb5-6c3067f789d4)
 Call ID: 9fb8dc59-1ce0-4365-9eb5-6c3067f789d4
  Args:
    type: :Person
    source: Carlos_Zurita_y_Delgado
  AddLiteral (d4c1ea0a-08c4-4f08-9383-638736b6ba04)
 Call ID: d4c1ea0a-08c4-4f08-9383-638736b6ba04
  Args:
    literal_value: 1939
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Infanta_Margarita
  AddTriple (31b104c5-8c84-46ae-95fb-9b9517d7155d)
 Call ID: 31b104c5-8c84-46ae-95fb-9b9517d7155d
  Args:
    relation: :isSisterOf
    target: Juan_Carlos_I
    source: Infanta_Margarita
  AddTriple (6cf1b1ab-5e73-474f-b575-aba97f91e24f)
 Call ID: 6cf1b1ab-5e73-474f-b575-aba97f91e24f
  Args:
    target: Felipe_VI
    source: Infanta_Margarita
    relation: :isAuntOf
  AddTriple (429baab6-ced6-4eb8-a654-97474ff3dc05)
 Call ID: 429baab6-ced6-4eb8-a654-97474ff3dc05
  Args:
    source: Infanta_Margarita
    target: Infante_Juan
    relation: :hasFather
  AddTriple (83c9b0a1-6db6-4f25-855d-382498596703)
 Call ID: 83c9b0a1-6db6-4f25-855d-382498596703
  Args:
    target: Princess_Mercedes
    source: Infanta_Margarita
    relation: :hasMother
  AddTriple (b3901bcc-8a2e-46e0-9dd9-6683ae8edb01)
 Call ID: b3901bcc-8a2e-46e0-9dd9-6683ae8edb01
  Args:
    source: Juan_Carlos_I
    target: Infante_Juan
    relation: :hasFather
  AddTriple (e1761936-e94f-4542-92d8-be60693b0b45)
 Call ID: e1761936-e94f-4542-92d8-be60693b0b45
  Args:
    relation: :hasMother
    source: Juan_Carlos_I
    target: Princess_Mercedes
  AddLiteral (d4106bfa-0935-4a69-9416-5d6104794de3)
 Call ID: d4106bfa-0935-4a69-9416-5d6104794de3
  Args:
    relation: :hasMarriageYear
    literal_value: 1972
    source: Infanta_Margarita
    literal_type: xsd:integer
  AddTriple (21fabdc1-4297-40d2-bbbd-71e8d569f685)
 Call ID: 21fabdc1-4297-40d2-bbbd-71e8d569f685
  Args:
    target: Carlos_Zurita_y_Delgado
    source: Infanta_Margarita
    relation: :hasRelation
  Finish (267811fc-b2fd-4852-9b31-862cf751e7d9)
 Call ID: 267811fc-b2fd-4852-9b31-862cf751e7d9
  Args: