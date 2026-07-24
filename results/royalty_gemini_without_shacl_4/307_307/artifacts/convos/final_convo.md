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
  AssignClass (bae018b9-c00f-4cb4-b024-40df654222ec)
 Call ID: bae018b9-c00f-4cb4-b024-40df654222ec
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (b1887296-f5f4-41c4-a2e6-02f66b85c1a0)
 Call ID: b1887296-f5f4-41c4-a2e6-02f66b85c1a0
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (fe95eeab-d998-4a6e-b2ae-6085de1f7591)
 Call ID: fe95eeab-d998-4a6e-b2ae-6085de1f7591
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1947
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (1847d189-6522-47b6-96a4-5b3260879f0e)
 Call ID: 1847d189-6522-47b6-96a4-5b3260879f0e
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Romsey
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AddLiteral (4b2443bf-eba4-49cc-8a10-9214b7f75fa1)
 Call ID: 4b2443bf-eba4-49cc-8a10-9214b7f75fa1
  Args:
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Lord Brabourne
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (6d154b64-5eb6-447d-bef4-e8d72934c0ce)
 Call ID: 6d154b64-5eb6-447d-bef4-e8d72934c0ce
  Args:
    source: Patricia_Knatchbull
    type: :Woman
  AssignClass (bf99ffa9-19d3-4932-b1c9-1bf3e42dd745)
 Call ID: bf99ffa9-19d3-4932-b1c9-1bf3e42dd745
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (b1a4c82a-cce9-48e3-881a-8fde0e45e7bf)
 Call ID: b1a4c82a-cce9-48e3-881a-8fde0e45e7bf
  Args:
    source: John_Knatchbull
    type: :Man
  AssignClass (00b0ffdf-95d1-4d06-bae1-0ab3804f1745)
 Call ID: 00b0ffdf-95d1-4d06-bae1-0ab3804f1745
  Args:
    source: John_Knatchbull
    type: :Person
  AddTriple (dd284b06-1658-4a54-87ec-a3a1c35edf74)
 Call ID: dd284b06-1658-4a54-87ec-a3a1c35edf74
  Args:
    relation: :hasFather
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
  AddTriple (d2a5cc1f-ea44-4d22-8cd7-cb06fb06dcc0)
 Call ID: d2a5cc1f-ea44-4d22-8cd7-cb06fb06dcc0
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Knatchbull
    relation: :hasMother
  AssignClass (56acc872-822d-4576-9a4e-af00df9c85cb)
 Call ID: 56acc872-822d-4576-9a4e-af00df9c85cb
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (e1304bd2-8cd1-4913-9bc8-d7440e3feae8)
 Call ID: e1304bd2-8cd1-4913-9bc8-d7440e3feae8
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (6f76054c-4f2c-475f-9acf-dee27cda2c01)
 Call ID: 6f76054c-4f2c-475f-9acf-dee27cda2c01
  Args:
    target: Louis_Mountbatten
    source: Patricia_Knatchbull
    relation: :hasFather
  AssignClass (6184a072-56cd-405c-baa4-a01cbfbe5189)
 Call ID: 6184a072-56cd-405c-baa4-a01cbfbe5189
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Woman
  AssignClass (2f3281c8-ba44-468c-8074-b5d9fef46d2d)
 Call ID: 2f3281c8-ba44-468c-8074-b5d9fef46d2d
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (fc9aaa93-fec7-470d-974e-f4cd54a00eaa)
 Call ID: fc9aaa93-fec7-470d-974e-f4cd54a00eaa
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1953
    source: Penelope_Meredith_Eastwood
  AddTriple (4df6608a-83d4-481d-886e-979bcb0c863a)
 Call ID: 4df6608a-83d4-481d-886e-979bcb0c863a
  Args:
    relation: :hasRelation
    target: Penelope_Meredith_Eastwood
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (723d3a0c-9337-4105-ac68-b687a272a345)
 Call ID: 723d3a0c-9337-4105-ac68-b687a272a345
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
  AssignClass (4a0927a4-c4de-4727-9d8b-0080c2de9563)
 Call ID: 4a0927a4-c4de-4727-9d8b-0080c2de9563
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (c78db152-53ed-4b40-a789-5d13641cec77)
 Call ID: c78db152-53ed-4b40-a789-5d13641cec77
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Person
  AddLiteral (b6b99b15-d83f-4997-bd1b-f0e48883be47)
 Call ID: b6b99b15-d83f-4997-bd1b-f0e48883be47
  Args:
    literal_value: 1912
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (f9dcf855-c7fd-4316-b8e0-78c9dee3805e)
 Call ID: f9dcf855-c7fd-4316-b8e0-78c9dee3805e
  Args:
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1980
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (b359fcb1-e7df-4a62-aa17-294f13a36dca)
 Call ID: b359fcb1-e7df-4a62-aa17-294f13a36dca
  Args:
    type: :Woman
    source: Marian_Elizabeth_Hood
  AssignClass (14c0bcc5-3bb0-4cb9-9d65-56f99bd4ceb0)
 Call ID: 14c0bcc5-3bb0-4cb9-9d65-56f99bd4ceb0
  Args:
    type: :Person
    source: Marian_Elizabeth_Hood
  AddLiteral (c0f80057-52a2-487f-897b-2e7eab4dda5c)
 Call ID: c0f80057-52a2-487f-897b-2e7eab4dda5c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1926
    source: Marian_Elizabeth_Hood
  AddLiteral (ecaaf243-76fd-4ffe-a11d-cd48045d1d60)
 Call ID: ecaaf243-76fd-4ffe-a11d-cd48045d1d60
  Args:
    literal_value: 2020
    source: Marian_Elizabeth_Hood
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (293f7035-b488-4523-a51c-33e9fef60e12)
 Call ID: 293f7035-b488-4523-a51c-33e9fef60e12
  Args:
    relation: :hasFather
    target: Reginald_Wray_Frank_Eastwood
    source: Penelope_Meredith_Eastwood
  AddTriple (f349a2b5-5250-428f-9799-2bdf30d299e3)
 Call ID: f349a2b5-5250-428f-9799-2bdf30d299e3
  Args:
    relation: :hasMother
    source: Penelope_Meredith_Eastwood
    target: Marian_Elizabeth_Hood
  AssignClass (3363c250-6cd9-438e-bd99-a8d82ea85d88)
 Call ID: 3363c250-6cd9-438e-bd99-a8d82ea85d88
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (6b654064-c8c5-495f-96ce-19632aa61e27)
 Call ID: 6b654064-c8c5-495f-96ce-19632aa61e27
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AddTriple (c553ceb1-9fd7-4553-9b9c-9aa761641b30)
 Call ID: c553ceb1-9fd7-4553-9b9c-9aa761641b30
  Args:
    relation: :hasBrother
    source: Norton_Louis_Philip_Knatchbull
    target: Nicholas_Knatchbull
  AssignClass (e09ffb23-e3ed-4724-8d83-a80175fc6ce9)
 Call ID: e09ffb23-e3ed-4724-8d83-a80175fc6ce9
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (76ff29b0-946e-48a5-9c2f-f178ade06751)
 Call ID: 76ff29b0-946e-48a5-9c2f-f178ade06751
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddLiteral (29dbd885-518f-4a8a-9857-a925b12669a9)
 Call ID: 29dbd885-518f-4a8a-9857-a925b12669a9
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Doreen_Knatchbull
    literal_value: 1983
  AddTriple (34736f2e-cade-48fe-8617-a63c5ba4ccac)
 Call ID: 34736f2e-cade-48fe-8617-a63c5ba4ccac
  Args:
    target: Doreen_Knatchbull
    source: John_Knatchbull
    relation: :hasMother
  AssignClass (131518ff-fa73-46c9-8f41-df79f187429b)
 Call ID: 131518ff-fa73-46c9-8f41-df79f187429b
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Woman
  AssignClass (781cab0d-61d3-44ac-98e2-1708cf0fcced)
 Call ID: 781cab0d-61d3-44ac-98e2-1708cf0fcced
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (33ff1316-a97a-4825-a207-39e60ffef0c7)
 Call ID: 33ff1316-a97a-4825-a207-39e60ffef0c7
  Args:
    target: Eugenie_Lady_Nuttall
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
  Finish (b949947a-09af-4be5-b6d0-5058aed39be0)
 Call ID: b949947a-09af-4be5-b6d0-5058aed39be0
  Args: