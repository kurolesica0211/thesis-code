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
Prince Alexander of Yugoslavia (Serbian: Александар П. Карађорђевић / Aleksandar P. Karađorđević; 13 August 1924 – 12 May 2016) was the elder son of Prince Paul, who served as Regent of Yugoslavia in the 1930s, and his wife, Princess Olga of Greece and Denmark.
Birth and education

Alexander was born at White Lodge, Richmond Park, United Kingdom.
As a nephew of Princess Marina, Duchess of Kent (née of Greece and Denmark), he was a first cousin of Prince Edward, Duke of Kent, Prince Michael of Kent, and Princess Alexandra of Kent; he was also a first cousin once removed of Prince Philip, Duke of Edinburgh.
Marriages and family

He took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On 12 February 1955, Alexander married Princess Maria Pia of Savoy, daughter of King Umberto II of Italy and of his wife, Princess Marie José of Belgium.
The couple had met on 22 August 1954 during the royal cruise of the Agamemnon, hosted by King Paul and Queen Frederica of Greece.
Alexander and Maria Pia have twin sons born in 1958:
Alexander and Maria Pia divorced in 1967, and in 2003 she married Prince Michel of Bourbon-Parma, himself divorced from Princess Yolande de Broglie-Revel.
On 2 November 1973, in a civil ceremony in Paris, Alexander married Princess Barbara Eleonore Marie of Liechtenstein(born 9 July 1942), daughter of Prince Johannes of Liechtenstein (first cousin once removed to Prince Hans-Adam II of Liechtenstein) and Countess Karoline of Ledebur-Wicheln (aunt of Hans Adam's late wife Marie, Princess of Liechtenstein).
On 28 October 1995 Prince Alexander and Princess Barbara were married in the Orthodox faith in
Oplenac, and had issue:


Flying career

The Prince wished to serve in the British Royal Air Force during World War Two, but was initially prevented by his father's political affiliations.
He was eventually commissioned in the RAF through the intervention of Prince George, Duke of Kent, his uncle.
Associations

Alexander was one of the four founding members of the Serbian Unity Congress.
On 17 February 2008, Alexander issued a statement condemning the declaration of independence by Kosovo.
On the occasion of Prince Alexander's 90th birthday on 13 August 2014, a celebration of his life in words and pictures appeared in that month's UK magazine Majesty.
Death

Prince Alexander died on 12 May 2016 in Paris, where he and his wife had lived for many years.
He was buried at Oplenac, Serbia, with his parents and brother, his coffin being carried by Serbian Air Force fighter pilots.



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
  AssignClass (6b3b1897-086d-4b4a-8e9c-c151d57fc2ae)
 Call ID: 6b3b1897-086d-4b4a-8e9c-c151d57fc2ae
  Args:
    source: Prince_Alexander_of_Yugoslavia
    type: :Man
  AssignClass (bc54ce1a-e059-45a0-8a72-20738a1beeff)
 Call ID: bc54ce1a-e059-45a0-8a72-20738a1beeff
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (dff8bbb2-8c38-4e25-b2e1-36dcd069b71e)
 Call ID: dff8bbb2-8c38-4e25-b2e1-36dcd069b71e
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AddLiteral (8e9629b0-4660-41cf-9bc2-a1cb6377654d)
 Call ID: 8e9629b0-4660-41cf-9bc2-a1cb6377654d
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1924
    source: Prince_Alexander_of_Yugoslavia
  AddLiteral (39a69462-d0a4-42d0-b3dc-cc4344bf5580)
 Call ID: 39a69462-d0a4-42d0-b3dc-cc4344bf5580
  Args:
    literal_value: 2016
    source: Prince_Alexander_of_Yugoslavia
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (a066e2d3-6994-4948-a8d7-98b2d5551063)
 Call ID: a066e2d3-6994-4948-a8d7-98b2d5551063
  Args:
    source: Prince_Alexander_of_Yugoslavia
    target: Prince_Paul_of_Yugoslavia
    relation: :hasFather
  AddTriple (6fca62e2-6400-46ad-8841-d1eaa8e356d7)
 Call ID: 6fca62e2-6400-46ad-8841-d1eaa8e356d7
  Args:
    relation: :hasMother
    target: Princess_Olga_of_Greece_and_Denmark
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (9fc69d44-dcc6-4a03-a1fb-a4ff2d55b6b8)
 Call ID: 9fc69d44-dcc6-4a03-a1fb-a4ff2d55b6b8
  Args:
    source: Princess_Maria_Pia_of_Savoy
    type: :Woman
  AddTriple (d323bbfa-0752-4eb2-858f-086715384128)
 Call ID: d323bbfa-0752-4eb2-858f-086715384128
  Args:
    source: Prince_Alexander_of_Yugoslavia
    target: Princess_Maria_Pia_of_Savoy
    relation: :hasRelation
  AddLiteral (67530aab-4388-41c3-a4f2-5391a306755c)
 Call ID: 67530aab-4388-41c3-a4f2-5391a306755c
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1955
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (d2c1d37d-0531-43a0-aab9-3496aea33e06)
 Call ID: d2c1d37d-0531-43a0-aab9-3496aea33e06
  Args:
    type: :Man
    source: King_Umberto_II_of_Italy
  AssignClass (ecfe0316-d0e0-4ac0-ac23-b98f761859bf)
 Call ID: ecfe0316-d0e0-4ac0-ac23-b98f761859bf
  Args:
    source: Princess_Marie_Jose_of_Belgium
    type: :Woman
  AddTriple (00c6fa2c-054a-4bed-80fc-2bbb2add0dfd)
 Call ID: 00c6fa2c-054a-4bed-80fc-2bbb2add0dfd
  Args:
    relation: :hasFather
    source: Princess_Maria_Pia_of_Savoy
    target: King_Umberto_II_of_Italy
  AddTriple (715e7c5d-9e06-416f-9adb-85faf8d60e6e)
 Call ID: 715e7c5d-9e06-416f-9adb-85faf8d60e6e
  Args:
    target: Princess_Marie_Jose_of_Belgium
    source: Princess_Maria_Pia_of_Savoy
    relation: :hasMother
  AssignClass (34e89485-cc84-4ac6-978c-1bee54b0fafc)
 Call ID: 34e89485-cc84-4ac6-978c-1bee54b0fafc
  Args:
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    type: :Woman
  AddTriple (10fe373d-0ecc-4c9f-be9f-d2c173850090)
 Call ID: 10fe373d-0ecc-4c9f-be9f-d2c173850090
  Args:
    relation: :hasRelation
    target: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    source: Prince_Alexander_of_Yugoslavia
  AddLiteral (b059e72e-3f43-4ec2-9c7d-60c550ce3e37)
 Call ID: b059e72e-3f43-4ec2-9c7d-60c550ce3e37
  Args:
    source: Prince_Alexander_of_Yugoslavia
    literal_value: 1973
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (533f846c-ff98-445f-8742-24fdd2313d22)
 Call ID: 533f846c-ff98-445f-8742-24fdd2313d22
  Args:
    source: Prince_Johannes_of_Liechtenstein
    type: :Man
  AssignClass (fc80e24a-4567-4e6e-aa85-6c90cc054be9)
 Call ID: fc80e24a-4567-4e6e-aa85-6c90cc054be9
  Args:
    type: :Woman
    source: Countess_Karoline_of_Ledebur-Wicheln
  AddTriple (8f83745e-3531-4f51-ac70-8091f83a4529)
 Call ID: 8f83745e-3531-4f51-ac70-8091f83a4529
  Args:
    target: Prince_Johannes_of_Liechtenstein
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    relation: :hasFather
  AddTriple (1e8cc20e-f8ff-4c08-9304-eafbbe8aa5e0)
 Call ID: 1e8cc20e-f8ff-4c08-9304-eafbbe8aa5e0
  Args:
    relation: :hasMother
    target: Countess_Karoline_of_Ledebur-Wicheln
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AssignClass (1989c82a-89ec-44e5-afe9-77c231111c30)
 Call ID: 1989c82a-89ec-44e5-afe9-77c231111c30
  Args:
    source: Prince_Michel_of_Bourbon-Parma
    type: :Man
  AddTriple (1ae3bf86-8783-4453-ac37-ba65eceffb11)
 Call ID: 1ae3bf86-8783-4453-ac37-ba65eceffb11
  Args:
    source: Princess_Maria_Pia_of_Savoy
    target: Prince_Michel_of_Bourbon-Parma
    relation: :hasRelation
  AssignClass (82f04004-30d7-4f4d-a712-c8d0618179da)
 Call ID: 82f04004-30d7-4f4d-a712-c8d0618179da
  Args:
    source: Princess_Yolande_de_Broglie-Revel
    type: :Woman
  AddTriple (7471b654-99ea-4465-9b9e-e3ccb1d76f91)
 Call ID: 7471b654-99ea-4465-9b9e-e3ccb1d76f91
  Args:
    target: Princess_Yolande_de_Broglie-Revel
    source: Prince_Michel_of_Bourbon-Parma
    relation: :hasRelation
  AssignClass (3ed2b324-4a2a-4e27-871c-5d74649e896a)
 Call ID: 3ed2b324-4a2a-4e27-871c-5d74649e896a
  Args:
    type: :Man
    source: Prince_George_Duke_of_Kent
  AddTriple (4106df84-bb17-4ab4-af00-60574e324d24)
 Call ID: 4106df84-bb17-4ab4-af00-60574e324d24
  Args:
    target: Prince_George_Duke_of_Kent
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasRelation
  Finish (5a535baf-2d15-4725-bbfc-ebe78d7249e9)
 Call ID: 5a535baf-2d15-4725-bbfc-ebe78d7249e9
  Args: