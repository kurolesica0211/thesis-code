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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Countess Eloise of Orange-Nassau, Jonkvrouwe van Amsberg (Eloise Beatrix Sophie Laurence; born 8 June 2002), in the media often styled as simply Eloise van Oranje, is the first child and daughter of Prince Constantijn and Princess Laurentien of the Netherlands.
She is the first grandchild of Queen Beatrix and Prince Claus of the Netherlands.
Life

Countess Eloise was born in HMC Bronovo Hospital in The Hague.
The christening of Countess Eloise took place in the chapel of Het Loo Palace in Apeldoorn on 15 December 2002.
Her godparents were Crown Prince Haakon of Norway, Prince Johan Friso of the Netherlands, Princess Carolina de Bourbon de Parme and Sophie van de Wouw.
Style, titles and names

By royal decree of 11 May 2001 (nr. 227), it was determined that the children born from the marriage of Prince Constantijn and Princess Laurentien of the Netherlands would bear the title Count/Countess of Orange‐Nassau and the honorific Jonkheer/Jonkvrouwe van Amsberg with the surname Van Oranje-Nassau van Amsberg.
Upon the abdication of Queen Beatrix, which took place on 30 April 2013, the children of Prince Constantijn and Princess Laurentien ceased to be members of the royal house, although they continue to be members of the royal family.



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
  AssignClass (292fe862-4351-4c89-abe6-341104a89018)
 Call ID: 292fe862-4351-4c89-abe6-341104a89018
  Args:
    source: Beatrix
    type: :Person
  AssignClass (88e247d2-fa2f-4829-b0cf-ef236dae4ff9)
 Call ID: 88e247d2-fa2f-4829-b0cf-ef236dae4ff9
  Args:
    type: :Woman
    source: Beatrix
  AssignClass (af962e64-290f-4e4a-a329-41f59ca3027b)
 Call ID: af962e64-290f-4e4a-a329-41f59ca3027b
  Args:
    source: Margriet
    type: :Person
  AssignClass (5c302ab3-144f-452b-b0fa-16d6384fd02e)
 Call ID: 5c302ab3-144f-452b-b0fa-16d6384fd02e
  Args:
    source: Margriet
    type: :Woman
  AssignClass (a6237a40-c7ba-4c12-84e5-b9cc3f1b56a8)
 Call ID: a6237a40-c7ba-4c12-84e5-b9cc3f1b56a8
  Args:
    source: Pieter_van_Vollenhoven
    type: :Person
  AssignClass (507230b4-005f-405c-84e3-2a22991b3346)
 Call ID: 507230b4-005f-405c-84e3-2a22991b3346
  Args:
    type: :Man
    source: Pieter_van_Vollenhoven
  AssignClass (7998867a-816e-42f8-ad41-40badeb274a5)
 Call ID: 7998867a-816e-42f8-ad41-40badeb274a5
  Args:
    source: Eloise_van_Oranje
    type: :Person
  AssignClass (bd0e74de-d2be-4eae-b43d-a118bd52be9d)
 Call ID: bd0e74de-d2be-4eae-b43d-a118bd52be9d
  Args:
    type: :Woman
    source: Eloise_van_Oranje
  AssignClass (b47b3b59-a813-427b-aea6-388a96f27868)
 Call ID: b47b3b59-a813-427b-aea6-388a96f27868
  Args:
    type: :Person
    source: Constantijn
  AssignClass (ae22b3c3-7a7c-40a0-8054-7e5d5addc638)
 Call ID: ae22b3c3-7a7c-40a0-8054-7e5d5addc638
  Args:
    source: Constantijn
    type: :Man
  AssignClass (4f4d03fb-8659-46b9-9673-ee8cf6dbd9b5)
 Call ID: 4f4d03fb-8659-46b9-9673-ee8cf6dbd9b5
  Args:
    source: Laurentien
    type: :Person
  AssignClass (a26b1d42-dab5-4c03-8563-fd49ce43b84e)
 Call ID: a26b1d42-dab5-4c03-8563-fd49ce43b84e
  Args:
    type: :Woman
    source: Laurentien
  AssignClass (3523dde6-24f8-4f60-96b8-c3e48d0f80bd)
 Call ID: 3523dde6-24f8-4f60-96b8-c3e48d0f80bd
  Args:
    source: Claus
    type: :Person
  AssignClass (c8ed1254-e5c0-4c63-bcd2-401748248aec)
 Call ID: c8ed1254-e5c0-4c63-bcd2-401748248aec
  Args:
    source: Claus
    type: :Man
  AddLiteral (b3dbe998-e2ea-4c3b-9e51-c98bd660d6ad)
 Call ID: b3dbe998-e2ea-4c3b-9e51-c98bd660d6ad
  Args:
    literal_value: 2002
    relation: :hasBirthYear
    source: Eloise_van_Oranje
    literal_type: xsd:integer
  AddTriple (27171620-a428-43e4-94fa-345ec3de0393)
 Call ID: 27171620-a428-43e4-94fa-345ec3de0393
  Args:
    target: Constantijn
    source: Eloise_van_Oranje
    relation: :hasFather
  AddTriple (fd5d5651-962b-4859-b62c-484f1a0566f5)
 Call ID: fd5d5651-962b-4859-b62c-484f1a0566f5
  Args:
    source: Eloise_van_Oranje
    relation: :hasMother
    target: Laurentien
  AddTriple (21bfaf88-84c7-46f7-8d1e-4a98582251bd)
 Call ID: 21bfaf88-84c7-46f7-8d1e-4a98582251bd
  Args:
    source: Eloise_van_Oranje
    relation: :hasMother
    target: Beatrix
  AddTriple (533e7d16-0694-47bd-bef7-529eea8e8a50)
 Call ID: 533e7d16-0694-47bd-bef7-529eea8e8a50
  Args:
    target: Claus
    source: Eloise_van_Oranje
    relation: :hasFather
  AddLiteral (61a2cd28-48d7-4323-bf03-3ef4c559032f)
 Call ID: 61a2cd28-48d7-4323-bf03-3ef4c559032f
  Args:
    literal_value: Eloise van Oranje
    relation: :knownAs
    source: Eloise_van_Oranje
    literal_type: xsd:string
  Finish (d5c1a2a1-3b9d-4bda-9a49-2fdc38963d95)
 Call ID: d5c1a2a1-3b9d-4bda-9a49-2fdc38963d95
  Args: