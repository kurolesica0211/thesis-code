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
  AssignClass (cc4da4df-1896-48cd-8003-ce5c5420f616)
 Call ID: cc4da4df-1896-48cd-8003-ce5c5420f616
  Args:
    source: Carlos_de_Borbón-Dos_Sicilias
    type: :Man
  AssignClass (c28d8968-4826-4601-acf8-a40f11c25b25)
 Call ID: c28d8968-4826-4601-acf8-a40f11c25b25
  Args:
    type: :Person
    source: Carlos_de_Borbón-Dos_Sicilias
  AddLiteral (195aec43-f9ac-49f4-8a19-b8d6f85c548f)
 Call ID: 195aec43-f9ac-49f4-8a19-b8d6f85c548f
  Args:
    literal_value: 1938
    source: Carlos_de_Borbón-Dos_Sicilias
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (3b371ae0-a4c3-40ee-b75b-34c968e3cfed)
 Call ID: 3b371ae0-a4c3-40ee-b75b-34c968e3cfed
  Args:
    literal_value: 2015
    source: Carlos_de_Borbón-Dos_Sicilias
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (c6e3b4e0-e044-4f64-85f0-6da053c89a99)
 Call ID: c6e3b4e0-e044-4f64-85f0-6da053c89a99
  Args:
    source: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
    type: :Man
  AssignClass (0aba2740-bdaa-40a5-9589-9fcc7fb401f1)
 Call ID: 0aba2740-bdaa-40a5-9589-9fcc7fb401f1
  Args:
    source: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
    type: :Person
  AddLiteral (69b36155-ecbc-49e0-ac67-398d160455a3)
 Call ID: 69b36155-ecbc-49e0-ac67-398d160455a3
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1901
    source: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
  AddLiteral (a6c7ecf0-a4ec-460a-b13e-e2145694b7ca)
 Call ID: a6c7ecf0-a4ec-460a-b13e-e2145694b7ca
  Args:
    source: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (1d7ee78b-b527-453d-8125-23c0e32383b9)
 Call ID: 1d7ee78b-b527-453d-8125-23c0e32383b9
  Args:
    source: Alicia_of_Bourbon-Parma
    type: :Woman
  AssignClass (19943aff-7b52-467a-896d-56d953ba19c8)
 Call ID: 19943aff-7b52-467a-896d-56d953ba19c8
  Args:
    source: Alicia_of_Bourbon-Parma
    type: :Person
  AddLiteral (5e7153ba-96cf-4b2b-b888-5b2542e1f710)
 Call ID: 5e7153ba-96cf-4b2b-b888-5b2542e1f710
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1917
    source: Alicia_of_Bourbon-Parma
  AddLiteral (8be38892-52fc-4bcc-9d41-1f0b239099ea)
 Call ID: 8be38892-52fc-4bcc-9d41-1f0b239099ea
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 2017
    source: Alicia_of_Bourbon-Parma
  AddTriple (8db6ef39-c0e7-4366-acb3-394a1e5b910d)
 Call ID: 8db6ef39-c0e7-4366-acb3-394a1e5b910d
  Args:
    source: Carlos_de_Borbón-Dos_Sicilias
    relation: :hasFather
    target: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
  AddTriple (2937f07c-7127-413c-98b2-aa051e2f5d7c)
 Call ID: 2937f07c-7127-413c-98b2-aa051e2f5d7c
  Args:
    source: Carlos_de_Borbón-Dos_Sicilias
    target: Alicia_of_Bourbon-Parma
    relation: :hasMother
  AssignClass (71a73f67-dcef-40d2-97b7-57eeda3e5011)
 Call ID: 71a73f67-dcef-40d2-97b7-57eeda3e5011
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (6d3bb621-a280-4f8a-b5d9-51036167967c)
 Call ID: 6d3bb621-a280-4f8a-b5d9-51036167967c
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (79234541-8831-4c86-91a8-e69b747521a2)
 Call ID: 79234541-8831-4c86-91a8-e69b747521a2
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Carlo_of_Bourbon-Two_Sicilies
    literal_value: 1870
  AddLiteral (6c42bf01-a7ac-4377-a153-3ca546062ae1)
 Call ID: 6c42bf01-a7ac-4377-a153-3ca546062ae1
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    literal_value: 1949
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (4d245e62-96e4-4189-8859-5a78d3d969b1)
 Call ID: 4d245e62-96e4-4189-8859-5a78d3d969b1
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (5f0a062e-0f76-4f6b-9db2-0514966fd8e4)
 Call ID: 5f0a062e-0f76-4f6b-9db2-0514966fd8e4
  Args:
    type: :Person
    source: Mercedes_Princess_of_Asturias
  AddLiteral (af8e38b0-a8b4-46f3-8eec-c3593c201cc1)
 Call ID: af8e38b0-a8b4-46f3-8eec-c3593c201cc1
  Args:
    source: Mercedes_Princess_of_Asturias
    literal_value: 1880
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (879ef082-bdd5-496e-8d6b-809af559addb)
 Call ID: 879ef082-bdd5-496e-8d6b-809af559addb
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1904
    source: Mercedes_Princess_of_Asturias
  AddTriple (00ae9d75-fa8c-464c-9d74-89f698eb924b)
 Call ID: 00ae9d75-fa8c-464c-9d74-89f698eb924b
  Args:
    target: Carlo_of_Bourbon-Two_Sicilies
    relation: :hasFather
    source: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
  AddTriple (f78a84b7-1658-4bee-b945-200d8200c445)
 Call ID: f78a84b7-1658-4bee-b945-200d8200c445
  Args:
    target: Mercedes_Princess_of_Asturias
    relation: :hasMother
    source: Alfonso_de_Borbón-Dos_Sicilias_y_Borbón
  AssignClass (784786cc-3b95-4138-932f-42db0d8eeba3)
 Call ID: 784786cc-3b95-4138-932f-42db0d8eeba3
  Args:
    source: Teresa_of_Bourbon-Dos_Sicilias
    type: :Woman
  AssignClass (ff0c1eaf-9142-4701-b6ac-deb4600f7cdd)
 Call ID: ff0c1eaf-9142-4701-b6ac-deb4600f7cdd
  Args:
    source: Teresa_of_Bourbon-Dos_Sicilias
    type: :Person
  AddTriple (528aa4e0-20c0-4f54-aa85-8aaac070bdc4)
 Call ID: 528aa4e0-20c0-4f54-aa85-8aaac070bdc4
  Args:
    source: Carlos_de_Borbón-Dos_Sicilias
    target: Teresa_of_Bourbon-Dos_Sicilias
    relation: :hasSister
  AssignClass (1cc66d45-b6f5-4ac5-9157-0b2fada5f3c2)
 Call ID: 1cc66d45-b6f5-4ac5-9157-0b2fada5f3c2
  Args:
    type: :Woman
    source: Anne_of_Orléans
  AssignClass (5af8a7d2-1f9e-4c7c-bef8-65856b77e084)
 Call ID: 5af8a7d2-1f9e-4c7c-bef8-65856b77e084
  Args:
    type: :Person
    source: Anne_of_Orléans
  AddTriple (9fa612fa-0c76-4e63-8823-f69827fd1380)
 Call ID: 9fa612fa-0c76-4e63-8823-f69827fd1380
  Args:
    relation: :hasRelation
    target: Anne_of_Orléans
    source: Carlos_de_Borbón-Dos_Sicilias
  Finish (5e2f7293-0726-4175-b723-3fa48f3b6d06)
 Call ID: 5e2f7293-0726-4175-b723-3fa48f3b6d06
  Args: