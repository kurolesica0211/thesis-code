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
  AssignClass (ad313fd6-e7c5-489c-b406-2567b85952b5)
 Call ID: ad313fd6-e7c5-489c-b406-2567b85952b5
  Args:
    type: :Woman
    source: Donata_of_Mecklenburg
  AddLiteral (3ab7b8b4-df8c-4c9c-bedf-206b81e7b3d4)
 Call ID: 3ab7b8b4-df8c-4c9c-bedf-206b81e7b3d4
  Args:
    literal_value: 1956
    relation: :hasBirthYear
    source: Donata_of_Mecklenburg
    literal_type: xsd:integer
  AssignClass (7c66c731-d14e-41c9-a0fd-6a2c248d5805)
 Call ID: 7c66c731-d14e-41c9-a0fd-6a2c248d5805
  Args:
    source: Christian_Louis_of_Mecklenburg-Schwerin
    type: :Man
  AssignClass (d2f4999f-1832-41a0-9d2c-85cdace07bb4)
 Call ID: d2f4999f-1832-41a0-9d2c-85cdace07bb4
  Args:
    type: :Woman
    source: Barbara_of_Prussia
  AddLiteral (c728a686-0383-4877-bddf-18c6c3723c10)
 Call ID: c728a686-0383-4877-bddf-18c6c3723c10
  Args:
    relation: :hasBirthYear
    literal_value: 1920
    literal_type: xsd:integer
    source: Barbara_of_Prussia
  AddLiteral (f8d76dcc-2190-47f6-9393-b15c128f3177)
 Call ID: f8d76dcc-2190-47f6-9393-b15c128f3177
  Args:
    literal_value: 1994
    relation: :hasDeathYear
    source: Barbara_of_Prussia
    literal_type: xsd:integer
  AddTriple (75cbba7f-d056-47d7-8533-e507a4456819)
 Call ID: 75cbba7f-d056-47d7-8533-e507a4456819
  Args:
    source: Donata_of_Mecklenburg
    relation: :hasFather
    target: Christian_Louis_of_Mecklenburg-Schwerin
  AddTriple (5362417f-38a0-48eb-93c3-21406df7311b)
 Call ID: 5362417f-38a0-48eb-93c3-21406df7311b
  Args:
    target: Barbara_of_Prussia
    relation: :hasMother
    source: Donata_of_Mecklenburg
  AssignClass (6867454b-881a-4846-a00b-f14b9180aa8d)
 Call ID: 6867454b-881a-4846-a00b-f14b9180aa8d
  Args:
    source: Friedrich_Franz_of_Mecklenburg-Schwerin
    type: :Man
  AddTriple (e166c9dc-bf85-4344-89ac-bc1b8db86aec)
 Call ID: e166c9dc-bf85-4344-89ac-bc1b8db86aec
  Args:
    relation: :isBrotherOf
    target: Friedrich_Franz_of_Mecklenburg-Schwerin
    source: Christian_Louis_of_Mecklenburg-Schwerin
  AssignClass (c8232521-77bc-42a5-80e4-bf4c1ee474fc)
 Call ID: c8232521-77bc-42a5-80e4-bf4c1ee474fc
  Args:
    source: Edwina_of_Mecklenburg
    type: :Woman
  AddLiteral (3bdd4db9-4515-456c-a1c6-776be70827c3)
 Call ID: 3bdd4db9-4515-456c-a1c6-776be70827c3
  Args:
    literal_value: 1960
    relation: :hasBirthYear
    source: Edwina_of_Mecklenburg
    literal_type: xsd:integer
  AddTriple (862a84b1-cf13-4fad-b445-70084793344e)
 Call ID: 862a84b1-cf13-4fad-b445-70084793344e
  Args:
    target: Donata_of_Mecklenburg
    relation: :isSisterOf
    source: Edwina_of_Mecklenburg
  AddTriple (dc040918-9446-4e2c-bb10-36457bcea40d)
 Call ID: dc040918-9446-4e2c-bb10-36457bcea40d
  Args:
    source: Edwina_of_Mecklenburg
    target: Christian_Louis_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (e3663ebf-267d-4c56-a773-b99208953ecc)
 Call ID: e3663ebf-267d-4c56-a773-b99208953ecc
  Args:
    source: Edwina_of_Mecklenburg
    target: Barbara_of_Prussia
    relation: :hasMother
  AddLiteral (cc3105df-922d-481e-ad82-6cc13d533714)
 Call ID: cc3105df-922d-481e-ad82-6cc13d533714
  Args:
    source: Friedrich_Franz_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2001
  AssignClass (40c5b1bd-93af-43ad-b2cc-f20d50d76fac)
 Call ID: 40c5b1bd-93af-43ad-b2cc-f20d50d76fac
  Args:
    type: :Woman
    source: Charlotte_of_Saxe-Altenburg
  AddTriple (616771bc-27c7-4ba4-9b4d-eaa28fe43ebe)
 Call ID: 616771bc-27c7-4ba4-9b4d-eaa28fe43ebe
  Args:
    source: Charlotte_of_Saxe-Altenburg
    target: Barbara_of_Prussia
    relation: :isMotherOf
  AssignClass (f1b26937-71e1-4323-a738-97f6ce982f5a)
 Call ID: f1b26937-71e1-4323-a738-97f6ce982f5a
  Args:
    type: :Man
    source: Ernst_II_of_Saxe-Altenburg
  AddTriple (f41fd8e6-1bd0-4e8d-97ae-61bebf9346d4)
 Call ID: f41fd8e6-1bd0-4e8d-97ae-61bebf9346d4
  Args:
    relation: :isFatherOf
    target: Charlotte_of_Saxe-Altenburg
    source: Ernst_II_of_Saxe-Altenburg
  AssignClass (952e4741-be30-46cf-9ada-73098fc3891c)
 Call ID: 952e4741-be30-46cf-9ada-73098fc3891c
  Args:
    type: :Man
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AddTriple (630deb81-675e-49f6-88a7-24df63c811e1)
 Call ID: 630deb81-675e-49f6-88a7-24df63c811e1
  Args:
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
    relation: :isFatherOf
    target: Christian_Louis_of_Mecklenburg-Schwerin
  AddTriple (527cc7c0-74b9-47cc-89f4-3dc87f794820)
 Call ID: 527cc7c0-74b9-47cc-89f4-3dc87f794820
  Args:
    target: Friedrich_Franz_of_Mecklenburg-Schwerin
    relation: :isFatherOf
    source: Frederick_Francis_IV_of_Mecklenburg-Schwerin
  AssignClass (84970364-6f58-446c-9652-8fe225a09ec7)
 Call ID: 84970364-6f58-446c-9652-8fe225a09ec7
  Args:
    source: Borwin_of_Mecklenburg
    type: :Man
  AssignClass (23052e82-a4e8-460c-b9b5-e3e9b50e3b3c)
 Call ID: 23052e82-a4e8-460c-b9b5-e3e9b50e3b3c
  Args:
    source: Christian_IX_of_Denmark
    type: :Man
  AssignClass (55187eef-531b-489e-8f9c-c3736cbf4c89)
 Call ID: 55187eef-531b-489e-8f9c-c3736cbf4c89
  Args:
    source: Alexandra_of_Hanover_and_Cumberland
    type: :Woman
  AddTriple (9b0fedfe-9993-485a-9252-24fc58ba5670)
 Call ID: 9b0fedfe-9993-485a-9252-24fc58ba5670
  Args:
    source: Alexandra_of_Hanover_and_Cumberland
    target: Christian_Louis_of_Mecklenburg-Schwerin
    relation: :isMotherOf
  AddTriple (656d7d74-92f6-4b77-b10a-36ee1f6e8fec)
 Call ID: 656d7d74-92f6-4b77-b10a-36ee1f6e8fec
  Args:
    source: Alexandra_of_Hanover_and_Cumberland
    relation: :isMotherOf
    target: Friedrich_Franz_of_Mecklenburg-Schwerin
  AssignClass (6e7dca6d-b8e4-4fd4-ac6c-463173fdcbf9)
 Call ID: 6e7dca6d-b8e4-4fd4-ac6c-463173fdcbf9
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (7e359327-71fe-4bee-9fb3-cc70d4b8eb33)
 Call ID: 7e359327-71fe-4bee-9fb3-cc70d4b8eb33
  Args:
    source: Thyra_of_Denmark
    type: :Woman
  AddTriple (253b5a1d-be7d-496c-900b-6c18bbfa170b)
 Call ID: 253b5a1d-be7d-496c-900b-6c18bbfa170b
  Args:
    source: Ernest_Augustus_of_Hanover
    relation: :isFatherOf
    target: Alexandra_of_Hanover_and_Cumberland
  AddTriple (706ec3e2-cd91-49fb-9e2a-52691e437226)
 Call ID: 706ec3e2-cd91-49fb-9e2a-52691e437226
  Args:
    source: Thyra_of_Denmark
    relation: :isMotherOf
    target: Alexandra_of_Hanover_and_Cumberland
  AddTriple (47894221-cf16-4552-84a2-cf04b6e84573)
 Call ID: 47894221-cf16-4552-84a2-cf04b6e84573
  Args:
    source: Christian_IX_of_Denmark
    relation: :isFatherOf
    target: Thyra_of_Denmark
  AssignClass (7dd061a1-8c29-43d0-ac16-9f9ade5b0542)
 Call ID: 7dd061a1-8c29-43d0-ac16-9f9ade5b0542
  Args:
    source: Louise_of_Hesse-Kassel
    type: :Woman
  AddTriple (b710f1a6-777f-4e35-9726-05fa92653f0f)
 Call ID: b710f1a6-777f-4e35-9726-05fa92653f0f
  Args:
    target: Thyra_of_Denmark
    relation: :isMotherOf
    source: Louise_of_Hesse-Kassel
  AssignClass (3826afea-2fd9-43a8-9830-518540b9e7b7)
 Call ID: 3826afea-2fd9-43a8-9830-518540b9e7b7
  Args:
    source: Sigismund_of_Prussia
    type: :Man
  AddTriple (0dc367a7-0e4a-4ccd-8e5b-5c4ded547b2e)
 Call ID: 0dc367a7-0e4a-4ccd-8e5b-5c4ded547b2e
  Args:
    source: Sigismund_of_Prussia
    relation: :isFatherOf
    target: Barbara_of_Prussia
  AssignClass (046f1f0b-967d-4b48-8f2f-eb4f8e0764c1)
 Call ID: 046f1f0b-967d-4b48-8f2f-eb4f8e0764c1
  Args:
    type: :Man
    source: Louis_IV_of_Hesse
  AssignClass (c34bbe60-d784-4d3b-9656-53c0a4e7f6d6)
 Call ID: c34bbe60-d784-4d3b-9656-53c0a4e7f6d6
  Args:
    type: :Woman
    source: Alice_of_Hesse
  AddTriple (19d4bb8b-45d2-4106-a9cd-2ff05854f47d)
 Call ID: 19d4bb8b-45d2-4106-a9cd-2ff05854f47d
  Args:
    source: Louis_IV_of_Hesse
    target: Sigismund_of_Prussia
    relation: :isFatherOf
  AddTriple (4b9d849b-e4bb-4aa2-97c2-68c0c3e22279)
 Call ID: 4b9d849b-e4bb-4aa2-97c2-68c0c3e22279
  Args:
    target: Sigismund_of_Prussia
    relation: :isMotherOf
    source: Alice_of_Hesse
  AssignClass (8f83ddb6-ae79-4dcc-88a6-8559408b4805)
 Call ID: 8f83ddb6-ae79-4dcc-88a6-8559408b4805
  Args:
    source: Queen_Victoria
    type: :Woman
  AddTriple (5366cc5a-0ade-4878-a966-7d0109cbb93f)
 Call ID: 5366cc5a-0ade-4878-a966-7d0109cbb93f
  Args:
    source: Queen_Victoria
    relation: :isMotherOf
    target: Alice_of_Hesse
  Finish (67e1ad47-d4d6-4e7e-8bfc-b5504f8ab8d5)
 Call ID: 67e1ad47-d4d6-4e7e-8bfc-b5504f8ab8d5
  Args: