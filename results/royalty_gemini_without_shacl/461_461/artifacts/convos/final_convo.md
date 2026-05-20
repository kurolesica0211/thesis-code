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
Lord Frederick Michael George David Louis Windsor (born 6 April 1979) is a member of the British royal family.
He is the only son of Prince and Princess Michael of Kent, and is 54th in the line of succession to the British throne.
He is married to British actress Sophie Winkleman and is a financial analyst by profession.
Early life and education

Frederick Michael George David Louis Windsor was born on 6 April 1979 at St Mary's Hospital, London, and was christened on 11 July at the Chapel Royal, St James's Palace, Westminster.
A first cousin once removed of Queen Elizabeth II and a first cousin twice removed of Prince Philip, Duke of Edinburgh, he is therefore both a second cousin and a second cousin once removed of King Charles III and his siblings.
Frederick and his sister, Lady Gabriella, were brought up in the Church of England.
Career

After graduating, Frederick worked as a fashion model, appearing in a campaign for Burberry and for the designer Tomasz Starzewski, and also as a music journalist, notably for Tatler magazine.
Personal life

On St Valentine's Day, 14 February 2009, Frederick became engaged to the actress Sophie Winkleman.
She was baptised at St James's Palace in December 2013 and has Princess Eugenie among her godparents.
Maud served as a bridesmaid at the wedding of Princess Eugenie and Jack Brooksbank in 2018.
On 20 January 2016, it was announced Frederick and Sophie had become parents to a second daughter, Isabella Alexandra May, who was born on 16 January 2016 at Chelsea and Westminster Hospital in London.
From September 2016 until its closure in 2023, Frederick was president of the charity Soldier On!, which supported vulnerable, disadvantaged, or socially isolated people through archaeology and heritage projects as well as personal development workshops.
On 21 February 2017, Frederick was inducted into the Grand Order of Water Rats charitable fraternity.
Titles and styles

Under letters patent issued in 1917 and still in force today, Frederick's father is entitled to the dignity of prince and the style His Royal Highness as the son of a son of George V. Although these letters do not bestow these royal dignities beyond grandchildren of monarchs (except in the case of the children of the Prince of Wales, as modified by Elizabeth II), they allow the children of sons of sons of a British monarch to be styled as the children of a duke, with the honorific courtesy style of Lord or Lady before their given names.
Since Lord Frederick is not a peer in his own right, his style is not hereditary and his children are not entitled to any distinctions, including the prefix The Honourable.



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
  AssignClass (49d77230-aca9-4ad2-b974-f12e8c459a4d)
 Call ID: 49d77230-aca9-4ad2-b974-f12e8c459a4d
  Args:
    type: :Man
    source: :FrederickWindsor
  AssignClass (7244798d-f205-41b5-a876-7f4c19855f81)
 Call ID: 7244798d-f205-41b5-a876-7f4c19855f81
  Args:
    type: :Person
    source: :FrederickWindsor
  AssignClass (47b0261a-554f-4763-bb84-81c82489771e)
 Call ID: 47b0261a-554f-4763-bb84-81c82489771e
  Args:
    source: :PrinceMichaelOfKent
    type: :Man
  AssignClass (6c8a8e19-089c-464f-b59f-cdafa628cb38)
 Call ID: 6c8a8e19-089c-464f-b59f-cdafa628cb38
  Args:
    source: :PrinceMichaelOfKent
    type: :Person
  AssignClass (d034eca4-ff9f-43d8-9ec4-f9c5f62324cc)
 Call ID: d034eca4-ff9f-43d8-9ec4-f9c5f62324cc
  Args:
    source: :PrincessMichaelOfKent
    type: :Woman
  AssignClass (a493ef50-139a-4068-a819-d45c6fba7594)
 Call ID: a493ef50-139a-4068-a819-d45c6fba7594
  Args:
    type: :Person
    source: :PrincessMichaelOfKent
  AssignClass (abd8bf0e-6de7-43bd-be01-a9033c5d5f73)
 Call ID: abd8bf0e-6de7-43bd-be01-a9033c5d5f73
  Args:
    source: :SophieWinkleman
    type: :Woman
  AssignClass (115b061b-7ff9-44bd-a51f-00e6a0d5c610)
 Call ID: 115b061b-7ff9-44bd-a51f-00e6a0d5c610
  Args:
    source: :SophieWinkleman
    type: :Person
  AssignClass (c23582ba-fe19-4b83-9ecb-8159c2e384c9)
 Call ID: c23582ba-fe19-4b83-9ecb-8159c2e384c9
  Args:
    source: :LadyGabriella
    type: :Woman
  AssignClass (5aba1413-0521-4af9-918b-505257f91878)
 Call ID: 5aba1413-0521-4af9-918b-505257f91878
  Args:
    type: :Person
    source: :LadyGabriella
  AssignClass (1f73422a-768d-4668-9b6e-5924aab648f6)
 Call ID: 1f73422a-768d-4668-9b6e-5924aab648f6
  Args:
    type: :Woman
    source: :IsabellaAlexandraMay
  AssignClass (5efc5b70-a42f-4bec-8924-4ea670c2b068)
 Call ID: 5efc5b70-a42f-4bec-8924-4ea670c2b068
  Args:
    source: :IsabellaAlexandraMay
    type: :Person
  AddLiteral (76ebb96e-2088-418b-a5a0-da86488e1648)
 Call ID: 76ebb96e-2088-418b-a5a0-da86488e1648
  Args:
    literal_value: 1979
    literal_type: xsd:integer
    source: :FrederickWindsor
    relation: :hasBirthYear
  AddTriple (d66c80ba-d88a-4d6b-a6a5-573a78ed69bc)
 Call ID: d66c80ba-d88a-4d6b-a6a5-573a78ed69bc
  Args:
    target: :PrinceMichaelOfKent
    relation: :hasFather
    source: :FrederickWindsor
  AddTriple (0dd27a81-30e2-4795-92cc-698e5af938e9)
 Call ID: 0dd27a81-30e2-4795-92cc-698e5af938e9
  Args:
    target: :PrincessMichaelOfKent
    relation: :hasMother
    source: :FrederickWindsor
  AddTriple (ccbdcccb-024c-4109-8f23-1ad0199ef1e8)
 Call ID: ccbdcccb-024c-4109-8f23-1ad0199ef1e8
  Args:
    relation: :hasSister
    target: :LadyGabriella
    source: :FrederickWindsor
  AddTriple (ed55d1d2-8972-4b3d-a242-33c33a5e74fe)
 Call ID: ed55d1d2-8972-4b3d-a242-33c33a5e74fe
  Args:
    relation: :isSisterOf
    target: :FrederickWindsor
    source: :LadyGabriella
  AddTriple (0e58ea78-eb34-4842-8d14-4224d86c7c71)
 Call ID: 0e58ea78-eb34-4842-8d14-4224d86c7c71
  Args:
    relation: :hasFather
    target: :PrinceMichaelOfKent
    source: :LadyGabriella
  AddTriple (d9214aa7-cff2-48d6-b93c-b8bd1dca3cbc)
 Call ID: d9214aa7-cff2-48d6-b93c-b8bd1dca3cbc
  Args:
    source: :LadyGabriella
    relation: :hasMother
    target: :PrincessMichaelOfKent
  AddTriple (a2d5da52-50b4-4331-b391-e8c5644693ec)
 Call ID: a2d5da52-50b4-4331-b391-e8c5644693ec
  Args:
    source: :PrinceMichaelOfKent
    relation: :isFatherOf
    target: :FrederickWindsor
  AddTriple (6a5bcfd1-9503-4b79-8331-9cfea9e53281)
 Call ID: 6a5bcfd1-9503-4b79-8331-9cfea9e53281
  Args:
    relation: :isFatherOf
    target: :LadyGabriella
    source: :PrinceMichaelOfKent
  AddTriple (feea441f-a029-4868-bcd5-e880e12305ab)
 Call ID: feea441f-a029-4868-bcd5-e880e12305ab
  Args:
    relation: :isMotherOf
    target: :FrederickWindsor
    source: :PrincessMichaelOfKent
  AddTriple (652f234d-1f21-4abe-92fe-c8be5c9cb71a)
 Call ID: 652f234d-1f21-4abe-92fe-c8be5c9cb71a
  Args:
    source: :PrincessMichaelOfKent
    relation: :isMotherOf
    target: :LadyGabriella
  AddTriple (cafcfc89-a464-4e43-b1fb-fb0c53e83054)
 Call ID: cafcfc89-a464-4e43-b1fb-fb0c53e83054
  Args:
    source: :IsabellaAlexandraMay
    target: :FrederickWindsor
    relation: :hasFather
  AddTriple (4582cb6a-0e1b-44b6-9b30-299accc9aa95)
 Call ID: 4582cb6a-0e1b-44b6-9b30-299accc9aa95
  Args:
    source: :IsabellaAlexandraMay
    relation: :hasMother
    target: :SophieWinkleman
  AddTriple (82d216ce-a916-4ea1-a8c7-e32a99072814)
 Call ID: 82d216ce-a916-4ea1-a8c7-e32a99072814
  Args:
    source: :FrederickWindsor
    target: :IsabellaAlexandraMay
    relation: :isFatherOf
  AddTriple (b17a4f2f-21ea-416c-aefe-23f714eebbf2)
 Call ID: b17a4f2f-21ea-416c-aefe-23f714eebbf2
  Args:
    target: :IsabellaAlexandraMay
    relation: :isMotherOf
    source: :SophieWinkleman
  Finish (76a47118-f541-4789-ac3b-325e90680801)
 Call ID: 76a47118-f541-4789-ac3b-325e90680801
  Args: