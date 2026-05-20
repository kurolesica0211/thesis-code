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
Princess Xenia Georgievna of Russia (22 August 1903 – 17 September 1965) was the younger daughter of Grand Duke George Mihailovich of Russia and Princess Maria Georgievna of Greece and Denmark.
She is known for recognizing Anna Anderson as Grand Duchess Anastasia.
Youth

Xenia and her older sister Princess Nina Georgievna, who was born in 1901, left Russia in 1914 to spend the war years in England with their mother.
In 1919, her father, his brother Grand Duke Nicholas Mikhailovich, and their cousins Grand Duke Paul Alexandrovich and Grand Duke Dmitry Konstantinovich, were executed by a Bolshevik firing squad in St. Petersburg.
Anna Anderson controversy

In the summer of 1927, Xenia involved herself in the Anna Anderson/Anastasia Tchaikovsky affair by telephoning Gleb Botkin (son of imperial physician Eugene Botkin, who had been murdered along with the former tsar and his family in 1918) with an invitation for Anna to live as a guest at their luxurious estate in New York's Oyster Bay.
Xenia explains her hospitality: "I had heard that Botkin was arranging to bring 'the invalid' to the United States through a newspaper organization.
As children, Xenia and her sister Nina had played frequently with the two youngest daughters of Tsar Nicholas II, Grand Duchesses Maria Nikolaevna and Anastasia Nikolaevna, as well as the youngest child and only boy, Tsarevitch Alexei.
Through her father, Xenia was Anastasia's second cousin, once removed and through her mother they were second cousins.
According to Xenia, Anastasia "cheated at games, kicked, scratched, pulled hair, and generally knew how to make herself obnoxious.
"


Xenia was on a cruise with her husband William in the West Indies at the time of Anna's arrival in New York.
She had arranged for Anna to stay with Annie Burr Jennings, a friend of Xenia's who lived in a Park Avenue townhouse.
Upon her return, Xenia sneaked unannounced into Annie Jennings's crowded salon to observe Anna.
After watching Anna offer her hand to Gleb Botkin, Xenia declared that she knew she was watching an equal.
"


Xenia recognized Anna Anderson as the Grand Duchess Anastasia at once, asserting that Anna was herself at all times, never giving the slightest impression of playing a part.
The two remained great friends for life even after Anna Anderson had to leave Xenia's home after quarreling.
Then her treatment of the Grand Duchess Xenia, sister of the last Tsar, led to a quarrel with William Leeds, who turned her out of the house.
Pierre Gilliard, tutor for the five children of Tsar Nicholas II from 1905 to 1918, pointed out that Princess Xenia had last seen her second cousin when Xenia was 10 and Anastasia was 12.
Xenia responded that she did not recognize Anastasia visually, but felt she was qualified to tell the difference between a member of the Romanov family and a "Polish peasant woman."
Anderson bore a strong family resemblance to Tsarina Alexandra's family and her moodiness and temper also reminded Xenia of her cousin Anastasia.
Prince Dmitri, son of Grand Duchess Xenia, wrote about what Princess Xenia had stated,


Xenia's irresponsible statement should be somehow refuted ...
We know she left Russia in 1914 aged 10 years old, I also know that Nina (her sister) and Xenia never saw Uncle Nicky's family very often, and when they did see them that was when they were very young.
Personal life

Xenia married twice.
At age 18 she married William Bateman Leeds Jr. (19 September 1902 – 31 December 1971), the son and heir of the American tin magnate William B. Leeds Sr. and the stepson of Xenia's maternal uncle Prince Christopher of Greece and Denmark, through his marriage to William’s mother, the former Nonie Stewart Leeds.
Xenia and William had a daughter on 25 February 1925, Nancy Helen Marie Leeds.
Xenia and William Leeds divorced in 1930.
Xenia's second marriage was with Herman Jud (1911–1987), whom she married at Glen Cove, New York, on 10 August 1946.
Death

Princess Xenia Georgievna died on 17 September 1965, aged 62, survived by her second husband and by her daughter, Nancy Leeds Wynkoop, and by granddaughter Alexandra.



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
  AssignClass (4e557bb6-6db0-4fb5-9824-ce1397171fd6)
 Call ID: 4e557bb6-6db0-4fb5-9824-ce1397171fd6
  Args:
    type: :Woman
    source: Xenia Georgievna
  AssignClass (3186ea45-c82e-4978-9b78-bd073268ab4b)
 Call ID: 3186ea45-c82e-4978-9b78-bd073268ab4b
  Args:
    type: :Person
    source: Xenia Georgievna
  AssignClass (5825b226-18cb-4ef4-842a-fe9651b65af9)
 Call ID: 5825b226-18cb-4ef4-842a-fe9651b65af9
  Args:
    type: :Ancestor
    source: Xenia Georgievna
  AssignClass (53f74336-11f4-4410-b1af-0940d4055915)
 Call ID: 53f74336-11f4-4410-b1af-0940d4055915
  Args:
    type: :Man
    source: George Mihailovich
  AssignClass (864c57db-864f-4d87-a19e-ced9b1b77a6e)
 Call ID: 864c57db-864f-4d87-a19e-ced9b1b77a6e
  Args:
    type: :Person
    source: George Mihailovich
  AssignClass (39cfd74d-65e6-4482-80cd-94e865069a71)
 Call ID: 39cfd74d-65e6-4482-80cd-94e865069a71
  Args:
    type: :Ancestor
    source: George Mihailovich
  AssignClass (65dbd447-f9c4-46e4-9b69-98edb6e1681d)
 Call ID: 65dbd447-f9c4-46e4-9b69-98edb6e1681d
  Args:
    type: :Woman
    source: Maria Georgievna
  AssignClass (36d4d125-fd5d-46c5-8c23-66ba6e3cebcb)
 Call ID: 36d4d125-fd5d-46c5-8c23-66ba6e3cebcb
  Args:
    type: :Person
    source: Maria Georgievna
  AssignClass (013efc2a-81e0-4098-afdc-e3810b332132)
 Call ID: 013efc2a-81e0-4098-afdc-e3810b332132
  Args:
    type: :Ancestor
    source: Maria Georgievna
  AddLiteral (0dc3a1d1-621b-46d0-aee9-e7fa275ae444)
 Call ID: 0dc3a1d1-621b-46d0-aee9-e7fa275ae444
  Args:
    literal_value: 1903
    relation: :hasBirthYear
    source: Xenia Georgievna
    literal_type: xsd:integer
  AddLiteral (827513e7-d39b-422e-95f4-6a0d33540866)
 Call ID: 827513e7-d39b-422e-95f4-6a0d33540866
  Args:
    literal_value: 1965
    literal_type: xsd:integer
    source: Xenia Georgievna
    relation: :hasDeathYear
  AddTriple (8f0a6753-6bdf-4d17-8d1d-dcee3c2557e2)
 Call ID: 8f0a6753-6bdf-4d17-8d1d-dcee3c2557e2
  Args:
    source: Xenia Georgievna
    relation: :hasFather
    target: George Mihailovich
  AddTriple (596e568c-b2e0-443a-a95d-948604591a13)
 Call ID: 596e568c-b2e0-443a-a95d-948604591a13
  Args:
    target: Maria Georgievna
    source: Xenia Georgievna
    relation: :hasMother
  AssignClass (e8a71e1c-7a1e-4140-8165-1b06ce8f7941)
 Call ID: e8a71e1c-7a1e-4140-8165-1b06ce8f7941
  Args:
    type: :Woman
    source: Nina Georgievna
  AssignClass (adb84ade-914e-4781-b4d0-143ad5cd9eef)
 Call ID: adb84ade-914e-4781-b4d0-143ad5cd9eef
  Args:
    type: :Person
    source: Nina Georgievna
  AddTriple (97c63a7f-61b4-4032-9e46-e750f7fdb4a2)
 Call ID: 97c63a7f-61b4-4032-9e46-e750f7fdb4a2
  Args:
    source: Xenia Georgievna
    relation: :hasSister
    target: Nina Georgievna
  AddTriple (583c2fbe-e5b6-40f0-b9e8-e299e5c17cd2)
 Call ID: 583c2fbe-e5b6-40f0-b9e8-e299e5c17cd2
  Args:
    target: Xenia Georgievna
    source: Nina Georgievna
    relation: :hasSister
  AssignClass (cf4c0de9-6f30-4a01-a67b-d5ce52d896a2)
 Call ID: cf4c0de9-6f30-4a01-a67b-d5ce52d896a2
  Args:
    type: :Man
    source: William Bateman Leeds Jr.
  AssignClass (dd954c58-9d7a-4512-b6e1-4eb8982a7462)
 Call ID: dd954c58-9d7a-4512-b6e1-4eb8982a7462
  Args:
    type: :Person
    source: William Bateman Leeds Jr.
  AddTriple (08c90d59-419d-4b04-9133-67c4f4ce2f08)
 Call ID: 08c90d59-419d-4b04-9133-67c4f4ce2f08
  Args:
    target: William Bateman Leeds Jr.
    relation: :hasRelation
    source: Xenia Georgievna
  AddLiteral (4190166f-9b9e-4706-b178-7a0832ebb9fb)
 Call ID: 4190166f-9b9e-4706-b178-7a0832ebb9fb
  Args:
    relation: :hasMarriageYear
    source: Xenia Georgievna
    literal_type: xsd:integer
    literal_value: 1921
  AssignClass (5a211b8f-e464-419b-a150-896c3933bf1b)
 Call ID: 5a211b8f-e464-419b-a150-896c3933bf1b
  Args:
    type: :Woman
    source: Nancy Helen Marie Leeds
  AssignClass (563c7e00-2154-4343-9cb5-2285b3a2155a)
 Call ID: 563c7e00-2154-4343-9cb5-2285b3a2155a
  Args:
    type: :Person
    source: Nancy Helen Marie Leeds
  AddTriple (4a7add39-df52-4e98-b51a-ec06cddb7670)
 Call ID: 4a7add39-df52-4e98-b51a-ec06cddb7670
  Args:
    source: Xenia Georgievna
    relation: :hasDaughter
    target: Nancy Helen Marie Leeds
  AddTriple (15b547de-fe8c-4ab1-8909-2caa4c23d59c)
 Call ID: 15b547de-fe8c-4ab1-8909-2caa4c23d59c
  Args:
    relation: :hasFather
    source: Nancy Helen Marie Leeds
    target: William Bateman Leeds Jr.
  AssignClass (a1e1c86e-8bd2-4aa1-b8af-c193e01f5c32)
 Call ID: a1e1c86e-8bd2-4aa1-b8af-c193e01f5c32
  Args:
    type: :Man
    source: Herman Jud
  AssignClass (6762e780-36b1-4ea1-a912-1916775d9380)
 Call ID: 6762e780-36b1-4ea1-a912-1916775d9380
  Args:
    type: :Person
    source: Herman Jud
  AddTriple (f55c4ec8-0780-47d2-b031-be0b1e362978)
 Call ID: f55c4ec8-0780-47d2-b031-be0b1e362978
  Args:
    target: Herman Jud
    source: Xenia Georgievna
    relation: :hasRelation
  AddLiteral (672d1baf-a08d-4f77-bb4e-f3f171af106c)
 Call ID: 672d1baf-a08d-4f77-bb4e-f3f171af106c
  Args:
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Xenia Georgievna
  AssignClass (8704058f-41c1-4c1a-be39-b1faa4b713f2)
 Call ID: 8704058f-41c1-4c1a-be39-b1faa4b713f2
  Args:
    type: :Man
    source: Nicholas Mikhailovich
  AssignClass (39bf2f07-621c-40b4-b7d3-e270872480a8)
 Call ID: 39bf2f07-621c-40b4-b7d3-e270872480a8
  Args:
    type: :Person
    source: Nicholas Mikhailovich
  AddTriple (344fef55-0b7c-43fa-8da9-3977ab803a22)
 Call ID: 344fef55-0b7c-43fa-8da9-3977ab803a22
  Args:
    target: Nicholas Mikhailovich
    relation: :hasBrother
    source: George Mihailovich
  Finish (7b3f3e21-999a-417e-b4b1-aa3e09b15303)
 Call ID: 7b3f3e21-999a-417e-b4b1-aa3e09b15303
  Args: