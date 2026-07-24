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
Duke Paul Frederick of Mecklenburg (German: Herzog Paul Friedrich zu Mecklenburg; 19 September 1852 – 17 May 1923) was a member of the House of Mecklenburg-Schwerin and general of the Mecklenburg cavalry.
Life

Duke Paul Frederick was born in Ludwigslust Castle as the second eldest son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and his first wife Princess Augusta Reuss of Köstritz, the daughter of Prince Henry LXIII Reuss of Köstritz.
Duke Paul Frederick married in Schwerin on 5 May 1881 his cousin, the Austrian born Princess Marie of Windisch-Graetz, the daughter of Prince Hugo of Windisch-Graetz and his wife Duchess Louise of Mecklenburg-Schwerin.
The couple who had five children who were all raised Roman Catholic, the religion of Princess Marie, lived a quiet life in Venice.
On 21 April 1884 Duke Paul Frederick renounced his and his sons rights of succession to Mecklenburg-Schwerin in favour of his younger brothers and their sons, so they would take precedence over him and his.
In 1887, Duke Paul Fredrick raised a Lutheran decided to convert to Roman Catholicism the religion of his wife and children.
In 1906 after upsetting his nephew Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, over the amount of money that he was spending Duke Paul Frederick and his wife were ordered to submit to the controller of the royal household.
Duke Paul Frederick died in Ludwigslust, where he and his wife are both buried in the Louisenkapelle.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (0301c990-a2b8-42a9-8601-0c0fe965e8a1)
 Call ID: 0301c990-a2b8-42a9-8601-0c0fe965e8a1
  Args:
    type: :Man
    source: Duke_Paul_Frederick_of_Mecklenburg
  AssignClass (df2ac1d1-446a-4b78-a3c7-da49df9456c3)
 Call ID: df2ac1d1-446a-4b78-a3c7-da49df9456c3
  Args:
    type: :Person
    source: Duke_Paul_Frederick_of_Mecklenburg
  AddLiteral (091b2d34-6991-4e78-a8d7-6704d0ac44a0)
 Call ID: 091b2d34-6991-4e78-a8d7-6704d0ac44a0
  Args:
    relation: :hasBirthYear
    source: Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1852
    literal_type: xsd:integer
  AddLiteral (0211603d-4b24-4a1b-addc-990edba55fd0)
 Call ID: 0211603d-4b24-4a1b-addc-990edba55fd0
  Args:
    literal_value: 1923
    source: Duke_Paul_Frederick_of_Mecklenburg
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (2e281374-b021-41e9-95fe-478bc871cffb)
 Call ID: 2e281374-b021-41e9-95fe-478bc871cffb
  Args:
    type: :Man
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (a3c3af4e-fda9-486c-9a72-c914e782a400)
 Call ID: a3c3af4e-fda9-486c-9a72-c914e782a400
  Args:
    type: :Person
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (7a2c3041-303a-488e-9ce4-f584646c4a33)
 Call ID: 7a2c3041-303a-488e-9ce4-f584646c4a33
  Args:
    target: Duke_Paul_Frederick_of_Mecklenburg
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
    relation: :isFatherOf
  AssignClass (0bde59d0-44bd-422a-b176-dcaf06ec9436)
 Call ID: 0bde59d0-44bd-422a-b176-dcaf06ec9436
  Args:
    type: :Woman
    source: Princess_Augusta_Reuss_of_Köstritz
  AssignClass (848c65a1-e2b7-426d-9f0b-aa216f0d7975)
 Call ID: 848c65a1-e2b7-426d-9f0b-aa216f0d7975
  Args:
    type: :Person
    source: Princess_Augusta_Reuss_of_Köstritz
  AddTriple (05ea3d44-1450-4007-918f-5bd3aa28317a)
 Call ID: 05ea3d44-1450-4007-918f-5bd3aa28317a
  Args:
    relation: :isMotherOf
    source: Princess_Augusta_Reuss_of_Köstritz
    target: Duke_Paul_Frederick_of_Mecklenburg
  AssignClass (dff30694-c671-47ef-8a03-a0feef7183d0)
 Call ID: dff30694-c671-47ef-8a03-a0feef7183d0
  Args:
    type: :Man
    source: Prince_Henry_LXIII_Reuss_of_Köstritz
  AssignClass (38f1e8ea-9e44-46bc-a45e-56e92e3938f3)
 Call ID: 38f1e8ea-9e44-46bc-a45e-56e92e3938f3
  Args:
    type: :Person
    source: Prince_Henry_LXIII_Reuss_of_Köstritz
  AddTriple (e88e0114-88a0-401b-8f30-b462cd34b9f2)
 Call ID: e88e0114-88a0-401b-8f30-b462cd34b9f2
  Args:
    target: Princess_Augusta_Reuss_of_Köstritz
    relation: :isFatherOf
    source: Prince_Henry_LXIII_Reuss_of_Köstritz
  AssignClass (61ab5212-c38d-400c-b56e-1f244e1c5780)
 Call ID: 61ab5212-c38d-400c-b56e-1f244e1c5780
  Args:
    type: :Woman
    source: Princess_Marie_of_Windisch_Graetz
  AssignClass (76084a45-f0ef-46b8-97ff-f2c58a4f5dba)
 Call ID: 76084a45-f0ef-46b8-97ff-f2c58a4f5dba
  Args:
    type: :Person
    source: Princess_Marie_of_Windisch_Graetz
  AddLiteral (69937d11-9d9d-4246-9728-6caf337f061d)
 Call ID: 69937d11-9d9d-4246-9728-6caf337f061d
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1881
  AddTriple (29a45bda-db3e-479d-a9e3-e173fba89bab)
 Call ID: 29a45bda-db3e-479d-a9e3-e173fba89bab
  Args:
    source: Duke_Paul_Frederick_of_Mecklenburg
    relation: :hasRelation
    target: Princess_Marie_of_Windisch_Graetz
  AssignClass (8c0c82c6-621d-4dc2-a14a-e2974d871b6a)
 Call ID: 8c0c82c6-621d-4dc2-a14a-e2974d871b6a
  Args:
    type: :Man
    source: Prince_Hugo_of_Windisch_Graetz
  AssignClass (41cd71a0-7ba1-459e-b72d-e510a5f9c9eb)
 Call ID: 41cd71a0-7ba1-459e-b72d-e510a5f9c9eb
  Args:
    type: :Person
    source: Prince_Hugo_of_Windisch_Graetz
  AddTriple (98bb2c1f-4590-4229-a960-bd13bdcf7ceb)
 Call ID: 98bb2c1f-4590-4229-a960-bd13bdcf7ceb
  Args:
    target: Princess_Marie_of_Windisch_Graetz
    relation: :isFatherOf
    source: Prince_Hugo_of_Windisch_Graetz
  AssignClass (7f111338-a7c3-4517-b83c-dcc99a786ae2)
 Call ID: 7f111338-a7c3-4517-b83c-dcc99a786ae2
  Args:
    type: :Woman
    source: Duchess_Louise_of_Mecklenburg_Schwerin
  AssignClass (b65a4455-acad-43df-99f3-d2da91c9eca2)
 Call ID: b65a4455-acad-43df-99f3-d2da91c9eca2
  Args:
    type: :Person
    source: Duchess_Louise_of_Mecklenburg_Schwerin
  AddTriple (2e4dd0aa-6fc5-4ac5-a9e3-805b40e29b08)
 Call ID: 2e4dd0aa-6fc5-4ac5-a9e3-805b40e29b08
  Args:
    source: Duchess_Louise_of_Mecklenburg_Schwerin
    relation: :isMotherOf
    target: Princess_Marie_of_Windisch_Graetz
  AssignClass (581366a0-61ca-441d-b4bb-d49a7d87c484)
 Call ID: 581366a0-61ca-441d-b4bb-d49a7d87c484
  Args:
    type: :Man
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (6ec05d17-f655-4d31-8f41-c703c79362de)
 Call ID: 6ec05d17-f655-4d31-8f41-c703c79362de
  Args:
    type: :Person
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  Finish (9b6c2993-2692-405a-aecf-583a92d03dd5)
 Call ID: 9b6c2993-2692-405a-aecf-583a92d03dd5
  Args: