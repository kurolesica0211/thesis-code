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
Princess Marie Louise of Hanover and Cumberland (11 October 1879 – 31 January 1948) was the eldest child of Ernest Augustus, Crown Prince of Hanover, and Princess Thyra of Denmark, the youngest daughter of Christian IX of Denmark and Louise of Hesse-Kassel.
Through her father, Marie Louise was a great-great-granddaughter of George III of the United Kingdom and Charlotte of Mecklenburg-Strelitz.
Marriage and children

Marie Louise married Prince Maximilian of Baden (1867–1929), her third cousin twice removed, on 10 July 1900 in Gmunden, Austria-Hungary.
He was the son of Prince Wilhelm of Baden and Princess Maria Maximilianovna of Leuchtenberg and became a first cousin twice removed of Napoleon III of France.
Marie Louise and Maximilian had one daughter and one son:


Ancestry

References

External links



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
  AssignClass (0658adda-13b2-4bc7-a2ec-e5266f830a31)
 Call ID: 0658adda-13b2-4bc7-a2ec-e5266f830a31
  Args:
    type: :Woman
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (ab713bed-466e-4500-83e6-9aaf2e84ff5c)
 Call ID: ab713bed-466e-4500-83e6-9aaf2e84ff5c
  Args:
    type: :Person
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AddLiteral (2db11a13-e3fe-4bb8-b32c-13481dc4bb75)
 Call ID: 2db11a13-e3fe-4bb8-b32c-13481dc4bb75
  Args:
    literal_value: 1879
    relation: :hasBirthYear
    source: :Marie_Louise_of_Hanover_and_Cumberland
    literal_type: xsd:integer
  AddLiteral (85e0b887-296e-4a85-be7e-55e75ecabea2)
 Call ID: 85e0b887-296e-4a85-be7e-55e75ecabea2
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1948
    source: :Marie_Louise_of_Hanover_and_Cumberland
  AssignClass (621ce1f8-41b6-4499-9b23-4b76986012b5)
 Call ID: 621ce1f8-41b6-4499-9b23-4b76986012b5
  Args:
    type: :Man
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (268b0155-fce7-497a-bb82-6f088fb2aa98)
 Call ID: 268b0155-fce7-497a-bb82-6f088fb2aa98
  Args:
    type: :Ancestor
    source: :Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (14bfb5d1-10e6-4bc1-91f4-5fb81dfa66cb)
 Call ID: 14bfb5d1-10e6-4bc1-91f4-5fb81dfa66cb
  Args:
    type: :Woman
    source: :Princess_Thyra_of_Denmark
  AssignClass (b8430979-f8a9-4c57-b706-f86a53a40797)
 Call ID: b8430979-f8a9-4c57-b706-f86a53a40797
  Args:
    type: :Ancestor
    source: :Princess_Thyra_of_Denmark
  AddTriple (21bbb46e-282b-4e30-ac2d-de5b3f3c586d)
 Call ID: 21bbb46e-282b-4e30-ac2d-de5b3f3c586d
  Args:
    target: :Ernest_Augustus_Crown_Prince_of_Hanover
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasFather
  AddTriple (d60027c6-4d6c-4d3a-8e8e-6d6407774265)
 Call ID: d60027c6-4d6c-4d3a-8e8e-6d6407774265
  Args:
    target: :Princess_Thyra_of_Denmark
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasMother
  AssignClass (a02e39ff-9efd-419d-9a45-43ff86251ae9)
 Call ID: a02e39ff-9efd-419d-9a45-43ff86251ae9
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (91e7ac34-a753-481a-a266-3b41c417ddc3)
 Call ID: 91e7ac34-a753-481a-a266-3b41c417ddc3
  Args:
    type: :Ancestor
    source: :Christian_IX_of_Denmark
  AssignClass (ee48330c-9009-4eb4-87bc-b810206c77a9)
 Call ID: ee48330c-9009-4eb4-87bc-b810206c77a9
  Args:
    type: :Woman
    source: :Louise_of_Hesse_Kassel
  AssignClass (942413a2-0ea2-453a-ab03-a4fe548200dc)
 Call ID: 942413a2-0ea2-453a-ab03-a4fe548200dc
  Args:
    type: :Ancestor
    source: :Louise_of_Hesse_Kassel
  AddTriple (c875d88a-ee7c-414f-9a3a-0748ec9e15f4)
 Call ID: c875d88a-ee7c-414f-9a3a-0748ec9e15f4
  Args:
    relation: :hasFather
    source: :Princess_Thyra_of_Denmark
    target: :Christian_IX_of_Denmark
  AddTriple (a22decdf-c22a-45a7-b0c7-11f747d38e57)
 Call ID: a22decdf-c22a-45a7-b0c7-11f747d38e57
  Args:
    target: :Louise_of_Hesse_Kassel
    relation: :hasMother
    source: :Princess_Thyra_of_Denmark
  AssignClass (31a0695e-b8c3-4d19-8c51-436064aa1041)
 Call ID: 31a0695e-b8c3-4d19-8c51-436064aa1041
  Args:
    type: :Man
    source: :George_III_of_the_United_Kingdom
  AssignClass (771c2298-340c-4750-bcb0-234e22db0322)
 Call ID: 771c2298-340c-4750-bcb0-234e22db0322
  Args:
    type: :Ancestor
    source: :George_III_of_the_United_Kingdom
  AssignClass (52a36a95-9dbe-451b-9ff2-5765def7b7b1)
 Call ID: 52a36a95-9dbe-451b-9ff2-5765def7b7b1
  Args:
    type: :Woman
    source: :Charlotte_of_Mecklenburg_Strelitz
  AssignClass (2eb25985-bf26-4434-bf7a-3bde16e7dec3)
 Call ID: 2eb25985-bf26-4434-bf7a-3bde16e7dec3
  Args:
    type: :Ancestor
    source: :Charlotte_of_Mecklenburg_Strelitz
  AddTriple (6904c04d-7663-4d05-a6c5-52416aee98a3)
 Call ID: 6904c04d-7663-4d05-a6c5-52416aee98a3
  Args:
    relation: :hasAncestor
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :George_III_of_the_United_Kingdom
  AddTriple (650181ea-c365-4956-857c-e4ac87a7818e)
 Call ID: 650181ea-c365-4956-857c-e4ac87a7818e
  Args:
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasAncestor
    target: :Charlotte_of_Mecklenburg_Strelitz
  AssignClass (3dd1d6c3-eaf0-4f21-b47b-91e1a15b7954)
 Call ID: 3dd1d6c3-eaf0-4f21-b47b-91e1a15b7954
  Args:
    type: :Man
    source: :Maximilian_of_Baden
  AssignClass (4cb15376-fee0-4185-b083-65b13d55ad3f)
 Call ID: 4cb15376-fee0-4185-b083-65b13d55ad3f
  Args:
    type: :Person
    source: :Maximilian_of_Baden
  AddLiteral (d238d3ef-3582-4e4e-950e-fb16fc29377a)
 Call ID: d238d3ef-3582-4e4e-950e-fb16fc29377a
  Args:
    literal_type: xsd:integer
    source: :Maximilian_of_Baden
    literal_value: 1867
    relation: :hasBirthYear
  AddLiteral (a6198c9d-2989-42d8-a541-34e59e945cda)
 Call ID: a6198c9d-2989-42d8-a541-34e59e945cda
  Args:
    source: :Maximilian_of_Baden
    literal_value: 1929
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (dbedd4df-85ea-4d7c-9dcb-f262a51722fc)
 Call ID: dbedd4df-85ea-4d7c-9dcb-f262a51722fc
  Args:
    literal_type: xsd:integer
    source: :Marie_Louise_of_Hanover_and_Cumberland
    relation: :hasMarriageYear
    literal_value: 1900
  AddTriple (dcfbfac9-14ef-4a9d-9816-a14b75465dbb)
 Call ID: dcfbfac9-14ef-4a9d-9816-a14b75465dbb
  Args:
    relation: :hasRelation
    source: :Marie_Louise_of_Hanover_and_Cumberland
    target: :Maximilian_of_Baden
  AssignClass (95fd9024-8675-4dcd-9653-8bdb1323e0d3)
 Call ID: 95fd9024-8675-4dcd-9653-8bdb1323e0d3
  Args:
    type: :Man
    source: :Wilhelm_of_Baden
  AssignClass (cdac082d-a2f7-4668-9656-62d81631f4fe)
 Call ID: cdac082d-a2f7-4668-9656-62d81631f4fe
  Args:
    type: :Ancestor
    source: :Wilhelm_of_Baden
  AssignClass (6cd38951-7e80-434e-950a-4d6541c0e4cd)
 Call ID: 6cd38951-7e80-434e-950a-4d6541c0e4cd
  Args:
    type: :Woman
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (69f09f1b-4997-4e93-909c-2301cc59ddb2)
 Call ID: 69f09f1b-4997-4e93-909c-2301cc59ddb2
  Args:
    type: :Ancestor
    source: :Maria_Maximilianovna_of_Leuchtenberg
  AddTriple (e38680b8-8b61-4d72-b670-cee7ec7f7685)
 Call ID: e38680b8-8b61-4d72-b670-cee7ec7f7685
  Args:
    target: :Wilhelm_of_Baden
    relation: :hasFather
    source: :Maximilian_of_Baden
  AddTriple (7b1bb354-5d7a-4201-a36d-8ccb2eccae9c)
 Call ID: 7b1bb354-5d7a-4201-a36d-8ccb2eccae9c
  Args:
    source: :Maximilian_of_Baden
    relation: :hasMother
    target: :Maria_Maximilianovna_of_Leuchtenberg
  AssignClass (b65ab44e-c4ad-4a3e-88d9-cdd40e677d05)
 Call ID: b65ab44e-c4ad-4a3e-88d9-cdd40e677d05
  Args:
    type: :Man
    source: :Napoleon_III_of_France
  AssignClass (6da4dd49-7d3a-4045-a6ff-26743abaecf9)
 Call ID: 6da4dd49-7d3a-4045-a6ff-26743abaecf9
  Args:
    type: :Person
    source: :Napoleon_III_of_France
  Finish (bc8632cc-b0fa-4c24-a6d8-d9c909d4c2d3)
 Call ID: bc8632cc-b0fa-4c24-a6d8-d9c909d4c2d3
  Args: