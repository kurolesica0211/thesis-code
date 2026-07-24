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
Duchess Marie Antoinette of Mecklenburg-Schwerin, also Manette (Marie Antoinette Margarethe Mathilde; 28 May 1884 – 26 October 1944) was the Duchess of Mecklenburg-Schwerin by birth and potential bride for King Alfonso XIII of Spain.
Early life

Marie Antoinette was born in Venice, into the House of Mecklenburg, as the third child and the second daughter of Duke Paul Frederick of Mecklenburg and Princess Marie of Windisch-Graetz.
Her brothers and sisters were Duke Paul Friedrich of Mecklenburg, Duchess Maria Luise of Mecklenburg-Schwerin (1883–1883), Duke Heinrich Borwin of Mecklenburg-Schwerin (1885–1942), and Duke Joseph of Mecklenburg-Schwerin (1889–1889).
She had a difficult relationship with her cousin Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, who regularly had to amortize her debts.
So, Marie Antoinette regularly had to sell archaeological artifacts belonging to her mother, excavated in Austria and Carniola, including Hallstatt Archaeological Site in Vače.
Potential bride for the King of Spain

She was German Kaiser Wilhelm II's candidate for a bride for King Alfonso XIII of Spain although he would marry the Kaiser's maternal first cousin, Princess Victoria Eugenie, niece of British King Edward VII.



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
  AssignClass (c033de24-d1ed-48d6-8a3e-a52c76b3a03e)
 Call ID: c033de24-d1ed-48d6-8a3e-a52c76b3a03e
  Args:
    source: MarieAntoinetteOfMecklenburgSchwerin
    type: :Woman
  AssignClass (fbb16e65-1ff1-46ca-981d-02538c75bfac)
 Call ID: fbb16e65-1ff1-46ca-981d-02538c75bfac
  Args:
    type: :Person
    source: MarieAntoinetteOfMecklenburgSchwerin
  AddLiteral (da4a2afd-826e-4fef-8c32-9b5b4b037c22)
 Call ID: da4a2afd-826e-4fef-8c32-9b5b4b037c22
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    source: MarieAntoinetteOfMecklenburgSchwerin
    literal_value: Manette
  AddLiteral (d07cb27c-6078-4fd4-a9f0-c8f61154069c)
 Call ID: d07cb27c-6078-4fd4-a9f0-c8f61154069c
  Args:
    literal_type: xsd:integer
    literal_value: 1884
    source: MarieAntoinetteOfMecklenburgSchwerin
    relation: :hasBirthYear
  AddLiteral (5f241d22-849a-49eb-a1f5-48d77e2c8e17)
 Call ID: 5f241d22-849a-49eb-a1f5-48d77e2c8e17
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: MarieAntoinetteOfMecklenburgSchwerin
    literal_value: 1944
  AssignClass (fa63ee28-2e51-4640-b545-5940c5addb7c)
 Call ID: fa63ee28-2e51-4640-b545-5940c5addb7c
  Args:
    type: :Man
    source: PaulFrederickOfMecklenburg
  AssignClass (34b951c6-0d98-4eed-8790-8cc27fa1dfba)
 Call ID: 34b951c6-0d98-4eed-8790-8cc27fa1dfba
  Args:
    source: PaulFrederickOfMecklenburg
    type: :Person
  AssignClass (eac67fa6-c778-45b3-b9d8-c64d4ec93270)
 Call ID: eac67fa6-c778-45b3-b9d8-c64d4ec93270
  Args:
    source: MarieOfWindischGraetz
    type: :Woman
  AssignClass (b13b159b-9439-4e38-972b-7979c408589f)
 Call ID: b13b159b-9439-4e38-972b-7979c408589f
  Args:
    source: MarieOfWindischGraetz
    type: :Person
  AddTriple (de60a536-aef3-43a9-aa6a-9581ac754ae1)
 Call ID: de60a536-aef3-43a9-aa6a-9581ac754ae1
  Args:
    source: MarieAntoinetteOfMecklenburgSchwerin
    target: PaulFrederickOfMecklenburg
    relation: :hasFather
  AddTriple (e4307e45-9127-4ba3-8385-5fb1ff36fc9a)
 Call ID: e4307e45-9127-4ba3-8385-5fb1ff36fc9a
  Args:
    relation: :hasMother
    target: MarieOfWindischGraetz
    source: MarieAntoinetteOfMecklenburgSchwerin
  AssignClass (22ccef9d-7d6c-446c-bb28-ebcd1dc38df5)
 Call ID: 22ccef9d-7d6c-446c-bb28-ebcd1dc38df5
  Args:
    source: PaulFriedrichOfMecklenburg
    type: :Man
  AssignClass (2f6ff417-5f97-458e-a761-55745f82ef47)
 Call ID: 2f6ff417-5f97-458e-a761-55745f82ef47
  Args:
    type: :Person
    source: PaulFriedrichOfMecklenburg
  AssignClass (c3af410b-3c2a-4a77-a07a-9229f48ca2c6)
 Call ID: c3af410b-3c2a-4a77-a07a-9229f48ca2c6
  Args:
    type: :Woman
    source: MariaLuiseOfMecklenburgSchwerin
  AssignClass (01624d44-d1af-4df4-ac09-f17fd03ff843)
 Call ID: 01624d44-d1af-4df4-ac09-f17fd03ff843
  Args:
    source: MariaLuiseOfMecklenburgSchwerin
    type: :Person
  AddLiteral (ac3ebe7e-7a91-45ac-aba1-4566479f687e)
 Call ID: ac3ebe7e-7a91-45ac-aba1-4566479f687e
  Args:
    literal_value: 1883
    source: MariaLuiseOfMecklenburgSchwerin
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b943217a-0b10-4aa1-bfc2-0379636e35a8)
 Call ID: b943217a-0b10-4aa1-bfc2-0379636e35a8
  Args:
    literal_type: xsd:integer
    source: MariaLuiseOfMecklenburgSchwerin
    literal_value: 1883
    relation: :hasDeathYear
  AssignClass (32f31373-faa3-42bb-8377-3e573c7a2f44)
 Call ID: 32f31373-faa3-42bb-8377-3e573c7a2f44
  Args:
    type: :Man
    source: HeinrichBorwinOfMecklenburgSchwerin
  AssignClass (c0e6c38f-6e86-4716-8fe2-30703dedfcda)
 Call ID: c0e6c38f-6e86-4716-8fe2-30703dedfcda
  Args:
    type: :Person
    source: HeinrichBorwinOfMecklenburgSchwerin
  AddLiteral (fcf1a3fb-e7c5-4203-81ff-c40787c73c05)
 Call ID: fcf1a3fb-e7c5-4203-81ff-c40787c73c05
  Args:
    literal_type: xsd:integer
    literal_value: 1885
    source: HeinrichBorwinOfMecklenburgSchwerin
    relation: :hasBirthYear
  AddLiteral (8f54727a-f923-40aa-8493-1b76559f1550)
 Call ID: 8f54727a-f923-40aa-8493-1b76559f1550
  Args:
    relation: :hasDeathYear
    literal_value: 1942
    source: HeinrichBorwinOfMecklenburgSchwerin
    literal_type: xsd:integer
  AssignClass (fe9adf60-6617-4374-84fa-ab93e93e0bc4)
 Call ID: fe9adf60-6617-4374-84fa-ab93e93e0bc4
  Args:
    type: :Man
    source: JosephOfMecklenburgSchwerin
  AssignClass (53e3d11f-b9b1-4dab-b127-7cb1aab6253c)
 Call ID: 53e3d11f-b9b1-4dab-b127-7cb1aab6253c
  Args:
    type: :Person
    source: JosephOfMecklenburgSchwerin
  AddLiteral (fe8c51a9-af04-4143-ab7b-f6d859370fb1)
 Call ID: fe8c51a9-af04-4143-ab7b-f6d859370fb1
  Args:
    source: JosephOfMecklenburgSchwerin
    literal_value: 1889
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c15ad139-115a-4314-aea0-37483a0a0fd8)
 Call ID: c15ad139-115a-4314-aea0-37483a0a0fd8
  Args:
    literal_type: xsd:integer
    literal_value: 1889
    source: JosephOfMecklenburgSchwerin
    relation: :hasDeathYear
  AddTriple (04bf5397-9699-45d0-bb73-a4b03318dc8a)
 Call ID: 04bf5397-9699-45d0-bb73-a4b03318dc8a
  Args:
    relation: :isSiblingOf
    source: MarieAntoinetteOfMecklenburgSchwerin
    target: PaulFriedrichOfMecklenburg
  AddTriple (e52b062f-12a1-45aa-be13-c5248a830e83)
 Call ID: e52b062f-12a1-45aa-be13-c5248a830e83
  Args:
    source: MarieAntoinetteOfMecklenburgSchwerin
    target: MariaLuiseOfMecklenburgSchwerin
    relation: :isSiblingOf
  AddTriple (a93b9ac8-9f08-48e1-9054-ba238c24b1e9)
 Call ID: a93b9ac8-9f08-48e1-9054-ba238c24b1e9
  Args:
    relation: :isSiblingOf
    target: HeinrichBorwinOfMecklenburgSchwerin
    source: MarieAntoinetteOfMecklenburgSchwerin
  AddTriple (22f5f9c2-3d60-473e-bdf9-cd4fc8a8c592)
 Call ID: 22f5f9c2-3d60-473e-bdf9-cd4fc8a8c592
  Args:
    relation: :isSiblingOf
    target: JosephOfMecklenburgSchwerin
    source: MarieAntoinetteOfMecklenburgSchwerin
  AssignClass (407bc7d9-92e4-4771-abec-ddbc4a4ee509)
 Call ID: 407bc7d9-92e4-4771-abec-ddbc4a4ee509
  Args:
    source: FrederickFrancisIVOfMecklenburgSchwerin
    type: :Man
  AssignClass (6b97176e-f3b1-4b9d-99d0-a0a60604546b)
 Call ID: 6b97176e-f3b1-4b9d-99d0-a0a60604546b
  Args:
    type: :Person
    source: FrederickFrancisIVOfMecklenburgSchwerin
  AddTriple (839c3344-5fc7-4e34-a5bc-60a47942591f)
 Call ID: 839c3344-5fc7-4e34-a5bc-60a47942591f
  Args:
    source: MarieAntoinetteOfMecklenburgSchwerin
    target: FrederickFrancisIVOfMecklenburgSchwerin
    relation: :isBloodrelationOf
  Finish (4f6ec939-2fc0-4bae-a498-b64900c5c9f3)
 Call ID: 4f6ec939-2fc0-4bae-a498-b64900c5c9f3
  Args: