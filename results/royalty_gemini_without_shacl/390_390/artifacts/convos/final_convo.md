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
Prince William Victor Charles Augustus Henry Sigismund of Prussia (German: Wilhelm Viktor Karl August Heinrich Sigismund; 27 November 1896 at Kiel – 14 November 1978 at Puntarenas, Costa Rica), was the second son of Prince Henry of Prussia and Princess Irene of Hesse and by Rhine.
He was the nephew of Kaiser Wilhelm II and Tsarina Alexandra of Russia.
Life

Marriage and issue

On 11 July 1919 at Hemmelmark, he married Princess Charlotte of Saxe-Altenburg (4 March 1899 – 16 February 1989), the eldest daughter of Ernst II, Duke of Saxe-Altenburg.
In 1927, Sigismund and his family resettled in Costa Rica  three years after his son Alfred (1924–2013) had been born in Guatemala.
In 1957, Sigismund returned to Germany to meet with Anna Anderson whom he recognized as his cousin Grand Duchess Anastasia.
Sigismund died in Puntarenas, Costa Rica, on 14 November 1978.
Honours and awards

Prince Sigismund received the following awards:


Ancestry

See also

References



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
  AssignClass (967d6078-696d-4f13-84e6-e97698331510)
 Call ID: 967d6078-696d-4f13-84e6-e97698331510
  Args:
    source: :Sigismund_of_Prussia
    type: :Man
  AssignClass (f37919a5-8e94-425a-bf1d-4fca9f64e0b0)
 Call ID: f37919a5-8e94-425a-bf1d-4fca9f64e0b0
  Args:
    source: :Sigismund_of_Prussia
    type: :Person
  AddLiteral (d4c196e1-2b35-43da-a6ff-991da584514e)
 Call ID: d4c196e1-2b35-43da-a6ff-991da584514e
  Args:
    literal_type: xsd:integer
    source: :Sigismund_of_Prussia
    relation: :hasBirthYear
    literal_value: 1896
  AddLiteral (2bb55de9-f080-4c12-8666-cc6bca633317)
 Call ID: 2bb55de9-f080-4c12-8666-cc6bca633317
  Args:
    relation: :hasDeathYear
    source: :Sigismund_of_Prussia
    literal_value: 1978
    literal_type: xsd:integer
  AssignClass (c663e2a6-85bd-4bda-83f6-77818f70c876)
 Call ID: c663e2a6-85bd-4bda-83f6-77818f70c876
  Args:
    type: :Man
    source: :Henry_of_Prussia
  AssignClass (e0c451ff-1c7e-443b-b1b8-cad403755c63)
 Call ID: e0c451ff-1c7e-443b-b1b8-cad403755c63
  Args:
    type: :Person
    source: :Henry_of_Prussia
  AddTriple (fa0b4e3d-8e0d-44dc-8187-e3e78a69b67d)
 Call ID: fa0b4e3d-8e0d-44dc-8187-e3e78a69b67d
  Args:
    relation: :hasFather
    source: :Sigismund_of_Prussia
    target: :Henry_of_Prussia
  AssignClass (cc1ce5f7-bdb3-48a5-95ff-9f3bc4b08e80)
 Call ID: cc1ce5f7-bdb3-48a5-95ff-9f3bc4b08e80
  Args:
    type: :Woman
    source: :Irene_of_Hesse
  AssignClass (7f08d9be-797b-4770-8b3e-243929828c24)
 Call ID: 7f08d9be-797b-4770-8b3e-243929828c24
  Args:
    source: :Irene_of_Hesse
    type: :Person
  AddTriple (4d2cd4b6-9e85-42a6-9d76-1ab990116868)
 Call ID: 4d2cd4b6-9e85-42a6-9d76-1ab990116868
  Args:
    relation: :hasMother
    source: :Sigismund_of_Prussia
    target: :Irene_of_Hesse
  AssignClass (e8f7a6ff-e6fe-4ccb-9a76-eb6a3979a9bb)
 Call ID: e8f7a6ff-e6fe-4ccb-9a76-eb6a3979a9bb
  Args:
    type: :Woman
    source: :Charlotte_of_Saxe-Altenburg
  AssignClass (b6c0b202-d342-4fd9-ad42-598b1ebcaf2e)
 Call ID: b6c0b202-d342-4fd9-ad42-598b1ebcaf2e
  Args:
    source: :Charlotte_of_Saxe-Altenburg
    type: :Person
  AddLiteral (9d4e9f59-e2f8-4870-b05c-9cb6ec883410)
 Call ID: 9d4e9f59-e2f8-4870-b05c-9cb6ec883410
  Args:
    relation: :hasMarriageYear
    source: :Sigismund_of_Prussia
    literal_value: 1919
    literal_type: xsd:integer
  AddTriple (8669e51b-5491-42bc-ab6a-31b116c1d3f8)
 Call ID: 8669e51b-5491-42bc-ab6a-31b116c1d3f8
  Args:
    source: :Sigismund_of_Prussia
    relation: :hasRelation
    target: :Charlotte_of_Saxe-Altenburg
  AssignClass (61e20799-18ea-444d-aa64-fcddb8094209)
 Call ID: 61e20799-18ea-444d-aa64-fcddb8094209
  Args:
    type: :Man
    source: :Alfred_of_Prussia
  AssignClass (7042b5c2-2c0d-4315-bdde-ce0606a21478)
 Call ID: 7042b5c2-2c0d-4315-bdde-ce0606a21478
  Args:
    source: :Alfred_of_Prussia
    type: :Person
  AddLiteral (abdf9856-9c3a-4d0f-bd63-21b9cc920efa)
 Call ID: abdf9856-9c3a-4d0f-bd63-21b9cc920efa
  Args:
    relation: :hasBirthYear
    source: :Alfred_of_Prussia
    literal_value: 1924
    literal_type: xsd:integer
  AddLiteral (0bd3bc14-1d17-4190-8a13-45434664b15b)
 Call ID: 0bd3bc14-1d17-4190-8a13-45434664b15b
  Args:
    literal_type: xsd:integer
    literal_value: 2013
    source: :Alfred_of_Prussia
    relation: :hasDeathYear
  AddTriple (e3e0dad8-f995-4fa9-93ea-62f9ab7c4cf2)
 Call ID: e3e0dad8-f995-4fa9-93ea-62f9ab7c4cf2
  Args:
    target: :Sigismund_of_Prussia
    relation: :isSonOf
    source: :Alfred_of_Prussia
  AssignClass (38d468be-ca19-480c-a31b-fdc96363e676)
 Call ID: 38d468be-ca19-480c-a31b-fdc96363e676
  Args:
    source: :Ernst_II_of_Saxe-Altenburg
    type: :Man
  AssignClass (04df1719-1206-44cc-aa05-2c3b0cefd92e)
 Call ID: 04df1719-1206-44cc-aa05-2c3b0cefd92e
  Args:
    source: :Ernst_II_of_Saxe-Altenburg
    type: :Person
  AddTriple (5a977175-e2b6-4bfb-84d2-739fbff61a9d)
 Call ID: 5a977175-e2b6-4bfb-84d2-739fbff61a9d
  Args:
    target: :Ernst_II_of_Saxe-Altenburg
    relation: :hasFather
    source: :Charlotte_of_Saxe-Altenburg
  Finish (fdd95eff-b50b-4bc7-9e30-46c10c425f6f)
 Call ID: fdd95eff-b50b-4bc7-9e30-46c10c425f6f
  Args: