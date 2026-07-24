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
Duchess Marie Antoinette of Mecklenburg-Schwerin, also Manette (Marie Antoinette Margarethe Mathilde; 28 May 1884 – 26 October 1944) was the Duchess of Mecklenburg-Schwerin by birth and potential bride for King Alfonso XIII of Spain.
Early life

Marie Antoinette was born in Venice, into the House of Mecklenburg, as the third child and the second daughter of Duke Paul Frederick of Mecklenburg and Princess Marie of Windisch-Graetz.
Her brothers and sisters were Duke Paul Friedrich of Mecklenburg, Duchess Maria Luise of Mecklenburg-Schwerin (1883–1883), Duke Heinrich Borwin of Mecklenburg-Schwerin (1885–1942), and Duke Joseph of Mecklenburg-Schwerin (1889–1889).
She had a difficult relationship with her cousin Frederick Francis IV, Grand Duke of Mecklenburg-Schwerin, who regularly had to amortize her debts.
So, Marie Antoinette regularly had to sell archaeological artifacts belonging to her mother, excavated in Austria and Carniola, including Hallstatt Archaeological Site in Vače.
Potential bride for the King of Spain

She was German Kaiser Wilhelm II's candidate for a bride for King Alfonso XIII of Spain although he would marry the Kaiser's maternal first cousin, Princess Victoria Eugenie, niece of British King Edward VII.



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
  AssignClass (0b579704-639b-4527-b724-e580365d93a7)
 Call ID: 0b579704-639b-4527-b724-e580365d93a7
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    type: :Woman
  AssignClass (e543ab82-8bdc-4986-995d-cb20c45b453b)
 Call ID: e543ab82-8bdc-4986-995d-cb20c45b453b
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    type: :Person
  AddLiteral (07e5d354-8565-404c-9116-5a498f8bc4a4)
 Call ID: 07e5d354-8565-404c-9116-5a498f8bc4a4
  Args:
    relation: :alsoKnownAs
    literal_value: Manette
    literal_type: xsd:string
    source: :MarieAntoinetteOfMecklenburgSchwerin
  AddLiteral (91fedc2a-8af1-433f-a5ef-9aedc19850ad)
 Call ID: 91fedc2a-8af1-433f-a5ef-9aedc19850ad
  Args:
    literal_type: xsd:integer
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :hasBirthYear
    literal_value: 1884
  AddLiteral (18f28354-0324-43e6-b6d3-8d7f1d8f5abd)
 Call ID: 18f28354-0324-43e6-b6d3-8d7f1d8f5abd
  Args:
    literal_type: xsd:integer
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :hasDeathYear
    literal_value: 1944
  AssignClass (01074614-c1d0-42da-953e-606554bfdc03)
 Call ID: 01074614-c1d0-42da-953e-606554bfdc03
  Args:
    source: :DukePaulFrederickOfMecklenburg
    type: :Man
  AssignClass (e3853fbe-1301-4525-b168-4c07fe80bbf0)
 Call ID: e3853fbe-1301-4525-b168-4c07fe80bbf0
  Args:
    type: :Person
    source: :DukePaulFrederickOfMecklenburg
  AssignClass (76e0c2e9-a616-41fc-a9a2-27b63007c31b)
 Call ID: 76e0c2e9-a616-41fc-a9a2-27b63007c31b
  Args:
    source: :PrincessMarieOfWindischGraetz
    type: :Woman
  AssignClass (d59976e7-e576-40c9-bbd2-9d58d4a0c710)
 Call ID: d59976e7-e576-40c9-bbd2-9d58d4a0c710
  Args:
    source: :PrincessMarieOfWindischGraetz
    type: :Person
  AddTriple (721cee98-36dc-417a-aa5a-ffaa4f9c0e8e)
 Call ID: 721cee98-36dc-417a-aa5a-ffaa4f9c0e8e
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    target: :DukePaulFrederickOfMecklenburg
    relation: :hasFather
  AddTriple (a6b340d2-4466-4c80-b13a-5304f8a5e9b3)
 Call ID: a6b340d2-4466-4c80-b13a-5304f8a5e9b3
  Args:
    target: :PrincessMarieOfWindischGraetz
    relation: :hasMother
    source: :MarieAntoinetteOfMecklenburgSchwerin
  AssignClass (09249f12-f6e3-4f1b-ab89-1c52e502497e)
 Call ID: 09249f12-f6e3-4f1b-ab89-1c52e502497e
  Args:
    source: :DukePaulFriedrichOfMecklenburg
    type: :Man
  AssignClass (889c9e34-2d35-453d-9470-97941c516f77)
 Call ID: 889c9e34-2d35-453d-9470-97941c516f77
  Args:
    type: :Person
    source: :DukePaulFriedrichOfMecklenburg
  AssignClass (044e1956-920f-42c4-a714-92eb3423f2f3)
 Call ID: 044e1956-920f-42c4-a714-92eb3423f2f3
  Args:
    type: :Woman
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
  AssignClass (b0a9cbf6-230e-47f8-8ab8-17332972ae34)
 Call ID: b0a9cbf6-230e-47f8-8ab8-17332972ae34
  Args:
    type: :Person
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
  AssignClass (53213315-8746-4400-b3df-7c8a288fc141)
 Call ID: 53213315-8746-4400-b3df-7c8a288fc141
  Args:
    type: :Man
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
  AssignClass (da510074-238c-48a5-a7bc-6c63850610e1)
 Call ID: da510074-238c-48a5-a7bc-6c63850610e1
  Args:
    type: :Person
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
  AssignClass (6ef2ecc4-8774-46be-b335-d99250a717c1)
 Call ID: 6ef2ecc4-8774-46be-b335-d99250a717c1
  Args:
    type: :Man
    source: :DukeJosephOfMecklenburgSchwerin
  AssignClass (3251e3c8-6dc6-4846-b795-b4307e205a74)
 Call ID: 3251e3c8-6dc6-4846-b795-b4307e205a74
  Args:
    type: :Person
    source: :DukeJosephOfMecklenburgSchwerin
  AddTriple (6762da35-b181-4ac0-825e-690b704e4cf6)
 Call ID: 6762da35-b181-4ac0-825e-690b704e4cf6
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :isSiblingOf
    target: :DukePaulFriedrichOfMecklenburg
  AddTriple (2ad6dbd1-2166-4b40-b3c4-c0228fa61077)
 Call ID: 2ad6dbd1-2166-4b40-b3c4-c0228fa61077
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :isSiblingOf
    target: :DuchessMariaLuiseOfMecklenburgSchwerin
  AddTriple (597df9d2-6ef7-4751-84c8-519dd0d4f08d)
 Call ID: 597df9d2-6ef7-4751-84c8-519dd0d4f08d
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    relation: :isSiblingOf
    target: :DukeHeinrichBorwinOfMecklenburgSchwerin
  AddTriple (6745d734-2e8e-4cb8-80ae-fa6d9daa8c1a)
 Call ID: 6745d734-2e8e-4cb8-80ae-fa6d9daa8c1a
  Args:
    source: :MarieAntoinetteOfMecklenburgSchwerin
    target: :DukeJosephOfMecklenburgSchwerin
    relation: :isSiblingOf
  AddLiteral (f62736fa-879c-4af7-8d2c-74e4adbbf1d5)
 Call ID: f62736fa-879c-4af7-8d2c-74e4adbbf1d5
  Args:
    literal_type: xsd:integer
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
    relation: :hasBirthYear
    literal_value: 1883
  AddLiteral (0557ec74-6db2-4b23-aee8-180d479bc9e3)
 Call ID: 0557ec74-6db2-4b23-aee8-180d479bc9e3
  Args:
    source: :DuchessMariaLuiseOfMecklenburgSchwerin
    literal_type: xsd:integer
    literal_value: 1883
    relation: :hasDeathYear
  AddLiteral (044963c4-30b6-46fa-bff1-a98cff2bc73c)
 Call ID: 044963c4-30b6-46fa-bff1-a98cff2bc73c
  Args:
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1885
  AddLiteral (5b250422-97ab-427e-b9db-c41ffb499ec4)
 Call ID: 5b250422-97ab-427e-b9db-c41ffb499ec4
  Args:
    literal_type: xsd:integer
    source: :DukeHeinrichBorwinOfMecklenburgSchwerin
    literal_value: 1942
    relation: :hasDeathYear
  AddLiteral (452b4236-07d3-4d77-94aa-1d5831b2924c)
 Call ID: 452b4236-07d3-4d77-94aa-1d5831b2924c
  Args:
    relation: :hasBirthYear
    literal_value: 1889
    literal_type: xsd:integer
    source: :DukeJosephOfMecklenburgSchwerin
  AddLiteral (d67b2261-fa35-404e-8b7c-7e7e5162858e)
 Call ID: d67b2261-fa35-404e-8b7c-7e7e5162858e
  Args:
    source: :DukeJosephOfMecklenburgSchwerin
    literal_type: xsd:integer
    literal_value: 1889
    relation: :hasDeathYear
  Finish (13eaaab1-32e4-4e94-9cb6-3228bf4504da)
 Call ID: 13eaaab1-32e4-4e94-9cb6-3228bf4504da
  Args: