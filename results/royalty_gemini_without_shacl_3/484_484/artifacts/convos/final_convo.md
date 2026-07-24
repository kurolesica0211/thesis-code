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
Archduchess Helena of Austria (full German name: Helena Marie Alice Christine Josefa Anna Margareta Madeleine Walburga Blandina Cäcilie Philomena Carmela Ignatia Rita de Cascia, Erzherzogin von Österreich, Prinzessin von Toskana; 30 October 1903 – 8 September 1924) was a member of the Tuscan branch of the House of Habsburg-Lorraine and an Archduchess of Austria and Princess of Bohemia, Hungary, and Tuscany by birth.
Through her marriage to Philipp Albrecht, Hereditary Duke of Württemberg, Helena became a member of the House of Württemberg and Hereditary Duchess consort of Württemberg.
Early life

Helena was born in Linz, Austria-Hungary, the second-eldest child and eldest daughter of Archduke Peter Ferdinand, Prince of Tuscany and his wife Princess Maria Cristina of Bourbon-Two Sicilies.
Helena was raised with her three siblings in Salzburg and Vienna until the end of World War I in 1918 when her family was exiled and moved to Lucerne, Switzerland.
Marriage and issue

Helena married Philipp Albrecht, Hereditary Duke of Württemberg, eldest child and son of Albrecht, Duke of Württemberg and his wife, Archduchess Margarete Sophie of Austria, on 24 October 1923 in Altshausen.
Helena and Philipp Albrecht had one daughter:


Death

Helena died just a week after giving birth to her daughter Maria Christina, aged only 20.
Her husband later married her sister Archduchess Rosa of Austria, Princess of Tuscany in 1928.



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
  AssignClass (559f7983-5aac-4d2c-8dce-c58e2a53daa6)
 Call ID: 559f7983-5aac-4d2c-8dce-c58e2a53daa6
  Args:
    source: Helena_of_Austria
    type: :Woman
  AssignClass (f32e7a6a-5c42-443f-ad0c-6cfbf76d2002)
 Call ID: f32e7a6a-5c42-443f-ad0c-6cfbf76d2002
  Args:
    type: :Person
    source: Helena_of_Austria
  AddLiteral (493229a3-e857-48ce-b24a-982ef9596f5a)
 Call ID: 493229a3-e857-48ce-b24a-982ef9596f5a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1903
    source: Helena_of_Austria
  AddLiteral (c640dbc1-27c2-4aee-8931-da8fcc07433e)
 Call ID: c640dbc1-27c2-4aee-8931-da8fcc07433e
  Args:
    literal_value: 1924
    source: Helena_of_Austria
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (14504e81-9bf6-47d1-81bb-7868549f45bd)
 Call ID: 14504e81-9bf6-47d1-81bb-7868549f45bd
  Args:
    type: :Man
    source: Peter_Ferdinand_of_Austria
  AssignClass (b8870b70-a48b-4a52-a80b-6d21ad24cdc5)
 Call ID: b8870b70-a48b-4a52-a80b-6d21ad24cdc5
  Args:
    type: :Person
    source: Peter_Ferdinand_of_Austria
  AssignClass (6f58cd1f-48aa-4cdb-b594-cd5d54c3efe4)
 Call ID: 6f58cd1f-48aa-4cdb-b594-cd5d54c3efe4
  Args:
    source: Peter_Ferdinand_of_Austria
    type: :Ancestor
  AssignClass (3bd2bfce-f074-4d36-9840-653183476511)
 Call ID: 3bd2bfce-f074-4d36-9840-653183476511
  Args:
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (152719bf-d6de-440a-86cf-96b18e3a099e)
 Call ID: 152719bf-d6de-440a-86cf-96b18e3a099e
  Args:
    type: :Person
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AssignClass (87405ab1-be49-4a93-9ac3-5600f5bb348b)
 Call ID: 87405ab1-be49-4a93-9ac3-5600f5bb348b
  Args:
    type: :Ancestor
    source: Maria_Cristina_of_Bourbon-Two_Sicilies
  AddTriple (2fd2f491-4974-4246-b9f2-e28ccb7419d8)
 Call ID: 2fd2f491-4974-4246-b9f2-e28ccb7419d8
  Args:
    target: Peter_Ferdinand_of_Austria
    source: Helena_of_Austria
    relation: :hasFather
  AddTriple (aeef6e1d-1432-4b0a-a781-d954db8355c3)
 Call ID: aeef6e1d-1432-4b0a-a781-d954db8355c3
  Args:
    target: Maria_Cristina_of_Bourbon-Two_Sicilies
    source: Helena_of_Austria
    relation: :hasMother
  AssignClass (8d230343-d5e7-43f9-bff0-8ef5b418f74f)
 Call ID: 8d230343-d5e7-43f9-bff0-8ef5b418f74f
  Args:
    source: Philipp_Albrecht_of_Württemberg
    type: :Man
  AssignClass (40117bec-171c-4a9b-bfb3-6852589396ba)
 Call ID: 40117bec-171c-4a9b-bfb3-6852589396ba
  Args:
    type: :Person
    source: Philipp_Albrecht_of_Württemberg
  AssignClass (08c3cfd3-1797-4451-9eec-5c6e5c70e30a)
 Call ID: 08c3cfd3-1797-4451-9eec-5c6e5c70e30a
  Args:
    type: :Ancestor
    source: Philipp_Albrecht_of_Württemberg
  AddLiteral (71714c7a-02a2-49d8-8ad5-55e1166c222e)
 Call ID: 71714c7a-02a2-49d8-8ad5-55e1166c222e
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1923
    source: Helena_of_Austria
  AddTriple (e1fd90c6-e0c0-4eb8-9360-fc787a44fded)
 Call ID: e1fd90c6-e0c0-4eb8-9360-fc787a44fded
  Args:
    source: Helena_of_Austria
    target: Philipp_Albrecht_of_Württemberg
    relation: :hasRelation
  AssignClass (28848f21-bc1f-4e85-a66d-256a83e3b6fb)
 Call ID: 28848f21-bc1f-4e85-a66d-256a83e3b6fb
  Args:
    source: Albrecht_of_Württemberg
    type: :Man
  AssignClass (fef20279-6c9c-4f28-a08b-2f9526b13b59)
 Call ID: fef20279-6c9c-4f28-a08b-2f9526b13b59
  Args:
    type: :Person
    source: Albrecht_of_Württemberg
  AssignClass (ff913970-6a95-433f-852b-18f5d2c6cfe1)
 Call ID: ff913970-6a95-433f-852b-18f5d2c6cfe1
  Args:
    source: Albrecht_of_Württemberg
    type: :Ancestor
  AssignClass (4a6adf46-ecb4-48b3-8665-453b6bae18d4)
 Call ID: 4a6adf46-ecb4-48b3-8665-453b6bae18d4
  Args:
    type: :Woman
    source: Margarete_Sophie_of_Austria
  AssignClass (25ec4f84-e77c-44e2-8682-a98fe438c5bc)
 Call ID: 25ec4f84-e77c-44e2-8682-a98fe438c5bc
  Args:
    source: Margarete_Sophie_of_Austria
    type: :Person
  AssignClass (398a7a25-dcd2-4672-913f-43b2230643e2)
 Call ID: 398a7a25-dcd2-4672-913f-43b2230643e2
  Args:
    type: :Ancestor
    source: Margarete_Sophie_of_Austria
  AddTriple (ff5fa8c9-d902-4410-a5a0-d7d6a3251e65)
 Call ID: ff5fa8c9-d902-4410-a5a0-d7d6a3251e65
  Args:
    target: Albrecht_of_Württemberg
    source: Philipp_Albrecht_of_Württemberg
    relation: :hasFather
  AddTriple (1eca824a-9935-4321-842b-8bac960dd2d6)
 Call ID: 1eca824a-9935-4321-842b-8bac960dd2d6
  Args:
    target: Margarete_Sophie_of_Austria
    source: Philipp_Albrecht_of_Württemberg
    relation: :hasMother
  AssignClass (04aca6d2-2ab0-4baa-997d-c1b10555eded)
 Call ID: 04aca6d2-2ab0-4baa-997d-c1b10555eded
  Args:
    type: :Woman
    source: Maria_Christina_of_Württemberg
  AssignClass (b6d8a5bb-a727-4aa5-a323-8f7e67e5137d)
 Call ID: b6d8a5bb-a727-4aa5-a323-8f7e67e5137d
  Args:
    source: Maria_Christina_of_Württemberg
    type: :Person
  AddTriple (6fac8ccc-c364-43c1-87ae-8fe7b759eba2)
 Call ID: 6fac8ccc-c364-43c1-87ae-8fe7b759eba2
  Args:
    target: Helena_of_Austria
    source: Maria_Christina_of_Württemberg
    relation: :hasMother
  AddTriple (367c9c12-6ee9-4556-9247-338764384682)
 Call ID: 367c9c12-6ee9-4556-9247-338764384682
  Args:
    relation: :hasFather
    target: Philipp_Albrecht_of_Württemberg
    source: Maria_Christina_of_Württemberg
  AssignClass (eb4a499b-ab3e-4b37-ac28-1514e36cc2b1)
 Call ID: eb4a499b-ab3e-4b37-ac28-1514e36cc2b1
  Args:
    source: Rosa_of_Austria
    type: :Woman
  AssignClass (56d50214-1cfe-447c-ad3d-50d9b5b042d9)
 Call ID: 56d50214-1cfe-447c-ad3d-50d9b5b042d9
  Args:
    source: Rosa_of_Austria
    type: :Person
  AddTriple (2dfab03a-5003-45f4-9524-1851e0326696)
 Call ID: 2dfab03a-5003-45f4-9524-1851e0326696
  Args:
    target: Helena_of_Austria
    source: Rosa_of_Austria
    relation: :isSisterOf
  AddTriple (f1733c60-b761-4fa1-9715-d58a5ae38e65)
 Call ID: f1733c60-b761-4fa1-9715-d58a5ae38e65
  Args:
    relation: :hasRelation
    source: Philipp_Albrecht_of_Württemberg
    target: Rosa_of_Austria
  AddLiteral (4827d1b0-aaa7-4630-9c3f-a92e7a0af220)
 Call ID: 4827d1b0-aaa7-4630-9c3f-a92e7a0af220
  Args:
    literal_value: 1928
    source: Rosa_of_Austria
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (664deb79-943c-4790-ae8f-a81ad362d3cf)
 Call ID: 664deb79-943c-4790-ae8f-a81ad362d3cf
  Args: