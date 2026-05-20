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
Don Gonzalo, Duke of Aquitaine (5 June 1937 – 27 May 2000) (Spanish: Gonzalo Víctor Alfonso José Bonifacio Antonio María y Todos los Santos de Borbón y Dampierre; French: Gonzalve Victor Alphonse Joseph Boniface Antoine Marie Toussaint de Bourbon) was a grandson of Alfonso XIII, King of Spain.
Life

Gonzalo was born in the Sant'Anna Clinic in Rome on 5 June 1937, the younger son of Infante Jaime, Duke of Segovia and his first wife, Emmanuelle de Dampierre.
In 1941, after the death of his paternal grandfather Alfonso XIII, Gonzalo moved with his family to Lausanne, Switzerland.
They lived first at the Hotel Royal before Gonzalo and his older brother Alfonso were sent to the Collège Saint-Jean in Fribourg.
The following year, General Francisco Franco allowed Gonzalo and Alfonso to continue their education in Spain.
In September 1955, Gonzalo and Alfonso were both injured in an automobile accident near Lausanne, on a return trip from Windsor during which they had driven all day and night.
In November 1961, Alfonso and Gonzalo, concerned that their father was wasting away his money, sought an injunction from a French court to compel him to turn over management of his affairs to a court-appointed trustee, being supported in their action by their grandmother, Queen Victoria Eugenie, as well as by other members of the Spanish royal family.
In January 1962, the court ruled that although there were insufficient grounds to find Jaime completely incompetent, a trustee was installed to restrain undue extravagance on his part.
On 8 March 1972, Jaime named Gonzalo a knight of the Order of the Holy Spirit and of the Order of Saint Michael; the declarative letters patent were dated 21 September 1972.
Also on 21 September 1972, Jaime gave Gonzalo the title duc d'Aquitaine (Duke of Aquitaine).



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
  AssignClass (0cee2319-22f3-41df-b42b-329f0ad187cc)
 Call ID: 0cee2319-22f3-41df-b42b-329f0ad187cc
  Args:
    type: :Man
    source: Gonzalo_de_Borbon_y_Dampierre
  AssignClass (7797e934-34b0-47c9-bc18-01e3b2efc168)
 Call ID: 7797e934-34b0-47c9-bc18-01e3b2efc168
  Args:
    type: :Person
    source: Gonzalo_de_Borbon_y_Dampierre
  AddLiteral (1f072cae-ddaa-4b32-ad51-ca9375e1b8b5)
 Call ID: 1f072cae-ddaa-4b32-ad51-ca9375e1b8b5
  Args:
    relation: :hasBirthYear
    literal_value: 1937
    literal_type: xsd:integer
    source: Gonzalo_de_Borbon_y_Dampierre
  AddLiteral (f3511fda-ad05-4e85-ab99-a5e02e4ac67e)
 Call ID: f3511fda-ad05-4e85-ab99-a5e02e4ac67e
  Args:
    source: Gonzalo_de_Borbon_y_Dampierre
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2000
  AssignClass (49eb1f1c-a244-40d7-b1f7-1428fe89d546)
 Call ID: 49eb1f1c-a244-40d7-b1f7-1428fe89d546
  Args:
    type: :Ancestor
    source: Alfonso_XIII_of_Spain
  AssignClass (32767ed8-3164-4676-a71c-67888f07f6e9)
 Call ID: 32767ed8-3164-4676-a71c-67888f07f6e9
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (dc48766b-3cfd-44e9-8583-8cee2c5b9b74)
 Call ID: dc48766b-3cfd-44e9-8583-8cee2c5b9b74
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (51a8eaa2-c24c-49cf-b67b-37cec54cb3f2)
 Call ID: 51a8eaa2-c24c-49cf-b67b-37cec54cb3f2
  Args:
    source: Alfonso_XIII_of_Spain
    relation: :isAncestorOf
    target: Gonzalo_de_Borbon_y_Dampierre
  AssignClass (36681d98-eb8a-4588-b498-cc6bcb978b16)
 Call ID: 36681d98-eb8a-4588-b498-cc6bcb978b16
  Args:
    type: :Ancestor
    source: Jaime_Duke_of_Segovia
  AssignClass (cbbc63c2-8776-43ae-8202-f5b8fd272f2a)
 Call ID: cbbc63c2-8776-43ae-8202-f5b8fd272f2a
  Args:
    type: :Man
    source: Jaime_Duke_of_Segovia
  AssignClass (be1eb551-2437-4d5e-89cf-1c4e77dc1281)
 Call ID: be1eb551-2437-4d5e-89cf-1c4e77dc1281
  Args:
    type: :Person
    source: Jaime_Duke_of_Segovia
  AddTriple (83be9ed8-d4ad-4c60-9fee-4073cf43b7cf)
 Call ID: 83be9ed8-d4ad-4c60-9fee-4073cf43b7cf
  Args:
    relation: :hasFather
    target: Jaime_Duke_of_Segovia
    source: Gonzalo_de_Borbon_y_Dampierre
  AssignClass (de2bcdc4-1ffa-4833-84a0-71349f7c6df7)
 Call ID: de2bcdc4-1ffa-4833-84a0-71349f7c6df7
  Args:
    type: :Woman
    source: Emmanuelle_de_Dampierre
  AssignClass (34005e6a-fd5e-4ec3-8cf8-d9c524032783)
 Call ID: 34005e6a-fd5e-4ec3-8cf8-d9c524032783
  Args:
    type: :Person
    source: Emmanuelle_de_Dampierre
  AddTriple (38a14961-2a12-4953-9122-b89028fe73b0)
 Call ID: 38a14961-2a12-4953-9122-b89028fe73b0
  Args:
    target: Emmanuelle_de_Dampierre
    relation: :hasMother
    source: Gonzalo_de_Borbon_y_Dampierre
  AssignClass (2e907502-a529-47c8-8be0-a60f7deaf1a2)
 Call ID: 2e907502-a529-47c8-8be0-a60f7deaf1a2
  Args:
    type: :Man
    source: Alfonso_brother_of_Gonzalo
  AssignClass (94f4ae93-495c-4054-8e5f-c5bed6ad9f2d)
 Call ID: 94f4ae93-495c-4054-8e5f-c5bed6ad9f2d
  Args:
    type: :Person
    source: Alfonso_brother_of_Gonzalo
  AddTriple (5fdb36a1-ac38-47be-bd9c-c8234ea476cf)
 Call ID: 5fdb36a1-ac38-47be-bd9c-c8234ea476cf
  Args:
    source: Gonzalo_de_Borbon_y_Dampierre
    relation: :hasBrother
    target: Alfonso_brother_of_Gonzalo
  AssignClass (65e70415-0e7a-43c6-8eaf-b83ea27bbe28)
 Call ID: 65e70415-0e7a-43c6-8eaf-b83ea27bbe28
  Args:
    type: :Woman
    source: Victoria_Eugenie_of_Battenberg
  AssignClass (73ecc3da-d6cd-496a-accf-81beca547973)
 Call ID: 73ecc3da-d6cd-496a-accf-81beca547973
  Args:
    type: :Person
    source: Victoria_Eugenie_of_Battenberg
  AddTriple (c03bffa6-9c6b-4211-83f1-ed040eb3fd71)
 Call ID: c03bffa6-9c6b-4211-83f1-ed040eb3fd71
  Args:
    relation: :isAncestorOf
    target: Gonzalo_de_Borbon_y_Dampierre
    source: Victoria_Eugenie_of_Battenberg
  Finish (76fd40e0-76a6-403b-817c-2417f7a454ae)
 Call ID: 76fd40e0-76a6-403b-817c-2417f7a454ae
  Args: