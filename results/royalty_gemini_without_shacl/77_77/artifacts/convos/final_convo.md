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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c4f95a78-64a3-4d5d-9f5e-49637f8958e8)
 Call ID: c4f95a78-64a3-4d5d-9f5e-49637f8958e8
  Args:
    type: :Man
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AssignClass (4995e042-f21c-4213-9a17-2964f45ed08c)
 Call ID: 4995e042-f21c-4213-9a17-2964f45ed08c
  Args:
    source: Julius_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (19fc39ab-ed7a-4eab-ac1b-22781a0cc982)
 Call ID: 19fc39ab-ed7a-4eab-ac1b-22781a0cc982
  Args:
    type: :Woman
    source: Mathilde_von_Salviati
  AssignClass (0a589f78-a2a9-47e9-a143-bbdc58aad755)
 Call ID: 0a589f78-a2a9-47e9-a143-bbdc58aad755
  Args:
    source: George_von_dem_Bussche-Haddenhausen
    type: :Man
  AssignClass (75b2f26b-a71a-4be6-a262-3272bdf6fb65)
 Call ID: 75b2f26b-a71a-4be6-a262-3272bdf6fb65
  Args:
    source: Baroness_Gosta_von_dem_Bussche-Haddenhausen
    type: :Woman
  AssignClass (a66cb010-b095-4c55-a4ae-0a630f902bfd)
 Call ID: a66cb010-b095-4c55-a4ae-0a630f902bfd
  Args:
    source: Prince_Claus_of_the_Netherlands
    type: :Man
  AssignClass (60eac7ad-5623-4601-a331-19bdc45ea848)
 Call ID: 60eac7ad-5623-4601-a331-19bdc45ea848
  Args:
    source: Maria_Eleonore_Martinez_de_Hoz
    type: :Woman
  AssignClass (9ba7e24f-bdfb-4456-889f-32b70d256448)
 Call ID: 9ba7e24f-bdfb-4456-889f-32b70d256448
  Args:
    source: Narciso_Martinez_de_Hoz
    type: :Man
  AssignClass (9add3ba0-4cd6-42d7-9e49-9a1826131c90)
 Call ID: 9add3ba0-4cd6-42d7-9e49-9a1826131c90
  Args:
    source: Mathilde_Stegmann
    type: :Woman
  AddLiteral (4a65f235-aaa2-4da0-967a-f206038e2b9e)
 Call ID: 4a65f235-aaa2-4da0-967a-f206038e2b9e
  Args:
    relation: :hasBirthYear
    literal_value: 1867
    literal_type: xsd:integer
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddLiteral (db523f95-a792-4a4c-b1c7-e60993368fad)
 Call ID: db523f95-a792-4a4c-b1c7-e60993368fad
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasDeathYear
    literal_value: 1939
    literal_type: xsd:integer
  AddLiteral (4acb3657-ba74-4930-bed4-b2369c5dd6ab)
 Call ID: 4acb3657-ba74-4930-bed4-b2369c5dd6ab
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1827
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (1218fecd-b3ee-4568-bca2-4cc6c07006c1)
 Call ID: 1218fecd-b3ee-4568-bca2-4cc6c07006c1
  Args:
    literal_value: 1882
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Julius_von_dem_Bussche-Haddenhausen
  AddLiteral (6c93e1e1-f66c-4336-9c59-061aa7405b02)
 Call ID: 6c93e1e1-f66c-4336-9c59-061aa7405b02
  Args:
    literal_type: xsd:integer
    literal_value: 1833
    relation: :hasBirthYear
    source: Mathilde_von_Salviati
  AddLiteral (1b329afd-7cf0-4f5e-b03f-d53f178d1f3f)
 Call ID: 1b329afd-7cf0-4f5e-b03f-d53f178d1f3f
  Args:
    literal_value: 1892
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Mathilde_von_Salviati
  AddLiteral (d4bb118f-6b15-454d-b938-f85a75ff39cf)
 Call ID: d4bb118f-6b15-454d-b938-f85a75ff39cf
  Args:
    source: Maria_Eleonore_Martinez_de_Hoz
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1875
  AddLiteral (045bc404-4162-4dd4-9edd-5829ac5ec933)
 Call ID: 045bc404-4162-4dd4-9edd-5829ac5ec933
  Args:
    source: Maria_Eleonore_Martinez_de_Hoz
    literal_type: xsd:integer
    literal_value: 1957
    relation: :hasDeathYear
  AddLiteral (4d2743af-e3c1-4ecd-9ae4-a71daf80dc78)
 Call ID: 4d2743af-e3c1-4ecd-9ae4-a71daf80dc78
  Args:
    literal_type: xsd:integer
    literal_value: 1899
    relation: :hasMarriageYear
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddTriple (ca0cd9fe-d999-4918-8215-4c289b671df8)
 Call ID: ca0cd9fe-d999-4918-8215-4c289b671df8
  Args:
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    target: Julius_von_dem_Bussche-Haddenhausen
    relation: :hasFather
  AddTriple (3393c69a-0cba-4240-b2a8-820df5be30ea)
 Call ID: 3393c69a-0cba-4240-b2a8-820df5be30ea
  Args:
    target: Mathilde_von_Salviati
    source: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
    relation: :hasMother
  AddTriple (59172ed4-7486-4344-91a6-5adf7de6dfd1)
 Call ID: 59172ed4-7486-4344-91a6-5adf7de6dfd1
  Args:
    relation: :isBrotherOf
    source: George_von_dem_Bussche-Haddenhausen
    target: Hilmar_Freiherr_von_dem_Bussche-Haddenhausen
  AddTriple (c00510ba-65b7-4cec-848f-46b5bacc0a18)
 Call ID: c00510ba-65b7-4cec-848f-46b5bacc0a18
  Args:
    relation: :isMotherOf
    source: George_von_dem_Bussche-Haddenhausen
    target: Baroness_Gosta_von_dem_Bussche-Haddenhausen
  AddTriple (1d842156-262c-4e35-9590-6d506e0e253c)
 Call ID: 1d842156-262c-4e35-9590-6d506e0e253c
  Args:
    relation: :isMotherOf
    target: Prince_Claus_of_the_Netherlands
    source: Baroness_Gosta_von_dem_Bussche-Haddenhausen
  AddTriple (437097a5-1cd2-4cca-b67b-4a815a4ab140)
 Call ID: 437097a5-1cd2-4cca-b67b-4a815a4ab140
  Args:
    relation: :hasFather
    target: Narciso_Martinez_de_Hoz
    source: Maria_Eleonore_Martinez_de_Hoz
  AddTriple (43f562d0-b721-496d-947d-30bb68f710b1)
 Call ID: 43f562d0-b721-496d-947d-30bb68f710b1
  Args:
    relation: :hasMother
    target: Mathilde_Stegmann
    source: Maria_Eleonore_Martinez_de_Hoz
  Finish (d2467fce-4fcb-41ba-b8eb-59e2a917f709)
 Call ID: d2467fce-4fcb-41ba-b8eb-59e2a917f709
  Args: