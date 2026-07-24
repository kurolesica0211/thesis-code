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
George Ivar Louis Mountbatten, 4th Marquess of Milford Haven (born 6 June 1961), styled Earl of Medina before 1970, is a British hereditary peer and businessman.
Biography

Family

Born on 6 June 1961, Lord Milford Haven is the elder son of the 3rd Marquess of Milford Haven and Janet Mercedes Bryce, the older brother of Lord Ivar Mountbatten, and a descendant of Queen Victoria, Catherine the Great, Alexander Pushkin, and Abram Gannibal.
Upon the death of his father on 14 April 1970, he became the 4th Marquess of Milford Haven and head of the Mountbatten family.
Lord Milford Haven married, first, Sarah Georgina Walker (born London, Middlesex, 17 November 1961/2), in London on 8 March 1989.
She is the daughter of Jean Maureen (née Hatton) and George Alfred Walker.
Lord Milford Haven and Walker had two children:


The couple divorced on 27 February 1996.
In June 2016, Walker married Michael Spencer, Lord Spencer of Alresford.
Lord Milford Haven subsequently married Clare Husted Steel at Coatue Point in Nantucket, Massachusetts, on 20 August 1997.
Career

In 2000, Lord Milford Haven founded uSwitch, a website to help consumers compare and change suppliers of various services.
Lord Milford Haven won the Queen's Cup with the Broncos team in 1988 and he reached the final in 2006.



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
  AssignClass (7969187b-28b3-420f-9d85-066c12b1accb)
 Call ID: 7969187b-28b3-420f-9d85-066c12b1accb
  Args:
    type: :Man
    source: George_Ivar_Louis_Mountbatten
  AssignClass (3388186d-2f51-411f-a404-37a6adae3481)
 Call ID: 3388186d-2f51-411f-a404-37a6adae3481
  Args:
    type: :Person
    source: George_Ivar_Louis_Mountbatten
  AddLiteral (7cec5aa7-b4c0-455c-b97f-0ca61bf3624f)
 Call ID: 7cec5aa7-b4c0-455c-b97f-0ca61bf3624f
  Args:
    source: George_Ivar_Louis_Mountbatten
    literal_value: 1961
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (7c34f978-599d-478e-8bb7-e4eb0946682a)
 Call ID: 7c34f978-599d-478e-8bb7-e4eb0946682a
  Args:
    type: :Man
    source: 3rd_Marquess_of_Milford_Haven
  AssignClass (92d04a2c-ebbc-43f0-9a5b-31e61e8721c1)
 Call ID: 92d04a2c-ebbc-43f0-9a5b-31e61e8721c1
  Args:
    type: :Person
    source: 3rd_Marquess_of_Milford_Haven
  AddTriple (9b188ccb-ddc8-4578-9f59-05d75503a9d9)
 Call ID: 9b188ccb-ddc8-4578-9f59-05d75503a9d9
  Args:
    relation: :hasFather
    target: 3rd_Marquess_of_Milford_Haven
    source: George_Ivar_Louis_Mountbatten
  AddLiteral (6a959a55-6513-4f86-878f-05ad26573e50)
 Call ID: 6a959a55-6513-4f86-878f-05ad26573e50
  Args:
    source: 3rd_Marquess_of_Milford_Haven
    literal_value: 1970
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (8afbd4ce-19f0-441f-9f4c-4a4b0a97f54d)
 Call ID: 8afbd4ce-19f0-441f-9f4c-4a4b0a97f54d
  Args:
    type: :Woman
    source: Janet_Mercedes_Bryce
  AssignClass (695e1f5c-0299-4657-8fd8-520ee7caa143)
 Call ID: 695e1f5c-0299-4657-8fd8-520ee7caa143
  Args:
    type: :Person
    source: Janet_Mercedes_Bryce
  AddTriple (80ecb1c8-4491-4e00-907f-949d3eb93af1)
 Call ID: 80ecb1c8-4491-4e00-907f-949d3eb93af1
  Args:
    relation: :hasMother
    target: Janet_Mercedes_Bryce
    source: George_Ivar_Louis_Mountbatten
  AssignClass (b0ca642e-f487-41f0-ae38-7d58aea8f117)
 Call ID: b0ca642e-f487-41f0-ae38-7d58aea8f117
  Args:
    type: :Man
    source: Lord_Ivar_Mountbatten
  AssignClass (b59d2958-c54d-40f2-a7a5-8e225b470a07)
 Call ID: b59d2958-c54d-40f2-a7a5-8e225b470a07
  Args:
    type: :Person
    source: Lord_Ivar_Mountbatten
  AddTriple (9eb51c09-3509-42d2-9d2d-d85f6db442e8)
 Call ID: 9eb51c09-3509-42d2-9d2d-d85f6db442e8
  Args:
    source: George_Ivar_Louis_Mountbatten
    target: Lord_Ivar_Mountbatten
    relation: :hasBrother
  AssignClass (5d69522e-8ef3-4500-8b0c-00b90b8777b6)
 Call ID: 5d69522e-8ef3-4500-8b0c-00b90b8777b6
  Args:
    type: :Woman
    source: Sarah_Georgina_Walker
  AssignClass (083ef1d1-5c93-437c-8dc5-7882801b48bc)
 Call ID: 083ef1d1-5c93-437c-8dc5-7882801b48bc
  Args:
    type: :Person
    source: Sarah_Georgina_Walker
  AddLiteral (0aadf333-3933-4d43-aa79-448a526b6b77)
 Call ID: 0aadf333-3933-4d43-aa79-448a526b6b77
  Args:
    literal_value: 1989
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: George_Ivar_Louis_Mountbatten
  AddTriple (50ef5508-a485-42f9-b782-a3ada0e1696b)
 Call ID: 50ef5508-a485-42f9-b782-a3ada0e1696b
  Args:
    relation: :hasRelation
    target: Sarah_Georgina_Walker
    source: George_Ivar_Louis_Mountbatten
  AssignClass (c3ffba5f-f2a6-430c-a0f1-a4401124796d)
 Call ID: c3ffba5f-f2a6-430c-a0f1-a4401124796d
  Args:
    type: :Woman
    source: Jean_Maureen_Hatton
  AssignClass (68597bad-4e24-4007-a4f5-25cc2785db96)
 Call ID: 68597bad-4e24-4007-a4f5-25cc2785db96
  Args:
    type: :Person
    source: Jean_Maureen_Hatton
  AssignClass (d68a8df1-78f9-421a-85f7-dc9d970a6f5d)
 Call ID: d68a8df1-78f9-421a-85f7-dc9d970a6f5d
  Args:
    type: :Man
    source: George_Alfred_Walker
  AssignClass (8a188584-6d85-4403-9fb2-ef8ccfa7ef42)
 Call ID: 8a188584-6d85-4403-9fb2-ef8ccfa7ef42
  Args:
    type: :Person
    source: George_Alfred_Walker
  AddTriple (13fb719e-fffd-4820-a2b7-e2640e0d4cb0)
 Call ID: 13fb719e-fffd-4820-a2b7-e2640e0d4cb0
  Args:
    target: Jean_Maureen_Hatton
    relation: :hasMother
    source: Sarah_Georgina_Walker
  AddTriple (0df8d350-4265-47e4-b255-a6f852a615b6)
 Call ID: 0df8d350-4265-47e4-b255-a6f852a615b6
  Args:
    target: George_Alfred_Walker
    relation: :hasFather
    source: Sarah_Georgina_Walker
  AssignClass (ad0cdfed-f17c-4dd6-99fe-d13410aa8974)
 Call ID: ad0cdfed-f17c-4dd6-99fe-d13410aa8974
  Args:
    type: :Woman
    source: Clare_Husted_Steel
  AssignClass (de6c2dc3-20e5-4f7f-99b4-59b9593b5570)
 Call ID: de6c2dc3-20e5-4f7f-99b4-59b9593b5570
  Args:
    type: :Person
    source: Clare_Husted_Steel
  AddTriple (cb45f059-62ff-458f-b077-fc5f3e1e1db5)
 Call ID: cb45f059-62ff-458f-b077-fc5f3e1e1db5
  Args:
    source: George_Ivar_Louis_Mountbatten
    target: Clare_Husted_Steel
    relation: :hasRelation
  AddLiteral (2fcf5203-046f-45fe-afb5-47c2f41e74d1)
 Call ID: 2fcf5203-046f-45fe-afb5-47c2f41e74d1
  Args:
    literal_value: 1997
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: George_Ivar_Louis_Mountbatten
  Finish (68a9329b-076f-469f-9dce-4b571b3c644f)
 Call ID: 68a9329b-076f-469f-9dce-4b571b3c644f
  Args: