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
  AssignClass (0f6642a5-d642-4b4e-bb18-e5c5e2105cc2)
 Call ID: 0f6642a5-d642-4b4e-bb18-e5c5e2105cc2
  Args:
    type: :Woman
    source: Beatrix_of_Hohenlohe-Langenburg
  AssignClass (2d14808b-9fe4-4384-8cf0-201fd3e39fce)
 Call ID: 2d14808b-9fe4-4384-8cf0-201fd3e39fce
  Args:
    type: :Person
    source: Beatrix_of_Hohenlohe-Langenburg
  AddLiteral (d8f1cfea-9784-4cc8-8a14-3975b9df4d3f)
 Call ID: d8f1cfea-9784-4cc8-8a14-3975b9df4d3f
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1936
  AddLiteral (7283f786-9f41-43db-bd74-9f749954783e)
 Call ID: 7283f786-9f41-43db-bd74-9f749954783e
  Args:
    source: Beatrix_of_Hohenlohe-Langenburg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1997
  AssignClass (35884a98-771b-4e7e-a3ed-f4c3b45bad51)
 Call ID: 35884a98-771b-4e7e-a3ed-f4c3b45bad51
  Args:
    type: :Man
    source: Gottfried_of_Hohenlohe-Langenburg
  AssignClass (bc06bb1f-99ce-4aa8-881d-e279d5e09865)
 Call ID: bc06bb1f-99ce-4aa8-881d-e279d5e09865
  Args:
    type: :Ancestor
    source: Gottfried_of_Hohenlohe-Langenburg
  AssignClass (1394ba46-eb21-4549-8a2a-ff806092dc1c)
 Call ID: 1394ba46-eb21-4549-8a2a-ff806092dc1c
  Args:
    type: :Person
    source: Gottfried_of_Hohenlohe-Langenburg
  AssignClass (e63b5450-2bf0-4b4c-b34f-0120086f2709)
 Call ID: e63b5450-2bf0-4b4c-b34f-0120086f2709
  Args:
    type: :Woman
    source: Margarita_of_Greece_and_Denmark
  AssignClass (3d2c2819-3257-411e-af17-0f7aaac21281)
 Call ID: 3d2c2819-3257-411e-af17-0f7aaac21281
  Args:
    type: :Ancestor
    source: Margarita_of_Greece_and_Denmark
  AssignClass (549a0da9-bb6c-4403-8ea0-a0716b340f72)
 Call ID: 549a0da9-bb6c-4403-8ea0-a0716b340f72
  Args:
    type: :Person
    source: Margarita_of_Greece_and_Denmark
  AddTriple (4e802e16-38ec-41bc-a1af-125b5ce274d4)
 Call ID: 4e802e16-38ec-41bc-a1af-125b5ce274d4
  Args:
    target: Gottfried_of_Hohenlohe-Langenburg
    source: Beatrix_of_Hohenlohe-Langenburg
    relation: :hasFather
  AddTriple (aca6e5ae-f7ee-4d4d-be2e-148beda9de0a)
 Call ID: aca6e5ae-f7ee-4d4d-be2e-148beda9de0a
  Args:
    target: Margarita_of_Greece_and_Denmark
    relation: :hasMother
    source: Beatrix_of_Hohenlohe-Langenburg
  AssignClass (2fc3aae7-a27c-4638-8047-91c2f6f5162a)
 Call ID: 2fc3aae7-a27c-4638-8047-91c2f6f5162a
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (bcea0af1-b668-4189-bfc9-344461d79392)
 Call ID: bcea0af1-b668-4189-bfc9-344461d79392
  Args:
    type: :Person
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (0044c449-9aff-4483-9ffa-dda8e7073c47)
 Call ID: 0044c449-9aff-4483-9ffa-dda8e7073c47
  Args:
    target: Prince_Philip_Duke_of_Edinburgh
    source: Margarita_of_Greece_and_Denmark
    relation: :isSisterOf
  AssignClass (95b89895-e130-4256-b766-09bf64d7afa1)
 Call ID: 95b89895-e130-4256-b766-09bf64d7afa1
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (4dc9f612-eb11-4cf5-9c94-637e48248954)
 Call ID: 4dc9f612-eb11-4cf5-9c94-637e48248954
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (29856089-0804-4730-9939-4a61e1dd11a1)
 Call ID: 29856089-0804-4730-9939-4a61e1dd11a1
  Args:
    type: :Woman
    source: Princess_Christina_of_Hesse
  AssignClass (62cc751f-3cf0-43ae-abe2-ef9429a6284d)
 Call ID: 62cc751f-3cf0-43ae-abe2-ef9429a6284d
  Args:
    type: :Person
    source: Princess_Christina_of_Hesse
  AssignClass (8e0102c9-f92c-422e-9b41-36b30b73081d)
 Call ID: 8e0102c9-f92c-422e-9b41-36b30b73081d
  Args:
    type: :Man
    source: Prince_Andrew_of_Yugoslavia
  AssignClass (a83e7bd6-b99a-4951-87b1-55fad2452aea)
 Call ID: a83e7bd6-b99a-4951-87b1-55fad2452aea
  Args:
    type: :Person
    source: Prince_Andrew_of_Yugoslavia
  AssignClass (bbee8159-4490-4597-8953-8bf614ef2a26)
 Call ID: bbee8159-4490-4597-8953-8bf614ef2a26
  Args:
    type: :Man
    source: Maximilian_Hereditary_Prince_of_Baden
  AssignClass (01daa026-2afc-468e-bf37-ee9f118b1431)
 Call ID: 01daa026-2afc-468e-bf37-ee9f118b1431
  Args:
    type: :Person
    source: Maximilian_Hereditary_Prince_of_Baden
  AssignClass (c37ed912-3d80-4daf-8aa9-8143e538d4f0)
 Call ID: c37ed912-3d80-4daf-8aa9-8143e538d4f0
  Args:
    type: :Woman
    source: Archduchess_Valerie_of_Austria
  AssignClass (852415aa-630d-4562-86fd-11363c32d7b5)
 Call ID: 852415aa-630d-4562-86fd-11363c32d7b5
  Args:
    type: :Person
    source: Archduchess_Valerie_of_Austria
  AddLiteral (476f4321-f678-4e0e-8478-7477c0d2105b)
 Call ID: 476f4321-f678-4e0e-8478-7477c0d2105b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Archduchess_Valerie_of_Austria
    literal_value: 1941
  AddLiteral (c4d5c823-7891-4729-a586-94cab5e2529f)
 Call ID: c4d5c823-7891-4729-a586-94cab5e2529f
  Args:
    source: Maximilian_Hereditary_Prince_of_Baden
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1966
  AddTriple (7ca39681-88f0-44ef-adba-26be573ef3b4)
 Call ID: 7ca39681-88f0-44ef-adba-26be573ef3b4
  Args:
    target: Maximilian_Hereditary_Prince_of_Baden
    source: Archduchess_Valerie_of_Austria
    relation: :hasMother
  AssignClass (c20540c8-19f6-4fa0-a704-260a9d46edc0)
 Call ID: c20540c8-19f6-4fa0-a704-260a9d46edc0
  Args:
    type: :Woman
    source: Margaret_Princess_of_Hesse_and_by_Rhine
  AssignClass (2c90c87e-a080-4070-aa58-db3ce3b08818)
 Call ID: 2c90c87e-a080-4070-aa58-db3ce3b08818
  Args:
    type: :Person
    source: Margaret_Princess_of_Hesse_and_by_Rhine
  AssignClass (230a59f1-d1b6-4b5b-81cd-4f6546f529bb)
 Call ID: 230a59f1-d1b6-4b5b-81cd-4f6546f529bb
  Args:
    type: :Woman
    source: Princess_Cecilie
  AssignClass (e6655648-b024-4745-b184-ab1ca2d3149c)
 Call ID: e6655648-b024-4745-b184-ab1ca2d3149c
  Args:
    type: :Person
    source: Princess_Cecilie
  Finish (f3233d19-5c33-4fbc-bf88-3553b0f74316)
 Call ID: f3233d19-5c33-4fbc-bf88-3553b0f74316
  Args: