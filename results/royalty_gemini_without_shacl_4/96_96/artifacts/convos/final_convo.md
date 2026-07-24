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
Patrick Bowes-Lyon, 15th and 2nd Earl of Strathmore and Kinghorne (22 September 1884 – 25 May 1949), styled as Master of Glamis until 1904 and Lord Glamis until 1944, was a British landowner, peer and British Army officer.
He was the eldest brother of Queen Elizabeth the Queen Mother, thus a maternal uncle of Queen Elizabeth II.
Life

Patrick Bowes-Lyon was born on 22 September 1884 at St Paul's Walden Bury, Hertfordshire to Claude, Lord Glamis, and Cecilia Cavendish-Bentinck.
Strathmore and three of his three surviving brothers all served in World War I.
He succeeded his father as 15th and 2nd Earl of Strathmore and Kinghorne (15th earl in the peerage of Scotland and 2nd earl in the peerage of the United Kingdom) on 7 November 1944.
He was the eldest brother of Lady Elizabeth Bowes-Lyon (later Queen Elizabeth the Queen Mother), and thus an uncle of Queen Elizabeth II and Princess Margaret.
As an uncle of the bride, Strathmore was a leading guest at the 1947 wedding of Princess Elizabeth and Philip Mountbatten.
Marriage and issue

He married Lady Dorothy Beatrix Godolphin Osborne (3 December 1888 – 18 June 1946), daughter of George, 10th Duke of Leeds, on 21 November 1908 in London.
They had four children:


Death

Strathmore died on 25 May 1949 in Angus, surviving his wife by almost three years, aged 64.



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
  AssignClass (c6124d36-717c-4b2c-81b6-ace11b16a4a8)
 Call ID: c6124d36-717c-4b2c-81b6-ace11b16a4a8
  Args:
    type: :Man
    source: Patrick_Bowes-Lyon
  AssignClass (c1d5c4d6-9a9d-42db-966c-5ad5235ddd76)
 Call ID: c1d5c4d6-9a9d-42db-966c-5ad5235ddd76
  Args:
    source: Patrick_Bowes-Lyon
    type: :Person
  AssignClass (0bbb4149-e3cd-4727-97ec-807d1a736dea)
 Call ID: 0bbb4149-e3cd-4727-97ec-807d1a736dea
  Args:
    type: :Man
    source: Claude_Lord_Glamis
  AssignClass (ab032aae-1d04-403b-9130-12b6bf27f13e)
 Call ID: ab032aae-1d04-403b-9130-12b6bf27f13e
  Args:
    source: Claude_Lord_Glamis
    type: :Person
  AssignClass (df1e727a-ea34-4163-88ef-4d48e597688a)
 Call ID: df1e727a-ea34-4163-88ef-4d48e597688a
  Args:
    source: Cecilia_Cavendish-Bentinck
    type: :Woman
  AssignClass (59b26e52-ea8a-4e2c-a927-c59edf7a05b4)
 Call ID: 59b26e52-ea8a-4e2c-a927-c59edf7a05b4
  Args:
    type: :Person
    source: Cecilia_Cavendish-Bentinck
  AssignClass (3ed26268-c65f-46c8-ac4c-c6e786137b7d)
 Call ID: 3ed26268-c65f-46c8-ac4c-c6e786137b7d
  Args:
    source: Queen_Elizabeth_the_Queen_Mother
    type: :Woman
  AssignClass (9ce3c822-6ec7-484b-bb9a-52fe83f8d40a)
 Call ID: 9ce3c822-6ec7-484b-bb9a-52fe83f8d40a
  Args:
    type: :Person
    source: Queen_Elizabeth_the_Queen_Mother
  AssignClass (6d0bdd4b-09c2-4bd2-95b6-4cf491d9af7d)
 Call ID: 6d0bdd4b-09c2-4bd2-95b6-4cf491d9af7d
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (e269783c-57ef-48f1-974b-803e8f32b202)
 Call ID: e269783c-57ef-48f1-974b-803e8f32b202
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (f79abff6-55d0-414a-a348-83197773d2dd)
 Call ID: f79abff6-55d0-414a-a348-83197773d2dd
  Args:
    source: Princess_Margaret
    type: :Woman
  AssignClass (55d05779-ddef-43a8-8de8-9dae65f3cc32)
 Call ID: 55d05779-ddef-43a8-8de8-9dae65f3cc32
  Args:
    type: :Person
    source: Princess_Margaret
  AssignClass (5658cb4d-698e-4812-8366-a3da9b3e9b86)
 Call ID: 5658cb4d-698e-4812-8366-a3da9b3e9b86
  Args:
    type: :Woman
    source: Lady_Dorothy_Beatrix_Godolphin_Osborne
  AssignClass (6367ff15-d18f-450e-a02e-b8926fbc006a)
 Call ID: 6367ff15-d18f-450e-a02e-b8926fbc006a
  Args:
    type: :Person
    source: Lady_Dorothy_Beatrix_Godolphin_Osborne
  AssignClass (9d6942bd-5df5-4528-bfe4-b26f722c3a64)
 Call ID: 9d6942bd-5df5-4528-bfe4-b26f722c3a64
  Args:
    type: :Man
    source: George_10th_Duke_of_Leeds
  AssignClass (9ae10ecd-a2fd-4856-8f76-daf96164fcdf)
 Call ID: 9ae10ecd-a2fd-4856-8f76-daf96164fcdf
  Args:
    source: George_10th_Duke_of_Leeds
    type: :Person
  AddLiteral (2afd8633-3084-4e32-a219-2d30ac77e3bd)
 Call ID: 2afd8633-3084-4e32-a219-2d30ac77e3bd
  Args:
    literal_value: 1884
    source: Patrick_Bowes-Lyon
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d48adbd0-aa3a-4394-89bb-90427f93cef0)
 Call ID: d48adbd0-aa3a-4394-89bb-90427f93cef0
  Args:
    relation: :hasDeathYear
    literal_value: 1949
    source: Patrick_Bowes-Lyon
    literal_type: xsd:integer
  AddTriple (66d4c660-e178-4df2-8348-0f02ccd818f0)
 Call ID: 66d4c660-e178-4df2-8348-0f02ccd818f0
  Args:
    source: Patrick_Bowes-Lyon
    target: Claude_Lord_Glamis
    relation: :hasFather
  AddTriple (525aebf5-f870-4634-a0bf-579f5fef5b16)
 Call ID: 525aebf5-f870-4634-a0bf-579f5fef5b16
  Args:
    target: Cecilia_Cavendish-Bentinck
    source: Patrick_Bowes-Lyon
    relation: :hasMother
  AddTriple (71623f0b-f9bf-42d0-a91e-faf366a5a67c)
 Call ID: 71623f0b-f9bf-42d0-a91e-faf366a5a67c
  Args:
    source: Patrick_Bowes-Lyon
    target: Queen_Elizabeth_the_Queen_Mother
    relation: :hasSister
  AddTriple (20ed5045-cffb-42f9-a3a7-24d8b1150b41)
 Call ID: 20ed5045-cffb-42f9-a3a7-24d8b1150b41
  Args:
    source: Lady_Dorothy_Beatrix_Godolphin_Osborne
    target: George_10th_Duke_of_Leeds
    relation: :hasFather
  AddLiteral (3881e23c-106a-43d8-9f17-bf50fbe8611d)
 Call ID: 3881e23c-106a-43d8-9f17-bf50fbe8611d
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Patrick_Bowes-Lyon
    literal_value: 1908
  AddTriple (98adb81e-8c10-4585-bf37-188665668383)
 Call ID: 98adb81e-8c10-4585-bf37-188665668383
  Args:
    source: Patrick_Bowes-Lyon
    target: Lady_Dorothy_Beatrix_Godolphin_Osborne
    relation: :hasRelation
  AddLiteral (b72e47ee-ad4b-4a13-a66c-7c474d1e7c76)
 Call ID: b72e47ee-ad4b-4a13-a66c-7c474d1e7c76
  Args:
    relation: :hasBirthYear
    literal_value: 1888
    source: Lady_Dorothy_Beatrix_Godolphin_Osborne
    literal_type: xsd:integer
  AddLiteral (bc38a079-9c2e-4fab-adf5-c132031851e1)
 Call ID: bc38a079-9c2e-4fab-adf5-c132031851e1
  Args:
    source: Lady_Dorothy_Beatrix_Godolphin_Osborne
    literal_type: xsd:integer
    literal_value: 1946
    relation: :hasDeathYear
  Finish (cc789f57-3f58-495e-ae8c-31d570863671)
 Call ID: cc789f57-3f58-495e-ae8c-31d570863671
  Args: