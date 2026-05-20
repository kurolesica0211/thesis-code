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
Angelica Margherita Edwina Hicks (born 16 September 1992) is a British fashion illustrator and internet personality.
Early life and family

Hicks was born on 16 September 1992 to Marina Allegra Federica Silvia Tondato, an Italian designer, and Ashley Louis David Hicks, a British artist and interior designer.
Hicks' paternal grandparents were the English interior decorator and designer David Nightingale Hicks and Lady Pamela Mountbatten, who served as a bridesmaid and as a lady-in-waiting to Elizabeth II.
Through her grandmother, Hicks is a relative of the Mountbatten family, itself a branch of the German princely Battenberg family, and a relative of the British royal family.
Hicks' great-grandparents, Louis Mountbatten, 1st Earl Mountbatten of Burma and The Honourable Edwina Ashley, served as the Viceroy and Vicereine of India.
Hicks grew up in Chelsea, London and was educated at a boarding school.
Career

Hicks works as a visual artist and fashion illustrator.
Hicks also made commissioned pieces for the American fashion designer Tory Burch and illustrated for the magazines Elle and Porter.
In 2021, Hicks launched a TikTok channel where she parodies haute couture outfits from red carpet events and fashion shows, recreating them out of duct tape, trash bags, metallic wrappers, foil, candy, and other materials.
By July 2022, Hicks amassed over 48,000 followers and her videos collectively received over 4 million likes.
Her videos led to Hicks collaborating with Valentino and Vogue Italia.
By September 2022, Hicks had over 86,000 followers on TikTok.
Personal life

Hicks resides in Carroll Gardens in Brooklyn, New York.



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
  AssignClass (59607a7b-e1fe-43ce-94b3-f8ebe340caaf)
 Call ID: 59607a7b-e1fe-43ce-94b3-f8ebe340caaf
  Args:
    type: :Person
    source: Angelica Margherita Edwina Hicks
  AssignClass (7784cfec-ca13-42e6-b133-8c372383eb36)
 Call ID: 7784cfec-ca13-42e6-b133-8c372383eb36
  Args:
    type: :Woman
    source: Angelica Margherita Edwina Hicks
  AddLiteral (daa4a34d-c4eb-42d0-85da-6548a8921394)
 Call ID: daa4a34d-c4eb-42d0-85da-6548a8921394
  Args:
    source: Angelica Margherita Edwina Hicks
    relation: :hasBirthYear
    literal_value: 1992
    literal_type: xsd:integer
  AssignClass (1217dc48-381c-4a91-89db-fb5c71979eb0)
 Call ID: 1217dc48-381c-4a91-89db-fb5c71979eb0
  Args:
    type: :Person
    source: Marina Allegra Federica Silvia Tondato
  AssignClass (574eea29-5873-4d65-a4f2-6a27d52bc493)
 Call ID: 574eea29-5873-4d65-a4f2-6a27d52bc493
  Args:
    type: :Woman
    source: Marina Allegra Federica Silvia Tondato
  AssignClass (bcb26a61-0573-4246-9dff-ee4024d905a1)
 Call ID: bcb26a61-0573-4246-9dff-ee4024d905a1
  Args:
    type: :Person
    source: Ashley Louis David Hicks
  AssignClass (fe5a342e-ec2b-4f8c-9c65-98f7d91c7feb)
 Call ID: fe5a342e-ec2b-4f8c-9c65-98f7d91c7feb
  Args:
    type: :Man
    source: Ashley Louis David Hicks
  AddTriple (027a6ebe-dea4-498f-a90b-e8d478261d6b)
 Call ID: 027a6ebe-dea4-498f-a90b-e8d478261d6b
  Args:
    relation: :hasMother
    target: Marina Allegra Federica Silvia Tondato
    source: Angelica Margherita Edwina Hicks
  AddTriple (36d2fc7a-45ce-4ff6-af2b-346e1bac7c90)
 Call ID: 36d2fc7a-45ce-4ff6-af2b-346e1bac7c90
  Args:
    target: Ashley Louis David Hicks
    relation: :hasFather
    source: Angelica Margherita Edwina Hicks
  AssignClass (00cd0206-ddbc-40d6-9900-352b42803b88)
 Call ID: 00cd0206-ddbc-40d6-9900-352b42803b88
  Args:
    type: :Person
    source: David Nightingale Hicks
  AssignClass (79d6513c-f601-48fb-a969-49450a201aef)
 Call ID: 79d6513c-f601-48fb-a969-49450a201aef
  Args:
    type: :Man
    source: David Nightingale Hicks
  AssignClass (ad1ec912-1cf0-4c92-a2a6-5957e4ad3838)
 Call ID: ad1ec912-1cf0-4c92-a2a6-5957e4ad3838
  Args:
    type: :Person
    source: Lady Pamela Mountbatten
  AssignClass (f5a7f107-f189-42e6-9177-828e77c6ee82)
 Call ID: f5a7f107-f189-42e6-9177-828e77c6ee82
  Args:
    type: :Woman
    source: Lady Pamela Mountbatten
  AddTriple (1e4ffd12-66ba-40b0-b5ca-998ae58468c6)
 Call ID: 1e4ffd12-66ba-40b0-b5ca-998ae58468c6
  Args:
    target: David Nightingale Hicks
    relation: :hasFather
    source: Ashley Louis David Hicks
  AddTriple (b6dead31-4fa0-487f-963a-7a1c5593fa92)
 Call ID: b6dead31-4fa0-487f-963a-7a1c5593fa92
  Args:
    source: Ashley Louis David Hicks
    target: Lady Pamela Mountbatten
    relation: :hasMother
  AssignClass (2d567ae3-8209-4023-9212-7a8f6529078d)
 Call ID: 2d567ae3-8209-4023-9212-7a8f6529078d
  Args:
    type: :Person
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
  AssignClass (b65f3f8c-98ac-4a25-8323-503c8d3a3147)
 Call ID: b65f3f8c-98ac-4a25-8323-503c8d3a3147
  Args:
    type: :Man
    source: Louis Mountbatten, 1st Earl Mountbatten of Burma
  AssignClass (4eada27e-5814-4380-bc6b-b25861bad640)
 Call ID: 4eada27e-5814-4380-bc6b-b25861bad640
  Args:
    type: :Person
    source: The Honourable Edwina Ashley
  AssignClass (fde79202-204e-443e-bbaf-18e78853ed9c)
 Call ID: fde79202-204e-443e-bbaf-18e78853ed9c
  Args:
    type: :Woman
    source: The Honourable Edwina Ashley
  AddTriple (462dc71b-e46c-41f3-b452-163f67d8865e)
 Call ID: 462dc71b-e46c-41f3-b452-163f67d8865e
  Args:
    target: Louis Mountbatten, 1st Earl Mountbatten of Burma
    relation: :hasFather
    source: Lady Pamela Mountbatten
  AddTriple (8b6056b1-46d3-400f-b805-3ac01fd71e20)
 Call ID: 8b6056b1-46d3-400f-b805-3ac01fd71e20
  Args:
    target: The Honourable Edwina Ashley
    relation: :hasMother
    source: Lady Pamela Mountbatten
  Finish (e11a6e56-316f-4c0c-9a33-4e1c62b5800f)
 Call ID: e11a6e56-316f-4c0c-9a33-4e1c62b5800f
  Args: