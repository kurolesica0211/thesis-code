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
  AssignClass (667d1719-017d-40b8-be87-66ea881dabb0)
 Call ID: 667d1719-017d-40b8-be87-66ea881dabb0
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (6ccf7582-cc4b-48ea-8196-c8e572bfe961)
 Call ID: 6ccf7582-cc4b-48ea-8196-c8e572bfe961
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Person
  AddLiteral (5b786e62-0977-4d21-b6be-ddbcb30e9474)
 Call ID: 5b786e62-0977-4d21-b6be-ddbcb30e9474
  Args:
    literal_value: 1947
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (d21e692d-ae3b-4b15-adaa-fea5d0e8c924)
 Call ID: d21e692d-ae3b-4b15-adaa-fea5d0e8c924
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Lord Romsey
  AddLiteral (1e43c15a-cf2c-4e2e-b662-697a172dda84)
 Call ID: 1e43c15a-cf2c-4e2e-b662-697a172dda84
  Args:
    literal_type: xsd:string
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Brabourne
    relation: :formerlyKnownAs
  AssignClass (7ccc05b2-31fb-47cd-a2fd-5fd50f734715)
 Call ID: 7ccc05b2-31fb-47cd-a2fd-5fd50f734715
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (ad94b56d-a9f8-4ec9-9deb-2f138f847e40)
 Call ID: ad94b56d-a9f8-4ec9-9deb-2f138f847e40
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (94422ab9-540a-44c5-9d93-5ffd058d70f3)
 Call ID: 94422ab9-540a-44c5-9d93-5ffd058d70f3
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (5f6d94a3-0c90-4897-8d0b-56e984c34381)
 Call ID: 5f6d94a3-0c90-4897-8d0b-56e984c34381
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (f8ee6e74-b97f-4f21-ba3f-163fd4be4429)
 Call ID: f8ee6e74-b97f-4f21-ba3f-163fd4be4429
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMother
    target: Patricia_Knatchbull
  AddTriple (8659c30e-78ef-4637-b401-78017ef56557)
 Call ID: 8659c30e-78ef-4637-b401-78017ef56557
  Args:
    target: John_Knatchbull
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (5ea88a42-a178-4429-bf54-aa5ae1dfe892)
 Call ID: 5ea88a42-a178-4429-bf54-aa5ae1dfe892
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (d4573539-f262-4f6c-a156-33f9294abf3a)
 Call ID: d4573539-f262-4f6c-a156-33f9294abf3a
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (0e143de0-35c0-4c49-b1c0-1e2d467b8ad4)
 Call ID: 0e143de0-35c0-4c49-b1c0-1e2d467b8ad4
  Args:
    relation: :hasFather
    target: Louis_Mountbatten
    source: Patricia_Knatchbull
  AssignClass (cc35da8e-bf79-4446-9dcc-95891c2d8e8e)
 Call ID: cc35da8e-bf79-4446-9dcc-95891c2d8e8e
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (ac4b634c-880c-41ff-bda9-c0a702df439c)
 Call ID: ac4b634c-880c-41ff-bda9-c0a702df439c
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (7d64b1a0-ffe0-48df-8c95-c13f6e0ea757)
 Call ID: 7d64b1a0-ffe0-48df-8c95-c13f6e0ea757
  Args:
    relation: :hasBirthYear
    literal_value: 1953
    source: Penelope_Meredith_Eastwood
    literal_type: xsd:integer
  AddTriple (24c4d0ec-0607-4c2a-8383-f31e07c1a91a)
 Call ID: 24c4d0ec-0607-4c2a-8383-f31e07c1a91a
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
  AddLiteral (f432bf6c-3f8d-491b-a0d3-66bf93b5f906)
 Call ID: f432bf6c-3f8d-491b-a0d3-66bf93b5f906
  Args:
    literal_value: 1979
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (4fa51204-c837-4e92-ba2c-181c2fe53200)
 Call ID: 4fa51204-c837-4e92-ba2c-181c2fe53200
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (bb60f507-16a0-4f54-9f06-1cd56578b8b7)
 Call ID: bb60f507-16a0-4f54-9f06-1cd56578b8b7
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Person
  AddLiteral (8cbc6962-295b-4a55-af3d-c69a8a50b7c3)
 Call ID: 8cbc6962-295b-4a55-af3d-c69a8a50b7c3
  Args:
    literal_value: 1912
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (c800d527-3292-4efa-8ae3-a38956990b2d)
 Call ID: c800d527-3292-4efa-8ae3-a38956990b2d
  Args:
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1980
    relation: :hasDeathYear
  AddTriple (edb1ad30-8afe-488e-aff7-64c6e42dc1be)
 Call ID: edb1ad30-8afe-488e-aff7-64c6e42dc1be
  Args:
    source: Penelope_Meredith_Eastwood
    target: Reginald_Wray_Frank_Eastwood
    relation: :hasFather
  AssignClass (1e715af5-308c-4401-800c-3e22a53e973f)
 Call ID: 1e715af5-308c-4401-800c-3e22a53e973f
  Args:
    source: Marian_Elizabeth_Hood
    type: :Woman
  AssignClass (bbee7f89-5681-4824-8ea7-85049a395ea2)
 Call ID: bbee7f89-5681-4824-8ea7-85049a395ea2
  Args:
    source: Marian_Elizabeth_Hood
    type: :Person
  AddLiteral (4755b4cf-c5f2-4d3f-be82-d45ad7b92c25)
 Call ID: 4755b4cf-c5f2-4d3f-be82-d45ad7b92c25
  Args:
    literal_value: 1926
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Marian_Elizabeth_Hood
  AddLiteral (67109727-913b-4677-9b42-272fab07d27c)
 Call ID: 67109727-913b-4677-9b42-272fab07d27c
  Args:
    relation: :hasDeathYear
    literal_value: 2020
    source: Marian_Elizabeth_Hood
    literal_type: xsd:integer
  AddTriple (3aff4429-8773-4112-9e67-01478c232fd2)
 Call ID: 3aff4429-8773-4112-9e67-01478c232fd2
  Args:
    source: Penelope_Meredith_Eastwood
    target: Marian_Elizabeth_Hood
    relation: :hasMother
  AssignClass (4e58051d-1fb8-436b-8783-d180631a6660)
 Call ID: 4e58051d-1fb8-436b-8783-d180631a6660
  Args:
    source: Nicholas_Knatchbull
    type: :Man
  AssignClass (651ecc50-7ea6-4a5c-b581-919ff21510a7)
 Call ID: 651ecc50-7ea6-4a5c-b581-919ff21510a7
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (60605977-13af-454e-82be-cfe1a86f3b8e)
 Call ID: 60605977-13af-454e-82be-cfe1a86f3b8e
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasBrother
    target: Nicholas_Knatchbull
  AssignClass (e39a2ecf-9b27-418d-9105-f552e44da8c2)
 Call ID: e39a2ecf-9b27-418d-9105-f552e44da8c2
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (1201490b-2b2d-471f-a7c6-9a1d95f30408)
 Call ID: 1201490b-2b2d-471f-a7c6-9a1d95f30408
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddTriple (9d31f192-1a1f-4f29-bb1a-8523a4ad56d5)
 Call ID: 9d31f192-1a1f-4f29-bb1a-8523a4ad56d5
  Args:
    target: Doreen_Knatchbull
    relation: :hasMother
    source: John_Knatchbull
  AssignClass (754513b7-268d-4149-89d1-8c26acf9b2de)
 Call ID: 754513b7-268d-4149-89d1-8c26acf9b2de
  Args:
    type: :Woman
    source: Eugenie_Lady_Nuttall
  AssignClass (a390d11d-3fbc-4cec-860c-2aa825dc78e7)
 Call ID: a390d11d-3fbc-4cec-860c-2aa825dc78e7
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Person
  AddTriple (ca8098e3-a508-4bd3-9cc8-6724e0676e91)
 Call ID: ca8098e3-a508-4bd3-9cc8-6724e0676e91
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Eugenie_Lady_Nuttall
    relation: :hasRelation
  AssignClass (c24ec943-15c0-4021-a1cd-851b76b52f4d)
 Call ID: c24ec943-15c0-4021-a1cd-851b76b52f4d
  Args:
    type: :Man
    source: Edward_Austen_Knight
  AssignClass (18d94f0a-3349-4884-9e10-6019fc8ad370)
 Call ID: 18d94f0a-3349-4884-9e10-6019fc8ad370
  Args:
    source: Edward_Austen_Knight
    type: :Person
  AssignClass (d1498a9c-e5b5-4a8f-9e81-c0f075cb8a7e)
 Call ID: d1498a9c-e5b5-4a8f-9e81-c0f075cb8a7e
  Args:
    type: :Woman
    source: Jane_Austen
  AssignClass (963a2702-d7bc-429b-93d8-2240c6889644)
 Call ID: 963a2702-d7bc-429b-93d8-2240c6889644
  Args:
    source: Jane_Austen
    type: :Person
  AddTriple (e308a3ef-c95d-48d6-b4fb-067d77a40309)
 Call ID: e308a3ef-c95d-48d6-b4fb-067d77a40309
  Args:
    source: Edward_Austen_Knight
    relation: :isBrotherOf
    target: Jane_Austen
  AddTriple (d573c57e-3b8d-4498-a8ac-f7842a9752c5)
 Call ID: d573c57e-3b8d-4498-a8ac-f7842a9752c5
  Args:
    target: Edward_Austen_Knight
    relation: :hasAncestor
    source: John_Knatchbull
  Finish (092ff443-5bce-4b33-9d17-054a3e9eab5b)
 Call ID: 092ff443-5bce-4b33-9d17-054a3e9eab5b
  Args: