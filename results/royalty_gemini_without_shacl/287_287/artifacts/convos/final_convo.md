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
Lady Rose Victoria Birgitte Louise Gilman (née Windsor; born 1 March 1980) is a British film art assistant and member of the British royal family.
She is the daughter of Prince Richard, Duke of Gloucester, and his wife Birgitte, Duchess of Gloucester.
Early life and education

Rose Victoria Birgitte Louise Windsor was born on 1 March 1980 at St Mary's Hospital, London, the youngest child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents included Prince Edward and Lady Sarah Armstrong-Jones.
Career

Rose has worked in the film industry as a film art assistant.
Her film credits include Harry Potter and the Order of the Phoenix, Harry Potter and the Half-Blood Prince, Margaret Thatcher: The Long Walk to Finchley, and the television series Little Britain.
Rose continues to make public appearances at state events alongside other members of the extended royal family, including the 2022 state funeral of Queen Elizabeth II and the 2023 coronation of King Charles III and Queen Camilla.
Marriage and children

Rose announced her engagement on 16 November 2007 to businessman George Gilman, the son of a former director of Leeds United.
Rose and her husband have a daughter, Lyla (born 30 May 2010, then 32nd in line of succession to the British throne), and a son, Rufus (born 30 October 2012, then 33rd in line of succession to the British throne).



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
  AssignClass (359f0bd3-6171-40ed-82f6-152ea68d4469)
 Call ID: 359f0bd3-6171-40ed-82f6-152ea68d4469
  Args:
    type: :Woman
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
  AssignClass (cfb5fdb6-e2dd-474c-b278-b91b87d0c8dc)
 Call ID: cfb5fdb6-e2dd-474c-b278-b91b87d0c8dc
  Args:
    type: :Person
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
  AssignClass (08078da6-65d4-4079-877d-20578e980d17)
 Call ID: 08078da6-65d4-4079-877d-20578e980d17
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    type: :Man
  AssignClass (ff5998d4-45d6-4fb7-acb7-db7ed4f83970)
 Call ID: ff5998d4-45d6-4fb7-acb7-db7ed4f83970
  Args:
    type: :Person
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (09c8e51d-4ae3-4d64-bdd6-322d59bf5f0c)
 Call ID: 09c8e51d-4ae3-4d64-bdd6-322d59bf5f0c
  Args:
    source: Birgitte_Duchess_of_Gloucester
    type: :Woman
  AssignClass (2a0ed9b7-1154-4dd6-bbbe-43c636691180)
 Call ID: 2a0ed9b7-1154-4dd6-bbbe-43c636691180
  Args:
    source: Birgitte_Duchess_of_Gloucester
    type: :Person
  AssignClass (a29d90a6-96da-4fd7-be47-8bf37e44ee1e)
 Call ID: a29d90a6-96da-4fd7-be47-8bf37e44ee1e
  Args:
    type: :Man
    source: George_Gilman
  AssignClass (dda5ca5c-8421-477d-bbdb-1eda8259612b)
 Call ID: dda5ca5c-8421-477d-bbdb-1eda8259612b
  Args:
    type: :Person
    source: George_Gilman
  AssignClass (963f4d14-2dc7-4193-90a5-3e798f8f76bb)
 Call ID: 963f4d14-2dc7-4193-90a5-3e798f8f76bb
  Args:
    type: :Woman
    source: Lyla_Gilman
  AssignClass (4c83f31e-ef50-47e8-8361-f09295c50d2a)
 Call ID: 4c83f31e-ef50-47e8-8361-f09295c50d2a
  Args:
    source: Lyla_Gilman
    type: :Person
  AssignClass (d3f724cb-7125-49ae-a19d-34462ffa1530)
 Call ID: d3f724cb-7125-49ae-a19d-34462ffa1530
  Args:
    type: :Man
    source: Rufus_Gilman
  AssignClass (0ca01b6a-b155-4d3e-a79d-48938fa998c6)
 Call ID: 0ca01b6a-b155-4d3e-a79d-48938fa998c6
  Args:
    type: :Person
    source: Rufus_Gilman
  AddLiteral (ef036570-2c64-4ba4-a1ea-f8fe6f5a5822)
 Call ID: ef036570-2c64-4ba4-a1ea-f8fe6f5a5822
  Args:
    relation: :hasBirthYear
    literal_value: 1980
    literal_type: xsd:integer
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
  AddTriple (d6697ce6-0b1c-4805-b659-1d853a3ef9cc)
 Call ID: d6697ce6-0b1c-4805-b659-1d853a3ef9cc
  Args:
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
    relation: :hasFather
    target: Prince_Richard_Duke_of_Gloucester
  AddTriple (d2edf662-3175-4bdb-a054-22d37bbb7399)
 Call ID: d2edf662-3175-4bdb-a054-22d37bbb7399
  Args:
    relation: :hasMother
    target: Birgitte_Duchess_of_Gloucester
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
  AddLiteral (eef0beed-eb16-4074-a073-e9dd489a180e)
 Call ID: eef0beed-eb16-4074-a073-e9dd489a180e
  Args:
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 2007
  AddTriple (2a7674ee-11c9-4c68-a442-cb1bf5880a1a)
 Call ID: 2a7674ee-11c9-4c68-a442-cb1bf5880a1a
  Args:
    relation: :hasRelation
    target: George_Gilman
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
  AddTriple (0105f450-6540-4594-b783-9c8f496fffb5)
 Call ID: 0105f450-6540-4594-b783-9c8f496fffb5
  Args:
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
    target: Lyla_Gilman
    relation: :hasDaughter
  AddTriple (d0ba38fa-c351-4b4a-8932-c317cf56285c)
 Call ID: d0ba38fa-c351-4b4a-8932-c317cf56285c
  Args:
    source: George_Gilman
    relation: :hasDaughter
    target: Lyla_Gilman
  AddTriple (5dae2387-f249-4edf-badf-bb584fb35f18)
 Call ID: 5dae2387-f249-4edf-badf-bb584fb35f18
  Args:
    source: Lady_Rose_Victoria_Birgitte_Louise_Gilman
    target: Rufus_Gilman
    relation: :hasSon
  AddTriple (ddc4d231-cc26-407f-8e4a-8d70d8cadf1d)
 Call ID: ddc4d231-cc26-407f-8e4a-8d70d8cadf1d
  Args:
    source: George_Gilman
    target: Rufus_Gilman
    relation: :hasSon
  Finish (89d71fd1-2e83-4c5b-a187-b8636446de1f)
 Call ID: 89d71fd1-2e83-4c5b-a187-b8636446de1f
  Args: