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
Bernhard, Prince of Saxe-Meiningen (German: Bernhard, Prinz von Sachsen-Meiningen; 30 June 1901 – 4 October 1984) was the head of the House of Saxe-Meiningen from 1946 until his death.
Prince of Saxe-Meiningen

Bernhard was born in Köln the third son of Prince Frederick Johann of Saxe-Meiningen and Countess Adelaide of Lippe-Biesterfeld.
His father was the second son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
After the death of his older brother Prince Georg in 1946 his nephew Prince Frederick Alfred renounced his succession rights and so Bernhard succeeded to the headship of the house of Saxe-Meiningen and the nominal title of Duke of Saxe-Meiningen (as Bernhard IV).
As his first marriage was morganatic his second son Prince Frederick Konrad succeeded him as head of the ducal house following his death in Bad Krozingen.
Bernhard and his first wife were declared guilty of a Nazi conspiracy against Austria in 1933; he was sentenced to six weeks in prison, while she was placed under house arrest.
Family

Bernhard was married morganatically to Margot Grössler (1911–1998), from Wrocław, daughter of Friedrich Grössler, a merchant, and Erika Wägner, in Eichenhof
They had two children, both of whom had no succession rights:


Bernhard married secondly in Ziegenberg über Bad Nauheim on 11 August 1948 to Baroness Vera Schäffer von Bernstein (1914–1994), daughter of Baron Friedrich "Fritz" Schäffer von Bernstein (1868–1958) and Emma Carola, née Passavant (1884–1971).
They had three children, including a son, Konrad, with full rights to the succession to the house of Saxe-Meiningen:


Ancestry

References



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
  AssignClass (07cd4b3a-eb9e-4f13-996c-2cf63364ea61)
 Call ID: 07cd4b3a-eb9e-4f13-996c-2cf63364ea61
  Args:
    type: :Man
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (25bab6fb-98d9-4bc8-8cca-f854e7f7309a)
 Call ID: 25bab6fb-98d9-4bc8-8cca-f854e7f7309a
  Args:
    type: :Person
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddLiteral (2cf07c55-a74c-4dc1-acd3-9bf5c092e3cf)
 Call ID: 2cf07c55-a74c-4dc1-acd3-9bf5c092e3cf
  Args:
    literal_value: 1901
    literal_type: xsd:positiveInteger
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasBirthYear
  AddLiteral (5b013b9b-0ca4-4dd6-a0f0-a18739526b5c)
 Call ID: 5b013b9b-0ca4-4dd6-a0f0-a18739526b5c
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1984
    relation: :hasDeathYear
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (60c5fd6b-49dc-4fbb-ae81-eac572ce1c55)
 Call ID: 60c5fd6b-49dc-4fbb-ae81-eac572ce1c55
  Args:
    type: :Man
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (4eb3d478-5cfe-40c4-8a98-2164f12162de)
 Call ID: 4eb3d478-5cfe-40c4-8a98-2164f12162de
  Args:
    type: :Person
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AddTriple (0bbcf870-5ec9-45d1-8faa-508ebf1021a1)
 Call ID: 0bbcf870-5ec9-45d1-8faa-508ebf1021a1
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (cb7bb0c8-ee21-4006-b283-18fbe55a5c41)
 Call ID: cb7bb0c8-ee21-4006-b283-18fbe55a5c41
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (f39d1c07-7abc-42b7-854e-6ee8d1cd8f44)
 Call ID: f39d1c07-7abc-42b7-854e-6ee8d1cd8f44
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (5b1e998b-b68b-4c12-b7f6-11dd872e9473)
 Call ID: 5b1e998b-b68b-4c12-b7f6-11dd872e9473
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasMother
    target: Countess_Adelaide_of_Lippe-Biesterfeld
  AssignClass (1fbdaa85-54c7-45ea-9da3-b551fe56874b)
 Call ID: 1fbdaa85-54c7-45ea-9da3-b551fe56874b
  Args:
    type: :Man
    source: Georg_II_Duke_of_Saxe-Meiningen
  AssignClass (fa2bf5e4-50ef-4874-ac98-397cd5ca3897)
 Call ID: fa2bf5e4-50ef-4874-ac98-397cd5ca3897
  Args:
    type: :Person
    source: Georg_II_Duke_of_Saxe-Meiningen
  AddTriple (9f85d710-3d81-40a4-9bac-e99d9a5c6202)
 Call ID: 9f85d710-3d81-40a4-9bac-e99d9a5c6202
  Args:
    target: Georg_II_Duke_of_Saxe-Meiningen
    relation: :hasFather
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (6ee88f86-086e-40ef-9657-1f0ea47857c1)
 Call ID: 6ee88f86-086e-40ef-9657-1f0ea47857c1
  Args:
    type: :Man
    source: Count_Ernst_of_Lippe-Biesterfeld
  AssignClass (78c027da-0a11-44e5-b23b-43b601e76fb9)
 Call ID: 78c027da-0a11-44e5-b23b-43b601e76fb9
  Args:
    type: :Person
    source: Count_Ernst_of_Lippe-Biesterfeld
  AddTriple (1dd7ad68-4463-40a3-be5a-9b16152d7e1a)
 Call ID: 1dd7ad68-4463-40a3-be5a-9b16152d7e1a
  Args:
    relation: :hasFather
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    target: Count_Ernst_of_Lippe-Biesterfeld
  AssignClass (ea4001c2-4a0c-4db1-ad51-7ae6c16f6119)
 Call ID: ea4001c2-4a0c-4db1-ad51-7ae6c16f6119
  Args:
    type: :Man
    source: Prince_Georg
  AssignClass (b60b4afd-7d72-4f5e-a669-54b980ff42b8)
 Call ID: b60b4afd-7d72-4f5e-a669-54b980ff42b8
  Args:
    type: :Person
    source: Prince_Georg
  AddTriple (67aad7f9-8d2a-42d1-978c-4ea9c40f10d6)
 Call ID: 67aad7f9-8d2a-42d1-978c-4ea9c40f10d6
  Args:
    target: Bernhard_Prince_of_Saxe-Meiningen
    relation: :isBrotherOf
    source: Prince_Georg
  AssignClass (0a55b5ea-91c0-4729-a225-8202cebbf24d)
 Call ID: 0a55b5ea-91c0-4729-a225-8202cebbf24d
  Args:
    type: :Man
    source: Prince_Frederick_Alfred
  AssignClass (fb976883-62a3-4355-8c10-825f37163534)
 Call ID: fb976883-62a3-4355-8c10-825f37163534
  Args:
    type: :Person
    source: Prince_Frederick_Alfred
  AddTriple (fa67baaa-5a20-4ca7-ac3d-c66c35c4574f)
 Call ID: fa67baaa-5a20-4ca7-ac3d-c66c35c4574f
  Args:
    target: Prince_Georg
    source: Prince_Frederick_Alfred
    relation: :hasFather
  AssignClass (c29e2cd2-63f8-43cf-8b68-132fd7bf646e)
 Call ID: c29e2cd2-63f8-43cf-8b68-132fd7bf646e
  Args:
    type: :Woman
    source: Margot_Grössler
  AssignClass (4852d22f-b02d-4ac6-bb50-2465de2997f4)
 Call ID: 4852d22f-b02d-4ac6-bb50-2465de2997f4
  Args:
    type: :Person
    source: Margot_Grössler
  AddLiteral (4b23ac7c-5f0f-4fef-932f-ff7761f63fa0)
 Call ID: 4b23ac7c-5f0f-4fef-932f-ff7761f63fa0
  Args:
    literal_value: 1911
    literal_type: xsd:positiveInteger
    source: Margot_Grössler
    relation: :hasBirthYear
  AddLiteral (19047ad8-973e-4b52-8a17-dd887dc57e87)
 Call ID: 19047ad8-973e-4b52-8a17-dd887dc57e87
  Args:
    source: Margot_Grössler
    relation: :hasDeathYear
    literal_value: 1998
    literal_type: xsd:positiveInteger
  AddTriple (15fa0f79-07e4-4684-82e0-0eaa9624217b)
 Call ID: 15fa0f79-07e4-4684-82e0-0eaa9624217b
  Args:
    target: Margot_Grössler
    source: Bernhard_Prince_of_Saxe-Meiningen
    relation: :hasRelation
  AssignClass (f14ba0af-145c-48f3-9c36-75b46bf43b53)
 Call ID: f14ba0af-145c-48f3-9c36-75b46bf43b53
  Args:
    type: :Man
    source: Friedrich_Grössler
  AssignClass (19ca824f-d23d-4ef6-b124-867007b78cea)
 Call ID: 19ca824f-d23d-4ef6-b124-867007b78cea
  Args:
    type: :Person
    source: Friedrich_Grössler
  AddTriple (f67c6cac-112f-4f45-b5f8-157322a94c1e)
 Call ID: f67c6cac-112f-4f45-b5f8-157322a94c1e
  Args:
    target: Friedrich_Grössler
    relation: :hasFather
    source: Margot_Grössler
  AssignClass (77f21dcd-7d0b-4dea-bac3-2076f681fff7)
 Call ID: 77f21dcd-7d0b-4dea-bac3-2076f681fff7
  Args:
    type: :Woman
    source: Erika_Wägner
  AssignClass (d5238a18-2542-4f0e-9351-4917eba3eaf1)
 Call ID: d5238a18-2542-4f0e-9351-4917eba3eaf1
  Args:
    type: :Person
    source: Erika_Wägner
  AddTriple (8060d648-a85b-4328-8858-277b6a6afbb7)
 Call ID: 8060d648-a85b-4328-8858-277b6a6afbb7
  Args:
    target: Erika_Wägner
    relation: :hasMother
    source: Margot_Grössler
  AssignClass (83c38b71-f120-4eda-84bd-ca575cb9c9aa)
 Call ID: 83c38b71-f120-4eda-84bd-ca575cb9c9aa
  Args:
    type: :Man
    source: Prince_Frederick_Konrad
  AssignClass (6b5010b3-de3d-43a5-adf0-13446f66d5b2)
 Call ID: 6b5010b3-de3d-43a5-adf0-13446f66d5b2
  Args:
    type: :Person
    source: Prince_Frederick_Konrad
  AddTriple (8273b441-1a96-4074-94ef-6f24ee416fdd)
 Call ID: 8273b441-1a96-4074-94ef-6f24ee416fdd
  Args:
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Prince_Frederick_Konrad
    relation: :hasFather
  AddTriple (51cbe193-27db-4792-aa9d-481752b7d4af)
 Call ID: 51cbe193-27db-4792-aa9d-481752b7d4af
  Args:
    relation: :hasMother
    source: Prince_Frederick_Konrad
    target: Margot_Grössler
  AssignClass (be3198e5-362c-4873-afd6-453156d277b4)
 Call ID: be3198e5-362c-4873-afd6-453156d277b4
  Args:
    type: :Woman
    source: Baroness_Vera_Schäffer_von_Bernstein
  AssignClass (d7fe20bb-c50c-4cc7-86ce-2a446250ab55)
 Call ID: d7fe20bb-c50c-4cc7-86ce-2a446250ab55
  Args:
    type: :Person
    source: Baroness_Vera_Schäffer_von_Bernstein
  AddLiteral (3a9cee2b-cc16-4cad-b299-557c16e4acca)
 Call ID: 3a9cee2b-cc16-4cad-b299-557c16e4acca
  Args:
    literal_value: 1914
    literal_type: xsd:positiveInteger
    source: Baroness_Vera_Schäffer_von_Bernstein
    relation: :hasBirthYear
  AddLiteral (58e970d2-c939-495a-9977-6b3062f7ef88)
 Call ID: 58e970d2-c939-495a-9977-6b3062f7ef88
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1994
    relation: :hasDeathYear
    source: Baroness_Vera_Schäffer_von_Bernstein
  AddLiteral (fe818f30-ec33-4035-a1fc-da7d89b7fcad)
 Call ID: fe818f30-ec33-4035-a1fc-da7d89b7fcad
  Args:
    relation: :hasMarriageYear
    source: Baroness_Vera_Schäffer_von_Bernstein
    literal_type: xsd:positiveInteger
    literal_value: 1948
  AddTriple (96340f2f-1b9b-4fda-b699-8d2c77517821)
 Call ID: 96340f2f-1b9b-4fda-b699-8d2c77517821
  Args:
    relation: :hasRelation
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Baroness_Vera_Schäffer_von_Bernstein
  AssignClass (717a31fe-5d03-4f6a-8822-1057dc41463d)
 Call ID: 717a31fe-5d03-4f6a-8822-1057dc41463d
  Args:
    type: :Man
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
  AssignClass (ced6561a-96df-49cf-96cb-b913c73aea28)
 Call ID: ced6561a-96df-49cf-96cb-b913c73aea28
  Args:
    type: :Person
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
  AddLiteral (e4d7d19d-94aa-4c41-85e4-10c2d7efb713)
 Call ID: e4d7d19d-94aa-4c41-85e4-10c2d7efb713
  Args:
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    relation: :hasBirthYear
    literal_value: 1868
    literal_type: xsd:positiveInteger
  AddLiteral (d02c04ba-fec1-4124-9726-91a5dd6eae97)
 Call ID: d02c04ba-fec1-4124-9726-91a5dd6eae97
  Args:
    literal_value: 1958
    literal_type: xsd:positiveInteger
    source: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
    relation: :hasDeathYear
  AddTriple (d97b81c2-665d-4ec0-b345-a3739398d9f7)
 Call ID: d97b81c2-665d-4ec0-b345-a3739398d9f7
  Args:
    relation: :hasFather
    source: Baroness_Vera_Schäffer_von_Bernstein
    target: Baron_Friedrich_Fritz_Schäffer_von_Bernstein
  AssignClass (96f2aeb3-2914-4b2e-b879-9b15f0d0070a)
 Call ID: 96f2aeb3-2914-4b2e-b879-9b15f0d0070a
  Args:
    type: :Woman
    source: Emma_Carola_Passavant
  AssignClass (ab4d6f59-9b1d-4cd4-891e-0bdde62f207c)
 Call ID: ab4d6f59-9b1d-4cd4-891e-0bdde62f207c
  Args:
    type: :Person
    source: Emma_Carola_Passavant
  AddLiteral (339ae5cc-44ac-497b-ab86-02175f321230)
 Call ID: 339ae5cc-44ac-497b-ab86-02175f321230
  Args:
    relation: :hasBirthYear
    source: Emma_Carola_Passavant
    literal_type: xsd:positiveInteger
    literal_value: 1884
  AddLiteral (ee01f707-c8ab-4a53-b8ea-fd70e48b037b)
 Call ID: ee01f707-c8ab-4a53-b8ea-fd70e48b037b
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1971
    relation: :hasDeathYear
    source: Emma_Carola_Passavant
  AddTriple (ba20b49c-d729-4a4a-bf50-361386cd2928)
 Call ID: ba20b49c-d729-4a4a-bf50-361386cd2928
  Args:
    target: Emma_Carola_Passavant
    relation: :hasMother
    source: Baroness_Vera_Schäffer_von_Bernstein
  AssignClass (4229d697-1853-422d-9802-0daf537f80f7)
 Call ID: 4229d697-1853-422d-9802-0daf537f80f7
  Args:
    type: :Man
    source: Konrad_of_Saxe-Meiningen
  AssignClass (807ea3d1-b932-4106-a6c8-5df96919ec1e)
 Call ID: 807ea3d1-b932-4106-a6c8-5df96919ec1e
  Args:
    type: :Person
    source: Konrad_of_Saxe-Meiningen
  AddTriple (04689ec8-d135-4818-88b8-2268585091c7)
 Call ID: 04689ec8-d135-4818-88b8-2268585091c7
  Args:
    source: Konrad_of_Saxe-Meiningen
    relation: :hasFather
    target: Bernhard_Prince_of_Saxe-Meiningen
  AddTriple (ecd4f5bd-3cdc-4e15-bc1b-c49277459116)
 Call ID: ecd4f5bd-3cdc-4e15-bc1b-c49277459116
  Args:
    relation: :hasMother
    source: Konrad_of_Saxe-Meiningen
    target: Baroness_Vera_Schäffer_von_Bernstein
  Finish (5d05600b-efbd-4402-adcf-56d032392637)
 Call ID: 5d05600b-efbd-4402-adcf-56d032392637
  Args: