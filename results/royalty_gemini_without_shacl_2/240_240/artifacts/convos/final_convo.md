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
Victoria Federica de Todos los Santos de Marichalar y Borbón, Lady of Tejada GE (born 9 September 2000) is the younger child and only daughter of Infanta Elena, Duchess of Lugo, and Jaime de Marichalar.
She is a granddaughter of King Juan Carlos I and Queen Sofía of Spain and a niece of King Felipe VI.
Victoria is fifth in the line of succession to the Spanish throne after her cousins, King Felipe's daughters Leonor, Princess of Asturias, and Infanta Sofía; her mother; and her brother, Felipe.
Early life and education

Victoria de Marichalar y Borbón was born 9 September 2000 at 13:00 in Ruber International Hospital in Madrid.
She made her first Holy Communion on 27 May 2009 at the Dominicos Church in Alcobendas, Spain.
Then she studied at a British boarding school for 3 years before returning to Spain at St. George's de La Moraleja.
Victoria studied ballet and horse riding.
Career

Marichalar has been reported to be working in the fashion industry and is quoted as saying that fashion is her "true calling".



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
  AssignClass (0d72881f-639c-4089-b73b-fdd2fe28be6b)
 Call ID: 0d72881f-639c-4089-b73b-fdd2fe28be6b
  Args:
    type: :Woman
    source: Victoria_Federica_de_Marichalar_y_Borbon
  AssignClass (f6def3d8-f771-4fc6-a149-d3e6b860c2a9)
 Call ID: f6def3d8-f771-4fc6-a149-d3e6b860c2a9
  Args:
    type: :Person
    source: Victoria_Federica_de_Marichalar_y_Borbon
  AddLiteral (bc5be664-624a-4bd2-98b9-1226cb68aea2)
 Call ID: bc5be664-624a-4bd2-98b9-1226cb68aea2
  Args:
    literal_type: xsd:string
    literal_value: Female
    source: Victoria_Federica_de_Marichalar_y_Borbon
    relation: :hasSex
  AddLiteral (cedd4fb6-5e89-4536-a4f1-a80fb3a870e0)
 Call ID: cedd4fb6-5e89-4536-a4f1-a80fb3a870e0
  Args:
    source: Victoria_Federica_de_Marichalar_y_Borbon
    literal_type: xsd:integer
    literal_value: 2000
    relation: :hasBirthYear
  AssignClass (e6c8937b-cdcd-4cc8-8db3-9232dd9f8002)
 Call ID: e6c8937b-cdcd-4cc8-8db3-9232dd9f8002
  Args:
    type: :Woman
    source: Infanta_Elena
  AssignClass (4ff01e51-ebe9-43a2-bca9-88e233fd06e7)
 Call ID: 4ff01e51-ebe9-43a2-bca9-88e233fd06e7
  Args:
    type: :Person
    source: Infanta_Elena
  AssignClass (15b1ccb6-d7c0-4963-8034-e9dc47f9bd74)
 Call ID: 15b1ccb6-d7c0-4963-8034-e9dc47f9bd74
  Args:
    type: :Man
    source: Jaime_de_Marichalar
  AssignClass (fdf21def-f975-466d-b39d-612fb8fed1a9)
 Call ID: fdf21def-f975-466d-b39d-612fb8fed1a9
  Args:
    type: :Person
    source: Jaime_de_Marichalar
  AddTriple (a2675418-5801-4f32-9720-6782b45184fb)
 Call ID: a2675418-5801-4f32-9720-6782b45184fb
  Args:
    relation: :hasMother
    target: Infanta_Elena
    source: Victoria_Federica_de_Marichalar_y_Borbon
  AddTriple (748a1ab5-9ed9-44f8-b0d7-2c09a1905e70)
 Call ID: 748a1ab5-9ed9-44f8-b0d7-2c09a1905e70
  Args:
    relation: :hasFather
    target: Jaime_de_Marichalar
    source: Victoria_Federica_de_Marichalar_y_Borbon
  AssignClass (9050078f-5834-4af6-b184-4bbe42acc0dd)
 Call ID: 9050078f-5834-4af6-b184-4bbe42acc0dd
  Args:
    type: :Man
    source: King_Juan_Carlos_I
  AssignClass (46758215-c839-44de-a485-274ca275b793)
 Call ID: 46758215-c839-44de-a485-274ca275b793
  Args:
    type: :Person
    source: King_Juan_Carlos_I
  AssignClass (c1939cc5-eb01-4693-9e99-00237670f3da)
 Call ID: c1939cc5-eb01-4693-9e99-00237670f3da
  Args:
    type: :Woman
    source: Queen_Sofia
  AssignClass (fddab38f-d951-4508-9d85-8999c437680a)
 Call ID: fddab38f-d951-4508-9d85-8999c437680a
  Args:
    type: :Person
    source: Queen_Sofia
  AddTriple (b8744954-ae60-49c3-8920-fc1854b4e5c6)
 Call ID: b8744954-ae60-49c3-8920-fc1854b4e5c6
  Args:
    relation: :hasParent
    target: King_Juan_Carlos_I
    source: Infanta_Elena
  AddTriple (9b9b2969-640e-4bbb-9a2d-e158f0182047)
 Call ID: 9b9b2969-640e-4bbb-9a2d-e158f0182047
  Args:
    relation: :hasParent
    target: Queen_Sofia
    source: Infanta_Elena
  AssignClass (2de0b6e6-c8e0-477f-824e-3d6b79864f4e)
 Call ID: 2de0b6e6-c8e0-477f-824e-3d6b79864f4e
  Args:
    type: :Man
    source: King_Felipe_VI
  AssignClass (827099a7-885e-4abc-9f2c-9bd63119dad4)
 Call ID: 827099a7-885e-4abc-9f2c-9bd63119dad4
  Args:
    type: :Person
    source: King_Felipe_VI
  AssignClass (2d3d914a-0714-48f4-8611-218ffc374d61)
 Call ID: 2d3d914a-0714-48f4-8611-218ffc374d61
  Args:
    type: :Woman
    source: Leonor_Princess_of_Asturias
  AssignClass (1cfca7be-2c5b-4693-ad2c-46a01241b129)
 Call ID: 1cfca7be-2c5b-4693-ad2c-46a01241b129
  Args:
    type: :Person
    source: Leonor_Princess_of_Asturias
  AssignClass (461e393e-13ca-4be8-85a5-aa2184d49fbf)
 Call ID: 461e393e-13ca-4be8-85a5-aa2184d49fbf
  Args:
    type: :Woman
    source: Infanta_Sofia
  AssignClass (7a9d1e51-95e4-46c0-8034-7bd7a0531c85)
 Call ID: 7a9d1e51-95e4-46c0-8034-7bd7a0531c85
  Args:
    type: :Person
    source: Infanta_Sofia
  AddTriple (475a4c58-bd05-4aaa-87d2-23b461179e31)
 Call ID: 475a4c58-bd05-4aaa-87d2-23b461179e31
  Args:
    relation: :hasFather
    target: King_Felipe_VI
    source: Leonor_Princess_of_Asturias
  AddTriple (71a9a43b-736d-4a89-ad13-6c68e38b3ef3)
 Call ID: 71a9a43b-736d-4a89-ad13-6c68e38b3ef3
  Args:
    source: Infanta_Sofia
    relation: :hasFather
    target: King_Felipe_VI
  AssignClass (3093dc7d-fd7e-47be-a13d-52fe9cc8e22b)
 Call ID: 3093dc7d-fd7e-47be-a13d-52fe9cc8e22b
  Args:
    type: :Man
    source: Felipe_de_Marichalar
  AssignClass (5b8f4fbc-7a7b-4fe4-92c9-e126700f8ca8)
 Call ID: 5b8f4fbc-7a7b-4fe4-92c9-e126700f8ca8
  Args:
    type: :Person
    source: Felipe_de_Marichalar
  AddTriple (e04591d8-7e89-4a76-908c-ab543798efb2)
 Call ID: e04591d8-7e89-4a76-908c-ab543798efb2
  Args:
    source: Felipe_de_Marichalar
    relation: :hasMother
    target: Infanta_Elena
  AddTriple (d827278f-8413-4ee6-bd88-ad27662ce279)
 Call ID: d827278f-8413-4ee6-bd88-ad27662ce279
  Args:
    target: Jaime_de_Marichalar
    relation: :hasFather
    source: Felipe_de_Marichalar
  Finish (e509f720-9b9c-403d-bf3c-8eb7b9bac557)
 Call ID: e509f720-9b9c-403d-bf3c-8eb7b9bac557
  Args: