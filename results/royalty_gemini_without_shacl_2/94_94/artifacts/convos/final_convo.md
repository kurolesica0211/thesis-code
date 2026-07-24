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
Wilhelm Herzog von Württemberg (born Wilhelm Friedrich Carl Philipp Albert Nikolaus Erich Maria; 13 August 1994) is the head of the House of Württemberg and a German businessman.
He is Chair of the Hofkammer des Hauses Württemberg, the company which manages the forests, farms, wineries, and housing estates of the former royal family of the Kingdom of Württemberg.
Life

Wilhelm is the eldest child of Friedrich, Hereditary Duke of Württemberg (1961–2018) and Princess Marie Wilhelmine of Wied (born 1973).
He was baptised in September 1994,  with his uncles Erich, Prince of Waldburg zu Zeil und Trauchburg, and Prince Wilhelm of Wied, as his godfathers.
On 9 May 2018, Wilhelm's father died in a car accident while driving on his way home to Friedrichshafen.
Upon the death of his father, Wilhelm became the heir apparent to his grandfather, Carl, Duke of Württemberg as Head of the House of Württemberg.
In July 2019, it was also announced that Wilhelm would be the future head of the Württemberg Hofkammer, the administrative offices of the family business.
On 7 June 2022, Wilhelm succeeded as Head of the House of Württemberg upon the death of his grandfather, Carl, Duke of Württemberg.
Wilhelm is unmarried.
With the headship of the house passing through the male line, the heir presumptive of the House of Württemberg is Wilhelm's paternal uncle Duke Eberhard of Württemberg, who married Gaby Maier on 15 July 2023.



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
  AssignClass (78e82ef5-cf59-4e00-9e68-a670bf9f665f)
 Call ID: 78e82ef5-cf59-4e00-9e68-a670bf9f665f
  Args:
    source: Wilhelm_Herzog_von_Württemberg
    type: :Man
  AssignClass (3887b260-812d-43eb-b26f-f0b104d7539f)
 Call ID: 3887b260-812d-43eb-b26f-f0b104d7539f
  Args:
    type: :Person
    source: Wilhelm_Herzog_von_Württemberg
  AddLiteral (5302f7ad-aac7-4073-8605-ab56d5c70508)
 Call ID: 5302f7ad-aac7-4073-8605-ab56d5c70508
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1994
    source: Wilhelm_Herzog_von_Württemberg
  AssignClass (22d81dc5-b8d5-4bfb-9401-8cd7d491206b)
 Call ID: 22d81dc5-b8d5-4bfb-9401-8cd7d491206b
  Args:
    type: :Man
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AssignClass (3e45d524-0b70-4f50-a758-520b4ab72abf)
 Call ID: 3e45d524-0b70-4f50-a758-520b4ab72abf
  Args:
    type: :Person
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AddLiteral (e8c245a2-d440-4ed6-b717-baff7234e943)
 Call ID: e8c245a2-d440-4ed6-b717-baff7234e943
  Args:
    source: Friedrich_Hereditary_Duke_of_Württemberg
    literal_value: 1961
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (5ae74ffa-b8fb-4fd9-bae0-0a62bb5bfb29)
 Call ID: 5ae74ffa-b8fb-4fd9-bae0-0a62bb5bfb29
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2018
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AssignClass (8b5b42a2-8f3e-42fe-bbd0-b5f0a8ef522c)
 Call ID: 8b5b42a2-8f3e-42fe-bbd0-b5f0a8ef522c
  Args:
    type: :Woman
    source: Princess_Marie_Wilhelmine_of_Wied
  AssignClass (95abd974-aa62-4628-876a-f53d385f5453)
 Call ID: 95abd974-aa62-4628-876a-f53d385f5453
  Args:
    source: Princess_Marie_Wilhelmine_of_Wied
    type: :Person
  AddLiteral (ad601cda-0280-4222-9266-2b277bb59624)
 Call ID: ad601cda-0280-4222-9266-2b277bb59624
  Args:
    source: Princess_Marie_Wilhelmine_of_Wied
    literal_value: 1973
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (870efc45-0f39-4281-9a18-7cc56cfa709f)
 Call ID: 870efc45-0f39-4281-9a18-7cc56cfa709f
  Args:
    relation: :hasFather
    source: Wilhelm_Herzog_von_Württemberg
    target: Friedrich_Hereditary_Duke_of_Württemberg
  AddTriple (fff719ed-d479-4da8-8f83-3809d7695104)
 Call ID: fff719ed-d479-4da8-8f83-3809d7695104
  Args:
    relation: :hasMother
    source: Wilhelm_Herzog_von_Württemberg
    target: Princess_Marie_Wilhelmine_of_Wied
  AssignClass (625490fb-9d2b-40c8-8972-e8c35775bbd7)
 Call ID: 625490fb-9d2b-40c8-8972-e8c35775bbd7
  Args:
    type: :Man
    source: Carl_Duke_of_Württemberg
  AssignClass (eddbb17e-bcc4-43fc-b944-436be8c31bf2)
 Call ID: eddbb17e-bcc4-43fc-b944-436be8c31bf2
  Args:
    source: Carl_Duke_of_Württemberg
    type: :Person
  AddTriple (d7fa2423-4ad1-45cb-b373-29451d69cdc1)
 Call ID: d7fa2423-4ad1-45cb-b373-29451d69cdc1
  Args:
    source: Friedrich_Hereditary_Duke_of_Württemberg
    target: Carl_Duke_of_Württemberg
    relation: :hasFather
  AddLiteral (bd3fe50a-d827-490f-ae2e-5db6cc6c1d5b)
 Call ID: bd3fe50a-d827-490f-ae2e-5db6cc6c1d5b
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Carl_Duke_of_Württemberg
    literal_value: 2022
  AssignClass (ac3723fa-859d-476c-81ae-32c0d964c4ae)
 Call ID: ac3723fa-859d-476c-81ae-32c0d964c4ae
  Args:
    source: Duke_Eberhard_of_Württemberg
    type: :Man
  AssignClass (4d4c0757-cf2d-4334-8030-154ab766a7f4)
 Call ID: 4d4c0757-cf2d-4334-8030-154ab766a7f4
  Args:
    type: :Person
    source: Duke_Eberhard_of_Württemberg
  AddTriple (4f20e406-bf0b-4b30-b491-4811125b582d)
 Call ID: 4f20e406-bf0b-4b30-b491-4811125b582d
  Args:
    relation: :hasFather
    target: Carl_Duke_of_Württemberg
    source: Duke_Eberhard_of_Württemberg
  AssignClass (0bd11f79-9b17-4119-ac29-bb2187e2703c)
 Call ID: 0bd11f79-9b17-4119-ac29-bb2187e2703c
  Args:
    source: Gaby_Maier
    type: :Woman
  AssignClass (00015a39-1876-424f-a22b-f602a35019ce)
 Call ID: 00015a39-1876-424f-a22b-f602a35019ce
  Args:
    source: Gaby_Maier
    type: :Person
  AddTriple (98b1da84-9a81-42fa-95be-069d0ba94bb9)
 Call ID: 98b1da84-9a81-42fa-95be-069d0ba94bb9
  Args:
    relation: :hasRelation
    target: Gaby_Maier
    source: Duke_Eberhard_of_Württemberg
  AddLiteral (c7fe7eb7-5801-4e49-8da6-0efbce0d9f71)
 Call ID: c7fe7eb7-5801-4e49-8da6-0efbce0d9f71
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2023
    source: Duke_Eberhard_of_Württemberg
  Finish (f7a33666-16f6-40c9-93b0-be56b208c948)
 Call ID: f7a33666-16f6-40c9-93b0-be56b208c948
  Args: