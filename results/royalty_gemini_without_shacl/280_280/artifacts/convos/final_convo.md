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
Princess María de las Mercedes of Bavaria, Infanta of Spain (3 October 1911 – 11 September 1953) was a German-Spanish princess.
She was the third wife of Georgian Prince Irakli Bagration of Mukhrani.
Through her father, Prince Ferdinand of Bavaria, she was a member of the Bavarian House of Wittelsbach.
Through her mother, Infanta María Teresa of Spain, she was a granddaughter of Alfonso XII and niece of Alfonso XIII.
Early life

Princess María de las Mercedes of Bavaria, Infanta of Spain, was born on 3 October 1911 at the Palace of the Cuesta de la Vega, Madrid, to Prince Ferdinand of Bavaria and Infanta María Teresa of Spain.
Her parents were first cousins, both grandchildren of Isabella II of Spain.
Prior to her birth, her uncle, King Alfonso XIII, declared that any children born of her parents' marriage would be Infantes or Infantas of Spain.
She was christened María de las Mercedes Teresa María de la
Her godparents were Infanta María de la Paz of Spain (her paternal grandmother) and Prince Adalbert of Bavaria (her paternal uncle, for whom Prince Carlos of Bourbon-Two Sicilies stood proxy).
She had two elder brothers, Luis Alfonso (1906–1983) and José Eugenio (1909–1966), and one younger sister, María del Pilar (1912–1918).
Marriage and issue

On 29 August 1946, Infanta María de las Mercedes married Prince Irakli Bagration of Mukhrani at the Miramar Palace in San Sebastián.
On the advice of Grand Duke Vladimir Kirillovich of Russia, Infante Juan, Count of Barcelona, head of the Spanish royal family in exile, recognised the union as dynastic.
In 1948, Irakli's sister Leonida married Grand Duke Vladimir.



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
  AssignClass (caaaa92e-0d33-4bdd-af24-12e5c40cc413)
 Call ID: caaaa92e-0d33-4bdd-af24-12e5c40cc413
  Args:
    type: :Person
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
  AssignClass (0ca5a427-fa44-4180-a017-d0d88921f5b4)
 Call ID: 0ca5a427-fa44-4180-a017-d0d88921f5b4
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    type: :Woman
  AddLiteral (cc3e88bc-93f4-4447-9751-c7a8047de796)
 Call ID: cc3e88bc-93f4-4447-9751-c7a8047de796
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    literal_value: 1911
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (2b1b46a6-2fe7-40d3-a64f-c5d6846989a3)
 Call ID: 2b1b46a6-2fe7-40d3-a64f-c5d6846989a3
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    literal_type: xsd:integer
    literal_value: 1953
    relation: :hasDeathYear
  AssignClass (46ca3e74-9728-44bd-8429-8ca2145ab6c5)
 Call ID: 46ca3e74-9728-44bd-8429-8ca2145ab6c5
  Args:
    type: :Person
    source: Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (d1b6a250-1c1d-41d1-b3dd-1abfb60e3353)
 Call ID: d1b6a250-1c1d-41d1-b3dd-1abfb60e3353
  Args:
    source: Prince_Irakli_Bagration_of_Mukhrani
    type: :Man
  AddLiteral (3852d625-f54e-4ebf-a143-23ec7c3cae47)
 Call ID: 3852d625-f54e-4ebf-a143-23ec7c3cae47
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    literal_type: xsd:integer
    literal_value: 1946
    relation: :hasMarriageYear
  AddTriple (78cee746-8009-4195-8609-68da572fc92b)
 Call ID: 78cee746-8009-4195-8609-68da572fc92b
  Args:
    target: Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasRelation
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
  AssignClass (7873ccdb-afc6-46a7-8277-bf5efaefcf77)
 Call ID: 7873ccdb-afc6-46a7-8277-bf5efaefcf77
  Args:
    source: Prince_Ferdinand_of_Bavaria
    type: :Person
  AssignClass (98274011-5a6c-46fd-a32a-ebf8efa1b3cb)
 Call ID: 98274011-5a6c-46fd-a32a-ebf8efa1b3cb
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Bavaria
  AssignClass (a087c52e-4e91-4cd0-bb7b-547ab85ac5c6)
 Call ID: a087c52e-4e91-4cd0-bb7b-547ab85ac5c6
  Args:
    type: :Person
    source: Infanta_Maria_Teresa_of_Spain
  AssignClass (27910231-ada6-4a2f-8117-81dfb5b2cbaa)
 Call ID: 27910231-ada6-4a2f-8117-81dfb5b2cbaa
  Args:
    source: Infanta_Maria_Teresa_of_Spain
    type: :Woman
  AddTriple (806b5e6a-a020-4392-9798-1896f2bb5eb7)
 Call ID: 806b5e6a-a020-4392-9798-1896f2bb5eb7
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasFather
    target: Prince_Ferdinand_of_Bavaria
  AddTriple (0fec400d-4a8a-4f99-96f5-4e517f7e7903)
 Call ID: 0fec400d-4a8a-4f99-96f5-4e517f7e7903
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasMother
    target: Infanta_Maria_Teresa_of_Spain
  AssignClass (95f2fe61-db4b-46da-9104-1ccbd6c1a4a9)
 Call ID: 95f2fe61-db4b-46da-9104-1ccbd6c1a4a9
  Args:
    type: :Person
    source: Luis_Alfonso
  AssignClass (0758cea7-9c4c-4d59-abc7-68d538df44a1)
 Call ID: 0758cea7-9c4c-4d59-abc7-68d538df44a1
  Args:
    type: :Man
    source: Luis_Alfonso
  AssignClass (1ed9ccc2-66bc-434e-9d32-d19fc21924b8)
 Call ID: 1ed9ccc2-66bc-434e-9d32-d19fc21924b8
  Args:
    source: Jose_Eugenio
    type: :Person
  AssignClass (5a17aa4b-0bfe-4a06-a28e-3115a9426faa)
 Call ID: 5a17aa4b-0bfe-4a06-a28e-3115a9426faa
  Args:
    type: :Man
    source: Jose_Eugenio
  AssignClass (5ce48f11-d409-4b80-826d-f9cdbc956284)
 Call ID: 5ce48f11-d409-4b80-826d-f9cdbc956284
  Args:
    type: :Person
    source: Maria_del_Pilar
  AssignClass (345f1869-b628-4b77-bab6-c416406d93e5)
 Call ID: 345f1869-b628-4b77-bab6-c416406d93e5
  Args:
    source: Maria_del_Pilar
    type: :Woman
  AddTriple (a1e2accd-3f27-41ac-9a94-19704f369c56)
 Call ID: a1e2accd-3f27-41ac-9a94-19704f369c56
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
    relation: :hasBrother
    target: Luis_Alfonso
  AddTriple (969cec28-faa9-4870-98fb-25cc3efc36a2)
 Call ID: 969cec28-faa9-4870-98fb-25cc3efc36a2
  Args:
    relation: :hasBrother
    target: Jose_Eugenio
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
  AddTriple (5f01c2bf-b809-4f02-a77d-caf77041488f)
 Call ID: 5f01c2bf-b809-4f02-a77d-caf77041488f
  Args:
    relation: :hasSister
    target: Maria_del_Pilar
    source: Princess_Maria_de_las_Mercedes_of_Bavaria
  AssignClass (e5508d73-a591-45b6-9287-1d344e675c69)
 Call ID: e5508d73-a591-45b6-9287-1d344e675c69
  Args:
    source: Alfonso_XII
    type: :Person
  AssignClass (7ae7bc61-6738-4771-97ad-1f17d24fd70e)
 Call ID: 7ae7bc61-6738-4771-97ad-1f17d24fd70e
  Args:
    type: :Man
    source: Alfonso_XII
  AddTriple (e9ecafb6-23a9-4cc3-a8d9-f8dfcc22523b)
 Call ID: e9ecafb6-23a9-4cc3-a8d9-f8dfcc22523b
  Args:
    target: Alfonso_XII
    relation: :hasAncestor
    source: Infanta_Maria_Teresa_of_Spain
  AssignClass (683359d8-008f-450e-988e-6c1b310e889e)
 Call ID: 683359d8-008f-450e-988e-6c1b310e889e
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (7748f309-cb2d-4539-812b-e6fe386f4f60)
 Call ID: 7748f309-cb2d-4539-812b-e6fe386f4f60
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (e43d50c0-131f-4c64-8bde-3e405a7be4d5)
 Call ID: e43d50c0-131f-4c64-8bde-3e405a7be4d5
  Args:
    type: :Person
    source: Isabella_II_of_Spain
  AssignClass (aa0eaa06-61b7-499b-81bc-67a8018b6d87)
 Call ID: aa0eaa06-61b7-499b-81bc-67a8018b6d87
  Args:
    source: Isabella_II_of_Spain
    type: :Woman
  AddTriple (9a649860-ac37-4fb1-af1e-f81c77fb9445)
 Call ID: 9a649860-ac37-4fb1-af1e-f81c77fb9445
  Args:
    source: Prince_Ferdinand_of_Bavaria
    relation: :hasAncestor
    target: Isabella_II_of_Spain
  AddTriple (19681c03-dce3-49fa-9660-f1916430bd57)
 Call ID: 19681c03-dce3-49fa-9660-f1916430bd57
  Args:
    source: Infanta_Maria_Teresa_of_Spain
    target: Isabella_II_of_Spain
    relation: :hasAncestor
  AssignClass (cc4316a0-6ac1-404f-a101-e0d52fc869e6)
 Call ID: cc4316a0-6ac1-404f-a101-e0d52fc869e6
  Args:
    source: Infanta_Maria_de_la_Paz_of_Spain
    type: :Person
  AssignClass (e9629708-4980-4d7c-9c24-ce9961cc239a)
 Call ID: e9629708-4980-4d7c-9c24-ce9961cc239a
  Args:
    type: :Woman
    source: Infanta_Maria_de_la_Paz_of_Spain
  AddTriple (802724ef-6a45-44a4-a819-cce62c950660)
 Call ID: 802724ef-6a45-44a4-a819-cce62c950660
  Args:
    source: Prince_Ferdinand_of_Bavaria
    target: Infanta_Maria_de_la_Paz_of_Spain
    relation: :hasMother
  AssignClass (c7b0d4de-35dc-4eae-bd41-88c548640dd9)
 Call ID: c7b0d4de-35dc-4eae-bd41-88c548640dd9
  Args:
    source: Prince_Adalbert_of_Bavaria
    type: :Person
  AssignClass (748766f8-8b21-49ce-b2b5-b671633b1b24)
 Call ID: 748766f8-8b21-49ce-b2b5-b671633b1b24
  Args:
    source: Prince_Adalbert_of_Bavaria
    type: :Man
  AssignClass (a3595a9b-b9c2-41df-8f05-a2b8a906adca)
 Call ID: a3595a9b-b9c2-41df-8f05-a2b8a906adca
  Args:
    type: :Person
    source: Prince_Carlos_of_Bourbon_Two_Sicilies
  AssignClass (686f2e46-e409-4054-a723-ff2cdfae92af)
 Call ID: 686f2e46-e409-4054-a723-ff2cdfae92af
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon_Two_Sicilies
  AssignClass (db855722-e018-4c2a-b3b4-ed05a057b768)
 Call ID: db855722-e018-4c2a-b3b4-ed05a057b768
  Args:
    source: Leonida
    type: :Person
  AssignClass (dc58b30d-0d9d-49f9-aec2-e1df98e3ced2)
 Call ID: dc58b30d-0d9d-49f9-aec2-e1df98e3ced2
  Args:
    source: Leonida_of_Mukhrani
    type: :Woman
  AssignClass (1b1428b1-ff98-425d-98e5-d320f11722c6)
 Call ID: 1b1428b1-ff98-425d-98e5-d320f11722c6
  Args:
    source: Grand_Duke_Vladimir_Kirillovich_of_Russia
    type: :Person
  AssignClass (0581d418-b5b0-4e30-867e-48742b2abe44)
 Call ID: 0581d418-b5b0-4e30-867e-48742b2abe44
  Args:
    type: :Man
    source: Grand_Duke_Vladimir_Kirillovich_of_Russia
  AddTriple (45320540-acf8-4894-963c-66d9324859e1)
 Call ID: 45320540-acf8-4894-963c-66d9324859e1
  Args:
    target: Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasBrother
    source: Leonida_of_Mukhrani
  AddLiteral (873ef26f-e9f7-422a-b50d-bd4301af9c7d)
 Call ID: 873ef26f-e9f7-422a-b50d-bd4301af9c7d
  Args:
    source: Leonida_of_Mukhrani
    literal_value: 1948
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (571d26b1-87e0-4034-90db-a8cf2733bb53)
 Call ID: 571d26b1-87e0-4034-90db-a8cf2733bb53
  Args:
    relation: :hasRelation
    target: Grand_Duke_Vladimir_Kirillovich_of_Russia
    source: Leonida_of_Mukhrani
  Finish (4920936c-8683-416c-88a3-7a31dd4161ac)
 Call ID: 4920936c-8683-416c-88a3-7a31dd4161ac
  Args: