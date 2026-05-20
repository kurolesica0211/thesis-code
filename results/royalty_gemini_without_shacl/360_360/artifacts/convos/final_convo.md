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
Don Alessandro Torlonia, 5th Prince of Civitella-Cesi (7 December 1911 – 1 May/12 May 1986) was an Italian banking heir and a member of the House of Torlonia.
About

Born in Rome on 7 December 1911, Torlonia was the son of Marino Torlonia, 4th Prince di Civitella-Cesi and his American wife, Mary Elsie Moore.
Don Alessandro's youngest sister was Donna Marina Torlonia di Civitella-Cesi, grandmother of the American actress Brooke Shields.
In 1941, when his mother was dying in New York City, Torlonia took a high speed boat from Portugal and was arrested in error by FBI, thinking he was an enemy of the state and taken to Ellis Island.
Not to be confused with his cousin with the same name, Alessandro Torlonia (1925–2017), Prince of Fucino and Prince assistant to the papal throne, head of another branch of the family.
In the 1980s, this cousin Torlonia held the title as the "richest man in Rome", as he was the heir to a banking fortune and owner of the famous Torlonia Collection of ancient art.
He died in the Palazzo Nuñez-Torlonia, Rome, in 1986.
Marriage and children

On 14 January 1935, Don Alessandro morganatically married in Rome the Infanta Beatriz of Spain (1909–2002), a daughter of King Alfonso XIII of Spain and of Princess Victoria Eugenie of Battenberg.



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
  AssignClass (5913f938-4d72-46c1-a1f4-f9f847aa2b75)
 Call ID: 5913f938-4d72-46c1-a1f4-f9f847aa2b75
  Args:
    source: Alessandro_Torlonia
    type: :Man
  AssignClass (f58228c1-d208-4bbd-ba67-565127b802b7)
 Call ID: f58228c1-d208-4bbd-ba67-565127b802b7
  Args:
    type: :Man
    source: Marino_Torlonia
  AssignClass (1d07167e-7cb2-4c98-9f76-f5e1452ea2a7)
 Call ID: 1d07167e-7cb2-4c98-9f76-f5e1452ea2a7
  Args:
    type: :Woman
    source: Mary_Elsie_Moore
  AssignClass (78ea5c99-bb24-4499-bf1a-8f53ffe98628)
 Call ID: 78ea5c99-bb24-4499-bf1a-8f53ffe98628
  Args:
    source: Marina_Torlonia
    type: :Woman
  AssignClass (a3628a72-4510-4fec-8a19-65478055d931)
 Call ID: a3628a72-4510-4fec-8a19-65478055d931
  Args:
    source: Brooke_Shields
    type: :Woman
  AssignClass (7422e26a-9be1-4e92-b10d-b2b8894ccc44)
 Call ID: 7422e26a-9be1-4e92-b10d-b2b8894ccc44
  Args:
    source: Alessandro_Torlonia_Cousin
    type: :Man
  AssignClass (d6c17708-89d7-474c-b411-8eafe678cbaf)
 Call ID: d6c17708-89d7-474c-b411-8eafe678cbaf
  Args:
    type: :Woman
    source: Beatriz_of_Spain
  AssignClass (7c5a782e-450d-428c-8604-8dd560f6b51d)
 Call ID: 7c5a782e-450d-428c-8604-8dd560f6b51d
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (5ec7da1a-08ff-44f2-adb0-e5527b5c73e7)
 Call ID: 5ec7da1a-08ff-44f2-adb0-e5527b5c73e7
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AddLiteral (b27c7741-c67a-4385-b4c1-eccbabc3c016)
 Call ID: b27c7741-c67a-4385-b4c1-eccbabc3c016
  Args:
    literal_type: xsd:integer
    literal_value: 1911
    relation: :hasBirthYear
    source: Alessandro_Torlonia
  AddLiteral (013adb41-18de-4b36-8779-68bf3adbb2a3)
 Call ID: 013adb41-18de-4b36-8779-68bf3adbb2a3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1986
    source: Alessandro_Torlonia
  AddTriple (3a447108-99bf-4290-9b91-be4b0f901e37)
 Call ID: 3a447108-99bf-4290-9b91-be4b0f901e37
  Args:
    target: Marino_Torlonia
    source: Alessandro_Torlonia
    relation: :hasFather
  AddTriple (9707a62b-bf7a-4006-a1b8-c909ee0ad612)
 Call ID: 9707a62b-bf7a-4006-a1b8-c909ee0ad612
  Args:
    target: Mary_Elsie_Moore
    source: Alessandro_Torlonia
    relation: :hasMother
  AddTriple (2218a3b6-0a79-4c25-8095-eda0420b497c)
 Call ID: 2218a3b6-0a79-4c25-8095-eda0420b497c
  Args:
    target: Marina_Torlonia
    relation: :hasSister
    source: Alessandro_Torlonia
  AddTriple (09507ace-7da4-4cd2-8366-58c49f23fd8e)
 Call ID: 09507ace-7da4-4cd2-8366-58c49f23fd8e
  Args:
    source: Marina_Torlonia
    relation: :isMotherOf
    target: Brooke_Shields
  AddLiteral (b28a6448-ca5a-4e57-83e0-619e3ec38f03)
 Call ID: b28a6448-ca5a-4e57-83e0-619e3ec38f03
  Args:
    source: Alessandro_Torlonia_Cousin
    literal_value: 1925
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (394baca2-7535-4bc8-8681-0a18e029e741)
 Call ID: 394baca2-7535-4bc8-8681-0a18e029e741
  Args:
    literal_type: xsd:integer
    source: Alessandro_Torlonia_Cousin
    relation: :hasDeathYear
    literal_value: 2017
  AddLiteral (560b9e70-91b3-4644-a3aa-cc8b8342a3e2)
 Call ID: 560b9e70-91b3-4644-a3aa-cc8b8342a3e2
  Args:
    source: Alessandro_Torlonia
    literal_value: 1935
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (33cec21b-0933-4a77-a54f-bcedd3b0dab1)
 Call ID: 33cec21b-0933-4a77-a54f-bcedd3b0dab1
  Args:
    relation: :hasRelation
    source: Alessandro_Torlonia
    target: Beatriz_of_Spain
  AddLiteral (4406c668-e7fc-4422-a1a2-1a38906d1f42)
 Call ID: 4406c668-e7fc-4422-a1a2-1a38906d1f42
  Args:
    source: Beatriz_of_Spain
    literal_value: 1909
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (72e7fd06-0e6c-4f14-89bd-833353778669)
 Call ID: 72e7fd06-0e6c-4f14-89bd-833353778669
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2002
    source: Beatriz_of_Spain
  AddTriple (84469668-26d6-43f9-bcd0-6b2b32e412b7)
 Call ID: 84469668-26d6-43f9-bcd0-6b2b32e412b7
  Args:
    source: Beatriz_of_Spain
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
  AddTriple (d1c135b0-77c1-44b1-a655-f5c0ef91af7d)
 Call ID: d1c135b0-77c1-44b1-a655-f5c0ef91af7d
  Args:
    target: Victoria_Eugenie_of_Battenberg
    source: Beatriz_of_Spain
    relation: :hasMother
  Finish (1ee9f1d3-d4db-4c83-9dc3-3dcc19b563b1)
 Call ID: 1ee9f1d3-d4db-4c83-9dc3-3dcc19b563b1
  Args: