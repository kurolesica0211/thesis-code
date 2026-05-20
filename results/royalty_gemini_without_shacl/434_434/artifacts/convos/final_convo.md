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
Simon Patrick Bowes-Lyon, 19th and 6th Earl of Strathmore and Kinghorne (born 18 June 1986), styled as Lord Glamis until 2016, is a Scottish peer and landowner, the owner of estates based at Glamis Castle.
The eldest son of Michael Bowes-Lyon, 18th Earl of Strathmore and Kinghorne, and his first wife, Isobel Weatherall, he is a second cousin once removed of King Charles III, whose maternal grandmother was a Bowes-Lyon.
In 2021, Strathmore pleaded guilty to sexually assaulting a woman at his ancestral home, Glamis Castle, and as a result served five months in prison.
Biography

Simon Patrick Bowes-Lyon was born on 18 June 1986 into the Bowes-Lyon family.
His father, Michael Bowes-Lyon, 18th Earl of Strathmore and Kinghorne, was a politician, soldier, and businessman, as well as a hereditary peer.
His mother is Isobel Weatherall, daughter of Captain Anthony Edward Weatherall.
Strathmore is a great-great-nephew of Queen Elizabeth the Queen Mother and thus a second cousin once removed of King Charles III and third cousin of his son, Prince William.
On his father's death on 27 February 2016, the then-Lord Glamis succeeded as 19th Earl.
In 2017 Strathmore decided to renovate Glamis House, a property on his estate and a childhood home of the Queen Mother, for use as a self-catering holiday home.
From 2016 to 2018, he was a director of Ark Hill Wind Farm Ltd. Strathmore is the chieftain of the Strathmore Highland Games, which takes place annually in the grounds of Glamis Castle.
COVID-19 violation

In June 2020, Durham Police contacted the Earl for violating the COVID-19-related travel restrictions then in place.
A report said Strathmore travelled 200 miles (320 km) to Holwick Lodge, Middleton-in-Teesdale, and that his butler was spotted buying newspapers.
Sexual assault conviction

In 2021, Strathmore was charged with sexual assault after admitting to attacking a 26-year-old woman at his Scottish home, Glamis Castle, in early 2020.
On 12 January 2021, Strathmore was granted bail and placed on the Violent and Sex Offender Register (ViSOR) by Sheriff Alistair Carmichael at Dundee Sheriff Court.
The Times reported calls for Strathmore to be removed as the Chieftain of the annual Strathmore Highland Games and as the President of the Angus Ball.
Drink driving conviction

On 10 November 2023, the Earl was convicted of drink driving at Perth Sheriff Court.
The Earl gave a reading of 55 mcg per 100 ml of breath; the legal limit is 22 mcg, therefore, he was 2.5 times over the legal limit.
Titles and styles

In addition to the Earldom of Strathmore and Kinghorne, Strathmore holds the following subsidiary titles: 17th Viscount Lyon, 19th Lord Lyon and Glamis, 26th Lord Glamis, 17th Lord Glamis, Tannadyce, Sidlaw and Strathdichtie, and 7th Baron Bowes, of Streatlam Castle.



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
  AssignClass (e75c31a5-9d53-4e23-a95d-81d456083782)
 Call ID: e75c31a5-9d53-4e23-a95d-81d456083782
  Args:
    type: :Man
    source: Simon_Patrick_Bowes-Lyon
  AssignClass (792e30a7-30e0-41dc-8793-ffcb97e96358)
 Call ID: 792e30a7-30e0-41dc-8793-ffcb97e96358
  Args:
    type: :Man
    source: Michael_Bowes-Lyon
  AssignClass (ea719331-784f-4dc3-8c5a-708d4ecd8416)
 Call ID: ea719331-784f-4dc3-8c5a-708d4ecd8416
  Args:
    type: :Woman
    source: Isobel_Weatherall
  AssignClass (fda4d55d-b439-406c-94b1-a0fa23efccb0)
 Call ID: fda4d55d-b439-406c-94b1-a0fa23efccb0
  Args:
    type: :Man
    source: Anthony_Edward_Weatherall
  AddLiteral (fe9552d7-80db-4606-9e93-a7242a89722f)
 Call ID: fe9552d7-80db-4606-9e93-a7242a89722f
  Args:
    relation: :hasBirthYear
    literal_value: 1986
    literal_type: xsd:integer
    source: Simon_Patrick_Bowes-Lyon
  AddTriple (c34906cd-fa3a-43dc-b4fe-81782985aa0a)
 Call ID: c34906cd-fa3a-43dc-b4fe-81782985aa0a
  Args:
    source: Simon_Patrick_Bowes-Lyon
    target: Michael_Bowes-Lyon
    relation: :hasFather
  AddTriple (e94cca56-4797-4e24-a76a-993906ea1a8a)
 Call ID: e94cca56-4797-4e24-a76a-993906ea1a8a
  Args:
    target: Isobel_Weatherall
    relation: :hasMother
    source: Simon_Patrick_Bowes-Lyon
  AddTriple (ed464112-b1a2-4031-8dcf-ad92b5841d98)
 Call ID: ed464112-b1a2-4031-8dcf-ad92b5841d98
  Args:
    source: Isobel_Weatherall
    relation: :hasFather
    target: Anthony_Edward_Weatherall
  AddTriple (ed05f26e-af28-4f86-b6e3-78d7d0d72f8a)
 Call ID: ed05f26e-af28-4f86-b6e3-78d7d0d72f8a
  Args:
    source: Simon_Patrick_Bowes-Lyon
    relation: :hasSex
    target: :Male
  AddTriple (bed54a6d-9d0a-45f6-9818-3769bd8d5271)
 Call ID: bed54a6d-9d0a-45f6-9818-3769bd8d5271
  Args:
    source: Michael_Bowes-Lyon
    relation: :hasSex
    target: :Male
  AddTriple (ef9712b9-a488-4aca-9a72-4518fe0aaea1)
 Call ID: ef9712b9-a488-4aca-9a72-4518fe0aaea1
  Args:
    source: Isobel_Weatherall
    relation: :hasSex
    target: :Female
  AddTriple (cc9daf42-3981-4404-8c05-f15f85066371)
 Call ID: cc9daf42-3981-4404-8c05-f15f85066371
  Args:
    source: Anthony_Edward_Weatherall
    target: :Male
    relation: :hasSex
  Finish (005383f1-684e-4204-a2a1-62ca4864cc1b)
 Call ID: 005383f1-684e-4204-a2a1-62ca4864cc1b
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Simon_Patrick_Bowes-Lyon a :Man ;
      :hasBirthYear 1986 ;
      :hasFather data:Michael_Bowes-Lyon ;
      :hasMother data:Isobel_Weatherall ;
      :hasSex data:Male .

  data:Anthony_Edward_Weatherall a :Man ;
      :hasSex data:Male .

  data:Isobel_Weatherall a :Woman ;
      :hasFather data:Anthony_Edward_Weatherall ;
      :hasSex data:Female .

  data:Michael_Bowes-Lyon a :Man ;
      :hasSex data:Male .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['Male', 'Female']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (4016b977-50a1-46e8-a22f-98bf1df0ed6f)
 Call ID: 4016b977-50a1-46e8-a22f-98bf1df0ed6f
  Args:
    type: :Sex
    source: Male
  AssignClass (84744bcc-8d11-40e8-b1b5-019e5c63b7da)
 Call ID: 84744bcc-8d11-40e8-b1b5-019e5c63b7da
  Args:
    source: Female
    type: :Sex
  Finish (c42524ad-d8c0-4c75-9dea-f937227f36ef)
 Call ID: c42524ad-d8c0-4c75-9dea-f937227f36ef
  Args: