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
  AssignClass (9adbd065-e6dd-4668-9652-b14b995ff223)
 Call ID: 9adbd065-e6dd-4668-9652-b14b995ff223
  Args:
    type: :Man
    source: PrinceNikolaOfYugoslavia
  AssignClass (663b1ab3-39e7-4569-a889-1e2a1c3ceb84)
 Call ID: 663b1ab3-39e7-4569-a889-1e2a1c3ceb84
  Args:
    source: PrinceNikolaOfYugoslavia
    type: :Person
  AddLiteral (8e6cd28b-1c21-42bf-94c3-c80535d6c751)
 Call ID: 8e6cd28b-1c21-42bf-94c3-c80535d6c751
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :hasBirthYear
    literal_value: 1928
    literal_type: xsd:integer
  AddLiteral (d158ff18-1d81-44a1-add0-5ce3b4cd55d4)
 Call ID: d158ff18-1d81-44a1-add0-5ce3b4cd55d4
  Args:
    literal_value: 1954
    relation: :hasDeathYear
    source: PrinceNikolaOfYugoslavia
    literal_type: xsd:integer
  AddLiteral (c4922dd3-43ac-4efd-934d-fd855b5fa639)
 Call ID: c4922dd3-43ac-4efd-934d-fd855b5fa639
  Args:
    literal_type: xsd:string
    source: PrinceNikolaOfYugoslavia
    relation: :alsoKnownAs
    literal_value: Prince Nicholas
  AddLiteral (c1d48d20-94dc-4b7f-8b0e-1d94275eca96)
 Call ID: c1d48d20-94dc-4b7f-8b0e-1d94275eca96
  Args:
    source: PrinceNikolaOfYugoslavia
    literal_value: Nikola Karađorđević
    relation: :alsoKnownAs
    literal_type: xsd:string
  AddLiteral (f302c82a-285e-4084-8d29-b87004c4b773)
 Call ID: f302c82a-285e-4084-8d29-b87004c4b773
  Args:
    literal_type: xsd:string
    source: PrinceNikolaOfYugoslavia
    literal_value: Nicky
    relation: :knownAs
  AssignClass (ae9fac01-a365-46f4-a1d2-33dc74befff2)
 Call ID: ae9fac01-a365-46f4-a1d2-33dc74befff2
  Args:
    type: :Man
    source: PrincePaulOfYugoslavia
  AssignClass (db72af42-054c-4ac3-ba8f-11ea572e02b7)
 Call ID: db72af42-054c-4ac3-ba8f-11ea572e02b7
  Args:
    source: PrincePaulOfYugoslavia
    type: :Person
  AssignClass (137d3774-0b7a-4215-890e-5de20c003139)
 Call ID: 137d3774-0b7a-4215-890e-5de20c003139
  Args:
    source: PrincessOlgaOfGreeceAndDenmark
    type: :Woman
  AssignClass (e0245618-5144-479a-94d8-a1b0b3e01b03)
 Call ID: e0245618-5144-479a-94d8-a1b0b3e01b03
  Args:
    source: PrincessOlgaOfGreeceAndDenmark
    type: :Person
  AddTriple (c4827c6c-466c-4d23-8fde-c83933aeef28)
 Call ID: c4827c6c-466c-4d23-8fde-c83933aeef28
  Args:
    relation: :hasFather
    target: PrincePaulOfYugoslavia
    source: PrinceNikolaOfYugoslavia
  AddTriple (01eb5493-1817-4dad-9fb9-e82196637136)
 Call ID: 01eb5493-1817-4dad-9fb9-e82196637136
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :hasMother
    target: PrincessOlgaOfGreeceAndDenmark
  AssignClass (0bf82747-0d46-44c1-87a3-9550ac55df50)
 Call ID: 0bf82747-0d46-44c1-87a3-9550ac55df50
  Args:
    type: :Man
    source: PrinceAlexander
  AssignClass (9d4fd2de-b143-4cd0-8dd9-ff64adc9dbbc)
 Call ID: 9d4fd2de-b143-4cd0-8dd9-ff64adc9dbbc
  Args:
    source: PrinceAlexander
    type: :Person
  AssignClass (53e99e17-8e3e-4184-aecc-e39e58708933)
 Call ID: 53e99e17-8e3e-4184-aecc-e39e58708933
  Args:
    type: :Woman
    source: PrincessElizabeth
  AssignClass (8b6b7183-74ad-4f72-a53f-d22edd0ffbea)
 Call ID: 8b6b7183-74ad-4f72-a53f-d22edd0ffbea
  Args:
    type: :Person
    source: PrincessElizabeth
  AddTriple (397a88ea-b64f-41ba-a5ff-65bd40d84b63)
 Call ID: 397a88ea-b64f-41ba-a5ff-65bd40d84b63
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :hasBrother
    target: PrinceAlexander
  AddTriple (16eed0da-22bf-4126-813c-56817f2c98eb)
 Call ID: 16eed0da-22bf-4126-813c-56817f2c98eb
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :hasSister
    target: PrincessElizabeth
  AssignClass (bdc59cf7-2d9d-47b7-b9ba-4a2b8d4838f4)
 Call ID: bdc59cf7-2d9d-47b7-b9ba-4a2b8d4838f4
  Args:
    source: ArsenKarađorđević
    type: :Man
  AssignClass (2ad5cb1b-c5b1-461d-8536-9daf093237cb)
 Call ID: 2ad5cb1b-c5b1-461d-8536-9daf093237cb
  Args:
    type: :Person
    source: ArsenKarađorđević
  AssignClass (abb05fb8-dd86-4bf9-a4e3-93aa3d695aee)
 Call ID: abb05fb8-dd86-4bf9-a4e3-93aa3d695aee
  Args:
    source: PrincessAuroraPavlovnaDemidovaDiSanDonato
    type: :Woman
  AssignClass (fb3612a1-7682-4e27-87f8-a9b16f2457ca)
 Call ID: fb3612a1-7682-4e27-87f8-a9b16f2457ca
  Args:
    type: :Person
    source: PrincessAuroraPavlovnaDemidovaDiSanDonato
  AddTriple (25abbb23-ba2e-4819-9f51-d65e558d7f0f)
 Call ID: 25abbb23-ba2e-4819-9f51-d65e558d7f0f
  Args:
    relation: :hasFather
    target: ArsenKarađorđević
    source: PrincePaulOfYugoslavia
  AddTriple (de166014-f6e4-45b2-b8af-087498e831c6)
 Call ID: de166014-f6e4-45b2-b8af-087498e831c6
  Args:
    relation: :hasMother
    target: PrincessAuroraPavlovnaDemidovaDiSanDonato
    source: PrincePaulOfYugoslavia
  AssignClass (fda6d5e6-8b5b-4ecb-9847-33d8ab0d7d2d)
 Call ID: fda6d5e6-8b5b-4ecb-9847-33d8ab0d7d2d
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    type: :Man
  AssignClass (47d3ca73-d49d-459c-9f32-ad9b170c642c)
 Call ID: 47d3ca73-d49d-459c-9f32-ad9b170c642c
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    type: :Person
  AssignClass (17d291c8-b8d5-4c38-84f1-6691d2d1004c)
 Call ID: 17d291c8-b8d5-4c38-84f1-6691d2d1004c
  Args:
    source: GrandDuchessElenaVladimirovnaOfRussia
    type: :Woman
  AssignClass (3ecfe747-ffce-4ca9-afc8-ba544fc75cb5)
 Call ID: 3ecfe747-ffce-4ca9-afc8-ba544fc75cb5
  Args:
    source: GrandDuchessElenaVladimirovnaOfRussia
    type: :Person
  AddTriple (4db03e4c-a2da-4fb3-9578-0aa20f760d15)
 Call ID: 4db03e4c-a2da-4fb3-9578-0aa20f760d15
  Args:
    relation: :hasFather
    target: PrinceNicholasOfGreeceAndDenmark
    source: PrincessOlgaOfGreeceAndDenmark
  AddTriple (f34877ca-1057-48aa-86a5-73cc5b181558)
 Call ID: f34877ca-1057-48aa-86a5-73cc5b181558
  Args:
    source: PrincessOlgaOfGreeceAndDenmark
    relation: :hasMother
    target: GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (aa48c89b-5f44-4fb0-ae74-4f9f41e0cdb2)
 Call ID: aa48c89b-5f44-4fb0-ae74-4f9f41e0cdb2
  Args:
    type: :Woman
    source: PrincessElizabethCountessOfToerringJettenbach
  AssignClass (142073fa-9a87-40cb-8aab-32048c74c2b9)
 Call ID: 142073fa-9a87-40cb-8aab-32048c74c2b9
  Args:
    source: PrincessElizabethCountessOfToerringJettenbach
    type: :Person
  AssignClass (0ddfa26e-4b04-44d5-ab1e-a6ffbcbd0cc7)
 Call ID: 0ddfa26e-4b04-44d5-ab1e-a6ffbcbd0cc7
  Args:
    type: :Woman
    source: PrincessMarinaDuchessOfKent
  AssignClass (0f620d41-296a-4ac9-8e91-ddefb02527ea)
 Call ID: 0f620d41-296a-4ac9-8e91-ddefb02527ea
  Args:
    source: PrincessMarinaDuchessOfKent
    type: :Person
  AddTriple (85baa3f3-2a2c-4196-8411-caa2247e99c8)
 Call ID: 85baa3f3-2a2c-4196-8411-caa2247e99c8
  Args:
    source: PrincessOlgaOfGreeceAndDenmark
    relation: :hasSister
    target: PrincessElizabethCountessOfToerringJettenbach
  AddTriple (fb1c93e9-d08b-425d-b598-91c4bd6f8774)
 Call ID: fb1c93e9-d08b-425d-b598-91c4bd6f8774
  Args:
    source: PrincessOlgaOfGreeceAndDenmark
    relation: :hasSister
    target: PrincessMarinaDuchessOfKent
  Finish (773ba0e7-c16c-4ba8-9b3c-622350c513cb)
 Call ID: 773ba0e7-c16c-4ba8-9b3c-622350c513cb
  Args: