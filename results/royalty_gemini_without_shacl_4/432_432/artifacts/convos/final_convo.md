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
Dame Sarah Rose Troughton (née Colman; born 3
Early life

Troughton was born in Paddington in 1953.
She is the eldest of the five children of Sir Timothy Colman, a past Lord Lieutenant of Norfolk, and Lady Mary Cecilia Bowes-Lyon, a granddaughter of Claude Bowes-Lyon, 14th
Her ancestor Jeremiah Colman (1777–1851) made a fortune from Colman's mustard, a business which eventually grew into Reckitt & Colman, of which her father was a director until 1989.
Public life

From 1990 to 2000, Troughton was lady-in-waiting to the Duchess of Kent.
As Lord Lieutenant, Troughton's public duties include overseeing arrangements for visits to Wiltshire by members of the Royal Family and escorting royal visitors; representing the King at events and presenting awards and medals on his behalf; liaising with the Wiltshire units of the Royal Navy, Army and Royal Air Force; leading the local magistracy as chairman of the Lord Chancellor's Advisory Committee on Justices of the Peace; and advising on nominations for national honours.
In January 2013, Troughton was appointed a Commander of the Order of St John by the Queen, and advanced to Dame of Grace of the order in 2021.
A BBC News article described Troughton as one of Camilla's longstanding personal friends.
Troughton was appointed a Dame Commander of the Royal Victorian Order in the 2025 New Year Honours.
Personal life

In 1977 she married Peter Troughton (born 1948), a member of HM Diplomatic Service, and the eldest son of Sir Charles Troughton, chairman of W H Smith.



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
  AssignClass (33ebdad8-fafd-4ac8-969a-0b4415fd95ed)
 Call ID: 33ebdad8-fafd-4ac8-969a-0b4415fd95ed
  Args:
    type: :Woman
    source: Sarah_Rose_Troughton
  AssignClass (c6f4a86a-0565-4f16-87a0-52331305977f)
 Call ID: c6f4a86a-0565-4f16-87a0-52331305977f
  Args:
    source: Sarah_Rose_Troughton
    type: :Person
  AddLiteral (2457b74b-934f-441e-8dae-dfde35a01da2)
 Call ID: 2457b74b-934f-441e-8dae-dfde35a01da2
  Args:
    relation: :hasBirthYear
    source: Sarah_Rose_Troughton
    literal_value: 1953
    literal_type: xsd:integer
  AssignClass (c6a3f4f1-2330-4396-8760-af27958684a6)
 Call ID: c6a3f4f1-2330-4396-8760-af27958684a6
  Args:
    source: Timothy_Colman
    type: :Man
  AssignClass (561f2cc7-ccf9-4549-901c-cbcb7dde1ab9)
 Call ID: 561f2cc7-ccf9-4549-901c-cbcb7dde1ab9
  Args:
    type: :Person
    source: Timothy_Colman
  AssignClass (87967899-0c36-4158-82a9-242854468b84)
 Call ID: 87967899-0c36-4158-82a9-242854468b84
  Args:
    type: :Woman
    source: Mary_Cecilia_Bowes-Lyon
  AssignClass (34996a19-7a3e-4b65-b0c2-13227642e07d)
 Call ID: 34996a19-7a3e-4b65-b0c2-13227642e07d
  Args:
    type: :Person
    source: Mary_Cecilia_Bowes-Lyon
  AddTriple (49693d03-a3ef-4af9-b5ea-ccfb0e4978d3)
 Call ID: 49693d03-a3ef-4af9-b5ea-ccfb0e4978d3
  Args:
    source: Sarah_Rose_Troughton
    relation: :hasFather
    target: Timothy_Colman
  AddTriple (3a6c071b-8853-4fbb-8449-53deeaceb567)
 Call ID: 3a6c071b-8853-4fbb-8449-53deeaceb567
  Args:
    relation: :hasMother
    source: Sarah_Rose_Troughton
    target: Mary_Cecilia_Bowes-Lyon
  AssignClass (da6eee13-62f1-4042-8f95-c4b312b83ff5)
 Call ID: da6eee13-62f1-4042-8f95-c4b312b83ff5
  Args:
    source: Claude_Bowes-Lyon
    type: :Man
  AssignClass (813aeab3-fc7d-4d4d-b658-0c070754c571)
 Call ID: 813aeab3-fc7d-4d4d-b658-0c070754c571
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AddTriple (c3e95c83-551d-40ae-be2d-c58c7eaa65c8)
 Call ID: c3e95c83-551d-40ae-be2d-c58c7eaa65c8
  Args:
    relation: :hasAncestor
    source: Mary_Cecilia_Bowes-Lyon
    target: Claude_Bowes-Lyon
  AssignClass (29c38304-f855-47d2-b535-86b60368c68e)
 Call ID: 29c38304-f855-47d2-b535-86b60368c68e
  Args:
    type: :Man
    source: Jeremiah_Colman
  AssignClass (9afb24a8-7d82-4a0c-8cec-7408330db955)
 Call ID: 9afb24a8-7d82-4a0c-8cec-7408330db955
  Args:
    type: :Person
    source: Jeremiah_Colman
  AddLiteral (ed0a8ea5-05a2-451a-a617-852b7030186f)
 Call ID: ed0a8ea5-05a2-451a-a617-852b7030186f
  Args:
    relation: :hasBirthYear
    source: Jeremiah_Colman
    literal_type: xsd:integer
    literal_value: 1777
  AddLiteral (8dd9f400-e1a1-4bef-b0e2-2d6bb9c441ff)
 Call ID: 8dd9f400-e1a1-4bef-b0e2-2d6bb9c441ff
  Args:
    source: Jeremiah_Colman
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1851
  AddTriple (4372e43c-c217-45c5-ad5c-c02c25d196b1)
 Call ID: 4372e43c-c217-45c5-ad5c-c02c25d196b1
  Args:
    target: Jeremiah_Colman
    source: Sarah_Rose_Troughton
    relation: :hasAncestor
  AssignClass (84fbe009-b78c-463c-97dc-3f75256ddf2c)
 Call ID: 84fbe009-b78c-463c-97dc-3f75256ddf2c
  Args:
    type: :Man
    source: Peter_Troughton
  AssignClass (5d5e9ec8-a3eb-4499-b55d-63b136982115)
 Call ID: 5d5e9ec8-a3eb-4499-b55d-63b136982115
  Args:
    source: Peter_Troughton
    type: :Person
  AddLiteral (25f04006-5f9c-4526-b465-17c84f4f5fdf)
 Call ID: 25f04006-5f9c-4526-b465-17c84f4f5fdf
  Args:
    relation: :hasBirthYear
    source: Peter_Troughton
    literal_type: xsd:integer
    literal_value: 1948
  AddLiteral (98edc66c-a39c-481f-a1fd-afe4a68abf58)
 Call ID: 98edc66c-a39c-481f-a1fd-afe4a68abf58
  Args:
    relation: :hasMarriageYear
    source: Sarah_Rose_Troughton
    literal_type: xsd:integer
    literal_value: 1977
  AddTriple (1911543a-ed45-4353-b3f1-d834fca1dd2a)
 Call ID: 1911543a-ed45-4353-b3f1-d834fca1dd2a
  Args:
    target: Peter_Troughton
    relation: :hasRelation
    source: Sarah_Rose_Troughton
  AssignClass (02bb2d00-ba1f-4489-95dc-1038d58c390a)
 Call ID: 02bb2d00-ba1f-4489-95dc-1038d58c390a
  Args:
    type: :Man
    source: Charles_Troughton
  AssignClass (cbd5ea99-3495-49c1-8bc7-74ce97953e3c)
 Call ID: cbd5ea99-3495-49c1-8bc7-74ce97953e3c
  Args:
    type: :Person
    source: Charles_Troughton
  AddTriple (10951458-766c-4be3-b8b7-24c6d922056e)
 Call ID: 10951458-766c-4be3-b8b7-24c6d922056e
  Args:
    target: Charles_Troughton
    relation: :hasFather
    source: Peter_Troughton
  Finish (304e0d10-6b9b-422d-992d-cdc77ab20a1d)
 Call ID: 304e0d10-6b9b-422d-992d-cdc77ab20a1d
  Args: