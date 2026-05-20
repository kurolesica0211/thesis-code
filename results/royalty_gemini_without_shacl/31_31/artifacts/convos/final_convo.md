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
Christoph of Schleswig-Holstein (22 August 1949 – 27 September 2023)
(German: Christoph Prinz zu Schleswig-Holstein) was the head of the House of Schleswig-Holstein-Sonderburg-Glücksburg (commonly known as the House of Glücksburg) and, by agnatic primogeniture, of the entire House of Oldenburg between 1980 and 2023.
Traditionally he would have been the eighth Duke of Schleswig-Holstein and Duke of Glücksburg, styled as His Highness.
House of Schleswig-Holstein-Sonderburg-Glücksburg

The House of Oldenburg — in one of its cadet branches — is patrilineally the royal house of Norway (1450–1818 and since 1905) and the United Kingdom (since 2022), and has been the reigning dynasty of several other countries including Denmark, Greece, Sweden and Russia.
As such, Christoph was the agnatic head of the family that today includes Harald V of Norway and, patrilineally, Charles III of the United Kingdom.
His great-great-grandfather, Friedrich, Duke of Schleswig-Holstein-Sonderburg-Glücksburg, was the older brother of Christian IX of Denmark, and through him Christoph is heir by male primogeniture to the Danish title Duke of Glücksburg (heir of the last extant ducal branch of the House of Schleswig-Holstein-Sonderburg) conferred by the Danish crown in 1825.
Christoph was also, cognatically, a descendant of Queen Victoria and Alexander II of Russia.
Life and activities

Christoph was born in Louisenlund Castle in Güby, near Eckernförde, Schleswig-Holstein, West Germany, the eldest son of Peter, Duke of Schleswig-Holstein (1922–1980), and his wife, Princess Marie Alix of Schaumburg-Lippe (1923-2021).
Christoph served as a Reservist in the German Army for two years, holding the rank of lieutenant.
Christoph succeeded to the headship of the ducal house on 30 September 1980 following the death of his father.
While possession of the united duchies of Schleswig and Holstein had been allocated by a series of wars and treaties since the First Schleswig War of 1848 and the London Protocol of 1852, the ducal title was borne by Christoph's father and paternal grandfather (as inherited from his great-grandfather, Friedrich Ferdinand, Duke of Schleswig-Holstein-Sonderburg-Glücksburg in 1934).
However, Christoph was known also by the title which is shared by male cadets of the dynasty, "Prinz zu (Prince of) Schleswig-Holstein-Sonderburg-Glücksburg".
From 1980 onward, Christoph chaired the board of the family foundation that owns the ancestral castle, Glücksburg Castle.
He was the owner of the Grünholz and Bienebek estates and was one of the largest landowners of Schleswig-Holstein.
Marriage and issue

Christoph married Princess Elisabeth of Lippe-Weissenfeld (b. 28 July 1957 in Munich), the youngest child of Prince Alfred Karl Friedrich Georg Franz of Lippe-Weissenfeld (1922-2024), who served as UNHCR representative for Italy, and his wife, Baroness Irmgard Julinka Wagner von Wehrborn (b. 1928).
They had four children: 


Death

Christoph died on 27 September 2023, at the age of 74, after a long-term illness.



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
  AssignClass (ef8d7861-418b-4dc2-9707-dbfd31939681)
 Call ID: ef8d7861-418b-4dc2-9707-dbfd31939681
  Args:
    source: Christoph_of_Schleswig-Holstein
    type: :Man
  AssignClass (3c3f4ec2-d897-4d9e-8921-bc802d34b6fc)
 Call ID: 3c3f4ec2-d897-4d9e-8921-bc802d34b6fc
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    type: :Man
  AssignClass (752f4b6b-bffe-4b01-9ad2-9b59950ea597)
 Call ID: 752f4b6b-bffe-4b01-9ad2-9b59950ea597
  Args:
    type: :Woman
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AssignClass (0b5707c4-e023-425e-bfb9-06aa3e743c53)
 Call ID: 0b5707c4-e023-425e-bfb9-06aa3e743c53
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    type: :Woman
  AssignClass (ed4c4c75-616a-4de9-a6d9-07763f23adee)
 Call ID: ed4c4c75-616a-4de9-a6d9-07763f23adee
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    type: :Man
  AssignClass (9f4dfc4c-eaaf-42bb-8f14-c28b9a8991d0)
 Call ID: 9f4dfc4c-eaaf-42bb-8f14-c28b9a8991d0
  Args:
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    type: :Woman
  AddLiteral (ee0232c0-a748-4b15-be97-0d8d4a67053b)
 Call ID: ee0232c0-a748-4b15-be97-0d8d4a67053b
  Args:
    relation: :hasBirthYear
    literal_value: 1949
    literal_type: xsd:integer
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (3025ec21-ae48-4212-8014-1692a7dfe3dc)
 Call ID: 3025ec21-ae48-4212-8014-1692a7dfe3dc
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2023
    source: Christoph_of_Schleswig-Holstein
  AddLiteral (abfb6bff-e2e3-4291-a8ce-82a901d4bbc3)
 Call ID: abfb6bff-e2e3-4291-a8ce-82a901d4bbc3
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1922
    source: Peter_Duke_of_Schleswig-Holstein
  AddLiteral (1da08578-37c5-48c0-8c42-480864fbf9d7)
 Call ID: 1da08578-37c5-48c0-8c42-480864fbf9d7
  Args:
    source: Peter_Duke_of_Schleswig-Holstein
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1980
  AddLiteral (0d4541ed-16b8-4ff6-9e12-8a8e6434c0a9)
 Call ID: 0d4541ed-16b8-4ff6-9e12-8a8e6434c0a9
  Args:
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1923
  AddLiteral (3bfbbd96-366b-46cd-a842-867586d84b4d)
 Call ID: 3bfbbd96-366b-46cd-a842-867586d84b4d
  Args:
    relation: :hasDeathYear
    literal_value: 2021
    literal_type: xsd:integer
    source: Princess_Marie_Alix_of_Schaumburg-Lippe
  AddLiteral (7a2d2593-fb83-489b-ad77-adf5bbc947de)
 Call ID: 7a2d2593-fb83-489b-ad77-adf5bbc947de
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasBirthYear
    literal_value: 1957
    literal_type: xsd:integer
  AddLiteral (2e856db2-52f6-45a4-8612-c0d696df1cbc)
 Call ID: 2e856db2-52f6-45a4-8612-c0d696df1cbc
  Args:
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    relation: :hasBirthYear
    literal_value: 1922
    literal_type: xsd:integer
  AddLiteral (4b0229d0-c891-4100-b89c-64463509a8be)
 Call ID: 4b0229d0-c891-4100-b89c-64463509a8be
  Args:
    literal_value: 2024
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
  AddLiteral (81b471ff-bf9a-4074-a3e7-1ef8977fecbe)
 Call ID: 81b471ff-bf9a-4074-a3e7-1ef8977fecbe
  Args:
    source: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
    literal_value: 1928
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (1287f4d3-0f87-48e5-8334-e6420e25914c)
 Call ID: 1287f4d3-0f87-48e5-8334-e6420e25914c
  Args:
    relation: :hasFather
    target: Peter_Duke_of_Schleswig-Holstein
    source: Christoph_of_Schleswig-Holstein
  AddTriple (4da8c4aa-5312-4ac6-a0ff-d3a108ef864c)
 Call ID: 4da8c4aa-5312-4ac6-a0ff-d3a108ef864c
  Args:
    source: Christoph_of_Schleswig-Holstein
    target: Princess_Marie_Alix_of_Schaumburg-Lippe
    relation: :hasMother
  AddTriple (07b15a26-0046-46a6-abda-de6effefac0e)
 Call ID: 07b15a26-0046-46a6-abda-de6effefac0e
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    target: Prince_Alfred_Karl_Friedrich_Georg_Franz_of_Lippe-Weissenfeld
    relation: :hasFather
  AddTriple (a75aab77-4d98-4b7c-9adf-8e7d185940e2)
 Call ID: a75aab77-4d98-4b7c-9adf-8e7d185940e2
  Args:
    source: Princess_Elisabeth_of_Lippe-Weissenfeld
    relation: :hasMother
    target: Baroness_Irmgard_Julinka_Wagner_von_Wehrborn
  Finish (b76aeca5-866c-49c6-946c-fff3cf129b9c)
 Call ID: b76aeca5-866c-49c6-946c-fff3cf129b9c
  Args: