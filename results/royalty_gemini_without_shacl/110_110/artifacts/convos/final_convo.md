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
Maximilian, Margrave of Baden (Maximilian Andreas Friedrich Gustav Ernst August Bernhard Prinz und Markgraf von Baden; 3 July 1933 – 29 December 2022),  also known as Max von Baden, was a German businessman and the head of House of Baden.
Through his mother, Princess Theodora of Greece and Denmark, the second sister of Prince Philip, Duke of Edinburgh, he was a first cousin of Charles III, King of the United Kingdom.
Early life and family

Maximilian was born on 3 July 1933 in Salem.
He was the second child and eldest son of Berthold, Margrave of Baden, and his wife, Princess Theodora of Greece and Denmark.
He had one older sister, Princess Margarita, and has a younger brother, Prince Ludwig (born 1937).
Marriage and children

Maximilian was briefly engaged to his first cousin, Princess Beatrix of Hohenlohe-Langenburg (daughter of his maternal aunt, Margarita, Princess of Hohenlohe-Langenburg), although this was eventually broken off.
In 1963, he followed his father as head of the former grand ducal house of Baden, styled HRH
The Margrave of Baden, Duke of Zähringen.
In 1966, he married Archduchess Valerie of Austria (b. 1941), daughter of Archduke Hubert Salvator of Austria and his wife, Princess Rosemary of Salm-Salm.
The Margrave and Margravine had four children: 


The Margravine represented the Margrave for the funeral of Queen Elizabeth II, his aunt, at Westminster Abbey in London on 19 September 2022, with Prince Bernhard and his wife, Princess Stephanie.
He was succeeded as titular margrave and head of house by his son Bernhard.
The Margrave's funeral service on 13 January 2023 in the church of Salem Abbey was attended by numerous representatives from politics, including the minister president of Baden-Württemberg, Winfried Kretschmann, and royalty and aristocracy, such as King Philippe of Belgium, Prince Albert II of Monaco and his sister Caroline, Princess of Hanover, Prince Hassan of Jordan and the Hereditary Princess of Liechtenstein as well as the heads or representatives of most of the former ruling houses of Germany.
His first cousin King Charles III was represented by Donatus, Landgrave of Hesse.



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
  AssignClass (8c5d6b2e-857e-4b85-ac31-e9c9a24bb1fe)
 Call ID: 8c5d6b2e-857e-4b85-ac31-e9c9a24bb1fe
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Man
  AssignClass (2ca652f0-4cd8-452e-8fab-97ddb9e61f5d)
 Call ID: 2ca652f0-4cd8-452e-8fab-97ddb9e61f5d
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Man
  AssignClass (a5b52615-e6dc-4527-baee-cef937fd18e2)
 Call ID: a5b52615-e6dc-4527-baee-cef937fd18e2
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (6c281169-63fb-477c-8d98-aa84258fdf06)
 Call ID: 6c281169-63fb-477c-8d98-aa84258fdf06
  Args:
    source: Princess_Margarita_of_Baden
    type: :Woman
  AssignClass (78d3c22b-f031-4a7d-abdb-2dc82bff4876)
 Call ID: 78d3c22b-f031-4a7d-abdb-2dc82bff4876
  Args:
    source: Prince_Ludwig_of_Baden
    type: :Man
  AssignClass (cfcbe9e6-bbdb-412e-890e-ef39dad50338)
 Call ID: cfcbe9e6-bbdb-412e-890e-ef39dad50338
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (1db2d05c-46a1-48b8-bfb4-a7d43554beb0)
 Call ID: 1db2d05c-46a1-48b8-bfb4-a7d43554beb0
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Man
  AddLiteral (8e403053-59f0-4aa4-bd1a-3b5bb0663477)
 Call ID: 8e403053-59f0-4aa4-bd1a-3b5bb0663477
  Args:
    literal_value: 1933
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (dd340290-8d37-482e-bc04-66729e040ff2)
 Call ID: dd340290-8d37-482e-bc04-66729e040ff2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2022
    source: Maximilian_Margrave_of_Baden
  AddLiteral (8ab56fd3-df25-43e3-9f31-014b1ea6e266)
 Call ID: 8ab56fd3-df25-43e3-9f31-014b1ea6e266
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Maximilian_Margrave_of_Baden
    literal_value: Max von Baden
  AddTriple (8fc9be98-f656-45a8-958c-98b3dd2a3e6a)
 Call ID: 8fc9be98-f656-45a8-958c-98b3dd2a3e6a
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Berthold_Margrave_of_Baden
    relation: :hasFather
  AddTriple (c10ee827-b08f-4e3d-8b81-98636f703ef1)
 Call ID: c10ee827-b08f-4e3d-8b81-98636f703ef1
  Args:
    relation: :hasMother
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Maximilian_Margrave_of_Baden
  AddTriple (e363d98a-f301-415a-ade5-1681da4f2b3d)
 Call ID: e363d98a-f301-415a-ade5-1681da4f2b3d
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Princess_Margarita_of_Baden
    relation: :hasSister
  AddTriple (111c4a82-f780-4018-9751-76206d01c65d)
 Call ID: 111c4a82-f780-4018-9751-76206d01c65d
  Args:
    target: Prince_Ludwig_of_Baden
    relation: :hasBrother
    source: Maximilian_Margrave_of_Baden
  AddLiteral (5cef08e9-8ec3-4ef4-8ceb-54d6a865a505)
 Call ID: 5cef08e9-8ec3-4ef4-8ceb-54d6a865a505
  Args:
    literal_value: 1937
    source: Prince_Ludwig_of_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (aff5d63d-9215-4d65-a336-01e5f8992298)
 Call ID: aff5d63d-9215-4d65-a336-01e5f8992298
  Args:
    relation: :hasFather
    target: Maximilian_Margrave_of_Baden
    source: Bernhard_Margrave_of_Baden
  AddTriple (149299ac-530f-4bd1-a417-3b2c6661957d)
 Call ID: 149299ac-530f-4bd1-a417-3b2c6661957d
  Args:
    target: Archduchess_Valerie_of_Austria
    relation: :hasMother
    source: Bernhard_Margrave_of_Baden
  AddLiteral (f988d12c-a173-4108-8f02-bf788731f202)
 Call ID: f988d12c-a173-4108-8f02-bf788731f202
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1966
    source: Maximilian_Margrave_of_Baden
  AddTriple (da93005c-b517-4844-8759-93c2b043654d)
 Call ID: da93005c-b517-4844-8759-93c2b043654d
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasRelation
    target: Archduchess_Valerie_of_Austria
  Finish (cb9c586b-48ec-4c78-b858-e7352e92be82)
 Call ID: cb9c586b-48ec-4c78-b858-e7352e92be82
  Args: