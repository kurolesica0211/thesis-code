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
Prince Gabriele of Bourbon-Two Sicilies (Gabriele Maria Giuseppe Carlo Ignazio Antonio Alfonso Pietro Giovanni Gerardo di Majella et Omni Sancti; 11 January 1897 – 22 October 1975) was a prince of the deposed dynasty which ruled the Kingdom of the Two Sicilies.
Family

Gabriel was the twelfth child and youngest son of Prince Alfonso, Count of Caserta, and his wife, Princess Maria Antonietta of Bourbon-Two Sicilies.
Marriage and issue

Gabriel married firstly Princess Malgorzata Izabella Czartoryska, daughter of Prince Adam Ludwik Czartoryski and Countess Maria Ludwika Krasińska, on 25 August 1927 in Paris.
The couple had one child before Malgorzata died in Cannes on 8 March 1929:


Gabriel married, secondly, Princess Cecylia Lubomirska, daughter of Prince Kasimierz Lubomirski and Countess Maria Theresia Granow-Wodicka, on 15 September 1932 in Kraków.



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
  AssignClass (e0169273-c1a7-4934-a351-2da0c8de6932)
 Call ID: e0169273-c1a7-4934-a351-2da0c8de6932
  Args:
    type: :Man
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AssignClass (670c4a7d-476a-450f-a7b8-029e025e9ef6)
 Call ID: 670c4a7d-476a-450f-a7b8-029e025e9ef6
  Args:
    type: :Person
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AddLiteral (7f04b2e7-7ac7-41b4-821b-ae8706567ac5)
 Call ID: 7f04b2e7-7ac7-41b4-821b-ae8706567ac5
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_value: 1897
    literal_type: xsd:integer
  AddLiteral (2d76f4b1-58e1-42f3-b929-acd9a530f60c)
 Call ID: 2d76f4b1-58e1-42f3-b929-acd9a530f60c
  Args:
    relation: :hasDeathYear
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1975
  AssignClass (5f2d8ff4-89b5-4205-989f-010d05b1aa04)
 Call ID: 5f2d8ff4-89b5-4205-989f-010d05b1aa04
  Args:
    type: :Man
    source: Prince_Alfonso_Count_of_Caserta
  AssignClass (c3365a16-7fc7-41fb-b840-78ad2d6fa4e3)
 Call ID: c3365a16-7fc7-41fb-b840-78ad2d6fa4e3
  Args:
    type: :Person
    source: Prince_Alfonso_Count_of_Caserta
  AssignClass (cefcd618-a50d-4a92-bded-46c753327b6c)
 Call ID: cefcd618-a50d-4a92-bded-46c753327b6c
  Args:
    type: :Woman
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (d710ace3-83c0-43b9-8a9a-7595d5e1b5f9)
 Call ID: d710ace3-83c0-43b9-8a9a-7595d5e1b5f9
  Args:
    type: :Person
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (df09f470-2cbf-4957-a20c-f409e705c089)
 Call ID: df09f470-2cbf-4957-a20c-f409e705c089
  Args:
    target: Prince_Alfonso_Count_of_Caserta
    relation: :hasFather
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AddTriple (133ca319-e6e9-4974-a290-c0e8424c42de)
 Call ID: 133ca319-e6e9-4974-a290-c0e8424c42de
  Args:
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AssignClass (c77253f0-14a9-44a4-90c7-856e4edebd70)
 Call ID: c77253f0-14a9-44a4-90c7-856e4edebd70
  Args:
    type: :Woman
    source: Princess_Malgorzata_Izabella_Czartoryska
  AssignClass (b2f95a3f-2440-4c13-85a2-31daf8576be8)
 Call ID: b2f95a3f-2440-4c13-85a2-31daf8576be8
  Args:
    type: :Person
    source: Princess_Malgorzata_Izabella_Czartoryska
  AddLiteral (1b175f89-782e-412b-a3a9-79b745330558)
 Call ID: 1b175f89-782e-412b-a3a9-79b745330558
  Args:
    relation: :hasMarriageYear
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1927
  AddTriple (e2c4094f-8bac-4dd5-91ba-1288a2f82d76)
 Call ID: e2c4094f-8bac-4dd5-91ba-1288a2f82d76
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Princess_Malgorzata_Izabella_Czartoryska
  AssignClass (19fd1233-dc3a-4423-843f-b0c92e7a990f)
 Call ID: 19fd1233-dc3a-4423-843f-b0c92e7a990f
  Args:
    type: :Man
    source: Prince_Adam_Ludwik_Czartoryski
  AssignClass (264e54f4-065b-4e6f-becd-ad110e9d7985)
 Call ID: 264e54f4-065b-4e6f-becd-ad110e9d7985
  Args:
    type: :Person
    source: Prince_Adam_Ludwik_Czartoryski
  AssignClass (1b9a261c-ecea-4602-874e-c3457484afa7)
 Call ID: 1b9a261c-ecea-4602-874e-c3457484afa7
  Args:
    type: :Woman
    source: Countess_Maria_Ludwika_Krasinska
  AssignClass (2d699e10-d34c-4c77-992e-1dc6530bb67a)
 Call ID: 2d699e10-d34c-4c77-992e-1dc6530bb67a
  Args:
    type: :Person
    source: Countess_Maria_Ludwika_Krasinska
  AddTriple (2f7d2fa5-31f0-4cac-9e87-6664062395c3)
 Call ID: 2f7d2fa5-31f0-4cac-9e87-6664062395c3
  Args:
    target: Prince_Adam_Ludwik_Czartoryski
    relation: :hasFather
    source: Princess_Malgorzata_Izabella_Czartoryska
  AddTriple (9859daaf-82b5-4455-92db-fa7b34c9d460)
 Call ID: 9859daaf-82b5-4455-92db-fa7b34c9d460
  Args:
    source: Princess_Malgorzata_Izabella_Czartoryska
    relation: :hasMother
    target: Countess_Maria_Ludwika_Krasinska
  AssignClass (b006e6f0-80b9-47c2-bce4-5c4e5fbebc28)
 Call ID: b006e6f0-80b9-47c2-bce4-5c4e5fbebc28
  Args:
    type: :Woman
    source: Princess_Cecylia_Lubomirska
  AssignClass (ba0212c6-0589-4e5e-acbc-9f83c15a3cf9)
 Call ID: ba0212c6-0589-4e5e-acbc-9f83c15a3cf9
  Args:
    type: :Person
    source: Princess_Cecylia_Lubomirska
  AddLiteral (5144a3c8-118a-49ea-8401-045806358af7)
 Call ID: 5144a3c8-118a-49ea-8401-045806358af7
  Args:
    literal_value: 1932
    literal_type: xsd:integer
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
  AddTriple (41a06420-ff33-4a46-9c93-9c254b969e22)
 Call ID: 41a06420-ff33-4a46-9c93-9c254b969e22
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: Princess_Cecylia_Lubomirska
    relation: :hasRelation
  AssignClass (13d1d837-5b2e-4cd6-b18c-85e5fbc75d71)
 Call ID: 13d1d837-5b2e-4cd6-b18c-85e5fbc75d71
  Args:
    type: :Man
    source: Prince_Kasimierz_Lubomirski
  AssignClass (ee6ae49a-475a-4890-97bd-915267da90fa)
 Call ID: ee6ae49a-475a-4890-97bd-915267da90fa
  Args:
    type: :Person
    source: Prince_Kasimierz_Lubomirski
  AssignClass (6c76e40f-cd46-4901-85a6-9914fef2da55)
 Call ID: 6c76e40f-cd46-4901-85a6-9914fef2da55
  Args:
    type: :Woman
    source: Countess_Maria_Theresia_Granow-Wodicka
  AssignClass (54129985-0763-4dae-a441-52d5d3364990)
 Call ID: 54129985-0763-4dae-a441-52d5d3364990
  Args:
    type: :Person
    source: Countess_Maria_Theresia_Granow-Wodicka
  AddTriple (ea857da2-d903-4ca0-80c9-fef4a10b196e)
 Call ID: ea857da2-d903-4ca0-80c9-fef4a10b196e
  Args:
    source: Princess_Cecylia_Lubomirska
    target: Prince_Kasimierz_Lubomirski
    relation: :hasFather
  AddTriple (cfb5618d-0ef3-4536-a1d5-f9581d0b3929)
 Call ID: cfb5618d-0ef3-4536-a1d5-f9581d0b3929
  Args:
    relation: :hasMother
    target: Countess_Maria_Theresia_Granow-Wodicka
    source: Princess_Cecylia_Lubomirska
  Finish (7892154f-70a2-4686-9449-66d985e19a8f)
 Call ID: 7892154f-70a2-4686-9449-66d985e19a8f
  Args: