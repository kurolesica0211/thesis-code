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
John Alexander Elphinstone, 17th Lord Elphinstone and 3rd Baron Elphinstone (22 March 1914 – 15 November 1975) was a British nobleman and serviceman during World War II.
He was a first cousin of Queen Elizabeth II.
He was a son of Sidney Elphinstone, 16th Lord Elphinstone, and Lady Mary Bowes-Lyon.
Andrew Charles Victor Elphinstone (the aide-de-camp to the Viceroy of India from 1941 to 1943) and the Hon.
Margaret Elphinstone, wife of writer Denys Rhodes.
His paternal grandparents were William Elphinstone, 15th Lord Elphinstone (the 1st Baron Elphinstone) and the former Lady Constance Euphemia Woronzow Murray (second daughter of Alexander Murray, 6th Earl of Dunmore).
He was a nephew of Queen Elizabeth
The Queen Mother and a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Lord Elphinstone served as president of the Scottish Association of Boys' Clubs, chairman of council of the Scottish branch of British Red Cross Society, and president of the Royal Zoological Society of Scotland.
Personal life

In 1970, during Manitoba's centennial, he was invited by the community of Elphinstone and gave a silver map case, which is today located at the Elphinstone post office, all named in his family's honor.



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
  AssignClass (fbdeac19-5925-41ac-85d7-060fc4709fcb)
 Call ID: fbdeac19-5925-41ac-85d7-060fc4709fcb
  Args:
    source: :John_Alexander_Elphinstone
    type: :Man
  AssignClass (b902d5e6-15f5-4725-a171-1bea481c3955)
 Call ID: b902d5e6-15f5-4725-a171-1bea481c3955
  Args:
    source: :John_Alexander_Elphinstone
    type: :Person
  AddLiteral (7d13e0f2-5750-468c-8b22-6b8930b1918a)
 Call ID: 7d13e0f2-5750-468c-8b22-6b8930b1918a
  Args:
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :John_Alexander_Elphinstone
  AddLiteral (6ffc952a-20a4-42c3-87be-69a956d4df04)
 Call ID: 6ffc952a-20a4-42c3-87be-69a956d4df04
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1975
    source: :John_Alexander_Elphinstone
  AssignClass (54e6d781-e5f2-4117-b062-ce4c8a72ba6b)
 Call ID: 54e6d781-e5f2-4117-b062-ce4c8a72ba6b
  Args:
    type: :Man
    source: :Sidney_Elphinstone
  AssignClass (ee75bab8-2d5b-4e41-acb4-e37e58c35b87)
 Call ID: ee75bab8-2d5b-4e41-acb4-e37e58c35b87
  Args:
    source: :Sidney_Elphinstone
    type: :Person
  AssignClass (32e318ad-e2c4-4ffb-8fdf-95fec60a6872)
 Call ID: 32e318ad-e2c4-4ffb-8fdf-95fec60a6872
  Args:
    source: :Lady_Mary_Bowes-Lyon
    type: :Woman
  AssignClass (4f98a067-d1e1-4e8b-a592-57d30acd4d97)
 Call ID: 4f98a067-d1e1-4e8b-a592-57d30acd4d97
  Args:
    type: :Person
    source: :Lady_Mary_Bowes-Lyon
  AddTriple (708b8621-b86e-44e9-9635-2f93801c2bc8)
 Call ID: 708b8621-b86e-44e9-9635-2f93801c2bc8
  Args:
    source: :John_Alexander_Elphinstone
    target: :Sidney_Elphinstone
    relation: :hasFather
  AddTriple (04b6995c-aaa4-4ac8-9c49-9bc456f285b0)
 Call ID: 04b6995c-aaa4-4ac8-9c49-9bc456f285b0
  Args:
    target: :Lady_Mary_Bowes-Lyon
    relation: :hasMother
    source: :John_Alexander_Elphinstone
  AssignClass (f851dedb-ea43-4c30-85da-7917da373afe)
 Call ID: f851dedb-ea43-4c30-85da-7917da373afe
  Args:
    source: :Andrew_Charles_Victor_Elphinstone
    type: :Man
  AssignClass (f2714c70-5b1c-474b-8715-ed9271013212)
 Call ID: f2714c70-5b1c-474b-8715-ed9271013212
  Args:
    source: :Andrew_Charles_Victor_Elphinstone
    type: :Person
  AssignClass (a218a756-d365-475e-a2a9-af99c8cac4c2)
 Call ID: a218a756-d365-475e-a2a9-af99c8cac4c2
  Args:
    type: :Woman
    source: :Margaret_Elphinstone
  AssignClass (3ceff87d-d869-4dad-aec8-c23682160102)
 Call ID: 3ceff87d-d869-4dad-aec8-c23682160102
  Args:
    source: :Margaret_Elphinstone
    type: :Person
  AddTriple (45b149df-d1a9-451a-9883-f48a20e0e105)
 Call ID: 45b149df-d1a9-451a-9883-f48a20e0e105
  Args:
    relation: :hasBrother
    target: :Andrew_Charles_Victor_Elphinstone
    source: :John_Alexander_Elphinstone
  AddTriple (972fd33a-fde4-4e6a-aa00-19da60500b74)
 Call ID: 972fd33a-fde4-4e6a-aa00-19da60500b74
  Args:
    source: :John_Alexander_Elphinstone
    relation: :hasSister
    target: :Margaret_Elphinstone
  AssignClass (c65a790d-44f5-4715-bf28-03279df945e7)
 Call ID: c65a790d-44f5-4715-bf28-03279df945e7
  Args:
    source: :William_Elphinstone
    type: :Man
  AssignClass (6fcb420a-ecf4-48f5-b1d4-0dcff41ccdf4)
 Call ID: 6fcb420a-ecf4-48f5-b1d4-0dcff41ccdf4
  Args:
    source: :William_Elphinstone
    type: :Person
  AssignClass (bd72c845-d972-4d51-b60e-09e6551a3499)
 Call ID: bd72c845-d972-4d51-b60e-09e6551a3499
  Args:
    type: :Woman
    source: :Lady_Constance_Euphemia_Woronzow_Murray
  AssignClass (2937fd47-68ef-482d-ac17-6a8012312477)
 Call ID: 2937fd47-68ef-482d-ac17-6a8012312477
  Args:
    source: :Lady_Constance_Euphemia_Woronzow_Murray
    type: :Person
  AddTriple (f01e75ca-b8dd-4d12-99c1-d2f2ed092c31)
 Call ID: f01e75ca-b8dd-4d12-99c1-d2f2ed092c31
  Args:
    source: :Sidney_Elphinstone
    relation: :hasFather
    target: :William_Elphinstone
  AddTriple (ea089ed7-4f0e-45fb-8b32-29461642859e)
 Call ID: ea089ed7-4f0e-45fb-8b32-29461642859e
  Args:
    source: :Sidney_Elphinstone
    relation: :hasMother
    target: :Lady_Constance_Euphemia_Woronzow_Murray
  AssignClass (3fe8099d-a917-43c2-8ff5-50bf0ccddcf3)
 Call ID: 3fe8099d-a917-43c2-8ff5-50bf0ccddcf3
  Args:
    type: :Man
    source: :Alexander_Murray
  AssignClass (36b2d1b0-4283-4596-ab54-1f869ad774cb)
 Call ID: 36b2d1b0-4283-4596-ab54-1f869ad774cb
  Args:
    source: :Alexander_Murray
    type: :Person
  AddTriple (62df7da5-dce8-4833-820d-aec518463810)
 Call ID: 62df7da5-dce8-4833-820d-aec518463810
  Args:
    source: :Lady_Constance_Euphemia_Woronzow_Murray
    target: :Alexander_Murray
    relation: :hasFather
  AssignClass (c00d9eb4-b0db-4555-aa96-42e4f3e78f4b)
 Call ID: c00d9eb4-b0db-4555-aa96-42e4f3e78f4b
  Args:
    source: :Denys_Rhodes
    type: :Man
  AssignClass (22730f47-9d54-4daa-9ed0-b93729e1976e)
 Call ID: 22730f47-9d54-4daa-9ed0-b93729e1976e
  Args:
    type: :Person
    source: :Denys_Rhodes
  AssignClass (a439fb7c-a3a6-4dd2-a703-dbba7377818f)
 Call ID: a439fb7c-a3a6-4dd2-a703-dbba7377818f
  Args:
    source: :Queen_Elizabeth_II
    type: :Woman
  AssignClass (9ded3ca1-1c79-44e1-bca6-d34d04531904)
 Call ID: 9ded3ca1-1c79-44e1-bca6-d34d04531904
  Args:
    source: :Queen_Elizabeth_II
    type: :Person
  AssignClass (7fd72e19-30ca-4c40-9930-e17b93a57dcf)
 Call ID: 7fd72e19-30ca-4c40-9930-e17b93a57dcf
  Args:
    source: :Princess_Margaret
    type: :Woman
  AssignClass (108ed40c-d172-4e37-a81e-6deabfada956)
 Call ID: 108ed40c-d172-4e37-a81e-6deabfada956
  Args:
    type: :Person
    source: :Princess_Margaret
  AssignClass (9a2bd428-2e2b-4997-a436-f200f6c2dd61)
 Call ID: 9a2bd428-2e2b-4997-a436-f200f6c2dd61
  Args:
    type: :Woman
    source: :Queen_Elizabeth_The_Queen_Mother
  AssignClass (52b76498-4a13-447e-988e-897a629315f8)
 Call ID: 52b76498-4a13-447e-988e-897a629315f8
  Args:
    source: :Queen_Elizabeth_The_Queen_Mother
    type: :Person
  AddTriple (10fc98b6-2395-4128-babc-10cc2a3062eb)
 Call ID: 10fc98b6-2395-4128-babc-10cc2a3062eb
  Args:
    relation: :hasRelation
    target: :Queen_Elizabeth_II
    source: :John_Alexander_Elphinstone
  AddTriple (9e81f88d-c4c6-490a-abb7-874ed98d325d)
 Call ID: 9e81f88d-c4c6-490a-abb7-874ed98d325d
  Args:
    relation: :hasRelation
    target: :Princess_Margaret
    source: :John_Alexander_Elphinstone
  Finish (e742c85d-e753-46a8-95f1-afc2151655a2)
 Call ID: e742c85d-e753-46a8-95f1-afc2151655a2
  Args: