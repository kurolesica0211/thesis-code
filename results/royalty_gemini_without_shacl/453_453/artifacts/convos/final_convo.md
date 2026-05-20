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
Princess Alexia of Greece and Denmark (Greek: Αλεξία Ντε Γκρες, romanized: Alexía de Grèce; born 10 July 1965) is the eldest child of Constantine II and Anne-Marie, who were King and Queen of Greece from 1964 until the abolition of the monarchy in 1973.
Biography

Alexia was born on 10 July 1965 at Mon Repos, a villa on the Greek island of Corfu used at the time as a summer residence by the Greek royal family.
She was the first child born to the then King Constantine II and Queen Anne-Marie of the Hellenes.
At the time of her birth, her father was King of Greece, her grandfather was King of Denmark, and her great-grandfather was King of Sweden.
As the monarch's only child, between her own birth and the birth on 20 May 1967 of her brother Pavlos, Alexia was heir presumptive to the throne of the Hellenes, then an extant monarchy.
The Greek Constitution of 1952 had changed Greece's order of succession to the throne from the previous Salic law, prevalent in much of the continent, and which precluded the succession of women, to male-preference primogeniture, which accorded succession to the throne to a female member of a dynasty if she has no brothers, similar to the then extant succession laws of the United Kingdom, Denmark and Spain.
Alexia grew up in exile and was raised in between Rome and London.
The family then briefly moved to Denmark and stayed at Amalienborg Palace, and then to London the following year.
Prior to Alexia's education at the Hellenic College of London, she attended the Miss Surtee's School for Boys and Girls in Rome, Italy.
Οn 20 December 2024, Alexia along with other members of the former royal family acquired Greek citizenship, under the surname "de Grèce".
Marriage and children

Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


On 9 July 1999, Alexia married Carlos Javier Morales Quintana, an architect and a champion yachtsman, at St. Sophia Cathedral, London.
In May 1999, two months before their wedding, Alexia and Carlos were involved in a yachting accident on a boat named the Alexia.
Alexia and Carlos were the only two people out of the thirteen on board to be injured.
Alexia suffered a broken collarbone and Carlos a fractured kneecap.
At her wedding, Alexia wore a gown by the Austrian designer Inge Sprawson.
Alexia's mother, Anne-Marie, and grandmother, Ingrid, had both also worn the same tiara on their own wedding day.
Her attendants included her sister Princess Theodora, her niece Princess Maria-Olympia, and Princess Mafalda, daughter of Kyril, Prince of Preslav, a son of former King Simeon of Bulgaria.
The couple have four children: 


Their children's last names are "Morales y de Grecia", which translates to "Morales and of Greece", taking their father's surname and their mother's royal title.
Alexia and her family now live in her husband's native land, at Puerto Calero marina, Yaiza, Lanzarote in the Canary Islands, in a house designed by her husband.
The Canary Islands are an autonomous community of Spain, where Alexia's aunt, Queen Sofía, lives and first cousin, Felipe VI, lives and rules.



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
  AssignClass (e3ea46ba-4412-4bd5-bd59-5ba0f0295444)
 Call ID: e3ea46ba-4412-4bd5-bd59-5ba0f0295444
  Args:
    type: :Woman
    source: Alexia
  AssignClass (b7cb80b5-41ab-438a-a808-c697dad2d61f)
 Call ID: b7cb80b5-41ab-438a-a808-c697dad2d61f
  Args:
    type: :Man
    source: Constantine_II
  AssignClass (4b184d73-798f-4866-a079-ef03434fd439)
 Call ID: 4b184d73-798f-4866-a079-ef03434fd439
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (431aa07c-a031-4c0d-8d06-f1a654435edb)
 Call ID: 431aa07c-a031-4c0d-8d06-f1a654435edb
  Args:
    type: :Man
    source: Pavlos
  AssignClass (e7362db1-853f-4022-9a43-2b25839bb5b9)
 Call ID: e7362db1-853f-4022-9a43-2b25839bb5b9
  Args:
    type: :Man
    source: Carlos_Javier_Morales_Quintana
  AssignClass (6495092f-fcd8-4dcd-ae27-c86a2956384d)
 Call ID: 6495092f-fcd8-4dcd-ae27-c86a2956384d
  Args:
    source: Theodora
    type: :Woman
  AssignClass (a6ee04e2-e962-4457-8f9b-eb9791629ae8)
 Call ID: a6ee04e2-e962-4457-8f9b-eb9791629ae8
  Args:
    type: :Woman
    source: Maria-Olympia
  AssignClass (761ea37d-2ebf-4a5f-a8d1-2c13b77538c3)
 Call ID: 761ea37d-2ebf-4a5f-a8d1-2c13b77538c3
  Args:
    type: :Woman
    source: Mafalda
  AssignClass (e1972327-1794-4719-84aa-b83bca9f7a69)
 Call ID: e1972327-1794-4719-84aa-b83bca9f7a69
  Args:
    type: :Man
    source: Kyril
  AssignClass (d3df0e55-ed1a-45a5-988f-09ff6db1c1ed)
 Call ID: d3df0e55-ed1a-45a5-988f-09ff6db1c1ed
  Args:
    source: Simeon
    type: :Man
  AssignClass (b3b1e532-93dc-4494-9cee-b0b9439456f8)
 Call ID: b3b1e532-93dc-4494-9cee-b0b9439456f8
  Args:
    source: Ingrid
    type: :Woman
  AssignClass (8b667c13-dab3-4bb0-8c67-200af9040afe)
 Call ID: 8b667c13-dab3-4bb0-8c67-200af9040afe
  Args:
    source: Sofia
    type: :Woman
  AssignClass (b69f9f69-7462-423d-a536-b63232438910)
 Call ID: b69f9f69-7462-423d-a536-b63232438910
  Args:
    type: :Man
    source: Felipe_VI
  AddLiteral (2dcc12d6-b1ec-4010-abe9-79e3ac60a518)
 Call ID: 2dcc12d6-b1ec-4010-abe9-79e3ac60a518
  Args:
    relation: :hasBirthYear
    literal_value: 1965
    source: Alexia
    literal_type: xsd:integer
  AddTriple (2e4fefee-86a1-43af-8a60-40612c82162e)
 Call ID: 2e4fefee-86a1-43af-8a60-40612c82162e
  Args:
    source: Alexia
    target: Constantine_II
    relation: :hasFather
  AddTriple (549cc245-bd9c-42b9-94fe-f787ac614df0)
 Call ID: 549cc245-bd9c-42b9-94fe-f787ac614df0
  Args:
    target: Anne-Marie
    source: Alexia
    relation: :hasMother
  AddTriple (605dd4e7-0a02-4250-8071-19044f1fa27c)
 Call ID: 605dd4e7-0a02-4250-8071-19044f1fa27c
  Args:
    target: Alexia
    source: Pavlos
    relation: :isBrotherOf
  AddTriple (3b2e79ba-a0f3-4726-8779-68cf54a0d624)
 Call ID: 3b2e79ba-a0f3-4726-8779-68cf54a0d624
  Args:
    target: Constantine_II
    source: Pavlos
    relation: :hasFather
  AddTriple (35cb746e-4d8a-43ea-b0a6-60510825d3e6)
 Call ID: 35cb746e-4d8a-43ea-b0a6-60510825d3e6
  Args:
    relation: :hasMother
    source: Pavlos
    target: Anne-Marie
  AddLiteral (8bfd1cf5-a636-462b-ac5b-c5ca74c16d1c)
 Call ID: 8bfd1cf5-a636-462b-ac5b-c5ca74c16d1c
  Args:
    source: Alexia
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1999
  AddTriple (769d977c-e62f-4cb4-9a0e-0bc25a8dfe68)
 Call ID: 769d977c-e62f-4cb4-9a0e-0bc25a8dfe68
  Args:
    relation: :hasRelation
    target: Carlos_Javier_Morales_Quintana
    source: Alexia
  AddTriple (317852ec-58b5-4ea7-8547-9a56e304ada4)
 Call ID: 317852ec-58b5-4ea7-8547-9a56e304ada4
  Args:
    relation: :isSisterOf
    source: Theodora
    target: Alexia
  AddTriple (0c6dafc4-cc3c-4ba5-9b17-155f5d487826)
 Call ID: 0c6dafc4-cc3c-4ba5-9b17-155f5d487826
  Args:
    target: Constantine_II
    source: Theodora
    relation: :hasFather
  AddTriple (90b00ba9-b700-4409-9818-3cebc56d4a2a)
 Call ID: 90b00ba9-b700-4409-9818-3cebc56d4a2a
  Args:
    target: Anne-Marie
    source: Theodora
    relation: :hasMother
  AddTriple (b5a0bc04-5554-4773-85d0-e11da8503c70)
 Call ID: b5a0bc04-5554-4773-85d0-e11da8503c70
  Args:
    relation: :isMotherOf
    target: Alexia
    source: Anne-Marie
  AddTriple (00d2b2b0-8f90-41ff-b1b5-f2dae1463cd3)
 Call ID: 00d2b2b0-8f90-41ff-b1b5-f2dae1463cd3
  Args:
    relation: :isMotherOf
    target: Pavlos
    source: Anne-Marie
  AddTriple (658c72b6-06b7-4dd0-8e02-4afc2b5295aa)
 Call ID: 658c72b6-06b7-4dd0-8e02-4afc2b5295aa
  Args:
    target: Theodora
    source: Anne-Marie
    relation: :isMotherOf
  AddTriple (26718652-6d7c-4465-8cff-c54a887912da)
 Call ID: 26718652-6d7c-4465-8cff-c54a887912da
  Args:
    target: Alexia
    source: Constantine_II
    relation: :isFatherOf
  AddTriple (5d428a69-fa9f-454b-a43b-1f17c4d77cfd)
 Call ID: 5d428a69-fa9f-454b-a43b-1f17c4d77cfd
  Args:
    target: Pavlos
    source: Constantine_II
    relation: :isFatherOf
  AddTriple (fb3d0c49-5c51-4861-b49e-8abbd0612a60)
 Call ID: fb3d0c49-5c51-4861-b49e-8abbd0612a60
  Args:
    target: Theodora
    source: Constantine_II
    relation: :isFatherOf
  AddTriple (081b327b-8073-4d77-afa6-b15d65ba564a)
 Call ID: 081b327b-8073-4d77-afa6-b15d65ba564a
  Args:
    relation: :isMotherOf
    target: Anne-Marie
    source: Ingrid
  AddTriple (44e46088-482c-471f-8eb2-c476684858ce)
 Call ID: 44e46088-482c-471f-8eb2-c476684858ce
  Args:
    relation: :isDaughterOf
    source: Mafalda
    target: Kyril
  AddTriple (91e52ce5-7280-402f-94dc-8b4c9adf5cba)
 Call ID: 91e52ce5-7280-402f-94dc-8b4c9adf5cba
  Args:
    source: Kyril
    target: Simeon
    relation: :isSonOf
  AddTriple (c715a379-f83b-4a59-859f-6c9f08c7e0dd)
 Call ID: c715a379-f83b-4a59-859f-6c9f08c7e0dd
  Args:
    source: Sofia
    target: Alexia
    relation: :isAuntOf
  Finish (e3b9496a-0c24-4683-87cd-29e1b01b643e)
 Call ID: e3b9496a-0c24-4683-87cd-29e1b01b643e
  Args: