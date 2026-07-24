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
  AssignClass (dcfb9c2a-a92b-45d8-abaa-4d60b8079bd6)
 Call ID: dcfb9c2a-a92b-45d8-abaa-4d60b8079bd6
  Args:
    source: Hilmar_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (f2f1a19e-11de-4d51-ad82-b22ccc97a7c3)
 Call ID: f2f1a19e-11de-4d51-ad82-b22ccc97a7c3
  Args:
    type: :Person
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AddLiteral (740306a6-ed51-4b70-a742-8a025b320d5a)
 Call ID: 740306a6-ed51-4b70-a742-8a025b320d5a
  Args:
    literal_value: 1867
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AddLiteral (5c690915-37e1-4bb7-bd98-e62e8cf633f8)
 Call ID: 5c690915-37e1-4bb7-bd98-e62e8cf633f8
  Args:
    relation: :hasDeathYear
    source: Hilmar_von_dem_Bussche-Haddenhausen
    literal_value: 1939
    literal_type: xsd:integer
  AssignClass (c8b8285a-5ed1-45f2-91d1-ee6ffc33d71c)
 Call ID: c8b8285a-5ed1-45f2-91d1-ee6ffc33d71c
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (80f3a18f-1f98-4a8b-ae92-927d958ebccb)
 Call ID: 80f3a18f-1f98-4a8b-ae92-927d958ebccb
  Args:
    type: :Person
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (108a031d-c720-4659-9ec4-cb26bec40932)
 Call ID: 108a031d-c720-4659-9ec4-cb26bec40932
  Args:
    literal_type: xsd:integer
    literal_value: 1827
    relation: :hasBirthYear
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (50d1fb20-d53c-4ffb-b6ad-d968760c5c20)
 Call ID: 50d1fb20-d53c-4ffb-b6ad-d968760c5c20
  Args:
    literal_type: xsd:integer
    literal_value: 1882
    relation: :hasDeathYear
    source: Julius_von_dem_Bussche-Haddenhausen
  AssignClass (deef9343-34d1-4a8d-a9eb-e95a36c342f6)
 Call ID: deef9343-34d1-4a8d-a9eb-e95a36c342f6
  Args:
    source: Mathilde_von_Salviati
    type: :Woman
  AssignClass (c3ec7411-4c0e-45a2-8a22-6f5168f3cf28)
 Call ID: c3ec7411-4c0e-45a2-8a22-6f5168f3cf28
  Args:
    type: :Person
    source: Mathilde_von_Salviati
  AddLiteral (82169ac9-5c82-4c76-b42a-6d1759ab6910)
 Call ID: 82169ac9-5c82-4c76-b42a-6d1759ab6910
  Args:
    source: Mathilde_von_Salviati
    relation: :hasBirthYear
    literal_value: 1833
    literal_type: xsd:integer
  AddLiteral (de4ac044-05d4-4516-8cfa-21ee6058705c)
 Call ID: de4ac044-05d4-4516-8cfa-21ee6058705c
  Args:
    literal_value: 1892
    literal_type: xsd:integer
    source: Mathilde_von_Salviati
    relation: :hasDeathYear
  AddTriple (df6fe781-9c75-43d4-9adc-b49bf592625a)
 Call ID: df6fe781-9c75-43d4-9adc-b49bf592625a
  Args:
    relation: :hasFather
    source: Hilmar_von_dem_Bussche-Haddenhausen
    target: Julius_von_dem_Bussche-Haddenhausen
  AddTriple (b310cdda-6bc9-4f45-9b87-06e472625dc6)
 Call ID: b310cdda-6bc9-4f45-9b87-06e472625dc6
  Args:
    target: Mathilde_von_Salviati
    relation: :hasMother
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AssignClass (31bfaf7d-5797-4c71-a788-aa0c9c8e7536)
 Call ID: 31bfaf7d-5797-4c71-a788-aa0c9c8e7536
  Args:
    type: :Man
    source: George_von_dem_Bussche-Haddenhausen
  AssignClass (2b73583d-6325-4687-92be-a5334d2ba326)
 Call ID: 2b73583d-6325-4687-92be-a5334d2ba326
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Person
  AddTriple (d57b2f4b-0786-4a58-abdc-bcada7221dac)
 Call ID: d57b2f4b-0786-4a58-abdc-bcada7221dac
  Args:
    target: Hilmar_von_dem_Bussche-Haddenhausen
    relation: :isBrotherOf
    source: George_von_dem_Bussche-Haddenhausen
  AssignClass (5bc02372-8926-4fd5-8750-74dbca3b19d0)
 Call ID: 5bc02372-8926-4fd5-8750-74dbca3b19d0
  Args:
    type: :Woman
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (7d33fe3f-6c71-412f-84e8-7310c4bb9dde)
 Call ID: 7d33fe3f-6c71-412f-84e8-7310c4bb9dde
  Args:
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    type: :Person
  AddTriple (d03bab0a-4b2b-4302-b3fe-45433e371587)
 Call ID: d03bab0a-4b2b-4302-b3fe-45433e371587
  Args:
    source: Baroness_Gösta_von_dem_Bussche-Haddenhausen
    relation: :isChildOf
    target: George_von_dem_Bussche-Haddenhausen
  AssignClass (4311133b-5284-49d2-bfb0-14536888152a)
 Call ID: 4311133b-5284-49d2-bfb0-14536888152a
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (78caa7c3-4bf9-4079-91af-c9afea61f9ad)
 Call ID: 78caa7c3-4bf9-4079-91af-c9afea61f9ad
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Person
  AddTriple (140d3713-c042-4081-aab4-e07c77629c24)
 Call ID: 140d3713-c042-4081-aab4-e07c77629c24
  Args:
    relation: :isChildOf
    source: Prince_Claus_of_the_Netherlands
    target: Baroness_Gösta_von_dem_Bussche-Haddenhausen
  AssignClass (e2b21cf4-de40-4501-80e5-2cbf0d07a745)
 Call ID: e2b21cf4-de40-4501-80e5-2cbf0d07a745
  Args:
    type: :Woman
    source: María_Eleonore_Martínez_de_Hoz
  AssignClass (5d0987ce-f4cf-47fe-b446-73a1d780705d)
 Call ID: 5d0987ce-f4cf-47fe-b446-73a1d780705d
  Args:
    type: :Person
    source: María_Eleonore_Martínez_de_Hoz
  AddLiteral (f754aad2-0491-495f-84a5-d11031d68b94)
 Call ID: f754aad2-0491-495f-84a5-d11031d68b94
  Args:
    relation: :hasBirthYear
    source: María_Eleonore_Martínez_de_Hoz
    literal_value: 1875
    literal_type: xsd:integer
  AddLiteral (4ced7181-0141-4674-83f0-d2e092a9296e)
 Call ID: 4ced7181-0141-4674-83f0-d2e092a9296e
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    relation: :hasDeathYear
    literal_value: 1957
    literal_type: xsd:integer
  AddLiteral (ba1f869b-6c79-4c9b-aa96-5f71772c38c0)
 Call ID: ba1f869b-6c79-4c9b-aa96-5f71772c38c0
  Args:
    literal_type: xsd:integer
    literal_value: 1899
    relation: :hasMarriageYear
    source: Hilmar_von_dem_Bussche-Haddenhausen
  AddTriple (b4276fe3-9cc3-44ac-ad03-952571bff382)
 Call ID: b4276fe3-9cc3-44ac-ad03-952571bff382
  Args:
    target: María_Eleonore_Martínez_de_Hoz
    source: Hilmar_von_dem_Bussche-Haddenhausen
    relation: :hasRelation
  AssignClass (840e228e-5ebd-47bd-a8ac-f5ab9d53b28e)
 Call ID: 840e228e-5ebd-47bd-a8ac-f5ab9d53b28e
  Args:
    type: :Man
    source: Narciso_Martínez_de_Hoz
  AssignClass (74055a13-96f7-4e5d-a089-b0cb8e239efc)
 Call ID: 74055a13-96f7-4e5d-a089-b0cb8e239efc
  Args:
    type: :Person
    source: Narciso_Martínez_de_Hoz
  AssignClass (3f04006f-d868-4884-a2ff-84cf9c55695d)
 Call ID: 3f04006f-d868-4884-a2ff-84cf9c55695d
  Args:
    type: :Woman
    source: Mathilde_Stegmann
  AssignClass (65ace974-86e1-4b68-b209-a404a70a48fb)
 Call ID: 65ace974-86e1-4b68-b209-a404a70a48fb
  Args:
    source: Mathilde_Stegmann
    type: :Person
  AddTriple (b81bf02e-1295-4573-a0b8-d78971ca23f5)
 Call ID: b81bf02e-1295-4573-a0b8-d78971ca23f5
  Args:
    source: María_Eleonore_Martínez_de_Hoz
    relation: :hasFather
    target: Narciso_Martínez_de_Hoz
  AddTriple (e3d2b49c-70ad-49ac-aec4-6757f0c0caed)
 Call ID: e3d2b49c-70ad-49ac-aec4-6757f0c0caed
  Args:
    target: Mathilde_Stegmann
    relation: :hasMother
    source: María_Eleonore_Martínez_de_Hoz
  Finish (82749c2a-29ac-4d22-8a89-fb252ed5b52f)
 Call ID: 82749c2a-29ac-4d22-8a89-fb252ed5b52f
  Args: