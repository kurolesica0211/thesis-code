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
  AssignClass (c1184c38-5fc7-4819-91a5-f231a9056314)
 Call ID: c1184c38-5fc7-4819-91a5-f231a9056314
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (47943b14-5ebb-482f-b3bf-e421945063f0)
 Call ID: 47943b14-5ebb-482f-b3bf-e421945063f0
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (ab725de1-bb48-40d0-9767-7e294771831b)
 Call ID: ab725de1-bb48-40d0-9767-7e294771831b
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1947
  AddLiteral (11f5cc6b-560d-4bd4-a8e2-c4ceb29768f0)
 Call ID: 11f5cc6b-560d-4bd4-a8e2-c4ceb29768f0
  Args:
    relation: :formerlyKnownAs
    literal_value: Lord Romsey
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
  AddLiteral (45eabae6-e10a-4327-89ac-582810c1b0e6)
 Call ID: 45eabae6-e10a-4327-89ac-582810c1b0e6
  Args:
    literal_type: xsd:string
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Brabourne
    relation: :formerlyKnownAs
  AssignClass (eac45ae5-1432-439c-bff7-19fb2f946ebc)
 Call ID: eac45ae5-1432-439c-bff7-19fb2f946ebc
  Args:
    source: Patricia_Knatchbull
    type: :Woman
  AssignClass (45d61b1d-f4ee-4d5b-8656-057c1fe6551f)
 Call ID: 45d61b1d-f4ee-4d5b-8656-057c1fe6551f
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (046ff224-a31c-4337-ac00-95ed62f1f0bf)
 Call ID: 046ff224-a31c-4337-ac00-95ed62f1f0bf
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (c422c8b5-ced2-4271-85a9-3e77297cfb78)
 Call ID: c422c8b5-ced2-4271-85a9-3e77297cfb78
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (b2d7cdb4-09e8-4873-bfd9-fa58108b85d2)
 Call ID: b2d7cdb4-09e8-4873-bfd9-fa58108b85d2
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
    relation: :hasFather
  AddTriple (a2a75232-a825-42e7-a9f4-6e178ff8967a)
 Call ID: a2a75232-a825-42e7-a9f4-6e178ff8967a
  Args:
    relation: :hasMother
    target: Patricia_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (df419d03-b6a0-41f2-8433-d49861b067d0)
 Call ID: df419d03-b6a0-41f2-8433-d49861b067d0
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (08ff278a-d3f0-486a-a1ef-48e93d1cc1da)
 Call ID: 08ff278a-d3f0-486a-a1ef-48e93d1cc1da
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Person
  AddLiteral (0d27a211-e12f-408e-bdcb-d01313667d1b)
 Call ID: 0d27a211-e12f-408e-bdcb-d01313667d1b
  Args:
    literal_type: xsd:integer
    source: Penelope_Meredith_Eastwood
    literal_value: 1953
    relation: :hasBirthYear
  AddLiteral (f8f05726-0a34-481d-963e-11d257b08dd2)
 Call ID: f8f05726-0a34-481d-963e-11d257b08dd2
  Args:
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
    relation: :hasMarriageYear
  AddTriple (9d1533c7-a41a-4a0f-94b7-be3eed77236a)
 Call ID: 9d1533c7-a41a-4a0f-94b7-be3eed77236a
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
  AssignClass (9aef1488-cfa1-4282-956d-3ba1cfd8c4ed)
 Call ID: 9aef1488-cfa1-4282-956d-3ba1cfd8c4ed
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (7acd2f9d-5b3f-4134-a65f-bbc01634a7b9)
 Call ID: 7acd2f9d-5b3f-4134-a65f-bbc01634a7b9
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (427d87ec-fc97-43b1-b0be-27b7fe92be9f)
 Call ID: 427d87ec-fc97-43b1-b0be-27b7fe92be9f
  Args:
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1912
    relation: :hasBirthYear
  AddLiteral (8c7015b2-3886-4b81-9a47-2a4c402fbd13)
 Call ID: 8c7015b2-3886-4b81-9a47-2a4c402fbd13
  Args:
    literal_value: 1980
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (4e4f958e-29ef-4241-9004-1765db2194d8)
 Call ID: 4e4f958e-29ef-4241-9004-1765db2194d8
  Args:
    source: Marian_Elizabeth
    type: :Woman
  AssignClass (458951fa-cabe-4534-ad2d-559a112db90f)
 Call ID: 458951fa-cabe-4534-ad2d-559a112db90f
  Args:
    type: :Person
    source: Marian_Elizabeth
  AddLiteral (542a6794-26a5-41cb-88cc-72a88b83eeac)
 Call ID: 542a6794-26a5-41cb-88cc-72a88b83eeac
  Args:
    relation: :hasBirthYear
    literal_value: 1926
    source: Marian_Elizabeth
    literal_type: xsd:integer
  AddLiteral (d249408b-de7e-40a4-9eb9-48afa6d8e210)
 Call ID: d249408b-de7e-40a4-9eb9-48afa6d8e210
  Args:
    relation: :hasDeathYear
    literal_value: 2020
    source: Marian_Elizabeth
    literal_type: xsd:integer
  AddTriple (4fa1b760-316c-4a46-bbd9-c4759217968b)
 Call ID: 4fa1b760-316c-4a46-bbd9-c4759217968b
  Args:
    target: Reginald_Wray_Frank_Eastwood
    source: Penelope_Meredith_Eastwood
    relation: :hasFather
  AddTriple (fcf0f405-6d0f-43d1-b33b-491e46bfbd7d)
 Call ID: fcf0f405-6d0f-43d1-b33b-491e46bfbd7d
  Args:
    source: Penelope_Meredith_Eastwood
    target: Marian_Elizabeth
    relation: :hasMother
  AssignClass (65149f23-5276-41d8-9d24-ea60b1bfd9b6)
 Call ID: 65149f23-5276-41d8-9d24-ea60b1bfd9b6
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (1ddaf52f-87d3-4be0-874f-733110d71512)
 Call ID: 1ddaf52f-87d3-4be0-874f-733110d71512
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddLiteral (75bdf061-7552-43ec-aaee-46995556361e)
 Call ID: 75bdf061-7552-43ec-aaee-46995556361e
  Args:
    literal_value: 1979
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Louis_Mountbatten
  AssignClass (1a9a7fe5-9e2c-4cfa-9ce9-05e11b711702)
 Call ID: 1a9a7fe5-9e2c-4cfa-9ce9-05e11b711702
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (9fa8041d-a521-4aa6-8ee5-d14045efa0d3)
 Call ID: 9fa8041d-a521-4aa6-8ee5-d14045efa0d3
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddLiteral (967ba3c8-419f-438c-b7f1-03be9816dfff)
 Call ID: 967ba3c8-419f-438c-b7f1-03be9816dfff
  Args:
    source: Nicholas_Knatchbull
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1979
  AssignClass (40ff4c4d-c35a-451f-8fc2-597b55d2bea5)
 Call ID: 40ff4c4d-c35a-451f-8fc2-597b55d2bea5
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (c3136051-3e3c-40cd-89dc-b1159e06fa59)
 Call ID: c3136051-3e3c-40cd-89dc-b1159e06fa59
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddLiteral (e66f258b-b295-45cf-af63-9bac41a09274)
 Call ID: e66f258b-b295-45cf-af63-9bac41a09274
  Args:
    relation: :hasDeathYear
    literal_value: 1979
    source: Doreen_Knatchbull
    literal_type: xsd:integer
  AddTriple (acf82b11-6218-4e03-85ba-5b3cd66414d2)
 Call ID: acf82b11-6218-4e03-85ba-5b3cd66414d2
  Args:
    relation: :hasBrother
    source: Norton_Louis_Philip_Knatchbull
    target: Nicholas_Knatchbull
  AddTriple (7d45e70a-33de-4dca-9ad3-c306d1ff180f)
 Call ID: 7d45e70a-33de-4dca-9ad3-c306d1ff180f
  Args:
    relation: :hasFather
    source: Nicholas_Knatchbull
    target: John_Knatchbull
  AddTriple (23b83ca8-d855-45c5-970a-b95605a201df)
 Call ID: 23b83ca8-d855-45c5-970a-b95605a201df
  Args:
    target: Patricia_Knatchbull
    source: Nicholas_Knatchbull
    relation: :hasMother
  AddTriple (4e00c354-18f7-46ed-8f33-c20730a8ae6e)
 Call ID: 4e00c354-18f7-46ed-8f33-c20730a8ae6e
  Args:
    target: Doreen_Knatchbull
    source: Patricia_Knatchbull
    relation: :hasMother
  AssignClass (a15473a7-7594-4ba2-8a5e-63d7bd8818f3)
 Call ID: a15473a7-7594-4ba2-8a5e-63d7bd8818f3
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Woman
  AssignClass (70a9138d-aa3a-45bd-887c-719d0544b563)
 Call ID: 70a9138d-aa3a-45bd-887c-719d0544b563
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Person
  AddTriple (5c868f49-8054-4d8a-8364-12d19b1f28bd)
 Call ID: 5c868f49-8054-4d8a-8364-12d19b1f28bd
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Eugenie_Lady_Nuttall
    relation: :hasRelation
  Finish (be5bfc3e-c6e4-41d8-80b7-9c047d1f1cbd)
 Call ID: be5bfc3e-c6e4-41d8-80b7-9c047d1f1cbd
  Args: