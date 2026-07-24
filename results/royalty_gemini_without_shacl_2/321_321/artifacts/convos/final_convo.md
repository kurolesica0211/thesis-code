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
  AssignClass (4e7788a4-a184-4984-a618-b06ba05128f7)
 Call ID: 4e7788a4-a184-4984-a618-b06ba05128f7
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    type: :Man
  AssignClass (adeb463e-1200-4ea8-9ad0-5aabd1cdb465)
 Call ID: adeb463e-1200-4ea8-9ad0-5aabd1cdb465
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    type: :Person
  AddLiteral (24672ddc-bbb1-4b5f-ab2a-d14ca0840a1d)
 Call ID: 24672ddc-bbb1-4b5f-ab2a-d14ca0840a1d
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    literal_value: 1938
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (c25c1526-c1b2-4ff9-8041-045f5d2895ef)
 Call ID: c25c1526-c1b2-4ff9-8041-045f5d2895ef
  Args:
    literal_value: 2015
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (7b7db35e-71ee-4874-8494-f74956774423)
 Call ID: 7b7db35e-71ee-4874-8494-f74956774423
  Args:
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
    type: :Man
  AssignClass (97f1ca92-9fd6-400e-ae2f-6c4ec657230f)
 Call ID: 97f1ca92-9fd6-400e-ae2f-6c4ec657230f
  Args:
    type: :Person
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AddLiteral (772831b0-19aa-41df-8e11-ce6a8c1946b9)
 Call ID: 772831b0-19aa-41df-8e11-ce6a8c1946b9
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
    literal_value: 1901
  AddLiteral (89d420c3-c47a-480b-a553-ab3d440a9c12)
 Call ID: 89d420c3-c47a-480b-a553-ab3d440a9c12
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1964
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AssignClass (d78fdff3-5fb7-410f-b23a-5d9f818fe2f3)
 Call ID: d78fdff3-5fb7-410f-b23a-5d9f818fe2f3
  Args:
    type: :Woman
    source: Alicia_of_Bourbon-Parma
  AssignClass (024a5668-3226-4428-8311-e325c0a54035)
 Call ID: 024a5668-3226-4428-8311-e325c0a54035
  Args:
    type: :Person
    source: Alicia_of_Bourbon-Parma
  AddLiteral (479b10bb-cb35-4172-a238-8a11451eea47)
 Call ID: 479b10bb-cb35-4172-a238-8a11451eea47
  Args:
    literal_value: 1917
    source: Alicia_of_Bourbon-Parma
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (212231a9-bd04-4643-999f-68b345d9a8b9)
 Call ID: 212231a9-bd04-4643-999f-68b345d9a8b9
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Alicia_of_Bourbon-Parma
    literal_value: 2017
  AddTriple (5a6b28aa-7b2c-47d5-9dea-6a693d2c0a36)
 Call ID: 5a6b28aa-7b2c-47d5-9dea-6a693d2c0a36
  Args:
    relation: :hasFather
    target: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
  AddTriple (0259ee98-b795-4972-8392-a8c6a3170249)
 Call ID: 0259ee98-b795-4972-8392-a8c6a3170249
  Args:
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    target: Alicia_of_Bourbon-Parma
    relation: :hasMother
  AssignClass (2ac8f82d-6f8d-4013-a67d-0d78e1972848)
 Call ID: 2ac8f82d-6f8d-4013-a67d-0d78e1972848
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (8ed24d23-e5ef-4dcf-9124-a6b3fcd880ee)
 Call ID: 8ed24d23-e5ef-4dcf-9124-a6b3fcd880ee
  Args:
    type: :Person
    source: Carlo_of_Bourbon-Two_Sicilies
  AddLiteral (73ebdc52-c58d-4add-b8ac-407c71596d06)
 Call ID: 73ebdc52-c58d-4add-b8ac-407c71596d06
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Carlo_of_Bourbon-Two_Sicilies
    literal_value: 1870
  AddLiteral (5bef7854-94e0-4571-91e0-268d4c719b02)
 Call ID: 5bef7854-94e0-4571-91e0-268d4c719b02
  Args:
    source: Carlo_of_Bourbon-Two_Sicilies
    literal_value: 1949
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (02024fde-59d6-4518-8786-250536259cf4)
 Call ID: 02024fde-59d6-4518-8786-250536259cf4
  Args:
    type: :Woman
    source: Mercedes_Princess_of_Asturias
  AssignClass (35e3a210-7497-4481-bf95-3edc4d838213)
 Call ID: 35e3a210-7497-4481-bf95-3edc4d838213
  Args:
    source: Mercedes_Princess_of_Asturias
    type: :Person
  AddLiteral (4ba1ef7e-c23d-4d37-ae55-fff9d0e9deb6)
 Call ID: 4ba1ef7e-c23d-4d37-ae55-fff9d0e9deb6
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1880
    source: Mercedes_Princess_of_Asturias
  AddLiteral (cbfcee1e-c76a-4a18-8ca2-1d5181554d5f)
 Call ID: cbfcee1e-c76a-4a18-8ca2-1d5181554d5f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1904
    source: Mercedes_Princess_of_Asturias
  AddTriple (875b4dc8-29c5-4a17-ad81-5d74712a2fec)
 Call ID: 875b4dc8-29c5-4a17-ad81-5d74712a2fec
  Args:
    relation: :hasFather
    target: Carlo_of_Bourbon-Two_Sicilies
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
  AddTriple (56faa1dd-3d73-40e5-9cdf-7e7c5df8a96f)
 Call ID: 56faa1dd-3d73-40e5-9cdf-7e7c5df8a96f
  Args:
    target: Mercedes_Princess_of_Asturias
    source: Alfonso_de_Borbon-Dos_Sicilias_y_Borbon
    relation: :hasMother
  AssignClass (e1d8a567-7c58-4be7-9ded-f7caa69c3221)
 Call ID: e1d8a567-7c58-4be7-9ded-f7caa69c3221
  Args:
    source: Teresa_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    type: :Woman
  AssignClass (299e1d84-39a3-448d-8a18-c92ed10be35b)
 Call ID: 299e1d84-39a3-448d-8a18-c92ed10be35b
  Args:
    source: Teresa_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    type: :Person
  AddTriple (38896cdb-73ef-4a44-8516-90cf10189475)
 Call ID: 38896cdb-73ef-4a44-8516-90cf10189475
  Args:
    source: Teresa_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    target: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    relation: :isSisterOf
  AssignClass (044d3053-2c4d-420b-a7c1-ed0d6e8c3764)
 Call ID: 044d3053-2c4d-420b-a7c1-ed0d6e8c3764
  Args:
    type: :Woman
    source: Anne_of_Orleans
  AssignClass (9835362a-7a09-48a3-ad7c-4cbdf10859c4)
 Call ID: 9835362a-7a09-48a3-ad7c-4cbdf10859c4
  Args:
    source: Anne_of_Orleans
    type: :Person
  AddTriple (7570713b-2f3e-4b30-8adb-6925f9d83a5c)
 Call ID: 7570713b-2f3e-4b30-8adb-6925f9d83a5c
  Args:
    target: Anne_of_Orleans
    source: Carlos_de_Borbon-Dos_Sicilias_y_Borbon-Parma
    relation: :hasRelation
  AssignClass (21a52faa-d9e3-4c47-9bd6-742760a8dc59)
 Call ID: 21a52faa-d9e3-4c47-9bd6-742760a8dc59
  Args:
    type: :Man
    source: Henri_Count_of_Paris
  AssignClass (3ae08c8f-f47a-4905-8327-f0e7082df56b)
 Call ID: 3ae08c8f-f47a-4905-8327-f0e7082df56b
  Args:
    type: :Person
    source: Henri_Count_of_Paris
  AddTriple (bab2f8b6-eb53-4731-9ef1-104e37472583)
 Call ID: bab2f8b6-eb53-4731-9ef1-104e37472583
  Args:
    target: Henri_Count_of_Paris
    source: Anne_of_Orleans
    relation: :hasFather
  Finish (f1dcd66b-79e1-4451-a46b-ec08e482fff0)
 Call ID: f1dcd66b-79e1-4451-a46b-ec08e482fff0
  Args: