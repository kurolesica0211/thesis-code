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
Rose Cecilia "Rosie" Stancer (née Clayton; born 25 January 1960) is a British explorer and polar adventurer, and a female-line second cousin of King Charles III of the UK.
Youth, education, family

Rosie Stancer attended Butterstone House School in Scotland and then Heathfield School, Ascot.
Stancer is the daughter of Lady Mary Cecilia Leveson-Gower (1917–2014) and Sir Samuel Clayton.
Her maternal grandparents were Rose Leveson-Gower, Countess Granville (an elder sister of Queen Elizabeth the Queen Mother), and William Leveson-Gower, 4th Earl Granville, naval commander, making her a second cousin of King Charles III.
Her paternal grandfather was Brigadier-General Sir Gilbert Falkingham Clayton, British Army intelligence officer and colonial administrator.
On 9 July 1993, she married William Wordie Stancer, with whom she has one son Jock Stancer.
Her husband’s grandfather was, like Stancer herself, a polar explorer James Wordie.
In 1997, Stancer was one of 20 amateur women selected for a place on the first all women's expedition to the North Pole, The 'McVities Penguin Polar Relay'.
M&G ISA South Pole Expedition 1999

In 1999, Stancer and four others from the first expedition organised and managed their own expedition to the South Pole, The 'M&G ISA Challenge'.
Snickers South Pole Solo 2004

In the Austral summer of 2003–4, Stancer skied solo and without re-supply to the South Pole on the 'Snickers South Pole Solo 2004' expedition.
Hauling a sledge more than twice her body weight for over 700 miles (1,100 km), Stancer reached the Pole in 43 days 23 hours, a day longer than Fiona Thornewill who reached the South Pole a few days before Stancer.
During the expedition Stancer gathered both meteorological and physiological data.
Mars North Pole Solo 2007

In 2007, Stancer attempted to become the first woman to trek solo to the Geographic North Pole.
Having traveled 426 nautical miles in 84 days, Stancer was still able to set the world record for furthest solo female expedition to the north.
The Long Haul Expedition 2019

In 2019, Stancer joined Mike Laird on concurrent solo expeditions across Siberia’s Lake Baikal, the world’s largest, deepest, oldest freshwater lake.
They traveled in opposite directions, with Stancer starting from the south and Laird from the north.
Completing over 700 km in 21 days, Stancer set the record.
Monarch's Way (2020)

Stancer walked the Monarch's Way in England in 2020.
In 2021 Stancer began a 'desert trilogy', travelling across the Aralkum in 2021 and the Sinai Peninsula in 2023; she travelled with Pom Oliver, Arabella Dorman and Lee Watts.
Charities

Stancer is an honorary board member for the charity Special Olympics GB, which seeks to provide sports training and competition in a variety of Olympic-style events for people with learning disabilities.
Awards

Stancer was awarded an honorary fellowship from the Polar exploration society.



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
  AssignClass (292a8611-5763-4323-9314-226ea194d67f)
 Call ID: 292a8611-5763-4323-9314-226ea194d67f
  Args:
    type: :Woman
    source: RosieStancer
  AssignClass (8728adac-d791-4db8-825a-6fdfc879aa31)
 Call ID: 8728adac-d791-4db8-825a-6fdfc879aa31
  Args:
    type: :Person
    source: RosieStancer
  AddLiteral (9087d76d-6a98-4717-a6da-a015e75a42c6)
 Call ID: 9087d76d-6a98-4717-a6da-a015e75a42c6
  Args:
    literal_value: 1960
    source: RosieStancer
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (7ba0a3ba-974b-450e-8184-c61daada6331)
 Call ID: 7ba0a3ba-974b-450e-8184-c61daada6331
  Args:
    type: :Woman
    source: LadyMaryCeciliaLevesonGower
  AssignClass (2f0b1190-01c8-4395-bd3f-a7c2b106a1b5)
 Call ID: 2f0b1190-01c8-4395-bd3f-a7c2b106a1b5
  Args:
    type: :Ancestor
    source: LadyMaryCeciliaLevesonGower
  AssignClass (209fd222-1430-47ef-b3bf-5369dc3f858a)
 Call ID: 209fd222-1430-47ef-b3bf-5369dc3f858a
  Args:
    type: :Man
    source: SirSamuelClayton
  AssignClass (a27d7da7-7cd3-4f31-9a44-d4c6e728c92c)
 Call ID: a27d7da7-7cd3-4f31-9a44-d4c6e728c92c
  Args:
    type: :Ancestor
    source: SirSamuelClayton
  AddLiteral (4f791f09-b592-480d-b841-a72ae88b455e)
 Call ID: 4f791f09-b592-480d-b841-a72ae88b455e
  Args:
    literal_value: 1917
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: LadyMaryCeciliaLevesonGower
  AddLiteral (2c6750b8-a6f3-4624-9c88-ea74e0c1be2c)
 Call ID: 2c6750b8-a6f3-4624-9c88-ea74e0c1be2c
  Args:
    source: LadyMaryCeciliaLevesonGower
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2014
  AddTriple (8a662b96-be2a-4701-8e6e-0e9d5fc7affe)
 Call ID: 8a662b96-be2a-4701-8e6e-0e9d5fc7affe
  Args:
    source: RosieStancer
    relation: :hasMother
    target: LadyMaryCeciliaLevesonGower
  AddTriple (0f478548-f8ee-4abe-9f68-c93fe9ab64cb)
 Call ID: 0f478548-f8ee-4abe-9f68-c93fe9ab64cb
  Args:
    relation: :hasFather
    target: SirSamuelClayton
    source: RosieStancer
  AssignClass (c171681f-ed70-411f-b296-15ff4d5062fd)
 Call ID: c171681f-ed70-411f-b296-15ff4d5062fd
  Args:
    type: :Woman
    source: RoseLevesonGowerCountessGranville
  AssignClass (c7f8e1c7-4e50-436e-b139-43f0cd4b7697)
 Call ID: c7f8e1c7-4e50-436e-b139-43f0cd4b7697
  Args:
    type: :Ancestor
    source: RoseLevesonGowerCountessGranville
  AssignClass (4bc316e9-158a-4eb2-aaa8-02ce4ff6409e)
 Call ID: 4bc316e9-158a-4eb2-aaa8-02ce4ff6409e
  Args:
    type: :Man
    source: WilliamLevesonGower4thEarlGranville
  AssignClass (465091bf-b5ea-4951-bd13-15ca37052144)
 Call ID: 465091bf-b5ea-4951-bd13-15ca37052144
  Args:
    type: :Ancestor
    source: WilliamLevesonGower4thEarlGranville
  AddTriple (3aa6d6c0-0c83-46e2-882f-6c9da715df39)
 Call ID: 3aa6d6c0-0c83-46e2-882f-6c9da715df39
  Args:
    relation: :hasMother
    target: RoseLevesonGowerCountessGranville
    source: LadyMaryCeciliaLevesonGower
  AddTriple (af899912-0ec2-4bb5-88d2-a382941f1315)
 Call ID: af899912-0ec2-4bb5-88d2-a382941f1315
  Args:
    relation: :hasFather
    target: WilliamLevesonGower4thEarlGranville
    source: LadyMaryCeciliaLevesonGower
  AssignClass (aa2a7515-4529-47ff-9c69-571c4b15b129)
 Call ID: aa2a7515-4529-47ff-9c69-571c4b15b129
  Args:
    type: :Man
    source: SirGilbertFalkinghamClayton
  AssignClass (5b6355bc-7482-4855-9ae7-fe1bab064e65)
 Call ID: 5b6355bc-7482-4855-9ae7-fe1bab064e65
  Args:
    type: :Ancestor
    source: SirGilbertFalkinghamClayton
  AddTriple (d924ff22-2d05-49f8-83fd-b4d01ebb0664)
 Call ID: d924ff22-2d05-49f8-83fd-b4d01ebb0664
  Args:
    relation: :hasFather
    target: SirGilbertFalkinghamClayton
    source: SirSamuelClayton
  AssignClass (dd6173eb-3762-4d57-94f4-4816ff6a3d99)
 Call ID: dd6173eb-3762-4d57-94f4-4816ff6a3d99
  Args:
    type: :Man
    source: WilliamWordieStancer
  AssignClass (dead2209-3e09-4981-a044-4ee72fea5d3d)
 Call ID: dead2209-3e09-4981-a044-4ee72fea5d3d
  Args:
    type: :Person
    source: WilliamWordieStancer
  AddTriple (4b308a28-c817-4e7d-a906-47497b426e56)
 Call ID: 4b308a28-c817-4e7d-a906-47497b426e56
  Args:
    relation: :hasRelation
    target: WilliamWordieStancer
    source: RosieStancer
  AddLiteral (66cd042e-d6d7-49fb-802d-625a7455a897)
 Call ID: 66cd042e-d6d7-49fb-802d-625a7455a897
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: RosieStancer
    literal_value: 1993
  AssignClass (e39403de-45e3-4d87-b29c-3264bbdc2b06)
 Call ID: e39403de-45e3-4d87-b29c-3264bbdc2b06
  Args:
    type: :Man
    source: JockStancer
  AssignClass (059f5414-d739-423c-bf5a-eaf5c0b14f53)
 Call ID: 059f5414-d739-423c-bf5a-eaf5c0b14f53
  Args:
    type: :Person
    source: JockStancer
  AddTriple (710f4cae-eac1-4a75-8748-061f104f2c75)
 Call ID: 710f4cae-eac1-4a75-8748-061f104f2c75
  Args:
    relation: :hasMother
    target: RosieStancer
    source: JockStancer
  AddTriple (4ee44a99-4c9d-4110-aef2-6e7f4e1787e9)
 Call ID: 4ee44a99-4c9d-4110-aef2-6e7f4e1787e9
  Args:
    relation: :hasFather
    target: WilliamWordieStancer
    source: JockStancer
  AssignClass (7b2af23a-3f20-47d4-a3b3-365099b81b42)
 Call ID: 7b2af23a-3f20-47d4-a3b3-365099b81b42
  Args:
    type: :Man
    source: JamesWordie
  AssignClass (bf201ddc-2078-4498-b3fa-c8fc3e3cc14c)
 Call ID: bf201ddc-2078-4498-b3fa-c8fc3e3cc14c
  Args:
    type: :Ancestor
    source: JamesWordie
  AddTriple (008ecfd0-1a26-487b-8a6c-04de42314148)
 Call ID: 008ecfd0-1a26-487b-8a6c-04de42314148
  Args:
    relation: :hasFather
    target: JamesWordie
    source: WilliamWordieStancer
  Finish (2382dcdb-4c42-4375-866b-f98de549114a)
 Call ID: 2382dcdb-4c42-4375-866b-f98de549114a
  Args: