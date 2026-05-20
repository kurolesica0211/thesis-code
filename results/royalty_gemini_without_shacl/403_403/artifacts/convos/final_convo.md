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
Prince Wolfgang of Hesse (Wolfgang Moritz Prinz von Hessen; 6 November 1896 – 12 July 1989) was the district administrator of Obertaunuskreis from 1933 to 1945.
Wolfgang was born at Castle Rumpenheim, Offenbach am Main, the fourth son of Prince Frederick Charles of Hesse (1868–1940) and Princess Margaret of Prussia (1872–1954).
His maternal uncle was the German Emperor Willhelm II.
In World War I, Wolfgang served as an officer in the command of Field Marshal August von Mackensen.
Towards the end of the war, Wolfgang's father Frederick Charles of Hesse was selected by the Central Powers as a prospective King of Finland on 9 October 1918, to replace his first cousin once removed, the deposed Russian emperor, Nicholas II, who was titled Grand Duke of Finland.
Wolfgang was designated heir, in preference to his elder twin brother Philipp to ensure the separation of the thrones of Hesse and Finland.
However, Frederick Charles renounced his candidature on 14 December 1918, and the title was never actually held by the family.
Wolfgang married on 17 September 1924 Princess Marie Alexandra of Baden (1902–1944), daughter of Prince Maximilian of Baden and Princess Marie Louise of Hanover; they had no children.
He joined the NSDAP and the SA in December 1933, and was appointed Landrat (district administrator) of Obertaunuskreis, a landkreis in the state of Hesse, serving in that capacity until the end of  World War II.



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
  AssignClass (c8154e11-8a43-4ae0-9b3a-4648285ff0cb)
 Call ID: c8154e11-8a43-4ae0-9b3a-4648285ff0cb
  Args:
    type: :Man
    source: Wolfgang_of_Hesse
  AssignClass (8d37e02f-b281-4aef-90bb-5d9157850ca4)
 Call ID: 8d37e02f-b281-4aef-90bb-5d9157850ca4
  Args:
    type: :Man
    source: Frederick_Charles_of_Hesse
  AssignClass (d08c6003-dba7-4312-9ca6-cb33582c374b)
 Call ID: d08c6003-dba7-4312-9ca6-cb33582c374b
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (596a6e2f-43b6-4590-a057-64dcd4124661)
 Call ID: 596a6e2f-43b6-4590-a057-64dcd4124661
  Args:
    source: Philipp_of_Hesse
    type: :Man
  AssignClass (e9c5646e-9cbc-4626-b9ed-a5fd97c0e55c)
 Call ID: e9c5646e-9cbc-4626-b9ed-a5fd97c0e55c
  Args:
    type: :Woman
    source: Marie_Alexandra_of_Baden
  AssignClass (ddc45b70-09f4-4b78-a7b8-bdf77ebbbfa6)
 Call ID: ddc45b70-09f4-4b78-a7b8-bdf77ebbbfa6
  Args:
    source: Maximilian_of_Baden
    type: :Man
  AssignClass (2aa8aa73-74d9-480e-9dd0-133b83a39124)
 Call ID: 2aa8aa73-74d9-480e-9dd0-133b83a39124
  Args:
    type: :Woman
    source: Marie_Louise_of_Hanover
  AddLiteral (b599cf30-78a8-494f-aafe-b55a57dc862e)
 Call ID: b599cf30-78a8-494f-aafe-b55a57dc862e
  Args:
    literal_type: xsd:integer
    source: Wolfgang_of_Hesse
    literal_value: 1896
    relation: :hasBirthYear
  AddLiteral (02a97afe-19fd-47de-adba-7053d268a25b)
 Call ID: 02a97afe-19fd-47de-adba-7053d268a25b
  Args:
    literal_type: xsd:integer
    literal_value: 1989
    source: Wolfgang_of_Hesse
    relation: :hasDeathYear
  AddTriple (3c4af477-1320-42f3-95d2-a36e89e1642a)
 Call ID: 3c4af477-1320-42f3-95d2-a36e89e1642a
  Args:
    source: Wolfgang_of_Hesse
    relation: :hasFather
    target: Frederick_Charles_of_Hesse
  AddTriple (fb2cc746-535a-4639-b1c0-7d793e2fe506)
 Call ID: fb2cc746-535a-4639-b1c0-7d793e2fe506
  Args:
    relation: :hasMother
    target: Margaret_of_Prussia
    source: Wolfgang_of_Hesse
  AddTriple (4f399351-2fe2-4ed4-a188-aa0daf187d80)
 Call ID: 4f399351-2fe2-4ed4-a188-aa0daf187d80
  Args:
    source: Philipp_of_Hesse
    target: Wolfgang_of_Hesse
    relation: :isBrotherOf
  AddTriple (c84992cb-8ce5-4a0e-9754-4f7fc109d4ff)
 Call ID: c84992cb-8ce5-4a0e-9754-4f7fc109d4ff
  Args:
    source: Wolfgang_of_Hesse
    target: Philipp_of_Hesse
    relation: :isBrotherOf
  AddTriple (454c7c44-8f01-42e4-a08f-2b89ffd1bbf7)
 Call ID: 454c7c44-8f01-42e4-a08f-2b89ffd1bbf7
  Args:
    source: Philipp_of_Hesse
    relation: :hasFather
    target: Frederick_Charles_of_Hesse
  AddTriple (da6d2f30-416d-4765-908e-ecab59efe476)
 Call ID: da6d2f30-416d-4765-908e-ecab59efe476
  Args:
    target: Margaret_of_Prussia
    relation: :hasMother
    source: Philipp_of_Hesse
  AddLiteral (03bbb71a-2df5-4092-b417-e2cad626ea0a)
 Call ID: 03bbb71a-2df5-4092-b417-e2cad626ea0a
  Args:
    relation: :hasMarriageYear
    source: Wolfgang_of_Hesse
    literal_value: 1924
    literal_type: xsd:integer
  AddTriple (bdad94b5-5d20-4653-a4de-a7097bbb0508)
 Call ID: bdad94b5-5d20-4653-a4de-a7097bbb0508
  Args:
    target: Marie_Alexandra_of_Baden
    relation: :hasRelation
    source: Wolfgang_of_Hesse
  AddTriple (48044716-a616-49ef-a487-e840cf014272)
 Call ID: 48044716-a616-49ef-a487-e840cf014272
  Args:
    relation: :hasFather
    target: Maximilian_of_Baden
    source: Marie_Alexandra_of_Baden
  AddTriple (b794b6ec-ba40-43c8-bead-1d083cf43111)
 Call ID: b794b6ec-ba40-43c8-bead-1d083cf43111
  Args:
    source: Marie_Alexandra_of_Baden
    target: Marie_Louise_of_Hanover
    relation: :hasMother
  Finish (6b995886-358b-46b5-8322-f27f3610d03e)
 Call ID: 6b995886-358b-46b5-8322-f27f3610d03e
  Args: