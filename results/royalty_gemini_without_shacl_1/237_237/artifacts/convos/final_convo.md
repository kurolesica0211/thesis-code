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
Duke Friedrich August of Oldenburg (11 January 1936 – 9 July 2017) was a member of the House of Holstein-Gottorp.
He is a son of Nikolaus, Hereditary Grand Duke of Oldenburg and Princess Helena of Waldeck and Pyrmont.
Family and early life

Frederich August is the sixth child and fourth son of Nikolaus, Hereditary Grand Duke of Oldenburg and his first wife Princess Helena of Waldeck and Pyrmont.
His paternal grandparents are Frederick Augustus II, Grand Duke of Oldenburg and Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin.
His maternal grandparents are Friedrich, Prince of Waldeck and Pyrmont and Princess Bathildis of Schaumburg-Lippe.
His grandfather was overthrown as Grand Duke of Oldenburg in 1918, at the end of World War I.
His father Nikolaus thus never legally succeeded to the title when the deposed Grand Duke died in 1931.
Friedrich is an uncle of Christian, Duke of Oldenburg, the current head of the House of Oldenburg.
Marriage and issue

Friedrich August's first wife was Princess Marie Cécile of Prussia, a daughter of Louis Ferdinand, Prince of Prussia (second son of William, German Crown Prince) and his wife, Grand Duchess Kira Kirillovna of Russia.
Friedrich August and Marie-Cécile have three children: a son, and two daughters.
Marie-Cécile and Friedrich August divorced on 23 November 1989.
On 9 February 1991, Friedrich August was remarried to Donata Countess of Castell-Rüdenhausen in Rüdenhausen, Germany.



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
  AssignClass (d529ddf3-1d4a-4474-8769-552a12846271)
 Call ID: d529ddf3-1d4a-4474-8769-552a12846271
  Args:
    source: Friedrich_August_of_Oldenburg
    type: :Man
  AssignClass (45eedb94-8ca5-4c05-8f58-092fb3bc2826)
 Call ID: 45eedb94-8ca5-4c05-8f58-092fb3bc2826
  Args:
    type: :Person
    source: Friedrich_August_of_Oldenburg
  AddLiteral (b140b788-a482-47a1-91a9-77de5ac6176b)
 Call ID: b140b788-a482-47a1-91a9-77de5ac6176b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Friedrich_August_of_Oldenburg
    literal_value: 1936
  AddLiteral (1b8a8a55-aa5e-4e94-9b7a-f91087a5eeae)
 Call ID: 1b8a8a55-aa5e-4e94-9b7a-f91087a5eeae
  Args:
    source: Friedrich_August_of_Oldenburg
    literal_value: 2017
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (487db2ef-c49e-4d6e-a6cd-9e2d8e7c7465)
 Call ID: 487db2ef-c49e-4d6e-a6cd-9e2d8e7c7465
  Args:
    type: :Man
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
  AssignClass (7e4d4b1e-9b8b-4d41-bcc6-1b82280af848)
 Call ID: 7e4d4b1e-9b8b-4d41-bcc6-1b82280af848
  Args:
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    type: :Person
  AssignClass (85bf0f53-583f-447d-859b-e1ae0b9f8f55)
 Call ID: 85bf0f53-583f-447d-859b-e1ae0b9f8f55
  Args:
    source: Princess_Helena_of_Waldeck_and_Pyrmont
    type: :Woman
  AssignClass (b65280cd-b5c9-42f6-a714-a445d5ec3b49)
 Call ID: b65280cd-b5c9-42f6-a714-a445d5ec3b49
  Args:
    source: Princess_Helena_of_Waldeck_and_Pyrmont
    type: :Person
  AddTriple (35ecc20c-5c06-4aa7-a79f-47d37946d212)
 Call ID: 35ecc20c-5c06-4aa7-a79f-47d37946d212
  Args:
    target: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    source: Friedrich_August_of_Oldenburg
    relation: :hasFather
  AddTriple (7d9e9fae-89ba-461b-9c9f-02d2c37d9eae)
 Call ID: 7d9e9fae-89ba-461b-9c9f-02d2c37d9eae
  Args:
    target: Princess_Helena_of_Waldeck_and_Pyrmont
    source: Friedrich_August_of_Oldenburg
    relation: :hasMother
  AssignClass (980f3ed0-713a-4221-84b7-aee25c941bd2)
 Call ID: 980f3ed0-713a-4221-84b7-aee25c941bd2
  Args:
    source: Frederick_Augustus_II_Grand_Duke_of_Oldenburg
    type: :Man
  AssignClass (2cbed2b5-47b1-402d-913a-1943e22c0c29)
 Call ID: 2cbed2b5-47b1-402d-913a-1943e22c0c29
  Args:
    type: :Person
    source: Frederick_Augustus_II_Grand_Duke_of_Oldenburg
  AssignClass (a308f6dc-da04-416e-95ad-bb8c1951b775)
 Call ID: a308f6dc-da04-416e-95ad-bb8c1951b775
  Args:
    source: Duchess_Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    type: :Woman
  AssignClass (75efca0b-8515-4761-ad46-8e6aee542039)
 Call ID: 75efca0b-8515-4761-ad46-8e6aee542039
  Args:
    source: Duchess_Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
    type: :Person
  AddTriple (e4d62d4e-6588-49ef-8c29-2a1a75e5ab2e)
 Call ID: e4d62d4e-6588-49ef-8c29-2a1a75e5ab2e
  Args:
    relation: :hasFather
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    target: Frederick_Augustus_II_Grand_Duke_of_Oldenburg
  AddTriple (2e09f8db-9a7a-4e5e-80b4-2e93b419e96a)
 Call ID: 2e09f8db-9a7a-4e5e-80b4-2e93b419e96a
  Args:
    relation: :hasMother
    source: Nikolaus_Hereditary_Grand_Duke_of_Oldenburg
    target: Duchess_Elisabeth_Alexandrine_of_Mecklenburg_Schwerin
  AssignClass (dd787219-75db-4d7f-b445-7eecc5856c01)
 Call ID: dd787219-75db-4d7f-b445-7eecc5856c01
  Args:
    source: Friedrich_Prince_of_Waldeck_and_Pyrmont
    type: :Man
  AssignClass (cb4ec95b-7cc1-48b2-8698-5a46ef15fd09)
 Call ID: cb4ec95b-7cc1-48b2-8698-5a46ef15fd09
  Args:
    source: Friedrich_Prince_of_Waldeck_and_Pyrmont
    type: :Person
  AssignClass (1d56d287-779e-4233-8a97-16ba0d109fd5)
 Call ID: 1d56d287-779e-4233-8a97-16ba0d109fd5
  Args:
    type: :Woman
    source: Princess_Bathildis_of_Schaumburg_Lippe
  AssignClass (53906104-88d3-43e5-bf95-d17311b6a23f)
 Call ID: 53906104-88d3-43e5-bf95-d17311b6a23f
  Args:
    type: :Person
    source: Princess_Bathildis_of_Schaumburg_Lippe
  AddTriple (eefc58bf-1f07-4e58-a77e-d5cf61974b91)
 Call ID: eefc58bf-1f07-4e58-a77e-d5cf61974b91
  Args:
    relation: :hasFather
    target: Friedrich_Prince_of_Waldeck_and_Pyrmont
    source: Princess_Helena_of_Waldeck_and_Pyrmont
  AddTriple (00f7ab36-a189-47e3-b7ea-5fc1b5834134)
 Call ID: 00f7ab36-a189-47e3-b7ea-5fc1b5834134
  Args:
    relation: :hasMother
    source: Princess_Helena_of_Waldeck_and_Pyrmont
    target: Princess_Bathildis_of_Schaumburg_Lippe
  AssignClass (b33dd147-ad1f-43cd-aef9-adc0191d02f8)
 Call ID: b33dd147-ad1f-43cd-aef9-adc0191d02f8
  Args:
    type: :Man
    source: Christian_Duke_of_Oldenburg
  AssignClass (71373cf0-a30c-40b8-b8f1-241df087f6c7)
 Call ID: 71373cf0-a30c-40b8-b8f1-241df087f6c7
  Args:
    type: :Person
    source: Christian_Duke_of_Oldenburg
  AddTriple (544fd732-b521-44a9-a006-64c4d3f1f9a1)
 Call ID: 544fd732-b521-44a9-a006-64c4d3f1f9a1
  Args:
    source: Friedrich_August_of_Oldenburg
    target: Christian_Duke_of_Oldenburg
    relation: :isUncleOf
  AssignClass (cf81a891-4d8e-4c52-b2a0-eb3ee1cdb613)
 Call ID: cf81a891-4d8e-4c52-b2a0-eb3ee1cdb613
  Args:
    type: :Woman
    source: Princess_Marie_Cecile_of_Prussia
  AssignClass (97760de7-35b8-4438-aa1e-4b555810faf6)
 Call ID: 97760de7-35b8-4438-aa1e-4b555810faf6
  Args:
    type: :Person
    source: Princess_Marie_Cecile_of_Prussia
  AddTriple (40b4adea-68fa-4892-a599-cdc87c447462)
 Call ID: 40b4adea-68fa-4892-a599-cdc87c447462
  Args:
    target: Princess_Marie_Cecile_of_Prussia
    source: Friedrich_August_of_Oldenburg
    relation: :hasRelation
  AssignClass (4d3b239e-0938-4d0a-a6e7-0c919611d8ec)
 Call ID: 4d3b239e-0938-4d0a-a6e7-0c919611d8ec
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Man
  AssignClass (46660b51-f5fb-4371-92a8-b905063c5767)
 Call ID: 46660b51-f5fb-4371-92a8-b905063c5767
  Args:
    source: Louis_Ferdinand_Prince_of_Prussia
    type: :Person
  AssignClass (f9a8d16e-967b-4227-aa70-ba47c88669e2)
 Call ID: f9a8d16e-967b-4227-aa70-ba47c88669e2
  Args:
    type: :Woman
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AssignClass (2c7848d3-cc45-4754-9242-77de11efb5d3)
 Call ID: 2c7848d3-cc45-4754-9242-77de11efb5d3
  Args:
    type: :Person
    source: Grand_Duchess_Kira_Kirillovna_of_Russia
  AddTriple (9d245def-bba0-491c-bc1a-e3827a1410c4)
 Call ID: 9d245def-bba0-491c-bc1a-e3827a1410c4
  Args:
    source: Princess_Marie_Cecile_of_Prussia
    target: Louis_Ferdinand_Prince_of_Prussia
    relation: :hasFather
  AddTriple (59de10f9-a8bf-4be1-bf1f-7ce822cb6101)
 Call ID: 59de10f9-a8bf-4be1-bf1f-7ce822cb6101
  Args:
    target: Grand_Duchess_Kira_Kirillovna_of_Russia
    source: Princess_Marie_Cecile_of_Prussia
    relation: :hasMother
  AssignClass (e14f6e27-16b2-4d20-b1da-b03c931995a0)
 Call ID: e14f6e27-16b2-4d20-b1da-b03c931995a0
  Args:
    type: :Woman
    source: Donata_Countess_of_Castell_Rudenhausen
  AssignClass (ac37e6a2-6891-49c1-b37e-4388a4cdaede)
 Call ID: ac37e6a2-6891-49c1-b37e-4388a4cdaede
  Args:
    type: :Person
    source: Donata_Countess_of_Castell_Rudenhausen
  AddTriple (666b64ca-bbff-48aa-b46a-46fc0194dbd5)
 Call ID: 666b64ca-bbff-48aa-b46a-46fc0194dbd5
  Args:
    source: Friedrich_August_of_Oldenburg
    target: Donata_Countess_of_Castell_Rudenhausen
    relation: :hasRelation
  Finish (f0ae81d3-e684-4486-917c-7f60308945a8)
 Call ID: f0ae81d3-e684-4486-917c-7f60308945a8
  Args: