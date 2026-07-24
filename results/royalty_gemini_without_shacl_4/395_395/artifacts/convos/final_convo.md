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
  AssignClass (5fd388ec-7f7f-4220-8b30-5189ba912090)
 Call ID: 5fd388ec-7f7f-4220-8b30-5189ba912090
  Args:
    type: :Man
    source: Nikolaus_of_Oldenburg
  AssignClass (4d2c38e0-81ed-4293-859c-d95ed0b03f6d)
 Call ID: 4d2c38e0-81ed-4293-859c-d95ed0b03f6d
  Args:
    source: Nikolaus_of_Oldenburg
    type: :Person
  AddLiteral (c44f20f9-81c6-4cea-a701-84a55b1eab13)
 Call ID: c44f20f9-81c6-4cea-a701-84a55b1eab13
  Args:
    source: Nikolaus_of_Oldenburg
    relation: :hasBirthYear
    literal_value: 1897
    literal_type: xsd:integer
  AddLiteral (2aa6b099-b64c-4418-a3fa-466c39dd98e7)
 Call ID: 2aa6b099-b64c-4418-a3fa-466c39dd98e7
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Nikolaus_of_Oldenburg
    literal_value: 1970
  AssignClass (55dbec63-5068-4a11-a488-a292ef9976b1)
 Call ID: 55dbec63-5068-4a11-a488-a292ef9976b1
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (3e7b59e1-e2c2-4621-a3e5-89b995b174d0)
 Call ID: 3e7b59e1-e2c2-4621-a3e5-89b995b174d0
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    type: :Person
  AddLiteral (9981369d-2035-4d06-9f54-ced9e0086858)
 Call ID: 9981369d-2035-4d06-9f54-ced9e0086858
  Args:
    literal_type: xsd:integer
    source: Frederick_Augustus_II_of_Oldenburg
    relation: :hasBirthYear
    literal_value: 1852
  AddLiteral (a746e54a-e899-40fe-a6ed-ca107460a231)
 Call ID: a746e54a-e899-40fe-a6ed-ca107460a231
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Frederick_Augustus_II_of_Oldenburg
    literal_value: 1931
  AddTriple (9acd3b54-673a-491e-a1a3-81ec86bacb3d)
 Call ID: 9acd3b54-673a-491e-a1a3-81ec86bacb3d
  Args:
    target: Frederick_Augustus_II_of_Oldenburg
    relation: :hasFather
    source: Nikolaus_of_Oldenburg
  AssignClass (9c4d22d7-59de-4b2c-aeeb-caca9e17bd85)
 Call ID: 9c4d22d7-59de-4b2c-aeeb-caca9e17bd85
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (bedac75b-378a-49a0-9126-32ed9b9750d8)
 Call ID: bedac75b-378a-49a0-9126-32ed9b9750d8
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (211487ef-f93b-4944-8cef-89ccedf19426)
 Call ID: 211487ef-f93b-4944-8cef-89ccedf19426
  Args:
    literal_type: xsd:integer
    literal_value: 1869
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasBirthYear
  AddLiteral (fa5a4ebe-8aed-4036-a395-e7b12429ef98)
 Call ID: fa5a4ebe-8aed-4036-a395-e7b12429ef98
  Args:
    literal_type: xsd:integer
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasDeathYear
    literal_value: 1955
  AddTriple (46e511d3-c471-4e9b-8edf-3529b2c26867)
 Call ID: 46e511d3-c471-4e9b-8edf-3529b2c26867
  Args:
    target: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    source: Nikolaus_of_Oldenburg
    relation: :hasMother
  AssignClass (44a7990c-0684-4086-8170-bec05d2653e1)
 Call ID: 44a7990c-0684-4086-8170-bec05d2653e1
  Args:
    type: :Man
    source: Peter_II_of_Oldenburg
  AssignClass (794a4f10-8c59-453a-a42f-3106628ed15d)
 Call ID: 794a4f10-8c59-453a-a42f-3106628ed15d
  Args:
    type: :Person
    source: Peter_II_of_Oldenburg
  AddTriple (3511fa8d-ae8a-4016-b60d-215ab3a30509)
 Call ID: 3511fa8d-ae8a-4016-b60d-215ab3a30509
  Args:
    target: Peter_II_of_Oldenburg
    source: Frederick_Augustus_II_of_Oldenburg
    relation: :hasFather
  AssignClass (69f5fafd-cb33-443b-ae0c-9d6ca331fd66)
 Call ID: 69f5fafd-cb33-443b-ae0c-9d6ca331fd66
  Args:
    source: Elisabeth_of_Saxe-Altenburg
    type: :Woman
  AssignClass (fd4cd253-f8f4-42f6-aabe-93f89fc122cf)
 Call ID: fd4cd253-f8f4-42f6-aabe-93f89fc122cf
  Args:
    source: Elisabeth_of_Saxe-Altenburg
    type: :Person
  AddTriple (6bd424b8-024b-4136-9059-1fea4cb18cc4)
 Call ID: 6bd424b8-024b-4136-9059-1fea4cb18cc4
  Args:
    relation: :hasMother
    source: Frederick_Augustus_II_of_Oldenburg
    target: Elisabeth_of_Saxe-Altenburg
  AssignClass (557de54b-9341-4e4f-ae40-2dedb94f72b9)
 Call ID: 557de54b-9341-4e4f-ae40-2dedb94f72b9
  Args:
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (903cc808-ddd7-400f-8b5d-243f8d768f18)
 Call ID: 903cc808-ddd7-400f-8b5d-243f8d768f18
  Args:
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (5fcee43e-ddb6-4152-9312-6ec9409371c4)
 Call ID: 5fcee43e-ddb6-4152-9312-6ec9409371c4
  Args:
    target: Frederick_Francis_II_of_Mecklenburg-Schwerin
    relation: :hasFather
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AssignClass (8c0e2357-4e14-4dad-9318-67ea79666242)
 Call ID: 8c0e2357-4e14-4dad-9318-67ea79666242
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (b2403b00-6c70-445a-9964-568810db33f7)
 Call ID: b2403b00-6c70-445a-9964-568810db33f7
  Args:
    source: Marie_of_Schwarzburg-Rudolstadt
    type: :Person
  AddTriple (01a41b0f-f605-4d4c-b8ef-95fa40713c1f)
 Call ID: 01a41b0f-f605-4d4c-b8ef-95fa40713c1f
  Args:
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (fd8a6346-247c-469f-a85a-48621b54bc52)
 Call ID: fd8a6346-247c-469f-a85a-48621b54bc52
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    type: :Woman
  AssignClass (c6324007-12af-44b4-acc2-e24ea4426a68)
 Call ID: c6324007-12af-44b4-acc2-e24ea4426a68
  Args:
    type: :Person
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (efd77bc4-a55d-47fc-ae1a-769c5d84a2df)
 Call ID: efd77bc4-a55d-47fc-ae1a-769c5d84a2df
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Helena_of_Waldeck_and_Pyrmont
    literal_value: 1899
  AddLiteral (a09479e4-9031-4cf1-9cc7-cce5becea1c6)
 Call ID: a09479e4-9031-4cf1-9cc7-cce5becea1c6
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: Helena_of_Waldeck_and_Pyrmont
    relation: :hasDeathYear
  AddLiteral (6a590763-4e35-4f9d-8d45-ad872579e5d2)
 Call ID: 6a590763-4e35-4f9d-8d45-ad872579e5d2
  Args:
    literal_value: 1921
    source: Nikolaus_of_Oldenburg
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (77bffb21-da9a-4ba4-9b85-886d06de23cd)
 Call ID: 77bffb21-da9a-4ba4-9b85-886d06de23cd
  Args:
    source: Friedrich_Prince_of_Waldeck_and_Pyrmont
    type: :Man
  AssignClass (cfd8644f-b027-4e4b-b707-8efadc93c02a)
 Call ID: cfd8644f-b027-4e4b-b707-8efadc93c02a
  Args:
    source: Friedrich_Prince_of_Waldeck_and_Pyrmont
    type: :Person
  AddTriple (8bb51404-8e71-44e7-b671-fb009bbc940c)
 Call ID: 8bb51404-8e71-44e7-b671-fb009bbc940c
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    relation: :hasFather
    target: Friedrich_Prince_of_Waldeck_and_Pyrmont
  AssignClass (89a2c2ee-d291-40dd-93c3-8fed9c58355d)
 Call ID: 89a2c2ee-d291-40dd-93c3-8fed9c58355d
  Args:
    type: :Woman
    source: Bathildis_of_Schaumburg-Lippe
  AssignClass (56a4ab03-491b-4e64-bba2-ac1dd10c3d91)
 Call ID: 56a4ab03-491b-4e64-bba2-ac1dd10c3d91
  Args:
    source: Bathildis_of_Schaumburg-Lippe
    type: :Person
  AddTriple (d4ecde80-7b6b-4b69-ac15-681f29fcd976)
 Call ID: d4ecde80-7b6b-4b69-ac15-681f29fcd976
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    relation: :hasMother
    target: Bathildis_of_Schaumburg-Lippe
  AssignClass (18d376c9-4bcf-481f-bae8-17287b4b6f3c)
 Call ID: 18d376c9-4bcf-481f-bae8-17287b4b6f3c
  Args:
    type: :Woman
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AssignClass (761f345a-235b-450d-9a4a-279dc7294894)
 Call ID: 761f345a-235b-450d-9a4a-279dc7294894
  Args:
    type: :Person
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AddLiteral (61cadc33-2f4b-4215-9158-102207554c02)
 Call ID: 61cadc33-2f4b-4215-9158-102207554c02
  Args:
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :hasBirthYear
    literal_value: 1903
    literal_type: xsd:integer
  AddLiteral (30bf0208-6440-4ed2-b303-bf7b50d14192)
 Call ID: 30bf0208-6440-4ed2-b303-bf7b50d14192
  Args:
    literal_type: xsd:integer
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :hasDeathYear
    literal_value: 1991
  AddLiteral (acb37361-df3a-4f39-afe0-01c59f9f857f)
 Call ID: acb37361-df3a-4f39-afe0-01c59f9f857f
  Args:
    literal_type: xsd:integer
    literal_value: 1950
    relation: :hasMarriageYear
    source: Nikolaus_of_Oldenburg
  AssignClass (d55bb7ad-04c6-40c0-a4cf-1fba857573cf)
 Call ID: d55bb7ad-04c6-40c0-a4cf-1fba857573cf
  Args:
    type: :Man
    source: Rudolf_von_Schutzbar_gen_Milchling
  AssignClass (83afcf70-ddcd-4c04-a228-4eb6893ea5e0)
 Call ID: 83afcf70-ddcd-4c04-a228-4eb6893ea5e0
  Args:
    type: :Person
    source: Rudolf_von_Schutzbar_gen_Milchling
  AddLiteral (a2991e2d-9324-4470-93f2-ff40bc7a55f7)
 Call ID: a2991e2d-9324-4470-93f2-ff40bc7a55f7
  Args:
    literal_type: xsd:integer
    literal_value: 1853
    source: Rudolf_von_Schutzbar_gen_Milchling
    relation: :hasBirthYear
  AddLiteral (8a6e975d-70ae-4561-955e-8876de1826e3)
 Call ID: 8a6e975d-70ae-4561-955e-8876de1826e3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Rudolf_von_Schutzbar_gen_Milchling
    literal_value: 1935
  AddTriple (5c50c606-7ce7-4985-b4d3-0bc7f4139a0e)
 Call ID: 5c50c606-7ce7-4985-b4d3-0bc7f4139a0e
  Args:
    relation: :hasFather
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    target: Rudolf_von_Schutzbar_gen_Milchling
  AssignClass (8d01bf2b-c86d-40c4-8b19-6cb1ccf9bf9d)
 Call ID: 8d01bf2b-c86d-40c4-8b19-6cb1ccf9bf9d
  Args:
    source: Rose_Marston
    type: :Woman
  AssignClass (d9c511fc-a84a-421f-89aa-d5957a0910bf)
 Call ID: d9c511fc-a84a-421f-89aa-d5957a0910bf
  Args:
    source: Rose_Marston
    type: :Person
  AddLiteral (7bd5c762-eeb8-4921-be73-f9e70d1b859c)
 Call ID: 7bd5c762-eeb8-4921-be73-f9e70d1b859c
  Args:
    literal_type: xsd:integer
    literal_value: 1872
    relation: :hasBirthYear
    source: Rose_Marston
  AddLiteral (76c747fd-f7bb-4504-b977-223e81d701eb)
 Call ID: 76c747fd-f7bb-4504-b977-223e81d701eb
  Args:
    relation: :hasDeathYear
    source: Rose_Marston
    literal_value: 1957
    literal_type: xsd:integer
  AddTriple (f7ad2795-bb4c-4453-b2ad-9f330bcaa454)
 Call ID: f7ad2795-bb4c-4453-b2ad-9f330bcaa454
  Args:
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :hasMother
    target: Rose_Marston
  Finish (717f9570-a68e-4118-a9e8-9e1505790ab5)
 Call ID: 717f9570-a68e-4118-a9e8-9e1505790ab5
  Args: