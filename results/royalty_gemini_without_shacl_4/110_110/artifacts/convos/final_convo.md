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
  AssignClass (61ffdfe1-1428-4a74-855f-6ec761cd205d)
 Call ID: 61ffdfe1-1428-4a74-855f-6ec761cd205d
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Man
  AssignClass (57c0e201-9d49-472b-b572-04afca20905a)
 Call ID: 57c0e201-9d49-472b-b572-04afca20905a
  Args:
    type: :Person
    source: Maximilian_Margrave_of_Baden
  AddLiteral (76de55ab-300d-4eef-a105-dd7b76fef5d7)
 Call ID: 76de55ab-300d-4eef-a105-dd7b76fef5d7
  Args:
    literal_value: 1933
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (c57ac550-c316-4880-a9ec-9567ef90da73)
 Call ID: c57ac550-c316-4880-a9ec-9567ef90da73
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2022
    source: Maximilian_Margrave_of_Baden
  AddLiteral (d5d05ab3-c183-4453-adcb-97c4a957baff)
 Call ID: d5d05ab3-c183-4453-adcb-97c4a957baff
  Args:
    literal_value: Max von Baden
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (95f008a1-4e06-4c9a-be96-727dc705622a)
 Call ID: 95f008a1-4e06-4c9a-be96-727dc705622a
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Man
  AssignClass (cf84efb1-109a-4f99-86a0-197b3abbcc4f)
 Call ID: cf84efb1-109a-4f99-86a0-197b3abbcc4f
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Person
  AssignClass (054ae3f8-5a7e-46a3-b64f-9f7aef7f6a8d)
 Call ID: 054ae3f8-5a7e-46a3-b64f-9f7aef7f6a8d
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Woman
  AssignClass (3e32c9c6-b021-4653-a78d-d1fa6f36bff7)
 Call ID: 3e32c9c6-b021-4653-a78d-d1fa6f36bff7
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Person
  AddTriple (a5672868-46eb-4057-8201-9f172c74d422)
 Call ID: a5672868-46eb-4057-8201-9f172c74d422
  Args:
    target: Berthold_Margrave_of_Baden
    relation: :hasFather
    source: Maximilian_Margrave_of_Baden
  AddTriple (f777e80c-950d-4e0d-94fa-acedc46ffe9f)
 Call ID: f777e80c-950d-4e0d-94fa-acedc46ffe9f
  Args:
    relation: :hasMother
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Maximilian_Margrave_of_Baden
  AssignClass (17c60651-1ac0-4e5a-b902-3895d575dfa3)
 Call ID: 17c60651-1ac0-4e5a-b902-3895d575dfa3
  Args:
    source: Princess_Margarita_of_Baden
    type: :Woman
  AssignClass (67db3add-fe5d-4a73-8dc3-7ed07aabc1b7)
 Call ID: 67db3add-fe5d-4a73-8dc3-7ed07aabc1b7
  Args:
    source: Princess_Margarita_of_Baden
    type: :Person
  AddTriple (810d628a-2fc5-432c-b3d3-e073c73e33b5)
 Call ID: 810d628a-2fc5-432c-b3d3-e073c73e33b5
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Princess_Margarita_of_Baden
    relation: :hasSister
  AssignClass (0410da30-2f81-4dfb-a7c0-7c126acedc46)
 Call ID: 0410da30-2f81-4dfb-a7c0-7c126acedc46
  Args:
    source: Prince_Ludwig_of_Baden
    type: :Man
  AssignClass (176d99e0-8359-4dfc-bb48-29f240ba67a0)
 Call ID: 176d99e0-8359-4dfc-bb48-29f240ba67a0
  Args:
    source: Prince_Ludwig_of_Baden
    type: :Person
  AddLiteral (bb4ac544-70f8-4f93-a928-a7ee3c3c0229)
 Call ID: bb4ac544-70f8-4f93-a928-a7ee3c3c0229
  Args:
    source: Prince_Ludwig_of_Baden
    literal_value: 1937
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (256a2a55-9973-437b-ad44-4eb3fe95b45d)
 Call ID: 256a2a55-9973-437b-ad44-4eb3fe95b45d
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasBrother
    target: Prince_Ludwig_of_Baden
  AssignClass (89835fab-188f-4112-bba0-a29ac4a6b65a)
 Call ID: 89835fab-188f-4112-bba0-a29ac4a6b65a
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (fd42f6b0-aff8-45ba-ba5d-74e015a13cd3)
 Call ID: fd42f6b0-aff8-45ba-ba5d-74e015a13cd3
  Args:
    type: :Person
    source: Archduchess_Valerie_of_Austria
  AddLiteral (b6cd9a1d-99b4-4c7c-93f2-8386471ef439)
 Call ID: b6cd9a1d-99b4-4c7c-93f2-8386471ef439
  Args:
    literal_value: 1941
    source: Archduchess_Valerie_of_Austria
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (94eaf111-e3ce-49f4-88c8-524df7c5160d)
 Call ID: 94eaf111-e3ce-49f4-88c8-524df7c5160d
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Maximilian_Margrave_of_Baden
    literal_value: 1966
  AddTriple (06967bbf-fef1-45f3-a401-996391dfa1fd)
 Call ID: 06967bbf-fef1-45f3-a401-996391dfa1fd
  Args:
    source: Maximilian_Margrave_of_Baden
    relation: :hasRelation
    target: Archduchess_Valerie_of_Austria
  AssignClass (e3db173b-f081-4357-9b4e-c02978cfc88a)
 Call ID: e3db173b-f081-4357-9b4e-c02978cfc88a
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Man
  AssignClass (357a9657-6bb9-4722-93b7-9cddaba7bfa3)
 Call ID: 357a9657-6bb9-4722-93b7-9cddaba7bfa3
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Person
  AssignClass (4596ea69-c787-4b1a-b8b8-f44e5a0c6180)
 Call ID: 4596ea69-c787-4b1a-b8b8-f44e5a0c6180
  Args:
    source: Princess_Rosemary_of_Salm_Salm
    type: :Woman
  AssignClass (f13034b5-050e-4605-89c9-98e218dc6297)
 Call ID: f13034b5-050e-4605-89c9-98e218dc6297
  Args:
    type: :Person
    source: Princess_Rosemary_of_Salm_Salm
  AddTriple (b3e1ae3f-de52-45e7-a878-624471cc05e5)
 Call ID: b3e1ae3f-de52-45e7-a878-624471cc05e5
  Args:
    source: Archduchess_Valerie_of_Austria
    relation: :hasFather
    target: Archduke_Hubert_Salvator_of_Austria
  AddTriple (6b639dab-9bd1-4f9a-ae41-d96c35598d9c)
 Call ID: 6b639dab-9bd1-4f9a-ae41-d96c35598d9c
  Args:
    source: Archduchess_Valerie_of_Austria
    relation: :hasMother
    target: Princess_Rosemary_of_Salm_Salm
  AssignClass (22134be9-ee69-4d1e-b4df-4606902000fb)
 Call ID: 22134be9-ee69-4d1e-b4df-4606902000fb
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Man
  AssignClass (4937719c-7ccd-4dd6-b131-e45696382b99)
 Call ID: 4937719c-7ccd-4dd6-b131-e45696382b99
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Person
  AddTriple (2f22447d-290c-4466-8e46-7a715c7fbb23)
 Call ID: 2f22447d-290c-4466-8e46-7a715c7fbb23
  Args:
    target: Bernhard_Margrave_of_Baden
    relation: :hasSon
    source: Maximilian_Margrave_of_Baden
  Finish (0424591f-0a37-45e0-8da8-2b4337499c3f)
 Call ID: 0424591f-0a37-45e0-8da8-2b4337499c3f
  Args: