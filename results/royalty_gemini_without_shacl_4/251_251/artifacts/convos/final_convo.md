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
Captain George Louis Victor Henry Serge Mountbatten, 2nd Marquess of Milford Haven (6 November 1892 – 8 April 1938), born Prince George of Battenberg, styled Earl of Medina between 1917 and 1921, was a Royal Navy officer and the elder son of Louis Mountbatten, 1st Marquess of Milford Haven (Prince Louis of Battenberg), and Princess Victoria of Hesse and by Rhine.
Biography

George was born 6 November 1892 in Darmstadt in the Grand Duchy of Hesse, then ruled by his maternal uncle Ernest Louis, Grand Duke of Hesse.
From birth, he was a prince of the Hessian royal family, albeit of a morganatic branch.
His siblings were Princess Alice (mother of Prince Philip, Duke of Edinburgh, to whom he was a mentor in Philip's adolescence), Queen Louise of Sweden and Louis Mountbatten, 1st
Earl Mountbatten of Burma (who assumed the role of Philip's mentor after George's death).
George followed his father into the Royal Navy, and after passing out from the Royal Naval College at Dartmouth, was promoted to sub-lieutenant on 15 January 1913.
In 1917, his father and several of his relations relinquished their German names, styles and titles in exchange for British peerages at the behest of George V. Accordingly, Prince George dropped the style of Serene Highness and his surname was anglicised to "Mountbatten."
When his father was created Marquess of Milford Haven in late 1917, George received the courtesy title of Earl of Medina, succeeding to his father's peerage after his death in September 1921.
Lord Milford Haven, as George was now known, remained in the Royal Navy after the war; he was promoted to lieutenant-commander on 15 February 1922 and to commander on 31 December 1926.
An accomplished mathematician, the Marquess "could work out complicated gunnery problems in his head" and "read books on calculus casually on trains".
Marriage and issue

Prince George of Battenberg, as he then was known, married Countess Nadejda Mikhailovna de Torby (daughter of Russian Grand Duke Michael Mikhailovich Romanov and his morganatic wife, Countess Sophie von Merenberg) on 15 November 1916 at the Russian Embassy, Welbeck Street, London.
They lived at Lynden Manor at Holyport in Berkshire and had two children:


Death

Lord Milford Haven died in London on 8 April 1938 of bone marrow cancer, aged 45.
His funeral took place at St Michael's Church, Bray, Berkshire, and he was buried in Bray Parish Cemetery.
Legacy to the British Museum

Lord Milford Haven left a collection of pornography, including artificial sex organs, to the British Museum.



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
  AssignClass (987de109-83d7-4b1b-8288-7467683a495b)
 Call ID: 987de109-83d7-4b1b-8288-7467683a495b
  Args:
    type: :Man
    source: George_Mountbatten
  AssignClass (d50a50ec-0bce-40c1-82bb-26e96b5f0208)
 Call ID: d50a50ec-0bce-40c1-82bb-26e96b5f0208
  Args:
    type: :Person
    source: George_Mountbatten
  AddLiteral (02256fcd-c130-4d57-a37f-f0fad3536dc7)
 Call ID: 02256fcd-c130-4d57-a37f-f0fad3536dc7
  Args:
    literal_type: xsd:integer
    source: George_Mountbatten
    relation: :hasBirthYear
    literal_value: 1892
  AddLiteral (e4d4df9b-cf48-42c2-97e3-0ca8d29b1a42)
 Call ID: e4d4df9b-cf48-42c2-97e3-0ca8d29b1a42
  Args:
    relation: :hasDeathYear
    literal_value: 1938
    literal_type: xsd:integer
    source: George_Mountbatten
  AssignClass (a57fe8ad-01f0-4f26-a9b6-79809caec9d9)
 Call ID: a57fe8ad-01f0-4f26-a9b6-79809caec9d9
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Marquess
  AssignClass (fdcd1eb4-874b-45a3-b333-b01627f077f3)
 Call ID: fdcd1eb4-874b-45a3-b333-b01627f077f3
  Args:
    source: Louis_Mountbatten_1st_Marquess
    type: :Person
  AssignClass (bb6eeb92-8c64-4bbc-9062-1a9b556d2de2)
 Call ID: bb6eeb92-8c64-4bbc-9062-1a9b556d2de2
  Args:
    source: Princess_Victoria_of_Hesse
    type: :Woman
  AssignClass (d25622ca-1775-4041-910c-49dfee899e86)
 Call ID: d25622ca-1775-4041-910c-49dfee899e86
  Args:
    type: :Person
    source: Princess_Victoria_of_Hesse
  AddTriple (dd0fb25f-fa53-496c-ba44-bd061eab8328)
 Call ID: dd0fb25f-fa53-496c-ba44-bd061eab8328
  Args:
    source: George_Mountbatten
    target: Louis_Mountbatten_1st_Marquess
    relation: :hasFather
  AddTriple (3233216b-1440-46ac-840a-d29cba4ecde0)
 Call ID: 3233216b-1440-46ac-840a-d29cba4ecde0
  Args:
    relation: :hasMother
    source: George_Mountbatten
    target: Princess_Victoria_of_Hesse
  AssignClass (5e09590f-a2fd-40b3-a228-402e52eef254)
 Call ID: 5e09590f-a2fd-40b3-a228-402e52eef254
  Args:
    source: Princess_Alice
    type: :Woman
  AssignClass (d6cfa7d6-70e1-4777-b3b8-5313f9be5a5d)
 Call ID: d6cfa7d6-70e1-4777-b3b8-5313f9be5a5d
  Args:
    type: :Person
    source: Princess_Alice
  AssignClass (30f031b2-53e6-40f8-8961-7b0a9b530dea)
 Call ID: 30f031b2-53e6-40f8-8961-7b0a9b530dea
  Args:
    type: :Woman
    source: Queen_Louise_of_Sweden
  AssignClass (af365a2b-275e-47b0-ade4-913bf26708b6)
 Call ID: af365a2b-275e-47b0-ade4-913bf26708b6
  Args:
    type: :Person
    source: Queen_Louise_of_Sweden
  AssignClass (5f3950e7-751f-4b4f-9839-1be9a0ab2757)
 Call ID: 5f3950e7-751f-4b4f-9839-1be9a0ab2757
  Args:
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
    type: :Man
  AssignClass (16f21876-6f23-4195-8f18-1b705665ca6b)
 Call ID: 16f21876-6f23-4195-8f18-1b705665ca6b
  Args:
    type: :Person
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AddTriple (56aa6c83-23c7-4181-b272-e435124e0765)
 Call ID: 56aa6c83-23c7-4181-b272-e435124e0765
  Args:
    target: Princess_Alice
    source: George_Mountbatten
    relation: :hasSister
  AddTriple (47ecbd69-bcb3-45ba-b094-4de7f4cbe4c7)
 Call ID: 47ecbd69-bcb3-45ba-b094-4de7f4cbe4c7
  Args:
    relation: :hasSister
    source: George_Mountbatten
    target: Queen_Louise_of_Sweden
  AddTriple (71196e1c-f134-4241-877c-9a311e01bf8f)
 Call ID: 71196e1c-f134-4241-877c-9a311e01bf8f
  Args:
    relation: :hasBrother
    source: George_Mountbatten
    target: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AssignClass (2d66addb-d4b7-44c2-b7cb-9151c05b3b9c)
 Call ID: 2d66addb-d4b7-44c2-b7cb-9151c05b3b9c
  Args:
    source: Nadejda_Mikhailovna_de_Torby
    type: :Woman
  AssignClass (6323dc62-acca-4f99-a988-5256fc71d8a5)
 Call ID: 6323dc62-acca-4f99-a988-5256fc71d8a5
  Args:
    source: Nadejda_Mikhailovna_de_Torby
    type: :Person
  AddLiteral (20912378-e14c-4fb7-9b1d-d70e25bc12be)
 Call ID: 20912378-e14c-4fb7-9b1d-d70e25bc12be
  Args:
    literal_value: 1916
    relation: :hasMarriageYear
    source: George_Mountbatten
    literal_type: xsd:integer
  AddTriple (60f961f9-c693-4063-9982-6e2d117655db)
 Call ID: 60f961f9-c693-4063-9982-6e2d117655db
  Args:
    relation: :hasRelation
    source: George_Mountbatten
    target: Nadejda_Mikhailovna_de_Torby
  AssignClass (e99583d4-26a4-4e3d-bb17-3ff31971ffca)
 Call ID: e99583d4-26a4-4e3d-bb17-3ff31971ffca
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (f389a8b1-4a11-441a-87a0-e00d17b036cc)
 Call ID: f389a8b1-4a11-441a-87a0-e00d17b036cc
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (c58cdc11-6a85-4c6f-898d-48ca1fd7c671)
 Call ID: c58cdc11-6a85-4c6f-898d-48ca1fd7c671
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    target: Princess_Alice
    relation: :hasMother
  AssignClass (dbf32b33-6bd6-4d40-8386-7bbc5bbb59d7)
 Call ID: dbf32b33-6bd6-4d40-8386-7bbc5bbb59d7
  Args:
    type: :Man
    source: Grand_Duke_Michael_Mikhailovich_Romanov
  AssignClass (4f35ba82-b354-479b-aa8d-ceeca24a38d3)
 Call ID: 4f35ba82-b354-479b-aa8d-ceeca24a38d3
  Args:
    type: :Person
    source: Grand_Duke_Michael_Mikhailovich_Romanov
  AssignClass (9698d362-fab3-42c2-a5ca-0cb4b2a7abd2)
 Call ID: 9698d362-fab3-42c2-a5ca-0cb4b2a7abd2
  Args:
    type: :Woman
    source: Countess_Sophie_von_Merenberg
  AssignClass (fd4f2368-817b-484d-8708-60f27738f93d)
 Call ID: fd4f2368-817b-484d-8708-60f27738f93d
  Args:
    source: Countess_Sophie_von_Merenberg
    type: :Person
  AddTriple (4a2579f6-ea1b-4784-a53f-0abf2b602aa5)
 Call ID: 4a2579f6-ea1b-4784-a53f-0abf2b602aa5
  Args:
    relation: :hasFather
    source: Nadejda_Mikhailovna_de_Torby
    target: Grand_Duke_Michael_Mikhailovich_Romanov
  AddTriple (dbcfa1a1-8f76-4b0b-835d-48d2fae249d0)
 Call ID: dbcfa1a1-8f76-4b0b-835d-48d2fae249d0
  Args:
    relation: :hasMother
    target: Countess_Sophie_von_Merenberg
    source: Nadejda_Mikhailovna_de_Torby
  AssignClass (0297cc37-5582-44b4-9f55-465a235fb850)
 Call ID: 0297cc37-5582-44b4-9f55-465a235fb850
  Args:
    source: Ernest_Louis_Grand_Duke_of_Hesse
    type: :Man
  AssignClass (f5151b66-c17a-4dc4-8a30-51cca4053981)
 Call ID: f5151b66-c17a-4dc4-8a30-51cca4053981
  Args:
    source: Ernest_Louis_Grand_Duke_of_Hesse
    type: :Person
  AddTriple (63186abe-eaff-48fe-b2ca-70a9c2c62e71)
 Call ID: 63186abe-eaff-48fe-b2ca-70a9c2c62e71
  Args:
    relation: :hasRelation
    target: Ernest_Louis_Grand_Duke_of_Hesse
    source: Princess_Victoria_of_Hesse
  Finish (8654e54b-c1d1-4988-965f-fbcc53b0ff3a)
 Call ID: 8654e54b-c1d1-4988-965f-fbcc53b0ff3a
  Args: