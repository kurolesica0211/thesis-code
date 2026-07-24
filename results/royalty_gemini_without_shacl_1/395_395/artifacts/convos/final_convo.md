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
  AssignClass (a4da545c-10ed-4b26-9189-4d703ad4c72c)
 Call ID: a4da545c-10ed-4b26-9189-4d703ad4c72c
  Args:
    type: :Man
    source: Nikolaus
  AssignClass (73778667-8ff8-441e-94f1-e199870a5069)
 Call ID: 73778667-8ff8-441e-94f1-e199870a5069
  Args:
    type: :Person
    source: Nikolaus
  AddLiteral (9152e12c-6d0f-4fd7-a1c9-03f8420d44e4)
 Call ID: 9152e12c-6d0f-4fd7-a1c9-03f8420d44e4
  Args:
    source: Nikolaus
    literal_value: 1897
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (952213a7-2a13-4a22-87f4-98b08b728f2c)
 Call ID: 952213a7-2a13-4a22-87f4-98b08b728f2c
  Args:
    literal_value: 1970
    source: Nikolaus
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (807db2b2-41e1-41f5-87a5-421a7323a35f)
 Call ID: 807db2b2-41e1-41f5-87a5-421a7323a35f
  Args:
    type: :Man
    source: Frederick_Augustus_II
  AssignClass (2ef3563f-be09-482b-ac52-4ff24d82e64a)
 Call ID: 2ef3563f-be09-482b-ac52-4ff24d82e64a
  Args:
    type: :Person
    source: Frederick_Augustus_II
  AddLiteral (6de80649-05e4-49e6-97ca-42f8c5422f88)
 Call ID: 6de80649-05e4-49e6-97ca-42f8c5422f88
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1852
    source: Frederick_Augustus_II
  AddLiteral (a5feb66f-b934-4ae6-a326-079ebcbf7809)
 Call ID: a5feb66f-b934-4ae6-a326-079ebcbf7809
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Frederick_Augustus_II
    literal_value: 1931
  AddTriple (a3763092-de71-42b8-ba14-05cc827354a9)
 Call ID: a3763092-de71-42b8-ba14-05cc827354a9
  Args:
    relation: :isSonOf
    target: Frederick_Augustus_II
    source: Nikolaus
  AssignClass (128525b4-03e3-419e-91e2-87acda3ac5c2)
 Call ID: 128525b4-03e3-419e-91e2-87acda3ac5c2
  Args:
    type: :Man
    source: Peter_II
  AssignClass (cda84933-1e8e-431e-bfc7-5d4bfa243a72)
 Call ID: cda84933-1e8e-431e-bfc7-5d4bfa243a72
  Args:
    type: :Person
    source: Peter_II
  AssignClass (6bba8c16-1217-4b6a-87d5-e15ea3c4ca58)
 Call ID: 6bba8c16-1217-4b6a-87d5-e15ea3c4ca58
  Args:
    type: :Woman
    source: Elisabeth_of_Saxe-Altenburg
  AssignClass (1306b982-579c-43e5-8554-71e95f57313f)
 Call ID: 1306b982-579c-43e5-8554-71e95f57313f
  Args:
    type: :Person
    source: Elisabeth_of_Saxe-Altenburg
  AddTriple (30a0fae5-815f-4358-a64d-fb846729c41c)
 Call ID: 30a0fae5-815f-4358-a64d-fb846729c41c
  Args:
    relation: :isSonOf
    target: Peter_II
    source: Frederick_Augustus_II
  AddTriple (36a6d50b-2ee6-4d76-bca6-d44fc94d91ba)
 Call ID: 36a6d50b-2ee6-4d76-bca6-d44fc94d91ba
  Args:
    relation: :hasMother
    target: Elisabeth_of_Saxe-Altenburg
    source: Frederick_Augustus_II
  AssignClass (6ce64ae9-455f-4846-b6b0-5ec40f0a34cf)
 Call ID: 6ce64ae9-455f-4846-b6b0-5ec40f0a34cf
  Args:
    type: :Woman
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (56842ceb-0667-4703-9340-e32f05b38b21)
 Call ID: 56842ceb-0667-4703-9340-e32f05b38b21
  Args:
    type: :Person
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (cda079b6-30e1-4ee1-9b87-d0323d2cee9c)
 Call ID: cda079b6-30e1-4ee1-9b87-d0323d2cee9c
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1869
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (3f2b60d9-f864-4f78-a01c-b38e376a4c2d)
 Call ID: 3f2b60d9-f864-4f78-a01c-b38e376a4c2d
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1955
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (ee0f16af-1da9-427b-adc5-e2de285dd1cf)
 Call ID: ee0f16af-1da9-427b-adc5-e2de285dd1cf
  Args:
    source: Nikolaus
    target: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (70de626c-d058-4b6f-891f-269128f25ef4)
 Call ID: 70de626c-d058-4b6f-891f-269128f25ef4
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (aa26a67c-ac09-48ea-ab1a-7918a81a468f)
 Call ID: aa26a67c-ac09-48ea-ab1a-7918a81a468f
  Args:
    type: :Person
    source: Frederick_Francis_II
  AssignClass (5699f8b1-1183-4c5c-91f2-f3b0ed08e768)
 Call ID: 5699f8b1-1183-4c5c-91f2-f3b0ed08e768
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (a4c760a1-85a2-4b0d-a8da-addc5757e146)
 Call ID: a4c760a1-85a2-4b0d-a8da-addc5757e146
  Args:
    type: :Person
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (94340d19-e99e-44b1-97d3-a9ac7781fd34)
 Call ID: 94340d19-e99e-44b1-97d3-a9ac7781fd34
  Args:
    relation: :isDaughterOf
    target: Frederick_Francis_II
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (189ed5bd-4dc9-417e-893a-ac9544b27aca)
 Call ID: 189ed5bd-4dc9-417e-893a-ac9544b27aca
  Args:
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (ab747815-a61b-4e81-8f06-7b73c5efe1f7)
 Call ID: ab747815-a61b-4e81-8f06-7b73c5efe1f7
  Args:
    type: :Woman
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (15d7d58a-148e-4c98-81d3-062f63e68a7e)
 Call ID: 15d7d58a-148e-4c98-81d3-062f63e68a7e
  Args:
    type: :Person
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (c6c1628e-c91a-4fc0-8e12-629258ae1d0d)
 Call ID: c6c1628e-c91a-4fc0-8e12-629258ae1d0d
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1899
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (4f94082e-1f94-4586-811d-aedd995037d1)
 Call ID: 4f94082e-1f94-4586-811d-aedd995037d1
  Args:
    literal_value: 1948
    source: Helena_of_Waldeck_and_Pyrmont
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (42e9225b-8fd1-49dd-910e-6ebe249a3109)
 Call ID: 42e9225b-8fd1-49dd-910e-6ebe249a3109
  Args:
    literal_value: 1921
    source: Nikolaus
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (0ec5c990-3551-4626-9a60-009b4f65562f)
 Call ID: 0ec5c990-3551-4626-9a60-009b4f65562f
  Args:
    target: Helena_of_Waldeck_and_Pyrmont
    source: Nikolaus
    relation: :hasRelation
  AssignClass (53000e8f-9814-4436-80ef-4a340a24312f)
 Call ID: 53000e8f-9814-4436-80ef-4a340a24312f
  Args:
    type: :Man
    source: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (dcf91608-401e-4758-a625-3208f80fcb7c)
 Call ID: dcf91608-401e-4758-a625-3208f80fcb7c
  Args:
    type: :Person
    source: Friedrich_of_Waldeck_and_Pyrmont
  AssignClass (beb324df-63f3-4d4b-aa8a-3efa9adb263a)
 Call ID: beb324df-63f3-4d4b-aa8a-3efa9adb263a
  Args:
    type: :Woman
    source: Bathildis_of_Schaumburg-Lippe
  AssignClass (9d4e8b52-057f-4d78-9c9e-c5def67018af)
 Call ID: 9d4e8b52-057f-4d78-9c9e-c5def67018af
  Args:
    type: :Person
    source: Bathildis_of_Schaumburg-Lippe
  AddTriple (43de7899-3df6-4c9a-9abd-83ce09a8ed80)
 Call ID: 43de7899-3df6-4c9a-9abd-83ce09a8ed80
  Args:
    relation: :isDaughterOf
    source: Helena_of_Waldeck_and_Pyrmont
    target: Friedrich_of_Waldeck_and_Pyrmont
  AddTriple (f46d25d3-3e84-4928-8727-c7a78cf1b3fa)
 Call ID: f46d25d3-3e84-4928-8727-c7a78cf1b3fa
  Args:
    relation: :hasMother
    source: Helena_of_Waldeck_and_Pyrmont
    target: Bathildis_of_Schaumburg-Lippe
  AssignClass (6e17d6a0-4a62-470b-97a1-e72eb89a939f)
 Call ID: 6e17d6a0-4a62-470b-97a1-e72eb89a939f
  Args:
    type: :Woman
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AssignClass (b669d09f-9a9a-4561-b575-a30c2e3bbac2)
 Call ID: b669d09f-9a9a-4561-b575-a30c2e3bbac2
  Args:
    type: :Person
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AddLiteral (a9d92676-f7b1-403a-91b3-d829774d5f14)
 Call ID: a9d92676-f7b1-403a-91b3-d829774d5f14
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    literal_value: 1903
  AddLiteral (16ecf63e-be17-4d8b-b390-da0e8d473f8c)
 Call ID: 16ecf63e-be17-4d8b-b390-da0e8d473f8c
  Args:
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    literal_value: 1991
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (0d1c655d-b300-4e83-96d8-75956e411b08)
 Call ID: 0d1c655d-b300-4e83-96d8-75956e411b08
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1950
    source: Nikolaus
  AddTriple (05f27928-01e8-4ba4-a3c0-dccb681a6499)
 Call ID: 05f27928-01e8-4ba4-a3c0-dccb681a6499
  Args:
    relation: :hasRelation
    target: Anne-Marie_von_Schutzbar_genannt_Milchling
    source: Nikolaus
  AssignClass (c28690ab-0740-487a-b8f4-14a89662976a)
 Call ID: c28690ab-0740-487a-b8f4-14a89662976a
  Args:
    type: :Man
    source: Rudolf_von_Schutzbar_gen_Milchling
  AssignClass (748eff79-4bc6-45ed-b055-bf9944eac069)
 Call ID: 748eff79-4bc6-45ed-b055-bf9944eac069
  Args:
    type: :Person
    source: Rudolf_von_Schutzbar_gen_Milchling
  AddLiteral (84329a52-399e-4cc7-a55f-8eaa2fba52b3)
 Call ID: 84329a52-399e-4cc7-a55f-8eaa2fba52b3
  Args:
    source: Rudolf_von_Schutzbar_gen_Milchling
    literal_value: 1853
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (49d2807e-5281-4404-a015-a51548bce8e5)
 Call ID: 49d2807e-5281-4404-a015-a51548bce8e5
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1935
    source: Rudolf_von_Schutzbar_gen_Milchling
  AssignClass (c7166cfb-c574-4580-8cb4-f2ffce5b8737)
 Call ID: c7166cfb-c574-4580-8cb4-f2ffce5b8737
  Args:
    type: :Woman
    source: Rose_Marston
  AssignClass (31cb3246-c74d-4dad-a11a-d5b18b9a5cdd)
 Call ID: 31cb3246-c74d-4dad-a11a-d5b18b9a5cdd
  Args:
    type: :Person
    source: Rose_Marston
  AddLiteral (91cd538c-4090-42c1-b5fe-32240578bc9d)
 Call ID: 91cd538c-4090-42c1-b5fe-32240578bc9d
  Args:
    source: Rose_Marston
    literal_value: 1872
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b08156b8-b85a-4c17-bdab-2d0ae1710b67)
 Call ID: b08156b8-b85a-4c17-bdab-2d0ae1710b67
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Rose_Marston
    literal_value: 1957
  AddTriple (3a881249-a1f8-4746-8ab6-502ea5726080)
 Call ID: 3a881249-a1f8-4746-8ab6-502ea5726080
  Args:
    target: Rudolf_von_Schutzbar_gen_Milchling
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :isDaughterOf
  AddTriple (f89e3bf3-175d-4bc8-a1e6-cfbf0ab2b420)
 Call ID: f89e3bf3-175d-4bc8-a1e6-cfbf0ab2b420
  Args:
    relation: :hasMother
    target: Rose_Marston
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  Finish (e82b7759-d0b2-4f41-b848-c01cced8333b)
 Call ID: e82b7759-d0b2-4f41-b848-c01cced8333b
  Args: