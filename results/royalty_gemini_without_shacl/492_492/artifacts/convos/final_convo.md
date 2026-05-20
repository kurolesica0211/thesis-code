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
Bernhard Prinz und Markgraf von Baden (born 27 May 1970), styled Margrave of Baden and Duke of Zähringen, is the head of the House of Baden since 29 December 2022 following the death of his father, Maximilian.
Early life and family

Bernhard was born at Schloss Salem in Salem, Baden-Württemberg, on 27 May 1970.
He is the eldest son of Maximilian, Margrave of Baden, and Archduchess Valerie of Austria (born 1941) and was styled as the heir of his father, Hereditary Prince of Baden.
His paternal grandparents were Berthold, Margrave of Baden, and Princess Theodora of Greece and Denmark, who was a sister of Prince Philip, Duke of Edinburgh.
His maternal grandparents were Archduke Hubert Salvator of Austria and Princess Rosemary of Salm-Salm.
Prince Bernhard manages the family estates, including Staufenberg Castle, and the margravial wineries dedicated to preserving the grape variety Müller-Thurgau.
Bernhard has close relations with the British royal family, and his granduncle, Prince Philip, Duke of Edinburgh, often came to Germany to shoot with the Baden family.
On 17 April 2021, Bernhard was one of only thirty mourners at Prince Philip's ceremonial funeral at St George's Chapel, Windsor Castle.
Bernhard, along with his cousins Philipp, Prince of Hohenlohe-Langenburg, and Donatus, Landgrave of Hesse, was chosen to represent the families of the Duke's late sisters who had been prevented from attending his wedding in 1947.
Bernhard and his wife and siblings later attended a service of thanksgiving for Prince Philip's life at Westminster Abbey on 29 March 2022.
On 29 December 2022, his father, Maximilian, died and Bernhard became head of the former grand ducal house of Baden.
Though royal and noble titles were abolished in Germany in 1919 when the Weimar Republic was proclaimed, he is sometimes styled and titled His Royal Highness The Margrave of Baden, Duke of Zähringen, by courtesy.
Prior to this, he was styled and titled His Grand Ducal Highness Hereditary Prince of Baden.
On 24 April 2025 the Margrave attended the funeral of Andreas, Prince of Saxe-Coburg and Gotha as the representative of Charles III.
Marriage and children

Bernhard married Stephanie Anne Kaul (born 27 June 1966), daughter of Christian Kaul and Hannelore Scheel, in a civil ceremony on 22 June 2001 and a religious ceremony the following day at Schloss Salem.



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
  AssignClass (2177ae9c-c0c6-42cc-a125-9924ee4a098e)
 Call ID: 2177ae9c-c0c6-42cc-a125-9924ee4a098e
  Args:
    type: :Man
    source: Bernhard
  AssignClass (15ae6094-2c28-400d-a8c1-4894ecd372fa)
 Call ID: 15ae6094-2c28-400d-a8c1-4894ecd372fa
  Args:
    type: :Man
    source: Maximilian
  AssignClass (2c703c05-013c-4ef5-9a11-40e812371913)
 Call ID: 2c703c05-013c-4ef5-9a11-40e812371913
  Args:
    type: :Woman
    source: Valerie
  AssignClass (d23d325c-7e48-4746-9578-7ab52af452f9)
 Call ID: d23d325c-7e48-4746-9578-7ab52af452f9
  Args:
    type: :Man
    source: Berthold
  AssignClass (3a216c1d-4507-472c-93cf-12be6a669870)
 Call ID: 3a216c1d-4507-472c-93cf-12be6a669870
  Args:
    type: :Woman
    source: Theodora
  AssignClass (04643d39-1319-43ab-b708-fda6a026c340)
 Call ID: 04643d39-1319-43ab-b708-fda6a026c340
  Args:
    source: HubertSalvator
    type: :Man
  AssignClass (a144d2cc-17f3-47de-9e38-bbf4149bb027)
 Call ID: a144d2cc-17f3-47de-9e38-bbf4149bb027
  Args:
    type: :Woman
    source: Rosemary
  AssignClass (9c0134a7-f56f-462e-9268-f3ef0511d7ff)
 Call ID: 9c0134a7-f56f-462e-9268-f3ef0511d7ff
  Args:
    type: :Woman
    source: StephanieAnneKaul
  AssignClass (1dee6913-7ab8-41ab-97ee-d6ac398ea6f8)
 Call ID: 1dee6913-7ab8-41ab-97ee-d6ac398ea6f8
  Args:
    source: ChristianKaul
    type: :Man
  AssignClass (24a6f7a0-75cb-40e4-9e95-f88981f75a04)
 Call ID: 24a6f7a0-75cb-40e4-9e95-f88981f75a04
  Args:
    type: :Woman
    source: HanneloreScheel
  AddLiteral (d1e1d78f-aceb-4831-8977-4302e77664ef)
 Call ID: d1e1d78f-aceb-4831-8977-4302e77664ef
  Args:
    relation: :hasBirthYear
    source: Bernhard
    literal_value: 1970
    literal_type: xsd:integer
  AddLiteral (c71e50ca-201c-4792-9779-f08424efffb9)
 Call ID: c71e50ca-201c-4792-9779-f08424efffb9
  Args:
    literal_value: 1941
    source: Valerie
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (332e1d27-fcc4-4f46-9d06-7fdbbdc3e168)
 Call ID: 332e1d27-fcc4-4f46-9d06-7fdbbdc3e168
  Args:
    literal_value: 1966
    source: StephanieAnneKaul
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (62b8e49a-6bf2-47cb-8c8d-2102a61506d5)
 Call ID: 62b8e49a-6bf2-47cb-8c8d-2102a61506d5
  Args:
    relation: :hasDeathYear
    source: Maximilian
    literal_value: 2022
    literal_type: xsd:integer
  AddLiteral (a30293b4-0747-4d78-9372-fccf7df09aa5)
 Call ID: a30293b4-0747-4d78-9372-fccf7df09aa5
  Args:
    literal_type: xsd:integer
    literal_value: 2001
    source: Bernhard
    relation: :hasMarriageYear
  AddTriple (81fb46aa-c125-4dae-8df2-46e3241e438e)
 Call ID: 81fb46aa-c125-4dae-8df2-46e3241e438e
  Args:
    relation: :hasFather
    source: Bernhard
    target: Maximilian
  AddTriple (147daa8d-dd9a-4902-84d8-17ec710cc656)
 Call ID: 147daa8d-dd9a-4902-84d8-17ec710cc656
  Args:
    relation: :hasMother
    target: Valerie
    source: Bernhard
  AddTriple (31137e57-6b90-4337-885d-698a5a1851c6)
 Call ID: 31137e57-6b90-4337-885d-698a5a1851c6
  Args:
    source: Maximilian
    target: Berthold
    relation: :hasFather
  AddTriple (5ca435a2-3565-401e-a54f-875c9b1c1747)
 Call ID: 5ca435a2-3565-401e-a54f-875c9b1c1747
  Args:
    target: Theodora
    source: Maximilian
    relation: :hasMother
  AddTriple (352e596e-a4ee-413f-be24-79f7a64ec6a0)
 Call ID: 352e596e-a4ee-413f-be24-79f7a64ec6a0
  Args:
    relation: :hasFather
    target: HubertSalvator
    source: Valerie
  AddTriple (47f71690-ec60-463b-acfa-d5a14034f8c0)
 Call ID: 47f71690-ec60-463b-acfa-d5a14034f8c0
  Args:
    relation: :hasMother
    source: Valerie
    target: Rosemary
  AddTriple (dcae82d2-3c80-4195-ac00-ed0e58b403ae)
 Call ID: dcae82d2-3c80-4195-ac00-ed0e58b403ae
  Args:
    target: ChristianKaul
    source: StephanieAnneKaul
    relation: :hasFather
  AddTriple (d4f0fbd7-2c8a-414f-bd81-4d7fa993f162)
 Call ID: d4f0fbd7-2c8a-414f-bd81-4d7fa993f162
  Args:
    source: StephanieAnneKaul
    target: HanneloreScheel
    relation: :hasMother
  Finish (729cd4eb-4dd5-47c4-b634-65fd6b169628)
 Call ID: 729cd4eb-4dd5-47c4-b634-65fd6b169628
  Args: