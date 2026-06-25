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
King Albert IIQueen Paola


Princess Astrid of Belgium, Archduchess of Austria-Este (born 5 June 1962), is the second child and first daughter of King Albert II and Queen Paola, and the younger sister to the current Belgian monarch, King Philippe.
She is married to Prince Lorenz of Belgium, head of the Austria-Este branch of the House of Habsburg-Lorraine, and is fifth in line of succession to the Belgian throne.
Biography

Princess Astrid was born one day before her father's 28th birthday at the Belvédère Château in Laeken, northern Brussels, and was named after her late paternal grandmother, Astrid of Sweden, King Leopold III's popular first wife, who had died in 1935 in a car accident aged 29.
Princess Astrid's godparents were her uncle Fabrizio, Prince Ruffo di Calabria-Santapau, 7th Duke di Guardia Lombarda, and her aunt Hereditary Grand Duchess Joséphine-Charlotte of Luxembourg.
Marriage and issue

Princess Astrid married Archduke Lorenz of Austria-Este, subsequently head of the House of Austria-Este, on 22 September 1984 at the Church of Our Lady of Victories at the Sablon in Brussels.
Lorenz is the eldest son of Robert, Archduke of Austria-Este (1915–1996) and Princess Margherita of Savoy-Aosta (1930–2022).
Princess Astrid and Prince Lorenz have five children:


Royal role

Astrid was formerly President of the Belgian Red Cross, a position which ended on 31 December 2007.
The princess is also a colonel in the Belgian Medical Service of the Belgian Armed Forces.
In April 2015, the Princess took over the Prince Albert Fund from her father King Albert.
Special Envoy

Princess Astrid has been for many years an advocate for landmine survivors rights, participating actively in the work of the Anti-Personnel Mine Ban Convention, also known as the Ottawa Treaty, since Belgium joined in 1998.
In 2013, the Princess was named Special Envoy of the convention, and has promoted the acceptance of a global ban on landmines and promoted the rights of survivors in various UN meetings.



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
  AssignClass (817c9558-5e6e-45e7-9777-c1c2f0931c7f)
 Call ID: 817c9558-5e6e-45e7-9777-c1c2f0931c7f
  Args:
    source: :King_Albert_II
    type: :Man
  AssignClass (f6832c9b-2e5f-4f97-86cf-8c0b5fc82afa)
 Call ID: f6832c9b-2e5f-4f97-86cf-8c0b5fc82afa
  Args:
    type: :Person
    source: :King_Albert_II
  AssignClass (2a970134-9dd1-48f5-ad6f-8ace2e2aac21)
 Call ID: 2a970134-9dd1-48f5-ad6f-8ace2e2aac21
  Args:
    source: :Queen_Paola
    type: :Woman
  AssignClass (fed24601-f134-4601-8c41-61161f591567)
 Call ID: fed24601-f134-4601-8c41-61161f591567
  Args:
    type: :Person
    source: :Queen_Paola
  AssignClass (008c1a8b-2a80-4f6f-acdc-5b2dd3e42bfe)
 Call ID: 008c1a8b-2a80-4f6f-acdc-5b2dd3e42bfe
  Args:
    type: :Woman
    source: :Princess_Astrid_of_Belgium
  AssignClass (3e99bdd3-50a3-41c1-8edf-080aaf31d47b)
 Call ID: 3e99bdd3-50a3-41c1-8edf-080aaf31d47b
  Args:
    type: :Person
    source: :Princess_Astrid_of_Belgium
  AssignClass (cfc144d1-5b5f-4fb6-b787-bbfb5007593d)
 Call ID: cfc144d1-5b5f-4fb6-b787-bbfb5007593d
  Args:
    source: :King_Philippe
    type: :Man
  AssignClass (92d582cf-13c5-4927-8515-13429aed4422)
 Call ID: 92d582cf-13c5-4927-8515-13429aed4422
  Args:
    type: :Person
    source: :King_Philippe
  AssignClass (35ca93d6-ddb1-4cb5-b22e-7a8a01012e0d)
 Call ID: 35ca93d6-ddb1-4cb5-b22e-7a8a01012e0d
  Args:
    source: :Prince_Lorenz_of_Belgium
    type: :Man
  AssignClass (42c35d80-5abf-4ca2-8fd3-e230d36d7636)
 Call ID: 42c35d80-5abf-4ca2-8fd3-e230d36d7636
  Args:
    source: :Prince_Lorenz_of_Belgium
    type: :Person
  AssignClass (e225a90d-5294-4553-91dc-089318e43bc4)
 Call ID: e225a90d-5294-4553-91dc-089318e43bc4
  Args:
    type: :Woman
    source: :Astrid_of_Sweden
  AssignClass (2a01f8e9-4c5d-4092-8bbc-7edbea0a4d47)
 Call ID: 2a01f8e9-4c5d-4092-8bbc-7edbea0a4d47
  Args:
    type: :Person
    source: :Astrid_of_Sweden
  AssignClass (1e7c12fb-a85e-4454-b39d-9a290466ab39)
 Call ID: 1e7c12fb-a85e-4454-b39d-9a290466ab39
  Args:
    type: :Man
    source: :King_Leopold_III
  AssignClass (e986b906-d242-4b38-b7d5-dd2cebef8fad)
 Call ID: e986b906-d242-4b38-b7d5-dd2cebef8fad
  Args:
    source: :King_Leopold_III
    type: :Person
  AssignClass (6c5315dc-450e-49cd-9b01-db875b1ed84e)
 Call ID: 6c5315dc-450e-49cd-9b01-db875b1ed84e
  Args:
    type: :Man
    source: :Fabrizio_Prince_Ruffo_di_Calabria_Santapau
  AssignClass (5e5fea27-445a-406c-8283-eca8d0c08558)
 Call ID: 5e5fea27-445a-406c-8283-eca8d0c08558
  Args:
    source: :Fabrizio_Prince_Ruffo_di_Calabria_Santapau
    type: :Person
  AssignClass (9b8d8274-72a1-4cef-a931-f953cb4cb577)
 Call ID: 9b8d8274-72a1-4cef-a931-f953cb4cb577
  Args:
    type: :Woman
    source: :Joséphine_Charlotte_of_Luxembourg
  AssignClass (a02453f0-222a-46e6-aaa8-07c46f751566)
 Call ID: a02453f0-222a-46e6-aaa8-07c46f751566
  Args:
    source: :Joséphine_Charlotte_of_Luxembourg
    type: :Person
  AssignClass (3256b000-87c1-4145-b0c0-77974c6d4d9e)
 Call ID: 3256b000-87c1-4145-b0c0-77974c6d4d9e
  Args:
    type: :Man
    source: :Robert_Archduke_of_Austria_Este
  AssignClass (5cda96bc-ee0b-414e-8e0c-2a7a797f6895)
 Call ID: 5cda96bc-ee0b-414e-8e0c-2a7a797f6895
  Args:
    type: :Person
    source: :Robert_Archduke_of_Austria_Este
  AssignClass (d87789f1-7872-4e00-8f03-a92f703b2c6f)
 Call ID: d87789f1-7872-4e00-8f03-a92f703b2c6f
  Args:
    source: :Princess_Margherita_of_Savoy_Aosta
    type: :Woman
  AssignClass (639ab7be-5589-4328-9ba1-09e771d7b279)
 Call ID: 639ab7be-5589-4328-9ba1-09e771d7b279
  Args:
    type: :Person
    source: :Princess_Margherita_of_Savoy_Aosta
  AddTriple (b5f062ff-1f25-47eb-b04e-14971b568766)
 Call ID: b5f062ff-1f25-47eb-b04e-14971b568766
  Args:
    relation: :hasFather
    target: :King_Albert_II
    source: :Princess_Astrid_of_Belgium
  AddTriple (4ed64dc1-332d-49e8-9da9-894b300f6b5c)
 Call ID: 4ed64dc1-332d-49e8-9da9-894b300f6b5c
  Args:
    target: :Queen_Paola
    source: :Princess_Astrid_of_Belgium
    relation: :hasMother
  AddTriple (466d0876-16ac-488e-bc37-6a82f1418a0e)
 Call ID: 466d0876-16ac-488e-bc37-6a82f1418a0e
  Args:
    relation: :isSisterOf
    source: :Princess_Astrid_of_Belgium
    target: :King_Philippe
  AddTriple (73f0531c-1475-4edc-a48c-fd731d0dd33d)
 Call ID: 73f0531c-1475-4edc-a48c-fd731d0dd33d
  Args:
    source: :King_Philippe
    target: :Princess_Astrid_of_Belgium
    relation: :isBrotherOf
  AddLiteral (f54e507f-2ad0-4a2b-a1ed-2d9a0ec4ef58)
 Call ID: f54e507f-2ad0-4a2b-a1ed-2d9a0ec4ef58
  Args:
    source: :Princess_Astrid_of_Belgium
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1962
  AddTriple (4a85a6ae-23f9-4dd7-bcb7-e75089866beb)
 Call ID: 4a85a6ae-23f9-4dd7-bcb7-e75089866beb
  Args:
    relation: :hasFather
    source: :Prince_Lorenz_of_Belgium
    target: :Robert_Archduke_of_Austria_Este
  AddTriple (91a5d4fa-db5b-4fb5-9669-207c1b4b28ac)
 Call ID: 91a5d4fa-db5b-4fb5-9669-207c1b4b28ac
  Args:
    relation: :hasMother
    source: :Prince_Lorenz_of_Belgium
    target: :Princess_Margherita_of_Savoy_Aosta
  AddLiteral (d7fc71e1-bed5-4187-801e-f438f008b08c)
 Call ID: d7fc71e1-bed5-4187-801e-f438f008b08c
  Args:
    literal_value: 1984
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: :Princess_Astrid_of_Belgium
  AddTriple (fbcfee94-7c07-47d5-9efd-fa7fe670eb93)
 Call ID: fbcfee94-7c07-47d5-9efd-fa7fe670eb93
  Args:
    source: :Princess_Astrid_of_Belgium
    target: :Prince_Lorenz_of_Belgium
    relation: :hasRelation
  AddTriple (55436c33-77ed-4f8b-8f0c-fbe59fd580c0)
 Call ID: 55436c33-77ed-4f8b-8f0c-fbe59fd580c0
  Args:
    relation: :hasFather
    source: :King_Albert_II
    target: :King_Leopold_III
  AddTriple (f7b2a5fe-c031-4961-b95c-4ca13e57dfc2)
 Call ID: f7b2a5fe-c031-4961-b95c-4ca13e57dfc2
  Args:
    source: :King_Albert_II
    target: :Astrid_of_Sweden
    relation: :hasMother
  AddLiteral (5d443db6-497c-4952-bdc9-b52b3b0c755e)
 Call ID: 5d443db6-497c-4952-bdc9-b52b3b0c755e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1935
    source: :Astrid_of_Sweden
  AddLiteral (781e8c71-2537-4844-8669-eb3de9571655)
 Call ID: 781e8c71-2537-4844-8669-eb3de9571655
  Args:
    literal_value: 1996
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Robert_Archduke_of_Austria_Este
  AddLiteral (69a0e93c-059e-419b-8f9f-8e35e9e2224c)
 Call ID: 69a0e93c-059e-419b-8f9f-8e35e9e2224c
  Args:
    literal_value: 2022
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Princess_Margherita_of_Savoy_Aosta
  Finish (0ef27f41-7f18-4bb5-80fe-40b544db4a50)
 Call ID: 0ef27f41-7f18-4bb5-80fe-40b544db4a50
  Args: