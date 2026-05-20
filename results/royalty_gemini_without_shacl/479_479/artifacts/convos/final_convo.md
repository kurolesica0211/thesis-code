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
Archduhess Rosa Maria Antonie Roberta Josepha Anna Walburga Carmela Ignazia Rita de Cascia of Austria(German: Rosa Maria Antonie Roberta Josepha Anna Walburga Carmela Ignazia Rita de Cascia, Erzherzogin von Österreich; 22 September 1906 – 17 September 1983) was a member of the Tuscan branch of the House of Habsburg-Lorraine and an Archduchess of Austria and Princess of Bohemia, Hungary, and Tuscany by birth.
Through her marriage to Philipp Albrecht, Duke of Württemberg, Rosa was also a member of the House of Württemberg and Duchess consort of Württemberg.
Early life

Rosa was the fourth and youngest child of Archduke Peter Ferdinand, Prince of Tuscany, and his wife, Princess Maria Cristina of Bourbon-Two Sicilies.
Marriage and issue

Rosa married Philipp Albrecht, Duke of Württemberg, eldest child and son of Albrecht, Duke of Württemberg, and his wife, Archduchess Margarete Sophie of Austria, on 1 August 1928 in Friedrichshafen.
Rosa and Philipp Albrecht had two sons and four daughters:


Ancestry

References

Bibliography



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
  AssignClass (d5172928-ec96-4f50-acdb-bb4f03b5e140)
 Call ID: d5172928-ec96-4f50-acdb-bb4f03b5e140
  Args:
    type: :Person
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AssignClass (1f8d0f8f-1f0d-4ed8-be7a-531647a60f02)
 Call ID: 1f8d0f8f-1f0d-4ed8-be7a-531647a60f02
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    type: :Woman
  AddLiteral (1699f433-46ac-4cd3-80c0-31d177774fe1)
 Call ID: 1699f433-46ac-4cd3-80c0-31d177774fe1
  Args:
    literal_value: 1906
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AddLiteral (b25784fd-eb0b-4e7d-8035-6de77edc00a9)
 Call ID: b25784fd-eb0b-4e7d-8035-6de77edc00a9
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1983
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AssignClass (6e014dcf-9031-4fbd-a0bf-b0a339e55a95)
 Call ID: 6e014dcf-9031-4fbd-a0bf-b0a339e55a95
  Args:
    source: Peter_Ferdinand_of_Austria
    type: :Person
  AssignClass (005ade45-628f-4a16-b181-2738b3b62e67)
 Call ID: 005ade45-628f-4a16-b181-2738b3b62e67
  Args:
    source: Peter_Ferdinand_of_Austria
    type: :Man
  AssignClass (f2156dff-c4fd-49e3-842f-5e0e005fbe8c)
 Call ID: f2156dff-c4fd-49e3-842f-5e0e005fbe8c
  Args:
    type: :Person
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (af9e1380-aa11-47ff-9f43-293e2a56425f)
 Call ID: af9e1380-aa11-47ff-9f43-293e2a56425f
  Args:
    type: :Woman
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AddTriple (ca7b944f-fbce-4058-85a1-dc426b7396bb)
 Call ID: ca7b944f-fbce-4058-85a1-dc426b7396bb
  Args:
    relation: :hasFather
    target: Peter_Ferdinand_of_Austria
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AddTriple (d3f5c4d3-dc1b-4fc8-a8d3-6e842c91a5f3)
 Call ID: d3f5c4d3-dc1b-4fc8-a8d3-6e842c91a5f3
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    relation: :hasMother
    target: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (f9c2a6f6-5919-46db-8971-f9e390185282)
 Call ID: f9c2a6f6-5919-46db-8971-f9e390185282
  Args:
    type: :Person
    source: Philipp_Albrecht_of_Württemberg
  AssignClass (86360057-066a-4a2c-a10e-ed7d8db3bd27)
 Call ID: 86360057-066a-4a2c-a10e-ed7d8db3bd27
  Args:
    type: :Man
    source: Philipp_Albrecht_of_Württemberg
  AddTriple (7ea4b8dc-73ef-4a24-9c07-373a0d5a04e8)
 Call ID: 7ea4b8dc-73ef-4a24-9c07-373a0d5a04e8
  Args:
    target: Philipp_Albrecht_of_Württemberg
    relation: :hasRelation
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
  AddLiteral (89b56807-a7a8-40d9-b3c6-51dec88ff0a0)
 Call ID: 89b56807-a7a8-40d9-b3c6-51dec88ff0a0
  Args:
    source: Rosa_Maria_Antonie_Roberta_Josepha_Anna_Walburga_Carmela_Ignazia_Rita_de_Cascia_of_Austria
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1928
  AssignClass (f4c444e1-dc0e-42fe-91b0-a5356b2334d6)
 Call ID: f4c444e1-dc0e-42fe-91b0-a5356b2334d6
  Args:
    type: :Person
    source: Albrecht_of_Württemberg
  AssignClass (5c0547e5-75af-41a6-82ac-cc7b9ae1cba2)
 Call ID: 5c0547e5-75af-41a6-82ac-cc7b9ae1cba2
  Args:
    type: :Man
    source: Albrecht_of_Württemberg
  AssignClass (0a6bdb88-29c7-43b5-b681-226ff265db11)
 Call ID: 0a6bdb88-29c7-43b5-b681-226ff265db11
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Person
  AssignClass (444df46d-e870-46b9-83dd-dc2297c73fa0)
 Call ID: 444df46d-e870-46b9-83dd-dc2297c73fa0
  Args:
    type: :Woman
    source: Margarete_Sophie_of_Austria
  AddTriple (b7f0274c-f853-456e-aa8b-228351596e9e)
 Call ID: b7f0274c-f853-456e-aa8b-228351596e9e
  Args:
    relation: :hasFather
    target: Albrecht_of_Württemberg
    source: Philipp_Albrecht_of_Württemberg
  AddTriple (64de2401-ce90-4145-ae2d-ea217c1345a3)
 Call ID: 64de2401-ce90-4145-ae2d-ea217c1345a3
  Args:
    relation: :hasMother
    target: Margarete_Sophie_of_Austria
    source: Philipp_Albrecht_of_Württemberg
  Finish (183e828a-4184-450c-804e-f830099d84cf)
 Call ID: 183e828a-4184-450c-804e-f830099d84cf
  Args: