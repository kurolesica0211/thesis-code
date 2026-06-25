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
  AssignClass (d7e37dee-f35c-42df-bd04-891dcf12bed4)
 Call ID: d7e37dee-f35c-42df-bd04-891dcf12bed4
  Args:
    source: GeorgeMountbatten
    type: :Man
  AssignClass (2a1bbaee-5189-4ac1-b881-d8151114edf7)
 Call ID: 2a1bbaee-5189-4ac1-b881-d8151114edf7
  Args:
    source: GeorgeMountbatten
    type: :Person
  AddLiteral (b06af16d-509f-481e-94b1-db3772908c63)
 Call ID: b06af16d-509f-481e-94b1-db3772908c63
  Args:
    literal_value: 1892
    source: GeorgeMountbatten
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (300d0d5f-d82b-4a7c-80c4-77218d0bda18)
 Call ID: 300d0d5f-d82b-4a7c-80c4-77218d0bda18
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: GeorgeMountbatten
    literal_value: 1938
  AssignClass (49858bda-3c45-4231-a142-ac6660839865)
 Call ID: 49858bda-3c45-4231-a142-ac6660839865
  Args:
    source: LouisMountbatten1stMarquess
    type: :Man
  AssignClass (9c89932b-939a-45b7-ba11-baecb3dc5f0a)
 Call ID: 9c89932b-939a-45b7-ba11-baecb3dc5f0a
  Args:
    source: LouisMountbatten1stMarquess
    type: :Person
  AssignClass (27c61463-0dcf-451c-8a4d-d578e30f5d67)
 Call ID: 27c61463-0dcf-451c-8a4d-d578e30f5d67
  Args:
    source: VictoriaOfHesse
    type: :Woman
  AssignClass (f4bee4c2-2948-4622-adfd-b8bd43ea51ee)
 Call ID: f4bee4c2-2948-4622-adfd-b8bd43ea51ee
  Args:
    source: VictoriaOfHesse
    type: :Person
  AddTriple (a3e1c3a5-9096-4398-9c2b-3d96d4e89d8d)
 Call ID: a3e1c3a5-9096-4398-9c2b-3d96d4e89d8d
  Args:
    relation: :hasFather
    source: GeorgeMountbatten
    target: LouisMountbatten1stMarquess
  AddTriple (2fa5230d-ff52-4c97-9eea-18df0dd625de)
 Call ID: 2fa5230d-ff52-4c97-9eea-18df0dd625de
  Args:
    target: VictoriaOfHesse
    relation: :hasMother
    source: GeorgeMountbatten
  AssignClass (4777146f-e3ac-4caa-b753-dccf69997a54)
 Call ID: 4777146f-e3ac-4caa-b753-dccf69997a54
  Args:
    source: PrincessAlice
    type: :Woman
  AssignClass (9d199091-7444-44a9-838b-0cb4da3d86df)
 Call ID: 9d199091-7444-44a9-838b-0cb4da3d86df
  Args:
    source: PrincessAlice
    type: :Person
  AssignClass (fa64801e-3e29-4bcc-b45c-7f5a1b80c6b7)
 Call ID: fa64801e-3e29-4bcc-b45c-7f5a1b80c6b7
  Args:
    source: QueenLouiseOfSweden
    type: :Woman
  AssignClass (c0eca95d-cd5a-459c-99b3-233a3ba24e92)
 Call ID: c0eca95d-cd5a-459c-99b3-233a3ba24e92
  Args:
    source: QueenLouiseOfSweden
    type: :Person
  AssignClass (34ff47d9-f782-489d-9cd8-1f5611fe12ea)
 Call ID: 34ff47d9-f782-489d-9cd8-1f5611fe12ea
  Args:
    source: LouisMountbatten1stEarl
    type: :Man
  AssignClass (cf8dd914-8e21-48e0-b996-b0eb278d5cdb)
 Call ID: cf8dd914-8e21-48e0-b996-b0eb278d5cdb
  Args:
    source: LouisMountbatten1stEarl
    type: :Person
  AddTriple (72d01d21-12ec-4e14-b54d-bc66385d5969)
 Call ID: 72d01d21-12ec-4e14-b54d-bc66385d5969
  Args:
    target: PrincessAlice
    relation: :isSiblingOf
    source: GeorgeMountbatten
  AddTriple (6b8ee68a-82c5-454b-9c09-be67e0f159a6)
 Call ID: 6b8ee68a-82c5-454b-9c09-be67e0f159a6
  Args:
    relation: :isSiblingOf
    source: GeorgeMountbatten
    target: QueenLouiseOfSweden
  AddTriple (2b0ce662-1e9c-4d19-8f53-3aa7ede8b953)
 Call ID: 2b0ce662-1e9c-4d19-8f53-3aa7ede8b953
  Args:
    relation: :isSiblingOf
    source: GeorgeMountbatten
    target: LouisMountbatten1stEarl
  AssignClass (5bd3fd1a-3d38-42d2-adda-499faaa5be2b)
 Call ID: 5bd3fd1a-3d38-42d2-adda-499faaa5be2b
  Args:
    source: NadejdaMikhailovnaDeTorby
    type: :Woman
  AssignClass (72b165b9-ff8d-473f-bc72-d4446050e53a)
 Call ID: 72b165b9-ff8d-473f-bc72-d4446050e53a
  Args:
    source: NadejdaMikhailovnaDeTorby
    type: :Person
  AddLiteral (de7e673b-1e5f-44f2-a727-5a8a2e6c687f)
 Call ID: de7e673b-1e5f-44f2-a727-5a8a2e6c687f
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1916
    source: GeorgeMountbatten
  AddTriple (737a764c-22c8-4c77-9446-04848164bd89)
 Call ID: 737a764c-22c8-4c77-9446-04848164bd89
  Args:
    target: NadejdaMikhailovnaDeTorby
    relation: :hasRelation
    source: GeorgeMountbatten
  AssignClass (a886fb6c-f2cd-4db9-aaf9-9295e0d844c0)
 Call ID: a886fb6c-f2cd-4db9-aaf9-9295e0d844c0
  Args:
    source: MichaelMikhailovichRomanov
    type: :Man
  AssignClass (aabd29f5-61e2-4260-b270-be8c3e592220)
 Call ID: aabd29f5-61e2-4260-b270-be8c3e592220
  Args:
    source: MichaelMikhailovichRomanov
    type: :Person
  AssignClass (06fdf093-b4fa-4da4-9aba-f2ed013ba96f)
 Call ID: 06fdf093-b4fa-4da4-9aba-f2ed013ba96f
  Args:
    source: SophieVonMerenberg
    type: :Woman
  AssignClass (28d2a711-424e-44a6-b0f4-d9fe55175eae)
 Call ID: 28d2a711-424e-44a6-b0f4-d9fe55175eae
  Args:
    source: SophieVonMerenberg
    type: :Person
  AddTriple (cce0f7be-1f30-410f-a873-ec1979c51b58)
 Call ID: cce0f7be-1f30-410f-a873-ec1979c51b58
  Args:
    source: NadejdaMikhailovnaDeTorby
    relation: :hasFather
    target: MichaelMikhailovichRomanov
  AddTriple (e519b39e-ca16-4552-b87e-87d5b171e05e)
 Call ID: e519b39e-ca16-4552-b87e-87d5b171e05e
  Args:
    source: NadejdaMikhailovnaDeTorby
    relation: :hasMother
    target: SophieVonMerenberg
  AssignClass (0b8a2192-6da0-47c3-83aa-e6be4275678c)
 Call ID: 0b8a2192-6da0-47c3-83aa-e6be4275678c
  Args:
    source: PrincePhilip
    type: :Man
  AssignClass (69fec9fb-b766-4b33-943b-0762ce6fb901)
 Call ID: 69fec9fb-b766-4b33-943b-0762ce6fb901
  Args:
    source: PrincePhilip
    type: :Person
  AddTriple (c1160a45-36a0-498a-a9b1-9d63d94f4791)
 Call ID: c1160a45-36a0-498a-a9b1-9d63d94f4791
  Args:
    source: PrincePhilip
    relation: :hasMother
    target: PrincessAlice
  Finish (39315c70-1d01-4496-a1d3-70b8eba0788d)
 Call ID: 39315c70-1d01-4496-a1d3-70b8eba0788d
  Args: