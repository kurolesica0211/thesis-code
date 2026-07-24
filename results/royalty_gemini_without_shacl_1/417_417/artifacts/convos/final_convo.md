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
Wittekind Adolf Heinrich Georg-Wilhelm, Prince of Waldeck and Pyrmont (Wittekind Adolf Heinrich Georg-Wilhelm Fürst zu Waldeck und Pyrmont; 9 March 1936 – 16 December 2024), was a member of the German nobility who from 1967 to 2024 was head of the House of Waldeck and Pyrmont.
Biography

Born in Arolsen (now Bad Arolsen) in Hesse, Germany, Wittekind was the only son of Josias Georg Wilhelm Adolf, Hereditary Prince of Waldeck and Pyrmont (1896−1967), an SS officer later found guilty of war crimes, and Duchess Altburg Marie Mathilde von Oldenburg (1903–2001), daughter of Frederick Augustus II, Grand Duke of Oldenburg.
He was the great-nephew of Emma of Waldeck and Pyrmont (later Queen of the Netherlands and Grand Duchess of Luxembourg) and thus a second cousin of Queen Beatrix of the Netherlands, whom he welcomed to Arolsen Castle in both 2008, on the 150th anniversary of Queen Emma's birth, and 2016, to celebrate his own 80th birthday.
Wittekind became head of the House of Waldeck and Pyrmont on his father's death in 1967.
Marriage and family

On 19 May 1988, in Frohnleiten, Wittekind married Countess Cecilia von Goëss-Saurau (born 1956), with whom he had three sons, including Carl-Anton, who succeeded him as Prince of Waldeck and Pyrmont.



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
  AssignClass (61992a29-79d4-4ef9-9779-d46589bde902)
 Call ID: 61992a29-79d4-4ef9-9779-d46589bde902
  Args:
    type: :Man
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (39b2f22b-48c2-4e0a-a988-b2ff47775cb8)
 Call ID: 39b2f22b-48c2-4e0a-a988-b2ff47775cb8
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    type: :Person
  AddLiteral (825c3476-1203-4c1e-baf4-d2085eaca5ea)
 Call ID: 825c3476-1203-4c1e-baf4-d2085eaca5ea
  Args:
    literal_value: 1936
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddLiteral (f3f5d522-d928-458a-bd1c-f5d8887e6540)
 Call ID: f3f5d522-d928-458a-bd1c-f5d8887e6540
  Args:
    relation: :hasDeathYear
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    literal_type: xsd:integer
    literal_value: 2024
  AssignClass (c2a31e7a-8673-4abc-a6d1-e924fa01e860)
 Call ID: c2a31e7a-8673-4abc-a6d1-e924fa01e860
  Args:
    type: :Man
    source: Josias_Georg_Wilhelm_Adolf
  AssignClass (2a167e61-e52e-4674-9a96-8b1f904ed49f)
 Call ID: 2a167e61-e52e-4674-9a96-8b1f904ed49f
  Args:
    type: :Person
    source: Josias_Georg_Wilhelm_Adolf
  AddLiteral (b15a07a4-501d-4172-9df0-f27ca7d9bb76)
 Call ID: b15a07a4-501d-4172-9df0-f27ca7d9bb76
  Args:
    literal_value: 1896
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Josias_Georg_Wilhelm_Adolf
  AddLiteral (68aa3382-61ce-4b36-8810-8fbadc9a3941)
 Call ID: 68aa3382-61ce-4b36-8810-8fbadc9a3941
  Args:
    relation: :hasDeathYear
    source: Josias_Georg_Wilhelm_Adolf
    literal_value: 1967
    literal_type: xsd:integer
  AssignClass (3c49f658-a7b1-4aa1-a564-e4d4b7969230)
 Call ID: 3c49f658-a7b1-4aa1-a564-e4d4b7969230
  Args:
    type: :Woman
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (3d1bd059-ebc8-43c2-b3bc-2b78a648edeb)
 Call ID: 3d1bd059-ebc8-43c2-b3bc-2b78a648edeb
  Args:
    type: :Person
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AddLiteral (d5159ca4-ddb5-412c-8bcb-ad31112586ca)
 Call ID: d5159ca4-ddb5-412c-8bcb-ad31112586ca
  Args:
    literal_value: 1903
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AddLiteral (7c54ad9a-0f46-47b1-ab79-a30f787757d5)
 Call ID: 7c54ad9a-0f46-47b1-ab79-a30f787757d5
  Args:
    literal_value: 2001
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AddTriple (0eed79fc-d70e-4f63-846a-249f8103a297)
 Call ID: 0eed79fc-d70e-4f63-846a-249f8103a297
  Args:
    target: Josias_Georg_Wilhelm_Adolf
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    relation: :hasFather
  AddTriple (6a85906d-6dec-48cc-9f78-d880af1335ca)
 Call ID: 6a85906d-6dec-48cc-9f78-d880af1335ca
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    relation: :hasMother
    target: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (0b7fd134-39a8-4abf-8a41-e7c8c25d7a13)
 Call ID: 0b7fd134-39a8-4abf-8a41-e7c8c25d7a13
  Args:
    type: :Man
    source: Frederick_Augustus_II_Grand_Duke_of_Oldenburg
  AssignClass (54380d0e-b6cb-4b9b-afee-c748a658054f)
 Call ID: 54380d0e-b6cb-4b9b-afee-c748a658054f
  Args:
    type: :Person
    source: Frederick_Augustus_II_Grand_Duke_of_Oldenburg
  AddTriple (f5c654ba-d0a3-4325-8de6-3f726a371894)
 Call ID: f5c654ba-d0a3-4325-8de6-3f726a371894
  Args:
    target: Frederick_Augustus_II_Grand_Duke_of_Oldenburg
    relation: :hasFather
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (050f0346-a524-42f4-9ab1-061411a99ac3)
 Call ID: 050f0346-a524-42f4-9ab1-061411a99ac3
  Args:
    source: Cecilia_von_Goess-Saurau
    type: :Woman
  AssignClass (cb5d951c-2cf7-440c-a0c3-c69332df0e58)
 Call ID: cb5d951c-2cf7-440c-a0c3-c69332df0e58
  Args:
    source: Cecilia_von_Goess-Saurau
    type: :Person
  AddLiteral (33cf3b54-f41a-458e-b5db-fd02f96378e8)
 Call ID: 33cf3b54-f41a-458e-b5db-fd02f96378e8
  Args:
    literal_type: xsd:integer
    literal_value: 1956
    relation: :hasBirthYear
    source: Cecilia_von_Goess-Saurau
  AddLiteral (873a8517-4201-45ed-8cfd-ed8dd018c013)
 Call ID: 873a8517-4201-45ed-8cfd-ed8dd018c013
  Args:
    literal_type: xsd:integer
    literal_value: 1988
    relation: :hasMarriageYear
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddTriple (b5ef9bcb-8f26-4f0a-9a23-fdeb9f304803)
 Call ID: b5ef9bcb-8f26-4f0a-9a23-fdeb9f304803
  Args:
    relation: :hasRelation
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    target: Cecilia_von_Goess-Saurau
  AssignClass (0d393033-5c62-4f9e-b433-3457f5bd92ca)
 Call ID: 0d393033-5c62-4f9e-b433-3457f5bd92ca
  Args:
    source: Carl-Anton
    type: :Man
  AssignClass (c68868f2-cf18-4dc1-bb9b-344658d7b728)
 Call ID: c68868f2-cf18-4dc1-bb9b-344658d7b728
  Args:
    source: Carl-Anton
    type: :Person
  AddTriple (13cb8844-262f-4801-83f0-f49cfcc10953)
 Call ID: 13cb8844-262f-4801-83f0-f49cfcc10953
  Args:
    relation: :hasFather
    source: Carl-Anton
    target: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddTriple (3e51d7d0-d6c2-4a8c-962d-a4886b212cb6)
 Call ID: 3e51d7d0-d6c2-4a8c-962d-a4886b212cb6
  Args:
    target: Cecilia_von_Goess-Saurau
    relation: :hasMother
    source: Carl-Anton
  AssignClass (71d0c6d7-e733-448a-b6e7-d1ec22796262)
 Call ID: 71d0c6d7-e733-448a-b6e7-d1ec22796262
  Args:
    type: :Woman
    source: Emma_of_Waldeck_and_Pyrmont
  AssignClass (dcb31ea7-6d1e-4f13-b218-379d3e7b838c)
 Call ID: dcb31ea7-6d1e-4f13-b218-379d3e7b838c
  Args:
    type: :Person
    source: Emma_of_Waldeck_and_Pyrmont
  Finish (dec94b1f-5a96-4fc1-a31d-6c885f8737eb)
 Call ID: dec94b1f-5a96-4fc1-a31d-6c885f8737eb
  Args: