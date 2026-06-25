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
  AssignClass (b29b5cdf-7c33-4462-af79-a50018a70787)
 Call ID: b29b5cdf-7c33-4462-af79-a50018a70787
  Args:
    source: Maria_Kirillovna_of_Russia
    type: :Woman
  AssignClass (cd2ae8df-f1bd-4589-9e09-40a05cbaeb61)
 Call ID: cd2ae8df-f1bd-4589-9e09-40a05cbaeb61
  Args:
    source: Maria_Kirillovna_of_Russia
    type: :Person
  AddLiteral (1f1eacb7-7e60-4778-85d0-60676e7050aa)
 Call ID: 1f1eacb7-7e60-4778-85d0-60676e7050aa
  Args:
    literal_type: xsd:integer
    source: Maria_Kirillovna_of_Russia
    literal_value: 1907
    relation: :hasBirthYear
  AddLiteral (5aa00a97-f279-4f0d-a516-b7c46a53607d)
 Call ID: 5aa00a97-f279-4f0d-a516-b7c46a53607d
  Args:
    source: Maria_Kirillovna_of_Russia
    literal_value: 1951
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (cfa0a99e-6559-41b4-829a-70987443cedf)
 Call ID: cfa0a99e-6559-41b4-829a-70987443cedf
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Man
  AssignClass (2fa037ee-f26c-4b7d-b23d-073affab664c)
 Call ID: 2fa037ee-f26c-4b7d-b23d-073affab664c
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Person
  AssignClass (a2eaa2a5-ff5e-4a16-b964-b43e10fe4d62)
 Call ID: a2eaa2a5-ff5e-4a16-b964-b43e10fe4d62
  Args:
    source: Victoria_Melita_of_Edinburgh
    type: :Woman
  AssignClass (2201a3a6-e49a-43ba-a76a-7eea8cda1f13)
 Call ID: 2201a3a6-e49a-43ba-a76a-7eea8cda1f13
  Args:
    source: Victoria_Melita_of_Edinburgh
    type: :Person
  AddTriple (48143820-aa2b-421a-ba40-3559e852165f)
 Call ID: 48143820-aa2b-421a-ba40-3559e852165f
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Kirill_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (f8437403-7664-47d3-a43a-5adde798020c)
 Call ID: f8437403-7664-47d3-a43a-5adde798020c
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Victoria_Melita_of_Edinburgh
    relation: :hasMother
  AssignClass (6068b764-278b-4186-9c56-2c8e6b771fb9)
 Call ID: 6068b764-278b-4186-9c56-2c8e6b771fb9
  Args:
    source: Maria_Alexandrovna_of_Russia
    type: :Woman
  AssignClass (fc7db0ee-626a-40f0-8fc1-ddef27db007e)
 Call ID: fc7db0ee-626a-40f0-8fc1-ddef27db007e
  Args:
    source: Maria_Alexandrovna_of_Russia
    type: :Person
  AddTriple (bb6d50a3-3e43-4968-b576-dd9dc8de8811)
 Call ID: bb6d50a3-3e43-4968-b576-dd9dc8de8811
  Args:
    source: Victoria_Melita_of_Edinburgh
    relation: :hasMother
    target: Maria_Alexandrovna_of_Russia
  AssignClass (6cc87bc2-75ca-4515-a03d-5ee5e8040248)
 Call ID: 6cc87bc2-75ca-4515-a03d-5ee5e8040248
  Args:
    source: Marie_of_Romania
    type: :Woman
  AssignClass (b12ead02-8d94-4a66-b574-8a29e84325e1)
 Call ID: b12ead02-8d94-4a66-b574-8a29e84325e1
  Args:
    source: Marie_of_Romania
    type: :Person
  AddTriple (de30ceb7-d597-44db-816a-4e9f8a1ab4b6)
 Call ID: de30ceb7-d597-44db-816a-4e9f8a1ab4b6
  Args:
    source: Maria_Kirillovna_of_Russia
    relation: :hasRelation
    target: Marie_of_Romania
  AssignClass (07af1682-407f-4045-8d44-d28b9583ef59)
 Call ID: 07af1682-407f-4045-8d44-d28b9583ef59
  Args:
    source: Ileana_of_Romania
    type: :Woman
  AssignClass (b7aee71a-8fdd-4d4e-a5c1-ac97d9665127)
 Call ID: b7aee71a-8fdd-4d4e-a5c1-ac97d9665127
  Args:
    source: Ileana_of_Romania
    type: :Person
  AddTriple (79d7012a-e43c-498d-a261-0c90cebc1352)
 Call ID: 79d7012a-e43c-498d-a261-0c90cebc1352
  Args:
    relation: :isSiblingOf
    target: Ileana_of_Romania
    source: Maria_Kirillovna_of_Russia
  AssignClass (5a5980e3-f89c-45ec-b93a-9bb37c4c3596)
 Call ID: 5a5980e3-f89c-45ec-b93a-9bb37c4c3596
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Man
  AssignClass (a48a8d70-c09c-4614-bc7b-286d7430c42a)
 Call ID: a48a8d70-c09c-4614-bc7b-286d7430c42a
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Person
  AddLiteral (04cf1831-2d90-4a83-9e68-80975de2fb37)
 Call ID: 04cf1831-2d90-4a83-9e68-80975de2fb37
  Args:
    source: Karl_6th_Prince_of_Leiningen
    literal_value: 1898
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (914963e4-cdc4-4644-b960-ce2f0ac80889)
 Call ID: 914963e4-cdc4-4644-b960-ce2f0ac80889
  Args:
    literal_type: xsd:integer
    literal_value: 1946
    source: Karl_6th_Prince_of_Leiningen
    relation: :hasDeathYear
  AddLiteral (c6eb3cb0-b97b-4e5b-96ab-eab31546c811)
 Call ID: c6eb3cb0-b97b-4e5b-96ab-eab31546c811
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Maria_Kirillovna_of_Russia
    literal_value: 1925
  AssignClass (8966e4b5-f9e3-4321-85fd-1abefdd75c9e)
 Call ID: 8966e4b5-f9e3-4321-85fd-1abefdd75c9e
  Args:
    source: Emich_Kirill
    type: :Man
  AssignClass (08a0d627-9201-4b42-ae4d-9fc749998555)
 Call ID: 08a0d627-9201-4b42-ae4d-9fc749998555
  Args:
    source: Emich_Kirill
    type: :Person
  AddTriple (cb23c2ef-01b2-47aa-894c-8418566ccf20)
 Call ID: cb23c2ef-01b2-47aa-894c-8418566ccf20
  Args:
    relation: :hasFather
    target: Karl_6th_Prince_of_Leiningen
    source: Emich_Kirill
  AddTriple (0a2c6fc5-d14d-448b-b4f2-f3f9f6d35df2)
 Call ID: 0a2c6fc5-d14d-448b-b4f2-f3f9f6d35df2
  Args:
    source: Emich_Kirill
    relation: :hasMother
    target: Maria_Kirillovna_of_Russia
  AddLiteral (9d668d0b-e4bf-49d5-8134-dc4eb07a755b)
 Call ID: 9d668d0b-e4bf-49d5-8134-dc4eb07a755b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1926
    source: Emich_Kirill
  AssignClass (a7dfc281-2c23-4871-a9fd-656998d4284e)
 Call ID: a7dfc281-2c23-4871-a9fd-656998d4284e
  Args:
    source: Carl_of_Leiningen
    type: :Man
  AssignClass (34840c76-67b6-409d-95ac-acb0556d8951)
 Call ID: 34840c76-67b6-409d-95ac-acb0556d8951
  Args:
    source: Carl_of_Leiningen
    type: :Person
  AssignClass (37c739df-c666-4210-8c0a-1bbe1a821534)
 Call ID: 37c739df-c666-4210-8c0a-1bbe1a821534
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (bf368d47-5e49-48bb-b720-e21aff9dbde6)
 Call ID: bf368d47-5e49-48bb-b720-e21aff9dbde6
  Args:
    source: Queen_Victoria
    type: :Person
  Finish (ddad71f0-8a1d-4c3c-aad9-8b7039d6b219)
 Call ID: ddad71f0-8a1d-4c3c-aad9-8b7039d6b219
  Args: