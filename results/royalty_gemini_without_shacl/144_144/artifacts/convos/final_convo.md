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
Queen Margrethe II


Count Henrik of Monpezat (born Prince Henrik of Denmark; 4 May 2009) is a member of the Danish royal family.
He is the third and youngest son of Prince Joachim and the only son of his second wife, Princess Marie.
He is a grandson of Queen Margrethe II and Prince Henrik and a nephew of King Frederik X. Henrik is eighth in the line of succession to the Danish throne.
Biography

Henrik was born a prince of Denmark on 4 May 2009 at Rigshospitalet, the Copenhagen University Hospital in Copenhagen.
At his christening, he received the names Henrik Carl Joachim Alain.
His godparents are his paternal aunt, Queen Mary of Denmark; his maternal uncles, Charles Cavallier and Benjamin Grandet; his mother's lady-in-waiting, Britt Davidsen Siesbye; as well as a family friend, Christian Scherfig.
On Ascension Day, Thursday 18 May 2023, Count Henrik was confirmed in Frederikskirken – The Danish Church in Paris.
The confirmation took place at 11:00, administered by the royal Chaplain-in-Ordinary, bishop Henrik Wigh-Poulsen, with the assistance of Frederikskirken's minister, Malene Bendtsen.
Titles and styles

Henrik was styled as "His Highness Prince Henrik of Denmark, Count of Monpezat" until 1 January 2023.
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
He is known as "His Excellency Count Henrik of Monpezat".
He and Prince Joachim's other children maintain their places in the order of succession.



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
  AssignClass (14a9ac9a-a216-4687-854c-e52bd4ac2bb7)
 Call ID: 14a9ac9a-a216-4687-854c-e52bd4ac2bb7
  Args:
    type: :Person
    source: Henrik_of_Monpezat
  AssignClass (78905cae-bdc0-4f69-8cbb-73248cdea1be)
 Call ID: 78905cae-bdc0-4f69-8cbb-73248cdea1be
  Args:
    type: :Man
    source: Henrik_of_Monpezat
  AddLiteral (1e7f8efb-a224-4894-99df-5c7f3825a0d3)
 Call ID: 1e7f8efb-a224-4894-99df-5c7f3825a0d3
  Args:
    relation: :knownAs
    literal_value: His Excellency Count Henrik of Monpezat
    source: Henrik_of_Monpezat
    literal_type: xsd:string
  AddLiteral (69f4d163-7a3f-4a2b-9b08-8def586a0fc7)
 Call ID: 69f4d163-7a3f-4a2b-9b08-8def586a0fc7
  Args:
    literal_value: His Highness Prince Henrik of Denmark, Count of Monpezat
    relation: :formerlyKnownAs
    source: Henrik_of_Monpezat
    literal_type: xsd:string
  AddLiteral (6c2591d4-1632-48fb-adc5-b626b9c0a2cb)
 Call ID: 6c2591d4-1632-48fb-adc5-b626b9c0a2cb
  Args:
    literal_type: xsd:integer
    source: Henrik_of_Monpezat
    relation: :hasBirthYear
    literal_value: 2009
  AssignClass (c0a930c5-c03d-4a54-bd40-54ade2db0981)
 Call ID: c0a930c5-c03d-4a54-bd40-54ade2db0981
  Args:
    type: :Person
    source: Joachim_of_Denmark
  AssignClass (6fe7e7b8-fdd8-4c43-b189-78d07cf49e61)
 Call ID: 6fe7e7b8-fdd8-4c43-b189-78d07cf49e61
  Args:
    type: :Man
    source: Joachim_of_Denmark
  AssignClass (58935fce-5dd8-4bd7-a5cf-e023eed612d7)
 Call ID: 58935fce-5dd8-4bd7-a5cf-e023eed612d7
  Args:
    type: :Person
    source: Marie_of_Denmark
  AssignClass (ec011a65-4491-42d4-82b1-5c5c273ca6f0)
 Call ID: ec011a65-4491-42d4-82b1-5c5c273ca6f0
  Args:
    type: :Woman
    source: Marie_of_Denmark
  AddTriple (4358612d-1107-478b-867b-db61bb4811a0)
 Call ID: 4358612d-1107-478b-867b-db61bb4811a0
  Args:
    relation: :hasFather
    source: Henrik_of_Monpezat
    target: Joachim_of_Denmark
  AddTriple (0f5f9844-ae34-488e-a206-bedff4689cd5)
 Call ID: 0f5f9844-ae34-488e-a206-bedff4689cd5
  Args:
    relation: :hasMother
    target: Marie_of_Denmark
    source: Henrik_of_Monpezat
  AssignClass (b76b3bfb-b95a-4afb-a691-b05e9c03a3c5)
 Call ID: b76b3bfb-b95a-4afb-a691-b05e9c03a3c5
  Args:
    type: :Person
    source: Margrethe_II
  AssignClass (08076145-6a6c-47e0-94a9-a38355489184)
 Call ID: 08076145-6a6c-47e0-94a9-a38355489184
  Args:
    type: :Woman
    source: Margrethe_II
  AssignClass (ba56bedf-204e-46be-bd93-b28b6bfee936)
 Call ID: ba56bedf-204e-46be-bd93-b28b6bfee936
  Args:
    type: :Person
    source: Henrik_Prince_Consort
  AssignClass (18d4317e-8bef-412a-a7b5-7359e4c89967)
 Call ID: 18d4317e-8bef-412a-a7b5-7359e4c89967
  Args:
    type: :Man
    source: Henrik_Prince_Consort
  AddTriple (c8aedf7b-53f0-492b-9fe9-398b763c409c)
 Call ID: c8aedf7b-53f0-492b-9fe9-398b763c409c
  Args:
    source: Henrik_of_Monpezat
    target: Margrethe_II
    relation: :hasAncestor
  AddTriple (17952811-2af4-498c-a053-b9de04b0ae1e)
 Call ID: 17952811-2af4-498c-a053-b9de04b0ae1e
  Args:
    source: Henrik_of_Monpezat
    target: Henrik_Prince_Consort
    relation: :hasAncestor
  AssignClass (371f8c6c-fffa-4d96-b9a1-a612b9a718a4)
 Call ID: 371f8c6c-fffa-4d96-b9a1-a612b9a718a4
  Args:
    type: :Person
    source: Frederik_X
  AssignClass (13b72bd6-d55b-49d1-968c-8672db900e1d)
 Call ID: 13b72bd6-d55b-49d1-968c-8672db900e1d
  Args:
    type: :Man
    source: Frederik_X
  Finish (6827cdd1-543b-449d-b4b5-cf6b734dd767)
 Call ID: 6827cdd1-543b-449d-b4b5-cf6b734dd767
  Args: