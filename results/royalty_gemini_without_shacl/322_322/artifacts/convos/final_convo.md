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
  AssignClass (fe9032dc-2435-46f1-939f-5840316717e6)
 Call ID: fe9032dc-2435-46f1-939f-5840316717e6
  Args:
    type: :Man
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AssignClass (bd6c9be9-792d-4af1-9bbe-88046fb90373)
 Call ID: bd6c9be9-792d-4af1-9bbe-88046fb90373
  Args:
    source: Henri_Count_of_Paris
    type: :Man
  AssignClass (9534e06f-c2a5-40e9-a5f3-d6c64ad668df)
 Call ID: 9534e06f-c2a5-40e9-a5f3-d6c64ad668df
  Args:
    source: Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (bd8ab394-f449-416e-ba2f-f8041d08a3bb)
 Call ID: bd8ab394-f449-416e-ba2f-f8041d08a3bb
  Args:
    source: Marie_Therese_of_Wurttemberg
    type: :Woman
  AssignClass (520f794b-4945-4b59-9b64-162e82a998f1)
 Call ID: 520f794b-4945-4b59-9b64-162e82a998f1
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Woman
  AssignClass (00f58dd3-4d34-4358-b032-196b12709e3a)
 Call ID: 00f58dd3-4d34-4358-b032-196b12709e3a
  Args:
    type: :Man
    source: Luis_Cousino_y_Sebire
  AssignClass (cac5cca6-7f73-42f5-b6b9-0677d6e4310d)
 Call ID: cac5cca6-7f73-42f5-b6b9-0677d6e4310d
  Args:
    type: :Woman
    source: Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AssignClass (93784f74-9c6b-47da-8d07-dabce06409cf)
 Call ID: 93784f74-9c6b-47da-8d07-dabce06409cf
  Args:
    type: :Man
    source: Jean_Robert_Boeuf
  AssignClass (f1f6c420-6bea-4a07-a217-65d673c30de5)
 Call ID: f1f6c420-6bea-4a07-a217-65d673c30de5
  Args:
    type: :Woman
    source: Marie_daughter_of_Henri
  AssignClass (f3f2efee-83dc-4231-85b0-b199978186d7)
 Call ID: f3f2efee-83dc-4231-85b0-b199978186d7
  Args:
    type: :Man
    source: Gundakar_of_Liechtenstein
  AssignClass (05bb1ab7-04c3-44de-8703-a6125c24294f)
 Call ID: 05bb1ab7-04c3-44de-8703-a6125c24294f
  Args:
    type: :Man
    source: Francois_brother_of_Henri
  AssignClass (d173abdf-da2a-427c-8699-c9bd55455c14)
 Call ID: d173abdf-da2a-427c-8699-c9bd55455c14
  Args:
    source: Diane_sister_of_Henri
    type: :Woman
  AssignClass (b38c7746-9529-42d7-a18d-36856d95ace7)
 Call ID: b38c7746-9529-42d7-a18d-36856d95ace7
  Args:
    type: :Man
    source: Michel_Count_of_Evreux
  AssignClass (8a30d0ba-ea15-4cf8-b8a7-56f783b7a016)
 Call ID: 8a30d0ba-ea15-4cf8-b8a7-56f783b7a016
  Args:
    type: :Man
    source: Thibaut_Count_of_La_Marche
  AssignClass (15ce68dc-90af-4cc2-a894-fa9d9d289696)
 Call ID: 15ce68dc-90af-4cc2-a894-fa9d9d289696
  Args:
    source: Jacques_Duke_of_Orleans
    type: :Man
  AssignClass (55ecf005-4b24-48a8-8b86-ec060c0bb6f0)
 Call ID: 55ecf005-4b24-48a8-8b86-ec060c0bb6f0
  Args:
    type: :Man
    source: Charles_Louis_dOrleans
  AssignClass (b7ff83d1-988e-438d-adfc-9d8f64cc8161)
 Call ID: b7ff83d1-988e-438d-adfc-9d8f64cc8161
  Args:
    type: :Man
    source: Foulques_dOrleans
  AssignClass (69ea9096-9120-4edc-8061-b754220b97fc)
 Call ID: 69ea9096-9120-4edc-8061-b754220b97fc
  Args:
    source: Francois_son_of_Henri
    type: :Man
  AssignClass (85064708-e0f8-4e43-bfbe-4f9b22468152)
 Call ID: 85064708-e0f8-4e43-bfbe-4f9b22468152
  Args:
    source: Jean_Duke_of_Vendome
    type: :Man
  AssignClass (710b4da1-0959-40ab-992f-69b85488fa31)
 Call ID: 710b4da1-0959-40ab-992f-69b85488fa31
  Args:
    type: :Man
    source: Louis_Alphonse_Duke_of_Anjou
  AddLiteral (cfb3e0dc-c7cf-4b0d-b2bd-39c07c65c6b9)
 Call ID: cfb3e0dc-c7cf-4b0d-b2bd-39c07c65c6b9
  Args:
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasBirthYear
    literal_value: 1933
    literal_type: xsd:integer
  AddLiteral (d251bc80-fd48-4112-955e-a4c5382be020)
 Call ID: d251bc80-fd48-4112-955e-a4c5382be020
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2019
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (c69a2f1a-a4b1-4d63-9a9f-8b503b465066)
 Call ID: c69a2f1a-a4b1-4d63-9a9f-8b503b465066
  Args:
    relation: :hasFather
    target: Henri_Count_of_Paris
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (10a32f89-1ad5-4e0a-9568-ab7d16efc4a5)
 Call ID: 10a32f89-1ad5-4e0a-9568-ab7d16efc4a5
  Args:
    relation: :hasMother
    target: Isabelle_of_Orleans_Braganza
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (c977d4d1-0bbb-4b19-b405-58c3dabc16fa)
 Call ID: c977d4d1-0bbb-4b19-b405-58c3dabc16fa
  Args:
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: Luis_Cousino_y_Sebire
    relation: :hasFather
  AddTriple (95059150-7ec2-4dec-a589-b5cd3dc41401)
 Call ID: 95059150-7ec2-4dec-a589-b5cd3dc41401
  Args:
    relation: :hasMother
    target: Antonia_Maria_Quinones_de_Leon_y_Banuelos
    source: Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
  AddTriple (ec3f86dc-c051-4105-b16a-280c331423cc)
 Call ID: ec3f86dc-c051-4105-b16a-280c331423cc
  Args:
    relation: :hasFather
    target: Henri_Count_of_Paris
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (855df0bd-fb04-42df-ace9-5f484e5df728)
 Call ID: 855df0bd-fb04-42df-ace9-5f484e5df728
  Args:
    relation: :hasBrother
    target: Francois_brother_of_Henri
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (0b11e918-0c7e-4430-b6f9-d3a0df6e48b8)
 Call ID: 0b11e918-0c7e-4430-b6f9-d3a0df6e48b8
  Args:
    target: Diane_sister_of_Henri
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasSister
  AddTriple (3b6b6029-3514-43c9-9fc4-082022b2e92c)
 Call ID: 3b6b6029-3514-43c9-9fc4-082022b2e92c
  Args:
    relation: :hasBrother
    target: Michel_Count_of_Evreux
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (e2933422-4662-47f2-8ae5-2e20d8470a7e)
 Call ID: e2933422-4662-47f2-8ae5-2e20d8470a7e
  Args:
    relation: :hasBrother
    source: Henri_Philippe_Pierre_Marie_dOrleans
    target: Thibaut_Count_of_La_Marche
  AddTriple (4da95163-3378-46a8-a013-b4ea34642cbc)
 Call ID: 4da95163-3378-46a8-a013-b4ea34642cbc
  Args:
    relation: :hasBrother
    target: Jacques_Duke_of_Orleans
    source: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (1774d87c-a53c-4fe6-a5d9-98d77784404c)
 Call ID: 1774d87c-a53c-4fe6-a5d9-98d77784404c
  Args:
    relation: :hasFather
    source: Charles_Louis_dOrleans
    target: Jacques_Duke_of_Orleans
  AddTriple (d01ae639-9160-47eb-a864-51d2b6ab8e99)
 Call ID: d01ae639-9160-47eb-a864-51d2b6ab8e99
  Args:
    target: Jacques_Duke_of_Orleans
    source: Foulques_dOrleans
    relation: :hasFather
  AddTriple (de7f43e5-6ccf-4fa4-b060-e40ef0b56b7c)
 Call ID: de7f43e5-6ccf-4fa4-b060-e40ef0b56b7c
  Args:
    relation: :hasFather
    source: Francois_son_of_Henri
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (7874ba7e-56cb-4b16-9b59-ae337a942ffa)
 Call ID: 7874ba7e-56cb-4b16-9b59-ae337a942ffa
  Args:
    relation: :hasFather
    source: Jean_Duke_of_Vendome
    target: Henri_Philippe_Pierre_Marie_dOrleans
  AddTriple (06f6fa84-b4f0-4e5e-bf25-25ce210ae380)
 Call ID: 06f6fa84-b4f0-4e5e-bf25-25ce210ae380
  Args:
    target: Marie_daughter_of_Henri
    source: Henri_Philippe_Pierre_Marie_dOrleans
    relation: :hasDaughter
  AddTriple (237a0d82-6254-46e3-8851-0e4772d603fd)
 Call ID: 237a0d82-6254-46e3-8851-0e4772d603fd
  Args:
    target: Henri_Philippe_Pierre_Marie_dOrleans
    source: Marie_daughter_of_Henri
    relation: :hasFather
  AddTriple (823f0aff-f231-45ad-a0be-5b3c2747d96b)
 Call ID: 823f0aff-f231-45ad-a0be-5b3c2747d96b
  Args:
    target: Marie_Therese_of_Wurttemberg
    source: Marie_daughter_of_Henri
    relation: :hasMother
  Finish (cf401d6d-8c93-4bcc-9ba4-624a36831679)
 Call ID: cf401d6d-8c93-4bcc-9ba4-624a36831679
  Args: