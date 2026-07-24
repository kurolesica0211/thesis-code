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
Infanta Maria Cristina of Spain, Countess Marone-Cinzano (María Cristina Teresa Alejandra María de Guadalupe María de la Concepción Ildefonsa Victoria Eugenia de Borbón y Battenberg; 12 December 1911 – 23 December 1996) was the fourth surviving child and youngest daughter of Alfonso XIII of Spain and Victoria Eugenie of Battenberg and paternal aunt of King Juan Carlos I.


Biography

Early life

Infanta Maria Cristina was born at the Palacio Real in Madrid, Spain.
By 1933 King Alfonso and his daughters, the Infantas Beatriz and Maria Cristina, had moved to Rome.
Their father warned would-be suitors of the inherent dangers of hemophilia, from which two of the king's sons, Alfonso and Gonzalo, suffered.
Maria Cristina had one step-son, from Enrico's previous marriage to Noemí Rosa de Alcorta y García-Mansilla (1907-1929):


The marriage of Maria Cristina and Enrico Eugenio produced four daughters:


Death

Infanta Maria Cristina returned to Spain and spent periods of time there, but never lived there permanently.
A funeral service for the Infanta was held in the chapel of the Royal Palace of Madrid on 24 December and a burial service was held on 26 December in the Marone-Cinzano Pantheon in Turin.



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
  AssignClass (d64bf094-50d2-481b-a8cf-e2815c9513d4)
 Call ID: d64bf094-50d2-481b-a8cf-e2815c9513d4
  Args:
    source: :MariaCristinaOfSpain
    type: :Woman
  AssignClass (8fdb741f-ad03-4a74-a765-9de1550c9a23)
 Call ID: 8fdb741f-ad03-4a74-a765-9de1550c9a23
  Args:
    source: :MariaCristinaOfSpain
    type: :Person
  AddLiteral (a113a4c3-9c35-4981-ac84-1acf252182e5)
 Call ID: a113a4c3-9c35-4981-ac84-1acf252182e5
  Args:
    relation: :knownAs
    source: :MariaCristinaOfSpain
    literal_value: Infanta Maria Cristina of Spain, Countess Marone-Cinzano
    literal_type: xsd:string
  AddLiteral (ecea008c-1b33-4438-837e-3a202730d4c8)
 Call ID: ecea008c-1b33-4438-837e-3a202730d4c8
  Args:
    source: :MariaCristinaOfSpain
    relation: :hasBirthYear
    literal_value: 1911
    literal_type: xsd:integer
  AddLiteral (a328c1f6-2af7-4066-aed7-2885e085caa8)
 Call ID: a328c1f6-2af7-4066-aed7-2885e085caa8
  Args:
    literal_type: xsd:integer
    literal_value: 1996
    source: :MariaCristinaOfSpain
    relation: :hasDeathYear
  AssignClass (dc3c4105-a289-440b-bc14-393d893807ea)
 Call ID: dc3c4105-a289-440b-bc14-393d893807ea
  Args:
    type: :Man
    source: :AlfonsoXIIIOfSpain
  AssignClass (db63a70d-4526-416f-9048-130852c0e3b5)
 Call ID: db63a70d-4526-416f-9048-130852c0e3b5
  Args:
    source: :AlfonsoXIIIOfSpain
    type: :Ancestor
  AddTriple (a6278474-9da7-4934-a649-d8c94dd5869f)
 Call ID: a6278474-9da7-4934-a649-d8c94dd5869f
  Args:
    source: :MariaCristinaOfSpain
    relation: :hasFather
    target: :AlfonsoXIIIOfSpain
  AssignClass (f345d65d-1b38-4dac-a5c3-d1fea4a3a192)
 Call ID: f345d65d-1b38-4dac-a5c3-d1fea4a3a192
  Args:
    source: :VictoriaEugenieOfBattenberg
    type: :Woman
  AssignClass (9fcf826f-a2f5-40cc-94f9-c5f1fb0cdb92)
 Call ID: 9fcf826f-a2f5-40cc-94f9-c5f1fb0cdb92
  Args:
    type: :Ancestor
    source: :VictoriaEugenieOfBattenberg
  AddTriple (bfa2392e-469c-4754-8358-ce10542c120c)
 Call ID: bfa2392e-469c-4754-8358-ce10542c120c
  Args:
    relation: :hasMother
    source: :MariaCristinaOfSpain
    target: :VictoriaEugenieOfBattenberg
  AssignClass (d6008788-2e0a-48fd-8d44-89d69b7e6144)
 Call ID: d6008788-2e0a-48fd-8d44-89d69b7e6144
  Args:
    type: :Man
    source: :JuanCarlosI
  AssignClass (a5b25a45-f55f-4912-9b77-678a13926ec9)
 Call ID: a5b25a45-f55f-4912-9b77-678a13926ec9
  Args:
    source: :JuanCarlosI
    type: :Person
  AddTriple (8c4ca2e5-0db4-457b-a55e-0e9b20172e85)
 Call ID: 8c4ca2e5-0db4-457b-a55e-0e9b20172e85
  Args:
    target: :JuanCarlosI
    relation: :isAuntOf
    source: :MariaCristinaOfSpain
  AssignClass (5bac1f42-41ec-4cf2-b75b-a71894049653)
 Call ID: 5bac1f42-41ec-4cf2-b75b-a71894049653
  Args:
    source: :BeatrizOfSpain
    type: :Woman
  AssignClass (8e0847b4-bd82-449e-8513-5eecf30d55b2)
 Call ID: 8e0847b4-bd82-449e-8513-5eecf30d55b2
  Args:
    type: :Person
    source: :BeatrizOfSpain
  AddTriple (59fd1b84-d4e8-4460-ba4d-8b21bca251f6)
 Call ID: 59fd1b84-d4e8-4460-ba4d-8b21bca251f6
  Args:
    source: :MariaCristinaOfSpain
    relation: :isSiblingOf
    target: :BeatrizOfSpain
  AssignClass (a1ae5673-dd7d-43af-a004-8aec71f7a6ee)
 Call ID: a1ae5673-dd7d-43af-a004-8aec71f7a6ee
  Args:
    source: :AlfonsoOfSpain
    type: :Man
  AssignClass (73229f00-039b-4a71-bbd5-80fd084509e6)
 Call ID: 73229f00-039b-4a71-bbd5-80fd084509e6
  Args:
    type: :Person
    source: :AlfonsoOfSpain
  AddTriple (868331e2-ec56-4625-91db-6af54d4df615)
 Call ID: 868331e2-ec56-4625-91db-6af54d4df615
  Args:
    relation: :isSiblingOf
    source: :MariaCristinaOfSpain
    target: :AlfonsoOfSpain
  AssignClass (ebbe7a6a-5c6b-4b59-931a-269eaee1c57c)
 Call ID: ebbe7a6a-5c6b-4b59-931a-269eaee1c57c
  Args:
    source: :GonzaloOfSpain
    type: :Man
  AssignClass (2bd19f04-8fde-41b6-b84a-f6a0c913883b)
 Call ID: 2bd19f04-8fde-41b6-b84a-f6a0c913883b
  Args:
    type: :Person
    source: :GonzaloOfSpain
  AddTriple (f3f64591-8652-4fc8-893b-e6a60a57b323)
 Call ID: f3f64591-8652-4fc8-893b-e6a60a57b323
  Args:
    relation: :isSiblingOf
    source: :MariaCristinaOfSpain
    target: :GonzaloOfSpain
  AssignClass (fefcb609-ed1c-4043-86e4-8f055f637ddc)
 Call ID: fefcb609-ed1c-4043-86e4-8f055f637ddc
  Args:
    type: :Man
    source: :EnricoEugenio
  AssignClass (79dc80e3-db5a-4339-8a5c-8c513527472f)
 Call ID: 79dc80e3-db5a-4339-8a5c-8c513527472f
  Args:
    type: :Person
    source: :EnricoEugenio
  AssignClass (7b4b5582-4953-4eff-98eb-a4b3ea728f2a)
 Call ID: 7b4b5582-4953-4eff-98eb-a4b3ea728f2a
  Args:
    source: :NoemiRosaDeAlcortaYGarcíaMansilla
    type: :Woman
  AssignClass (f14c4ffe-dcbb-4607-9922-2489bbd0dfef)
 Call ID: f14c4ffe-dcbb-4607-9922-2489bbd0dfef
  Args:
    type: :Person
    source: :NoemiRosaDeAlcortaYGarcíaMansilla
  AssignClass (455c3fc0-3de0-4b4c-88c6-91c577d415d2)
 Call ID: 455c3fc0-3de0-4b4c-88c6-91c577d415d2
  Args:
    type: :Man
    source: :StepSonOfMariaCristina
  AssignClass (ce023584-177d-4f6d-aad7-787a03db7fe2)
 Call ID: ce023584-177d-4f6d-aad7-787a03db7fe2
  Args:
    source: :StepSonOfMariaCristina
    type: :Person
  AddTriple (9ef34785-83dc-451b-98e0-49d5ba447429)
 Call ID: 9ef34785-83dc-451b-98e0-49d5ba447429
  Args:
    target: :EnricoEugenio
    source: :StepSonOfMariaCristina
    relation: :hasFather
  AddTriple (4169b0b0-ce63-404a-a1da-10915ab2bb61)
 Call ID: 4169b0b0-ce63-404a-a1da-10915ab2bb61
  Args:
    relation: :hasMother
    source: :StepSonOfMariaCristina
    target: :NoemiRosaDeAlcortaYGarcíaMansilla
  Finish (66dbf2bf-3801-49e8-81cd-9382d5aaae72)
 Call ID: 66dbf2bf-3801-49e8-81cd-9382d5aaae72
  Args: