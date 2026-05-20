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
George William, Hereditary Prince of Hanover, Duke of Brunswick-Lüneburg (German: Georg Wilhelm Christian Albert Edward Alexander Friedrich Ernst Waldemar Adolf; 28 October 1880 – 20 May 1912) was a German prince from the House of Hanover.
He was the second child and eldest son of Ernest Augustus, Crown Prince of Hanover and Duke of Cumberland, and Princess Thyra of Denmark.
His father was the only son of George V of Hanover and his mother was the youngest daughter of Christian IX of Denmark.
His great-grandfather, Prince Ernest Augustus, Duke of Cumberland and Teviotdale, the fifth son of George III of the United Kingdom, became king of Hanover in 1837 because Salic Law barred Queen Victoria from inheriting the Hanoverian throne.
His godparents included his maternal grandfather Christian IX of Denmark, his uncle George I of Greece, his uncle Frederick, Crown Prince of Denmark, his uncle Alexander Alexandrovich, Tsarevich of Russia, his uncle Albert Edward, Prince of Wales, his uncle Prince Valdemar of Denmark, Prince George, Duke of Cambridge, and William, Duke of Brunswick.
The family had lived in exile in Austria since the Kingdom of Hanover was annexed by Prussia in the aftermath of the 1866 Austro-Prussian War.
His father succeeded as pretender to the Hanoverian throne and as Duke of Cumberland and Teviotdale in the peerage of Great Britain in 1878.
He represented his father at the funeral of Edward VII and the coronation of George V.


When his kinsman William, Duke of Brunswick, died unmarried in 1884, George William was his heir after his father.
Otto von Bismarck blocked Crown Ernest Augustus's claim because he had never relinquished his claim to Hanover and instead appointed Prince Albert of Prussia regent.
Prince Albert died in 1906 and Crown Ernest Augustus offered that he and George William would renounce their claims to Brunswick to allow his second son Prince Ernest Augustus to succeed.
The Bundesrat rejected this and appointed Duke John Albert of Mecklenburg as regent.
The younger Ernest Augustus finally succeeded in 1913 after he married the German Emperor's daughter after George William's death.
Death

On 20 May 1912, George William was killed, aged 31, in a car crash near Nackel, Brandenburg, while driving from Prague to Copenhagen to attend the funeral of his uncle, Frederick VIII of Denmark.
In response to George William's death, Wilhelm II, German Emperor, sent his sons Prince Eitel Friedrich and Prince August Wilhelm of Prussia to Nackel and sent a message of condolence to the Duke of Cumberland.
In response to this friendly gesture, the Duke sent his only surviving son, Ernest Augustus, to Berlin to thank the Emperor.
In Berlin, Ernest Augustus met and fell in love with the emperor's only daughter, Princess Victoria Louise of Prussia.
They married in 1913, thus reconciling the Houses of Hohenzollern and Hanover, and the Emperor approved Ernest Augustus's succession to the duchy of Brunswick shortly after.



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
  AssignClass (f32b0c20-afe9-4b82-b772-e514e7bf613c)
 Call ID: f32b0c20-afe9-4b82-b772-e514e7bf613c
  Args:
    source: George_William
    type: :Man
  AssignClass (3bbe1861-46b9-4d26-be48-9644569277c4)
 Call ID: 3bbe1861-46b9-4d26-be48-9644569277c4
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (76ee2a7f-d61d-4bc9-b123-b85677514899)
 Call ID: 76ee2a7f-d61d-4bc9-b123-b85677514899
  Args:
    type: :Woman
    source: Princess_Thyra_of_Denmark
  AssignClass (56c04723-f368-436d-97e2-bf9b4d93f29a)
 Call ID: 56c04723-f368-436d-97e2-bf9b4d93f29a
  Args:
    type: :Man
    source: George_V_of_Hanover
  AssignClass (eab90927-58dd-4a75-bd05-23c31918e334)
 Call ID: eab90927-58dd-4a75-bd05-23c31918e334
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (f45e09bc-0f1b-4280-9b86-41784a6bfb58)
 Call ID: f45e09bc-0f1b-4280-9b86-41784a6bfb58
  Args:
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    type: :Man
  AssignClass (d7cec865-eaea-4181-8e2e-1d95bbe30736)
 Call ID: d7cec865-eaea-4181-8e2e-1d95bbe30736
  Args:
    type: :Man
    source: George_III_of_the_United_Kingdom
  AssignClass (5efea920-6aa1-4426-b089-536ae08ce7e9)
 Call ID: 5efea920-6aa1-4426-b089-536ae08ce7e9
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (d3bfa389-4401-4d6e-979b-da32f0581cc5)
 Call ID: d3bfa389-4401-4d6e-979b-da32f0581cc5
  Args:
    type: :Man
    source: Prince_Ernest_Augustus_the_younger
  AssignClass (0c901c52-8659-4f98-8881-6f9bb7bf94c9)
 Call ID: 0c901c52-8659-4f98-8881-6f9bb7bf94c9
  Args:
    source: Princess_Victoria_Louise_of_Prussia
    type: :Woman
  AssignClass (6c4f1963-ce8c-4de1-90df-172a64206729)
 Call ID: 6c4f1963-ce8c-4de1-90df-172a64206729
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AddLiteral (f389cbe6-dad0-4a0a-acb7-d85e13d8b0ef)
 Call ID: f389cbe6-dad0-4a0a-acb7-d85e13d8b0ef
  Args:
    literal_value: 1880
    source: George_William
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (e4709a1c-093f-4d28-a049-3b9db27ba194)
 Call ID: e4709a1c-093f-4d28-a049-3b9db27ba194
  Args:
    relation: :hasDeathYear
    literal_value: 1912
    source: George_William
    literal_type: xsd:integer
  AddTriple (3bddc693-66ac-4eea-b192-2422aab31c61)
 Call ID: 3bddc693-66ac-4eea-b192-2422aab31c61
  Args:
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    source: George_William
    relation: :hasFather
  AddTriple (1f254484-a640-444a-9b42-15f62eb740a3)
 Call ID: 1f254484-a640-444a-9b42-15f62eb740a3
  Args:
    source: George_William
    relation: :hasMother
    target: Princess_Thyra_of_Denmark
  AddTriple (5b15c59b-cb33-4808-89d4-f38194ebc9cd)
 Call ID: 5b15c59b-cb33-4808-89d4-f38194ebc9cd
  Args:
    target: George_V_of_Hanover
    relation: :hasFather
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (e3e80a33-c932-4e22-8da2-d952777ebfbf)
 Call ID: e3e80a33-c932-4e22-8da2-d952777ebfbf
  Args:
    target: Christian_IX_of_Denmark
    relation: :hasFather
    source: Princess_Thyra_of_Denmark
  AddTriple (377eb262-202e-4c91-a2cf-850f3c2d2e25)
 Call ID: 377eb262-202e-4c91-a2cf-850f3c2d2e25
  Args:
    source: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
    relation: :hasFather
    target: George_III_of_the_United_Kingdom
  AddTriple (3fc69d3e-32ae-4de7-bef2-bdbb0c723ca9)
 Call ID: 3fc69d3e-32ae-4de7-bef2-bdbb0c723ca9
  Args:
    relation: :hasFather
    source: Ernest_Augustus_Crown_Prince_of_Hanover
    target: Prince_Ernest_Augustus_Duke_of_Cumberland_and_Teviotdale
  AddTriple (f993d6cb-9137-448b-ae3a-3f26645f2d3c)
 Call ID: f993d6cb-9137-448b-ae3a-3f26645f2d3c
  Args:
    target: Ernest_Augustus_Crown_Prince_of_Hanover
    relation: :hasFather
    source: Prince_Ernest_Augustus_the_younger
  AddTriple (d9c8127b-5469-49df-aad5-ee5b180ca1cb)
 Call ID: d9c8127b-5469-49df-aad5-ee5b180ca1cb
  Args:
    target: Wilhelm_II_German_Emperor
    relation: :hasMother
    source: Princess_Victoria_Louise_of_Prussia
  AddLiteral (4eefada0-819e-4397-b6be-ca04abad9f55)
 Call ID: 4eefada0-819e-4397-b6be-ca04abad9f55
  Args:
    literal_value: 1913
    source: Prince_Ernest_Augustus_the_younger
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (81bc2a95-e944-49dd-9fd3-c1112dfea097)
 Call ID: 81bc2a95-e944-49dd-9fd3-c1112dfea097
  Args:
    target: Princess_Victoria_Louise_of_Prussia
    source: Prince_Ernest_Augustus_the_younger
    relation: :hasRelation
  Finish (c1c79ddb-ed3a-4502-b6d0-b5ff92b7e60a)
 Call ID: c1c79ddb-ed3a-4502-b6d0-b5ff92b7e60a
  Args: