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
Prince Gabriele of Bourbon-Two Sicilies (Gabriele Maria Giuseppe Carlo Ignazio Antonio Alfonso Pietro Giovanni Gerardo di Majella et Omni Sancti; 11 January 1897 – 22 October 1975) was a prince of the deposed dynasty which ruled the Kingdom of the Two Sicilies.
Family

Gabriel was the twelfth child and youngest son of Prince Alfonso, Count of Caserta, and his wife, Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage and issue

Gabriel married firstly Princess Malgorzata Izabella Czartoryska, daughter of Prince Adam Ludwik Czartoryski and Countess Maria Ludwika Krasińska, on 25 August 1927 in Paris.
The couple had one child before Malgorzata died in Cannes on 8 March 1929:


Gabriel married, secondly, Princess Cecylia Lubomirska, daughter of Prince Kasimierz Lubomirski and Countess Maria Theresia Granow-Wodicka, on 15 September 1932 in Kraków.



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
  AssignClass (e6e35022-84e1-414b-9685-8184ff807fa3)
 Call ID: e6e35022-84e1-414b-9685-8184ff807fa3
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (a513bd26-146a-4555-be22-10732257572e)
 Call ID: a513bd26-146a-4555-be22-10732257572e
  Args:
    type: :Person
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AddLiteral (1ed2c7b6-c7ff-4e8a-b3c9-d5e63796edd0)
 Call ID: 1ed2c7b6-c7ff-4e8a-b3c9-d5e63796edd0
  Args:
    relation: :hasBirthYear
    literal_value: 1897
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (16c248b0-3b77-4cc8-9d05-08939e7f61a9)
 Call ID: 16c248b0-3b77-4cc8-9d05-08939e7f61a9
  Args:
    relation: :hasDeathYear
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1975
    literal_type: xsd:integer
  AssignClass (5752f010-6216-4eb9-b2c7-d88904683782)
 Call ID: 5752f010-6216-4eb9-b2c7-d88904683782
  Args:
    source: Prince_Alfonso_Count_of_Caserta
    type: :Man
  AssignClass (5ec67ba9-5547-4a92-ba1a-106c62c23d96)
 Call ID: 5ec67ba9-5547-4a92-ba1a-106c62c23d96
  Args:
    type: :Person
    source: Prince_Alfonso_Count_of_Caserta
  AssignClass (ac1dc5bd-4c98-4298-b46e-c1ba80edc9e3)
 Call ID: ac1dc5bd-4c98-4298-b46e-c1ba80edc9e3
  Args:
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (4c966dde-1db8-43d8-942f-78f324d06757)
 Call ID: 4c966dde-1db8-43d8-942f-78f324d06757
  Args:
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (12d6c129-e5b7-469d-a90b-4d0d646adeb4)
 Call ID: 12d6c129-e5b7-469d-a90b-4d0d646adeb4
  Args:
    relation: :hasFather
    target: Prince_Alfonso_Count_of_Caserta
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AddTriple (3e3621e3-080a-4139-b5b2-bf7598dd4d9a)
 Call ID: 3e3621e3-080a-4139-b5b2-bf7598dd4d9a
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (79135acb-cb20-4ac3-997f-b67fc8e1c861)
 Call ID: 79135acb-cb20-4ac3-997f-b67fc8e1c861
  Args:
    source: Princess_Malgorzata_Izabella_Czartoryska
    type: :Woman
  AssignClass (0fa4d375-4e1e-4d24-8abb-47553ee93467)
 Call ID: 0fa4d375-4e1e-4d24-8abb-47553ee93467
  Args:
    source: Princess_Malgorzata_Izabella_Czartoryska
    type: :Person
  AssignClass (c7464631-2d21-45d7-b6a6-cd3d2ee86d8f)
 Call ID: c7464631-2d21-45d7-b6a6-cd3d2ee86d8f
  Args:
    type: :Man
    source: Prince_Adam_Ludwik_Czartoryski
  AssignClass (2fff2ed9-5687-408f-b4b4-2cf98bb58c57)
 Call ID: 2fff2ed9-5687-408f-b4b4-2cf98bb58c57
  Args:
    source: Prince_Adam_Ludwik_Czartoryski
    type: :Person
  AssignClass (05fc6520-91bf-49b1-afd3-b1bdfdae7d64)
 Call ID: 05fc6520-91bf-49b1-afd3-b1bdfdae7d64
  Args:
    source: Countess_Maria_Ludwika_Krasinska
    type: :Woman
  AssignClass (9e5eaa7a-6d7b-49e4-92ba-15ef09ba7c3a)
 Call ID: 9e5eaa7a-6d7b-49e4-92ba-15ef09ba7c3a
  Args:
    type: :Person
    source: Countess_Maria_Ludwika_Krasinska
  AddTriple (98912396-d7b8-45a4-b749-9879bd21f7f2)
 Call ID: 98912396-d7b8-45a4-b749-9879bd21f7f2
  Args:
    relation: :hasFather
    target: Prince_Adam_Ludwik_Czartoryski
    source: Princess_Malgorzata_Izabella_Czartoryska
  AddTriple (1746bde9-fa86-476b-866f-ee95750d4df5)
 Call ID: 1746bde9-fa86-476b-866f-ee95750d4df5
  Args:
    source: Princess_Malgorzata_Izabella_Czartoryska
    target: Countess_Maria_Ludwika_Krasinska
    relation: :hasMother
  AddLiteral (86f92ba4-03e4-48fe-b2f4-5b7454051cbd)
 Call ID: 86f92ba4-03e4-48fe-b2f4-5b7454051cbd
  Args:
    literal_type: xsd:integer
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1927
    relation: :hasMarriageYear
  AddTriple (eedcbba0-1ee8-47da-8014-ee560df5995f)
 Call ID: eedcbba0-1ee8-47da-8014-ee560df5995f
  Args:
    target: Princess_Malgorzata_Izabella_Czartoryska
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (797b2bcc-bd7b-429c-9f1d-f04b21975d55)
 Call ID: 797b2bcc-bd7b-429c-9f1d-f04b21975d55
  Args:
    literal_type: xsd:integer
    literal_value: 1929
    source: Princess_Malgorzata_Izabella_Czartoryska
    relation: :hasDeathYear
  AssignClass (3ecf4efb-1630-4b7a-b2b3-ea3182fa1d34)
 Call ID: 3ecf4efb-1630-4b7a-b2b3-ea3182fa1d34
  Args:
    source: Princess_Cecylia_Lubomirska
    type: :Woman
  AssignClass (2c61f17f-1beb-4340-9af2-ac5ec2a51bef)
 Call ID: 2c61f17f-1beb-4340-9af2-ac5ec2a51bef
  Args:
    type: :Person
    source: Princess_Cecylia_Lubomirska
  AssignClass (c6d40f65-cb73-4165-baa6-82826ff66b9a)
 Call ID: c6d40f65-cb73-4165-baa6-82826ff66b9a
  Args:
    type: :Man
    source: Prince_Kasimierz_Lubomirski
  AssignClass (40edf764-0900-4d18-af78-4c9d4878149a)
 Call ID: 40edf764-0900-4d18-af78-4c9d4878149a
  Args:
    type: :Person
    source: Prince_Kasimierz_Lubomirski
  AssignClass (2d51e7c9-ed92-4af3-8053-51ea900e33b6)
 Call ID: 2d51e7c9-ed92-4af3-8053-51ea900e33b6
  Args:
    type: :Woman
    source: Countess_Maria_Theresia_Granow-Wodicka
  AssignClass (fdb5209a-5b15-4053-9521-e230ddbf62cb)
 Call ID: fdb5209a-5b15-4053-9521-e230ddbf62cb
  Args:
    source: Countess_Maria_Theresia_Granow-Wodicka
    type: :Person
  AddTriple (05395020-14fa-495d-b855-2a944c092a72)
 Call ID: 05395020-14fa-495d-b855-2a944c092a72
  Args:
    relation: :hasFather
    target: Prince_Kasimierz_Lubomirski
    source: Princess_Cecylia_Lubomirska
  AddTriple (a355338c-9387-4e46-abd4-d12531759359)
 Call ID: a355338c-9387-4e46-abd4-d12531759359
  Args:
    relation: :hasMother
    source: Princess_Cecylia_Lubomirska
    target: Countess_Maria_Theresia_Granow-Wodicka
  AddLiteral (9831e227-f9f8-46e0-a17d-b665b0bf9819)
 Call ID: 9831e227-f9f8-46e0-a17d-b665b0bf9819
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1932
  AddTriple (22af39e9-26f4-4104-95a5-ebe77f97109d)
 Call ID: 22af39e9-26f4-4104-95a5-ebe77f97109d
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: Princess_Cecylia_Lubomirska
    relation: :hasRelation
  Finish (d8924afe-dd9e-4986-8873-5a41a8793412)
 Call ID: d8924afe-dd9e-4986-8873-5a41a8793412
  Args: