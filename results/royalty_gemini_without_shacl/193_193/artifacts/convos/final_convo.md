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
David Chavchavadze (May 20, 1924 – October 5, 2014) was a British-born American author and a former Central Intelligence Agency (CIA) officer of Georgian-Russian origin.
Life and death

Chavchavadze was born in London to Prince Paul Chavchavadze (1899–1971) and Princess Nina Georgievna of Russia (Romanov) (1901–1974), a descendant of a prominent Georgian noble family and the Imperial Russian dynasty.
His father, Prince Paul, was a fiction writer and translator of writings from Georgian into English, and an émigré in the United Kingdom, and then the United States.
Chavchavadze entered the United States Army in 1943 and served during World War II as liaison for the U.S. Army Air Force Lend-Lease supply operations to the Soviet Union.
After his retirement, Chavchavadze specialized in tracing the nobility of Imperial Russia and authored The Grand Dukes (1989).
Via his mother, Chavchavadze is great-great-grandson (through Grand Duke Mikhail Nicholaevich) and simultaneously great-great-great-grandson (through Queen of Greece, Olga Constantinovna) of Nicholas I.
David Chavchavadze died in his sleep on October 5, 2014, aged 90, after a long illness.
They have one step-son, Paul George Olkhovsky (August 11, 1960).



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
  AssignClass (38c4d3a3-774c-49ef-84a0-d9e099607143)
 Call ID: 38c4d3a3-774c-49ef-84a0-d9e099607143
  Args:
    type: :Man
    source: David_Chavchavadze
  AssignClass (fffb16e5-2f7f-4099-96be-299f0614ebf3)
 Call ID: fffb16e5-2f7f-4099-96be-299f0614ebf3
  Args:
    source: David_Chavchavadze
    type: :Person
  AddLiteral (e899fee1-f6e5-4907-949c-4de8d63c30f7)
 Call ID: e899fee1-f6e5-4907-949c-4de8d63c30f7
  Args:
    relation: :hasBirthYear
    source: David_Chavchavadze
    literal_value: 1924
    literal_type: xsd:integer
  AddLiteral (c9f0546a-ed50-42b9-8314-03481acb1e19)
 Call ID: c9f0546a-ed50-42b9-8314-03481acb1e19
  Args:
    relation: :hasDeathYear
    literal_value: 2014
    source: David_Chavchavadze
    literal_type: xsd:integer
  AssignClass (624eabb3-8611-4e22-89e9-8dc1f80a6a01)
 Call ID: 624eabb3-8611-4e22-89e9-8dc1f80a6a01
  Args:
    type: :Man
    source: Prince_Paul_Chavchavadze
  AssignClass (f6b8cb8f-6d2a-4f53-9c9c-796a0efb838c)
 Call ID: f6b8cb8f-6d2a-4f53-9c9c-796a0efb838c
  Args:
    type: :Person
    source: Prince_Paul_Chavchavadze
  AddLiteral (71f7ed13-c7ea-4b6d-8c69-df7659d65f3c)
 Call ID: 71f7ed13-c7ea-4b6d-8c69-df7659d65f3c
  Args:
    literal_type: xsd:integer
    source: Prince_Paul_Chavchavadze
    literal_value: 1899
    relation: :hasBirthYear
  AddLiteral (0a3335a7-c005-414d-aa5a-f7daef1784eb)
 Call ID: 0a3335a7-c005-414d-aa5a-f7daef1784eb
  Args:
    relation: :hasDeathYear
    literal_value: 1971
    source: Prince_Paul_Chavchavadze
    literal_type: xsd:integer
  AssignClass (9c4a6da7-ee31-416a-8086-501831fc543e)
 Call ID: 9c4a6da7-ee31-416a-8086-501831fc543e
  Args:
    source: Princess_Nina_Georgievna_of_Russia
    type: :Woman
  AssignClass (e1b1c5a8-9e6b-4224-a582-2eb9f6b100e4)
 Call ID: e1b1c5a8-9e6b-4224-a582-2eb9f6b100e4
  Args:
    type: :Person
    source: Princess_Nina_Georgievna_of_Russia
  AddLiteral (239becf5-df78-4bbe-8f7f-7e53b39f8088)
 Call ID: 239becf5-df78-4bbe-8f7f-7e53b39f8088
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1901
    source: Princess_Nina_Georgievna_of_Russia
  AddLiteral (a15232a0-aaa5-4219-a9f2-1c487bce3226)
 Call ID: a15232a0-aaa5-4219-a9f2-1c487bce3226
  Args:
    relation: :hasDeathYear
    source: Princess_Nina_Georgievna_of_Russia
    literal_value: 1974
    literal_type: xsd:integer
  AddTriple (bf08d0c2-3155-4747-97c0-ff71270a881a)
 Call ID: bf08d0c2-3155-4747-97c0-ff71270a881a
  Args:
    target: Prince_Paul_Chavchavadze
    relation: :hasFather
    source: David_Chavchavadze
  AddTriple (696e33a2-8a35-4dbe-86d7-beed3f849763)
 Call ID: 696e33a2-8a35-4dbe-86d7-beed3f849763
  Args:
    target: Princess_Nina_Georgievna_of_Russia
    source: David_Chavchavadze
    relation: :hasMother
  AssignClass (7c90e37f-e755-46b2-87cc-b23ce6d08af1)
 Call ID: 7c90e37f-e755-46b2-87cc-b23ce6d08af1
  Args:
    type: :Man
    source: Paul_George_Olkhovsky
  AssignClass (83e21de7-cc80-4fab-a00d-bd892b36f2a0)
 Call ID: 83e21de7-cc80-4fab-a00d-bd892b36f2a0
  Args:
    type: :Person
    source: Paul_George_Olkhovsky
  AddLiteral (6b7a626b-a31a-4e99-a8f9-2370735aa792)
 Call ID: 6b7a626b-a31a-4e99-a8f9-2370735aa792
  Args:
    relation: :hasBirthYear
    literal_value: 1960
    source: Paul_George_Olkhovsky
    literal_type: xsd:integer
  Finish (a082766d-b2db-4271-b75f-2a059f062907)
 Call ID: a082766d-b2db-4271-b75f-2a059f062907
  Args: