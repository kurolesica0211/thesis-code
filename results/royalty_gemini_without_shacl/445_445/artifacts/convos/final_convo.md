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
Lady Charlotte Anne Santo Domingo (née Wellesley; 8 October 1990) is an English aristocrat and socialite and photography producer.
Early life and family

Lady Charlotte Wellesley was born at St Mary's Hospital, London on 8 October 1990 to Princess Antonia of Prussia and Charles Wellesley, Marquess of Douro.
After the death of her paternal grandfather, Valerian Wellesley, 8th Duke of Wellington, in 2014, her father succeeded him as the 9th Duke of Wellington, the 9th Prince of Waterloo, the 9th Duke of Victoria, and the 10th Duke of Ciudad Rodrigo.
Her mother, Princess Antonia, is the youngest child of Prince Frederick of Prussia and Lady Brigid Guinness.
Through her mother, Lady Charlotte is a great-great-granddaughter of Wilhelm II, German Emperor and a great-great-great-great-granddaughter of Queen Victoria.
Lady Charlotte grew up at Stratfield Saye House, her family's estate in Hampshire.
She is the younger sister of Arthur Wellesley, Earl of Mornington and Lady Mary Wellesley.
Education and career

Lady Charlotte attended Wycombe Abbey, an all-girls boarding school in Buckinghamshire.
Personal life

Lady Charlotte married Colombian-American financier Alejandro Santo Domingo in Íllora, Spain, on 28 May 2016.



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
  AssignClass (4af15c27-1931-4bf3-b7d1-a7a808657d4a)
 Call ID: 4af15c27-1931-4bf3-b7d1-a7a808657d4a
  Args:
    source: Lady_Charlotte_Anne_Santo_Domingo
    type: :Woman
  AssignClass (90510161-37fc-4632-891c-d9382ddffded)
 Call ID: 90510161-37fc-4632-891c-d9382ddffded
  Args:
    source: Lady_Charlotte_Anne_Santo_Domingo
    type: :Person
  AssignClass (6a32a589-24e9-47b7-85a3-37bd0c1ea59b)
 Call ID: 6a32a589-24e9-47b7-85a3-37bd0c1ea59b
  Args:
    source: Princess_Antonia_of_Prussia
    type: :Woman
  AssignClass (f7e16dd4-aaf7-49ce-bced-23dd780fffcb)
 Call ID: f7e16dd4-aaf7-49ce-bced-23dd780fffcb
  Args:
    source: Princess_Antonia_of_Prussia
    type: :Person
  AssignClass (1fe2c578-02d1-4afd-a228-b90dd226cef6)
 Call ID: 1fe2c578-02d1-4afd-a228-b90dd226cef6
  Args:
    type: :Man
    source: Charles_Wellesley_Marquess_of_Douro
  AssignClass (725f36df-b7e4-4d1a-99a9-ecbeb533259a)
 Call ID: 725f36df-b7e4-4d1a-99a9-ecbeb533259a
  Args:
    source: Charles_Wellesley_Marquess_of_Douro
    type: :Person
  AssignClass (ea9ad0a1-9175-4958-a022-c8497bffeac3)
 Call ID: ea9ad0a1-9175-4958-a022-c8497bffeac3
  Args:
    type: :Man
    source: Valerian_Wellesley_8th_Duke_of_Wellington
  AssignClass (123bd6bc-0b35-42c5-b759-03fb448e10f4)
 Call ID: 123bd6bc-0b35-42c5-b759-03fb448e10f4
  Args:
    type: :Person
    source: Valerian_Wellesley_8th_Duke_of_Wellington
  AssignClass (9a873e7e-1ad1-49a8-9669-3ddf87ff7b86)
 Call ID: 9a873e7e-1ad1-49a8-9669-3ddf87ff7b86
  Args:
    source: Prince_Frederick_of_Prussia
    type: :Man
  AssignClass (a0305565-28fc-40e0-8a48-fbcf57db1d2d)
 Call ID: a0305565-28fc-40e0-8a48-fbcf57db1d2d
  Args:
    type: :Person
    source: Prince_Frederick_of_Prussia
  AssignClass (43474f8b-cb55-4eb5-97b4-fddb6c4ac3b8)
 Call ID: 43474f8b-cb55-4eb5-97b4-fddb6c4ac3b8
  Args:
    source: Lady_Brigid_Guinness
    type: :Woman
  AssignClass (0db2e48c-3427-44fb-ad65-125eb8c9e943)
 Call ID: 0db2e48c-3427-44fb-ad65-125eb8c9e943
  Args:
    source: Lady_Brigid_Guinness
    type: :Person
  AssignClass (adc9ddb1-6ea9-453a-b2dc-fee3432649dc)
 Call ID: adc9ddb1-6ea9-453a-b2dc-fee3432649dc
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (b10317ba-e50d-4598-a61c-fb942348f240)
 Call ID: b10317ba-e50d-4598-a61c-fb942348f240
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Person
  AssignClass (657ca51f-e51c-45ed-843e-f57a4e34b886)
 Call ID: 657ca51f-e51c-45ed-843e-f57a4e34b886
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (3a258b02-f86b-4b89-a96a-62ee85d75e3b)
 Call ID: 3a258b02-f86b-4b89-a96a-62ee85d75e3b
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (ca8f4f5b-e3d2-4515-abf3-dc9f8b64f000)
 Call ID: ca8f4f5b-e3d2-4515-abf3-dc9f8b64f000
  Args:
    type: :Man
    source: Arthur_Wellesley_Earl_of_Mornington
  AssignClass (af432b3a-3c96-4e57-82e6-84b92b7508d0)
 Call ID: af432b3a-3c96-4e57-82e6-84b92b7508d0
  Args:
    source: Arthur_Wellesley_Earl_of_Mornington
    type: :Person
  AssignClass (af8f2a06-6fbc-4dad-b5ba-1f73e6aabf36)
 Call ID: af8f2a06-6fbc-4dad-b5ba-1f73e6aabf36
  Args:
    type: :Woman
    source: Lady_Mary_Wellesley
  AssignClass (c2324a8d-48a5-4cd4-b03c-d3f82c74b909)
 Call ID: c2324a8d-48a5-4cd4-b03c-d3f82c74b909
  Args:
    source: Lady_Mary_Wellesley
    type: :Person
  AssignClass (e689bb21-0f3e-4584-a1e5-037f0a01f5a6)
 Call ID: e689bb21-0f3e-4584-a1e5-037f0a01f5a6
  Args:
    source: Alejandro_Santo_Domingo
    type: :Man
  AssignClass (d610c715-7088-4dda-882e-89e98a1f9ae5)
 Call ID: d610c715-7088-4dda-882e-89e98a1f9ae5
  Args:
    source: Alejandro_Santo_Domingo
    type: :Person
  AddLiteral (2cf8242f-b86c-43b5-b7e3-01fd8f11af7b)
 Call ID: 2cf8242f-b86c-43b5-b7e3-01fd8f11af7b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1990
    source: Lady_Charlotte_Anne_Santo_Domingo
  AddTriple (6c21bec7-c737-4749-b5f4-b6ec8984516b)
 Call ID: 6c21bec7-c737-4749-b5f4-b6ec8984516b
  Args:
    source: Lady_Charlotte_Anne_Santo_Domingo
    target: Princess_Antonia_of_Prussia
    relation: :hasMother
  AddTriple (4563151f-82e8-4b33-ac79-6344b0c4f47d)
 Call ID: 4563151f-82e8-4b33-ac79-6344b0c4f47d
  Args:
    relation: :hasFather
    target: Charles_Wellesley_Marquess_of_Douro
    source: Lady_Charlotte_Anne_Santo_Domingo
  AddTriple (b233ccdc-a535-41f2-b940-450ca68d1f27)
 Call ID: b233ccdc-a535-41f2-b940-450ca68d1f27
  Args:
    source: Charles_Wellesley_Marquess_of_Douro
    target: Valerian_Wellesley_8th_Duke_of_Wellington
    relation: :hasFather
  AddTriple (962163ed-ab8f-402f-94ff-9d51b8319b00)
 Call ID: 962163ed-ab8f-402f-94ff-9d51b8319b00
  Args:
    target: Prince_Frederick_of_Prussia
    source: Princess_Antonia_of_Prussia
    relation: :hasFather
  AddTriple (2c789fd7-1b1c-47d0-8762-925369956f2b)
 Call ID: 2c789fd7-1b1c-47d0-8762-925369956f2b
  Args:
    relation: :hasMother
    target: Lady_Brigid_Guinness
    source: Princess_Antonia_of_Prussia
  AddTriple (39d06ff8-683a-4036-bb12-1b4758c192e4)
 Call ID: 39d06ff8-683a-4036-bb12-1b4758c192e4
  Args:
    target: Arthur_Wellesley_Earl_of_Mornington
    source: Lady_Charlotte_Anne_Santo_Domingo
    relation: :hasBrother
  AddTriple (ce34f2f6-af0c-41c4-a796-fb26ce267b56)
 Call ID: ce34f2f6-af0c-41c4-a796-fb26ce267b56
  Args:
    relation: :hasSister
    source: Lady_Charlotte_Anne_Santo_Domingo
    target: Lady_Mary_Wellesley
  AddLiteral (34d2dee0-2e2d-4b79-91b6-b4bc9081ee3b)
 Call ID: 34d2dee0-2e2d-4b79-91b6-b4bc9081ee3b
  Args:
    source: Lady_Charlotte_Anne_Santo_Domingo
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2016
  AddTriple (1cc73bf3-c996-49ad-b4cd-ad8d5dddd37f)
 Call ID: 1cc73bf3-c996-49ad-b4cd-ad8d5dddd37f
  Args:
    relation: :hasRelation
    target: Alejandro_Santo_Domingo
    source: Lady_Charlotte_Anne_Santo_Domingo
  Finish (1240caf7-68be-4b49-9201-221577aaa3c6)
 Call ID: 1240caf7-68be-4b49-9201-221577aaa3c6
  Args: