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
  AssignClass (b2df3042-da48-44c9-a96d-d7aae8da28ba)
 Call ID: b2df3042-da48-44c9-a96d-d7aae8da28ba
  Args:
    type: :Woman
    source: Marina_Victoria_Alexandra_Ogilvy
  AssignClass (d03c07b4-410f-467a-b581-ce8069744dd3)
 Call ID: d03c07b4-410f-467a-b581-ce8069744dd3
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    type: :Person
  AddLiteral (70f768eb-1f2b-4c0b-a532-19e3fb659d8c)
 Call ID: 70f768eb-1f2b-4c0b-a532-19e3fb659d8c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1966
    source: Marina_Victoria_Alexandra_Ogilvy
  AssignClass (11d861ed-ee7f-41b3-888d-62210b1657eb)
 Call ID: 11d861ed-ee7f-41b3-888d-62210b1657eb
  Args:
    source: Sir_Angus_Ogilvy
    type: :Man
  AssignClass (057f8357-43eb-453c-903f-05479d3d67b4)
 Call ID: 057f8357-43eb-453c-903f-05479d3d67b4
  Args:
    source: Sir_Angus_Ogilvy
    type: :Person
  AssignClass (53d2b25c-279f-400e-b5fa-4d1d54601daa)
 Call ID: 53d2b25c-279f-400e-b5fa-4d1d54601daa
  Args:
    source: Princess_Alexandra_of_Kent
    type: :Woman
  AssignClass (061b4f85-81d5-44c4-9cb6-90e7a8e38c72)
 Call ID: 061b4f85-81d5-44c4-9cb6-90e7a8e38c72
  Args:
    source: Princess_Alexandra_of_Kent
    type: :Person
  AddTriple (4d87adf9-6c69-4e5d-a80b-7250fb975cc9)
 Call ID: 4d87adf9-6c69-4e5d-a80b-7250fb975cc9
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Sir_Angus_Ogilvy
    relation: :hasFather
  AddTriple (c4b4f5bc-d126-4b33-bf5d-81c218cb8763)
 Call ID: c4b4f5bc-d126-4b33-bf5d-81c218cb8763
  Args:
    relation: :hasMother
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Princess_Alexandra_of_Kent
  AssignClass (841c9837-a7f6-4932-a80d-8d2ca9e75aec)
 Call ID: 841c9837-a7f6-4932-a80d-8d2ca9e75aec
  Args:
    type: :Man
    source: James_Ogilvy
  AssignClass (277f3060-d156-4228-8933-8bc7763378d7)
 Call ID: 277f3060-d156-4228-8933-8bc7763378d7
  Args:
    source: James_Ogilvy
    type: :Person
  AddTriple (ae0f71a0-fe33-4432-b092-69b70068904d)
 Call ID: ae0f71a0-fe33-4432-b092-69b70068904d
  Args:
    relation: :hasBrother
    source: Marina_Victoria_Alexandra_Ogilvy
    target: James_Ogilvy
  AddLiteral (36613ddf-7cc9-4aaa-9885-b0f4bcaf8db7)
 Call ID: 36613ddf-7cc9-4aaa-9885-b0f4bcaf8db7
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: James_Ogilvy
    literal_value: 1964
  AssignClass (eb26f6aa-3974-40e2-9afc-e10ee0f1f312)
 Call ID: eb26f6aa-3974-40e2-9afc-e10ee0f1f312
  Args:
    source: Paul_Julian_Mowatt
    type: :Man
  AssignClass (46826755-2781-48bc-b542-2bcfc51c0413)
 Call ID: 46826755-2781-48bc-b542-2bcfc51c0413
  Args:
    type: :Person
    source: Paul_Julian_Mowatt
  AddLiteral (a2314ffa-5a8d-402f-b9e5-d84cb7ff3d43)
 Call ID: a2314ffa-5a8d-402f-b9e5-d84cb7ff3d43
  Args:
    source: Paul_Julian_Mowatt
    literal_value: 1962
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (be17465c-d5ee-4a5d-8908-bf674f9c03e3)
 Call ID: be17465c-d5ee-4a5d-8908-bf674f9c03e3
  Args:
    literal_value: 1990
    source: Marina_Victoria_Alexandra_Ogilvy
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (93735358-f870-46b8-8e3b-751fb3fd6e1a)
 Call ID: 93735358-f870-46b8-8e3b-751fb3fd6e1a
  Args:
    source: Zenouska_May_Mowatt
    type: :Woman
  AssignClass (97b17453-6693-4fbf-9c6c-436154aaba1d)
 Call ID: 97b17453-6693-4fbf-9c6c-436154aaba1d
  Args:
    type: :Person
    source: Zenouska_May_Mowatt
  AddLiteral (054d64b9-8fad-45fc-a328-6b8f500eace5)
 Call ID: 054d64b9-8fad-45fc-a328-6b8f500eace5
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1990
    source: Zenouska_May_Mowatt
  AddTriple (0d33671e-9f28-4ab1-971f-8bd1286fc432)
 Call ID: 0d33671e-9f28-4ab1-971f-8bd1286fc432
  Args:
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Zenouska_May_Mowatt
    relation: :hasChild
  AddTriple (7c5707ea-b1d9-4791-a8f5-a5109fefee17)
 Call ID: 7c5707ea-b1d9-4791-a8f5-a5109fefee17
  Args:
    target: Zenouska_May_Mowatt
    source: Paul_Julian_Mowatt
    relation: :hasChild
  AssignClass (1cc9fff0-31b6-47ff-b5b7-8218bbb3c1f9)
 Call ID: 1cc9fff0-31b6-47ff-b5b7-8218bbb3c1f9
  Args:
    source: Christian_Alexander_Mowatt
    type: :Man
  AssignClass (3a61e13f-f011-455c-8fe8-473752e689ce)
 Call ID: 3a61e13f-f011-455c-8fe8-473752e689ce
  Args:
    source: Christian_Alexander_Mowatt
    type: :Person
  AddLiteral (f2b9eaf4-07f5-46dd-9750-fde6db8ac87d)
 Call ID: f2b9eaf4-07f5-46dd-9750-fde6db8ac87d
  Args:
    literal_value: 1993
    source: Christian_Alexander_Mowatt
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (6905487d-cbd9-4571-9ce3-1a29927aa92f)
 Call ID: 6905487d-cbd9-4571-9ce3-1a29927aa92f
  Args:
    relation: :hasChild
    source: Marina_Victoria_Alexandra_Ogilvy
    target: Christian_Alexander_Mowatt
  AddTriple (94f5b643-53bd-4bce-87ae-f185062fda14)
 Call ID: 94f5b643-53bd-4bce-87ae-f185062fda14
  Args:
    target: Christian_Alexander_Mowatt
    source: Paul_Julian_Mowatt
    relation: :hasChild
  AssignClass (efbd03a1-5d8c-4d6e-bb05-4b3bce9e9c0c)
 Call ID: efbd03a1-5d8c-4d6e-bb05-4b3bce9e9c0c
  Args:
    type: :Woman
    source: Princess_Marina_of_Greece_and_Denmark
  AssignClass (a7dbecd3-469f-4e90-a6e0-556bd7dbabb8)
 Call ID: a7dbecd3-469f-4e90-a6e0-556bd7dbabb8
  Args:
    type: :Person
    source: Princess_Marina_of_Greece_and_Denmark
  Finish (f4a01595-e1f8-4029-a603-6917eaca49f2)
 Call ID: f4a01595-e1f8-4029-a603-6917eaca49f2
  Args: