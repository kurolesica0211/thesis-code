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
  AssignClass (eeaecf2d-5a4e-47ab-af32-cf19af519398)
 Call ID: eeaecf2d-5a4e-47ab-af32-cf19af519398
  Args:
    type: :Woman
    source: Maria_Kirillovna
  AssignClass (99b15346-72e8-43a1-a75d-86ba9bca2613)
 Call ID: 99b15346-72e8-43a1-a75d-86ba9bca2613
  Args:
    source: Maria_Kirillovna
    type: :Person
  AddLiteral (7db9dde2-3d52-4662-9ad4-d78a3a36fd42)
 Call ID: 7db9dde2-3d52-4662-9ad4-d78a3a36fd42
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Maria_Kirillovna
    literal_value: 1907
  AddLiteral (e1dd5a2c-0430-48c8-a2cb-1c88b264a023)
 Call ID: e1dd5a2c-0430-48c8-a2cb-1c88b264a023
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1951
    source: Maria_Kirillovna
  AssignClass (a153c87c-9258-4e58-b01c-98464d7f083e)
 Call ID: a153c87c-9258-4e58-b01c-98464d7f083e
  Args:
    source: Kirill_Vladimirovich
    type: :Man
  AssignClass (5ef1d69c-0eec-48d1-b60a-b81ac43adc76)
 Call ID: 5ef1d69c-0eec-48d1-b60a-b81ac43adc76
  Args:
    type: :Person
    source: Kirill_Vladimirovich
  AssignClass (557c5d59-c2f6-4340-8775-1609be76e3ae)
 Call ID: 557c5d59-c2f6-4340-8775-1609be76e3ae
  Args:
    type: :Woman
    source: Victoria_Melita
  AssignClass (5b2d6cbb-0eac-4de3-86fe-e6ab6a9aa960)
 Call ID: 5b2d6cbb-0eac-4de3-86fe-e6ab6a9aa960
  Args:
    source: Victoria_Melita
    type: :Person
  AddTriple (71a35275-7234-4aca-8fc3-966c80061fd0)
 Call ID: 71a35275-7234-4aca-8fc3-966c80061fd0
  Args:
    target: Kirill_Vladimirovich
    relation: :hasFather
    source: Maria_Kirillovna
  AddTriple (07b79503-b031-4c52-9c2c-00c4a8d09dcc)
 Call ID: 07b79503-b031-4c52-9c2c-00c4a8d09dcc
  Args:
    source: Maria_Kirillovna
    target: Victoria_Melita
    relation: :hasMother
  AssignClass (3171fcba-2cdd-49a9-9989-f68caba30e2b)
 Call ID: 3171fcba-2cdd-49a9-9989-f68caba30e2b
  Args:
    source: Maria_Alexandrovna
    type: :Woman
  AssignClass (db321ab6-2b30-4d43-a3cc-3ab9451fb5ff)
 Call ID: db321ab6-2b30-4d43-a3cc-3ab9451fb5ff
  Args:
    source: Maria_Alexandrovna
    type: :Person
  AssignClass (b03ff240-a1e0-44ad-92c2-c17ede2b9583)
 Call ID: b03ff240-a1e0-44ad-92c2-c17ede2b9583
  Args:
    source: Marie_of_Romania
    type: :Woman
  AssignClass (ae94f288-670d-4621-8104-b6d89e4e7fff)
 Call ID: ae94f288-670d-4621-8104-b6d89e4e7fff
  Args:
    source: Marie_of_Romania
    type: :Person
  AssignClass (ce32c52f-aca5-46ee-bfd5-5e7b3dcef517)
 Call ID: ce32c52f-aca5-46ee-bfd5-5e7b3dcef517
  Args:
    type: :Woman
    source: Ileana_of_Romania
  AssignClass (89c6965d-7032-4285-974d-08381b2b347a)
 Call ID: 89c6965d-7032-4285-974d-08381b2b347a
  Args:
    type: :Person
    source: Ileana_of_Romania
  AssignClass (be65a081-167e-46f6-8b4d-cb38f52ff1d5)
 Call ID: be65a081-167e-46f6-8b4d-cb38f52ff1d5
  Args:
    source: Karl_of_Leiningen
    type: :Man
  AssignClass (3f953253-27e8-4a61-bf3c-e3e76a27e8f2)
 Call ID: 3f953253-27e8-4a61-bf3c-e3e76a27e8f2
  Args:
    source: Karl_of_Leiningen
    type: :Person
  AddLiteral (0884345e-9e15-4bf5-a739-0c68796804bd)
 Call ID: 0884345e-9e15-4bf5-a739-0c68796804bd
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Karl_of_Leiningen
    literal_value: 1898
  AddLiteral (ea525036-486c-4203-83be-024877edfd49)
 Call ID: ea525036-486c-4203-83be-024877edfd49
  Args:
    literal_value: 1946
    source: Karl_of_Leiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (e87841f1-e716-4a4f-adca-a5b7776d438a)
 Call ID: e87841f1-e716-4a4f-adca-a5b7776d438a
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Maria_Kirillovna
    literal_value: 1925
  AddTriple (be83c0b4-d8af-4fe5-a9c4-a0235fa43cef)
 Call ID: be83c0b4-d8af-4fe5-a9c4-a0235fa43cef
  Args:
    source: Maria_Kirillovna
    target: Karl_of_Leiningen
    relation: :hasRelation
  AssignClass (9a8d6c20-cce4-4688-a298-f761fecd534a)
 Call ID: 9a8d6c20-cce4-4688-a298-f761fecd534a
  Args:
    source: Emich_Kirill
    type: :Man
  AssignClass (51dff6b7-18e0-4c98-9cf3-7325cd0db39d)
 Call ID: 51dff6b7-18e0-4c98-9cf3-7325cd0db39d
  Args:
    source: Emich_Kirill
    type: :Person
  AddTriple (0b544b64-c4a4-4cab-9e25-34015613ce99)
 Call ID: 0b544b64-c4a4-4cab-9e25-34015613ce99
  Args:
    relation: :hasFather
    target: Karl_of_Leiningen
    source: Emich_Kirill
  AddTriple (7dcfd5b1-b148-48ac-92b1-1d60e922980d)
 Call ID: 7dcfd5b1-b148-48ac-92b1-1d60e922980d
  Args:
    source: Emich_Kirill
    relation: :hasMother
    target: Maria_Kirillovna
  AssignClass (64a163b7-fc2b-4ec7-a312-7c897b256cc4)
 Call ID: 64a163b7-fc2b-4ec7-a312-7c897b256cc4
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (f2ec29db-0383-4f02-bd12-23c900ed7f5e)
 Call ID: f2ec29db-0383-4f02-bd12-23c900ed7f5e
  Args:
    source: Queen_Victoria
    type: :Person
  AssignClass (054d519e-78dc-478a-8449-ea1af5da4358)
 Call ID: 054d519e-78dc-478a-8449-ea1af5da4358
  Args:
    source: Carl_of_Leiningen
    type: :Man
  AssignClass (9d2a4012-f5a9-4c8f-88e6-cb3f27023b68)
 Call ID: 9d2a4012-f5a9-4c8f-88e6-cb3f27023b68
  Args:
    source: Carl_of_Leiningen
    type: :Person
  Finish (9edef324-3fab-4142-938c-cc972fac38c6)
 Call ID: 9edef324-3fab-4142-938c-cc972fac38c6
  Args: