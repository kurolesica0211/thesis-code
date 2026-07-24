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
  AssignClass (fa65dab9-44bc-49c3-ba55-053a9bca35f1)
 Call ID: fa65dab9-44bc-49c3-ba55-053a9bca35f1
  Args:
    type: :Man
    source: Prince_Karl_of_Leiningen
  AssignClass (192fb834-9b2c-4938-9fcf-c51bc1428b6e)
 Call ID: 192fb834-9b2c-4938-9fcf-c51bc1428b6e
  Args:
    source: Prince_Karl_of_Leiningen
    type: :Person
  AddLiteral (660b1ae1-038b-49a8-90e3-4004f4123ec7)
 Call ID: 660b1ae1-038b-49a8-90e3-4004f4123ec7
  Args:
    relation: :hasBirthYear
    literal_value: 1928
    source: Prince_Karl_of_Leiningen
    literal_type: xsd:integer
  AddLiteral (d7995c99-cc0b-4a41-a91d-c1cfe245e367)
 Call ID: d7995c99-cc0b-4a41-a91d-c1cfe245e367
  Args:
    source: Prince_Karl_of_Leiningen
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1990
  AssignClass (edbb0958-34dc-4f2d-93c4-32a3e11edfba)
 Call ID: edbb0958-34dc-4f2d-93c4-32a3e11edfba
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Man
  AssignClass (434aa462-8fc2-43b1-b09d-97ed52c34d1a)
 Call ID: 434aa462-8fc2-43b1-b09d-97ed52c34d1a
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Person
  AddLiteral (3e618b07-da35-4ea6-ada3-ab92ee7e5aef)
 Call ID: 3e618b07-da35-4ea6-ada3-ab92ee7e5aef
  Args:
    relation: :hasBirthYear
    literal_value: 1898
    source: Karl_6th_Prince_of_Leiningen
    literal_type: xsd:integer
  AddLiteral (3587e2ec-ca08-4400-afd0-e94defa6f077)
 Call ID: 3587e2ec-ca08-4400-afd0-e94defa6f077
  Args:
    relation: :hasDeathYear
    literal_value: 1946
    source: Karl_6th_Prince_of_Leiningen
    literal_type: xsd:integer
  AssignClass (6baa3120-aa23-4cae-9c2c-4335589689b3)
 Call ID: 6baa3120-aa23-4cae-9c2c-4335589689b3
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
  AssignClass (7427247d-9107-4c7b-a1c7-9784275af2f3)
 Call ID: 7427247d-9107-4c7b-a1c7-9784275af2f3
  Args:
    type: :Person
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
  AddTriple (55790a56-a3a1-471f-beaa-e83e8e66646f)
 Call ID: 55790a56-a3a1-471f-beaa-e83e8e66646f
  Args:
    target: Karl_6th_Prince_of_Leiningen
    source: Prince_Karl_of_Leiningen
    relation: :hasFather
  AddTriple (efc45272-3492-44a5-bfdc-c9696d56a195)
 Call ID: efc45272-3492-44a5-bfdc-c9696d56a195
  Args:
    relation: :hasMother
    target: Grand_Duchess_Maria_Kirillovna_of_Russia
    source: Prince_Karl_of_Leiningen
  AssignClass (897ca35a-47c5-4ae1-a658-f43cf15dcc5c)
 Call ID: 897ca35a-47c5-4ae1-a658-f43cf15dcc5c
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AssignClass (d14094d4-ee61-4f61-89a7-d73cefde5942)
 Call ID: d14094d4-ee61-4f61-89a7-d73cefde5942
  Args:
    type: :Person
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AssignClass (68ef95fb-d18b-4460-8def-8d6fbe123013)
 Call ID: 68ef95fb-d18b-4460-8def-8d6fbe123013
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Edinburgh
  AssignClass (a7bf3543-ec69-43ec-add7-18ba5ed1ae47)
 Call ID: a7bf3543-ec69-43ec-add7-18ba5ed1ae47
  Args:
    source: Princess_Victoria_Melita_of_Edinburgh
    type: :Person
  AddTriple (c7425393-eb00-4b73-87ec-87663d013057)
 Call ID: c7425393-eb00-4b73-87ec-87663d013057
  Args:
    target: Grand_Duke_Kirill_Vladimirovich_of_Russia
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    relation: :hasFather
  AddTriple (56289854-7c35-44aa-a0e4-1d8e433ca340)
 Call ID: 56289854-7c35-44aa-a0e4-1d8e433ca340
  Args:
    target: Princess_Victoria_Melita_of_Edinburgh
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    relation: :hasMother
  AssignClass (c3df0ee5-04c3-4e19-8db1-837a49df1273)
 Call ID: c3df0ee5-04c3-4e19-8db1-837a49df1273
  Args:
    type: :Woman
    source: Queen_Victoria_of_the_United_Kingdom
  AssignClass (f816468f-a5df-4cd0-95b2-16cd764d4381)
 Call ID: f816468f-a5df-4cd0-95b2-16cd764d4381
  Args:
    type: :Person
    source: Queen_Victoria_of_the_United_Kingdom
  AssignClass (1bd2be7d-7113-46de-b29e-0cb067cb31a2)
 Call ID: 1bd2be7d-7113-46de-b29e-0cb067cb31a2
  Args:
    source: Emperor_Alexander_II_of_Russia
    type: :Man
  AssignClass (e4ca56b5-c234-40e7-a58c-4edfef8f1f37)
 Call ID: e4ca56b5-c234-40e7-a58c-4edfef8f1f37
  Args:
    type: :Person
    source: Emperor_Alexander_II_of_Russia
  AssignClass (83fe5979-96d1-4b36-bba9-0528158a640e)
 Call ID: 83fe5979-96d1-4b36-bba9-0528158a640e
  Args:
    type: :Woman
    source: Princess_Marie_Louise_of_Bulgaria
  AssignClass (0936df7e-afb8-48aa-a6db-e09b426fda2d)
 Call ID: 0936df7e-afb8-48aa-a6db-e09b426fda2d
  Args:
    source: Princess_Marie_Louise_of_Bulgaria
    type: :Person
  AssignClass (95de317a-17ff-4daf-8221-d5462505dcdd)
 Call ID: 95de317a-17ff-4daf-8221-d5462505dcdd
  Args:
    source: Boris_III_of_Bulgaria
    type: :Man
  AssignClass (6621de85-ee99-43f5-bed0-d9656e5f1d73)
 Call ID: 6621de85-ee99-43f5-bed0-d9656e5f1d73
  Args:
    type: :Person
    source: Boris_III_of_Bulgaria
  AssignClass (fe22f395-b3bc-441e-a17a-ce2b648d820b)
 Call ID: fe22f395-b3bc-441e-a17a-ce2b648d820b
  Args:
    type: :Woman
    source: Princess_Giovanna_of_Italy
  AssignClass (eefe3414-664b-4f21-a013-b2c4ad2c685b)
 Call ID: eefe3414-664b-4f21-a013-b2c4ad2c685b
  Args:
    type: :Person
    source: Princess_Giovanna_of_Italy
  AddTriple (0f7a4dbd-53d7-499f-9eb9-f89881412f75)
 Call ID: 0f7a4dbd-53d7-499f-9eb9-f89881412f75
  Args:
    relation: :hasFather
    source: Princess_Marie_Louise_of_Bulgaria
    target: Boris_III_of_Bulgaria
  AddTriple (0e1bac17-bae6-41ee-9140-3f43dc7d13e9)
 Call ID: 0e1bac17-bae6-41ee-9140-3f43dc7d13e9
  Args:
    relation: :hasMother
    source: Princess_Marie_Louise_of_Bulgaria
    target: Princess_Giovanna_of_Italy
  AddLiteral (8f356a7e-7ec2-4542-bd8a-157b20d82360)
 Call ID: 8f356a7e-7ec2-4542-bd8a-157b20d82360
  Args:
    literal_value: 1968
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Karl_of_Leiningen
  Finish (81cf6f4e-f382-43c5-8882-bc5d4be02faa)
 Call ID: 81cf6f4e-f382-43c5-8882-bc5d4be02faa
  Args: