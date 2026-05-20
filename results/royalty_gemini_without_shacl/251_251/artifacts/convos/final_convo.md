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
Michael Fergus Bowes-Lyon, 18th and 5th Earl of Strathmore and Kinghorne (7 June 1957 – 27 February 2016), styled Lord Glamis between 1972 and 1987, also known as Mikey Strathmore, was a British Conservative politician, Scots Guards officer and stockbroker.
He was a first cousin once removed of Queen Elizabeth II, and second cousin of King Charles III.
Early life and education

Strathmore was born on 7 June 1957 in Windsor, the only son of Fergus Bowes-Lyon, later 17th Earl of Strathmore and Kinghorne, and his wife, Mary Pamela McCorquodale.
His paternal grandfather, Lieutenant-Colonel The Honourable Michael Bowes-Lyon, was an elder brother of Queen Elizabeth the Queen Mother, thus making Michael a first cousin once removed of Queen Elizabeth II and Princess Margaret.
He served as the Queen Mother's page of honour from 1971 to 1973 and often stayed with her at the Castle of Mey and the Royal Lodge, Windsor.
He was raised in Humbie, East Lothian, with his two sisters, Elizabeth and Diana.
Career

After Sandhurst, Strathmore was commissioned in the Scots Guards in 1980.
In 1987, Strathmore succeeded his father as 18th Earl of Strathmore and Kinghorne and inherited Holwick Hall in Teesdale, County Durham, and Glamis Castle, the Queen Mother's girlhood home, in Angus.
After resigning his ministerial post, Strathmore sat on the board of Polypipe from 1994 until it was acquired by IMI plc in 1999.
He also served as president of Boys' Brigade from 1994 to 1999 and as patron of the Friends of the Bowes Museum in County Durham, a position he inherited from the Queen Mother.
Personal life

Strathmore was married three times.
On 14 November 1984, Lord Glamis, as he was then, married Isobel Charlotte Weatherall (born c. 1962), great-granddaughter of Henry Keswick and sister of Percy Weatherall, at St James's Church, Piccadilly, with the Queen Mother in attendance.
Strathmore and Weatherall were separated in 2003 and divorced in 2005.
On 24 November 2005, Strathmore married Damaris Stuart-William, a clinical psychologist.
They had one son:


On 4 August 2012, Strathmore married Karen Baxter (née Orrock), who survived him.
As a hobby, he restored old automobiles and lorries, often featuring in the Strathmore Vintage Vehicle Rally.
In 2002, as the head of the Bowes-Lyon family, he walked behind the Queen Mother's coffin during her funeral procession and attended the private service of committal in the King George VI Memorial Chapel.
Strathmore died of colorectal cancer on 27 February 2016 in London, aged 58.
A memorial service was held at the Church of St Mary the Virgin in Middleton-in-Teesdale, near his County Durham properties, on 12 May and another, attended by Prince Charles, was held at St Martin-in-the-Fields in London on 8 June.



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
  AssignClass (39c0291a-4664-41d3-a144-a7ef348fa659)
 Call ID: 39c0291a-4664-41d3-a144-a7ef348fa659
  Args:
    type: :Man
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (1fa5a1dc-770d-40cb-afd6-adb708feafab)
 Call ID: 1fa5a1dc-770d-40cb-afd6-adb708feafab
  Args:
    type: :Person
    source: :Michael_Fergus_Bowes-Lyon
  AddLiteral (bcb19799-bcaf-44c9-a0e0-b87d6a6afff8)
 Call ID: bcb19799-bcaf-44c9-a0e0-b87d6a6afff8
  Args:
    literal_value: Mikey Strathmore
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Michael_Fergus_Bowes-Lyon
  AddLiteral (520f7b38-775b-479d-881d-d74a3a8fadb7)
 Call ID: 520f7b38-775b-479d-881d-d74a3a8fadb7
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1957
    relation: :hasBirthYear
  AddLiteral (2f130778-ce38-48bf-b409-599853644149)
 Call ID: 2f130778-ce38-48bf-b409-599853644149
  Args:
    relation: :hasDeathYear
    literal_value: 2016
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
  AssignClass (18de7c3b-7e50-4d9a-b3ef-977b06355981)
 Call ID: 18de7c3b-7e50-4d9a-b3ef-977b06355981
  Args:
    type: :Man
    source: :Fergus_Bowes-Lyon
  AssignClass (57d7caa6-3eea-442f-b7fa-59a0b66b93a1)
 Call ID: 57d7caa6-3eea-442f-b7fa-59a0b66b93a1
  Args:
    type: :Person
    source: :Fergus_Bowes-Lyon
  AddTriple (96927cfc-5ec6-48c1-98cc-b058c95f1a2d)
 Call ID: 96927cfc-5ec6-48c1-98cc-b058c95f1a2d
  Args:
    relation: :hasFather
    target: :Fergus_Bowes-Lyon
    source: :Michael_Fergus_Bowes-Lyon
  AssignClass (ad04982e-40c4-4ab1-aaba-401f13d05405)
 Call ID: ad04982e-40c4-4ab1-aaba-401f13d05405
  Args:
    type: :Woman
    source: :Mary_Pamela_McCorquodale
  AssignClass (686dcf97-83fd-4c4a-a2c8-4779f39b461c)
 Call ID: 686dcf97-83fd-4c4a-a2c8-4779f39b461c
  Args:
    type: :Person
    source: :Mary_Pamela_McCorquodale
  AddTriple (4d51aac2-19bc-4c54-a227-efa3271526ea)
 Call ID: 4d51aac2-19bc-4c54-a227-efa3271526ea
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    target: :Mary_Pamela_McCorquodale
    relation: :hasMother
  AssignClass (40506aeb-6068-4788-b1bd-236e3898ab35)
 Call ID: 40506aeb-6068-4788-b1bd-236e3898ab35
  Args:
    type: :Woman
    source: :Elizabeth_Bowes-Lyon_sister
  AssignClass (51486875-12ad-4244-b1a3-e90e794a8b76)
 Call ID: 51486875-12ad-4244-b1a3-e90e794a8b76
  Args:
    type: :Person
    source: :Elizabeth_Bowes-Lyon_sister
  AddTriple (2b88c486-5605-4c6e-bf7c-92e63e805fb6)
 Call ID: 2b88c486-5605-4c6e-bf7c-92e63e805fb6
  Args:
    target: :Elizabeth_Bowes-Lyon_sister
    source: :Michael_Fergus_Bowes-Lyon
    relation: :hasSister
  AssignClass (2a5b117b-554a-4e69-b764-c4fcf371b4c3)
 Call ID: 2a5b117b-554a-4e69-b764-c4fcf371b4c3
  Args:
    type: :Woman
    source: :Diana_Bowes-Lyon
  AssignClass (910d84dd-71b0-456c-9c75-49554e90b8a0)
 Call ID: 910d84dd-71b0-456c-9c75-49554e90b8a0
  Args:
    type: :Person
    source: :Diana_Bowes-Lyon
  AddTriple (33d8473b-57a4-4336-9fc0-8f0ce6991bec)
 Call ID: 33d8473b-57a4-4336-9fc0-8f0ce6991bec
  Args:
    target: :Diana_Bowes-Lyon
    source: :Michael_Fergus_Bowes-Lyon
    relation: :hasSister
  AssignClass (1aaad8cd-041e-47d3-afcd-83a92834f5d2)
 Call ID: 1aaad8cd-041e-47d3-afcd-83a92834f5d2
  Args:
    type: :Man
    source: :Michael_Bowes-Lyon_grandfather
  AssignClass (867f681f-8c0d-4af4-bc96-25c43d20251f)
 Call ID: 867f681f-8c0d-4af4-bc96-25c43d20251f
  Args:
    type: :Person
    source: :Michael_Bowes-Lyon_grandfather
  AddTriple (9126ea10-e38b-4343-9e8c-6ca43fd0f90e)
 Call ID: 9126ea10-e38b-4343-9e8c-6ca43fd0f90e
  Args:
    relation: :hasFather
    source: :Fergus_Bowes-Lyon
    target: :Michael_Bowes-Lyon_grandfather
  AssignClass (e617c73e-293a-4aee-8761-0cb06a61cf4d)
 Call ID: e617c73e-293a-4aee-8761-0cb06a61cf4d
  Args:
    type: :Woman
    source: :Isobel_Charlotte_Weatherall
  AssignClass (4b9a5614-3d5e-4e52-907a-b36ddbfe0dfe)
 Call ID: 4b9a5614-3d5e-4e52-907a-b36ddbfe0dfe
  Args:
    type: :Person
    source: :Isobel_Charlotte_Weatherall
  AddLiteral (9e8227da-3c73-453c-b982-da207a5749b3)
 Call ID: 9e8227da-3c73-453c-b982-da207a5749b3
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1984
    relation: :hasMarriageYear
  AssignClass (0cde29c7-ce74-42e2-8d93-1174f8edbaeb)
 Call ID: 0cde29c7-ce74-42e2-8d93-1174f8edbaeb
  Args:
    type: :Woman
    source: :Damaris_Stuart-William
  AssignClass (4d29d3f5-6cda-44c6-8275-ba55cbe5d7d4)
 Call ID: 4d29d3f5-6cda-44c6-8275-ba55cbe5d7d4
  Args:
    type: :Person
    source: :Damaris_Stuart-William
  AddLiteral (ef509bf9-937b-4be6-b13b-75cb0bb97b5c)
 Call ID: ef509bf9-937b-4be6-b13b-75cb0bb97b5c
  Args:
    literal_type: xsd:integer
    source: :Michael_Fergus_Bowes-Lyon
    literal_value: 2005
    relation: :hasMarriageYear
  AssignClass (9a8c2767-20bc-4d1a-8095-994bd844705b)
 Call ID: 9a8c2767-20bc-4d1a-8095-994bd844705b
  Args:
    type: :Woman
    source: :Karen_Baxter
  AssignClass (8728fe4b-5109-4514-90c4-2e3c4d4f9773)
 Call ID: 8728fe4b-5109-4514-90c4-2e3c4d4f9773
  Args:
    type: :Person
    source: :Karen_Baxter
  AddLiteral (64d33016-c33f-4038-9117-c159d198a059)
 Call ID: 64d33016-c33f-4038-9117-c159d198a059
  Args:
    source: :Michael_Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 2012
    relation: :hasMarriageYear
  Finish (0acb0931-e209-4133-a655-605ec50919ec)
 Call ID: 0acb0931-e209-4133-a655-605ec50919ec
  Args: