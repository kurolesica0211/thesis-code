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
George Ivar Louis Mountbatten, 4th Marquess of Milford Haven (born 6 June 1961), styled Earl of Medina before 1970, is a British hereditary peer and businessman.
Biography

Family

Born on 6 June 1961, Lord Milford Haven is the elder son of the 3rd Marquess of Milford Haven and Janet Mercedes Bryce, the older brother of Lord Ivar Mountbatten, and a descendant of Queen Victoria, Catherine the Great, Alexander Pushkin, and Abram Gannibal.
Upon the death of his father on 14 April 1970, he became the 4th Marquess of Milford Haven and head of the Mountbatten family.
Lord Milford Haven married, first, Sarah Georgina Walker (born London, Middlesex, 17 November 1961/2), in London on 8 March 1989.
She is the daughter of Jean Maureen (née Hatton) and George Alfred Walker.
Lord Milford Haven and Walker had two children:


The couple divorced on 27 February 1996.
In June 2016, Walker married Michael Spencer, Lord Spencer of Alresford.
Lord Milford Haven subsequently married Clare Husted Steel at Coatue Point in Nantucket, Massachusetts, on 20 August 1997.
Career

In 2000, Lord Milford Haven founded uSwitch, a website to help consumers compare and change suppliers of various services.
Lord Milford Haven won the Queen's Cup with the Broncos team in 1988 and he reached the final in 2006.



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
  AssignClass (478277c0-08ba-45bb-9120-c220b5f458b2)
 Call ID: 478277c0-08ba-45bb-9120-c220b5f458b2
  Args:
    source: George_Ivar_Louis_Mountbatten
    type: :Man
  AssignClass (a8a5f718-bd58-421b-875e-1926a3b067c4)
 Call ID: a8a5f718-bd58-421b-875e-1926a3b067c4
  Args:
    type: :Person
    source: George_Ivar_Louis_Mountbatten
  AddLiteral (bae8feb8-a9ae-4a6f-acc5-269aa588e761)
 Call ID: bae8feb8-a9ae-4a6f-acc5-269aa588e761
  Args:
    source: George_Ivar_Louis_Mountbatten
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1961
  AssignClass (cecd2923-2b23-4cdf-956c-e515170d1c63)
 Call ID: cecd2923-2b23-4cdf-956c-e515170d1c63
  Args:
    type: :Woman
    source: Janet_Mercedes_Bryce
  AssignClass (e92e9cdc-0032-4712-a9a6-d08fcf827963)
 Call ID: e92e9cdc-0032-4712-a9a6-d08fcf827963
  Args:
    type: :Person
    source: Janet_Mercedes_Bryce
  AddTriple (48b85d73-08c1-432b-b88b-4ede362ed666)
 Call ID: 48b85d73-08c1-432b-b88b-4ede362ed666
  Args:
    source: George_Ivar_Louis_Mountbatten
    target: Janet_Mercedes_Bryce
    relation: :hasMother
  AssignClass (131d8f92-24d4-4fb4-ade5-91761446631a)
 Call ID: 131d8f92-24d4-4fb4-ade5-91761446631a
  Args:
    type: :Man
    source: 3rd_Marquess_of_Milford_Haven
  AssignClass (5a85262f-3174-459a-b942-411330287ab8)
 Call ID: 5a85262f-3174-459a-b942-411330287ab8
  Args:
    type: :Person
    source: 3rd_Marquess_of_Milford_Haven
  AddTriple (5ec5791b-af93-48ba-9166-fa0aaa2b0d5a)
 Call ID: 5ec5791b-af93-48ba-9166-fa0aaa2b0d5a
  Args:
    relation: :hasFather
    target: 3rd_Marquess_of_Milford_Haven
    source: George_Ivar_Louis_Mountbatten
  AssignClass (7c86f012-d7d8-41b9-831f-e0419f7879e9)
 Call ID: 7c86f012-d7d8-41b9-831f-e0419f7879e9
  Args:
    source: Lord_Ivar_Mountbatten
    type: :Man
  AssignClass (e62dba33-4fed-4d6d-a657-3d2dc9685314)
 Call ID: e62dba33-4fed-4d6d-a657-3d2dc9685314
  Args:
    source: Lord_Ivar_Mountbatten
    type: :Person
  AddTriple (28168182-b764-4ae3-8d4c-2e4c3fc5fed3)
 Call ID: 28168182-b764-4ae3-8d4c-2e4c3fc5fed3
  Args:
    source: George_Ivar_Louis_Mountbatten
    relation: :hasBrother
    target: Lord_Ivar_Mountbatten
  AssignClass (fef17cca-2e14-495d-9e56-c910369d9987)
 Call ID: fef17cca-2e14-495d-9e56-c910369d9987
  Args:
    source: Sarah_Georgina_Walker
    type: :Woman
  AssignClass (d893145c-fd59-400e-876c-46543e64fa64)
 Call ID: d893145c-fd59-400e-876c-46543e64fa64
  Args:
    type: :Person
    source: Sarah_Georgina_Walker
  AddLiteral (7a238953-139e-41db-aa17-27434c1aab07)
 Call ID: 7a238953-139e-41db-aa17-27434c1aab07
  Args:
    relation: :hasMarriageYear
    literal_value: 1989
    source: George_Ivar_Louis_Mountbatten
    literal_type: xsd:integer
  AssignClass (075bbac9-7001-4fb9-9629-876e4d7026a6)
 Call ID: 075bbac9-7001-4fb9-9629-876e4d7026a6
  Args:
    type: :Woman
    source: Jean_Maureen_Hatton
  AssignClass (0fa28232-209f-46f0-b02c-7e60029fe3d7)
 Call ID: 0fa28232-209f-46f0-b02c-7e60029fe3d7
  Args:
    source: Jean_Maureen_Hatton
    type: :Person
  AssignClass (b6ca56ff-0ab5-44c6-a812-867afa52c7a9)
 Call ID: b6ca56ff-0ab5-44c6-a812-867afa52c7a9
  Args:
    type: :Man
    source: George_Alfred_Walker
  AssignClass (eacfc41c-a028-4bcf-9ae1-cec7bfd89670)
 Call ID: eacfc41c-a028-4bcf-9ae1-cec7bfd89670
  Args:
    source: George_Alfred_Walker
    type: :Person
  AddTriple (3cd9c486-8bac-4627-91bf-c4beda2ebaf5)
 Call ID: 3cd9c486-8bac-4627-91bf-c4beda2ebaf5
  Args:
    relation: :hasMother
    target: Jean_Maureen_Hatton
    source: Sarah_Georgina_Walker
  AddTriple (c79fbf83-ccca-47d5-a37d-ec92b832b5ea)
 Call ID: c79fbf83-ccca-47d5-a37d-ec92b832b5ea
  Args:
    target: George_Alfred_Walker
    relation: :hasFather
    source: Sarah_Georgina_Walker
  AssignClass (b9a86bb1-a1c5-455a-bee7-b6011c110db7)
 Call ID: b9a86bb1-a1c5-455a-bee7-b6011c110db7
  Args:
    source: Clare_Husted_Steel
    type: :Woman
  AssignClass (414f5f76-4a29-4bba-b04c-7656caff4675)
 Call ID: 414f5f76-4a29-4bba-b04c-7656caff4675
  Args:
    source: Clare_Husted_Steel
    type: :Person
  AddLiteral (f1ebf434-6e01-474d-81a2-218adc09eea9)
 Call ID: f1ebf434-6e01-474d-81a2-218adc09eea9
  Args:
    relation: :hasMarriageYear
    literal_value: 1997
    source: George_Ivar_Louis_Mountbatten
    literal_type: xsd:integer
  AssignClass (fff8a72c-569a-4101-82f4-4594bb49593f)
 Call ID: fff8a72c-569a-4101-82f4-4594bb49593f
  Args:
    type: :Man
    source: Michael_Spencer
  AssignClass (8d3d7f98-cd87-4008-ac31-3e81ea6f17fe)
 Call ID: 8d3d7f98-cd87-4008-ac31-3e81ea6f17fe
  Args:
    source: Michael_Spencer
    type: :Person
  Finish (b9d06af8-f158-446a-b41c-eae9a3dc6ba7)
 Call ID: b9d06af8-f158-446a-b41c-eae9a3dc6ba7
  Args: