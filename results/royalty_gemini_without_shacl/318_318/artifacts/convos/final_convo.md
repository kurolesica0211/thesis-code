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
Don Carlos, Prince of Bourbon-Two Sicilies, Infante of Spain (Full Italian name: Carlo Maria Francesco d'Assisi Pasquale Ferdinando Antonio di Padova Francesco de Paola Alfonso Andrea Avelino Tancredi, Principe di Borbone delle Due Sicilie, Infante di Spagna; 10 November 1870 – 11 November 1949) was the son of Prince Alfonso of the Two Sicilies, Count of Caserta and Princess Maria Antonietta of Bourbon-Two Sicilies, and nephew of the last King of the Two Sicilies, Francis II.


Marriages and children

On 14 February 1901 in Madrid, Carlos married Mercedes, Princess of Asturias, elder daughter of the late King Alfonso XII of Spain and of his wife Archduchess Maria Christina of Austria.
Mercedes was the elder sister and heir presumptive to King Alfonso XIII of Spain, an unmarried teenager.
In 1907, Carlos married secondly to Princess Louise of Orléans, daughter of Prince Philippe, Count of Paris.
The couple had four children:


Prince Carlos's descendants include King Felipe VI of Spain, Prince Pedro, Duke of Calabria, Prince Pedro Carlos of Orléans-Braganza, and Philip, Hereditary Prince of Yugoslavia, among others.
Military service

Carlos served in the Spanish Army in the Spanish–American War and received the Military Order of Maria Cristina.
Two Sicilies succession

In 1894, Carlos's father Alfonso became the head of the House of Bourbon-Two Sicilies.
On marrying his first wife, Carlos renounced on 14 December 1900 his future rights of succession to the non-existent Crown of Two Sicilies in an official document, known as the Act of Cannes, subject to a requirement in the Treaty of Naples of 1759 and the Pragmatic Decree of 6 October 1759 that the Crown of Spain should not be combined with the "Italian Sovereignty".
In 1960, Carlos' elder brother Ferdinand died without male issue, and a dispute arose between Carlos' son Alfonso and Carlos' younger brother Ranieri on the headship of the house, this with competing claims: by the law of primogeniture, Carlos' son Alfonso was considered the heir, but Ranieri claimed that Carlos had renounced his rights and those of his descendants according to the Act of Cannes.
Alfonso refuted that claim by stating that it was only a promise from his father to relinquish this right if the crown of the Kingdom of the Two Sicilies were to be united with the Spanish Crown.
Since this did not happen, the act had no effect and Carlos' son Alfonso reclaimed his rights.
Alfonso's claim was recognised by the heads of the different lines of the House of Bourbon, although not by the head of the Orleans family, and in 1983 the Spanish Council of State, following an investigation by the Ministries of Justice and Foreign Affairs, the Royal Academy of Jurisprudence and Legislation and the Institute Salazar y Castro concluded unanimously in favour of Infante Don Alfonso's only son, Prince and Infante Don Carlos, a position shared by the Spanish Royal House.



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
  AssignClass (4fd9879b-e12a-4501-9d06-e4c5d3132c49)
 Call ID: 4fd9879b-e12a-4501-9d06-e4c5d3132c49
  Args:
    source: Don_Carlos
    type: :Man
  AssignClass (25543fec-c87e-489e-b455-ebb96057864b)
 Call ID: 25543fec-c87e-489e-b455-ebb96057864b
  Args:
    source: Don_Carlos
    type: :Person
  AddLiteral (abd74a46-ec35-450b-94a1-03d6d267527a)
 Call ID: abd74a46-ec35-450b-94a1-03d6d267527a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1870
    source: Don_Carlos
  AddLiteral (a2ff6011-8339-4c83-8342-497347336e79)
 Call ID: a2ff6011-8339-4c83-8342-497347336e79
  Args:
    literal_value: 1949
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Don_Carlos
  AssignClass (798fd844-e693-4cd8-a8e2-f09909225984)
 Call ID: 798fd844-e693-4cd8-a8e2-f09909225984
  Args:
    source: Alfonso_Two_Sicilies
    type: :Man
  AssignClass (ed3d812d-c806-4ad3-82b4-bdf7063c080b)
 Call ID: ed3d812d-c806-4ad3-82b4-bdf7063c080b
  Args:
    type: :Person
    source: Alfonso_Two_Sicilies
  AssignClass (da959594-85c6-4688-8d89-0c4121d217c7)
 Call ID: da959594-85c6-4688-8d89-0c4121d217c7
  Args:
    source: Maria_Antonietta
    type: :Woman
  AssignClass (95aa3229-9d28-498f-a53e-f447f8e5660f)
 Call ID: 95aa3229-9d28-498f-a53e-f447f8e5660f
  Args:
    type: :Person
    source: Maria_Antonietta
  AddTriple (24467029-9b8a-44da-8756-ed1ae5aea754)
 Call ID: 24467029-9b8a-44da-8756-ed1ae5aea754
  Args:
    target: Alfonso_Two_Sicilies
    relation: :hasFather
    source: Don_Carlos
  AddTriple (be069e9b-37f6-48ad-a1da-89e3d10cda32)
 Call ID: be069e9b-37f6-48ad-a1da-89e3d10cda32
  Args:
    relation: :hasMother
    target: Maria_Antonietta
    source: Don_Carlos
  AssignClass (59f42bee-f2ac-4f24-9b53-d579f8f42104)
 Call ID: 59f42bee-f2ac-4f24-9b53-d579f8f42104
  Args:
    source: Francis_II
    type: :Man
  AssignClass (e8a10743-49f6-440a-a4d1-faa5bbb29ea3)
 Call ID: e8a10743-49f6-440a-a4d1-faa5bbb29ea3
  Args:
    type: :Person
    source: Francis_II
  AddTriple (f72ecdc6-7c65-402a-8437-b11fd4f26c08)
 Call ID: f72ecdc6-7c65-402a-8437-b11fd4f26c08
  Args:
    relation: :isBrotherOf
    target: Alfonso_Two_Sicilies
    source: Francis_II
  AssignClass (986fecf7-e17d-4f8a-90a5-8ed9a6e0e990)
 Call ID: 986fecf7-e17d-4f8a-90a5-8ed9a6e0e990
  Args:
    type: :Woman
    source: Mercedes_Princess_Asturias
  AssignClass (15f596ff-5ec0-458e-bd11-ebc838a3084a)
 Call ID: 15f596ff-5ec0-458e-bd11-ebc838a3084a
  Args:
    type: :Person
    source: Mercedes_Princess_Asturias
  AddTriple (7a3f896a-ec7b-42dd-96b6-2b6d3ce72103)
 Call ID: 7a3f896a-ec7b-42dd-96b6-2b6d3ce72103
  Args:
    relation: :hasRelation
    target: Mercedes_Princess_Asturias
    source: Don_Carlos
  AddLiteral (5f94f379-7023-4bb2-bb51-55c03223ac98)
 Call ID: 5f94f379-7023-4bb2-bb51-55c03223ac98
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1901
    source: Don_Carlos
  AssignClass (8e41d934-84df-4634-b38a-f3868ca00678)
 Call ID: 8e41d934-84df-4634-b38a-f3868ca00678
  Args:
    source: Alfonso_XII_Spain
    type: :Man
  AssignClass (feb74582-807c-4356-9b86-53d3541f36a4)
 Call ID: feb74582-807c-4356-9b86-53d3541f36a4
  Args:
    source: Alfonso_XII_Spain
    type: :Person
  AssignClass (5c34c061-1664-4f23-83c5-9fada7e14d72)
 Call ID: 5c34c061-1664-4f23-83c5-9fada7e14d72
  Args:
    type: :Woman
    source: Maria_Christina_Austria
  AssignClass (6de9631c-e373-4188-8245-94363a73c7b9)
 Call ID: 6de9631c-e373-4188-8245-94363a73c7b9
  Args:
    source: Maria_Christina_Austria
    type: :Person
  AddTriple (57f51414-0c72-4920-ba77-cb7e575b9a01)
 Call ID: 57f51414-0c72-4920-ba77-cb7e575b9a01
  Args:
    relation: :hasFather
    target: Alfonso_XII_Spain
    source: Mercedes_Princess_Asturias
  AddTriple (e411df5b-cc6d-4095-b733-cb616c66970f)
 Call ID: e411df5b-cc6d-4095-b733-cb616c66970f
  Args:
    source: Mercedes_Princess_Asturias
    target: Maria_Christina_Austria
    relation: :hasMother
  AssignClass (fedf19f4-e5cf-417b-b852-fec10c54f04d)
 Call ID: fedf19f4-e5cf-417b-b852-fec10c54f04d
  Args:
    type: :Man
    source: Alfonso_XIII_Spain
  AssignClass (2c5cd438-c83d-4f65-97fc-140e6051d114)
 Call ID: 2c5cd438-c83d-4f65-97fc-140e6051d114
  Args:
    source: Alfonso_XIII_Spain
    type: :Person
  AddTriple (6c448b45-7d4a-4873-86a5-48aa7547215d)
 Call ID: 6c448b45-7d4a-4873-86a5-48aa7547215d
  Args:
    source: Mercedes_Princess_Asturias
    target: Alfonso_XIII_Spain
    relation: :isSisterOf
  AssignClass (4ca7d002-d4d0-4256-b774-f36794a69225)
 Call ID: 4ca7d002-d4d0-4256-b774-f36794a69225
  Args:
    source: Louise_Orleans
    type: :Woman
  AssignClass (ab687b2f-70d3-4bc4-bfb6-e2b68a4ee69d)
 Call ID: ab687b2f-70d3-4bc4-bfb6-e2b68a4ee69d
  Args:
    type: :Person
    source: Louise_Orleans
  AddTriple (0e68987d-1342-4b45-9251-c0e560caf307)
 Call ID: 0e68987d-1342-4b45-9251-c0e560caf307
  Args:
    source: Don_Carlos
    relation: :hasRelation
    target: Louise_Orleans
  AssignClass (166bb6d3-6fc0-4db0-aa80-6212bf936d95)
 Call ID: 166bb6d3-6fc0-4db0-aa80-6212bf936d95
  Args:
    source: Philippe_Count_Paris
    type: :Man
  AssignClass (8bf2cb0f-d4b9-400d-8522-e6508dd845ad)
 Call ID: 8bf2cb0f-d4b9-400d-8522-e6508dd845ad
  Args:
    type: :Person
    source: Philippe_Count_Paris
  AddTriple (820e7ff2-e3eb-4d0e-9bed-1b063000deb3)
 Call ID: 820e7ff2-e3eb-4d0e-9bed-1b063000deb3
  Args:
    relation: :hasFather
    target: Philippe_Count_Paris
    source: Louise_Orleans
  AssignClass (65262a8a-4ff5-4e9f-b19a-75322e7a0b84)
 Call ID: 65262a8a-4ff5-4e9f-b19a-75322e7a0b84
  Args:
    source: Ferdinand_Two_Sicilies
    type: :Man
  AssignClass (f602b427-3443-4c1f-b0ae-34a027419544)
 Call ID: f602b427-3443-4c1f-b0ae-34a027419544
  Args:
    source: Ferdinand_Two_Sicilies
    type: :Person
  AddTriple (2a3ef565-2a4d-4467-a81e-9cc0ed6aab2f)
 Call ID: 2a3ef565-2a4d-4467-a81e-9cc0ed6aab2f
  Args:
    source: Ferdinand_Two_Sicilies
    target: Don_Carlos
    relation: :isBrotherOf
  AssignClass (c8c9b075-ccec-47c0-999c-5baf421f9c9b)
 Call ID: c8c9b075-ccec-47c0-999c-5baf421f9c9b
  Args:
    source: Ranieri_Two_Sicilies
    type: :Man
  AssignClass (bd79e9d6-99fe-432d-bafb-f483b3dd53e1)
 Call ID: bd79e9d6-99fe-432d-bafb-f483b3dd53e1
  Args:
    type: :Person
    source: Ranieri_Two_Sicilies
  AddTriple (50b2aa9a-b9b6-474a-a7b3-6e4b56adacc4)
 Call ID: 50b2aa9a-b9b6-474a-a7b3-6e4b56adacc4
  Args:
    relation: :isBrotherOf
    target: Don_Carlos
    source: Ranieri_Two_Sicilies
  AssignClass (850d8ba4-2d9b-463c-a687-e5ddc5eae91d)
 Call ID: 850d8ba4-2d9b-463c-a687-e5ddc5eae91d
  Args:
    type: :Man
    source: Alfonso_Son_of_Carlos
  AssignClass (80ff2d1b-0bce-4862-8d4b-b3dc4cd38d36)
 Call ID: 80ff2d1b-0bce-4862-8d4b-b3dc4cd38d36
  Args:
    type: :Person
    source: Alfonso_Son_of_Carlos
  AddTriple (2e338f66-6f96-4f41-91fc-c851fbe478dc)
 Call ID: 2e338f66-6f96-4f41-91fc-c851fbe478dc
  Args:
    source: Alfonso_Son_of_Carlos
    relation: :isSonOf
    target: Don_Carlos
  Finish (74f476dd-3f22-42cd-ba75-361c2c62a754)
 Call ID: 74f476dd-3f22-42cd-ba75-361c2c62a754
  Args: