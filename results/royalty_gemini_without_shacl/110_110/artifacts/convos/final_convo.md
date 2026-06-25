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
  AssignClass (4e85fa4b-a650-4f24-b3f1-02dadada603d)
 Call ID: 4e85fa4b-a650-4f24-b3f1-02dadada603d
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Man
  AssignClass (d20c8fcd-9f5f-404b-8878-074817e63c54)
 Call ID: d20c8fcd-9f5f-404b-8878-074817e63c54
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Person
  AddLiteral (3b5ee7c5-ef3b-4215-9e40-06d1f5bbfdd6)
 Call ID: 3b5ee7c5-ef3b-4215-9e40-06d1f5bbfdd6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1933
    source: Maximilian_Margrave_of_Baden
  AddLiteral (27f1212c-7ecf-4f7e-adfd-7c0b671b08eb)
 Call ID: 27f1212c-7ecf-4f7e-adfd-7c0b671b08eb
  Args:
    source: Maximilian_Margrave_of_Baden
    literal_value: 2022
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (a53c2372-a9a1-40aa-b426-c370ec736716)
 Call ID: a53c2372-a9a1-40aa-b426-c370ec736716
  Args:
    literal_value: Max von Baden
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (a889c61f-0702-42f5-9042-0d9475ea9432)
 Call ID: a889c61f-0702-42f5-9042-0d9475ea9432
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Man
  AssignClass (0f7a52d1-52ff-4b2b-961f-280157a46b90)
 Call ID: 0f7a52d1-52ff-4b2b-961f-280157a46b90
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Person
  AssignClass (36bb7bdd-c7d5-405f-99ef-6ba422a223d0)
 Call ID: 36bb7bdd-c7d5-405f-99ef-6ba422a223d0
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (239e8ee5-d63e-4c96-b862-7cae73ff55ec)
 Call ID: 239e8ee5-d63e-4c96-b862-7cae73ff55ec
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Person
  AddTriple (873ba6e6-3d59-45a8-a6ba-c7a5936c20fc)
 Call ID: 873ba6e6-3d59-45a8-a6ba-c7a5936c20fc
  Args:
    target: Berthold_Margrave_of_Baden
    source: Maximilian_Margrave_of_Baden
    relation: :hasFather
  AddTriple (6bc588ec-ca87-49d8-8cb6-e574c438df38)
 Call ID: 6bc588ec-ca87-49d8-8cb6-e574c438df38
  Args:
    relation: :hasMother
    source: Maximilian_Margrave_of_Baden
    target: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (aee87283-d0c8-46ae-acfe-65f4290d63a6)
 Call ID: aee87283-d0c8-46ae-acfe-65f4290d63a6
  Args:
    type: :Woman
    source: Princess_Margarita
  AssignClass (0fd52c75-5a12-4a77-a2a0-dfeb356f5f36)
 Call ID: 0fd52c75-5a12-4a77-a2a0-dfeb356f5f36
  Args:
    source: Princess_Margarita
    type: :Person
  AddTriple (5d2efe47-e370-4aed-a519-fc73fb113c49)
 Call ID: 5d2efe47-e370-4aed-a519-fc73fb113c49
  Args:
    relation: :hasSister
    source: Maximilian_Margrave_of_Baden
    target: Princess_Margarita
  AssignClass (937e81ea-4df1-4a49-8a23-9df43407cebd)
 Call ID: 937e81ea-4df1-4a49-8a23-9df43407cebd
  Args:
    source: Prince_Ludwig
    type: :Man
  AssignClass (99beb4c3-4b33-4498-99c5-174cf702b4d1)
 Call ID: 99beb4c3-4b33-4498-99c5-174cf702b4d1
  Args:
    source: Prince_Ludwig
    type: :Person
  AddLiteral (27ef12d1-b1c5-430b-a080-509d57e26839)
 Call ID: 27ef12d1-b1c5-430b-a080-509d57e26839
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1937
    source: Prince_Ludwig
  AddTriple (6403d341-5fd9-440c-b2cf-1fd13bed2624)
 Call ID: 6403d341-5fd9-440c-b2cf-1fd13bed2624
  Args:
    target: Prince_Ludwig
    source: Maximilian_Margrave_of_Baden
    relation: :hasBrother
  AssignClass (50701420-78c5-48bd-809e-f50ac2ddc7b7)
 Call ID: 50701420-78c5-48bd-809e-f50ac2ddc7b7
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (863ca1aa-a808-4a57-9758-df2c698e4011)
 Call ID: 863ca1aa-a808-4a57-9758-df2c698e4011
  Args:
    type: :Person
    source: Archduchess_Valerie_of_Austria
  AddLiteral (7d743aff-2383-4163-b6d3-d6654af5b03f)
 Call ID: 7d743aff-2383-4163-b6d3-d6654af5b03f
  Args:
    literal_value: 1941
    source: Archduchess_Valerie_of_Austria
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (ab02b96f-33ef-47ca-a5d2-339a2c973ec0)
 Call ID: ab02b96f-33ef-47ca-a5d2-339a2c973ec0
  Args:
    literal_value: 1966
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (1ab6f3b6-c5a3-4850-a085-7f6980f67822)
 Call ID: 1ab6f3b6-c5a3-4850-a085-7f6980f67822
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Archduchess_Valerie_of_Austria
    relation: :hasRelation
  AssignClass (7596457f-4a93-40d4-b182-0ad4cbd9fc65)
 Call ID: 7596457f-4a93-40d4-b182-0ad4cbd9fc65
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Man
  AssignClass (237c54cb-c554-4564-8dc5-e7c236026b2f)
 Call ID: 237c54cb-c554-4564-8dc5-e7c236026b2f
  Args:
    type: :Person
    source: Bernhard_Margrave_of_Baden
  AddTriple (bbfe9c93-0030-47e4-8caf-48156e451132)
 Call ID: bbfe9c93-0030-47e4-8caf-48156e451132
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Bernhard_Margrave_of_Baden
    relation: :hasSon
  AssignClass (9947b753-651b-472c-b541-1bcf482d926c)
 Call ID: 9947b753-651b-472c-b541-1bcf482d926c
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (4a969517-0d41-4a78-909b-f501f5389f25)
 Call ID: 4a969517-0d41-4a78-909b-f501f5389f25
  Args:
    source: Prince_Philip_Duke_of_Edinburgh
    type: :Person
  AddTriple (5a86080e-ad53-4cf6-8014-bd3faa489316)
 Call ID: 5a86080e-ad53-4cf6-8014-bd3faa489316
  Args:
    relation: :hasSister
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Prince_Philip_Duke_of_Edinburgh
  AssignClass (86d9454f-676d-4a97-9b8a-fbe91053cfeb)
 Call ID: 86d9454f-676d-4a97-9b8a-fbe91053cfeb
  Args:
    source: Charles_III_King_of_the_United_Kingdom
    type: :Man
  AssignClass (4269a380-ab8d-4923-bcd7-7f1cb8a3b238)
 Call ID: 4269a380-ab8d-4923-bcd7-7f1cb8a3b238
  Args:
    source: Charles_III_King_of_the_United_Kingdom
    type: :Person
  AssignClass (ef9aec6f-ad8d-487f-93a1-0e41495d9148)
 Call ID: ef9aec6f-ad8d-487f-93a1-0e41495d9148
  Args:
    type: :Woman
    source: Margarita_Princess_of_Hohenlohe_Langenburg
  AssignClass (f5a7be4f-cfa9-4129-8390-a11fda6869fa)
 Call ID: f5a7be4f-cfa9-4129-8390-a11fda6869fa
  Args:
    source: Margarita_Princess_of_Hohenlohe_Langenburg
    type: :Person
  AssignClass (95fd3215-2fe9-41db-952c-0504c31df0a8)
 Call ID: 95fd3215-2fe9-41db-952c-0504c31df0a8
  Args:
    type: :Woman
    source: Princess_Beatrix_of_Hohenlohe_Langenburg
  AssignClass (e397015a-d25f-405f-9813-cdbb01b6f093)
 Call ID: e397015a-d25f-405f-9813-cdbb01b6f093
  Args:
    source: Princess_Beatrix_of_Hohenlohe_Langenburg
    type: :Person
  AddTriple (b5936abc-323c-4312-8eec-a56b817a85f3)
 Call ID: b5936abc-323c-4312-8eec-a56b817a85f3
  Args:
    target: Margarita_Princess_of_Hohenlohe_Langenburg
    source: Princess_Beatrix_of_Hohenlohe_Langenburg
    relation: :hasMother
  AddTriple (6dff8680-3ff6-4b6d-86ec-dfe6ebc6df7b)
 Call ID: 6dff8680-3ff6-4b6d-86ec-dfe6ebc6df7b
  Args:
    source: Archduchess_Valerie_of_Austria
    target: Archduke_Hubert_Salvator_of_Austria
    relation: :hasFather
  AssignClass (dbef654b-f9b7-4866-a158-35703e9c642e)
 Call ID: dbef654b-f9b7-4866-a158-35703e9c642e
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Man
  AssignClass (d844541a-58c5-422e-9912-83c8ef9014f1)
 Call ID: d844541a-58c5-422e-9912-83c8ef9014f1
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Person
  AddTriple (c3036b33-d941-4ea3-9b8f-748b2a6c3bb7)
 Call ID: c3036b33-d941-4ea3-9b8f-748b2a6c3bb7
  Args:
    relation: :hasMother
    target: Princess_Rosemary_of_Salm_Salm
    source: Archduchess_Valerie_of_Austria
  AssignClass (7270738c-86d1-4200-800a-1bc5679a65bd)
 Call ID: 7270738c-86d1-4200-800a-1bc5679a65bd
  Args:
    source: Princess_Rosemary_of_Salm_Salm
    type: :Woman
  AssignClass (4b78e1ec-d5d2-4cd3-9462-624df028e5f2)
 Call ID: 4b78e1ec-d5d2-4cd3-9462-624df028e5f2
  Args:
    source: Princess_Rosemary_of_Salm_Salm
    type: :Person
  Finish (e9671578-5c0e-40f7-8414-7b134df825aa)
 Call ID: e9671578-5c0e-40f7-8414-7b134df825aa
  Args: