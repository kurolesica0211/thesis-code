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
  AssignClass (85d7f654-cfc7-4222-82c8-6a18280c6573)
 Call ID: 85d7f654-cfc7-4222-82c8-6a18280c6573
  Args:
    type: :Man
    source: Emich Kyrill, Prince of Leiningen
  AssignClass (5f6d0ec7-4aca-40b8-a236-59a3cbb4acb9)
 Call ID: 5f6d0ec7-4aca-40b8-a236-59a3cbb4acb9
  Args:
    source: Emich Kyrill, Prince of Leiningen
    type: :Person
  AddLiteral (3ec78b4f-5653-41eb-a530-c76eb033f4b8)
 Call ID: 3ec78b4f-5653-41eb-a530-c76eb033f4b8
  Args:
    source: Emich Kyrill, Prince of Leiningen
    literal_value: 1926
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (d4a23661-583a-4602-a703-4856af92b269)
 Call ID: d4a23661-583a-4602-a703-4856af92b269
  Args:
    source: Emich Kyrill, Prince of Leiningen
    literal_value: 1991
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (0d3302c8-e227-4827-9976-8463eb36e41b)
 Call ID: 0d3302c8-e227-4827-9976-8463eb36e41b
  Args:
    source: Karl, Prince of Leiningen
    type: :Man
  AssignClass (3b08ea3e-eca2-43f9-9175-b298f08e343a)
 Call ID: 3b08ea3e-eca2-43f9-9175-b298f08e343a
  Args:
    source: Karl, Prince of Leiningen
    type: :Person
  AddLiteral (315539d6-e07a-41e6-983d-685764d7c04b)
 Call ID: 315539d6-e07a-41e6-983d-685764d7c04b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Karl, Prince of Leiningen
    literal_value: 1898
  AddLiteral (ad929095-74d8-41ac-a9f9-891731cb9d49)
 Call ID: ad929095-74d8-41ac-a9f9-891731cb9d49
  Args:
    literal_value: 1946
    source: Karl, Prince of Leiningen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (6a3217af-5cff-4902-84c5-cca685f6fac8)
 Call ID: 6a3217af-5cff-4902-84c5-cca685f6fac8
  Args:
    relation: :hasFather
    source: Emich Kyrill, Prince of Leiningen
    target: Karl, Prince of Leiningen
  AssignClass (3ddf836a-65b5-4ddb-bf55-83ea8c637de9)
 Call ID: 3ddf836a-65b5-4ddb-bf55-83ea8c637de9
  Args:
    type: :Man
    source: Emich, 5th Prince of Leiningen
  AssignClass (2a37c760-4358-4122-9a4d-5683ea72d156)
 Call ID: 2a37c760-4358-4122-9a4d-5683ea72d156
  Args:
    type: :Person
    source: Emich, 5th Prince of Leiningen
  AssignClass (95042e5b-68bc-4e0c-81c7-5acf5c79a11a)
 Call ID: 95042e5b-68bc-4e0c-81c7-5acf5c79a11a
  Args:
    type: :Woman
    source: Princess Feodore of Hohenlohe-Langenburg
  AssignClass (7d1d226c-5b89-44f4-a971-2b38837eaf0a)
 Call ID: 7d1d226c-5b89-44f4-a971-2b38837eaf0a
  Args:
    type: :Person
    source: Princess Feodore of Hohenlohe-Langenburg
  AddTriple (99099f70-55b8-4c54-8a73-780f19764f5b)
 Call ID: 99099f70-55b8-4c54-8a73-780f19764f5b
  Args:
    source: Karl, Prince of Leiningen
    target: Emich, 5th Prince of Leiningen
    relation: :hasFather
  AddTriple (d3b722ac-98e8-42fc-bb45-e3cb35c6bfda)
 Call ID: d3b722ac-98e8-42fc-bb45-e3cb35c6bfda
  Args:
    target: Princess Feodore of Hohenlohe-Langenburg
    source: Karl, Prince of Leiningen
    relation: :hasMother
  AssignClass (a836318c-ee00-4d3d-a353-e2cb94403215)
 Call ID: a836318c-ee00-4d3d-a353-e2cb94403215
  Args:
    source: Grand Duchess Maria Kirillovna of Russia
    type: :Woman
  AssignClass (b65556af-c24d-4ef3-b87a-159c46961546)
 Call ID: b65556af-c24d-4ef3-b87a-159c46961546
  Args:
    source: Grand Duchess Maria Kirillovna of Russia
    type: :Person
  AddLiteral (d768881f-f5c8-42fd-bb76-6773a5084671)
 Call ID: d768881f-f5c8-42fd-bb76-6773a5084671
  Args:
    literal_value: 1907
    source: Grand Duchess Maria Kirillovna of Russia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (da75d727-a4b2-4fc9-9365-de99465a4a16)
 Call ID: da75d727-a4b2-4fc9-9365-de99465a4a16
  Args:
    literal_value: 1951
    source: Grand Duchess Maria Kirillovna of Russia
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (9994313e-2e04-44e7-ab24-db17d90ba94a)
 Call ID: 9994313e-2e04-44e7-ab24-db17d90ba94a
  Args:
    target: Grand Duchess Maria Kirillovna of Russia
    source: Emich Kyrill, Prince of Leiningen
    relation: :hasMother
  AssignClass (ad8e4345-6935-40fc-834d-4ca960207d11)
 Call ID: ad8e4345-6935-40fc-834d-4ca960207d11
  Args:
    type: :Man
    source: Grand Duke Kirill Vladimirovich of Russia
  AssignClass (b06a13c7-f525-4f85-8387-c37e87754b0b)
 Call ID: b06a13c7-f525-4f85-8387-c37e87754b0b
  Args:
    type: :Person
    source: Grand Duke Kirill Vladimirovich of Russia
  AssignClass (048bb99a-6f51-4e52-aa43-07f344abbf8c)
 Call ID: 048bb99a-6f51-4e52-aa43-07f344abbf8c
  Args:
    source: Princess Victoria Melita of Edinburgh
    type: :Woman
  AssignClass (ab4aa102-d99f-4e86-be6c-22885608c188)
 Call ID: ab4aa102-d99f-4e86-be6c-22885608c188
  Args:
    type: :Person
    source: Princess Victoria Melita of Edinburgh
  AddTriple (a40ac3c2-57a3-403d-91ac-6c807e72d82f)
 Call ID: a40ac3c2-57a3-403d-91ac-6c807e72d82f
  Args:
    relation: :hasFather
    target: Grand Duke Kirill Vladimirovich of Russia
    source: Grand Duchess Maria Kirillovna of Russia
  AddTriple (0bc3875e-0d83-4135-ba2e-0bff7597ece8)
 Call ID: 0bc3875e-0d83-4135-ba2e-0bff7597ece8
  Args:
    relation: :hasMother
    target: Princess Victoria Melita of Edinburgh
    source: Grand Duchess Maria Kirillovna of Russia
  AssignClass (4af56141-e754-41b7-8187-91396b7ddd6e)
 Call ID: 4af56141-e754-41b7-8187-91396b7ddd6e
  Args:
    source: Duchess Eilika of Oldenburg
    type: :Woman
  AssignClass (58609548-879c-4be5-a054-d93ecdb5686d)
 Call ID: 58609548-879c-4be5-a054-d93ecdb5686d
  Args:
    source: Duchess Eilika of Oldenburg
    type: :Person
  AddLiteral (73d1b92d-0e1e-40ed-8f96-9af9d5c8fc67)
 Call ID: 73d1b92d-0e1e-40ed-8f96-9af9d5c8fc67
  Args:
    literal_value: 1928
    source: Duchess Eilika of Oldenburg
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (ef8941a0-d42a-4729-bad6-e4415e152ea6)
 Call ID: ef8941a0-d42a-4729-bad6-e4415e152ea6
  Args:
    source: Duchess Eilika of Oldenburg
    literal_value: 2016
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (c28cca0b-0c77-44f6-a600-814b62e7dcab)
 Call ID: c28cca0b-0c77-44f6-a600-814b62e7dcab
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1950
    source: Emich Kyrill, Prince of Leiningen
  AddTriple (2d771e81-b83f-41cb-b0e0-0904da414907)
 Call ID: 2d771e81-b83f-41cb-b0e0-0904da414907
  Args:
    relation: :hasRelation
    target: Duchess Eilika of Oldenburg
    source: Emich Kyrill, Prince of Leiningen
  AssignClass (6b144424-588f-4bf0-9a17-0a99badc9140)
 Call ID: 6b144424-588f-4bf0-9a17-0a99badc9140
  Args:
    type: :Man
    source: Nikolaus, Hereditary Grand Duke of Oldenburg
  AssignClass (22fac79d-80a5-4bce-9946-a6eea90167ec)
 Call ID: 22fac79d-80a5-4bce-9946-a6eea90167ec
  Args:
    type: :Person
    source: Nikolaus, Hereditary Grand Duke of Oldenburg
  AssignClass (62f2c737-5641-4898-946c-59480d68a5d9)
 Call ID: 62f2c737-5641-4898-946c-59480d68a5d9
  Args:
    source: Princess Helena of Waldeck and Pyrmont
    type: :Woman
  AssignClass (2aa705b2-56a3-41e5-9bb3-db7716ea60eb)
 Call ID: 2aa705b2-56a3-41e5-9bb3-db7716ea60eb
  Args:
    type: :Person
    source: Princess Helena of Waldeck and Pyrmont
  AddTriple (b2603a4a-febd-4f35-ab14-b6976cce2a46)
 Call ID: b2603a4a-febd-4f35-ab14-b6976cce2a46
  Args:
    relation: :hasFather
    source: Duchess Eilika of Oldenburg
    target: Nikolaus, Hereditary Grand Duke of Oldenburg
  AddTriple (dce74a26-8eff-4ad2-8135-8623f8e28e2a)
 Call ID: dce74a26-8eff-4ad2-8135-8623f8e28e2a
  Args:
    target: Princess Helena of Waldeck and Pyrmont
    source: Duchess Eilika of Oldenburg
    relation: :hasMother
  Finish (9a98eb5d-9e73-41e3-907e-bbb5625ea491)
 Call ID: 9a98eb5d-9e73-41e3-907e-bbb5625ea491
  Args: