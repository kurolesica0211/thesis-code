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
Princess Feodora of Saxe-Meiningen (Feodora Karola Charlotte Marie Adelheid Auguste Mathilde; 29 May 1890 – 12 March 1972) was the eldest child of Prince Friedrich Johann of Saxe-Meiningen, a younger son of Georg II, Duke of Saxe-Meiningen, and Countess Adelaide of Lippe-Biesterfeld, a daughter of Ernst, Count of Lippe-Biesterfeld.
By marriage, she was known as Grand Duchess of Saxe-Weimar-Eisenach.
Biography

Marriage

During a summer visit to the palace Wilhelmshöhe, Feodora was urged by her kinsman Emperor Wilhelm II to make a match with the widowed Wilhelm Ernst, Grand Duke of Saxe-Weimar-Eisenach.
This was seen by many to be due to mutual ill will between Wilhelm and Feodora's grandfather Georg II, Duke of Saxe-Meiningen, whose morganatic wedding to Ellen Franz had displeased many royal personages like Wilhelm.
Wilhelm's disapproval was even more surprising in that he had recently allowed the marriage between a Hohenzollern dynast (Prince Frederick William of Prussia) with a much lower-ranked member of the nobility (Princess Agatha of Hohenlohe-Schillingsfürst); it was considered odd that he refused to recognize one equal marriage yet acknowledged another lesser match, especially when the latter was within his own family and subject to the rigid Hohenzollern house laws.
The Emperor's boycott of the wedding was so strongly resented in Saxe-Meiningen that, when newspapers announced that Wilhelm would not be attending the wedding, the official communication from the royal palace declared that he had never been invited.
On 14 January 1910 in Meiningen, Feodora was married to Wilhelm Ernst.
She was his second wife (his first wife Princess Caroline Reuss, Elder Line had died childless after eighteen months of marriage in 1905).
Court life


Feodora's marriage was unhappy; the Weimar court was generally considered to be one of the most stifling and etiquette-driven in Germany.
Feodora was unhappy in such an environment; at the age of 23, reports leaked out that she was staying at a sanatorium for her health.
Feodora was very popular among the middle and lower classes of Weimar; this was largely attributed to her charm and kindness to the poor and suffering.
Feodora died on 12 March 1972 in Freiburg
Issue

Feodora and her husband had four children:


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
  AssignClass (986f95dc-0ccd-4bb0-8ed4-cdb2352559d7)
 Call ID: 986f95dc-0ccd-4bb0-8ed4-cdb2352559d7
  Args:
    type: :Woman
    source: Feodora_of_Saxe-Meiningen
  AssignClass (4393eb5c-fa95-469a-822e-90fc3b543a1a)
 Call ID: 4393eb5c-fa95-469a-822e-90fc3b543a1a
  Args:
    type: :Person
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (b0418780-1a5a-46b6-8886-7074624513e5)
 Call ID: b0418780-1a5a-46b6-8886-7074624513e5
  Args:
    literal_value: Feodora Karola Charlotte Marie Adelheid Auguste Mathilde
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Feodora_of_Saxe-Meiningen
  AddLiteral (cec63720-f568-491f-a9b8-28f4a9f52edf)
 Call ID: cec63720-f568-491f-a9b8-28f4a9f52edf
  Args:
    relation: :hasBirthYear
    source: Feodora_of_Saxe-Meiningen
    literal_value: 1890
    literal_type: xsd:integer
  AddLiteral (79ba698a-f44d-4c06-adc9-4d3732d70c8b)
 Call ID: 79ba698a-f44d-4c06-adc9-4d3732d70c8b
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    source: Feodora_of_Saxe-Meiningen
    relation: :hasDeathYear
  AddLiteral (dcae3475-9067-4c2d-8da1-424ec7038fc0)
 Call ID: dcae3475-9067-4c2d-8da1-424ec7038fc0
  Args:
    source: Feodora_of_Saxe-Meiningen
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Grand Duchess of Saxe-Weimar-Eisenach
  AssignClass (9ccfd1ea-017f-4d08-ac2c-28f986f0bae0)
 Call ID: 9ccfd1ea-017f-4d08-ac2c-28f986f0bae0
  Args:
    type: :Man
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (75d339f8-63c4-40f8-85dd-dc346f05c2be)
 Call ID: 75d339f8-63c4-40f8-85dd-dc346f05c2be
  Args:
    type: :Person
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (a5d21871-3e53-4961-8576-3c8b59d8a825)
 Call ID: a5d21871-3e53-4961-8576-3c8b59d8a825
  Args:
    type: :Ancestor
    source: Friedrich_Johann_of_Saxe-Meiningen
  AddTriple (decda5b2-f4e6-4953-9680-0474ecf403b1)
 Call ID: decda5b2-f4e6-4953-9680-0474ecf403b1
  Args:
    relation: :hasFather
    target: Friedrich_Johann_of_Saxe-Meiningen
    source: Feodora_of_Saxe-Meiningen
  AssignClass (924ad5fa-2a03-416f-954d-c9db83b7da73)
 Call ID: 924ad5fa-2a03-416f-954d-c9db83b7da73
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (98e303e6-8c7d-442a-8b51-332c744c8261)
 Call ID: 98e303e6-8c7d-442a-8b51-332c744c8261
  Args:
    type: :Person
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (cc83a2dc-beb1-4664-b0ac-c573ed7052c1)
 Call ID: cc83a2dc-beb1-4664-b0ac-c573ed7052c1
  Args:
    type: :Ancestor
    source: Georg_II_Duke_of_Saxe-Meiningen
  AddTriple (ec7f1221-f80a-43ee-821a-ea9e630a8c4b)
 Call ID: ec7f1221-f80a-43ee-821a-ea9e630a8c4b
  Args:
    relation: :hasFather
    target: Georg_II_Duke_of_Saxe-Meiningen
    source: Friedrich_Johann_of_Saxe-Meiningen
  AssignClass (40252243-4c5e-4097-bbcc-b45b7f7ff7e0)
 Call ID: 40252243-4c5e-4097-bbcc-b45b7f7ff7e0
  Args:
    type: :Woman
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (2ec20eff-1f16-4cbe-846a-0c86a8dfff46)
 Call ID: 2ec20eff-1f16-4cbe-846a-0c86a8dfff46
  Args:
    type: :Person
    source: Adelaide_of_Lippe-Biesterfeld
  AssignClass (8e253b70-0260-469d-9a91-82c50fdcaaf6)
 Call ID: 8e253b70-0260-469d-9a91-82c50fdcaaf6
  Args:
    type: :Ancestor
    source: Adelaide_of_Lippe-Biesterfeld
  AddTriple (c1c909ec-bce7-403b-a926-fabf1616b5a6)
 Call ID: c1c909ec-bce7-403b-a926-fabf1616b5a6
  Args:
    target: Adelaide_of_Lippe-Biesterfeld
    source: Feodora_of_Saxe-Meiningen
    relation: :hasMother
  AssignClass (b8696c38-6829-4d90-ac23-a77dee3abda8)
 Call ID: b8696c38-6829-4d90-ac23-a77dee3abda8
  Args:
    type: :Man
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (e4ad0f49-00d0-400f-ba0d-00af09211d1a)
 Call ID: e4ad0f49-00d0-400f-ba0d-00af09211d1a
  Args:
    type: :Person
    source: Ernst_Count_of_Lippe-Biesterfeld
  AssignClass (d13da3c4-9790-4aaf-9e1b-9e11d9dacba0)
 Call ID: d13da3c4-9790-4aaf-9e1b-9e11d9dacba0
  Args:
    type: :Ancestor
    source: Ernst_Count_of_Lippe-Biesterfeld
  AddTriple (1f4e8ad5-7461-4069-9d56-d6454de98345)
 Call ID: 1f4e8ad5-7461-4069-9d56-d6454de98345
  Args:
    source: Adelaide_of_Lippe-Biesterfeld
    target: Ernst_Count_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (40fab092-3521-4049-90e6-4f58463adbc3)
 Call ID: 40fab092-3521-4049-90e6-4f58463adbc3
  Args:
    type: :Man
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AssignClass (343ff063-a777-4ee9-821b-c859d9e595b4)
 Call ID: 343ff063-a777-4ee9-821b-c859d9e595b4
  Args:
    type: :Person
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
  AddLiteral (20bf83fd-f8fc-4657-9076-dff7833122d6)
 Call ID: 20bf83fd-f8fc-4657-9076-dff7833122d6
  Args:
    literal_value: 1910
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Feodora_of_Saxe-Meiningen
  AddTriple (b278d3fa-3597-4a7f-9cc6-6a7fa4a81b7e)
 Call ID: b278d3fa-3597-4a7f-9cc6-6a7fa4a81b7e
  Args:
    source: Feodora_of_Saxe-Meiningen
    target: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
    relation: :hasRelation
  AssignClass (9767af2a-ef58-4ccf-bfa0-1d79227b8f21)
 Call ID: 9767af2a-ef58-4ccf-bfa0-1d79227b8f21
  Args:
    type: :Woman
    source: Caroline_Reuss_Elder_Line
  AssignClass (c4fa3369-38b3-40a0-98d9-043c2dd2c95a)
 Call ID: c4fa3369-38b3-40a0-98d9-043c2dd2c95a
  Args:
    type: :Person
    source: Caroline_Reuss_Elder_Line
  AddTriple (7818e412-580b-42d9-acf6-a00b7f77681b)
 Call ID: 7818e412-580b-42d9-acf6-a00b7f77681b
  Args:
    relation: :hasRelation
    source: Wilhelm_Ernst_Grand_Duke_of_Saxe-Weimar-Eisenach
    target: Caroline_Reuss_Elder_Line
  AssignClass (ed8a7742-a328-473b-be2f-048a640869c7)
 Call ID: ed8a7742-a328-473b-be2f-048a640869c7
  Args:
    type: :Woman
    source: Ellen_Franz
  AssignClass (d528ef9f-7e4c-4545-9fbd-53308cc4b53b)
 Call ID: d528ef9f-7e4c-4545-9fbd-53308cc4b53b
  Args:
    type: :Person
    source: Ellen_Franz
  AddTriple (b0ba3a50-c361-4d80-a1e8-953225dc1761)
 Call ID: b0ba3a50-c361-4d80-a1e8-953225dc1761
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    target: Ellen_Franz
    relation: :hasRelation
  AssignClass (cce1da7e-046a-4e5b-9418-a9610f7839ab)
 Call ID: cce1da7e-046a-4e5b-9418-a9610f7839ab
  Args:
    type: :Man
    source: Wilhelm_II_Emperor
  AssignClass (335aafc1-3493-4347-9a0b-e80baed426e6)
 Call ID: 335aafc1-3493-4347-9a0b-e80baed426e6
  Args:
    type: :Person
    source: Wilhelm_II_Emperor
  AssignClass (49d2af15-22bb-435a-8d21-391f5ee4c0c4)
 Call ID: 49d2af15-22bb-435a-8d21-391f5ee4c0c4
  Args:
    type: :Man
    source: Prince_Frederick_William_of_Prussia
  AssignClass (54c3fdfc-2789-47f6-a871-5edbb4b10f54)
 Call ID: 54c3fdfc-2789-47f6-a871-5edbb4b10f54
  Args:
    type: :Person
    source: Prince_Frederick_William_of_Prussia
  AssignClass (ac78b7f4-acd2-4617-8eb8-d1fc24bffdc6)
 Call ID: ac78b7f4-acd2-4617-8eb8-d1fc24bffdc6
  Args:
    type: :Woman
    source: Princess_Agatha_of_Hohenlohe-Schillingsfürst
  AssignClass (352274bc-1d03-4625-b690-4c4845d2e5e1)
 Call ID: 352274bc-1d03-4625-b690-4c4845d2e5e1
  Args:
    type: :Person
    source: Princess_Agatha_of_Hohenlohe-Schillingsfürst
  AddTriple (3c150d08-d369-45c6-8d94-5317e8a14f51)
 Call ID: 3c150d08-d369-45c6-8d94-5317e8a14f51
  Args:
    source: Prince_Frederick_William_of_Prussia
    target: Princess_Agatha_of_Hohenlohe-Schillingsfürst
    relation: :hasRelation
  Finish (fd4b8fb8-15db-404a-bb99-01e9ca49a8ec)
 Call ID: fd4b8fb8-15db-404a-bb99-01e9ca49a8ec
  Args: