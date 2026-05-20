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
Princess Urraca of Bourbon-Two Sicilies (Italian: Urraca Maria Isabella Carolina Aldegonda Carmela, Principessa di Borbone delle
Due Sicilie; 14 July 1913, Nymphenburg Palace, Munich, Kingdom of Bavaria – 3 May 1999, Sigmaringen, Baden-Württemberg, Germany) was a member of the House of Bourbon-Two Sicilies and a Princess of Bourbon-Two Sicilies.
Early life and family

Princess Urraca of Bourbon-Two Sicilies was born on 14 July 1913, at Nymphenburg Palace in Munich, Kingdom of Bavaria.
She was the sixth and youngest child of Prince Ferdinand Pius of Bourbon-Two Sicilies, Duke of Castro (1869–1960) and his wife Princess Maria Ludwiga Theresia of Bavaria (1872–1954).
Ferdinand Pius was the Head of the House of Bourbon-Two Sicilies and pretender to the defunct throne of the Kingdom of the Two Sicilies from 26 May 1934 to 7 January 1960.
Urraca had five older siblings, four sisters and one brother: Princess Maria Antonietta (1898–1957), Princess Maria Cristina (1899–1985), Prince Ruggiero Maria, Duke of Noto (1901–1914), Princess Barbara Maria (1902–1927), and Princess Lucia (1908–2001).
Through her father, Urraca was a granddaughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta (1841–1934) and his wife Princess Maria Antonietta of Bourbon-Two Sicilies (1851–1938).
Urraca was descended from King Francis I of the Two Sicilies (1777–1830) through her paternal great-grandfathers, King Ferdinand II of the Two Sicilies (1810–1859) and Prince Francis of Bourbon-Two Sicilies, Count of Trapani (1827–1892).
Through her mother, she was a granddaughter of King Ludwig III of Bavaria (1845– 1921) and his wife Archduchess Maria Theresa of Austria-Este (1849–1919).
Urraca chose not to celebrate her birthday, stating: "How can a Bourbon celebrate on the day of the Bastille's taking?
"


Adult life

As the daughter of the heir-apparent, then head of the House of Bourbon-Two Sicilies, Urraca regularly represented her family at royal and aristocratic functions and charitable events.
She attended the funeral of her great-uncle Prince Leopold of Bavaria on 3 October 1930, at St. Michael's Church in Munich.
Urraca, her mother, and her sister Lucia attended an afternoon dance tea at the Hotel Vier Jahreszeiten and the Hungarian Aid Association's Hungarian Ball in Munich in January 1934.
On 16 April 1936, Urraca attended the wedding of her first cousin Infante Alfonso of Spain, Prince of Bourbon-Two Sicilies to Princess Alicia of Bourbon-Parma at the Minoritenkirche in Vienna.
She was a guest of honor at the Austrian Armed Forces' Spring Parade in April 1936, along with Alfonso XIII of Spain, Princess Maria Anna of Bourbon-Parma, and Prince Elias of Bourbon-Parma.
Urraca attended the Baltic Red Cross Ball and the ball of Countess Adelheid Arco-Valley in the Cherubinsälen of the Hotel Vier Jahreszeiten in February 1938.
On 23 October 1957, she attended the wedding of her first cousin Princess Marie Gabrielle of Bavaria and Georg, Prince of Waldburg zu Zeil und Trauchburg in Munich.
On the night of 10 January 1957, Urraca was driving her eldest sister Maria Antonietta to her home in Lindau, Germany, when their automobile collided with a truck that had skid on ice near Winterthur, Switzerland.
Maria Antonietta was killed in the accident and Urraca was seriously injured.
Urraca was also an active supporter of Duosicilian historical societies and other royalty and nobility organizations.
Her first cousin once removed and claimant to the Duosicilian throne, Infante Carlos, Duke of Calabria, was also in attendance.
In February 1994, Urraca traveled to Gaeta where she participated in a tribute to the centenary of the death of Francis II, King of the Two Sicilies and an observation of the 133rd anniversary of the conclusion of the Siege of Gaeta which marked the victory of the Kingdom of Sardinia over Two Sicilies.
Death

Urraca died on 3 May 1999, in Sigmaringen, Baden-Württemberg, Germany.



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
  AssignClass (8a4c875c-7abd-4a57-83ae-570e19c253aa)
 Call ID: 8a4c875c-7abd-4a57-83ae-570e19c253aa
  Args:
    type: :Person
    source: :Urraca_of_Bourbon-Two_Sicilies
  AssignClass (d32f8098-a195-4074-8b07-cad3c1b1b965)
 Call ID: d32f8098-a195-4074-8b07-cad3c1b1b965
  Args:
    source: :Urraca_of_Bourbon-Two_Sicilies
    type: :Woman
  AddLiteral (0be36444-f818-4c15-a2b9-85481a5e2543)
 Call ID: 0be36444-f818-4c15-a2b9-85481a5e2543
  Args:
    source: :Urraca_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1913
  AddLiteral (2e4555ee-de99-4479-9dce-121d94456ee0)
 Call ID: 2e4555ee-de99-4479-9dce-121d94456ee0
  Args:
    source: :Urraca_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1999
  AssignClass (6188a377-3970-45a9-857b-cd2d6b643c22)
 Call ID: 6188a377-3970-45a9-857b-cd2d6b643c22
  Args:
    source: :Ferdinand_Pius_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (0a130d56-62f9-4677-b22a-13132089b7dd)
 Call ID: 0a130d56-62f9-4677-b22a-13132089b7dd
  Args:
    type: :Man
    source: :Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AssignClass (9f11a096-ae04-4572-9bdc-34ee6f5b0793)
 Call ID: 9f11a096-ae04-4572-9bdc-34ee6f5b0793
  Args:
    source: :Maria_Ludwiga_Theresia_of_Bavaria
    type: :Person
  AssignClass (ab8850ad-1856-46d9-bf76-ddf4fceba6a9)
 Call ID: ab8850ad-1856-46d9-bf76-ddf4fceba6a9
  Args:
    type: :Woman
    source: :Maria_Ludwiga_Theresia_of_Bavaria
  AddTriple (d2adadd8-bd82-42e6-8bb6-6d398c5815db)
 Call ID: d2adadd8-bd82-42e6-8bb6-6d398c5815db
  Args:
    target: :Ferdinand_Pius_of_Bourbon-Two_Sicilies
    source: :Urraca_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (f8abc2ee-443b-4944-b5f9-84ee3d7f3e27)
 Call ID: f8abc2ee-443b-4944-b5f9-84ee3d7f3e27
  Args:
    relation: :hasMother
    source: :Urraca_of_Bourbon-Two_Sicilies
    target: :Maria_Ludwiga_Theresia_of_Bavaria
  AssignClass (9180dba3-3cd6-4f86-bdaf-8433d5fb6a91)
 Call ID: 9180dba3-3cd6-4f86-bdaf-8433d5fb6a91
  Args:
    type: :Person
    source: :Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (5481ae4f-f32e-4187-bd97-6b7b3369e9e6)
 Call ID: 5481ae4f-f32e-4187-bd97-6b7b3369e9e6
  Args:
    source: :Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (7af18917-c0ea-4e7e-8160-c919f95da563)
 Call ID: 7af18917-c0ea-4e7e-8160-c919f95da563
  Args:
    type: :Person
    source: :Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (88e7481c-670a-4b97-af9f-ad07c3dc5d3c)
 Call ID: 88e7481c-670a-4b97-af9f-ad07c3dc5d3c
  Args:
    type: :Woman
    source: :Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (4fbdb25b-9125-4aa4-81d1-197cc58e7b58)
 Call ID: 4fbdb25b-9125-4aa4-81d1-197cc58e7b58
  Args:
    source: :Ruggiero_Maria_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (ce0b23fa-75c3-41c6-86d2-e17b7fe06865)
 Call ID: ce0b23fa-75c3-41c6-86d2-e17b7fe06865
  Args:
    source: :Ruggiero_Maria_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (6f1bb285-b7fb-43bd-957d-f7f0d2428f9f)
 Call ID: 6f1bb285-b7fb-43bd-957d-f7f0d2428f9f
  Args:
    type: :Person
    source: :Barbara_Maria_of_Bourbon-Two_Sicilies
  AssignClass (068b5e5d-e974-46f6-8c5f-7d3d2b0c599d)
 Call ID: 068b5e5d-e974-46f6-8c5f-7d3d2b0c599d
  Args:
    type: :Woman
    source: :Barbara_Maria_of_Bourbon-Two_Sicilies
  AssignClass (73928c5a-2808-4ec5-911c-105128126de1)
 Call ID: 73928c5a-2808-4ec5-911c-105128126de1
  Args:
    type: :Person
    source: :Lucia_of_Bourbon-Two_Sicilies
  AssignClass (98fb9cfc-dbee-419a-a39a-70267892db9d)
 Call ID: 98fb9cfc-dbee-419a-a39a-70267892db9d
  Args:
    type: :Woman
    source: :Lucia_of_Bourbon-Two_Sicilies
  AddTriple (bba83654-31cd-4430-a73a-33ab4965f233)
 Call ID: bba83654-31cd-4430-a73a-33ab4965f233
  Args:
    target: :Maria_Antonietta_of_Bourbon-Two_Sicilies
    source: :Urraca_of_Bourbon-Two_Sicilies
    relation: :isSiblingOf
  AddTriple (bdb45e91-190a-4ab8-b984-0cbd879e90ca)
 Call ID: bdb45e91-190a-4ab8-b984-0cbd879e90ca
  Args:
    relation: :isSiblingOf
    target: :Maria_Cristina_of_Bourbon-Two_Sicilies
    source: :Urraca_of_Bourbon-Two_Sicilies
  AddTriple (dc2ea984-4aa5-4a45-a109-b5d3a4f21fc8)
 Call ID: dc2ea984-4aa5-4a45-a109-b5d3a4f21fc8
  Args:
    relation: :isSiblingOf
    source: :Urraca_of_Bourbon-Two_Sicilies
    target: :Ruggiero_Maria_of_Bourbon-Two_Sicilies
  AddTriple (9e22193a-6850-40e3-9aae-04cdb006cfa6)
 Call ID: 9e22193a-6850-40e3-9aae-04cdb006cfa6
  Args:
    relation: :isSiblingOf
    source: :Urraca_of_Bourbon-Two_Sicilies
    target: :Barbara_Maria_of_Bourbon-Two_Sicilies
  AddTriple (fd1723b7-b48d-4dbf-97ca-a6c87572bea0)
 Call ID: fd1723b7-b48d-4dbf-97ca-a6c87572bea0
  Args:
    target: :Lucia_of_Bourbon-Two_Sicilies
    source: :Urraca_of_Bourbon-Two_Sicilies
    relation: :isSiblingOf
  AssignClass (1c3feb45-161c-4e52-968e-5e08284656d8)
 Call ID: 1c3feb45-161c-4e52-968e-5e08284656d8
  Args:
    source: :Alfonso_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (73f82651-74a5-4b1f-a7bf-922dc104b620)
 Call ID: 73f82651-74a5-4b1f-a7bf-922dc104b620
  Args:
    type: :Man
    source: :Alfonso_of_Bourbon-Two_Sicilies
  AssignClass (e664935f-13af-4b44-9937-428f98f57ad5)
 Call ID: e664935f-13af-4b44-9937-428f98f57ad5
  Args:
    type: :Person
    source: :Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
  AssignClass (988c4be1-941c-4ec4-bae5-e3c36734138b)
 Call ID: 988c4be1-941c-4ec4-bae5-e3c36734138b
  Args:
    source: :Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
    type: :Woman
  AddTriple (d53aed8f-642e-45ee-8f28-796014eef115)
 Call ID: d53aed8f-642e-45ee-8f28-796014eef115
  Args:
    source: :Ferdinand_Pius_of_Bourbon-Two_Sicilies
    target: :Alfonso_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (788418b0-4141-4e13-a87a-6880852b2f84)
 Call ID: 788418b0-4141-4e13-a87a-6880852b2f84
  Args:
    relation: :hasMother
    target: :Maria_Antonietta_of_Bourbon-Two_Sicilies_1851
    source: :Ferdinand_Pius_of_Bourbon-Two_Sicilies
  AssignClass (9aed7f0d-cc64-41f8-a347-fa06ec62d5ed)
 Call ID: 9aed7f0d-cc64-41f8-a347-fa06ec62d5ed
  Args:
    source: :Ludwig_III_of_Bavaria
    type: :Person
  AssignClass (7ef86031-8d2f-498e-80cd-0b3965425634)
 Call ID: 7ef86031-8d2f-498e-80cd-0b3965425634
  Args:
    type: :Man
    source: :Ludwig_III_of_Bavaria
  AssignClass (a391f790-9266-49c5-8c58-680c7b5b5b9b)
 Call ID: a391f790-9266-49c5-8c58-680c7b5b5b9b
  Args:
    source: :Maria_Theresa_of_Austria-Este
    type: :Person
  AssignClass (0ceb122d-4b5c-4923-b8ef-b89c970869d8)
 Call ID: 0ceb122d-4b5c-4923-b8ef-b89c970869d8
  Args:
    source: :Maria_Theresa_of_Austria-Este
    type: :Woman
  AddTriple (ee03a040-38ac-4898-937e-f136dcb5fb69)
 Call ID: ee03a040-38ac-4898-937e-f136dcb5fb69
  Args:
    target: :Ludwig_III_of_Bavaria
    source: :Maria_Ludwiga_Theresia_of_Bavaria
    relation: :hasFather
  AddTriple (9a47394c-14ad-4711-9d23-29e763ac9077)
 Call ID: 9a47394c-14ad-4711-9d23-29e763ac9077
  Args:
    target: :Maria_Theresa_of_Austria-Este
    source: :Maria_Ludwiga_Theresia_of_Bavaria
    relation: :hasMother
  Finish (9bb9da41-691e-48e9-9cc3-e4ca19fc3fd1)
 Call ID: 9bb9da41-691e-48e9-9cc3-e4ca19fc3fd1
  Args: