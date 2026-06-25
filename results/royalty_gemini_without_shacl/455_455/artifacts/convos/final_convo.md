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
  AssignClass (a9d9f9cd-da77-48c7-9ce2-f1a644096d40)
 Call ID: a9d9f9cd-da77-48c7-9ce2-f1a644096d40
  Args:
    source: :Alexia
    type: :Woman
  AssignClass (b53cb3cc-f275-4d14-a988-1a6f52b5e74a)
 Call ID: b53cb3cc-f275-4d14-a988-1a6f52b5e74a
  Args:
    type: :Person
    source: :Alexia
  AddLiteral (dce6b2a7-f334-420a-8e29-ad82fa836d8f)
 Call ID: dce6b2a7-f334-420a-8e29-ad82fa836d8f
  Args:
    source: :Alexia
    literal_value: 1965
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (60a3161f-f710-48ee-a6de-383c5a6d68d0)
 Call ID: 60a3161f-f710-48ee-a6de-383c5a6d68d0
  Args:
    source: :ConstantineII
    type: :Man
  AssignClass (92ef441c-0eaf-41df-973a-c0914b834195)
 Call ID: 92ef441c-0eaf-41df-973a-c0914b834195
  Args:
    source: :ConstantineII
    type: :Person
  AssignClass (33df0a31-8fb3-4eb2-861a-ad42a55f49e5)
 Call ID: 33df0a31-8fb3-4eb2-861a-ad42a55f49e5
  Args:
    type: :Woman
    source: :AnneMarie
  AssignClass (4703df6f-6089-4512-816d-fa5121131667)
 Call ID: 4703df6f-6089-4512-816d-fa5121131667
  Args:
    source: :AnneMarie
    type: :Person
  AddTriple (0c891bd7-8b02-45b0-a71b-0eec1cb63295)
 Call ID: 0c891bd7-8b02-45b0-a71b-0eec1cb63295
  Args:
    target: :ConstantineII
    source: :Alexia
    relation: :hasFather
  AddTriple (dc811f8c-1a8f-4369-9d9c-42dd76369321)
 Call ID: dc811f8c-1a8f-4369-9d9c-42dd76369321
  Args:
    relation: :hasMother
    source: :Alexia
    target: :AnneMarie
  AssignClass (60955352-a6d7-499c-b47b-4847278df771)
 Call ID: 60955352-a6d7-499c-b47b-4847278df771
  Args:
    source: :Pavlos
    type: :Man
  AssignClass (07740ce8-28f3-4f7f-86ff-b5cd690284d8)
 Call ID: 07740ce8-28f3-4f7f-86ff-b5cd690284d8
  Args:
    type: :Person
    source: :Pavlos
  AddTriple (7b47c6c4-87e2-4af2-a40f-8520e5dd3996)
 Call ID: 7b47c6c4-87e2-4af2-a40f-8520e5dd3996
  Args:
    target: :Pavlos
    relation: :isSiblingOf
    source: :Alexia
  AssignClass (a3ad793b-4605-4417-aaf6-7af321f48385)
 Call ID: a3ad793b-4605-4417-aaf6-7af321f48385
  Args:
    type: :Man
    source: :CarlosJavierMoralesQuintana
  AssignClass (2ff857d6-0149-4939-bf02-981f0675fb99)
 Call ID: 2ff857d6-0149-4939-bf02-981f0675fb99
  Args:
    source: :CarlosJavierMoralesQuintana
    type: :Person
  AddTriple (f1368db4-de64-499b-9739-773cea3dec3b)
 Call ID: f1368db4-de64-499b-9739-773cea3dec3b
  Args:
    source: :Alexia
    relation: :hasRelation
    target: :CarlosJavierMoralesQuintana
  AddLiteral (cdf41ab9-0299-4ecd-b4bd-944ed9b86711)
 Call ID: cdf41ab9-0299-4ecd-b4bd-944ed9b86711
  Args:
    literal_value: 1999
    source: :Alexia
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (7ea8e1da-9b2d-4546-a07b-3dfa2d6d8a1f)
 Call ID: 7ea8e1da-9b2d-4546-a07b-3dfa2d6d8a1f
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (f8a59063-6bf7-41b1-8a3b-822a505ecde6)
 Call ID: f8a59063-6bf7-41b1-8a3b-822a505ecde6
  Args:
    type: :Person
    source: :Theodora
  AddTriple (017f20b2-6c10-4544-8169-dfd697ffbf21)
 Call ID: 017f20b2-6c10-4544-8169-dfd697ffbf21
  Args:
    target: :Alexia
    source: :Theodora
    relation: :isSisterOf
  AssignClass (93f80563-5c0f-489b-86f4-8cd14d913e51)
 Call ID: 93f80563-5c0f-489b-86f4-8cd14d913e51
  Args:
    source: :MariaOlympia
    type: :Woman
  AssignClass (0f1e90a1-c225-4387-b032-0bcad7bdad16)
 Call ID: 0f1e90a1-c225-4387-b032-0bcad7bdad16
  Args:
    type: :Person
    source: :MariaOlympia
  AddTriple (db032921-af55-4d70-b49f-a028b6dd41c7)
 Call ID: db032921-af55-4d70-b49f-a028b6dd41c7
  Args:
    source: :MariaOlympia
    relation: :hasMother
    target: :Pavlos
  AssignClass (35d6592d-4be2-42f1-8756-c2f790f5de95)
 Call ID: 35d6592d-4be2-42f1-8756-c2f790f5de95
  Args:
    type: :Woman
    source: :Sofia
  AssignClass (602744e9-beb7-4c6f-9f04-b25b9b9e9842)
 Call ID: 602744e9-beb7-4c6f-9f04-b25b9b9e9842
  Args:
    source: :Sofia
    type: :Person
  AddTriple (96eac1fb-4587-48d4-9a3e-9aece15ab011)
 Call ID: 96eac1fb-4587-48d4-9a3e-9aece15ab011
  Args:
    relation: :isAuntOf
    source: :Sofia
    target: :Alexia
  AssignClass (21c0e299-e3ec-4ce8-bcdc-ba8f3675e9c6)
 Call ID: 21c0e299-e3ec-4ce8-bcdc-ba8f3675e9c6
  Args:
    type: :Man
    source: :FelipeVI
  AssignClass (b90e42ba-af2c-4a6a-8304-db8fb25cf88d)
 Call ID: b90e42ba-af2c-4a6a-8304-db8fb25cf88d
  Args:
    source: :FelipeVI
    type: :Person
  AddTriple (90bbb26b-961e-43a1-9f1c-be39f380bd72)
 Call ID: 90bbb26b-961e-43a1-9f1c-be39f380bd72
  Args:
    relation: :isBloodrelationOf
    source: :Alexia
    target: :FelipeVI
  AssignClass (ab388cd6-918a-4101-9ecc-74c15c8f6bbc)
 Call ID: ab388cd6-918a-4101-9ecc-74c15c8f6bbc
  Args:
    type: :Woman
    source: :Ingrid
  AssignClass (281a0f60-fb92-4d93-82c7-b4017d296b8a)
 Call ID: 281a0f60-fb92-4d93-82c7-b4017d296b8a
  Args:
    source: :Ingrid
    type: :Person
  AddTriple (d9f80695-855d-4a22-876c-05e96f3b2eba)
 Call ID: d9f80695-855d-4a22-876c-05e96f3b2eba
  Args:
    relation: :hasMother
    source: :AnneMarie
    target: :Ingrid
  AssignClass (f9044905-677a-46af-9fb5-0c7043773a1a)
 Call ID: f9044905-677a-46af-9fb5-0c7043773a1a
  Args:
    source: :Mafalda
    type: :Woman
  AssignClass (58fecf20-32d9-48fe-b85a-5bd4295627c0)
 Call ID: 58fecf20-32d9-48fe-b85a-5bd4295627c0
  Args:
    source: :Mafalda
    type: :Person
  AssignClass (9898aac9-c488-469a-99d6-49c475973942)
 Call ID: 9898aac9-c488-469a-99d6-49c475973942
  Args:
    type: :Man
    source: :Kyril
  AssignClass (f252243b-05c1-4397-be9d-551571728c9f)
 Call ID: f252243b-05c1-4397-be9d-551571728c9f
  Args:
    source: :Kyril
    type: :Person
  AddTriple (8560a7b3-bc8e-4349-a591-474a08a726d3)
 Call ID: 8560a7b3-bc8e-4349-a591-474a08a726d3
  Args:
    source: :Mafalda
    relation: :hasFather
    target: :Kyril
  AssignClass (b6d52b44-a178-446b-9682-cd22dde039b7)
 Call ID: b6d52b44-a178-446b-9682-cd22dde039b7
  Args:
    type: :Man
    source: :Simeon
  AssignClass (196489ea-d042-4533-8693-fdf34a6b28c0)
 Call ID: 196489ea-d042-4533-8693-fdf34a6b28c0
  Args:
    source: :Simeon
    type: :Person
  AddTriple (5f3344f8-1b3b-4e50-ad97-40479a23ba28)
 Call ID: 5f3344f8-1b3b-4e50-ad97-40479a23ba28
  Args:
    relation: :hasFather
    source: :Kyril
    target: :Simeon
  Finish (47afa4bf-9c49-4284-b935-00394851570a)
 Call ID: 47afa4bf-9c49-4284-b935-00394851570a
  Args: