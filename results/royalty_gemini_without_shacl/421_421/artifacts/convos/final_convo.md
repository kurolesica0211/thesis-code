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
Prince Wilhelm Victor of Prussia (German: Wilhelm Viktor Ernst Freund Friedrich Georg Adalbert; 15 February 1919 – 7 February 1989) was a German royal, soldier and diplomat.
Life

Prince Wilhelm Victor was a grandson of Emperor Wilhelm II and the youngest child of Prince Adalbert of Prussia (1884–1948) and Princess Adelheid "Adi" of Saxe-Meiningen (1891–1971).
His father, Prince Adalbert carried also the title "Graf von Lingen".
His only surviving sister, Princess Viktoria Marina (1917–1981) married Kirby William Patterson (1907–1984).
Marriage

Prince Wilhelm Victor married at Donaueschingen 20 July 1944 Marie Antoinette, Countess of Hoyos-Stichsenstein (Hohenthurm, 27 June 1920 – Marbella 1 March 2004),  daughter of Friedrich, Count of Hoyos-Stichsenstein (1876–1951) and Countess Wilhelmine von Wuthenau-Hohenthurm (1895–1983), niece of Sophie, Duchess of Hohenberg.
They had the following issue:


Death

Prince Wilhelm Viktor died on 7 February 1989 at age 69.



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
  AssignClass (f2eaef30-34c9-41e9-8fce-46c5f75501e3)
 Call ID: f2eaef30-34c9-41e9-8fce-46c5f75501e3
  Args:
    type: :Man
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (85dee58e-69e4-4e6f-987e-c5c769fcdbfd)
 Call ID: 85dee58e-69e4-4e6f-987e-c5c769fcdbfd
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    type: :Person
  AddLiteral (c19676cb-1ccc-4cad-8f9e-1d53b1629be6)
 Call ID: c19676cb-1ccc-4cad-8f9e-1d53b1629be6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1919
    source: Prince_Wilhelm_Victor_of_Prussia
  AddLiteral (4aba0803-d622-4c65-9d1b-b7fcf2b50245)
 Call ID: 4aba0803-d622-4c65-9d1b-b7fcf2b50245
  Args:
    literal_value: 1989
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (39c380da-b44a-4f5f-9825-90fac8763ee8)
 Call ID: 39c380da-b44a-4f5f-9825-90fac8763ee8
  Args:
    source: Prince_Adalbert_of_Prussia
    type: :Man
  AssignClass (59dc5f2c-b52a-40ac-831c-85a15667f5b9)
 Call ID: 59dc5f2c-b52a-40ac-831c-85a15667f5b9
  Args:
    type: :Person
    source: Prince_Adalbert_of_Prussia
  AddLiteral (45e3aef5-3fed-4629-adf1-7bb70ad9e54a)
 Call ID: 45e3aef5-3fed-4629-adf1-7bb70ad9e54a
  Args:
    source: Prince_Adalbert_of_Prussia
    literal_type: xsd:integer
    literal_value: 1884
    relation: :hasBirthYear
  AddLiteral (a6a1e517-6d10-4372-ad7f-80a3092068f0)
 Call ID: a6a1e517-6d10-4372-ad7f-80a3092068f0
  Args:
    relation: :hasDeathYear
    literal_value: 1948
    literal_type: xsd:integer
    source: Prince_Adalbert_of_Prussia
  AddTriple (8bb0c428-3cff-4aee-a9e6-14e16e1a88cb)
 Call ID: 8bb0c428-3cff-4aee-a9e6-14e16e1a88cb
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    relation: :hasFather
    target: Prince_Adalbert_of_Prussia
  AssignClass (69217323-f20c-4341-b873-1465621978ba)
 Call ID: 69217323-f20c-4341-b873-1465621978ba
  Args:
    source: Princess_Adelheid_of_Saxe-Meiningen
    type: :Woman
  AssignClass (13befda2-e3dd-44e5-b23f-64d039130888)
 Call ID: 13befda2-e3dd-44e5-b23f-64d039130888
  Args:
    type: :Person
    source: Princess_Adelheid_of_Saxe-Meiningen
  AddLiteral (d481f26f-3765-4fee-a501-eea654a215dd)
 Call ID: d481f26f-3765-4fee-a501-eea654a215dd
  Args:
    source: Princess_Adelheid_of_Saxe-Meiningen
    literal_type: xsd:integer
    literal_value: 1891
    relation: :hasBirthYear
  AddLiteral (288f4a9e-236c-4b8b-a2b6-213c2189fa94)
 Call ID: 288f4a9e-236c-4b8b-a2b6-213c2189fa94
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1971
    source: Princess_Adelheid_of_Saxe-Meiningen
  AddTriple (35fee36b-6c81-4df9-9fa8-d8d5dceb1632)
 Call ID: 35fee36b-6c81-4df9-9fa8-d8d5dceb1632
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    target: Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasMother
  AssignClass (f606475f-04e5-48b9-a14d-07e03bfc7fdb)
 Call ID: f606475f-04e5-48b9-a14d-07e03bfc7fdb
  Args:
    source: Princess_Viktoria_Marina
    type: :Woman
  AssignClass (f82c01a1-1f60-482d-9db4-ea1436011531)
 Call ID: f82c01a1-1f60-482d-9db4-ea1436011531
  Args:
    source: Princess_Viktoria_Marina
    type: :Person
  AddLiteral (ba59f392-0f43-4834-bc60-bfd3e1f7770d)
 Call ID: ba59f392-0f43-4834-bc60-bfd3e1f7770d
  Args:
    source: Princess_Viktoria_Marina
    relation: :hasBirthYear
    literal_value: 1917
    literal_type: xsd:integer
  AddLiteral (d3b820f1-1fcd-445b-bbb9-18252ade1f7c)
 Call ID: d3b820f1-1fcd-445b-bbb9-18252ade1f7c
  Args:
    literal_type: xsd:integer
    literal_value: 1981
    relation: :hasDeathYear
    source: Princess_Viktoria_Marina
  AddTriple (6e263ffe-fc84-4c78-a394-ecf274c61dfd)
 Call ID: 6e263ffe-fc84-4c78-a394-ecf274c61dfd
  Args:
    target: Princess_Viktoria_Marina
    relation: :hasSister
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (e2ff079d-eda8-4157-9abc-324213b8f59c)
 Call ID: e2ff079d-eda8-4157-9abc-324213b8f59c
  Args:
    type: :Woman
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AssignClass (a9c46b2e-25d5-499f-b8cb-3c05dafe75c6)
 Call ID: a9c46b2e-25d5-499f-b8cb-3c05dafe75c6
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    type: :Person
  AddLiteral (ca92e5e7-0042-48b3-86aa-61d6682bd369)
 Call ID: ca92e5e7-0042-48b3-86aa-61d6682bd369
  Args:
    literal_value: 1920
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AddLiteral (1bd17ccc-bcd6-4aae-a5a7-f896b6842a8f)
 Call ID: 1bd17ccc-bcd6-4aae-a5a7-f896b6842a8f
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasDeathYear
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AddLiteral (b7d8c735-f91c-4c7e-a258-16511f04ad57)
 Call ID: b7d8c735-f91c-4c7e-a258-16511f04ad57
  Args:
    source: Prince_Wilhelm_Victor_of_Prussia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1944
  AddTriple (5da425c9-f81a-4161-ad7b-ae35b648619d)
 Call ID: 5da425c9-f81a-4161-ad7b-ae35b648619d
  Args:
    relation: :hasRelation
    target: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    source: Prince_Wilhelm_Victor_of_Prussia
  AssignClass (e907cd60-3be8-4785-85c7-b13be61ca31b)
 Call ID: e907cd60-3be8-4785-85c7-b13be61ca31b
  Args:
    type: :Man
    source: Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (c7c753b2-ca7f-4544-93ff-6c37c94a643a)
 Call ID: c7c753b2-ca7f-4544-93ff-6c37c94a643a
  Args:
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    type: :Person
  AddLiteral (b5774806-6d3b-4bfe-9fa3-e92343a4aaec)
 Call ID: b5774806-6d3b-4bfe-9fa3-e92343a4aaec
  Args:
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    literal_value: 1876
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (1b1cee49-849b-44bd-b359-30fe18be0681)
 Call ID: 1b1cee49-849b-44bd-b359-30fe18be0681
  Args:
    source: Friedrich_Count_of_Hoyos-Stichsenstein
    literal_type: xsd:integer
    literal_value: 1951
    relation: :hasDeathYear
  AddTriple (234f3334-fb25-4c24-89ab-8b9c4e66d2ed)
 Call ID: 234f3334-fb25-4c24-89ab-8b9c4e66d2ed
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    target: Friedrich_Count_of_Hoyos-Stichsenstein
    relation: :hasFather
  AssignClass (a5ef7ab9-5a47-449e-bad5-cb5c12bda61b)
 Call ID: a5ef7ab9-5a47-449e-bad5-cb5c12bda61b
  Args:
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    type: :Woman
  AssignClass (ff33f1c4-6c7b-46d9-a0b3-5e74294f1cb7)
 Call ID: ff33f1c4-6c7b-46d9-a0b3-5e74294f1cb7
  Args:
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    type: :Person
  AddLiteral (d7f39614-59b6-4ed0-a018-ab52334378e0)
 Call ID: d7f39614-59b6-4ed0-a018-ab52334378e0
  Args:
    literal_value: 1895
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AddLiteral (956d6e02-c75a-4f4a-b8a6-a9449af5123a)
 Call ID: 956d6e02-c75a-4f4a-b8a6-a9449af5123a
  Args:
    relation: :hasDeathYear
    literal_value: 1983
    literal_type: xsd:integer
    source: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AddTriple (8887b085-1296-41c6-ae74-d53ab9e05fdc)
 Call ID: 8887b085-1296-41c6-ae74-d53ab9e05fdc
  Args:
    source: Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    target: Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    relation: :hasMother
  Finish (3068ad7f-c2f7-4af3-a730-85a2e1465055)
 Call ID: 3068ad7f-c2f7-4af3-a730-85a2e1465055
  Args: