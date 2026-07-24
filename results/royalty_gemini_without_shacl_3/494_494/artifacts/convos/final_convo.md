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
Bernhard Prinz und Markgraf von Baden (born 27 May 1970), styled Margrave of Baden and Duke of Zähringen, is the head of the House of Baden since 29 December 2022 following the death of his father, Maximilian.
Early life and family

Bernhard was born at Schloss Salem in Salem, Baden-Württemberg, on 27 May 1970.
He is the eldest son of Maximilian, Margrave of Baden, and Archduchess Valerie of Austria (born 1941) and was styled as the heir of his father, Hereditary Prince of Baden.
His paternal grandparents were Berthold, Margrave of Baden, and Princess Theodora of Greece and Denmark, who was a sister of Prince Philip, Duke of Edinburgh.
His maternal grandparents were Archduke Hubert Salvator of Austria and Princess Rosemary of Salm-Salm.
Prince Bernhard manages the family estates, including Staufenberg Castle, and the margravial wineries dedicated to preserving the grape variety Müller-Thurgau.
Bernhard has close relations with the British royal family, and his granduncle, Prince Philip, Duke of Edinburgh, often came to Germany to shoot with the Baden family.
On 17 April 2021, Bernhard was one of only thirty mourners at Prince Philip's ceremonial funeral at St George's Chapel, Windsor Castle.
Bernhard, along with his cousins Philipp, Prince of Hohenlohe-Langenburg, and Donatus, Landgrave of Hesse, was chosen to represent the families of the Duke's late sisters who had been prevented from attending his wedding in 1947.
Bernhard and his wife and siblings later attended a service of thanksgiving for Prince Philip's life at Westminster Abbey on 29 March 2022.
On 30 March 2023, he and his wife attended a state banquet given by Frank-Walter Steinmeier, President of Germany, at Bellevue Palace during King Charles III and Queen Camilla's state visit to Germany.
On 29 December 2022, his father, Maximilian, died and Bernhard became head of the former grand ducal house of Baden.
Though royal and noble titles were abolished in Germany in 1919 when the Weimar Republic was proclaimed, he is sometimes styled and titled His Royal Highness The Margrave of Baden, Duke of Zähringen, by courtesy.
Prior to this, he was styled and titled His Grand Ducal Highness Hereditary Prince of Baden.
On 24 April 2025 the Margrave attended the funeral of Andreas, Prince of Saxe-Coburg and Gotha as the representative of Charles III.
Marriage and children

Bernhard married Stephanie Anne Kaul (born 27 June 1966), daughter of Christian Kaul and Hannelore Scheel, in a civil ceremony on 22 June 2001 and a religious ceremony the following day at Schloss Salem.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (ab48f690-e8ce-4b6d-925b-e2bc192b0fa1)
 Call ID: ab48f690-e8ce-4b6d-925b-e2bc192b0fa1
  Args:
    type: :Man
    source: :Bernhard
  AssignClass (b8e99033-41c5-42fb-8002-7e7606c7e331)
 Call ID: b8e99033-41c5-42fb-8002-7e7606c7e331
  Args:
    source: :Bernhard
    type: :Person
  AddLiteral (2ad45867-7a84-4959-b33c-122143a3df26)
 Call ID: 2ad45867-7a84-4959-b33c-122143a3df26
  Args:
    source: :Bernhard
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1970
  AssignClass (d785314f-7776-456e-b8ee-964cad654a23)
 Call ID: d785314f-7776-456e-b8ee-964cad654a23
  Args:
    source: :Maximilian
    type: :Man
  AssignClass (97e81647-5d77-46b3-a2f4-34fa61960b9e)
 Call ID: 97e81647-5d77-46b3-a2f4-34fa61960b9e
  Args:
    source: :Maximilian
    type: :Person
  AddTriple (59960b8f-6679-44f9-bfa3-689eb53d99d9)
 Call ID: 59960b8f-6679-44f9-bfa3-689eb53d99d9
  Args:
    target: :Maximilian
    relation: :hasFather
    source: :Bernhard
  AssignClass (3c9a3a93-cec1-42b0-a1af-734b9a2aa068)
 Call ID: 3c9a3a93-cec1-42b0-a1af-734b9a2aa068
  Args:
    source: :Valerie
    type: :Woman
  AssignClass (ef0c536b-7d6e-4bd6-8091-79238912338a)
 Call ID: ef0c536b-7d6e-4bd6-8091-79238912338a
  Args:
    source: :Valerie
    type: :Person
  AddLiteral (3e987af7-c640-45e8-b4aa-d389b25a30b3)
 Call ID: 3e987af7-c640-45e8-b4aa-d389b25a30b3
  Args:
    source: :Valerie
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1941
  AddTriple (27d5a770-bf6f-48af-93e5-eb02754eb847)
 Call ID: 27d5a770-bf6f-48af-93e5-eb02754eb847
  Args:
    target: :Valerie
    source: :Bernhard
    relation: :hasMother
  AssignClass (9fa72540-a7be-4eb1-9c26-bd1196e9b713)
 Call ID: 9fa72540-a7be-4eb1-9c26-bd1196e9b713
  Args:
    source: :Berthold
    type: :Man
  AssignClass (76957ed1-5c47-4fdf-98ec-17b3117d0fab)
 Call ID: 76957ed1-5c47-4fdf-98ec-17b3117d0fab
  Args:
    type: :Person
    source: :Berthold
  AddTriple (35098429-1ac0-405a-8e7c-616ef216828d)
 Call ID: 35098429-1ac0-405a-8e7c-616ef216828d
  Args:
    target: :Berthold
    source: :Maximilian
    relation: :hasFather
  AssignClass (01cc4008-926a-4827-b59f-13027b41626f)
 Call ID: 01cc4008-926a-4827-b59f-13027b41626f
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (dce2fb86-334e-429e-b483-1e681d9d5ad1)
 Call ID: dce2fb86-334e-429e-b483-1e681d9d5ad1
  Args:
    type: :Person
    source: :Theodora
  AddTriple (6464b996-b50e-413b-81f9-50f439efb569)
 Call ID: 6464b996-b50e-413b-81f9-50f439efb569
  Args:
    source: :Maximilian
    relation: :hasMother
    target: :Theodora
  AssignClass (69c9b334-f240-488d-9679-7d6de430a0b3)
 Call ID: 69c9b334-f240-488d-9679-7d6de430a0b3
  Args:
    type: :Man
    source: :HubertSalvator
  AssignClass (bef525c6-3d85-4791-8761-7a871cc4c1e9)
 Call ID: bef525c6-3d85-4791-8761-7a871cc4c1e9
  Args:
    type: :Person
    source: :HubertSalvator
  AddTriple (ce22d8db-9489-4183-a545-a9b9edf2c871)
 Call ID: ce22d8db-9489-4183-a545-a9b9edf2c871
  Args:
    source: :Valerie
    relation: :hasFather
    target: :HubertSalvator
  AssignClass (88c900af-2b67-4474-8dc8-e6652cbd4da9)
 Call ID: 88c900af-2b67-4474-8dc8-e6652cbd4da9
  Args:
    type: :Woman
    source: :RosemaryOfSalmSalm
  AssignClass (09702ab5-414a-4158-911a-69ea6ccbdd14)
 Call ID: 09702ab5-414a-4158-911a-69ea6ccbdd14
  Args:
    type: :Person
    source: :RosemaryOfSalmSalm
  AddTriple (ddb41d58-dcf5-47d1-9f2e-04388046ac9f)
 Call ID: ddb41d58-dcf5-47d1-9f2e-04388046ac9f
  Args:
    target: :RosemaryOfSalmSalm
    relation: :hasMother
    source: :Valerie
  AssignClass (9a905995-124a-4052-a56e-7a8326557afb)
 Call ID: 9a905995-124a-4052-a56e-7a8326557afb
  Args:
    type: :Woman
    source: :StephanieAnneKaul
  AssignClass (6df6252d-e79c-4684-a294-3c0a4242dc4f)
 Call ID: 6df6252d-e79c-4684-a294-3c0a4242dc4f
  Args:
    source: :StephanieAnneKaul
    type: :Person
  AddLiteral (665bd6da-54f2-4ece-9f6f-1225c56fe528)
 Call ID: 665bd6da-54f2-4ece-9f6f-1225c56fe528
  Args:
    literal_value: 1966
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :StephanieAnneKaul
  AddTriple (04183fab-5699-4985-8343-d2eeee6a9bd2)
 Call ID: 04183fab-5699-4985-8343-d2eeee6a9bd2
  Args:
    target: :StephanieAnneKaul
    source: :Bernhard
    relation: :hasRelation
  AddLiteral (41d6edc8-7427-4dbe-a502-5e851be41446)
 Call ID: 41d6edc8-7427-4dbe-a502-5e851be41446
  Args:
    source: :Bernhard
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2001
  AssignClass (4288c1a1-b1cc-4bd7-8cce-89de7cfdee2b)
 Call ID: 4288c1a1-b1cc-4bd7-8cce-89de7cfdee2b
  Args:
    source: :ChristianKaul
    type: :Man
  AssignClass (41d3fbbc-9938-46b3-9c99-f35e1a6a1147)
 Call ID: 41d3fbbc-9938-46b3-9c99-f35e1a6a1147
  Args:
    type: :Person
    source: :ChristianKaul
  AddTriple (cae917db-18b1-4c2c-af90-93f320fb6f1a)
 Call ID: cae917db-18b1-4c2c-af90-93f320fb6f1a
  Args:
    relation: :hasFather
    source: :StephanieAnneKaul
    target: :ChristianKaul
  AssignClass (7d037f51-b0f3-4e68-be71-9ee7e1e374e2)
 Call ID: 7d037f51-b0f3-4e68-be71-9ee7e1e374e2
  Args:
    type: :Woman
    source: :HanneloreScheel
  AssignClass (fa23dea9-5710-406c-8126-a3fee802eac8)
 Call ID: fa23dea9-5710-406c-8126-a3fee802eac8
  Args:
    type: :Person
    source: :HanneloreScheel
  AddTriple (cffbaa20-21cc-4441-914f-302c1815ef1e)
 Call ID: cffbaa20-21cc-4441-914f-302c1815ef1e
  Args:
    source: :StephanieAnneKaul
    relation: :hasMother
    target: :HanneloreScheel
  AddLiteral (f5f74897-9567-49e0-a934-bf7435fb8380)
 Call ID: f5f74897-9567-49e0-a934-bf7435fb8380
  Args:
    literal_value: 2022
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Maximilian
  Finish (76459114-d411-45aa-9088-00b530006620)
 Call ID: 76459114-d411-45aa-9088-00b530006620
  Args: