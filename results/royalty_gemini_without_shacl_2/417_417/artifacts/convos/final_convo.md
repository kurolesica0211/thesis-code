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
  AssignClass (032218ff-d409-4d7c-944e-c3fca7e3ed65)
 Call ID: 032218ff-d409-4d7c-944e-c3fca7e3ed65
  Args:
    type: :Man
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (fdb334ee-5c8c-47ef-8a85-74ff74ded2fb)
 Call ID: fdb334ee-5c8c-47ef-8a85-74ff74ded2fb
  Args:
    type: :Person
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddLiteral (b9078c03-d8bc-4771-b777-5e59bc3cd875)
 Call ID: b9078c03-d8bc-4771-b777-5e59bc3cd875
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1936
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddLiteral (400a1164-7e90-4a54-974e-4f5a7d7da808)
 Call ID: 400a1164-7e90-4a54-974e-4f5a7d7da808
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2024
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (9f17b1e2-2beb-4729-a0c4-718d8ab31786)
 Call ID: 9f17b1e2-2beb-4729-a0c4-718d8ab31786
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    type: :Man
  AssignClass (f19a8b20-7570-444c-bcd2-41837bc7f17c)
 Call ID: f19a8b20-7570-444c-bcd2-41837bc7f17c
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    type: :Person
  AddLiteral (0a0f5bfd-31be-428e-8dff-8311929a19b6)
 Call ID: 0a0f5bfd-31be-428e-8dff-8311929a19b6
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    literal_value: 1896
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (6871fa62-e3d0-44af-9d50-ae6a01c1aea8)
 Call ID: 6871fa62-e3d0-44af-9d50-ae6a01c1aea8
  Args:
    source: Josias_Georg_Wilhelm_Adolf
    literal_type: xsd:integer
    literal_value: 1967
    relation: :hasDeathYear
  AssignClass (350419d8-d2cc-4997-beec-aeec9b90b29c)
 Call ID: 350419d8-d2cc-4997-beec-aeec9b90b29c
  Args:
    type: :Woman
    source: Altburg_Marie_Mathilde_von_Oldenburg
  AssignClass (cb30e2f1-4aac-415f-8d2f-457c28e2dcff)
 Call ID: cb30e2f1-4aac-415f-8d2f-457c28e2dcff
  Args:
    source: Altburg_Marie_Mathilde_von_Oldenburg
    type: :Person
  AddLiteral (9db6374d-61ff-4f83-859d-c7143165d008)
 Call ID: 9db6374d-61ff-4f83-859d-c7143165d008
  Args:
    source: Altburg_Marie_Mathilde_von_Oldenburg
    relation: :hasBirthYear
    literal_value: 1903
    literal_type: xsd:integer
  AddLiteral (a1e51878-ded5-482f-9c1f-09474c244905)
 Call ID: a1e51878-ded5-482f-9c1f-09474c244905
  Args:
    source: Altburg_Marie_Mathilde_von_Oldenburg
    literal_value: 2001
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (59c58832-2d0d-4a5c-b3d6-ebf0c92d9a72)
 Call ID: 59c58832-2d0d-4a5c-b3d6-ebf0c92d9a72
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    target: Josias_Georg_Wilhelm_Adolf
    relation: :hasFather
  AddTriple (9d6659b0-d4ca-49ce-8ee6-9105cb20405d)
 Call ID: 9d6659b0-d4ca-49ce-8ee6-9105cb20405d
  Args:
    target: Altburg_Marie_Mathilde_von_Oldenburg
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    relation: :hasMother
  AssignClass (65ee3c0d-001d-4f35-9fed-481c1b42e3b7)
 Call ID: 65ee3c0d-001d-4f35-9fed-481c1b42e3b7
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    type: :Man
  AssignClass (b6085a86-8d4b-4650-9bdd-96cb16052965)
 Call ID: b6085a86-8d4b-4650-9bdd-96cb16052965
  Args:
    type: :Person
    source: Frederick_Augustus_II_of_Oldenburg
  AddTriple (8f6651b3-005b-40f4-847c-046c2cf75697)
 Call ID: 8f6651b3-005b-40f4-847c-046c2cf75697
  Args:
    source: Altburg_Marie_Mathilde_von_Oldenburg
    target: Frederick_Augustus_II_of_Oldenburg
    relation: :hasFather
  AssignClass (cddf32a7-529b-4ea6-8861-4db52829f5e7)
 Call ID: cddf32a7-529b-4ea6-8861-4db52829f5e7
  Args:
    type: :Woman
    source: Cecilia_von_Goëss-Saurau
  AssignClass (fd4f0b29-58ea-442d-8738-e4c828c34335)
 Call ID: fd4f0b29-58ea-442d-8738-e4c828c34335
  Args:
    source: Cecilia_von_Goëss-Saurau
    type: :Person
  AddLiteral (3aa106ac-6898-4e10-a09d-e836d1742e03)
 Call ID: 3aa106ac-6898-4e10-a09d-e836d1742e03
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1956
    source: Cecilia_von_Goëss-Saurau
  AddTriple (6330d38d-3d36-4b11-a18b-df675f063517)
 Call ID: 6330d38d-3d36-4b11-a18b-df675f063517
  Args:
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
    target: Cecilia_von_Goëss-Saurau
    relation: :hasRelation
  AddLiteral (e87d4e8d-8cad-4614-afc1-c307c655aa5a)
 Call ID: e87d4e8d-8cad-4614-afc1-c307c655aa5a
  Args:
    literal_value: 1988
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AssignClass (2a2669b7-3245-4d0c-9329-7890f8ddf834)
 Call ID: 2a2669b7-3245-4d0c-9329-7890f8ddf834
  Args:
    type: :Man
    source: Carl-Anton
  AssignClass (7fabe076-d76f-41d3-b23f-a60e21f79133)
 Call ID: 7fabe076-d76f-41d3-b23f-a60e21f79133
  Args:
    type: :Person
    source: Carl-Anton
  AddTriple (96358085-3beb-4828-ba30-34c0159d5d69)
 Call ID: 96358085-3beb-4828-ba30-34c0159d5d69
  Args:
    relation: :hasFather
    source: Carl-Anton
    target: Wittekind_Adolf_Heinrich_Georg-Wilhelm
  AddTriple (f5503687-f306-4654-8344-e48f36aab1e6)
 Call ID: f5503687-f306-4654-8344-e48f36aab1e6
  Args:
    relation: :hasMother
    target: Cecilia_von_Goëss-Saurau
    source: Carl-Anton
  Finish (245abd60-6fd3-4de8-a9ef-4ddda0664251)
 Call ID: 245abd60-6fd3-4de8-a9ef-4ddda0664251
  Args: