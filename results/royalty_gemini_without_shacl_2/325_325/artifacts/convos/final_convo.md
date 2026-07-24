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
Emich Kyrill, Prince of Leiningen (German: Emich Kirill Ferdinand Hermann Fürst zu Leiningen; 18 October 1926 – 30 October 1991) was a German entrepreneur and son of Karl, Prince of Leiningen.
Early life

Emich was born at Coburg, Weimar Republic, the first child of Karl, Prince of Leiningen (1898–1946), (son of Emich, 5th Prince of Leiningen and Princess Feodore of Hohenlohe-Langenburg) and his wife, Grand Duchess Maria Kirillovna of Russia (1907–1951), (daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh).
Through his mother, he was a descendant of Queen Victoria and Tsar Alexander II.
Through his father, he was a descendant of the Vasa kings of Sweden and of both of Queen Victoria's half-siblings, Carl, Prince of Leiningen and Feodora, Princess of Hohenlohe-Langenburg.
As a result, Emich was the first descendant of all three of Princess Victoria of Saxe-Coburg-Saalfeld's children.
Marriage

Emich married on 10 August 1950 in Rastede to Duchess Eilika of Oldenburg (2 February 1928 – 26 January 2016), fourth child and second daughter of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.



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
  AssignClass (b1b6202e-4da1-467e-82ce-022c4ffc4220)
 Call ID: b1b6202e-4da1-467e-82ce-022c4ffc4220
  Args:
    type: :Man
    source: Emich_Kyrill_Prince_of_Leiningen
  AssignClass (4194b19f-3fe9-431e-9158-30d26f0a72ae)
 Call ID: 4194b19f-3fe9-431e-9158-30d26f0a72ae
  Args:
    type: :Person
    source: Emich_Kyrill_Prince_of_Leiningen
  AddLiteral (6f9d001b-7678-41a2-bbff-d1775c073109)
 Call ID: 6f9d001b-7678-41a2-bbff-d1775c073109
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1926
  AddLiteral (9f9f8393-2388-4608-8af5-4b6084e7effd)
 Call ID: 9f9f8393-2388-4608-8af5-4b6084e7effd
  Args:
    literal_value: 1991
    literal_type: xsd:integer
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasDeathYear
  AssignClass (a9e3b81a-5e29-413b-b112-7a3017d62daf)
 Call ID: a9e3b81a-5e29-413b-b112-7a3017d62daf
  Args:
    type: :Man
    source: Karl_Prince_of_Leiningen
  AssignClass (df1ad01b-2af9-4eba-b323-c6511e25dd82)
 Call ID: df1ad01b-2af9-4eba-b323-c6511e25dd82
  Args:
    type: :Person
    source: Karl_Prince_of_Leiningen
  AddLiteral (1974bc6f-5f6c-4240-81ec-105d1a145229)
 Call ID: 1974bc6f-5f6c-4240-81ec-105d1a145229
  Args:
    source: Karl_Prince_of_Leiningen
    relation: :hasBirthYear
    literal_value: 1898
    literal_type: xsd:integer
  AddLiteral (0b88d3dd-19b6-4576-b297-b20415fe1047)
 Call ID: 0b88d3dd-19b6-4576-b297-b20415fe1047
  Args:
    source: Karl_Prince_of_Leiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1946
  AddTriple (516597a4-67ce-4e40-af2e-d814eba706b9)
 Call ID: 516597a4-67ce-4e40-af2e-d814eba706b9
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasFather
    target: Karl_Prince_of_Leiningen
  AssignClass (6ac9d107-9f47-4c4d-a79b-ce7e470fb774)
 Call ID: 6ac9d107-9f47-4c4d-a79b-ce7e470fb774
  Args:
    type: :Woman
    source: Maria_Kirillovna_of_Russia
  AssignClass (61e095e4-134f-41d6-a2df-422fd1c39521)
 Call ID: 61e095e4-134f-41d6-a2df-422fd1c39521
  Args:
    type: :Person
    source: Maria_Kirillovna_of_Russia
  AddLiteral (e42bc291-9ee3-40ba-b2c5-df087afe2582)
 Call ID: e42bc291-9ee3-40ba-b2c5-df087afe2582
  Args:
    source: Maria_Kirillovna_of_Russia
    relation: :hasBirthYear
    literal_value: 1907
    literal_type: xsd:integer
  AddLiteral (4dddaa4d-9b84-48c7-bdf2-305e8f8ffa22)
 Call ID: 4dddaa4d-9b84-48c7-bdf2-305e8f8ffa22
  Args:
    relation: :hasDeathYear
    source: Maria_Kirillovna_of_Russia
    literal_value: 1951
    literal_type: xsd:integer
  AddTriple (3f7b8b54-fa2f-4abe-8b28-eb9b856a9ed4)
 Call ID: 3f7b8b54-fa2f-4abe-8b28-eb9b856a9ed4
  Args:
    target: Maria_Kirillovna_of_Russia
    relation: :hasMother
    source: Emich_Kyrill_Prince_of_Leiningen
  AssignClass (6fe4ef85-c229-4624-a9e7-18bb6495eca6)
 Call ID: 6fe4ef85-c229-4624-a9e7-18bb6495eca6
  Args:
    type: :Man
    source: Emich_5th_Prince_of_Leiningen
  AssignClass (574abd53-b278-4471-bc0a-ab37b873e516)
 Call ID: 574abd53-b278-4471-bc0a-ab37b873e516
  Args:
    type: :Person
    source: Emich_5th_Prince_of_Leiningen
  AddTriple (b6dbb722-c7d5-4a6e-aed1-68cb03f119f8)
 Call ID: b6dbb722-c7d5-4a6e-aed1-68cb03f119f8
  Args:
    source: Karl_Prince_of_Leiningen
    relation: :hasFather
    target: Emich_5th_Prince_of_Leiningen
  AssignClass (ac9e564a-980c-49e3-861b-c5f1f4a5a752)
 Call ID: ac9e564a-980c-49e3-861b-c5f1f4a5a752
  Args:
    type: :Woman
    source: Princess_Feodore_of_Hohenlohe-Langenburg
  AssignClass (f7f3e6cd-161f-49fc-a274-3ba7a233fcf8)
 Call ID: f7f3e6cd-161f-49fc-a274-3ba7a233fcf8
  Args:
    type: :Person
    source: Princess_Feodore_of_Hohenlohe-Langenburg
  AddTriple (745fe2f8-3da1-4d0d-8677-c011ba949bfd)
 Call ID: 745fe2f8-3da1-4d0d-8677-c011ba949bfd
  Args:
    target: Princess_Feodore_of_Hohenlohe-Langenburg
    source: Karl_Prince_of_Leiningen
    relation: :hasMother
  AssignClass (578baafe-bddd-4af8-8124-756d8383cc8d)
 Call ID: 578baafe-bddd-4af8-8124-756d8383cc8d
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AssignClass (b42f7679-ca3b-4354-abad-0bddef007420)
 Call ID: b42f7679-ca3b-4354-abad-0bddef007420
  Args:
    type: :Person
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AddTriple (a19b298d-f27d-4939-987f-08778d38ac66)
 Call ID: a19b298d-f27d-4939-987f-08778d38ac66
  Args:
    target: Grand_Duke_Kirill_Vladimirovich_of_Russia
    relation: :hasFather
    source: Maria_Kirillovna_of_Russia
  AssignClass (4bff5375-6d1f-4cab-84ea-0ec0dfbe87c7)
 Call ID: 4bff5375-6d1f-4cab-84ea-0ec0dfbe87c7
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Edinburgh
  AssignClass (e86fea31-f3a0-4712-8891-6aed1883c0ed)
 Call ID: e86fea31-f3a0-4712-8891-6aed1883c0ed
  Args:
    type: :Person
    source: Princess_Victoria_Melita_of_Edinburgh
  AddTriple (0bbe485d-74c8-4f50-ac95-1cba7e154a75)
 Call ID: 0bbe485d-74c8-4f50-ac95-1cba7e154a75
  Args:
    relation: :hasMother
    source: Maria_Kirillovna_of_Russia
    target: Princess_Victoria_Melita_of_Edinburgh
  AssignClass (e963ffc5-9cd6-46ac-bd14-3d7fde2280f0)
 Call ID: e963ffc5-9cd6-46ac-bd14-3d7fde2280f0
  Args:
    type: :Woman
    source: Duchess_Eilika_of_Oldenburg
  AssignClass (e61b6b9f-81b1-4f0b-870e-97537e90f14e)
 Call ID: e61b6b9f-81b1-4f0b-870e-97537e90f14e
  Args:
    type: :Person
    source: Duchess_Eilika_of_Oldenburg
  AddLiteral (eba5fc5d-cded-4688-968e-3216f162c223)
 Call ID: eba5fc5d-cded-4688-968e-3216f162c223
  Args:
    literal_type: xsd:integer
    literal_value: 1928
    source: Duchess_Eilika_of_Oldenburg
    relation: :hasBirthYear
  AddLiteral (635608bc-8f26-43ab-bfae-c0b7772278c8)
 Call ID: 635608bc-8f26-43ab-bfae-c0b7772278c8
  Args:
    literal_value: 2016
    literal_type: xsd:integer
    source: Duchess_Eilika_of_Oldenburg
    relation: :hasDeathYear
  AddLiteral (9b1b4b11-fc21-495d-bdab-65e26ad52105)
 Call ID: 9b1b4b11-fc21-495d-bdab-65e26ad52105
  Args:
    literal_type: xsd:integer
    literal_value: 1950
    relation: :hasMarriageYear
    source: Emich_Kyrill_Prince_of_Leiningen
  AddTriple (89f6ae48-0507-4a83-9a7f-83728299b762)
 Call ID: 89f6ae48-0507-4a83-9a7f-83728299b762
  Args:
    relation: :hasRelation
    source: Emich_Kyrill_Prince_of_Leiningen
    target: Duchess_Eilika_of_Oldenburg
  AssignClass (6f45bfb2-903d-430c-a14b-e08c5c16f8bc)
 Call ID: 6f45bfb2-903d-430c-a14b-e08c5c16f8bc
  Args:
    type: :Man
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
  AssignClass (f13eda0a-3b17-42cc-a6be-4e3bc6367089)
 Call ID: f13eda0a-3b17-42cc-a6be-4e3bc6367089
  Args:
    type: :Person
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
  AddTriple (270fa577-2854-46bc-b60f-647ceeb86e38)
 Call ID: 270fa577-2854-46bc-b60f-647ceeb86e38
  Args:
    target: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    relation: :hasFather
    source: Duchess_Eilika_of_Oldenburg
  AssignClass (dc0f71ee-0264-4d66-be5a-5905efe7ddbc)
 Call ID: dc0f71ee-0264-4d66-be5a-5905efe7ddbc
  Args:
    type: :Woman
    source: Princess_Helena_of_Waldeck_and_Pyrmont
  AssignClass (40120740-377f-4dd5-98de-662dea6045ca)
 Call ID: 40120740-377f-4dd5-98de-662dea6045ca
  Args:
    type: :Person
    source: Princess_Helena_of_Waldeck_and_Pyrmont
  AddTriple (3759e128-086b-479e-ab84-ef7c6be9a67b)
 Call ID: 3759e128-086b-479e-ab84-ef7c6be9a67b
  Args:
    target: Princess_Helena_of_Waldeck_and_Pyrmont
    relation: :hasMother
    source: Duchess_Eilika_of_Oldenburg
  Finish (ee8344ee-614c-4e26-b452-017beb23070a)
 Call ID: ee8344ee-614c-4e26-b452-017beb23070a
  Args: