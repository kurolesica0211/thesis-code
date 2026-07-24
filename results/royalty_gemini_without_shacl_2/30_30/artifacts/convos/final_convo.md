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
Princess Alexandra of Hanover (Alexandra Charlotte Ulrike Maryam Virginia; born 20 July 1999) is a Monegasque figure skater and the fourth child of Princess Caroline of Monaco and the third of Ernst August, Prince of Hanover.
Family

Alexandra was born on 20 July 1999 in Vöcklabruck, Upper Austria.
She was christened on 19 September that year by Horst Hirschler, Landesbischof of the Evangelical-Lutheran Church of Hanover, in a ceremony at her father's hunting lodge Auerbach, near Grünau im Almtal, Upper Austria.
Her godparents are her paternal aunt Alexandra, Princess of Leiningen, maternal half-sister Charlotte Casiraghi, Ulrike Ulmschneider, Maryam Sachs, Virginia Gallico, George Condo, and Eric Maier.
From her father's previous marriage, she has two half-brothers, Hereditary Prince Ernst August and Prince Christian of Hanover.
Her maternal uncle, Albert II, is the sovereign of Monaco.
On her father's side, she is a descendant of Queen Victoria of the United Kingdom, Wilhelm II, German Emperor, and King Christian IX of Denmark.
Alexandra is the only one of Princess Caroline's four children who bears any royal style or title.
While she is formally styled as Her Royal Highness Princess Alexandra of Hanover in Monaco, she is afforded the style and title out of courtesy elsewhere.
Early life, education, and career

Initially enrolled in public school in Le Mée-sur-Seine, near Paris, she finished her primary and secondary schooling Monaco.
Figure skating career

Alexandra began skating when she was ten years old after receiving ice skates as a Christmas present.
At the age of 12, she competed in the "Skate 7" class at the 10th Figure Skating Championship in Monaco, finishing in second place.
Alexandra represented Monaco in figure skating at the 2015 European Youth Olympic Festival in Austria and in two competitive events during the 2015–16 season at the ISU Junior Grand Prix of Figure Skating.
Junior Grand Prix


Programs

Competitive highlights

Detailed results

Personal life

When Alexandra was 11 years old, German entertainment magazine Freizeit Revue published an article about and photographs of her competing at a figure skating competition in France.
Alexandra sought injunctive relief and sued the magazine, taking the case to the German Federal Court of Justice.
In March 2015, Alexandra attended Monaco's Rose Ball for the first time.
In October 2018, Alexandra converted to Catholicism, thereby renouncing her distant place in the line of succession to the British throne.



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
  AssignClass (073d0172-d848-46c5-b93e-448fe496538f)
 Call ID: 073d0172-d848-46c5-b93e-448fe496538f
  Args:
    type: :Woman
    source: Alexandra_of_Hanover
  AssignClass (684b290d-8151-4018-92a2-3cdd944c1c0a)
 Call ID: 684b290d-8151-4018-92a2-3cdd944c1c0a
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddLiteral (5b4cf208-8c8b-414c-b02c-a916fbf2b615)
 Call ID: 5b4cf208-8c8b-414c-b02c-a916fbf2b615
  Args:
    source: Alexandra_of_Hanover
    literal_value: 1999
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (16ea4c1c-e4c9-4226-808d-ae56be164366)
 Call ID: 16ea4c1c-e4c9-4226-808d-ae56be164366
  Args:
    type: :Woman
    source: Princess_Caroline_of_Monaco
  AssignClass (4cb2cc80-4913-480e-a58f-364235d210e4)
 Call ID: 4cb2cc80-4913-480e-a58f-364235d210e4
  Args:
    type: :Person
    source: Princess_Caroline_of_Monaco
  AssignClass (1dccd6fd-a990-4afd-9c89-efa635bff4e4)
 Call ID: 1dccd6fd-a990-4afd-9c89-efa635bff4e4
  Args:
    type: :Man
    source: Ernst_August_Prince_of_Hanover
  AssignClass (3b411fbb-0c8d-45dc-a7dd-5186da126564)
 Call ID: 3b411fbb-0c8d-45dc-a7dd-5186da126564
  Args:
    type: :Person
    source: Ernst_August_Prince_of_Hanover
  AddTriple (44dad47a-c3d4-4a8c-8a4d-16d049daa587)
 Call ID: 44dad47a-c3d4-4a8c-8a4d-16d049daa587
  Args:
    target: Princess_Caroline_of_Monaco
    source: Alexandra_of_Hanover
    relation: :hasMother
  AddTriple (62939e3a-eddb-4413-9193-bd14b777a039)
 Call ID: 62939e3a-eddb-4413-9193-bd14b777a039
  Args:
    target: Ernst_August_Prince_of_Hanover
    source: Alexandra_of_Hanover
    relation: :hasFather
  AssignClass (26f4b0e1-c639-4a37-9f1c-973148cf029f)
 Call ID: 26f4b0e1-c639-4a37-9f1c-973148cf029f
  Args:
    type: :Man
    source: Hereditary_Prince_Ernst_August
  AssignClass (de4861f8-44a3-4179-b98f-4534d6ea210c)
 Call ID: de4861f8-44a3-4179-b98f-4534d6ea210c
  Args:
    type: :Person
    source: Hereditary_Prince_Ernst_August
  AssignClass (88deaa13-94c6-42c0-9da7-4e03afa3f625)
 Call ID: 88deaa13-94c6-42c0-9da7-4e03afa3f625
  Args:
    type: :Man
    source: Prince_Christian_of_Hanover
  AssignClass (79fbc15f-f74e-433f-b9c6-9ee59ffb3502)
 Call ID: 79fbc15f-f74e-433f-b9c6-9ee59ffb3502
  Args:
    type: :Person
    source: Prince_Christian_of_Hanover
  AddTriple (30a2dd55-bb0c-42b6-ab9c-db6e032ad297)
 Call ID: 30a2dd55-bb0c-42b6-ab9c-db6e032ad297
  Args:
    target: Ernst_August_Prince_of_Hanover
    source: Hereditary_Prince_Ernst_August
    relation: :hasFather
  AddTriple (83f41ca1-cc6a-4704-814c-3cc904aed0e7)
 Call ID: 83f41ca1-cc6a-4704-814c-3cc904aed0e7
  Args:
    relation: :hasFather
    source: Prince_Christian_of_Hanover
    target: Ernst_August_Prince_of_Hanover
  AssignClass (07522242-68e0-41c5-8cda-720d5ef429fa)
 Call ID: 07522242-68e0-41c5-8cda-720d5ef429fa
  Args:
    type: :Man
    source: Albert_II_of_Monaco
  AssignClass (c1cda241-b6cf-46f1-af78-0813b8de8a83)
 Call ID: c1cda241-b6cf-46f1-af78-0813b8de8a83
  Args:
    type: :Person
    source: Albert_II_of_Monaco
  AddTriple (51e969d9-b4e3-40df-bbb8-ab0e61cadfd7)
 Call ID: 51e969d9-b4e3-40df-bbb8-ab0e61cadfd7
  Args:
    source: Albert_II_of_Monaco
    target: Princess_Caroline_of_Monaco
    relation: :hasSister
  AssignClass (4707b0a0-2683-4389-8f73-0bb387de077e)
 Call ID: 4707b0a0-2683-4389-8f73-0bb387de077e
  Args:
    type: :Woman
    source: Queen_Victoria_of_the_United_Kingdom
  AssignClass (541220d4-f585-408c-9e7a-ec9968074a3c)
 Call ID: 541220d4-f585-408c-9e7a-ec9968074a3c
  Args:
    type: :Ancestor
    source: Queen_Victoria_of_the_United_Kingdom
  AssignClass (4e88ca88-84e4-401f-aa99-372f05c0a775)
 Call ID: 4e88ca88-84e4-401f-aa99-372f05c0a775
  Args:
    type: :Man
    source: Wilhelm_II_German_Emperor
  AssignClass (52955118-65bc-40f6-8e29-7ab992adda6c)
 Call ID: 52955118-65bc-40f6-8e29-7ab992adda6c
  Args:
    type: :Ancestor
    source: Wilhelm_II_German_Emperor
  AssignClass (fd1b4b0a-9d1d-4db7-8231-cfdbb643863f)
 Call ID: fd1b4b0a-9d1d-4db7-8231-cfdbb643863f
  Args:
    type: :Man
    source: King_Christian_IX_of_Denmark
  AssignClass (15c091f5-27d5-4a97-b419-d4e1ded8ef81)
 Call ID: 15c091f5-27d5-4a97-b419-d4e1ded8ef81
  Args:
    type: :Ancestor
    source: King_Christian_IX_of_Denmark
  AddTriple (5a662fbe-8d29-4388-beab-276e1abea415)
 Call ID: 5a662fbe-8d29-4388-beab-276e1abea415
  Args:
    target: Queen_Victoria_of_the_United_Kingdom
    source: Alexandra_of_Hanover
    relation: :hasAncestor
  AddTriple (9c09de78-f46e-48ff-be2e-1ffbd08ffee9)
 Call ID: 9c09de78-f46e-48ff-be2e-1ffbd08ffee9
  Args:
    relation: :hasAncestor
    source: Alexandra_of_Hanover
    target: Wilhelm_II_German_Emperor
  AddTriple (ba699c52-ed58-4976-badf-f5b21dc058b2)
 Call ID: ba699c52-ed58-4976-badf-f5b21dc058b2
  Args:
    source: Alexandra_of_Hanover
    target: King_Christian_IX_of_Denmark
    relation: :hasAncestor
  Finish (bcc82127-75e2-4c41-8f4a-1535fc563690)
 Call ID: bcc82127-75e2-4c41-8f4a-1535fc563690
  Args: