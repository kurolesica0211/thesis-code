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
Princess Marie Louise of Hanover and Cumberland (11 October 1879 – 31 January 1948) was the eldest child of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark, the youngest daughter of Christian IX of Denmark and Louise of Hesse-Kassel.
Through her father, Marie Louise was a great-great-granddaughter of George III of the United Kingdom and Charlotte of Mecklenburg-Strelitz.
Marriage and children

Marie Louise married Prince Maximilian of Baden (1867–1929), her third cousin twice removed, on 10 July 1900 in Gmunden, Austria-Hungary.
He was the son of Prince Wilhelm of Baden and Princess Maria Maximilianovna of Leuchtenberg and became a first cousin twice removed of Napoleon III of France.
Marie Louise and Maximilian had one daughter and one son:


Ancestry

References

External links



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
  AssignClass (16ef3f4e-9d5a-4898-9695-8ca5e77bfca0)
 Call ID: 16ef3f4e-9d5a-4898-9695-8ca5e77bfca0
  Args:
    source: :Marie_Louise_of_Hanover_and_Cumberland
    type: :Woman
  AssignClass (1e335ff4-aeb7-46c0-af90-a22ff59ff5b4)
 Call ID: 1e335ff4-aeb7-46c0-af90-a22ff59ff5b4
  Args:
    source: :Marie_Louise_of_Hanover_and_Cumberland
    type: :Person
  AddLiteral (43c6e0d5-da29-413f-90ec-d23ce904a2f5)
 Call ID: 43c6e0d5-da29-413f-90ec-d23ce904a2f5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_value: 1879
  AddLiteral (4d386661-3d96-44f8-bdea-373372fa99a7)
 Call ID: 4d386661-3d96-44f8-bdea-373372fa99a7
  Args:
    literal_value: 1948
    relation: :hasDeathYear
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
  AssignClass (844f1213-dbe6-469c-8514-ca6f1d43faa2)
 Call ID: 844f1213-dbe6-469c-8514-ca6f1d43faa2
  Args:
    type: :Man
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (36f3c9b1-0390-4b75-b1d2-6e7710647bc8)
 Call ID: 36f3c9b1-0390-4b75-b1d2-6e7710647bc8
  Args:
    type: :Person
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (ce2c85c0-e1a1-4919-8125-310cc83d143f)
 Call ID: ce2c85c0-e1a1-4919-8125-310cc83d143f
  Args:
    type: :Woman
    source: :Princess_Thyra_of_Denmark
  AssignClass (54238f1e-5268-4e46-b45c-b25126f2fa83)
 Call ID: 54238f1e-5268-4e46-b45c-b25126f2fa83
  Args:
    source: :Princess_Thyra_of_Denmark
    type: :Person
  AddTriple (d5b8e2b5-68c3-49f3-a494-4e0068fd7623)
 Call ID: d5b8e2b5-68c3-49f3-a494-4e0068fd7623
  Args:
    relation: :hasFather
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (e3e17a1a-adf0-4f3a-aefb-edc0a96f30bf)
 Call ID: e3e17a1a-adf0-4f3a-aefb-edc0a96f30bf
  Args:
    target: :Princess_Thyra_of_Denmark
    relation: :hasMother
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (d5069642-c440-431f-a5e6-0ff54cc43ef5)
 Call ID: d5069642-c440-431f-a5e6-0ff54cc43ef5
  Args:
    source: :Christian_IX_of_Denmark
    type: :Man
  AssignClass (e44ea899-d9ca-4d72-aab7-afb1d1a4e861)
 Call ID: e44ea899-d9ca-4d72-aab7-afb1d1a4e861
  Args:
    type: :Person
    source: :Christian_IX_of_Denmark
  AssignClass (8229d16d-c8aa-481f-960f-1c204c291d8d)
 Call ID: 8229d16d-c8aa-481f-960f-1c204c291d8d
  Args:
    source: :Louise_of_Hesse_Kassel
    type: :Woman
  AssignClass (43661af0-733d-4c02-894c-597b2ed7a2be)
 Call ID: 43661af0-733d-4c02-894c-597b2ed7a2be
  Args:
    source: :Louise_of_Hesse_Kassel
    type: :Person
  AddTriple (3f051d03-27c1-41d5-87df-19e8a2175ec2)
 Call ID: 3f051d03-27c1-41d5-87df-19e8a2175ec2
  Args:
    target: :Christian_IX_of_Denmark
    source: :Princess_Thyra_of_Denmark
    relation: :hasFather
  AddTriple (52e2acca-553e-49d1-9b98-cf3789ea873b)
 Call ID: 52e2acca-553e-49d1-9b98-cf3789ea873b
  Args:
    target: :Louise_of_Hesse_Kassel
    source: :Princess_Thyra_of_Denmark
    relation: :hasMother
  AssignClass (a15123f4-9c3a-4cbd-ad5a-224ed34c88ce)
 Call ID: a15123f4-9c3a-4cbd-ad5a-224ed34c88ce
  Args:
    source: :George_III_of_the_United_Kingdom
    type: :Man
  AssignClass (67490008-c7f7-4c97-bd9d-90b3ecadb033)
 Call ID: 67490008-c7f7-4c97-bd9d-90b3ecadb033
  Args:
    source: :George_III_of_the_United_Kingdom
    type: :Person
  AssignClass (86c937f9-4811-40fb-96dc-194e8f4c5e26)
 Call ID: 86c937f9-4811-40fb-96dc-194e8f4c5e26
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    type: :Woman
  AssignClass (c70d6e2e-cb82-435c-bb90-20a0f99bce00)
 Call ID: c70d6e2e-cb82-435c-bb90-20a0f99bce00
  Args:
    source: :Charlotte_of_Mecklenburg_Strelitz
    type: :Person
  AddTriple (6f7c1b6d-5e0f-42d2-948f-481642d6d8ad)
 Call ID: 6f7c1b6d-5e0f-42d2-948f-481642d6d8ad
  Args:
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasAncestor
    target: :George_III_of_the_United_Kingdom
  AddTriple (5e2b060c-299c-40ca-af11-a63f5b59a5c9)
 Call ID: 5e2b060c-299c-40ca-af11-a63f5b59a5c9
  Args:
    target: :Charlotte_of_Mecklenburg_Strelitz
    relation: :hasAncestor
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (f4c510cd-42ab-4896-a1ee-4a5ae30a9174)
 Call ID: f4c510cd-42ab-4896-a1ee-4a5ae30a9174
  Args:
    type: :Man
    source: :Maximilian_of_Baden
  AssignClass (9b0fb565-9685-4d17-883a-83dae2af5a36)
 Call ID: 9b0fb565-9685-4d17-883a-83dae2af5a36
  Args:
    source: :Maximilian_of_Baden
    type: :Person
  AddLiteral (3a07ea05-b863-4bba-a539-48acd82e5e17)
 Call ID: 3a07ea05-b863-4bba-a539-48acd82e5e17
  Args:
    literal_value: 1867
    source: :Maximilian_of_Baden
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (85ff6bad-5f72-43ad-9a74-a925fa858784)
 Call ID: 85ff6bad-5f72-43ad-9a74-a925fa858784
  Args:
    literal_value: 1929
    source: :Maximilian_of_Baden
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (84ec127b-7a00-409b-a20b-d1d74c9b19c7)
 Call ID: 84ec127b-7a00-409b-a20b-d1d74c9b19c7
  Args:
    literal_value: 1900
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AddTriple (a1d3a046-fbe6-4ef5-b189-c512c7f15485)
 Call ID: a1d3a046-fbe6-4ef5-b189-c512c7f15485
  Args:
    target: :Maximilian_of_Baden
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasRelation
  AssignClass (54907aeb-3cd0-4d4a-aff9-f5c15a6caed6)
 Call ID: 54907aeb-3cd0-4d4a-aff9-f5c15a6caed6
  Args:
    type: :Man
    source: :Wilhelm_of_Baden
  AssignClass (443bee88-2fb8-49fd-9273-a186c2de735c)
 Call ID: 443bee88-2fb8-49fd-9273-a186c2de735c
  Args:
    source: :Wilhelm_of_Baden
    type: :Person
  AssignClass (80167f0a-77ac-4d50-a619-9a71c12fa391)
 Call ID: 80167f0a-77ac-4d50-a619-9a71c12fa391
  Args:
    source: :Maria_Maximilianovna_of_Leuchtenberg
    type: :Woman
  AssignClass (23874983-3d3a-47d8-a375-94a55e05ed91)
 Call ID: 23874983-3d3a-47d8-a375-94a55e05ed91
  Args:
    type: :Person
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (d610ec8c-f143-4730-9618-3705148110f0)
 Call ID: d610ec8c-f143-4730-9618-3705148110f0
  Args:
    relation: :hasFather
    source: :Maximilian_of_Baden
    target: :Wilhelm_of_Baden
  AddTriple (41d17536-df1a-4a7e-be42-0d7643934043)
 Call ID: 41d17536-df1a-4a7e-be42-0d7643934043
  Args:
    source: :Maximilian_of_Baden
    relation: :hasMother
    target: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (94b14e02-b0ab-43e7-b88b-e32371c9013f)
 Call ID: 94b14e02-b0ab-43e7-b88b-e32371c9013f
  Args:
    source: :Napoleon_III_of_France
    type: :Man
  AssignClass (92265c72-7f66-489b-b275-c980e435f649)
 Call ID: 92265c72-7f66-489b-b275-c980e435f649
  Args:
    type: :Person
    source: :Napoleon_III_of_France
  AddTriple (b24565ba-c242-40cc-b020-a528fd533e2e)
 Call ID: b24565ba-c242-40cc-b020-a528fd533e2e
  Args:
    target: :Napoleon_III_of_France
    relation: :hasRelation
    source: :Maximilian_of_Baden
  Finish (9059b59f-8eab-4661-b7b6-a6bd1a21cb36)
 Call ID: 9059b59f-8eab-4661-b7b6-a6bd1a21cb36
  Args: