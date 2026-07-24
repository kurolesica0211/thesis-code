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
Princess Maria Immaculata Cristina Pia Isabella of Bourbon-Two Sicilies (Full Italian name: Maria Immacolata Speranza Pia Teresa Cristina Filomena Lucia Anna Isabella Cecilia Apollonia Barbara Agnese Zenobia, Principessa di Borbone delle
Due Sicilie,) (30 October 1874 – 28 November 1947) was the fourth child and eldest daughter of Prince Alfonso of Bourbon-Two Sicilies, Count of Caserta, and his wife Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage

Maria Immaculata married Prince Johann Georg of Saxony, sixth child and second-eldest son of George of Saxony and his wife Maria Anna of Portugal, on 30 October 1906 in Cannes.
Her mother-in-law, Maria Anna, was the daughter of Maria II of Portugal and her husband Ferdinand II of Portugal.
The couple did not have children, but Maria Immaculata cared for the children of her brother-in-law Frederick Augustus III of Saxony.



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
  AssignClass (f79160f3-7f0b-4ebc-90a0-21e2cfa39500)
 Call ID: f79160f3-7f0b-4ebc-90a0-21e2cfa39500
  Args:
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (b73423b2-fb5c-4428-8b85-874f76429074)
 Call ID: b73423b2-fb5c-4428-8b85-874f76429074
  Args:
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (ad923e55-3b28-478d-a877-9eefce749840)
 Call ID: ad923e55-3b28-478d-a877-9eefce749840
  Args:
    literal_type: xsd:string
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_value: Maria Immaculata Cristina Pia Isabella of Bourbon-Two Sicilies
    relation: :knownAs
  AddLiteral (b45bbaef-dd86-4426-a862-d0013b7502fb)
 Call ID: b45bbaef-dd86-4426-a862-d0013b7502fb
  Args:
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
  AddLiteral (ef64ffdc-fea3-4418-a8a5-7c27a167db56)
 Call ID: ef64ffdc-fea3-4418-a8a5-7c27a167db56
  Args:
    relation: :hasDeathYear
    literal_value: 1947
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AssignClass (75ea0583-3a49-49c1-9898-00740a6ac586)
 Call ID: 75ea0583-3a49-49c1-9898-00740a6ac586
  Args:
    source: :Prince_Alfonso_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (97944355-2544-489b-b7f7-db479d828d38)
 Call ID: 97944355-2544-489b-b7f7-db479d828d38
  Args:
    source: :Prince_Alfonso_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (2e0bf778-747a-4b79-94c7-0f356da16202)
 Call ID: 2e0bf778-747a-4b79-94c7-0f356da16202
  Args:
    type: :Woman
    source: :Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (90af174b-f809-4880-b96d-7400fe3e1f8e)
 Call ID: 90af174b-f809-4880-b96d-7400fe3e1f8e
  Args:
    source: :Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (39997099-c072-451a-8b03-0d3d6be9520f)
 Call ID: 39997099-c072-451a-8b03-0d3d6be9520f
  Args:
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    relation: :hasFather
    target: :Prince_Alfonso_of_Bourbon-Two_Sicilies
  AddTriple (031d7741-3632-49b3-a0c4-378096f44bad)
 Call ID: 031d7741-3632-49b3-a0c4-378096f44bad
  Args:
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    relation: :hasMother
    target: :Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (960c9f7c-48f2-4e66-8f76-2ad1b49c9578)
 Call ID: 960c9f7c-48f2-4e66-8f76-2ad1b49c9578
  Args:
    type: :Man
    source: :Prince_Johann_Georg_of_Saxony
  AssignClass (5b0e25d5-93aa-4e9d-a37b-8ef4f40a3238)
 Call ID: 5b0e25d5-93aa-4e9d-a37b-8ef4f40a3238
  Args:
    source: :Prince_Johann_Georg_of_Saxony
    type: :Person
  AddLiteral (b74da413-4356-466e-bd18-b19346036671)
 Call ID: b74da413-4356-466e-bd18-b19346036671
  Args:
    literal_type: xsd:integer
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    literal_value: 1906
    relation: :hasMarriageYear
  AddTriple (34ebb090-c18d-4168-8004-e7af1860d281)
 Call ID: 34ebb090-c18d-4168-8004-e7af1860d281
  Args:
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: :Prince_Johann_Georg_of_Saxony
  AssignClass (766d04e7-4d45-4a67-b078-677a32c387bd)
 Call ID: 766d04e7-4d45-4a67-b078-677a32c387bd
  Args:
    source: :George_of_Saxony
    type: :Man
  AssignClass (341caaa8-5ab3-46d2-bfe0-55b4abeeceaf)
 Call ID: 341caaa8-5ab3-46d2-bfe0-55b4abeeceaf
  Args:
    type: :Person
    source: :George_of_Saxony
  AssignClass (54a1feb9-f90b-4d5c-a711-cd0cf1d16635)
 Call ID: 54a1feb9-f90b-4d5c-a711-cd0cf1d16635
  Args:
    type: :Woman
    source: :Maria_Anna_of_Portugal
  AssignClass (d9102b87-8c35-4d0a-a646-07fed6adee1d)
 Call ID: d9102b87-8c35-4d0a-a646-07fed6adee1d
  Args:
    source: :Maria_Anna_of_Portugal
    type: :Person
  AddTriple (586134d9-c85a-4b0e-b964-5198beb97bbf)
 Call ID: 586134d9-c85a-4b0e-b964-5198beb97bbf
  Args:
    relation: :hasFather
    target: :George_of_Saxony
    source: :Prince_Johann_Georg_of_Saxony
  AddTriple (a11028ee-ffaf-4e8a-a5fe-cc5ae91bf7e9)
 Call ID: a11028ee-ffaf-4e8a-a5fe-cc5ae91bf7e9
  Args:
    source: :Prince_Johann_Georg_of_Saxony
    relation: :hasMother
    target: :Maria_Anna_of_Portugal
  AssignClass (f17aa8f7-7d43-4ed7-802b-b1d41ec66584)
 Call ID: f17aa8f7-7d43-4ed7-802b-b1d41ec66584
  Args:
    source: :Maria_II_of_Portugal
    type: :Woman
  AssignClass (a5197882-6956-4634-8884-1cb54aaa6903)
 Call ID: a5197882-6956-4634-8884-1cb54aaa6903
  Args:
    source: :Maria_II_of_Portugal
    type: :Person
  AssignClass (d2370549-abc7-4452-a0a9-ba2becc48c54)
 Call ID: d2370549-abc7-4452-a0a9-ba2becc48c54
  Args:
    type: :Man
    source: :Ferdinand_II_of_Portugal
  AssignClass (0c2de9e2-10cd-4570-b4d1-713adba1396f)
 Call ID: 0c2de9e2-10cd-4570-b4d1-713adba1396f
  Args:
    type: :Person
    source: :Ferdinand_II_of_Portugal
  AddTriple (b8d93758-961e-4bf5-a719-456174a4d06a)
 Call ID: b8d93758-961e-4bf5-a719-456174a4d06a
  Args:
    relation: :hasMother
    target: :Maria_II_of_Portugal
    source: :Maria_Anna_of_Portugal
  AddTriple (73f80c74-69e5-4430-8a9d-ebf757247400)
 Call ID: 73f80c74-69e5-4430-8a9d-ebf757247400
  Args:
    source: :Maria_Anna_of_Portugal
    relation: :hasFather
    target: :Ferdinand_II_of_Portugal
  AssignClass (6c70f50e-24ca-4a1e-a451-2c78598cdc4e)
 Call ID: 6c70f50e-24ca-4a1e-a451-2c78598cdc4e
  Args:
    type: :Man
    source: :Frederick_Augustus_III_of_Saxony
  AssignClass (53f6a0f1-3d37-40aa-b838-966a832a3937)
 Call ID: 53f6a0f1-3d37-40aa-b838-966a832a3937
  Args:
    source: :Frederick_Augustus_III_of_Saxony
    type: :Person
  AddTriple (944fdf0d-74a6-4f92-a05a-c0036b61f527)
 Call ID: 944fdf0d-74a6-4f92-a05a-c0036b61f527
  Args:
    source: :Maria_Immaculata_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: :Frederick_Augustus_III_of_Saxony
  Finish (17646b84-b6d8-4261-8d43-5ac5649f18a0)
 Call ID: 17646b84-b6d8-4261-8d43-5ac5649f18a0
  Args: