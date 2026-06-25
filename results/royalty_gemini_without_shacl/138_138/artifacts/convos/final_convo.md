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
Prince Alexander of Yugoslavia (Serbian: Александар П. Карађорђевић / Aleksandar P. Karađorđević; 13 August 1924 – 12 May 2016) was the elder son of Prince Paul, who served as Regent of Yugoslavia in the 1930s, and his wife, Princess Olga of Greece and Denmark.
Birth and education

Alexander was born at White Lodge, Richmond Park, United Kingdom.
As a nephew of Princess Marina, Duchess of Kent (née of Greece and Denmark), he was a first cousin of Prince Edward, Duke of Kent, Prince Michael of Kent, and Princess Alexandra of Kent; he was also a first cousin once removed of Prince Philip, Duke of Edinburgh.
Marriages and family

He took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On 12 February 1955, Alexander married Princess Maria Pia of Savoy, daughter of King Umberto II of Italy and of his wife, Princess Marie José of Belgium.
The couple had met on 22 August 1954 during the royal cruise of the Agamemnon, hosted by King Paul and Queen Frederica of Greece.
Alexander and Maria Pia have twin sons born in 1958:
Alexander and Maria Pia divorced in 1967, and in 2003 she married Prince Michel of Bourbon-Parma, himself divorced from Princess Yolande de Broglie-Revel.
On 2 November 1973, in a civil ceremony in Paris, Alexander married Princess Barbara Eleonore Marie of Liechtenstein(born 9 July 1942), daughter of Prince Johannes of Liechtenstein (first cousin once removed to Prince Hans-Adam II of Liechtenstein) and Countess Karoline of Ledebur-Wicheln (aunt of Hans Adam's late wife Marie, Princess of Liechtenstein).
On 28 October 1995 Prince Alexander and Princess Barbara were married in the Orthodox faith in
Oplenac, and had issue:


Flying career

The Prince wished to serve in the British Royal Air Force during World War Two, but was initially prevented by his father's political affiliations.
He was eventually commissioned in the RAF through the intervention of Prince George, Duke of Kent, his uncle.
Associations

Alexander was one of the four founding members of the Serbian Unity Congress.
On 17 February 2008, Alexander issued a statement condemning the declaration of independence by Kosovo.
On the occasion of Prince Alexander's 90th birthday on 13 August 2014, a celebration of his life in words and pictures appeared in that month's UK magazine Majesty.
Death

Prince Alexander died on 12 May 2016 in Paris, where he and his wife had lived for many years.
He was buried at Oplenac, Serbia, with his parents and brother, his coffin being carried by Serbian Air Force fighter pilots.



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
  AssignClass (7b8971b4-70b2-4bd9-9041-2d9059cf26f3)
 Call ID: 7b8971b4-70b2-4bd9-9041-2d9059cf26f3
  Args:
    type: :Man
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (b4df0497-25d5-408d-ab66-bc6249733917)
 Call ID: b4df0497-25d5-408d-ab66-bc6249733917
  Args:
    type: :Person
    source: Prince_Alexander_of_Yugoslavia
  AddLiteral (fcce092b-1663-4697-aba9-235ea53349f9)
 Call ID: fcce092b-1663-4697-aba9-235ea53349f9
  Args:
    literal_value: 1924
    literal_type: xsd:integer
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasBirthYear
  AddLiteral (f93b9578-4551-4a19-915e-ffcc15e67bf1)
 Call ID: f93b9578-4551-4a19-915e-ffcc15e67bf1
  Args:
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasDeathYear
    literal_value: 2016
    literal_type: xsd:integer
  AssignClass (143a2474-b7eb-40c7-8a26-7521836a5710)
 Call ID: 143a2474-b7eb-40c7-8a26-7521836a5710
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (a695c99f-746a-4740-9316-ee2423c48ff2)
 Call ID: a695c99f-746a-4740-9316-ee2423c48ff2
  Args:
    source: Prince_Paul_of_Yugoslavia
    type: :Person
  AddTriple (0b2b53e3-bd1d-441d-bbee-18c802e4c04d)
 Call ID: 0b2b53e3-bd1d-441d-bbee-18c802e4c04d
  Args:
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasFather
    target: Prince_Paul_of_Yugoslavia
  AssignClass (10a86c48-e24d-4d1a-9b38-ce62daa50685)
 Call ID: 10a86c48-e24d-4d1a-9b38-ce62daa50685
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (48d17428-e661-46e2-84eb-f73ff0a953dc)
 Call ID: 48d17428-e661-46e2-84eb-f73ff0a953dc
  Args:
    type: :Person
    source: Princess_Olga_of_Greece_and_Denmark
  AddTriple (0c313932-e9fc-4432-8c83-ac85082f9844)
 Call ID: 0c313932-e9fc-4432-8c83-ac85082f9844
  Args:
    target: Princess_Olga_of_Greece_and_Denmark
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasMother
  AssignClass (b6a4ba38-fc53-40a9-8099-262fa5919ceb)
 Call ID: b6a4ba38-fc53-40a9-8099-262fa5919ceb
  Args:
    source: Princess_Maria_Pia_of_Savoy
    type: :Woman
  AssignClass (534d40c3-fc3d-49c0-9120-89a9e0c801ba)
 Call ID: 534d40c3-fc3d-49c0-9120-89a9e0c801ba
  Args:
    type: :Person
    source: Princess_Maria_Pia_of_Savoy
  AddLiteral (d04683fa-c944-48d3-98a7-845d3f520469)
 Call ID: d04683fa-c944-48d3-98a7-845d3f520469
  Args:
    literal_type: xsd:integer
    literal_value: 1955
    relation: :hasMarriageYear
    source: Prince_Alexander_of_Yugoslavia
  AddTriple (56e79bf5-6513-4085-8f91-4601988c5418)
 Call ID: 56e79bf5-6513-4085-8f91-4601988c5418
  Args:
    target: Princess_Maria_Pia_of_Savoy
    relation: :hasRelation
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (997cfa10-ea6f-461c-9caf-845b85e63fd2)
 Call ID: 997cfa10-ea6f-461c-9caf-845b85e63fd2
  Args:
    source: King_Umberto_II_of_Italy
    type: :Man
  AssignClass (4df12139-5f4f-4993-ad7d-278928fed79a)
 Call ID: 4df12139-5f4f-4993-ad7d-278928fed79a
  Args:
    source: King_Umberto_II_of_Italy
    type: :Person
  AddTriple (98bb941d-40b1-4f5c-9eeb-6176f4f9eaa6)
 Call ID: 98bb941d-40b1-4f5c-9eeb-6176f4f9eaa6
  Args:
    relation: :hasFather
    source: Princess_Maria_Pia_of_Savoy
    target: King_Umberto_II_of_Italy
  AssignClass (a7e85f42-41b9-433b-a1a7-5d989590477f)
 Call ID: a7e85f42-41b9-433b-a1a7-5d989590477f
  Args:
    type: :Woman
    source: Princess_Marie_Jose_of_Belgium
  AssignClass (f2ea66c7-ae07-4ba6-b2d9-343f3e0e8cc6)
 Call ID: f2ea66c7-ae07-4ba6-b2d9-343f3e0e8cc6
  Args:
    type: :Person
    source: Princess_Marie_Jose_of_Belgium
  AddTriple (5856415c-ebe8-4266-b34f-ea7069a93322)
 Call ID: 5856415c-ebe8-4266-b34f-ea7069a93322
  Args:
    target: Princess_Marie_Jose_of_Belgium
    source: Princess_Maria_Pia_of_Savoy
    relation: :hasMother
  AssignClass (0a3a04cd-3eb8-4fdc-a09f-10574feacb44)
 Call ID: 0a3a04cd-3eb8-4fdc-a09f-10574feacb44
  Args:
    source: Prince_Michel_of_Bourbon-Parma
    type: :Man
  AssignClass (e73a9276-deed-4f17-b254-7fc6b0dc855c)
 Call ID: e73a9276-deed-4f17-b254-7fc6b0dc855c
  Args:
    type: :Person
    source: Prince_Michel_of_Bourbon-Parma
  AddLiteral (6e60dd35-da75-4726-aaac-90a49398e7ac)
 Call ID: 6e60dd35-da75-4726-aaac-90a49398e7ac
  Args:
    literal_value: 2003
    literal_type: xsd:integer
    source: Princess_Maria_Pia_of_Savoy
    relation: :hasMarriageYear
  AddTriple (9314b901-090b-4263-b151-668c6b1fafe6)
 Call ID: 9314b901-090b-4263-b151-668c6b1fafe6
  Args:
    source: Princess_Maria_Pia_of_Savoy
    relation: :hasRelation
    target: Prince_Michel_of_Bourbon-Parma
  AssignClass (9350891b-9350-4f1f-bfb1-1d43b9aa330f)
 Call ID: 9350891b-9350-4f1f-bfb1-1d43b9aa330f
  Args:
    type: :Woman
    source: Princess_Yolande_de_Broglie-Revel
  AssignClass (388df101-4828-429f-8e64-0c5bb93efc40)
 Call ID: 388df101-4828-429f-8e64-0c5bb93efc40
  Args:
    type: :Person
    source: Princess_Yolande_de_Broglie-Revel
  AddTriple (a2d72d74-4d08-4e54-8184-9c2cf497f039)
 Call ID: a2d72d74-4d08-4e54-8184-9c2cf497f039
  Args:
    target: Princess_Yolande_de_Broglie-Revel
    relation: :hasRelation
    source: Prince_Michel_of_Bourbon-Parma
  AssignClass (c5e28767-65eb-47c3-8177-ec8923fa7ee1)
 Call ID: c5e28767-65eb-47c3-8177-ec8923fa7ee1
  Args:
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    type: :Woman
  AssignClass (632c0f0a-b7aa-4cfb-8c8a-895fef9bdcab)
 Call ID: 632c0f0a-b7aa-4cfb-8c8a-895fef9bdcab
  Args:
    type: :Person
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AddLiteral (c12df2b1-b83e-40aa-97f0-e570357b9eb0)
 Call ID: c12df2b1-b83e-40aa-97f0-e570357b9eb0
  Args:
    relation: :hasMarriageYear
    source: Prince_Alexander_of_Yugoslavia
    literal_type: xsd:integer
    literal_value: 1973
  AddTriple (d31ef9c1-31f9-4aac-adac-7b3c8304b3c9)
 Call ID: d31ef9c1-31f9-4aac-adac-7b3c8304b3c9
  Args:
    relation: :hasRelation
    source: Prince_Alexander_of_Yugoslavia
    target: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AssignClass (dc067536-94ca-47c2-a447-ba950d9359be)
 Call ID: dc067536-94ca-47c2-a447-ba950d9359be
  Args:
    type: :Man
    source: Prince_Johannes_of_Liechtenstein
  AssignClass (6d95f8bb-2a48-4212-81c7-e924b5ec7e1a)
 Call ID: 6d95f8bb-2a48-4212-81c7-e924b5ec7e1a
  Args:
    type: :Person
    source: Prince_Johannes_of_Liechtenstein
  AddTriple (b43b1029-94bf-40f8-9408-203f5015f064)
 Call ID: b43b1029-94bf-40f8-9408-203f5015f064
  Args:
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    relation: :hasFather
    target: Prince_Johannes_of_Liechtenstein
  AssignClass (21e62ae8-3740-4b74-8c7c-78d97e1bae92)
 Call ID: 21e62ae8-3740-4b74-8c7c-78d97e1bae92
  Args:
    source: Countess_Karoline_of_Ledebur-Wicheln
    type: :Woman
  AssignClass (dd390b27-b115-409f-a6f2-fc58ff7c6397)
 Call ID: dd390b27-b115-409f-a6f2-fc58ff7c6397
  Args:
    source: Countess_Karoline_of_Ledebur-Wicheln
    type: :Person
  AddTriple (f1bc5145-40b6-4169-841f-de29599bc721)
 Call ID: f1bc5145-40b6-4169-841f-de29599bc721
  Args:
    relation: :hasMother
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    target: Countess_Karoline_of_Ledebur-Wicheln
  AssignClass (8e6f0529-0595-46f3-8857-54e7d1208480)
 Call ID: 8e6f0529-0595-46f3-8857-54e7d1208480
  Args:
    source: Prince_George_Duke_of_Kent
    type: :Man
  AssignClass (cbfb1c22-603f-4377-b0d6-b09be0214fd9)
 Call ID: cbfb1c22-603f-4377-b0d6-b09be0214fd9
  Args:
    type: :Person
    source: Prince_George_Duke_of_Kent
  AddTriple (1515229d-8161-445f-b427-0678d260790f)
 Call ID: 1515229d-8161-445f-b427-0678d260790f
  Args:
    target: Prince_George_Duke_of_Kent
    source: Prince_Alexander_of_Yugoslavia
    relation: :hasRelation
  Finish (15c8d578-b9e8-4c0c-b865-defcab6284ab)
 Call ID: 15c8d578-b9e8-4c0c-b865-defcab6284ab
  Args: