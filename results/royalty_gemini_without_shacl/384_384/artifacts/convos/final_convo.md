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
Prince Karl Franz Josef Wilhelm Friedrich Eduard Paul of Prussia (15 December 1916 – 23 January 1975) was the only child of Prince Joachim of Prussia and Princess Marie-Auguste of Anhalt.
He was also a grandson of Wilhelm II, German Emperor.
Early life

Prince Karl Franz was born on 15 December 1916 in Potsdam.
He was the only child born to Prince Joachim of Prussia and Princess Marie-Auguste of Anhalt and was the Emperor's fourth grandchild to be born since World War I began; he was consequently very young when Hohenzollern fortunes fell.
His grandfather abdicated in 1918, and his father, Prince Joachim, committed suicide in 1920.
At the time of his grandfather's abdication, Prince Karl Franz was twelfth in line of succession to the German and Prussian thrones.
After his father's suicide, Karl Franz was taken into custody by his paternal uncle, Prince Eitel Friedrich of Prussia.
As the legal head of the House of Hohenzollern, he claimed this right because Emperor Wilhelm had issued an edict placing Hohenzollern powers in Eitel's hands.
Eitel's defence had also stated that Marie-Auguste was not a fit person for Karl Franz's guardianship.
Marie-Auguste went to court however and made a plea that she was heartbroken, which may have helped win the case for her.
In 1922, Marie-Auguste sued ex-Emperor Wilhelm for financial support that had been promised in her and Joachim's marriage contract.
Wilhelm's attorney argued that the House of Hohenzollern laws were no longer valid, and therefore there was no obligation to support her.
In World War II, Karl Franz served as a lieutenant in an armoured car division, and at one point was stationed on the Polish front.
Marriages

First

On 1 October 1940, Karl Franz married Princess Henriette Hermine Wanda Ida Luise of Schönaich-Carolath.
She was the daughter of Princess Hermine Reuss of Greiz, who had been the second wife of Karl Franz's grandfather Emperor Wilhelm II since 1922 (Henriette was thus Kaiser Wilhelm's stepdaughter).
Held at Wilhelm's private residence without much ceremony, he and Hermine attended the ceremony, as did a few other guests.
Second

Karl Franz married secondly, on 9 November 1946, to Luise Dora Hartmann (5 September 1909 Hamburg, Germany –
Third

Karl Franz married lastly, on 20 July 1959 in Lima, Peru, Eva Maria Herrera y Valdeavellano (10 June 1922 Lima, Peru – 6 March 1987 Lima, Peru).
They were married until Prince Karl's death and had two daughters:


Ancestry

References



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
  AssignClass (52e00f24-4130-4f94-b2e9-3e9e4eca24e5)
 Call ID: 52e00f24-4130-4f94-b2e9-3e9e4eca24e5
  Args:
    source: Prince_Karl_Franz_of_Prussia
    type: :Man
  AssignClass (06e73aeb-d38b-4067-90ca-83364850326d)
 Call ID: 06e73aeb-d38b-4067-90ca-83364850326d
  Args:
    type: :Person
    source: Prince_Karl_Franz_of_Prussia
  AssignClass (6ed55155-70fe-48b3-b131-503658ae3c19)
 Call ID: 6ed55155-70fe-48b3-b131-503658ae3c19
  Args:
    type: :Man
    source: Prince_Joachim_of_Prussia
  AssignClass (e6755fbb-cad3-4dc7-9584-7369773978ed)
 Call ID: e6755fbb-cad3-4dc7-9584-7369773978ed
  Args:
    source: Prince_Joachim_of_Prussia
    type: :Person
  AssignClass (6d5cc75f-1af6-4911-a893-0ad529cdbf3f)
 Call ID: 6d5cc75f-1af6-4911-a893-0ad529cdbf3f
  Args:
    source: Princess_Marie_Auguste_of_Anhalt
    type: :Woman
  AssignClass (7d54f421-c392-452f-9bd5-d080777ea92a)
 Call ID: 7d54f421-c392-452f-9bd5-d080777ea92a
  Args:
    type: :Person
    source: Princess_Marie_Auguste_of_Anhalt
  AssignClass (cbc35d2c-4fb0-4cc5-90f2-a121b4bc152b)
 Call ID: cbc35d2c-4fb0-4cc5-90f2-a121b4bc152b
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (1ee779fa-0086-4a2b-a382-955ebcfeb545)
 Call ID: 1ee779fa-0086-4a2b-a382-955ebcfeb545
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (6eac3ba3-7e18-464f-bbcd-4387cb20fa82)
 Call ID: 6eac3ba3-7e18-464f-bbcd-4387cb20fa82
  Args:
    type: :Man
    source: Prince_Eitel_Friedrich_of_Prussia
  AssignClass (9d543191-0325-407f-b706-cfea888819f3)
 Call ID: 9d543191-0325-407f-b706-cfea888819f3
  Args:
    source: Prince_Eitel_Friedrich_of_Prussia
    type: :Person
  AssignClass (8ed60286-6bac-4617-bfa9-606e48c97e05)
 Call ID: 8ed60286-6bac-4617-bfa9-606e48c97e05
  Args:
    source: Princess_Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich_Carolath
    type: :Woman
  AssignClass (0c7babea-54ce-470b-ac4b-a510a4def2f8)
 Call ID: 0c7babea-54ce-470b-ac4b-a510a4def2f8
  Args:
    source: Princess_Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich_Carolath
    type: :Person
  AssignClass (a8674ab4-3122-446a-a1d6-c1c925b08ca4)
 Call ID: a8674ab4-3122-446a-a1d6-c1c925b08ca4
  Args:
    source: Princess_Hermine_Reuss_of_Greiz
    type: :Woman
  AssignClass (f63ccccb-fd53-4ef2-82c3-3dc24f7066a9)
 Call ID: f63ccccb-fd53-4ef2-82c3-3dc24f7066a9
  Args:
    type: :Person
    source: Princess_Hermine_Reuss_of_Greiz
  AssignClass (83190577-f6e5-4a3e-a850-e0c8e87ad3f6)
 Call ID: 83190577-f6e5-4a3e-a850-e0c8e87ad3f6
  Args:
    source: Luise_Dora_Hartmann
    type: :Woman
  AssignClass (fbb6cb24-2b24-4a9c-b479-f6a6d5d20683)
 Call ID: fbb6cb24-2b24-4a9c-b479-f6a6d5d20683
  Args:
    type: :Person
    source: Luise_Dora_Hartmann
  AssignClass (36320285-deb8-4a4e-88e3-68e2eb3df115)
 Call ID: 36320285-deb8-4a4e-88e3-68e2eb3df115
  Args:
    source: Eva_Maria_Herrera_y_Valdeavellano
    type: :Woman
  AssignClass (198e6223-df0a-42c3-b427-c0e5e84a24c2)
 Call ID: 198e6223-df0a-42c3-b427-c0e5e84a24c2
  Args:
    type: :Person
    source: Eva_Maria_Herrera_y_Valdeavellano
  AddLiteral (817c786a-eccc-4173-86d6-746cc1277c91)
 Call ID: 817c786a-eccc-4173-86d6-746cc1277c91
  Args:
    literal_type: xsd:integer
    source: Prince_Karl_Franz_of_Prussia
    literal_value: 1916
    relation: :hasBirthYear
  AddLiteral (848f5d86-8541-4bbd-9aca-c0693c93b59f)
 Call ID: 848f5d86-8541-4bbd-9aca-c0693c93b59f
  Args:
    source: Prince_Karl_Franz_of_Prussia
    literal_value: 1975
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (b8b629b7-6afc-41dc-b02b-c7f23e968e2b)
 Call ID: b8b629b7-6afc-41dc-b02b-c7f23e968e2b
  Args:
    relation: :hasFather
    source: Prince_Karl_Franz_of_Prussia
    target: Prince_Joachim_of_Prussia
  AddTriple (690070b6-dfb1-4a6d-82b3-917a514b971a)
 Call ID: 690070b6-dfb1-4a6d-82b3-917a514b971a
  Args:
    relation: :hasMother
    source: Prince_Karl_Franz_of_Prussia
    target: Princess_Marie_Auguste_of_Anhalt
  AddTriple (57d4b6c4-a257-464b-9787-bd6a444ae00b)
 Call ID: 57d4b6c4-a257-464b-9787-bd6a444ae00b
  Args:
    source: Prince_Karl_Franz_of_Prussia
    relation: :hasFather
    target: Wilhelm_II_German_Emperor
  AddTriple (8e61388c-5799-4803-81b3-34a6c46e24f6)
 Call ID: 8e61388c-5799-4803-81b3-34a6c46e24f6
  Args:
    target: Wilhelm_II_German_Emperor
    relation: :hasFather
    source: Prince_Joachim_of_Prussia
  AddTriple (e186d1ea-5f1d-4cd1-a5ef-61d85be71c90)
 Call ID: e186d1ea-5f1d-4cd1-a5ef-61d85be71c90
  Args:
    target: Prince_Joachim_of_Prussia
    source: Prince_Eitel_Friedrich_of_Prussia
    relation: :isBrotherOf
  AddLiteral (3264491c-7de4-45a0-8e1a-089a593cdb55)
 Call ID: 3264491c-7de4-45a0-8e1a-089a593cdb55
  Args:
    literal_value: 1940
    source: Prince_Karl_Franz_of_Prussia
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (9ee5e981-3d8e-4a02-8ab9-97e7c409e48f)
 Call ID: 9ee5e981-3d8e-4a02-8ab9-97e7c409e48f
  Args:
    source: Prince_Karl_Franz_of_Prussia
    relation: :hasRelation
    target: Princess_Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich_Carolath
  AddTriple (a0354fb1-e0ad-4e63-a678-477a35dc9c8c)
 Call ID: a0354fb1-e0ad-4e63-a678-477a35dc9c8c
  Args:
    target: Princess_Hermine_Reuss_of_Greiz
    source: Princess_Henriette_Hermine_Wanda_Ida_Luise_of_Schönaich_Carolath
    relation: :hasMother
  AddLiteral (433c185e-f0bf-490e-a7ac-dfe6146ae5de)
 Call ID: 433c185e-f0bf-490e-a7ac-dfe6146ae5de
  Args:
    source: Prince_Karl_Franz_of_Prussia
    literal_value: 1946
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (f7d99d9a-fa4e-47e2-9a82-9e5e27296cf2)
 Call ID: f7d99d9a-fa4e-47e2-9a82-9e5e27296cf2
  Args:
    source: Prince_Karl_Franz_of_Prussia
    relation: :hasRelation
    target: Luise_Dora_Hartmann
  AddLiteral (5c2cac94-0a47-42d4-b918-166a8b03bd78)
 Call ID: 5c2cac94-0a47-42d4-b918-166a8b03bd78
  Args:
    relation: :hasMarriageYear
    source: Prince_Karl_Franz_of_Prussia
    literal_value: 1959
    literal_type: xsd:integer
  AddTriple (55af93e8-3215-405b-81f5-ec14d9fdf859)
 Call ID: 55af93e8-3215-405b-81f5-ec14d9fdf859
  Args:
    relation: :hasRelation
    source: Prince_Karl_Franz_of_Prussia
    target: Eva_Maria_Herrera_y_Valdeavellano
  Finish (5b78eba9-9e13-460b-88dc-35b3f71b8a72)
 Call ID: 5b78eba9-9e13-460b-88dc-35b3f71b8a72
  Args: