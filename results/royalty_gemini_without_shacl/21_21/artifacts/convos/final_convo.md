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
  AssignClass (85269f66-2e21-4606-af7c-96ca4f17b8c9)
 Call ID: 85269f66-2e21-4606-af7c-96ca4f17b8c9
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Man
  AssignClass (cbac113b-c9d5-414b-8542-47935900b80b)
 Call ID: cbac113b-c9d5-414b-8542-47935900b80b
  Args:
    source: Norton_Louis_Philip_Knatchbull
    type: :Person
  AddLiteral (86ed26a8-d0e3-4c1a-882a-4c92919b1de2)
 Call ID: 86ed26a8-d0e3-4c1a-882a-4c92919b1de2
  Args:
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasBirthYear
    literal_value: 1947
  AddLiteral (396050ed-2b3b-412c-8edd-bc7d840994ff)
 Call ID: 396050ed-2b3b-412c-8edd-bc7d840994ff
  Args:
    literal_value: Lord Romsey
    source: Norton_Louis_Philip_Knatchbull
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AddLiteral (a4457292-4dd5-42d2-9d69-82b2af81b5ee)
 Call ID: a4457292-4dd5-42d2-9d69-82b2af81b5ee
  Args:
    relation: :formerlyKnownAs
    source: Norton_Louis_Philip_Knatchbull
    literal_value: Lord Brabourne
    literal_type: xsd:string
  AssignClass (2743c636-6caf-4a71-890f-3855f52b993f)
 Call ID: 2743c636-6caf-4a71-890f-3855f52b993f
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (9bf428ed-62ae-4775-9916-90436424d586)
 Call ID: 9bf428ed-62ae-4775-9916-90436424d586
  Args:
    source: Patricia_Knatchbull
    type: :Person
  AssignClass (2649b411-50f1-4a18-8269-83928b5cbd87)
 Call ID: 2649b411-50f1-4a18-8269-83928b5cbd87
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (7f838426-dbd1-45dc-a392-7a73ce9c2846)
 Call ID: 7f838426-dbd1-45dc-a392-7a73ce9c2846
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (57168284-f062-4848-982e-f551a53f2465)
 Call ID: 57168284-f062-4848-982e-f551a53f2465
  Args:
    target: Patricia_Knatchbull
    relation: :hasMother
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (5fcbc2b4-31b7-4beb-bde0-854e61eb5dc7)
 Call ID: 5fcbc2b4-31b7-4beb-bde0-854e61eb5dc7
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
    relation: :hasFather
  AddLiteral (c41776ed-d90e-405a-bb49-f876bc663cf9)
 Call ID: c41776ed-d90e-405a-bb49-f876bc663cf9
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: John_Knatchbull
    literal_value: 2005
  AddLiteral (85a7ebe3-09fc-43f7-9e94-ea1b38c89919)
 Call ID: 85a7ebe3-09fc-43f7-9e94-ea1b38c89919
  Args:
    source: Patricia_Knatchbull
    relation: :hasDeathYear
    literal_value: 2017
    literal_type: xsd:integer
  AssignClass (d2959a26-729e-44a0-858b-d5689ce5a1ad)
 Call ID: d2959a26-729e-44a0-858b-d5689ce5a1ad
  Args:
    source: Louis_Mountbatten
    type: :Man
  AssignClass (8e8400ba-6d2e-4dcf-b5e3-06fbaff3c56b)
 Call ID: 8e8400ba-6d2e-4dcf-b5e3-06fbaff3c56b
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (54815bc7-77ee-4ee6-a8f4-54c122bfc7ed)
 Call ID: 54815bc7-77ee-4ee6-a8f4-54c122bfc7ed
  Args:
    target: Louis_Mountbatten
    relation: :hasFather
    source: Patricia_Knatchbull
  AssignClass (e65956a8-22dc-4647-bda1-54538d9424d5)
 Call ID: e65956a8-22dc-4647-bda1-54538d9424d5
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (fe18ac03-9ff4-473b-be73-7269063e59f4)
 Call ID: fe18ac03-9ff4-473b-be73-7269063e59f4
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (c2161399-fdc1-400f-b755-3c5d30a37065)
 Call ID: c2161399-fdc1-400f-b755-3c5d30a37065
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasBrother
    target: Nicholas_Knatchbull
  AssignClass (3c309814-5a17-48c2-b574-80faf6653c91)
 Call ID: 3c309814-5a17-48c2-b574-80faf6653c91
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (97f9d540-f9ca-4854-a213-45f5c10f8385)
 Call ID: 97f9d540-f9ca-4854-a213-45f5c10f8385
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddTriple (081471d3-2fc8-47d4-88fb-40464a973a49)
 Call ID: 081471d3-2fc8-47d4-88fb-40464a973a49
  Args:
    target: Doreen_Knatchbull
    relation: :hasMother
    source: John_Knatchbull
  AssignClass (6284907f-b172-49fd-a35b-71986f88a736)
 Call ID: 6284907f-b172-49fd-a35b-71986f88a736
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Woman
  AssignClass (598878a0-33cc-41e6-abcd-224feb3ebcd1)
 Call ID: 598878a0-33cc-41e6-abcd-224feb3ebcd1
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Person
  AddLiteral (7a354ef1-6122-4a3b-a355-85dcac3a71aa)
 Call ID: 7a354ef1-6122-4a3b-a355-85dcac3a71aa
  Args:
    source: Penelope_Meredith_Eastwood
    relation: :hasBirthYear
    literal_value: 1953
    literal_type: xsd:integer
  AddLiteral (6c1f40e0-6c76-4d7e-b62a-3f357565fd67)
 Call ID: 6c1f40e0-6c76-4d7e-b62a-3f357565fd67
  Args:
    literal_value: 1979
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (3c6d80d0-4e0a-4188-9126-8e8a7a80549d)
 Call ID: 3c6d80d0-4e0a-4188-9126-8e8a7a80549d
  Args:
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (4d7694ee-b466-4614-a808-1a7ab25ffdb5)
 Call ID: 4d7694ee-b466-4614-a808-1a7ab25ffdb5
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Man
  AssignClass (bb69f390-4b72-4ce4-a91d-634623cabb7b)
 Call ID: bb69f390-4b72-4ce4-a91d-634623cabb7b
  Args:
    source: Reginald_Wray_Frank_Eastwood
    type: :Person
  AssignClass (604b4070-3ff5-484e-b1d7-4cf9edad25ac)
 Call ID: 604b4070-3ff5-484e-b1d7-4cf9edad25ac
  Args:
    type: :Woman
    source: Marian_Elizabeth_Hood
  AssignClass (74c61f21-2618-4c5d-9278-08c4505da82d)
 Call ID: 74c61f21-2618-4c5d-9278-08c4505da82d
  Args:
    type: :Person
    source: Marian_Elizabeth_Hood
  AddTriple (7ac82468-aaca-442b-852e-a0387f1404cf)
 Call ID: 7ac82468-aaca-442b-852e-a0387f1404cf
  Args:
    source: Penelope_Meredith_Eastwood
    relation: :hasFather
    target: Reginald_Wray_Frank_Eastwood
  AddTriple (7f21745e-2de7-40ab-8434-99fede8a2749)
 Call ID: 7f21745e-2de7-40ab-8434-99fede8a2749
  Args:
    source: Penelope_Meredith_Eastwood
    target: Marian_Elizabeth_Hood
    relation: :hasMother
  AddLiteral (9d6fba7d-b8f7-4d4c-b932-e72480b6a6d7)
 Call ID: 9d6fba7d-b8f7-4d4c-b932-e72480b6a6d7
  Args:
    relation: :hasDeathYear
    source: Reginald_Wray_Frank_Eastwood
    literal_value: 1980
    literal_type: xsd:integer
  AddLiteral (4f5f2e1c-9a7d-45ae-8c75-4043309acf75)
 Call ID: 4f5f2e1c-9a7d-45ae-8c75-4043309acf75
  Args:
    literal_type: xsd:integer
    literal_value: 2020
    source: Marian_Elizabeth_Hood
    relation: :hasDeathYear
  AssignClass (6d9acf5a-4013-4ac4-9053-3a39037dabf6)
 Call ID: 6d9acf5a-4013-4ac4-9053-3a39037dabf6
  Args:
    source: Eugenie_Lady_Nuttall
    type: :Woman
  AssignClass (5b3ab3f7-b68e-42bd-9081-c558ed9569dc)
 Call ID: 5b3ab3f7-b68e-42bd-9081-c558ed9569dc
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (7c773711-c85a-4865-b9ce-7016d25e9f27)
 Call ID: 7c773711-c85a-4865-b9ce-7016d25e9f27
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Eugenie_Lady_Nuttall
    relation: :hasRelation
  Finish (eaa4f8fe-df7c-4e5e-a0bc-c4ee2e3d90e6)
 Call ID: eaa4f8fe-df7c-4e5e-a0bc-c4ee2e3d90e6
  Args: