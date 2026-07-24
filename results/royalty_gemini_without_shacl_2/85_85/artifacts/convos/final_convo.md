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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Princess Katarina of Yugoslavia, Lady de Silva (born 28 November 1959) is an English businessperson specialising in etiquette and decorum courses.
Early life

Katarina was born at King’s College Hospital in London to Princess Margarita of Baden and Prince Tomislav of Yugoslavia.
Her father's dynasty having been deposed and banished from Yugoslavia after World War II, she grew up in exile, largely in England.
She has one brother, Prince Nikola of Yugoslavia, and two half-brothers, Prince George and Prince Michael.
She is a first cousin of Alexander, Crown Prince of Yugoslavia.
Her grandmother, Princess Theodora, Margravine of Baden, was the sister of Prince Philip, Duke of Edinburgh, late husband of Queen Elizabeth II.
Princess Katharina is the senior female-line descendant of Queen Victoria, through the Queen's second daughter Alice, Grand Duchess of Hesse, who was the grandmother of Princess Katharina's great-grandmother, Princess Alice of Battenberg.
Career

In 1978, Katarina was presented as a debutante to high society at the International Debutante Ball at the Waldorf-Astoria Hotel.
As of 2013, Katarina and former Royal butler Grant Harrold develop and sell etiquette and decorum classes.
Personal life

Katarina married barrister Sir Desmond de Silva on 5 December 1987.
They had one daughter, Victoria Marie Esmé Margarita, born on 6 September 1991.
Charity work

In 2009, Katarina supported the charity Project Change: Bermuda to raise funds towards building a hospital and training medical staff in Burundi.
Katarina served as the president of the Guild of Travel and Tourism in the United Kingdom.
In 2013, she became patron of the Society of Genealogists succeeding Prince Michael of Kent.
Honours

Ancestry

Katarina is a member of the House of Karađorđević.
Through her father, Katarina descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, and furthermore from Emperor Nicholas I of Russia, King Ferdinand II and Queen Maria II of Portugal, and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through her mother, Katarina descends from Leopold, Grand Duke of Baden, kings George V of Hanover, Christian IX of Denmark, George I of Greece and Nicholas I, Emperor of Russia.



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
  AssignClass (49f2bbbd-2c07-4ade-a0ce-2853d1dfe98e)
 Call ID: 49f2bbbd-2c07-4ade-a0ce-2853d1dfe98e
  Args:
    type: :Woman
    source: Princess Katarina of Yugoslavia
  AssignClass (88954564-fd63-4512-af32-225aa9c113c5)
 Call ID: 88954564-fd63-4512-af32-225aa9c113c5
  Args:
    type: :Person
    source: Princess Katarina of Yugoslavia
  AddLiteral (6fd045a1-0e0d-4079-8619-c048c14bbf4d)
 Call ID: 6fd045a1-0e0d-4079-8619-c048c14bbf4d
  Args:
    literal_type: xsd:integer
    literal_value: 1959
    relation: :hasBirthYear
    source: Princess Katarina of Yugoslavia
  AssignClass (cba11e29-1b98-4df2-a08b-a7ca75e13cb6)
 Call ID: cba11e29-1b98-4df2-a08b-a7ca75e13cb6
  Args:
    type: :Woman
    source: Princess Margarita of Baden
  AssignClass (6865e34b-95f1-4928-8ca3-8b9b8038cca9)
 Call ID: 6865e34b-95f1-4928-8ca3-8b9b8038cca9
  Args:
    source: Princess Margarita of Baden
    type: :Person
  AssignClass (0e47055d-7b6d-40c4-9a33-014accc93ab7)
 Call ID: 0e47055d-7b6d-40c4-9a33-014accc93ab7
  Args:
    source: Prince Tomislav of Yugoslavia
    type: :Man
  AssignClass (1e8284f8-1444-4aac-ae97-08387c041c08)
 Call ID: 1e8284f8-1444-4aac-ae97-08387c041c08
  Args:
    type: :Person
    source: Prince Tomislav of Yugoslavia
  AddTriple (50228d68-14fc-45f2-9ddd-bc32afd3490e)
 Call ID: 50228d68-14fc-45f2-9ddd-bc32afd3490e
  Args:
    relation: :hasMother
    target: Princess Margarita of Baden
    source: Princess Katarina of Yugoslavia
  AddTriple (5d0126bd-056a-4383-9585-dcd39cb9574a)
 Call ID: 5d0126bd-056a-4383-9585-dcd39cb9574a
  Args:
    source: Princess Katarina of Yugoslavia
    target: Prince Tomislav of Yugoslavia
    relation: :hasFather
  AssignClass (d7314b7f-e58e-4e3d-bd68-06059a0814a5)
 Call ID: d7314b7f-e58e-4e3d-bd68-06059a0814a5
  Args:
    type: :Man
    source: Prince Nikola of Yugoslavia
  AssignClass (d7d33aeb-e022-44eb-b868-01ef39bbb87a)
 Call ID: d7d33aeb-e022-44eb-b868-01ef39bbb87a
  Args:
    type: :Person
    source: Prince Nikola of Yugoslavia
  AddTriple (9942edc5-0943-48f7-8cad-2807fb2e0afd)
 Call ID: 9942edc5-0943-48f7-8cad-2807fb2e0afd
  Args:
    source: Princess Katarina of Yugoslavia
    relation: :hasBrother
    target: Prince Nikola of Yugoslavia
  AssignClass (8ac5c8e0-bcb1-4ef2-8b8d-8639db14a7ce)
 Call ID: 8ac5c8e0-bcb1-4ef2-8b8d-8639db14a7ce
  Args:
    type: :Man
    source: Prince George
  AssignClass (84033ca3-11fa-482d-aabb-6fe1888999c4)
 Call ID: 84033ca3-11fa-482d-aabb-6fe1888999c4
  Args:
    type: :Person
    source: Prince George
  AssignClass (4a6880b7-bea8-46f5-8dd5-8f45855822b2)
 Call ID: 4a6880b7-bea8-46f5-8dd5-8f45855822b2
  Args:
    source: Prince Michael
    type: :Man
  AssignClass (e0ef44a6-f7ca-4acd-997a-dfe0c42c0925)
 Call ID: e0ef44a6-f7ca-4acd-997a-dfe0c42c0925
  Args:
    type: :Person
    source: Prince Michael
  AddTriple (be5d7fcc-a2b9-4925-8b24-623b0b6aa4fa)
 Call ID: be5d7fcc-a2b9-4925-8b24-623b0b6aa4fa
  Args:
    source: Princess Katarina of Yugoslavia
    relation: :hasBrother
    target: Prince George
  AddTriple (118a950b-0836-44b2-a9a1-07dbbf9a930c)
 Call ID: 118a950b-0836-44b2-a9a1-07dbbf9a930c
  Args:
    relation: :hasBrother
    target: Prince Michael
    source: Princess Katarina of Yugoslavia
  AssignClass (028d35b2-8db3-4bb0-8381-617ac82a9c88)
 Call ID: 028d35b2-8db3-4bb0-8381-617ac82a9c88
  Args:
    type: :Man
    source: Sir Desmond de Silva
  AssignClass (c3963b9d-d1b6-4d49-9efd-e7744412b5cb)
 Call ID: c3963b9d-d1b6-4d49-9efd-e7744412b5cb
  Args:
    source: Sir Desmond de Silva
    type: :Person
  AddLiteral (8c467070-f3c2-4c3d-992f-023a2f601d13)
 Call ID: 8c467070-f3c2-4c3d-992f-023a2f601d13
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1987
    source: Princess Katarina of Yugoslavia
  AssignClass (465fc969-4bb7-432d-8d07-ad6598716024)
 Call ID: 465fc969-4bb7-432d-8d07-ad6598716024
  Args:
    type: :Woman
    source: Victoria Marie Esmé Margarita
  AssignClass (258a5f34-ee61-45c3-89f2-2e1b145095ed)
 Call ID: 258a5f34-ee61-45c3-89f2-2e1b145095ed
  Args:
    type: :Person
    source: Victoria Marie Esmé Margarita
  AddTriple (97234409-63d3-4934-82e5-c5690d66ae43)
 Call ID: 97234409-63d3-4934-82e5-c5690d66ae43
  Args:
    target: Victoria Marie Esmé Margarita
    relation: :hasDaughter
    source: Princess Katarina of Yugoslavia
  AddTriple (5f9664be-6145-4162-8ba5-149a14fb2240)
 Call ID: 5f9664be-6145-4162-8ba5-149a14fb2240
  Args:
    source: Victoria Marie Esmé Margarita
    target: Sir Desmond de Silva
    relation: :hasFather
  Finish (c902cef9-1cdf-4f21-9b76-7a606b7a191e)
 Call ID: c902cef9-1cdf-4f21-9b76-7a606b7a191e
  Args: