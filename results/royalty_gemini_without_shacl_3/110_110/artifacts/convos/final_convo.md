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
  AssignClass (375ce1b2-870d-423f-9e49-f429ca11ca94)
 Call ID: 375ce1b2-870d-423f-9e49-f429ca11ca94
  Args:
    type: :Man
    source: Maximilian_Margrave_of_Baden
  AssignClass (da58e0ce-1562-49c4-9226-4aa32f9fe171)
 Call ID: da58e0ce-1562-49c4-9226-4aa32f9fe171
  Args:
    source: Maximilian_Margrave_of_Baden
    type: :Person
  AddLiteral (5be8da11-196c-433c-89ac-9d4acae6bcff)
 Call ID: 5be8da11-196c-433c-89ac-9d4acae6bcff
  Args:
    literal_value: 1933
    literal_type: xsd:integer
    source: Maximilian_Margrave_of_Baden
    relation: :hasBirthYear
  AddLiteral (943d56a0-47a8-4b5c-829b-bf79a0649a90)
 Call ID: 943d56a0-47a8-4b5c-829b-bf79a0649a90
  Args:
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:integer
    literal_value: 2022
    relation: :hasDeathYear
  AddLiteral (9138c487-6246-4dab-9e3c-f50714d1e1e9)
 Call ID: 9138c487-6246-4dab-9e3c-f50714d1e1e9
  Args:
    relation: :alsoKnownAs
    literal_value: Max von Baden
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:string
  AssignClass (63743aae-c34d-4c2b-9130-9ec4d4d95995)
 Call ID: 63743aae-c34d-4c2b-9130-9ec4d4d95995
  Args:
    type: :Man
    source: Berthold_Margrave_of_Baden
  AssignClass (e9237cd9-93a0-4fa8-9066-3d009ce9d58e)
 Call ID: e9237cd9-93a0-4fa8-9066-3d009ce9d58e
  Args:
    source: Berthold_Margrave_of_Baden
    type: :Person
  AddTriple (077c1996-ed51-48aa-aee4-21576b869c0b)
 Call ID: 077c1996-ed51-48aa-aee4-21576b869c0b
  Args:
    relation: :hasFather
    target: Berthold_Margrave_of_Baden
    source: Maximilian_Margrave_of_Baden
  AssignClass (483bb67c-6880-4f65-84e4-95974180ccf9)
 Call ID: 483bb67c-6880-4f65-84e4-95974180ccf9
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (5d981261-1b5a-4ad1-a1e7-316abfd7ba0f)
 Call ID: 5d981261-1b5a-4ad1-a1e7-316abfd7ba0f
  Args:
    source: Princess_Theodora_of_Greece_and_Denmark
    type: :Person
  AddTriple (ba25237d-fecc-4b0b-b291-c6cd52d0daad)
 Call ID: ba25237d-fecc-4b0b-b291-c6cd52d0daad
  Args:
    target: Princess_Theodora_of_Greece_and_Denmark
    source: Maximilian_Margrave_of_Baden
    relation: :hasMother
  AssignClass (386b39a2-d78d-4622-84ee-f5df72de71fe)
 Call ID: 386b39a2-d78d-4622-84ee-f5df72de71fe
  Args:
    source: Princess_Margarita
    type: :Woman
  AssignClass (1e4aef28-f775-489b-8a0f-dca6cc8b4c3b)
 Call ID: 1e4aef28-f775-489b-8a0f-dca6cc8b4c3b
  Args:
    type: :Person
    source: Princess_Margarita
  AddTriple (d50bf061-bbc1-4b2d-b92f-7ffae3640ced)
 Call ID: d50bf061-bbc1-4b2d-b92f-7ffae3640ced
  Args:
    target: Princess_Margarita
    source: Maximilian_Margrave_of_Baden
    relation: :hasSister
  AssignClass (018526fc-599c-4af0-82bc-639182448ae5)
 Call ID: 018526fc-599c-4af0-82bc-639182448ae5
  Args:
    source: Prince_Ludwig
    type: :Man
  AssignClass (01398390-bc51-4086-a245-5f0398b0080d)
 Call ID: 01398390-bc51-4086-a245-5f0398b0080d
  Args:
    source: Prince_Ludwig
    type: :Person
  AddTriple (301fec63-5ba7-4aa1-aeff-d25ce635d0b4)
 Call ID: 301fec63-5ba7-4aa1-aeff-d25ce635d0b4
  Args:
    target: Prince_Ludwig
    source: Maximilian_Margrave_of_Baden
    relation: :hasBrother
  AddLiteral (5c0a3e1c-7d83-48a4-996f-752fcbfbd429)
 Call ID: 5c0a3e1c-7d83-48a4-996f-752fcbfbd429
  Args:
    relation: :hasBirthYear
    literal_value: 1937
    literal_type: xsd:integer
    source: Prince_Ludwig
  AssignClass (6868d249-07b5-48b2-8f4a-0800d287dea6)
 Call ID: 6868d249-07b5-48b2-8f4a-0800d287dea6
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (f30559c6-772d-4dea-b45d-8c3887aefab8)
 Call ID: f30559c6-772d-4dea-b45d-8c3887aefab8
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Person
  AddLiteral (6bb4452f-e004-4a3f-bbe0-22c785c24457)
 Call ID: 6bb4452f-e004-4a3f-bbe0-22c785c24457
  Args:
    literal_value: 1941
    source: Archduchess_Valerie_of_Austria
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (cc7f3207-6c3f-4724-9f12-ee70a7cd09c2)
 Call ID: cc7f3207-6c3f-4724-9f12-ee70a7cd09c2
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Maximilian_Margrave_of_Baden
    literal_value: 1966
  AssignClass (9eaecede-ec42-4a28-bbc2-47344ceed681)
 Call ID: 9eaecede-ec42-4a28-bbc2-47344ceed681
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Man
  AssignClass (0cb7864b-aeb4-42f8-be08-48d6dd9b8596)
 Call ID: 0cb7864b-aeb4-42f8-be08-48d6dd9b8596
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Person
  AssignClass (e08cbea2-6f3e-4495-8430-0bfa37c9cf48)
 Call ID: e08cbea2-6f3e-4495-8430-0bfa37c9cf48
  Args:
    source: Princess_Rosemary_of_Salm-Salm
    type: :Woman
  AssignClass (f43cdc2a-c51a-4def-bbd7-537872509b14)
 Call ID: f43cdc2a-c51a-4def-bbd7-537872509b14
  Args:
    type: :Person
    source: Princess_Rosemary_of_Salm-Salm
  AddTriple (cc92ec72-1cab-4e31-b699-142c9f98b911)
 Call ID: cc92ec72-1cab-4e31-b699-142c9f98b911
  Args:
    relation: :hasFather
    source: Archduchess_Valerie_of_Austria
    target: Archduke_Hubert_Salvator_of_Austria
  AddTriple (a7685961-cc99-46a8-8d02-edff09394f1a)
 Call ID: a7685961-cc99-46a8-8d02-edff09394f1a
  Args:
    source: Archduchess_Valerie_of_Austria
    target: Princess_Rosemary_of_Salm-Salm
    relation: :hasMother
  AssignClass (5a66163e-de97-4965-87f8-7222925adf8f)
 Call ID: 5a66163e-de97-4965-87f8-7222925adf8f
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Man
  AssignClass (8501fd76-4291-45e1-90be-e257e9d1c384)
 Call ID: 8501fd76-4291-45e1-90be-e257e9d1c384
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Person
  AddTriple (65124583-4ec2-44b6-b4a7-1a2b788e76eb)
 Call ID: 65124583-4ec2-44b6-b4a7-1a2b788e76eb
  Args:
    relation: :hasSon
    source: Maximilian_Margrave_of_Baden
    target: Bernhard_Margrave_of_Baden
  Finish (e6118268-c170-4f15-9aa9-588a8b6d0912)
 Call ID: e6118268-c170-4f15-9aa9-588a8b6d0912
  Args: