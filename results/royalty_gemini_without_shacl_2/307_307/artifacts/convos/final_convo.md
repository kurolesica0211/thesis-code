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
  AssignClass (ed056be8-4cf4-4a56-bab8-69a70ef21060)
 Call ID: ed056be8-4cf4-4a56-bab8-69a70ef21060
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (24fdd9ae-9e87-4244-b2f5-53498ab4f92a)
 Call ID: 24fdd9ae-9e87-4244-b2f5-53498ab4f92a
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (edb9daca-e2e0-43ad-9f9c-8d30ca887990)
 Call ID: edb9daca-e2e0-43ad-9f9c-8d30ca887990
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1947
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (969e633f-46c0-4573-8d53-26ad60131674)
 Call ID: 969e633f-46c0-4573-8d53-26ad60131674
  Args:
    literal_value: Lord Romsey
    literal_type: xsd:string
    relation: :formerlyKnownAs
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (d01b3ae5-66ab-4f2a-8e47-6799884c2a31)
 Call ID: d01b3ae5-66ab-4f2a-8e47-6799884c2a31
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Lord Brabourne
  AssignClass (2d37010a-445f-4cb3-9733-b173b24a152b)
 Call ID: 2d37010a-445f-4cb3-9733-b173b24a152b
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (404a8779-94f6-4233-b1a1-99e5d3c9a4cd)
 Call ID: 404a8779-94f6-4233-b1a1-99e5d3c9a4cd
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (aff5c095-352d-4213-b95c-8a22c85ad906)
 Call ID: aff5c095-352d-4213-b95c-8a22c85ad906
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (dbc2afea-6f5c-47ab-a43e-a2949e266b7f)
 Call ID: dbc2afea-6f5c-47ab-a43e-a2949e266b7f
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (9199c470-9872-43ba-afb4-906ff3eff8f6)
 Call ID: 9199c470-9872-43ba-afb4-906ff3eff8f6
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: John_Knatchbull
    relation: :hasFather
  AddTriple (7a6d02c4-0438-4eb1-9c94-8a848ddb8619)
 Call ID: 7a6d02c4-0438-4eb1-9c94-8a848ddb8619
  Args:
    target: Patricia_Knatchbull
    relation: :hasMother
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (fc562455-2078-4ef8-8db2-a92abf05a472)
 Call ID: fc562455-2078-4ef8-8db2-a92abf05a472
  Args:
    literal_value: 2017
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Patricia_Knatchbull
  AssignClass (acf5a3b6-e282-49ca-b671-effea7269051)
 Call ID: acf5a3b6-e282-49ca-b671-effea7269051
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (57e8f118-535e-4465-ab7d-61eb431dc68d)
 Call ID: 57e8f118-535e-4465-ab7d-61eb431dc68d
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (82991e5d-b462-434f-a530-96f44070f2f5)
 Call ID: 82991e5d-b462-434f-a530-96f44070f2f5
  Args:
    source: Patricia_Knatchbull
    relation: :hasFather
    target: Louis_Mountbatten
  AssignClass (da6cdb60-877d-4674-b492-a678a499eff1)
 Call ID: da6cdb60-877d-4674-b492-a678a499eff1
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (e85c2553-c04f-4a2b-8475-ed595da95d37)
 Call ID: e85c2553-c04f-4a2b-8475-ed595da95d37
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (f7c99c80-7513-452c-a5bb-6af16350c402)
 Call ID: f7c99c80-7513-452c-a5bb-6af16350c402
  Args:
    source: Penelope_Meredith_Eastwood
    literal_value: 1953
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (6db86fdd-e5db-4e07-b668-21d01add6893)
 Call ID: 6db86fdd-e5db-4e07-b668-21d01add6893
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
  AddLiteral (ccd65eaa-9459-408c-b2a5-283815afb2ed)
 Call ID: ccd65eaa-9459-408c-b2a5-283815afb2ed
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1979
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (054d3c27-40bf-423e-b0f0-d9d3757a9438)
 Call ID: 054d3c27-40bf-423e-b0f0-d9d3757a9438
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (d2bbb1b7-9ccd-4eba-92d3-0395f01ef05f)
 Call ID: d2bbb1b7-9ccd-4eba-92d3-0395f01ef05f
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (7b55f933-3b40-4529-ad22-2898a4cc3266)
 Call ID: 7b55f933-3b40-4529-ad22-2898a4cc3266
  Args:
    literal_value: 1912
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (c71dfbfe-8f18-441c-9402-2e4c8ebaa2f5)
 Call ID: c71dfbfe-8f18-441c-9402-2e4c8ebaa2f5
  Args:
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1980
  AssignClass (67840712-ddbe-48d9-a971-8c60f609db5f)
 Call ID: 67840712-ddbe-48d9-a971-8c60f609db5f
  Args:
    type: :Woman
    source: Marian_Elizabeth_Hood
  AssignClass (eaff856d-8243-4a3a-b1aa-a1be5aded091)
 Call ID: eaff856d-8243-4a3a-b1aa-a1be5aded091
  Args:
    type: :Person
    source: Marian_Elizabeth_Hood
  AddLiteral (688e02f8-7088-4207-82f4-8bebcb2052fc)
 Call ID: 688e02f8-7088-4207-82f4-8bebcb2052fc
  Args:
    source: Marian_Elizabeth_Hood
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1926
  AddLiteral (a5755929-6049-4188-a3e7-c168b199c26e)
 Call ID: a5755929-6049-4188-a3e7-c168b199c26e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2020
    source: Marian_Elizabeth_Hood
  AddTriple (4e39af9f-0c2f-4bed-a9ee-bbfadef30fb3)
 Call ID: 4e39af9f-0c2f-4bed-a9ee-bbfadef30fb3
  Args:
    target: Marian_Elizabeth_Hood
    relation: :hasMother
    source: Penelope_Meredith_Eastwood
  AddTriple (e0e49149-dbcd-47c4-b8a4-1ce5aa828bbb)
 Call ID: e0e49149-dbcd-47c4-b8a4-1ce5aa828bbb
  Args:
    source: Penelope_Meredith_Eastwood
    target: Reginald_Wray_Frank_Eastwood
    relation: :hasFather
  AssignClass (ae6c592c-f416-40c4-8cd4-5af4e1461f50)
 Call ID: ae6c592c-f416-40c4-8cd4-5af4e1461f50
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (3f60d7ff-7f59-47b9-9fff-8318b5c3936a)
 Call ID: 3f60d7ff-7f59-47b9-9fff-8318b5c3936a
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AddTriple (f7b2703d-f9b2-4d57-b957-c59fdb96ecde)
 Call ID: f7b2703d-f9b2-4d57-b957-c59fdb96ecde
  Args:
    relation: :hasBrother
    target: Nicholas_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (6815f894-a6c5-40fc-b227-123d88ca06bc)
 Call ID: 6815f894-a6c5-40fc-b227-123d88ca06bc
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (dda768c0-817e-4c78-b8d1-7c0cecaef9ef)
 Call ID: dda768c0-817e-4c78-b8d1-7c0cecaef9ef
  Args:
    type: :Person
    source: Doreen_Knatchbull
  AddTriple (74f1164b-2579-422a-b1d3-8c4fe833c990)
 Call ID: 74f1164b-2579-422a-b1d3-8c4fe833c990
  Args:
    target: Doreen_Knatchbull
    relation: :hasMother
    source: John_Knatchbull
  AssignClass (b440aae5-e6ac-489a-b727-388321dbc4b3)
 Call ID: b440aae5-e6ac-489a-b727-388321dbc4b3
  Args:
    type: :Woman
    source: Eugenie_Lady_Nuttall
  AssignClass (bc3dfcbf-2b8f-4e52-bcbb-f1a4f759e0d2)
 Call ID: bc3dfcbf-2b8f-4e52-bcbb-f1a4f759e0d2
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (e11236e9-670e-44ca-ad31-74ccf238783d)
 Call ID: e11236e9-670e-44ca-ad31-74ccf238783d
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasRelation
    target: Eugenie_Lady_Nuttall
  AssignClass (f7f3a3c9-fa3f-430d-889b-f549459a0ebc)
 Call ID: f7f3a3c9-fa3f-430d-889b-f549459a0ebc
  Args:
    type: :Man
    source: Edward_Austen_Knight
  AssignClass (97656181-ddc6-4096-bea7-192ac3d1a549)
 Call ID: 97656181-ddc6-4096-bea7-192ac3d1a549
  Args:
    type: :Person
    source: Edward_Austen_Knight
  AddTriple (35408b9b-451f-4934-8705-933b13d1b3b4)
 Call ID: 35408b9b-451f-4934-8705-933b13d1b3b4
  Args:
    target: Edward_Austen_Knight
    relation: :hasAncestor
    source: John_Knatchbull
  Finish (3369df4b-f690-4e92-b2a4-b0c76ddf631a)
 Call ID: 3369df4b-f690-4e92-b2a4-b0c76ddf631a
  Args: