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
Princess Alexandrine Irene of Prussia (7 April 1915 – 2 October 1980) was the elder daughter and fifth child of Wilhelm, German Crown Prince, and Cecilie of Mecklenburg-Schwerin.
Her grandparents were Wilhelm II, German Emperor and his wife Augusta Victoria of Schleswig-Holstein, and Frederick Francis III of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
Alexandrine was a member of the House of Hohenzollern.
She was a great-great-granddaughter of Queen Victoria.
Life

Alexandrine was born at the Kronprinzenpalais in Berlin.
She followed older brothers Wilhelm, Louis Ferdinand, Hubertus, and Frederick.
Alexandrine's only sister, Cecilie, was born in 1917.
It became clear shortly after Alexandrine's birth that she had Down syndrome.
Unlike other disabled royal children, Alexandrine was not hidden away.
As a teenager, Alexandrine attended the Trüpersche Sonderschule, a school dedicated to the education of children with special needs.
Alexandrine celebrated her confirmation along with her sister Cecilie in October 1934.
Alexandrine lived most of her later life in Bavaria, first in Pöcking and later near Lake Starnberg, where she was visited there regularly by her family, particularly her brother Louis Ferdinand.
Alexandrine died on 2 October 1980.
She was buried near her parents and brother Frederick at Hohenzollern Castle.



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
  AssignClass (b3c5449e-0371-41ed-b3cd-37a8befc03d5)
 Call ID: b3c5449e-0371-41ed-b3cd-37a8befc03d5
  Args:
    type: :Person
    source: Alexandrine
  AssignClass (dd0d8425-4f26-47c6-9392-b40da6fb32ab)
 Call ID: dd0d8425-4f26-47c6-9392-b40da6fb32ab
  Args:
    type: :Woman
    source: Alexandrine
  AddLiteral (9060a58a-5991-452b-95b8-a18f0e6b5efd)
 Call ID: 9060a58a-5991-452b-95b8-a18f0e6b5efd
  Args:
    source: Alexandrine
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1915
  AddLiteral (d74c11d4-d3a3-44c5-a447-23c9e6d28766)
 Call ID: d74c11d4-d3a3-44c5-a447-23c9e6d28766
  Args:
    literal_value: 1980
    relation: :hasDeathYear
    source: Alexandrine
    literal_type: xsd:integer
  AssignClass (4f39d76c-9cdf-4709-9dff-aee5bb494533)
 Call ID: 4f39d76c-9cdf-4709-9dff-aee5bb494533
  Args:
    type: :Person
    source: Wilhelm_German_Crown_Prince
  AssignClass (a93e7c91-d9f2-41bd-9e8a-cbd88d856a67)
 Call ID: a93e7c91-d9f2-41bd-9e8a-cbd88d856a67
  Args:
    type: :Man
    source: Wilhelm_German_Crown_Prince
  AssignClass (202a7e53-2dbd-4a75-a880-29408224866d)
 Call ID: 202a7e53-2dbd-4a75-a880-29408224866d
  Args:
    type: :Person
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (596c33e5-8011-465b-86bc-35a6d583f49d)
 Call ID: 596c33e5-8011-465b-86bc-35a6d583f49d
  Args:
    type: :Woman
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (dc2e365d-d139-4bc2-9137-494081ec6bcd)
 Call ID: dc2e365d-d139-4bc2-9137-494081ec6bcd
  Args:
    target: Wilhelm_German_Crown_Prince
    relation: :hasFather
    source: Alexandrine
  AddTriple (09e786a1-57c4-472e-98eb-23603978063a)
 Call ID: 09e786a1-57c4-472e-98eb-23603978063a
  Args:
    target: Cecilie_of_Mecklenburg-Schwerin
    relation: :hasMother
    source: Alexandrine
  AssignClass (20eb150a-62b0-4883-a4ad-015a15ccb2f2)
 Call ID: 20eb150a-62b0-4883-a4ad-015a15ccb2f2
  Args:
    type: :Person
    source: Wilhelm_II_German_Emperor
  AssignClass (276a86f1-69d2-4585-a2b4-428b23924d6e)
 Call ID: 276a86f1-69d2-4585-a2b4-428b23924d6e
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (da60610d-e156-43f5-a3e6-1e92d5cc1188)
 Call ID: da60610d-e156-43f5-a3e6-1e92d5cc1188
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (dfa21419-0035-484b-8a1d-2fe510938fb6)
 Call ID: dfa21419-0035-484b-8a1d-2fe510938fb6
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (39d99502-feff-442a-97d2-fbad3749f06c)
 Call ID: 39d99502-feff-442a-97d2-fbad3749f06c
  Args:
    type: :Person
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (2740cc5d-40b3-412e-b590-416f35991922)
 Call ID: 2740cc5d-40b3-412e-b590-416f35991922
  Args:
    type: :Man
    source: Frederick_Francis_III_of_Mecklenburg-Schwerin
  AssignClass (f13abc45-3a69-49f2-bee5-51ee7a02f4a3)
 Call ID: f13abc45-3a69-49f2-bee5-51ee7a02f4a3
  Args:
    type: :Person
    source: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AssignClass (77975503-9896-4f74-b775-e162eab1c056)
 Call ID: 77975503-9896-4f74-b775-e162eab1c056
  Args:
    type: :Woman
    source: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AddTriple (963a2baf-41dc-4b15-9344-fc0bb27a46d9)
 Call ID: 963a2baf-41dc-4b15-9344-fc0bb27a46d9
  Args:
    relation: :hasParent
    target: Wilhelm_II_German_Emperor
    source: Wilhelm_German_Crown_Prince
  AddTriple (4218291d-f646-412e-b019-f4bdeb6822a6)
 Call ID: 4218291d-f646-412e-b019-f4bdeb6822a6
  Args:
    source: Wilhelm_German_Crown_Prince
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasParent
  AddTriple (01639456-d926-4598-a4b7-0f61e15c02af)
 Call ID: 01639456-d926-4598-a4b7-0f61e15c02af
  Args:
    target: Frederick_Francis_III_of_Mecklenburg-Schwerin
    relation: :hasParent
    source: Cecilie_of_Mecklenburg-Schwerin
  AddTriple (6f941f43-b582-413b-b04b-72d04c9ab312)
 Call ID: 6f941f43-b582-413b-b04b-72d04c9ab312
  Args:
    relation: :hasParent
    target: Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    source: Cecilie_of_Mecklenburg-Schwerin
  AssignClass (87d484f7-76a7-4a8f-92a1-7d4fd52a6492)
 Call ID: 87d484f7-76a7-4a8f-92a1-7d4fd52a6492
  Args:
    type: :Person
    source: Wilhelm_brother
  AssignClass (f14b48f5-39cb-44d0-9056-5cbcd4e02fd5)
 Call ID: f14b48f5-39cb-44d0-9056-5cbcd4e02fd5
  Args:
    type: :Man
    source: Wilhelm_brother
  AssignClass (20d21eb4-8f8c-47ef-afb5-ae98a2ff05f6)
 Call ID: 20d21eb4-8f8c-47ef-afb5-ae98a2ff05f6
  Args:
    type: :Person
    source: Louis_Ferdinand
  AssignClass (46c8bfb5-e55e-47bd-88a2-044251cb9810)
 Call ID: 46c8bfb5-e55e-47bd-88a2-044251cb9810
  Args:
    type: :Man
    source: Louis_Ferdinand
  AssignClass (9c6329f8-a423-4ebe-9d19-f115457846d9)
 Call ID: 9c6329f8-a423-4ebe-9d19-f115457846d9
  Args:
    type: :Person
    source: Hubertus
  AssignClass (f5efafcf-17b9-4869-9fe8-441a97d08b1f)
 Call ID: f5efafcf-17b9-4869-9fe8-441a97d08b1f
  Args:
    type: :Man
    source: Hubertus
  AssignClass (8ad8eb8e-acd0-4dc9-bfce-b97c22c31c2e)
 Call ID: 8ad8eb8e-acd0-4dc9-bfce-b97c22c31c2e
  Args:
    type: :Person
    source: Frederick_brother
  AssignClass (3769409d-398d-4558-a6d0-14e8b9ab431d)
 Call ID: 3769409d-398d-4558-a6d0-14e8b9ab431d
  Args:
    type: :Man
    source: Frederick_brother
  AssignClass (b4777f71-2474-4685-8c5a-d25b59153043)
 Call ID: b4777f71-2474-4685-8c5a-d25b59153043
  Args:
    type: :Person
    source: Cecilie_sister
  AssignClass (ab218237-3df8-4816-82cd-d4449f0e7b7a)
 Call ID: ab218237-3df8-4816-82cd-d4449f0e7b7a
  Args:
    type: :Woman
    source: Cecilie_sister
  AddTriple (f9b64d8f-f877-4acf-ae0d-9709659542fc)
 Call ID: f9b64d8f-f877-4acf-ae0d-9709659542fc
  Args:
    source: Alexandrine
    relation: :hasBrother
    target: Wilhelm_brother
  AddTriple (d98a7749-118e-431b-b3f0-243ffde4ed26)
 Call ID: d98a7749-118e-431b-b3f0-243ffde4ed26
  Args:
    relation: :hasBrother
    target: Louis_Ferdinand
    source: Alexandrine
  AddTriple (ca452dee-ba96-4ab7-b3b9-68a3c2e7aa88)
 Call ID: ca452dee-ba96-4ab7-b3b9-68a3c2e7aa88
  Args:
    source: Alexandrine
    relation: :hasBrother
    target: Hubertus
  AddTriple (7af7e69f-97c9-4e25-b340-ff14e0132376)
 Call ID: 7af7e69f-97c9-4e25-b340-ff14e0132376
  Args:
    source: Alexandrine
    target: Frederick_brother
    relation: :hasBrother
  AddTriple (36b395ec-29bb-4c5e-a6fa-88bb77209ddb)
 Call ID: 36b395ec-29bb-4c5e-a6fa-88bb77209ddb
  Args:
    source: Alexandrine
    relation: :hasSister
    target: Cecilie_sister
  AssignClass (6c1dc857-79d7-4c84-8b7f-c11757dc4895)
 Call ID: 6c1dc857-79d7-4c84-8b7f-c11757dc4895
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (e45d54e8-afdd-4e8a-90ea-1407ac1a27ad)
 Call ID: e45d54e8-afdd-4e8a-90ea-1407ac1a27ad
  Args:
    type: :Woman
    source: Queen_Victoria
  AddTriple (01a0d5fa-cb6c-4650-8c0c-b6a91ed4a5d0)
 Call ID: 01a0d5fa-cb6c-4650-8c0c-b6a91ed4a5d0
  Args:
    source: Alexandrine
    target: Queen_Victoria
    relation: :hasAncestor
  Finish (8e94a841-6bc3-4eac-9a26-0895101ee252)
 Call ID: 8e94a841-6bc3-4eac-9a26-0895101ee252
  Args: