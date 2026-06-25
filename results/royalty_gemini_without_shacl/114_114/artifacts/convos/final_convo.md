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
  AssignClass (c5e3edb0-50b0-4271-8d58-2249b1284deb)
 Call ID: c5e3edb0-50b0-4271-8d58-2249b1284deb
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (7ddac812-2bdf-4807-9831-2c5854a01a1b)
 Call ID: 7ddac812-2bdf-4807-9831-2c5854a01a1b
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Person
  AddLiteral (8fa45bdc-544b-4f1e-86ba-551562020cd2)
 Call ID: 8fa45bdc-544b-4f1e-86ba-551562020cd2
  Args:
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1947
    relation: :hasBirthYear
  AddLiteral (530e1e98-766b-474e-bf1c-ae70dc906ae7)
 Call ID: 530e1e98-766b-474e-bf1c-ae70dc906ae7
  Args:
    relation: :formerlyKnownAs
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
    literal_value: Lord Romsey
  AddLiteral (5c3e16b6-26bb-4112-9e9b-cc4907d561b8)
 Call ID: 5c3e16b6-26bb-4112-9e9b-cc4907d561b8
  Args:
    relation: :formerlyKnownAs
    literal_value: Lord Brabourne
    literal_type: xsd:string
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (e0f2f15c-9c58-4700-a982-ea983a7731bc)
 Call ID: e0f2f15c-9c58-4700-a982-ea983a7731bc
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (103e23ef-205e-4a32-91fb-a9fa552391b7)
 Call ID: 103e23ef-205e-4a32-91fb-a9fa552391b7
  Args:
    source: Patricia_Knatchbull
    type: :Person
  AssignClass (a8a4b54b-3399-4a8f-b6cb-24774c5b9755)
 Call ID: a8a4b54b-3399-4a8f-b6cb-24774c5b9755
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (785483dc-80dd-47f9-bacd-7a83ef66e315)
 Call ID: 785483dc-80dd-47f9-bacd-7a83ef66e315
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (f9535c12-b71e-44c3-9b3f-2ecf3ccd549e)
 Call ID: f9535c12-b71e-44c3-9b3f-2ecf3ccd549e
  Args:
    relation: :hasMother
    target: Patricia_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (cd399cd3-cbec-411b-a1ec-d301860e63bd)
 Call ID: cd399cd3-cbec-411b-a1ec-d301860e63bd
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasFather
    target: John_Knatchbull
  AddLiteral (35e93128-bafe-4d4d-ba06-edd97fcdabf9)
 Call ID: 35e93128-bafe-4d4d-ba06-edd97fcdabf9
  Args:
    source: John_Knatchbull
    literal_type: xsd:integer
    literal_value: 2005
    relation: :hasDeathYear
  AddLiteral (d759e185-4aee-499b-8e75-4de18507f69b)
 Call ID: d759e185-4aee-499b-8e75-4de18507f69b
  Args:
    relation: :hasDeathYear
    source: Patricia_Knatchbull
    literal_type: xsd:integer
    literal_value: 2017
  AssignClass (5c067313-204d-4986-a5e7-3da5cf117c4c)
 Call ID: 5c067313-204d-4986-a5e7-3da5cf117c4c
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (bdf02bdb-5c08-4b75-af8f-8f000f9d12da)
 Call ID: bdf02bdb-5c08-4b75-af8f-8f000f9d12da
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (fb030c9d-38f4-4922-be06-b8e684643012)
 Call ID: fb030c9d-38f4-4922-be06-b8e684643012
  Args:
    relation: :hasFather
    target: Louis_Mountbatten
    source: Patricia_Knatchbull
  AssignClass (6cc7cd7e-b5b7-4dca-92f0-d05ae9cb55ef)
 Call ID: 6cc7cd7e-b5b7-4dca-92f0-d05ae9cb55ef
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (33970805-348f-4b3c-a0f2-6254ff11a3c2)
 Call ID: 33970805-348f-4b3c-a0f2-6254ff11a3c2
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (3ba1351a-b9e9-4bee-92a0-294fb2a68e4e)
 Call ID: 3ba1351a-b9e9-4bee-92a0-294fb2a68e4e
  Args:
    relation: :isSiblingOf
    target: Nicholas_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (491e1f33-8535-4ecd-a0eb-371ce73a3368)
 Call ID: 491e1f33-8535-4ecd-a0eb-371ce73a3368
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (d759fd50-40fe-432e-b682-9e41e750ba5e)
 Call ID: d759fd50-40fe-432e-b682-9e41e750ba5e
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AssignClass (fab896c5-437d-4b80-abf1-64ff107f9388)
 Call ID: fab896c5-437d-4b80-abf1-64ff107f9388
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (ca62907b-badf-477f-a0ad-ea653cb52226)
 Call ID: ca62907b-badf-477f-a0ad-ea653cb52226
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (69bc873b-0906-437c-b0b9-5223e60400f9)
 Call ID: 69bc873b-0906-437c-b0b9-5223e60400f9
  Args:
    literal_type: xsd:integer
    source: Penelope_Meredith_Eastwood
    literal_value: 1953
    relation: :hasBirthYear
  AddTriple (8f588bd0-1afa-4e91-8b5d-0784b9163505)
 Call ID: 8f588bd0-1afa-4e91-8b5d-0784b9163505
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
    target: Penelope_Meredith_Eastwood
  AddLiteral (336d5b58-0d96-4a01-968e-50eb23e39b40)
 Call ID: 336d5b58-0d96-4a01-968e-50eb23e39b40
  Args:
    literal_value: 1979
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMarriageYear
  AssignClass (167923e5-f11a-48e8-b3d8-7f20f8494f95)
 Call ID: 167923e5-f11a-48e8-b3d8-7f20f8494f95
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (53f25f85-8fe7-4774-ab98-678ed2b8f6cc)
 Call ID: 53f25f85-8fe7-4774-ab98-678ed2b8f6cc
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (dc42d6e4-cfa9-4739-b1da-d055e199274f)
 Call ID: dc42d6e4-cfa9-4739-b1da-d055e199274f
  Args:
    literal_value: 1912
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
    relation: :hasBirthYear
  AddLiteral (a1aa28d1-3dc4-4733-8144-e2de42fc39fb)
 Call ID: a1aa28d1-3dc4-4733-8144-e2de42fc39fb
  Args:
    relation: :hasDeathYear
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
    literal_value: 1980
  AssignClass (fc274146-ad6f-4355-9a3b-c9faf9fe6921)
 Call ID: fc274146-ad6f-4355-9a3b-c9faf9fe6921
  Args:
    source: Marian_Elizabeth
    type: :Woman
  AssignClass (9341d322-f02c-4a97-bd04-2d036b16f29c)
 Call ID: 9341d322-f02c-4a97-bd04-2d036b16f29c
  Args:
    source: Marian_Elizabeth
    type: :Person
  AddLiteral (6173ffd5-adad-486c-9224-36792ec37f63)
 Call ID: 6173ffd5-adad-486c-9224-36792ec37f63
  Args:
    source: Marian_Elizabeth
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasBirthYear
  AddLiteral (2f53e5f5-a5c6-4bd7-990a-29d30b25fc3d)
 Call ID: 2f53e5f5-a5c6-4bd7-990a-29d30b25fc3d
  Args:
    literal_value: 2020
    literal_type: xsd:integer
    source: Marian_Elizabeth
    relation: :hasDeathYear
  AddTriple (9de74edb-3165-4b64-85ce-7251476c6f89)
 Call ID: 9de74edb-3165-4b64-85ce-7251476c6f89
  Args:
    source: Penelope_Meredith_Eastwood
    relation: :hasFather
    target: Reginald_Wray_Frank_Eastwood
  AddTriple (20cbad7e-5a2f-4a6f-9fcd-a2abcf9001a8)
 Call ID: 20cbad7e-5a2f-4a6f-9fcd-a2abcf9001a8
  Args:
    target: Marian_Elizabeth
    relation: :hasMother
    source: Penelope_Meredith_Eastwood
  AssignClass (5718a0dd-2332-4528-af2e-341df6db8556)
 Call ID: 5718a0dd-2332-4528-af2e-341df6db8556
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Woman
  AssignClass (a5792f3a-cb39-40e9-8c98-6c76891aaf43)
 Call ID: a5792f3a-cb39-40e9-8c98-6c76891aaf43
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (fffa41dc-de09-49ad-bf79-20a7635da469)
 Call ID: fffa41dc-de09-49ad-bf79-20a7635da469
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
    target: Eugenie_Lady_Nuttall
  Finish (b95918c3-4e6a-4d0e-89b1-2a7e3a392c3d)
 Call ID: b95918c3-4e6a-4d0e-89b1-2a7e3a392c3d
  Args: