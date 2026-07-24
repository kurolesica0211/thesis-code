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
  AssignClass (a476b486-3ab3-49ca-b557-aea2b7b568b1)
 Call ID: a476b486-3ab3-49ca-b557-aea2b7b568b1
  Args:
    type: :Man
    source: :Duke_Paul_Frederick_of_Mecklenburg
  AssignClass (f4a81feb-620f-4164-affa-5768a541ab3a)
 Call ID: f4a81feb-620f-4164-affa-5768a541ab3a
  Args:
    type: :Person
    source: :Duke_Paul_Frederick_of_Mecklenburg
  AddLiteral (cec91120-6619-4796-ac25-974e51da9621)
 Call ID: cec91120-6619-4796-ac25-974e51da9621
  Args:
    relation: :hasBirthYear
    literal_value: 1852
    source: :Duke_Paul_Frederick_of_Mecklenburg
    literal_type: xsd:integer
  AddLiteral (2e11a3f5-d770-44be-b2d8-9b941940dac3)
 Call ID: 2e11a3f5-d770-44be-b2d8-9b941940dac3
  Args:
    literal_type: xsd:integer
    source: :Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1923
    relation: :hasDeathYear
  AssignClass (256faa5f-b338-46e4-a6e2-236424d3c3fd)
 Call ID: 256faa5f-b338-46e4-a6e2-236424d3c3fd
  Args:
    type: :Man
    source: :Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (99855de0-516c-428f-a731-a8e76c40e4f6)
 Call ID: 99855de0-516c-428f-a731-a8e76c40e4f6
  Args:
    type: :Person
    source: :Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (2fc637cb-e3d2-4b53-ae1d-05fd0b012d56)
 Call ID: 2fc637cb-e3d2-4b53-ae1d-05fd0b012d56
  Args:
    relation: :hasFather
    source: :Duke_Paul_Frederick_of_Mecklenburg
    target: :Frederick_Francis_II_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (29723b10-5c4c-43a9-99ca-3e0ea16e414b)
 Call ID: 29723b10-5c4c-43a9-99ca-3e0ea16e414b
  Args:
    type: :Woman
    source: :Princess_Augusta_Reuss_of_Köstritz
  AssignClass (519677be-ae43-451f-b507-30bc81002090)
 Call ID: 519677be-ae43-451f-b507-30bc81002090
  Args:
    type: :Person
    source: :Princess_Augusta_Reuss_of_Köstritz
  AddTriple (04a409b1-9a80-4744-a363-0126f8fe916c)
 Call ID: 04a409b1-9a80-4744-a363-0126f8fe916c
  Args:
    target: :Princess_Augusta_Reuss_of_Köstritz
    source: :Duke_Paul_Frederick_of_Mecklenburg
    relation: :hasMother
  AssignClass (2e436c74-c67d-432e-aaab-44a384055d2d)
 Call ID: 2e436c74-c67d-432e-aaab-44a384055d2d
  Args:
    type: :Man
    source: :Prince_Henry_LXIII_Reuss_of_Köstritz
  AssignClass (1d27b2c5-5356-4e3c-8d56-dcd1b3fd71fa)
 Call ID: 1d27b2c5-5356-4e3c-8d56-dcd1b3fd71fa
  Args:
    type: :Person
    source: :Prince_Henry_LXIII_Reuss_of_Köstritz
  AddTriple (f19aa931-57d6-405c-8c2b-15d62c318fb7)
 Call ID: f19aa931-57d6-405c-8c2b-15d62c318fb7
  Args:
    relation: :hasFather
    target: :Prince_Henry_LXIII_Reuss_of_Köstritz
    source: :Princess_Augusta_Reuss_of_Köstritz
  AssignClass (b1fe7444-241c-4d97-8de7-0640a0676262)
 Call ID: b1fe7444-241c-4d97-8de7-0640a0676262
  Args:
    type: :Woman
    source: :Princess_Marie_of_Windisch_Graetz
  AssignClass (4aba7894-5535-4873-b591-19675be57497)
 Call ID: 4aba7894-5535-4873-b591-19675be57497
  Args:
    type: :Person
    source: :Princess_Marie_of_Windisch_Graetz
  AddLiteral (c090c974-6c8e-49fa-a51b-b14ce84f2f9a)
 Call ID: c090c974-6c8e-49fa-a51b-b14ce84f2f9a
  Args:
    literal_type: xsd:integer
    source: :Duke_Paul_Frederick_of_Mecklenburg
    literal_value: 1881
    relation: :hasMarriageYear
  AddTriple (e42b6caf-1226-41d9-8879-3b3fb266a5ba)
 Call ID: e42b6caf-1226-41d9-8879-3b3fb266a5ba
  Args:
    relation: :hasRelation
    source: :Duke_Paul_Frederick_of_Mecklenburg
    target: :Princess_Marie_of_Windisch_Graetz
  AssignClass (e744ad83-a3f4-43e4-894e-bdff31b8c218)
 Call ID: e744ad83-a3f4-43e4-894e-bdff31b8c218
  Args:
    type: :Man
    source: :Prince_Hugo_of_Windisch_Graetz
  AssignClass (b2718df5-7653-4219-9b48-8cc5873a34e3)
 Call ID: b2718df5-7653-4219-9b48-8cc5873a34e3
  Args:
    type: :Person
    source: :Prince_Hugo_of_Windisch_Graetz
  AddTriple (1977685c-aa3a-4020-8a67-c1065c555267)
 Call ID: 1977685c-aa3a-4020-8a67-c1065c555267
  Args:
    relation: :hasFather
    target: :Prince_Hugo_of_Windisch_Graetz
    source: :Princess_Marie_of_Windisch_Graetz
  AssignClass (9c97ca2b-6ed0-473c-aa74-26f37c456dea)
 Call ID: 9c97ca2b-6ed0-473c-aa74-26f37c456dea
  Args:
    type: :Woman
    source: :Duchess_Louise_of_Mecklenburg_Schwerin
  AssignClass (b0995ab3-598a-4c32-abc4-4bdaded2a139)
 Call ID: b0995ab3-598a-4c32-abc4-4bdaded2a139
  Args:
    type: :Person
    source: :Duchess_Louise_of_Mecklenburg_Schwerin
  AddTriple (1b888e80-3274-4800-8e22-c5b3ac6b7d9d)
 Call ID: 1b888e80-3274-4800-8e22-c5b3ac6b7d9d
  Args:
    relation: :hasMother
    target: :Duchess_Louise_of_Mecklenburg_Schwerin
    source: :Princess_Marie_of_Windisch_Graetz
  AssignClass (be1864e2-6cf6-4219-97bb-65533a94660f)
 Call ID: be1864e2-6cf6-4219-97bb-65533a94660f
  Args:
    type: :Man
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AssignClass (290185d0-c832-4ddf-865f-1e63310590af)
 Call ID: 290185d0-c832-4ddf-865f-1e63310590af
  Args:
    type: :Person
    source: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
  AddTriple (5b2526c3-7487-404c-86e1-722de6f975fd)
 Call ID: 5b2526c3-7487-404c-86e1-722de6f975fd
  Args:
    target: :Frederick_Francis_IV_Grand_Duke_of_Mecklenburg_Schwerin
    source: :Duke_Paul_Frederick_of_Mecklenburg
    relation: :hasRelation
  Finish (095f0603-0026-4069-a410-7cc0f1054cfb)
 Call ID: 095f0603-0026-4069-a410-7cc0f1054cfb
  Args: