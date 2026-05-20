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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Floris Frederik Martijn of Orange-Nassau, van Vollenhoven (born 10 April 1975) is the fourth and youngest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Prince Floris has three older brothers: Prince Maurits, Prince Bernhard, Prince Pieter-Christiaan


Marriage and children

Prince Floris announced his engagement to Aimée Söhngen, the daughter of Hans Söhngen and Eleonoor Stammeijer, on 25 February 2005.
Prince Floris had been 10th in the line of succession to the Dutch throne but decided not to seek parliamentary approval for his marriage, as would be required in the Netherlands.
Prince Floris and Princess Aimée's first child, Magali Margriet Eleonoor van Vollenhoven, was born at VU University Medical Center in Amsterdam on 9 October 2007.
She is named for Aimée's sister, Magali Söhngen, and her mother Eleonoor, as well as Princess Margriet.
Their second child, Eliane Sophia Carolina van Vollenhoven, was born at VU University Medical Center in Amsterdam on 5 July 2009.
Their third child, a son named Willem Jan Johannes Pieter Floris, was born at HMC Bronovo  in The Hague on 1 July 2013.
Ancestry

References

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (26787c4a-49d6-4fc7-b62a-c1214ec48e28)
 Call ID: 26787c4a-49d6-4fc7-b62a-c1214ec48e28
  Args:
    type: :Woman
    source: Princess_Margriet
  AssignClass (735b0786-4798-4d52-8f79-103860926883)
 Call ID: 735b0786-4798-4d52-8f79-103860926883
  Args:
    type: :Man
    source: Pieter_van_Vollenhoven
  AssignClass (668f5085-93d3-493c-bccd-1044a2b60e00)
 Call ID: 668f5085-93d3-493c-bccd-1044a2b60e00
  Args:
    type: :Man
    source: Prince_Floris
  AssignClass (244d43e8-e3e6-48f2-86a2-14b1dcc59d79)
 Call ID: 244d43e8-e3e6-48f2-86a2-14b1dcc59d79
  Args:
    source: Prince_Maurits
    type: :Man
  AssignClass (4ff785c6-e73d-49bb-b007-abb16ff5e369)
 Call ID: 4ff785c6-e73d-49bb-b007-abb16ff5e369
  Args:
    source: Prince_Bernhard
    type: :Man
  AssignClass (bdba019b-a0a1-4cec-b1fc-375090b7dcd3)
 Call ID: bdba019b-a0a1-4cec-b1fc-375090b7dcd3
  Args:
    source: Prince_Pieter-Christiaan
    type: :Man
  AssignClass (74a19951-bffd-42d6-996a-91f37b802f17)
 Call ID: 74a19951-bffd-42d6-996a-91f37b802f17
  Args:
    type: :Woman
    source: Aimée_Söhngen
  AssignClass (b6802932-57e2-4cf3-a1b6-5ec652b1eed6)
 Call ID: b6802932-57e2-4cf3-a1b6-5ec652b1eed6
  Args:
    source: Hans_Söhngen
    type: :Man
  AssignClass (a4362d2c-4ae7-4dcd-8555-cdea719b25b4)
 Call ID: a4362d2c-4ae7-4dcd-8555-cdea719b25b4
  Args:
    source: Eleonoor_Stammeijer
    type: :Woman
  AssignClass (119530b1-3d67-459c-a9f8-f93b71e7a70f)
 Call ID: 119530b1-3d67-459c-a9f8-f93b71e7a70f
  Args:
    source: Magali_Margriet_Eleonoor_van_Vollenhoven
    type: :Woman
  AssignClass (24fc8b15-a52b-4d2d-baa4-c85191fb3978)
 Call ID: 24fc8b15-a52b-4d2d-baa4-c85191fb3978
  Args:
    type: :Woman
    source: Eliane_Sophia_Carolina_van_Vollenhoven
  AssignClass (0005b68b-521b-49c0-bde3-b65104feab3c)
 Call ID: 0005b68b-521b-49c0-bde3-b65104feab3c
  Args:
    type: :Man
    source: Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AddLiteral (9df9c188-61fe-4d19-98e0-825783429010)
 Call ID: 9df9c188-61fe-4d19-98e0-825783429010
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Floris
    literal_value: 1975
  AddTriple (8edd3d43-06f6-4aca-a0c5-02e0df9ec1ef)
 Call ID: 8edd3d43-06f6-4aca-a0c5-02e0df9ec1ef
  Args:
    target: Princess_Margriet
    relation: :hasMother
    source: Prince_Floris
  AddTriple (2e1a046a-20f1-4f6d-8207-9c8f6fdcedb0)
 Call ID: 2e1a046a-20f1-4f6d-8207-9c8f6fdcedb0
  Args:
    source: Prince_Floris
    relation: :hasFather
    target: Pieter_van_Vollenhoven
  AddTriple (7ee62f8c-2b87-47d7-a520-0a8a8466da8f)
 Call ID: 7ee62f8c-2b87-47d7-a520-0a8a8466da8f
  Args:
    source: Prince_Floris
    target: Prince_Maurits
    relation: :isBrotherOf
  AddTriple (eb4611c8-bc88-495d-a445-c213e890cfb7)
 Call ID: eb4611c8-bc88-495d-a445-c213e890cfb7
  Args:
    source: Prince_Floris
    target: Prince_Bernhard
    relation: :isBrotherOf
  AddTriple (47d0e9a7-fb14-443b-9d21-be5c44f264a4)
 Call ID: 47d0e9a7-fb14-443b-9d21-be5c44f264a4
  Args:
    target: Prince_Pieter-Christiaan
    relation: :isBrotherOf
    source: Prince_Floris
  AddTriple (21c42419-c53f-4e11-8cb9-afe608d2bf59)
 Call ID: 21c42419-c53f-4e11-8cb9-afe608d2bf59
  Args:
    source: Aimée_Söhngen
    target: Eleonoor_Stammeijer
    relation: :hasMother
  AddTriple (c9f254cf-b59a-4135-a890-10e0849abd1f)
 Call ID: c9f254cf-b59a-4135-a890-10e0849abd1f
  Args:
    source: Aimée_Söhngen
    relation: :hasFather
    target: Hans_Söhngen
  AddTriple (f3ef2ef0-d717-4c03-9995-85494097f1fe)
 Call ID: f3ef2ef0-d717-4c03-9995-85494097f1fe
  Args:
    relation: :hasMother
    target: Aimée_Söhngen
    source: Magali_Margriet_Eleonoor_van_Vollenhoven
  AddTriple (a5d51b81-99e7-48bd-b5cd-8bbf26c2a457)
 Call ID: a5d51b81-99e7-48bd-b5cd-8bbf26c2a457
  Args:
    source: Magali_Margriet_Eleonoor_van_Vollenhoven
    relation: :hasFather
    target: Prince_Floris
  AddTriple (03f4e2e8-c1ae-4479-9eed-0c8e893ec4bd)
 Call ID: 03f4e2e8-c1ae-4479-9eed-0c8e893ec4bd
  Args:
    source: Eliane_Sophia_Carolina_van_Vollenhoven
    target: Aimée_Söhngen
    relation: :hasMother
  AddTriple (a072f102-2a58-4614-93d5-daf0b1b85417)
 Call ID: a072f102-2a58-4614-93d5-daf0b1b85417
  Args:
    source: Eliane_Sophia_Carolina_van_Vollenhoven
    target: Prince_Floris
    relation: :hasFather
  AddTriple (118b0ac8-4452-4533-a568-f4ae2efb8e5b)
 Call ID: 118b0ac8-4452-4533-a568-f4ae2efb8e5b
  Args:
    target: Aimée_Söhngen
    relation: :hasMother
    source: Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AddTriple (2b38ae59-6ab4-4f1a-872b-bc77c813afa0)
 Call ID: 2b38ae59-6ab4-4f1a-872b-bc77c813afa0
  Args:
    source: Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
    target: Prince_Floris
    relation: :hasFather
  Finish (0a0cb2d5-272a-4a7c-87a3-ffac8a71d284)
 Call ID: 0a0cb2d5-272a-4a7c-87a3-ffac8a71d284
  Args: