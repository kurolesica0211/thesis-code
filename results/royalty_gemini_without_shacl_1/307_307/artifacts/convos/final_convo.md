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
  AssignClass (caae9713-5785-4cf6-b877-572375b643a3)
 Call ID: caae9713-5785-4cf6-b877-572375b643a3
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (cdfaec6b-f10e-497a-9f11-e4d7201432b2)
 Call ID: cdfaec6b-f10e-497a-9f11-e4d7201432b2
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (a82736f2-6fb2-4765-9561-823ae325a1c6)
 Call ID: a82736f2-6fb2-4765-9561-823ae325a1c6
  Args:
    relation: :hasBirthYear
    literal_value: 1947
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (e9e246ba-81a3-4912-b31b-c006c5e7a7c7)
 Call ID: e9e246ba-81a3-4912-b31b-c006c5e7a7c7
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Lord Romsey
  AddLiteral (59ae8881-379b-4710-ba1b-d5b75ca49558)
 Call ID: 59ae8881-379b-4710-ba1b-d5b75ca49558
  Args:
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Lord Brabourne
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (de6c28d4-9d2f-46e8-8478-c7934fa1033f)
 Call ID: de6c28d4-9d2f-46e8-8478-c7934fa1033f
  Args:
    source: Patricia_Knatchbull
    type: :Woman
  AssignClass (95861cb8-00de-47bd-9c3a-418a4e97db68)
 Call ID: 95861cb8-00de-47bd-9c3a-418a4e97db68
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (c68e9be3-7583-4a2a-a768-cb5c0c95ed93)
 Call ID: c68e9be3-7583-4a2a-a768-cb5c0c95ed93
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (1d9fdf25-8f8f-4ef4-a8b4-c29e00eae2bd)
 Call ID: 1d9fdf25-8f8f-4ef4-a8b4-c29e00eae2bd
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (4eaabc6d-0c34-41a8-9786-6d81cd864520)
 Call ID: 4eaabc6d-0c34-41a8-9786-6d81cd864520
  Args:
    relation: :hasMother
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Knatchbull
  AddTriple (814537ad-989f-432d-b9ad-12e1b6d798e1)
 Call ID: 814537ad-989f-432d-b9ad-12e1b6d798e1
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
    relation: :hasFather
  AddLiteral (d8d05802-69ef-46ef-b964-06755537cade)
 Call ID: d8d05802-69ef-46ef-b964-06755537cade
  Args:
    source: Patricia_Knatchbull
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (e9a6ced5-c4d5-4fae-ad77-c7c375c9dcbe)
 Call ID: e9a6ced5-c4d5-4fae-ad77-c7c375c9dcbe
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (68f0da90-bf4b-467c-9690-fbe8bc4b414b)
 Call ID: 68f0da90-bf4b-467c-9690-fbe8bc4b414b
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (e95bf1af-4ecf-4ee6-908b-c6d46088a817)
 Call ID: e95bf1af-4ecf-4ee6-908b-c6d46088a817
  Args:
    relation: :hasFather
    target: Louis_Mountbatten
    source: Patricia_Knatchbull
  AssignClass (e86ce254-7f31-490b-bee0-c8465d698758)
 Call ID: e86ce254-7f31-490b-bee0-c8465d698758
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (5c0994c4-7aaf-4a32-a0bf-98d0dcbabb6f)
 Call ID: 5c0994c4-7aaf-4a32-a0bf-98d0dcbabb6f
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Person
  AddLiteral (4e73ca1a-dd04-43d4-bce0-fc02c9d3e38a)
 Call ID: 4e73ca1a-dd04-43d4-bce0-fc02c9d3e38a
  Args:
    source: Penelope_Meredith_Eastwood
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1953
  AddTriple (fdbb50a3-9b69-4ace-b52d-a10b7341a551)
 Call ID: fdbb50a3-9b69-4ace-b52d-a10b7341a551
  Args:
    relation: :hasRelation
    target: Penelope_Meredith_Eastwood
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (3b6ff87a-5333-4d8d-a883-932b19c4f317)
 Call ID: 3b6ff87a-5333-4d8d-a883-932b19c4f317
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (397a84c9-7afb-433c-9001-442143efcf19)
 Call ID: 397a84c9-7afb-433c-9001-442143efcf19
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Man
  AssignClass (fd7304d6-bb72-4a47-b13a-cbc6f619e959)
 Call ID: fd7304d6-bb72-4a47-b13a-cbc6f619e959
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Person
  AddLiteral (7c6ba3bb-4266-490f-8533-616759e86b51)
 Call ID: 7c6ba3bb-4266-490f-8533-616759e86b51
  Args:
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1912
  AddLiteral (0dbbafa6-4b89-4589-a1e4-3dbb13344fa6)
 Call ID: 0dbbafa6-4b89-4589-a1e4-3dbb13344fa6
  Args:
    literal_type: xsd:integer
    literal_value: 1980
    relation: :hasDeathYear
    source: Reginald_Wray_Frank_Eastwood
  AddTriple (a6ada60a-b021-4f1f-9fd9-0cf84402e781)
 Call ID: a6ada60a-b021-4f1f-9fd9-0cf84402e781
  Args:
    target: Reginald_Wray_Frank_Eastwood
    source: Penelope_Meredith_Eastwood
    relation: :hasFather
  AssignClass (22a0cac2-d8bd-47d8-b460-80749fe39ee6)
 Call ID: 22a0cac2-d8bd-47d8-b460-80749fe39ee6
  Args:
    type: :Woman
    source: Marian_Elizabeth_Hood
  AssignClass (d2852723-f475-4645-9574-ae889f7dc856)
 Call ID: d2852723-f475-4645-9574-ae889f7dc856
  Args:
    source: Marian_Elizabeth_Hood
    type: :Person
  AddLiteral (c05ffd0c-f125-4809-bb6f-471044fb67e1)
 Call ID: c05ffd0c-f125-4809-bb6f-471044fb67e1
  Args:
    literal_type: xsd:integer
    literal_value: 1926
    relation: :hasBirthYear
    source: Marian_Elizabeth_Hood
  AddLiteral (940a3eb8-1af2-4b9b-8684-5359a00bf0a6)
 Call ID: 940a3eb8-1af2-4b9b-8684-5359a00bf0a6
  Args:
    source: Marian_Elizabeth_Hood
    literal_type: xsd:integer
    literal_value: 2020
    relation: :hasDeathYear
  AddTriple (b6e1f19f-e403-4195-99b5-1183f0e369e7)
 Call ID: b6e1f19f-e403-4195-99b5-1183f0e369e7
  Args:
    relation: :hasMother
    target: Marian_Elizabeth_Hood
    source: Penelope_Meredith_Eastwood
  AssignClass (0e238173-eaf2-4378-8726-9433d1dcf23f)
 Call ID: 0e238173-eaf2-4378-8726-9433d1dcf23f
  Args:
    source: Nicholas_Knatchbull
    type: :Man
  AssignClass (032a8745-113b-4fdc-80e5-31770d570df3)
 Call ID: 032a8745-113b-4fdc-80e5-31770d570df3
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AddTriple (353009b3-1c88-4c96-9b63-3ec1ba3623c1)
 Call ID: 353009b3-1c88-4c96-9b63-3ec1ba3623c1
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Nicholas_Knatchbull
    relation: :hasBrother
  AssignClass (45bfd5f2-f927-4cdc-a60a-7647178ab91c)
 Call ID: 45bfd5f2-f927-4cdc-a60a-7647178ab91c
  Args:
    source: Doreen_Knatchbull
    type: :Woman
  AssignClass (24f98795-5406-49e1-9488-053bf19be276)
 Call ID: 24f98795-5406-49e1-9488-053bf19be276
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddTriple (6e024e62-4849-4ba1-b9f2-20a05493c387)
 Call ID: 6e024e62-4849-4ba1-b9f2-20a05493c387
  Args:
    relation: :hasMother
    target: Doreen_Knatchbull
    source: John_Knatchbull
  AssignClass (bc2bbc29-6dd7-4d6d-8e5f-1f4c9003392f)
 Call ID: bc2bbc29-6dd7-4d6d-8e5f-1f4c9003392f
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Woman
  AssignClass (c7af874f-3083-46a1-88c6-519b80c0a56a)
 Call ID: c7af874f-3083-46a1-88c6-519b80c0a56a
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Person
  AddTriple (7797f1fe-aa4d-48e5-a0e8-faa7abbd79cf)
 Call ID: 7797f1fe-aa4d-48e5-a0e8-faa7abbd79cf
  Args:
    relation: :hasRelation
    target: Eugenie_Lady_Nuttall
    source: Norton_Louis_Philip_Knatchbull
  Finish (20943442-d124-4a70-b9d6-85f10a3e7e1c)
 Call ID: 20943442-d124-4a70-b9d6-85f10a3e7e1c
  Args: