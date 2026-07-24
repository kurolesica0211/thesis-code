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
Princess Beatrix of Hohenlohe-Langenburg (German: Beatrix Alice Marie Melita Margarete Prinzessin zu Hohenlohe-Langenburg; 10 July 1936 – 15 November 1997) was a German princess from the House of Hohenlohe-Langenburg.
She was a niece of Prince Philip, Duke of Edinburgh, and thus a first cousin of King Charles III.
Biography

Beatrix was born on 10 July 1936 in Schwäbisch Hall to Gottfried, Hereditary Prince of Hohenlohe-Langenburg, and Princess Margarita of Greece and Denmark, the eldest sister of Prince Philip, Duke of Edinburgh.
The family was not invited to Philip's wedding to Princess Elizabeth of the United Kingdom in 1947, due to her parents' membership in the Nazi Party.
Six years later, however, Beatrix and her family were seated in the royal box at  her aunt's coronation in Westminster Abbey.
In January 1956, Beatrix and her cousin, Princess Christina of Hesse, moved to London into a flat arranged by their uncle, Prince Philip, in Dolphin Square.
Beatrix took dressmaking classes at the Royal College of Art.
While Princess Christina eventually settled in the United Kingdom, marrying Prince Andrew of Yugoslavia whom the princesses were close friends with during their stay, Beatrix returned to Germany that same year.
In 1961, Beatrix became engaged to her first cousin, Maximilian, Hereditary Prince of Baden.
Maximilian later married Archduchess Valerie of Austria (b. 1941) in 1966 and Beatrix never married.
In her later years, she served as secretary to Margaret, Princess of Hesse and by Rhine, the sister-in-law of her aunt, Princess Cecilie.
She lived in Langenburg, Germany, for most of her life.
She continued to attend family events in Britain, such as the weddings of her cousins Prince Charles (later King Charles III) and Prince Andrew in 1981 and 1986, respectively.
Beatrix died on 15 November 1997, aged 61, in the town where she was born.



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
  AssignClass (8963e825-8a26-4992-94ca-268bbf8866ac)
 Call ID: 8963e825-8a26-4992-94ca-268bbf8866ac
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    type: :Woman
  AssignClass (9b8cc202-dbe2-42e6-ad6b-294521139198)
 Call ID: 9b8cc202-dbe2-42e6-ad6b-294521139198
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    type: :Person
  AddLiteral (2924e84a-66e6-495c-90f3-9bbc714498be)
 Call ID: 2924e84a-66e6-495c-90f3-9bbc714498be
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1936
  AddLiteral (9c33ff77-9bc8-4807-ae3d-7ec135a6d741)
 Call ID: 9c33ff77-9bc8-4807-ae3d-7ec135a6d741
  Args:
    literal_value: 1997
    literal_type: xsd:integer
    source: Beatrix_of_Hohenlohe-Langenburg
    relation: :hasDeathYear
  AssignClass (be8dad1e-3ca8-42e9-9cbd-537ee1dd743e)
 Call ID: be8dad1e-3ca8-42e9-9cbd-537ee1dd743e
  Args:
    source: Gottfried_of_Hohenlohe-Langenburg
    type: :Man
  AssignClass (c7671310-9fc8-4c94-8b45-b3eed47cf4b5)
 Call ID: c7671310-9fc8-4c94-8b45-b3eed47cf4b5
  Args:
    type: :Person
    source: Gottfried_of_Hohenlohe-Langenburg
  AssignClass (5e84d467-b61e-4a5f-bd87-91db56017199)
 Call ID: 5e84d467-b61e-4a5f-bd87-91db56017199
  Args:
    type: :Woman
    source: Margarita_of_Greece_and_Denmark
  AssignClass (5e0c777b-50a1-4cb7-ab43-4c093340b482)
 Call ID: 5e0c777b-50a1-4cb7-ab43-4c093340b482
  Args:
    type: :Person
    source: Margarita_of_Greece_and_Denmark
  AddTriple (1d240dc5-0f5b-4f88-bde8-72de8bd579f6)
 Call ID: 1d240dc5-0f5b-4f88-bde8-72de8bd579f6
  Args:
    target: Gottfried_of_Hohenlohe-Langenburg
    relation: :hasFather
    source: Beatrix_of_Hohenlohe-Langenburg
  AddTriple (7ddb6ddb-23dd-4aa3-b7a6-b7ddbcb19317)
 Call ID: 7ddb6ddb-23dd-4aa3-b7a6-b7ddbcb19317
  Args:
    relation: :hasMother
    target: Margarita_of_Greece_and_Denmark
    source: Beatrix_of_Hohenlohe-Langenburg
  AssignClass (4561ec4f-a218-4c2a-9298-f754953f9b2d)
 Call ID: 4561ec4f-a218-4c2a-9298-f754953f9b2d
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Man
  AssignClass (a87acac5-11b1-4ae5-9008-1e16c6286594)
 Call ID: a87acac5-11b1-4ae5-9008-1e16c6286594
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (7f33c5d5-2327-4467-a93b-06ac027acb81)
 Call ID: 7f33c5d5-2327-4467-a93b-06ac027acb81
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    target: Margarita_of_Greece_and_Denmark
    relation: :isBrotherOf
  AddTriple (ad7c5f57-88b2-42d3-bb3e-90fe1195e2b6)
 Call ID: ad7c5f57-88b2-42d3-bb3e-90fe1195e2b6
  Args:
    relation: :isSisterOf
    target: Prince_Philip_Duke_of_Edinburgh
    source: Margarita_of_Greece_and_Denmark
  AssignClass (426cf64c-2306-42bc-b9b0-582716393002)
 Call ID: 426cf64c-2306-42bc-b9b0-582716393002
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (7c3ff79a-6b31-4bc0-82e6-510b4952f959)
 Call ID: 7c3ff79a-6b31-4bc0-82e6-510b4952f959
  Args:
    source: King_Charles_III
    type: :Person
  AssignClass (91ea4eb1-a658-47b9-976c-209f894dfccc)
 Call ID: 91ea4eb1-a658-47b9-976c-209f894dfccc
  Args:
    type: :Woman
    source: Princess_Christina_of_Hesse
  AssignClass (4830d3f1-ad3e-4a7c-a0bd-50325f12c52c)
 Call ID: 4830d3f1-ad3e-4a7c-a0bd-50325f12c52c
  Args:
    type: :Person
    source: Princess_Christina_of_Hesse
  AssignClass (a48c5a6b-73bd-48ee-b1d7-c71b4e7279be)
 Call ID: a48c5a6b-73bd-48ee-b1d7-c71b4e7279be
  Args:
    source: Prince_Andrew_of_Yugoslavia
    type: :Man
  AssignClass (4dd516ca-54f2-40b3-a351-f0c9aa6c005a)
 Call ID: 4dd516ca-54f2-40b3-a351-f0c9aa6c005a
  Args:
    type: :Person
    source: Prince_Andrew_of_Yugoslavia
  AssignClass (e38500af-0190-4c0f-a10e-cec225983bd8)
 Call ID: e38500af-0190-4c0f-a10e-cec225983bd8
  Args:
    source: Maximilian_Hereditary_Prince_of_Baden
    type: :Man
  AssignClass (055ee051-8244-405a-a8fc-c6b36faf4585)
 Call ID: 055ee051-8244-405a-a8fc-c6b36faf4585
  Args:
    source: Maximilian_Hereditary_Prince_of_Baden
    type: :Person
  AssignClass (c52e53ae-56f8-43b3-9626-3341abc39542)
 Call ID: c52e53ae-56f8-43b3-9626-3341abc39542
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (ffbf0254-8840-4b19-8596-66457e11dbb7)
 Call ID: ffbf0254-8840-4b19-8596-66457e11dbb7
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Person
  AddLiteral (ac21cf1e-4f01-4e71-a98c-3a6c7995117e)
 Call ID: ac21cf1e-4f01-4e71-a98c-3a6c7995117e
  Args:
    relation: :hasMarriageYear
    source: Maximilian_Hereditary_Prince_of_Baden
    literal_value: 1966
    literal_type: xsd:integer
  AssignClass (f7fd87d5-c91a-4961-8e94-f82100e1aac1)
 Call ID: f7fd87d5-c91a-4961-8e94-f82100e1aac1
  Args:
    source: Margaret_Princess_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (9ea39fe6-87af-47b6-b75d-fbd12ecec485)
 Call ID: 9ea39fe6-87af-47b6-b75d-fbd12ecec485
  Args:
    type: :Person
    source: Margaret_Princess_of_Hesse_and_by_Rhine
  AssignClass (7127464e-7ef6-43e6-919c-dea92448d9ac)
 Call ID: 7127464e-7ef6-43e6-919c-dea92448d9ac
  Args:
    source: Princess_Cecilie
    type: :Woman
  AssignClass (d3054170-d2c6-445d-a8b3-d26ea1c754e2)
 Call ID: d3054170-d2c6-445d-a8b3-d26ea1c754e2
  Args:
    type: :Person
    source: Princess_Cecilie
  Finish (5c59d226-9e88-44c8-aac9-b55e13a5b3b4)
 Call ID: 5c59d226-9e88-44c8-aac9-b55e13a5b3b4
  Args: