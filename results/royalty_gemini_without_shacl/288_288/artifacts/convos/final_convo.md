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
Prince Amedeo, 3rd Duke of Aosta (Amedeo Umberto Isabella Luigi Filippo Maria Giuseppe Giovanni di Savoia-Aosta; 21 October 1898 – 3 March 1942) was the third Duke of Aosta and a first cousin once removed of the King of Italy, Victor Emmanuel III.
Biography

Amedeo was born in Turin, Piedmont, to Prince Emanuele Filiberto, 2nd Duke of Aosta (son of Amadeo I of Spain and Princess Maria Vittoria), and Princess Hélène (daughter of Prince Philippe of Orléans and Princess Marie Isabelle of Orléans).
As his patrilinal great-grandfather was King Victor Emmanuel II of Italy, he was a member of the House of Savoy.
He was known from birth by the courtesy title of Duke of Apulia.
Amedeo was a very tall man (in stark contrast to the King, who was known to be quite short).
According to Amedeo Guillet, he was once referred to by a journalist as "Your Highness" (which in Italian could also be interpreted to mean "your height").
The Duke replied in jest: "198 centimetres ".
Education and early military career

Amedeo was educated at St David's College, Reigate, Surrey, in England.
Amedeo entered the Nunziatella, the military academy in Naples, joined the Italian Royal Army (Regio Esercito) and fought with distinction in the artillery during World War I.
Amedeo subsequently rejoined the Italian armed forces and became a pilot.
Amedeo served under Marshal Rodolfo Graziani and Libyan Governor Pietro Badoglio during the later stages of the so-called "pacification of Libya" (1911 to 1932).
Amedeo and his fellow airmen harried the Senussi forces of Omar Mukhtar from the sky.
When hostilities in Libya came to an end in early 1932, much was made of the participation of the "Duke of Apulia" as the commander of the airmen who forced the Senussi to flee Libya and seek relief in Egypt.
Amedeo, portrayed by the tall actor Sky du Mont, appears in several non-flying scenes with Graziani in the movie The Lion of the Desert, about the Italian conquest of Libya.
On 4 July 1931, upon the death of his father, Amedeo became the Duke of Aosta.
Viceroy and governor-general

In 1937, after the Italian conquest of Ethiopia during the Second Italo-Abyssinian War, the Duke of Aosta replaced Marshal Graziani as Viceroy and as Governor-General of Italian East Africa.
Amedeo was succeeded by his brother, Aimone, 4th Duke of Aosta.
Aftermath

Amedeo was well known and highly regarded for being a gentleman.
Count Galeazzo Ciano, Italian Foreign Minister under his father-in-law, Italian dictator Benito Mussolini, paid Amedeo a high compliment in his famous diaries.
Upon being given the news of the Duke's death, Ciano wrote, "So dies the image of a Prince and an Italian.
"


Emperor Haile Selassie of Ethiopia was also impressed by the respect and care that the Duke of Aosta showed to the exiled Emperor's personal property left behind in Addis Ababa.
In a gesture of thanks, the Emperor during his state visit to Italy in 1953 invited the widowed Duchess of Aosta to tea during his stay in Milan, but was then informed by the Italian government that receiving the Duchess would cause offence to the Italian Republic, and so the Emperor cancelled the visit.
Instead he invited the 5th Duke of Aosta to Ethiopia in the mid-1960s, and accorded him all the protocol due to visiting royalty.
Family

Amedeo was married on 5 November 1927, in Naples, to his first cousin Princess Anne of Orléans (1906–1986), daughter of Prince Jean, Duke of Guise, and Princess Isabelle of Orléans.
They had two daughters:


Cultural depictions

Prince Amedeo's time in Italian Cyrenaica was depicted in the 1981 film Lion of the Desert; Amedeo was played by Sky du Mont.


Amedeo was also briefly mentioned in A Farewell to Arms by Ernest Hemingway.
In the popular mod for the grand strategy game Hearts of Iron IV, Kaiserreich, Amedeo is depicted as King Amadeo I di Savoia-Aosta of Sardinia, an exiled monarchist government of Italy seeking to reclaim the land from the northern Socialist Republic of Italy and southern Kingdom of the Two Sicilies.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (8ee0cfe7-f150-4eec-8aa8-63fa1d84aebd)
 Call ID: 8ee0cfe7-f150-4eec-8aa8-63fa1d84aebd
  Args:
    type: :Man
    source: Amedeo_3rd_Duke_of_Aosta
  AssignClass (6bf8e45d-7767-4dba-8586-2e346ea1d598)
 Call ID: 6bf8e45d-7767-4dba-8586-2e346ea1d598
  Args:
    type: :Person
    source: Amedeo_3rd_Duke_of_Aosta
  AssignClass (77af27bc-28fe-420f-b436-5a77a054a6f2)
 Call ID: 77af27bc-28fe-420f-b436-5a77a054a6f2
  Args:
    type: :Ancestor
    source: Amedeo_3rd_Duke_of_Aosta
  AddLiteral (7098ae46-3548-4a0f-a176-f1500e09567d)
 Call ID: 7098ae46-3548-4a0f-a176-f1500e09567d
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    literal_value: 1898
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (b2dc3977-b09d-430c-af46-4f9674262729)
 Call ID: b2dc3977-b09d-430c-af46-4f9674262729
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1942
  AddLiteral (fdc95b7e-2dda-40e0-90eb-e4b7de738ae0)
 Call ID: fdc95b7e-2dda-40e0-90eb-e4b7de738ae0
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    literal_value: Duke of Apulia
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AssignClass (7a4aab51-cc3f-4480-b3a0-d5fcfe80e14a)
 Call ID: 7a4aab51-cc3f-4480-b3a0-d5fcfe80e14a
  Args:
    type: :Man
    source: Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (ecc5ab24-316f-4db4-81a7-dd1925e06a5a)
 Call ID: ecc5ab24-316f-4db4-81a7-dd1925e06a5a
  Args:
    type: :Ancestor
    source: Emanuele_Filiberto_2nd_Duke_of_Aosta
  AddTriple (f7112f5b-4a98-407f-a7c5-578f746f70d9)
 Call ID: f7112f5b-4a98-407f-a7c5-578f746f70d9
  Args:
    target: Emanuele_Filiberto_2nd_Duke_of_Aosta
    relation: :hasFather
    source: Amedeo_3rd_Duke_of_Aosta
  AssignClass (200532cd-05cc-4575-8b05-5a77811cbe75)
 Call ID: 200532cd-05cc-4575-8b05-5a77811cbe75
  Args:
    type: :Woman
    source: Princess_Helene
  AssignClass (f0e7e101-0c2f-4fcf-a923-5dc1f01717c0)
 Call ID: f0e7e101-0c2f-4fcf-a923-5dc1f01717c0
  Args:
    type: :Ancestor
    source: Princess_Helene
  AddTriple (312bb68b-b63f-432c-8357-70ee6a2a3517)
 Call ID: 312bb68b-b63f-432c-8357-70ee6a2a3517
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    target: Princess_Helene
    relation: :hasMother
  AssignClass (b51195ff-b8b8-4787-9cd8-a18a227afc3b)
 Call ID: b51195ff-b8b8-4787-9cd8-a18a227afc3b
  Args:
    type: :Man
    source: Amadeo_I_of_Spain
  AssignClass (6f34d4db-1893-49c1-9a32-619a60594579)
 Call ID: 6f34d4db-1893-49c1-9a32-619a60594579
  Args:
    type: :Ancestor
    source: Amadeo_I_of_Spain
  AddTriple (adef10f8-9f84-46a9-b546-59e043a22555)
 Call ID: adef10f8-9f84-46a9-b546-59e043a22555
  Args:
    source: Amadeo_I_of_Spain
    relation: :isFatherOf
    target: Emanuele_Filiberto_2nd_Duke_of_Aosta
  AssignClass (72d40a69-4167-42ed-afef-240395196c72)
 Call ID: 72d40a69-4167-42ed-afef-240395196c72
  Args:
    type: :Woman
    source: Princess_Maria_Vittoria
  AssignClass (3423ff7e-7ca0-4a70-84a1-f94128acd953)
 Call ID: 3423ff7e-7ca0-4a70-84a1-f94128acd953
  Args:
    type: :Ancestor
    source: Princess_Maria_Vittoria
  AddTriple (ec357711-e0f3-4d34-a162-caf474689633)
 Call ID: ec357711-e0f3-4d34-a162-caf474689633
  Args:
    source: Princess_Maria_Vittoria
    target: Emanuele_Filiberto_2nd_Duke_of_Aosta
    relation: :isMotherOf
  AssignClass (76ea5334-2673-47c2-a58d-6cea2a57b214)
 Call ID: 76ea5334-2673-47c2-a58d-6cea2a57b214
  Args:
    type: :Man
    source: Prince_Philippe_of_Orleans
  AssignClass (e1e20de2-118b-4eb3-b765-bb6ff20c5357)
 Call ID: e1e20de2-118b-4eb3-b765-bb6ff20c5357
  Args:
    type: :Ancestor
    source: Prince_Philippe_of_Orleans
  AddTriple (762c8064-ef4d-4b4b-be03-789132510afa)
 Call ID: 762c8064-ef4d-4b4b-be03-789132510afa
  Args:
    source: Prince_Philippe_of_Orleans
    target: Princess_Helene
    relation: :isFatherOf
  AssignClass (c2eabd86-bb3b-4284-b301-75d1c621df9f)
 Call ID: c2eabd86-bb3b-4284-b301-75d1c621df9f
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (62bbebae-ea8e-41d4-941e-61661942d3f1)
 Call ID: 62bbebae-ea8e-41d4-941e-61661942d3f1
  Args:
    type: :Ancestor
    source: Princess_Marie_Isabelle_of_Orleans
  AddTriple (0396ad3b-0b60-463d-b837-2709a9720377)
 Call ID: 0396ad3b-0b60-463d-b837-2709a9720377
  Args:
    target: Princess_Helene
    relation: :isMotherOf
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (6f3afc1a-4e38-4a11-aeed-5841a335fe98)
 Call ID: 6f3afc1a-4e38-4a11-aeed-5841a335fe98
  Args:
    type: :Man
    source: Aimone_4th_Duke_of_Aosta
  AssignClass (a33b7846-c8a8-429f-89c9-d2adb7eaa09b)
 Call ID: a33b7846-c8a8-429f-89c9-d2adb7eaa09b
  Args:
    type: :Person
    source: Aimone_4th_Duke_of_Aosta
  AddTriple (3ef5dfaf-8863-4c6e-903a-b37965a1d009)
 Call ID: 3ef5dfaf-8863-4c6e-903a-b37965a1d009
  Args:
    target: Aimone_4th_Duke_of_Aosta
    relation: :hasBrother
    source: Amedeo_3rd_Duke_of_Aosta
  AssignClass (7c72916b-ac49-4f14-9982-9d5f6becb222)
 Call ID: 7c72916b-ac49-4f14-9982-9d5f6becb222
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (448dfe15-462e-4bbb-b0f2-9c25cc1679db)
 Call ID: 448dfe15-462e-4bbb-b0f2-9c25cc1679db
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AddLiteral (58f0cfb8-c64e-4705-9055-a0cb5364d294)
 Call ID: 58f0cfb8-c64e-4705-9055-a0cb5364d294
  Args:
    literal_value: 1927
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Amedeo_3rd_Duke_of_Aosta
  AddTriple (1707b6ad-ca12-4bfc-a98f-bd59da7441e4)
 Call ID: 1707b6ad-ca12-4bfc-a98f-bd59da7441e4
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    relation: :hasRelation
    target: Princess_Anne_of_Orleans
  AssignClass (01205180-213c-41c1-a775-ad937a7aa1db)
 Call ID: 01205180-213c-41c1-a775-ad937a7aa1db
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AssignClass (0634fa59-bc30-4bd1-b8d7-c65822baea2e)
 Call ID: 0634fa59-bc30-4bd1-b8d7-c65822baea2e
  Args:
    type: :Ancestor
    source: Prince_Jean_Duke_of_Guise
  AddTriple (9c1edea5-8dc9-42b9-b65c-5acf39fea662)
 Call ID: 9c1edea5-8dc9-42b9-b65c-5acf39fea662
  Args:
    relation: :isFatherOf
    target: Princess_Anne_of_Orleans
    source: Prince_Jean_Duke_of_Guise
  AssignClass (79c5ae56-396a-4d74-b05e-416575d0cf68)
 Call ID: 79c5ae56-396a-4d74-b05e-416575d0cf68
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orleans
  AssignClass (ce8800c0-284b-4c26-9c46-e70b82097901)
 Call ID: ce8800c0-284b-4c26-9c46-e70b82097901
  Args:
    type: :Ancestor
    source: Princess_Isabelle_of_Orleans
  AddTriple (aa861e77-5a2d-4362-8c61-b6f7db0709ef)
 Call ID: aa861e77-5a2d-4362-8c61-b6f7db0709ef
  Args:
    source: Princess_Isabelle_of_Orleans
    target: Princess_Anne_of_Orleans
    relation: :isMotherOf
  Finish (1c420923-55f2-48a0-a969-78c86bcd5217)
 Call ID: 1c420923-55f2-48a0-a969-78c86bcd5217
  Args: