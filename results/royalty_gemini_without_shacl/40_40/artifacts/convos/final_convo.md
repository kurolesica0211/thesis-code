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
Infante Gonzalo of Spain (Gonzalo Manuel Maria Bernardo Narciso Alfonso Mauricio de Borbón y Battenberg; 24 October 1914 – 13 August 1934) was the fourth surviving son and youngest child of King Alfonso XIII of Spain and his wife Princess Victoria Eugenie of Battenberg.
He was the youngest grandson of Princess Beatrice of the United Kingdom.
Life

Gonzalo was born in Madrid.
He was baptized with the names Gonzalo Manuel María Bernardo Narciso Alfonso Mauricio.
He received his final name in honor of his uncle, Prince Maurice of Battenberg, who was killed in World War I shortly before Gonzalo's baptism.
The infante was educated privately.
Because he inherited the genetic disorder hemophilia from his mother's family (a fact not widely known in Spain during his life), he had some ill health, although he was an active sportsman.
In May 1924, nine-year-old Gonzalo inaugurated the Estadio Chamartín, the new football stadium for Real Madrid, kicking the ball of honour and yelling "¡Hala Madrid!.
"


On 14 April 1931, Gonzalo accompanied his mother into exile.
In August 1934, Gonzalo was spending the summer holidays with his family at the villa of Count Ladislaus de Hoyos at Pörtschach am Wörthersee in Austria.
On the evening of 11 August, Gonzalo and his sister Infanta Beatriz were driving from Klagenfurt to Pörtschach.
Neither Gonzalo nor Beatriz appeared badly hurt, and so they returned to their villa.
Several hours later it became clear that Gonzalo had severe abdominal bleeding.
His eldest brother, Alfonso, would die just over four years later from very similar circumstances—having also inherited hemophilia, he was involved in a crash after the automobile he was in swerved to avoid a truck.
Gonzalo was buried in the graveyard at Pörtschach.



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
  AssignClass (0b177a5c-10eb-45d9-8759-77efad60303c)
 Call ID: 0b177a5c-10eb-45d9-8759-77efad60303c
  Args:
    type: :Man
    source: :Gonzalo_of_Spain
  AssignClass (0e8ccb6b-b650-4b9f-b387-389e0f1bba48)
 Call ID: 0e8ccb6b-b650-4b9f-b387-389e0f1bba48
  Args:
    type: :Person
    source: :Gonzalo_of_Spain
  AssignClass (8bf8e3d9-69ce-495f-a54a-5612c5f37dc3)
 Call ID: 8bf8e3d9-69ce-495f-a54a-5612c5f37dc3
  Args:
    type: :Man
    source: :Alfonso_XIII_of_Spain
  AssignClass (ff84ea2f-ea30-40ba-9765-ed3be38183f9)
 Call ID: ff84ea2f-ea30-40ba-9765-ed3be38183f9
  Args:
    source: :Alfonso_XIII_of_Spain
    type: :Ancestor
  AssignClass (fbca159e-8786-4eb2-819d-e018c1a1b0ac)
 Call ID: fbca159e-8786-4eb2-819d-e018c1a1b0ac
  Args:
    source: :Alfonso_XIII_of_Spain
    type: :Person
  AssignClass (ec60500c-b3fb-4091-be06-3641b84e74dd)
 Call ID: ec60500c-b3fb-4091-be06-3641b84e74dd
  Args:
    source: :Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (94cd9627-4cf7-446b-9fb5-8deefb10403b)
 Call ID: 94cd9627-4cf7-446b-9fb5-8deefb10403b
  Args:
    source: :Victoria_Eugenie_of_Battenberg
    type: :Ancestor
  AssignClass (479fec94-b615-447f-9b2d-cb083bd8b27e)
 Call ID: 479fec94-b615-447f-9b2d-cb083bd8b27e
  Args:
    type: :Person
    source: :Victoria_Eugenie_of_Battenberg
  AssignClass (ce2859d5-c981-415d-9cd8-f4b5bf12f283)
 Call ID: ce2859d5-c981-415d-9cd8-f4b5bf12f283
  Args:
    source: :Beatrice_of_the_United_Kingdom
    type: :Woman
  AssignClass (2ff8af81-3172-460f-be5e-33a094427b3b)
 Call ID: 2ff8af81-3172-460f-be5e-33a094427b3b
  Args:
    source: :Beatrice_of_the_United_Kingdom
    type: :Ancestor
  AssignClass (1c44fc5f-fd42-4fdc-a2cc-7ba63af72c21)
 Call ID: 1c44fc5f-fd42-4fdc-a2cc-7ba63af72c21
  Args:
    type: :Person
    source: :Beatrice_of_the_United_Kingdom
  AssignClass (1f23692d-66f0-40cd-8ab6-8e0bb0eaa850)
 Call ID: 1f23692d-66f0-40cd-8ab6-8e0bb0eaa850
  Args:
    type: :Man
    source: :Maurice_of_Battenberg
  AssignClass (0e77a26d-5b34-44c6-acd7-88f9da4466c7)
 Call ID: 0e77a26d-5b34-44c6-acd7-88f9da4466c7
  Args:
    type: :Person
    source: :Maurice_of_Battenberg
  AssignClass (4c01f326-ee8e-4886-a221-d8896b665ccb)
 Call ID: 4c01f326-ee8e-4886-a221-d8896b665ccb
  Args:
    source: :Beatriz_of_Spain
    type: :Woman
  AssignClass (0bba2328-11f4-45f1-aeb9-51c546101e77)
 Call ID: 0bba2328-11f4-45f1-aeb9-51c546101e77
  Args:
    type: :Person
    source: :Beatriz_of_Spain
  AssignClass (5881275b-d2b1-4f32-be51-023ba296206c)
 Call ID: 5881275b-d2b1-4f32-be51-023ba296206c
  Args:
    type: :Man
    source: :Alfonso_of_Spain
  AssignClass (3a8d128a-9105-450a-b493-ec7507f5f123)
 Call ID: 3a8d128a-9105-450a-b493-ec7507f5f123
  Args:
    source: :Alfonso_of_Spain
    type: :Person
  AddLiteral (02e56eae-d897-40cc-bef5-2a0f5fe3b1f6)
 Call ID: 02e56eae-d897-40cc-bef5-2a0f5fe3b1f6
  Args:
    literal_type: xsd:string
    literal_value: Gonzalo Manuel Maria Bernardo Narciso Alfonso Mauricio de Borbón y Battenberg
    relation: :knownAs
    source: :Gonzalo_of_Spain
  AddLiteral (b2ba147a-097c-408d-b201-7f72615d16ba)
 Call ID: b2ba147a-097c-408d-b201-7f72615d16ba
  Args:
    literal_type: xsd:integer
    source: :Gonzalo_of_Spain
    relation: :hasBirthYear
    literal_value: 1914
  AddLiteral (88a4f6a6-ca23-47e9-a816-bb8ccf59ca26)
 Call ID: 88a4f6a6-ca23-47e9-a816-bb8ccf59ca26
  Args:
    relation: :hasDeathYear
    source: :Gonzalo_of_Spain
    literal_value: 1934
    literal_type: xsd:integer
  AddTriple (946970de-1fe0-4d84-a6c8-b7b9c49bebfe)
 Call ID: 946970de-1fe0-4d84-a6c8-b7b9c49bebfe
  Args:
    target: :Alfonso_XIII_of_Spain
    relation: :hasFather
    source: :Gonzalo_of_Spain
  AddTriple (e1dbae78-d0ce-4b23-8a1f-73189922b242)
 Call ID: e1dbae78-d0ce-4b23-8a1f-73189922b242
  Args:
    target: :Victoria_Eugenie_of_Battenberg
    source: :Gonzalo_of_Spain
    relation: :hasMother
  AddTriple (afe807f9-3374-420a-860a-2da7103071b0)
 Call ID: afe807f9-3374-420a-860a-2da7103071b0
  Args:
    target: :Beatrice_of_the_United_Kingdom
    source: :Gonzalo_of_Spain
    relation: :hasAncestor
  AddTriple (0910874e-049b-42c8-bb69-14ae57c7245d)
 Call ID: 0910874e-049b-42c8-bb69-14ae57c7245d
  Args:
    target: :Gonzalo_of_Spain
    source: :Beatriz_of_Spain
    relation: :isSisterOf
  AddTriple (6c186b92-d28b-4536-bf80-159d92ceca98)
 Call ID: 6c186b92-d28b-4536-bf80-159d92ceca98
  Args:
    target: :Alfonso_of_Spain
    source: :Gonzalo_of_Spain
    relation: :hasBrother
  Finish (a8b2c0c4-8b96-473a-910b-e214d7983d0e)
 Call ID: a8b2c0c4-8b96-473a-910b-e214d7983d0e
  Args: