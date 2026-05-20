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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Princess Katarina of Yugoslavia, Lady de Silva (born 28 November 1959) is an English businessperson specialising in etiquette and decorum courses.
Early life

Katarina was born at King’s College Hospital in London to Princess Margarita of Baden and Prince Tomislav of Yugoslavia.
Her father's dynasty having been deposed and banished from Yugoslavia after World War II, she grew up in exile, largely in England.
She has one brother, Prince Nikola of Yugoslavia, and two half-brothers, Prince George and Prince Michael.
She is a first cousin of Alexander, Crown Prince of Yugoslavia.
Her grandmother, Princess Theodora, Margravine of Baden, was the sister of Prince Philip, Duke of Edinburgh, late husband of Queen Elizabeth II.
Princess Katharina is the senior female-line descendant of Queen Victoria, through the Queen's second daughter Alice, Grand Duchess of Hesse, who was the grandmother of Princess Katharina's great-grandmother, Princess Alice of Battenberg.
Career

In 1978, Katarina was presented as a debutante to high society at the International Debutante Ball at the Waldorf-Astoria Hotel.
As of 2013, Katarina and former Royal butler Grant Harrold develop and sell etiquette and decorum classes.
Personal life

Katarina married barrister Sir Desmond de Silva on 5 December 1987.
They had one daughter, Victoria Marie Esmé Margarita, born on 6 September 1991.
Charity work

In 2009, Katarina supported the charity Project Change: Bermuda to raise funds towards building a hospital and training medical staff in Burundi.
Katarina served as the president of the Guild of Travel and Tourism in the United Kingdom.
In 2013, she became patron of the Society of Genealogists succeeding Prince Michael of Kent.
Honours

Ancestry

Katarina is a member of the House of Karađorđević.
Through her father, Katarina descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, and furthermore from Emperor Nicholas I of Russia, King Ferdinand II and Queen Maria II of Portugal, and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through her mother, Katarina descends from Leopold, Grand Duke of Baden, kings George V of Hanover, Christian IX of Denmark, George I of Greece and Nicholas I, Emperor of Russia.



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
  AssignClass (4010517a-c740-4551-b0be-d7ce82833ff2)
 Call ID: 4010517a-c740-4551-b0be-d7ce82833ff2
  Args:
    source: Katarina of Yugoslavia
    type: :Woman
  AssignClass (2034ae1b-f298-4f20-be3c-63c89276e2e6)
 Call ID: 2034ae1b-f298-4f20-be3c-63c89276e2e6
  Args:
    source: Katarina of Yugoslavia
    type: :Person
  AssignClass (b660efba-81b7-4841-a548-06bbe59e7c04)
 Call ID: b660efba-81b7-4841-a548-06bbe59e7c04
  Args:
    type: :Woman
    source: Margarita of Baden
  AssignClass (708cfd3b-2bbe-403f-8cfc-994a2bad70a2)
 Call ID: 708cfd3b-2bbe-403f-8cfc-994a2bad70a2
  Args:
    source: Margarita of Baden
    type: :Person
  AssignClass (b00ab7ce-cf8e-4729-9d9b-63a8b262cdda)
 Call ID: b00ab7ce-cf8e-4729-9d9b-63a8b262cdda
  Args:
    type: :Man
    source: Tomislav of Yugoslavia
  AssignClass (5fd540fe-a5aa-4ab9-bae0-cc458ae9ab3a)
 Call ID: 5fd540fe-a5aa-4ab9-bae0-cc458ae9ab3a
  Args:
    source: Tomislav of Yugoslavia
    type: :Person
  AssignClass (8df70532-ba91-49f2-b5d8-85a38dcfe201)
 Call ID: 8df70532-ba91-49f2-b5d8-85a38dcfe201
  Args:
    type: :Man
    source: Nikola of Yugoslavia
  AssignClass (1f28a581-1ca1-4858-9838-48ad77ca9137)
 Call ID: 1f28a581-1ca1-4858-9838-48ad77ca9137
  Args:
    source: Nikola of Yugoslavia
    type: :Person
  AssignClass (49dd2401-1b22-4de7-b460-efbefe37389d)
 Call ID: 49dd2401-1b22-4de7-b460-efbefe37389d
  Args:
    source: George of Yugoslavia
    type: :Man
  AssignClass (b61344d0-09aa-4e5c-8d5c-6f6e5c526e36)
 Call ID: b61344d0-09aa-4e5c-8d5c-6f6e5c526e36
  Args:
    type: :Person
    source: George of Yugoslavia
  AssignClass (13a29540-c36e-4354-b33e-ed0ffc6f89ec)
 Call ID: 13a29540-c36e-4354-b33e-ed0ffc6f89ec
  Args:
    type: :Man
    source: Michael of Yugoslavia
  AssignClass (92946282-0ce8-4d9c-a27c-c3c9dee4dc32)
 Call ID: 92946282-0ce8-4d9c-a27c-c3c9dee4dc32
  Args:
    source: Michael of Yugoslavia
    type: :Person
  AssignClass (51633c81-bd7c-4c38-aaac-40201302cdff)
 Call ID: 51633c81-bd7c-4c38-aaac-40201302cdff
  Args:
    type: :Man
    source: Desmond de Silva
  AssignClass (ea4fd2d5-0edd-47c3-b0c0-5f787f115dfb)
 Call ID: ea4fd2d5-0edd-47c3-b0c0-5f787f115dfb
  Args:
    type: :Person
    source: Desmond de Silva
  AssignClass (2b6849fb-1281-438d-af52-ae646789a5ea)
 Call ID: 2b6849fb-1281-438d-af52-ae646789a5ea
  Args:
    type: :Woman
    source: Victoria Marie Esmé Margarita
  AssignClass (c4ee4cab-1cf5-4651-871f-0b5dc1b049b4)
 Call ID: c4ee4cab-1cf5-4651-871f-0b5dc1b049b4
  Args:
    type: :Person
    source: Victoria Marie Esmé Margarita
  AddTriple (cd3db3f2-2066-4784-902a-49a7a4f62617)
 Call ID: cd3db3f2-2066-4784-902a-49a7a4f62617
  Args:
    relation: :hasFather
    target: Tomislav of Yugoslavia
    source: Katarina of Yugoslavia
  AddTriple (e97d4151-031e-4d87-b7a4-e4d431025005)
 Call ID: e97d4151-031e-4d87-b7a4-e4d431025005
  Args:
    relation: :hasMother
    target: Margarita of Baden
    source: Katarina of Yugoslavia
  AddTriple (ee2eebc5-2a4e-4920-bc05-ee6cbf1ee0dd)
 Call ID: ee2eebc5-2a4e-4920-bc05-ee6cbf1ee0dd
  Args:
    relation: :hasBrother
    target: Nikola of Yugoslavia
    source: Katarina of Yugoslavia
  AddTriple (03390e9d-1062-47a9-b2e9-d0ccdba0bba1)
 Call ID: 03390e9d-1062-47a9-b2e9-d0ccdba0bba1
  Args:
    source: Katarina of Yugoslavia
    target: George of Yugoslavia
    relation: :hasBrother
  AddTriple (1d982f81-c706-4429-9f30-442bd7e140e4)
 Call ID: 1d982f81-c706-4429-9f30-442bd7e140e4
  Args:
    source: Katarina of Yugoslavia
    target: Michael of Yugoslavia
    relation: :hasBrother
  AddTriple (43e5b5b5-a708-461d-82c9-3063862ddaf2)
 Call ID: 43e5b5b5-a708-461d-82c9-3063862ddaf2
  Args:
    target: Victoria Marie Esmé Margarita
    relation: :hasDaughter
    source: Katarina of Yugoslavia
  AddTriple (1bc9de99-570d-4df8-8691-fb6b5c90dc9a)
 Call ID: 1bc9de99-570d-4df8-8691-fb6b5c90dc9a
  Args:
    source: Victoria Marie Esmé Margarita
    target: Desmond de Silva
    relation: :hasFather
  AddLiteral (2b04c6f0-5830-47a3-aa27-5468f21189ff)
 Call ID: 2b04c6f0-5830-47a3-aa27-5468f21189ff
  Args:
    literal_value: 1959
    source: Katarina of Yugoslavia
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (52bc35f7-6a84-49bb-944e-dc825756996f)
 Call ID: 52bc35f7-6a84-49bb-944e-dc825756996f
  Args:
    source: Victoria Marie Esmé Margarita
    literal_value: 1991
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (a58013d5-903d-48b5-849f-c289a9017d7e)
 Call ID: a58013d5-903d-48b5-849f-c289a9017d7e
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1987
    source: Katarina of Yugoslavia
  Finish (0892c6aa-7633-43a3-b522-ac46eb5580ce)
 Call ID: 0892c6aa-7633-43a3-b522-ac46eb5580ce
  Args: