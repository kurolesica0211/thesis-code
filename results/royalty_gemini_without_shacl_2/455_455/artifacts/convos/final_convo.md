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
  AssignClass (77c8ff20-c2a9-491d-bcd9-76e0b0f97427)
 Call ID: 77c8ff20-c2a9-491d-bcd9-76e0b0f97427
  Args:
    type: :Woman
    source: Alexia
  AssignClass (3b9801fe-a2ca-4ce1-aee2-ecee6d66074c)
 Call ID: 3b9801fe-a2ca-4ce1-aee2-ecee6d66074c
  Args:
    type: :Person
    source: Alexia
  AddLiteral (f5bb960d-4acc-4098-bd47-c4458137e581)
 Call ID: f5bb960d-4acc-4098-bd47-c4458137e581
  Args:
    source: Alexia
    relation: :hasBirthYear
    literal_value: 1965
    literal_type: xsd:integer
  AssignClass (a76fd6d2-a6f2-4cd6-85c2-8a61cb3a32d1)
 Call ID: a76fd6d2-a6f2-4cd6-85c2-8a61cb3a32d1
  Args:
    type: :Man
    source: Constantine_II
  AssignClass (1c184894-3c09-4864-9ea7-38ab85bbbeb3)
 Call ID: 1c184894-3c09-4864-9ea7-38ab85bbbeb3
  Args:
    source: Constantine_II
    type: :Person
  AssignClass (636efb7a-027e-4c3c-aabc-ef6fee3c764b)
 Call ID: 636efb7a-027e-4c3c-aabc-ef6fee3c764b
  Args:
    source: Anne-Marie
    type: :Woman
  AssignClass (42a0eddf-e0ee-4dfb-a014-a1f91af0ca41)
 Call ID: 42a0eddf-e0ee-4dfb-a014-a1f91af0ca41
  Args:
    source: Anne-Marie
    type: :Person
  AddTriple (ba70a736-14ed-4989-8b19-e30f6714ae3b)
 Call ID: ba70a736-14ed-4989-8b19-e30f6714ae3b
  Args:
    source: Alexia
    target: Constantine_II
    relation: :hasFather
  AddTriple (cc591a26-b5ce-40b3-a84b-004e5b9cf419)
 Call ID: cc591a26-b5ce-40b3-a84b-004e5b9cf419
  Args:
    target: Anne-Marie
    source: Alexia
    relation: :hasMother
  AssignClass (2ec7d669-6f1b-4d4d-89bf-ed5508d66194)
 Call ID: 2ec7d669-6f1b-4d4d-89bf-ed5508d66194
  Args:
    type: :Man
    source: Pavlos
  AssignClass (f7b24aee-1df8-4513-9a1d-500d7e158a9c)
 Call ID: f7b24aee-1df8-4513-9a1d-500d7e158a9c
  Args:
    source: Pavlos
    type: :Person
  AddTriple (72919bd2-a288-4509-8ec3-f77d6f3ced4a)
 Call ID: 72919bd2-a288-4509-8ec3-f77d6f3ced4a
  Args:
    relation: :isSiblingOf
    target: Pavlos
    source: Alexia
  AssignClass (24ca985b-ada0-4a64-aa51-442c3e72e3d5)
 Call ID: 24ca985b-ada0-4a64-aa51-442c3e72e3d5
  Args:
    type: :Man
    source: Carlos_Javier_Morales_Quintana
  AssignClass (31d6370f-9e48-4c66-9705-5a3244a26f07)
 Call ID: 31d6370f-9e48-4c66-9705-5a3244a26f07
  Args:
    source: Carlos_Javier_Morales_Quintana
    type: :Person
  AddTriple (69347197-9a7e-41e3-94b9-bffc1eb8d09e)
 Call ID: 69347197-9a7e-41e3-94b9-bffc1eb8d09e
  Args:
    relation: :hasRelation
    source: Alexia
    target: Carlos_Javier_Morales_Quintana
  AddLiteral (eae54317-2f4c-47b3-8d2e-27ac64825bb4)
 Call ID: eae54317-2f4c-47b3-8d2e-27ac64825bb4
  Args:
    literal_value: 1999
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Alexia
  AssignClass (561e1fad-efcf-41a1-80b6-5dd041375882)
 Call ID: 561e1fad-efcf-41a1-80b6-5dd041375882
  Args:
    source: Theodora
    type: :Woman
  AssignClass (15f2d43b-30c4-49dd-94e5-053a41e59d88)
 Call ID: 15f2d43b-30c4-49dd-94e5-053a41e59d88
  Args:
    source: Theodora
    type: :Person
  AddTriple (fa437bb3-8da0-48ce-ad43-e90a5fde4ac6)
 Call ID: fa437bb3-8da0-48ce-ad43-e90a5fde4ac6
  Args:
    target: Theodora
    source: Alexia
    relation: :isSiblingOf
  AssignClass (5c48fcf6-12ed-4e85-8dba-050557cdf705)
 Call ID: 5c48fcf6-12ed-4e85-8dba-050557cdf705
  Args:
    type: :Woman
    source: Maria-Olympia
  AssignClass (bff9d276-c48f-438d-9899-a7e1b3b6113f)
 Call ID: bff9d276-c48f-438d-9899-a7e1b3b6113f
  Args:
    type: :Person
    source: Maria-Olympia
  AddTriple (810c1fb4-c09f-4be8-b646-22ead84dc89f)
 Call ID: 810c1fb4-c09f-4be8-b646-22ead84dc89f
  Args:
    target: Pavlos
    source: Maria-Olympia
    relation: :hasMother
  AssignClass (f36bf7db-79a4-4cf4-a153-0787833eac53)
 Call ID: f36bf7db-79a4-4cf4-a153-0787833eac53
  Args:
    type: :Woman
    source: Mafalda
  AssignClass (a113769d-fbd5-4e5e-b664-6bb069a05e63)
 Call ID: a113769d-fbd5-4e5e-b664-6bb069a05e63
  Args:
    type: :Person
    source: Mafalda
  AssignClass (15eaa3d3-61f1-4894-810f-4eefef916e21)
 Call ID: 15eaa3d3-61f1-4894-810f-4eefef916e21
  Args:
    source: Kyril
    type: :Man
  AssignClass (92b80305-4246-43b3-ac1f-2e5bf6fdaf9d)
 Call ID: 92b80305-4246-43b3-ac1f-2e5bf6fdaf9d
  Args:
    type: :Person
    source: Kyril
  AddTriple (88cb81f5-4a62-4257-8960-f4ae30eae6cd)
 Call ID: 88cb81f5-4a62-4257-8960-f4ae30eae6cd
  Args:
    relation: :hasFather
    target: Kyril
    source: Mafalda
  AssignClass (f34f5e04-1cf2-44b7-bf7b-c1b30267a0f8)
 Call ID: f34f5e04-1cf2-44b7-bf7b-c1b30267a0f8
  Args:
    type: :Man
    source: Simeon_of_Bulgaria
  AssignClass (db9436c4-a32f-43df-9436-6b2627b638ec)
 Call ID: db9436c4-a32f-43df-9436-6b2627b638ec
  Args:
    type: :Person
    source: Simeon_of_Bulgaria
  AddTriple (cb9d677b-55e0-4064-98db-6c7d0044c874)
 Call ID: cb9d677b-55e0-4064-98db-6c7d0044c874
  Args:
    target: Simeon_of_Bulgaria
    source: Kyril
    relation: :hasFather
  AssignClass (3ce7073d-f9ad-4268-b677-a531e1ac3e37)
 Call ID: 3ce7073d-f9ad-4268-b677-a531e1ac3e37
  Args:
    type: :Woman
    source: Sofia
  AssignClass (9ac88d33-8521-4afd-9d1a-d1441c6e744f)
 Call ID: 9ac88d33-8521-4afd-9d1a-d1441c6e744f
  Args:
    source: Sofia
    type: :Person
  AddTriple (e86c1573-071b-41b3-ade9-297d24f7e89a)
 Call ID: e86c1573-071b-41b3-ade9-297d24f7e89a
  Args:
    source: Sofia
    target: Alexia
    relation: :isAuntOf
  AssignClass (135b9d4d-72c6-48e9-8ef6-1247888dd400)
 Call ID: 135b9d4d-72c6-48e9-8ef6-1247888dd400
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (c478fa12-9c12-46d6-921b-983e5b8cc20b)
 Call ID: c478fa12-9c12-46d6-921b-983e5b8cc20b
  Args:
    type: :Person
    source: Felipe_VI
  AddTriple (6338e399-d454-4135-a231-a2ccf691cc55)
 Call ID: 6338e399-d454-4135-a231-a2ccf691cc55
  Args:
    target: Felipe_VI
    source: Alexia
    relation: :isBloodrelationOf
  Finish (474ac3d5-803b-4186-b4be-fce8747e40a8)
 Call ID: 474ac3d5-803b-4186-b4be-fce8747e40a8
  Args: