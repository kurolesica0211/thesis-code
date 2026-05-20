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
Gerald David Lascelles (/ˈlæsəls/ LASS-əlss; 21 August 1924 – 27 February 1998) was the younger son of Henry Lascelles, 6th Earl of Harewood, and Mary, Princess Royal, the only daughter of King George V and Queen Mary.
He was a first cousin of Queen Elizabeth II.
He was styled The Honourable Gerald Lascelles.
Life

Gerald David Lascelles was born at Goldsborough Hall, near Knaresborough, West Riding of Yorkshire, and was baptised in October 1924 with the Prince of Wales and the Duchess of York (later King Edward VIII and Queen Elizabeth) as his godparents represented there by proxies.
The baptism was held in private at St. Mary's Church in the village of Goldsborough.
In 1955, the family moved to Fort Belvedere, Surrey, the former country home of Gerald Lascelles's uncle, Edward VIII (the Duke of Windsor).
On 17 November 1978, Lascelles married his second wife, actress Elizabeth Colvin (née Elizabeth Evelyn Collingwood, 23 April 1924 – 14 January 2006), in Vienna, Austria.
They had a son: 


Interests and positions

Lascelles was the president of the British Racing Drivers' Club from 1964 to 1991, after the 5th Earl Howe died.
Lord Howe had asked Lascelles to replace him, who was briefly a driver before this.
In his role as BRDC president, Lascelles was invited by the Australian Racing Drivers Club, promoters of the Bathurst 1000 Touring car race, to be the Grand Marshal for the 1985 race.
Death

Lascelles died in Bergerac, France, on 27 February 1998 at the age of 73.



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
  AssignClass (c48880bf-5b24-4906-b2e2-4d0b85dfecb7)
 Call ID: c48880bf-5b24-4906-b2e2-4d0b85dfecb7
  Args:
    source: Gerald David Lascelles
    type: :Man
  AssignClass (b54f22d0-b47f-4c52-ac9e-41b30b8c0951)
 Call ID: b54f22d0-b47f-4c52-ac9e-41b30b8c0951
  Args:
    type: :Man
    source: Henry Lascelles, 6th Earl of Harewood
  AssignClass (83d83116-fa6c-420f-b4c3-9eb0e2db8c25)
 Call ID: 83d83116-fa6c-420f-b4c3-9eb0e2db8c25
  Args:
    source: Mary, Princess Royal
    type: :Woman
  AssignClass (50f6f2ea-7817-49de-abc0-4ad19e8108a8)
 Call ID: 50f6f2ea-7817-49de-abc0-4ad19e8108a8
  Args:
    type: :Man
    source: King George V
  AssignClass (7664a309-4eb6-40eb-84ff-8307f481f29e)
 Call ID: 7664a309-4eb6-40eb-84ff-8307f481f29e
  Args:
    type: :Woman
    source: Queen Mary
  AssignClass (82a942f7-8d0e-4d66-955a-2cf4225c609f)
 Call ID: 82a942f7-8d0e-4d66-955a-2cf4225c609f
  Args:
    source: Queen Elizabeth II
    type: :Woman
  AssignClass (29bba0aa-be6b-499d-a6b3-8a10293ee957)
 Call ID: 29bba0aa-be6b-499d-a6b3-8a10293ee957
  Args:
    type: :Woman
    source: Elizabeth Colvin
  AssignClass (fe59314e-5c59-4fb0-8f81-b275c3f78cc0)
 Call ID: fe59314e-5c59-4fb0-8f81-b275c3f78cc0
  Args:
    source: Edward VIII
    type: :Man
  AddLiteral (c17244ce-1077-4237-9f93-5bce829d2087)
 Call ID: c17244ce-1077-4237-9f93-5bce829d2087
  Args:
    relation: :hasBirthYear
    source: Gerald David Lascelles
    literal_type: xsd:integer
    literal_value: 1924
  AddLiteral (3556210c-e376-4749-8952-3b94eeca5683)
 Call ID: 3556210c-e376-4749-8952-3b94eeca5683
  Args:
    literal_value: 1998
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Gerald David Lascelles
  AddTriple (72fea906-4d42-47b8-8475-2f71cf744ca1)
 Call ID: 72fea906-4d42-47b8-8475-2f71cf744ca1
  Args:
    target: Henry Lascelles, 6th Earl of Harewood
    source: Gerald David Lascelles
    relation: :hasFather
  AddTriple (49ec6890-0852-45fa-b65c-2163307eebec)
 Call ID: 49ec6890-0852-45fa-b65c-2163307eebec
  Args:
    target: Mary, Princess Royal
    relation: :hasMother
    source: Gerald David Lascelles
  AddTriple (6837f493-cd26-4d9c-be1f-d1f6c04bf355)
 Call ID: 6837f493-cd26-4d9c-be1f-d1f6c04bf355
  Args:
    relation: :hasFather
    source: Mary, Princess Royal
    target: King George V
  AddTriple (f30618d3-6fc2-4322-8306-399e074bab5d)
 Call ID: f30618d3-6fc2-4322-8306-399e074bab5d
  Args:
    source: Mary, Princess Royal
    relation: :hasMother
    target: Queen Mary
  AddTriple (6d85a57b-2956-48bd-8f23-1dc4c4ef9efd)
 Call ID: 6d85a57b-2956-48bd-8f23-1dc4c4ef9efd
  Args:
    target: 1978
    relation: :hasMarriageYear
    source: Gerald David Lascelles
  AddTriple (36088d89-0119-4e91-8b22-b9595a6b6997)
 Call ID: 36088d89-0119-4e91-8b22-b9595a6b6997
  Args:
    target: Elizabeth Colvin
    source: Gerald David Lascelles
    relation: :hasRelation
  AddLiteral (73437f30-9c96-4406-a72f-ed28cbb42f04)
 Call ID: 73437f30-9c96-4406-a72f-ed28cbb42f04
  Args:
    literal_type: xsd:string
    literal_value: The Honourable Gerald Lascelles
    source: Gerald David Lascelles
    relation: :knownAs
  Finish (6a5a2d1e-45e5-4958-8914-7d6420b3855c)
 Call ID: 6a5a2d1e-45e5-4958-8914-7d6420b3855c
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

  data:Edward_VIII a :Man .

  data:Gerald_David_Lascelles a :Man ;
      :hasBirthYear 1924 ;
      :hasDeathYear 1998 ;
      :hasFather data:Henry_Lascelles%2C_6th_Earl_of_Harewood ;
      :hasMarriageYear data:1978 ;
      :hasMother data:Mary%2C_Princess_Royal ;
      :hasRelation data:Elizabeth_Colvin ;
      :knownAs "The Honourable Gerald Lascelles"^^xsd:string .

  data:Queen_Elizabeth_II a :Woman .

  data:Elizabeth_Colvin a :Woman .

  data:Henry_Lascelles%2C_6th_Earl_of_Harewood a :Man .

  data:King_George_V a :Man .

  data:Mary%2C_Princess_Royal a :Woman ;
      :hasFather data:King_George_V ;
      :hasMother data:Queen_Mary .

  data:Queen_Mary a :Woman .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['1978']

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
  RemoveLiteral (69f2250d-4268-4159-ad09-4e5bf835f2ed)
 Call ID: 69f2250d-4268-4159-ad09-4e5bf835f2ed
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Gerald David Lascelles
    literal_value: 1978
  AddLiteral (6b6aa479-16b0-484d-b050-322d22b28e53)
 Call ID: 6b6aa479-16b0-484d-b050-322d22b28e53
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:string
    source: Gerald David Lascelles
    literal_value: 1978
  AssignClass (56ae1a17-bf5d-419e-ab93-b07f21a0ba63)
 Call ID: 56ae1a17-bf5d-419e-ab93-b07f21a0ba63
  Args:
    source: 1978
    type: :DomainEntity
  Finish (de8a7a5e-1bff-40c4-9f43-a753e829cb38)
 Call ID: de8a7a5e-1bff-40c4-9f43-a753e829cb38
  Args: