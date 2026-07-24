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
  AssignClass (259c1028-8fcb-4997-9a4d-0536794afa5b)
 Call ID: 259c1028-8fcb-4997-9a4d-0536794afa5b
  Args:
    type: :Woman
    source: :Donata_of_Mecklenburg
  AssignClass (c7142cec-efe9-400c-a717-76a1b9980ff4)
 Call ID: c7142cec-efe9-400c-a717-76a1b9980ff4
  Args:
    type: :Person
    source: :Donata_of_Mecklenburg
  AddLiteral (83d1b5c7-5095-482a-8143-f5ae26a77f5b)
 Call ID: 83d1b5c7-5095-482a-8143-f5ae26a77f5b
  Args:
    literal_value: 1956
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Donata_of_Mecklenburg
  AssignClass (4cc60f55-13c2-479a-bef8-9a7c3213c2ba)
 Call ID: 4cc60f55-13c2-479a-bef8-9a7c3213c2ba
  Args:
    type: :Man
    source: :Christian_Louis_of_Mecklenburg_Schwerin
  AssignClass (b57f4663-4eee-4196-b3c3-a7f430871926)
 Call ID: b57f4663-4eee-4196-b3c3-a7f430871926
  Args:
    type: :Person
    source: :Christian_Louis_of_Mecklenburg_Schwerin
  AssignClass (99592800-9b27-4836-95d1-918177ae1826)
 Call ID: 99592800-9b27-4836-95d1-918177ae1826
  Args:
    type: :Woman
    source: :Barbara_of_Prussia
  AssignClass (169b69d3-7815-4786-83df-0e8d3be2e59b)
 Call ID: 169b69d3-7815-4786-83df-0e8d3be2e59b
  Args:
    type: :Person
    source: :Barbara_of_Prussia
  AddLiteral (6fbafd4c-612a-4691-9024-e4fe480014b3)
 Call ID: 6fbafd4c-612a-4691-9024-e4fe480014b3
  Args:
    source: :Barbara_of_Prussia
    relation: :hasBirthYear
    literal_value: 1920
    literal_type: xsd:integer
  AddLiteral (d10a2779-b9b0-4ebe-886c-0a62fbd76a04)
 Call ID: d10a2779-b9b0-4ebe-886c-0a62fbd76a04
  Args:
    source: :Barbara_of_Prussia
    literal_type: xsd:integer
    literal_value: 1994
    relation: :hasDeathYear
  AddTriple (9ed61887-a45f-46e0-bba4-85d57fdff776)
 Call ID: 9ed61887-a45f-46e0-bba4-85d57fdff776
  Args:
    relation: :hasFather
    target: :Christian_Louis_of_Mecklenburg_Schwerin
    source: :Donata_of_Mecklenburg
  AddTriple (9642974b-81ca-41e9-8406-9fa5caa2037d)
 Call ID: 9642974b-81ca-41e9-8406-9fa5caa2037d
  Args:
    relation: :hasMother
    source: :Donata_of_Mecklenburg
    target: :Barbara_of_Prussia
  AssignClass (7b1aa8f7-1571-4b8a-b0d8-363e2ade9146)
 Call ID: 7b1aa8f7-1571-4b8a-b0d8-363e2ade9146
  Args:
    type: :Man
    source: :Friedrich_Franz_of_Mecklenburg_Schwerin
  AssignClass (20ba640d-96d4-4c3e-a813-e7f690146c6d)
 Call ID: 20ba640d-96d4-4c3e-a813-e7f690146c6d
  Args:
    type: :Person
    source: :Friedrich_Franz_of_Mecklenburg_Schwerin
  AddTriple (d1851a0d-add5-4559-bdfc-c1a260efd0b6)
 Call ID: d1851a0d-add5-4559-bdfc-c1a260efd0b6
  Args:
    source: :Christian_Louis_of_Mecklenburg_Schwerin
    target: :Friedrich_Franz_of_Mecklenburg_Schwerin
    relation: :isBrotherOf
  AssignClass (73e8890a-f000-4ee2-98f1-8bc76e9b7f08)
 Call ID: 73e8890a-f000-4ee2-98f1-8bc76e9b7f08
  Args:
    type: :Woman
    source: :Charlotte_of_Saxe_Altenburg
  AssignClass (c2249b64-77bb-479b-968d-e52723a0c505)
 Call ID: c2249b64-77bb-479b-968d-e52723a0c505
  Args:
    type: :Person
    source: :Charlotte_of_Saxe_Altenburg
  AddTriple (b156db3f-047f-4c86-b64b-a14f57b0d619)
 Call ID: b156db3f-047f-4c86-b64b-a14f57b0d619
  Args:
    source: :Charlotte_of_Saxe_Altenburg
    target: :Barbara_of_Prussia
    relation: :isMotherOf
  AssignClass (964c0878-9779-4585-a62c-4576d5f6490f)
 Call ID: 964c0878-9779-4585-a62c-4576d5f6490f
  Args:
    type: :Man
    source: :Ernst_II_of_Saxe_Altenburg
  AssignClass (6dc25b15-a74b-4c2c-a1bd-d89a2a11189c)
 Call ID: 6dc25b15-a74b-4c2c-a1bd-d89a2a11189c
  Args:
    type: :Person
    source: :Ernst_II_of_Saxe_Altenburg
  AddTriple (5b584e5e-b4a5-4390-8bea-8f85d3e3143b)
 Call ID: 5b584e5e-b4a5-4390-8bea-8f85d3e3143b
  Args:
    relation: :isFatherOf
    source: :Ernst_II_of_Saxe_Altenburg
    target: :Charlotte_of_Saxe_Altenburg
  AssignClass (50b7656e-e3a7-48e7-ab96-502b3cdca744)
 Call ID: 50b7656e-e3a7-48e7-ab96-502b3cdca744
  Args:
    type: :Woman
    source: :Edwina_of_Mecklenburg
  AssignClass (ebe7dde8-05bc-4fa8-8176-0329f42c1202)
 Call ID: ebe7dde8-05bc-4fa8-8176-0329f42c1202
  Args:
    type: :Person
    source: :Edwina_of_Mecklenburg
  AddLiteral (9f1d2d08-83ca-4129-a2b6-3c9ee6c9af9e)
 Call ID: 9f1d2d08-83ca-4129-a2b6-3c9ee6c9af9e
  Args:
    literal_value: 1960
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Edwina_of_Mecklenburg
  AddTriple (ff231084-a808-4eb8-81c0-1e8b86af512e)
 Call ID: ff231084-a808-4eb8-81c0-1e8b86af512e
  Args:
    relation: :isSisterOf
    target: :Donata_of_Mecklenburg
    source: :Edwina_of_Mecklenburg
  AssignClass (f3507f0b-f954-4949-8469-e6bf4db00793)
 Call ID: f3507f0b-f954-4949-8469-e6bf4db00793
  Args:
    type: :Man
    source: :Frederick_Francis_IV_of_Mecklenburg_Schwerin
  AssignClass (c6c47ef1-cae2-43a3-8ca5-a5c914f86164)
 Call ID: c6c47ef1-cae2-43a3-8ca5-a5c914f86164
  Args:
    type: :Person
    source: :Frederick_Francis_IV_of_Mecklenburg_Schwerin
  AddTriple (79b53158-3cc1-4ab1-af8e-b70659d3f74f)
 Call ID: 79b53158-3cc1-4ab1-af8e-b70659d3f74f
  Args:
    relation: :isFatherOf
    target: :Christian_Louis_of_Mecklenburg_Schwerin
    source: :Frederick_Francis_IV_of_Mecklenburg_Schwerin
  AssignClass (cc259825-dc5e-492a-a5d0-b4ddbc328d40)
 Call ID: cc259825-dc5e-492a-a5d0-b4ddbc328d40
  Args:
    type: :Woman
    source: :Alexandra_of_Hanover_and_Cumberland
  AssignClass (082fd194-c81b-4ed8-9355-16bd9eacf3f2)
 Call ID: 082fd194-c81b-4ed8-9355-16bd9eacf3f2
  Args:
    type: :Person
    source: :Alexandra_of_Hanover_and_Cumberland
  AddTriple (114c0be6-407e-4a35-8f08-290028e87e0a)
 Call ID: 114c0be6-407e-4a35-8f08-290028e87e0a
  Args:
    source: :Alexandra_of_Hanover_and_Cumberland
    target: :Christian_Louis_of_Mecklenburg_Schwerin
    relation: :isMotherOf
  AddTriple (7eff8143-b4ea-4151-b415-76c2e1a2b6de)
 Call ID: 7eff8143-b4ea-4151-b415-76c2e1a2b6de
  Args:
    relation: :isFatherOf
    target: :Christian_Louis_of_Mecklenburg_Schwerin
    source: :Frederick_Francis_IV_of_Mecklenburg_Schwerin
  AssignClass (341b4331-2073-4ed0-aab5-bb982eb189fb)
 Call ID: 341b4331-2073-4ed0-aab5-bb982eb189fb
  Args:
    type: :Man
    source: :Ernest_Augustus_of_Hanover
  AssignClass (ac590d8e-d090-43e6-aba9-776a93c8eed1)
 Call ID: ac590d8e-d090-43e6-aba9-776a93c8eed1
  Args:
    type: :Person
    source: :Ernest_Augustus_of_Hanover
  AssignClass (7df7c158-9bd8-4cbe-8454-b90cc628c13f)
 Call ID: 7df7c158-9bd8-4cbe-8454-b90cc628c13f
  Args:
    type: :Woman
    source: :Thyra_of_Denmark
  AssignClass (41a8a4c8-f83d-4a9d-b0e7-29a696ded355)
 Call ID: 41a8a4c8-f83d-4a9d-b0e7-29a696ded355
  Args:
    type: :Person
    source: :Thyra_of_Denmark
  AddTriple (d246d1c9-a350-4789-9fa1-0924d4506ec3)
 Call ID: d246d1c9-a350-4789-9fa1-0924d4506ec3
  Args:
    relation: :isFatherOf
    source: :Ernest_Augustus_of_Hanover
    target: :Alexandra_of_Hanover_and_Cumberland
  AddTriple (b186d848-eebc-495e-a1bb-3d68b9d815e8)
 Call ID: b186d848-eebc-495e-a1bb-3d68b9d815e8
  Args:
    relation: :isMotherOf
    source: :Thyra_of_Denmark
    target: :Alexandra_of_Hanover_and_Cumberland
  AssignClass (6f17e34f-7860-4217-973d-7a5c62d6cab7)
 Call ID: 6f17e34f-7860-4217-973d-7a5c62d6cab7
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (4e9c87b6-4274-4c02-9613-b5ae8c13ff83)
 Call ID: 4e9c87b6-4274-4c02-9613-b5ae8c13ff83
  Args:
    type: :Person
    source: :Christian_IX_of_Denmark
  AssignClass (ac768749-8bc1-4508-a1db-a3f45705bdc6)
 Call ID: ac768749-8bc1-4508-a1db-a3f45705bdc6
  Args:
    type: :Woman
    source: :Louise_of_Hesse_Kassel
  AssignClass (128a78da-7d42-45ae-b290-e1df96f38599)
 Call ID: 128a78da-7d42-45ae-b290-e1df96f38599
  Args:
    type: :Person
    source: :Louise_of_Hesse_Kassel
  AddTriple (2b00c10a-4719-4dce-9aca-498931324438)
 Call ID: 2b00c10a-4719-4dce-9aca-498931324438
  Args:
    target: :Thyra_of_Denmark
    source: :Christian_IX_of_Denmark
    relation: :isFatherOf
  AddTriple (84afb1a5-ac76-4283-a32a-ad3a7666db33)
 Call ID: 84afb1a5-ac76-4283-a32a-ad3a7666db33
  Args:
    relation: :isMotherOf
    source: :Louise_of_Hesse_Kassel
    target: :Thyra_of_Denmark
  AssignClass (85d5ef64-47ed-43af-9f48-a2f5392590b3)
 Call ID: 85d5ef64-47ed-43af-9f48-a2f5392590b3
  Args:
    type: :Man
    source: :Sigismund_of_Prussia
  AssignClass (8c3cd057-6904-4052-9f0d-ef847a243c91)
 Call ID: 8c3cd057-6904-4052-9f0d-ef847a243c91
  Args:
    type: :Person
    source: :Sigismund_of_Prussia
  AddTriple (045823b2-aef4-40a9-ae86-4b4dc9e49987)
 Call ID: 045823b2-aef4-40a9-ae86-4b4dc9e49987
  Args:
    target: :Barbara_of_Prussia
    source: :Sigismund_of_Prussia
    relation: :isFatherOf
  AssignClass (ea22c623-2059-48f8-8cf4-785b19a5d583)
 Call ID: ea22c623-2059-48f8-8cf4-785b19a5d583
  Args:
    type: :Man
    source: :Louis_IV_of_Hesse
  AssignClass (59289259-9349-42ad-8cbf-39ab1fe8f240)
 Call ID: 59289259-9349-42ad-8cbf-39ab1fe8f240
  Args:
    type: :Person
    source: :Louis_IV_of_Hesse
  AssignClass (b3fef3c6-e106-40b9-8e73-927ea9c8766b)
 Call ID: b3fef3c6-e106-40b9-8e73-927ea9c8766b
  Args:
    type: :Woman
    source: :Alice_of_Hesse
  AssignClass (7a4c1288-49a6-4bc2-8e9c-822141b81cc2)
 Call ID: 7a4c1288-49a6-4bc2-8e9c-822141b81cc2
  Args:
    type: :Person
    source: :Alice_of_Hesse
  AddTriple (5d143bcf-3731-4296-9edb-5ccf290626f1)
 Call ID: 5d143bcf-3731-4296-9edb-5ccf290626f1
  Args:
    relation: :isFatherOf
    source: :Louis_IV_of_Hesse
    target: :Sigismund_of_Prussia
  AddTriple (e3a82a30-ba4e-4ebb-b3e1-b46fa6e1890e)
 Call ID: e3a82a30-ba4e-4ebb-b3e1-b46fa6e1890e
  Args:
    relation: :isMotherOf
    source: :Alice_of_Hesse
    target: :Sigismund_of_Prussia
  AssignClass (c5e899d4-30d9-4ba4-bf99-b031f85e1346)
 Call ID: c5e899d4-30d9-4ba4-bf99-b031f85e1346
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (6474ecd6-408a-47f0-a62e-196778d209e0)
 Call ID: 6474ecd6-408a-47f0-a62e-196778d209e0
  Args:
    type: :Person
    source: :Queen_Victoria
  AddTriple (250b73d3-b52a-49e8-9557-bcc342d6a4db)
 Call ID: 250b73d3-b52a-49e8-9557-bcc342d6a4db
  Args:
    source: :Queen_Victoria
    target: :Alice_of_Hesse
    relation: :isMotherOf
  Finish (1b55838a-9912-4182-9d87-363bd18397ca)
 Call ID: 1b55838a-9912-4182-9d87-363bd18397ca
  Args: