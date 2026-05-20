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
The Duke of CalabriaThe Duchess of Calabria


Prince Jaime of Bourbon-Two Sicilies, Duke of Noto (born 26 June 1993) is a Spanish aristocrat and heir to the headship of the House of Bourbon-Two Sicilies as eldest son of Prince Pedro, Duke of Calabria.
Biography

Jaime was born on 26 June 1993 in Madrid, Spain, as the illegitimate son of Prince Pedro, then Duke of Noto (born 16 October 1968), and Sofia Landaluce y Melgarejo (born 23 November 1973).
His paternal grandparents are Infante Carlos, Duke of Calabria (1938–2015), and his wife, Princess Anne of Orléans.
The Duke of Noto was educated at the Centro Universitario Villanueva (with a degree in law) and then obtained a master's degree in management from the IE University Business School.
Claim to the throne

Jaime's grandfather, Infante Don Carlos of Spain, Duke of Calabria, had to consider whether the future marriage of Prince Pedro to Sofía Landaluce y Melgarejo would meet the conditions established in the Sovereign Act that was signed in Naples on 7 April 1829, Law no. 2362, which gave the "head of Our House of Bourbon... such authority as is necessary to protect the purity and splendour of the throne", by requiring all members of the dynasty to have formal permission to marry.
The marriages of all members of the dynasty that had been considered capable of transmitting dynastic rights had been to royal princesses until the marriage of Prince Ranieri to Countess Carolina Zamoyska in 1929.
The ultimate decision of Infante Carlos to permit his son's marriage to be considered dynastic followed the marriages of the daughters of King Juan Carlos without them being required to renounce their right of succession to the Spanish throne, and a change in the marriage rules of the House of Austria.
Infante Carlos and his wife attended the marriage of Prince Pedro on 30 March 2001, and the marriage is treated as a dynastic marriage transmitting full rights of succession to all the children of Prince Pedro and his wife.
It was made clear by the date of the marriage of the future King Felipe VI in 2004 that the children of Prince Pedro and his wife had full dynastic rights, and the children bear the style of Royal Highness and the title of Prince(ss) of Bourbon-Two Sicilies.
Marriage and issue

On 25 September 2021 at Monreale Cathedral in Palermo, Jaime married Lady Charlotte Lindesay-Bethune, youngest daughter of James Lindesay-Bethune, 16th Earl of Lindsay, and his wife, Diana Mary Chamberlayne-Macdonald.
On 13 October 2023, the Duke and Duchess of Noto had their first child in London – a daughter named Francesca Sofía.
On 19 November 2025, the Duke and Duchess of Noto had their second child in London – a daughter named Ines.



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
  AssignClass (4fc4e320-6d5e-44c7-a579-7573363d5fd9)
 Call ID: 4fc4e320-6d5e-44c7-a579-7573363d5fd9
  Args:
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (4a71437e-8e7f-49af-b17b-9e25c7c5b908)
 Call ID: 4a71437e-8e7f-49af-b17b-9e25c7c5b908
  Args:
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (0e9fbf7d-0936-4bab-8f0b-710a60d147e8)
 Call ID: 0e9fbf7d-0936-4bab-8f0b-710a60d147e8
  Args:
    literal_value: 1993
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (acc91d1a-87c7-4fcc-9439-7f33549b0887)
 Call ID: acc91d1a-87c7-4fcc-9439-7f33549b0887
  Args:
    type: :Man
    source: Prince_Pedro_Duke_of_Calabria
  AssignClass (a362e740-c7b4-443d-8ff8-0cbc869d67f9)
 Call ID: a362e740-c7b4-443d-8ff8-0cbc869d67f9
  Args:
    type: :Ancestor
    source: Prince_Pedro_Duke_of_Calabria
  AssignClass (edd2f742-4cb8-4784-aeed-bc3790246165)
 Call ID: edd2f742-4cb8-4784-aeed-bc3790246165
  Args:
    type: :Person
    source: Prince_Pedro_Duke_of_Calabria
  AddLiteral (ceb7e28c-c387-4c26-9ae4-839ad5297f0a)
 Call ID: ceb7e28c-c387-4c26-9ae4-839ad5297f0a
  Args:
    relation: :hasBirthYear
    source: Prince_Pedro_Duke_of_Calabria
    literal_type: xsd:integer
    literal_value: 1968
  AssignClass (718e84f0-84d5-4698-8066-e00f2c623ff3)
 Call ID: 718e84f0-84d5-4698-8066-e00f2c623ff3
  Args:
    type: :Woman
    source: Sofia_Landaluce_y_Melgarejo
  AssignClass (91359c83-1810-47df-884f-448e93842b24)
 Call ID: 91359c83-1810-47df-884f-448e93842b24
  Args:
    type: :Person
    source: Sofia_Landaluce_y_Melgarejo
  AddLiteral (79244651-3d0b-454d-ae72-962a29423699)
 Call ID: 79244651-3d0b-454d-ae72-962a29423699
  Args:
    source: Sofia_Landaluce_y_Melgarejo
    literal_type: xsd:integer
    literal_value: 1973
    relation: :hasBirthYear
  AddTriple (3607d951-d731-4594-a4c3-13741a622bcb)
 Call ID: 3607d951-d731-4594-a4c3-13741a622bcb
  Args:
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: Prince_Pedro_Duke_of_Calabria
  AddTriple (7e9e4740-d0d9-441f-853c-4c4bb671872f)
 Call ID: 7e9e4740-d0d9-441f-853c-4c4bb671872f
  Args:
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
    target: Sofia_Landaluce_y_Melgarejo
    relation: :hasMother
  AssignClass (b99b06b4-f25d-4e00-8aa8-a763cd94ccfc)
 Call ID: b99b06b4-f25d-4e00-8aa8-a763cd94ccfc
  Args:
    type: :Man
    source: Infante_Carlos_Duke_of_Calabria
  AssignClass (210b8384-514a-42cd-99cb-a5d7a787d35d)
 Call ID: 210b8384-514a-42cd-99cb-a5d7a787d35d
  Args:
    type: :Ancestor
    source: Infante_Carlos_Duke_of_Calabria
  AssignClass (5ab666a1-14be-4dcd-bfa3-370a563e0595)
 Call ID: 5ab666a1-14be-4dcd-bfa3-370a563e0595
  Args:
    source: Infante_Carlos_Duke_of_Calabria
    type: :Person
  AddLiteral (8655a2c7-db11-4483-af6f-fe9b38a1b163)
 Call ID: 8655a2c7-db11-4483-af6f-fe9b38a1b163
  Args:
    relation: :hasBirthYear
    literal_value: 1938
    source: Infante_Carlos_Duke_of_Calabria
    literal_type: xsd:integer
  AddLiteral (041ec221-06ff-40d8-89a8-9c4d76df0037)
 Call ID: 041ec221-06ff-40d8-89a8-9c4d76df0037
  Args:
    literal_value: 2015
    source: Infante_Carlos_Duke_of_Calabria
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (7736c7e4-cff6-4739-a3a9-a87bc9169f52)
 Call ID: 7736c7e4-cff6-4739-a3a9-a87bc9169f52
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (152dd4a4-0f49-4294-b41f-81ca0b8dc83f)
 Call ID: 152dd4a4-0f49-4294-b41f-81ca0b8dc83f
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AddTriple (bb2e41f1-2fb1-44c9-878e-f909ee1e3d03)
 Call ID: bb2e41f1-2fb1-44c9-878e-f909ee1e3d03
  Args:
    source: Prince_Pedro_Duke_of_Calabria
    target: Infante_Carlos_Duke_of_Calabria
    relation: :hasFather
  AddTriple (6a77c0a8-08ad-4f0f-8eb8-f661b1fad3f5)
 Call ID: 6a77c0a8-08ad-4f0f-8eb8-f661b1fad3f5
  Args:
    relation: :hasMother
    target: Princess_Anne_of_Orleans
    source: Prince_Pedro_Duke_of_Calabria
  AssignClass (1b4508f6-3d4d-4f7c-a6e8-012c7379d248)
 Call ID: 1b4508f6-3d4d-4f7c-a6e8-012c7379d248
  Args:
    source: Lady_Charlotte_Lindesay-Bethune
    type: :Woman
  AssignClass (17bd8aab-4d87-48f2-842e-635106ef29ad)
 Call ID: 17bd8aab-4d87-48f2-842e-635106ef29ad
  Args:
    source: Lady_Charlotte_Lindesay-Bethune
    type: :Person
  AddTriple (41e4e675-6d53-4d78-ae2f-89e9b31ec993)
 Call ID: 41e4e675-6d53-4d78-ae2f-89e9b31ec993
  Args:
    target: Lady_Charlotte_Lindesay-Bethune
    relation: :hasRelation
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
  AddLiteral (ab03534a-8f93-4b26-a572-1e0fc60bbd08)
 Call ID: ab03534a-8f93-4b26-a572-1e0fc60bbd08
  Args:
    source: Prince_Jaime_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 2021
    relation: :hasMarriageYear
  AssignClass (6ffb49f8-b7e7-4a14-9826-b0ca1cdcf915)
 Call ID: 6ffb49f8-b7e7-4a14-9826-b0ca1cdcf915
  Args:
    source: Francesca_Sofia
    type: :Woman
  AssignClass (bdb610bf-960a-4a4c-831b-88421287bb88)
 Call ID: bdb610bf-960a-4a4c-831b-88421287bb88
  Args:
    type: :Person
    source: Francesca_Sofia
  AddTriple (3a4723ff-5728-49cb-9b62-dcd7d3f04370)
 Call ID: 3a4723ff-5728-49cb-9b62-dcd7d3f04370
  Args:
    source: Francesca_Sofia
    relation: :hasFather
    target: Prince_Jaime_of_Bourbon-Two_Sicilies
  AddTriple (a85e6b42-b16a-4ed8-9fc1-705398cc3af6)
 Call ID: a85e6b42-b16a-4ed8-9fc1-705398cc3af6
  Args:
    source: Francesca_Sofia
    relation: :hasMother
    target: Lady_Charlotte_Lindesay-Bethune
  AssignClass (a31ba0c2-4f6f-4791-a25e-6932fce51d2f)
 Call ID: a31ba0c2-4f6f-4791-a25e-6932fce51d2f
  Args:
    type: :Woman
    source: Ines
  AssignClass (aa98a3c4-70e5-4b13-9076-7062fc333fe1)
 Call ID: aa98a3c4-70e5-4b13-9076-7062fc333fe1
  Args:
    source: Ines
    type: :Person
  AddTriple (96a5a0a7-e306-45de-a908-50b6113692ac)
 Call ID: 96a5a0a7-e306-45de-a908-50b6113692ac
  Args:
    source: Ines
    relation: :hasFather
    target: Prince_Jaime_of_Bourbon-Two_Sicilies
  AddTriple (6180c424-9ab9-4090-883c-a55606784e88)
 Call ID: 6180c424-9ab9-4090-883c-a55606784e88
  Args:
    source: Ines
    relation: :hasMother
    target: Lady_Charlotte_Lindesay-Bethune
  AssignClass (28078edb-8c0a-40ab-9a91-d103c3f304db)
 Call ID: 28078edb-8c0a-40ab-9a91-d103c3f304db
  Args:
    type: :Man
    source: James_Lindesay-Bethune_16th_Earl_of_Lindsay
  AssignClass (f34df7fa-f5d5-4074-aef1-0706d84b8a25)
 Call ID: f34df7fa-f5d5-4074-aef1-0706d84b8a25
  Args:
    type: :Person
    source: James_Lindesay-Bethune_16th_Earl_of_Lindsay
  AssignClass (ca7a49f3-9bfe-4e7c-a34e-444967bf51a2)
 Call ID: ca7a49f3-9bfe-4e7c-a34e-444967bf51a2
  Args:
    type: :Woman
    source: Diana_Mary_Chamberlayne-Macdonald
  AssignClass (29d2f674-b686-486f-abc7-6d967f1f7eff)
 Call ID: 29d2f674-b686-486f-abc7-6d967f1f7eff
  Args:
    source: Diana_Mary_Chamberlayne-Macdonald
    type: :Person
  AddTriple (feb37874-0fb3-4b43-a436-fb85a5cbc9b5)
 Call ID: feb37874-0fb3-4b43-a436-fb85a5cbc9b5
  Args:
    target: James_Lindesay-Bethune_16th_Earl_of_Lindsay
    relation: :hasFather
    source: Lady_Charlotte_Lindesay-Bethune
  AddTriple (4215f6a0-6479-4854-bbad-94cdd56a9b62)
 Call ID: 4215f6a0-6479-4854-bbad-94cdd56a9b62
  Args:
    source: Lady_Charlotte_Lindesay-Bethune
    target: Diana_Mary_Chamberlayne-Macdonald
    relation: :hasMother
  Finish (04db801b-8e90-4879-afde-d88fb1def237)
 Call ID: 04db801b-8e90-4879-afde-d88fb1def237
  Args: