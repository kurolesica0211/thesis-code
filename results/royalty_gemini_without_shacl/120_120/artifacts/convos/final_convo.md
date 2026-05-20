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
Archduke Sigismund, Grand Duke of Tuscany (Sigismund Otto Maria Josef Gottfried Henrich Erik Leopold Ferdinand von Habsburg-Lothringen; born 21 April 1966) is the head of the Tuscan branch of the House of Habsburg-Lorraine, and thus the claimant to the Tuscan throne.
His father was Archduke Leopoldo Franz, son of Archduke Gottfried of Austria and a claimant to the defunct throne of the Grand Duchy of Tuscany, and a great-grandson of Ferdinand IV, Grand Duke of Tuscany, the last ruler of that state.
His mother, Laetitia d'Arenberg, is a French-Uruguayan businesswoman and socialite descended from French noble families.
In 1993, his father, Archduke Leopold Franz of Austria-Tuscany, renounced his rights as head of the Tuscan grand ducal family in favour of Sigismund, as his second marriage—contracted after a divorce—conflicted with the statutes of the Order of Saint Stephen, of which he was then head.
Since then, Sigismund has been the head of the Tuscan branch of the House of Habsburg-Lorraine.
Marriage and issue

On 11 September 1999 in London, Sigismund married Elyssa Edmonstone (born 11 September 1973 in Glasgow), daughter of Sir Archibald Bruce Edmonstone, 7th Baronet of Edmonstone of Duntreath and his second wife, Julieta Isabel Deakin, daughter of Major-General Peter Deakin.



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
  AssignClass (c8b912b5-b7b9-4103-833c-2137416b5f69)
 Call ID: c8b912b5-b7b9-4103-833c-2137416b5f69
  Args:
    source: Sigismund
    type: :Man
  AssignClass (12de831e-511b-46d2-9680-bdb7afe8b144)
 Call ID: 12de831e-511b-46d2-9680-bdb7afe8b144
  Args:
    type: :Person
    source: Sigismund
  AddLiteral (85dee3a0-7563-478f-95a5-c6158a8bfc5f)
 Call ID: 85dee3a0-7563-478f-95a5-c6158a8bfc5f
  Args:
    literal_value: 1966
    source: Sigismund
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (19686847-4ee3-4f21-8913-932080c96094)
 Call ID: 19686847-4ee3-4f21-8913-932080c96094
  Args:
    source: Leopoldo_Franz
    type: :Man
  AssignClass (aca7d097-7ccc-4514-81aa-558c5062fd3b)
 Call ID: aca7d097-7ccc-4514-81aa-558c5062fd3b
  Args:
    source: Leopoldo_Franz
    type: :Ancestor
  AssignClass (eca7bc4a-dc34-4a59-972e-2ae3705a74c1)
 Call ID: eca7bc4a-dc34-4a59-972e-2ae3705a74c1
  Args:
    source: Leopoldo_Franz
    type: :Person
  AddTriple (dcba122b-3a69-47e1-aa16-f6110969617d)
 Call ID: dcba122b-3a69-47e1-aa16-f6110969617d
  Args:
    target: Leopoldo_Franz
    relation: :hasFather
    source: Sigismund
  AssignClass (207d556f-2066-4840-bcc6-c18f6dacd583)
 Call ID: 207d556f-2066-4840-bcc6-c18f6dacd583
  Args:
    type: :Man
    source: Gottfried_of_Austria
  AssignClass (5a22c335-f852-401c-8c7a-302654aa5c4a)
 Call ID: 5a22c335-f852-401c-8c7a-302654aa5c4a
  Args:
    type: :Ancestor
    source: Gottfried_of_Austria
  AssignClass (aa71c584-5039-4feb-b28f-1c41cf2c576a)
 Call ID: aa71c584-5039-4feb-b28f-1c41cf2c576a
  Args:
    source: Gottfried_of_Austria
    type: :Person
  AddTriple (72ee1c73-6c62-41cb-b5f2-4f9d24b28b13)
 Call ID: 72ee1c73-6c62-41cb-b5f2-4f9d24b28b13
  Args:
    target: Gottfried_of_Austria
    source: Leopoldo_Franz
    relation: :hasFather
  AssignClass (8a67d940-14a1-4e7b-8882-e94fec2b8fe0)
 Call ID: 8a67d940-14a1-4e7b-8882-e94fec2b8fe0
  Args:
    source: Ferdinand_IV
    type: :Man
  AssignClass (c6d8e11b-a6da-48f0-84a8-aef65b30721b)
 Call ID: c6d8e11b-a6da-48f0-84a8-aef65b30721b
  Args:
    source: Ferdinand_IV
    type: :Ancestor
  AssignClass (3c439235-9eb9-41a3-9f0a-cc2d1670369c)
 Call ID: 3c439235-9eb9-41a3-9f0a-cc2d1670369c
  Args:
    source: Ferdinand_IV
    type: :Person
  AddTriple (3e402a22-534c-4768-89a5-7f22b6faebf1)
 Call ID: 3e402a22-534c-4768-89a5-7f22b6faebf1
  Args:
    target: Ferdinand_IV
    source: Leopoldo_Franz
    relation: :hasAncestor
  AssignClass (505f228f-30d1-4e3d-9d96-8015927d16cc)
 Call ID: 505f228f-30d1-4e3d-9d96-8015927d16cc
  Args:
    type: :Woman
    source: Laetitia_d_Arenberg
  AssignClass (f8cb2c4a-cc00-453d-ac68-59dc36611cc6)
 Call ID: f8cb2c4a-cc00-453d-ac68-59dc36611cc6
  Args:
    type: :Person
    source: Laetitia_d_Arenberg
  AddTriple (11ec59d8-e7d2-4d7d-bbcb-a0a84ac13846)
 Call ID: 11ec59d8-e7d2-4d7d-bbcb-a0a84ac13846
  Args:
    target: Laetitia_d_Arenberg
    relation: :hasMother
    source: Sigismund
  AssignClass (6d0e328a-5851-4d93-b940-456cc51e9729)
 Call ID: 6d0e328a-5851-4d93-b940-456cc51e9729
  Args:
    source: Elyssa_Edmonstone
    type: :Woman
  AssignClass (2ebadad8-3b53-4e8c-bfa9-1c2bf78c6617)
 Call ID: 2ebadad8-3b53-4e8c-bfa9-1c2bf78c6617
  Args:
    source: Elyssa_Edmonstone
    type: :Person
  AddLiteral (150f771e-4538-4e04-b828-4f4810981579)
 Call ID: 150f771e-4538-4e04-b828-4f4810981579
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Elyssa_Edmonstone
    literal_value: 1973
  AddTriple (77dd1898-6de8-4bb1-af09-701cfdec59c7)
 Call ID: 77dd1898-6de8-4bb1-af09-701cfdec59c7
  Args:
    relation: :hasRelation
    source: Sigismund
    target: Elyssa_Edmonstone
  AddLiteral (6f2ccbd9-ea83-4ab5-b8f7-126cf72367cd)
 Call ID: 6f2ccbd9-ea83-4ab5-b8f7-126cf72367cd
  Args:
    literal_value: 1999
    literal_type: xsd:integer
    source: Sigismund
    relation: :hasMarriageYear
  AssignClass (de69c2bc-31e4-4c10-b482-8d0d10160070)
 Call ID: de69c2bc-31e4-4c10-b482-8d0d10160070
  Args:
    type: :Man
    source: Archibald_Bruce_Edmonstone
  AssignClass (c8aed5c6-5237-47dd-8b94-13ac554f2e74)
 Call ID: c8aed5c6-5237-47dd-8b94-13ac554f2e74
  Args:
    type: :Ancestor
    source: Archibald_Bruce_Edmonstone
  AssignClass (691475c4-6ba9-4f8f-a100-b595d981f2bb)
 Call ID: 691475c4-6ba9-4f8f-a100-b595d981f2bb
  Args:
    source: Archibald_Bruce_Edmonstone
    type: :Person
  AddTriple (5cc23c01-fc26-4e72-8690-6ebd593b60bb)
 Call ID: 5cc23c01-fc26-4e72-8690-6ebd593b60bb
  Args:
    source: Elyssa_Edmonstone
    relation: :hasFather
    target: Archibald_Bruce_Edmonstone
  AssignClass (d962302d-c42b-4b67-aa39-58efc0f3162a)
 Call ID: d962302d-c42b-4b67-aa39-58efc0f3162a
  Args:
    type: :Woman
    source: Julieta_Isabel_Deakin
  AssignClass (fbe03830-633b-4ff5-85f0-a41adfcf1f25)
 Call ID: fbe03830-633b-4ff5-85f0-a41adfcf1f25
  Args:
    source: Julieta_Isabel_Deakin
    type: :Ancestor
  AssignClass (d83e01bf-9e19-4ea4-bbdb-5e541069d636)
 Call ID: d83e01bf-9e19-4ea4-bbdb-5e541069d636
  Args:
    type: :Person
    source: Julieta_Isabel_Deakin
  AddTriple (a5c009ce-5da0-4110-92a4-0a0a1328bbaf)
 Call ID: a5c009ce-5da0-4110-92a4-0a0a1328bbaf
  Args:
    target: Julieta_Isabel_Deakin
    source: Elyssa_Edmonstone
    relation: :hasMother
  AssignClass (8457fabe-ccd3-4d80-a43a-f9fa42764b35)
 Call ID: 8457fabe-ccd3-4d80-a43a-f9fa42764b35
  Args:
    type: :Man
    source: Peter_Deakin
  AssignClass (2d0e1882-6b7b-4a0f-af1e-5387e7aed02d)
 Call ID: 2d0e1882-6b7b-4a0f-af1e-5387e7aed02d
  Args:
    source: Peter_Deakin
    type: :Ancestor
  AssignClass (8f70ceef-92e3-4e60-ae5c-8f7be0b78207)
 Call ID: 8f70ceef-92e3-4e60-ae5c-8f7be0b78207
  Args:
    type: :Person
    source: Peter_Deakin
  AddTriple (0d856129-73da-42e6-bc06-78054871b702)
 Call ID: 0d856129-73da-42e6-bc06-78054871b702
  Args:
    target: Peter_Deakin
    source: Julieta_Isabel_Deakin
    relation: :hasFather
  Finish (04be2693-e54b-47ca-a829-d6bad997aac5)
 Call ID: 04be2693-e54b-47ca-a829-d6bad997aac5
  Args: