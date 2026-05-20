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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Bernhard Lucas Emmanuel of Orange-Nassau, van Vollenhoven (born 25 December 1969) is a Dutch racing driver, entrepreneur and member of the Dutch royal family.
He is the second son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
With Willem-Alexander's succession however, he is no longer a member of the Dutch Royal House, and is no longer in line to direct succession to the Dutch throne, but still retains his membership of the Dutch royal family 


Early life and education

Bernhard was born on 25 December 1969 in Nijmegen in the Netherlands.
He is the second son of Princess Margriet and Pieter van Vollenhoven.
He has three brothers: Princes Maurits, Pieter-Christiaan, and Floris.
Subsequently, in 1989 he attended Groningen University in the Netherlands where he studied marketing and market research.
Business

Bernhard is a self-employed entrepreneur.
In 2002, the name Ritzen Koeriers was changed to Logistieke Meesters, at which time Bernhard was no longer involved in the business.
Marriage and family

While studying in Groningen, Bernhard met Annette Sekrève, (born 18 April 1972).
They have three children: Isabella Lily Juliana (born 2002), Samuel Bernhard Louis (born 2004), and Benjamin Pieter Floris (born 2008).
According to a royal decree of 5 July 2000, the children were granted the family name van Vollenhoven, without titles.
In January 2026, Bernhard and Annette announced that they were to divorce.
Upon the announcement of the planned abdication of Queen Beatrix, which took place on 30 April 2013, it was also restated that after the abdication, the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible for the throne.
Health

Bernhard has been receiving treatment for Crohn's disease since 2002.
Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (34df7eec-a246-454a-becb-7008251c3507)
 Call ID: 34df7eec-a246-454a-becb-7008251c3507
  Args:
    type: :Man
    source: :Bernhard_van_Vollenhoven
  AssignClass (951ad339-2313-4cd1-b99d-38ccf472bcae)
 Call ID: 951ad339-2313-4cd1-b99d-38ccf472bcae
  Args:
    source: :Princess_Margriet
    type: :Woman
  AssignClass (5b86ac96-bd82-436f-bfe6-2b262fcb8cf7)
 Call ID: 5b86ac96-bd82-436f-bfe6-2b262fcb8cf7
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  AssignClass (9653028f-35f8-4c64-aa98-99623ecf4b09)
 Call ID: 9653028f-35f8-4c64-aa98-99623ecf4b09
  Args:
    source: :Annette_Sekreve
    type: :Woman
  AssignClass (b65f543d-83c7-4415-a5e0-df5d7ef36dce)
 Call ID: b65f543d-83c7-4415-a5e0-df5d7ef36dce
  Args:
    type: :Woman
    source: :Isabella_Lily_Juliana
  AssignClass (1e2c8a48-491d-4e39-ab58-3737f8019cf8)
 Call ID: 1e2c8a48-491d-4e39-ab58-3737f8019cf8
  Args:
    source: :Samuel_Bernhard_Louis
    type: :Man
  AssignClass (4b563f12-85ce-46bc-b295-48b6d0e81fb7)
 Call ID: 4b563f12-85ce-46bc-b295-48b6d0e81fb7
  Args:
    type: :Man
    source: :Benjamin_Pieter_Floris
  AddLiteral (943571d6-2955-4d15-89c0-aaba5af6e5a8)
 Call ID: 943571d6-2955-4d15-89c0-aaba5af6e5a8
  Args:
    source: :Bernhard_van_Vollenhoven
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1969
  AddTriple (6f843cc6-86bd-4809-adfc-0762de403b86)
 Call ID: 6f843cc6-86bd-4809-adfc-0762de403b86
  Args:
    source: :Bernhard_van_Vollenhoven
    relation: :hasMother
    target: :Princess_Margriet
  AddTriple (0f8dc6f7-af9f-420b-aed1-22c80d66adf2)
 Call ID: 0f8dc6f7-af9f-420b-aed1-22c80d66adf2
  Args:
    relation: :hasFather
    target: :Pieter_van_Vollenhoven
    source: :Bernhard_van_Vollenhoven
  AddLiteral (eea0d2be-4fc2-4b8c-b6b4-9862b0ebb058)
 Call ID: eea0d2be-4fc2-4b8c-b6b4-9862b0ebb058
  Args:
    literal_type: xsd:integer
    literal_value: 1972
    relation: :hasBirthYear
    source: :Annette_Sekreve
  AddTriple (de05cad1-141d-403c-81f6-ae5df503073e)
 Call ID: de05cad1-141d-403c-81f6-ae5df503073e
  Args:
    relation: :hasMother
    target: :Annette_Sekreve
    source: :Isabella_Lily_Juliana
  AddTriple (0e8575ff-a6e8-46aa-8412-41e0460b9591)
 Call ID: 0e8575ff-a6e8-46aa-8412-41e0460b9591
  Args:
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
    source: :Isabella_Lily_Juliana
  AddLiteral (10ff1e99-ba30-4198-8b13-2ee065b24448)
 Call ID: 10ff1e99-ba30-4198-8b13-2ee065b24448
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2002
    source: :Isabella_Lily_Juliana
  AddTriple (108eddbd-7524-45a9-aa5f-1e1b8ec5d3bb)
 Call ID: 108eddbd-7524-45a9-aa5f-1e1b8ec5d3bb
  Args:
    target: :Annette_Sekreve
    relation: :hasMother
    source: :Samuel_Bernhard_Louis
  AddTriple (7edd459d-c193-4daa-a7a5-9673279b6f46)
 Call ID: 7edd459d-c193-4daa-a7a5-9673279b6f46
  Args:
    source: :Samuel_Bernhard_Louis
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
  AddLiteral (db6c724c-b01b-4dda-ba43-2b9d1e2593fe)
 Call ID: db6c724c-b01b-4dda-ba43-2b9d1e2593fe
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasBirthYear
    source: :Samuel_Bernhard_Louis
  AddTriple (dd7ca982-f5b6-487c-ba0e-871bdb608382)
 Call ID: dd7ca982-f5b6-487c-ba0e-871bdb608382
  Args:
    source: :Benjamin_Pieter_Floris
    relation: :hasMother
    target: :Annette_Sekreve
  AddTriple (f0040d42-bf43-4ea7-acd8-b0683f3352b1)
 Call ID: f0040d42-bf43-4ea7-acd8-b0683f3352b1
  Args:
    source: :Benjamin_Pieter_Floris
    target: :Bernhard_van_Vollenhoven
    relation: :hasFather
  AddLiteral (cfa38b00-0e69-4499-939a-3075526cab2b)
 Call ID: cfa38b00-0e69-4499-939a-3075526cab2b
  Args:
    literal_type: xsd:integer
    literal_value: 2008
    relation: :hasBirthYear
    source: :Benjamin_Pieter_Floris
  Finish (6b1f1a3b-78ef-4287-a212-86ef490bcea1)
 Call ID: 6b1f1a3b-78ef-4287-a212-86ef490bcea1
  Args: