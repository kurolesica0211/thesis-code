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
Maximilian, Margrave of Baden (Maximilian Andreas Friedrich Gustav Ernst August Bernhard Prinz und Markgraf von Baden; 3 July 1933 – 29 December 2022),  also known as Max von Baden, was a German businessman and the head of House of Baden.
Through his mother, Princess Theodora of Greece and Denmark, the second sister of Prince Philip, Duke of Edinburgh, he was a first cousin of Charles III, King of the United Kingdom.
Early life and family

Maximilian was born on 3 July 1933 in Salem.
He was the second child and eldest son of Berthold, Margrave of Baden, and his wife, Princess Theodora of Greece and Denmark.
He had one older sister, Princess Margarita, and has a younger brother, Prince Ludwig (born 1937).
Marriage and children

Maximilian was briefly engaged to his first cousin, Princess Beatrix of Hohenlohe-Langenburg (daughter of his maternal aunt, Margarita, Princess of Hohenlohe-Langenburg), although this was eventually broken off.
In 1963, he followed his father as head of the former grand ducal house of Baden, styled HRH
The Margrave of Baden, Duke of Zähringen.
In 1966, he married Archduchess Valerie of Austria (b. 1941), daughter of Archduke Hubert Salvator of Austria and his wife, Princess Rosemary of Salm-Salm.
The Margrave and Margravine had four children: 


The Margravine represented the Margrave for the funeral of Queen Elizabeth II, his aunt, at Westminster Abbey in London on 19 September 2022, with Prince Bernhard and his wife, Princess Stephanie.
He was succeeded as titular margrave and head of house by his son Bernhard.
The Margrave's funeral service on 13 January 2023 in the church of Salem Abbey was attended by numerous representatives from politics, including the minister president of Baden-Württemberg, Winfried Kretschmann, and royalty and aristocracy, such as King Philippe of Belgium, Prince Albert II of Monaco and his sister Caroline, Princess of Hanover, Prince Hassan of Jordan and the Hereditary Princess of Liechtenstein as well as the heads or representatives of most of the former ruling houses of Germany.



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
  AssignClass (715565ff-7b04-44b2-9954-f1efaf37f099)
 Call ID: 715565ff-7b04-44b2-9954-f1efaf37f099
  Args:
    type: :Man
    source: Maximilian_Margrave_of_Baden
  AssignClass (cafbd236-fd8f-4ec4-bad2-b15fbfa1f1e3)
 Call ID: cafbd236-fd8f-4ec4-bad2-b15fbfa1f1e3
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Person
  AddLiteral (4f0f4662-c415-4c2d-86bf-1343b8caee67)
 Call ID: 4f0f4662-c415-4c2d-86bf-1343b8caee67
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Maximilian_Margrave_of_Baden
    literal_value: Max von Baden
  AddLiteral (4b47e2ca-14e8-4566-b6b1-f32ce9cc787c)
 Call ID: 4b47e2ca-14e8-4566-b6b1-f32ce9cc787c
  Args:
    source: Maximilian_Margrave_of_Baden
    literal_value: 1933
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (dd72588a-7e18-44b2-94a8-9669a5402fc3)
 Call ID: dd72588a-7e18-44b2-94a8-9669a5402fc3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2022
    source: Maximilian_Margrave_of_Baden
  AssignClass (c0a11064-eedd-4a21-9627-c3329bbaf603)
 Call ID: c0a11064-eedd-4a21-9627-c3329bbaf603
  Args:
    type: :Man
    source: Berthold_Margrave_of_Baden
  AssignClass (8601eb17-7e11-4854-9c14-b898d40117ba)
 Call ID: 8601eb17-7e11-4854-9c14-b898d40117ba
  Args:
    type: :Person
    source: Berthold_Margrave_of_Baden
  AssignClass (31f2462a-7ce6-4759-8d9f-5e5cd012a90d)
 Call ID: 31f2462a-7ce6-4759-8d9f-5e5cd012a90d
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (fe363922-0f92-4790-98fc-7c7078fea5a2)
 Call ID: fe363922-0f92-4790-98fc-7c7078fea5a2
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Person
  AddTriple (191950ef-dd67-45b1-bb66-ee95ba487572)
 Call ID: 191950ef-dd67-45b1-bb66-ee95ba487572
  Args:
    target: Berthold_Margrave_of_Baden
    relation: :hasFather
    source: Maximilian_Margrave_of_Baden
  AddTriple (ba8e3e72-7281-480e-8bea-8174b4f5c6d7)
 Call ID: ba8e3e72-7281-480e-8bea-8174b4f5c6d7
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasMother
    target: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (e98926a2-0f85-426b-8bcb-fd96af1b1b69)
 Call ID: e98926a2-0f85-426b-8bcb-fd96af1b1b69
  Args:
    source: Princess_Margarita_of_Baden
    type: :Woman
  AssignClass (db11cb23-3ca6-4ebd-a172-eabae0875d37)
 Call ID: db11cb23-3ca6-4ebd-a172-eabae0875d37
  Args:
    source: Princess_Margarita_of_Baden
    type: :Person
  AddTriple (dbad3963-a7e2-421f-bead-3cc988f761a3)
 Call ID: dbad3963-a7e2-421f-bead-3cc988f761a3
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Princess_Margarita_of_Baden
    relation: :hasSister
  AssignClass (400b7070-8505-4617-bfb2-91ebe20e0670)
 Call ID: 400b7070-8505-4617-bfb2-91ebe20e0670
  Args:
    type: :Man
    source: Prince_Ludwig_of_Baden
  AssignClass (6b4c2c04-9e4a-4f5f-af4a-6624c8735626)
 Call ID: 6b4c2c04-9e4a-4f5f-af4a-6624c8735626
  Args:
    source: Prince_Ludwig_of_Baden
    type: :Person
  AddLiteral (5b393663-8cb2-4256-82ec-54262b57bf8a)
 Call ID: 5b393663-8cb2-4256-82ec-54262b57bf8a
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1937
    source: Prince_Ludwig_of_Baden
  AddTriple (0e7a0a35-33cd-4fcb-865f-1ee5892870a0)
 Call ID: 0e7a0a35-33cd-4fcb-865f-1ee5892870a0
  Args:
    relation: :hasBrother
    target: Prince_Ludwig_of_Baden
    source: Maximilian_Margrave_of_Baden
  AssignClass (fc4b6604-4483-44ea-8818-4e404705e277)
 Call ID: fc4b6604-4483-44ea-8818-4e404705e277
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (701f035d-1363-419f-a2d0-4e64befae319)
 Call ID: 701f035d-1363-419f-a2d0-4e64befae319
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Person
  AddLiteral (c7d1d9a5-8d7d-4079-9324-768d43e356f0)
 Call ID: c7d1d9a5-8d7d-4079-9324-768d43e356f0
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1941
    source: Archduchess_Valerie_of_Austria
  AddLiteral (29314db1-bb2a-4313-b9cd-4bf85ebc1985)
 Call ID: 29314db1-bb2a-4313-b9cd-4bf85ebc1985
  Args:
    literal_value: 1966
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (d5418c3a-6a16-4b0d-bf70-add251f63159)
 Call ID: d5418c3a-6a16-4b0d-bf70-add251f63159
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasRelation
    target: Archduchess_Valerie_of_Austria
  AssignClass (73286bd8-e415-43dc-b852-de8e068bcdde)
 Call ID: 73286bd8-e415-43dc-b852-de8e068bcdde
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Man
  AssignClass (01257e6f-da7e-4bff-83da-0808c4ee7dcc)
 Call ID: 01257e6f-da7e-4bff-83da-0808c4ee7dcc
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Person
  AddTriple (baa09d06-c81c-4dad-9f32-009446e7f4b9)
 Call ID: baa09d06-c81c-4dad-9f32-009446e7f4b9
  Args:
    relation: :hasSon
    target: Bernhard_Margrave_of_Baden
    source: Maximilian_Margrave_of_Baden
  AssignClass (79b8cd40-8071-4d0e-bdf4-51a5e2948d06)
 Call ID: 79b8cd40-8071-4d0e-bdf4-51a5e2948d06
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Man
  AssignClass (2d556281-1002-433e-b4c5-1b060d30e2a2)
 Call ID: 2d556281-1002-433e-b4c5-1b060d30e2a2
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Person
  AssignClass (69a10bff-538d-48d4-ab3d-e2c8c1e9b1e4)
 Call ID: 69a10bff-538d-48d4-ab3d-e2c8c1e9b1e4
  Args:
    source: Princess_Rosemary_of_Salm-Salm
    type: :Woman
  AssignClass (be126259-8bb0-4eb4-81f9-cb18d99c91af)
 Call ID: be126259-8bb0-4eb4-81f9-cb18d99c91af
  Args:
    type: :Person
    source: Princess_Rosemary_of_Salm-Salm
  AddTriple (08f76696-8976-4941-8290-fd7ffdd364bd)
 Call ID: 08f76696-8976-4941-8290-fd7ffdd364bd
  Args:
    relation: :hasFather
    target: Archduke_Hubert_Salvator_of_Austria
    source: Archduchess_Valerie_of_Austria
  AddTriple (4c657c01-265e-4b0e-9d80-56bbb29ec1a4)
 Call ID: 4c657c01-265e-4b0e-9d80-56bbb29ec1a4
  Args:
    target: Princess_Rosemary_of_Salm-Salm
    relation: :hasMother
    source: Archduchess_Valerie_of_Austria
  AssignClass (6a4aa48a-a918-4520-9464-f3d117566ea7)
 Call ID: 6a4aa48a-a918-4520-9464-f3d117566ea7
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (e7ce40a4-a578-4ebd-b42b-0093ab69dec4)
 Call ID: e7ce40a4-a578-4ebd-b42b-0093ab69dec4
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (3d53158b-4fc7-4e45-b345-b644564d5fe3)
 Call ID: 3d53158b-4fc7-4e45-b345-b644564d5fe3
  Args:
    target: Princess_Theodora_of_Greece_and_Denmark
    relation: :isBrotherOf
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (6cb9bf23-9197-4cd6-96e0-bffaa15a985a)
 Call ID: 6cb9bf23-9197-4cd6-96e0-bffaa15a985a
  Args:
    source: King_Charles_III
    type: :Man
  AssignClass (2e8b7c77-d99b-45ce-b4e4-840ebb33b709)
 Call ID: 2e8b7c77-d99b-45ce-b4e4-840ebb33b709
  Args:
    source: King_Charles_III
    type: :Person
  Finish (63143cff-d8ac-4ce9-9323-99738bfdb769)
 Call ID: 63143cff-d8ac-4ce9-9323-99738bfdb769
  Args: