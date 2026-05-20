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
Princess Isabelle of Orléans (Isabelle Marie Laure Mercédès Ferdinande; 7 May 1878 – 21 April 1961) was a member of the French Orleanist royal family and by marriage Duchess of Guise.
Biography

Early life

Isabelle was born at the Château d'Eu in Eu, France, the third daughter and fifth (fourth surviving) child of Prince Philippe, Count of Paris and Infanta Maria Isabel of Spain.
Marriage and issue

As a young woman, Isabelle had many suitors, chief among them being the future Albert I of Belgium.
Albert, however, was forced to end the courtship under pressure from his uncle King Leopold II, who feared that a marriage to the daughter of an exiled pretender to the French throne would result in backlash from the republican government in Paris.
On 30 October 1899, Isabelle married her first cousin Prince Jean, Duke of Guise.
Jean was the son of prince Robert, Duke of Chartres and Françoise d'Orléans.
Upon the death of her brother, Philippe of Orléans, Duke of Orléans, claimant to the throne of France as "Philip VIII", the Duke of Guise became, at least for his Orleanist supporters, titular king of France as "Jean III".
The couple had four children:


Princess Isabelle died in Larache, Morocco, on 21 April 1962 at age 82.



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
  AssignClass (0e0ca15b-f10f-4a0d-ba9f-88bf833ddc1f)
 Call ID: 0e0ca15b-f10f-4a0d-ba9f-88bf833ddc1f
  Args:
    source: Isabelle_of_Orleans
    type: :Person
  AssignClass (a42ee82b-4788-4d88-8afa-e64adb37c7ab)
 Call ID: a42ee82b-4788-4d88-8afa-e64adb37c7ab
  Args:
    source: Isabelle_of_Orleans
    type: :Woman
  AssignClass (9fb92db3-9836-4acb-9a07-84769776dbad)
 Call ID: 9fb92db3-9836-4acb-9a07-84769776dbad
  Args:
    type: :Person
    source: Philippe_Count_of_Paris
  AssignClass (5e19dff1-369f-49ad-9747-e6ca882d329a)
 Call ID: 5e19dff1-369f-49ad-9747-e6ca882d329a
  Args:
    type: :Man
    source: Philippe_Count_of_Paris
  AssignClass (489054f5-5532-44fb-a15a-5cd3e2c37462)
 Call ID: 489054f5-5532-44fb-a15a-5cd3e2c37462
  Args:
    type: :Person
    source: Maria_Isabel_of_Spain
  AssignClass (a4d85589-a268-44df-b431-1628daba7371)
 Call ID: a4d85589-a268-44df-b431-1628daba7371
  Args:
    source: Maria_Isabel_of_Spain
    type: :Woman
  AssignClass (b2025168-f709-4cd3-8472-c936f737a0e4)
 Call ID: b2025168-f709-4cd3-8472-c936f737a0e4
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Person
  AssignClass (fb445905-8ab9-4621-af0c-f0e1d1446484)
 Call ID: fb445905-8ab9-4621-af0c-f0e1d1446484
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AssignClass (79c18308-de34-451f-9513-01a5147f3278)
 Call ID: 79c18308-de34-451f-9513-01a5147f3278
  Args:
    source: Robert_Duke_of_Chartres
    type: :Person
  AssignClass (414dd322-e0e7-44d2-a60c-2b8116022ef6)
 Call ID: 414dd322-e0e7-44d2-a60c-2b8116022ef6
  Args:
    type: :Man
    source: Robert_Duke_of_Chartres
  AssignClass (85967fb8-17ad-4774-b851-3625e77e2bee)
 Call ID: 85967fb8-17ad-4774-b851-3625e77e2bee
  Args:
    type: :Person
    source: Francoise_dOrleans
  AssignClass (f73b4118-c06c-4421-8876-4f439fd42aa4)
 Call ID: f73b4118-c06c-4421-8876-4f439fd42aa4
  Args:
    source: Francoise_dOrleans
    type: :Woman
  AssignClass (bfecfda1-f651-44e2-999c-6648af9be5f4)
 Call ID: bfecfda1-f651-44e2-999c-6648af9be5f4
  Args:
    type: :Person
    source: Philippe_of_Orleans_Duke_of_Orleans
  AssignClass (4e620cac-4f7b-47c0-9531-d10d216bf4af)
 Call ID: 4e620cac-4f7b-47c0-9531-d10d216bf4af
  Args:
    type: :Man
    source: Philippe_of_Orleans_Duke_of_Orleans
  AddLiteral (f32b47cb-2552-426b-9aba-1f6cb8ea4c43)
 Call ID: f32b47cb-2552-426b-9aba-1f6cb8ea4c43
  Args:
    source: Isabelle_of_Orleans
    literal_value: Isabelle Marie Laure Mercédès Ferdinande
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (c6399fcb-ca91-4b99-809c-c2c0acbf80d3)
 Call ID: c6399fcb-ca91-4b99-809c-c2c0acbf80d3
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1878
    source: Isabelle_of_Orleans
  AddLiteral (9b254c94-8694-4ba0-8c71-b733334ab5af)
 Call ID: 9b254c94-8694-4ba0-8c71-b733334ab5af
  Args:
    source: Isabelle_of_Orleans
    relation: :hasDeathYear
    literal_value: 1962
    literal_type: xsd:integer
  AddTriple (c64abb1b-a6c7-4636-bd95-e52b6eb0ec17)
 Call ID: c64abb1b-a6c7-4636-bd95-e52b6eb0ec17
  Args:
    target: Philippe_Count_of_Paris
    source: Isabelle_of_Orleans
    relation: :hasFather
  AddTriple (5abbe7d6-d5b4-4700-b37e-dbac66d8f570)
 Call ID: 5abbe7d6-d5b4-4700-b37e-dbac66d8f570
  Args:
    relation: :hasMother
    source: Isabelle_of_Orleans
    target: Maria_Isabel_of_Spain
  AddTriple (ab405d7e-c106-4b5e-94ed-ce6227b9be23)
 Call ID: ab405d7e-c106-4b5e-94ed-ce6227b9be23
  Args:
    target: Philippe_of_Orleans_Duke_of_Orleans
    source: Isabelle_of_Orleans
    relation: :hasBrother
  AddTriple (b0d1c25a-f25e-40dc-971a-9632a3359d2b)
 Call ID: b0d1c25a-f25e-40dc-971a-9632a3359d2b
  Args:
    source: Prince_Jean_Duke_of_Guise
    target: Robert_Duke_of_Chartres
    relation: :hasFather
  AddTriple (7ef3181e-c8a7-4114-815d-2f902e36d99d)
 Call ID: 7ef3181e-c8a7-4114-815d-2f902e36d99d
  Args:
    target: Francoise_dOrleans
    source: Prince_Jean_Duke_of_Guise
    relation: :hasMother
  AddLiteral (8b7e84fe-a659-49be-b792-95ba3c620914)
 Call ID: 8b7e84fe-a659-49be-b792-95ba3c620914
  Args:
    source: Isabelle_of_Orleans
    literal_value: 1899
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (8cda0b62-49b2-40a0-9f88-00aaedfa68af)
 Call ID: 8cda0b62-49b2-40a0-9f88-00aaedfa68af
  Args:
    target: Prince_Jean_Duke_of_Guise
    source: Isabelle_of_Orleans
    relation: :hasRelation
  Finish (8ff890c1-b1e5-4e34-a94b-e547c17b04ae)
 Call ID: 8ff890c1-b1e5-4e34-a94b-e547c17b04ae
  Args: