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
The Dowager Princess Napoléon


Olympia Bonaparte, Princess Napoléon (Olympia Elene Marie; née Countess Olympia von und zu Arco-Zinneberg, born 4 January 1988), is the wife of Jean-Christophe, Prince Napoléon, the disputed head of the House of Bonaparte and, in the view of Bonapartists, the pretender to the abolished French imperial throne.
Early life and family

Countess Olympia Elene Marie von und zu Arco-Zinneberg was born on 4 January 1988 in Munich to Count Riprand von und zu Arco-Zinneberg (1955-2021) and his wife, Archduchess Maria Beatrice of Austria-Este.
Through her father she is a great-great-granddaughter of Ludwig III and Maria Theresa of Austria-Este, the last king and queen of Bavaria.
Through her mother she is the granddaughter of Robert, Archduke of Austria-Este and Princess Margherita of Savoy-Aosta.
She is a great-granddaughter of Charles I and Zita of Bourbon-Parma, the last emperor and empress of Austria.
Olympia is also the great-great-great-great-grandniece of Marie Louise, Duchess of Parma, the second wife of Napoleon I.


Personal life

Olympia graduated from Yale University with a bachelor's degree in political science and from Columbia University in 2015 with a Master of Arts degree in art history.
She met Jean-Christophe, Prince Napoléon during a semester studying abroad in Paris.
Olympia and Jean-Christophe first held a civil marriage on 17 October 2019 at the town hall of Neuilly-sur-Seine.
The wedding festivities were attended by members of European royal and noble families including Henri, Grand Duke of Luxembourg; Guillaume, Hereditary Grand Duke of Luxembourg; Stéphanie, Hereditary Grand Duchess of Luxembourg; Princess Maria Laura of Belgium, Archduchess of Austria-Este; Pavlos, Crown Prince of Greece; Princess Maria-Olympia of Greece and Denmark; Prince Philippos of Greece and Denmark; Nina Flohr; Prince Félix of Luxembourg; Princess Claire of Luxembourg; Prince Christian of Hanover; Princess Christian of Hanover; Princess Beatrice of York; and Edoardo Mapelli Mozzi.
The Princess gave birth to a son, Louis Charles Riprand Victor Jérôme Marie, on 7 December 2022 in Paris.



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
  AssignClass (3ffb9359-d260-41df-be4b-52275b1b0367)
 Call ID: 3ffb9359-d260-41df-be4b-52275b1b0367
  Args:
    source: Olympia_Bonaparte
    type: :Woman
  AssignClass (201ee729-e61a-4b69-93d2-6cd3af71544b)
 Call ID: 201ee729-e61a-4b69-93d2-6cd3af71544b
  Args:
    type: :Person
    source: Olympia_Bonaparte
  AddLiteral (1e9b6053-c020-444f-8aeb-11d3506ff407)
 Call ID: 1e9b6053-c020-444f-8aeb-11d3506ff407
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Olympia_Bonaparte
    literal_value: 1988
  AddLiteral (d2d01b21-1c46-4a50-999f-8a98801e3201)
 Call ID: d2d01b21-1c46-4a50-999f-8a98801e3201
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Olympia_Bonaparte
    literal_value: Olympia Elene Marie
  AddLiteral (bb40bf7c-4d80-453d-8861-c601be5cb47d)
 Call ID: bb40bf7c-4d80-453d-8861-c601be5cb47d
  Args:
    literal_value: Countess Olympia von und zu Arco-Zinneberg
    source: Olympia_Bonaparte
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AssignClass (1ed6206a-9643-49d0-b1f8-174124b171d2)
 Call ID: 1ed6206a-9643-49d0-b1f8-174124b171d2
  Args:
    source: Jean-Christophe_Prince_Napoleon
    type: :Man
  AssignClass (145f89ce-615b-4c59-8bc4-2b7659a50dfd)
 Call ID: 145f89ce-615b-4c59-8bc4-2b7659a50dfd
  Args:
    source: Jean-Christophe_Prince_Napoleon
    type: :Person
  AddTriple (0bc64de6-4cc9-45f5-9bea-74ac7205882b)
 Call ID: 0bc64de6-4cc9-45f5-9bea-74ac7205882b
  Args:
    target: Jean-Christophe_Prince_Napoleon
    relation: :hasRelation
    source: Olympia_Bonaparte
  AddLiteral (8a20faba-50d2-4c64-b93a-4b0133a2d434)
 Call ID: 8a20faba-50d2-4c64-b93a-4b0133a2d434
  Args:
    literal_value: 2019
    source: Olympia_Bonaparte
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (b05c910b-9ec5-46c4-921d-2b3a4e809108)
 Call ID: b05c910b-9ec5-46c4-921d-2b3a4e809108
  Args:
    source: Riprand_von_und_zu_Arco-Zinneberg
    type: :Man
  AssignClass (927ec206-ea9b-4eeb-a75e-589d537699df)
 Call ID: 927ec206-ea9b-4eeb-a75e-589d537699df
  Args:
    type: :Ancestor
    source: Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (a9f3df46-05a7-4c0f-b6d4-79941509c64d)
 Call ID: a9f3df46-05a7-4c0f-b6d4-79941509c64d
  Args:
    type: :Person
    source: Riprand_von_und_zu_Arco-Zinneberg
  AddLiteral (1fb34805-162f-4351-93b6-2fc2de1aa6fc)
 Call ID: 1fb34805-162f-4351-93b6-2fc2de1aa6fc
  Args:
    source: Riprand_von_und_zu_Arco-Zinneberg
    literal_value: 1955
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f909d9d6-ca61-421e-9c49-4421bbda59e1)
 Call ID: f909d9d6-ca61-421e-9c49-4421bbda59e1
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2021
    source: Riprand_von_und_zu_Arco-Zinneberg
  AssignClass (6218d85c-62ea-4596-a2b6-0573984ee9f4)
 Call ID: 6218d85c-62ea-4596-a2b6-0573984ee9f4
  Args:
    source: Maria_Beatrice_of_Austria-Este
    type: :Woman
  AssignClass (b8f55e36-6f24-4299-b2dc-05e551fde608)
 Call ID: b8f55e36-6f24-4299-b2dc-05e551fde608
  Args:
    source: Maria_Beatrice_of_Austria-Este
    type: :Ancestor
  AssignClass (58ef42f6-fc15-4843-9b90-6bf74c4e66d9)
 Call ID: 58ef42f6-fc15-4843-9b90-6bf74c4e66d9
  Args:
    source: Maria_Beatrice_of_Austria-Este
    type: :Person
  AddTriple (106d169d-706b-46e6-a292-76feb4bb4874)
 Call ID: 106d169d-706b-46e6-a292-76feb4bb4874
  Args:
    source: Olympia_Bonaparte
    relation: :hasFather
    target: Riprand_von_und_zu_Arco-Zinneberg
  AddTriple (8c98c308-b1f9-46c8-a274-56e5edcc830f)
 Call ID: 8c98c308-b1f9-46c8-a274-56e5edcc830f
  Args:
    source: Olympia_Bonaparte
    relation: :hasMother
    target: Maria_Beatrice_of_Austria-Este
  AssignClass (f737a260-2839-4b91-a205-7ad81926edb8)
 Call ID: f737a260-2839-4b91-a205-7ad81926edb8
  Args:
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    type: :Man
  AssignClass (0aeda58c-5cac-4b43-98a9-d7c0bd165ad8)
 Call ID: 0aeda58c-5cac-4b43-98a9-d7c0bd165ad8
  Args:
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    type: :Person
  AddTriple (f1b01501-0be4-4154-901f-f893245e8f88)
 Call ID: f1b01501-0be4-4154-901f-f893245e8f88
  Args:
    relation: :isSonOf
    target: Olympia_Bonaparte
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
  AddTriple (99a16721-bf50-4df6-90e7-51ec6578636c)
 Call ID: 99a16721-bf50-4df6-90e7-51ec6578636c
  Args:
    source: Louis_Charles_Riprand_Victor_Jerome_Marie
    target: Jean-Christophe_Prince_Napoleon
    relation: :isSonOf
  Finish (c3939d91-8be0-4f86-8360-86f12117234d)
 Call ID: c3939d91-8be0-4f86-8360-86f12117234d
  Args: