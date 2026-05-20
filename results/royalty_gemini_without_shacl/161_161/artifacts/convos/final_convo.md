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
Amélie of Orléans (French: Marie Amélie Louise Hélène; 28 September 1865 – 25 October 1951) was the last Queen of Portugal as the wife of Carlos I of Portugal.
She was regent of Portugal during the absence of her husband in 1895.
She was the eldest daughter of Prince Philippe, Count of Paris, and Princess Marie Isabelle d'Orléans, and a "Princess of Orléans" by birth.
Amélie's paternal grandparents were Prince Ferdinand Philippe, Duke of Orléans, and Duchess Helena of Mecklenburg-Schwerin.
Her maternal grandparents were Prince Antoine, Duke of Montpensier, and the Infanta Luisa Fernanda of Spain.
The Dukes of Orléans and Montpensier were siblings, both sons of King Louis-Philippe I of France, and Maria Amalia of the Two Sicilies.
Marriage and issue

On 22 May 1886, Amélie married Carlos, Prince Royal of Portugal.
He was the eldest son of King Luís I of Portugal and Maria Pia of Savoy.
At first, the marriage was not popular and Queen Maria Pia was expecting to marry Carlos to Archduchess Marie Valerie of Austria, Princess Mathilde of Saxony, Princess Viktoria of Prussia or Princess Victoria of Wales.
However, Amélie and Carlos came to live quite harmoniously with each other.
They had three children:


Queen consort

On 19 October 1889, King Luís died and Carlos succeeded him on the throne.
Amélie became the new Queen consort of Portugal.
Amélie played an active role as a queen, and somewhat softened the growing criticism towards the monarchy with her personal popularity, though she did receive some criticism for her expenses.
In 1892, Pope Leo XIII gave a Golden Rose to Amélie.
On their way to the Palace of Necessidades, the carriage carrying Carlos and his family passed through the Rua do Arsenal.
The King died immediately, his heir Prince Dom Luís Filipe was mortally wounded and Infante Dom Manuel was hit in the arm.
Queen Amélie remained unharmed as she tried to defend her youngest son, the new king Manuel II, with the flower bouquet she kept in her hand.
About twenty minutes later, Prince Luís Filipe died and the next day Manuel was acclaimed King of Portugal, the last of the Braganza dynasty.
Manuel II was deposed in a military coup, later known as the 5 October 1910 revolution, which resulted in the establishment of the Portuguese First Republic.
Queen Amélie left Portugal with the rest of the royal family and went into exile.
During the Second World War, the Portuguese government invited her to return to Portugal, but she declined the offer.
She visited Portugal for the last time in 1945.
Later years and death

In 1949, Amélie left her Portuguese possessions to her godson, Duarte Pio, Duke of Braganza, at the request of Prime Minister António de Oliveira Salazar.
She was given a state funeral and buried at the Pantheon of the Braganzas located in the Monastery of São Vicente de Fora, in Lisbon, Portugal.



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
  AssignClass (e7750c8c-b8fe-4034-a54d-cc051f3403e1)
 Call ID: e7750c8c-b8fe-4034-a54d-cc051f3403e1
  Args:
    type: :Woman
    source: Amélie_of_Orléans
  AssignClass (9d78f4d7-3c6f-45d4-aaf8-8460ee6c3c1f)
 Call ID: 9d78f4d7-3c6f-45d4-aaf8-8460ee6c3c1f
  Args:
    source: Amélie_of_Orléans
    type: :Person
  AddLiteral (5d6e39c8-1a01-4275-90ba-f32c0de8f911)
 Call ID: 5d6e39c8-1a01-4275-90ba-f32c0de8f911
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Amélie_of_Orléans
    literal_value: Marie Amélie Louise Hélène
  AddLiteral (0489b59e-41ef-47e0-945a-ecf7a787d94e)
 Call ID: 0489b59e-41ef-47e0-945a-ecf7a787d94e
  Args:
    literal_value: 1865
    source: Amélie_of_Orléans
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (0110cce3-7b56-4de6-80c0-f15897340121)
 Call ID: 0110cce3-7b56-4de6-80c0-f15897340121
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Amélie_of_Orléans
    literal_value: 1951
  AssignClass (4eb2a6d7-978e-4acc-ac47-ba9a4fd730c3)
 Call ID: 4eb2a6d7-978e-4acc-ac47-ba9a4fd730c3
  Args:
    source: Carlos_I_of_Portugal
    type: :Man
  AssignClass (f4266b5e-3287-4244-9f87-62cdeb030447)
 Call ID: f4266b5e-3287-4244-9f87-62cdeb030447
  Args:
    source: Carlos_I_of_Portugal
    type: :Person
  AddTriple (7c2f8b21-9912-41cd-9d96-6f993900689e)
 Call ID: 7c2f8b21-9912-41cd-9d96-6f993900689e
  Args:
    relation: :hasRelation
    target: Carlos_I_of_Portugal
    source: Amélie_of_Orléans
  AddLiteral (23becfa9-f57d-4b67-993b-e15328786afb)
 Call ID: 23becfa9-f57d-4b67-993b-e15328786afb
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Amélie_of_Orléans
    literal_value: 1886
  AssignClass (308433e1-4ab6-4977-b994-c068c74da3fa)
 Call ID: 308433e1-4ab6-4977-b994-c068c74da3fa
  Args:
    type: :Man
    source: Prince_Philippe_Count_of_Paris
  AssignClass (749a0013-b11d-47aa-84ca-a40ec6597f49)
 Call ID: 749a0013-b11d-47aa-84ca-a40ec6597f49
  Args:
    type: :Ancestor
    source: Prince_Philippe_Count_of_Paris
  AssignClass (b40b3044-860c-4822-a3c2-53d966c7a45d)
 Call ID: b40b3044-860c-4822-a3c2-53d966c7a45d
  Args:
    source: Princess_Marie_Isabelle_dOrléans
    type: :Woman
  AssignClass (1e9f83f7-505a-4b61-8589-9ae368e42eb3)
 Call ID: 1e9f83f7-505a-4b61-8589-9ae368e42eb3
  Args:
    type: :Ancestor
    source: Princess_Marie_Isabelle_dOrléans
  AddTriple (fa32a634-72d4-4b4a-b375-e3042efd44ae)
 Call ID: fa32a634-72d4-4b4a-b375-e3042efd44ae
  Args:
    source: Amélie_of_Orléans
    relation: :hasFather
    target: Prince_Philippe_Count_of_Paris
  AddTriple (4b0eab20-e065-4d34-b827-25756d766554)
 Call ID: 4b0eab20-e065-4d34-b827-25756d766554
  Args:
    relation: :hasMother
    target: Princess_Marie_Isabelle_dOrléans
    source: Amélie_of_Orléans
  AssignClass (53e115e3-3420-4393-844b-fa38d6c419dc)
 Call ID: 53e115e3-3420-4393-844b-fa38d6c419dc
  Args:
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
    type: :Man
  AssignClass (328ef235-3aa5-488d-9be0-412f7c39871c)
 Call ID: 328ef235-3aa5-488d-9be0-412f7c39871c
  Args:
    type: :Ancestor
    source: Prince_Ferdinand_Philippe_Duke_of_Orléans
  AssignClass (5d196660-04ad-4209-bcb1-ae2c958b8ef1)
 Call ID: 5d196660-04ad-4209-bcb1-ae2c958b8ef1
  Args:
    source: Duchess_Helena_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (28bb487f-6ab2-4bce-ab97-201320413f4a)
 Call ID: 28bb487f-6ab2-4bce-ab97-201320413f4a
  Args:
    type: :Ancestor
    source: Duchess_Helena_of_Mecklenburg_Schwerin
  AddTriple (8a442eaa-be34-4b9a-b689-225ae2d07c21)
 Call ID: 8a442eaa-be34-4b9a-b689-225ae2d07c21
  Args:
    target: Prince_Ferdinand_Philippe_Duke_of_Orléans
    relation: :hasFather
    source: Prince_Philippe_Count_of_Paris
  AddTriple (02fbccb1-f580-44d8-be0d-e7295b524b03)
 Call ID: 02fbccb1-f580-44d8-be0d-e7295b524b03
  Args:
    relation: :hasMother
    target: Duchess_Helena_of_Mecklenburg_Schwerin
    source: Prince_Philippe_Count_of_Paris
  AssignClass (71a2e96d-0d11-43eb-922c-54b535634564)
 Call ID: 71a2e96d-0d11-43eb-922c-54b535634564
  Args:
    source: Prince_Antoine_Duke_of_Montpensier
    type: :Man
  AssignClass (8f080ae0-f4b9-4f2e-90ec-13f4948f0624)
 Call ID: 8f080ae0-f4b9-4f2e-90ec-13f4948f0624
  Args:
    type: :Ancestor
    source: Prince_Antoine_Duke_of_Montpensier
  AssignClass (47f8594c-a8fa-4551-8414-e0e48837851d)
 Call ID: 47f8594c-a8fa-4551-8414-e0e48837851d
  Args:
    source: Infanta_Luisa_Fernanda_of_Spain
    type: :Woman
  AssignClass (57e9f06a-1d0c-4972-8f3f-32111dda2eda)
 Call ID: 57e9f06a-1d0c-4972-8f3f-32111dda2eda
  Args:
    source: Infanta_Luisa_Fernanda_of_Spain
    type: :Ancestor
  AddTriple (0f945aaf-9475-4c94-8428-5e485d8eb403)
 Call ID: 0f945aaf-9475-4c94-8428-5e485d8eb403
  Args:
    target: Prince_Antoine_Duke_of_Montpensier
    relation: :hasFather
    source: Princess_Marie_Isabelle_dOrléans
  AddTriple (8916b0a0-501f-403e-bf89-2320bf49f643)
 Call ID: 8916b0a0-501f-403e-bf89-2320bf49f643
  Args:
    target: Infanta_Luisa_Fernanda_of_Spain
    relation: :hasMother
    source: Princess_Marie_Isabelle_dOrléans
  AssignClass (82f6c505-7146-4232-80d9-3eece983151b)
 Call ID: 82f6c505-7146-4232-80d9-3eece983151b
  Args:
    source: King_Louis_Philippe_I_of_France
    type: :Man
  AssignClass (8244a76d-c83c-4f79-ad4b-8187ae6862f4)
 Call ID: 8244a76d-c83c-4f79-ad4b-8187ae6862f4
  Args:
    source: King_Louis_Philippe_I_of_France
    type: :Ancestor
  AssignClass (b3c6d776-6d12-44e0-ad8c-16b7711f0b26)
 Call ID: b3c6d776-6d12-44e0-ad8c-16b7711f0b26
  Args:
    type: :Woman
    source: Maria_Amalia_of_the_Two_Sicilies
  AssignClass (e9114a62-8d3c-491d-b822-f47f37e69136)
 Call ID: e9114a62-8d3c-491d-b822-f47f37e69136
  Args:
    source: Maria_Amalia_of_the_Two_Sicilies
    type: :Ancestor
  AddTriple (78b33b9b-5021-4886-a8d7-c648ac86bad5)
 Call ID: 78b33b9b-5021-4886-a8d7-c648ac86bad5
  Args:
    source: King_Louis_Philippe_I_of_France
    relation: :isFatherOf
    target: Prince_Ferdinand_Philippe_Duke_of_Orléans
  AddTriple (1a6c93a5-9afd-456d-9dbf-35e29844bbae)
 Call ID: 1a6c93a5-9afd-456d-9dbf-35e29844bbae
  Args:
    source: King_Louis_Philippe_I_of_France
    target: Prince_Antoine_Duke_of_Montpensier
    relation: :isFatherOf
  AddTriple (f2823f6d-90a6-4841-abd4-0d4ecdc1174e)
 Call ID: f2823f6d-90a6-4841-abd4-0d4ecdc1174e
  Args:
    relation: :isMotherOf
    target: Prince_Ferdinand_Philippe_Duke_of_Orléans
    source: Maria_Amalia_of_the_Two_Sicilies
  AddTriple (5919c406-710b-496f-90cb-4ee8c93818a4)
 Call ID: 5919c406-710b-496f-90cb-4ee8c93818a4
  Args:
    relation: :isMotherOf
    target: Prince_Antoine_Duke_of_Montpensier
    source: Maria_Amalia_of_the_Two_Sicilies
  AssignClass (bc788e04-1e00-4152-9fd2-3bfe6b7746a5)
 Call ID: bc788e04-1e00-4152-9fd2-3bfe6b7746a5
  Args:
    type: :Man
    source: King_Luís_I_of_Portugal
  AssignClass (7b47e6bb-07c5-44fb-bffa-2d0a26a22da7)
 Call ID: 7b47e6bb-07c5-44fb-bffa-2d0a26a22da7
  Args:
    type: :Ancestor
    source: King_Luís_I_of_Portugal
  AssignClass (38154603-f041-4de6-bc92-538576b510ee)
 Call ID: 38154603-f041-4de6-bc92-538576b510ee
  Args:
    type: :Woman
    source: Maria_Pia_of_Savoy
  AssignClass (b7218528-4b85-4559-8003-3fce77484287)
 Call ID: b7218528-4b85-4559-8003-3fce77484287
  Args:
    source: Maria_Pia_of_Savoy
    type: :Ancestor
  AddTriple (91803816-c682-42be-ae30-6f0d734ead19)
 Call ID: 91803816-c682-42be-ae30-6f0d734ead19
  Args:
    target: King_Luís_I_of_Portugal
    relation: :hasFather
    source: Carlos_I_of_Portugal
  AddTriple (13ab69d8-d43c-4318-ab6c-eaafd425d2a7)
 Call ID: 13ab69d8-d43c-4318-ab6c-eaafd425d2a7
  Args:
    source: Carlos_I_of_Portugal
    target: Maria_Pia_of_Savoy
    relation: :hasMother
  AssignClass (399e452a-c67c-4c7b-bdf9-9699bcf909e3)
 Call ID: 399e452a-c67c-4c7b-bdf9-9699bcf909e3
  Args:
    type: :Man
    source: Prince_Dom_Luís_Filipe
  AssignClass (01c03d0c-4d39-4492-bc4d-a2654d7f0eb9)
 Call ID: 01c03d0c-4d39-4492-bc4d-a2654d7f0eb9
  Args:
    type: :Person
    source: Prince_Dom_Luís_Filipe
  AssignClass (bfb01a96-b500-4ba1-9c9d-389dc9cc967e)
 Call ID: bfb01a96-b500-4ba1-9c9d-389dc9cc967e
  Args:
    source: Infante_Dom_Manuel_Manuel_II
    type: :Man
  AssignClass (dc184751-11f5-4b03-952e-ca8abda9a98d)
 Call ID: dc184751-11f5-4b03-952e-ca8abda9a98d
  Args:
    source: Infante_Dom_Manuel_Manuel_II
    type: :Person
  AddTriple (a9fe5ad3-f729-4413-b8a5-edb45eae7052)
 Call ID: a9fe5ad3-f729-4413-b8a5-edb45eae7052
  Args:
    source: Prince_Dom_Luís_Filipe
    target: Carlos_I_of_Portugal
    relation: :hasFather
  AddTriple (39abcff4-27f4-4420-a3cb-4321548bdc3d)
 Call ID: 39abcff4-27f4-4420-a3cb-4321548bdc3d
  Args:
    target: Amélie_of_Orléans
    relation: :hasMother
    source: Prince_Dom_Luís_Filipe
  AddTriple (427fe002-bec9-4e2d-ada1-549d6936da4d)
 Call ID: 427fe002-bec9-4e2d-ada1-549d6936da4d
  Args:
    source: Infante_Dom_Manuel_Manuel_II
    target: Carlos_I_of_Portugal
    relation: :hasFather
  AddTriple (65554622-795f-4763-8d29-386e70ed7e8e)
 Call ID: 65554622-795f-4763-8d29-386e70ed7e8e
  Args:
    source: Infante_Dom_Manuel_Manuel_II
    relation: :hasMother
    target: Amélie_of_Orléans
  Finish (98347fa0-a148-4871-b1e1-4f8f573f0129)
 Call ID: 98347fa0-a148-4871-b1e1-4f8f573f0129
  Args: