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
Princess Alexandrine Irene of Prussia (7 April 1915 – 2 October 1980) was the elder daughter and fifth child of Wilhelm, German Crown Prince, and Cecilie of Mecklenburg-Schwerin.
Her grandparents were Wilhelm II, German Emperor and his wife Augusta Victoria of Schleswig-Holstein, and Frederick Francis III of Mecklenburg-Schwerin and Grand Duchess Anastasia Mikhailovna of Russia.
Alexandrine was a member of the House of Hohenzollern.
She was a great-great-granddaughter of Queen Victoria.
Life

Alexandrine was born at the Kronprinzenpalais in Berlin.
She followed older brothers Wilhelm, Louis Ferdinand, Hubertus, and Frederick.
Alexandrine's only sister, Cecilie, was born in 1917.
It became clear shortly after Alexandrine's birth that she had Down syndrome.
Unlike other disabled royal children, Alexandrine was not hidden away.
As a teenager, Alexandrine attended the Trüpersche Sonderschule, a school dedicated to the education of children with special needs.
Alexandrine celebrated her confirmation along with her sister Cecilie in October 1934.
Alexandrine lived most of her later life in Bavaria, first in Pöcking and later near Lake Starnberg, where she was visited there regularly by her family, particularly her brother Louis Ferdinand.
Alexandrine died on 2 October 1980.
She was buried near her parents and brother Frederick at Hohenzollern Castle.



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
  AssignClass (4f9bcd25-87b6-4985-9ef7-06d360bbbcf9)
 Call ID: 4f9bcd25-87b6-4985-9ef7-06d360bbbcf9
  Args:
    source: :Alexandrine_Irene_of_Prussia
    type: :Woman
  AssignClass (c7027d2f-1a41-4d6d-bee1-5ea4390a3805)
 Call ID: c7027d2f-1a41-4d6d-bee1-5ea4390a3805
  Args:
    source: :Alexandrine_Irene_of_Prussia
    type: :Person
  AddLiteral (b528e2b9-813f-4a31-b1a9-8c8ae9045a9c)
 Call ID: b528e2b9-813f-4a31-b1a9-8c8ae9045a9c
  Args:
    literal_type: xsd:integer
    source: :Alexandrine_Irene_of_Prussia
    relation: :hasBirthYear
    literal_value: 1915
  AddLiteral (2db54567-4ec7-45ea-bf48-99c3299fe142)
 Call ID: 2db54567-4ec7-45ea-bf48-99c3299fe142
  Args:
    literal_type: xsd:integer
    source: :Alexandrine_Irene_of_Prussia
    literal_value: 1980
    relation: :hasDeathYear
  AssignClass (78cde456-dd12-4a20-91af-860511aea37c)
 Call ID: 78cde456-dd12-4a20-91af-860511aea37c
  Args:
    source: :Wilhelm_German_Crown_Prince
    type: :Man
  AssignClass (af688a81-5243-4dd8-b874-0bfa434779ff)
 Call ID: af688a81-5243-4dd8-b874-0bfa434779ff
  Args:
    source: :Wilhelm_German_Crown_Prince
    type: :Ancestor
  AssignClass (85cce661-fdcb-47a5-bb55-d40fc1e433f5)
 Call ID: 85cce661-fdcb-47a5-bb55-d40fc1e433f5
  Args:
    source: :Cecilie_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (570dfb69-aaf7-4ed8-8049-3ee0f7648695)
 Call ID: 570dfb69-aaf7-4ed8-8049-3ee0f7648695
  Args:
    source: :Cecilie_of_Mecklenburg-Schwerin
    type: :Ancestor
  AddTriple (7715d273-6b48-4b72-83dd-a9c8fb14b35a)
 Call ID: 7715d273-6b48-4b72-83dd-a9c8fb14b35a
  Args:
    target: :Wilhelm_German_Crown_Prince
    source: :Alexandrine_Irene_of_Prussia
    relation: :hasFather
  AddTriple (948b86f0-cbea-4b3e-ada1-430e2a9ca9e2)
 Call ID: 948b86f0-cbea-4b3e-ada1-430e2a9ca9e2
  Args:
    target: :Cecilie_of_Mecklenburg-Schwerin
    source: :Alexandrine_Irene_of_Prussia
    relation: :hasMother
  AssignClass (e7bdd764-363f-421a-80e1-b5f8161203c6)
 Call ID: e7bdd764-363f-421a-80e1-b5f8161203c6
  Args:
    source: :Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (d4c2a299-d6c8-4dd9-8139-d5367c85b3d2)
 Call ID: d4c2a299-d6c8-4dd9-8139-d5367c85b3d2
  Args:
    source: :Wilhelm_II_German_Emperor
    type: :Ancestor
  AssignClass (aa54a5f4-3751-4d91-8e9d-b54990f0ec37)
 Call ID: aa54a5f4-3751-4d91-8e9d-b54990f0ec37
  Args:
    source: :Augusta_Victoria_of_Schleswig-Holstein
    type: :Woman
  AssignClass (fec1041c-0519-41b2-a935-44689046de00)
 Call ID: fec1041c-0519-41b2-a935-44689046de00
  Args:
    source: :Augusta_Victoria_of_Schleswig-Holstein
    type: :Ancestor
  AssignClass (971a5374-3a5a-4e2b-ae3f-8c0e16ee6331)
 Call ID: 971a5374-3a5a-4e2b-ae3f-8c0e16ee6331
  Args:
    source: :Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (cd4f6905-4447-460d-b0ca-781ca44a135c)
 Call ID: cd4f6905-4447-460d-b0ca-781ca44a135c
  Args:
    source: :Frederick_Francis_III_of_Mecklenburg-Schwerin
    type: :Ancestor
  AssignClass (39ba5e4e-daf4-4261-b7e8-d54d7b75e1c2)
 Call ID: 39ba5e4e-daf4-4261-b7e8-d54d7b75e1c2
  Args:
    source: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    type: :Woman
  AssignClass (83cfc9d8-c89d-4293-90e9-9da8345fae13)
 Call ID: 83cfc9d8-c89d-4293-90e9-9da8345fae13
  Args:
    source: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
    type: :Ancestor
  AddTriple (7ef36956-7f13-4f6e-b138-5c949589055f)
 Call ID: 7ef36956-7f13-4f6e-b138-5c949589055f
  Args:
    relation: :hasFather
    source: :Wilhelm_German_Crown_Prince
    target: :Wilhelm_II_German_Emperor
  AddTriple (73558eb5-5b90-4504-bf04-cfe1be57383e)
 Call ID: 73558eb5-5b90-4504-bf04-cfe1be57383e
  Args:
    relation: :hasMother
    source: :Wilhelm_German_Crown_Prince
    target: :Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (4335c654-0a60-432f-9fda-66a81038c157)
 Call ID: 4335c654-0a60-432f-9fda-66a81038c157
  Args:
    source: :Cecilie_of_Mecklenburg-Schwerin
    relation: :hasFather
    target: :Frederick_Francis_III_of_Mecklenburg-Schwerin
  AddTriple (5d97d357-c996-44a0-a3d4-90261263b701)
 Call ID: 5d97d357-c996-44a0-a3d4-90261263b701
  Args:
    relation: :hasMother
    source: :Cecilie_of_Mecklenburg-Schwerin
    target: :Grand_Duchess_Anastasia_Mikhailovna_of_Russia
  AssignClass (d9e05895-9021-489a-b3d6-d8b2d5de35fd)
 Call ID: d9e05895-9021-489a-b3d6-d8b2d5de35fd
  Args:
    source: :Wilhelm_brother
    type: :Man
  AssignClass (6ea215b7-df3e-405b-9c31-db2f9fe394cf)
 Call ID: 6ea215b7-df3e-405b-9c31-db2f9fe394cf
  Args:
    source: :Wilhelm_brother
    type: :Person
  AssignClass (9fc786c3-6306-45dd-9512-a2ebfdd3b12a)
 Call ID: 9fc786c3-6306-45dd-9512-a2ebfdd3b12a
  Args:
    source: :Louis_Ferdinand
    type: :Man
  AssignClass (47a7f1bd-2425-427c-a538-76cf5c7832cd)
 Call ID: 47a7f1bd-2425-427c-a538-76cf5c7832cd
  Args:
    source: :Louis_Ferdinand
    type: :Person
  AssignClass (c3a3fc21-103e-4955-9a47-75045fbaec74)
 Call ID: c3a3fc21-103e-4955-9a47-75045fbaec74
  Args:
    source: :Hubertus
    type: :Man
  AssignClass (e926ab37-35b8-421d-badf-e6ef2530eb1a)
 Call ID: e926ab37-35b8-421d-badf-e6ef2530eb1a
  Args:
    source: :Hubertus
    type: :Person
  AssignClass (1a63bd56-f8c9-4e67-bbab-1f7bd2d9426e)
 Call ID: 1a63bd56-f8c9-4e67-bbab-1f7bd2d9426e
  Args:
    source: :Frederick_brother
    type: :Man
  AssignClass (8670bf46-6141-4faa-825a-37be9eaea94d)
 Call ID: 8670bf46-6141-4faa-825a-37be9eaea94d
  Args:
    source: :Frederick_brother
    type: :Person
  AssignClass (548a5f4c-7d72-4e8a-b33b-6af4fc8da820)
 Call ID: 548a5f4c-7d72-4e8a-b33b-6af4fc8da820
  Args:
    source: :Cecilie_sister
    type: :Woman
  AssignClass (ece3b719-6955-49a5-9c02-11e638639f36)
 Call ID: ece3b719-6955-49a5-9c02-11e638639f36
  Args:
    source: :Cecilie_sister
    type: :Person
  AddTriple (ce445554-3231-4715-96b6-0729543680bc)
 Call ID: ce445554-3231-4715-96b6-0729543680bc
  Args:
    target: :Wilhelm_brother
    source: :Alexandrine_Irene_of_Prussia
    relation: :isSiblingOf
  AddTriple (3b1cd9d5-96e1-48fc-b12d-d6ea55dc1f89)
 Call ID: 3b1cd9d5-96e1-48fc-b12d-d6ea55dc1f89
  Args:
    relation: :isSiblingOf
    source: :Alexandrine_Irene_of_Prussia
    target: :Louis_Ferdinand
  AddTriple (22d035d7-9fe6-4c72-bbc5-c23f6ce2cd90)
 Call ID: 22d035d7-9fe6-4c72-bbc5-c23f6ce2cd90
  Args:
    relation: :isSiblingOf
    source: :Alexandrine_Irene_of_Prussia
    target: :Hubertus
  AddTriple (73b768f3-94a5-42bd-a504-98e57f0c41b0)
 Call ID: 73b768f3-94a5-42bd-a504-98e57f0c41b0
  Args:
    target: :Frederick_brother
    relation: :isSiblingOf
    source: :Alexandrine_Irene_of_Prussia
  AddTriple (47a1e3b9-21e4-475e-9e54-3f29a0a1b69d)
 Call ID: 47a1e3b9-21e4-475e-9e54-3f29a0a1b69d
  Args:
    source: :Alexandrine_Irene_of_Prussia
    relation: :isSiblingOf
    target: :Cecilie_sister
  Finish (64232360-716d-4d4b-8416-37782e299c78)
 Call ID: 64232360-716d-4d4b-8416-37782e299c78
  Args: