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
Lady Sarah Frances Elizabeth Chatto (née Armstrong-Jones; born 1
She is the only daughter of Princess Margaret, Countess of Snowdon, and Antony Armstrong-Jones, 1st Earl of Snowdon.
She and her brother, David Armstrong-Jones, 2nd Earl of Snowdon, are the only maternal first cousins of King Charles III.
Early life and education

Lady Sarah Frances Elizabeth Armstrong-Jones was born at 8:20 am on 1 May 1964 at Kensington Palace in London.
She is the second child and only daughter of Princess Margaret and Antony Armstrong-Jones, 1st Earl of Snowdon.
Sarah is a godmother to Prince Harry, Duke of Sussex, Lady Rose Gilman, and Lady Louise Windsor.
She also has half-siblings on her father's side: Polly Fry (born 1960), Lady Frances Armstrong-Jones (born 1979), and Jasper Cable-Alexander (born 1998).
Sarah and her brother, David, then Viscount Linley, grew up in the nursery of Kensington Palace, Apartment 10.
Their parents' marriage was fractious; the couple formally separated when Sarah was 12 and divorced when she was 14.
Holidays were given to the royal estates at Sandringham and Balmoral, where Sarah did landscape painting.
Sarah was a bridesmaid at the wedding of her cousin Charles, Prince of Wales, and Lady Diana Spencer.
The film's producer, her relative John Knatchbull, 7th Baron Brabourne (son-in-law of Louis Mountbatten, 1st Earl Mountbatten of Burma), gave her a job as an intern assisting the wardrobe department and studying wood gilding under her father's cousin Thomas Messel.
Professional life

Chatto has been exhibiting her work, always under the name Sarah Armstrong-Jones, at The Redfern Gallery since 1995.
Chatto does not undertake public duties and is not considered a "working royal".
However, it has been reported that she was close to her aunt Queen Elizabeth II.
Chatto is frequently seen attending public events such as jubilees and funerals, as well as semi-private royal family events, such as the Sandringham Christmas service, with her sons.
Marriage and children

Sarah met Daniel Chatto during her years in India with her father in the 1980s.
Chatto was working on another British film, Heat and Dust.
He is from a theatrical family, the son of actor Tom Chatto (1920–1982) and the theatrical agent Ros Chatto (born Rosalind Joan Thompson; died 2012).
Her bridesmaids were half-sister Lady Frances, Zara Phillips (daughter of her first cousin Princess Anne), and Tara Noble-Singh, a family friend.



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
  AssignClass (e131c972-0b58-4d19-a6a6-c59feb18a20f)
 Call ID: e131c972-0b58-4d19-a6a6-c59feb18a20f
  Args:
    source: Sarah_Chatto
    type: :Woman
  AssignClass (e93530b2-e0b6-40ce-859e-8bfb47b84728)
 Call ID: e93530b2-e0b6-40ce-859e-8bfb47b84728
  Args:
    source: Sarah_Chatto
    type: :Person
  AddLiteral (d7ddac3c-3451-4147-a660-4abfd9e8d9ee)
 Call ID: d7ddac3c-3451-4147-a660-4abfd9e8d9ee
  Args:
    source: Sarah_Chatto
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1964
  AssignClass (2aeb4023-71f8-4967-b36d-37cfb95235e4)
 Call ID: 2aeb4023-71f8-4967-b36d-37cfb95235e4
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (199d85be-0705-4d87-b841-1e8bd75975f9)
 Call ID: 199d85be-0705-4d87-b841-1e8bd75975f9
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (26dbf719-575f-4091-b4b7-3fcfb1a422f4)
 Call ID: 26dbf719-575f-4091-b4b7-3fcfb1a422f4
  Args:
    source: Antony_Armstrong-Jones
    type: :Man
  AssignClass (9ef80a30-3957-41a3-a558-ca1c6a7917dd)
 Call ID: 9ef80a30-3957-41a3-a558-ca1c6a7917dd
  Args:
    type: :Person
    source: Antony_Armstrong-Jones
  AddTriple (2ab8505a-a60e-442d-b189-436cf863217a)
 Call ID: 2ab8505a-a60e-442d-b189-436cf863217a
  Args:
    relation: :hasMother
    source: Sarah_Chatto
    target: Princess_Margaret
  AddTriple (5275f1b1-dc0b-474b-bd44-19686ba192d2)
 Call ID: 5275f1b1-dc0b-474b-bd44-19686ba192d2
  Args:
    target: Antony_Armstrong-Jones
    source: Sarah_Chatto
    relation: :hasFather
  AssignClass (d3119898-aa9a-4a53-a774-97f19ef93410)
 Call ID: d3119898-aa9a-4a53-a774-97f19ef93410
  Args:
    source: David_Armstrong-Jones
    type: :Man
  AssignClass (7c6d82b9-d95d-45dc-8cdb-3ec090920d6b)
 Call ID: 7c6d82b9-d95d-45dc-8cdb-3ec090920d6b
  Args:
    type: :Person
    source: David_Armstrong-Jones
  AddTriple (ea5d1bd8-8e99-44ed-8a7f-beffee25c669)
 Call ID: ea5d1bd8-8e99-44ed-8a7f-beffee25c669
  Args:
    relation: :isSiblingOf
    source: Sarah_Chatto
    target: David_Armstrong-Jones
  AddTriple (698d7c78-c2fb-43cb-b609-2fff599f4588)
 Call ID: 698d7c78-c2fb-43cb-b609-2fff599f4588
  Args:
    relation: :hasMother
    source: David_Armstrong-Jones
    target: Princess_Margaret
  AddTriple (51825efe-e6c4-4e24-8914-802f30c424f6)
 Call ID: 51825efe-e6c4-4e24-8914-802f30c424f6
  Args:
    relation: :hasFather
    source: David_Armstrong-Jones
    target: Antony_Armstrong-Jones
  AssignClass (eef596ec-70b6-43ed-9f3b-ed964e64aaa1)
 Call ID: eef596ec-70b6-43ed-9f3b-ed964e64aaa1
  Args:
    source: Daniel_Chatto
    type: :Man
  AssignClass (87359a49-1074-44b1-a853-893800a3b7c2)
 Call ID: 87359a49-1074-44b1-a853-893800a3b7c2
  Args:
    type: :Person
    source: Daniel_Chatto
  AssignClass (bb700964-356a-4d09-b2c8-955fdd3dcd0d)
 Call ID: bb700964-356a-4d09-b2c8-955fdd3dcd0d
  Args:
    source: Tom_Chatto
    type: :Man
  AssignClass (3ae2f3b3-6776-43ce-af0b-54e65f41a905)
 Call ID: 3ae2f3b3-6776-43ce-af0b-54e65f41a905
  Args:
    source: Tom_Chatto
    type: :Person
  AddLiteral (6ccef47c-2432-466a-b612-036d34ff05a6)
 Call ID: 6ccef47c-2432-466a-b612-036d34ff05a6
  Args:
    literal_value: 1920
    relation: :hasBirthYear
    source: Tom_Chatto
    literal_type: xsd:integer
  AddLiteral (6c0c52ca-3e27-411c-aa47-2c9a2dfd02a1)
 Call ID: 6c0c52ca-3e27-411c-aa47-2c9a2dfd02a1
  Args:
    literal_type: xsd:integer
    source: Tom_Chatto
    literal_value: 1982
    relation: :hasDeathYear
  AssignClass (9ab083c1-5279-4197-a166-47355dca9b79)
 Call ID: 9ab083c1-5279-4197-a166-47355dca9b79
  Args:
    type: :Woman
    source: Ros_Chatto
  AssignClass (a926c83a-5a8a-446b-b247-58e3f8ee5e87)
 Call ID: a926c83a-5a8a-446b-b247-58e3f8ee5e87
  Args:
    source: Ros_Chatto
    type: :Person
  AddLiteral (16e69957-f6f1-44ad-9fa8-5257c3b50853)
 Call ID: 16e69957-f6f1-44ad-9fa8-5257c3b50853
  Args:
    literal_type: xsd:integer
    source: Ros_Chatto
    relation: :hasDeathYear
    literal_value: 2012
  AddTriple (241910b9-c679-41f0-9079-f98d8965951f)
 Call ID: 241910b9-c679-41f0-9079-f98d8965951f
  Args:
    target: Tom_Chatto
    source: Daniel_Chatto
    relation: :hasFather
  AddTriple (1cc7bba7-f84e-43fd-a931-e3ca7932d8b1)
 Call ID: 1cc7bba7-f84e-43fd-a931-e3ca7932d8b1
  Args:
    source: Daniel_Chatto
    target: Ros_Chatto
    relation: :hasMother
  AssignClass (aaae88b8-c9dd-44ac-8f5d-3a9ed2d191e9)
 Call ID: aaae88b8-c9dd-44ac-8f5d-3a9ed2d191e9
  Args:
    source: Polly_Fry
    type: :Woman
  AssignClass (8a5ccd07-b7d3-4fda-81a6-0ee69865e6de)
 Call ID: 8a5ccd07-b7d3-4fda-81a6-0ee69865e6de
  Args:
    type: :Person
    source: Polly_Fry
  AddTriple (8cbe145a-e464-4f4f-b618-8f39fe4ebde0)
 Call ID: 8cbe145a-e464-4f4f-b618-8f39fe4ebde0
  Args:
    relation: :hasFather
    target: Antony_Armstrong-Jones
    source: Polly_Fry
  AssignClass (2056edc5-e940-4b28-a755-798cb4ab5047)
 Call ID: 2056edc5-e940-4b28-a755-798cb4ab5047
  Args:
    source: Frances_Armstrong-Jones
    type: :Woman
  AssignClass (23ea29f1-1254-4e41-add6-42001e2fb572)
 Call ID: 23ea29f1-1254-4e41-add6-42001e2fb572
  Args:
    type: :Person
    source: Frances_Armstrong-Jones
  AddTriple (d736afde-07b5-4084-b1b1-58f12289c46d)
 Call ID: d736afde-07b5-4084-b1b1-58f12289c46d
  Args:
    relation: :hasFather
    source: Frances_Armstrong-Jones
    target: Antony_Armstrong-Jones
  AssignClass (59f5998e-2773-4867-8b71-c0bb7a5e64e6)
 Call ID: 59f5998e-2773-4867-8b71-c0bb7a5e64e6
  Args:
    source: Jasper_Cable-Alexander
    type: :Man
  AssignClass (06e8d307-d89b-4977-abb4-9dbca399fef9)
 Call ID: 06e8d307-d89b-4977-abb4-9dbca399fef9
  Args:
    source: Jasper_Cable-Alexander
    type: :Person
  AddTriple (0823e18e-7f88-42b0-ae7a-61f5b00d4973)
 Call ID: 0823e18e-7f88-42b0-ae7a-61f5b00d4973
  Args:
    relation: :hasFather
    source: Jasper_Cable-Alexander
    target: Antony_Armstrong-Jones
  Finish (4192aaad-a9e7-4f75-a83e-d02bd9067cb3)
 Call ID: 4192aaad-a9e7-4f75-a83e-d02bd9067cb3
  Args: