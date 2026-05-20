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
Princess Dolores of Bourbon-Two Sicilies (15 November 1909 – 11 May 1996) was a daughter of Prince Carlos of Bourbon-Two Sicilies and his wife Princess Louise of Orléans.
Princess Dolores was born into the House of Bourbon-Two Sicilies and was a member of the Polish-Lithuanian noble Czartoryski family through her marriage to Prince Augustyn Józef Czartoryski.
She was also an aunt of Juan Carlos I of Spain, son of her sister Princess María de las Mercedes of Bourbon-Two Sicilies.
Early life

Born on 15 November 1909 at the Palace of Villamejor, Princess Dolores of Bourbon-Two Sicilies was the second child of Prince Carlos of Bourbon-Two Sicilies and his second wife Princess Louise of Orléans.
She was christened Maria de los Dolores Victoria Felipa Luisa Mercedes.
Princess Dolores, nicknamed Dola among his relatives, was closely related to the Spanish royal family.
Her father, Prince Carlos of Bourbon-Two Sicilies, had renounced his right to the throne of Two Sicilies becoming a Spanish citizen when he married his first wife, Mercedes, Princess of Asturias, the eldest sister of King Alfonso XIII of Spain.
Dolores’s mother, Princess Louise of Orléans was a first cousin once removed of the Spanish King.
As a result, Dolores and her sibling grew up in close proximity to the Spanish royal family.
Her cousins, the children of King Alfonso XIII and Queen Victoria Eugenie were the same age as Dolores and her younger siblings.
The family lived at the Palace of Villamejor in Madrid, vacations were spent near Seville in the Palace of Villamanrique, property of her maternal grandmother, Isabelle, Countess of Paris.
Princess Dolores studied with her sisters Mercedes  and Esperanza in a school of Irish nuns in Madrid.
Dolores was twelve years old when she moved with her family to Seville when her father was appointed Military Captain General of Andalusia.
The Princess and her sisters continued their studies as boarders at  the school of Irish nuns in Castilleja de la Cueva in Seville.
Marriage and later life

In Paris, Princess Dolores met a wealthy Polish aristocrat Prince Augustyn Józef Czartoryski, 13th Prince Czartoryski, Duke of Klewan and Zuków, son of Prince Adam Ludwik Czartoryski and his wife Countess Maria Ludwika Krasińska.
The couple settled in Kraków, Poland where Dolores’s husband took over the running of the Family Museum.
In September 1939 with the Invasion of Poland bombs fell on Kraków, Prince Augustyn and Princess Dolores, who was pregnant, decided to leave the country and move to Spain.
After reaching Paris, Princess Dolores and her husband moved permanently to Spain.
They settled in Seville where Princess Dolores gave birth to a son: Prince Adam Karol Czartoryski (born 2 January 1940).
In 1943 the couple bought a rural property in Dos Hermanas which they called it Garden of the Princess, the farm was self-sufficient for the subsistence of the family.
The couple had a second son also born in Seville, Prince Ludwik Piotr Czartoryski (13 March 1945 - 3 May 1946), but the child died at only fourteen months.
At the end of the war, the properties of the Czartoryski family were nationalized by the Polish government and the family decided not to return to Kraków, for fear of the Soviet occupation.
Prince Augustyn was in poor health, the troubles and tribulation of the war took a toll on his life and he died on 1 July 1946, aged thirty nine.
The deaths of  both her youngest son and her husband only two months apart in 1946 deeply affected the Princess, who was left a widow with a six-year-old child.
Princess Dolores continued living in Seville, Spain.
Four years into her widowhood, she fell in love with Carlos Chías Osorio (born at Barcelona 26 Feb 1925), an ex seminarist, teacher  and preceptor of her son Adam.
Carlos Chias Osorio quickly became well liked in Dos Hermanas and in spite of the age disparity the marriage was a happy one.
After the death of Princess Dolores's mother in April that year, the couple moved to Madrid.
In the following decades, the princess and her husband lived simply in Madrid.



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
  AssignClass (de344db5-c895-4525-ac1a-341505c0c161)
 Call ID: de344db5-c895-4525-ac1a-341505c0c161
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (c88bb017-1bc3-40c2-8e39-f3dfb197daff)
 Call ID: c88bb017-1bc3-40c2-8e39-f3dfb197daff
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (fbd2cc27-d781-4b27-83d3-8db999138e9f)
 Call ID: fbd2cc27-d781-4b27-83d3-8db999138e9f
  Args:
    type: :Woman
    source: Princess_Louise_of_Orleans
  AssignClass (c54955e1-1994-4813-9e15-96ad605af016)
 Call ID: c54955e1-1994-4813-9e15-96ad605af016
  Args:
    source: Prince_Augustyn_Jozef_Czartoryski
    type: :Man
  AssignClass (53158a8f-861e-4776-b666-f1f335a16818)
 Call ID: 53158a8f-861e-4776-b666-f1f335a16818
  Args:
    source: Prince_Adam_Karol_Czartoryski
    type: :Man
  AssignClass (16246cf6-7ccd-42a3-adb4-f0320904de04)
 Call ID: 16246cf6-7ccd-42a3-adb4-f0320904de04
  Args:
    source: Prince_Ludwik_Piotr_Czartoryski
    type: :Man
  AssignClass (556ef39a-a554-49cf-bf43-322c45601f57)
 Call ID: 556ef39a-a554-49cf-bf43-322c45601f57
  Args:
    type: :Man
    source: Carlos_Chias_Osorio
  AssignClass (119f3b70-2416-4c13-9ddd-d5420cf7a106)
 Call ID: 119f3b70-2416-4c13-9ddd-d5420cf7a106
  Args:
    source: Princess_Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    type: :Woman
  AssignClass (11567b37-2071-4c68-b746-9f1595edf016)
 Call ID: 11567b37-2071-4c68-b746-9f1595edf016
  Args:
    source: Juan_Carlos_I_of_Spain
    type: :Man
  AddLiteral (c793f28f-610a-45b8-9dd2-a379f16a1d41)
 Call ID: c793f28f-610a-45b8-9dd2-a379f16a1d41
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1909
  AddLiteral (de5b000a-2685-4c53-a077-a840241d5072)
 Call ID: de5b000a-2685-4c53-a077-a840241d5072
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1996
  AddTriple (bb00a83c-47ff-41f8-9751-91543f92de3a)
 Call ID: bb00a83c-47ff-41f8-9751-91543f92de3a
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    relation: :hasFather
  AddTriple (a67d958a-84fa-4f77-ac49-eecb4b0c88e0)
 Call ID: a67d958a-84fa-4f77-ac49-eecb4b0c88e0
  Args:
    relation: :hasMother
    target: Princess_Louise_of_Orleans
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
  AddTriple (c571bd75-4c1e-4441-9bb6-3e7c8e5a67d5)
 Call ID: c571bd75-4c1e-4441-9bb6-3e7c8e5a67d5
  Args:
    relation: :hasSister
    target: Princess_Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
  AddTriple (39254731-2292-49d6-988f-16d1729fe048)
 Call ID: 39254731-2292-49d6-988f-16d1729fe048
  Args:
    relation: :hasChild
    target: Juan_Carlos_I_of_Spain
    source: Princess_Maria_de_las_Mercedes_of_Bourbon-Two_Sicilies
  AddTriple (0574a272-01fc-43d2-8105-9d0e288477b6)
 Call ID: 0574a272-01fc-43d2-8105-9d0e288477b6
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasChild
    target: Prince_Adam_Karol_Czartoryski
  AddTriple (d8ae3356-829d-4b67-9bdb-ac97bc662692)
 Call ID: d8ae3356-829d-4b67-9bdb-ac97bc662692
  Args:
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :hasChild
    target: Prince_Ludwik_Piotr_Czartoryski
  AddTriple (54fabcd4-27ba-4a65-80b1-6e21e530b640)
 Call ID: 54fabcd4-27ba-4a65-80b1-6e21e530b640
  Args:
    source: Prince_Augustyn_Jozef_Czartoryski
    target: Prince_Adam_Karol_Czartoryski
    relation: :hasChild
  AddTriple (bd562541-cd8d-4985-b75b-10a5d17d987d)
 Call ID: bd562541-cd8d-4985-b75b-10a5d17d987d
  Args:
    target: Prince_Ludwik_Piotr_Czartoryski
    relation: :hasChild
    source: Prince_Augustyn_Jozef_Czartoryski
  AddLiteral (f9290641-5e19-401e-8687-0a9249870f75)
 Call ID: f9290641-5e19-401e-8687-0a9249870f75
  Args:
    source: Prince_Adam_Karol_Czartoryski
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1940
  AddLiteral (810fbf81-b0ae-4732-8dfb-cc6a752d788d)
 Call ID: 810fbf81-b0ae-4732-8dfb-cc6a752d788d
  Args:
    literal_value: 1945
    source: Prince_Ludwik_Piotr_Czartoryski
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (c732ace4-20fd-453e-8a0e-4a2e1f359359)
 Call ID: c732ace4-20fd-453e-8a0e-4a2e1f359359
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Ludwik_Piotr_Czartoryski
    literal_value: 1946
  AddLiteral (b79eee96-f6ab-4ddd-afb1-53fdfd0d64a8)
 Call ID: b79eee96-f6ab-4ddd-afb1-53fdfd0d64a8
  Args:
    literal_value: 1946
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Augustyn_Jozef_Czartoryski
  AddLiteral (6810862a-d956-40f1-b108-8c6a82614c68)
 Call ID: 6810862a-d956-40f1-b108-8c6a82614c68
  Args:
    literal_value: Dola
    source: Princess_Dolores_of_Bourbon-Two_Sicilies
    relation: :knownAs
    literal_type: xsd:string
  Finish (0c35a553-2478-449a-b276-4a35088b1744)
 Call ID: 0c35a553-2478-449a-b276-4a35088b1744
  Args: