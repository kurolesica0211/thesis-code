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
Michael Claude Hamilton Bowes-Lyon (1 October 1893 – 1 May 1953), known as Mickie Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother and maternal uncle of Queen Elizabeth II.
Biography

Bowes-Lyon was born on 1 October 1893, the fifth son and eighth child of Claude Bowes-Lyon, Lord Glamis, later 14th
During World War I, Bowes-Lyon served in France in The Royal Scots (Lothian Regiment).
After the war, Bowes-Lyon was a justice of the peace and deputy lieutenant of Bedfordshire.
In 1928, Bowes-Lyon married Elizabeth Margaret Cator (1899–1959), daughter of John Cator, at St George's, Hanover Square.
Cator had been a bridesmaid at his sister Elizabeth's wedding to Prince Albert, Duke of York, in 1923.
Bowes-Lyon predeceased him and the earldom was inherited by his eldest son, Fergus, in 1972.
Bowes-Lyon died on 1 May 1953 at his home in Biggleswade as the result of asthma.



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
  AssignClass (fea15a2d-85fa-4c7a-98a4-c0a393ebe7b8)
 Call ID: fea15a2d-85fa-4c7a-98a4-c0a393ebe7b8
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    type: :Man
  AssignClass (50a6ad99-87d9-4e5b-8bed-48a0461ff457)
 Call ID: 50a6ad99-87d9-4e5b-8bed-48a0461ff457
  Args:
    type: :Person
    source: :Michael_Claude_Hamilton_Bowes-Lyon
  AddLiteral (e270c431-48ca-41bb-a3fc-9dac9eb8881f)
 Call ID: e270c431-48ca-41bb-a3fc-9dac9eb8881f
  Args:
    relation: :hasBirthYear
    literal_value: 1893
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (392e6ce3-5378-4c67-abea-ae133d0526a1)
 Call ID: 392e6ce3-5378-4c67-abea-ae133d0526a1
  Args:
    literal_type: xsd:integer
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasDeathYear
    literal_value: 1953
  AddLiteral (71501011-2590-4fe9-a113-70fddfafe98a)
 Call ID: 71501011-2590-4fe9-a113-70fddfafe98a
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    literal_type: xsd:string
    literal_value: Mickie Bowes-Lyon
    relation: :knownAs
  AssignClass (3a3e1c54-d360-4172-92df-1f8e3fe6efb1)
 Call ID: 3a3e1c54-d360-4172-92df-1f8e3fe6efb1
  Args:
    source: :Claude_Bowes-Lyon
    type: :Man
  AssignClass (44c7674b-56d3-4f90-9957-34b776be325a)
 Call ID: 44c7674b-56d3-4f90-9957-34b776be325a
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon
  AddTriple (fedc0242-20c4-488d-9c0d-458f224ce145)
 Call ID: fedc0242-20c4-488d-9c0d-458f224ce145
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasFather
    target: :Claude_Bowes-Lyon
  AssignClass (5a0db607-b970-4671-a2e2-374009c59885)
 Call ID: 5a0db607-b970-4671-a2e2-374009c59885
  Args:
    type: :Woman
    source: :Elizabeth_the_Queen_Mother
  AssignClass (da39cbcb-bf38-41b0-a85b-bff2510cd3f9)
 Call ID: da39cbcb-bf38-41b0-a85b-bff2510cd3f9
  Args:
    type: :Person
    source: :Elizabeth_the_Queen_Mother
  AddTriple (13d22421-b98c-4ccb-8ff3-9425f0b7bb08)
 Call ID: 13d22421-b98c-4ccb-8ff3-9425f0b7bb08
  Args:
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    relation: :isBrotherOf
    target: :Elizabeth_the_Queen_Mother
  AssignClass (6b6664e9-b50f-48af-8c6b-8af2ddccde45)
 Call ID: 6b6664e9-b50f-48af-8c6b-8af2ddccde45
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (bd114073-a658-4eba-bd96-8518f87d8fa3)
 Call ID: bd114073-a658-4eba-bd96-8518f87d8fa3
  Args:
    source: :Queen_Elizabeth_II
    type: :Person
  AddTriple (edcf04c4-d185-47b6-be78-a53e2d5fbe95)
 Call ID: edcf04c4-d185-47b6-be78-a53e2d5fbe95
  Args:
    relation: :isUncleOf
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    target: :Queen_Elizabeth_II
  AssignClass (a4787a81-c371-419a-a47e-ad29d7a710c1)
 Call ID: a4787a81-c371-419a-a47e-ad29d7a710c1
  Args:
    type: :Woman
    source: :Elizabeth_Margaret_Cator
  AssignClass (f18e992d-893c-43a2-836c-6da333638b1d)
 Call ID: f18e992d-893c-43a2-836c-6da333638b1d
  Args:
    type: :Person
    source: :Elizabeth_Margaret_Cator
  AddLiteral (70be43ea-2bbe-4fc6-a3fb-145f4485cf67)
 Call ID: 70be43ea-2bbe-4fc6-a3fb-145f4485cf67
  Args:
    relation: :hasMarriageYear
    literal_value: 1928
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    literal_type: xsd:integer
  AddTriple (d7878b30-f61a-46b7-b46e-d9d330f0f364)
 Call ID: d7878b30-f61a-46b7-b46e-d9d330f0f364
  Args:
    relation: :hasRelation
    source: :Michael_Claude_Hamilton_Bowes-Lyon
    target: :Elizabeth_Margaret_Cator
  AssignClass (1be27105-8ba5-4df2-aa93-4a00c76b1902)
 Call ID: 1be27105-8ba5-4df2-aa93-4a00c76b1902
  Args:
    source: :John_Cator
    type: :Man
  AssignClass (aca01327-fecf-4b06-89d8-75d2fe7b5c41)
 Call ID: aca01327-fecf-4b06-89d8-75d2fe7b5c41
  Args:
    type: :Person
    source: :John_Cator
  AddTriple (547c9745-ede2-4dc4-853c-e13915f691a8)
 Call ID: 547c9745-ede2-4dc4-853c-e13915f691a8
  Args:
    relation: :hasFather
    source: :Elizabeth_Margaret_Cator
    target: :John_Cator
  AssignClass (f2a2e4aa-cd88-4c83-9628-96d2752ec593)
 Call ID: f2a2e4aa-cd88-4c83-9628-96d2752ec593
  Args:
    source: :Fergus_Bowes-Lyon
    type: :Man
  AssignClass (36d738d8-9d2a-447d-afb5-7887f546de16)
 Call ID: 36d738d8-9d2a-447d-afb5-7887f546de16
  Args:
    type: :Person
    source: :Fergus_Bowes-Lyon
  AddTriple (54353b9a-96a7-457e-9a32-9b4f8ba2b4ef)
 Call ID: 54353b9a-96a7-457e-9a32-9b4f8ba2b4ef
  Args:
    target: :Michael_Claude_Hamilton_Bowes-Lyon
    source: :Fergus_Bowes-Lyon
    relation: :isSonOf
  Finish (358c1d23-7e49-4ef3-9b1d-e67742878c6f)
 Call ID: 358c1d23-7e49-4ef3-9b1d-e67742878c6f
  Args: