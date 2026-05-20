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
Queen Margrethe II


Count Nikolai of Monpezat SK (born Prince Nikolai of Denmark; 28 August 1999) is a member of the Danish royal family.
He is the eldest son of Prince Joachim and his first wife, Alexandra, Countess of Frederiksborg, the eldest grandchild of Queen Margrethe II and Prince Henrik, and the eldest nephew of King Frederik X.
Biography

Nikolai was born a prince of Denmark at Rigshospitalet in Copenhagen on 28 August 1999.
He is the oldest grandchild of Queen Margrethe II and her late husband, Prince Henrik.
Nikolai was baptised in the chapel of the Fredensborg Palace on 6 November 1999 by the Danish Chaplain-in-Ordinary, Christian Thodberg.
At the christening, the musical work Lys på din vej, composed by Frederik Magle and dedicated to the prince, was performed for the first time.
His godparents are his paternal uncle King Frederik X, his maternal aunt Nicola Baird, Prince Edward, Duke of Edinburgh, Peter Steenstrup and Camilla Flint.
After their divorce in 2005, Prince Joachim and Alexandra had joint custody of the prince and his brother Prince Felix.
Nikolai and Felix have two half-siblings, Henrik and Athena, from their father's second marriage to Marie Cavallier.
Nikolai was confirmed on 18 May 2013 in Fredensborg Palace Church in the presence of his immediate family and all his godparents.
Like his father and uncle, Nikolai attended Krebs School in Copenhagen.
As part of that course, in 2023, Nikolai moved to Australia to take a semester at University of Technology Sydney.
In early 2018, Nikolai signed as a fashion model with the agency Scoop Models.
In February 2023, Nikolai signed as a model for Elite Model World - Paris under the name of 'Nikolai'.
Subsequently, in May he also signed with Barcelona-based modeling agency Sight Management Studio as 'Count Nikolai of Monpezat'.
In June 2024, Nikolai graduated from Copenhagen Business School with a Master of Science in Merchandising degree (cand.merc.).
In December 2025, it was announced that Nikolai would make his acting debut in the film adaptation of Hjalmar Söderberg's novel Doktor Glas (1905).
Titles, styles and honours

Titles and styles

Originally styled "His Highness Prince Nikolai of Denmark", Nikolai's style was expanded on 29 April 2008 to "His Highness Prince Nikolai of Denmark, Count of Monpezat".
In September 2022, Queen Margrethe II decided to restrict the titles Prince and Princess to the direct line of succession to the throne.
Since 1 January 2023, Count Nikolai is known as "His Excellency Count Nikolai of Monpezat".



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
  AssignClass (32354e49-11e1-482c-9b72-e3153dc54666)
 Call ID: 32354e49-11e1-482c-9b72-e3153dc54666
  Args:
    type: :Man
    source: :Nikolai
  AssignClass (0d965393-6dd2-4666-b583-9fb99e349b40)
 Call ID: 0d965393-6dd2-4666-b583-9fb99e349b40
  Args:
    source: :Joachim
    type: :Man
  AssignClass (cddf9006-1406-4737-8faa-05c71054fe61)
 Call ID: cddf9006-1406-4737-8faa-05c71054fe61
  Args:
    source: :Alexandra
    type: :Woman
  AssignClass (58bcee43-0981-4b3f-8636-389f09fbe7b2)
 Call ID: 58bcee43-0981-4b3f-8636-389f09fbe7b2
  Args:
    type: :Woman
    source: :MargretheII
  AssignClass (f2974c2d-ca89-4b3a-97f5-8cb2595c97a8)
 Call ID: f2974c2d-ca89-4b3a-97f5-8cb2595c97a8
  Args:
    type: :Man
    source: :Henrik
  AssignClass (0443a891-b039-47ce-bf5d-55605635a17d)
 Call ID: 0443a891-b039-47ce-bf5d-55605635a17d
  Args:
    source: :FrederikX
    type: :Man
  AssignClass (1118d733-fe05-4df5-a7aa-3cb05d22d0ee)
 Call ID: 1118d733-fe05-4df5-a7aa-3cb05d22d0ee
  Args:
    type: :Man
    source: :Felix
  AssignClass (8118e329-cfa0-4df8-8ac7-15049067187d)
 Call ID: 8118e329-cfa0-4df8-8ac7-15049067187d
  Args:
    source: :HenrikJunior
    type: :Man
  AssignClass (4fec60e8-dd00-42fb-a17a-6023330f0246)
 Call ID: 4fec60e8-dd00-42fb-a17a-6023330f0246
  Args:
    source: :Athena
    type: :Woman
  AssignClass (116697d5-b5f0-47f5-a036-9c086a90b86a)
 Call ID: 116697d5-b5f0-47f5-a036-9c086a90b86a
  Args:
    type: :Woman
    source: :MarieCavallier
  AddTriple (8f7306de-f7cc-4e6d-b409-51f495de946b)
 Call ID: 8f7306de-f7cc-4e6d-b409-51f495de946b
  Args:
    relation: :hasFather
    target: :Joachim
    source: :Nikolai
  AddTriple (80bcb7a0-973f-46f6-922d-c41e8cce1528)
 Call ID: 80bcb7a0-973f-46f6-922d-c41e8cce1528
  Args:
    source: :Nikolai
    target: :Alexandra
    relation: :hasMother
  AddTriple (1584d88c-fc57-48f9-95c8-f46265c07c4a)
 Call ID: 1584d88c-fc57-48f9-95c8-f46265c07c4a
  Args:
    source: :Felix
    target: :Joachim
    relation: :hasFather
  AddTriple (5e24b16c-8314-4d85-bd4f-bb0a9eda28ae)
 Call ID: 5e24b16c-8314-4d85-bd4f-bb0a9eda28ae
  Args:
    target: :Alexandra
    relation: :hasMother
    source: :Felix
  AddTriple (8e43aafc-fdb6-4cbe-9234-52f12b03cc2a)
 Call ID: 8e43aafc-fdb6-4cbe-9234-52f12b03cc2a
  Args:
    source: :HenrikJunior
    target: :Joachim
    relation: :hasFather
  AddTriple (d0e07a93-9322-4569-b1b8-fc26dc489f04)
 Call ID: d0e07a93-9322-4569-b1b8-fc26dc489f04
  Args:
    relation: :hasMother
    target: :MarieCavallier
    source: :HenrikJunior
  AddTriple (2d03c988-124a-41c0-8539-b5193c59f75e)
 Call ID: 2d03c988-124a-41c0-8539-b5193c59f75e
  Args:
    source: :Athena
    target: :Joachim
    relation: :hasFather
  AddTriple (0ef8500f-fe65-425e-b5c3-76b04358f149)
 Call ID: 0ef8500f-fe65-425e-b5c3-76b04358f149
  Args:
    relation: :hasMother
    target: :MarieCavallier
    source: :Athena
  AddLiteral (8593fbab-d6ee-46c0-9bb5-bc4cacb8bf9c)
 Call ID: 8593fbab-d6ee-46c0-9bb5-bc4cacb8bf9c
  Args:
    source: :Nikolai
    literal_value: 1999
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (b229010b-db7f-4f88-a466-7a8ebdded69c)
 Call ID: b229010b-db7f-4f88-a466-7a8ebdded69c
  Args:
    source: :Nikolai
    relation: :knownAs
    target: :CountNikolaiOfMonpezat
  AddTriple (c47bead8-a3e2-40f6-9c90-0eb828a0135b)
 Call ID: c47bead8-a3e2-40f6-9c90-0eb828a0135b
  Args:
    source: :Nikolai
    relation: :formerlyKnownAs
    target: :PrinceNikolaiOfDenmark
  Finish (6caacb7a-6551-4ded-b1ee-f49042da82b2)
 Call ID: 6caacb7a-6551-4ded-b1ee-f49042da82b2
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

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Athena a :Woman ;
      :hasFather data:Joachim ;
      :hasMother data:MarieCavallier .

  data:Felix a :Man ;
      :hasFather data:Joachim ;
      :hasMother data:Alexandra .

  data:FrederikX a :Man .

  data:Henrik a :Man .

  data:HenrikJunior a :Man ;
      :hasFather data:Joachim ;
      :hasMother data:MarieCavallier .

  data:MargretheII a :Woman .

  data:Nikolai a :Man ;
      :formerlyKnownAs data:PrinceNikolaiOfDenmark ;
      :hasBirthYear 1999 ;
      :hasFather data:Joachim ;
      :hasMother data:Alexandra ;
      :knownAs data:CountNikolaiOfMonpezat .

  data:Alexandra a :Woman .

  data:MarieCavallier a :Woman .

  data:Joachim a :Man .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['PrinceNikolaiOfDenmark', 'CountNikolaiOfMonpezat']

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
  AssignClass (787b0051-03c0-4079-bd22-437072c6c159)
 Call ID: 787b0051-03c0-4079-bd22-437072c6c159
  Args:
    source: :PrinceNikolaiOfDenmark
    type: :DomainEntity
  AssignClass (35fe8f17-d80e-4f90-af53-c86d6733d383)
 Call ID: 35fe8f17-d80e-4f90-af53-c86d6733d383
  Args:
    type: :DomainEntity
    source: :CountNikolaiOfMonpezat
  Finish (9fb5e568-3078-4ca9-9e67-5f80f1c2931d)
 Call ID: 9fb5e568-3078-4ca9-9e67-5f80f1c2931d
  Args: