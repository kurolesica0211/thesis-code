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
James Alexander Philip Theo Mountbatten-Windsor, Earl of Wessex (born 17 December 2007), styled Viscount Severn until 2023, is a member of the British royal family.
He is the younger child and only son of Prince Edward, Duke of Edinburgh, and Sophie, Duchess of Edinburgh.
James is the youngest grandchild of Queen Elizabeth II and Prince Philip, Duke of Edinburgh, and a nephew of King Charles III.
Infancy

James Alexander Philip Theo Mountbatten-Windsor was born at 4:20 pm on 17 December 2007 at Frimley Park Hospital, Surrey by caesarean section.
His father Prince Edward, Duke of Edinburgh, is the youngest child of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
His mother Sophie, Duchess of Edinburgh, worked in public relations before becoming a full-time member of the royal family after her marriage in 1999.
His full name, James Alexander Philip Theo, was announced on 21 December.
James was baptised on 19 April 2008 in the private chapel at Windsor Castle by David Conner, Dean of Windsor, witnessed by his godparents, Alastair Bruce, Duncan Bullivant, Thomas Hill, Denise Poulton, Jeanye Irwin, and his paternal grandparents, Elizabeth II and Prince Philip.
Education

James attended Eagle House School, a coeducational preparatory school near Sandhurst, Berkshire, from 2011 to 2021, before enrolling at the private Radley College in Oxfordshire.
Official appearances

James made his first official appearance in the carriage procession at Trooping the Colour in 2016, and also took part in the 2022 Trooping the Colour.
Following the thanksgiving memorial service for his grandfather Prince Philip on 29 March 2022, James attended the Platinum Jubilee National Service of Thanksgiving and the Platinum Party at the Palace in June 2022.
On 17 September 2022, during the period of official mourning for his grandmother Queen Elizabeth II, James joined his sister Louise and six cousins in mounting a 15-minute vigil around the Queen's coffin as it lay in state at Westminster Hall.
On 6 May 2023, James, who then held the courtesy title Earl of Wessex, attended his uncle Charles III's coronation at Westminster Abbey, together with the rest of the royal family.
The following day, he attended the Coronation Concert at Windsor Castle.
On 31 March 2024, James attended the Easter Matins Service at St. George's Chapel, Windsor Castle, with his mother and father.
James was accorded this courtesy title at birth as heir apparent to his father's earldom.
At birth, James automatically became a prince of the United Kingdom (Prince James of Wessex, now Prince James of Edinburgh) under the terms of the 1917 letters patent, which assigned princely status and the style of Royal Highness to all male-line grandchildren of a sovereign.
However, when his parents married, Buckingham Palace announced that their children would be styled as the children of an earl rather than as prince or princess.
In 2020, James's mother reaffirmed that James and his sister retained the right to their royal titles and styles, and could choose whether to use them from the age of 18.
When his father was created Duke of Edinburgh in March 2023, James became styled by courtesy as Earl of Wessex, the family's senior subsidiary title.
The Dukedom of Edinburgh, having been created as a life peerage, will become extinct upon his father's death, but James remains heir apparent to his father's hereditary peerages of Earl of Wessex, Earl of Forfar, and Viscount Severn.
Honours and decorations

In June 2008, to recognise Prince Edward's visit to the Canadian province of Manitoba, a lake in the north of the province was named Lake James.
James's sister was similarly honoured by Lake Louise in the same province.



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
  AssignClass (49e5e21e-580b-4c7a-8b8c-2b8a2a711678)
 Call ID: 49e5e21e-580b-4c7a-8b8c-2b8a2a711678
  Args:
    type: :Man
    source: James_Alexander_Philip_Theo_Mountbatten-Windsor
  AssignClass (fd1d804b-4bdd-4e82-aaf6-8dc283af3f3b)
 Call ID: fd1d804b-4bdd-4e82-aaf6-8dc283af3f3b
  Args:
    type: :Person
    source: James_Alexander_Philip_Theo_Mountbatten-Windsor
  AssignClass (21cd10d2-31c9-4de2-904b-0dab943759c0)
 Call ID: 21cd10d2-31c9-4de2-904b-0dab943759c0
  Args:
    type: :Man
    source: Prince_Edward_Duke_of_Edinburgh
  AssignClass (adafc8cf-a8cc-44bf-98b2-9279c4e054f7)
 Call ID: adafc8cf-a8cc-44bf-98b2-9279c4e054f7
  Args:
    type: :Person
    source: Prince_Edward_Duke_of_Edinburgh
  AssignClass (50f7c06e-c938-4185-94b9-52c85ec7f2c0)
 Call ID: 50f7c06e-c938-4185-94b9-52c85ec7f2c0
  Args:
    type: :Ancestor
    source: Prince_Edward_Duke_of_Edinburgh
  AssignClass (8c0da115-7a51-4d83-841d-eeb30af4f7f5)
 Call ID: 8c0da115-7a51-4d83-841d-eeb30af4f7f5
  Args:
    type: :Woman
    source: Sophie_Duchess_of_Edinburgh
  AssignClass (621fc74e-aad1-456a-9ca2-1f2cf3178b5e)
 Call ID: 621fc74e-aad1-456a-9ca2-1f2cf3178b5e
  Args:
    type: :Person
    source: Sophie_Duchess_of_Edinburgh
  AssignClass (5de1dc30-0306-4668-a9cd-d41fb7fe6ecb)
 Call ID: 5de1dc30-0306-4668-a9cd-d41fb7fe6ecb
  Args:
    source: Sophie_Duchess_of_Edinburgh
    type: :Ancestor
  AssignClass (0d10286c-bf74-4a27-ba51-07e4a7e21b83)
 Call ID: 0d10286c-bf74-4a27-ba51-07e4a7e21b83
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (698b2bd5-9082-4a65-bdbe-d9de40ce73d1)
 Call ID: 698b2bd5-9082-4a65-bdbe-d9de40ce73d1
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AssignClass (c6f1b9da-25d8-4d33-a427-b8e8fb8b4de9)
 Call ID: c6f1b9da-25d8-4d33-a427-b8e8fb8b4de9
  Args:
    source: Queen_Elizabeth_II
    type: :Ancestor
  AssignClass (cff1bd4b-76cc-4de1-9d9f-59e8c93f87f2)
 Call ID: cff1bd4b-76cc-4de1-9d9f-59e8c93f87f2
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (7025630e-db4f-44ee-89af-39bb45d0c3a9)
 Call ID: 7025630e-db4f-44ee-89af-39bb45d0c3a9
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AssignClass (a7d95de0-1da5-4873-bfd5-20a32901c14b)
 Call ID: a7d95de0-1da5-4873-bfd5-20a32901c14b
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Ancestor
  AssignClass (0c885111-5f4c-458b-9510-132b4a27f61f)
 Call ID: 0c885111-5f4c-458b-9510-132b4a27f61f
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (1d1149a9-a585-4d90-85d0-47530d666047)
 Call ID: 1d1149a9-a585-4d90-85d0-47530d666047
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (c48d89b2-72cc-4660-a489-c7e78228f333)
 Call ID: c48d89b2-72cc-4660-a489-c7e78228f333
  Args:
    source: Louise
    type: :Woman
  AssignClass (40109240-2a6a-4449-beee-4188790b38ec)
 Call ID: 40109240-2a6a-4449-beee-4188790b38ec
  Args:
    source: Louise
    type: :Person
  AddLiteral (309438a2-1906-4d59-bc41-97b80d91e760)
 Call ID: 309438a2-1906-4d59-bc41-97b80d91e760
  Args:
    relation: :hasBirthYear
    literal_value: 2007
    literal_type: xsd:integer
    source: James_Alexander_Philip_Theo_Mountbatten-Windsor
  AddTriple (c0488434-6480-4c36-bd8f-32d15d8c91f0)
 Call ID: c0488434-6480-4c36-bd8f-32d15d8c91f0
  Args:
    relation: :hasFather
    source: James_Alexander_Philip_Theo_Mountbatten-Windsor
    target: Prince_Edward_Duke_of_Edinburgh
  AddTriple (ece9df85-fac6-4b8e-b3ab-0d66d49697e7)
 Call ID: ece9df85-fac6-4b8e-b3ab-0d66d49697e7
  Args:
    relation: :hasMother
    source: James_Alexander_Philip_Theo_Mountbatten-Windsor
    target: Sophie_Duchess_of_Edinburgh
  AddTriple (a371894f-e365-4fa7-a6b0-0b5d437e621a)
 Call ID: a371894f-e365-4fa7-a6b0-0b5d437e621a
  Args:
    source: Prince_Edward_Duke_of_Edinburgh
    target: Prince_Philip_Duke_of_Edinburgh
    relation: :hasFather
  AddTriple (795c756a-cc79-4501-83a3-2bb4b38c8623)
 Call ID: 795c756a-cc79-4501-83a3-2bb4b38c8623
  Args:
    target: Queen_Elizabeth_II
    source: Prince_Edward_Duke_of_Edinburgh
    relation: :hasMother
  AddTriple (043212c3-1c55-4439-8dd8-f42ccc1e320c)
 Call ID: 043212c3-1c55-4439-8dd8-f42ccc1e320c
  Args:
    relation: :hasSister
    target: Louise
    source: James_Alexander_Philip_Theo_Mountbatten-Windsor
  AddTriple (da0fb638-bd36-464f-89b4-2470c265f13c)
 Call ID: da0fb638-bd36-464f-89b4-2470c265f13c
  Args:
    relation: :hasFather
    target: Prince_Edward_Duke_of_Edinburgh
    source: Louise
  AddTriple (e8661812-4434-474b-90d7-0bd14ab5af71)
 Call ID: e8661812-4434-474b-90d7-0bd14ab5af71
  Args:
    relation: :hasMother
    target: Sophie_Duchess_of_Edinburgh
    source: Louise
  Finish (3a2c4474-1995-47d4-90ce-3b2fbdc8df2c)
 Call ID: 3a2c4474-1995-47d4-90ce-3b2fbdc8df2c
  Args: