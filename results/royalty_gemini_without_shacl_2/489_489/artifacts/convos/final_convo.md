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
Wilhelm Karl Adalbert Erich Detloff Prinz von Preussen (30 January 1922 in Potsdam – 9 April 2007 in Holzminden) was the third son of Prince Oskar of Prussia, and the last surviving grandson of Wilhelm II, the last German Emperor.
Biography

Wilhelm-Karl was the youngest of Prince Oskar of Prussia and Countess Ina Marie von Bassewitz's four children.
Wilhelm-Karl worked tirelessly to keep the Order intact during the Cold War and helped to reunite its membership after the fall of East Germany.
Amongst other orders and awards, Wilhelm-Karl received the Grand Merit Cross (with star) of the Order of Merit of the Federal Republic of Germany and the Grand Cross of the Order pro merito Melitensi of the Sovereign Military Order of Malta.
Marriage and issue

In 1952, Wilhelm-Karl married Armgard Else Helene von Veltheim (17 February 1926 - 1 November 2019), daughter of Friedrich von Veltheim (1881–1955) and his wife, Ottonie von Alvensleben (1883–1960).



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
  AssignClass (e854263c-999f-42b9-8af6-04dc9d8d709e)
 Call ID: e854263c-999f-42b9-8af6-04dc9d8d709e
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    type: :Man
  AssignClass (bf2824c9-a1f8-4c3a-9b13-1e849e73af36)
 Call ID: bf2824c9-a1f8-4c3a-9b13-1e849e73af36
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    type: :Person
  AddLiteral (f9d4b0b4-e684-419c-b19d-e417d1ca41ff)
 Call ID: f9d4b0b4-e684-419c-b19d-e417d1ca41ff
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    literal_value: 1922
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (4d317258-e3a0-40b6-9452-1878901227f6)
 Call ID: 4d317258-e3a0-40b6-9452-1878901227f6
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    literal_value: 2007
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (fa275e60-a5c4-4906-a65c-f1586bdc0bdd)
 Call ID: fa275e60-a5c4-4906-a65c-f1586bdc0bdd
  Args:
    source: Oskar_of_Prussia
    type: :Man
  AssignClass (e6995bf7-4f0d-465d-9f10-e38d48e45eda)
 Call ID: e6995bf7-4f0d-465d-9f10-e38d48e45eda
  Args:
    type: :Person
    source: Oskar_of_Prussia
  AssignClass (8df813a0-7689-4b2d-adbd-1b64b861c4a1)
 Call ID: 8df813a0-7689-4b2d-adbd-1b64b861c4a1
  Args:
    type: :Woman
    source: Ina_Marie_von_Bassewitz
  AssignClass (c90b84c8-55dd-4a40-9737-72b695999085)
 Call ID: c90b84c8-55dd-4a40-9737-72b695999085
  Args:
    source: Ina_Marie_von_Bassewitz
    type: :Person
  AddTriple (0507567e-e19d-486f-aa92-9df45c508532)
 Call ID: 0507567e-e19d-486f-aa92-9df45c508532
  Args:
    relation: :hasFather
    target: Oskar_of_Prussia
    source: Wilhelm_Karl_Prinz_von_Preussen
  AddTriple (651f3ed4-4459-4be3-b48e-9bc11e6781c5)
 Call ID: 651f3ed4-4459-4be3-b48e-9bc11e6781c5
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    target: Ina_Marie_von_Bassewitz
    relation: :hasMother
  AssignClass (7635abe5-c7e9-45ea-9104-af445bc6f630)
 Call ID: 7635abe5-c7e9-45ea-9104-af445bc6f630
  Args:
    type: :Woman
    source: Armgard_Else_Helene_von_Veltheim
  AssignClass (83c32868-6850-4e71-9258-a33bebe6a89f)
 Call ID: 83c32868-6850-4e71-9258-a33bebe6a89f
  Args:
    type: :Person
    source: Armgard_Else_Helene_von_Veltheim
  AddLiteral (017d09f0-5e6e-4e49-a67f-4dd9341023ff)
 Call ID: 017d09f0-5e6e-4e49-a67f-4dd9341023ff
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1952
    source: Wilhelm_Karl_Prinz_von_Preussen
  AddTriple (570e5e9e-ee97-4cbb-ad57-22bdeaae1167)
 Call ID: 570e5e9e-ee97-4cbb-ad57-22bdeaae1167
  Args:
    source: Wilhelm_Karl_Prinz_von_Preussen
    target: Armgard_Else_Helene_von_Veltheim
    relation: :hasRelation
  AddLiteral (469a2be1-bcc7-47d9-8a40-930613a9df08)
 Call ID: 469a2be1-bcc7-47d9-8a40-930613a9df08
  Args:
    source: Armgard_Else_Helene_von_Veltheim
    literal_value: 1926
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (184cd55a-539f-4b3f-8ff2-48a172f78460)
 Call ID: 184cd55a-539f-4b3f-8ff2-48a172f78460
  Args:
    source: Armgard_Else_Helene_von_Veltheim
    literal_value: 2019
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (67e36a12-d453-4150-9e21-616da13a2735)
 Call ID: 67e36a12-d453-4150-9e21-616da13a2735
  Args:
    source: Friedrich_von_Veltheim
    type: :Man
  AssignClass (906ebdf4-75b2-482a-8cc6-f1f3a7f9cdce)
 Call ID: 906ebdf4-75b2-482a-8cc6-f1f3a7f9cdce
  Args:
    source: Friedrich_von_Veltheim
    type: :Person
  AssignClass (7c7a1a43-e1ee-4df3-96dd-69bceb1348c6)
 Call ID: 7c7a1a43-e1ee-4df3-96dd-69bceb1348c6
  Args:
    type: :Woman
    source: Ottonie_von_Alvensleben
  AssignClass (8d7a4ffe-b1cb-4b43-99ed-4837e6633833)
 Call ID: 8d7a4ffe-b1cb-4b43-99ed-4837e6633833
  Args:
    type: :Person
    source: Ottonie_von_Alvensleben
  AddTriple (7606e219-eaeb-41af-b295-b8f10463fb31)
 Call ID: 7606e219-eaeb-41af-b295-b8f10463fb31
  Args:
    relation: :hasFather
    target: Friedrich_von_Veltheim
    source: Armgard_Else_Helene_von_Veltheim
  AddTriple (b01f215b-d923-4397-b216-45655c735d03)
 Call ID: b01f215b-d923-4397-b216-45655c735d03
  Args:
    source: Armgard_Else_Helene_von_Veltheim
    target: Ottonie_von_Alvensleben
    relation: :hasMother
  AddLiteral (f02c755b-0244-4c21-88ec-96b662930c74)
 Call ID: f02c755b-0244-4c21-88ec-96b662930c74
  Args:
    literal_value: 1881
    source: Friedrich_von_Veltheim
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bd8d0b5f-4343-47ca-a83f-c1a9b93b2553)
 Call ID: bd8d0b5f-4343-47ca-a83f-c1a9b93b2553
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1955
    source: Friedrich_von_Veltheim
  AddLiteral (aef8fe5d-4702-449c-98bd-e441475d5f39)
 Call ID: aef8fe5d-4702-449c-98bd-e441475d5f39
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Ottonie_von_Alvensleben
    literal_value: 1883
  AddLiteral (51b4b006-bb2a-4c9f-aa1f-70fb2569374e)
 Call ID: 51b4b006-bb2a-4c9f-aa1f-70fb2569374e
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1960
    source: Ottonie_von_Alvensleben
  Finish (59c237b4-e7b7-40a6-8139-ca6028773284)
 Call ID: 59c237b4-e7b7-40a6-8139-ca6028773284
  Args: