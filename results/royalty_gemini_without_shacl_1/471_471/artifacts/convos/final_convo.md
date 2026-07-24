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
  AssignClass (51cbf28b-5675-4979-8eab-7123fbbe67a3)
 Call ID: 51cbf28b-5675-4979-8eab-7123fbbe67a3
  Args:
    type: :Woman
    source: :Maria_Kirillovna_of_Russia
  AssignClass (6df7ce4b-b72f-4dce-a3fd-dae8f451fe0a)
 Call ID: 6df7ce4b-b72f-4dce-a3fd-dae8f451fe0a
  Args:
    type: :Person
    source: :Maria_Kirillovna_of_Russia
  AddLiteral (71c04e6e-ed9d-4916-9bf5-6a9d792b0426)
 Call ID: 71c04e6e-ed9d-4916-9bf5-6a9d792b0426
  Args:
    source: :Maria_Kirillovna_of_Russia
    literal_value: 1907
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d57f6a05-74f1-4a65-9866-a290dc46d50b)
 Call ID: d57f6a05-74f1-4a65-9866-a290dc46d50b
  Args:
    source: :Maria_Kirillovna_of_Russia
    literal_value: 1951
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (7bc67317-4749-4546-8ae4-7955b40f7606)
 Call ID: 7bc67317-4749-4546-8ae4-7955b40f7606
  Args:
    type: :Man
    source: :Kirill_Vladimirovich_of_Russia
  AssignClass (ba4e7ce0-1397-42b8-89a6-e1c444c32bda)
 Call ID: ba4e7ce0-1397-42b8-89a6-e1c444c32bda
  Args:
    type: :Ancestor
    source: :Kirill_Vladimirovich_of_Russia
  AssignClass (5da50c72-abf1-411f-a332-ec4dc8937d4e)
 Call ID: 5da50c72-abf1-411f-a332-ec4dc8937d4e
  Args:
    type: :Person
    source: :Kirill_Vladimirovich_of_Russia
  AssignClass (4d388715-7c6f-4e21-825e-3b73b45d1cf1)
 Call ID: 4d388715-7c6f-4e21-825e-3b73b45d1cf1
  Args:
    type: :Woman
    source: :Victoria_Melita_of_Edinburgh
  AssignClass (7b935423-f6f9-4444-bcc4-441e9c7debd7)
 Call ID: 7b935423-f6f9-4444-bcc4-441e9c7debd7
  Args:
    type: :Ancestor
    source: :Victoria_Melita_of_Edinburgh
  AssignClass (6715fa89-ef0f-4d01-a133-5090639ae09e)
 Call ID: 6715fa89-ef0f-4d01-a133-5090639ae09e
  Args:
    type: :Person
    source: :Victoria_Melita_of_Edinburgh
  AddTriple (0f70facc-98ad-41aa-8913-42aa07fc6277)
 Call ID: 0f70facc-98ad-41aa-8913-42aa07fc6277
  Args:
    source: :Maria_Kirillovna_of_Russia
    target: :Kirill_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (87497e0c-ea76-4b82-ae11-d3c6ca787e44)
 Call ID: 87497e0c-ea76-4b82-ae11-d3c6ca787e44
  Args:
    source: :Maria_Kirillovna_of_Russia
    target: :Victoria_Melita_of_Edinburgh
    relation: :hasMother
  AssignClass (99dbe20e-683e-4005-9eac-21faf6e98a32)
 Call ID: 99dbe20e-683e-4005-9eac-21faf6e98a32
  Args:
    type: :Woman
    source: :Maria_Alexandrovna_of_Russia
  AssignClass (51482990-9159-42d7-b2a1-af39bec0ccdd)
 Call ID: 51482990-9159-42d7-b2a1-af39bec0ccdd
  Args:
    type: :Ancestor
    source: :Maria_Alexandrovna_of_Russia
  AssignClass (85a7ff13-4450-4901-990d-7a4eea59159e)
 Call ID: 85a7ff13-4450-4901-990d-7a4eea59159e
  Args:
    type: :Person
    source: :Maria_Alexandrovna_of_Russia
  AssignClass (8edee20c-6e35-4664-a26c-3ec405b495ed)
 Call ID: 8edee20c-6e35-4664-a26c-3ec405b495ed
  Args:
    type: :Woman
    source: :Marie_of_Romania
  AssignClass (b55266a8-a3c5-4f7c-aaab-6a2776be02b1)
 Call ID: b55266a8-a3c5-4f7c-aaab-6a2776be02b1
  Args:
    type: :Ancestor
    source: :Marie_of_Romania
  AssignClass (e4f94950-b194-4d4a-b885-7dd9fb8ca2d7)
 Call ID: e4f94950-b194-4d4a-b885-7dd9fb8ca2d7
  Args:
    type: :Person
    source: :Marie_of_Romania
  AssignClass (79e54f77-7f27-4528-b114-7840a6a84bfe)
 Call ID: 79e54f77-7f27-4528-b114-7840a6a84bfe
  Args:
    type: :Woman
    source: :Ileana_of_Romania
  AssignClass (f1f73b17-41a5-4329-9acc-3349d6540848)
 Call ID: f1f73b17-41a5-4329-9acc-3349d6540848
  Args:
    type: :Person
    source: :Ileana_of_Romania
  AssignClass (6b99eb9e-77cd-4fa6-a669-070c754a618c)
 Call ID: 6b99eb9e-77cd-4fa6-a669-070c754a618c
  Args:
    type: :Man
    source: :Karl_6th_Prince_of_Leiningen
  AssignClass (5440f7ac-18ea-4212-b027-1c9f50dcd454)
 Call ID: 5440f7ac-18ea-4212-b027-1c9f50dcd454
  Args:
    type: :Ancestor
    source: :Karl_6th_Prince_of_Leiningen
  AssignClass (ba08d310-2608-4fad-9b55-1e795a9eaf18)
 Call ID: ba08d310-2608-4fad-9b55-1e795a9eaf18
  Args:
    type: :Person
    source: :Karl_6th_Prince_of_Leiningen
  AddLiteral (88dfdde9-8b7f-4eba-932e-19ec67157e12)
 Call ID: 88dfdde9-8b7f-4eba-932e-19ec67157e12
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1898
    source: :Karl_6th_Prince_of_Leiningen
  AddLiteral (f376e728-c2b1-45b2-8d9b-9da123abbbdb)
 Call ID: f376e728-c2b1-45b2-8d9b-9da123abbbdb
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1946
    source: :Karl_6th_Prince_of_Leiningen
  AddLiteral (a9243ff3-471b-42f0-aeb3-e7e60830c807)
 Call ID: a9243ff3-471b-42f0-aeb3-e7e60830c807
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Maria_Kirillovna_of_Russia
    literal_value: 1925
  AddTriple (e0c7c9b7-84dd-4fda-baa5-4db25fddde49)
 Call ID: e0c7c9b7-84dd-4fda-baa5-4db25fddde49
  Args:
    source: :Maria_Kirillovna_of_Russia
    target: :Karl_6th_Prince_of_Leiningen
    relation: :hasRelation
  AssignClass (7ee9cb0c-770a-4c9f-a6ca-aae850acdcd5)
 Call ID: 7ee9cb0c-770a-4c9f-a6ca-aae850acdcd5
  Args:
    type: :Man
    source: :Emich_Kirill_of_Leiningen
  AssignClass (04c5e39a-b802-44d7-bf33-73a58b10264c)
 Call ID: 04c5e39a-b802-44d7-bf33-73a58b10264c
  Args:
    type: :Person
    source: :Emich_Kirill_of_Leiningen
  AddTriple (1485fe75-6388-4797-9d8a-7302e3bbec6b)
 Call ID: 1485fe75-6388-4797-9d8a-7302e3bbec6b
  Args:
    relation: :hasFather
    source: :Emich_Kirill_of_Leiningen
    target: :Karl_6th_Prince_of_Leiningen
  AddTriple (84522e6d-f336-47a3-a112-586dd21691e0)
 Call ID: 84522e6d-f336-47a3-a112-586dd21691e0
  Args:
    relation: :hasMother
    source: :Emich_Kirill_of_Leiningen
    target: :Maria_Kirillovna_of_Russia
  AssignClass (d329165b-227e-4a0b-82f1-dced724431a7)
 Call ID: d329165b-227e-4a0b-82f1-dced724431a7
  Args:
    type: :Man
    source: :Carl_of_Leiningen
  AssignClass (d7b874d3-6f35-4f73-88c4-412ffd7d0c8a)
 Call ID: d7b874d3-6f35-4f73-88c4-412ffd7d0c8a
  Args:
    type: :Ancestor
    source: :Carl_of_Leiningen
  AssignClass (0f0cbadf-ea0c-4ff7-98cd-46b17a15236b)
 Call ID: 0f0cbadf-ea0c-4ff7-98cd-46b17a15236b
  Args:
    type: :Person
    source: :Carl_of_Leiningen
  AssignClass (1d3d1037-a3c8-450e-8001-c1487985a9e2)
 Call ID: 1d3d1037-a3c8-450e-8001-c1487985a9e2
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (d80b7999-91e4-47e4-aa2b-c200b66c0fb4)
 Call ID: d80b7999-91e4-47e4-aa2b-c200b66c0fb4
  Args:
    type: :Ancestor
    source: :Queen_Victoria
  AssignClass (b2053f07-9c54-4497-b9af-4cb91bacb3f9)
 Call ID: b2053f07-9c54-4497-b9af-4cb91bacb3f9
  Args:
    type: :Person
    source: :Queen_Victoria
  Finish (adf64436-5443-4326-bd3d-a69551134f0e)
 Call ID: adf64436-5443-4326-bd3d-a69551134f0e
  Args: