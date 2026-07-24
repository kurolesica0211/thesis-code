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
John David James Dalrymple, 14th Earl of Stair (born 4 September 1961) is a British politician and a former crossbench member of the House of Lords.
Background

Stair is the eldest child of John Dalrymple, 13th
Earl of Stair and Davina Katherine Bowes-Lyon (2 May 1930 – 1 November 2017), daughter of David Bowes-Lyon, brother of Queen Elizabeth
Lord Stair's mother, Davina, therefore, was a first cousin of Queen Elizabeth II and he is a second cousin of The King, The Princess Royal, Andrew Mountbatten-Windsor, and The Duke of Edinburgh.
Through his mother, he is descended from the Bowes-Lyon, Astor, and Cavendish-Bentinck families.
Through his paternal-grandmother, Violet Evelyn Dalrymple (Née Harford), he is a direct descendent of Frederick Calvert, 6th Baron Baltimore, the Calvert family were the founders and Proprietors of Province of Maryland.
Political career

Upon inheriting his peerage in 1996, Lord Stair entered the House of Lords and sat as a crossbencher.
Following the death of Davina Ingrams, 18th Baroness Darcy de Knayth in 2008, Lord Stair was elected to the Lords.
Family

Lord Stair married Emily Mary Julia Stonor (daughter of Ralph Stonor, 7th Baron Camoys, and Elizabeth Mary Hyde Parker) in 2006.



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
  AssignClass (1d01259c-6c8f-40e5-9c07-9f5c36de2d54)
 Call ID: 1d01259c-6c8f-40e5-9c07-9f5c36de2d54
  Args:
    type: :Man
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
  AssignClass (2f3419b4-758b-4441-b607-c2c6c3a7db3e)
 Call ID: 2f3419b4-758b-4441-b607-c2c6c3a7db3e
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    type: :Person
  AddLiteral (c9f2275a-9d28-4333-8ffe-2baca52bf72d)
 Call ID: c9f2275a-9d28-4333-8ffe-2baca52bf72d
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1961
  AssignClass (ae8571cf-a19f-4a54-967a-be537a75f388)
 Call ID: ae8571cf-a19f-4a54-967a-be537a75f388
  Args:
    source: John_Dalrymple_13th_Earl_of_Stair
    type: :Man
  AssignClass (227b890a-521f-42c0-bc7b-f2600094ae9c)
 Call ID: 227b890a-521f-42c0-bc7b-f2600094ae9c
  Args:
    source: John_Dalrymple_13th_Earl_of_Stair
    type: :Person
  AssignClass (1d5bd486-3a8b-44a8-8531-ca1c01df3859)
 Call ID: 1d5bd486-3a8b-44a8-8531-ca1c01df3859
  Args:
    type: :Woman
    source: Davina_Katherine_Bowes-Lyon
  AssignClass (64df0bd1-95c4-436c-a336-05de57c3337d)
 Call ID: 64df0bd1-95c4-436c-a336-05de57c3337d
  Args:
    source: Davina_Katherine_Bowes-Lyon
    type: :Person
  AddLiteral (57c4fb33-8c45-4b44-adfb-c3f7adb8f767)
 Call ID: 57c4fb33-8c45-4b44-adfb-c3f7adb8f767
  Args:
    literal_value: 1930
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: Davina_Katherine_Bowes-Lyon
  AddLiteral (fcb851bc-285b-4152-ab07-b1554f659c7c)
 Call ID: fcb851bc-285b-4152-ab07-b1554f659c7c
  Args:
    source: Davina_Katherine_Bowes-Lyon
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    literal_value: 2017
  AddTriple (0058c3fc-43e0-4644-80e8-90266274202f)
 Call ID: 0058c3fc-43e0-4644-80e8-90266274202f
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    relation: :hasFather
    target: John_Dalrymple_13th_Earl_of_Stair
  AddTriple (b0e3ec5f-edaa-44ce-8ec5-abbdaef76404)
 Call ID: b0e3ec5f-edaa-44ce-8ec5-abbdaef76404
  Args:
    target: Davina_Katherine_Bowes-Lyon
    relation: :hasMother
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
  AssignClass (926301cd-d2ab-4e10-9d23-acb48c0e40b8)
 Call ID: 926301cd-d2ab-4e10-9d23-acb48c0e40b8
  Args:
    type: :Man
    source: David_Bowes-Lyon
  AssignClass (a0693762-ca59-4972-8b51-392e674a4165)
 Call ID: a0693762-ca59-4972-8b51-392e674a4165
  Args:
    type: :Person
    source: David_Bowes-Lyon
  AddTriple (2013f053-6d7b-47c1-9099-f9b4d196599b)
 Call ID: 2013f053-6d7b-47c1-9099-f9b4d196599b
  Args:
    relation: :hasFather
    source: Davina_Katherine_Bowes-Lyon
    target: David_Bowes-Lyon
  AssignClass (31693be7-1cb5-4bc5-a9cd-200f9c9a3340)
 Call ID: 31693be7-1cb5-4bc5-a9cd-200f9c9a3340
  Args:
    type: :Woman
    source: Queen_Elizabeth
  AssignClass (a006ca9b-13e4-4253-b5f6-6f8de4b335b1)
 Call ID: a006ca9b-13e4-4253-b5f6-6f8de4b335b1
  Args:
    type: :Person
    source: Queen_Elizabeth
  AddTriple (1f1ba154-0a1e-4132-b2ea-fdd82ae1ef93)
 Call ID: 1f1ba154-0a1e-4132-b2ea-fdd82ae1ef93
  Args:
    relation: :isSisterOf
    source: David_Bowes-Lyon
    target: Queen_Elizabeth
  AssignClass (fe01a9c1-b75c-4242-9242-2d10717ad865)
 Call ID: fe01a9c1-b75c-4242-9242-2d10717ad865
  Args:
    type: :Woman
    source: Violet_Evelyn_Dalrymple
  AssignClass (fa18c677-18ad-4b5a-a6df-527aabf8580a)
 Call ID: fa18c677-18ad-4b5a-a6df-527aabf8580a
  Args:
    type: :Person
    source: Violet_Evelyn_Dalrymple
  AddTriple (69ee2e80-641c-49b9-bd97-3926eb5a93f3)
 Call ID: 69ee2e80-641c-49b9-bd97-3926eb5a93f3
  Args:
    target: Violet_Evelyn_Dalrymple
    relation: :hasMother
    source: John_Dalrymple_13th_Earl_of_Stair
  AssignClass (57db7b23-fa2d-4d6c-9fb6-008b5ceed4f2)
 Call ID: 57db7b23-fa2d-4d6c-9fb6-008b5ceed4f2
  Args:
    source: Frederick_Calvert_6th_Baron_Baltimore
    type: :Man
  AssignClass (cb959e97-408e-4fd8-830c-855c28caf117)
 Call ID: cb959e97-408e-4fd8-830c-855c28caf117
  Args:
    source: Frederick_Calvert_6th_Baron_Baltimore
    type: :Person
  AddTriple (5255f324-4ebf-4db1-b5e8-7f0850f23b2c)
 Call ID: 5255f324-4ebf-4db1-b5e8-7f0850f23b2c
  Args:
    target: Frederick_Calvert_6th_Baron_Baltimore
    relation: :hasAncestor
    source: Violet_Evelyn_Dalrymple
  AssignClass (c9657e7b-bff0-4f5a-af8d-b47db02ee4e5)
 Call ID: c9657e7b-bff0-4f5a-af8d-b47db02ee4e5
  Args:
    source: Emily_Mary_Julia_Stonor
    type: :Woman
  AssignClass (8bcf4af1-2cfd-4078-a885-ea53cca9fff2)
 Call ID: 8bcf4af1-2cfd-4078-a885-ea53cca9fff2
  Args:
    type: :Person
    source: Emily_Mary_Julia_Stonor
  AddTriple (6c4d473f-5f4b-4ea3-a041-bac7b1345b73)
 Call ID: 6c4d473f-5f4b-4ea3-a041-bac7b1345b73
  Args:
    relation: :hasRelation
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    target: Emily_Mary_Julia_Stonor
  AddLiteral (087e4223-1ac7-424f-948a-de6a3377407d)
 Call ID: 087e4223-1ac7-424f-948a-de6a3377407d
  Args:
    source: John_David_James_Dalrymple_14th_Earl_of_Stair
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    literal_value: 2006
  AssignClass (44364d80-123b-48ae-9677-13546df2f452)
 Call ID: 44364d80-123b-48ae-9677-13546df2f452
  Args:
    source: Ralph_Stonor_7th_Baron_Camoys
    type: :Man
  AssignClass (ec95e89a-44bf-4b8a-a5a4-74f2c59f0bc1)
 Call ID: ec95e89a-44bf-4b8a-a5a4-74f2c59f0bc1
  Args:
    type: :Person
    source: Ralph_Stonor_7th_Baron_Camoys
  AssignClass (aa6e385f-8fbe-4663-a752-abde7017a67c)
 Call ID: aa6e385f-8fbe-4663-a752-abde7017a67c
  Args:
    source: Elizabeth_Mary_Hyde_Parker
    type: :Woman
  AssignClass (4d00c3de-d074-4579-a6a5-d98afdbe385f)
 Call ID: 4d00c3de-d074-4579-a6a5-d98afdbe385f
  Args:
    type: :Person
    source: Elizabeth_Mary_Hyde_Parker
  AddTriple (3b762700-0457-42ff-895b-628736bb4e1a)
 Call ID: 3b762700-0457-42ff-895b-628736bb4e1a
  Args:
    relation: :hasFather
    source: Emily_Mary_Julia_Stonor
    target: Ralph_Stonor_7th_Baron_Camoys
  AddTriple (c4cbace1-55ae-4388-b8bf-a2a43db888a3)
 Call ID: c4cbace1-55ae-4388-b8bf-a2a43db888a3
  Args:
    target: Elizabeth_Mary_Hyde_Parker
    relation: :hasMother
    source: Emily_Mary_Julia_Stonor
  Finish (4ca1ebbc-74f3-4c8f-806d-de2cea8cc070)
 Call ID: 4ca1ebbc-74f3-4c8f-806d-de2cea8cc070
  Args: