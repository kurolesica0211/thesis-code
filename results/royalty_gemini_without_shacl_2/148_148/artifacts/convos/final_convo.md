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
  AssignClass (2b4d2522-0a5b-4651-8fb4-6637cdad7906)
 Call ID: 2b4d2522-0a5b-4651-8fb4-6637cdad7906
  Args:
    source: Prince_Karl_of_Leiningen
    type: :Man
  AssignClass (5880f0e8-494e-446a-94d9-09178c1fc768)
 Call ID: 5880f0e8-494e-446a-94d9-09178c1fc768
  Args:
    type: :Person
    source: Prince_Karl_of_Leiningen
  AddLiteral (b3669266-e30d-411b-9fb4-2bb107023bd3)
 Call ID: b3669266-e30d-411b-9fb4-2bb107023bd3
  Args:
    literal_value: 1928
    relation: :hasBirthYear
    source: Prince_Karl_of_Leiningen
    literal_type: xsd:integer
  AddLiteral (d9f744bc-2257-4cd1-8a4a-873a87095f54)
 Call ID: d9f744bc-2257-4cd1-8a4a-873a87095f54
  Args:
    source: Prince_Karl_of_Leiningen
    relation: :hasDeathYear
    literal_value: 1990
    literal_type: xsd:integer
  AssignClass (8031c753-589c-476d-bf5a-7334cef7ba05)
 Call ID: 8031c753-589c-476d-bf5a-7334cef7ba05
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Man
  AssignClass (ca86d435-46f5-41de-b87f-904d59d5f6dd)
 Call ID: ca86d435-46f5-41de-b87f-904d59d5f6dd
  Args:
    source: Karl_6th_Prince_of_Leiningen
    type: :Person
  AddLiteral (54cb12da-6313-4e26-87b3-7fefc15f7d52)
 Call ID: 54cb12da-6313-4e26-87b3-7fefc15f7d52
  Args:
    literal_type: xsd:integer
    source: Karl_6th_Prince_of_Leiningen
    literal_value: 1898
    relation: :hasBirthYear
  AddLiteral (f7fd16c6-b9a5-4166-8c3f-8d65db374db0)
 Call ID: f7fd16c6-b9a5-4166-8c3f-8d65db374db0
  Args:
    literal_type: xsd:integer
    source: Karl_6th_Prince_of_Leiningen
    relation: :hasDeathYear
    literal_value: 1946
  AddTriple (91a652f9-5b81-41f6-9f74-646f9d1e1221)
 Call ID: 91a652f9-5b81-41f6-9f74-646f9d1e1221
  Args:
    relation: :hasFather
    target: Karl_6th_Prince_of_Leiningen
    source: Prince_Karl_of_Leiningen
  AssignClass (9f868791-2506-459d-b245-7aed58c8dbef)
 Call ID: 9f868791-2506-459d-b245-7aed58c8dbef
  Args:
    type: :Woman
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
  AssignClass (847a6664-9fc1-44d2-9fb6-671af9bd6254)
 Call ID: 847a6664-9fc1-44d2-9fb6-671af9bd6254
  Args:
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    type: :Person
  AddTriple (04b7e750-9c24-4756-9990-1cddae7877cd)
 Call ID: 04b7e750-9c24-4756-9990-1cddae7877cd
  Args:
    relation: :hasMother
    source: Prince_Karl_of_Leiningen
    target: Grand_Duchess_Maria_Kirillovna_of_Russia
  AssignClass (56435ab8-57df-4d30-80da-4fb4cff69b81)
 Call ID: 56435ab8-57df-4d30-80da-4fb4cff69b81
  Args:
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
    type: :Man
  AssignClass (f7ab78c9-be38-4561-aa51-0d4d0b275011)
 Call ID: f7ab78c9-be38-4561-aa51-0d4d0b275011
  Args:
    type: :Person
    source: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AssignClass (007095a9-131a-4daf-831e-dc9bf586a12b)
 Call ID: 007095a9-131a-4daf-831e-dc9bf586a12b
  Args:
    type: :Woman
    source: Princess_Victoria_Melita_of_Edinburgh
  AssignClass (09682811-9297-420d-a9d7-ef70dbdaae0c)
 Call ID: 09682811-9297-420d-a9d7-ef70dbdaae0c
  Args:
    type: :Person
    source: Princess_Victoria_Melita_of_Edinburgh
  AddTriple (abf126e3-319a-4665-9aba-54edfb6a08c6)
 Call ID: abf126e3-319a-4665-9aba-54edfb6a08c6
  Args:
    relation: :hasFather
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    target: Grand_Duke_Kirill_Vladimirovich_of_Russia
  AddTriple (89bb477a-e55a-4f23-9027-7a0087d153de)
 Call ID: 89bb477a-e55a-4f23-9027-7a0087d153de
  Args:
    source: Grand_Duchess_Maria_Kirillovna_of_Russia
    target: Princess_Victoria_Melita_of_Edinburgh
    relation: :hasMother
  AssignClass (11868184-ccc6-4576-921d-bbd4347ad259)
 Call ID: 11868184-ccc6-4576-921d-bbd4347ad259
  Args:
    source: Princess_Marie_Louise_of_Bulgaria
    type: :Woman
  AssignClass (f091cf2a-e94a-4f62-bab6-9e9fb59b5774)
 Call ID: f091cf2a-e94a-4f62-bab6-9e9fb59b5774
  Args:
    source: Princess_Marie_Louise_of_Bulgaria
    type: :Person
  AssignClass (b22527b3-41ef-4575-a67f-ed02e8e5fc9b)
 Call ID: b22527b3-41ef-4575-a67f-ed02e8e5fc9b
  Args:
    type: :Man
    source: Boris_III_of_Bulgaria
  AssignClass (e21d4c81-05cf-4d5d-b0d6-19e0b3877042)
 Call ID: e21d4c81-05cf-4d5d-b0d6-19e0b3877042
  Args:
    source: Boris_III_of_Bulgaria
    type: :Person
  AssignClass (ba03fca7-1d64-46da-9599-5d673fca991a)
 Call ID: ba03fca7-1d64-46da-9599-5d673fca991a
  Args:
    type: :Woman
    source: Princess_Giovanna_of_Italy
  AssignClass (ff333b59-5f90-4d5b-bc9c-fed4fd6a461e)
 Call ID: ff333b59-5f90-4d5b-bc9c-fed4fd6a461e
  Args:
    source: Princess_Giovanna_of_Italy
    type: :Person
  AddTriple (be672dda-557e-4572-9efb-81da59605a82)
 Call ID: be672dda-557e-4572-9efb-81da59605a82
  Args:
    target: Boris_III_of_Bulgaria
    source: Princess_Marie_Louise_of_Bulgaria
    relation: :hasFather
  AddTriple (05ade074-f975-44ca-8bed-4671f8a77dcc)
 Call ID: 05ade074-f975-44ca-8bed-4671f8a77dcc
  Args:
    relation: :hasMother
    target: Princess_Giovanna_of_Italy
    source: Princess_Marie_Louise_of_Bulgaria
  AddLiteral (ee53d4d5-daaa-4f8d-b02e-d69deb4405fe)
 Call ID: ee53d4d5-daaa-4f8d-b02e-d69deb4405fe
  Args:
    literal_type: xsd:integer
    source: Prince_Karl_of_Leiningen
    literal_value: 1968
    relation: :hasMarriageYear
  Finish (10a5ce2f-f10a-45d6-97c1-ceee664223fb)
 Call ID: 10a5ce2f-f10a-45d6-97c1-ceee664223fb
  Args: