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
Princess Eugenie of Greece and Denmark (Greek: Ευγενία, romanized: Evyenía; 10 February 1910 – 13 February 1989) was by birth member of the Greek royal family and by marriage member of the House of Radziwiłł and House of Thurn und Taxis.
Early life and ancestry

Eugenie was the youngest child and only daughter of Prince George of Greece and Denmark and his wife, Princess Marie Bonaparte, daughter of Marie-Félix Blanc and Prince Roland Bonaparte, a great-nephew of Napoleon I.
Her father was the second son of George I of Greece and Olga Constantinovna of Russia.
She had one elder brother, Prince Peter of Greece and Denmark, who, at the time of his birth, was third in line of succession to the Greek throne, preceded only by his unmarried cousin Paul and his own and Eugenia's father, Prince George.
As a cousin of the bridegroom, Eugenie was a leading guest at the 1947 wedding of Princess Elizabeth and Philip, Duke of Edinburgh.
She authored Le Tsarevitch, Enfant Martyr, a biography of Aleksey Nikolaevich, Tsarevich of Russia, written in French, which was published in 1990.
Marriage and issue

She married Prince Dominik Rainer Radziwiłł, member of the House of Radziwiłł (and son of Prince Hieronim Radziwiłł and Archduchess Renata of Austria), on 30 May 1938 in Paris.
They had two children:


Eugénie remarried on 28 November 1949 to Prince Raymundo della Torre e Tasso, Duke of Castel Duino, a cadet member of the House of Thurn and Taxis.



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
  AssignClass (21bce3e6-95cb-41ef-bcf8-efe224269150)
 Call ID: 21bce3e6-95cb-41ef-bcf8-efe224269150
  Args:
    source: :Princess_Eugenie_of_Greece_and_Denmark
    type: :Person
  AssignClass (7774661d-28a6-4606-883c-c903cf4e641a)
 Call ID: 7774661d-28a6-4606-883c-c903cf4e641a
  Args:
    source: :Princess_Eugenie_of_Greece_and_Denmark
    type: :Woman
  AddLiteral (801d5c8d-2425-48e7-9e4e-ab84d900a37b)
 Call ID: 801d5c8d-2425-48e7-9e4e-ab84d900a37b
  Args:
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1910
    relation: :hasBirthYear
  AddLiteral (7852e93b-a371-45b2-84f1-17eff2f76d78)
 Call ID: 7852e93b-a371-45b2-84f1-17eff2f76d78
  Args:
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1989
    relation: :hasDeathYear
  AssignClass (b11c6c49-4f26-41dc-b0e7-ab1a1043aa0e)
 Call ID: b11c6c49-4f26-41dc-b0e7-ab1a1043aa0e
  Args:
    type: :Person
    source: :Prince_George_of_Greece_and_Denmark
  AssignClass (9a853f9d-4ef6-45c7-9b9b-270a2ba008ff)
 Call ID: 9a853f9d-4ef6-45c7-9b9b-270a2ba008ff
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    type: :Man
  AssignClass (caf4742b-14c9-40bf-b95b-e20568585eef)
 Call ID: caf4742b-14c9-40bf-b95b-e20568585eef
  Args:
    source: :Princess_Marie_Bonaparte
    type: :Person
  AssignClass (55477446-24c4-4a44-ae20-1b0cc5c3ea57)
 Call ID: 55477446-24c4-4a44-ae20-1b0cc5c3ea57
  Args:
    type: :Woman
    source: :Princess_Marie_Bonaparte
  AddTriple (ff78102c-5f57-4364-8da4-52503af4c97e)
 Call ID: ff78102c-5f57-4364-8da4-52503af4c97e
  Args:
    relation: :hasFather
    target: :Prince_George_of_Greece_and_Denmark
    source: :Princess_Eugenie_of_Greece_and_Denmark
  AddTriple (f9ecad72-0a44-4df4-b7ff-76f5487ec0be)
 Call ID: f9ecad72-0a44-4df4-b7ff-76f5487ec0be
  Args:
    relation: :hasMother
    target: :Princess_Marie_Bonaparte
    source: :Princess_Eugenie_of_Greece_and_Denmark
  AssignClass (28cfabce-3cec-4b36-b08a-37e6966ebe95)
 Call ID: 28cfabce-3cec-4b36-b08a-37e6966ebe95
  Args:
    source: :Marie-Felix_Blanc
    type: :Person
  AssignClass (1f1fba15-4a9b-4ba1-be9b-65c24bd22620)
 Call ID: 1f1fba15-4a9b-4ba1-be9b-65c24bd22620
  Args:
    type: :Woman
    source: :Marie-Felix_Blanc
  AssignClass (c7e49152-138e-43a4-8ada-fe09bc2ea69d)
 Call ID: c7e49152-138e-43a4-8ada-fe09bc2ea69d
  Args:
    type: :Person
    source: :Prince_Roland_Bonaparte
  AssignClass (7a152cec-de24-4bd8-8ae0-19ed0ada956d)
 Call ID: 7a152cec-de24-4bd8-8ae0-19ed0ada956d
  Args:
    source: :Prince_Roland_Bonaparte
    type: :Man
  AddTriple (a84416a8-5d08-4374-93d6-65334a7c927d)
 Call ID: a84416a8-5d08-4374-93d6-65334a7c927d
  Args:
    target: :Marie-Felix_Blanc
    relation: :hasMother
    source: :Princess_Marie_Bonaparte
  AddTriple (4fa5c687-6f1c-4026-9f1b-efbbe688fee0)
 Call ID: 4fa5c687-6f1c-4026-9f1b-efbbe688fee0
  Args:
    target: :Prince_Roland_Bonaparte
    relation: :hasFather
    source: :Princess_Marie_Bonaparte
  AssignClass (0ef318c5-6b14-4479-a945-6424b129b24b)
 Call ID: 0ef318c5-6b14-4479-a945-6424b129b24b
  Args:
    type: :Person
    source: :George_I_of_Greece
  AssignClass (89346c02-2751-406b-81a5-52bd9c4576a2)
 Call ID: 89346c02-2751-406b-81a5-52bd9c4576a2
  Args:
    type: :Man
    source: :George_I_of_Greece
  AssignClass (436662ef-01fb-4b71-a17a-3a02112d3ddf)
 Call ID: 436662ef-01fb-4b71-a17a-3a02112d3ddf
  Args:
    type: :Person
    source: :Olga_Constantinovna_of_Russia
  AssignClass (74574cbf-807c-48cd-8f72-f425f3101cd7)
 Call ID: 74574cbf-807c-48cd-8f72-f425f3101cd7
  Args:
    type: :Woman
    source: :Olga_Constantinovna_of_Russia
  AddTriple (22e38225-813c-49c8-9a35-73f8917370fc)
 Call ID: 22e38225-813c-49c8-9a35-73f8917370fc
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    target: :George_I_of_Greece
    relation: :hasFather
  AddTriple (b8f6c46d-4d21-4d1c-a2c0-a697fee76946)
 Call ID: b8f6c46d-4d21-4d1c-a2c0-a697fee76946
  Args:
    source: :Prince_George_of_Greece_and_Denmark
    target: :Olga_Constantinovna_of_Russia
    relation: :hasMother
  AssignClass (08e14723-4f72-4b00-8b53-ad2ee23eb597)
 Call ID: 08e14723-4f72-4b00-8b53-ad2ee23eb597
  Args:
    source: :Prince_Peter_of_Greece_and_Denmark
    type: :Person
  AssignClass (65a2c6a5-9e1d-4526-9556-211759302c15)
 Call ID: 65a2c6a5-9e1d-4526-9556-211759302c15
  Args:
    type: :Man
    source: :Prince_Peter_of_Greece_and_Denmark
  AddTriple (7f7ae35d-8b56-4b93-b0e7-fc60109b09a6)
 Call ID: 7f7ae35d-8b56-4b93-b0e7-fc60109b09a6
  Args:
    relation: :hasBrother
    target: :Prince_Peter_of_Greece_and_Denmark
    source: :Princess_Eugenie_of_Greece_and_Denmark
  AddTriple (c924d708-0daa-4d37-bdb0-f65b74d00cdd)
 Call ID: c924d708-0daa-4d37-bdb0-f65b74d00cdd
  Args:
    source: :Prince_Peter_of_Greece_and_Denmark
    relation: :hasFather
    target: :Prince_George_of_Greece_and_Denmark
  AddTriple (fae17aec-fca8-430e-8f0a-d72288e6f4ab)
 Call ID: fae17aec-fca8-430e-8f0a-d72288e6f4ab
  Args:
    target: :Princess_Marie_Bonaparte
    relation: :hasMother
    source: :Prince_Peter_of_Greece_and_Denmark
  AssignClass (b0e0c058-d611-4455-a2bd-65270d970511)
 Call ID: b0e0c058-d611-4455-a2bd-65270d970511
  Args:
    type: :Person
    source: :Prince_Dominik_Rainer_Radziwill
  AssignClass (d7d00fda-66ce-4e98-bced-bacf7ec65863)
 Call ID: d7d00fda-66ce-4e98-bced-bacf7ec65863
  Args:
    source: :Prince_Dominik_Rainer_Radziwill
    type: :Man
  AddLiteral (1a0a2dae-028e-45eb-b2c3-297739ba3449)
 Call ID: 1a0a2dae-028e-45eb-b2c3-297739ba3449
  Args:
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1938
    relation: :hasMarriageYear
  AssignClass (37e7a784-bac6-4755-b93b-db84eebac5a7)
 Call ID: 37e7a784-bac6-4755-b93b-db84eebac5a7
  Args:
    type: :Person
    source: :Prince_Hieronim_Radziwill
  AssignClass (4bd68e23-cc02-4543-8257-15c734657eb2)
 Call ID: 4bd68e23-cc02-4543-8257-15c734657eb2
  Args:
    source: :Prince_Hieronim_Radziwill
    type: :Man
  AssignClass (ab778c2f-212e-44ed-a937-fd2e926de3e3)
 Call ID: ab778c2f-212e-44ed-a937-fd2e926de3e3
  Args:
    source: :Archduchess_Renata_of_Austria
    type: :Person
  AssignClass (7ff3a5f1-abea-46f6-86b4-71e57efef716)
 Call ID: 7ff3a5f1-abea-46f6-86b4-71e57efef716
  Args:
    type: :Woman
    source: :Archduchess_Renata_of_Austria
  AddTriple (f3e9c65e-9514-4c0a-a71b-26b73e82561e)
 Call ID: f3e9c65e-9514-4c0a-a71b-26b73e82561e
  Args:
    source: :Prince_Dominik_Rainer_Radziwill
    target: :Prince_Hieronim_Radziwill
    relation: :hasFather
  AddTriple (d18bd7e6-c1ca-4783-ab93-92386e54b934)
 Call ID: d18bd7e6-c1ca-4783-ab93-92386e54b934
  Args:
    source: :Prince_Dominik_Rainer_Radziwill
    target: :Archduchess_Renata_of_Austria
    relation: :hasMother
  AssignClass (3be56dcc-1ce2-4355-bc17-acf73a4984d5)
 Call ID: 3be56dcc-1ce2-4355-bc17-acf73a4984d5
  Args:
    type: :Person
    source: :Prince_Raymundo_della_Torre_e_Tasso
  AssignClass (0b5f1d23-a840-4e45-9e14-46e683306bd4)
 Call ID: 0b5f1d23-a840-4e45-9e14-46e683306bd4
  Args:
    source: :Prince_Raymundo_della_Torre_e_Tasso
    type: :Man
  AddLiteral (0288011c-e209-4753-9f36-d3a18b0a1dac)
 Call ID: 0288011c-e209-4753-9f36-d3a18b0a1dac
  Args:
    relation: :hasMarriageYear
    source: :Princess_Eugenie_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1949
  Finish (2d7221c7-f4df-4807-90b3-e1ca931ffa9e)
 Call ID: 2d7221c7-f4df-4807-90b3-e1ca931ffa9e
  Args: