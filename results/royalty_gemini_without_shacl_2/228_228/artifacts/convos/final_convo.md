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
Prince Waldemar of Prussia (Joachim Friedrich Ernst Waldemar; 10 February 1868 – 27 March 1879) was the sixth child and youngest son of the German Crown Prince and Crown Princess, later Emperor Frederick III and Empress Victoria.
Prince Waldemar was a grandson of both William I, German Emperor, and Queen Victoria of the United Kingdom.
Biography

Early life

Waldemar was the favourite of both the Princess Royal and her husband.
Waldemar had a "fun loving" character and a great sense of humour and love for animals and sports.
On one occasion, when visiting his grandmother, Queen Victoria, Waldemar let loose his pet crocodile in her study, much to the shock of the middle-aged queen.
The Princess Royal wrote that she would be unhappy when Waldemar went off to school, "as he is my very own boy."
She seemed to prefer Waldemar over his elder brothers Wilhelm and Heinrich.
Death

Less than four months after the deaths of his maternal aunt, Alice, Grand Duchess of Hesse and cousin, Marie, Waldemar became seriously ill with diphtheria and died in Berlin, Germany on 27 March 1879.
He was buried in the royal mausoleum attached to the Friedenskirche at Potsdam, near the main altar and his elder brother Prince Sigismund of Prussia.



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
  AssignClass (8d9b62f8-0dda-44f7-9e67-deef1b33210c)
 Call ID: 8d9b62f8-0dda-44f7-9e67-deef1b33210c
  Args:
    type: :Person
    source: Waldemar_of_Prussia
  AssignClass (18cb9922-69b5-47d5-bb73-f4093df005ea)
 Call ID: 18cb9922-69b5-47d5-bb73-f4093df005ea
  Args:
    type: :Man
    source: Waldemar_of_Prussia
  AddLiteral (077de45a-9fb6-4a3a-81e8-8ce80e8add17)
 Call ID: 077de45a-9fb6-4a3a-81e8-8ce80e8add17
  Args:
    literal_value: 1868
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Waldemar_of_Prussia
  AddLiteral (aed339bd-dead-4c40-b856-d1ef3222f1e8)
 Call ID: aed339bd-dead-4c40-b856-d1ef3222f1e8
  Args:
    literal_value: 1879
    relation: :hasDeathYear
    source: Waldemar_of_Prussia
    literal_type: xsd:integer
  AssignClass (09949ba3-f541-4eeb-9a41-17b5567c1871)
 Call ID: 09949ba3-f541-4eeb-9a41-17b5567c1871
  Args:
    type: :Person
    source: Frederick_III
  AssignClass (eedd78ba-62f3-4a6f-8a1c-df454a704ef8)
 Call ID: eedd78ba-62f3-4a6f-8a1c-df454a704ef8
  Args:
    type: :Man
    source: Frederick_III
  AssignClass (e2195869-4b8e-4d88-8943-c8a2556ce045)
 Call ID: e2195869-4b8e-4d88-8943-c8a2556ce045
  Args:
    type: :Person
    source: Victoria_Empress
  AssignClass (39a07dd0-c02c-4aa1-9c76-9340d21943d2)
 Call ID: 39a07dd0-c02c-4aa1-9c76-9340d21943d2
  Args:
    type: :Woman
    source: Victoria_Empress
  AddTriple (49a7378a-6aad-4c59-ad6f-5d4b5143daab)
 Call ID: 49a7378a-6aad-4c59-ad6f-5d4b5143daab
  Args:
    relation: :hasFather
    target: Frederick_III
    source: Waldemar_of_Prussia
  AddTriple (992b8562-c061-4825-8670-5b6162c4da22)
 Call ID: 992b8562-c061-4825-8670-5b6162c4da22
  Args:
    relation: :hasMother
    target: Victoria_Empress
    source: Waldemar_of_Prussia
  AssignClass (2d30521c-fa8e-4bb4-9707-665e276afa02)
 Call ID: 2d30521c-fa8e-4bb4-9707-665e276afa02
  Args:
    type: :Person
    source: William_I
  AssignClass (e7793ec8-adb6-4487-90d9-3e5f3bf5465b)
 Call ID: e7793ec8-adb6-4487-90d9-3e5f3bf5465b
  Args:
    type: :Man
    source: William_I
  AssignClass (33139488-ddb0-4870-b289-fa2cf47a8884)
 Call ID: 33139488-ddb0-4870-b289-fa2cf47a8884
  Args:
    type: :Person
    source: Queen_Victoria
  AssignClass (653f701b-68ec-4a92-a4e3-74110973ef55)
 Call ID: 653f701b-68ec-4a92-a4e3-74110973ef55
  Args:
    type: :Woman
    source: Queen_Victoria
  AddTriple (dc8f75ff-4eb9-4f37-9c71-c775b4fc512d)
 Call ID: dc8f75ff-4eb9-4f37-9c71-c775b4fc512d
  Args:
    source: Waldemar_of_Prussia
    target: William_I
    relation: :hasAncestor
  AddTriple (4d8d675e-a878-421d-8666-cf393e782577)
 Call ID: 4d8d675e-a878-421d-8666-cf393e782577
  Args:
    source: Waldemar_of_Prussia
    target: Queen_Victoria
    relation: :hasAncestor
  AssignClass (7b76b6d3-8de2-4050-96e6-8b6f26cea43f)
 Call ID: 7b76b6d3-8de2-4050-96e6-8b6f26cea43f
  Args:
    type: :Person
    source: Wilhelm_of_Prussia
  AssignClass (50b73975-ed27-4451-9717-bb7a95b90171)
 Call ID: 50b73975-ed27-4451-9717-bb7a95b90171
  Args:
    type: :Man
    source: Wilhelm_of_Prussia
  AssignClass (28474008-0e00-4271-b829-fbb3cf55ebac)
 Call ID: 28474008-0e00-4271-b829-fbb3cf55ebac
  Args:
    type: :Person
    source: Heinrich_of_Prussia
  AssignClass (a3fd739f-1f44-4b52-b8ab-4b6ef056d6bd)
 Call ID: a3fd739f-1f44-4b52-b8ab-4b6ef056d6bd
  Args:
    type: :Man
    source: Heinrich_of_Prussia
  AddTriple (0328b039-9773-4d62-b16a-75099713197e)
 Call ID: 0328b039-9773-4d62-b16a-75099713197e
  Args:
    source: Waldemar_of_Prussia
    target: Wilhelm_of_Prussia
    relation: :isSiblingOf
  AddTriple (4c213327-223f-4a39-ac56-f987c46dfda5)
 Call ID: 4c213327-223f-4a39-ac56-f987c46dfda5
  Args:
    source: Waldemar_of_Prussia
    target: Heinrich_of_Prussia
    relation: :isSiblingOf
  AssignClass (187998b4-0bb1-45f5-a50b-432f610bb231)
 Call ID: 187998b4-0bb1-45f5-a50b-432f610bb231
  Args:
    type: :Person
    source: Alice_of_Hesse
  AssignClass (faf4b59a-47d9-4a3b-be2d-6fdc09feaf41)
 Call ID: faf4b59a-47d9-4a3b-be2d-6fdc09feaf41
  Args:
    type: :Woman
    source: Alice_of_Hesse
  AddTriple (bf2abe6d-2f56-4c01-9096-e23dac8b69e7)
 Call ID: bf2abe6d-2f56-4c01-9096-e23dac8b69e7
  Args:
    target: Alice_of_Hesse
    relation: :hasRelation
    source: Waldemar_of_Prussia
  AssignClass (261326a2-0e83-46ec-82f9-6a9137f44324)
 Call ID: 261326a2-0e83-46ec-82f9-6a9137f44324
  Args:
    type: :Person
    source: Marie_of_Hesse
  AssignClass (3098e08a-7bde-433c-ade5-31691f04d220)
 Call ID: 3098e08a-7bde-433c-ade5-31691f04d220
  Args:
    type: :Woman
    source: Marie_of_Hesse
  AddTriple (e461dc2d-690d-4831-8f41-01c3d52b06b8)
 Call ID: e461dc2d-690d-4831-8f41-01c3d52b06b8
  Args:
    source: Waldemar_of_Prussia
    target: Marie_of_Hesse
    relation: :hasRelation
  AssignClass (145aae20-9137-4001-b16c-d3802bb9b60c)
 Call ID: 145aae20-9137-4001-b16c-d3802bb9b60c
  Args:
    type: :Person
    source: Sigismund_of_Prussia
  AssignClass (16397017-47c2-49b2-9ad4-c458a79cae69)
 Call ID: 16397017-47c2-49b2-9ad4-c458a79cae69
  Args:
    type: :Man
    source: Sigismund_of_Prussia
  AddTriple (88486b1f-3969-4e3a-9cc9-c7cacfded7c4)
 Call ID: 88486b1f-3969-4e3a-9cc9-c7cacfded7c4
  Args:
    target: Sigismund_of_Prussia
    relation: :isSiblingOf
    source: Waldemar_of_Prussia
  Finish (aeacc583-1dfd-47cb-9812-ec4e06fbf5f2)
 Call ID: aeacc583-1dfd-47cb-9812-ec4e06fbf5f2
  Args: