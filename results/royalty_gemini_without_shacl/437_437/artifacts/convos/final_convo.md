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
  AssignClass (dc8f453e-eccf-4935-b7be-7a3c6968cb4e)
 Call ID: dc8f453e-eccf-4935-b7be-7a3c6968cb4e
  Args:
    source: India_Riven_Oxenberg
    type: :Person
  AssignClass (e4e10211-0912-47b0-9800-3162bfd7d8fe)
 Call ID: e4e10211-0912-47b0-9800-3162bfd7d8fe
  Args:
    type: :Woman
    source: India_Riven_Oxenberg
  AddLiteral (7e4f7421-ff43-4100-9fe6-84091ec73158)
 Call ID: 7e4f7421-ff43-4100-9fe6-84091ec73158
  Args:
    source: India_Riven_Oxenberg
    literal_value: 1991
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (f0dac1f0-7b5f-4602-b21a-21ca11e73b97)
 Call ID: f0dac1f0-7b5f-4602-b21a-21ca11e73b97
  Args:
    type: :Person
    source: Catherine_Oxenberg
  AssignClass (94d7bec8-da46-4713-afa1-aa78507780b8)
 Call ID: 94d7bec8-da46-4713-afa1-aa78507780b8
  Args:
    type: :Woman
    source: Catherine_Oxenberg
  AssignClass (42f425dc-bed6-4577-8e1a-6bd8618e1255)
 Call ID: 42f425dc-bed6-4577-8e1a-6bd8618e1255
  Args:
    type: :Person
    source: William_Weitz_Shaffer
  AssignClass (c88179e3-a7aa-4751-89ab-7ed4bbb5dde5)
 Call ID: c88179e3-a7aa-4751-89ab-7ed4bbb5dde5
  Args:
    source: William_Weitz_Shaffer
    type: :Man
  AddTriple (42b3251e-2af8-419c-a502-27a29e4e84f0)
 Call ID: 42b3251e-2af8-419c-a502-27a29e4e84f0
  Args:
    target: Catherine_Oxenberg
    source: India_Riven_Oxenberg
    relation: :hasMother
  AddTriple (b5464e59-ea44-44da-b6ae-db0af8df4ee2)
 Call ID: b5464e59-ea44-44da-b6ae-db0af8df4ee2
  Args:
    relation: :hasFather
    target: William_Weitz_Shaffer
    source: India_Riven_Oxenberg
  AssignClass (90edbb6f-1af9-452f-8dc0-481b6521e2c7)
 Call ID: 90edbb6f-1af9-452f-8dc0-481b6521e2c7
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Person
  AssignClass (5faa83bb-168c-44c7-9f00-8c345de6d89f)
 Call ID: 5faa83bb-168c-44c7-9f00-8c345de6d89f
  Args:
    type: :Woman
    source: Princess_Elizabeth_of_Yugoslavia
  AssignClass (339ad8e4-ed59-4aed-843e-07091bc127ea)
 Call ID: 339ad8e4-ed59-4aed-843e-07091bc127ea
  Args:
    source: Howard_Oxenberg
    type: :Person
  AssignClass (2bc62c73-94f8-4e20-9def-e54ccf03a18c)
 Call ID: 2bc62c73-94f8-4e20-9def-e54ccf03a18c
  Args:
    type: :Man
    source: Howard_Oxenberg
  AddTriple (d90c5ce5-1ab7-4f6a-99bf-807ce0a600df)
 Call ID: d90c5ce5-1ab7-4f6a-99bf-807ce0a600df
  Args:
    target: Princess_Elizabeth_of_Yugoslavia
    source: Catherine_Oxenberg
    relation: :hasMother
  AddTriple (278254bf-9071-4730-b8f3-b498bc6695ee)
 Call ID: 278254bf-9071-4730-b8f3-b498bc6695ee
  Args:
    relation: :hasFather
    target: Howard_Oxenberg
    source: Catherine_Oxenberg
  AssignClass (290fc6c0-b5df-4e81-849e-7c9b87e78577)
 Call ID: 290fc6c0-b5df-4e81-849e-7c9b87e78577
  Args:
    type: :Person
    source: Prince_Regent_Paul_of_Yugoslavia
  AssignClass (019487b2-4ecd-4970-b9d8-b0910ba130c3)
 Call ID: 019487b2-4ecd-4970-b9d8-b0910ba130c3
  Args:
    source: Prince_Regent_Paul_of_Yugoslavia
    type: :Man
  AddTriple (65a2aa59-4fae-4678-8fbd-79cc834a9ccb)
 Call ID: 65a2aa59-4fae-4678-8fbd-79cc834a9ccb
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    target: Prince_Regent_Paul_of_Yugoslavia
    relation: :hasFather
  AssignClass (87f17c4e-601d-4203-8d7b-5c9f40b41713)
 Call ID: 87f17c4e-601d-4203-8d7b-5c9f40b41713
  Args:
    type: :Person
    source: Christina_Oxenberg
  AssignClass (05b66b30-c33c-47a7-abed-5dfdb44bc2ea)
 Call ID: 05b66b30-c33c-47a7-abed-5dfdb44bc2ea
  Args:
    source: Christina_Oxenberg
    type: :Woman
  AddTriple (407a7b11-9581-43b4-8d84-b27c3993a604)
 Call ID: 407a7b11-9581-43b4-8d84-b27c3993a604
  Args:
    relation: :isSisterOf
    target: Catherine_Oxenberg
    source: Christina_Oxenberg
  AssignClass (c58a367f-12da-448d-a11a-928a909159c3)
 Call ID: c58a367f-12da-448d-a11a-928a909159c3
  Args:
    type: :Person
    source: Casper_Van_Dien
  AssignClass (afac3b0d-fe76-4e2f-a3d6-9fafc72f9625)
 Call ID: afac3b0d-fe76-4e2f-a3d6-9fafc72f9625
  Args:
    type: :Man
    source: Casper_Van_Dien
  AssignClass (0811c069-f5f9-43d8-9f77-a4808d5d8476)
 Call ID: 0811c069-f5f9-43d8-9f77-a4808d5d8476
  Args:
    source: Victoria_de_Silva
    type: :Person
  AssignClass (11e6460b-27c7-4c8c-8355-04522e5119aa)
 Call ID: 11e6460b-27c7-4c8c-8355-04522e5119aa
  Args:
    source: Victoria_de_Silva
    type: :Woman
  AssignClass (e2ab944a-3a3d-43db-9cbb-85cce0adb0d4)
 Call ID: e2ab944a-3a3d-43db-9cbb-85cce0adb0d4
  Args:
    type: :Person
    source: Princess_Katarina
  AssignClass (47caf427-a3fc-4f94-bd9c-a8521bcefdb2)
 Call ID: 47caf427-a3fc-4f94-bd9c-a8521bcefdb2
  Args:
    source: Princess_Katarina
    type: :Woman
  AssignClass (d17b5429-5d47-4b1d-b4ee-4bd585894ecb)
 Call ID: d17b5429-5d47-4b1d-b4ee-4bd585894ecb
  Args:
    type: :Person
    source: Sir_Desmond_de_Silva
  AssignClass (b57a7e7a-9fda-4100-b8cd-5024c4d7879e)
 Call ID: b57a7e7a-9fda-4100-b8cd-5024c4d7879e
  Args:
    type: :Man
    source: Sir_Desmond_de_Silva
  AddTriple (6f0d5579-1777-4892-a2df-c211d6c2c8ab)
 Call ID: 6f0d5579-1777-4892-a2df-c211d6c2c8ab
  Args:
    relation: :hasMother
    target: Princess_Katarina
    source: Victoria_de_Silva
  AddTriple (9eda92c3-9545-44bb-b928-a003141abcf6)
 Call ID: 9eda92c3-9545-44bb-b928-a003141abcf6
  Args:
    relation: :hasFather
    target: Sir_Desmond_de_Silva
    source: Victoria_de_Silva
  AssignClass (226caa41-53c9-42cb-9576-727f7e85130c)
 Call ID: 226caa41-53c9-42cb-9576-727f7e85130c
  Args:
    source: Patrick_D_Ignazio
    type: :Person
  AssignClass (082ef42a-d6fb-4223-9c88-00cc87cf07fb)
 Call ID: 082ef42a-d6fb-4223-9c88-00cc87cf07fb
  Args:
    source: Patrick_D_Ignazio
    type: :Man
  AssignClass (07711803-bb99-483e-b846-4f6ab95cdbd1)
 Call ID: 07711803-bb99-483e-b846-4f6ab95cdbd1
  Args:
    source: India_Riven_Oxenberg_Daughter
    type: :Person
  AssignClass (728e8060-aa33-4c16-acdd-b5c48d395683)
 Call ID: 728e8060-aa33-4c16-acdd-b5c48d395683
  Args:
    source: India_Riven_Oxenberg_Daughter
    type: :Woman
  AddTriple (1db9e397-0c81-4938-86e6-3eab263f709f)
 Call ID: 1db9e397-0c81-4938-86e6-3eab263f709f
  Args:
    target: India_Riven_Oxenberg
    source: India_Riven_Oxenberg_Daughter
    relation: :hasMother
  AddTriple (40e71879-3818-41e3-8b4f-04b8c3a64a32)
 Call ID: 40e71879-3818-41e3-8b4f-04b8c3a64a32
  Args:
    source: India_Riven_Oxenberg_Daughter
    target: Patrick_D_Ignazio
    relation: :hasFather
  Finish (edff9c93-8cc2-4288-9c44-da9d1b2571ae)
 Call ID: edff9c93-8cc2-4288-9c44-da9d1b2571ae
  Args: