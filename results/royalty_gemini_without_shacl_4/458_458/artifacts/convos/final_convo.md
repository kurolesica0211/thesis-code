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
  AssignClass (64cddc1a-8eda-4a48-b7f3-4104e6e59dba)
 Call ID: 64cddc1a-8eda-4a48-b7f3-4104e6e59dba
  Args:
    type: :Woman
    source: Alexia_of_Greece_and_Denmark
  AssignClass (496a398d-95fc-45af-b739-16ea5faa2bb3)
 Call ID: 496a398d-95fc-45af-b739-16ea5faa2bb3
  Args:
    type: :Person
    source: Alexia_of_Greece_and_Denmark
  AddLiteral (f6083c76-823c-466a-a281-6cdfa9c2600e)
 Call ID: f6083c76-823c-466a-a281-6cdfa9c2600e
  Args:
    literal_type: xsd:positiveInteger
    source: Alexia_of_Greece_and_Denmark
    literal_value: 1965
    relation: :hasBirthYear
  AssignClass (a19c25a5-ad79-42a8-84cc-22d31d7dab2c)
 Call ID: a19c25a5-ad79-42a8-84cc-22d31d7dab2c
  Args:
    type: :Man
    source: Constantine_II
  AssignClass (93652fdc-3b4b-407c-ba7e-288505b184ae)
 Call ID: 93652fdc-3b4b-407c-ba7e-288505b184ae
  Args:
    type: :Person
    source: Constantine_II
  AssignClass (78cd8a7c-bb8b-4abe-9725-177f7a86ff74)
 Call ID: 78cd8a7c-bb8b-4abe-9725-177f7a86ff74
  Args:
    type: :Woman
    source: Anne-Marie
  AssignClass (8cf2eced-a9a7-4d36-9210-53eb2e423666)
 Call ID: 8cf2eced-a9a7-4d36-9210-53eb2e423666
  Args:
    type: :Person
    source: Anne-Marie
  AddTriple (79bfda94-d12f-4d79-bc0b-f737ab121c9c)
 Call ID: 79bfda94-d12f-4d79-bc0b-f737ab121c9c
  Args:
    target: Constantine_II
    relation: :hasFather
    source: Alexia_of_Greece_and_Denmark
  AddTriple (d641b8a9-4ccb-40c6-ad27-363982618f2e)
 Call ID: d641b8a9-4ccb-40c6-ad27-363982618f2e
  Args:
    relation: :hasMother
    target: Anne-Marie
    source: Alexia_of_Greece_and_Denmark
  AssignClass (1731246b-d8ae-47b6-98be-2b3ff35c5b67)
 Call ID: 1731246b-d8ae-47b6-98be-2b3ff35c5b67
  Args:
    type: :Man
    source: Pavlos
  AssignClass (a60213c1-61f6-40a5-8b30-640eb20cb6a2)
 Call ID: a60213c1-61f6-40a5-8b30-640eb20cb6a2
  Args:
    type: :Person
    source: Pavlos
  AddTriple (d75232f4-a84a-4b7f-84c9-6f159cdb9ff1)
 Call ID: d75232f4-a84a-4b7f-84c9-6f159cdb9ff1
  Args:
    source: Alexia_of_Greece_and_Denmark
    target: Pavlos
    relation: :hasBrother
  AssignClass (48794b7a-6a30-4a80-b411-52b6592bea8e)
 Call ID: 48794b7a-6a30-4a80-b411-52b6592bea8e
  Args:
    type: :Man
    source: Carlos_Javier_Morales_Quintana
  AssignClass (14b5465f-bf01-4f5c-b740-1b7cd3194d1a)
 Call ID: 14b5465f-bf01-4f5c-b740-1b7cd3194d1a
  Args:
    type: :Person
    source: Carlos_Javier_Morales_Quintana
  AddLiteral (8362308c-92e1-4651-912e-0b00b39f679a)
 Call ID: 8362308c-92e1-4651-912e-0b00b39f679a
  Args:
    relation: :hasMarriageYear
    literal_value: 1999
    literal_type: xsd:positiveInteger
    source: Alexia_of_Greece_and_Denmark
  AddTriple (a9907ae9-bdd6-4ca2-8a38-41c30bb92d6a)
 Call ID: a9907ae9-bdd6-4ca2-8a38-41c30bb92d6a
  Args:
    target: Carlos_Javier_Morales_Quintana
    relation: :hasRelation
    source: Alexia_of_Greece_and_Denmark
  AssignClass (db12f3c0-57f2-415c-a61b-a7b3239f201c)
 Call ID: db12f3c0-57f2-415c-a61b-a7b3239f201c
  Args:
    type: :Woman
    source: Theodora
  AssignClass (a295e7b9-cd77-4d11-ac5d-f349595b89ae)
 Call ID: a295e7b9-cd77-4d11-ac5d-f349595b89ae
  Args:
    type: :Person
    source: Theodora
  AddTriple (fd16b651-e9ba-41e2-ab09-50ec3b14893b)
 Call ID: fd16b651-e9ba-41e2-ab09-50ec3b14893b
  Args:
    source: Alexia_of_Greece_and_Denmark
    relation: :hasSister
    target: Theodora
  AssignClass (9f15f5a0-2336-4984-89f6-a32f6f0fdc90)
 Call ID: 9f15f5a0-2336-4984-89f6-a32f6f0fdc90
  Args:
    type: :Woman
    source: Maria-Olympia
  AssignClass (ec5dae3b-131d-4fd0-8374-1ef65538d948)
 Call ID: ec5dae3b-131d-4fd0-8374-1ef65538d948
  Args:
    type: :Person
    source: Maria-Olympia
  AssignClass (16fb92c5-f736-4ad0-ade7-b33674a5a957)
 Call ID: 16fb92c5-f736-4ad0-ade7-b33674a5a957
  Args:
    type: :Woman
    source: Sofia
  AssignClass (3417a519-c2b8-4eb4-b39b-a11921c0645b)
 Call ID: 3417a519-c2b8-4eb4-b39b-a11921c0645b
  Args:
    type: :Person
    source: Sofia
  AddTriple (7c54289a-2037-40d8-921b-34235b8be217)
 Call ID: 7c54289a-2037-40d8-921b-34235b8be217
  Args:
    target: Alexia_of_Greece_and_Denmark
    relation: :isAuntOf
    source: Sofia
  AssignClass (fbdd832a-bc2b-4acb-ac48-7dc8830c6afc)
 Call ID: fbdd832a-bc2b-4acb-ac48-7dc8830c6afc
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (7358e589-a0c0-4b44-8d87-ba2c27261fd5)
 Call ID: 7358e589-a0c0-4b44-8d87-ba2c27261fd5
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (4c6235af-2241-48d5-b234-d1cd3312f0d1)
 Call ID: 4c6235af-2241-48d5-b234-d1cd3312f0d1
  Args:
    type: :Woman
    source: Ingrid
  AssignClass (6b537ab2-26fd-45a0-9a64-0c24f84d959a)
 Call ID: 6b537ab2-26fd-45a0-9a64-0c24f84d959a
  Args:
    type: :Person
    source: Ingrid
  AssignClass (3b299c8c-2f57-4739-a98a-c2f0eceaf541)
 Call ID: 3b299c8c-2f57-4739-a98a-c2f0eceaf541
  Args:
    type: :Woman
    source: Mafalda
  AssignClass (aa00348b-593a-456e-8abc-12789be57436)
 Call ID: aa00348b-593a-456e-8abc-12789be57436
  Args:
    type: :Person
    source: Mafalda
  AssignClass (67f89027-d606-4de5-8cac-d3e942d50a71)
 Call ID: 67f89027-d606-4de5-8cac-d3e942d50a71
  Args:
    type: :Man
    source: Kyril
  AssignClass (19a0e511-024a-4d6c-b1e7-003b34644498)
 Call ID: 19a0e511-024a-4d6c-b1e7-003b34644498
  Args:
    type: :Person
    source: Kyril
  AssignClass (1f50b6fc-1d30-4ed4-b3e0-3307e487460b)
 Call ID: 1f50b6fc-1d30-4ed4-b3e0-3307e487460b
  Args:
    type: :Man
    source: Simeon
  AssignClass (1b8b0a54-59cd-4ba8-a31e-96dacdc533b6)
 Call ID: 1b8b0a54-59cd-4ba8-a31e-96dacdc533b6
  Args:
    type: :Person
    source: Simeon
  AddTriple (e6fa5a7d-f4e0-45b7-adc7-d368888e24b3)
 Call ID: e6fa5a7d-f4e0-45b7-adc7-d368888e24b3
  Args:
    relation: :hasFather
    target: Kyril
    source: Mafalda
  AddTriple (3e4fb450-9013-4275-b1ae-721bbfe84a8a)
 Call ID: 3e4fb450-9013-4275-b1ae-721bbfe84a8a
  Args:
    target: Simeon
    relation: :hasFather
    source: Kyril
  Finish (63e0a41e-e982-462f-be3a-7cb71aea8a53)
 Call ID: 63e0a41e-e982-462f-be3a-7cb71aea8a53
  Args: