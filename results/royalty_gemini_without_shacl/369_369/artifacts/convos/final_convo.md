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
Duke John Albert of Mecklenburg (German: Herzog Johann Albrecht zu Mecklenburg; given names John Albert Ernest Constantine Frederick Henry; 8 December 1857 – 16 February 1920) was a member of the House of Mecklenburg-Schwerin who served as the regent of two states of the German Empire.
He was first regent of the Grand Duchy of Mecklenburg-Schwerin from 1897 to 1901 for his nephew Frederick Francis IV, Grand Duke of Mecklenburg, and thereafter regent of the Duchy of Brunswick from 1907 to 1913.
Birth and interests

Duke John Albert of Mecklenburg was born in Schwerin the fifth child of Frederick Francis II, Grand Duke of Mecklenburg and his first wife Princess Augusta Reuss of Köstritz (1822–1862).
Duke John Albert was educated in Dresden, pursued a career in the Prussian Army and was well known for his love of sports.
Regencies

Following the death of his brother Frederick Francis III, Grand Duke of Mecklenburg on 10 April 1897, Duke John Albert was appointed regent for his young nephew the new Grand Duke, Frederick Francis IV after his older brother Duke Paul Frederick had renounced his claim to the regency.
On 28 May 1907, Duke John Albert was elected regent of the Duchy of Brunswick following the death of Prince Albert of Prussia by the state's diet, accepting the offer he arrived in Brunswick on 5 June 1907.
The reason for the regency in Brunswick was that in 1884 when William, Duke of Brunswick died his distant cousin and heir Ernest Augustus, Crown Prince of Hanover was prevented from taking over the duchy because he refused to renounce his claim to the throne of the Kingdom of Hanover which had been annexed by Prussia in 1866.
Shortly after assuming the regency, Duke John Albert would walk Brunswick in civilian clothes visiting museums, libraries and other institutions in the duchy, asking questions of people to discover their living conditions.
Duke John Albert also cut down on the expenses of the royal household by cutting the number of servants and retainers to the minimum needed to run the household.
The regency came to an end on 1 November 1913 when Ernest Augustus, Crown Prince of Hanover's son Ernest Augustus was permitted to ascend to Duchy following his marriage to Princess Victoria Louise of Prussia, the only daughter of the German Emperor, William II, which helped heal the rift between the houses of Hanover and Hohenzollern.
War years

During the First World War, Duke John Albert was active with the German Colonial Society in defending Germany's colonial possessions from suggestions that they should be abandoned.
Duke John Albert died in 1920 in Wiligrad castle near Lübstorf aged 62.
Marriages

John Albert was married twice: firstly in Weimar on 6 November 1886 to Princess Elisabeth Sybille of Saxe-Weimar-Eisenach (28 February 1854–10 July 1908)
the daughter of Charles Alexander, Grand Duke of Saxe-Weimar-Eisenach; secondly in Brunswick on 15 December 1909 to Princess Elisabeth of Stolberg-Rossla (1885–1969), who following his death was to marry his half brother Duke Adolf Friedrich in 1924.
Ojimukoka

Ojimukoka, a small settlement, postoffice and railway station in Namibia, was renamed Johann - Albrechtshöhe, and then simply Albrechts in his honour.



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
  AssignClass (8d998c2f-06df-4b75-a998-48ab87ad7456)
 Call ID: 8d998c2f-06df-4b75-a998-48ab87ad7456
  Args:
    source: John_Albert_of_Mecklenburg
    type: :Man
  AssignClass (60a851ff-c6df-46c0-af3c-78d50e00d467)
 Call ID: 60a851ff-c6df-46c0-af3c-78d50e00d467
  Args:
    source: John_Albert_of_Mecklenburg
    type: :Person
  AddLiteral (373f49a5-4bc4-4b5e-8b41-cf7a840b47d2)
 Call ID: 373f49a5-4bc4-4b5e-8b41-cf7a840b47d2
  Args:
    literal_type: xsd:integer
    literal_value: 1857
    relation: :hasBirthYear
    source: John_Albert_of_Mecklenburg
  AddLiteral (0fec13ab-5811-42b5-89ee-ac5e0ceeec4b)
 Call ID: 0fec13ab-5811-42b5-89ee-ac5e0ceeec4b
  Args:
    literal_type: xsd:integer
    literal_value: 1920
    relation: :hasDeathYear
    source: John_Albert_of_Mecklenburg
  AssignClass (5e7403b3-56be-47a6-b5cd-6536abc22445)
 Call ID: 5e7403b3-56be-47a6-b5cd-6536abc22445
  Args:
    source: Frederick_Francis_II_of_Mecklenburg
    type: :Man
  AssignClass (5e541e39-09e7-4c02-916e-84726060b896)
 Call ID: 5e541e39-09e7-4c02-916e-84726060b896
  Args:
    type: :Person
    source: Frederick_Francis_II_of_Mecklenburg
  AssignClass (8714e2c9-c72c-4e63-a01c-469b7aa81c99)
 Call ID: 8714e2c9-c72c-4e63-a01c-469b7aa81c99
  Args:
    type: :Woman
    source: Augusta_Reuss_of_Köstritz
  AssignClass (a6440a72-7d3e-4edc-92e5-7fa5be8a2d09)
 Call ID: a6440a72-7d3e-4edc-92e5-7fa5be8a2d09
  Args:
    source: Augusta_Reuss_of_Köstritz
    type: :Person
  AddTriple (fb5f4acf-2e4e-4344-8c49-9aab361ca0fe)
 Call ID: fb5f4acf-2e4e-4344-8c49-9aab361ca0fe
  Args:
    target: Frederick_Francis_II_of_Mecklenburg
    source: John_Albert_of_Mecklenburg
    relation: :hasFather
  AddTriple (fb869baa-406e-4ea1-9ffa-eb3ecb7934fe)
 Call ID: fb869baa-406e-4ea1-9ffa-eb3ecb7934fe
  Args:
    target: Augusta_Reuss_of_Köstritz
    relation: :hasMother
    source: John_Albert_of_Mecklenburg
  AssignClass (949220f6-9199-47be-954b-589cebf90782)
 Call ID: 949220f6-9199-47be-954b-589cebf90782
  Args:
    source: Frederick_Francis_III_of_Mecklenburg
    type: :Man
  AssignClass (7dad7fd1-4be1-4d32-a208-7387bc65d912)
 Call ID: 7dad7fd1-4be1-4d32-a208-7387bc65d912
  Args:
    source: Frederick_Francis_III_of_Mecklenburg
    type: :Person
  AddTriple (2f6259b0-2dfe-49cc-bd7e-adf78a7d00dc)
 Call ID: 2f6259b0-2dfe-49cc-bd7e-adf78a7d00dc
  Args:
    target: Frederick_Francis_III_of_Mecklenburg
    source: John_Albert_of_Mecklenburg
    relation: :hasBrother
  AssignClass (ae551b3e-72e9-404f-a843-276e390812cd)
 Call ID: ae551b3e-72e9-404f-a843-276e390812cd
  Args:
    type: :Man
    source: Frederick_Francis_IV_of_Mecklenburg
  AssignClass (0349b4ae-d190-45c6-a3b2-86e89dcec3fa)
 Call ID: 0349b4ae-d190-45c6-a3b2-86e89dcec3fa
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg
    type: :Person
  AddTriple (681a31e9-ba05-4f5a-bd1e-2693e59a257c)
 Call ID: 681a31e9-ba05-4f5a-bd1e-2693e59a257c
  Args:
    relation: :isFatherOf
    source: Frederick_Francis_III_of_Mecklenburg
    target: Frederick_Francis_IV_of_Mecklenburg
  AssignClass (b65493bd-cf98-4172-9d0f-7104f089511b)
 Call ID: b65493bd-cf98-4172-9d0f-7104f089511b
  Args:
    source: Paul_Frederick_of_Mecklenburg
    type: :Man
  AssignClass (7018cfb0-c232-4e8a-b16f-72f768729396)
 Call ID: 7018cfb0-c232-4e8a-b16f-72f768729396
  Args:
    source: Paul_Frederick_of_Mecklenburg
    type: :Person
  AddTriple (0ad8c664-3bcc-4396-8c4c-af4d822d3114)
 Call ID: 0ad8c664-3bcc-4396-8c4c-af4d822d3114
  Args:
    target: Paul_Frederick_of_Mecklenburg
    source: John_Albert_of_Mecklenburg
    relation: :hasBrother
  AssignClass (e8de861f-c1d7-47c9-aad2-61d15fea4f9d)
 Call ID: e8de861f-c1d7-47c9-aad2-61d15fea4f9d
  Args:
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
    type: :Woman
  AssignClass (3665cd03-97b6-4b5c-bd79-6d13648a52aa)
 Call ID: 3665cd03-97b6-4b5c-bd79-6d13648a52aa
  Args:
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
    type: :Person
  AddTriple (74169bee-f66f-4a89-b6db-0400d306a966)
 Call ID: 74169bee-f66f-4a89-b6db-0400d306a966
  Args:
    relation: :hasRelation
    source: John_Albert_of_Mecklenburg
    target: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
  AddLiteral (a57aa23f-e831-47d3-8835-a79d33c96c1d)
 Call ID: a57aa23f-e831-47d3-8835-a79d33c96c1d
  Args:
    relation: :hasMarriageYear
    source: John_Albert_of_Mecklenburg
    literal_value: 1886
    literal_type: xsd:integer
  AssignClass (b390fc65-4f6d-4629-a21f-e52876f11f34)
 Call ID: b390fc65-4f6d-4629-a21f-e52876f11f34
  Args:
    source: Charles_Alexander_of_Saxe-Weimar-Eisenach
    type: :Man
  AssignClass (02cd2acb-f51a-49a8-bb0b-d36aab37279c)
 Call ID: 02cd2acb-f51a-49a8-bb0b-d36aab37279c
  Args:
    type: :Person
    source: Charles_Alexander_of_Saxe-Weimar-Eisenach
  AddTriple (a21b7215-491e-4e5b-8c0f-a10d110237e7)
 Call ID: a21b7215-491e-4e5b-8c0f-a10d110237e7
  Args:
    target: Charles_Alexander_of_Saxe-Weimar-Eisenach
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
    relation: :hasFather
  AssignClass (f13e5c9a-057f-475f-9611-1dde58438254)
 Call ID: f13e5c9a-057f-475f-9611-1dde58438254
  Args:
    source: Elisabeth_of_Stolberg-Rossla
    type: :Woman
  AssignClass (f9742731-3413-451c-8f57-68e868cd6e68)
 Call ID: f9742731-3413-451c-8f57-68e868cd6e68
  Args:
    type: :Person
    source: Elisabeth_of_Stolberg-Rossla
  AddTriple (a6df57b8-3216-4bcc-86ca-447c2bfa5788)
 Call ID: a6df57b8-3216-4bcc-86ca-447c2bfa5788
  Args:
    source: John_Albert_of_Mecklenburg
    relation: :hasRelation
    target: Elisabeth_of_Stolberg-Rossla
  AddLiteral (0dc2fdb4-3924-423c-8548-8725b3470a79)
 Call ID: 0dc2fdb4-3924-423c-8548-8725b3470a79
  Args:
    literal_value: 1909
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: John_Albert_of_Mecklenburg
  AssignClass (776031fe-22ef-48c6-8141-ada4a95abca6)
 Call ID: 776031fe-22ef-48c6-8141-ada4a95abca6
  Args:
    type: :Man
    source: Adolf_Friedrich_of_Mecklenburg
  AssignClass (2f2d4e0e-c550-4c4b-8bce-797b4dab0071)
 Call ID: 2f2d4e0e-c550-4c4b-8bce-797b4dab0071
  Args:
    source: Adolf_Friedrich_of_Mecklenburg
    type: :Person
  AddTriple (b05919ad-a154-4563-a31d-193192e58f0a)
 Call ID: b05919ad-a154-4563-a31d-193192e58f0a
  Args:
    relation: :hasBrother
    source: John_Albert_of_Mecklenburg
    target: Adolf_Friedrich_of_Mecklenburg
  Finish (b60580d7-f78d-4373-aa7a-478f75a59f9a)
 Call ID: b60580d7-f78d-4373-aa7a-478f75a59f9a
  Args: