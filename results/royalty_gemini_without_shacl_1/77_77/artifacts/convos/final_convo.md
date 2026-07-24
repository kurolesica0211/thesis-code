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
  AssignClass (47708efd-55ca-4301-8832-1dcbc0250c86)
 Call ID: 47708efd-55ca-4301-8832-1dcbc0250c86
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (e60cfe09-0196-49dc-9f2a-6000a66955d0)
 Call ID: e60cfe09-0196-49dc-9f2a-6000a66955d0
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    type: :Person
  AddLiteral (63211077-a1e9-488c-b8a3-d5e43a0a2f98)
 Call ID: 63211077-a1e9-488c-b8a3-d5e43a0a2f98
  Args:
    literal_type: xsd:integer
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_value: 1867
    relation: :hasBirthYear
  AddLiteral (3780c761-9687-4775-8805-91ee64dd1ffd)
 Call ID: 3780c761-9687-4775-8805-91ee64dd1ffd
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1939
    relation: :hasDeathYear
  AssignClass (3d042d51-9f70-4ccc-a6ce-3b43efe38689)
 Call ID: 3d042d51-9f70-4ccc-a6ce-3b43efe38689
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (cfc126f5-2961-4825-8cda-5e10c5d78020)
 Call ID: cfc126f5-2961-4825-8cda-5e10c5d78020
  Args:
    type: :Person
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (2947393e-b18d-4f99-8b3e-55b9cee48efd)
 Call ID: 2947393e-b18d-4f99-8b3e-55b9cee48efd
  Args:
    relation: :hasBirthYear
    literal_value: 1827
    source: Julius_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
  AddLiteral (d6e68694-52dd-4899-b46e-1f622d0f6cb2)
 Call ID: d6e68694-52dd-4899-b46e-1f622d0f6cb2
  Args:
    literal_type: xsd:integer
    source: Julius_von_dem_Bussche-Haddenhausen
    literal_value: 1882
    relation: :hasDeathYear
  AssignClass (b646f9c7-6103-40cb-9270-5683cb2e8777)
 Call ID: b646f9c7-6103-40cb-9270-5683cb2e8777
  Args:
    type: :Woman
    source: Mathilde_von_Salviati
  AssignClass (19425970-bebd-44c9-81e5-b632792f7e13)
 Call ID: 19425970-bebd-44c9-81e5-b632792f7e13
  Args:
    source: Mathilde_von_Salviati
    type: :Person
  AddLiteral (c225b04a-c342-42d3-b054-e83bc8d38a80)
 Call ID: c225b04a-c342-42d3-b054-e83bc8d38a80
  Args:
    literal_type: xsd:integer
    source: Mathilde_von_Salviati
    literal_value: 1833
    relation: :hasBirthYear
  AddLiteral (13258df6-8ed9-4cd6-a47e-c4aabe56ec09)
 Call ID: 13258df6-8ed9-4cd6-a47e-c4aabe56ec09
  Args:
    literal_value: 1892
    literal_type: xsd:integer
    source: Mathilde_von_Salviati
    relation: :hasDeathYear
  AddTriple (10e6a16c-2700-4036-87aa-f6be8a069e50)
 Call ID: 10e6a16c-2700-4036-87aa-f6be8a069e50
  Args:
    target: Julius_von_dem_Bussche-Haddenhausen
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (aba7162a-0ff9-4abe-a9cc-afd1f8314a6b)
 Call ID: aba7162a-0ff9-4abe-a9cc-afd1f8314a6b
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    target: Mathilde_von_Salviati
    relation: :hasMother
  AssignClass (4038e600-dce1-4cac-a21b-2f7841b2c0f2)
 Call ID: 4038e600-dce1-4cac-a21b-2f7841b2c0f2
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (b2dff8e9-8a27-402a-9d41-57bd2acdda27)
 Call ID: b2dff8e9-8a27-402a-9d41-57bd2acdda27
  Args:
    type: :Person
    source: George_von_dem_Bussche-Haddenhausen
  AddTriple (4a24207a-8e02-43a2-864c-47dfcfece6b9)
 Call ID: 4a24207a-8e02-43a2-864c-47dfcfece6b9
  Args:
    target: George_von_dem_Bussche-Haddenhausen
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :isSiblingOf
  AssignClass (0edd2ab4-92bc-4c8b-92f5-7760524ccca6)
 Call ID: 0edd2ab4-92bc-4c8b-92f5-7760524ccca6
  Args:
    type: :Woman
    source: Baroness_Gosta_von_dem_Bussche-Haddenhausen
  AssignClass (b7814594-228e-499b-a867-9347df679cf1)
 Call ID: b7814594-228e-499b-a867-9347df679cf1
  Args:
    source: Baroness_Gosta_von_dem_Bussche-Haddenhausen
    type: :Person
  AddTriple (b506965a-755e-4dca-b1d8-65cc7a0711eb)
 Call ID: b506965a-755e-4dca-b1d8-65cc7a0711eb
  Args:
    relation: :hasMother
    source: Baroness_Gosta_von_dem_Bussche-Haddenhausen
    target: George_von_dem_Bussche-Haddenhausen
  AssignClass (3c86259d-616e-4301-917b-f5a8fc400f05)
 Call ID: 3c86259d-616e-4301-917b-f5a8fc400f05
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (df2ce6cb-0e6b-4da9-8a41-b9771411cda5)
 Call ID: df2ce6cb-0e6b-4da9-8a41-b9771411cda5
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Person
  AddTriple (8169c409-5bb4-46cd-8da6-9d41610c470a)
 Call ID: 8169c409-5bb4-46cd-8da6-9d41610c470a
  Args:
    relation: :hasMother
    target: Baroness_Gosta_von_dem_Bussche-Haddenhausen
    source: Prince_Claus_of_the_Netherlands
  AssignClass (b7b59ad0-505e-46b2-80f5-097b97b7e2a3)
 Call ID: b7b59ad0-505e-46b2-80f5-097b97b7e2a3
  Args:
    source: Maria_Eleonore_Martinez_de_Hoz
    type: :Woman
  AssignClass (bfd6b79e-0920-4a0d-877b-3c1fcccfa82c)
 Call ID: bfd6b79e-0920-4a0d-877b-3c1fcccfa82c
  Args:
    type: :Person
    source: Maria_Eleonore_Martinez_de_Hoz
  AddLiteral (07ba745d-dcb0-429d-8a2f-f72211d177df)
 Call ID: 07ba745d-dcb0-429d-8a2f-f72211d177df
  Args:
    relation: :hasBirthYear
    literal_value: 1875
    source: Maria_Eleonore_Martinez_de_Hoz
    literal_type: xsd:integer
  AddLiteral (04afd1cf-1027-4000-9e09-cb2f371e9e07)
 Call ID: 04afd1cf-1027-4000-9e09-cb2f371e9e07
  Args:
    source: Maria_Eleonore_Martinez_de_Hoz
    literal_type: xsd:integer
    literal_value: 1957
    relation: :hasDeathYear
  AddLiteral (bad07304-7c6d-46b7-9b73-25858ec6339e)
 Call ID: bad07304-7c6d-46b7-9b73-25858ec6339e
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    literal_type: xsd:integer
    literal_value: 1899
    relation: :hasMarriageYear
  AddTriple (54356c9f-cfe9-4d5c-9f6a-024ab3863538)
 Call ID: 54356c9f-cfe9-4d5c-9f6a-024ab3863538
  Args:
    target: Maria_Eleonore_Martinez_de_Hoz
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
  AssignClass (f98ac1bd-0db0-44bb-a613-46c97cdf7b51)
 Call ID: f98ac1bd-0db0-44bb-a613-46c97cdf7b51
  Args:
    type: :Man
    source: Narciso_Martinez_de_Hoz
  AssignClass (4d48cb26-8793-4219-8c50-b25b2435ee59)
 Call ID: 4d48cb26-8793-4219-8c50-b25b2435ee59
  Args:
    type: :Person
    source: Narciso_Martinez_de_Hoz
  AssignClass (fa1a1332-9f82-48cd-8d53-ec048224c42f)
 Call ID: fa1a1332-9f82-48cd-8d53-ec048224c42f
  Args:
    type: :Woman
    source: Mathilde_Stegmann
  AssignClass (8c8722b2-b6f6-41d6-b2e0-55eb4b0db1c2)
 Call ID: 8c8722b2-b6f6-41d6-b2e0-55eb4b0db1c2
  Args:
    source: Mathilde_Stegmann
    type: :Person
  AddTriple (a9b4e16b-f692-4c37-b274-4e54929918c1)
 Call ID: a9b4e16b-f692-4c37-b274-4e54929918c1
  Args:
    relation: :hasFather
    source: Maria_Eleonore_Martinez_de_Hoz
    target: Narciso_Martinez_de_Hoz
  AddTriple (fb3be621-e7af-4f3d-9046-5ac209717929)
 Call ID: fb3be621-e7af-4f3d-9046-5ac209717929
  Args:
    relation: :hasMother
    source: Maria_Eleonore_Martinez_de_Hoz
    target: Mathilde_Stegmann
  Finish (5eed8bf9-e1ad-4835-b0a0-0ac3d1cbf949)
 Call ID: 5eed8bf9-e1ad-4835-b0a0-0ac3d1cbf949
  Args: