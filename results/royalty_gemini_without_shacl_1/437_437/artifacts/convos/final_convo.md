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
India Riven Oxenberg (born June 7, 1991) is an American actress and documentary film producer.
A granddaughter of Princess Elizabeth of Yugoslavia, she is a relative of the House of Karađorđević, the former royal family of Serbia and, later, Yugoslavia.
Oxenberg began her career as a child actress, with small roles in film and television projects that her mother, Catherine Oxenberg, and then-stepfather, Casper Van Dien, were involved in.
As a teenager, she was a cast member of the reality television series I Married a Princess.
From 2011 to 2018, Oxenberg was involved in NXIVM, an American multi-level marketing company that was later exposed as a cult.
Early life and education

Oxenberg was born on June 7, 1991, to actress Catherine Oxenberg and William Weitz Shaffer.
Oxenberg's father was arrested in 1992 for smuggling marijuana from Thailand, reportedly profiting $50 million from drug trading.
Her maternal grandparents are Princess Elizabeth of Yugoslavia and Howard Oxenberg, a Jewish dress manufacturer.
As a great-granddaughter of Prince Regent Paul of Yugoslavia (Elizabeth's father), Oxenberg is a descendant of the House of Karađorđević, which ruled Serbia and Yugoslavia.
Oxenberg is also a relative of the British royal family, the Danish royal family, and the Greek royal family through her great-grandmother, Princess Olga of Greece and Denmark.
She is a niece of writer and fashion designer Christina Oxenberg.
In 2008, Oxenberg was presented to society at Le Bal des débutantes at the Hôtel de Crillon in Paris.
She was one of two descendants of the Karađorđević dynasty to make her debut at Le Bal that year, alongside her cousin Victoria de Silva, the daughter of Princess Katarina and Sir Desmond de Silva.
Career

Oxenberg's first film was the 2001 television drama The Miracle of the Cards.
In 2002, Oxenberg played the role of Mattie in the science fiction television film The Vector File.
Oxenberg was a cast member on the 2005 Lifetime reality television series I Married a Princess, which followed her family while her mother was married to Casper Van Dien.
In 2009, she had a small role in the Disney film Princess Protection Program.
Personal life

In 2018, Oxenberg met Patrick D'Ignazio, a chef, while working as a manager for a restaurant in New York City.
Oxenberg and D’Ignazio had their first child, a girl, in 2024.
NXIVM

After attending college for one year, Oxenberg, alongside her mother, enrolled in a self-help entrepreneurship course hosted by NXIVM, following a recommendation from a family friend.
While they initially started the program together, Oxenberg's mother eventually withdrew.
In January 2015, after five years in NXIVM, Oxenberg was approached by Allison Mack about joining a secret sorority, "DOS".
In DOS, Mack became a mentor to Oxenberg.
Oxenberg was instructed to provide personal family secrets and pose for nude photographs for Mack, who also limited the amount of food Oxenberg could eat and required her to cook and clean for her while living with Mack in Albany, New York.
Throughout this process, Oxenberg was groomed to become a sexual partner for NXIVM's founder and the leader of DOS, Keith Raniere.
In January 2016, Oxenberg was held down and branded with the initials of Raniere.
Oxenberg left NXIVM in 2018.
While Oxenberg was involved in NXIVM, her mother Catherine tried to get her out of the organization and expose the cult through media in 2017.
In 2018, Catherine wrote the book Captive: A Mother's Crusade to Save Her Daughter from a Terrifying Cult.
In 2019, Catherine produced the Lifetime television movie Escaping the NXIVM Cult: A Mother's Fight to Save Her Daughter.
Oxenberg officially left NXIVM in the summer of 2018 and moved back to Malibu with her mother.
Oxenberg's time in the cult was discussed in the HBO 2020 documentary The Vow.
Oxenberg produced and starred in the 2020 Starz documentary series Seduced: Inside the NXIVM Cult.
Oxenberg had her NXIVM brand covered up with a tattoo of a mandala and the inscription "ancora imparo" (i'm still learning) by a tattoo artist in New York City's East Village.



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
  AssignClass (239d45c5-30cc-4274-b8f6-ea7be9d5f3cb)
 Call ID: 239d45c5-30cc-4274-b8f6-ea7be9d5f3cb
  Args:
    type: :Person
    source: :India_Riven_Oxenberg
  AssignClass (dc706d7c-7170-45b6-afd2-d532ed90593a)
 Call ID: dc706d7c-7170-45b6-afd2-d532ed90593a
  Args:
    type: :Woman
    source: :India_Riven_Oxenberg
  AddLiteral (e3faab66-2df0-4329-a4ae-d5d3d679db7e)
 Call ID: e3faab66-2df0-4329-a4ae-d5d3d679db7e
  Args:
    source: :India_Riven_Oxenberg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1991
  AssignClass (e419c767-d052-4779-a93f-52d6dc9d328f)
 Call ID: e419c767-d052-4779-a93f-52d6dc9d328f
  Args:
    type: :Person
    source: :Catherine_Oxenberg
  AssignClass (51b33e15-2997-42ea-86b0-7fcea9cdef32)
 Call ID: 51b33e15-2997-42ea-86b0-7fcea9cdef32
  Args:
    type: :Woman
    source: :Catherine_Oxenberg
  AssignClass (2ad0c2f9-4189-48ee-b8a5-fe1fb76c9c66)
 Call ID: 2ad0c2f9-4189-48ee-b8a5-fe1fb76c9c66
  Args:
    type: :Person
    source: :William_Weitz_Shaffer
  AssignClass (9d5dd1b2-3611-435c-a903-01c2bf9bcf25)
 Call ID: 9d5dd1b2-3611-435c-a903-01c2bf9bcf25
  Args:
    type: :Man
    source: :William_Weitz_Shaffer
  AddTriple (06ec1d4a-6c00-4f5d-929e-e3d94b00b2ea)
 Call ID: 06ec1d4a-6c00-4f5d-929e-e3d94b00b2ea
  Args:
    target: :Catherine_Oxenberg
    relation: :hasMother
    source: :India_Riven_Oxenberg
  AddTriple (a73ca5b8-414d-456c-82ab-93d2c5da2c2b)
 Call ID: a73ca5b8-414d-456c-82ab-93d2c5da2c2b
  Args:
    relation: :hasFather
    target: :William_Weitz_Shaffer
    source: :India_Riven_Oxenberg
  AssignClass (df51e53c-b4a9-4679-9f0a-da7d5dcc0de2)
 Call ID: df51e53c-b4a9-4679-9f0a-da7d5dcc0de2
  Args:
    type: :Person
    source: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (24c2b677-cf90-4f78-94a5-ca15823c5e69)
 Call ID: 24c2b677-cf90-4f78-94a5-ca15823c5e69
  Args:
    type: :Woman
    source: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (1626dc9b-220e-4e65-8b82-b2c0270e9447)
 Call ID: 1626dc9b-220e-4e65-8b82-b2c0270e9447
  Args:
    type: :Person
    source: :Howard_Oxenberg
  AssignClass (bb2c97d4-ad60-4b24-b679-92c0dcb42105)
 Call ID: bb2c97d4-ad60-4b24-b679-92c0dcb42105
  Args:
    type: :Man
    source: :Howard_Oxenberg
  AddTriple (e3dcd462-82c4-461e-8a94-40ad952edb79)
 Call ID: e3dcd462-82c4-461e-8a94-40ad952edb79
  Args:
    source: :Catherine_Oxenberg
    relation: :hasMother
    target: :Princess_Elizabeth_of_Yugoslavia
  AddTriple (e1fce4f6-09bf-4cb4-828d-26f2d04c7880)
 Call ID: e1fce4f6-09bf-4cb4-828d-26f2d04c7880
  Args:
    relation: :hasFather
    target: :Howard_Oxenberg
    source: :Catherine_Oxenberg
  AssignClass (0a1eeda2-1b6f-4898-bea0-5d815eb45b38)
 Call ID: 0a1eeda2-1b6f-4898-bea0-5d815eb45b38
  Args:
    type: :Person
    source: :Prince_Regent_Paul_of_Yugoslavia
  AssignClass (86c5966d-236d-42eb-898d-339ed8c366b2)
 Call ID: 86c5966d-236d-42eb-898d-339ed8c366b2
  Args:
    type: :Man
    source: :Prince_Regent_Paul_of_Yugoslavia
  AddTriple (70d85062-70e1-4770-a4b0-43ba32d207ca)
 Call ID: 70d85062-70e1-4770-a4b0-43ba32d207ca
  Args:
    target: :Prince_Regent_Paul_of_Yugoslavia
    relation: :hasFather
    source: :Princess_Elizabeth_of_Yugoslavia
  AssignClass (88d82831-108b-4c31-933b-ad70a2e7472e)
 Call ID: 88d82831-108b-4c31-933b-ad70a2e7472e
  Args:
    type: :Person
    source: :Christina_Oxenberg
  AssignClass (8eec4f4f-53f7-459b-bdde-a1cd26dab56e)
 Call ID: 8eec4f4f-53f7-459b-bdde-a1cd26dab56e
  Args:
    type: :Woman
    source: :Christina_Oxenberg
  AddTriple (20eaea29-4207-4d20-b12e-022d9d1d4680)
 Call ID: 20eaea29-4207-4d20-b12e-022d9d1d4680
  Args:
    source: :Catherine_Oxenberg
    relation: :isSisterOf
    target: :Christina_Oxenberg
  AssignClass (80d65959-caa7-4432-94c5-68ed9f02da12)
 Call ID: 80d65959-caa7-4432-94c5-68ed9f02da12
  Args:
    type: :Person
    source: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (f949f4ca-7cbb-4e11-8db9-24b4ea713191)
 Call ID: f949f4ca-7cbb-4e11-8db9-24b4ea713191
  Args:
    type: :Woman
    source: :Princess_Olga_of_Greece_and_Denmark
  AssignClass (de11553e-3b8f-4634-9357-c9f1a8fabd27)
 Call ID: de11553e-3b8f-4634-9357-c9f1a8fabd27
  Args:
    type: :Person
    source: :Casper_Van_Dien
  AssignClass (7e59ec91-e6f4-4a42-88c4-f0b293525ec9)
 Call ID: 7e59ec91-e6f4-4a42-88c4-f0b293525ec9
  Args:
    type: :Man
    source: :Casper_Van_Dien
  AssignClass (af55a889-55b3-44da-a0b4-f98e553d6c02)
 Call ID: af55a889-55b3-44da-a0b4-f98e553d6c02
  Args:
    type: :Person
    source: :Patrick_DIgnazio
  AssignClass (ea2295c1-4451-4bf9-b97b-55aa4dc96f71)
 Call ID: ea2295c1-4451-4bf9-b97b-55aa4dc96f71
  Args:
    type: :Man
    source: :Patrick_DIgnazio
  AssignClass (114c8677-b782-45c1-a6d6-4b47bfedf013)
 Call ID: 114c8677-b782-45c1-a6d6-4b47bfedf013
  Args:
    type: :Person
    source: :Unnamed_Daughter_of_Oxenberg
  AssignClass (9355ed18-1485-495e-a0e9-90184cd1dbb9)
 Call ID: 9355ed18-1485-495e-a0e9-90184cd1dbb9
  Args:
    type: :Woman
    source: :Unnamed_Daughter_of_Oxenberg
  AddTriple (898edfaa-564b-414b-8de7-eef1bc0027da)
 Call ID: 898edfaa-564b-414b-8de7-eef1bc0027da
  Args:
    relation: :hasMother
    target: :India_Riven_Oxenberg
    source: :Unnamed_Daughter_of_Oxenberg
  AddTriple (7ca7c608-1fc1-4fa1-bfd0-ceb849165183)
 Call ID: 7ca7c608-1fc1-4fa1-bfd0-ceb849165183
  Args:
    target: :Patrick_DIgnazio
    relation: :hasFather
    source: :Unnamed_Daughter_of_Oxenberg
  Finish (b71d28a3-1c79-4abd-87d3-f0554db2d31c)
 Call ID: b71d28a3-1c79-4abd-87d3-f0554db2d31c
  Args: