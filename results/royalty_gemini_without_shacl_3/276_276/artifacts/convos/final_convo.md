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
  AssignClass (43f8ad58-356c-4fb7-9f45-bb0c16d42f3b)
 Call ID: 43f8ad58-356c-4fb7-9f45-bb0c16d42f3b
  Args:
    type: :Man
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AssignClass (ac9b9d05-d34b-46bd-9a5a-b3d1040e51b5)
 Call ID: ac9b9d05-d34b-46bd-9a5a-b3d1040e51b5
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (1fc466ec-4a4f-445d-9608-5977b6354ec1)
 Call ID: 1fc466ec-4a4f-445d-9608-5977b6354ec1
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1897
  AddLiteral (ea101e35-a856-4a8d-aa2e-a58ee92de3f7)
 Call ID: ea101e35-a856-4a8d-aa2e-a58ee92de3f7
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1975
  AssignClass (e8bf6cb1-695f-4d9d-b4f9-0a803a6e0187)
 Call ID: e8bf6cb1-695f-4d9d-b4f9-0a803a6e0187
  Args:
    source: Prince_Alfonso_Count_of_Caserta
    type: :Man
  AssignClass (e1a1e68b-5756-47af-aea2-f7c8a977f22e)
 Call ID: e1a1e68b-5756-47af-aea2-f7c8a977f22e
  Args:
    source: Prince_Alfonso_Count_of_Caserta
    type: :Person
  AssignClass (924d0f28-76db-4365-ad2c-619bd4a12d2e)
 Call ID: 924d0f28-76db-4365-ad2c-619bd4a12d2e
  Args:
    type: :Woman
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AssignClass (4cbb2648-180c-49e0-8df0-a109120c113a)
 Call ID: 4cbb2648-180c-49e0-8df0-a109120c113a
  Args:
    type: :Person
    source: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
  AddTriple (39898f27-846d-4f2f-a89e-c0df8769031e)
 Call ID: 39898f27-846d-4f2f-a89e-c0df8769031e
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: Prince_Alfonso_Count_of_Caserta
    relation: :hasFather
  AddTriple (efdc7a79-a135-4e48-a6ee-ae4f14b0f45f)
 Call ID: efdc7a79-a135-4e48-a6ee-ae4f14b0f45f
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    target: Princess_Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
  AssignClass (8c522587-ebf2-47c4-a1b0-c30a8b2c6826)
 Call ID: 8c522587-ebf2-47c4-a1b0-c30a8b2c6826
  Args:
    source: Princess_Malgorzata_Izabella_Czartoryska
    type: :Woman
  AssignClass (d58b1838-7140-4bd9-8d5e-20ac1aa9621b)
 Call ID: d58b1838-7140-4bd9-8d5e-20ac1aa9621b
  Args:
    type: :Person
    source: Princess_Malgorzata_Izabella_Czartoryska
  AddLiteral (ded01758-e9b8-481a-80d2-1f3aed62f1d9)
 Call ID: ded01758-e9b8-481a-80d2-1f3aed62f1d9
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1927
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AddTriple (d58c2cae-cead-4959-8c38-ba5b50355ecd)
 Call ID: d58c2cae-cead-4959-8c38-ba5b50355ecd
  Args:
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasRelation
    target: Princess_Malgorzata_Izabella_Czartoryska
  AssignClass (aa19987c-efc2-4637-aecd-1df42c7212b1)
 Call ID: aa19987c-efc2-4637-aecd-1df42c7212b1
  Args:
    type: :Man
    source: Prince_Adam_Ludwik_Czartoryski
  AssignClass (ffa357c1-bbef-4a56-b708-764a13fb3ad3)
 Call ID: ffa357c1-bbef-4a56-b708-764a13fb3ad3
  Args:
    source: Prince_Adam_Ludwik_Czartoryski
    type: :Person
  AssignClass (fbe1099c-ab6b-424f-9028-a2f1937e24d0)
 Call ID: fbe1099c-ab6b-424f-9028-a2f1937e24d0
  Args:
    type: :Woman
    source: Countess_Maria_Ludwika_Krasinska
  AssignClass (267d1a40-c194-497a-a43c-f641a75141a7)
 Call ID: 267d1a40-c194-497a-a43c-f641a75141a7
  Args:
    source: Countess_Maria_Ludwika_Krasinska
    type: :Person
  AddTriple (86e8c4e4-2038-46ed-a601-0bd58527bab4)
 Call ID: 86e8c4e4-2038-46ed-a601-0bd58527bab4
  Args:
    target: Prince_Adam_Ludwik_Czartoryski
    relation: :hasFather
    source: Princess_Malgorzata_Izabella_Czartoryska
  AddTriple (193bc6bd-4e5b-472d-b650-4134fcae6cf8)
 Call ID: 193bc6bd-4e5b-472d-b650-4134fcae6cf8
  Args:
    source: Princess_Malgorzata_Izabella_Czartoryska
    relation: :hasMother
    target: Countess_Maria_Ludwika_Krasinska
  AssignClass (9d69aab3-4b24-404b-826e-98c80384828b)
 Call ID: 9d69aab3-4b24-404b-826e-98c80384828b
  Args:
    source: Princess_Cecylia_Lubomirska
    type: :Woman
  AssignClass (eb8f9d23-40a9-40f2-aa8c-33ca284e85f1)
 Call ID: eb8f9d23-40a9-40f2-aa8c-33ca284e85f1
  Args:
    type: :Person
    source: Princess_Cecylia_Lubomirska
  AddLiteral (dba5944a-c0ff-4a4b-b47a-27da087cb7b0)
 Call ID: dba5944a-c0ff-4a4b-b47a-27da087cb7b0
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
    literal_value: 1932
  AddTriple (e09414be-ff45-4a71-a599-4068f65aa4e0)
 Call ID: e09414be-ff45-4a71-a599-4068f65aa4e0
  Args:
    relation: :hasRelation
    target: Princess_Cecylia_Lubomirska
    source: Prince_Gabriele_of_Bourbon-Two_Sicilies
  AssignClass (6ee52961-300d-4bcd-95ed-6f6ad6c47c5e)
 Call ID: 6ee52961-300d-4bcd-95ed-6f6ad6c47c5e
  Args:
    source: Prince_Kasimierz_Lubomirski
    type: :Man
  AssignClass (5c91c5cd-66cb-4220-9e5e-cbdad8509887)
 Call ID: 5c91c5cd-66cb-4220-9e5e-cbdad8509887
  Args:
    type: :Person
    source: Prince_Kasimierz_Lubomirski
  AssignClass (acd4bb7c-f770-410f-aeca-53566dde0c7d)
 Call ID: acd4bb7c-f770-410f-aeca-53566dde0c7d
  Args:
    type: :Woman
    source: Countess_Maria_Theresia_Granow-Wodicka
  AssignClass (30d45275-551a-40cf-8ec9-4cbfd9cfe6f7)
 Call ID: 30d45275-551a-40cf-8ec9-4cbfd9cfe6f7
  Args:
    source: Countess_Maria_Theresia_Granow-Wodicka
    type: :Person
  AddTriple (1d803d82-bc42-4523-96ed-c6c0459f160a)
 Call ID: 1d803d82-bc42-4523-96ed-c6c0459f160a
  Args:
    relation: :hasFather
    target: Prince_Kasimierz_Lubomirski
    source: Princess_Cecylia_Lubomirska
  AddTriple (b64128db-ba66-48fc-850d-ef5af6fbbb51)
 Call ID: b64128db-ba66-48fc-850d-ef5af6fbbb51
  Args:
    relation: :hasMother
    target: Countess_Maria_Theresia_Granow-Wodicka
    source: Princess_Cecylia_Lubomirska
  Finish (2df37254-5d9a-46b5-8f87-cfa206d1491a)
 Call ID: 2df37254-5d9a-46b5-8f87-cfa206d1491a
  Args: