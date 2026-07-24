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
  AssignClass (b1ae2175-5a34-441c-ba8d-52ec94bab7e1)
 Call ID: b1ae2175-5a34-441c-ba8d-52ec94bab7e1
  Args:
    source: GeorgeMountbatten
    type: :Man
  AssignClass (eb5ff8fe-73d8-4510-9ab8-b0fa7f3ea3f7)
 Call ID: eb5ff8fe-73d8-4510-9ab8-b0fa7f3ea3f7
  Args:
    type: :Person
    source: GeorgeMountbatten
  AddLiteral (9e0f12f5-0e47-4d07-88f2-3089113b344a)
 Call ID: 9e0f12f5-0e47-4d07-88f2-3089113b344a
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1892
    source: GeorgeMountbatten
  AddLiteral (70827746-f842-4788-a7a3-6586a7fdf438)
 Call ID: 70827746-f842-4788-a7a3-6586a7fdf438
  Args:
    source: GeorgeMountbatten
    literal_value: 1938
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (cf706799-9ca9-40be-81bc-728421b5005f)
 Call ID: cf706799-9ca9-40be-81bc-728421b5005f
  Args:
    literal_type: xsd:string
    source: GeorgeMountbatten
    literal_value: GeorgeMountbatten
    relation: :knownAs
  AddLiteral (915c2bf4-5b51-4789-b565-715db11f107e)
 Call ID: 915c2bf4-5b51-4789-b565-715db11f107e
  Args:
    literal_type: xsd:string
    literal_value: Prince George of Battenberg
    source: GeorgeMountbatten
    relation: :formerlyKnownAs
  AddLiteral (9735e2ba-b21e-4539-b5d0-7515e8972908)
 Call ID: 9735e2ba-b21e-4539-b5d0-7515e8972908
  Args:
    source: GeorgeMountbatten
    literal_value: Earl of Medina
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AddLiteral (6c82d614-600f-403a-8c3c-eed54069fb34)
 Call ID: 6c82d614-600f-403a-8c3c-eed54069fb34
  Args:
    literal_type: xsd:string
    source: GeorgeMountbatten
    literal_value: Lord Milford Haven
    relation: :alsoKnownAs
  AssignClass (96fe2c6d-244e-4c15-8253-86fb3262a2a8)
 Call ID: 96fe2c6d-244e-4c15-8253-86fb3262a2a8
  Args:
    type: :Man
    source: LouisMountbatten1stMarquess
  AssignClass (30cbae82-6bea-4160-8292-1a14365c59c8)
 Call ID: 30cbae82-6bea-4160-8292-1a14365c59c8
  Args:
    type: :Person
    source: LouisMountbatten1stMarquess
  AddTriple (de985efd-0fea-49fe-8bb9-89cd3de5958b)
 Call ID: de985efd-0fea-49fe-8bb9-89cd3de5958b
  Args:
    relation: :hasFather
    source: GeorgeMountbatten
    target: LouisMountbatten1stMarquess
  AssignClass (c8c6a29d-3588-4f11-8bc2-2e8b99d7bddb)
 Call ID: c8c6a29d-3588-4f11-8bc2-2e8b99d7bddb
  Args:
    type: :Woman
    source: PrincessVictoriaOfHesse
  AssignClass (1aed1c86-b1a1-41b1-85c5-eb2e1e1d2329)
 Call ID: 1aed1c86-b1a1-41b1-85c5-eb2e1e1d2329
  Args:
    type: :Person
    source: PrincessVictoriaOfHesse
  AddTriple (029bd8be-1bcf-46de-9e23-7703d7b04228)
 Call ID: 029bd8be-1bcf-46de-9e23-7703d7b04228
  Args:
    target: PrincessVictoriaOfHesse
    source: GeorgeMountbatten
    relation: :hasMother
  AssignClass (05dea834-6168-4fd4-8cec-037ba8019989)
 Call ID: 05dea834-6168-4fd4-8cec-037ba8019989
  Args:
    source: PrincessAlice
    type: :Woman
  AssignClass (0298cc88-cace-44a4-b816-35d1b5f5ecf7)
 Call ID: 0298cc88-cace-44a4-b816-35d1b5f5ecf7
  Args:
    source: PrincessAlice
    type: :Person
  AddTriple (cd047775-e351-4c1a-b9e6-a36ff362d2aa)
 Call ID: cd047775-e351-4c1a-b9e6-a36ff362d2aa
  Args:
    relation: :isSiblingOf
    source: GeorgeMountbatten
    target: PrincessAlice
  AssignClass (5bd51800-5cee-42fb-a36b-efb92d9d9bde)
 Call ID: 5bd51800-5cee-42fb-a36b-efb92d9d9bde
  Args:
    type: :Woman
    source: QueenLouiseOfSweden
  AssignClass (0d9d0687-3231-476d-831b-6952f19ef15d)
 Call ID: 0d9d0687-3231-476d-831b-6952f19ef15d
  Args:
    source: QueenLouiseOfSweden
    type: :Person
  AddTriple (263712f7-450f-4569-a08f-ac464928570b)
 Call ID: 263712f7-450f-4569-a08f-ac464928570b
  Args:
    relation: :isSiblingOf
    source: GeorgeMountbatten
    target: QueenLouiseOfSweden
  AssignClass (54223d39-52d5-4af6-9792-8bca31f1a2de)
 Call ID: 54223d39-52d5-4af6-9792-8bca31f1a2de
  Args:
    type: :Man
    source: LouisMountbatten1stEarl
  AssignClass (b444f436-6a23-4be5-b5d1-dd437c8a3a65)
 Call ID: b444f436-6a23-4be5-b5d1-dd437c8a3a65
  Args:
    type: :Person
    source: LouisMountbatten1stEarl
  AddTriple (63c31a7e-4a72-458c-8d0b-602022a81539)
 Call ID: 63c31a7e-4a72-458c-8d0b-602022a81539
  Args:
    source: GeorgeMountbatten
    relation: :isSiblingOf
    target: LouisMountbatten1stEarl
  AssignClass (d88b84aa-cbd4-4ae7-965c-761488e8472d)
 Call ID: d88b84aa-cbd4-4ae7-965c-761488e8472d
  Args:
    source: NadejdaMikhailovnaDeTorby
    type: :Woman
  AssignClass (8b1cb488-3b3d-4b9b-a7cb-ec0a5dd94584)
 Call ID: 8b1cb488-3b3d-4b9b-a7cb-ec0a5dd94584
  Args:
    source: NadejdaMikhailovnaDeTorby
    type: :Person
  AddLiteral (404c7fda-da68-4850-9654-0b6ac149343b)
 Call ID: 404c7fda-da68-4850-9654-0b6ac149343b
  Args:
    relation: :hasMarriageYear
    source: GeorgeMountbatten
    literal_value: 1916
    literal_type: xsd:integer
  AddTriple (efb48cfc-8d7e-4435-8e9e-0fced723069b)
 Call ID: efb48cfc-8d7e-4435-8e9e-0fced723069b
  Args:
    source: GeorgeMountbatten
    relation: :hasRelation
    target: NadejdaMikhailovnaDeTorby
  AssignClass (8366a1bb-74af-4aae-9ea4-6576903011b2)
 Call ID: 8366a1bb-74af-4aae-9ea4-6576903011b2
  Args:
    source: MichaelMikhailovichRomanov
    type: :Man
  AssignClass (8cad8b1a-c3cd-444d-b10e-7cf4d368eb42)
 Call ID: 8cad8b1a-c3cd-444d-b10e-7cf4d368eb42
  Args:
    source: MichaelMikhailovichRomanov
    type: :Person
  AddTriple (ae3b0f87-af15-4610-bdc9-095d68aba1af)
 Call ID: ae3b0f87-af15-4610-bdc9-095d68aba1af
  Args:
    source: NadejdaMikhailovnaDeTorby
    relation: :hasFather
    target: MichaelMikhailovichRomanov
  AssignClass (f6c99ca2-74dc-4d67-b731-d6b18c615a9b)
 Call ID: f6c99ca2-74dc-4d67-b731-d6b18c615a9b
  Args:
    source: SophieVonMerenberg
    type: :Woman
  AssignClass (9160aaeb-62d4-47ca-8d63-6a3fb933ee2d)
 Call ID: 9160aaeb-62d4-47ca-8d63-6a3fb933ee2d
  Args:
    type: :Person
    source: SophieVonMerenberg
  AddTriple (5b56d5be-49df-49ba-b37e-3b7e05f9fa26)
 Call ID: 5b56d5be-49df-49ba-b37e-3b7e05f9fa26
  Args:
    relation: :hasMother
    source: NadejdaMikhailovnaDeTorby
    target: SophieVonMerenberg
  Finish (2f5763f3-c12f-4472-ba36-f7b4f19508d4)
 Call ID: 2f5763f3-c12f-4472-ba36-f7b4f19508d4
  Args: