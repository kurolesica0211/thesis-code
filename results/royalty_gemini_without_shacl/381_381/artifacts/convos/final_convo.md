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
Princess Tatiana Maria Renata Eugenia Elisabeth Margarete Radziwiłł (28 August 1939 – 19 December 2025) was a French-Polish aristocrat, bacteriologist and nurse.
The eldest daughter of Prince Dominik Rainer Radziwiłł and Princess Eugénie of Greece and Denmark, she was a member of the House of Radziwiłł and a close relative to the Greek, Romanian, Spanish,  Danish, British, and Serbian royal families and the former imperial families of Austria, France, and Russia.
Radziwiłł served as a bridesmaid at the Wedding of Prince Juan Carlos of Spain and Princess Sophia of Greece and Denmark in 1962 and at the wedding of Constantine II of Greece and Princess Anne-Marie of Denmark in 1964.
Early life and family

Radziwiłł was born in Rouen, Normandy on 28 August 1939 to Prince Dominik Rainer Radziwiłł, an officer in the Polish Army, and Princess Eugénie of Greece and Denmark, a member of the Greek royal family.
By birth, she was a member of the House of Radziwill, one of the wealthiest and most important Polish-Lithuanian magnate families, and was the granddaughter of Prince Hieronim Mikołaj Radziwiłł and Archduchess Renata of Austria.
Her maternal grandparents were Prince George of Greece and Denmark, second son of George I of Greece and Olga Constantinovna of Russia, and Princess Marie Bonaparte, daughter of Roland Napoléon Bonaparte, 6th Prince of Canino and Musignano and Marie-Félix Blanc.
Radziwiłł's parents divorced in 1946.
Her father remarried in 1947 to Lida Lacey Bloodgood, daughter of Lida Fleitmann Bloodgood, and her mother remarried in 1949 to Prince Raimondo della Torre e Tasso, Duke of Castel Duino.
Radziwiłł and her parents fled their home in 1940 after the Fall of France, taking refuge in Saint-Tropez before going in to exile in South Africa, then part of the British Empire.
They were later joined by her grandparents, Prince George of Greece and Denmark and Princess Marie Bonaparte, as well as other members of the Greek royal family, including Crown Princess Frederika and her children.
Throughout her childhood, Radziwiłł became close friend with her second cousin, Princess Sophia of Greece and Denmark (the future Queen of Spain).
She also spent a lot of her childhood with her maternal grandmother, Princess Marie, who was a psychoanalyst and authored Le Livre de Tatiana shortly after Tatiana's birth.
Radziwiłł returned to France in 1945 following the end of the war, just three years after the birth of her brother, Prince George.
She was educated in schools in France and in Greece, studying music and languages.
She took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Public life and royal duties

As a relative of many reigning royal families in Europe, Radziwiłł attended various events across the continent including the Coronation of Elizabeth II in 1953 and the Royal Cruise Agamemnon in 1954.
As a young woman, Radziwiłł was considered as a potential wife for the future Harald V of Norway.
In 1956, she was part of the official entourage at a reception for King Paul of Greece in Bois de Boulogne and at the Hôtel de Ville, Paris.
She remained close to the Greek royal family, serving as a bridesmaid for her cousin, Princess Sophia, when she married the future King of Spain in 1962.
Radziwiłł  served alongside Princess Irene of Greece and Denmark, Princess Irene of the Netherlands, Princess Alexandra of Kent, Princess Anne d'Orléans, Infanta Pilar of Spain, Princess Anne-Marie of Denmark, and Princess Benedikte of Denmark.
In March 1963, Tatiana Radziwiłł attended the festivities celebrating the 100th Anniversary of the Greek Monarchy.
She was present at the doxology service, a parade, and a gala performance at the National Theatre of Greece.
In August 1963, she accompanied the Crown Prince of Greece while he hosted the 11th World Scout Jamboree.
In 1964, she served as a bridesmaid in the wedding of her cousins, Constantine II of Greece and Princess Anne-Marie of Denmark.
In 2021, she attended the wedding of Prince Philippos of Greece and Denmark and Nina Flohr.
In 2024, she attended the wedding of Princess Theodora of Greece and Denmark and Matthew Kumar.
Personal life and death

While studying nursing and bacteriology at the University of Paris, Radziwiłł met a French cardiologist, Dr. Jean Henri Fruchard, the son of Colonel Dr. Henri Fruchard and his second wife, Eunice McCooey.
Their wedding was attended by members of the Greek and Danish royal families, including King Constantine II of Greece, Queen Anne-Marie of Greece, Dowager Queen Frederica of Greece, Queen Ingrid of Denmark, Princess Alice of Greece, Princess Irene of Greece, and Princess Sophia of Greece.
Radziwiłł and Fruchaud had two children, Fabiola (born 1967) and Alexis (born 1969).
A close friend and second cousin of Queen Sofía of Spain, Radziwiłł accompanied the Queen on international trips and attended events at Zarzuela Palace and Marivent Palace.
Radziwiłł died on 19 December 2025 in Paris, at the age of 86.
Her funeral took place on 10 January 2026 at Saint-Thomas-d'Aquin, Paris and was attended by members of the Spanish and Greek royal families and their relatives, including King Felipe VI and Queen Sofia of Spain as well as Queen Anne-Marie and Crown Prince Pavlos of Greece.
Popular culture

Radziwiłł is portrayed by Paloma Bloyd in Antonio Hernández's 2011 Spanish television film directed Sofía.
She was also portrayed in Benoît Jacquot's 2004 television film Princesse Marie.
In his 2013 book, La récréation, Frédéric Mitterrand writes about attending an exhibition on Princess Marie Bonaparte with Radziwiłł.



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
  AssignClass (d403ca9d-a8d0-4add-8ca4-20ab5d11234e)
 Call ID: d403ca9d-a8d0-4add-8ca4-20ab5d11234e
  Args:
    source: Tatiana_Radziwiłł
    type: :Woman
  AssignClass (55e74536-e94d-4ef7-9558-b91968f3ca78)
 Call ID: 55e74536-e94d-4ef7-9558-b91968f3ca78
  Args:
    source: Tatiana_Radziwiłł
    type: :Person
  AddLiteral (e672fe2c-694f-4563-b1ca-05cbf6cc9af4)
 Call ID: e672fe2c-694f-4563-b1ca-05cbf6cc9af4
  Args:
    source: Tatiana_Radziwiłł
    literal_value: Tatiana Maria Renata Eugenia Elisabeth Margarete Radziwiłł
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (89612feb-6fbf-4ba5-aa28-458f66549a3c)
 Call ID: 89612feb-6fbf-4ba5-aa28-458f66549a3c
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Tatiana_Radziwiłł
    literal_value: 1939
  AddLiteral (5ca132f2-d1ee-419e-ab76-5b6a66191661)
 Call ID: 5ca132f2-d1ee-419e-ab76-5b6a66191661
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Tatiana_Radziwiłł
    literal_value: 2025
  AssignClass (185b9426-76b6-4bee-b8d4-00dc10d7391a)
 Call ID: 185b9426-76b6-4bee-b8d4-00dc10d7391a
  Args:
    type: :Man
    source: Dominik_Rainer_Radziwiłł
  AssignClass (df145b54-7442-4b75-9e97-2f9116d0e066)
 Call ID: df145b54-7442-4b75-9e97-2f9116d0e066
  Args:
    source: Dominik_Rainer_Radziwiłł
    type: :Ancestor
  AssignClass (ef0aee79-32c9-4fe9-96fd-dec3c3b9978b)
 Call ID: ef0aee79-32c9-4fe9-96fd-dec3c3b9978b
  Args:
    source: Eugénie_of_Greece_and_Denmark
    type: :Woman
  AssignClass (d433357a-1f1f-4c92-8666-70fa3d265657)
 Call ID: d433357a-1f1f-4c92-8666-70fa3d265657
  Args:
    source: Eugénie_of_Greece_and_Denmark
    type: :Ancestor
  AddTriple (23c0873c-8d84-43ff-b5da-e6ff3ee11bb4)
 Call ID: 23c0873c-8d84-43ff-b5da-e6ff3ee11bb4
  Args:
    source: Tatiana_Radziwiłł
    relation: :hasFather
    target: Dominik_Rainer_Radziwiłł
  AddTriple (9585afc9-6130-42f3-afaa-042fb5de60db)
 Call ID: 9585afc9-6130-42f3-afaa-042fb5de60db
  Args:
    source: Tatiana_Radziwiłł
    target: Eugénie_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (3aa137e6-ed23-4794-b7f8-072a85da0897)
 Call ID: 3aa137e6-ed23-4794-b7f8-072a85da0897
  Args:
    source: George_Radziwiłł
    type: :Man
  AddTriple (8284e119-f7f2-410b-a8ad-82ee99f0dd63)
 Call ID: 8284e119-f7f2-410b-a8ad-82ee99f0dd63
  Args:
    source: Tatiana_Radziwiłł
    target: George_Radziwiłł
    relation: :hasBrother
  AssignClass (a502e4ca-9b61-49f3-8d13-1cb881b9df60)
 Call ID: a502e4ca-9b61-49f3-8d13-1cb881b9df60
  Args:
    type: :Man
    source: Hieronim_Mikołaj_Radziwiłł
  AssignClass (c08ce5e8-d068-454d-bf7d-8ed74a24a88f)
 Call ID: c08ce5e8-d068-454d-bf7d-8ed74a24a88f
  Args:
    type: :Woman
    source: Renata_of_Austria
  AddTriple (0455975d-2d25-4633-9981-1fa482e6e9d7)
 Call ID: 0455975d-2d25-4633-9981-1fa482e6e9d7
  Args:
    relation: :hasFather
    target: Hieronim_Mikołaj_Radziwiłł
    source: Dominik_Rainer_Radziwiłł
  AddTriple (c471496c-302a-4ab6-9956-508b3fced769)
 Call ID: c471496c-302a-4ab6-9956-508b3fced769
  Args:
    target: Renata_of_Austria
    relation: :hasMother
    source: Dominik_Rainer_Radziwiłł
  AssignClass (5a32d8ec-45db-455c-a782-94ab93671244)
 Call ID: 5a32d8ec-45db-455c-a782-94ab93671244
  Args:
    source: George_of_Greece_and_Denmark
    type: :Man
  AssignClass (9b40424e-bd75-440b-b980-4549e14df5c0)
 Call ID: 9b40424e-bd75-440b-b980-4549e14df5c0
  Args:
    source: Marie_Bonaparte
    type: :Woman
  AddTriple (cda32aa5-89bc-4f2c-813d-983b1d253e3f)
 Call ID: cda32aa5-89bc-4f2c-813d-983b1d253e3f
  Args:
    source: Eugénie_of_Greece_and_Denmark
    target: George_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (f3e73055-bb57-4120-b552-14acf27c98e2)
 Call ID: f3e73055-bb57-4120-b552-14acf27c98e2
  Args:
    source: Eugénie_of_Greece_and_Denmark
    relation: :hasMother
    target: Marie_Bonaparte
  AssignClass (ed491337-08d6-4730-ba3d-81bd85bd0426)
 Call ID: ed491337-08d6-4730-ba3d-81bd85bd0426
  Args:
    type: :Man
    source: George_I_of_Greece
  AssignClass (c3fdbfb6-817d-4624-8b03-9ff5deb2c188)
 Call ID: c3fdbfb6-817d-4624-8b03-9ff5deb2c188
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AddTriple (ec687e81-0fd7-4d8a-a44e-96b07afb5118)
 Call ID: ec687e81-0fd7-4d8a-a44e-96b07afb5118
  Args:
    relation: :hasFather
    target: George_I_of_Greece
    source: George_of_Greece_and_Denmark
  AddTriple (390ecca0-80c1-49c9-bdf5-a270f7a6fa0b)
 Call ID: 390ecca0-80c1-49c9-bdf5-a270f7a6fa0b
  Args:
    source: George_of_Greece_and_Denmark
    relation: :hasMother
    target: Olga_Constantinovna_of_Russia
  AssignClass (c8961447-8fb5-425d-9897-5283ac6ab5ff)
 Call ID: c8961447-8fb5-425d-9897-5283ac6ab5ff
  Args:
    type: :Man
    source: Roland_Napoléon_Bonaparte
  AssignClass (69fd1087-cd4c-44cc-8e12-b543c94ba4dc)
 Call ID: 69fd1087-cd4c-44cc-8e12-b543c94ba4dc
  Args:
    type: :Woman
    source: Marie-Félix_Blanc
  AddTriple (c920f0c4-c5d2-4cfb-9dc8-a0c49759c577)
 Call ID: c920f0c4-c5d2-4cfb-9dc8-a0c49759c577
  Args:
    source: Marie_Bonaparte
    relation: :hasFather
    target: Roland_Napoléon_Bonaparte
  AddTriple (4f1dbe7f-742e-407e-838f-c2c210df1630)
 Call ID: 4f1dbe7f-742e-407e-838f-c2c210df1630
  Args:
    relation: :hasMother
    target: Marie-Félix_Blanc
    source: Marie_Bonaparte
  AssignClass (936051ca-c1b1-4273-bf5e-f59dd6126784)
 Call ID: 936051ca-c1b1-4273-bf5e-f59dd6126784
  Args:
    source: Jean_Henri_Fruchaud
    type: :Man
  AddTriple (ea5a2a28-7679-417e-82be-1f095a60f7cf)
 Call ID: ea5a2a28-7679-417e-82be-1f095a60f7cf
  Args:
    relation: :hasRelation
    target: Jean_Henri_Fruchaud
    source: Tatiana_Radziwiłł
  AssignClass (0aef79de-963e-4280-9213-f9f816c29322)
 Call ID: 0aef79de-963e-4280-9213-f9f816c29322
  Args:
    type: :Woman
    source: Fabiola_Fruchaud
  AssignClass (5a2e90b2-8faa-4427-9bcd-37b667adc4ed)
 Call ID: 5a2e90b2-8faa-4427-9bcd-37b667adc4ed
  Args:
    source: Alexis_Fruchaud
    type: :Man
  AddTriple (3b09828d-b830-4bc8-bd53-34248c2be997)
 Call ID: 3b09828d-b830-4bc8-bd53-34248c2be997
  Args:
    source: Tatiana_Radziwiłł
    relation: :hasDaughter
    target: Fabiola_Fruchaud
  AddTriple (d4b89e6f-f624-4dc5-95a3-3b48f722830f)
 Call ID: d4b89e6f-f624-4dc5-95a3-3b48f722830f
  Args:
    relation: :hasSon
    target: Alexis_Fruchaud
    source: Tatiana_Radziwiłł
  AddTriple (0da1aa77-c09e-46c7-8e7d-24ceb50b0122)
 Call ID: 0da1aa77-c09e-46c7-8e7d-24ceb50b0122
  Args:
    relation: :hasFather
    target: Jean_Henri_Fruchaud
    source: Fabiola_Fruchaud
  AddTriple (f9f579e7-dc76-406c-a103-3f00989516d4)
 Call ID: f9f579e7-dc76-406c-a103-3f00989516d4
  Args:
    source: Alexis_Fruchaud
    target: Jean_Henri_Fruchaud
    relation: :hasFather
  Finish (3b84677c-6753-417d-8d56-f6c565662688)
 Call ID: 3b84677c-6753-417d-8d56-f6c565662688
  Args: