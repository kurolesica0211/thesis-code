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
Franz Wilhelm Victor Christoph Stephan Prinz von Preussen (born 3 September 1943) is a German businessman and member of the House of Hohenzollern, the former ruling German imperial house and royal house of Prussia.
He is also the great-grandson of German Emperor Wilhelm II.
Biography

Franz Wilhelm Prince of Prussia was born in Grünberg, Silesia, as the son of Prince Karl Franz of Prussia and his first wife Princess Henriette von Schönaich-Carolath.
He had a twin brother, Prince Friedrich Christian, who died three weeks after his birth.
Prince Franz Wilhelm is a grandson of Prince Joachim of Prussia, the youngest son of Emperor Wilhelm II.
In 2002 Franz Wilhelm with Theodor Tantzen founded the Prinz von Preußen Grundbesitz AG, a project development and project management company which restores old buildings in Germany.
Personal life

Franz Wilhelm married his third cousin once removed, Grand Duchess Maria Vladimirovna of Russia, great-great-granddaughter of Queen Victoria, civilly on 4 September 1976 at Dinard and religiously on 22 September at the Russian Orthodox Chapel in Madrid.
Before his marriage, he converted to the Russian Orthodox faith and was created a Grand Duke of Russia with the name Mikhail Pavlovich by his father-in-law Grand Duke Vladimir of Russia.
Franz Wilhelm and Grand Duchess Maria had one son before divorcing on 19 June 1985 (they separated in 1982), at which point he reverted to his previous title.
He married Nadia Nour El Etreby (born 2 August 1949) on 14 March 2019, to whom was bestowed upon marriage the courtesy style and title of Her Royal Highness Princess Franz Wilhelm of Prussia.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (4eb2997d-f025-4e82-94d2-8db176a8883c)
 Call ID: 4eb2997d-f025-4e82-94d2-8db176a8883c
  Args:
    source: Franz_Wilhelm_Prince_of_Prussia
    type: :Man
  AssignClass (a2aa3884-f21a-4604-8cc5-3e8814bf5777)
 Call ID: a2aa3884-f21a-4604-8cc5-3e8814bf5777
  Args:
    source: Franz_Wilhelm_Prince_of_Prussia
    type: :Person
  AddLiteral (06585ab9-4770-48e3-8a3a-b5317c125c9a)
 Call ID: 06585ab9-4770-48e3-8a3a-b5317c125c9a
  Args:
    literal_type: xsd:integer
    literal_value: 1943
    relation: :hasBirthYear
    source: Franz_Wilhelm_Prince_of_Prussia
  AssignClass (44ea4c94-1a39-43cf-b25e-4be09be657ba)
 Call ID: 44ea4c94-1a39-43cf-b25e-4be09be657ba
  Args:
    source: Karl_Franz_of_Prussia
    type: :Man
  AssignClass (971e96ff-8fee-4449-a2b6-d8fa8d7bc483)
 Call ID: 971e96ff-8fee-4449-a2b6-d8fa8d7bc483
  Args:
    source: Karl_Franz_of_Prussia
    type: :Person
  AssignClass (3069f589-f6a6-4f01-8de4-41c5ae00ee21)
 Call ID: 3069f589-f6a6-4f01-8de4-41c5ae00ee21
  Args:
    source: Henriette_von_Schönaich-Carolath
    type: :Woman
  AssignClass (cef44ab5-928a-42ef-a545-45e3038db83d)
 Call ID: cef44ab5-928a-42ef-a545-45e3038db83d
  Args:
    source: Henriette_von_Schönaich-Carolath
    type: :Person
  AddTriple (2a1f7352-9ee8-4f51-bae7-38990534e461)
 Call ID: 2a1f7352-9ee8-4f51-bae7-38990534e461
  Args:
    source: Franz_Wilhelm_Prince_of_Prussia
    target: Karl_Franz_of_Prussia
    relation: :hasFather
  AddTriple (03d50388-82d2-4b74-9547-d9b7fc4a16ae)
 Call ID: 03d50388-82d2-4b74-9547-d9b7fc4a16ae
  Args:
    source: Franz_Wilhelm_Prince_of_Prussia
    target: Henriette_von_Schönaich-Carolath
    relation: :hasMother
  AssignClass (f249767b-f64f-4d49-8d4e-80bbdf1511a7)
 Call ID: f249767b-f64f-4d49-8d4e-80bbdf1511a7
  Args:
    source: Friedrich_Christian_of_Prussia
    type: :Man
  AssignClass (f4e03544-aa0d-4c16-8932-4d91b92b3085)
 Call ID: f4e03544-aa0d-4c16-8932-4d91b92b3085
  Args:
    source: Friedrich_Christian_of_Prussia
    type: :Person
  AddTriple (98daeadb-4696-459d-948d-944d2290c384)
 Call ID: 98daeadb-4696-459d-948d-944d2290c384
  Args:
    relation: :hasBrother
    target: Friedrich_Christian_of_Prussia
    source: Franz_Wilhelm_Prince_of_Prussia
  AssignClass (c8ba4b06-5ea7-4f51-8fb0-3434287c6077)
 Call ID: c8ba4b06-5ea7-4f51-8fb0-3434287c6077
  Args:
    source: Joachim_of_Prussia
    type: :Man
  AssignClass (714c1cf7-fa2a-41a8-8119-4da649b120fa)
 Call ID: 714c1cf7-fa2a-41a8-8119-4da649b120fa
  Args:
    source: Joachim_of_Prussia
    type: :Person
  AddTriple (aa342a29-91bf-4c3d-9ae4-0d524ae84ddd)
 Call ID: aa342a29-91bf-4c3d-9ae4-0d524ae84ddd
  Args:
    source: Franz_Wilhelm_Prince_of_Prussia
    target: Joachim_of_Prussia
    relation: :hasAncestor
  AssignClass (95e12560-df62-4de5-b27e-ecc48ec948f6)
 Call ID: 95e12560-df62-4de5-b27e-ecc48ec948f6
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Man
  AssignClass (82c23f23-7f03-463a-b856-f57e7583e09d)
 Call ID: 82c23f23-7f03-463a-b856-f57e7583e09d
  Args:
    source: Wilhelm_II_German_Emperor
    type: :Person
  AddTriple (b747f66f-0733-4430-8fc3-ea0291b83f6c)
 Call ID: b747f66f-0733-4430-8fc3-ea0291b83f6c
  Args:
    target: Wilhelm_II_German_Emperor
    source: Joachim_of_Prussia
    relation: :hasFather
  AssignClass (2020a937-9130-43c6-9771-cdd70a834c80)
 Call ID: 2020a937-9130-43c6-9771-cdd70a834c80
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (f7e1b0eb-a7b9-4d77-9554-dc386351ff80)
 Call ID: f7e1b0eb-a7b9-4d77-9554-dc386351ff80
  Args:
    source: Maria_Vladimirovna_of_Russia
    type: :Person
  AddLiteral (2edc4624-13b8-450a-84e5-b4d95bf77aff)
 Call ID: 2edc4624-13b8-450a-84e5-b4d95bf77aff
  Args:
    literal_value: 1976
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Franz_Wilhelm_Prince_of_Prussia
  AddTriple (e9e19146-aaac-487a-beb9-86d8f4fbb0d2)
 Call ID: e9e19146-aaac-487a-beb9-86d8f4fbb0d2
  Args:
    relation: :hasRelation
    source: Franz_Wilhelm_Prince_of_Prussia
    target: Maria_Vladimirovna_of_Russia
  AssignClass (89b68cae-3649-4d52-a7b9-78f95f85ff6d)
 Call ID: 89b68cae-3649-4d52-a7b9-78f95f85ff6d
  Args:
    source: Nadia_Nour_El_Etreby
    type: :Woman
  AssignClass (73c25351-612a-4134-8d1d-2903870ed711)
 Call ID: 73c25351-612a-4134-8d1d-2903870ed711
  Args:
    source: Nadia_Nour_El_Etreby
    type: :Person
  AddLiteral (071a6ba4-d7f3-4bd4-ad45-dadd8ef4369c)
 Call ID: 071a6ba4-d7f3-4bd4-ad45-dadd8ef4369c
  Args:
    relation: :hasBirthYear
    source: Nadia_Nour_El_Etreby
    literal_type: xsd:integer
    literal_value: 1949
  AddLiteral (3b9ef88b-e6bf-4443-9f0f-02c6dae7781d)
 Call ID: 3b9ef88b-e6bf-4443-9f0f-02c6dae7781d
  Args:
    relation: :hasMarriageYear
    source: Franz_Wilhelm_Prince_of_Prussia
    literal_type: xsd:integer
    literal_value: 2019
  AddTriple (56f494cc-8d94-4586-b05e-dbfd3e72f1f5)
 Call ID: 56f494cc-8d94-4586-b05e-dbfd3e72f1f5
  Args:
    relation: :hasRelation
    source: Franz_Wilhelm_Prince_of_Prussia
    target: Nadia_Nour_El_Etreby
  AssignClass (f6ae207d-3b9b-4a34-8b2f-4a528c6240ca)
 Call ID: f6ae207d-3b9b-4a34-8b2f-4a528c6240ca
  Args:
    source: Vladimir_of_Russia
    type: :Man
  AssignClass (76b590ea-6ac9-4d0b-a023-8a20b272aba9)
 Call ID: 76b590ea-6ac9-4d0b-a023-8a20b272aba9
  Args:
    source: Vladimir_of_Russia
    type: :Person
  Finish (4617e286-05d2-438e-830f-6b278b68457c)
 Call ID: 4617e286-05d2-438e-830f-6b278b68457c
  Args: