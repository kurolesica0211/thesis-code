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
  AssignClass (1d05e95b-5a01-42a8-8f88-3148f067ded1)
 Call ID: 1d05e95b-5a01-42a8-8f88-3148f067ded1
  Args:
    type: :Woman
    source: :Rosie_Stancer
  AssignClass (c0e70be5-01b8-42ca-ba27-92d4540d3d87)
 Call ID: c0e70be5-01b8-42ca-ba27-92d4540d3d87
  Args:
    type: :Person
    source: :Rosie_Stancer
  AddLiteral (ab4ed3d2-8d26-4242-ac1b-bcf9e2987c24)
 Call ID: ab4ed3d2-8d26-4242-ac1b-bcf9e2987c24
  Args:
    relation: :knownAs
    source: :Rosie_Stancer
    literal_value: Rose Cecilia Stancer
    literal_type: xsd:string
  AddLiteral (8825cb65-9a3b-4a68-ab59-0fe5c823bf7f)
 Call ID: 8825cb65-9a3b-4a68-ab59-0fe5c823bf7f
  Args:
    literal_value: Rosie Stancer
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: :Rosie_Stancer
  AddLiteral (063fc12b-7f8a-4908-8234-2216b0606cfa)
 Call ID: 063fc12b-7f8a-4908-8234-2216b0606cfa
  Args:
    relation: :formerlyKnownAs
    source: :Rosie_Stancer
    literal_value: Rose Clayton
    literal_type: xsd:string
  AddLiteral (ef46a21e-4133-43e8-9845-1c8224d83287)
 Call ID: ef46a21e-4133-43e8-9845-1c8224d83287
  Args:
    source: :Rosie_Stancer
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1960
  AssignClass (0eed3b04-6fa2-496f-9dbe-6bfcfea8fc7d)
 Call ID: 0eed3b04-6fa2-496f-9dbe-6bfcfea8fc7d
  Args:
    type: :Woman
    source: :Lady_Mary_Cecilia_Leveson-Gower
  AssignClass (82495e0c-05af-47e1-aff0-c3bf794c9378)
 Call ID: 82495e0c-05af-47e1-aff0-c3bf794c9378
  Args:
    type: :Person
    source: :Lady_Mary_Cecilia_Leveson-Gower
  AddLiteral (e888d5d9-2197-400d-ba02-e8cb86197c69)
 Call ID: e888d5d9-2197-400d-ba02-e8cb86197c69
  Args:
    relation: :hasBirthYear
    source: :Lady_Mary_Cecilia_Leveson-Gower
    literal_value: 1917
    literal_type: xsd:integer
  AddLiteral (aff423f2-5b93-4aae-86e4-91f660f9e77c)
 Call ID: aff423f2-5b93-4aae-86e4-91f660f9e77c
  Args:
    literal_type: xsd:integer
    literal_value: 2014
    source: :Lady_Mary_Cecilia_Leveson-Gower
    relation: :hasDeathYear
  AssignClass (1008310e-f155-4c45-8391-70ea6cb659e3)
 Call ID: 1008310e-f155-4c45-8391-70ea6cb659e3
  Args:
    type: :Man
    source: :Sir_Samuel_Clayton
  AssignClass (6677f6f9-a227-414f-850b-2824580c06a1)
 Call ID: 6677f6f9-a227-414f-850b-2824580c06a1
  Args:
    type: :Person
    source: :Sir_Samuel_Clayton
  AddTriple (40554853-5bd8-4031-ad08-50063451d89a)
 Call ID: 40554853-5bd8-4031-ad08-50063451d89a
  Args:
    target: :Lady_Mary_Cecilia_Leveson-Gower
    relation: :hasMother
    source: :Rosie_Stancer
  AddTriple (f39dc971-4071-46d1-8d3c-78e83af41b02)
 Call ID: f39dc971-4071-46d1-8d3c-78e83af41b02
  Args:
    target: :Sir_Samuel_Clayton
    relation: :hasFather
    source: :Rosie_Stancer
  AssignClass (c992c650-553e-4053-95b8-5e1fade5e51a)
 Call ID: c992c650-553e-4053-95b8-5e1fade5e51a
  Args:
    type: :Woman
    source: :Rose_Leveson-Gower_Countess_Granville
  AssignClass (48acc667-3b3e-461d-9214-68b330378a1a)
 Call ID: 48acc667-3b3e-461d-9214-68b330378a1a
  Args:
    type: :Person
    source: :Rose_Leveson-Gower_Countess_Granville
  AssignClass (f23fb72f-2d33-46e5-9fe4-597033dc8db3)
 Call ID: f23fb72f-2d33-46e5-9fe4-597033dc8db3
  Args:
    type: :Man
    source: :William_Leveson-Gower_4th_Earl_Granville
  AssignClass (e5ac02b8-1859-4242-a5d8-fc0a6b18c73f)
 Call ID: e5ac02b8-1859-4242-a5d8-fc0a6b18c73f
  Args:
    type: :Person
    source: :William_Leveson-Gower_4th_Earl_Granville
  AddTriple (23c33a0b-be9f-43bd-a38b-0682f571acb5)
 Call ID: 23c33a0b-be9f-43bd-a38b-0682f571acb5
  Args:
    source: :Lady_Mary_Cecilia_Leveson-Gower
    relation: :hasMother
    target: :Rose_Leveson-Gower_Countess_Granville
  AddTriple (b8315c44-875b-48b7-9668-72d031dd5c25)
 Call ID: b8315c44-875b-48b7-9668-72d031dd5c25
  Args:
    source: :Lady_Mary_Cecilia_Leveson-Gower
    target: :William_Leveson-Gower_4th_Earl_Granville
    relation: :hasFather
  AssignClass (8a9849a1-7ab9-4069-83e4-3f34a0dd8d78)
 Call ID: 8a9849a1-7ab9-4069-83e4-3f34a0dd8d78
  Args:
    type: :Man
    source: :Sir_Gilbert_Falkingham_Clayton
  AssignClass (33fd7e7b-7ea3-467b-8fc5-a4485de9ea6f)
 Call ID: 33fd7e7b-7ea3-467b-8fc5-a4485de9ea6f
  Args:
    type: :Person
    source: :Sir_Gilbert_Falkingham_Clayton
  AddTriple (dbc31ef0-46c4-4b04-ba89-a255733cb76f)
 Call ID: dbc31ef0-46c4-4b04-ba89-a255733cb76f
  Args:
    source: :Sir_Samuel_Clayton
    target: :Sir_Gilbert_Falkingham_Clayton
    relation: :hasFather
  AssignClass (e54f3781-2ec2-488b-ae43-fbdc1dc8625b)
 Call ID: e54f3781-2ec2-488b-ae43-fbdc1dc8625b
  Args:
    type: :Man
    source: :William_Wordie_Stancer
  AssignClass (6b661f29-822f-43a9-a3b4-bf3831e849cd)
 Call ID: 6b661f29-822f-43a9-a3b4-bf3831e849cd
  Args:
    type: :Person
    source: :William_Wordie_Stancer
  AddLiteral (126e4dc0-7a7f-4d88-ba2a-b13b35858981)
 Call ID: 126e4dc0-7a7f-4d88-ba2a-b13b35858981
  Args:
    relation: :hasMarriageYear
    source: :Rosie_Stancer
    literal_value: 1993
    literal_type: xsd:integer
  AssignClass (fa73f003-0eb6-4340-ad9f-29f96f1ae5b2)
 Call ID: fa73f003-0eb6-4340-ad9f-29f96f1ae5b2
  Args:
    type: :Man
    source: :Jock_Stancer
  AssignClass (3a24dc3c-c606-4531-9552-abd128b70eb6)
 Call ID: 3a24dc3c-c606-4531-9552-abd128b70eb6
  Args:
    type: :Person
    source: :Jock_Stancer
  AddTriple (4c96c361-6a69-49bb-8bd3-734abe279007)
 Call ID: 4c96c361-6a69-49bb-8bd3-734abe279007
  Args:
    target: :Rosie_Stancer
    relation: :hasMother
    source: :Jock_Stancer
  AddTriple (dab3630a-4ce3-4c30-bd3b-145ccdd7404e)
 Call ID: dab3630a-4ce3-4c30-bd3b-145ccdd7404e
  Args:
    source: :Jock_Stancer
    relation: :hasFather
    target: :William_Wordie_Stancer
  AssignClass (400816c0-5bd5-4d85-bf78-bb1a89942157)
 Call ID: 400816c0-5bd5-4d85-bf78-bb1a89942157
  Args:
    type: :Man
    source: :James_Wordie
  AssignClass (247cc9ec-101f-4a22-a8c6-25a328a7b407)
 Call ID: 247cc9ec-101f-4a22-a8c6-25a328a7b407
  Args:
    type: :Person
    source: :James_Wordie
  Finish (f38b4ba2-ca25-4fa2-a57d-06c6425b2137)
 Call ID: f38b4ba2-ca25-4fa2-a57d-06c6425b2137
  Args: