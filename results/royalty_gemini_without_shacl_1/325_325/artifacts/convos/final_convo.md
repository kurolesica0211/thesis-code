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
  AssignClass (422d7f32-fb57-484c-a7ca-0d494c1b6276)
 Call ID: 422d7f32-fb57-484c-a7ca-0d494c1b6276
  Args:
    source: Emich_Kyrill_Prince_of_Leiningen
    type: :Man
  AssignClass (801715ce-89c2-4f91-bab5-c4a68307e84c)
 Call ID: 801715ce-89c2-4f91-bab5-c4a68307e84c
  Args:
    type: :Man
    source: Karl_Prince_of_Leiningen
  AssignClass (8686bb97-02cb-47a7-8d2c-ebf75b955e8c)
 Call ID: 8686bb97-02cb-47a7-8d2c-ebf75b955e8c
  Args:
    type: :Man
    source: Emich_5th_Prince_of_Leiningen
  AssignClass (e34d2285-53d6-4d22-a94e-84845a816b80)
 Call ID: e34d2285-53d6-4d22-a94e-84845a816b80
  Args:
    source: Princess_Feodore_of_Hohenlohe-Langenburg
    type: :Woman
  AssignClass (9b942c45-0449-49d6-bf41-543e27d24a00)
 Call ID: 9b942c45-0449-49d6-bf41-543e27d24a00
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
  AssignClass (d4d0ee4c-d966-4d55-a6af-60718cdfb078)
 Call ID: d4d0ee4c-d966-4d55-a6af-60718cdfb078
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AssignClass (f8a3da0e-7989-43d7-add6-20672fe1ad5f)
 Call ID: f8a3da0e-7989-43d7-add6-20672fe1ad5f
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Edinburgh
  AssignClass (9fbc4f17-e31d-4318-b666-707157c95f3f)
 Call ID: 9fbc4f17-e31d-4318-b666-707157c95f3f
  Args:
    source: Duchess_Eilika_of_Oldenburg
    type: :Woman
  AssignClass (6ab283a5-3278-4a3d-b9aa-5237b943881d)
 Call ID: 6ab283a5-3278-4a3d-b9aa-5237b943881d
  Args:
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    type: :Man
  AssignClass (b51366c6-c31c-4c0c-9d8d-856f98bc3040)
 Call ID: b51366c6-c31c-4c0c-9d8d-856f98bc3040
  Args:
    source: Princess_Helena_of_Waldeck_and_Pyrmont
    type: :Woman
  AddLiteral (28dbba29-3551-45d2-b190-aaabbebf8bf7)
 Call ID: 28dbba29-3551-45d2-b190-aaabbebf8bf7
  Args:
    literal_value: 1926
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (c982d218-8f4c-43dc-93da-40d721bbce9e)
 Call ID: c982d218-8f4c-43dc-93da-40d721bbce9e
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_value: 1991
  AddLiteral (87f16b6f-75f4-4454-9b4d-5afe1fd36254)
 Call ID: 87f16b6f-75f4-4454-9b4d-5afe1fd36254
  Args:
    literal_value: 1898
    literal_type: xsd:integer
    source: Karl_Prince_of_Leiningen
    relation: :hasBirthYear
  AddLiteral (d8431d7a-a553-4144-bb9a-b3bc06bf7b4e)
 Call ID: d8431d7a-a553-4144-bb9a-b3bc06bf7b4e
  Args:
    literal_type: xsd:integer
    source: Karl_Prince_of_Leiningen
    relation: :hasDeathYear
    literal_value: 1946
  AddLiteral (dabfe385-7ccd-410c-b873-f3afb5ace1bd)
 Call ID: dabfe385-7ccd-410c-b873-f3afb5ace1bd
  Args:
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1907
  AddLiteral (3133b4bf-43b5-4d1b-8d04-9bbaaa45386a)
 Call ID: 3133b4bf-43b5-4d1b-8d04-9bbaaa45386a
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    literal_value: 1951
  AddLiteral (6fb48c8e-e294-42ab-96c4-93b9a153295f)
 Call ID: 6fb48c8e-e294-42ab-96c4-93b9a153295f
  Args:
    literal_type: xsd:integer
    source: Duchess_Eilika_of_Oldenburg
    relation: :hasBirthYear
    literal_value: 1928
  AddLiteral (f497c28e-eb5c-4d8e-a292-0ae8c8dff40f)
 Call ID: f497c28e-eb5c-4d8e-a292-0ae8c8dff40f
  Args:
    source: Duchess_Eilika_of_Oldenburg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2016
  AddTriple (9ea310c3-222a-44f1-ade6-038daa6f51bd)
 Call ID: 9ea310c3-222a-44f1-ade6-038daa6f51bd
  Args:
    target: Karl_Prince_of_Leiningen
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasFather
  AddTriple (ddf15eb0-9c15-48d4-9f82-26a66ce50f5b)
 Call ID: ddf15eb0-9c15-48d4-9f82-26a66ce50f5b
  Args:
    relation: :hasMother
    target: Grand_Duchess_Maria_Kirillovna_of_Russia
    source: Emich_Kyrill_Prince_of_Leiningen
  AddTriple (c6764447-d6d7-442f-9c8d-8831682577cf)
 Call ID: c6764447-d6d7-442f-9c8d-8831682577cf
  Args:
    target: Emich_5th_Prince_of_Leiningen
    source: Karl_Prince_of_Leiningen
    relation: :hasFather
  AddTriple (dedd76e5-9cb9-4865-bdf6-49398a04b4da)
 Call ID: dedd76e5-9cb9-4865-bdf6-49398a04b4da
  Args:
    relation: :hasMother
    source: Karl_Prince_of_Leiningen
    target: Princess_Feodore_of_Hohenlohe-Langenburg
  AddTriple (c7a0ed29-1c45-44b3-84d7-be3d2c69c8d0)
 Call ID: c7a0ed29-1c45-44b3-84d7-be3d2c69c8d0
  Args:
    target: Grand_Duke_Kirill_Vladimirovich_of_Russia
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    relation: :hasFather
  AddTriple (c866d593-7887-44ce-9f3c-2e58cac0e80a)
 Call ID: c866d593-7887-44ce-9f3c-2e58cac0e80a
  Args:
    relation: :hasMother
    target: Princess_Victoria_Melita_of_Edinburgh
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
  AddTriple (4b944002-27b9-4b85-bb13-67ce45d23703)
 Call ID: 4b944002-27b9-4b85-bb13-67ce45d23703
  Args:
    relation: :hasFather
    target: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    source: Duchess_Eilika_of_Oldenburg
  AddTriple (ba6a5ac7-8270-4c2d-a6b2-c1c9c22adc1e)
 Call ID: ba6a5ac7-8270-4c2d-a6b2-c1c9c22adc1e
  Args:
    relation: :hasMother
    target: Princess_Helena_of_Waldeck_and_Pyrmont
    source: Duchess_Eilika_of_Oldenburg
  AddLiteral (fe2b8031-4271-4700-b521-92c72e9ef6fe)
 Call ID: fe2b8031-4271-4700-b521-92c72e9ef6fe
  Args:
    literal_value: 1950
    source: Emich_Kyrill_Prince_of_Leiningen
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (5cae7843-340c-41f6-92f4-9f0e405c5ed7)
 Call ID: 5cae7843-340c-41f6-92f4-9f0e405c5ed7
  Args:
    target: Duchess_Eilika_of_Oldenburg
    source: Emich_Kyrill_Prince_of_Leiningen
    relation: :hasRelation
  Finish (2a1df193-ff45-4f27-a14a-baee93039ea6)
 Call ID: 2a1df193-ff45-4f27-a14a-baee93039ea6
  Args: