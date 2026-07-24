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
  AssignClass (4978473a-b293-443d-b395-9206ca4289d8)
 Call ID: 4978473a-b293-443d-b395-9206ca4289d8
  Args:
    type: :Woman
    source: India_Riven_Oxenberg
  AssignClass (6acb5bea-ef90-4f3d-89be-ad50401d0a3d)
 Call ID: 6acb5bea-ef90-4f3d-89be-ad50401d0a3d
  Args:
    source: India_Riven_Oxenberg
    type: :Person
  AddLiteral (eba020cf-9aac-4eb7-a59f-89aaaa313c0f)
 Call ID: eba020cf-9aac-4eb7-a59f-89aaaa313c0f
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: India_Riven_Oxenberg
    literal_value: 1991
  AssignClass (bb4f1266-2fff-4481-80a5-04b9ee595f8d)
 Call ID: bb4f1266-2fff-4481-80a5-04b9ee595f8d
  Args:
    source: Catherine_Oxenberg
    type: :Woman
  AssignClass (7b9d170b-5637-430c-a0e9-3f138fe29038)
 Call ID: 7b9d170b-5637-430c-a0e9-3f138fe29038
  Args:
    source: Catherine_Oxenberg
    type: :Person
  AssignClass (a3591a85-06a0-4730-9090-8cf4786fdbb8)
 Call ID: a3591a85-06a0-4730-9090-8cf4786fdbb8
  Args:
    source: William_Weitz_Shaffer
    type: :Man
  AssignClass (b411bd1c-36aa-4bb3-b1ae-765f9cfc291d)
 Call ID: b411bd1c-36aa-4bb3-b1ae-765f9cfc291d
  Args:
    type: :Person
    source: William_Weitz_Shaffer
  AddTriple (6962bb17-93bc-400e-8751-83e43201ec56)
 Call ID: 6962bb17-93bc-400e-8751-83e43201ec56
  Args:
    target: Catherine_Oxenberg
    source: India_Riven_Oxenberg
    relation: :hasMother
  AddTriple (4c799e12-aea7-4f2e-9ed0-34743bc74dad)
 Call ID: 4c799e12-aea7-4f2e-9ed0-34743bc74dad
  Args:
    source: India_Riven_Oxenberg
    target: William_Weitz_Shaffer
    relation: :hasFather
  AssignClass (5aa6a2a4-5b8c-428c-a192-457f14b67777)
 Call ID: 5aa6a2a4-5b8c-428c-a192-457f14b67777
  Args:
    type: :Woman
    source: Princess_Elizabeth_of_Yugoslavia
  AssignClass (efb55f01-7460-4b0a-8854-dffab6f3ee38)
 Call ID: efb55f01-7460-4b0a-8854-dffab6f3ee38
  Args:
    source: Princess_Elizabeth_of_Yugoslavia
    type: :Person
  AssignClass (1cadc0ef-3c53-4e6e-ac43-8f358edd1cf1)
 Call ID: 1cadc0ef-3c53-4e6e-ac43-8f358edd1cf1
  Args:
    source: Howard_Oxenberg
    type: :Man
  AssignClass (a9e3e3c4-c092-4697-9001-f1863bba38e9)
 Call ID: a9e3e3c4-c092-4697-9001-f1863bba38e9
  Args:
    source: Howard_Oxenberg
    type: :Person
  AddTriple (1fbb8fba-da95-4929-9b99-71b4478f271e)
 Call ID: 1fbb8fba-da95-4929-9b99-71b4478f271e
  Args:
    source: Catherine_Oxenberg
    target: Princess_Elizabeth_of_Yugoslavia
    relation: :hasMother
  AddTriple (b0e069d6-1df3-49c7-8f8d-cbd1abd122d9)
 Call ID: b0e069d6-1df3-49c7-8f8d-cbd1abd122d9
  Args:
    relation: :hasFather
    target: Howard_Oxenberg
    source: Catherine_Oxenberg
  AssignClass (f10625dd-c487-42ce-b4a6-3afa45024536)
 Call ID: f10625dd-c487-42ce-b4a6-3afa45024536
  Args:
    source: Prince_Regent_Paul_of_Yugoslavia
    type: :Man
  AssignClass (f60295df-3fac-418d-a486-0bfbcc56840a)
 Call ID: f60295df-3fac-418d-a486-0bfbcc56840a
  Args:
    type: :Person
    source: Prince_Regent_Paul_of_Yugoslavia
  AddTriple (7044f56e-12c5-4b12-a697-64a045ff8972)
 Call ID: 7044f56e-12c5-4b12-a697-64a045ff8972
  Args:
    relation: :hasFather
    source: Princess_Elizabeth_of_Yugoslavia
    target: Prince_Regent_Paul_of_Yugoslavia
  AssignClass (cc17a1a6-e84f-40ff-bc5c-bf58e390aa7f)
 Call ID: cc17a1a6-e84f-40ff-bc5c-bf58e390aa7f
  Args:
    type: :Woman
    source: Christina_Oxenberg
  AssignClass (68b55a04-c340-45b0-bd5e-ba5b7191ea3a)
 Call ID: 68b55a04-c340-45b0-bd5e-ba5b7191ea3a
  Args:
    type: :Person
    source: Christina_Oxenberg
  AddTriple (3410a899-9262-4b0b-97ed-a6052ef62acd)
 Call ID: 3410a899-9262-4b0b-97ed-a6052ef62acd
  Args:
    relation: :isSisterOf
    source: Christina_Oxenberg
    target: Catherine_Oxenberg
  AssignClass (6ebce135-540f-41e6-b0d0-68569af0529c)
 Call ID: 6ebce135-540f-41e6-b0d0-68569af0529c
  Args:
    type: :Woman
    source: Victoria_de_Silva
  AssignClass (791cc17b-f465-4096-94e4-3d1d741137a8)
 Call ID: 791cc17b-f465-4096-94e4-3d1d741137a8
  Args:
    type: :Person
    source: Victoria_de_Silva
  AssignClass (212a9bdf-41a3-4221-932e-203653308083)
 Call ID: 212a9bdf-41a3-4221-932e-203653308083
  Args:
    source: Princess_Katarina
    type: :Woman
  AssignClass (65131073-e4dd-42a7-bd09-38bfd8eb5230)
 Call ID: 65131073-e4dd-42a7-bd09-38bfd8eb5230
  Args:
    type: :Person
    source: Princess_Katarina
  AssignClass (fa9303ac-0b51-4b2e-a1c1-86db6098ea41)
 Call ID: fa9303ac-0b51-4b2e-a1c1-86db6098ea41
  Args:
    source: Sir_Desmond_de_Silva
    type: :Man
  AssignClass (ad91973c-4af3-49b0-b404-6cce11c8229c)
 Call ID: ad91973c-4af3-49b0-b404-6cce11c8229c
  Args:
    source: Sir_Desmond_de_Silva
    type: :Person
  AddTriple (47294860-b089-4b3a-8b2d-bfe794600e16)
 Call ID: 47294860-b089-4b3a-8b2d-bfe794600e16
  Args:
    relation: :hasMother
    source: Victoria_de_Silva
    target: Princess_Katarina
  AddTriple (4a89f81d-98ab-4187-9435-ac2e8d4b0c61)
 Call ID: 4a89f81d-98ab-4187-9435-ac2e8d4b0c61
  Args:
    relation: :hasFather
    source: Victoria_de_Silva
    target: Sir_Desmond_de_Silva
  AssignClass (0d9f4897-087f-4965-af8d-2c0000f6cc2b)
 Call ID: 0d9f4897-087f-4965-af8d-2c0000f6cc2b
  Args:
    type: :Woman
    source: Princess_Olga_of_Greece_and_Denmark
  AssignClass (d011b00d-ba1c-4d80-9353-e7509b4dc5e2)
 Call ID: d011b00d-ba1c-4d80-9353-e7509b4dc5e2
  Args:
    source: Princess_Olga_of_Greece_and_Denmark
    type: :Person
  AssignClass (30586484-4560-4e36-b2d8-fcaaee45e65c)
 Call ID: 30586484-4560-4e36-b2d8-fcaaee45e65c
  Args:
    type: :Man
    source: Casper_Van_Dien
  AssignClass (a7a6d072-de06-4fd5-9033-371590cbc8cb)
 Call ID: a7a6d072-de06-4fd5-9033-371590cbc8cb
  Args:
    type: :Person
    source: Casper_Van_Dien
  Finish (2ded2973-7e08-47c5-a28e-21ff815973cb)
 Call ID: 2ded2973-7e08-47c5-a28e-21ff815973cb
  Args: