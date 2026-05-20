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
Prince Archie of Sussex (Archie Harrison Mountbatten-Windsor; born 6 May 2019) is a member of the British royal family.
He is the son of Prince Harry, Duke of Sussex, and Meghan, Duchess of Sussex.
A grandson of King Charles III, he is sixth in the line of succession to the British throne.
Birth, family and infancy

Archie Harrison Mountbatten-Windsor was born at 05:26 (BST) (04:26 UTC) on 6 May 2019 at Portland Hospital in London.
He is the first child of Prince Harry, Duke of Sussex and Meghan, Duchess of Sussex.
Archie has mixed-race ancestry, with African-American and European-American maternal lineage, and holds dual citizenship of the United Kingdom and the United States.
Archie's parents brought him to meet his great-grandparents Queen Elizabeth II and Prince Philip for the first time when he was two days old.
Four of the godparents were later reported to be Charlie van Straubenzee, Tiggy Pettifer, Mark Dyer, and the 7th Duke of Westminster.
In early 2020, Archie's parents stepped down from their roles as working members of the royal family.
Public appearances

In September and October 2019, Archie accompanied his parents on a Southern African tour to Malawi, Angola, South Africa and Botswana.
Title and styles

As heir apparent to his father's dukedom of Sussex, earldom of Dumbarton, and barony of Kilkeel, Archie was at birth and by custom entitled to use Prince Harry's senior subsidiary title, Earl of Dumbarton, as a courtesy.
However, the media reported that the Duke and Duchess decided, instead, that Archie would be styled as Master Archie Harrison Mountbatten-Windsor, in accordance with their reported wish that he grow up as a private citizen.
Upon the accession of Charles III, Archie became entitled to use the title prince and style Royal Highness, as the child of a son of the monarch, pursuant to letters patent issued by King George V in 1917.
However, sources reported that it was unclear whether he would use that title and style, noting that not all members of the royal family who are eligible for a title choose to use one.
In the interview Oprah with Meghan and Harry, the Duchess of Sussex said that she had been told that changes would be made to remove that entitlement; Charles III's plans for a scaled-down royal family dated back to the 1990s.
The official website of the royal family was updated to refer to him as "Prince Archie of Sussex" on 9 March 2023.



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
  AssignClass (10d28f52-32e3-4d7c-b28d-0807afb058c9)
 Call ID: 10d28f52-32e3-4d7c-b28d-0807afb058c9
  Args:
    type: :Person
    source: Archie Harrison Mountbatten-Windsor
  AssignClass (a73e55c3-3da1-4e3d-963a-b9f5562c37e8)
 Call ID: a73e55c3-3da1-4e3d-963a-b9f5562c37e8
  Args:
    type: :Person
    source: Prince Harry, Duke of Sussex
  AssignClass (650df09e-b661-48f1-a1d6-37ce33b7e964)
 Call ID: 650df09e-b661-48f1-a1d6-37ce33b7e964
  Args:
    type: :Person
    source: Meghan, Duchess of Sussex
  AssignClass (58ef55bf-702b-484e-a373-b2fa945eccbd)
 Call ID: 58ef55bf-702b-484e-a373-b2fa945eccbd
  Args:
    type: :Person
    source: King Charles III
  AssignClass (8950f62a-46fb-43df-96dc-4e8d76e8cf6c)
 Call ID: 8950f62a-46fb-43df-96dc-4e8d76e8cf6c
  Args:
    type: :Person
    source: Queen Elizabeth II
  AssignClass (616f60a3-ae89-43de-8d0e-4d9262322ee6)
 Call ID: 616f60a3-ae89-43de-8d0e-4d9262322ee6
  Args:
    type: :Person
    source: Prince Philip
  AssignClass (fb1619ee-a54a-4b9b-b6c2-e2a13235ae66)
 Call ID: fb1619ee-a54a-4b9b-b6c2-e2a13235ae66
  Args:
    type: :Male
    source: Archie Harrison Mountbatten-Windsor
  AssignClass (ca3f0cd3-36a1-4c87-ab35-4037789d40eb)
 Call ID: ca3f0cd3-36a1-4c87-ab35-4037789d40eb
  Args:
    type: :Male
    source: Prince Harry, Duke of Sussex
  AssignClass (f73fc8e7-2b5f-4e21-940f-22dc3aa8209e)
 Call ID: f73fc8e7-2b5f-4e21-940f-22dc3aa8209e
  Args:
    type: :Male
    source: King Charles III
  AssignClass (bf6dfffd-d2c5-4f2f-91f2-604e4c9a5a99)
 Call ID: bf6dfffd-d2c5-4f2f-91f2-604e4c9a5a99
  Args:
    type: :Male
    source: Prince Philip
  AssignClass (352f7638-1a1b-4129-817d-f48a67cba8a0)
 Call ID: 352f7638-1a1b-4129-817d-f48a67cba8a0
  Args:
    type: :Woman
    source: Meghan, Duchess of Sussex
  AssignClass (c095be0f-9383-4cab-b7f5-cc614bb6aa7f)
 Call ID: c095be0f-9383-4cab-b7f5-cc614bb6aa7f
  Args:
    type: :Woman
    source: Queen Elizabeth II
  AddTriple (91dd341c-f342-4ea2-873a-8d6b3d2e0239)
 Call ID: 91dd341c-f342-4ea2-873a-8d6b3d2e0239
  Args:
    relation: :hasFather
    target: Prince Harry, Duke of Sussex
    source: Archie Harrison Mountbatten-Windsor
  AddTriple (dd42aad8-531b-4903-a011-41ff9f14d560)
 Call ID: dd42aad8-531b-4903-a011-41ff9f14d560
  Args:
    target: Meghan, Duchess of Sussex
    source: Archie Harrison Mountbatten-Windsor
    relation: :hasMother
  AddTriple (b7507531-6691-485c-a8c9-29c87f70ae7f)
 Call ID: b7507531-6691-485c-a8c9-29c87f70ae7f
  Args:
    target: King Charles III
    source: Prince Harry, Duke of Sussex
    relation: :hasFather
  AddLiteral (554fd776-98b5-48a0-8074-227913e7833b)
 Call ID: 554fd776-98b5-48a0-8074-227913e7833b
  Args:
    source: Archie Harrison Mountbatten-Windsor
    literal_value: 2019
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (adfa6921-596d-4f29-9700-40385cd7254c)
 Call ID: adfa6921-596d-4f29-9700-40385cd7254c
  Args:
    literal_value: Prince Archie of Sussex
    source: Archie Harrison Mountbatten-Windsor
    literal_type: xsd:string
    relation: :knownAs
  Finish (aa8924ff-70b4-4495-8c33-854cdd499298)
 Call ID: aa8924ff-70b4-4495-8c33-854cdd499298
  Args: