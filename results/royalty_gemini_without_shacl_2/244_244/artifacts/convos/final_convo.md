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


Alexander Karageorgevitch (Serbian Cyrillic: Александар Карађорђевић, romanized: Aleksandar Karađorđević; born 15 January 1982), also known as Prince Alexander of Serbia and Yugoslavia or Prince Aleksandar III Karađorđević, is a member of the House of Karađorđević, the former ruling family of the defunct Kingdom of Yugoslavia.
Early life and education

Prince Alexander was born 15 January 1982 in Vienna, Virginia, Alexander is the third and youngest child of the last crown prince of Yugoslavia, Alexander, and his first wife, Princess Maria da Gloria of Orléans-Braganza.
His godparents are Queen Sofía of Spain, King Constantine II of Greece (first cousins of his father), and Princess Anne, Duchess of Calabria (first cousin of his mother).
Alexander lived in Virginia until 1984.
In 1982, Alexander and his twin brother were baptized by Lavrentije, Serbian Orthodox Bishop of Western Europe, at a castle in Villamanrique de la Condesa, near Seville, Spain.
Alexander's parents divorced in 1985.
After the divorce, his father married Katherine Clairy Batis later that year, while his mother married Ignacio, 19th Duke of Segorbe in the same year.
Through his mother, Alexander has two younger half-sisters, Sol María de la Blanca Medina y Orléans-Braganza, 54th Countess of Ampurias (b. 1986) and Ana Luna Medina y Orléans-Braganza, 17th Countess of Ricla (b. 1988).
Alexander was educated in London and Canterbury with his twin brother.
Alexander was at a graduate school at an American university completing a MFA degree in advertising (Art Direction).
Patronages

In Serbia he is Chairman of the Board of Directors of the Crown Prince Foundation for Education and Culture (since 2024).
Personal life

Prince Alexander attended the reburial of his grandparents King Peter II and Queen Alexandra, great-grandmother Queen Maria, and granduncle Prince Andrew in the Royal Family Mausoleum at Oplenac on 26 May 2013.
The Serbian Royal Regalia were placed over King Peter's coffin, having Alexander placing a diamond sabre near to the Karađorđević Crown.
In 2015, Alexander dated Dunja Kusturica, a daughter of Serbian filmmaker and musician Emir Kusturica.
At the time, their relationship was compared to one of Catherine and Prince William by Serbian media.
On 17 July 2015, Prince Alexander and his brothers were present at their father's 70th birthday celebration in Belgrade.
Ancestors

Alexander is a member of the House of Karađorđević.
Through his father, Alexander descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, and Alexander of Greece, and furthermore from emperors Nicholas I of Russia and Frederick III of the Germans and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through his mother, Alexander descends from the Emperor Pedro II of Brazil, and kings Louis Philippe I of France and Francis I of the Two Sicilies, and furthermore from Francis I, Holy Roman Emperor and king Charles III of Spain.



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
  AssignClass (e62e9f40-5c93-4376-afb9-2b3a7379fb84)
 Call ID: e62e9f40-5c93-4376-afb9-2b3a7379fb84
  Args:
    type: :Man
    source: Alexander_Karageorgevitch
  AssignClass (7db090ef-1ad9-4e1c-9779-e562df919afe)
 Call ID: 7db090ef-1ad9-4e1c-9779-e562df919afe
  Args:
    type: :Person
    source: Alexander_Karageorgevitch
  AddLiteral (8242282f-3408-49db-977f-ff453a8c07be)
 Call ID: 8242282f-3408-49db-977f-ff453a8c07be
  Args:
    relation: :hasBirthYear
    literal_value: 1982
    literal_type: xsd:integer
    source: Alexander_Karageorgevitch
  AddLiteral (c773dc2e-bf09-4184-a57a-2e46a3ec54c1)
 Call ID: c773dc2e-bf09-4184-a57a-2e46a3ec54c1
  Args:
    literal_type: xsd:string
    source: Alexander_Karageorgevitch
    relation: :alsoKnownAs
    literal_value: Prince Alexander of Serbia and Yugoslavia
  AddLiteral (b4ede78d-3699-4d10-a3fe-0935137c07d9)
 Call ID: b4ede78d-3699-4d10-a3fe-0935137c07d9
  Args:
    source: Alexander_Karageorgevitch
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Prince Aleksandar III Karađorđević
  AssignClass (ad6c6fa0-9cb8-4176-9c57-4073b7b6d704)
 Call ID: ad6c6fa0-9cb8-4176-9c57-4073b7b6d704
  Args:
    type: :Man
    source: Alexander_Yugoslavia_Sr
  AssignClass (25613853-3226-471b-863d-42de119de60f)
 Call ID: 25613853-3226-471b-863d-42de119de60f
  Args:
    type: :Person
    source: Alexander_Yugoslavia_Sr
  AssignClass (2ff73904-d33e-4d3d-8c5f-da0cc4114e0d)
 Call ID: 2ff73904-d33e-4d3d-8c5f-da0cc4114e0d
  Args:
    type: :Woman
    source: Maria_da_Gloria
  AssignClass (d0d0b72f-ed6f-4970-8a9b-3b24c7db1a52)
 Call ID: d0d0b72f-ed6f-4970-8a9b-3b24c7db1a52
  Args:
    type: :Person
    source: Maria_da_Gloria
  AddTriple (5b0aa63a-1dc7-4d60-b351-866fc5c4d02d)
 Call ID: 5b0aa63a-1dc7-4d60-b351-866fc5c4d02d
  Args:
    relation: :hasFather
    target: Alexander_Yugoslavia_Sr
    source: Alexander_Karageorgevitch
  AddTriple (acaf8398-8987-44d7-b884-26916086e35f)
 Call ID: acaf8398-8987-44d7-b884-26916086e35f
  Args:
    relation: :hasMother
    target: Maria_da_Gloria
    source: Alexander_Karageorgevitch
  AssignClass (e517ab12-0aea-4f55-a224-60367083c435)
 Call ID: e517ab12-0aea-4f55-a224-60367083c435
  Args:
    type: :Woman
    source: Katherine_Clairy_Batis
  AssignClass (8a74f1e0-dc0a-42eb-8a9e-04d2704ace55)
 Call ID: 8a74f1e0-dc0a-42eb-8a9e-04d2704ace55
  Args:
    type: :Person
    source: Katherine_Clairy_Batis
  AssignClass (174dc41f-e01d-4f6f-a939-6a647b798a72)
 Call ID: 174dc41f-e01d-4f6f-a939-6a647b798a72
  Args:
    type: :Man
    source: Ignacio_Duke_of_Segorbe
  AssignClass (cada5ffe-ff04-4ca7-b0f5-7867b62be8eb)
 Call ID: cada5ffe-ff04-4ca7-b0f5-7867b62be8eb
  Args:
    type: :Person
    source: Ignacio_Duke_of_Segorbe
  AssignClass (d33a6e2a-edbd-49c8-9887-f7a313ed890d)
 Call ID: d33a6e2a-edbd-49c8-9887-f7a313ed890d
  Args:
    type: :Woman
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (82e53ea0-34b4-495a-8317-f61ef83d605c)
 Call ID: 82e53ea0-34b4-495a-8317-f61ef83d605c
  Args:
    type: :Person
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (3fd361fc-95bb-4845-9a95-d47512ff64c9)
 Call ID: 3fd361fc-95bb-4845-9a95-d47512ff64c9
  Args:
    type: :Woman
    source: Ana_Luna_Medina_y_Orleans_Braganza
  AssignClass (85eb64f3-d7c3-494f-86ad-3fc451c980b0)
 Call ID: 85eb64f3-d7c3-494f-86ad-3fc451c980b0
  Args:
    type: :Person
    source: Ana_Luna_Medina_y_Orleans_Braganza
  AddTriple (c962de07-559c-4122-a9c4-3c63e3078eaf)
 Call ID: c962de07-559c-4122-a9c4-3c63e3078eaf
  Args:
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
    relation: :hasMother
    target: Maria_da_Gloria
  AddTriple (ede4bfdb-1b8f-4cf9-924f-5fcb3f25114b)
 Call ID: ede4bfdb-1b8f-4cf9-924f-5fcb3f25114b
  Args:
    target: Maria_da_Gloria
    relation: :hasMother
    source: Ana_Luna_Medina_y_Orleans_Braganza
  AddTriple (227c627c-671d-4a82-baf9-0431f98a070c)
 Call ID: 227c627c-671d-4a82-baf9-0431f98a070c
  Args:
    source: Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
    relation: :hasFather
    target: Ignacio_Duke_of_Segorbe
  AddTriple (345a77c7-8712-4308-be64-d8f392da497c)
 Call ID: 345a77c7-8712-4308-be64-d8f392da497c
  Args:
    target: Ignacio_Duke_of_Segorbe
    relation: :hasFather
    source: Ana_Luna_Medina_y_Orleans_Braganza
  AssignClass (3a1dcce8-bd3a-42db-ae06-e395b7bf7ef0)
 Call ID: 3a1dcce8-bd3a-42db-ae06-e395b7bf7ef0
  Args:
    type: :Man
    source: King_Peter_II
  AssignClass (9079f4af-66e7-4bd2-9a27-49396628b573)
 Call ID: 9079f4af-66e7-4bd2-9a27-49396628b573
  Args:
    type: :Person
    source: King_Peter_II
  AssignClass (cf0a65e3-7131-4b6d-98ec-b5d1b157babb)
 Call ID: cf0a65e3-7131-4b6d-98ec-b5d1b157babb
  Args:
    type: :Woman
    source: Queen_Alexandra
  AssignClass (86f935db-d7f1-4fb7-801e-0afa4e8ad13d)
 Call ID: 86f935db-d7f1-4fb7-801e-0afa4e8ad13d
  Args:
    type: :Person
    source: Queen_Alexandra
  AssignClass (cffd4c24-1b86-455d-8cc7-97698eeaa244)
 Call ID: cffd4c24-1b86-455d-8cc7-97698eeaa244
  Args:
    type: :Woman
    source: Queen_Maria
  AssignClass (f249bd44-cef6-424d-992c-a234764bd81e)
 Call ID: f249bd44-cef6-424d-992c-a234764bd81e
  Args:
    type: :Person
    source: Queen_Maria
  AssignClass (23456aec-44a4-4e9c-b989-49f58e2e0634)
 Call ID: 23456aec-44a4-4e9c-b989-49f58e2e0634
  Args:
    type: :Man
    source: Prince_Andrew
  AssignClass (4c76c3a6-13e9-4bab-93d9-e87655c86d6e)
 Call ID: 4c76c3a6-13e9-4bab-93d9-e87655c86d6e
  Args:
    type: :Person
    source: Prince_Andrew
  Finish (5444f5b2-cd16-421e-83da-b0affcd77b2e)
 Call ID: 5444f5b2-cd16-421e-83da-b0affcd77b2e
  Args: