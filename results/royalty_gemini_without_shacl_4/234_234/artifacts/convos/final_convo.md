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
  AssignClass (20ca04fd-9f75-4a83-aa80-035d462d623e)
 Call ID: 20ca04fd-9f75-4a83-aa80-035d462d623e
  Args:
    source: Juan_Count_of_Barcelona
    type: :Man
  AssignClass (721cf284-4813-4f12-9af0-692263b6a3b1)
 Call ID: 721cf284-4813-4f12-9af0-692263b6a3b1
  Args:
    type: :Person
    source: Juan_Count_of_Barcelona
  AddLiteral (e2920235-ce43-4249-b983-71338fbb71cd)
 Call ID: e2920235-ce43-4249-b983-71338fbb71cd
  Args:
    literal_value: 1913
    source: Juan_Count_of_Barcelona
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (cd4f1e28-5512-433e-9a2f-f30b0043eab8)
 Call ID: cd4f1e28-5512-433e-9a2f-f30b0043eab8
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1993
    source: Juan_Count_of_Barcelona
  AssignClass (61ffcec9-6b0d-4b63-84ea-125bd5dcc1ca)
 Call ID: 61ffcec9-6b0d-4b63-84ea-125bd5dcc1ca
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (ac7eafd2-40a3-440b-84de-0fdd9022e019)
 Call ID: ac7eafd2-40a3-440b-84de-0fdd9022e019
  Args:
    source: Alfonso_XIII
    type: :Person
  AssignClass (e57cc62d-4211-46a4-97e1-bab33a40aeaf)
 Call ID: e57cc62d-4211-46a4-97e1-bab33a40aeaf
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (74c8079e-3765-4a88-94fc-916596691145)
 Call ID: 74c8079e-3765-4a88-94fc-916596691145
  Args:
    source: Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (c3c66928-8044-45f3-8b2e-ff999e066717)
 Call ID: c3c66928-8044-45f3-8b2e-ff999e066717
  Args:
    target: Alfonso_XIII
    source: Juan_Count_of_Barcelona
    relation: :hasFather
  AddTriple (70b6fdd1-7bea-40ff-b8e6-a5b4fb918010)
 Call ID: 70b6fdd1-7bea-40ff-b8e6-a5b4fb918010
  Args:
    relation: :hasMother
    source: Juan_Count_of_Barcelona
    target: Victoria_Eugenie_of_Battenberg
  AssignClass (ce423014-c7f0-42e5-a09d-3318c4ee48f8)
 Call ID: ce423014-c7f0-42e5-a09d-3318c4ee48f8
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (641cb0d2-60bd-4bcb-bd0b-abf957557685)
 Call ID: 641cb0d2-60bd-4bcb-bd0b-abf957557685
  Args:
    source: Juan_Carlos_I
    type: :Person
  AddTriple (b8984a75-f708-483d-8ca9-bb545dcfcb26)
 Call ID: b8984a75-f708-483d-8ca9-bb545dcfcb26
  Args:
    relation: :isSonOf
    source: Juan_Carlos_I
    target: Juan_Count_of_Barcelona
  AssignClass (36cca308-1d8b-48c0-8371-a94da092b0a5)
 Call ID: 36cca308-1d8b-48c0-8371-a94da092b0a5
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (a7859f8a-746d-4b46-8a7a-c93ebc7fd9e1)
 Call ID: a7859f8a-746d-4b46-8a7a-c93ebc7fd9e1
  Args:
    source: Alfonso_Prince_of_Asturias
    type: :Person
  AssignClass (9fcf29a7-8a50-4682-aaef-b3a8690967a9)
 Call ID: 9fcf29a7-8a50-4682-aaef-b3a8690967a9
  Args:
    source: Jaime_Duke_of_Segovia
    type: :Man
  AssignClass (fc3b1725-a450-493b-ad5b-957beddf9b10)
 Call ID: fc3b1725-a450-493b-ad5b-957beddf9b10
  Args:
    type: :Person
    source: Jaime_Duke_of_Segovia
  AddTriple (1f356542-c833-472e-8dae-572fd2823a9d)
 Call ID: 1f356542-c833-472e-8dae-572fd2823a9d
  Args:
    target: Alfonso_Prince_of_Asturias
    source: Juan_Count_of_Barcelona
    relation: :isBrotherOf
  AddTriple (83e85b39-d656-4148-b587-f4a32cd0c7f1)
 Call ID: 83e85b39-d656-4148-b587-f4a32cd0c7f1
  Args:
    relation: :isBrotherOf
    source: Juan_Count_of_Barcelona
    target: Jaime_Duke_of_Segovia
  AssignClass (6108929e-4313-4699-9d70-296848af08f1)
 Call ID: 6108929e-4313-4699-9d70-296848af08f1
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AssignClass (96759ca3-b7c6-4d4c-bcab-570d7cfc7fef)
 Call ID: 96759ca3-b7c6-4d4c-bcab-570d7cfc7fef
  Args:
    source: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (facc3930-c4d9-443a-b7db-b63cfa02a45c)
 Call ID: facc3930-c4d9-443a-b7db-b63cfa02a45c
  Args:
    source: Juan_Count_of_Barcelona
    literal_value: 1935
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (b115a4a1-3058-4c05-bc89-9dd4c29fce42)
 Call ID: b115a4a1-3058-4c05-bc89-9dd4c29fce42
  Args:
    relation: :hasRelation
    target: Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    source: Juan_Count_of_Barcelona
  AssignClass (fcefdf9c-5405-48d3-9a27-a8ce6d86e3fa)
 Call ID: fcefdf9c-5405-48d3-9a27-a8ce6d86e3fa
  Args:
    source: Pilar
    type: :Woman
  AssignClass (472344c3-228f-426b-9bd0-923595ecb512)
 Call ID: 472344c3-228f-426b-9bd0-923595ecb512
  Args:
    type: :Person
    source: Pilar
  AddTriple (a0ec60cf-608b-4792-8670-d7ecb7354e71)
 Call ID: a0ec60cf-608b-4792-8670-d7ecb7354e71
  Args:
    relation: :isChildOf
    source: Pilar
    target: Juan_Count_of_Barcelona
  AddTriple (f997526d-6b7b-478b-b578-650718d59d86)
 Call ID: f997526d-6b7b-478b-b578-650718d59d86
  Args:
    target: Juan_Count_of_Barcelona
    source: Juan_Carlos_I
    relation: :isChildOf
  AssignClass (79da9249-b003-43a6-9a7f-723d567ba573)
 Call ID: 79da9249-b003-43a6-9a7f-723d567ba573
  Args:
    type: :Woman
    source: Frederica_of_Greece
  AssignClass (b1094c92-c0c6-467e-8ea2-0c1be95e5a34)
 Call ID: b1094c92-c0c6-467e-8ea2-0c1be95e5a34
  Args:
    source: Frederica_of_Greece
    type: :Person
  AssignClass (07561513-2eec-4a31-a569-ba4c00dec356)
 Call ID: 07561513-2eec-4a31-a569-ba4c00dec356
  Args:
    source: Paul_of_Greece
    type: :Man
  AssignClass (9095f1b8-5827-44ed-82b9-f663fe22ee35)
 Call ID: 9095f1b8-5827-44ed-82b9-f663fe22ee35
  Args:
    type: :Person
    source: Paul_of_Greece
  AssignClass (2e02ed95-6884-4678-8cd3-f1b53489f639)
 Call ID: 2e02ed95-6884-4678-8cd3-f1b53489f639
  Args:
    source: Sofia_of_Greece
    type: :Woman
  AssignClass (6476b8a9-aa4a-461e-a8f2-f22492f9e1ee)
 Call ID: 6476b8a9-aa4a-461e-a8f2-f22492f9e1ee
  Args:
    source: Sofia_of_Greece
    type: :Person
  AddTriple (14796fc5-d74a-434c-b5b0-e6255f0d76a9)
 Call ID: 14796fc5-d74a-434c-b5b0-e6255f0d76a9
  Args:
    target: Paul_of_Greece
    source: Sofia_of_Greece
    relation: :hasFather
  AddTriple (6aaedbc3-b307-4db9-9ac3-6934777b9d3c)
 Call ID: 6aaedbc3-b307-4db9-9ac3-6934777b9d3c
  Args:
    target: Frederica_of_Greece
    source: Sofia_of_Greece
    relation: :hasMother
  Finish (8c870290-708a-4104-9973-4d6f0091898a)
 Call ID: 8c870290-708a-4104-9973-4d6f0091898a
  Args: