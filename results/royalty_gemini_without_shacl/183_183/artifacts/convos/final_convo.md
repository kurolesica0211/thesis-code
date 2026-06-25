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


Peter Karageorgevitch (Serbian Cyrillic: Петар Карађорђевић, romanized: Petar Karađorđević; born 5 February 1980), also known as Prince Peter of Serbia and Yugoslavia, is an American born Spanish-Serbian graphic designer and a member of the House of Karađorđević.
He is the oldest grandchild and the first grandson of the last Yugoslav king, Peter II.
Between his birth and his renunciation in 2022, he was known as the Hereditary Prince.
Early life and education

Peter is the first son and the oldest child of the last Crown Prince of the former Kingdom of Yugoslavia, Alexander, and Princess Maria da Gloria of Orléans-Braganza.
His godfather was Prince Alexander of Yugoslavia, a son of Prince Paul of Yugoslavia.
His godmother is Anne, Princess Royal.
Peter has two younger brothers, twins Philip and Alexander (born 1982).
Peter's parents divorced in 1985.
After the divorce, his father married Katherine Clairy Batis later that year, while his mother married Ignacio, Duke of Segorbe later that year also.
Through his mother, Peter has two younger half-sisters, Sol María de la Blanca Medina y Orléans-Braganza, Countess of Ampurias (b. 1986) and Ana Luna Medina y Orléans-Braganza, Countess of Ricla (b. 1988).
In 1991, Peter with his father and brothers briefly visited Belgrade, Yugoslavia.
In February 2001, the Parliament of FR Yugoslavia passed legislation conferring citizenship on members of the Karađorđević family, making Peter eligible for a Yugoslav citizenship.
In July 2001, his father and step-mother moved to Belgrade, Serbia, FR Yugoslavia.
In June 1998, Peter graduated from The King's School, Canterbury, in England, having obtained three A-levels in Art, Spanish, and French, and ten GCSEs.
Public life

Prince Peter attended the reburial of his grandparents King Peter II and Queen Alexandra, great-grandmother Queen Maria, and great-uncle Prince Andrew in the Royal Family Mausoleum at Oplenac on 26 May 2013.
The Serbian Royal Regalia were placed over King Peter's coffin, having Peter placing the Karađorđević Crown.
On 17 July 2015, Prince Peter and his brothers were present at their father's 70th birthday celebration in Belgrade.
On 27 April 2022, Prince Peter renounced his title of Hereditary Prince – for himself and his descendants – in favor of his younger brother Philip.
The ceremony took place in Seville at Casa de Pilatos in the presence of his mother Princess Maria da Gloria, his stepfather the 19th Duke of Segorbe, his brother Philip, his sister-in-law Princess Danica, his half sister the 54th Countess of Ampurias, Ljubodrag Grujić, member of the Crown Council, Chancellor of the Orders and the Herald of the House of Karađorđević, and Nikola Stanković, Chief of Staff of the Crown Prince.
His father, Crown Prince Alexander, did not attend the event, and was dissatisfied with Peter's renunciation.
Personal life

Prince Peter used to work in a field of graphic design and art direction in London and New York City.
Peter has a daughter named Dolores Luna Noor born in 2017 by Lauren Estelle Jones (b. 1984).
Honours

Ancestors

Peter is a member of the House of Karađorđević.
Through his father, Peter descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, Christian IX of Denmark and Alexander of Greece, and furthermore from emperors Nicholas I of Russia and Frederick III of the Germans and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through his mother, Peter descends from the Emperor Pedro II of Brazil, and kings Louis Philippe I of France and Francis I of the Two Sicilies, and furthermore from Francis I, Holy Roman Emperor and king Charles III of Spain.



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
  AssignClass (14cd9c1c-fa91-4a69-9fe6-8fa55d17614e)
 Call ID: 14cd9c1c-fa91-4a69-9fe6-8fa55d17614e
  Args:
    type: :Man
    source: :Peter_Karageorgevitch
  AssignClass (29e245c0-f862-4d36-8479-cb5bf340739b)
 Call ID: 29e245c0-f862-4d36-8479-cb5bf340739b
  Args:
    source: :Peter_Karageorgevitch
    type: :Person
  AddLiteral (b86d5555-08e6-4207-8e0b-a8e0cfaf8a21)
 Call ID: b86d5555-08e6-4207-8e0b-a8e0cfaf8a21
  Args:
    relation: :hasBirthYear
    source: :Peter_Karageorgevitch
    literal_type: xsd:integer
    literal_value: 1980
  AddLiteral (87b6dba7-39bc-4d09-9845-bf6672294bfb)
 Call ID: 87b6dba7-39bc-4d09-9845-bf6672294bfb
  Args:
    literal_value: Prince Peter of Serbia and Yugoslavia
    literal_type: xsd:string
    source: :Peter_Karageorgevitch
    relation: :alsoKnownAs
  AssignClass (c64c076a-5a8f-4a93-878b-02895c4bd9d6)
 Call ID: c64c076a-5a8f-4a93-878b-02895c4bd9d6
  Args:
    type: :Man
    source: :Alexander_of_Yugoslavia
  AssignClass (d3210f4e-afde-4413-880b-0eca57e4d2bc)
 Call ID: d3210f4e-afde-4413-880b-0eca57e4d2bc
  Args:
    type: :Person
    source: :Alexander_of_Yugoslavia
  AssignClass (58e90b57-10a7-4217-8df4-327c0de32c3f)
 Call ID: 58e90b57-10a7-4217-8df4-327c0de32c3f
  Args:
    source: :Maria_da_Gloria
    type: :Woman
  AssignClass (a6259c45-4778-4059-80b1-e6ad6d312011)
 Call ID: a6259c45-4778-4059-80b1-e6ad6d312011
  Args:
    type: :Person
    source: :Maria_da_Gloria
  AddTriple (642509de-bb90-405f-b871-17e03c37b205)
 Call ID: 642509de-bb90-405f-b871-17e03c37b205
  Args:
    source: :Peter_Karageorgevitch
    relation: :hasFather
    target: :Alexander_of_Yugoslavia
  AddTriple (b620a605-835e-44fc-b47c-18a5e95550e2)
 Call ID: b620a605-835e-44fc-b47c-18a5e95550e2
  Args:
    source: :Peter_Karageorgevitch
    relation: :hasMother
    target: :Maria_da_Gloria
  AssignClass (c6b6392d-c246-46ed-b281-a0c0b411630f)
 Call ID: c6b6392d-c246-46ed-b281-a0c0b411630f
  Args:
    type: :Man
    source: :Philip_Karageorgevitch
  AssignClass (c60d8c1d-2fcc-4898-86a5-5dfcc2ea7802)
 Call ID: c60d8c1d-2fcc-4898-86a5-5dfcc2ea7802
  Args:
    source: :Philip_Karageorgevitch
    type: :Person
  AssignClass (ca693a28-2621-433e-b678-60451f40bff7)
 Call ID: ca693a28-2621-433e-b678-60451f40bff7
  Args:
    source: :Alexander_Karageorgevitch_Jr
    type: :Man
  AssignClass (e178620e-cd17-4a20-86c1-6c828d060255)
 Call ID: e178620e-cd17-4a20-86c1-6c828d060255
  Args:
    source: :Alexander_Karageorgevitch_Jr
    type: :Person
  AddTriple (e66dd372-b5ad-4e5e-856d-7cb4ef1686b4)
 Call ID: e66dd372-b5ad-4e5e-856d-7cb4ef1686b4
  Args:
    target: :Philip_Karageorgevitch
    relation: :hasBrother
    source: :Peter_Karageorgevitch
  AddTriple (43729753-05e7-470f-8362-fc1af6f88b77)
 Call ID: 43729753-05e7-470f-8362-fc1af6f88b77
  Args:
    source: :Peter_Karageorgevitch
    relation: :hasBrother
    target: :Alexander_Karageorgevitch_Jr
  AssignClass (e281a707-2fe9-449e-b0fd-a2a4dd456d44)
 Call ID: e281a707-2fe9-449e-b0fd-a2a4dd456d44
  Args:
    type: :Woman
    source: :Dolores_Luna_Noor
  AssignClass (3dc67624-315a-4a40-9893-0b9a6464dc47)
 Call ID: 3dc67624-315a-4a40-9893-0b9a6464dc47
  Args:
    type: :Person
    source: :Dolores_Luna_Noor
  AddTriple (cd4b6cb6-1164-40c6-aa61-27a6390c24e2)
 Call ID: cd4b6cb6-1164-40c6-aa61-27a6390c24e2
  Args:
    source: :Peter_Karageorgevitch
    target: :Dolores_Luna_Noor
    relation: :hasDaughter
  AddLiteral (d1ab6826-244e-4100-9685-b46b9aefbcdb)
 Call ID: d1ab6826-244e-4100-9685-b46b9aefbcdb
  Args:
    literal_value: 2017
    literal_type: xsd:integer
    source: :Dolores_Luna_Noor
    relation: :hasBirthYear
  AssignClass (d65dbfae-c9d3-417f-a744-4249b56b7880)
 Call ID: d65dbfae-c9d3-417f-a744-4249b56b7880
  Args:
    source: :Lauren_Estelle_Jones
    type: :Woman
  AssignClass (b2329703-f78e-4431-ad17-920a21fe370b)
 Call ID: b2329703-f78e-4431-ad17-920a21fe370b
  Args:
    type: :Person
    source: :Lauren_Estelle_Jones
  AddTriple (ba9f3a47-c334-4ee3-9118-376a097ab534)
 Call ID: ba9f3a47-c334-4ee3-9118-376a097ab534
  Args:
    source: :Dolores_Luna_Noor
    target: :Lauren_Estelle_Jones
    relation: :hasMother
  AssignClass (b4c9e4c6-bba2-48dc-a7ee-caa9d8f9606c)
 Call ID: b4c9e4c6-bba2-48dc-a7ee-caa9d8f9606c
  Args:
    type: :Man
    source: :Peter_II_of_Yugoslavia
  AssignClass (73627524-ebaa-41ed-adc7-3c1125c3f1b3)
 Call ID: 73627524-ebaa-41ed-adc7-3c1125c3f1b3
  Args:
    type: :Person
    source: :Peter_II_of_Yugoslavia
  AddTriple (7ed8342b-e99c-4925-9e16-7fd2cd88f4b5)
 Call ID: 7ed8342b-e99c-4925-9e16-7fd2cd88f4b5
  Args:
    source: :Peter_II_of_Yugoslavia
    relation: :isAncestorOf
    target: :Peter_Karageorgevitch
  AssignClass (e07cf7d3-73e9-4b9c-889b-286c82487b04)
 Call ID: e07cf7d3-73e9-4b9c-889b-286c82487b04
  Args:
    type: :Woman
    source: :Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (8127d41c-d570-4808-9280-fa828fcb48e8)
 Call ID: 8127d41c-d570-4808-9280-fa828fcb48e8
  Args:
    type: :Person
    source: :Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
  AssignClass (1c1905bd-b665-475b-9ac1-5dd77f14e56a)
 Call ID: 1c1905bd-b665-475b-9ac1-5dd77f14e56a
  Args:
    type: :Woman
    source: :Ana_Luna_Medina_y_Orleans_Braganza
  AssignClass (e1f2c3cb-0278-4095-9400-1c6cbef52d43)
 Call ID: e1f2c3cb-0278-4095-9400-1c6cbef52d43
  Args:
    type: :Person
    source: :Ana_Luna_Medina_y_Orleans_Braganza
  AddTriple (c443cc32-5fd2-4d7d-a72e-e090e4a740e5)
 Call ID: c443cc32-5fd2-4d7d-a72e-e090e4a740e5
  Args:
    source: :Sol_Maria_de_la_Blanca_Medina_y_Orleans_Braganza
    relation: :hasMother
    target: :Maria_da_Gloria
  AddTriple (a3f7676e-4f6c-4df3-9245-5968896606e6)
 Call ID: a3f7676e-4f6c-4df3-9245-5968896606e6
  Args:
    source: :Ana_Luna_Medina_y_Orleans_Braganza
    relation: :hasMother
    target: :Maria_da_Gloria
  Finish (173e1501-b4ff-408e-8c03-ed87f3cb6b8a)
 Call ID: 173e1501-b4ff-408e-8c03-ed87f3cb6b8a
  Args: