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
  AssignClass (47b950ee-fbe2-4949-8fdd-912033f34385)
 Call ID: 47b950ee-fbe2-4949-8fdd-912033f34385
  Args:
    type: :Man
    source: Maximilian_Margrave_of_Baden
  AssignClass (9b33ccba-bfa5-48f6-9666-60f60fa6aff9)
 Call ID: 9b33ccba-bfa5-48f6-9666-60f60fa6aff9
  Args:
    type: :Man
    source: Berthold_Margrave_of_Baden
  AssignClass (45d4d79b-0917-4306-8f07-956c53768be2)
 Call ID: 45d4d79b-0917-4306-8f07-956c53768be2
  Args:
    type: :Woman
    source: Princess_Theodora_of_Greece_and_Denmark
  AssignClass (3dd45b5a-d9ce-474c-a8e6-364e14223d17)
 Call ID: 3dd45b5a-d9ce-474c-a8e6-364e14223d17
  Args:
    type: :Woman
    source: Princess_Margarita_of_Baden
  AssignClass (4eeb3cb2-e2f0-4445-a03a-3d98d91c18b0)
 Call ID: 4eeb3cb2-e2f0-4445-a03a-3d98d91c18b0
  Args:
    type: :Man
    source: Prince_Ludwig_of_Baden
  AssignClass (2d15e530-e692-4b41-bca7-8797159ff531)
 Call ID: 2d15e530-e692-4b41-bca7-8797159ff531
  Args:
    source: Archduchess_Valerie_of_Austria
    type: :Woman
  AssignClass (216cc4ba-24f7-4147-81d3-86cd96ee20fb)
 Call ID: 216cc4ba-24f7-4147-81d3-86cd96ee20fb
  Args:
    source: Archduke_Hubert_Salvator_of_Austria
    type: :Man
  AssignClass (d0fa7560-c114-4e4d-b227-f7f9728f59ef)
 Call ID: d0fa7560-c114-4e4d-b227-f7f9728f59ef
  Args:
    source: Princess_Rosemary_of_Salm-Salm
    type: :Woman
  AssignClass (887ab1b8-f333-458f-9b3b-7b913c3160d9)
 Call ID: 887ab1b8-f333-458f-9b3b-7b913c3160d9
  Args:
    source: Bernhard_Margrave_of_Baden
    type: :Man
  AddLiteral (93bee5dc-21f6-4081-9793-81c8039f42ec)
 Call ID: 93bee5dc-21f6-4081-9793-81c8039f42ec
  Args:
    literal_value: 1933
    relation: :hasBirthYear
    source: Maximilian_Margrave_of_Baden
    literal_type: xsd:integer
  AddLiteral (2bc17243-2a03-44b1-b4b3-034c65016846)
 Call ID: 2bc17243-2a03-44b1-b4b3-034c65016846
  Args:
    literal_type: xsd:integer
    source: Maximilian_Margrave_of_Baden
    literal_value: 2022
    relation: :hasDeathYear
  AddLiteral (fdd48440-eaa7-4d77-aa06-336ae1dc09bd)
 Call ID: fdd48440-eaa7-4d77-aa06-336ae1dc09bd
  Args:
    relation: :alsoKnownAs
    literal_value: Max von Baden
    literal_type: xsd:string
    source: Maximilian_Margrave_of_Baden
  AddTriple (8d2fd57a-30cc-43f9-a867-e925d26d2a2d)
 Call ID: 8d2fd57a-30cc-43f9-a867-e925d26d2a2d
  Args:
    source: Maximilian_Margrave_of_Baden
    target: Berthold_Margrave_of_Baden
    relation: :hasFather
  AddTriple (a752fa1f-4873-4110-bf7a-da6a577f25c1)
 Call ID: a752fa1f-4873-4110-bf7a-da6a577f25c1
  Args:
    target: Princess_Theodora_of_Greece_and_Denmark
    relation: :hasMother
    source: Maximilian_Margrave_of_Baden
  AddTriple (01053cef-55d5-4fa5-b399-591ef821cc4d)
 Call ID: 01053cef-55d5-4fa5-b399-591ef821cc4d
  Args:
    target: Princess_Margarita_of_Baden
    relation: :hasSister
    source: Maximilian_Margrave_of_Baden
  AddTriple (1368d731-96f6-4249-b0ac-f007b9c32a95)
 Call ID: 1368d731-96f6-4249-b0ac-f007b9c32a95
  Args:
    relation: :hasBrother
    target: Prince_Ludwig_of_Baden
    source: Maximilian_Margrave_of_Baden
  AddLiteral (b9ba1b6e-c8e4-44ad-8024-a06ac03c6873)
 Call ID: b9ba1b6e-c8e4-44ad-8024-a06ac03c6873
  Args:
    literal_value: 1937
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Ludwig_of_Baden
  AddTriple (a106b5c4-718d-43ed-9ebf-a022ef5bb570)
 Call ID: a106b5c4-718d-43ed-9ebf-a022ef5bb570
  Args:
    source: Archduchess_Valerie_of_Austria
    relation: :hasFather
    target: Archduke_Hubert_Salvator_of_Austria
  AddTriple (b853379b-6b03-4b03-9853-9ef9567f45d7)
 Call ID: b853379b-6b03-4b03-9853-9ef9567f45d7
  Args:
    target: Princess_Rosemary_of_Salm-Salm
    relation: :hasMother
    source: Archduchess_Valerie_of_Austria
  AddLiteral (4cfc8beb-ca18-48ae-8606-08c695dcc3e0)
 Call ID: 4cfc8beb-ca18-48ae-8606-08c695dcc3e0
  Args:
    source: Archduchess_Valerie_of_Austria
    literal_type: xsd:integer
    literal_value: 1941
    relation: :hasBirthYear
  AddTriple (b0e69f99-1dde-4c4b-bdd4-0bfcdcf3db52)
 Call ID: b0e69f99-1dde-4c4b-bdd4-0bfcdcf3db52
  Args:
    relation: :hasFather
    target: Maximilian_Margrave_of_Baden
    source: Bernhard_Margrave_of_Baden
  AddTriple (e227941c-9841-4238-8666-222ee5f5e48e)
 Call ID: e227941c-9841-4238-8666-222ee5f5e48e
  Args:
    target: Archduchess_Valerie_of_Austria
    relation: :hasMother
    source: Bernhard_Margrave_of_Baden
  AddLiteral (0232a317-4303-44f3-930b-301310f1c408)
 Call ID: 0232a317-4303-44f3-930b-301310f1c408
  Args:
    literal_type: xsd:integer
    source: Maximilian_Margrave_of_Baden
    literal_value: 1966
    relation: :hasMarriageYear
  Finish (3f77f8bf-2de0-438e-8198-1cc619a703c7)
 Call ID: 3f77f8bf-2de0-438e-8198-1cc619a703c7
  Args: