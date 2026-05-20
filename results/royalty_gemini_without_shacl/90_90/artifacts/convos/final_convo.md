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
Princess Marina of Greece and Denmark (Greek: Μαρίνα; 13 December  1906 – 27 August 1968), later Duchess of Kent, was a Greek and Danish princess by birth and a British princess by marriage.
A granddaughter of King George I of Greece and Queen Olga, she was the daughter of Prince Nicholas of Greece and Denmark and Grand Duchess Elena Vladimirovna of Russia.
In 1934, she married Prince George, Duke of Kent, the fourth son of King George V and Queen Mary.
Edward, Alexandra, and Michael.
Early life

Marina was born on 13 December 1906 in Athens, Greece, during the reign of her paternal grandfather, George I of Greece.
She was the third and youngest daughter of Prince Nicholas of Greece and Denmark and his wife, Grand Duchess Elena Vladimirovna of Russia.
Her father was the third son of George I of Greece and Queen Olga, while her mother was the only daughter of Grand Duke Vladimir Alexandrovich and Grand Duchess Maria Pavlovna of Russia.
Through her father she was a great-granddaughter of Christian IX of Denmark, and through her mother a granddaughter of Emperor Alexander II of Russia.
Marina had two elder sisters, Princess Olga and Princess Elizabeth.
Olga married Prince Paul of Yugoslavia in 1923; following the assassination of his cousin, Alexander I of Yugoslavia, Paul served as Prince Regent of Yugoslavia from 1934 to 1941.
One of their paternal uncles was Prince Andrew of Greece and Denmark, father of Prince Philip, Duke of Edinburgh, making Marina and her sisters Philip's first cousins.
Marina spent her early years in Greece and lived with her parents and paternal grandparents at Tatoi Palace.
She and her sisters were raised to be devout and religious, a quality encouraged by their grandmother, Queen Olga of Greece.
The family travelled outside Greece frequently, especially during the summer months.
Marina's first recorded visit to Britain was in 1910, when she was three, following the death of her godfather, Edward VII.
During that visit she met her godmother and future mother-in-law, Queen Mary, who treated Marina and her sisters as if they were her own children.
The Greek royal family was forced into exile when Marina was 11, following the overthrow of the monarchy.
They later settled in Paris, while Marina spent periods living with her extended family across Europe.
Marriage and children

Wedding ceremony

In 1932, Marina met Prince George (later the Duke of Kent), her second cousin through Christian IX of Denmark, in London.
Their betrothal was announced in August 1934, and George was created Duke of Kent on 9 October.
It was the first major royal wedding since that of Prince Albert, Duke of York (later George VI), and Lady Elizabeth Bowes-Lyon (later Queen Elizabeth the Queen mother) 11 years earlier.
Marina remains the most recent foreign princess to marry into the British royal family.
Married life

Marina and George established their first home at 3 Belgrave Square, close to Buckingham Palace.
Marina became patroness of several organisations and charities, including the Elizabeth Garrett Anderson Hospital, the Women's Hospital Fund, and the Central School of Speech and Drama, causes she continued to support throughout her life.
She developed a close relationship with her mother-in-law with whom she often spent time while George was undertaking royal duties.
The couple had three children:


George was killed on 25 August 1942 in an air crash at Eagle's Rock, near Dunbeath, Caithness, Scotland, while on active service with the Royal Air Force.
According to royal biographer Hugo Vickers, Marina was "the only war widow in Britain whose estate was forced to pay death duties".
During the Second World War, Marina trained as a nurse for three months under the pseudonym "Sister Kay" and joined the Civil Nursing Reserve.
Later life and death

After her husband's death, Marina continued to be an active member of the British royal family, carrying out a wide range of royal and official engagements.
In 1947, Marina visited Greece and Italy.
Later in 1952, Marina visited Sarawak (then a British Crown Colony), where she laid the foundation stone of the St. Thomas's Cathedral in Kuching.
In 1954, Marina was granted an Apartment at Kensington Palace as a permanent grace-and-favour residence.
During her early widowhood she had often stayed with her mother-in-law at Marlborough House; however Mary's death in 1953 created a need for Marina to have her own London residence.
The Apartment had stood vacant for nearly 15 years, having previously been the home of Princess Louise, Duchess of Argyll, prior to her death in 1939.
As the apartment was considered too large for Marina's needs, its eastern half was divided to create Apartment 1A.
During the renovations, Marina reportedly considered removing an original Wren staircase inside Apartment 1, finding it "too much like a servant's staircase" and too narrow for descending in full evening dress; palace officials intervened to prevent its removal.
Marina and her three children took up residence in October 1955, and Apartment 1 remained her home until her death in 1968.
In March 1957, when the Gold Coast achieved independence from Britain as Ghana, Marina was appointed to represent the Queen at the celebrations.
50 years later, at the 50th anniversary of Ghana's independence, her son, Edward, was appointed by the Queen to represent her.
Marina earned a place in the International Best Dressed List Hall of Fame in 1960, together with the Princess of Monaco, Patricia Lopez-Willshaw, and Merle Oberon.
In September and October 1966, when the British Protectorates of Bechuanaland and Basutoland became the Republic of Botswana and the Kingdom of Lesotho respectively, Marina was again appointed to represent the Queen at both independence celebrations.
The main public hospital in Gaborone, the new capital of Botswana, is named Princess Marina Hospital.
She served as Chancellor of the University of Kent at Canterbury from 1963 until her death.
Marina died at 11:40 am on 27 August 1968 at Kensington Palace from a brain tumour, aged 61.
Her funeral service was held at St. George's Chapel, Windsor Castle, on 30 August.
Her funeral was the last royal ceremony attended by her brother-in-law, the former king Edward VIII.
Marina's will was sealed in London after her death.
Legacy

Marina gave her name to a number of institutions and facilities, including:


References in popular culture

Titles, styles, honours, and arms

Titles and styles

Marina was known as the Princess Marina of Greece.
After her marriage she was styled Her Royal Highness The Duchess of Kent, and was later known as Her Royal Highness The Princess Marina, Duchess of Kent.



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
  AssignClass (61ef0e74-2ff0-40b0-ae5e-271b1ef8074b)
 Call ID: 61ef0e74-2ff0-40b0-ae5e-271b1ef8074b
  Args:
    type: :Woman
    source: :Princess_Marina_of_Greece_and_Denmark
  AssignClass (7936fff4-b455-42b9-ba59-a025302e5cb3)
 Call ID: 7936fff4-b455-42b9-ba59-a025302e5cb3
  Args:
    type: :Man
    source: :Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (391ff06c-60ac-4c01-9a89-168808b5664d)
 Call ID: 391ff06c-60ac-4c01-9a89-168808b5664d
  Args:
    type: :Woman
    source: :Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (2704eb1b-2b77-44e5-9576-4c632c48ea93)
 Call ID: 2704eb1b-2b77-44e5-9576-4c632c48ea93
  Args:
    type: :Man
    source: :King_George_I_of_Greece
  AssignClass (b583489d-b643-40e4-9f6e-700251888eec)
 Call ID: b583489d-b643-40e4-9f6e-700251888eec
  Args:
    type: :Woman
    source: :Queen_Olga_of_Greece
  AssignClass (9d09f0f1-3cb9-4a2b-b566-fe8250766d8b)
 Call ID: 9d09f0f1-3cb9-4a2b-b566-fe8250766d8b
  Args:
    type: :Man
    source: :Prince_George_Duke_of_Kent
  AssignClass (fb598cdb-1d84-40b3-81dd-9200e6bb7d00)
 Call ID: fb598cdb-1d84-40b3-81dd-9200e6bb7d00
  Args:
    type: :Man
    source: :King_George_V
  AssignClass (53699ac2-fbf4-43c9-a348-19c6a31743d6)
 Call ID: 53699ac2-fbf4-43c9-a348-19c6a31743d6
  Args:
    type: :Woman
    source: :Queen_Mary
  AssignClass (1b71cc5d-2f5c-4e49-8932-d56d397a4985)
 Call ID: 1b71cc5d-2f5c-4e49-8932-d56d397a4985
  Args:
    type: :Man
    source: :Edward
  AssignClass (a54b08c9-1d4f-4edb-9089-1a8d2b3b6765)
 Call ID: a54b08c9-1d4f-4edb-9089-1a8d2b3b6765
  Args:
    type: :Woman
    source: :Alexandra
  AssignClass (ca86ce52-0cb8-4c94-9962-bce25e5fd4d4)
 Call ID: ca86ce52-0cb8-4c94-9962-bce25e5fd4d4
  Args:
    type: :Man
    source: :Michael
  AddTriple (57325ea5-6f69-4ed1-945d-f0b125a8ca66)
 Call ID: 57325ea5-6f69-4ed1-945d-f0b125a8ca66
  Args:
    target: :Prince_Nicholas_of_Greece_and_Denmark
    source: :Princess_Marina_of_Greece_and_Denmark
    relation: :hasFather
  AddTriple (1bc82d1c-8c85-4c58-9abb-e28789b6596c)
 Call ID: 1bc82d1c-8c85-4c58-9abb-e28789b6596c
  Args:
    source: :Princess_Marina_of_Greece_and_Denmark
    target: :Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AddTriple (aa096956-ed00-4384-8166-ec4a39b1cd2b)
 Call ID: aa096956-ed00-4384-8166-ec4a39b1cd2b
  Args:
    relation: :hasFather
    source: :Prince_Nicholas_of_Greece_and_Denmark
    target: :King_George_I_of_Greece
  AddTriple (785fe42b-7433-4448-8d98-8b9a02daf65e)
 Call ID: 785fe42b-7433-4448-8d98-8b9a02daf65e
  Args:
    relation: :hasMother
    target: :Queen_Olga_of_Greece
    source: :Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (f634f732-e3aa-428d-966e-84bb22a185f9)
 Call ID: f634f732-e3aa-428d-966e-84bb22a185f9
  Args:
    target: :King_George_V
    source: :Prince_George_Duke_of_Kent
    relation: :hasFather
  AddTriple (52408b20-8a1d-4930-a3c9-0b3d8375a75a)
 Call ID: 52408b20-8a1d-4930-a3c9-0b3d8375a75a
  Args:
    source: :Prince_George_Duke_of_Kent
    target: :Queen_Mary
    relation: :hasMother
  AddTriple (944f1431-ce90-4cb4-8ece-cd05f52bbe8b)
 Call ID: 944f1431-ce90-4cb4-8ece-cd05f52bbe8b
  Args:
    relation: :hasFather
    source: :Edward
    target: :Prince_George_Duke_of_Kent
  AddTriple (a7ebca9a-de30-4d83-a2df-0c36cb8251d5)
 Call ID: a7ebca9a-de30-4d83-a2df-0c36cb8251d5
  Args:
    target: :Princess_Marina_of_Greece_and_Denmark
    source: :Edward
    relation: :hasMother
  AddTriple (699d05c2-0775-4c6b-a79c-b461acd7a1ce)
 Call ID: 699d05c2-0775-4c6b-a79c-b461acd7a1ce
  Args:
    source: :Alexandra
    target: :Prince_George_Duke_of_Kent
    relation: :hasFather
  AddTriple (86a1ac26-6bf1-41b7-8f66-0f6d9bd15c96)
 Call ID: 86a1ac26-6bf1-41b7-8f66-0f6d9bd15c96
  Args:
    relation: :hasMother
    target: :Princess_Marina_of_Greece_and_Denmark
    source: :Alexandra
  AddTriple (d9dcfa1e-7f19-40b5-a9b7-4d8b643563c2)
 Call ID: d9dcfa1e-7f19-40b5-a9b7-4d8b643563c2
  Args:
    target: :Prince_George_Duke_of_Kent
    source: :Michael
    relation: :hasFather
  AddTriple (9c8de994-394a-4126-86b7-c38e2c54276e)
 Call ID: 9c8de994-394a-4126-86b7-c38e2c54276e
  Args:
    source: :Michael
    target: :Princess_Marina_of_Greece_and_Denmark
    relation: :hasMother
  AddLiteral (d00fbd4e-9a58-4bbb-acb9-096f92dce60b)
 Call ID: d00fbd4e-9a58-4bbb-acb9-096f92dce60b
  Args:
    literal_value: 1906
    source: :Princess_Marina_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (10cf49ef-d673-474d-b6d9-46630179434f)
 Call ID: 10cf49ef-d673-474d-b6d9-46630179434f
  Args:
    source: :Princess_Marina_of_Greece_and_Denmark
    literal_value: 1968
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddLiteral (6f3ed35f-1a3a-439c-9d1f-f55b622c57ad)
 Call ID: 6f3ed35f-1a3a-439c-9d1f-f55b622c57ad
  Args:
    literal_value: 1934
    source: :Princess_Marina_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (d687705d-40c7-4d7f-873a-76feb587d36e)
 Call ID: d687705d-40c7-4d7f-873a-76feb587d36e
  Args: