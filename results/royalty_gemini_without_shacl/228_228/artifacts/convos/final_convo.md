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
  AssignClass (8bacd6c2-a95a-4b3a-b1d6-28ab633ef53e)
 Call ID: 8bacd6c2-a95a-4b3a-b1d6-28ab633ef53e
  Args:
    type: :Person
    source: :Waldemar_of_Prussia
  AssignClass (f8f30678-3848-409a-8edb-ae15e2580f71)
 Call ID: f8f30678-3848-409a-8edb-ae15e2580f71
  Args:
    type: :Man
    source: :Waldemar_of_Prussia
  AddLiteral (00f84935-b3aa-4ed9-9e7e-2eded5fdf2bf)
 Call ID: 00f84935-b3aa-4ed9-9e7e-2eded5fdf2bf
  Args:
    literal_value: Joachim Friedrich Ernst Waldemar
    literal_type: xsd:string
    source: :Waldemar_of_Prussia
    relation: :alsoKnownAs
  AddLiteral (f9d82a33-4e56-43e9-b5f5-ab4d768ef04c)
 Call ID: f9d82a33-4e56-43e9-b5f5-ab4d768ef04c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1868
    source: :Waldemar_of_Prussia
  AddLiteral (3a1b7c75-3bcc-496f-81c9-9641a22e210a)
 Call ID: 3a1b7c75-3bcc-496f-81c9-9641a22e210a
  Args:
    literal_value: 1879
    literal_type: xsd:integer
    source: :Waldemar_of_Prussia
    relation: :hasDeathYear
  AssignClass (e1389054-7029-455b-a000-5da2d316b775)
 Call ID: e1389054-7029-455b-a000-5da2d316b775
  Args:
    source: :Frederick_III
    type: :Person
  AssignClass (4bcefefc-318f-4564-b857-16788f96fc05)
 Call ID: 4bcefefc-318f-4564-b857-16788f96fc05
  Args:
    source: :Frederick_III
    type: :Man
  AssignClass (ff3f7b9e-a5e4-40a6-9f4f-2bac7a7a5184)
 Call ID: ff3f7b9e-a5e4-40a6-9f4f-2bac7a7a5184
  Args:
    source: :Victoria_Empress
    type: :Person
  AssignClass (9d9e1282-d51f-4a0f-8dcc-656ca1ed700e)
 Call ID: 9d9e1282-d51f-4a0f-8dcc-656ca1ed700e
  Args:
    type: :Woman
    source: :Victoria_Empress
  AddTriple (3a578d09-840a-4a54-8d1e-d56a75e3daf1)
 Call ID: 3a578d09-840a-4a54-8d1e-d56a75e3daf1
  Args:
    source: :Waldemar_of_Prussia
    target: :Frederick_III
    relation: :hasFather
  AddTriple (6f3f719e-e839-4758-892a-7bf1a0cd5a83)
 Call ID: 6f3f719e-e839-4758-892a-7bf1a0cd5a83
  Args:
    source: :Waldemar_of_Prussia
    target: :Victoria_Empress
    relation: :hasMother
  AssignClass (11853cf0-e245-4d9c-b8de-baf2043dc98c)
 Call ID: 11853cf0-e245-4d9c-b8de-baf2043dc98c
  Args:
    type: :Person
    source: :William_I
  AssignClass (7933891d-d7a1-4fd1-a8eb-8c583d5537b1)
 Call ID: 7933891d-d7a1-4fd1-a8eb-8c583d5537b1
  Args:
    type: :Man
    source: :William_I
  AssignClass (bdc5e158-78ef-496f-beb3-051d0a98b2c7)
 Call ID: bdc5e158-78ef-496f-beb3-051d0a98b2c7
  Args:
    source: :Victoria_Queen
    type: :Person
  AssignClass (cc3cc4af-12d0-4fd9-bf71-33f2b50867ff)
 Call ID: cc3cc4af-12d0-4fd9-bf71-33f2b50867ff
  Args:
    type: :Woman
    source: :Victoria_Queen
  AddTriple (a6aaa39e-e6c5-43d9-97cb-b5ad2a3f0c8b)
 Call ID: a6aaa39e-e6c5-43d9-97cb-b5ad2a3f0c8b
  Args:
    target: :William_I
    relation: :hasAncestor
    source: :Waldemar_of_Prussia
  AddTriple (76f9b2ed-61b3-46b7-92b9-e6ecb816fe54)
 Call ID: 76f9b2ed-61b3-46b7-92b9-e6ecb816fe54
  Args:
    target: :Victoria_Queen
    relation: :hasAncestor
    source: :Waldemar_of_Prussia
  AssignClass (36161e29-3c09-444b-98b1-0d25138e8c11)
 Call ID: 36161e29-3c09-444b-98b1-0d25138e8c11
  Args:
    source: :Wilhelm
    type: :Person
  AssignClass (14f92e8d-32bc-42ed-b018-5ff724ea5429)
 Call ID: 14f92e8d-32bc-42ed-b018-5ff724ea5429
  Args:
    type: :Man
    source: :Wilhelm
  AssignClass (0ece3958-972e-4518-8bd4-2686f495f8d2)
 Call ID: 0ece3958-972e-4518-8bd4-2686f495f8d2
  Args:
    type: :Person
    source: :Heinrich
  AssignClass (32fb8bc6-ecf0-46d3-991e-8d512b45b018)
 Call ID: 32fb8bc6-ecf0-46d3-991e-8d512b45b018
  Args:
    type: :Man
    source: :Heinrich
  AddTriple (1d2d9fe2-01ec-48d7-b594-eb35ecda6452)
 Call ID: 1d2d9fe2-01ec-48d7-b594-eb35ecda6452
  Args:
    target: :Wilhelm
    relation: :isSiblingOf
    source: :Waldemar_of_Prussia
  AddTriple (71ae48ce-6fab-4bf8-8459-83896775f1f4)
 Call ID: 71ae48ce-6fab-4bf8-8459-83896775f1f4
  Args:
    relation: :isSiblingOf
    target: :Heinrich
    source: :Waldemar_of_Prussia
  AssignClass (f545bb16-5659-4270-a4b5-20600b714321)
 Call ID: f545bb16-5659-4270-a4b5-20600b714321
  Args:
    type: :Person
    source: :Alice_of_Hesse
  AssignClass (eaba6041-90ea-422e-99c4-f41ea44cc6d1)
 Call ID: eaba6041-90ea-422e-99c4-f41ea44cc6d1
  Args:
    type: :Woman
    source: :Alice_of_Hesse
  AssignClass (160e81fe-7811-4414-bf2c-3261edac1840)
 Call ID: 160e81fe-7811-4414-bf2c-3261edac1840
  Args:
    source: :Marie_of_Hesse
    type: :Person
  AssignClass (301ea84e-ec93-4e94-9059-e3363e3b12f8)
 Call ID: 301ea84e-ec93-4e94-9059-e3363e3b12f8
  Args:
    type: :Woman
    source: :Marie_of_Hesse
  AddTriple (d76632aa-ddae-4902-b6e1-2a475e61a7b5)
 Call ID: d76632aa-ddae-4902-b6e1-2a475e61a7b5
  Args:
    target: :Waldemar_of_Prussia
    relation: :isAuntOf
    source: :Alice_of_Hesse
  AssignClass (61c6ea14-6dff-4178-9410-8dabef79ad4f)
 Call ID: 61c6ea14-6dff-4178-9410-8dabef79ad4f
  Args:
    type: :Person
    source: :Sigismund_of_Prussia
  AssignClass (e145c147-d366-4aea-a39f-d6fa67ee882e)
 Call ID: e145c147-d366-4aea-a39f-d6fa67ee882e
  Args:
    source: :Sigismund_of_Prussia
    type: :Man
  AddTriple (880a92e5-b02b-48cb-9e30-df0bd987d7a1)
 Call ID: 880a92e5-b02b-48cb-9e30-df0bd987d7a1
  Args:
    source: :Waldemar_of_Prussia
    relation: :isSiblingOf
    target: :Sigismund_of_Prussia
  Finish (996f9973-329c-45f7-998f-b224655b364e)
 Call ID: 996f9973-329c-45f7-998f-b224655b364e
  Args: