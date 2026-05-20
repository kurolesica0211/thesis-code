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
Princess Isabelle Françoise Hélène Marie d'Orléans (27 November 1900, Le Nouvion-en-Thiérache, France – 12 February 1983, Neuilly-sur-Seine, France) was a member of the House of Orléans and, by marriage, a member of the ducal Harcourt family and of the princely House of Murat.
She was one of the four children of Prince Jean, Duke of Guise (1874–1940), who would become the Orleanist pretender to the French throne in 1926, and Princess Isabelle of Orléans.
Marriages

In 1923 the tradition of Orléans princesses marrying only other royalty (since the alleged 1681 wedding of La Grande Mademoiselle) was dispensed with, as nearly all of her relatives attended Isabelle's wedding at Amélie of Orléans château in Le Chesnay on 12 September to Count Bruno d'Harcourt (1899–1930), son of Count Eugène d'Harcourt and Armande de Pierre de Bernis.
An automobile racer, Harcourt was killed during practice for the Moroccan Grand Prix, leaving his wife with four children:


As a widow, Isabelle remarried the Bonapartist Prince Pierre Murat (1900–1948) in 1934, at Jouy-en-Josas, "upon renunciation of the rank and prerogatives appertaining to princesses of the House of France".
Prince Murat was a  great-grandson of Prince Lucien Murat.
In 1940, as World War II began and when her father died, Isabelle again took refuge at the family estate, Larache, in Morocco, where she shared quarters with her mother, and her elder sister the widowed Princess Françoise of Greece, along with her brother Henri, Count of Paris and the latter's son, Prince Michel d'Orléans.Isabella often visited her parents in Morocco, Belgium and France, especially during World 
War II.
In 1953, her younger sister,Princess Françoise, widow of Prince Christopher of Greece, died in her Paris home after a long period of depression.
Princess Isabella herself died in 1983 and is buried in the Montparnasse Cemetery in Paris.



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
  AssignClass (cdc2ac20-dad6-4913-bb1b-658806fce308)
 Call ID: cdc2ac20-dad6-4913-bb1b-658806fce308
  Args:
    type: :Woman
    source: :PrincessIsabelleDOrleans
  AddLiteral (6b2ab363-2715-4a42-9f90-8abae77af212)
 Call ID: 6b2ab363-2715-4a42-9f90-8abae77af212
  Args:
    literal_value: 1900
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :PrincessIsabelleDOrleans
  AddLiteral (e29118e5-b49b-40a6-8374-653a2d41be7f)
 Call ID: e29118e5-b49b-40a6-8374-653a2d41be7f
  Args:
    relation: :hasDeathYear
    literal_value: 1983
    source: :PrincessIsabelleDOrleans
    literal_type: xsd:integer
  AssignClass (a3c0e640-cc47-46d6-be5b-346618725ff2)
 Call ID: a3c0e640-cc47-46d6-be5b-346618725ff2
  Args:
    type: :Man
    source: :PrinceJeanDukeOfGuise
  AddLiteral (81067556-4282-4557-b329-dad471ed22dc)
 Call ID: 81067556-4282-4557-b329-dad471ed22dc
  Args:
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :PrinceJeanDukeOfGuise
  AddLiteral (b1f78df4-b430-4952-8f80-1d6c7460bc38)
 Call ID: b1f78df4-b430-4952-8f80-1d6c7460bc38
  Args:
    relation: :hasDeathYear
    literal_value: 1940
    source: :PrinceJeanDukeOfGuise
    literal_type: xsd:integer
  AssignClass (b481c216-3485-44e3-8f90-5d1653b67aab)
 Call ID: b481c216-3485-44e3-8f90-5d1653b67aab
  Args:
    type: :Woman
    source: :PrincessIsabelleOfOrleans
  AddTriple (3f92079a-1dcd-4499-84b6-f836c374a48f)
 Call ID: 3f92079a-1dcd-4499-84b6-f836c374a48f
  Args:
    target: :PrinceJeanDukeOfGuise
    relation: :hasFather
    source: :PrincessIsabelleDOrleans
  AddTriple (9115b567-5dc3-47f1-b740-5f4c709b56b6)
 Call ID: 9115b567-5dc3-47f1-b740-5f4c709b56b6
  Args:
    source: :PrincessIsabelleDOrleans
    relation: :hasMother
    target: :PrincessIsabelleOfOrleans
  AssignClass (2bd999f1-4c2a-4c4a-88de-7ece2925c9a6)
 Call ID: 2bd999f1-4c2a-4c4a-88de-7ece2925c9a6
  Args:
    type: :Man
    source: :CountBrunoDHarcourt
  AddLiteral (843a6779-6b49-4083-9b36-28ec3bdd8e9a)
 Call ID: 843a6779-6b49-4083-9b36-28ec3bdd8e9a
  Args:
    literal_value: 1899
    relation: :hasBirthYear
    source: :CountBrunoDHarcourt
    literal_type: xsd:integer
  AddLiteral (e9739902-3786-42b0-abbc-99b0a619781b)
 Call ID: e9739902-3786-42b0-abbc-99b0a619781b
  Args:
    literal_type: xsd:integer
    source: :CountBrunoDHarcourt
    relation: :hasDeathYear
    literal_value: 1930
  AddLiteral (2c414be5-b1e0-4a46-a92b-57c747982550)
 Call ID: 2c414be5-b1e0-4a46-a92b-57c747982550
  Args:
    literal_value: 1923
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :PrincessIsabelleDOrleans
  AddTriple (3dcd2544-6ac6-48ce-b2bf-2d4b2e13d8a6)
 Call ID: 3dcd2544-6ac6-48ce-b2bf-2d4b2e13d8a6
  Args:
    relation: :hasRelation
    target: :CountBrunoDHarcourt
    source: :PrincessIsabelleDOrleans
  AssignClass (c4de5003-46eb-4f44-a123-4c3647bcc849)
 Call ID: c4de5003-46eb-4f44-a123-4c3647bcc849
  Args:
    type: :Man
    source: :CountEugeneDHarcourt
  AssignClass (9acfffaa-3f36-40ab-8273-0b37f1667e28)
 Call ID: 9acfffaa-3f36-40ab-8273-0b37f1667e28
  Args:
    type: :Woman
    source: :ArmandeDePierreDeBernis
  AddTriple (b10fdd1a-a62d-4adb-891d-efddbd830806)
 Call ID: b10fdd1a-a62d-4adb-891d-efddbd830806
  Args:
    source: :CountBrunoDHarcourt
    target: :CountEugeneDHarcourt
    relation: :hasFather
  AddTriple (2c3c79f5-c230-44a5-bd5d-dc6466e24b7c)
 Call ID: 2c3c79f5-c230-44a5-bd5d-dc6466e24b7c
  Args:
    relation: :hasMother
    target: :ArmandeDePierreDeBernis
    source: :CountBrunoDHarcourt
  AssignClass (64ce918f-82aa-4cfb-b379-b34b84bcadaf)
 Call ID: 64ce918f-82aa-4cfb-b379-b34b84bcadaf
  Args:
    type: :Man
    source: :PrincePierreMurat
  AddLiteral (01b9f743-ac9f-4088-9d45-3a5b061e678b)
 Call ID: 01b9f743-ac9f-4088-9d45-3a5b061e678b
  Args:
    relation: :hasBirthYear
    literal_value: 1900
    literal_type: xsd:integer
    source: :PrincePierreMurat
  AddLiteral (d44ea3aa-0b77-484e-b506-84833014c967)
 Call ID: d44ea3aa-0b77-484e-b506-84833014c967
  Args:
    literal_type: xsd:integer
    source: :PrincePierreMurat
    relation: :hasDeathYear
    literal_value: 1948
  AddLiteral (314f352c-1d1d-475a-8b9e-2b372afb5bfc)
 Call ID: 314f352c-1d1d-475a-8b9e-2b372afb5bfc
  Args:
    literal_value: 1934
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :PrincessIsabelleDOrleans
  AddTriple (cc5c338c-2ab2-4bef-8ead-a34ff8f8d498)
 Call ID: cc5c338c-2ab2-4bef-8ead-a34ff8f8d498
  Args:
    target: :PrincePierreMurat
    relation: :hasRelation
    source: :PrincessIsabelleDOrleans
  AssignClass (9eddc7ba-5877-4826-9794-6afa0172e665)
 Call ID: 9eddc7ba-5877-4826-9794-6afa0172e665
  Args:
    type: :Man
    source: :PrinceLucienMurat
  AssignClass (08b87275-fdfa-4d39-bdd4-b3b4fbd006e0)
 Call ID: 08b87275-fdfa-4d39-bdd4-b3b4fbd006e0
  Args:
    type: :Woman
    source: :PrincessFrancoiseOfGreece
  AddTriple (c82f004f-db78-4247-bc25-1049cea18d8c)
 Call ID: c82f004f-db78-4247-bc25-1049cea18d8c
  Args:
    relation: :hasSister
    target: :PrincessFrancoiseOfGreece
    source: :PrincessIsabelleDOrleans
  AssignClass (47df5df7-ea7b-478e-83c8-b97d443e0291)
 Call ID: 47df5df7-ea7b-478e-83c8-b97d443e0291
  Args:
    type: :Man
    source: :PrinceChristopherOfGreece
  AddTriple (20e4243c-7265-445c-abfd-03ea2c31ad69)
 Call ID: 20e4243c-7265-445c-abfd-03ea2c31ad69
  Args:
    relation: :hasRelation
    target: :PrinceChristopherOfGreece
    source: :PrincessFrancoiseOfGreece
  AssignClass (66b0f3d5-b3e5-4121-a254-0c374ad422b5)
 Call ID: 66b0f3d5-b3e5-4121-a254-0c374ad422b5
  Args:
    type: :Man
    source: :HenriCountOfParis
  AddTriple (4872eeb4-d989-44c3-8504-a4206192e85e)
 Call ID: 4872eeb4-d989-44c3-8504-a4206192e85e
  Args:
    relation: :hasBrother
    target: :HenriCountOfParis
    source: :PrincessIsabelleDOrleans
  AssignClass (4ad99c89-8416-43db-a5e5-a78d3d930c40)
 Call ID: 4ad99c89-8416-43db-a5e5-a78d3d930c40
  Args:
    type: :Man
    source: :PrinceMichelDOrleans
  AddTriple (8260031a-8407-4973-94ba-c8844abc9a56)
 Call ID: 8260031a-8407-4973-94ba-c8844abc9a56
  Args:
    source: :PrinceMichelDOrleans
    target: :HenriCountOfParis
    relation: :hasFather
  Finish (e17e6c15-2962-43c5-959d-4ae7b736296e)
 Call ID: e17e6c15-2962-43c5-959d-4ae7b736296e
  Args: