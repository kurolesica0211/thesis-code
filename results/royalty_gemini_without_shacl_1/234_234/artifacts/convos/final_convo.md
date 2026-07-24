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
Infante Juan, Count of Barcelona (Juan Carlos Teresa Silverio Alfonso de Borbón y Battenberg; 20 June 1913 – 1 April 1993), was a claimant to the Spanish throne as Juan III.
He was the third son and designated heir of King Alfonso XIII and Victoria Eugenie of Battenberg.
Juan's son Juan Carlos I became King of Spain when Spain's constitutional monarchy was restored in 1975.
Early life

Infante Juan was born at the Palace of San Ildefonso.
Owing to the renunciations in 1933 of his brothers Alfonso, Prince of Asturias, and Infante Jaime, Duke of Segovia, Infante Juan became first in line to the defunct Spanish throne.
He thus received the title Prince of Asturias while serving with the Royal Navy in Bombay.
He married Princess María de las Mercedes of Bourbon-Two Sicilies (1910–2000), known in Spain as Doña María de las Mercedes de Borbón-Dos Sicilias y Orleans, in Rome on 12 October 1935.
Children

They had four children:


They lived in Cannes and Rome, and, with the outbreak of World War II, they moved to Lausanne to live with his mother, Victoria Eugenie.
Together with their children Pilar and Juan Carlos, they took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
On this trip, Juan Carlos met the hosts' 15-year-old daughter, Sofia, his future wife, for the first time.
Claim to the Spanish throne

In 1931, Juan was subject to dynastic negotiations between the Alfonsists and the Carlists, concluded in the so-called Pact of Territet, which was never implemented.
Juan became heir apparent to the defunct Spanish throne after the renunciations of his two older brothers, Alfonso and Jaime, in 1933.
To assert his claim to the throne, following his father's death (in 1941) he used the title of Count of Barcelona, a sovereign title associated with the Spanish crown.
Spain runs the risk of being dragged into a new fratricidal conflict and of finding itself totally isolated from the world.
When General Franco declared Spain a monarchy in 1947, he characterized it as a "restoration".
However, Franco was afraid that Juan would roll back the Spanish State because he favoured constitutional monarchy, which would restore parliamentary democracy.
As a result, in 1969, Franco passed over Juan in favour of Juan's son, Juan Carlos, who Franco believed would be more likely to continue the dictatorship after his death.
Juan Carlos later surprised many by his support of democratising Spain.
Franco and Juan did not have a good relationship, with the latter constantly pressing Franco to restore the monarchy.
Relations soured further when Juan called Franco an "illegitimate usurper".
Juan formally renounced his rights to the Spanish throne eight years after being displaced as recognised heir to the throne by Franco, and two years after his son, Juan Carlos, had become king.
In return, his son officially granted him the title of Count of Barcelona, which he had claimed for so long.
After his death in 1993, he was buried with honours due a king, under the name Juan III (his title if he had become king) in the Royal Crypt of the monastery of San Lorenzo de El Escorial, near Madrid.



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
  AssignClass (679bc29b-fc65-47f0-ac81-bc4aee1bee96)
 Call ID: 679bc29b-fc65-47f0-ac81-bc4aee1bee96
  Args:
    source: Juan_Count_of_Barcelona
    type: :Man
  AssignClass (d4d109ab-03ab-4900-98cd-beebd759551f)
 Call ID: d4d109ab-03ab-4900-98cd-beebd759551f
  Args:
    source: Juan_Count_of_Barcelona
    type: :Person
  AddLiteral (91f51a70-3ffb-42a6-b9da-7debed274742)
 Call ID: 91f51a70-3ffb-42a6-b9da-7debed274742
  Args:
    source: Juan_Count_of_Barcelona
    literal_value: 1913
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (09614978-dc5b-419a-9cbf-aa831e661a37)
 Call ID: 09614978-dc5b-419a-9cbf-aa831e661a37
  Args:
    literal_value: 1993
    source: Juan_Count_of_Barcelona
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (785ec146-b02c-46d8-9529-052ceeaef887)
 Call ID: 785ec146-b02c-46d8-9529-052ceeaef887
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (666dbbec-bba3-4529-9fca-625834f3f2df)
 Call ID: 666dbbec-bba3-4529-9fca-625834f3f2df
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (828bc6bb-116d-4c8f-b2c9-eec0d3face7f)
 Call ID: 828bc6bb-116d-4c8f-b2c9-eec0d3face7f
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (70c28585-ee4b-4c0f-a5e0-766396af1b9c)
 Call ID: 70c28585-ee4b-4c0f-a5e0-766396af1b9c
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (425f8ceb-1982-4322-8598-495d3972f239)
 Call ID: 425f8ceb-1982-4322-8598-495d3972f239
  Args:
    source: Juan_Count_of_Barcelona
    target: Alfonso_XIII
    relation: :hasFather
  AddTriple (8e349d86-e754-400a-a3e2-0da9679454e2)
 Call ID: 8e349d86-e754-400a-a3e2-0da9679454e2
  Args:
    relation: :hasMother
    source: Juan_Count_of_Barcelona
    target: Victoria_Eugenie_of_Battenberg
  AssignClass (12251197-c4ad-4be8-91e0-05a8d49bf659)
 Call ID: 12251197-c4ad-4be8-91e0-05a8d49bf659
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (00b3f92a-249b-4fc8-81a0-f9274c02ee2d)
 Call ID: 00b3f92a-249b-4fc8-81a0-f9274c02ee2d
  Args:
    type: :Person
    source: Juan_Carlos_I
  AddTriple (60df4a9b-87a1-48be-b2bc-5aec857b7435)
 Call ID: 60df4a9b-87a1-48be-b2bc-5aec857b7435
  Args:
    target: Juan_Count_of_Barcelona
    source: Juan_Carlos_I
    relation: :hasFather
  AssignClass (c610ada9-41ef-494c-ad04-b1d5aecb768e)
 Call ID: c610ada9-41ef-494c-ad04-b1d5aecb768e
  Args:
    type: :Man
    source: Alfonso_Prince_of_Asturias
  AssignClass (e0d05574-39bd-466b-996e-328fb5f365b6)
 Call ID: e0d05574-39bd-466b-996e-328fb5f365b6
  Args:
    type: :Person
    source: Alfonso_Prince_of_Asturias
  AddTriple (bd279f7b-662f-4f6a-8fd8-64f479140f11)
 Call ID: bd279f7b-662f-4f6a-8fd8-64f479140f11
  Args:
    relation: :isBrotherOf
    source: Alfonso_Prince_of_Asturias
    target: Juan_Count_of_Barcelona
  AssignClass (4416633f-f4d8-4c9a-bbb0-12960c7f9fb9)
 Call ID: 4416633f-f4d8-4c9a-bbb0-12960c7f9fb9
  Args:
    source: Jaime_Duke_of_Segovia
    type: :Man
  AssignClass (d4293197-68da-4f01-8d8e-0385b8fa56d1)
 Call ID: d4293197-68da-4f01-8d8e-0385b8fa56d1
  Args:
    source: Jaime_Duke_of_Segovia
    type: :Person
  AddTriple (262537c8-574c-4a77-ab48-79e2aec211dc)
 Call ID: 262537c8-574c-4a77-ab48-79e2aec211dc
  Args:
    relation: :isBrotherOf
    target: Juan_Count_of_Barcelona
    source: Jaime_Duke_of_Segovia
  AssignClass (113dc7f3-49d9-4fcf-88e1-544544cf0efb)
 Call ID: 113dc7f3-49d9-4fcf-88e1-544544cf0efb
  Args:
    source: Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
    type: :Woman
  AssignClass (5912332b-6fcb-414a-a2aa-1c732489c198)
 Call ID: 5912332b-6fcb-414a-a2aa-1c732489c198
  Args:
    source: Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
    type: :Person
  AddTriple (9557eed8-5f27-4f6c-9cfe-b6c08014c989)
 Call ID: 9557eed8-5f27-4f6c-9cfe-b6c08014c989
  Args:
    relation: :hasRelation
    source: Juan_Count_of_Barcelona
    target: Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
  AddLiteral (829594a1-dbbb-42df-a1da-131c1eff9b9b)
 Call ID: 829594a1-dbbb-42df-a1da-131c1eff9b9b
  Args:
    literal_value: 1935
    source: Juan_Count_of_Barcelona
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (2b097725-104b-480c-ad2a-6950551990fc)
 Call ID: 2b097725-104b-480c-ad2a-6950551990fc
  Args:
    type: :Woman
    source: Pilar
  AssignClass (9fe9f2cb-7f6d-439c-a80f-7deb943208fb)
 Call ID: 9fe9f2cb-7f6d-439c-a80f-7deb943208fb
  Args:
    type: :Person
    source: Pilar
  AddTriple (9d3dd715-1c41-44f1-9e0b-17f0521fc6f5)
 Call ID: 9d3dd715-1c41-44f1-9e0b-17f0521fc6f5
  Args:
    relation: :hasFather
    source: Pilar
    target: Juan_Count_of_Barcelona
  AddTriple (c3b849e4-d560-4fdb-b480-ee97ab1429bf)
 Call ID: c3b849e4-d560-4fdb-b480-ee97ab1429bf
  Args:
    relation: :hasMother
    target: Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
    source: Pilar
  AddTriple (361bb3a1-b8cb-4406-a137-060144b6f00e)
 Call ID: 361bb3a1-b8cb-4406-a137-060144b6f00e
  Args:
    relation: :hasFather
    target: Juan_Count_of_Barcelona
    source: Juan_Carlos_I
  AddTriple (9d586990-8a17-4aab-87e5-06e082552b65)
 Call ID: 9d586990-8a17-4aab-87e5-06e082552b65
  Args:
    target: Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
    source: Juan_Carlos_I
    relation: :hasMother
  AssignClass (1f3076ec-f1e0-4a64-976f-67659dc75e11)
 Call ID: 1f3076ec-f1e0-4a64-976f-67659dc75e11
  Args:
    source: Sofia
    type: :Woman
  AssignClass (4f7d388b-d0d2-4780-bcf7-4597deeb5ed2)
 Call ID: 4f7d388b-d0d2-4780-bcf7-4597deeb5ed2
  Args:
    type: :Person
    source: Sofia
  AddTriple (d3dd88cb-86f5-471c-893b-7b3b1f16819d)
 Call ID: d3dd88cb-86f5-471c-893b-7b3b1f16819d
  Args:
    source: Juan_Carlos_I
    target: Sofia
    relation: :hasRelation
  AssignClass (a4d7f70e-9d36-4844-9961-9a2dc931b5ad)
 Call ID: a4d7f70e-9d36-4844-9961-9a2dc931b5ad
  Args:
    type: :Man
    source: Paul_of_Greece
  AssignClass (6e339cce-2085-4c6c-b8cf-17104522fde9)
 Call ID: 6e339cce-2085-4c6c-b8cf-17104522fde9
  Args:
    type: :Person
    source: Paul_of_Greece
  AssignClass (eda9adf1-32f4-473f-b8af-4e1098c51131)
 Call ID: eda9adf1-32f4-473f-b8af-4e1098c51131
  Args:
    source: Frederica_of_Greece
    type: :Woman
  AssignClass (5cfd3af6-f966-43db-b471-5eb8b04f961d)
 Call ID: 5cfd3af6-f966-43db-b471-5eb8b04f961d
  Args:
    type: :Person
    source: Frederica_of_Greece
  AddTriple (aaeb3756-5f82-4535-9ba0-460228b5e0c4)
 Call ID: aaeb3756-5f82-4535-9ba0-460228b5e0c4
  Args:
    source: Paul_of_Greece
    target: Frederica_of_Greece
    relation: :hasRelation
  AddTriple (209661cc-f43b-4d47-8577-31fc58329e74)
 Call ID: 209661cc-f43b-4d47-8577-31fc58329e74
  Args:
    target: Paul_of_Greece
    source: Sofia
    relation: :hasFather
  AddTriple (230d2e8f-4fa2-40c2-86d3-8b04adb8d0ad)
 Call ID: 230d2e8f-4fa2-40c2-86d3-8b04adb8d0ad
  Args:
    target: Frederica_of_Greece
    source: Sofia
    relation: :hasMother
  Finish (2bb4b17f-bb78-4baf-8518-a41fda8a348f)
 Call ID: 2bb4b17f-bb78-4baf-8518-a41fda8a348f
  Args: