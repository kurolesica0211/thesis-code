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
  AssignClass (3e49f978-c2ed-4abe-ada4-a7b94bffc35a)
 Call ID: 3e49f978-c2ed-4abe-ada4-a7b94bffc35a
  Args:
    source: PrinceNikolaOfYugoslavia
    type: :Man
  AssignClass (d98cc60d-9211-4e3c-9888-961d9a4eb4e2)
 Call ID: d98cc60d-9211-4e3c-9888-961d9a4eb4e2
  Args:
    source: PrinceNikolaOfYugoslavia
    type: :Person
  AddLiteral (155f41c7-4387-46cd-84b1-6f61fa056cc2)
 Call ID: 155f41c7-4387-46cd-84b1-6f61fa056cc2
  Args:
    literal_type: xsd:integer
    source: PrinceNikolaOfYugoslavia
    relation: :hasBirthYear
    literal_value: 1928
  AddLiteral (94d38901-d4e4-4a0b-8052-554cfd9af9cf)
 Call ID: 94d38901-d4e4-4a0b-8052-554cfd9af9cf
  Args:
    literal_value: 1954
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: PrinceNikolaOfYugoslavia
  AddLiteral (860a19af-d469-4d01-b895-aee1c90b9d3b)
 Call ID: 860a19af-d469-4d01-b895-aee1c90b9d3b
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :alsoKnownAs
    literal_type: xsd:string
    literal_value: Prince Nicholas
  AddLiteral (6258dbfd-3e2e-45f7-836e-522745f1ee40)
 Call ID: 6258dbfd-3e2e-45f7-836e-522745f1ee40
  Args:
    literal_type: xsd:string
    source: PrinceNikolaOfYugoslavia
    relation: :alsoKnownAs
    literal_value: Nikola Karađorđević
  AddLiteral (94e4576b-9955-4acb-9744-5dd6d7015e71)
 Call ID: 94e4576b-9955-4acb-9744-5dd6d7015e71
  Args:
    literal_value: Nicky
    literal_type: xsd:string
    relation: :knownAs
    source: PrinceNikolaOfYugoslavia
  AssignClass (f044079c-5766-4561-a919-1b0e9792ce43)
 Call ID: f044079c-5766-4561-a919-1b0e9792ce43
  Args:
    source: PrincePaulOfYugoslavia
    type: :Man
  AssignClass (e4cb0ecb-139e-4f60-9a35-522e003cffec)
 Call ID: e4cb0ecb-139e-4f60-9a35-522e003cffec
  Args:
    source: PrincePaulOfYugoslavia
    type: :Person
  AssignClass (c238dc3e-a578-4467-89ca-4ef9381ad8b4)
 Call ID: c238dc3e-a578-4467-89ca-4ef9381ad8b4
  Args:
    source: PrincessOlgaOfGreeceAndDenmark
    type: :Woman
  AssignClass (3ae15214-021b-45e9-9cc3-4f9ea7a23cee)
 Call ID: 3ae15214-021b-45e9-9cc3-4f9ea7a23cee
  Args:
    type: :Person
    source: PrincessOlgaOfGreeceAndDenmark
  AddTriple (c60ba131-e8ac-414b-9142-8a7343bb4931)
 Call ID: c60ba131-e8ac-414b-9142-8a7343bb4931
  Args:
    target: PrincePaulOfYugoslavia
    relation: :hasFather
    source: PrinceNikolaOfYugoslavia
  AddTriple (2131851c-82bd-4ad2-a8df-8b06296ea02d)
 Call ID: 2131851c-82bd-4ad2-a8df-8b06296ea02d
  Args:
    target: PrincessOlgaOfGreeceAndDenmark
    relation: :hasMother
    source: PrinceNikolaOfYugoslavia
  AssignClass (0f189feb-e703-4382-a36a-6a06003fff50)
 Call ID: 0f189feb-e703-4382-a36a-6a06003fff50
  Args:
    type: :Man
    source: PrinceAlexander
  AssignClass (de255fcb-9301-4df3-b55f-7d8c90bbfd62)
 Call ID: de255fcb-9301-4df3-b55f-7d8c90bbfd62
  Args:
    type: :Person
    source: PrinceAlexander
  AddTriple (10c1ed64-6731-4ef3-a735-9fab19f80cbd)
 Call ID: 10c1ed64-6731-4ef3-a735-9fab19f80cbd
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :hasBrother
    target: PrinceAlexander
  AssignClass (e780dccd-c1cd-42b1-9231-85d858f7c208)
 Call ID: e780dccd-c1cd-42b1-9231-85d858f7c208
  Args:
    type: :Woman
    source: PrincessElizabeth
  AssignClass (23650d67-d6ab-4870-b58c-2fc62170d240)
 Call ID: 23650d67-d6ab-4870-b58c-2fc62170d240
  Args:
    type: :Person
    source: PrincessElizabeth
  AddTriple (0342f4a7-3270-4b50-9599-be84102731a6)
 Call ID: 0342f4a7-3270-4b50-9599-be84102731a6
  Args:
    target: PrincessElizabeth
    source: PrinceNikolaOfYugoslavia
    relation: :hasSister
  AssignClass (47781c53-f443-46cd-80c5-fe8c62ce6468)
 Call ID: 47781c53-f443-46cd-80c5-fe8c62ce6468
  Args:
    type: :Woman
    source: GrandDuchessElenaVladimirovnaOfRussia
  AssignClass (a244b691-d35d-4cc7-b3cc-d57625fc7ad2)
 Call ID: a244b691-d35d-4cc7-b3cc-d57625fc7ad2
  Args:
    source: GrandDuchessElenaVladimirovnaOfRussia
    type: :Person
  AssignClass (f012a308-e974-4eca-9f04-85be8fb58cb7)
 Call ID: f012a308-e974-4eca-9f04-85be8fb58cb7
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    type: :Man
  AssignClass (dd98309d-6231-4eda-a9b3-dc39a2df0a6c)
 Call ID: dd98309d-6231-4eda-a9b3-dc39a2df0a6c
  Args:
    source: PrinceNicholasOfGreeceAndDenmark
    type: :Person
  AddTriple (7368b6f3-8a1a-4bd4-bee7-f696ad42c437)
 Call ID: 7368b6f3-8a1a-4bd4-bee7-f696ad42c437
  Args:
    relation: :hasFather
    source: PrinceNikolaOfYugoslavia
    target: ArsenKarađorđević
  AddTriple (a5ad5d17-f6ac-4372-ab1f-2120b2b21079)
 Call ID: a5ad5d17-f6ac-4372-ab1f-2120b2b21079
  Args:
    source: PrinceNikolaOfYugoslavia
    relation: :hasMother
    target: PrincessAuroraPavlovnaDemidovaDiSanDonato
  AssignClass (24579895-cb8c-4b10-bba5-b030cd0d046f)
 Call ID: 24579895-cb8c-4b10-bba5-b030cd0d046f
  Args:
    source: ArsenKarađorđević
    type: :Man
  AssignClass (92d32f57-0a10-433c-944b-2b6b58dda48d)
 Call ID: 92d32f57-0a10-433c-944b-2b6b58dda48d
  Args:
    source: ArsenKarađorđević
    type: :Person
  AssignClass (f371cad6-6f7e-4f67-ab5d-8b1bb2c02405)
 Call ID: f371cad6-6f7e-4f67-ab5d-8b1bb2c02405
  Args:
    source: PrincessAuroraPavlovnaDemidovaDiSanDonato
    type: :Woman
  AssignClass (1ecd799e-7fb4-4e39-b6ac-d0f1df80559b)
 Call ID: 1ecd799e-7fb4-4e39-b6ac-d0f1df80559b
  Args:
    source: PrincessAuroraPavlovnaDemidovaDiSanDonato
    type: :Person
  AddTriple (11fc371d-71bd-4eca-a143-9fb2d1f08deb)
 Call ID: 11fc371d-71bd-4eca-a143-9fb2d1f08deb
  Args:
    target: GrandDuchessElenaVladimirovnaOfRussia
    relation: :hasMother
    source: PrincessOlgaOfGreeceAndDenmark
  AddTriple (726a1dca-3d53-4026-b92c-d7dc67b69c0a)
 Call ID: 726a1dca-3d53-4026-b92c-d7dc67b69c0a
  Args:
    target: PrinceNicholasOfGreeceAndDenmark
    relation: :hasFather
    source: PrincessOlgaOfGreeceAndDenmark
  AssignClass (a557359a-da60-4386-9cce-c5eb8c8e211e)
 Call ID: a557359a-da60-4386-9cce-c5eb8c8e211e
  Args:
    source: PrincessElizabethCountessOfToerringJettenbach
    type: :Woman
  AssignClass (5c55e8b0-9370-4121-b684-c74b2575f6b6)
 Call ID: 5c55e8b0-9370-4121-b684-c74b2575f6b6
  Args:
    source: PrincessElizabethCountessOfToerringJettenbach
    type: :Person
  AssignClass (21005d99-3096-45e3-aebd-6a0c19a885fd)
 Call ID: 21005d99-3096-45e3-aebd-6a0c19a885fd
  Args:
    type: :Woman
    source: PrincessMarinaDuchessOfKent
  AssignClass (fe2b12f8-64f9-4c8e-b2ee-fd2842d8a95b)
 Call ID: fe2b12f8-64f9-4c8e-b2ee-fd2842d8a95b
  Args:
    type: :Person
    source: PrincessMarinaDuchessOfKent
  AddTriple (3f6d5b34-33fa-4469-98fe-e76ea0b4affc)
 Call ID: 3f6d5b34-33fa-4469-98fe-e76ea0b4affc
  Args:
    relation: :isAuntOf
    source: PrincessElizabethCountessOfToerringJettenbach
    target: PrinceNikolaOfYugoslavia
  AddTriple (dc935096-f836-448e-b17f-4946b4f0bc8d)
 Call ID: dc935096-f836-448e-b17f-4946b4f0bc8d
  Args:
    source: PrincessMarinaDuchessOfKent
    relation: :isAuntOf
    target: PrinceNikolaOfYugoslavia
  Finish (32d6ca39-77c7-4119-863b-d76045c988fe)
 Call ID: 32d6ca39-77c7-4119-863b-d76045c988fe
  Args: