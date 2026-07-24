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
  AssignClass (6c02bb42-528b-47e1-914c-19c847ea9ce9)
 Call ID: 6c02bb42-528b-47e1-914c-19c847ea9ce9
  Args:
    source: :MariaCristinaOfSpain
    type: :Person
  AssignClass (6e5808e3-7d0f-4eab-b96a-bd807fcc4ab2)
 Call ID: 6e5808e3-7d0f-4eab-b96a-bd807fcc4ab2
  Args:
    source: :MariaCristinaOfSpain
    type: :Woman
  AssignClass (5231b079-5e1a-46c2-831b-c31d75cfe81c)
 Call ID: 5231b079-5e1a-46c2-831b-c31d75cfe81c
  Args:
    source: :AlfonsoXIIIOfSpain
    type: :Person
  AssignClass (29d346fc-d1bd-4e06-832f-b7d518db0d2b)
 Call ID: 29d346fc-d1bd-4e06-832f-b7d518db0d2b
  Args:
    source: :AlfonsoXIIIOfSpain
    type: :Man
  AssignClass (787e0ef2-2dc6-4e1b-acd7-fafc5d5f70a7)
 Call ID: 787e0ef2-2dc6-4e1b-acd7-fafc5d5f70a7
  Args:
    source: :VictoriaEugenieOfBattenberg
    type: :Person
  AssignClass (771db858-7e78-4e3e-8e83-ae023dd5f2b2)
 Call ID: 771db858-7e78-4e3e-8e83-ae023dd5f2b2
  Args:
    source: :VictoriaEugenieOfBattenberg
    type: :Woman
  AssignClass (09d6bc29-b681-4eda-85ff-79888eee110b)
 Call ID: 09d6bc29-b681-4eda-85ff-79888eee110b
  Args:
    source: :JuanCarlosI
    type: :Person
  AssignClass (b2c6702c-227a-4a5b-adfb-d1bcc1953218)
 Call ID: b2c6702c-227a-4a5b-adfb-d1bcc1953218
  Args:
    source: :JuanCarlosI
    type: :Man
  AssignClass (78d6dd71-3f5e-4011-88a5-668624800124)
 Call ID: 78d6dd71-3f5e-4011-88a5-668624800124
  Args:
    type: :Person
    source: :BeatrizOfSpain
  AssignClass (0c5052a5-4c5d-4000-807d-d74d857addcb)
 Call ID: 0c5052a5-4c5d-4000-807d-d74d857addcb
  Args:
    source: :BeatrizOfSpain
    type: :Woman
  AssignClass (c617ad3f-8b71-4936-8414-45423f0f94db)
 Call ID: c617ad3f-8b71-4936-8414-45423f0f94db
  Args:
    source: :AlfonsoOfSpain
    type: :Person
  AssignClass (67e0f1f0-2d65-4156-80dc-080d7738f9ef)
 Call ID: 67e0f1f0-2d65-4156-80dc-080d7738f9ef
  Args:
    source: :AlfonsoOfSpain
    type: :Man
  AssignClass (76fbe7a3-a99b-43cc-8463-4d47393c92fb)
 Call ID: 76fbe7a3-a99b-43cc-8463-4d47393c92fb
  Args:
    source: :GonzaloOfSpain
    type: :Person
  AssignClass (3a4114b4-2e27-4a87-8bde-92cc701edf40)
 Call ID: 3a4114b4-2e27-4a87-8bde-92cc701edf40
  Args:
    type: :Man
    source: :GonzaloOfSpain
  AssignClass (25540a3e-104f-4d4a-9efd-6a8f89b689d9)
 Call ID: 25540a3e-104f-4d4a-9efd-6a8f89b689d9
  Args:
    type: :Person
    source: :EnricoEugenio
  AssignClass (1e0456aa-60ca-4be6-b500-6fb1a8e07fe1)
 Call ID: 1e0456aa-60ca-4be6-b500-6fb1a8e07fe1
  Args:
    type: :Man
    source: :EnricoEugenio
  AddLiteral (a23a8f33-693b-4159-92c4-14de9b268be3)
 Call ID: a23a8f33-693b-4159-92c4-14de9b268be3
  Args:
    source: :MariaCristinaOfSpain
    literal_value: 1911
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (fc818523-2c81-4d0e-b547-f4130381961c)
 Call ID: fc818523-2c81-4d0e-b547-f4130381961c
  Args:
    literal_value: 1996
    source: :MariaCristinaOfSpain
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (70c96676-053f-41c1-b9a1-181430430178)
 Call ID: 70c96676-053f-41c1-b9a1-181430430178
  Args:
    relation: :hasFather
    source: :MariaCristinaOfSpain
    target: :AlfonsoXIIIOfSpain
  AddTriple (8658ace0-b912-4a56-aa71-b3162e9efe29)
 Call ID: 8658ace0-b912-4a56-aa71-b3162e9efe29
  Args:
    relation: :hasMother
    source: :MariaCristinaOfSpain
    target: :VictoriaEugenieOfBattenberg
  AddTriple (f69a2663-0a65-427f-a42b-d289f5586ac5)
 Call ID: f69a2663-0a65-427f-a42b-d289f5586ac5
  Args:
    relation: :isAuntOf
    target: :JuanCarlosI
    source: :MariaCristinaOfSpain
  AddTriple (d1d7704b-50b2-49d0-ad38-6dd4b4fbb3df)
 Call ID: d1d7704b-50b2-49d0-ad38-6dd4b4fbb3df
  Args:
    relation: :isSisterOf
    source: :MariaCristinaOfSpain
    target: :BeatrizOfSpain
  AddTriple (00a9b448-e7cb-48d7-9db1-569d54e01163)
 Call ID: 00a9b448-e7cb-48d7-9db1-569d54e01163
  Args:
    source: :AlfonsoOfSpain
    target: :AlfonsoXIIIOfSpain
    relation: :isBrotherOf
  AddTriple (7eeb4599-4b71-42c0-9fad-806efadf4fbc)
 Call ID: 7eeb4599-4b71-42c0-9fad-806efadf4fbc
  Args:
    target: :AlfonsoXIIIOfSpain
    source: :GonzaloOfSpain
    relation: :isBrotherOf
  AddTriple (f9349653-3c34-4623-96a9-ff4eb59bed21)
 Call ID: f9349653-3c34-4623-96a9-ff4eb59bed21
  Args:
    relation: :hasFather
    source: :AlfonsoOfSpain
    target: :AlfonsoXIIIOfSpain
  AddTriple (64609a54-2dad-45e4-aefc-d7adfcf9e3de)
 Call ID: 64609a54-2dad-45e4-aefc-d7adfcf9e3de
  Args:
    target: :AlfonsoXIIIOfSpain
    source: :GonzaloOfSpain
    relation: :hasFather
  Finish (091d42db-454b-4172-afd5-486f22639d6e)
 Call ID: 091d42db-454b-4172-afd5-486f22639d6e
  Args: