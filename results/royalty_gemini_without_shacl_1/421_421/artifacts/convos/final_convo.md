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
Friedrich Wilhelm of Lippe (German: Friedrich Wilhelm Ernst Viktor Alexander Prinz zur Lippe; born 7 September 1947) is a claimant to the headship of the House of Lippe.
Early life

Friedrich Wilhelm was born out of wedlock at Neuwied, West Germany, the first child of Prince Ernst August of Lippe (1917–1990; son of Prince Julius Ernst of Lippe and Duchess Marie of Mecklenburg-Strelitz) and his wife, Christa von Arnim (b. 1923; daughter of Curt David von Arnim and his wife, Stephanie von Stechow).
Marriage

Friedrich Wilhelm married on 18 September 1991 in Munich to Andrea Messner (b. 1966), daughter of Günther Messner, and his wife, Lieselotte Trzoska.
House of Lippe

On 30 December 1949 his father's first cousin Prince Armin succeeded his father, Leopold IV as head of the House of Lippe.
On 22 March 1953, he renounced his position in favour of his older half-brother, Prince Leopold.
Prince Leopold later in 1958 renounced the headship in favour of his older brother, Hereditary Prince Ernst.
Later in that year the Hereditary Prince called a family council where it was agreed by the princes in attendance that the oldest prince living in Germany would be head of the house.
Therefore, the position went to Prince Simon Casimir (1900–1980).
His father died in 1990 and Friedrich Wilhelm continued the claim, despite his illegitimate birth.
Prince Armin, who has said he did not think his decision in 1953 was irrevocable, also claimed to be head of the house until his death in 2015, with his son Stephan, Prince of Lippe continuing his claim.



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
  AssignClass (3c6d8cb5-ec44-41b2-9213-e711ce6ca761)
 Call ID: 3c6d8cb5-ec44-41b2-9213-e711ce6ca761
  Args:
    type: :Man
    source: Friedrich Wilhelm of Lippe
  AssignClass (45b99f69-310a-4273-a387-398b2a185390)
 Call ID: 45b99f69-310a-4273-a387-398b2a185390
  Args:
    type: :Person
    source: Friedrich Wilhelm of Lippe
  AddLiteral (ff5868a7-5338-433f-9b43-16a4eaf7ebf8)
 Call ID: ff5868a7-5338-433f-9b43-16a4eaf7ebf8
  Args:
    source: Friedrich Wilhelm of Lippe
    literal_type: xsd:integer
    literal_value: 1947
    relation: :hasBirthYear
  AssignClass (16561248-7665-4040-a074-5fee9bcbb02a)
 Call ID: 16561248-7665-4040-a074-5fee9bcbb02a
  Args:
    type: :Man
    source: Ernst August of Lippe
  AssignClass (b97140d6-a13e-4340-a47b-3f0b226d8e07)
 Call ID: b97140d6-a13e-4340-a47b-3f0b226d8e07
  Args:
    type: :Person
    source: Ernst August of Lippe
  AddLiteral (5ae51be0-3937-4a7e-a5dc-be89cf4ef6dd)
 Call ID: 5ae51be0-3937-4a7e-a5dc-be89cf4ef6dd
  Args:
    source: Ernst August of Lippe
    literal_type: xsd:integer
    literal_value: 1917
    relation: :hasBirthYear
  AddLiteral (b8bace08-05fb-4bb0-8ca8-0767cc6036c8)
 Call ID: b8bace08-05fb-4bb0-8ca8-0767cc6036c8
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1990
    source: Ernst August of Lippe
  AssignClass (27d3009c-4a06-4c77-9685-4456b94dfca6)
 Call ID: 27d3009c-4a06-4c77-9685-4456b94dfca6
  Args:
    type: :Woman
    source: Christa von Arnim
  AssignClass (daa62b86-e2bf-4838-bb06-4670c4a2ba32)
 Call ID: daa62b86-e2bf-4838-bb06-4670c4a2ba32
  Args:
    type: :Person
    source: Christa von Arnim
  AddLiteral (b3ade922-623d-4526-bd74-6a9072f3e15b)
 Call ID: b3ade922-623d-4526-bd74-6a9072f3e15b
  Args:
    relation: :hasBirthYear
    literal_value: 1923
    literal_type: xsd:integer
    source: Christa von Arnim
  AddTriple (0332f631-8251-4c9a-9988-3edac5c66de5)
 Call ID: 0332f631-8251-4c9a-9988-3edac5c66de5
  Args:
    relation: :hasFather
    target: Ernst August of Lippe
    source: Friedrich Wilhelm of Lippe
  AddTriple (aec89b22-8f51-4384-a18e-6ccbfcbd0ee2)
 Call ID: aec89b22-8f51-4384-a18e-6ccbfcbd0ee2
  Args:
    relation: :hasMother
    target: Christa von Arnim
    source: Friedrich Wilhelm of Lippe
  AssignClass (ecd8bebc-fd24-42ae-8509-d79d2a778104)
 Call ID: ecd8bebc-fd24-42ae-8509-d79d2a778104
  Args:
    type: :Man
    source: Julius Ernst of Lippe
  AssignClass (009d8cee-0287-4ae0-ba00-e64dfadb15d2)
 Call ID: 009d8cee-0287-4ae0-ba00-e64dfadb15d2
  Args:
    type: :Person
    source: Julius Ernst of Lippe
  AssignClass (b084c58a-350c-4a49-b489-2bd1a896db80)
 Call ID: b084c58a-350c-4a49-b489-2bd1a896db80
  Args:
    type: :Woman
    source: Marie of Mecklenburg-Strelitz
  AssignClass (8e280a34-fbd5-4f51-8540-48318cbcba9c)
 Call ID: 8e280a34-fbd5-4f51-8540-48318cbcba9c
  Args:
    type: :Person
    source: Marie of Mecklenburg-Strelitz
  AddTriple (8aac00c0-7b39-40ab-847a-b43d0912f20f)
 Call ID: 8aac00c0-7b39-40ab-847a-b43d0912f20f
  Args:
    target: Julius Ernst of Lippe
    source: Ernst August of Lippe
    relation: :hasFather
  AddTriple (8748a2a2-dd0d-4c7c-b135-82ffc795fb69)
 Call ID: 8748a2a2-dd0d-4c7c-b135-82ffc795fb69
  Args:
    relation: :hasMother
    source: Ernst August of Lippe
    target: Marie of Mecklenburg-Strelitz
  AssignClass (b1fdd80e-e635-4690-891b-e5357dfc7df8)
 Call ID: b1fdd80e-e635-4690-891b-e5357dfc7df8
  Args:
    type: :Man
    source: Curt David von Arnim
  AssignClass (cc9747d3-9842-4f63-89f2-c4201aa384a6)
 Call ID: cc9747d3-9842-4f63-89f2-c4201aa384a6
  Args:
    type: :Person
    source: Curt David von Arnim
  AssignClass (ef1dc1dc-6c50-4fdc-88ad-2bc2b1f74e23)
 Call ID: ef1dc1dc-6c50-4fdc-88ad-2bc2b1f74e23
  Args:
    type: :Woman
    source: Stephanie von Stechow
  AssignClass (2b6bc515-5416-4cd0-8dc6-5a4593271848)
 Call ID: 2b6bc515-5416-4cd0-8dc6-5a4593271848
  Args:
    type: :Person
    source: Stephanie von Stechow
  AddTriple (a0b87d93-aae8-42f0-bf2c-5c073e5be388)
 Call ID: a0b87d93-aae8-42f0-bf2c-5c073e5be388
  Args:
    relation: :hasFather
    target: Curt David von Arnim
    source: Christa von Arnim
  AddTriple (d1db860b-d7b6-477c-a2ff-afd35e8de62b)
 Call ID: d1db860b-d7b6-477c-a2ff-afd35e8de62b
  Args:
    relation: :hasMother
    target: Stephanie von Stechow
    source: Christa von Arnim
  AssignClass (8d461549-e46a-499b-93c6-3b459744b489)
 Call ID: 8d461549-e46a-499b-93c6-3b459744b489
  Args:
    type: :Woman
    source: Andrea Messner
  AssignClass (211332d2-7210-4614-8825-435b37485a4b)
 Call ID: 211332d2-7210-4614-8825-435b37485a4b
  Args:
    type: :Person
    source: Andrea Messner
  AddLiteral (e1581f4d-5569-42ba-9677-47471d75532b)
 Call ID: e1581f4d-5569-42ba-9677-47471d75532b
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1966
    source: Andrea Messner
  AddLiteral (6ccbf7e6-47c0-4d5f-91aa-ca732aa2829d)
 Call ID: 6ccbf7e6-47c0-4d5f-91aa-ca732aa2829d
  Args:
    literal_value: 1991
    literal_type: xsd:integer
    source: Friedrich Wilhelm of Lippe
    relation: :hasMarriageYear
  AddTriple (05e6339d-53fc-4925-8fd5-d17e404524c5)
 Call ID: 05e6339d-53fc-4925-8fd5-d17e404524c5
  Args:
    relation: :hasRelation
    target: Andrea Messner
    source: Friedrich Wilhelm of Lippe
  AssignClass (d4a039be-fe45-4629-af43-e3e8a34e7d5c)
 Call ID: d4a039be-fe45-4629-af43-e3e8a34e7d5c
  Args:
    type: :Man
    source: Günther Messner
  AssignClass (8dd3ef1d-f709-414d-a37a-03bae15280fb)
 Call ID: 8dd3ef1d-f709-414d-a37a-03bae15280fb
  Args:
    type: :Person
    source: Günther Messner
  AssignClass (11ec17ce-23ef-4478-9a97-6f2897eedb63)
 Call ID: 11ec17ce-23ef-4478-9a97-6f2897eedb63
  Args:
    type: :Woman
    source: Lieselotte Trzoska
  AssignClass (570ddbcf-c786-47ba-ab6f-b53cc19bd8c3)
 Call ID: 570ddbcf-c786-47ba-ab6f-b53cc19bd8c3
  Args:
    type: :Person
    source: Lieselotte Trzoska
  AddTriple (673d73df-2685-4857-8d10-a8d2e4492158)
 Call ID: 673d73df-2685-4857-8d10-a8d2e4492158
  Args:
    relation: :hasFather
    source: Andrea Messner
    target: Günther Messner
  AddTriple (1d420524-dc4c-4b47-82e0-146b3d75bc63)
 Call ID: 1d420524-dc4c-4b47-82e0-146b3d75bc63
  Args:
    target: Lieselotte Trzoska
    source: Andrea Messner
    relation: :hasMother
  AssignClass (f5cced80-4858-4150-9b44-983a36fefeab)
 Call ID: f5cced80-4858-4150-9b44-983a36fefeab
  Args:
    type: :Man
    source: Armin of Lippe
  AssignClass (fdae88db-42c3-40f2-8155-930303c075ba)
 Call ID: fdae88db-42c3-40f2-8155-930303c075ba
  Args:
    type: :Person
    source: Armin of Lippe
  AssignClass (a433d5af-3c81-4cc0-9414-b2f4b9eb1ec8)
 Call ID: a433d5af-3c81-4cc0-9414-b2f4b9eb1ec8
  Args:
    type: :Man
    source: Leopold IV of Lippe
  AssignClass (076119dc-a72e-405f-af4b-2f5fb4beb440)
 Call ID: 076119dc-a72e-405f-af4b-2f5fb4beb440
  Args:
    type: :Person
    source: Leopold IV of Lippe
  AddTriple (ad1dd541-db53-4866-bab6-e59d70ab0832)
 Call ID: ad1dd541-db53-4866-bab6-e59d70ab0832
  Args:
    relation: :hasFather
    target: Leopold IV of Lippe
    source: Armin of Lippe
  AssignClass (aa848503-1e55-410f-9e79-f0a24d2c39ea)
 Call ID: aa848503-1e55-410f-9e79-f0a24d2c39ea
  Args:
    type: :Man
    source: Leopold of Lippe
  AssignClass (c1220660-3630-425e-bde2-51fccb760d58)
 Call ID: c1220660-3630-425e-bde2-51fccb760d58
  Args:
    type: :Person
    source: Leopold of Lippe
  AssignClass (ecd4fbd0-05bd-4196-8b8b-a57c14cf1c49)
 Call ID: ecd4fbd0-05bd-4196-8b8b-a57c14cf1c49
  Args:
    type: :Man
    source: Ernst of Lippe
  AssignClass (a0c1c94e-a7c4-4e77-9309-2bebd39c199c)
 Call ID: a0c1c94e-a7c4-4e77-9309-2bebd39c199c
  Args:
    type: :Person
    source: Ernst of Lippe
  AssignClass (974ca842-0292-4752-8467-056cc7dd308c)
 Call ID: 974ca842-0292-4752-8467-056cc7dd308c
  Args:
    type: :Man
    source: Simon Casimir of Lippe
  AssignClass (9015dae7-96fa-485e-896f-4823e09227ca)
 Call ID: 9015dae7-96fa-485e-896f-4823e09227ca
  Args:
    type: :Person
    source: Simon Casimir of Lippe
  AddLiteral (b88a4745-64c2-48d5-9cd6-0d5abd89658b)
 Call ID: b88a4745-64c2-48d5-9cd6-0d5abd89658b
  Args:
    literal_value: 1900
    literal_type: xsd:integer
    source: Simon Casimir of Lippe
    relation: :hasBirthYear
  AddLiteral (f7a60a99-f77e-4fd7-8be5-34be3d6a42eb)
 Call ID: f7a60a99-f77e-4fd7-8be5-34be3d6a42eb
  Args:
    literal_value: 1980
    literal_type: xsd:integer
    source: Simon Casimir of Lippe
    relation: :hasDeathYear
  AssignClass (9d414c56-898a-4fcf-a252-be500bd6298c)
 Call ID: 9d414c56-898a-4fcf-a252-be500bd6298c
  Args:
    type: :Man
    source: Stephan of Lippe
  AssignClass (83e9a4cc-71d9-4e6b-9caf-dc746f5ef240)
 Call ID: 83e9a4cc-71d9-4e6b-9caf-dc746f5ef240
  Args:
    type: :Person
    source: Stephan of Lippe
  AddTriple (26878f50-303e-4a97-9beb-0d8b44a7d2b3)
 Call ID: 26878f50-303e-4a97-9beb-0d8b44a7d2b3
  Args:
    target: Armin of Lippe
    source: Stephan of Lippe
    relation: :hasFather
  AddLiteral (c7aebac6-cc0e-4913-93b0-5d276b09fce4)
 Call ID: c7aebac6-cc0e-4913-93b0-5d276b09fce4
  Args:
    relation: :hasDeathYear
    source: Armin of Lippe
    literal_value: 2015
    literal_type: xsd:integer
  Finish (a60757e8-5eee-484b-867b-284776b2951a)
 Call ID: a60757e8-5eee-484b-867b-284776b2951a
  Args: