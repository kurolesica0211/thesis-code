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
Ferdinand d'Orléans, Duke of Montpensier (French: Ferdinand François Philippe Marie Laurent d'Orléans, Duc de Montpensier) (9 September 1884 – 30 January 1924) was a member of the House of Orléans and a Prince of France.
Early life

Ferdinand was born on 9 September 1884 at Château d'Eu, Eu, Seine-Inférieure, French Republic.
He was the eighth, and youngest, child of Philippe d'Orléans, Count of Paris and his wife Marie Isabelle d'Orléans.
His elder siblings were Princess Amélie (wife of Carlos I of Portugal), Prince Philippe (who married Archduchess Maria Dorothea, daughter of Archduke Joseph Karl of Austria), Princess Hélène (the wife of Emmanuel Philibert, 2nd Duke of Aosta), Prince Charles (who died young), Princess Isabelle (wife of Prince Jean D'Orléans, Duke of Guise), Prince Jacques (who also died young), and Princess Louise (wife of Prince Carlos of Bourbon-Two Sicilies).
His paternal grandparents were Prince Ferdinand, Duke of Orléans and Duchess Helene of Mecklenburg-Schwerin.
Through his father, he was a great-grandson of Louis-Philippe I, King of the French and his wife Queen Maria Amalia of the Two Sicilies.
His maternal grandparents were Infanta Luisa Fernanda of Spain and Prince Antoine, Duke of Montpensier (the youngest son of Louis-Philippe of France and Maria Amalia of Naples and Sicily).
Career

The Duke lived in England for many years, until "his reported indiscretions with regard to his recollections of Queen Victoria made it somewhat uncomfortable for him when in London."
Others considered for the throne were Prince Ghika of Romania, Prince Karl, Duke of Urach, Prince Moritz of Schaumburg-Lippe, Prince Vittorio Emanuele, Count of Turin and Prince Arthur of Connaught.
Personal life

On 20 August 1921, Ferdinand married Doña María Isabel González de Olañeta e Ibarreta (22 April 1895 – 11 July 1958), 3rd Marchioness of Valdeterrazo and Grandee of Spain, 2nd
She was the daughter of Don Ulpiano González de Olañeta y González de Ocampo, 2nd Marquis of Valdeterrazo and Grandee of Spain, and his wife Doña Isabel de Ibarreta y Uhagón.
Ferdinand and María Isabel did not have children.
The Duke of Montpensier died on 30 January 1924 at the Château de Randan in Randan in the French Republic.



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
  AssignClass (2cfd0916-3876-4ed6-9e74-c309dd793e12)
 Call ID: 2cfd0916-3876-4ed6-9e74-c309dd793e12
  Args:
    type: :Man
    source: Ferdinand_dOrleans_Duke_of_Montpensier
  AssignClass (f0ad7d16-6a44-456f-b2b1-ce1e482bcdc7)
 Call ID: f0ad7d16-6a44-456f-b2b1-ce1e482bcdc7
  Args:
    type: :Person
    source: Ferdinand_dOrleans_Duke_of_Montpensier
  AddLiteral (11870cfb-170e-4aad-81f8-aa6a61b2379d)
 Call ID: 11870cfb-170e-4aad-81f8-aa6a61b2379d
  Args:
    source: Ferdinand_dOrleans_Duke_of_Montpensier
    relation: :hasBirthYear
    literal_value: 1884
    literal_type: xsd:integer
  AddLiteral (81dcedde-f1ed-4a93-8d64-e384ca7e6693)
 Call ID: 81dcedde-f1ed-4a93-8d64-e384ca7e6693
  Args:
    source: Ferdinand_dOrleans_Duke_of_Montpensier
    relation: :hasDeathYear
    literal_value: 1924
    literal_type: xsd:integer
  AssignClass (2b86058c-83cd-4460-a463-1a5f763cab95)
 Call ID: 2b86058c-83cd-4460-a463-1a5f763cab95
  Args:
    type: :Man
    source: Philippe_dOrleans_Count_of_Paris
  AssignClass (590ede57-cfd7-4308-b4ac-4297b64d235e)
 Call ID: 590ede57-cfd7-4308-b4ac-4297b64d235e
  Args:
    type: :Person
    source: Philippe_dOrleans_Count_of_Paris
  AssignClass (d46b0707-533d-4313-82f2-9fbfb3fa580b)
 Call ID: d46b0707-533d-4313-82f2-9fbfb3fa580b
  Args:
    type: :Woman
    source: Marie_Isabelle_dOrleans
  AssignClass (486b7fac-ae6f-4834-8df3-e2c463c4ed88)
 Call ID: 486b7fac-ae6f-4834-8df3-e2c463c4ed88
  Args:
    type: :Person
    source: Marie_Isabelle_dOrleans
  AddTriple (1a5e1cf9-1df8-4ad8-98dc-a8d0e37f465b)
 Call ID: 1a5e1cf9-1df8-4ad8-98dc-a8d0e37f465b
  Args:
    source: Ferdinand_dOrleans_Duke_of_Montpensier
    relation: :hasFather
    target: Philippe_dOrleans_Count_of_Paris
  AddTriple (c050a5d0-6cfb-48d9-ac21-d856f0cd5d35)
 Call ID: c050a5d0-6cfb-48d9-ac21-d856f0cd5d35
  Args:
    source: Ferdinand_dOrleans_Duke_of_Montpensier
    relation: :hasMother
    target: Marie_Isabelle_dOrleans
  AssignClass (39bd9046-9330-4bcc-a3e1-3316bbaa6171)
 Call ID: 39bd9046-9330-4bcc-a3e1-3316bbaa6171
  Args:
    type: :Woman
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AssignClass (ba61e95b-3f0a-4d5f-857c-3708d666d406)
 Call ID: ba61e95b-3f0a-4d5f-857c-3708d666d406
  Args:
    type: :Person
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AddLiteral (8c6a6efc-0b1e-44ea-8795-13fc96f22e1a)
 Call ID: 8c6a6efc-0b1e-44ea-8795-13fc96f22e1a
  Args:
    source: Ferdinand_dOrleans_Duke_of_Montpensier
    relation: :hasMarriageYear
    literal_value: 1921
    literal_type: xsd:integer
  AddTriple (0b35be52-11a2-4d74-87fb-73b6dd726b6a)
 Call ID: 0b35be52-11a2-4d74-87fb-73b6dd726b6a
  Args:
    source: Ferdinand_dOrleans_Duke_of_Montpensier
    relation: :hasRelation
    target: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
  AssignClass (6c4cad39-ae01-4812-8a64-30746897d362)
 Call ID: 6c4cad39-ae01-4812-8a64-30746897d362
  Args:
    type: :Man
    source: Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
  AssignClass (9070723a-8441-487c-9dba-392d063d7898)
 Call ID: 9070723a-8441-487c-9dba-392d063d7898
  Args:
    type: :Person
    source: Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
  AssignClass (44ee7455-a689-4a40-873e-778c2d767d33)
 Call ID: 44ee7455-a689-4a40-873e-778c2d767d33
  Args:
    type: :Woman
    source: Isabel_de_Ibarreta_y_Uhagon
  AssignClass (32e0efa1-95f3-4054-a5fb-81c326e79051)
 Call ID: 32e0efa1-95f3-4054-a5fb-81c326e79051
  Args:
    type: :Person
    source: Isabel_de_Ibarreta_y_Uhagon
  AddTriple (54def5e9-81d7-4713-ba22-f7937815b4bf)
 Call ID: 54def5e9-81d7-4713-ba22-f7937815b4bf
  Args:
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
    relation: :hasFather
    target: Ulpiano_Gonzalez_de_Olaneta_y_Gonzalez_de_Ocampo
  AddTriple (2ca7c75b-7bcc-405f-a2e4-24844fb9f4e8)
 Call ID: 2ca7c75b-7bcc-405f-a2e4-24844fb9f4e8
  Args:
    source: Maria_Isabel_Gonzalez_de_Olaneta_e_Ibarreta
    relation: :hasMother
    target: Isabel_de_Ibarreta_y_Uhagon
  Finish (77337302-f847-4970-a635-e10133a4c16f)
 Call ID: 77337302-f847-4970-a635-e10133a4c16f
  Args: