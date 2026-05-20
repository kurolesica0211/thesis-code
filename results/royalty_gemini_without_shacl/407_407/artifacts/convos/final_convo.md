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
Mary Frances Elphinstone, Lady Elphinstone GCVO (née Bowes-Lyon; 30 August 1883 – 8 February 1961), was a British aristocrat.
She was an elder sister of Queen Elizabeth the Queen Mother and an aunt and godmother of Queen Elizabeth II.
Early life

Lady Elphinstone was born The Honourable Mary Frances Bowes-Lyon on 30 August 1883 in Angus, Scotland, to Claude Bowes-Lyon, 14th
She was an elder sister of Elizabeth Bowes-Lyon known as Queen Elizabeth of the United Kingdom (later the Queen Mother).
Personal life

Lady Mary married Sidney Elphinstone, 16th Lord Elphinstone (1869–1955) on 24 July 1910 in Westminster.
Lord Elphinstone inherited extensive estates, some of which had been in the family since the reign of King David II of Scotland.
He served as a governor of the Bank of Scotland, Lord Clerk Register of Scotland and Keeper of the Signet and Lord High Commissioner of the Church of Scotland.
The couple had five children:


In 1937, Lady Elphinstone attended her sister and brother-in-law's coronation whereby she sat behind her niece Princess Elizabeth, who would be the future queen, in the royal box.
She was one of the leading guests in the wedding of Princess Elizabeth and Philip Mountbatten in 1947.
Lord Elphinstone died at their home Carberry Tower, Musselburgh, on 28 November 1955.
Lady Elphinstone, who served as president of the Midlothian branch of the British Red Cross, died on 8 February 1961, aged 77, also at Carberry Tower in Inveresk, Scotland.



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
  AssignClass (8e564749-5778-49a6-aafe-833594e66766)
 Call ID: 8e564749-5778-49a6-aafe-833594e66766
  Args:
    type: :Woman
    source: :Mary_Frances_Elphinstone
  AssignClass (beaa0218-ffc9-43fb-b4c6-5e9e9c44d6b0)
 Call ID: beaa0218-ffc9-43fb-b4c6-5e9e9c44d6b0
  Args:
    type: :Person
    source: :Mary_Frances_Elphinstone
  AddLiteral (2b51fa18-84b1-4e23-adfa-68ecdd226912)
 Call ID: 2b51fa18-84b1-4e23-adfa-68ecdd226912
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Mary_Frances_Elphinstone
    literal_value: 1883
  AddLiteral (2dd9ba08-edd2-4e3c-b94f-307720c48e01)
 Call ID: 2dd9ba08-edd2-4e3c-b94f-307720c48e01
  Args:
    source: :Mary_Frances_Elphinstone
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1961
  AddTriple (f909e2d1-d7cb-4765-87d0-7688700640f1)
 Call ID: f909e2d1-d7cb-4765-87d0-7688700640f1
  Args:
    target: :Lady_Elphinstone
    source: :Mary_Frances_Elphinstone
    relation: :knownAs
  AssignClass (68f1717e-c5e2-464e-8895-ad6f6e76fc78)
 Call ID: 68f1717e-c5e2-464e-8895-ad6f6e76fc78
  Args:
    type: :Woman
    source: :Queen_Elizabeth_the_Queen_Mother
  AssignClass (28e626d1-274b-47c4-897e-bf27ff8ebf48)
 Call ID: 28e626d1-274b-47c4-897e-bf27ff8ebf48
  Args:
    type: :Person
    source: :Queen_Elizabeth_the_Queen_Mother
  AddTriple (ef8e7597-ba1f-42e1-8e4b-18f0af91dfaf)
 Call ID: ef8e7597-ba1f-42e1-8e4b-18f0af91dfaf
  Args:
    target: :Queen_Elizabeth_the_Queen_Mother
    source: :Mary_Frances_Elphinstone
    relation: :isSisterOf
  AssignClass (59c7c05f-5fe3-436a-a4e6-8539865a27a2)
 Call ID: 59c7c05f-5fe3-436a-a4e6-8539865a27a2
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (38518e04-ddc6-4c87-bd49-100f430bd366)
 Call ID: 38518e04-ddc6-4c87-bd49-100f430bd366
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AddTriple (e91dfdb3-6625-4b26-b082-b4af25c4bd85)
 Call ID: e91dfdb3-6625-4b26-b082-b4af25c4bd85
  Args:
    target: :Queen_Elizabeth_II
    relation: :isAuntOf
    source: :Mary_Frances_Elphinstone
  AssignClass (ccc2a8ab-bc74-4740-a157-b20a726ed9df)
 Call ID: ccc2a8ab-bc74-4740-a157-b20a726ed9df
  Args:
    type: :Man
    source: :Claude_Bowes-Lyon
  AssignClass (ceed8771-b803-4943-82ea-203fdb6d4d82)
 Call ID: ceed8771-b803-4943-82ea-203fdb6d4d82
  Args:
    type: :Person
    source: :Claude_Bowes-Lyon
  AddTriple (238698c8-7bfd-4c78-b9aa-eb3f91b1746a)
 Call ID: 238698c8-7bfd-4c78-b9aa-eb3f91b1746a
  Args:
    target: :Claude_Bowes-Lyon
    source: :Mary_Frances_Elphinstone
    relation: :hasFather
  AssignClass (e5dd6fd2-a085-460d-a693-bf1f7b2c2867)
 Call ID: e5dd6fd2-a085-460d-a693-bf1f7b2c2867
  Args:
    type: :Man
    source: :Sidney_Elphinstone
  AssignClass (c04b0297-16cf-4ef7-819c-a52fea324c7d)
 Call ID: c04b0297-16cf-4ef7-819c-a52fea324c7d
  Args:
    type: :Person
    source: :Sidney_Elphinstone
  AddLiteral (127dccf5-abcf-4cb1-bdf2-ad086df8f9d9)
 Call ID: 127dccf5-abcf-4cb1-bdf2-ad086df8f9d9
  Args:
    literal_value: 1910
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Mary_Frances_Elphinstone
  AddTriple (4aca77ae-6261-4bb7-bc1b-f57e8281bb99)
 Call ID: 4aca77ae-6261-4bb7-bc1b-f57e8281bb99
  Args:
    relation: :hasRelation
    source: :Mary_Frances_Elphinstone
    target: :Sidney_Elphinstone
  AddLiteral (dd3f545a-245d-4821-b52e-2888e1cf8ae5)
 Call ID: dd3f545a-245d-4821-b52e-2888e1cf8ae5
  Args:
    literal_value: 1869
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Sidney_Elphinstone
  AddLiteral (8cbbb502-62a5-4773-a4ba-e6f8c3b2c88d)
 Call ID: 8cbbb502-62a5-4773-a4ba-e6f8c3b2c88d
  Args:
    literal_value: 1955
    source: :Sidney_Elphinstone
    relation: :hasDeathYear
    literal_type: xsd:integer
  Finish (08dcf708-555a-4e14-a6b3-9c42c7ccaa79)
 Call ID: 08dcf708-555a-4e14-a6b3-9c42c7ccaa79
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Mary_Frances_Elphinstone a :Person,
          :Woman ;
      :hasBirthYear 1883 ;
      :hasDeathYear 1961 ;
      :hasFather data:Claude_Bowes-Lyon ;
      :hasMarriageYear 1910 ;
      :hasRelation data:Sidney_Elphinstone ;
      :isAuntOf data:Queen_Elizabeth_II ;
      :isSisterOf data:Queen_Elizabeth_the_Queen_Mother ;
      :knownAs data:Lady_Elphinstone .

  data:Claude_Bowes-Lyon a :Man,
          :Person .

  data:Queen_Elizabeth_II a :Person,
          :Woman .

  data:Queen_Elizabeth_the_Queen_Mother a :Person,
          :Woman .

  data:Sidney_Elphinstone a :Man,
          :Person ;
      :hasBirthYear 1869 ;
      :hasDeathYear 1955 .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['Lady_Elphinstone']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e9b0b901-a02a-4c61-91d2-166861a5ecae)
 Call ID: e9b0b901-a02a-4c61-91d2-166861a5ecae
  Args:
    type: :Person
    source: :Lady_Elphinstone
  Finish (fa78835c-e79a-4af4-a983-678798e65b03)
 Call ID: fa78835c-e79a-4af4-a983-678798e65b03
  Args: