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
Prince Karl of Leiningen (Karl Vladimir Ernst Heinrich; 2 January 1928 – 28 September 1990) was the second son of Karl, 6th Prince of Leiningen (1898–1946), and Grand Duchess Maria Kirillovna of Russia.
She was the elder daughter of Grand Duke Kirill Vladimirovich of Russia and Princess Victoria Melita of Edinburgh.
As such, Karl was a great-great-grandson of both Queen Victoria of the United Kingdom and Emperor Alexander II of Russia (as Victoria Melita and Kirill Vladimirovich were both grandchildren of Alexander II).
Biography

Career

Born in Coburg, Germany, he worked mainly as a salesman in Paris as a young man.
With his wife, Karl subsequently resolved to take up a business career in Toronto, Canada.
Marriage and issue

Karl met Princess Marie Louise of Bulgaria in Madrid, where she was living with her mother.
She was the only daughter of Boris III of Bulgaria by his wife Princess Giovanna of Italy.
Karl announced his engagement to Marie Louise in December 1956.
Amorbach had been the residence of the House of Leiningen since 1803, and the town's streets were lined with hundreds of cheering spectators; Karl's family owns huge estates in South Germany, and was considered to be one of the wealthiest of Germany's noble families.
Karl traveled to Canada early in their marriage, and the couple decided to settle there.
The marriage produced two sons:


The marriage was unhappy, and Karl and Marie Louise divorced on 4 December 1968.
Later in life, Karl reminisced, "Princes are expected to marry princesses, so I married Marie-Louise, the daughter of Bulgarian ex-King Boris III".
Later life

Karl eventually became a naturalized Canadian citizen.
Persuaded by some Jewish friends to visit Israel, Karl eventually found a job through the help of new-found Israeli friends.



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
  AssignClass (0fb3975c-cace-4032-a9c1-171de6ee33a7)
 Call ID: 0fb3975c-cace-4032-a9c1-171de6ee33a7
  Args:
    source: Karl_of_Leiningen
    type: :Man
  AssignClass (1934bfaf-fd75-47b6-a0a0-d07e4ec4d41d)
 Call ID: 1934bfaf-fd75-47b6-a0a0-d07e4ec4d41d
  Args:
    type: :Person
    source: Karl_of_Leiningen
  AddLiteral (23d1d598-dde4-495d-a0b1-632d4b1bfc07)
 Call ID: 23d1d598-dde4-495d-a0b1-632d4b1bfc07
  Args:
    relation: :hasBirthYear
    literal_value: 1928
    source: Karl_of_Leiningen
    literal_type: xsd:integer
  AddLiteral (a1b13f3e-869c-4fb0-9579-23d3a3cae66c)
 Call ID: a1b13f3e-869c-4fb0-9579-23d3a3cae66c
  Args:
    literal_value: 1990
    source: Karl_of_Leiningen
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (6707be8e-23e2-46fd-ae64-c608c2394661)
 Call ID: 6707be8e-23e2-46fd-ae64-c608c2394661
  Args:
    literal_value: Karl Vladimir Ernst Heinrich
    source: Karl_of_Leiningen
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (0f6d876e-0257-460c-89a6-fccc7bc11d4f)
 Call ID: 0f6d876e-0257-460c-89a6-fccc7bc11d4f
  Args:
    type: :Man
    source: Karl_6th_Prince_of_Leiningen
  AssignClass (f6f16c21-0acf-455d-97ab-f539c72856c7)
 Call ID: f6f16c21-0acf-455d-97ab-f539c72856c7
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Person
  AddLiteral (00544870-594d-44c2-9c2f-07c68fbdc646)
 Call ID: 00544870-594d-44c2-9c2f-07c68fbdc646
  Args:
    literal_value: 1898
    source: Karl_6th_Prince_of_Leiningen
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (679225ee-0c33-4482-807e-41c8d1a0850b)
 Call ID: 679225ee-0c33-4482-807e-41c8d1a0850b
  Args:
    literal_value: 1946
    literal_type: xsd:integer
    source: Karl_6th_Prince_of_Leiningen
    relation: :hasDeathYear
  AddTriple (81ad0f5b-1419-4fa7-b264-9e64537798a6)
 Call ID: 81ad0f5b-1419-4fa7-b264-9e64537798a6
  Args:
    relation: :hasFather
    target: Karl_6th_Prince_of_Leiningen
    source: Karl_of_Leiningen
  AssignClass (01f66ec9-983b-4bf5-a6f5-2b7136f71d2b)
 Call ID: 01f66ec9-983b-4bf5-a6f5-2b7136f71d2b
  Args:
    type: :Woman
    source: Maria_Kirillovna_of_Russia
  AssignClass (d77a7afb-e6c8-40d7-9107-16c1855ee410)
 Call ID: d77a7afb-e6c8-40d7-9107-16c1855ee410
  Args:
    type: :Person
    source: Maria_Kirillovna_of_Russia
  AddTriple (7295f426-0f46-4b99-8b08-c58f090b6779)
 Call ID: 7295f426-0f46-4b99-8b08-c58f090b6779
  Args:
    relation: :hasMother
    source: Karl_of_Leiningen
    target: Maria_Kirillovna_of_Russia
  AssignClass (bf2eca0d-eb3d-4900-8fa9-a2fea2ec5e88)
 Call ID: bf2eca0d-eb3d-4900-8fa9-a2fea2ec5e88
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Man
  AssignClass (b4f86afa-52fa-4d54-8b10-15d25bc226a2)
 Call ID: b4f86afa-52fa-4d54-8b10-15d25bc226a2
  Args:
    source: Kirill_Vladimirovich_of_Russia
    type: :Person
  AssignClass (7d4f6ad0-f277-43f0-bd74-4cf7c13d2474)
 Call ID: 7d4f6ad0-f277-43f0-bd74-4cf7c13d2474
  Args:
    source: Victoria_Melita_of_Edinburgh
    type: :Woman
  AssignClass (7f0891ef-cf81-49dc-b6cc-b7511560bb87)
 Call ID: 7f0891ef-cf81-49dc-b6cc-b7511560bb87
  Args:
    type: :Person
    source: Victoria_Melita_of_Edinburgh
  AddTriple (38dc1031-c588-46ea-add4-1a9f1cdffb31)
 Call ID: 38dc1031-c588-46ea-add4-1a9f1cdffb31
  Args:
    source: Maria_Kirillovna_of_Russia
    target: Kirill_Vladimirovich_of_Russia
    relation: :hasFather
  AddTriple (37625808-1117-4e42-83a9-b544d38b143f)
 Call ID: 37625808-1117-4e42-83a9-b544d38b143f
  Args:
    target: Victoria_Melita_of_Edinburgh
    source: Maria_Kirillovna_of_Russia
    relation: :hasMother
  AssignClass (e9972abe-229e-4d55-8188-1c238c6c9ed9)
 Call ID: e9972abe-229e-4d55-8188-1c238c6c9ed9
  Args:
    type: :Woman
    source: Marie_Louise_of_Bulgaria
  AssignClass (c4729707-00bf-4912-be0f-a1a7b9779e8e)
 Call ID: c4729707-00bf-4912-be0f-a1a7b9779e8e
  Args:
    type: :Person
    source: Marie_Louise_of_Bulgaria
  AddTriple (5b079e46-37fc-4da3-8e66-6a94ce2da004)
 Call ID: 5b079e46-37fc-4da3-8e66-6a94ce2da004
  Args:
    target: Marie_Louise_of_Bulgaria
    source: Karl_of_Leiningen
    relation: :hasRelation
  AddLiteral (9216d2fe-bd48-4e4e-8553-e5e29e4443df)
 Call ID: 9216d2fe-bd48-4e4e-8553-e5e29e4443df
  Args:
    source: Karl_of_Leiningen
    literal_type: xsd:integer
    literal_value: 1956
    relation: :hasMarriageYear
  AssignClass (209ea76a-c44b-48f6-b00a-1659abc5b428)
 Call ID: 209ea76a-c44b-48f6-b00a-1659abc5b428
  Args:
    type: :Man
    source: Boris_III_of_Bulgaria
  AssignClass (901ab634-9471-4800-9860-8bc703074730)
 Call ID: 901ab634-9471-4800-9860-8bc703074730
  Args:
    type: :Person
    source: Boris_III_of_Bulgaria
  AssignClass (e8356f20-da30-4f4f-b767-2e488a4ff7d0)
 Call ID: e8356f20-da30-4f4f-b767-2e488a4ff7d0
  Args:
    source: Giovanna_of_Italy
    type: :Woman
  AssignClass (f79099c9-047a-4d7c-887c-9fc8b74a5cb7)
 Call ID: f79099c9-047a-4d7c-887c-9fc8b74a5cb7
  Args:
    type: :Person
    source: Giovanna_of_Italy
  AddTriple (f66fb100-a7f7-418a-a7c6-69b996d8c12f)
 Call ID: f66fb100-a7f7-418a-a7c6-69b996d8c12f
  Args:
    target: Boris_III_of_Bulgaria
    source: Marie_Louise_of_Bulgaria
    relation: :hasFather
  AddTriple (e0cea8e2-35e0-42af-9a3b-3a2a28266ccd)
 Call ID: e0cea8e2-35e0-42af-9a3b-3a2a28266ccd
  Args:
    source: Marie_Louise_of_Bulgaria
    target: Giovanna_of_Italy
    relation: :hasMother
  Finish (c77042ea-2ce9-46f1-9416-75fa7d5761b2)
 Call ID: c77042ea-2ce9-46f1-9416-75fa7d5761b2
  Args: