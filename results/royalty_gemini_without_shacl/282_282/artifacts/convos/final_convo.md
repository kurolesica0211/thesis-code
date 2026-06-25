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
Fergus Michael Claude Bowes-Lyon, 17th and 4th Earl of Strathmore and Kinghorne (31 December 1928 – 19 August 1987) was a British landowner and peer.
He was a nephew of Queen Elizabeth the Queen Mother, thus a first cousin of Queen Elizabeth II.
Early life and family

Born on 31 December 1928, Strathmore was the eldest son of Michael Claude Hamilton Bowes-Lyon and Elizabeth Margaret Cator (1899–1959).
His paternal grandparents were the 14th Earl and Countess of Strathmore and Kinghorne, and his maternal grandfather was John Cator, Conservative MP for Huntingdon.
In 1953, during the coronation of his cousin, Queen Elizabeth II, he was one of many servicemen lining the processional route.
Strathmore, then Captain Fergus Bowes-Lyon, married Mary Pamela McCorquodale (31 May 1932 – 28 April 2025) at St Margaret's, Westminster, on 10 April 1956 in a ceremony attended by his cousin, the Queen.
He was succeeded by his son, Michael.



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
  AssignClass (68df2683-88bf-4542-96e3-21ecc22b8f48)
 Call ID: 68df2683-88bf-4542-96e3-21ecc22b8f48
  Args:
    source: Fergus_Michael_Claude_Bowes-Lyon
    type: :Man
  AssignClass (a3a89004-855a-43c3-98a8-005c2391dc60)
 Call ID: a3a89004-855a-43c3-98a8-005c2391dc60
  Args:
    type: :Person
    source: Fergus_Michael_Claude_Bowes-Lyon
  AddLiteral (dbb15c49-129e-4e3d-bafa-0eeab2b03d8b)
 Call ID: dbb15c49-129e-4e3d-bafa-0eeab2b03d8b
  Args:
    relation: :hasBirthYear
    literal_value: 1928
    source: Fergus_Michael_Claude_Bowes-Lyon
    literal_type: xsd:integer
  AddLiteral (2a046e85-7dd6-409f-86e6-a2beb1b60ee4)
 Call ID: 2a046e85-7dd6-409f-86e6-a2beb1b60ee4
  Args:
    relation: :hasDeathYear
    literal_value: 1987
    source: Fergus_Michael_Claude_Bowes-Lyon
    literal_type: xsd:integer
  AssignClass (9655483b-610d-4c84-b337-6b3344dea095)
 Call ID: 9655483b-610d-4c84-b337-6b3344dea095
  Args:
    type: :Man
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (eacc0906-c700-47b6-9c3d-bc94c71ddf7d)
 Call ID: eacc0906-c700-47b6-9c3d-bc94c71ddf7d
  Args:
    type: :Person
    source: Michael_Claude_Hamilton_Bowes-Lyon
  AssignClass (ec3f0636-32d0-499b-8e88-d84d763930d4)
 Call ID: ec3f0636-32d0-499b-8e88-d84d763930d4
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (b5457131-c48f-4171-8275-b8a91fc6669f)
 Call ID: b5457131-c48f-4171-8275-b8a91fc6669f
  Args:
    source: Elizabeth_Margaret_Cator
    type: :Person
  AddLiteral (2499afcb-2f45-4afe-ba2d-a5392525b8eb)
 Call ID: 2499afcb-2f45-4afe-ba2d-a5392525b8eb
  Args:
    source: Elizabeth_Margaret_Cator
    literal_value: 1899
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (1fb140fe-6c5f-4c22-a2bb-0aaca0138dc3)
 Call ID: 1fb140fe-6c5f-4c22-a2bb-0aaca0138dc3
  Args:
    literal_type: xsd:integer
    literal_value: 1959
    relation: :hasDeathYear
    source: Elizabeth_Margaret_Cator
  AddTriple (88f6e71b-651c-4c0a-9b86-d4dadc728e7d)
 Call ID: 88f6e71b-651c-4c0a-9b86-d4dadc728e7d
  Args:
    target: Michael_Claude_Hamilton_Bowes-Lyon
    relation: :hasFather
    source: Fergus_Michael_Claude_Bowes-Lyon
  AddTriple (1e197d4d-0af4-4550-bd83-bd125bdb0f96)
 Call ID: 1e197d4d-0af4-4550-bd83-bd125bdb0f96
  Args:
    target: Elizabeth_Margaret_Cator
    relation: :hasMother
    source: Fergus_Michael_Claude_Bowes-Lyon
  AssignClass (096fbbf2-6fd9-4997-a3ff-f8a1ca0697e2)
 Call ID: 096fbbf2-6fd9-4997-a3ff-f8a1ca0697e2
  Args:
    type: :Man
    source: John_Cator
  AssignClass (ed3bc281-a6e7-4607-91fb-959f0d24fbbf)
 Call ID: ed3bc281-a6e7-4607-91fb-959f0d24fbbf
  Args:
    source: John_Cator
    type: :Person
  AddTriple (2b69957c-db4e-4ae8-9da8-8f2dc2d20727)
 Call ID: 2b69957c-db4e-4ae8-9da8-8f2dc2d20727
  Args:
    source: Elizabeth_Margaret_Cator
    relation: :hasFather
    target: John_Cator
  AssignClass (a9e3506e-c0a9-4087-aa5f-fc9d38613eb6)
 Call ID: a9e3506e-c0a9-4087-aa5f-fc9d38613eb6
  Args:
    source: Mary_Pamela_McCorquodale
    type: :Woman
  AssignClass (b75f0a4a-3575-4187-83b1-20b0420d1b55)
 Call ID: b75f0a4a-3575-4187-83b1-20b0420d1b55
  Args:
    source: Mary_Pamela_McCorquodale
    type: :Person
  AddLiteral (c10699b0-6b58-49b6-be98-2bb0e7557a77)
 Call ID: c10699b0-6b58-49b6-be98-2bb0e7557a77
  Args:
    source: Mary_Pamela_McCorquodale
    literal_value: 1932
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (fec4b061-f62b-452e-87a0-f680c05fc527)
 Call ID: fec4b061-f62b-452e-87a0-f680c05fc527
  Args:
    literal_value: 2025
    relation: :hasDeathYear
    source: Mary_Pamela_McCorquodale
    literal_type: xsd:integer
  AddLiteral (6dd5bbba-b52e-4bad-b147-941a72e1a5f3)
 Call ID: 6dd5bbba-b52e-4bad-b147-941a72e1a5f3
  Args:
    literal_type: xsd:integer
    literal_value: 1956
    relation: :hasMarriageYear
    source: Fergus_Michael_Claude_Bowes-Lyon
  AddTriple (ed17e8e8-4b4f-4d5d-9ba1-b3d8a471bb1f)
 Call ID: ed17e8e8-4b4f-4d5d-9ba1-b3d8a471bb1f
  Args:
    target: Mary_Pamela_McCorquodale
    source: Fergus_Michael_Claude_Bowes-Lyon
    relation: :hasRelation
  AssignClass (3f01a0cf-099c-40f2-ac33-e7007f4e4b2d)
 Call ID: 3f01a0cf-099c-40f2-ac33-e7007f4e4b2d
  Args:
    source: Michael_Bowes-Lyon
    type: :Man
  AssignClass (997fbf6f-b973-4fc9-a5bf-d1863bc6cf14)
 Call ID: 997fbf6f-b973-4fc9-a5bf-d1863bc6cf14
  Args:
    source: Michael_Bowes-Lyon
    type: :Person
  AddTriple (d41074bb-26bb-4213-84aa-763d484ddab2)
 Call ID: d41074bb-26bb-4213-84aa-763d484ddab2
  Args:
    target: Fergus_Michael_Claude_Bowes-Lyon
    relation: :hasFather
    source: Michael_Bowes-Lyon
  Finish (d5209e9f-83d6-41c3-991b-eb4c7df8a0ef)
 Call ID: d5209e9f-83d6-41c3-991b-eb4c7df8a0ef
  Args: