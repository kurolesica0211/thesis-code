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
Princess Maria Kirillovna of Russia (2 February 1907 – 25 October 1951) was the eldest daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh.
She was born in Coburg when her parents were in exile because their marriage had not been approved by Tsar Nicholas II.
The family returned to Russia prior to World War I, but was forced to flee following the Russian Revolution of 1917.
Biography

Early life

Maria was raised in Coburg and in Saint-Briac, France.
She was born Princess Maria Kirillovna of Russia, but her father granted her the title Grand Duchess of Russia with the style Imperial Highness when he declared himself Guardian of the Throne in 1921.
As a child, the dark-haired, dark-eyed Maria took after her maternal grandmother, Grand Duchess Maria Alexandrovna of Russia, in appearance, with a wide, round face and a tendency to be overweight and to look older than her actual age when she was still a teenager.
In 1922, when she was fifteen, the "flighty" Maria visited her aunt, Queen Marie of Romania, and carried on a flirtation with the son-in-law of a lady-in-waiting at the Romanian court.
Her thirteen-year-old cousin, Princess Ileana of Romania, spread rumors about the flirtation when Maria returned home, resulting in strained relations between Marie of Romania and Maria's mother, Victoria.
Marriage and issue

On 24 February 1925, Maria was engaged to Karl, 6th Prince of Leiningen (13 February 1898 – 2 August 1946), and they were married on 25 November.
They were third cousins, as Karl's great-grandfather Carl, was the half-brother of Maria's great-grandmother, Queen Victoria.
Victoria was at her daughter's bedside when she gave birth to her first child, Emich Kirill, in 1926.
She also attended the subsequent births of Maria's children.
Maria had seven children in all, one of whom died in infancy during World War II.
Maria, left with little money, struggled to support her surviving six children.
Karl and Maria had seven children:


Ancestry

Notes

References

External links



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
  AssignClass (212269aa-a5e3-4c67-8195-694ebeedd44f)
 Call ID: 212269aa-a5e3-4c67-8195-694ebeedd44f
  Args:
    type: :Woman
    source: :Maria_Kirillovna_of_Russia
  AssignClass (0e6472bb-ba8d-4feb-b32e-ecbeedc859ac)
 Call ID: 0e6472bb-ba8d-4feb-b32e-ecbeedc859ac
  Args:
    source: :Maria_Kirillovna_of_Russia
    type: :Person
  AddLiteral (e61ad895-87ca-41c3-bf96-4bb7667dc4ff)
 Call ID: e61ad895-87ca-41c3-bf96-4bb7667dc4ff
  Args:
    literal_type: xsd:integer
    source: :Maria_Kirillovna_of_Russia
    relation: :hasBirthYear
    literal_value: 1907
  AddLiteral (e8de0872-8683-4739-89a3-61d74cb077a6)
 Call ID: e8de0872-8683-4739-89a3-61d74cb077a6
  Args:
    literal_type: xsd:integer
    source: :Maria_Kirillovna_of_Russia
    relation: :hasDeathYear
    literal_value: 1951
  AssignClass (51331847-b4c0-43d6-90e8-aec239bee455)
 Call ID: 51331847-b4c0-43d6-90e8-aec239bee455
  Args:
    source: :Kirill_Vladimirovich_of_Russia
    type: :Man
  AssignClass (2a1c6d0f-09f7-4c62-b828-66790a304932)
 Call ID: 2a1c6d0f-09f7-4c62-b828-66790a304932
  Args:
    source: :Kirill_Vladimirovich_of_Russia
    type: :Person
  AssignClass (867a40ca-a34b-4360-9910-a27ca8c714a6)
 Call ID: 867a40ca-a34b-4360-9910-a27ca8c714a6
  Args:
    type: :Ancestor
    source: :Kirill_Vladimirovich_of_Russia
  AssignClass (31edb91e-b7ad-4242-8d86-5901d2e05ca5)
 Call ID: 31edb91e-b7ad-4242-8d86-5901d2e05ca5
  Args:
    type: :Woman
    source: :Victoria_Melita_of_Edinburgh
  AssignClass (f929f47a-f8c0-44cf-aba6-2c9c8efd0cb3)
 Call ID: f929f47a-f8c0-44cf-aba6-2c9c8efd0cb3
  Args:
    type: :Person
    source: :Victoria_Melita_of_Edinburgh
  AssignClass (bb3c4761-d97c-4686-a8e5-876dd2b8d73f)
 Call ID: bb3c4761-d97c-4686-a8e5-876dd2b8d73f
  Args:
    source: :Victoria_Melita_of_Edinburgh
    type: :Ancestor
  AddTriple (3bf22947-3811-4e3c-bd08-8a8343d9914a)
 Call ID: 3bf22947-3811-4e3c-bd08-8a8343d9914a
  Args:
    target: :Kirill_Vladimirovich_of_Russia
    relation: :hasFather
    source: :Maria_Kirillovna_of_Russia
  AddTriple (7b68c948-c1cc-4da7-b106-8fc5ac0aa178)
 Call ID: 7b68c948-c1cc-4da7-b106-8fc5ac0aa178
  Args:
    source: :Maria_Kirillovna_of_Russia
    relation: :hasMother
    target: :Victoria_Melita_of_Edinburgh
  AssignClass (203d5204-61de-4c48-847b-d4066af0d4cc)
 Call ID: 203d5204-61de-4c48-847b-d4066af0d4cc
  Args:
    source: :Maria_Alexandrovna_of_Russia
    type: :Woman
  AssignClass (e65b2162-4570-4b4d-bff9-76b8ed300687)
 Call ID: e65b2162-4570-4b4d-bff9-76b8ed300687
  Args:
    source: :Maria_Alexandrovna_of_Russia
    type: :Person
  AssignClass (dfe008f1-00f1-49e4-b835-cea253afd74c)
 Call ID: dfe008f1-00f1-49e4-b835-cea253afd74c
  Args:
    type: :Ancestor
    source: :Maria_Alexandrovna_of_Russia
  AssignClass (c0106048-40e2-4a44-bd3c-0f351cf325b2)
 Call ID: c0106048-40e2-4a44-bd3c-0f351cf325b2
  Args:
    type: :Woman
    source: :Marie_of_Romania
  AssignClass (e53addb9-981f-4622-b80f-580a4b364f37)
 Call ID: e53addb9-981f-4622-b80f-580a4b364f37
  Args:
    source: :Marie_of_Romania
    type: :Person
  AssignClass (b7f32944-54b0-4d03-861d-63b9d4bd9669)
 Call ID: b7f32944-54b0-4d03-861d-63b9d4bd9669
  Args:
    type: :Woman
    source: :Ileana_of_Romania
  AssignClass (eb765f9b-2080-441d-9431-74e0f99a5cae)
 Call ID: eb765f9b-2080-441d-9431-74e0f99a5cae
  Args:
    type: :Person
    source: :Ileana_of_Romania
  AssignClass (bb3dcb2b-723d-4614-a62b-ab01e5dc28f3)
 Call ID: bb3dcb2b-723d-4614-a62b-ab01e5dc28f3
  Args:
    source: :Karl_Prince_of_Leiningen
    type: :Man
  AssignClass (2a9a8b6e-7b9e-41fa-acc0-866627bbdf8d)
 Call ID: 2a9a8b6e-7b9e-41fa-acc0-866627bbdf8d
  Args:
    type: :Person
    source: :Karl_Prince_of_Leiningen
  AssignClass (56a40ce3-3d11-441f-b13b-c7271aae77d7)
 Call ID: 56a40ce3-3d11-441f-b13b-c7271aae77d7
  Args:
    type: :Ancestor
    source: :Karl_Prince_of_Leiningen
  AddLiteral (f560d528-11f6-4e1c-a594-d8fb846b6b64)
 Call ID: f560d528-11f6-4e1c-a594-d8fb846b6b64
  Args:
    relation: :hasBirthYear
    literal_value: 1898
    source: :Karl_Prince_of_Leiningen
    literal_type: xsd:integer
  AddLiteral (ef8939de-83b5-46e2-ab1d-827f90bf1cc3)
 Call ID: ef8939de-83b5-46e2-ab1d-827f90bf1cc3
  Args:
    relation: :hasDeathYear
    literal_value: 1946
    source: :Karl_Prince_of_Leiningen
    literal_type: xsd:integer
  AddLiteral (529a9661-2548-418b-ba12-58948365db60)
 Call ID: 529a9661-2548-418b-ba12-58948365db60
  Args:
    literal_type: xsd:integer
    source: :Maria_Kirillovna_of_Russia
    relation: :hasMarriageYear
    literal_value: 1925
  AssignClass (77f04854-eb74-4e1d-b88f-1b893261575b)
 Call ID: 77f04854-eb74-4e1d-b88f-1b893261575b
  Args:
    type: :Man
    source: :Emich_Kirill
  AssignClass (c033061a-713d-4ba9-a7e9-9a1034b732a1)
 Call ID: c033061a-713d-4ba9-a7e9-9a1034b732a1
  Args:
    type: :Person
    source: :Emich_Kirill
  AddTriple (9a21bf5b-eeb4-41f2-867c-1f3d3e8b21f5)
 Call ID: 9a21bf5b-eeb4-41f2-867c-1f3d3e8b21f5
  Args:
    relation: :hasFather
    target: :Karl_Prince_of_Leiningen
    source: :Emich_Kirill
  AddTriple (96812af4-0922-4c3a-b0a1-c15c0c08d8fa)
 Call ID: 96812af4-0922-4c3a-b0a1-c15c0c08d8fa
  Args:
    target: :Maria_Kirillovna_of_Russia
    relation: :hasMother
    source: :Emich_Kirill
  AssignClass (19db2c12-7445-4f9a-b72b-12e06c611830)
 Call ID: 19db2c12-7445-4f9a-b72b-12e06c611830
  Args:
    source: :Queen_Victoria
    type: :Woman
  AssignClass (3105a2a8-da82-4da9-a2b2-5eb61925e632)
 Call ID: 3105a2a8-da82-4da9-a2b2-5eb61925e632
  Args:
    type: :Person
    source: :Queen_Victoria
  AssignClass (163b45da-a43c-46eb-a9c1-11ad5a4a730b)
 Call ID: 163b45da-a43c-46eb-a9c1-11ad5a4a730b
  Args:
    type: :Ancestor
    source: :Queen_Victoria
  AssignClass (f699f6f5-ec29-4188-a9fd-ae692bbf8eb1)
 Call ID: f699f6f5-ec29-4188-a9fd-ae692bbf8eb1
  Args:
    type: :Man
    source: :Carl_GreatGrandfather_Karl
  AssignClass (885d6b88-0c91-4dad-a73e-d2e20e148cfd)
 Call ID: 885d6b88-0c91-4dad-a73e-d2e20e148cfd
  Args:
    source: :Carl_GreatGrandfather_Karl
    type: :Person
  AssignClass (3f014a20-91c1-4a21-9375-9ef76f944c8e)
 Call ID: 3f014a20-91c1-4a21-9375-9ef76f944c8e
  Args:
    type: :Ancestor
    source: :Carl_GreatGrandfather_Karl
  Finish (658fe1e0-fd7b-483c-8f7f-f9d7c1f72b7b)
 Call ID: 658fe1e0-fd7b-483c-8f7f-f9d7c1f72b7b
  Args: