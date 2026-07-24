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
Norton Louis Philip Knatchbull, 3rd Earl Mountbatten of Burma (born 8 October 1947), known until 2005 as Lord Romsey and until 2017 as the Lord Brabourne, is a British peer.
Life and education

Mountbatten was born at King's College Hospital in London as the eldest son of Patricia Knatchbull, née Mountbatten, later 2nd Countess Mountbatten of Burma, and film producer John Knatchbull, 7th Baron Brabourne.
Mountbatten was educated at the Dragon School, in Oxford, and Gordonstoun School, Elgin, Moray, Scotland.
On the death of his father on 23 September 2005, he became the 8th Baron Brabourne, of Brabourne in the County of Kent, in the peerage of the United Kingdom.
He also succeeded to the Knatchbull Baronetcy, of Mersham Hatch in the County of Kent, in the baronetage of England.
On the death of his mother on 13 June 2017, he became Earl Mountbatten of Burma, also a title in the peerage of the United Kingdom created for his grandfather, Admiral of the Fleet Lord Louis Mountbatten.
Mountbatten is the godfather of Philip's grandson, the Prince of Wales.
He is also related to author Jane Austen, as his father, John Knatchbull, 7th Baron Brabourne, was a direct descendant of her brother Edward Austen Knight.
Marriage and children

Mountbatten is married to Penelope Meredith Eastwood (born 16 April 1953), a daughter of Reginald Wray Frank Eastwood (1912–1980), a self-made millionaire former butcher who founded the Angus Steakhouse chain, and Marian Elizabeth (1926–2020), née Hood.
They were wed on 20 October 1979 at Romsey Abbey, less than two months after the IRA murdered his 79-year-old maternal grandfather, Louis Mountbatten, 1st
Earl Mountbatten of Burma; his 14-year-old younger brother, Nicholas Knatchbull; and his 83-year-old paternal grandmother, Doreen Knatchbull, Dowager Lady Brabourne.
The 3rd Earl Mountbatten of Burma and his wife have three children and three grandsons:


From 2010 to 2014, Mountbatten was in an extramarital relationship with Eugenie, Lady Nuttall, widow of Sir Nicholas Nuttall, 3rd Baronet, who was heir to the Edmund Nuttall Limited construction company.



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
  AssignClass (8a9f2825-7446-46b0-adae-dc13e9af1350)
 Call ID: 8a9f2825-7446-46b0-adae-dc13e9af1350
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (be38e47d-6f1d-4fe7-8f91-ce0dad089091)
 Call ID: be38e47d-6f1d-4fe7-8f91-ce0dad089091
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (8b450488-9851-4270-923d-373557bed572)
 Call ID: 8b450488-9851-4270-923d-373557bed572
  Args:
    literal_value: 1947
    relation: :hasBirthYear
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:integer
  AddLiteral (4e0d7ea2-1bdb-41f9-af03-320f12aac1c3)
 Call ID: 4e0d7ea2-1bdb-41f9-af03-320f12aac1c3
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
    literal_value: Lord Romsey
    relation: :formerlyKnownAs
  AddLiteral (f96f61e3-4f51-4e5c-bae5-3a85e30c5105)
 Call ID: f96f61e3-4f51-4e5c-bae5-3a85e30c5105
  Args:
    relation: :formerlyKnownAs
    literal_value: Lord Brabourne
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
  AssignClass (4bf0de64-d6db-4aef-9f45-92a774da3fc8)
 Call ID: 4bf0de64-d6db-4aef-9f45-92a774da3fc8
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (e92ee905-e30c-4e2d-ae3e-57d569bf00a3)
 Call ID: e92ee905-e30c-4e2d-ae3e-57d569bf00a3
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (9f72d2a8-92f5-4293-900b-f097fb201318)
 Call ID: 9f72d2a8-92f5-4293-900b-f097fb201318
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (dead64f4-9b8a-4931-851e-e12c0f93df97)
 Call ID: dead64f4-9b8a-4931-851e-e12c0f93df97
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (1d75e419-4f6d-4971-8086-91eebf5ea6af)
 Call ID: 1d75e419-4f6d-4971-8086-91eebf5ea6af
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Knatchbull
    relation: :hasMother
  AddTriple (5ce5a35b-5502-47ad-9399-f9b1403ccbd7)
 Call ID: 5ce5a35b-5502-47ad-9399-f9b1403ccbd7
  Args:
    target: John_Knatchbull
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (ca6856ad-710f-4008-81ae-034f1ac30955)
 Call ID: ca6856ad-710f-4008-81ae-034f1ac30955
  Args:
    source: John_Knatchbull
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2005
  AddLiteral (edcc1bc2-3fd0-4937-803a-c8567749cf7a)
 Call ID: edcc1bc2-3fd0-4937-803a-c8567749cf7a
  Args:
    literal_value: 2017
    relation: :hasDeathYear
    source: Patricia_Knatchbull
    literal_type: xsd:integer
  AssignClass (d01ac23d-6117-41d0-88cc-a627f9126623)
 Call ID: d01ac23d-6117-41d0-88cc-a627f9126623
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (653b9063-7c24-4879-b55f-8e3931eaaf97)
 Call ID: 653b9063-7c24-4879-b55f-8e3931eaaf97
  Args:
    type: :Person
    source: Louis_Mountbatten
  AssignClass (702a0d27-1053-48c3-a34f-9e6b65589ff5)
 Call ID: 702a0d27-1053-48c3-a34f-9e6b65589ff5
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (58413632-4c8c-48fa-b0b7-dbfdffefa45d)
 Call ID: 58413632-4c8c-48fa-b0b7-dbfdffefa45d
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AssignClass (91d107f3-ae6c-471b-8e1c-cfc8f3cf4528)
 Call ID: 91d107f3-ae6c-471b-8e1c-cfc8f3cf4528
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (c8f30ebc-eb1d-4752-9c21-13c7a4bc340e)
 Call ID: c8f30ebc-eb1d-4752-9c21-13c7a4bc340e
  Args:
    type: :Person
    source: Doreen_Knatchbull
  AddTriple (14f9db67-1e84-482a-b525-8c30977cbda4)
 Call ID: 14f9db67-1e84-482a-b525-8c30977cbda4
  Args:
    relation: :isBrotherOf
    target: Norton_Louis_Philip_Knatchbull
    source: Nicholas_Knatchbull
  AssignClass (36cd7a7c-5336-4af3-88d5-eaa1c4661d44)
 Call ID: 36cd7a7c-5336-4af3-88d5-eaa1c4661d44
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (5cbd0977-8d53-41f6-9028-e64277ebcf79)
 Call ID: 5cbd0977-8d53-41f6-9028-e64277ebcf79
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (2b1354c0-cd3e-493f-b3c9-c71350b71634)
 Call ID: 2b1354c0-cd3e-493f-b3c9-c71350b71634
  Args:
    relation: :hasBirthYear
    literal_value: 1953
    literal_type: xsd:integer
    source: Penelope_Meredith_Eastwood
  AddTriple (f785d12b-a407-47ba-a530-fcdac384e8ec)
 Call ID: f785d12b-a407-47ba-a530-fcdac384e8ec
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
    target: Penelope_Meredith_Eastwood
  AddLiteral (1db57bef-419e-4ba3-bade-0a603b168023)
 Call ID: 1db57bef-419e-4ba3-bade-0a603b168023
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:integer
    literal_value: 1979
    relation: :hasMarriageYear
  AssignClass (cb2aa376-2870-4c42-b981-8541fea01ee8)
 Call ID: cb2aa376-2870-4c42-b981-8541fea01ee8
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (c2ca1324-2d10-481f-82e3-a1b9d59a634c)
 Call ID: c2ca1324-2d10-481f-82e3-a1b9d59a634c
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (e1916224-629d-45bf-baa0-a88019caf98d)
 Call ID: e1916224-629d-45bf-baa0-a88019caf98d
  Args:
    type: :Woman
    source: Marian_Elizabeth
  AssignClass (8d10dfb8-dc75-465d-bfa1-568d46782415)
 Call ID: 8d10dfb8-dc75-465d-bfa1-568d46782415
  Args:
    type: :Person
    source: Marian_Elizabeth
  AddTriple (327416fd-df66-40d5-8741-43ca830a836b)
 Call ID: 327416fd-df66-40d5-8741-43ca830a836b
  Args:
    source: Penelope_Meredith_Eastwood
    target: Reginald_Wray_Frank_Eastwood
    relation: :hasFather
  AddTriple (30064560-2eee-4be8-90a3-df8811193ced)
 Call ID: 30064560-2eee-4be8-90a3-df8811193ced
  Args:
    source: Penelope_Meredith_Eastwood
    relation: :hasMother
    target: Marian_Elizabeth
  AddLiteral (8c7c4165-7ecd-4189-b7ff-6b5361287411)
 Call ID: 8c7c4165-7ecd-4189-b7ff-6b5361287411
  Args:
    relation: :hasDeathYear
    literal_value: 1980
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
  AddLiteral (f705158b-2613-4eeb-997e-53ba55aca329)
 Call ID: f705158b-2613-4eeb-997e-53ba55aca329
  Args:
    literal_value: 2020
    relation: :hasDeathYear
    source: Marian_Elizabeth
    literal_type: xsd:integer
  AssignClass (3e01d776-ce09-4bb4-b182-269f16540d53)
 Call ID: 3e01d776-ce09-4bb4-b182-269f16540d53
  Args:
    type: :Woman
    source: Eugenie_Lady_Nuttall
  AssignClass (948d6cd4-ee04-4f07-a7b9-d507df48af01)
 Call ID: 948d6cd4-ee04-4f07-a7b9-d507df48af01
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (9b8018ad-8726-4a01-8ed1-e27fd0446e48)
 Call ID: 9b8018ad-8726-4a01-8ed1-e27fd0446e48
  Args:
    target: Eugenie_Lady_Nuttall
    relation: :hasRelation
    source: Norton_Louis_Philip_Knatchbull
  Finish (d8c84157-6b9e-4a1d-b6a4-1bce6b34300b)
 Call ID: d8c84157-6b9e-4a1d-b6a4-1bce6b34300b
  Args: