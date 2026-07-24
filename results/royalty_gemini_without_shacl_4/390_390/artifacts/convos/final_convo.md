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
Franz Wilhelm Victor Christoph Stephan Prinz von Preussen (born 3 September 1943) is a German businessman and member of the House of Hohenzollern, the former ruling German imperial house and royal house of Prussia.
He is also the great-grandson of German Emperor Wilhelm II.
Biography

Franz Wilhelm Prince of Prussia was born in Grünberg, Silesia, as the son of Prince Karl Franz of Prussia and his first wife Princess Henriette von Schönaich-Carolath.
He had a twin brother, Prince Friedrich Christian, who died three weeks after his birth.
Prince Franz Wilhelm is a grandson of Prince Joachim of Prussia, the youngest son of Emperor Wilhelm II.
In 2002 Franz Wilhelm with Theodor Tantzen founded the Prinz von Preußen Grundbesitz AG, a project development and project management company which restores old buildings in Germany.
Personal life

Franz Wilhelm married his third cousin once removed, Grand Duchess Maria Vladimirovna of Russia, great-great-granddaughter of Queen Victoria, civilly on 4 September 1976 at Dinard and religiously on 22 September at the Russian Orthodox Chapel in Madrid.
Before his marriage, he converted to the Russian Orthodox faith and was created a Grand Duke of Russia with the name Mikhail Pavlovich by his father-in-law Grand Duke Vladimir of Russia.
Franz Wilhelm and Grand Duchess Maria had one son before divorcing on 19 June 1985 (they separated in 1982), at which point he reverted to his previous title.
He married Nadia Nour El Etreby (born 2 August 1949) on 14 March 2019, to whom was bestowed upon marriage the courtesy style and title of Her Royal Highness Princess Franz Wilhelm of Prussia.



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
  AssignClass (f5cb7d16-e85c-46c7-a0d5-1fedb0e4dba5)
 Call ID: f5cb7d16-e85c-46c7-a0d5-1fedb0e4dba5
  Args:
    type: :Man
    source: Franz_Wilhelm_Prinz_von_Preussen
  AssignClass (8ee72137-f6c5-4fe9-9232-b1ffd92ce43c)
 Call ID: 8ee72137-f6c5-4fe9-9232-b1ffd92ce43c
  Args:
    type: :Person
    source: Franz_Wilhelm_Prinz_von_Preussen
  AddLiteral (59c2f1dc-e211-4295-ad97-498ea1e0e78b)
 Call ID: 59c2f1dc-e211-4295-ad97-498ea1e0e78b
  Args:
    literal_type: xsd:nonNegativeInteger
    source: Franz_Wilhelm_Prinz_von_Preussen
    relation: :hasBirthYear
    literal_value: 1943
  AssignClass (437d2d63-90c0-4876-8a5e-0f9bfc0cb7df)
 Call ID: 437d2d63-90c0-4876-8a5e-0f9bfc0cb7df
  Args:
    type: :Man
    source: Karl_Franz_of_Prussia
  AssignClass (d1e4dcf9-c9f5-44bf-8b51-9b0a133f7b63)
 Call ID: d1e4dcf9-c9f5-44bf-8b51-9b0a133f7b63
  Args:
    type: :Person
    source: Karl_Franz_of_Prussia
  AddTriple (1d37ad52-cd6c-4ef7-aab0-9f03e5d48b34)
 Call ID: 1d37ad52-cd6c-4ef7-aab0-9f03e5d48b34
  Args:
    target: Karl_Franz_of_Prussia
    relation: :hasFather
    source: Franz_Wilhelm_Prinz_von_Preussen
  AssignClass (5f3ac240-094c-4200-a517-ebe846a84eac)
 Call ID: 5f3ac240-094c-4200-a517-ebe846a84eac
  Args:
    type: :Woman
    source: Henriette_von_Schönaich-Carolath
  AssignClass (a354e1bc-e11f-460d-93a4-22dc383a4124)
 Call ID: a354e1bc-e11f-460d-93a4-22dc383a4124
  Args:
    type: :Person
    source: Henriette_von_Schönaich-Carolath
  AddTriple (be053745-7ce4-4fac-a0e0-89236faa656e)
 Call ID: be053745-7ce4-4fac-a0e0-89236faa656e
  Args:
    source: Franz_Wilhelm_Prinz_von_Preussen
    relation: :hasMother
    target: Henriette_von_Schönaich-Carolath
  AssignClass (a2522a56-1868-4af1-a4f2-620e375a8105)
 Call ID: a2522a56-1868-4af1-a4f2-620e375a8105
  Args:
    type: :Man
    source: Friedrich_Christian_of_Prussia
  AssignClass (265ea77a-1c06-4b38-93e6-da2a1e4f8a79)
 Call ID: 265ea77a-1c06-4b38-93e6-da2a1e4f8a79
  Args:
    type: :Person
    source: Friedrich_Christian_of_Prussia
  AddTriple (7e5c5261-3203-4c45-8d1f-1a52d8dc977d)
 Call ID: 7e5c5261-3203-4c45-8d1f-1a52d8dc977d
  Args:
    target: Friedrich_Christian_of_Prussia
    relation: :isSiblingOf
    source: Franz_Wilhelm_Prinz_von_Preussen
  AssignClass (6684f67c-9f1f-411c-9e25-1cb7321a9dab)
 Call ID: 6684f67c-9f1f-411c-9e25-1cb7321a9dab
  Args:
    type: :Man
    source: Joachim_of_Prussia
  AssignClass (15b0d631-1c21-40d9-a549-3dbc8741bf94)
 Call ID: 15b0d631-1c21-40d9-a549-3dbc8741bf94
  Args:
    type: :Person
    source: Joachim_of_Prussia
  AddTriple (9791dc36-55e3-4c2c-8ccd-aa00fd851578)
 Call ID: 9791dc36-55e3-4c2c-8ccd-aa00fd851578
  Args:
    relation: :hasFather
    target: Joachim_of_Prussia
    source: Karl_Franz_of_Prussia
  AssignClass (f64c64c2-2aac-4b70-bfb2-7a456b341b5e)
 Call ID: f64c64c2-2aac-4b70-bfb2-7a456b341b5e
  Args:
    type: :Man
    source: Wilhelm_II_of_Germany
  AssignClass (9fe8621f-99fb-4d42-a50c-78988154659f)
 Call ID: 9fe8621f-99fb-4d42-a50c-78988154659f
  Args:
    type: :Person
    source: Wilhelm_II_of_Germany
  AddTriple (df3569a5-f928-49ff-afe0-252e2e569da3)
 Call ID: df3569a5-f928-49ff-afe0-252e2e569da3
  Args:
    source: Joachim_of_Prussia
    relation: :hasFather
    target: Wilhelm_II_of_Germany
  AssignClass (e1d214bb-8023-4084-80d2-ac38dfac93a8)
 Call ID: e1d214bb-8023-4084-80d2-ac38dfac93a8
  Args:
    type: :Woman
    source: Maria_Vladimirovna_of_Russia
  AssignClass (c39f16eb-a314-47f0-8840-bb9dc823385e)
 Call ID: c39f16eb-a314-47f0-8840-bb9dc823385e
  Args:
    type: :Person
    source: Maria_Vladimirovna_of_Russia
  AddLiteral (3e07be84-a194-41d3-8cdf-811c8d31b281)
 Call ID: 3e07be84-a194-41d3-8cdf-811c8d31b281
  Args:
    relation: :hasMarriageYear
    literal_value: 1976
    literal_type: xsd:nonNegativeInteger
    source: Franz_Wilhelm_Prinz_von_Preussen
  AddTriple (ee5fa801-85f6-473e-a7cd-42e8751159f2)
 Call ID: ee5fa801-85f6-473e-a7cd-42e8751159f2
  Args:
    source: Franz_Wilhelm_Prinz_von_Preussen
    relation: :hasRelation
    target: Maria_Vladimirovna_of_Russia
  AssignClass (21a05a73-7a65-4465-88b9-fe72b035938c)
 Call ID: 21a05a73-7a65-4465-88b9-fe72b035938c
  Args:
    type: :Man
    source: Vladimir_of_Russia
  AssignClass (1dd15a2c-8b6d-462d-9935-41529e56c3e4)
 Call ID: 1dd15a2c-8b6d-462d-9935-41529e56c3e4
  Args:
    type: :Person
    source: Vladimir_of_Russia
  AddTriple (9b44bbf9-07fd-47d2-9f5d-44bd78d85d91)
 Call ID: 9b44bbf9-07fd-47d2-9f5d-44bd78d85d91
  Args:
    source: Maria_Vladimirovna_of_Russia
    relation: :hasFather
    target: Vladimir_of_Russia
  AssignClass (84ef7949-443e-4b43-98f4-f9af76123304)
 Call ID: 84ef7949-443e-4b43-98f4-f9af76123304
  Args:
    type: :Woman
    source: Nadia_Nour_El_Etreby
  AssignClass (5bb613d3-31ca-4875-bcd0-02273d68b326)
 Call ID: 5bb613d3-31ca-4875-bcd0-02273d68b326
  Args:
    type: :Person
    source: Nadia_Nour_El_Etreby
  AddLiteral (3c9be26e-1f00-4cdc-ae45-08a334cf5382)
 Call ID: 3c9be26e-1f00-4cdc-ae45-08a334cf5382
  Args:
    literal_type: xsd:nonNegativeInteger
    source: Nadia_Nour_El_Etreby
    literal_value: 1949
    relation: :hasBirthYear
  AddLiteral (a1acfb54-cbff-4e35-a55d-7f50a3889564)
 Call ID: a1acfb54-cbff-4e35-a55d-7f50a3889564
  Args:
    literal_type: xsd:nonNegativeInteger
    source: Franz_Wilhelm_Prinz_von_Preussen
    relation: :hasMarriageYear
    literal_value: 2019
  AddTriple (da180a0c-f5f1-4717-bb79-70540176d2bf)
 Call ID: da180a0c-f5f1-4717-bb79-70540176d2bf
  Args:
    source: Franz_Wilhelm_Prinz_von_Preussen
    relation: :hasRelation
    target: Nadia_Nour_El_Etreby
  Finish (730605f6-1092-45d7-a6e2-c9f3c5316463)
 Call ID: 730605f6-1092-45d7-a6e2-c9f3c5316463
  Args: