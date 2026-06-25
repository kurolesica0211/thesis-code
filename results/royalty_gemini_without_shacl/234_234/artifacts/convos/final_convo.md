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
  AssignClass (db4bfee8-3f02-4d0a-b1a6-8c3192e21dbd)
 Call ID: db4bfee8-3f02-4d0a-b1a6-8c3192e21dbd
  Args:
    type: :Man
    source: :InfanteJuan
  AssignClass (ed867d48-6d49-4044-b8a9-9032980b7d2d)
 Call ID: ed867d48-6d49-4044-b8a9-9032980b7d2d
  Args:
    source: :InfanteJuan
    type: :Person
  AddLiteral (60a72f51-4ebd-48dc-9a28-90a2a304c4ed)
 Call ID: 60a72f51-4ebd-48dc-9a28-90a2a304c4ed
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Juan Carlos Teresa Silverio Alfonso de Borbón y Battenberg
    source: :InfanteJuan
  AddLiteral (36e1b977-e5be-4a8a-8964-122240eb9003)
 Call ID: 36e1b977-e5be-4a8a-8964-122240eb9003
  Args:
    relation: :hasBirthYear
    literal_value: 1913
    literal_type: xsd:integer
    source: :InfanteJuan
  AddLiteral (053c28fa-ab65-4214-8806-b8b8b26a2df7)
 Call ID: 053c28fa-ab65-4214-8806-b8b8b26a2df7
  Args:
    relation: :hasDeathYear
    literal_value: 1993
    literal_type: xsd:integer
    source: :InfanteJuan
  AssignClass (d2d3208f-c0f1-4889-9d0a-cc87d6dd9a8b)
 Call ID: d2d3208f-c0f1-4889-9d0a-cc87d6dd9a8b
  Args:
    source: :AlfonsoXIII
    type: :Man
  AssignClass (c58195ee-f0d4-4014-90b7-842cc15391cc)
 Call ID: c58195ee-f0d4-4014-90b7-842cc15391cc
  Args:
    source: :AlfonsoXIII
    type: :Person
  AssignClass (06bf51b3-eb31-4883-9cb7-a1d408ce4a84)
 Call ID: 06bf51b3-eb31-4883-9cb7-a1d408ce4a84
  Args:
    type: :Woman
    source: :VictoriaEugenie
  AssignClass (26cdeae8-754d-4429-b7cb-e308e3351593)
 Call ID: 26cdeae8-754d-4429-b7cb-e308e3351593
  Args:
    source: :VictoriaEugenie
    type: :Person
  AddTriple (d13e13c0-cf1f-423c-8203-069cfeeafb35)
 Call ID: d13e13c0-cf1f-423c-8203-069cfeeafb35
  Args:
    source: :InfanteJuan
    relation: :hasFather
    target: :AlfonsoXIII
  AddTriple (27437db2-3e0d-46c7-9a93-35182b80cb23)
 Call ID: 27437db2-3e0d-46c7-9a93-35182b80cb23
  Args:
    target: :VictoriaEugenie
    relation: :hasMother
    source: :InfanteJuan
  AssignClass (e3e1949b-ce74-44be-9f27-f0e1bfd62301)
 Call ID: e3e1949b-ce74-44be-9f27-f0e1bfd62301
  Args:
    type: :Man
    source: :JuanCarlosI
  AssignClass (fd34b0f0-5a24-4a79-a1e3-e2ca080648c5)
 Call ID: fd34b0f0-5a24-4a79-a1e3-e2ca080648c5
  Args:
    source: :JuanCarlosI
    type: :Person
  AddTriple (60ab699f-655b-4fc9-a1f6-fbc29bb7d8b2)
 Call ID: 60ab699f-655b-4fc9-a1f6-fbc29bb7d8b2
  Args:
    source: :JuanCarlosI
    relation: :hasFather
    target: :InfanteJuan
  AssignClass (9474b261-4e17-4d4f-b16b-f20fb6b6a6b6)
 Call ID: 9474b261-4e17-4d4f-b16b-f20fb6b6a6b6
  Args:
    source: :AlfonsoPrinceOfAsturias
    type: :Man
  AssignClass (222baa0f-43f3-43db-ae8a-3d7dd2b9f2a4)
 Call ID: 222baa0f-43f3-43db-ae8a-3d7dd2b9f2a4
  Args:
    type: :Person
    source: :AlfonsoPrinceOfAsturias
  AssignClass (83b4b0d3-3ffc-457f-9155-be64d9379085)
 Call ID: 83b4b0d3-3ffc-457f-9155-be64d9379085
  Args:
    source: :InfanteJaime
    type: :Man
  AssignClass (2b8f1906-a99b-4c3c-8e6a-580af6824f96)
 Call ID: 2b8f1906-a99b-4c3c-8e6a-580af6824f96
  Args:
    type: :Person
    source: :InfanteJaime
  AddTriple (354ae647-65b9-42e4-a707-1825f638ed2a)
 Call ID: 354ae647-65b9-42e4-a707-1825f638ed2a
  Args:
    target: :AlfonsoPrinceOfAsturias
    relation: :isBrotherOf
    source: :InfanteJuan
  AddTriple (134280c8-e8ae-4c41-ac96-20f2f7375597)
 Call ID: 134280c8-e8ae-4c41-ac96-20f2f7375597
  Args:
    relation: :isBrotherOf
    target: :InfanteJaime
    source: :InfanteJuan
  AssignClass (e6cbd5ad-39fb-4a9a-9ab7-ea78871a0d51)
 Call ID: e6cbd5ad-39fb-4a9a-9ab7-ea78871a0d51
  Args:
    type: :Woman
    source: :MariaDeLasMercedes
  AssignClass (4a86ed4f-8757-4c13-873c-f9f0c83305ba)
 Call ID: 4a86ed4f-8757-4c13-873c-f9f0c83305ba
  Args:
    type: :Person
    source: :MariaDeLasMercedes
  AddLiteral (022d1b11-1bdd-445b-bdbb-120d044641cf)
 Call ID: 022d1b11-1bdd-445b-bdbb-120d044641cf
  Args:
    source: :MariaDeLasMercedes
    literal_type: xsd:integer
    literal_value: 1910
    relation: :hasBirthYear
  AddLiteral (a39c4016-898d-4ca7-bb01-ff4a9459532a)
 Call ID: a39c4016-898d-4ca7-bb01-ff4a9459532a
  Args:
    literal_value: 2000
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :MariaDeLasMercedes
  AddLiteral (065ceca4-719d-45eb-8fda-5fe24a256fe0)
 Call ID: 065ceca4-719d-45eb-8fda-5fe24a256fe0
  Args:
    literal_type: xsd:integer
    literal_value: 1935
    relation: :hasMarriageYear
    source: :InfanteJuan
  AddTriple (17c1eeed-12f9-4387-85aa-7a5e73cd7621)
 Call ID: 17c1eeed-12f9-4387-85aa-7a5e73cd7621
  Args:
    target: :MariaDeLasMercedes
    relation: :hasRelation
    source: :InfanteJuan
  AssignClass (e75d961b-2ba1-41a9-bacb-411843f828d5)
 Call ID: e75d961b-2ba1-41a9-bacb-411843f828d5
  Args:
    source: :Pilar
    type: :Woman
  AssignClass (e8dec4a8-a84c-4001-a57d-d3d3ef92245a)
 Call ID: e8dec4a8-a84c-4001-a57d-d3d3ef92245a
  Args:
    type: :Person
    source: :Pilar
  AddTriple (c2c10c21-bbfa-4646-87b0-7ba632edf707)
 Call ID: c2c10c21-bbfa-4646-87b0-7ba632edf707
  Args:
    target: :MariaDeLasMercedes
    relation: :hasMother
    source: :Pilar
  AddTriple (88842074-479a-4d8b-b834-0dd276196ef6)
 Call ID: 88842074-479a-4d8b-b834-0dd276196ef6
  Args:
    relation: :hasFather
    target: :InfanteJuan
    source: :Pilar
  AddTriple (d6f8486b-cd20-4992-93ce-4a06ec85ba54)
 Call ID: d6f8486b-cd20-4992-93ce-4a06ec85ba54
  Args:
    source: :JuanCarlosI
    target: :InfanteJuan
    relation: :hasFather
  AddTriple (a8986e60-bc07-4d57-9e0e-c96fccff6d5c)
 Call ID: a8986e60-bc07-4d57-9e0e-c96fccff6d5c
  Args:
    relation: :hasMother
    target: :MariaDeLasMercedes
    source: :JuanCarlosI
  AssignClass (f145edcd-dae2-4146-b115-7ed846374405)
 Call ID: f145edcd-dae2-4146-b115-7ed846374405
  Args:
    source: :QueenFrederica
    type: :Woman
  AssignClass (64ab5569-94e9-46cf-89c0-291563479b6f)
 Call ID: 64ab5569-94e9-46cf-89c0-291563479b6f
  Args:
    type: :Person
    source: :QueenFrederica
  AssignClass (af523188-d3fd-4f92-bae3-1b33fa8407a8)
 Call ID: af523188-d3fd-4f92-bae3-1b33fa8407a8
  Args:
    source: :KingPaul
    type: :Man
  AssignClass (c008ae9f-7eed-42db-8c1c-93749e5eb9da)
 Call ID: c008ae9f-7eed-42db-8c1c-93749e5eb9da
  Args:
    source: :KingPaul
    type: :Person
  AssignClass (508d3134-1d83-4cfc-a3a6-ef25d1c9b9a0)
 Call ID: 508d3134-1d83-4cfc-a3a6-ef25d1c9b9a0
  Args:
    source: :Sofia
    type: :Woman
  AssignClass (8d2443b9-358f-47fa-bc08-ab127352d095)
 Call ID: 8d2443b9-358f-47fa-bc08-ab127352d095
  Args:
    type: :Person
    source: :Sofia
  AddTriple (f39a1d37-9dd6-45aa-9d1a-f7f6354ab4e7)
 Call ID: f39a1d37-9dd6-45aa-9d1a-f7f6354ab4e7
  Args:
    source: :Sofia
    target: :KingPaul
    relation: :hasFather
  AddTriple (c09037ad-7a45-4a8a-a63b-7d25c820774f)
 Call ID: c09037ad-7a45-4a8a-a63b-7d25c820774f
  Args:
    relation: :hasMother
    target: :QueenFrederica
    source: :Sofia
  Finish (293c52c4-1fa0-47d5-ab8b-71fd3d402d39)
 Call ID: 293c52c4-1fa0-47d5-ab8b-71fd3d402d39
  Args: