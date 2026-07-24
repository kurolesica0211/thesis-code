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
Philipp, Prince of Hohenlohe-Langenburg (Philipp Gottfried Alexander; born 20 January 1970), is the head of the House of Hohenlohe-Langenburg, since the death of his father in 2004.
Early life and ancestry

He was born in Crailsheim, West Germany, the middle child and only son of Kraft, Prince of Hohenlohe-Langenburg (1935–2004) and his first wife, Princess Charlotte of Croÿ (b. 1938).
Paternally, he is a grandson of Princess Margarita of Greece and Denmark, and a grandnephew of Prince Philip, Duke of Edinburgh, whose funeral he attended.
Anne, Princess Royal is one of his godmothers.
Maternally, he is the grandson of Prince Alexander of Croy (1912–2002) and his Scottish wife, Anna Elspeth Campbell (1917–1986), granddaughter of Archibald Campbell, 6th of Glendaruel.
He sought public support from (then) Charles, Prince of Wales, the current King Charles III, and from former vice chancellor and foreign minister Joschka Fischer of the Green Party, who both attended a conference at Langenburg Castle in 2013.
Together with Fischer he founded the Langenburg Forum for Sustainability which cooperates with Charles' International Sustainability Unit


Langenburg castle is partially open to the public, including the state rooms and a museum of classic cars.
Marriage and issue

He married Saskia Binder (b. 15 January 1973 in Munich), daughter of former Deutsche Bank Munich director Hans Peter Binder, on 6 September 2003 in a civil ceremony at Langenburg.



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
  AssignClass (e4c397d3-ea42-494b-afb6-7f767ca5e84e)
 Call ID: e4c397d3-ea42-494b-afb6-7f767ca5e84e
  Args:
    type: :Man
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AssignClass (a77cd35c-ca03-45e5-a736-5ea435919628)
 Call ID: a77cd35c-ca03-45e5-a736-5ea435919628
  Args:
    type: :Person
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AddLiteral (5ee2884e-29e6-49c8-9232-b125e5e359a6)
 Call ID: 5ee2884e-29e6-49c8-9232-b125e5e359a6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_value: 1970
  AssignClass (4cc77b66-a5d3-49e4-80fb-337f08faff5d)
 Call ID: 4cc77b66-a5d3-49e4-80fb-337f08faff5d
  Args:
    type: :Man
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AssignClass (4cfd5955-fbbf-4fcc-9e7d-e1339d1ea7bb)
 Call ID: 4cfd5955-fbbf-4fcc-9e7d-e1339d1ea7bb
  Args:
    type: :Person
    source: Kraft_Prince_of_Hohenlohe-Langenburg
  AddLiteral (0b369fe4-c378-4b61-af82-190ddd819c28)
 Call ID: 0b369fe4-c378-4b61-af82-190ddd819c28
  Args:
    literal_type: xsd:integer
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    literal_value: 1935
    relation: :hasBirthYear
  AddLiteral (42879268-ad79-4749-ac72-0fdc8ff58764)
 Call ID: 42879268-ad79-4749-ac72-0fdc8ff58764
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    relation: :hasDeathYear
  AssignClass (9db61076-53b0-4bce-aefe-714087d371b8)
 Call ID: 9db61076-53b0-4bce-aefe-714087d371b8
  Args:
    type: :Woman
    source: Princess_Charlotte_of_Croy
  AssignClass (20f22ce6-f096-461b-a212-d641e7c1236a)
 Call ID: 20f22ce6-f096-461b-a212-d641e7c1236a
  Args:
    type: :Person
    source: Princess_Charlotte_of_Croy
  AddLiteral (f7bad8bc-3fe5-4596-bbb3-5c416a5514a4)
 Call ID: f7bad8bc-3fe5-4596-bbb3-5c416a5514a4
  Args:
    relation: :hasBirthYear
    literal_value: 1938
    source: Princess_Charlotte_of_Croy
    literal_type: xsd:integer
  AddTriple (3cdd138a-ef0c-4407-8d52-3ac21ec19e57)
 Call ID: 3cdd138a-ef0c-4407-8d52-3ac21ec19e57
  Args:
    relation: :hasFather
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    target: Kraft_Prince_of_Hohenlohe-Langenburg
  AddTriple (612b3897-2d21-4ae5-8aa7-37611f7a6dfc)
 Call ID: 612b3897-2d21-4ae5-8aa7-37611f7a6dfc
  Args:
    target: Princess_Charlotte_of_Croy
    relation: :hasMother
    source: Philipp_Prince_of_Hohenlohe-Langenburg
  AssignClass (9364c289-d243-411f-80f5-9fccd2a5f7f6)
 Call ID: 9364c289-d243-411f-80f5-9fccd2a5f7f6
  Args:
    type: :Woman
    source: Princess_Margarita_of_Greece_and_Denmark
  AssignClass (7f5ef02f-baa5-4652-9bf6-8937591ca09d)
 Call ID: 7f5ef02f-baa5-4652-9bf6-8937591ca09d
  Args:
    type: :Person
    source: Princess_Margarita_of_Greece_and_Denmark
  AddTriple (478438a8-ce30-4746-a740-96d0b10ef6e8)
 Call ID: 478438a8-ce30-4746-a740-96d0b10ef6e8
  Args:
    target: Princess_Margarita_of_Greece_and_Denmark
    source: Kraft_Prince_of_Hohenlohe-Langenburg
    relation: :hasMother
  AssignClass (caaf18a7-5f54-49e2-afcd-4feecf877015)
 Call ID: caaf18a7-5f54-49e2-afcd-4feecf877015
  Args:
    type: :Man
    source: Prince_Alexander_of_Croy
  AssignClass (ee14e2d2-ab6f-431f-8cbd-b22d7e8163d0)
 Call ID: ee14e2d2-ab6f-431f-8cbd-b22d7e8163d0
  Args:
    type: :Person
    source: Prince_Alexander_of_Croy
  AddLiteral (a2d41e12-cd20-4c82-9ac3-899b7c11798f)
 Call ID: a2d41e12-cd20-4c82-9ac3-899b7c11798f
  Args:
    relation: :hasBirthYear
    source: Prince_Alexander_of_Croy
    literal_value: 1912
    literal_type: xsd:integer
  AddLiteral (f0c833d0-810b-4ac2-9be5-ee9216c18811)
 Call ID: f0c833d0-810b-4ac2-9be5-ee9216c18811
  Args:
    literal_value: 2002
    source: Prince_Alexander_of_Croy
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (44879acd-236a-47dd-958b-5ba0b557afca)
 Call ID: 44879acd-236a-47dd-958b-5ba0b557afca
  Args:
    type: :Woman
    source: Anna_Elspeth_Campbell
  AssignClass (f40207ec-8f93-4409-97c2-980bef6149d1)
 Call ID: f40207ec-8f93-4409-97c2-980bef6149d1
  Args:
    type: :Person
    source: Anna_Elspeth_Campbell
  AddLiteral (90a88307-7f78-45d6-a456-ef8994111deb)
 Call ID: 90a88307-7f78-45d6-a456-ef8994111deb
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
    source: Anna_Elspeth_Campbell
  AddLiteral (9d654bae-6795-4fc7-85f1-f8b8fbaa557c)
 Call ID: 9d654bae-6795-4fc7-85f1-f8b8fbaa557c
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1986
    source: Anna_Elspeth_Campbell
  AddTriple (101ac461-e53f-4e20-8659-4bae65524d31)
 Call ID: 101ac461-e53f-4e20-8659-4bae65524d31
  Args:
    target: Prince_Alexander_of_Croy
    source: Princess_Charlotte_of_Croy
    relation: :hasFather
  AddTriple (82d01de2-611f-48a1-8528-39983a951e2a)
 Call ID: 82d01de2-611f-48a1-8528-39983a951e2a
  Args:
    target: Anna_Elspeth_Campbell
    relation: :hasMother
    source: Princess_Charlotte_of_Croy
  AssignClass (5d3611be-0f36-4786-98ba-22ac50e7d8bb)
 Call ID: 5d3611be-0f36-4786-98ba-22ac50e7d8bb
  Args:
    type: :Woman
    source: Saskia_Binder
  AssignClass (d6f7b192-808b-4155-8f64-03c1b6d1fec0)
 Call ID: d6f7b192-808b-4155-8f64-03c1b6d1fec0
  Args:
    type: :Person
    source: Saskia_Binder
  AddLiteral (b5e42318-8b37-439c-be03-3573ed9f8cd6)
 Call ID: b5e42318-8b37-439c-be03-3573ed9f8cd6
  Args:
    literal_value: 1973
    source: Saskia_Binder
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (9cf562af-766f-47bb-b57a-0a2b870a1b41)
 Call ID: 9cf562af-766f-47bb-b57a-0a2b870a1b41
  Args:
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    literal_value: 2003
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (1f6ba192-ab6d-4055-a7d2-a66b1990ab08)
 Call ID: 1f6ba192-ab6d-4055-a7d2-a66b1990ab08
  Args:
    target: Saskia_Binder
    source: Philipp_Prince_of_Hohenlohe-Langenburg
    relation: :hasRelation
  AssignClass (d9a36d13-660b-4e4f-8197-99c7d401577d)
 Call ID: d9a36d13-660b-4e4f-8197-99c7d401577d
  Args:
    type: :Man
    source: Hans_Peter_Binder
  AssignClass (752b6770-a031-40a9-8aa2-a62975f97218)
 Call ID: 752b6770-a031-40a9-8aa2-a62975f97218
  Args:
    type: :Person
    source: Hans_Peter_Binder
  AddTriple (5bbcc9ba-c7ac-469e-aa42-ed91f2143b91)
 Call ID: 5bbcc9ba-c7ac-469e-aa42-ed91f2143b91
  Args:
    target: Hans_Peter_Binder
    relation: :hasFather
    source: Saskia_Binder
  Finish (ac69b701-c88d-4ce8-a0dc-a7c98cb98026)
 Call ID: ac69b701-c88d-4ce8-a0dc-a7c98cb98026
  Args: