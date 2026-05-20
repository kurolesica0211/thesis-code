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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (62139733-b7a3-4638-96d8-f7e15fe17cf6)
 Call ID: 62139733-b7a3-4638-96d8-f7e15fe17cf6
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    type: :Man
  AssignClass (cfc3d6d4-c25c-4c95-9ca3-2d32d5d00358)
 Call ID: cfc3d6d4-c25c-4c95-9ca3-2d32d5d00358
  Args:
    type: :Person
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddLiteral (cc0f093d-b031-4ebb-b942-962fe912b9ae)
 Call ID: cc0f093d-b031-4ebb-b942-962fe912b9ae
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasBirthYear
    literal_value: 1933
    literal_type: xsd:integer
  AddLiteral (79128e9d-ed48-4729-95fe-6f42957cf724)
 Call ID: 79128e9d-ed48-4729-95fe-6f42957cf724
  Args:
    relation: :hasDeathYear
    source: Henri_Philippe_Pierre_Marie_dOrleans
    literal_type: xsd:integer
    literal_value: 2019
  AssignClass (d7a9565a-102d-4d9e-9a96-2317416f17e4)
 Call ID: d7a9565a-102d-4d9e-9a96-2317416f17e4
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (6efe5f26-9b46-4f2b-a746-480d73e393b9)
 Call ID: 6efe5f26-9b46-4f2b-a746-480d73e393b9
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddLiteral (3acb022a-fedb-47f3-90d4-00a33bb2ac3c)
 Call ID: 3acb022a-fedb-47f3-90d4-00a33bb2ac3c
  Args:
    relation: :hasBirthYear
    source: Henri_Count_of_Paris
    literal_value: 1908
    literal_type: xsd:integer
  AddLiteral (5279fb56-5754-4a6b-a77e-f22a257e930e)
 Call ID: 5279fb56-5754-4a6b-a77e-f22a257e930e
  Args:
    literal_value: 1999
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Henri_Count_of_Paris
  AssignClass (5932b81c-09c3-41e3-8d6f-cec1bd80f94a)
 Call ID: 5932b81c-09c3-41e3-8d6f-cec1bd80f94a
  Args:
    source: Princess_Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (47303448-8b6d-4390-a9bc-717adff3bbe8)
 Call ID: 47303448-8b6d-4390-a9bc-717adff3bbe8
  Args:
    type: :Person
    source: Princess_Isabelle_of_Orleans_Braganza
  AddTriple (c685353f-c846-41f6-98ba-d20572a2148f)
 Call ID: c685353f-c846-41f6-98ba-d20572a2148f
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasFather
    target: Henri_Count_of_Paris
  AddTriple (587c9828-bb0a-4532-84cb-8675da0c6117)
 Call ID: 587c9828-bb0a-4532-84cb-8675da0c6117
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasMother
    target: Princess_Isabelle_of_Orleans_Braganza
  AssignClass (a619bd86-22cf-4590-a43f-f8f0ecb4a89b)
 Call ID: a619bd86-22cf-4590-a43f-f8f0ecb4a89b
  Args:
    source: Duchess_Marie_Therese_of_Wurttemberg
    type: :Woman
  AssignClass (9027f587-6fb5-435d-90ad-86b186e4b302)
 Call ID: 9027f587-6fb5-435d-90ad-86b186e4b302
  Args:
    type: :Person
    source: Duchess_Marie_Therese_of_Wurttemberg
  AddLiteral (18eaad7f-39b0-4e7f-ad67-4a79d32dd5d2)
 Call ID: 18eaad7f-39b0-4e7f-ad67-4a79d32dd5d2
  Args:
    source: Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1934
  AddLiteral (d9f47219-8266-4e07-8b01-1b3c6baf95b8)
 Call ID: d9f47219-8266-4e07-8b01-1b3c6baf95b8
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasMarriageYear
    literal_value: 1984
    literal_type: xsd:integer
  AssignClass (4404cee6-6390-4043-987e-4302a07da228)
 Call ID: 4404cee6-6390-4043-987e-4302a07da228
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Woman
  AssignClass (2cadb967-d264-4624-ba74-5c0384fb0369)
 Call ID: 2cadb967-d264-4624-ba74-5c0384fb0369
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Person
  AddLiteral (cdbea038-ce4e-49fa-bf4a-26026037c6d5)
 Call ID: cdbea038-ce4e-49fa-bf4a-26026037c6d5
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1938
  AddLiteral (d8ab1058-9ca8-453a-b3cc-3e0625cf44b7)
 Call ID: d8ab1058-9ca8-453a-b3cc-3e0625cf44b7
  Args:
    literal_type: xsd:integer
    literal_value: 2022
    relation: :hasDeathYear
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AssignClass (d30c4d15-f43b-4f36-a177-dc2c65d91d5f)
 Call ID: d30c4d15-f43b-4f36-a177-dc2c65d91d5f
  Args:
    source: Luis_Cousino_y_Sebire
    type: :Man
  AssignClass (a6fd8d2c-7778-4bf6-aaab-24557dd8ec78)
 Call ID: a6fd8d2c-7778-4bf6-aaab-24557dd8ec78
  Args:
    type: :Person
    source: Luis_Cousino_y_Sebire
  AssignClass (bdc5ffb8-900d-4295-b72e-191ada565121)
 Call ID: bdc5ffb8-900d-4295-b72e-191ada565121
  Args:
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Woman
  AssignClass (d273e280-17c5-4485-96b0-af97696b7189)
 Call ID: d273e280-17c5-4485-96b0-af97696b7189
  Args:
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Person
  AddTriple (314f30a6-9f59-4a66-882f-bcfff89b40c8)
 Call ID: 314f30a6-9f59-4a66-882f-bcfff89b40c8
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasFather
    target: Luis_Cousino_y_Sebire
  AddTriple (e0aa5ac6-3c3b-4f6e-9bf8-319f8b8d4791)
 Call ID: e0aa5ac6-3c3b-4f6e-9bf8-319f8b8d4791
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    relation: :hasMother
  AssignClass (4b6dbb63-e5ee-4116-9725-287fad04734d)
 Call ID: 4b6dbb63-e5ee-4116-9725-287fad04734d
  Args:
    source: Jean_Robert_Boeuf
    type: :Man
  AssignClass (654acaee-9839-428c-8341-9613edaa1a77)
 Call ID: 654acaee-9839-428c-8341-9613edaa1a77
  Args:
    type: :Person
    source: Jean_Robert_Boeuf
  AssignClass (0f2cda0e-afdf-4e8f-90f3-c02710fd9ca7)
 Call ID: 0f2cda0e-afdf-4e8f-90f3-c02710fd9ca7
  Args:
    source: Marie_of_Orleans
    type: :Woman
  AssignClass (db79253a-d2d4-4272-808e-e66b9d06ecee)
 Call ID: db79253a-d2d4-4272-808e-e66b9d06ecee
  Args:
    source: Marie_of_Orleans
    type: :Person
  AddTriple (283294bd-fabe-4aea-9b26-c2bfe4cb688f)
 Call ID: 283294bd-fabe-4aea-9b26-c2bfe4cb688f
  Args:
    relation: :isDaughterOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Marie_of_Orleans
  AddTriple (8e69e7ce-350b-4331-97a2-bb13072c8211)
 Call ID: 8e69e7ce-350b-4331-97a2-bb13072c8211
  Args:
    source: Marie_of_Orleans
    target: Duchess_Marie_Therese_of_Wurttemberg
    relation: :isDaughterOf
  AssignClass (26209210-4de8-49fc-9358-15d45863498e)
 Call ID: 26209210-4de8-49fc-9358-15d45863498e
  Args:
    type: :Man
    source: Prince_Gundakar_of_Liechtenstein
  AssignClass (82746f7c-81f3-4dd4-be1e-af61eabf1d4b)
 Call ID: 82746f7c-81f3-4dd4-be1e-af61eabf1d4b
  Args:
    type: :Person
    source: Prince_Gundakar_of_Liechtenstein
  AssignClass (b9a22b5c-375d-41fc-9482-cf7d01033e1f)
 Call ID: b9a22b5c-375d-41fc-9482-cf7d01033e1f
  Args:
    source: Francois_of_Orleans_brother
    type: :Man
  AssignClass (4f29fbbd-ebe4-4cd1-af54-69e8fe8ccc39)
 Call ID: 4f29fbbd-ebe4-4cd1-af54-69e8fe8ccc39
  Args:
    source: Francois_of_Orleans_brother
    type: :Person
  AddTriple (bfd2bf98-e8af-4cda-970b-45f1411a1bb6)
 Call ID: bfd2bf98-e8af-4cda-970b-45f1411a1bb6
  Args:
    relation: :hasBrother
    target: Francois_of_Orleans_brother
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (2a7a66a2-e5e0-4d85-b7a9-e8be7e3b8dfe)
 Call ID: 2a7a66a2-e5e0-4d85-b7a9-e8be7e3b8dfe
  Args:
    type: :Woman
    source: Diane_of_Orleans
  AssignClass (271513ab-56c2-4d6b-a36d-dcda54bb2aab)
 Call ID: 271513ab-56c2-4d6b-a36d-dcda54bb2aab
  Args:
    source: Diane_of_Orleans
    type: :Person
  AddTriple (5c674246-6f65-4926-9e62-c86f31f68f7f)
 Call ID: 5c674246-6f65-4926-9e62-c86f31f68f7f
  Args:
    target: Diane_of_Orleans
    relation: :hasSister
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (ed710be3-5b6b-49c6-95da-c99e8a19662b)
 Call ID: ed710be3-5b6b-49c6-95da-c99e8a19662b
  Args:
    source: Michel_of_Orleans
    type: :Man
  AssignClass (90a13c5b-2862-4e82-a139-ca31fd308920)
 Call ID: 90a13c5b-2862-4e82-a139-ca31fd308920
  Args:
    type: :Person
    source: Michel_of_Orleans
  AddTriple (ced990ac-4559-40ad-8142-af942f9c9af4)
 Call ID: ced990ac-4559-40ad-8142-af942f9c9af4
  Args:
    target: Michel_of_Orleans
    relation: :hasBrother
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (8b48eeec-ae45-4ef6-bea1-5438db6731e3)
 Call ID: 8b48eeec-ae45-4ef6-bea1-5438db6731e3
  Args:
    source: Thibaut_of_Orleans
    type: :Man
  AssignClass (a6e11fb8-bef9-4d14-b3c1-2e27103d8a31)
 Call ID: a6e11fb8-bef9-4d14-b3c1-2e27103d8a31
  Args:
    type: :Person
    source: Thibaut_of_Orleans
  AddTriple (88bed7df-5e4e-4c58-b579-f6e54110f1a4)
 Call ID: 88bed7df-5e4e-4c58-b579-f6e54110f1a4
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasBrother
    target: Thibaut_of_Orleans
  AssignClass (49f9e499-b94e-4c61-97a9-271a9da84da2)
 Call ID: 49f9e499-b94e-4c61-97a9-271a9da84da2
  Args:
    type: :Man
    source: Jacques_of_Orleans
  AssignClass (426730b5-cd9b-4eea-8f04-12e6432dfae5)
 Call ID: 426730b5-cd9b-4eea-8f04-12e6432dfae5
  Args:
    type: :Person
    source: Jacques_of_Orleans
  AddTriple (f18e1dcf-2197-4b65-854f-9c90e0286c04)
 Call ID: f18e1dcf-2197-4b65-854f-9c90e0286c04
  Args:
    relation: :hasBrother
    target: Jacques_of_Orleans
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (5211665c-d555-46a5-9789-7393fb30b628)
 Call ID: 5211665c-d555-46a5-9789-7393fb30b628
  Args:
    type: :Man
    source: Charles_Louis_dOrleans
  AssignClass (048a9f9d-d741-4c77-98a6-6ca013bd88b4)
 Call ID: 048a9f9d-d741-4c77-98a6-6ca013bd88b4
  Args:
    type: :Person
    source: Charles_Louis_dOrleans
  AddTriple (45b21ae2-131b-4c5f-aa9a-a3ab626ff508)
 Call ID: 45b21ae2-131b-4c5f-aa9a-a3ab626ff508
  Args:
    relation: :hasFather
    target: Jacques_of_Orleans
    source: Charles_Louis_dOrleans
  AssignClass (527bcfa0-74d2-4306-bc14-25095813ee5b)
 Call ID: 527bcfa0-74d2-4306-bc14-25095813ee5b
  Args:
    source: Foulques_dOrleans
    type: :Man
  AssignClass (fd3cee31-7f46-46a0-89d7-a26166e939b0)
 Call ID: fd3cee31-7f46-46a0-89d7-a26166e939b0
  Args:
    source: Foulques_dOrleans
    type: :Person
  AddTriple (ddcaf8c4-7fe2-48a0-9821-53a1f7a5f683)
 Call ID: ddcaf8c4-7fe2-48a0-9821-53a1f7a5f683
  Args:
    source: Foulques_dOrleans
    relation: :hasFather
    target: Jacques_of_Orleans
  AssignClass (f32976bc-005c-422e-a54a-7d13b0f394f9)
 Call ID: f32976bc-005c-422e-a54a-7d13b0f394f9
  Args:
    source: Francois_of_Orleans_son
    type: :Man
  AssignClass (d6159c66-1bd4-4d71-9dd6-5ada4e710e31)
 Call ID: d6159c66-1bd4-4d71-9dd6-5ada4e710e31
  Args:
    type: :Person
    source: Francois_of_Orleans_son
  AddTriple (4c1b361b-26a9-461e-ba1b-c8ae7753ff0a)
 Call ID: 4c1b361b-26a9-461e-ba1b-c8ae7753ff0a
  Args:
    relation: :isSonOf
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Francois_of_Orleans_son
  AssignClass (b0e4fff3-267e-42fb-9635-6de5f4f25741)
 Call ID: b0e4fff3-267e-42fb-9635-6de5f4f25741
  Args:
    type: :Man
    source: Jean_of_Orleans
  AssignClass (3d20b8ee-5d45-4f48-b466-46ba51ec4321)
 Call ID: 3d20b8ee-5d45-4f48-b466-46ba51ec4321
  Args:
    source: Jean_of_Orleans
    type: :Person
  AddTriple (f344bac8-6699-4d51-8ed8-42a792fa8e8e)
 Call ID: f344bac8-6699-4d51-8ed8-42a792fa8e8e
  Args:
    target: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :isSonOf
    source: Jean_of_Orleans
  Finish (a2972d50-af4d-4352-950c-6d5fb2aa20c7)
 Call ID: a2972d50-af4d-4352-950c-6d5fb2aa20c7
  Args: