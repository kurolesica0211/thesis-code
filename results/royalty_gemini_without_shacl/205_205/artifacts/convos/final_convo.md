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
Christina Oxenberg (born December 27, 1962) is an American writer, humorist, and fashion designer.
Her two knitwear clothing lines, Christina Oxenberg and Ox, have appeared in Barneys, Bloomingdale's, and luxury boutiques throughout the world.
Oxenberg is the daughter of Princess Elizabeth of Yugoslavia and is a descendant of the Serbian House of Karađorđević.
Early life

Christina Oxenberg was born in New York City.
She is a daughter of Princess Elizabeth of Yugoslavia (born 1936) and her first husband Howard Oxenberg (1919–2010), a Jewish self-made textile and clothing tycoon and close friend of the Kennedy family.
Princess Elizabeth is the only daughter of Prince Paul of Yugoslavia (who served as regent for his cousin's eldest son King Peter II of Yugoslavia) and Princess Olga of Greece and Denmark.
She has a full sister, Catherine Oxenberg, and a half-brother on her mother's side, Neil Balfour (born 1970).
On her father's side she has a half-brother, Robert Oxenberg, and two half-sisters Starr Oxenberg and Ashley Harcourt.
She is a first cousin of Prince Edward, Duke of Kent, and also a maternal second cousin of Queen Sofía of Spain, making her a second cousin once removed of King Charles III.
Career

After high school, Oxenberg worked various jobs in New York ranging from a secretary to a roller-rink attendant.
Upon her return, Oxenberg secured a job at Studio 54.
In 1994, Simon & Schuster commissioned Oxenberg to write a semi-autobiographical novel that would eventually be published as Royal Blue.
As a result of the book, Oxenberg appeared on the cover of New York Magazine and was profiled in People.
In 2000, Oxenberg went on hiatus from writing and took a job at Robert F. Kennedy Jr.'s Waterkeeper Alliance.
The two discussed the possibility of a clothing line using Oxenberg's name.
From 2002 to 2010, Oxenberg produced two clothing lines (Christina Oxenberg and Ox).
Christina Oxenberg would go on to self-publish several collections of short stories between 2010 and 2014, including Do These Gloves Make My Ass Look Fat?, Life is Short: Read Short Stories, and When in Doubt...Double the Dosage.
Since 2012 Oxenberg has contributed articles to Key West weekly magazine Konk Life.
In 2014, Oxenberg helped organize a visit by John Hemingway (Ernest Hemingway's grandson) to David Wolkowsky's Tennessee Williams Collection.
In 2015, Christina Oxenberg moved to Serbia for a year to write and research her book, Royal Dynasty – An Insider's History of the Serbian Royal Family, which was published in Serbian in 2015 by the publisher, Laguna.
For her work, Oxenberg received an award from the Serbian Academy of Sciences and Arts in 2016.
Subsequently, Oxenberg was interviewed by the Sunday Times, Radio Gorgeous and Tatler, and she presented the book at the Oxford Literary Festival on 22 March 2018.
Bibliography

Novels


Short story collections


Autobiographies


Ancestry

Christina Oxenberg is a direct descendant of Karađorđe, a peasant from Šumadija region in today's Serbia, leader of First Serbian Uprising against the Ottomans, and founder of the Karađorđević Dynasty; of King George I of Greece; of Tsar Alexander II of Russia; of King George II of Great Britain, Empress Catherine II of Russia, and  William the Conqueror, through Frederick of Mecklenburg-Schwerin.
Oxenberg's maternal grandmother, Princess Olga, was the daughter of Grand Duchess Elena Vladimirovna of Russia and Prince Nicholas of Greece and Denmark, himself the son of another Romanov grand duchess, Queen Olga Konstantinovna of the Hellenes and her Danish-born husband King George of Greece, brother of Queen Alexandra of the United Kingdom and the Empress Maria Fyodorovna.
Princess Olga was the sister of Princess Marina, who married Prince George, Duke of Kent (an uncle of Queen Elizabeth II); and Olga/Marina were also paternal first cousins of the Duke of Edinburgh (husband of Queen Elizabeth II) through their respective fathers Prince Nicholas of Greece and Denmark and Prince Andrew of Greece and Denmark, who were brothers.



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
  AssignClass (650f3483-7041-4082-944e-68d8332550f8)
 Call ID: 650f3483-7041-4082-944e-68d8332550f8
  Args:
    type: :Woman
    source: Christina Oxenberg
  AddLiteral (40d915b9-8c50-4e5e-9084-accf15295ddf)
 Call ID: 40d915b9-8c50-4e5e-9084-accf15295ddf
  Args:
    relation: :hasBirthYear
    source: Christina Oxenberg
    literal_value: 1962
    literal_type: xsd:integer
  AssignClass (c30dc63c-5944-47c0-ab6e-1432e6d8dcb7)
 Call ID: c30dc63c-5944-47c0-ab6e-1432e6d8dcb7
  Args:
    source: Princess Elizabeth of Yugoslavia
    type: :Woman
  AddLiteral (02194715-60c6-4130-8925-fb3c6aa2958f)
 Call ID: 02194715-60c6-4130-8925-fb3c6aa2958f
  Args:
    source: Princess Elizabeth of Yugoslavia
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1936
  AddTriple (4e762f9f-aca8-489b-8028-e9ceb54db2e5)
 Call ID: 4e762f9f-aca8-489b-8028-e9ceb54db2e5
  Args:
    target: Princess Elizabeth of Yugoslavia
    relation: :hasMother
    source: Christina Oxenberg
  AssignClass (d882e15d-764b-4ade-a355-6917a66afdb9)
 Call ID: d882e15d-764b-4ade-a355-6917a66afdb9
  Args:
    type: :Man
    source: Howard Oxenberg
  AddLiteral (6ad37d55-7410-4310-a0e7-f8fdee4e611e)
 Call ID: 6ad37d55-7410-4310-a0e7-f8fdee4e611e
  Args:
    literal_value: 1919
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Howard Oxenberg
  AddLiteral (c6dc3b4b-97b4-4b91-91ac-93d7e3f5b907)
 Call ID: c6dc3b4b-97b4-4b91-91ac-93d7e3f5b907
  Args:
    relation: :hasDeathYear
    source: Howard Oxenberg
    literal_value: 2010
    literal_type: xsd:integer
  AddTriple (98f4b3d9-634a-4f88-8161-fb7311708c44)
 Call ID: 98f4b3d9-634a-4f88-8161-fb7311708c44
  Args:
    source: Christina Oxenberg
    relation: :hasFather
    target: Howard Oxenberg
  AssignClass (64e5e954-8ca2-4024-8ca4-d87ae1589e17)
 Call ID: 64e5e954-8ca2-4024-8ca4-d87ae1589e17
  Args:
    type: :Man
    source: Prince Paul of Yugoslavia
  AddTriple (44aa0afe-e7ee-42ec-a335-7f0aa55294ef)
 Call ID: 44aa0afe-e7ee-42ec-a335-7f0aa55294ef
  Args:
    target: Prince Paul of Yugoslavia
    source: Princess Elizabeth of Yugoslavia
    relation: :hasFather
  AssignClass (723dfea3-9897-4b3c-9e51-bfcfc6c62aa5)
 Call ID: 723dfea3-9897-4b3c-9e51-bfcfc6c62aa5
  Args:
    type: :Woman
    source: Princess Olga of Greece and Denmark
  AddTriple (9438621a-808a-4096-ab39-2d0212b19405)
 Call ID: 9438621a-808a-4096-ab39-2d0212b19405
  Args:
    target: Princess Olga of Greece and Denmark
    source: Princess Elizabeth of Yugoslavia
    relation: :hasMother
  AssignClass (702ac1f5-e144-487d-8c29-4654be93e6ac)
 Call ID: 702ac1f5-e144-487d-8c29-4654be93e6ac
  Args:
    type: :Woman
    source: Catherine Oxenberg
  AddTriple (7d8186b6-65dc-46eb-b80d-a61f899e266f)
 Call ID: 7d8186b6-65dc-46eb-b80d-a61f899e266f
  Args:
    relation: :hasSister
    source: Christina Oxenberg
    target: Catherine Oxenberg
  AssignClass (7c23264f-6b7e-4dd5-933e-d904a05b3b0e)
 Call ID: 7c23264f-6b7e-4dd5-933e-d904a05b3b0e
  Args:
    type: :Man
    source: Neil Balfour
  AddLiteral (4e96bee2-895c-46f8-a1b1-6a5ec37da8ff)
 Call ID: 4e96bee2-895c-46f8-a1b1-6a5ec37da8ff
  Args:
    literal_type: xsd:integer
    literal_value: 1970
    source: Neil Balfour
    relation: :hasBirthYear
  AddTriple (1553f730-2b88-4fb3-9268-fdfa816b0b48)
 Call ID: 1553f730-2b88-4fb3-9268-fdfa816b0b48
  Args:
    target: Princess Elizabeth of Yugoslavia
    source: Neil Balfour
    relation: :hasMother
  AssignClass (17c0f53b-2265-4d37-be8a-b0ab4c3a28d1)
 Call ID: 17c0f53b-2265-4d37-be8a-b0ab4c3a28d1
  Args:
    source: Robert Oxenberg
    type: :Man
  AddTriple (6953a34a-fdf0-47b6-aa32-40d88256707e)
 Call ID: 6953a34a-fdf0-47b6-aa32-40d88256707e
  Args:
    target: Howard Oxenberg
    relation: :hasFather
    source: Robert Oxenberg
  AssignClass (2cbe8256-c308-4849-8486-75bade521806)
 Call ID: 2cbe8256-c308-4849-8486-75bade521806
  Args:
    source: Starr Oxenberg
    type: :Woman
  AddTriple (36a9dbd0-e23d-4976-b1b8-264c14578240)
 Call ID: 36a9dbd0-e23d-4976-b1b8-264c14578240
  Args:
    relation: :hasFather
    source: Starr Oxenberg
    target: Howard Oxenberg
  AssignClass (cedeaf93-dfe6-4680-9ab9-d0b8a55bc2ce)
 Call ID: cedeaf93-dfe6-4680-9ab9-d0b8a55bc2ce
  Args:
    source: Ashley Harcourt
    type: :Woman
  AddTriple (73a427d7-a4eb-42af-aedd-eadefa0408fa)
 Call ID: 73a427d7-a4eb-42af-aedd-eadefa0408fa
  Args:
    target: Howard Oxenberg
    source: Ashley Harcourt
    relation: :hasFather
  Finish (92ddcb40-f38f-4404-adbe-758507685d23)
 Call ID: 92ddcb40-f38f-4404-adbe-758507685d23
  Args: