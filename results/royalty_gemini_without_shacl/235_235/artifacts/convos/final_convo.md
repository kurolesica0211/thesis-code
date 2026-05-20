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
Princess Josephine of Denmark, Countess of Monpezat RE (Josephine Sophia Ivalo Mathilda; born 8 January 2011) is a member of the Danish royal family.
She is the fourth and youngest child of King Frederik X and Queen Mary, and the seventh grandchild of Queen Margrethe II and Prince Henrik.
She is the twin sister of Prince Vincent.
Josephine is fourth in line to the Danish throne, after her older siblings, Crown Prince Christian and Princess Isabella, and her elder twin brother, Prince Vincent.
Birth and christening

Queen Margrethe II


Josephine was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:56 am local time, 26 minutes after her twin brother.
Josephine and Vincent were baptised on 14 April at the Church of Holmen in central Copenhagen by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Princess Josephine wore a christening gown found among her great-grandmother Queen Ingrid's belongings, making her the first child of a future Danish monarch not to wear the Danish royal family's traditional christening gown (which was worn by her twin brother) since it was taken into use in 1870.
The Princess's name was announced as Josephine Sophia Ivalo Mathilda.
Her godparents are her paternal aunt, Princess Marie of Denmark; her maternal aunt, Patricia Bailey; as well as her parents' friends Prince Carlo, Duke of Castro, Count Bendt Wedell, Birgitte Handwerk and Josephine Rechner.
Public appearances and education

On 3 August 2014, during the family's official visit to Greenland, Josephine, her parents and siblings, took part in a tree planting in Qaqortoq's new poplar grove, Ivalos og Miniks Poppellund, named after Josephine and her brother who are known by their Greenlandic middle names in Greenland.
On 15 August 2017, Josephine and her twin brother started school at Tranegårdsskolen in Gentofte – the same public school as her older siblings.
In August 2023, the Royal House announced that Josephine would be starting at Kildegård Privatskole in Hellerup in September 2023.
Both Josephine and her twin brother were confirmed on 18 April 2026.
Titles, styles, and honours

Josephine is styled as Her Royal Highness Princess Josephine of Denmark, Countess of Monpezat.



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
  AssignClass (1014b687-b8de-4863-9984-574f781ab568)
 Call ID: 1014b687-b8de-4863-9984-574f781ab568
  Args:
    type: :Person
    source: Princess_Josephine_of_Denmark
  AssignClass (a9149b00-3952-4a4c-be6b-55b35a338af2)
 Call ID: a9149b00-3952-4a4c-be6b-55b35a338af2
  Args:
    source: Princess_Josephine_of_Denmark
    type: :Woman
  AssignClass (1f022582-eccb-4f8a-b958-0d3cdf37ba26)
 Call ID: 1f022582-eccb-4f8a-b958-0d3cdf37ba26
  Args:
    type: :Person
    source: King_Frederik_X
  AssignClass (ba86f6b0-9285-45cc-88dc-27211d98e293)
 Call ID: ba86f6b0-9285-45cc-88dc-27211d98e293
  Args:
    type: :Man
    source: King_Frederik_X
  AssignClass (536291f0-28ff-4304-bc86-dfd793bf991a)
 Call ID: 536291f0-28ff-4304-bc86-dfd793bf991a
  Args:
    source: King_Frederik_X
    type: :Ancestor
  AssignClass (9dcda567-3165-4ba5-93b2-dd0f8458e201)
 Call ID: 9dcda567-3165-4ba5-93b2-dd0f8458e201
  Args:
    type: :Person
    source: Queen_Mary
  AssignClass (11d41ae2-6011-48eb-a6e2-bc73d0fd7725)
 Call ID: 11d41ae2-6011-48eb-a6e2-bc73d0fd7725
  Args:
    source: Queen_Mary
    type: :Woman
  AssignClass (3d05b39c-a178-4104-a82f-a7f265959bc7)
 Call ID: 3d05b39c-a178-4104-a82f-a7f265959bc7
  Args:
    source: Queen_Mary
    type: :Ancestor
  AssignClass (4123db0d-a138-463c-9746-5c965834269f)
 Call ID: 4123db0d-a138-463c-9746-5c965834269f
  Args:
    source: Prince_Vincent
    type: :Person
  AssignClass (90d02e8e-5333-4076-a7f3-4963314bfb56)
 Call ID: 90d02e8e-5333-4076-a7f3-4963314bfb56
  Args:
    type: :Man
    source: Prince_Vincent
  AssignClass (452ce515-9039-4cf1-9481-4085342ecf62)
 Call ID: 452ce515-9039-4cf1-9481-4085342ecf62
  Args:
    type: :Person
    source: Queen_Margrethe_II
  AssignClass (d70aca3d-45ea-4f90-abbb-61891fbf5b93)
 Call ID: d70aca3d-45ea-4f90-abbb-61891fbf5b93
  Args:
    type: :Woman
    source: Queen_Margrethe_II
  AssignClass (40749f2a-77d5-4ed9-8af9-d4acb0d94241)
 Call ID: 40749f2a-77d5-4ed9-8af9-d4acb0d94241
  Args:
    type: :Ancestor
    source: Queen_Margrethe_II
  AssignClass (6d9782c2-8ba1-4872-b043-8336f995f474)
 Call ID: 6d9782c2-8ba1-4872-b043-8336f995f474
  Args:
    source: Prince_Henrik
    type: :Person
  AssignClass (100bd116-7a4b-465c-b5a1-306f084d22e7)
 Call ID: 100bd116-7a4b-465c-b5a1-306f084d22e7
  Args:
    source: Prince_Henrik
    type: :Man
  AssignClass (c91af159-5f89-4b7e-862a-4c695ad2ec6d)
 Call ID: c91af159-5f89-4b7e-862a-4c695ad2ec6d
  Args:
    type: :Ancestor
    source: Prince_Henrik
  AddTriple (14524aa3-a0fa-46bd-81d8-70ce3e935aa0)
 Call ID: 14524aa3-a0fa-46bd-81d8-70ce3e935aa0
  Args:
    source: Princess_Josephine_of_Denmark
    target: King_Frederik_X
    relation: :hasFather
  AddTriple (490d1f7f-6ba9-41a1-8584-caadf6796d57)
 Call ID: 490d1f7f-6ba9-41a1-8584-caadf6796d57
  Args:
    source: Princess_Josephine_of_Denmark
    target: Queen_Mary
    relation: :hasMother
  AddTriple (ac794ad3-a060-47ff-b753-c23215abed97)
 Call ID: ac794ad3-a060-47ff-b753-c23215abed97
  Args:
    target: Prince_Vincent
    source: Princess_Josephine_of_Denmark
    relation: :hasBrother
  AddTriple (5477ada8-f7a4-4537-9792-f438b811f062)
 Call ID: 5477ada8-f7a4-4537-9792-f438b811f062
  Args:
    relation: :isSisterOf
    target: Prince_Vincent
    source: Princess_Josephine_of_Denmark
  AddLiteral (927f366d-878e-4fcc-b4db-dc43a3f34611)
 Call ID: 927f366d-878e-4fcc-b4db-dc43a3f34611
  Args:
    literal_value: 2011
    source: Princess_Josephine_of_Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (7b398dbb-370c-471c-963b-c2a6f4136f54)
 Call ID: 7b398dbb-370c-471c-963b-c2a6f4136f54
  Args:
    source: Prince_Vincent
    target: King_Frederik_X
    relation: :hasFather
  AddTriple (c99ed85d-c580-430a-938f-837925d8602b)
 Call ID: c99ed85d-c580-430a-938f-837925d8602b
  Args:
    source: Prince_Vincent
    target: Queen_Mary
    relation: :hasMother
  AddTriple (56b0dd6e-43d0-4fe4-9ba1-b039e5d71d1a)
 Call ID: 56b0dd6e-43d0-4fe4-9ba1-b039e5d71d1a
  Args:
    relation: :hasParent
    target: Queen_Margrethe_II
    source: King_Frederik_X
  AddTriple (06bde68a-6855-4b55-8bf7-2e1a06164f83)
 Call ID: 06bde68a-6855-4b55-8bf7-2e1a06164f83
  Args:
    relation: :hasParent
    source: King_Frederik_X
    target: Prince_Henrik
  Finish (7fe8fddc-141e-4e83-97c0-cdd40bb57ec7)
 Call ID: 7fe8fddc-141e-4e83-97c0-cdd40bb57ec7
  Args: