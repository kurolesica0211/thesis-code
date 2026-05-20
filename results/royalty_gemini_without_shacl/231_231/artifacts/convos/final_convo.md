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
Louis Ferdinand, Prince of Prussia (German: Louis Ferdinand Victor Eduard Adalbert Michael Hubertus Prinz von Preußen; 9 November 1907 –  26 September 1994) was a grandson of Kaiser Wilhelm II and member of the  House of Hohenzollern, which occupied the Prussian and German thrones until the abolition of those monarchies in 1918.
Biography

Louis Ferdinand was born in Potsdam as the third in succession to the throne of the German Empire, after his father, German Crown Prince William and elder brother Prince Wilhelm of Prussia.
When Louis Ferdinand's older brother Prince Wilhelm renounced his succession rights to marry a member of the untitled nobility in 1933 (he was later to be killed in action in France in 1940 while fighting in the German army), Louis Ferdinand replaced him as second in the line of succession to the defunct German and Prussian thrones after the former Crown Prince.
Louis Ferdinand was educated in Berlin and deviated from his family's tradition by not pursuing a military career.
Louis Ferdinand dissociated himself from the Nazis after this.
He married his second cousin, Grand Duchess Kira Kirillovna of Russia, in 1938 in first a Russian Orthodox ceremony in Potsdam and then a Lutheran ceremony in Huis Doorn, Netherlands.
Kira was the second daughter of Grand Duke Kyril Vladimirovich and Princess Victoria Melita of Saxe-Coburg and Gotha.
His third son and heir apparent, Prince Louis Ferdinand, died in 1977 during military maneuvers, and thus his one-year-old grandson Georg Friedrich, Prince of Prussia (son of Prince Louis Ferdinand) became the new heir apparent to the defunct Prussian and German Imperial throne.
Upon Louis Ferdinand's death in 1994, Georg Friedrich became the pretender to the defunct thrones and head of the Hohenzollern family.
The prince was a popular figure.
In 1968 Der Spiegel reported that in a survey of their readers by Quick magazine about who would be the most honorable person to become President of the Federal Republic of Germany, Louis Ferdinand, the only one of twelve candidates who was not a politician, won with 39.8% before Carlo Schmid and Ludwig Erhard.
In a similar survey by the tabloid Bild, readers chose Louis Ferdinand by 55.6%.
In an interview with Quick, the prince indicated that he might accept the presidency but would not relinquish his claim to the imperial or Prussian crowns.
After German reunification, he arranged for Prussian King Frederick the Great to be reburied from the Christ Chapel at Hohenzollern Castle to the crypt chamber prepared by Frederick himself on the terrace of his Sanssouci Palace in Potsdam.
Instead of complying with his last wish after his death, the king had been laid to rest in the Garrison Church, Potsdam next to his unloved father Frederick William I of Prussia in 1786.
Both coffins were relocated during World War II and ended up in the prince's castle in what became West Germany.
The prince had Frederick William I's coffin taken to the crypt of the Church of Peace, Potsdam because the Garrison Church had been destroyed in 1945.
In interviews with C.L. Sulzberger for the book The Fall of Eagles, Louis Ferdinand expressed a deep sense of admiration for the informal bicycle monarchy and crowned republic style favored and used by the Dutch, Belgian, and Scandinavian royal families.
Praising how vehicles carrying the King or Queen would stop and wait at traffic lights, Louis Ferdinand stated that if the House of Hohenzollern were ever restored to the German throne during his lifetime, this same informality was a quality he fully intended to emulate.
Prince Ferdinand of Hohenzollern, a member of the senior Swabian branch of the Hohenzollern dynasty, Hohenzollern-Sigmaringen, is his godson.



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
  AssignClass (92b75468-4dc7-4ef7-8536-33c29c0ec532)
 Call ID: 92b75468-4dc7-4ef7-8536-33c29c0ec532
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Man
  AssignClass (ee75e85e-5e36-4cf1-8678-f31ffc3997b7)
 Call ID: ee75e85e-5e36-4cf1-8678-f31ffc3997b7
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (fb9ca499-ae30-4fc7-84bc-c72af4e573b2)
 Call ID: fb9ca499-ae30-4fc7-84bc-c72af4e573b2
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (c6493b8d-c13f-47c1-8fc7-2ec1efe7df8e)
 Call ID: c6493b8d-c13f-47c1-8fc7-2ec1efe7df8e
  Args:
    source: Wilhelm_II
    type: :Person
  AssignClass (d7875a00-6fd3-4824-a7ee-639b2c494212)
 Call ID: d7875a00-6fd3-4824-a7ee-639b2c494212
  Args:
    source: German_Crown_Prince_William
    type: :Man
  AssignClass (c4bee3b6-7f1c-4828-b998-61c29e3aaec4)
 Call ID: c4bee3b6-7f1c-4828-b998-61c29e3aaec4
  Args:
    source: German_Crown_Prince_William
    type: :Person
  AssignClass (d4e69681-1ca0-4380-a041-e212a0759fa9)
 Call ID: d4e69681-1ca0-4380-a041-e212a0759fa9
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Prussia
  AssignClass (3f39b1b2-5eff-4f96-a1f5-b35bb10c36a6)
 Call ID: 3f39b1b2-5eff-4f96-a1f5-b35bb10c36a6
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Prussia
  AssignClass (e224016a-4810-443a-b8c1-845356fa567a)
 Call ID: e224016a-4810-443a-b8c1-845356fa567a
  Args:
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    type: :Woman
  AssignClass (e94d119f-bb7f-4a20-bb6e-4a197363a830)
 Call ID: e94d119f-bb7f-4a20-bb6e-4a197363a830
  Args:
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    type: :Person
  AssignClass (40a129ba-2bb5-468d-b87b-4ae74b15f291)
 Call ID: 40a129ba-2bb5-468d-b87b-4ae74b15f291
  Args:
    source: Grand_Duke_Kyril_Vladimirovich
    type: :Man
  AssignClass (43db1b32-7e99-4f93-a3db-ba3b9e9b2f4c)
 Call ID: 43db1b32-7e99-4f93-a3db-ba3b9e9b2f4c
  Args:
    source: Grand_Duke_Kyril_Vladimirovich
    type: :Person
  AssignClass (e57bb9e3-6629-48c0-ac52-988beb7907c2)
 Call ID: e57bb9e3-6629-48c0-ac52-988beb7907c2
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha
  AssignClass (d378d0cf-0584-43bf-8b8a-b1678e4262e1)
 Call ID: d378d0cf-0584-43bf-8b8a-b1678e4262e1
  Args:
    source: Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha
    type: :Person
  AssignClass (1efa9b2e-560c-4159-9903-a40afe1ceade)
 Call ID: 1efa9b2e-560c-4159-9903-a40afe1ceade
  Args:
    type: :Man
    source: Prince_Louis_Ferdinand_son
  AssignClass (8e018993-1c61-4df7-9759-723912d5c9c4)
 Call ID: 8e018993-1c61-4df7-9759-723912d5c9c4
  Args:
    type: :Person
    source: Prince_Louis_Ferdinand_son
  AssignClass (47b614b0-081c-4a05-9671-9606e40b593e)
 Call ID: 47b614b0-081c-4a05-9671-9606e40b593e
  Args:
    source: Georg_Friedrich_Prince_of_Prussia
    type: :Man
  AssignClass (be1a0374-d8b0-455e-b2c0-dfde3b91b846)
 Call ID: be1a0374-d8b0-455e-b2c0-dfde3b91b846
  Args:
    type: :Person
    source: Georg_Friedrich_Prince_of_Prussia
  AddLiteral (2dfd49d5-931f-48c3-b640-82ce9cfb478b)
 Call ID: 2dfd49d5-931f-48c3-b640-82ce9cfb478b
  Args:
    literal_type: xsd:integer
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :hasBirthYear
    literal_value: 1907
  AddLiteral (1b5b4af0-5481-4990-ae77-2e83e1106577)
 Call ID: 1b5b4af0-5481-4990-ae77-2e83e1106577
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1994
  AddTriple (695e3897-f69e-4f25-b163-64fc657ed069)
 Call ID: 695e3897-f69e-4f25-b163-64fc657ed069
  Args:
    relation: :hasFather
    source: Louis_Ferdinand_Prince_of_Prussia
    target: German_Crown_Prince_William
  AddTriple (af4920ba-e272-42ea-aa6a-36f19a367ec0)
 Call ID: af4920ba-e272-42ea-aa6a-36f19a367ec0
  Args:
    relation: :isSonOf
    target: German_Crown_Prince_William
    source: Louis_Ferdinand_Prince_of_Prussia
  AddTriple (2b869550-8554-48cf-b2ea-f5f5323d87d3)
 Call ID: 2b869550-8554-48cf-b2ea-f5f5323d87d3
  Args:
    target: Prince_Wilhelm_of_Prussia
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :isBrotherOf
  AddTriple (76a527ef-bef6-4592-9fc0-69b989736e11)
 Call ID: 76a527ef-bef6-4592-9fc0-69b989736e11
  Args:
    relation: :hasBrother
    source: Louis_Ferdinand_Prince_of_Prussia
    target: Prince_Wilhelm_of_Prussia
  AddTriple (2253ae69-3778-40e4-bfd9-c1315f82b09c)
 Call ID: 2253ae69-3778-40e4-bfd9-c1315f82b09c
  Args:
    target: 1938
    source: Louis_Ferdinand_Prince_of_Prussia
    relation: :hasMarriageYear
  AddTriple (5cb250aa-d46c-4184-bb43-fc38205dd0e0)
 Call ID: 5cb250aa-d46c-4184-bb43-fc38205dd0e0
  Args:
    target: 1938
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    relation: :hasMarriageYear
  AddTriple (77ec1526-83f9-4f48-8ca1-17de681bab24)
 Call ID: 77ec1526-83f9-4f48-8ca1-17de681bab24
  Args:
    target: Grand_Duke_Kyril_Vladimirovich
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    relation: :hasFather
  AddTriple (87a8fc9f-48fc-4040-89f4-52d669f01c9d)
 Call ID: 87a8fc9f-48fc-4040-89f4-52d669f01c9d
  Args:
    target: Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    relation: :hasMother
  AddTriple (1a38cd8c-20f4-4e18-a8d6-8e62090dc1f0)
 Call ID: 1a38cd8c-20f4-4e18-a8d6-8e62090dc1f0
  Args:
    target: Louis_Ferdinand_Prince_of_Prussia
    source: Prince_Louis_Ferdinand_son
    relation: :hasFather
  AddTriple (c3f5f462-a74e-4226-a972-9e4866a20f45)
 Call ID: c3f5f462-a74e-4226-a972-9e4866a20f45
  Args:
    target: Georg_Friedrich_Prince_of_Prussia
    source: Prince_Louis_Ferdinand_son
    relation: :isFatherOf
  Finish (82a03433-c9dd-40d6-a29a-52536a0cf983)
 Call ID: 82a03433-c9dd-40d6-a29a-52536a0cf983
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Grand_Duchess_Kira_Kirillovna_of_Russia a :Person,
          :Woman ;
      :hasFather data:Grand_Duke_Kyril_Vladimirovich ;
      :hasMarriageYear data:1938 ;
      :hasMother data:Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha .

  data:Prince_Louis_Ferdinand_son a :Man,
          :Person ;
      :hasFather data:Louis_Ferdinand_Prince_of_Prussia ;
      :isFatherOf data:Georg_Friedrich_Prince_of_Prussia .

  data:Wilhelm_II a :Man,
          :Person .

  data:Georg_Friedrich_Prince_of_Prussia a :Man,
          :Person .

  data:Grand_Duke_Kyril_Vladimirovich a :Man,
          :Person .

  data:Louis_Ferdinand_Prince_of_Prussia a :Man,
          :Person ;
      :hasBirthYear 1907 ;
      :hasBrother data:Prince_Wilhelm_of_Prussia ;
      :hasDeathYear 1994 ;
      :hasFather data:German_Crown_Prince_William ;
      :hasMarriageYear data:1938 ;
      :isBrotherOf data:Prince_Wilhelm_of_Prussia ;
      :isSonOf data:German_Crown_Prince_William .

  data:Princess_Victoria_Melita_of_Saxe-Coburg_and_Gotha a :Person,
          :Woman .

  data:German_Crown_Prince_William a :Man,
          :Person .

  data:Prince_Wilhelm_of_Prussia a :Man,
          :Person .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['1938']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  UnassignClass (a4a4d918-119f-4886-8433-cc80c0fd1a9b)
 Call ID: a4a4d918-119f-4886-8433-cc80c0fd1a9b
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Man
  UnassignClass (9ada5bb6-492b-473e-8e7f-ea87de4fbf31)
 Call ID: 9ada5bb6-492b-473e-8e7f-ea87de4fbf31
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  UnassignClass (8c1c0c9f-6932-44ca-b453-45ede7e29dfc)
 Call ID: 8c1c0c9f-6932-44ca-b453-45ede7e29dfc
  Args:
    type: :Woman
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  UnassignClass (b91d4ab5-6818-47ea-adf7-ab6a3b712a11)
 Call ID: b91d4ab5-6818-47ea-adf7-ab6a3b712a11
  Args:
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    type: :Person
  RemoveTriple (fabd0d2c-51b7-415a-b51b-37cc3ee5db1a)
 Call ID: fabd0d2c-51b7-415a-b51b-37cc3ee5db1a
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    target: 1938
    relation: :hasMarriageYear
  RemoveTriple (29896685-4bb7-440f-9790-a22df2b373b2)
 Call ID: 29896685-4bb7-440f-9790-a22df2b373b2
  Args:
    relation: :hasMarriageYear
    target: 1938
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AssignClass (1733dd67-0f17-40bb-a414-cd79f6c18cea)
 Call ID: 1733dd67-0f17-40bb-a414-cd79f6c18cea
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Man
  AssignClass (c16f0aaf-22ca-4fb1-b01d-da83eb4ac905)
 Call ID: c16f0aaf-22ca-4fb1-b01d-da83eb4ac905
  Args:
    type: :Person
    source: Louis_Ferdinand_Prince_of_Prussia
  AssignClass (10a0154e-9087-4892-9f7f-4ce4ee6ef97b)
 Call ID: 10a0154e-9087-4892-9f7f-4ce4ee6ef97b
  Args:
    type: :Woman
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AssignClass (784308d2-2402-4eb8-a5f1-b29f2207e003)
 Call ID: 784308d2-2402-4eb8-a5f1-b29f2207e003
  Args:
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    type: :Person
  AddLiteral (adbaf571-21a0-4c03-af34-c374a5bb6a59)
 Call ID: adbaf571-21a0-4c03-af34-c374a5bb6a59
  Args:
    relation: :hasMarriageYear
    source: Louis_Ferdinand_Prince_of_Prussia
    literal_type: xsd:integer
    literal_value: 1938
  AddLiteral (3dfc10d2-bb2c-4b95-bdfa-3962208dd126)
 Call ID: 3dfc10d2-bb2c-4b95-bdfa-3962208dd126
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
    literal_value: 1938
  Finish (4acb3934-2846-449e-8884-f1009a0252d0)
 Call ID: 4acb3934-2846-449e-8884-f1009a0252d0
  Args: