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
  AssignClass (a9bae79b-469d-48db-b1f3-82a1b0c9269a)
 Call ID: a9bae79b-469d-48db-b1f3-82a1b0c9269a
  Args:
    source: :PrinceNikolaOfYugoslavia
    type: :Man
  AssignClass (4bb93490-8cb6-4c33-a5cb-27fb0d6f5b40)
 Call ID: 4bb93490-8cb6-4c33-a5cb-27fb0d6f5b40
  Args:
    source: :PrinceNikolaOfYugoslavia
    type: :Person
  AddLiteral (34489442-97e3-462a-95b2-512e64d56c33)
 Call ID: 34489442-97e3-462a-95b2-512e64d56c33
  Args:
    literal_value: 1928
    literal_type: xsd:integer
    source: :PrinceNikolaOfYugoslavia
    relation: :hasBirthYear
  AddLiteral (0a3ea183-9c8d-4aea-968b-8724593f8194)
 Call ID: 0a3ea183-9c8d-4aea-968b-8724593f8194
  Args:
    source: :PrinceNikolaOfYugoslavia
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1954
  AddLiteral (cedd46d8-2cb5-4a33-a480-f58e22c80bb7)
 Call ID: cedd46d8-2cb5-4a33-a480-f58e22c80bb7
  Args:
    literal_value: Prince Nicholas
    literal_type: xsd:string
    source: :PrinceNikolaOfYugoslavia
    relation: :alsoKnownAs
  AddLiteral (9c9cd8c9-ec43-4671-9ca7-1afcb23df09c)
 Call ID: 9c9cd8c9-ec43-4671-9ca7-1afcb23df09c
  Args:
    literal_value: Nikola Karađorđević
    relation: :alsoKnownAs
    source: :PrinceNikolaOfYugoslavia
    literal_type: xsd:string
  AddLiteral (c184caa0-32d0-4cc1-a7f9-e6c655e17e53)
 Call ID: c184caa0-32d0-4cc1-a7f9-e6c655e17e53
  Args:
    literal_type: xsd:string
    relation: :knownAs
    source: :PrinceNikolaOfYugoslavia
    literal_value: Nicky
  AssignClass (5552df8a-4a5b-40f5-9c06-0a1fb6229829)
 Call ID: 5552df8a-4a5b-40f5-9c06-0a1fb6229829
  Args:
    type: :Man
    source: :PrincePaulOfYugoslavia
  AssignClass (43188b5e-687f-43e2-95ea-871c58507a5c)
 Call ID: 43188b5e-687f-43e2-95ea-871c58507a5c
  Args:
    source: :PrincePaulOfYugoslavia
    type: :Person
  AddTriple (899c35c8-4fc3-42ac-a7aa-9bc697ec0f5f)
 Call ID: 899c35c8-4fc3-42ac-a7aa-9bc697ec0f5f
  Args:
    target: :PrincePaulOfYugoslavia
    source: :PrinceNikolaOfYugoslavia
    relation: :hasFather
  AssignClass (3e771675-17e1-4fe3-9c35-9497270fa1d6)
 Call ID: 3e771675-17e1-4fe3-9c35-9497270fa1d6
  Args:
    source: :PrincessOlgaOfGreeceAndDenmark
    type: :Woman
  AssignClass (7954a064-2d3a-4b35-8c31-633534c888e9)
 Call ID: 7954a064-2d3a-4b35-8c31-633534c888e9
  Args:
    type: :Person
    source: :PrincessOlgaOfGreeceAndDenmark
  AddTriple (70a66551-3c3e-4607-abe2-f0004a94231c)
 Call ID: 70a66551-3c3e-4607-abe2-f0004a94231c
  Args:
    source: :PrinceNikolaOfYugoslavia
    target: :PrincessOlgaOfGreeceAndDenmark
    relation: :hasMother
  AssignClass (10142fb1-b5e4-41a0-8c2b-7988275b999a)
 Call ID: 10142fb1-b5e4-41a0-8c2b-7988275b999a
  Args:
    source: :PrinceAlexander
    type: :Man
  AssignClass (84089763-4e6e-4c64-a7ae-469afe643475)
 Call ID: 84089763-4e6e-4c64-a7ae-469afe643475
  Args:
    source: :PrinceAlexander
    type: :Person
  AddTriple (e6dcaf1f-425e-45bf-8939-66e84a03f2c8)
 Call ID: e6dcaf1f-425e-45bf-8939-66e84a03f2c8
  Args:
    relation: :hasBrother
    target: :PrinceAlexander
    source: :PrinceNikolaOfYugoslavia
  AssignClass (95cbf6aa-4357-47df-b113-c0331a4ad7cd)
 Call ID: 95cbf6aa-4357-47df-b113-c0331a4ad7cd
  Args:
    type: :Woman
    source: :PrincessElizabeth
  AssignClass (3d10e64d-f689-4f8d-84a4-eb1bfff9a76d)
 Call ID: 3d10e64d-f689-4f8d-84a4-eb1bfff9a76d
  Args:
    type: :Person
    source: :PrincessElizabeth
  AddTriple (c8c30f28-b493-4bd4-9215-c1c57c56f0c6)
 Call ID: c8c30f28-b493-4bd4-9215-c1c57c56f0c6
  Args:
    target: :PrincessElizabeth
    source: :PrinceNikolaOfYugoslavia
    relation: :hasSister
  AssignClass (2e820fa0-aa68-4598-b885-eb3c27f96e59)
 Call ID: 2e820fa0-aa68-4598-b885-eb3c27f96e59
  Args:
    type: :Woman
    source: :GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (2113f3bf-1ac6-4dad-9e04-3dbcf5b1c3ef)
 Call ID: 2113f3bf-1ac6-4dad-9e04-3dbcf5b1c3ef
  Args:
    type: :Person
    source: :GrandDuchessElenaVladimirovnaOfRussia
  AddTriple (a2e08579-7a16-445a-9696-1915dc563480)
 Call ID: a2e08579-7a16-445a-9696-1915dc563480
  Args:
    relation: :hasMother
    source: :PrincessOlgaOfGreeceAndDenmark
    target: :GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (fcfe9f47-a84b-4223-baa6-6bc9a40e7018)
 Call ID: fcfe9f47-a84b-4223-baa6-6bc9a40e7018
  Args:
    source: :PrincessElizabethCountessOfToerringJettenbach
    type: :Woman
  AssignClass (dadcb9fa-245a-4be9-afcc-4f02161b727c)
 Call ID: dadcb9fa-245a-4be9-afcc-4f02161b727c
  Args:
    source: :PrincessElizabethCountessOfToerringJettenbach
    type: :Person
  AssignClass (6b813423-b05f-47ed-a713-d59f4e2d4981)
 Call ID: 6b813423-b05f-47ed-a713-d59f4e2d4981
  Args:
    source: :PrincessMarinaDuchessOfKent
    type: :Woman
  AssignClass (a2d3e6d7-bf13-4752-abb8-ca3b53636a15)
 Call ID: a2d3e6d7-bf13-4752-abb8-ca3b53636a15
  Args:
    type: :Person
    source: :PrincessMarinaDuchessOfKent
  AssignClass (b649f858-087e-42ab-aa9e-37317f8c2ca2)
 Call ID: b649f858-087e-42ab-aa9e-37317f8c2ca2
  Args:
    type: :Man
    source: :ArsenKarađorđević
  AssignClass (55287ec9-e526-42a9-9ece-f17ebad2a95a)
 Call ID: 55287ec9-e526-42a9-9ece-f17ebad2a95a
  Args:
    type: :Person
    source: :ArsenKarađorđević
  AssignClass (79876cb4-9ba9-4e2e-a980-3457f43a7434)
 Call ID: 79876cb4-9ba9-4e2e-a980-3457f43a7434
  Args:
    type: :Woman
    source: :PrincessAuroraPavlovnaDemidovaDiSanDonato
  AssignClass (cc49c143-085e-4041-8473-07ca24974fef)
 Call ID: cc49c143-085e-4041-8473-07ca24974fef
  Args:
    type: :Person
    source: :PrincessAuroraPavlovnaDemidovaDiSanDonato
  AddTriple (07d6f9df-c9aa-469e-9972-ef472b7d8f0c)
 Call ID: 07d6f9df-c9aa-469e-9972-ef472b7d8f0c
  Args:
    source: :PrincePaulOfYugoslavia
    target: :ArsenKarađorđević
    relation: :hasFather
  AddTriple (bc4c1f26-daf4-46f0-adea-139752175e9c)
 Call ID: bc4c1f26-daf4-46f0-adea-139752175e9c
  Args:
    relation: :hasMother
    source: :PrincePaulOfYugoslavia
    target: :PrincessAuroraPavlovnaDemidovaDiSanDonato
  AssignClass (9878385d-194f-4006-b662-7f0b41d575a7)
 Call ID: 9878385d-194f-4006-b662-7f0b41d575a7
  Args:
    source: :PrinceNicholasOfGreeceAndDenmark
    type: :Man
  AssignClass (475b4497-d51b-4812-9401-0d2a2f6067d6)
 Call ID: 475b4497-d51b-4812-9401-0d2a2f6067d6
  Args:
    source: :PrinceNicholasOfGreeceAndDenmark
    type: :Person
  AddTriple (709ef76e-30e9-4c45-918d-4a3ad7e773ff)
 Call ID: 709ef76e-30e9-4c45-918d-4a3ad7e773ff
  Args:
    relation: :hasFather
    source: :PrincessOlgaOfGreeceAndDenmark
    target: :PrinceNicholasOfGreeceAndDenmark
  AddTriple (bc6c9c9f-8193-408c-8ca4-932febec7273)
 Call ID: bc6c9c9f-8193-408c-8ca4-932febec7273
  Args:
    source: :PrincessOlgaOfGreeceAndDenmark
    target: :GrandDuchessElenaVladimirovnaOfRussia
    relation: :hasMother
  Finish (fde3a185-940c-4412-a378-061cd1300725)
 Call ID: fde3a185-940c-4412-a378-061cd1300725
  Args: