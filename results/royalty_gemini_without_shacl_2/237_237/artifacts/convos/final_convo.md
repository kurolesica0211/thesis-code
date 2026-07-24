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
Duke Friedrich August of Oldenburg (11 January 1936 – 9 July 2017) was a member of the House of Holstein-Gottorp.
He is a son of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.
Family and early life

Frederich August is the sixth child and fourth son of Nikolaus, Hereditary Grand Duke of Oldenburg and his first wife Princess Helena of Waldeck and Pyrmont.
His paternal grandparents are Frederick Augustus II, Grand Duke of Oldenburg and Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin.
His maternal grandparents are Friedrich, Prince of Waldeck and Pyrmont and Princess Bathildis of Schaumburg-Lippe.
His grandfather was overthrown as Grand Duke of Oldenburg in 1918, at the end of World War I.
His father Nikolaus thus never legally succeeded to the title when the deposed Grand Duke died in 1931.
Friedrich is an uncle of Christian, Duke of Oldenburg, the current head of the House of Oldenburg.
Marriage and issue

Friedrich August's first wife was Princess Marie Cécile of Prussia, a daughter of Louis Ferdinand, Prince of Prussia (second son of William, German Crown Prince) and his wife, Grand Duchess Kira Kirillovna of Russia.
Friedrich August and Marie-Cécile have three children: a son, and two daughters.
Marie-Cécile and Friedrich August divorced on 23 November 1989.
On 9 February 1991, Friedrich August was remarried to Donata Countess of Castell-Rüdenhausen in Rüdenhausen, Germany.



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
  AssignClass (1324c10d-3c98-4bf6-a3a1-a01bf97f1ba2)
 Call ID: 1324c10d-3c98-4bf6-a3a1-a01bf97f1ba2
  Args:
    type: :Man
    source: FriedrichAugustOfOldenburg
  AssignClass (95df754d-367d-40b7-8c6c-bf4421b44575)
 Call ID: 95df754d-367d-40b7-8c6c-bf4421b44575
  Args:
    source: FriedrichAugustOfOldenburg
    type: :Person
  AddLiteral (0b8cc55c-49f2-4aa3-8f7c-e5d2ef432e0b)
 Call ID: 0b8cc55c-49f2-4aa3-8f7c-e5d2ef432e0b
  Args:
    literal_type: xsd:integer
    literal_value: 1936
    source: FriedrichAugustOfOldenburg
    relation: :hasBirthYear
  AddLiteral (c50b355c-5f5c-484d-b185-89ae9efc90b2)
 Call ID: c50b355c-5f5c-484d-b185-89ae9efc90b2
  Args:
    literal_type: xsd:integer
    literal_value: 2017
    relation: :hasDeathYear
    source: FriedrichAugustOfOldenburg
  AssignClass (0e1063e2-91f3-47fa-b71e-fa97185d32c8)
 Call ID: 0e1063e2-91f3-47fa-b71e-fa97185d32c8
  Args:
    type: :Man
    source: NikolausHereditaryGrandDukeOfOldenburg
  AssignClass (24c5c289-2021-4636-bf88-63edf7a24494)
 Call ID: 24c5c289-2021-4636-bf88-63edf7a24494
  Args:
    type: :Person
    source: NikolausHereditaryGrandDukeOfOldenburg
  AssignClass (22028bcb-a85d-434e-bce9-826908953178)
 Call ID: 22028bcb-a85d-434e-bce9-826908953178
  Args:
    type: :Woman
    source: PrincessHelenaOfWaldeckAndPyrmont
  AssignClass (cd22276b-417f-480d-8aae-b88300f67689)
 Call ID: cd22276b-417f-480d-8aae-b88300f67689
  Args:
    type: :Person
    source: PrincessHelenaOfWaldeckAndPyrmont
  AddTriple (93275939-28d5-48f8-a49c-3d3d1fd5585b)
 Call ID: 93275939-28d5-48f8-a49c-3d3d1fd5585b
  Args:
    source: FriedrichAugustOfOldenburg
    relation: :hasFather
    target: NikolausHereditaryGrandDukeOfOldenburg
  AddTriple (b121a9ec-ada5-4269-9d2c-bb90da542186)
 Call ID: b121a9ec-ada5-4269-9d2c-bb90da542186
  Args:
    relation: :hasMother
    source: FriedrichAugustOfOldenburg
    target: PrincessHelenaOfWaldeckAndPyrmont
  AssignClass (b6119ed5-be09-4930-9939-908885c5fe39)
 Call ID: b6119ed5-be09-4930-9939-908885c5fe39
  Args:
    type: :Man
    source: FrederickAugustusII_GrandDukeOfOldenburg
  AssignClass (5f94748d-0daa-4e26-9868-2ede151f209e)
 Call ID: 5f94748d-0daa-4e26-9868-2ede151f209e
  Args:
    type: :Person
    source: FrederickAugustusII_GrandDukeOfOldenburg
  AssignClass (fc22fa2c-8573-4e1e-b872-0cf1aaed2707)
 Call ID: fc22fa2c-8573-4e1e-b872-0cf1aaed2707
  Args:
    type: :Woman
    source: DuchessElisabethAlexandrineOfMecklenburgSchwerin
  AssignClass (a7c0dac3-5418-419b-992c-b9ed9050c6e8)
 Call ID: a7c0dac3-5418-419b-992c-b9ed9050c6e8
  Args:
    source: DuchessElisabethAlexandrineOfMecklenburgSchwerin
    type: :Person
  AddTriple (fafc011f-fc3d-460c-8fa3-56986b939e81)
 Call ID: fafc011f-fc3d-460c-8fa3-56986b939e81
  Args:
    target: FrederickAugustusII_GrandDukeOfOldenburg
    source: NikolausHereditaryGrandDukeOfOldenburg
    relation: :hasFather
  AddTriple (6d0589d7-5106-4fc0-94ec-b32010d135e2)
 Call ID: 6d0589d7-5106-4fc0-94ec-b32010d135e2
  Args:
    source: NikolausHereditaryGrandDukeOfOldenburg
    relation: :hasMother
    target: DuchessElisabethAlexandrineOfMecklenburgSchwerin
  AssignClass (e28f0425-6fdb-4a7c-b546-168d3a090e45)
 Call ID: e28f0425-6fdb-4a7c-b546-168d3a090e45
  Args:
    source: FriedrichPrinceOfWaldeckAndPyrmont
    type: :Man
  AssignClass (a4ae8207-1a74-434e-86f9-4c543991bbc5)
 Call ID: a4ae8207-1a74-434e-86f9-4c543991bbc5
  Args:
    source: FriedrichPrinceOfWaldeckAndPyrmont
    type: :Person
  AssignClass (610f36fb-f2de-4731-9eda-1bd3f2cb00bd)
 Call ID: 610f36fb-f2de-4731-9eda-1bd3f2cb00bd
  Args:
    type: :Woman
    source: PrincessBathildisOfSchaumburgLippe
  AssignClass (8723a756-084b-4a5e-91f0-1438c4d7057d)
 Call ID: 8723a756-084b-4a5e-91f0-1438c4d7057d
  Args:
    source: PrincessBathildisOfSchaumburgLippe
    type: :Person
  AddTriple (3ec6ccaa-73f2-44d2-90e8-d4ffc076c3b4)
 Call ID: 3ec6ccaa-73f2-44d2-90e8-d4ffc076c3b4
  Args:
    target: FriedrichPrinceOfWaldeckAndPyrmont
    relation: :hasFather
    source: PrincessHelenaOfWaldeckAndPyrmont
  AddTriple (99687362-f780-4d01-8d39-ffb1f5490a6b)
 Call ID: 99687362-f780-4d01-8d39-ffb1f5490a6b
  Args:
    target: PrincessBathildisOfSchaumburgLippe
    relation: :hasMother
    source: PrincessHelenaOfWaldeckAndPyrmont
  AssignClass (222eb333-f13c-4c6c-bb9a-ae4492981297)
 Call ID: 222eb333-f13c-4c6c-bb9a-ae4492981297
  Args:
    source: ChristianDukeOfOldenburg
    type: :Man
  AssignClass (438d795f-8e98-4dd7-b40b-05f397accfdd)
 Call ID: 438d795f-8e98-4dd7-b40b-05f397accfdd
  Args:
    type: :Person
    source: ChristianDukeOfOldenburg
  AddTriple (e0c0c4d2-56ad-4ce8-bcee-7f60ad1478a4)
 Call ID: e0c0c4d2-56ad-4ce8-bcee-7f60ad1478a4
  Args:
    target: ChristianDukeOfOldenburg
    source: FriedrichAugustOfOldenburg
    relation: :isUncleOf
  AssignClass (4339c738-6479-46bc-a116-640f4127cb5d)
 Call ID: 4339c738-6479-46bc-a116-640f4127cb5d
  Args:
    type: :Woman
    source: PrincessMarieCecileOfPrussia
  AssignClass (ee70eaa6-8d9a-4aad-b396-7a37c5f1ee40)
 Call ID: ee70eaa6-8d9a-4aad-b396-7a37c5f1ee40
  Args:
    type: :Person
    source: PrincessMarieCecileOfPrussia
  AssignClass (38be5771-b13e-40e0-a795-f434061440fb)
 Call ID: 38be5771-b13e-40e0-a795-f434061440fb
  Args:
    source: LouisFerdinandPrinceOfPrussia
    type: :Man
  AssignClass (97672491-2dce-4fc8-bf86-aa5355a80db4)
 Call ID: 97672491-2dce-4fc8-bf86-aa5355a80db4
  Args:
    type: :Person
    source: LouisFerdinandPrinceOfPrussia
  AssignClass (c9b3d507-1214-4749-bbd0-88db9b059965)
 Call ID: c9b3d507-1214-4749-bbd0-88db9b059965
  Args:
    source: GrandDuchessKiraKirillovnaOfRussia
    type: :Woman
  AssignClass (176ec0d1-6c4d-4e40-b342-30680998e4c3)
 Call ID: 176ec0d1-6c4d-4e40-b342-30680998e4c3
  Args:
    source: GrandDuchessKiraKirillovnaOfRussia
    type: :Person
  AddTriple (c8c448fd-e96f-4df2-a34b-0aa4e2c88825)
 Call ID: c8c448fd-e96f-4df2-a34b-0aa4e2c88825
  Args:
    target: LouisFerdinandPrinceOfPrussia
    source: PrincessMarieCecileOfPrussia
    relation: :hasFather
  AddTriple (4df84f49-6da6-4f8f-ba49-f897bcda02fc)
 Call ID: 4df84f49-6da6-4f8f-ba49-f897bcda02fc
  Args:
    target: GrandDuchessKiraKirillovnaOfRussia
    relation: :hasMother
    source: PrincessMarieCecileOfPrussia
  AssignClass (ba1fa794-5d76-406c-b4ea-951c5611afd2)
 Call ID: ba1fa794-5d76-406c-b4ea-951c5611afd2
  Args:
    type: :Woman
    source: DonataCountessOfCastellRudenhausen
  AssignClass (d84042eb-137c-41d3-a14b-2ecb775dd87f)
 Call ID: d84042eb-137c-41d3-a14b-2ecb775dd87f
  Args:
    type: :Person
    source: DonataCountessOfCastellRudenhausen
  Finish (1b3e32cf-78f3-4e58-8789-1a64b6dd78bc)
 Call ID: 1b3e32cf-78f3-4e58-8789-1a64b6dd78bc
  Args: