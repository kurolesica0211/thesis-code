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
Georg, Prince of Saxe-Meiningen (11 October 1892 – 6 January 1946) was the head of the house of Saxe-Meiningen from 1941 until his death.
He was born in Kassel as the eldest son of Prince Frederick Johann of Saxe-Meiningen (1861-1914) and Countess Adelaide of Lippe-Biesterfeld (1870–1948).
His father was a son of Georg II, Duke of Saxe-Meiningen and his mother a daughter of Count Ernst of Lippe-Biesterfeld.
Georg studied law at the Universities of Munich and Jena.
Georg suspended his studies to serve in World War I and saw action as a captain in a cavalry regiment.
After the death of his uncle Ernst on 29 December 1941, Georg succeeded to the headship of the house of Saxe-Meiningen and assumed the title of Duke of Saxe-Meiningen and style Georg III.
Georg and his family were expropriated without compensation in 1945.
Georg, who served as a major in the Wehrmacht died in the Russian prisoner of war camp near Cherepovets (Tscherepowetz in German) in Northern Russia.
His heir was his second and only surviving son Prince Frederick Alfred who renounced the succession, being a monk in 1953, allowing it to pass to his uncle Bernhard.
Marriage and children

He was married in Freiburg im Breisgau on 22 February 1919 to Countess Klara Marie von Korff genannt Schmising-Kerssenbrock (Darmstadt, 31 May 1895



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
  AssignClass (5be18b8a-10fb-43ef-b46b-07fb6322b4b1)
 Call ID: 5be18b8a-10fb-43ef-b46b-07fb6322b4b1
  Args:
    type: :Man
    source: Georg_Prince_of_Saxe_Meiningen
  AssignClass (ee2bcef6-142c-4dd6-99a1-3fefb31c783c)
 Call ID: ee2bcef6-142c-4dd6-99a1-3fefb31c783c
  Args:
    type: :Person
    source: Georg_Prince_of_Saxe_Meiningen
  AddLiteral (b7af683f-1bdb-4620-ac8b-324ecafbe2c0)
 Call ID: b7af683f-1bdb-4620-ac8b-324ecafbe2c0
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Georg_Prince_of_Saxe_Meiningen
    literal_value: 1892
  AddLiteral (277a462e-6ee3-4134-8165-fe4b33be9f41)
 Call ID: 277a462e-6ee3-4134-8165-fe4b33be9f41
  Args:
    source: Georg_Prince_of_Saxe_Meiningen
    literal_value: 1946
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (475c4efc-22d9-4b2a-8647-b6bf1c2d3d95)
 Call ID: 475c4efc-22d9-4b2a-8647-b6bf1c2d3d95
  Args:
    source: Prince_Frederick_Johann_of_Saxe_Meiningen
    type: :Man
  AssignClass (02f35bb5-3aab-4503-a4ac-1762da56635d)
 Call ID: 02f35bb5-3aab-4503-a4ac-1762da56635d
  Args:
    type: :Person
    source: Prince_Frederick_Johann_of_Saxe_Meiningen
  AddLiteral (f6786593-ced1-4c6a-b8a8-65e44fd3efe1)
 Call ID: f6786593-ced1-4c6a-b8a8-65e44fd3efe1
  Args:
    literal_type: xsd:integer
    literal_value: 1861
    source: Prince_Frederick_Johann_of_Saxe_Meiningen
    relation: :hasBirthYear
  AddLiteral (dcde3159-5871-4865-a8e1-a34a0ae24362)
 Call ID: dcde3159-5871-4865-a8e1-a34a0ae24362
  Args:
    relation: :hasDeathYear
    source: Prince_Frederick_Johann_of_Saxe_Meiningen
    literal_value: 1914
    literal_type: xsd:integer
  AssignClass (a88437aa-486b-452b-9817-051c14280267)
 Call ID: a88437aa-486b-452b-9817-051c14280267
  Args:
    type: :Woman
    source: Countess_Adelaide_of_Lippe_Biesterfeld
  AssignClass (9276d731-9adc-4179-8e65-1bd51843b065)
 Call ID: 9276d731-9adc-4179-8e65-1bd51843b065
  Args:
    type: :Person
    source: Countess_Adelaide_of_Lippe_Biesterfeld
  AddLiteral (e3cab196-2b6a-48e3-a270-0f5ccc7df2e4)
 Call ID: e3cab196-2b6a-48e3-a270-0f5ccc7df2e4
  Args:
    literal_type: xsd:integer
    source: Countess_Adelaide_of_Lippe_Biesterfeld
    literal_value: 1870
    relation: :hasBirthYear
  AddLiteral (0ce5e63a-d558-483f-897e-5c14dc34300a)
 Call ID: 0ce5e63a-d558-483f-897e-5c14dc34300a
  Args:
    source: Countess_Adelaide_of_Lippe_Biesterfeld
    literal_value: 1948
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (dc3df0d2-c4d4-4590-9597-40160a2ff2b3)
 Call ID: dc3df0d2-c4d4-4590-9597-40160a2ff2b3
  Args:
    source: Georg_Prince_of_Saxe_Meiningen
    relation: :hasFather
    target: Prince_Frederick_Johann_of_Saxe_Meiningen
  AddTriple (bec48a9f-0911-4790-ac0f-6e4d23d735f2)
 Call ID: bec48a9f-0911-4790-ac0f-6e4d23d735f2
  Args:
    relation: :hasMother
    source: Georg_Prince_of_Saxe_Meiningen
    target: Countess_Adelaide_of_Lippe_Biesterfeld
  AssignClass (4a408adc-95bd-4970-b7af-f1af114c5945)
 Call ID: 4a408adc-95bd-4970-b7af-f1af114c5945
  Args:
    source: Georg_II_Duke_of_Saxe_Meiningen
    type: :Man
  AssignClass (2dea18c6-5e3b-4eab-b8ba-437688e3fd0f)
 Call ID: 2dea18c6-5e3b-4eab-b8ba-437688e3fd0f
  Args:
    type: :Person
    source: Georg_II_Duke_of_Saxe_Meiningen
  AddTriple (8c39b57c-28f2-4e36-a818-f5d3f2ccd037)
 Call ID: 8c39b57c-28f2-4e36-a818-f5d3f2ccd037
  Args:
    target: Georg_II_Duke_of_Saxe_Meiningen
    relation: :hasFather
    source: Prince_Frederick_Johann_of_Saxe_Meiningen
  AssignClass (061e1341-ffb0-4d02-8d30-1bfc392523d9)
 Call ID: 061e1341-ffb0-4d02-8d30-1bfc392523d9
  Args:
    type: :Man
    source: Count_Ernst_of_Lippe_Biesterfeld
  AssignClass (0dc38e6e-a5c9-4ba3-b077-30205ef128aa)
 Call ID: 0dc38e6e-a5c9-4ba3-b077-30205ef128aa
  Args:
    type: :Person
    source: Count_Ernst_of_Lippe_Biesterfeld
  AddTriple (da0e6818-b2b3-4dec-85ba-6c6c6c7c0c3d)
 Call ID: da0e6818-b2b3-4dec-85ba-6c6c6c7c0c3d
  Args:
    source: Countess_Adelaide_of_Lippe_Biesterfeld
    relation: :hasFather
    target: Count_Ernst_of_Lippe_Biesterfeld
  AssignClass (5d9cc076-d04f-4f2d-a584-4547143a884a)
 Call ID: 5d9cc076-d04f-4f2d-a584-4547143a884a
  Args:
    source: Prince_Frederick_Alfred
    type: :Man
  AssignClass (aee64f09-0cab-4046-b353-d89399144ed0)
 Call ID: aee64f09-0cab-4046-b353-d89399144ed0
  Args:
    type: :Person
    source: Prince_Frederick_Alfred
  AddTriple (6f481937-9abd-4120-87fe-00dde4fa87ad)
 Call ID: 6f481937-9abd-4120-87fe-00dde4fa87ad
  Args:
    target: Georg_Prince_of_Saxe_Meiningen
    relation: :hasFather
    source: Prince_Frederick_Alfred
  AssignClass (b98311a4-b131-4fd2-a619-47a132f02e3c)
 Call ID: b98311a4-b131-4fd2-a619-47a132f02e3c
  Args:
    source: Bernhard
    type: :Man
  AssignClass (80e28160-fe07-4839-b351-770ef9665d1f)
 Call ID: 80e28160-fe07-4839-b351-770ef9665d1f
  Args:
    source: Bernhard
    type: :Person
  AssignClass (cba2bd08-8e57-4e50-be0a-f42e895ba4f0)
 Call ID: cba2bd08-8e57-4e50-be0a-f42e895ba4f0
  Args:
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising_Kerssenbrock
    type: :Woman
  AssignClass (24804c8f-dabf-4647-8fbf-fc1e825d60d4)
 Call ID: 24804c8f-dabf-4647-8fbf-fc1e825d60d4
  Args:
    type: :Person
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising_Kerssenbrock
  AddLiteral (6fe47f20-cb2f-4435-bef4-662053a3e16f)
 Call ID: 6fe47f20-cb2f-4435-bef4-662053a3e16f
  Args:
    source: Countess_Klara_Marie_von_Korff_genannt_Schmising_Kerssenbrock
    literal_value: 1895
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (3acb4991-256c-4cea-af37-25f57ff68ec0)
 Call ID: 3acb4991-256c-4cea-af37-25f57ff68ec0
  Args:
    literal_value: 1919
    source: Georg_Prince_of_Saxe_Meiningen
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (cb31a635-0be4-41a2-8460-f61d1ab18a85)
 Call ID: cb31a635-0be4-41a2-8460-f61d1ab18a85
  Args: