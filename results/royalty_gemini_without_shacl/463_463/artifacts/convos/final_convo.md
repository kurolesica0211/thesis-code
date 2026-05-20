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
  AssignClass (c32e047d-2676-4d06-9fa3-81f96c5e191f)
 Call ID: c32e047d-2676-4d06-9fa3-81f96c5e191f
  Args:
    source: FrederickWindsor
    type: :Man
  AssignClass (91daa27d-938f-489e-b229-2addbb64efc0)
 Call ID: 91daa27d-938f-489e-b229-2addbb64efc0
  Args:
    type: :Person
    source: FrederickWindsor
  AddLiteral (b7c10aff-e085-4a74-8b1c-589b6f13394b)
 Call ID: b7c10aff-e085-4a74-8b1c-589b6f13394b
  Args:
    relation: :hasBirthYear
    literal_value: 1979
    literal_type: xsd:integer
    source: FrederickWindsor
  AddTriple (6da1b5dc-89d7-4e30-b19e-32f2a67a8e23)
 Call ID: 6da1b5dc-89d7-4e30-b19e-32f2a67a8e23
  Args:
    relation: :knownAs
    target: Lord Frederick Michael George David Louis Windsor
    source: FrederickWindsor
  AssignClass (fee1655a-8875-4f40-97e9-1fc55bda5936)
 Call ID: fee1655a-8875-4f40-97e9-1fc55bda5936
  Args:
    type: :Man
    source: PrinceMichaelOfKent
  AssignClass (0435f472-0fca-43d8-acac-599ee6271631)
 Call ID: 0435f472-0fca-43d8-acac-599ee6271631
  Args:
    source: PrinceMichaelOfKent
    type: :Person
  AssignClass (42fdc922-a11c-43ee-abe2-925f8f186e21)
 Call ID: 42fdc922-a11c-43ee-abe2-925f8f186e21
  Args:
    source: PrincessMichaelOfKent
    type: :Woman
  AssignClass (3a5392e9-1eb1-4ccb-86a4-8ad2a2f96a12)
 Call ID: 3a5392e9-1eb1-4ccb-86a4-8ad2a2f96a12
  Args:
    type: :Person
    source: PrincessMichaelOfKent
  AddTriple (4806dab1-fba4-4dfd-ad83-82eba5700b0c)
 Call ID: 4806dab1-fba4-4dfd-ad83-82eba5700b0c
  Args:
    target: PrinceMichaelOfKent
    relation: :hasFather
    source: FrederickWindsor
  AddTriple (49822373-0957-4da3-aec5-f4a23db60d94)
 Call ID: 49822373-0957-4da3-aec5-f4a23db60d94
  Args:
    relation: :hasMother
    target: PrincessMichaelOfKent
    source: FrederickWindsor
  AssignClass (59262004-3836-4bf2-a8d0-5ad4083de36c)
 Call ID: 59262004-3836-4bf2-a8d0-5ad4083de36c
  Args:
    type: :Woman
    source: SophieWinkleman
  AssignClass (617ce85b-738a-42b3-9a14-889540aa44d3)
 Call ID: 617ce85b-738a-42b3-9a14-889540aa44d3
  Args:
    source: SophieWinkleman
    type: :Person
  AddTriple (6738ae5e-8e69-48b4-a9db-883fac5ea926)
 Call ID: 6738ae5e-8e69-48b4-a9db-883fac5ea926
  Args:
    target: SophieWinkleman
    relation: :hasRelation
    source: FrederickWindsor
  AssignClass (b0b2299e-0776-4919-ac8c-2ef29181d1c2)
 Call ID: b0b2299e-0776-4919-ac8c-2ef29181d1c2
  Args:
    type: :Woman
    source: LadyGabriella
  AssignClass (da423797-aba8-407e-9242-0d1695fe72f3)
 Call ID: da423797-aba8-407e-9242-0d1695fe72f3
  Args:
    source: LadyGabriella
    type: :Person
  AddTriple (50080799-b562-4c15-858f-426e83fdd587)
 Call ID: 50080799-b562-4c15-858f-426e83fdd587
  Args:
    source: FrederickWindsor
    target: LadyGabriella
    relation: :isSiblingOf
  AssignClass (804bda51-6b11-4404-bfc5-962ae00f5814)
 Call ID: 804bda51-6b11-4404-bfc5-962ae00f5814
  Args:
    type: :Woman
    source: IsabellaAlexandraMay
  AssignClass (69cdbaea-ccb4-400b-8bd9-f89c665897ab)
 Call ID: 69cdbaea-ccb4-400b-8bd9-f89c665897ab
  Args:
    source: IsabellaAlexandraMay
    type: :Person
  AddTriple (867e731e-2d30-4baf-a5ce-ca2b79c9f21d)
 Call ID: 867e731e-2d30-4baf-a5ce-ca2b79c9f21d
  Args:
    target: IsabellaAlexandraMay
    relation: :hasDaughter
    source: FrederickWindsor
  AddTriple (29dcf179-09f7-4c4e-8d48-7db071761695)
 Call ID: 29dcf179-09f7-4c4e-8d48-7db071761695
  Args:
    relation: :hasDaughter
    target: IsabellaAlexandraMay
    source: SophieWinkleman
  Finish (6d6844ce-a708-4a61-bf2d-d3746f731c81)
 Call ID: 6d6844ce-a708-4a61-bf2d-d3746f731c81
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

  data:FrederickWindsor a :Man,
          :Person ;
      :hasBirthYear 1979 ;
      :hasDaughter data:IsabellaAlexandraMay ;
      :hasFather data:PrinceMichaelOfKent ;
      :hasMother data:PrincessMichaelOfKent ;
      :hasRelation data:SophieWinkleman ;
      :isSiblingOf data:LadyGabriella ;
      :knownAs data:Lord_Frederick_Michael_George_David_Louis_Windsor .

  data:LadyGabriella a :Person,
          :Woman .

  data:PrinceMichaelOfKent a :Man,
          :Person .

  data:PrincessMichaelOfKent a :Person,
          :Woman .

  data:SophieWinkleman a :Person,
          :Woman ;
      :hasDaughter data:IsabellaAlexandraMay .

  data:IsabellaAlexandraMay a :Person,
          :Woman .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['Lord_Frederick_Michael_George_David_Louis_Windsor']

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
  AssignClass (fec77101-2fc6-466b-a0b1-bc30d082179b)
 Call ID: fec77101-2fc6-466b-a0b1-bc30d082179b
  Args:
    type: :Person
    source: Lord_Frederick_Michael_George_David_Louis_Windsor
  Finish (0797043e-746f-45b4-a58f-ce4c5a19a58b)
 Call ID: 0797043e-746f-45b4-a58f-ce4c5a19a58b
  Args: