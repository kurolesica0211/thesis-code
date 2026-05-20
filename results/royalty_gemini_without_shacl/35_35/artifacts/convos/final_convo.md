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
Louis Alphonse de Bourbon, Duke of Anjou (Spanish: Luis Alfonso Gonzalo Víctor Manuel Marco de Borbón y Martínez-Bordiú; born 25 April 1974) is regarded by French Legitimists as the head of the House of Bourbon and the rightful claimant to the defunct throne of France under the name Louis XX.
His claim is based on his descent from Louis XIV (r. 1643–1715) through his grandson Philip V of Spain.
The rival Orleanist pretenders argue that this, as well as being born a Spanish citizen, makes Louis Alphonse ineligible for the throne.
Louis Alphonse is patrilineally the senior great-grandson of King Alfonso XIII of Spain.
Early life

Birth

Louis Alphonse was born in Madrid, the second son of Alfonso de Borbón, Duke of Anjou and Cádiz, and of his wife María del Carmen Martínez-Bordiú y Franco, eldest granddaughter of Francisco Franco.
Alfonso was at that time the dauphin (using "Duke of Bourbon" as title of pretence) according to those who supported the claim of his father, Infante Jaime, Duke of Segovia to the French throne.
On 20 March 1975, Jaime died, and Alfonso then asserted his claim to be Head of the House of Bourbon and Legitimist claimant to the throne of France.
Childhood

Louis Alphonse's parents separated in 1982, and their Catholic marriage was annulled in 1986.
On 7 February 1984, Louis Alphonse's older brother Francisco died as the result of a car crash in which Louis Alphonse was also injured, although less so than their father, who was driving the automobile.
From that date Louis Alphonse was recognised as the heir apparent to his father by the Legitimists.
As such, he was given the additional title Duke of Bourbon on 27 September 1984 by his father.
In 1987, the Spanish government declared that titles traditionally attached to the dynasty (such as the Dukedom of Cádiz) would henceforth be borne by its members on a lifetime only basis, forestalling Louis Alphonse from inheriting that grandeeship.
Education

Louis Alphonse took his primary studies at College Molière, a bilingual school, where he earned his baccalaureate.
Louis is multilingual, speaking English, Spanish, and French (in addition to some Italian and German).
In 1994, Louis Alphonse received 150 million pesetas from a lawsuit against Vail Associates, which owned the ski resort where the accident occurred.
Louis Alphonse was recognised by some members of the Capetian dynasty as Chef de la Maison de Bourbon (Head of the House of Bourbon) and took the title Duke of Anjou, but not his father's Spanish dukedom.
Louis Alphonse was the heir apparent to his mother's Spanish Dukedom of Franco and Grandeeship until the abolition of the titles by the Democratic Memory Law.
In 2002, Louis Alphonse was elected by the French Society of the Cincinnati as the representative of Louis XVI.
In addition to his Spanish citizenship, Louis Alphonse acquired French nationality through his paternal grandmother, Emmanuelle de Dampierre, also a French citizen.
In 2017, Louis Alphonse stated that he wishes for the remains of his ancestors, including King Charles X, to remain at the Kostanjevica Monastery, after a movement reportedly began to have the King's remains moved to be buried along with other French monarchs in Basilica of St Denis.
In 2021, Louis Alphonse attended the wedding of Grand Duke George Mikhailovich of Russia.
I consider it my role as head of the House of Bourbon and heir of the dynasty that made France to speak on the issue...At a moment of decision, I hope that the monarchical legacy of which I am the trustee is still sufficiently vibrant in the heart of my compatriots to be a source of inspiration and, I must say, hope."
- Louis Alphonse de Bourbon, in October 2025, amid the 2024–2025 French political crisis.
Louis Alphonse describes himself as a monarchist, "but not anti-republican".
In March 2018, Louis Alphonse was named honorary president of the Francisco Franco National Foundation, a position held by his grandmother, Carmen Franco, 1st Duchess of Franco, until her death in December 2017.
On 15 July, later that year, he headed a Movement-for-Spain demonstration at the Valley of the Fallen monument, leading supporters of the late Spanish dictator, his great-grandfather Francisco Franco.
They opposed the Spanish social democratic government's plan to remove Franco's remains from a basilica near Madrid.
"


Marriage and children

Louis Alphonse's engagement to marry María Margarita Vargas Santaella, the daughter of Venezuelan businessman Victor Vargas, was announced in November 2003.
Although no official reason was given, it was no secret that the then king of Spain, Juan Carlos I, did not approve his cousin's claim to the French throne, nor the fact that Louis Alphonse issued the wedding invitations styled as "Duke of Anjou".
Louis Alphonse and María Margarita had their first child, Eugénie, on 5 March 2007 at Mount Sinai Medical Center in Miami, Florida.
Her godparents are Prince Charles-Emmanuel of Bourbon-Parma and his wife, Constance.
French Legitimists recognize her as Eugénie, Madame Royale,: 47  the style commonly attributed to the eldest unmarried daughter of a king of France (in Spain her name is Dona Eugenia de Borbón y Vargas).
: 47 


The couple had twin sons, Louis and Alphonse, on 28 May 2010 in New York City.
In Spain, the twins are Don Luis and Don Alfonso de Borbón y Vargas.:



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
  AssignClass (19e23701-f82f-4ef9-873e-e0e70c0d35fe)
 Call ID: 19e23701-f82f-4ef9-873e-e0e70c0d35fe
  Args:
    type: :Man
    source: Louis_Alphonse_de_Bourbon
  AddLiteral (82712084-35a6-4248-986c-4339ea498bc4)
 Call ID: 82712084-35a6-4248-986c-4339ea498bc4
  Args:
    relation: :hasBirthYear
    literal_value: 1974
    source: Louis_Alphonse_de_Bourbon
    literal_type: xsd:integer
  AssignClass (706d1815-5c22-48df-a356-c4a31ff1e073)
 Call ID: 706d1815-5c22-48df-a356-c4a31ff1e073
  Args:
    type: :Man
    source: Alfonso_de_Borbon
  AssignClass (4f277be6-864d-48a2-93b1-467fe1577c6a)
 Call ID: 4f277be6-864d-48a2-93b1-467fe1577c6a
  Args:
    type: :Woman
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AddTriple (9491f0bf-fb64-4695-85d1-7a1395c174c3)
 Call ID: 9491f0bf-fb64-4695-85d1-7a1395c174c3
  Args:
    target: Alfonso_de_Borbon
    relation: :hasFather
    source: Louis_Alphonse_de_Bourbon
  AddTriple (9bec44f8-f235-4acf-b7e5-83778428b81b)
 Call ID: 9bec44f8-f235-4acf-b7e5-83778428b81b
  Args:
    source: Louis_Alphonse_de_Bourbon
    relation: :hasMother
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AssignClass (91586bde-d608-4693-b9f5-b8a2ad831bd6)
 Call ID: 91586bde-d608-4693-b9f5-b8a2ad831bd6
  Args:
    type: :Man
    source: Francisco_de_Borbon
  AddTriple (cd92e84a-c51c-4a07-b5a4-f013614e7f9a)
 Call ID: cd92e84a-c51c-4a07-b5a4-f013614e7f9a
  Args:
    relation: :hasBrother
    target: Francisco_de_Borbon
    source: Louis_Alphonse_de_Bourbon
  AddTriple (0ba238ba-f027-44a2-821f-492db243aea6)
 Call ID: 0ba238ba-f027-44a2-821f-492db243aea6
  Args:
    relation: :hasFather
    target: Alfonso_de_Borbon
    source: Francisco_de_Borbon
  AddTriple (3566b93f-a9ce-43e0-b9d2-d12523644ea5)
 Call ID: 3566b93f-a9ce-43e0-b9d2-d12523644ea5
  Args:
    source: Francisco_de_Borbon
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    relation: :hasMother
  AddLiteral (7b7375cb-4175-4b76-a8bc-f5c3fa3702ab)
 Call ID: 7b7375cb-4175-4b76-a8bc-f5c3fa3702ab
  Args:
    relation: :hasDeathYear
    literal_value: 1984
    literal_type: xsd:integer
    source: Francisco_de_Borbon
  AssignClass (371665cb-6259-48cc-a50b-a38fbc0c625b)
 Call ID: 371665cb-6259-48cc-a50b-a38fbc0c625b
  Args:
    type: :Man
    source: Jaime_de_Borbon
  AddTriple (cc0e8bcc-f42c-41a8-b7a7-006e2bcf59b4)
 Call ID: cc0e8bcc-f42c-41a8-b7a7-006e2bcf59b4
  Args:
    target: Jaime_de_Borbon
    relation: :hasFather
    source: Alfonso_de_Borbon
  AddLiteral (4f94e9c6-fa64-44a8-8c1c-c7ce68cbe091)
 Call ID: 4f94e9c6-fa64-44a8-8c1c-c7ce68cbe091
  Args:
    literal_value: 1975
    relation: :hasDeathYear
    source: Jaime_de_Borbon
    literal_type: xsd:integer
  AssignClass (5071c6a8-7f91-4c8f-bb89-1ec8e9559aa3)
 Call ID: 5071c6a8-7f91-4c8f-bb89-1ec8e9559aa3
  Args:
    type: :Man
    source: Francisco_Franco
  AddTriple (65137d19-6f15-4c01-b054-c1da1502464b)
 Call ID: 65137d19-6f15-4c01-b054-c1da1502464b
  Args:
    target: Francisco_Franco
    relation: :hasFather
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AssignClass (357fb5b4-68e4-4201-9013-0c4719618e75)
 Call ID: 357fb5b4-68e4-4201-9013-0c4719618e75
  Args:
    type: :Woman
    source: Maria_Margarita_Vargas_Santaella
  AddTriple (f844c8ba-c6e6-4989-86e0-ed81ad1fe824)
 Call ID: f844c8ba-c6e6-4989-86e0-ed81ad1fe824
  Args:
    source: Louis_Alphonse_de_Bourbon
    relation: :hasRelation
    target: Maria_Margarita_Vargas_Santaella
  AssignClass (856618e1-d4d3-4794-957d-b04757100e2b)
 Call ID: 856618e1-d4d3-4794-957d-b04757100e2b
  Args:
    type: :Woman
    source: Eugenie_de_Borbon_y_Vargas
  AddTriple (cd3f15ec-6b3a-4fb9-93f0-a333d22ddf6c)
 Call ID: cd3f15ec-6b3a-4fb9-93f0-a333d22ddf6c
  Args:
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
    source: Eugenie_de_Borbon_y_Vargas
  AddTriple (b41371a4-ec6b-49b3-88bd-c91c4b865ab3)
 Call ID: b41371a4-ec6b-49b3-88bd-c91c4b865ab3
  Args:
    source: Eugenie_de_Borbon_y_Vargas
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
  AssignClass (0d781d60-ae37-4f12-a274-368767cc6383)
 Call ID: 0d781d60-ae37-4f12-a274-368767cc6383
  Args:
    type: :Man
    source: Louis_de_Borbon_y_Vargas
  AddTriple (e207c7cc-92c7-4a24-ab85-ce37cef85542)
 Call ID: e207c7cc-92c7-4a24-ab85-ce37cef85542
  Args:
    source: Louis_de_Borbon_y_Vargas
    target: Louis_Alphonse_de_Bourbon
    relation: :hasFather
  AddTriple (43db1d5a-3512-4b43-b9d7-14993a059751)
 Call ID: 43db1d5a-3512-4b43-b9d7-14993a059751
  Args:
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
    source: Louis_de_Borbon_y_Vargas
  AssignClass (f78cd3f6-2f43-4ffe-b2ff-f4f44b5dc600)
 Call ID: f78cd3f6-2f43-4ffe-b2ff-f4f44b5dc600
  Args:
    type: :Man
    source: Alphonse_de_Borbon_y_Vargas
  AddTriple (aa649251-d82c-4797-8b77-04bbae6ffd83)
 Call ID: aa649251-d82c-4797-8b77-04bbae6ffd83
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    relation: :hasFather
    target: Louis_Alphonse_de_Bourbon
  AddTriple (60b36961-315f-423f-a84a-828754f5d38d)
 Call ID: 60b36961-315f-423f-a84a-828754f5d38d
  Args:
    source: Alphonse_de_Borbon_y_Vargas
    relation: :hasMother
    target: Maria_Margarita_Vargas_Santaella
  AssignClass (4658d4ae-f4e7-4065-8cc2-97d355763353)
 Call ID: 4658d4ae-f4e7-4065-8cc2-97d355763353
  Args:
    type: :Man
    source: Victor_Vargas
  AddTriple (742eced8-63a6-412b-b6cb-2ba427e50b9b)
 Call ID: 742eced8-63a6-412b-b6cb-2ba427e50b9b
  Args:
    source: Maria_Margarita_Vargas_Santaella
    target: Victor_Vargas
    relation: :hasFather
  AssignClass (14481a11-143c-4e7b-a9bf-9e495c3f861e)
 Call ID: 14481a11-143c-4e7b-a9bf-9e495c3f861e
  Args:
    type: :Woman
    source: Emmanuelle_de_Dampierre
  AddTriple (b7283c5f-dc03-4051-bb6f-b6ac024d3027)
 Call ID: b7283c5f-dc03-4051-bb6f-b6ac024d3027
  Args:
    source: Alfonso_de_Borbon
    relation: :hasMother
    target: Emmanuelle_de_Dampierre
  Finish (4bef61e8-dde5-4978-89dd-6cc03a36d869)
 Call ID: 4bef61e8-dde5-4978-89dd-6cc03a36d869
  Args: