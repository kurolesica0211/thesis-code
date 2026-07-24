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
  AssignClass (0166a30c-6546-4336-a511-70f711d5be04)
 Call ID: 0166a30c-6546-4336-a511-70f711d5be04
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (6f5104da-85e9-4f52-9aa2-d1733520353a)
 Call ID: 6f5104da-85e9-4f52-9aa2-d1733520353a
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (c05eedd2-cb2f-4d4f-b7e8-dfbd1c0390ee)
 Call ID: c05eedd2-cb2f-4d4f-b7e8-dfbd1c0390ee
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (70307b2d-e472-481d-90d5-e60159659576)
 Call ID: 70307b2d-e472-481d-90d5-e60159659576
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Woman
  AssignClass (66c10810-6752-4755-9ef4-86e7a432a514)
 Call ID: 66c10810-6752-4755-9ef4-86e7a432a514
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (517b5f01-b8eb-452d-abb4-b9d23665afcc)
 Call ID: 517b5f01-b8eb-452d-abb4-b9d23665afcc
  Args:
    type: :Woman
    source: Marian_Elizabeth
  AssignClass (2acec841-9741-4a44-b7ce-0cb02e19a89e)
 Call ID: 2acec841-9741-4a44-b7ce-0cb02e19a89e
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (4957ee28-1822-4f65-8bb8-283b905248da)
 Call ID: 4957ee28-1822-4f65-8bb8-283b905248da
  Args:
    source: Nicholas_Knatchbull
    type: :Man
  AssignClass (a20bb21a-51cd-4e10-ac10-f7cd1906d922)
 Call ID: a20bb21a-51cd-4e10-ac10-f7cd1906d922
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AddLiteral (67dba56f-78eb-4c90-8166-2356c576c0f0)
 Call ID: 67dba56f-78eb-4c90-8166-2356c576c0f0
  Args:
    relation: :hasBirthYear
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1947
    literal_type: xsd:integer
  AddLiteral (693491c6-8367-4568-bdf0-f3021166cf37)
 Call ID: 693491c6-8367-4568-bdf0-f3021166cf37
  Args:
    literal_type: xsd:string
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Romsey
    relation: :formerlyKnownAs
  AddLiteral (2547947b-0848-4dc1-b921-918ec555e99e)
 Call ID: 2547947b-0848-4dc1-b921-918ec555e99e
  Args:
    literal_value: Lord Brabourne
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AddTriple (561334c1-d2f3-4991-a264-eb9886f1b3e5)
 Call ID: 561334c1-d2f3-4991-a264-eb9886f1b3e5
  Args:
    relation: :hasMother
    target: Patricia_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (8379060a-d119-418b-bcaf-1ff6d20d416a)
 Call ID: 8379060a-d119-418b-bcaf-1ff6d20d416a
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasFather
    target: John_Knatchbull
  AddTriple (84d838fc-9caa-4cab-9b9a-8fae96b2aa19)
 Call ID: 84d838fc-9caa-4cab-9b9a-8fae96b2aa19
  Args:
    source: Penelope_Meredith_Eastwood
    relation: :hasMother
    target: Marian_Elizabeth
  AddTriple (8c8deae2-8685-4aa9-93bf-1f512196f1a0)
 Call ID: 8c8deae2-8685-4aa9-93bf-1f512196f1a0
  Args:
    source: Penelope_Meredith_Eastwood
    target: Reginald_Wray_Frank_Eastwood
    relation: :hasFather
  AddTriple (8ea60963-5c1a-461c-98d0-cd45fba54881)
 Call ID: 8ea60963-5c1a-461c-98d0-cd45fba54881
  Args:
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (5a1ee8c2-ebce-4cb7-a970-0e9c634568f7)
 Call ID: 5a1ee8c2-ebce-4cb7-a970-0e9c634568f7
  Args:
    literal_type: xsd:integer
    literal_value: 1979
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMarriageYear
  AddLiteral (a64130d7-6e15-4cb8-837b-b4d3a33650e4)
 Call ID: a64130d7-6e15-4cb8-837b-b4d3a33650e4
  Args:
    literal_value: 1953
    source: Penelope_Meredith_Eastwood
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (58116c89-b4e3-40d0-bd9f-0576a4b4cb13)
 Call ID: 58116c89-b4e3-40d0-bd9f-0576a4b4cb13
  Args:
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1912
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (7c757e57-7790-466b-a6df-deb8c366493e)
 Call ID: 7c757e57-7790-466b-a6df-deb8c366493e
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    source: Reginald_Wray_Frank_Eastwood
    relation: :hasDeathYear
  AddLiteral (7bdfa9b3-1f90-4701-b7a3-55928385deb6)
 Call ID: 7bdfa9b3-1f90-4701-b7a3-55928385deb6
  Args:
    literal_type: xsd:integer
    literal_value: 1926
    source: Marian_Elizabeth
    relation: :hasBirthYear
  AddLiteral (769bb466-4127-414f-94ca-128836bea536)
 Call ID: 769bb466-4127-414f-94ca-128836bea536
  Args:
    literal_type: xsd:integer
    source: Marian_Elizabeth
    literal_value: 2020
    relation: :hasDeathYear
  AddTriple (34521f3a-cbc9-4805-828a-2bd96212bc54)
 Call ID: 34521f3a-cbc9-4805-828a-2bd96212bc54
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Nicholas_Knatchbull
    relation: :hasBrother
  AddTriple (0eec3f4a-b2a0-4282-bc66-1653ed413345)
 Call ID: 0eec3f4a-b2a0-4282-bc66-1653ed413345
  Args:
    source: Nicholas_Knatchbull
    target: Patricia_Knatchbull
    relation: :hasMother
  AddTriple (9fc8c7db-10ca-4574-b897-db134d0c3f55)
 Call ID: 9fc8c7db-10ca-4574-b897-db134d0c3f55
  Args:
    target: John_Knatchbull
    relation: :hasFather
    source: Nicholas_Knatchbull
  AddTriple (e82cc750-e675-4799-9088-765b2ff7aa73)
 Call ID: e82cc750-e675-4799-9088-765b2ff7aa73
  Args:
    relation: :hasMother
    target: Doreen_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (ce9cc6b7-4b7a-4942-a60e-d9e066d8cf4f)
 Call ID: ce9cc6b7-4b7a-4942-a60e-d9e066d8cf4f
  Args:
    source: John_Knatchbull
    target: Doreen_Knatchbull
    relation: :hasFather
  AddTriple (37c38eb5-3db3-4f74-91e5-0900139d489e)
 Call ID: 37c38eb5-3db3-4f74-91e5-0900139d489e
  Args:
    source: Patricia_Knatchbull
    relation: :hasMother
    target: Louis_Mountbatten
  AddLiteral (775524ad-3621-4c29-b1a1-c6d75b3f38b1)
 Call ID: 775524ad-3621-4c29-b1a1-c6d75b3f38b1
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1979
    source: Louis_Mountbatten
  AddLiteral (67113d52-d798-47c5-ae93-5d1c2c902cf0)
 Call ID: 67113d52-d798-47c5-ae93-5d1c2c902cf0
  Args:
    relation: :hasDeathYear
    literal_value: 1979
    source: Nicholas_Knatchbull
    literal_type: xsd:integer
  AddLiteral (be9fd094-bdc6-449b-8431-9794d9d57975)
 Call ID: be9fd094-bdc6-449b-8431-9794d9d57975
  Args:
    source: Doreen_Knatchbull
    literal_value: 1979
    literal_type: xsd:integer
    relation: :hasDeathYear
  Finish (be254309-073a-441e-b9d1-b0a1755f5d9a)
 Call ID: be254309-073a-441e-b9d1-b0a1755f5d9a
  Args: