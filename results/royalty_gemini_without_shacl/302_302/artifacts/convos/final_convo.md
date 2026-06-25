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
Prince Nikola of Yugoslavia (29 June 1928 – 12 April 1954), also known in Britain as Prince Nicholas and in Serbia as Nikola Karađorđević (Serbian Cyrillic: Никола Карађорђевић), was the younger son of Prince Paul of Yugoslavia by his wife Princess Olga of Greece and Denmark.
Biography

Prince Nikola was born into the House of Karađorđević, the dynasty that ruled Serbia and later the Kingdom of Yugoslavia.
Known as "Nicky", he was educated in England at Oxford University and was a frequent social escort to Princess Margaret, sister of Queen Elizabeth II.
Prince Nikola died unmarried in 1954, survived by his parents, Prince Paul and Princess Olga of Yugoslavia; older brother Prince Alexander and younger sister, Princess Elizabeth; also his maternal grandmother, Grand Duchess Elena Vladimirovna of Russia (Princess Nicholas of Greece and Denmark) and his maternal aunts, Princess Elizabeth, Countess of Toerring-Jettenbach, and Princess Marina, Duchess of Kent.
Death

Nikola died in a road accident at Datchet, now in Berkshire, England, some five miles from the home of his aunt, the Duchess of Kent.
He was
driving himself alone towards London, on his way to a meeting with Princess Margaret the same evening, to attend a full-dress rehearsal of a play being performed by a group of young socialites.
He was a paternal grandson of Arsen Karađorđević, Prince of Serbia and Princess Aurora Pavlovna Demidova di San Donato.
He was a maternal grandson of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.



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
  AssignClass (44f4768c-342a-4f72-ba8b-9b0ba0ca7554)
 Call ID: 44f4768c-342a-4f72-ba8b-9b0ba0ca7554
  Args:
    type: :Man
    source: :PrinceNikolaOfYugoslavia
  AssignClass (2945e2ed-98ce-4c76-8a15-9c1082bcb9b7)
 Call ID: 2945e2ed-98ce-4c76-8a15-9c1082bcb9b7
  Args:
    type: :Person
    source: :PrinceNikolaOfYugoslavia
  AddLiteral (69f5de5a-4eaa-49e2-98b4-b22adad2b373)
 Call ID: 69f5de5a-4eaa-49e2-98b4-b22adad2b373
  Args:
    literal_value: 1928
    source: :PrinceNikolaOfYugoslavia
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (0803bd50-4078-4285-95d5-d7f00b4223d5)
 Call ID: 0803bd50-4078-4285-95d5-d7f00b4223d5
  Args:
    source: :PrinceNikolaOfYugoslavia
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1954
  AddLiteral (8bf7f95c-7c68-450f-aa3b-ebc0edea07cf)
 Call ID: 8bf7f95c-7c68-450f-aa3b-ebc0edea07cf
  Args:
    literal_value: Prince Nicholas
    source: :PrinceNikolaOfYugoslavia
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddLiteral (81007363-e7a9-43f7-bbf3-61d78fceeba4)
 Call ID: 81007363-e7a9-43f7-bbf3-61d78fceeba4
  Args:
    literal_value: Nikola Karađorđević
    source: :PrinceNikolaOfYugoslavia
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (566f0a91-c0b2-46a5-84aa-e02e7b5ee77d)
 Call ID: 566f0a91-c0b2-46a5-84aa-e02e7b5ee77d
  Args:
    literal_value: Nicky
    source: :PrinceNikolaOfYugoslavia
    literal_type: xsd:string
    relation: :knownAs
  AssignClass (27a4016d-1bf0-47b5-8c23-ae375dff7ac8)
 Call ID: 27a4016d-1bf0-47b5-8c23-ae375dff7ac8
  Args:
    type: :Man
    source: :PrincePaulOfYugoslavia
  AssignClass (053c7e42-6c2f-4d03-ae65-b9c96edb43a5)
 Call ID: 053c7e42-6c2f-4d03-ae65-b9c96edb43a5
  Args:
    type: :Person
    source: :PrincePaulOfYugoslavia
  AddTriple (28918bee-5226-4797-8283-bb75f2dc0e58)
 Call ID: 28918bee-5226-4797-8283-bb75f2dc0e58
  Args:
    relation: :hasFather
    source: :PrinceNikolaOfYugoslavia
    target: :PrincePaulOfYugoslavia
  AssignClass (f5e057a3-b06f-4d0d-acda-0104eda9ee6e)
 Call ID: f5e057a3-b06f-4d0d-acda-0104eda9ee6e
  Args:
    source: :PrincessOlgaOfGreeceAndDenmark
    type: :Woman
  AssignClass (7433d6cf-4931-49c5-8113-bd29b6d661dc)
 Call ID: 7433d6cf-4931-49c5-8113-bd29b6d661dc
  Args:
    source: :PrincessOlgaOfGreeceAndDenmark
    type: :Person
  AddTriple (af67fb0b-1702-4928-915b-f1ef299b41ce)
 Call ID: af67fb0b-1702-4928-915b-f1ef299b41ce
  Args:
    relation: :hasMother
    source: :PrinceNikolaOfYugoslavia
    target: :PrincessOlgaOfGreeceAndDenmark
  AssignClass (1e02bc19-cf0f-4842-a461-069c91d84df0)
 Call ID: 1e02bc19-cf0f-4842-a461-069c91d84df0
  Args:
    source: :PrinceAlexander
    type: :Man
  AssignClass (6dc9b90d-7cdd-4937-8272-7254daf6a233)
 Call ID: 6dc9b90d-7cdd-4937-8272-7254daf6a233
  Args:
    type: :Person
    source: :PrinceAlexander
  AddTriple (6ec5131d-c866-422c-854d-2bf18162c31f)
 Call ID: 6ec5131d-c866-422c-854d-2bf18162c31f
  Args:
    source: :PrinceNikolaOfYugoslavia
    relation: :hasBrother
    target: :PrinceAlexander
  AssignClass (5dc63351-811e-4e20-a436-4d0f7a20d2ba)
 Call ID: 5dc63351-811e-4e20-a436-4d0f7a20d2ba
  Args:
    source: :PrincessElizabeth
    type: :Woman
  AssignClass (069c705d-4507-43c9-9d2f-cf1162d38598)
 Call ID: 069c705d-4507-43c9-9d2f-cf1162d38598
  Args:
    type: :Person
    source: :PrincessElizabeth
  AddTriple (f390ac96-abe7-449a-864c-e20fbfab13ac)
 Call ID: f390ac96-abe7-449a-864c-e20fbfab13ac
  Args:
    source: :PrinceNikolaOfYugoslavia
    relation: :hasSister
    target: :PrincessElizabeth
  AssignClass (7ffc9235-f56d-4dee-b95e-102c3dbaa44e)
 Call ID: 7ffc9235-f56d-4dee-b95e-102c3dbaa44e
  Args:
    source: :GrandDuchessElenaVladimirovnaOfRussia
    type: :Woman
  AssignClass (9b4336da-6968-4be6-b07e-696256f688bf)
 Call ID: 9b4336da-6968-4be6-b07e-696256f688bf
  Args:
    source: :GrandDuchessElenaVladimirovnaOfRussia
    type: :Person
  AddTriple (a94f1c6a-76ce-426f-8d8e-5ed6a9e1a54f)
 Call ID: a94f1c6a-76ce-426f-8d8e-5ed6a9e1a54f
  Args:
    source: :PrincessOlgaOfGreeceAndDenmark
    relation: :hasMother
    target: :GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (ac697d31-f012-44af-9d37-a5debcbbf21d)
 Call ID: ac697d31-f012-44af-9d37-a5debcbbf21d
  Args:
    source: :PrincessElizabethCountessOfToerringJettenbach
    type: :Woman
  AssignClass (c8d3c6af-3511-4853-a2ce-82e87e61f4b6)
 Call ID: c8d3c6af-3511-4853-a2ce-82e87e61f4b6
  Args:
    type: :Person
    source: :PrincessElizabethCountessOfToerringJettenbach
  AddTriple (a4c8d130-c5e5-40dc-a377-f9fd3a47cc63)
 Call ID: a4c8d130-c5e5-40dc-a377-f9fd3a47cc63
  Args:
    relation: :isAuntOf
    source: :PrincessElizabethCountessOfToerringJettenbach
    target: :PrinceNikolaOfYugoslavia
  AssignClass (90f31230-7e88-4acd-8ffe-4decb4fd460b)
 Call ID: 90f31230-7e88-4acd-8ffe-4decb4fd460b
  Args:
    source: :PrincessMarinaDuchessOfKent
    type: :Woman
  AssignClass (cecf5c4d-8ae4-4b93-aaff-f9352632f7a8)
 Call ID: cecf5c4d-8ae4-4b93-aaff-f9352632f7a8
  Args:
    source: :PrincessMarinaDuchessOfKent
    type: :Person
  AddTriple (7451c9d3-4bfb-4e41-a862-f5d20da24286)
 Call ID: 7451c9d3-4bfb-4e41-a862-f5d20da24286
  Args:
    target: :PrinceNikolaOfYugoslavia
    relation: :isAuntOf
    source: :PrincessMarinaDuchessOfKent
  AssignClass (e710eef8-3529-4364-8e4f-a174ff12e5f9)
 Call ID: e710eef8-3529-4364-8e4f-a174ff12e5f9
  Args:
    source: :ArsenKaradjordjevic
    type: :Man
  AssignClass (3244125c-de96-4ef3-b0f1-cc4dc4be3e7e)
 Call ID: 3244125c-de96-4ef3-b0f1-cc4dc4be3e7e
  Args:
    source: :ArsenKaradjordjevic
    type: :Person
  AddTriple (0e071d3c-1d5a-49e4-b570-432afdef7a40)
 Call ID: 0e071d3c-1d5a-49e4-b570-432afdef7a40
  Args:
    target: :ArsenKaradjordjevic
    source: :PrincePaulOfYugoslavia
    relation: :hasFather
  AssignClass (013d56e7-eb6c-48c5-a533-2ea2975afa7c)
 Call ID: 013d56e7-eb6c-48c5-a533-2ea2975afa7c
  Args:
    type: :Woman
    source: :PrincessAuroraPavlovnaDemidovaDiSanDonato
  AssignClass (f75ce90d-a20a-4a24-8322-32a3dd34a463)
 Call ID: f75ce90d-a20a-4a24-8322-32a3dd34a463
  Args:
    type: :Person
    source: :PrincessAuroraPavlovnaDemidovaDiSanDonato
  AddTriple (d2d4b3e3-7b41-465d-919c-53391290abb5)
 Call ID: d2d4b3e3-7b41-465d-919c-53391290abb5
  Args:
    target: :PrincessAuroraPavlovnaDemidovaDiSanDonato
    source: :PrincePaulOfYugoslavia
    relation: :hasMother
  AssignClass (04869794-6af4-429b-b91b-feafc7225747)
 Call ID: 04869794-6af4-429b-b91b-feafc7225747
  Args:
    type: :Man
    source: :PrinceNicholasOfGreeceAndDenmark
  AssignClass (f0458e94-2f19-41fd-bdee-e14d7d63ff56)
 Call ID: f0458e94-2f19-41fd-bdee-e14d7d63ff56
  Args:
    source: :PrinceNicholasOfGreeceAndDenmark
    type: :Person
  AddTriple (0e915544-36e5-42f5-8406-7c948a059627)
 Call ID: 0e915544-36e5-42f5-8406-7c948a059627
  Args:
    source: :PrincessOlgaOfGreeceAndDenmark
    relation: :hasFather
    target: :PrinceNicholasOfGreeceAndDenmark
  Finish (86615607-b1e5-4e5a-a065-8f51f008164c)
 Call ID: 86615607-b1e5-4e5a-a065-8f51f008164c
  Args: