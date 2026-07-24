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
  AssignClass (2dfab409-6405-4153-af14-caa85a18595e)
 Call ID: 2dfab409-6405-4153-af14-caa85a18595e
  Args:
    type: :Man
    source: :Alexander_of_Yugoslavia
  AssignClass (e5e33658-f375-42e6-8c02-77a074ff4377)
 Call ID: e5e33658-f375-42e6-8c02-77a074ff4377
  Args:
    source: :Alexander_of_Yugoslavia
    type: :Person
  AddLiteral (49f9e26f-dbcf-4454-92a8-4279f973c2ca)
 Call ID: 49f9e26f-dbcf-4454-92a8-4279f973c2ca
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1924
    relation: :hasBirthYear
    source: :Alexander_of_Yugoslavia
  AddLiteral (59bd17aa-737a-4bb9-9367-535793c0b9a6)
 Call ID: 59bd17aa-737a-4bb9-9367-535793c0b9a6
  Args:
    source: :Alexander_of_Yugoslavia
    relation: :hasDeathYear
    literal_value: 2016
    literal_type: xsd:positiveInteger
  AssignClass (31dbe743-682b-4eb5-a4bd-bdc535f5a999)
 Call ID: 31dbe743-682b-4eb5-a4bd-bdc535f5a999
  Args:
    type: :Man
    source: :Prince_Paul
  AssignClass (564dec1f-b7f2-4d32-b3f3-7bb8cf23450b)
 Call ID: 564dec1f-b7f2-4d32-b3f3-7bb8cf23450b
  Args:
    type: :Person
    source: :Prince_Paul
  AddTriple (c9c5ceed-c186-4d4c-a7ad-fab6a4f61589)
 Call ID: c9c5ceed-c186-4d4c-a7ad-fab6a4f61589
  Args:
    target: :Prince_Paul
    relation: :hasFather
    source: :Alexander_of_Yugoslavia
  AssignClass (8e311902-6063-4535-bca9-3997294c0e28)
 Call ID: 8e311902-6063-4535-bca9-3997294c0e28
  Args:
    type: :Woman
    source: :Princess_Olga
  AssignClass (718a3c86-a82b-46f8-bee4-740740959494)
 Call ID: 718a3c86-a82b-46f8-bee4-740740959494
  Args:
    type: :Person
    source: :Princess_Olga
  AddTriple (91e0ae74-4e2d-4a58-9499-e0b5ec9af05c)
 Call ID: 91e0ae74-4e2d-4a58-9499-e0b5ec9af05c
  Args:
    relation: :hasMother
    target: :Princess_Olga
    source: :Alexander_of_Yugoslavia
  AssignClass (960ba611-c646-49c1-be85-771c0d7fb06f)
 Call ID: 960ba611-c646-49c1-be85-771c0d7fb06f
  Args:
    type: :Woman
    source: :Princess_Maria_Pia
  AssignClass (1a2b9705-be53-42d6-a016-179281521c80)
 Call ID: 1a2b9705-be53-42d6-a016-179281521c80
  Args:
    source: :Princess_Maria_Pia
    type: :Person
  AddTriple (464f68d2-2520-4dd8-bb86-aaa8dc3dff02)
 Call ID: 464f68d2-2520-4dd8-bb86-aaa8dc3dff02
  Args:
    relation: :hasRelation
    target: :Princess_Maria_Pia
    source: :Alexander_of_Yugoslavia
  AddLiteral (270dc53f-dd2e-452b-b2d8-1930497681bb)
 Call ID: 270dc53f-dd2e-452b-b2d8-1930497681bb
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1955
    relation: :hasMarriageYear
    source: :Alexander_of_Yugoslavia
  AssignClass (f99eac37-3273-485f-bbb2-eeee6cfa0277)
 Call ID: f99eac37-3273-485f-bbb2-eeee6cfa0277
  Args:
    type: :Man
    source: :King_Umberto_II
  AssignClass (708ec25b-f1e3-4898-bd26-2bf5d95d47ec)
 Call ID: 708ec25b-f1e3-4898-bd26-2bf5d95d47ec
  Args:
    type: :Person
    source: :King_Umberto_II
  AddTriple (a0674c31-896a-4188-8d8f-17faf2fde534)
 Call ID: a0674c31-896a-4188-8d8f-17faf2fde534
  Args:
    target: :King_Umberto_II
    relation: :hasFather
    source: :Princess_Maria_Pia
  AssignClass (20510454-1461-4935-bb1b-492cd4ee8035)
 Call ID: 20510454-1461-4935-bb1b-492cd4ee8035
  Args:
    source: :Princess_Marie_Jose
    type: :Woman
  AssignClass (16f24d82-d7bb-47fc-92d1-8e21b118ecde)
 Call ID: 16f24d82-d7bb-47fc-92d1-8e21b118ecde
  Args:
    type: :Person
    source: :Princess_Marie_Jose
  AddTriple (2e6761be-c6a7-4720-8bb1-439252498aee)
 Call ID: 2e6761be-c6a7-4720-8bb1-439252498aee
  Args:
    source: :Princess_Maria_Pia
    relation: :hasMother
    target: :Princess_Marie_Jose
  AssignClass (d253d6e5-913f-42a3-bb80-40e2ad03b1fd)
 Call ID: d253d6e5-913f-42a3-bb80-40e2ad03b1fd
  Args:
    type: :Man
    source: :Prince_Michel_of_Bourbon_Parma
  AssignClass (50b21b83-b3de-4d54-a855-8b727d526524)
 Call ID: 50b21b83-b3de-4d54-a855-8b727d526524
  Args:
    source: :Prince_Michel_of_Bourbon_Parma
    type: :Person
  AddTriple (8e606c79-1b92-4447-8fa8-093da602b477)
 Call ID: 8e606c79-1b92-4447-8fa8-093da602b477
  Args:
    relation: :hasRelation
    target: :Prince_Michel_of_Bourbon_Parma
    source: :Princess_Maria_Pia
  AssignClass (57bf3b76-e594-4f8b-8e81-ec2f04d905e7)
 Call ID: 57bf3b76-e594-4f8b-8e81-ec2f04d905e7
  Args:
    source: :Princess_Yolande_de_Broglie_Revel
    type: :Woman
  AssignClass (6dad2182-c64d-4eac-9d57-886a4c747d04)
 Call ID: 6dad2182-c64d-4eac-9d57-886a4c747d04
  Args:
    type: :Person
    source: :Princess_Yolande_de_Broglie_Revel
  AddTriple (e82279e2-aae8-4d3e-a10f-ceb03d7459c2)
 Call ID: e82279e2-aae8-4d3e-a10f-ceb03d7459c2
  Args:
    target: :Princess_Yolande_de_Broglie_Revel
    relation: :hasRelation
    source: :Prince_Michel_of_Bourbon_Parma
  AssignClass (f26806d4-4c4f-4128-84d7-157b72c8d54d)
 Call ID: f26806d4-4c4f-4128-84d7-157b72c8d54d
  Args:
    source: :Princess_Barbara_Eleonore_Marie
    type: :Woman
  AssignClass (f14041e0-2438-4de6-8d4f-c4e21a9cc3e2)
 Call ID: f14041e0-2438-4de6-8d4f-c4e21a9cc3e2
  Args:
    source: :Princess_Barbara_Eleonore_Marie
    type: :Person
  AddTriple (b99a4cba-b1e6-4d25-b974-011d9fca4a9c)
 Call ID: b99a4cba-b1e6-4d25-b974-011d9fca4a9c
  Args:
    relation: :hasRelation
    target: :Princess_Barbara_Eleonore_Marie
    source: :Alexander_of_Yugoslavia
  AddLiteral (9f7577e5-ee90-4e26-87c7-7d981ff0ec8e)
 Call ID: 9f7577e5-ee90-4e26-87c7-7d981ff0ec8e
  Args:
    source: :Alexander_of_Yugoslavia
    relation: :hasMarriageYear
    literal_value: 1973
    literal_type: xsd:positiveInteger
  AssignClass (878ca8e6-1230-4854-abfb-687e0dff9e8c)
 Call ID: 878ca8e6-1230-4854-abfb-687e0dff9e8c
  Args:
    type: :Man
    source: :Prince_Johannes_of_Liechtenstein
  AssignClass (305a9ab9-18d0-44cb-ada6-070ce7eb01ee)
 Call ID: 305a9ab9-18d0-44cb-ada6-070ce7eb01ee
  Args:
    type: :Person
    source: :Prince_Johannes_of_Liechtenstein
  AddTriple (ec8d99dc-6a2c-44ea-b167-dc30acbecc03)
 Call ID: ec8d99dc-6a2c-44ea-b167-dc30acbecc03
  Args:
    relation: :hasFather
    target: :Prince_Johannes_of_Liechtenstein
    source: :Princess_Barbara_Eleonore_Marie
  AssignClass (913c4ed7-8156-42b1-b72b-1f922a5cbeac)
 Call ID: 913c4ed7-8156-42b1-b72b-1f922a5cbeac
  Args:
    source: :Countess_Karoline_of_Ledebur_Wicheln
    type: :Woman
  AssignClass (79fa4794-b412-486e-974a-078f6007a64c)
 Call ID: 79fa4794-b412-486e-974a-078f6007a64c
  Args:
    type: :Person
    source: :Countess_Karoline_of_Ledebur_Wicheln
  AddTriple (87791de5-3d15-40f2-92b0-242c7d5e1f3e)
 Call ID: 87791de5-3d15-40f2-92b0-242c7d5e1f3e
  Args:
    source: :Princess_Barbara_Eleonore_Marie
    relation: :hasMother
    target: :Countess_Karoline_of_Ledebur_Wicheln
  Finish (5fa048f9-4cea-484f-8150-bb4df875bb83)
 Call ID: 5fa048f9-4cea-484f-8150-bb4df875bb83
  Args: