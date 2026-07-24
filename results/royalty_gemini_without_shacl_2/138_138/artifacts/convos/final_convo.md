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
  AssignClass (791cc032-48a6-4a69-bdac-0226e048976e)
 Call ID: 791cc032-48a6-4a69-bdac-0226e048976e
  Args:
    type: :Man
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (08b4a14d-ad27-4999-8b28-82ad79119be4)
 Call ID: 08b4a14d-ad27-4999-8b28-82ad79119be4
  Args:
    type: :Man
    source: Prince_Paul_of_Yugoslavia
  AssignClass (8aa39ef5-2000-46b6-ad71-9cf502979924)
 Call ID: 8aa39ef5-2000-46b6-ad71-9cf502979924
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AddLiteral (fcf0b2a9-ca32-49ee-8004-765056aadf25)
 Call ID: fcf0b2a9-ca32-49ee-8004-765056aadf25
  Args:
    literal_type: xsd:positiveInteger
    source: Prince_Alexander_of_Yugoslavia
    literal_value: 1924
    relation: :hasBirthYear
  AddLiteral (caf8bb51-6c92-4025-91a0-c179e9bd34de)
 Call ID: caf8bb51-6c92-4025-91a0-c179e9bd34de
  Args:
    relation: :hasDeathYear
    literal_value: 2016
    literal_type: xsd:positiveInteger
    source: Prince_Alexander_of_Yugoslavia
  AddTriple (0a81c226-c561-4f75-a419-ce22a1636b9f)
 Call ID: 0a81c226-c561-4f75-a419-ce22a1636b9f
  Args:
    target: Prince_Paul_of_Yugoslavia
    relation: :hasFather
    source: Prince_Alexander_of_Yugoslavia
  AddTriple (8ff7742d-1404-421a-ae93-5bfc4bf9dea9)
 Call ID: 8ff7742d-1404-421a-ae93-5bfc4bf9dea9
  Args:
    target: Princess_Olga_of_Greece_and_Denmark
    relation: :hasMother
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (81625193-fe0b-472b-b667-f2232c9101cf)
 Call ID: 81625193-fe0b-472b-b667-f2232c9101cf
  Args:
    type: :Woman
    source: Princess_Maria_Pia_of_Savoy
  AddTriple (9a6e3044-783c-4965-983f-422b2ecc793d)
 Call ID: 9a6e3044-783c-4965-983f-422b2ecc793d
  Args:
    relation: :hasFather
    target: King_Umberto_II_of_Italy
    source: Princess_Maria_Pia_of_Savoy
  AssignClass (85cc1756-f2ef-4d0b-88f5-7836de97532b)
 Call ID: 85cc1756-f2ef-4d0b-88f5-7836de97532b
  Args:
    type: :Man
    source: King_Umberto_II_of_Italy
  AddTriple (cdd72144-8829-4eaa-b7ce-495c5b81c657)
 Call ID: cdd72144-8829-4eaa-b7ce-495c5b81c657
  Args:
    relation: :hasMother
    target: Princess_Marie_Jose_of_Belgium
    source: Princess_Maria_Pia_of_Savoy
  AssignClass (bfc7f505-8c17-4112-a523-4d29b83a980e)
 Call ID: bfc7f505-8c17-4112-a523-4d29b83a980e
  Args:
    type: :Woman
    source: Princess_Marie_Jose_of_Belgium
  AddLiteral (b65ece18-8618-4c27-aa06-d6fde3875c05)
 Call ID: b65ece18-8618-4c27-aa06-d6fde3875c05
  Args:
    source: Prince_Alexander_of_Yugoslavia
    literal_type: xsd:positiveInteger
    literal_value: 1955
    relation: :hasMarriageYear
  AddTriple (79f1629a-cd64-4cdf-ba6a-7c56cea9f58f)
 Call ID: 79f1629a-cd64-4cdf-ba6a-7c56cea9f58f
  Args:
    relation: :hasRelation
    target: Princess_Maria_Pia_of_Savoy
    source: Prince_Alexander_of_Yugoslavia
  AssignClass (bfd5b453-a063-4536-93b8-ddcfa731fdc7)
 Call ID: bfd5b453-a063-4536-93b8-ddcfa731fdc7
  Args:
    type: :Woman
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AddLiteral (f7ff707a-0a82-4e02-a387-b9b7afe2cfb3)
 Call ID: f7ff707a-0a82-4e02-a387-b9b7afe2cfb3
  Args:
    literal_type: xsd:positiveInteger
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    literal_value: 1942
    relation: :hasBirthYear
  AddTriple (bd5f8122-fe2f-44be-9779-097aafacae47)
 Call ID: bd5f8122-fe2f-44be-9779-097aafacae47
  Args:
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    target: Prince_Johannes_of_Liechtenstein
    relation: :hasFather
  AssignClass (62e17754-d1a4-44f5-a3c7-fca24dc900f0)
 Call ID: 62e17754-d1a4-44f5-a3c7-fca24dc900f0
  Args:
    type: :Man
    source: Prince_Johannes_of_Liechtenstein
  AddTriple (c990d71b-d122-4f19-ad34-4d09b50cfb02)
 Call ID: c990d71b-d122-4f19-ad34-4d09b50cfb02
  Args:
    relation: :hasMother
    target: Countess_Karoline_of_Ledebur_Wicheln
    source: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
  AssignClass (b6fe0294-a6d2-485f-ab74-76707e52be13)
 Call ID: b6fe0294-a6d2-485f-ab74-76707e52be13
  Args:
    type: :Woman
    source: Countess_Karoline_of_Ledebur_Wicheln
  AddLiteral (145d203e-a323-468e-9d6c-180fbea6f27e)
 Call ID: 145d203e-a323-468e-9d6c-180fbea6f27e
  Args:
    literal_type: xsd:positiveInteger
    source: Prince_Alexander_of_Yugoslavia
    literal_value: 1973
    relation: :hasMarriageYear
  AddTriple (80e27947-8122-4e42-b530-093be807d19e)
 Call ID: 80e27947-8122-4e42-b530-093be807d19e
  Args:
    source: Prince_Alexander_of_Yugoslavia
    target: Princess_Barbara_Eleonore_Marie_of_Liechtenstein
    relation: :hasRelation
  Finish (a7b486b0-14cf-4214-9282-c8c8ffe5a761)
 Call ID: a7b486b0-14cf-4214-9282-c8c8ffe5a761
  Args: