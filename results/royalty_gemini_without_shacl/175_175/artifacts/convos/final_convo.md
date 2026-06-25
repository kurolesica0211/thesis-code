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
Princess Alexia of Greece and Denmark (Greek: Αλεξία Ντε Γκρες, romanized: Alexía de Grèce; born 10 July 1965) is the eldest child of Constantine II and Anne-Marie, who were King and Queen of Greece from 1964 until the abolition of the monarchy in 1973.
Biography

Alexia was born on 10 July 1965 at Mon Repos, a villa on the Greek island of Corfu used at the time as a summer residence by the Greek royal family.
She was the first child born to the then King Constantine II and Queen Anne-Marie of the Hellenes.
At the time of her birth, her father was King of Greece, her grandfather was King of Denmark, and her great-grandfather was King of Sweden.
As the monarch's only child, between her own birth and the birth on 20 May 1967 of her brother Pavlos, Alexia was heir presumptive to the throne of the Hellenes, then an extant monarchy.
The Greek Constitution of 1952 had changed Greece's order of succession to the throne from the previous Salic law, prevalent in much of the continent, and which precluded the succession of women, to male-preference primogeniture, which accorded succession to the throne to a female member of a dynasty if she has no brothers, similar to the then extant succession laws of the United Kingdom, Denmark and Spain.
Alexia grew up in exile and was raised in between Rome and London.
The family then briefly moved to Denmark and stayed at Amalienborg Palace, and then to London the following year.
Prior to Alexia's education at the Hellenic College of London, she attended the Miss Surtee's School for Boys and Girls in Rome, Italy.
Οn 20 December 2024, Alexia along with other members of the former royal family acquired Greek citizenship, under the surname "de Grèce".
Marriage and children

Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


On 9 July 1999, Alexia married Carlos Javier Morales Quintana, an architect and a champion yachtsman, at St. Sophia Cathedral, London.
In May 1999, two months before their wedding, Alexia and Carlos were involved in a yachting accident on a boat named the Alexia.
Alexia and Carlos were the only two people out of the thirteen on board to be injured.
Alexia suffered a broken collarbone and Carlos a fractured kneecap.
At her wedding, Alexia wore a gown by the Austrian designer Inge Sprawson.
Alexia's mother, Anne-Marie, and grandmother, Ingrid, had both also worn the same tiara on their own wedding day.
Her attendants included her sister Princess Theodora, her niece Princess Maria-Olympia, and Princess Mafalda, daughter of Kyril, Prince of Preslav, a son of former King Simeon of Bulgaria.
The couple have four children: 


Their children's last names are "Morales y de Grecia", which translates to "Morales and of Greece", taking their father's surname and their mother's royal title.
Alexia and her family now live in her husband's native land, at Puerto Calero marina, Yaiza, Lanzarote in the Canary Islands, in a house designed by her husband.
The Canary Islands are an autonomous community of Spain, where Alexia's aunt, Queen Sofía, lives and first cousin, Felipe VI, lives and rules.



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
  AssignClass (14dfa235-cf0b-4180-a6bd-48a12ff2cf77)
 Call ID: 14dfa235-cf0b-4180-a6bd-48a12ff2cf77
  Args:
    source: Alexia
    type: :Woman
  AssignClass (7f8ba93a-08ba-4d41-a28c-2f7699104490)
 Call ID: 7f8ba93a-08ba-4d41-a28c-2f7699104490
  Args:
    type: :Person
    source: Alexia
  AddLiteral (becf9cf6-15f4-486a-b5a8-75fcad98d923)
 Call ID: becf9cf6-15f4-486a-b5a8-75fcad98d923
  Args:
    source: Alexia
    relation: :hasBirthYear
    literal_value: 1965
    literal_type: xsd:integer
  AssignClass (602d55cf-4f89-47b2-97fd-72ae4954d775)
 Call ID: 602d55cf-4f89-47b2-97fd-72ae4954d775
  Args:
    source: ConstantineII
    type: :Man
  AssignClass (7514a0f8-c063-45b8-9e3f-a322c6e4351f)
 Call ID: 7514a0f8-c063-45b8-9e3f-a322c6e4351f
  Args:
    source: ConstantineII
    type: :Person
  AssignClass (7c230023-318a-42cc-8bea-d5fd5207b918)
 Call ID: 7c230023-318a-42cc-8bea-d5fd5207b918
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (df4ea5ab-95fd-41b6-85d3-a4d53a700f9d)
 Call ID: df4ea5ab-95fd-41b6-85d3-a4d53a700f9d
  Args:
    source: Anne-Marie
    type: :Person
  AddTriple (0725c34e-2b00-4a62-adbf-46c626602ccc)
 Call ID: 0725c34e-2b00-4a62-adbf-46c626602ccc
  Args:
    relation: :hasFather
    source: Alexia
    target: ConstantineII
  AddTriple (2d225081-5702-448c-9528-bb0a3e4d14ca)
 Call ID: 2d225081-5702-448c-9528-bb0a3e4d14ca
  Args:
    target: Anne-Marie
    source: Alexia
    relation: :hasMother
  AssignClass (6046b106-0d85-431b-a3d7-e0042b467950)
 Call ID: 6046b106-0d85-431b-a3d7-e0042b467950
  Args:
    type: :Man
    source: Pavlos
  AssignClass (240db14a-ccd0-473c-aee9-ba87bcfccd7a)
 Call ID: 240db14a-ccd0-473c-aee9-ba87bcfccd7a
  Args:
    type: :Person
    source: Pavlos
  AddTriple (52f09520-ffd5-448e-97ac-918c1c92276f)
 Call ID: 52f09520-ffd5-448e-97ac-918c1c92276f
  Args:
    source: Pavlos
    relation: :isBrotherOf
    target: Alexia
  AssignClass (9ecb23fc-34de-4269-96c1-de90fe10140b)
 Call ID: 9ecb23fc-34de-4269-96c1-de90fe10140b
  Args:
    type: :Man
    source: CarlosJavierMoralesQuintana
  AssignClass (429128c9-1407-4988-ace5-3ddb5699d916)
 Call ID: 429128c9-1407-4988-ace5-3ddb5699d916
  Args:
    source: CarlosJavierMoralesQuintana
    type: :Person
  AddTriple (2d341c98-e97c-425d-b1d5-5e7f8b6758ad)
 Call ID: 2d341c98-e97c-425d-b1d5-5e7f8b6758ad
  Args:
    target: CarlosJavierMoralesQuintana
    source: Alexia
    relation: :hasRelation
  AddLiteral (422ba154-ad00-4433-b53b-6a45a4aed8c4)
 Call ID: 422ba154-ad00-4433-b53b-6a45a4aed8c4
  Args:
    literal_type: xsd:integer
    literal_value: 1999
    source: Alexia
    relation: :hasMarriageYear
  AssignClass (c26173ad-b8e1-4a22-bc68-72a70b2b5b85)
 Call ID: c26173ad-b8e1-4a22-bc68-72a70b2b5b85
  Args:
    type: :Woman
    source: Theodora
  AssignClass (abea7734-f3ae-444d-a0ff-76c17b7ffb60)
 Call ID: abea7734-f3ae-444d-a0ff-76c17b7ffb60
  Args:
    source: Theodora
    type: :Person
  AddTriple (fc48c083-0174-4e57-8538-d41164d2ee77)
 Call ID: fc48c083-0174-4e57-8538-d41164d2ee77
  Args:
    relation: :isSisterOf
    source: Theodora
    target: Alexia
  AssignClass (21cd6f50-7270-4098-b1fe-3842d0f139d1)
 Call ID: 21cd6f50-7270-4098-b1fe-3842d0f139d1
  Args:
    type: :Woman
    source: Maria-Olympia
  AssignClass (410b09c5-c911-4d4d-a7e6-99bf38f252c5)
 Call ID: 410b09c5-c911-4d4d-a7e6-99bf38f252c5
  Args:
    type: :Person
    source: Maria-Olympia
  AddTriple (07357001-c157-4412-95ec-3dc3a44d638b)
 Call ID: 07357001-c157-4412-95ec-3dc3a44d638b
  Args:
    relation: :isChildOf
    source: Maria-Olympia
    target: Pavlos
  AssignClass (3436ea20-4c1f-4157-8bf0-1378b96cdd80)
 Call ID: 3436ea20-4c1f-4157-8bf0-1378b96cdd80
  Args:
    source: Sofia
    type: :Woman
  AssignClass (ce2ce1a7-7661-4db4-86cd-223d4663ba6a)
 Call ID: ce2ce1a7-7661-4db4-86cd-223d4663ba6a
  Args:
    type: :Person
    source: Sofia
  AddTriple (064fde4a-482a-4841-a65d-c714e3120152)
 Call ID: 064fde4a-482a-4841-a65d-c714e3120152
  Args:
    target: Alexia
    relation: :isAuntOf
    source: Sofia
  AssignClass (b01c7679-b3fe-4940-8fbc-d4a2c6d7f60b)
 Call ID: b01c7679-b3fe-4940-8fbc-d4a2c6d7f60b
  Args:
    type: :Man
    source: FelipeVI
  AssignClass (4db217e0-6f5f-45b6-8eb0-8200d9ac65de)
 Call ID: 4db217e0-6f5f-45b6-8eb0-8200d9ac65de
  Args:
    source: FelipeVI
    type: :Person
  AddTriple (ab4ba8bd-19f4-413d-a2e1-f28536111ca7)
 Call ID: ab4ba8bd-19f4-413d-a2e1-f28536111ca7
  Args:
    target: Alexia
    source: FelipeVI
    relation: :isBloodrelationOf
  AssignClass (383c89d4-883a-4ea6-9d0c-060e15030a00)
 Call ID: 383c89d4-883a-4ea6-9d0c-060e15030a00
  Args:
    source: Ingrid
    type: :Woman
  AssignClass (5ed6018a-3239-4bbb-91c2-686956874c9a)
 Call ID: 5ed6018a-3239-4bbb-91c2-686956874c9a
  Args:
    type: :Person
    source: Ingrid
  AddTriple (29793c65-9370-4e09-989f-6948bc797657)
 Call ID: 29793c65-9370-4e09-989f-6948bc797657
  Args:
    target: Ingrid
    source: Anne-Marie
    relation: :hasMother
  Finish (6ec44ce0-673c-4d0d-a4fd-8ff3a014a524)
 Call ID: 6ec44ce0-673c-4d0d-a4fd-8ff3a014a524
  Args: