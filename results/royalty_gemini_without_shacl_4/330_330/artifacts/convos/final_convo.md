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
Fergus Bowes-Lyon (18 April 1889 – 27 September 1915) was a British officer and older brother of Elizabeth Bowes-Lyon, who later became the queen consort of King George VI.
He was a maternal uncle of Queen Elizabeth II.
Early life and marriage

Fergus Bowes-Lyon was born at Forbes House in Ham, Surrey, the son of Claude Bowes-Lyon, 14th
Bowes-Lyon had his early education at Ludgrove School.
On 17 September 1914, Bowes-Lyon married Lady Christian Norah Dawson-Damer (7 August 1890 – 29 March 1959), daughter of the 5th Earl of Portarlington.
Rosemary was only two months old when Fergus died in the line of duty on 27 September 1915, only 10 days after the first anniversary of his wedding.
His issue:


World War I

In the First World War, Bowes-Lyon served with the 8th Battalion, Black Watch: as a lieutenant since 19 August 1914, and as temporary captain since 17 November.
Bowes-Lyon was killed in action on 27 September 1915, during the Battle of the Hohenzollern Redoubt in the Battle of Loos.
At the time of Bowes-Lyon's death, his brother John was also serving with the Black Watch.
His mother, Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne, was severely affected by the loss of her son, and after his death became an invalid, withdrawn from public life until the marriage of her daughter Elizabeth to the future king George VI in 1923.
Fergus's widow later married Captain William Frederick Martin (d. 6 October 1947).
In November 2011, Bowes-Lyon's grandson supplied family records to the Commonwealth War Graves Commission detailing his original burial place, and showing that it had remained marked until the end of the war.



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
  AssignClass (6559be7e-0033-4d33-9c24-ec4f870e0eee)
 Call ID: 6559be7e-0033-4d33-9c24-ec4f870e0eee
  Args:
    type: :Man
    source: Fergus_Bowes-Lyon
  AssignClass (6e1d2a0a-22d7-4c88-9285-9d1910694f42)
 Call ID: 6e1d2a0a-22d7-4c88-9285-9d1910694f42
  Args:
    source: Fergus_Bowes-Lyon
    type: :Person
  AddLiteral (e811cc85-95bf-4cdc-9a81-d5a5a8a734e7)
 Call ID: e811cc85-95bf-4cdc-9a81-d5a5a8a734e7
  Args:
    source: Fergus_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1889
    relation: :hasBirthYear
  AddLiteral (32e65fc1-c5fb-4373-b2c9-1874aaa3c6b3)
 Call ID: 32e65fc1-c5fb-4373-b2c9-1874aaa3c6b3
  Args:
    relation: :hasDeathYear
    literal_value: 1915
    literal_type: xsd:integer
    source: Fergus_Bowes-Lyon
  AssignClass (5c3b207e-4ca2-48c1-b15f-98d456f802d9)
 Call ID: 5c3b207e-4ca2-48c1-b15f-98d456f802d9
  Args:
    source: Elizabeth_Bowes-Lyon
    type: :Woman
  AssignClass (2d5243b9-3d26-4de0-8179-b17b0c7d45bc)
 Call ID: 2d5243b9-3d26-4de0-8179-b17b0c7d45bc
  Args:
    type: :Person
    source: Elizabeth_Bowes-Lyon
  AddTriple (8c09640d-c693-4bfe-bdab-25f72ac52891)
 Call ID: 8c09640d-c693-4bfe-bdab-25f72ac52891
  Args:
    target: Elizabeth_Bowes-Lyon
    source: Fergus_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (fccbd8a0-3e70-4eed-bdee-16feb0d95043)
 Call ID: fccbd8a0-3e70-4eed-bdee-16feb0d95043
  Args:
    type: :Man
    source: King_George_VI
  AssignClass (ebd740f2-89ad-4037-85f3-56091e7eca4e)
 Call ID: ebd740f2-89ad-4037-85f3-56091e7eca4e
  Args:
    source: King_George_VI
    type: :Person
  AssignClass (c3f1c08c-2647-41f2-a241-ba5499dfdc40)
 Call ID: c3f1c08c-2647-41f2-a241-ba5499dfdc40
  Args:
    source: Queen_Elizabeth_II
    type: :Woman
  AssignClass (aae0e8cd-131b-4e54-96a7-d7bf7348ae12)
 Call ID: aae0e8cd-131b-4e54-96a7-d7bf7348ae12
  Args:
    type: :Person
    source: Queen_Elizabeth_II
  AddTriple (67192627-5122-409e-9774-cefef905899f)
 Call ID: 67192627-5122-409e-9774-cefef905899f
  Args:
    relation: :isUncleOf
    target: Queen_Elizabeth_II
    source: Fergus_Bowes-Lyon
  AssignClass (e288380e-225d-49ae-bbe2-d5ab6ea0dbb2)
 Call ID: e288380e-225d-49ae-bbe2-d5ab6ea0dbb2
  Args:
    type: :Man
    source: Claude_Bowes-Lyon
  AssignClass (042f3c63-e8cc-46e6-8223-7f0c6e7317b6)
 Call ID: 042f3c63-e8cc-46e6-8223-7f0c6e7317b6
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AddTriple (0b189148-cf4a-43ee-a9fa-8c03f2bf4447)
 Call ID: 0b189148-cf4a-43ee-a9fa-8c03f2bf4447
  Args:
    source: Fergus_Bowes-Lyon
    target: Claude_Bowes-Lyon
    relation: :hasFather
  AssignClass (fc60404a-ba93-49c6-a916-76f2804e4fba)
 Call ID: fc60404a-ba93-49c6-a916-76f2804e4fba
  Args:
    type: :Woman
    source: Lady_Christian_Norah_Dawson-Damer
  AssignClass (6889400d-2b21-40ac-8475-0c97591fd467)
 Call ID: 6889400d-2b21-40ac-8475-0c97591fd467
  Args:
    type: :Person
    source: Lady_Christian_Norah_Dawson-Damer
  AddTriple (a0933e69-744a-4a2f-911b-7648039d14c5)
 Call ID: a0933e69-744a-4a2f-911b-7648039d14c5
  Args:
    target: Lady_Christian_Norah_Dawson-Damer
    source: Fergus_Bowes-Lyon
    relation: :hasRelation
  AddLiteral (2b6472a5-36ca-4d71-8661-9e1c44da0b6e)
 Call ID: 2b6472a5-36ca-4d71-8661-9e1c44da0b6e
  Args:
    literal_value: 1914
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Fergus_Bowes-Lyon
  AssignClass (b7e919de-b50e-48c9-a126-1ce0544ec851)
 Call ID: b7e919de-b50e-48c9-a126-1ce0544ec851
  Args:
    source: Rosemary_Bowes-Lyon
    type: :Woman
  AssignClass (aeb8aba1-c9a9-47d5-a997-cc2a22773248)
 Call ID: aeb8aba1-c9a9-47d5-a997-cc2a22773248
  Args:
    type: :Person
    source: Rosemary_Bowes-Lyon
  AddTriple (9b59c757-f7c2-4a04-ac10-cc9eb43b05e6)
 Call ID: 9b59c757-f7c2-4a04-ac10-cc9eb43b05e6
  Args:
    relation: :isChildOf
    target: Fergus_Bowes-Lyon
    source: Rosemary_Bowes-Lyon
  AddTriple (29b52afc-fa75-4c05-849b-7c015072b1bc)
 Call ID: 29b52afc-fa75-4c05-849b-7c015072b1bc
  Args:
    target: Lady_Christian_Norah_Dawson-Damer
    source: Rosemary_Bowes-Lyon
    relation: :isChildOf
  AssignClass (dc622b6e-fea8-4fe8-ab83-f21cded0e0d1)
 Call ID: dc622b6e-fea8-4fe8-ab83-f21cded0e0d1
  Args:
    source: John_Bowes-Lyon
    type: :Man
  AssignClass (2dd147e8-1f80-4b31-9fc0-9fe0a5fb0cf2)
 Call ID: 2dd147e8-1f80-4b31-9fc0-9fe0a5fb0cf2
  Args:
    source: John_Bowes-Lyon
    type: :Person
  AddTriple (1b6ec58f-7751-4089-ae06-92f25c7c1182)
 Call ID: 1b6ec58f-7751-4089-ae06-92f25c7c1182
  Args:
    target: John_Bowes-Lyon
    source: Fergus_Bowes-Lyon
    relation: :isSiblingOf
  AssignClass (bd41970e-4731-4d69-bdf7-c25e8b2c4bc1)
 Call ID: bd41970e-4731-4d69-bdf7-c25e8b2c4bc1
  Args:
    source: Cecilia_Bowes-Lyon
    type: :Woman
  AssignClass (34d1f88e-e6b0-46d1-ac43-87cff8ab3fcd)
 Call ID: 34d1f88e-e6b0-46d1-ac43-87cff8ab3fcd
  Args:
    type: :Person
    source: Cecilia_Bowes-Lyon
  AddTriple (f497e3bc-6ceb-46f1-ad59-35db57b877ec)
 Call ID: f497e3bc-6ceb-46f1-ad59-35db57b877ec
  Args:
    relation: :hasMother
    target: Cecilia_Bowes-Lyon
    source: Fergus_Bowes-Lyon
  AssignClass (348a089c-ddab-43fb-93ff-388e326be2f3)
 Call ID: 348a089c-ddab-43fb-93ff-388e326be2f3
  Args:
    type: :Man
    source: William_Frederick_Martin
  AssignClass (d6fa73bc-d502-4b61-a0b8-602c95804d3c)
 Call ID: d6fa73bc-d502-4b61-a0b8-602c95804d3c
  Args:
    type: :Person
    source: William_Frederick_Martin
  AddTriple (776b89ae-6453-43dd-8854-e41ebc93d625)
 Call ID: 776b89ae-6453-43dd-8854-e41ebc93d625
  Args:
    relation: :hasRelation
    source: Lady_Christian_Norah_Dawson-Damer
    target: William_Frederick_Martin
  Finish (82e874cd-2138-418a-9880-d04d47b752d4)
 Call ID: 82e874cd-2138-418a-9880-d04d47b752d4
  Args: