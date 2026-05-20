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
Queen Margrethe II


Princess Benedikte of Denmark, Princess of Sayn-Wittgenstein-Berleburg RE, SKmd, D.Ht.
(Benedikte Astrid Ingeborg Ingrid, born 29 April 1944) is a member of the Danish royal family.
She is the second daughter and child of King Frederik IX and Queen Ingrid of Denmark.
She is a younger sister of Queen Margrethe II of Denmark, and therefore an aunt of Margrethe's son, the current King of Denmark, Frederik X.
She is also an older sister of Queen Anne-Marie of Greece.
Princess Benedikte often represents the Danish monarch at official or semi-official events.
She and her late husband, Richard, 6th Prince of Sayn-Wittgenstein-Berleburg, had three children.
Princess Benedikte is currently tenth and last in the line of succession to the Danish throne.
Early life

Birth and family

Benedikte was born on 29 April 1944 at Frederik VIII's Palace, her parents' residence at the Amalienborg palace complex, the principal residence of the Danish royal family in the district of Frederiksstaden in central Copenhagen.
She was the second child and daughter of Crown Prince Frederik and Crown Princess Ingrid of Denmark.
Her father was the eldest son of King Christian X and Queen Alexandrine of Denmark, and her mother was the only daughter of Crown Prince Gustav Adolf of Sweden and his first wife, Princess Margaret of Connaught.
Her birth took place during Nazi Germany's Occupation of Denmark.
The day after the birth of the princess, members of the Danish resistance group Holger Danske performed a salute of 21 bombs in the Ørstedsparken public park in central Copenhagen as a reference to the traditional 21-gun salute performed by the Danish Army and Navy at the occasion of royal births.
Her godparents were King Christian X and Queen Alexandrine of Denmark (her paternal grandparents); Prince Gustav of Denmark (paternal grand-uncle); King Gustaf V of Sweden (maternal great-grandfather), Sigvard Bernadotte (maternal uncle); Princess Caroline-Mathilde of Denmark (paternal aunt by marriage); Princess Ingeborg of Denmark (paternal grand-aunt); Princess Margaretha of Sweden (her father's first cousin); Sir Alexander Ramsay (maternal grand-uncle by marriage) and Queen Elizabeth of the United Kingdom.
Benedikte has one elder sister, Margrethe, former Queen of Denmark, and a younger sister, Anne Marie, who was born in 1946 and married Constantine II of Greece.
Childhood and education

Benedikte and her sisters grew up in apartments at Frederik VIII's Palace at Amalienborg in Copenhagen and in Fredensborg Palace in North Zealand.
On 20 April 1947, King Christian X died and Benedikte's father ascended the throne as King Frederik IX.
At the time of her father's accession to the throne, only males could ascend the throne of Denmark.
As her parents had no sons, it was assumed that her uncle Prince Knud would one day assume the throne.
The popularity of Frederik IX and his daughters and the more prominent role of women in Danish life paved the way for a new Act of Succession in 1953 which permitted female succession to the throne following the principle of male-preference primogeniture, where a female can ascend to the throne if she has no brothers.
Benedikte's elder sister Margrethe therefore became heir presumptive, and Benedikte and Anne-Marie became second and third in the line of succession.
Benedikte was educated at N. Zahle's School, a private school in Copenhagen, followed by stays at an English boarding school, Benenden School in Kent (1957), and a Swiss finishing school, Brillantmont International School in Lausanne (1960-1961).
In 1965, she took a class at Margrethe-Skolen, a private fashion and design school in Copenhagen.
Marriage

Benedikte was married on 3 February 1968 at Fredensborg Palace Church to Richard, 6th Prince of Sayn-Wittgenstein-Berleburg (1934–2017).
They had three children:


Upon her marriage, it was decided that Benedikte's children would need to be raised in Denmark in order to have succession rights.
Since the condition was not met, Benedikte's three children are not in line to succeed to the throne.
The children of Benedikte are styled as Highnesses by a Danish Order in Council.
While she and her husband resided at Berleburg Castle, Benedikte and her family retained a close connection to Denmark.
Since her husband's death in 2017, her primary residence has been her apartment at Christian VIII's Palace in Copenhagen.
Interests

Benedikte has undertaken official engagements for the Danish royal family since her youth, particular within the areas of equestrianism, scouting, disabilities and illnesses as well as children and youths.
After Queen Ingrid's death in 2000, she took over several of her patronages and additionally began receiving a yearly appanage.
Among her patronages are SOS Children's Villages (Denmark), Parasport Denmark and the National Association against Eating Disorders and Self-Harm.
As of April 2026, Benedikte holds 23 patronages.
Equestrianism

Benedikte is very involved in equestrian sport and is patron of the World Breeding Federation for Sport Horses, the Danish Warmblood Association and Hestens Værn.
Following revelations about the handling of cases of animal cruelty within the federation as well as allegations of leadership misconduct from members of the board (on which her daughter, Nathalie, was a member) of the federation in 2024, Benedikte withdrew her patronage.
The then chairman of the DRF, Dan Boyter, was revealed to have contacted the private secretaries of both Benedikte and her nephew, King Frederik X, in an effort to have Princess Nathalie (who was among 4 members of the board to raise a motion of no confidence and subsequently file a complain with the National Olympic Committee and Sports Confederation of Denmark's Ethics Committee against Boyter) removed from the board.
Scouting

Benedikte was introduced to the scouting movement when she was a teenager by her mother who had been an active patron of the Danish Girl Guides since 1936.
In 1963, at the age of 19, Benedikte stepped in for her mother, who had fallen ill, and opened the Guiding World Conference in Nyborg with a speech held in both English and French.
Benedikte has retained a close commitment to Girl Guide and Girl Scout organisations in Denmark as well as internationally.
She succeeded her mother as chairman of Pigespejdernes Fællesråd Danmark (Joint Committee of Girl Guides in Denmark).
She is patron of De grønne pigespejdere (The Green Girl Guides, Denmark), Det Danske Spejderkorps (The Danish Guide and Scout Association) and the Danish YWCA in London.
She is an honorary member of the St George's Guilds in Denmark.
Honours and awards

As Princess of Denmark, Benedikte is entitled to the style "Her Royal Highness".



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
  AssignClass (c4891060-21b8-4f4e-bca6-8ad7c0665e84)
 Call ID: c4891060-21b8-4f4e-bca6-8ad7c0665e84
  Args:
    type: :Person
    source: Princess Benedikte of Denmark
  AssignClass (9c68dc0d-b6c1-4e51-b130-dbbc877b0b6b)
 Call ID: 9c68dc0d-b6c1-4e51-b130-dbbc877b0b6b
  Args:
    source: Princess Benedikte of Denmark
    type: :Woman
  AddLiteral (35f5b984-2e88-4b47-93c6-1135b0fc9c71)
 Call ID: 35f5b984-2e88-4b47-93c6-1135b0fc9c71
  Args:
    source: Princess Benedikte of Denmark
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1944
  AssignClass (9b1f2181-659f-47cf-ac5e-f85a9623cff7)
 Call ID: 9b1f2181-659f-47cf-ac5e-f85a9623cff7
  Args:
    type: :Person
    source: King Frederik IX
  AssignClass (422422c7-8c0e-4b72-b058-485430022c41)
 Call ID: 422422c7-8c0e-4b72-b058-485430022c41
  Args:
    source: King Frederik IX
    type: :Man
  AssignClass (429423ec-d398-4616-9354-3637805feb95)
 Call ID: 429423ec-d398-4616-9354-3637805feb95
  Args:
    source: Queen Ingrid of Denmark
    type: :Person
  AssignClass (50ed7f0c-5f4d-4f4a-bb18-6554b3795c03)
 Call ID: 50ed7f0c-5f4d-4f4a-bb18-6554b3795c03
  Args:
    type: :Woman
    source: Queen Ingrid of Denmark
  AddTriple (e05c5ea1-5714-4c0b-b9ec-d270629bf068)
 Call ID: e05c5ea1-5714-4c0b-b9ec-d270629bf068
  Args:
    source: Princess Benedikte of Denmark
    relation: :hasFather
    target: King Frederik IX
  AddTriple (b608adad-3f21-4ad6-833c-321cefb12536)
 Call ID: b608adad-3f21-4ad6-833c-321cefb12536
  Args:
    source: Princess Benedikte of Denmark
    target: Queen Ingrid of Denmark
    relation: :hasMother
  AssignClass (97fc3ff3-3ccf-4a6b-bc9b-a0f1849db09e)
 Call ID: 97fc3ff3-3ccf-4a6b-bc9b-a0f1849db09e
  Args:
    type: :Person
    source: Queen Margrethe II
  AssignClass (af458e15-132c-47a4-98af-324b59c9cb06)
 Call ID: af458e15-132c-47a4-98af-324b59c9cb06
  Args:
    type: :Woman
    source: Queen Margrethe II
  AddTriple (f0bd105d-23bb-4ac9-9b3f-572412c8d085)
 Call ID: f0bd105d-23bb-4ac9-9b3f-572412c8d085
  Args:
    target: Queen Margrethe II
    relation: :isSisterOf
    source: Princess Benedikte of Denmark
  AssignClass (1277ba88-6970-4f6b-aec8-ff712981d644)
 Call ID: 1277ba88-6970-4f6b-aec8-ff712981d644
  Args:
    type: :Person
    source: Frederik X
  AssignClass (80320041-8797-4dc6-9e54-e0fcd2c254fc)
 Call ID: 80320041-8797-4dc6-9e54-e0fcd2c254fc
  Args:
    source: Frederik X
    type: :Man
  AddTriple (1d3f6da3-158f-4423-9e6c-7e83546e773f)
 Call ID: 1d3f6da3-158f-4423-9e6c-7e83546e773f
  Args:
    relation: :isSonOf
    target: Queen Margrethe II
    source: Frederik X
  AssignClass (cb63b661-94c5-4e0d-9141-9692d6d019fe)
 Call ID: cb63b661-94c5-4e0d-9141-9692d6d019fe
  Args:
    type: :Person
    source: Queen Anne-Marie of Greece
  AssignClass (662a3503-497a-421a-bf3e-d08f1294d825)
 Call ID: 662a3503-497a-421a-bf3e-d08f1294d825
  Args:
    type: :Woman
    source: Queen Anne-Marie of Greece
  AddTriple (c7ad39de-b225-4844-9641-886a639a0542)
 Call ID: c7ad39de-b225-4844-9641-886a639a0542
  Args:
    relation: :isSisterOf
    target: Queen Anne-Marie of Greece
    source: Princess Benedikte of Denmark
  AssignClass (05b03ed4-6fda-4f29-b760-0cf9aa879a2b)
 Call ID: 05b03ed4-6fda-4f29-b760-0cf9aa879a2b
  Args:
    source: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (7f28c498-9b15-468a-bf34-0c3353af1772)
 Call ID: 7f28c498-9b15-468a-bf34-0c3353af1772
  Args:
    source: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
    type: :Man
  AddLiteral (cc420b4f-2df1-4701-8616-66c654d8bd52)
 Call ID: cc420b4f-2df1-4701-8616-66c654d8bd52
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1968
    source: Princess Benedikte of Denmark
  AddTriple (f9467b1b-59b1-4cac-8fbe-4573f6572897)
 Call ID: f9467b1b-59b1-4cac-8fbe-4573f6572897
  Args:
    source: Princess Benedikte of Denmark
    target: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
    relation: :hasRelation
  AssignClass (80904072-fc5c-44ee-a3d3-706bb2300e94)
 Call ID: 80904072-fc5c-44ee-a3d3-706bb2300e94
  Args:
    type: :Person
    source: King Christian X
  AssignClass (2f0e1dc6-9fba-484d-aa3e-db7a250aae99)
 Call ID: 2f0e1dc6-9fba-484d-aa3e-db7a250aae99
  Args:
    source: King Christian X
    type: :Man
  AssignClass (64ff36e0-7f5a-42db-9c4a-8eb3346eb1ae)
 Call ID: 64ff36e0-7f5a-42db-9c4a-8eb3346eb1ae
  Args:
    source: Queen Alexandrine of Denmark
    type: :Person
  AssignClass (2d7103bf-f993-4b9e-906c-42db34cff694)
 Call ID: 2d7103bf-f993-4b9e-906c-42db34cff694
  Args:
    type: :Woman
    source: Queen Alexandrine of Denmark
  AddTriple (d692c025-a9fb-47e3-886c-7999fdb0cc69)
 Call ID: d692c025-a9fb-47e3-886c-7999fdb0cc69
  Args:
    relation: :hasFather
    target: King Christian X
    source: King Frederik IX
  AddTriple (7ffab202-f878-4ffc-b78e-e2b419943c8c)
 Call ID: 7ffab202-f878-4ffc-b78e-e2b419943c8c
  Args:
    relation: :hasMother
    target: Queen Alexandrine of Denmark
    source: King Frederik IX
  AssignClass (4862ed06-334b-447d-9306-14f2935303d2)
 Call ID: 4862ed06-334b-447d-9306-14f2935303d2
  Args:
    type: :Person
    source: Crown Prince Gustav Adolf of Sweden
  AssignClass (f1ba3dc1-c5d3-4b78-bc5b-53c50b476425)
 Call ID: f1ba3dc1-c5d3-4b78-bc5b-53c50b476425
  Args:
    type: :Man
    source: Crown Prince Gustav Adolf of Sweden
  AssignClass (7dfc39a1-7a90-4bec-a8cc-b6d33889c48a)
 Call ID: 7dfc39a1-7a90-4bec-a8cc-b6d33889c48a
  Args:
    type: :Person
    source: Princess Margaret of Connaught
  AssignClass (a3dc1495-c739-429a-a571-3b79128603be)
 Call ID: a3dc1495-c739-429a-a571-3b79128603be
  Args:
    source: Princess Margaret of Connaught
    type: :Woman
  AddTriple (b6811bc3-eddd-4f3e-8a71-2d92e915b902)
 Call ID: b6811bc3-eddd-4f3e-8a71-2d92e915b902
  Args:
    relation: :hasFather
    target: Crown Prince Gustav Adolf of Sweden
    source: Queen Ingrid of Denmark
  AddTriple (4710b451-b605-4510-8d97-2d3e900a637d)
 Call ID: 4710b451-b605-4510-8d97-2d3e900a637d
  Args:
    relation: :hasMother
    target: Princess Margaret of Connaught
    source: Queen Ingrid of Denmark
  AssignClass (3659c691-fdc5-4046-847c-593c17b35469)
 Call ID: 3659c691-fdc5-4046-847c-593c17b35469
  Args:
    type: :Person
    source: Nathalie
  AssignClass (702dd24e-4080-459e-b7c7-899a43f2421e)
 Call ID: 702dd24e-4080-459e-b7c7-899a43f2421e
  Args:
    source: Nathalie
    type: :Woman
  AddTriple (f958720d-1062-4880-bf8b-78836ca2e370)
 Call ID: f958720d-1062-4880-bf8b-78836ca2e370
  Args:
    source: Nathalie
    target: Princess Benedikte of Denmark
    relation: :isDaughterOf
  AddTriple (eff813f4-88d5-4b0c-a1a0-5302e40118dc)
 Call ID: eff813f4-88d5-4b0c-a1a0-5302e40118dc
  Args:
    source: Nathalie
    relation: :isDaughterOf
    target: Richard, 6th Prince of Sayn-Wittgenstein-Berleburg
  AssignClass (83ba4a59-f9f2-43fc-b0e8-97d74f99d5fe)
 Call ID: 83ba4a59-f9f2-43fc-b0e8-97d74f99d5fe
  Args:
    source: Constantine II of Greece
    type: :Person
  AssignClass (0a18d055-4c25-467a-8faa-9fae3af5fe78)
 Call ID: 0a18d055-4c25-467a-8faa-9fae3af5fe78
  Args:
    source: Constantine II of Greece
    type: :Man
  AddTriple (7d37f78a-05c5-49e0-9c4e-72f9cc9129cb)
 Call ID: 7d37f78a-05c5-49e0-9c4e-72f9cc9129cb
  Args:
    source: Queen Anne-Marie of Greece
    target: Constantine II of Greece
    relation: :hasRelation
  Finish (1b5e0f9f-7031-4d72-bf16-8cbd7a7b09c1)
 Call ID: 1b5e0f9f-7031-4d72-bf16-8cbd7a7b09c1
  Args: