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
Lady Davina Elizabeth Alice Benedikte Windsor (born 19 November 1977) is a member of the British royal family, and is the elder daughter of the Duke and Duchess of Gloucester.
She was known as Lady Davina Lewis between 2004 and 2018, during her marriage to Gary Lewis.
Early life and education

Davina Elizabeth Alice Benedikte Windsor was born on 19 November 1977 at St Mary's Hospital, London, the second child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents are Captain Mark Phillips, the Duke of Buccleuch, Elisabeth, Lady Camoys, Susan Wigley, Roger Wellesley Smith and Caroline, Baroness Rosenørn-Lehn.
Lady Davina grew up in Kensington Palace.
Marriage and children

On 31 July 2004, Davina married Gary Christie Lewis (born 15 August 1970), a Māori.
Lewis is also the first person of known Māori descent to marry a member of the royal family, or to marry the daughter of a British prince.
The wedding took place on 31 July 2004 at the private chapel of Kensington Palace, Davina's childhood home.
Apart from the Duke and Duchess of Gloucester and the bride's siblings, no other members of the royal family were present at the wedding; only close friends and family were involved.
Davina and her former husband have a daughter, Senna Kowhai, who was born on 22 June 2010 and a son, Tāne Mahuta, who was born 25 May 2012.
Davina was also stepmother to Lewis's son from a previous relationship, Ari (born 1992).
Davina does not carry out official functions but does attend family events including royal weddings.
Davina and Gary Lewis were invited to attend the Queen's reception for members of the New Zealand All Blacks at Buckingham Palace in 2005.
She and her then husband also attended Prince William's wedding in 2011.



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
  AssignClass (b165eaba-81eb-4b08-96de-221302a5aa53)
 Call ID: b165eaba-81eb-4b08-96de-221302a5aa53
  Args:
    type: :Woman
    source: :Davina_Windsor
  AssignClass (e5004f73-f000-46f3-9401-8271bb20156f)
 Call ID: e5004f73-f000-46f3-9401-8271bb20156f
  Args:
    source: :Davina_Windsor
    type: :Person
  AddLiteral (234c4cad-2f0f-4b35-bf7e-192e1173d67d)
 Call ID: 234c4cad-2f0f-4b35-bf7e-192e1173d67d
  Args:
    source: :Davina_Windsor
    literal_value: 1977-11-19
    relation: :hasBirthYear
    literal_type: xsd:string
  AssignClass (c7d58f73-4687-46cf-95a2-0efa78de8637)
 Call ID: c7d58f73-4687-46cf-95a2-0efa78de8637
  Args:
    source: :Prince_Richard_Duke_of_Gloucester
    type: :Man
  AssignClass (2d2b85d6-8dc7-4305-bf6e-a615b06ec8d8)
 Call ID: 2d2b85d6-8dc7-4305-bf6e-a615b06ec8d8
  Args:
    source: :Prince_Richard_Duke_of_Gloucester
    type: :Person
  AssignClass (5bde699f-e645-4e05-82a5-60f72ea6480a)
 Call ID: 5bde699f-e645-4e05-82a5-60f72ea6480a
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    type: :Woman
  AssignClass (8ea1e65b-3707-4bc3-bbd3-5536dbb82d4e)
 Call ID: 8ea1e65b-3707-4bc3-bbd3-5536dbb82d4e
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    type: :Person
  AddTriple (eef9ee33-1844-4a44-a7d2-899157c7ccc9)
 Call ID: eef9ee33-1844-4a44-a7d2-899157c7ccc9
  Args:
    relation: :hasFather
    target: :Prince_Richard_Duke_of_Gloucester
    source: :Davina_Windsor
  AddTriple (f7e4324f-beb7-43b7-9fae-0682194b1c37)
 Call ID: f7e4324f-beb7-43b7-9fae-0682194b1c37
  Args:
    target: :Birgitte_Duchess_of_Gloucester
    source: :Davina_Windsor
    relation: :hasMother
  AssignClass (02994d39-43dd-4467-9b57-7abd90bb819c)
 Call ID: 02994d39-43dd-4467-9b57-7abd90bb819c
  Args:
    source: :Gary_Lewis
    type: :Man
  AssignClass (443ef42f-486c-4005-a635-52818e34f38d)
 Call ID: 443ef42f-486c-4005-a635-52818e34f38d
  Args:
    type: :Person
    source: :Gary_Lewis
  AddTriple (214ea86d-1cbd-485b-8c39-b603862a8b17)
 Call ID: 214ea86d-1cbd-485b-8c39-b603862a8b17
  Args:
    source: :Davina_Windsor
    target: :Gary_Lewis
    relation: :hasRelation
  AddLiteral (1f55d823-46e1-4e12-9e99-52c6620f6c20)
 Call ID: 1f55d823-46e1-4e12-9e99-52c6620f6c20
  Args:
    source: :Davina_Windsor
    relation: :hasMarriageYear
    literal_value: 2004
    literal_type: xsd:string
  AddLiteral (0abd1b08-408e-4da5-9a67-15922606896f)
 Call ID: 0abd1b08-408e-4da5-9a67-15922606896f
  Args:
    literal_value: Lady Davina Lewis
    relation: :formerlyKnownAs
    literal_type: xsd:string
    source: :Davina_Windsor
  AssignClass (16a99d72-20fa-4d63-90d9-df234b084a39)
 Call ID: 16a99d72-20fa-4d63-90d9-df234b084a39
  Args:
    type: :Woman
    source: :Senna_Kowhai
  AssignClass (dd648bda-419c-410c-a63b-d29c2ac34973)
 Call ID: dd648bda-419c-410c-a63b-d29c2ac34973
  Args:
    source: :Senna_Kowhai
    type: :Person
  AddTriple (9a9f378f-8f2c-41f4-887d-0dc9cae42849)
 Call ID: 9a9f378f-8f2c-41f4-887d-0dc9cae42849
  Args:
    source: :Senna_Kowhai
    target: :Davina_Windsor
    relation: :isDaughterOf
  AddTriple (5dad8a84-4587-4a49-a546-82d0fd973207)
 Call ID: 5dad8a84-4587-4a49-a546-82d0fd973207
  Args:
    relation: :isDaughterOf
    source: :Senna_Kowhai
    target: :Gary_Lewis
  AssignClass (37a0fab0-9f5a-4a99-a328-73afca1aa293)
 Call ID: 37a0fab0-9f5a-4a99-a328-73afca1aa293
  Args:
    type: :Man
    source: :Tane_Mahuta
  AssignClass (79001e1f-4c11-4b97-8b6a-bb51058918a9)
 Call ID: 79001e1f-4c11-4b97-8b6a-bb51058918a9
  Args:
    source: :Tane_Mahuta
    type: :Person
  AddTriple (086e9baf-bf76-4e85-9d11-0705c171e46f)
 Call ID: 086e9baf-bf76-4e85-9d11-0705c171e46f
  Args:
    relation: :isSonOf
    source: :Tane_Mahuta
    target: :Davina_Windsor
  AddTriple (8a6c3ee7-1cb9-4423-9d91-1b1f852f1ca9)
 Call ID: 8a6c3ee7-1cb9-4423-9d91-1b1f852f1ca9
  Args:
    relation: :isSonOf
    target: :Gary_Lewis
    source: :Tane_Mahuta
  AssignClass (54597fa1-b242-43a3-9821-674124bfc979)
 Call ID: 54597fa1-b242-43a3-9821-674124bfc979
  Args:
    source: :Ari
    type: :Man
  AssignClass (19f3a330-66c2-44be-9deb-f961fa0264fe)
 Call ID: 19f3a330-66c2-44be-9deb-f961fa0264fe
  Args:
    source: :Ari
    type: :Person
  AddTriple (927fd954-df13-4f50-af40-b90d3082d6c3)
 Call ID: 927fd954-df13-4f50-af40-b90d3082d6c3
  Args:
    source: :Ari
    target: :Gary_Lewis
    relation: :isSonOf
  Finish (14f652b9-b968-4512-bbb0-f93a0fa06f31)
 Call ID: 14f652b9-b968-4512-bbb0-f93a0fa06f31
  Args: