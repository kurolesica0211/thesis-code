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
Carl Herzog von Württemberg (Carl Maria Peter Ferdinand Philipp Albrecht Joseph Michael Pius Konrad Robert Ulrich; 1 August 1936 – 7 June 2022) was the head of the House of Württemberg from 1975 to 2022.
He was the second son of Philipp Albrecht, Duke of Württemberg, and Archduchess Rosa of Austria, Princess of Tuscany.
Carl became heir-presumptive to the headship of the House of Württemberg on 29 June 1959, when his older brother, Ludwig, renounced his succession rights.
It also maintains some seventy cultural monuments of the House of Württemberg.
Charitable activities

Carl took part in many social and charitable activities, including the German Red Cross, the Friends of Cancer Children, the Free School Foundation, the Art Foundation, the Preventive Youth Welfare Foundation, and the Baden-Württemberg Monument Foundation, which he chaired from 2002 to 2008.
He was Patron of the Society for the Promotion of the State Museum of Württemberg, and chairman of the Friends of the University of Tübingen and the University Foundation.
Marriage and issue

On 21 July 1960, Carl married Princess Diane d'Orléans, the daughter of Prince Henri, Count of Paris, and his wife Princess Isabelle of Orléans-Braganza.
The wedding took place at Schloss Altshausen, the ancestral seat of the Dukes of Württemberg.
They had four sons and two daughters and sixteen grandchildren:


Honours and awards

House of Württemberg

States

Formerly reigning families

Religious orders

Academic institutions

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
  AssignClass (3f43e4a0-b660-477b-8c1f-ca46ee6738dd)
 Call ID: 3f43e4a0-b660-477b-8c1f-ca46ee6738dd
  Args:
    source: Carl_Herzog_von_Württemberg
    type: :Man
  AssignClass (7a07b616-d6df-4b67-847f-2cd4bced1782)
 Call ID: 7a07b616-d6df-4b67-847f-2cd4bced1782
  Args:
    source: Philipp_Albrecht_Duke_of_Württemberg
    type: :Man
  AssignClass (70ebfc7e-132e-4de5-8a74-1f1897b1b9e2)
 Call ID: 70ebfc7e-132e-4de5-8a74-1f1897b1b9e2
  Args:
    type: :Woman
    source: Rosa_of_Austria
  AssignClass (ba3897ce-9d23-4224-a3ac-ebcdb07a9e9f)
 Call ID: ba3897ce-9d23-4224-a3ac-ebcdb07a9e9f
  Args:
    type: :Man
    source: Ludwig_Württemberg
  AssignClass (1b49c694-5a7c-4023-8b00-7a3d07999b43)
 Call ID: 1b49c694-5a7c-4023-8b00-7a3d07999b43
  Args:
    source: Diane_dOrléans
    type: :Woman
  AssignClass (de39309e-8e10-47c6-903c-59e665ccdf44)
 Call ID: de39309e-8e10-47c6-903c-59e665ccdf44
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (9fd31785-8648-4513-96bd-e6e509053c09)
 Call ID: 9fd31785-8648-4513-96bd-e6e509053c09
  Args:
    type: :Woman
    source: Isabelle_of_Orléans-Braganza
  AddLiteral (dc6b2a02-354e-4d1b-a1e6-917660c37d3d)
 Call ID: dc6b2a02-354e-4d1b-a1e6-917660c37d3d
  Args:
    relation: :hasBirthYear
    source: Carl_Herzog_von_Württemberg
    literal_type: xsd:integer
    literal_value: 1936
  AddLiteral (448d214f-f18f-49d1-8ec2-05b75770ebb2)
 Call ID: 448d214f-f18f-49d1-8ec2-05b75770ebb2
  Args:
    literal_value: 2022
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Carl_Herzog_von_Württemberg
  AddTriple (d1231704-6115-4df9-97f1-ff91b3d7fa6d)
 Call ID: d1231704-6115-4df9-97f1-ff91b3d7fa6d
  Args:
    source: Carl_Herzog_von_Württemberg
    relation: :hasFather
    target: Philipp_Albrecht_Duke_of_Württemberg
  AddTriple (b64752b5-2349-42b4-9ce6-4dc70892559d)
 Call ID: b64752b5-2349-42b4-9ce6-4dc70892559d
  Args:
    source: Carl_Herzog_von_Württemberg
    relation: :hasMother
    target: Rosa_of_Austria
  AddTriple (56370435-3b69-4e98-a5a9-9c8a07ed1d76)
 Call ID: 56370435-3b69-4e98-a5a9-9c8a07ed1d76
  Args:
    source: Ludwig_Württemberg
    target: Carl_Herzog_von_Württemberg
    relation: :isBrotherOf
  AddTriple (a948d08d-a195-4e81-bbf6-0e7d8e624b61)
 Call ID: a948d08d-a195-4e81-bbf6-0e7d8e624b61
  Args:
    target: Philipp_Albrecht_Duke_of_Württemberg
    relation: :hasFather
    source: Carl_Herzog_von_Württemberg
  AddTriple (cf037489-efdc-49c3-a721-333b59d4376d)
 Call ID: cf037489-efdc-49c3-a721-333b59d4376d
  Args:
    target: Rosa_of_Austria
    relation: :hasMother
    source: Carl_Herzog_von_Württemberg
  AddTriple (79bcfdea-01e6-4df0-bb19-93dd9495b829)
 Call ID: 79bcfdea-01e6-4df0-bb19-93dd9495b829
  Args:
    relation: :hasFather
    target: Philipp_Albrecht_Duke_of_Württemberg
    source: Carl_Herzog_von_Württemberg
  AddTriple (f5fe1d14-550f-4561-aba1-ae41b2c37950)
 Call ID: f5fe1d14-550f-4561-aba1-ae41b2c37950
  Args:
    source: Carl_Herzog_von_Württemberg
    target: Rosa_of_Austria
    relation: :hasMother
  AddTriple (b9fc7aef-b2e9-4894-8475-f4eefe5a9a11)
 Call ID: b9fc7aef-b2e9-4894-8475-f4eefe5a9a11
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Diane_dOrléans
  AddTriple (0b0ee099-c914-4d56-9b07-e0169917247e)
 Call ID: 0b0ee099-c914-4d56-9b07-e0169917247e
  Args:
    source: Diane_dOrléans
    target: Isabelle_of_Orléans-Braganza
    relation: :hasMother
  AddLiteral (2af98eeb-08ce-408a-ba45-8633a29a1419)
 Call ID: 2af98eeb-08ce-408a-ba45-8633a29a1419
  Args:
    literal_value: 1960
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Carl_Herzog_von_Württemberg
  Finish (70d3e6b8-bff6-4557-bb8b-7ab8fad9494b)
 Call ID: 70d3e6b8-bff6-4557-bb8b-7ab8fad9494b
  Args: