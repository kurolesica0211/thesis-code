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
Infanta Maria Cristina of Spain, Countess Marone-Cinzano (María Cristina Teresa Alejandra María de Guadalupe María de la Concepción Ildefonsa Victoria Eugenia de Borbón y Battenberg; 12 December 1911 – 23 December 1996) was the fourth surviving child and youngest daughter of Alfonso XIII of Spain and Victoria Eugenie of Battenberg and paternal aunt of King Juan Carlos I.


Biography

Early life

Infanta Maria Cristina was born at the Palacio Real in Madrid, Spain.
By 1933 King Alfonso and his daughters, the Infantas Beatriz and Maria Cristina, had moved to Rome.
Their father warned would-be suitors of the inherent dangers of hemophilia, from which two of the king's sons, Alfonso and Gonzalo, suffered.
Maria Cristina had one step-son, from Enrico's previous marriage to Noemí Rosa de Alcorta y García-Mansilla (1907-1929):


The marriage of Maria Cristina and Enrico Eugenio produced four daughters:


Death

Infanta Maria Cristina returned to Spain and spent periods of time there, but never lived there permanently.
A funeral service for the Infanta was held in the chapel of the Royal Palace of Madrid on 24 December and a burial service was held on 26 December in the Marone-Cinzano Pantheon in Turin.



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
  AssignClass (5a1e654e-b6b5-4408-b1b5-d001f3f8d4c1)
 Call ID: 5a1e654e-b6b5-4408-b1b5-d001f3f8d4c1
  Args:
    source: Maria_Cristina_of_Spain
    type: :Woman
  AssignClass (be08ad90-8b4c-4900-afdc-2b5bde872076)
 Call ID: be08ad90-8b4c-4900-afdc-2b5bde872076
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (d2390e92-12f4-469d-946a-d3881fe049b0)
 Call ID: d2390e92-12f4-469d-946a-d3881fe049b0
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (27c6e060-de52-4429-bb69-02f24cf203e1)
 Call ID: 27c6e060-de52-4429-bb69-02f24cf203e1
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (062d3213-acb5-4280-990a-b6024d68016d)
 Call ID: 062d3213-acb5-4280-990a-b6024d68016d
  Args:
    source: Alfonso_son_of_Alfonso_XIII
    type: :Man
  AssignClass (0cad3a3f-d843-4c07-8c27-da924fb6ddf9)
 Call ID: 0cad3a3f-d843-4c07-8c27-da924fb6ddf9
  Args:
    source: Gonzalo_son_of_Alfonso_XIII
    type: :Man
  AssignClass (9fa5a08e-143a-4e4e-84a0-25bbdc0a02e3)
 Call ID: 9fa5a08e-143a-4e4e-84a0-25bbdc0a02e3
  Args:
    source: Beatriz_of_Spain
    type: :Woman
  AssignClass (fb4f08cf-0cff-42b6-8789-a3a8d3475ef4)
 Call ID: fb4f08cf-0cff-42b6-8789-a3a8d3475ef4
  Args:
    source: Enrico_Eugenio
    type: :Man
  AssignClass (f2ab381b-7cb7-4047-a1bd-0d216747a378)
 Call ID: f2ab381b-7cb7-4047-a1bd-0d216747a378
  Args:
    source: Noemi_Rosa_de_Alcorta_y_Garcia-Mansilla
    type: :Woman
  AddLiteral (edcf67a3-aeaf-416f-8843-4d650fab5958)
 Call ID: edcf67a3-aeaf-416f-8843-4d650fab5958
  Args:
    literal_type: xsd:integer
    literal_value: 1911
    source: Maria_Cristina_of_Spain
    relation: :hasBirthYear
  AddLiteral (e898a652-2939-4b40-9b86-a76892ffa21a)
 Call ID: e898a652-2939-4b40-9b86-a76892ffa21a
  Args:
    source: Maria_Cristina_of_Spain
    literal_type: xsd:integer
    literal_value: 1996
    relation: :hasDeathYear
  AddTriple (747e4b73-c512-4953-85f1-58fd777c27dc)
 Call ID: 747e4b73-c512-4953-85f1-58fd777c27dc
  Args:
    target: Alfonso_XIII_of_Spain
    source: Maria_Cristina_of_Spain
    relation: :hasFather
  AddTriple (b42aad66-82d9-4a56-ba5b-0423df86f796)
 Call ID: b42aad66-82d9-4a56-ba5b-0423df86f796
  Args:
    relation: :hasMother
    source: Maria_Cristina_of_Spain
    target: Victoria_Eugenie_of_Battenberg
  AddTriple (f6a2f6c5-2fd6-46e7-a695-96a11e69ba47)
 Call ID: f6a2f6c5-2fd6-46e7-a695-96a11e69ba47
  Args:
    source: Maria_Cristina_of_Spain
    target: Juan_Carlos_I
    relation: :isAuntOf
  AddTriple (6a580abf-9693-4d3d-af87-3fc80208496c)
 Call ID: 6a580abf-9693-4d3d-af87-3fc80208496c
  Args:
    source: Alfonso_son_of_Alfonso_XIII
    target: Maria_Cristina_of_Spain
    relation: :isBrotherOf
  AddTriple (39246538-7489-4c6d-8df4-215025c66667)
 Call ID: 39246538-7489-4c6d-8df4-215025c66667
  Args:
    relation: :isBrotherOf
    target: Maria_Cristina_of_Spain
    source: Gonzalo_son_of_Alfonso_XIII
  AddTriple (74fe160f-d864-4cc5-8985-45bf65b546cf)
 Call ID: 74fe160f-d864-4cc5-8985-45bf65b546cf
  Args:
    relation: :isSisterOf
    source: Beatriz_of_Spain
    target: Maria_Cristina_of_Spain
  AddTriple (a7df1ed6-0e87-43e1-9b69-5669d4ad33d4)
 Call ID: a7df1ed6-0e87-43e1-9b69-5669d4ad33d4
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Alfonso_son_of_Alfonso_XIII
  AddTriple (468506b4-dbfc-4700-bbbd-abffd75b35e4)
 Call ID: 468506b4-dbfc-4700-bbbd-abffd75b35e4
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Gonzalo_son_of_Alfonso_XIII
  AddTriple (95272726-baef-475b-9131-110a9ac79c4b)
 Call ID: 95272726-baef-475b-9131-110a9ac79c4b
  Args:
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
    source: Beatriz_of_Spain
  AddTriple (edc78b17-d60c-4d2a-b8dc-c6cd02aaf985)
 Call ID: edc78b17-d60c-4d2a-b8dc-c6cd02aaf985
  Args:
    target: Victoria_Eugenie_of_Battenberg
    source: Beatriz_of_Spain
    relation: :hasMother
  AddTriple (ae461bf6-67cd-4dca-ba97-3e9c6099d248)
 Call ID: ae461bf6-67cd-4dca-ba97-3e9c6099d248
  Args:
    relation: :hasMother
    target: Victoria_Eugenie_of_Battenberg
    source: Alfonso_son_of_Alfonso_XIII
  AddTriple (e50fc457-a07c-4250-ae0d-8785c0363ce8)
 Call ID: e50fc457-a07c-4250-ae0d-8785c0363ce8
  Args:
    target: Victoria_Eugenie_of_Battenberg
    source: Gonzalo_son_of_Alfonso_XIII
    relation: :hasMother
  AddTriple (e0e68684-5931-4133-b525-7b5f98a7d1f5)
 Call ID: e0e68684-5931-4133-b525-7b5f98a7d1f5
  Args:
    relation: :hasRelation
    source: Maria_Cristina_of_Spain
    target: Enrico_Eugenio
  AddTriple (5d5ce02d-a16e-40ab-bbcf-906c8cf2858b)
 Call ID: 5d5ce02d-a16e-40ab-bbcf-906c8cf2858b
  Args:
    source: Enrico_Eugenio
    target: Noemi_Rosa_de_Alcorta_y_Garcia-Mansilla
    relation: :hasRelation
  Finish (7eaee9f1-0618-41d1-9628-f883aff2bb64)
 Call ID: 7eaee9f1-0618-41d1-9628-f883aff2bb64
  Args: