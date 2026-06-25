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
Klaus Felix von Amsberg (German: Klaus Felix Friedrich Leopold Gabriel Archim Julius August von Amsberg; 1 September 1890 – 19 December 1953) was a member of the German Niederer Adel (lower nobility) and father of Prince Claus of the Netherlands.
Early life

He was born at Rehna, Mecklenburg-Schwerin, German Empire (now Mecklenburg-Vorpommern, Germany), the first child of Wilhelm von Amsberg (1856–1929), by his marriage to Elise von Vieregg (1866–1951), member of an old aristocratic family.
Claus was from 1917 the steward of an estate after a failed venture in Africa as a planter.
Marriage

Claus married on 4 September 1924 at Hitzacker to Baroness Gösta von dem Bussche-Haddenhausen (26 January 1902 –
13 June 1996), daughter of Baron Georg von dem Bussche-Haddenhausen (1869–1923) and Baroness Gabriele von dem Bussche-Ippenburg (1877–1973).



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
  AssignClass (5b63ee05-6f44-469e-bfa3-01d1df149465)
 Call ID: 5b63ee05-6f44-469e-bfa3-01d1df149465
  Args:
    type: :Man
    source: Klaus_Felix_von_Amsberg
  AssignClass (26ed350f-3085-43b1-8d52-99769f0452b3)
 Call ID: 26ed350f-3085-43b1-8d52-99769f0452b3
  Args:
    source: Wilhelm_von_Amsberg
    type: :Man
  AssignClass (f69dd0dc-7ea2-4119-a9b1-d250db9c8f6d)
 Call ID: f69dd0dc-7ea2-4119-a9b1-d250db9c8f6d
  Args:
    type: :Woman
    source: Elise_von_Vieregg
  AssignClass (0ae34bc6-4aa7-4840-a9c7-44fd11303369)
 Call ID: 0ae34bc6-4aa7-4840-a9c7-44fd11303369
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (10ade1a2-ceb6-4765-9512-859d636652b0)
 Call ID: 10ade1a2-ceb6-4765-9512-859d636652b0
  Args:
    type: :Man
    source: Georg_von_dem_Bussche-Haddenhausen
  AssignClass (13cc5534-3852-45c1-b003-9fc8b16ddf00)
 Call ID: 13cc5534-3852-45c1-b003-9fc8b16ddf00
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    type: :Woman
  AddLiteral (44859871-0b5f-412a-9fc7-c764f5c92661)
 Call ID: 44859871-0b5f-412a-9fc7-c764f5c92661
  Args:
    literal_type: xsd:integer
    source: Klaus_Felix_von_Amsberg
    relation: :hasBirthYear
    literal_value: 1890
  AddLiteral (5866231d-d685-4cff-a066-f7793facd583)
 Call ID: 5866231d-d685-4cff-a066-f7793facd583
  Args:
    literal_type: xsd:integer
    source: Klaus_Felix_von_Amsberg
    relation: :hasDeathYear
    literal_value: 1953
  AddLiteral (4a2d56bc-fdfb-4836-bbb8-3564f5af1aec)
 Call ID: 4a2d56bc-fdfb-4836-bbb8-3564f5af1aec
  Args:
    source: Wilhelm_von_Amsberg
    literal_type: xsd:integer
    literal_value: 1856
    relation: :hasBirthYear
  AddLiteral (d2a1c291-821b-4def-9c29-aa989d0ac290)
 Call ID: d2a1c291-821b-4def-9c29-aa989d0ac290
  Args:
    literal_type: xsd:integer
    source: Wilhelm_von_Amsberg
    relation: :hasDeathYear
    literal_value: 1929
  AddLiteral (113ab069-da09-478f-bdce-8b440a48dcb5)
 Call ID: 113ab069-da09-478f-bdce-8b440a48dcb5
  Args:
    source: Elise_von_Vieregg
    literal_type: xsd:integer
    literal_value: 1866
    relation: :hasBirthYear
  AddLiteral (9ab46cbd-2184-4863-92c5-177192307a9d)
 Call ID: 9ab46cbd-2184-4863-92c5-177192307a9d
  Args:
    literal_value: 1951
    relation: :hasDeathYear
    source: Elise_von_Vieregg
    literal_type: xsd:integer
  AddLiteral (6a96d4c4-9756-4394-9966-2f640dfc3bde)
 Call ID: 6a96d4c4-9756-4394-9966-2f640dfc3bde
  Args:
    relation: :hasMarriageYear
    literal_value: 1924
    literal_type: xsd:integer
    source: Klaus_Felix_von_Amsberg
  AddLiteral (a596371e-9377-4aa6-ba0f-b1d107ce775d)
 Call ID: a596371e-9377-4aa6-ba0f-b1d107ce775d
  Args:
    literal_type: xsd:integer
    source: Gosta_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
    literal_value: 1902
  AddLiteral (ef1848c1-740f-49a0-a6f5-0fe6ae49c0be)
 Call ID: ef1848c1-740f-49a0-a6f5-0fe6ae49c0be
  Args:
    literal_value: 1996
    relation: :hasDeathYear
    source: Gosta_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AddLiteral (5ec05a1a-0e68-445f-9b91-b5ac4bb21510)
 Call ID: 5ec05a1a-0e68-445f-9b91-b5ac4bb21510
  Args:
    relation: :hasBirthYear
    literal_value: 1869
    literal_type: xsd:integer
    source: Georg_von_dem_Bussche-Haddenhausen
  AddLiteral (b2f5c8d8-a702-4bf9-a0fa-c9ba0dad575d)
 Call ID: b2f5c8d8-a702-4bf9-a0fa-c9ba0dad575d
  Args:
    source: Georg_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1923
    relation: :hasDeathYear
  AddLiteral (2b39323b-5c84-4ac1-8f2a-2809f592f76b)
 Call ID: 2b39323b-5c84-4ac1-8f2a-2809f592f76b
  Args:
    literal_value: 1877
    relation: :hasBirthYear
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_type: xsd:integer
  AddLiteral (8d52611a-e0a6-40e9-8acd-a594ead20fad)
 Call ID: 8d52611a-e0a6-40e9-8acd-a594ead20fad
  Args:
    source: Gabriele_von_dem_Bussche-Ippenburg
    literal_type: xsd:integer
    literal_value: 1973
    relation: :hasDeathYear
  AddTriple (03d2b4a1-ef3a-4359-94b8-9f6d254f21a1)
 Call ID: 03d2b4a1-ef3a-4359-94b8-9f6d254f21a1
  Args:
    target: Wilhelm_von_Amsberg
    source: Klaus_Felix_von_Amsberg
    relation: :hasFather
  AddTriple (dab128ac-743c-4a76-bfb2-675afa95f5ec)
 Call ID: dab128ac-743c-4a76-bfb2-675afa95f5ec
  Args:
    target: Elise_von_Vieregg
    source: Klaus_Felix_von_Amsberg
    relation: :hasMother
  AddTriple (0cca0933-e497-48a3-839d-2d973bfb70cc)
 Call ID: 0cca0933-e497-48a3-839d-2d973bfb70cc
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    target: Georg_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (efce0565-4d89-4ce6-9d3a-eb600ca844d3)
 Call ID: efce0565-4d89-4ce6-9d3a-eb600ca844d3
  Args:
    source: Gosta_von_dem_Bussche-Haddenhausen
    target: Gabriele_von_dem_Bussche-Ippenburg
    relation: :hasMother
  Finish (816f3627-4c1d-4f47-9d5b-912028cf73c1)
 Call ID: 816f3627-4c1d-4f47-9d5b-912028cf73c1
  Args: