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
  AssignClass (9d25f68b-b739-4a24-ada7-ed954943d0c5)
 Call ID: 9d25f68b-b739-4a24-ada7-ed954943d0c5
  Args:
    type: :Woman
    source: Marina_Victoria_Alexandra_Ogilvy
  AssignClass (0c4444c3-a25b-449e-83a7-96a405cb1bf4)
 Call ID: 0c4444c3-a25b-449e-83a7-96a405cb1bf4
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    type: :Person
  AddLiteral (04c1a5a6-0e02-4828-9aaa-c1d9025822fc)
 Call ID: 04c1a5a6-0e02-4828-9aaa-c1d9025822fc
  Args:
    literal_value: 1966
    source: Marina_Victoria_Alexandra_Ogilvy
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (893c8697-d831-4235-9cc4-b29ef4b57f15)
 Call ID: 893c8697-d831-4235-9cc4-b29ef4b57f15
  Args:
    type: :Man
    source: Sir_Angus_Ogilvy
  AssignClass (33be5e91-5b80-4ad1-8e19-9ac7214b4ab0)
 Call ID: 33be5e91-5b80-4ad1-8e19-9ac7214b4ab0
  Args:
    source: Sir_Angus_Ogilvy
    type: :Person
  AssignClass (2309c887-1e2c-40a2-b680-709e8b10cc73)
 Call ID: 2309c887-1e2c-40a2-b680-709e8b10cc73
  Args:
    source: Princess_Alexandra_of_Kent
    type: :Woman
  AssignClass (9d7605ee-667d-41bd-93c7-e98bdad78441)
 Call ID: 9d7605ee-667d-41bd-93c7-e98bdad78441
  Args:
    type: :Person
    source: Princess_Alexandra_of_Kent
  AddTriple (be9a77a4-da72-4f62-86f8-255f33091c6c)
 Call ID: be9a77a4-da72-4f62-86f8-255f33091c6c
  Args:
    relation: :hasFather
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Sir_Angus_Ogilvy
  AddTriple (b7432ac0-8999-44a7-999a-acad45b9402a)
 Call ID: b7432ac0-8999-44a7-999a-acad45b9402a
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Princess_Alexandra_of_Kent
    relation: :hasMother
  AssignClass (11873ad3-003b-4c61-911e-6c7614d02940)
 Call ID: 11873ad3-003b-4c61-911e-6c7614d02940
  Args:
    type: :Man
    source: James_Ogilvy
  AssignClass (9d536478-2c5c-431e-be3d-10d505d97a01)
 Call ID: 9d536478-2c5c-431e-be3d-10d505d97a01
  Args:
    type: :Person
    source: James_Ogilvy
  AddTriple (78283295-6a35-4867-856a-abe4808fb03d)
 Call ID: 78283295-6a35-4867-856a-abe4808fb03d
  Args:
    relation: :hasBrother
    source: Marina_Victoria_Alexandra_Ogilvy
    target: James_Ogilvy
  AddLiteral (fc7eda4c-994e-4cac-890b-7b771c9bce6a)
 Call ID: fc7eda4c-994e-4cac-890b-7b771c9bce6a
  Args:
    source: James_Ogilvy
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (494057e7-d0bc-48eb-98fc-f66201407b63)
 Call ID: 494057e7-d0bc-48eb-98fc-f66201407b63
  Args:
    source: Paul_Julian_Mowatt
    type: :Man
  AssignClass (ee977dcc-717f-42f4-894a-084d8b1e1bd3)
 Call ID: ee977dcc-717f-42f4-894a-084d8b1e1bd3
  Args:
    type: :Person
    source: Paul_Julian_Mowatt
  AddLiteral (3fc597c1-f782-48b9-85c2-fb2ff7086da5)
 Call ID: 3fc597c1-f782-48b9-85c2-fb2ff7086da5
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1962
    source: Paul_Julian_Mowatt
  AddTriple (8196708a-5921-4222-9a71-7881f309db59)
 Call ID: 8196708a-5921-4222-9a71-7881f309db59
  Args:
    target: Paul_Julian_Mowatt
    source: Marina_Victoria_Alexandra_Ogilvy
    relation: :hasRelation
  AddLiteral (eb59e55e-e348-45d3-9e05-5bf73e258610)
 Call ID: eb59e55e-e348-45d3-9e05-5bf73e258610
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    literal_value: 1990
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (7881ffa6-cab9-42eb-a840-554788816569)
 Call ID: 7881ffa6-cab9-42eb-a840-554788816569
  Args:
    source: Zenouska_May_Mowatt
    type: :Woman
  AssignClass (ff81b105-2c31-46f5-9d50-f38848035122)
 Call ID: ff81b105-2c31-46f5-9d50-f38848035122
  Args:
    type: :Person
    source: Zenouska_May_Mowatt
  AssignClass (7a140c8c-445e-4a7b-95e0-edb43f6c84bd)
 Call ID: 7a140c8c-445e-4a7b-95e0-edb43f6c84bd
  Args:
    type: :Man
    source: Christian_Alexander_Mowatt
  AssignClass (d9e66c78-0c89-497c-878c-10b9bf94b8b3)
 Call ID: d9e66c78-0c89-497c-878c-10b9bf94b8b3
  Args:
    type: :Person
    source: Christian_Alexander_Mowatt
  AddTriple (7c313029-0b0d-43c2-9379-6d929ce06fa9)
 Call ID: 7c313029-0b0d-43c2-9379-6d929ce06fa9
  Args:
    relation: :hasChild
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Zenouska_May_Mowatt
  AddTriple (bc5e163f-1d0f-4b91-8ef9-c854b6d4d43b)
 Call ID: bc5e163f-1d0f-4b91-8ef9-c854b6d4d43b
  Args:
    relation: :hasChild
    target: Christian_Alexander_Mowatt
    source: Marina_Victoria_Alexandra_Ogilvy
  AddTriple (ca1cc68c-a527-4a66-87ab-87830977e177)
 Call ID: ca1cc68c-a527-4a66-87ab-87830977e177
  Args:
    target: Zenouska_May_Mowatt
    source: Paul_Julian_Mowatt
    relation: :hasChild
  AddTriple (4408f750-bfc9-4731-bd68-588e60791bec)
 Call ID: 4408f750-bfc9-4731-bd68-588e60791bec
  Args:
    relation: :hasChild
    target: Christian_Alexander_Mowatt
    source: Paul_Julian_Mowatt
  AddLiteral (694b980a-a892-447a-9d72-5edeb3aa7bb3)
 Call ID: 694b980a-a892-447a-9d72-5edeb3aa7bb3
  Args:
    relation: :hasBirthYear
    literal_value: 1990
    source: Zenouska_May_Mowatt
    literal_type: xsd:integer
  AddLiteral (520605fd-8577-4093-bc47-3bd5bf41c8fa)
 Call ID: 520605fd-8577-4093-bc47-3bd5bf41c8fa
  Args:
    relation: :hasBirthYear
    source: Christian_Alexander_Mowatt
    literal_value: 1993
    literal_type: xsd:integer
  Finish (c7e6117b-8177-4dd7-97bb-28421bb1e2f2)
 Call ID: c7e6117b-8177-4dd7-97bb-28421bb1e2f2
  Args: