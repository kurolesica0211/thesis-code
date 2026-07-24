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
  AssignClass (08070091-8d04-46c6-a562-edb6fedc63d1)
 Call ID: 08070091-8d04-46c6-a562-edb6fedc63d1
  Args:
    type: :Woman
    source: :Sarah_Troughton
  AssignClass (1dc4699e-ef09-47ab-a028-a2951c9e41f1)
 Call ID: 1dc4699e-ef09-47ab-a028-a2951c9e41f1
  Args:
    source: :Sarah_Troughton
    type: :Person
  AddLiteral (6de625b6-e655-41de-bff8-04ad4670ea3a)
 Call ID: 6de625b6-e655-41de-bff8-04ad4670ea3a
  Args:
    literal_value: 1953
    relation: :hasBirthYear
    source: :Sarah_Troughton
    literal_type: xsd:integer
  AssignClass (421b40a5-cc1b-4b12-a8a8-2f998d30726e)
 Call ID: 421b40a5-cc1b-4b12-a8a8-2f998d30726e
  Args:
    source: :Timothy_Colman
    type: :Man
  AssignClass (d964fb4e-8c4f-4fa8-8f52-104c3acd6731)
 Call ID: d964fb4e-8c4f-4fa8-8f52-104c3acd6731
  Args:
    type: :Person
    source: :Timothy_Colman
  AssignClass (7a83d055-b402-48a5-ae68-555c7a39fdc8)
 Call ID: 7a83d055-b402-48a5-ae68-555c7a39fdc8
  Args:
    source: :Mary_Cecilia_Bowes-Lyon
    type: :Woman
  AssignClass (46209849-6694-49c3-ba97-94ec4de58bb1)
 Call ID: 46209849-6694-49c3-ba97-94ec4de58bb1
  Args:
    source: :Mary_Cecilia_Bowes-Lyon
    type: :Person
  AddTriple (8f59bf88-e239-4cc3-9830-6ecc14f50e2b)
 Call ID: 8f59bf88-e239-4cc3-9830-6ecc14f50e2b
  Args:
    target: :Timothy_Colman
    source: :Sarah_Troughton
    relation: :hasFather
  AddTriple (d9a8d267-d8b1-4241-a48c-db857fe5f500)
 Call ID: d9a8d267-d8b1-4241-a48c-db857fe5f500
  Args:
    target: :Mary_Cecilia_Bowes-Lyon
    relation: :hasMother
    source: :Sarah_Troughton
  AssignClass (d8c793aa-1d10-492f-86bf-93517a5d619f)
 Call ID: d8c793aa-1d10-492f-86bf-93517a5d619f
  Args:
    source: :Jeremiah_Colman
    type: :Man
  AssignClass (56219ea9-e909-421e-9d93-7fb4e2a53c4c)
 Call ID: 56219ea9-e909-421e-9d93-7fb4e2a53c4c
  Args:
    source: :Jeremiah_Colman
    type: :Ancestor
  AddLiteral (4cd3972f-3468-4488-826f-01b27e6a3779)
 Call ID: 4cd3972f-3468-4488-826f-01b27e6a3779
  Args:
    literal_value: 1777
    relation: :hasBirthYear
    source: :Jeremiah_Colman
    literal_type: xsd:integer
  AddLiteral (10ebd1f2-daeb-42a1-8f79-462681ca4ef3)
 Call ID: 10ebd1f2-daeb-42a1-8f79-462681ca4ef3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Jeremiah_Colman
    literal_value: 1851
  AddTriple (43d8c3f6-fe2e-48af-bd02-795c5b1f3cad)
 Call ID: 43d8c3f6-fe2e-48af-bd02-795c5b1f3cad
  Args:
    source: :Sarah_Troughton
    relation: :hasAncestor
    target: :Jeremiah_Colman
  AssignClass (b8d411ef-f641-415e-a7ba-54253902bcdf)
 Call ID: b8d411ef-f641-415e-a7ba-54253902bcdf
  Args:
    source: :Claude_Bowes-Lyon
    type: :Man
  AssignClass (a442aac4-9ce6-4e8d-83c8-7c5bd6161df9)
 Call ID: a442aac4-9ce6-4e8d-83c8-7c5bd6161df9
  Args:
    source: :Claude_Bowes-Lyon
    type: :Ancestor
  AddTriple (8844b59d-69db-4c51-97b9-9290432800da)
 Call ID: 8844b59d-69db-4c51-97b9-9290432800da
  Args:
    relation: :hasAncestor
    source: :Mary_Cecilia_Bowes-Lyon
    target: :Claude_Bowes-Lyon
  AssignClass (c1256306-ed20-483e-a871-e67f28e50daf)
 Call ID: c1256306-ed20-483e-a871-e67f28e50daf
  Args:
    source: :Peter_Troughton
    type: :Man
  AssignClass (d6d1ac83-1129-43c4-aa8f-7be42fc9854c)
 Call ID: d6d1ac83-1129-43c4-aa8f-7be42fc9854c
  Args:
    source: :Peter_Troughton
    type: :Person
  AddLiteral (1b8094d5-c888-4923-975a-759cabf16cf9)
 Call ID: 1b8094d5-c888-4923-975a-759cabf16cf9
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: :Peter_Troughton
    relation: :hasBirthYear
  AddLiteral (a79d06f1-61f7-49a9-81ab-874f0b89b2b5)
 Call ID: a79d06f1-61f7-49a9-81ab-874f0b89b2b5
  Args:
    source: :Sarah_Troughton
    relation: :hasMarriageYear
    literal_value: 1977
    literal_type: xsd:integer
  AddTriple (2308d3e1-5c18-4814-bb6c-aaeb489fded0)
 Call ID: 2308d3e1-5c18-4814-bb6c-aaeb489fded0
  Args:
    source: :Sarah_Troughton
    relation: :hasRelation
    target: :Peter_Troughton
  AssignClass (70a3fff8-f2da-4d8d-ae1f-2aabb9acc9b1)
 Call ID: 70a3fff8-f2da-4d8d-ae1f-2aabb9acc9b1
  Args:
    source: :Charles_Troughton
    type: :Man
  AssignClass (375054ec-325d-4cd9-8a7d-916b726a7ed4)
 Call ID: 375054ec-325d-4cd9-8a7d-916b726a7ed4
  Args:
    type: :Person
    source: :Charles_Troughton
  AddTriple (a4e7758c-68a6-4064-a35d-462551ff54f8)
 Call ID: a4e7758c-68a6-4064-a35d-462551ff54f8
  Args:
    target: :Charles_Troughton
    source: :Peter_Troughton
    relation: :hasFather
  Finish (2b19fbf7-2751-4d4a-b075-736e478b0505)
 Call ID: 2b19fbf7-2751-4d4a-b075-736e478b0505
  Args: