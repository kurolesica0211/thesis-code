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
Franz Wilhelm Victor Christoph Stephan Prinz von Preussen (born 3 September 1943) is a German businessman and member of the House of Hohenzollern, the former ruling German imperial house and royal house of Prussia.
He is also the great-grandson of German Emperor Wilhelm II.
Biography

Franz Wilhelm Prince of Prussia was born in Grünberg, Silesia, as the son of Prince Karl Franz of Prussia and his first wife Princess Henriette von Schönaich-Carolath.
He had a twin brother, Prince Friedrich Christian, who died three weeks after his birth.
Prince Franz Wilhelm is a grandson of Prince Joachim of Prussia, the youngest son of Emperor Wilhelm II.
In 2002 Franz Wilhelm with Theodor Tantzen founded the Prinz von Preußen Grundbesitz AG, a project development and project management company which restores old buildings in Germany.
Personal life

Franz Wilhelm married his third cousin once removed, Grand Duchess Maria Vladimirovna of Russia, great-great-granddaughter of Queen Victoria, civilly on 4 September 1976 at Dinard and religiously on 22 September at the Russian Orthodox Chapel in Madrid.
Before his marriage, he converted to the Russian Orthodox faith and was created a Grand Duke of Russia with the name Mikhail Pavlovich by his father-in-law Grand Duke Vladimir of Russia.
Franz Wilhelm and Grand Duchess Maria had one son before divorcing on 19 June 1985 (they separated in 1982), at which point he reverted to his previous title.
He married Nadia Nour El Etreby (born 2 August 1949) on 14 March 2019, to whom was bestowed upon marriage the courtesy style and title of Her Royal Highness Princess Franz Wilhelm of Prussia.



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
  AssignClass (d1030f76-9c83-4edb-9ab9-ffade05bbcda)
 Call ID: d1030f76-9c83-4edb-9ab9-ffade05bbcda
  Args:
    type: :Man
    source: FranzWilhelmPrinzVonPreussen
  AssignClass (03ea5c3b-6e3f-4dcc-aaf2-040a9c60b844)
 Call ID: 03ea5c3b-6e3f-4dcc-aaf2-040a9c60b844
  Args:
    type: :Person
    source: FranzWilhelmPrinzVonPreussen
  AssignClass (bda8c2f8-781b-4325-aaaf-389437e214ac)
 Call ID: bda8c2f8-781b-4325-aaaf-389437e214ac
  Args:
    type: :Male
    source: Male
  AddLiteral (7714b616-22da-4882-9bbe-25595ac4c096)
 Call ID: 7714b616-22da-4882-9bbe-25595ac4c096
  Args:
    source: FranzWilhelmPrinzVonPreussen
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1943
  AddTriple (28dec084-f52c-41fc-b1d6-066e7dff7ca4)
 Call ID: 28dec084-f52c-41fc-b1d6-066e7dff7ca4
  Args:
    relation: :hasSex
    source: FranzWilhelmPrinzVonPreussen
    target: Male
  AssignClass (5f548c14-6c29-4410-a0b2-a7b7394c2247)
 Call ID: 5f548c14-6c29-4410-a0b2-a7b7394c2247
  Args:
    type: :Man
    source: KarlFranzOfPrussia
  AssignClass (32f52900-3685-4b1a-9ff4-4aa3fe60994b)
 Call ID: 32f52900-3685-4b1a-9ff4-4aa3fe60994b
  Args:
    type: :Person
    source: KarlFranzOfPrussia
  AddTriple (cc567276-4eed-4972-b62f-6eb621d127b1)
 Call ID: cc567276-4eed-4972-b62f-6eb621d127b1
  Args:
    relation: :isFatherOf
    source: KarlFranzOfPrussia
    target: FranzWilhelmPrinzVonPreussen
  AssignClass (c1121020-1ac0-491a-89bf-8b7e52ad9967)
 Call ID: c1121020-1ac0-491a-89bf-8b7e52ad9967
  Args:
    type: :Woman
    source: HenrietteVonSchonaichCarolath
  AssignClass (bb05b571-bb22-4ab0-b35e-cd993296efc6)
 Call ID: bb05b571-bb22-4ab0-b35e-cd993296efc6
  Args:
    type: :Person
    source: HenrietteVonSchonaichCarolath
  AddTriple (16c8b240-8155-4cbe-9824-bcb44aa2883f)
 Call ID: 16c8b240-8155-4cbe-9824-bcb44aa2883f
  Args:
    target: FranzWilhelmPrinzVonPreussen
    source: HenrietteVonSchonaichCarolath
    relation: :isMotherOf
  AssignClass (de580fe3-3107-413e-8796-00daefdfe329)
 Call ID: de580fe3-3107-413e-8796-00daefdfe329
  Args:
    type: :Man
    source: FriedrichChristian
  AssignClass (52b68812-fef4-4482-94b9-b821b4f33c10)
 Call ID: 52b68812-fef4-4482-94b9-b821b4f33c10
  Args:
    type: :Person
    source: FriedrichChristian
  AddTriple (1d282dcb-0ba6-4dc0-91fb-39f3935796fa)
 Call ID: 1d282dcb-0ba6-4dc0-91fb-39f3935796fa
  Args:
    relation: :hasBrother
    source: FranzWilhelmPrinzVonPreussen
    target: FriedrichChristian
  AssignClass (f551ecf9-77de-41d9-aec0-e3dc64ee8ce3)
 Call ID: f551ecf9-77de-41d9-aec0-e3dc64ee8ce3
  Args:
    type: :Man
    source: JoachimOfPrussia
  AssignClass (210ebafc-bba6-4530-be5f-40e5c5e87401)
 Call ID: 210ebafc-bba6-4530-be5f-40e5c5e87401
  Args:
    type: :Person
    source: JoachimOfPrussia
  AddTriple (0fe16d7d-1e37-4a2b-a3e5-28fc471d31cb)
 Call ID: 0fe16d7d-1e37-4a2b-a3e5-28fc471d31cb
  Args:
    target: KarlFranzOfPrussia
    source: JoachimOfPrussia
    relation: :isFatherOf
  AssignClass (c40c6f7c-e4b9-4341-8be2-a0ad134ac6e5)
 Call ID: c40c6f7c-e4b9-4341-8be2-a0ad134ac6e5
  Args:
    type: :Man
    source: WilhelmII
  AssignClass (2cea90ab-4e77-4d28-b511-052a0e87e560)
 Call ID: 2cea90ab-4e77-4d28-b511-052a0e87e560
  Args:
    type: :Person
    source: WilhelmII
  AddTriple (cf51e798-f9b2-4704-8b42-2f9f2f61442e)
 Call ID: cf51e798-f9b2-4704-8b42-2f9f2f61442e
  Args:
    relation: :isFatherOf
    target: JoachimOfPrussia
    source: WilhelmII
  AssignClass (593bb715-c407-445e-84ef-a80d58c7aed7)
 Call ID: 593bb715-c407-445e-84ef-a80d58c7aed7
  Args:
    type: :Woman
    source: MariaVladimirovnaOfRussia
  AssignClass (b38d0cca-b543-4af1-884e-fb358f4fcc5c)
 Call ID: b38d0cca-b543-4af1-884e-fb358f4fcc5c
  Args:
    type: :Person
    source: MariaVladimirovnaOfRussia
  AddLiteral (9aa504a6-f27c-4b7d-bf99-8a74b526e1e0)
 Call ID: 9aa504a6-f27c-4b7d-bf99-8a74b526e1e0
  Args:
    literal_value: 1976
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: FranzWilhelmPrinzVonPreussen
  AddTriple (11bfd20e-e10c-405b-81f8-287d79dea77b)
 Call ID: 11bfd20e-e10c-405b-81f8-287d79dea77b
  Args:
    target: MariaVladimirovnaOfRussia
    source: FranzWilhelmPrinzVonPreussen
    relation: :hasRelation
  AssignClass (bfac470d-3685-4a8a-9dbe-9460814a753f)
 Call ID: bfac470d-3685-4a8a-9dbe-9460814a753f
  Args:
    type: :Woman
    source: QueenVictoria
  AssignClass (d3a1b93c-e3c7-40e6-baf7-fb6c168db809)
 Call ID: d3a1b93c-e3c7-40e6-baf7-fb6c168db809
  Args:
    type: :Person
    source: QueenVictoria
  AssignClass (faa60301-27da-4ef0-b52f-617fed7b792b)
 Call ID: faa60301-27da-4ef0-b52f-617fed7b792b
  Args:
    type: :Man
    source: VladimirOfRussia
  AssignClass (c44493c1-40a4-4b37-8690-0ead04ca6d98)
 Call ID: c44493c1-40a4-4b37-8690-0ead04ca6d98
  Args:
    type: :Person
    source: VladimirOfRussia
  AddTriple (5f2a5e78-d349-4108-97f0-b2753a5dfca9)
 Call ID: 5f2a5e78-d349-4108-97f0-b2753a5dfca9
  Args:
    source: VladimirOfRussia
    target: MariaVladimirovnaOfRussia
    relation: :isFatherOf
  AssignClass (28da8a84-f1a3-47ef-804c-bdb1541167a2)
 Call ID: 28da8a84-f1a3-47ef-804c-bdb1541167a2
  Args:
    type: :Woman
    source: NadiaNourElEtreby
  AssignClass (62008acd-f097-42b0-974b-aabcb67954e0)
 Call ID: 62008acd-f097-42b0-974b-aabcb67954e0
  Args:
    type: :Person
    source: NadiaNourElEtreby
  AddLiteral (3ba0a288-9fea-49fa-a754-9f76a4905fed)
 Call ID: 3ba0a288-9fea-49fa-a754-9f76a4905fed
  Args:
    source: NadiaNourElEtreby
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1949
  AddLiteral (551f8ec3-5070-4f98-9665-dd1603fb007e)
 Call ID: 551f8ec3-5070-4f98-9665-dd1603fb007e
  Args:
    literal_type: xsd:integer
    literal_value: 2019
    relation: :hasMarriageYear
    source: FranzWilhelmPrinzVonPreussen
  AddTriple (2ee8dcd1-5bdc-4906-a03b-0b0919aa4fa0)
 Call ID: 2ee8dcd1-5bdc-4906-a03b-0b0919aa4fa0
  Args:
    relation: :hasRelation
    target: NadiaNourElEtreby
    source: FranzWilhelmPrinzVonPreussen
  Finish (ee61b7b0-a320-4f94-9ac0-feea250ac60d)
 Call ID: ee61b7b0-a320-4f94-9ac0-feea250ac60d
  Args: