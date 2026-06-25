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
  AssignClass (7ce62b7f-bb7e-467c-ac2c-b25afe33c97e)
 Call ID: 7ce62b7f-bb7e-467c-ac2c-b25afe33c97e
  Args:
    type: :Woman
    source: Sarah_Rose_Troughton
  AssignClass (ac3134c5-5e3c-47e8-b8e4-a6a0cb4bddd8)
 Call ID: ac3134c5-5e3c-47e8-b8e4-a6a0cb4bddd8
  Args:
    source: Sarah_Rose_Troughton
    type: :Person
  AddLiteral (1910b5cc-3beb-4495-96a9-af5086fef740)
 Call ID: 1910b5cc-3beb-4495-96a9-af5086fef740
  Args:
    relation: :hasBirthYear
    literal_value: 1953
    source: Sarah_Rose_Troughton
    literal_type: xsd:integer
  AssignClass (e0c43ac0-0a40-40c7-8587-2c976150fbaa)
 Call ID: e0c43ac0-0a40-40c7-8587-2c976150fbaa
  Args:
    type: :Man
    source: Timothy_Colman
  AssignClass (823862d1-4f90-42f6-884d-41344a767a1a)
 Call ID: 823862d1-4f90-42f6-884d-41344a767a1a
  Args:
    type: :Person
    source: Timothy_Colman
  AddTriple (eff2fab4-e675-4c6c-a569-1b6c83ac4cdf)
 Call ID: eff2fab4-e675-4c6c-a569-1b6c83ac4cdf
  Args:
    target: Timothy_Colman
    relation: :hasFather
    source: Sarah_Rose_Troughton
  AssignClass (f69c4c60-be58-493b-a684-5714533c1e7d)
 Call ID: f69c4c60-be58-493b-a684-5714533c1e7d
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    type: :Woman
  AssignClass (e4dcc705-354b-4419-8e01-8d1108c2f978)
 Call ID: e4dcc705-354b-4419-8e01-8d1108c2f978
  Args:
    type: :Person
    source: Mary_Cecilia_Bowes-Lyon
  AddTriple (755b80bd-a4a7-4a22-bac6-8c637199b83d)
 Call ID: 755b80bd-a4a7-4a22-bac6-8c637199b83d
  Args:
    source: Sarah_Rose_Troughton
    target: Mary_Cecilia_Bowes-Lyon
    relation: :hasMother
  AssignClass (2dd30da8-52d7-4b35-a1c2-4090eb721bab)
 Call ID: 2dd30da8-52d7-4b35-a1c2-4090eb721bab
  Args:
    type: :Man
    source: Claude_Bowes-Lyon_14th
  AssignClass (b2805010-4668-49e2-a382-f04bb90e7779)
 Call ID: b2805010-4668-49e2-a382-f04bb90e7779
  Args:
    type: :Person
    source: Claude_Bowes-Lyon_14th
  AddTriple (159d2230-6f6a-4079-8562-e122dd2db26e)
 Call ID: 159d2230-6f6a-4079-8562-e122dd2db26e
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    target: Claude_Bowes-Lyon_14th
    relation: :hasAncestor
  AssignClass (cc19c6d4-79ce-49ab-97b5-8eed6063a33c)
 Call ID: cc19c6d4-79ce-49ab-97b5-8eed6063a33c
  Args:
    source: Jeremiah_Colman
    type: :Man
  AssignClass (6820098a-55e5-4926-8479-65fc75713a6f)
 Call ID: 6820098a-55e5-4926-8479-65fc75713a6f
  Args:
    type: :Person
    source: Jeremiah_Colman
  AddTriple (ea2e7e2c-c554-45ee-9e7e-cb7eca0b09d2)
 Call ID: ea2e7e2c-c554-45ee-9e7e-cb7eca0b09d2
  Args:
    relation: :hasAncestor
    target: Jeremiah_Colman
    source: Sarah_Rose_Troughton
  AddLiteral (5028d85b-d10c-4c4c-b62b-af72535c436a)
 Call ID: 5028d85b-d10c-4c4c-b62b-af72535c436a
  Args:
    literal_value: 1777
    relation: :hasBirthYear
    source: Jeremiah_Colman
    literal_type: xsd:integer
  AddLiteral (b9c52272-fe8c-417c-a847-a29c44b846de)
 Call ID: b9c52272-fe8c-417c-a847-a29c44b846de
  Args:
    literal_value: 1851
    relation: :hasDeathYear
    source: Jeremiah_Colman
    literal_type: xsd:integer
  AssignClass (4f702093-98b0-41e6-8464-2c7376534aea)
 Call ID: 4f702093-98b0-41e6-8464-2c7376534aea
  Args:
    type: :Man
    source: Peter_Troughton
  AssignClass (c26dca94-31ef-48e8-96ab-3d305bb4a3d8)
 Call ID: c26dca94-31ef-48e8-96ab-3d305bb4a3d8
  Args:
    type: :Person
    source: Peter_Troughton
  AddLiteral (39083106-498f-46a2-a22f-2f394fe3df31)
 Call ID: 39083106-498f-46a2-a22f-2f394fe3df31
  Args:
    literal_type: xsd:integer
    source: Peter_Troughton
    relation: :hasBirthYear
    literal_value: 1948
  AddLiteral (fd265d1f-4d23-43fc-9e50-b6ceafe1e54b)
 Call ID: fd265d1f-4d23-43fc-9e50-b6ceafe1e54b
  Args:
    source: Sarah_Rose_Troughton
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1977
  AddTriple (579ecd35-8ba3-457a-a783-6dc6f914e740)
 Call ID: 579ecd35-8ba3-457a-a783-6dc6f914e740
  Args:
    source: Sarah_Rose_Troughton
    target: Peter_Troughton
    relation: :hasRelation
  AssignClass (1da4fa81-8be2-4458-9c0f-04cfd803a3d3)
 Call ID: 1da4fa81-8be2-4458-9c0f-04cfd803a3d3
  Args:
    source: Charles_Troughton
    type: :Man
  AssignClass (cbaf3db5-3465-4231-b8ac-94443d131fc9)
 Call ID: cbaf3db5-3465-4231-b8ac-94443d131fc9
  Args:
    type: :Person
    source: Charles_Troughton
  AddTriple (e104e222-2745-4541-b9fc-0c59d2454ba7)
 Call ID: e104e222-2745-4541-b9fc-0c59d2454ba7
  Args:
    source: Peter_Troughton
    relation: :hasFather
    target: Charles_Troughton
  Finish (a9a53dcd-5275-44ec-b9c5-877f97bc2774)
 Call ID: a9a53dcd-5275-44ec-b9c5-877f97bc2774
  Args: