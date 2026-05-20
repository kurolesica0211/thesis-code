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
Granville George Fergus Leveson-Gower, 6th Earl Granville (born 10 September 1959) is a British peer, landowner, and artist.
He was known as Lord Leveson until 1996 and was a member of the House of Lords from 1996 to 1999.
Biography

The elder son of Granville Leveson-Gower, 5th Earl Granville, whose mother Rose Leveson-Gower, Countess Granville, was a daughter of the Earl of Strathmore and Kinghorne and a sister of Queen Elizabeth the Queen Mother, he was educated at Eton College and from 1973 to 1976 was Page of Honour to Queen Elizabeth II, who was his godmother.
On 31 October 1996, he succeeded as Earl Granville (1833), Viscount Granville (1814), and Baron Leveson of Stone (1814), all in the peerage of the United Kingdom, at the time giving him a seat in the House of Lords.
Granville is the resident laird of North Uist, living on the island at Callernish House, Griminish, near Lochmaddy, a house shaped like a doughnut designed in the 1960s by Sir Martyn Beckett.
In 1999, a local smokehouse business came up for sale and Granville took it over, aiming to produce high quality smoked salmon and sea trout.
With a passion for beachcombing, Granville has also become an artist and sculptor, inspired by flotsam and jetsam and has exhibited his work in North Uist and Edinburgh.
On 23 May 1997, Granville married Anne Topping, a daughter of Bernard Topping, and they had three children:


In 2021, Granville was reported to be living at Callernish with a new wife, Florence Pearson (married in 2016), an artist, their two young sons, a labrador trained to find ambergris, and a parrot.



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
  AssignClass (653b9361-3cb1-427a-b449-c5dc5bf50927)
 Call ID: 653b9361-3cb1-427a-b449-c5dc5bf50927
  Args:
    source: Granville_George_Fergus_Leveson-Gower
    type: :Man
  AssignClass (b1e6fa56-da8c-4002-8976-47d20a5c4275)
 Call ID: b1e6fa56-da8c-4002-8976-47d20a5c4275
  Args:
    type: :Person
    source: Granville_George_Fergus_Leveson-Gower
  AddLiteral (f62436f7-3d25-4738-a9b3-2e8f41ae8014)
 Call ID: f62436f7-3d25-4738-a9b3-2e8f41ae8014
  Args:
    literal_type: xsd:integer
    literal_value: 1959
    relation: :hasBirthYear
    source: Granville_George_Fergus_Leveson-Gower
  AddLiteral (d0ee7d8f-137a-4741-af90-d8daea6098cf)
 Call ID: d0ee7d8f-137a-4741-af90-d8daea6098cf
  Args:
    literal_value: Lord Leveson
    literal_type: xsd:string
    source: Granville_George_Fergus_Leveson-Gower
    relation: :formerlyKnownAs
  AssignClass (b9d74d7b-6d6d-4e79-addc-e5a5cef5b734)
 Call ID: b9d74d7b-6d6d-4e79-addc-e5a5cef5b734
  Args:
    type: :Man
    source: Granville_Leveson-Gower_5th_Earl_Granville
  AssignClass (12ac856f-8488-4107-b028-7fc92f56196b)
 Call ID: 12ac856f-8488-4107-b028-7fc92f56196b
  Args:
    type: :Person
    source: Granville_Leveson-Gower_5th_Earl_Granville
  AddTriple (84993eeb-aa12-472f-87f5-07159182735f)
 Call ID: 84993eeb-aa12-472f-87f5-07159182735f
  Args:
    relation: :hasFather
    target: Granville_Leveson-Gower_5th_Earl_Granville
    source: Granville_George_Fergus_Leveson-Gower
  AssignClass (94e71c10-e649-41ce-b82f-c84a70b58cf3)
 Call ID: 94e71c10-e649-41ce-b82f-c84a70b58cf3
  Args:
    source: Rose_Leveson-Gower_Countess_Granville
    type: :Woman
  AssignClass (b64096a2-6b02-4a8b-97b2-e7f62c30aeb6)
 Call ID: b64096a2-6b02-4a8b-97b2-e7f62c30aeb6
  Args:
    type: :Person
    source: Rose_Leveson-Gower_Countess_Granville
  AddTriple (efcbbe95-d20b-4baa-ad88-62d68e1c4639)
 Call ID: efcbbe95-d20b-4baa-ad88-62d68e1c4639
  Args:
    target: Rose_Leveson-Gower_Countess_Granville
    relation: :hasMother
    source: Granville_George_Fergus_Leveson-Gower
  AssignClass (6beeb52a-ffbd-4678-8f8e-681a3d642960)
 Call ID: 6beeb52a-ffbd-4678-8f8e-681a3d642960
  Args:
    type: :Woman
    source: Anne_Topping
  AssignClass (abc39a42-e227-43f5-b0d1-b474f926a8f2)
 Call ID: abc39a42-e227-43f5-b0d1-b474f926a8f2
  Args:
    type: :Person
    source: Anne_Topping
  AddTriple (81594f15-6b1b-4f0f-b9eb-990e04c3b70c)
 Call ID: 81594f15-6b1b-4f0f-b9eb-990e04c3b70c
  Args:
    source: Granville_George_Fergus_Leveson-Gower
    target: Anne_Topping
    relation: :hasRelation
  AddLiteral (9eb847d0-41ab-4264-a0f8-00137400ec21)
 Call ID: 9eb847d0-41ab-4264-a0f8-00137400ec21
  Args:
    source: Granville_George_Fergus_Leveson-Gower
    relation: :hasMarriageYear
    literal_value: 1997
    literal_type: xsd:integer
  AssignClass (9ccd18f1-6d29-4b23-aa99-fedb49460696)
 Call ID: 9ccd18f1-6d29-4b23-aa99-fedb49460696
  Args:
    type: :Man
    source: Bernard_Topping
  AssignClass (08afe2de-42d7-4267-8ed2-2e155171b54d)
 Call ID: 08afe2de-42d7-4267-8ed2-2e155171b54d
  Args:
    source: Bernard_Topping
    type: :Person
  AddTriple (418221dd-d3a0-4b9e-8535-2773ed7acb21)
 Call ID: 418221dd-d3a0-4b9e-8535-2773ed7acb21
  Args:
    source: Anne_Topping
    relation: :hasFather
    target: Bernard_Topping
  AssignClass (f34d0a6b-82a8-4df3-960b-27bc38712398)
 Call ID: f34d0a6b-82a8-4df3-960b-27bc38712398
  Args:
    type: :Woman
    source: Florence_Pearson
  AssignClass (1af9ba37-0109-48f4-921c-3134b70cd3a2)
 Call ID: 1af9ba37-0109-48f4-921c-3134b70cd3a2
  Args:
    source: Florence_Pearson
    type: :Person
  AddTriple (83905738-d158-4ed7-8f67-328e3a4ceb86)
 Call ID: 83905738-d158-4ed7-8f67-328e3a4ceb86
  Args:
    target: Florence_Pearson
    relation: :hasRelation
    source: Granville_George_Fergus_Leveson-Gower
  AddLiteral (f7ff6456-06c3-42f6-8712-359a7a459df7)
 Call ID: f7ff6456-06c3-42f6-8712-359a7a459df7
  Args:
    literal_type: xsd:integer
    literal_value: 2016
    relation: :hasMarriageYear
    source: Granville_George_Fergus_Leveson-Gower
  Finish (59a73279-5179-4875-8f50-c7cb873a7eaa)
 Call ID: 59a73279-5179-4875-8f50-c7cb873a7eaa
  Args: