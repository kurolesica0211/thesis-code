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
  AssignClass (8301b797-54e5-48a6-8524-1418d5ff0310)
 Call ID: 8301b797-54e5-48a6-8524-1418d5ff0310
  Args:
    type: :Man
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
  AssignClass (95b8278f-d62e-420b-bf7e-5b91dec12725)
 Call ID: 95b8278f-d62e-420b-bf7e-5b91dec12725
  Args:
    type: :Person
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
  AddLiteral (004127b2-af95-47fd-aa5e-9a5d5eb413a2)
 Call ID: 004127b2-af95-47fd-aa5e-9a5d5eb413a2
  Args:
    relation: :hasBirthYear
    literal_value: 1897
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (bf28c9d5-96b9-48f2-bd25-97f4bdb8fd5f)
 Call ID: bf28c9d5-96b9-48f2-bd25-97f4bdb8fd5f
  Args:
    literal_type: xsd:integer
    literal_value: 1975
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
  AssignClass (0c1f3b85-b3b0-4ccf-b229-04e929c85375)
 Call ID: 0c1f3b85-b3b0-4ccf-b229-04e929c85375
  Args:
    type: :Man
    source: :Prince_Alfonso_Count_of_Caserta
  AssignClass (b7b64087-ab45-40fa-bb9b-641bf25eabc4)
 Call ID: b7b64087-ab45-40fa-bb9b-641bf25eabc4
  Args:
    type: :Person
    source: :Prince_Alfonso_Count_of_Caserta
  AssignClass (6a282b86-b78e-4ad6-8755-20b50f66eff8)
 Call ID: 6a282b86-b78e-4ad6-8755-20b50f66eff8
  Args:
    type: :Woman
    source: :Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (b78efbe5-edf7-4c1c-a877-d360a767c846)
 Call ID: b78efbe5-edf7-4c1c-a877-d360a767c846
  Args:
    type: :Person
    source: :Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (f7f69846-546b-4a5f-962c-187451e0c2a5)
 Call ID: f7f69846-546b-4a5f-962c-187451e0c2a5
  Args:
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: :Prince_Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (96a654fd-b982-45c7-bad2-7cb29411027f)
 Call ID: 96a654fd-b982-45c7-bad2-7cb29411027f
  Args:
    relation: :hasMother
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: :Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (40b21228-6786-4007-aa17-b7bd1109180f)
 Call ID: 40b21228-6786-4007-aa17-b7bd1109180f
  Args:
    type: :Woman
    source: :Princess_Malgorzata_Izabella_Czartoryska
  AssignClass (6ba7ca2e-3f74-46a6-92b3-f235e1ee9061)
 Call ID: 6ba7ca2e-3f74-46a6-92b3-f235e1ee9061
  Args:
    type: :Person
    source: :Princess_Malgorzata_Izabella_Czartoryska
  AddTriple (b6825210-5747-4dd0-90bf-f7b6e398888f)
 Call ID: b6825210-5747-4dd0-90bf-f7b6e398888f
  Args:
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: :Princess_Malgorzata_Izabella_Czartoryska
    relation: :hasRelation
  AddLiteral (273868ab-6667-4497-914c-d30e5fd41688)
 Call ID: 273868ab-6667-4497-914c-d30e5fd41688
  Args:
    literal_type: xsd:integer
    literal_value: 1927
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
  AssignClass (f512c17a-da38-4530-b0c4-3973cf81527a)
 Call ID: f512c17a-da38-4530-b0c4-3973cf81527a
  Args:
    type: :Man
    source: :Prince_Adam_Ludwik_Czartoryski
  AssignClass (c74082b8-8b0a-4247-8b4d-1c7c28151bdd)
 Call ID: c74082b8-8b0a-4247-8b4d-1c7c28151bdd
  Args:
    type: :Person
    source: :Prince_Adam_Ludwik_Czartoryski
  AssignClass (efacea72-7fd1-41d9-8d94-7459c545a705)
 Call ID: efacea72-7fd1-41d9-8d94-7459c545a705
  Args:
    type: :Woman
    source: :Countess_Maria_Ludwika_Krasinska
  AssignClass (c05314eb-51eb-4340-b920-d9e0f810189b)
 Call ID: c05314eb-51eb-4340-b920-d9e0f810189b
  Args:
    type: :Person
    source: :Countess_Maria_Ludwika_Krasinska
  AddTriple (b8a44dfa-3d30-4f73-8a56-fe6e3c5276d2)
 Call ID: b8a44dfa-3d30-4f73-8a56-fe6e3c5276d2
  Args:
    relation: :hasFather
    target: :Prince_Adam_Ludwik_Czartoryski
    source: :Princess_Malgorzata_Izabella_Czartoryska
  AddTriple (cc3fdc1b-81c5-4c3d-8119-7499739d3251)
 Call ID: cc3fdc1b-81c5-4c3d-8119-7499739d3251
  Args:
    relation: :hasMother
    target: :Countess_Maria_Ludwika_Krasinska
    source: :Princess_Malgorzata_Izabella_Czartoryska
  AssignClass (fca1ba50-da9f-435d-9dc1-ef2f59b1ec45)
 Call ID: fca1ba50-da9f-435d-9dc1-ef2f59b1ec45
  Args:
    type: :Woman
    source: :Princess_Cecylia_Lubomirska
  AssignClass (13f0ea17-632a-4073-85b4-418a205e592a)
 Call ID: 13f0ea17-632a-4073-85b4-418a205e592a
  Args:
    type: :Person
    source: :Princess_Cecylia_Lubomirska
  AddTriple (ef583bfd-c36b-40a2-b866-4a93134aa4f5)
 Call ID: ef583bfd-c36b-40a2-b866-4a93134aa4f5
  Args:
    target: :Princess_Cecylia_Lubomirska
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (e9a84a8e-d4bc-4aa3-aab0-e39d76031486)
 Call ID: e9a84a8e-d4bc-4aa3-aab0-e39d76031486
  Args:
    source: :Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1932
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (1abc15b7-a6b7-4bd4-9dbe-8b78eb373392)
 Call ID: 1abc15b7-a6b7-4bd4-9dbe-8b78eb373392
  Args:
    type: :Man
    source: :Prince_Kasimierz_Lubomirski
  AssignClass (4cab836f-0848-435d-8c94-6564a6463bd2)
 Call ID: 4cab836f-0848-435d-8c94-6564a6463bd2
  Args:
    type: :Person
    source: :Prince_Kasimierz_Lubomirski
  AssignClass (bd5e7a79-9784-4461-8ee4-7f335c3615f0)
 Call ID: bd5e7a79-9784-4461-8ee4-7f335c3615f0
  Args:
    type: :Woman
    source: :Countess_Maria_Theresia_Granow-Wodicka
  AssignClass (9377134a-a155-4875-a0f2-bb45372eef50)
 Call ID: 9377134a-a155-4875-a0f2-bb45372eef50
  Args:
    type: :Person
    source: :Countess_Maria_Theresia_Granow-Wodicka
  AddTriple (f5924eb4-8d9d-4616-941b-5898521d4a2f)
 Call ID: f5924eb4-8d9d-4616-941b-5898521d4a2f
  Args:
    target: :Prince_Kasimierz_Lubomirski
    source: :Princess_Cecylia_Lubomirska
    relation: :hasFather
  AddTriple (75cb4174-9985-4c08-a1ac-a2103f65f10d)
 Call ID: 75cb4174-9985-4c08-a1ac-a2103f65f10d
  Args:
    relation: :hasMother
    source: :Princess_Cecylia_Lubomirska
    target: :Countess_Maria_Theresia_Granow-Wodicka
  Finish (f233e0fc-f8f0-440c-85ab-177fd3658ff3)
 Call ID: f233e0fc-f8f0-440c-85ab-177fd3658ff3
  Args: