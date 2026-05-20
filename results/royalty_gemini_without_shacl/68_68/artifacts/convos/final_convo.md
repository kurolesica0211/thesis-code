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
Charles Augustus, Hereditary Grand Duke of Saxe-Weimar-Eisenach (Carl August Wilhelm Ernst Friedrich Georg Johann Albrecht; 28 July 1912 – 14 October 1988), was a German prince and head of the grand ducal house of Saxe-Weimar-Eisenach.
Life

He was born in Schloss Wilhelmsthal as the eldest son and heir of Wilhelm Ernst, Grand Duke of Saxe-Weimar-Eisenach, and his second wife, Princess Feodora of Saxe-Meiningen.
When his father died on 24 April 1923, Charles Augustus succeeded him as head of the House of Saxe-Weimar-Eisenach.
Charles Augustus died at Schienen and was succeeded as head of the grand ducal house by his son, Michael.
Marriage and issue

Charles Augustus was married at the Wartburg Castle on 5 October 1944 to Baroness Elisabeth of Wangenheim-Winterstein (Tübingen, 16 January 1912 – Munich, 15 March 2010), daughter of Othmar Baron von Wangenheim-Winterstein and wife, Baroness Maud von Trützschler.



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
  AssignClass (d4e9618b-410a-4dad-8749-7b537bb9ebf5)
 Call ID: d4e9618b-410a-4dad-8749-7b537bb9ebf5
  Args:
    type: :Man
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
  AssignClass (16663fb7-bc7e-4253-8e56-e202dac5a38f)
 Call ID: 16663fb7-bc7e-4253-8e56-e202dac5a38f
  Args:
    source: Wilhelm_Ernst_of_Saxe-Weimar-Eisenach
    type: :Man
  AssignClass (db70f732-8522-42f6-92fb-beb1dc145bc3)
 Call ID: db70f732-8522-42f6-92fb-beb1dc145bc3
  Args:
    source: Feodora_of_Saxe-Meiningen
    type: :Woman
  AssignClass (30e9928a-6a47-4e95-8693-b2d1cfb5aa55)
 Call ID: 30e9928a-6a47-4e95-8693-b2d1cfb5aa55
  Args:
    source: Michael_of_Saxe-Weimar-Eisenach
    type: :Man
  AssignClass (24f01d9f-da60-4181-847e-130a7305e166)
 Call ID: 24f01d9f-da60-4181-847e-130a7305e166
  Args:
    source: Elisabeth_of_Wangenheim-Winterstein
    type: :Woman
  AssignClass (2f259a65-10a3-4fae-b57a-4b85dc211627)
 Call ID: 2f259a65-10a3-4fae-b57a-4b85dc211627
  Args:
    source: Othmar_von_Wangenheim-Winterstein
    type: :Man
  AssignClass (9fdd0661-6644-4499-a318-902136765ca0)
 Call ID: 9fdd0661-6644-4499-a318-902136765ca0
  Args:
    type: :Woman
    source: Maud_von_Trützschler
  AddLiteral (f032cdb4-a77f-4f23-b154-9188f648ebd7)
 Call ID: f032cdb4-a77f-4f23-b154-9188f648ebd7
  Args:
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1912
  AddLiteral (28555426-6aa3-49da-9c58-cc3611019049)
 Call ID: 28555426-6aa3-49da-9c58-cc3611019049
  Args:
    literal_value: 1988
    literal_type: xsd:integer
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
    relation: :hasDeathYear
  AddTriple (8500d5a3-f6f5-4181-997c-b34b9b6bb5db)
 Call ID: 8500d5a3-f6f5-4181-997c-b34b9b6bb5db
  Args:
    target: Wilhelm_Ernst_of_Saxe-Weimar-Eisenach
    relation: :hasFather
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
  AddTriple (ac5bc308-183b-4410-8373-6a8a2e5ceefa)
 Call ID: ac5bc308-183b-4410-8373-6a8a2e5ceefa
  Args:
    target: Feodora_of_Saxe-Meiningen
    relation: :hasMother
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
  AddTriple (bd1d703c-70f5-4c21-88bb-fe8c9c84dda9)
 Call ID: bd1d703c-70f5-4c21-88bb-fe8c9c84dda9
  Args:
    target: Michael_of_Saxe-Weimar-Eisenach
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
    relation: :isFatherOf
  AddLiteral (c591994c-8e45-476a-8bad-40122280a2cd)
 Call ID: c591994c-8e45-476a-8bad-40122280a2cd
  Args:
    literal_value: 1944
    literal_type: xsd:integer
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
    relation: :hasMarriageYear
  AddTriple (a39655c1-e8c9-4682-a2bc-74c710a4c1d2)
 Call ID: a39655c1-e8c9-4682-a2bc-74c710a4c1d2
  Args:
    relation: :hasRelation
    source: Charles_Augustus_of_Saxe-Weimar-Eisenach
    target: Elisabeth_of_Wangenheim-Winterstein
  AddLiteral (dd7dad1e-1e77-4fa3-b44d-dac74e57b2ef)
 Call ID: dd7dad1e-1e77-4fa3-b44d-dac74e57b2ef
  Args:
    literal_value: 1912
    relation: :hasBirthYear
    source: Elisabeth_of_Wangenheim-Winterstein
    literal_type: xsd:integer
  AddLiteral (5820c858-855b-49ce-8644-01c3c5838870)
 Call ID: 5820c858-855b-49ce-8644-01c3c5838870
  Args:
    literal_value: 2010
    relation: :hasDeathYear
    source: Elisabeth_of_Wangenheim-Winterstein
    literal_type: xsd:integer
  AddTriple (e0666fd4-94c3-4fa4-bc2a-c46fe3c9fd14)
 Call ID: e0666fd4-94c3-4fa4-bc2a-c46fe3c9fd14
  Args:
    target: Othmar_von_Wangenheim-Winterstein
    relation: :hasFather
    source: Elisabeth_of_Wangenheim-Winterstein
  AddTriple (cd220c28-e9b0-4aa9-9a9f-b24b02ad24ea)
 Call ID: cd220c28-e9b0-4aa9-9a9f-b24b02ad24ea
  Args:
    source: Elisabeth_of_Wangenheim-Winterstein
    relation: :hasMother
    target: Maud_von_Trützschler
  Finish (b05a6f00-cb3d-48d6-9109-f3c8e838fa98)
 Call ID: b05a6f00-cb3d-48d6-9109-f3c8e838fa98
  Args: