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
Prince Adam Karol Czartoryski (.mw-parser-output .IPA-label-small{font-size:85%}.mw-parser-output .references .IPA-label-small,.mw-parser-output .infobox .IPA-label-small,.mw-parser-output .navbox .IPA-label-small{font-size:100%}Polish: ; Spanish: Adán Carlos, IPA:  born 2 January 1940) is a Polish and Spanish aristocrat who is head of the Polish-Lithuanian House of Czartoryski.
In 2016, he sold the family art collection held in the Czartoryski Museum to the Polish state for approximately €100 million.
Origins

Adam Karol Czartoryski is the son of Prince Augustyn Józef Czartoryski (1907–1946) and his wife, Princess María de los Dolores of Bourbon-Two Sicilies.
Through his mother, he is the first cousin of King Juan Carlos I of Spain.
He is the head of the Polish House of Czartoryski, descendants of Gediminas (died 1341), ruler of the Grand Duchy of Lithuania.
The Czartoryski rose to power under August Aleksander Czartoryski (1697–1782) of the Klewa line, who married Countess Zofia von Dönhoff, the only heir to the Sieniawski family.
The Czartoryski and the Potocki were the two most influential aristocratic families of the last decades of the Polish–Lithuanian Commonwealth (1569–1795).
The Gestapo arrested Prince Augustyn and Princess Dolores, who was pregnant with Prince Adam Karol.
Through their connections to Italian and Spanish royalty they arranged to be deported to Spain.
Adam Karol Czartoryski was born on 2 January 1940 in Seville, Spain.
Adam Karol's brother Ludwik Piotr was born in 1945.
Prince Augustyn and Ludwik Piotr both died in 1946 and were buried in the crypt of the Silesian Church in Seville.
Adam Karol Czartoryski was educated in Spain and then in England.
Returning to his native Spain at the end of the sixties, Czartoryski continued his Karate training  under the guidance of Japanese Sensei Yasunari Ishimi.
Czartoryski was director of several international karate organizations.
In 1976 the Chinese government gave sports medals to Adam Czartoryski Bourbon and Fernando Compte, president of the Spanish Wrestling Association.
In 1982 Czartoryski was elected vice-president of the World Karate Federation and the European Karate Federation.
In 1974 Czartoryski became head trustee of the Polish Dzialynska Trust, set up by his family in Norwich, England in 1899 to support Polish students in the United Kingdom and in Poland.
In 1989, after the fall of the Polish People's Republic, Czartoryski was able to visit Poland for the first time.
That year the Polish government restored ownership of the family art collection and library to Czartoryski.
In 1992 Czartoryski represented Poland at  the opening of "Circa 1492:
In 1997 Czartoryski noticed the sale at Sotheby's of a painting by the Dutch artist Jan Mostaert named Portrait of a Lady, Presumably Anne of Bretagne, which he claimed to have come from his family's looted art collection.
Czartoryski's mother, Princess María de los Dolores, died in Madrid in 1996.
In December 2016 he sold the Czartoryski collection to the Polish state at an extremely low price in a transaction that drew some criticism and resulted in legal battles.
Czartoryski collection sale

The Czartoryski collection was started in 1796 by Adam Karol Czartoryski's ancestor, Princess Izabela Czartoryska, a liberal progressive who corresponded with Voltaire, Jean-Jacques Rousseau and Benjamin Franklin.
In 1798 Prince Adam Jerzy Czartoryski, Izabela's son, visited Italy where he bought Leonardo da Vinci's Lady with an Ermine and Raphael's Portrait of a young man.
When the Germans invaded Poland that year, Augustyn Józef Czartoryski had the most valuable items hidden beneath the baroque Sieniawski family castle, while others were stored in the cellar of the museum.
After the war the Polish representative at the Allies Commission for the Retrieval of Works of Art found many of the stolen paintings and claimed them for the Czartoryski Museum.
In London in the late 1960s Adam Karol Czartoryski met Professor Marek Rostworowski , who had been appointed in 1965 as director of the Czartoryski Collection in Poland.
That year the High Court restored the Czartoryski Museum and Library and their contents to Czartoryski, who set up the Princes Czartoryski Foundation to manage the collection.
The Princes Czartoryski Museum in Kraków was closed for extensive renovations in 2010, including adding a glass and steel roof to a courtyard that was not being used.
Czartoryski decided to entrust his collection to the Polish Nation, including the Lady With An Ermine, Landscape with the Good Samaritan and works by Pierre-Auguste Renoir.
By law, the Czartoryski Collection could anyway not leave the country without authorization by the government.
The management board of the Czartoryski Foundation complained that they had not been consulted over the sale, and resigned.
The endowment was challenged by Czartoryski's daughter, Tamara, and in 2018 resulted in a lawsuit between Adam Karol and his daughter.



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
  AssignClass (38311984-2af3-49ee-91e0-c4c7f49a9402)
 Call ID: 38311984-2af3-49ee-91e0-c4c7f49a9402
  Args:
    type: :Man
    source: Adam_Karol_Czartoryski
  AssignClass (846e3c9c-c95f-4bff-bf07-dff82a37b874)
 Call ID: 846e3c9c-c95f-4bff-bf07-dff82a37b874
  Args:
    type: :Person
    source: Adam_Karol_Czartoryski
  AddLiteral (992b9667-2d4f-402e-9a73-fed9cc6267e9)
 Call ID: 992b9667-2d4f-402e-9a73-fed9cc6267e9
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Adam_Karol_Czartoryski
    literal_value: 1940
  AssignClass (58b2ff0d-5367-47ce-99f0-06d907dac7ad)
 Call ID: 58b2ff0d-5367-47ce-99f0-06d907dac7ad
  Args:
    type: :Man
    source: Augustyn_Józef_Czartoryski
  AssignClass (e252ac88-c975-4fbb-9903-e86dad0c1a69)
 Call ID: e252ac88-c975-4fbb-9903-e86dad0c1a69
  Args:
    type: :Person
    source: Augustyn_Józef_Czartoryski
  AssignClass (35239650-d3ac-46cb-ab94-c8d4e4ef3a67)
 Call ID: 35239650-d3ac-46cb-ab94-c8d4e4ef3a67
  Args:
    type: :Ancestor
    source: Augustyn_Józef_Czartoryski
  AddLiteral (4274fd4a-827a-4ccf-9bb9-2d14a96f9d67)
 Call ID: 4274fd4a-827a-4ccf-9bb9-2d14a96f9d67
  Args:
    source: Augustyn_Józef_Czartoryski
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1907
  AddLiteral (3d803f48-1643-42a9-a36b-a7ec177745ba)
 Call ID: 3d803f48-1643-42a9-a36b-a7ec177745ba
  Args:
    literal_value: 1946
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Augustyn_Józef_Czartoryski
  AssignClass (1cacee01-f624-4a87-b97a-db88bfef7853)
 Call ID: 1cacee01-f624-4a87-b97a-db88bfef7853
  Args:
    type: :Woman
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (79259fd8-5e3c-44bb-850a-e90f0502fd62)
 Call ID: 79259fd8-5e3c-44bb-850a-e90f0502fd62
  Args:
    type: :Person
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (241cd214-919e-427f-af6f-e32f3818aeb4)
 Call ID: 241cd214-919e-427f-af6f-e32f3818aeb4
  Args:
    type: :Ancestor
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AddLiteral (9514d06a-c6d7-4a73-9ce1-6dac1b148b67)
 Call ID: 9514d06a-c6d7-4a73-9ce1-6dac1b148b67
  Args:
    literal_value: 1996
    source: María_de_los_Dolores_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (185211a7-a193-4941-86ab-6a868bbab599)
 Call ID: 185211a7-a193-4941-86ab-6a868bbab599
  Args:
    target: Augustyn_Józef_Czartoryski
    source: Adam_Karol_Czartoryski
    relation: :hasFather
  AddTriple (824a3c93-32f9-42f0-bb75-6f478bd51a1e)
 Call ID: 824a3c93-32f9-42f0-bb75-6f478bd51a1e
  Args:
    relation: :hasMother
    source: Adam_Karol_Czartoryski
    target: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (fe34f846-81f1-4b48-b9c2-9a8f4e939acb)
 Call ID: fe34f846-81f1-4b48-b9c2-9a8f4e939acb
  Args:
    type: :Man
    source: Ludwik_Piotr_Czartoryski
  AssignClass (ab0afa64-39a0-48dc-9cc3-5316eeac7985)
 Call ID: ab0afa64-39a0-48dc-9cc3-5316eeac7985
  Args:
    type: :Person
    source: Ludwik_Piotr_Czartoryski
  AddLiteral (9b227010-d23f-4a0d-acd3-e4c1bc91cb09)
 Call ID: 9b227010-d23f-4a0d-acd3-e4c1bc91cb09
  Args:
    literal_type: xsd:integer
    source: Ludwik_Piotr_Czartoryski
    relation: :hasBirthYear
    literal_value: 1945
  AddLiteral (dccaad09-be04-4ba0-be5b-657910c5e639)
 Call ID: dccaad09-be04-4ba0-be5b-657910c5e639
  Args:
    literal_value: 1946
    source: Ludwik_Piotr_Czartoryski
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (5091c091-ae75-4f28-b915-8814f1462835)
 Call ID: 5091c091-ae75-4f28-b915-8814f1462835
  Args:
    relation: :hasBrother
    source: Adam_Karol_Czartoryski
    target: Ludwik_Piotr_Czartoryski
  AddTriple (ddb30300-41f0-41b8-ac40-f3709d2ecbb0)
 Call ID: ddb30300-41f0-41b8-ac40-f3709d2ecbb0
  Args:
    target: Augustyn_Józef_Czartoryski
    source: Ludwik_Piotr_Czartoryski
    relation: :hasFather
  AddTriple (dfd3ddb7-4a60-445c-a8b4-d336970e0dd0)
 Call ID: dfd3ddb7-4a60-445c-a8b4-d336970e0dd0
  Args:
    relation: :hasMother
    source: Ludwik_Piotr_Czartoryski
    target: María_de_los_Dolores_of_Bourbon-Two_Sicilies
  AssignClass (e00e2a8f-6463-488d-9225-d52566923625)
 Call ID: e00e2a8f-6463-488d-9225-d52566923625
  Args:
    type: :Woman
    source: Tamara_Czartoryska
  AssignClass (2db781c4-f2db-4f2a-910d-e460ca05752b)
 Call ID: 2db781c4-f2db-4f2a-910d-e460ca05752b
  Args:
    type: :Person
    source: Tamara_Czartoryska
  AddTriple (ff13eaeb-1b90-4b6b-9422-c0eeec8c5bbc)
 Call ID: ff13eaeb-1b90-4b6b-9422-c0eeec8c5bbc
  Args:
    target: Adam_Karol_Czartoryski
    relation: :isDaughterOf
    source: Tamara_Czartoryska
  AssignClass (d75d4082-e3ec-4206-9f28-3e90bae0530a)
 Call ID: d75d4082-e3ec-4206-9f28-3e90bae0530a
  Args:
    type: :Woman
    source: Izabela_Czartoryska
  AssignClass (3a3b6d0a-fadc-40ea-bc16-7901486ba266)
 Call ID: 3a3b6d0a-fadc-40ea-bc16-7901486ba266
  Args:
    type: :Person
    source: Izabela_Czartoryska
  AssignClass (d33b2ae6-52b8-4b4d-9311-47589f619029)
 Call ID: d33b2ae6-52b8-4b4d-9311-47589f619029
  Args:
    type: :Ancestor
    source: Izabela_Czartoryska
  AddTriple (c56cfc82-9fd9-4b39-ba7e-1cf2c7d9d0a6)
 Call ID: c56cfc82-9fd9-4b39-ba7e-1cf2c7d9d0a6
  Args:
    relation: :isAncestorOf
    source: Izabela_Czartoryska
    target: Adam_Karol_Czartoryski
  AssignClass (5e8f88b3-cf26-4942-9727-07a129abf455)
 Call ID: 5e8f88b3-cf26-4942-9727-07a129abf455
  Args:
    type: :Man
    source: Adam_Jerzy_Czartoryski
  AssignClass (7f484837-dd8e-4bae-9ac0-9ed416f5c75b)
 Call ID: 7f484837-dd8e-4bae-9ac0-9ed416f5c75b
  Args:
    type: :Person
    source: Adam_Jerzy_Czartoryski
  AssignClass (8aeee9f1-341e-4597-8d1a-aee29fdf66db)
 Call ID: 8aeee9f1-341e-4597-8d1a-aee29fdf66db
  Args:
    type: :Ancestor
    source: Adam_Jerzy_Czartoryski
  AddTriple (45571c11-efa7-4616-ac69-c9e89410e3c2)
 Call ID: 45571c11-efa7-4616-ac69-c9e89410e3c2
  Args:
    relation: :isSonOf
    source: Adam_Jerzy_Czartoryski
    target: Izabela_Czartoryska
  AssignClass (8b0b41a4-5164-4d92-828b-e41ca1a21fa0)
 Call ID: 8b0b41a4-5164-4d92-828b-e41ca1a21fa0
  Args:
    type: :Man
    source: August_Aleksander_Czartoryski
  AssignClass (f89590bd-6155-4984-b0d8-66b0acbce041)
 Call ID: f89590bd-6155-4984-b0d8-66b0acbce041
  Args:
    type: :Person
    source: August_Aleksander_Czartoryski
  AssignClass (84a28563-ea85-4f78-b1cb-babee03405fc)
 Call ID: 84a28563-ea85-4f78-b1cb-babee03405fc
  Args:
    type: :Ancestor
    source: August_Aleksander_Czartoryski
  AddLiteral (0f682379-6911-4c14-84af-cbde730497f2)
 Call ID: 0f682379-6911-4c14-84af-cbde730497f2
  Args:
    literal_value: 1697
    relation: :hasBirthYear
    source: August_Aleksander_Czartoryski
    literal_type: xsd:integer
  AddLiteral (bd5be0dc-e0ba-4bdc-8b25-4565f16710fb)
 Call ID: bd5be0dc-e0ba-4bdc-8b25-4565f16710fb
  Args:
    literal_value: 1782
    relation: :hasDeathYear
    source: August_Aleksander_Czartoryski
    literal_type: xsd:integer
  AssignClass (ef2a2e2f-a3f1-468f-bcb6-81f96efd5c72)
 Call ID: ef2a2e2f-a3f1-468f-bcb6-81f96efd5c72
  Args:
    type: :Woman
    source: Zofia_von_Dönhoff
  AssignClass (05d2200a-8012-4c2a-b771-86ec99e908f1)
 Call ID: 05d2200a-8012-4c2a-b771-86ec99e908f1
  Args:
    type: :Person
    source: Zofia_von_Dönhoff
  AddTriple (792e8551-1f8d-4520-9fb4-2b92dcf44915)
 Call ID: 792e8551-1f8d-4520-9fb4-2b92dcf44915
  Args:
    source: August_Aleksander_Czartoryski
    relation: :hasRelation
    target: Zofia_von_Dönhoff
  Finish (38c597b7-b690-43e9-8d93-4aafce7de828)
 Call ID: 38c597b7-b690-43e9-8d93-4aafce7de828
  Args: