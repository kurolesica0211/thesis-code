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
Hilmar Freiherr von dem Bussche-Haddenhausen (31 January 1867 – 19 November 1939) was a German nobleman and a diplomat.
Early life

Hilmar was born in Hanover on 31 January 1867, and belonged to the ancient von dem Bussche noble family which originated from the County of Ravensberg.
He was a son of the deputy chief stable master Julius von dem Bussche-Haddenhausen (1827–1882) and his wife Mathilde von Salviati (1833–1892).
His younger brother, George von dem Bussche-Haddenhausen, was the mother of Baroness Gösta von dem Bussche-Haddenhausen (herself the mother of Prince Claus of the Netherlands, consort of Queen Beatrix of the Netherlands).
Career

In 1894, Bussche-Haddenhausen was appointed to the Foreign Office and began his diplomatic career.
In May 1896, Bussche-Haddenhausen was appointed legation councilor before he was recalled from Tangier in November.
Bussche-Haddenhausen's served in Washington until May 1906, when he returned to the Foreign Office in Berlin in the Politics Department working, primarily, as a department head for English affairs.
He served in that role for four years, until his mission ended shortly before the outbreak of World War I.


Bussche-Haddenhausen took over as acting head of the German embassy in Bucharest on 18 September 1914, again succeeding Julius von Waldthausen, who retired.
In December 1915, Bussche-Haddenhausen was appointed Envoy but had to return to Germany at short notice in the summer of 1916 because of the unexpected break in diplomatic relations with Romania.
In the beginning of the Weimar Republic, Bussche-Haddenhausen withdrew from public life.
Personal life

On 15 August 1899 in Buenos Aires, Bussche-Haddenhausen married María Eleonore Martínez de Hoz (1875–1957), the daughter of Argentinian landowner Narciso Martínez de Hoz, who was from one of the richest families in Argentina, and Mathilde Stegmann.
Together, they had five children, including:


Baron von dem Bussche-Haddenhausen died on 19 November 1939 in Ramos Mejía, Argentina.



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
  AssignClass (d68f38db-7f1b-4c53-9d7f-8f50d8b20625)
 Call ID: d68f38db-7f1b-4c53-9d7f-8f50d8b20625
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (50e4185e-d714-4a75-bb14-5ca27b02d7a1)
 Call ID: 50e4185e-d714-4a75-bb14-5ca27b02d7a1
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (cdcc7961-12d6-4f75-8c3f-4079b9781ff0)
 Call ID: cdcc7961-12d6-4f75-8c3f-4079b9781ff0
  Args:
    literal_type: xsd:integer
    literal_value: 1867
    relation: :hasBirthYear
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddLiteral (27bf0b25-c933-4e82-9a7c-7a672df65c67)
 Call ID: 27bf0b25-c933-4e82-9a7c-7a672df65c67
  Args:
    literal_type: xsd:integer
    literal_value: 1939
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
  AssignClass (d5a1d203-09da-493e-ad1d-9faad7109185)
 Call ID: d5a1d203-09da-493e-ad1d-9faad7109185
  Args:
    type: :Man
    source: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (a1a3c0d1-9afc-4fcc-90e6-3c1c0aa3d2e0)
 Call ID: a1a3c0d1-9afc-4fcc-90e6-3c1c0aa3d2e0
  Args:
    type: :Person
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (eb5a0108-1058-4910-b4d7-82f5dc77b788)
 Call ID: eb5a0108-1058-4910-b4d7-82f5dc77b788
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasBirthYear
    literal_value: 1827
    literal_type: xsd:integer
  AddLiteral (271cc9e2-29ee-4530-bf25-8e788f755fb3)
 Call ID: 271cc9e2-29ee-4530-bf25-8e788f755fb3
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Julius_von_dem_Bussche-Haddenhausen
    literal_value: 1882
  AssignClass (6cc11129-41be-4435-9939-20afbd715051)
 Call ID: 6cc11129-41be-4435-9939-20afbd715051
  Args:
    source: Mathilde_von_Salviati
    type: :Woman
  AssignClass (2dbdd261-2871-49b2-a042-4d15c8d3bf3f)
 Call ID: 2dbdd261-2871-49b2-a042-4d15c8d3bf3f
  Args:
    type: :Person
    source: Mathilde_von_Salviati
  AddLiteral (cc6a6c79-2af6-4e69-be26-bc17c61aab48)
 Call ID: cc6a6c79-2af6-4e69-be26-bc17c61aab48
  Args:
    source: Mathilde_von_Salviati
    relation: :hasBirthYear
    literal_value: 1833
    literal_type: xsd:integer
  AddLiteral (79fd44e1-60f8-4d37-b188-d849b7923adb)
 Call ID: 79fd44e1-60f8-4d37-b188-d849b7923adb
  Args:
    literal_value: 1892
    source: Mathilde_von_Salviati
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (82b7d369-9a9e-40b3-bc8b-3bb6df57673a)
 Call ID: 82b7d369-9a9e-40b3-bc8b-3bb6df57673a
  Args:
    target: Julius_von_dem_Bussche-Haddenhausen
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (05e6c251-33dc-405a-92fe-83d7242afdbd)
 Call ID: 05e6c251-33dc-405a-92fe-83d7242afdbd
  Args:
    relation: :hasMother
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    target: Mathilde_von_Salviati
  AssignClass (8b583468-f5e8-48e4-a3ca-13b0eb626d04)
 Call ID: 8b583468-f5e8-48e4-a3ca-13b0eb626d04
  Args:
    type: :Man
    source: George_von_dem_Bussche-Haddenhausen
  AssignClass (828f9abf-e913-4d22-8ccd-b38651c2b452)
 Call ID: 828f9abf-e913-4d22-8ccd-b38651c2b452
  Args:
    type: :Person
    source: George_von_dem_Bussche-Haddenhausen
  AddTriple (e6d36d87-e3c0-45b0-93e6-6b813aa811bd)
 Call ID: e6d36d87-e3c0-45b0-93e6-6b813aa811bd
  Args:
    target: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    source: George_von_dem_Bussche-Haddenhausen
    relation: :isBrotherOf
  AssignClass (93dc0ef6-8a9b-47b6-9fef-73baf8279f1f)
 Call ID: 93dc0ef6-8a9b-47b6-9fef-73baf8279f1f
  Args:
    type: :Woman
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (c02f4673-42c0-43f2-9272-3e3dfb529e2c)
 Call ID: c02f4673-42c0-43f2-9272-3e3dfb529e2c
  Args:
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    type: :Person
  AddTriple (57f19bce-b786-4611-bcc3-656c531e90dd)
 Call ID: 57f19bce-b786-4611-bcc3-656c531e90dd
  Args:
    target: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    source: George_von_dem_Bussche-Haddenhausen
    relation: :isMotherOf
  AssignClass (9cb45d58-1d7a-4282-a105-5af7fef11689)
 Call ID: 9cb45d58-1d7a-4282-a105-5af7fef11689
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (df5035af-e1c1-42a6-b5eb-b5b1e2cc9ec7)
 Call ID: df5035af-e1c1-42a6-b5eb-b5b1e2cc9ec7
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Person
  AddTriple (c89f6463-8aad-42b0-8847-1621eae2adaa)
 Call ID: c89f6463-8aad-42b0-8847-1621eae2adaa
  Args:
    target: Prince_Claus_of_the_Netherlands
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    relation: :isMotherOf
  AssignClass (9f5fe2c2-b362-4dc6-a4ee-0b352b03e08f)
 Call ID: 9f5fe2c2-b362-4dc6-a4ee-0b352b03e08f
  Args:
    type: :Woman
    source: María_Eleonore_Martínez_de_Hoz
  AssignClass (0bdde593-2110-4e01-b15d-050fbf226b53)
 Call ID: 0bdde593-2110-4e01-b15d-050fbf226b53
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    type: :Person
  AddLiteral (5ded7e2d-c961-406a-9af8-eca428805430)
 Call ID: 5ded7e2d-c961-406a-9af8-eca428805430
  Args:
    literal_value: 1875
    relation: :hasBirthYear
    source: María_Eleonore_Martínez_de_Hoz
    literal_type: xsd:integer
  AddLiteral (8a5d57e7-cc25-46c2-9923-010ec32491a2)
 Call ID: 8a5d57e7-cc25-46c2-9923-010ec32491a2
  Args:
    literal_type: xsd:integer
    literal_value: 1957
    relation: :hasDeathYear
    source: María_Eleonore_Martínez_de_Hoz
  AddLiteral (cfbe8c3a-b4c1-42bd-9b41-ca83d46f6059)
 Call ID: cfbe8c3a-b4c1-42bd-9b41-ca83d46f6059
  Args:
    relation: :hasMarriageYear
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_value: 1899
    literal_type: xsd:integer
  AddTriple (ba33da83-3366-49c6-aa30-6e4192b3b658)
 Call ID: ba33da83-3366-49c6-aa30-6e4192b3b658
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
    target: María_Eleonore_Martínez_de_Hoz
  AssignClass (aa6b19f5-73e3-47fd-9cb0-604bb3314275)
 Call ID: aa6b19f5-73e3-47fd-9cb0-604bb3314275
  Args:
    type: :Man
    source: Narciso_Martínez_de_Hoz
  AssignClass (5373cf19-21c8-47da-ac84-0b8a6f7b3735)
 Call ID: 5373cf19-21c8-47da-ac84-0b8a6f7b3735
  Args:
    source: Narciso_Martínez_de_Hoz
    type: :Person
  AssignClass (8e506656-8061-416e-85ef-1d4cad3a2483)
 Call ID: 8e506656-8061-416e-85ef-1d4cad3a2483
  Args:
    type: :Woman
    source: Mathilde_Stegmann
  AssignClass (aa2a4d97-0ae5-4a0f-ab78-618126e53e34)
 Call ID: aa2a4d97-0ae5-4a0f-ab78-618126e53e34
  Args:
    source: Mathilde_Stegmann
    type: :Person
  AddTriple (1db5a5ae-19ac-46f3-93c1-093469a43c9a)
 Call ID: 1db5a5ae-19ac-46f3-93c1-093469a43c9a
  Args:
    target: Narciso_Martínez_de_Hoz
    source: María_Eleonore_Martínez_de_Hoz
    relation: :hasFather
  AddTriple (ac9e7a7c-2c1c-49d5-9159-38df2a063506)
 Call ID: ac9e7a7c-2c1c-49d5-9159-38df2a063506
  Args:
    target: Mathilde_Stegmann
    relation: :hasMother
    source: María_Eleonore_Martínez_de_Hoz
  Finish (fcb84704-ced9-4d10-be97-a8b006041478)
 Call ID: fcb84704-ced9-4d10-be97-a8b006041478
  Args: