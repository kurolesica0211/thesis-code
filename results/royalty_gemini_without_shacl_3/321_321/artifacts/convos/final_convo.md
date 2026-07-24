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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (190f82ce-e669-419c-9d1e-0fefa98460cc)
 Call ID: 190f82ce-e669-419c-9d1e-0fefa98460cc
  Args:
    type: :Man
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
  AssignClass (63e3374e-97b2-40e9-b0f7-ea2f3c75b67b)
 Call ID: 63e3374e-97b2-40e9-b0f7-ea2f3c75b67b
  Args:
    type: :Person
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
  AddLiteral (bdb16af9-5603-43e5-92a0-a8554cb8ddd0)
 Call ID: bdb16af9-5603-43e5-92a0-a8554cb8ddd0
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (ddbef04b-19bd-447d-bd59-272f3c0fa50f)
 Call ID: ddbef04b-19bd-447d-bd59-272f3c0fa50f
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    literal_type: xsd:integer
    literal_value: 2015
    relation: :hasDeathYear
  AssignClass (c471515c-b632-4d6a-aad1-eca15e8442ab)
 Call ID: c471515c-b632-4d6a-aad1-eca15e8442ab
  Args:
    type: :Man
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AssignClass (39bdb6fc-794d-4ecd-af86-6b16163752f2)
 Call ID: 39bdb6fc-794d-4ecd-af86-6b16163752f2
  Args:
    type: :Person
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AddLiteral (4f8ff3dc-a6ff-4533-a8f6-3bf9402fc7c6)
 Call ID: 4f8ff3dc-a6ff-4533-a8f6-3bf9402fc7c6
  Args:
    relation: :hasBirthYear
    literal_value: 1901
    literal_type: xsd:integer
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AddLiteral (482e4fbe-ede7-48cf-8554-a6729e7733a7)
 Call ID: 482e4fbe-ede7-48cf-8554-a6729e7733a7
  Args:
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AssignClass (c38faef3-710e-4a2b-b03f-fbfaa7db5023)
 Call ID: c38faef3-710e-4a2b-b03f-fbfaa7db5023
  Args:
    type: :Woman
    source: Alicia_of_Bourbon-Parma
  AssignClass (5cc9d40f-fa94-48cf-866c-b89b78af476d)
 Call ID: 5cc9d40f-fa94-48cf-866c-b89b78af476d
  Args:
    type: :Person
    source: Alicia_of_Bourbon-Parma
  AddLiteral (c3da50ca-f4a1-47f7-bca2-8eca1a9b33e3)
 Call ID: c3da50ca-f4a1-47f7-bca2-8eca1a9b33e3
  Args:
    relation: :hasBirthYear
    literal_value: 1917
    literal_type: xsd:integer
    source: Alicia_of_Bourbon-Parma
  AddLiteral (cdd4e9e1-b8a8-4cfc-9f1f-d62f34b47407)
 Call ID: cdd4e9e1-b8a8-4cfc-9f1f-d62f34b47407
  Args:
    source: Alicia_of_Bourbon-Parma
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2017
  AddTriple (1a6ddd68-1942-4567-8e58-e7cede2f8335)
 Call ID: 1a6ddd68-1942-4567-8e58-e7cede2f8335
  Args:
    relation: :hasFather
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    target: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AddTriple (38ef17cb-8e37-4e5e-acc9-5dc60a53b471)
 Call ID: 38ef17cb-8e37-4e5e-acc9-5dc60a53b471
  Args:
    target: Alicia_of_Bourbon-Parma
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    relation: :hasMother
  AssignClass (912d84d3-9b07-4c00-9b15-a4177a59b5aa)
 Call ID: 912d84d3-9b07-4c00-9b15-a4177a59b5aa
  Args:
    type: :Man
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (da6e6752-39cd-4a02-aaf6-177feb4632e2)
 Call ID: da6e6752-39cd-4a02-aaf6-177feb4632e2
  Args:
    type: :Person
    source: Carlo_of_Bourbon-Two_Sicilies
  AddLiteral (8c1f1e54-88a2-4faf-be12-54ded5e49374)
 Call ID: 8c1f1e54-88a2-4faf-be12-54ded5e49374
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1870
    source: Carlo_of_Bourbon-Two_Sicilies
  AddLiteral (8e6ad17e-40f8-43ea-a9f4-0d15c9a18543)
 Call ID: 8e6ad17e-40f8-43ea-a9f4-0d15c9a18543
  Args:
    literal_type: xsd:integer
    literal_value: 1949
    relation: :hasDeathYear
    source: Carlo_of_Bourbon-Two_Sicilies
  AssignClass (849b587c-c1d3-46bc-b7b2-bc5ae00177e6)
 Call ID: 849b587c-c1d3-46bc-b7b2-bc5ae00177e6
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (2902ce79-e395-42f7-8fbf-20802539201e)
 Call ID: 2902ce79-e395-42f7-8fbf-20802539201e
  Args:
    type: :Person
    source: Mercedes_Princess_of_Asturias
  AddLiteral (e2350b71-13e5-4fca-8c5c-6c78e6145016)
 Call ID: e2350b71-13e5-4fca-8c5c-6c78e6145016
  Args:
    source: Mercedes_Princess_of_Asturias
    relation: :hasBirthYear
    literal_value: 1880
    literal_type: xsd:integer
  AddLiteral (33aaaa06-73c7-4dc6-96c4-6c39899b4995)
 Call ID: 33aaaa06-73c7-4dc6-96c4-6c39899b4995
  Args:
    source: Mercedes_Princess_of_Asturias
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1904
  AddTriple (9de94bf3-2772-4bc2-8309-813f6ef8cf80)
 Call ID: 9de94bf3-2772-4bc2-8309-813f6ef8cf80
  Args:
    relation: :hasFather
    target: Carlo_of_Bourbon-Two_Sicilies
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AddTriple (bf07909d-ce9b-4441-a1f0-316dfdbf1a2b)
 Call ID: bf07909d-ce9b-4441-a1f0-316dfdbf1a2b
  Args:
    target: Mercedes_Princess_of_Asturias
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
    relation: :hasMother
  AssignClass (affb5c7d-a14e-4c89-9168-aa561ad9f20a)
 Call ID: affb5c7d-a14e-4c89-9168-aa561ad9f20a
  Args:
    type: :Woman
    source: Teresa_of_Bourbon-Dos_Sicilias
  AssignClass (2a561f07-58f0-444a-b116-d1234dde1a7e)
 Call ID: 2a561f07-58f0-444a-b116-d1234dde1a7e
  Args:
    type: :Person
    source: Teresa_of_Bourbon-Dos_Sicilias
  AddTriple (4fd90352-c28a-434f-a1a5-7956479d6999)
 Call ID: 4fd90352-c28a-434f-a1a5-7956479d6999
  Args:
    target: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
    source: Teresa_of_Bourbon-Dos_Sicilias
    relation: :hasFather
  AddTriple (a555f30e-fcbf-4add-87da-d7208c0b5cc0)
 Call ID: a555f30e-fcbf-4add-87da-d7208c0b5cc0
  Args:
    relation: :hasMother
    source: Teresa_of_Bourbon-Dos_Sicilias
    target: Alicia_of_Bourbon-Parma
  AssignClass (d09f7830-bd93-4d51-aeda-ba74519ab378)
 Call ID: d09f7830-bd93-4d51-aeda-ba74519ab378
  Args:
    type: :Woman
    source: Anne_of_Orleans
  AssignClass (eb11b33b-c4db-4a0f-a5e4-b5f7f8935177)
 Call ID: eb11b33b-c4db-4a0f-a5e4-b5f7f8935177
  Args:
    type: :Person
    source: Anne_of_Orleans
  AddTriple (94ad7dcd-0a14-4476-bf92-70c78f7c95c6)
 Call ID: 94ad7dcd-0a14-4476-bf92-70c78f7c95c6
  Args:
    relation: :hasRelation
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    target: Anne_of_Orleans
  AssignClass (bef77f00-3308-4719-b708-8cf545e6e8df)
 Call ID: bef77f00-3308-4719-b708-8cf545e6e8df
  Args:
    type: :Man
    source: Inigo_Moreno
  AssignClass (2f0c8f34-2f7a-4444-abaf-e10bf7b31f6e)
 Call ID: 2f0c8f34-2f7a-4444-abaf-e10bf7b31f6e
  Args:
    type: :Person
    source: Inigo_Moreno
  AddTriple (7e3cd110-6beb-4767-a7a3-1bdabc593d70)
 Call ID: 7e3cd110-6beb-4767-a7a3-1bdabc593d70
  Args:
    target: Inigo_Moreno
    source: Teresa_of_Bourbon-Dos_Sicilias
    relation: :hasRelation
  AssignClass (c4771a9f-591c-4557-b7b1-2b94e5f53b4e)
 Call ID: c4771a9f-591c-4557-b7b1-2b94e5f53b4e
  Args:
    type: :Man
    source: Juan_Carlos_I
  AssignClass (0e1d9755-740b-4643-91ca-0cc9470d5bb8)
 Call ID: 0e1d9755-740b-4643-91ca-0cc9470d5bb8
  Args:
    type: :Person
    source: Juan_Carlos_I
  AssignClass (d8c10036-d53a-4ad7-8ecb-11b4e651a1bb)
 Call ID: d8c10036-d53a-4ad7-8ecb-11b4e651a1bb
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (51bbc5b5-7d47-4c70-8a62-ebf279e2e7d2)
 Call ID: 51bbc5b5-7d47-4c70-8a62-ebf279e2e7d2
  Args:
    type: :Person
    source: Felipe_VI
  AssignClass (58bb23e4-d34c-4e38-bdbd-e783e20736ed)
 Call ID: 58bb23e4-d34c-4e38-bdbd-e783e20736ed
  Args:
    type: :Man
    source: Alfonso_XIII
  AssignClass (06441ae7-862a-402f-9195-21b7fd9b6cff)
 Call ID: 06441ae7-862a-402f-9195-21b7fd9b6cff
  Args:
    type: :Person
    source: Alfonso_XIII
  AssignClass (b206e3ab-7518-43bb-8cd8-f7931d785742)
 Call ID: b206e3ab-7518-43bb-8cd8-f7931d785742
  Args:
    type: :Man
    source: Alfonso_XII
  AssignClass (177be391-1e30-42d4-b4e9-c4c8e6b58871)
 Call ID: 177be391-1e30-42d4-b4e9-c4c8e6b58871
  Args:
    type: :Person
    source: Alfonso_XII
  AddTriple (c529e3ad-433c-4823-b267-396a2af72517)
 Call ID: c529e3ad-433c-4823-b267-396a2af72517
  Args:
    relation: :hasFather
    source: Mercedes_Princess_of_Asturias
    target: Alfonso_XII
  AssignClass (0c3f569e-b653-42d8-8927-232942f32318)
 Call ID: 0c3f569e-b653-42d8-8927-232942f32318
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (869cbc5d-9eeb-436e-8aaf-5f093203a295)
 Call ID: 869cbc5d-9eeb-436e-8aaf-5f093203a295
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddTriple (3a08b59d-a483-40ed-b3e4-b0f3d8f147b1)
 Call ID: 3a08b59d-a483-40ed-b3e4-b0f3d8f147b1
  Args:
    relation: :hasFather
    source: Anne_of_Orleans
    target: Henri_Count_of_Paris
  AssignClass (c7ff7add-899b-4436-a676-8f5eeff89493)
 Call ID: c7ff7add-899b-4436-a676-8f5eeff89493
  Args:
    type: :Man
    source: Ferdinand_Duke_of_Calabria
  AssignClass (b44cf923-4013-4de8-a341-eb2010c98f1c)
 Call ID: b44cf923-4013-4de8-a341-eb2010c98f1c
  Args:
    type: :Person
    source: Ferdinand_Duke_of_Calabria
  AssignClass (413f5cd8-85e5-435f-95e4-a4e05318cd24)
 Call ID: 413f5cd8-85e5-435f-95e4-a4e05318cd24
  Args:
    type: :Man
    source: Ranieri_Duke_of_Castro
  AssignClass (2c443491-94a3-4945-a40a-76883ed0901a)
 Call ID: 2c443491-94a3-4945-a40a-76883ed0901a
  Args:
    type: :Person
    source: Ranieri_Duke_of_Castro
  AddLiteral (e0b367b5-85f5-41b6-9f16-fd793fda9b26)
 Call ID: e0b367b5-85f5-41b6-9f16-fd793fda9b26
  Args:
    source: Ranieri_Duke_of_Castro
    relation: :hasBirthYear
    literal_value: 1883
    literal_type: xsd:integer
  AddLiteral (022b8a25-60af-4b1c-918a-b574b7db08f6)
 Call ID: 022b8a25-60af-4b1c-918a-b574b7db08f6
  Args:
    literal_type: xsd:integer
    literal_value: 1973
    relation: :hasDeathYear
    source: Ranieri_Duke_of_Castro
  AssignClass (ca9e454b-35a9-43fe-a08c-0091e9e2a592)
 Call ID: ca9e454b-35a9-43fe-a08c-0091e9e2a592
  Args:
    type: :Man
    source: Philip_V_of_Spain
  AssignClass (1f26b5ed-4bf3-401c-8b98-ae7819c914bc)
 Call ID: 1f26b5ed-4bf3-401c-8b98-ae7819c914bc
  Args:
    type: :Person
    source: Philip_V_of_Spain
  AssignClass (c6373120-cbea-4044-8f93-7f191ae97d57)
 Call ID: c6373120-cbea-4044-8f93-7f191ae97d57
  Args:
    type: :Man
    source: Charles_III_of_Spain
  AssignClass (038b192b-c9e3-4ca9-a5c9-cb68df1512c1)
 Call ID: 038b192b-c9e3-4ca9-a5c9-cb68df1512c1
  Args:
    type: :Person
    source: Charles_III_of_Spain
  AssignClass (171c3a79-556f-4c80-a6da-5d54434aff06)
 Call ID: 171c3a79-556f-4c80-a6da-5d54434aff06
  Args:
    type: :Man
    source: Ferdinand_I_of_the_Two_Sicilies
  AssignClass (7a248f03-2605-4756-b959-47a344a2069d)
 Call ID: 7a248f03-2605-4756-b959-47a344a2069d
  Args:
    type: :Person
    source: Ferdinand_I_of_the_Two_Sicilies
  AddTriple (428b25db-07d6-4000-92a8-f1f72a9d56be)
 Call ID: 428b25db-07d6-4000-92a8-f1f72a9d56be
  Args:
    relation: :hasFather
    source: Ferdinand_I_of_the_Two_Sicilies
    target: Charles_III_of_Spain
  AssignClass (e2b9f4ac-f0cb-4cc4-b6d2-0edf09aaca21)
 Call ID: e2b9f4ac-f0cb-4cc4-b6d2-0edf09aaca21
  Args:
    type: :Man
    source: Paul_of_the_Hellenes
  AssignClass (82baa9b5-1193-45d0-9794-e28e902ddfba)
 Call ID: 82baa9b5-1193-45d0-9794-e28e902ddfba
  Args:
    type: :Person
    source: Paul_of_the_Hellenes
  AssignClass (d3d4bdcc-885b-438e-8474-e1d2f8cb0a88)
 Call ID: d3d4bdcc-885b-438e-8474-e1d2f8cb0a88
  Args:
    type: :Woman
    source: Sophia_of_Greece
  AssignClass (f503a6ab-3b10-4154-a510-06f36d70ef5e)
 Call ID: f503a6ab-3b10-4154-a510-06f36d70ef5e
  Args:
    type: :Person
    source: Sophia_of_Greece
  AddTriple (36a44f5e-ace4-47ea-b88b-5a5095c58b4a)
 Call ID: 36a44f5e-ace4-47ea-b88b-5a5095c58b4a
  Args:
    target: Paul_of_the_Hellenes
    source: Sophia_of_Greece
    relation: :hasFather
  AssignClass (f4648359-f27f-40c7-9405-781afe1a8b03)
 Call ID: f4648359-f27f-40c7-9405-781afe1a8b03
  Args:
    type: :Man
    source: Carlo_Duke_of_Castro
  AssignClass (bc3d0675-aa5f-49a6-b08e-2327c1704b23)
 Call ID: bc3d0675-aa5f-49a6-b08e-2327c1704b23
  Args:
    type: :Person
    source: Carlo_Duke_of_Castro
  AssignClass (88eeba92-bc2e-4417-9186-65c1c3b72db3)
 Call ID: 88eeba92-bc2e-4417-9186-65c1c3b72db3
  Args:
    type: :Man
    source: Don_Juan_de_Borbon
  AssignClass (5551b6ce-41c5-481d-b17c-f492608f31fb)
 Call ID: 5551b6ce-41c5-481d-b17c-f492608f31fb
  Args:
    type: :Person
    source: Don_Juan_de_Borbon
  Finish (a54d3ae3-1d88-4101-9da8-ecae182291fa)
 Call ID: a54d3ae3-1d88-4101-9da8-ecae182291fa
  Args: