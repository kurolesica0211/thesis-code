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
  AssignClass (6c3395e1-7fcf-4459-8584-8cda91aa8080)
 Call ID: 6c3395e1-7fcf-4459-8584-8cda91aa8080
  Args:
    source: Nikolaus_of_Oldenburg
    type: :Man
  AssignClass (a31a39f9-8e4a-4523-a0cd-475d7d639ab4)
 Call ID: a31a39f9-8e4a-4523-a0cd-475d7d639ab4
  Args:
    type: :Man
    source: Frederick_Augustus_II_of_Oldenburg
  AssignClass (62a1fc5f-ef97-45cc-8b31-e3929017cb27)
 Call ID: 62a1fc5f-ef97-45cc-8b31-e3929017cb27
  Args:
    type: :Man
    source: Peter_II_of_Oldenburg
  AssignClass (bfa9b31e-0725-450b-a298-9260bc666c21)
 Call ID: bfa9b31e-0725-450b-a298-9260bc666c21
  Args:
    source: Elisabeth_of_Saxe-Altenburg
    type: :Woman
  AssignClass (ac949a48-960d-43a4-a50d-564cd38e1f85)
 Call ID: ac949a48-960d-43a4-a50d-564cd38e1f85
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    type: :Woman
  AssignClass (c1bc32d3-f79b-496d-8f1e-39dd6a001d05)
 Call ID: c1bc32d3-f79b-496d-8f1e-39dd6a001d05
  Args:
    type: :Man
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AssignClass (1551532a-181e-42f5-b72e-1c3664649613)
 Call ID: 1551532a-181e-42f5-b72e-1c3664649613
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (0fe17215-9da9-458c-9d22-74bfee074258)
 Call ID: 0fe17215-9da9-458c-9d22-74bfee074258
  Args:
    type: :Woman
    source: Helena_of_Waldeck_and_Pyrmont
  AssignClass (02428ee3-9b81-4f2e-83ac-22802e57c7aa)
 Call ID: 02428ee3-9b81-4f2e-83ac-22802e57c7aa
  Args:
    source: Friedrich_of_Waldeck_and_Pyrmont
    type: :Man
  AssignClass (bc47f4e6-0355-4f4e-9b42-84f2e857524c)
 Call ID: bc47f4e6-0355-4f4e-9b42-84f2e857524c
  Args:
    source: Bathildis_of_Schaumburg-Lippe
    type: :Woman
  AssignClass (c8cc0ab1-b93d-45e3-8ec8-d6423aa32bf2)
 Call ID: c8cc0ab1-b93d-45e3-8ec8-d6423aa32bf2
  Args:
    type: :Woman
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AssignClass (b0f3faf2-fcfa-4a5d-816e-8e20a9d76c80)
 Call ID: b0f3faf2-fcfa-4a5d-816e-8e20a9d76c80
  Args:
    source: Bechtold_von_Bernstorff
    type: :Man
  AssignClass (434223d5-1473-40d1-b25c-84930150c1e3)
 Call ID: 434223d5-1473-40d1-b25c-84930150c1e3
  Args:
    source: Rudolf_von_Schutzbar_genannt_Milchling
    type: :Man
  AssignClass (1c8a48df-cc5b-41f1-8a62-acb3b8987aa5)
 Call ID: 1c8a48df-cc5b-41f1-8a62-acb3b8987aa5
  Args:
    source: Rose_Marston
    type: :Woman
  AddLiteral (ff608b15-2b1e-4149-a011-1cec7a0497ca)
 Call ID: ff608b15-2b1e-4149-a011-1cec7a0497ca
  Args:
    source: Nikolaus_of_Oldenburg
    relation: :hasBirthYear
    literal_value: 1897
    literal_type: xsd:integer
  AddLiteral (676c115d-4180-474c-abea-c12deb42243b)
 Call ID: 676c115d-4180-474c-abea-c12deb42243b
  Args:
    literal_value: 1970
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Nikolaus_of_Oldenburg
  AddLiteral (b6bd5af4-5efa-4beb-9021-becd5c77e5d2)
 Call ID: b6bd5af4-5efa-4beb-9021-becd5c77e5d2
  Args:
    relation: :hasBirthYear
    literal_value: 1852
    literal_type: xsd:integer
    source: Frederick_Augustus_II_of_Oldenburg
  AddLiteral (59118d6c-95a7-4336-a3cb-4c76c9fccf1b)
 Call ID: 59118d6c-95a7-4336-a3cb-4c76c9fccf1b
  Args:
    source: Frederick_Augustus_II_of_Oldenburg
    literal_value: 1931
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (ae173c11-8f7d-4274-9ac5-2cb711b4383d)
 Call ID: ae173c11-8f7d-4274-9ac5-2cb711b4383d
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    literal_value: 1869
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (f3361bad-e76f-4825-b60a-688386e5130e)
 Call ID: f3361bad-e76f-4825-b60a-688386e5130e
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1955
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddLiteral (c97ee01f-6bd4-4778-af95-1618187d2384)
 Call ID: c97ee01f-6bd4-4778-af95-1618187d2384
  Args:
    source: Helena_of_Waldeck_and_Pyrmont
    relation: :hasBirthYear
    literal_value: 1899
    literal_type: xsd:integer
  AddLiteral (37b3c835-f65b-4fc8-95b8-603cf12bae87)
 Call ID: 37b3c835-f65b-4fc8-95b8-603cf12bae87
  Args:
    relation: :hasDeathYear
    literal_value: 1948
    literal_type: xsd:integer
    source: Helena_of_Waldeck_and_Pyrmont
  AddLiteral (32f153b5-b85f-49f4-87c4-978bca4d1665)
 Call ID: 32f153b5-b85f-49f4-87c4-978bca4d1665
  Args:
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1903
  AddLiteral (1d1c851f-25dc-488f-b9d5-bbc4251c566b)
 Call ID: 1d1c851f-25dc-488f-b9d5-bbc4251c566b
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1991
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
  AddLiteral (bf7ac1cd-c77c-4082-871d-730da4d20cde)
 Call ID: bf7ac1cd-c77c-4082-871d-730da4d20cde
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1853
    source: Rudolf_von_Schutzbar_genannt_Milchling
  AddLiteral (c0ba8c43-8ef0-49b9-81b5-7a70ad88f6b6)
 Call ID: c0ba8c43-8ef0-49b9-81b5-7a70ad88f6b6
  Args:
    source: Rudolf_von_Schutzbar_genannt_Milchling
    relation: :hasDeathYear
    literal_value: 1935
    literal_type: xsd:integer
  AddLiteral (a1eca480-5158-47d2-823c-71a019d75746)
 Call ID: a1eca480-5158-47d2-823c-71a019d75746
  Args:
    source: Rose_Marston
    literal_type: xsd:integer
    literal_value: 1872
    relation: :hasBirthYear
  AddLiteral (df448fd3-24e2-42f0-ab52-0efca0386254)
 Call ID: df448fd3-24e2-42f0-ab52-0efca0386254
  Args:
    literal_value: 1957
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Rose_Marston
  AddTriple (711a7975-f29a-4f6d-ae92-75bae887823a)
 Call ID: 711a7975-f29a-4f6d-ae92-75bae887823a
  Args:
    source: Nikolaus_of_Oldenburg
    target: Frederick_Augustus_II_of_Oldenburg
    relation: :hasFather
  AddTriple (b40c3e49-a616-4299-8435-fc8ed38253e2)
 Call ID: b40c3e49-a616-4299-8435-fc8ed38253e2
  Args:
    relation: :hasMother
    source: Nikolaus_of_Oldenburg
    target: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (a939e9b8-8d2c-4c8e-9f6f-12498fa5a0f3)
 Call ID: a939e9b8-8d2c-4c8e-9f6f-12498fa5a0f3
  Args:
    target: Peter_II_of_Oldenburg
    source: Frederick_Augustus_II_of_Oldenburg
    relation: :hasFather
  AddTriple (9eab9670-1a09-4881-b909-f95f9b8e4ddc)
 Call ID: 9eab9670-1a09-4881-b909-f95f9b8e4ddc
  Args:
    relation: :hasMother
    target: Elisabeth_of_Saxe-Altenburg
    source: Frederick_Augustus_II_of_Oldenburg
  AddTriple (7a6f7bcf-f36f-40d3-974a-82a68d5a2a79)
 Call ID: 7a6f7bcf-f36f-40d3-974a-82a68d5a2a79
  Args:
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
    target: Frederick_Francis_II_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (4c51c9e0-c503-465a-bf45-b82cc47b0e20)
 Call ID: 4c51c9e0-c503-465a-bf45-b82cc47b0e20
  Args:
    relation: :hasMother
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Elisabeth_Alexandrine_of_Mecklenburg-Schwerin
  AddTriple (02128938-ad85-4201-9c9a-8dbef874731e)
 Call ID: 02128938-ad85-4201-9c9a-8dbef874731e
  Args:
    relation: :hasFather
    source: Helena_of_Waldeck_and_Pyrmont
    target: Friedrich_of_Waldeck_and_Pyrmont
  AddTriple (866f1193-322d-4b6d-aa6f-2bad9fd99ec4)
 Call ID: 866f1193-322d-4b6d-aa6f-2bad9fd99ec4
  Args:
    target: Bathildis_of_Schaumburg-Lippe
    source: Helena_of_Waldeck_and_Pyrmont
    relation: :hasMother
  AddTriple (bdf03582-7ec5-45d8-8a6b-38c5e0b59fc2)
 Call ID: bdf03582-7ec5-45d8-8a6b-38c5e0b59fc2
  Args:
    target: Rudolf_von_Schutzbar_genannt_Milchling
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    relation: :hasFather
  AddTriple (4bf1e143-ea23-4400-a65e-d3ea00dd5784)
 Call ID: 4bf1e143-ea23-4400-a65e-d3ea00dd5784
  Args:
    source: Anne-Marie_von_Schutzbar_genannt_Milchling
    target: Rose_Marston
    relation: :hasMother
  AddLiteral (f985213a-9b0e-449c-a343-556b787f113c)
 Call ID: f985213a-9b0e-449c-a343-556b787f113c
  Args:
    source: Nikolaus_of_Oldenburg
    literal_value: 1921
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddLiteral (a8ed2da6-b8b0-48fc-a6c1-2f2d2caed597)
 Call ID: a8ed2da6-b8b0-48fc-a6c1-2f2d2caed597
  Args:
    source: Nikolaus_of_Oldenburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1950
  Finish (74b02c07-01a6-4d0c-925c-39150b75644c)
 Call ID: 74b02c07-01a6-4d0c-925c-39150b75644c
  Args: