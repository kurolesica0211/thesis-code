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
Princess Maria Immaculata Cristina Pia Isabella of Bourbon-Two Sicilies (Full Italian name: Maria Immacolata Speranza Pia Teresa Cristina Filomena Lucia Anna Isabella Cecilia Apollonia Barbara Agnese Zenobia, Principessa di Borbone delle
Due Sicilie,) (30 October 1874 – 28 November 1947) was the fourth child and eldest daughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta, and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage

Maria Immaculata married Prince Johann Georg of Saxony, sixth child and second-eldest son of George of Saxony and his wife Maria Anna of Portugal, on 30 October 1906 in Cannes.
Her mother-in-law, Maria Anna, was the daughter of Maria II of Portugal and her husband Ferdinand II of Portugal.
The couple did not have children, but Maria Immaculata cared for the children of her brother-in-law Frederick Augustus III of Saxony.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (bdace8ca-9e2b-4915-b6b1-318bb85ae677)
 Call ID: bdace8ca-9e2b-4915-b6b1-318bb85ae677
  Args:
    type: :Woman
    source: MariaImmaculata
  AssignClass (f2d3fdea-f413-457f-b179-de84b309c803)
 Call ID: f2d3fdea-f413-457f-b179-de84b309c803
  Args:
    type: :Person
    source: MariaImmaculata
  AddLiteral (1944f5a3-0e7d-4d39-8ea3-54f76dfb42be)
 Call ID: 1944f5a3-0e7d-4d39-8ea3-54f76dfb42be
  Args:
    relation: :hasBirthYear
    literal_value: 1874
    literal_type: xsd:integer
    source: MariaImmaculata
  AddLiteral (d00f0ca6-0ff8-461e-baaa-b4b8c736dc75)
 Call ID: d00f0ca6-0ff8-461e-baaa-b4b8c736dc75
  Args:
    source: MariaImmaculata
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1947
  AssignClass (0252a5a7-eb6a-453f-8b37-f0c28159e087)
 Call ID: 0252a5a7-eb6a-453f-8b37-f0c28159e087
  Args:
    type: :Man
    source: Alfonso
  AssignClass (2c5c74b6-b198-4434-8e8d-567aa52f3f50)
 Call ID: 2c5c74b6-b198-4434-8e8d-567aa52f3f50
  Args:
    type: :Person
    source: Alfonso
  AssignClass (5377167c-d1cd-484e-a2c4-2559851ec8a2)
 Call ID: 5377167c-d1cd-484e-a2c4-2559851ec8a2
  Args:
    type: :Woman
    source: MariaAntonietta
  AssignClass (a8568abf-762d-44e9-be87-8baca40355a3)
 Call ID: a8568abf-762d-44e9-be87-8baca40355a3
  Args:
    type: :Person
    source: MariaAntonietta
  AddTriple (e91aec43-fc47-45fb-ac29-302271b66d6a)
 Call ID: e91aec43-fc47-45fb-ac29-302271b66d6a
  Args:
    relation: :hasFather
    source: MariaImmaculata
    target: Alfonso
  AddTriple (88efc2dc-eb98-451d-96bf-d3ea318f0587)
 Call ID: 88efc2dc-eb98-451d-96bf-d3ea318f0587
  Args:
    relation: :hasMother
    target: MariaAntonietta
    source: MariaImmaculata
  AssignClass (7fcea401-2db7-4e81-8d3f-80c2cd790bd4)
 Call ID: 7fcea401-2db7-4e81-8d3f-80c2cd790bd4
  Args:
    type: :Man
    source: JohannGeorg
  AssignClass (91636fcf-8902-4747-8199-717932c399d0)
 Call ID: 91636fcf-8902-4747-8199-717932c399d0
  Args:
    type: :Person
    source: JohannGeorg
  AddTriple (e9a700db-bcfb-4b01-91fd-bdf736aa46ee)
 Call ID: e9a700db-bcfb-4b01-91fd-bdf736aa46ee
  Args:
    relation: :hasRelation
    source: MariaImmaculata
    target: JohannGeorg
  AddLiteral (bc17c41e-0968-493c-8ac4-7ab11b49a42a)
 Call ID: bc17c41e-0968-493c-8ac4-7ab11b49a42a
  Args:
    relation: :hasMarriageYear
    literal_value: 1906
    source: MariaImmaculata
    literal_type: xsd:integer
  AssignClass (1dd34eb3-adba-4933-a898-b463e3b3bd7a)
 Call ID: 1dd34eb3-adba-4933-a898-b463e3b3bd7a
  Args:
    type: :Man
    source: GeorgeOfSaxony
  AssignClass (2dc71ac1-5197-424b-9a4d-f64e0c667739)
 Call ID: 2dc71ac1-5197-424b-9a4d-f64e0c667739
  Args:
    type: :Person
    source: GeorgeOfSaxony
  AssignClass (9541fe6e-7f3f-4156-8067-d7be58afee78)
 Call ID: 9541fe6e-7f3f-4156-8067-d7be58afee78
  Args:
    type: :Woman
    source: MariaAnnaOfPortugal
  AssignClass (c7086330-7b91-40a6-ab85-3855d925e333)
 Call ID: c7086330-7b91-40a6-ab85-3855d925e333
  Args:
    type: :Person
    source: MariaAnnaOfPortugal
  AddTriple (c8caa2ef-5219-4b21-b02e-b82856b84a75)
 Call ID: c8caa2ef-5219-4b21-b02e-b82856b84a75
  Args:
    relation: :hasFather
    target: GeorgeOfSaxony
    source: JohannGeorg
  AddTriple (8f9c9890-d25d-45af-b529-e205854b2c56)
 Call ID: 8f9c9890-d25d-45af-b529-e205854b2c56
  Args:
    target: MariaAnnaOfPortugal
    source: JohannGeorg
    relation: :hasMother
  AssignClass (68a17c08-f26c-4f79-8aa5-d2fea0f5e245)
 Call ID: 68a17c08-f26c-4f79-8aa5-d2fea0f5e245
  Args:
    type: :Woman
    source: MariaIIOfPortugal
  AssignClass (2786df64-f6f9-4658-ae3f-66d3abf6073f)
 Call ID: 2786df64-f6f9-4658-ae3f-66d3abf6073f
  Args:
    type: :Person
    source: MariaIIOfPortugal
  AssignClass (f7361c2d-cd5e-4d89-80d1-4f4cee2f1778)
 Call ID: f7361c2d-cd5e-4d89-80d1-4f4cee2f1778
  Args:
    type: :Man
    source: FerdinandIIOfPortugal
  AssignClass (68aafaee-0eeb-4182-98df-4704d675f4cc)
 Call ID: 68aafaee-0eeb-4182-98df-4704d675f4cc
  Args:
    type: :Person
    source: FerdinandIIOfPortugal
  AddTriple (46c8b277-174c-4f4d-945a-8222ff3338c9)
 Call ID: 46c8b277-174c-4f4d-945a-8222ff3338c9
  Args:
    source: MariaAnnaOfPortugal
    target: MariaIIOfPortugal
    relation: :hasMother
  AddTriple (442c3739-e614-454c-8b6a-29551a73c169)
 Call ID: 442c3739-e614-454c-8b6a-29551a73c169
  Args:
    target: FerdinandIIOfPortugal
    source: MariaAnnaOfPortugal
    relation: :hasFather
  AssignClass (fb25697c-a822-44e2-86a3-2ffd268d1612)
 Call ID: fb25697c-a822-44e2-86a3-2ffd268d1612
  Args:
    type: :Man
    source: FrederickAugustusIII
  AssignClass (aa355d4b-c72d-4b6c-99ae-30070816e698)
 Call ID: aa355d4b-c72d-4b6c-99ae-30070816e698
  Args:
    type: :Person
    source: FrederickAugustusIII
  AddTriple (c24159f1-624d-4d35-9f83-db15c168de52)
 Call ID: c24159f1-624d-4d35-9f83-db15c168de52
  Args:
    relation: :hasRelation
    source: MariaImmaculata
    target: FrederickAugustusIII
  Finish (8d6805d7-d148-407f-b73e-1cff0d109859)
 Call ID: 8d6805d7-d148-407f-b73e-1cff0d109859
  Args: