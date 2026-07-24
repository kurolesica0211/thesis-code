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
  AssignClass (f88f7d59-052d-4b83-a28b-545616d32a0c)
 Call ID: f88f7d59-052d-4b83-a28b-545616d32a0c
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (f452cbcf-7d42-4715-976f-6d7a248212b4)
 Call ID: f452cbcf-7d42-4715-976f-6d7a248212b4
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (c15f4198-bc92-4d17-8036-ddae5a54551a)
 Call ID: c15f4198-bc92-4d17-8036-ddae5a54551a
  Args:
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1947
    relation: :hasBirthYear
  AddLiteral (b3dc4a89-c54a-4272-8a76-bba3655f65e0)
 Call ID: b3dc4a89-c54a-4272-8a76-bba3655f65e0
  Args:
    literal_type: xsd:string
    source: Norton_Louis_Philip_Knatchbull
    relation: :formerlyKnownAs
    literal_value: Lord Romsey
  AddLiteral (2c4b6834-f560-4081-9a4f-00d7cdcad242)
 Call ID: 2c4b6834-f560-4081-9a4f-00d7cdcad242
  Args:
    literal_value: Lord Brabourne
    relation: :formerlyKnownAs
    source: Norton_Louis_Philip_Knatchbull
    literal_type: xsd:string
  AssignClass (833fee89-6b0f-48d4-812d-989a7f35139a)
 Call ID: 833fee89-6b0f-48d4-812d-989a7f35139a
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (08e8e40f-1efb-491f-be85-28246c2b6686)
 Call ID: 08e8e40f-1efb-491f-be85-28246c2b6686
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (ee7dd3c7-8bd7-46d3-a051-6218505d5daf)
 Call ID: ee7dd3c7-8bd7-46d3-a051-6218505d5daf
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (cc53280c-e410-4935-b94d-5e4f7ee14772)
 Call ID: cc53280c-e410-4935-b94d-5e4f7ee14772
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (75db2bd3-fa5e-4c1e-8ded-60e00a24f340)
 Call ID: 75db2bd3-fa5e-4c1e-8ded-60e00a24f340
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Patricia_Knatchbull
    relation: :hasMother
  AddTriple (e7fc1368-6299-4598-8ef2-3e87b9aa65e9)
 Call ID: e7fc1368-6299-4598-8ef2-3e87b9aa65e9
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasFather
    target: John_Knatchbull
  AddLiteral (f8fbc881-aaec-4d93-9b98-58b7dde79536)
 Call ID: f8fbc881-aaec-4d93-9b98-58b7dde79536
  Args:
    literal_type: xsd:integer
    literal_value: 2005
    relation: :hasDeathYear
    source: John_Knatchbull
  AddLiteral (87d39e2f-3fe5-44ec-9ee7-f3f1b9a9eb66)
 Call ID: 87d39e2f-3fe5-44ec-9ee7-f3f1b9a9eb66
  Args:
    source: Patricia_Knatchbull
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (77632ba2-c8b6-4df2-b4bc-5ed9dec974fb)
 Call ID: 77632ba2-c8b6-4df2-b4bc-5ed9dec974fb
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (ee22237a-8115-4303-a899-90813f312f94)
 Call ID: ee22237a-8115-4303-a899-90813f312f94
  Args:
    type: :Person
    source: Louis_Mountbatten
  AddTriple (c0b40126-206e-4679-ae18-ca65ac67eb78)
 Call ID: c0b40126-206e-4679-ae18-ca65ac67eb78
  Args:
    relation: :isAncestorOf
    target: Norton_Louis_Philip_Knatchbull
    source: Louis_Mountbatten
  AssignClass (264b1358-87b8-48ef-8832-2db41aae3a06)
 Call ID: 264b1358-87b8-48ef-8832-2db41aae3a06
  Args:
    type: :Woman
    source: Penelope_Meredith_Eastwood
  AssignClass (3ab6b763-d577-4389-aed4-2cf6534ef21e)
 Call ID: 3ab6b763-d577-4389-aed4-2cf6534ef21e
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (5052d82c-6e57-492f-93ef-0f7e541f7366)
 Call ID: 5052d82c-6e57-492f-93ef-0f7e541f7366
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1953
    source: Penelope_Meredith_Eastwood
  AddTriple (a22bb7e2-a0a7-4c60-ac99-bf3b8baff759)
 Call ID: a22bb7e2-a0a7-4c60-ac99-bf3b8baff759
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
  AddLiteral (a96e1f9c-6025-43d4-be27-d9c87c918bce)
 Call ID: a96e1f9c-6025-43d4-be27-d9c87c918bce
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (928becb3-e513-48f0-9ea5-69c1fc07b72b)
 Call ID: 928becb3-e513-48f0-9ea5-69c1fc07b72b
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (9946c377-61a1-4d59-b3bc-4c6fe6cf0639)
 Call ID: 9946c377-61a1-4d59-b3bc-4c6fe6cf0639
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AddLiteral (35966510-cb45-43e0-90e6-3c3265cac721)
 Call ID: 35966510-cb45-43e0-90e6-3c3265cac721
  Args:
    literal_type: xsd:integer
    source: Reginald_Wray_Frank_Eastwood
    relation: :hasBirthYear
    literal_value: 1912
  AddLiteral (4ac66c1b-d0e6-412b-99a5-0d8392b353da)
 Call ID: 4ac66c1b-d0e6-412b-99a5-0d8392b353da
  Args:
    relation: :hasDeathYear
    literal_value: 1980
    source: Reginald_Wray_Frank_Eastwood
    literal_type: xsd:integer
  AddTriple (fad96915-87c8-41a7-a8c5-c7266bfc0c13)
 Call ID: fad96915-87c8-41a7-a8c5-c7266bfc0c13
  Args:
    relation: :hasFather
    target: Reginald_Wray_Frank_Eastwood
    source: Penelope_Meredith_Eastwood
  AssignClass (e451062b-294c-4f56-8f6f-76f4e66c262a)
 Call ID: e451062b-294c-4f56-8f6f-76f4e66c262a
  Args:
    type: :Woman
    source: Marian_Elizabeth
  AssignClass (496f7002-3334-4a3f-8e2c-a127c2122079)
 Call ID: 496f7002-3334-4a3f-8e2c-a127c2122079
  Args:
    type: :Person
    source: Marian_Elizabeth
  AddLiteral (efa10b12-34bc-4fd9-ad2b-35964ddb8c03)
 Call ID: efa10b12-34bc-4fd9-ad2b-35964ddb8c03
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1926
    source: Marian_Elizabeth
  AddLiteral (d308ba90-0501-45c1-8ca7-4858febe19a1)
 Call ID: d308ba90-0501-45c1-8ca7-4858febe19a1
  Args:
    source: Marian_Elizabeth
    literal_value: 2020
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (bac1962a-4882-4541-8485-e4860a824d21)
 Call ID: bac1962a-4882-4541-8485-e4860a824d21
  Args:
    relation: :hasMother
    target: Marian_Elizabeth
    source: Penelope_Meredith_Eastwood
  AssignClass (cd846f33-6df8-4367-9866-a9d5f2d458fa)
 Call ID: cd846f33-6df8-4367-9866-a9d5f2d458fa
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (65b8e7cc-2e99-4a89-a9d6-bba857ecd7dd)
 Call ID: 65b8e7cc-2e99-4a89-a9d6-bba857ecd7dd
  Args:
    type: :Person
    source: Nicholas_Knatchbull
  AddTriple (545cc07e-e993-4447-9849-0a240b7fd97e)
 Call ID: 545cc07e-e993-4447-9849-0a240b7fd97e
  Args:
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasBrother
    target: Nicholas_Knatchbull
  AssignClass (ebf939b3-02ab-4cad-b3a7-e882116514b1)
 Call ID: ebf939b3-02ab-4cad-b3a7-e882116514b1
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (33855495-7c4c-4151-af16-5fb57bd5d8bc)
 Call ID: 33855495-7c4c-4151-af16-5fb57bd5d8bc
  Args:
    type: :Person
    source: Doreen_Knatchbull
  AddTriple (ee43a91d-ed7c-485f-97ae-cf8270541421)
 Call ID: ee43a91d-ed7c-485f-97ae-cf8270541421
  Args:
    target: Doreen_Knatchbull
    relation: :hasMother
    source: John_Knatchbull
  AssignClass (1d23cef6-95ac-4ddc-a585-d5bc972681ae)
 Call ID: 1d23cef6-95ac-4ddc-a585-d5bc972681ae
  Args:
    type: :Woman
    source: Eugenie_Lady_Nuttall
  AssignClass (a0bfb993-8d12-4a38-8b03-b6ab56d87bd2)
 Call ID: a0bfb993-8d12-4a38-8b03-b6ab56d87bd2
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (ee3c6e89-4f4c-4457-b1e9-74829cfc4e09)
 Call ID: ee3c6e89-4f4c-4457-b1e9-74829cfc4e09
  Args:
    relation: :hasRelation
    target: Eugenie_Lady_Nuttall
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (9333fb05-cd54-4d4d-a743-9577afb35d5c)
 Call ID: 9333fb05-cd54-4d4d-a743-9577afb35d5c
  Args:
    type: :Man
    source: Nicholas_Nuttall
  AssignClass (98d5cca3-7a66-413f-885c-2f59d66d2d04)
 Call ID: 98d5cca3-7a66-413f-885c-2f59d66d2d04
  Args:
    type: :Person
    source: Nicholas_Nuttall
  AddTriple (8034e947-b87f-4524-a83a-f5d91eb6a8c6)
 Call ID: 8034e947-b87f-4524-a83a-f5d91eb6a8c6
  Args:
    source: Eugenie_Lady_Nuttall
    target: Nicholas_Nuttall
    relation: :hasRelation
  Finish (90af6819-6a04-43dd-98e1-8328429f0ada)
 Call ID: 90af6819-6a04-43dd-98e1-8328429f0ada
  Args: