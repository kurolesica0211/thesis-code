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
Princess Maria di Grazia of Bourbon-Two Sicilies (12 August 1878 – 20 June 1973) was a Princess of Bourbon-Two Sicilies by birth as well as Princess Imperial of Brazil and Princess of Orleans-Braganza through her marriage to Prince Luiz of Orléans-Braganza, secondborn son and pretense heir of Isabel, Princess Imperial of Brazil.
Early life and family

Princess Maria was born at their parents' Villa Maria Teresa in Cannes, where her family had been exiled since the 1861 due to the Italian Unification.
She was the sixth child and third daughter of Prince Alfonso, Count of Caserta and his wife Princess Antonietta of Bourbon-Two Sicilies.
She was usually called “Maria Pia”.
Her father, the third son of King Ferdinand II of the Two Sicilies, became Head of the Royal House of the Two Sicilies with the death of his elder brother, King Francis II, in 1894.
Maria di Grazia was baptized and had Robert I, Duke of Parma, and his first wife, Princess Maria Pia of the Two Sicilies, as godparents.
Maria di Grazia and her sisters were educated at the College of the Sacred Heart of Aix-Provence, an institution run by nuns near Cannes.
There, Maria di Grazia spent her childhood and, after finishing her studies, her youth.
In one of the visits of the Emperor Pedro II of Brazil to Cannes, he visited the Villa Maria Teresa.
The Count of Caserta gathered all his children to present them to the monarch, and Maria di Grazia, at the age of ten, had to play "Turkish March" by Mozart, on the piano.
Upon turning 18, Maria di Grazia was taken with her sisters to be presented to the court of Emperor Franz Joseph I of Austria.
After Austria, the princesses were taken to Munich, where they were given a gala lunch by Luitpold, Prince Regent of Bavaria.
Marriage and issue

Princess Maria di Grazia met her future fiancé when they were still young, when Luiz eventually arrived in Europe due to the exile imposed by the proclamation of the republic in Brazil in 1889.
They later reconnected in 1903 when Prince Luiz, then serving in the Austrian Army, was visiting several relatives in France.
On 4 November 1908 Princess Maria di Grazia married Prince Luiz Maria of Orléans-Braganza, son of Prince Gaston of Orléans, Count of Eu and Isabel, Princess Imperial of Brazil, in Cannes.
Later life

Prince Luiz died in 1920 leaving Maria a widow for the remainder of her life.
In 1922, Maria accompanied the Brazilian Imperial Family to Brazil for the country's centennial celebrations of its independence.
During the course of the trip, the Count of Eu died while recumbent upon her shoulder.
After that, Princess Maria preferred to live with her children in France, where they could have a better education.
}} Media related to Princess Maria di Grazia of the Two Sicilies at Wikimedia Commons



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
  AssignClass (b2159f00-b994-4b42-81fb-15e56b9fc410)
 Call ID: b2159f00-b994-4b42-81fb-15e56b9fc410
  Args:
    type: :Woman
    source: Maria_di_Grazia
  AssignClass (353ced2a-719c-4e34-aed3-0590d3fc3adf)
 Call ID: 353ced2a-719c-4e34-aed3-0590d3fc3adf
  Args:
    source: Maria_di_Grazia
    type: :Person
  AddLiteral (9771e86f-5273-4608-85ce-9c64a44617ff)
 Call ID: 9771e86f-5273-4608-85ce-9c64a44617ff
  Args:
    source: Maria_di_Grazia
    literal_type: xsd:string
    literal_value: Maria Pia
    relation: :knownAs
  AddLiteral (284d309f-1f32-4714-ac73-41ec5314a8b2)
 Call ID: 284d309f-1f32-4714-ac73-41ec5314a8b2
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1878
    source: Maria_di_Grazia
  AddLiteral (aaabc1c5-526d-4e85-9018-dd246a510330)
 Call ID: aaabc1c5-526d-4e85-9018-dd246a510330
  Args:
    source: Maria_di_Grazia
    literal_type: xsd:integer
    literal_value: 1973
    relation: :hasDeathYear
  AssignClass (9d796e70-f244-455a-a5e4-90512f0fe2ca)
 Call ID: 9d796e70-f244-455a-a5e4-90512f0fe2ca
  Args:
    type: :Man
    source: Alfonso_Count_of_Caserta
  AssignClass (fd2d3e5d-b9a0-49be-96e1-f5d735cf64d4)
 Call ID: fd2d3e5d-b9a0-49be-96e1-f5d735cf64d4
  Args:
    source: Alfonso_Count_of_Caserta
    type: :Person
  AssignClass (20502a9e-6d95-422e-bea1-e571eddf7873)
 Call ID: 20502a9e-6d95-422e-bea1-e571eddf7873
  Args:
    type: :Woman
    source: Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (4bd68c15-db05-4251-966b-7f7e4b39e20b)
 Call ID: 4bd68c15-db05-4251-966b-7f7e4b39e20b
  Args:
    source: Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (8db988df-3b99-4780-ac5e-de26075de2eb)
 Call ID: 8db988df-3b99-4780-ac5e-de26075de2eb
  Args:
    source: Maria_di_Grazia
    target: Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (87ff07ce-dcc5-4e90-bd6a-873c6814d8b8)
 Call ID: 87ff07ce-dcc5-4e90-bd6a-873c6814d8b8
  Args:
    relation: :hasMother
    source: Maria_di_Grazia
    target: Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (2d61580d-6ca3-4e6f-bf3c-c110921e14d8)
 Call ID: 2d61580d-6ca3-4e6f-bf3c-c110921e14d8
  Args:
    source: Luiz_Maria_of_Orléans-Braganza
    type: :Man
  AssignClass (90f61adb-6c50-4953-9c6b-9b6749045410)
 Call ID: 90f61adb-6c50-4953-9c6b-9b6749045410
  Args:
    source: Luiz_Maria_of_Orléans-Braganza
    type: :Person
  AddTriple (6bb725f0-614a-4fd0-b5a4-df93f6682f46)
 Call ID: 6bb725f0-614a-4fd0-b5a4-df93f6682f46
  Args:
    source: Maria_di_Grazia
    target: Luiz_Maria_of_Orléans-Braganza
    relation: :hasRelation
  AddLiteral (5356337f-4c2b-4cbe-bde2-42b743ab9cfd)
 Call ID: 5356337f-4c2b-4cbe-bde2-42b743ab9cfd
  Args:
    relation: :hasMarriageYear
    literal_value: 1908
    literal_type: xsd:integer
    source: Maria_di_Grazia
  AssignClass (871a508d-cb4a-4012-b6e3-f55198d7aa48)
 Call ID: 871a508d-cb4a-4012-b6e3-f55198d7aa48
  Args:
    type: :Man
    source: Gaston_of_Orléans_Count_of_Eu
  AssignClass (753468da-a13e-4cfb-855a-1b0ef7ebcd73)
 Call ID: 753468da-a13e-4cfb-855a-1b0ef7ebcd73
  Args:
    type: :Person
    source: Gaston_of_Orléans_Count_of_Eu
  AssignClass (26a7bb8f-7a10-4051-afcf-f3620ce125b9)
 Call ID: 26a7bb8f-7a10-4051-afcf-f3620ce125b9
  Args:
    type: :Woman
    source: Isabel_Princess_Imperial_of_Brazil
  AssignClass (20bb4a32-725e-4a12-aabc-59264d18c818)
 Call ID: 20bb4a32-725e-4a12-aabc-59264d18c818
  Args:
    source: Isabel_Princess_Imperial_of_Brazil
    type: :Person
  AddTriple (5f9c5e6f-5d36-4397-9adf-a97ddeaf0ec9)
 Call ID: 5f9c5e6f-5d36-4397-9adf-a97ddeaf0ec9
  Args:
    relation: :hasFather
    target: Gaston_of_Orléans_Count_of_Eu
    source: Luiz_Maria_of_Orléans-Braganza
  AddTriple (3df13666-2af6-4ef6-95d0-2371cbf18ec8)
 Call ID: 3df13666-2af6-4ef6-95d0-2371cbf18ec8
  Args:
    relation: :hasMother
    source: Luiz_Maria_of_Orléans-Braganza
    target: Isabel_Princess_Imperial_of_Brazil
  AssignClass (ce6b5708-75a9-403a-8612-cc97ae8dba07)
 Call ID: ce6b5708-75a9-403a-8612-cc97ae8dba07
  Args:
    source: Ferdinand_II_of_the_Two_Sicilies
    type: :Man
  AssignClass (4d3fa389-6c0f-42d3-aef1-6b1c98f00bd9)
 Call ID: 4d3fa389-6c0f-42d3-aef1-6b1c98f00bd9
  Args:
    type: :Person
    source: Ferdinand_II_of_the_Two_Sicilies
  AddTriple (1ef1738f-6820-4ed7-a431-1f4cfb89e42a)
 Call ID: 1ef1738f-6820-4ed7-a431-1f4cfb89e42a
  Args:
    relation: :hasFather
    source: Alfonso_Count_of_Caserta
    target: Ferdinand_II_of_the_Two_Sicilies
  AssignClass (2a24c82b-52e7-4f2f-97d0-21d0ebde6664)
 Call ID: 2a24c82b-52e7-4f2f-97d0-21d0ebde6664
  Args:
    type: :Man
    source: Francis_II_of_the_Two_Sicilies
  AssignClass (b393c9b5-a1b3-4a45-bd89-c37d43761c06)
 Call ID: b393c9b5-a1b3-4a45-bd89-c37d43761c06
  Args:
    type: :Person
    source: Francis_II_of_the_Two_Sicilies
  AddTriple (76608c7a-39b8-4645-a0f1-2c83abbd4052)
 Call ID: 76608c7a-39b8-4645-a0f1-2c83abbd4052
  Args:
    relation: :hasBrother
    source: Alfonso_Count_of_Caserta
    target: Francis_II_of_the_Two_Sicilies
  Finish (e66ae371-3c7d-48a5-bb09-1278664320dc)
 Call ID: e66ae371-3c7d-48a5-bb09-1278664320dc
  Args: