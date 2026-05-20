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
  AssignClass (496da2c3-59ce-4189-9631-0751bd5dfe19)
 Call ID: 496da2c3-59ce-4189-9631-0751bd5dfe19
  Args:
    type: :Man
    source: Prince_Amedeo
  AssignClass (ab5ca4b0-9bf5-4b06-a597-98e9e018dbf4)
 Call ID: ab5ca4b0-9bf5-4b06-a597-98e9e018dbf4
  Args:
    source: Prince_Amedeo
    type: :Person
  AssignClass (5d855ced-d0bf-491f-9aab-2d3fa9211978)
 Call ID: 5d855ced-d0bf-491f-9aab-2d3fa9211978
  Args:
    source: Emanuele_Filiberto
    type: :Man
  AssignClass (9be762c5-3144-408a-b66f-6e46d6b387cd)
 Call ID: 9be762c5-3144-408a-b66f-6e46d6b387cd
  Args:
    type: :Ancestor
    source: Emanuele_Filiberto
  AssignClass (b10767a1-d383-413e-bf58-5326e6f4bcdf)
 Call ID: b10767a1-d383-413e-bf58-5326e6f4bcdf
  Args:
    source: Emanuele_Filiberto
    type: :Person
  AssignClass (3ad05ae7-906b-4c6a-a3ad-65e63704359c)
 Call ID: 3ad05ae7-906b-4c6a-a3ad-65e63704359c
  Args:
    type: :Woman
    source: Princess_Helene
  AssignClass (dc2b0998-f594-4b4f-9e6d-0766e9dc64f2)
 Call ID: dc2b0998-f594-4b4f-9e6d-0766e9dc64f2
  Args:
    source: Princess_Helene
    type: :Ancestor
  AssignClass (b2106e73-0548-47fe-abea-8e7a0a34f02c)
 Call ID: b2106e73-0548-47fe-abea-8e7a0a34f02c
  Args:
    source: Princess_Helene
    type: :Person
  AssignClass (bfd94e80-7988-452b-8d32-1fcad832a61e)
 Call ID: bfd94e80-7988-452b-8d32-1fcad832a61e
  Args:
    type: :Man
    source: Amadeo_I_of_Spain
  AssignClass (30c349a2-ee7a-45a0-a25e-82b742f78e7a)
 Call ID: 30c349a2-ee7a-45a0-a25e-82b742f78e7a
  Args:
    source: Amadeo_I_of_Spain
    type: :Ancestor
  AssignClass (8b47e4a8-eae1-4d3e-b24c-a0944d4eeaa3)
 Call ID: 8b47e4a8-eae1-4d3e-b24c-a0944d4eeaa3
  Args:
    type: :Person
    source: Amadeo_I_of_Spain
  AssignClass (00448d8b-acd6-46ac-b979-46d4b8ea0aaf)
 Call ID: 00448d8b-acd6-46ac-b979-46d4b8ea0aaf
  Args:
    type: :Woman
    source: Princess_Maria_Vittoria
  AssignClass (cc7f786d-3e1d-428c-a602-70ca5a24c611)
 Call ID: cc7f786d-3e1d-428c-a602-70ca5a24c611
  Args:
    source: Princess_Maria_Vittoria
    type: :Ancestor
  AssignClass (130e339c-fbc0-49fa-9d26-d35473aec642)
 Call ID: 130e339c-fbc0-49fa-9d26-d35473aec642
  Args:
    type: :Person
    source: Princess_Maria_Vittoria
  AssignClass (6379c205-8be2-4052-81b0-0698e772bc09)
 Call ID: 6379c205-8be2-4052-81b0-0698e772bc09
  Args:
    type: :Man
    source: Prince_Philippe_of_Orleans
  AssignClass (10286879-2e47-4635-a169-a6efacc65d12)
 Call ID: 10286879-2e47-4635-a169-a6efacc65d12
  Args:
    type: :Ancestor
    source: Prince_Philippe_of_Orleans
  AssignClass (a7e5f809-6498-4068-a13e-6d161d21a2a0)
 Call ID: a7e5f809-6498-4068-a13e-6d161d21a2a0
  Args:
    source: Prince_Philippe_of_Orleans
    type: :Person
  AssignClass (4e73c5bc-ee05-4d40-bb5d-f8e7697d7762)
 Call ID: 4e73c5bc-ee05-4d40-bb5d-f8e7697d7762
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (ed66dc41-bdc9-4a6e-bd1d-080b3e1c0026)
 Call ID: ed66dc41-bdc9-4a6e-bd1d-080b3e1c0026
  Args:
    source: Princess_Marie_Isabelle_of_Orleans
    type: :Ancestor
  AssignClass (683478a5-db73-425a-b4c2-5f76486ec48b)
 Call ID: 683478a5-db73-425a-b4c2-5f76486ec48b
  Args:
    type: :Person
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (9b09bbef-cd85-4e20-8324-316bbc829c20)
 Call ID: 9b09bbef-cd85-4e20-8324-316bbc829c20
  Args:
    type: :Man
    source: Aimone
  AssignClass (2c2f644e-13e0-403e-b601-5f195bef787b)
 Call ID: 2c2f644e-13e0-403e-b601-5f195bef787b
  Args:
    source: Aimone
    type: :Person
  AssignClass (3371ee1e-9b7a-4f65-bab5-f658f92855f9)
 Call ID: 3371ee1e-9b7a-4f65-bab5-f658f92855f9
  Args:
    type: :Woman
    source: Princess_Anne_of_Orleans
  AssignClass (561a2f77-0d42-40e5-a673-6beeb8a68948)
 Call ID: 561a2f77-0d42-40e5-a673-6beeb8a68948
  Args:
    type: :Person
    source: Princess_Anne_of_Orleans
  AssignClass (60cca7f9-350e-430b-9517-ea711ef54caa)
 Call ID: 60cca7f9-350e-430b-9517-ea711ef54caa
  Args:
    type: :Man
    source: Prince_Jean_Duke_of_Guise
  AssignClass (bea71b6c-73e5-4b5f-9b7a-8890e641947e)
 Call ID: bea71b6c-73e5-4b5f-9b7a-8890e641947e
  Args:
    source: Prince_Jean_Duke_of_Guise
    type: :Ancestor
  AssignClass (6c8edd31-0d88-45d8-80ae-751703eed0f0)
 Call ID: 6c8edd31-0d88-45d8-80ae-751703eed0f0
  Args:
    type: :Person
    source: Prince_Jean_Duke_of_Guise
  AssignClass (fdde233c-dba2-42bd-871a-f34ffd32ded6)
 Call ID: fdde233c-dba2-42bd-871a-f34ffd32ded6
  Args:
    type: :Woman
    source: Princess_Isabelle_of_Orleans
  AssignClass (494d6c16-3ea4-45ad-82b8-52af8f5a6d61)
 Call ID: 494d6c16-3ea4-45ad-82b8-52af8f5a6d61
  Args:
    type: :Ancestor
    source: Princess_Isabelle_of_Orleans
  AssignClass (aadaada7-90fd-47e3-b43b-c1fef0f5b7c4)
 Call ID: aadaada7-90fd-47e3-b43b-c1fef0f5b7c4
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans
  AddLiteral (ea963fcc-cb54-49fb-8a3a-152a8bfed41a)
 Call ID: ea963fcc-cb54-49fb-8a3a-152a8bfed41a
  Args:
    literal_type: xsd:integer
    literal_value: 1898
    relation: :hasBirthYear
    source: Prince_Amedeo
  AddLiteral (f9911c33-3220-4627-b39e-b6087ea36133)
 Call ID: f9911c33-3220-4627-b39e-b6087ea36133
  Args:
    source: Prince_Amedeo
    relation: :hasDeathYear
    literal_value: 1942
    literal_type: xsd:integer
  AddTriple (d65cd56a-3067-4123-8506-0f748bcbd7d7)
 Call ID: d65cd56a-3067-4123-8506-0f748bcbd7d7
  Args:
    source: Prince_Amedeo
    relation: :hasFather
    target: Emanuele_Filiberto
  AddTriple (6a94ac3f-f536-48a9-9f8a-3ed007a43d9d)
 Call ID: 6a94ac3f-f536-48a9-9f8a-3ed007a43d9d
  Args:
    source: Prince_Amedeo
    relation: :hasMother
    target: Princess_Helene
  AddTriple (56c413bf-c575-4a2f-8dd9-1a155551caa4)
 Call ID: 56c413bf-c575-4a2f-8dd9-1a155551caa4
  Args:
    target: Amadeo_I_of_Spain
    source: Emanuele_Filiberto
    relation: :hasFather
  AddTriple (829399a5-6140-4e2c-9ba9-a20ba16788c9)
 Call ID: 829399a5-6140-4e2c-9ba9-a20ba16788c9
  Args:
    target: Princess_Maria_Vittoria
    relation: :hasMother
    source: Emanuele_Filiberto
  AddTriple (066f7a95-5249-4a57-a172-d38727bf556a)
 Call ID: 066f7a95-5249-4a57-a172-d38727bf556a
  Args:
    target: Prince_Philippe_of_Orleans
    source: Princess_Helene
    relation: :hasFather
  AddTriple (799b753b-cc02-4c40-adb8-45ecc7d484b9)
 Call ID: 799b753b-cc02-4c40-adb8-45ecc7d484b9
  Args:
    source: Princess_Helene
    relation: :hasMother
    target: Princess_Marie_Isabelle_of_Orleans
  AddTriple (8cc3e1eb-d462-4d64-b94d-854db89e2d0e)
 Call ID: 8cc3e1eb-d462-4d64-b94d-854db89e2d0e
  Args:
    target: Prince_Amedeo
    source: Aimone
    relation: :isBrotherOf
  AddTriple (96ff657a-cdb5-4bc1-8199-04043f412ad5)
 Call ID: 96ff657a-cdb5-4bc1-8199-04043f412ad5
  Args:
    target: Prince_Jean_Duke_of_Guise
    source: Princess_Anne_of_Orleans
    relation: :hasFather
  AddTriple (21ca0191-cc98-4131-957a-5603032b6bf8)
 Call ID: 21ca0191-cc98-4131-957a-5603032b6bf8
  Args:
    source: Princess_Anne_of_Orleans
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans
  AddLiteral (14e0df39-7bec-4a78-83cc-e19d0da2968c)
 Call ID: 14e0df39-7bec-4a78-83cc-e19d0da2968c
  Args:
    relation: :hasMarriageYear
    source: Prince_Amedeo
    literal_type: xsd:integer
    literal_value: 1927
  AddTriple (494913e7-a904-4e1a-862d-42bba35f6df5)
 Call ID: 494913e7-a904-4e1a-862d-42bba35f6df5
  Args:
    source: Prince_Amedeo
    relation: :hasRelation
    target: Princess_Anne_of_Orleans
  Finish (f58d80ea-72e1-438b-b305-0a95b38543f6)
 Call ID: f58d80ea-72e1-438b-b305-0a95b38543f6
  Args: