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
  AssignClass (1e392ca4-0c99-4299-9344-0c585222f903)
 Call ID: 1e392ca4-0c99-4299-9344-0c585222f903
  Args:
    type: :Man
    source: Norton_Louis_Philip_Knatchbull
  AssignClass (dace3e54-44ff-473d-b5ca-1eec0d6e2ee4)
 Call ID: dace3e54-44ff-473d-b5ca-1eec0d6e2ee4
  Args:
    type: :Person
    source: Norton_Louis_Philip_Knatchbull
  AddLiteral (ac1bccde-bdf1-44c8-b005-cc1fc752d8b0)
 Call ID: ac1bccde-bdf1-44c8-b005-cc1fc752d8b0
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1947
  AssignClass (b083a1d8-026b-437f-8d25-46b97a001cb0)
 Call ID: b083a1d8-026b-437f-8d25-46b97a001cb0
  Args:
    type: :Woman
    source: Patricia_Knatchbull
  AssignClass (2074cb76-fe8e-4601-a2cd-b38bf0024fee)
 Call ID: 2074cb76-fe8e-4601-a2cd-b38bf0024fee
  Args:
    type: :Person
    source: Patricia_Knatchbull
  AssignClass (e12464b2-7805-47ad-a8ec-0ed065d5850c)
 Call ID: e12464b2-7805-47ad-a8ec-0ed065d5850c
  Args:
    type: :Man
    source: John_Knatchbull
  AssignClass (42a3b953-758c-4392-a516-01fc8c39793b)
 Call ID: 42a3b953-758c-4392-a516-01fc8c39793b
  Args:
    type: :Person
    source: John_Knatchbull
  AddTriple (18eb62b6-d46f-4a58-89a0-d7d67dd61a42)
 Call ID: 18eb62b6-d46f-4a58-89a0-d7d67dd61a42
  Args:
    relation: :hasFather
    target: John_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
  AddTriple (e833a5e7-a936-40b5-981e-d3ed04b968d4)
 Call ID: e833a5e7-a936-40b5-981e-d3ed04b968d4
  Args:
    target: Patricia_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasMother
  AssignClass (8850d6c7-936a-4a3c-8cb6-606dcb2c5b03)
 Call ID: 8850d6c7-936a-4a3c-8cb6-606dcb2c5b03
  Args:
    type: :Man
    source: Louis_Mountbatten
  AssignClass (312a2457-a7b8-43fe-bc99-adbd9e5be3af)
 Call ID: 312a2457-a7b8-43fe-bc99-adbd9e5be3af
  Args:
    source: Louis_Mountbatten
    type: :Person
  AddTriple (a33d4693-d462-482c-837e-1931267f6473)
 Call ID: a33d4693-d462-482c-837e-1931267f6473
  Args:
    source: Patricia_Knatchbull
    target: Louis_Mountbatten
    relation: :hasFather
  AssignClass (8da77939-aa82-47aa-8573-718c209cf665)
 Call ID: 8da77939-aa82-47aa-8573-718c209cf665
  Args:
    type: :Man
    source: Nicholas_Knatchbull
  AssignClass (df742ecf-3939-42bf-b7b1-425c9db1dff7)
 Call ID: df742ecf-3939-42bf-b7b1-425c9db1dff7
  Args:
    source: Nicholas_Knatchbull
    type: :Person
  AddTriple (60c1efe9-94a4-44dc-8c93-cf9ca729cc37)
 Call ID: 60c1efe9-94a4-44dc-8c93-cf9ca729cc37
  Args:
    target: Nicholas_Knatchbull
    source: Norton_Louis_Philip_Knatchbull
    relation: :hasBrother
  AssignClass (947f4738-777a-4035-93c7-9ca88aef8e61)
 Call ID: 947f4738-777a-4035-93c7-9ca88aef8e61
  Args:
    type: :Woman
    source: Doreen_Knatchbull
  AssignClass (bdc5d8ad-81db-45e2-87d3-ff164a947db1)
 Call ID: bdc5d8ad-81db-45e2-87d3-ff164a947db1
  Args:
    source: Doreen_Knatchbull
    type: :Person
  AddTriple (3ceda386-e1f5-4ee8-89c9-206df2670abf)
 Call ID: 3ceda386-e1f5-4ee8-89c9-206df2670abf
  Args:
    relation: :hasMother
    source: John_Knatchbull
    target: Doreen_Knatchbull
  AssignClass (483ed583-8bc3-40de-b85a-64ddb59f7b9a)
 Call ID: 483ed583-8bc3-40de-b85a-64ddb59f7b9a
  Args:
    source: Penelope_Meredith_Eastwood
    type: :Woman
  AssignClass (c2989bd0-2cac-43c6-b2e1-0ee386e82649)
 Call ID: c2989bd0-2cac-43c6-b2e1-0ee386e82649
  Args:
    type: :Person
    source: Penelope_Meredith_Eastwood
  AddLiteral (66f525f9-8dad-47b0-85ee-584f81319f2c)
 Call ID: 66f525f9-8dad-47b0-85ee-584f81319f2c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1953
    source: Penelope_Meredith_Eastwood
  AddTriple (da5ec36a-8314-4d33-928e-d22c83bd0042)
 Call ID: da5ec36a-8314-4d33-928e-d22c83bd0042
  Args:
    source: Norton_Louis_Philip_Knatchbull
    target: Penelope_Meredith_Eastwood
    relation: :hasRelation
  AddLiteral (59f6c589-2b13-4ea3-9ab2-339391031658)
 Call ID: 59f6c589-2b13-4ea3-9ab2-339391031658
  Args:
    source: Norton_Louis_Philip_Knatchbull
    literal_value: 1979
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (22cb0e50-7662-403c-af23-d9f3eec73010)
 Call ID: 22cb0e50-7662-403c-af23-d9f3eec73010
  Args:
    type: :Man
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (05b379e3-1218-4b34-9935-d6feffbe5a6d)
 Call ID: 05b379e3-1218-4b34-9935-d6feffbe5a6d
  Args:
    type: :Person
    source: Reginald_Wray_Frank_Eastwood
  AssignClass (ee24b048-bd8c-465c-b7fa-c8a1dbc13f82)
 Call ID: ee24b048-bd8c-465c-b7fa-c8a1dbc13f82
  Args:
    source: Marian_Elizabeth
    type: :Woman
  AssignClass (70be9a27-a116-4064-a191-4e810ccc640e)
 Call ID: 70be9a27-a116-4064-a191-4e810ccc640e
  Args:
    source: Marian_Elizabeth
    type: :Person
  AddTriple (f9e7e710-c29a-40ab-8b2d-97205ef14c60)
 Call ID: f9e7e710-c29a-40ab-8b2d-97205ef14c60
  Args:
    relation: :hasFather
    target: Reginald_Wray_Frank_Eastwood
    source: Penelope_Meredith_Eastwood
  AddTriple (0f73ff1e-b2f2-478a-b5b4-3b25a40d7fe5)
 Call ID: 0f73ff1e-b2f2-478a-b5b4-3b25a40d7fe5
  Args:
    relation: :hasMother
    source: Penelope_Meredith_Eastwood
    target: Marian_Elizabeth
  AssignClass (486f98f7-153c-423f-bf43-649d78d2cbd6)
 Call ID: 486f98f7-153c-423f-bf43-649d78d2cbd6
  Args:
    type: :Woman
    source: Eugenie_Lady_Nuttall
  AssignClass (9f142d76-d855-4d3e-9199-fe193cba9beb)
 Call ID: 9f142d76-d855-4d3e-9199-fe193cba9beb
  Args:
    type: :Person
    source: Eugenie_Lady_Nuttall
  AddTriple (a1afedb1-55af-4c8f-bc44-aef9b03f27aa)
 Call ID: a1afedb1-55af-4c8f-bc44-aef9b03f27aa
  Args:
    relation: :hasRelation
    target: Eugenie_Lady_Nuttall
    source: Norton_Louis_Philip_Knatchbull
  Finish (3ef223a2-4c19-41df-9b0a-d02c7ce0c9fe)
 Call ID: 3ef223a2-4c19-41df-9b0a-d02c7ce0c9fe
  Args: