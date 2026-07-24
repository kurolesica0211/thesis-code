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
Dame Sarah Rose Troughton (née Colman; born 3
Early life

Troughton was born in Paddington in 1953.
She is the eldest of the five children of Sir Timothy Colman, a past Lord Lieutenant of Norfolk, and Lady Mary Cecilia Bowes-Lyon, a granddaughter of Claude Bowes-Lyon, 14th
Her ancestor Jeremiah Colman (1777–1851) made a fortune from Colman's mustard, a business which eventually grew into Reckitt & Colman, of which her father was a director until 1989.
Public life

From 1990 to 2000, Troughton was lady-in-waiting to the Duchess of Kent.
As Lord Lieutenant, Troughton's public duties include overseeing arrangements for visits to Wiltshire by members of the Royal Family and escorting royal visitors; representing the King at events and presenting awards and medals on his behalf; liaising with the Wiltshire units of the Royal Navy, Army and Royal Air Force; leading the local magistracy as chairman of the Lord Chancellor's Advisory Committee on Justices of the Peace; and advising on nominations for national honours.
In January 2013, Troughton was appointed a Commander of the Order of St John by the Queen, and advanced to Dame of Grace of the order in 2021.
A BBC News article described Troughton as one of Camilla's longstanding personal friends.
Troughton was appointed a Dame Commander of the Royal Victorian Order in the 2025 New Year Honours.
Personal life

In 1977 she married Peter Troughton (born 1948), a member of HM Diplomatic Service, and the eldest son of Sir Charles Troughton, chairman of W H Smith.



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
  AssignClass (8c5075a1-69c2-4af6-8c51-66ea3b898dff)
 Call ID: 8c5075a1-69c2-4af6-8c51-66ea3b898dff
  Args:
    type: :Woman
    source: Sarah_Rose_Troughton
  AssignClass (799e8006-a1d5-43e5-88f4-1626dcd9ab34)
 Call ID: 799e8006-a1d5-43e5-88f4-1626dcd9ab34
  Args:
    type: :Person
    source: Sarah_Rose_Troughton
  AddLiteral (394ead70-670e-4ecd-af9a-31591f38a13c)
 Call ID: 394ead70-670e-4ecd-af9a-31591f38a13c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1953
    source: Sarah_Rose_Troughton
  AssignClass (bf11a4b7-f7d9-4c90-89a3-9ec5ce1de323)
 Call ID: bf11a4b7-f7d9-4c90-89a3-9ec5ce1de323
  Args:
    source: Timothy_Colman
    type: :Man
  AssignClass (39a82be5-100e-41a2-9f2f-2bd6e9e9d955)
 Call ID: 39a82be5-100e-41a2-9f2f-2bd6e9e9d955
  Args:
    type: :Ancestor
    source: Timothy_Colman
  AssignClass (075d85eb-0629-46fb-86b9-8db0289fdada)
 Call ID: 075d85eb-0629-46fb-86b9-8db0289fdada
  Args:
    type: :Person
    source: Timothy_Colman
  AssignClass (90488f85-5e78-4998-8b87-de3c025e15d8)
 Call ID: 90488f85-5e78-4998-8b87-de3c025e15d8
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    type: :Woman
  AssignClass (e3af5aeb-b294-414d-bb15-b6eb68b7386d)
 Call ID: e3af5aeb-b294-414d-bb15-b6eb68b7386d
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    type: :Ancestor
  AssignClass (9f3e6d44-5346-42df-8c3b-ddfe0f8cadf9)
 Call ID: 9f3e6d44-5346-42df-8c3b-ddfe0f8cadf9
  Args:
    type: :Person
    source: Mary_Cecilia_Bowes-Lyon
  AddTriple (60a600dc-c29e-48dd-a4df-2d5f392f32c3)
 Call ID: 60a600dc-c29e-48dd-a4df-2d5f392f32c3
  Args:
    target: Timothy_Colman
    relation: :hasFather
    source: Sarah_Rose_Troughton
  AddTriple (3c3e148a-c2c1-4bee-984c-8be2184d3344)
 Call ID: 3c3e148a-c2c1-4bee-984c-8be2184d3344
  Args:
    source: Sarah_Rose_Troughton
    relation: :hasMother
    target: Mary_Cecilia_Bowes-Lyon
  AssignClass (c4fd4b09-6f06-48f7-bb8d-9307bf8c6b79)
 Call ID: c4fd4b09-6f06-48f7-bb8d-9307bf8c6b79
  Args:
    type: :Man
    source: Jeremiah_Colman
  AssignClass (95fd8210-544e-4e28-8bcd-38340f97b1c4)
 Call ID: 95fd8210-544e-4e28-8bcd-38340f97b1c4
  Args:
    source: Jeremiah_Colman
    type: :Ancestor
  AssignClass (75f39723-2197-4c3c-9a0b-98955a9c8029)
 Call ID: 75f39723-2197-4c3c-9a0b-98955a9c8029
  Args:
    type: :Person
    source: Jeremiah_Colman
  AddLiteral (0c963cbb-4751-4f5e-a112-56b29baab58a)
 Call ID: 0c963cbb-4751-4f5e-a112-56b29baab58a
  Args:
    literal_type: xsd:integer
    source: Jeremiah_Colman
    literal_value: 1777
    relation: :hasBirthYear
  AddLiteral (6221041f-e419-4a63-8790-743b4461e3ff)
 Call ID: 6221041f-e419-4a63-8790-743b4461e3ff
  Args:
    relation: :hasDeathYear
    literal_value: 1851
    source: Jeremiah_Colman
    literal_type: xsd:integer
  AddTriple (1ca92131-ae9d-4b11-8d4a-4668a2c1bc64)
 Call ID: 1ca92131-ae9d-4b11-8d4a-4668a2c1bc64
  Args:
    source: Sarah_Rose_Troughton
    relation: :hasAncestor
    target: Jeremiah_Colman
  AssignClass (348c9018-81c5-4992-a375-d4918a0fe6b1)
 Call ID: 348c9018-81c5-4992-a375-d4918a0fe6b1
  Args:
    type: :Man
    source: Claude_Bowes-Lyon_14th
  AssignClass (1485113e-66ff-4272-8f20-e09d4e43be56)
 Call ID: 1485113e-66ff-4272-8f20-e09d4e43be56
  Args:
    type: :Ancestor
    source: Claude_Bowes-Lyon_14th
  AssignClass (909d3ed8-de64-48f2-8a68-3c83df71ed2c)
 Call ID: 909d3ed8-de64-48f2-8a68-3c83df71ed2c
  Args:
    source: Claude_Bowes-Lyon_14th
    type: :Person
  AddTriple (4c3c3b4f-9438-4930-9142-02d71d10ba8e)
 Call ID: 4c3c3b4f-9438-4930-9142-02d71d10ba8e
  Args:
    target: Mary_Cecilia_Bowes-Lyon
    relation: :isAncestorOf
    source: Claude_Bowes-Lyon_14th
  AssignClass (aff9e5d8-c7f8-421a-b2be-c7b36accec0c)
 Call ID: aff9e5d8-c7f8-421a-b2be-c7b36accec0c
  Args:
    source: Peter_Troughton
    type: :Man
  AssignClass (ded3069c-30ce-44b7-a2a7-df76dc3aac36)
 Call ID: ded3069c-30ce-44b7-a2a7-df76dc3aac36
  Args:
    source: Peter_Troughton
    type: :Person
  AddLiteral (f125b11d-27bf-4564-b9ef-0ffaf9a687dd)
 Call ID: f125b11d-27bf-4564-b9ef-0ffaf9a687dd
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasBirthYear
    source: Peter_Troughton
  AddLiteral (d69851a9-7b76-49ae-85f3-9796c65a9f90)
 Call ID: d69851a9-7b76-49ae-85f3-9796c65a9f90
  Args:
    literal_type: xsd:integer
    literal_value: 1977
    source: Sarah_Rose_Troughton
    relation: :hasMarriageYear
  AddTriple (84756df2-62b7-4523-a64f-41567e663d85)
 Call ID: 84756df2-62b7-4523-a64f-41567e663d85
  Args:
    relation: :hasRelation
    source: Sarah_Rose_Troughton
    target: Peter_Troughton
  AssignClass (eed20834-428c-47cd-b0bf-2fd809574510)
 Call ID: eed20834-428c-47cd-b0bf-2fd809574510
  Args:
    type: :Man
    source: Charles_Troughton
  AssignClass (7e01ba6a-7d0d-4582-9bbd-3644fe6c700e)
 Call ID: 7e01ba6a-7d0d-4582-9bbd-3644fe6c700e
  Args:
    type: :Ancestor
    source: Charles_Troughton
  AssignClass (83840f7e-de88-427e-9c53-f57a4c19a4af)
 Call ID: 83840f7e-de88-427e-9c53-f57a4c19a4af
  Args:
    type: :Person
    source: Charles_Troughton
  AddTriple (487f6808-a7da-4960-aac8-2fb480165f37)
 Call ID: 487f6808-a7da-4960-aac8-2fb480165f37
  Args:
    source: Peter_Troughton
    relation: :hasFather
    target: Charles_Troughton
  Finish (9974a0e0-8ca1-4083-92cf-68243cbac0f7)
 Call ID: 9974a0e0-8ca1-4083-92cf-68243cbac0f7
  Args: