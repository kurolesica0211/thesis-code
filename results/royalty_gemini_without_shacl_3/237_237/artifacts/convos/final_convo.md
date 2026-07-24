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
  AssignClass (3c016355-a956-421a-a510-cc14faa4ed93)
 Call ID: 3c016355-a956-421a-a510-cc14faa4ed93
  Args:
    source: FriedrichAugustOfOldenburg
    type: :Man
  AssignClass (caf1c124-c0c3-493d-8bcb-141e5a1e7a7e)
 Call ID: caf1c124-c0c3-493d-8bcb-141e5a1e7a7e
  Args:
    source: NikolausHereditaryGrandDukeOfOldenburg
    type: :Man
  AssignClass (3dba4c3c-8726-4ee3-8d7b-631f3ed68ec5)
 Call ID: 3dba4c3c-8726-4ee3-8d7b-631f3ed68ec5
  Args:
    source: PrincessHelenaOfWaldeckAndPyrmont
    type: :Woman
  AddLiteral (f0c33fdd-528f-4578-8f4c-f6b38938cb83)
 Call ID: f0c33fdd-528f-4578-8f4c-f6b38938cb83
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1936
    source: FriedrichAugustOfOldenburg
  AddLiteral (c97fa215-6840-482d-879b-c0041a0bed0f)
 Call ID: c97fa215-6840-482d-879b-c0041a0bed0f
  Args:
    source: FriedrichAugustOfOldenburg
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (ebb65923-e15c-4e79-bd0e-1ee2787a1555)
 Call ID: ebb65923-e15c-4e79-bd0e-1ee2787a1555
  Args:
    source: FriedrichAugustOfOldenburg
    target: NikolausHereditaryGrandDukeOfOldenburg
    relation: :hasFather
  AddTriple (179e2da2-709c-4e17-9552-028e74a632e9)
 Call ID: 179e2da2-709c-4e17-9552-028e74a632e9
  Args:
    source: FriedrichAugustOfOldenburg
    relation: :hasMother
    target: PrincessHelenaOfWaldeckAndPyrmont
  AssignClass (011e95a5-0810-4ef8-8dfa-2996a45649d9)
 Call ID: 011e95a5-0810-4ef8-8dfa-2996a45649d9
  Args:
    type: :Man
    source: FrederickAugustusII_GrandDukeOfOldenburg
  AssignClass (c3b220a1-4a2b-4288-808d-b6cc7048cef1)
 Call ID: c3b220a1-4a2b-4288-808d-b6cc7048cef1
  Args:
    source: DuchessElisabethAlexandrineOfMecklenburgSchwerin
    type: :Woman
  AssignClass (9f9f2a2d-74e6-4cf8-86b6-e389823ceaae)
 Call ID: 9f9f2a2d-74e6-4cf8-86b6-e389823ceaae
  Args:
    type: :Man
    source: Friedrich_PrinceOfWaldeckAndPyrmont
  AssignClass (5c4b813b-e048-4705-9437-594806dddc5c)
 Call ID: 5c4b813b-e048-4705-9437-594806dddc5c
  Args:
    type: :Woman
    source: PrincessBathildisOfSchaumburgLippe
  AddTriple (4b26b4d2-0edf-4450-8437-19965c8c7f7b)
 Call ID: 4b26b4d2-0edf-4450-8437-19965c8c7f7b
  Args:
    source: NikolausHereditaryGrandDukeOfOldenburg
    target: FrederickAugustusII_GrandDukeOfOldenburg
    relation: :hasFather
  AddTriple (0be4255e-cbe2-4e00-9b85-fb9baa6f1858)
 Call ID: 0be4255e-cbe2-4e00-9b85-fb9baa6f1858
  Args:
    target: DuchessElisabethAlexandrineOfMecklenburgSchwerin
    relation: :hasMother
    source: NikolausHereditaryGrandDukeOfOldenburg
  AddTriple (1e029d87-9837-431f-801d-c29d285f8e61)
 Call ID: 1e029d87-9837-431f-801d-c29d285f8e61
  Args:
    relation: :hasFather
    target: Friedrich_PrinceOfWaldeckAndPyrmont
    source: PrincessHelenaOfWaldeckAndPyrmont
  AddTriple (f9137e2f-c5c8-4a28-8c02-a1a81077188b)
 Call ID: f9137e2f-c5c8-4a28-8c02-a1a81077188b
  Args:
    relation: :hasMother
    target: PrincessBathildisOfSchaumburgLippe
    source: PrincessHelenaOfWaldeckAndPyrmont
  AssignClass (37c0307f-06f9-43b3-9690-b508e17f527d)
 Call ID: 37c0307f-06f9-43b3-9690-b508e17f527d
  Args:
    type: :Man
    source: Christian_DukeOfOldenburg
  AddTriple (244d829e-67b1-4fbe-baf7-f2bcc07a37f6)
 Call ID: 244d829e-67b1-4fbe-baf7-f2bcc07a37f6
  Args:
    target: Christian_DukeOfOldenburg
    relation: :isUncleOf
    source: FriedrichAugustOfOldenburg
  AssignClass (826721e9-1e87-4172-a310-d49d56db17d3)
 Call ID: 826721e9-1e87-4172-a310-d49d56db17d3
  Args:
    source: PrincessMarieCecileOfPrussia
    type: :Woman
  AddTriple (18bb10b5-ae97-47b7-a07b-c6263e756e99)
 Call ID: 18bb10b5-ae97-47b7-a07b-c6263e756e99
  Args:
    relation: :hasRelation
    target: PrincessMarieCecileOfPrussia
    source: FriedrichAugustOfOldenburg
  AssignClass (b6e8a17e-79b1-4f3e-af46-4d5f44a2a2e1)
 Call ID: b6e8a17e-79b1-4f3e-af46-4d5f44a2a2e1
  Args:
    type: :Man
    source: LouisFerdinand_PrinceOfPrussia
  AssignClass (24f233b4-2dd5-4988-ae88-cb0e4c791efa)
 Call ID: 24f233b4-2dd5-4988-ae88-cb0e4c791efa
  Args:
    source: GrandDuchessKiraKirillovnaOfRussia
    type: :Woman
  AddTriple (f6eaf888-03a9-4185-9521-5a05fad2ec20)
 Call ID: f6eaf888-03a9-4185-9521-5a05fad2ec20
  Args:
    source: PrincessMarieCecileOfPrussia
    target: LouisFerdinand_PrinceOfPrussia
    relation: :hasFather
  AddTriple (03143da7-2ea1-48af-a2f9-117a3f6d148c)
 Call ID: 03143da7-2ea1-48af-a2f9-117a3f6d148c
  Args:
    relation: :hasMother
    target: GrandDuchessKiraKirillovnaOfRussia
    source: PrincessMarieCecileOfPrussia
  AssignClass (34536f71-a6a6-4fdf-a3df-87a5d9e57db3)
 Call ID: 34536f71-a6a6-4fdf-a3df-87a5d9e57db3
  Args:
    type: :Woman
    source: DonataCountessOfCastellRudenhausen
  AddTriple (ca0f5825-fd71-4477-ba0d-98e6362cecb7)
 Call ID: ca0f5825-fd71-4477-ba0d-98e6362cecb7
  Args:
    source: FriedrichAugustOfOldenburg
    target: DonataCountessOfCastellRudenhausen
    relation: :hasRelation
  AddLiteral (2b71152f-8e6d-4269-8cc7-73a966bc373b)
 Call ID: 2b71152f-8e6d-4269-8cc7-73a966bc373b
  Args:
    literal_value: 1991
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: DonataCountessOfCastellRudenhausen
  Finish (8836c1f4-317a-4964-82bc-68826c024ebc)
 Call ID: 8836c1f4-317a-4964-82bc-68826c024ebc
  Args: