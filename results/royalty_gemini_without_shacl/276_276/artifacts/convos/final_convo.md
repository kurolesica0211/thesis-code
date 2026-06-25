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
  AssignClass (43df7cc8-34a2-44cd-93e3-e48b2921fdba)
 Call ID: 43df7cc8-34a2-44cd-93e3-e48b2921fdba
  Args:
    source: :Gabriele_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (af33aff9-a1ca-47d6-b3bf-fc89997288a6)
 Call ID: af33aff9-a1ca-47d6-b3bf-fc89997288a6
  Args:
    type: :Person
    source: :Gabriele_of_Bourbon-Two_Sicilies
  AddLiteral (6a33a90f-a0b2-472d-8b6b-69faa98113ba)
 Call ID: 6a33a90f-a0b2-472d-8b6b-69faa98113ba
  Args:
    literal_value: 1897
    relation: :hasBirthYear
    source: :Gabriele_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
  AddLiteral (3080e31b-7d24-43fc-a330-3c9080db907c)
 Call ID: 3080e31b-7d24-43fc-a330-3c9080db907c
  Args:
    source: :Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1975
  AssignClass (ed8a14d2-d144-4f9f-8d68-638b3fe621ff)
 Call ID: ed8a14d2-d144-4f9f-8d68-638b3fe621ff
  Args:
    type: :Man
    source: :Alfonso_Count_of_Caserta
  AssignClass (32d93edb-1a03-42ee-afbf-66892eb88460)
 Call ID: 32d93edb-1a03-42ee-afbf-66892eb88460
  Args:
    type: :Person
    source: :Alfonso_Count_of_Caserta
  AssignClass (a0a9a451-0cba-4114-be11-ce1d372490ea)
 Call ID: a0a9a451-0cba-4114-be11-ce1d372490ea
  Args:
    source: :Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (253e1f41-1464-4a9e-8eb1-3a71f79716a8)
 Call ID: 253e1f41-1464-4a9e-8eb1-3a71f79716a8
  Args:
    source: :Maria_Antonietta_of_Bourbon-Two_Sicilies
    type: :Person
  AddTriple (97680d4f-814c-4dbd-afa4-461f3c4baac1)
 Call ID: 97680d4f-814c-4dbd-afa4-461f3c4baac1
  Args:
    relation: :hasFather
    source: :Gabriele_of_Bourbon-Two_Sicilies
    target: :Alfonso_Count_of_Caserta
  AddTriple (136d2f79-3820-4dfd-92fe-0b8472222bf2)
 Call ID: 136d2f79-3820-4dfd-92fe-0b8472222bf2
  Args:
    target: :Maria_Antonietta_of_Bourbon-Two_Sicilies
    relation: :hasMother
    source: :Gabriele_of_Bourbon-Two_Sicilies
  AssignClass (aa8b1449-76c9-40c1-826c-eed4fae2b38e)
 Call ID: aa8b1449-76c9-40c1-826c-eed4fae2b38e
  Args:
    source: :Malgorzata_Izabella_Czartoryska
    type: :Woman
  AssignClass (c1e88e53-1cfb-4aa3-8805-42be50dec704)
 Call ID: c1e88e53-1cfb-4aa3-8805-42be50dec704
  Args:
    type: :Person
    source: :Malgorzata_Izabella_Czartoryska
  AddTriple (744d252a-1ca8-4adc-baa4-b64d97a50f51)
 Call ID: 744d252a-1ca8-4adc-baa4-b64d97a50f51
  Args:
    target: :Malgorzata_Izabella_Czartoryska
    relation: :hasRelation
    source: :Gabriele_of_Bourbon-Two_Sicilies
  AddLiteral (3088934a-6752-44a7-b107-3cabde000dde)
 Call ID: 3088934a-6752-44a7-b107-3cabde000dde
  Args:
    source: :Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1927
  AssignClass (5b36a9b8-57d9-42bc-bf92-1b71dfa0ede8)
 Call ID: 5b36a9b8-57d9-42bc-bf92-1b71dfa0ede8
  Args:
    type: :Man
    source: :Adam_Ludwik_Czartoryski
  AssignClass (59ae2184-0e2d-403d-9f49-7deaae96ec16)
 Call ID: 59ae2184-0e2d-403d-9f49-7deaae96ec16
  Args:
    type: :Person
    source: :Adam_Ludwik_Czartoryski
  AssignClass (a74f98b7-1ce9-408a-8a84-8c2424be667f)
 Call ID: a74f98b7-1ce9-408a-8a84-8c2424be667f
  Args:
    type: :Woman
    source: :Maria_Ludwika_Krasinska
  AssignClass (a92c6e9a-a144-4675-bd4e-6a102ee2fc8e)
 Call ID: a92c6e9a-a144-4675-bd4e-6a102ee2fc8e
  Args:
    type: :Person
    source: :Maria_Ludwika_Krasinska
  AddTriple (fb57cbf0-cc8b-4fcc-adcb-bf9350243fce)
 Call ID: fb57cbf0-cc8b-4fcc-adcb-bf9350243fce
  Args:
    target: :Adam_Ludwik_Czartoryski
    source: :Malgorzata_Izabella_Czartoryska
    relation: :hasFather
  AddTriple (14e565ab-c3f0-4b27-a561-bb67f445f64f)
 Call ID: 14e565ab-c3f0-4b27-a561-bb67f445f64f
  Args:
    target: :Maria_Ludwika_Krasinska
    source: :Malgorzata_Izabella_Czartoryska
    relation: :hasMother
  AddLiteral (6f5a8cf4-86f8-4409-89f9-a31f452ceca8)
 Call ID: 6f5a8cf4-86f8-4409-89f9-a31f452ceca8
  Args:
    literal_value: 1929
    literal_type: xsd:integer
    source: :Malgorzata_Izabella_Czartoryska
    relation: :hasDeathYear
  AssignClass (61b37c9d-f9b8-4274-85cb-52af38a40a0d)
 Call ID: 61b37c9d-f9b8-4274-85cb-52af38a40a0d
  Args:
    source: :Cecylia_Lubomirska
    type: :Woman
  AssignClass (a5102677-9be9-4196-bb5d-a986d2960a6b)
 Call ID: a5102677-9be9-4196-bb5d-a986d2960a6b
  Args:
    type: :Person
    source: :Cecylia_Lubomirska
  AddTriple (6de9988e-3ed4-469d-b869-c888f5bec226)
 Call ID: 6de9988e-3ed4-469d-b869-c888f5bec226
  Args:
    target: :Cecylia_Lubomirska
    source: :Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (def7c3e7-83fb-494a-a7b9-3edaeeb17f50)
 Call ID: def7c3e7-83fb-494a-a7b9-3edaeeb17f50
  Args:
    literal_value: 1932
    source: :Gabriele_of_Bourbon-Two_Sicilies
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (33fe48ef-0f21-490f-9a38-fa7773b02a77)
 Call ID: 33fe48ef-0f21-490f-9a38-fa7773b02a77
  Args:
    type: :Man
    source: :Kasimierz_Lubomirski
  AssignClass (c32f6724-5954-4680-a760-e9430e5f5f0a)
 Call ID: c32f6724-5954-4680-a760-e9430e5f5f0a
  Args:
    type: :Person
    source: :Kasimierz_Lubomirski
  AssignClass (20f427c2-f89c-4999-8621-0ebbe2e86c2a)
 Call ID: 20f427c2-f89c-4999-8621-0ebbe2e86c2a
  Args:
    source: :Maria_Theresia_Granow-Wodicka
    type: :Woman
  AssignClass (ad9ed260-5259-417b-91d9-ac5d91e4d7d6)
 Call ID: ad9ed260-5259-417b-91d9-ac5d91e4d7d6
  Args:
    source: :Maria_Theresia_Granow-Wodicka
    type: :Person
  AddTriple (050491f9-e5d2-4e24-b60b-541c22f42a5b)
 Call ID: 050491f9-e5d2-4e24-b60b-541c22f42a5b
  Args:
    target: :Kasimierz_Lubomirski
    source: :Cecylia_Lubomirska
    relation: :hasFather
  AddTriple (fa7bba20-bd83-4f4a-8cc0-ffdae69333ad)
 Call ID: fa7bba20-bd83-4f4a-8cc0-ffdae69333ad
  Args:
    target: :Maria_Theresia_Granow-Wodicka
    source: :Cecylia_Lubomirska
    relation: :hasMother
  Finish (259762f0-b060-4c0f-848f-cdea8945f7a1)
 Call ID: 259762f0-b060-4c0f-848f-cdea8945f7a1
  Args: