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
Nikolaus, Hereditary Grand Duke of Oldenburg (German: Nikolaus Friedrich Wilhelm von Holstein-Gottorp, Erbgroßherzog von Oldenburg; 10 August 1897 – 3 April 1970) was the eldest son of Frederick Augustus II, Grand Duke of Oldenburg, who was the last ruling Grand Duke of Oldenburg.
In 1931, Nikolaus succeeded to his father's titles and assumed the role of pretender to the Grand Duchy, until his death in 1970.
Early life

Nikolaus was born at Oldenburg, Grand Duchy of Oldenburg, the third child and first son of Frederick Augustus II, Grand Duke of Oldenburg (1852–1931) (son of Peter II, Grand Duke of Oldenburg and Princess Elisabeth of Saxe-Altenburg) and his wife, Duchess Elisabeth Alexandrine of Mecklenburg-Schwerin (1869–1955) (daughter of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin and Princess Marie of Schwarzburg-Rudolstadt).
Marriage and issue

Nikolaus married on 26 October 1921 in Arolsen to Princess Helena of Waldeck and Pyrmont (1899–1948), only daughter of Friedrich, Prince of Waldeck and Pyrmont, and Princess Bathildis of Schaumburg-Lippe.
They had nine children:


When his first wife died in 1948, he married secondly on 20 September 1950 in Güldenstein to a fellow noblewoman, Anne-Marie von Schutzbar genannt Milchling (1903–1991), former wife of Count Bechtold von Bernstorff, daughter of Rudolf von Schutzbar gen. Milchling (1853-1935) and Rose Marston (1872-1957).



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
  AssignClass (d3d7ab93-10c2-4316-a2fe-01487dfc636b)
 Call ID: d3d7ab93-10c2-4316-a2fe-01487dfc636b
  Args:
    type: :Man
    source: Nikolaus_von_Oldenburg
  AssignClass (bfe36f54-85b4-4f60-a8b6-102ebe849e72)
 Call ID: bfe36f54-85b4-4f60-a8b6-102ebe849e72
  Args:
    type: :Person
    source: Nikolaus_von_Oldenburg
  AddLiteral (30f70487-2d87-45e0-9c76-e867fc32f07f)
 Call ID: 30f70487-2d87-45e0-9c76-e867fc32f07f
  Args:
    relation: :hasBirthYear
    literal_value: 1897
    source: Nikolaus_von_Oldenburg
    literal_type: xsd:integer
  AddLiteral (e0c9264a-be48-4f08-aef8-40b96781029b)
 Call ID: e0c9264a-be48-4f08-aef8-40b96781029b
  Args:
    source: Nikolaus_von_Oldenburg
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1970
  AssignClass (00593c97-132f-4d82-a50a-143775aeb669)
 Call ID: 00593c97-132f-4d82-a50a-143775aeb669
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (04272feb-66b7-4e0e-ab84-3f48353ee35d)
 Call ID: 04272feb-66b7-4e0e-ab84-3f48353ee35d
  Args:
    type: :Person
    source: Frederick_Augustus_II_of_Oldenburg
  AddLiteral (5bb143ac-c184-47d7-a2e7-1fffb0c05908)
 Call ID: 5bb143ac-c184-47d7-a2e7-1fffb0c05908
  Args:
    relation: :hasBirthYear
    literal_value: 1852
    source: Frederick_Augustus_II_of_Oldenburg
    literal_type: xsd:integer
  AddLiteral (efdbdfa3-c30e-4ccb-8e2d-87712eb3d9b1)
 Call ID: efdbdfa3-c30e-4ccb-8e2d-87712eb3d9b1
  Args:
    relation: :hasDeathYear
    literal_value: 1931
    source: Frederick_Augustus_II_of_Oldenburg
    literal_type: xsd:integer
  AddTriple (530f0831-8fbd-4dff-8b84-754f5d4bb226)
 Call ID: 530f0831-8fbd-4dff-8b84-754f5d4bb226
  Args:
    target: Frederick_Augustus_II_of_Oldenburg
    source: Nikolaus_von_Oldenburg
    relation: :hasFather
  AssignClass (ede44388-3f68-40ab-a438-aadcc9e8b14b)
 Call ID: ede44388-3f68-40ab-a438-aadcc9e8b14b
  Args:
    type: :Man
    source: Peter_II_of_Oldenburg
  AssignClass (01c3822d-c0ee-4cfd-836d-a0ae4ef8c102)
 Call ID: 01c3822d-c0ee-4cfd-836d-a0ae4ef8c102
  Args:
    type: :Person
    source: Peter_II_of_Oldenburg
  AddTriple (2786eb59-3a20-4a60-a381-f2332088fc98)
 Call ID: 2786eb59-3a20-4a60-a381-f2332088fc98
  Args:
    relation: :hasFather
    source: Frederick_Augustus_II_of_Oldenburg
    target: Peter_II_of_Oldenburg
  AssignClass (a6a398b8-1c24-4c76-b704-f98ff6065884)
 Call ID: a6a398b8-1c24-4c76-b704-f98ff6065884
  Args:
    source: Elisabeth_of_Saxe-Altenburg
    type: :Woman
  AssignClass (f49f1175-0250-4a5c-92d5-4f159980bdce)
 Call ID: f49f1175-0250-4a5c-92d5-4f159980bdce
  Args:
    source: Elisabeth_of_Saxe-Altenburg
    type: :Person
  AddTriple (c5e41959-760d-4364-94a9-b3ab2bd6c38b)
 Call ID: c5e41959-760d-4364-94a9-b3ab2bd6c38b
  Args:
    relation: :hasMother
    source: Frederick_Augustus_II_of_Oldenburg
    target: Elisabeth_of_Saxe-Altenburg
  AssignClass (13161b37-25f3-4a8b-aaab-a736b4c3ed00)
 Call ID: 13161b37-25f3-4a8b-aaab-a736b4c3ed00
  Args:
    type: :Woman
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (859fa537-2599-4f61-8040-aefdc7aa60d8)
 Call ID: 859fa537-2599-4f61-8040-aefdc7aa60d8
  Args:
    type: :Person
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (aa6a3127-d540-4bfb-acfc-0f193f0ea8f6)
 Call ID: aa6a3127-d540-4bfb-acfc-0f193f0ea8f6
  Args:
    literal_value: 1869
    relation: :hasBirthYear
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddLiteral (88c27819-fca5-479e-b058-785c3f67929b)
 Call ID: 88c27819-fca5-479e-b058-785c3f67929b
  Args:
    literal_type: xsd:integer
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_value: 1955
  AddTriple (5f1c1e37-60af-4d5d-b5c4-a74265a2a01d)
 Call ID: 5f1c1e37-60af-4d5d-b5c4-a74265a2a01d
  Args:
    source: Nikolaus_von_Oldenburg
    target: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (6c8f086f-673f-4a82-b8c7-33680ca2a49e)
 Call ID: 6c8f086f-673f-4a82-b8c7-33680ca2a49e
  Args:
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (9594e39c-78ce-42ff-9c5f-bf500634c26e)
 Call ID: 9594e39c-78ce-42ff-9c5f-bf500634c26e
  Args:
    type: :Person
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AddTriple (55563476-484e-4ba6-99df-bedab71efa8f)
 Call ID: 55563476-484e-4ba6-99df-bedab71efa8f
  Args:
    relation: :hasFather
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    target: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AssignClass (5545e9e1-cce2-47b2-a77f-4d6f50133e71)
 Call ID: 5545e9e1-cce2-47b2-a77f-4d6f50133e71
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    type: :Woman
  AssignClass (dac3783a-c27d-482e-b0ea-353bd4932d9a)
 Call ID: dac3783a-c27d-482e-b0ea-353bd4932d9a
  Args:
    type: :Person
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (931776bc-593d-43d9-86aa-b8192d30df2b)
 Call ID: 931776bc-593d-43d9-86aa-b8192d30df2b
  Args:
    relation: :hasMother
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    target: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (5dda0249-6e11-4e31-9211-2dc4ea2acbd3)
 Call ID: 5dda0249-6e11-4e31-9211-2dc4ea2acbd3
  Args:
    type: :Woman
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (ef57c641-2335-4ac1-878d-875a178cd49b)
 Call ID: ef57c641-2335-4ac1-878d-875a178cd49b
  Args:
    type: :Person
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (31791f82-5b6f-4a2f-af85-3989f659395f)
 Call ID: 31791f82-5b6f-4a2f-af85-3989f659395f
  Args:
    relation: :hasBirthYear
    literal_value: 1899
    source: Helena_of_Waldeck_and_Pyrmont
    literal_type: xsd:integer
  AddLiteral (911026e5-a022-469e-88a9-6523db333966)
 Call ID: 911026e5-a022-469e-88a9-6523db333966
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    literal_type: xsd:integer
    literal_value: 1948
    relation: :hasDeathYear
  AddLiteral (e8a3f3a6-bcd9-4f26-92bf-4102e33d0084)
 Call ID: e8a3f3a6-bcd9-4f26-92bf-4102e33d0084
  Args:
    source: Nikolaus_von_Oldenburg
    literal_type: xsd:integer
    literal_value: 1921
    relation: :hasMarriageYear
  AddTriple (ab33fc38-4d05-427e-907f-4bf0e6f95bb0)
 Call ID: ab33fc38-4d05-427e-907f-4bf0e6f95bb0
  Args:
    source: Nikolaus_von_Oldenburg
    target: Helena_of_Waldeck_and_Pyrmont
    relation: :hasRelation
  AssignClass (b787d3f1-5d5d-4993-b774-0c17a1c3bfbb)
 Call ID: b787d3f1-5d5d-4993-b774-0c17a1c3bfbb
  Args:
    source: Friedrich_of_Waldeck_and_Pyrmont
    type: :Man
  AssignClass (cd788330-c5aa-4d4d-ba5e-f8bf885a1eca)
 Call ID: cd788330-c5aa-4d4d-ba5e-f8bf885a1eca
  Args:
    source: Friedrich_of_Waldeck_and_Pyrmont
    type: :Person
  AddTriple (8c349db5-79b9-48f0-9ee9-1c4f669b4221)
 Call ID: 8c349db5-79b9-48f0-9ee9-1c4f669b4221
  Args:
    relation: :hasFather
    source: Helena_of_Waldeck_and_Pyrmont
    target: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (c8ebaebf-4413-4532-b4e6-1d1c8aa17a4c)
 Call ID: c8ebaebf-4413-4532-b4e6-1d1c8aa17a4c
  Args:
    source: Bathildis_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (21d36ed3-3780-452b-97a1-d5c491abfe3f)
 Call ID: 21d36ed3-3780-452b-97a1-d5c491abfe3f
  Args:
    type: :Person
    source: Bathildis_of_Schaumburg-Lippe
  AddTriple (75250319-aa70-4b53-8b48-49206d363e17)
 Call ID: 75250319-aa70-4b53-8b48-49206d363e17
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    target: Bathildis_of_Schaumburg-Lippe
    relation: :hasMother
  AssignClass (902df556-d52e-4e61-a47d-a54482d09505)
 Call ID: 902df556-d52e-4e61-a47d-a54482d09505
  Args:
    type: :Woman
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AssignClass (eb00bfc0-03d8-4b4a-adb1-6df8e20719d3)
 Call ID: eb00bfc0-03d8-4b4a-adb1-6df8e20719d3
  Args:
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    type: :Person
  AddLiteral (66172b20-d21d-4be1-b781-482f1235d371)
 Call ID: 66172b20-d21d-4be1-b781-482f1235d371
  Args:
    relation: :hasBirthYear
    literal_value: 1903
    literal_type: xsd:integer
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AddLiteral (05866f75-6cc0-4e9a-ad23-7c8b6c617ed3)
 Call ID: 05866f75-6cc0-4e9a-ad23-7c8b6c617ed3
  Args:
    literal_value: 1991
    relation: :hasDeathYear
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    literal_type: xsd:integer
  AddLiteral (6af8df77-e336-4d4c-9a1f-0aa46d8d200e)
 Call ID: 6af8df77-e336-4d4c-9a1f-0aa46d8d200e
  Args:
    literal_value: 1950
    relation: :hasMarriageYear
    source: Nikolaus_von_Oldenburg
    literal_type: xsd:integer
  AddTriple (0ad8ab63-bb5f-4c5e-aa9a-58d1bf022820)
 Call ID: 0ad8ab63-bb5f-4c5e-aa9a-58d1bf022820
  Args:
    source: Nikolaus_von_Oldenburg
    target: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :hasRelation
  AssignClass (8630d90b-6d86-4bd9-876a-dda987f09926)
 Call ID: 8630d90b-6d86-4bd9-876a-dda987f09926
  Args:
    source: Rudolf_von_Schutzbar_gen_Milchling
    type: :Man
  AssignClass (fe286569-dd67-414a-a41b-a390d4a9c1a4)
 Call ID: fe286569-dd67-414a-a41b-a390d4a9c1a4
  Args:
    source: Rudolf_von_Schutzbar_gen_Milchling
    type: :Person
  AddLiteral (30f12f6e-85a2-4846-a1fd-5f2f8ed86b3a)
 Call ID: 30f12f6e-85a2-4846-a1fd-5f2f8ed86b3a
  Args:
    relation: :hasBirthYear
    literal_value: 1853
    source: Rudolf_von_Schutzbar_gen_Milchling
    literal_type: xsd:integer
  AddLiteral (9333ff7b-27b7-475f-b15a-38027f8783b9)
 Call ID: 9333ff7b-27b7-475f-b15a-38027f8783b9
  Args:
    relation: :hasDeathYear
    literal_value: 1935
    literal_type: xsd:integer
    source: Rudolf_von_Schutzbar_gen_Milchling
  AddTriple (16c5d77e-ecde-43cc-a52c-a9c185cf848c)
 Call ID: 16c5d77e-ecde-43cc-a52c-a9c185cf848c
  Args:
    target: Rudolf_von_Schutzbar_gen_Milchling
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :hasFather
  AssignClass (9b632cd7-74ed-48ea-a4a8-b6dd3fd589ef)
 Call ID: 9b632cd7-74ed-48ea-a4a8-b6dd3fd589ef
  Args:
    type: :Woman
    source: Rose_Marston
  AssignClass (ac1b39e0-1099-4dcb-bd4a-16badf6c793a)
 Call ID: ac1b39e0-1099-4dcb-bd4a-16badf6c793a
  Args:
    type: :Person
    source: Rose_Marston
  AddLiteral (f9d7bf2f-c5a1-4a3e-a45a-70dfd9c76f8b)
 Call ID: f9d7bf2f-c5a1-4a3e-a45a-70dfd9c76f8b
  Args:
    literal_type: xsd:integer
    source: Rose_Marston
    relation: :hasBirthYear
    literal_value: 1872
  AddLiteral (f0449698-cd40-4a07-b2bd-f93152854619)
 Call ID: f0449698-cd40-4a07-b2bd-f93152854619
  Args:
    relation: :hasDeathYear
    literal_value: 1957
    source: Rose_Marston
    literal_type: xsd:integer
  AddTriple (c8e53a69-04dd-4483-bc36-f71c9f790075)
 Call ID: c8e53a69-04dd-4483-bc36-f71c9f790075
  Args:
    relation: :hasMother
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    target: Rose_Marston
  Finish (a36b78e0-a471-4ba9-9dbb-eede4d05a572)
 Call ID: a36b78e0-a471-4ba9-9dbb-eede4d05a572
  Args: