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
  AssignClass (1eba91a4-02b7-4023-9ddd-ac2541999fc5)
 Call ID: 1eba91a4-02b7-4023-9ddd-ac2541999fc5
  Args:
    type: :Man
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (3c59d66b-e2a7-4991-86c2-2748f9eef7db)
 Call ID: 3c59d66b-e2a7-4991-86c2-2748f9eef7db
  Args:
    type: :Person
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddLiteral (4141a806-2643-4a75-b926-cb225f551170)
 Call ID: 4141a806-2643-4a75-b926-cb225f551170
  Args:
    literal_value: 1901
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
    source: Bernhard_Prince_of_Saxe-Meiningen
  AddLiteral (764ffca9-58e1-4449-9f8f-1f86e916ba0f)
 Call ID: 764ffca9-58e1-4449-9f8f-1f86e916ba0f
  Args:
    literal_type: xsd:positiveInteger
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_value: 1984
    relation: :hasDeathYear
  AssignClass (cc62b21a-e0cf-4d78-92d4-e23673538692)
 Call ID: cc62b21a-e0cf-4d78-92d4-e23673538692
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Man
  AssignClass (c72c5ee8-19ab-4f14-b862-e2a1bd8af749)
 Call ID: c72c5ee8-19ab-4f14-b862-e2a1bd8af749
  Args:
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
    type: :Person
  AddTriple (3e668ddb-a37b-433d-97d6-21684249c3b1)
 Call ID: 3e668ddb-a37b-433d-97d6-21684249c3b1
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Prince_Frederick_Johann_of_Saxe-Meiningen
    relation: :hasFather
  AssignClass (7cf9346c-563a-462e-a322-55ed04537386)
 Call ID: 7cf9346c-563a-462e-a322-55ed04537386
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    type: :Woman
  AssignClass (5f94ae39-882f-4ebd-94df-678ca259f681)
 Call ID: 5f94ae39-882f-4ebd-94df-678ca259f681
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe-Biesterfeld
  AddTriple (8b7c09a0-ca5b-46e1-8345-4daf44ba2740)
 Call ID: 8b7c09a0-ca5b-46e1-8345-4daf44ba2740
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Countess_Adelaide_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (985884a2-b0a2-4eb3-89cc-1f60a3bba734)
 Call ID: 985884a2-b0a2-4eb3-89cc-1f60a3bba734
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Man
  AssignClass (47866897-3322-43a0-a06f-bacf9632be30)
 Call ID: 47866897-3322-43a0-a06f-bacf9632be30
  Args:
    source: Georg_II_Duke_of_Saxe-Meiningen
    type: :Person
  AddTriple (4d1973c9-126a-48d5-b6db-a7f0fa29712b)
 Call ID: 4d1973c9-126a-48d5-b6db-a7f0fa29712b
  Args:
    relation: :hasFather
    target: Georg_II_Duke_of_Saxe-Meiningen
    source: Prince_Frederick_Johann_of_Saxe-Meiningen
  AssignClass (d8c4a3ae-779e-4b6e-811b-31907449e69d)
 Call ID: d8c4a3ae-779e-4b6e-811b-31907449e69d
  Args:
    source: Count_Ernst_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (abc37ed6-ec41-4efd-9db0-3f5f303d6688)
 Call ID: abc37ed6-ec41-4efd-9db0-3f5f303d6688
  Args:
    type: :Person
    source: Count_Ernst_of_Lippe-Biesterfeld
  AddTriple (312f4319-4a06-412c-af3b-1bd612a44cea)
 Call ID: 312f4319-4a06-412c-af3b-1bd612a44cea
  Args:
    source: Countess_Adelaide_of_Lippe-Biesterfeld
    target: Count_Ernst_of_Lippe-Biesterfeld
    relation: :hasFather
  AssignClass (bbed1161-2360-46b8-8a33-c141b51eae95)
 Call ID: bbed1161-2360-46b8-8a33-c141b51eae95
  Args:
    type: :Man
    source: Prince_Georg
  AssignClass (29956886-62f1-400c-9abf-cf16293be81c)
 Call ID: 29956886-62f1-400c-9abf-cf16293be81c
  Args:
    type: :Person
    source: Prince_Georg
  AddTriple (a8611295-07b2-4b6c-b4c6-3721e9681a07)
 Call ID: a8611295-07b2-4b6c-b4c6-3721e9681a07
  Args:
    relation: :hasBrother
    target: Prince_Georg
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (a70596c1-3dd0-4ad5-baa8-9204b1196ad0)
 Call ID: a70596c1-3dd0-4ad5-baa8-9204b1196ad0
  Args:
    type: :Man
    source: Prince_Frederick_Alfred
  AssignClass (bf65bd0c-8b1a-4cc7-b45f-051e1d0b755d)
 Call ID: bf65bd0c-8b1a-4cc7-b45f-051e1d0b755d
  Args:
    source: Prince_Frederick_Alfred
    type: :Person
  AssignClass (3e559d4f-40d8-45b3-ae51-184c82241d7f)
 Call ID: 3e559d4f-40d8-45b3-ae51-184c82241d7f
  Args:
    source: Prince_Frederick_Konrad
    type: :Man
  AssignClass (1f42f79e-c2bc-4d95-88c2-14115f9658d6)
 Call ID: 1f42f79e-c2bc-4d95-88c2-14115f9658d6
  Args:
    type: :Person
    source: Prince_Frederick_Konrad
  AddTriple (67a36e8d-ff8a-4d7f-b7c1-a3dd70d61faa)
 Call ID: 67a36e8d-ff8a-4d7f-b7c1-a3dd70d61faa
  Args:
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Prince_Frederick_Konrad
    relation: :hasFather
  AssignClass (3621bb7b-9752-478c-8f66-ec5bd48c2567)
 Call ID: 3621bb7b-9752-478c-8f66-ec5bd48c2567
  Args:
    source: Margot_Grössler
    type: :Woman
  AssignClass (1074b810-1117-4ff6-8e31-c2e6f6243a1a)
 Call ID: 1074b810-1117-4ff6-8e31-c2e6f6243a1a
  Args:
    type: :Person
    source: Margot_Grössler
  AddLiteral (a18e3fe7-adf0-43a7-873a-accc3a72a971)
 Call ID: a18e3fe7-adf0-43a7-873a-accc3a72a971
  Args:
    source: Margot_Grössler
    literal_type: xsd:positiveInteger
    literal_value: 1911
    relation: :hasBirthYear
  AddLiteral (4c70a99a-8ba0-4e6e-96a2-47fa1c2e996f)
 Call ID: 4c70a99a-8ba0-4e6e-96a2-47fa1c2e996f
  Args:
    source: Margot_Grössler
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1998
  AddTriple (7dc2be84-91fd-4eaa-8321-2369a25a0b32)
 Call ID: 7dc2be84-91fd-4eaa-8321-2369a25a0b32
  Args:
    source: Bernhard_Prince_of_Saxe-Meiningen
    target: Margot_Grössler
    relation: :hasRelation
  AssignClass (eb7ee187-e5ad-48f2-886f-7269c9d28601)
 Call ID: eb7ee187-e5ad-48f2-886f-7269c9d28601
  Args:
    source: Friedrich_Grössler
    type: :Man
  AssignClass (9b631ee6-f679-4a1e-9aec-d8d70ed1c4e9)
 Call ID: 9b631ee6-f679-4a1e-9aec-d8d70ed1c4e9
  Args:
    source: Friedrich_Grössler
    type: :Person
  AssignClass (71c3f6e5-3f33-4f1c-a0dc-0b6d1c4d0ebf)
 Call ID: 71c3f6e5-3f33-4f1c-a0dc-0b6d1c4d0ebf
  Args:
    source: Erika_Wägner
    type: :Woman
  AssignClass (c522ee30-1268-4d0b-8eed-72c1c30153b2)
 Call ID: c522ee30-1268-4d0b-8eed-72c1c30153b2
  Args:
    type: :Person
    source: Erika_Wägner
  AddTriple (e773085d-d6d4-4502-b479-048a64e437c3)
 Call ID: e773085d-d6d4-4502-b479-048a64e437c3
  Args:
    relation: :hasFather
    target: Friedrich_Grössler
    source: Margot_Grössler
  AddTriple (48b9d93e-8aad-4eca-824c-70ba61705468)
 Call ID: 48b9d93e-8aad-4eca-824c-70ba61705468
  Args:
    relation: :hasMother
    source: Margot_Grössler
    target: Erika_Wägner
  AssignClass (d089a6fe-aed4-4934-b276-30b4e756f8e1)
 Call ID: d089a6fe-aed4-4934-b276-30b4e756f8e1
  Args:
    source: Vera_Schäffer_von_Bernstein
    type: :Woman
  AssignClass (c752e4d3-f3e0-4f3d-ac5b-41c54e3f8ccf)
 Call ID: c752e4d3-f3e0-4f3d-ac5b-41c54e3f8ccf
  Args:
    type: :Person
    source: Vera_Schäffer_von_Bernstein
  AddLiteral (e3fe91ee-6778-4486-b717-0f35c60dcfed)
 Call ID: e3fe91ee-6778-4486-b717-0f35c60dcfed
  Args:
    literal_type: xsd:positiveInteger
    source: Vera_Schäffer_von_Bernstein
    relation: :hasBirthYear
    literal_value: 1914
  AddLiteral (0ce11952-105e-4846-8d63-2e103be59b38)
 Call ID: 0ce11952-105e-4846-8d63-2e103be59b38
  Args:
    relation: :hasDeathYear
    literal_value: 1994
    source: Vera_Schäffer_von_Bernstein
    literal_type: xsd:positiveInteger
  AddLiteral (2c58958d-70aa-4428-bc16-8dfcc6c8dc30)
 Call ID: 2c58958d-70aa-4428-bc16-8dfcc6c8dc30
  Args:
    relation: :hasMarriageYear
    literal_value: 1948
    source: Bernhard_Prince_of_Saxe-Meiningen
    literal_type: xsd:positiveInteger
  AddTriple (324c8bd2-98fc-4c97-b99e-7a5ce4446e87)
 Call ID: 324c8bd2-98fc-4c97-b99e-7a5ce4446e87
  Args:
    relation: :hasRelation
    target: Vera_Schäffer_von_Bernstein
    source: Bernhard_Prince_of_Saxe-Meiningen
  AssignClass (d5c162f3-f898-4c00-9ae3-fdfb88d1aed4)
 Call ID: d5c162f3-f898-4c00-9ae3-fdfb88d1aed4
  Args:
    type: :Man
    source: Baron_Friedrich_Schäffer_von_Bernstein
  AssignClass (484dee6f-77f8-40a5-a1c8-6d19aa6a3723)
 Call ID: 484dee6f-77f8-40a5-a1c8-6d19aa6a3723
  Args:
    source: Baron_Friedrich_Schäffer_von_Bernstein
    type: :Person
  AddLiteral (be61514c-6372-4703-91c9-7cc17e704b8a)
 Call ID: be61514c-6372-4703-91c9-7cc17e704b8a
  Args:
    relation: :hasBirthYear
    literal_value: 1868
    literal_type: xsd:positiveInteger
    source: Baron_Friedrich_Schäffer_von_Bernstein
  AddLiteral (9c1b3443-729f-4d0f-811f-876be62ded88)
 Call ID: 9c1b3443-729f-4d0f-811f-876be62ded88
  Args:
    relation: :hasDeathYear
    literal_value: 1958
    literal_type: xsd:positiveInteger
    source: Baron_Friedrich_Schäffer_von_Bernstein
  AssignClass (0aa1c060-44c6-4a2e-8fe5-848c49786257)
 Call ID: 0aa1c060-44c6-4a2e-8fe5-848c49786257
  Args:
    source: Emma_Carola_Passavant
    type: :Woman
  AssignClass (5acef0be-5059-4c3a-83c9-2bd2308e8a44)
 Call ID: 5acef0be-5059-4c3a-83c9-2bd2308e8a44
  Args:
    type: :Person
    source: Emma_Carola_Passavant
  AddLiteral (545044c1-35ef-4f3d-8989-1a0c2d8bea59)
 Call ID: 545044c1-35ef-4f3d-8989-1a0c2d8bea59
  Args:
    source: Emma_Carola_Passavant
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1884
  AddLiteral (c9098da0-79c2-44b4-b8e1-85710d25a2c2)
 Call ID: c9098da0-79c2-44b4-b8e1-85710d25a2c2
  Args:
    relation: :hasDeathYear
    literal_value: 1971
    source: Emma_Carola_Passavant
    literal_type: xsd:positiveInteger
  AddTriple (f3cdcc7e-cbbc-4dc1-890a-801fe6dd2b65)
 Call ID: f3cdcc7e-cbbc-4dc1-890a-801fe6dd2b65
  Args:
    relation: :hasFather
    source: Vera_Schäffer_von_Bernstein
    target: Baron_Friedrich_Schäffer_von_Bernstein
  AddTriple (7ed0a2fe-ecbd-4024-acf9-e15c32b0ad63)
 Call ID: 7ed0a2fe-ecbd-4024-acf9-e15c32b0ad63
  Args:
    source: Vera_Schäffer_von_Bernstein
    target: Emma_Carola_Passavant
    relation: :hasMother
  AssignClass (71d20e73-f58c-4118-85ea-cc19b5d3ac7c)
 Call ID: 71d20e73-f58c-4118-85ea-cc19b5d3ac7c
  Args:
    type: :Man
    source: Konrad
  AssignClass (4d702fa8-4c4f-48f2-89bb-0e2200f449fa)
 Call ID: 4d702fa8-4c4f-48f2-89bb-0e2200f449fa
  Args:
    source: Konrad
    type: :Person
  AddTriple (51d7cc57-58db-46df-9a93-0f6e8d64de74)
 Call ID: 51d7cc57-58db-46df-9a93-0f6e8d64de74
  Args:
    target: Bernhard_Prince_of_Saxe-Meiningen
    source: Konrad
    relation: :hasFather
  AddTriple (09c89249-f54f-498f-b0ce-0e3629dccde4)
 Call ID: 09c89249-f54f-498f-b0ce-0e3629dccde4
  Args:
    relation: :hasMother
    target: Vera_Schäffer_von_Bernstein
    source: Konrad
  Finish (329ae97f-4bc2-44e2-9dc3-7a0795e1d040)
 Call ID: 329ae97f-4bc2-44e2-9dc3-7a0795e1d040
  Args: