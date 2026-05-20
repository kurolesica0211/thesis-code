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
Victoria Federica de Todos los Santos de Marichalar y Borbón, Lady of Tejada GE (born 9 September 2000) is the younger child and only daughter of Infanta Elena, Duchess of Lugo, and Jaime de Marichalar.
She is a granddaughter of King Juan Carlos I and Queen Sofía of Spain and a niece of King Felipe VI.
Victoria is fifth in the line of succession to the Spanish throne after her cousins, King Felipe's daughters Leonor, Princess of Asturias, and Infanta Sofía; her mother; and her brother, Felipe.
Early life and education

Victoria de Marichalar y Borbón was born 9 September 2000 at 13:00 in Ruber International Hospital in Madrid.
She made her first Holy Communion on 27 May 2009 at the Dominicos Church in Alcobendas, Spain.
Then she studied at a British boarding school for 3 years before returning to Spain at St. George's de La Moraleja.
Victoria studied ballet and horse riding.
Career

Marichalar has been reported to be working in the fashion industry and is quoted as saying that fashion is her "true calling".



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
  AssignClass (9e57116c-0213-4cee-83fc-d4a6b065f776)
 Call ID: 9e57116c-0213-4cee-83fc-d4a6b065f776
  Args:
    type: :Person
    source: :VictoriaFedericaDeMarichalarYBorbón
  AssignClass (13667838-3464-41a2-8dc6-a8ebc480cd41)
 Call ID: 13667838-3464-41a2-8dc6-a8ebc480cd41
  Args:
    source: :VictoriaFedericaDeMarichalarYBorbón
    type: :Woman
  AssignClass (836cfc54-54cd-47c7-a4f2-5ae11a373ca1)
 Call ID: 836cfc54-54cd-47c7-a4f2-5ae11a373ca1
  Args:
    type: :Person
    source: :InfantaElenaDuchessOfLugo
  AssignClass (b78a7dcc-f1a0-4cb8-895c-1980d15e7dc6)
 Call ID: b78a7dcc-f1a0-4cb8-895c-1980d15e7dc6
  Args:
    type: :Woman
    source: :InfantaElenaDuchessOfLugo
  AssignClass (4697a62b-01ff-4366-8d0b-36a77f602afa)
 Call ID: 4697a62b-01ff-4366-8d0b-36a77f602afa
  Args:
    type: :Person
    source: :JaimeDeMarichalar
  AssignClass (cdda65a3-b8cf-4b8c-983e-9101a6e37edc)
 Call ID: cdda65a3-b8cf-4b8c-983e-9101a6e37edc
  Args:
    source: :JaimeDeMarichalar
    type: :Man
  AssignClass (6124f09a-a85c-402a-9116-a1b14beebfce)
 Call ID: 6124f09a-a85c-402a-9116-a1b14beebfce
  Args:
    type: :Person
    source: :JuanCarlosI
  AssignClass (57c5bc5f-8762-4593-b8fa-b3b5455c2ad0)
 Call ID: 57c5bc5f-8762-4593-b8fa-b3b5455c2ad0
  Args:
    type: :Man
    source: :JuanCarlosI
  AssignClass (7d4d2291-e06a-4d26-b974-39c69fa389a4)
 Call ID: 7d4d2291-e06a-4d26-b974-39c69fa389a4
  Args:
    type: :Person
    source: :SofiaOfSpain
  AssignClass (141391ff-ddf9-4944-a2ee-61a9af439dc0)
 Call ID: 141391ff-ddf9-4944-a2ee-61a9af439dc0
  Args:
    source: :SofiaOfSpain
    type: :Woman
  AssignClass (04e8ae4b-bd09-47b1-85ab-26b725dcb7c5)
 Call ID: 04e8ae4b-bd09-47b1-85ab-26b725dcb7c5
  Args:
    source: :FelipeVI
    type: :Person
  AssignClass (aeab4426-6f67-4638-a5c7-aa7faa9016df)
 Call ID: aeab4426-6f67-4638-a5c7-aa7faa9016df
  Args:
    source: :FelipeVI
    type: :Man
  AssignClass (30e560d9-ace9-469c-bc08-441a513860e1)
 Call ID: 30e560d9-ace9-469c-bc08-441a513860e1
  Args:
    source: :LeonorPrincessOfAsturias
    type: :Person
  AssignClass (153b229a-3fa7-4c14-9187-6e05e15eb701)
 Call ID: 153b229a-3fa7-4c14-9187-6e05e15eb701
  Args:
    source: :LeonorPrincessOfAsturias
    type: :Woman
  AssignClass (5987b351-1f38-4422-8bcc-ab93e294ead3)
 Call ID: 5987b351-1f38-4422-8bcc-ab93e294ead3
  Args:
    type: :Person
    source: :InfantaSofia
  AssignClass (eed304bc-8b15-43c4-8bcb-981e192a7523)
 Call ID: eed304bc-8b15-43c4-8bcb-981e192a7523
  Args:
    type: :Woman
    source: :InfantaSofia
  AssignClass (a155fa01-54c6-4527-a969-02f4eca922d1)
 Call ID: a155fa01-54c6-4527-a969-02f4eca922d1
  Args:
    type: :Person
    source: :FelipeDeMarichalar
  AssignClass (ec6e9e11-107a-48c6-b26e-13d773740386)
 Call ID: ec6e9e11-107a-48c6-b26e-13d773740386
  Args:
    source: :FelipeDeMarichalar
    type: :Man
  AddLiteral (96c7344a-67c4-4928-8d2c-96c230f30641)
 Call ID: 96c7344a-67c4-4928-8d2c-96c230f30641
  Args:
    relation: :hasBirthYear
    literal_type: xsd:string
    literal_value: 2000-09-09
    source: :VictoriaFedericaDeMarichalarYBorbón
  AddTriple (1ef5c31c-1ccc-46d0-b716-a1554a953ca8)
 Call ID: 1ef5c31c-1ccc-46d0-b716-a1554a953ca8
  Args:
    target: :InfantaElenaDuchessOfLugo
    source: :VictoriaFedericaDeMarichalarYBorbón
    relation: :hasMother
  AddTriple (8be2acb7-1d51-4f6c-9d9f-6f3f58d36cb8)
 Call ID: 8be2acb7-1d51-4f6c-9d9f-6f3f58d36cb8
  Args:
    relation: :hasFather
    target: :JaimeDeMarichalar
    source: :VictoriaFedericaDeMarichalarYBorbón
  AddTriple (22356c08-11ca-472c-8ea1-ebe041adc329)
 Call ID: 22356c08-11ca-472c-8ea1-ebe041adc329
  Args:
    target: :SofiaOfSpain
    source: :InfantaElenaDuchessOfLugo
    relation: :hasMother
  AddTriple (d206422b-14a6-4ae4-b377-c5c83dc9cda3)
 Call ID: d206422b-14a6-4ae4-b377-c5c83dc9cda3
  Args:
    target: :JuanCarlosI
    source: :InfantaElenaDuchessOfLugo
    relation: :hasFather
  AddTriple (33d3d138-d5bf-430c-95d4-94e688c77ae5)
 Call ID: 33d3d138-d5bf-430c-95d4-94e688c77ae5
  Args:
    relation: :hasBrother
    source: :VictoriaFedericaDeMarichalarYBorbón
    target: :FelipeDeMarichalar
  Finish (59aeb5dd-3455-4cd7-8fb5-b01ee8e12f17)
 Call ID: 59aeb5dd-3455-4cd7-8fb5-b01ee8e12f17
  Args: