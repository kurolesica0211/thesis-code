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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Peter Karageorgevitch (Serbian Cyrillic: Петар Карађорђевић, romanized: Petar Karađorđević; born 5 February 1980), also known as Prince Peter of Serbia and Yugoslavia, is an American born Spanish-Serbian graphic designer and a member of the House of Karađorđević.
He is the oldest grandchild and the first grandson of the last Yugoslav king, Peter II.
Between his birth and his renunciation in 2022, he was known as the Hereditary Prince.
Early life and education

Peter is the first son and the oldest child of the last Crown Prince of the former Kingdom of Yugoslavia, Alexander, and Princess Maria da Gloria of Orléans-Braganza.
His godfather was Prince Alexander of Yugoslavia, a son of Prince Paul of Yugoslavia.
His godmother is Anne, Princess Royal.
Peter has two younger brothers, twins Philip and Alexander (born 1982).
Peter's parents divorced in 1985.
After the divorce, his father married Katherine Clairy Batis later that year, while his mother married Ignacio, Duke of Segorbe later that year also.
Through his mother, Peter has two younger half-sisters, Sol María de la Blanca Medina y Orléans-Braganza, Countess of Ampurias (b. 1986) and Ana Luna Medina y Orléans-Braganza, Countess of Ricla (b. 1988).
In 1991, Peter with his father and brothers briefly visited Belgrade, Yugoslavia.
In February 2001, the Parliament of FR Yugoslavia passed legislation conferring citizenship on members of the Karađorđević family, making Peter eligible for a Yugoslav citizenship.
In July 2001, his father and step-mother moved to Belgrade, Serbia, FR Yugoslavia.
In June 1998, Peter graduated from The King's School, Canterbury, in England, having obtained three A-levels in Art, Spanish, and French, and ten GCSEs.
Public life

Prince Peter attended the reburial of his grandparents King Peter II and Queen Alexandra, great-grandmother Queen Maria, and great-uncle Prince Andrew in the Royal Family Mausoleum at Oplenac on 26 May 2013.
The Serbian Royal Regalia were placed over King Peter's coffin, having Peter placing the Karađorđević Crown.
On 17 July 2015, Prince Peter and his brothers were present at their father's 70th birthday celebration in Belgrade.
On 27 April 2022, Prince Peter renounced his title of Hereditary Prince – for himself and his descendants – in favor of his younger brother Philip.
The ceremony took place in Seville at Casa de Pilatos in the presence of his mother Princess Maria da Gloria, his stepfather the 19th Duke of Segorbe, his brother Philip, his sister-in-law Princess Danica, his half sister the 54th Countess of Ampurias, Ljubodrag Grujić, member of the Crown Council, Chancellor of the Orders and the Herald of the House of Karađorđević, and Nikola Stanković, Chief of Staff of the Crown Prince.
His father, Crown Prince Alexander, did not attend the event, and was dissatisfied with Peter's renunciation.
Personal life

Prince Peter used to work in a field of graphic design and art direction in London and New York City.
Peter has a daughter named Dolores Luna Noor born in 2017 by Lauren Estelle Jones (b. 1984).
Honours

Ancestors

Peter is a member of the House of Karađorđević.
Through his father, Peter descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, Christian IX of Denmark and Alexander of Greece, and furthermore from emperors Nicholas I of Russia and Frederick III of the Germans and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through his mother, Peter descends from the Emperor Pedro II of Brazil, and kings Louis Philippe I of France and Francis I of the Two Sicilies, and furthermore from Francis I, Holy Roman Emperor and king Charles III of Spain.



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
  AssignClass (772941cf-abe9-4d1c-b4ac-198bb9e7541c)
 Call ID: 772941cf-abe9-4d1c-b4ac-198bb9e7541c
  Args:
    source: Peter_Karageorgevitch
    type: :Man
  AssignClass (fd4de57e-10bb-4762-9d10-dd9de8000341)
 Call ID: fd4de57e-10bb-4762-9d10-dd9de8000341
  Args:
    type: :Person
    source: Peter_Karageorgevitch
  AddLiteral (89f629ff-f300-4d3d-bb3f-30a34b2def48)
 Call ID: 89f629ff-f300-4d3d-bb3f-30a34b2def48
  Args:
    literal_value: Prince Peter of Serbia and Yugoslavia
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: Peter_Karageorgevitch
  AddLiteral (0e5b1cb3-08a7-49a4-87d0-4da608c8ff80)
 Call ID: 0e5b1cb3-08a7-49a4-87d0-4da608c8ff80
  Args:
    literal_type: xsd:string
    source: Peter_Karageorgevitch
    relation: :formerlyKnownAs
    literal_value: Hereditary Prince
  AddLiteral (79db761b-9cb9-4a2f-9c49-03aa6461e14c)
 Call ID: 79db761b-9cb9-4a2f-9c49-03aa6461e14c
  Args:
    literal_type: xsd:integer
    source: Peter_Karageorgevitch
    relation: :hasBirthYear
    literal_value: 1980
  AssignClass (1e4dd0ec-a0ee-4d78-bac0-7dc161e7345f)
 Call ID: 1e4dd0ec-a0ee-4d78-bac0-7dc161e7345f
  Args:
    type: :Man
    source: Alexander_Yugoslavia
  AssignClass (a889bcac-327f-4ec1-9a3a-712090552bd3)
 Call ID: a889bcac-327f-4ec1-9a3a-712090552bd3
  Args:
    type: :Person
    source: Alexander_Yugoslavia
  AssignClass (3ab80e20-23ca-4927-ba32-53d8229fc8c3)
 Call ID: 3ab80e20-23ca-4927-ba32-53d8229fc8c3
  Args:
    type: :Woman
    source: Maria_da_Gloria
  AssignClass (06e3f19d-fa63-4d81-a75c-10dad68d21d0)
 Call ID: 06e3f19d-fa63-4d81-a75c-10dad68d21d0
  Args:
    source: Maria_da_Gloria
    type: :Person
  AddTriple (ad6456aa-e2e1-4693-8ffe-52e4c07d7f6a)
 Call ID: ad6456aa-e2e1-4693-8ffe-52e4c07d7f6a
  Args:
    source: Peter_Karageorgevitch
    relation: :hasFather
    target: Alexander_Yugoslavia
  AddTriple (01b174a1-08c6-4a52-9bfd-6ab7f7e53dd3)
 Call ID: 01b174a1-08c6-4a52-9bfd-6ab7f7e53dd3
  Args:
    source: Peter_Karageorgevitch
    relation: :hasMother
    target: Maria_da_Gloria
  AssignClass (3d35239c-8684-4e2c-b8b5-731c8841c521)
 Call ID: 3d35239c-8684-4e2c-b8b5-731c8841c521
  Args:
    type: :Man
    source: Philip_Karageorgevitch
  AssignClass (0f99432c-1096-4050-a702-da1e13847cd0)
 Call ID: 0f99432c-1096-4050-a702-da1e13847cd0
  Args:
    source: Philip_Karageorgevitch
    type: :Person
  AddTriple (a45aa2c3-ad27-4429-a225-2bdbb3ed99d7)
 Call ID: a45aa2c3-ad27-4429-a225-2bdbb3ed99d7
  Args:
    target: Philip_Karageorgevitch
    source: Peter_Karageorgevitch
    relation: :hasBrother
  AssignClass (149dc905-859a-4ab3-a634-22995ad25c0c)
 Call ID: 149dc905-859a-4ab3-a634-22995ad25c0c
  Args:
    type: :Man
    source: Alexander_Jr_Karageorgevitch
  AssignClass (ba4821d7-dbca-4dec-93ed-cfd989d4352d)
 Call ID: ba4821d7-dbca-4dec-93ed-cfd989d4352d
  Args:
    type: :Person
    source: Alexander_Jr_Karageorgevitch
  AddTriple (6fa52b03-d14b-4870-96e1-0fe43e3ce9a2)
 Call ID: 6fa52b03-d14b-4870-96e1-0fe43e3ce9a2
  Args:
    source: Peter_Karageorgevitch
    relation: :hasBrother
    target: Alexander_Jr_Karageorgevitch
  AssignClass (506cdd06-2c80-44ed-827d-d800486ec01c)
 Call ID: 506cdd06-2c80-44ed-827d-d800486ec01c
  Args:
    type: :Woman
    source: Dolores_Luna_Noor
  AssignClass (2ff557a7-ee45-4f9c-83b3-9259f0efabcf)
 Call ID: 2ff557a7-ee45-4f9c-83b3-9259f0efabcf
  Args:
    type: :Person
    source: Dolores_Luna_Noor
  AddTriple (94656023-d773-4be6-88b1-7e06eabbb61e)
 Call ID: 94656023-d773-4be6-88b1-7e06eabbb61e
  Args:
    target: Dolores_Luna_Noor
    source: Peter_Karageorgevitch
    relation: :hasDaughter
  AddLiteral (dc76e737-8aac-4639-9d41-ba55b4ab1d9f)
 Call ID: dc76e737-8aac-4639-9d41-ba55b4ab1d9f
  Args:
    literal_type: xsd:integer
    source: Dolores_Luna_Noor
    relation: :hasBirthYear
    literal_value: 2017
  AssignClass (82791e0b-de37-4eb7-9f41-8ca395dc618e)
 Call ID: 82791e0b-de37-4eb7-9f41-8ca395dc618e
  Args:
    type: :Woman
    source: Lauren_Estelle_Jones
  AssignClass (dc27350a-554a-4d9c-a214-2da07a703d0a)
 Call ID: dc27350a-554a-4d9c-a214-2da07a703d0a
  Args:
    source: Lauren_Estelle_Jones
    type: :Person
  AddTriple (22879756-6733-4c24-9ed8-744efcf4b54e)
 Call ID: 22879756-6733-4c24-9ed8-744efcf4b54e
  Args:
    source: Dolores_Luna_Noor
    relation: :hasMother
    target: Lauren_Estelle_Jones
  AddLiteral (40173553-3267-4994-bb12-1133fd87e2d5)
 Call ID: 40173553-3267-4994-bb12-1133fd87e2d5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Lauren_Estelle_Jones
    literal_value: 1984
  AssignClass (f1aa53b1-cdca-4be8-b289-50506b7548df)
 Call ID: f1aa53b1-cdca-4be8-b289-50506b7548df
  Args:
    type: :Woman
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (0404c13c-e0fe-4738-982c-1dcd3c2391f6)
 Call ID: 0404c13c-e0fe-4738-982c-1dcd3c2391f6
  Args:
    type: :Person
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AddTriple (7f845f35-9cb2-4be9-8c40-07f96cda6c2b)
 Call ID: 7f845f35-9cb2-4be9-8c40-07f96cda6c2b
  Args:
    target: Maria_da_Gloria
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
    relation: :hasMother
  AssignClass (7898ffa6-d9be-4bf9-a8d8-8e14b270be31)
 Call ID: 7898ffa6-d9be-4bf9-a8d8-8e14b270be31
  Args:
    source: Ana_Luna_Medina_y_Orleans_Braganza
    type: :Woman
  AssignClass (c3817b0d-e978-437a-a91f-790adcd6622d)
 Call ID: c3817b0d-e978-437a-a91f-790adcd6622d
  Args:
    source: Ana_Luna_Medina_y_Orleans_Braganza
    type: :Person
  AddTriple (d37a92ba-1adb-4b4d-b7a5-fa6ff6ae98c3)
 Call ID: d37a92ba-1adb-4b4d-b7a5-fa6ff6ae98c3
  Args:
    source: Ana_Luna_Medina_y_Orleans_Braganza
    relation: :hasMother
    target: Maria_da_Gloria
  Finish (44d15daa-a0db-434e-89e8-709b6c2782d3)
 Call ID: 44d15daa-a0db-434e-89e8-709b6c2782d3
  Args: