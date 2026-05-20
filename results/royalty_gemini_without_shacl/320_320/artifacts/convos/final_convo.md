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
Don Carlos María Alfonso Marcelo de Borbón-Dos Sicilias y Borbón-Parma, Infante of Spain, Duke of Calabria (16 January 1938 – 5 October 2015) was, at his death, the last male infante of Spain during the reigns of his cousins King Juan Carlos I and King Felipe VI.
Early life and education

The second of three children and the only son of Infante Alfonso de Borbón-Dos Sicilias y Borbón (1901–1964) and Princess Alicia of Bourbon-Parma (1917–2017), he was born during his parents' exile from republican Spain in Lausanne, Switzerland.
As the elder son of Prince Carlo of Bourbon-Two Sicilies by Mercedes, Princess of Asturias (1880–1904), the eldest child of Alfonso XII of Spain, Alfonso had been heir presumptive to the Spanish throne between the death in childbirth of his mother and the birth in May 1907 of a son to his mother's brother, King Alfonso XIII.
If Mateu Morral’s attempt to assassinate King Alfonso XIII of Spain had succeeded, Infante Alfonso (Infante Carlos's father) would have become at that moment the King of Spain.
Raised from infancy side-by-side with his future king, Juan Carlos I (Carlos's elder by 11 days), the cousins attended school together first in Switzerland and later in Spain.
Carlos was chosen by the Spanish pretender, Don Juan de Borbón, Count of Barcelona, to become Juan Carlos's roommate at a boarding school that Don Juan and Spain's dictator Francisco Franco agreed to establish to bring the potential future king from his family's exile in Portugal to be educated in Spain.
In November 1948 Carlos and Juan Carlos took up residence there, along with eight selected sons of the aristocracy (and one commoner, the future cabinet member José Luis Leal Maldonado) and a team of tutors selected by Don Juan, including as headmaster the liberal scholar José Garrido, along with a traditionalist chaplain, Ignacio de Zulueta.
Family

Carlos lived in Madrid with his family.
Carlos met his future wife, Princess Anne of Orléans, in Madrid, at the wedding of his elder sister, Princess Teresa, with Don Iñigo Moreno, future Marquess of Laula.
In May 1962 they met again at the wedding in Athens of Infante Juan Carlos to Princess Sophia, daughter of the Greek king Paul of the Hellenes, appearing together at each of several occasions over the course of the week-long wedding celebrations.
Two months later, Anne was invited to and visited the home of Carlos's parents at Toledana.
Although both were Roman Catholic Bourbons by male-line descent, a disagreement now erupted between the couple's fathers about the dynastic claim of Carlos's father to the legacy of the deposed House of Bourbon-Two Sicilies dynasty, whose last undisputed head, Ferdinand, Duke of Calabria, died without a son in January 1960.
Carlos's father, Infante Alfonso, had asserted himself as rightful heir because his late father, Carlo of Bourbon-Two Sicilies (1870–1949), had been Ferdinand's next oldest brother.
Anne's father Henri, Count of Paris, however, upheld the claim of Ferdinand's next younger brother, Prince Ranieri, Duke of Castro (1883–1973) to the headship of the house, contending that Carlo had renounced his and his future descendants' Sicilian rights when he married the Spanish heiress presumptive, Mercedes of Asturias, in 1901, no doubt being mindful that his own claim to be head of the royal House of France depended upon the validity of the 1713 renunciation of a senior Bourbon prince, Philip V of Spain, in favor of the junior House of Orléans.
Carlos's father died in 1964, and with patience, persistence and compromise from afar, he eventually obtained the hand of his bride.
The 250 guests received one of two different invitations from either the bride's parents or the groom; the former referred to the bride's marriage to HRH Prince Carlos of Bourbon, while the latter announced the wedding of Princess Anne of France to the Duke of Calabria.
Issue

The couple had five children:


Endeavors

Departing Europe to spend a year abroad after his broken engagement, Carlos rounded out his study of the law with internships at several banks in the Americas, notably Chase Manhattan in New York, the National Bank of Mexico and the Banco Popular del Peru.
Following marriage, Carlos and his wife remained for sometime guests of the Marquès de Decio, head of the household of Infante Alfonso in his capacity as Duke of Calabria.
Carlos then launched a professional specialization in financial law and banking.
After his father's death in 1964 he also managed his family's large agricultural holdings in Spain.
Claimant

Infante Carlos was one of two claimants of the dignity of Head of the Royal House of the Two Sicilies.
The other claimant was his second cousin Prince Carlo of Bourbon-Two Sicilies, Duke of Castro.
Infante Carlos was also one of two claimants to the Grand Magistery of the Sacred Military Constantinian Order of Saint George; the other claimant is Carlo, Duke of Castro.
Infante Carlos was the senior male-line descendant of Ferdinand IV and III of Naples and Sicily (Ferdinand I of the Two Sicilies) and as such "first born legitimate heir of the Farnese" (primogenito legittimo farnesiano), as Ferdinand was designated by his father, King Charles III of Spain, on 16 October 1759 (ten days after abdicating the Two Sicilies Crown).
Although Ferdinand had two elder brothers, his eldest brother was mentally impaired and deemed unfit to inherit any crown; his next eldest brother, meanwhile, was his father's heir to the crown of Spain; treaty provisions prevented the union of the crowns of Spain, Naples and Sicily on the head of one person.
Titles and honors

Titles

Prince Carlos was created an Infante of Spain by King Juan Carlos I of Spain by Royal Decree 2412 dated 16 December 1994 as the "representative of a line linked historically to the Spanish Crown".
Infante Carlos was also President of the Spanish Foundation of the United World College, President of the Patronato of the Naval Museum, President of the Spanish Confederation of Foundations, President of the Iberoamerican Confederation of Foundations, President of the Foundation of San Benito de Alcántara, and President of the Foundation for the Protection of Nature (Fundación Fondo para la Protección de la Naturaleza).
Under the traditional succession laws of the Kingdom of Navarre, Carlos's mother Infanta Alicia, born a Princess of Bourbon-Parma, was the claimant to that throne, which was formally united with the Kingdom of France in the seventeenth century.



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
  AssignClass (544a004a-ba1c-472c-8c8f-1c5c796fb136)
 Call ID: 544a004a-ba1c-472c-8c8f-1c5c796fb136
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias
    type: :Man
  AssignClass (3163388b-cc4d-4fae-8f9c-c91e464e97ab)
 Call ID: 3163388b-cc4d-4fae-8f9c-c91e464e97ab
  Args:
    type: :Person
    source: Carlos_de_Borbon-Dos_Sicilias
  AssignClass (bb20a6e0-cad1-43f3-9c75-d6bf0176aaae)
 Call ID: bb20a6e0-cad1-43f3-9c75-d6bf0176aaae
  Args:
    type: :Ancestor
    source: Carlos_de_Borbon-Dos_Sicilias
  AddLiteral (74a8f1bc-32ca-4caf-bd6a-902fecc5708e)
 Call ID: 74a8f1bc-32ca-4caf-bd6a-902fecc5708e
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias
    literal_value: 1938
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4803c5c5-e677-4add-8344-262ac0c35a47)
 Call ID: 4803c5c5-e677-4add-8344-262ac0c35a47
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias
    literal_value: 2015
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (4abbf91c-7b79-44a7-9f9b-b929609c345c)
 Call ID: 4abbf91c-7b79-44a7-9f9b-b929609c345c
  Args:
    source: Alfonso_de_Borbon-Dos_Sicilias
    type: :Man
  AssignClass (a32bb117-e35b-4c32-99a1-0989cfa0234d)
 Call ID: a32bb117-e35b-4c32-99a1-0989cfa0234d
  Args:
    type: :Person
    source: Alfonso_de_Borbon-Dos_Sicilias
  AssignClass (0ab3dcd2-a5e4-426d-882a-2d92c1d41974)
 Call ID: 0ab3dcd2-a5e4-426d-882a-2d92c1d41974
  Args:
    source: Alfonso_de_Borbon-Dos_Sicilias
    type: :Ancestor
  AddLiteral (38fd14f0-1778-4338-ac9c-8132c002cab4)
 Call ID: 38fd14f0-1778-4338-ac9c-8132c002cab4
  Args:
    relation: :hasBirthYear
    literal_value: 1901
    literal_type: xsd:integer
    source: Alfonso_de_Borbon-Dos_Sicilias
  AddLiteral (736bfa27-bc4e-4503-bc51-2e26e7d552cd)
 Call ID: 736bfa27-bc4e-4503-bc51-2e26e7d552cd
  Args:
    source: Alfonso_de_Borbon-Dos_Sicilias
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1964
  AssignClass (5d33bab2-d928-4282-9577-b8ddb425e38e)
 Call ID: 5d33bab2-d928-4282-9577-b8ddb425e38e
  Args:
    type: :Woman
    source: Alicia_of_Bourbon-Parma
  AssignClass (a3b865ac-2e09-4cc1-9ab9-485070689528)
 Call ID: a3b865ac-2e09-4cc1-9ab9-485070689528
  Args:
    source: Alicia_of_Bourbon-Parma
    type: :Person
  AssignClass (f8fba7fc-4dcf-41f6-845f-d39b29ce27c5)
 Call ID: f8fba7fc-4dcf-41f6-845f-d39b29ce27c5
  Args:
    type: :Ancestor
    source: Alicia_of_Bourbon-Parma
  AddLiteral (d6a328a9-e59d-4a44-9a16-228ae1245b37)
 Call ID: d6a328a9-e59d-4a44-9a16-228ae1245b37
  Args:
    literal_value: 1917
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Alicia_of_Bourbon-Parma
  AddLiteral (2d325f05-5abd-48ee-a200-e1b0765178c5)
 Call ID: 2d325f05-5abd-48ee-a200-e1b0765178c5
  Args:
    source: Alicia_of_Bourbon-Parma
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2017
  AddTriple (303fa739-6a17-47c8-8625-0e51018e1106)
 Call ID: 303fa739-6a17-47c8-8625-0e51018e1106
  Args:
    target: Alfonso_de_Borbon-Dos_Sicilias
    relation: :hasFather
    source: Carlos_de_Borbon-Dos_Sicilias
  AddTriple (5e447870-5dcb-45cb-8d67-72a7fa4a526a)
 Call ID: 5e447870-5dcb-45cb-8d67-72a7fa4a526a
  Args:
    target: Alicia_of_Bourbon-Parma
    relation: :hasMother
    source: Carlos_de_Borbon-Dos_Sicilias
  AssignClass (26a9e84f-0585-431e-a8c0-8a7b7af85b19)
 Call ID: 26a9e84f-0585-431e-a8c0-8a7b7af85b19
  Args:
    type: :Man
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (5bb7be88-133c-4b02-8bd2-e3d1610cd3f7)
 Call ID: 5bb7be88-133c-4b02-8bd2-e3d1610cd3f7
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (eba12896-f283-4f75-b1d3-5e4bdb809dac)
 Call ID: eba12896-f283-4f75-b1d3-5e4bdb809dac
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    type: :Ancestor
  AddLiteral (23b2245d-1ad4-4a88-8075-92d4f56c2791)
 Call ID: 23b2245d-1ad4-4a88-8075-92d4f56c2791
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_value: 1870
    literal_type: xsd:integer
  AddLiteral (d5d41c2f-59f3-4749-92cd-cd2cecb910c5)
 Call ID: d5d41c2f-59f3-4749-92cd-cd2cecb910c5
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1949
  AssignClass (e6d2c2fb-0ddf-4f37-95c0-a792b037c6f8)
 Call ID: e6d2c2fb-0ddf-4f37-95c0-a792b037c6f8
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (15f75c66-f7da-414e-9977-0407cf39b82b)
 Call ID: 15f75c66-f7da-414e-9977-0407cf39b82b
  Args:
    type: :Person
    source: Mercedes_Princess_of_Asturias
  AssignClass (2ca6f013-8b92-412e-aaab-7ae50c5248c0)
 Call ID: 2ca6f013-8b92-412e-aaab-7ae50c5248c0
  Args:
    source: Mercedes_Princess_of_Asturias
    type: :Ancestor
  AddLiteral (edd0aa48-d099-419b-a32b-093d493d1888)
 Call ID: edd0aa48-d099-419b-a32b-093d493d1888
  Args:
    source: Mercedes_Princess_of_Asturias
    relation: :hasBirthYear
    literal_value: 1880
    literal_type: xsd:integer
  AddLiteral (adcb6e2c-f335-4fbb-aed4-9c6a358283a2)
 Call ID: adcb6e2c-f335-4fbb-aed4-9c6a358283a2
  Args:
    source: Mercedes_Princess_of_Asturias
    relation: :hasDeathYear
    literal_value: 1904
    literal_type: xsd:integer
  AddTriple (1db97e2f-82fc-4e67-8aa2-610f6846a893)
 Call ID: 1db97e2f-82fc-4e67-8aa2-610f6846a893
  Args:
    target: Carlo_of_Bourbon-Two_Sicilies
    source: Alfonso_de_Borbon-Dos_Sicilias
    relation: :hasFather
  AddTriple (1f9d042a-ff9b-442f-908a-2009f846abde)
 Call ID: 1f9d042a-ff9b-442f-908a-2009f846abde
  Args:
    target: Mercedes_Princess_of_Asturias
    source: Alfonso_de_Borbon-Dos_Sicilias
    relation: :hasMother
  AssignClass (1e0b08ee-5dc1-4d59-bee2-4d535d631cce)
 Call ID: 1e0b08ee-5dc1-4d59-bee2-4d535d631cce
  Args:
    type: :Woman
    source: Teresa_de_Borbon-Dos_Sicilias
  AssignClass (9141a172-2f99-4fcc-abca-74c16025264b)
 Call ID: 9141a172-2f99-4fcc-abca-74c16025264b
  Args:
    type: :Person
    source: Teresa_de_Borbon-Dos_Sicilias
  AddTriple (bfc7eefd-2eb2-4f91-9a29-6d71ec79104f)
 Call ID: bfc7eefd-2eb2-4f91-9a29-6d71ec79104f
  Args:
    target: Teresa_de_Borbon-Dos_Sicilias
    source: Carlos_de_Borbon-Dos_Sicilias
    relation: :hasSister
  AssignClass (a39b8fae-8aca-4032-861c-d51f63979831)
 Call ID: a39b8fae-8aca-4032-861c-d51f63979831
  Args:
    source: Anne_of_Orleans
    type: :Woman
  AssignClass (8fe2c786-a0f0-46d7-9b4b-7ed3ce48da56)
 Call ID: 8fe2c786-a0f0-46d7-9b4b-7ed3ce48da56
  Args:
    type: :Person
    source: Anne_of_Orleans
  AssignClass (fcde463a-57e7-4efa-9355-a756cd852adf)
 Call ID: fcde463a-57e7-4efa-9355-a756cd852adf
  Args:
    type: :Ancestor
    source: Anne_of_Orleans
  AddTriple (edbf1f18-459b-4ea5-b530-e46a0830672b)
 Call ID: edbf1f18-459b-4ea5-b530-e46a0830672b
  Args:
    target: Anne_of_Orleans
    source: Carlos_de_Borbon-Dos_Sicilias
    relation: :hasRelation
  Finish (a97513c0-9a52-4f74-8ac2-05ecf25062b9)
 Call ID: a97513c0-9a52-4f74-8ac2-05ecf25062b9
  Args: