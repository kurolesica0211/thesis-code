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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (016f21af-06ee-4895-ad3d-0c73710a0c53)
 Call ID: 016f21af-06ee-4895-ad3d-0c73710a0c53
  Args:
    source: :Juan_Count_of_Barcelona
    type: :Man
  AddLiteral (ca1b0ac2-f12e-475c-8e7e-ceff04d217d1)
 Call ID: ca1b0ac2-f12e-475c-8e7e-ceff04d217d1
  Args:
    source: :Juan_Count_of_Barcelona
    literal_type: xsd:string
    literal_value: Juan Carlos Teresa Silverio Alfonso de Borbón y Battenberg
    relation: :alsoKnownAs
  AddLiteral (4e955da6-d8f4-4d4e-a939-77ec5147cfd5)
 Call ID: 4e955da6-d8f4-4d4e-a939-77ec5147cfd5
  Args:
    source: :Juan_Count_of_Barcelona
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1913
  AddLiteral (fbd9c729-b006-4319-9b21-1fb68df0bdb9)
 Call ID: fbd9c729-b006-4319-9b21-1fb68df0bdb9
  Args:
    source: :Juan_Count_of_Barcelona
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1993
  AssignClass (5983e2c3-1407-4783-aa1a-e2f74ee632d8)
 Call ID: 5983e2c3-1407-4783-aa1a-e2f74ee632d8
  Args:
    source: :Alfonso_XIII
    type: :Man
  AssignClass (3523d6f9-8aa2-4718-8a70-47a9e2deba4c)
 Call ID: 3523d6f9-8aa2-4718-8a70-47a9e2deba4c
  Args:
    type: :Woman
    source: :Victoria_Eugenie_of_Battenberg
  AddTriple (8d527f68-5f67-44b7-90a0-927a4da9e4e6)
 Call ID: 8d527f68-5f67-44b7-90a0-927a4da9e4e6
  Args:
    relation: :hasFather
    target: :Alfonso_XIII
    source: :Juan_Count_of_Barcelona
  AddTriple (fccd581f-6bbb-49fe-a971-88038d28ac52)
 Call ID: fccd581f-6bbb-49fe-a971-88038d28ac52
  Args:
    source: :Juan_Count_of_Barcelona
    relation: :hasMother
    target: :Victoria_Eugenie_of_Battenberg
  AssignClass (65f304da-c5f4-4705-8c76-63dabfd49e19)
 Call ID: 65f304da-c5f4-4705-8c76-63dabfd49e19
  Args:
    type: :Man
    source: :Juan_Carlos_I
  AddTriple (d206f2ea-866f-4cd3-ab50-1739a48809bf)
 Call ID: d206f2ea-866f-4cd3-ab50-1739a48809bf
  Args:
    relation: :isSonOf
    target: :Juan_Count_of_Barcelona
    source: :Juan_Carlos_I
  AssignClass (bd889988-0727-49ae-ad8f-6c010048df36)
 Call ID: bd889988-0727-49ae-ad8f-6c010048df36
  Args:
    source: :Alfonso_Prince_of_Asturias
    type: :Man
  AssignClass (ee35cead-2a37-465f-b306-3d091dd14e6a)
 Call ID: ee35cead-2a37-465f-b306-3d091dd14e6a
  Args:
    source: :Jaime_Duke_of_Segovia
    type: :Man
  AddTriple (699e135d-5168-43d3-858a-6e2147c1362f)
 Call ID: 699e135d-5168-43d3-858a-6e2147c1362f
  Args:
    relation: :isBrotherOf
    target: :Juan_Count_of_Barcelona
    source: :Alfonso_Prince_of_Asturias
  AddTriple (d87a3634-8444-49c0-9cd4-0e2c5c904fce)
 Call ID: d87a3634-8444-49c0-9cd4-0e2c5c904fce
  Args:
    relation: :isBrotherOf
    target: :Juan_Count_of_Barcelona
    source: :Jaime_Duke_of_Segovia
  AssignClass (a7da7c6d-8344-4d83-850d-3ef72b8b2007)
 Call ID: a7da7c6d-8344-4d83-850d-3ef72b8b2007
  Args:
    source: :Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
    type: :Woman
  AddLiteral (790c0bac-d685-4d12-88a5-952a87966796)
 Call ID: 790c0bac-d685-4d12-88a5-952a87966796
  Args:
    source: :Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
    literal_type: xsd:integer
    literal_value: 1910
    relation: :hasBirthYear
  AddLiteral (f3f6c762-46f6-403e-bf43-1ca6f3c10876)
 Call ID: f3f6c762-46f6-403e-bf43-1ca6f3c10876
  Args:
    literal_value: 2000
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
  AddLiteral (ba68fab3-0dd9-4a99-a6f7-dac081a716c9)
 Call ID: ba68fab3-0dd9-4a99-a6f7-dac081a716c9
  Args:
    literal_value: 1935
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Juan_Count_of_Barcelona
  AddTriple (318ca84b-a641-466e-a5ad-38148b87d8ad)
 Call ID: 318ca84b-a641-466e-a5ad-38148b87d8ad
  Args:
    source: :Juan_Count_of_Barcelona
    relation: :hasRelation
    target: :Maria_de_las_Mercedes_of_Bourbon_Two_Sicilies
  AssignClass (f746720d-00f6-4fd1-bb73-a94b27fdc56d)
 Call ID: f746720d-00f6-4fd1-bb73-a94b27fdc56d
  Args:
    type: :Woman
    source: :Pilar
  AddTriple (6cabddcb-d81d-4fde-b1ad-dc87e23f0d92)
 Call ID: 6cabddcb-d81d-4fde-b1ad-dc87e23f0d92
  Args:
    relation: :isChildOf
    target: :Juan_Count_of_Barcelona
    source: :Pilar
  AddTriple (1faa27fb-2261-4d4d-986e-9e09978f5c20)
 Call ID: 1faa27fb-2261-4d4d-986e-9e09978f5c20
  Args:
    source: :Juan_Carlos_I
    target: :Juan_Count_of_Barcelona
    relation: :isChildOf
  AssignClass (fe900588-8f06-4e62-8a7d-59f4dc0804c1)
 Call ID: fe900588-8f06-4e62-8a7d-59f4dc0804c1
  Args:
    source: :Sofia
    type: :Woman
  AddTriple (5e087a4e-daab-4048-97c6-c718df2ecc9d)
 Call ID: 5e087a4e-daab-4048-97c6-c718df2ecc9d
  Args:
    relation: :hasRelation
    target: :Sofia
    source: :Juan_Carlos_I
  Finish (ab8ed95e-06cf-4529-9070-8141fb6485a3)
 Call ID: ab8ed95e-06cf-4529-9070-8141fb6485a3
  Args: