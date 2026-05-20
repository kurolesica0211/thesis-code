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
Prince Wilhelm Eitel Friedrich Christian Karl of Prussia (7 July 1883 – 8 December 1942) was the second son of Emperor Wilhelm II of Germany by his first wife, Princess Augusta Viktoria of Schleswig-Holstein-Sonderburg-Augustenburg.
Early life

Prince Eitel Friedrich was born on 7 July 1883 as the second son of the then Prince Wilhelm of Prussia, and his first wife, Princess Augusta Victoria of Schleswig-Holstein.
He was born in the Marmorpalais of Potsdam in the Province of Brandenburg, where his parents resided until his father acceded to the throne as Emperor Wilhelm II in 1888.
He spent his childhood with his siblings at the New Palace, also in Potsdam, and his school days with his brothers at the Prinzenhaus in Plön in his mother's ancestral Schleswig-Holstein.
On 27 February 1906, Prince Eitel married Duchess Sophia Charlotte of Oldenburg (2 February 1879 Oldenburg – 29 March 1964 Westerstede) in Berlin.
In 1907, it was reported that Member of the Reichstag Otto Arendt had proposed the elevation of Alsace-Lorraine to a grand duchy within the empire, with Eitel Friedrich as monarch; however, while the Kaiser did express interest, ultimately nothing came of the plan.
World War I

Raised at the cadet corps of Plön Castle, Prince Eitel was in the front line from the beginning of World War I and was wounded at Bapaume, where he commanded the Prussian First Foot Guards.
The two men were hiding in a nearby tree line from what they thought was the advancing Russian army and who turned out to be the grenadiers, guardsmen, and officers of Prince Eitel.
Regimental Commissions

Source:


Orders and decorations

Two ships were named after Prince Eitel, the passenger ship Prince Eitel Friedrich (1901) and the Reich postal steamer Prince Eitel Friedrich (1904).
Berlin, Prussia, 1907.



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
  AssignClass (9805b7b2-f8b3-48c3-a885-d194088383c4)
 Call ID: 9805b7b2-f8b3-48c3-a885-d194088383c4
  Args:
    type: :Man
    source: :Prince_Eitel_Friedrich_of_Prussia
  AssignClass (9a8aea16-363f-4762-92d4-5d1080f21b37)
 Call ID: 9a8aea16-363f-4762-92d4-5d1080f21b37
  Args:
    type: :Man
    source: :Emperor_Wilhelm_II_of_Germany
  AssignClass (ef05cc7b-4dff-4a0f-8b59-2786cc4547a8)
 Call ID: ef05cc7b-4dff-4a0f-8b59-2786cc4547a8
  Args:
    type: :Woman
    source: :Princess_Augusta_Viktoria_of_Schleswig-Holstein-Sonderburg-Augustenburg
  AssignClass (219fcf4c-d15c-4157-8457-160e1ce0f85a)
 Call ID: 219fcf4c-d15c-4157-8457-160e1ce0f85a
  Args:
    type: :Woman
    source: :Duchess_Sophia_Charlotte_of_Oldenburg
  AddLiteral (2da8c47b-e3cf-4872-8944-77ac35c41d97)
 Call ID: 2da8c47b-e3cf-4872-8944-77ac35c41d97
  Args:
    source: :Prince_Eitel_Friedrich_of_Prussia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1883
  AddLiteral (97694f2e-f217-4eeb-aa3c-79aecc519955)
 Call ID: 97694f2e-f217-4eeb-aa3c-79aecc519955
  Args:
    literal_value: 1942
    relation: :hasDeathYear
    source: :Prince_Eitel_Friedrich_of_Prussia
    literal_type: xsd:integer
  AddTriple (156d34d1-4946-40f5-85fb-494f305f7488)
 Call ID: 156d34d1-4946-40f5-85fb-494f305f7488
  Args:
    target: :Emperor_Wilhelm_II_of_Germany
    source: :Prince_Eitel_Friedrich_of_Prussia
    relation: :hasFather
  AddTriple (aac1e6a4-0836-4b87-8999-60cb62fc384f)
 Call ID: aac1e6a4-0836-4b87-8999-60cb62fc384f
  Args:
    relation: :hasMother
    source: :Prince_Eitel_Friedrich_of_Prussia
    target: :Princess_Augusta_Viktoria_of_Schleswig-Holstein-Sonderburg-Augustenburg
  AddTriple (4e7e715e-1bd1-4a3b-ae3a-b3ffdd326f0a)
 Call ID: 4e7e715e-1bd1-4a3b-ae3a-b3ffdd326f0a
  Args:
    source: :Prince_Eitel_Friedrich_of_Prussia
    relation: :hasMarriageYear
    target: :Duchess_Sophia_Charlotte_of_Oldenburg
  AddLiteral (f82e72d4-07fe-4982-9b07-e38f46fd117b)
 Call ID: f82e72d4-07fe-4982-9b07-e38f46fd117b
  Args:
    relation: :hasMarriageYear
    source: :Prince_Eitel_Friedrich_of_Prussia
    literal_type: xsd:integer
    literal_value: 1906
  AddLiteral (3f6fce91-3dc8-48de-8d6e-9d949b6bfbcd)
 Call ID: 3f6fce91-3dc8-48de-8d6e-9d949b6bfbcd
  Args:
    literal_value: 1879
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Duchess_Sophia_Charlotte_of_Oldenburg
  AddLiteral (69f135a9-48f2-4dbb-85e5-2e1e8adbf4cc)
 Call ID: 69f135a9-48f2-4dbb-85e5-2e1e8adbf4cc
  Args:
    literal_value: 1964
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Duchess_Sophia_Charlotte_of_Oldenburg
  AddTriple (c0eace6e-a11f-4ca4-a7f5-d3590905cc6e)
 Call ID: c0eace6e-a11f-4ca4-a7f5-d3590905cc6e
  Args:
    relation: :hasSex
    source: :Prince_Eitel_Friedrich_of_Prussia
    target: :Male
  AddTriple (ab972528-a83a-4dbd-9506-c83021f176ac)
 Call ID: ab972528-a83a-4dbd-9506-c83021f176ac
  Args:
    relation: :hasSex
    source: :Emperor_Wilhelm_II_of_Germany
    target: :Male
  AddTriple (1a51926a-feb0-4b4d-88f7-3ae1e4ca398a)
 Call ID: 1a51926a-feb0-4b4d-88f7-3ae1e4ca398a
  Args:
    relation: :hasSex
    source: :Princess_Augusta_Viktoria_of_Schleswig-Holstein-Sonderburg-Augustenburg
    target: :Female
  AddTriple (874307ff-be66-4ace-a0e6-09f00e06336b)
 Call ID: 874307ff-be66-4ace-a0e6-09f00e06336b
  Args:
    target: :Female
    relation: :hasSex
    source: :Duchess_Sophia_Charlotte_of_Oldenburg
  Finish (36b7d9e9-2c4f-4e21-92f9-ba02172129e2)
 Call ID: 36b7d9e9-2c4f-4e21-92f9-ba02172129e2
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

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Prince_Eitel_Friedrich_of_Prussia a :Man ;
      :hasBirthYear 1883 ;
      :hasDeathYear 1942 ;
      :hasFather data:Emperor_Wilhelm_II_of_Germany ;
      :hasMarriageYear data:Duchess_Sophia_Charlotte_of_Oldenburg,
          1906 ;
      :hasMother data:Princess_Augusta_Viktoria_of_Schleswig-Holstein-Sonderburg-Augustenburg ;
      :hasSex data:Male .

  data:Duchess_Sophia_Charlotte_of_Oldenburg a :Woman ;
      :hasBirthYear 1879 ;
      :hasDeathYear 1964 ;
      :hasSex data:Female .

  data:Emperor_Wilhelm_II_of_Germany a :Man ;
      :hasSex data:Male .

  data:Princess_Augusta_Viktoria_of_Schleswig-Holstein-Sonderburg-Augustenburg a :Woman ;
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
  AssignClass (f7847d03-e682-420c-a04c-e3a07f558e8e)
 Call ID: f7847d03-e682-420c-a04c-e3a07f558e8e
  Args:
    source: :Male
    type: :Male
  AssignClass (5f74fc88-6fe9-4d84-985e-4a287c06598d)
 Call ID: 5f74fc88-6fe9-4d84-985e-4a287c06598d
  Args:
    source: :Female
    type: :Female
  Finish (cf19461c-2033-4ae5-b1e4-9134c265fc95)
 Call ID: cf19461c-2033-4ae5-b1e4-9134c265fc95
  Args: