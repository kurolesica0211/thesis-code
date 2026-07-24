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
  AssignClass (bd8131c3-54d7-4711-9bba-59bf1169d23f)
 Call ID: bd8131c3-54d7-4711-9bba-59bf1169d23f
  Args:
    type: :Woman
    source: Rosie_Stancer
  AssignClass (82ca4bbe-5edc-4043-ac7f-7b2db0c85cf2)
 Call ID: 82ca4bbe-5edc-4043-ac7f-7b2db0c85cf2
  Args:
    source: Lady_Mary_Cecilia_Leveson-Gower
    type: :Woman
  AssignClass (479c70a8-9817-42c1-8823-bb9ab3ae766f)
 Call ID: 479c70a8-9817-42c1-8823-bb9ab3ae766f
  Args:
    type: :Man
    source: Sir_Samuel_Clayton
  AssignClass (81c93594-e865-495d-a3d8-7e7a8361ff0b)
 Call ID: 81c93594-e865-495d-a3d8-7e7a8361ff0b
  Args:
    source: Rose_Leveson-Gower_Countess_Granville
    type: :Woman
  AssignClass (d776bade-54ff-4173-99c3-ca8dd7567b7b)
 Call ID: d776bade-54ff-4173-99c3-ca8dd7567b7b
  Args:
    source: William_Leveson-Gower_4th_Earl_Granville
    type: :Man
  AssignClass (48421132-91b4-467a-b2c6-7a77350cc178)
 Call ID: 48421132-91b4-467a-b2c6-7a77350cc178
  Args:
    type: :Woman
    source: Queen_Elizabeth_the_Queen_Mother
  AssignClass (c414c086-5bdb-4f54-ae76-9f12a539b3a2)
 Call ID: c414c086-5bdb-4f54-ae76-9f12a539b3a2
  Args:
    type: :Man
    source: Sir_Gilbert_Falkingham_Clayton
  AssignClass (d1163f51-c3b3-415d-be64-01d06c7a6817)
 Call ID: d1163f51-c3b3-415d-be64-01d06c7a6817
  Args:
    type: :Man
    source: William_Wordie_Stancer
  AssignClass (04b20e62-95ec-43d7-a723-7fa4a095d8fd)
 Call ID: 04b20e62-95ec-43d7-a723-7fa4a095d8fd
  Args:
    source: Jock_Stancer
    type: :Man
  AssignClass (36681936-243b-4ccd-97f5-7d5adabeb405)
 Call ID: 36681936-243b-4ccd-97f5-7d5adabeb405
  Args:
    source: James_Wordie
    type: :Man
  AddLiteral (a902d820-9fa8-40f4-8c6a-22644a1289ca)
 Call ID: a902d820-9fa8-40f4-8c6a-22644a1289ca
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Rosie_Stancer
    literal_value: 1960
  AddTriple (3ed3dfa7-04c5-4803-b085-dbd74777dc5f)
 Call ID: 3ed3dfa7-04c5-4803-b085-dbd74777dc5f
  Args:
    target: Lady_Mary_Cecilia_Leveson-Gower
    relation: :hasMother
    source: Rosie_Stancer
  AddTriple (af78a058-c885-4706-89b7-60d355ad30eb)
 Call ID: af78a058-c885-4706-89b7-60d355ad30eb
  Args:
    source: Rosie_Stancer
    relation: :hasFather
    target: Sir_Samuel_Clayton
  AddTriple (395c02cd-e572-479b-ab98-57649f12cf96)
 Call ID: 395c02cd-e572-479b-ab98-57649f12cf96
  Args:
    source: Lady_Mary_Cecilia_Leveson-Gower
    target: Rose_Leveson-Gower_Countess_Granville
    relation: :hasMother
  AddTriple (e9e1cdbf-79df-49ed-88db-a7a690d6fa1f)
 Call ID: e9e1cdbf-79df-49ed-88db-a7a690d6fa1f
  Args:
    source: Lady_Mary_Cecilia_Leveson-Gower
    target: William_Leveson-Gower_4th_Earl_Granville
    relation: :hasFather
  AddTriple (20ef6601-fc91-4431-90dd-d99c63c8c6ab)
 Call ID: 20ef6601-fc91-4431-90dd-d99c63c8c6ab
  Args:
    source: Queen_Elizabeth_the_Queen_Mother
    target: Rose_Leveson-Gower_Countess_Granville
    relation: :hasSister
  AddTriple (dabbff11-5eb8-4810-bb79-074e6f316286)
 Call ID: dabbff11-5eb8-4810-bb79-074e6f316286
  Args:
    source: Sir_Samuel_Clayton
    target: Sir_Gilbert_Falkingham_Clayton
    relation: :hasFather
  AddLiteral (4d8fd038-83e3-4ea9-ba8e-b5b3615712d1)
 Call ID: 4d8fd038-83e3-4ea9-ba8e-b5b3615712d1
  Args:
    source: Rosie_Stancer
    literal_value: 1993
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (177cc3ce-de36-404e-8f84-8f2bd568e5de)
 Call ID: 177cc3ce-de36-404e-8f84-8f2bd568e5de
  Args:
    source: Rosie_Stancer
    relation: :hasSon
    target: Jock_Stancer
  AddTriple (f980dbd1-94c4-4ef7-a572-5b6e589c7914)
 Call ID: f980dbd1-94c4-4ef7-a572-5b6e589c7914
  Args:
    relation: :hasFather
    target: James_Wordie
    source: William_Wordie_Stancer
  Finish (ce5df676-5b62-480b-a1a6-8318fd8a5f47)
 Call ID: ce5df676-5b62-480b-a1a6-8318fd8a5f47
  Args: