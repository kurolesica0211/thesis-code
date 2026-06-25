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
Marina Victoria Alexandra Ogilvy (born 31 July 1966) is the younger child and only daughter of Sir Angus Ogilvy and Princess Alexandra of Kent.
Early life

Marina was born at Thatched House Lodge in Richmond Park, London, the home of her parents, on 31 July 1966.
She was named after her maternal grandmother, Princess Marina of Greece and Denmark, who was also a first cousin of Prince Philip, Duke of Edinburgh.
She has an elder brother, James Ogilvy, who was born in 1964.
Marina was educated at St Mary's School, Wantage.
Marriage and children

In November 1989, Marina announced that she was pregnant by her boyfriend Paul Julian Mowatt (born in Hendon, 28 November 1962), a freelance photographer.
Marina's parents denied her allegations and said that they loved her, had not cut her off and that she was welcome at home any time.
Marina married Mowatt in Richmond Park, Surrey, on 2 February 1990, wearing a red velvet bolero with gold trim, with a black dress underneath, and a black hat.
They had two children: Zenouska May Mowatt (born 26 May 1990), and Christian Alexander Mowatt (born 4 June 1993) and divorced in October 1997.



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
  AssignClass (5a8ff08c-1d2a-4c0f-b082-1e549cc4feba)
 Call ID: 5a8ff08c-1d2a-4c0f-b082-1e549cc4feba
  Args:
    type: :Woman
    source: Marina_Victoria_Alexandra_Ogilvy
  AssignClass (f78bc9ea-ebc8-4e0e-9bd1-ad9f1faf8f53)
 Call ID: f78bc9ea-ebc8-4e0e-9bd1-ad9f1faf8f53
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    type: :Person
  AddLiteral (4f7ec75f-ef29-498d-bbee-627cd2124b5a)
 Call ID: 4f7ec75f-ef29-498d-bbee-627cd2124b5a
  Args:
    literal_value: 1966
    source: Marina_Victoria_Alexandra_Ogilvy
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (ed643c66-73d6-4f07-bd78-a9b727713310)
 Call ID: ed643c66-73d6-4f07-bd78-a9b727713310
  Args:
    type: :Man
    source: Sir_Angus_Ogilvy
  AssignClass (4c6c11c8-a875-4441-ab0e-dc4e6bbcc056)
 Call ID: 4c6c11c8-a875-4441-ab0e-dc4e6bbcc056
  Args:
    source: Sir_Angus_Ogilvy
    type: :Person
  AssignClass (490e0ec9-7314-41d6-9b37-13a641578c9a)
 Call ID: 490e0ec9-7314-41d6-9b37-13a641578c9a
  Args:
    source: Princess_Alexandra_of_Kent
    type: :Woman
  AssignClass (1ca7886c-87a4-4a79-ad6e-6ab9d4e4743b)
 Call ID: 1ca7886c-87a4-4a79-ad6e-6ab9d4e4743b
  Args:
    source: Princess_Alexandra_of_Kent
    type: :Person
  AddTriple (37864987-d90b-4057-8af4-89dbe1a9c990)
 Call ID: 37864987-d90b-4057-8af4-89dbe1a9c990
  Args:
    relation: :hasFather
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Sir_Angus_Ogilvy
  AddTriple (16c4e12b-5190-4085-b2e1-678b69a92570)
 Call ID: 16c4e12b-5190-4085-b2e1-678b69a92570
  Args:
    target: Princess_Alexandra_of_Kent
    relation: :hasMother
    source: Marina_Victoria_Alexandra_Ogilvy
  AssignClass (252c28fa-babe-45a4-ac3f-8d7c2720924f)
 Call ID: 252c28fa-babe-45a4-ac3f-8d7c2720924f
  Args:
    type: :Man
    source: James_Ogilvy
  AssignClass (8e739742-c95d-4f96-bdf5-ca095d850536)
 Call ID: 8e739742-c95d-4f96-bdf5-ca095d850536
  Args:
    source: James_Ogilvy
    type: :Person
  AddLiteral (aa4c7a47-d48a-4948-98ce-fb7552d198ca)
 Call ID: aa4c7a47-d48a-4948-98ce-fb7552d198ca
  Args:
    literal_value: 1964
    literal_type: xsd:integer
    source: James_Ogilvy
    relation: :hasBirthYear
  AddTriple (07b33be7-dfd0-4548-972d-de2f89909790)
 Call ID: 07b33be7-dfd0-4548-972d-de2f89909790
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    relation: :hasBrother
    target: James_Ogilvy
  AssignClass (abe5b3dc-da8f-4cc3-a08a-86b0457a3062)
 Call ID: abe5b3dc-da8f-4cc3-a08a-86b0457a3062
  Args:
    source: Paul_Julian_Mowatt
    type: :Man
  AssignClass (b7b379a8-f7c3-4488-bf4a-379768a37af4)
 Call ID: b7b379a8-f7c3-4488-bf4a-379768a37af4
  Args:
    type: :Person
    source: Paul_Julian_Mowatt
  AddLiteral (2973e4a9-96aa-4ad1-8258-c304787a25be)
 Call ID: 2973e4a9-96aa-4ad1-8258-c304787a25be
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Paul_Julian_Mowatt
    literal_value: 1962
  AddLiteral (4728061e-ca0d-444d-bc8c-372d45d43caf)
 Call ID: 4728061e-ca0d-444d-bc8c-372d45d43caf
  Args:
    literal_type: xsd:integer
    source: Marina_Victoria_Alexandra_Ogilvy
    relation: :hasMarriageYear
    literal_value: 1990
  AddTriple (6cdf0fec-519d-402d-82ca-e012c0fc71a5)
 Call ID: 6cdf0fec-519d-402d-82ca-e012c0fc71a5
  Args:
    target: Paul_Julian_Mowatt
    relation: :hasRelation
    source: Marina_Victoria_Alexandra_Ogilvy
  AssignClass (b5e37392-54eb-4e23-b373-20b07e154716)
 Call ID: b5e37392-54eb-4e23-b373-20b07e154716
  Args:
    type: :Woman
    source: Zenouska_May_Mowatt
  AssignClass (38cfa2f1-e78c-4ca8-9116-4f9e653d3a2e)
 Call ID: 38cfa2f1-e78c-4ca8-9116-4f9e653d3a2e
  Args:
    type: :Person
    source: Zenouska_May_Mowatt
  AddLiteral (2eb45a2b-949a-4d0b-a2e4-eed00875d6b2)
 Call ID: 2eb45a2b-949a-4d0b-a2e4-eed00875d6b2
  Args:
    literal_value: 1990
    source: Zenouska_May_Mowatt
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (8f7cd302-3f4f-4176-9915-486ba2c6e8d5)
 Call ID: 8f7cd302-3f4f-4176-9915-486ba2c6e8d5
  Args:
    target: Marina_Victoria_Alexandra_Ogilvy
    source: Zenouska_May_Mowatt
    relation: :hasMother
  AddTriple (65f13841-fdbd-471e-845f-a1b16824c066)
 Call ID: 65f13841-fdbd-471e-845f-a1b16824c066
  Args:
    relation: :hasFather
    source: Zenouska_May_Mowatt
    target: Paul_Julian_Mowatt
  AssignClass (a8e1b7c9-d4d8-44b4-b54f-2999bd827eeb)
 Call ID: a8e1b7c9-d4d8-44b4-b54f-2999bd827eeb
  Args:
    type: :Man
    source: Christian_Alexander_Mowatt
  AssignClass (c0b07b4c-a79e-49bf-af6c-778293f9a28e)
 Call ID: c0b07b4c-a79e-49bf-af6c-778293f9a28e
  Args:
    type: :Person
    source: Christian_Alexander_Mowatt
  AddLiteral (f3c46c00-6232-43af-bc89-c005f4cd9d04)
 Call ID: f3c46c00-6232-43af-bc89-c005f4cd9d04
  Args:
    relation: :hasBirthYear
    source: Christian_Alexander_Mowatt
    literal_type: xsd:integer
    literal_value: 1993
  AddTriple (e1e92a40-c2b7-461d-bc1b-0005b5e397f2)
 Call ID: e1e92a40-c2b7-461d-bc1b-0005b5e397f2
  Args:
    relation: :hasMother
    source: Christian_Alexander_Mowatt
    target: Marina_Victoria_Alexandra_Ogilvy
  AddTriple (870f3dcb-9aca-4142-b2b9-653ba78a8791)
 Call ID: 870f3dcb-9aca-4142-b2b9-653ba78a8791
  Args:
    target: Paul_Julian_Mowatt
    relation: :hasFather
    source: Christian_Alexander_Mowatt
  Finish (bc1ed566-432d-44ad-ae5e-8709aee644db)
 Call ID: bc1ed566-432d-44ad-ae5e-8709aee644db
  Args: