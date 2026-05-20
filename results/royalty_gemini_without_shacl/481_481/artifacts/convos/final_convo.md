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
Prince Hermann Friedrich Fernando Roland of Leiningen (German: Hermann Friedrich Fernando Roland Prinz zu Leiningen; born April 16, 1963) is a Canadian banker and the younger son of Prince Karl of Leiningen and Princess Marie Louise of Bulgaria.
Life

Leiningen was born in Toronto, Ontario.
Through his mother, Leiningen is a grandson of King Boris III of Bulgaria, a great-grandson of King Victor Emmanuel III of Italy and great-great-grandson of King Nicholas of Montenegro.
Leiningen is a financial analyst and banker, addressed as Mr. Hermann Leiningen professionally.
As of 2015, Leiningen worked for a division of Royal Bank of Canada.
On 16 May 1987, Leiningen married Deborah Cully (born December 2, 1961).
Prince Herman is an honorary member of the Board of Trustees of the H.C.V. Princess Marie Louise and of the King Boris and Queen Giovanna Fund who manages Vrana Palace in Sofia.



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
  AssignClass (1e735962-06f5-4258-bcad-2fb6f2fb454c)
 Call ID: 1e735962-06f5-4258-bcad-2fb6f2fb454c
  Args:
    source: Hermann_Leiningen
    type: :Man
  AssignClass (525d2866-cba6-445e-85d9-278169e3c178)
 Call ID: 525d2866-cba6-445e-85d9-278169e3c178
  Args:
    type: :Person
    source: Hermann_Leiningen
  AssignClass (46e92a99-e1a2-44ae-ae69-a2bed73a9a67)
 Call ID: 46e92a99-e1a2-44ae-ae69-a2bed73a9a67
  Args:
    source: Karl_Leiningen
    type: :Man
  AssignClass (c2af51fa-4471-48dc-8fac-79c159085322)
 Call ID: c2af51fa-4471-48dc-8fac-79c159085322
  Args:
    type: :Ancestor
    source: Karl_Leiningen
  AssignClass (5496c809-6d90-4eb5-a67d-b0eb48c1120b)
 Call ID: 5496c809-6d90-4eb5-a67d-b0eb48c1120b
  Args:
    type: :Woman
    source: Marie_Louise_Bulgaria
  AssignClass (90ea3b4c-f45a-4e7f-bd6a-3f436fb539bc)
 Call ID: 90ea3b4c-f45a-4e7f-bd6a-3f436fb539bc
  Args:
    source: Marie_Louise_Bulgaria
    type: :Ancestor
  AssignClass (51fb2223-a42c-4960-abf9-5b66a6c9d9cc)
 Call ID: 51fb2223-a42c-4960-abf9-5b66a6c9d9cc
  Args:
    type: :Woman
    source: Deborah_Cully
  AssignClass (e1189e15-8132-4ea0-985d-addc71b1c009)
 Call ID: e1189e15-8132-4ea0-985d-addc71b1c009
  Args:
    source: Deborah_Cully
    type: :Person
  AddLiteral (1b6ebe5c-5899-42d0-8b1a-c525f682875c)
 Call ID: 1b6ebe5c-5899-42d0-8b1a-c525f682875c
  Args:
    literal_type: xsd:integer
    literal_value: 1963
    source: Hermann_Leiningen
    relation: :hasBirthYear
  AddLiteral (599169e0-0279-43d1-8946-9eed41102aa5)
 Call ID: 599169e0-0279-43d1-8946-9eed41102aa5
  Args:
    literal_value: Mr. Hermann Leiningen
    literal_type: xsd:string
    source: Hermann_Leiningen
    relation: :knownAs
  AddTriple (fb160718-f42e-4f18-8243-f63b6ff50bb8)
 Call ID: fb160718-f42e-4f18-8243-f63b6ff50bb8
  Args:
    relation: :hasFather
    source: Hermann_Leiningen
    target: Karl_Leiningen
  AddTriple (743965ac-a66a-4408-8776-af005d3d02e4)
 Call ID: 743965ac-a66a-4408-8776-af005d3d02e4
  Args:
    source: Hermann_Leiningen
    relation: :hasMother
    target: Marie_Louise_Bulgaria
  AddTriple (d46de57b-eaa4-49cc-b3db-a4d457c5978c)
 Call ID: d46de57b-eaa4-49cc-b3db-a4d457c5978c
  Args:
    source: Hermann_Leiningen
    relation: :hasSex
    target: :Male
  AddTriple (4d92d48c-0416-4b92-aaf4-cd0dbc59cdc6)
 Call ID: 4d92d48c-0416-4b92-aaf4-cd0dbc59cdc6
  Args:
    target: :Male
    source: Karl_Leiningen
    relation: :hasSex
  AddTriple (210b10e7-594a-4681-bf55-3624960422cd)
 Call ID: 210b10e7-594a-4681-bf55-3624960422cd
  Args:
    target: :Female
    source: Marie_Louise_Bulgaria
    relation: :hasSex
  AddTriple (55cd2502-6d8d-4837-86bd-6494ef4d06d2)
 Call ID: 55cd2502-6d8d-4837-86bd-6494ef4d06d2
  Args:
    target: :Female
    relation: :hasSex
    source: Deborah_Cully
  AddLiteral (e2a169b7-343e-40cc-9fb8-115724b21d4a)
 Call ID: e2a169b7-343e-40cc-9fb8-115724b21d4a
  Args:
    literal_type: xsd:integer
    literal_value: 1987
    source: Hermann_Leiningen
    relation: :hasMarriageYear
  AddLiteral (07e9663a-bfd3-4432-933d-fbbdaa662649)
 Call ID: 07e9663a-bfd3-4432-933d-fbbdaa662649
  Args:
    literal_value: 1961
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Deborah_Cully
  AddTriple (1be39cd3-c590-4f06-b52f-f7025555b56a)
 Call ID: 1be39cd3-c590-4f06-b52f-f7025555b56a
  Args:
    target: Deborah_Cully
    source: Hermann_Leiningen
    relation: :hasRelation
  Finish (53a60e49-8954-4efe-a5eb-d2c621ed13cb)
 Call ID: 53a60e49-8954-4efe-a5eb-d2c621ed13cb
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

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Hermann_Leiningen a :Man,
          :Person ;
      :hasBirthYear 1963 ;
      :hasFather data:Karl_Leiningen ;
      :hasMarriageYear 1987 ;
      :hasMother data:Marie_Louise_Bulgaria ;
      :hasRelation data:Deborah_Cully ;
      :hasSex data:Male ;
      :knownAs "Mr. Hermann Leiningen"^^xsd:string .

  data:Deborah_Cully a :Person,
          :Woman ;
      :hasBirthYear 1961 ;
      :hasSex data:Female .

  data:Karl_Leiningen a :Ancestor,
          :Man ;
      :hasSex data:Male .

  data:Marie_Louise_Bulgaria a :Ancestor,
          :Woman ;
      :hasSex data:Female .



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
  AssignClass (2f50c41d-391c-42b3-8521-9f528e50b949)
 Call ID: 2f50c41d-391c-42b3-8521-9f528e50b949
  Args:
    source: Male
    type: :Sex
  AssignClass (ad0d10e3-46e9-49a2-82a5-5856d34f35bf)
 Call ID: ad0d10e3-46e9-49a2-82a5-5856d34f35bf
  Args:
    source: Female
    type: :Sex
  Finish (cdff99ee-b8e7-412d-b6a7-99b75c3e007b)
 Call ID: cdff99ee-b8e7-412d-b6a7-99b75c3e007b
  Args: