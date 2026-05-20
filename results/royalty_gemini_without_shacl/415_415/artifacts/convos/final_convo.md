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
Wittekind Adolf Heinrich Georg-Wilhelm, Prince of Waldeck and Pyrmont (Wittekind Adolf Heinrich Georg-Wilhelm Fürst zu Waldeck und Pyrmont; 9 March 1936 – 16 December 2024), was a member of the German nobility who from 1967 to 2024 was head of the House of Waldeck and Pyrmont.
Biography

Born in Arolsen (now Bad Arolsen) in Hesse, Germany, Wittekind was the only son of Josias Georg Wilhelm Adolf, Hereditary Prince of Waldeck and Pyrmont (1896−1967), an SS officer later found guilty of war crimes, and Duchess Altburg Marie Mathilde von Oldenburg (1903–2001), daughter of Frederick Augustus II, Grand Duke of Oldenburg.
He was the great-nephew of Emma of Waldeck and Pyrmont (later Queen of the Netherlands and Grand Duchess of Luxembourg) and thus a second cousin of Queen Beatrix of the Netherlands, whom he welcomed to Arolsen Castle in both 2008, on the 150th anniversary of Queen Emma's birth, and 2016, to celebrate his own 80th birthday.
Wittekind became head of the House of Waldeck and Pyrmont on his father's death in 1967.
Marriage and family

On 19 May 1988, in Frohnleiten, Wittekind married Countess Cecilia von Goëss-Saurau (born 1956), with whom he had three sons, including Carl-Anton, who succeeded him as Prince of Waldeck and Pyrmont.



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
  AssignClass (58da2f32-3172-4525-8adc-2136b4dd608b)
 Call ID: 58da2f32-3172-4525-8adc-2136b4dd608b
  Args:
    type: :Man
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (fa53e9b4-3d09-4e16-b4ba-c3a6a20d9960)
 Call ID: fa53e9b4-3d09-4e16-b4ba-c3a6a20d9960
  Args:
    type: :Person
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddLiteral (79fa9f48-72b2-420f-b501-da20b2ef150b)
 Call ID: 79fa9f48-72b2-420f-b501-da20b2ef150b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    literal_value: 1936
  AddLiteral (97415186-2f15-4598-8cdd-1f9b163b93a1)
 Call ID: 97415186-2f15-4598-8cdd-1f9b163b93a1
  Args:
    literal_value: 2024
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (8dfb1fce-1098-46b7-99cf-2f5e67faf0e7)
 Call ID: 8dfb1fce-1098-46b7-99cf-2f5e67faf0e7
  Args:
    type: :Man
    source: Josias_Georg_Wilhelm_Adolf
  AssignClass (65dc5859-f23f-4df5-bbdb-15ec697ce9d5)
 Call ID: 65dc5859-f23f-4df5-bbdb-15ec697ce9d5
  Args:
    type: :Person
    source: Josias_Georg_Wilhelm_Adolf
  AddLiteral (bcf5715c-28f5-42aa-a22c-ef473ce7dd2f)
 Call ID: bcf5715c-28f5-42aa-a22c-ef473ce7dd2f
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    literal_value: 1896
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (a37e7ca5-b6a7-453d-a6db-6661df1ed683)
 Call ID: a37e7ca5-b6a7-453d-a6db-6661df1ed683
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    literal_value: 1967
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (ec6983e2-c700-4aa4-855c-c79584f11cba)
 Call ID: ec6983e2-c700-4aa4-855c-c79584f11cba
  Args:
    type: :Woman
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (cd89e638-15d5-4898-bf89-b93e5896973e)
 Call ID: cd89e638-15d5-4898-bf89-b93e5896973e
  Args:
    type: :Person
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AddLiteral (0a6f7edd-877c-4f26-98ea-dabdc2d8e605)
 Call ID: 0a6f7edd-877c-4f26-98ea-dabdc2d8e605
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1903
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AddLiteral (3f355aa6-2566-492e-ae3e-cfef7bf692d9)
 Call ID: 3f355aa6-2566-492e-ae3e-cfef7bf692d9
  Args:
    literal_value: 2001
    source: Altburg_Marie_Mathilde_von_Oldenburg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (ac89d79c-58cd-4918-b748-dff3c44c8fb7)
 Call ID: ac89d79c-58cd-4918-b748-dff3c44c8fb7
  Args:
    relation: :hasFather
    target: Josias_Georg_Wilhelm_Adolf
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddTriple (5553f400-4606-4769-b365-6787aa050d1c)
 Call ID: 5553f400-4606-4769-b365-6787aa050d1c
  Args:
    target: Altburg_Marie_Mathilde_von_Oldenburg
    relation: :hasMother
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (a95ffe97-ff8e-4faa-b694-e8e29ecee9a4)
 Call ID: a95ffe97-ff8e-4faa-b694-e8e29ecee9a4
  Args:
    type: :Woman
    source: Cecilia_von_Goess-Saurau
  AssignClass (25fb2216-65c2-41c5-b63f-ca93dbf99d5c)
 Call ID: 25fb2216-65c2-41c5-b63f-ca93dbf99d5c
  Args:
    type: :Person
    source: Cecilia_von_Goess-Saurau
  AddLiteral (90dfc822-d160-4c7e-9da2-6ba7e4977245)
 Call ID: 90dfc822-d160-4c7e-9da2-6ba7e4977245
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1956
    source: Cecilia_von_Goess-Saurau
  AddLiteral (3c66b867-60d2-4bb1-a130-7a12c5db246a)
 Call ID: 3c66b867-60d2-4bb1-a130-7a12c5db246a
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1988
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddTriple (e00803a4-50b8-40f0-ac52-06b9fa65082e)
 Call ID: e00803a4-50b8-40f0-ac52-06b9fa65082e
  Args:
    relation: :hasRelation
    target: Cecilia_von_Goess-Saurau
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (c6a833d1-5e00-46bc-86e6-7bac38dfa77d)
 Call ID: c6a833d1-5e00-46bc-86e6-7bac38dfa77d
  Args:
    type: :Man
    source: Carl-Anton
  AssignClass (764406ab-cda6-45e8-bb87-8513832bcd05)
 Call ID: 764406ab-cda6-45e8-bb87-8513832bcd05
  Args:
    type: :Person
    source: Carl-Anton
  AddTriple (234be491-0c88-47ef-8ee9-9f9f4735491e)
 Call ID: 234be491-0c88-47ef-8ee9-9f9f4735491e
  Args:
    relation: :hasFather
    target: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    source: Carl-Anton
  AddTriple (8aaf8c41-83ed-4258-ac56-a9be63db96d6)
 Call ID: 8aaf8c41-83ed-4258-ac56-a9be63db96d6
  Args:
    source: Carl-Anton
    target: Cecilia_von_Goess-Saurau
    relation: :hasMother
  Finish (179eb461-1734-4f35-8725-4bbd5e4f69af)
 Call ID: 179eb461-1734-4f35-8725-4bbd5e4f69af
  Args: