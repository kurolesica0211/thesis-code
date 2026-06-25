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
  AssignClass (52f89365-ef70-492f-b5a2-7f760a92aeba)
 Call ID: 52f89365-ef70-492f-b5a2-7f760a92aeba
  Args:
    source: Rosie_Stancer
    type: :Woman
  AssignClass (20baf3b4-2c7a-4828-b93f-470e24c63668)
 Call ID: 20baf3b4-2c7a-4828-b93f-470e24c63668
  Args:
    source: Rosie_Stancer
    type: :Person
  AddLiteral (bdadb170-568d-430a-83a7-4ef702219e84)
 Call ID: bdadb170-568d-430a-83a7-4ef702219e84
  Args:
    literal_type: xsd:date
    source: Rosie_Stancer
    relation: :hasBirthYear
    literal_value: 1960-01-25
  AssignClass (0344777a-756d-4086-87e3-4f8443b2c0b1)
 Call ID: 0344777a-756d-4086-87e3-4f8443b2c0b1
  Args:
    source: Lady_Mary_Cecilia_Leveson-Gower
    type: :Woman
  AssignClass (e35df284-39ca-47e5-b770-386a9ca0d7bf)
 Call ID: e35df284-39ca-47e5-b770-386a9ca0d7bf
  Args:
    source: Lady_Mary_Cecilia_Leveson-Gower
    type: :Person
  AssignClass (bb1eb19f-07ab-4399-a348-2a1317e01732)
 Call ID: bb1eb19f-07ab-4399-a348-2a1317e01732
  Args:
    source: Sir_Samuel_Clayton
    type: :Man
  AssignClass (6c3690f7-c6b4-40cb-9a24-a3ac127c0240)
 Call ID: 6c3690f7-c6b4-40cb-9a24-a3ac127c0240
  Args:
    source: Sir_Samuel_Clayton
    type: :Person
  AddTriple (4052b178-b0fd-4024-8f54-0fb693e1252d)
 Call ID: 4052b178-b0fd-4024-8f54-0fb693e1252d
  Args:
    target: Lady_Mary_Cecilia_Leveson-Gower
    source: Rosie_Stancer
    relation: :hasMother
  AddTriple (a8d0a531-c4a0-4b23-90e1-9f04f20d2759)
 Call ID: a8d0a531-c4a0-4b23-90e1-9f04f20d2759
  Args:
    source: Rosie_Stancer
    target: Sir_Samuel_Clayton
    relation: :hasFather
  AssignClass (1802ce16-30d6-4763-9291-522eb23c2c93)
 Call ID: 1802ce16-30d6-4763-9291-522eb23c2c93
  Args:
    source: Rose_Leveson-Gower_Countess_Granville
    type: :Woman
  AssignClass (9d4b2694-1bdb-42d3-91fd-1b9f782920c3)
 Call ID: 9d4b2694-1bdb-42d3-91fd-1b9f782920c3
  Args:
    source: Rose_Leveson-Gower_Countess_Granville
    type: :Person
  AssignClass (1f5f1359-971e-4b72-83b0-cc9ed0d4d2ae)
 Call ID: 1f5f1359-971e-4b72-83b0-cc9ed0d4d2ae
  Args:
    source: William_Leveson-Gower_4th_Earl_Granville
    type: :Man
  AssignClass (e73aa692-f3ac-4bd3-97de-17ed3d2c5041)
 Call ID: e73aa692-f3ac-4bd3-97de-17ed3d2c5041
  Args:
    source: William_Leveson-Gower_4th_Earl_Granville
    type: :Person
  AddTriple (00f435e6-3c75-4ce3-a70d-00066b18d0e2)
 Call ID: 00f435e6-3c75-4ce3-a70d-00066b18d0e2
  Args:
    relation: :hasMother
    source: Lady_Mary_Cecilia_Leveson-Gower
    target: Rose_Leveson-Gower_Countess_Granville
  AddTriple (b25baa83-97f6-4c54-b7da-45c11c1cc42f)
 Call ID: b25baa83-97f6-4c54-b7da-45c11c1cc42f
  Args:
    relation: :hasFather
    source: Lady_Mary_Cecilia_Leveson-Gower
    target: William_Leveson-Gower_4th_Earl_Granville
  AssignClass (35b716ce-616d-4246-ae13-786f74ffbd62)
 Call ID: 35b716ce-616d-4246-ae13-786f74ffbd62
  Args:
    source: Sir_Gilbert_Falkingham_Clayton
    type: :Man
  AssignClass (dc777dff-218f-4709-a509-4fd5af7bc2e2)
 Call ID: dc777dff-218f-4709-a509-4fd5af7bc2e2
  Args:
    source: Sir_Gilbert_Falkingham_Clayton
    type: :Person
  AddTriple (61a05315-7d14-4861-9cc8-738dfe97143e)
 Call ID: 61a05315-7d14-4861-9cc8-738dfe97143e
  Args:
    target: Sir_Gilbert_Falkingham_Clayton
    source: Sir_Samuel_Clayton
    relation: :hasFather
  AssignClass (0d2225fa-4b2f-4faa-bd48-92a689e9bce8)
 Call ID: 0d2225fa-4b2f-4faa-bd48-92a689e9bce8
  Args:
    source: William_Wordie_Stancer
    type: :Man
  AssignClass (7f6cdea3-7bfb-49f2-9593-6929a3d5c505)
 Call ID: 7f6cdea3-7bfb-49f2-9593-6929a3d5c505
  Args:
    source: William_Wordie_Stancer
    type: :Person
  AddLiteral (514cb5a2-c97b-431f-b67b-2265d4a5841a)
 Call ID: 514cb5a2-c97b-431f-b67b-2265d4a5841a
  Args:
    literal_type: xsd:integer
    source: Rosie_Stancer
    literal_value: 1993
    relation: :hasMarriageYear
  AddTriple (bf8fee8b-1d99-4870-8131-560dfe00ed36)
 Call ID: bf8fee8b-1d99-4870-8131-560dfe00ed36
  Args:
    target: William_Wordie_Stancer
    source: Rosie_Stancer
    relation: :hasRelation
  AssignClass (0d9d7d5c-d80f-47d6-898b-b04e82782d28)
 Call ID: 0d9d7d5c-d80f-47d6-898b-b04e82782d28
  Args:
    source: Jock_Stancer
    type: :Man
  AssignClass (350e860a-4bc1-4209-a451-a48e1813cb7a)
 Call ID: 350e860a-4bc1-4209-a451-a48e1813cb7a
  Args:
    source: Jock_Stancer
    type: :Person
  AddTriple (42dbad68-9945-4f36-a13b-a3e12729c7fb)
 Call ID: 42dbad68-9945-4f36-a13b-a3e12729c7fb
  Args:
    relation: :hasMother
    source: Jock_Stancer
    target: Rosie_Stancer
  AddTriple (af3c1a86-fd44-4e39-ab88-403e9d7c8491)
 Call ID: af3c1a86-fd44-4e39-ab88-403e9d7c8491
  Args:
    relation: :hasFather
    source: Jock_Stancer
    target: William_Wordie_Stancer
  AssignClass (8448d8d1-b2d7-4143-b678-2cb90d751d43)
 Call ID: 8448d8d1-b2d7-4143-b678-2cb90d751d43
  Args:
    source: James_Wordie
    type: :Man
  AssignClass (62eed5da-7de3-4b58-b807-5afcd1ffa845)
 Call ID: 62eed5da-7de3-4b58-b807-5afcd1ffa845
  Args:
    source: James_Wordie
    type: :Person
  AddTriple (7fc8ba73-e6c3-4b44-98c5-dd118b9c99d9)
 Call ID: 7fc8ba73-e6c3-4b44-98c5-dd118b9c99d9
  Args:
    source: William_Wordie_Stancer
    target: James_Wordie
    relation: :hasFather
  Finish (e00f9314-ecd3-4887-a5cf-b295b83d7558)
 Call ID: e00f9314-ecd3-4887-a5cf-b295b83d7558
  Args: