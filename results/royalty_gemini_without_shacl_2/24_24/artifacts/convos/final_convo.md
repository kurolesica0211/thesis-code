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
Duchess Marie Antoinette of Mecklenburg-Schwerin, also Manette (Marie Antoinette Margarethe Mathilde; 28 May 1884 – 26 October 1944) was the Duchess of Mecklenburg-Schwerin by birth and potential bride for King Alfonso XIII of Spain.
Early life

Marie Antoinette was born in Venice, into the House of Mecklenburg, as the third child and the second daughter of Duke Paul Frederick of Mecklenburg and Princess Marie of Windisch-Graetz.
Her brothers and sisters were Duke Paul Friedrich of Mecklenburg, Duchess Maria Luise of Mecklenburg-Schwerin (1883–1883), Duke Heinrich Borwin of Mecklenburg-Schwerin (1885–1942), and Duke Joseph of Mecklenburg-Schwerin (1889–1889).
She had a difficult relationship with her cousin Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, who regularly had to amortize her debts.
So, Marie Antoinette regularly had to sell archaeological artifacts belonging to her mother, excavated in Austria and Carniola, including Hallstatt Archaeological Site in Vače.
Potential bride for the King of Spain

She was German Kaiser Wilhelm II's candidate for a bride for King Alfonso XIII of Spain although he would marry the Kaiser's maternal first cousin, Princess Victoria Eugenie, niece of British King Edward VII.



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
  AssignClass (b859b396-c840-45dd-904f-f039aba02611)
 Call ID: b859b396-c840-45dd-904f-f039aba02611
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (edcbc97f-de36-433d-b9c0-3daf98df3586)
 Call ID: edcbc97f-de36-433d-b9c0-3daf98df3586
  Args:
    type: :Person
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AddLiteral (5b7b2e46-e5c1-4f64-bcba-cfa63ca43290)
 Call ID: 5b7b2e46-e5c1-4f64-bcba-cfa63ca43290
  Args:
    literal_type: xsd:string
    literal_value: Manette
    relation: :alsoKnownAs
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AddLiteral (d31baf27-fc14-482b-8976-d6075a9e0710)
 Call ID: d31baf27-fc14-482b-8976-d6075a9e0710
  Args:
    literal_type: xsd:integer
    literal_value: 1884
    relation: :hasBirthYear
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AddLiteral (9d51348e-daf7-4b48-a569-35d4fec9971b)
 Call ID: 9d51348e-daf7-4b48-a569-35d4fec9971b
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    literal_value: 1944
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (df750ca1-ffd1-46a8-a1f7-2d50406077dc)
 Call ID: df750ca1-ffd1-46a8-a1f7-2d50406077dc
  Args:
    type: :Man
    source: Paul_Frederick_of_Mecklenburg
  AssignClass (3f8f8006-5be3-4a41-8d0e-aad0b2db08b2)
 Call ID: 3f8f8006-5be3-4a41-8d0e-aad0b2db08b2
  Args:
    source: Paul_Frederick_of_Mecklenburg
    type: :Person
  AssignClass (ed703bdd-284f-4df5-a3cc-b855248b5d09)
 Call ID: ed703bdd-284f-4df5-a3cc-b855248b5d09
  Args:
    type: :Woman
    source: Marie_of_Windisch-Graetz
  AssignClass (2a05fba7-893f-4607-8dfc-65871a5691d3)
 Call ID: 2a05fba7-893f-4607-8dfc-65871a5691d3
  Args:
    type: :Person
    source: Marie_of_Windisch-Graetz
  AddTriple (a9158819-bcbf-42cc-8933-eef5f93bf903)
 Call ID: a9158819-bcbf-42cc-8933-eef5f93bf903
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Paul_Frederick_of_Mecklenburg
    relation: :hasFather
  AddTriple (1405f511-794f-4c08-b987-bc8bc963d0d6)
 Call ID: 1405f511-794f-4c08-b987-bc8bc963d0d6
  Args:
    relation: :hasMother
    target: Marie_of_Windisch-Graetz
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AssignClass (7d329db2-594f-4681-9f07-bc8291255a96)
 Call ID: 7d329db2-594f-4681-9f07-bc8291255a96
  Args:
    source: Paul_Friedrich_of_Mecklenburg
    type: :Man
  AssignClass (ac30bbd3-44f5-493e-99e7-54ae24b51c86)
 Call ID: ac30bbd3-44f5-493e-99e7-54ae24b51c86
  Args:
    type: :Person
    source: Paul_Friedrich_of_Mecklenburg
  AssignClass (0bece2b7-e1a3-4aca-a632-45680b2fb560)
 Call ID: 0bece2b7-e1a3-4aca-a632-45680b2fb560
  Args:
    type: :Woman
    source: Maria_Luise_of_Mecklenburg-Schwerin
  AssignClass (c6b250e0-484b-4dbb-bf67-b43aeb196b2d)
 Call ID: c6b250e0-484b-4dbb-bf67-b43aeb196b2d
  Args:
    source: Maria_Luise_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (99e6eca8-8b69-46fb-a38a-a66a043a24e6)
 Call ID: 99e6eca8-8b69-46fb-a38a-a66a043a24e6
  Args:
    type: :Man
    source: Heinrich_Borwin_of_Mecklenburg-Schwerin
  AssignClass (e5023491-0c60-4db7-87de-f5e64fc8d289)
 Call ID: e5023491-0c60-4db7-87de-f5e64fc8d289
  Args:
    type: :Person
    source: Heinrich_Borwin_of_Mecklenburg-Schwerin
  AssignClass (36af4f28-859e-4a3b-9cd7-143e3f1d62de)
 Call ID: 36af4f28-859e-4a3b-9cd7-143e3f1d62de
  Args:
    type: :Man
    source: Joseph_of_Mecklenburg-Schwerin
  AssignClass (84f1bc37-146f-4db8-8ecd-4847d9dca06b)
 Call ID: 84f1bc37-146f-4db8-8ecd-4847d9dca06b
  Args:
    source: Joseph_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (c02bfeab-58b0-4fa0-8a1a-f116bb680b15)
 Call ID: c02bfeab-58b0-4fa0-8a1a-f116bb680b15
  Args:
    relation: :isSiblingOf
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Paul_Friedrich_of_Mecklenburg
  AddTriple (89dacf4f-8cc0-4b3b-9500-31275f5964de)
 Call ID: 89dacf4f-8cc0-4b3b-9500-31275f5964de
  Args:
    relation: :isSiblingOf
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Maria_Luise_of_Mecklenburg-Schwerin
  AddTriple (a794409a-50cc-480c-ae68-1f42d7d247cc)
 Call ID: a794409a-50cc-480c-ae68-1f42d7d247cc
  Args:
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    target: Heinrich_Borwin_of_Mecklenburg-Schwerin
    relation: :isSiblingOf
  AddTriple (9b236dc8-be9d-4be8-8536-d70b0f925e68)
 Call ID: 9b236dc8-be9d-4be8-8536-d70b0f925e68
  Args:
    relation: :isSiblingOf
    target: Joseph_of_Mecklenburg-Schwerin
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
  AddLiteral (29893d06-4057-4f68-a78c-9c8c8df3ef68)
 Call ID: 29893d06-4057-4f68-a78c-9c8c8df3ef68
  Args:
    literal_type: xsd:integer
    source: Maria_Luise_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_value: 1883
  AddLiteral (da850a22-988d-4937-8aef-ebf8babdd044)
 Call ID: da850a22-988d-4937-8aef-ebf8babdd044
  Args:
    literal_type: xsd:integer
    source: Maria_Luise_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_value: 1883
  AddLiteral (fbca24f7-a4b5-4c3f-851a-1f2bd7d66ccd)
 Call ID: fbca24f7-a4b5-4c3f-851a-1f2bd7d66ccd
  Args:
    source: Heinrich_Borwin_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
    literal_value: 1885
    literal_type: xsd:integer
  AddLiteral (14ef6584-5638-4790-8896-0c8d12ae6731)
 Call ID: 14ef6584-5638-4790-8896-0c8d12ae6731
  Args:
    source: Heinrich_Borwin_of_Mecklenburg-Schwerin
    literal_value: 1942
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (2bd14b8f-ca58-4675-b210-9f31f4f51942)
 Call ID: 2bd14b8f-ca58-4675-b210-9f31f4f51942
  Args:
    literal_value: 1889
    relation: :hasBirthYear
    source: Joseph_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddLiteral (e32e2847-ab2c-42f5-9851-93f49da2143f)
 Call ID: e32e2847-ab2c-42f5-9851-93f49da2143f
  Args:
    source: Joseph_of_Mecklenburg-Schwerin
    literal_value: 1889
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (c1d3dc95-0b8e-4fde-a275-43748a7f8ca5)
 Call ID: c1d3dc95-0b8e-4fde-a275-43748a7f8ca5
  Args:
    type: :Man
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (3e7d38b2-c8ef-43fa-8186-c5471221a66e)
 Call ID: 3e7d38b2-c8ef-43fa-8186-c5471221a66e
  Args:
    type: :Person
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddTriple (934bf2ef-efbd-4265-82a8-597034e1459d)
 Call ID: 934bf2ef-efbd-4265-82a8-597034e1459d
  Args:
    target: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    source: Marie_Antoinette_of_Mecklenburg-Schwerin
    relation: :isBloodrelationOf
  Finish (71cd6c30-75de-45e8-8e90-a24ba40f2435)
 Call ID: 71cd6c30-75de-45e8-8e90-a24ba40f2435
  Args: