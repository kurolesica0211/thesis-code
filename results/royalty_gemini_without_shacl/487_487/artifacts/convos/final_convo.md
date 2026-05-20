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
Wilhelm Karl Adalbert Erich Detloff Prinz von Preussen (30 January 1922 in Potsdam – 9 April 2007 in Holzminden) was the third son of Prince Oskar of Prussia, and the last surviving grandson of Wilhelm II, the last German Emperor.
Biography

Wilhelm-Karl was the youngest of Prince Oskar of Prussia and Countess Ina Marie von Bassewitz's four children.
Wilhelm-Karl worked tirelessly to keep the Order intact during the Cold War and helped to reunite its membership after the fall of East Germany.
Amongst other orders and awards, Wilhelm-Karl received the Grand Merit Cross (with star) of the Order of Merit of the Federal Republic of Germany and the Grand Cross of the Order pro merito Melitensi of the Sovereign Military Order of Malta.
Marriage and issue

In 1952, Wilhelm-Karl married Armgard Else Helene von Veltheim (17 February 1926 - 1 November 2019), daughter of Friedrich von Veltheim (1881–1955) and his wife, Ottonie von Alvensleben (1883–1960).



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
  AssignClass (b0e09aa0-146e-419a-a569-524a803106de)
 Call ID: b0e09aa0-146e-419a-a569-524a803106de
  Args:
    source: Wilhelm-Karl_von_Preussen
    type: :Man
  AssignClass (a672cb4a-b6c8-4a11-882c-3ae1bd29c03a)
 Call ID: a672cb4a-b6c8-4a11-882c-3ae1bd29c03a
  Args:
    type: :Man
    source: Prince_Oskar_of_Prussia
  AssignClass (aa5121f0-d0ab-4d5e-923b-9faca85224ba)
 Call ID: aa5121f0-d0ab-4d5e-923b-9faca85224ba
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Woman
  AssignClass (57d8f640-cc0b-45a7-9055-87585462336e)
 Call ID: 57d8f640-cc0b-45a7-9055-87585462336e
  Args:
    type: :Woman
    source: Armgard_Else_Helene_von_Veltheim
  AssignClass (63db5aef-8e38-4342-b4b4-e6da2aadb532)
 Call ID: 63db5aef-8e38-4342-b4b4-e6da2aadb532
  Args:
    type: :Man
    source: Friedrich_von_Veltheim
  AssignClass (1b7f21ae-e85a-4c2e-8d62-146e950a21d6)
 Call ID: 1b7f21ae-e85a-4c2e-8d62-146e950a21d6
  Args:
    source: Ottonie_von_Alvensleben
    type: :Woman
  AddLiteral (e065699f-0bea-4dd8-9a7f-a22039fad5b6)
 Call ID: e065699f-0bea-4dd8-9a7f-a22039fad5b6
  Args:
    literal_type: xsd:string
    literal_value: 1922
    source: Wilhelm-Karl_von_Preussen
    relation: :hasBirthYear
  AddLiteral (4657a88d-601d-4bc8-b101-ad257d76bc7a)
 Call ID: 4657a88d-601d-4bc8-b101-ad257d76bc7a
  Args:
    literal_type: xsd:string
    source: Wilhelm-Karl_von_Preussen
    relation: :hasDeathYear
    literal_value: 2007
  AddTriple (5f94828f-51e5-4d8c-9971-2c4a2dbcb1d3)
 Call ID: 5f94828f-51e5-4d8c-9971-2c4a2dbcb1d3
  Args:
    target: Prince_Oskar_of_Prussia
    relation: :hasFather
    source: Wilhelm-Karl_von_Preussen
  AddTriple (7f94fbaa-3f71-428c-b3c9-746b24bd7918)
 Call ID: 7f94fbaa-3f71-428c-b3c9-746b24bd7918
  Args:
    source: Wilhelm-Karl_von_Preussen
    relation: :hasMother
    target: Ina_Marie_von_Bassewitz
  AddLiteral (2743a3e2-cda7-443c-ac16-e8f35009b659)
 Call ID: 2743a3e2-cda7-443c-ac16-e8f35009b659
  Args:
    source: Wilhelm-Karl_von_Preussen
    relation: :hasMarriageYear
    literal_value: 1952
    literal_type: xsd:string
  AddTriple (4fcc415b-53a6-48b2-8602-49f7ed314b50)
 Call ID: 4fcc415b-53a6-48b2-8602-49f7ed314b50
  Args:
    target: Armgard_Else_Helene_von_Veltheim
    relation: :hasRelation
    source: Wilhelm-Karl_von_Preussen
  AddLiteral (b983c078-961e-4f80-b379-43d642d8b475)
 Call ID: b983c078-961e-4f80-b379-43d642d8b475
  Args:
    literal_type: xsd:string
    source: Armgard_Else_Helene_von_Veltheim
    relation: :hasBirthYear
    literal_value: 1926
  AddLiteral (8bfb6d05-3b51-4aaf-af64-f75944f14126)
 Call ID: 8bfb6d05-3b51-4aaf-af64-f75944f14126
  Args:
    literal_type: xsd:string
    literal_value: 2019
    source: Armgard_Else_Helene_von_Veltheim
    relation: :hasDeathYear
  AddTriple (6ac0dd89-5b47-4c90-a7f2-a5518a01e823)
 Call ID: 6ac0dd89-5b47-4c90-a7f2-a5518a01e823
  Args:
    source: Armgard_Else_Helene_von_Veltheim
    relation: :hasFather
    target: Friedrich_von_Veltheim
  AddTriple (6c2792bc-3dd8-4987-9718-b035f4ee1ccf)
 Call ID: 6c2792bc-3dd8-4987-9718-b035f4ee1ccf
  Args:
    target: Ottonie_von_Alvensleben
    relation: :hasMother
    source: Armgard_Else_Helene_von_Veltheim
  AddLiteral (13271ace-869f-4f06-88ef-dd13356504ad)
 Call ID: 13271ace-869f-4f06-88ef-dd13356504ad
  Args:
    source: Friedrich_von_Veltheim
    relation: :hasBirthYear
    literal_value: 1881
    literal_type: xsd:string
  AddLiteral (d1766c09-3301-4038-93ab-d6edd622e8f6)
 Call ID: d1766c09-3301-4038-93ab-d6edd622e8f6
  Args:
    literal_type: xsd:string
    literal_value: 1955
    source: Friedrich_von_Veltheim
    relation: :hasDeathYear
  AddLiteral (6853cd8d-c30f-4216-95dd-2e2f466a2ff7)
 Call ID: 6853cd8d-c30f-4216-95dd-2e2f466a2ff7
  Args:
    literal_type: xsd:string
    literal_value: 1883
    source: Ottonie_von_Alvensleben
    relation: :hasBirthYear
  AddLiteral (36209efd-ec36-4234-8307-d13b07cbf64d)
 Call ID: 36209efd-ec36-4234-8307-d13b07cbf64d
  Args:
    literal_value: 1960
    source: Ottonie_von_Alvensleben
    relation: :hasDeathYear
    literal_type: xsd:string
  Finish (ad86d7cc-0257-40a9-b8d2-e8caff69ec31)
 Call ID: ad86d7cc-0257-40a9-b8d2-e8caff69ec31
  Args: