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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Prince Achileas-Andreas of Greece and Denmark (Greek: Αχιλλέας Ανδρέας Ντε Γκρες, romanized: Achilléas-Andréas de Grèce; born 12 August 2000), known by the stage name Achi Miller, is an actor, socialite, and member of the former Greek royal family and the extended Danish royal family.
He is the second son and third child of Crown Prince Pavlos of Greece and Marie-Chantal Miller.
His paternal grandparents are Constantine II of Greece and Anne-Marie of Denmark, who were the last King and Queen of the Hellenes.
Early life and education

Achileas-Andreas was born on 12 August 2000 at Weill Cornell Medical Center in New York City.
Personal life

On September 28, 2024, Achileas-Andreas served as a groomsman at the wedding of Princess Theodora of Greece and Denmark and Matthew Kumar at the Metropolitan Cathedral in Athens.
Achileas-Andreas was in a relationship with Isabella Massenet, daughter of Dame Natalie Massenet, until October 2024.
Οn 20 December 2024, Achileas-Andreas along with other members of the former royal family acquired Greek citizenship, under the surname "de Grèce".
Under the stage name Achi Miller, he had a minor role in the 2023 film No Hard Feelings.



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
  AssignClass (7dddec4d-055b-4ac3-94ec-ce485b339c26)
 Call ID: 7dddec4d-055b-4ac3-94ec-ce485b339c26
  Args:
    type: :Man
    source: PrinceAchileas-AndreasOfGreeceAndDenmark
  AssignClass (4375e5b4-9313-4ab7-831b-6c210a4db77d)
 Call ID: 4375e5b4-9313-4ab7-831b-6c210a4db77d
  Args:
    type: :Person
    source: PrinceAchileas-AndreasOfGreeceAndDenmark
  AddLiteral (a8135b68-a675-444b-8bab-1960ebbdde04)
 Call ID: a8135b68-a675-444b-8bab-1960ebbdde04
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: PrinceAchileas-AndreasOfGreeceAndDenmark
    literal_value: Achi Miller
  AddLiteral (c7085396-421c-436f-ab9c-70e9ee54ff05)
 Call ID: c7085396-421c-436f-ab9c-70e9ee54ff05
  Args:
    source: PrinceAchileas-AndreasOfGreeceAndDenmark
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2000
  AssignClass (4af4c2c5-80fb-460d-95c4-4114370754c5)
 Call ID: 4af4c2c5-80fb-460d-95c4-4114370754c5
  Args:
    type: :Man
    source: CrownPrincePavlosOfGreece
  AssignClass (29ebeef2-0381-43cf-8f4d-8d3bd082706b)
 Call ID: 29ebeef2-0381-43cf-8f4d-8d3bd082706b
  Args:
    type: :Person
    source: CrownPrincePavlosOfGreece
  AssignClass (f7f9e579-86c9-4428-85fe-62154943d840)
 Call ID: f7f9e579-86c9-4428-85fe-62154943d840
  Args:
    type: :Woman
    source: Marie-ChantalMiller
  AssignClass (9bc8bf53-bbee-4857-aa0b-1579bc5b5ca3)
 Call ID: 9bc8bf53-bbee-4857-aa0b-1579bc5b5ca3
  Args:
    type: :Person
    source: Marie-ChantalMiller
  AddTriple (d1ee477a-a27c-4121-a5d6-1333ec236801)
 Call ID: d1ee477a-a27c-4121-a5d6-1333ec236801
  Args:
    source: PrinceAchileas-AndreasOfGreeceAndDenmark
    relation: :hasFather
    target: CrownPrincePavlosOfGreece
  AddTriple (24004bb8-25e9-4910-9669-e088c08f4652)
 Call ID: 24004bb8-25e9-4910-9669-e088c08f4652
  Args:
    relation: :hasMother
    target: Marie-ChantalMiller
    source: PrinceAchileas-AndreasOfGreeceAndDenmark
  AssignClass (302be41f-c475-48f6-9285-4ccdc92b9b5d)
 Call ID: 302be41f-c475-48f6-9285-4ccdc92b9b5d
  Args:
    type: :Man
    source: ConstantineIIOfGreece
  AssignClass (f0bedd56-2c9e-45e1-9822-f2e37d3c8d84)
 Call ID: f0bedd56-2c9e-45e1-9822-f2e37d3c8d84
  Args:
    type: :Person
    source: ConstantineIIOfGreece
  AssignClass (bfec6c18-95b9-4881-a18f-5da28952bc65)
 Call ID: bfec6c18-95b9-4881-a18f-5da28952bc65
  Args:
    type: :Woman
    source: QueenAnne-MarieOfDenmark
  AssignClass (bd07b5f2-ab6c-4067-9c39-7f4872bf7474)
 Call ID: bd07b5f2-ab6c-4067-9c39-7f4872bf7474
  Args:
    type: :Person
    source: QueenAnne-MarieOfDenmark
  AddTriple (334e3c8c-8b85-475c-bb89-94f156c5972b)
 Call ID: 334e3c8c-8b85-475c-bb89-94f156c5972b
  Args:
    relation: :hasFather
    target: ConstantineIIOfGreece
    source: CrownPrincePavlosOfGreece
  AddTriple (9c66d81d-5b93-4a2f-af4f-564adb98b602)
 Call ID: 9c66d81d-5b93-4a2f-af4f-564adb98b602
  Args:
    relation: :hasMother
    target: QueenAnne-MarieOfDenmark
    source: CrownPrincePavlosOfGreece
  AssignClass (7485b3fb-0cf4-4d39-b6c1-dc4189234fe1)
 Call ID: 7485b3fb-0cf4-4d39-b6c1-dc4189234fe1
  Args:
    type: :Woman
    source: PrincessTheodoraOfGreeceAndDenmark
  AssignClass (db58d0e3-543d-41c7-8d85-acc6e7fbf608)
 Call ID: db58d0e3-543d-41c7-8d85-acc6e7fbf608
  Args:
    type: :Person
    source: PrincessTheodoraOfGreeceAndDenmark
  AssignClass (a1b01f36-4ee6-4eb0-aa31-dd7bfc9a56ae)
 Call ID: a1b01f36-4ee6-4eb0-aa31-dd7bfc9a56ae
  Args:
    type: :Man
    source: MatthewKumar
  AssignClass (3f5fe67b-cee0-44d9-aeb5-ec8dd45b110a)
 Call ID: 3f5fe67b-cee0-44d9-aeb5-ec8dd45b110a
  Args:
    type: :Person
    source: MatthewKumar
  AssignClass (69696836-1ff6-471a-b8d3-be2a8d9024d0)
 Call ID: 69696836-1ff6-471a-b8d3-be2a8d9024d0
  Args:
    type: :Woman
    source: IsabellaMassenet
  AssignClass (917e29e9-a00d-4392-9800-a48441ee5317)
 Call ID: 917e29e9-a00d-4392-9800-a48441ee5317
  Args:
    type: :Person
    source: IsabellaMassenet
  AssignClass (671f297d-ae5a-4065-9c4c-aa2fbe3ca2f9)
 Call ID: 671f297d-ae5a-4065-9c4c-aa2fbe3ca2f9
  Args:
    type: :Woman
    source: DameNatalieMassenet
  AssignClass (6fd45a79-a1fd-4d39-b00f-4d4165b37764)
 Call ID: 6fd45a79-a1fd-4d39-b00f-4d4165b37764
  Args:
    type: :Person
    source: DameNatalieMassenet
  AddTriple (6d37b0d6-8dda-4e34-88b7-cca4453c7704)
 Call ID: 6d37b0d6-8dda-4e34-88b7-cca4453c7704
  Args:
    target: DameNatalieMassenet
    relation: :hasMother
    source: IsabellaMassenet
  AssignClass (b5708149-0884-4512-8b00-b4de0471cead)
 Call ID: b5708149-0884-4512-8b00-b4de0471cead
  Args:
    type: :Woman
    source: QueenSofiaOfSpain
  AssignClass (359990ca-31e5-43c4-86ce-381dee8aaa3b)
 Call ID: 359990ca-31e5-43c4-86ce-381dee8aaa3b
  Args:
    type: :Person
    source: QueenSofiaOfSpain
  AssignClass (7a0f2ab3-baa7-4c88-879e-70975bd5e5cb)
 Call ID: 7a0f2ab3-baa7-4c88-879e-70975bd5e5cb
  Args:
    type: :Woman
    source: MarinaConsortOfPrinceMichael
  AssignClass (5519d29d-8bb8-4825-8c9f-89e9bb681237)
 Call ID: 5519d29d-8bb8-4825-8c9f-89e9bb681237
  Args:
    type: :Person
    source: MarinaConsortOfPrinceMichael
  Finish (54d46c34-a0f7-4d13-8cc5-db94cf43c783)
 Call ID: 54d46c34-a0f7-4d13-8cc5-db94cf43c783
  Args: