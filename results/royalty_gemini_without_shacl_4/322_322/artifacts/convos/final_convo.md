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
Duchess Donata of Mecklenburg (born 11 March 1956) is the senior remaining member of the House of Mecklenburg-Schwerin.
Since there are no males left in the family, the Schwerin branch itself is considered extinct due to the Salic law of succession, leaving Mecklenburg-Strelitz as the only remaining line of the House of Mecklenburg.
Duchess of Mecklenburg

She was born in Kiel in the state of Schleswig-Holstein the eldest daughter of Duke Christian Louis of Mecklenburg-Schwerin and his wife Princess Barbara of Prussia (1920-1994).
Her father was the younger brother to the last surviving male of the House of Mecklenburg-Schwerin, Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin.
Her mother was the daughter of Princess Charlotte of Saxe-Altenburg, the eldest daughter of Ernst II, the last duke of Saxe-Altenburg.
Donata had only one sister Edwina (born 25 September 1960), and as her uncle had no children the House of Mecklenburg-Schwerin became extinct in the male line in 2001 when her uncle died.
As a result, the Mecklenburg-Strelitz line, headed by Borwin, Duke of Mecklenburg, will become the only surviving line of the House of Mecklenburg when both Donata and Edwina are dead.
Her paternal grandfather was the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
She is also a descendant of Christian IX of Denmark as her paternal grandmother, Alexandra of Hanover and Cumberland, a daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark, was the youngest daughter and fifth child of Christian IX of Denmark and Louise of Hesse-Kassel.
Her maternal grandfather was Prince Sigismund of Prussia, a grandson of Grand Duke Louis IV and Alice, Grand Duchess of Hesse and by Rhine, the second daughter of Queen Victoria.



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
  AssignClass (13646977-a28c-4dc8-a339-aabcc93b32bc)
 Call ID: 13646977-a28c-4dc8-a339-aabcc93b32bc
  Args:
    source: Donata_of_Mecklenburg
    type: :Woman
  AssignClass (fda302c0-3953-4ce5-969c-77842035a857)
 Call ID: fda302c0-3953-4ce5-969c-77842035a857
  Args:
    source: Donata_of_Mecklenburg
    type: :Person
  AddLiteral (7a24c3b4-d189-44c7-b5df-341e1121cf56)
 Call ID: 7a24c3b4-d189-44c7-b5df-341e1121cf56
  Args:
    source: Donata_of_Mecklenburg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1956
  AssignClass (2c4f12fa-a7d4-4def-8139-e67a1e9434cc)
 Call ID: 2c4f12fa-a7d4-4def-8139-e67a1e9434cc
  Args:
    type: :Man
    source: Christian_Louis_of_Mecklenburg-Schwerin
  AssignClass (d629acbf-a192-439b-8be7-0b9927d4d4a9)
 Call ID: d629acbf-a192-439b-8be7-0b9927d4d4a9
  Args:
    type: :Person
    source: Christian_Louis_of_Mecklenburg-Schwerin
  AssignClass (9530b26e-6892-44cb-bd2d-cae4e96ebcda)
 Call ID: 9530b26e-6892-44cb-bd2d-cae4e96ebcda
  Args:
    source: Barbara_of_Prussia
    type: :Woman
  AssignClass (2080a852-66ef-4cc9-bd3a-3bd6773866cb)
 Call ID: 2080a852-66ef-4cc9-bd3a-3bd6773866cb
  Args:
    source: Barbara_of_Prussia
    type: :Person
  AddLiteral (91ff016b-4496-40a8-8488-f3b21839c1fd)
 Call ID: 91ff016b-4496-40a8-8488-f3b21839c1fd
  Args:
    literal_value: 1920
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Barbara_of_Prussia
  AddLiteral (3a73fded-750d-430b-aaaf-e74b8ac18b6f)
 Call ID: 3a73fded-750d-430b-aaaf-e74b8ac18b6f
  Args:
    source: Barbara_of_Prussia
    literal_value: 1994
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (e84fcedf-17e8-479c-a004-5d835b932843)
 Call ID: e84fcedf-17e8-479c-a004-5d835b932843
  Args:
    source: Donata_of_Mecklenburg
    relation: :hasFather
    target: Christian_Louis_of_Mecklenburg-Schwerin
  AddTriple (40c265e0-d392-4264-a61d-801fe14268ef)
 Call ID: 40c265e0-d392-4264-a61d-801fe14268ef
  Args:
    source: Donata_of_Mecklenburg
    target: Barbara_of_Prussia
    relation: :hasMother
  AssignClass (05f58d67-d7b3-4ec2-abd4-5b609c418eb1)
 Call ID: 05f58d67-d7b3-4ec2-abd4-5b609c418eb1
  Args:
    type: :Man
    source: Friedrich_Franz_of_Mecklenburg-Schwerin
  AssignClass (1d13267a-bb51-47c0-86ad-8cf3135aa68a)
 Call ID: 1d13267a-bb51-47c0-86ad-8cf3135aa68a
  Args:
    source: Friedrich_Franz_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (4c520029-d00d-4f60-bc93-59ecc23ed750)
 Call ID: 4c520029-d00d-4f60-bc93-59ecc23ed750
  Args:
    source: Christian_Louis_of_Mecklenburg-Schwerin
    relation: :isBrotherOf
    target: Friedrich_Franz_of_Mecklenburg-Schwerin
  AssignClass (ed951799-3bd6-47d5-9ae9-5c27295ce4ae)
 Call ID: ed951799-3bd6-47d5-9ae9-5c27295ce4ae
  Args:
    source: Charlotte_of_Saxe-Altenburg
    type: :Woman
  AssignClass (ab954006-83dd-45d5-9568-a30d584cd969)
 Call ID: ab954006-83dd-45d5-9568-a30d584cd969
  Args:
    type: :Person
    source: Charlotte_of_Saxe-Altenburg
  AddTriple (15ebf9e0-97e4-43ae-bcc2-5f1885d43918)
 Call ID: 15ebf9e0-97e4-43ae-bcc2-5f1885d43918
  Args:
    source: Barbara_of_Prussia
    relation: :hasMother
    target: Charlotte_of_Saxe-Altenburg
  AssignClass (e4de3477-5c42-41b2-8a10-d3782c78b8f2)
 Call ID: e4de3477-5c42-41b2-8a10-d3782c78b8f2
  Args:
    source: Ernst_II_of_Saxe-Altenburg
    type: :Man
  AssignClass (4196dd14-7452-4302-a8e9-e46e6dbf27e9)
 Call ID: 4196dd14-7452-4302-a8e9-e46e6dbf27e9
  Args:
    source: Ernst_II_of_Saxe-Altenburg
    type: :Person
  AddTriple (433b6189-aeb2-4cac-81e2-9738e39c6ca5)
 Call ID: 433b6189-aeb2-4cac-81e2-9738e39c6ca5
  Args:
    source: Charlotte_of_Saxe-Altenburg
    target: Ernst_II_of_Saxe-Altenburg
    relation: :hasFather
  AssignClass (7dbe0150-2e5b-484f-b3e3-4acf9c2e8218)
 Call ID: 7dbe0150-2e5b-484f-b3e3-4acf9c2e8218
  Args:
    type: :Woman
    source: Edwina_of_Mecklenburg-Schwerin
  AssignClass (2189a1d5-51f4-40b0-9026-bbc35766be38)
 Call ID: 2189a1d5-51f4-40b0-9026-bbc35766be38
  Args:
    source: Edwina_of_Mecklenburg-Schwerin
    type: :Person
  AddLiteral (1218e030-cfec-42bd-9c00-e6f6a6b870a2)
 Call ID: 1218e030-cfec-42bd-9c00-e6f6a6b870a2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1960
    source: Edwina_of_Mecklenburg-Schwerin
  AddTriple (386e686a-bc4c-411d-8548-9e2bba4df915)
 Call ID: 386e686a-bc4c-411d-8548-9e2bba4df915
  Args:
    source: Edwina_of_Mecklenburg-Schwerin
    relation: :hasFather
    target: Christian_Louis_of_Mecklenburg-Schwerin
  AddTriple (2699b1f4-864b-494f-8420-45025b667635)
 Call ID: 2699b1f4-864b-494f-8420-45025b667635
  Args:
    source: Edwina_of_Mecklenburg-Schwerin
    target: Barbara_of_Prussia
    relation: :hasMother
  AssignClass (b8910a1c-17a6-42b8-96ad-ea94e0ef0377)
 Call ID: b8910a1c-17a6-42b8-96ad-ea94e0ef0377
  Args:
    source: Borwin_of_Mecklenburg
    type: :Man
  AssignClass (eda00f8c-44d6-4dd0-94d5-6c7ba6bb5925)
 Call ID: eda00f8c-44d6-4dd0-94d5-6c7ba6bb5925
  Args:
    type: :Person
    source: Borwin_of_Mecklenburg
  AssignClass (da389140-c50e-483b-942d-0eddfd8254f9)
 Call ID: da389140-c50e-483b-942d-0eddfd8254f9
  Args:
    type: :Man
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (719374c7-5fcf-4a88-be03-6c6dd8db55ac)
 Call ID: 719374c7-5fcf-4a88-be03-6c6dd8db55ac
  Args:
    type: :Person
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddTriple (31413e9e-3f4c-4866-a87b-897f45a6dd28)
 Call ID: 31413e9e-3f4c-4866-a87b-897f45a6dd28
  Args:
    relation: :hasFather
    target: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    source: Christian_Louis_of_Mecklenburg-Schwerin
  AssignClass (0e600096-089d-4702-a640-3bf33f23658d)
 Call ID: 0e600096-089d-4702-a640-3bf33f23658d
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (4529eff9-c3d3-4eba-afb1-f1559bd6e7fb)
 Call ID: 4529eff9-c3d3-4eba-afb1-f1559bd6e7fb
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AssignClass (7ef9b410-374f-418c-bd1e-2a262b5dde2a)
 Call ID: 7ef9b410-374f-418c-bd1e-2a262b5dde2a
  Args:
    type: :Woman
    source: Alexandra_of_Hanover_and_Cumberland
  AssignClass (e7fe50ea-e428-4774-af39-f79934783b85)
 Call ID: e7fe50ea-e428-4774-af39-f79934783b85
  Args:
    source: Alexandra_of_Hanover_and_Cumberland
    type: :Person
  AddTriple (50db8dd2-e86f-4b1d-b987-eb9ff50b944a)
 Call ID: 50db8dd2-e86f-4b1d-b987-eb9ff50b944a
  Args:
    source: Christian_Louis_of_Mecklenburg-Schwerin
    target: Alexandra_of_Hanover_and_Cumberland
    relation: :hasMother
  AssignClass (02323961-fc14-4ae0-aeb8-cd02031b85bf)
 Call ID: 02323961-fc14-4ae0-aeb8-cd02031b85bf
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (eff97f80-4e6f-4c3b-8abb-e39c1a99db77)
 Call ID: eff97f80-4e6f-4c3b-8abb-e39c1a99db77
  Args:
    source: Ernest_Augustus_of_Hanover
    type: :Person
  AssignClass (f7a278f6-5f7b-4a71-bd2e-266cff55d9d4)
 Call ID: f7a278f6-5f7b-4a71-bd2e-266cff55d9d4
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AssignClass (2d9b3b6f-ea0e-4c8e-ae2d-5c6d6ab0dc85)
 Call ID: 2d9b3b6f-ea0e-4c8e-ae2d-5c6d6ab0dc85
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddTriple (766c1ca5-3256-4b78-80b4-4c6302603612)
 Call ID: 766c1ca5-3256-4b78-80b4-4c6302603612
  Args:
    relation: :hasFather
    target: Ernest_Augustus_of_Hanover
    source: Alexandra_of_Hanover_and_Cumberland
  AddTriple (6b73dd99-ad6c-4ef7-badb-f14f5382cb5c)
 Call ID: 6b73dd99-ad6c-4ef7-badb-f14f5382cb5c
  Args:
    target: Thyra_of_Denmark
    relation: :hasMother
    source: Alexandra_of_Hanover_and_Cumberland
  AddTriple (2dc4a5ab-7fa9-44dd-918e-27e48a437ade)
 Call ID: 2dc4a5ab-7fa9-44dd-918e-27e48a437ade
  Args:
    relation: :hasFather
    target: Christian_IX_of_Denmark
    source: Thyra_of_Denmark
  AssignClass (727e13c5-f6f6-4904-9f1d-2b5647d67a5f)
 Call ID: 727e13c5-f6f6-4904-9f1d-2b5647d67a5f
  Args:
    source: Louise_of_Hesse-Kassel
    type: :Woman
  AssignClass (9d7e92fe-9ad3-48f7-ba5d-8b2c5d1df47d)
 Call ID: 9d7e92fe-9ad3-48f7-ba5d-8b2c5d1df47d
  Args:
    source: Louise_of_Hesse-Kassel
    type: :Person
  AddTriple (f5fc11a5-0dc4-42af-a89d-11a468ec8bde)
 Call ID: f5fc11a5-0dc4-42af-a89d-11a468ec8bde
  Args:
    target: Louise_of_Hesse-Kassel
    relation: :hasMother
    source: Thyra_of_Denmark
  AssignClass (a0c674f3-c141-408e-a325-a3c771a1606c)
 Call ID: a0c674f3-c141-408e-a325-a3c771a1606c
  Args:
    source: Sigismund_of_Prussia
    type: :Man
  AssignClass (8380b1a2-3798-4c2b-b30f-286099f53241)
 Call ID: 8380b1a2-3798-4c2b-b30f-286099f53241
  Args:
    type: :Person
    source: Sigismund_of_Prussia
  AddTriple (69a50e25-8548-46bd-98c4-d78fb9e78d16)
 Call ID: 69a50e25-8548-46bd-98c4-d78fb9e78d16
  Args:
    target: Sigismund_of_Prussia
    relation: :hasFather
    source: Barbara_of_Prussia
  AssignClass (15e4cd6a-0dc5-43be-aae9-5964692ba088)
 Call ID: 15e4cd6a-0dc5-43be-aae9-5964692ba088
  Args:
    source: Louis_IV_of_Hesse
    type: :Man
  AssignClass (4d6a03a3-cd21-4288-8c1c-5f5ab5934459)
 Call ID: 4d6a03a3-cd21-4288-8c1c-5f5ab5934459
  Args:
    source: Louis_IV_of_Hesse
    type: :Person
  AssignClass (d7780da2-bed1-4cec-b5f1-3a7aef386b9f)
 Call ID: d7780da2-bed1-4cec-b5f1-3a7aef386b9f
  Args:
    source: Alice_of_the_United_Kingdom
    type: :Woman
  AssignClass (ac832268-0ebf-4d72-a414-32e580c39fda)
 Call ID: ac832268-0ebf-4d72-a414-32e580c39fda
  Args:
    source: Alice_of_the_United_Kingdom
    type: :Person
  AssignClass (619dafa7-043b-4aed-8cea-bef5bc89e266)
 Call ID: 619dafa7-043b-4aed-8cea-bef5bc89e266
  Args:
    source: Queen_Victoria
    type: :Woman
  AssignClass (9a4bcb68-354b-453b-9d67-141c5f76a74d)
 Call ID: 9a4bcb68-354b-453b-9d67-141c5f76a74d
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (4d0e5f07-878d-430d-a158-f5c256e9e108)
 Call ID: 4d0e5f07-878d-430d-a158-f5c256e9e108
  Args:
    target: Queen_Victoria
    relation: :hasMother
    source: Alice_of_the_United_Kingdom
  Finish (4a929def-c407-44ad-8c23-f331391ccffe)
 Call ID: 4a929def-c407-44ad-8c23-f331391ccffe
  Args: