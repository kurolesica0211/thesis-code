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
  AssignClass (f1de1902-0a9b-4f12-83c1-3b60ebd41acf)
 Call ID: f1de1902-0a9b-4f12-83c1-3b60ebd41acf
  Args:
    type: :Person
    source: Maria_Kirillovna_of_Russia
  AssignClass (ce0c360c-2f0c-4dca-8ef0-f7c2289a37a7)
 Call ID: ce0c360c-2f0c-4dca-8ef0-f7c2289a37a7
  Args:
    type: :Woman
    source: Maria_Kirillovna_of_Russia
  AddLiteral (125913d1-ba2d-4644-a048-5de851f018a8)
 Call ID: 125913d1-ba2d-4644-a048-5de851f018a8
  Args:
    literal_value: 1907
    source: Maria_Kirillovna_of_Russia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (a13933fb-84ef-4b78-b6df-2dfc5e71f934)
 Call ID: a13933fb-84ef-4b78-b6df-2dfc5e71f934
  Args:
    source: Maria_Kirillovna_of_Russia
    literal_value: 1951
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (7382c29d-6995-4204-a0e7-6b1d9b190d3b)
 Call ID: 7382c29d-6995-4204-a0e7-6b1d9b190d3b
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Person
  AssignClass (fb1b2982-b2b9-46d9-b9d4-348b75ef2ea6)
 Call ID: fb1b2982-b2b9-46d9-b9d4-348b75ef2ea6
  Args:
    type: :Man
    source: Kirill_Vladimirovich_of_Russia
  AssignClass (670f1203-d047-42b0-ae6b-6adc38e90c65)
 Call ID: 670f1203-d047-42b0-ae6b-6adc38e90c65
  Args:
    type: :Person
    source: Victoria_Melita_of_Edinburgh
  AssignClass (2d811789-de90-4977-9728-807e332c3b8c)
 Call ID: 2d811789-de90-4977-9728-807e332c3b8c
  Args:
    type: :Woman
    source: Victoria_Melita_of_Edinburgh
  AddTriple (808ad2ab-0456-42c6-b8ba-bc0133b5e24c)
 Call ID: 808ad2ab-0456-42c6-b8ba-bc0133b5e24c
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Kirill_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (25b12ff6-6700-4612-ba88-9c842c89d15c)
 Call ID: 25b12ff6-6700-4612-ba88-9c842c89d15c
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Victoria_Melita_of_Edinburgh
    relation: :hasMother
  AssignClass (f7915712-de34-4718-a2f8-c501ce3d5fdb)
 Call ID: f7915712-de34-4718-a2f8-c501ce3d5fdb
  Args:
    type: :Person
    source: Karl_6th_Prince_of_Leiningen
  AssignClass (59778d49-763f-4041-80f9-cb786edbb3d8)
 Call ID: 59778d49-763f-4041-80f9-cb786edbb3d8
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Man
  AddLiteral (9d05fe87-fc4d-4f01-87f9-a4e35f68cda2)
 Call ID: 9d05fe87-fc4d-4f01-87f9-a4e35f68cda2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Karl_6th_Prince_of_Leiningen
    literal_value: 1898
  AddLiteral (8f916291-b888-4862-ac81-e75c99ae1701)
 Call ID: 8f916291-b888-4862-ac81-e75c99ae1701
  Args:
    relation: :hasDeathYear
    source: Karl_6th_Prince_of_Leiningen
    literal_value: 1946
    literal_type: xsd:integer
  AddLiteral (64a1ce0b-da26-4f55-98a1-af1435145114)
 Call ID: 64a1ce0b-da26-4f55-98a1-af1435145114
  Args:
    relation: :hasMarriageYear
    literal_value: 1925
    source: Maria_Kirillovna_of_Russia
    literal_type: xsd:integer
  AddTriple (0964c649-746f-4df7-99ae-a903dd1c3eca)
 Call ID: 0964c649-746f-4df7-99ae-a903dd1c3eca
  Args:
    relation: :hasRelation
    source: Maria_Kirillovna_of_Russia
    target: Karl_6th_Prince_of_Leiningen
  AssignClass (caf2b285-3d94-4cbd-92f7-70f82e7ada1d)
 Call ID: caf2b285-3d94-4cbd-92f7-70f82e7ada1d
  Args:
    source: Emich_Kirill
    type: :Person
  AssignClass (9e0758ee-960d-4e04-940f-bfc43799bbbc)
 Call ID: 9e0758ee-960d-4e04-940f-bfc43799bbbc
  Args:
    source: Emich_Kirill
    type: :Man
  AddTriple (b86ab2a0-acf1-43ef-9e4e-e1963b0b3ad2)
 Call ID: b86ab2a0-acf1-43ef-9e4e-e1963b0b3ad2
  Args:
    relation: :isChildOf
    target: Maria_Kirillovna_of_Russia
    source: Emich_Kirill
  AddTriple (befe7c88-6fb5-4ecd-88cd-15e551982b4e)
 Call ID: befe7c88-6fb5-4ecd-88cd-15e551982b4e
  Args:
    relation: :isChildOf
    target: Karl_6th_Prince_of_Leiningen
    source: Emich_Kirill
  AssignClass (f4374bf9-9826-4948-b86e-d6b8c497420d)
 Call ID: f4374bf9-9826-4948-b86e-d6b8c497420d
  Args:
    type: :Person
    source: Maria_Alexandrovna_of_Russia
  AssignClass (98912c8a-09b1-4670-8406-1635c65a3d57)
 Call ID: 98912c8a-09b1-4670-8406-1635c65a3d57
  Args:
    type: :Woman
    source: Maria_Alexandrovna_of_Russia
  AssignClass (9c446901-8d76-47ea-8743-e5cf5939a6e2)
 Call ID: 9c446901-8d76-47ea-8743-e5cf5939a6e2
  Args:
    source: Marie_of_Romania
    type: :Person
  AssignClass (b7208b35-b1cb-4673-ad42-f9fdfcabb236)
 Call ID: b7208b35-b1cb-4673-ad42-f9fdfcabb236
  Args:
    source: Marie_of_Romania
    type: :Woman
  AssignClass (557ae290-9a06-49f6-bcf6-e6c82acf2d90)
 Call ID: 557ae290-9a06-49f6-bcf6-e6c82acf2d90
  Args:
    source: Ileana_of_Romania
    type: :Person
  AssignClass (aa06879c-c7a4-4187-b39d-350e784e2550)
 Call ID: aa06879c-c7a4-4187-b39d-350e784e2550
  Args:
    source: Ileana_of_Romania
    type: :Woman
  Finish (2abfac04-2621-4da3-ac3f-9a95a27b861c)
 Call ID: 2abfac04-2621-4da3-ac3f-9a95a27b861c
  Args: