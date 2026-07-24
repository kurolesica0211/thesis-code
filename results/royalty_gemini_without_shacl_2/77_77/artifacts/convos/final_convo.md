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
  AssignClass (6e5a4ad7-f0e9-4923-b337-9da03ae6c7de)
 Call ID: 6e5a4ad7-f0e9-4923-b337-9da03ae6c7de
  Args:
    type: :Man
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AssignClass (99d2bcdd-e320-4f80-97a2-4e0283a2db4f)
 Call ID: 99d2bcdd-e320-4f80-97a2-4e0283a2db4f
  Args:
    type: :Person
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddLiteral (b739c467-8c06-49e8-a07b-9c63af07f75c)
 Call ID: b739c467-8c06-49e8-a07b-9c63af07f75c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_value: 1867
  AddLiteral (e70b8164-2a18-450e-a2bf-f09c442f15ec)
 Call ID: e70b8164-2a18-450e-a2bf-f09c442f15ec
  Args:
    relation: :hasDeathYear
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1939
  AssignClass (12e1183b-46ad-4e08-81b0-80b282485612)
 Call ID: 12e1183b-46ad-4e08-81b0-80b282485612
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (0e33976c-da7c-4746-a606-324a92f040cb)
 Call ID: 0e33976c-da7c-4746-a606-324a92f040cb
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (6d4ce17c-8951-4115-b86c-0369fbf9fe22)
 Call ID: 6d4ce17c-8951-4115-b86c-0369fbf9fe22
  Args:
    literal_value: 1827
    relation: :hasBirthYear
    source: Julius_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AddLiteral (aabd99f9-49ff-4cb3-a893-0272ec9cfd8e)
 Call ID: aabd99f9-49ff-4cb3-a893-0272ec9cfd8e
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Julius_von_dem_Bussche-Haddenhausen
    literal_value: 1882
  AssignClass (6ae74e96-77f1-4824-aa6a-d063ed8a5668)
 Call ID: 6ae74e96-77f1-4824-aa6a-d063ed8a5668
  Args:
    type: :Woman
    source: Mathilde_von_Salviati
  AssignClass (a89f81f8-0f07-4699-ba10-613529eafd99)
 Call ID: a89f81f8-0f07-4699-ba10-613529eafd99
  Args:
    source: Mathilde_von_Salviati
    type: :Person
  AddLiteral (0c42ff27-6124-4b41-a33b-ea46e12fc745)
 Call ID: 0c42ff27-6124-4b41-a33b-ea46e12fc745
  Args:
    source: Mathilde_von_Salviati
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1833
  AddLiteral (1384a1f0-591e-4378-817e-58bfca88e743)
 Call ID: 1384a1f0-591e-4378-817e-58bfca88e743
  Args:
    relation: :hasDeathYear
    source: Mathilde_von_Salviati
    literal_type: xsd:integer
    literal_value: 1892
  AddTriple (56070e11-e7ef-4be1-89cd-3b2c99bc5aa5)
 Call ID: 56070e11-e7ef-4be1-89cd-3b2c99bc5aa5
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    target: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (bc8e480f-f0d0-4906-8cd4-0b5bc921ee00)
 Call ID: bc8e480f-f0d0-4906-8cd4-0b5bc921ee00
  Args:
    target: Mathilde_von_Salviati
    relation: :hasMother
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AssignClass (63c4750a-b79a-4d72-bd63-8f113824ffa4)
 Call ID: 63c4750a-b79a-4d72-bd63-8f113824ffa4
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (fdd723ea-3eb1-41ab-b343-49dd3e99d51d)
 Call ID: fdd723ea-3eb1-41ab-b343-49dd3e99d51d
  Args:
    type: :Person
    source: George_von_dem_Bussche-Haddenhausen
  AddTriple (97e033c6-0537-46fb-a0e5-ef12d107d940)
 Call ID: 97e033c6-0537-46fb-a0e5-ef12d107d940
  Args:
    relation: :hasBrother
    target: George_von_dem_Bussche-Haddenhausen
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AssignClass (7ed31236-230c-4a06-963c-2c394d39aab2)
 Call ID: 7ed31236-230c-4a06-963c-2c394d39aab2
  Args:
    type: :Woman
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (ebf87192-f3d7-430f-bffb-82cfc69d6ff0)
 Call ID: ebf87192-f3d7-430f-bffb-82cfc69d6ff0
  Args:
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    type: :Person
  AddTriple (57c98378-bced-4a67-8d8a-52ec146dfe3e)
 Call ID: 57c98378-bced-4a67-8d8a-52ec146dfe3e
  Args:
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    relation: :hasMother
    target: George_von_dem_Bussche-Haddenhausen
  AssignClass (6bf5a4ad-c89a-4ced-a716-a4f50863a91d)
 Call ID: 6bf5a4ad-c89a-4ced-a716-a4f50863a91d
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    type: :Woman
  AssignClass (9a5e6780-b3b6-4562-b042-7c7df061f4ef)
 Call ID: 9a5e6780-b3b6-4562-b042-7c7df061f4ef
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    type: :Person
  AddLiteral (d52ed9e8-8c30-422f-b9d0-319e207650d7)
 Call ID: d52ed9e8-8c30-422f-b9d0-319e207650d7
  Args:
    literal_value: 1875
    source: María_Eleonore_Martínez_de_Hoz
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (d6ac5522-c665-4629-bca6-6eb1136ef4a2)
 Call ID: d6ac5522-c665-4629-bca6-6eb1136ef4a2
  Args:
    literal_type: xsd:integer
    source: María_Eleonore_Martínez_de_Hoz
    relation: :hasDeathYear
    literal_value: 1957
  AddLiteral (a96edb30-3bcc-44c6-a37a-159c529f2c01)
 Call ID: a96edb30-3bcc-44c6-a37a-159c529f2c01
  Args:
    literal_type: xsd:integer
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasMarriageYear
    literal_value: 1899
  AddTriple (3b724d3a-7f5f-446f-92d7-96a4f6ba0495)
 Call ID: 3b724d3a-7f5f-446f-92d7-96a4f6ba0495
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
    target: María_Eleonore_Martínez_de_Hoz
  AssignClass (1ab33276-382b-4cfa-bcb7-32c15c55dd0d)
 Call ID: 1ab33276-382b-4cfa-bcb7-32c15c55dd0d
  Args:
    type: :Man
    source: Narciso_Martínez_de_Hoz
  AssignClass (25e31e84-df79-47aa-be75-172f70d419d4)
 Call ID: 25e31e84-df79-47aa-be75-172f70d419d4
  Args:
    source: Narciso_Martínez_de_Hoz
    type: :Person
  AssignClass (d6119cf1-6722-4069-86df-f800c2b4ac2d)
 Call ID: d6119cf1-6722-4069-86df-f800c2b4ac2d
  Args:
    type: :Woman
    source: Mathilde_Stegmann
  AssignClass (3d8c7bc7-e5bd-4faa-a514-2b45e8a24447)
 Call ID: 3d8c7bc7-e5bd-4faa-a514-2b45e8a24447
  Args:
    source: Mathilde_Stegmann
    type: :Person
  AddTriple (f290afbe-465d-4605-ae3a-dff1a4d680f6)
 Call ID: f290afbe-465d-4605-ae3a-dff1a4d680f6
  Args:
    relation: :hasFather
    target: Narciso_Martínez_de_Hoz
    source: María_Eleonore_Martínez_de_Hoz
  AddTriple (28fb4804-3447-4a8d-bd6d-d062874c9409)
 Call ID: 28fb4804-3447-4a8d-bd6d-d062874c9409
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    target: Mathilde_Stegmann
    relation: :hasMother
  Finish (1d22dbb1-fce4-4c4a-9710-1b376869d4aa)
 Call ID: 1d22dbb1-fce4-4c4a-9710-1b376869d4aa
  Args: