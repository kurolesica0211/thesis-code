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
  AssignClass (215beaf5-3647-4ad4-aa86-9bd39bdf09d0)
 Call ID: 215beaf5-3647-4ad4-aa86-9bd39bdf09d0
  Args:
    type: :Woman
    source: Alexia
  AssignClass (b6d76502-c4a1-48c2-8c9e-e53f6dddcbab)
 Call ID: b6d76502-c4a1-48c2-8c9e-e53f6dddcbab
  Args:
    source: Constantine_II
    type: :Man
  AssignClass (6c01e942-30dc-450b-bf7f-2542000fcf0a)
 Call ID: 6c01e942-30dc-450b-bf7f-2542000fcf0a
  Args:
    source: Anne-Marie
    type: :Woman
  AssignClass (99e84cac-fc9a-4952-89e0-8ada8893edcc)
 Call ID: 99e84cac-fc9a-4952-89e0-8ada8893edcc
  Args:
    source: Pavlos
    type: :Man
  AssignClass (bd6003af-5bd8-40f6-afe3-35dc56211fba)
 Call ID: bd6003af-5bd8-40f6-afe3-35dc56211fba
  Args:
    source: Carlos_Javier_Morales_Quintana
    type: :Man
  AssignClass (a7fb3714-b375-44f0-9cdf-4356cfaf140e)
 Call ID: a7fb3714-b375-44f0-9cdf-4356cfaf140e
  Args:
    type: :Woman
    source: Theodora
  AssignClass (87f852db-732c-4292-8904-fdc3cbd51989)
 Call ID: 87f852db-732c-4292-8904-fdc3cbd51989
  Args:
    source: Maria-Olympia
    type: :Woman
  AssignClass (8cf158bc-3c90-435d-abdf-165d21fb6844)
 Call ID: 8cf158bc-3c90-435d-abdf-165d21fb6844
  Args:
    type: :Woman
    source: Mafalda
  AssignClass (0322c81c-90b9-4cb2-b3a6-b5a533c0c39f)
 Call ID: 0322c81c-90b9-4cb2-b3a6-b5a533c0c39f
  Args:
    type: :Man
    source: Kyril
  AssignClass (6babbec8-2811-4571-bd5b-d9ae6bc81042)
 Call ID: 6babbec8-2811-4571-bd5b-d9ae6bc81042
  Args:
    source: Simeon
    type: :Man
  AssignClass (58e65dc5-5edc-4749-a3c9-4a9e36142198)
 Call ID: 58e65dc5-5edc-4749-a3c9-4a9e36142198
  Args:
    source: Ingrid
    type: :Woman
  AssignClass (1e04460c-95c1-425a-85f7-b0c4933baa2b)
 Call ID: 1e04460c-95c1-425a-85f7-b0c4933baa2b
  Args:
    type: :Woman
    source: Sofia
  AssignClass (c5117f59-232f-454f-8c77-14ad4477ad9f)
 Call ID: c5117f59-232f-454f-8c77-14ad4477ad9f
  Args:
    source: Felipe_VI
    type: :Man
  AssignClass (05a8d382-eba4-4554-9864-6be4f7c6092f)
 Call ID: 05a8d382-eba4-4554-9864-6be4f7c6092f
  Args:
    source: Michael
    type: :Man
  AssignClass (513f0f58-ab48-40a6-91ec-aae9dee2078c)
 Call ID: 513f0f58-ab48-40a6-91ec-aae9dee2078c
  Args:
    type: :Woman
    source: Marina
  AddLiteral (2745431e-a5fe-45a4-a515-128e8a652f79)
 Call ID: 2745431e-a5fe-45a4-a515-128e8a652f79
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Alexia
    literal_value: 1965
  AddTriple (ce146ab0-f3b6-41a4-bc31-6f7b8e2bd54e)
 Call ID: ce146ab0-f3b6-41a4-bc31-6f7b8e2bd54e
  Args:
    target: Constantine_II
    relation: :hasFather
    source: Alexia
  AddTriple (7b41bb56-6718-4f3d-be50-8a0494568e54)
 Call ID: 7b41bb56-6718-4f3d-be50-8a0494568e54
  Args:
    source: Alexia
    target: Anne-Marie
    relation: :hasMother
  AddTriple (c3985780-690b-4322-8bd5-935fa4604e68)
 Call ID: c3985780-690b-4322-8bd5-935fa4604e68
  Args:
    source: Pavlos
    relation: :isBrotherOf
    target: Alexia
  AddTriple (6a8c7cbc-bc42-4c37-ad8e-c47ebd516058)
 Call ID: 6a8c7cbc-bc42-4c37-ad8e-c47ebd516058
  Args:
    relation: :isSisterOf
    target: Alexia
    source: Theodora
  AddTriple (84d087b9-97d5-4bf9-9ea3-32dd8c92713c)
 Call ID: 84d087b9-97d5-4bf9-9ea3-32dd8c92713c
  Args:
    relation: :hasFather
    target: Constantine_II
    source: Alexia
  AddTriple (16ac7e74-21e8-4e58-ac8c-4099ffa079b6)
 Call ID: 16ac7e74-21e8-4e58-ac8c-4099ffa079b6
  Args:
    source: Alexia
    relation: :hasMother
    target: Anne-Marie
  AddTriple (28b5aa6b-744a-4b42-9d33-ad5ac5939a41)
 Call ID: 28b5aa6b-744a-4b42-9d33-ad5ac5939a41
  Args:
    source: Pavlos
    relation: :hasFather
    target: Constantine_II
  AddTriple (135cc5ab-928b-499e-9f18-d85f9d3d5872)
 Call ID: 135cc5ab-928b-499e-9f18-d85f9d3d5872
  Args:
    target: Anne-Marie
    relation: :hasMother
    source: Pavlos
  AddLiteral (dbe24535-51ca-4a0a-81d4-9b94fe979ca2)
 Call ID: dbe24535-51ca-4a0a-81d4-9b94fe979ca2
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1999
    source: Alexia
  AddTriple (b5304871-c2f2-49b5-a817-fd7d7441331d)
 Call ID: b5304871-c2f2-49b5-a817-fd7d7441331d
  Args:
    target: Carlos_Javier_Morales_Quintana
    relation: :hasRelation
    source: Alexia
  AddTriple (ef88f4c8-dae0-457f-857e-e4d8f3a19bca)
 Call ID: ef88f4c8-dae0-457f-857e-e4d8f3a19bca
  Args:
    source: Mafalda
    target: Kyril
    relation: :isDaughterOf
  AddTriple (c8b365c5-b311-49cf-972f-272a1be2c45b)
 Call ID: c8b365c5-b311-49cf-972f-272a1be2c45b
  Args:
    source: Kyril
    target: Simeon
    relation: :isSonOf
  AddTriple (abf02845-4e81-4dfb-9b46-e8141774d9ee)
 Call ID: abf02845-4e81-4dfb-9b46-e8141774d9ee
  Args:
    target: Anne-Marie
    relation: :isSisterOf
    source: Sofia
  AddTriple (87de5697-43eb-4a00-a551-48b9c98e918f)
 Call ID: 87de5697-43eb-4a00-a551-48b9c98e918f
  Args:
    target: Anne-Marie
    relation: :isSisterOf
    source: Ingrid
  AddTriple (bb589058-b7de-4c6d-993f-ca697135fd10)
 Call ID: bb589058-b7de-4c6d-993f-ca697135fd10
  Args:
    source: Sofia
    relation: :isSisterOf
    target: Alexia
  AddTriple (e98c8861-0810-4872-9f25-27d4cb140ed5)
 Call ID: e98c8861-0810-4872-9f25-27d4cb140ed5
  Args:
    source: Michael
    target: Marina
    relation: :isFatherOf
  Finish (e8fe5d0f-939b-4b7a-a4d2-4e802aab742e)
 Call ID: e8fe5d0f-939b-4b7a-a4d2-4e802aab742e
  Args: