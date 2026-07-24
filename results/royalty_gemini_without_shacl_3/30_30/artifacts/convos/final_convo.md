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
  AssignClass (da890c58-733b-4939-9419-eca09e34433d)
 Call ID: da890c58-733b-4939-9419-eca09e34433d
  Args:
    type: :Woman
    source: :Alexandra_of_Hanover
  AssignClass (86836a9a-0b0d-454e-b08a-b99338b3c113)
 Call ID: 86836a9a-0b0d-454e-b08a-b99338b3c113
  Args:
    type: :Person
    source: :Alexandra_of_Hanover
  AddLiteral (dc2a7aa7-65ae-458e-8ea4-626e2f98cbdc)
 Call ID: dc2a7aa7-65ae-458e-8ea4-626e2f98cbdc
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Alexandra_of_Hanover
    literal_value: 1999
  AssignClass (d38f603a-994e-4263-bf20-fbace72fad6e)
 Call ID: d38f603a-994e-4263-bf20-fbace72fad6e
  Args:
    type: :Woman
    source: :Princess_Caroline_of_Monaco
  AssignClass (880713dc-ec02-4c62-a469-c1776b591640)
 Call ID: 880713dc-ec02-4c62-a469-c1776b591640
  Args:
    type: :Person
    source: :Princess_Caroline_of_Monaco
  AssignClass (a043756a-dee3-488a-82e8-494974384844)
 Call ID: a043756a-dee3-488a-82e8-494974384844
  Args:
    type: :Man
    source: :Ernst_August_Prince_of_Hanover
  AssignClass (f2d3912f-3d0d-401f-9e36-1d5ce9c75367)
 Call ID: f2d3912f-3d0d-401f-9e36-1d5ce9c75367
  Args:
    type: :Person
    source: :Ernst_August_Prince_of_Hanover
  AddTriple (301d2a01-aedb-4769-8b22-914f07895e44)
 Call ID: 301d2a01-aedb-4769-8b22-914f07895e44
  Args:
    source: :Alexandra_of_Hanover
    relation: :hasMother
    target: :Princess_Caroline_of_Monaco
  AddTriple (795fae40-425a-44e5-8e74-99dfe16ee447)
 Call ID: 795fae40-425a-44e5-8e74-99dfe16ee447
  Args:
    source: :Alexandra_of_Hanover
    relation: :hasFather
    target: :Ernst_August_Prince_of_Hanover
  AssignClass (580d2fe6-5876-4a2b-9b62-db0dec8c0633)
 Call ID: 580d2fe6-5876-4a2b-9b62-db0dec8c0633
  Args:
    type: :Man
    source: :Ernst_August_Hereditary_Prince
  AssignClass (62037c29-4d93-426d-a4b1-ed377bd77292)
 Call ID: 62037c29-4d93-426d-a4b1-ed377bd77292
  Args:
    type: :Person
    source: :Ernst_August_Hereditary_Prince
  AssignClass (2289b1a2-188e-4335-a0fb-41e18895dce7)
 Call ID: 2289b1a2-188e-4335-a0fb-41e18895dce7
  Args:
    type: :Man
    source: :Prince_Christian_of_Hanover
  AssignClass (4dd3b657-aafc-4384-80fa-94a31f806de9)
 Call ID: 4dd3b657-aafc-4384-80fa-94a31f806de9
  Args:
    type: :Person
    source: :Prince_Christian_of_Hanover
  AddTriple (2219030f-11ae-4386-b433-4614098f6a3e)
 Call ID: 2219030f-11ae-4386-b433-4614098f6a3e
  Args:
    target: :Ernst_August_Hereditary_Prince
    source: :Alexandra_of_Hanover
    relation: :hasBrother
  AddTriple (87e2f504-4170-44fc-9752-c337638346a4)
 Call ID: 87e2f504-4170-44fc-9752-c337638346a4
  Args:
    target: :Prince_Christian_of_Hanover
    source: :Alexandra_of_Hanover
    relation: :hasBrother
  AssignClass (a5c9a900-7ecd-48ce-aeb0-0b46acf518ed)
 Call ID: a5c9a900-7ecd-48ce-aeb0-0b46acf518ed
  Args:
    type: :Man
    source: :Albert_II_of_Monaco
  AssignClass (65441a55-a018-4d02-8ab0-87738075def0)
 Call ID: 65441a55-a018-4d02-8ab0-87738075def0
  Args:
    type: :Person
    source: :Albert_II_of_Monaco
  AddTriple (f7afde4f-3cf5-4688-bb2e-074868a53bc2)
 Call ID: f7afde4f-3cf5-4688-bb2e-074868a53bc2
  Args:
    target: :Alexandra_of_Hanover
    source: :Albert_II_of_Monaco
    relation: :isUncleOf
  AssignClass (66fe6a8f-dfa8-4657-ba6e-3bed2cb71a36)
 Call ID: 66fe6a8f-dfa8-4657-ba6e-3bed2cb71a36
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (e6ba23fe-a830-41e0-97d3-5f12f739f574)
 Call ID: e6ba23fe-a830-41e0-97d3-5f12f739f574
  Args:
    type: :Person
    source: :Queen_Victoria
  AssignClass (f8fcaaf9-0719-4394-9d77-c7b01e3dd4c8)
 Call ID: f8fcaaf9-0719-4394-9d77-c7b01e3dd4c8
  Args:
    type: :Man
    source: :Wilhelm_II_German_Emperor
  AssignClass (6ab5cb6d-15f9-45f8-b6fd-112fdc09c147)
 Call ID: 6ab5cb6d-15f9-45f8-b6fd-112fdc09c147
  Args:
    type: :Person
    source: :Wilhelm_II_German_Emperor
  AssignClass (4cb1a322-d687-4670-a116-be2940551b0a)
 Call ID: 4cb1a322-d687-4670-a116-be2940551b0a
  Args:
    type: :Man
    source: :Christian_IX_of_Denmark
  AssignClass (ad7a8744-0224-464f-89cb-6285f16c3ca9)
 Call ID: ad7a8744-0224-464f-89cb-6285f16c3ca9
  Args:
    type: :Person
    source: :Christian_IX_of_Denmark
  AddTriple (017dceeb-4194-4fb4-b548-e9628e1364ba)
 Call ID: 017dceeb-4194-4fb4-b548-e9628e1364ba
  Args:
    target: :Queen_Victoria
    source: :Alexandra_of_Hanover
    relation: :hasAncestor
  AddTriple (31f4d17d-c936-479b-a4a3-450111f2f353)
 Call ID: 31f4d17d-c936-479b-a4a3-450111f2f353
  Args:
    target: :Wilhelm_II_German_Emperor
    relation: :hasAncestor
    source: :Alexandra_of_Hanover
  AddTriple (415ec5d5-3a12-42bd-80b4-91fedc46d56f)
 Call ID: 415ec5d5-3a12-42bd-80b4-91fedc46d56f
  Args:
    target: :Christian_IX_of_Denmark
    relation: :hasAncestor
    source: :Alexandra_of_Hanover
  Finish (33bf9f4f-82cd-4409-836e-4f8254a25027)
 Call ID: 33bf9f4f-82cd-4409-836e-4f8254a25027
  Args: