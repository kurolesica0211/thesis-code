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
The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Diane, Dowager Duchess of Württemberg (née Princess Diane of Orléans; born 24 March 1940) is a French-German painter, sculptor, writer and philanthropist.
She is the widow of Carl, Duke of Württemberg, head of the House of Württemberg.
She is the fourth daughter and sixth child of Henri, Count of Paris, Orléanist pretender to the throne of France, and his wife, Princess Isabelle of Orléans-Braganza.
Early life

Diane was born in Petrópolis, Brazil, the fourth daughter and sixth child of the Orléanist claimant to the French throne, Henri, Count of Paris, and his wife, Princess Isabelle of Orléans-Braganza.
At the time of her birth, as a claimant to the throne, her father was banned from living in France.
In 1979, the Duchess established an eponymous foundation, "Diane Herzogin von Württemberg, Prinzessin von Frankreich-Stiftung," to aid disadvantaged children.
Marriage and issue

In 1956, on a cruise organized by Queen Frederica of Greece, Diane met Duke Carl of Württemberg, son and heir of Philipp Albrecht, Duke of Württemberg, and his wife, Archduchess Rosa of Austria.
In 1957, her brother, Henri, married Carl's sister, Marie-Thérèse.
On 21 July 1960, Diane married Carl at Altshausen.
In 1975, Carl succeeded his father as head of the House of Württemberg.



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
  AssignClass (505837b5-29e8-40a2-a8c3-7d57e8189378)
 Call ID: 505837b5-29e8-40a2-a8c3-7d57e8189378
  Args:
    type: :Woman
    source: Diane_of_Orléans
  AssignClass (3b19b5e7-9032-4f36-98c6-873619b654d4)
 Call ID: 3b19b5e7-9032-4f36-98c6-873619b654d4
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (00c8874c-3406-48a2-9496-298d44b00add)
 Call ID: 00c8874c-3406-48a2-9496-298d44b00add
  Args:
    source: Isabelle_of_Orléans-Braganza
    type: :Woman
  AssignClass (a4679724-2d17-4704-ba1e-d1e796dbc5a1)
 Call ID: a4679724-2d17-4704-ba1e-d1e796dbc5a1
  Args:
    source: Carl_Duke_of_Württemberg
    type: :Man
  AssignClass (36ef4bea-5a4a-41a5-ae16-4531bb2786bb)
 Call ID: 36ef4bea-5a4a-41a5-ae16-4531bb2786bb
  Args:
    type: :Man
    source: Philipp_Albrecht_Duke_of_Württemberg
  AssignClass (9f375923-d747-464a-bc09-1c311540164f)
 Call ID: 9f375923-d747-464a-bc09-1c311540164f
  Args:
    source: Rosa_of_Austria
    type: :Woman
  AssignClass (14787cc6-b834-41ee-ab29-693070b7f8a2)
 Call ID: 14787cc6-b834-41ee-ab29-693070b7f8a2
  Args:
    source: Henri_brother_of_Diane
    type: :Man
  AssignClass (a34d794b-a725-4a7b-8acf-0069d029cc9f)
 Call ID: a34d794b-a725-4a7b-8acf-0069d029cc9f
  Args:
    source: Marie-Thérèse
    type: :Woman
  AddLiteral (643538df-ee76-4a4e-a8b5-aebaf0f29069)
 Call ID: 643538df-ee76-4a4e-a8b5-aebaf0f29069
  Args:
    literal_type: xsd:integer
    source: Diane_of_Orléans
    literal_value: 1940
    relation: :hasBirthYear
  AddTriple (e405cc65-891b-4add-8774-f700de6ae8c3)
 Call ID: e405cc65-891b-4add-8774-f700de6ae8c3
  Args:
    target: Henri_Count_of_Paris
    relation: :hasFather
    source: Diane_of_Orléans
  AddTriple (f850a237-1063-4209-8190-f570b385c796)
 Call ID: f850a237-1063-4209-8190-f570b385c796
  Args:
    source: Diane_of_Orléans
    relation: :hasMother
    target: Isabelle_of_Orléans-Braganza
  AddTriple (936cd502-0aa2-4185-a105-b0c2dc0b84c4)
 Call ID: 936cd502-0aa2-4185-a105-b0c2dc0b84c4
  Args:
    source: Carl_Duke_of_Württemberg
    relation: :hasFather
    target: Philipp_Albrecht_Duke_of_Württemberg
  AddTriple (bd277ebd-1a78-4db3-a3b0-c971b3310e87)
 Call ID: bd277ebd-1a78-4db3-a3b0-c971b3310e87
  Args:
    target: Rosa_of_Austria
    relation: :hasMother
    source: Carl_Duke_of_Württemberg
  AddTriple (b277efb2-6d6f-4fa2-9bf4-243662b76ed9)
 Call ID: b277efb2-6d6f-4fa2-9bf4-243662b76ed9
  Args:
    target: Henri_brother_of_Diane
    source: Diane_of_Orléans
    relation: :hasBrother
  AddTriple (67e9966f-89ec-4384-8a90-9b231154ebe0)
 Call ID: 67e9966f-89ec-4384-8a90-9b231154ebe0
  Args:
    target: Marie-Thérèse
    source: Carl_Duke_of_Württemberg
    relation: :hasSister
  AddTriple (18fe6d3d-5bab-44a1-8eae-c3ffbd358770)
 Call ID: 18fe6d3d-5bab-44a1-8eae-c3ffbd358770
  Args:
    target: Carl_Duke_of_Württemberg
    source: Diane_of_Orléans
    relation: :hasRelation
  AddLiteral (aeadb19c-b16c-4bf7-bc65-23663f627d9a)
 Call ID: aeadb19c-b16c-4bf7-bc65-23663f627d9a
  Args:
    relation: :hasMarriageYear
    literal_value: 1960
    source: Diane_of_Orléans
    literal_type: xsd:integer
  AddTriple (8a5bc48d-b3fc-401f-9ad2-431aa65a39dd)
 Call ID: 8a5bc48d-b3fc-401f-9ad2-431aa65a39dd
  Args:
    target: Marie-Thérèse
    source: Henri_brother_of_Diane
    relation: :hasRelation
  AddLiteral (3f0bda27-1c55-4af6-9c74-d90a3a420924)
 Call ID: 3f0bda27-1c55-4af6-9c74-d90a3a420924
  Args:
    literal_type: xsd:integer
    source: Henri_brother_of_Diane
    literal_value: 1957
    relation: :hasMarriageYear
  Finish (e862d3bd-cb5a-4475-96f5-f391807a3547)
 Call ID: e862d3bd-cb5a-4475-96f5-f391807a3547
  Args: