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
Alexander Patrick Gregers Richard Windsor, Earl of Ulster (born 24 October 1974), is a member of the British royal family and the only son of Prince Richard, Duke of Gloucester, and Birgitte, Duchess of Gloucester.
He is the heir apparent to the dukedom of Gloucester and is the second cousin of Charles III.
He is also sometimes referred to as Alex Ulster.
Early life and education

Alexander Patrick Gregers Richard Windsor was born prematurely on 24 October 1974 at St Mary's Hospital, London.
He is the only son of Prince Richard, Duke of Gloucester, and Birgitte, Duchess of Gloucester.
Alexander attended Eton College and later graduated with a degree in war studies from King's College London in 1996.
Military career

Alexander was commissioned in the King's Royal Hussars on 10 April 1998 as a subaltern (second lieutenant) with seniority from 14 April 1995; he was given the service number 548299.
Marriage and family

On 22 June 2002, Alexander married Claire Booth, a physician, at the Queen's Chapel, St James's Palace.
Lady Ulster is a professor of Gene Therapy and Paediatric Immunology at University College London's Great Ormond Street Institute of Child Health.
Alexander continues to make public appearances at state events alongside other members of the extended royal family, including the 2022 state funeral of Queen Elizabeth II and the 2023 coronation of King Charles III and Queen Camilla.



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
  AssignClass (2bb96e8e-ef05-4b39-8b30-318f7c762a99)
 Call ID: 2bb96e8e-ef05-4b39-8b30-318f7c762a99
  Args:
    type: :Man
    source: Alexander_Patrick_Gregers_Richard_Windsor
  AssignClass (d883821f-12a7-42c0-8b56-06d945f053fd)
 Call ID: d883821f-12a7-42c0-8b56-06d945f053fd
  Args:
    type: :Person
    source: Alexander_Patrick_Gregers_Richard_Windsor
  AddLiteral (ab608a2a-378b-4ba0-9458-5414a7dc6aaa)
 Call ID: ab608a2a-378b-4ba0-9458-5414a7dc6aaa
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1974
    source: Alexander_Patrick_Gregers_Richard_Windsor
  AddLiteral (da667e02-811b-467e-be29-760c8b7de7a8)
 Call ID: da667e02-811b-467e-be29-760c8b7de7a8
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Alex Ulster
    source: Alexander_Patrick_Gregers_Richard_Windsor
  AssignClass (46917f5a-10dc-4e8d-9625-e880f412e1bf)
 Call ID: 46917f5a-10dc-4e8d-9625-e880f412e1bf
  Args:
    type: :Man
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (5f3b0135-1f00-40df-9748-4572c4bdad9f)
 Call ID: 5f3b0135-1f00-40df-9748-4572c4bdad9f
  Args:
    type: :Person
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (9aaac8cd-b217-441e-a268-14126eae2004)
 Call ID: 9aaac8cd-b217-441e-a268-14126eae2004
  Args:
    type: :Woman
    source: Birgitte_Duchess_of_Gloucester
  AssignClass (0d9229dd-113a-4cf9-bc7a-1c9aef28e17d)
 Call ID: 0d9229dd-113a-4cf9-bc7a-1c9aef28e17d
  Args:
    type: :Person
    source: Birgitte_Duchess_of_Gloucester
  AddTriple (b4394eea-8623-4f6f-a551-df5f8cf55ff3)
 Call ID: b4394eea-8623-4f6f-a551-df5f8cf55ff3
  Args:
    target: Prince_Richard_Duke_of_Gloucester
    source: Alexander_Patrick_Gregers_Richard_Windsor
    relation: :hasFather
  AddTriple (6ece70f7-a511-4e8f-9fc1-dd7447a5fe7f)
 Call ID: 6ece70f7-a511-4e8f-9fc1-dd7447a5fe7f
  Args:
    relation: :hasMother
    source: Alexander_Patrick_Gregers_Richard_Windsor
    target: Birgitte_Duchess_of_Gloucester
  AssignClass (f54d395d-9a71-446f-9b18-76c54f7b1c07)
 Call ID: f54d395d-9a71-446f-9b18-76c54f7b1c07
  Args:
    type: :Woman
    source: Claire_Booth
  AssignClass (28e99238-0c20-4164-b70d-300001b3f0cb)
 Call ID: 28e99238-0c20-4164-b70d-300001b3f0cb
  Args:
    type: :Person
    source: Claire_Booth
  AddLiteral (cf63289e-9d66-4a71-a2c0-03e198950b21)
 Call ID: cf63289e-9d66-4a71-a2c0-03e198950b21
  Args:
    literal_value: 2002
    source: Alexander_Patrick_Gregers_Richard_Windsor
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (23aaafd0-5d8e-4da5-9070-89726396c697)
 Call ID: 23aaafd0-5d8e-4da5-9070-89726396c697
  Args:
    relation: :hasRelation
    target: Claire_Booth
    source: Alexander_Patrick_Gregers_Richard_Windsor
  AssignClass (77efc389-13c3-4dd7-b1d9-09628ed1b2e9)
 Call ID: 77efc389-13c3-4dd7-b1d9-09628ed1b2e9
  Args:
    type: :Man
    source: Charles_III
  AssignClass (0e43556a-26d3-4fbd-ab14-4e11b2e6d331)
 Call ID: 0e43556a-26d3-4fbd-ab14-4e11b2e6d331
  Args:
    type: :Person
    source: Charles_III
  AddTriple (6ed7c455-0aef-4f38-b7ac-b6d2deaea696)
 Call ID: 6ed7c455-0aef-4f38-b7ac-b6d2deaea696
  Args:
    relation: :hasRelation
    target: Charles_III
    source: Alexander_Patrick_Gregers_Richard_Windsor
  Finish (76d7fafc-adc7-42a7-b29a-7150d74c7b18)
 Call ID: 76d7fafc-adc7-42a7-b29a-7150d74c7b18
  Args: